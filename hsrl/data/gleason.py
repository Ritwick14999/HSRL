"""Gleason2019 adapter: reads the label set built by data/gleason_labels.py.

Training-visible tables come from folds/fold{k}/{labelled_list,train_unlabelled,val,test}.csv. Of these,
only labelled_list carries votes. patches.csv (votes for every patch) is read only inside eval_labels.
"""
from pathlib import Path

import pandas as pd

from .base import SplitData
from .registry import register
from .votes import apply_vote_mode


def labels_set_name(cfg):
    name = f"labels_benign-{cfg['benign_rule']}"
    if cfg.get("exclude_readers"):
        name += "_excl-" + "-".join(f"r{r}" for r in sorted(cfg["exclude_readers"]))
    return name


@register("gleason")
def load_gleason(cfg):
    root = Path(cfg["processed_root"])
    set_dir = root / f"p{cfg['tile_size']}" / labels_set_name(cfg)
    if not set_dir.exists():
        excl = cfg.get("exclude_readers") or []
        raise FileNotFoundError(
            f"{set_dir} not built. Run: python -I data/gleason_labels.py tile_size={cfg['tile_size']} "
            f"benign_rule={cfg['benign_rule']} \"exclude_readers={list(excl)}\"")
    return load_label_set(set_dir, cfg, image_root=root, name=f"gleason/{set_dir.name}/fold{cfg['fold']}")


def load_label_set(set_dir, cfg, image_root, name):
    """Leakage-safe loading of a label set in the shared format (patches.csv + folds/fold<k>/...)."""
    set_dir = Path(set_dir)
    fold_dir = set_dir / "folds" / f"fold{cfg['fold']}"
    reader_cols = [f"r{k}" for k in range(1, 7)]

    lab = pd.read_csv(fold_dir / "labelled_list.csv", dtype={c: "Int64" for c in reader_cols})
    include_ties = cfg.get("include_ties", False)
    if not include_ties:
        lab = lab[lab.train_majority == 1]
    lab = apply_vote_mode(lab, reader_cols, cfg.get("vote_mode", "linked"), seed=cfg.get("vote_seed", 0))
    lab = lab.assign(label=lab.majority_label.fillna(-1).astype(int))
    labelled = lab[["patch_id", "core_id", "path", "label", "q", "n_readers", "votes_g4"] + reader_cols].reset_index(drop=True)

    pool = cfg.get("unlabelled_pool", "filtered")
    if pool == "filtered":
        unl = pd.read_csv(fold_dir / "train_unlabelled.csv")
    elif pool == "all_tissue":
        # every tissue tile on training-split cores that is not in the labelled list (no vote filter)
        split = pd.read_csv(fold_dir / "split.csv")
        train_cores = set(split.loc[split.split == "train", "core_id"])
        labelled_ids = set(split.loc[split.labelled == 1, "patch_id"])
        tiles = pd.read_csv(set_dir / "reader_labels.csv", usecols=["patch_id", "core_id", "path"])
        unl = tiles[tiles.core_id.isin(train_cores) & ~tiles.patch_id.isin(labelled_ids)]
    else:
        raise ValueError(f"unlabelled_pool {pool}")
    val = pd.read_csv(fold_dir / "val.csv")
    test = pd.read_csv(fold_dir / "test.csv")

    def eval_labels(split_name):
        p = pd.read_csv(set_dir / "patches.csv", dtype={c: "Int64" for c in reader_cols})
        ids = {"val": val, "test": test, "unlabelled": unl, "labelled": labelled}[split_name].patch_id
        cols = ["patch_id", "core_id", "majority_label", "q", "tie", "unanimous", "n_readers", "votes_g4"] + reader_cols
        return p[p.patch_id.isin(set(ids))][cols].reset_index(drop=True)

    return SplitData(name=name, image_root=Path(image_root), n_classes=2,
                     labelled=labelled, unlabelled=unl[["patch_id", "core_id", "path"]].reset_index(drop=True),
                     val=val[["patch_id", "core_id", "path"]], test=test[["patch_id", "core_id", "path"]],
                     reader_cols=reader_cols, _eval_labels=eval_labels)
