#!/usr/bin/env bash
# Serve one preregistered under-10B benchmark model with vLLM.
# Usage: ./serve_model.sh [qwen3.5-9b|granite-4.1-8b|gemma-4-e4b] [port]
#
# Environment:
#   HF_HOME                  model cache (default: the EOS cache; stage it in /dev/shm for fast loads)
#   VLLM_VENV                isolated vLLM virtualenv (default: <repo>/.venv-vllm)
#   GPU_MEMORY_UTILIZATION   default 0.90
#   MAX_NUM_SEQS             default 16 (the KV cache on an A100-40GB fits ~15 full-length requests;
#                            output throughput on Qwen3.5-9B: 60 tok/s at 1, 365 at 8, 450 at 16)
#   LORA_ADAPTER             PEFT adapter directory to expose next to the base model
#   LORA_NAME                served name of that adapter (default: sft); a profile selects it with
#                            `served_model: <name>` on its model plugin, and episodes record it as
#                            the model identifier
#
# Thinking is left to the request: every request from the harness sends
# chat_template_kwargs.enable_thinking=false (see model_registry.request_defaults).

set -euo pipefail

export CUDA_MODULE_LOADING=LAZY
export HF_HOME="${HF_HOME:-/eos/project-d/diagbox/dvc/aprotani/models/hf}"
# Tool-call syntax is sampled freely, not grammar-constrained (the default flipped to strict in
# vLLM 0.26). GRPO rollouts pin the same value so training and serving sample the same way.
export VLLM_ENFORCE_STRICT_TOOL_CALLING=0

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VLLM_VENV="${VLLM_VENV:-$REPO_ROOT/.venv-vllm}"
MODEL="${1:-qwen3.5-9b}"
PORT="${2:-8000}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VLLM=("$VLLM_VENV/bin/python" "$SCRIPT_DIR/vllm_serve.py")

export PATH="$VLLM_VENV/bin:$PATH"

COMMON_FLAGS=(
  --port "$PORT"
  --gpu-memory-utilization "${GPU_MEMORY_UTILIZATION:-0.90}"
  --dtype auto
  --max-num-seqs "${MAX_NUM_SEQS:-16}"
  --max-model-len 32768
  --enable-prefix-caching
)

if [ -n "${LORA_ADAPTER:-}" ]; then
  [ -f "$LORA_ADAPTER/adapter_config.json" ] || {
    echo "LORA_ADAPTER is not a PEFT adapter directory: $LORA_ADAPTER" >&2
    exit 1
  }
  COMMON_FLAGS+=(
    --enable-lora
    --lora-modules "${LORA_NAME:-sft}=$LORA_ADAPTER"
    --max-lora-rank "${MAX_LORA_RANK:-64}"
  )
fi

case "$MODEL" in
  qwen3.5-9b)
    # The model card's MTP speculative decoding is lossless and measured 60 -> 80 output tok/s
    # single-stream (TPOT 14.2 -> 8.5 ms, 76% draft acceptance on tool-call output); it needs
    # `ninja` in the vLLM venv for the JIT kernels.
    "${VLLM[@]}" \
      --model Qwen/Qwen3.5-9B \
      "${COMMON_FLAGS[@]}" \
      --language-model-only \
      --enable-auto-tool-choice \
      --tool-call-parser qwen3_coder \
      --speculative-config '{"method":"qwen3_next_mtp","num_speculative_tokens":2}'
    ;;
  gemma-4-e4b)
    "${VLLM[@]}" \
      --model google/gemma-4-E4B-it \
      "${COMMON_FLAGS[@]}" \
      --language-model-only \
      --enable-auto-tool-choice \
      --tool-call-parser gemma4
    ;;
  granite-4.1-8b)
    "${VLLM[@]}" \
      --model ibm-granite/granite-4.1-8b \
      "${COMMON_FLAGS[@]}" \
      --enable-auto-tool-choice \
      --tool-call-parser granite4
    ;;
  *)
    echo "Unknown model: $MODEL" >&2
    echo "Supported: qwen3.5-9b, granite-4.1-8b, gemma-4-e4b" >&2
    exit 1
    ;;
esac
