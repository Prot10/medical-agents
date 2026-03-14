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
    ATYPICAL_PARKINSONISM_MSA = "atypical_parkinsonism_msa"
    ATYPICAL_PARKINSONISM_PSP = "atypical_parkinsonism_psp"
    FUNCTIONAL_NEUROLOGICAL_DISORDER = "functional_neurological_disorder"


class Modality(str, Enum):
    EEG = "eeg"
    MRI = "mri"
    FMRI = "fmri"
    ECG = "ecg"
    LABS = "labs"
    CSF = "csf"
    EMG_NCS = "emg_ncs"
    CLINICAL_HISTORY = "clinical_history"


class CaseDifficulty(str, Enum):
    STRAIGHTFORWARD = "straightforward"
    MODERATE = "moderate"
    DIAGNOSTIC_PUZZLE = "diagnostic_puzzle"


class ActionCategory(str, Enum):
    REQUIRED = "required"
    ACCEPTABLE = "acceptable"
    CONTRAINDICATED = "contraindicated"


class EncounterType(str, Enum):
    EMERGENCY = "emergency"
    INPATIENT = "inpatient"
    OUTPATIENT = "outpatient"
