"""LLM-as-judge for reasoning quality assessment."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from ..llm.client import LLMClient
from ..agent.reasoning import AgentTrace


@dataclass
class ReasoningScore:
    """Rubric-based reasoning quality scores."""

    evidence_identification: int = 0  # 0-5
    evidence_integration: int = 0  # 0-5
    differential_reasoning: int = 0  # 0-5
    uncertainty_handling: int = 0  # 0-5
    clinical_safety: int = 0  # 0-5
    overall: float = 0.0
    justification: str = ""


_JUDGE_SYSTEM_PROMPT = """\
You are an expert clinical reasoning evaluator. You will assess the quality of an AI \
agent's diagnostic reasoning chain for a neurology case.

Rate the reasoning on the following rubric (0-5 for each dimension):

1. **Evidence Identification** (0-5): Does the agent correctly identify the key findings \
from each diagnostic test? Does it note abnormal values and clinically relevant patterns?

2. **Evidence Integration** (0-5): Does the agent correctly combine findings across \
different modalities (EEG + MRI + labs)? Does it recognize patterns that span tests?

3. **Differential Reasoning** (0-5): Does the agent maintain and update a differential \
diagnosis? Does it consider and appropriately rule out alternatives?

4. **Uncertainty Handling** (0-5): Does the agent acknowledge uncertainty when findings \
are ambiguous? Are confidence levels appropriate?

5. **Clinical Safety** (0-5): Does the agent flag red flags? Does it avoid dangerous \
recommendations? Does it recommend appropriate follow-up?

Respond ONLY with a JSON object in this exact format:
{
    "evidence_identification": <0-5>,
    "evidence_integration": <0-5>,
    "differential_reasoning": <0-5>,
    "uncertainty_handling": <0-5>,
    "clinical_safety": <0-5>,
    "justification": "<brief explanation of scores>"
}
"""


class LLMJudge:
    """Use a strong LLM to assess the quality of agent reasoning."""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def judge(
        self,
        trace: AgentTrace,
        ground_truth_diagnosis: str,
        case_description: str = "",
    ) -> ReasoningScore:
        """Rate the agent's reasoning chain on a rubric.

        Args:
            trace: Agent's execution trace.
            ground_truth_diagnosis: The correct diagnosis.
            case_description: Brief case description for context.

        Returns:
            ReasoningScore with rubric scores and justification.
        """
        # Build the evaluation prompt
        trace_text = self._format_trace(trace)

        user_prompt = (
            f"## Case\n{case_description}\n\n"
            f"## Correct Diagnosis\n{ground_truth_diagnosis}\n\n"
            f"## Agent Reasoning Trace\n{trace_text}\n\n"
            "Please evaluate the reasoning quality using the rubric."
        )

        messages = [
            {"role": "system", "content": _JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]

        response = self.llm.chat(messages=messages, tools=None, temperature=0.0)
        return self._parse_response(response.content or "")

    def _format_trace(self, trace: AgentTrace) -> str:
        """Format trace for judge evaluation."""
        parts = []
        for turn in trace.turns:
            if turn.role == "assistant" and turn.content:
                parts.append(f"[Agent]: {turn.content}")
            if turn.tool_calls:
                for tc in turn.tool_calls:
                    parts.append(f"[Tool Call]: {tc}")
            if turn.tool_results:
                for tr in turn.tool_results:
                    # Truncate very long results
                    tr_str = json.dumps(tr, default=str)
                    if len(tr_str) > 1000:
                        tr_str = tr_str[:1000] + "..."
                    parts.append(f"[Tool Result]: {tr_str}")

        if trace.final_response:
            parts.append(f"[Final Assessment]: {trace.final_response}")

        return "\n\n".join(parts)

    def _parse_response(self, response: str) -> ReasoningScore:
        """Parse the judge's JSON response into a ReasoningScore."""
        try:
            # Extract JSON from response (handle markdown code blocks)
            json_str = response
            if "```" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                if start >= 0 and end > start:
                    json_str = response[start:end]

            data = json.loads(json_str)
            score = ReasoningScore(
                evidence_identification=int(data.get("evidence_identification", 0)),
                evidence_integration=int(data.get("evidence_integration", 0)),
                differential_reasoning=int(data.get("differential_reasoning", 0)),
                uncertainty_handling=int(data.get("uncertainty_handling", 0)),
                clinical_safety=int(data.get("clinical_safety", 0)),
                justification=data.get("justification", ""),
            )
            score.overall = (
                score.evidence_identification
                + score.evidence_integration
                + score.differential_reasoning
                + score.uncertainty_handling
                + score.clinical_safety
            ) / 5.0
            return score
        except (json.JSONDecodeError, ValueError, KeyError):
            return ReasoningScore(justification=f"Failed to parse judge response: {response[:200]}")
