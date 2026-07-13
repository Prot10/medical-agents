from __future__ import annotations
from .base import BaseTool


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
