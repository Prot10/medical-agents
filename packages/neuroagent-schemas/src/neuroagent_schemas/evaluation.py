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


class GroundTruth(BaseModel):
    primary_diagnosis: str
    icd_code: str
    differential: list[dict[str, str]] = []  # diagnosis, likelihood, key_features
    optimal_actions: list[ActionStep] = []
    critical_actions: list[str] = []  # MUST do
    contraindicated_actions: list[str] = []  # MUST NOT do
    key_reasoning_points: list[str] = []
