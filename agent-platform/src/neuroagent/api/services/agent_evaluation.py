"""Agent-output evaluation helpers used by the API route."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import AsyncIterator

from neuroagent_schemas import NeuroBenchCase

from neuroagent.agent.reasoning import AgentTrace
from neuroagent.evaluation.metrics import MetricsCalculator
from neuroagent.llm.client import LLMClient
from neuroagent.llm.prompts import load_prompt

from .sse_bridge import SSEBridge

logger = logging.getLogger(__name__)

_oracle_prompt_cache: str | None = None


def _get_oracle_system_prompt() -> str:
    global _oracle_prompt_cache
    if _oracle_prompt_cache is None:
        _oracle_prompt_cache = load_prompt("llm_judge.txt")
    return _oracle_prompt_cache


async def stream_evaluation_events(
    case: NeuroBenchCase,
    events: list[dict],
    final_response: str,
    tools_called: list[str],
    total_tool_calls: int,
    evaluator_model: str,
    evaluator_base_url: str,
    evaluator_api_key: str,
) -> AsyncIterator[dict]:
    """Run rule-based metrics plus LLM judge and yield API event dicts."""
    # Thread-safe bridge: the evaluator runs in a worker thread, and
    # asyncio.Queue must only be touched from the event loop thread.
    bridge = SSEBridge()

    def _run_sync() -> None:
        try:
            trace = AgentTrace(
                case_id=case.case_id,
                turns=[],
                final_response=final_response,
                total_tool_calls=total_tool_calls,
                tools_called=tools_called,
            )
            metrics = MetricsCalculator().compute_all(trace, case.ground_truth)

            bridge.put_from_thread({
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

            bridge.put_from_thread({"type": "judge_started"})

            llm = LLMClient(
                base_url=evaluator_base_url,
                api_key=evaluator_api_key,
                model=evaluator_model,
                temperature=0.0,
                max_tokens=8192,
                presence_penalty=0.0,
            )
            messages = [
                {"role": "system", "content": _get_oracle_system_prompt()},
                {
                    "role": "user",
                    "content": _build_oracle_user_prompt(case, events, final_response),
                },
            ]

            full_content: list[str] = []
            for ev in llm.chat_stream(messages=messages, tools=None):
                if bridge.client_disconnected:
                    # Nothing to persist here — stop paying for judge tokens.
                    logger.info("Evaluation client disconnected; stopping judge stream")
                    return
                if ev["type"] == "content_delta":
                    full_content.append(ev["delta"])
                    bridge.put_from_thread({"type": "judge_delta", "delta": ev["delta"]})

            bridge.put_from_thread({
                "type": "judge_complete",
                **_parse_oracle_response("".join(full_content)),
            })
        except Exception as exc:
            bridge.put_from_thread({"type": "eval_error", "message": str(exc)})
        finally:
            bridge.put_from_thread(None)

    loop = asyncio.get_running_loop()
    run_future = loop.run_in_executor(None, _run_sync)
    run_future.add_done_callback(_log_worker_failure)

    completed = False
    try:
        async for event in bridge.events():
            yield event
        completed = True
    finally:
        if not completed:
            # Client disconnected — stop buffering judge output.
            bridge.mark_disconnected()
            logger.info(
                "SSE client disconnected during evaluation of case %s", case.case_id
            )


def _log_worker_failure(future: asyncio.Future) -> None:
    """Surface unexpected executor-task failures instead of losing them."""
    if future.cancelled():
        return
    exc = future.exception()
    if exc is not None:
        logger.error("Evaluation worker thread failed", exc_info=exc)


def _build_oracle_user_prompt(
    case: NeuroBenchCase,
    events: list[dict],
    final_response: str,
) -> str:
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
        f"**Vitals:** BP {p.vitals.bp_systolic}/{p.vitals.bp_diastolic}, "
        f"HR {p.vitals.hr}, Temp {p.vitals.temp}°C, RR {p.vitals.rr}, "
        f"SpO2 {p.vitals.spo2}%\n"
    )

    trace_parts: list[str] = []
    for ev in events:
        event_type = ev.get("type", "")
        if event_type == "thinking":
            content = ev.get("content", "")
            think = ev.get("think_content", "")
            if content:
                trace_parts.append(f"[Agent Reasoning]: {content}")
            if think:
                trace_parts.append(f"[Internal Thinking]: {think[:2000]}")
        elif event_type == "tool_call":
            name = ev.get("tool_name", "unknown")
            args = ev.get("arguments", {})
            trace_parts.append(f"[Tool Call: {name}]: {json.dumps(args, default=str)}")
        elif event_type == "tool_result":
            name = ev.get("tool_name", "unknown")
            output = ev.get("output", {})
            output_str = json.dumps(output, default=str)
            if len(output_str) > 2000:
                output_str = output_str[:2000] + "..."
            trace_parts.append(f"[Tool Result: {name}]: {output_str}")
        elif event_type == "assessment":
            trace_parts.append(f"[Final Assessment]: {ev.get('content', '')}")

    if final_response and not any("[Final Assessment]" in part for part in trace_parts):
        trace_parts.append(f"[Final Assessment]: {final_response}")

    gt = case.ground_truth
    gt_section = (
        f"## Ground Truth\n"
        f"**Primary Diagnosis:** {gt.primary_diagnosis}\n"
        f"**ICD Code:** {gt.icd_code}\n"
        f"**Differential Diagnoses:**\n"
    )
    for d in gt.differential:
        likelihood = d.likelihood.value if hasattr(d.likelihood, "value") else str(d.likelihood)
        gt_section += f"  - {d.diagnosis} ({likelihood}): {d.key_features}\n"

    gt_section += "\n**Optimal Actions:**\n"
    for action in gt.optimal_actions:
        gt_section += f"  - [{action.category.value}] {action.action}\n"

    gt_section += f"\n**Critical Actions:** {', '.join(gt.critical_actions)}\n"
    gt_section += f"**Contraindicated Actions:** {', '.join(gt.contraindicated_actions)}\n"
    gt_section += "**Key Reasoning Points:**\n"
    for point in gt.key_reasoning_points:
        gt_section += f"  - {point}\n"

    meta_section = (
        f"## Case Metadata\n"
        f"**Condition:** {case.condition.value}\n"
        f"**Difficulty:** {case.difficulty.value}\n"
        f"**Encounter Type:** {case.encounter_type.value}\n"
    )

    trace_section = "## Agent Reasoning Trace\n" + "\n\n".join(trace_parts)
    return f"{case_section}\n{trace_section}\n\n{gt_section}\n{meta_section}"


def _parse_oracle_response(response: str) -> dict:
    try:
        json_str = response
        if "```" in response or "{" in response:
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
            "red_herring_handling": data.get("red_herring_handling"),
            "uncertainty_calibration": int(data.get("uncertainty_calibration", 0)),
            "composite_score": float(data.get("composite_score", 0)),
            "strengths": data.get("strengths", []),
            "weaknesses": data.get("weaknesses", []),
            "critical_errors": data.get("critical_errors", []),
            "justification": data.get("justification", ""),
        }
    except (json.JSONDecodeError, ValueError, KeyError):
        return {
            "diagnostic_accuracy": 0,
            "evidence_identification": 0,
            "evidence_integration": 0,
            "differential_reasoning": 0,
            "tool_efficiency": 0,
            "clinical_safety": 0,
            "red_herring_handling": None,
            "uncertainty_calibration": 0,
            "composite_score": 0,
            "strengths": [],
            "weaknesses": [],
            "critical_errors": [],
            "justification": f"Failed to parse: {response[:300]}",
        }
