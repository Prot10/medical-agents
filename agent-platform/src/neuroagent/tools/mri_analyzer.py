from __future__ import annotations
from typing import Any
from .base import BaseTool, ToolResult
from .mock_server import MockServer


class MRIAnalyzerTool(BaseTool):
    name = "analyze_brain_mri"
    description = (
        "Analyze a brain MRI scan for structural abnormalities. Returns "
        "findings with locations, signal characteristics, volumetrics, "
        "differential diagnoses, and clinical impression."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for the MRI interpretation.",
            },
            "mri_file_path": {
                "type": "string",
                "description": "Path to the MRI scan file.",
            },
            "sequences": {
                "type": "array",
                "items": {"type": "string"},
                "description": "MRI sequences to analyze (e.g., T1, T2, FLAIR, DWI).",
            },
            "contrast": {
                "type": "boolean",
                "description": "Whether contrast-enhanced sequences are available.",
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
