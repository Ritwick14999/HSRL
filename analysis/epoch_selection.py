"""How much would choosing the epoch on the TEST set inflate a result? (D41, diagnostic only.)

Reads epoch_eval.csv (val and test metrics after every epoch, logged with eval.per_epoch_test=true; never used in
training) and compares, per run:
  final        the model at the end of training (what every other table reports)
  best_val     the epoch with the highest validation accuracy (a legitimate selection rule)
  best_test    the epoch with the highest test accuracy (an optimistic, invalid rule)
For HSRL runs all Stage II and Stage III epochs are candidates; the final model is the last Stage III epoch.

Usage: python -I analysis/epoch_selection.py --root results/mhist_protocol --out results/mhist_protocol_summary
"""
import argparse
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aggregate_runs import md_table, pm  # noqa: E402

NAME = re.compile(r"^f(\d+)s(\d+)_(.+)$")
METRICS = ("acc", "macro_f1", "bal_acc")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="results/mhist_protocol")
    ap.add_argument("--out", default="results/mhist_protocol_summary")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for d in sorted(Path(args.root).iterdir()):
        m = NAME.match(d.name)
        if not m or not (d / "epoch_eval.csv").exists() or not (d / "metrics.json").exists():
            continue
        e = pd.read_csv(d / "epoch_eval.csv").reset_index(drop=True)
        final = e.iloc[-1]
        bv = e.iloc[e.val_acc[::-1].idxmax()]          # ties -> latest epoch
        bt = e.iloc[e.test_acc[::-1].idxmax()]
        r = {"run": d.name, "fold": int(m[1]), "seed": int(m[2]), "cfg": m[3], "n_epochs": len(e),
             "best_test_epoch": f"{bt.stage}:{int(bt.epoch)}", "best_val_epoch": f"{bv.stage}:{int(bv.epoch)}"}
        for k in METRICS:
            r[f"final_{k}"] = final[f"test_{k}"]
            r[f"best_val_{k}"] = bv[f"test_{k}"]
            r[f"best_test_{k}"] = bt[f"test_{k}"]
            r[f"inflation_{k}"] = bt[f"test_{k}"] - final[f"test_{k}"]
        rows.append(r)
    R = pd.DataFrame(rows)
    R.to_csv(out / "epoch_selection_per_run.csv", index=False)
    cols = [f"{p}_{k}" for k in ("acc", "macro_f1") for p in ("final", "best_val", "best_test", "inflation")]
    summ = [{"config": c, "runs": len(g), **{k: pm(100 * g[k]) for k in cols}} for c, g in R.groupby("cfg", sort=False)]
    md = ["# Epoch selection on MHIST (diagnostic, D41)\n",
          "Test metrics in % (mean ± std over draws). final = end of training; best_val = epoch with the highest validation "
          "accuracy; best_test = epoch with the highest TEST accuracy (invalid selection, shown only to measure the "
          "possible inflation); inflation = best_test − final.\n",
          md_table(pd.DataFrame(summ)) + "\n", "## Per run\n", md_table(R.round(4)) + "\n"]
    (out / "epoch_selection.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
