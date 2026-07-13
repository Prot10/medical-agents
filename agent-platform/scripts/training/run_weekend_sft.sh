#!/bin/bash
# Weekend SFT: run each Qwen3.5 model fully (train, then evaluate base-vs-SFT on the held-out
# 100-case test split) before moving to the next. 4B first as a full dress rehearsal, then 9B.
#
# One A100, so models run sequentially. Base weights load from RAM (/dev/shm, auto-staged from
# EOS); adapters and results are written to EOS. Nothing large touches local disk.
#
# Run detached:
#   nohup bash agent-platform/scripts/training/run_weekend_sft.sh > weekend_sft.log 2>&1 &
#
# Idempotent: each stage skips if its output already exists, so it is safe to re-run after an
# interruption.
set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"  # repo root

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODELS=("Qwen3.5-4B" "Qwen3.5-9B")
EOS_ROOT="${EOS_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent}"

echo "#########################################################"
echo "# Weekend SFT — ${MODELS[*]}"
echo "# Start: $(date)"
echo "#########################################################"

for TAG in "${MODELS[@]}"; do
  echo ""
  echo "==================== $TAG ===================="

  # 1. Base model on the test set FIRST — same split/sampling as the SFT eval, so the two are
  #    directly comparable, and the RAM-staged base is scored before training touches the GPU.
  echo "[$TAG] base test-set eval — $(date)"
  if ! MODE=base bash "$SCRIPT_DIR/run_sft_eval.sh" "$TAG"; then
    echo "[$TAG] BASE EVAL FAILED — continuing (training can still run)." >&2
  fi

  # 2. Train the adapter (written to EOS).
  echo "[$TAG] training — $(date)"
  if ! bash "$SCRIPT_DIR/run_sft_training.sh" "Qwen/$TAG"; then
    echo "[$TAG] TRAINING FAILED — skipping SFT eval, continuing to next model." >&2
    continue
  fi

  ADAPTER="$EOS_ROOT/checkpoints/sft_$TAG"
  if [ ! -f "$ADAPTER/adapter_model.safetensors" ]; then
    echo "[$TAG] no adapter at $ADAPTER after training — skipping SFT eval." >&2
    continue
  fi

  # 3. SFT model on the same test set, then compare against the base results from step 1.
  echo "[$TAG] SFT test-set eval + compare — $(date)"
  if ! MODE=sft bash "$SCRIPT_DIR/run_sft_eval.sh" "$TAG"; then
    echo "[$TAG] SFT EVAL FAILED — adapter is safe on EOS; continuing to next model." >&2
    continue
  fi
  echo "[$TAG] done — $(date)"
done

echo ""
echo "#########################################################"
echo "# Weekend SFT complete: $(date)"
echo "# Adapters:  $EOS_ROOT/checkpoints/sft_*"
echo "# Results:   $EOS_ROOT/results/sft_eval/*"
echo "#########################################################"
