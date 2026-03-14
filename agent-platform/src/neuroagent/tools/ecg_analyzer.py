from __future__ import annotations
from typing import Any
from .base import BaseTool, ToolResult
from .mock_server import MockServer


class ECGAnalyzerTool(BaseTool):
    name = "analyze_ecg"
    description = (
        "Analyze a 12-lead ECG for cardiac abnormalities. Returns rhythm "
        "analysis, intervals, axis, findings, and clinical correlation."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for the ECG interpretation.",
            },
            "ecg_file_path": {
                "type": "string",
                "description": "Path to the ECG recording file.",
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
