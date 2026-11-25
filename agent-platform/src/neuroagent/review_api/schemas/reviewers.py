"""Pydantic models for reviewer-code identity."""

from __future__ import annotations

import hashlib
import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

ReviewerRole = Literal["reviewer", "admin"]
# Sections of the "work the case as the agent" study a code may open (services/agent_mode).
AgentSection = Literal["agent_synthetic", "agent_mimic"]

_CODE_PATTERN = re.compile(r"^[A-Z0-9-]{3,64}$")
_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{1,31}$")


class ReviewerCode(BaseModel):
    """One row from ``reviewer_codes.yaml``."""

    code: str = Field(..., description="Unique uppercase code")
    name: str = Field(..., min_length=1, max_length=120)
    role: ReviewerRole = "reviewer"
    specialty: str | None = Field(default=None, max_length=120)
    credentials: str | None = Field(default=None, max_length=120)
    active: bool = True
    # Agent-mode codes only. A code with `sections` opens those sections of the agent-mode study
    # and nothing else: no dataset review, no policies, no ground truth. A code without it is a
    # dataset-review code and behaves exactly as before.
    sections: list[AgentSection] = Field(default_factory=list)
    # Public identifier written into agent-mode records and episodes (`physician:<id>`), so the
    # secret code never reaches a log. Defaults to a hash of the code.
    id: str | None = None
    # The same person's dataset-review code(s): synthetic cases they reviewed there are skipped.
    linked_review_codes: list[str] = Field(default_factory=list)

    @field_validator("id")
    @classmethod
    def _check_id(cls, value: str | None) -> str | None:
        if value is not None and not _ID_PATTERN.fullmatch(value):
            raise ValueError("id must be 2-32 chars of a-z, 0-9, or hyphen")
        return value

    @field_validator("linked_review_codes", mode="before")
    @classmethod
    def _normalize_links(cls, value: object) -> object:
        if isinstance(value, list):
            return [item.strip().upper() if isinstance(item, str) else item for item in value]
        return value

    @model_validator(mode="after")
    def _agent_codes_are_not_admins(self) -> "ReviewerCode":
        if self.sections and self.role != "reviewer":
            raise ValueError("an agent-mode code (with sections) cannot be an admin")
        if len(set(self.sections)) != len(self.sections):
            raise ValueError("sections must not repeat")
        return self

    @property
    def is_agent_mode(self) -> bool:
        return bool(self.sections)

    @property
    def public_id(self) -> str:
        return self.id or "r-" + hashlib.sha256(self.code.encode()).hexdigest()[:10]

    @field_validator("code", mode="before")
    @classmethod
    def _normalize_code(cls, value: object) -> str:
        if not isinstance(value, str):
            raise TypeError("code must be a string")
        normalized = value.strip().upper()
        if not _CODE_PATTERN.fullmatch(normalized):
            raise ValueError(
                "code must be 3-16 chars of A-Z, 0-9, or hyphen"
            )
        return normalized


class ReviewerProfile(BaseModel):
    """Response payload for ``/reviewers/me``."""

    code: str
    name: str
    role: ReviewerRole
    specialty: str | None = None
    credentials: str | None = None
    # Non-empty for an agent-mode code: the client then shows the agent-mode study only.
    sections: list[AgentSection] = Field(default_factory=list)
