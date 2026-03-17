# Tool Reference

NeuroAgent equips the LLM with **7 diagnostic tools** exposed via OpenAI-compatible function calling. The agent decides which tools to invoke and in what order as part of its ReAct reasoning loop. This document is the authoritative reference for every tool: what it does, what it accepts, and what it returns.

## Architecture

```
                        ┌──────────────────┐
                        │  LLM (ReAct)     │
                        │  "I need an EEG" │
                        └────────┬─────────┘
                                 │  ToolCall(name, params)
                        ┌────────▼─────────┐
                        │  ToolRegistry    │
                        │  dispatch by name│
                        └────────┬─────────┘
                                 │  BaseTool.execute()
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                   ▼
        ┌───────────┐    ┌───────────┐       ┌───────────┐
        │ MockServer│    │ Real Model│       │ External  │
        │(eval mode)│    │ (future)  │       │ API (fut.)│
        └───────────┘    └───────────┘       └───────────┘
```

### Key abstractions (`tools/base.py`)

| Class | Purpose |
|---|---|
| `BaseTool` | Abstract base. Every tool defines `name`, `description`, `parameter_schema`, and `execute()`. |
| `ToolCall` | What the agent produces: `tool_name` + `parameters` dict. |
| `ToolResult` | What the tool returns: `tool_name`, `success` (bool), `output` (dict), optional `error_message`. |

Tools are registered in `ToolRegistry` and their definitions are passed to the LLM via `get_tool_definition()` which returns an OpenAI-style function spec (`{type: "function", function: {name, description, parameters}}`).

### Execution modes

- **Evaluation (MockServer)**: All tools are backed by `MockServer`, which looks up pre-generated outputs from `NeuroBenchCase.initial_tool_outputs` and `followup_outputs`. This is the current default.
- **Live (future)**: Each tool would connect to a real model endpoint or external API. Currently raises `NotImplementedError`.
- **v3 Realistic mode**: The v3 dataset (`data/neurobench_v3/`) strips interpretive fields from tool outputs. Fields like `clinical_significance`, `differential_by_imaging`, `recommended_actions`, and diagnostic `impression` text are nulled or rewritten to match what real clinical reports provide. This forces the agent to perform actual clinical reasoning rather than reading pre-digested answers. See "Tool Output Modes" below.

### Ablation controls

`AgentConfig` supports two knobs for ablation experiments:

- `allowed_tools: list[str] | None` — whitelist; only these tools are exposed.
- `excluded_tools: list[str] | None` — blacklist; these tools are removed.
- `all_info_upfront: bool` — bypass the tool loop entirely; dump all outputs at once and get a single-shot response.

---

## Tool Catalog

All tools share one required parameter: **`clinical_context`** (string) — the clinical question or scenario motivating the investigation. The agent should write a brief justification here, which also serves as visible reasoning when `<think>` tags are hidden.

---

### 1. `analyze_eeg` — EEG Analyzer

Analyze an electroencephalography recording for neurological abnormalities.

**When to call**: Suspected seizures, epilepsy, encephalopathy, altered mental status, sleep disorders, or to differentiate epileptic vs. non-epileptic events.

#### Parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `clinical_context` | string | yes | Clinical context for the EEG interpretation. |
| `eeg_file_path` | string | no | Path to the EEG recording file. |
| `patient_age` | integer | no | Patient age in years (affects normal-range interpretation). |
| `focus_areas` | string[] | no | Specific areas or patterns to focus on (e.g., `["temporal_sharp_waves", "generalized_slowing"]`). |

#### Returns: `EEGReport`

| Field | Type | Description |
|---|---|---|
| `classification` | `"normal"` \| `"abnormal"` | Overall EEG classification. |
| `background` | dict[str, str] | Background activity: `posterior_dominant_rhythm`, `anterior_rhythm`, `sleep` features. |
| `findings` | `EEGFinding[]` | Individual abnormalities detected (see below). |
| `artifacts` | dict[str, str][] | Artifacts noted (muscle, electrode pop, movement, etc.). |
| `activating_procedures` | dict[str, str] | Results of hyperventilation, photic stimulation, sleep deprivation. |
| `confidence` | float (0.0–1.0) | Interpretation confidence score. |
| `impression` | string | Clinical impression — narrative summary. |
| `limitations` | string | Quality or duration limitations of the recording. |
| `recommended_actions` | string[] | Suggested follow-up (e.g., "long-term monitoring", "video-EEG"). |

**`EEGFinding` fields**: `type` (e.g., sharp_wave, slowing, periodic_discharge), `location` (e.g., "F8/T4, right anterior temporal"), `frequency`, `morphology`, `state` (awake/sleep), `clinical_correlation`.

> **v3 realistic mode**: In the v3 dataset, `confidence` is set to 0.0 (not provided), `impression` is stripped of disease names (descriptive findings only + "Clinical correlation recommended."), `recommended_actions` is replaced with `["Clinical correlation recommended."]`, and all `EEGFinding.clinical_correlation` fields are set to `""`.

---

### 2. `analyze_brain_mri` — Brain MRI Analyzer

Analyze a brain MRI scan for structural abnormalities, volumetric changes, and differential diagnoses.

**When to call**: Suspected structural lesions, tumors, stroke, dementia (atrophy patterns), multiple sclerosis (demyelination), or any focal neurological deficit requiring anatomical correlation.

#### Parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `clinical_context` | string | yes | Clinical context for the MRI interpretation. |
| `mri_file_path` | string | no | Path to the MRI scan file. |
| `sequences` | string[] | no | MRI sequences to analyze (e.g., `["T1", "T2", "FLAIR", "DWI", "SWI"]`). |
| `contrast` | boolean | no | Whether contrast-enhanced sequences are available. |

#### Returns: `MRIReport`

| Field | Type | Description |
|---|---|---|
| `findings` | `MRIFinding[]` | Structural findings (see below). |
| `volumetrics` | dict[str, str] \| null | Brain volumes, cortical thickness, percentiles vs. age norms. |
| `additional_observations` | string[] | Incidental findings, microbleeds, white matter hyperintensities, etc. |
| `impression` | string | Clinical impression — narrative summary. |
| `differential_by_imaging` | dict[str, str][] | Imaging-based differential: `diagnosis`, `likelihood`. |
| `confidence` | float (0.0–1.0) | Interpretation confidence score. |
| `recommended_actions` | string[] | Suggested follow-up imaging or procedures. |

**`MRIFinding` fields**: `type` (e.g., mass_lesion, atrophy, white_matter_lesion), `location`, `size`, `signal_characteristics` (dict with T1/T2/FLAIR/DWI/contrast signals), `mass_effect`, `borders`.

> **v3 realistic mode**: `differential_by_imaging` is `[]` (empty), `confidence` is 0.0, `recommended_actions` is `["Clinical correlation recommended."]`, `impression` is stripped of diagnosis names and treatment recommendations, and `additional_observations` entries containing diagnostic conclusions are removed.

---

### 3. `analyze_ecg` — ECG Analyzer

Analyze a 12-lead electrocardiogram for cardiac abnormalities relevant to neurological presentations.

**When to call**: Syncope, suspected cardioembolic stroke, arrhythmia-related seizure mimics, or autonomic dysfunction evaluation.

#### Parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `clinical_context` | string | yes | Clinical context for the ECG interpretation. |
| `ecg_file_path` | string | no | Path to the ECG recording file. |

#### Returns: `ECGReport`

| Field | Type | Description |
|---|---|---|
| `rhythm` | string | Rhythm classification (e.g., "normal sinus rhythm", "atrial fibrillation"). |
| `rate` | int | Heart rate in beats per minute. |
| `intervals` | dict[str, str] | PR, QRS, QT/QTc intervals in milliseconds. |
| `axis` | string | Cardiac axis (normal, left deviation, right deviation, extreme). |
| `findings` | string[] | Specific abnormalities (ST changes, T-wave inversions, LVH, etc.). |
| `interpretation` | string | Summary interpretation. |
| `clinical_correlation` | string | How ECG findings relate to the neurological presentation. |

> **v3 realistic mode**: `clinical_correlation` is `""` (empty). `interpretation` is stripped of disease-etiology commentary, keeping only rhythm/rate/interval descriptions.

---

### 4. `interpret_labs` — Lab Interpreter

Interpret laboratory results across multiple panels with reference ranges, abnormality flags, and clinical interpretation in context.

**When to call**: Essentially every case — labs establish baseline metabolic status, screen for infectious/inflammatory/autoimmune/metabolic etiologies, and guide treatment decisions.

#### Parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `clinical_context` | string | yes | Clinical context for lab interpretation. |
| `panels` | string[] | no | Which panels to interpret (e.g., `["CBC", "BMP", "LFT", "thyroid", "coagulation"]`). |
| `patient_age` | integer | no | Patient age in years (affects reference ranges). |
| `patient_sex` | string | no | Patient sex — `"male"` or `"female"` (affects reference ranges). |

#### Returns: `LabResults`

| Field | Type | Description |
|---|---|---|
| `panels` | dict[str, LabValue[]] | Results grouped by panel name (CBC, BMP, Coagulation, Lipid, Cardiac, Thyroid, Dementia screening, Inflammatory markers, Liver function, etc.). |
| `interpretation` | string | Overall clinical interpretation of the lab picture. |
| `abnormal_values_summary` | string[] | Highlighted abnormal values with clinical significance. |

**`LabValue` fields**: `test` (name), `value` (float or string), `unit`, `reference_range`, `is_abnormal` (bool), `clinical_significance` (optional explanation).

> **v3 realistic mode**: All `LabValue.clinical_significance` fields are `null`. `interpretation` is replaced with a terse list of abnormal values only (e.g., "Abnormal values: Sodium 126 mEq/L (L), Glucose 186 mg/dL (H)."). `abnormal_values_summary` entries are stripped of prose explanations, keeping only "Test: value unit (H/L)".

---

### 5. `analyze_csf` — CSF Analyzer

Analyze cerebrospinal fluid results including cell counts, chemistry, and special tests.

**When to call**: Suspected CNS infection (meningitis, encephalitis), autoimmune encephalitis (antibody panels), demyelinating disease (oligoclonal bands), subarachnoid hemorrhage (xanthochromia), or CNS malignancy (cytology).

#### Parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `clinical_context` | string | yes | Clinical context for CSF interpretation. |
| `special_tests` | string[] | no | Special CSF tests to interpret (e.g., `["HSV_PCR", "oligoclonal_bands", "NMDAR_antibodies", "cytology"]`). |

#### Returns: `CSFResults`

| Field | Type | Description |
|---|---|---|
| `appearance` | string | Visual appearance (clear, turbid, xanthochromic, hemorrhagic). |
| `opening_pressure` | string | Opening pressure in cmH2O. |
| `cell_count` | dict[str, str] | WBC, RBC, and differential (neutrophils, lymphocytes, monocytes %). |
| `protein` | string | Protein level in mg/dL. |
| `glucose` | string | CSF glucose in mg/dL. |
| `glucose_ratio` | string | CSF glucose / serum glucose ratio. |
| `special_tests` | dict[str, str] | Results of special tests: Gram stain, culture, HSV PCR, crypto antigen, oligoclonal bands, antibody panels, cytology, etc. |
| `interpretation` | string | Clinical interpretation of the CSF profile. |

> **v3 realistic mode**: `interpretation` is replaced with a terse numerical summary (e.g., "Opening pressure: 31 cmH2O. WBC: 392 (72% PMN/24% lymph). Protein: 153.2 mg/dL. Glucose: 30.7 mg/dL (ratio 0.24)."). No diagnostic commentary.

---

### 6. `search_medical_literature` — Literature Search

Search medical literature and clinical guidelines for evidence relevant to a clinical question.

**When to call**: Rare or atypical presentations, evidence for treatment decisions, guideline recommendations for specific scenarios, or when the differential includes uncommon conditions.

#### Parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `query` | string | yes | Clinical question or search query. |
| `max_results` | integer | no | Maximum results to return (default: 5). |

#### Returns: `LiteratureSearchResult`

| Field | Type | Description |
|---|---|---|
| `query` | string | The search query used. |
| `results` | dict[str, str][] | Individual results, each with `source` (journal/guideline), `finding` (key result), `evidence_level`. |
| `summary` | string | Synthesized summary of the evidence. |

**MockServer note**: In evaluation mode, literature search results are pre-generated and matched by the `query` parameter — exact match first, then falls back to the first available result.

---

### 7. `check_drug_interactions` — Drug Interaction Checker

Check drug interactions, contraindications, formulary status, and alternatives for a proposed medication.

**When to call**: Before recommending any new medication, especially anticonvulsants (complex interactions with CYP enzymes), anticoagulants, or when the patient has polypharmacy.

#### Parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `drug` | string | yes | The proposed medication to check. |
| `current_medications` | string[] | no | List of patient's current medications. |
| `patient_conditions` | string[] | no | List of patient's medical conditions (for contraindication checking). |

#### Returns: `DrugInteractionResult`

| Field | Type | Description |
|---|---|---|
| `proposed` | string | The drug being evaluated. |
| `interactions` | string[] | Drug-drug interactions with current medications. |
| `contraindications` | string[] | Absolute contraindications. |
| `warnings` | string[] | Precautions and relative contraindications. |
| `formulary_status` | string | Availability status (e.g., "available", "restricted", "prior authorization"). |
| `alternatives` | string[] | Suggested alternative medications. |

**MockServer note**: Drug interaction results are pre-generated and matched by the `drug` parameter.

---

## Additional tool: `check_hospital_rules` (not in default registry)

Defined in `tools/hospital_rules_checker.py` but **not registered** in the default 7-tool registry. Hospital rules are instead injected into the system prompt via the `RulesEngine`. This tool exists for potential future use as an on-demand protocol lookup.

| Name | Type | Required | Description |
|---|---|---|---|
| `clinical_scenario` | string | yes | Description of the current clinical scenario. |
| `suspected_condition` | string | no | The suspected or confirmed condition. |

---

## How the MockServer routes tool calls

During evaluation, `MockServer` receives every `ToolCall` and returns pre-generated outputs from the loaded `NeuroBenchCase`:

1. **Diagnostic tools** (EEG, MRI, ECG, labs, CSF): Direct lookup from `case.initial_tool_outputs.{eeg,mri,ecg,labs,csf}`. Returns `None` (tool fails gracefully) if that modality isn't available for the case.

2. **Literature search**: Matches by `query` parameter against keys in `case.initial_tool_outputs.literature_search` dict. Falls back to the first available entry if no exact match.

3. **Drug interactions**: Matches by `drug` parameter against keys in `case.initial_tool_outputs.drug_interactions` dict. Same fallback behavior.

4. **Follow-up outputs**: If no initial output matches, searches `case.followup_outputs[]` for entries where `tool_name` matches. These represent conditional test results (e.g., a repeat MRI with contrast, or a specialized CSF panel ordered after initial results).

5. **No match**: Returns `ToolResult(success=False, error_message="No {tool} data available...")`, prompting the agent to reconsider whether the test is appropriate.

All outputs are serialized via `model.model_dump()` (Pydantic v2) and returned as JSON dicts within `ToolResult.output`.

---

## Tool Output Modes: v1 (Enhanced) vs v3 (Realistic)

The NeuroBench dataset exists in two output modes, both containing the same 200 cases (100 synthetic + 100 real-case-seeded):

### v1 / v2: Enhanced tool outputs (original)

Tool outputs include interpretive fields designed to make the task easier:
- `LabValue.clinical_significance` explains WHY a value matters for the diagnosis
- `MRIReport.differential_by_imaging` provides a ranked imaging differential
- `EEGReport.impression` names specific diseases and recommends management
- `CSFResults.interpretation` provides full diagnostic formulations
- Numeric `confidence` scores (0.0-1.0) on imaging reports

These outputs read like an attending physician's case discussion — the answer is partially embedded in the tool results. This mode is useful for:
- Testing whether the agent can follow pre-digested clinical reasoning
- Establishing an upper bound on diagnostic accuracy
- Comparing tool-augmented vs. no-tool performance where tool outputs are maximally informative

### v3: Realistic tool outputs (stripped)

The same 200 cases with interpretive fields removed or rewritten to match real-world clinical reports:
- Lab values show numbers, units, reference ranges, and H/L flags only — no clinical interpretation
- MRI/EEG impressions describe findings without naming diseases or suggesting treatments
- No imaging differentials, no confidence scores, no recommended actions beyond "Clinical correlation recommended."
- CSF results are terse numerical summaries

This mode tests genuine clinical reasoning: the agent must synthesize raw findings across modalities to reach a diagnosis, just as a real clinician would interpret reports from radiology, pathology, and the lab.

**For the NMI paper**, the primary benchmark uses v3 (realistic). The v1→v3 accuracy delta is reported as an ablation showing the effect of interpretive tool outputs on agent performance.

### Creating v3 from v1/v2

```bash
uv run python agent-platform/scripts/create_v3_dataset.py
```

This script reads both `data/neurobench_v1/cases/` and `data/neurobench_v2/cases/`, applies the stripping transformations, and writes 200 cleaned cases to `data/neurobench_v3/cases/`.

---

## Source files

| File | Description |
|---|---|
| `tools/base.py` | `BaseTool`, `ToolCall`, `ToolResult` abstractions |
| `tools/tool_registry.py` | `ToolRegistry` with `create_default_registry()` |
| `tools/eeg_analyzer.py` | `EEGAnalyzerTool` |
| `tools/mri_analyzer.py` | `MRIAnalyzerTool` |
| `tools/ecg_analyzer.py` | `ECGAnalyzerTool` |
| `tools/lab_interpreter.py` | `LabInterpreterTool` |
| `tools/csf_analyzer.py` | `CSFAnalyzerTool` |
| `tools/literature_search.py` | `LiteratureSearchTool` |
| `tools/drug_interaction.py` | `DrugInteractionTool` |
| `tools/hospital_rules_checker.py` | `HospitalRulesCheckerTool` (not in default registry) |
| `tools/mock_server.py` | `MockServer` for evaluation mode |
| `neuroagent-schemas/tool_outputs.py` | Pydantic output models (`EEGReport`, `MRIReport`, etc.) |
