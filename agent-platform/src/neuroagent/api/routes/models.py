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

from neuroagent.model_registry import AVAILABLE_MODELS, HF_TO_KEY, KEY_TO_MODEL

router = APIRouter(tags=["models"])
logger = logging.getLogger(__name__)

_LLM_BACKENDS = [("http://localhost:8000", "vllm")]

# Module-level state. All mutation of these globals (kill/spawn/assign) must
# happen while holding _models_lock, otherwise two concurrent load requests can
# each spawn a vLLM server and orphan one of the processes on the GPU.
_models_lock = asyncio.Lock()
_loading_model: str | None = None
_vllm_process: asyncio.subprocess.Process | None = None

_SERVE_SCRIPT = Path(__file__).resolve().parents[4] / "scripts" / "runtime" / "serve_model.sh"


async def _get_active_models() -> list[dict]:
    """Probe the local vLLM server for a registered model."""
    active: list[dict] = []
    async with httpx.AsyncClient(timeout=3.0) as client:
        for base_url, backend in _LLM_BACKENDS:
            try:
                resp = await client.get(f"{base_url}/v1/models")
                if resp.status_code == 200:
                    data = resp.json()
                    for m in data.get("data", []):
                        model_id = m.get("id", "")
                        key = HF_TO_KEY.get(model_id)
                        if key is not None:
                            active.append({
                                "key": key,
                                "model_id": model_id,
                                "backend": backend,
                                "base_url": f"{base_url}/v1",
                            })
            except Exception:
                continue
    return active


async def _kill_vllm() -> None:
    """Stop the vLLM process started by this API instance, if any."""
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

    return result


@router.post("/models/{model_key}/load")
async def load_model(model_key: str) -> StreamingResponse:
    """Load a vLLM model, streaming progress via SSE."""
    if model_key not in KEY_TO_MODEL:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown model: {model_key}. Available: {list(KEY_TO_MODEL.keys())}",
        )

    model_info = KEY_TO_MODEL[model_key]

    async def _stream():
        global _loading_model, _vllm_process

        model_name = model_info["name"]
        size_gb = model_info["size_gb"]
        expected_seconds = model_info["expected_load_seconds"]
        timeout_seconds = 600

        def sse(data: dict) -> str:
            return f"data: {json.dumps(data)}\n\n"

        try:
            # Steps 1-2 mutate the module globals (kill old server, spawn new
            # one) — serialize them so concurrent load/unload requests can't
            # orphan a vLLM process.
            async with _models_lock:
                # Step 1: Kill existing vLLM if running
                active = await _get_active_models()
                vllm_active = [m for m in active if m["backend"] == "vllm"]

                if vllm_active:
                    active_key = vllm_active[0]["key"]
                    if active_key == model_key:
                        yield sse({
                            "phase": "ready",
                            "model": model_key,
                            "model_name": model_name,
                            "message": f"{model_name} is already ready",
                            "elapsed": 0,
                            "progress": 100,
                        })
                        return
                    if _vllm_process is None:
                        yield sse({
                            "phase": "error",
                            "message": (
                                f"Cannot replace externally managed model {active_key}; "
                                "stop its vLLM server first"
                            ),
                            "progress": 0,
                        })
                        return
                    yield sse({
                        "phase": "unloading",
                        "message": f"Stopping {active_key}...",
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
                # Local handle: the polling below must track the process this
                # request spawned even if another request later replaces the global.
                proc = _vllm_process

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
                    if proc.stdout:
                        try:
                            chunk = await asyncio.wait_for(
                                proc.stdout.read(4096), timeout=0.1
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
                    if proc.returncode is not None:
                        _loading_model = None
                        # Read remaining output for error message
                        err_msg = ""
                        if proc.stdout:
                            remaining = await proc.stdout.read()
                            err_msg = remaining.decode(errors="replace")[-500:]
                        yield sse({
                            "phase": "error",
                            "message": f"vLLM exited with code {proc.returncode}",
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
    """Stop the vLLM server managed by this API instance, if any."""
    global _loading_model
    async with _models_lock:
        _loading_model = None
        await _kill_vllm()
    return {"status": "ok", "message": "Managed model server stopped"}
