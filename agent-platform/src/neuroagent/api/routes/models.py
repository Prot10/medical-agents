"""Model listing and status endpoints."""

from __future__ import annotations

import logging

import httpx
from fastapi import APIRouter

router = APIRouter(tags=["models"])
logger = logging.getLogger(__name__)

AVAILABLE_MODELS = [
    {
        "key": "qwen3.5-9b",
        "name": "Qwen3.5-9B",
        "hf_model_id": "Qwen/Qwen3.5-9B",
        "description": "Fast, good tool calling. Thinking mode enabled.",
    },
    {
        "key": "qwen3.5-27b-awq",
        "name": "Qwen3.5-27B AWQ",
        "hf_model_id": "QuantTrio/Qwen3.5-27B-AWQ",
        "description": "Best quality. AWQ Marlin quantization.",
    },
    {
        "key": "medgemma-4b",
        "name": "MedGemma 1.5 4B",
        "hf_model_id": "google/medgemma-1.5-4b-it",
        "description": "Medical specialist, fast.",
    },
    {
        "key": "medgemma-27b",
        "name": "MedGemma 27B",
        "hf_model_id": "ig1/medgemma-27b-text-it-FP8-Dynamic",
        "description": "Medical specialist, best quality.",
    },
]

# Map HF model ID to our key
_HF_TO_KEY = {m["hf_model_id"]: m["key"] for m in AVAILABLE_MODELS}

# Backend endpoints to probe for running models
_LLM_BACKENDS = [
    ("http://localhost:8000", "vllm"),   # vLLM
    ("http://localhost:11434", "ollama"),  # Ollama
]


async def _get_active_models() -> list[dict]:
    """Probe vLLM and Ollama to find which models are currently loaded."""
    active: list[dict] = []
    async with httpx.AsyncClient(timeout=3.0) as client:
        for base_url, backend in _LLM_BACKENDS:
            try:
                resp = await client.get(f"{base_url}/v1/models")
                if resp.status_code == 200:
                    data = resp.json()
                    for m in data.get("data", []):
                        model_id = m.get("id", "")
                        active.append({
                            "key": _HF_TO_KEY.get(model_id, model_id),
                            "model_id": model_id,
                            "backend": backend,
                            "base_url": f"{base_url}/v1",
                        })
            except Exception:
                continue
    return active



@router.get("/models")
async def list_models() -> list[dict]:
    """Return available models with their current status."""
    active_models = await _get_active_models()
    active_keys = {m["key"] for m in active_models}

    result = []
    # Add the static model list with status
    for m in AVAILABLE_MODELS:
        status = "ready" if m["key"] in active_keys else "offline"
        result.append({**m, "status": status})

    # Add any Ollama models not in the static list (e.g. qwen3.5:4b)
    static_keys = {m["key"] for m in AVAILABLE_MODELS}
    for am in active_models:
        if am["key"] not in static_keys:
            result.append({
                "key": am["key"],
                "name": am["model_id"],
                "hf_model_id": am["model_id"],
                "description": f"Ollama model ({am['backend']})",
                "status": "ready",
            })
    return result
