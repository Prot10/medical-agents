# NeuroBench v2 case contract

Each case validates as `NeuroBenchCase` with `schema_version: "2.0"`.

Top-level fields describe the patient, initial outputs, conditional follow-up outputs, fallback outputs and clinician-reviewable ground truth. The fallback tier makes off-path agent actions return coherent results instead of failing the simulation.

The ground-truth policy contains:

| Field | Meaning |
|---|---|
| `review_status` | `draft`, `needs_revision` or physician `approved` |
| `diagnosis` | accepted labels and ICD codes |
| `differential` | plausible alternatives and distinguishing features |
| `action_criteria` | evidence goals with set-valued tool-call alternatives |
| `avoided_actions` | wasteful, harmful or contraindicated call patterns |
| `sequence_constraints` | soft workflow or hard safety ordering |
| `stop_rule` | required evidence before assessment and action allowance |
| `assessment` | required and prohibited final recommendations |
| `key_clinical_evidence` | observable evidence, never private reasoning |
| `red_herrings` | misleading findings and their correct interpretation |

Criterion IDs are unique and lowercase. Stop and sequence references must resolve to an existing action criterion. A case never creates a fake action merely to make a reference valid.

See `dataset-generation/POLICY_AUTHORING_GUIDE.md` for authoring and review rules.
