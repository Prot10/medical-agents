"""Reusable FastAPI dependencies for the review API."""

from __future__ import annotations

from fastapi import Depends, Header, HTTPException, Request, status

from .schemas.reviewers import ReviewerCode
from .services.rate_limit import AuthRateLimiter
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


def get_auth_limiter(request: Request) -> AuthRateLimiter | None:
    return getattr(request.app.state, "auth_limiter", None)


def current_reviewer(
    request: Request,
    x_reviewer_code: str | None = Header(default=None, alias="X-Reviewer-Code"),
    registry: ReviewerCodeRegistry = Depends(get_reviewer_registry),
) -> ReviewerCode:
    """Resolve the calling reviewer or 401, with brute-force throttling."""
    limiter = get_auth_limiter(request)
    key = AuthRateLimiter.client_key(request) if limiter else ""

    if limiter:
        retry_after = limiter.retry_after(key)
        if retry_after is not None:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many failed attempts. Try again later.",
                headers={"Retry-After": str(retry_after)},
            )

    reviewer = registry.get(x_reviewer_code)
    if reviewer is None or not reviewer.active:
        if limiter:
            limiter.record_failure(key)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive reviewer code",
            headers={"WWW-Authenticate": "X-Reviewer-Code"},
        )
    if limiter:
        limiter.record_success(key)
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
