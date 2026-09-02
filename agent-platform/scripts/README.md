# Maintained scripts

- `runtime/serve_model.sh`: serve one model from the fixed benchmark panel.
- `runtime/vllm_serve.py`: vLLM launcher with the site-specific CUDA detection workaround.
- `review/build_condition_tool_guidance.py`: build physician-review guidance.
- `validation/report_panel_case_tiers.py`: report drift between condition-level generation defaults and per-case policies.
- `validation/apply_diagnosis_synonyms.py`: expand `config/policies/diagnosis_synonyms.yaml` into every case's accepted diagnosis labels and ICD codes (idempotent; `--check` for CI).
- `diversify_cases.py`: dataset diversification utility.

Benchmark execution is `python -m neuroagent.evaluation.benchmark`; SFT is `python -m neuroagent.training.train_sft`; candidate episodes are exported with `python -m neuroagent.training.data.export_episodes`.
