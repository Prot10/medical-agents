"""Case definition Pydantic models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from .enums import CaseDifficulty, EncounterType, NeurologicalCondition
from .evaluation import GroundTruth
from .patient import PatientProfile
from .tool_outputs import (
    CSFResults,
    DrugInteractionResult,
    ECGReport,
    EEGReport,
    LabResults,
    LiteratureSearchResult,
    MRIReport,
)


class ToolOutputSet(BaseModel):
    """All pre-generated tool outputs for one case."""

    eeg: EEGReport | None = None
    mri: MRIReport | None = None
    ecg: ECGReport | None = None
    labs: LabResults | None = None
    csf: CSFResults | None = None
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
    ground_truth: GroundTruth
    metadata: dict[str, Any] = {}
