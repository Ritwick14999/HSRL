"""Summarise a set of runs: test metrics (overall / unanimous / split-vote), Stage III diagnostics, Stage I collapse
monitoring curves. Writes <out>/summary.md, <out>/test_metrics.csv and <out>/collapse_<run>.png.

Usage: python -I analysis/summarise_runs.py --runs results/a results/b ... --out results/phase3_fold0
"""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

# reference palette (dataviz skill, light mode): categorical slots 1-4 + chart chrome
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
INK, INK2, MUTED, GRID, AXIS, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"


def style_axes(ax, title, ylabel):
    ax.set_facecolor(SURFACE)
    ax.set_title(title, color=INK, fontsize=10, loc="left")
    ax.set_ylabel(ylabel, color=INK2, fontsize=9)
    ax.set_xlabel("Stage I epoch (-1 = before training)", color=INK2, fontsize=9)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS)
    ax.tick_params(colors=MUTED, labelsize=8)


def line_panel(ax, df, cols, labels, title, ylabel, ylim=None):
    ends = []
    for i, (c, lab) in enumerate(zip(cols, labels)):
        d = df[["epoch", c]].dropna()
        ax.plot(d.epoch, d[c], color=SERIES[i], linewidth=2, label=lab)
        ends.append((d[c].iloc[-1], lab, d.epoch.iloc[-1]))
    style_axes(ax, title, ylabel)
    if ylim:
        ax.set_ylim(*ylim)
    # end labels, dodged vertically so coincident series stay legible
    lo, hi = ax.get_ylim()
    gap = 0.06 * (hi - lo)
    placed = []
    for y, lab, x in sorted(ends):
        y_lab = max(y, placed[-1] + gap) if placed else y
        placed.append(y_lab)
        ax.annotate(lab, (x, y), xytext=(x + 0.6, y_lab), textcoords="data", color=INK2, fontsize=8, va="center")
    ax.legend(frameon=False, fontsize=8, labelcolor=INK2, loc="best")
    ax.margins(x=0.12)


def collapse_figure(mon, title, path):
    fig, axes = plt.subplots(2, 2, figsize=(11, 7), facecolor=SURFACE)
    line_panel(axes[0, 0], mon, ["mean_d_ap", "mean_d_an", "mean_d_nc", "mean_d_ac"],
               ["d_ap", "d_an", "d_nc", "d_ac"], "Mean tuple distances (mined tuples)", "squared distance")
    line_panel(axes[0, 1], mon, ["frac_t1_active", "frac_t2_active", "frac_t3_active"],
               ["term 1", "term 2", "term 3"], "Fraction of tuples with an active hinge", "fraction", (0, 1.05))
    line_panel(axes[1, 0], mon, ["val_spread_sq"], ["spread"],
               "Embedding spread: mean pairwise sq. distance (fixed val subset)", "squared distance")
    line_panel(axes[1, 1], mon, ["knn5_acc", "knn5_bal_acc"], ["accuracy", "balanced acc."],
               "kNN (k=5) on val, projection embeddings", "score", (0.4, 1.0))
    fig.suptitle(title, color=INK, fontsize=11, x=0.01, ha="left")
    fig.tight_layout()
    fig.savefig(path, dpi=130, facecolor=SURFACE)
    plt.close(fig)


def md_table(df):
    cols = list(df.columns)
    out = ["| " + " | ".join(map(str, cols)) + " |", "|" + "---|" * len(cols)]
    out += ["| " + " | ".join(str(r[c]) for c in cols) + " |" for _, r in df.iterrows()]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rows, diag_rows, md = [], [], ["# Fold 0, seed 0: baseline runs\n"]
    for r in map(Path, args.runs):
        m = json.load(open(r / "metrics.json"))
        evals = {k: v for k, v in m.items() if k.startswith("eval_")}
        for tag, ev in evals.items():
            for subset, mm in ev["test"].items():
                rows.append({"run": r.name, "stage": tag[5:], "subset": subset, **mm})
        for rnd, d in (m.get("pseudo_label_diagnostics") or {}).items():
            diag_rows.append({"run": r.name, "round": rnd, "pool": d["pool"], "accepted": d["accepted"],
                              "coverage": d["coverage"], "precision": d["overall"]["precision"],
                              "prec_unanimous": d["unanimous"]["precision"], "n_unanimous": d["unanimous"]["n"],
                              "prec_split": d["split_vote"]["precision"], "n_split": d["split_vote"]["n"],
                              "tie_accepted": d["tie_accepted"]})
        if m.get("flags"):
            md.append(f"**FLAG ({r.name})**: " + "; ".join(m["flags"]) + "\n")
        if (r / "stage1_monitor.csv").exists():
            mon = pd.read_csv(r / "stage1_monitor.csv")
            collapse_figure(mon, f"Stage I collapse monitoring: {r.name}", out / f"collapse_{r.name}.png")
            keep = ["epoch", "mean_d_ap", "mean_d_an", "mean_d_nc", "mean_d_ac", "frac_t1_active", "frac_t2_active",
                    "frac_t3_active", "val_spread_sq", "val_mean_norm_of_mean", "knn5_acc", "knn5_bal_acc"]
            sub = mon[mon.epoch.isin([-1, 0, 1, 2, 4, 9, 14, 19, 24, 29])][[c for c in keep if c in mon]].round(3)
            md.append(f"## Stage I monitoring: {r.name}\n\n![](collapse_{r.name}.png)\n\n" + md_table(sub) + "\n")
        md.append(f"- {r.name}: wall time {m.get('wall_time_sec')} s, max GPU mem {m['env'].get('max_gpu_mem_gb')} GB, "
                  f"data {m['data']}\n")
    t = pd.DataFrame(rows)
    t.to_csv(out / "test_metrics.csv", index=False)
    show = t[["run", "stage", "subset", "n", "acc", "bal_acc", "macro_f1", "auroc", "brier"]]
    md.insert(1, "## Test metrics (fold 0 test slides 001 + 003, non-tie patches)\n\n" + md_table(show) + "\n")
    if diag_rows:
        md.insert(2, "## Stage III pseudo-labels (precision vs hidden majority labels, non-tie)\n\n"
                  + md_table(pd.DataFrame(diag_rows)) + "\n")
    (out / "summary.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
