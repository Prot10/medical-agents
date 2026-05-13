"""Pydantic models for reviewer-code identity."""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator

ReviewerRole = Literal["reviewer", "admin"]

_CODE_PATTERN = re.compile(r"^[A-Z0-9-]{3,16}$")


class ReviewerCode(BaseModel):
    """One row from ``reviewer_codes.yaml``."""

    code: str = Field(..., description="Unique uppercase code")
    name: str = Field(..., min_length=1, max_length=120)
    role: ReviewerRole = "reviewer"
    active: bool = True

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
