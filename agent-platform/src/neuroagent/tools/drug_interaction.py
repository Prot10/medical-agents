from __future__ import annotations
from .base import BaseTool


class DrugInteractionTool(BaseTool):
    name = "check_drug_interactions"
    description = (
        "Check drug interactions, contraindications, and formulary status "
        "for a proposed medication. Returns interactions with current "
        "medications, warnings, and alternative options."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "drug": {
                "type": "string",
                "description": "The proposed medication to check.",
            },
            "current_medications": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of patient's current medications.",
            },
            "patient_conditions": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of patient's medical conditions.",
            },
        },
        "required": ["drug"],
    }
