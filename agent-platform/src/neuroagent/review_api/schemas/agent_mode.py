"""Models of the agent-mode study: what a physician sends and what is stored per case."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from neuroagent_schemas import ClinicalEpisode
from pydantic import BaseModel, ConfigDict, Field, field_validator

RecordStatus = Literal["in_progress", "completed", "failed"]
# What the harness did with one action the physician sent.
StepOutcome = Literal[
    "observed",  # a tool order that was placed and answered
    "schema_rejected",  # a tool order the tool's schema refused: an error observation, the turn is spent
    "action_rejected",  # not a valid action at all (the adapter refused it): counted, no turn spent
    "assessment",  # the final assessment, accepted
]


class StepTelemetry(BaseModel):
    """Light client-side context of one step. No keystrokes, no free text beyond search terms."""

    model_config = ConfigDict(extra="ignore")

    # Seconds the page was visible between the result being shown and the action being sent.
    active_seconds: float | None = Field(default=None, ge=0, le=7 * 86400)
    # Tool cards opened before choosing, in order.
    tools_opened: list[str] = Field(default_factory=list, max_length=80)
    # Terms typed in the catalogue filter (as left after typing stopped).
    searches: list[str] = Field(default_factory=list, max_length=20)
    raw_view_opened: bool = False
    # The step was finished after the page was loaded again (the browser was closed in between).
    resumed: bool = False

    @field_validator("tools_opened", "searches")
    @classmethod
    def _short_items(cls, value: list[str]) -> list[str]:
        return [item[:80] for item in value]


class ActionRequest(BaseModel):
    """One action as the physician sends it: the function call the agent would emit, plus why."""

    model_config = ConfigDict(extra="forbid")

    # Number of actions already sent for this case; a stale page (double click, second tab) is refused.
    expected_step: int = Field(ge=0)
    name: str = Field(min_length=1, max_length=64)
    arguments: dict[str, Any] = Field(default_factory=dict)
    # Why this test now, or for the assessment the reasoning behind the diagnosis. Physician-only.
    rationale: str = Field(min_length=1, max_length=4000)
    telemetry: StepTelemetry = Field(default_factory=StepTelemetry)

    @field_validator("rationale")
    @classmethod
    def _not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("a rationale is required")
        return value.strip()


class PhysicianStep(BaseModel):
    """One action sent by the physician, with the physician-only data around it."""

    index: int
    turn: int
    name: str
    arguments: dict[str, Any]
    outcome: StepOutcome
    rationale: str
    shown_at: datetime  # when the server returned what the physician acted on
    sent_at: datetime  # when the server received the action
    server_seconds: float
    # Recorded as the action's `latency_seconds`: active time when the client reports it.
    latency_seconds: float
    client: StepTelemetry = Field(default_factory=StepTelemetry)


class AgentRecord(BaseModel):
    """Everything stored for one (reviewer, section, case)."""

    record_version: Literal[1] = 1
    section: str
    set_id: str
    case_id: str
    case_number: int
    reviewer_id: str
    reviewer_name: str
    status: RecordStatus = "in_progress"
    started_at: datetime
    updated_at: datetime
    finished_at: datetime | None = None
    provenance: dict[str, Any] = Field(default_factory=dict)
    # The episode in the benchmark's own format: scored and analysed as a model episode is.
    episode: ClinicalEpisode = Field(default_factory=ClinicalEpisode)
    # Physician-only data, apart from the agent-comparable episode.
    steps: list[PhysicianStep] = Field(default_factory=list)
    diagnostic_reasoning: str | None = None
    failure: dict[str, str] | None = None

    @property
    def invalid_attempts(self) -> int:
        return sum(step.outcome in ("action_rejected", "schema_rejected") for step in self.steps)
