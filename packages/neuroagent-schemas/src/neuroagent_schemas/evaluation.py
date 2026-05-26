"""Evaluation and ground truth Pydantic models."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from .enums import ActionCategory, Likelihood, SequenceSeverity


class DifferentialDx(BaseModel):
    """A differential diagnosis entry with structured likelihood."""

    diagnosis: str
    likelihood: Likelihood
    key_features: str = ""
    icd_code: str | None = None


class ActionStep(BaseModel):
    """A step in the optimal diagnostic workup.

    Only steps that *should* be performed live here (required / recommended /
    optional). Steps that should NOT be performed live in `harmful_tools` or
    `contraindicated_actions` on the parent GroundTruth.
    """

    step: int
    action: str
    tool_name: str | None = None
    expected_finding: str = ""
    category: ActionCategory
    tool_parameters: dict[str, Any] = {}
    citation: str = ""  # e.g., "AAN 2009 Practice Parameter ALS", "AHA/ASA 2019 §3.2"
    guideline_source: str = ""  # short tag matching the criteria pack allow-list


class ToolClassification(BaseModel):
    """A per-case classification of a tool that should NOT be called.

    Used in `GroundTruth.useless_tools` and `GroundTruth.harmful_tools`.
    The distinction matters for metric weighting:
    - useless = wasted resources (precision / cost penalty)
    - harmful = patient harm (safety penalty)
    """

    tool_name: str
    tool_parameters: dict[str, Any] = {}
    rationale: str  # one-sentence justification, clinician-readable
    citation: str = ""  # guideline reference when applicable


class SequenceConstraint(BaseModel):
    """An ordering constraint between two tool calls.

    Only authored where ordering is clinically load-bearing (don't over-author).
    Typical entries: imaging-before-LP in suspected mass effect; labs-before-empiric
    therapy in suspected metabolic disease; MRI-before-LP in unexplained
    encephalopathy.
    """

    before: str  # tool_name that must precede
    after: str  # tool_name that must follow
    reason: str
    citation: str = ""
    severity: SequenceSeverity = SequenceSeverity.SOFT


class RedHerring(BaseModel):
    """An intentional distractor embedded in a case to test agent reasoning."""

    data_point: str  # what the misleading element is
    location: str  # legacy free-text label (e.g., "labs", "history")
    field_path: str = ""  # structured dotted path (e.g., "initial_tool_outputs.labs.panels.metabolic[3]")
    intended_effect: str  # how it might mislead
    correct_interpretation: str  # what the agent should conclude


class GroundTruth(BaseModel):
    primary_diagnosis: str
    icd_code: str
    differential: list[DifferentialDx] = []
    optimal_actions: list[ActionStep] = []
    # NEW (v5 gold trajectory regen): explicit per-case classification of tools
    # the agent should NOT call. Enables tool_precision / safety metrics that
    # the previous set-membership-only model could not express.
    useless_tools: list[ToolClassification] = []
    harmful_tools: list[ToolClassification] = []
    sequence_constraints: list[SequenceConstraint] = []
    critical_actions: list[str] = Field(
        default_factory=list,
        description="Free-text MUST-do clinical actions (some may not map to a tool).",
    )
    contraindicated_actions: list[str] = Field(
        default_factory=list,
        description="Free-text MUST-NOT-do clinical actions (some may not map to a tool).",
    )
    key_reasoning_points: list[str] = []
    red_herrings: list[RedHerring] = []
