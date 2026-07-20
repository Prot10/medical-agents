#!/bin/bash
# GRPO from the SFT checkpoint, on the 500-case TRAIN split.
#
#   bash agent-platform/scripts/training/run_grpo_training.sh Qwen3.5-4B
#   bash agent-platform/scripts/training/run_grpo_training.sh Qwen3.5-9B
#
# The policy starts from the SFT LoRA adapter on EOS and keeps training that SAME adapter
# (PeftModel is_trainable=True) — SFT -> GRPO, the standard order. Rewards are computed
# ONLINE by CompositeReward (config/training/reward_weights.yaml) against each case's
# ground truth: correctness, actions, safety, cost, compliance, format.
#
# Scope, stated plainly: TRL's GRPOTrainer samples completions in ONE shot. The model
# writes its reasoning and its <tool_call> blocks in a single pass and never sees a tool
# RESPONSE. So this optimises a one-shot "triage and order the right workup" policy, not
# the multi-turn ReAct loop the agent is evaluated with. It is the right lever for tool
# selection / safety / cost; it cannot teach the model to react to a tool result.
#
# Base weights load from RAM (/dev/shm, staged from EOS); the adapter is written to EOS.
set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"  # repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_ui.sh"

MODEL_TAG="${1:-Qwen3.5-9B}"
BASE_MODEL="Qwen/$MODEL_TAG"

EOS_ROOT="${EOS_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent}"
CHECKPOINTS_ROOT="${CHECKPOINTS_ROOT:-$EOS_ROOT/checkpoints}"
SFT_ADAPTER="${SFT_ADAPTER:-$CHECKPOINTS_ROOT/sft_${MODEL_TAG}}"
OUT_DIR="${OUT_DIR:-$CHECKPOINTS_ROOT/grpo_${MODEL_TAG}}"
DATA="${DATA:-data/neurobench/grpo/train_prompts.jsonl}"
# Held-out validation, same 100-case TEST split the SFT eval uses. GRPO has no eval_loss, so
# the metric is the mean reward on prompts the policy never trains on, and the best-scoring
# checkpoint is the one kept.
EVAL_DATA="${EVAL_DATA:-data/neurobench/grpo/test_prompts.jsonl}"
EVAL_SUBSET="${EVAL_SUBSET:-20}"   # evaluation generates, so it costs like training per prompt
EVAL_STEPS="${EVAL_STEPS:-40}"

# Memory knobs. Generation is the peak: the completions are decoded (with a KV cache on top
# of a ~6k-token prompt) before any backward pass — so the group size and the completion
# cap, not the weights, decide whether this fits in 40GB. Measured peaks are in
# docs/training/grpo-recipe.md; PRECISION=qlora buys back ~13GB on the 9B.
PRECISION="${PRECISION:-bf16}"
case "$PRECISION" in
  qlora) QLORA_FLAG="--qlora" ;;
  bf16)  QLORA_FLAG="" ;;
  *) ui_err "PRECISION must be bf16 or qlora (got '$PRECISION')"; exit 1 ;;
esac

# Recipe tuned after the first run's reward barely moved. The changes and their sources:
#   G=6       every published GRPO recipe uses >=8, but HF `generate` re-prefills the identical
#             ~6k-token prompt once PER completion (vLLM would dedupe via prefix caching; it is
#             not in the training venv), so G is capped by generation memory. Measured on the 9B
#             QLoRA: G=4 -> 25 GB, G=6 -> 32.7 GB (83%), G=8 -> OOM. G=6 is the ceiling; still a
#             50% larger, less noisy reward group than the first run's G=4. The 4B (smaller base,
#             bf16) has room for G=8 and run_grpo_both.sh uses it there.
#   KL=0      TRL's own default and DAPO both drop the KL term; a KL leash to the SFT prior
#             works against moving in reward space. Also skips the reference forward -> memory.
#   LR 1e-5   3e-6 is a full-FT rate; a rank-64 LoRA adapter wants ~1e-5 (Unsloth practice).
#   1 epoch   the research wants >=300 optimiser steps, but HF `generate` re-prefills the 6k
#             prompt PER completion (no prefix caching without vLLM), so a group of G takes
#             ~80s (4B) / ~120s (9B). At that rate 3 epochs is ~33h/50h — impractical. 1 epoch
#             with grad_accum=2 gives 250 optimiser steps in ~11h (4B) / ~17h (9B), close to
#             the step target within a tractable budget. GRAD_ACCUM=2 (not 4) buys more steps
#             from the one pass. The path to the full recipe is vLLM-in-the-loop generation
#             (prefix-caches the shared prompt, ~5x faster) — see docs/training/grpo-recipe.md.
#   comp 512  measured single-turn completions are ~290-350 tokens, so 1024 was wasted KV cache;
#             512 is ample and halves the generation peak, which is what lets G=8 fit.
# GSPO (sequence-level IS) and scale_rewards=none are set in train_grpo.py's GRPOConfig.
# MULTI_TURN=1 drives the real multi-turn ReAct loop (the "grouped" GRPO). The completion
# then holds several assistant turns PLUS the (masked) tool outputs, so it needs a much larger
# budget than the one-shot plan, and the bigger sequences want a smaller reward group.
MULTI_TURN="${MULTI_TURN:-0}"
if [ "$MULTI_TURN" = 1 ]; then
  NUM_GENERATIONS="${NUM_GENERATIONS:-4}"    # longer multi-turn sequences → smaller group
  # 4096 is the MEASURED ceiling on the 40GB A100 at G=4: it completed 2 steps at a 37.3 GB
  # peak (94%), and the peak is GENERATION (G sequences x ~10k tokens of KV cache), not the
  # training forward. Do not raise this without lowering G — 6144 OOMs.
  # It also has to be this large for behavioural reasons: at 2048 the agent managed only 2.5
  # tool calls, vs 4.5/3.5 at 4096 and the ~3.9 it actually uses at eval. Too small a budget
  # silently truncates real agent behaviour rather than just clipping tokens.
  MAX_COMPLETION="${MAX_COMPLETION:-4096}"
  MULTI_TURN_FLAG="--multi-turn"
  # vLLM-accelerated rollouts (colocate — the only single-GPU vLLM mode). Generation is
  # essentially all of a multi-turn step, and HF generate re-prefills the shared ~6.2k prompt
  # once per generation per turn; vLLM prefix-caches it. VLLM_GPU_FRAC is the engine's share of
  # the card, the rest is left for training.
  # MEASURED: colocate does NOT fit at 4B on a 40GB card. The engine's share (~12GB at 0.30)
  # plus training OOMs at 38.9GB in use. This matches HF's own guidance that colocate is
  # practical "up to ~3B on a 24GB GPU". Server mode is not an option either — TRL refuses to
  # share a device with it. So vLLM rollouts need a second GPU; default OFF.
  # Everything is wired and working up to this point (engine init, weight sync, generation,
  # tool execution, sampling logprobs) — only the memory does not fit.
  USE_VLLM="${USE_VLLM:-0}"
  VLLM_GPU_FRAC="${VLLM_GPU_FRAC:-0.30}"
  # Multi-turn reaches a diagnosis, so correctness/format are live components again. The
  # single-turn config zeroes both, which makes a right and a wrong diagnosis score identically.
  REWARD_CONFIG_DEFAULT="agent-platform/config/training/reward_weights_grpo_multiturn.yaml"
else
  NUM_GENERATIONS="${NUM_GENERATIONS:-6}"    # completions per prompt = the reward group (9B ceiling)
  MAX_COMPLETION="${MAX_COMPLETION:-512}"    # one-shot plan: think + tool calls (measured ~290-350 tok)
  MULTI_TURN_FLAG=""
  REWARD_CONFIG_DEFAULT="agent-platform/config/training/reward_weights_grpo.yaml"
fi
GRAD_ACCUM="${GRAD_ACCUM:-2}"                # reward groups accumulated per optimiser step
EPOCHS="${EPOCHS:-1}"
LR="${LR:-1e-5}"                             # rank-64 LoRA wants ~10x a full-FT rate
KL_COEFF="${KL_COEFF:-0}"                    # no KL term (TRL default; DAPO drops it)
REWARD_CONFIG="${REWARD_CONFIG:-$REWARD_CONFIG_DEFAULT}"
HOSPITAL="${HOSPITAL:-de_charite}"           # same rule set as the definitive eval
MAX_STEPS="${MAX_STEPS:--1}"                 # set to 2 for a smoke test

# per_device_train_batch_size defaults to num_generations, keeping one prompt's whole reward
# group in a single forward/backward. It can be set SMALLER for multi-turn: the advantage is
# computed from the rewards (already known before the forward), so splitting the group across
# forwards is safe, and it is the main memory lever — the logits tensor is
# batch x completion_len x 248k-vocab, which dominates everything else on long trajectories.
BATCH_SIZE="${BATCH_SIZE:-$NUM_GENERATIONS}"
# Generation is the memory wall (G sequences x a ~6.2k-token prompt prefilled at once), so the
# generation batch stays at ONE group; gradients are de-noised by accumulating over GRAD_ACCUM
# groups instead of by generating more at once. gen_batch 8 OOM'd at completion 1024; at 512
# (the new default) it fits — verified on the 9B.
# It tracks NUM_GENERATIONS, not BATCH_SIZE: a reward group may never be split across generation
# batches (TRL enforces divisibility), whereas the training-forward batch is free to be smaller.
GEN_BATCH="${GEN_BATCH:-$NUM_GENERATIONS}"

VLLM_FLAGS=""
if [ "${USE_VLLM:-0}" = 1 ]; then
  VLLM_FLAGS="--use-vllm --vllm-gpu-memory-utilization ${VLLM_GPU_FRAC:-0.30}"
fi

[ -f "$SFT_ADAPTER/adapter_model.safetensors" ] || {
  ui_err "no SFT adapter at $SFT_ADAPTER — run run_sft_training.sh first."; exit 1; }
# The prompt datasets are cheap to render and identical for 4B and 9B (same chat template),
# so build them on demand rather than making the run fail on a missing file.
for spec in "train:$DATA" "test:$EVAL_DATA"; do
  split="${spec%%:*}"; path="${spec#*:}"
  [ -f "$path" ] && continue
  ui_step "Building $split prompts → $path"
  uv run python -m neuroagent.training.data.build_grpo_dataset \
      --split "$split" --hospital "$HOSPITAL" --model "$BASE_MODEL" --output "$path" || exit 1
done

source "$SCRIPT_DIR/_stage.sh"
source "$SCRIPT_DIR/_gpu.sh"
stage_base "$BASE_MODEL" || exit 1
free_gpu "before GRPO"

export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export CUDA_MODULE_LOADING=LAZY
export NEUROAGENT_DATASET=data/neurobench   # online reward loads the cases from here
mkdir -p "$OUT_DIR"

# Verbose logs go to a FILE; the terminal keeps the tqdm step bar + the concise reward line.
LOG_FILE="${LOG_FILE:-results/logs/grpo_${MODEL_TAG}_$(date +%Y%m%d_%H%M%S).log}"
mkdir -p "$(dirname "$LOG_FILE")"

ui_panel "GRPO · $MODEL_TAG  ${C_GREY}(from the SFT adapter)${C_RESET}" \
  "precision|$PRECISION" \
  "init|$SFT_ADAPTER" \
  "base|RAM (staged from EOS)" \
  "output|$OUT_DIR ${C_GREY}(EOS)${C_RESET}" \
  "data|$DATA ${C_GREY}hospital=$HOSPITAL${C_RESET}" \
  "reward|online CompositeReward (6 components)" \
  "group|$NUM_GENERATIONS completions × $GRAD_ACCUM prompts = $GEN_BATCH / step" \
  "completion|≤ $MAX_COMPLETION tok   ${C_GREY}LR${C_RESET} $LR   ${C_GREY}KL β${C_RESET} $KL_COEFF" \
  "log|$LOG_FILE ${C_GREY}(verbose → file)${C_RESET}"

uv run python -m neuroagent.training.train_grpo \
    --stage grpo \
    --model "$SFT_ADAPTER" \
    --base-model "$BASE_MODEL" \
    --data "$DATA" \
    --output "$OUT_DIR" \
    --hospital "$HOSPITAL" \
    --reward-config "$REWARD_CONFIG" \
    --tool-costs agent-platform/config/tools/costs.yaml \
    --rules-dir agent-platform/config/hospital_rules \
    --epochs "$EPOCHS" \
    --batch-size "$BATCH_SIZE" \
    --grad-accum "$GRAD_ACCUM" \
    --num-generations "$NUM_GENERATIONS" \
    --generation-batch-size "$GEN_BATCH" \
    --max-completion-length "$MAX_COMPLETION" \
    --lr "$LR" \
    --kl-coeff "$KL_COEFF" \
    --max-steps "$MAX_STEPS" \
    --eval-data "$EVAL_DATA" \
    --eval-subset "$EVAL_SUBSET" \
    --eval-steps "$EVAL_STEPS" \
    --log-file "$LOG_FILE" \
    $MULTI_TURN_FLAG $VLLM_FLAGS \
    $QLORA_FLAG
STATUS=$?

echo ""
if [ $STATUS -eq 0 ]; then
  ui_ok "GRPO complete — adapter + run_summary.json on EOS: $OUT_DIR"
else
  ui_err "GRPO FAILED (exit $STATUS)"
fi
ui_info "End: $(date)"
exit $STATUS
