# Fixed model panel

The benchmark compares exactly three open models below 10B parameters, all with native tool calling:

| Key | Hugging Face id | Notes |
|---|---|---|
| `qwen3.5-9b` | `Qwen/Qwen3.5-9B` | hybrid gated-delta-net/attention; thinking disabled per request; vLLM `qwen3_coder` parser |
| `granite-4.1-8b` | `ibm-granite/granite-4.1-8b` | dense; Apache-2.0; no thinking switch; vLLM `granite4` parser |
| `gemma-4-e4b` | `google/gemma-4-E4B-it` | gated on Hugging Face; thinking disabled per request; vLLM `gemma4` parser |

Every model runs the policy, direct and ReAct-prompt conditions (nine profiles). The registry in
`model_registry.py` is the single source for ids, adapters aliases and per-request defaults;
`serve_model.sh` and the API load only these keys.

Serving on one A100-40GB (vLLM 0.23, bf16, 32k context, prefix caching; measured 2026-09-02 on the
real prompt shape of ~8k input tokens, 128 output tokens):

| Model | load (RAM-staged) | weights | KV cache | 1 stream | 8 concurrent | 16 concurrent |
|---|---:|---:|---:|---:|---:|---:|
| Qwen3.5-9B | 137 s | 16.8 GiB | 489k tokens | 60 tok/s, TPOT 14 ms | 365 tok/s | 448 tok/s |
| Qwen3.5-9B + MTP spec. decoding (default) | 137 s | 17.3 GiB | 425k tokens | 80 tok/s, TPOT 8.5 ms | 417 tok/s | 502 tok/s |
| Gemma 4 E4B | 3 s | 14.3 GiB | 854k tokens | 73 tok/s, TPOT 12 ms | 427 tok/s | 786 tok/s |
| Granite 4.1 8B | 3 s | 15.7 GiB | 124k tokens | 56 tok/s, TPOT 16 ms | 317 tok/s | 574 tok/s |

SGLang 0.5.9 was measured on the same Qwen3.5-9B workload and was slower at every concurrency
(44 vs 60 tok/s single-stream, 277 vs 448 tok/s at 16), so vLLM is the engine.

```bash
HF_HOME=/dev/shm/hf agent-platform/scripts/runtime/serve_model.sh qwen3.5-9b
```

Model weights live on EOS (`/eos/project-d/diagbox/dvc/NeuroAgent/models/base/huggingface`); stage a
copy in `/dev/shm/hf` before serving or training.
