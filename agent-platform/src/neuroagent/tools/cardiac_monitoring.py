from __future__ import annotations
from typing import Any
from .base import BaseTool, ToolResult
from .mock_server import MockServer


class CardiacMonitoringTool(BaseTool):
    name = "order_cardiac_monitoring"
    description = (
        "Order prolonged cardiac rhythm monitoring for arrhythmia detection. "
        "Used in syncope workup and cryptogenic stroke (paroxysmal AFib). "
        "Types: holter_24h (~$150), holter_48h (~$200), event_monitor_30d "
        "(~$300), telemetry (~$100/day). For a single 12-lead ECG, use "
        "analyze_ecg instead."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for cardiac monitoring.",
            },
            "monitor_type": {
                "type": "string",
                "enum": ["holter_24h", "holter_48h", "event_monitor_30d", "telemetry"],
                "description": (
                    "Type of monitoring. 'holter_24h'/'holter_48h': continuous recording. "
                    "'event_monitor_30d': patient-activated, captures infrequent events. "
                    "'telemetry': inpatient continuous monitoring."
                ),
                "default": "holter_24h",
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
