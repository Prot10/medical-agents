from __future__ import annotations

import logging
from typing import Any

from .base import BaseTool
from .vocabulary import is_valid_mri_protocol, mri_protocols

logger = logging.getLogger(__name__)


class MRIAnalyzerTool(BaseTool):
    name = "analyze_brain_mri"
    description = (
        "Order and analyze a brain MRI scan. Specify the clinical protocol "
        "(standard, epilepsy, stroke, tumor, ms, dementia) and whether "
        "contrast (gadolinium) is needed. Returns findings with locations, "
        "signal characteristics, volumetrics, and clinical impression. "
        "Note: MRI is slower than CT — for emergency hemorrhage exclusion, "
        "use order_ct_scan instead."
    )
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
                    "'standard': general brain screen."
                ),
            },
            "contrast": {
                "type": "boolean",
                "description": "Whether gadolinium contrast is needed (e.g., for tumor, MS, infection).",
            },
        },
        "required": ["clinical_context"],
    }

    def _validate_parameters(self, parameters: dict[str, Any]) -> None:
        """Warn (only) when `protocol` is outside the closed vocabulary."""
        protocol = parameters.get("protocol")
        if isinstance(protocol, str) and not is_valid_mri_protocol(protocol):
            logger.warning(
                "analyze_brain_mri called with out-of-vocabulary protocol %r (known: %s). "
                "Proceeding unchanged — the protocol does not change billing, but no "
                "optimal action pinning a protocol can match.",
                protocol,
                ", ".join(mri_protocols()),
            )
