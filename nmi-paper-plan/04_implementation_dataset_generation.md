# NeuroBench Dataset Generation — Implementation Plan (Claude Max / CLI Edition)

## Overview

This file is the implementation guide for the **NeuroBench dataset generation pipeline**. It produces a corpus of 500+ neurology patient cases, each with pre-generated mock tool outputs that the NeuroAgent platform (see `05_implementation_agent_platform.md`) will consume at evaluation time.

**Key change from original plan**: Instead of using the Anthropic/OpenAI API with `instructor`, we use the **Claude Code CLI** (`claude -p`) powered by a Claude Max subscription. This eliminates API costs entirely. The generation loop is a simple bash script that invokes `claude -p` with structured prompts and pipes output to JSON files, then a Python validator checks schema conformance.

### Critical Interface Contract

The dataset generation pipeline MUST produce cases in the exact format that the agent platform expects. Both systems share a single source of truth for schemas, defined in a shared `neuroagent-schemas` package.

---

## Project Structure

```
neuroagent/
├── pyproject.toml                         # Monorepo root (uv workspace)
├── packages/
│   └── neuroagent-schemas/                # SHARED SCHEMAS (both systems import this)
│       ├── pyproject.toml
│       └── src/neuroagent_schemas/
│           ├── __init__.py
│           ├── patient.py                 # PatientProfile, Demographics, ClinicalHistory
│           ├── tool_outputs.py            # EEGReport, MRIReport, LabResults, CSFResults, ...
│           ├── case.py                    # NeuroBenchCase (full case with all tool outputs)
│           ├── evaluation.py              # GroundTruth, ActionSequence, DifficultyRating
│           └── enums.py                   # NeurologicalCondition, Modality, Severity, ...
├── dataset-generation/                    # THIS PIPELINE
│   ├── pyproject.toml
│   ├── config/
│   │   ├── conditions.yaml               # Condition specs (start with 5, expand to 30)
│   │   └── prompt_template.md            # The master prompt template for case generation
│   ├── src/neurobench_gen/
│   │   ├── __init__.py
│   │   ├── build_prompt.py              # Reads condition YAML + schema → assembles prompt
│   │   ├── validate_case.py             # Loads JSON, validates with Pydantic schemas
│   │   ├── validators/
│   │   │   ├── __init__.py
│   │   │   ├── clinical_plausibility.py # Rule-based: vital signs, lab ranges, age checks
│   │   │   └── completeness.py          # All required fields populated
│   │   └── stats.py                     # Dataset statistics
│   ├── scripts/
│   │   ├── generate_batch.sh            # Main loop: claude -p < prompt > case.json
│   │   ├── generate_one.sh              # Generate + validate a single case (debug)
│   │   ├── validate_all.py              # Run validators on all existing cases
│   │   └── dataset_statistics.py        # Print dataset stats
│   └── tests/
│       ├── test_schemas.py
│       └── test_validators.py
├── data/
│   └── neurobench_v1/
│       ├── cases/                        # One JSON file per case
│       ├── failed/                       # Cases that failed validation (for debugging)
│       └── metadata.json                 # Generation metadata
└── agent-platform/                       # See 05_implementation_agent_platform.md
    └── ...
```

---

## Generation Architecture: Claude CLI Pipeline

### How it works

```
┌──────────────────────────────────────────────────────────────┐
│  1. build_prompt.py reads condition YAML + schema JSON       │
│     → writes a complete prompt to /tmp/prompt.md             │
│                                                              │
│  2. generate_batch.sh loops over conditions × difficulties:  │
│     claude -p "$(cat /tmp/prompt.md)" --output-format json   │
│     → captures raw JSON output                               │
│                                                              │
│  3. validate_case.py loads the JSON into Pydantic models     │
│     → if valid: save to data/neurobench_v1/cases/            │
│     → if invalid: save to data/neurobench_v1/failed/ + log   │
│                                                              │
│  4. On validation failure, optionally re-run with the        │
│     validation error appended to the prompt (self-correct)   │
└──────────────────────────────────────────────────────────────┘
```

### Why this works well

- **No API costs**: Claude Max subscription covers all usage
- **No library dependencies for generation**: Just bash + `claude` CLI
- **Pydantic validation still catches errors**: Same schema guarantees
- **Simple retry**: Re-invoke `claude -p` with error feedback appended
- **Resumable**: Script checks if `CASE-ID.json` already exists, skips it
- **Each case is independent**: No shared state, trivially parallelizable

### Prompt strategy

Each `claude -p` invocation gets a single comprehensive prompt that includes:
1. The JSON schema for the complete `NeuroBenchCase` model (auto-exported from Pydantic)
2. The condition specification from `conditions.yaml`
3. The difficulty level and demographic parameters
4. Instructions to generate the ENTIRE case (patient + all tool outputs + follow-ups + ground truth) in ONE response
5. Instruction to output ONLY valid JSON, no markdown fences, no commentary

This "single mega-prompt" approach ensures cross-modal consistency since the LLM generates EEG, MRI, labs, etc. in a single coherent pass.

---

## Step-by-Step Implementation TODO

### Phase 0: Project Setup

```
TODO-D0.1: Initialize monorepo with uv workspace
  - Create pyproject.toml at root with [tool.uv.workspace]
  - Use Python 3.11+
  - Initialize packages/neuroagent-schemas and dataset-generation

TODO-D0.2: Install core dependencies for dataset-generation
  Dependencies:
    - pydantic >= 2.0         # Schema validation
    - pyyaml                  # Config loading
    - rich                    # Progress display
    - typer                   # CLI for validate/stats scripts
    - pytest                  # Testing

  NOT needed (removed from original plan):
    - instructor              # No API, using claude CLI instead
    - openai                  # No API
    - polars                  # Overkill for stats, stdlib suffices

TODO-D0.3: Create output directories
  - data/neurobench_v1/cases/
  - data/neurobench_v1/failed/
```

### Phase 1: Shared Schemas (`neuroagent-schemas`)

This is the MOST IMPORTANT step. Both the dataset generator and the agent platform depend on these. The schemas also get exported as JSON Schema and embedded in the generation prompt.

```
TODO-D1.1: Define enums (enums.py)
  - NeurologicalCondition (start with 5 for pilot, expand to ~30 later):
    PILOT SET: FOCAL_EPILEPSY_TEMPORAL, ISCHEMIC_STROKE,
    AUTOIMMUNE_ENCEPHALITIS_NMDAR, ALZHEIMERS_EARLY, SYNCOPE_CARDIAC
  - Modality: EEG, MRI, FMRI, ECG, LABS, CSF, EMG_NCS, CLINICAL_HISTORY
  - CaseDifficulty: STRAIGHTFORWARD, MODERATE, DIAGNOSTIC_PUZZLE
  - ActionCategory: REQUIRED, ACCEPTABLE, CONTRAINDICATED
  - EncounterType: EMERGENCY, INPATIENT, OUTPATIENT

TODO-D1.2: Define patient schemas (patient.py)
  Pydantic models: Demographics, Medication, ClinicalHistory,
  NeurologicalExam, Vitals, PatientProfile
  (Full field specs unchanged from original plan)

TODO-D1.3: Define tool output schemas (tool_outputs.py)
  EEGFinding, EEGReport, MRIFinding, MRIReport, LabValue, LabResults,
  CSFResults, ECGReport, LiteratureSearchResult, DrugInteractionResult
  (Full field specs unchanged from original plan)

TODO-D1.4: Define case schema (case.py)
  ToolOutputSet, FollowUpToolOutput, NeuroBenchCase

TODO-D1.5: Define evaluation schemas (evaluation.py)
  ActionStep, GroundTruth

TODO-D1.6: Add JSON Schema export utility
  - Add a script/function that dumps each Pydantic model's JSON schema
  - This JSON schema gets embedded in the generation prompt so Claude
    knows the exact output format
  - Key: use model.model_json_schema() to export

TODO-D1.7: Write tests for all schemas
  - Test parsing, validation constraints, round-trip serialization
  - Create one complete example case fixture
```

### Phase 2: Condition Specifications (5 conditions for pilot)

```
TODO-D2.1: Create conditions.yaml (PILOT — 5 conditions)
  For the initial 50-case run, define these 5 conditions:

  1. focal_epilepsy_temporal — classic neurology, well-defined findings
  2. ischemic_stroke — emergency setting, clear imaging
  3. autoimmune_encephalitis_nmdar — diagnostic puzzle, multi-modal
  4. alzheimers_early — outpatient, subtle findings
  5. syncope_cardiac — non-neurological cause, tests agent's restraint

  Each condition defines:
  - name, icd_code, description
  - typical_demographics: age_range, sex_bias
  - required_modalities, optional_modalities
  - key_findings per modality and difficulty level
  - differential_diagnoses
  - difficulty_variants (straightforward, moderate, diagnostic_puzzle)
  - common_followups: list of trigger_action + tool_name pairs

TODO-D2.2: Distribution for 50-case pilot
  Per condition: 10 cases
    - 4 straightforward, 3 moderate, 3 diagnostic_puzzle
  Total: 50 cases
```

### Phase 3: Generation Engine (Claude CLI)

```
TODO-D3.1: Create prompt_template.md
  A Jinja2-style template that build_prompt.py fills in:

  ===
  You are an expert neurologist and medical educator creating a realistic
  simulated patient case for a neurology AI benchmark.

  ## Task
  Generate a COMPLETE patient case as a single JSON object conforming
  exactly to the schema below. Output ONLY the JSON — no markdown fences,
  no commentary, no explanation.

  ## JSON Schema
  {{ json_schema }}

  ## Condition
  {{ condition_yaml }}

  ## Parameters
  - Case ID: {{ case_id }}
  - Difficulty: {{ difficulty }}
  - Encounter type: {{ encounter_type }}

  ## Requirements
  1. The patient profile must be clinically realistic and internally consistent
  2. ALL tool outputs must be cross-modally consistent with each other
  3. For {{ difficulty }} difficulty:
     - STRAIGHTFORWARD: findings clearly point to the diagnosis
     - MODERATE: some findings are subtle or ambiguous
     - DIAGNOSTIC_PUZZLE: initial findings may be misleading
  4. Generate at least 5 follow-up tool outputs for predictable follow-up requests
  5. Ground truth must include the correct diagnosis, differential, and optimal actions
  6. Vital signs, lab values, and medication doses must be physiologically plausible
  7. The case should read like a real patient encounter, not a textbook example
  ===

TODO-D3.2: Implement build_prompt.py
  def build_prompt(condition_key: str, difficulty: str, case_id: str,
                   schema_path: str, conditions_path: str) -> str:
      """
      Reads the template, fills in:
      - The full NeuroBenchCase JSON schema (from Pydantic export)
      - The specific condition spec (from conditions.yaml)
      - Case ID, difficulty, encounter type
      Returns the assembled prompt string.
      """

TODO-D3.3: Implement generate_batch.sh
  #!/bin/bash
  # Main generation loop
  #
  # Usage: ./generate_batch.sh [--dry-run] [--parallel N]
  #
  # For each (condition, difficulty, case_number):
  #   1. Compute case_id (e.g., FEPI-TEMP-S01)
  #   2. Skip if data/neurobench_v1/cases/{case_id}.json exists
  #   3. Run: python build_prompt.py → /tmp/prompt_${case_id}.md
  #   4. Run: claude -p "$(cat /tmp/prompt_${case_id}.md)" --output-format json \
  #           > /tmp/raw_${case_id}.json
  #   5. Run: python validate_case.py /tmp/raw_${case_id}.json
  #      - If valid → move to data/neurobench_v1/cases/{case_id}.json
  #      - If invalid → retry once with error, then move to failed/
  #   6. Print progress

TODO-D3.4: Implement generate_one.sh
  # Debug helper: generate one case and pretty-print the result
  # Usage: ./generate_one.sh focal_epilepsy_temporal straightforward 01

TODO-D3.5: Implement validate_case.py
  def validate_case(json_path: str) -> tuple[bool, list[str]]:
      """
      1. Load JSON from file
      2. Parse into NeuroBenchCase Pydantic model
      3. Run rule-based validators (vital signs, lab ranges, completeness)
      4. Return (is_valid, list_of_issues)
      """
```

### Phase 4: Validation (Rule-Based Only for Pilot)

```
TODO-D4.1: Implement clinical_plausibility.py (rule-based)
  Checks:
  - Vital signs in physiological range
  - Lab values in physiological range
  - Age 18-90
  - Confidence values 0.0-1.0
  - Required fields non-empty

TODO-D4.2: Implement completeness.py
  Checks:
  - All required modalities for the condition have tool outputs
  - Ground truth has primary_diagnosis, differential, optimal_actions
  - At least 5 follow-up outputs
  - Case ID matches expected pattern

Note: Cross-modal consistency validation (LLM-as-judge) is deferred to
after the pilot. For the 50-case pilot, we rely on the single-prompt
approach for consistency and do manual spot-checks.
```

### Phase 5: Statistics and Inspection

```
TODO-D5.1: Implement dataset_statistics.py
  Print:
  - Total cases by condition and difficulty
  - Modality coverage
  - Age/sex distributions
  - Validation pass rate
  - Average follow-up count per case

TODO-D5.2: Manual quality review
  After generating 50 cases, manually inspect 5-10 cases for:
  - Clinical realism
  - Cross-modal consistency
  - Appropriate difficulty calibration
  - Ground truth accuracy
```

---

## 50-Case Pilot Plan

### Goal
Generate 50 validated cases across 5 conditions to prove the pipeline works
and the case quality is sufficient before scaling to 500+.

### Distribution

| Condition | Straightforward | Moderate | Puzzle | Total |
|-----------|----------------|----------|--------|-------|
| Focal epilepsy (temporal) | 4 | 3 | 3 | 10 |
| Ischemic stroke | 4 | 3 | 3 | 10 |
| Anti-NMDAR encephalitis | 4 | 3 | 3 | 10 |
| Early Alzheimer's | 4 | 3 | 3 | 10 |
| Cardiac syncope | 4 | 3 | 3 | 10 |
| **Total** | **20** | **15** | **15** | **50** |

### Case ID Convention
`{CONDITION_ABBREV}-{DIFFICULTY_LETTER}{NUMBER}`
- FEPI-TEMP-S01 = Focal Epilepsy Temporal, Straightforward, #01
- ISCH-STR-M01 = Ischemic Stroke, Moderate, #01
- NMDAR-ENC-P01 = NMDAR Encephalitis, Puzzle, #01
- ALZ-EARLY-S01 = Alzheimer's Early, Straightforward, #01
- SYNC-CARD-M01 = Cardiac Syncope, Moderate, #01

### Execution Order
1. Set up monorepo + schemas + conditions YAML
2. Generate 1 case manually, inspect, iterate on prompt
3. Generate remaining 49 cases via batch script
4. Validate all, fix failures
5. Print statistics, spot-check 5-10 cases manually

---

## Scaling to 500+ Cases (After Pilot Validation)

Once the 50-case pilot confirms quality:
1. Expand conditions.yaml to all ~30 conditions
2. Add LLM-as-judge cross-modal validation (via `claude -p`)
3. Add longitudinal case generation (multi-encounter)
4. Add train/val/test splitting
5. Run batch generation in parallel (multiple `claude -p` processes)

---

## Key Design Decisions and Rationale

1. **Claude CLI over API**: Uses Claude Max subscription — zero API cost. The `claude -p` flag enables non-interactive single-prompt mode, perfect for scripted generation.

2. **Single mega-prompt per case**: Generate the ENTIRE case (patient + all tool outputs + follow-ups + ground truth) in one `claude -p` call. This ensures cross-modal consistency without needing multiple coordinated API calls.

3. **JSON Schema in prompt**: Export the Pydantic model's JSON schema and embed it directly in the prompt. Claude follows JSON schemas very reliably, reducing validation failures.

4. **Bash orchestration, Python validation**: The generation loop is a simple bash script (easy to parallelize, resume, debug). Validation is Python with Pydantic (type-safe, reusable by agent platform).

5. **5 conditions first, 30 later**: Start small to validate quality before investing in the full condition set. The 5 pilot conditions cover diverse clinical scenarios (emergency, outpatient, puzzle, non-neurological).

6. **Rule-based validation for pilot, LLM-judge later**: Avoids the chicken-and-egg of needing Claude CLI calls for validation during generation. Add LLM-as-judge in the scaling phase.
