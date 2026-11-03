"""Prompt construction shared by inference and SFT.

One transcript codec renders a typed episode into chat messages. The same function builds the
inference request and the SFT example, so the model is trained on exactly the format it is
evaluated with.
"""

from __future__ import annotations

import json
from typing import Any

from neuroagent_schemas import (
    ActionProposed,
    ClinicalEpisode,
    NeuroBenchCase,
    ObservationReceived,
    PluginEvent,
    ToolAction,
)

SUBMIT_NAME = "submit_assessment"
REACT_NAMESPACE = "react.rationale"

POLICY_SYSTEM_PROMPT = """You are a clinical decision-support agent operating in a simulated hospital.
At every turn choose exactly one structured action: order one available tool, or submit the final
assessment. Use only information in the case and returned observations. Prefer the smallest safe,
diagnostically useful work-up. Do not order tests that cannot change management. Submit as soon as
the evidence is sufficient. This system is for research and clinician support, not autonomous care."""

REACT_ADDENDUM = """This is the isolated ReAct ablation. Before the structured action, provide a
brief rationale in the assistant content, then make exactly one function call in the same response
(a tool, or submit_assessment). Never answer in prose alone. Do not reveal hidden chain-of-thought;
state only concise clinical evidence and the purpose of the selected action."""


def format_patient_info(case: NeuroBenchCase) -> str:
    """Render only information available at the start of the encounter."""
    patient = case.patient
    vitals = patient.vitals
    exam = patient.neurological_exam
    history = patient.clinical_history
    parts = [
        f"Patient: {patient.demographics.age}-year-old {patient.demographics.sex}{format_body_size(patient.demographics)}",
        f"Chief complaint: {patient.chief_complaint}",
        f"History of present illness: {patient.history_present_illness}",
    ]
    if history.past_medical_history:
        parts.append(f"Past medical history: {'; '.join(history.past_medical_history)}")
    if history.medications:
        medications = [
            f"{item.drug} {item.dose} {item.frequency} ({item.indication})"
            for item in history.medications
        ]
        parts.append(f"Current medications: {'; '.join(medications)}")
    if history.allergies:
        parts.append(f"Allergies: {', '.join(history.allergies)}")
    if history.family_history:
        parts.append(f"Family history: {'; '.join(history.family_history)}")
    if history.social_history:
        parts.append(
            "Social history: "
            + "; ".join(f"{key}: {value}" for key, value in history.social_history.items())
        )

    exam_parts = [
        f"{label}: {value}"
        for label, value in (
            ("Mental status", exam.mental_status),
            ("Cranial nerves", exam.cranial_nerves),
            ("Motor", exam.motor),
            ("Sensory", exam.sensory),
            ("Reflexes", exam.reflexes),
            ("Coordination", exam.coordination),
            ("Gait", exam.gait),
            ("Additional", exam.additional),
        )
        if value
    ]
    # Every NeuroBench case has a neurological exam; a general-medicine case may carry its whole
    # examination, neurological findings included, as `physical_exam` systems instead.
    if exam_parts:
        parts.append("Neurological examination:\n" + "\n".join(f"  {item}" for item in exam_parts))
    if patient.physical_exam:
        parts.append(
            "Physical examination:\n"
            + "\n".join(f"  {system}: {finding}" for system, finding in patient.physical_exam.items())
        )
    parts.append(format_vitals(vitals))
    return "\n".join(parts)


def format_body_size(demographics: Any) -> str:
    """Height, weight and BMI as recorded; a measure the record left blank is not shown."""
    size = [
        f"{label} {value:g} {unit}".rstrip()
        for label, value, unit in (
            ("height", demographics.height_cm, "cm"),
            ("weight", demographics.weight_kg, "kg"),
            ("BMI", demographics.bmi, ""),
        )
        if value is not None
    ]
    return f", {', '.join(size)}" if size else ""


def format_vitals(vitals: Any) -> str:
    """The vitals line. A vital the record left blank is named as not recorded, never filled in."""
    recorded, missing = [], []
    if vitals.bp_systolic is not None and vitals.bp_diastolic is not None:
        recorded.append(f"BP {vitals.bp_systolic}/{vitals.bp_diastolic} mmHg")
    else:
        missing.append("BP")
    for label, value, unit in (
        ("HR", vitals.hr, " bpm"),
        ("Temp", vitals.temp, "°C"),
        ("RR", vitals.rr, ""),
        ("SpO2", vitals.spo2, "%"),
    ):
        if value is None:
            missing.append(label)
        else:
            recorded.append(f"{label} {value}{unit}")
    line = "Vitals: " + (", ".join(recorded) if recorded else "none recorded")
    if recorded and missing:
        line += f" (not recorded: {', '.join(missing)})"
    return line


def observation_payload(event: ObservationReceived) -> dict[str, Any]:
    return {
        "tool_name": event.tool_name,
        "success": event.success,
        "output": event.output,
        "error_message": event.error_message,
    }


def tool_call(action: ToolAction | Any, call_id: str) -> dict[str, Any]:
    """OpenAI-shaped tool call for either action type.

    Arguments stay a mapping, which is what chat templates render; the LLM client serializes
    them to the JSON string the wire format requires.
    """
    if isinstance(action, ToolAction):
        name, arguments = action.tool_name, action.arguments
    else:
        name, arguments = SUBMIT_NAME, action.model_dump(mode="json", exclude={"type"})
    return {"id": call_id, "type": "function", "function": {"name": name, "arguments": arguments}}


def transcript(
    case: NeuroBenchCase,
    episode: ClinicalEpisode,
    *,
    react: bool = False,
    correction: str | None = None,
) -> list[dict[str, Any]]:
    """Chat messages for the next model request, or the full SFT example.

    Actions are OpenAI tool calls and observations are ``tool`` messages; the tool catalogue
    travels in the request (or the chat template), not in the transcript. Observations recorded
    at turn 0 (the direct baseline) were not ordered by the model and are presented as evidence
    available at the start of the encounter. Rejected outputs are not replayed; the retry
    carries a one-off ``correction`` instead. The ReAct rationale is replayed only in the
    ablation, never in SFT examples.
    """
    system = POLICY_SYSTEM_PROMPT + ("\n\n" + REACT_ADDENDUM if react else "")
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system},
        {"role": "user", "content": format_patient_info(case)},
    ]
    preloaded = [
        observation_payload(event)
        for event in episode.events
        if isinstance(event, ObservationReceived) and event.turn == 0
    ]
    if preloaded:
        messages.append(
            {
                "role": "user",
                "content": "Results already available for this encounter:\n"
                + json.dumps(preloaded, sort_keys=True),
            }
        )
    rationale = {
        event.turn: str(event.payload.get("value", ""))
        for event in episode.events
        if react and isinstance(event, PluginEvent) and event.namespace == REACT_NAMESPACE
    }
    call_index = 0
    for event in episode.events:
        if isinstance(event, ActionProposed):
            call_index += 1
            messages.append(
                {
                    "role": "assistant",
                    "content": rationale.get(event.turn),
                    "tool_calls": [tool_call(event.action, f"call_{call_index}")],
                }
            )
        elif isinstance(event, ObservationReceived) and event.turn > 0:
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": f"call_{call_index}",
                    "content": json.dumps(observation_payload(event), sort_keys=True),
                }
            )
    if correction:
        # Delivered as environment feedback inside the latest observation rather than as a new user
        # turn: Qwen's template re-renders every earlier assistant turn (dropping the empty think
        # block) once a user message follows it, which would make the transcript seen at turn k+1
        # inconsistent with what the model generated from at turn k.
        if messages[-1]["role"] == "tool":
            messages[-1] = {**messages[-1], "content": messages[-1]["content"] + "\n\n" + correction}
        else:
            messages.append({"role": "user", "content": correction})
    return messages
