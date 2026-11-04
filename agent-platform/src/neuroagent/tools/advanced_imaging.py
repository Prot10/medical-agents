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
        "(transcranial_doppler) to EUR 4600 (DaTscan) — so choose the modality that answers the "
        "specific question."
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
                    "Imaging modality. 'amyloid_PET'/'tau_PET': cerebral amyloid / tau deposition. "
                    "'FDG_PET': cerebral glucose metabolism; normal grey matter takes up FDG "
                    "avidly. 'amino_acid_PET': 11C-methionine or 18F-FET — amino-acid transport, "
                    "low in normal cortex. 'cardiac_FDG_PET': myocardial FDG uptake after dietary "
                    "suppression of myocardial glucose uptake — a different study from the brain "
                    "scan, not the same scan read differently. 'DaTscan': striatal dopamine "
                    "transporter binding. 'MIBG_scan': cardiac sympathetic (postganglionic) "
                    "innervation, as the heart-to-mediastinum ratio. 'perfusion_MRI': cerebral "
                    "blood flow and rCBV. 'CT_perfusion': cerebral blood flow, blood volume and "
                    "transit-time maps, with automated volumes of reduced flow. 'MR_spectroscopy': "
                    "the brain metabolite spectrum (NAA, choline, creatine, lactate, lipids, "
                    "myo-inositol). 'MR_angiography'/'MR_venography': arterial / venous sinus "
                    "imaging. 'cardiac_MRI': cardiac function and myocardial tissue "
                    "characterisation, with T1/T2 mapping and late gadolinium enhancement. "
                    "'coronary_CTA': non-invasive coronary anatomy. 'coronary_angiography': "
                    "invasive catheter coronary angiography; an angiographic finding alone does "
                    "not establish the cause of a symptom. 'carotid_duplex': extracranial carotid "
                    "and vertebral flow velocities and plaque. 'transcranial_doppler': "
                    "intracranial arterial flow velocities. 'functional_MRI': BOLD motor and "
                    "language mapping and hemispheric language lateralisation. 'DTI_tractography': "
                    "diffusion tractography of the corticospinal tract, arcuate fasciculus and "
                    "optic radiations. 'whole_body_FDG_PET': whole-body 18F-FDG PET/CT, skull base "
                    "to mid-thigh (a different acquisition from the cerebral 'FDG_PET')."
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
