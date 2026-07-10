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

echo "========================================="
echo " SFT Evaluation — $MODEL_TAG on $SPLIT split"
echo " Base:    $BASE_MODEL (from RAM)"
echo " Adapter: $ADAPTER (LoRA, from EOS — no merge)"
echo " Repeats: $REPEATS"
echo " Results: $RESULTS_DIR"
echo "========================================="

_kill_vllm() {
  pkill -f "vllm_serve.py" 2>/dev/null || true
  pkill -f "VLLM::EngineCore" 2>/dev/null || true
  sleep 5
}

# One server hosts the base weights AND the LoRA adapter. Base is addressed by its model-id,
# the adapter by the name "sft" (see serve_model.sh LORA_ADAPTER). So both evals run against
# a single vLLM start — no merge, no restart between base and SFT.
if [ ! -f "$RESULTS_DIR/base_results.json" ] || [ ! -f "$RESULTS_DIR/sft_results.json" ]; then
  echo "[1/3] Starting vLLM ($MODEL_TAG base + LoRA adapter)..."
  _kill_vllm
  LORA_ADAPTER="$ADAPTER" bash "$SCRIPT_DIR/../runtime/serve_model.sh" "$SERVE_KEY" "$PORT" &
  for _ in $(seq 1 180); do
    curl -s "http://localhost:$PORT/v1/models" | grep -q "\"sft\"" && { echo "vLLM ready (base + sft)"; break; }
    sleep 5
  done
fi

# -------- base --------
if [ ! -f "$RESULTS_DIR/base_results.json" ]; then
  echo "[2/3] Evaluating BASE $MODEL_TAG on $SPLIT..."
  uv run python agent-platform/scripts/training/run_sft_eval_cases.py evaluate \
      --model-id "$BASE_MODEL" --run-name "base-$SERVE_KEY" --split "$SPLIT" \
      --hospital "$HOSPITAL" --repeats "$REPEATS" \
      --output "$RESULTS_DIR/base_results.json" --port "$PORT"
else
  echo "[2/3] Base results exist, skipping."
fi

# -------- SFT (LoRA adapter, addressed as "sft") --------
if [ ! -f "$RESULTS_DIR/sft_results.json" ]; then
  echo "[3/3] Evaluating SFT $MODEL_TAG (LoRA) on $SPLIT..."
  uv run python agent-platform/scripts/training/run_sft_eval_cases.py evaluate \
      --model-id "sft" --run-name "sft-$SERVE_KEY" --split "$SPLIT" \
      --hospital "$HOSPITAL" --repeats "$REPEATS" \
      --output "$RESULTS_DIR/sft_results.json" --port "$PORT"
else
  echo "[3/3] SFT results exist, skipping."
fi
_kill_vllm

# -------- compare --------
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
