"""Case listing and detail endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

router = APIRouter(tags=["cases"])


@router.get("/cases")
def list_cases(request: Request) -> list[dict]:
    """Return lightweight index of all cases."""
    return list(request.app.state.case_index.values())


@router.get("/cases/{case_id}")
def get_case(case_id: str, request: Request) -> dict:
    """Return full case data including patient info and ground truth."""
    case = request.app.state.case_objects.get(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail=f"Case '{case_id}' not found")
    return case.model_dump(mode="json")
