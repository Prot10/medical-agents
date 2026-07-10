# Shared GPU teardown, sourced by the training and eval scripts.
#
# The eval serves with vLLM and training loads with HuggingFace; only one can hold the A100 at
# a time. vLLM spawns an EngineCore child that does not always die with its launcher, so a
# plain `pkill` can leave ~10GB pinned and OOM the next phase. free_gpu() kills the vLLM
# processes and then WAITS until the GPU memory is actually released — a verify, not a hope.

# Kill this project's vLLM processes and block until the GPU is (almost) empty.
free_gpu() {
  local reason="${1:-switching phase}"
  echo "▶ Freeing GPU ($reason)..."

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
      echo "✓ GPU free (${used} MiB used)"
      return 0
    fi
    sleep 3
  done

  # Still occupied — report exactly what, so a stuck run is diagnosable rather than a silent OOM.
  echo "WARNING: GPU still shows ${used:-?} MiB after teardown. Holding processes:" >&2
  nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader 2>/dev/null >&2 || true
  return 1
}
