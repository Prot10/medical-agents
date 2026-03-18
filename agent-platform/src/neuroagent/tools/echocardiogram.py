from __future__ import annotations
from typing import Any
from .base import BaseTool, ToolResult
from .mock_server import MockServer


class EchocardiogramTool(BaseTool):
    name = "order_echocardiogram"
    description = (
        "Order echocardiography for cardiac structure and function assessment. "
        "Used in stroke workup (cardioembolic source: PFO, thrombus, valve "
        "vegetations), syncope evaluation, and heart failure. Types: TTE "
        "(transthoracic, ~$300), TEE (transesophageal, ~$600), bubble study (~$400)."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the echocardiogram.",
            },
            "echo_type": {
                "type": "string",
                "enum": ["TTE", "TEE", "bubble_study"],
                "description": (
                    "Type of echocardiogram. 'TTE': transthoracic (standard, non-invasive). "
                    "'TEE': transesophageal (better for PFO, thrombus, endocarditis). "
                    "'bubble_study': contrast echo for PFO/shunt detection."
                ),
                "default": "TTE",
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
