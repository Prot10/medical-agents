"""Agent execution endpoint with SSE streaming."""

from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any, AsyncIterator

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from neuroagent.model_registry import KEY_TO_HF, OLLAMA_BASE_URL, VLLM_BASE_URL
from neuroagent_schemas import NeuroBenchCase

from ...agent.orchestrator import AgentOrchestrator, load_agent_config
from ...evaluation.runner import format_patient_info
from ..services.agent_evaluation import stream_evaluation_events
from ..services.sse_bridge import SSEBridge
from .traces import validate_trace_id
from ...rules.rules_engine import AVAILABLE_HOSPITALS, RulesEngine
from ...tools.mock_server import MockServer
from ...tools.tool_registry import ToolRegistry

logger = logging.getLogger(__name__)
router = APIRouter(tags=["agent"])

class RunRequest(BaseModel):
    case_id: str
    hospital: str = "us_mayo"
    model: str = "qwen3.5-9b"
    base_url: str | None = None   # custom LLM endpoint (e.g. GitHub Models)
    api_key: str | None = None    # API key for custom endpoint


class EvaluateRequest(BaseModel):
    case_id: str
    model: str = "qwen3.5-9b"          # evaluator model
    events: list[dict] = Field(default_factory=list)  # agent events to evaluate
    final_response: str = ""            # agent's final assessment text
    tools_called: list[str] = Field(default_factory=list)  # tools the agent called


class ReplayRequest(BaseModel):
    trace_id: str


def _sse_event(data: dict) -> str:
    return f"data: {json.dumps(data, default=str)}\n\n"



# _format_initial_info removed — use format_patient_info from evaluation.runner


async def _stream_agent_events(
    case: NeuroBenchCase,
    hospital: str,
    model_hf_id: str,
    base_url: str,
    rules_dir: str,
    traces_dir: Any,
    api_key: str = "not-needed",
) -> AsyncIterator[str]:
    """Run agent in a thread, push events to an async queue for true SSE streaming."""

    mock_server = MockServer(case)
    tool_registry = ToolRegistry.create_default_registry(mock_server=mock_server)
    rules_engine = RulesEngine(rules_dir, hospital=hospital)

    config = load_agent_config(
        base_url=base_url,
        model=model_hf_id,
        api_key=api_key,
        hospital=hospital,
    )
    agent = AgentOrchestrator(
        config=config, tool_registry=tool_registry, rules_engine=rules_engine,
    )
    patient_info = format_patient_info(case)

    # Yield run_started immediately
    yield _sse_event({
        "type": "run_started",
        "case_id": case.case_id,
        "hospital": hospital,
        "model": model_hf_id,
        "max_turns": config.max_turns,
    })

    # Thread-safe bridge so events stream as they're produced (the sync agent
    # runs in a worker thread; asyncio.Queue is not thread-safe on its own).
    bridge = SSEBridge()
    all_events: list[dict] = []

    def _save_trace() -> None:
        """Persist the trace for replay. Runs in the worker thread, so the
        potentially large JSON write never blocks the event loop, and it runs
        even if the SSE client disconnected before the run finished."""
        run_complete = next(
            (e for e in all_events if e.get("type") == "run_complete"), None
        )
        if not (run_complete and traces_dir):
            return
        trace_data = {
            "case_id": case.case_id,
            "hospital": hospital,
            "model": model_hf_id,
            "condition": case.condition.value,
            "difficulty": case.difficulty.value,
            "events": all_events,
            **{k: v for k, v in run_complete.items() if k != "type"},
        }
        trace_file = traces_dir / f"{case.case_id}_{time.time_ns()}.json"
        trace_file.write_text(json.dumps(trace_data, indent=2, default=str))

    def _run_sync():
        """Run in thread pool — hands each event to the bridge."""
        try:
            for event in agent.run_streaming(
                patient_info=patient_info,
                case_id=case.case_id,
            ):
                all_events.append(event)
                bridge.put_from_thread(event)
        except Exception as e:
            bridge.put_from_thread({"type": "error", "message": str(e)})
        finally:
            try:
                _save_trace()
            except Exception:
                logger.exception("Failed to save trace for case %s", case.case_id)
            bridge.put_from_thread(None)  # sentinel

    loop = asyncio.get_running_loop()
    run_future = loop.run_in_executor(None, _run_sync)
    run_future.add_done_callback(_log_worker_failure)

    # Consume events from the bridge and yield as SSE
    completed = False
    try:
        async for event in bridge.events():
            yield _sse_event(event)
        completed = True
    finally:
        if not completed:
            # Client disconnected (GeneratorExit/CancelledError). Stop
            # buffering; the worker keeps running and still saves the trace.
            bridge.mark_disconnected()
            logger.info(
                "SSE client disconnected during run for case %s; "
                "the agent run continues and the trace will still be saved",
                case.case_id,
            )


def _log_worker_failure(future: Any) -> None:
    """Surface unexpected executor-task failures instead of losing them."""
    if future.cancelled():
        return
    exc = future.exception()
    if exc is not None:
        logger.error("Agent worker thread failed", exc_info=exc)


@router.post("/agent/run")
async def run_agent(body: RunRequest, request: Request):
    """Run the agent on a case and stream results via SSE."""
    case = request.app.state.case_objects.get(body.case_id)
    if case is None:
        raise HTTPException(status_code=404, detail=f"Case '{body.case_id}' not found")
    if body.hospital not in AVAILABLE_HOSPITALS:
        raise HTTPException(status_code=400, detail=f"Hospital '{body.hospital}' not found")
    # Resolve model key to model ID and base URL
    api_key = "not-needed"
    if body.model.startswith("copilot:"):
        # GitHub Copilot model — get token from copilot module
        from .copilot import get_copilot_api_token
        copilot_token = await get_copilot_api_token()
        if not copilot_token:
            raise HTTPException(status_code=401, detail="Not authenticated with GitHub Copilot")
        model_hf_id = body.model.removeprefix("copilot:")
        base_url = "https://api.githubcopilot.com"
        api_key = copilot_token
    elif body.base_url and body.api_key:
        # Custom provider (e.g. GitHub Models)
        model_hf_id = body.model
        base_url = body.base_url
        api_key = body.api_key
    elif body.model in KEY_TO_HF:
        model_hf_id = KEY_TO_HF[body.model]
        base_url = VLLM_BASE_URL
    else:
        # Assume Ollama model (e.g. "qwen3.5:4b")
        model_hf_id = body.model
        base_url = OLLAMA_BASE_URL

    return StreamingResponse(
        _stream_agent_events(
            case=case,
            hospital=body.hospital,
            model_hf_id=model_hf_id,
            base_url=base_url,
            rules_dir=request.app.state.rules_dir,
            traces_dir=request.app.state.traces_dir,
            # Pass the resolved key — for copilot models this is the exchanged
            # Copilot token, which `body.api_key or ...` used to drop.
            api_key=api_key,
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
    trace_id = validate_trace_id(body.trace_id)
    trace_file = request.app.state.traces_dir / f"{trace_id}.json"
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
            # Fast replay: ~80 tokens/sec for deltas, brief pauses for block events
            etype = event.get("type", "")
            if etype in ("think_delta", "content_delta"):
                await asyncio.sleep(0.0125)
            elif etype in ("tool_call", "tool_result", "thinking", "assessment"):
                await asyncio.sleep(0.05)
            else:
                await asyncio.sleep(0.02)

    return StreamingResponse(
        _replay(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )



@router.post("/agent/evaluate")
async def evaluate_agent(body: EvaluateRequest, request: Request):
    """Evaluate agent output against ground truth. Streams metrics + LLM judge."""
    case = request.app.state.case_objects.get(body.case_id)
    if case is None:
        raise HTTPException(status_code=404, detail=f"Case '{body.case_id}' not found")

    # Resolve evaluator model
    if body.model.startswith("copilot:"):
        from .copilot import get_copilot_api_token
        copilot_token = await get_copilot_api_token()
        if not copilot_token:
            raise HTTPException(status_code=401, detail="Not authenticated with GitHub Copilot")
        evaluator_model = body.model.removeprefix("copilot:")
        evaluator_base_url = "https://api.githubcopilot.com"
        evaluator_api_key = copilot_token
    elif body.model in KEY_TO_HF:
        evaluator_model = KEY_TO_HF[body.model]
        evaluator_base_url = VLLM_BASE_URL
        evaluator_api_key = "not-needed"
    else:
        evaluator_model = body.model
        evaluator_base_url = OLLAMA_BASE_URL
        evaluator_api_key = "not-needed"

    return StreamingResponse(
        (
            _sse_event(event)
            async for event in stream_evaluation_events(
                case=case,
                events=body.events,
                final_response=body.final_response,
                tools_called=body.tools_called,
                total_tool_calls=len(body.tools_called),
                evaluator_model=evaluator_model,
                evaluator_base_url=evaluator_base_url,
                evaluator_api_key=evaluator_api_key,
            )
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
