# Runtime

`serve_model.sh` accepts only `qwen3.5-9b`, `gemma-4-e4b` or `medgemma-1.5-4b`. It launches the colocated `vllm_serve.py` wrapper.

Environment controls:

- `VLLM_VENV`: vLLM environment path.
- `HF_HOME`: Hugging Face cache.
- `GPU_MEMORY_UTILIZATION` and `MAX_NUM_SEQS`.
- `NO_PREFIX_CACHING=1`.
- `LORA_ADAPTER` and optional `MAX_LORA_RANK`.

The script rejects arbitrary model paths to keep the benchmark matrix reproducible.
