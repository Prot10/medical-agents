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
MERGED_MODEL="${MERGED_MODEL:-$EOS_ROOT/models/ft/qwen3.5-$(echo "$MODEL_TAG" | grep -oiE '[0-9]+b' | head -1 | tr '[:upper:]' '[:lower:]')-sft}"

RESULTS_DIR="${RESULTS_DIR:-results/sft_eval/${MODEL_TAG}}"
SPLIT="${SPLIT:-test}"
HOSPITAL="${HOSPITAL:-de_charite}"
REPEATS="${REPEATS:-3}"
PORT="${PORT:-8000}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export CUDA_MODULE_LOADING=LAZY
mkdir -p "$RESULTS_DIR"

echo "========================================="
echo " SFT Evaluation — $MODEL_TAG on $SPLIT split"
echo " Base:    $BASE_MODEL"
echo " Adapter: $ADAPTER"
echo " Repeats: $REPEATS"
echo " Results: $RESULTS_DIR"
echo "========================================="

_kill_vllm() {
  pkill -f "vllm_serve.py" 2>/dev/null || true
  pkill -f "VLLM::EngineCore" 2>/dev/null || true
  sleep 5
}

_serve_and_wait() {  # $1 = serve target (key or abs path)
  _kill_vllm
  bash "$SCRIPT_DIR/../runtime/serve_model.sh" "$1" "$PORT" &
  for _ in $(seq 1 120); do
    curl -s "http://localhost:$PORT/v1/models" | grep -q "model" && { echo "vLLM ready"; return 0; }
    sleep 5
  done
  echo "ERROR: vLLM did not become ready" >&2
  return 1
}

# -------- Step 1: merge adapter --------
if [ ! -f "$MERGED_MODEL/config.json" ]; then
  echo "[1/4] Merging adapter into base..."
  mkdir -p "$(dirname "$MERGED_MODEL")"
  uv run python -m neuroagent.training.merge_adapter \
      --base-model "$BASE_MODEL" --adapter "$ADAPTER" --output "$MERGED_MODEL"
else
  echo "[1/4] Merged model exists, skipping."
fi

# -------- Step 2: base model --------
if [ ! -f "$RESULTS_DIR/base_results.json" ]; then
  echo "[2/4] Evaluating BASE $MODEL_TAG on $SPLIT..."
  _serve_and_wait "$SERVE_KEY"
  uv run python agent-platform/scripts/training/run_sft_eval_cases.py evaluate \
      --model-id "$BASE_MODEL" --run-name "base-$SERVE_KEY" --split "$SPLIT" \
      --hospital "$HOSPITAL" --repeats "$REPEATS" \
      --output "$RESULTS_DIR/base_results.json" --port "$PORT"
  _kill_vllm
else
  echo "[2/4] Base results exist, skipping."
fi

# -------- Step 3: SFT model --------
if [ ! -f "$RESULTS_DIR/sft_results.json" ]; then
  echo "[3/4] Evaluating SFT $MODEL_TAG on $SPLIT..."
  _serve_and_wait "$MERGED_MODEL"
  uv run python agent-platform/scripts/training/run_sft_eval_cases.py evaluate \
      --model-id "$MERGED_MODEL" --run-name "sft-$SERVE_KEY" --split "$SPLIT" \
      --hospital "$HOSPITAL" --repeats "$REPEATS" \
      --output "$RESULTS_DIR/sft_results.json" --port "$PORT"
  _kill_vllm
else
  echo "[3/4] SFT results exist, skipping."
fi

# -------- Step 4: compare --------
echo "[4/4] Comparing..."
uv run python agent-platform/scripts/training/run_sft_eval_cases.py compare \
    --base-results "$RESULTS_DIR/base_results.json" \
    --sft-results "$RESULTS_DIR/sft_results.json" \
    --output "$RESULTS_DIR/comparison.json"

# Persist to EOS alongside the checkpoint.
EOS_RESULTS="$EOS_ROOT/results/sft_eval/${MODEL_TAG}"
mkdir -p "$EOS_RESULTS"
cp -r "$RESULTS_DIR/." "$EOS_RESULTS/"

echo "========================================="
echo " Done. Results: $RESULTS_DIR  (copied to $EOS_RESULTS)"
echo "========================================="
