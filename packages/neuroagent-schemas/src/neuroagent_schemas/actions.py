"""Canonical model actions and append-only clinical episode events."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated, Any, Literal
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class LenientModel(BaseModel):
    """Assessment payloads drop unknown keys: models decorate differential entries with labels such
    as ``title`` under unconstrained decoding, and failing the episode over a cosmetic key would
    measure the harness, not the policy. Tool arguments stay strict because tools execute them."""

    model_config = ConfigDict(extra="ignore")


class DiagnosisHypothesis(LenientModel):
    diagnosis: str = Field(min_length=1)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class ToolAction(StrictModel):
    type: Literal["tool"] = "tool"
    tool_name: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)


class SubmitAssessment(LenientModel):
    type: Literal["submit_assessment"] = "submit_assessment"
    primary_diagnosis: str = Field(min_length=1)
    icd10_code: str | None = Field(
        default=None, description="ICD-10 code of the primary diagnosis, e.g. G40.209"
    )
    differential: list[DiagnosisHypothesis] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    urgency: Literal["emergent", "urgent", "routine"]
    recommendations: list[str] = Field(default_factory=list)

    @field_validator("differential", mode="before")
    @classmethod
    def _bare_labels(cls, value: Any) -> Any:
        """A differential given as plain strings is the same clinical content."""
        if isinstance(value, list):
            return [{"diagnosis": item} if isinstance(item, str) else item for item in value]
        return value


ClinicalAction = Annotated[
    ToolAction | SubmitAssessment,
    Field(discriminator="type"),
]


def _now() -> datetime:
    return datetime.now(timezone.utc)


class EventBase(StrictModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=_now)
    turn: int = Field(ge=0)


class RunStarted(EventBase):
    type: Literal["run.started"] = "run.started"
    case_id: str
    profile_id: str
    model_id: str
    plugin_versions: dict[str, str] = Field(default_factory=dict)


class ModelRequested(EventBase):
    type: Literal["model.requested"] = "model.requested"
    prompt_tokens: int = Field(default=0, ge=0)


class ActionProposed(EventBase):
    type: Literal["action.proposed"] = "action.proposed"
    action: ClinicalAction
    completion_tokens: int = Field(default=0, ge=0)
    latency_seconds: float = Field(default=0.0, ge=0.0)


class ActionRejected(EventBase):
    type: Literal["action.rejected"] = "action.rejected"
    reason: str
    retry_allowed: bool


class ObservationReceived(EventBase):
    type: Literal["observation.received"] = "observation.received"
    tool_name: str
    success: bool
    output: dict[str, Any] | None = None
    error_message: str | None = None
    cost_usd: float = Field(default=0.0, ge=0.0)
    from_fallback: bool = False
    library: bool = False  # the fallback came from the benchmark-level library, not the case
    rejected: bool = False  # the call violated the tool's schema and was never placed
    unavailable: bool = False  # a recorded case holds no result for this order (never performed)


class AssessmentSubmitted(EventBase):
    type: Literal["assessment.submitted"] = "assessment.submitted"
    assessment: SubmitAssessment


class PluginEvent(EventBase):
    type: Literal["plugin.event"] = "plugin.event"
    namespace: str = Field(pattern=r"^[a-z][a-z0-9_.-]+$")
    payload: dict[str, Any] = Field(default_factory=dict)


class RunCompleted(EventBase):
    type: Literal["run.completed"] = "run.completed"
    reason: Literal["assessment_submitted"] = "assessment_submitted"


class RunFailed(EventBase):
    type: Literal["run.failed"] = "run.failed"
    reason: Literal[
        "invalid_action",
        "budget_exhausted",
        "model_error",
        "environment_error",
    ]
    message: str = ""


EpisodeEvent = Annotated[
    RunStarted
    | ModelRequested
    | ActionProposed
    | ActionRejected
    | ObservationReceived
    | AssessmentSubmitted
    | PluginEvent
    | RunCompleted
    | RunFailed,
    Field(discriminator="type"),
]


class ClinicalEpisode(StrictModel):
    schema_version: Literal["1.0"] = "1.0"
    events: list[EpisodeEvent] = Field(default_factory=list)

    @property
    def actions(self) -> list[ClinicalAction]:
        return [event.action for event in self.events if isinstance(event, ActionProposed)]

    @property
    def tool_actions(self) -> list[ToolAction]:
        return [action for action in self.actions if isinstance(action, ToolAction)]

    @property
    def assessment(self) -> SubmitAssessment | None:
        for event in reversed(self.events):
            if isinstance(event, AssessmentSubmitted):
                return event.assessment
        return None

    @property
    def total_cost_usd(self) -> float:
        return sum(
            event.cost_usd for event in self.events if isinstance(event, ObservationReceived)
        )

    @property
    def total_tokens(self) -> int:
        return sum(
            event.prompt_tokens if isinstance(event, ModelRequested)
            else event.completion_tokens if isinstance(event, ActionProposed)
            else 0
            for event in self.events
        )
