from __future__ import annotations
from .base import BaseTool


class ECGAnalyzerTool(BaseTool):
    name = "analyze_ecg"
    description = (
        "Analyze a 12-lead ECG (~$20). Returns rhythm analysis, intervals, "
        "axis, findings, and clinical correlation. For prolonged cardiac "
        "rhythm monitoring (Holter, event monitor), use order_cardiac_monitoring."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for the ECG interpretation.",
            },
        },
        "required": ["clinical_context"],
    }
