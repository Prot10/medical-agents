"""Prompt construction from typed cases and append-only episode events."""

from __future__ import annotations

import json
from typing import Any

from neuroagent_schemas import (
    ActionProposed,
    ActionRejected,
    ClinicalEpisode,
    NeuroBenchCase,
    ObservationReceived,
)


POLICY_SYSTEM_PROMPT = """You are a clinical decision-support agent operating in a simulated hospital.
At every turn choose exactly one structured action: order one available tool, or submit the final
assessment. Use only information in the case and returned observations. Prefer the smallest safe,
diagnostically useful work-up. Do not order tests that cannot change management. Submit as soon as
the evidence is sufficient. This system is for research and clinician support, not autonomous care."""

REACT_ADDENDUM = """This is the isolated ReAct ablation. Before the structured action, provide a
brief rationale in the assistant content. Do not reveal hidden chain-of-thought; state only concise
clinical evidence and the purpose of the selected action."""


def format_patient_info(case: NeuroBenchCase) -> str:
    """Render only information available at the start of the encounter."""
    patient = case.patient
    vitals = patient.vitals
    exam = patient.neurological_exam
    parts = [
        f"Patient: {patient.demographics.age}-year-old {patient.demographics.sex}",
        f"Chief complaint: {patient.chief_complaint}",
        f"History of present illness: {patient.history_present_illness}",
    ]
    history = patient.clinical_history
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

    exam_parts = []
    for label, value in (
        ("Mental status", exam.mental_status),
        ("Cranial nerves", exam.cranial_nerves),
        ("Motor", exam.motor),
        ("Sensory", exam.sensory),
        ("Reflexes", exam.reflexes),
        ("Coordination", exam.coordination),
        ("Gait", exam.gait),
        ("Additional", exam.additional),
    ):
        if value:
            exam_parts.append(f"{label}: {value}")
    parts.append("Neurological examination:\n" + "\n".join(f"  {item}" for item in exam_parts))
    parts.append(
        f"Vitals: BP {vitals.bp_systolic}/{vitals.bp_diastolic} mmHg, "
        f"HR {vitals.hr} bpm, Temp {vitals.temp}°C, RR {vitals.rr}, SpO2 {vitals.spo2}%"
    )
    return "\n".join(parts)


def episode_messages(
    case: NeuroBenchCase,
    episode: ClinicalEpisode,
    *,
    react: bool = False,
    correction: str | None = None,
) -> list[dict[str, Any]]:
    """Build a provider-neutral transcript without persisting free-form reasoning."""
    system = POLICY_SYSTEM_PROMPT + ("\n\n" + REACT_ADDENDUM if react else "")
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system},
        {"role": "user", "content": format_patient_info(case)},
    ]
    for event in episode.events:
        if isinstance(event, ActionProposed):
            messages.append(
                {
                    "role": "assistant",
                    "content": json.dumps(event.action.model_dump(mode="json"), sort_keys=True),
                }
            )
        elif isinstance(event, ObservationReceived):
            payload = {
                "tool_name": event.tool_name,
                "success": event.success,
                "output": event.output,
                "error_message": event.error_message,
            }
            messages.append({"role": "user", "content": "Observation: " + json.dumps(payload)})
        elif isinstance(event, ActionRejected):
            messages.append(
                {
                    "role": "user",
                    "content": (
                        "The previous response was invalid: "
                        + event.reason
                        + ". Return exactly one valid structured action."
                    ),
                }
            )
    if correction:
        messages.append({"role": "user", "content": correction})
    return messages
