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
from ...agent.reasoning import AgentTrace, AgentTurn
from ...evaluation.metrics import MetricsCalculator
from ...evaluation.llm_judge import LLMJudge
from ...llm.client import LLMClient
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

# Ollama models use their tag as both key and model ID, served on port 11434
OLLAMA_BASE_URL = "http://localhost:11434/v1"
VLLM_BASE_URL = "http://localhost:8000/v1"


class RunRequest(BaseModel):
    case_id: str
    hospital: str = "us_mayo"
    model: str = "qwen3.5-9b"
    base_url: str | None = None   # custom LLM endpoint (e.g. GitHub Models)
    api_key: str | None = None    # API key for custom endpoint


class EvaluateRequest(BaseModel):
    case_id: str
    model: str = "qwen3.5-9b"          # evaluator model
    events: list[dict] = []             # agent events to evaluate
    final_response: str = ""            # agent's final assessment text
    tools_called: list[str] = []        # tools the agent called


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
    base_url: str,
    rules_dir: str,
    traces_dir: Any,
    api_key: str = "not-needed",
) -> AsyncIterator[str]:
    """Run agent in a thread, push events to an async queue for true SSE streaming."""
    mock_server = MockServer(case)
    tool_registry = ToolRegistry.create_default_registry(mock_server=mock_server)
    rules_engine = RulesEngine(rules_dir, hospital=hospital)

    config = AgentConfig(base_url=base_url, model=model_hf_id, api_key=api_key)
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
            "condition": case.condition.value,
            "difficulty": case.difficulty.value,
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
    elif body.model in MODEL_KEY_TO_HF:
        model_hf_id = MODEL_KEY_TO_HF[body.model]
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
            api_key=body.api_key or "not-needed",
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


from pathlib import Path as _Path

_JUDGE_PROMPT_PATH = _Path(__file__).resolve().parents[4] / "config" / "system_prompts" / "llm_judge.md"
_oracle_prompt_cache: str | None = None


def _get_oracle_system_prompt() -> str:
    """Load the oracle evaluation prompt from llm_judge.md (cached)."""
    global _oracle_prompt_cache
    if _oracle_prompt_cache is None:
        _oracle_prompt_cache = _JUDGE_PROMPT_PATH.read_text()
    return _oracle_prompt_cache


async def _stream_evaluation(
    case: NeuroBenchCase,
    events: list[dict],
    final_response: str,
    tools_called: list[str],
    total_tool_calls: int,
    evaluator_model: str,
    evaluator_base_url: str,
    evaluator_api_key: str,
) -> AsyncIterator[str]:
    """Run evaluation (metrics + LLM judge) and stream results as SSE."""
    queue: asyncio.Queue[dict | None] = asyncio.Queue()

    def _run_sync():
        try:
            # Step 1: Rule-based metrics (instant)
            trace = AgentTrace(
                case_id=case.case_id,
                turns=[],
                final_response=final_response,
                total_tool_calls=total_tool_calls,
                tools_called=tools_called,
            )
            calc = MetricsCalculator()
            metrics = calc.compute_all(trace, case.ground_truth)

            queue.put_nowait({
                "type": "metrics",
                "diagnostic_accuracy_top1": metrics.diagnostic_accuracy_top1,
                "diagnostic_accuracy_top3": metrics.diagnostic_accuracy_top3,
                "action_precision": round(metrics.action_precision, 3),
                "action_recall": round(metrics.action_recall, 3),
                "critical_actions_hit": round(metrics.critical_actions_hit, 3),
                "contraindicated_actions_taken": metrics.contraindicated_actions_taken,
                "efficiency_score": round(metrics.efficiency_score, 3),
                "safety_score": round(metrics.safety_score, 3),
            })

            # Step 2: LLM Oracle Judge (streaming)
            queue.put_nowait({"type": "judge_started"})

            llm = LLMClient(
                base_url=evaluator_base_url,
                api_key=evaluator_api_key,
                model=evaluator_model,
                temperature=0.0,
                max_tokens=8192,
                presence_penalty=0.0,
            )

            # Build the full evaluation context
            user_prompt = _build_oracle_user_prompt(case, events, final_response)

            messages = [
                {"role": "system", "content": _get_oracle_system_prompt()},
                {"role": "user", "content": user_prompt},
            ]

            # Stream the judge response
            full_content = []
            for ev in llm.chat_stream(messages=messages, tools=None):
                if ev["type"] == "content_delta":
                    full_content.append(ev["delta"])
                    queue.put_nowait({"type": "judge_delta", "delta": ev["delta"]})

            # Parse the complete JSON response
            full_text = "".join(full_content)
            scores = _parse_oracle_response(full_text)

            queue.put_nowait({"type": "judge_complete", **scores})

        except Exception as e:
            queue.put_nowait({"type": "eval_error", "message": str(e)})
        finally:
            queue.put_nowait(None)

    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, _run_sync)

    while True:
        event = await queue.get()
        if event is None:
            break
        yield _sse_event(event)


def _build_oracle_user_prompt(case: NeuroBenchCase, events: list[dict], final_response: str) -> str:
    """Build the user prompt with full case context, agent trace, and ground truth."""
    # Case presentation
    p = case.patient
    case_section = (
        f"## Case Presentation\n"
        f"**Demographics:** {p.demographics.age}-year-old {p.demographics.sex}\n"
        f"**Chief Complaint:** {p.chief_complaint}\n"
        f"**HPI:** {p.history_present_illness}\n"
        f"**PMH:** {', '.join(p.clinical_history.past_medical_history) or 'None'}\n"
        f"**Medications:** {', '.join(f'{m.drug} {m.dose} {m.frequency}' for m in p.clinical_history.medications) or 'None'}\n"
        f"**Allergies:** {', '.join(p.clinical_history.allergies) or 'NKDA'}\n"
        f"**Neuro Exam:** {p.neurological_exam.model_dump_json()}\n"
        f"**Vitals:** BP {p.vitals.bp_systolic}/{p.vitals.bp_diastolic}, HR {p.vitals.hr}, "
        f"Temp {p.vitals.temp}°C, RR {p.vitals.rr}, SpO2 {p.vitals.spo2}%\n"
    )

    # Agent reasoning trace
    trace_parts = []
    for ev in events:
        t = ev.get("type", "")
        if t == "thinking":
            content = ev.get("content", "")
            think = ev.get("think_content", "")
            if content:
                trace_parts.append(f"[Agent Reasoning]: {content}")
            if think:
                trace_parts.append(f"[Internal Thinking]: {think[:2000]}")
        elif t == "tool_call":
            name = ev.get("tool_name", "unknown")
            args = ev.get("arguments", {})
            trace_parts.append(f"[Tool Call: {name}]: {json.dumps(args, default=str)}")
        elif t == "tool_result":
            name = ev.get("tool_name", "unknown")
            output = ev.get("output", {})
            output_str = json.dumps(output, default=str)
            if len(output_str) > 2000:
                output_str = output_str[:2000] + "..."
            trace_parts.append(f"[Tool Result: {name}]: {output_str}")
        elif t == "assessment":
            trace_parts.append(f"[Final Assessment]: {ev.get('content', '')}")

    if final_response and not any("[Final Assessment]" in p for p in trace_parts):
        trace_parts.append(f"[Final Assessment]: {final_response}")

    trace_section = f"## Agent Reasoning Trace\n" + "\n\n".join(trace_parts)

    # Ground truth
    gt = case.ground_truth
    gt_section = (
        f"## Ground Truth\n"
        f"**Primary Diagnosis:** {gt.primary_diagnosis}\n"
        f"**ICD Code:** {gt.icd_code}\n"
        f"**Differential Diagnoses:**\n"
    )
    for d in gt.differential:
        diag = d.get("diagnosis", "") if isinstance(d, dict) else str(d)
        likelihood = d.get("likelihood", "") if isinstance(d, dict) else ""
        distinguishing = d.get("key_distinguishing", "") if isinstance(d, dict) else ""
        gt_section += f"  - {diag} ({likelihood}): {distinguishing}\n"

    gt_section += f"\n**Optimal Actions:**\n"
    for a in gt.optimal_actions:
        gt_section += f"  - [{a.category.value}] {a.action}\n"

    gt_section += f"\n**Critical Actions:** {', '.join(gt.critical_actions)}\n"
    gt_section += f"**Contraindicated Actions:** {', '.join(gt.contraindicated_actions)}\n"
    gt_section += f"**Key Reasoning Points:**\n"
    for kp in gt.key_reasoning_points:
        gt_section += f"  - {kp}\n"

    # Case metadata
    meta_section = (
        f"## Case Metadata\n"
        f"**Condition:** {case.condition.value}\n"
        f"**Difficulty:** {case.difficulty.value}\n"
        f"**Encounter Type:** {case.encounter_type.value}\n"
    )

    return f"{case_section}\n{trace_section}\n\n{gt_section}\n{meta_section}"


def _parse_oracle_response(response: str) -> dict:
    """Parse the oracle's JSON response into a dict of scores."""
    try:
        json_str = response
        if "```" in response:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
        elif "{" in response:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = response[start:end]

        data = json.loads(json_str)
        return {
            "diagnostic_accuracy": int(data.get("diagnostic_accuracy", 0)),
            "evidence_identification": int(data.get("evidence_identification", 0)),
            "evidence_integration": int(data.get("evidence_integration", 0)),
            "differential_reasoning": int(data.get("differential_reasoning", 0)),
            "tool_efficiency": int(data.get("tool_efficiency", 0)),
            "clinical_safety": int(data.get("clinical_safety", 0)),
            "red_herring_handling": data.get("red_herring_handling"),  # can be null
            "uncertainty_calibration": int(data.get("uncertainty_calibration", 0)),
            "composite_score": float(data.get("composite_score", 0)),
            "strengths": data.get("strengths", []),
            "weaknesses": data.get("weaknesses", []),
            "critical_errors": data.get("critical_errors", []),
            "justification": data.get("justification", ""),
        }
    except (json.JSONDecodeError, ValueError, KeyError):
        return {
            "diagnostic_accuracy": 0, "evidence_identification": 0,
            "evidence_integration": 0, "differential_reasoning": 0,
            "tool_efficiency": 0, "clinical_safety": 0,
            "red_herring_handling": None, "uncertainty_calibration": 0,
            "composite_score": 0, "strengths": [], "weaknesses": [],
            "critical_errors": [], "justification": f"Failed to parse: {response[:300]}",
        }


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
    elif body.model in MODEL_KEY_TO_HF:
        evaluator_model = MODEL_KEY_TO_HF[body.model]
        evaluator_base_url = VLLM_BASE_URL
        evaluator_api_key = "not-needed"
    else:
        evaluator_model = body.model
        evaluator_base_url = OLLAMA_BASE_URL
        evaluator_api_key = "not-needed"

    return StreamingResponse(
        _stream_evaluation(
            case=case,
            events=body.events,
            final_response=body.final_response,
            tools_called=body.tools_called,
            total_tool_calls=len(body.tools_called),
            evaluator_model=evaluator_model,
            evaluator_base_url=evaluator_base_url,
            evaluator_api_key=evaluator_api_key,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
