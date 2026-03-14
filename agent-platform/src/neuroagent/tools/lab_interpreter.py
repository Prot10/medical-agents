from __future__ import annotations
from typing import Any
from .base import BaseTool, ToolResult
from .mock_server import MockServer


class LabInterpreterTool(BaseTool):
    name = "interpret_labs"
    description = (
        "Interpret laboratory results including CBC, BMP, liver function, "
        "thyroid, and specialized panels. Returns values with reference "
        "ranges, abnormality flags, and clinical interpretation."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for lab interpretation.",
            },
            "panels": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Which lab panels to interpret (e.g., CBC, BMP, LFT, thyroid).",
            },
            "patient_age": {
                "type": "integer",
                "description": "Patient age in years.",
            },
            "patient_sex": {
                "type": "string",
                "description": "Patient sex (e.g., male, female).",
            },
        },
        "required": ["clinical_context"],
    }

    def __init__(self, mock_server: MockServer | None = None):
        self.mock_server = mock_server

    def execute(self, parameters: dict[str, Any]) -> ToolResult:
        if self.mock_server:
            return self.mock_server.get_output(self.name, parameters)
        raise NotImplementedError(f"Real {self.name} model not yet connected")
