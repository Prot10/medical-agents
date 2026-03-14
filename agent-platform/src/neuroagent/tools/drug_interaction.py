from __future__ import annotations
from typing import Any
from .base import BaseTool, ToolResult
from .mock_server import MockServer


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

    def __init__(self, mock_server: MockServer | None = None):
        self.mock_server = mock_server

    def execute(self, parameters: dict[str, Any]) -> ToolResult:
        if self.mock_server:
            return self.mock_server.get_output(self.name, parameters)
        raise NotImplementedError(f"Real {self.name} model not yet connected")
