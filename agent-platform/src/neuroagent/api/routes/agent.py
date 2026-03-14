"""Agent execution endpoint with SSE streaming."""

from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any, AsyncIterator

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from neuroagent_schemas import NeuroBenchCase

from ...agent.orchestrator import AgentConfig, AgentOrchestrator
from ...rules.rules_engine import AVAILABLE_HOSPITALS, RulesEngine
from ...tools.mock_server import MockServer
from ...tools.tool_registry import ToolRegistry

logger = logging.getLogger(__name__)
router = APIRouter(tags=["agent"])

MODEL_KEY_TO_HF = {
    "qwen3.5-9b": "Qwen/Qwen3.5-9B",
    "qwen3.5-27b-awq": "QuantTrio/Qwen3.5-27B-AWQ",
    "medgemma-4b": "google/medgemma-1.5-4b-it",
    "medgemma-27b": "ig1/medgemma-27b-text-it-FP8-Dynamic",
}


class RunRequest(BaseModel):
    case_id: str
    hospital: str = "us_mayo"
    model: str = "qwen3.5-9b"


class ReplayRequest(BaseModel):
    trace_id: str


def _sse_event(data: dict) -> str:
    return f"data: {json.dumps(data, default=str)}\n\n"


def _format_initial_info(case: NeuroBenchCase) -> str:
    parts = [
        f"Patient: {case.patient.demographics.age}-year-old {case.patient.demographics.sex}",
        f"Chief complaint: {case.patient.chief_complaint}",
        f"History of present illness: {case.patient.history_present_illness}",
    ]
    pmh = case.patient.clinical_history.past_medical_history
    if pmh:
        parts.append(f"Past medical history: {', '.join(pmh)}")
    meds = case.patient.clinical_history.medications
    if meds:
        med_strs = [f"{m.drug} {m.dose} {m.frequency}" for m in meds]
        parts.append(f"Current medications: {', '.join(med_strs)}")
    allergies = case.patient.clinical_history.allergies
    if allergies:
        parts.append(f"Allergies: {', '.join(allergies)}")
    parts.append(f"Neurological examination: {case.patient.neurological_exam.model_dump_json()}")
    parts.append(f"Vitals: {case.patient.vitals.model_dump_json()}")
    return "\n".join(parts)


async def _stream_agent_events(
    case: NeuroBenchCase,
    hospital: str,
    model_hf_id: str,
    rules_dir: str,
    traces_dir: Any,
) -> AsyncIterator[str]:
    """Run agent in a thread, push events to an async queue for true SSE streaming."""
    mock_server = MockServer(case)
    tool_registry = ToolRegistry.create_default_registry(mock_server=mock_server)
    rules_engine = RulesEngine(rules_dir, hospital=hospital)

    config = AgentConfig(model=model_hf_id, hospital=hospital)
    agent = AgentOrchestrator(
        config=config, tool_registry=tool_registry, rules_engine=rules_engine,
    )
    patient_info = _format_initial_info(case)

    # Yield run_started immediately
    yield _sse_event({
        "type": "run_started",
        "case_id": case.case_id,
        "hospital": hospital,
        "model": model_hf_id,
        "max_turns": config.max_turns,
    })

    # Use an async queue so events stream as they're produced
    queue: asyncio.Queue[dict | None] = asyncio.Queue()
    all_events: list[dict] = []

    def _run_sync():
        """Run in thread pool — puts each event onto the queue."""
        try:
            for event in agent.run_streaming(
                patient_info=patient_info,
                case_id=case.case_id,
            ):
                all_events.append(event)
                queue.put_nowait(event)
        except Exception as e:
            queue.put_nowait({"type": "error", "message": str(e)})
        finally:
            queue.put_nowait(None)  # sentinel

    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, _run_sync)

    # Consume events from queue and yield as SSE
    while True:
        event = await queue.get()
        if event is None:
            break
        yield _sse_event(event)

    # Save trace for replay
    run_complete = next((e for e in all_events if e.get("type") == "run_complete"), None)
    if run_complete and traces_dir:
        trace_data = {
            "case_id": case.case_id,
            "hospital": hospital,
            "model": model_hf_id,
            "events": all_events,
            **{k: v for k, v in run_complete.items() if k != "type"},
        }
        trace_file = traces_dir / f"{case.case_id}_{time.time_ns()}.json"
        trace_file.write_text(json.dumps(trace_data, indent=2, default=str))


@router.post("/agent/run")
async def run_agent(body: RunRequest, request: Request):
    """Run the agent on a case and stream results via SSE."""
    case = request.app.state.case_objects.get(body.case_id)
    if case is None:
        raise HTTPException(status_code=404, detail=f"Case '{body.case_id}' not found")
    if body.hospital not in AVAILABLE_HOSPITALS:
        raise HTTPException(status_code=400, detail=f"Hospital '{body.hospital}' not found")
    model_hf_id = MODEL_KEY_TO_HF.get(body.model)
    if model_hf_id is None:
        raise HTTPException(status_code=400, detail=f"Model '{body.model}' not found")

    return StreamingResponse(
        _stream_agent_events(
            case=case,
            hospital=body.hospital,
            model_hf_id=model_hf_id,
            rules_dir=request.app.state.rules_dir,
            traces_dir=request.app.state.traces_dir,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/agent/replay")
async def replay_trace(body: ReplayRequest, request: Request):
    """Replay a saved trace as SSE events with small delays."""
    trace_file = request.app.state.traces_dir / f"{body.trace_id}.json"
    if not trace_file.exists():
        raise HTTPException(status_code=404, detail=f"Trace '{body.trace_id}' not found")

    trace_data = json.loads(trace_file.read_text())

    async def _replay() -> AsyncIterator[str]:
        yield _sse_event({
            "type": "run_started",
            "case_id": trace_data.get("case_id"),
            "hospital": trace_data.get("hospital"),
            "model": trace_data.get("model"),
            "max_turns": 15,
        })
        for event in trace_data.get("events", []):
            yield _sse_event(event)
            await asyncio.sleep(0.15)

    return StreamingResponse(
        _replay(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
