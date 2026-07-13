#!/bin/bash
# SFT on the 1000 gold trajectories (agent distillation), train split only.
#
# Run: bash agent-platform/scripts/training/run_sft_training.sh [model]
#   model defaults to Qwen/Qwen3.5-9B; pass Qwen/Qwen3.5-4B for the small student.
#
# Trains on the 500 train cases (1000 trajectories, two styles each); 10% of TRAIN cases are
# carved out for eval_loss / early stopping. The 100 test cases are never seen — evaluate
# them afterwards with run_sft_eval.sh.
#
# Base weights stage to /dev/shm (RAM); the adapter is written straight to EOS. Precision is
# QLoRA (default) or bf16 LoRA via PRECISION=bf16.
set -euo pipefail

cd /home/aprotani/projects/medical-agents

MODEL="${1:-Qwen/Qwen3.5-9B}"
MODEL_TAG="$(basename "$MODEL")"

EOS_ROOT="${EOS_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent}"
CHECKPOINTS_ROOT="${CHECKPOINTS_ROOT:-$EOS_ROOT/checkpoints}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Storage split (measured): reading a full model off the EOS FUSE mount is ~1-2h of scattered
# small reads. Writing is fast (221 MB/s). So stage the base into /dev/shm (RAM, not the full
# local disk) once, load from there, and write every checkpoint straight to EOS. stage_base
# is idempotent and validates the copy before returning, and sets HF_HOME/HF_HUB_OFFLINE.
source "$SCRIPT_DIR/_stage.sh"
stage_base "$MODEL" || exit 1
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

RUN_NAME="sft_${MODEL_TAG}"
# The finetuned adapter + run_summary go straight to EOS (small, fast to write there).
EOS_DIR="$CHECKPOINTS_ROOT/$RUN_NAME"

# Idempotent: if the adapter is already on EOS, don't retrain (makes the weekend runner safe to
# re-run after an interruption). Override with FORCE_RETRAIN=1.
if [ -f "$EOS_DIR/adapter_model.safetensors" ] && [ "${FORCE_RETRAIN:-0}" != 1 ]; then
  echo "✓ $MODEL_TAG adapter already trained at $EOS_DIR — skipping (FORCE_RETRAIN=1 to redo)"
  exit 0
fi

DATA="${DATA:-training_data/gold_trajectories/trajectories.jsonl}"
SPLITS="${SPLITS:-data/neurobench/splits}"

# The longest trajectory is ~15,809 tokens once the 12 tool schemas are rendered into the
# prompt. Truncation removes the END of a trajectory — the final diagnosis — so the cap must
# sit above that. The probe reports what the GPU can actually hold.
SEQ_CAP="${SEQ_CAP:-16384}"
PROBE_JSON="results/sft_probe/max_seq_probe.json"
if [ -z "${MAX_SEQ:-}" ]; then
  if [ ! -f "$PROBE_JSON" ]; then
    echo "ERROR: $PROBE_JSON missing. Run:" >&2
    echo "  uv run python agent-platform/scripts/training/probe_max_seq_length.py --liger" >&2
    echo "or set MAX_SEQ=N explicitly." >&2
    exit 1
  fi
  MAX_SEQ="$(python3 -c "
import json
probed = json.load(open('$PROBE_JSON'))['shared_max_seq_length']
print(min(probed, $SEQ_CAP))")"
fi

if [ "$MAX_SEQ" -lt 16384 ]; then
  echo "WARNING: max_seq=$MAX_SEQ truncates the longest trajectories (up to 15,809 tokens)."
  echo "         Truncation cuts the final diagnosis. Consider a smaller model or shorter prompts."
fi

# Per-model recipe. LoRA adapters are randomly initialised, so they want ~10x the LR of a
# full fine-tune; 1e-4..2e-4 is the consensus band for rank-64 QLoRA. The 4B has VRAM
# headroom, so it skips optimizer paging and takes a slightly higher LR.
case "$MODEL_TAG" in
  Qwen3.5-4B) LR="${LR:-2e-4}";   OPTIM="${OPTIM:-adamw_8bit}" ;;
  *)          LR="${LR:-1.5e-4}"; OPTIM="${OPTIM:-paged_adamw_8bit}" ;;
esac

# Precision: qlora (4-bit NF4, default) or bf16 (16-bit base LoRA). bf16 avoids quantization
# error on the base — Unsloth's Qwen3.5 guidance — at ~2 GB more memory (measured: 27.2 GB vs
# 25.2 GB at seq 13312 on the 9B; both fit 40 GB with margin). Opt in with PRECISION=bf16.
PRECISION="${PRECISION:-qlora}"
case "$PRECISION" in
  qlora) QLORA_FLAG="--qlora" ;;
  bf16)  QLORA_FLAG="" ;;
  *) echo "ERROR: PRECISION must be 'qlora' or 'bf16', got '$PRECISION'" >&2; exit 1 ;;
esac

EPOCHS="${EPOCHS:-3}"
BATCH="${BATCH:-1}"
GRAD_ACCUM="${GRAD_ACCUM:-16}"   # effective batch 16; LoRA tolerates large batches poorly

# flash-linear-attention supplies Qwen3.5's gated-delta-net Triton kernels. Without it the
# model trains correctly but ~2.2x slower (torch fallback). Warn loudly rather than silently
# burn hours — it is a project dependency (agent-platform[training]).
if ! uv run python -c "import fla" 2>/dev/null; then
  echo "WARNING: flash-linear-attention not importable — Qwen3.5 will run the slow torch"
  echo "         fallback (~2.2x slower). Install with: uv sync --extra training"
fi

N_TRAJ="$(wc -l < "$DATA")"
mkdir -p "$EOS_DIR" results/sft_probe

echo "========================================="
echo " SFT — agent distillation"
echo " Model:      $MODEL ($PRECISION)"
echo " Data:       $DATA ($N_TRAJ trajectories, train split only)"
echo " Max seq:    $MAX_SEQ tokens (probe, capped at $SEQ_CAP)"
echo " LoRA:       rank=64, alpha=128, all linear layers"
echo " LR:         $LR ($OPTIM), cosine, warmup 0.05, wd 0.01"
echo " Epochs:     $EPOCHS, batch=$BATCH x accum=$GRAD_ACCUM (effective $((BATCH*GRAD_ACCUM)))"
echo " Loss:       assistant-only (observations masked, verified before step 1)"
echo " NEFTune:    off (degrades tool-argument fidelity)"
echo " Validation: 10% of TRAIN cases, early stopping on eval_loss"
echo " Base:       $SHM_HF (RAM, staged from EOS)"
echo " Output:     $EOS_DIR (EOS — only the adapter, written directly)"
echo "========================================="
echo "Start: $(date)"
echo ""

# A prior eval phase serves with vLLM; make sure it fully released the A100 before we load the
# model for training, or the trainer OOMs on a GPU that still looks occupied.
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_gpu.sh"
free_gpu "before training" || true

# Checkpoints and the final adapter are written straight to EOS.
uv run python -m neuroagent.training.train_grpo \
    --stage sft \
    --model "$MODEL" \
    --data "$DATA" \
    --output "$EOS_DIR" \
    --lora-rank 64 \
    --lora-alpha 128 \
    --epochs "$EPOCHS" \
    --batch-size "$BATCH" \
    --grad-accum "$GRAD_ACCUM" \
    --lr "$LR" \
    --optim "$OPTIM" \
    --top-fraction 1.0 \
    --max-seq-length "$MAX_SEQ" \
    --splits-dir "$SPLITS" \
    --val-fraction 0.1 \
    --early-stopping-patience 1 \
    --max-steps "${MAX_STEPS:--1}" \
    $QLORA_FLAG

echo ""
echo "Adapter + run_summary.json on EOS: $EOS_DIR"
echo "========================================="
echo " Done. End: $(date)"
echo "========================================="
