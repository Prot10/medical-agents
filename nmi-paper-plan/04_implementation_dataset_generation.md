# NeuroBench Dataset Generation — Implementation Plan for Claude Code

## Overview

This file is the implementation guide for the **NeuroBench dataset generation pipeline**. It produces a corpus of 500+ neurology patient cases, each with pre-generated mock tool outputs that the NeuroAgent platform (see `05_implementation_agent_platform.md`) will consume at evaluation time.

### Critical Interface Contract

The dataset generation pipeline MUST produce cases in the exact format that the agent platform expects. Both systems share a single source of truth for schemas, defined in a shared `neuroagent-schemas` package (see Section 10).

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
│   │   ├── conditions.yaml                # All 30 neurological conditions with parameters
│   │   ├── demographics.yaml              # Age/sex/comorbidity distributions
│   │   ├── tool_output_templates.yaml     # Prompt templates for generating each tool output
│   │   └── generation_config.yaml         # LLM settings, batch sizes, retry policy
│   ├── src/neurobench_gen/
│   │   ├── __init__.py
│   │   ├── pipeline.py                    # Main orchestration: condition → case → tools → validate
│   │   ├── case_generator.py              # Generates clinical vignettes from condition specs
│   │   ├── tool_output_generator.py       # Generates mock tool outputs for each case
│   │   ├── followup_generator.py          # Generates branching follow-up tool outputs
│   │   ├── ground_truth_generator.py      # Generates optimal action sequences + evaluation criteria
│   │   ├── validators/
│   │   │   ├── __init__.py
│   │   │   ├── cross_modal_consistency.py # Validates EEG/MRI/labs consistency
│   │   │   ├── clinical_plausibility.py   # Validates vital signs, lab ranges, temporal logic
│   │   │   └── completeness.py            # Ensures all required fields are populated
│   │   ├── llm_client.py                  # Unified LLM interface (OpenAI-compatible, supports local vLLM)
│   │   └── utils.py                       # Retry logic, logging, checkpointing
│   ├── scripts/
│   │   ├── generate_full_dataset.py       # Main entry point: generate all 500+ cases
│   │   ├── generate_single_case.py        # Debug: generate and inspect one case
│   │   ├── validate_dataset.py            # Run all validators on existing dataset
│   │   └── dataset_statistics.py          # Compute and print dataset stats
│   └── tests/
│       ├── test_case_generator.py
│       ├── test_tool_output_generator.py
│       ├── test_validators.py
│       └── test_schemas.py
└── agent-platform/                        # See 05_implementation_agent_platform.md
    └── ...
```

---

## Step-by-Step Implementation TODO

### Phase 0: Project Setup

```
TODO-D0.1: Initialize monorepo with uv workspace
  - Create pyproject.toml at root with [tool.uv.workspace] pointing to packages/*, dataset-generation/, agent-platform/
  - Use Python 3.11+
  - Run: uv init --lib packages/neuroagent-schemas
  - Run: uv init dataset-generation
  - Run: uv init agent-platform

TODO-D0.2: Install core dependencies for dataset-generation
  Dependencies:
    - pydantic >= 2.0         # Schema validation (ALL schemas are Pydantic models)
    - instructor >= 1.0       # Structured LLM output extraction with automatic retries
    - openai >= 1.0           # OpenAI-compatible API client (works with vLLM, Anthropic, etc.)
    - pyyaml                  # Config loading
    - rich                    # Progress bars and logging
    - typer                   # CLI interface
    - pytest                  # Testing
    - polars                  # Dataset statistics (faster than pandas)

TODO-D0.3: Set up configuration files
  - Create config/generation_config.yaml with:
    - llm_provider: "anthropic" | "openai" | "vllm_local"
    - model_name: "claude-sonnet-4-20250514" (for generation) or local Qwen3 endpoint
    - temperature: 0.7 (for diversity) / 0.0 (for validation)
    - max_retries: 3
    - batch_size: 10
    - checkpoint_every: 50
    - output_dir: "./data/neurobench_v1"
```

### Phase 1: Shared Schemas (`neuroagent-schemas`)

This is the MOST IMPORTANT step — both the dataset generator and the agent platform depend on these schemas. Get them right first.

```
TODO-D1.1: Define enums (enums.py)
  Create the following enums:
  - NeurologicalCondition: ~30 values (FOCAL_EPILEPSY_TEMPORAL, FOCAL_EPILEPSY_FRONTAL,
    GENERALIZED_EPILEPSY, ALZHEIMERS_EARLY, ALZHEIMERS_MODERATE, ISCHEMIC_STROKE,
    HEMORRHAGIC_STROKE, TIA, MULTIPLE_SCLEROSIS, PARKINSONS, MIGRAINE_WITH_AURA,
    MIGRAINE_WITHOUT_AURA, BACTERIAL_MENINGITIS, VIRAL_ENCEPHALITIS,
    AUTOIMMUNE_ENCEPHALITIS_NMDAR, AUTOIMMUNE_ENCEPHALITIS_LGI1, BRAIN_TUMOR_GLIOMA,
    BRAIN_TUMOR_MENINGIOMA, BRAIN_TUMOR_METASTASIS, FTD, NPH, MYASTHENIA_GRAVIS,
    PERIPHERAL_NEUROPATHY, SYNCOPE_CARDIAC, SYNCOPE_VASOVAGAL, CJD, CADASIL,
    NEUROSARCOIDOSIS, STATUS_EPILEPTICUS, ATYPICAL_PARKINSONISM_MSA,
    ATYPICAL_PARKINSONISM_PSP, FUNCTIONAL_NEUROLOGICAL_DISORDER)
  - Modality: EEG, MRI, FMRI, ECG, LABS, CSF, EMG_NCS, CLINICAL_HISTORY
  - CaseDifficulty: STRAIGHTFORWARD, MODERATE, DIAGNOSTIC_PUZZLE
  - ActionCategory: REQUIRED, ACCEPTABLE, CONTRAINDICATED
  - EncounterType: EMERGENCY, INPATIENT, OUTPATIENT

TODO-D1.2: Define patient schemas (patient.py)
  Pydantic models:
  - Demographics(BaseModel):
      age: int (18-90), sex: Literal["male","female"], handedness: str,
      ethnicity: str, bmi: float | None
  - Medication(BaseModel):
      drug: str, dose: str, frequency: str, indication: str
  - ClinicalHistory(BaseModel):
      past_medical_history: list[str], medications: list[Medication],
      allergies: list[str], family_history: list[str],
      social_history: dict[str, str]
  - NeurologicalExam(BaseModel):
      mental_status: str, cranial_nerves: str, motor: str, sensory: str,
      reflexes: str, coordination: str, gait: str, additional: str | None
  - Vitals(BaseModel):
      bp_systolic: int, bp_diastolic: int, hr: int, temp: float,
      rr: int, spo2: int
  - PatientProfile(BaseModel):
      patient_id: str, demographics: Demographics, clinical_history: ClinicalHistory,
      neurological_exam: NeurologicalExam, vitals: Vitals,
      chief_complaint: str, history_present_illness: str

TODO-D1.3: Define tool output schemas (tool_outputs.py)
  These are the EXACT schemas the agent platform will receive when it calls a tool.
  Pydantic models:

  - EEGFinding(BaseModel):
      type: str (e.g., "sharp_wave", "slowing", "periodic_discharge")
      location: str (e.g., "F8/T4, right anterior temporal")
      frequency: str, morphology: str, state: str,
      clinical_correlation: str

  - EEGReport(BaseModel):
      classification: Literal["normal", "abnormal"]
      background: dict[str, str]  # pdr, sleep_features, overall
      findings: list[EEGFinding]
      artifacts: list[dict[str, str]]
      activating_procedures: dict[str, str]
      confidence: float  # 0.0-1.0
      impression: str
      limitations: str
      recommended_actions: list[str]

  - MRIFinding(BaseModel):
      type: str (e.g., "mass_lesion", "atrophy", "white_matter_lesion")
      location: str, size: str | None,
      signal_characteristics: dict[str, str]  # T1, T2, FLAIR, DWI, contrast
      mass_effect: str | None, borders: str | None

  - MRIReport(BaseModel):
      findings: list[MRIFinding]
      volumetrics: dict[str, str] | None
      additional_observations: list[str]
      impression: str
      differential_by_imaging: list[dict[str, str]]
      confidence: float
      recommended_actions: list[str]

  - LabValue(BaseModel):
      test: str, value: float | str, unit: str,
      reference_range: str, is_abnormal: bool,
      clinical_significance: str | None

  - LabResults(BaseModel):
      panels: dict[str, list[LabValue]]  # keyed by panel name: "CBC", "BMP", "CSF", etc.
      interpretation: str
      abnormal_values_summary: list[str]

  - CSFResults(BaseModel):
      appearance: str, opening_pressure: str,
      cell_count: dict[str, str], protein: str, glucose: str,
      glucose_ratio: str, special_tests: dict[str, str],  # e.g. "HSV_PCR": "negative"
      interpretation: str

  - ECGReport(BaseModel):
      rhythm: str, rate: int, intervals: dict[str, str],
      axis: str, findings: list[str], interpretation: str,
      clinical_correlation: str

  - LiteratureSearchResult(BaseModel):
      query: str
      results: list[dict[str, str]]  # source, finding, evidence_level
      summary: str

  - DrugInteractionResult(BaseModel):
      proposed: str, interactions: list[str],
      contraindications: list[str], warnings: list[str],
      formulary_status: str, alternatives: list[str]

TODO-D1.4: Define case schema (case.py)
  - ToolOutputSet(BaseModel):
      """All pre-generated tool outputs for one case."""
      eeg: EEGReport | None
      mri: MRIReport | None
      ecg: ECGReport | None
      labs: LabResults | None
      csf: CSFResults | None
      literature_search: dict[str, LiteratureSearchResult] | None  # keyed by query
      drug_interactions: dict[str, DrugInteractionResult] | None   # keyed by drug

  - FollowUpToolOutput(BaseModel):
      """A conditional tool output triggered by a specific agent request."""
      trigger_action: str  # e.g. "request_contrast_mri", "request_video_eeg"
      tool_name: str
      output: EEGReport | MRIReport | LabResults | CSFResults | ECGReport

  - NeuroBenchCase(BaseModel):
      case_id: str
      condition: NeurologicalCondition
      difficulty: CaseDifficulty
      encounter_type: EncounterType
      patient: PatientProfile
      initial_tool_outputs: ToolOutputSet
      followup_outputs: list[FollowUpToolOutput]
      ground_truth: GroundTruth
      metadata: dict[str, Any]  # generation timestamp, LLM used, validation scores

TODO-D1.5: Define evaluation schemas (evaluation.py)
  - ActionStep(BaseModel):
      step: int, action: str, tool_name: str | None,
      expected_finding: str, category: ActionCategory

  - GroundTruth(BaseModel):
      primary_diagnosis: str
      icd_code: str
      differential: list[dict[str, str]]  # diagnosis, likelihood, key_features
      optimal_actions: list[ActionStep]
      critical_actions: list[str]         # MUST do
      contraindicated_actions: list[str]  # MUST NOT do
      key_reasoning_points: list[str]     # things the agent should mention in its reasoning

TODO-D1.6: Write tests for all schemas
  - Test that example JSON can be parsed into each model
  - Test validation constraints (age 18-90, confidence 0.0-1.0, etc.)
  - Test that serialization round-trips correctly
  - Create a fixture with one complete example case (will be used in agent platform tests too)
```

### Phase 2: Condition Specifications

```
TODO-D2.1: Create conditions.yaml
  For each of the ~30 conditions, define:
  - name, icd_code, description
  - typical_demographics: age_range, sex_bias, prevalence_weight
  - required_modalities: which tools MUST have outputs
  - optional_modalities: which tools MAY have outputs
  - key_findings: per modality, what findings are expected
  - typical_presentation: common symptoms, onset pattern
  - differential_diagnoses: what else it could be confused with
  - difficulty_variants:
      straightforward: typical textbook presentation
      moderate: some atypical features
      diagnostic_puzzle: misleading initial presentation

  Example for one condition:
  ```yaml
  focal_epilepsy_temporal:
    name: "Focal epilepsy — temporal lobe"
    icd_code: "G40.109"
    description: "Focal seizures originating from the temporal lobe"
    typical_demographics:
      age_range: [15, 60]
      sex_bias: null  # equal
      prevalence_weight: 0.08  # 8% of cases
    required_modalities: [EEG, MRI, LABS]
    optional_modalities: [FMRI, ECG]
    key_findings:
      eeg:
        - "Temporal sharp waves or spikes (anterior > posterior)"
        - "Possible intermittent temporal slowing"
      mri:
        straightforward: "Hippocampal sclerosis OR low-grade tumor (DNET/ganglioglioma)"
        moderate: "Subtle hippocampal asymmetry, equivocal"
        diagnostic_puzzle: "Normal MRI (MRI-negative focal epilepsy)"
      labs:
        - "Typically normal"
        - "Post-ictal prolactin may be elevated"
    differential_diagnoses:
      - "Psychogenic non-epileptic seizures"
      - "Syncope"
      - "Migraine with aura"
      - "TIA"
    difficulty_variants:
      straightforward:
        presentation: "Classic temporal aura (déjà vu) → GTC, clear MRI lesion"
        expected_agent_confidence: 0.85
      moderate:
        presentation: "Atypical aura (epigastric rising), subtle MRI finding"
        expected_agent_confidence: 0.65
      diagnostic_puzzle:
        presentation: "Episodes mistaken for panic attacks, normal MRI, subtle EEG"
        expected_agent_confidence: 0.40
  ```

TODO-D2.2: Create demographics.yaml
  Define sampling distributions:
  - age: weighted distribution (peak 40-70 for general neurology)
  - sex: 50/50 default, condition-specific overrides
  - comorbidities: prevalence-weighted random selection
    (hypertension: 30%, diabetes: 15%, depression: 20%, etc.)
  - medications: realistic polypharmacy based on age and comorbidities
```

### Phase 3: Case Generation Engine

```
TODO-D3.1: Implement llm_client.py
  A unified client that wraps the instructor library:

  class LLMClient:
      def __init__(self, config: GenerationConfig):
          # Supports: Anthropic API, OpenAI API, local vLLM endpoint
          # Uses instructor for structured output extraction
          self.client = instructor.from_openai(OpenAI(base_url=config.base_url, api_key=config.api_key))

      def generate(self, response_model: type[BaseModel], messages: list[dict],
                   temperature: float = 0.7, max_retries: int = 3) -> BaseModel:
          """Generate a structured response conforming to the Pydantic model."""
          return self.client.chat.completions.create(
              model=self.config.model_name,
              response_model=response_model,
              messages=messages,
              temperature=temperature,
              max_retries=max_retries  # instructor automatically retries on validation failure
          )

  Key: the instructor library handles Pydantic validation + automatic retries.
  If the LLM returns JSON that doesn't pass validation, instructor re-prompts
  with the validation error until it gets a valid response (up to max_retries).

TODO-D3.2: Implement case_generator.py
  class CaseGenerator:
      def generate_case(self, condition: ConditionSpec, difficulty: CaseDifficulty,
                        demographics: Demographics | None = None) -> PatientProfile:
          """
          Step 1: Generate a complete clinical vignette.

          Uses a detailed prompt that includes:
          - The condition specification (from conditions.yaml)
          - The difficulty variant
          - The demographics (sampled if not provided)
          - Instructions for clinical realism

          Returns a validated PatientProfile Pydantic model.
          """

  The prompt template should be comprehensive (see scenario walkthrough doc for the
  level of detail expected). Key: instruct the LLM to generate the case as if writing
  for a medical board exam — clinically accurate, internally consistent, and at the
  specified difficulty level.

  IMPORTANT: The prompt must include the difficulty-specific key findings from
  conditions.yaml, so the LLM knows what findings the case should have. This
  ensures the clinical narrative will be consistent with the tool outputs
  generated in the next step.

TODO-D3.3: Implement tool_output_generator.py
  class ToolOutputGenerator:
      def generate_tool_outputs(self, patient: PatientProfile,
                                 condition: ConditionSpec,
                                 difficulty: CaseDifficulty) -> ToolOutputSet:
          """
          Step 2: Generate mock tool outputs for the case.

          For each required modality, generate a detailed tool output that is:
          1. Consistent with the clinical narrative
          2. Consistent with the target diagnosis
          3. At the appropriate difficulty level
          4. In the exact Pydantic schema the agent platform expects

          Uses instructor with the specific Pydantic model for each tool output
          (EEGReport, MRIReport, etc.)
          """

  CRITICAL DESIGN DECISION: Generate tool outputs in a SINGLE prompt that includes
  the full patient profile and ALL required modality outputs together. This ensures
  cross-modal consistency (the LLM sees the EEG findings when generating the MRI
  findings). Do NOT generate each modality independently — that's how you get
  inconsistencies.

  The prompt should look like:
  ```
  You are an expert neurologist creating realistic diagnostic results for a
  simulated patient case. You MUST ensure all results are cross-modally consistent.

  PATIENT PROFILE: {patient.model_dump_json()}
  TARGET DIAGNOSIS: {condition.name} ({difficulty.value} difficulty)
  EXPECTED KEY FINDINGS: {condition.key_findings}

  Generate the following tool outputs as a single coherent set.
  For {difficulty.value} difficulty:
  - straightforward: findings clearly point to the diagnosis
  - moderate: some findings are subtle or ambiguous
  - diagnostic_puzzle: initial findings may be misleading

  Generate outputs for: {required_modalities}
  ```

  Use instructor with response_model=ToolOutputSet to get all outputs in one call.

TODO-D3.4: Implement followup_generator.py
  class FollowUpGenerator:
      def generate_followups(self, case: NeuroBenchCase,
                              condition: ConditionSpec) -> list[FollowUpToolOutput]:
          """
          Step 3: Generate conditional follow-up tool outputs.

          For each condition, there are predictable follow-up tests an agent
          might request. Pre-generate results for 10-15 common follow-ups.

          Examples:
          - If agent requests contrast MRI → generate enhanced MRI report
          - If agent requests video-EEG → generate prolonged EEG report
          - If agent requests specific antibody panel → generate result
          - If agent requests lumbar puncture → generate CSF results
          """

  Define common follow-up actions per condition in conditions.yaml, then
  generate the outputs using the same cross-modal consistency approach.

TODO-D3.5: Implement ground_truth_generator.py
  class GroundTruthGenerator:
      def generate_ground_truth(self, case: NeuroBenchCase,
                                 condition: ConditionSpec) -> GroundTruth:
          """
          Step 4: Generate the ground truth evaluation criteria.

          Uses a separate LLM call (or the same one) to produce:
          - Primary diagnosis + ICD code
          - Ranked differential
          - Optimal action sequence (ordered steps)
          - Critical actions (must-do)
          - Contraindicated actions (must-not-do)
          - Key reasoning points (things agent should mention)
          """

  IMPORTANT: Use temperature=0.0 for this step to ensure deterministic,
  accurate ground truth. Consider using a stronger model if the main
  generation model is local/smaller.
```

### Phase 4: Validation Engine

```
TODO-D4.1: Implement cross_modal_consistency.py
  class CrossModalValidator:
      def validate(self, case: NeuroBenchCase) -> ValidationResult:
          """
          Check that findings across modalities are consistent:
          - If EEG shows right temporal focus → MRI should show right temporal
            abnormality (or explicitly be normal if that's the diagnostic puzzle)
          - If labs show CSF pleocytosis → clinical history should mention
            meningeal symptoms (or the agent should discover it)
          - Laterality consistency: all modalities agree on side
          - Temporal consistency: onset dates/durations make sense
          """

  Use an LLM-as-judge call: pass all tool outputs to a strong LLM and ask
  it to identify any inconsistencies. Parse the response into a structured
  ValidationResult with pass/fail and specific issues found.

TODO-D4.2: Implement clinical_plausibility.py
  class ClinicalPlausibilityValidator:
      def validate(self, case: NeuroBenchCase) -> ValidationResult:
          """
          Rule-based + LLM checks:
          - Vital signs in physiological range (HR 40-180, BP 60/30-220/140, etc.)
          - Lab values in physiological range (even abnormal ones)
          - Age-appropriate findings (don't give a 25-year-old severe brain atrophy)
          - Medication doses are realistic
          - Timeline is plausible (symptoms before presentation, not after)
          """

TODO-D4.3: Implement completeness.py
  class CompletenessValidator:
      def validate(self, case: NeuroBenchCase) -> ValidationResult:
          """
          Check that all required fields are populated:
          - All required modalities have tool outputs
          - All tool outputs pass Pydantic validation
          - Ground truth has all required fields
          - At least 5 follow-up outputs are generated
          """
```

### Phase 5: Pipeline Orchestration

```
TODO-D5.1: Implement pipeline.py
  class NeuroBenchPipeline:
      def __init__(self, config_path: str):
          self.config = load_config(config_path)
          self.llm = LLMClient(self.config)
          self.case_gen = CaseGenerator(self.llm)
          self.tool_gen = ToolOutputGenerator(self.llm)
          self.followup_gen = FollowUpGenerator(self.llm)
          self.gt_gen = GroundTruthGenerator(self.llm)
          self.validators = [CrossModalValidator(self.llm),
                             ClinicalPlausibilityValidator(),
                             CompletenessValidator()]

      def generate_dataset(self, target_count: int = 500):
          """
          Main loop:
          1. Sample condition + difficulty + demographics according to distribution
          2. Generate case (clinical vignette)
          3. Generate tool outputs (cross-modal, single prompt)
          4. Generate follow-up outputs
          5. Generate ground truth
          6. Validate (all three validators)
          7. If validation fails → retry (up to 3x) or flag for manual review
          8. Save to disk (JSON)
          9. Checkpoint every N cases
          10. Print running statistics
          """

      def generate_single_case(self, condition: str, difficulty: str) -> NeuroBenchCase:
          """Debug/inspect a single case."""

  Key implementation details:
  - Use asyncio for parallel generation (multiple cases at once)
  - Checkpoint to disk every 50 cases (resume from checkpoint on failure)
  - Save failed cases separately for debugging
  - Log token usage and cost estimates
  - Rich progress bar showing: generated / validated / failed / total

TODO-D5.2: Implement generate_full_dataset.py (CLI entry point)
  @app.command()
  def generate(
      config: str = "config/generation_config.yaml",
      target_count: int = 500,
      resume_from: str | None = None,  # path to checkpoint
      dry_run: bool = False,           # generate 5 cases and stop
  ):
      pipeline = NeuroBenchPipeline(config)
      if resume_from:
          pipeline.load_checkpoint(resume_from)
      pipeline.generate_dataset(target_count)

TODO-D5.3: Implement dataset_statistics.py
  Print:
  - Total cases, by condition, by difficulty
  - Modality coverage (how many cases have EEG, MRI, etc.)
  - Demographic distributions (age histogram, sex ratio)
  - Validation pass rates
  - Average number of follow-up outputs per case
  - Token usage and cost summary
```

### Phase 6: Output Format

```
TODO-D6.1: Define output directory structure
  data/neurobench_v1/
  ├── cases/
  │   ├── FEPI-TEMP-001.json    # One JSON file per case (full NeuroBenchCase)
  │   ├── FEPI-TEMP-002.json
  │   ├── ALZ-EARLY-001.json
  │   └── ...
  ├── longitudinal/
  │   ├── LONG-001/
  │   │   ├── encounter_1.json
  │   │   ├── encounter_2.json
  │   │   └── trajectory.json    # Expected reasoning across encounters
  │   └── ...
  ├── splits/
  │   ├── train.txt              # Case IDs for training (if RL fine-tuning)
  │   ├── val.txt                # Case IDs for validation
  │   └── test.txt               # Case IDs for held-out evaluation
  ├── statistics.json            # Dataset summary statistics
  └── metadata.json              # Generation config, LLM versions, timestamps

TODO-D6.2: Implement longitudinal case generation
  Separately from single-encounter cases, generate 50 multi-encounter patients:
  - Each has 3-5 encounters over months/years
  - Condition evolves (e.g., epilepsy becomes drug-resistant, Alzheimer's progresses)
  - Each encounter is a full NeuroBenchCase
  - trajectory.json defines what the agent should remember and how it should
    reason across encounters

TODO-D6.3: Implement train/val/test splitting
  - 60% train, 15% val, 25% test
  - Stratified by condition and difficulty
  - Longitudinal cases always go in test (they're the hardest evaluation)
  - Ensure no condition has fewer than 5 cases in the test set
```

---

## Estimated Token Usage and Cost

Rough estimates per case (using Claude Sonnet for generation):
- Clinical vignette: ~2K input + ~2K output tokens
- Tool outputs (all modalities): ~3K input + ~4K output tokens
- Follow-up outputs (10 per case): ~15K input + ~10K output tokens
- Ground truth: ~2K input + ~1K output tokens
- Validation (3 validators): ~6K input + ~2K output tokens

**Per case total**: ~28K input + ~19K output ≈ 47K tokens
**500 cases**: ~23.5M tokens

At Claude Sonnet rates (~$3/M input, ~$15/M output):
- Input cost: ~$70
- Output cost: ~$285
- **Total: ~$350 for 500 cases** (very manageable)

For local generation with Qwen3-32B via vLLM: effectively free (compute only).

---

## Key Design Decisions and Rationale

1. **Instructor + Pydantic over raw JSON parsing**: Instructor handles automatic retries on validation failure, reducing the need for custom retry logic. The LLM gets the validation error message and can self-correct.

2. **Single-prompt cross-modal generation**: Generating all tool outputs in one call ensures consistency. The alternative (separate calls per modality) leads to contradictions.

3. **YAML condition specs over hardcoded logic**: Makes it easy to add new conditions, adjust distributions, or modify key findings without changing code.

4. **Shared schemas package**: Both the dataset generator and agent platform import the same Pydantic models. If you change a tool output format, both systems update automatically.

5. **Checkpoint-based generation**: Generating 500 cases will take hours. Checkpointing every 50 cases means you never lose more than 50 cases on a crash.
