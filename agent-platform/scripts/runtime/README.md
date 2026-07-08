# Runtime Scripts

Manual agent execution and model serving utilities.

Keep:
- `run_single_case.py` — single-case CLI smoke/debug runner.
- `interactive_demo.py` — manual text-entry demo runner.
- `serve_model.sh`, `vllm_serve.py` — local/vLLM serving used by the API and benchmarks.
- `nano_v3_reasoning_parser.py`, `nemotron_toolcall_parser.py` — vLLM parser plugins used by `serve_model.sh`.

Needs update:
- `nano_v3_reasoning_parser.py` works as a parser plugin, but the filename is misleading now that dataset v3 cleanup is gone.
