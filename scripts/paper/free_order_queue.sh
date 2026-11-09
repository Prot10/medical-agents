#!/usr/bin/env bash
# Free-order ablation for the whole panel, menu arm and free-order arm on the same code, 6 Nov 2026.
#
# For each model: serve it with vLLM, run the menu profile (policy-*) and the free-order profile
# (free-order-*) on the 600 cases, seeds 1-3, concurrency 16, draft policies; stop the server; next
# model. Free-order episodes that failed on the environment (a gateway outage) are retried by up to
# two more --resume passes. A step whose summary.json exists is skipped, so the script can be
# restarted at any point. It runs on rockhopper in tmux and needs nothing from the Mac: weights
# are staged in /dev/shm/hf beforehand (Kerberos may be gone by the time a model starts), the
# gateway key is ~/.config/cern-ml/aigw.key.
#
#   tmux new-session -d -s panel "CODE=~/projects/ma-free OUT=~/projects/medical-agents/outputs/paper/free_order_panel \
#       CLEANUP_WEIGHTS='granite-4.1-8b gemma-4-e4b' \
#       bash ~/projects/ma-free/scripts/paper/free_order_queue.sh granite-4.1-8b gemma-4-e4b qwen3.5-9b"
set -uo pipefail

CODE=${CODE:?code checkout with the free-order loop}
OUT=${OUT:?output folder}
PY=${PY:-$HOME/projects/medical-agents/.venv/bin/python}
VLLM_VENV=${VLLM_VENV:-$HOME/projects/medical-agents/.venv-vllm}
SEEDS=${SEEDS:-"1 2 3"}
CLEANUP_WEIGHTS=${CLEANUP_WEIGHTS:-}  # model keys whose /dev/shm weights are deleted once their runs end
MODELS=("$@")
mkdir -p "$OUT"
STATUS=$OUT/status.txt
log() { echo "$(date '+%F %T') $*" | tee -a "$STATUS"; }

declare -A PROFILE_SUFFIX=([qwen3.5-9b]=qwen3.5-9b [granite-4.1-8b]=granite-4.1-8b [gemma-4-e4b]=gemma-4-e4b)

serve() {  # start vLLM for $1, wait until it answers (max 20 min)
  # Own process group, so stopping it never touches another vLLM on the machine.
  setsid bash -c "cd '$CODE' && HF_HOME=/dev/shm/hf HF_HUB_OFFLINE=1 VLLM_VENV='$VLLM_VENV' nice -n 10 \
     agent-platform/scripts/runtime/serve_model.sh '$1' > '$OUT/vllm-$1.log' 2>&1" &
  SERVER=$!
  for _ in $(seq 80); do
    curl -sf localhost:8000/v1/models >/dev/null && return 0
    kill -0 $SERVER 2>/dev/null || return 1
    sleep 15
  done
  return 1
}

stop_server() {
  [ -n "${SERVER:-}" ] || return 0
  kill -- -"$SERVER" 2>/dev/null
  for _ in $(seq 40); do nvidia-smi --query-compute-apps=pid --format=csv,noheader | grep -q . || break; sleep 3; done
  SERVER=
}

bench() {  # bench PROFILE DIR SEED
  PYTHONPATH=$CODE/agent-platform/src:$CODE/packages/neuroagent-schemas/src nice -n 10 "$PY" \
    -m neuroagent.evaluation.benchmark --profile "$1" --all --seed "$3" --concurrency 16 \
    --allow-draft-policies --resume --output "$2" >> "$2.log" 2>&1
}

failed_on_environment() {  # number of episodes of DIR whose run failed on the environment
  grep -l '"reason": "environment_error"' "$1"/episodes/*.json 2>/dev/null | wc -l
}

trap 'stop_server' EXIT
cd "$CODE"
for model in "${MODELS[@]}"; do
  suffix=${PROFILE_SUFFIX[$model]:?unknown model $model}
  hf=$(PYTHONPATH=$CODE/agent-platform/src "$PY" -c "from neuroagent.model_registry import KEY_TO_HF; print(KEY_TO_HF['$model'].replace('/', '--'))")
  if [ ! -d "/dev/shm/hf/hub/models--$hf" ]; then
    log "$model: weights not staged in /dev/shm/hf, skipped"; continue
  fi
  todo=0
  for arm in policy free-order; do for s in $SEEDS; do
    [ -f "$OUT/$model/$arm-s$s/summary.json" ] || todo=1
  done; done
  [ $todo = 1 ] || { log "$model: all done already"; continue; }
  log "$model: starting vLLM"
  if ! serve "$model"; then log "$model: vLLM did not start (see vllm-$model.log)"; stop_server; continue; fi
  for arm in policy free-order; do
    for s in $SEEDS; do
      dir=$OUT/$model/$arm-s$s
      [ -f "$dir/summary.json" ] && [ "$(failed_on_environment "$dir")" = 0 ] && continue
      mkdir -p "$OUT/$model"
      for pass in 1 2 3; do
        bench "$arm-$suffix" "$dir" "$s"; rc=$?
        left=$(failed_on_environment "$dir")
        log "$model $arm s$s pass $pass exit=$rc environment_failures=$left"
        [ "$left" = 0 ] && break
        sleep 300
      done
    done
  done
  stop_server
  log "$model: done"
  if [[ " $CLEANUP_WEIGHTS " == *" $model "* ]]; then
    rm -rf "/dev/shm/hf/hub/models--$hf" && log "$model: staged weights removed from /dev/shm"
  fi
done

for model in "${MODELS[@]}"; do
  [ -d "$OUT/$model" ] && PYTHONPATH=$CODE/agent-platform/src:$CODE/packages/neuroagent-schemas/src "$PY" \
    "$CODE/scripts/paper/free_order_compare.py" --menu "$OUT/$model/policy-s{seed}" --free "$OUT/$model/free-order-s{seed}" \
    --seeds $SEEDS > "$OUT/$model/compare.txt" 2>&1
done
log ALL_DONE
