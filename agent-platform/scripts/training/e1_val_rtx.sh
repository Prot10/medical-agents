#!/usr/bin/env bash
# E1 validation on the RTX PRO 6000, in the training pod beside the policy arm (10 Nov 2026: Andrea asked to keep
# the A100s free and use the RTX only). Waits until the outcome arm has ended, so one training arm (~35 GB) and
# this vLLM (GPU_MEMORY_UTILIZATION 0.30, ~29 GB) share the 96 GB with a margin. Scores every archived adapter
# (WEIGHTS/<arm>/seed-N/adapters/checkpoint-*) on the 60 validation cases, seeds 0-2, then picks each arm's
# checkpoint by its own reward (select_checkpoint.py, decision D7). Engineering only (draft policies).
#
# Usage (inside the pod, tmux `val`): SEED=1 bash e1_val_rtx.sh
# One arm trained alone (13 Nov 2026, policy reward v3): ARMS=policy WAIT_FOR= R=/tmp/ma-<snapshot> V=/tmp/venv-<snapshot>
#   RUN=<runs>/e1_qwen3.5-9b-policy-v3/seed-1 W=<ckpts>/qwen3.5-9b-policy-v3 L=/tmp/e1val-v3/seed-1 SEED=1 bash e1_val_rtx.sh
# With one arm (~35 GB) training there is room from the start, so WAIT_FOR is empty and the 40 GB check is the gate.
# Starts from the results already on EOS ($OUT), copied to /tmp, so nothing scored is run again.
# Ends with E1_VAL_EXIT=done in $L/loop.log once checkpoint-500 is scored on all seeds in both arms.
set -uo pipefail
SEED=${SEED:-1}
R=${R:-/tmp/ma-e1} V=${V:-/tmp/venv-e1}  # the snapshot and venv of e1_rtx.sh
W=${W:-/eos/project-d/diagbox/dvc/NeuroAgent/checkpoints/paper-e1/qwen3.5-9b}
RUN=${RUN:-/eos/project-d/diagbox/dvc/aprotani/medical-agents/runs/e1_qwen3.5-9b/seed-$SEED}
OUT=$RUN/val
L=${L:-/tmp/e1val/seed-$SEED}
ARMS=${ARMS:-policy outcome} WAIT_FOR=${WAIT_FOR-outcome exit=}
export HF_HOME=/tmp/hf HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false DRAFT=1
export VLLM_CACHE_ROOT=/tmp/vllm-cache TRITON_CACHE_DIR=/tmp/triton TORCHINDUCTOR_CACHE_DIR=/tmp/inductor
export VLLM_CUDART_SO_PATH=$V/lib/python3.12/site-packages/nvidia/cu13/lib/libcudart.so.13
export VLLM_VENV=$V PYTHON=$V/bin/python GPU_MEMORY_UTILIZATION=${GPU_MEMORY_UTILIZATION:-0.30}
export PYTHONPATH=$R/agent-platform/src:$R/packages/neuroagent-schemas/src
mkdir -p "$L"
log() { echo "$(date -Is) $*" >> "$L/loop.log"; }
[ -d "$L/policy" ] || rsync -a "$OUT/" "$L/" 2>/dev/null

[ -n "$WAIT_FOR" ] && until grep -q "$WAIT_FOR" "$RUN/status.txt" 2>/dev/null; do sleep 300; done
log "validation starts: arms [$ARMS], gpu util $GPU_MEMORY_UTILIZATION"
done_arm() { for s in 0 1 2; do grep -q "^checkpoint-500 seed=$s exit=0" "$L/$1/status.txt" 2>/dev/null || return 1; done; }
while true; do
  for r in $ARMS; do
    a=$W/$r/seed-$SEED/adapters
    ls "$a" 2>/dev/null | grep -q '^checkpoint-' || continue
    # Leave room for the training arm: start a vLLM only with 40 GB free.
    until [ "$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits)" -ge 40000 ]; do sleep 120; done
    log "$r: scoring"
    bash "$R/agent-platform/scripts/training/eval_checkpoints.sh" "$a" "$R/data/neurobench/splits/validation_cases.txt" \
      "$L/$r" 0 1 2 >> "$L/loop.log" 2>&1
    "$PYTHON" "$R/agent-platform/scripts/training/select_checkpoint.py" "$L/$r" --reward $r --allow-draft-policies \
      --json "$L/$r/selection.json" > "$L/$r/selection.txt" 2>&1
    rsync -a --exclude adapters "$L/" "$OUT/" 2>/dev/null
  done
  all=1; for r in $ARMS; do done_arm $r || all=0; done
  [ $all = 1 ] && { log "E1_VAL_EXIT=done"; rsync -a --exclude adapters "$L/" "$OUT/"; break; }
  sleep 1800
done
