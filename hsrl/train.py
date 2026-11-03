"""Entry point: one run = one method on one fold with one seed, written to results/<run_name>/.

Usage:  python -I hsrl/train.py --config configs/hsrl_gleason.yaml [dotted.key=value ...]
"""
import argparse
import sys
import time
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
import timm
import torch

from hsrl.data import load_dataset
from hsrl.evaluate import evaluate_predictions, pseudo_label_diagnostics
from hsrl.models import HSRLNet, param_counts
from hsrl import stages
from hsrl.utils import load_config, make_run_dir, save_json, save_yaml, set_seed


def subset_data(data, spec, seed):
    """Deterministic tiny subset for smoke tests."""
    rng = np.random.default_rng(seed)
    take = lambda df, n: df.iloc[np.sort(rng.choice(len(df), min(n, len(df)), replace=False))].reset_index(drop=True)
    lab = data.labelled
    data.labelled = pd.concat([take(lab[lab.label == k], spec["labelled_per_class"]) for k in sorted(lab.label.unique())],
                              ignore_index=True)
    data.unlabelled = take(data.unlabelled, spec["unlabelled"])
    data.val = take(data.val, spec["val"])
    data.test = take(data.test, spec["test"])
    return data


class CollapseMonitor:
    """Stage I collapse monitoring (evaluation code, called once before training and after every epoch).
    Logs the epoch's tuple statistics plus, on projection embeddings z (eval mode, no augmentation):
      val_spread_sq  mean pairwise squared distance over a fixed val subset (collapse -> 0)
      knn_acc        k-NN accuracy on that val subset with the labelled training set as reference
    Val labels are used only to score kNN; nothing feeds back into training."""

    def __init__(self, ctx, n_val=512, k=5):
        self.ctx, self.k = ctx, k
        rng = np.random.default_rng(ctx.seed)
        val = ctx.data.val
        self.val = val.iloc[np.sort(rng.choice(len(val), min(n_val, len(val)), replace=False))].reset_index(drop=True)
        y = ctx.data.eval_labels("val").set_index("patch_id").loc[self.val.patch_id]
        self.y_val = y.majority_label.to_numpy()
        self.nontie = ~y.tie.astype(bool).to_numpy()
        self.y_lab = ctx.data.labelled.label.to_numpy()
        # in-process loading (num_workers=0): ~1k images per call, avoids extra worker processes in low RAM
        self.dl_lab = stages.make_loader(ctx, ctx.data.labelled, train=False, batch_size=128, stream=20, num_workers=0)
        self.dl_val = stages.make_loader(ctx, self.val, train=False, batch_size=128, stream=21, num_workers=0)
        self.rows = []

    @torch.no_grad()
    def _embed(self, model, dl):
        model.eval()
        zs = []
        for b in dl:
            with self.ctx.autocast():
                feats = model.features(b["image"].to(self.ctx.device, non_blocking=True))
            zs.append(model.embed(feats))
        return torch.cat(zs)

    def __call__(self, epoch, model, tuple_stats):
        zl, zv = self._embed(model, self.dl_lab), self._embed(model, self.dl_val)
        dvv = torch.cdist(zv, zv) ** 2
        n = len(zv)
        spread = (dvv.sum() / (n * (n - 1))).item()
        nn_idx = torch.cdist(zv, zl).topk(self.k, largest=False).indices.cpu().numpy()
        votes = self.y_lab[nn_idx]
        pred = (votes.mean(1) > 0.5).astype(int)
        y, m = self.y_val[self.nontie].astype(int), pred[self.nontie]
        from sklearn.metrics import balanced_accuracy_score
        row = {"epoch": epoch, **tuple_stats, "val_spread_sq": spread,
               "val_mean_norm_of_mean": zv.mean(0).norm().item(),
               f"knn{self.k}_acc": float((m == y).mean()), f"knn{self.k}_bal_acc": float(balanced_accuracy_score(y, m))}
        self.rows.append(row)
        pd.DataFrame(self.rows).to_csv(self.ctx.run_dir / "stage1_monitor.csv", index=False)
        print(f"[monitor] epoch {epoch}: spread {spread:.3f} knn{self.k} acc {row[f'knn{self.k}_acc']:.3f} "
              f"bal {row[f'knn{self.k}_bal_acc']:.3f}", flush=True)


STAGE1_DATA_KEYS = ("dataset", "processed_root", "tile_size", "benign_rule", "exclude_readers", "fold", "vote_mode",
                    "vote_seed", "include_ties", "subset", "labelled_pct")


def reuse_stage1(cfg, src, model, run_dir, device):
    """Load the Stage I result of an earlier run instead of retraining it. Stage I never sees Stage II/III settings and
    training is deterministic, so this is only allowed when everything Stage I depends on is identical."""
    import shutil
    import yaml
    src = Path(src)
    sc = yaml.safe_load(open(src / "config.yaml"))
    strip = lambda d: {k: v for k, v in d.items() if k != "reuse_from"}
    checks = {"seed": (sc["seed"], cfg["seed"]), "model": (sc["model"], cfg["model"]), "augment": (sc["augment"], cfg["augment"]),
              "stage1": (strip(sc["stage1"]), strip(cfg["stage1"])),
              **{f"data.{k}": (sc["data"].get(k), cfg["data"].get(k)) for k in STAGE1_DATA_KEYS}}
    bad = {k: v for k, v in checks.items() if v[0] != v[1]}
    if bad:
        raise ValueError(f"stage1.reuse_from={src}: Stage I settings differ: {bad}")
    model.load_state_dict(torch.load(src / "model_stage1.pt", map_location=device))
    if (src / "stage1_monitor.csv").exists():
        shutil.copy(src / "stage1_monitor.csv", run_dir / "stage1_monitor.csv")
    print(f"[stage1] reused from {src} (identical Stage I settings and seed)", flush=True)
    import json
    return json.load(open(src / "metrics.json")).get("stage1", [])


class EpochTestLog:
    """DIAGNOSTIC ONLY (eval.per_epoch_test): val and test metrics after every epoch, written to epoch_eval.csv, to
    measure how much picking the epoch on the test set would inflate a result. Never used for training or selection."""

    def __init__(self, ctx):
        self.ctx, self.rows = ctx, []

    def __call__(self, stage, ep, model):
        row = {"stage": stage, "epoch": ep}
        for split in ("val", "test"):
            preds = stages.predict(self.ctx, model, getattr(self.ctx.data, split))
            ev = evaluate_predictions(preds, self.ctx.data.eval_labels(split))["overall"]
            row.update({f"{split}_{k}": ev[k] for k in ("acc", "bal_acc", "macro_f1", "auroc")})
        self.rows.append(row)
        pd.DataFrame(self.rows).to_csv(self.ctx.run_dir / "epoch_eval.csv", index=False)


def evaluate_stage(ctx, model, tag, metrics, embeddings=False):
    """Predict val/test, save predictions, compute metrics (evaluation only, after the stage has trained)."""
    out = {}
    for split in ctx.cfg["eval"]["splits"]:
        df = getattr(ctx.data, split)
        res = stages.predict(ctx, model, df, embeddings=embeddings and split == "test")
        preds, z = res if isinstance(res, tuple) else (res, None)
        preds.to_csv(ctx.run_dir / f"preds_{tag}_{split}.csv", index=False)
        if z is not None:
            np.save(ctx.run_dir / f"embeddings_{tag}_{split}.npy", z)
        out[split] = evaluate_predictions(preds, ctx.data.eval_labels(split))
    metrics[f"eval_{tag}"] = out
    print(f"[eval {tag}] " + "  ".join(f"{s}: acc {v['overall']['acc']:.3f} bal_acc {v['overall']['bal_acc']:.3f} "
                                       f"auroc {v['overall']['auroc']:.3f}" for s, v in out.items()), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/hsrl_gleason.yaml")
    ap.add_argument("overrides", nargs="*")
    args = ap.parse_args()
    cfg = load_config(args.config, args.overrides)
    device = torch.device(cfg.get("device", "cuda"))
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but not available")
    run_dir = make_run_dir(cfg)
    save_yaml(cfg, run_dir / "config.yaml")
    set_seed(cfg["seed"])

    data = load_dataset(cfg["data"])
    if cfg["data"].get("subset"):
        data = subset_data(data, cfg["data"]["subset"], cfg["seed"])
    model = HSRLNet(n_classes=data.n_classes, **cfg["model"]).to(device)
    metrics = {"run_dir": str(run_dir), "dataset": data.name, "data": data.summary(), "params": param_counts(model),
               "env": {"torch": torch.__version__, "cuda": torch.version.cuda, "timm": timm.__version__,
                       "gpu": torch.cuda.get_device_name() if device.type == "cuda" else None}}
    print(metrics["data"], metrics["params"], flush=True)
    ctx = stages.Ctx(cfg, data, run_dir, device)
    hook = EpochTestLog(ctx) if cfg["eval"].get("per_epoch_test") else None   # diagnostic only
    t_start = time.time()
    try:
        if cfg["method"] == "hsrl":
            if cfg["stage1"].get("enabled", True) and cfg["stage1"].get("reuse_from"):
                metrics["stage1"] = reuse_stage1(cfg, cfg["stage1"]["reuse_from"], model, run_dir, device)
                metrics["stage1_source"] = str(cfg["stage1"]["reuse_from"])
            elif cfg["stage1"].get("enabled", True):
                mon = CollapseMonitor(ctx, **cfg.get("monitor", {})) if cfg.get("monitor") is not None else None
                metrics["stage1"] = stages.stage1(ctx, model, monitor=mon)
                torch.save(model.state_dict(), run_dir / "model_stage1.pt")
            else:
                print("[stage1] skipped (ablation: classifier on ImageNet features)", flush=True)
            metrics["stage2"] = stages.stage2(ctx, model, epoch_hook=hook)
            evaluate_stage(ctx, model, "stage2", metrics)
            metrics["stage3"] = stages.stage3(ctx, model, epoch_hook=hook)
            evaluate_stage(ctx, model, "stage3", metrics, embeddings=cfg["eval"].get("save_embeddings", True))
            # Stage III diagnostics against hidden labels (after training; evaluation only)
            unl_labels = data.eval_labels("unlabelled")
            metrics["pseudo_label_diagnostics"] = {
                p.stem: pseudo_label_diagnostics(pd.read_csv(p), unl_labels, cfg["stage3"]["tau"])
                for p in sorted(run_dir.glob("pseudo_labels_round*.csv"))}
            cov = metrics["pseudo_label_diagnostics"]["pseudo_labels_round0"]["coverage"]
            if cov < 0.05:
                metrics.setdefault("flags", []).append(f"Stage III pseudo-label coverage near zero ({cov:.3f}) at tau "
                                                       f"{cfg['stage3']['tau']}")
                print("WARNING:", metrics["flags"][-1], flush=True)
        elif cfg["method"] == "supervised":
            metrics["supervised"] = stages.supervised(ctx, model, epoch_hook=hook)
            evaluate_stage(ctx, model, "supervised", metrics, embeddings=cfg["eval"].get("save_embeddings", True))
        else:
            raise ValueError(cfg["method"])
    finally:
        ctx.close()
    torch.save(model.state_dict(), run_dir / "model_final.pt")
    metrics["wall_time_sec"] = round(time.time() - t_start, 1)
    if device.type == "cuda":
        metrics["env"]["max_gpu_mem_gb"] = round(torch.cuda.max_memory_allocated() / 1e9, 2)
    save_json(metrics, run_dir / "metrics.json")
    print(f"done: {run_dir}  ({metrics['wall_time_sec']}s)")


if __name__ == "__main__":
    main()
