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
        "Obtain tissue and issue an integrated histopathological diagnosis. For a brain "
        "tumour this is the only route to a definitive diagnosis, grade and treatment branch — "
        "imaging alone yields a suspicion, reported as NOS. It also covers nodal sampling when "
        "a systemic disease has to be confirmed histologically outside the organ that is "
        "symptomatic. Request the molecular assays that change management; each is billed "
        "separately, and a purely histological pattern needs none. Molecular work-up must not "
        "delay radiotherapy or tumour-specific pharmacotherapy."
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
                    "How tissue is obtained. 'resection': maximal safe resection where "
                    "feasible given site and clinical condition; also therapeutic. "
                    "'stereotactic_biopsy': where microsurgical resection is not safely "
                    "feasible; serial samples along the trajectory avoid sampling bias. "
                    "'lymph_node_biopsy': endobronchial needle aspiration or surgical nodal "
                    "sampling — the low-risk route to histological confirmation of a systemic "
                    "disease when the accessible node is not the symptomatic organ. "
                    "'temporal_artery_biopsy': a segment of the superficial temporal artery, "
                    "the histological test for giant cell arteritis."
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
                    "Assays to run on the specimen. 'IDH1_IHC' and 'ATRX_IHC' routinely; "
                    "'IDH1_IDH2_sequencing' where IHC is negative, in grade 2-3 diffuse "
                    "gliomas and in glioblastoma under 55 years; '1p_19q_codeletion' in "
                    "IDH-mutant gliomas with retained ATRX; 'CDKN2A_B_deletion' in "
                    "IDH-mutant astrocytomas; 'TERT_promoter', 'EGFR_amplification', "
                    "'chr7_gain_chr10_loss' in IDH-wildtype astrocytic gliomas lacking "
                    "microvascular proliferation and necrosis; 'H3K27_status' for midline "
                    "tumours; 'MGMT_methylation' in glioblastoma (by PCR, pyrosequencing or "
                    "array — NOT immunocytochemistry); 'BRAF_V600' in IDH-wildtype tumours. "
                    "'CD20_IHC' and 'EBER_ISH': B-cell lineage and Epstein-Barr virus in a suspected "
                    "primary CNS or EBV-associated lymphoma. 'SOX10_IHC' and 'Melan_A_HMB45_IHC': "
                    "melanocytic markers, to exclude a metastatic melanoma."
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
