"""HSRL training stages (Sec. 3.3) and the supervised-only baseline.

LEAKAGE RULE: every function here reads labels/votes only from ctx.data.labelled. Unlabelled, val and test
tables carry ids and paths only; ctx.data.eval_labels is never called in this module. epoch_hook (optional) is
evaluation code supplied by train.py; it runs after an epoch has trained and never changes training.
"""
import csv
import time

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader

from .data import ImageDataset, build_transforms
from .losses import build_structural_loss, soft_cross_entropy
from .mining import mine_tuples
from .samplers import ClassBalancedBatchSampler

LOG_FIELDS = ["stage", "epoch", "step", "loss", "lr", "n_tuples", "t1", "t2", "t3",
              "frac_t1_active", "frac_t2_active", "frac_t3_active", "acc"]
TUPLE_FIELDS = ["epoch", "step", "anchor_id", "pos_id", "neg_id", "conf_id", "d_ap", "d_an", "d_nc", "d_ac",
                "t1", "t2", "t3", "t1_active", "t2_active", "t3_active"]


class Ctx:
    def __init__(self, cfg, data, run_dir, device):
        self.cfg, self.data, self.run_dir, self.device = cfg, data, run_dir, device
        self.seed = cfg["seed"]
        amp = cfg.get("amp", "bf16")
        self.amp_dtype = {"bf16": torch.bfloat16, "fp16": torch.float16, "none": None}[amp]
        self.log_f = open(run_dir / "train_log.csv", "w", newline="")
        self.log = csv.DictWriter(self.log_f, LOG_FIELDS)
        self.log.writeheader()
        self.global_step = 0

    def autocast(self):
        return torch.autocast("cuda", dtype=self.amp_dtype or torch.float32, enabled=self.amp_dtype is not None
                              and self.device.type == "cuda")

    def write_log(self, **row):
        self.log.writerow({k: row.get(k, "") for k in LOG_FIELDS})

    def close(self):
        self.log_f.close()


def _seed_worker(worker_id):
    s = torch.initial_seed() % 2**32
    np.random.seed(s)
    import random
    random.seed(s)


def make_loader(ctx, df, train, batch_size=None, targets=None, soft=None, shuffle=False, batch_sampler=None,
                stream=0, num_workers=None):
    ds = ImageDataset(df, ctx.data.image_root, build_transforms(ctx.cfg["augment"], train), targets, soft)
    g = torch.Generator()
    g.manual_seed(ctx.seed * 1000 + stream)
    nw = ctx.cfg["data"].get("num_workers", 4) if num_workers is None else num_workers
    kw = dict(num_workers=nw, pin_memory=ctx.device.type == "cuda", worker_init_fn=_seed_worker, generator=g,
              persistent_workers=nw > 0)
    if batch_sampler is not None:
        return DataLoader(ds, batch_sampler=batch_sampler, **kw)
    return DataLoader(ds, batch_size=batch_size, shuffle=shuffle, drop_last=False, **kw)


def set_trainable(model, f, g, h):
    for mod, flag in ((model.f, f), (model.g, g), (model.h, h)):
        for p in mod.parameters():
            p.requires_grad_(flag)


def _adamw(params, c):
    return torch.optim.AdamW([p for p in params if p.requires_grad], lr=c["lr"], weight_decay=c["weight_decay"])


def hard_or_soft_targets(df, mode, n_classes):
    """(N, K) target matrix for the labelled table: one-hot majority labels or soft (1-q, q)."""
    if mode == "hard":
        return np.eye(n_classes, dtype=np.float32)[df["label"].to_numpy()]
    if mode == "soft":
        assert n_classes == 2, "soft targets defined for binary q"
        q = df["q"].to_numpy(dtype=np.float32)
        return np.stack([1 - q, q], 1)
    raise ValueError(mode)


# --------------------------------------------------------------------------------------------- Stage I
def labelled_votes(ctx):
    """Votes of the labelled training table, the only vote-bearing table (LEAKAGE RULE), for vote-aware Stage I
    losses. q = votes / readers exactly (the csv rounds q). Reader columns already carry the vote mode."""
    lab = ctx.data.labelled
    k, R = lab.votes_g4.to_numpy(float), lab.n_readers.to_numpy(float)
    if not np.allclose(k / R, lab.q.to_numpy(float), atol=1e-5):
        raise ValueError("labelled q differs from votes_g4 / n_readers")
    rc = [c for c in ctx.data.reader_cols if c in lab]
    return {"V": lab[rc].fillna(-1).to_numpy(np.int64), "q": k / R, "k": k, "R": R,
            "mode": ctx.cfg["data"].get("vote_mode", "linked"), "min_shared": ctx.cfg["stage1"].get("min_shared", 3)}


def tuple_votes(votes, bidx, tuples, device):
    """Per-tuple vote information for the mined tuples of one batch (bidx maps batch rows to labelled rows)."""
    from .agreement import PAIR_ROLES, pair_bounds
    g = {r: bidx[tuples[r].cpu().numpy()] for r in "apnc"}
    meta = {"L": {}, "U": {}, "k": {r: votes["k"][g[r]] for r in "apnc"}, "R": {r: votes["R"][g[r]] for r in "apnc"},
            "q": {r: torch.as_tensor(votes["q"][g[r]], dtype=torch.float32, device=device) for r in "apnc"}}
    for name, (u, v) in PAIR_ROLES.items():
        L, U, _ = pair_bounds(votes["V"], votes["q"], g[u], g[v], votes["mode"], votes["min_shared"])
        meta["L"][name] = torch.as_tensor(L, dtype=torch.float32, device=device)
        meta["U"][name] = torch.as_tensor(U, dtype=torch.float32, device=device)
    return meta


def stage1(ctx, model, monitor=None):
    """monitor(epoch, model, tuple_stats) is called before training (epoch=-1) and after every epoch; it is
    evaluation code supplied by train.py (collapse monitoring) and must not change the model."""
    c = ctx.cfg["stage1"]
    lab = ctx.data.labelled
    assert (lab.label >= 0).all(), "Stage I needs majority labels (ties excluded)"
    set_trainable(model, f=True, g=True, h=False)
    model.train()
    opt = _adamw(list(model.f.parameters()) + list(model.g.parameters()), c)
    sampler = ClassBalancedBatchSampler(lab.label.to_numpy(), c["batch_size"], seed=ctx.seed)
    dl = make_loader(ctx, lab, train=True, targets=lab.label, batch_sampler=sampler, stream=1)
    loss_fn = build_structural_loss(c)
    votes = labelled_votes(ctx) if getattr(loss_fn, "needs_votes", False) else None
    gen = torch.Generator().manual_seed(ctx.seed)
    select_gen = torch.Generator().manual_seed(ctx.seed + 7919)   # random controls; leaves the mining stream unchanged
    ids = lab.patch_id.to_numpy()
    tuple_path = ctx.run_dir / "tuples_stage1.csv"
    first = True
    history = []
    if monitor is not None:
        monitor(-1, model, {})
        model.train()
    for ep in range(c["epochs"]):
        t0, losses = time.time(), []
        acc_stats = {k: [] for k in ("d_ap", "d_an", "d_nc", "d_ac", "t1", "t2", "t3")}
        sel_stats = {}
        for b in dl:
            x = b["image"].to(ctx.device, non_blocking=True)
            y = b["target"].to(ctx.device)
            with ctx.autocast():
                feats = model.features(x)
            z = model.embed(feats)
            tuples = mine_tuples(z, y, c.get("conf_rule", "second_nearest"), gen)
            meta = {"labels": y}
            if votes is not None:
                meta.update(tuple_votes(votes, b["idx"].numpy(), tuples, ctx.device), gen=select_gen)
            loss, lg = loss_fn(z, tuples, meta)
            for k in (k for k in lg if k.startswith(("cert", "kept", "margin"))):
                sel_stats.setdefault(k, []).append(lg[k].cpu())
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()

            losses.append(loss.item())
            for k in acc_stats:
                acc_stats[k].append(lg[k].cpu())
            act = {k: (lg[k] > 0).float().mean().item() for k in ("t1", "t2", "t3")}
            ctx.write_log(stage="stage1", epoch=ep, step=ctx.global_step, loss=loss.item(), lr=c["lr"],
                          n_tuples=len(tuples["a"]), t1=lg["t1"].mean().item(), t2=lg["t2"].mean().item(),
                          t3=lg["t3"].mean().item(), frac_t1_active=act["t1"], frac_t2_active=act["t2"],
                          frac_t3_active=act["t3"])
            if c.get("log_tuples", True):
                bidx = b["idx"].numpy()
                tid = {k: ids[bidx[tuples[k].cpu().numpy()]] for k in ("a", "p", "n", "c")}
                df = pd.DataFrame({"epoch": ep, "step": ctx.global_step, "anchor_id": tid["a"], "pos_id": tid["p"],
                                   "neg_id": tid["n"], "conf_id": tid["c"],
                                   **{k: lg[k].cpu().numpy().round(6) for k in ("d_ap", "d_an", "d_nc", "d_ac", "t1", "t2", "t3")},
                                   **{f"{k}_active": (lg[k] > 0).cpu().numpy().astype(int) for k in ("t1", "t2", "t3")},
                                   **{k: lg[k].cpu().numpy().astype(int) for k in ("kept1", "kept2", "kept3") if k in lg}})
                fields = TUPLE_FIELDS + [k for k in ("kept1", "kept2", "kept3") if k in lg]
                df[fields].to_csv(tuple_path, mode="w" if first else "a", header=first, index=False)
                first = False
            ctx.global_step += 1
        cat = {k: torch.cat(v) for k, v in acc_stats.items()}
        ts = {**{f"mean_{k}": cat[k].mean().item() for k in ("d_ap", "d_an", "d_nc", "d_ac")},
              **{f"frac_{k}_active": (cat[k] > 0).float().mean().item() for k in ("t1", "t2", "t3")},
              **{f"frac_{k}": torch.cat(v).mean().item() for k, v in sel_stats.items() if not k.startswith("margin")},
              **{f"mean_{k}_kept": (torch.cat(v).sum() / torch.cat(sel_stats[f"kept{k[-1]}"]).sum().clamp(min=1)).item()
                 for k, v in sel_stats.items() if k.startswith("margin")}}
        history.append({"epoch": ep, "loss": float(np.mean(losses)), "sec": time.time() - t0, **ts})
        print(f"[stage1] epoch {ep} loss {history[-1]['loss']:.4f} d_ap {ts['mean_d_ap']:.3f} d_an {ts['mean_d_an']:.3f} "
              f"({history[-1]['sec']:.1f}s)", flush=True)
        if monitor is not None:
            monitor(ep, model, ts)
            model.train()
    return history


# --------------------------------------------------------------------------------------------- Stage II
def stage2(ctx, model, epoch_hook=None):
    c = ctx.cfg["stage2"]
    lab = ctx.data.labelled
    set_trainable(model, f=False, g=False, h=True)
    tgt = hard_or_soft_targets(lab, c.get("targets", "hard"), ctx.data.n_classes)
    dl = make_loader(ctx, lab, train=True, batch_size=c["batch_size"], targets=lab.label.clip(lower=0),
                     soft=tgt, shuffle=True, stream=2)
    opt = _adamw(model.h.parameters(), c)
    history = []
    for ep in range(c["epochs"]):
        model.f.eval()   # frozen backbone: BN running statistics are not updated
        model.h.train()
        t0, losses, correct, n = time.time(), [], 0, 0
        for b in dl:
            x = b["image"].to(ctx.device, non_blocking=True)
            with torch.no_grad(), ctx.autocast():
                feats = model.features(x)
            logits = model.classify(feats)
            loss = soft_cross_entropy(logits, b["soft"].to(ctx.device))
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
            losses.append(loss.item())
            correct += (logits.argmax(1).cpu() == b["target"]).sum().item()
            n += len(x)
            ctx.write_log(stage="stage2", epoch=ep, step=ctx.global_step, loss=loss.item(), lr=c["lr"])
            ctx.global_step += 1
        history.append({"epoch": ep, "loss": float(np.mean(losses)), "train_acc": correct / n, "sec": time.time() - t0})
        print(f"[stage2] epoch {ep} loss {history[-1]['loss']:.4f} acc {correct / n:.3f}", flush=True)
        if epoch_hook:
            epoch_hook("stage2", ep, model)
    return history


# --------------------------------------------------------------------------------------------- prediction
@torch.no_grad()
def predict(ctx, model, df, batch_size=128, embeddings=False, stream=9):
    model.eval()
    dl = make_loader(ctx, df, train=False, batch_size=batch_size, stream=stream)
    probs, zs = [], []
    for b in dl:
        x = b["image"].to(ctx.device, non_blocking=True)
        with ctx.autocast():
            feats = model.features(x)
        probs.append(F.softmax(model.classify(feats), 1).cpu())
        if embeddings:
            zs.append(model.embed(feats).cpu())
    probs = torch.cat(probs).numpy()
    out = pd.DataFrame({"patch_id": df.patch_id.to_numpy(), **{f"prob_{k}": probs[:, k] for k in range(probs.shape[1])}})
    return (out, torch.cat(zs).numpy()) if embeddings else out


# --------------------------------------------------------------------------------------------- Stage III
def pseudo_label(ctx, model, round_idx):
    c = ctx.cfg["stage3"]
    pr = predict(ctx, model, ctx.data.unlabelled, stream=10 + round_idx)
    P = pr.filter(like="prob_").to_numpy()
    pr["p_max"] = P.max(1)
    pr["pseudo"] = P.argmax(1)
    pr["accepted"] = (pr.p_max > c["tau"]).astype(int)
    pr.to_csv(ctx.run_dir / f"pseudo_labels_round{round_idx}.csv", index=False)
    return pr


def stage3(ctx, model, epoch_hook=None):
    c = ctx.cfg["stage3"]
    K = ctx.data.n_classes
    lab = ctx.data.labelled
    lab_t = hard_or_soft_targets(lab, c.get("labelled_targets", "hard"), K)
    set_trainable(model, f=True, g=True, h=True)
    opt = _adamw(model.parameters(), c)
    history, dl = [], None
    for ep in range(c["epochs"]):
        if ep == 0 or c.get("refresh_every_epoch", False):
            pr = pseudo_label(ctx, model, ep)
            acc = ctx.data.unlabelled.merge(pr[pr.accepted == 1][["patch_id", "pseudo"]], on="patch_id")
            df = pd.concat([lab[["patch_id", "path"]], acc[["patch_id", "path"]]], ignore_index=True)
            tgt = np.concatenate([lab_t, np.eye(K, dtype=np.float32)[acc.pseudo.to_numpy()]])
            hard = np.concatenate([lab.label.clip(lower=0).to_numpy(), acc.pseudo.to_numpy()])
            dl = make_loader(ctx, df, train=True, batch_size=c["batch_size"], targets=hard, soft=tgt, shuffle=True,
                             stream=3 + ep)
            n_acc = int(len(acc))
            print(f"[stage3] round {ep}: accepted {n_acc}/{len(pr)} pseudo-labels "
                  f"(class counts {np.bincount(acc.pseudo, minlength=K).tolist()})", flush=True)
        model.train()
        t0, losses = time.time(), []
        for b in dl:
            x = b["image"].to(ctx.device, non_blocking=True)
            with ctx.autocast():
                logits = model(x)
            loss = soft_cross_entropy(logits, b["soft"].to(ctx.device))
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
            losses.append(loss.item())
            ctx.write_log(stage="stage3", epoch=ep, step=ctx.global_step, loss=loss.item(), lr=c["lr"])
            ctx.global_step += 1
        history.append({"epoch": ep, "loss": float(np.mean(losses)), "n_pseudo": n_acc,
                        "pseudo_coverage": n_acc / len(ctx.data.unlabelled), "sec": time.time() - t0})
        print(f"[stage3] epoch {ep} loss {history[-1]['loss']:.4f} ({history[-1]['sec']:.1f}s)", flush=True)
        if epoch_hook:
            epoch_hook("stage3", ep, model)
    return history


# --------------------------------------------------------------------------------------------- baseline
def supervised(ctx, model, epoch_hook=None):
    """Supervised-only baseline: f + h trained end-to-end with cross-entropy on the labelled set only."""
    c = ctx.cfg["supervised"]
    lab = ctx.data.labelled
    set_trainable(model, f=True, g=False, h=True)
    tgt = hard_or_soft_targets(lab, c.get("targets", "hard"), ctx.data.n_classes)
    dl = make_loader(ctx, lab, train=True, batch_size=c["batch_size"], targets=lab.label.clip(lower=0), soft=tgt,
                     shuffle=True, stream=4)
    opt = _adamw(list(model.f.parameters()) + list(model.h.parameters()), c)
    history = []
    for ep in range(c["epochs"]):
        model.train()
        t0, losses = time.time(), []
        for b in dl:
            x = b["image"].to(ctx.device, non_blocking=True)
            with ctx.autocast():
                logits = model(x)
            loss = soft_cross_entropy(logits, b["soft"].to(ctx.device))
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
            losses.append(loss.item())
            ctx.write_log(stage="supervised", epoch=ep, step=ctx.global_step, loss=loss.item(), lr=c["lr"])
            ctx.global_step += 1
        history.append({"epoch": ep, "loss": float(np.mean(losses)), "sec": time.time() - t0})
        print(f"[supervised] epoch {ep} loss {history[-1]['loss']:.4f}", flush=True)
        if epoch_hook:
            epoch_hook("supervised", ep, model)
    return history
