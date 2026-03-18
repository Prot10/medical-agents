#!/usr/bin/env bash
# Helper script to serve models with vLLM for NeuroAgent evaluation.
# Usage: ./serve_model.sh [model_name] [port]
#
# Supported models:
#   qwen3.5-9b         - Qwen3.5-9B fp16 (DEFAULT — fast, good tool calling)
#   qwen3.5-27b-awq    - Qwen3.5-27B AWQ via Marlin kernels (best quality)
#   medgemma-4b         - MedGemma-1.5-4B-IT bf16 (medical specialist, fast)
#   medgemma-27b        - MedGemma-27B-Text-IT FP8 (medical specialist, best quality)
#
# Performance notes:
#   - AWQ models use awq_marlin kernels (10x faster than plain awq GEMM)
#   - Thinking mode is ENABLED for Qwen3.5 — reasons in <think> blocks;
#     the reasoning-parser separates thinking from visible output
#   - --language-model-only disables the vision encoder (text-only, saves VRAM)
#   - Prefix caching enabled for repeated system prompts
#   - CUDA graphs enabled (default) — first run takes 1-3 min to compile

set -euo pipefail

# Fix for driver/library version mismatch on some RHEL/CentOS systems
export CUDA_MODULE_LOADING=LAZY

# Use local disk for HuggingFace model cache
export HF_HOME="${HF_HOME:-/home/aprotani/.cache/huggingface}"

VLLM_VENV="${VLLM_VENV:-/home/aprotani/projects/medical-agents/.venv-vllm}"
MODEL="${1:-qwen3.5-9b}"
PORT="${2:-8000}"

# Use patched launcher to work around NVML/driver version mismatch
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VLLM="$VLLM_VENV/bin/python $SCRIPT_DIR/vllm_serve.py"

# Common optimized flags for single-GPU A100-40GB
# GPU_MEMORY_UTILIZATION env var allows dual-model serving (split GPU memory)
GPU_MEM="${GPU_MEMORY_UTILIZATION:-0.95}"
COMMON_FLAGS=(
  --port "$PORT"
  --gpu-memory-utilization "$GPU_MEM"
  --enable-prefix-caching
  --dtype auto
  --max-num-seqs 4
)

# Qwen3.5-specific flags: reasoning parser + tool calling + text-only
QWEN35_FLAGS=(
  --reasoning-parser qwen3
  --enable-auto-tool-choice
  --tool-call-parser qwen3_coder
  --language-model-only
)

echo "Starting vLLM server for model: $MODEL on port $PORT"

case "$MODEL" in
  qwen3.5-9b)
    $VLLM \
      --model Qwen/Qwen3.5-9B \
      "${COMMON_FLAGS[@]}" \
      "${QWEN35_FLAGS[@]}" \
      --max-model-len 131072
    ;;
  qwen3.5-27b-awq)
    # CRITICAL: use awq_marlin, NOT awq — Marlin kernels are ~10x faster
    $VLLM \
      --model QuantTrio/Qwen3.5-27B-AWQ \
      "${COMMON_FLAGS[@]}" \
      "${QWEN35_FLAGS[@]}" \
      --max-model-len 32768 \
      --quantization awq_marlin
    ;;
  medgemma-4b)
    # MedGemma 1.5 4B — Gemma 3 based, multimodal but we use text-only
    # 8.6 GB bf16, fits easily with plenty of KV cache room
    # Note: MedGemma does not support native tool calling; agent falls back
    # to text-only diagnosis without tool use
    $VLLM \
      --model google/medgemma-1.5-4b-it \
      "${COMMON_FLAGS[@]}" \
      --max-model-len 32768 \
      --enable-auto-tool-choice \
      --tool-call-parser hermes
    ;;
  medgemma-27b)
    # MedGemma 27B Text — Gemma 3 based, text-only, FP8 dynamic quantization
    # 27 GB in VRAM, ~8 GB for KV cache — limited to 8K context
    # Note: MedGemma does not support native tool calling
    $VLLM \
      --model ig1/medgemma-27b-text-it-FP8-Dynamic \
      "${COMMON_FLAGS[@]}" \
      --max-num-seqs 2 \
      --max-model-len 8192 \
      --enable-auto-tool-choice \
      --tool-call-parser hermes
    ;;
  *)
    echo "Unknown model: $MODEL"
    echo "Supported: qwen3.5-9b, qwen3.5-27b-awq, medgemma-4b, medgemma-27b"
    exit 1
    ;;
esac
