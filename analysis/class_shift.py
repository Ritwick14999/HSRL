"""Soft- vs hard-target class shift, paired within one label-set setting.

For each pair (soft config, hard config, stage) and every (fold, seed) present in both, computes on test non-tie patches:
predicted G4/5 rate, G3 recall, G4/5 recall, balanced accuracy, Brier (vs majority label), accuracy on split-vote and
unanimous patches; then paired differences soft − hard. Run once per setting (e.g. with / without Map1). Settings use
different label sets, so only the WITHIN-setting differences should be compared across settings, never raw values.

Also summarises each setting's label set: kept patches, labelled patches per fold, and the minority votes carried by the
labelled G3- and G4/5-majority patches (what soft targets encode).

Usage: python -I analysis/class_shift.py --setting "with Map1" results/main results/soft \
                                         --setting "Map1 excluded" results/excl_r1 results/excl_r1 --out results/excl_r1_summary
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
import yaml
from scipy import stats

from aggregate_runs import md_table, pm  # noqa: E402
from hsrl.data import load_dataset  # noqa: E402
from hsrl.data.gleason import labels_set_name  # noqa: E402

PAIRS = [("supervised_soft", "supervised", "supervised", "Supervised (35 ep), final"),
         ("hsrl_soft", "hsrl", "stage2", "HSRL (Stage I 30 ep), after Stage II"),
         ("hsrl_soft", "hsrl", "stage3", "HSRL (Stage I 30 ep), final (after Stage III)")]
METRICS = ["pred_g4_rate", "recall_g3", "recall_g4", "bal_acc", "brier", "acc_split", "acc_unanimous"]


def run_metrics(run_dir, stage, cache):
    cfg = yaml.safe_load(open(run_dir / "config.yaml"))["data"]
    key = (labels_set_name(cfg), cfg["fold"])
    if key not in cache:   # hidden test labels: evaluation only
        cache[key] = load_dataset(cfg).eval_labels("test")[["patch_id", "majority_label", "tie", "unanimous"]]
    x = pd.read_csv(run_dir / f"preds_{stage}_test.csv").merge(cache[key], on="patch_id")
    x = x[~x.tie.astype(bool)]
    y = x.majority_label.astype(int).to_numpy()
    p = x.prob_1.to_numpy()
    pr = (p > 0.5).astype(int)
    sp = ~x.unanimous.astype(bool).to_numpy()
    r3, r4 = ((pr == 0) & (y == 0)).sum() / (y == 0).sum(), ((pr == 1) & (y == 1)).sum() / (y == 1).sum()
    return {"pred_g4_rate": pr.mean(), "recall_g3": r3, "recall_g4": r4, "bal_acc": (r3 + r4) / 2,
            "brier": float(np.mean((p - y) ** 2)), "acc_split": (pr[sp] == y[sp]).mean(), "acc_unanimous": (pr[~sp] == y[~sp]).mean(),
            "n_test": len(y)}


def label_set_summary(processed_root, data_cfg):
    d = Path(processed_root) / f"p{data_cfg['tile_size']}" / labels_set_name(data_cfg)
    rows = []
    for f in range(3):
        fd = d / "folds" / f"fold{f}"
        L = pd.read_csv(fd / "labelled_list.csv")
        L = L[L.train_majority == 1]
        g3, g4 = L[L.majority_label == 0], L[L.majority_label == 1]
        split = pd.read_csv(fd / "split.csv")
        rows.append({"fold": f, "kept patches": len(split), "labelled (used)": len(L),
                     "unlabelled pool": int(((split.split == "train") & (split.labelled == 0)).sum()),
                     "val": int((split.split == "val").sum()), "test": int((split.split == "test").sum()),
                     "labelled G3: mean q": round(g3.q.mean(), 3), "labelled G3: share with any G4/5 vote": round((g3.q > 0).mean(), 2),
                     "labelled G4/5: mean 1−q": round((1 - g4.q).mean(), 3),
                     "labelled G4/5: share with any G3 vote": round((g4.q < 1).mean(), 2),
                     "mean readers per labelled patch": round(L.n_readers.mean(), 2)})
    return pd.DataFrame(rows).astype(str)   # avoid float formatting of counts in md_table


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--setting", nargs=3, action="append", metavar=("NAME", "HARD_ROOT", "SOFT_ROOT"), required=True)
    ap.add_argument("--out", default="results/excl_r1_summary")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    cache, per_run, diffs = {}, [], []
    md = ["# Soft vs hard targets: class shift within each label-set setting\n",
          "Test non-tie patches. Paired differences soft − hard on the same (fold, seed); CI = t-interval over pairs "
          "(optimistic, 3 test-slide sets). Compare differences across settings, never raw values (different label sets).\n"]
    for name, hard_root, soft_root in args.setting:
        hard_root, soft_root = Path(hard_root), Path(soft_root)
        for soft_cfg, hard_cfg, stage, title in PAIRS:
            for f in range(3):
                for s in range(5):
                    rh, rs = hard_root / f"f{f}s{s}_{hard_cfg}", soft_root / f"f{f}s{s}_{soft_cfg}"
                    if not ((rh / "metrics.json").exists() and (rs / "metrics.json").exists()):
                        continue
                    mh, ms = run_metrics(rh, stage, cache), run_metrics(rs, stage, cache)
                    for tgt, m in (("hard", mh), ("soft", ms)):
                        per_run.append({"setting": name, "comparison": title, "target": tgt, "fold": f, "seed": s, **m})
        R = pd.DataFrame([r for r in per_run if r["setting"] == name])
        if R.empty:
            continue
        any_run = next(p for p in sorted(hard_root.glob("f0s0_*")) if (p / "config.yaml").exists())
        dcfg = yaml.safe_load(open(any_run / "config.yaml"))["data"]
        md.append(f"## Setting: {name} (label set `{labels_set_name(dcfg)}`)\n\n" +
                  md_table(label_set_summary(dcfg["processed_root"], dcfg)) + "\n")
        for title, g in R.groupby("comparison", sort=False):
            rows = []
            for tgt in ("hard", "soft"):
                gg = g[g.target == tgt]
                rows.append({"target": tgt, "runs": len(gg), **{m: pm(gg[m]) for m in METRICS}})
            H = g[g.target == "hard"].set_index(["fold", "seed"])
            S = g[g.target == "soft"].set_index(["fold", "seed"])
            drow = {"target": "Δ soft − hard", "runs": len(H)}
            for m in METRICS:
                d = (S[m] - H[m]).dropna()
                n = len(d)
                ci = stats.t.ppf(0.975, n - 1) * d.std(ddof=1) / np.sqrt(n) if n > 1 else np.nan
                pf = d.groupby(level="fold").mean()
                drow[m] = f"{d.mean():+.3f} [{d.mean() - ci:+.3f}, {d.mean() + ci:+.3f}]"
                diffs.append({"setting": name, "comparison": title, "metric": m, "n_pairs": n, "mean_diff": d.mean(),
                              "ci95_lo": d.mean() - ci, "ci95_hi": d.mean() + ci, "soft_higher": f"{(d > 0).sum()}/{n}",
                              "per_fold_mean": " / ".join(f"f{i}:{v:+.3f}" for i, v in pf.items()),
                              "folds_same_sign": int((np.sign(pf) == np.sign(d.mean())).sum())})
            rows.append(drow)
            md.append(f"### {title}\n\n" + md_table(pd.DataFrame(rows)) + "\n")
    pd.DataFrame(per_run).to_csv(out / "class_shift_per_run.csv", index=False)
    D = pd.DataFrame(diffs)
    D.to_csv(out / "class_shift_paired.csv", index=False)
    # side-by-side shift (within-setting differences only)
    side = D.pivot_table(index=["comparison", "metric"], columns="setting", values="mean_diff", sort=False).reset_index()
    md.append("## Side by side: soft − hard shift in each setting (within-setting paired differences)\n\n" +
              md_table(side) + "\n\nFull rows with CIs, per-fold means and sign counts: `class_shift_paired.csv`.\n")
    (out / "class_shift.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
