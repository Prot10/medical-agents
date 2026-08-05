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

import logging
from typing import Any

from .base import BaseTool
from .vocabulary import (
    is_valid_molecular_assay,
    is_valid_tissue_procedure,
    molecular_assays,
    tissue_procedures,
)

logger = logging.getLogger(__name__)


class TissueDiagnosisTool(BaseTool):
    name = "obtain_tissue_diagnosis"
    description = (
        "Obtain tissue and issue an integrated histomolecular diagnosis. This is the only "
        "route to a definitive diagnosis, grade and treatment branch for a brain tumour — "
        "imaging alone yields a suspicion, reported as NOS. Request the molecular assays "
        "that change management; each is billed separately. Molecular work-up must not delay "
        "radiotherapy or tumour-specific pharmacotherapy."
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
                    "feasible; serial samples along the trajectory avoid sampling bias."
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
                    "array — NOT immunocytochemistry); 'BRAF_V600' in IDH-wildtype tumours."
                ),
            },
        },
        "required": ["clinical_context", "procedure"],
    }

    def _validate_parameters(self, parameters: dict[str, Any]) -> None:
        """Warn (only) on out-of-vocabulary procedure or assay."""
        procedure = parameters.get("procedure")
        if isinstance(procedure, str) and not is_valid_tissue_procedure(procedure):
            logger.warning(
                "obtain_tissue_diagnosis called with out-of-vocabulary procedure %r "
                "(known: %s). Proceeding unchanged — fallback output/cost will apply.",
                procedure,
                ", ".join(tissue_procedures()),
            )
        assays = parameters.get("molecular_assays")
        if isinstance(assays, (list, tuple)):
            unknown = [a for a in assays if not is_valid_molecular_assay(str(a))]
            if unknown:
                logger.warning(
                    "obtain_tissue_diagnosis called with %d out-of-vocabulary molecular "
                    "assay(s): %s. Proceeding unchanged — default rate applies and no "
                    "optimal action can match them.",
                    len(unknown),
                    ", ".join(repr(u) for u in unknown),
                )
