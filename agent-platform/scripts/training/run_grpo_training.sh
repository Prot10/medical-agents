#!/bin/bash
# GRPO Training from SFT checkpoint on gold trajectories
# Run: bash agent-platform/scripts/training/run_grpo_training.sh
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"  # repo root

# Where checkpoint adapters live. Defaults to EOS; override for local NVMe.
CHECKPOINTS_ROOT="${CHECKPOINTS_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent/checkpoints}"
mkdir -p "$CHECKPOINTS_ROOT"

# Where generated training data lives. Defaults to EOS; override for local.
TRAINING_DATA_ROOT="${TRAINING_DATA_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent/training_data}"
mkdir -p "$TRAINING_DATA_ROOT"

export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

echo "========================================="
echo " GRPO Training — from SFT checkpoint"
echo " Model: Qwen/Qwen3.5-9B + SFT LoRA"
echo " Data: 140 fold0 train cases (no val contamination)"
echo " Reward: online (6-component, 200 NeuroBench cases)"
echo " LoRA: rank=64, alpha=128, QLoRA NF4"
echo " Epochs: 5, gens=2, max_completion=1024"
echo " Estimated: ~4h on single A100-40GB"
echo "========================================="
echo ""
echo "Start time: $(date)"
echo ""

uv run python -m neuroagent.training.train_grpo \
    --stage grpo \
    --model "$CHECKPOINTS_ROOT/sft_769/checkpoint-272" \
    --data "$TRAINING_DATA_ROOT/grpo_dataset/train_fold0.jsonl" \
    --output "$CHECKPOINTS_ROOT/grpo_from_sft" \
    --lora-rank 64 \
    --lora-alpha 128 \
    --epochs 5 \
    --batch-size 1 \
    --num-generations 2 \
    --max-completion-length 1024 \
    --qlora

echo ""
echo "========================================="
echo " GRPO Training Complete"
echo " Checkpoint: $CHECKPOINTS_ROOT/grpo_from_sft"
echo " End time: $(date)"
echo "========================================="
