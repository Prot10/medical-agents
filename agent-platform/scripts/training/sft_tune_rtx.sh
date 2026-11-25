#!/usr/bin/env bash
# Stronger SFT baseline (Andrea, 25 Nov 2026): the first SFT (2 epochs, lr 1e-4, LoRA r16) left the work-up
# of the untrained model unchanged on the test split. Is it too weak, or does imitation not transfer to held-out
# conditions? Three adapters on the same reference episodes (the scripted perfect agent, 419 training cases):
#   v1  2 epochs, lr 1e-4, r16  (already trained, checkpoints/sft-reference/qwen3.5-9b)
#   v2  4 epochs, lr 2e-4, r16
#   v3  4 epochs, lr 2e-4, r64
# Each, and the untrained model, is evaluated on the validation split (60 cases x 3 seeds) and on 60 training
# cases (seed 0: did it learn to imitate?). The adapter with the highest mean validation policy score is chosen,
# as for model A; only that one is run on the test split, and only if it is not v1 (already run).
#
# Runs in the RTX pod after baselines_rtx.sh, reusing its source tree and venv:
#   CODE=/eos/.../code bash $CODE/sft_tune_rtx.sh
# Local work in /tmp/sft, synced to $OUT; ends with SFT_EXIT=done in $OUT/status.txt.
set -uo pipefail
CODE=${CODE:-/eos/project-d/diagbox/dvc/aprotani/medical-agents/code}
R=${R:-/tmp/ma-baselines_bd86d10d} V=${V:-/tmp/venv-baselines_bd86d10d}
OUT=${OUT:-/eos/project-d/diagbox/dvc/aprotani/medical-agents/runs/sft_tune_20261125}
W=${W:-/eos/project-d/diagbox/dvc/NeuroAgent/checkpoints}
SEEDS=${SEEDS:-0 1 2} CONC=${CONC:-24}
export HF_HOME=/tmp/hf TOKENIZERS_PARALLELISM=false FLA_TILELANG=0 TRITON_CACHE_DIR=/tmp/triton
export VLLM_CACHE_ROOT=/tmp/vllm-cache TORCHINDUCTOR_CACHE_DIR=/tmp/inductor VLLM_VENV=$V
export PATH=$V/bin:$PATH VLLM_CUDART_SO_PATH=$V/lib/python3.12/site-packages/nvidia/cu13/lib/libcudart.so.13
L=/tmp/sft; mkdir -p "$L" "$OUT"
mark() { echo "$(date -Is) $*" | tee -a "$L/status.txt"; cp "$L/status.txt" "$OUT/" 2>/dev/null; }

mark "waiting for the baseline run"
until grep -q BL_EXIT=done /tmp/bl/status.txt 2>/dev/null; do sleep 120; done
cd "$R" || { mark "SFT_EXIT=no-source-tree"; exit 1; }
cp "$CODE/train_sft.py" agent-platform/src/neuroagent/training/train_sft.py
mark "start: train_sft.py with --lora-rank copied in"
( while sleep 900; do rsync -a "$L/" "$OUT/" 2>/dev/null; done ) & SYNC=$!

declare -A ADAPTER=([v1]=$W/sft-reference/qwen3.5-9b [v2]=$W/sft-reference-e4-r16/qwen3.5-9b [v3]=$W/sft-reference-e4-r64/qwen3.5-9b)
train() {  # train VARIANT RANK
  local v=$1 rank=$2
  [ -f "${ADAPTER[$v]}/adapter_config.json" ] && return 0
  python -m neuroagent.training.train_sft --model qwen3.5-9b --episodes training_data/sft_reference_episodes.jsonl \
    --allow-candidates --epochs 4 --learning-rate 2e-4 --lora-rank "$rank" --output "${ADAPTER[$v]}" > "$L/train_$v.log" 2>&1
  mark "train $v exit=$?"
}
train v2 16 & sleep 120; train v3 64 & wait

# One server, the base model plus every adapter (aliases v1, v2, v3).
mods=""; for v in v1 v2 v3; do
  [ -f "${ADAPTER[$v]}/adapter_config.json" ] || { mark "missing adapter $v"; continue; }
  mkdir -p /tmp/adapters/$v && cp -a "${ADAPTER[$v]}/." /tmp/adapters/$v/; mods="$mods $v=/tmp/adapters/$v"
done
pkill -f 'scripts/runtime/[v]llm_serve.py'; sleep 10
LORA_MODULES="$mods" MAX_NUM_SEQS=32 nohup bash agent-platform/scripts/runtime/serve_model.sh qwen3.5-9b > "$L/serve.log" 2>&1 &
for _ in $(seq 1 120); do curl -sf localhost:8000/v1/models > /dev/null && break; sleep 15; done
curl -sf localhost:8000/v1/models > /dev/null || { mark "SFT_EXIT=server"; exit 1; }
mark "server up:$mods"

VAL=$(cat data/neurobench/splits/validation_cases.txt)
TRAIN60=$(python -c "import random;ids=open('data/neurobench/splits/train_cases.txt').read().split();print(' '.join(sorted(random.Random(0).sample(ids,60))))")
run() {  # run TAG SEED SERVED CASES...
  local tag=$1 seed=$2 served=$3; shift 3
  local dir="$L/$tag/seed-$seed"; [ -f "$dir/summary.json" ] && return 0; mkdir -p "$dir"
  python -m neuroagent.evaluation.benchmark --profile policy-qwen3.5-9b --seed "$seed" --concurrency "$CONC" \
    --allow-draft-policies --resume --output "$dir" ${served:+--served-model "$served"} --cases "$@" > "$dir.log" 2>&1
  mark "$tag seed=$seed exit=$?"
}
for v in base v1 v2 v3; do
  served=$v; [ $v = base ] && served=
  for s in $SEEDS; do run "validation/$v" "$s" "$served" $VAL; done
  run "train60/$v" 0 "$served" $TRAIN60
done

python - "$L" > "$L/selection.txt" <<'EOF'
import json, glob, statistics, sys
root = sys.argv[1]
def mean(tag, key):
    rows = [json.load(open(f)) for f in glob.glob(f"{root}/{tag}/seed-*/summary.json")]
    return statistics.fmean(r["mean_reward"][key] for r in rows) if rows else float("nan")
print("variant  val_score  val_dx  val_required  train60_score  train60_required")
for v in ["base", "v1", "v2", "v3"]:
    print(f"{v:8} {mean('validation/'+v,'scalar'):.3f}  {mean('validation/'+v,'diagnosis'):.3f}  "
          f"{mean('validation/'+v,'required_action_coverage'):.3f}  {mean('train60/'+v,'scalar'):.3f}  "
          f"{mean('train60/'+v,'required_action_coverage'):.3f}")
best = max(["v1", "v2", "v3"], key=lambda v: mean("validation/" + v, "scalar"))
print("chosen", best)
EOF
cat "$L/selection.txt" >> "$L/status.txt"
best=$(awk '/^chosen/{print $2}' "$L/selection.txt")
if [ -n "$best" ] && [ "$best" != v1 ]; then
  for s in $SEEDS; do
    dir="$L/test/$best/seed-$s"; [ -f "$dir/summary.json" ] && continue; mkdir -p "$dir"
    python -m neuroagent.evaluation.benchmark --profile policy-qwen3.5-9b --split test --seed "$s" --concurrency "$CONC" \
      --allow-draft-policies --resume --served-model "$best" --output "$dir" > "$dir.log" 2>&1
    mark "test/$best seed=$s exit=$?"
  done
fi
pkill -f 'scripts/runtime/[v]llm_serve.py'
kill $SYNC 2>/dev/null; rsync -a "$L/" "$OUT/"
mark "SFT_EXIT=done chosen=$best"
