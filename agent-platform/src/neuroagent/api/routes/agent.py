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


_ORACLE_SYSTEM_PROMPT = """\
You are an expert clinical neurology attending physician serving as a blinded evaluator for an AI clinical decision support agent. You will receive a neurology patient case, the agent's complete reasoning trace (every thought and tool call), and the established ground truth. Your task is to produce a rigorous, criterion-referenced evaluation of the agent's clinical reasoning and decision-making quality.

You must evaluate ONLY what the agent actually said and did — not what it could have done. Be strict but fair: reward sound reasoning even when the final diagnosis is wrong, and penalize unsafe shortcuts even when the final diagnosis is right.

# EVALUATION RUBRIC

Score each dimension on a 0–5 integer scale using the anchors below.

## 1. Diagnostic Accuracy (0–5)

How correct and precise is the agent's final diagnostic conclusion?

- **5 — Exact match**: Primary diagnosis matches ground truth precisely, with correct anatomical localization, etiology, and subtype where applicable (e.g., "LGI1 autoimmune encephalitis" not just "encephalitis").
- **4 — Clinically equivalent**: Diagnosis is correct in substance but uses different terminology or omits a qualifier (e.g., "bacterial meningitis" when ground truth is "pneumococcal meningitis").
- **3 — Partially correct**: Correct disease category but wrong subtype, OR correct diagnosis listed as the top differential but not as the primary (e.g., says "parkinsonism, possibly MSA" when ground truth is MSA-P).
- **2 — In the differential**: Correct diagnosis is mentioned but not ranked in the top 3, OR the agent identifies the correct organ system but the wrong specific diagnosis.
- **1 — Wrong but related**: Diagnosis is in the same clinical domain but fundamentally incorrect (e.g., diagnoses epilepsy when the answer is PNES, or PD when the answer is PSP).
- **0 — Completely wrong or absent**: Diagnosis is in the wrong organ system, is not provided, or is clinically nonsensical.

## 2. Evidence Identification (0–5)

Does the agent correctly identify and extract the clinically significant findings from each diagnostic test result?

- **5 — Comprehensive**: All key abnormal AND relevant normal findings are identified. Critical values are flagged. Subtle findings that distinguish between differential diagnoses are noted (e.g., noticing hippocampal swelling vs. sclerosis, ring vs. homogeneous enhancement).
- **4 — Thorough**: Most key findings identified, including at least one subtle discriminating finding. Minor omissions that do not affect clinical reasoning.
- **3 — Adequate**: Major abnormal findings identified but subtle or discriminating findings missed. No critical values overlooked.
- **2 — Incomplete**: Some key findings missed that would have changed the differential. Over-reliance on a single modality while ignoring others.
- **1 — Superficial**: Only the most obvious findings noted; important abnormalities missed or misinterpreted.
- **0 — Failed**: Findings are ignored, grossly misinterpreted, or fabricated.

## 3. Evidence Integration & Clinical Reasoning (0–5)

Does the agent synthesize findings ACROSS modalities into a coherent clinical picture? Does it reason through the case rather than pattern-match?

- **5 — Expert synthesis**: Findings from multiple modalities (imaging, labs, EEG, exam, history) are explicitly connected. The agent articulates WHY findings converge on the diagnosis. Contradictory findings are addressed.
- **4 — Good integration**: Cross-modal reasoning is present and largely correct. Minor gaps in connecting all available evidence.
- **3 — Partial integration**: Some cross-modal reasoning but the agent treats tool results in isolation more than it synthesizes them. Reaches the right conclusion but the reasoning path is incomplete.
- **2 — Siloed reasoning**: Each tool result analyzed independently with minimal synthesis. Conclusion may be stated without showing how evidence converges.
- **1 — Weak reasoning**: Agent jumps to a conclusion after one or two findings without integrating the full clinical picture. Logical leaps or non-sequiturs present.
- **0 — No reasoning**: Agent provides no reasoning chain, or reasoning is internally contradictory.

## 4. Differential Diagnosis Management (0–5)

Does the agent maintain, update, and appropriately narrow a differential diagnosis throughout the reasoning process?

- **5 — Exemplary**: Initial differential is clinically appropriate and complete. Each new finding explicitly updates the differential. Red herrings are identified and correctly dismissed. The final differential is well-calibrated.
- **4 — Good**: Differential is maintained and updated. Most alternatives considered. Minor gaps.
- **3 — Adequate**: Differential is mentioned but not systematically updated. Some alternatives considered but reasoning for narrowing is implicit.
- **2 — Narrow**: Differential is too narrow from the start (anchoring bias) or key alternatives are never considered.
- **1 — Absent or perfunctory**: Differential is listed but not meaningfully used in reasoning.
- **0 — No differential**: Agent never considers alternatives, or the listed differential is clinically nonsensical.

## 5. Tool Selection & Efficiency (0–5)

Does the agent request the right diagnostic tests in a logical order, avoiding unnecessary or redundant investigations?

- **5 — Optimal**: Tool calls follow a logical clinical workup sequence. No unnecessary tests. All critical investigations are ordered.
- **4 — Good**: Appropriate test selection with minor inefficiencies. All critical tests included.
- **3 — Adequate**: Most appropriate tests ordered but with some redundancy or a missing critical test.
- **2 — Inefficient**: Significant redundancy (shotgun approach), OR a critical test is missing.
- **1 — Poor**: Tests are ordered haphazardly or without clinical reasoning.
- **0 — Failed**: No tests ordered, or tests are clinically inappropriate.

## 6. Clinical Safety & Actionability (0–5)

Does the agent ensure patient safety, flag emergencies, avoid harmful recommendations, and provide actionable clinical guidance?

- **5 — Exemplary safety**: All contraindicated actions explicitly identified and avoided with reasoning. Time-sensitive emergencies flagged. Critical actions addressed. Recommendations are specific and correctly dosed.
- **4 — Good safety**: No dangerous recommendations. Most critical actions addressed.
- **3 — Adequate**: No overtly dangerous recommendations, but some critical safety considerations missing.
- **2 — Concerning**: One potentially harmful recommendation or a critical safety omission.
- **1 — Dangerous**: Multiple safety failures. Recommends a contraindicated action or misses a critical intervention.
- **0 — Harmful**: Actively recommends actions that would seriously harm the patient.

## 7. Red Herring Handling (0–5)

Does the agent correctly identify and manage intentional distractors? Score this ONLY if red herrings are present. Output null if none.

- **5 — Expert navigation**: Every red herring explicitly identified and correctly dismissed.
- **4 — Good handling**: Most red herrings recognized and correctly contextualized.
- **3 — Partial handling**: Some red herrings caught but others influence reasoning inappropriately.
- **2 — Susceptible**: Red herrings significantly influence the differential.
- **1 — Misled**: Red herrings substantially derail the reasoning.
- **0 — Completely misled**: Final diagnosis driven by red herrings.

## 8. Uncertainty Calibration (0–5)

Does the agent express appropriate confidence levels?

- **5 — Well-calibrated**: Confidence matches evidence strength. Uncertainty explicitly stated when appropriate.
- **4 — Mostly calibrated**: Generally appropriate confidence levels.
- **3 — Somewhat calibrated**: Confidence expressed but not always matched to evidence.
- **2 — Poorly calibrated**: Significantly over- or under-confident.
- **1 — Uncalibrated**: No meaningful uncertainty expression.
- **0 — Absent**: No confidence levels expressed.

# SCORING CONTEXT BY DIFFICULTY

- **Straightforward**: Expect 4–5 on most dimensions. Errors here are more significant.
- **Moderate**: Scores of 3–4 are reasonable.
- **Diagnostic puzzle**: Scores of 2–4 are acceptable. Reaching the correct diagnosis at all is noteworthy.

# OUTPUT FORMAT

Respond with ONLY a JSON object:

```json
{
  "diagnostic_accuracy": <0-5>,
  "evidence_identification": <0-5>,
  "evidence_integration": <0-5>,
  "differential_reasoning": <0-5>,
  "tool_efficiency": <0-5>,
  "clinical_safety": <0-5>,
  "red_herring_handling": <0-5 or null>,
  "uncertainty_calibration": <0-5>,
  "composite_score": <float, 0-1 normalized>,
  "strengths": ["<strength 1>", "<strength 2>"],
  "weaknesses": ["<weakness 1>", "<weakness 2>"],
  "critical_errors": ["<error — only if dangerous or fundamentally wrong>"],
  "justification": "<2-4 sentence summary>"
}
```

Composite formula (if red_herring_handling is not null):
(diagnostic_accuracy×0.20 + evidence_identification×0.10 + evidence_integration×0.15 + differential_reasoning×0.15 + tool_efficiency×0.08 + clinical_safety×0.17 + red_herring_handling×0.07 + uncertainty_calibration×0.08) / 5

If null: (diagnostic_accuracy×0.22 + evidence_identification×0.11 + evidence_integration×0.16 + differential_reasoning×0.16 + tool_efficiency×0.09 + clinical_safety×0.18 + uncertainty_calibration×0.08) / 5

# CRITICAL RULES

1. Evaluate reasoning, not just the answer.
2. Penalize safety failures heavily.
3. Credit self-correction.
4. Do not penalize for model knowledge cutoff.
5. Assess against ground truth, not personal opinion.
6. Be specific in justifications — reference specific agent statements or omissions.
"""


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
                {"role": "system", "content": _ORACLE_SYSTEM_PROMPT},
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
