#!/bin/bash
# DPO Training Pipeline: collect → pairs → train
# Decouples generation (vLLM) from training (QLoRA) to fit A100-40GB
#
# Run: bash agent-platform/scripts/run_dpo_training.sh
set -euo pipefail
cd /home/aprotani/projects/medical-agents

# Where checkpoint adapters live. Defaults to EOS; override for local NVMe.
CHECKPOINTS_ROOT="${CHECKPOINTS_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent/checkpoints}"
mkdir -p "$CHECKPOINTS_ROOT"

# Where generated training data lives. Defaults to EOS; override for local.
TRAINING_DATA_ROOT="${TRAINING_DATA_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent/training_data}"
mkdir -p "$TRAINING_DATA_ROOT"

export CUDA_MODULE_LOADING=LAZY
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SFT_MODEL="/home/aprotani/projects/medical-agents/models/qwen3.5-9b-sft769"
SFT_ADAPTER="$CHECKPOINTS_ROOT/sft_769/checkpoint-272"
SFT_MERGED="/home/aprotani/projects/medical-agents/models/qwen3.5-9b-sft769"
DATASET="data/neurobench_v4"
SPLIT_FILE="$DATASET/splits/fold0_train.txt"
TRAJECTORIES="$TRAINING_DATA_ROOT/dpo_trajectories.json"
PAIRS="$TRAINING_DATA_ROOT/dpo_pairs.json"
OUTPUT="$CHECKPOINTS_ROOT/dpo_from_sft"
ROLLOUTS=8
HOSPITAL="de_charite"
PORT=8000

echo "========================================="
echo " DPO Training Pipeline"
echo " Step 1: Collect $ROLLOUTS rollouts × 140 cases via vLLM"
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

    pkill -f "vllm_serve.py" || true
    pkill -f "VLLM::EngineCore" || true
    sleep 5

    echo "Starting vLLM with SFT model..."
    bash "$SCRIPT_DIR/serve_model.sh" "$SFT_MODEL" "$PORT" &
    VLLM_PID=$!

    echo "Waiting for vLLM..."
    for i in $(seq 1 120); do
        if curl -s "http://localhost:$PORT/v1/models" 2>/dev/null | grep -q "model"; then
            echo "vLLM ready after $((i*5))s"
            break
        fi
        sleep 5
    done

    uv run python -m neuroagent.training.train_dpo collect \
        --model "$SFT_MODEL" \
        --dataset "$DATASET" \
        --split-file "$SPLIT_FILE" \
        --output "$TRAJECTORIES" \
        --rollouts "$ROLLOUTS" \
        --hospital "$HOSPITAL" \
        --base-url "http://localhost:$PORT/v1"

    kill "$VLLM_PID" 2>/dev/null || true
    pkill -f "vllm_serve.py" || true
    pkill -f "VLLM::EngineCore" || true
    sleep 5
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
