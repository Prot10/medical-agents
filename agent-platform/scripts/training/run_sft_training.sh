#!/bin/bash
# SFT Training on gold trajectories with train/val split
# Run: bash agent-platform/scripts/training/run_sft_training.sh
set -euo pipefail

# Must run from the repo root so DATASET / split paths resolve.
cd /home/aprotani/projects/medical-agents

# Where checkpoint adapters live. Defaults to EOS so finetunes survive across
# nodes; override (e.g. CHECKPOINTS_ROOT=./checkpoints) for fast local NVMe.
CHECKPOINTS_ROOT="${CHECKPOINTS_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent/checkpoints}"
mkdir -p "$CHECKPOINTS_ROOT"

# Where generated training data lives (gold trajectories, DPO pairs, GRPO sets).
# Defaults to EOS; override (e.g. TRAINING_DATA_ROOT=./training_data) locally.
TRAINING_DATA_ROOT="${TRAINING_DATA_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent/training_data}"
mkdir -p "$TRAINING_DATA_ROOT"

export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

echo "========================================="
echo " SFT Training — 769 gold trajectories"
echo " Model: Qwen/Qwen3.5-9B (QLoRA NF4)"
echo " LoRA: rank=64, alpha=128"
echo " Epochs: 5, batch=1, grad_accum=8"
echo " Max seq: 4096 tokens (eval-safe)"
echo " Loss: completion-only (not on prompts)"
echo " Scheduler: cosine, weight_decay=0.01"
echo " NEFTune: alpha=5.0"
echo " Validation: fold 0 (541 train / 228 val)"
echo " Best model: saved by eval_loss"
echo "========================================="
echo ""
echo "Start time: $(date)"
echo ""

uv run python -m neuroagent.training.train_grpo \
    --stage sft \
    --model Qwen/Qwen3.5-9B \
    --data "$TRAINING_DATA_ROOT/gold_trajectories_v5/trajectories.jsonl" \
    --output "$CHECKPOINTS_ROOT/sft_769" \
    --lora-rank 64 \
    --lora-alpha 128 \
    --epochs 5 \
    --batch-size 1 \
    --top-fraction 1.0 \
    --splits-dir data/neurobench_v4/splits \
    --fold 0 \
    --qlora

echo ""
echo "========================================="
echo " SFT Training Complete"
echo " Checkpoint: $CHECKPOINTS_ROOT/sft_769"
echo " End time: $(date)"
echo "========================================="
