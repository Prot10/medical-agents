from __future__ import annotations

import logging
from typing import Any

from .base import BaseTool
from .vocabulary import csf_special_tests, normalize_analyte

logger = logging.getLogger(__name__)


class CSFAnalyzerTool(BaseTool):
    name = "analyze_csf"
    description = (
        "Analyze cerebrospinal fluid from a lumbar puncture. Cell count, protein and "
        "glucose are always reported; name the additional assays you want in "
        "`special_tests`, each of which is priced and scored separately. Returns "
        "interpretation and clinical correlation."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for CSF interpretation.",
            },
            # Vocabulary derived from costs.yaml (see tools/vocabulary.py). Advisory rather
            # than closed: an unlisted assay still runs and is charged `default_test`.
            # The old "e.g., HSV PCR, oligoclonal bands" wording is why the same generic
            # panel — oligoclonal bands, PCR, antibodies, 14-3-3/RT-QuIC — was attached to
            # subarachnoid haemorrhage, meningitis, GBS and NPH alike, which the clinical
            # reviewers flagged in each of them.
            "special_tests": {
                "type": "array",
                "items": {"type": "string", "enum": csf_special_tests()},
                "description": (
                    "Additional CSF assays to run, billed separately from the EUR 230 "
                    "lumbar puncture: from EUR 18 (IgG index) to EUR 1840 (autoimmune "
                    "panel). Order the assay the differential calls for — 14-3-3 and "
                    "RT_QuIC answer a prion question, HSV_PCR an encephalitis question."
                ),
            },
        },
        "required": ["clinical_context"],
    }

    def _validate_parameters(self, parameters: dict[str, Any]) -> None:
        """Warn (only) when an assay is outside the priced vocabulary.

        Out-of-vocabulary assays get the default rate and cannot match a ground-truth
        action, which is a silent scoring loss, so it must be visible in the logs.
        """
        tests = parameters.get("special_tests")
        if not isinstance(tests, (list, tuple)):
            return
        known = {normalize_analyte(t) for t in csf_special_tests()}
        unknown = [t for t in tests if normalize_analyte(str(t)) not in known]
        if unknown:
            logger.warning(
                "analyze_csf called with %d out-of-vocabulary special_test(s): %s. "
                "Proceeding unchanged — default rate applies and no optimal action can "
                "match them.",
                len(unknown),
                ", ".join(repr(u) for u in unknown),
            )
