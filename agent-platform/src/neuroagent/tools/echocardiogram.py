from __future__ import annotations
from .base import BaseTool


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
