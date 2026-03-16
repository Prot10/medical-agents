"""Trace listing, download, and deletion endpoints."""

from __future__ import annotations

import json

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response

router = APIRouter(tags=["traces"])

# Reverse mapping: HuggingFace model ID → short key
_HF_TO_SHORT: dict[str, str] = {
    "Qwen/Qwen3.5-9B": "qwen3.5-9b",
    "QuantTrio/Qwen3.5-27B-AWQ": "qwen3.5-27b-awq",
    "google/medgemma-1.5-4b-it": "medgemma-4b",
    "ig1/medgemma-27b-text-it-FP8-Dynamic": "medgemma-27b",
}


@router.get("/traces")
def list_traces(request: Request) -> list[dict]:
    """List saved trace files with enriched metadata."""
    traces_dir = request.app.state.traces_dir
    case_index: dict[str, dict] = getattr(request.app.state, "case_index", {})
    result = []
    for trace_file in sorted(traces_dir.glob("*.json")):
        try:
            data = json.loads(trace_file.read_text())
            case_id = data.get("case_id", "")
            case_meta = case_index.get(case_id, {})
            model_hf = data.get("model", "")
            result.append({
                "trace_id": trace_file.stem,
                "case_id": case_id,
                "hospital": data.get("hospital", ""),
                "model": model_hf,
                "model_short": _HF_TO_SHORT.get(model_hf, model_hf),
                "condition": data.get("condition") or case_meta.get("condition", ""),
                "difficulty": data.get("difficulty") or case_meta.get("difficulty", ""),
                "total_tool_calls": data.get("total_tool_calls", 0),
                "tools_called": data.get("tools_called", []),
                "total_tokens": data.get("total_tokens", 0),
                "elapsed_time_seconds": data.get("elapsed_time_seconds", 0),
            })
        except Exception:
            continue
    return result


@router.get("/traces/{trace_id}")
def get_trace(trace_id: str, request: Request) -> dict:
    """Download a full trace JSON."""
    trace_file = request.app.state.traces_dir / f"{trace_id}.json"
    if not trace_file.exists():
        raise HTTPException(status_code=404, detail=f"Trace '{trace_id}' not found")
    return json.loads(trace_file.read_text())


@router.delete("/traces/{trace_id}", status_code=204)
def delete_trace(trace_id: str, request: Request) -> Response:
    """Delete a saved trace file."""
    if "/" in trace_id or ".." in trace_id:
        raise HTTPException(status_code=400, detail="Invalid trace ID")
    trace_file = request.app.state.traces_dir / f"{trace_id}.json"
    if not trace_file.exists():
        raise HTTPException(status_code=404, detail=f"Trace '{trace_id}' not found")
    trace_file.unlink()
    return Response(status_code=204)
