from __future__ import annotations
from neuroagent_schemas import (
    NeuroBenchCase, EEGReport, MRIReport, ECGReport, LabResults, CSFResults,
    LiteratureSearchResult, DrugInteractionResult,
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

    def _match_followup_output(self, tool_name: str, parameters: dict[str, Any]) -> BaseModel | None:
        for followup in self.case.followup_outputs:
            if followup.tool_name == tool_name:
                return followup.output
        return None

    def get_call_log(self) -> list[ToolCall]:
        return list(self.call_log)
