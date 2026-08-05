"""Structured bedside assessment as an orderable act.

Reviewer 1 named three required diagnostic steps that no tool could express, all of them
clinical rather than instrumental:

* migraine with aura — "the true required diagnostic tool should be a structured
  headache/aura history with neurological examination and application of ICHD-3 criteria",
  documenting aura type, complete reversibility, gradual spread, symptom succession,
  duration, and red flags. Their alternative was to drop the condition for lacking a
  test-based workup (ICHD-3; EHF/EAN 2021; NICE CG150).
* normal pressure hydrocephalus — objective gait and cognitive assessment, ideally before and
  after the CSF tap test: timed walking tests, Timed Up and Go, standardised gait/balance
  assessment (International iNPH guidelines; AAN; Japanese iNPH 3rd ed.).
* the dementias — a bedside cognitive screen ahead of imaging, as the first step of the
  suggested sequence (NICE NG97; SNLG/ISS; DETeCD-ADRD 2025).

It also answers their FND objection. FND is a positive clinical diagnosis — Hoover's sign,
entrainment — so with this tool the condition becomes solvable *without* imaging, which is
exactly the correct pathway, and it can be kept as the benchmark's diagnostic-restraint probe
with every instrumental tool optional.

Deliberately non-overlapping with `order_specialized_test`: a full validated battery is
`neuropsych_battery`, bedside spirometry is `respiratory_function`, and formal autonomic
testing is `autonomic_testing`. Duplicating a study under two tools would let either satisfy
the ground truth.
"""

from __future__ import annotations

import logging
from typing import Any

from .base import BaseTool
from .vocabulary import assessment_types, is_valid_assessment_type

logger = logging.getLogger(__name__)


class ClinicalAssessmentTool(BaseTool):
    name = "perform_clinical_assessment"
    description = (
        "Perform a structured bedside assessment and receive the findings and scores: a "
        "cognitive screen, an ICHD-3 headache and aura history, timed gait and balance "
        "testing, or examination for positive functional neurological signs. These are "
        "clinical acts, not instrumental tests — for several conditions they are the "
        "confirmatory step, and for a purely clinical diagnosis they are the whole pathway."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "What the assessment is meant to establish or exclude.",
            },
            # Enum derived from costs.yaml (see tools/vocabulary.py).
            "assessment_type": {
                "type": "string",
                "enum": assessment_types(),
                "description": (
                    "'cognitive_screen': MoCA / MMSE at the bedside, with informant history "
                    "— the first step in suspected cognitive decline, before imaging (a full "
                    "battery is order_specialized_test{neuropsych_battery}). "
                    "'structured_headache_history_ichd3': headache and aura features against "
                    "ICHD-3 criteria — reversibility, gradual spread, succession, duration, "
                    "red flags. 'gait_and_balance_timed': Timed Up and Go and timed walk; "
                    "run before and after a CSF tap test in suspected NPH. "
                    "'functional_neuro_signs': Hoover's sign, entrainment and the other "
                    "positive signs of a functional disorder."
                ),
            },
            "timing": {
                "type": "string",
                "description": (
                    "Optional label for when the assessment was performed, e.g. 'baseline' "
                    "or 'post_tap_test' — the NPH tap test is interpreted as a pair."
                ),
            },
        },
        "required": ["clinical_context", "assessment_type"],
    }

    def _validate_parameters(self, parameters: dict[str, Any]) -> None:
        """Warn (only) when `assessment_type` is outside the closed vocabulary."""
        assessment = parameters.get("assessment_type")
        if isinstance(assessment, str) and not is_valid_assessment_type(assessment):
            logger.warning(
                "perform_clinical_assessment called with out-of-vocabulary "
                "assessment_type %r (known: %s). Proceeding unchanged — fallback "
                "output/cost will apply.",
                assessment,
                ", ".join(assessment_types()),
            )
