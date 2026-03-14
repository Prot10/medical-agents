from __future__ import annotations
from typing import Any
from .base import BaseTool, ToolResult
from .mock_server import MockServer


class HospitalRulesCheckerTool(BaseTool):
    name = "check_hospital_rules"
    description = (
        "Check hospital protocols and clinical pathways applicable to the "
        "current clinical scenario. Returns required steps, timing "
        "requirements, and any mandatory actions."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_scenario": {
                "type": "string",
                "description": "Description of the current clinical scenario.",
            },
            "suspected_condition": {
                "type": "string",
                "description": "The suspected or confirmed condition.",
            },
        },
        "required": ["clinical_scenario"],
    }

    def __init__(self, mock_server: MockServer | None = None):
        self.mock_server = mock_server

    def execute(self, parameters: dict[str, Any]) -> ToolResult:
        if self.mock_server:
            return self.mock_server.get_output(self.name, parameters)
        raise NotImplementedError(f"Real {self.name} model not yet connected")
