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
    bp_systolic: int
    bp_diastolic: int
    hr: int
    temp: float
    rr: int
    spo2: int


class PatientProfile(BaseModel):
    patient_id: str
    demographics: Demographics
    clinical_history: ClinicalHistory
    neurological_exam: NeurologicalExam
    vitals: Vitals
    chief_complaint: str
    history_present_illness: str
