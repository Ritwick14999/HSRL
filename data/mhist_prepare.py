"""Prepare MHIST in the same label-set format as Gleason, so the whole pipeline runs unchanged.

Reads  data/mhist/annotations.csv (Image Name, Majority Vote Label, Number of Annotators who Selected SSA (Out of 7),
       Partition) and data/mhist/images/*.png (224x224, already the network's input size).
Writes <out>/labels_p<pct>/patches.csv and folds/fold<k>/{split,labelled_list,train_unlabelled,val,test}.csv
       for each labelled fraction, plus config.yaml and stats.json.

MHIST releases vote COUNTS only (7 pathologists, no reader identities): reader columns r1..r6 stay empty and
q = SSA votes / 7. SSA = label 1 (the "positive" class, as G4/5 in Gleason). Folds = independent labelled draws on
the official split: fold k draws its validation set (val_frac of train) and its labelled subset (labelled_frac of
train, from the non-val images), both stratified by majority label with seed k. Test = the official test partition,
or with --split random a per-draw random test set of the same size (protocol check, D43).

Usage: python -I data/mhist_prepare.py [--root data/mhist] [--out data/processed/mhist] [--draws 5]
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

READERS = [f"r{k}" for k in range(1, 7)]


def stratified_take(df, frac_of, n_total, rng):
    """Take round(frac * n_total) rows of df, stratified by majority_label."""
    n = int(round(frac_of * n_total))
    parts = []
    for _, g in df.groupby("majority_label"):
        k = int(round(n * len(g) / len(df)))
        parts.append(g.index[rng.permutation(len(g))[:k]])
    return np.concatenate(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="data/mhist")
    ap.add_argument("--out", default="data/processed/mhist")
    ap.add_argument("--draws", type=int, default=5)
    ap.add_argument("--val-frac", type=float, default=0.10)
    ap.add_argument("--labelled-fracs", type=float, nargs="+", default=[0.10, 1.0])
    ap.add_argument("--labelled-of", choices=["train", "all"], default="train",
                    help="labelled count = frac x train images (default) or frac x all 3,152 images (protocol check)")
    ap.add_argument("--split", choices=["official", "random"], default="official",
                    help="official train/test partition (default), or per draw a random image-level train/test split of "
                         "all images with the official sizes, stratified by label (protocol check D43; suffix 'rs')")
    args = ap.parse_args()
    a = pd.read_csv(Path(args.root) / "annotations.csv")
    a.columns = ["image", "label", "ssa_votes", "partition"]
    assert ((a.label == "SSA") == (a.ssa_votes >= 4)).all(), "majority label disagrees with the vote count"
    assert all((Path(args.root) / "images" / f).exists() for f in a.image)
    p = pd.DataFrame({"patch_id": a.image.str.replace(".png", "", regex=False), "path": "images/" + a.image,
                      "n_readers": 7, "votes_g4": a.ssa_votes, "q": (a.ssa_votes / 7).round(6),
                      "majority_label": (a.label == "SSA").astype(int), "tie": False,
                      "unanimous": a.ssa_votes.isin([0, 7]), "partition": a.partition})
    p["core_id"] = p.patch_id                       # no patient / slide grouping in the release
    p["group_id"] = "mhist_" + p.partition
    for r in READERS:
        p[r] = pd.array([pd.NA] * len(p), dtype="Int64")
    suffix = ("all" if args.labelled_of == "all" else "") + ("rs" if args.split == "random" else "")
    n_test = int((p.partition == "test").sum())
    for frac in args.labelled_fracs:
        d = Path(args.out) / f"labels_p{int(round(frac * 100))}{suffix}"
        (d / "folds").mkdir(parents=True, exist_ok=True)
        p.to_csv(d / "patches.csv", index=False)       # 'partition' = official partition; the draw's split is in split.csv
        stats = {"n": len(p), "train": len(p) - n_test, "test": n_test, "split": args.split, "folds": {}}
        for k in range(args.draws):
            rng = np.random.default_rng([20261031, k])
            if args.split == "random":                  # own RNG stream, so val/labelled draws use rng exactly as before
                test_idx = stratified_take(p, n_test / len(p), len(p), np.random.default_rng([20261031, k, 1]))
                is_test = p.index.isin(test_idx)
            else:
                is_test = (p.partition == "test").to_numpy()
            train = p[~is_test]
            val_idx = stratified_take(train, args.val_frac, len(train), rng)
            rest = train.drop(val_idx)
            n_ref = len(p) if args.labelled_of == "all" else len(train)
            lab_idx = rest.index if frac >= 1.0 else stratified_take(rest, frac, n_ref, rng)
            split = pd.Series("train", index=p.index)
            split[is_test] = "test"
            split[val_idx] = "val"
            labelled = pd.Series(0, index=p.index)
            labelled[lab_idx] = 1
            s = pd.DataFrame({"patch_id": p.patch_id, "core_id": p.core_id, "group_id": p.group_id, "split": split,
                              "labelled": labelled, "train_majority": labelled})
            fd = d / "folds" / f"fold{k}"
            fd.mkdir(parents=True, exist_ok=True)
            s.to_csv(fd / "split.csv", index=False)
            lab = p.loc[labelled == 1].assign(train_majority=1)
            lab[["patch_id", "core_id", "group_id", "path", "majority_label", "tie", "train_majority", "n_readers"]
                + READERS + ["votes_g4", "q"]].to_csv(fd / "labelled_list.csv", index=False)
            for name, sel in (("train_unlabelled", (split == "train") & (labelled == 0)), ("val", split == "val"),
                              ("test", split == "test")):
                p.loc[sel, ["patch_id", "core_id", "group_id", "path"]].to_csv(fd / f"{name}.csv", index=False)
            stats["folds"][f"fold{k}"] = {"labelled": int(labelled.sum()), "labelled_ssa": int(p.loc[labelled == 1, "majority_label"].sum()),
                                          "unlabelled": int(((split == "train") & (labelled == 0)).sum()),
                                          "val": int((split == "val").sum()), "test": int((split == "test").sum()),
                                          "test_ssa": int(p.loc[split == "test", "majority_label"].sum()),
                                          "test_official": int((p.partition[split == "test"] == "test").sum())}
        with open(d / "stats.json", "w") as f:
            json.dump(stats, f, indent=2)
        with open(d / "config.yaml", "w") as f:
            yaml.safe_dump({"val_frac": args.val_frac, "labelled_frac": frac, "labelled_of": args.labelled_of,
                            "split": args.split, "draws": args.draws, "seed": 20261031}, f)
        print(d, json.dumps(stats["folds"]["fold0"]))


if __name__ == "__main__":
    main()
