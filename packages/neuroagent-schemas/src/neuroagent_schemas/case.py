"""Case definition Pydantic models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, model_validator

from .enums import CaseDifficulty, EncounterType, NeurologicalCondition
from .evaluation import GroundTruth
from .patient import PatientProfile
from .tool_outputs import (
    AdvancedImagingReport,
    CardiacMonitoringReport,
    CSFResults,
    CTReport,
    DrugInteractionResult,
    ECGReport,
    EchoReport,
    EEGReport,
    LabResults,
    LiteratureSearchResult,
    MRIReport,
    SpecializedTestReport,
)


class ToolOutputSet(BaseModel):
    """All pre-generated tool outputs for one case."""

    eeg: EEGReport | None = None
    mri: MRIReport | None = None
    ecg: ECGReport | None = None
    labs: LabResults | None = None
    csf: CSFResults | None = None
    ct: CTReport | None = None
    echo: EchoReport | None = None
    cardiac_monitoring: CardiacMonitoringReport | None = None
    advanced_imaging: AdvancedImagingReport | None = None
    specialized_test: SpecializedTestReport | None = None
    literature_search: dict[str, LiteratureSearchResult] | None = None
    drug_interactions: dict[str, DrugInteractionResult] | None = None


# Maps a tool name to the output model it must produce. Used to resolve the
# `FollowUpToolOutput.output` union deterministically: the union members overlap
# (several share `findings`/`impression`/`recommended_actions`) and Pydantic
# ignores extra keys, so an unkeyed union silently picks the wrong member —
# losing the output's content at runtime. Resolve by tool name instead.
_TOOL_OUTPUT_MODEL: dict[str, type[BaseModel]] = {
    "analyze_eeg": EEGReport,
    "analyze_brain_mri": MRIReport,
    "interpret_labs": LabResults,
    "analyze_csf": CSFResults,
    "analyze_ecg": ECGReport,
    "order_ct_scan": CTReport,
    "order_echocardiogram": EchoReport,
    "order_cardiac_monitoring": CardiacMonitoringReport,
    "order_advanced_imaging": AdvancedImagingReport,
    "order_specialized_test": SpecializedTestReport,
    "search_medical_literature": LiteratureSearchResult,
    "check_drug_interactions": DrugInteractionResult,
}


class FollowUpToolOutput(BaseModel):
    """A conditional tool output triggered by a specific agent request."""

    trigger_action: str
    tool_name: str
    # The model_validator below dispatches by tool_name; the union is the fallback.
    output: (
        EEGReport
        | MRIReport
        | LabResults
        | CSFResults
        | ECGReport
        | CTReport
        | EchoReport
        | CardiacMonitoringReport
        | AdvancedImagingReport
        | SpecializedTestReport
        | LiteratureSearchResult
        | DrugInteractionResult
    )

    @model_validator(mode="before")
    @classmethod
    def _resolve_output_by_tool(cls, data: Any) -> Any:
        """Coerce `output` to the model implied by `tool_name` before the union
        is tried, so resolution is deterministic. A malformed output raises a
        clear error here instead of silently mis-resolving to the wrong type."""
        if isinstance(data, dict):
            model = _TOOL_OUTPUT_MODEL.get(data.get("tool_name"))
            out = data.get("output")
            if model is not None and isinstance(out, dict):
                data = {**data, "output": model.model_validate(out)}
        return data


class NeuroBenchCase(BaseModel):
    case_id: str
    condition: NeurologicalCondition
    difficulty: CaseDifficulty
    encounter_type: EncounterType
    patient: PatientProfile
    initial_tool_outputs: ToolOutputSet
    followup_outputs: list[FollowUpToolOutput] = []
    # Off-pathway tier: clinically coherent normal / non-contributory results
    # for tools the agent may call that are not on this case's diagnostic
    # pathway. Keeps the simulation realistic instead of erroring out.
    fallback_tool_outputs: ToolOutputSet | None = None
    ground_truth: GroundTruth
    metadata: dict[str, Any] = {}
