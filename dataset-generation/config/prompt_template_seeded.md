You are an expert neurologist and medical educator creating a realistic simulated patient case for NeuroBench, a clinical-agent benchmark.

## Task

Use the real published case below as the clinical foundation for one complete NeuroBench case. The case must let an agent choose any available action, discover evidence through tools, stop when justified, and submit an assessment.

Output exactly one JSON object conforming to the supplied schema. Output no markdown or commentary.

## JSON schema

{json_schema}

## Source case

**Source**: {source_journal} (PMCID: {source_pmcid})
**Original diagnosis**: {source_diagnosis}

### Clinical presentation

{source_case_prompt}

### Published clinical reasoning

{source_reasoning}

## Case parameters

- Case ID: `{case_id}`
- Condition: `{condition_name}`
- Difficulty: `{difficulty}`
- Encounter type: `{encounter_type}`

## Condition specification

{condition_yaml}

## Authoring requirements

### Preserve the clinical case without leaking answers

- Base demographics, chronology, symptoms, examination and complexity on the source.
- Minor demographic changes are allowed for diversity when clinically coherent.
- Write a detailed HPI of at least 150 words.
- Remove diagnostic test results and the final diagnosis from the presentation. Put discoverable results in tool outputs.
- Keep every patient field and tool result mutually consistent.

### Simulate the patient at 360 degrees

- Populate the presentation, history, medications, allergies, vital signs and complete relevant neurological examination.
- Provide realistic initial, follow-up and fallback outputs so both useful and off-path actions return clinically coherent observations.
- Use numeric laboratory values with units and reference ranges.
- Use real medications with realistic doses, frequencies and indications.
- Include at least five conditional follow-up outputs, spanning useful and less-useful actions where clinically appropriate.

### Calibrate difficulty

- Straightforward: clear supporting findings and minimal confounding.
- Moderate: one or two plausible incidental or misleading findings.
- Diagnostic puzzle: a plausible mimic, equivocal early evidence or a decisive clue discoverable only through follow-up.

### Author a policy, not a golden trajectory

Set `schema_version` to `"2.0"` and `ground_truth.review_status` to `"draft"`. Synthetic generation can never mark a policy approved.

The ground truth must contain:

- `diagnosis.accepted`: all defensible names that should count as correct.
- `diagnosis.icd_codes`: applicable codes.
- `differential`: plausible alternatives with likelihood and distinguishing features.
- `action_criteria`: clinically meaningful evidence goals. Every criterion has a unique lowercase `criterion_id`, label, importance, one or more interchangeable tool-call patterns in `alternatives`, expected evidence, rationale and citations.
- `avoided_actions`: case-specific wasteful, harmful or contraindicated calls, expressed as tool-call patterns with rationale and citations. Do not penalize a reasonable alternative merely because it differs from one preferred workflow.
- `sequence_constraints`: only clinically meaningful ordering relations between existing action-criterion IDs. Use `hard` only for safety-critical ordering. Omit a constraint if either referenced criterion is absent; never invent an action criterion solely to satisfy a sequence.
- `stop_rule.required_before_assessment`: existing required criterion IDs that must be satisfied before assessment.
- `stop_rule.max_additional_actions`: a small defensible allowance after the stop condition is met.
- `assessment.required_recommendations` and `assessment.prohibited_recommendations`.
- `key_clinical_evidence`: observable evidence, not hidden chain-of-thought.
- `red_herrings`: misleading data with its location, intended effect and correct interpretation.

Do not create reasoning traces, thought text, ReAct transcripts or one canonical action order. The policy must score multiple clinically equivalent paths.

### Metadata

Include:

- `"source": "MedCaseReasoning"`
- `"source_pmcid": "{source_pmcid}"`
- `"source_license": "CC-BY 4.0"`
- `"generation_method": "real_case_seed"`
- a human-readable condition name
- a difficulty description
- expected agent confidence: 0.80–0.90 for straightforward, 0.55–0.70 for moderate, 0.30–0.45 for puzzle

## Output

Return one valid JSON object only.
