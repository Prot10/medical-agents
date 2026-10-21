"""Personal progress endpoint (per-reviewer)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status

from ..dependencies import current_reviewer
from ..schemas.reviewers import ReviewerCode
from ..services.aggregations import reviewer_progress_summary

router = APIRouter(tags=["progress"])


@router.get("/datasets/{version}/progress")
def my_progress(
    version: str,
    request: Request,
    reviewer: ReviewerCode = Depends(current_reviewer),
) -> dict[str, Any]:
    all_datasets = request.app.state.all_datasets
    if version not in all_datasets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset '{version}' not found",
        )
    case_objects = all_datasets[version][1]
    store = request.app.state.annotation_store
    return reviewer_progress_summary(store, version, reviewer.code, case_objects)
