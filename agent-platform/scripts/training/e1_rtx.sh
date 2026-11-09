#!/usr/bin/env bash
# E1 on the RTX PRO 6000 (ml.cern.ch pod, tmux `work`): the policy arm and the outcome arm of one training
# seed, side by side, everything equal but the reward. Decisions of 9 Nov 2026 (tracker D2-D7, D11, D13):
#   Qwen3.5-9B from base (D3); the 419 cases of the 14 training conditions (`--split train`, D11);
#   draft policies in training (D2); outcome reward 0.85*D + 0.15*(1 - cost/B), B = 5913 USD (D6);
#   500 steps, lr 2e-5, 8 generations x 2 cases per step, checkpoints every 50 steps (D7: chosen later on
#   the validation cases by eval_checkpoints.sh + select_checkpoint.py, on another GPU). Same seed = same
#   cases per step in both arms. Nothing here touches validation or test cases.
#
# Usage (inside the pod): SNAP=/eos/.../e1_<commit>.tar.gz SEED=1 bash e1_rtx.sh
# Writes /tmp/e1 (logs, rollouts), synced to $OUT every 15 min; adapters and checkpoints go to $WEIGHTS on EOS.
# A crashed arm resumes from its last checkpoint (3 attempts). Ends with E1_EXIT=done in $OUT/status.txt.
set -uo pipefail
SEED=${SEED:-1}
SNAP=${SNAP:?SNAP=<code snapshot tar.gz on EOS>}
STEPS=${STEPS:-500} LR=${LR:-2e-5} SAVE=${SAVE:-50} B=${B:-5913}
OUT=${OUT:-/eos/project-d/diagbox/dvc/aprotani/medical-agents/runs/e1_qwen3.5-9b/seed-$SEED}
WEIGHTS=${WEIGHTS:-/eos/project-d/diagbox/dvc/NeuroAgent/checkpoints/paper-e1/qwen3.5-9b}
export HF_HOME=/tmp/hf TOKENIZERS_PARALLELISM=false
export UV_NO_MODIFY_PATH=1 UV_INSTALL_DIR=/tmp/uvbin UV_CACHE_DIR=/tmp/uvcache
export UV_PYTHON_INSTALL_DIR=/tmp/uvpython XDG_DATA_HOME=/tmp/xdg XDG_CACHE_HOME=/tmp/xdgcache
export UV_PROJECT_ENVIRONMENT=/tmp/venv-e1 TRITON_CACHE_DIR=/tmp/triton TRITON_CACHE_AUTOTUNING=1
export VLLM_CACHE_ROOT=/tmp/vllm-cache TORCHINDUCTOR_CACHE_DIR=/tmp/inductor
L=/tmp/e1/seed-$SEED; mkdir -p "$L" "$OUT" "$WEIGHTS"
mark() { echo "$(date -Is) $*" | tee -a "$L/status.txt"; cp "$L/status.txt" "$OUT/" 2>/dev/null; }
touch "$WEIGHTS/.write_test" "$OUT/.write_test" || { echo "E1_EXIT=eos-write"; exit 1; }

# Environment: the locked stack of the snapshot (vLLM 0.32, TRL 1.17), as in the November sweep.
[ -x /tmp/uvbin/uv ] || curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH=/tmp/uvbin:$PATH
if [ ! -d /tmp/ma-e1 ]; then mkdir -p /tmp/ma-e1 && tar -xzf "$SNAP" -C /tmp/ma-e1; fi
cd /tmp/ma-e1 && find . -name '._*' -not -path './.git/*' -delete
uv sync --all-packages --extra training > "$L/sync.log" 2>&1 || { mark "E1_EXIT=sync"; cp "$L/sync.log" "$OUT/"; exit 1; }
export PATH=/tmp/venv-e1/bin:$PATH
# vLLM takes the first mapped library named libcudart, and tilelang ships libcudart_stub.so without cudaDeviceReset
export VLLM_CUDART_SO_PATH=/tmp/venv-e1/lib/python3.12/site-packages/nvidia/cu13/lib/libcudart.so.13
grep -rl 'def find_loaded_library' /tmp/venv-e1/lib/python3.12/site-packages --include='*.py' \
  | xargs sed -i 's/if lib_name in line:/if lib_name in line and "_stub" not in line:/'
python -c "import torch,vllm,trl;print(torch.__version__,torch.version.cuda,torch.cuda.get_device_name(0),vllm.__version__,trl.__version__);torch.ones(1).cuda()" > "$L/env.txt" 2>&1
python -c "from huggingface_hub import snapshot_download as s; print(s('Qwen/Qwen3.5-9B'))" >> "$L/env.txt" 2>&1 \
  || { mark "E1_EXIT=model-download"; cp "$L/env.txt" "$OUT/"; exit 1; }
cat "$L/env.txt" > "$OUT/env.txt"
cp /tmp/ma-e1/COMMIT "$OUT/" 2>/dev/null
mark "env ready: commit $(cat /tmp/ma-e1/COMMIT 2>/dev/null) $(head -1 "$L/env.txt")"

# Logs to EOS every 15 min, from /tmp so an EOS outage cannot break the runs.
( while sleep 900; do rsync -a --exclude 'rollouts*' "$L/" "$OUT/" 2>/dev/null; done ) & SYNC=$!
nvidia-smi --query-gpu=timestamp,utilization.gpu,memory.used --format=csv,noheader -l 60 > "$L/gpu.csv" & SMI=$!

arm() {  # arm REWARD [extra args]
  local r=$1; shift
  for attempt in 1 2 3; do
    # Two colocated runs need about 75 GB: wait for free memory rather than collide.
    until [ "$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits)" -ge 45000 ]; do sleep 60; done
    python -m neuroagent.training.train_grpo --model qwen3.5-9b --split train --seed "$SEED" \
      --max-steps "$STEPS" --learning-rate "$LR" --num-generations 8 --cases-per-step 2 --save-steps "$SAVE" \
      --reward "$r" "$@" --vllm-gpu-memory-utilization 0.35 --allow-draft-policies --resume \
      --output "$L/$r" --weights-dir "$WEIGHTS/$r/seed-$SEED" >> "$L/$r.log" 2>&1
    rc=$?; mark "$r attempt=$attempt exit=$rc"; [ $rc = 0 ] && break; sleep 120
  done
  mark "$r exit=$rc"
}
arm policy & P=$!; sleep 180
arm outcome --outcome-budget-usd "$B" --outcome-cost-weight 0.15 & O=$!
wait $P $O
kill $SYNC $SMI 2>/dev/null
rsync -a "$L/" "$OUT/"
mark "E1_EXIT=done"
