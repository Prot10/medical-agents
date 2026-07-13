#!/bin/bash
# Evaluate GRPO model on fold0 val set (60 cases × 3 repeats)
# Run: bash agent-platform/scripts/training/run_grpo_eval.sh
set -euo pipefail
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"  # repo root

export CUDA_MODULE_LOADING=LAZY
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MERGED_MODEL="${MERGED_MODEL:-${MODELS_ROOT:-models}/qwen3.5-9b-grpo}"
RESULTS_DIR="results/sft_eval"
PORT=8000

echo "========================================="
echo " GRPO Evaluation — fold0 val (60 cases)"
echo " Model: $MERGED_MODEL"
echo " Start: $(date)"
echo "========================================="

# Kill any existing vLLM
pkill -f "vllm_serve.py" || true
pkill -f "VLLM::EngineCore" || true
sleep 5

# Start vLLM
echo "Starting vLLM..."
bash "$SCRIPT_DIR/../runtime/serve_model.sh" "$MERGED_MODEL" "$PORT" &
VLLM_PID=$!

echo "Waiting for vLLM..."
for i in $(seq 1 120); do
    if curl -s "http://localhost:$PORT/v1/models" 2>/dev/null | grep -q "model"; then
        echo "vLLM ready after $((i*5))s"
        break
    fi
    sleep 5
done

# Run evaluation
uv run python agent-platform/scripts/training/run_sft_eval_cases.py evaluate \
    --model-id "$MERGED_MODEL" \
    --run-name "grpo-qwen3.5-9b" \
    --hospital "de_charite" \
    --repeats 3 \
    --output "$RESULTS_DIR/grpo_results.json" \
    --port "$PORT"

# Stop server
kill "$VLLM_PID" 2>/dev/null || true
pkill -f "vllm_serve.py" || true
pkill -f "VLLM::EngineCore" || true
sleep 3

# Compare all three models
echo ""
echo "========================================="
echo " Comparing Base vs SFT vs GRPO"
echo "========================================="
python3 -c "
import json
from collections import defaultdict

def load(path):
    data = json.loads(open(path).read())
    r = data['results']
    n = len(r)
    if n == 0: return None
    return {
        'n': n,
        'top1': sum(1 for x in r if x['diagnostic_accuracy_top1']) / n,
        'top3': sum(1 for x in r if x['diagnostic_accuracy_top3']) / n,
        'critical': sum(x['critical_actions_hit'] for x in r) / n,
        'safety': sum(x['safety_score'] for x in r) / n,
        'tools': sum(x['tool_call_count'] for x in r) / n,
        'cost': sum(x['total_cost_usd'] for x in r) / n,
    }

models = {}
for name, path in [('Base', '$RESULTS_DIR/base_results.json'), ('SFT', '$RESULTS_DIR/sft_results.json'), ('GRPO', '$RESULTS_DIR/grpo_results.json')]:
    try:
        models[name] = load(path)
    except: pass

header = f'{\"\":20s}'
for name in models: header += f'{name:>8s}'
print(header)
print('-' * len(header))
for key in ['top1', 'top3', 'critical', 'safety', 'tools', 'cost']:
    row = f'{key:20s}'
    for name, m in models.items():
        v = m[key]
        if key == 'cost': row += f'\${v:>7,.0f}'
        elif key == 'tools': row += f'{v:>8.1f}'
        else: row += f'{v:>7.1%}'
    print(row)
row = f'{\"runs\":20s}'
for name, m in models.items(): row += f'{m[\"n\"]:>8d}'
print(row)

# Per-difficulty breakdown
print()
for name, path in [('Base', '$RESULTS_DIR/base_results.json'), ('SFT', '$RESULTS_DIR/sft_results.json'), ('GRPO', '$RESULTS_DIR/grpo_results.json')]:
    try:
        r = json.loads(open(path).read())['results']
        by_diff = defaultdict(list)
        for x in r: by_diff[x['difficulty']].append(x)
        accs = []
        for d in ['straightforward', 'moderate', 'diagnostic_puzzle']:
            if d in by_diff:
                rs = by_diff[d]
                accs.append(f'{d[:6]}={sum(1 for x in rs if x[\"diagnostic_accuracy_top1\"])/len(rs):.0%}')
        print(f'  {name:6s}: {\"  \".join(accs)}')
    except: pass
"

echo ""
echo "========================================="
echo " Done! $(date)"
echo " Results: $RESULTS_DIR/"
echo "========================================="
