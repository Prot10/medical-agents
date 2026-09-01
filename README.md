# NeuroAgent / NeuroBench

NeuroBench is a physician-validated, 360-degree simulated-patient dataset and an executable benchmark for small open medical agents. The v2 implementation evaluates typed clinical actions, evidence discovery, safe test selection, stopping, cost and final assessment without requiring one golden trajectory or chain-of-thought.

## What is implemented

- 600 schema-v2 neurology cases across 20 conditions.
- A typed policy harness with standard, direct and ReAct-prompt conditions.
- A fixed under-10B panel: Qwen3.5-9B, Gemma 4 E4B and MedGemma 1.5 4B.
- Eight checked experiment profiles.
- A clinical-policy reward with safety caps and adequacy-gated efficiency.
- Structured independent physician review and adjudication.
- LoRA SFT over typed episodes and a backend-neutral GRPO coordinator.
- A JSON API for profiles, runs, models, cases, hospitals and persisted episodes.
- A dedicated physician-review application in `web-review`.

The architecture and experimental boundaries are documented in [agent-platform/docs/clinical-policy-harness.md](agent-platform/docs/clinical-policy-harness.md).

## Setup

```bash
uv sync --all-packages
uv run pytest agent-platform/tests
```

Training dependencies are optional:

```bash
uv sync --all-packages --extra training
```

## Run the API

```bash
agent-platform/scripts/runtime/serve_model.sh qwen3.5-9b
uv run uvicorn neuroagent.api.app:app --host 127.0.0.1 --port 8888
```

List `GET /api/v1/profiles`, then submit a case to `POST /api/v1/runs`.

## Physician review

```bash
uv run uvicorn neuroagent.review_api.app:app --host 127.0.0.1 --port 8889
cd web-review
npm install
npm run dev
```

Synthetic cases begin as `draft`. A reportable policy requires two independent all-dimension approvals; disagreement is adjudicated by a third physician.

## Training

Typed bootstrap episodes live in `training_data/bootstrap/candidate_episodes.jsonl` and are explicitly labeled `candidate_not_gold`.

```bash
uv run python -m neuroagent.training.train_sft \
  --model qwen3.5-9b \
  --episodes training_data/bootstrap/candidate_episodes.jsonl \
  --cases data/neurobench/cases \
  --output outputs/qwen-sft \
  --allow-candidates
```

Candidate opt-in is intended for bootstrap experiments. Final reportable SFT should use replay-valid, quality-gated episodes under the preregistered data policy.
