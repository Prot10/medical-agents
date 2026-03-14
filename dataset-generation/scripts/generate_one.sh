#!/usr/bin/env bash
#
# generate_one.sh — Generate and validate a single NeuroBench case
#
# Usage:
#   ./generate_one.sh focal_epilepsy_temporal straightforward FEPI-TEMP-S01
#   ./generate_one.sh ischemic_stroke moderate ISCH-STR-M01
#
set -euo pipefail

if [[ $# -ne 3 ]]; then
    echo "Usage: $0 <condition_key> <difficulty> <case_id>"
    echo ""
    echo "Conditions: focal_epilepsy_temporal, ischemic_stroke,"
    echo "            autoimmune_encephalitis_nmdar, alzheimers_early, syncope_cardiac"
    echo "Difficulties: straightforward, moderate, diagnostic_puzzle"
    echo ""
    echo "Example: $0 focal_epilepsy_temporal straightforward FEPI-TEMP-S01"
    exit 1
fi

CONDITION="$1"
DIFFICULTY="$2"
CASE_ID="$3"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$PROJECT_DIR/.." && pwd)"
DATA_DIR="$REPO_ROOT/data/neurobench_v1"

mkdir -p "$DATA_DIR/cases" "$DATA_DIR/failed"

echo "Building prompt for: $CASE_ID ($CONDITION / $DIFFICULTY)"

# Build the prompt
prompt=$(cd "$REPO_ROOT" && uv run --project dataset-generation \
    python -m neurobench_gen.build_prompt "$CONDITION" "$DIFFICULTY" "$CASE_ID")

echo "Prompt built ($(echo "$prompt" | wc -c) bytes). Calling claude..."
echo ""

# Call claude
raw_output=$(claude -p "$prompt" --output-format json)

# Save raw output
tmp_file="/tmp/neurobench_raw_${CASE_ID}.json"
echo "$raw_output" > "$tmp_file"
echo "Raw output saved to $tmp_file ($(echo "$raw_output" | wc -c) bytes)"

# Validate
echo ""
echo "Validating..."
if cd "$REPO_ROOT" && uv run --project dataset-generation \
    python -m neurobench_gen.validate_case "$tmp_file"; then
    cp "$tmp_file" "$DATA_DIR/cases/${CASE_ID}.json"
    echo ""
    echo "✓ Case saved to $DATA_DIR/cases/${CASE_ID}.json"
else
    cp "$tmp_file" "$DATA_DIR/failed/${CASE_ID}.json"
    echo ""
    echo "✗ Validation failed — saved to $DATA_DIR/failed/${CASE_ID}.json"
fi

# Pretty-print summary
echo ""
echo "━━━ Case Summary ━━━"
cd "$REPO_ROOT" && uv run --project dataset-generation python -c "
import json, sys
with open('$tmp_file') as f:
    data = json.load(f)
print(f'Case ID:    {data.get(\"case_id\", \"N/A\")}')
print(f'Condition:  {data.get(\"condition\", \"N/A\")}')
print(f'Difficulty: {data.get(\"difficulty\", \"N/A\")}')
p = data.get('patient', {})
d = p.get('demographics', {})
print(f'Patient:    {d.get(\"age\", \"?\")}yo {d.get(\"sex\", \"?\")}')
print(f'Complaint:  {p.get(\"chief_complaint\", \"N/A\")}')
gt = data.get('ground_truth', {})
print(f'Diagnosis:  {gt.get(\"primary_diagnosis\", \"N/A\")}')
print(f'ICD Code:   {gt.get(\"icd_code\", \"N/A\")}')
to = data.get('initial_tool_outputs', {})
tools = [k for k, v in to.items() if v is not None]
print(f'Tools:      {', '.join(tools) if tools else \"none\"}')
fu = data.get('followup_outputs', [])
print(f'Follow-ups: {len(fu)}')
" 2>/dev/null || echo "(could not parse summary)"
