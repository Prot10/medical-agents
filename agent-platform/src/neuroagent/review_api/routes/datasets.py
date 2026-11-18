"""Read-only dataset and case endpoints.

These power the case list and case detail in the review frontend.
Datasets are addressed by ``version`` in the URL — there is no global
"active dataset" concept (unlike the main agent API).
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status

from ..config import AVAILABLE_DATASETS
from ..dependencies import current_reviewer
from ..schemas.reviewers import ReviewerCode

router = APIRouter(tags=["datasets"])


def _datasets(request: Request) -> dict[str, tuple[dict, dict]]:
    return request.app.state.all_datasets


@router.get("/datasets")
def list_datasets(
    request: Request,
    _reviewer: ReviewerCode = Depends(current_reviewer),
) -> list[dict[str, Any]]:
    """List every registered dataset with its case count."""
    all_datasets = _datasets(request)
    default_version: str = request.app.state.default_dataset_version
    out: list[dict[str, Any]] = []
    for version, info in AVAILABLE_DATASETS.items():
        idx = all_datasets.get(version, ({},))[0]
        out.append(
            {
                "version": version,
                "name": info.name,
                "description": info.description,
                "case_count": len(idx),
                "is_default": version == default_version,
            }
        )
    return out


@router.get("/datasets/{version}/cases")
def list_cases(
    version: str,
    request: Request,
    _reviewer: ReviewerCode = Depends(current_reviewer),
) -> list[dict[str, Any]]:
    """Lightweight index of every case in the given dataset version."""
    all_datasets = _datasets(request)
    if version not in all_datasets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset '{version}' not found",
        )
    idx = all_datasets[version][0]
    return list(idx.values())


@router.get("/datasets/{version}/cases/{case_id}")
def get_case(
    version: str,
    case_id: str,
    request: Request,
    _reviewer: ReviewerCode = Depends(current_reviewer),
) -> dict[str, Any]:
    """Return the full NeuroBenchCase for the given (version, case_id)."""
    all_datasets = _datasets(request)
    if version not in all_datasets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset '{version}' not found",
        )
    case = all_datasets[version][1].get(case_id)
    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Case '{case_id}' not found in {version}",
        )
    return case.model_dump(mode="json")


@router.get("/review-sets")
def list_review_sets(
    request: Request,
    _reviewer: ReviewerCode = Depends(current_reviewer),
) -> list[dict[str, Any]]:
    """Every review set (a fixed case subset re-reviewed in its own space), in file order.

    A set's id is a dataset version: its cases, reviews and progress use the same routes.
    """
    return [
        {
            "id": s.id,
            "base_version": s.base,
            "name": s.name,
            "description": s.description,
            "case_ids": list(s.case_ids),
            "case_count": len(s.case_ids),
        }
        for s in getattr(request.app.state, "review_sets", {}).values()
    ]
