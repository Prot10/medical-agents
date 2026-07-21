#!/usr/bin/env bash
# Helper script to serve models with vLLM for NeuroAgent evaluation.
# Usage: ./serve_model.sh [model_name] [port]
#
# Supported models:
#   qwen3.5-4b           - Qwen3.5-4B bf16 (smallest, fast iteration)
#   qwen3.5-9b           - Qwen3.5-9B bf16 (DEFAULT — fast, good tool calling)
#   qwen3.5-27b-awq      - Qwen3.5-27B AWQ via Marlin kernels (best Qwen quality)
#   medgemma-4b          - MedGemma-1.5-4B-IT bf16 (medical specialist, fast) [GATED]
#   medgemma-27b         - MedGemma-27B-Text-IT FP8 (medical specialist, best quality)
#   nemotron-nano-9b-v2  - NVIDIA Nemotron-Nano-9B-v2 (hybrid Mamba/Transformer)
#   nemotron-3-nano-4b   - NVIDIA Nemotron-3-Nano-4B BF16 (latest gen, smallest)
#   gemma-4-e2b          - Gemma 4 E2B (5B total / 2B effective, PLE)
#   gemma-4-e4b          - Gemma 4 E4B (8B total / 4B effective, PLE)
#   gemma-4-12b          - Gemma 4 12B (encoder-free multimodal dense)
#
# Performance notes:
#   - AWQ models use awq_marlin kernels (10x faster than plain awq GEMM)
#   - Thinking mode is ENABLED for Qwen3.5 — reasons in <think> blocks;
#     the reasoning-parser separates thinking from visible output
#   - --language-model-only disables the vision encoder (text-only, saves VRAM)
#   - Prefix caching enabled for repeated system prompts
#   - CUDA graphs enabled (default) — first run takes 1-3 min to compile
#   - Weights default to EOS — cold load ~3-7 min on EOS vs ~40s on local NVMe

set -euo pipefail

# Fix for driver/library version mismatch on some RHEL/CentOS systems
export CUDA_MODULE_LOADING=LAZY

# Models live on EOS by default (~100 GB of weights staged there).
# Override by exporting HF_HOME before invoking this script if you want to use
# a local cache. See benchmark in commit history for cold/warm load times.
export HF_HOME="${HF_HOME:-/eos/project-d/diagbox/dvc/NeuroAgent/models/base/huggingface}"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VLLM_VENV="${VLLM_VENV:-$REPO_ROOT/.venv-vllm}"
MODEL="${1:-qwen3.5-9b}"
PORT="${2:-8000}"

# vLLM 0.23+ spawns engine subprocesses that shell out to 'ninja' for build
# steps; without prepending the venv's bin to PATH, the engine fails with
# FileNotFoundError: 'ninja'.
export PATH="$VLLM_VENV/bin:$PATH"

# Use patched launcher to work around NVML/driver version mismatch
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VLLM="$VLLM_VENV/bin/python $SCRIPT_DIR/vllm_serve.py"

# Common optimized flags for single-GPU A100-40GB
# GPU_MEMORY_UTILIZATION env var allows manual GPU memory partitioning
GPU_MEM="${GPU_MEMORY_UTILIZATION:-0.95}"
# Concurrent sequences the engine will batch. 4 suits the interactive dashboard (one agent at a
# time, lowest latency); batch evaluation raises it via MAX_NUM_SEQS so many cases run at once.
COMMON_FLAGS=(
  --port "$PORT"
  --gpu-memory-utilization "$GPU_MEM"
  --dtype auto
  --max-num-seqs "${MAX_NUM_SEQS:-4}"
)
# Prefix caching is a big speed win (the ~6k prompt is shared across an agent's turns), but vLLM
# flags it as EXPERIMENTAL for Qwen3.5's GDN/Mamba linear-attention layers. On by default;
# NO_PREFIX_CACHING=1 disables it when a reported benchmark must not depend on that path.
if [ "${NO_PREFIX_CACHING:-0}" = 1 ]; then
  echo "Prefix caching DISABLED (NO_PREFIX_CACHING=1)"
else
  COMMON_FLAGS+=(--enable-prefix-caching)
fi

# Train/serve parity for multi-turn GRPO. Qwen3.5's shipped template is an INFERENCE template:
# it strips <think> from any assistant turn a user message follows, so with reflection enabled
# the agent loses its own reasoning from context. Multi-turn training renders with TRL's
# think-preserving TRAINING template, and evaluating a policy under a different template than
# it was trained on reintroduces exactly the train/serve mismatch that made the first GRPO runs
# look flat. Export it with `python -m neuroagent.training.export_chat_template` and point
# CHAT_TEMPLATE at the file.
if [ -n "${CHAT_TEMPLATE:-}" ]; then
  [ -f "$CHAT_TEMPLATE" ] || { echo "CHAT_TEMPLATE set but not found: $CHAT_TEMPLATE" >&2; exit 1; }
  COMMON_FLAGS+=(--chat-template "$CHAT_TEMPLATE")
fi

# Qwen3.5-specific flags: reasoning parser + tool calling + text-only
QWEN35_FLAGS=(
  --reasoning-parser qwen3
  --enable-auto-tool-choice
  --tool-call-parser qwen3_coder
  --language-model-only
)

# Optional LoRA adapter. Set LORA_ADAPTER=/path/to/adapter to serve base + adapter from one
# process: requests with model="<base>" hit the base weights, model="sft" hit the adapter.
# Avoids merging a full fine-tuned model (no 18GB write, no slow reload) — the base loads
# from RAM and only the ~300MB adapter comes off EOS.
if [ -n "${LORA_ADAPTER:-}" ]; then
  QWEN35_FLAGS+=(
    --enable-lora
    --lora-modules "sft=$LORA_ADAPTER"
    --max-lora-rank "${MAX_LORA_RANK:-64}"
  )
  echo "Serving with LoRA adapter 'sft' = $LORA_ADAPTER"
fi

echo "Starting vLLM server for model: $MODEL on port $PORT"

case "$MODEL" in
  qwen3.5-4b)
    # Qwen3.5-4B bf16 — same architecture/flags as 9B, smaller weights.
    $VLLM \
      --model Qwen/Qwen3.5-4B \
      "${COMMON_FLAGS[@]}" \
      "${QWEN35_FLAGS[@]}" \
      --max-model-len 131072
    ;;
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
  nemotron-nano-9b-v2)
    # NVIDIA Nemotron-Nano-9B-v2 — hybrid Mamba/Transformer architecture.
    # Native function calling via NVIDIA's custom parser plugin (vendored +
    # patched for vLLM 0.17.1 — see nemotron_toolcall_parser.py). Verified
    # end-to-end: emits structured tool_calls in `<TOOLCALL>` JSON format.
    $VLLM \
      --model nvidia/NVIDIA-Nemotron-Nano-9B-v2 \
      "${COMMON_FLAGS[@]}" \
      --max-model-len 65536 \
      --trust-remote-code \
      --mamba-ssm-cache-dtype float32 \
      --enable-auto-tool-choice \
      --tool-parser-plugin "$SCRIPT_DIR/nemotron_toolcall_parser.py" \
      --tool-call-parser nemotron_json
    ;;
  nemotron-3-nano-4b)
    # NVIDIA Nemotron-3-Nano-4B-BF16 — latest Nemotron gen, smallest variant.
    # Per NVIDIA model card: native tool calling via Qwen3-coder parser +
    # custom nano_v3 reasoning parser (NOT the TOOLCALL/json scheme used by
    # Nemotron-Nano-9B-v2). The reasoning plugin is vendored alongside.
    $VLLM \
      --model nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16 \
      "${COMMON_FLAGS[@]}" \
      --max-model-len 65536 \
      --trust-remote-code \
      --enable-auto-tool-choice \
      --tool-call-parser qwen3_coder \
      --reasoning-parser-plugin "$SCRIPT_DIR/nano_v3_reasoning_parser.py" \
      --reasoning-parser nano_v3
    ;;
  gemma-4-e2b)
    # Google Gemma 4 E2B — 5B total / 2B effective parameters via Per-Layer
    # Embeddings (PLE). Native function calling via vLLM's built-in gemma4
    # tool/reasoning parsers (added in 0.23.0). Multimodal (text+image+audio).
    $VLLM \
      --model google/gemma-4-E2B-it \
      "${COMMON_FLAGS[@]}" \
      --max-model-len 32768 \
      --enable-auto-tool-choice \
      --tool-call-parser gemma4 \
      --reasoning-parser gemma4
    ;;
  gemma-4-e4b)
    # Gemma 4 E4B — 8B total / 4B effective (PLE). Same as E2B but bigger.
    $VLLM \
      --model google/gemma-4-E4B-it \
      "${COMMON_FLAGS[@]}" \
      --max-model-len 32768 \
      --enable-auto-tool-choice \
      --tool-call-parser gemma4 \
      --reasoning-parser gemma4
    ;;
  gemma-4-12b)
    # Gemma 4 12B — encoder-free dense multimodal. 24 GB BF16, fits A100-40GB.
    $VLLM \
      --model google/gemma-4-12B-it \
      "${COMMON_FLAGS[@]}" \
      --max-model-len 32768 \
      --enable-auto-tool-choice \
      --tool-call-parser gemma4 \
      --reasoning-parser gemma4
    ;;
  *)
    # If MODEL is a path to a local model directory, serve it with Qwen3.5 flags
    if [ -d "$MODEL" ] || [ -d "$(pwd)/$MODEL" ]; then
      echo "Serving local model: $MODEL"
      $VLLM \
        --model "$MODEL" \
        "${COMMON_FLAGS[@]}" \
        "${QWEN35_FLAGS[@]}" \
        --max-model-len 131072 \
        --trust-remote-code
    else
      echo "Unknown model: $MODEL"
      echo "Supported: qwen3.5-4b, qwen3.5-9b, qwen3.5-27b-awq,"
      echo "           medgemma-4b, medgemma-27b,"
      echo "           nemotron-nano-9b-v2, nemotron-3-nano-4b,"
      echo "           gemma-4-e2b, gemma-4-e4b, gemma-4-12b"
      echo "Or pass a path to a local model directory."
      exit 1
    fi
    ;;
esac
