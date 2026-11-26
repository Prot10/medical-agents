"""Reusable FastAPI dependencies for the review API."""

from __future__ import annotations

from fastapi import Depends, Header, HTTPException, Request, status

from .schemas.reviewers import ReviewerCode
from .services.rate_limit import AuthRateLimiter
from .services.review_sets import visible_sets
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


def authenticated_code(
    request: Request,
    x_reviewer_code: str | None = Header(default=None, alias="X-Reviewer-Code"),
    registry: ReviewerCodeRegistry = Depends(get_reviewer_registry),
) -> ReviewerCode:
    """Resolve the calling code (of either kind) or 401, with brute-force throttling."""
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


def current_reviewer(
    request: Request,
    reviewer: ReviewerCode = Depends(authenticated_code),
) -> ReviewerCode:
    """Resolve a dataset-review code. An agent-mode code is refused on every dataset-review route:
    it must never reach a case file, a policy or a ground truth.

    On a route addressed by ``{version}``, a guided code (assigned review sets) reaches only its
    sets, and no code reaches a set it is not shown (an ``assigned_only`` set of someone else).
    """
    if reviewer.is_agent_mode:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This code opens the agent-mode study only",
        )
    sets = getattr(request.app.state, "review_sets", {})
    try:
        allowed = {s.id for s in visible_sets(reviewer, sets)}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc
    version = request.path_params.get("version")
    if version is not None:
        if reviewer.is_guided and version not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This code opens its assigned review set only",
            )
        if version in sets and version not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Review set not assigned to this code")
    return reviewer


def agent_mode_reviewer(
    reviewer: ReviewerCode = Depends(authenticated_code),
) -> ReviewerCode:
    """Resolve an agent-mode code or 403 (dataset-review and admin codes do not work cases)."""
    if not reviewer.is_agent_mode:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This code does not open the agent-mode study",
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
