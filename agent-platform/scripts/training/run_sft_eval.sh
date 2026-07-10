#!/bin/bash
# Evaluate an SFT-finetuned Qwen3.5 against its base on the held-out 100-case TEST split.
#
# Run: bash agent-platform/scripts/training/run_sft_eval.sh [model_tag]
#   model_tag defaults to Qwen3.5-9B; pass Qwen3.5-4B for the small student.
#
# The test split is the 100 cases no gold trajectory was ever generated for, so this
# measures generalisation, not recall of training data. Base and SFT are each served in
# turn, evaluated with REPEATS samples per case, then compared.
set -euo pipefail
cd /home/aprotani/projects/medical-agents

MODEL_TAG="${1:-Qwen3.5-9B}"
SERVE_KEY="$(echo "$MODEL_TAG" | tr '[:upper:]' '[:lower:]')"   # qwen3.5-9b / qwen3.5-4b
BASE_MODEL="Qwen/$MODEL_TAG"

EOS_ROOT="${EOS_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent}"
CHECKPOINTS_ROOT="${CHECKPOINTS_ROOT:-$EOS_ROOT/checkpoints}"
ADAPTER="${ADAPTER:-$CHECKPOINTS_ROOT/sft_${MODEL_TAG}}"

# Same storage split as training: stage the base model into /dev/shm (RAM) for a fast load
# (reading it off EOS FUSE takes ~1-2h), and keep the finetuned merged model on EOS. Nothing
# large lands on local disk. (Future: skip the merge and serve base+adapter via vLLM's native
# LoRA support, avoiding the full-model write entirely.)
EOS_HF="$EOS_ROOT/models/base/huggingface"
SHM_HF="${SHM_HF:-/dev/shm/hf}"
MODEL_DIR="models--Qwen--$MODEL_TAG"
if [ ! -d "$SHM_HF/hub/$MODEL_DIR" ]; then
  echo "Staging $MODEL_TAG from EOS to $SHM_HF (RAM, one-time)..."
  mkdir -p "$SHM_HF/hub"
  cp -r "$EOS_HF/hub/$MODEL_DIR" "$SHM_HF/hub/" || { echo "ERROR: base not on EOS" >&2; exit 1; }
fi
export HF_HOME="$SHM_HF"
export HF_HUB_OFFLINE=1

RESULTS_DIR="${RESULTS_DIR:-results/sft_eval/${MODEL_TAG}}"
SPLIT="${SPLIT:-test}"
HOSPITAL="${HOSPITAL:-de_charite}"
REPEATS="${REPEATS:-3}"
PORT="${PORT:-8000}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export CUDA_MODULE_LOADING=LAZY
mkdir -p "$RESULTS_DIR"

# MODE selects what to evaluate. The weekend runner scores the base on the test set BEFORE
# training (base does not need the adapter), then the SFT model after — same split, same
# sampling, directly comparable.
#   base : serve base only, evaluate base            (run before training)
#   sft  : serve base + LoRA, evaluate the adapter   (run after training)
#   both : serve base + LoRA, evaluate both, compare (default, standalone use)
MODE="${MODE:-${2:-both}}"

echo "========================================="
echo " SFT Evaluation — $MODEL_TAG on $SPLIT split (mode: $MODE)"
echo " Base:    $BASE_MODEL (from RAM)"
[ "$MODE" != "base" ] && echo " Adapter: $ADAPTER (LoRA, from EOS — no merge)"
echo " Repeats: $REPEATS   Results: $RESULTS_DIR"
echo "========================================="

source "$SCRIPT_DIR/_gpu.sh"
_kill_vllm() { free_gpu "eval teardown"; }

_serve() {  # $1 = "base" (no adapter) or "lora" (base + adapter)
  _kill_vllm
  local ready_token="model"
  if [ "$1" = "lora" ]; then
    [ -f "$ADAPTER/adapter_model.safetensors" ] || { echo "ERROR: no adapter at $ADAPTER" >&2; return 1; }
    LORA_ADAPTER="$ADAPTER" bash "$SCRIPT_DIR/../runtime/serve_model.sh" "$SERVE_KEY" "$PORT" &
    ready_token='"sft"'
  else
    bash "$SCRIPT_DIR/../runtime/serve_model.sh" "$SERVE_KEY" "$PORT" &
  fi
  for _ in $(seq 1 180); do
    curl -s "http://localhost:$PORT/v1/models" | grep -q "$ready_token" && { echo "vLLM ready"; return 0; }
    sleep 5
  done
  echo "ERROR: vLLM did not become ready" >&2
  return 1
}

# -------- base (before training) --------
if [ "$MODE" = "base" ] || [ "$MODE" = "both" ]; then
  if [ ! -f "$RESULTS_DIR/base_results.json" ]; then
    echo "Evaluating BASE $MODEL_TAG on $SPLIT..."
    _serve base
    uv run python agent-platform/scripts/training/run_sft_eval_cases.py evaluate \
        --model-id "$BASE_MODEL" --run-name "base-$SERVE_KEY" --split "$SPLIT" \
        --hospital "$HOSPITAL" --repeats "$REPEATS" \
        --output "$RESULTS_DIR/base_results.json" --port "$PORT"
    _kill_vllm
  else
    echo "Base results exist, skipping."
  fi
fi

# -------- SFT (after training) --------
if [ "$MODE" = "sft" ] || [ "$MODE" = "both" ]; then
  if [ ! -f "$RESULTS_DIR/sft_results.json" ]; then
    echo "Evaluating SFT $MODEL_TAG (LoRA) on $SPLIT..."
    _serve lora
    uv run python agent-platform/scripts/training/run_sft_eval_cases.py evaluate \
        --model-id "sft" --run-name "sft-$SERVE_KEY" --split "$SPLIT" \
        --hospital "$HOSPITAL" --repeats "$REPEATS" \
        --output "$RESULTS_DIR/sft_results.json" --port "$PORT"
    _kill_vllm
  else
    echo "SFT results exist, skipping."
  fi
fi

# -------- compare (only once both halves exist) --------
if [ -f "$RESULTS_DIR/base_results.json" ] && [ -f "$RESULTS_DIR/sft_results.json" ]; then
  echo "Comparing base vs SFT..."
  uv run python agent-platform/scripts/training/run_sft_eval_cases.py compare \
      --base-results "$RESULTS_DIR/base_results.json" \
      --sft-results "$RESULTS_DIR/sft_results.json" \
      --output "$RESULTS_DIR/comparison.json"
fi

# Persist whatever exists to EOS alongside the checkpoint.
EOS_RESULTS="$EOS_ROOT/results/sft_eval/${MODEL_TAG}"
mkdir -p "$EOS_RESULTS"
cp -r "$RESULTS_DIR/." "$EOS_RESULTS/"

echo "========================================="
echo " Done. Results: $RESULTS_DIR  (copied to $EOS_RESULTS)"
echo "========================================="
