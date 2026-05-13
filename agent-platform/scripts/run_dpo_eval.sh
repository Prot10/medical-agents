#!/bin/bash
# Evaluate DPO model on fold0 val set and compare all 4 models
# Run: bash agent-platform/scripts/run_dpo_eval.sh
set -euo pipefail
cd /home/aprotani/projects/medical-agents

export CUDA_MODULE_LOADING=LAZY
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DPO_MODEL="/home/aprotani/projects/medical-agents/models/qwen3.5-9b-dpo"
RESULTS_DIR="results/sft_eval"
PORT=8000

echo "========================================="
echo " DPO Evaluation — fold0 val (60 cases)"
echo " Model: $DPO_MODEL"
echo " Start: $(date)"
echo "========================================="

pkill -f "vllm_serve.py" || true
pkill -f "VLLM::EngineCore" || true
sleep 5

echo "Starting vLLM..."
bash "$SCRIPT_DIR/serve_model.sh" "$DPO_MODEL" "$PORT" &
VLLM_PID=$!

echo "Waiting for vLLM..."
for i in $(seq 1 120); do
    if curl -s "http://localhost:$PORT/v1/models" 2>/dev/null | grep -q "model"; then
        echo "vLLM ready after $((i*5))s"
        break
    fi
    sleep 5
done

uv run python agent-platform/scripts/run_sft_eval_cases.py evaluate \
    --model-id "$DPO_MODEL" \
    --run-name "dpo-qwen3.5-9b" \
    --hospital "de_charite" \
    --repeats 3 \
    --output "$RESULTS_DIR/dpo_results.json" \
    --port "$PORT"

kill "$VLLM_PID" 2>/dev/null || true
pkill -f "vllm_serve.py" || true
pkill -f "VLLM::EngineCore" || true
sleep 3

echo ""
echo "========================================="
echo " Comparing Base vs SFT vs GRPO vs DPO"
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
for name, path in [('Base', '$RESULTS_DIR/base_results.json'), ('SFT', '$RESULTS_DIR/sft_results.json'), ('GRPO', '$RESULTS_DIR/grpo_results.json'), ('DPO', '$RESULTS_DIR/dpo_results.json')]:
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

print()
for diff in ['straightforward', 'moderate', 'diagnostic_puzzle']:
    row = f'{diff[:16]:16s}'
    for name, path in [('Base', '$RESULTS_DIR/base_results.json'), ('SFT', '$RESULTS_DIR/sft_results.json'), ('GRPO', '$RESULTS_DIR/grpo_results.json'), ('DPO', '$RESULTS_DIR/dpo_results.json')]:
        try:
            r = json.loads(open(path).read())['results']
            rs = [x for x in r if x['difficulty'] == diff]
            a = sum(1 for x in rs if x['diagnostic_accuracy_top1'])/len(rs) if rs else 0
            row += f'{a:>7.0%}'
        except: row += f'{\"\":>7s}'
    print(row)
"

echo ""
echo "========================================="
echo " Done! $(date)"
echo "========================================="
