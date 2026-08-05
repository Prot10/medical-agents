"""Enumeration types for the neuroagent-schemas package."""

from enum import Enum


class NeurologicalCondition(str, Enum):
    FOCAL_EPILEPSY_TEMPORAL = "focal_epilepsy_temporal"
    FOCAL_EPILEPSY_FRONTAL = "focal_epilepsy_frontal"
    GENERALIZED_EPILEPSY = "generalized_epilepsy"
    ALZHEIMERS_EARLY = "alzheimers_early"
    ALZHEIMERS_MODERATE = "alzheimers_moderate"
    ISCHEMIC_STROKE = "ischemic_stroke"
    HEMORRHAGIC_STROKE = "hemorrhagic_stroke"
    TIA = "tia"
    MULTIPLE_SCLEROSIS = "multiple_sclerosis"
    PARKINSONS = "parkinsons"
    MIGRAINE_WITH_AURA = "migraine_with_aura"
    MIGRAINE_WITHOUT_AURA = "migraine_without_aura"
    BACTERIAL_MENINGITIS = "bacterial_meningitis"
    VIRAL_ENCEPHALITIS = "viral_encephalitis"
    AUTOIMMUNE_ENCEPHALITIS_NMDAR = "autoimmune_encephalitis_nmdar"
    AUTOIMMUNE_ENCEPHALITIS_LGI1 = "autoimmune_encephalitis_lgi1"
    BRAIN_TUMOR_GLIOMA = "brain_tumor_glioma"
    BRAIN_TUMOR_MENINGIOMA = "brain_tumor_meningioma"
    BRAIN_TUMOR_METASTASIS = "brain_tumor_metastasis"
    FTD = "ftd"
    NPH = "nph"
    MYASTHENIA_GRAVIS = "myasthenia_gravis"
    PERIPHERAL_NEUROPATHY = "peripheral_neuropathy"
    SYNCOPE_CARDIAC = "syncope_cardiac"
    SYNCOPE_VASOVAGAL = "syncope_vasovagal"
    CJD = "cjd"
    CADASIL = "cadasil"
    NEUROSARCOIDOSIS = "neurosarcoidosis"
    STATUS_EPILEPTICUS = "status_epilepticus"
    GUILLAIN_BARRE = "guillain_barre"
    SUBARACHNOID_HEMORRHAGE = "subarachnoid_hemorrhage"
    HEPATIC_ENCEPHALOPATHY = "hepatic_encephalopathy"
    ALS = "als"
    ATYPICAL_PARKINSONISM_MSA = "atypical_parkinsonism_msa"
    ATYPICAL_PARKINSONISM_PSP = "atypical_parkinsonism_psp"
    FUNCTIONAL_NEUROLOGICAL_DISORDER = "functional_neurological_disorder"
    # Added for the 23-condition set agreed with the clinical reviewers, 2026-08-05.
    # HEMORRHAGIC_STROKE and VIRAL_ENCEPHALITIS above were already defined but unused; they
    # now carry spontaneous intracerebral haemorrhage and HSV encephalitis respectively. The
    # keys are deliberately not renamed: five hospital_rules trigger lists match
    # "hemorrhagic_stroke" as a literal, and the clinical identity lives in the
    # conditions.yaml `name` and the UI label — the same split as ftd /
    # frontotemporal_dementia and als / amyotrophic_lateral_sclerosis.
    VASCULAR_DEMENTIA = "vascular_dementia"
    DEMENTIA_WITH_LEWY_BODIES = "dementia_with_lewy_bodies"


class CaseDifficulty(str, Enum):
    STRAIGHTFORWARD = "straightforward"
    MODERATE = "moderate"
    DIAGNOSTIC_PUZZLE = "diagnostic_puzzle"


class ActionCategory(str, Enum):
    """Tier of a step in `optimal_actions`.

    - REQUIRED: must be performed; missing it incurs a recall penalty.
    - RECOMMENDED: expected workup hygiene; helpful but not penalized if skipped.
    - OPTIONAL: defensible if performed, not penalized in either direction.

    Contraindicated / harmful tool calls do NOT live in optimal_actions. Use
    `GroundTruth.harmful_tools` (structured) or `GroundTruth.contraindicated_actions`
    (free-text) instead.
    """

    REQUIRED = "required"
    RECOMMENDED = "recommended"
    OPTIONAL = "optional"


class Likelihood(str, Enum):
    """Likelihood scale for entries in `GroundTruth.differential`."""

    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class SequenceSeverity(str, Enum):
    """How strict an entry in `GroundTruth.sequence_constraints` is.

    - SOFT: ordering matters for workflow quality; violation penalizes efficiency.
    - HARD: ordering is a safety constraint; violation is a safety event
      (e.g., LP before imaging in suspected mass effect → herniation risk).
    """

    SOFT = "soft"
    HARD = "hard"


class EncounterType(str, Enum):
    EMERGENCY = "emergency"
    INPATIENT = "inpatient"
    OUTPATIENT = "outpatient"
