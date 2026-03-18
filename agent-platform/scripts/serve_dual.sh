#!/usr/bin/env bash
# Launch both orchestrator and specialist models simultaneously for dual-model mode.
#
# Usage:
#   ./agent-platform/scripts/serve_dual.sh                           # defaults: qwen3.5-27b-awq + medgemma-4b
#   ./agent-platform/scripts/serve_dual.sh qwen3.5-9b medgemma-4b   # custom models
#
# Memory split on A100-40GB:
#   Orchestrator (port 8000): 58% GPU memory (~23 GB)
#   Specialist   (port 8001): 35% GPU memory (~14 GB)
#   Overhead:                  7% (~3 GB)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

ORCHESTRATOR_MODEL="${1:-qwen3.5-27b-awq}"
SPECIALIST_MODEL="${2:-medgemma-4b}"
ORCHESTRATOR_PORT=8000
SPECIALIST_PORT=8001
ORCHESTRATOR_GPU_MEM=0.58
SPECIALIST_GPU_MEM=0.35

log() { echo -e "\033[1;36m[dual] $1\033[0m"; }
warn() { echo -e "\033[1;33m[dual] ⚠ $1\033[0m"; }
err() { echo -e "\033[1;31m[dual] ✗ $1\033[0m"; }
ok() { echo -e "\033[1;32m[dual] ✓ $1\033[0m"; }

# Kill all vLLM processes and free GPU
nuke_all() {
    pkill -9 -f "vllm_serve.py" 2>/dev/null || true
    pkill -9 -f "VLLM::EngineCore" 2>/dev/null || true
    nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null | tr -d ' ' | xargs kill -9 2>/dev/null || true
    sleep 3
}

wait_for_health() {
    local port="$1"
    local name="$2"
    local max_wait=420
    local elapsed=0
    echo -n "  Waiting for $name (port $port)"
    while ! curl -sf "http://localhost:${port}/health" > /dev/null 2>&1; do
        if [ $elapsed -ge $max_wait ]; then
            echo ""
            err "$name did not start within ${max_wait}s"
            return 1
        fi
        echo -n "."
        sleep 3
        elapsed=$((elapsed + 3))
    done
    echo " ready! (${elapsed}s)"
}

cleanup() {
    trap - EXIT INT TERM
    echo ""
    warn "Shutting down both models..."
    nuke_all
    echo "Done."
    exit 0
}
trap cleanup INT TERM EXIT

# Clean slate
log "Cleaning up existing processes..."
nuke_all

log "Starting dual-model serving"
log "  Orchestrator: $ORCHESTRATOR_MODEL (port $ORCHESTRATOR_PORT, ${ORCHESTRATOR_GPU_MEM} GPU)"
log "  Specialist:   $SPECIALIST_MODEL (port $SPECIALIST_PORT, ${SPECIALIST_GPU_MEM} GPU)"
echo ""

# Start orchestrator
log "Starting orchestrator: $ORCHESTRATOR_MODEL"
GPU_MEMORY_UTILIZATION=$ORCHESTRATOR_GPU_MEM \
    bash "$SCRIPT_DIR/serve_model.sh" "$ORCHESTRATOR_MODEL" "$ORCHESTRATOR_PORT" \
    > "$REPO_ROOT/results/vllm_orchestrator.log" 2>&1 &
ORCH_PID=$!

# Start specialist
log "Starting specialist: $SPECIALIST_MODEL"
GPU_MEMORY_UTILIZATION=$SPECIALIST_GPU_MEM \
    bash "$SCRIPT_DIR/serve_model.sh" "$SPECIALIST_MODEL" "$SPECIALIST_PORT" \
    > "$REPO_ROOT/results/vllm_specialist.log" 2>&1 &
SPEC_PID=$!

# Wait for both to be ready
wait_for_health $ORCHESTRATOR_PORT "$ORCHESTRATOR_MODEL" || { nuke_all; exit 1; }
wait_for_health $SPECIALIST_PORT "$SPECIALIST_MODEL" || { nuke_all; exit 1; }

ok "Both models ready!"
echo ""
log "Orchestrator: http://localhost:$ORCHESTRATOR_PORT/v1  (PID $ORCH_PID)"
log "Specialist:   http://localhost:$SPECIALIST_PORT/v1  (PID $SPEC_PID)"
echo ""
log "Press Ctrl+C to stop both models."

# Wait forever (until Ctrl+C)
wait
