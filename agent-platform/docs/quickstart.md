# Quickstart

## Prerequisites

- NVIDIA GPU with >= 20GB VRAM (A100 40GB recommended)
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

## 1. Install dependencies

```bash
# From the repo root
uv sync --all-packages
```

For the vLLM inference server (separate venv to avoid dependency conflicts):

```bash
uv venv .venv-vllm --python 3.11
.venv-vllm/bin/pip install vllm==0.17.1
```

## 2. Download a model

```bash
HF_HOME=~/.cache/huggingface .venv-vllm/bin/huggingface-cli download Qwen/Qwen3.5-9B
```

## 3. Start the inference server

```bash
cd agent-platform
./scripts/serve_model.sh              # default: qwen3.5-9b
./scripts/serve_model.sh qwen3.5-27b-awq  # larger model
```

Wait until you see `Uvicorn running on http://0.0.0.0:8000`.

## 4. Run a case

```bash
uv run python agent-platform/scripts/run_single_case.py \
    agent-platform/tests/fixtures/sample_case.json
```

## 5. Run tests

```bash
uv run pytest agent-platform/tests/ -v
```
