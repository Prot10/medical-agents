"""The fixed under-10B model panel used by benchmark and training profiles.

``request_defaults`` are sent with every chat request for that model: the sampling settings each
model card recommends, plus the thinking switch. Qwen3.5 and Gemma 4 think by default; with
thinking on, Qwen3.5-9B spent its whole 4096-token budget without emitting a tool call under
``tool_choice=required`` and emitted several calls at once under ``auto`` (measured 2026-09-02 on
vLLM 0.23), so both run with thinking disabled and the ReAct profile is the only rationale
condition. Granite 4.1 has no thinking switch and no recommended sampling; it runs greedy.
Runs are replicated over seeds (`benchmark --seed`).
"""

from __future__ import annotations

VLLM_BASE_URL = "http://localhost:8000/v1"

AVAILABLE_MODELS: list[dict] = [
    {
        "key": "qwen3.5-9b",
        "name": "Qwen3.5-9B",
        "hf_model_id": "Qwen/Qwen3.5-9B",
        "description": "General open model; native structured tool calling.",
        "size_gb": 19.0,
        "expected_load_seconds": 300,
        # Model card, instruct (non-thinking) mode for general tasks.
        "request_defaults": {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 20,
            "presence_penalty": 1.5,
            "chat_template_kwargs": {"enable_thinking": False},
        },
        # Lossless multi-token-prediction draft (model card); +33% decode measured on the A100.
        "engine_kwargs": {"speculative_config": {"method": "qwen3_next_mtp", "num_speculative_tokens": 2}},
    },
    {
        "key": "granite-4.1-8b",
        "name": "Granite 4.1 8B",
        "hf_model_id": "ibm-granite/granite-4.1-8b",
        "description": "IBM dense 8B instruct model; native tool calling, Apache-2.0.",
        "size_gb": 17.0,
        "expected_load_seconds": 300,
        "request_defaults": {"temperature": 0.0},
    },
    {
        "key": "gemma-4-e4b",
        "name": "Gemma 4 E4B",
        "hf_model_id": "google/gemma-4-E4B-it",
        "description": "General open model; native structured tool calling.",
        "size_gb": 15.0,
        "expected_load_seconds": 300,
        # Model card: standardized sampling for all use cases.
        "request_defaults": {
            "temperature": 1.0,
            "top_p": 0.95,
            "top_k": 64,
            "chat_template_kwargs": {"enable_thinking": False},
        },
    },
]

HF_TO_KEY = {model["hf_model_id"]: model["key"] for model in AVAILABLE_MODELS}
KEY_TO_MODEL = {model["key"]: model for model in AVAILABLE_MODELS}
KEY_TO_HF = {model["key"]: model["hf_model_id"] for model in AVAILABLE_MODELS}
