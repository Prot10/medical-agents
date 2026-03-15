You are an expert neurologist and medical educator creating a realistic simulated patient case for a neurology AI diagnostic benchmark called NeuroBench.

## Task

You are given a **real published clinical case report** as a seed. Your job is to use this real case as the clinical foundation and transform it into a complete NeuroBench case with structured tool outputs that force an AI agent to use diagnostic tools.

Generate a COMPLETE patient case as a single JSON object conforming EXACTLY to the schema below. Output ONLY valid JSON — no markdown fences, no commentary, no explanation before or after.

## JSON Schema

The output must conform to this exact schema:

{json_schema}

## Source Case (Real Published Case Report)

**Source**: {source_journal} (PMCID: {source_pmcid})
**Original diagnosis**: {source_diagnosis}

### Clinical Presentation (from published case):
{source_case_prompt}

### Published Diagnostic Reasoning:
{source_reasoning}

## Case Parameters

- **Case ID**: `{case_id}`
- **Condition**: `{condition_name}`
- **Difficulty**: `{difficulty}`
- **Encounter type**: `{encounter_type}`

## Condition Specifications

{condition_yaml}

## Instructions for Seed-Based Case Generation

### 1. USE the real case as your clinical foundation
- The patient demographics, clinical history, presenting symptoms, and exam findings should be **inspired by** the real case
- You may modify demographics (age, sex, ethnicity) slightly for diversity, but keep the clinical scenario realistic and consistent with the source
- The HPI should reflect the same clinical trajectory as the source case, written as a detailed narrative (at least 150 words)
- Preserve the clinical complexity and atypical features from the real case — these are what make it realistic

### 2. SEPARATE presentation from diagnostic evidence
This is critical: the source case text often mentions diagnostic results inline (e.g., "MRI showed periventricular lesions"). You must:
- **REMOVE** diagnostic test results from the HPI and patient presentation
- Instead, place them in the structured **tool outputs** (MRI report, lab results, EEG report, CSF results, ECG)
- The patient presentation should describe symptoms and exam findings, but NOT reveal what the tests showed
- This forces the AI agent to **call diagnostic tools** to discover the evidence

### 3. ADD disguising information and red herrings (especially for moderate/puzzle difficulty)
- **STRAIGHTFORWARD**: Findings clearly support the diagnosis. Minimal confounders.
- **MODERATE**: Add 1-2 incidental/confounding findings:
  - An incidental lab abnormality (e.g., mildly elevated TSH in a stroke patient)
  - A borderline imaging finding that could suggest an alternative diagnosis
  - A medication that could cause some of the symptoms
  - A family history item that points to a different condition
- **DIAGNOSTIC PUZZLE**: Add significant misdirection:
  - Initial presentation mimics a different condition
  - Key diagnostic test is initially equivocal or negative
  - Red herring findings that suggest a more common diagnosis
  - The critical diagnostic clue is buried in follow-up results, not initial tests

### 4. GENERATE structured tool outputs
Create detailed specialist reports for the required modalities. Each report should:
- Read like a real radiologist/pathologist/technician wrote it
- Contain the key diagnostic findings from the source case (now extracted from the narrative)
- Include realistic normal and incidental findings alongside pathological ones
- Have appropriate confidence levels and recommended actions
- Be internally consistent with each other and the patient presentation

### 5. GENERATE follow-up outputs (at least 5)
Create conditional outputs that an agent could request:
- Additional imaging (repeat MRI, CT angiography, DaTscan, VEP, etc.)
- Additional labs (autoimmune panels, genetic testing, specialized markers)
- Additional tests (repeat LP, EEG monitoring, autonomic testing)
- Literature searches and drug interaction checks
- These should include both useful and less-useful follow-ups to test the agent's clinical judgment

### 6. BUILD ground truth from the source case's reasoning
- Use the published `diagnostic_reasoning` to inform your `key_reasoning_points`
- Map the source's differential diagnosis discussion to structured `differential` entries
- Create a realistic `optimal_actions` sequence that a competent neurologist would follow
- Include `critical_actions` (must-do) and `contraindicated_actions` (must-not-do)

### 7. METADATA
Include in metadata:
- `"source": "MedCaseReasoning"`
- `"source_pmcid": "{source_pmcid}"`
- `"source_license": "CC-BY 4.0"`
- `"generation_method": "real_case_seed"`
- `"condition_name"`: human-readable condition name
- `"difficulty_description"`: what makes this case this difficulty level
- `"expected_agent_confidence"`: 0.80-0.90 for straightforward, 0.55-0.70 for moderate, 0.30-0.45 for puzzle

## Clinical Realism Requirements

1. **Cross-modal consistency**: ALL tool outputs must be internally consistent with each other AND with the clinical narrative.
2. **Lab values**: Use specific numeric values with correct units and reference ranges. Mark abnormal values correctly. Include complete panels (CBC, BMP at minimum).
3. **Medications**: Use real drug names with realistic doses and frequencies. Include indication for each medication.
4. **Neurological exam**: Write a complete neurological examination appropriate to the condition and difficulty level.
5. **Vital signs**: Use physiologically realistic values adjusted for the clinical scenario.

## Output Format

Output a single JSON object. No wrapping, no explanation. Just the JSON.
