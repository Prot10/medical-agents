#!/bin/bash
# Rejection-sampling fine-tuning (RFT / STaR), stage 1: generate + filter the data.
#
#   1. serve the model to sample from (base, or base + an SFT LoRA adapter)
#   2. roll out N trajectories per TRAIN case at temperature T (diverse samples)
#   3. keep only the diagnostically-correct ones, dedupe, cap per case
#
# Then train on the result with run_sft_training.sh (DATA=<the RFT jsonl>). Sampling from the
# SFT'd model (ADAPTER=...) reinforces reasoning the student can already produce — the point
# of RFT. Run: bash run_rft.sh Qwen3.5-9B
set -uo pipefail
cd /home/aprotani/projects/medical-agents

MODEL_TAG="${1:-Qwen3.5-9B}"
SERVE_KEY="$(echo "$MODEL_TAG" | tr '[:upper:]' '[:lower:]')"
BASE_MODEL="Qwen/$MODEL_TAG"
EOS_ROOT="${EOS_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent}"
ADAPTER="${ADAPTER:-$EOS_ROOT/checkpoints/sft_${MODEL_TAG}}"   # sample from the SFT model; unset ADAPTER='' for base
N="${N:-16}"                       # rollouts per train case
TEMP="${TEMP:-0.7}"                # sampling temperature (diversity)
HOSPITAL="${HOSPITAL:-de_charite}"
PORT="${PORT:-8000}"
OUT="${OUT:-results/rft/${MODEL_TAG}}"
DATA_OUT="${DATA_OUT:-training_data/rft_trajectories/${MODEL_TAG}/trajectories.jsonl}"
MAX_PER_CASE="${MAX_PER_CASE:-4}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EVAL=agent-platform/scripts/training/run_sft_eval_cases.py

source "$SCRIPT_DIR/_stage.sh"
source "$SCRIPT_DIR/_gpu.sh"
stage_base "$BASE_MODEL" || exit 1
export CUDA_MODULE_LOADING=LAZY
mkdir -p "$OUT" "$(dirname "$DATA_OUT")"
ROLLOUTS="$OUT/rollouts.jsonl"

echo "#########################################################"
echo "# RFT rollouts — $MODEL_TAG : $N samples/case @ temp $TEMP, TRAIN split"
[ -n "$ADAPTER" ] && echo "# sampling from SFT model (LoRA $ADAPTER)" || echo "# sampling from BASE model"
echo "# Start: $(date)"
echo "#########################################################"

free_gpu "before serving"
if [ -n "$ADAPTER" ] && [ -f "$ADAPTER/adapter_model.safetensors" ]; then
  MODEL_ID="sft"; READY='"sft"'
  LORA_ADAPTER="$ADAPTER" bash "$SCRIPT_DIR/../runtime/serve_model.sh" "$SERVE_KEY" "$PORT" &
else
  MODEL_ID="$BASE_MODEL"; READY="model"
  bash "$SCRIPT_DIR/../runtime/serve_model.sh" "$SERVE_KEY" "$PORT" &
fi
for _ in $(seq 1 180); do
  curl -s "http://localhost:$PORT/v1/models" | grep -q "$READY" && { echo "✓ vLLM ready"; break; }
  sleep 5
done

# Roll out on the TRAIN split. Reuses the eval runner: the agent + the diagnostic_accuracy_top1
# verifier + full-conversation capture, just with N repeats at temp T on the train cases.
uv run python "$EVAL" evaluate \
  --model-id "$MODEL_ID" --run-name "rft-$SERVE_KEY" --split train \
  --hospital "$HOSPITAL" --temperature "$TEMP" --repeats "$N" \
  --no-save-bundles --rollout-jsonl "$ROLLOUTS" \
  --output "$OUT/rollout_metrics.json" --port "$PORT"

free_gpu "rollouts done"

# Filter to verified-correct, dedupe, cap per case, write the SFT dataset.
uv run python "$SCRIPT_DIR/build_rft_dataset.py" \
  --rollouts "$ROLLOUTS" --output "$DATA_OUT" --max-per-case "$MAX_PER_CASE"

# Persist to EOS.
mkdir -p "$EOS_ROOT/results/rft/${MODEL_TAG}"
cp -r "$OUT/." "$EOS_ROOT/results/rft/${MODEL_TAG}/"

echo ""
echo "#########################################################"
echo "# RFT data ready: $DATA_OUT"
echo "# Next — SFT on it (from the SAME base, fresh adapter):"
echo "#   DATA=$DATA_OUT CHECKPOINTS_ROOT=$EOS_ROOT/checkpoints_rft \\"
echo "#     FORCE_RETRAIN=1 PRECISION=bf16 bash $SCRIPT_DIR/run_sft_training.sh $BASE_MODEL"
echo "# Then evaluate with run_definitive_eval.sh and compare to the SFT baseline."
echo "#########################################################"
