#!/usr/bin/env bash
# MIMIC pilot, 7 Nov 2026: no tools vs tools vs GRPO-trained, Qwen3.5-9B, on the converted MIMIC
# cases. Runs on rockhopper in tmux; record-derived files (cases, episodes, logs) stay under OUT,
# which must be in /eos/user/a/aprotani/physionet/ (PhysioNet DUA). Only compare.txt, which holds
# aggregates, is meant to be read from elsewhere.
#
# Waits until the GPU queue in tmux `panel` has ended and the case builder has written
# report/task04.done, snapshots the cases, serves Qwen3.5-9B with two GRPO adapters from the
# 2 Nov sweep (arm `base` = the default train_grpo configuration, arm `grpo` = the best arm on
# validation), and runs four arms, seeds 1-3, draft policies (engineering, not reportable):
#   narrative   presentation only, no tool catalogue (narrative-qwen3.5-9b)
#   tools       policy loop, base model (policy-qwen3.5-9b)
#   grpo-default policy loop, adapter sweep arm `base`
#   grpo-best    policy loop, adapter sweep arm `grpo`
#
#   tmux new-session -d -s mimic-eval "CODE=~/projects/ma-eval OUT=$W/out/eval_20261107 \
#       bash ~/projects/ma-eval/scripts/paper/mimic_eval.sh"
# Later case sets: CASES_SRC=$W/out/06_cases SELECTION=$W/out/06_selection.csv DONE_FLAG=$W/report/task06.done
set -uo pipefail

W=${W:-/eos/user/a/aprotani/physionet/work/mimic-neuro}
CODE=${CODE:?code checkout}
OUT=${OUT:?output folder under /eos/user/a/aprotani/physionet/}
[[ "$OUT" == /eos/user/a/aprotani/physionet/* ]] || { echo "OUT must be under the PhysioNet folder"; exit 1; }
PY=${PY:-$HOME/projects/medical-agents/.venv/bin/python}
VLLM_VENV=${VLLM_VENV:-$HOME/projects/medical-agents/.venv-vllm}
SEEDS=${SEEDS:-"1 2 3"}
ADAPTERS=${ADAPTERS:-/dev/shm/adapters-mimic-eval}
CASES_SRC=${CASES_SRC:-}
DONE_FLAG=${DONE_FLAG:-$W/report/task04.done}  # the case builder's done flag to wait for
ADAPTER_SRC=${ADAPTER_SRC:-/eos/project-d/diagbox/dvc/NeuroAgent/checkpoints/sweep-2026-11}
# TMPDIR goes to EOS only for the benchmark: vLLM puts its IPC sockets in the temp folder, and
# Unix sockets do not work on the EOS mount.
mkdir -p "$OUT"
STATUS=$OUT/status.txt
log() { echo "$(date '+%F %T') $*" | tee -a "$STATUS"; }

while tmux has-session -t panel 2>/dev/null; do sleep 120; done
log "panel queue ended"
while [ ! -f "$DONE_FLAG" ]; do sleep 120; done
log "case builder done ($(basename "$DONE_FLAG"))"
if [ -z "$CASES_SRC" ]; then
  for d in "$W/out/04_cases" "$W/out/03_cases"; do
    [ -d "$d" ] && [ "$(ls "$d"/*.json 2>/dev/null | wc -l)" -ge 40 ] && { CASES_SRC=$d; break; }
  done
fi
[ -n "$CASES_SRC" ] || { log "no case folder found"; exit 1; }
# The case folder also keeps drafts that were excluded on reading or replaced: copy only the
# cases the selection file lists without an exclusion (04_selection.csv, else 03_selection.csv).
SELECTION=${SELECTION:-$W/out/$(basename "$CASES_SRC" | cut -d_ -f1)_selection.csv}
[ -f "$SELECTION" ] || { log "no selection file $SELECTION"; exit 1; }
if [ ! -d "$OUT/dataset/cases" ]; then
  mkdir -p "$OUT/dataset/cases"
  python3 - "$SELECTION" "$CASES_SRC" "$OUT/dataset/cases" <<'EOF' || { log "case copy failed"; exit 1; }
import csv, shutil, sys
from pathlib import Path
selection, src, dst = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
keep = [row["case_id"] for row in csv.DictReader(open(selection)) if row["case_id"] and not row["exclusion"]]
missing = [case for case in keep if not (src / f"{case}.json").exists()]
if missing:
    sys.exit(f"{len(missing)} selected cases missing from the case folder")
for case in keep:
    shutil.copy2(src / f"{case}.json", dst / f"{case}.json")
EOF
fi
log "cases: $(ls "$OUT/dataset/cases" | wc -l) from $CASES_SRC"
( cd "$OUT/dataset/cases" && sha256sum *.json > ../SHA256SUMS )

for a in base grpo; do  # stage the two sweep adapters in RAM (weights never on local disk)
  if [ ! -f "$ADAPTERS/$a/adapter_config.json" ]; then
    mkdir -p "$ADAPTERS/$a" && cp "$ADAPTER_SRC/$a/adapter_config.json" "$ADAPTER_SRC/$a/adapter_model.safetensors" "$ADAPTERS/$a/" \
      && cmp -s "$ADAPTER_SRC/$a/adapter_model.safetensors" "$ADAPTERS/$a/adapter_model.safetensors" \
      || { log "could not stage adapter $a from $ADAPTER_SRC"; exit 1; }
  fi
done
if nvidia-smi --query-compute-apps=pid --format=csv,noheader | grep -q .; then
  log "GPU busy, waiting"; while nvidia-smi --query-compute-apps=pid --format=csv,noheader | grep -q .; do sleep 120; done
fi

setsid bash -c "cd '$CODE' && HF_HOME=/dev/shm/hf HF_HUB_OFFLINE=1 VLLM_VENV='$VLLM_VENV' \
   LORA_MODULES='grpo-default=$ADAPTERS/base grpo-best=$ADAPTERS/grpo' nice -n 10 \
   agent-platform/scripts/runtime/serve_model.sh qwen3.5-9b > '$OUT/vllm.log' 2>&1" &
SERVER=$!
trap 'kill -- -"$SERVER" 2>/dev/null' EXIT
trap 'exit 1' HUP INT TERM  # tmux kill-session sends HUP: still stop the server
up=0
for _ in $(seq 80); do
  models=$(curl -sf localhost:8000/v1/models) && { up=1; break; }
  kill -0 $SERVER 2>/dev/null || break
  sleep 15
done
[ $up = 1 ] && grep -q grpo-default <<<"$models" && grep -q grpo-best <<<"$models" || { log "vLLM did not start with both adapters"; exit 1; }
log "vLLM up with grpo-default and grpo-best"

bench() {  # bench ARM PROFILE SEED [SERVED]
  local dir=$OUT/$1-s$3
  [ -f "$dir/summary.json" ] && return 0
  TMPDIR=$W/tmp PYTHONPATH=$CODE/agent-platform/src:$CODE/packages/neuroagent-schemas/src nice -n 10 "$PY" \
    -m neuroagent.evaluation.benchmark --profile "$2" --all --seed "$3" --concurrency 16 \
    --allow-draft-policies --resume --dataset-dir "$OUT/dataset" --output "$dir" \
    ${4:+--served-model "$4"} >> "$dir.log" 2>&1
  log "$1 s$3 exit=$?"
}

for s in $SEEDS; do
  bench narrative narrative-qwen3.5-9b "$s"
  bench tools policy-qwen3.5-9b "$s"
  bench grpo-default policy-qwen3.5-9b "$s" grpo-default
  bench grpo-best policy-qwen3.5-9b "$s" grpo-best
done

PYTHONPATH=$CODE/agent-platform/src:$CODE/packages/neuroagent-schemas/src "$PY" "$CODE/scripts/paper/arm_compare.py" \
  --root "$OUT" --arms narrative tools grpo-default grpo-best --reference tools --seeds $SEEDS \
  > "$OUT/compare.txt" 2>&1
log "compare written"
kill -- -"$SERVER" 2>/dev/null; trap - EXIT
rm -rf "$ADAPTERS"
log ALL_DONE
