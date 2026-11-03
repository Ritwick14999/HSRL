"""Step 1 of the extension plan: does the joint four-image formulation (plan §4) change anything on real tuples?

No training. For each HSRL run, the labelled images are embedded with the end-of-Stage-I model (model_stage1.pt)
and two tuple sets are examined: the tuples HSRL actually mined in the last Stage I epoch, and random role-valid
tuples (as in the census). Only votes of labelled training images are used (LEAKAGE RULE; analysis only).

Notation (plan §4). Tuple (a, p, n, c); pairs ap, an, ac, pn, pc, nc. t_ij = 1 - d_ij / 4, d = squared Euclidean
distance between the normalised embeddings. One reader's decisions on the four images form a pattern b in {0,1}^4
(1 = SSA / G4); e_ij(b) = 1 if the pattern gives i and j the same class. v(b) = number of readers with pattern b, with
sum_b v(b) = R and sum_b v(b) b_i = k_i. Then s_ij = sum_b v(b) e_ij(b) / R and, with C(b) = (1/6) sum (t_ij - e_ij(b))^2,

    L_joint = max_v (1/R) sum_b v(b) C(b) = (1/6) sum_ij t_ij^2 + (1/6) max_v sum_ij s_ij(v) (1 - 2 t_ij)
    L_ind   = (1/6) sum_ij max_{s in [L_ij, U_ij]} [t_ij^2 + s (1 - 2 t_ij)]        (each pair's worst case alone)

with the Fréchet bounds L_ij = |q_i + q_j - 1|, U_ij = 1 - |q_i - q_j|. L_joint <= L_ind always (checked on every
tuple). gap = L_ind - L_joint > 0 means the six pairwise worst cases cannot hold together for any reader allocation;
the gradient dL/dt_ij = (t_ij - s*_ij) / 3 then differs as well.

Allocation models:
  exact  integer v, R = 7, k = SSA votes (MHIST only: the same 7 readers read every image)
  relax  fractional v with marginals q (the plan's LP relaxation; a common-population model). The only option on
         Gleason, where the readers differ between cores, so there it is a model, not a guaranteed bound.

Scope measure, independent of the embeddings: each pairwise worst case is a vertex of the box prod [L_ij, U_ij]
(every pair at L or U). Joint and independent coincide for every embedding whose signs of (1 - 2t) select a vertex
if and only if that vertex is jointly feasible. We count feasible vertices on a sample of tuples.

Usage:  python -I analysis/joint_check.py                       (5 MHIST + 15 Gleason HSRL runs, default)
        python -I analysis/joint_check.py --runs results/mhist/f0s0_hsrl --n-random 100 --n-scope 20 --out <dir>
"""
import argparse
import glob
import itertools
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
import torch
import yaml

from analysis.aggregate_runs import md_table
from analysis.tuple_census import embed_patches, load_labelled, random_tuples
from hsrl.agreement import A_MARG, E, PAIR_NAMES, PAIRS, solve_allocation as _solve
from hsrl.agreement import joint_worst_case as joint_max, tuple_bounds as bounds

DEFAULT_RUNS = ["results/mhist/f*s*_hsrl", "results/main/f*s*_hsrl"]
ROLE_COLS = ("anchor_id", "pos_id", "neg_id", "conf_id")
# Reading fixed in advance (ASSUMPTIONS D44): primary = MHIST, mined tuples, exact counts, mean over the 5 draws.
CRIT_PCT_GAP, CRIT_REL_GAP = 10.0, 0.05


_scope_cache = {}


def vertex_scope(m, total, integer):
    """(distinct box vertices, jointly feasible ones) for marginals m. Does not depend on the order of the images."""
    key = (integer, float(total), tuple(sorted(np.round(np.asarray(m, float), 9))))
    if key in _scope_cache:
        return _scope_cache[key]
    ms = np.array(key[2])
    L, U = bounds(ms, total)
    free = np.flatnonzero(U - L > 1e-9)
    A = np.vstack([A_MARG, E.T])
    n_ok = 0
    for choice in itertools.product((False, True), repeat=len(free)):
        target = L.copy()
        target[free[list(choice)]] = U[free[list(choice)]]
        r = _solve(np.zeros(16), A, np.concatenate([[total], ms, target]), total, integer)
        if r.status not in (0, 2):
            raise RuntimeError(f"feasibility check failed (status {r.status}) for {ms}, {target}")
        n_ok += r.status == 0
    _scope_cache[key] = (2 ** len(free), n_ok)
    return _scope_cache[key]


def tuple_rows(T, z, k, q, models, scope_idx, ids):
    rows = []
    for row_i, idx in enumerate(T):
        idx = list(idx)
        zz = z[idx]
        t = np.array([1.0 - ((zz[i] - zz[j]) ** 2).sum() / 4.0 for i, j in PAIRS])
        w = 1.0 - 2.0 * t
        base = float((t ** 2).sum())
        row = {"anchor_id": ids[idx[0]], "pos_id": ids[idx[1]], "neg_id": ids[idx[2]], "conf_id": ids[idx[3]],
               "n_split": int(((q[idx] > 0) & (q[idx] < 1)).sum()),
               **{f"q_{r}": float(q[i]) for r, i in zip("apnc", idx)}, **{f"t_{p}": t[j] for j, p in enumerate(PAIR_NAMES)}}
        for model in models:
            m, total, integer = (k[idx], 7.0, True) if model == "exact" else (q[idx], 1.0, False)
            L, U = bounds(m, total)
            s_ind = np.where(w > 0, U, L) / total
            v_ind = float(w @ s_ind)
            v_joint, s_joint = joint_max(w, m, total, integer)
            gap = (v_ind - v_joint) / 6.0
            if gap < -1e-7:
                raise AssertionError(f"joint worst case above the independent one ({gap:.2e}): {ids[idx[0]]}")
            L_ind, L_joint = (base + v_ind) / 6.0, (base + v_joint) / 6.0
            g_ind, g_joint = (t - s_ind) / 3.0, (t - s_joint) / 3.0
            cos = float(g_ind @ g_joint / (np.linalg.norm(g_ind) * np.linalg.norm(g_joint) + 1e-12))
            row.update({f"{model}_L_ind": L_ind, f"{model}_L_joint": L_joint, f"{model}_gap": max(gap, 0.0),
                        f"{model}_rel_gap": max(gap, 0.0) / max(L_ind, 1e-12), f"{model}_grad_cos": cos,
                        f"{model}_s_ind": " ".join(f"{v:.3f}" for v in s_ind),
                        f"{model}_s_joint": " ".join(f"{v:.3f}" for v in s_joint)})
            if row_i in scope_idx:
                nv, nf = vertex_scope(m, total, integer)
                row.update({f"{model}_n_vertices": nv, f"{model}_n_feasible": nf})
        rows.append(row)
    return pd.DataFrame(rows)


def summarise(df, models, tol):
    out = {"n_tuples": int(len(df)), "mean_t": {p: float(df[f"t_{p}"].mean()) for p in PAIR_NAMES}}
    for model in models:
        g, rg = df[f"{model}_gap"], df[f"{model}_rel_gap"]
        has = g > tol
        r = {"pct_gap": 100 * float(has.mean()), "mean_rel_gap": float(rg.mean()),
             "mean_rel_gap_given_gap": float(rg[has].mean()) if has.any() else 0.0,
             "p90_rel_gap": float(rg.quantile(0.9)),
             "mean_grad_cos_given_gap": float(df.loc[has, f"{model}_grad_cos"].mean()) if has.any() else float("nan"),
             "pct_gap_by_n_split": {int(s): 100 * float((d[f"{model}_gap"] > tol).mean())
                                    for s, d in df.groupby("n_split")},
             "n_by_n_split": {int(s): int(len(d)) for s, d in df.groupby("n_split")}}
        if f"{model}_n_vertices" in df:
            sc = df.dropna(subset=[f"{model}_n_vertices"])
            frac = sc[f"{model}_n_feasible"] / sc[f"{model}_n_vertices"]
            r.update({"n_scope": int(len(sc)), "pct_all_vertices_feasible": 100 * float((frac == 1).mean()),
                      "mean_frac_vertices_feasible": float(frac.mean())})
        out[model] = r
    if "exact" in models and "relax" in models:
        diff = df["relax_L_joint"] - df["exact_L_joint"]
        if (diff < -1e-7).any():
            raise AssertionError("relaxation below the exact joint worst case")
        out["relax_vs_exact"] = {"pct_relax_above_exact": 100 * float((diff > tol).mean()),
                                 "mean_rel_diff": float((diff / df["exact_L_joint"]).mean())}
    return out


def analyse_run(run_dir, args, device, out_root):
    cfg = yaml.safe_load(open(run_dir / "config.yaml"))
    dataset = cfg["data"].get("dataset", "gleason")
    lab, _, q_csv, y = load_labelled(cfg)
    k, R = lab.votes_g4.to_numpy(float), lab.n_readers.to_numpy(float)
    q = k / R                                       # exact fractions (the csv rounds q to 6 decimals)
    if not np.allclose(q, q_csv, atol=1e-5):
        raise ValueError(f"{run_dir}: q differs from votes_g4 / n_readers")
    models = ("exact", "relax") if dataset == "mhist" else ("relax",)
    if dataset == "mhist" and not (R == 7).all():
        raise ValueError(f"{run_dir}: MHIST image without 7 readers")
    ids = lab.patch_id.to_numpy()
    pos = {pid: i for i, pid in enumerate(ids)}
    log = pd.read_csv(run_dir / "tuples_stage1.csv")
    last = log[log.epoch == log.epoch.max()]
    for c in ROLE_COLS:   # leakage guard: every tuple member must be a labelled training image
        if not last[c].isin(pos).all():
            raise ValueError(f"{run_dir}: {c} outside the labelled set")
    rng = np.random.default_rng([args.seed, int(cfg["data"]["fold"]), int(cfg.get("seed", 0))])
    rt = random_tuples(y, args.n_random, rng)
    sets = {"mined_last_epoch": np.column_stack([last[c].map(pos).to_numpy() for c in ROLE_COLS]),
            "random": np.column_stack([rt[r] for r in "apnc"])}
    z = embed_patches(run_dir, cfg, lab, device).numpy().astype(np.float64)
    od = out_root / dataset / run_dir.name
    od.mkdir(parents=True, exist_ok=True)
    summ = {"run": str(run_dir), "dataset": dataset, "n_labelled": int(len(lab)), "models": list(models),
            "stage1_epoch_used": int(last.epoch.iloc[0]), "sets": {}}
    for name, T in sets.items():
        scope_idx = set(rng.choice(len(T), size=min(args.n_scope, len(T)), replace=False).tolist())
        df = tuple_rows(T, z, k, q, models, scope_idx, ids)
        df.to_csv(od / f"tuples_{name}.csv", index=False)
        summ["sets"][name] = summarise(df, models, args.tol)
    with open(od / "summary.json", "w") as f:
        json.dump(summ, f, indent=2)
    return summ


def flat_rows(summaries):
    rows = []
    for s in summaries:
        for name, st in s["sets"].items():
            for model in s["models"]:
                r = {"dataset": s["dataset"], "run": Path(s["run"]).name, "set": name, "model": model,
                     "n_tuples": st["n_tuples"]}
                r.update({k: v for k, v in st[model].items() if not isinstance(v, dict)})
                if "relax_vs_exact" in st and model == "exact":
                    r.update(st["relax_vs_exact"])
                rows.append(r)
    return pd.DataFrame(rows)


def write_report(per_run, summaries, out_root, args):
    metrics = ["pct_gap", "mean_rel_gap_given_gap", "p90_rel_gap", "mean_grad_cos_given_gap",
               "pct_all_vertices_feasible", "mean_frac_vertices_feasible"]
    lines = ["# Step 1: does the joint four-image loss differ from the independent pairwise worst case?\n",
             f"No training. End-of-Stage-I embeddings of each HSRL run; votes of labelled training images only. "
             f"gap > {args.tol:g} counts as a difference. 'vertices' = the 2^m pairwise worst cases (m = pairs with L < U); "
             "'all vertices feasible' means joint = independent for every possible embedding. Mean ± std over runs.\n",
             "## Per dataset, tuple set and allocation model\n",
             "| dataset | set | model | runs | tuples/run | " + " | ".join(metrics) + " |",
             "|---" * (5 + len(metrics)) + "|"]
    for (ds, st, mo), g in per_run.groupby(["dataset", "set", "model"], sort=False):
        cells = [f"{g[m].mean():.3f} ± {g[m].std(ddof=0):.3f}" if m in g and g[m].notna().any() else "–" for m in metrics]
        lines.append(f"| {ds} | {st} | {mo} | {len(g)} | {g.n_tuples.mean():.0f} | " + " | ".join(cells) + " |")
    if "pct_relax_above_exact" in per_run:
        ex = per_run[(per_run.model == "exact")].groupby("set")[["pct_relax_above_exact", "mean_rel_diff"]].mean()
        lines += ["\n## MHIST: exact integer counts vs LP relaxation\n", md_table(ex.reset_index(), 4)]
    lines.append("\n## Share of tuples with a gap, by number of split-vote images in the tuple (pooled over runs)\n")
    for s in ("mined_last_epoch", "random"):
        rows = []
        for sm in summaries:
            for model in sm["models"]:
                d = sm["sets"][s][model]
                for n_split, pct in d["pct_gap_by_n_split"].items():
                    rows.append({"dataset": sm["dataset"], "model": model, "n_split": int(n_split),
                                 "n": d["n_by_n_split"][n_split], "with_gap": pct / 100 * d["n_by_n_split"][n_split]})
        t = pd.DataFrame(rows).groupby(["dataset", "model", "n_split"]).sum()
        t["pct_gap"] = (100 * t.with_gap / t.n).round(1)
        lines += [f"\n### {s}\n", md_table(t[["n", "pct_gap"]].reset_index(), 1)]
    mh = [sm for sm in summaries if sm["dataset"] == "mhist"]
    if mh:
        ex = []
        for sm in mh:
            df = pd.read_csv(out_root / "mhist" / Path(sm["run"]).name / "tuples_mined_last_epoch.csv")
            ex.append(df.assign(run=Path(sm["run"]).name))
        ex = pd.concat(ex).sort_values("exact_gap", ascending=False).head(3)
        cols = ["run", "q_a", "q_p", "q_n", "q_c"] + [f"t_{p}" for p in PAIR_NAMES] + \
               ["exact_s_ind", "exact_s_joint", "exact_L_ind", "exact_L_joint", "exact_rel_gap"]
        lines += ["\n## Largest gaps, MHIST mined tuples, exact counts (pairs in order ap an ac pn pc nc)\n",
                  md_table(ex[cols], 3)]
        prim = per_run[(per_run.dataset == "mhist") & (per_run.set == "mined_last_epoch") & (per_run.model == "exact")]
        pg, rg = prim.pct_gap.mean(), prim.mean_rel_gap_given_gap.mean()
        met = bool(pg >= CRIT_PCT_GAP and rg >= CRIT_REL_GAP)
        lines += ["\n## Reading fixed in advance (ASSUMPTIONS D44)\n",
                  f"Primary: MHIST, mined tuples, exact counts, mean over {len(prim)} draws. The joint loss has something "
                  f"to act on if the joint worst case is below the independent one in >= {CRIT_PCT_GAP:g}% of tuples AND "
                  f"those gaps average >= {100 * CRIT_REL_GAP:g}% of the loss.\n",
                  f"- tuples with a gap: {pg:.1f}% · mean relative gap where there is one: {100 * rg:.1f}%",
                  f"- **criterion met: {met}**"]
    (out_root / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", nargs="+", default=DEFAULT_RUNS, help="run folders or glob patterns")
    ap.add_argument("--out", default="results/joint_check")
    ap.add_argument("--n-random", type=int, default=1000)
    ap.add_argument("--n-scope", type=int, default=200, help="tuples per set for the embedding-free vertex count")
    ap.add_argument("--tol", type=float, default=1e-6)
    ap.add_argument("--seed", type=int, default=20261101)
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):   # the report contains ± and · (Windows consoles default to cp1252)
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    runs = sorted({Path(p) for pat in args.runs for p in (glob.glob(pat) or [pat])})
    runs = [r for r in runs if (r / "model_stage1.pt").exists() and (r / "tuples_stage1.csv").exists()]
    if not runs:
        raise SystemExit("no HSRL run with model_stage1.pt and tuples_stage1.csv found")
    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)
    with open(out_root / "config.json", "w") as f:
        json.dump({**vars(args), "runs": [str(r) for r in runs], "criterion": {"pct_gap": CRIT_PCT_GAP,
                   "rel_gap": CRIT_REL_GAP}}, f, indent=2)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    summaries = []
    for i, r in enumerate(runs, 1):
        t0 = time.time()
        summaries.append(analyse_run(r, args, device, out_root))
        s = summaries[-1]["sets"]["mined_last_epoch"]
        m = summaries[-1]["models"][0]
        print(f"[{i}/{len(runs)}] {r}  mined: {s[m]['pct_gap']:.1f}% with a gap ({m})  ({time.time() - t0:.0f}s)",
              flush=True)
    per_run = flat_rows(summaries)
    per_run.to_csv(out_root / "per_run.csv", index=False)
    print(write_report(per_run, summaries, out_root, args))


if __name__ == "__main__":
    main()
