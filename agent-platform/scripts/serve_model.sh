#!/usr/bin/env bash
# Helper script to serve models with vLLM for NeuroAgent evaluation.
# Usage: ./serve_model.sh <model_name> [port]
#
# Supported models:
#   qwen3.5-27b-awq    - Qwen3.5-27B AWQ quantized (primary, best tool calling)
#   qwen3.5-27b-fp8    - Qwen3.5-27B FP8 (higher quality, needs more VRAM)
#   medgemma-27b        - MedGemma-27B-Text-IT GGUF Q4 (medical specialist)
#   medgemma-4b         - MedGemma-1.5-4B-IT (fast medical, good for iteration)
#   openbio-8b          - OpenBioLLM-8B (fast medical baseline)

set -euo pipefail

# Fix for driver/library version mismatch on some RHEL/CentOS systems
export CUDA_MODULE_LOADING=LAZY

# Use local disk for HuggingFace model cache
export HF_HOME="${HF_HOME:-/home/aprotani/.cache/huggingface}"

VLLM_VENV="${VLLM_VENV:-/home/aprotani/projects/medical-agents/.venv-vllm}"
MODEL="${1:-qwen3.5-27b-awq}"
PORT="${2:-8000}"

# Use patched launcher to work around NVML/driver version mismatch
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VLLM="$VLLM_VENV/bin/python $SCRIPT_DIR/vllm_serve.py"

echo "Starting vLLM server for model: $MODEL on port $PORT"

case "$MODEL" in
  qwen3.5-27b-awq)
    $VLLM \
      --model QuantTrio/Qwen3.5-27B-AWQ \
      --port "$PORT" \
      --max-model-len 32768 \
      --enable-auto-tool-choice \
      --tool-call-parser qwen3_coder \
      --gpu-memory-utilization 0.90 \
      --quantization awq
    ;;
  qwen3.5-27b-fp8)
    $VLLM \
      --model Qwen/Qwen3.5-27B-FP8 \
      --port "$PORT" \
      --max-model-len 16384 \
      --enable-auto-tool-choice \
      --tool-call-parser qwen3_coder \
      --gpu-memory-utilization 0.95
    ;;
  medgemma-27b)
    $VLLM \
      --model unsloth/medgemma-27b-text-it-GGUF:Q4_K_M \
      --port "$PORT" \
      --max-model-len 32768 \
      --tokenizer google/medgemma-27b-text-it \
      --gpu-memory-utilization 0.90
    ;;
  medgemma-4b)
    $VLLM \
      --model google/medgemma-1.5-4b-it \
      --port "$PORT" \
      --max-model-len 32768 \
      --gpu-memory-utilization 0.90
    ;;
  openbio-8b)
    $VLLM \
      --model aaditya/Llama3-OpenBioLLM-8B \
      --port "$PORT" \
      --max-model-len 32768 \
      --enable-auto-tool-choice \
      --tool-call-parser hermes \
      --gpu-memory-utilization 0.90
    ;;
  *)
    echo "Unknown model: $MODEL"
    echo "Supported: qwen3.5-27b-awq, qwen3.5-27b-fp8, medgemma-27b, medgemma-4b, openbio-8b"
    exit 1
    ;;
esac
