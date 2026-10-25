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


def _tokens(text: str) -> set[str]:
    return set(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


def _code(text: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", text.upper())


# Negation scope is the clause: text between punctuation, a spaced dash or "but".
_CLAUSE = re.compile(r"[,;:.()\[\]{}]|\s[-–—]\s|[–—]|\bbut\b")
# A clause that denies what it names: "CADASIL excluded", "ALS criteria not met".
_DENIED_CLAUSE = re.compile(
    r"\b(?:ruled out|excluded|unlikely|less likely"
    r"|not (?:met|likely|present|supported|fulfilled|confirmed|satisfied|consistent))\b"
)
# A cue that denies the rest of its clause: "MOGAD rather than MS", "SAH, not aneurysmal".
_DENIAL_ONSET = re.compile(
    r"\b(?:not|no|rather than|instead of|excluding|without evidence of|mimicking|masquerading as"
    r"|(?:previously |initially |originally )?(?:mis)?diagnosed as|mislabell?ed as)\b"
)


def _affirmed(text: str) -> str:
    """The part of a diagnosis text that is asserted, with denied clauses removed.

    "non-X" becomes the single word "nonX", so "non-aneurysmal" never supplies "aneurysmal".
    "without X" becomes "withoutX" in the same way: "PD without dementia" names no dementia, and
    "migraine without aura" stays distinct from "migraine with aura". "X negative" becomes
    "Xnegative", so "LGI1-negative encephalitis" does not name LGI1 encephalitis.
    """
    text = re.sub(r"\bnon[\s-]+(?=[a-z])", "non", text.lower())
    kept = []
    for clause in _CLAUSE.split(text):
        if _DENIED_CLAUSE.search(clause):
            continue
        onset = _DENIAL_ONSET.search(clause)
        kept.append(clause[: onset.start()] if onset else clause)
    text = re.sub(r"\bwithout\s+(?=[a-z])", "without", " ".join(kept))
    return re.sub(r"\b([a-z0-9]+)[\s-]+negative\b", r"\1negative", text)


def _names(candidate: set[str], labels: list[str]) -> bool:
    return any(label <= candidate for text in labels if (label := _tokens(_affirmed(text))))


class DiagnosisCriterion(StrictModel):
    """Accepted and rejected labels, and ICD-10 codes, for the primary diagnosis.

    A submitted diagnosis matches when every token of an accepted label occurs in its asserted
    part (order and punctuation insensitive; denied clauses such as "rather than MS" or "CADASIL
    excluded" are dropped first), no rejected label occurs there (a competing diagnosis named
    alongside, e.g. "ALS or MS", or a wrong subtype, e.g. "PD dementia"), and every required
    component of a mixed diagnosis is named too. The ICD code never decides the diagnosis: it is
    scored apart by `code_matches`. Labels are seeded per ICD code from
    `config/policies/diagnosis_synonyms.yaml` and refined by physician review.
    """

    accepted: list[str] = Field(min_length=1)
    icd_codes: list[str] = Field(default_factory=list)
    rejected: list[str] = Field(default_factory=list)
    # Mixed diagnoses: each component is a list of alternative labels, one of which must be named.
    required_components: list[list[str]] = Field(default_factory=list)

    def matches(self, diagnosis: str) -> bool:
        candidate = _tokens(_affirmed(diagnosis))
        return (
            _names(candidate, self.accepted)
            and not _names(candidate, self.rejected)
            and all(_names(candidate, component) for component in self.required_components)
        )

    def code_matches(self, icd10_code: str | None) -> bool:
        """The submitted code equals an accepted one at the WHO subcategory level (4 characters).

        ICD-10-CM extends the WHO codes, so G43.1 (WHO) and G43.109 (CM) agree, while G30.0 and
        G30.1 (onset before and after 65) do not.
        """
        submitted = _code(icd10_code or "")
        if len(submitted) < 3:
            return False
        for code in map(_code, self.icd_codes):
            width = min(4, len(submitted), len(code))
            if width >= 3 and submitted[:width] == code[:width]:
                return True
        return False


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
