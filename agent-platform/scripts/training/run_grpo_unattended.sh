#!/bin/bash
# Unattended sequential MULTI-TURN GRPO: 4B first, then 9B. Built to run for days with nobody
# watching. Everything that has bitten a long run before is handled here explicitly:
#
#   * Kerberos ticket kept alive so EOS checkpoint writes do not die mid-run. A background loop
#     renews it (from a KEYTAB if you made one — indefinite; otherwise `kinit -R`, which only
#     covers the ticket's ~4-day renewable window). SEE THE KEYTAB NOTE printed at startup.
#   * GPU drained and VERIFIED EMPTY between every phase. HF training and the model swap cannot
#     share the card; a process that has not fully released would OOM the next run. We poll
#     nvidia-smi until memory actually drops, not just assume it.
#   * 9B auto-fallback: multi-turn at G=4/8192 may not fit the 9B on one 40GB card. If it OOMs
#     before making progress, the run retries at a smaller group / completion budget, so the 9B
#     trains at the largest config that FITS instead of crashing. The 4B uses the validated recipe.
#   * Continue-on-failure: the 9B is attempted even if the 4B fails. Every outcome is logged and
#     written to a STATUS file you can `cat` when you check in.
#   * The previous grpo_<model> adapter (if any) is archived aside, never overwritten, so this is
#     a clean run and nothing is lost.
#
# HOW TO LAUNCH (must survive your SSH disconnect):
#     tmux new -s grpo
#     bash agent-platform/scripts/training/run_grpo_unattended.sh
#     # detach: Ctrl-b then d.  reattach: tmux attach -t grpo
#   or fully detached:
#     nohup bash agent-platform/scripts/training/run_grpo_unattended.sh >/dev/null 2>&1 &
#
# CHECK IN:   cat results/grpo_unattended_*/STATUS.txt
set -uo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"     # repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ----------------------------------------------------------------------------- config
EOS_ROOT="${EOS_ROOT:-/eos/project-d/diagbox/dvc/NeuroAgent}"
CKPT_ROOT="$EOS_ROOT/checkpoints"
PRINCIPAL="${KRB_PRINCIPAL:-$(klist 2>/dev/null | awk '/Default principal/{print $3}')}"
# A keytab makes renewal indefinite and passwordless. Create one BEFORE leaving with ktutil
# (NOT cern-get-keytab — that is for host/service accounts and can reset your AD password):
#   ktutil
#     addent -password -p <you>@CERN.CH -k 1 -e aes256-cts-hmac-sha1-96   # password once
#     wkt $HOME/krb5.keytab
#     quit
#   chmod 600 $HOME/krb5.keytab
# It is then found automatically here. No keytab? The loop still renews the existing ticket,
# but only within its ~4-7 day renewable window (widen it first with:  kinit -r 7d).
KEYTAB="${KEYTAB:-$HOME/krb5.keytab}"
MODELS=("Qwen3.5-4B" "Qwen3.5-9B")
EPOCHS="${EPOCHS:-1}"                # 1 epoch ~= the ~250-step GRPO target
MAX_STEPS="${MAX_STEPS:--1}"         # -1 = full epoch; set e.g. 200 to cap wall-clock
EVAL_AFTER="${EVAL_AFTER:-0}"        # 0 = train only (fewest GPU swaps, most robust). 1 = also eval+compare.
FORCE_RETRAIN="${FORCE_RETRAIN:-1}"  # 1 = archive any existing grpo_<model> and retrain fresh

STAMP="$(date +%Y%m%d_%H%M%S)"
RUN_ROOT="results/grpo_unattended_$STAMP"
mkdir -p "$RUN_ROOT"
MASTER_LOG="$RUN_ROOT/master.log"
STATUS_FILE="$RUN_ROOT/STATUS.txt"

log()  { echo "[$(date '+%F %T')] $*" | tee -a "$MASTER_LOG"; }
stat() { echo "[$(date '+%F %T')] $*" >  "$STATUS_FILE"; log "STATUS → $*"; }

# ----------------------------------------------------------------------------- kerberos renewal
# Keep the TGT (and any AFS token) fresh so EOS stays writable for the whole run.
renew_once() {
  if [ -f "$KEYTAB" ] && [ -n "$PRINCIPAL" ]; then
    kinit -k -t "$KEYTAB" "$PRINCIPAL" >>"$RUN_ROOT/renew.log" 2>&1 || true   # keytab: indefinite
  else
    kinit -R >>"$RUN_ROOT/renew.log" 2>&1 || true                            # renew existing: ~4d cap
  fi
  command -v aklog >/dev/null 2>&1 && aklog >>"$RUN_ROOT/renew.log" 2>&1 || true
}
renew_daemon() { while true; do renew_once; sleep 1800; done; }   # every 30 min

# ----------------------------------------------------------------------------- gpu drain (verified)
# Kill any lingering trainer and WAIT until the card is actually empty. Matches the python module
# name only, so it never touches this script or the renewal loop.
ensure_gpu_free() {
  local why="${1:-between phases}" used=""
  log "Draining GPU ($why)…"
  pkill -9 -f "neuroagent.training.train_grpo" 2>/dev/null || true
  pkill -9 -f "vllm_serve.py" 2>/dev/null || true
  pkill -9 -f "EngineCore"    2>/dev/null || true
  sleep 8
  for _ in $(seq 1 90); do          # up to 15 min for CUDA to release
    used="$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1)"
    used="${used//[!0-9]/}"
    if [ -n "$used" ] && [ "$used" -lt 2000 ]; then
      log "GPU free (${used} MiB used)."
      return 0
    fi
    sleep 10
  done
  log "WARNING: GPU still ${used:-?} MiB after drain. Holding processes:"
  nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader 2>&1 | tee -a "$MASTER_LOG"
  return 1
}

# ----------------------------------------------------------------------------- one training attempt
# Args: TAG, then env overrides as NAME=VALUE... . Returns 0 on success. Writes to a per-attempt log.
# Distinguishes an EARLY OOM (config too big → caller should shrink) from any other exit.
attempt_train() {
  local tag="$1"; shift
  local out="$CKPT_ROOT/grpo_${tag}"
  local logf="$RUN_ROOT/train_${tag}_$(date +%H%M%S).log"
  log "[$tag] training → $logf   env: $*"
  # Run through the normal script so staging, FLA_TILELANG, GPUfree, promotion all apply.
  # shellcheck disable=SC2086
  env MULTI_TURN=1 PRECISION=qlora EPOCHS="$EPOCHS" MAX_STEPS="$MAX_STEPS" \
      OUT_DIR="$out" LOG_FILE="$logf" "$@" \
      bash "$SCRIPT_DIR/run_grpo_training.sh" "$tag" >>"$MASTER_LOG" 2>&1
  local rc=$?
  if [ $rc -eq 0 ]; then log "[$tag] training OK"; return 0; fi
  # non-zero: was it an early OOM (before step 2)?  grep the verbose file the run wrote.
  local oom steps
  oom=$(grep -cE "OutOfMemoryError|CUDA out of memory" "$logf" 2>/dev/null || echo 0)
  steps=$(grep -cE "step [0-9]+ metrics" "$logf" 2>/dev/null || echo 0)
  if [ "$oom" -gt 0 ] && [ "$steps" -lt 2 ]; then
    log "[$tag] EARLY OOM (rc=$rc, steps=$steps) — config too large."
    return 20   # sentinel: caller should try a smaller config
  fi
  log "[$tag] training FAILED (rc=$rc, oom=$oom, steps=$steps) — not an early OOM, not retrying."
  return $rc
}

archive_old_output() {
  local tag="$1" out="$CKPT_ROOT/grpo_${tag}"
  if [ "$FORCE_RETRAIN" = 1 ] && [ -e "$out" ]; then
    local arch="${out}_pre_${STAMP}"
    log "[$tag] archiving existing adapter → $arch"
    mv "$out" "$arch" 2>>"$MASTER_LOG" || log "[$tag] WARN: could not archive old output"
  fi
}

# ----------------------------------------------------------------------------- optional eval
run_eval() {
  local tag="$1" key; key="$(echo "$tag" | tr '[:upper:]' '[:lower:]')"
  ensure_gpu_free "before $tag eval" || { log "[$tag] eval skipped: GPU not free"; return 1; }
  local root="results/grpo_eval/${tag}" sft_root="results/definitive_eval/${tag}"
  mkdir -p "$root/greedy" "$root/sampled"
  for s in greedy sampled; do
    local src="$sft_root/$s/base-${key}_results.json" dst="$root/$s/base-${key}_results.json"
    [ -f "$src" ] && [ ! -f "$dst" ] && cp "$src" "$dst"
  done
  log "[$tag] agent eval of the GRPO adapter (presence_penalty=0.5, timeout=300, think template)"
  # PRESENCE_PENALTY=0.5: the sampled arm's default 1.5 left the 9B with empty final answers.
  ADAPTER="$CKPT_ROOT/grpo_${tag}" ROOT="$root" CONCURRENCY="${CONCURRENCY:-8}" \
    PRESENCE_PENALTY="${PRESENCE_PENALTY:-0.5}" REQUEST_TIMEOUT="${REQUEST_TIMEOUT:-300}" \
    bash "$SCRIPT_DIR/run_definitive_eval.sh" "$tag" >>"$MASTER_LOG" 2>&1 \
    || { log "[$tag] eval FAILED — the adapter is safe on EOS."; return 1; }
  for s in greedy sampled; do
    local sft_res="$sft_root/$s/sft-${key}_results.json" grpo_res="$root/$s/sft-${key}_results.json"
    [ -f "$sft_res" ] && [ -f "$grpo_res" ] && \
      uv run python "$SCRIPT_DIR/run_sft_eval_cases.py" compare \
        --base-results "$sft_res" --sft-results "$grpo_res" \
        --output "$root/$s/sft_vs_grpo.json" >>"$MASTER_LOG" 2>&1 || true
  done
  log "[$tag] eval done → $root/*/sft_vs_grpo.json"
}

# ============================================================================= run
renew_once
renew_daemon & KRB_PID=$!
trap 'kill $KRB_PID 2>/dev/null || true' EXIT

stat "starting; principal=${PRINCIPAL:-UNKNOWN}"
log  "run dir: $RUN_ROOT   status: $STATUS_FILE"
if [ -f "$KEYTAB" ]; then
  log "Kerberos: KEYTAB found ($KEYTAB) → renewal is INDEFINITE. Good for a multi-day run."
else
  renew_line="$(klist 2>/dev/null | awk '/renew until/{print; exit}')"
  log "Kerberos: NO KEYTAB. Renewing the existing ticket only — capped at its renewable window:"
  log "          ${renew_line:-<none>}"
  log "  ┌ IMPORTANT: two full multi-turn runs likely EXCEED that window. If EOS dies mid-9B,"
  log "  │ checkpoints stop saving. For INDEFINITE passwordless renewal, BEFORE leaving make a"
  log "  │ keytab once:  ktutil → addent -password -p ${PRINCIPAL:-<you>@CERN.CH} -k 1 -e aes256-cts-hmac-sha1-96"
  log "  │               → wkt \$HOME/krb5.keytab → quit ; chmod 600 \$HOME/krb5.keytab"
  log "  └ then relaunch (auto-detected). Or, for a shorter run, widen the window: kinit -r 7d."
fi

# preflight: EOS writable + both SFT adapters present + models staged + GPU free
tf="$CKPT_ROOT/.write_test_$$"; if touch "$tf" 2>/dev/null; then rm -f "$tf"; log "EOS writable ✓";
  else stat "ABORT: EOS not writable (kinit?)"; exit 1; fi
for tag in "${MODELS[@]}"; do
  [ -f "$CKPT_ROOT/sft_${tag}/adapter_model.safetensors" ] || { stat "ABORT: no SFT adapter for $tag"; exit 1; }
done
source "$SCRIPT_DIR/_stage.sh" 2>/dev/null || true
for tag in "${MODELS[@]}"; do
  log "staging base $tag to /dev/shm (idempotent)…"
  stage_base "Qwen/$tag" >>"$MASTER_LOG" 2>&1 || log "WARN: staging $tag returned non-zero"
done
ensure_gpu_free "startup" || log "WARN: GPU not clean at startup; continuing"

declare -A RESULT
for tag in "${MODELS[@]}"; do
  stat "TRAIN $tag (epochs=$EPOCHS max_steps=$MAX_STEPS)"
  ensure_gpu_free "before $tag" || log "[$tag] WARN: GPU not clean before start"
  archive_old_output "$tag"

  if [ "$tag" = "Qwen3.5-4B" ]; then
    # validated recipe = run_grpo_training.sh multi-turn defaults (G=4/8192/per-turn3072/32ch)
    if attempt_train "$tag"; then RESULT[$tag]="trained"; else RESULT[$tag]="TRAIN_FAILED"; fi
  else
    # 9B: try largest first, auto-shrink on an early OOM. "G MAXCOMP CHUNKS GRAD_ACCUM"
    NINE_CONFIGS=("4 8192 64 2" "2 8192 64 4" "2 4096 64 4")
    RESULT[$tag]="TRAIN_FAILED"
    for cfg in "${NINE_CONFIGS[@]}"; do
      read -r g mc ch ga <<<"$cfg"
      ensure_gpu_free "before $tag (G=$g comp=$mc)" || true
      log "[$tag] attempting G=$g MAX_COMPLETION=$mc LOGIT_CHUNKS=$ch GRAD_ACCUM=$ga"
      attempt_train "$tag" NUM_GENERATIONS="$g" MAX_COMPLETION="$mc" LOGIT_CHUNKS="$ch" GRAD_ACCUM="$ga"
      rc=$?
      if [ $rc -eq 0 ]; then RESULT[$tag]="trained (G=$g comp=$mc)"; break; fi
      if [ $rc -eq 20 ]; then log "[$tag] shrinking config and retrying…"; archive_old_output "$tag"; continue; fi
      RESULT[$tag]="TRAIN_FAILED (rc=$rc)"; break   # non-OOM failure: stop retrying
    done
  fi

  if [ "$EVAL_AFTER" = 1 ] && [[ "${RESULT[$tag]}" == trained* ]]; then
    stat "EVAL $tag"
    run_eval "$tag" && RESULT[$tag]="${RESULT[$tag]} + evaluated" || RESULT[$tag]="${RESULT[$tag]} + eval_failed"
  fi
  ensure_gpu_free "after $tag" || true
  log "[$tag] outcome: ${RESULT[$tag]}"
done

# ----------------------------------------------------------------------------- summary
{
  echo "=== GRPO unattended run complete: $(date) ==="
  for tag in "${MODELS[@]}"; do
    echo "  $tag: ${RESULT[$tag]:-not run}"
    echo "     adapter: $CKPT_ROOT/grpo_${tag}/adapter_model.safetensors"
  done
  [ "$EVAL_AFTER" = 1 ] && echo "  comparisons: results/grpo_eval/*/{greedy,sampled}/sft_vs_grpo.json"
  echo "  full log: $MASTER_LOG"
} | tee -a "$MASTER_LOG"
stat "DONE — $(for t in "${MODELS[@]}"; do echo -n "$t=${RESULT[$t]:-?}; "; done)"
