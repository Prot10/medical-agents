from __future__ import annotations

import logging
from typing import Any

from .base import BaseTool
from .vocabulary import echocardiogram_types, is_valid_echo_type

logger = logging.getLogger(__name__)


class EchocardiogramTool(BaseTool):
    name = "order_echocardiogram"
    description = (
        "Order echocardiography for cardiac structure and function: ventricular size and "
        "systolic function, wall thickness, valve morphology and gradients, atrial size, "
        "pulmonary pressures, pericardium, and intracardiac masses or thrombus. Costs run "
        "from EUR 276 (TTE) to EUR 552 (TEE). A structural finding is not by itself the cause "
        "of a symptom — report it against the mechanism under test."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the echocardiogram.",
            },
            # The enum is derived from costs.yaml so the tool, the cost registry and the
            # benchmark's ground truth cannot drift apart. See tools/vocabulary.py.
            "echo_type": {
                "type": "string",
                "enum": echocardiogram_types(),
                "description": (
                    "Type of echocardiogram. 'TTE': transthoracic — the standard study, "
                    "non-invasive. 'TEE': transesophageal — when the transthoracic window is "
                    "non-diagnostic, or for a prosthetic valve, an intracardiac mass, "
                    "endocarditis or aortic dissection. 'bubble_study': agitated-saline "
                    "contrast for a right-to-left shunt. 'exercise_echo': imaging during or "
                    "immediately after graded exercise, standing, sitting or semi-supine — "
                    "the answer is a provoked outflow-tract gradient or an exercise-induced "
                    "wall-motion or rhythm change that the resting study cannot show."
                ),
                "default": "TTE",
            },
        },
        "required": ["clinical_context"],
    }

    def _validate_parameters(self, parameters: dict[str, Any]) -> None:
        """Warn (only) when `echo_type` is outside the closed vocabulary."""
        echo_type = parameters.get("echo_type")
        if isinstance(echo_type, str) and not is_valid_echo_type(echo_type):
            logger.warning(
                "order_echocardiogram called with out-of-vocabulary echo_type %r "
                "(known: %s). Proceeding unchanged — fallback output/cost will apply.",
                echo_type,
                ", ".join(echocardiogram_types()),
            )
