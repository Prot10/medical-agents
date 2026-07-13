from __future__ import annotations
import logging
from typing import Any
from .base import BaseTool
from .vocabulary import advanced_imaging_modalities, is_valid_modality

logger = logging.getLogger(__name__)


class AdvancedImagingTool(BaseTool):
    name = "order_advanced_imaging"
    description = (
        "Order advanced neuroimaging studies including PET scans, DaTscan, "
        "MR perfusion/spectroscopy/angiography/venography, cardiac MIBG, "
        "transcranial doppler, and carotid duplex ultrasound. "
        "Costs vary widely: DaTscan (~$5,000), amyloid_PET (~$4,000), "
        "FDG_PET (~$2,000), perfusion_MRI / MR_spectroscopy (~$500), "
        "carotid_duplex (~$350)."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the advanced imaging study.",
            },
            # The enum is derived from costs.yaml so the tool, the cost registry and the
            # benchmark's ground truth cannot drift apart. See tools/vocabulary.py.
            "modality": {
                "type": "string",
                "enum": advanced_imaging_modalities(),
                "description": (
                    "Imaging modality. 'amyloid_PET'/'tau_PET': Alzheimer biomarkers. "
                    "'FDG_PET': glucose metabolism (dementia pattern, tumor grading). "
                    "'DaTscan': dopamine transporter (parkinsonian syndromes). "
                    "'MIBG_scan': cardiac sympathetic denervation (PD vs MSA). "
                    "'perfusion_MRI': cerebral blood flow. 'MR_spectroscopy': metabolites. "
                    "'MR_angiography'/'MR_venography': arterial / venous sinus imaging. "
                    "'carotid_duplex': carotid stenosis. 'transcranial_doppler': vasospasm."
                ),
            },
        },
        "required": ["clinical_context", "modality"],
    }

    def _validate_parameters(self, parameters: dict[str, Any]) -> None:
        """Warn (only) when `modality` is outside the closed vocabulary.

        Out-of-vocabulary values silently get the off-pathway fallback output
        and the default cost tier; that behavior is intentionally preserved
        (changing it would change agent behavior mid-benchmark), but it must
        be visible in the logs.
        """
        modality = parameters.get("modality")
        if isinstance(modality, str) and not is_valid_modality(modality):
            logger.warning(
                "order_advanced_imaging called with out-of-vocabulary modality %r "
                "(known: %s). Proceeding unchanged — fallback output/cost will apply.",
                modality,
                ", ".join(advanced_imaging_modalities()),
            )
