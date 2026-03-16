# Patient Data & Case Structure

This document describes the complete data model for patient information in NeuroAgent: how patients are represented, what a NeuroBench case contains, how ground truth is structured, and how longitudinal memory works.

All models are defined as Pydantic v2 `BaseModel` subclasses in the `neuroagent-schemas` package (`packages/neuroagent-schemas/src/neuroagent_schemas/`).

---

## 1. Patient Profile

**Schema**: `neuroagent_schemas.patient.PatientProfile`

The `PatientProfile` is the core clinical representation of a patient at presentation time. It contains everything the agent sees before requesting any diagnostic tests.

```
PatientProfile
├── patient_id          (string)
├── demographics        (Demographics)
├── clinical_history    (ClinicalHistory)
│   ├── past_medical_history    (string[])
│   ├── medications             (Medication[])
│   ├── allergies               (string[])
│   ├── family_history          (string[])
│   └── social_history          (dict[str, str])
├── neurological_exam   (NeurologicalExam)
├── vitals              (Vitals)
├── chief_complaint     (string)
└── history_present_illness     (string)
```

### 1.1 Demographics

| Field | Type | Constraints | Description |
|---|---|---|---|
| `age` | int | 18–90 | Patient age in years. |
| `sex` | `"male"` \| `"female"` | — | Biological sex. |
| `handedness` | string | default: `"right"` | Handedness (relevant for lateralization in epilepsy/stroke). |
| `ethnicity` | string | default: `""` | Self-reported ethnicity (e.g., "East Asian", "Caucasian", "Hispanic"). |
| `bmi` | float \| null | optional | Body mass index, when clinically relevant. |

### 1.2 Clinical History

#### Past Medical History (`past_medical_history: list[str]`)

Free-text list of prior conditions with relevant context. Each entry is a self-contained statement:

```json
[
  "Type 2 diabetes mellitus (10 years, on metformin, last HbA1c 7.2%)",
  "Hypertension (15 years, on lisinopril 20 mg)",
  "Hyperlipidemia (on atorvastatin 40 mg)",
  "Remote history of left MCA TIA (3 years ago, full recovery)"
]
```

#### Medications (`medications: list[Medication]`)

Active medication list. Each entry is a structured `Medication` object:

| Field | Type | Description |
|---|---|---|
| `drug` | string | Medication name (generic or brand). |
| `dose` | string | Dose with units (e.g., `"5 mg"`, `"100 mg per actuation"`). |
| `frequency` | string | Dosing schedule (e.g., `"once daily"`, `"twice daily"`, `"as needed"`). |
| `indication` | string | Reason for the medication (e.g., `"hypertension"`, `"seizure prophylaxis"`). |

```json
{
  "drug": "Levetiracetam",
  "dose": "500 mg",
  "frequency": "twice daily",
  "indication": "seizure prophylaxis"
}
```

#### Allergies (`allergies: list[str]`)

Drug allergies with reaction type:

```json
["Penicillin (rash)", "Sulfonamides (anaphylaxis)"]
```

#### Family History (`family_history: list[str]`)

Family members and their neurological/relevant conditions:

```json
[
  "Mother: Alzheimer's disease (diagnosed age 72)",
  "Father: Type 2 diabetes, hypertension, deceased age 68 from myocardial infarction",
  "Maternal uncle: epilepsy (unknown type)"
]
```

#### Social History (`social_history: dict[str, str]`)

Standardized keys covering lifestyle and functional status:

| Key | Description | Example values |
|---|---|---|
| `occupation` | Current employment | `"Retired teacher"`, `"Software engineer"` |
| `education` | Education level | `"Master's degree"`, `"High school diploma"` |
| `living_situation` | Home environment | `"Lives alone in apartment"`, `"With spouse"` |
| `tobacco` | Smoking status | `"Never smoker"`, `"Former smoker (quit 10 years ago, 20 pack-year history)"` |
| `alcohol` | Consumption level | `"Social drinker (2-3 drinks/week)"`, `"None"` |
| `recreational_drugs` | Substance use | `"Denies"`, `"Remote marijuana use in college"` |
| `exercise` | Activity level | `"Walks 30 minutes daily"`, `"Sedentary"` |
| `driving` | Driving status | `"Active driver"`, `"Stopped driving 6 months ago due to episodes"` |

### 1.3 Neurological Exam

**Schema**: `neuroagent_schemas.patient.NeurologicalExam`

A structured neurological examination with 7 standard domains plus an optional `additional` field for findings that don't fit neatly into the standard categories.

| Field | Type | Description |
|---|---|---|
| `mental_status` | string | Level of consciousness, orientation, attention, memory, language, cognitive screening scores (MMSE, MoCA). |
| `cranial_nerves` | string | CN II–XII assessment: visual fields, pupillary responses, extraocular movements, facial sensation/motor, hearing, palate, tongue, etc. |
| `motor` | string | Strength (MRC grading), tone (normal/spastic/rigid/flaccid), bulk, tremor, pronator drift. |
| `sensory` | string | Light touch, pinprick, temperature, vibration, proprioception, graphesthesia, stereognosis. |
| `reflexes` | string | Deep tendon reflexes (biceps, triceps, brachioradialis, patellar, Achilles) with grading, plantar response (Babinski). |
| `coordination` | string | Finger-to-nose, heel-to-shin, rapid alternating movements, dysmetria. |
| `gait` | string | Gait quality, base width, arm swing, Romberg sign, tandem walking. |
| `additional` | string \| null | Specialized findings: primitive reflexes (grasp, palmomental), optic ataxia, environmental agnosia, myoclonus, etc. |

Example `mental_status`:
```
"Alert and oriented x3. MoCA 18/30 (lost points: 5-word recall 0/5, serial 7s 1/5, clock drawing abnormal, abstraction 0/2). Fluent speech with occasional word-finding pauses. Intact repetition and comprehension."
```

### 1.4 Vitals

**Schema**: `neuroagent_schemas.patient.Vitals`

| Field | Type | Unit | Description |
|---|---|---|---|
| `bp_systolic` | int | mmHg | Systolic blood pressure. |
| `bp_diastolic` | int | mmHg | Diastolic blood pressure. |
| `hr` | int | bpm | Heart rate. |
| `temp` | float | °C | Body temperature. |
| `rr` | int | breaths/min | Respiratory rate. |
| `spo2` | int | % | Oxygen saturation. |

### 1.5 Chief Complaint & HPI

| Field | Type | Description |
|---|---|---|
| `chief_complaint` | string | One-line presenting symptom, as reported by the patient. |
| `history_present_illness` | string | Multi-paragraph narrative of the current illness: onset, duration, progression, associated symptoms, relevant positives and negatives. |

The `history_present_illness` is typically the richest text field. It reads like a clinical note and provides the agent's primary input for forming an initial differential:

```
"68-year-old right-handed man presenting with 18-month progressive memory loss. Wife reports increasing difficulty remembering recent conversations, misplacing objects, and getting lost in familiar places. Initially attributed to normal aging, but symptoms have accelerated over the past 6 months. He has missed bill payments and left the stove on twice. No hallucinations, personality changes, or motor symptoms. No incontinence or gait difficulties..."
```

---

## 2. NeuroBench Case

**Schema**: `neuroagent_schemas.case.NeuroBenchCase`

A complete benchmark case bundles the patient profile with pre-generated tool outputs, evaluation criteria, and metadata. This is the fundamental unit of the NeuroBench dataset.

```
NeuroBenchCase
├── case_id                 (string)
├── condition               (NeurologicalCondition enum)
├── difficulty              (CaseDifficulty enum)
├── encounter_type          (EncounterType enum)
├── patient                 (PatientProfile)
├── initial_tool_outputs    (ToolOutputSet)
├── followup_outputs        (FollowUpToolOutput[])
├── ground_truth            (GroundTruth)
└── metadata                (dict)
```

### 2.1 Case Identification

**`case_id`** follows a structured naming convention:

```
{CONDITION_ABBREV}-{DIFFICULTY_CODE}{NUMBER}
```

| Component | V1 (synthetic) | V2 (real-case-seeded) |
|---|---|---|
| Condition | `ALZ-EARLY`, `ISCH-STR`, `FEPI-TEMP`, etc. | Same abbreviations |
| Difficulty | `S` = straightforward, `M` = moderate, `P` = diagnostic puzzle | `RS`, `RM`, `RP` (prefixed with R) |
| Number | 01, 02, 03 | 01, 02, 03 |

Examples: `ALZ-EARLY-P01`, `ISCH-STR-S03`, `FEPI-TEMP-RM02`

### 2.2 Enumerations

#### NeurologicalCondition (32 conditions)

Organized by clinical domain:

| Domain | Conditions |
|---|---|
| **Epilepsy** | `focal_epilepsy_temporal`, `focal_epilepsy_frontal`, `generalized_epilepsy`, `status_epilepticus` |
| **Dementia** | `alzheimers_early`, `alzheimers_moderate`, `ftd`, `nph`, `cjd` |
| **Cerebrovascular** | `ischemic_stroke`, `hemorrhagic_stroke`, `tia`, `cadasil` |
| **Movement Disorders** | `parkinsons`, `atypical_parkinsonism_msa`, `atypical_parkinsonism_psp` |
| **Neuroimmunology** | `multiple_sclerosis`, `autoimmune_encephalitis_nmdar`, `autoimmune_encephalitis_lgi1`, `myasthenia_gravis`, `neurosarcoidosis` |
| **Infections** | `bacterial_meningitis`, `viral_encephalitis` |
| **Neuro-oncology** | `brain_tumor_glioma`, `brain_tumor_meningioma`, `brain_tumor_metastasis` |
| **Headache** | `migraine_with_aura`, `migraine_without_aura` |
| **Syncope** | `syncope_cardiac`, `syncope_vasovagal` |
| **Peripheral** | `peripheral_neuropathy` |
| **Functional** | `functional_neurological_disorder` |

#### CaseDifficulty

| Level | Description |
|---|---|
| `straightforward` | Classic textbook presentation. Clear findings, minimal ambiguity. |
| `moderate` | Some atypical features, conflicting data, or comorbidities. |
| `diagnostic_puzzle` | Intentional distractors (red herrings), rare presentations, overlapping syndromes. |

#### EncounterType

| Type | Typical scenario |
|---|---|
| `emergency` | Acute presentations: stroke, status epilepticus, meningitis. |
| `inpatient` | Admitted patients: encephalitis workup, tumor evaluation. |
| `outpatient` | Chronic/subacute: progressive dementia, epilepsy follow-up, headache clinic. |

### 2.3 Tool Output Set

**Schema**: `neuroagent_schemas.case.ToolOutputSet`

Pre-generated outputs for the initial round of investigations. Not all modalities are available for every case — `null` means "this test was not ordered / not available."

| Field | Type | Description |
|---|---|---|
| `eeg` | `EEGReport \| null` | Pre-generated EEG interpretation. |
| `mri` | `MRIReport \| null` | Pre-generated brain MRI interpretation. |
| `ecg` | `ECGReport \| null` | Pre-generated ECG interpretation. |
| `labs` | `LabResults \| null` | Pre-generated lab results across panels. |
| `csf` | `CSFResults \| null` | Pre-generated CSF analysis. |
| `literature_search` | `dict[str, LiteratureSearchResult] \| null` | Keyed by query string. Multiple queries may be pre-generated. |
| `drug_interactions` | `dict[str, DrugInteractionResult] \| null` | Keyed by drug name. Multiple drugs may be pre-generated. |

The literature and drug interaction tools are keyed by their primary parameter (query or drug name) because the agent can call them with different arguments on the same case.

### 2.4 Follow-up Outputs

**Schema**: `neuroagent_schemas.case.FollowUpToolOutput`

Conditional outputs that simulate a second round of testing. These represent tests the agent might order after reviewing initial results.

| Field | Type | Description |
|---|---|---|
| `trigger_action` | string | The agent request that activates this output (e.g., "Repeat MRI with gadolinium contrast"). |
| `tool_name` | string | Which tool this responds to (e.g., `"analyze_brain_mri"`). |
| `output` | `EEGReport \| MRIReport \| ...` | The pre-generated result for this follow-up test. |

The MockServer matches follow-ups by `tool_name` (sequentially, first match). This allows benchmark cases to include clinically realistic multi-step investigations — e.g., initial labs show elevated ESR, agent orders CSF, CSF shows pleocytosis, agent orders specific antibody panels.

### 2.5 Metadata

Free-form dict for case provenance:

| Key | Description |
|---|---|
| `version` | Dataset version (`"v1"` or `"v2"`). |
| `generation_date` | ISO date of case generation. |
| `clinical_notes` | Free-text notes about the case design. |
| `teaching_points` | List of educational takeaways. |
| `created_by` | Generator identifier (e.g., `"claude-3.5-sonnet"`, `"pmc-seeded"`). |

---

## 3. Ground Truth & Evaluation

**Schema**: `neuroagent_schemas.evaluation.GroundTruth`

Every case includes a structured ground truth used for automated evaluation.

```
GroundTruth
├── primary_diagnosis           (string)
├── icd_code                    (string)
├── differential                (dict[str, str][])
├── optimal_actions             (ActionStep[])
├── critical_actions            (string[])
├── contraindicated_actions     (string[])
├── key_reasoning_points        (string[])
└── red_herrings                (RedHerring[])
```

### 3.1 Diagnosis

| Field | Type | Description |
|---|---|---|
| `primary_diagnosis` | string | The definitive diagnosis (e.g., "Early-onset Alzheimer's disease, posterior cortical atrophy variant"). |
| `icd_code` | string | ICD-10 code (e.g., `"G30.9"`, `"I63.9"`). |

### 3.2 Differential Diagnosis

```json
[
  {
    "diagnosis": "Lewy body dementia",
    "likelihood": "low",
    "key_features": "No visual hallucinations, no REM sleep behavior disorder, no fluctuating cognition"
  },
  {
    "diagnosis": "Frontotemporal dementia",
    "likelihood": "low",
    "key_features": "No personality changes, no disinhibition, no semantic deficits"
  }
]
```

### 3.3 Optimal Actions

**Schema**: `neuroagent_schemas.evaluation.ActionStep`

An ordered sequence of the ideal investigation pathway:

| Field | Type | Description |
|---|---|---|
| `step` | int | Step number in the optimal sequence. |
| `action` | string | What the agent should do (e.g., "Order brain MRI with volumetrics"). |
| `tool_name` | string \| null | Which tool this maps to (null for non-tool actions like "Obtain informed consent"). |
| `expected_finding` | string | What the correct tool output will show. |
| `category` | `ActionCategory` | `"required"`, `"acceptable"`, or `"contraindicated"`. |

**ActionCategory**:
- **required**: MUST be performed for a complete workup.
- **acceptable**: Clinically reasonable but not essential.
- **contraindicated**: Must NOT be performed (e.g., lumbar puncture with raised intracranial pressure).

### 3.4 Safety Constraints

| Field | Type | Description |
|---|---|---|
| `critical_actions` | string[] | Actions that MUST be performed regardless of reasoning path (e.g., "Check coagulation before lumbar puncture"). |
| `contraindicated_actions` | string[] | Actions that MUST NOT be performed (e.g., "Do not perform lumbar puncture without excluding mass lesion"). |

### 3.5 Key Reasoning Points

Free-text list of what the agent should conclude from the evidence:

```json
[
  "The combination of progressive visuospatial dysfunction with relatively preserved memory suggests posterior cortical atrophy",
  "MRI showing posterior-predominant atrophy with parieto-occipital involvement supports PCA variant of Alzheimer's",
  "Young age of onset (< 65) is consistent with early-onset AD"
]
```

### 3.6 Red Herrings

**Schema**: `neuroagent_schemas.evaluation.RedHerring`

Intentional distractors embedded in moderate and puzzle-difficulty cases:

| Field | Type | Description |
|---|---|---|
| `data_point` | string | The misleading element. |
| `location` | string | Where it appears (e.g., `"labs"`, `"history"`, `"mri"`, `"eeg"`). |
| `intended_effect` | string | How it might mislead (e.g., "suggests infection over tumor"). |
| `correct_interpretation` | string | What the agent should actually conclude. |

```json
{
  "data_point": "Mildly elevated WBC in CSF",
  "location": "csf",
  "intended_effect": "Suggests infectious meningitis",
  "correct_interpretation": "Reactive pleocytosis secondary to tumor lysis, not infection — protein is elevated but glucose ratio is normal and cultures are negative"
}
```

---

## 4. Patient Memory (Longitudinal)

**Schema**: `neuroagent.memory.patient_memory.PatientMemory`

ChromaDB-backed vector store for tracking patients across multiple encounters. This allows the agent to recall prior visits for the same patient.

### 4.1 Storage

After each agent run, `PatientMemory.store_encounter()` saves:

| Field | Storage | Description |
|---|---|---|
| `encounter_id` | ChromaDB document ID | `"{patient_id}_{iso_timestamp}"` |
| `summary` | ChromaDB document text | Condensed encounter summary (tools called + assessment, max 2000 chars). |
| `patient_id` | metadata | Patient identifier for filtering. |
| `date` | metadata | ISO timestamp. |
| `tools_called` | metadata (JSON) | List of tools used in the encounter. |
| `total_tool_calls` | metadata | Total number of tool invocations. |
| `has_diagnosis` | metadata | Whether the agent reached a diagnosis. |

### 4.2 Retrieval

`PatientMemory.retrieve()` returns a formatted history string injected into the system prompt:

1. Filters by `patient_id` (exact match).
2. Sorts by date (most recent first).
3. Returns up to `max_encounters` (default: 5).
4. Formats as markdown sections:

```
Previous encounters for this patient (3 found):

### Encounter 1 (2024-11-15T10:30:00)
Tests performed: analyze_brain_mri, interpret_labs
Assessment:
### Primary Diagnosis
Early-onset Alzheimer's disease...

### Encounter 2 (2024-10-01T14:20:00)
...
```

The memory string is appended to the system prompt under a `## Patient History (From Previous Encounters)` section.

### 4.3 Design choices

- **Cosine similarity** (`hnsw:space: cosine`) for the ChromaDB collection, enabling semantic search for similar past encounters if `current_complaint` is provided (not yet implemented — current retrieval is ID-based only).
- **Summarization**: Only the tools called and final assessment are stored, not the full trace. This keeps memory compact and avoids injecting verbose reasoning into future prompts.
- **No patient demographics in memory**: Demographics come from the `PatientProfile` in the case, not from memory. Memory is purely for longitudinal encounter history.

---

## 5. Data Flow Summary

```
┌──────────────────────────────────────────────────────────────┐
│                     NeuroBenchCase JSON                       │
│  ┌─────────────┐  ┌────────────────┐  ┌───────────────────┐ │
│  │PatientProfile│  │ToolOutputSet   │  │GroundTruth        │ │
│  │(what the     │  │(pre-generated  │  │(expected diagnosis│ │
│  │ agent sees)  │  │ test results)  │  │ and actions)      │ │
│  └──────┬──────┘  └───────┬────────┘  └──────────┬────────┘ │
└─────────┼─────────────────┼──────────────────────┼──────────┘
          │                 │                      │
          ▼                 ▼                      │
   ┌─────────────┐  ┌──────────────┐               │
   │ System Prompt│  │  MockServer  │               │
   │ (formatted   │  │ (serves tool │               │
   │  narrative)  │  │  outputs)    │               │
   └──────┬──────┘  └──────┬───────┘               │
          │                │                       │
          ▼                ▼                       │
   ┌───────────────────────────┐                   │
   │     Agent (ReAct Loop)    │                   │
   │  THINK → ACT → OBSERVE   │                   │
   │        → REFLECT          │                   │
   └────────────┬──────────────┘                   │
                │                                  │
                ▼                                  ▼
   ┌───────────────────┐              ┌──────────────────────┐
   │   AgentTrace      │              │  MetricsCalculator   │
   │   (reasoning      │─────────────▶│  (compares trace     │
   │    record)        │              │   vs. ground truth)  │
   └───────────────────┘              └──────────────────────┘
```

1. **Case loading**: `NeuroBenchCase` JSON is deserialized into Pydantic models.
2. **Prompt formatting**: `PatientProfile` fields are converted to a clinical narrative and sent as the user message. Hospital rules and patient memory (if any) are injected into the system prompt.
3. **Tool dispatch**: The agent calls tools; `MockServer` returns matching outputs from `initial_tool_outputs` or `followup_outputs`.
4. **Trace recording**: Every turn (reasoning, tool calls, tool results) is captured in `AgentTrace`.
5. **Evaluation**: `MetricsCalculator` compares the trace against `GroundTruth` — diagnostic accuracy, action recall, safety violations, reasoning quality.
6. **Memory storage**: If patient memory is enabled, the encounter summary is stored in ChromaDB for future retrieval.

---

## 6. Source Files

| File | Description |
|---|---|
| `neuroagent-schemas/patient.py` | `PatientProfile`, `Demographics`, `Medication`, `ClinicalHistory`, `NeurologicalExam`, `Vitals` |
| `neuroagent-schemas/case.py` | `NeuroBenchCase`, `ToolOutputSet`, `FollowUpToolOutput` |
| `neuroagent-schemas/evaluation.py` | `GroundTruth`, `ActionStep`, `RedHerring` |
| `neuroagent-schemas/enums.py` | `NeurologicalCondition`, `CaseDifficulty`, `EncounterType`, `ActionCategory`, `Modality` |
| `neuroagent-schemas/tool_outputs.py` | All tool output models (see [tools.md](tools.md)) |
| `neuroagent/memory/patient_memory.py` | `PatientMemory` (ChromaDB longitudinal store) |
| `neuroagent/agent/reasoning.py` | `AgentTrace`, `AgentTurn` |
| `data/neurobench_v1/cases/*.json` | 100 synthetic cases (v1) |
| `data/neurobench_v2/cases/*.json` | 100 real-case-seeded cases (v2) |
