from __future__ import annotations
from typing import Any
from .base import BaseTool, ToolResult
from .mock_server import MockServer


class AdvancedImagingTool(BaseTool):
    name = "order_advanced_imaging"
    description = (
        "Order advanced neuroimaging studies including PET scans, DaTscan, "
        "MR perfusion/spectroscopy, and carotid duplex ultrasound. "
        "Types: amyloid_PET (~$4,000, Alzheimer's confirmation), "
        "FDG_PET (~$2,000, dementia/tumor metabolism), "
        "DaTscan (~$5,000, parkinsonian syndromes), "
        "perfusion_MRI (~$500), MR_spectroscopy (~$500), "
        "carotid_duplex (~$350, stenosis screening)."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the advanced imaging study.",
            },
            "imaging_type": {
                "type": "string",
                "enum": [
                    "amyloid_PET", "FDG_PET", "DaTscan",
                    "perfusion_MRI", "MR_spectroscopy", "carotid_duplex",
                ],
                "description": (
                    "Type of advanced imaging. 'amyloid_PET': amyloid plaque detection "
                    "(Alzheimer's). 'FDG_PET': glucose metabolism (dementia, tumor). "
                    "'DaTscan': dopamine transporter imaging (parkinsonian syndromes). "
                    "'perfusion_MRI': cerebral blood flow (stroke, tumor grading). "
                    "'MR_spectroscopy': brain metabolite analysis (tumor, metabolic). "
                    "'carotid_duplex': carotid artery stenosis screening."
                ),
            },
        },
        "required": ["clinical_context", "imaging_type"],
    }

    def __init__(self, mock_server: MockServer | None = None):
        self.mock_server = mock_server

    def execute(self, parameters: dict[str, Any]) -> ToolResult:
        if self.mock_server:
            return self.mock_server.get_output(self.name, parameters)
        raise NotImplementedError(f"Real {self.name} model not yet connected")
