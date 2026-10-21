"""Per-reviewer CRUD endpoints for case reviews and annotations.

Every endpoint is gated by ``X-Reviewer-Code`` and scoped to that reviewer.
A reviewer can only see (and only modify) annotations under their own
directory — there is no way to read another reviewer's data from these
routes.
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status

from ..dependencies import current_reviewer
from ..schemas.annotations import (
    CaseComment,
    CaseCommentCreate,
    CaseCommentUpdate,
    CaseReview,
    CaseReviewSummary,
    FieldAnnotation,
    FieldAnnotationCreate,
    FieldAnnotationUpdate,
    HeartbeatRequest,
    StatusUpdate,
)
from ..schemas.reviewers import ReviewerCode
from ..services.annotation_store import AnnotationStore

router = APIRouter(tags=["annotations"])

# Per-case caps (mirror the schema max_length) to guard against disk-exhaustion
# from a single reviewer hammering the create endpoints.
MAX_ANNOTATIONS_PER_CASE = 2000
MAX_COMMENTS_PER_CASE = 500


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _store(request: Request) -> AnnotationStore:
    return request.app.state.annotation_store


def _ensure_dataset(request: Request, version: str) -> str:
    if version not in request.app.state.all_datasets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset '{version}' not found",
        )
    return version


def _ensure_case(request: Request, version: str, case_id: str) -> str:
    version = _ensure_dataset(request, version)
    if case_id not in request.app.state.all_datasets[version][1]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case '{case_id}' not found in {version}",
        )
    return version


# ----------------------------------------------------------------------
# Whole-review reads


@router.get(
    "/datasets/{version}/reviews",
    response_model=list[CaseReviewSummary],
)
def list_my_reviews(
    version: str,
    request: Request,
    reviewer: ReviewerCode = Depends(current_reviewer),
) -> list[CaseReviewSummary]:
    version = _ensure_dataset(request, version)
    return _store(request).list_for_reviewer(version, reviewer.code)


@router.get(
    "/datasets/{version}/reviews/{case_id}",
    response_model=CaseReview,
)
def get_review(
    version: str,
    case_id: str,
    request: Request,
    reviewer: ReviewerCode = Depends(current_reviewer),
) -> CaseReview:
    version = _ensure_case(request, version, case_id)
    return _store(request).load_or_init(version, reviewer.code, case_id)


# ----------------------------------------------------------------------
# Status


@router.patch(
    "/datasets/{version}/reviews/{case_id}/status",
    response_model=CaseReview,
)
def set_status(
    version: str,
    case_id: str,
    body: StatusUpdate,
    request: Request,
    reviewer: ReviewerCode = Depends(current_reviewer),
) -> CaseReview:
    version = _ensure_case(request, version, case_id)
    store = _store(request)
    with store.lock_for(version, reviewer.code, case_id):
        review = store.load_or_init(version, reviewer.code, case_id)
        if body.status in {"approved", "needs_changes"}:
            if body.policy_verdict is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="A complete policy verdict is required for a terminal review.",
                )
            if body.status == "approved" and not body.policy_verdict.approves_all:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Approved status requires approval of every policy dimension.",
                )
            if body.status == "approved" and review.unresolved_errors:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Resolve all error annotations before approval.",
                )
            review.policy_verdict = body.policy_verdict
        else:
            review.policy_verdict = None
        review.status = body.status
        return store.save(review)


# ----------------------------------------------------------------------
# Field annotations


@router.post(
    "/datasets/{version}/reviews/{case_id}/annotations",
    response_model=CaseReview,
    status_code=status.HTTP_201_CREATED,
)
def create_annotation(
    version: str,
    case_id: str,
    body: FieldAnnotationCreate,
    request: Request,
    reviewer: ReviewerCode = Depends(current_reviewer),
) -> CaseReview:
    version = _ensure_case(request, version, case_id)
    store = _store(request)
    with store.lock_for(version, reviewer.code, case_id):
        review = store.load_or_init(version, reviewer.code, case_id)
        if any(a.id == body.id for a in review.field_annotations):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Annotation '{body.id}' already exists",
            )
        if len(review.field_annotations) >= MAX_ANNOTATIONS_PER_CASE:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Annotation limit reached for this case",
            )
        now = _utcnow()
        review.field_annotations.append(
            FieldAnnotation(**body.model_dump(), created_at=now, updated_at=now)
        )
        if review.status == "pending":
            review.status = "in_progress"
        return store.save(review)


@router.put(
    "/datasets/{version}/reviews/{case_id}/annotations/{annotation_id}",
    response_model=CaseReview,
)
def update_annotation(
    version: str,
    case_id: str,
    annotation_id: str,
    body: FieldAnnotationUpdate,
    request: Request,
    reviewer: ReviewerCode = Depends(current_reviewer),
) -> CaseReview:
    version = _ensure_case(request, version, case_id)
    store = _store(request)
    with store.lock_for(version, reviewer.code, case_id):
        review = store.load_or_init(version, reviewer.code, case_id)
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
    "/datasets/{version}/reviews/{case_id}/annotations/{annotation_id}",
    response_model=CaseReview,
)
def delete_annotation(
    version: str,
    case_id: str,
    annotation_id: str,
    request: Request,
    reviewer: ReviewerCode = Depends(current_reviewer),
) -> CaseReview:
    version = _ensure_case(request, version, case_id)
    store = _store(request)
    with store.lock_for(version, reviewer.code, case_id):
        review = store.load_or_init(version, reviewer.code, case_id)
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
# Case-wide comments


@router.post(
    "/datasets/{version}/reviews/{case_id}/comments",
    response_model=CaseReview,
    status_code=status.HTTP_201_CREATED,
)
def create_comment(
    version: str,
    case_id: str,
    body: CaseCommentCreate,
    request: Request,
    reviewer: ReviewerCode = Depends(current_reviewer),
) -> CaseReview:
    version = _ensure_case(request, version, case_id)
    store = _store(request)
    with store.lock_for(version, reviewer.code, case_id):
        review = store.load_or_init(version, reviewer.code, case_id)
        if any(c.id == body.id for c in review.case_comments):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Comment '{body.id}' already exists",
            )
        if len(review.case_comments) >= MAX_COMMENTS_PER_CASE:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Comment limit reached for this case",
            )
        now = _utcnow()
        review.case_comments.append(
            CaseComment(**body.model_dump(), created_at=now, updated_at=now)
        )
        if review.status == "pending":
            review.status = "in_progress"
        return store.save(review)


@router.put(
    "/datasets/{version}/reviews/{case_id}/comments/{comment_id}",
    response_model=CaseReview,
)
def update_comment(
    version: str,
    case_id: str,
    comment_id: str,
    body: CaseCommentUpdate,
    request: Request,
    reviewer: ReviewerCode = Depends(current_reviewer),
) -> CaseReview:
    version = _ensure_case(request, version, case_id)
    store = _store(request)
    with store.lock_for(version, reviewer.code, case_id):
        review = store.load_or_init(version, reviewer.code, case_id)
        for idx, comment in enumerate(review.case_comments):
            if comment.id == comment_id:
                updates = body.model_dump(exclude_unset=True)
                updates["updated_at"] = _utcnow()
                review.case_comments[idx] = comment.model_copy(update=updates)
                return store.save(review)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Comment '{comment_id}' not found",
    )


@router.delete(
    "/datasets/{version}/reviews/{case_id}/comments/{comment_id}",
    response_model=CaseReview,
)
def delete_comment(
    version: str,
    case_id: str,
    comment_id: str,
    request: Request,
    reviewer: ReviewerCode = Depends(current_reviewer),
) -> CaseReview:
    version = _ensure_case(request, version, case_id)
    store = _store(request)
    with store.lock_for(version, reviewer.code, case_id):
        review = store.load_or_init(version, reviewer.code, case_id)
        before = len(review.case_comments)
        review.case_comments = [c for c in review.case_comments if c.id != comment_id]
        if len(review.case_comments) == before:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment '{comment_id}' not found",
            )
        return store.save(review)


# ----------------------------------------------------------------------
# Heartbeat


# Anything beyond ~90 min of active time on a single case is almost certainly
# a forgotten tab — even a thorough diagnostic-puzzle review tops out under an
# hour. The client already gates on tab-visibility and user-input recency, but
# this server cap is the last line against runaway accumulation.
MAX_CASE_TIME_SECONDS = 5400


@router.post("/datasets/{version}/reviews/{case_id}/heartbeat")
def heartbeat(
    version: str,
    case_id: str,
    body: HeartbeatRequest,
    request: Request,
    reviewer: ReviewerCode = Depends(current_reviewer),
) -> dict[str, int]:
    version = _ensure_case(request, version, case_id)
    store = _store(request)
    with store.lock_for(version, reviewer.code, case_id):
        review = store.load_or_init(version, reviewer.code, case_id)
        review.time_spent_seconds = min(
            review.time_spent_seconds + body.seconds, MAX_CASE_TIME_SECONDS
        )
        review.last_active_at = _utcnow()
        store.save(review)
    return {"time_spent_seconds": review.time_spent_seconds}
