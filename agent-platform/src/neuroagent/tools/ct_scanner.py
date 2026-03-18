from __future__ import annotations
from typing import Any
from .base import BaseTool, ToolResult
from .mock_server import MockServer


class CTScanTool(BaseTool):
    name = "order_ct_scan"
    description = (
        "Order a CT scan of the head. CT is faster and cheaper than MRI — "
        "use for emergency neuroimaging (hemorrhage exclusion, acute trauma), "
        "or CT angiography (CTA) for vascular assessment in acute stroke. "
        "Cost: ~$200 base, +$100 contrast, +$200 CTA."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the CT scan.",
            },
            "contrast": {
                "type": "boolean",
                "description": "Whether IV contrast is needed.",
                "default": False,
            },
            "angiography": {
                "type": "boolean",
                "description": "Whether CT angiography (CTA) is needed for vascular assessment.",
                "default": False,
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
