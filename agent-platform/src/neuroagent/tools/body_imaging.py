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

import logging
from typing import Any

from .base import BaseTool
from .vocabulary import body_imaging_studies, is_valid_body_imaging_study

logger = logging.getLogger(__name__)


class BodyImagingTool(BaseTool):
    name = "order_body_imaging"
    description = (
        "Image a region OUTSIDE the brain and skull: pelvis/abdomen (occult tumour search, "
        "portosystemic shunts), chest (pulmonary embolism, aortic dissection, an intrathoracic "
        "mass), mediastinum (thymoma), spine (cord compression, myelitis), or peripheral nerve "
        "(nerve root enlargement). Use this when the question is about an organ the brain "
        "imaging tools cannot see — order_ct_scan images the head and neck only. `study` fuses "
        "region and modality because a CT and an MRI of the same region are different studies."
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
                    "Region and modality. 'pelvis_abdomen_CT'/'_MRI'/'_ultrasound': occult "
                    "neoplasm search (ovarian teratoma in anti-NMDAR encephalitis), "
                    "'testicular_ultrasound': age- and sex-adapted germ-cell tumour screening "
                    "in selected male anti-NMDAR cases, "
                    "portosystemic shunts in refractory hepatic encephalopathy. "
                    "'chest_CT': lung parenchyma, mediastinum, an intrathoracic mass. "
                    "'chest_CTA': CT angiography of the thorax — pulmonary embolism, aortic "
                    "dissection, when either has to be confirmed or excluded rapidly. "
                    "'chest_abdomen_pelvis_CT': the staging / occult-primary study in one "
                    "acquisition — a paraneoplastic tumour search, or excluding an extracranial "
                    "primary before calling a lesion a primary brain tumour. "
                    "'mediastinum_CT'/'_MRI': thymic hyperplasia or thymoma in myasthenia "
                    "gravis. 'spine_MRI'/'_CT': cord compression, transverse myelitis, "
                    "spinal tumour — the mimics of an ascending flaccid weakness. "
                    "'peripheral_nerve_MRI'/'_ultrasound': nerve root enhancement, nerve "
                    "enlargement."
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

    def _validate_parameters(self, parameters: dict[str, Any]) -> None:
        """Warn (only) when `study` is outside the closed vocabulary."""
        study = parameters.get("study")
        if isinstance(study, str) and not is_valid_body_imaging_study(study):
            logger.warning(
                "order_body_imaging called with out-of-vocabulary study %r (known: %s). "
                "Proceeding unchanged — fallback output/cost will apply.",
                study,
                ", ".join(body_imaging_studies()),
            )
