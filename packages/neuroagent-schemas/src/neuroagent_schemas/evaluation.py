"""Evaluation and ground truth Pydantic models."""

from __future__ import annotations

from pydantic import BaseModel

from .enums import ActionCategory


class ActionStep(BaseModel):
    step: int
    action: str
    tool_name: str | None = None
    expected_finding: str = ""
    category: ActionCategory


class RedHerring(BaseModel):
    """An intentional distractor embedded in a case to test agent reasoning."""

    data_point: str  # what the misleading element is
    location: str  # where it appears (e.g., "labs", "history", "mri")
    intended_effect: str  # how it might mislead (e.g., "suggests infection over tumor")
    correct_interpretation: str  # what the agent should conclude


class GroundTruth(BaseModel):
    primary_diagnosis: str
    icd_code: str
    differential: list[dict[str, str]] = []  # diagnosis, likelihood, key_features
    optimal_actions: list[ActionStep] = []
    critical_actions: list[str] = []  # MUST do
    contraindicated_actions: list[str] = []  # MUST NOT do
    key_reasoning_points: list[str] = []
    red_herrings: list[RedHerring] = []  # intentional distractors for puzzle/moderate cases
