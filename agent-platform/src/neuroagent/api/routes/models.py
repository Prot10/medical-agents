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


async def _get_active_model(base_url: str = "http://localhost:8000") -> str | None:
    """Probe the vLLM server to find which model is currently loaded."""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{base_url}/v1/models")
            if resp.status_code == 200:
                data = resp.json()
                models = data.get("data", [])
                if models:
                    model_id = models[0].get("id", "")
                    return _HF_TO_KEY.get(model_id, model_id)
    except Exception:
        pass
    return None


@router.get("/models")
async def list_models() -> list[dict]:
    """Return available models with their current status."""
    active_key = await _get_active_model()

    result = []
    for m in AVAILABLE_MODELS:
        status = "offline"
        if active_key == m["key"]:
            status = "ready"
        result.append({**m, "status": status})
    return result
