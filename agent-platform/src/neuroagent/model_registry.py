"""The fixed model panel used by benchmark and training profiles.

The three under-10B models are the panel the paper trains and compares; Qwen3.8-27B is the larger
untrained reference of Fig. 6 (25 Nov 2026), evaluated only, never trained. Gemma 4 31B, Granite 4.1
30B and Llama 3.3 70B (FP8) are larger untrained references from other families (Andrea, 26 Nov
2026): the two larger siblings of the panel models, and an older, much larger model.

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
        # Model card, thinking mode for general tasks. Used only by `benchmark --thinking-tokens`
        # (17 Nov 2026: re-testing thinking now that longer traces are affordable); the server
        # then needs REASONING_PARSER=qwen3 so the trace stays out of the parsed tool call.
        "thinking_request_defaults": {
            "temperature": 1.0,
            "top_p": 0.95,
            "top_k": 20,
            "presence_penalty": 1.5,
            "chat_template_kwargs": {"enable_thinking": True},
        },
        # Prefix cache on, MTP off: re-prefilling the transcript every turn is what costs, and MTP
        # adds no throughput with the cache on. On vLLM 0.23 the two together moved logprobs well
        # past the batching noise floor (2 Nov 2026); 0.32 does not, vllm#53912 is still open.
        "engine_kwargs": {"enable_prefix_caching": True},
    },
    {
        "key": "qwen3.8-27b",
        "name": "Qwen3.8-27B",
        "hf_model_id": "Qwen/Qwen3.8-27B",
        "description": "Larger Qwen of the same family (Fig. 6 reference); evaluated untrained only.",
        "size_gb": 54.0,
        "expected_load_seconds": 600,
        # Model card, instruct (non-thinking) mode: the same settings as Qwen3.5-9B.
        "request_defaults": {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 20,
            "presence_penalty": 1.5,
            "chat_template_kwargs": {"enable_thinking": False},
        },
        "engine_kwargs": {"enable_prefix_caching": True},
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
    {
        "key": "gemma-4-31b",
        "name": "Gemma 4 31B",
        "hf_model_id": "google/gemma-4-31B-it",
        "description": "Larger Gemma 4 (dense); untrained reference, evaluated only.",
        "size_gb": 63.0,
        "expected_load_seconds": 600,
        # Model card: the same standardized sampling as Gemma 4 E4B.
        "request_defaults": {
            "temperature": 1.0,
            "top_p": 0.95,
            "top_k": 64,
            "chat_template_kwargs": {"enable_thinking": False},
        },
    },
    {
        "key": "granite-4.1-30b",
        "name": "Granite 4.1 30B",
        "hf_model_id": "ibm-granite/granite-4.1-30b",
        "description": "Larger Granite 4.1 (dense, bf16); untrained reference, evaluated only.",
        "size_gb": 58.0,
        "expected_load_seconds": 600,
        # No recommended sampling (generation_config is empty): greedy, as Granite 4.1 8B.
        "request_defaults": {"temperature": 0.0},
    },
    {
        "key": "llama-3.3-70b",
        "name": "Llama 3.3 70B (FP8)",
        "hf_model_id": "RedHatAI/Llama-3.3-70B-Instruct-FP8-dynamic",
        "description": "Older (Dec 2024), much larger model of another family; FP8 so it fits the RTX "
        "PRO 6000. Untrained reference, evaluated only.",
        "size_gb": 71.0,
        "expected_load_seconds": 900,
        # generation_config.json of the model.
        "request_defaults": {"temperature": 0.6, "top_p": 0.9},
    },
]

HF_TO_KEY = {model["hf_model_id"]: model["key"] for model in AVAILABLE_MODELS}
KEY_TO_MODEL = {model["key"]: model for model in AVAILABLE_MODELS}
KEY_TO_HF = {model["key"]: model["hf_model_id"] for model in AVAILABLE_MODELS}
