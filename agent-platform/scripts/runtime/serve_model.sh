#!/usr/bin/env bash
# Serve one preregistered under-10B benchmark model with vLLM.
# Usage: ./serve_model.sh [qwen3.5-9b|gemma-4-e4b|medgemma-1.5-4b] [port]

set -euo pipefail

export CUDA_MODULE_LOADING=LAZY
export HF_HOME="${HF_HOME:-/eos/project-d/diagbox/dvc/NeuroAgent/models/base/huggingface}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VLLM_VENV="${VLLM_VENV:-$REPO_ROOT/.venv-vllm}"
MODEL="${1:-qwen3.5-9b}"
PORT="${2:-8000}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VLLM=("$VLLM_VENV/bin/python" "$SCRIPT_DIR/vllm_serve.py")

export PATH="$VLLM_VENV/bin:$PATH"

COMMON_FLAGS=(
  --port "$PORT"
  --gpu-memory-utilization "${GPU_MEMORY_UTILIZATION:-0.95}"
  --dtype auto
  --max-num-seqs "${MAX_NUM_SEQS:-4}"
)

if [ "${NO_PREFIX_CACHING:-0}" != 1 ]; then
  COMMON_FLAGS+=(--enable-prefix-caching)
fi

if [ -n "${LORA_ADAPTER:-}" ]; then
  [ -f "$LORA_ADAPTER/adapter_config.json" ] || {
    echo "LORA_ADAPTER is not a PEFT adapter directory: $LORA_ADAPTER" >&2
    exit 1
  }
  COMMON_FLAGS+=(
    --enable-lora
    --lora-modules "sft=$LORA_ADAPTER"
    --max-lora-rank "${MAX_LORA_RANK:-64}"
  )
fi

case "$MODEL" in
  qwen3.5-9b)
    "${VLLM[@]}" \
      --model Qwen/Qwen3.5-9B \
      "${COMMON_FLAGS[@]}" \
      --max-model-len 32768 \
      --language-model-only \
      --enable-auto-tool-choice \
      --tool-call-parser qwen3_coder
    ;;
  gemma-4-e4b)
    "${VLLM[@]}" \
      --model google/gemma-4-E4B-it \
      "${COMMON_FLAGS[@]}" \
      --max-model-len 32768 \
      --enable-auto-tool-choice \
      --tool-call-parser gemma4
    ;;
  medgemma-1.5-4b)
    "${VLLM[@]}" \
      --model google/medgemma-1.5-4b-it \
      "${COMMON_FLAGS[@]}" \
      --max-model-len 32768
    ;;
  *)
    echo "Unknown model: $MODEL" >&2
    echo "Supported: qwen3.5-9b, gemma-4-e4b, medgemma-1.5-4b" >&2
    exit 1
    ;;
esac
