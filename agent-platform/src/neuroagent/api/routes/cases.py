"""Case listing, detail, and dataset switching endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

router = APIRouter(tags=["cases"])


@router.get("/datasets")
def list_datasets(request: Request) -> list[dict]:
    """List available datasets with their version, name, case count, and active status."""
    from ..app import DATASETS

    all_datasets = request.app.state.all_datasets
    active = request.app.state.active_dataset
    result = []
    for version, info in DATASETS.items():
        idx = all_datasets.get(version, ({},))[0]
        result.append({
            "version": version,
            "name": info["name"],
            "description": info["description"],
            "case_count": len(idx),
            "active": version == active,
        })
    return result


@router.post("/datasets/{version}/activate")
def activate_dataset(version: str, request: Request) -> dict:
    """Switch the active dataset."""
    all_datasets = request.app.state.all_datasets
    if version not in all_datasets:
        raise HTTPException(status_code=404, detail=f"Dataset '{version}' not found")

    idx, objs = all_datasets[version]
    request.app.state.active_dataset = version
    request.app.state.case_index = idx
    request.app.state.case_objects = objs

    from ..app import DATASETS
    request.app.state.dataset_path = DATASETS[version]["path"]

    return {"status": "ok", "version": version, "case_count": len(idx)}


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
