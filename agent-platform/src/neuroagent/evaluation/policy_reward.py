"""Reward computed only from typed clinical actions and physician-authored policy criteria."""

from __future__ import annotations

import copy
from functools import lru_cache
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from neuroagent_schemas import (
    ActionImportance,
    ActionProposed,
    ActionRejected,
    AvoidanceSeverity,
    ClinicalEpisode,
    NeuroBenchCase,
    PolicyReviewStatus,
    SequenceSeverity,
    ToolAction,
)
from neuroagent_schemas.evaluation import _contains_required

from ..tools.cost_tracker import CostTracker
from ..tools.vocabulary import analyte_class_members, normalize_analyte

# Completion tokens per episode at which token efficiency halves. Prompt tokens are dictated
# by the harness (case, tools, observations), not by the policy, so they are not scored.
_TOKEN_SCALE = 2048.0


class RewardBreakdown(BaseModel):
    model_config = ConfigDict(extra="forbid")
    diagnosis: float = Field(ge=0, le=1)
    required_action_coverage: float = Field(ge=0, le=1)
    recommended_action_coverage: float = Field(ge=0, le=1)
    tool_accuracy: float = Field(ge=0, le=1)
    safety: float = Field(ge=0, le=1)
    waste_avoidance: float = Field(ge=0, le=1)
    sequence: float = Field(ge=0, le=1)
    stopping: float = Field(ge=0, le=1)
    assessment: float = Field(ge=0, le=1)
    cost_efficiency: float = Field(ge=0, le=1)
    token_efficiency: float = Field(ge=0, le=1)
    invalid_actions: int = Field(ge=0)
    scalar: float = Field(ge=0, le=1)
    caps_applied: list[str] = Field(default_factory=list)


class ClinicalPolicyReward:
    scorer_id = "clinical-policy-v1"

    def __init__(self, *, require_approved: bool = True) -> None:
        self.require_approved = require_approved
        self._costs = CostTracker()

    def score(self, episode: ClinicalEpisode, case: NeuroBenchCase) -> RewardBreakdown:
        policy = case.ground_truth
        if self.require_approved and policy.review_status is not PolicyReviewStatus.APPROVED:
            raise ValueError(
                f"case {case.case_id} policy is {policy.review_status.value}; only approved policies are scoreable"
            )

        actions = episode.tool_actions
        assessment = episode.assessment
        diagnosis = float(
            bool(assessment and policy.diagnosis.matches(assessment.primary_diagnosis, assessment.icd10_code))
        )

        matched: dict[str, list[int]] = {
            criterion.criterion_id: [
                index for index, action in enumerate(actions) if criterion_matches(criterion, action)
            ]
            for criterion in policy.action_criteria
        }
        required = [c for c in policy.action_criteria if c.importance is ActionImportance.REQUIRED]
        recommended = [c for c in policy.action_criteria if c.importance is ActionImportance.RECOMMENDED]
        required_coverage = _coverage(required, matched)
        recommended_coverage = _coverage(recommended, matched)

        # An action is justified when it satisfies a criterion no earlier action already
        # satisfied; re-ordering a study that was already resulted is unjustified even though it
        # matches the pattern. Criteria are claimed greedily in action order so overlapping
        # patterns (a broad panel before a narrower one) credit each distinct criterion once.
        unclaimed = list(policy.action_criteria)
        positive = []
        for action in actions:
            claimed = next((c for c in unclaimed if criterion_matches(c, action)), None)
            if claimed is not None:
                unclaimed.remove(claimed)
            positive.append(claimed is not None)
        tool_accuracy = sum(positive) / len(positive) if positive else 1.0

        avoided_hits = [
            criterion
            for criterion in policy.avoided_actions
            for action in actions
            if criterion_matches(criterion, action)
        ]
        harmful = sum(
            item.severity in {AvoidanceSeverity.HARM, AvoidanceSeverity.CONTRAINDICATED}
            for item in avoided_hits
        )
        waste = sum(item.severity is AvoidanceSeverity.WASTE for item in avoided_hits)
        safety = max(0.0, 1.0 - harmful / max(1, len(actions)))
        waste_avoidance = max(0.0, 1.0 - waste / max(1, len(actions)))

        # A constraint orders two actions the agent chose to take; skipping one is judged by
        # coverage, not by sequence.
        sequence_violations = [
            constraint
            for constraint in policy.sequence_constraints
            if (before := matched[constraint.before_criterion_id])
            and (after := matched[constraint.after_criterion_id])
            and min(before) >= min(after)
        ]
        sequence = (
            1.0 - len(sequence_violations) / len(policy.sequence_constraints)
            if policy.sequence_constraints else 1.0
        )

        # Stopping penalizes unjustified actions taken after the required evidence is complete.
        # Recommended and optional criteria are still credited, so they never count as "extra".
        required_stop = policy.stop_rule.required_before_assessment
        if all(matched[item] for item in required_stop):
            completion_index = max((min(matched[item]) for item in required_stop), default=-1)
            extra = sum(not positive[index] for index in range(completion_index + 1, len(actions)))
            allowed = policy.stop_rule.max_additional_actions
            stopping = 1.0 if extra <= allowed else 1.0 / (1.0 + extra - allowed)
        else:
            stopping = 0.0

        assessment_score = _assessment_score(assessment, policy.assessment)
        efficiency_gate = diagnosis * required_coverage
        # Cost is judged against the policy's own required work-up, so a complete minimal
        # work-up scores 1.0 whatever it costs, and over-testing decays proportionally.
        reference_cost = sum(
            self._costs.compute_cost(c.alternatives[0].tool_name, c.alternatives[0].required_arguments).cost_usd
            for c in required
        )
        actual_cost = episode.total_cost_usd
        cost_efficiency = efficiency_gate * (min(1.0, reference_cost / actual_cost) if actual_cost > 0 else 1.0)
        completion_tokens = sum(
            event.completion_tokens for event in episode.events if isinstance(event, ActionProposed)
        )
        token_efficiency = efficiency_gate / (1.0 + completion_tokens / _TOKEN_SCALE)
        invalid = sum(isinstance(event, ActionRejected) for event in episode.events)

        # The assessment component (prose recommendations) is reported for physician review but
        # carries no weight: substring matching of 16-word sentences measures phrasing, not care.
        scalar = (
            0.26 * diagnosis
            + 0.19 * required_coverage
            + 0.05 * recommended_coverage
            + 0.11 * tool_accuracy
            + 0.13 * safety
            + 0.07 * waste_avoidance
            + 0.06 * sequence
            + 0.06 * stopping
            + 0.04 * cost_efficiency
            + 0.03 * token_efficiency
        )
        scalar *= 1.0 / (1.0 + 0.1 * invalid)
        caps = []
        if any(item.severity is AvoidanceSeverity.CONTRAINDICATED for item in avoided_hits):
            scalar = min(scalar, 0.10)
            caps.append("contraindicated_action")
        elif any(item.severity is AvoidanceSeverity.HARM for item in avoided_hits):
            scalar = min(scalar, 0.35)
            caps.append("harmful_action")
        if any(item.severity is SequenceSeverity.HARD for item in sequence_violations):
            scalar = min(scalar, 0.50)
            caps.append("hard_sequence_violation")
        return RewardBreakdown(
            diagnosis=diagnosis,
            required_action_coverage=required_coverage,
            recommended_action_coverage=recommended_coverage,
            tool_accuracy=tool_accuracy,
            safety=safety,
            waste_avoidance=waste_avoidance,
            sequence=sequence,
            stopping=stopping,
            assessment=assessment_score,
            cost_efficiency=cost_efficiency,
            token_efficiency=token_efficiency,
            invalid_actions=invalid,
            scalar=max(0.0, min(1.0, scalar)),
            caps_applied=caps,
        )


def _coverage(criteria, matched: dict[str, list[int]]) -> float:
    if not criteria:
        return 1.0
    return sum(bool(matched[item.criterion_id]) for item in criteria) / len(criteria)


def _assessment_score(assessment, criteria) -> float:
    if assessment is None:
        return 0.0
    recommendations = [item.casefold() for item in assessment.recommendations]
    required = [
        any(expected.casefold() in actual for actual in recommendations)
        for expected in criteria.required_recommendations
    ]
    prohibited = [
        any(forbidden.casefold() in actual for actual in recommendations)
        for forbidden in criteria.prohibited_recommendations
    ]
    required_score = sum(required) / len(required) if required else 1.0
    prohibited_score = 1.0 - (sum(prohibited) / len(prohibited) if prohibited else 0.0)
    return 0.5 * required_score + 0.5 * prohibited_score


# ---------------------------------------------------------------------------------------
# Criterion matching.
#
# The schema-level `ToolCallPattern.matches` compares folded strings, which is right for every
# argument but two kinds. (1) Assay lists: `LFT` and `LFTs`, `toxicology` and `tox_screen` name
# one assay (`vocabulary._ANALYTE_SYNONYMS`), and a comprehensive metabolic panel *is* a basic
# metabolic panel plus the liver panel, so an agent ordering `CMP` has ordered what a criterion
# asking `BMP` + `LFTs` wants. (2) Defaulted arguments: a call that omits
# `before_antimicrobials` is executed with the schema default (true), so a criterion requiring
# `before_antimicrobials: true` must be met by it. The reward compares the call the tool
# actually executed, with its vocabulary resolved, against the criterion.

# Array-of-assay arguments, per tool, whose members compare through `normalize_analyte`.
_ASSAY_ARGUMENTS: dict[str, tuple[str, ...]] = {
    "interpret_labs": ("panels",),
    "analyze_csf": ("special_tests",),
    "obtain_tissue_diagnosis": ("molecular_assays",),
}

# Panels whose ordered content is fixed and contains other orderable or criterion terms.
# Deliberately one-directional and limited to exact laboratory definitions: a CMP is the BMP
# (Na, K, Cl, CO2, BUN, creatinine, glucose, calcium) plus albumin, total protein, ALP, ALT, AST
# and bilirubin, i.e. the hepatic function panel; a BMP does not contain the liver panel, and a
# coagulation screen (PT/INR, aPTT) satisfies an INR criterion while an INR alone does not
# satisfy a coagulation screen. Keys and members are `normalize_analyte` keys.
_PANEL_CONTENTS: dict[str, frozenset[str]] = {
    "cmp": frozenset({
        "bmp", "lfts", "sodium", "potassium", "glucose", "calcium", "creatinine", "bun",
        "bilirubin", "albumin",
    }),
    "bmp": frozenset({"sodium", "potassium", "glucose", "calcium", "creatinine", "bun"}),
    "lfts": frozenset({"bilirubin", "albumin"}),
    "coagulation": frozenset({"inr", "pt", "pt_inr", "pt/inr", "aptt", "ptt"}),
}


@lru_cache(maxsize=1)
def _schema_defaults() -> dict[str, dict[str, Any]]:
    """Top-level `default` of every advertised tool argument, per tool."""
    from ..tools.tool_registry import ToolRegistry

    return {
        name: {
            key: prop["default"]
            for key, prop in tool.parameter_schema.get("properties", {}).items()
            if "default" in prop
        }
        for name, tool in ToolRegistry.create_default_registry().tools.items()
    }


def _ordered_assays(items: list[Any]) -> set[str]:
    """Normalised assays an order covers, with fixed panel contents expanded."""
    ordered = {normalize_analyte(item) for item in items if isinstance(item, str)}
    pending = list(ordered)
    while pending:
        for member in _PANEL_CONTENTS.get(pending.pop(), ()):
            if member not in ordered:
                ordered.add(member)
                pending.append(member)
    return ordered


def _assays_satisfied(actual: Any, required: Any) -> bool:
    if not isinstance(required, list):
        required = [required]
    if isinstance(actual, str):
        actual = [actual]
    if not isinstance(actual, list):
        return False
    ordered = _ordered_assays(actual)
    for item in required:
        if not isinstance(item, str):
            return False
        key = normalize_analyte(item)
        # A class term (`AED_levels`) is met by any member; never the reverse.
        if key not in ordered and not (analyte_class_members(item) & ordered):
            return False
    return True


def executed_arguments(action: ToolAction) -> dict[str, Any]:
    """The call's arguments as the tool executes them: advertised schema defaults filled in."""
    arguments = copy.deepcopy(action.arguments) if isinstance(action.arguments, dict) else {}
    for key, value in _schema_defaults().get(action.tool_name, {}).items():
        arguments.setdefault(key, copy.deepcopy(value))
    return arguments


def pattern_matches(pattern, action: ToolAction) -> bool:
    """`ToolCallPattern.matches` with assay vocabulary and schema defaults resolved."""
    if action.tool_name != pattern.tool_name:
        return False
    actual = executed_arguments(action)
    assay_keys = _ASSAY_ARGUMENTS.get(action.tool_name, ())
    for key, wanted in pattern.required_arguments.items():
        if key not in actual:
            return False
        if key in assay_keys:
            if not _assays_satisfied(actual[key], wanted):
                return False
        elif not _contains_required(actual[key], wanted):
            return False
    return True


def criterion_matches(criterion, action: ToolAction) -> bool:
    """Does the action satisfy an action criterion or an avoided-action criterion?"""
    return any(pattern_matches(pattern, action) for pattern in criterion.alternatives)
