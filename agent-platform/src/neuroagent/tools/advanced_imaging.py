from __future__ import annotations
from .base import BaseTool
from .vocabulary import advanced_imaging_modalities


class AdvancedImagingTool(BaseTool):
    name = "order_advanced_imaging"
    description = (
        "Order advanced imaging: molecular/PET studies, dopaminergic and cardiac sympathetic "
        "imaging, perfusion (MR or CT), spectroscopy, MR angiography and venography, "
        "ultrasound-based vascular studies, and second-line cardiac imaging beyond the "
        "echocardiogram. Costs vary by more than an order of magnitude — from EUR 230 "
        "(transcranial_doppler) to EUR 4600 (DaTscan) — so choose the modality that answers "
        "the specific question."
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
                    "'FDG_PET': cerebral glucose metabolism (dementia pattern); NOT an "
                    "adequate tracer for a primary brain tumour. 'amino_acid_PET': "
                    "11C-methionine or 18F-FET — separates active tumour from necrosis or "
                    "treatment effect and targets biopsy at the most aggressive area. "
                    "'cardiac_FDG_PET': myocardial inflammation after dietary suppression of "
                    "myocardial glucose uptake — a different study from the brain scan, not "
                    "the same scan read differently. 'DaTscan': dopamine transporter "
                    "(parkinsonian syndromes). 'MIBG_scan': cardiac sympathetic denervation "
                    "(PD vs MSA, Lewy body disease). 'perfusion_MRI': cerebral blood flow and "
                    "rCBV. 'CT_perfusion': core-to-penumbra quantification for tissue-based "
                    "stroke selection outside the standard time window. 'MR_spectroscopy': "
                    "metabolites, including 2-hydroxyglutarate. 'MR_angiography'/"
                    "'MR_venography': arterial / venous sinus imaging. 'cardiac_MRI': "
                    "myocardial tissue characterisation with late gadolinium enhancement — "
                    "infiltrative or arrhythmogenic substrate, myocarditis, fibrosis. "
                    "'coronary_CTA': non-invasive coronary anatomy. 'coronary_angiography': "
                    "invasive catheter study, indicated by suspected myocardial ischaemia; "
                    "an angiographic finding alone does not establish the cause of a symptom. "
                    "'carotid_duplex': carotid stenosis. 'transcranial_doppler': vasospasm."
                ),
            },
        },
        "required": ["clinical_context", "modality"],
    }
    vocabulary = {"modality": advanced_imaging_modalities}
    pack_notes = {
        "general_medicine": {
            "modality": (
                "'VQ_scan': ventilation-perfusion lung scan for pulmonary embolism when CT "
                "angiography is contraindicated. 'HIDA_scan': hepatobiliary scintigraphy for "
                "acute cholecystitis."
            ),
        },
    }
