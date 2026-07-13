# Quickstart

## Prerequisites

- NVIDIA GPU with >= 20GB VRAM (A100 40GB recommended)
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

## 1. Install dependencies

```bash
# From the repo root — app + eval
uv sync --all-packages

# For SFT / RFT fine-tuning, also install the optional training extra
# (torch, transformers, trl, peft, bitsandbytes, flash-linear-attention, liger-kernel):
uv sync --all-packages --extra training
```

`flash-linear-attention` (in the training extra) is required for Qwen3.5 — without it the
gated-delta-net layers run a ~2.2×-slower torch fallback. It is pure Triton, no `nvcc` needed.

For the vLLM inference server (separate venv to avoid dependency conflicts):

```bash
uv venv .venv-vllm --python 3.11
.venv-vllm/bin/pip install vllm==0.23.0
```

## 2. Download a model

```bash
HF_HOME=~/.cache/huggingface .venv-vllm/bin/huggingface-cli download Qwen/Qwen3.5-9B
```

## 3. Start the inference server

```bash
cd agent-platform
./scripts/runtime/serve_model.sh              # default: qwen3.5-9b
./scripts/runtime/serve_model.sh qwen3.5-27b-awq  # larger model
```

Wait until you see `Uvicorn running on http://0.0.0.0:8000`.

## 4. Run a case

```bash
uv run python agent-platform/scripts/runtime/run_single_case.py \
    agent-platform/tests/fixtures/sample_case.json
```

## 5. Run the web dashboard

```bash
# Start the API server (loads all 600 cases on startup)
uv run uvicorn neuroagent.api.app:app --host 0.0.0.0 --port 8888
```

Open `http://localhost:8888` in your browser. Select a case, choose a hospital, and click **Run Agent** to watch the reasoning in real time.

> The dashboard works without a GPU for browsing cases and replaying saved traces. A running vLLM server is only needed for live agent execution.

See [web-api.md](web-api.md) for the full API reference.

## 6. Run tests

```bash
uv run pytest agent-platform/tests/ -v
```
