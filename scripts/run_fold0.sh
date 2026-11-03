#!/usr/bin/env bash
# Phase 3 (fold 0, seed 0) + Phase 4 census. Stops at the first failure.
set -euo pipefail
cd "$(dirname "$0")/.."
PY=.venv/Scripts/python
mkdir -p results/logs

echo "== unit tests"; $PY -I -m pytest -q tests
echo "== smoke: collapse monitor";  $PY -I hsrl/train.py --config configs/smoke.yaml run_name=smoke_monitor > results/logs/smoke_monitor.log 2>&1
test -s results/smoke_monitor/stage1_monitor.csv
echo "== smoke: no Stage I";        $PY -I hsrl/train.py --config configs/smoke.yaml run_name=smoke_no_stage1 stage1.enabled=false > results/logs/smoke_no_stage1.log 2>&1

run () {  # run_name, overrides...
  local name=$1; shift
  echo "== $name  ($(date +%H:%M:%S))"
  $PY -I hsrl/train.py --config configs/hsrl_gleason.yaml run_name="$name" "$@" > "results/logs/$name.log" 2>&1
  grep -E "^\[eval|WARNING|done" "results/logs/$name.log" || true
}
run f0s0_supervised       method=supervised
run f0s0_hsrl
run f0s0_hsrl_no_t2       "stage1.terms=[1,3]"
run f0s0_hsrl_no_stage1   stage1.enabled=false

echo "== summary"
$PY -I analysis/summarise_runs.py --out results/phase3_fold0 \
    --runs results/f0s0_supervised results/f0s0_hsrl results/f0s0_hsrl_no_t2 results/f0s0_hsrl_no_stage1 \
    > results/logs/summary.log 2>&1
echo "== census"
$PY -I analysis/tuple_census.py --run results/f0s0_hsrl --epochs 0,29 > results/logs/census_hsrl.log 2>&1
$PY -I analysis/tuple_census.py --run results/f0s0_hsrl_no_t2 --epochs 0,29 > results/logs/census_hsrl_no_t2.log 2>&1
echo "== all done ($(date +%H:%M:%S))"
