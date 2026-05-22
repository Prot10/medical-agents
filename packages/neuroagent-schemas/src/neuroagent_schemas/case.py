"""Case definition Pydantic models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

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


class FollowUpToolOutput(BaseModel):
    """A conditional tool output triggered by a specific agent request."""

    trigger_action: str
    tool_name: str
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
