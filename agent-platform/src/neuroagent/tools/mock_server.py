from __future__ import annotations
from neuroagent_schemas import (
    NeuroBenchCase, EEGReport, MRIReport, ECGReport, LabResults, CSFResults,
    LiteratureSearchResult, DrugInteractionResult,
    CTReport, EchoReport, CardiacMonitoringReport,
    AdvancedImagingReport, SpecializedTestReport,
)
from .base import ToolCall, ToolResult
from typing import Any
from pydantic import BaseModel


class MockServer:
    """Serves pre-generated tool outputs from a NeuroBenchCase."""

    def __init__(self, case: NeuroBenchCase):
        self.case = case
        self.call_log: list[ToolCall] = []

    def get_output(self, tool_name: str, parameters: dict[str, Any]) -> ToolResult:
        self.call_log.append(ToolCall(tool_name=tool_name, parameters=parameters))

        # Check initial tool outputs
        output = self._match_initial_output(tool_name, parameters)
        if output is not None:
            return ToolResult(
                tool_name=tool_name, success=True,
                output=output.model_dump() if isinstance(output, BaseModel) else output,
            )

        # Specialist consultation: synthesize from ground truth (returns ToolResult directly)
        if tool_name == "consult_medical_specialist":
            return self._synthesize_specialist_opinion(parameters)

        # Check follow-up outputs
        output = self._match_followup_output(tool_name, parameters)
        if output is not None:
            return ToolResult(
                tool_name=tool_name, success=True,
                output=output.model_dump() if isinstance(output, BaseModel) else output,
            )

        return ToolResult(
            tool_name=tool_name, success=False, output=None,
            error_message=(
                f"No {tool_name} data available for this patient. "
                f"Consider whether this test is appropriate."
            ),
        )

    def _match_initial_output(self, tool_name: str, parameters: dict[str, Any]) -> BaseModel | None:
        mapping = {
            "analyze_eeg": self.case.initial_tool_outputs.eeg,
            "analyze_brain_mri": self.case.initial_tool_outputs.mri,
            "analyze_ecg": self.case.initial_tool_outputs.ecg,
            "interpret_labs": self.case.initial_tool_outputs.labs,
            "analyze_csf": self.case.initial_tool_outputs.csf,
            "order_ct_scan": self.case.initial_tool_outputs.ct,
            "order_echocardiogram": self.case.initial_tool_outputs.echo,
            "order_cardiac_monitoring": self.case.initial_tool_outputs.cardiac_monitoring,
            "order_advanced_imaging": self.case.initial_tool_outputs.advanced_imaging,
            "order_specialized_test": self.case.initial_tool_outputs.specialized_test,
        }

        # Direct mapping for diagnostic tools
        if tool_name in mapping:
            return mapping[tool_name]

        # Literature search: match by query parameter
        if tool_name == "search_medical_literature" and self.case.initial_tool_outputs.literature_search:
            query = parameters.get("query", "")
            # Try exact match first, then return first available
            if query in self.case.initial_tool_outputs.literature_search:
                return self.case.initial_tool_outputs.literature_search[query]
            results = list(self.case.initial_tool_outputs.literature_search.values())
            return results[0] if results else None

        # Drug interaction: match by drug parameter
        if tool_name == "check_drug_interactions" and self.case.initial_tool_outputs.drug_interactions:
            drug = parameters.get("drug", "")
            if drug in self.case.initial_tool_outputs.drug_interactions:
                return self.case.initial_tool_outputs.drug_interactions[drug]
            results = list(self.case.initial_tool_outputs.drug_interactions.values())
            return results[0] if results else None

        return None

    def _synthesize_specialist_opinion(self, parameters: dict[str, Any]) -> BaseModel | None:
        """Synthesize a specialist opinion from the case's ground truth.

        In evaluation mode, the specialist "knows" the correct reasoning and
        provides hints without directly stating the diagnosis.  This mimics
        what a real specialist consultation would provide.
        """
        gt = self.case.ground_truth
        question = parameters.get("specific_question", "")

        # Build a helpful (but not answer-giving) specialist response
        parts = ["### Specialist Opinion"]

        # Use key reasoning points as the basis for the opinion
        if gt.key_reasoning_points:
            # Include 2-3 reasoning points as clinical insights
            insights = gt.key_reasoning_points[:3]
            parts.append(
                "Based on the clinical information provided, I would highlight "
                "the following considerations:\n"
                + "\n".join(f"- {p}" for p in insights)
            )

        parts.append("\n### Differential Critique")
        if gt.differential:
            for d in gt.differential[:3]:
                diag = d.get("diagnosis", "")
                feat = d.get("key_distinguishing", d.get("key_features", ""))
                parts.append(f"- **{diag}**: {feat}")

        parts.append("\n### Red Flags")
        if gt.red_herrings:
            for rh in gt.red_herrings:
                parts.append(
                    f"- **{rh.data_point}** (in {rh.location}): "
                    f"{rh.correct_interpretation}"
                )
        else:
            parts.append("- No specific red flags identified in the provided data.")

        parts.append("\n### Recommendation")
        if gt.critical_actions:
            parts.append(
                "I would ensure the following critical steps are completed:\n"
                + "\n".join(f"- {a}" for a in gt.critical_actions[:3])
            )

        # Return directly as a ToolResult (bypass the model_dump path in get_output)
        return ToolResult(
            tool_name="consult_medical_specialist",
            success=True,
            output={"specialist_opinion": "\n".join(parts), "model": "mock_specialist"},
        )

    def _match_followup_output(self, tool_name: str, parameters: dict[str, Any]) -> BaseModel | None:
        for followup in self.case.followup_outputs:
            if followup.tool_name == tool_name:
                return followup.output
        return None

    def get_call_log(self) -> list[ToolCall]:
        return list(self.call_log)
