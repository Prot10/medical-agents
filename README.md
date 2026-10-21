# NeuroAgent / NeuroBench

NeuroBench is a physician-validated, 360-degree simulated-patient dataset and an executable benchmark for small open medical agents. The v2 implementation evaluates typed clinical actions, evidence discovery, safe test selection, stopping, cost and final assessment without requiring one golden trajectory or chain-of-thought.

## What is implemented

- 600 schema-v2 neurology cases across 20 conditions.
- A typed policy harness with standard, direct and ReAct-prompt conditions, and one transcript codec shared by inference and SFT.
- A fixed under-10B panel: Qwen3.5-9B, IBM Granite 4.1 8B and Gemma 4 E4B.
- Nine checked experiment profiles and a batch runner that persists every episode.
- A clinical-policy reward with safety caps and adequacy-gated efficiency.
- Structured independent physician review and adjudication.
- LoRA SFT over typed episodes and a backend-neutral GRPO coordinator.
- A JSON API for profiles, runs, models, cases, hospitals and persisted episodes.
- A dashboard in `web` for cases, policies, live and replayed episodes and the engineering reward.
- A dedicated physician-review application in `web-review`.

The architecture and experimental boundaries are documented in [agent-platform/docs/clinical-policy-harness.md](agent-platform/docs/clinical-policy-harness.md).

## Setup

```bash
uv sync --all-packages --extra dev --extra training
uv run pytest agent-platform/tests packages/neuroagent-schemas/tests
```

## Serve a model and run the benchmark

```bash
uv venv .venv-vllm --python 3.12 && uv pip install --python .venv-vllm/bin/python vllm
HF_HOME=/dev/shm/hf agent-platform/scripts/runtime/serve_model.sh qwen3.5-9b
uv run python -m neuroagent.evaluation.benchmark --profile policy-qwen3.5-9b \
  --cases FEPI-TEMP-M01 SAH-M01 --output outputs/smoke/policy-qwen --allow-draft-policies
```

The run API exposes the same path over HTTP:

```bash
uv run uvicorn neuroagent.api.app:app --host 127.0.0.1 --port 8888
```

List `GET /api/v1/profiles`, then submit a case to `POST /api/v1/runs` (or `POST /api/v1/runs/stream` for the episode events as Server-Sent Events).

## Dashboard

```bash
cd web
npm ci
npm run dev        # http://localhost:5173, proxies /api to port 8888
```

`npm run build` writes `web/dist`, which the run API then serves at `/`. The dashboard picks a checked profile, streams a run live, replays saved episodes and shows the policy reward; on draft policies that reward is an engineering check, never a reportable number.

## Physician review

```bash
uv run uvicorn neuroagent.review_api.app:app --host 127.0.0.1 --port 8889
cd web-review
npm ci
npm run dev
```

Synthetic cases begin as `draft`. A reportable policy requires two independent all-dimension approvals; disagreement is adjudicated by a third physician. Draft policies are scoreable only with `--allow-draft-policies`, and those numbers are not reportable.

## GPU validation and training

Follow the [A100 validation handoff](docs/A100_VALIDATION_HANDOFF.md) before running model or training experiments. It defines the environment capture, contract tests, the smoke matrix, reward checks, serving throughput measurements and required artifacts.

No physician-approved episode file is committed. Candidate episodes are exported from benchmark runs and are training-eligible only with an explicit flag:

```bash
uv run python -m neuroagent.training.data.export_episodes --runs outputs/smoke/policy-qwen --output training_data/candidate_episodes.jsonl
uv run python -m neuroagent.training.train_sft --model qwen3.5-9b \
  --episodes training_data/candidate_episodes.jsonl --output /eos/project-d/diagbox/dvc/NeuroAgent/checkpoints/sft-qwen/qwen3.5-9b --allow-candidates
```

Weights are written to EOS only (the trainers refuse a local path). Serve the adapter from a RAM copy, `cp -r <eos adapter dir> /dev/shm/sft-qwen && LORA_ADAPTER=/dev/shm/sft-qwen LORA_NAME=sft-qwen3.5-9b serve_model.sh qwen3.5-9b`, and evaluate it with `--served-model sft-qwen3.5-9b`. The current GRPO surface is a backend contract, not a completed distributed trainer.
