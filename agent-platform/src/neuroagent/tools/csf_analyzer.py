from __future__ import annotations
from typing import Any
from .base import BaseTool, ToolResult
from .mock_server import MockServer


class CSFAnalyzerTool(BaseTool):
    name = "analyze_csf"
    description = (
        "Analyze cerebrospinal fluid results including cell count, protein, "
        "glucose, and special tests (e.g., HSV PCR, oligoclonal bands, "
        "cytology). Returns interpretation and clinical correlation."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for CSF interpretation.",
            },
            "special_tests": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Special CSF tests to interpret (e.g., HSV PCR, oligoclonal bands).",
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
