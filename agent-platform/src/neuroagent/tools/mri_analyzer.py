from __future__ import annotations
from typing import Any
from .base import BaseTool, ToolResult
from .mock_server import MockServer


class MRIAnalyzerTool(BaseTool):
    name = "analyze_brain_mri"
    description = (
        "Order and analyze a brain MRI scan. Specify the clinical protocol "
        "(standard, epilepsy, stroke, tumor, ms, dementia) and whether "
        "contrast (gadolinium) is needed. Returns findings with locations, "
        "signal characteristics, volumetrics, and clinical impression. "
        "Note: MRI is slower than CT — for emergency hemorrhage exclusion, "
        "use order_ct_scan instead."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context and indication for the MRI.",
            },
            "protocol": {
                "type": "string",
                "enum": ["standard", "epilepsy", "stroke", "tumor", "ms", "dementia"],
                "description": (
                    "MRI protocol to use. 'epilepsy': thin coronal hippocampal cuts (ILAE HARNESS-MRI). "
                    "'stroke': DWI emphasis + MRA. 'tumor': includes perfusion-weighted sequences. "
                    "'ms': sagittal FLAIR + post-contrast T1. 'dementia': volumetric with hippocampal assessment. "
                    "'standard': general brain screen."
                ),
            },
            "contrast": {
                "type": "boolean",
                "description": "Whether gadolinium contrast is needed (e.g., for tumor, MS, infection).",
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
