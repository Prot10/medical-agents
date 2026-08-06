from __future__ import annotations
import logging
from typing import Any
from .base import BaseTool
from .vocabulary import advanced_imaging_modalities, is_valid_modality

logger = logging.getLogger(__name__)


class AdvancedImagingTool(BaseTool):
    name = "order_advanced_imaging"
    description = (
        "Order advanced neuroimaging: molecular/PET studies, dopaminergic and cardiac "
        "sympathetic imaging, perfusion (MR or CT), spectroscopy, MR angiography and "
        "venography, and ultrasound-based vascular studies. Costs vary by more than an "
        "order of magnitude — from EUR 230 (transcranial_doppler) to EUR 4600 (DaTscan) — "
        "so choose the modality that answers the specific question."
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
                    "'FDG_PET': glucose metabolism (dementia pattern); NOT an adequate "
                    "tracer for a primary brain tumour. 'amino_acid_PET': 11C-methionine or "
                    "18F-FET — separates active tumour from necrosis or treatment effect and "
                    "targets biopsy at the most aggressive area. 'DaTscan': dopamine "
                    "transporter (parkinsonian syndromes). 'MIBG_scan': cardiac sympathetic "
                    "denervation (PD vs MSA, Lewy body disease). 'perfusion_MRI': cerebral "
                    "blood flow and rCBV. 'CT_perfusion': core-to-penumbra quantification "
                    "for tissue-based stroke selection outside the standard time window. "
                    "'MR_spectroscopy': metabolites, including 2-hydroxyglutarate. "
                    "'MR_angiography'/'MR_venography': arterial / venous sinus imaging. "
                    "'cardiac_MRI': myocardial tissue characterisation with late gadolinium "
                    "enhancement. 'carotid_duplex': carotid stenosis. "
                    "'transcranial_doppler': vasospasm."
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
