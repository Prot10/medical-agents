#!/bin/bash
# Evaluate SFT-finetuned Qwen3.5-9B vs base on fold0 validation set (60 cases).
#
# Steps:
#   1. Merge LoRA adapter into base model
#   2. Run base model eval on fold0 val (60 cases, 3 repeats)
#   3. Run SFT model eval on fold0 val (60 cases, 3 repeats)
#   4. Compare results
#
# Prerequisites: GPU available, vLLM venv at $VLLM_VENV
# Run: bash agent-platform/scripts/run_sft_eval.sh
set -euo pipefail
cd /home/aprotani/projects/medical-agents

# Where checkpoint adapters live. Defaults to EOS; override for local NVMe.
CHECKPOINTS_ROOT="${CHECKPOINTS_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent/checkpoints}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ADAPTER="$CHECKPOINTS_ROOT/sft_769/checkpoint-272"
MERGED_MODEL="models/qwen3.5-9b-sft769"
BASE_MODEL="Qwen/Qwen3.5-9B"
RESULTS_DIR="results/sft_eval"
HOSPITAL="de_charite"
REPEATS=3
PORT=8000

export CUDA_MODULE_LOADING=LAZY

echo "========================================="
echo " SFT Evaluation — fold0 val (60 cases)"
echo " Base:  $BASE_MODEL"
echo " SFT:   $ADAPTER"
echo " Repeats: $REPEATS"
echo "========================================="

mkdir -p "$RESULTS_DIR"

# -------------------------------------------------------
# Step 1: Merge adapter (if not already done)
# -------------------------------------------------------
if [ ! -f "$MERGED_MODEL/config.json" ]; then
    echo ""
    echo "[Step 1/4] Merging LoRA adapter into base model..."
    uv run python -m neuroagent.training.merge_adapter \
        --base-model "$BASE_MODEL" \
        --adapter "$ADAPTER" \
        --output "$MERGED_MODEL"
    echo "Merged model saved to $MERGED_MODEL"
else
    echo "[Step 1/4] Merged model already exists at $MERGED_MODEL, skipping."
fi

# -------------------------------------------------------
# Step 2: Evaluate BASE model on fold0 val
# -------------------------------------------------------
if [ ! -f "$RESULTS_DIR/base_results.json" ]; then
    echo ""
    echo "[Step 2/4] Evaluating BASE Qwen3.5-9B on fold0 val..."

    # Kill any existing vLLM
    pkill -f "vllm_serve.py" || true
    pkill -f "VLLM::EngineCore" || true
    sleep 5

    # Start base model server
    echo "Starting vLLM for base model..."
    bash "$SCRIPT_DIR/serve_model.sh" qwen3.5-9b "$PORT" &
    VLLM_PID=$!

    # Wait for server to be ready
    echo "Waiting for vLLM server..."
    for i in $(seq 1 120); do
        if curl -s "http://localhost:$PORT/v1/models" | grep -q "model"; then
            echo "vLLM ready after ${i}s"
            break
        fi
        sleep 5
    done

    # Run evaluation
    uv run python agent-platform/scripts/run_sft_eval_cases.py evaluate \
        --model-id "$BASE_MODEL" \
        --run-name "base-qwen3.5-9b" \
        --hospital "$HOSPITAL" \
        --repeats "$REPEATS" \
        --output "$RESULTS_DIR/base_results.json" \
        --port "$PORT"

    # Stop server
    kill "$VLLM_PID" 2>/dev/null || true
    pkill -f "vllm_serve.py" || true
    pkill -f "VLLM::EngineCore" || true
    sleep 5
else
    echo "[Step 2/4] Base results already exist, skipping."
fi

# -------------------------------------------------------
# Step 3: Evaluate SFT model on fold0 val
# -------------------------------------------------------
if [ ! -f "$RESULTS_DIR/sft_results.json" ]; then
    echo ""
    echo "[Step 3/4] Evaluating SFT model on fold0 val..."

    # Kill any existing vLLM
    pkill -f "vllm_serve.py" || true
    pkill -f "VLLM::EngineCore" || true
    sleep 5

    # Start SFT model server (merged weights, same flags as base)
    echo "Starting vLLM for SFT model..."
    MERGED_ABS="$(cd /home/aprotani/projects/medical-agents && pwd)/$MERGED_MODEL"
    bash "$SCRIPT_DIR/serve_model.sh" "$MERGED_ABS" "$PORT" &
    VLLM_PID=$!

    # Wait for server
    echo "Waiting for vLLM server..."
    for i in $(seq 1 120); do
        if curl -s "http://localhost:$PORT/v1/models" | grep -q "model"; then
            echo "vLLM ready after ${i}s"
            break
        fi
        sleep 5
    done

    # Run evaluation — model-id must match what vLLM reports (absolute path)
    uv run python agent-platform/scripts/run_sft_eval_cases.py evaluate \
        --model-id "$MERGED_ABS" \
        --run-name "sft-qwen3.5-9b" \
        --hospital "$HOSPITAL" \
        --repeats "$REPEATS" \
        --output "$RESULTS_DIR/sft_results.json" \
        --port "$PORT"

    # Stop server
    kill "$VLLM_PID" 2>/dev/null || true
    pkill -f "vllm_serve.py" || true
    pkill -f "VLLM::EngineCore" || true
    sleep 5
else
    echo "[Step 3/4] SFT results already exist, skipping."
fi

# -------------------------------------------------------
# Step 4: Compare results
# -------------------------------------------------------
echo ""
echo "[Step 4/4] Comparing results..."
uv run python agent-platform/scripts/run_sft_eval_cases.py compare \
    --base-results "$RESULTS_DIR/base_results.json" \
    --sft-results "$RESULTS_DIR/sft_results.json" \
    --output "$RESULTS_DIR/comparison.json"

echo ""
echo "========================================="
echo " Evaluation complete!"
echo " Results: $RESULTS_DIR/"
echo "========================================="
