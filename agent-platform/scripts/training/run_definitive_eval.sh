#!/bin/bash
# Definitive base-vs-SFT evaluation for one model, aligned with the agent-eval literature:
#   * GREEDY (temp=0, 1 pass)  -> primary pass@1 accuracy, deterministic and comparable
#                                 (Chen et al. 2021, HumanEval convention)
#   * SAMPLED (temp=0.7, 3x)   -> reliability / variance across trials
#                                 (Yao et al. 2024, tau-bench pass^k; Wang et al. self-consistency)
#   * full traces saved as judge bundles -> LLM-judge composite score
#                                 (Zheng et al. MT-Bench; Singhal et al. Med-PaLM rubric)
#   * paired bootstrap CI + McNemar in the compare step
#                                 (Dietterich 1998; Efron bootstrap; Card et al. 2020)
#
# Base and SFT are served from ONE vLLM process (base by id, adapter as "sft"), so every
# comparison is same-session and same-code. Run: bash run_definitive_eval.sh Qwen3.5-9B
set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"  # repo root

MODEL_TAG="${1:-Qwen3.5-9B}"
SERVE_KEY="$(echo "$MODEL_TAG" | tr '[:upper:]' '[:lower:]')"
BASE_MODEL="Qwen/$MODEL_TAG"
EOS_ROOT="${EOS_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent}"
ADAPTER="${ADAPTER:-$EOS_ROOT/checkpoints/sft_${MODEL_TAG}}"
SPLIT="${SPLIT:-test}"
HOSPITAL="${HOSPITAL:-de_charite}"
PORT="${PORT:-8000}"
ROOT="${ROOT:-results/definitive_eval/${MODEL_TAG}}"
# Cases run concurrently against vLLM (each is an independent agent session). The agent loop is
# I/O-bound and vLLM batches server-side, so this is what makes the full 800-rollout eval finish
# in hours instead of a day.
CONCURRENCY="${CONCURRENCY:-8}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_ui.sh"
EVAL=agent-platform/scripts/training/run_sft_eval_cases.py

source "$SCRIPT_DIR/_stage.sh"
source "$SCRIPT_DIR/_gpu.sh"
stage_base "$BASE_MODEL" || exit 1
export CUDA_MODULE_LOADING=LAZY
mkdir -p "$ROOT"

ui_panel "Definitive eval · $MODEL_TAG on $SPLIT" \
  "compare|base vs SFT/LoRA" \
  "sampling|greedy (temp0 ×1) + sampled (temp0.7 ×3), traces saved" \
  "start|$(date)"

# One server hosts base + the LoRA adapter for the whole run.
free_gpu "before serving"
[ -f "$ADAPTER/adapter_model.safetensors" ] || { ui_err "no adapter at $ADAPTER"; exit 1; }
ui_step "Starting vLLM ($MODEL_TAG base + LoRA, max_num_seqs=$CONCURRENCY)…"
LORA_ADAPTER="$ADAPTER" MAX_NUM_SEQS="$CONCURRENCY" \
  bash "$SCRIPT_DIR/../runtime/serve_model.sh" "$SERVE_KEY" "$PORT" &
for _ in $(seq 1 180); do
  curl -s "http://localhost:$PORT/v1/models" | grep -q "\"sft\"" && { ui_ok "vLLM ready (base + sft)"; break; }
  sleep 5
done

# Verbose eval logs go to a file; the terminal keeps the live progress bar.
LOG_FILE="${LOG_FILE:-results/logs/eval_${MODEL_TAG}_$(date +%Y%m%d_%H%M%S).log}"
mkdir -p "$(dirname "$LOG_FILE")"

# _eval <sampling_name> <temperature> <repeats> <model-id> <run-name>
_eval() {
  local samp="$1" temp="$2" reps="$3" mid="$4" rn="$5"
  local out="$ROOT/$samp/${rn}_results.json"
  if [ -f "$out" ]; then ui_info "$samp/$rn exists, skipping"; return 0; fi
  uv run python "$EVAL" evaluate \
    --model-id "$mid" --run-name "$rn" --split "$SPLIT" --hospital "$HOSPITAL" \
    --temperature "$temp" --repeats "$reps" --output "$out" --port "$PORT" \
    --concurrency "$CONCURRENCY" --log-file "$LOG_FILE"
}

for samp in "greedy:0:1" "sampled:0.7:3"; do
  name="${samp%%:*}"; rest="${samp#*:}"; temp="${rest%%:*}"; reps="${rest##*:}"
  ui_section "$name (temp=$temp ×$reps)"
  _eval "$name" "$temp" "$reps" "$BASE_MODEL" "base-$SERVE_KEY"
  _eval "$name" "$temp" "$reps" "sft"         "sft-$SERVE_KEY"
  uv run python "$EVAL" compare \
    --base-results "$ROOT/$name/base-${SERVE_KEY}_results.json" \
    --sft-results  "$ROOT/$name/sft-${SERVE_KEY}_results.json" \
    --output "$ROOT/$name/comparison.json"
done

free_gpu "eval done"

# Persist to EOS (results + the judge bundles for the composite score).
EOS_OUT="$EOS_ROOT/results/definitive_eval/${MODEL_TAG}"
mkdir -p "$EOS_OUT"
cp -r "$ROOT/." "$EOS_OUT/"

ui_panel "Definitive eval complete · $MODEL_TAG" \
  "finished|$(date)" \
  "results|$ROOT ${C_GREY}(copied to $EOS_OUT)${C_RESET}" \
  "judge|$ROOT/*/judge_bundles/ ${C_GREY}→ run the llm-judge next${C_RESET}"
