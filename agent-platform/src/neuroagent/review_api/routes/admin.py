"""Admin (researcher) endpoints — aggregate views across all reviewers."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from neuroagent.datasets import normalize_dataset_version

from ..dependencies import get_reviewer_registry, require_admin
from ..schemas.reviewers import ReviewerCode
from ..services.aggregations import (
    all_reviewers_progress,
    case_diff,
    field_hotspots,
    inter_rater_agreement,
)
from ..services.reviewer_codes import ReviewerCodeRegistry
from ..services.tool_review_aggregations import tool_review_summary

router = APIRouter(prefix="/admin", tags=["admin"])


def _require_dataset(request: Request, version: str) -> tuple[str, dict]:
    version = normalize_dataset_version(version)
    all_datasets = request.app.state.all_datasets
    if version not in all_datasets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset '{version}' not found",
        )
    return version, all_datasets[version][1]


@router.get("/datasets/{version}/agreement")
def get_agreement(
    version: str,
    request: Request,
    _admin: ReviewerCode = Depends(require_admin),
    registry: ReviewerCodeRegistry = Depends(get_reviewer_registry),
) -> dict[str, Any]:
    version, case_objects = _require_dataset(request, version)
    return inter_rater_agreement(
        request.app.state.annotation_store,
        version,
        registry.all(),
        case_objects,
    )


@router.get("/datasets/{version}/progress")
def get_all_progress(
    version: str,
    request: Request,
    _admin: ReviewerCode = Depends(require_admin),
    registry: ReviewerCodeRegistry = Depends(get_reviewer_registry),
) -> list[dict[str, Any]]:
    version, case_objects = _require_dataset(request, version)
    return all_reviewers_progress(
        request.app.state.annotation_store,
        version,
        registry.all(),
        case_objects,
    )


@router.get("/datasets/{version}/field-hotspots")
def get_field_hotspots(
    version: str,
    request: Request,
    _admin: ReviewerCode = Depends(require_admin),
    registry: ReviewerCodeRegistry = Depends(get_reviewer_registry),
) -> list[dict[str, Any]]:
    version, case_objects = _require_dataset(request, version)
    reviewer_codes = [r.code for r in registry.all() if r.role == "reviewer"]
    return field_hotspots(
        request.app.state.annotation_store,
        version,
        reviewer_codes,
        case_objects,
    )


@router.get("/datasets/{version}/cases/{case_id}/diff")
def get_case_diff(
    version: str,
    case_id: str,
    request: Request,
    _admin: ReviewerCode = Depends(require_admin),
    registry: ReviewerCodeRegistry = Depends(get_reviewer_registry),
) -> dict[str, Any]:
    version, case_objects = _require_dataset(request, version)
    if case_id not in case_objects:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case '{case_id}' not found in {version}",
        )
    return case_diff(
        request.app.state.annotation_store,
        version,
        case_id,
        registry.all(),
    )


@router.get("/datasets/{version}/tool-review")
def get_tool_review_summary(
    version: str,
    request: Request,
    _admin: ReviewerCode = Depends(require_admin),
    registry: ReviewerCodeRegistry = Depends(get_reviewer_registry),
) -> dict[str, Any]:
    version, _case_objects = _require_dataset(request, version)
    return tool_review_summary(
        request.app.state.tool_review_store,
        version,
        registry.all(),
    )
