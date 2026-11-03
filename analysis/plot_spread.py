"""Stage I embedding spread (val subset) vs epoch for every run: one panel per fold (main grid, 30 epochs) plus a
panel for the fold-0 deviation runs (NOT the paper's protocol). Thin line per seed; colour = config.

Usage: python -I analysis/plot_spread.py --out results/REPORT_figures/spread_all_runs.png
"""
import argparse
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

# reference palette (dataviz skill, light): categorical slots 1-3 + chrome
COL = {"hsrl": "#2a78d6", "hsrl_no_t2": "#eb6834", "hsrl_s1e60": "#2a78d6", "hsrl_no_t2_s1e60": "#eb6834",
       "hsrl_boundary": "#1baf7a"}
LABEL = {"hsrl": "HSRL", "hsrl_no_t2": "HSRL without negatives term", "hsrl_s1e60": "HSRL, 60 epochs",
         "hsrl_no_t2_s1e60": "Without negatives term, 60 epochs", "hsrl_boundary": "HSRL, boundary mining rule"}
INK, INK2, MUTED, GRID, AXIS, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
NAME = re.compile(r"^f(\d+)s(\d+)_(.+)$")


def load(root, cfgs):
    out = []
    for d in sorted(Path(root).iterdir()):
        m = NAME.match(d.name)
        if m and m[3] in cfgs and (d / "stage1_monitor.csv").exists():
            mon = pd.read_csv(d / "stage1_monitor.csv")
            out.append((int(m[1]), int(m[2]), m[3], mon))
    return out


def style(ax, title):
    ax.set_facecolor(SURFACE)
    ax.set_title(title, color=INK, fontsize=10, loc="left")
    ax.set_xlabel("Epoch of embedding stage (−1 = before training)", color=INK2, fontsize=9)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS)
    ax.tick_params(colors=MUTED, labelsize=8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/REPORT_figures/spread_all_runs.png")
    ap.add_argument("--set", choices=["main", "s1e60"], default="main",
                    help="main: 30-epoch grid + fold-0 deviation panel; s1e60: 60-epoch Stage I runs on all folds")
    args = ap.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if args.set == "s1e60":
        runs = load("results/deviations", {"hsrl_s1e60", "hsrl_no_t2_s1e60"})
        fig, axes = plt.subplots(1, 3, figsize=(14, 4.2), facecolor=SURFACE, sharey=True)
        for f in range(3):
            for fold, seed, cfg, mon in runs:
                if fold == f:
                    ax = axes[f]
                    ax.plot(mon.epoch, mon.val_spread_sq, color=COL[cfg], linewidth=1.4, alpha=0.85, label=LABEL[cfg])
            style(axes[f], f"Fold {f}")
        h, l = axes[0].get_legend_handles_labels()
        uniq = dict(zip(l, h))
        fig.legend(list(uniq.values()), list(uniq.keys()), loc="lower left", bbox_to_anchor=(0.06, 0.0), ncol=2,
                   frameon=False, fontsize=9, labelcolor=INK2)
        axes[0].set_ylabel("Embedding spread (validation)", color=INK2, fontsize=9)
        fig.tight_layout(rect=(0, 0.06, 1, 1))
        fig.savefig(out, dpi=130, facecolor=SURFACE)
        print(out)
        return
    main_runs = load("results/main", {"hsrl", "hsrl_no_t2"})
    dev_runs = [r for r in load("results/deviations", {"hsrl_s1e60", "hsrl_no_t2_s1e60", "hsrl_boundary"})
                if r[0] == 0 and r[1] <= 2]   # the fold-0, 3-seed deviation set of REPORT.md §3
    fig, axes = plt.subplots(1, 4, figsize=(17, 4.2), facecolor=SURFACE, sharey=True)
    for f in range(3):
        ax = axes[f]
        seen = set()
        for fold, seed, cfg, mon in main_runs:
            if fold != f:
                continue
            ax.plot(mon.epoch, mon.val_spread_sq, color=COL[cfg], linewidth=1.4, alpha=0.85,
                    label=LABEL[cfg] if cfg not in seen else None)
            seen.add(cfg)
        style(ax, f"Fold {f}")
    ax = axes[3]
    seen = set()
    for fold, seed, cfg, mon in dev_runs:
        ax.plot(mon.epoch, mon.val_spread_sq, color=COL[cfg], linewidth=1.4, alpha=0.85,
                linestyle="-" if cfg != "hsrl_no_t2_s1e60" else (0, (1, 0)),
                label=LABEL[cfg] if cfg not in seen else None)
        seen.add(cfg)
    style(ax, "Fold 0, modified settings")
    hd, ld = ax.get_legend_handles_labels()
    fig.legend(hd, ld, loc="lower right", bbox_to_anchor=(0.99, 0.0), ncol=3, frameon=False, fontsize=9, labelcolor=INK2)
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower left", bbox_to_anchor=(0.06, 0.0), ncol=2, frameon=False, fontsize=9, labelcolor=INK2)
    axes[0].set_ylabel("Embedding spread (validation)", color=INK2, fontsize=9)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(out, dpi=130, facecolor=SURFACE)
    print(out)


if __name__ == "__main__":
    main()
