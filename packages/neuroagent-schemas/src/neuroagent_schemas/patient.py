"""Patient-related Pydantic models."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class Demographics(BaseModel):
    age: int = Field(ge=18, le=90)
    sex: Literal["male", "female"]
    handedness: str = "right"
    ethnicity: str = ""
    bmi: float | None = None


class Medication(BaseModel):
    drug: str
    dose: str
    frequency: str
    indication: str


class ClinicalHistory(BaseModel):
    past_medical_history: list[str] = []
    medications: list[Medication] = []
    allergies: list[str] = []
    family_history: list[str] = []
    social_history: dict[str, str] = {}


class NeurologicalExam(BaseModel):
    mental_status: str = ""
    cranial_nerves: str = ""
    motor: str = ""
    sensory: str = ""
    reflexes: str = ""
    coordination: str = ""
    gait: str = ""
    additional: str | None = None


class Vitals(BaseModel):
    # Every NeuroBench case records all six. A recorded case may not (MIMIC-IV-ED triage leaves
    # some blank), and a missing vital is reported as missing, never filled with a normal value.
    bp_systolic: int | None = None
    bp_diastolic: int | None = None
    hr: int | None = None
    temp: float | None = None
    rr: int | None = None
    spo2: int | None = None


class PatientProfile(BaseModel):
    patient_id: str
    demographics: Demographics
    clinical_history: ClinicalHistory
    # Every NeuroBench case has one. A general-medicine case may leave it empty and carry its
    # neurological findings, if any, as the `neurological` system of `physical_exam`.
    neurological_exam: NeurologicalExam = NeurologicalExam()
    # General physical exam findings, keyed by system (general, chest, abdomen, etc.).
    # Empty in most NeuroBench cases; populated for inpatient/ICU presentations (e.g., bulbar
    # MG crisis, MG-RM15) where non-neurological physical findings are diagnostically
    # relevant, and the whole examination of a general-medicine case. The `neurological` key,
    # when present alongside `neurological_exam`, is the same content in a different
    # free-text framing.
    physical_exam: dict[str, str] = {}
    vitals: Vitals
    chief_complaint: str
    history_present_illness: str
