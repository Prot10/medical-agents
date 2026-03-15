"""LLM-as-judge for reasoning quality assessment."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from neuroagent_schemas import GroundTruth, NeuroBenchCase

from ..agent.reasoning import AgentTrace
from ..llm.client import LLMClient

# Load the judge system prompt from file
_PROMPT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "config" / "system_prompts"


def _load_judge_prompt() -> str:
    prompt_path = _PROMPT_DIR / "llm_judge.txt"
    if prompt_path.exists():
        return prompt_path.read_text()
    raise FileNotFoundError(f"Judge prompt not found at {prompt_path}")


@dataclass
class ReasoningScore:
    """Rubric-based reasoning quality scores (8 dimensions)."""

    diagnostic_accuracy: int = 0  # 0-5
    evidence_identification: int = 0  # 0-5
    evidence_integration: int = 0  # 0-5
    differential_reasoning: int = 0  # 0-5
    tool_efficiency: int = 0  # 0-5
    clinical_safety: int = 0  # 0-5
    red_herring_handling: int | None = None  # 0-5 or None if no red herrings
    uncertainty_calibration: int = 0  # 0-5
    composite_score: float = 0.0  # 0-1 weighted mean
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    critical_errors: list[str] = field(default_factory=list)
    justification: str = ""

    # Keep backward-compatible alias
    @property
    def overall(self) -> float:
        return self.composite_score

    def compute_composite(self) -> float:
        """Compute the weighted composite score (0-1 scale)."""
        if self.red_herring_handling is not None:
            raw = (
                self.diagnostic_accuracy * 0.20
                + self.evidence_identification * 0.10
                + self.evidence_integration * 0.15
                + self.differential_reasoning * 0.15
                + self.tool_efficiency * 0.08
                + self.clinical_safety * 0.17
                + self.red_herring_handling * 0.07
                + self.uncertainty_calibration * 0.08
            )
        else:
            raw = (
                self.diagnostic_accuracy * 0.22
                + self.evidence_identification * 0.11
                + self.evidence_integration * 0.16
                + self.differential_reasoning * 0.16
                + self.tool_efficiency * 0.09
                + self.clinical_safety * 0.18
                + self.uncertainty_calibration * 0.08
            )
        self.composite_score = round(raw / 5.0, 4)
        return self.composite_score


class LLMJudge:
    """Use a strong LLM to assess the quality of agent reasoning."""

    def __init__(self, llm: LLMClient):
        self.llm = llm
        self._system_prompt = _load_judge_prompt()

    def judge(
        self,
        trace: AgentTrace,
        case: NeuroBenchCase,
    ) -> ReasoningScore:
        """Rate the agent's reasoning chain on the full 8-dimension rubric.

        Args:
            trace: Agent's execution trace.
            case: The full NeuroBench case (patient info + ground truth).

        Returns:
            ReasoningScore with rubric scores, strengths/weaknesses, and justification.
        """
        user_prompt = self._build_user_prompt(trace, case)

        messages = [
            {"role": "system", "content": self._system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = self.llm.chat(messages=messages, tools=None, temperature=0.0)
        return self._parse_response(response.content or "", case.ground_truth)

    # Keep backward-compatible signature
    def judge_legacy(
        self,
        trace: AgentTrace,
        ground_truth_diagnosis: str,
        case_description: str = "",
    ) -> ReasoningScore:
        """Legacy interface — prefer judge() with full NeuroBenchCase."""
        trace_text = self._format_trace(trace)
        user_prompt = (
            f"## Case Presentation\n{case_description}\n\n"
            f"## Ground Truth\n### Correct Diagnosis\n{ground_truth_diagnosis}\n\n"
            f"## Agent Reasoning Trace\n{trace_text}\n\n"
            "Evaluate the agent's reasoning using the rubric."
        )

        messages = [
            {"role": "system", "content": self._system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = self.llm.chat(messages=messages, tools=None, temperature=0.0)
        return self._parse_response(response.content or "")

    def _build_user_prompt(self, trace: AgentTrace, case: NeuroBenchCase) -> str:
        """Build the complete user prompt with case, trace, and ground truth."""
        parts: list[str] = []

        # --- Case metadata ---
        parts.append("## Case Metadata")
        parts.append(f"- **Case ID**: {case.case_id}")
        parts.append(f"- **Condition**: {case.condition.value}")
        parts.append(f"- **Difficulty**: {case.difficulty.value}")
        parts.append(f"- **Encounter type**: {case.encounter_type.value}")
        parts.append("")

        # --- Case presentation (what the agent received) ---
        parts.append("## Case Presentation")
        p = case.patient
        parts.append(
            f"**Patient**: {p.demographics.age}-year-old {p.demographics.sex}, "
            f"{p.demographics.ethnicity}, BMI {p.demographics.bmi}"
        )
        parts.append(f"**Chief complaint**: {p.chief_complaint}")
        parts.append(f"**HPI**: {p.history_present_illness}")

        if p.clinical_history.past_medical_history:
            parts.append(f"**PMH**: {'; '.join(p.clinical_history.past_medical_history)}")
        if p.clinical_history.medications:
            med_strs = [f"{m.drug} {m.dose} {m.frequency}" for m in p.clinical_history.medications]
            parts.append(f"**Medications**: {'; '.join(med_strs)}")
        if p.clinical_history.allergies:
            parts.append(f"**Allergies**: {', '.join(p.clinical_history.allergies)}")

        exam = p.neurological_exam
        parts.append(f"**Neuro exam**: Mental status: {exam.mental_status}. "
                      f"Cranial nerves: {exam.cranial_nerves}. Motor: {exam.motor}. "
                      f"Sensory: {exam.sensory}. Reflexes: {exam.reflexes}. "
                      f"Coordination: {exam.coordination}. Gait: {exam.gait}.")
        if exam.additional:
            parts.append(f"**Additional exam**: {exam.additional}")

        v = p.vitals
        parts.append(
            f"**Vitals**: BP {v.bp_systolic}/{v.bp_diastolic}, HR {v.hr}, "
            f"Temp {v.temp}°C, RR {v.rr}, SpO2 {v.spo2}%"
        )
        parts.append("")

        # --- Agent reasoning trace ---
        parts.append("## Agent Reasoning Trace")
        parts.append(self._format_trace(trace))
        parts.append("")

        # --- Ground truth ---
        parts.append("## Ground Truth")
        gt = case.ground_truth
        parts.append(f"**Primary diagnosis**: {gt.primary_diagnosis}")
        parts.append(f"**ICD code**: {gt.icd_code}")

        if gt.differential:
            parts.append("**Differential diagnoses**:")
            for d in gt.differential:
                parts.append(
                    f"  - {d.get('diagnosis', '')} ({d.get('likelihood', '')}): "
                    f"{d.get('key_distinguishing', d.get('key_features', ''))}"
                )

        if gt.critical_actions:
            parts.append(f"**Critical actions (MUST do)**: {'; '.join(gt.critical_actions)}")
        if gt.contraindicated_actions:
            parts.append(f"**Contraindicated actions (MUST NOT do)**: {'; '.join(gt.contraindicated_actions)}")
        if gt.key_reasoning_points:
            parts.append("**Key reasoning points**:")
            for kp in gt.key_reasoning_points:
                parts.append(f"  - {kp}")

        if gt.red_herrings:
            parts.append("**Intentional red herrings**:")
            for rh in gt.red_herrings:
                parts.append(
                    f"  - **{rh.data_point}** (in {rh.location}): "
                    f"intended to {rh.intended_effect}. "
                    f"Correct interpretation: {rh.correct_interpretation}"
                )
        parts.append("")

        parts.append("Evaluate the agent's reasoning using the rubric.")
        return "\n".join(parts)

    def _format_trace(self, trace: AgentTrace) -> str:
        """Format trace for judge evaluation."""
        parts = []
        for i, turn in enumerate(trace.turns):
            if turn.role == "assistant" and turn.content:
                parts.append(f"**[Turn {turn.turn_number} — Agent Reasoning]**:\n{turn.content}")
            if turn.tool_calls:
                for tc in turn.tool_calls:
                    tool_name = tc.get("function", {}).get("name", str(tc)) if isinstance(tc, dict) else str(tc)
                    tool_args = tc.get("function", {}).get("arguments", "") if isinstance(tc, dict) else ""
                    parts.append(f"**[Tool Call]**: `{tool_name}`({tool_args})")
            if turn.tool_results:
                for tr in turn.tool_results:
                    tr_str = json.dumps(tr, default=str)
                    if len(tr_str) > 2000:
                        tr_str = tr_str[:2000] + "... [truncated]"
                    parts.append(f"**[Tool Result]**:\n```json\n{tr_str}\n```")

        if trace.final_response:
            parts.append(f"**[Final Assessment]**:\n{trace.final_response}")

        return "\n\n".join(parts)

    def _parse_response(
        self, response: str, ground_truth: GroundTruth | None = None
    ) -> ReasoningScore:
        """Parse the judge's JSON response into a ReasoningScore."""
        try:
            # Extract JSON from response (handle markdown code blocks)
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

            rh_score = data.get("red_herring_handling")
            if rh_score is not None:
                rh_score = int(rh_score)

            score = ReasoningScore(
                diagnostic_accuracy=int(data.get("diagnostic_accuracy", 0)),
                evidence_identification=int(data.get("evidence_identification", 0)),
                evidence_integration=int(data.get("evidence_integration", 0)),
                differential_reasoning=int(data.get("differential_reasoning", 0)),
                tool_efficiency=int(data.get("tool_efficiency", 0)),
                clinical_safety=int(data.get("clinical_safety", 0)),
                red_herring_handling=rh_score,
                uncertainty_calibration=int(data.get("uncertainty_calibration", 0)),
                strengths=data.get("strengths", []),
                weaknesses=data.get("weaknesses", []),
                critical_errors=data.get("critical_errors", []),
                justification=data.get("justification", ""),
            )

            # Use the judge's composite if provided, otherwise compute
            if "composite_score" in data and data["composite_score"] is not None:
                score.composite_score = float(data["composite_score"])
            else:
                score.compute_composite()

            return score
        except (json.JSONDecodeError, ValueError, KeyError):
            return ReasoningScore(
                justification=f"Failed to parse judge response: {response[:300]}"
            )
