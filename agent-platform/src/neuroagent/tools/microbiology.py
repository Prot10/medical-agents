"""Microbiology on specimens other than CSF.

Two of the reviewers' requests, one gap: the agent could culture cerebrospinal fluid and
nothing else.

* acute bacterial meningitis — blood cultures with susceptibility testing, whole-blood PCR
  for meningococcus and pneumococcus, and a throat swab, obtained as early as possible and
  preferably before the first antimicrobial dose. Sampling must not delay empirical therapy:
  where lumbar puncture is deferred or imaging is needed first, cultures are drawn and
  treatment started before imaging (WHO 2025).
* hepatic encephalopathy — the infection screen that identifies the precipitant: blood
  cultures, urine culture, and diagnostic paracentesis in *every* patient with ascites. A
  patient with ascites who has not been tapped leaves spontaneous bacterial peritonitis
  unexcluded (EASL 2022).

`collected_before_antimicrobials` is a first-class parameter rather than prose because yield
for every assay here collapses once treatment has started, and the reports are required to
state it rather than leave it to be inferred.
"""

from __future__ import annotations

import logging
from typing import Any

from .base import BaseTool
from .vocabulary import is_valid_specimen, microbiology_specimens

logger = logging.getLogger(__name__)


class MicrobiologyTool(BaseTool):
    name = "order_microbiology"
    description = (
        "Culture, stain or PCR a specimen other than CSF: blood, urine, throat swab, or "
        "ascitic fluid via diagnostic paracentesis. Use this to identify a pathogen or an "
        "infectious precipitant outside the cerebrospinal compartment. Sampling should not "
        "delay empirical antimicrobial therapy — draw, then treat."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the specimen.",
            },
            # Enum derived from costs.yaml (see tools/vocabulary.py).
            "specimen": {
                "type": "string",
                "enum": microbiology_specimens(),
                "description": (
                    "What to sample. 'blood_culture': two sets, with susceptibility "
                    "testing. 'whole_blood_pcr': meningococcus / pneumococcus and other "
                    "principal meningeal pathogens. 'throat_swab': meningococcal culture. "
                    "'urine': urinalysis and culture. 'ascitic_fluid': diagnostic "
                    "paracentesis with PMN count, protein and culture — indicated in every "
                    "patient with ascites and altered mental status."
                ),
            },
            "tests": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Assays to run on the specimen (e.g. culture, gram_stain, "
                    "susceptibility, pcr, cell_count, protein)."
                ),
            },
            "before_antimicrobials": {
                "type": "boolean",
                "description": (
                    "Whether the specimen is being taken before the first antimicrobial "
                    "dose. Yield of culture, stain and PCR falls sharply once treatment "
                    "has started, so the report states this either way."
                ),
                "default": True,
            },
        },
        "required": ["clinical_context", "specimen"],
    }

    def _validate_parameters(self, parameters: dict[str, Any]) -> None:
        """Warn (only) when `specimen` is outside the closed vocabulary."""
        specimen = parameters.get("specimen")
        if isinstance(specimen, str) and not is_valid_specimen(specimen):
            logger.warning(
                "order_microbiology called with out-of-vocabulary specimen %r (known: %s). "
                "Proceeding unchanged — fallback output/cost will apply.",
                specimen,
                ", ".join(microbiology_specimens()),
            )
