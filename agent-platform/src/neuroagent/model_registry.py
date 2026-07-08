"""Shared model registry for API routes and trace metadata."""

from __future__ import annotations

VLLM_BASE_URL = "http://localhost:8000/v1"
OLLAMA_BASE_URL = "http://localhost:11434/v1"

AVAILABLE_MODELS: list[dict] = [
    {
        "key": "qwen3.5-4b",
        "name": "Qwen3.5-4B",
        "hf_model_id": "Qwen/Qwen3.5-4B",
        "description": "Smallest Qwen3.5. Native tool calling.",
        "size_gb": 8.8,
        "expected_load_seconds": 180,
        "supports_tools": True,
    },
    {
        "key": "qwen3.5-9b",
        "name": "Qwen3.5-9B",
        "hf_model_id": "Qwen/Qwen3.5-9B",
        "description": "Fast Qwen3.5 with thinking mode. Native tool calling.",
        "size_gb": 19.0,
        "expected_load_seconds": 300,
        "supports_tools": True,
    },
    {
        "key": "qwen3.5-27b-awq",
        "name": "Qwen3.5-27B AWQ",
        "hf_model_id": "QuantTrio/Qwen3.5-27B-AWQ",
        "description": "Best Qwen quality. AWQ Marlin. Native tool calling.",
        "size_gb": 21.0,
        "expected_load_seconds": 360,
        "supports_tools": True,
    },
    {
        "key": "medgemma-4b",
        "name": "MedGemma 1.5 4B",
        "hf_model_id": "google/medgemma-1.5-4b-it",
        "description": "Medical text model, fast. Text-only.",
        "size_gb": 8.1,
        "expected_load_seconds": 180,
        "supports_tools": False,
    },
    {
        "key": "medgemma-27b",
        "name": "MedGemma 27B",
        "hf_model_id": "ig1/medgemma-27b-text-it-FP8-Dynamic",
        "description": "Medical text model, best quality. Text-only.",
        "size_gb": 30.0,
        "expected_load_seconds": 500,
        "supports_tools": False,
    },
    {
        "key": "nemotron-nano-9b-v2",
        "name": "Nemotron Nano 9B v2",
        "hf_model_id": "nvidia/NVIDIA-Nemotron-Nano-9B-v2",
        "description": "NVIDIA Nemotron Nano. Native tool calling.",
        "size_gb": 17.0,
        "expected_load_seconds": 300,
        "supports_tools": True,
    },
    {
        "key": "nemotron-3-nano-4b",
        "name": "Nemotron-3 Nano 4B",
        "hf_model_id": "nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16",
        "description": "NVIDIA Nemotron-3 latest gen, smallest. Native tool calling.",
        "size_gb": 7.5,
        "expected_load_seconds": 180,
        "supports_tools": True,
    },
    {
        "key": "gemma-4-e2b",
        "name": "Gemma 4 E2B",
        "hf_model_id": "google/gemma-4-E2B-it",
        "description": "Google Gemma 4, 5B total / 2B effective. Native tool calling.",
        "size_gb": 9.6,
        "expected_load_seconds": 240,
        "supports_tools": True,
    },
    {
        "key": "gemma-4-e4b",
        "name": "Gemma 4 E4B",
        "hf_model_id": "google/gemma-4-E4B-it",
        "description": "Google Gemma 4, 8B total / 4B effective. Native tool calling.",
        "size_gb": 15.0,
        "expected_load_seconds": 300,
        "supports_tools": True,
    },
    {
        "key": "gemma-4-12b",
        "name": "Gemma 4 12B",
        "hf_model_id": "google/gemma-4-12B-it",
        "description": "Google Gemma 4, encoder-free 12B dense multimodal. Native tool calling.",
        "size_gb": 22.3,
        "expected_load_seconds": 420,
        "supports_tools": True,
    },
]

HF_TO_KEY = {m["hf_model_id"]: m["key"] for m in AVAILABLE_MODELS}
KEY_TO_MODEL = {m["key"]: m for m in AVAILABLE_MODELS}
KEY_TO_HF = {m["key"]: m["hf_model_id"] for m in AVAILABLE_MODELS}
