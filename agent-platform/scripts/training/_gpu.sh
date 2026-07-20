# Shared GPU environment + teardown, sourced by the training and eval scripts.
#
# Qwen3.5's gated-delta-rule layers run through flash-linear-attention, whose TileLang backend
# shells out to the pip-installed CUDA 13 nvcc; that nvcc rejects its own bundled headers here
# ("CUDA compiler and CUDA toolkit headers are incompatible"). It fails only in the BACKWARD
# kernel, so a run loads the model, generates, completes a rollout, and then dies in
# loss.backward(). Pin fla to Triton, its reference backend: measured finite forward+backward,
# forward within 4.8e-3 of fla's independent recurrent implementation, gradient within 3.5e-2
# of a finite-difference check of its own forward. Not overridden if already set.
export FLA_TILELANG="${FLA_TILELANG:-0}"
#
# The eval serves with vLLM and training loads with HuggingFace; only one can hold the A100 at
# a time. vLLM spawns an EngineCore child that does not always die with its launcher, so a
# plain `pkill` can leave ~10GB pinned and OOM the next phase. free_gpu() kills the vLLM
# processes and then WAITS until the GPU memory is actually released — a verify, not a hope.

# ui_* come from _ui.sh when the caller sourced it; plain fallbacks otherwise.
type ui_step >/dev/null 2>&1 || { ui_step(){ echo "▶ $*"; }; ui_ok(){ echo "✓ $*"; }; ui_warn(){ echo "⚠ $*" >&2; }; ui_err(){ echo "✗ $*" >&2; }; ui_info(){ echo "  $*"; }; }

# Kill this project's vLLM processes and block until the GPU is (almost) empty.
free_gpu() {
  local reason="${1:-switching phase}"
  ui_step "Freeing GPU ($reason)…"

  # SIGTERM first (clean shutdown), then SIGKILL the stragglers. "EngineCore" is vLLM-specific,
  # so this never touches another user's job.
  pkill -f "vllm_serve.py"      2>/dev/null || true
  pkill -f "EngineCore"         2>/dev/null || true
  sleep 3
  pkill -9 -f "vllm_serve.py"   2>/dev/null || true
  pkill -9 -f "EngineCore"      2>/dev/null || true

  # Wait for the memory to actually drop. CUDA release lags the process exit.
  local used
  for _ in $(seq 1 40); do
    used="$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1)"
    used="${used//[!0-9]/}"
    if [ -n "$used" ] && [ "$used" -lt 1500 ]; then
      ui_ok "GPU free (${used} MiB used)"
      return 0
    fi
    sleep 3
  done

  # Still occupied — report exactly what, so a stuck run is diagnosable rather than a silent OOM.
  ui_warn "GPU still shows ${used:-?} MiB after teardown. Holding processes:"
  nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader 2>/dev/null >&2 || true
  return 1
}
