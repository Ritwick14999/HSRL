"""Resumable job queue for the main grid, the deviation experiments and the post-processing.

- A run counts as done when <results_root>/<run_name>/metrics.json exists; done runs are skipped.
- A run directory without metrics.json is incomplete and is re-run from scratch (overwrite=true).
- Order: pre jobs (pre_jobs), then training jobs, then post jobs (post_jobs). Pre/post jobs are skipped once their
  done marker exists (jobs without a marker always rerun; they are cheap summaries).
- Pause gracefully: create an empty file results/STOP. The runner finishes the current job, deletes the file and exits.
  Rerun this script to continue where it stopped.
- Progress: results/queue_status.csv; per-run logs: results/logs/<root>/<run_name>.log

Usage: python -I scripts/run_queue.py [--only main|deviations|post] [--dry-run]
"""
import argparse
import csv
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
STOP = ROOT / "results" / "STOP"
STATUS = ROOT / "results" / "queue_status.csv"

MAIN_CFGS = {"supervised": ["method=supervised"], "hsrl": [], "hsrl_no_t2": ["stage1.terms=[1,3]"],
             "hsrl_no_stage1": ["stage1.enabled=false"]}
# DEVIATIONS FROM THE PAPER (fold 0): saved under results/deviations/
DEV_CFGS = {"hsrl_s1e60": ["stage1.epochs=60"], "hsrl_no_t2_s1e60": ["stage1.terms=[1,3]", "stage1.epochs=60"],
            "hsrl_boundary": ["stage1.conf_rule=boundary"]}


def train_job(root, fold, seed, cfg, overrides, config="configs/hsrl_gleason.yaml"):
    name = f"f{fold}s{seed}_{cfg}"
    return {"kind": "train", "root": root, "name": name, "config": config,
            "args": [f"run_name={name}", f"results_root=results/{root}", f"data.fold={fold}", f"seed={seed}", *overrides]}


# Batch 2 (DEVIATIONS): 60-epoch Stage I on all folds and a budget-matched supervised control (60 + 5 epochs)
BATCH2_CFGS = {"hsrl_s1e60": DEV_CFGS["hsrl_s1e60"], "hsrl_no_t2_s1e60": DEV_CFGS["hsrl_no_t2_s1e60"],
               "supervised_e65": ["method=supervised", "supervised.epochs=65"]}


def build_queue():
    q = []
    main = lambda seeds: [train_job("main", f, s, c, o) for s in seeds for f in range(3) for c, o in MAIN_CFGS.items()]
    dev = lambda seeds: [train_job("deviations", 0, s, c, o) for s in seeds for c, o in DEV_CFGS.items()]
    q += main([0]) + dev([0]) + main([1, 2, 3, 4]) + dev([1, 2])
    q += [train_job("deviations", f, s, c, o) for s in range(5) for f in range(3) for c, o in BATCH2_CFGS.items()]
    # Batch 3: soft targets (1-q, q) from labelled-patch votes. HSRL soft runs reuse the Stage I checkpoint of the
    # hard-target run with the same fold, seed and Stage I schedule (Stage I is identical by construction).
    for s in range(5):
        for f in range(3):
            q += [train_job("soft", f, s, "supervised_soft", ["method=supervised", "supervised.targets=soft"]),
                  train_job("soft", f, s, "supervised_soft_e65", ["method=supervised", "supervised.targets=soft",
                                                                  "supervised.epochs=65"]),
                  train_job("soft", f, s, "hsrl_soft", ["stage2.targets=soft", f"stage1.reuse_from=results/main/f{f}s{s}_hsrl"]),
                  train_job("soft", f, s, "hsrl_soft_s1e60", ["stage2.targets=soft", "stage1.epochs=60",
                                                              f"stage1.reuse_from=results/deviations/f{f}s{s}_hsrl_s1e60"])]
    # Batch 4: Map1 excluded (label set labels_benign-drop_excl-r1), hard vs soft. hsrl_soft reuses the Stage I of the
    # hsrl run just before it (same fold, seed, label set).
    ex = "data.exclude_readers=[1]"
    for s in range(5):
        for f in range(3):
            q += [train_job("excl_r1", f, s, "supervised", ["method=supervised", ex]),
                  train_job("excl_r1", f, s, "supervised_soft", ["method=supervised", "supervised.targets=soft", ex]),
                  train_job("excl_r1", f, s, "hsrl", [ex]),
                  train_job("excl_r1", f, s, "hsrl_soft", ["stage2.targets=soft", ex,
                                                          f"stage1.reuse_from=results/excl_r1/f{f}s{s}_hsrl"])]
    # Batch 5a: reader-swap control for §8, Map4 excluded (no grading bias, coverage similar to Map1)
    ex4 = "data.exclude_readers=[4]"
    for s in range(5):
        for f in range(3):
            q += [train_job("excl_r4", f, s, "supervised", ["method=supervised", ex4]),
                  train_job("excl_r4", f, s, "supervised_soft", ["method=supervised", "supervised.targets=soft", ex4]),
                  train_job("excl_r4", f, s, "hsrl", [ex4]),
                  train_job("excl_r4", f, s, "hsrl_soft", ["stage2.targets=soft", ex4,
                                                          f"stage1.reuse_from=results/excl_r4/f{f}s{s}_hsrl"])]
    # Batch 5b: tile-size sensitivity (D9): the 4 main configurations on 1024 px tiles
    for s in range(5):
        for f in range(3):
            q += [train_job("p1024", f, s, c, [*o, "data.tile_size=1024"]) for c, o in MAIN_CFGS.items()]
    # Batch 6: MHIST reproduction of the paper's Table 2 / Table 4 (draw k = labelled draw k, seed k)
    mh = {"supervised": ["method=supervised"], "supervised_full": ["method=supervised", "data.labelled_pct=100"],
          "hsrl": [], "hsrl_no_t2": ["stage1.terms=[1,3]"], "hsrl_no_stage1": ["stage1.enabled=false"],
          "hsrl_triplet": ["stage1.terms=[1]"]}
    for k in range(5):
        q += [train_job("mhist", k, k, c, o, config="configs/mhist.yaml") for c, o in mh.items()]
    # Batch 7: MHIST label curve for supervised training (20% and 50% labelled) and soft targets (1-q, q) from the
    # labelled images' vote counts. hsrl_soft reuses the Stage I of the Batch 6 hsrl run with the same draw.
    for k in range(5):
        q += [train_job("mhist", k, k, "supervised_p20", ["method=supervised", "data.labelled_pct=20"], config="configs/mhist.yaml"),
              train_job("mhist", k, k, "supervised_p50", ["method=supervised", "data.labelled_pct=50"], config="configs/mhist.yaml"),
              train_job("mhist", k, k, "supervised_soft", ["method=supervised", "supervised.targets=soft"], config="configs/mhist.yaml"),
              train_job("mhist", k, k, "hsrl_soft", ["stage2.targets=soft", f"stage1.reuse_from=results/mhist/f{k}s{k}_hsrl"],
                        config="configs/mhist.yaml")]
    # Batch 8 (D41): protocol checks for the 10% gap on MHIST. Diagnostics, not the paper's protocol.
    ep = "eval.per_epoch_test=true"
    for k in range(5):
        mk = lambda c, o: train_job("mhist_protocol", k, k, c, o, config="configs/mhist.yaml")
        q += [mk("supervised_epochlog", ["method=supervised", ep]),
              mk("hsrl_epochlog", [ep, f"stage1.reuse_from=results/mhist/f{k}s{k}_hsrl"]),
              mk("supervised_all10", ["method=supervised", "data.labelled_pct=10all"]),
              mk("hsrl_all10", ["data.labelled_pct=10all"]),
              mk("supervised_r288", ["method=supervised", "augment.resize=288"]),
              mk("hsrl_r288", ["augment.resize=288"])]
    # Batch 9 (D43): random image-level train/test split instead of the official one (label sets labels_p10rs /
    # labels_p100rs, built by the pre job below). Protocol check for the 10% gap, not the paper's protocol.
    rs = {"supervised": ["method=supervised", "data.labelled_pct=10rs"], "hsrl": ["data.labelled_pct=10rs"],
          "hsrl_no_stage1": ["stage1.enabled=false", "data.labelled_pct=10rs"],
          "supervised_full": ["method=supervised", "data.labelled_pct=100rs"]}
    for k in range(5):
        q += [train_job("mhist_randsplit", k, k, c, o, config="configs/mhist.yaml") for c, o in rs.items()]
    # Batch 10 (D45, extension plan step 2): Stage I structural supervision replaced by annotation-aware losses on
    # MHIST (counts only); soft Stage II targets as the matched baseline results/mhist/f{k}s{k}_hsrl_soft.
    for k in range(5):
        q += [train_job("mhist_ext", k, k, c, ["stage2.targets=soft", *o], config="configs/mhist.yaml")
              for c, o in EXT_CFGS.items()]
    # Batch 11 (D45): supported ordering on Gleason with linked, permuted and counts-only votes (information removal,
    # plan §6). Permuted votes are redrawn per seed. Baseline: results/soft/f{f}s{s}_hsrl_soft.
    for s in range(2):
        for f in range(3):
            q += [train_job("gleason_ext", f, s, f"supported_{m}", ["stage2.targets=soft", "stage1.loss=supported",
                                                                     f"data.vote_mode={v}", f"data.vote_seed={s}"])
                  for m, v in (("linked", "linked"), ("permuted", "permuted"), ("counts", "counts_only"))]
    # Batch 12 (D47): the guaranteed gap as the margin of supported ordering. MHIST draws 0-4 first (draws 5-9 follow
    # in Batch 13), then Gleason with linked votes (vs results/gleason_ext/*_supported_linked).
    mg = lambda k: [train_job("mhist_margin", k, k, c, ["stage2.targets=soft", *o], config="configs/mhist.yaml")
                    for c, o in MARGIN_CFGS.items()]
    for k in range(5):
        q += mg(k)
    for s in range(2):
        for f in range(3):
            q += [train_job("gleason_margin", f, s, "supported_gap_linked", ["stage2.targets=soft", "stage1.loss=supported",
                            "stage1.margin=gap", "data.vote_mode=linked", f"data.vote_seed={s}"])]
    # Batch 13 (D46): MHIST draws 5-9 for the Batch 6/7 baselines and the D45 losses, plus the D47 margin runs
    for k in range(5, 10):
        mk = lambda c, o: train_job("mhist_d10", k, k, c, o, config="configs/mhist.yaml")
        q += [mk("hsrl", []), mk("hsrl_soft", ["stage2.targets=soft", f"stage1.reuse_from=results/mhist_d10/f{k}s{k}_hsrl"]),
              mk("supervised", ["method=supervised"]), mk("supervised_soft", ["method=supervised", "supervised.targets=soft"])]
        q += [mk(c, ["stage2.targets=soft", *o]) for c, o in EXT_CFGS.items()] + mg(k)
    # Batch 14 (D46): HSRL rerun control, seed 100 + k on draw k (the later seed= override wins)
    for k in range(10):
        rr = lambda c, o: train_job("mhist_rerun", k, k, c, [*o, f"seed={100 + k}"], config="configs/mhist.yaml")
        q += [rr("hsrl_rerun", []),
              rr("hsrl_soft_rerun", ["stage2.targets=soft", f"stage1.reuse_from=results/mhist_rerun/f{k}s{k}_hsrl_rerun"])]
    return q


EXT_CFGS = {"supported": ["stage1.loss=supported"],
            "supported_random": ["stage1.loss=supported", "stage1.select=random"],
            "supported_conf": ["stage1.loss=supported", "stage1.select=confidence"],
            "interval": ["stage1.loss=interval"],
            "worstcase": ["stage1.loss=interval_worstcase"],
            "joint": ["stage1.loss=joint", "stage1.joint_model=exact"]}
MARGIN_CFGS = {f"supported_{m}": ["stage1.loss=supported", f"stage1.margin={m}"]
               for m in ("gap", "gap_shuffled", "similarity")}


def pre_jobs():
    """Run before the training queue (batch 9): the fine-tuned-feature pilot (D42; needs only the finished Batch 6
    supervised checkpoints) and the random-split MHIST label sets that the Batch 9 training jobs read (D43)."""
    return [{"kind": "pre", "name": "pilot_ft_mhist", "cmd": [PY, "-I", "hsrl/pilot_frozen.py", "--config",
             "configs/pilot_ft_mhist.yaml"], "done": ROOT / "results/pilot_ft_mhist/report.md"},
            {"kind": "pre", "name": "prepare_mhist_randsplit", "cmd": [PY, "-I", "data/mhist_prepare.py", "--split", "random",
             "--labelled-fracs", "0.10", "1.0"], "done": ROOT / "data/processed/mhist/labels_p100rs/stats.json"}]


def post_jobs():
    jobs = [{"kind": "post", "name": f"census_f{f}s{s}_hsrl",
             "cmd": [PY, "-I", "analysis/tuple_census.py", "--run", f"results/main/f{f}s{s}_hsrl", "--epochs", "0,29"],
             "done": ROOT / f"results/main/f{f}s{s}_hsrl/census/census_v2.done"} for f in range(3) for s in range(5)]
    jobs += [{"kind": "post", "name": "census_aggregate", "cmd": [PY, "-I", "analysis/census_aggregate.py"], "done": None},
             {"kind": "post", "name": "aggregate_main", "cmd": [PY, "-I", "analysis/aggregate_runs.py", "--roots", "results/main",
              "--out", "results/main_summary", "--pairs", "hsrl:supervised", "hsrl:hsrl_no_t2", "hsrl:hsrl_no_stage1",
              "hsrl_no_t2:supervised", "hsrl_no_stage1:supervised"], "done": None},
             {"kind": "post", "name": "aggregate_deviations", "cmd": [PY, "-I", "analysis/aggregate_runs.py", "--roots",
              "results/main", "results/deviations", "--folds", "0", "--seeds", "0", "1", "2", "--out", "results/deviations_summary",
              "--pairs", "hsrl_s1e60:hsrl", "hsrl_no_t2_s1e60:hsrl_no_t2", "hsrl_s1e60:hsrl_no_t2_s1e60", "hsrl_boundary:hsrl"],
              "done": None},
             {"kind": "post", "name": "tsne_f0s0", "cmd": [PY, "-I", "analysis/tsne.py", "--root", "results/main", "--fold", "0",
              "--seed", "0", "--out", "results/main_summary"], "done": ROOT / "results/main_summary/tsne_f0s0_label.png"}]
    # batch 2: census on the 60-epoch HSRL runs, then the 30- vs 60-epoch / matched-budget comparison
    jobs += [{"kind": "post", "name": f"census_f{f}s{s}_hsrl_s1e60",
              "cmd": [PY, "-I", "analysis/tuple_census.py", "--run", f"results/deviations/f{f}s{s}_hsrl_s1e60", "--epochs", "0,29,59"],
              "done": ROOT / f"results/deviations/f{f}s{s}_hsrl_s1e60/census/census_v2.done"} for f in range(3) for s in range(5)]
    jobs += [{"kind": "post", "name": "census_aggregate_s1e60", "cmd": [PY, "-I", "analysis/census_aggregate.py", "--root",
              "results/deviations", "--cfg", "hsrl_s1e60", "--out", "results/census_summary_s1e60"], "done": None},
             {"kind": "post", "name": "aggregate_budget", "cmd": [PY, "-I", "analysis/aggregate_runs.py", "--roots", "results/main",
              "results/deviations", "--out", "results/budget_summary", "--cfgs", "supervised", "hsrl", "hsrl_no_t2",
              "supervised_e65", "hsrl_s1e60", "hsrl_no_t2_s1e60", "--pairs", "hsrl_s1e60:hsrl", "hsrl_no_t2_s1e60:hsrl_no_t2",
              "supervised_e65:supervised", "hsrl_s1e60:supervised_e65", "hsrl_no_t2_s1e60:supervised_e65",
              "hsrl_s1e60:hsrl_no_t2_s1e60"], "done": None}]
    # batch 3: soft-target comparison and pseudo-label precision/coverage over all runs
    jobs += [{"kind": "post", "name": "aggregate_soft", "cmd": [PY, "-I", "analysis/aggregate_runs.py", "--roots", "results/main",
              "results/deviations", "results/soft", "--out", "results/soft_summary", "--cfgs", "supervised", "supervised_e65",
              "supervised_soft", "supervised_soft_e65", "hsrl", "hsrl_s1e60", "hsrl_soft", "hsrl_soft_s1e60", "--pairs",
              "supervised_soft:supervised", "supervised_soft_e65:supervised_e65", "hsrl_soft:hsrl", "hsrl_soft_s1e60:hsrl_s1e60",
              "hsrl_soft:supervised_soft", "hsrl_soft_s1e60:supervised_soft_e65"], "done": None},
             {"kind": "post", "name": "pseudo_coverage", "cmd": [PY, "-I", "analysis/pseudo_coverage.py", "--roots", "results/main",
              "results/deviations", "results/soft", "--out", "results/pseudo_coverage"], "done": None}]
    # batch 4: Map1 excluded, soft vs hard within the setting, with the with-Map1 shift alongside for reference
    jobs += [{"kind": "post", "name": "aggregate_excl_r1", "cmd": [PY, "-I", "analysis/aggregate_runs.py", "--roots",
              "results/excl_r1", "--out", "results/excl_r1_summary", "--pairs", "supervised_soft:supervised", "hsrl_soft:hsrl",
              "hsrl:supervised", "hsrl_soft:supervised_soft"], "done": None},
             {"kind": "post", "name": "class_shift", "cmd": [PY, "-I", "analysis/class_shift.py", "--setting", "with Map1",
              "results/main", "results/soft", "--setting", "Map1 excluded", "results/excl_r1", "results/excl_r1",
              "--out", "results/excl_r1_summary"], "done": None}]
    # batch 5: reader swap (three settings side by side) and the 1024 px sensitivity check
    jobs += [{"kind": "post", "name": "aggregate_excl_r4", "cmd": [PY, "-I", "analysis/aggregate_runs.py", "--roots",
              "results/excl_r4", "--out", "results/excl_r4_summary", "--pairs", "supervised_soft:supervised", "hsrl_soft:hsrl"],
              "done": None},
             {"kind": "post", "name": "class_shift_reader_swap", "cmd": [PY, "-I", "analysis/class_shift.py",
              "--setting", "with Map1", "results/main", "results/soft", "--setting", "Map1 excluded", "results/excl_r1",
              "results/excl_r1", "--setting", "Map4 excluded", "results/excl_r4", "results/excl_r4",
              "--out", "results/reader_swap_summary"], "done": None},
             {"kind": "post", "name": "aggregate_p1024", "cmd": [PY, "-I", "analysis/aggregate_runs.py", "--roots", "results/p1024",
              "--out", "results/p1024_summary", "--pairs", "hsrl:supervised", "hsrl:hsrl_no_t2", "hsrl:hsrl_no_stage1",
              "hsrl_no_t2:supervised"], "done": None}]
    jobs += [{"kind": "post", "name": "aggregate_mhist", "cmd": [PY, "-I", "analysis/aggregate_runs.py", "--roots", "results/mhist",
              "--out", "results/mhist_summary", "--pairs", "hsrl:supervised", "hsrl:hsrl_no_stage1", "hsrl:hsrl_triplet",
              "hsrl:hsrl_no_t2", "supervised_full:supervised", "supervised_full:hsrl", "supervised_p20:supervised",
              "supervised_p50:supervised", "supervised_soft:supervised", "hsrl_soft:hsrl", "hsrl_soft:supervised_soft"],
              "done": None}]
    # batch 7: MHIST counts-only census (linked verdicts all skipped: no reader identities) and equal-coverage precision
    jobs += [{"kind": "post", "name": f"census_mhist_f{k}s{k}_hsrl",
              "cmd": [PY, "-I", "analysis/tuple_census.py", "--run", f"results/mhist/f{k}s{k}_hsrl", "--epochs", "0,29"],
              "done": ROOT / f"results/mhist/f{k}s{k}_hsrl/census/census_v2.done"} for k in range(5)]
    jobs += [{"kind": "post", "name": "census_aggregate_mhist", "cmd": [PY, "-I", "analysis/census_aggregate.py", "--root",
              "results/mhist", "--cfg", "hsrl", "--out", "results/mhist_census_summary"], "done": None},
             {"kind": "post", "name": "pseudo_coverage_mhist", "cmd": [PY, "-I", "analysis/pseudo_coverage.py", "--roots",
              "results/mhist", "--out", "results/mhist_pseudo_coverage", "--pairs", "hsrl_no_t2:hsrl", "hsrl_no_stage1:hsrl",
              "hsrl_triplet:hsrl", "hsrl_soft:hsrl"], "done": None}]
    # batch 8: protocol checks (D41) and the counts-only frozen-feature pilot on MHIST (D40, exploratory)
    jobs += [{"kind": "post", "name": "epoch_selection_mhist", "cmd": [PY, "-I", "analysis/epoch_selection.py", "--root",
              "results/mhist_protocol", "--out", "results/mhist_protocol_summary"], "done": None},
             {"kind": "post", "name": "aggregate_mhist_protocol", "cmd": [PY, "-I", "analysis/aggregate_runs.py", "--roots",
              "results/mhist", "results/mhist_protocol", "--out", "results/mhist_protocol_summary", "--cfgs", "supervised",
              "hsrl", "supervised_epochlog", "hsrl_epochlog", "supervised_all10", "hsrl_all10", "supervised_r288", "hsrl_r288",
              "--pairs", "supervised_all10:supervised", "hsrl_all10:hsrl", "supervised_r288:supervised", "hsrl_r288:hsrl",
              "hsrl_all10:supervised_all10", "hsrl_r288:supervised_r288"], "done": None},
             {"kind": "post", "name": "pilot_frozen_mhist", "cmd": [PY, "-I", "hsrl/pilot_frozen.py", "--config",
              "configs/pilot_frozen_mhist.yaml"], "done": ROOT / "results/pilot_frozen_mhist/report.md"}]
    # batch 9: random-split runs (D43). Their test sets differ from the official one, so they are summarised on their
    # own; comparisons with results/mhist are of means, not paired.
    jobs += [{"kind": "post", "name": "aggregate_mhist_randsplit", "cmd": [PY, "-I", "analysis/aggregate_runs.py", "--roots",
              "results/mhist_randsplit", "--out", "results/mhist_randsplit_summary", "--pairs", "hsrl:supervised",
              "hsrl:hsrl_no_stage1", "hsrl_no_stage1:supervised", "supervised_full:supervised", "supervised_full:hsrl"],
              "done": None}]
    # batches 10-11 (D45): annotation-aware Stage I losses vs HSRL's (same draws / folds and seeds, soft Stage II)
    ext = list(EXT_CFGS)
    jobs += [{"kind": "post", "name": "aggregate_mhist_ext", "cmd": [PY, "-I", "analysis/aggregate_runs.py", "--roots",
              "results/mhist", "results/mhist_ext", "--out", "results/mhist_ext_summary", "--cfgs", "supervised_soft",
              "hsrl_soft", *ext, "--pairs", *[f"{c}:hsrl_soft" for c in ext], "supported:supported_random",
              "supported:supported_conf", "joint:worstcase", "joint:interval", *[f"{c}:supervised_soft" for c in ext]],
              "done": None},
             {"kind": "post", "name": "pseudo_coverage_mhist_ext", "cmd": [PY, "-I", "analysis/pseudo_coverage.py", "--roots",
              "results/mhist", "results/mhist_ext", "--out", "results/mhist_ext_pseudo_coverage", "--pairs",
              *[f"{c}:hsrl_soft" for c in ext], "supported:supported_random", "supported:supported_conf",
              "joint:worstcase"], "done": None}]
    gl = ["supported_linked", "supported_permuted", "supported_counts"]
    jobs += [{"kind": "post", "name": "aggregate_gleason_ext", "cmd": [PY, "-I", "analysis/aggregate_runs.py", "--roots",
              "results/soft", "results/gleason_ext", "--seeds", "0", "1", "--out", "results/gleason_ext_summary", "--cfgs",
              "supervised_soft", "hsrl_soft", *gl, "--pairs", "supported_linked:supported_permuted",
              "supported_linked:supported_counts", "supported_permuted:supported_counts", *[f"{c}:hsrl_soft" for c in gl]],
              "done": None},
             {"kind": "post", "name": "pseudo_coverage_gleason_ext", "cmd": [PY, "-I", "analysis/pseudo_coverage.py",
              "--roots", "results/soft", "results/gleason_ext", "--out", "results/gleason_ext_pseudo_coverage", "--pairs",
              *[f"{c}:hsrl_soft" for c in gl], "supported_linked:supported_permuted"], "done": None}]
    # batches 12-14 (D46, D47): pre-registered readings, plus the full 10-draw MHIST and Gleason margin summaries
    mr = ["results/mhist", "results/mhist_ext", "results/mhist_d10", "results/mhist_margin", "results/mhist_rerun"]
    jobs += [{"kind": "post", "name": "followup_check", "cmd": [PY, "-I", "analysis/followup_check.py"], "done": None},
             {"kind": "post", "name": "aggregate_mhist_d10", "cmd": [PY, "-I", "analysis/aggregate_runs.py", "--roots", *mr,
              "--out", "results/mhist_d10_summary", "--cfgs", "hsrl", "hsrl_soft", "supervised", "supervised_soft",
              "hsrl_soft_rerun", *ext, *MARGIN_CFGS, "--pairs", *[f"{c}:hsrl_soft" for c in [*ext, *MARGIN_CFGS]],
              "supported_gap:supported", "supported_gap:supported_gap_shuffled", "hsrl:supervised",
              "hsrl_soft:supervised_soft", "hsrl_soft_rerun:hsrl_soft"], "done": None},
             {"kind": "post", "name": "pseudo_coverage_mhist_d10", "cmd": [PY, "-I", "analysis/pseudo_coverage.py", "--roots",
              *mr, "--out", "results/mhist_d10_pseudo_coverage", "--pairs", *[f"{c}:hsrl_soft" for c in [*ext, *MARGIN_CFGS]],
              "supported_gap:supported"], "done": None},
             {"kind": "post", "name": "aggregate_gleason_margin", "cmd": [PY, "-I", "analysis/aggregate_runs.py", "--roots",
              "results/soft", "results/gleason_ext", "results/gleason_margin", "--seeds", "0", "1", "--out",
              "results/gleason_margin_summary", "--cfgs", "hsrl_soft", "supported_linked", "supported_gap_linked",
              "--pairs", "supported_gap_linked:supported_linked", "supported_gap_linked:hsrl_soft"], "done": None}]
    return jobs


def run_side_jobs(jobs, kind):
    """Pre/post jobs: skipped when their done marker exists; a failure is logged and the queue goes on."""
    for j in jobs:
        check_stop()
        if j["done"] is not None and Path(j["done"]).exists():
            continue
        t0 = time.time()
        print(f"[{kind}] {j['name']}  ({time.strftime('%H:%M:%S')})", flush=True)
        rc = run(j["cmd"], ROOT / "results" / "logs" / kind / f"{j['name']}.log")
        log_status({"time": time.strftime("%Y-%m-%d %H:%M:%S"), "job": f"{kind}/{j['name']}",
                    "status": "ok" if rc == 0 else f"FAILED rc={rc}", "sec": round(time.time() - t0)})
        if rc != 0:
            print(f"  FAILED (rc={rc}); see results/logs/{kind}/{j['name']}.log", flush=True)


def log_status(row):
    new = not STATUS.exists()
    with open(STATUS, "a", newline="") as f:
        w = csv.DictWriter(f, ["time", "job", "status", "sec"])
        if new:
            w.writeheader()
        w.writerow(row)


def check_stop():
    if STOP.exists():
        STOP.unlink()
        print(f"STOP file found: exiting cleanly. Rerun `python -I scripts/run_queue.py` to resume.", flush=True)
        sys.exit(0)


def run(cmd, log_path):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "w") as lf:
        return subprocess.run(cmd, cwd=ROOT, stdout=lf, stderr=subprocess.STDOUT).returncode


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["main", "deviations", "post"])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    queue = [j for j in build_queue() if args.only in (None, j["root"])] if args.only != "post" else []
    todo = [j for j in queue if not (ROOT / "results" / j["root"] / j["name"] / "metrics.json").exists()]
    pre = [j for j in pre_jobs() if not Path(j["done"]).exists()] if args.only is None else []
    print(f"{len(pre)} pre jobs to run; {len(queue)} training jobs, {len(queue) - len(todo)} done, {len(todo)} to run",
          flush=True)
    if args.dry_run:
        for j in pre:
            print("pre", j["name"], " ".join(j["cmd"][2:]))
        for j in todo:
            print(j["root"], j["name"], " ".join(j["args"]))
        return
    run_side_jobs(pre, "pre")
    for i, j in enumerate(todo):
        check_stop()
        run_dir = ROOT / "results" / j["root"] / j["name"]
        args_ = list(j["args"]) + (["overwrite=true"] if run_dir.exists() else [])
        t0 = time.time()
        print(f"[{i + 1}/{len(todo)}] {j['root']}/{j['name']}  ({time.strftime('%H:%M:%S')})", flush=True)
        rc = run([PY, "-I", "hsrl/train.py", "--config", j.get("config", "configs/hsrl_gleason.yaml"), *args_],
                 ROOT / "results" / "logs" / j["root"] / f"{j['name']}.log")
        log_status({"time": time.strftime("%Y-%m-%d %H:%M:%S"), "job": f"{j['root']}/{j['name']}",
                    "status": "ok" if rc == 0 else f"FAILED rc={rc}", "sec": round(time.time() - t0)})
        if rc != 0:
            print(f"  FAILED (rc={rc}); see results/logs/{j['root']}/{j['name']}.log. Continuing with the next job.", flush=True)
    if args.only in (None, "post"):
        run_side_jobs(post_jobs(), "post")
    print("queue finished", flush=True)


if __name__ == "__main__":
    main()
