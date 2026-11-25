#!/usr/bin/env bash
# Fig. 2 and Fig. 6 baselines on the NeuroBench test split (119 cases x 3 seeds), RTX PRO 6000 pod,
# tmux `work`. Decisions of 25 Nov 2026 (paper/decisions.md): test split now (these agents pick no
# checkpoint), SFT on the scripted perfect agent's episodes of the 419 training cases, Qwen3.8-27B as
# the larger model. Nothing here is trained on validation or test cases (train_sft refuses test ids).
#
#   phase 1  Qwen3.5-9B served at 40% of the card; beside it, LoRA SFT on the reference episodes.
#            Evaluated: untrained (policy), no test (narrative), rules in the prompt, multi-agent panel.
#   phase 2  Qwen3.5-9B with the SFT adapter (alias `sft`): the supervised fine-tuning baseline.
#   phase 3  Qwen3.8-27B: untrained, rules in the prompt, multi-agent panel.
#   phase 4  Gemma 4 E4B and Granite 4.1 8B untrained (Fig. 2).
#
# Usage (inside the pod): SNAP=/eos/.../baselines_<commit>.tar.gz bash baselines_rtx.sh
# PHASES="1 2 3 4" by default; SEEDS="0 1 2". A finished (profile, seed) is skipped on restart, and an
# interrupted one resumes episode by episode (--resume). Local work in /tmp/bl, synced to $OUT every
# 15 min; the adapter goes to $WEIGHTS on EOS. Ends with BL_EXIT=done in $OUT/status.txt.
set -uo pipefail
SNAP=${SNAP:?SNAP=<code snapshot tar.gz on EOS>}
PHASES=${PHASES:-1 2 3 4} SEEDS=${SEEDS:-0 1 2} CONC=${CONC:-24}
OUT=${OUT:-/eos/project-d/diagbox/dvc/aprotani/medical-agents/runs/baselines_test_20261125}
WEIGHTS=${WEIGHTS:-/eos/project-d/diagbox/dvc/NeuroAgent/checkpoints/sft-reference/qwen3.5-9b}
export HF_HOME=/tmp/hf TOKENIZERS_PARALLELISM=false
export UV_NO_MODIFY_PATH=1 UV_INSTALL_DIR=/tmp/uvbin UV_CACHE_DIR=/tmp/uvcache
export UV_PYTHON_INSTALL_DIR=/tmp/uvpython XDG_DATA_HOME=/tmp/xdg XDG_CACHE_HOME=/tmp/xdgcache
NAME=$(basename "$SNAP" .tar.gz) R=/tmp/ma-$(basename "$SNAP" .tar.gz) V=/tmp/venv-$(basename "$SNAP" .tar.gz)
export UV_PROJECT_ENVIRONMENT=$V TRITON_CACHE_DIR=/tmp/triton VLLM_CACHE_ROOT=/tmp/vllm-cache TORCHINDUCTOR_CACHE_DIR=/tmp/inductor
L=${L:-/tmp/bl}; mkdir -p "$L" "$OUT" "$WEIGHTS"
mark() { echo "$(date -Is) $*" | tee -a "$L/status.txt"; cp "$L/status.txt" "$OUT/" 2>/dev/null; }
touch "$WEIGHTS/.write_test" "$OUT/.write_test" || { echo "BL_EXIT=eos-write"; exit 1; }

# Environment: the snapshot's locked stack, as in e1_rtx.sh (vLLM and TRL in one venv).
[ -x /tmp/uvbin/uv ] || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH=/tmp/uvbin:$PATH
if [ ! -d "$R" ]; then mkdir -p "$R" && tar -xzf "$SNAP" -C "$R"; fi
cd "$R" && find . -name '._*' -not -path './.git/*' -delete
uv sync --all-packages --extra training > "$L/sync.log" 2>&1 || { mark "BL_EXIT=sync"; cp "$L/sync.log" "$OUT/"; exit 1; }
export PATH=$V/bin:$PATH VLLM_VENV=$V
export VLLM_CUDART_SO_PATH=$V/lib/python3.12/site-packages/nvidia/cu13/lib/libcudart.so.13
grep -rl 'def find_loaded_library' $V/lib/python3.12/site-packages --include='*.py' \
  | xargs sed -i 's/if lib_name in line:/if lib_name in line and "_stub" not in line:/'
python -c "import torch,vllm,trl;print(torch.__version__,torch.cuda.get_device_name(0),vllm.__version__,trl.__version__)" > "$L/env.txt" 2>&1
cp "$L/env.txt" "$OUT/"; cp "$R/COMMIT" "$OUT/" 2>/dev/null
mark "env ready: $NAME phases=[$PHASES] seeds=[$SEEDS] $(head -1 "$L/env.txt")"

( while sleep 900; do rsync -a "$L/" "$OUT/" 2>/dev/null; done ) & SYNC=$!
nvidia-smi --query-gpu=timestamp,utilization.gpu,memory.used --format=csv,noheader -l 60 > "$L/gpu.csv" & SMI=$!

download() { python -c "from huggingface_hub import snapshot_download as s; print(s('$1'))" >> "$L/env.txt" 2>&1; }

SERVER=
serve() {  # serve MODEL [GPU_UTIL]: start vLLM and wait until it answers
  stop_server
  GPU_MEMORY_UTILIZATION=${2:-0.90} MAX_NUM_SEQS=32 nohup bash agent-platform/scripts/runtime/serve_model.sh "$1" \
    > "$L/serve_$1${LORA_NAME:+_$LORA_NAME}.log" 2>&1 & SERVER=$!
  for _ in $(seq 1 120); do
    curl -sf localhost:8000/v1/models > /dev/null && { mark "server up: $1 ${LORA_NAME:-}"; return 0; }
    kill -0 $SERVER 2>/dev/null || break; sleep 15
  done
  mark "server failed: $1"; return 1
}
stop_server() {
  [ -n "$SERVER" ] && kill $SERVER 2>/dev/null && wait $SERVER 2>/dev/null
  pkill -f 'vllm_serve.py' 2>/dev/null; sleep 10; SERVER=
}

evaluate() {  # evaluate PROFILE TAG [benchmark args]: 119 test cases for every seed
  local profile=$1 tag=$2; shift 2
  for seed in $SEEDS; do
    local dir="$L/$tag/seed-$seed"
    [ -f "$dir/summary.json" ] && continue
    mkdir -p "$dir"
    python -m neuroagent.evaluation.benchmark --profile "$profile" --split test --seed "$seed" \
      --concurrency "$CONC" --allow-draft-policies --resume --output "$dir" "$@" > "$dir.log" 2>&1
    mark "$tag seed=$seed exit=$?"
  done
}

for phase in $PHASES; do
  case $phase in
    1)
      download Qwen/Qwen3.5-9B
      serve qwen3.5-9b 0.40 || continue
      if [ ! -f "$WEIGHTS/adapter_config.json" ]; then
        ( python -m neuroagent.training.train_sft --model qwen3.5-9b \
            --episodes training_data/sft_reference_episodes.jsonl --allow-candidates \
            --output "$WEIGHTS" > "$L/sft.log" 2>&1; mark "sft exit=$?" ) & SFT=$!
      fi
      evaluate policy-qwen3.5-9b qwen3.5-9b/untrained
      evaluate narrative-qwen3.5-9b qwen3.5-9b/no-test
      evaluate rules-qwen3.5-9b qwen3.5-9b/rules
      evaluate panel-qwen3.5-9b qwen3.5-9b/panel
      [ -n "${SFT:-}" ] && wait $SFT
      # An SFT started by hand (a rerun) also holds the card: the next phases need all of it.
      while pgrep -f neuroagent.training.train_sft > /dev/null; do sleep 60; done
      ;;
    2)
      [ -f "$WEIGHTS/adapter_config.json" ] || { mark "no SFT adapter in $WEIGHTS: phase 2 skipped"; continue; }
      mkdir -p /tmp/sft-adapter && cp -a "$WEIGHTS/." /tmp/sft-adapter/
      LORA_ADAPTER=/tmp/sft-adapter LORA_NAME=sft serve qwen3.5-9b 0.90 || continue
      evaluate policy-qwen3.5-9b qwen3.5-9b/sft --served-model sft
      ;;
    3)
      download Qwen/Qwen3.8-27B
      serve qwen3.8-27b 0.90 || continue
      evaluate policy-qwen3.8-27b qwen3.8-27b/untrained
      evaluate rules-qwen3.8-27b qwen3.8-27b/rules
      evaluate panel-qwen3.8-27b qwen3.8-27b/panel
      ;;
    4)
      for m in gemma-4-e4b:google/gemma-4-E4B-it:policy-gemma-4-e4b granite-4.1-8b:ibm-granite/granite-4.1-8b:policy-granite-4.1-8b; do
        IFS=: read key hf profile <<< "$m"
        download "$hf"; serve "$key" 0.90 || continue
        evaluate "$profile" "$key/untrained"
      done
      ;;
  esac
done
stop_server
kill $SYNC $SMI 2>/dev/null
rsync -a "$L/" "$OUT/"
mark "BL_EXIT=done"
