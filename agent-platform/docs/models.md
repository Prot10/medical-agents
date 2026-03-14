# Models

NeuroAgent uses [vLLM](https://docs.vllm.ai/) to serve LLMs locally via an OpenAI-compatible API.

## Supported models

| Shortname | HuggingFace ID | Size | VRAM | Notes |
|---|---|---|---|---|
| `qwen3.5-9b` | `Qwen/Qwen3.5-9B` | ~18 GB | ~20 GB | **Default.** Fast, good tool calling. Best for development and iteration. |
| `qwen3.5-27b-awq` | `QuantTrio/Qwen3.5-27B-AWQ` | ~15 GB | ~22 GB | AWQ 4-bit quantized. Better reasoning, slower (~5 tok/s on A100). |
| `qwen3.5-27b-fp8` | `Qwen/Qwen3.5-27B-FP8` | ~28 GB | ~32 GB | FP8 quantized. Highest quality 27B option. Needs large GPU. |
| `medgemma-27b` | `unsloth/medgemma-27b-text-it-GGUF:Q4_K_M` | ~15 GB | ~20 GB | Medical-domain specialist. Requires `huggingface-cli login` (gated). |
| `medgemma-4b` | `google/medgemma-1.5-4b-it` | ~8 GB | ~10 GB | Small medical model. Fast iteration. Gated access. |
| `openbio-8b` | `aaditya/Llama3-OpenBioLLM-8B` | ~16 GB | ~18 GB | Biomedical baseline. |

## Serving a model

```bash
# Default (Qwen3.5-9B)
./scripts/serve_model.sh

# Specific model
./scripts/serve_model.sh qwen3.5-27b-awq

# Custom port
./scripts/serve_model.sh qwen3.5-9b 8001
```

The server exposes an OpenAI-compatible API at `http://localhost:{port}/v1`.

## Using a different model in scripts

All CLI scripts accept `--model` and `--base-url` flags. The `--model` value must exactly match the HuggingFace ID used when serving:

```bash
# Run with the default 9B model
uv run python scripts/run_single_case.py tests/fixtures/sample_case.json

# Run with the 27B AWQ model
uv run python scripts/run_single_case.py tests/fixtures/sample_case.json \
    --model QuantTrio/Qwen3.5-27B-AWQ

# Run against a remote endpoint
uv run python scripts/run_single_case.py tests/fixtures/sample_case.json \
    --model gpt-4o \
    --base-url https://api.openai.com/v1 \
    --api-key sk-...
```

## Downloading models

```bash
# Set cache location (default: ~/.cache/huggingface)
export HF_HOME=~/.cache/huggingface

# Download via the vLLM venv (has huggingface-hub installed)
.venv-vllm/bin/huggingface-cli download Qwen/Qwen3.5-9B
.venv-vllm/bin/huggingface-cli download QuantTrio/Qwen3.5-27B-AWQ

# For gated models (MedGemma), login first:
.venv-vllm/bin/huggingface-cli login
.venv-vllm/bin/huggingface-cli download google/medgemma-1.5-4b-it
```

## Think tag handling

Qwen3.x models use a "thinking mode" that wraps internal chain-of-thought in `<think>...</think>` tags. NeuroAgent automatically strips these in `LLMClient._parse_response()` so they never appear in traces, reports, or the final assessment.

If you switch to a non-Qwen model that doesn't use think tags, the stripping is a no-op — no configuration needed.
