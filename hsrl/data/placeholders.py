"""Adapters still to be written. Each must return a SplitData (see base.py) with the same interface:
labelled (patch_id, path, label, q, optional reader votes), unlabelled / val / test (patch_id, path).

MHIST: annotations.csv gives majority label + number of SSA votes (7 readers). There is no reader linkage,
       so reader columns are NA and only counts_only is meaningful.
PCam:  a single label per image. q = label, no votes.
"""
from .registry import register


@register("mhist")
def load_mhist(cfg):
    """MHIST label set built by data/mhist_prepare.py. Folds = independent labelled draws on the official split.
    Votes are counts only (reader columns empty), so only the counts_only vote mode is meaningful."""
    from pathlib import Path
    from .gleason import load_label_set
    if cfg.get("vote_mode", "counts_only") not in ("counts_only", "linked"):
        raise ValueError("MHIST has no reader identities: use vote_mode counts_only")
    set_dir = Path(cfg["processed_root"]) / f"labels_p{cfg.get('labelled_pct', 10)}"
    if not set_dir.exists():
        raise FileNotFoundError(f"{set_dir} not built. Run: python -I data/mhist_prepare.py")
    return load_label_set(set_dir, {**cfg, "unlabelled_pool": "filtered"}, image_root=cfg["image_root"],
                          name=f"mhist/{set_dir.name}/draw{cfg['fold']}")


@register("pcam")
def load_pcam(cfg):
    raise NotImplementedError("PCam adapter not implemented yet")
