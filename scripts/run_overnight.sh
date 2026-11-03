#!/usr/bin/env bash
# Overnight batch (2026-10-25): (1) exploratory pilot, (2) pilot robustness + Map1-excluded pilot,
# (3) Map4 reader swap, (4) 1024 px tiles. Resumable: finished pilot reports are skipped, and the queue skips
# finished runs. A failure is logged and the script moves on.
cd "$(dirname "$0")/.."
PY=.venv/Scripts/python
mkdir -p results/logs/pilot
pilot () {  # name, report path, args...
  local name=$1 done=$2; shift 2
  if [ -f "$done" ]; then echo "== $name: already done"; return; fi
  echo "== $name ($(date +%H:%M:%S))"
  $PY -I hsrl/pilot_frozen.py "$@" > "results/logs/pilot/$name.log" 2>&1 || echo "   FAILED: see results/logs/pilot/$name.log"
}
pilot main        results/pilot_frozen/report.md         --config configs/pilot_frozen.yaml
pilot robust      results/pilot_frozen_robust/report.md  --config configs/pilot_frozen_robust.yaml
pilot excl_r1     results/pilot_frozen_excl_r1/report.md --config configs/pilot_frozen.yaml \
      "data.exclude_readers=[1]" results_dir=results/pilot_frozen_excl_r1 \
      features_path=data/processed/gleason/p512/features_effb2_imagenet_excl-r1.npz
echo "== queue: Map4 reader swap + 1024 px tiles ($(date +%H:%M:%S))"
$PY -I scripts/run_queue.py
echo "== overnight finished ($(date +%H:%M:%S))"
