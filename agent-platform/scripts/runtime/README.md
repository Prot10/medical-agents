# Runtime

`serve_model.sh` accepts only `qwen3.5-9b`, `granite-4.1-8b` or `gemma-4-e4b`. It launches the colocated `vllm_serve.py` wrapper from the isolated `.venv-vllm` environment.

Environment controls:

- `VLLM_VENV`: vLLM environment path.
- `HF_HOME`: Hugging Face cache. Stage the model in `/dev/shm/hf` for fast loads (Qwen3.5-9B loads in ~140 s from RAM).
- `GPU_MEMORY_UTILIZATION` (0.90) and `MAX_NUM_SEQS` (16).
- `LORA_ADAPTER`, `LORA_NAME` (default `sft`) and `MAX_LORA_RANK`: expose a PEFT adapter next to the base model. A profile evaluates it by setting `served_model: <LORA_NAME>` on its model plugin; the episode then records that alias as `model_id`.

The script rejects arbitrary model paths to keep the benchmark matrix reproducible. Thinking is disabled per request by the harness (`model_registry.request_defaults`), not by a server flag.
