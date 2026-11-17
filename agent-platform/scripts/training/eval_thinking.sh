#!/usr/bin/env bash
# Thinking off vs on for the untrained Qwen3.5-9B on validation cases (17 Nov 2026).
#
# The panel runs with thinking off since 2 Sep 2026 (vLLM 0.23, 4096 tokens: Qwen spent the budget
# without a tool call). This re-tests it with longer budgets before deciding whether the trained
# models should think. One vLLM server with the qwen3 reasoning parser serves every arm, so the
# trace stays out of the parsed tool call; the off arm sends the profile's own defaults, the on
# arms the model card's thinking sampling and THINKING max_tokens per turn
# (`benchmark --thinking-tokens`). Validation only: a test-split case is refused.
#
# Usage: eval_thinking.sh CASES_FILE OUTPUT [ARMS...]
#   ARMS  "off" or a token budget per turn; default: off 8192 16384 32768
# Environment: SEEDS (default "0 1 2"), PROFILE (policy-qwen3.5-9b), CONCURRENCY (32),
# GPU_MEMORY_UTILIZATION (0.85), MAX_MODEL_LEN (65536), DRAFT=1 for --allow-draft-policies,
# PYTHON, VLLM_VENV, HF_HOME. An arm/seed already in OUTPUT/status.txt with exit=0 is skipped.

set -uo pipefail
[ $# -ge 2 ] || { sed -n '2,/^$/p' "$0"; exit 2; }
CASES_FILE=$1 OUT=$2; shift 2
ARMS=("$@"); [ ${#ARMS[@]} -eq 0 ] && ARMS=(off 8192 16384 32768)
read -ra SEEDS <<< "${SEEDS:-0 1 2}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VLLM_VENV="${VLLM_VENV:-$REPO_ROOT/.venv-vllm}"
PYTHON="${PYTHON:-$REPO_ROOT/.venv/bin/python}"
PROFILE=${PROFILE:-policy-qwen3.5-9b}
export PATH="$VLLM_VENV/bin:$PATH"
export PYTHONPATH="$REPO_ROOT/agent-platform/src:$REPO_ROOT/packages/neuroagent-schemas/src"
export TOKENIZERS_PARALLELISM=false
CASES=$(cat "$CASES_FILE")
"$PYTHON" -c 'import sys; from neuroagent.datasets import refuse_test_cases; refuse_test_cases(sys.argv[1:])' $CASES || exit 1
draft=(); [ "${DRAFT:-0}" = 1 ] && draft=(--allow-draft-policies)
mkdir -p "$OUT"; touch "$OUT/status.txt"

nice -n 10 "$VLLM_VENV/bin/python" "$REPO_ROOT/agent-platform/scripts/runtime/vllm_serve.py" --model Qwen/Qwen3.5-9B \
  --port 8000 --gpu-memory-utilization "${GPU_MEMORY_UTILIZATION:-0.85}" --dtype auto --max-num-seqs 32 \
  --max-model-len "${MAX_MODEL_LEN:-65536}" --enable-prefix-caching --language-model-only \
  --reasoning-parser qwen3 --enable-auto-tool-choice --tool-call-parser qwen3_coder >> "$OUT/vllm.log" 2>&1 &
S=$!
trap 'kill $S 2>/dev/null' EXIT
up=0
for _ in $(seq 1 240); do
  kill -0 $S 2>/dev/null || break
  curl -s -f -m 3 http://127.0.0.1:8000/v1/models > /dev/null && { up=1; break; }
  sleep 5
done
[ $up = 1 ] || { echo "vLLM did not start (see $OUT/vllm.log)" >&2; exit 1; }

for arm in "${ARMS[@]}"; do
  extra=(); [ "$arm" = off ] || extra=(--thinking-tokens "$arm")
  for seed in "${SEEDS[@]}"; do
    grep -q "^$arm seed=$seed exit=0" "$OUT/status.txt" && continue
    o=$OUT/$arm-s$seed
    (cd "$REPO_ROOT" && nice -n 10 "$PYTHON" -m neuroagent.evaluation.benchmark --profile "$PROFILE" \
      --cases $CASES --output "$o" --concurrency "${CONCURRENCY:-32}" --seed "$seed" "${draft[@]}" "${extra[@]}" > "$o.log" 2>&1)
    echo "$arm seed=$seed exit=$? $(date -u +%FT%TZ)" >> "$OUT/status.txt"
  done
done
echo "done -> $OUT/status.txt"
