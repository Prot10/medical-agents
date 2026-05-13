"""Reusable FastAPI dependencies for the review API."""

from __future__ import annotations

from fastapi import Depends, Header, HTTPException, Request, status

from .schemas.reviewers import ReviewerCode
from .services.reviewer_codes import ReviewerCodeRegistry


def get_reviewer_registry(request: Request) -> ReviewerCodeRegistry:
    registry: ReviewerCodeRegistry | None = getattr(
        request.app.state, "reviewer_registry", None
    )
    if registry is None:  # pragma: no cover — fail-fast for misconfiguration
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Reviewer registry not initialised",
        )
    return registry


def current_reviewer(
    x_reviewer_code: str | None = Header(default=None, alias="X-Reviewer-Code"),
    registry: ReviewerCodeRegistry = Depends(get_reviewer_registry),
) -> ReviewerCode:
    """Resolve the calling reviewer or 401."""
    reviewer = registry.get(x_reviewer_code)
    if reviewer is None or not reviewer.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive reviewer code",
            headers={"WWW-Authenticate": "X-Reviewer-Code"},
        )
    return reviewer


def require_admin(
    reviewer: ReviewerCode = Depends(current_reviewer),
) -> ReviewerCode:
    """Resolve an admin reviewer or 403."""
    if reviewer.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required",
        )
    return reviewer
