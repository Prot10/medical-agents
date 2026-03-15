"""Hospital rules endpoints."""

from __future__ import annotations

import re
from pathlib import Path

import yaml
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

from ...rules.rules_engine import AVAILABLE_HOSPITALS, RulesEngine

router = APIRouter(tags=["hospitals"])


class PathwayUpdate(BaseModel):
    name: str
    description: str
    triggers: list[str]
    steps: list[dict]
    contraindicated: list[str]


@router.get("/hospitals")
def list_hospitals(request: Request) -> list[dict]:
    """Return list of available hospitals with metadata."""
    result = []
    for hospital_id, name in AVAILABLE_HOSPITALS.items():
        engine = RulesEngine(request.app.state.rules_dir, hospital=hospital_id)
        result.append({
            "id": hospital_id,
            "name": name,
            "pathways": [
                {"name": p.name, "description": p.description, "triggers": p.triggers}
                for p in engine.pathways
            ],
        })
    return result


@router.get("/hospitals/{hospital_id}/rules")
def get_hospital_rules(hospital_id: str, request: Request) -> dict:
    """Return full pathway details for a hospital."""
    if hospital_id not in AVAILABLE_HOSPITALS:
        raise HTTPException(status_code=404, detail=f"Hospital '{hospital_id}' not found")

    engine = RulesEngine(request.app.state.rules_dir, hospital=hospital_id)
    return {
        "id": hospital_id,
        "name": AVAILABLE_HOSPITALS[hospital_id],
        "pathways": [
            {
                "name": p.name,
                "description": p.description,
                "triggers": p.triggers,
                "steps": [
                    {
                        "action": s.action,
                        "timing": s.timing,
                        "mandatory": s.mandatory,
                        "condition": s.condition,
                        "details": s.details,
                    }
                    for s in p.steps
                ],
                "contraindicated": p.contraindicated,
            }
            for p in engine.pathways
        ],
    }


def _get_hospital_dir(request: Request, hospital_id: str) -> Path:
    """Validate hospital and return its rules directory."""
    if hospital_id not in AVAILABLE_HOSPITALS:
        raise HTTPException(status_code=404, detail=f"Hospital '{hospital_id}' not found")
    return Path(request.app.state.rules_dir) / hospital_id


def _sorted_yaml_files(hospital_dir: Path) -> list[Path]:
    """Return sorted list of YAML pathway files in a hospital directory."""
    return sorted(hospital_dir.glob("*.yaml"))


def _pathway_dict_from_body(body: PathwayUpdate) -> dict:
    """Convert a PathwayUpdate body to a YAML-serializable dict."""
    return {
        "name": body.name,
        "description": body.description,
        "triggers": body.triggers,
        "steps": body.steps,
        "contraindicated": body.contraindicated,
    }


def _slugify(name: str) -> str:
    """Convert a pathway name to a filesystem-safe slug."""
    slug = name.lower().replace(" ", "_")
    slug = re.sub(r"[^a-z0-9_]", "", slug)
    return slug


@router.put("/hospitals/{hospital_id}/rules/{pathway_index}")
def update_pathway(
    hospital_id: str, pathway_index: int, body: PathwayUpdate, request: Request
) -> dict:
    """Update an existing pathway by index."""
    hospital_dir = _get_hospital_dir(request, hospital_id)
    yaml_files = _sorted_yaml_files(hospital_dir)

    if pathway_index < 0 or pathway_index >= len(yaml_files):
        raise HTTPException(status_code=404, detail=f"Pathway index {pathway_index} out of range")

    target_file = yaml_files[pathway_index]
    data = _pathway_dict_from_body(body)
    target_file.write_text(yaml.dump(data, default_flow_style=False, sort_keys=False))

    return data


@router.post("/hospitals/{hospital_id}/rules", status_code=201)
def create_pathway(hospital_id: str, body: PathwayUpdate, request: Request) -> dict:
    """Create a new pathway."""
    hospital_dir = _get_hospital_dir(request, hospital_id)
    slug = _slugify(body.name)
    target_file = hospital_dir / f"{slug}.yaml"

    if target_file.exists():
        raise HTTPException(status_code=409, detail=f"Pathway file '{target_file.name}' already exists")

    data = _pathway_dict_from_body(body)
    target_file.write_text(yaml.dump(data, default_flow_style=False, sort_keys=False))

    return data


@router.delete("/hospitals/{hospital_id}/rules/{pathway_index}")
def delete_pathway(
    hospital_id: str, pathway_index: int, request: Request
) -> dict:
    """Delete a pathway by index."""
    hospital_dir = _get_hospital_dir(request, hospital_id)
    yaml_files = _sorted_yaml_files(hospital_dir)

    if pathway_index < 0 or pathway_index >= len(yaml_files):
        raise HTTPException(status_code=404, detail=f"Pathway index {pathway_index} out of range")

    yaml_files[pathway_index].unlink()

    return {"status": "ok"}
