"""Tissue acquisition and integrated histomolecular diagnosis.

The most consequential finding of the July 2026 review. Reviewer 2 on high-grade glioma:
"with imaging, blood tests, EEG and ECG the best attainable output is a suspicion, and the
classification itself provides the label for that state — NOS." Every glioma case in the
benchmark was unsolvable by construction, because the entity, the grade and the treatment
branch all follow from tissue and the action space had no way to obtain any.

Two acts, one tool, because they are inseparable in practice: the specimen is worthless if
inadequate for molecular work-up, and the molecular panel is meaningless without a specimen.

* Tissue acquisition — maximal safe resection where feasible, or frame-based/frameless
  stereotactic biopsy where microsurgical resection is not safely feasible. Management
  without a tissue diagnosis is reserved for very exceptional situations (AIOM 2023).
* Integrated diagnosis — a layered report: integrated diagnosis, histological diagnosis, CNS
  WHO grade, molecular findings. Each assay is here because it changes the answer, not to
  complete a taxonomy: IDH separates the two grade 4 entities, 1p/19q separates
  oligodendroglioma from astrocytoma and with it PCV from temozolomide, CDKN2A/B assigns
  grade 4 without any histological feature of malignancy, MGMT decides treatment in elderly
  or frail patients. MGMT must not be assessed by immunocytochemistry (WHO CNS5, Louis 2021).
"""

from __future__ import annotations


from .base import BaseTool
from .vocabulary import (
    molecular_assays,
    tissue_procedures,
)


class TissueDiagnosisTool(BaseTool):
    name = "obtain_tissue_diagnosis"
    description = (
        "Obtain tissue and issue an integrated histopathological diagnosis, with a grade where one "
        "applies. Name the molecular assays you want in `molecular_assays`; each is billed "
        "separately."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication, and the lesion's site and appearance.",
            },
            # Enums derived from costs.yaml (see tools/vocabulary.py).
            "procedure": {
                "type": "string",
                "enum": tissue_procedures(),
                "description": (
                    "How tissue is obtained. 'resection': surgical resection, which is also "
                    "therapeutic. 'stereotactic_biopsy': needle biopsy with serial samples along a "
                    "stereotactic trajectory. 'lymph_node_biopsy': endobronchial needle aspiration "
                    "or surgical nodal sampling. 'temporal_artery_biopsy': a segment of the "
                    "superficial temporal artery. 'open_biopsy': open surgical biopsy through a "
                    "laminectomy or craniotomy, without resection."
                ),
            },
            "site": {
                "type": "string",
                "description": "Anatomical target of the procedure.",
            },
            "molecular_assays": {
                "type": "array",
                "items": {"type": "string", "enum": molecular_assays()},
                "description": (
                    "Assays to run on the specimen. 'IDH1_IHC': IDH1 R132H immunohistochemistry. "
                    "'ATRX_IHC': ATRX nuclear expression. 'IDH1_IDH2_sequencing': IDH1 and IDH2 "
                    "hotspot sequencing. '1p_19q_codeletion': whole-arm 1p/19q codeletion. "
                    "'CDKN2A_B_deletion': homozygous CDKN2A/B deletion. 'TERT_promoter': TERT "
                    "promoter mutation. 'EGFR_amplification': EGFR gene amplification. "
                    "'chr7_gain_chr10_loss': combined gain of chromosome 7 and loss of chromosome "
                    "10. 'H3K27_status': H3 K27M mutation and H3K27me3 loss. 'MGMT_methylation': "
                    "MGMT promoter methylation by PCR, pyrosequencing or array (not "
                    "immunohistochemistry). 'BRAF_V600': BRAF V600E mutation. 'CD20_IHC': B-cell "
                    "lineage. 'EBER_ISH': Epstein-Barr virus-encoded RNA. 'SOX10_IHC' and "
                    "'Melan_A_HMB45_IHC': melanocytic markers. 'chromogranin_A_synaptophysin_IHC': "
                    "neuroendocrine markers. 'PAX8_IHC', 'TTF1_IHC', 'thyroglobulin_IHC': "
                    "epithelial lineage markers (renal or Mullerian, lung, thyroid). "
                    "'H3G34_status': H3 G34 mutation. 'DNA_methylation_profiling': genome-wide DNA "
                    "methylation classification."
                ),
            },
        },
        "required": ["clinical_context", "procedure"],
    }
    vocabulary = {"procedure": tissue_procedures, "molecular_assays": molecular_assays}
    pack_notes = {
        "general_medicine": {
            "": (
                "In general medicine it also covers percutaneous, endoscopic, skin and bone "
                "marrow biopsies."
            ),
            "procedure": (
                "'image_guided_core_biopsy': percutaneous needle biopsy of a liver, lung, bone "
                "or soft-tissue lesion under CT or ultrasound guidance. 'endoscopic_biopsy': "
                "histology of biopsies taken at an endoscopy ordered separately. 'skin_biopsy': "
                "punch biopsy of a skin lesion. 'bone_marrow_biopsy': aspirate and trephine."
            ),
        },
    }
