"""Audit of everything run so far (pre-meeting check). Writes results/audit/audit_report.md.

Checks
 1. Completeness: every expected run has metrics.json; no NaN in the headline metrics.
 2. Recomputation: for a random sample of runs, balanced accuracy and Brier recomputed from the saved test
    predictions and the label set must match metrics.json.
 3. Headline numbers recomputed directly from metrics.json (independent of analysis/aggregate_runs.py).
 4. Split integrity for every label set used (no core in two splits, test slides disjoint, labelled only from train).
 5. Leakage: hidden-label access (eval_labels) appears only in evaluation code paths.
 6. Stage I reuse: every reused run points at the hard-target twin with the same fold, seed and schedule.
 7. Pilot criterion recomputed independently from per_run.csv.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "data"))

import numpy as np
import pandas as pd
import yaml

sys.stdout.reconfigure(encoding="utf-8")
NAME = re.compile(r"^f(\d)s(\d)_(.+)$")
EXPECTED = {
    "main": ["supervised", "hsrl", "hsrl_no_t2", "hsrl_no_stage1"],
    "deviations": ["hsrl_s1e60", "hsrl_no_t2_s1e60", "supervised_e65"],
    "soft": ["supervised_soft", "supervised_soft_e65", "hsrl_soft", "hsrl_soft_s1e60"],
    "excl_r1": ["supervised", "supervised_soft", "hsrl", "hsrl_soft"],
    "excl_r4": ["supervised", "supervised_soft", "hsrl", "hsrl_soft"],
    "p1024": ["supervised", "hsrl", "hsrl_no_t2", "hsrl_no_stage1"],
}
out_lines = ["# Audit report\n"]


def say(s=""):
    print(s)
    out_lines.append(s)


def final_eval(m):
    return m.get("eval_stage3") or m.get("eval_supervised")


# 1. completeness ----------------------------------------------------------------------------------------------
say("## 1. Completeness")
problems = 0
for root, cfgs in EXPECTED.items():
    for c in cfgs:
        n = 0
        for f in range(3):
            for s in range(5):
                p = ROOT / "results" / root / f"f{f}s{s}_{c}" / "metrics.json"
                if not p.exists():
                    say(f"- MISSING {root}/f{f}s{s}_{c}")
                    problems += 1
                    continue
                ev = final_eval(json.load(open(p)))
                if ev is None or any(np.isnan(ev["test"]["overall"][k]) for k in ("acc", "bal_acc", "brier", "auroc")):
                    say(f"- NaN/absent metrics {root}/f{f}s{s}_{c}")
                    problems += 1
                n += 1
        say(f"- {root}/{c}: {n}/15 complete")
dev3 = [ROOT / "results/deviations" / f"f0s{s}_hsrl_boundary" / "metrics.json" for s in range(3)]
say(f"- deviations/hsrl_boundary (fold 0): {sum(p.exists() for p in dev3)}/3 complete")
say(f"**Completeness problems: {problems}**\n")

# 2. recomputation from saved predictions ---------------------------------------------------------------------
say("## 2. Metrics recomputed from saved predictions")
from hsrl.data import load_dataset
rng = np.random.default_rng(0)
runs = [d for root in EXPECTED for d in (ROOT / "results" / root).iterdir() if NAME.match(d.name) and (d / "metrics.json").exists()]
cache, worst = {}, 0.0
for d in rng.choice(runs, 25, replace=False):
    m = json.load(open(d / "metrics.json"))
    tag = "stage3" if "eval_stage3" in m else "supervised"
    cfg = yaml.safe_load(open(d / "config.yaml"))["data"]
    key = (cfg["tile_size"], tuple(cfg.get("exclude_readers") or []), cfg["fold"])
    if key not in cache:
        cache[key] = load_dataset(cfg).eval_labels("test")
    x = pd.read_csv(d / f"preds_{tag}_test.csv").merge(cache[key], on="patch_id")
    x = x[~x.tie.astype(bool)]
    y, p = x.majority_label.astype(int).to_numpy(), x.prob_1.to_numpy()
    pr = (p > 0.5).astype(int)
    bal = (((pr == 0) & (y == 0)).sum() / (y == 0).sum() + ((pr == 1) & (y == 1)).sum() / (y == 1).sum()) / 2
    brier = float(np.mean((p - y) ** 2))
    ref = m[f"eval_{tag}"]["test"]["overall"]
    worst = max(worst, abs(bal - ref["bal_acc"]), abs(brier - ref["brier"]))
say(f"- 25 random runs; largest |difference| in balanced accuracy or Brier: **{worst:.5f}** (metrics.json is rounded to 4 d.p.)\n")

# 3. headline numbers -------------------------------------------------------------------------------------------
say("## 3. Headline numbers recomputed from metrics.json")


def table(root, cfgs):
    rows = []
    for c in cfgs:
        vals = []
        for f in range(3):
            for s in range(5):
                ev = final_eval(json.load(open(ROOT / "results" / root / f"f{f}s{s}_{c}" / "metrics.json")))["test"]
                vals.append((f, s, ev["overall"]["acc"], ev["overall"]["bal_acc"], ev["overall"]["brier"], ev["split_vote"]["acc"]))
        v = pd.DataFrame(vals, columns=["fold", "seed", "acc", "bal_acc", "brier", "acc_split"])
        rows.append((c, v))
    return rows


main = dict(table("main", EXPECTED["main"]))
for c, v in main.items():
    say(f"- main/{c}: acc {v.acc.mean():.3f}, bal acc {v.bal_acc.mean():.3f}, Brier {v.brier.mean():.3f}, split acc {v.acc_split.mean():.3f}")
d = main["hsrl"].bal_acc - main["supervised"].bal_acc
db = main["hsrl"].brier - main["supervised"].brier
say(f"- paired HSRL − supervised: bal acc {d.mean():+.3f} ({(d > 0).sum()}/15 better), Brier {db.mean():+.3f} ({(db < 0).sum()}/15 better)")
dev = dict(table("deviations", ["hsrl_s1e60", "supervised_e65"]))
d2 = dev["hsrl_s1e60"].bal_acc - dev["supervised_e65"].bal_acc
say(f"- paired HSRL 60 ep − supervised 65 ep: bal acc {d2.mean():+.3f}")
p1 = dict(table("p1024", ["supervised", "hsrl"]))
say(f"- 1024 px: HSRL bal acc {p1['hsrl'].bal_acc.mean():.3f} vs supervised {p1['supervised'].bal_acc.mean():.3f}\n")

# 4. split integrity --------------------------------------------------------------------------------------------
say("## 4. Split integrity per label set")
sets = [("p512", "labels_benign-drop"), ("p512", "labels_benign-drop_excl-r1"), ("p512", "labels_benign-drop_excl-r4"),
        ("p1024", "labels_benign-drop")]
for T, name in sets:
    base = ROOT / "data/processed/gleason" / T / name
    p = pd.read_csv(base / "patches.csv")
    test_seen = []
    for f in range(3):
        s = pd.read_csv(base / "folds" / f"fold{f}" / "split.csv")
        assert (s.groupby("core_id").split.nunique() == 1).all(), (name, f, "core in two splits")
        ts = sorted(s.loc[s.split == "test", "group_id"].unique())
        assert not set(s.loc[s.split != "test", "group_id"]) & set(ts), (name, f, "test slide leaks")
        assert (s.loc[s.labelled == 1, "split"] == "train").all(), (name, f, "labelled outside train")
        for fn in ("train_unlabelled", "val", "test"):
            assert not ({"r1", "q", "majority_label", "votes_g4"} & set(pd.read_csv(base / "folds" / f"fold{f}" / f"{fn}.csv", nrows=1).columns))
        test_seen += ts
    assert sorted(test_seen) == sorted(p.group_id.unique())
    say(f"- {T}/{name}: OK ({len(p)} patches; no core in two splits; test slides disjoint; each slide tested once; "
        "labelled only from train; unlabelled/val/test files carry no votes)")
say("")

# 5. leakage: where hidden labels are read -----------------------------------------------------------------------
say("## 5. Hidden-label access (eval_labels) call sites")
for f in sorted(list((ROOT / "hsrl").rglob("*.py")) + list((ROOT / "analysis").glob("*.py"))):
    for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if "eval_labels(" in line and "def eval_labels" not in line:
            say(f"- {f.relative_to(ROOT).as_posix()}:{i}: `{line.strip()[:110]}`")
say("All call sites must be evaluation, monitoring or post-hoc analysis; none may be in hsrl/stages.py.")
stages_src = (ROOT / "hsrl/stages.py").read_text(encoding="utf-8")
say(f"- hsrl/stages.py reads hidden labels: **{'YES (PROBLEM)' if 'eval_labels(' in stages_src else 'no'}**\n")

# 6. Stage I reuse --------------------------------------------------------------------------------------------
say("## 6. Stage I reuse pointers")
bad = 0
n = 0
for root in ("soft", "excl_r1", "excl_r4"):
    for d in (ROOT / "results" / root).iterdir():
        m = NAME.match(d.name)
        if not m or "soft" not in m[3] or not m[3].startswith("hsrl"):
            continue
        cfg = yaml.safe_load(open(d / "config.yaml"))
        src = cfg["stage1"].get("reuse_from")
        exp = {"soft/hsrl_soft": f"results/main/f{m[1]}s{m[2]}_hsrl",
               "soft/hsrl_soft_s1e60": f"results/deviations/f{m[1]}s{m[2]}_hsrl_s1e60",
               "excl_r1/hsrl_soft": f"results/excl_r1/f{m[1]}s{m[2]}_hsrl",
               "excl_r4/hsrl_soft": f"results/excl_r4/f{m[1]}s{m[2]}_hsrl"}[f"{root}/{m[3]}"]
        n += 1
        if src != exp or cfg["stage2"]["targets"] != "soft":
            bad += 1
            say(f"- MISMATCH {root}/{d.name}: {src}")
say(f"- {n} reused runs checked, mismatches: **{bad}**\n")

# 7. pilot criterion -----------------------------------------------------------------------------------------
say("## 7. Pilot criterion recomputed independently")
R = pd.read_csv(ROOT / "results/pilot_frozen/per_run.csv")
base = ["probe_hard", "probe_soft", "hsrl_t13", "annotator_aware"]
for metric in ("overall_bal_acc", "split_vote_acc"):
    best = max(base, key=lambda b: R[R.method == b][metric].mean())
    for m in sorted(x for x in R.method.unique() if x.startswith(("interval", "worstcase"))):
        A = R[R.method == m].set_index(["fold", "seed"])[metric]
        B = R[R.method == best].set_index(["fold", "seed"])[metric]
        dd = A - B
        ok = (dd >= 0.01).sum() >= 12 and (dd.groupby(level="fold").mean() >= 0.01).sum() >= 2
        say(f"- {metric}: {m} vs {best}: mean {dd.mean():+.4f}, pairs ≥ +1pt {(dd >= 0.01).sum()}/15, meets: {ok}")

(ROOT / "results/audit").mkdir(parents=True, exist_ok=True)
(ROOT / "results/audit/audit_report.md").write_text("\n".join(out_lines), encoding="utf-8")
