#!/usr/bin/env bash
# Full NeuroBench v4 comparison: 12-tool schema + cost tracking.
#
# Phase 1: Qwen3.5-9B   → react + no-tools
# Phase 2: MedGemma-4B   → no-tools only
# Phase 3: Qwen3.5-27B   → react + no-tools
#
# Default: 30 cases per difficulty (90 total), 3 repeats = 270 executions per model config
# v4 dataset: 200 cases with 12 tools and cost tracking (migrated from v3)
#
# Uses nvidia-smi to reliably kill ALL GPU-holding processes between phases.
#
# Usage:
#   ./agent-platform/scripts/run_v4_full.sh
#   ./agent-platform/scripts/run_v4_full.sh --skip-phase qwen9b          # skip phase 1
#   ./agent-platform/scripts/run_v4_full.sh --skip-phase 1               # same, by number
#   ./agent-platform/scripts/run_v4_full.sh --skip-phase 1 --skip-phase 2  # skip phases 1+2
#   ./agent-platform/scripts/run_v4_full.sh --hospital us_mayo
#   ./agent-platform/scripts/run_v4_full.sh --cases-per-difficulty 10     # smaller run

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

PORT="${VLLM_PORT:-8000}"
HEALTH_URL="http://localhost:${PORT}/health"
VLLM_PID=""

# Default args — v4 dataset, 30 cases per difficulty, separate output
CASES_PER_DIFF=30
REPEATS=3
HOSPITAL="de_charite"
DATASET="v4"
OUTPUT_BASE="results/v4_comparison"
SKIP_PHASES=""  # comma-separated: "1", "1,2", "qwen9b", "medgemma", "qwen27b"

PYTHON_ARGS=()
while [[ $# -gt 0 ]]; do
    case $1 in
        --cases-per-difficulty) CASES_PER_DIFF="$2"; shift 2 ;;
        --repeats)             REPEATS="$2"; shift 2 ;;
        --hospital)            HOSPITAL="$2"; shift 2 ;;
        --dataset)             DATASET="$2"; shift 2 ;;
        --output-dir)          OUTPUT_BASE="$2"; shift 2 ;;
        --skip-phase)          SKIP_PHASES="$SKIP_PHASES,$2"; shift 2 ;;
        *)                     PYTHON_ARGS+=("$1"); shift ;;
    esac
done

should_skip() {
    local phase_num="$1"
    local phase_name="$2"
    [[ "$SKIP_PHASES" == *"$phase_num"* ]] && return 0
    [[ "$SKIP_PHASES" == *"$phase_name"* ]] && return 0
    return 1
}

COMMON_PY_ARGS=(
    --cases-per-difficulty "$CASES_PER_DIFF"
    --repeats "$REPEATS"
    --hospital "$HOSPITAL"
    --dataset "$DATASET"
    "${PYTHON_ARGS[@]}"
)

# ---------------------------------------------------------------------------
# Core function: nuke everything vLLM-related and verify GPU is free
# ---------------------------------------------------------------------------
nuke_vllm() {
    # 1. Kill the tracked parent process
    if [ -n "$VLLM_PID" ] && kill -0 "$VLLM_PID" 2>/dev/null; then
        kill -9 "$VLLM_PID" 2>/dev/null || true
    fi
    VLLM_PID=""

    # 2. Kill by name pattern (catches API server, engine core, resource tracker)
    pkill -9 -f "vllm_serve.py" 2>/dev/null || true
    pkill -9 -f "VLLM::EngineCore" 2>/dev/null || true
    pkill -9 -f "vllm.entrypoints" 2>/dev/null || true

    # 3. Kill anything on our port
    local port_pids
    port_pids=$(lsof -ti :"$PORT" 2>/dev/null || true)
    [ -n "$port_pids" ] && echo "$port_pids" | xargs kill -9 2>/dev/null || true

    # 4. THE RELIABLE WAY: kill whatever nvidia-smi says is on the GPU
    local gpu_pids
    gpu_pids=$(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null | tr -d ' ' || true)
    if [ -n "$gpu_pids" ]; then
        echo "  Killing GPU processes: $gpu_pids"
        echo "$gpu_pids" | xargs kill -9 2>/dev/null || true
    fi

    # 5. Wait and verify GPU is actually free
    local attempt=0
    while [ $attempt -lt 10 ]; do
        sleep 2
        gpu_pids=$(nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null | tr -d ' ' || true)
        if [ -z "$gpu_pids" ]; then
            local used_mb
            used_mb=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1 || echo "0")
            echo "  GPU free (${used_mb}MiB used)"
            return 0
        fi
        echo "  GPU still held by: $gpu_pids — killing again"
        echo "$gpu_pids" | xargs kill -9 2>/dev/null || true
        attempt=$((attempt + 1))
    done
    echo "  WARNING: GPU may not be fully released"
    return 1
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
log() { echo -e "\n\033[1;36m══════ $1 ══════\033[0m\n"; }
warn() { echo -e "\033[1;33m⚠ $1\033[0m"; }
err() { echo -e "\033[1;31m✗ $1\033[0m"; }
ok() { echo -e "\033[1;32m✓ $1\033[0m"; }

wait_for_server() {
    local model_name="$1"
    local max_wait=420
    local elapsed=0
    echo -n "Waiting for vLLM ($model_name) to be ready"
    while ! curl -sf "$HEALTH_URL" > /dev/null 2>&1; do
        if [ -n "$VLLM_PID" ] && ! kill -0 "$VLLM_PID" 2>/dev/null; then
            echo ""
            err "vLLM process died during startup"
            return 1
        fi
        if [ $elapsed -ge $max_wait ]; then
            echo ""
            err "vLLM did not start within ${max_wait}s"
            return 1
        fi
        echo -n "."
        sleep 3
        elapsed=$((elapsed + 3))
    done
    echo " ready! (${elapsed}s)"
}

start_server() {
    local model_name="$1"
    log "Starting vLLM: $model_name (port $PORT)"

    local log_file="$REPO_ROOT/$OUTPUT_BASE/vllm_${model_name}.log"
    mkdir -p "$(dirname "$log_file")"

    bash "$SCRIPT_DIR/serve_model.sh" "$model_name" "$PORT" \
        > "$log_file" 2>&1 &
    VLLM_PID=$!
    echo "vLLM PID: $VLLM_PID (logs: $log_file)"

    if ! wait_for_server "$model_name"; then
        err "Failed to start $model_name — check $log_file"
        nuke_vllm
        return 1
    fi
}

run_phase() {
    local phase_num="$1"
    local model_key="$2"
    local run_label="$3"
    local skip_args="$4"
    local out_subdir="$5"

    log "Phase $phase_num: $run_label"

    if ! start_server "$model_key"; then
        err "Skipping Phase $phase_num — $model_key failed to start"
        return 1
    fi

    # shellcheck disable=SC2086
    uv run python agent-platform/scripts/run_v3_comparison.py \
        $skip_args \
        "${COMMON_PY_ARGS[@]}" \
        --output-dir "$OUTPUT_BASE/$out_subdir" \
        || { err "Phase $phase_num Python script failed"; }

    ok "Phase $phase_num complete"
    log "Stopping $model_key"
    nuke_vllm
}

# Ctrl+C — fast cleanup, no GPU polling loops
cleanup() {
    trap - EXIT INT TERM
    echo ""
    warn "Interrupted! Killing all vLLM processes..."
    [ -n "$VLLM_PID" ] && kill -9 "$VLLM_PID" 2>/dev/null || true
    pkill -9 -f "vllm_serve.py" 2>/dev/null || true
    pkill -9 -f "VLLM::EngineCore" 2>/dev/null || true
    nvidia-smi --query-compute-apps=pid --format=csv,noheader 2>/dev/null | tr -d ' ' | xargs kill -9 2>/dev/null || true
    echo "Cleanup done."
    exit 1
}
trap cleanup INT TERM
trap 'nuke_vllm 2>/dev/null || true' EXIT

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

mkdir -p "$REPO_ROOT/$OUTPUT_BASE"

START_TIME=$(date +%s)
log "NeuroBench v4 Full Comparison — $(date)"
echo "  Cases: $((CASES_PER_DIFF * 3)) ($CASES_PER_DIFF per difficulty)"
echo "  Repeats: $REPEATS"
echo "  Hospital: $HOSPITAL"
echo "  Dataset: $DATASET"
echo "  Output: $OUTPUT_BASE"
echo "  Tools: 12 (v4 schema with cost tracking)"

echo ""
echo "Cleaning up stale processes..."
nuke_vllm

# Phase 1: Qwen3.5-9B
if should_skip 1 "qwen9b"; then
    log "Phase 1: SKIPPED (--skip-phase)"
else
    run_phase 1 "qwen3.5-9b" \
        "Qwen3.5-9B — ReAct + No-Tools" \
        "--skip-model medgemma-4b --skip-model qwen3.5-27b-awq" \
        "qwen3.5-9b"
fi

# Phase 2: MedGemma-4B
if should_skip 2 "medgemma"; then
    log "Phase 2: SKIPPED (--skip-phase)"
else
    run_phase 2 "medgemma-4b" \
        "MedGemma-1.5-4B — No-Tools" \
        "--skip-model qwen3.5-9b --skip-model qwen3.5-27b-awq" \
        "medgemma-4b"
fi

# Phase 3: Qwen3.5-27B-AWQ
if should_skip 3 "qwen27b"; then
    log "Phase 3: SKIPPED (--skip-phase)"
else
    run_phase 3 "qwen3.5-27b-awq" \
        "Qwen3.5-27B-AWQ — ReAct + No-Tools" \
        "--skip-model qwen3.5-9b --skip-model medgemma-4b" \
        "qwen3.5-27b-awq"
fi

# Merge results
log "Merging all results"

uv run python -c "
import json
from pathlib import Path
from collections import defaultdict

out = Path('$OUTPUT_BASE')
subdirs = ['qwen3.5-9b', 'medgemma-4b', 'qwen3.5-27b-awq']
merged = {'config': {}, 'results': [], 'cases_selected': []}

for sd in subdirs:
    f = out / sd / 'comparison_results.json'
    if f.exists():
        data = json.loads(f.read_text())
        merged['results'].extend(data.get('results', []))
        if not merged['cases_selected']:
            merged['cases_selected'] = data.get('cases_selected', [])
        merged['config'].update(data.get('config', {}))

merged['config']['runs'] = sorted(set(r['run_name'] for r in merged['results']))

with open(out / 'merged_results.json', 'w') as f:
    json.dump(merged, f, indent=2, default=str)

by_run = defaultdict(list)
for r in merged['results']:
    by_run[r['run_name']].append(r)

print()
print('=' * 85)
print('  MERGED RESULTS SUMMARY (v4 — 12 tools + cost tracking)')
print('=' * 85)

for run_name in sorted(by_run):
    rr = by_run[run_name]
    n = len(rr)
    if n == 0: continue
    top1 = sum(r['diagnostic_accuracy_top1'] for r in rr)
    top3 = sum(r['diagnostic_accuracy_top3'] for r in rr)
    safety = sum(r['safety_score'] for r in rr) / n
    tools = sum(r['tool_call_count'] for r in rr)
    tokens = sum(r['total_tokens'] for r in rr)
    time_s = sum(r['elapsed_seconds'] for r in rr)
    avg_cost = sum(r.get('total_cost_usd', 0) for r in rr) / n
    avg_eff = sum(r.get('cost_efficiency', 0) for r in rr) / n

    by_case = defaultdict(list)
    for r in rr:
        by_case[r['case_id']].append(r['diagnostic_accuracy_top1'])
    n_cases = len(by_case)
    n_consistent = sum(1 for hits in by_case.values() if all(hits) or not any(hits))

    print(f'''
  {run_name} ({n} runs):
    Top-1 accuracy:  {top1}/{n} ({top1/n:.0%})
    Top-3 accuracy:  {top3}/{n} ({top3/n:.0%})
    Consistency:     {n_consistent}/{n_cases} cases ({n_consistent/n_cases:.0%})
    Mean safety:     {safety:.2f}
    Avg cost/case:   \${avg_cost:,.0f}
    Cost efficiency: {avg_eff:.2f}
    Total tools:     {tools}
    Total tokens:    {tokens:,}
    Total time:      {time_s:.0f}s ({time_s/60:.1f}min)''')

print()
print('=' * 85)
"

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
log "Complete! Total wall time: $((ELAPSED / 60))m $((ELAPSED % 60))s"
echo "Results: $OUTPUT_BASE"
