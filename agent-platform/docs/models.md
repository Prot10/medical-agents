# Models

NeuroAgent uses [vLLM](https://docs.vllm.ai/) to serve LLMs locally via an OpenAI-compatible API.

## Supported models

| Shortname | HuggingFace ID | Size | VRAM | Notes |
|---|---|---|---|---|
| `qwen3.5-9b` | `Qwen/Qwen3.5-9B` | ~18 GB | ~20 GB | **Default.** Fast (~70 tok/s on A100), good tool calling. Best for development. |
| `qwen3.5-27b-awq` | `QuantTrio/Qwen3.5-27B-AWQ` | ~15 GB | ~22 GB | AWQ 4-bit via Marlin kernels (~55 tok/s). Best quality. |
| `medgemma-27b` | `ig1/medgemma-27b-text-it-FP8-Dynamic` | ~31 GB | ~33 GB | Medical specialist, FP8 quantized. Tight on A100-40GB (8K context limit). |
| `medgemma-4b` | `google/medgemma-1.5-4b-it` | ~8 GB | ~10 GB | Small medical model. Fast iteration. Gated access. |
| `openbio-8b` | `aaditya/Llama3-OpenBioLLM-8B` | ~16 GB | ~18 GB | Biomedical baseline. |

## Qwen3.5 architecture

Qwen3.5 is a **hybrid architecture** — not a standard transformer. It uses Gated DeltaNet (linear attention) + Gated Attention + FFN in a repeating pattern. 75% of layers use linear attention (fast, constant-memory), 25% use full attention (precise retrieval). All models are natively multimodal but we use `--language-model-only` to save VRAM.

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

### Key vLLM flags used

| Flag | Value | Why |
|---|---|---|
| `--reasoning-parser qwen3` | Separates `<think>` blocks into `reasoning_content` field | Required for Qwen3.5 thinking mode |
| `--tool-call-parser qwen3_coder` | Parses Qwen3.5 tool call format | Required for tool calling |
| `--language-model-only` | Disables vision encoder | Saves VRAM for text-only workloads |
| `--quantization awq_marlin` | Uses Marlin mixed-precision CUDA kernels | **10x faster** than plain `awq` GEMM |
| `--enable-prefix-caching` | Caches KV for repeated system prompts | Free speedup for agent loop |
| `--gpu-memory-utilization 0.95` | Uses 95% of VRAM | More KV cache capacity |

### Performance: awq vs awq_marlin

The `--quantization` flag matters enormously for AWQ models:

| Backend | Tok/s (A100-40GB, 27B) | Notes |
|---|---|---|
| `awq` | ~5 tok/s | Slow GEMM kernels. **Do not use.** |
| `awq_marlin` | ~55 tok/s | Fast Marlin kernels. **Always use this.** |

### Qwen3.5-27B-AWQ

The 27B dense model quantized to AWQ 4-bit (~15GB). With `awq_marlin` kernels it achieves ~55 tok/s on A100-40GB, leaving ~16GB for KV cache.

If you omit `--quantization` entirely, vLLM auto-detects and uses Marlin when compatible.

## Sampling parameters

Qwen3.5 with thinking mode has specific recommended sampling parameters:

| Parameter | Value | Rationale |
|---|---|---|
| `temperature` | 1.0 | Qwen3.5 docs recommend this for reasoning tasks with thinking |
| `top_p` | 0.95 | Nucleus sampling for diverse reasoning |
| `presence_penalty` | 1.5 | Reduces repetition in long outputs |
| `max_tokens` | 8192 | Sufficient for medical reasoning + structured assessment |

These are configured in `config/agent_config.yaml` and `AgentConfig` defaults.

## Using a different model in scripts

All CLI scripts accept `--model` and `--base-url` flags:

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

## Think tag handling

Qwen3.5 models generate internal chain-of-thought in `<think>...</think>` tags (thinking mode). This is handled at two levels:

1. **Server-side**: `--reasoning-parser qwen3` separates thinking content into the `reasoning_content` field of the API response
2. **Client-side**: `strip_think_tags()` in `LLMClient._parse_response()` strips any residual tags from the content field

Important: Qwen3.5 does **NOT** support `/think` or `/nothink` commands in messages (that was Qwen3 only). To disable thinking mode, use the per-request API parameter:

```python
extra_body={"chat_template_kwargs": {"enable_thinking": False}}
```

For multi-turn conversations, the chat template automatically strips thinking blocks from history. If building messages manually, strip `<think>...</think>` from assistant messages before passing them back.

## Downloading models

```bash
export HF_HOME=~/.cache/huggingface

.venv-vllm/bin/huggingface-cli download Qwen/Qwen3.5-9B
.venv-vllm/bin/huggingface-cli download QuantTrio/Qwen3.5-27B-AWQ

# For gated models (MedGemma), login first:
.venv-vllm/bin/huggingface-cli login
.venv-vllm/bin/huggingface-cli download google/medgemma-1.5-4b-it
```
