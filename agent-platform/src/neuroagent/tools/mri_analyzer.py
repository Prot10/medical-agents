from __future__ import annotations


from .base import BaseTool
from .vocabulary import mri_protocols


class MRIAnalyzerTool(BaseTool):
    name = "analyze_brain_mri"
    description = (
        "Order and analyze a brain MRI scan. Specify the protocol and whether "
        "contrast (gadolinium) is given. Returns findings with locations, "
        "signal characteristics, volumetrics, and clinical impression. "
        "Note: MRI is slower than CT — for emergency neuroimaging, "
        "use order_ct_scan instead."
    )
    # Catalogue prose rule (4 Nov 2026, docs/benchmark/tool-contract.md): a description says
    # what a study measures and returns, never which disease it is for. The same text is
    # mirrored in review_api/services/tool_io.py.
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context and indication for the MRI.",
            },
            # The enum is derived from costs.yaml so the tool, the cost registry and the
            # benchmark's ground truth cannot drift apart. See tools/vocabulary.py.
            "protocol": {
                "type": "string",
                "enum": mri_protocols(),
                "description": (
                    "MRI protocol to use. 'epilepsy': thin coronal hippocampal cuts (ILAE HARNESS-MRI). "
                    "'stroke': DWI emphasis + MRA. 'tumor': includes perfusion-weighted sequences. "
                    "'ms': sagittal FLAIR + post-contrast T1. 'dementia': volumetric with hippocampal assessment. "
                    "'orbits': fat-suppressed thin coronal and axial sections of the orbits and optic nerves. "
                    "'pituitary': thin sagittal and coronal sections of the sella. "
                    "'standard': general brain screen."
                ),
            },
            "contrast": {
                "type": "boolean",
                # Gadolinium is given on an indication, not by default (ACR Manual on Contrast
                # Media): an order that does not ask for it is a non-contrast study, as the
                # scorer and the cost model already read it (24 Oct 2026).
                "default": False,
                "description": "Whether gadolinium contrast is given.",
            },
        },
        "required": ["clinical_context"],
    }
