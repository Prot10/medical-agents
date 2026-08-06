from __future__ import annotations
from .base import BaseTool
from .vocabulary import by_type_values


class CardiacMonitoringTool(BaseTool):
    name = "order_cardiac_monitoring"
    description = (
        "Order prolonged cardiac rhythm monitoring — the only study that can correlate a "
        "symptom with the rhythm at the moment it happens. Match the modality to how often "
        "events occur: inpatient telemetry (EUR 92/day) while the patient is at risk, "
        "holter_24h/holter_48h (EUR 138/184) for events at least weekly, an event monitor "
        "(EUR 230/276) when they are weeks apart, an implantable loop recorder (EUR 4600) when "
        "they are months apart. An unselected 24-hour recording in a patient with rare events "
        "is diagnostic in a very small minority. For a single 12-lead ECG, use analyze_ecg."
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
                "enum": by_type_values("order_cardiac_monitoring"),
                "description": (
                    "Type of monitoring. 'holter_24h'/'holter_48h': continuous recording. "
                    "'event_monitor_14d'/'event_monitor_30d': patient-activated, captures "
                    "infrequent events. 'implantable_loop_recorder': months to years of "
                    "monitoring (cryptogenic stroke, unexplained syncope). "
                    "'telemetry': inpatient continuous monitoring."
                ),
                "default": "holter_24h",
            },
        },
        "required": ["clinical_context"],
    }
