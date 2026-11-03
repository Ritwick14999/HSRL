"""Pre-registered readings of D46 (MHIST draws 5-9, HSRL rerun control) and D47 (certified gap as a margin).

Balanced accuracy on the official MHIST test set (Gleason: held-out folds), final model (after Stage III for HSRL
variants, end of training for supervised runs), paired on the same draw (Gleason: same fold and seed). A view with
missing runs is reported as incomplete, never judged.

Usage: python -I analysis/followup_check.py [--out results/followup_check]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analysis.aggregate_runs import md_table  # noqa: E402

MHIST_ROOTS = ["mhist", "mhist_ext", "mhist_d10", "mhist_margin", "mhist_rerun"]
D45 = ["supported", "supported_random", "supported_conf", "interval", "worstcase", "joint"]
MARGIN = ["supported_gap", "supported_gap_shuffled", "supported_similarity"]
COMPARISONS = [*[(c, "hsrl_soft") for c in D45 + MARGIN], ("supported", "supported_random"),
               ("supported", "supported_conf"), ("joint", "worstcase"), ("supported_gap", "supported"),
               ("supported_gap", "supported_gap_shuffled"), ("supported_similarity", "supported")]
SECONDARY = [("hsrl", "supervised"), ("hsrl_soft", "supervised_soft"), ("hsrl_soft_rerun", "hsrl_soft")]
VIEWS = [("draws 0-4 (5-draw verdict, rule 4/5)", range(5), 4), ("draws 5-9 (replication, rule 4/5)", range(5, 10), 4),
         ("draws 0-9 (primary, rule 8/10)", range(10), 8)]


def score(path):
    m = json.load(open(path))
    ev = m["eval_stage3"] if "eval_stage3" in m else m["eval_supervised"]
    return 100 * ev["test"]["overall"]["bal_acc"]


def find(roots, fold, seed, cfg):
    hits = [ROOT / "results" / r / f"f{fold}s{seed}_{cfg}" / "metrics.json" for r in roots]
    hits = [h for h in hits if h.exists()]
    assert len(hits) <= 1, f"run found twice: {hits}"
    return score(hits[0]) if hits else np.nan


def judge(d, need):
    """Mean difference, count positive, 95% t-interval and the pre-registered verdict (mean >= +1.0 and >= need)."""
    d = np.asarray(d, float)
    n = len(d)
    half = stats.t.ppf(0.975, n - 1) * d.std(ddof=1) / np.sqrt(n) if n > 1 else np.nan
    ok = d.mean() >= 1.0 and (d > 0).sum() >= need
    return {"mean": round(d.mean(), 2), "up": f"{int((d > 0).sum())}/{n}", "ci95": f"[{d.mean() - half:+.2f}, {d.mean() + half:+.2f}]",
            "pass": "PASS" if ok else "no"}


def mhist(out):
    cfgs = ["hsrl", "hsrl_soft", "supervised", "supervised_soft", "hsrl_soft_rerun", *D45, *MARGIN]
    t = pd.DataFrame({c: [find(MHIST_ROOTS, k, k, c) for k in range(10)] for c in cfgs}, index=pd.RangeIndex(10, name="draw"))
    t.round(2).to_csv(out / "mhist_per_draw.csv")
    md = ["## MHIST: balanced accuracy per draw (%)\n", md_table(t.reset_index(), floatfmt=1), ""]

    def section(title, pairs, views):
        rows = []
        for a, b in pairs:
            for name, draws, need in views:
                d = (t.loc[list(draws), a] - t.loc[list(draws), b]).dropna()
                if len(d) < len(draws):
                    rows.append({"comparison": f"{a} − {b}", "view": name, "mean": None, "up": f"incomplete ({len(d)}/{len(draws)})",
                                 "ci95": "", "pass": ""})
                else:
                    rows.append({"comparison": f"{a} − {b}", "view": name, **judge(d, need)})
        md.extend([f"## {title}\n", md_table(pd.DataFrame(rows)), ""])

    section("D45 / D47 comparisons (Δ balanced accuracy, points; pass = mean ≥ +1.0 and positive in the required draws)",
            COMPARISONS, VIEWS)
    section("Secondary (D46.4) and rerun noise", SECONDARY, [VIEWS[2]])

    # D46.3: is "gains only on HSRL's weak draws" more than rerun noise?
    need = ["hsrl_soft", "hsrl_soft_rerun", *D45]
    if t[need].notna().all().all():
        weak = t.hsrl_soft.nsmallest(5).index
        strong = t.index.difference(weak)
        mean6 = t[D45].mean(1)
        rows = []
        for name, idx in (("weak draws " + ", ".join(map(str, sorted(weak))), weak), ("other draws", strong)):
            rows.append({"draws": name, "six losses − hsrl_soft": round((mean6[idx] - t.hsrl_soft[idx]).mean(), 2),
                         "rerun − hsrl_soft": round((t.hsrl_soft_rerun[idx] - t.hsrl_soft[idx]).mean(), 2),
                         "six losses − rerun": round((mean6[idx] - t.hsrl_soft_rerun[idx]).mean(), 2)})
        stat = (mean6[weak] - t.hsrl_soft_rerun[weak]).mean()
        per_loss = {c: round((t[c][weak] - t.hsrl_soft_rerun[weak]).mean(), 2) for c in D45}
        md += ["## D46.3: weak-draw pattern vs an HSRL rerun\n", md_table(pd.DataFrame(rows)), "",
               f"Per loss, weak draws, loss − rerun: {per_loss}", "",
               f"**Reading:** six losses − rerun on the weak draws = {stat:+.2f} points (bar +1.0): "
               + ("the weak-draw gain is more than rerun noise." if stat >= 1.0 else
                  "the weak-draw gain is attributed to rerun noise (regression to the mean)."), ""]
    else:
        md += ["## D46.3: weak-draw pattern vs an HSRL rerun\n", "Incomplete: not all runs are finished.", ""]
    return md


def gleason(out):
    cols = {"hsrl_soft": ["soft"], "supported_linked": ["gleason_ext"], "supported_gap_linked": ["gleason_margin"]}
    rows = [{"fold": f, "seed": s, **{c: find(r, f, s, c) for c, r in cols.items()}} for f in range(3) for s in range(2)]
    t = pd.DataFrame(rows)
    t.round(2).to_csv(out / "gleason_margin_per_run.csv", index=False)
    md = ["## Gleason, linked votes: gap margin (D47.3)\n", md_table(t, floatfmt=1), ""]
    for a, b in (("supported_gap_linked", "supported_linked"), ("supported_gap_linked", "hsrl_soft")):
        d = t[a] - t[b]
        if d.isna().any():
            md.append(f"- {a} − {b}: incomplete ({d.notna().sum()}/6)")
            continue
        folds = (t.assign(d=d).groupby("fold").d.mean())
        ok = d.mean() >= 1.0 and (d > 0).sum() >= 5 and (folds > 0).all()
        md.append(f"- {a} − {b}: mean {d.mean():+.2f}, positive {(d > 0).sum()}/6, fold means "
                  + " / ".join(f"{v:+.2f}" for v in folds) + (" → PASS" if ok else " → no")
                  + (" (pre-registered test)" if b == "supported_linked" else " (reported alongside)"))
    return md + [""]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/followup_check")
    out = ROOT / ap.parse_args().out
    out.mkdir(parents=True, exist_ok=True)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    md = ["# D46 / D47 follow-up check\n", "Pre-registered in ASSUMPTIONS.md (D46, D47). Balanced accuracy in points, paired. "
          "CI = t-interval over draws (all draws share one test set, so it covers labelled-set and training variation only).\n"]
    md += mhist(out) + gleason(out)
    (out / "report.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
