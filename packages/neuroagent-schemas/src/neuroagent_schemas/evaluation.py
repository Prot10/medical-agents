"""Clinician-reviewable policy specifications for evaluation and training."""

from __future__ import annotations

import re
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .actions import ToolAction
from .enums import Likelihood, SequenceSeverity


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PolicyReviewStatus(str, Enum):
    DRAFT = "draft"
    NEEDS_REVISION = "needs_revision"
    APPROVED = "approved"


class ActionImportance(str, Enum):
    REQUIRED = "required"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"


class AvoidanceSeverity(str, Enum):
    WASTE = "waste"
    HARM = "harm"
    CONTRAINDICATED = "contraindicated"


def _fold(value: Any) -> Any:
    if isinstance(value, str):
        return " ".join(value.strip().lower().replace("_", " ").split())
    if isinstance(value, list):
        return [_fold(item) for item in value]
    if isinstance(value, dict):
        return {key: _fold(item) for key, item in value.items()}
    return value


def _contains_required(actual: Any, required: Any) -> bool:
    actual, required = _fold(actual), _fold(required)
    if isinstance(required, list):
        if not isinstance(actual, list):
            return False
        return all(any(_contains_required(candidate, item) for candidate in actual) for item in required)
    if isinstance(required, dict):
        return isinstance(actual, dict) and all(
            key in actual and _contains_required(actual[key], value)
            for key, value in required.items()
        )
    return actual == required


class ToolCallPattern(StrictModel):
    tool_name: str = Field(min_length=1)
    required_arguments: dict[str, Any] = Field(default_factory=dict)

    def matches(self, action: ToolAction) -> bool:
        return (
            action.tool_name == self.tool_name
            and _contains_required(action.arguments, self.required_arguments)
        )


class DiagnosisCriterion(StrictModel):
    accepted: list[str] = Field(min_length=1)
    icd_codes: list[str] = Field(default_factory=list)

    def matches(self, diagnosis: str) -> bool:
        candidate = re.sub(r"[^a-z0-9]+", " ", diagnosis.lower()).strip()
        return any(
            candidate == re.sub(r"[^a-z0-9]+", " ", accepted.lower()).strip()
            or candidate in re.sub(r"[^a-z0-9]+", " ", accepted.lower()).strip()
            or re.sub(r"[^a-z0-9]+", " ", accepted.lower()).strip() in candidate
            for accepted in self.accepted
        )


class DifferentialDx(StrictModel):
    diagnosis: str
    likelihood: Likelihood
    key_features: str = ""
    icd_code: str | None = None


class ActionCriterion(StrictModel):
    criterion_id: str = Field(pattern=r"^[a-z][a-z0-9_.-]*$")
    label: str = Field(min_length=1)
    importance: ActionImportance
    alternatives: list[ToolCallPattern] = Field(min_length=1)
    expected_evidence: str = ""
    rationale: str = ""
    citations: list[str] = Field(default_factory=list)

    def matches(self, action: ToolAction) -> bool:
        return any(pattern.matches(action) for pattern in self.alternatives)


class AvoidedActionCriterion(StrictModel):
    criterion_id: str = Field(pattern=r"^[a-z][a-z0-9_.-]*$")
    severity: AvoidanceSeverity
    alternatives: list[ToolCallPattern] = Field(min_length=1)
    rationale: str
    citations: list[str] = Field(default_factory=list)

    def matches(self, action: ToolAction) -> bool:
        return any(pattern.matches(action) for pattern in self.alternatives)


class SequenceConstraint(StrictModel):
    before_criterion_id: str
    after_criterion_id: str
    reason: str
    citations: list[str] = Field(default_factory=list)
    severity: SequenceSeverity = SequenceSeverity.SOFT


class StopRule(StrictModel):
    required_before_assessment: list[str] = Field(default_factory=list)
    max_additional_actions: int = Field(default=0, ge=0)


class AssessmentCriteria(StrictModel):
    required_recommendations: list[str] = Field(default_factory=list)
    prohibited_recommendations: list[str] = Field(default_factory=list)


class RedHerring(StrictModel):
    data_point: str
    location: str
    field_path: str = ""
    intended_effect: str
    correct_interpretation: str


class GroundTruth(StrictModel):
    review_status: PolicyReviewStatus
    diagnosis: DiagnosisCriterion
    differential: list[DifferentialDx] = Field(default_factory=list)
    action_criteria: list[ActionCriterion] = Field(default_factory=list)
    avoided_actions: list[AvoidedActionCriterion] = Field(default_factory=list)
    sequence_constraints: list[SequenceConstraint] = Field(default_factory=list)
    stop_rule: StopRule
    assessment: AssessmentCriteria = Field(default_factory=AssessmentCriteria)
    key_clinical_evidence: list[str] = Field(default_factory=list)
    red_herrings: list[RedHerring] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_references(self) -> "GroundTruth":
        action_ids = [criterion.criterion_id for criterion in self.action_criteria]
        avoided_ids = [criterion.criterion_id for criterion in self.avoided_actions]
        if len(action_ids) != len(set(action_ids)):
            raise ValueError("action criterion ids must be unique")
        if len(avoided_ids) != len(set(avoided_ids)):
            raise ValueError("avoided-action criterion ids must be unique")
        known = set(action_ids)
        referenced = set(self.stop_rule.required_before_assessment)
        for constraint in self.sequence_constraints:
            referenced.add(constraint.before_criterion_id)
            referenced.add(constraint.after_criterion_id)
        missing = sorted(referenced - known)
        if missing:
            raise ValueError(f"policy references unknown action criteria: {missing}")
        return self
