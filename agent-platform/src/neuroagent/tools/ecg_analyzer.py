from __future__ import annotations
from .base import BaseTool


class ECGAnalyzerTool(BaseTool):
    name = "analyze_ecg"
    description = (
        "Analyze a 12-lead ECG (EUR 18). Returns rhythm, rate, PR/QRS/QT-QTc intervals, "
        "axis, conduction and repolarization, and clinical correlation. Cheap enough to be "
        "part of the initial evaluation of any transient loss of consciousness; a normal "
        "tracing does not exclude a paroxysmal arrhythmia. For prolonged rhythm monitoring "
        "(telemetry, Holter, event monitor, loop recorder), use order_cardiac_monitoring."
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
