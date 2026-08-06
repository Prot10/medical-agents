from __future__ import annotations

import logging
from typing import Any

from .base import BaseTool
from .vocabulary import eeg_types, is_valid_eeg_type

logger = logging.getLogger(__name__)


class EEGAnalyzerTool(BaseTool):
    name = "analyze_eeg"
    description = (
        "Order and analyze an EEG recording. Specify the type: 'routine' "
        "(20-40 min, EUR 230), 'ambulatory' (24-72 hr home, EUR 644), 'video' "
        "(inpatient video-EEG, EUR 1104/day), or 'continuous_icu' (EUR 828/day). "
        "Returns classification (normal/abnormal), detected findings with "
        "locations, activating procedure results, and clinical impression. An interictal "
        "recording is often normal, which does not by itself exclude a paroxysmal disorder."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for the EEG interpretation.",
            },
            # The enum is derived from costs.yaml so the tool, the cost registry and the
            # benchmark's ground truth cannot drift apart. See tools/vocabulary.py.
            "eeg_type": {
                "type": "string",
                "enum": eeg_types(),
                "description": (
                    "Type of EEG study. 'routine': 20-40 min outpatient. "
                    "'ambulatory': 24-72 hr home monitoring. "
                    "'video': inpatient video-EEG monitoring (epilepsy surgery workup). "
                    "'continuous_icu': ICU continuous EEG for status monitoring."
                ),
                "default": "routine",
            },
            "patient_age": {
                "type": "integer",
                "description": "Patient age in years.",
            },
            "focus_areas": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Specific areas or patterns to focus on.",
            },
        },
        "required": ["clinical_context"],
    }

    def _validate_parameters(self, parameters: dict[str, Any]) -> None:
        """Warn (only) when `eeg_type` is outside the closed vocabulary."""
        eeg_type = parameters.get("eeg_type")
        if isinstance(eeg_type, str) and not is_valid_eeg_type(eeg_type):
            logger.warning(
                "analyze_eeg called with out-of-vocabulary eeg_type %r (known: %s). "
                "Proceeding unchanged — fallback output/cost will apply.",
                eeg_type,
                ", ".join(eeg_types()),
            )
