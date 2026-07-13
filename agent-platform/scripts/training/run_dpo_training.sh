#!/bin/bash
# DPO Training Pipeline: collect → pairs → train
# Decouples generation (vLLM) from training (QLoRA) to fit A100-40GB
#
# Run: bash agent-platform/scripts/training/run_dpo_training.sh
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"  # repo root

# Where checkpoint adapters live. Defaults to EOS; override for local NVMe.
CHECKPOINTS_ROOT="${CHECKPOINTS_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent/checkpoints}"
mkdir -p "$CHECKPOINTS_ROOT"

# Where generated training data lives. Defaults to EOS; override for local.
TRAINING_DATA_ROOT="${TRAINING_DATA_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent/training_data}"
mkdir -p "$TRAINING_DATA_ROOT"

export CUDA_MODULE_LOADING=LAZY
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODEL_TAG="${MODEL_TAG:-Qwen3.5-9B}"
BASE_MODEL="Qwen/$MODEL_TAG"
SERVE_KEY="$(echo "$MODEL_TAG" | tr '[:upper:]' '[:lower:]')"
# SFT adapter written by run_sft_training.sh; served as LoRA for rollout collection.
SFT_ADAPTER="${SFT_ADAPTER:-$CHECKPOINTS_ROOT/sft_${MODEL_TAG}}"
# Merged SFT model (base + adapter) — DPO needs full weights: policy init + frozen reference.
SFT_MERGED="${SFT_MERGED:-models/${SERVE_KEY}-sft-merged}"
DATASET="data/neurobench"
SPLIT_FILE="$DATASET/splits/train_cases.txt"   # v5 train split; test stays held out
TRAJECTORIES="$TRAINING_DATA_ROOT/dpo_trajectories.json"
PAIRS="$TRAINING_DATA_ROOT/dpo_pairs.json"
OUTPUT="$CHECKPOINTS_ROOT/dpo_from_sft_${MODEL_TAG}"
ROLLOUTS=8
HOSPITAL="de_charite"
PORT=8000

# Stage base weights into /dev/shm (RAM) — EOS FUSE reads are too slow for a full model.
source "$SCRIPT_DIR/_stage.sh"
source "$SCRIPT_DIR/_gpu.sh"
stage_base "$BASE_MODEL" || exit 1

if [ ! -f "$SFT_ADAPTER/adapter_model.safetensors" ]; then
    echo "ERROR: no SFT adapter at $SFT_ADAPTER — run run_sft_training.sh first" >&2
    exit 1
fi

echo "========================================="
echo " DPO Training Pipeline — $MODEL_TAG"
echo " Step 1: Collect $ROLLOUTS rollouts × $(wc -l < "$SPLIT_FILE") train cases via vLLM"
echo " Step 2: Build preference pairs"
echo " Step 3: Train DPO (3 epochs, max_length=3584)"
echo " Start: $(date)"
echo "========================================="

# -------------------------------------------------------
# Step 1: Collect trajectories via vLLM
# -------------------------------------------------------
if [ ! -f "$TRAJECTORIES" ]; then
    echo ""
    echo "[Step 1/3] Collecting trajectories..."

    free_gpu "before serving" || true

    echo "Starting vLLM (base + SFT LoRA served as 'sft')..."
    LORA_ADAPTER="$SFT_ADAPTER" bash "$SCRIPT_DIR/../runtime/serve_model.sh" "$SERVE_KEY" "$PORT" &

    echo "Waiting for vLLM..."
    for i in $(seq 1 180); do
        if curl -s "http://localhost:$PORT/v1/models" 2>/dev/null | grep -q '"sft"'; then
            echo "vLLM ready after $((i*5))s"
            break
        fi
        sleep 5
    done

    uv run python -m neuroagent.training.train_dpo collect \
        --model sft \
        --dataset "$DATASET" \
        --split-file "$SPLIT_FILE" \
        --output "$TRAJECTORIES" \
        --rollouts "$ROLLOUTS" \
        --hospital "$HOSPITAL" \
        --base-url "http://localhost:$PORT/v1"

    free_gpu "rollouts done" || true
    echo "Trajectories saved to $TRAJECTORIES"
else
    echo "[Step 1/3] Trajectories already exist at $TRAJECTORIES, skipping."
fi

# -------------------------------------------------------
# Step 2: Build DPO preference pairs
# -------------------------------------------------------
if [ ! -f "$PAIRS" ]; then
    echo ""
    echo "[Step 2/3] Building DPO pairs..."
    uv run python -m neuroagent.training.train_dpo pairs \
        --trajectories "$TRAJECTORIES" \
        --output "$PAIRS" \
        --min-reward-gap 0.05
    echo "Pairs saved to $PAIRS"
else
    echo "[Step 2/3] Pairs already exist at $PAIRS, skipping."
fi

# -------------------------------------------------------
# Step 3: DPO Training
# -------------------------------------------------------
echo ""
echo "[Step 3/3] DPO Training..."
# Merge the SFT adapter into the base once — DPO trains from full SFT weights.
if [ ! -d "$SFT_MERGED" ]; then
    echo "Merging SFT adapter into base -> $SFT_MERGED ..."
    uv run python -m neuroagent.training.merge_adapter \
        --base-model "$BASE_MODEL" \
        --adapter "$SFT_ADAPTER" \
        --output "$SFT_MERGED"
fi
# Use merged SFT model as base so that:
# - Reference model = frozen SFT weights (correct for preference learning)
# - Policy model = SFT + fresh rsLoRA adapter
# Using rsLoRA (alpha/sqrt(r)) for stable high-rank DPO training
uv run python -m neuroagent.training.train_dpo train \
    --model "$SFT_MERGED" \
    --pairs "$PAIRS" \
    --output "$OUTPUT" \
    --epochs 3 \
    --batch-size 1 \
    --lr 5e-7 \
    --beta 0.1 \
    --max-length 3584 \
    --qlora

echo ""
echo "========================================="
echo " DPO Training Complete"
echo " Checkpoint: $OUTPUT"
echo " End: $(date)"
echo "========================================="
