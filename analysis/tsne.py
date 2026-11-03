"""t-SNE of test-set representations for one (fold, seed).

Row 1: backbone features f (final model) for every config, the representation the classifier sees.
Row 2: projection embeddings z (the paper's t-SNE space) after Stage I and at the end of training, for the HSRL variants.
Figure A colours by majority label (ties excluded); figure B colours by vote fraction q (diverging, ties included).
Silhouette scores (cosine, in the original space, majority labels) are reported per panel.

Usage: python -I analysis/tsne.py --root results/main --fold 0 --seed 0 --out results/main_summary
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import yaml
from matplotlib.colors import LinearSegmentedColormap
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score

from hsrl.data import ImageDataset, build_transforms, load_dataset
from hsrl.models import HSRLNet

# reference palette (dataviz skill, light): categorical slots 1-2, diverging blue <-> red with gray midpoint
C_G3, C_G4 = "#2a78d6", "#eb6834"
DIVERGING = LinearSegmentedColormap.from_list("q", ["#2a78d6", "#c3c2b7", "#e34948"])
INK, INK2, MUTED, AXIS, SURFACE = "#0b0b0b", "#52514e", "#898781", "#c3c2b7", "#fcfcfb"


@torch.no_grad()
def extract(run_dir, ckpt, cfg, df, device):
    model = HSRLNet(n_classes=2, **{**cfg["model"], "pretrained": False}).to(device)
    model.load_state_dict(torch.load(run_dir / ckpt, map_location=device))
    model.eval()
    dl = torch.utils.data.DataLoader(ImageDataset(df, cfg["data"]["processed_root"], build_transforms(cfg["augment"], False)),
                                     batch_size=128, num_workers=0)
    fs, zs = [], []
    for b in dl:
        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=device.type == "cuda"):
            f = model.features(b["image"].to(device))
        fs.append(f.float().cpu())
        zs.append(model.embed(f).cpu())
    return torch.cat(fs).numpy(), torch.cat(zs).numpy()


def tsne(x, seed):
    x = PCA(n_components=min(50, x.shape[1]), random_state=seed).fit_transform(x)
    return TSNE(perplexity=30, init="pca", random_state=seed).fit_transform(x)


def style(ax, title):
    ax.set_facecolor(SURFACE)
    ax.set_title(title, color=INK, fontsize=9, loc="left")
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(AXIS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="results/main")
    ap.add_argument("--fold", type=int, default=0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default="results/main_summary")
    args = ap.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    tag = f"f{args.fold}s{args.seed}"
    runs = {c: Path(args.root) / f"{tag}_{c}" for c in ("supervised", "hsrl", "hsrl_no_t2", "hsrl_no_stage1")}
    cfg = yaml.safe_load(open(runs["hsrl"] / "config.yaml"))
    data = load_dataset(cfg["data"])
    test = data.test
    lab = data.eval_labels("test").set_index("patch_id").loc[test.patch_id]   # evaluation only
    tie = lab.tie.astype(bool).to_numpy()
    y = lab.majority_label.fillna(-1).astype(int).to_numpy()
    q = lab.q.to_numpy(float)
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    panels = []
    feats = {}
    for c, r in runs.items():
        feats[(c, "final")] = extract(r, "model_final.pt", cfg, test, dev)
        if (r / "model_stage1.pt").exists():
            feats[(c, "stage1")] = extract(r, "model_stage1.pt", cfg, test, dev)
    for c in runs:
        panels.append((f"{c}: backbone f (final)", feats[(c, "final")][0]))
    for c in ("hsrl", "hsrl_no_t2"):
        panels.append((f"{c}: projection z (after Stage I)", feats[(c, "stage1")][1]))
        panels.append((f"{c}: projection z (final)", feats[(c, "final")][1]))

    emb, sil = [], []
    for title, x in panels:
        emb.append(tsne(x, args.seed))
        sil.append(silhouette_score(x[~tie], y[~tie], metric="cosine"))
        print(f"{title}: silhouette {sil[-1]:.3f}", flush=True)
    pd.DataFrame({"panel": [p[0] for p in panels], "silhouette_cosine": sil}).to_csv(out / f"tsne_{tag}_silhouette.csv", index=False)
    np.savez_compressed(out / f"tsne_{tag}_coords.npz", coords=np.stack(emb), patch_id=test.patch_id.to_numpy(), q=q, y=y)

    for mode in ("label", "q"):
        fig, axes = plt.subplots(2, 4, figsize=(16, 8.4), facecolor=SURFACE)
        for ax, (title, _), e, s in zip(axes.ravel(), panels, emb, sil):
            if mode == "label":
                for k, col, name in ((0, C_G3, "G3 (majority)"), (1, C_G4, "G4/5 (majority)")):
                    m = (y == k) & ~tie
                    ax.scatter(e[m, 0], e[m, 1], s=4, c=col, alpha=0.55, linewidths=0, label=name)
            else:
                sc = ax.scatter(e[:, 0], e[:, 1], s=4, c=q, cmap=DIVERGING, vmin=0, vmax=1, alpha=0.7, linewidths=0)
            style(ax, f"{title}\nsilhouette {s:.3f}")
        if mode == "label":
            h, l = axes[0, 0].get_legend_handles_labels()
            fig.legend(h, l, loc="lower center", ncol=2, frameon=False, markerscale=4, labelcolor=INK2)
        else:
            cb = fig.colorbar(sc, ax=axes, orientation="horizontal", fraction=0.03, pad=0.04)
            cb.set_label("q = fraction of readers voting G4/5", color=INK2)
            cb.ax.tick_params(colors=MUTED)
        fig.suptitle(f"t-SNE of test patches, fold {args.fold} seed {args.seed} "
                     f"({'coloured by majority label, ties excluded' if mode == 'label' else 'coloured by vote fraction q'})",
                     color=INK, x=0.01, ha="left")
        if mode == "label":
            fig.tight_layout(rect=(0, 0.04, 1, 0.97))
        fig.savefig(out / f"tsne_{tag}_{mode}.png", dpi=120, facecolor=SURFACE)
        plt.close(fig)
    print("done")


if __name__ == "__main__":
    main()
