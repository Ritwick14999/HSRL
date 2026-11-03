# HSRL reimplementation + Gleason2019 multi-reader pipeline

Main write-up: [results/REPORT.md](results/REPORT.md). Unspecified choices: [ASSUMPTIONS.md](ASSUMPTIONS.md).

## Setup
```bash
python -m venv .venv
.venv/Scripts/python -m pip install numpy pillow pandas pyyaml scikit-learn matplotlib
```
Raw data layout (not in git): `data/gleason/TrainImgs/*.jpg` and `data/gleason/Map{1..6}/*.png`. Each
`Maps{k}_T.zip` is extracted into its own `Map{k}/` folder, because all maps share identical file names.

## Phase 0: inspect the data
```bash
.venv/Scripts/python -I data/inspect_gleason.py --root data/gleason --out results/phase0_inspect
```
Report: `results/phase0_inspect/phase0_report.md`.

## Phase 1: patch dataset
```bash
# 1a. tile + tissue mask + per-reader class counts + 224px patches (~6 min, both tile sizes)
.venv/Scripts/python -I data/gleason_extract.py --config configs/data/gleason_extract.yaml
# 1b. labels, votes, filtering, slide-grouped folds (seconds; key=value overrides the config)
.venv/Scripts/python -I data/gleason_labels.py --choose-folds tile_size=512      # rank fold partitions
.venv/Scripts/python -I data/gleason_labels.py tile_size=512  benign_rule=ignore
.venv/Scripts/python -I data/gleason_labels.py tile_size=512  benign_rule=drop
.venv/Scripts/python -I data/gleason_labels.py tile_size=1024 benign_rule=ignore
.venv/Scripts/python -I data/gleason_labels.py tile_size=1024 benign_rule=drop
.venv/Scripts/python -I data/gleason_labels.py tile_size=512  benign_rule=ignore "exclude_readers=[2]"
# 1c. integrity checks + statistics
.venv/Scripts/python -I data/gleason_phase1_report.py
```
Outputs: `data/processed/gleason/p{T}/<labels_set>/{patches.csv, folds/fold{k}/...}`. Report:
`results/phase1_dataset/phase1_report.md`.

## Phase 2: HSRL
```bash
.venv/Scripts/python -m pip install torch==2.14.0 torchvision --index-url https://download.pytorch.org/whl/cu130
.venv/Scripts/python -m pip install timm pytest
.venv/Scripts/python -I -m pytest -q tests                                  # unit tests
.venv/Scripts/python -I hsrl/train.py --config configs/smoke.yaml          # smoke test (tiny subset, 2 epochs/stage)
.venv/Scripts/python -I hsrl/train.py --config configs/hsrl_gleason.yaml   # full HSRL, fold 0, seed 0
.venv/Scripts/python -I hsrl/train.py --config configs/hsrl_gleason.yaml method=supervised
.venv/Scripts/python -I hsrl/train.py --config configs/hsrl_gleason.yaml "stage1.terms=[1,3]" run_name=hsrl_no_t2_fold0_seed0
```
Any config key can be overridden with `dotted.key=value`. Examples: `data.fold=1`, `seed=3`, `"data.exclude_readers=[1]"`,
`stage2.targets=soft`, `stage1.conf_rule=boundary`, `data.unlabelled_pool=all_tissue`, `stage3.refresh_every_epoch=true`.

Each run writes `results/<run_name>/`:
- `config.yaml`, `metrics.json`, `train_log.csv` (per step)
- `tuples_stage1.csv` (every mined tuple)
- `pseudo_labels_round*.csv`, `preds_<stage>_<split>.csv`, `embeddings_<stage>_test.npy`
- `model_*.pt`

Per-run folders are not in the repository (only on the training machine). Every run's test metrics are listed in
the matching summary folder (`results/*_summary/all_test_metrics.csv` or `per_run.csv`).

Code layout: `hsrl/data/` (pluggable datasets, vote modes), `hsrl/models.py` (f, g, h), `hsrl/losses.py`
(structural losses), `hsrl/mining.py` (tuple mining), `hsrl/samplers.py`, `hsrl/stages.py` (Stages I–III,
supervised baseline), `hsrl/evaluate.py`, `hsrl/train.py`.

## Phase 3–4: main grid, deviations, census
```bash
.venv/Scripts/python -I scripts/run_queue.py --dry-run     # list jobs still to run
.venv/Scripts/python -I scripts/run_queue.py               # run everything (resumable; ~7.5 h from scratch)
.venv/Scripts/python -I scripts/run_queue.py --only post   # only census / aggregation / t-SNE
```
- **Pause:** create an empty file `results/STOP`. The queue finishes the current run and exits.
- **Resume:** rerun the same command. Finished runs (those with `metrics.json`) are skipped; an interrupted run restarts from scratch.
- Progress: `results/queue_status.csv`. Logs: `results/logs/`.

Outputs:
- `results/main/` — 4 configs × 5 seeds × 3 folds
- `results/deviations/` — not the paper's protocol
- `results/main_summary/report.md`, `results/deviations_summary/report.md`, `results/census_summary/report.md`
- Batch 2 (deviations: 60-epoch Stage I, 65-epoch supervised control): `results/budget_summary/report.md`,
  `results/census_summary_s1e60/report.md`
- Batch 3 (soft-label baselines; HSRL soft runs reuse the hard-target Stage I via `stage1.reuse_from`): `results/soft/`,
  `results/soft_summary/report.md`
- Pseudo-label precision at equal coverage / coverage at equal precision (all runs, no retraining):
  `results/pseudo_coverage/report.md` (`analysis/pseudo_coverage.py`)
- Batch 4 (Map1 excluded, soft vs hard): `results/excl_r1/`, `results/excl_r1_summary/class_shift.md`
  (`analysis/class_shift.py`), `results/excl_r1_summary/report.md`
- Exploratory pilot (interval losses on frozen ImageNet features):
  `.venv/Scripts/python -I hsrl/pilot_frozen.py --config configs/pilot_frozen.yaml`, plus `configs/pilot_frozen_robust.yaml`
  for the robustness checks. Outputs go to `results/pilot_frozen*/`, `results/reader_swap_summary/` and `results/p1024_summary/`.
- MHIST (Batches 6–9): `data/mhist_prepare.py` builds the label sets; runs in `results/mhist*/`, summaries in
  `results/mhist*_summary/`.
- Extension plan step 1 (no training): `.venv/Scripts/python -I analysis/joint_check.py` → `results/joint_check/summary.md`
  (does the joint four-image loss differ from the pairwise worst case on real tuples?).
- Extension plan step 2 (Batches 10–11): new Stage I losses selected by `stage1.loss=supported|interval|interval_worstcase|joint`
  (`stage1.select=certified|random|confidence` for supported ordering; `data.vote_mode` for linked / permuted / counts-only).
  Runs in `results/mhist_ext/` and `results/gleason_ext/`, summaries in `results/*_ext_summary/` and
  `results/*_ext_pseudo_coverage/`.
- Follow-ups (Batches 12–14; D46 ten MHIST draws + HSRL rerun control, D47 certified gap as a margin): runs in
  `results/mhist_d10/`, `results/mhist_rerun/`, `results/mhist_margin/`, `results/gleason_margin/`; pre-registered
  readings by `analysis/followup_check.py` → `results/followup_check/report.md`.
- Brute-force checks of the propositions (vote bounds, certificate, worst-case cost, joint ≤ pairwise, LP relaxation):
  `.venv/Scripts/python -I analysis/proof_checks.py` (~2 min).
- Consolidated write-up: `results/REPORT.md` (figures in `results/REPORT_figures/`)
- t-SNE: `results/main_summary/tsne_f0s0_*.png`

Single analyses:
```bash
.venv/Scripts/python -I analysis/tuple_census.py --run results/main/f0s0_hsrl --epochs 0,29
.venv/Scripts/python -I analysis/aggregate_runs.py --roots results/main --out results/main_summary --pairs hsrl:supervised
.venv/Scripts/python -I analysis/tsne.py --root results/main --fold 0 --seed 0 --out results/main_summary
```
