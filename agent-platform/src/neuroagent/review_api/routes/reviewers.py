"""Endpoints for reviewer identity."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from ..dependencies import current_reviewer, get_reviewer_registry, require_admin
from ..schemas.reviewers import ReviewerCode, ReviewerProfile
from ..services.reviewer_codes import ReviewerCodeRegistry

router = APIRouter(tags=["reviewers"])


@router.get("/reviewers/me", response_model=ReviewerProfile)
def get_me(reviewer: ReviewerCode = Depends(current_reviewer)) -> ReviewerProfile:
    """Validate the X-Reviewer-Code header and return the caller's profile."""
    return ReviewerProfile(code=reviewer.code, name=reviewer.name, role=reviewer.role)


@router.get("/reviewers", response_model=list[ReviewerProfile])
def list_reviewers(
    _admin: ReviewerCode = Depends(require_admin),
    registry: ReviewerCodeRegistry = Depends(get_reviewer_registry),
) -> list[ReviewerProfile]:
    """Admin-only: list every reviewer."""
    return [
        ReviewerProfile(code=r.code, name=r.name, role=r.role)
        for r in registry.all()
    ]
