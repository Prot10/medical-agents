# Runtime Scripts

Manual agent execution and model serving utilities.

Keep:
- `run_single_case.py` — single-case CLI smoke/debug runner.
- `interactive_demo.py` — manual text-entry demo runner.
- `serve_model.sh`, `vllm_serve.py` — local/vLLM serving used by the API and benchmarks.
- `nano_v3_reasoning_parser.py`, `nemotron_toolcall_parser.py` — vLLM parser plugins used by `serve_model.sh`.

Note:
- The `v3` in `nano_v3_reasoning_parser.py` refers to the Nemotron-3 Nano model family, not dataset v3. It registers the `nano_v3` vLLM reasoning parser used by `serve_model.sh nemotron-3-nano-4b` (`--reasoning-parser nano_v3`).
