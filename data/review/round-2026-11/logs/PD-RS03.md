# PD-RS03

## Reviewer notes
Reviewer status: R1 in_progress | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| ec3fb0d3-edaa-4ec9-8a89-ef737d3a9f0d | FIXED (D28) | `patient.neurological_exam.motor` 'Pisa syndrome noted with trunk leaning to the left' -> 'Leftward lateral trunk flexion of about 8 degrees when standing, fully corrected when supine and on passive correction'; `ground_truth.assessment.required_recommendations[4]` physiotherapy for 'leftward lateral trunk flexion and stooping' with reassessment of the degree [Tinazzi_2022]; `ground_truth.differential[1]` (MSA) and `ground_truth.key_clinical_evidence[3]` state 8 degrees, reversible, below the 10-degree Pisa threshold [Tinazzi_2022][Wenning_2022]; `metadata.difficulty_description`, `metadata.difficulty_rationale` 'Pisa' replaced |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.action_criteria[0], ground_truth.stop_rule | Class D1 (plan C1, unnoted case): clinically typical asymmetric rest-tremor PD with MRI required and in the stop rule | FIXED (MRI optional, label 'Consider brain MRI only if an atypical feature or another structural question arises', rationale citing NICE NG71 and MDS 2015; stop rule [] ) |
| C | minor | ground_truth.key_clinical_evidence[2], ground_truth.differential[0], [1], [6] | MRI-based evidence after the MRI left the pathway | FIXED (D1 'if MRI is obtained' / 'and, if imaged') |
| C | minor | ground_truth.differential[3], ground_truth.red_herrings[0].correct_interpretation | Cited the optional B12/copper/ceruloplasmin results as established (plan F4) | FIXED ('if measured') |
| B | minor | metadata.revision_reason, metadata.last_revised | Updated | FIXED |
| - | - | whole case | Checked: MoCA 26 subscores, orthostatic 12/6, battery impression vs rows, DaTscan laterality, no literature output, no gadolinium MRI; no stored report mentions the trunk posture (the HPI 'appears to lean to one side' is the daughter's description, consistent with the exam) | no change |

## Changes
The trunk posture is now documented as a leftward lateral trunk flexion of about 8 degrees on standing that corrects fully when supine and on passive correction, and it is no longer called Pisa syndrome anywhere (Pisa syndrome needs more than 10 degrees, MDS task force 2022); the physiotherapy must keeps postural rehabilitation and asks to reassess the degree at follow-up, and the PD label is unchanged. As a class change for clinically typical PD (NICE NG71 1.2.9), the brain MRI is now optional and no longer required before the diagnosis, so the case has no required test; the MRI evidence and the vascular, MSA and PSP differential entries argue from the clinical findings, with MRI only 'if imaged'. The nutritional differential and the bypass red herring cite the (optional) B12 and copper results only 'if measured'.

## Verification
perfect_agent.py -v: ok; mri_probe.py: plain MRI only, no gadolinium content; test_case_guards.py -k (6 cases): 48 passed; case_io.py check: schema and synonym guard OK, no failure names this case (remaining failures: test_guidance_claims PD rows, central, and PD-RM05 zero-cost required set, another worker's case).

Pass 1: 0 errors found
- Re-read the note, ruling, D1/D28 and the diff, and read the final case in full. The 8-degree reversible lateral trunk flexion is consistent across the exam, must, MSA differential, KCE and metadata, and "Pisa syndrome" is no longer asserted. The MRI is optional with an empty stop rule; the optional labs are stated "if measured"; the orthostatic figures (12/6, HR +8) and MoCA subscores (sum 26) are consistent. No material error.
- Cosmetic (not counted): the log's own-findings row said that the gait and levodopa-challenge reports carry "leftward trunk lean" wording. No stored report mentions the posture, so the row is corrected (log only; no case change).
- Checks re-run by the verifier: perfect_agent.py -v ok; mri_probe.py plain MRI only; test_case_guards -k (6 cases) 48 passed; case_io.py check schema and synonym guard OK, the only failures are the central test_guidance_claims PD rows (labs, ECG).
