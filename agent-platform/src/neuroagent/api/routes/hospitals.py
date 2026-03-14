"""Hospital rules endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request

from ...rules.rules_engine import AVAILABLE_HOSPITALS, RulesEngine

router = APIRouter(tags=["hospitals"])


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
