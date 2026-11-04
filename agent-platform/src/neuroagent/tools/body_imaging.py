"""Cross-sectional imaging outside the central nervous system.

The July 2026 clinical tool review found the action space could image the brain and nothing
else. Four of the reviewers' twelve requests were the same gap in different organs:

* anti-NMDAR encephalitis — pelvic/abdominal imaging for an ovarian teratoma. Described as a
  required step once the syndrome is recognised, independent of antibody confirmation, and a
  missed tumour is a missed treatable cause (Graus 2016; Titulaer 2013).
* myasthenia gravis — CT or MRI of the anterior mediastinum in every newly diagnosed
  patient, irrespective of distribution or serostatus. A chest radiograph does not
  substitute (Jacob 2025).
* Guillain-Barré — whole-spine MRI to exclude cord compression, the one mimic that is both
  common and time-critical, and previously unreachable in the action space (EAN/PNS 2023).
* hepatic encephalopathy — portal-venous abdominal imaging for spontaneous portosystemic
  shunts, found in a large majority of encephalopathy refractory to medical therapy
  (ACG 2026).
"""

from __future__ import annotations


from .base import BaseTool
from .vocabulary import body_imaging_studies


class BodyImagingTool(BaseTool):
    name = "order_body_imaging"
    description = (
        "Image a region OUTSIDE the brain and skull: pelvis and abdomen, testes, chest, "
        "mediastinum, spine, peripheral nerves, leg veins and temporal arteries, by CT, MRI, "
        "ultrasound or radiograph. Use this when the question is about an organ the brain imaging "
        "tools cannot see — order_ct_scan images the head and neck only. `study` fuses region and "
        "modality because a CT and an MRI of the same region are different studies."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the study.",
            },
            # Enum derived from costs.yaml (see tools/vocabulary.py).
            "study": {
                "type": "string",
                "enum": body_imaging_studies(),
                "description": (
                    "Region and modality. 'pelvis_abdomen_CT'/'_MRI'/'_ultrasound': the abdominal "
                    "and pelvic organs and vessels. 'testicular_ultrasound': scrotal ultrasound of "
                    "both testes. 'chest_CT': lung parenchyma, pleura and mediastinum. "
                    "'chest_CTA': CT angiography of the pulmonary arteries and the thoracic aorta. "
                    "'chest_abdomen_pelvis_CT': chest, abdomen and pelvis in one acquisition. "
                    "'mediastinum_CT'/'_MRI': dedicated mediastinal imaging. 'spine_MRI'/'_CT': "
                    "spinal cord, nerve roots, vertebrae and epidural space. "
                    "'peripheral_nerve_MRI'/'_ultrasound': calibre, signal and enhancement of "
                    "nerve roots, plexus and peripheral nerves. 'lower_extremity_venous_duplex': "
                    "compression and Doppler ultrasound of the leg veins. 'chest_xray': two-view "
                    "chest radiograph. 'temporal_artery_ultrasound': wall thickness and lumen of "
                    "the superficial temporal arteries."
                ),
            },
            "contrast": {
                "type": "boolean",
                "description": "Whether IV contrast is needed.",
                "default": False,
            },
        },
        "required": ["clinical_context", "study"],
    }
    vocabulary = {"study": body_imaging_studies}
    pack_notes = {
        "general_medicine": {
            "study": (
                "'abdomen_xray', 'extremity_xray': plain radiographs, the first-line image of "
                "the abdomen (obstruction, free air) and a limb. "
                "'hepatobiliary_ultrasound': gallbladder and bile ducts. 'renal_ultrasound': "
                "hydronephrosis, kidney size. 'neck_ultrasound': thyroid and cervical nodes."
            ),
        },
    }
