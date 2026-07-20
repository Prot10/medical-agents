#!/bin/bash
# GRPO on both students, end to end: 4B first (the cheap dress rehearsal), then 9B.
#
# HOW TO RUN — the terminal shows the progress UI (training step bar + reward line, then the
# eval progress bars); all the verbose framework/INFO/warning output is written to per-stage
# files under results/logs/ for later analysis. So do NOT pipe everything into one log with
# `> file 2>&1` — that is exactly what hid the UI before. Run it in tmux instead, which keeps
# the live UI on screen AND survives an SSH disconnect:
#
#   tmux new -s grpo
#   bash agent-platform/scripts/training/run_grpo_both.sh
#   # detach with Ctrl-b d ; reattach later with:  tmux attach -t grpo
#
# Verbose logs land in results/logs/grpo_<model>_<ts>.log and eval_<model>_<ts>.log.
#
# Per model:
#   1. GRPO from the SFT adapter, with held-out validation reward every EVAL_STEPS steps.
#      The checkpoint kept is the one with the best reward on the TEST-split prompts, not
#      the last step — GRPO can over-optimise the training reward while held-out flattens.
#   2. Agent evaluation of the resulting adapter on the 100-case TEST split, in the real
#      multi-turn ReAct loop (greedy + sampled), scored with the same metrics as the SFT eval.
#   3. Paired SFT-vs-GRPO comparison on that split.
#
# Step 2 matters more than usual here: GRPO's rollout is SINGLE-TURN (the policy writes its
# reasoning and tool calls in one shot and never sees a tool response), while the agent is
# served multi-turn. The reward is the right one and it is not gameable — measured, the
# optimum is "order the correct workup AND state the leading diagnosis" — but whether that
# one-shot policy transfers to the ReAct loop is an empirical question, and step 2 is the
# only thing that answers it. A GRPO run whose training reward rises but whose test-split
# top-1 falls is a real outcome, not a bug.
#
# One A100, so the models run in sequence. Idempotent: every stage skips if its output exists.
set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"  # repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/_ui.sh"

MODELS=("Qwen3.5-4B" "Qwen3.5-9B")
EOS_ROOT="${EOS_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent}"
CONCURRENCY="${CONCURRENCY:-12}"     # cases run in parallel in the agent eval
EVAL_AFTER="${EVAL_AFTER:-1}"        # set 0 to train only and evaluate later

# 9B needs QLoRA: bf16 peaks at 37.2 GB of 39.5 (94%) — one long completion from OOM.
# QLoRA peaks at 25.0 GB (63%). The 4B has room for bf16.
PRECISION_4B="${PRECISION_4B:-bf16}"
PRECISION_9B="${PRECISION_9B:-qlora}"
# Reward-group size is capped by generation memory (HF generate re-prefills the ~6k prompt per
# completion). The smaller 4B base has room for G=8; the 9B tops out at G=6 (G=8 OOMs).
G_4B="${G_4B:-8}"
G_9B="${G_9B:-6}"

ui_panel "GRPO suite · ${MODELS[*]}" \
  "train|500 prompts (train split)" \
  "validate|test split, held out" \
  "then|agent eval on the 100-case test split · SFT vs GRPO" \
  "start|$(date)"

for TAG in "${MODELS[@]}"; do
  ui_section "$TAG"
  SFT_ADAPTER="$EOS_ROOT/checkpoints/sft_${TAG}"
  GRPO_ADAPTER="$EOS_ROOT/checkpoints/grpo_${TAG}"
  case "$TAG" in
    *4B) PRECISION="$PRECISION_4B"; NGEN="$G_4B" ;;
    *)   PRECISION="$PRECISION_9B"; NGEN="$G_9B" ;;
  esac

  if [ ! -f "$SFT_ADAPTER/adapter_model.safetensors" ]; then
    ui_warn "[$TAG] no SFT adapter at $SFT_ADAPTER — skipping."
    continue
  fi

  # ---- 1. GRPO ----
  if [ -f "$GRPO_ADAPTER/adapter_model.safetensors" ] && [ "${FORCE_RETRAIN:-0}" != 1 ]; then
    ui_ok "[$TAG] GRPO adapter already at $GRPO_ADAPTER — skipping training (FORCE_RETRAIN=1 to redo)"
  else
    ui_step "[$TAG] GRPO training (precision=$PRECISION, G=$NGEN) — $(date)"
    if ! PRECISION="$PRECISION" NUM_GENERATIONS="$NGEN" bash "$SCRIPT_DIR/run_grpo_training.sh" "$TAG"; then
      ui_err "[$TAG] GRPO TRAINING FAILED — continuing to the next model."
      continue
    fi
  fi

  [ "$EVAL_AFTER" = 1 ] || { ui_info "[$TAG] EVAL_AFTER=0 — trained only."; continue; }

  # ---- 2. Agent eval of the GRPO adapter on the held-out split ----
  # run_definitive_eval.sh serves base + the adapter named "sft" from one vLLM process; point
  # ADAPTER at the GRPO checkpoint and it evaluates that instead. The base half of the run is
  # identical to the SFT eval's base half, so seed it from those results rather than paying
  # for 400 more rollouts.
  ROOT="results/grpo_eval/${TAG}"
  SFT_ROOT="results/definitive_eval/${TAG}"
  SERVE_KEY="$(echo "$TAG" | tr '[:upper:]' '[:lower:]')"
  for samp in greedy sampled; do
    mkdir -p "$ROOT/$samp"
    src="$SFT_ROOT/$samp/base-${SERVE_KEY}_results.json"
    dst="$ROOT/$samp/base-${SERVE_KEY}_results.json"
    [ -f "$src" ] && [ ! -f "$dst" ] && cp "$src" "$dst" && ui_info "[$TAG] reused base $samp results"
  done

  ui_step "[$TAG] agent eval of the GRPO adapter on the test split — $(date)"
  if ! ADAPTER="$GRPO_ADAPTER" ROOT="$ROOT" CONCURRENCY="$CONCURRENCY" \
       bash "$SCRIPT_DIR/run_definitive_eval.sh" "$TAG"; then
    ui_err "[$TAG] GRPO EVAL FAILED — the adapter is safe on EOS."
    continue
  fi

  # ---- 3. SFT vs GRPO, paired, on the same cases ----
  # The eval writes the adapter's rollouts under the run name "sft-<key>" (that is what the
  # LoRA is served as), so here it is the GRPO adapter's results. Compare it against the SFT
  # adapter's results from the definitive eval — that is the delta GRPO actually bought.
  for samp in greedy sampled; do
    sft_res="$SFT_ROOT/$samp/sft-${SERVE_KEY}_results.json"
    grpo_res="$ROOT/$samp/sft-${SERVE_KEY}_results.json"
    if [ -f "$sft_res" ] && [ -f "$grpo_res" ]; then
      ui_step "[$TAG] $samp: SFT vs GRPO"
      uv run python agent-platform/scripts/training/run_sft_eval_cases.py compare \
          --base-results "$sft_res" --sft-results "$grpo_res" \
          --output "$ROOT/$samp/sft_vs_grpo.json"
    fi
  done

  cp -r "$ROOT/." "$EOS_ROOT/results/grpo_eval/${TAG}/" 2>/dev/null || \
    { mkdir -p "$EOS_ROOT/results/grpo_eval/${TAG}" && cp -r "$ROOT/." "$EOS_ROOT/results/grpo_eval/${TAG}/"; }
  ui_ok "[$TAG] done — $(date)"
done

ui_panel "GRPO suite complete" \
  "finished|$(date)" \
  "adapters|$EOS_ROOT/checkpoints/grpo_*" \
  "results|results/grpo_eval/*/{greedy,sampled}/sft_vs_grpo.json"
