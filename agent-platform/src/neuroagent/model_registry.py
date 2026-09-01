"""The fixed under-10B model panel used by benchmark and training profiles."""

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
        "supports_tools": True,
        "adapter": "native-tools",
    },
    {
        "key": "gemma-4-e4b",
        "name": "Gemma 4 E4B",
        "hf_model_id": "google/gemma-4-E4B-it",
        "description": "General open model; native structured tool calling.",
        "size_gb": 15.0,
        "expected_load_seconds": 300,
        "supports_tools": True,
        "adapter": "native-tools",
    },
    {
        "key": "medgemma-1.5-4b",
        "name": "MedGemma 1.5 4B",
        "hf_model_id": "google/medgemma-1.5-4b-it",
        "description": "Medical model evaluated through the strict JSON action adapter.",
        "size_gb": 8.1,
        "expected_load_seconds": 180,
        "supports_tools": False,
        "adapter": "json-action",
    },
]

HF_TO_KEY = {model["hf_model_id"]: model["key"] for model in AVAILABLE_MODELS}
KEY_TO_MODEL = {model["key"]: model for model in AVAILABLE_MODELS}
KEY_TO_HF = {model["key"]: model["hf_model_id"] for model in AVAILABLE_MODELS}
