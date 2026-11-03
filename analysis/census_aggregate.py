"""Aggregate the tuple census over the HSRL-original runs (results/main/f{fold}s{seed}_hsrl/census/).
Primary pseudo-label measure: core level. Patch level is secondary.

Usage: python -I analysis/census_aggregate.py [--root results/main] [--out results/census_summary]
"""
import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from aggregate_runs import md_table, pm  # noqa: E402

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="results/main")
    ap.add_argument("--cfg", default="hsrl", help="config whose runs are aggregated (run names f{fold}s{seed}_{cfg})")
    ap.add_argument("--out", default="results/census_summary")
    args = ap.parse_args()
    NAME = re.compile(rf"^f(\d+)s(\d+)_{re.escape(args.cfg)}$")
    sys.stdout.reconfigure(encoding="utf-8")
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    tabs, core, patch = [], [], []
    for d in sorted(Path(args.root).iterdir()):
        m = NAME.match(d.name)
        if not m or not (d / "census" / "census_v2.done").exists():
            continue
        fold, seed = int(m[1]), int(m[2])
        t = pd.read_csv(d / "census" / "census_table.csv").assign(run=d.name, fold=fold, seed=seed)
        t["set"] = t["set"].str.replace(r"B_mined_epoch(\d+)", lambda x: f"B_mined_epoch{x[1]}", regex=True)
        tabs.append(t)
        c = json.load(open(d / "census" / "census_summary.json"))["pseudo_label_concentration"]
        cl = c.get("core_level", {})
        if cl:
            core.append({"run": d.name, "fold": fold, "seed": seed, "n_cores": cl["n_cores"], "n_patches": cl["n_patches"],
                         **{f"{k}_{s}": cl[k][s] for k in ("viol_rate", "undecided_rate")
                            for s in ("spearman", "perm_p", "partial_spearman_ctrl_split_frac", "partial_perm_p")}})
        ks = [k for k in ("nbr_viol_rate", "nbr_undecided_rate") if k in c]   # MHIST: counts-only rate only
        if ks:
            patch.append({"run": d.name, "fold": fold, "seed": seed, "n_accepted": c["n_accepted_nontie"],
                          "n_wrong": c["n_wrong_confident"],
                          "err_unanimous": c["error_rate_unanimous"], "err_split": c["error_rate_split_vote"],
                          **{f"{k}_auroc{'' if s == '' else '_' + s}": (c[k]["auroc_predicting_wrong"] if s == "" else
                                                                         c[k][f"within_{s}"]["auroc_predicting_wrong"])
                             for k in ks for s in ("", "unanimous", "split_vote")}})
    T = pd.concat(tabs, ignore_index=True)
    T.to_csv(out / "census_all_runs.csv", index=False)
    md = [f"# Tuple census across folds ({args.cfg}, {T.run.nunique()} runs)\n",
          "Counts-only bounds assume a common reader panel (not strictly true for Gleason). Linked verdicts skip pairs with < 3 shared "
          "readers. Set A (random tuples) depends only on the fold's labelled set, so it is identical across seeds within a fold.\n"]
    cols = ["pct_certified", "pct_contradicted", "pct_undecided", "pct_supported", "pct_violated", "pct_tie",
            "pct_linked_violated_given_undecided", "pct_linked_violated_given_certified", "pct_linked_violated_given_contradicted"]
    A = T[(T["set"] == "A_random") & (T.seed == T.groupby("fold").seed.transform("min"))]
    md.append("## Set A: 100k random role-valid tuples, per fold (%)\n\n" +
              md_table(A[["fold", "term", "ordering"] + cols].round(1)) + "\n")
    rows = []
    for (s, term), g in T[T["set"] != "A_random"].groupby(["set", "term"]):
        rows.append({"set": s, "term": term, "runs": len(g), **{c: pm(g[c].dropna()) for c in cols},
                     "skipped_pct": pm(100 * g.n_linked_skipped / g.n_tuples)})
    md.append("## Set B: mined tuples (mean ± std over runs, %)\n\n" + md_table(pd.DataFrame(rows)) + "\n")
    if core:
        C = pd.DataFrame(core)
        C.to_csv(out / "core_level_all_runs.csv", index=False)
        md.append("## Pseudo-label errors vs tuple status: CORE LEVEL (primary)\n\nPer run: Spearman over cores (>= 5 accepted "
                  "non-tie pseudo-labels) between the core's pseudo-label error rate and the mean violation (or counts-undecided) "
                  "rate of its labelled patches. Partial = controlling for the core's split-vote share among accepted patches. "
                  "p = core-level permutation (5000).\n")
        summ = []
        for k in ("viol_rate", "undecided_rate"):
            for kind, rc, pc in (("raw", f"{k}_spearman", f"{k}_perm_p"),
                                 ("partial (ctrl split share)", f"{k}_partial_spearman_ctrl_split_frac", f"{k}_partial_perm_p")):
                row = {"rate": k, "correlation": kind, "all runs": pm(C[rc]), "runs p<0.05": f"{(C[pc] < 0.05).sum()}/{len(C)}"}
                for f, g in C.groupby("fold"):
                    row[f"fold {f}"] = pm(g[rc])
                summ.append(row)
        md.append(md_table(pd.DataFrame(summ)) + "\n\nPer run:\n\n" + md_table(C.round(3)) + "\n")
    if patch:
        Pt = pd.DataFrame(patch)
        Pt.to_csv(out / "patch_level_all_runs.csv", index=False)
        summ = [{"measure": c, "all runs": pm(Pt[c]), **{f"fold {f}": pm(g[c]) for f, g in Pt.groupby("fold")}}
                for c in Pt.columns if c not in ("run", "fold", "seed")]
        md.append("## Pseudo-label errors vs tuple status: PATCH LEVEL (secondary)\n\nAUROC of the mean violation / undecided rate "
                  "of the 5 nearest labelled patches (Stage I embedding) for predicting a wrong accepted pseudo-label; overall and "
                  "within unanimous / split-vote patches. Patch-level p-values are optimistic (patches within a core are "
                  "correlated) and are not aggregated here.\n\n" + md_table(pd.DataFrame(summ)) + "\n")
    (out / "report.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
