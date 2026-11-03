from __future__ import annotations


from .base import BaseTool
from .vocabulary import csf_sources, csf_special_tests


class CSFAnalyzerTool(BaseTool):
    name = "analyze_csf"
    description = (
        "Analyze cerebrospinal fluid from a lumbar puncture, a shunt tap, an external "
        "ventricular drain or an extended lumbar drain. Cell count, protein and glucose are always reported; name the "
        "additional assays you want in `special_tests`, each of which is priced and scored "
        "separately. Returns interpretation and clinical correlation."
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
            # Optional, so every existing call and criterion means a lumbar puncture as before.
            # Added on the October 2026 review: ventricular CSF from a shunt or a drain is a
            # different sample with different reference values, and a healthcare-associated
            # ventriculitis is diagnosed on it, so a case must be able to require it.
            "source": {
                "type": "string",
                "enum": csf_sources(),
                "description": (
                    "Where the CSF is drawn. 'lumbar_puncture' (default). 'shunt_tap': "
                    "aspiration from the reservoir of a ventricular shunt, for suspected "
                    "shunt infection or malfunction. 'external_ventricular_drain': a sample "
                    "from the drain's sampling port in a patient with an EVD in place. "
                    "'lumbar_drain': extended lumbar drainage through an indwelling catheter "
                    "(about 10 mL/h over 72 hours), the drainage trial after a negative tap test."
                ),
                "default": "lumbar_puncture",
            },
        },
        "required": ["clinical_context"],
    }
