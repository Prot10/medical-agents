# Maintained scripts

- `runtime/serve_model.sh`: serve one model from the fixed benchmark panel.
- `runtime/vllm_serve.py`: vLLM launcher with the site-specific CUDA detection workaround.
- `review/build_condition_tool_guidance.py`: build physician-review guidance.
- `validation/report_panel_case_tiers.py`: report drift between condition-level generation defaults and per-case policies.
- `diversify_cases.py`: dataset diversification utility.

Benchmark execution is a Python API in `neuroagent.evaluation.runner`; SFT and GRPO live in `neuroagent.training`. Removed experiment-specific shell pipelines are intentionally unsupported.
