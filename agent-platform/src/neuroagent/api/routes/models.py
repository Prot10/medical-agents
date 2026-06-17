"""Model listing, loading, and status endpoints."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import signal
from pathlib import Path

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter(tags=["models"])
logger = logging.getLogger(__name__)

# expected_load_seconds reflects cold-load from EOS (~70 MB/s sequential read
# + ~60s constant overhead for engine init / compile-cache replay). Warm loads
# (page cache hot) are ~30-40s regardless of model size.
#
# `supports_tools` is whether the model emits structured `tool_calls` via vLLM
# (i.e. usable in the ReAct loop). Verified empirically per model below. Models
# marked False can only be used in dual-model mode as the text-only specialist.
AVAILABLE_MODELS = [
    {
        "key": "qwen3.5-4b",
        "name": "Qwen3.5-4B",
        "hf_model_id": "Qwen/Qwen3.5-4B",
        "description": "Smallest Qwen3.5. Native tool calling (qwen3_coder parser).",
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
        "description": "Best Qwen quality. AWQ Marlin. Native tool calling (inferred).",
        "size_gb": 21.0,
        "expected_load_seconds": 360,
        "supports_tools": True,
    },
    {
        "key": "medgemma-4b",
        "name": "MedGemma 1.5 4B",
        "hf_model_id": "google/medgemma-1.5-4b-it",
        "description": "Medical specialist, fast. Text-only. (Gated — needs HF token.)",
        "size_gb": 8.1,
        "expected_load_seconds": 180,
        "supports_tools": False,
    },
    {
        "key": "medgemma-27b",
        "name": "MedGemma 27B",
        "hf_model_id": "ig1/medgemma-27b-text-it-FP8-Dynamic",
        "description": "Medical specialist, best quality. FP8. Text-only (Gemma not tool-trained).",
        "size_gb": 30.0,
        "expected_load_seconds": 500,
        "supports_tools": False,
    },
    {
        "key": "nemotron-nano-9b-v2",
        "name": "Nemotron Nano 9B v2",
        "hf_model_id": "nvidia/NVIDIA-Nemotron-Nano-9B-v2",
        "description": "NVIDIA Nemotron Nano (hybrid Mamba/Transformer). Native tool calling.",
        "size_gb": 17.0,
        "expected_load_seconds": 300,
        "supports_tools": True,
    },
    {
        "key": "nemotron-3-nano-4b",
        "name": "Nemotron-3 Nano 4B",
        "hf_model_id": "nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16",
        "description": "NVIDIA Nemotron-3 latest gen, smallest. Native tool calling (qwen3_coder parser + nano_v3 reasoning).",
        "size_gb": 7.5,
        "expected_load_seconds": 180,
        "supports_tools": True,
    },
    {
        "key": "gemma-4-e2b",
        "name": "Gemma 4 E2B",
        "hf_model_id": "google/gemma-4-E2B-it",
        "description": "Google Gemma 4, 5B total / 2B effective (PLE). Native tool calling. Multimodal.",
        "size_gb": 9.6,
        "expected_load_seconds": 240,
        "supports_tools": True,
    },
    {
        "key": "gemma-4-e4b",
        "name": "Gemma 4 E4B",
        "hf_model_id": "google/gemma-4-E4B-it",
        "description": "Google Gemma 4, 8B total / 4B effective (PLE). Native tool calling. Multimodal.",
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

_HF_TO_KEY = {m["hf_model_id"]: m["key"] for m in AVAILABLE_MODELS}
_KEY_TO_MODEL = {m["key"]: m for m in AVAILABLE_MODELS}

_LLM_BACKENDS = [
    ("http://localhost:8000", "vllm"),
    ("http://localhost:11434", "ollama"),
]

# Module-level state
_loading_model: str | None = None
_vllm_process: asyncio.subprocess.Process | None = None

_SERVE_SCRIPT = Path(__file__).resolve().parents[4] / "scripts" / "serve_model.sh"


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


async def _kill_vllm() -> None:
    """Kill any running vLLM processes."""
    global _vllm_process

    if _vllm_process is not None:
        try:
            # Kill the entire process group
            os.killpg(os.getpgid(_vllm_process.pid), signal.SIGTERM)
        except (ProcessLookupError, OSError):
            pass
        try:
            await asyncio.wait_for(_vllm_process.wait(), timeout=10)
        except asyncio.TimeoutError:
            try:
                os.killpg(os.getpgid(_vllm_process.pid), signal.SIGKILL)
            except (ProcessLookupError, OSError):
                pass
        _vllm_process = None

    # Also pkill in case started externally — kill serve script, vllm_serve,
    # and any orphaned EngineCore workers that hold GPU memory
    for pattern in ["vllm_serve.py", "serve_model.sh", "VLLM::EngineCore"]:
        proc = await asyncio.create_subprocess_exec(
            "pkill", "-9", "-f", pattern,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await proc.wait()


@router.get("/models")
async def list_models() -> list[dict]:
    """Return available models with their current status."""
    active_models = await _get_active_models()
    active_keys = {m["key"] for m in active_models}

    result = []
    for m in AVAILABLE_MODELS:
        if _loading_model == m["key"]:
            status = "loading"
        elif m["key"] in active_keys:
            status = "ready"
        else:
            status = "offline"
        result.append({
            "key": m["key"],
            "name": m["name"],
            "hf_model_id": m["hf_model_id"],
            "description": m["description"],
            "size_gb": m["size_gb"],
            "expected_load_seconds": m["expected_load_seconds"],
            "supports_tools": m.get("supports_tools", True),
            "status": status,
        })

    # Add Ollama models not in our static list
    static_keys = {m["key"] for m in AVAILABLE_MODELS}
    for am in active_models:
        if am["key"] not in static_keys:
            result.append({
                "key": am["key"],
                "name": am["model_id"],
                "hf_model_id": am["model_id"],
                "description": f"Ollama model ({am['backend']})",
                "size_gb": 0,
                "expected_load_seconds": 60,
                "supports_tools": True,
                "status": "ready",
            })
    return result


@router.post("/models/{model_key}/load")
async def load_model(model_key: str) -> StreamingResponse:
    """Load a vLLM model, streaming progress via SSE."""
    if model_key not in _KEY_TO_MODEL:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown model: {model_key}. Available: {list(_KEY_TO_MODEL.keys())}",
        )

    model_info = _KEY_TO_MODEL[model_key]

    async def _stream():
        global _loading_model, _vllm_process

        model_name = model_info["name"]
        size_gb = model_info["size_gb"]
        expected_seconds = model_info["expected_load_seconds"]
        timeout_seconds = 600

        def sse(data: dict) -> str:
            return f"data: {json.dumps(data)}\n\n"

        try:
            # Step 1: Kill existing vLLM if running
            active = await _get_active_models()
            vllm_active = [m for m in active if m["backend"] == "vllm"]

            if vllm_active:
                yield sse({
                    "phase": "unloading",
                    "message": f"Stopping {vllm_active[0]['key']}...",
                    "progress": 0,
                })
                await _kill_vllm()
                await asyncio.sleep(3)

            # Step 2: Start loading
            _loading_model = model_key
            logger.info("Loading model %s via %s", model_key, _SERVE_SCRIPT)

            yield sse({
                "phase": "starting",
                "model": model_key,
                "model_name": model_name,
                "size_gb": size_gb,
                "expected_seconds": expected_seconds,
                "message": f"Starting vLLM for {model_name} ({size_gb:.1f} GB)...",
                "progress": 0,
            })

            # Launch serve_model.sh
            _vllm_process = await asyncio.create_subprocess_exec(
                "bash", str(_SERVE_SCRIPT), model_key,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                start_new_session=True,
            )

            # Step 3: Poll and stream progress
            elapsed = 0
            poll_interval = 3
            phase = "loading"
            last_log_line = ""

            async with httpx.AsyncClient(timeout=5.0) as client:
                while elapsed < timeout_seconds:
                    await asyncio.sleep(poll_interval)
                    elapsed += poll_interval

                    # Read any available stdout from vLLM (non-blocking)
                    if _vllm_process.stdout:
                        try:
                            chunk = await asyncio.wait_for(
                                _vllm_process.stdout.read(4096), timeout=0.1
                            )
                            if chunk:
                                lines = chunk.decode(errors="replace").strip().split("\n")
                                for line in lines:
                                    line = line.strip()
                                    if not line:
                                        continue
                                    # Detect loading phases from vLLM output
                                    if "Loading model" in line or "loading weight" in line.lower():
                                        phase = "weights"
                                    elif "CUDA graph" in line or "cudagraph" in line.lower():
                                        phase = "cuda_graphs"
                                    elif "Uvicorn running" in line or "Application startup" in line:
                                        phase = "ready"
                                    last_log_line = line[-120:]  # truncate
                        except asyncio.TimeoutError:
                            pass

                    # Check if process died
                    if _vllm_process.returncode is not None:
                        _loading_model = None
                        # Read remaining output for error message
                        err_msg = ""
                        if _vllm_process.stdout:
                            remaining = await _vllm_process.stdout.read()
                            err_msg = remaining.decode(errors="replace")[-500:]
                        yield sse({
                            "phase": "error",
                            "message": f"vLLM exited with code {_vllm_process.returncode}",
                            "detail": err_msg,
                            "progress": 0,
                        })
                        return

                    # Check if model is ready
                    try:
                        resp = await client.get("http://localhost:8000/v1/models")
                        if resp.status_code == 200:
                            _loading_model = None
                            yield sse({
                                "phase": "ready",
                                "model": model_key,
                                "model_name": model_name,
                                "message": f"{model_name} is ready",
                                "elapsed": elapsed,
                                "progress": 100,
                            })
                            return
                    except Exception:
                        pass

                    # Estimate progress: use elapsed/expected, capped at 95%
                    progress = min(95, int((elapsed / expected_seconds) * 90))

                    phase_labels = {
                        "loading": "Loading model weights",
                        "weights": "Loading model weights",
                        "cuda_graphs": "Compiling CUDA graphs",
                    }
                    phase_label = phase_labels.get(phase, "Initializing")

                    yield sse({
                        "phase": phase,
                        "message": f"{phase_label}...",
                        "elapsed": elapsed,
                        "expected_seconds": expected_seconds,
                        "size_gb": size_gb,
                        "progress": progress,
                        "log": last_log_line if last_log_line else None,
                    })

            # Timeout
            _loading_model = None
            yield sse({
                "phase": "error",
                "message": f"Timeout after {timeout_seconds}s",
                "progress": 0,
            })

        except Exception as exc:
            _loading_model = None
            logger.exception("Error loading model %s", model_key)
            yield sse({
                "phase": "error",
                "message": str(exc),
                "progress": 0,
            })

    return StreamingResponse(
        _stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/models/unload")
async def unload_model() -> dict:
    """Stop any running vLLM model server."""
    global _loading_model
    _loading_model = None
    await _kill_vllm()
    return {"status": "ok", "message": "Model server stopped"}
