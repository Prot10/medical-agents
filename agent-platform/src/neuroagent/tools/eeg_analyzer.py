from __future__ import annotations
from typing import Any
from .base import BaseTool, ToolResult
from .mock_server import MockServer


class EEGAnalyzerTool(BaseTool):
    name = "analyze_eeg"
    description = (
        "Order and analyze an EEG recording. Specify the type: 'routine' "
        "(20-40 min, ~$250), 'ambulatory' (24-72 hr home, ~$700), 'video' "
        "(inpatient video-EEG, ~$1,200/day), or 'continuous_icu' (~$900/day). "
        "Returns classification (normal/abnormal), detected findings with "
        "locations, activating procedure results, and clinical impression."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for the EEG interpretation.",
            },
            "eeg_type": {
                "type": "string",
                "enum": ["routine", "ambulatory", "video", "continuous_icu"],
                "description": (
                    "Type of EEG study. 'routine': 20-40 min outpatient. "
                    "'ambulatory': 24-72 hr home monitoring. "
                    "'video': inpatient video-EEG monitoring (epilepsy surgery workup). "
                    "'continuous_icu': ICU continuous EEG for status monitoring."
                ),
                "default": "routine",
            },
            "patient_age": {
                "type": "integer",
                "description": "Patient age in years.",
            },
            "focus_areas": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Specific areas or patterns to focus on.",
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
