from __future__ import annotations


from .base import BaseTool
from .vocabulary import csf_special_tests


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
            # Vocabulary derived from costs.yaml (see tools/vocabulary.py); any spelling that
            # normalises to a member is accepted, anything else is rejected at execution.
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
