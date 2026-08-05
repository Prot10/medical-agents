from __future__ import annotations
from neuroagent_schemas import (
    NeuroBenchCase, EEGReport, MRIReport, ECGReport, LabResults, CSFResults,
    LiteratureSearchResult, DrugInteractionResult,
    CTReport, EchoReport, CardiacMonitoringReport,
    AdvancedImagingReport, SpecializedTestReport,
)
from .base import ToolCall, ToolResult
from .followup_matcher import resolve_followup
from typing import Any
from pydantic import BaseModel


class MockServer:
    """Serves pre-generated tool outputs from a NeuroBenchCase."""

    def __init__(self, case: NeuroBenchCase):
        self.case = case
        self.call_log: list[ToolCall] = []
        # Trigger slugs of follow-ups already served this session. Lets distinct
        # re-orders of the same tool escalate through distinct follow-ups.
        self._served_triggers: set[str] = set()

    def get_output(self, tool_name: str, parameters: dict[str, Any]) -> ToolResult:
        # Whether this tool was already called BEFORE this call (a re-order).
        is_repeat_call = any(c.tool_name == tool_name for c in self.call_log)
        self.call_log.append(ToolCall(tool_name=tool_name, parameters=parameters))

        initial = self._match_initial_output(tool_name, parameters)

        # Precedence: a matching follow-up for this specific re-order OVERRIDES the
        # (stale) initial output; a bare first call to a tool still returns its
        # initial output. See followup_matcher.resolve_followup for the full rule.
        followup = resolve_followup(
            tool_name, parameters, self.case.followup_outputs,
            self._served_triggers,
            has_initial_output=initial is not None,
            is_repeat_call=is_repeat_call,
        )
        if followup is not None:
            self._served_triggers.add(followup.trigger_action)
            output = followup.output
            return ToolResult(
                tool_name=tool_name, success=True,
                output=output.model_dump() if isinstance(output, BaseModel) else output,
            )

        # Initial tool output (first, parameter-light order on the pathway).
        if initial is not None:
            return ToolResult(
                tool_name=tool_name, success=True,
                output=initial.model_dump() if isinstance(initial, BaseModel) else initial,
            )

        # Off-pathway fallback: a clinically coherent normal / non-contributory
        # result for a tool that is not on this case's diagnostic pathway.
        output = self._match_fallback_output(tool_name, parameters)
        if output is not None:
            return ToolResult(
                tool_name=tool_name, success=True, from_fallback=True,
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
            # Added with the four post-review tools.
            "order_body_imaging": self.case.initial_tool_outputs.body_imaging,
            "order_microbiology": self.case.initial_tool_outputs.microbiology,
            "obtain_tissue_diagnosis": self.case.initial_tool_outputs.tissue_diagnosis,
            "perform_clinical_assessment": self.case.initial_tool_outputs.clinical_assessment,
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

    def _match_fallback_output(self, tool_name: str, parameters: dict[str, Any]) -> BaseModel | None:
        """Resolve a tool call against the off-pathway fallback tier."""
        fb = self.case.fallback_tool_outputs
        if fb is None:
            return None

        mapping = {
            "analyze_eeg": fb.eeg,
            "analyze_brain_mri": fb.mri,
            "analyze_ecg": fb.ecg,
            "interpret_labs": fb.labs,
            "analyze_csf": fb.csf,
            "order_ct_scan": fb.ct,
            "order_echocardiogram": fb.echo,
            "order_cardiac_monitoring": fb.cardiac_monitoring,
            "order_advanced_imaging": fb.advanced_imaging,
            "order_specialized_test": fb.specialized_test,
            "order_body_imaging": fb.body_imaging,
            "order_microbiology": fb.microbiology,
            "obtain_tissue_diagnosis": fb.tissue_diagnosis,
            "perform_clinical_assessment": fb.clinical_assessment,
        }
        if tool_name in mapping:
            return mapping[tool_name]

        if tool_name == "search_medical_literature" and fb.literature_search:
            results = list(fb.literature_search.values())
            return results[0] if results else None

        if tool_name == "check_drug_interactions" and fb.drug_interactions:
            results = list(fb.drug_interactions.values())
            return results[0] if results else None

        return None

    def get_call_log(self) -> list[ToolCall]:
        return list(self.call_log)
