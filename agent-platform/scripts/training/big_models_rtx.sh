#!/usr/bin/env bash
# Larger untrained references of other families (Andrea, 26 Nov 2026): beside Qwen3.8-27B, which is a
# newer generation of the panel's own family, Gemma 4 31B and Granite 4.1 30B (larger siblings of the
# panel models) and Llama 3.3 70B FP8 (older, much larger). Each set up as Qwen3.8-27B was, without
# training: the policy prompt, the rules in the prompt, and the multi-agent panel. Test split, 3 seeds.
#
# Runs in the RTX pod after sft_tune_rtx.sh, reusing the baselines source tree and venv:
#   CODE=/eos/.../code bash $CODE/big_models_rtx.sh
# $CODE/big_models_files.tar holds the registry, serve script and profiles added on 26 Nov.
# Results in /tmp/bl/<model>/{untrained,rules,panel} (next to the other baselines), synced to $OUT; ends with BIG_EXIT=done.
set -uo pipefail
CODE=${CODE:-/eos/project-d/diagbox/dvc/aprotani/medical-agents/code}
R=${R:-/tmp/ma-baselines_bd86d10d} V=${V:-/tmp/venv-baselines_bd86d10d}
OUT=${OUT:-/eos/project-d/diagbox/dvc/aprotani/medical-agents/runs/baselines_test_20261125}
SEEDS=${SEEDS:-0 1 2} CONC=${CONC:-24}
export HF_HOME=/tmp/hf TOKENIZERS_PARALLELISM=false TRITON_CACHE_DIR=/tmp/triton
export VLLM_CACHE_ROOT=/tmp/vllm-cache TORCHINDUCTOR_CACHE_DIR=/tmp/inductor VLLM_VENV=$V
export PATH=$V/bin:$PATH VLLM_CUDART_SO_PATH=$V/lib/python3.12/site-packages/nvidia/cu13/lib/libcudart.so.13
L=/tmp/bl; mkdir -p "$L/big" "$OUT"
mark() { echo "$(date -Is) $*" | tee -a "$L/big/status.txt"; cp "$L/big/status.txt" "$OUT/big_status.txt" 2>/dev/null; }

mark "waiting for the SFT tuning run"
until grep -q SFT_EXIT= /tmp/sft/status.txt 2>/dev/null; do sleep 120; done
cd "$R" || { mark "BIG_EXIT=no-source-tree"; exit 1; }
tar -xf "$CODE/big_models_files.tar" -C "$R" || { mark "BIG_EXIT=files"; exit 1; }
mark "start"

for spec in gemma-4-31b:google/gemma-4-31B-it:0.90:24 granite-4.1-30b:ibm-granite/granite-4.1-30b:0.90:24 \
            llama-3.3-70b:RedHatAI/Llama-3.3-70B-Instruct-FP8-dynamic:0.93:12; do
  IFS=: read key hf util conc <<< "$spec"
  python -c "from huggingface_hub import snapshot_download as s; s('$hf')" >> "$L/big/download.log" 2>&1 \
    || { mark "download failed: $key"; continue; }
  pkill -f 'scripts/runtime/[v]llm_serve.py'; sleep 10
  GPU_MEMORY_UTILIZATION=$util MAX_NUM_SEQS=$conc nohup bash agent-platform/scripts/runtime/serve_model.sh "$key" \
    > "$L/big/serve_$key.log" 2>&1 &
  up=; for _ in $(seq 1 120); do curl -sf -m 10 localhost:8000/v1/models > /dev/null && { up=1; break; }; sleep 15; done
  [ -n "$up" ] || { mark "server failed: $key"; continue; }
  mark "server up: $key"
  for arm in policy:untrained rules:rules panel:panel; do
    for s in $SEEDS; do
      dir="$L/$key/${arm#*:}/seed-$s"; [ -f "$dir/summary.json" ] && continue; mkdir -p "$dir"
      python -m neuroagent.evaluation.benchmark --profile "${arm%%:*}-$key" --split test --seed "$s" \
        --concurrency "$conc" --allow-draft-policies --resume --output "$dir" > "$dir.log" 2>&1
      mark "$key/${arm#*:} seed=$s exit=$?"
      rsync -a "$L/$key" "$OUT/"
    done
  done
done
pkill -f 'scripts/runtime/[v]llm_serve.py'
rsync -a "$L/big" "$OUT/"
mark "BIG_EXIT=done"
