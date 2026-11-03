"""Phase 1b: per-reader patch labels -> binary votes -> patch filter -> slide-grouped folds.

Reads  <processed_root>/p{T}/tiles_raw.csv  (from data/gleason_extract.py)
Writes <processed_root>/p{T}/<name>/
         patches.csv                       one row per kept patch (votes for ALL patches, analysis only)
         reader_labels.csv                 every tissue tile, raw per-reader label + coverage
         folds/fold{k}/split.csv           patch_id, split (train/val/test), labelled, train_majority
         folds/fold{k}/labelled_list.csv   labelled training patches (the only patches whose votes may train)
         folds/fold{k}/{train_unlabelled,val,test}.csv   patch ids only (no votes, by design)
         stats.json, config.yaml

Reader label (per tile, per reader who annotated the core): dominant class over the tile's tissue
pixels, counting unannotated (mask 0) as its own class; valid only if it covers >= min_coverage of
tissue pixels and is not "unann". Raw labels: NA (no map / empty map / excluded), none, benign, g3, g4, g5.
Binary vote: g3 -> 0, g4/g5 -> 1; benign -> NA (benign_rule=ignore) or drop the patch (benign_rule=drop).

LEAKAGE RULE: votes may enter training only for labelled training patches. This script only writes
them to patches.csv / labelled_list.csv; the unlabelled/val/test split files carry ids only.

Usage:  python -I data/gleason_labels.py --config configs/data/gleason_labels.yaml [key=value ...]
        python -I data/gleason_labels.py --choose-folds tile_size=512
"""
import argparse
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.model_selection import StratifiedGroupKFold

CLASS_NAMES = ["unann", "benign", "g3", "g4", "g5"]
BINARY = {"g3": 0, "g4": 1, "g5": 1}


def load_config(path, overrides):
    cfg = yaml.safe_load(open(path))
    for o in overrides:
        k, v = o.split("=", 1)
        cfg[k] = yaml.safe_load(v)
    if not cfg.get("name"):
        tag = f"labels_benign-{cfg['benign_rule']}"
        if cfg["exclude_readers"]:
            tag += "_excl-" + "-".join(f"r{r}" for r in cfg["exclude_readers"])
        cfg["name"] = tag
    return cfg


def reader_labels(tiles, cfg):
    """Raw per-reader label and dominant-class coverage for every tissue tile."""
    out = tiles[["patch_id", "core_id", "slide", "path", "tissue_frac", "tissue_px"]].copy()
    for k in range(1, cfg["n_readers"] + 1):
        counts = tiles[[f"r{k}_n_{c}" for c in CLASS_NAMES]].to_numpy()
        annotated = (tiles[f"r{k}_status"] == "annotated").to_numpy() & (k not in cfg["exclude_readers"])
        dom = counts.argmax(1)
        cov = counts.max(1) / tiles["tissue_px"].to_numpy()
        lab = np.where(dom == 0, "none", np.array(CLASS_NAMES, dtype=object)[dom])
        lab = np.where(cov >= cfg["min_coverage"], lab, "none")
        out[f"raw_r{k}"] = np.where(annotated, lab, "NA")
        out[f"cov_r{k}"] = np.where(annotated, np.round(cov, 4), np.nan)
        out[f"dom_r{k}"] = np.where(annotated, np.array(CLASS_NAMES, dtype=object)[dom], "NA")
    return out


def binary_votes(rl, cfg):
    """Apply the binary mapping, benign rule and min-reader filter. Returns kept patches."""
    R = cfg["n_readers"]
    df = rl.copy()
    raw = df[[f"raw_r{k}" for k in range(1, R + 1)]]
    df["n_annotators"] = (raw != "NA").sum(axis=1)
    df["n_benign"] = (raw == "benign").sum(axis=1)
    for k in range(1, R + 1):
        df[f"r{k}"] = df[f"raw_r{k}"].map(BINARY).astype("Int64")
    votes = df[[f"r{k}" for k in range(1, R + 1)]]
    df["n_readers"] = votes.notna().sum(axis=1)
    df["votes_g4"] = votes.sum(axis=1, skipna=True).astype(int)
    keep = df["n_readers"] >= cfg["min_valid_readers"]
    if cfg["benign_rule"] == "drop":
        keep &= df["n_benign"] == 0
    elif cfg["benign_rule"] != "ignore":
        raise ValueError(cfg["benign_rule"])
    df = df[keep].copy()
    df["q"] = (df["votes_g4"] / df["n_readers"]).round(6)
    df["tie"] = 2 * df["votes_g4"] == df["n_readers"]
    df["majority_label"] = pd.array(np.where(df["tie"], pd.NA, (df["q"] > 0.5).astype(int)), dtype="Int64")
    df["unanimous"] = (df["votes_g4"] == 0) | (df["votes_g4"] == df["n_readers"])
    df["group_id"] = df["slide"]
    cols = (["patch_id", "core_id", "group_id", "path", "n_readers"] + [f"r{k}" for k in range(1, R + 1)]
            + ["votes_g4", "q", "majority_label", "tie", "unanimous", "n_annotators", "n_benign", "tissue_frac"]
            + [f"raw_r{k}" for k in range(1, R + 1)] + [f"cov_r{k}" for k in range(1, R + 1)])
    return df[cols].reset_index(drop=True)


def stratum(p):
    return np.where(p["tie"], 2, p["majority_label"].fillna(0).astype(int))


def choose_folds(p, slides):
    """Score every partition of the slides into 3 test pairs: test size near 1/3, G4 rate near overall."""
    nt = p[~p.tie]
    g_all = nt.majority_label.mean()
    rows = []
    first = slides[0]
    for partner in slides[1:]:
        rest = [s for s in slides if s not in (first, partner)]
        for partner2 in rest[1:]:
            last = [s for s in rest if s not in (rest[0], partner2)]
            folds = [(first, partner), (rest[0], partner2), tuple(last)]
            share = [p.group_id.isin(f).mean() for f in folds]
            g4 = [nt[nt.group_id.isin(f)].majority_label.mean() for f in folds]
            score = sum(abs(s - 1 / 3) for s in share) + sum(abs(g - g_all) for g in g4)
            rows.append({"folds": folds, "test_share": np.round(share, 3).tolist(),
                         "test_g4_rate": np.round(g4, 3).tolist(), "score": round(score, 4)})
    return pd.DataFrame(rows).sort_values("score").reset_index(drop=True), g_all


def make_splits(p, cfg, fold_idx, test_slides):
    rng = np.random.default_rng([cfg["seed"], fold_idx])
    split = pd.Series("train", index=p.index)
    split[p.group_id.isin(test_slides)] = "test"
    tr = p[split == "train"]
    n_splits = max(2, round(1 / cfg["val_frac"]))
    sgkf = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=cfg["seed"] + fold_idx)
    _, val_idx = next(sgkf.split(tr, stratum(tr), groups=tr.core_id))
    split[tr.index[val_idx]] = "val"
    labelled = pd.Series(False, index=p.index)
    tr = p[split == "train"]
    st = pd.Series(stratum(tr), index=tr.index)
    for s in sorted(st.unique()):
        idx = st.index[st == s].to_numpy()
        n = int(round(cfg["labelled_frac"] * len(idx)))
        labelled[rng.choice(idx, n, replace=False)] = True
    train_majority = labelled & ~(p.tie & cfg["exclude_ties_from_training"])
    return pd.DataFrame({"patch_id": p.patch_id, "core_id": p.core_id, "group_id": p.group_id, "split": split,
                         "labelled": labelled.astype(int), "train_majority": train_majority.astype(int)})


def split_stats(p, s):
    out = {}
    m = p.merge(s[["patch_id", "split", "labelled"]], on="patch_id")
    m["part"] = np.where(m.split == "train", np.where(m.labelled == 1, "train_labelled", "train_unlabelled"), m.split)
    for part, g in list(m.groupby("part")) + [("train", m[m.split == "train"])]:
        out[part] = {"n": int(len(g)), "n_g3": int((g.majority_label == 0).sum()), "n_g4": int((g.majority_label == 1).sum()),
                     "n_tie": int(g.tie.sum()), "unanimous_frac": round(float(g.unanimous.mean()), 4) if len(g) else None,
                     "n_cores": int(g.core_id.nunique()), "slides": sorted(g.group_id.unique().tolist())}
    return out


def dataset_stats(rl, p, cfg):
    R = cfg["n_readers"]
    st = {"n_tissue_tiles": int(len(rl)), "n_kept": int(len(p)), "n_cores_kept": int(p.core_id.nunique())}
    raw = rl[[f"raw_r{k}" for k in range(1, R + 1)]]
    st["raw_label_counts_reader_tile"] = {k: int(v) for k, v in raw.stack().value_counts().items()}
    dom = rl[[f"dom_r{k}" for k in range(1, R + 1)]].to_numpy()
    none_mask = raw.to_numpy() == "none"
    st["none_reason"] = {"dominant_unannotated": int((none_mask & (dom == "unann")).sum()),
                         "dominant_below_coverage": int((none_mask & (dom != "unann")).sum())}
    # funnel
    nb = (raw == "benign").sum(axis=1)
    nv = raw.isin(list(BINARY)).sum(axis=1)
    st["funnel"] = {"tiles_with_>=1_binary_vote": int((nv >= 1).sum()),
                    f"tiles_with_>={cfg['min_valid_readers']}_binary_votes": int((nv >= cfg["min_valid_readers"]).sum()),
                    "of_those_with_any_benign_reader": int(((nv >= cfg["min_valid_readers"]) & (nb > 0)).sum())}
    st["class"] = {"g3": int((p.majority_label == 0).sum()), "g4": int((p.majority_label == 1).sum()), "tie": int(p.tie.sum())}
    st["unanimous_frac"] = round(float(p.unanimous.mean()), 4)
    st["unanimous_frac_non_tie"] = round(float(p[~p.tie].unanimous.mean()), 4)
    st["n_readers_hist"] = {int(k): int(v) for k, v in p.n_readers.value_counts().sort_index().items()}
    q = p.assign(qf=p.votes_g4.astype(str) + "/" + p.n_readers.astype(str))
    st["q_by_fraction"] = {k: int(v) for k, v in q.qf.value_counts().sort_index().items()}
    st["q_hist"] = {f"[{a:.1f},{b:.1f}{']' if b == 1 else ')'}": int(((p.q >= a) & ((p.q < b) | ((b == 1) & (p.q <= 1)))).sum())
                    for a, b in zip(np.arange(0, 1, 0.2), np.arange(0.2, 1.01, 0.2))}
    st["q_mean"] = round(float(p.q.mean()), 4)
    readers = {}
    for k in range(1, R + 1):
        v = p[f"r{k}"]
        readers[f"r{k}"] = {"n_votes": int(v.notna().sum()), "frac_patches": round(float(v.notna().mean()), 4),
                            "g4_rate": round(float(v.mean()), 4) if v.notna().any() else None,
                            "n_cores_with_votes": int(p.loc[v.notna(), "core_id"].nunique())}
    st["readers"] = readers
    pair = {}
    for a, b in itertools.combinations(range(1, R + 1), 2):
        both = p[f"r{a}"].notna() & p[f"r{b}"].notna()
        if both.sum() == 0:
            continue
        x, y = p.loc[both, f"r{a}"].astype(int).to_numpy(), p.loc[both, f"r{b}"].astype(int).to_numpy()
        po = (x == y).mean()
        pe = x.mean() * y.mean() + (1 - x.mean()) * (1 - y.mean())
        pair[f"r{a}-r{b}"] = {"n_shared": int(both.sum()), "agree": round(float(po), 4),
                              "kappa": round(float((po - pe) / (1 - pe)), 4) if pe < 1 else None}
    st["pairwise_binary_agreement"] = pair
    return st


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/data/gleason_labels.yaml")
    ap.add_argument("--choose-folds", action="store_true")
    ap.add_argument("overrides", nargs="*")
    args = ap.parse_args()
    cfg = load_config(args.config, args.overrides)
    root = Path(cfg["processed_root"]) / f"p{cfg['tile_size']}"
    tiles = pd.read_csv(root / "tiles_raw.csv")
    rl = reader_labels(tiles, cfg)
    p = binary_votes(rl, cfg)

    if args.choose_folds:
        table, g_all = choose_folds(p, sorted(p.group_id.unique()))
        pd.set_option("display.width", 200)
        print(f"overall G4 rate (non-tie) {g_all:.3f}; {len(p)} patches")
        print(table.to_string())
        return

    out = root / cfg["name"]
    (out / "folds").mkdir(parents=True, exist_ok=True)
    with open(out / "config.yaml", "w") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)
    rl.to_csv(out / "reader_labels.csv", index=False)
    p.to_csv(out / "patches.csv", index=False)
    stats = dataset_stats(rl, p, cfg)
    stats["folds"] = {}
    for i, test_slides in enumerate(cfg["folds"]):
        s = make_splits(p, cfg, i, test_slides)
        fd = out / "folds" / f"fold{i}"
        fd.mkdir(parents=True, exist_ok=True)
        s.to_csv(fd / "split.csv", index=False)
        lab = p.merge(s.loc[s.labelled == 1, ["patch_id", "train_majority"]], on="patch_id")
        lab[["patch_id", "core_id", "group_id", "path", "majority_label", "tie", "train_majority", "n_readers"]
            + [f"r{k}" for k in range(1, cfg["n_readers"] + 1)] + ["votes_g4", "q"]].to_csv(fd / "labelled_list.csv", index=False)
        for name, sel in [("train_unlabelled", (s.split == "train") & (s.labelled == 0)),
                          ("val", s.split == "val"), ("test", s.split == "test")]:
            s.loc[sel, ["patch_id", "core_id", "group_id"]].merge(p[["patch_id", "path"]], on="patch_id").to_csv(
                fd / f"{name}.csv", index=False)
        fs = split_stats(p, s)
        fs["test_slides"] = list(test_slides)
        # alternative unlabelled pool: every tissue tile on training cores not in val/labelled (no vote filter)
        train_cores = set(s.loc[s.split == "train", "core_id"])
        lab_ids = set(s.loc[s.labelled == 1, "patch_id"])
        fs["alt_unlabelled_pool_all_tissue"] = int((rl.core_id.isin(train_cores) & ~rl.patch_id.isin(lab_ids)).sum())
        stats["folds"][f"fold{i}"] = fs
    with open(out / "stats.json", "w") as f:
        json.dump(stats, f, indent=2)
    print(f"wrote {out}  kept={stats['n_kept']} class={stats['class']} unanimous={stats['unanimous_frac']}")


if __name__ == "__main__":
    main()
