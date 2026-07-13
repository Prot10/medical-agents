#!/usr/bin/env bash
#
# generate_batch.sh — Generate NeuroBench cases using claude CLI
#
# Conditions are read from config/conditions.yaml (20 conditions), so the
# script stays in sync with the dataset automatically. For each selected
# condition it generates a batch of synthetic cases per difficulty
# (default 4 straightforward + 3 moderate + 3 puzzle), skipping case IDs
# that already exist in data/neurobench/cases/.
#
# IMPORTANT: This script must be run OUTSIDE of a Claude Code session.
# It calls `claude -p` which cannot be nested inside another claude session.
#
# Usage:
#   ./generate_batch.sh                          # all conditions from conditions.yaml
#   ./generate_batch.sh --dry-run                # show what would be generated
#   ./generate_batch.sh --condition ischemic_stroke        # one condition only
#   ./generate_batch.sh --counts 6,4,4           # S,M,P cases per condition
#   ./generate_batch.sh --start 11               # number cases from 11 (extend a batch)
#   ./generate_batch.sh --max-retries 3          # validation retries per case
#
# For a single case (same underlying pipeline), use:
#   ./generate_one.sh <condition_key> <difficulty> <case_id>
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
DATA_DIR="$REPO_ROOT/data/neurobench"
CASES_DIR="$DATA_DIR/cases"
FAILED_DIR="$DATA_DIR/failed"
CONDITIONS_YAML="$PROJECT_DIR/config/conditions.yaml"

mkdir -p "$CASES_DIR" "$FAILED_DIR"

# Parse arguments
DRY_RUN=false
FILTER_CONDITION=""
MAX_RETRIES=2
COUNTS="4,3,3"   # straightforward,moderate,diagnostic_puzzle per condition
START=1

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=true; shift ;;
        --condition) FILTER_CONDITION="$2"; shift 2 ;;
        --counts) COUNTS="$2"; shift 2 ;;
        --start) START="$2"; shift 2 ;;
        --max-retries) MAX_RETRIES="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

IFS=',' read -r COUNT_S COUNT_M COUNT_P <<< "$COUNTS"
if [[ -z "${COUNT_S:-}" || -z "${COUNT_M:-}" || -z "${COUNT_P:-}" ]]; then
    echo "ERROR: --counts must be S,M,P (e.g. 4,3,3)"; exit 1
fi

# Load condition_key<TAB>abbreviation pairs from conditions.yaml
mapfile -t CONDITION_ROWS < <(cd "$REPO_ROOT" && uv run --project dataset-generation python -c "
import yaml
with open('$CONDITIONS_YAML') as f:
    conditions = yaml.safe_load(f)
for key, spec in conditions.items():
    print(f\"{key}\t{spec['abbreviation']}\")
")

if [[ ${#CONDITION_ROWS[@]} -eq 0 ]]; then
    echo "ERROR: no conditions loaded from $CONDITIONS_YAML"; exit 1
fi

if [[ -n "$FILTER_CONDITION" ]]; then
    if ! printf '%s\n' "${CONDITION_ROWS[@]}" | cut -f1 | grep -qx "$FILTER_CONDITION"; then
        echo "ERROR: unknown condition '$FILTER_CONDITION'. Available:"
        printf '%s\n' "${CONDITION_ROWS[@]}" | cut -f1 | sed 's/^/  /'
        exit 1
    fi
fi

# Counters
total=0
generated=0
skipped=0
failed=0

for row in "${CONDITION_ROWS[@]}"; do
    condition="${row%%$'\t'*}"
    abbrev="${row##*$'\t'}"

    if [[ -n "$FILTER_CONDITION" && "$condition" != "$FILTER_CONDITION" ]]; then
        continue
    fi

    for difficulty in straightforward moderate diagnostic_puzzle; do
        case "$difficulty" in
            straightforward) dletter="S"; count="$COUNT_S" ;;
            moderate) dletter="M"; count="$COUNT_M" ;;
            diagnostic_puzzle) dletter="P"; count="$COUNT_P" ;;
        esac

        for ((n = START; n < START + count; n++)); do
            case_id="$(printf '%s-%s%02d' "$abbrev" "$dletter" "$n")"
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
