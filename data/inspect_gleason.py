"""Phase 0: inspect the Gleason2019 training set (no training).

Reads   <root>/TrainImgs/*.jpg and <root>/Map{1..6}/*.png  (one folder per pathologist map)
Writes  <out>/files_*.csv, mask_values.csv, value_appearance.csv, reader_counts.csv,
        pairwise_kappa.csv, loo_agreement.csv, zip_timestamps.csv, phase0_summary.json

Usage:  python -I data/inspect_gleason.py --root data/gleason --out results/phase0_inspect
"""
import argparse
import hashlib
import json
import re
import zipfile
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

N_MAPS = 6
IMG_RE = re.compile(r"^slide(\d{3})_core(\d{3})\.jpg$")
MASK_RE = re.compile(r"^slide(\d{3})_core(\d{3})_classimg_nonconvex\.png$")
DS_STATS = 4    # downsample factor for value-appearance statistics
DS_AGREE = 8    # downsample factor for inter-map agreement (nearest neighbour)


def kappa(a, b):
    """Unweighted Cohen's kappa between two label arrays (all values present in either)."""
    vals = np.union1d(np.unique(a), np.unique(b))
    lut = np.zeros(256, dtype=np.int64)
    lut[vals] = np.arange(len(vals))
    k = len(vals)
    cm = np.bincount(lut[a].ravel() * k + lut[b].ravel(), minlength=k * k).reshape(k, k).astype(np.float64)
    n = cm.sum()
    po = np.trace(cm) / n
    pe = (cm.sum(0) * cm.sum(1)).sum() / n**2
    return float((po - pe) / (1 - pe)) if pe < 1 else float("nan")


def process_core(args):
    root, core_id = args
    root = Path(root)
    out = {"core_id": core_id, "maps": {}}
    img = Image.open(root / "TrainImgs" / f"{core_id}.jpg")
    out["img_size"] = img.size
    out["img_mode"] = img.mode
    small = img.reduce(DS_STATS)
    rgb = np.asarray(small, dtype=np.float32)
    hsv = np.asarray(small.convert("HSV"), dtype=np.float32)
    sat, val = hsv[..., 1], hsv[..., 2]
    glass = (sat < 20) & (val > 200)  # crude "white / glass" detector, for describing label values only

    agree_masks = {}
    for m in range(1, N_MAPS + 1):
        p = root / f"Map{m}" / f"{core_id}_classimg_nonconvex.png"
        if not p.exists():
            continue
        raw = p.read_bytes()
        mk = Image.open(p)
        info = {"size": mk.size, "mode": mk.mode, "file_md5": hashlib.md5(raw).hexdigest(),
                "png_info": {k: str(v) for k, v in mk.info.items()}}
        a = np.asarray(mk)
        if a.ndim == 3:
            info["is_multichannel"] = True
            info["channels_equal"] = bool(all((a[..., c] == a[..., 0]).all() for c in range(1, a.shape[2])))
            a = a[..., 0]
        info["array_md5"] = hashlib.md5(a.tobytes()).hexdigest()
        cnt = np.bincount(a.ravel(), minlength=256)
        info["value_counts"] = {int(v): int(c) for v, c in enumerate(cnt) if c}
        # appearance of each label value in the H&E image (downsampled)
        a_s = a[: rgb.shape[0] * DS_STATS : DS_STATS, : rgb.shape[1] * DS_STATS : DS_STATS]
        app = {}
        if a_s.shape == sat.shape:
            for v in info["value_counts"]:
                sel = a_s == v
                n = int(sel.sum())
                if n == 0:
                    continue
                app[v] = {"n": n, "sum_r": float(rgb[..., 0][sel].sum()), "sum_g": float(rgb[..., 1][sel].sum()),
                          "sum_b": float(rgb[..., 2][sel].sum()), "sum_sat": float(sat[sel].sum()),
                          "n_glass": int(glass[sel].sum())}
        info["appearance"] = app
        out["maps"][m] = info
        agree_masks[m] = a[::DS_AGREE, ::DS_AGREE]

    # pairwise kappa between maps on this core
    ms = sorted(agree_masks)
    pk = {}
    for i, mi in enumerate(ms):
        for mj in ms[i + 1:]:
            if agree_masks[mi].shape == agree_masks[mj].shape:
                pk[f"{mi}-{mj}"] = kappa(agree_masks[mi], agree_masks[mj])
    out["pairwise_kappa"] = pk
    # leave-one-out: each map vs pixelwise mode of the other maps (ties -> smallest value)
    loo = {}
    for m in ms:
        others = [agree_masks[o] for o in ms if o != m and agree_masks[o].shape == agree_masks[m].shape]
        if len(others) < 2:
            continue
        st = np.stack(others)
        counts = np.stack([(st == v).sum(0) for v in range(7)])
        mode = counts.argmax(0).astype(np.uint8)
        a = agree_masks[m]
        cancer = np.isin(a, [3, 4, 5])
        oc = np.isin(mode, [3, 4, 5])
        loo[m] = {"kappa_vs_others_mode": kappa(a, mode),
                  "frac_cancer_self": float(cancer.mean()), "frac_cancer_others": float(oc.mean()),
                  "mean_grade_self": float(a[cancer].mean()) if cancer.any() else None,
                  "mean_grade_others": float(mode[oc].mean()) if oc.any() else None}
    out["loo"] = loo
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="data/gleason")
    ap.add_argument("--out", default="results/phase0_inspect")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    root, out = Path(args.root), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    summary = {}

    # ---- 1. file listing / naming --------------------------------------------------------
    listing = {"TrainImgs": sorted(p.name for p in (root / "TrainImgs").iterdir())}
    for m in range(1, N_MAPS + 1):
        listing[f"Map{m}"] = sorted(p.name for p in (root / f"Map{m}").iterdir())
    bad_names = {k: [n for n in v if not (IMG_RE if k == "TrainImgs" else MASK_RE).match(n)]
                 for k, v in listing.items()}
    summary["n_files"] = {k: len(v) for k, v in listing.items()}
    summary["nonconforming_names"] = bad_names
    img_cores = {IMG_RE.match(n).group(0)[:-4] for n in listing["TrainImgs"] if IMG_RE.match(n)}
    map_cores = {}
    for m in range(1, N_MAPS + 1):
        map_cores[m] = {n.replace("_classimg_nonconvex.png", "") for n in listing[f"Map{m}"] if MASK_RE.match(n)}
    summary["mask_cores_without_image"] = {m: sorted(map_cores[m] - img_cores) for m in map_cores}
    rows = []
    for c in sorted(img_cores):
        s, k = IMG_RE.match(c + ".jpg").groups()
        rows.append({"core_id": c, "slide": f"slide{s}", "core_num": int(k),
                     **{f"map{m}": int(c in map_cores[m]) for m in map_cores}})
    cores = pd.DataFrame(rows)
    cores["n_readers"] = cores[[f"map{m}" for m in map_cores]].sum(1)
    cores.to_csv(out / "cores.csv", index=False)

    # ---- 2. zip timestamps (per-map annotation sessions) ---------------------------------
    ts_rows = []
    for m in range(1, N_MAPS + 1):
        z = root / f"Maps{m}_T.zip"
        if z.exists():
            with zipfile.ZipFile(z) as zf:
                for zi in zf.infolist():
                    ts_rows.append({"map": m, "name": zi.filename, "datetime": "%04d-%02d-%02d %02d:%02d:%02d" % zi.date_time,
                                    "size": zi.file_size})
    pd.DataFrame(ts_rows).to_csv(out / "zip_timestamps.csv", index=False)

    # ---- 3. per-core image + mask analysis -----------------------------------------------
    with ProcessPoolExecutor(args.workers) as ex:
        results = list(ex.map(process_core, [(str(root), c) for c in sorted(img_cores)], chunksize=2))

    img_rows, mv_rows, app_acc, pk_rows, loo_rows, meta_rows = [], [], defaultdict(lambda: defaultdict(float)), [], [], []
    for r in results:
        img_rows.append({"core_id": r["core_id"], "width": r["img_size"][0], "height": r["img_size"][1], "mode": r["img_mode"]})
        for m, info in r["maps"].items():
            meta_rows.append({"core_id": r["core_id"], "map": m, "width": info["size"][0], "height": info["size"][1],
                              "mode": info["mode"], "file_md5": info["file_md5"], "array_md5": info["array_md5"],
                              "size_matches_image": tuple(info["size"]) == tuple(r["img_size"]),
                              "png_info": json.dumps(info["png_info"]),
                              "multichannel": info.get("is_multichannel", False)})
            tot = sum(info["value_counts"].values())
            for v, c in info["value_counts"].items():
                mv_rows.append({"core_id": r["core_id"], "map": m, "value": v, "pixels": c, "frac": c / tot})
            for v, a in info["appearance"].items():
                for k, x in a.items():
                    app_acc[(m, v)][k] += x
        for pair, k in r["pairwise_kappa"].items():
            mi, mj = map(int, pair.split("-"))
            pk_rows.append({"core_id": r["core_id"], "map_i": mi, "map_j": mj, "kappa": k})
        for m, d in r["loo"].items():
            loo_rows.append({"core_id": r["core_id"], "map": m, **d})

    imgs = pd.DataFrame(img_rows)
    imgs.to_csv(out / "images.csv", index=False)
    meta = pd.DataFrame(meta_rows)
    meta.to_csv(out / "mask_meta.csv", index=False)
    mv = pd.DataFrame(mv_rows)
    mv.to_csv(out / "mask_values.csv", index=False)
    app = pd.DataFrame([{"map": m, "value": v, "n_px_ds": a["n"],
                         "mean_R": a["sum_r"] / a["n"], "mean_G": a["sum_g"] / a["n"], "mean_B": a["sum_b"] / a["n"],
                         "mean_sat": a["sum_sat"] / a["n"], "frac_glass": a["n_glass"] / a["n"]}
                        for (m, v), a in sorted(app_acc.items())])
    app.to_csv(out / "value_appearance.csv", index=False)
    pk = pd.DataFrame(pk_rows)
    pk = pk.merge(cores[["core_id", "slide"]], on="core_id")
    pk.to_csv(out / "pairwise_kappa.csv", index=False)
    loo = pd.DataFrame(loo_rows).merge(cores[["core_id", "slide"]], on="core_id")
    loo.to_csv(out / "loo_agreement.csv", index=False)

    # duplicate-mask check: identical arrays across different maps of the same core / across cores
    dup_same_core = meta.groupby(["core_id", "array_md5"]).filter(lambda g: len(g) > 1)
    dup_any = meta.groupby("array_md5").filter(lambda g: len(g) > 1)
    dup_same_core.to_csv(out / "duplicate_masks_same_core.csv", index=False)
    dup_any.to_csv(out / "duplicate_masks_any.csv", index=False)

    summary["image_sizes"] = imgs.groupby(["width", "height", "mode"]).size().reset_index(name="n").to_dict("records")
    summary["mask_sizes"] = meta.groupby(["map", "width", "height", "mode"]).size().reset_index(name="n").to_dict("records")
    summary["mask_size_mismatch"] = meta.loc[~meta.size_matches_image, ["core_id", "map", "width", "height"]].to_dict("records")
    summary["n_dup_same_core"] = int(len(dup_same_core))
    summary["n_dup_any"] = int(len(dup_any))
    with open(out / "phase0_summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
