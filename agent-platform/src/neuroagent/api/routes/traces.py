"""Trace listing and download endpoints."""

from __future__ import annotations

import json

from fastapi import APIRouter, HTTPException, Request

router = APIRouter(tags=["traces"])


@router.get("/traces")
def list_traces(request: Request) -> list[dict]:
    """List saved trace files available for replay."""
    traces_dir = request.app.state.traces_dir
    result = []
    for trace_file in sorted(traces_dir.glob("*.json")):
        try:
            data = json.loads(trace_file.read_text())
            result.append({
                "trace_id": trace_file.stem,
                "case_id": data.get("case_id"),
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
