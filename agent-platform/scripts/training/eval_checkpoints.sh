#!/usr/bin/env bash
# Score the LoRA checkpoints of a GRPO run on held-out cases, beside the training (P3-01).
#
# The trainer writes checkpoint-<step>/ to its --weights-dir on EOS every --save-steps; this script,
# on another GPU (an A100 while the RTX trains), serves the base model with up to four checkpoints
# as LoRA modules per vLLM start and runs the benchmark on each, seed by seed. A checkpoint already
# scored is skipped, so the script can be started again as new checkpoints land. Checkpoint
# selection reads the validation cases only: a case list with a test-split case is refused.
#
# Usage: eval_checkpoints.sh WEIGHTS_DIR CASES_FILE OUTPUT [SEEDS...]
#   WEIGHTS_DIR  EOS directory holding checkpoint-*/ (adapter_config.json, adapter_model.safetensors)
#   CASES_FILE   whitespace-separated validation case ids
#   OUTPUT       local directory: OUTPUT/{base,checkpoint-N}-s{seed}/ (benchmark outputs), status.txt
#   SEEDS        default 0 1 2
# Environment: PROFILE (default policy-qwen3.5-9b), CONCURRENCY (32), GPU_MEMORY_UTILIZATION (0.85),
# DRAFT=1 to pass --allow-draft-policies (engineering only), HF_HOME (stage the base model in /dev/shm),
# PYTHON (default <repo>/.venv/bin/python). Serves Qwen3.5-9B only, the one model trained for now.

set -uo pipefail
[ $# -ge 3 ] || { sed -n '2,/^$/p' "$0"; exit 2; }
WEIGHTS=$1 CASES_FILE=$2 OUT=$3; shift 3
SEEDS=("$@"); [ ${#SEEDS[@]} -eq 0 ] && SEEDS=(0 1 2)
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VLLM_VENV="${VLLM_VENV:-$REPO_ROOT/.venv-vllm}"
PYTHON="${PYTHON:-$REPO_ROOT/.venv/bin/python}"  # from a worktree: the main clone's .venv
PROFILE=${PROFILE:-policy-qwen3.5-9b}
export PATH="$VLLM_VENV/bin:$PATH"  # ninja: FlashInfer JIT-builds the LoRA kernels
export PYTHONPATH="$REPO_ROOT/agent-platform/src:$REPO_ROOT/packages/neuroagent-schemas/src"
export TOKENIZERS_PARALLELISM=false
CASES=$(cat "$CASES_FILE")
"$PYTHON" -c 'import sys; from neuroagent.datasets import refuse_test_cases; refuse_test_cases(sys.argv[1:])' $CASES || exit 1
draft=(); [ "${DRAFT:-0}" = 1 ] && draft=(--allow-draft-policies)
mkdir -p "$OUT" "$OUT/adapters"
touch "$OUT/status.txt"

scored() { grep -q "^$1 seed=$2 exit=0" "$OUT/status.txt"; }

run() {  # run MODEL_TAG SERVED_NAME
  for seed in "${SEEDS[@]}"; do
    scored "$1" "$seed" && continue
    o=$OUT/$1-s$seed
    extra=(); [ "$2" = base ] || extra=(--served-model "$2")
    (cd "$REPO_ROOT" && nice -n 10 "$PYTHON" -m neuroagent.evaluation.benchmark --profile "$PROFILE" \
      --cases $CASES --output "$o" --concurrency "${CONCURRENCY:-32}" --seed "$seed" "${draft[@]}" "${extra[@]}" > "$o.log" 2>&1)
    echo "$1 seed=$seed exit=$?" >> "$OUT/status.txt"
  done
}

serve() {  # serve [TAG=DIR ...]; sets S
  lora=(); [ $# -gt 0 ] && lora=(--enable-lora --max-lora-rank 64 --max-loras 4 --max-cpu-loras 4 --lora-modules "$@")
  nice -n 10 "$VLLM_VENV/bin/python" "$REPO_ROOT/agent-platform/scripts/runtime/vllm_serve.py" --model Qwen/Qwen3.5-9B \
    --port 8000 --gpu-memory-utilization "${GPU_MEMORY_UTILIZATION:-0.85}" --dtype auto --max-num-seqs 32 \
    --max-model-len 32768 --enable-prefix-caching --language-model-only --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder "${lora[@]}" >> "$OUT/vllm.log" 2>&1 &
  S=$!
  for _ in $(seq 1 240); do
    kill -0 $S 2>/dev/null || break
    curl -s -f -m 3 http://127.0.0.1:8000/v1/models > /dev/null && return 0
    sleep 5
  done
  echo "vLLM did not start (see $OUT/vllm.log)" >&2; kill $S 2>/dev/null; exit 1
}

pending=()
for tag in $(ls "$WEIGHTS" 2>/dev/null | grep '^checkpoint-[0-9]*$' | sort -t- -k2 -n); do
  d=$WEIGHTS/$tag
  [ -f "$d/adapter_model.safetensors" ] || continue
  all=1; for seed in "${SEEDS[@]}"; do scored "$tag" "$seed" || all=0; done
  [ $all = 1 ] && continue
  mkdir -p "$OUT/adapters/$tag"
  cp "$d/adapter_config.json" "$d/adapter_model.safetensors" "$OUT/adapters/$tag/"
  pending+=("$tag")
done

# The base model once, then the pending checkpoints four at a time (one vLLM start per group).
base_done=1; for seed in "${SEEDS[@]}"; do scored base "$seed" || base_done=0; done
groups=$(( (${#pending[@]} + 3) / 4 ))
if [ $base_done = 0 ] && [ $groups = 0 ]; then serve; run base base; kill $S; wait $S 2>/dev/null; fi
for g in $(seq 0 $(( groups - 1 ))); do
  tags=("${pending[@]:$(( g * 4 )):4}")
  mods=(); for t in "${tags[@]}"; do mods+=("$t=$OUT/adapters/$t"); done
  serve "${mods[@]}"
  [ $g = 0 ] && [ $base_done = 0 ] && run base base
  for t in "${tags[@]}"; do run "$t" "$t"; done
  kill $S; wait $S 2>/dev/null
done
rm -rf "$OUT/adapters"
echo "done: base + ${#pending[@]} checkpoint(s) -> $OUT/status.txt"
