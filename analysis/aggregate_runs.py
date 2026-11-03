"""Aggregate runs named f{fold}s{seed}_{config}: mean +/- std, paired differences, before/after Stage III,
pseudo-label diagnostics and Stage I collapse/escape epochs. Writes <out>/report.md and CSVs.

Collapse/escape (Stage I monitor, val embedding spread s; s0 = spread before training):
  collapse epoch = first epoch with s < 0.1 * s0;  escape epoch = first later epoch with s > 0.5 * s0.

Usage: python -I analysis/aggregate_runs.py --roots results/main --out results/main_summary --pairs hsrl:supervised ...
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

NAME = re.compile(r"^f(\d+)s(\d+)_(.+)$")
METRICS = ["acc", "bal_acc", "macro_f1", "auroc", "brier"]


def md_table(df, floatfmt=3):
    df = df.copy()
    cols = list(df.columns)
    fmt = lambda v: (f"{v:.{floatfmt}f}" if isinstance(v, (float, np.floating)) and not np.isnan(v) else str(v))
    lines = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    lines += ["| " + " | ".join(fmt(r[c]) for c in cols) + " |" for _, r in df.iterrows()]
    return "\n".join(lines)


def pm(x):
    x = np.asarray(x, float)
    return f"{x.mean():.3f} ± {x.std(ddof=1):.3f}" if len(x) > 1 else f"{x.mean():.3f}"


def collapse_stats(mon):
    s0 = mon.loc[mon.epoch == -1, "val_spread_sq"].iloc[0]
    tr = mon[mon.epoch >= 0].reset_index(drop=True)
    col = tr[tr.val_spread_sq < 0.1 * s0]
    collapse = int(col.epoch.iloc[0]) if len(col) else None
    escape = None
    if collapse is not None:
        esc = tr[(tr.epoch > collapse) & (tr.val_spread_sq > 0.5 * s0)]
        escape = int(esc.epoch.iloc[0]) if len(esc) else None
    last = tr.iloc[-1]
    return {"spread_init": s0, "spread_min": tr.val_spread_sq.min(), "epoch_min": int(tr.epoch[tr.val_spread_sq.idxmin()]),
            "collapse_epoch": collapse, "escape_epoch": escape, "spread_final": last.val_spread_sq,
            "knn5_bal_acc_final": last.knn5_bal_acc, "t1_active_final": last.frac_t1_active,
            "t2_active_final": last.frac_t2_active, "t3_active_final": last.frac_t3_active, "n_epochs": int(tr.epoch.max()) + 1}


def load_runs(roots, folds, seeds, cfgs=()):
    rows, diag, coll = [], [], []
    for root in roots:
        for d in sorted(Path(root).iterdir()):
            m = NAME.match(d.name)
            if not m or not (d / "metrics.json").exists():
                continue
            fold, seed, cfg = int(m[1]), int(m[2]), m[3]
            if (folds and fold not in folds) or (seeds and seed not in seeds) or (cfgs and cfg not in cfgs):
                continue
            mt = json.load(open(d / "metrics.json"))
            final_tag = "supervised" if "eval_supervised" in mt else "stage3"
            for tag in ("supervised", "stage2", "stage3"):
                ev = mt.get(f"eval_{tag}")
                if not ev:
                    continue
                for subset, mm in ev["test"].items():
                    rows.append({"run": d.name, "root": root, "fold": fold, "seed": seed, "cfg": cfg,
                                 "stage": "final" if tag == final_tag else "before_stage3", "subset": subset, **mm})
            for rnd, dg in (mt.get("pseudo_label_diagnostics") or {}).items():
                diag.append({"run": d.name, "fold": fold, "seed": seed, "cfg": cfg, "coverage": dg["coverage"],
                             "precision": dg["overall"]["precision"], "prec_unanimous": dg["unanimous"]["precision"],
                             "prec_split": dg["split_vote"]["precision"], "accepted": dg["accepted"]})
            if (d / "stage1_monitor.csv").exists():
                coll.append({"run": d.name, "fold": fold, "seed": seed, "cfg": cfg,
                             **collapse_stats(pd.read_csv(d / "stage1_monitor.csv"))})
    return pd.DataFrame(rows), pd.DataFrame(diag), pd.DataFrame(coll)


def paired(t, a, b, stage_a="final", stage_b="final"):
    """Paired differences a - b on matching (fold, seed), per subset and metric."""
    out = []
    for subset in ("overall", "unanimous", "split_vote"):
        A = t[(t.cfg == a) & (t.stage == stage_a) & (t.subset == subset)].set_index(["fold", "seed"])
        B = t[(t.cfg == b) & (t.stage == stage_b) & (t.subset == subset)].set_index(["fold", "seed"])
        idx = A.index.intersection(B.index)
        if not len(idx):
            continue
        for met in METRICS:
            d = (A.loc[idx, met] - B.loc[idx, met])
            n = len(d)
            ci = stats.t.ppf(0.975, n - 1) * d.std(ddof=1) / np.sqrt(n) if n > 1 else np.nan
            per_fold = d.groupby(level="fold").mean()
            better = (d < 0).sum() if met == "brier" else (d > 0).sum()
            out.append({"comparison": f"{a} − {b}" if stage_a == stage_b else f"{a}[{stage_a}] − {b}[{stage_b}]",
                        "subset": subset, "metric": met, "n_pairs": n, "mean_diff": d.mean(), "std": d.std(ddof=1),
                        "ci95_lo": d.mean() - ci, "ci95_hi": d.mean() + ci, "a_better": f"{better}/{n}",
                        "per_fold_mean": " / ".join(f"f{k}:{v:+.3f}" for k, v in per_fold.items()),
                        "folds_same_sign": int((np.sign(per_fold) == np.sign(d.mean())).sum())})
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roots", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--folds", nargs="*", type=int, default=[])
    ap.add_argument("--seeds", nargs="*", type=int, default=[])
    ap.add_argument("--pairs", nargs="*", default=[])
    ap.add_argument("--cfgs", nargs="*", default=[], help="only these configs (default: all)")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    t, diag, coll = load_runs(args.roots, args.folds, args.seeds, args.cfgs)
    t.to_csv(out / "all_test_metrics.csv", index=False)
    md = [f"# Aggregate over {', '.join(args.roots)}\n",
          f"Runs: {t.run.nunique()}; folds {sorted(map(int, t.fold.unique()))}; seeds {sorted(map(int, t.seed.unique()))}. "
          "Test = held-out slides "
          "of each fold, non-tie patches. mean ± std over all (fold, seed) runs. 'final' = after Stage III "
          "(HSRL variants) or end of training (supervised); 'before_stage3' = after Stage II.\n"]

    # 1. mean +/- std of final metrics
    rows = []
    for cfg, g in t[t.stage == "final"].groupby("cfg", sort=False):
        r = {"config": cfg, "runs": g.run.nunique()}
        for met in METRICS:
            r[met] = pm(g[g.subset == "overall"][met])
        r["acc_unanimous"] = pm(g[g.subset == "unanimous"].acc)
        r["acc_split"] = pm(g[g.subset == "split_vote"].acc)
        rows.append(r)
    md.append("## 1. Final test metrics (mean ± std over runs)\n\n" + md_table(pd.DataFrame(rows)) + "\n")
    rows = []
    for (cfg, fold), g in t[(t.stage == "final") & (t.subset == "overall")].groupby(["cfg", "fold"], sort=False):
        gs = t[(t.stage == "final") & (t.subset == "split_vote") & (t.cfg == cfg) & (t.fold == fold)]
        rows.append({"config": cfg, "fold": fold, "seeds": len(g), "acc": pm(g.acc), "bal_acc": pm(g.bal_acc),
                     "auroc": pm(g.auroc), "acc_split": pm(gs.acc)})
    md.append("### Per fold (mean ± std over seeds)\n\n" + md_table(pd.DataFrame(rows)) + "\n")

    # 2. paired differences
    if args.pairs:
        P = pd.concat([paired(t, *p.split(":")) for p in args.pairs], ignore_index=True)
        P.to_csv(out / "paired_differences.csv", index=False)
        show = P[P.metric.isin(["acc", "bal_acc", "auroc", "brier"]) & (P.subset == "overall") |
                 (P.metric == "acc") & (P.subset == "split_vote")]
        md.append("## 2. Paired differences (same fold and seed)\n\nCI = t-interval over all pairs. These pairs are not "
                  "independent (3 folds, so 3 test-slide sets), so the per-fold means and the number of folds agreeing in sign "
                  "are the conservative view.\n\n" + md_table(show) + "\n")

    # 3. before / after Stage III
    b3 = t[t.cfg.str.startswith("hsrl")]
    if len(b3):
        P3 = pd.concat([paired(t, c, c, "final", "before_stage3") for c in b3.cfg.unique()], ignore_index=True)
        P3.to_csv(out / "stage3_effect.csv", index=False)
        show = P3[(P3.metric.isin(["acc", "bal_acc", "auroc"]) & (P3.subset == "overall")) |
                  ((P3.metric == "acc") & (P3.subset.isin(["split_vote", "unanimous"])))]
        md.append("## 3. Effect of Stage III (after − before, paired within run)\n\n" + md_table(show) + "\n")
        per_run = []
        for run, g in b3.groupby("run"):
            row = {"run": run}
            for stg in ("before_stage3", "final"):
                for sub, met in (("overall", "acc"), ("overall", "bal_acc"), ("split_vote", "acc"), ("unanimous", "acc")):
                    v = g[(g.stage == stg) & (g.subset == sub)][met]
                    row[f"{'pre' if stg != 'final' else 'post'}_{met if sub == 'overall' else sub + '_acc'}"] = float(v.iloc[0]) if len(v) else np.nan
            per_run.append(row)
        pr = pd.DataFrame(per_run)
        pr.to_csv(out / "per_run_before_after_stage3.csv", index=False)
        md.append("### Every run: before (pre) / after (post) Stage III\n\n" + md_table(pr) + "\n")

    # 4. pseudo-label diagnostics
    if len(diag):
        diag.to_csv(out / "pseudo_label_diagnostics.csv", index=False)
        rows = [{"config": c, "runs": len(g), **{k: pm(g[k].astype(float)) for k in ("coverage", "precision", "prec_unanimous", "prec_split")},
                 "min_coverage": g.coverage.min()} for c, g in diag.groupby("cfg", sort=False)]
        md.append("## 4. Stage III pseudo-labels (vs hidden majority labels)\n\n" + md_table(pd.DataFrame(rows)) + "\n")

    # 5. collapse / escape
    if len(coll):
        coll.to_csv(out / "collapse_per_run.csv", index=False)
        rows = []
        for c, g in coll.groupby("cfg", sort=False):
            esc = g.escape_epoch.dropna()
            rows.append({"config": c, "runs": len(g), "stage1_epochs": int(g.n_epochs.iloc[0]),
                         "collapsed": f"{g.collapse_epoch.notna().sum()}/{len(g)}",
                         "escaped": f"{len(esc)}/{len(g)}",
                         "escape_epoch": " ".join(str(int(e)) for e in esc) if len(esc) else "-",
                         "spread_min": pm(g.spread_min), "spread_final": pm(g.spread_final),
                         "knn5_bal_acc_final": pm(g.knn5_bal_acc_final),
                         "t1/t2/t3_active_final": f"{g.t1_active_final.mean():.2f}/{g.t2_active_final.mean():.2f}/{g.t3_active_final.mean():.2f}"})
        md.append("## 5. Stage I collapse monitoring (collapse: spread < 0.1·s0; escape: later spread > 0.5·s0)\n\n"
                  + md_table(pd.DataFrame(rows)) + "\n\nPer run:\n\n"
                  + md_table(coll[["run", "spread_init", "spread_min", "epoch_min", "collapse_epoch", "escape_epoch",
                                   "spread_final", "knn5_bal_acc_final"]]) + "\n")
    (out / "report.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
