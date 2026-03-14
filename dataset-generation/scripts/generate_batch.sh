#!/usr/bin/env bash
#
# generate_batch.sh — Generate NeuroBench cases using claude CLI
#
# IMPORTANT: This script must be run OUTSIDE of a Claude Code session.
# It calls `claude -p` which cannot be nested inside another claude session.
#
# Usage:
#   ./generate_batch.sh                    # Generate all 50 pilot cases
#   ./generate_batch.sh --dry-run          # Show what would be generated
#   ./generate_batch.sh --condition focal_epilepsy_temporal  # Only one condition
#
# Alternative: Cases can also be generated directly within a Claude Code
# conversation using subagents (see the implementation plan doc).
#
set -euo pipefail

# Check we're not inside a Claude Code session
if [[ -n "${CLAUDECODE:-}" ]]; then
    echo "ERROR: Cannot run inside a Claude Code session."
    echo "Run this script from a regular terminal, or use the"
    echo "in-conversation generation approach instead."
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$PROJECT_DIR/.." && pwd)"
DATA_DIR="$REPO_ROOT/data/neurobench_v1"
CASES_DIR="$DATA_DIR/cases"
FAILED_DIR="$DATA_DIR/failed"

mkdir -p "$CASES_DIR" "$FAILED_DIR"

# Parse arguments
DRY_RUN=false
FILTER_CONDITION=""
MAX_RETRIES=2

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=true; shift ;;
        --condition) FILTER_CONDITION="$2"; shift 2 ;;
        --max-retries) MAX_RETRIES="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Distribution: 5 conditions × (4 straightforward + 3 moderate + 3 puzzle) = 50
declare -A CONDITIONS=(
    ["focal_epilepsy_temporal"]="FEPI-TEMP"
    ["ischemic_stroke"]="ISCH-STR"
    ["autoimmune_encephalitis_nmdar"]="NMDAR-ENC"
    ["alzheimers_early"]="ALZ-EARLY"
    ["syncope_cardiac"]="SYNC-CARD"
)

declare -A DIFFICULTY_COUNTS=(
    ["straightforward"]=4
    ["moderate"]=3
    ["diagnostic_puzzle"]=3
)

# Counters
total=0
generated=0
skipped=0
failed=0

for condition in "${!CONDITIONS[@]}"; do
    if [[ -n "$FILTER_CONDITION" && "$condition" != "$FILTER_CONDITION" ]]; then
        continue
    fi

    abbrev="${CONDITIONS[$condition]}"

    for difficulty in straightforward moderate diagnostic_puzzle; do
        count="${DIFFICULTY_COUNTS[$difficulty]}"

        case "$difficulty" in
            straightforward) dletter="S" ;;
            moderate) dletter="M" ;;
            diagnostic_puzzle) dletter="P" ;;
        esac

        for i in $(seq -w 1 "$count"); do
            case_id="${abbrev}-${dletter}${i}"
            total=$((total + 1))

            if [[ -f "$CASES_DIR/${case_id}.json" ]]; then
                echo "[SKIP] $case_id already exists"
                skipped=$((skipped + 1))
                continue
            fi

            if $DRY_RUN; then
                echo "[DRY-RUN] Would generate: $case_id ($condition / $difficulty)"
                continue
            fi

            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "[GEN] $case_id — $condition / $difficulty"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

            # Build the prompt
            prompt=$(cd "$REPO_ROOT" && uv run --project dataset-generation \
                python -m neurobench_gen.build_prompt "$condition" "$difficulty" "$case_id")

            success=false
            for attempt in $(seq 1 $((MAX_RETRIES + 1))); do
                echo "  Attempt $attempt/$((MAX_RETRIES + 1))..."

                raw_output=$(claude -p "$prompt" --output-format json 2>/dev/null) || true

                if [[ -z "$raw_output" ]]; then
                    echo "  Empty response, retrying..."
                    continue
                fi

                tmp_file="/tmp/neurobench_raw_${case_id}.json"
                echo "$raw_output" > "$tmp_file"

                if cd "$REPO_ROOT" && uv run --project dataset-generation \
                    python -m neurobench_gen.validate_case "$tmp_file" 2>/tmp/validate_errors_${case_id}.txt; then
                    mv "$tmp_file" "$CASES_DIR/${case_id}.json"
                    echo "  ✓ Valid"
                    success=true
                    break
                else
                    echo "  ✗ Validation failed:"
                    cat /tmp/validate_errors_${case_id}.txt | head -5
                    if [[ $attempt -lt $((MAX_RETRIES + 1)) ]]; then
                        errors=$(cat /tmp/validate_errors_${case_id}.txt)
                        prompt="$prompt

## PREVIOUS ATTEMPT FAILED VALIDATION
Fix ALL errors:
$errors
Output ONLY valid JSON."
                    fi
                fi
            done

            if $success; then
                generated=$((generated + 1))
            else
                [[ -f "/tmp/neurobench_raw_${case_id}.json" ]] && \
                    mv "/tmp/neurobench_raw_${case_id}.json" "$FAILED_DIR/${case_id}.json"
                echo "  ✗ FAILED — saved to $FAILED_DIR/"
                failed=$((failed + 1))
            fi
            echo ""
        done
    done
done

echo ""
echo "━━━ SUMMARY ━━━"
echo "  Total: $total | Generated: $generated | Skipped: $skipped | Failed: $failed"
