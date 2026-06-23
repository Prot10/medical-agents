"""Per-reviewer tool-review endpoints.

A reviewer assesses the agent's tool catalog (grouped by condition),
annotates coverage gaps, and proposes new tools. Every endpoint is gated
by ``X-Reviewer-Code`` and scoped to that reviewer's own file.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status

from ..dependencies import current_reviewer
from ..schemas.annotations import (
    FieldAnnotation,
    FieldAnnotationCreate,
    FieldAnnotationUpdate,
)
from ..schemas.reviewers import ReviewerCode
from ..schemas.tool_review import (
    ProposedTool,
    ProposedToolCreate,
    ProposedToolUpdate,
    ToolCatalog,
    ToolReview,
    ToolReviewCompleteUpdate,
)
from ..services.tool_review_store import ToolReviewStore

router = APIRouter(tags=["tool-review"])

# Per-reviewer caps (mirror the schema max_length) — guard against disk abuse.
MAX_TOOL_ANNOTATIONS = 2000
MAX_PROPOSALS = 500


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _store(request: Request) -> ToolReviewStore:
    return request.app.state.tool_review_store


def _ensure_dataset(request: Request, version: str) -> None:
    if version not in request.app.state.all_datasets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset '{version}' not found",
        )


# ----------------------------------------------------------------------
# Catalog (read-only)


@router.get("/datasets/{version}/tool-catalog", response_model=ToolCatalog)
def get_tool_catalog(version: str, request: Request,
                     _reviewer: ReviewerCode = Depends(current_reviewer)) -> ToolCatalog:
    _ensure_dataset(request, version)
    catalog = request.app.state.tool_catalogs.get(version)
    if catalog is None:  # pragma: no cover — built at startup for every dataset
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No tool catalog for '{version}'",
        )
    return catalog


# ----------------------------------------------------------------------
# Whole-review read


@router.get("/datasets/{version}/tool-review", response_model=ToolReview)
def get_tool_review(version: str, request: Request,
                    reviewer: ReviewerCode = Depends(current_reviewer)) -> ToolReview:
    _ensure_dataset(request, version)
    return _store(request).load_or_init(version, reviewer.code)


# ----------------------------------------------------------------------
# Completion flag (drives the first-run reminder)


@router.patch("/datasets/{version}/tool-review/complete", response_model=ToolReview)
def set_complete(version: str, body: ToolReviewCompleteUpdate, request: Request,
                 reviewer: ReviewerCode = Depends(current_reviewer)) -> ToolReview:
    _ensure_dataset(request, version)
    store = _store(request)
    review = store.load_or_init(version, reviewer.code)
    review.completed_at = _utcnow() if body.completed else None
    return store.save(review)


# ----------------------------------------------------------------------
# Field annotations (reuse FieldAnnotation; field_path encodes the target)


@router.post(
    "/datasets/{version}/tool-review/annotations",
    response_model=ToolReview,
    status_code=status.HTTP_201_CREATED,
)
def create_annotation(version: str, body: FieldAnnotationCreate, request: Request,
                      reviewer: ReviewerCode = Depends(current_reviewer)) -> ToolReview:
    _ensure_dataset(request, version)
    store = _store(request)
    review = store.load_or_init(version, reviewer.code)
    if any(a.id == body.id for a in review.field_annotations):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Annotation '{body.id}' already exists",
        )
    if len(review.field_annotations) >= MAX_TOOL_ANNOTATIONS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Annotation limit reached",
        )
    now = _utcnow()
    review.field_annotations.append(
        FieldAnnotation(**body.model_dump(), created_at=now, updated_at=now)
    )
    return store.save(review)


@router.put(
    "/datasets/{version}/tool-review/annotations/{annotation_id}",
    response_model=ToolReview,
)
def update_annotation(version: str, annotation_id: str, body: FieldAnnotationUpdate,
                      request: Request,
                      reviewer: ReviewerCode = Depends(current_reviewer)) -> ToolReview:
    _ensure_dataset(request, version)
    store = _store(request)
    review = store.load_or_init(version, reviewer.code)
    for idx, annotation in enumerate(review.field_annotations):
        if annotation.id == annotation_id:
            updates = body.model_dump(exclude_unset=True)
            updates["updated_at"] = _utcnow()
            review.field_annotations[idx] = annotation.model_copy(update=updates)
            return store.save(review)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Annotation '{annotation_id}' not found",
    )


@router.delete(
    "/datasets/{version}/tool-review/annotations/{annotation_id}",
    response_model=ToolReview,
)
def delete_annotation(version: str, annotation_id: str, request: Request,
                      reviewer: ReviewerCode = Depends(current_reviewer)) -> ToolReview:
    _ensure_dataset(request, version)
    store = _store(request)
    review = store.load_or_init(version, reviewer.code)
    before = len(review.field_annotations)
    review.field_annotations = [
        a for a in review.field_annotations if a.id != annotation_id
    ]
    if len(review.field_annotations) == before:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Annotation '{annotation_id}' not found",
        )
    return store.save(review)


# ----------------------------------------------------------------------
# Proposed tools


@router.post(
    "/datasets/{version}/tool-review/proposals",
    response_model=ToolReview,
    status_code=status.HTTP_201_CREATED,
)
def create_proposal(version: str, body: ProposedToolCreate, request: Request,
                    reviewer: ReviewerCode = Depends(current_reviewer)) -> ToolReview:
    _ensure_dataset(request, version)
    store = _store(request)
    review = store.load_or_init(version, reviewer.code)
    if any(p.id == body.id for p in review.proposed_tools):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Proposal '{body.id}' already exists",
        )
    if len(review.proposed_tools) >= MAX_PROPOSALS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Proposal limit reached",
        )
    now = _utcnow()
    review.proposed_tools.append(
        ProposedTool(**body.model_dump(), created_at=now, updated_at=now)
    )
    return store.save(review)


@router.put(
    "/datasets/{version}/tool-review/proposals/{proposal_id}",
    response_model=ToolReview,
)
def update_proposal(version: str, proposal_id: str, body: ProposedToolUpdate,
                    request: Request,
                    reviewer: ReviewerCode = Depends(current_reviewer)) -> ToolReview:
    _ensure_dataset(request, version)
    store = _store(request)
    review = store.load_or_init(version, reviewer.code)
    for idx, proposal in enumerate(review.proposed_tools):
        if proposal.id == proposal_id:
            updates = body.model_dump(exclude_unset=True)
            updates["updated_at"] = _utcnow()
            review.proposed_tools[idx] = proposal.model_copy(update=updates)
            return store.save(review)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Proposal '{proposal_id}' not found",
    )


@router.delete(
    "/datasets/{version}/tool-review/proposals/{proposal_id}",
    response_model=ToolReview,
)
def delete_proposal(version: str, proposal_id: str, request: Request,
                    reviewer: ReviewerCode = Depends(current_reviewer)) -> ToolReview:
    _ensure_dataset(request, version)
    store = _store(request)
    review = store.load_or_init(version, reviewer.code)
    before = len(review.proposed_tools)
    review.proposed_tools = [
        p for p in review.proposed_tools if p.id != proposal_id
    ]
    if len(review.proposed_tools) == before:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proposal '{proposal_id}' not found",
        )
    return store.save(review)
