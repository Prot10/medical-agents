"""Model API lifecycle behavior for registered and external vLLM servers."""

from __future__ import annotations

import asyncio
import json

from neuroagent.api.routes import models


def _events(payload: bytes) -> list[dict]:
    return [
        json.loads(line.removeprefix("data: "))
        for line in payload.decode().splitlines()
        if line.startswith("data: ")
    ]


async def _load_events(model_key: str) -> list[dict]:
    response = await models.load_model(model_key)
    chunks = []
    async for chunk in response.body_iterator:
        chunks.append(chunk.encode() if isinstance(chunk, str) else chunk)
    return _events(b"".join(chunks))


def test_load_is_idempotent_when_requested_model_is_already_ready(monkeypatch):
    async def active_models():
        return [{"key": "qwen3.5-9b", "backend": "vllm"}]

    async def fail_spawn(*args, **kwargs):
        raise AssertionError("an already-ready model must not start another server")

    monkeypatch.setattr(models, "_get_active_models", active_models)
    monkeypatch.setattr(models.asyncio, "create_subprocess_exec", fail_spawn)
    monkeypatch.setattr(models, "_vllm_process", None)

    events = asyncio.run(_load_events("qwen3.5-9b"))

    assert events == [
        {
            "phase": "ready",
            "model": "qwen3.5-9b",
            "model_name": "Qwen3.5-9B",
            "message": "Qwen3.5-9B is already ready",
            "elapsed": 0,
            "progress": 100,
        }
    ]


def test_load_refuses_to_replace_externally_managed_server(monkeypatch):
    async def active_models():
        return [{"key": "qwen3.5-9b", "backend": "vllm"}]

    async def fail_spawn(*args, **kwargs):
        raise AssertionError("an external server must not be replaced")

    monkeypatch.setattr(models, "_get_active_models", active_models)
    monkeypatch.setattr(models.asyncio, "create_subprocess_exec", fail_spawn)
    monkeypatch.setattr(models, "_vllm_process", None)

    events = asyncio.run(_load_events("gemma-4-e4b"))

    assert events == [
        {
            "phase": "error",
            "message": (
                "Cannot replace externally managed model qwen3.5-9b; "
                "stop its vLLM server first"
            ),
            "progress": 0,
        }
    ]
