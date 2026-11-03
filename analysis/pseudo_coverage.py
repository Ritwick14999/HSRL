"""Pseudo-label precision at equal coverage and coverage at equal precision, from the saved Stage III files
(pseudo_labels_round0.csv: confidence of the Stage II model on every unlabelled-pool patch). No retraining.

For a run, sort the pool by p_max (descending; ties broken by patch_id). Accepting the top k gives
  coverage(k)  = k / N_pool                         (pool includes tie patches, as in the Stage III diagnostics)
  precision(k) = correct / non-tie among the top k  (vs hidden majority labels; evaluation only)
Precision at coverage c uses k = round(c * N). Coverage at precision p is the largest k / N with
precision(k) >= p and k >= min_k (precision is noisy for tiny k). The pool is identical across configs within a fold,
so equal-coverage comparisons rank the same patches.

Usage: python -I analysis/pseudo_coverage.py --roots results/main results/deviations results/soft --out results/pseudo_coverage
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml
from scipy import stats

from aggregate_runs import md_table, pm  # noqa: E402
from hsrl.data import load_dataset  # noqa: E402

NAME = re.compile(r"^f(\d+)s(\d+)_(.+)$")
COVERAGES = (0.3, 0.5, 0.7, 0.8)
PRECISIONS = (0.90, 0.93, 0.95)
# reference palette (dataviz skill, light): series slots 1-4 + chrome; colour follows the variant, not the schedule
COL = {"hsrl": "#2a78d6", "hsrl_no_t2": "#eb6834", "hsrl_no_stage1": "#1baf7a", "hsrl_soft": "#eda100",
       "hsrl_s1e60": "#2a78d6", "hsrl_no_t2_s1e60": "#eb6834", "hsrl_soft_s1e60": "#eda100"}
ROWS = [("30-epoch embedding stage", ["hsrl", "hsrl_no_t2", "hsrl_no_stage1", "hsrl_soft"]),
        ("60-epoch embedding stage", ["hsrl_s1e60", "hsrl_no_t2_s1e60", "hsrl_soft_s1e60"])]
NAMES = {"hsrl": "HSRL", "hsrl_no_t2": "Without negatives term", "hsrl_no_stage1": "Without embedding stage",
         "hsrl_soft": "Soft labels", "hsrl_s1e60": "HSRL", "hsrl_no_t2_s1e60": "Without negatives term",
         "hsrl_soft_s1e60": "Soft labels"}
INK, INK2, MUTED, GRID, AXIS, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"


def curve(pl, labels):
    m = pl.merge(labels, on="patch_id", how="left").sort_values(["p_max", "patch_id"], ascending=[False, True])
    nontie = ~m.tie.astype(bool).to_numpy()
    correct = (m.pseudo.to_numpy() == m.majority_label.fillna(-1).astype(int).to_numpy()) & nontie
    split = (~m.unanimous.astype(bool).to_numpy()) & nontie
    n_nt, n_ok, n_split = np.cumsum(nontie), np.cumsum(correct), np.cumsum(split)
    with np.errstate(invalid="ignore", divide="ignore"):
        prec = np.where(n_nt > 0, n_ok / np.maximum(n_nt, 1), np.nan)
        split_share = np.where(n_nt > 0, n_split / np.maximum(n_nt, 1), np.nan)
    cov = np.arange(1, len(m) + 1) / len(m)
    return cov, prec, split_share, m


def summarise_run(pl, labels, min_k):
    cov, prec, split_share, m = curve(pl, labels)
    N = len(cov)
    out = {"pool": N}
    for c in COVERAGES:
        k = max(1, int(round(c * N)))
        out[f"prec@cov{c:.1f}"] = prec[k - 1]
        out[f"split_share@cov{c:.1f}"] = split_share[k - 1]
    for p in PRECISIONS:
        ok = np.flatnonzero((prec >= p) & (np.arange(1, N + 1) >= min_k))
        out[f"cov@prec{p:.2f}"] = cov[ok[-1]] if len(ok) else 0.0
    acc = pl.accepted == 1
    out["tau_coverage"] = acc.mean()
    k = int(acc.sum())
    out["tau_precision"] = prec[k - 1] if k else np.nan
    return out, cov, prec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roots", nargs="+", default=["results/main", "results/deviations", "results/soft"])
    ap.add_argument("--out", default="results/pseudo_coverage")
    ap.add_argument("--min-k", type=int, default=50)
    ap.add_argument("--pairs", nargs="*", default=["hsrl_no_t2:hsrl", "hsrl_no_stage1:hsrl", "hsrl_s1e60:hsrl",
                    "hsrl_no_t2_s1e60:hsrl_s1e60", "hsrl_boundary:hsrl", "hsrl_soft:hsrl", "hsrl_soft_s1e60:hsrl_s1e60"])
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    label_cache, rows, curves = {}, [], {}
    grid = np.linspace(0.05, 1.0, 96)
    for root in args.roots:
        if not Path(root).exists():
            continue
        for d in sorted(Path(root).iterdir()):
            m = NAME.match(d.name)
            if not m or not (d / "pseudo_labels_round0.csv").exists() or not (d / "metrics.json").exists():
                continue
            fold, seed, cfg = int(m[1]), int(m[2]), m[3]
            rc = yaml.safe_load(open(d / "config.yaml"))["data"]
            key = (rc.get("dataset", "gleason"), rc.get("labelled_pct"), fold, rc["tile_size"], rc["benign_rule"],
                   tuple(rc.get("exclude_readers") or []), rc.get("unlabelled_pool", "filtered"))
            if key not in label_cache:   # hidden labels of the unlabelled pool: evaluation only
                label_cache[key] = load_dataset(rc).eval_labels("unlabelled")[["patch_id", "majority_label", "tie", "unanimous"]]
            pl = pd.read_csv(d / "pseudo_labels_round0.csv")
            s, cov, prec = summarise_run(pl, label_cache[key], args.min_k)
            rows.append({"run": d.name, "root": root, "fold": fold, "seed": seed, "cfg": cfg, **s})
            curves[(cfg, fold, seed)] = np.interp(grid, cov, prec)
    R = pd.DataFrame(rows)
    R.to_csv(out / "per_run.csv", index=False)
    metric_cols = [c for c in R.columns if c.startswith(("prec@", "cov@", "split_share@", "tau_"))]

    md = ["# Pseudo-label precision at equal coverage / coverage at equal precision\n",
          f"Runs: {len(R)} (all runs with a saved Stage III pseudo-label file). Pool = vote-filtered unlabelled split of the fold, "
          "identical for every config. Precision vs hidden majority labels (non-tie). Coverage at precision p = largest "
          f"accepted fraction whose precision is still >= p (top-k by confidence, k >= {args.min_k}). split_share = "
          "fraction of split-vote patches among accepted non-tie patches. tau_* = the actual operating point at tau = 0.85.\n"]
    summ = [{"config": c, "runs": len(g), **{k: pm(g[k].astype(float)) for k in metric_cols}} for c, g in R.groupby("cfg", sort=False)]
    md.append("## Mean ± std per config\n\n" + md_table(pd.DataFrame(summ)) + "\n")

    prow = []
    for pair in args.pairs:
        a, b = pair.split(":")
        A = R[R.cfg == a].set_index(["fold", "seed"])
        B = R[R.cfg == b].set_index(["fold", "seed"])
        idx = A.index.intersection(B.index)
        if not len(idx):
            continue
        for k in [c for c in metric_cols if c.startswith(("prec@", "cov@"))] + ["split_share@cov0.5"]:
            d = A.loc[idx, k].astype(float) - B.loc[idx, k].astype(float)
            n = len(d)
            ci = stats.t.ppf(0.975, n - 1) * d.std(ddof=1) / np.sqrt(n) if n > 1 else np.nan
            pf = d.groupby(level="fold").mean()
            prow.append({"comparison": f"{a} − {b}", "metric": k, "n_pairs": n, "mean_diff": d.mean(),
                         "ci95_lo": d.mean() - ci, "ci95_hi": d.mean() + ci, "a_higher": f"{(d > 0).sum()}/{n}",
                         "per_fold_mean": " / ".join(f"f{i}:{v:+.3f}" for i, v in pf.items()),
                         "folds_same_sign": int((np.sign(pf) == np.sign(d.mean())).sum())})
    P = pd.DataFrame(prow)
    P.to_csv(out / "paired_differences.csv", index=False)
    md.append("## Paired differences (same fold and seed)\n\nCI = t-interval over pairs (optimistic: 3 test folds). "
              "Positive = first config higher.\n\n" + md_table(P) + "\n")

    # figure: mean precision-coverage curve per config; rows = schedule, columns = folds
    folds = sorted(R.fold.unique())
    fig, axes = plt.subplots(len(ROWS), len(folds), figsize=(5 * len(folds), 7.6), facecolor=SURFACE, sharex=True, sharey=True)
    for r, (title, cfgs) in enumerate(ROWS):
        for j, f in enumerate(folds):
            ax = axes[r, j]
            for c in cfgs:
                cs = [v for (cc, ff, _), v in curves.items() if cc == c and ff == f]
                if not cs:
                    continue
                ax.plot(grid, np.mean(cs, 0), color=COL[c], linewidth=2, label=NAMES.get(c, c))
                op = R[(R.cfg == c) & (R.fold == f)]
                ax.plot(op.tau_coverage.mean(), op.tau_precision.mean(), "o", color=COL[c], markersize=8,
                        markeredgecolor=SURFACE, markeredgewidth=2)
            ax.set_facecolor(SURFACE)
            ax.set_title(f"Fold {f}, {title}", color=INK, fontsize=9, loc="left")
            ax.grid(True, color=GRID, linewidth=0.6)
            ax.set_axisbelow(True)
            for s in ("top", "right"):
                ax.spines[s].set_visible(False)
            for s in ("left", "bottom"):
                ax.spines[s].set_color(AXIS)
            ax.tick_params(colors=MUTED, labelsize=8)
            ax.set_ylim(0.70, 1.0)
            if r == len(ROWS) - 1:
                ax.set_xlabel("Coverage (fraction of unlabelled pool accepted)", color=INK2, fontsize=8)
            if j == 0:
                ax.set_ylabel("Precision", color=INK2, fontsize=9)
            if j == 0:
                ax.legend(frameon=False, fontsize=8, labelcolor=INK2, loc="lower left")
    fig.tight_layout()
    fig.savefig(out / "precision_coverage.png", dpi=120, facecolor=SURFACE)
    (out / "report.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
