"""EXPLORATORY PILOT: pairwise interval losses on frozen ImageNet EfficientNet-B2 features (supervisor's plan,
'first test: pairwise bounds'). Not part of the HSRL reproduction.

All methods share, within a (fold, seed): the cached features, the labelled patches, one fixed set of tuples
(a, p, n, c) sampled once (p same majority class as a, n and c the other class), the head initialisation and the
mini-batch order. Pair losses train on the four pairs of every tuple (ap, an, nc, ac).

Methods
  probe_hard / probe_soft     linear probe on the features, hard majority / Peterson soft (1-q, q) targets
  hsrl_t13                    head trained with HSRL terms 1 + 3 on the fixed tuples
  annotator_aware             shared hidden layer + one output head per reader on linked votes, prediction =
                              mean of the reader heads (multi-head 'who said what' style)
  interval_<mode>             head trained with IntervalLoss, mode in linked / permuted / counts_only
  worstcase_<mode>            head trained with WorstCaseIntervalLoss, same modes
Head embeddings are evaluated with a linear probe on hard majority targets (primary). A soft-target probe and
test-pair reader-agreement retrieval (Spearman of t vs linked agreement) are reported as secondary measures.

LEAKAGE RULE: votes and labels enter training only for labelled training patches. Test labels and votes are
read through eval_labels for evaluation only.

Usage: python -I hsrl/pilot_frozen.py --config configs/pilot_frozen.yaml [--smoke]
"""
import argparse
import sys
import time
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from scipy import stats

from hsrl.agreement import linked_agreement, pair_bounds
from hsrl.data import ImageDataset, build_transforms, load_dataset
from hsrl.data.votes import apply_vote_mode
from hsrl.evaluate import evaluate_predictions
from hsrl.losses import HSRLLoss, IntervalLoss, WorstCaseIntervalLoss, pair_similarity
from hsrl.models import HSRLNet
from hsrl.utils import load_config, save_yaml

READERS = [f"r{k}" for k in range(1, 7)]
BASELINES = ["probe_hard", "probe_soft", "hsrl_t13", "annotator_aware"]
PAIR_METHODS = [f"{v}_{m}" for v in ("interval", "worstcase") for m in ("linked", "permuted", "counts_only")]


# ------------------------------------------------------------------------------------------- features
def check_backbone_source(run_dir, cfg, fold):
    """LEAKAGE GUARD for fine-tuned features (D42): the backbone must come from a finished supervised run on the same
    dataset, labelled set and draw, so the only labels it has seen are this draw's labelled training images."""
    from hsrl.utils import load_config
    if not (run_dir / "metrics.json").exists():
        raise FileNotFoundError(f"{run_dir}: run not finished (no metrics.json)")
    rc, dc = load_config(run_dir / "config.yaml", []), cfg["data"]
    bad = {k: (a, b) for k, a, b in (("method", rc["method"], "supervised"), ("dataset", rc["data"]["dataset"], dc["dataset"]),
                                     ("fold", rc["data"]["fold"], fold),
                                     ("labelled_pct", str(rc["data"].get("labelled_pct", 10)), str(dc.get("labelled_pct", 10))))
           if a != b}
    if bad:
        raise ValueError(f"backbone {run_dir} does not match this draw (run vs pilot): {bad}")


@torch.no_grad()
def extract_features(cfg, device, fold=None):
    """ImageNet features (one cache for all folds), or with backbone_ckpt: features of a fine-tuned backbone, one
    cache per fold ("{fold}" in features_path and backbone_ckpt)."""
    path = Path(cfg["features_path"].format(fold=fold))
    if path.exists():
        d = np.load(path, allow_pickle=True)
        return pd.Series(range(len(d["patch_id"])), index=d["patch_id"]), d["feats"]
    from hsrl.data.gleason import labels_set_name
    dc = cfg["data"]
    if dc["dataset"] == "mhist":
        table = Path(dc["processed_root"]) / f"labels_p{dc.get('labelled_pct', 10)}" / "patches.csv"
    else:
        table = Path(dc["processed_root"]) / f"p{dc['tile_size']}" / labels_set_name(dc) / "patches.csv"
    patches = pd.read_csv(table, usecols=["patch_id", "path"])
    if cfg.get("backbone_ckpt"):
        ckpt = Path(cfg["backbone_ckpt"].format(fold=fold))
        check_backbone_source(ckpt.parent, cfg, fold)
        model = HSRLNet(pretrained=False)
        model.load_state_dict(torch.load(ckpt, map_location="cpu"))
        model = model.to(device).eval()
    else:
        model = HSRLNet(pretrained=True).to(device).eval()
    ds = ImageDataset(patches, dc.get("image_root") or dc["processed_root"], build_transforms(cfg["augment"], train=False))
    dl = torch.utils.data.DataLoader(ds, batch_size=128, num_workers=4)
    out = []
    for b in dl:
        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=device.type == "cuda"):
            out.append(model.features(b["image"].to(device)).float().cpu())
    feats = torch.cat(out).numpy()
    path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(path, patch_id=patches.patch_id.to_numpy(), feats=feats)
    return pd.Series(range(len(patches)), index=patches.patch_id.to_numpy()), feats


# ------------------------------------------------------------------------------------------- pieces
def sample_tuples(y, k, rng):
    """k tuples per labelled anchor: p same class (!= a), n != c from the other class. Fixed for the run."""
    idx = {c: np.flatnonzero(y == c) for c in (0, 1)}
    rows = []
    for a in range(len(y)):
        same, other = idx[y[a]][idx[y[a]] != a], idx[1 - y[a]]
        for _ in range(k):
            n, c = rng.choice(other, 2, replace=False)
            rows.append((a, rng.choice(same), n, c))
    return np.array(rows)


class Head(nn.Module):
    def __init__(self, d_in, hidden, d_out):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d_in, hidden), nn.ReLU(inplace=True), nn.Linear(hidden, d_out))

    def forward(self, x):
        return F.normalize(self.net(x), dim=1)


def train_probe(X, targets, cfg, seed, device):
    """Linear probe, full batch, soft cross-entropy on (N, 2) targets (one-hot = hard)."""
    torch.manual_seed(seed)
    lin = nn.Linear(X.shape[1], 2).to(device)
    opt = torch.optim.AdamW(lin.parameters(), lr=cfg["lr"], weight_decay=cfg["weight_decay"])
    T = torch.as_tensor(targets, dtype=torch.float32, device=device)
    for _ in range(cfg["steps"]):
        loss = -(T * F.log_softmax(lin(X), 1)).sum(1).mean()
        opt.zero_grad()
        loss.backward()
        opt.step()
    return lin


def train_head(X, tuples, loss_name, bounds, cfg, seed, order_seed, device):
    torch.manual_seed(seed)
    head = Head(X.shape[1], cfg["hidden"], cfg["dim"]).to(device)
    opt = torch.optim.AdamW(head.parameters(), lr=cfg["lr"], weight_decay=cfg["weight_decay"])
    T = torch.as_tensor(tuples, device=device)
    if loss_name == "hsrl_t13":
        loss_fn = HSRLLoss(cfg["alpha"], 0.0, cfg["gamma"], terms=(1, 3))
    else:
        loss_fn = IntervalLoss() if loss_name == "interval" else WorstCaseIntervalLoss()
        Lb = torch.as_tensor(bounds[0], dtype=torch.float32, device=device)   # (M, 4)
        Ub = torch.as_tensor(bounds[1], dtype=torch.float32, device=device)
    g = torch.Generator().manual_seed(order_seed)
    hist = []
    for ep in range(cfg["epochs"]):
        perm = torch.randperm(len(T), generator=g).to(device)
        tot = 0.0
        for s in range(0, len(T), cfg["batch_tuples"]):
            bi = perm[s:s + cfg["batch_tuples"]]
            tb = T[bi]
            z = head(X)
            if loss_name == "hsrl_t13":
                loss, _ = loss_fn(z, {"a": tb[:, 0], "p": tb[:, 1], "n": tb[:, 2], "c": tb[:, 3]})
            else:
                pi = torch.cat([tb[:, 0], tb[:, 0], tb[:, 2], tb[:, 0]])        # ap, an, nc, ac
                pj = torch.cat([tb[:, 1], tb[:, 2], tb[:, 3], tb[:, 3]])
                L = torch.cat([Lb[bi, 0], Lb[bi, 1], Lb[bi, 2], Lb[bi, 3]])
                U = torch.cat([Ub[bi, 0], Ub[bi, 1], Ub[bi, 2], Ub[bi, 3]])
                loss, _ = loss_fn(z, {"i": pi, "j": pj}, {"L": L, "U": U})
            opt.zero_grad()
            loss.backward()
            opt.step()
            tot += loss.item() * len(bi)
        hist.append(tot / len(T))
    return head, hist


def train_annotator_aware(X, V, cfg, seed, device):
    torch.manual_seed(seed)
    R = V.shape[1]
    shared = nn.Sequential(nn.Linear(X.shape[1], cfg["hidden"]), nn.ReLU(inplace=True)).to(device)
    heads = nn.Linear(cfg["hidden"], 2 * R).to(device)
    opt = torch.optim.AdamW(list(shared.parameters()) + list(heads.parameters()), lr=cfg["lr"],
                            weight_decay=cfg["weight_decay"])
    Vt = torch.as_tensor(V, device=device)
    mask = Vt >= 0
    for _ in range(cfg["steps"]):
        logits = heads(shared(X)).view(len(X), R, 2)
        loss = F.cross_entropy(logits[mask], Vt[mask])
        opt.zero_grad()
        loss.backward()
        opt.step()
    return lambda Xq: F.softmax(heads(shared(Xq)).view(len(Xq), R, 2), -1).mean(1)


def retrieval_spearman(z_test, V_test, rng, n_pairs, min_shared):
    """Spearman between embedding similarity t and linked agreement on random test pairs (evaluation only)."""
    i = rng.integers(0, len(V_test), n_pairs * 3)
    j = rng.integers(0, len(V_test), n_pairs * 3)
    keep = i != j
    s, n = linked_agreement(V_test, i[keep], j[keep])
    ok = n >= min_shared
    ii, jj, ss = i[keep][ok][:n_pairs], j[keep][ok][:n_pairs], s[ok][:n_pairs]
    t = pair_similarity(z_test[ii], z_test[jj]).cpu().numpy()
    return float(stats.spearmanr(t, ss).statistic)


# ------------------------------------------------------------------------------------------- one (fold, seed)
def run_fold_seed(cfg, fold, seed, index, feats, device):
    dc = dict(cfg["data"], fold=fold)
    data = load_dataset(dc)
    lab = data.labelled
    y = lab.label.to_numpy()
    q = lab.q.to_numpy(float)
    V_link = lab[READERS].fillna(-1).astype(int).to_numpy()
    needs_ids = any(m.endswith(("linked", "permuted", "linked_renamed")) or "_permuted_p" in m or m == "annotator_aware"
                    for m in cfg["methods"])
    V_perm = (apply_vote_mode(lab, READERS, "permuted", seed=1000 * fold + seed)[READERS].fillna(-1).astype(int).to_numpy()
              if needs_ids else V_link)
    test_lab = data.eval_labels("test")                                      # evaluation only
    test_ids = test_lab.patch_id.to_numpy()
    V_test = test_lab[READERS].fillna(-1).astype(int).to_numpy()

    Xl_np = feats[index[lab.patch_id].to_numpy()]
    mu, sd = Xl_np.mean(0), Xl_np.std(0) + 1e-6                               # labelled-train statistics only
    to_t = lambda a: torch.as_tensor((a - mu) / sd, dtype=torch.float32, device=device)
    Xl, Xt = to_t(Xl_np), to_t(feats[index[test_ids].to_numpy()])
    hard = np.eye(2)[y]
    soft = np.stack([1 - q, q], 1)

    rng = np.random.default_rng([cfg["seed_base"], fold, seed])
    tuples = sample_tuples(y, cfg["head"]["tuples_per_anchor"], rng)
    pairs = [(tuples[:, 0], tuples[:, 1]), (tuples[:, 0], tuples[:, 2]), (tuples[:, 2], tuples[:, 3]), (tuples[:, 0], tuples[:, 3])]
    # vote sources per mode key. permuted draw k uses seed 1000*fold + seed + 100000*k (k = 0 is the main pilot's draw);
    # linked_renamed = one consistent relabelling of reader ids for the whole dataset (must not change anything)
    sources = {"linked": ("linked", V_link), "counts_only": ("counts_only", V_link),
               "linked_renamed": ("linked", V_link[:, np.random.default_rng(99).permutation(V_link.shape[1])])}
    for k in cfg.get("permutation_draws", [0]) if needs_ids else []:
        Vp = V_perm if k == 0 else apply_vote_mode(lab, READERS, "permuted", seed=1000 * fold + seed + 100000 * k)[
            READERS].fillna(-1).astype(int).to_numpy()
        sources["permuted" if len(cfg.get("permutation_draws", [0])) == 1 else f"permuted_p{k}"] = ("permuted", Vp)
    needed = {m.split("_", 1)[1] for m in cfg["methods"] if m.split("_", 1)[0] in ("interval", "worstcase")}
    bounds, exact_frac = {}, {}
    for key in needed:
        mode, V = sources[key]
        Ls, Us, ex = zip(*(pair_bounds(V, q, i, j, mode, cfg["min_shared"]) for i, j in pairs))
        bounds[key] = (np.stack(Ls, 1), np.stack(Us, 1))
        exact_frac[key] = float(np.mean(ex))

    init_seed, order_seed = 100 * seed + fold, 10_000 + 100 * seed + fold
    rows, preds_all = [], []

    def evaluate(method, prob1, z_test=None, extra=None):
        preds = pd.DataFrame({"patch_id": test_ids, "prob_1": prob1})
        ev = evaluate_predictions(preds, test_lab)
        r = {"fold": fold, "seed": seed, "method": method, "n_labelled": len(lab), "n_tuples": len(tuples)}
        for sub in ("overall", "unanimous", "split_vote"):
            for k in ("acc", "bal_acc", "brier", "auroc"):
                r[f"{sub}_{k}"] = ev[sub][k]
        if z_test is not None and (V_test >= 0).any():
            r["retrieval_spearman"] = retrieval_spearman(z_test, V_test, np.random.default_rng([fold, 7]),
                                                         cfg["retrieval_pairs"], cfg["min_shared"])
        r.update(extra or {})
        rows.append(r)
        preds_all.append(preds.assign(fold=fold, seed=seed, method=method))

    pc = cfg["probe"]
    for name, tgt in (("probe_hard", hard), ("probe_soft", soft)):
        if name in cfg["methods"]:
            lin = train_probe(Xl, tgt, pc, init_seed, device)
            with torch.no_grad():
                evaluate(name, F.softmax(lin(Xt), 1)[:, 1].cpu().numpy())
    if "annotator_aware" in cfg["methods"]:
        predict = train_annotator_aware(Xl, V_link, cfg["annotator"], init_seed, device)
        with torch.no_grad():
            evaluate("annotator_aware", predict(Xt)[:, 1].cpu().numpy())
    for method in [m for m in cfg["methods"] if m == "hsrl_t13" or m.split("_", 1)[0] in ("interval", "worstcase")]:
        if method == "hsrl_t13":
            loss_name, b, extra = "hsrl_t13", None, {}
        else:
            variant, mode = method.split("_", 1)
            loss_name, b, extra = variant, bounds[mode], {"exact_pair_frac": exact_frac[mode]}
        head, hist = train_head(Xl, tuples, loss_name, b, cfg["head"], init_seed, order_seed, device)
        with torch.no_grad():
            zl, zt = head(Xl), head(Xt)
        lin = train_probe(zl, hard, pc, init_seed, device)
        lin_s = train_probe(zl, soft, pc, init_seed, device)
        with torch.no_grad():
            p_soft = F.softmax(lin_s(zt), 1)[:, 1].cpu().numpy()
            ev_s = evaluate_predictions(pd.DataFrame({"patch_id": test_ids, "prob_1": p_soft}), test_lab)
            extra.update({"loss_first": hist[0], "loss_last": hist[-1], "softprobe_bal_acc": ev_s["overall"]["bal_acc"],
                          "softprobe_brier": ev_s["overall"]["brier"],
                          "softprobe_split_acc": ev_s["split_vote"]["acc"]})
            evaluate(method, F.softmax(lin(zt), 1)[:, 1].cpu().numpy(), z_test=zt, extra=extra)
    return rows, pd.concat(preds_all)


# ------------------------------------------------------------------------------------------- report
def paired(R, a, b, metric):
    A = R[R.method == a].set_index(["fold", "seed"])[metric]
    B = R[R.method == b].set_index(["fold", "seed"])[metric]
    d = (A - B).dropna()
    sign = -1 if "brier" in metric else 1                                        # lower Brier is better
    n = len(d)
    ci = stats.t.ppf(0.975, n - 1) * d.std(ddof=1) / np.sqrt(n) if n > 1 else np.nan
    pf = d.groupby(level="fold").mean()
    return {"mean_diff": d.mean(), "ci_lo": d.mean() - ci, "ci_hi": d.mean() + ci,
            "pairs_ge_1pt": int((sign * d >= 0.01).sum()), "pairs_better": int((sign * d > 0).sum()), "n_pairs": n,
            "folds_ge_1pt": int((sign * pf >= 0.01).sum()),
            "per_fold": " / ".join(f"f{k}:{v:+.3f}" for k, v in pf.items())}


CRITERION = {"pairs": 12, "folds": 2}   # Gleason pilot; the MHIST pilot sets its own in the config (pre-registered)


def meets(p):
    """Pre-registered criterion: >= +1 point in >= CRITERION['pairs'] pairs and on >= CRITERION['folds'] folds."""
    return p["pairs_ge_1pt"] >= CRITERION["pairs"] and p["folds_ge_1pt"] >= CRITERION["folds"]


def write_report(R, out, cfg):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
    from aggregate_runs import md_table, pm
    metrics = {"overall_bal_acc": "bal acc", "split_vote_acc": "split-vote acc", "unanimous_acc": "unanimous acc",
               "overall_brier": "Brier"}
    md = [f"# EXPLORATORY PILOT: interval losses on {cfg.get('features_name', 'frozen ImageNet features')}\n",
          f"{R.groupby(['fold', 'seed']).ngroups} (fold, seed) pairs. Test = held-out slides (Gleason) or the official test "
          "set (MHIST), non-tie patches. Head methods are evaluated with a hard-target linear probe on the head embedding. "
          "Criterion fixed in advance: >= +1 point on balanced or split-vote accuracy over the best baseline in >= "
          f"{CRITERION['pairs']}/{R.groupby(['fold', 'seed']).ngroups} pairs and on >= {CRITERION['folds']}/"
          f"{R.fold.nunique()} folds (MHIST: labelled draws).\n"]
    rows = [{"method": m, "runs": len(g), **{lab: pm(g[k]) for k, lab in metrics.items()},
             **({"retrieval ρ": pm(g.retrieval_spearman)} if "retrieval_spearman" in g and g.retrieval_spearman.notna().any()
                else {})}
            for m, g in R.groupby("method", sort=False)]
    md.append("## Mean ± std per method\n\n" + md_table(pd.DataFrame(rows)) + "\n")
    present = [m for m in BASELINES if m in set(R.method)]
    best = {k: max(present, key=lambda m: R[R.method == m][k].mean()) for k in ("overall_bal_acc", "split_vote_acc")}
    md.append(f"Best baseline: balanced accuracy = `{best['overall_bal_acc']}`, split-vote accuracy = `{best['split_vote_acc']}`.\n")
    crit, prow = [], []
    for m in PAIR_METHODS:
        if m not in set(R.method):
            continue
        ok = {}
        for k in ("overall_bal_acc", "split_vote_acc"):
            p = paired(R, m, best[k], k)
            ok[k] = meets(p)
            prow.append({"method": m, "vs": best[k], "metric": metrics[k], **{kk: (round(v, 4) if isinstance(v, float) else v)
                                                                            for kk, v in p.items()}})
        for k in ("unanimous_acc", "overall_brier"):
            b = best["overall_bal_acc"]
            p = paired(R, m, b, k)
            prow.append({"method": m, "vs": b, "metric": metrics[k], **{kk: (round(v, 4) if isinstance(v, float) else v)
                                                                       for kk, v in p.items()}})
        crit.append({"method": m, "bal acc criterion": ok["overall_bal_acc"], "split acc criterion": ok["split_vote_acc"],
                     "SUCCESS": ok["overall_bal_acc"] or ok["split_vote_acc"]})
    md.append("## Paired differences vs the best baseline\n\n" + md_table(pd.DataFrame(prow)) + "\n")
    md.append("## Pre-registered success criterion\n\n" + md_table(pd.DataFrame(crit)) + "\n")
    link = []
    for v in ("interval", "worstcase"):
        a, b = f"{v}_linked", f"{v}_permuted"
        if {a, b} <= set(R.method):
            res = {k: paired(R, a, b, k) for k in ("overall_bal_acc", "split_vote_acc")}
            link.append({"variant": v, **{f"{metrics[k]}: Δ": round(p["mean_diff"], 4) for k, p in res.items()},
                         **{f"{metrics[k]}: pairs ≥ +1pt": p["pairs_ge_1pt"] for k, p in res.items()},
                         **{f"{metrics[k]}: folds ≥ +1pt": p["folds_ge_1pt"] for k, p in res.items()},
                         "LINKAGE MATTERS": any(meets(p) for p in res.values())})
    md.append("## Linkage test: linked − permuted (same standard)\n\n" + (md_table(pd.DataFrame(link)) if link else "-") + "\n")
    (out / "report.md").write_text("\n".join(md), encoding="utf-8")
    return "\n".join(md)


def write_robustness_report(R, out):
    """Secondary checks: (1) consistent reader renaming must leave linked results unchanged; (2) linked vs each of
    several permutation draws and vs their mean, by the pre-registered standard."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "analysis"))
    from aggregate_runs import md_table
    md = ["# EXPLORATORY PILOT, robustness checks (secondary to the pre-registered result)\n"]
    ren = []
    for v in ("interval", "worstcase"):
        a, b = R[R.method == f"{v}_linked"], R[R.method == f"{v}_linked_renamed"]
        if len(a) and len(b):
            m = a.merge(b, on=["fold", "seed"], suffixes=("", "_r"))
            ren.append({"variant": v, "pairs": len(m),
                        "max |Δ bal acc|": float((m.overall_bal_acc - m.overall_bal_acc_r).abs().max()),
                        "max |Δ Brier|": float((m.overall_brier - m.overall_brier_r).abs().max())})
    md.append("## Consistent reader renaming (should be 0)\n\n" + (md_table(pd.DataFrame(ren)) if ren else "-") + "\n")
    rows = []
    for v in ("interval", "worstcase"):
        draws = sorted(m for m in R.method.unique() if m.startswith(f"{v}_permuted_p"))
        if not draws or f"{v}_linked" not in set(R.method):
            continue
        mean_perm = (R[R.method.isin(draws)].groupby(["fold", "seed"])[["overall_bal_acc", "split_vote_acc"]].mean()
                     .reset_index().assign(method=f"{v}_permuted_mean"))
        RR = pd.concat([R, mean_perm], ignore_index=True)
        for d in draws + [f"{v}_permuted_mean"]:
            for k, lab in (("overall_bal_acc", "bal acc"), ("split_vote_acc", "split-vote acc")):
                p = paired(RR, f"{v}_linked", d, k)
                rows.append({"variant": v, "vs": d, "metric": lab, "Δ linked − permuted": round(p["mean_diff"], 4),
                             "pairs ≥ +1pt": p["pairs_ge_1pt"], "folds ≥ +1pt": p["folds_ge_1pt"], "meets standard": meets(p)})
    md.append("## Linked vs repeated permutation draws\n\n" + (md_table(pd.DataFrame(rows)) if rows else "-") + "\n")
    (out / "report.md").write_text("\n".join(md), encoding="utf-8")
    return "\n".join(md)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/pilot_frozen.yaml")
    ap.add_argument("--smoke", action="store_true", help="fold 0, seed 0 only")
    ap.add_argument("overrides", nargs="*")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    cfg = load_config(args.config, args.overrides)
    CRITERION.update(cfg.get("criterion", {}))
    out = Path(cfg["results_dir"] + ("_smoke" if args.smoke else ""))
    out.mkdir(parents=True, exist_ok=True)
    save_yaml(cfg, out / "config.yaml")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    t0 = time.time()
    per_fold = "{fold}" in cfg["features_path"]          # fine-tuned backbone: one feature cache per fold
    if not per_fold:
        index, feats = extract_features(cfg, device)
        print(f"features {feats.shape} ({time.time() - t0:.0f}s)", flush=True)
    folds, seeds = ([0], [0]) if args.smoke else (cfg["folds"], cfg["seeds"])
    rows, preds = [], []
    for fold in folds:
        if per_fold:
            index, feats = extract_features(cfg, device, fold)
            print(f"fold {fold} features {feats.shape} ({time.time() - t0:.0f}s)", flush=True)
        for seed in seeds:
            t1 = time.time()
            r, p = run_fold_seed(cfg, fold, seed, index, feats, device)
            rows += r
            preds.append(p)
            print(f"fold {fold} seed {seed}: {len(r)} methods ({time.time() - t1:.0f}s)", flush=True)
            pd.DataFrame(rows).to_csv(out / "per_run.csv", index=False)
    pd.concat(preds).to_csv(out / "test_predictions.csv", index=False)
    report = write_robustness_report if cfg.get("report") == "robustness" else write_report
    print(report(pd.DataFrame(rows), out) if report is write_robustness_report else report(pd.DataFrame(rows), out, cfg))
    print(f"done in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
