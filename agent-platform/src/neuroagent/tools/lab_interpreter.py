from __future__ import annotations

import logging
from typing import Any

from .base import BaseTool
from .vocabulary import lab_panels, normalize_analyte

logger = logging.getLogger(__name__)


class LabInterpreterTool(BaseTool):
    name = "interpret_labs"
    description = (
        "Interpret laboratory results. Name the individual assays you want in `panels` — "
        "each is priced and scored separately, so requesting a broad panel when one analyte "
        "answers the question costs more without adding diagnostic yield. Returns values "
        "with reference ranges, abnormality flags, and clinical interpretation."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for lab interpretation.",
            },
            # Vocabulary derived from costs.yaml (see tools/vocabulary.py). Advisory rather
            # than closed: an unlisted assay still runs and is charged `default_panel`, but
            # naming one from this list is what makes the request priceable and scoreable.
            # Before this list existed the parameter read "e.g., CBC, BMP, LFT, thyroid",
            # which told the agent nothing about the 150 assays actually available — the
            # clinical reviewers flagged the resulting bucket in nine conditions.
            "panels": {
                "type": "array",
                "items": {"type": "string", "enum": lab_panels()},
                "description": (
                    "Individual assays or named panels to interpret. Each entry is billed "
                    "separately, from EUR 5 (glucose, sodium) to EUR 2300 "
                    "(paraneoplastic). Prefer the specific assay the question needs."
                ),
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

    def _validate_parameters(self, parameters: dict[str, Any]) -> None:
        """Warn (only) when an assay is outside the priced vocabulary.

        Out-of-vocabulary analytes are charged `default_panel` and cannot match a
        ground-truth action, which is a silent scoring loss — so it must be visible in the
        logs. Behaviour is deliberately unchanged: rejecting the call would change agent
        behaviour mid-benchmark.
        """
        panels = parameters.get("panels")
        if not isinstance(panels, (list, tuple)):
            return
        known = {normalize_analyte(p) for p in lab_panels()}
        unknown = [p for p in panels if normalize_analyte(str(p)) not in known]
        if unknown:
            logger.warning(
                "interpret_labs called with %d out-of-vocabulary panel(s): %s. "
                "Proceeding unchanged — default_panel rate applies and no optimal action "
                "can match them.",
                len(unknown),
                ", ".join(repr(u) for u in unknown),
            )
