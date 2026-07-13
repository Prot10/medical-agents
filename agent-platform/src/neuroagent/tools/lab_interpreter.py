from __future__ import annotations
from .base import BaseTool


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
