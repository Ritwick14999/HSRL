"""Phase 1a: tile Gleason2019 cores, build tissue masks, count each reader's classes per tile,
and save every tissue tile as a resized patch.

For every tile size T this writes
  <out_root>/p{T}/tiles_raw.csv   one row per tissue tile (>= min_tissue_frac), with per-reader
                                  class pixel counts over tissue pixels: r{k}_n{c}, c in CLASS_NAMES
  <out_root>/p{T}/images/<core_id>/<patch_id>.png
and, once, <out_root>/core_readers.csv, pixel_confusion.csv, extract_config.yaml.

Labels are NOT decided here (see data/gleason_labels.py), so labelling rules can change without
re-reading images.

Usage:  python -I data/gleason_extract.py --config configs/data/gleason_extract.yaml
"""
import argparse
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

# raw mask value -> class index. 0 unannotated, 1 and 6 benign (merged), 3/4/5 Gleason patterns.
CLASS_NAMES = ["unann", "benign", "g3", "g4", "g5"]
LUT = np.full(256, 255, dtype=np.uint8)
LUT[[0, 1, 6, 3, 4, 5]] = [0, 1, 1, 2, 3, 4]
NOT_TISSUE = 5


def otsu_threshold(x):
    hist = np.bincount(x.ravel(), minlength=256).astype(np.float64)
    p = hist / hist.sum()
    omega = np.cumsum(p)
    mu = np.cumsum(p * np.arange(256))
    with np.errstate(divide="ignore", invalid="ignore"):
        sigma_b = (mu[-1] * omega - mu) ** 2 / (omega * (1 - omega))
    return int(np.nanargmax(sigma_b))


def tile_view(a, T, oy, ox, nh, nw):
    return a[oy:oy + nh * T, ox:ox + nw * T].reshape(nh, T, nw, T)


def process_core(job):
    core_id, cfg = job
    raw = Path(cfg["raw_root"])
    out_root = Path(cfg["out_root"])
    R = cfg["n_readers"]
    tcfg = cfg["tissue"]

    img = Image.open(raw / "TrainImgs" / f"{core_id}.jpg").convert("RGB")
    W, H = img.size
    sat = np.asarray(img.convert("HSV"))[..., 1]
    if tcfg["method"] == "otsu":
        thr = otsu_threshold(sat[:: tcfg["otsu_downsample"], :: tcfg["otsu_downsample"]])
    else:
        thr = int(tcfg["fixed_threshold"])
    tissue = sat > thr
    del sat

    # reader masks -> class index, non-tissue set to NOT_TISSUE. Entirely-zero masks = not annotated.
    cls, core_info = {}, {"core_id": core_id, "slide": core_id[:8], "width": W, "height": H,
                          "otsu_thr": thr, "tissue_frac": float(tissue.mean())}
    for k in range(1, R + 1):
        p = raw / f"Map{k}" / f"{core_id}_classimg_nonconvex.png"
        status = "missing"
        if p.exists():
            m = np.asarray(Image.open(p))
            assert m.shape == tissue.shape, (core_id, k, m.shape)
            if not m.any():
                status = "empty"
            else:
                c = LUT[m]
                assert (c != 255).all(), f"unexpected mask value in {p}"
                c[~tissue] = NOT_TISSUE
                cls[k] = c
                status = "annotated"
        core_info[f"r{k}"] = status

    # pixel-level confusion between reader pairs: tissue pixels where both readers are non-zero
    s = cfg["agreement_downsample"]
    conf_rows = []
    ks = sorted(cls)
    for i, a in enumerate(ks):
        ca = cls[a][::s, ::s]
        for b in ks[i + 1:]:
            cb = cls[b][::s, ::s]
            sel = (ca >= 1) & (ca <= 4) & (cb >= 1) & (cb <= 4)
            cm = np.bincount((ca[sel] - 1).astype(np.int64) * 4 + (cb[sel] - 1), minlength=16)
            conf_rows.append({"core_id": core_id, "reader_a": a, "reader_b": b,
                              **{f"c{x}{y}": int(cm[x * 4 + y]) for x in range(4) for y in range(4)}})

    tile_rows = {}
    for T in cfg["tile_sizes"]:
        nh, nw = H // T, W // T
        oy, ox = (H - nh * T) // 2, (W - nw * T) // 2
        tfrac = tile_view(tissue, T, oy, ox, nh, nw).mean((1, 3))
        tpx = tile_view(tissue, T, oy, ox, nh, nw).sum((1, 3))
        counts = {k: np.stack([(tile_view(cls[k], T, oy, ox, nh, nw) == c).sum((1, 3))
                               for c in range(len(CLASS_NAMES))]) for k in ks}
        img_dir = out_root / f"p{T}" / "images" / core_id
        img_dir.mkdir(parents=True, exist_ok=True)
        rows = []
        for r in range(nh):
            for c in range(nw):
                if tfrac[r, c] < tcfg["min_tissue_frac"]:
                    continue
                y0, x0 = oy + r * T, ox + c * T
                pid = f"{core_id}_p{T}_r{r:02d}_c{c:02d}"
                path = img_dir / f"{pid}.png"
                img.crop((x0, y0, x0 + T, y0 + T)).resize(
                    (cfg["patch_out_size"], cfg["patch_out_size"]), Image.LANCZOS).save(path)
                row = {"patch_id": pid, "core_id": core_id, "slide": core_id[:8], "tile_size": T,
                       "row": r, "col": c, "y0": y0, "x0": x0, "tissue_frac": float(tfrac[r, c]),
                       "tissue_px": int(tpx[r, c]), "path": path.relative_to(out_root).as_posix()}
                for k in range(1, R + 1):
                    row[f"r{k}_status"] = core_info[f"r{k}"]
                    for ci, name in enumerate(CLASS_NAMES):
                        row[f"r{k}_n_{name}"] = int(counts[k][ci, r, c]) if k in counts else -1
                rows.append(row)
        tile_rows[T] = rows
    return core_info, conf_rows, tile_rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/data/gleason_extract.yaml")
    ap.add_argument("--limit", type=int, default=0, help="process only the first N cores (debug)")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    out_root = Path(cfg["out_root"])
    out_root.mkdir(parents=True, exist_ok=True)
    with open(out_root / "extract_config.yaml", "w") as f:
        yaml.safe_dump(cfg, f, sort_keys=False)

    cores = sorted(p.stem for p in (Path(cfg["raw_root"]) / "TrainImgs").glob("*.jpg"))
    if args.limit:
        cores = cores[: args.limit]
    t0 = time.time()
    core_infos, conf_rows, tiles = [], [], {T: [] for T in cfg["tile_sizes"]}
    with ProcessPoolExecutor(cfg["workers"]) as ex:
        for i, (ci, cr, tr) in enumerate(ex.map(process_core, [(c, cfg) for c in cores])):
            core_infos.append(ci)
            conf_rows += cr
            for T in tr:
                tiles[T] += tr[T]
            if (i + 1) % 20 == 0:
                print(f"{i + 1}/{len(cores)} cores, {time.time() - t0:.0f}s", flush=True)

    pd.DataFrame(core_infos).to_csv(out_root / "core_readers.csv", index=False)
    pd.DataFrame(conf_rows).to_csv(out_root / "pixel_confusion.csv", index=False)
    for T, rows in tiles.items():
        pd.DataFrame(rows).to_csv(out_root / f"p{T}" / "tiles_raw.csv", index=False)
        print(f"tile {T}: {len(rows)} tissue tiles")
    print(f"done in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
