"""Tool output Pydantic models for diagnostic results."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel


class EEGFinding(BaseModel):
    type: str  # e.g., "sharp_wave", "slowing", "periodic_discharge"
    location: str  # e.g., "F8/T4, right anterior temporal"
    frequency: str = ""
    morphology: str = ""
    state: str = ""  # awake, sleep, etc.
    clinical_correlation: str = ""


class EEGReport(BaseModel):
    classification: Literal["normal", "abnormal"]
    background: dict[str, str] = {}  # pdr, sleep_features, overall
    findings: list[EEGFinding] = []
    artifacts: list[dict[str, str]] = []
    activating_procedures: dict[str, str] = {}
    impression: str
    limitations: str = ""
    recommended_actions: list[str] = []


class MRIFinding(BaseModel):
    type: str  # e.g., "mass_lesion", "atrophy", "white_matter_lesion"
    location: str
    size: str | None = None
    signal_characteristics: dict[str, str] = {}  # T1, T2, FLAIR, DWI, contrast
    mass_effect: str | None = None
    borders: str | None = None


class MRIReport(BaseModel):
    findings: list[MRIFinding] = []
    volumetrics: dict[str, str] | None = None
    additional_observations: list[str] = []
    impression: str
    # `differential_by_imaging` was removed: the structured `{diagnosis, rationale}`
    # list was naming the gold-truth diagnosis as its first entry in ~82% of cases
    # (audit finding) — real radiologists embed any differential considerations in
    # impression prose, not in a typed list. The field has been emptied across all
    # 104 affected v5 cases.
    recommended_actions: list[str] = []


class LabValue(BaseModel):
    test: str
    value: float | str
    unit: str
    reference_range: str
    is_abnormal: bool
    clinical_significance: str | None = None


class LabResults(BaseModel):
    panels: dict[str, list[LabValue]] = {}  # keyed by panel name
    interpretation: str
    abnormal_values_summary: list[str] = []


class CSFResults(BaseModel):
    appearance: str
    opening_pressure: str
    cell_count: dict[str, str] = {}
    protein: str
    glucose: str
    glucose_ratio: str = ""
    special_tests: dict[str, str] = {}
    interpretation: str


class ECGReport(BaseModel):
    rhythm: str
    rate: int
    intervals: dict[str, str] = {}
    axis: str = ""
    findings: list[str] = []
    interpretation: str
    # `clinical_correlation` was removed: 2/602 populated (0.3%) and not a
    # field real ECG reports carry. Cardiologists put any correlation language
    # in `interpretation` prose.


class LiteratureSearchResult(BaseModel):
    query: str
    results: list[dict[str, str]] = []  # source, finding, evidence_level
    summary: str


class DrugInteractionResult(BaseModel):
    proposed: str = ""
    interactions: list[str] = []
    contraindications: list[str] = []
    warnings: list[str] = []
    formulary_status: str = ""
    alternatives: list[str] = []
    summary: str = ""  # free-text pharmacology/interaction review, when not field-structured


# -------------------------------------------------------------------
# New output models for expanded tool set (v4)
# -------------------------------------------------------------------


class CTFinding(BaseModel):
    type: str  # e.g., "hemorrhage", "mass", "infarct", "fracture"
    location: str
    size: str | None = None
    density: str | None = None  # hyperdense, hypodense, isodense
    description: str = ""


class CTReport(BaseModel):
    findings: list[CTFinding] = []
    contrast_used: bool = False
    angiography_findings: dict[str, str] | None = None  # vessel, stenosis, occlusion
    additional_observations: list[str] = []
    impression: str
    recommended_actions: list[str] = []


class EchoReport(BaseModel):
    chambers: dict[str, str] = {}  # LV, RV, LA, RA dimensions and function
    valves: dict[str, str] = {}  # mitral, aortic, tricuspid, pulmonic
    ejection_fraction: float | None = None
    wall_motion: str | None = None
    findings: list[str] = []
    impression: str
    recommended_actions: list[str] = []


class CardiacMonitoringReport(BaseModel):
    duration_hours: int = 0
    monitor_type: str = ""  # holter_24h, event_monitor_30d, telemetry
    rhythm_summary: str = ""
    heart_rate_range: dict[str, int] = {}  # min, max, average
    events: list[dict[str, str]] = []  # timestamp, type, duration, description
    findings: list[str] = []
    impression: str = ""
    recommended_actions: list[str] = []


class AdvancedImagingReport(BaseModel):
    modality: str = ""  # amyloid_PET, FDG_PET, DaTscan, perfusion_MRI, MR_spectroscopy, carotid_duplex
    tracer_or_protocol: str | None = None
    findings: list[dict[str, str]] = []  # region, uptake/signal, interpretation
    quantitative_data: dict[str, str] | None = None  # SUV, ratios, etc.
    impression: str = ""
    recommended_actions: list[str] = []


class SpecializedTestReport(BaseModel):
    test_type: str = ""  # neuropsych_battery, emg_ncs, vep, ssep, baep, tilt_table, etc.
    findings: list[dict[str, str]] = []
    quantitative_data: dict[str, str] | None = None  # scores, latencies, etc.
    impression: str = ""
    recommended_actions: list[str] = []


