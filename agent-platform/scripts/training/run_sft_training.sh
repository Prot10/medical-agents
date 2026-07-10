#!/bin/bash
# SFT on gold trajectories (agent distillation).
#
# Run: bash agent-platform/scripts/training/run_sft_training.sh [model]
#   model defaults to Qwen/Qwen3.5-9B; pass Qwen/Qwen3.5-4B for the small student.
#
# max_seq comes from the probe (results/sft_probe/max_seq_probe.json) so training length
# is a measured hardware fact, not a guess. Override with MAX_SEQ=N.
set -euo pipefail

cd /home/aprotani/projects/medical-agents

MODEL="${1:-Qwen/Qwen3.5-9B}"
MODEL_TAG="$(basename "$MODEL")"

# Base models live on EOS; local disk has no room for them.
export HF_HOME="${HF_HOME:-/eos/project-d/diagbox/dvc/NeuroAgent/models/base/huggingface}"

CHECKPOINTS_ROOT="${CHECKPOINTS_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent/checkpoints}"
mkdir -p "$CHECKPOINTS_ROOT"

TRAINING_DATA_ROOT="${TRAINING_DATA_ROOT:-./training_data}"
DATA="$TRAINING_DATA_ROOT/gold_trajectories_v6/trajectories.jsonl"

# Longest real trajectory measured on the train split is ~9.3k tokens, so anything above
# ~10k only wastes the truncation ceiling — cap the probe's answer there.
SEQ_CAP="${SEQ_CAP:-12288}"
PROBE_JSON="results/sft_probe/max_seq_probe.json"
if [ -z "${MAX_SEQ:-}" ]; then
  if [ ! -f "$PROBE_JSON" ]; then
    echo "ERROR: $PROBE_JSON missing. Run probe_max_seq_length.py or set MAX_SEQ=N." >&2
    exit 1
  fi
  MAX_SEQ="$(python3 -c "
import json
probed = json.load(open('$PROBE_JSON'))['shared_max_seq_length']
print(min(probed, $SEQ_CAP))")"
fi

export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

N_TRAJ="$(wc -l < "$DATA")"

echo "========================================="
echo " SFT — agent distillation"
echo " Model:      $MODEL (QLoRA NF4)"
echo " Data:       $DATA ($N_TRAJ trajectories)"
echo " Max seq:    $MAX_SEQ tokens (from probe)"
echo " LoRA:       rank=64, alpha=128"
echo " Epochs:     3, batch=1, grad_accum=8"
echo " Loss:       assistant-only (observations masked)"
echo " Scheduler:  cosine, weight_decay=0.01, NEFTune=5.0"
echo " Validation: 10% of TRAIN cases (test set untouched)"
echo "========================================="
echo "Start: $(date)"
echo ""

uv run python -m neuroagent.training.train_grpo \
    --stage sft \
    --model "$MODEL" \
    --data "$DATA" \
    --output "$CHECKPOINTS_ROOT/sft_${MODEL_TAG}" \
    --lora-rank 64 \
    --lora-alpha 128 \
    --epochs 3 \
    --batch-size 1 \
    --top-fraction 1.0 \
    --max-seq-length "$MAX_SEQ" \
    --splits-dir data/neurobench/splits \
    --val-fraction 0.1 \
    --qlora

echo ""
echo "========================================="
echo " Done. Checkpoint: $CHECKPOINTS_ROOT/sft_${MODEL_TAG}"
echo " End: $(date)"
echo "========================================="
