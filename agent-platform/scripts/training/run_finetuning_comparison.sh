#!/bin/bash
# End-to-end fine-tuning comparison pipeline for NeuroAgent
# Runs: SFT → GRPO → DAPO on Qwen3.5-9B with QLoRA
# Hardware: Single A100-40GB
set -euo pipefail

# === Configuration ===
MODEL="Qwen/Qwen3.5-9B"
DATASET="data/neurobench"
# Where generated training data lives. Defaults to EOS; override for local.
TRAINING_DATA_ROOT="${TRAINING_DATA_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent/training_data}"
TRAINING_DATA="$TRAINING_DATA_ROOT/gold_trajectories_v5"
# Where checkpoint adapters live. Defaults to EOS; override for local NVMe.
CHECKPOINTS="${CHECKPOINTS_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent/checkpoints}"
RESULTS="results/finetuning_comparison"

LORA_RANK=64
LORA_ALPHA=128
SFT_EPOCHS=3
GRPO_EPOCHS=15
DAPO_EPOCHS=10
BATCH_SIZE=2
NUM_GENERATIONS=4

# === Setup ===
mkdir -p "$CHECKPOINTS" "$RESULTS" "$TRAINING_DATA"

echo "========================================="
echo " NeuroAgent Fine-Tuning Pipeline"
echo " Model: $MODEL"
echo " Dataset: $DATASET"
echo " Hardware: QLoRA on single A100-40GB"
echo "========================================="

# === Phase 1: Data Preparation ===
echo ""
echo "[Phase 1] Preparing data..."

# 1.1 Generate prompts for gold trajectory generation
echo "  [1.1] Preparing trajectory prompts..."
uv run python -m neuroagent.training.data.generate_gold_trajectories \
    --dataset "$DATASET" \
    --output "$TRAINING_DATA" \
    --prepare-prompts

# 1.2 Generate k-fold splits
echo "  [1.2] Generating 5-fold splits..."
uv run python -m neuroagent.training.data.split_dataset \
    --dataset "$DATASET" \
    --k 5

echo "  [1.3] Gold trajectories must be generated via Claude Code subagent."
echo "  Check $TRAINING_DATA/manifest.json for prompts."
echo "  After generation, run: --validate to check them."

# Check if trajectories exist
if [ ! -f "$TRAINING_DATA/trajectories.jsonl" ]; then
    echo ""
    echo "  ⚠ No trajectories.jsonl found!"
    echo "  Generate gold trajectories first, then re-run this script."
    echo "  Skipping to evaluation of base model..."
    echo ""
fi

# === Phase 2: SFT ===
if [ -f "$TRAINING_DATA/trajectories.jsonl" ]; then
    echo ""
    echo "[Phase 2] SFT Training..."
    echo "  Config: QLoRA, rank=$LORA_RANK, alpha=$LORA_ALPHA, epochs=$SFT_EPOCHS"

    uv run python -m neuroagent.training.train_grpo \
        --stage sft \
        --model "$MODEL" \
        --data "$TRAINING_DATA/trajectories.jsonl" \
        --output "$CHECKPOINTS/sft_warmup" \
        --lora-rank "$LORA_RANK" \
        --lora-alpha "$LORA_ALPHA" \
        --epochs "$SFT_EPOCHS" \
        --batch-size "$BATCH_SIZE" \
        --qlora

    echo "  SFT checkpoint: $CHECKPOINTS/sft_warmup"
fi

# === Phase 3a: GRPO ===
if [ -d "$CHECKPOINTS/sft_warmup" ]; then
    echo ""
    echo "[Phase 3a] Collecting trajectories from SFT model..."
    uv run python -m neuroagent.training.data.prepare_trajectories \
        --dataset "$DATASET" \
        --output "$TRAINING_DATA/sft_trajectories.json" \
        --model-checkpoint "$CHECKPOINTS/sft_warmup" \
        --rollouts-per-case 8

    echo ""
    echo "[Phase 3a] Formatting for GRPO..."
    uv run python -m neuroagent.training.data.format_for_grpo \
        --input "$TRAINING_DATA/sft_trajectories.json" \
        --output "$TRAINING_DATA/grpo_dataset" \
        --mode full

    echo ""
    echo "[Phase 3a] GRPO Training (15 epochs with integrated curriculum)..."
    uv run python -m neuroagent.training.train_grpo \
        --stage grpo \
        --model "$CHECKPOINTS/sft_warmup" \
        --data "$TRAINING_DATA/grpo_dataset/train.jsonl" \
        --output "$CHECKPOINTS/grpo_final" \
        --lora-rank "$LORA_RANK" \
        --lora-alpha "$LORA_ALPHA" \
        --epochs "$GRPO_EPOCHS" \
        --batch-size 1 \
        --num-generations "$NUM_GENERATIONS" \
        --qlora

    echo "  GRPO checkpoint: $CHECKPOINTS/grpo_final"
fi

# === Phase 3b: DAPO ===
if [ -d "$CHECKPOINTS/sft_warmup" ] && [ -f "$TRAINING_DATA/grpo_dataset/train.jsonl" ]; then
    echo ""
    echo "[Phase 3b] DAPO Training (10 epochs, token-level loss)..."
    uv run python -m neuroagent.training.train_dapo \
        --model "$CHECKPOINTS/sft_warmup" \
        --data "$TRAINING_DATA/grpo_dataset/train.jsonl" \
        --output "$CHECKPOINTS/dapo_final" \
        --lora-rank "$LORA_RANK" \
        --lora-alpha "$LORA_ALPHA" \
        --epochs "$DAPO_EPOCHS" \
        --batch-size 1 \
        --num-generations "$NUM_GENERATIONS" \
        --qlora

    echo "  DAPO checkpoint: $CHECKPOINTS/dapo_final"
fi

# === Phase 4: Evaluation ===
echo ""
echo "[Phase 4] Evaluation..."

# Evaluate all model variants
for VARIANT in base sft grpo dapo; do
    case $VARIANT in
        base)   ADAPTER="" ;;
        sft)    ADAPTER="$CHECKPOINTS/sft_warmup" ;;
        grpo)   ADAPTER="$CHECKPOINTS/grpo_final" ;;
        dapo)   ADAPTER="$CHECKPOINTS/dapo_final" ;;
    esac

    if [ "$VARIANT" = "base" ] || [ -d "$ADAPTER" ]; then
        echo "  Evaluating: $VARIANT"
        ADAPTER_FLAG=""
        [ -n "$ADAPTER" ] && ADAPTER_FLAG="--adapter $ADAPTER"

        uv run python -m neuroagent.training.evaluate_finetuned \
            --base-model "$MODEL" \
            $ADAPTER_FLAG \
            --dataset "$DATASET" \
            --output "$RESULTS/${VARIANT}_eval.json" || true
    fi
done

echo ""
echo "========================================="
echo " Pipeline complete!"
echo " Results: $RESULTS/"
echo "========================================="
