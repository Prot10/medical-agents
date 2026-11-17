# PD-RS01

## Reviewer notes
Reviewer status: R1 in_progress | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 582e1ee0-bba8-4bcf-b975-dc9c7cd2ea7f | FIXED (D26) | `ground_truth.assessment.required_recommendations[1]` D26 canonical text; `ground_truth.diagnosis.rejected` 'lithium induced tremor' removed ('lithium induced parkinsonism' kept; tested with DiagnosisCriterion.matches: "Parkinson's disease", "Probable Parkinson's disease" and "Idiopathic Parkinson's disease with a lithium-related postural tremor component" match; "Lithium-induced parkinsonism", "Drug-induced parkinsonism", "Lithium induced tremor" do not); `ground_truth.differential[0]` 'Possible contributor' (low); class alignment of `ground_truth.key_clinical_evidence[3]` and `ground_truth.red_herrings[0].correct_interpretation` |
| 1d3af06d-d343-4919-9b88-4b2f0f80ae98 | FIXED (D14) | `ground_truth.assessment.required_recommendations[3]` D14 canonical text plus the NICE ICD/EDS warning if an agonist is used |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.action_criteria[0], ground_truth.stop_rule | Class D1 (plan C1, unnoted case): typical PD with MRI required and in the stop rule | FIXED (MRI optional, label 'Consider brain MRI only if an atypical feature or another structural question arises', rationale citing NICE NG71 and MDS 2015; stop rule []) |
| C | minor | ground_truth.sequence_constraints[0] | Unsourced MRI-before-DaTscan soft constraint (class D2) | FIXED (deleted) |
| C | minor | ground_truth.key_clinical_evidence[4], ground_truth.differential[3], [4], [5] | MRI-based evidence after the MRI left the pathway ([4] MSA also carried an MRI clause, beyond the plan's list) | FIXED (D1 forms) |
| C | minor | ground_truth.key_clinical_evidence[1] | Optional UPSIT result stated as established (plan F4) | FIXED ('if a validated smell test is obtained') |
| B | minor | metadata.difficulty_description, metadata.difficulty_rationale, metadata.revision_reason, metadata.last_revised | 'lithium ... causes postural rather than rest tremor' framing and '1 required criterion (MRI)' | FIXED |
| - | - | whole case | Checked: lithium level 0.72 in the lab panel served for the recommended lab criterion; drug output flags lisinopril-lithium and bipolar risk; PRO[1] (no abrupt lithium stop) consistent with the new must; no literature output; no gadolinium MRI | no change |

## Changes
The lithium must no longer implies that a therapeutic level excludes a lithium effect: PD stays the leading diagnosis, but chronic lithium may contribute to tremor or parkinsonism even at 0.72 mEq/L, any change is coordinated with psychiatry without abrupt withdrawal, and the level and renal function are monitored because of lisinopril. 'Lithium induced tremor' no longer vetoes an answer (his postural tremor component may be lithium-related); the lithium differential is a low-likelihood possible contributor. The bipolar must now asks for psychiatric coordination and monitoring for hypomania, mania, psychosis and impulse-control symptoms during levodopa initiation and titration, and avoidance or particular caution with dopamine agonists. As a class change for clinically typical PD (NICE NG71 1.2.9) the MRI is optional and out of the stop rule, and the MRI-before-DaTscan constraint is gone; the lithium level and the medication review stay recommended. Evidence lines mention MRI and smell-test results only 'if obtained'.

## Verification
perfect_agent.py -v: ok; mri_probe.py: plain MRI only, no gadolinium content; test_case_guards.py -k (6 cases): 48 passed; case_io.py check: schema and synonym guard OK, no failure names this case (remaining failures: test_guidance_claims PD rows, central, and PD-RM05 zero-cost required set, another worker's case).

Pass 1: 0 errors found
- Re-read the notes, rulings, plan entries and the diff, and read the final case in full. Every note has a correct FIXED ruling, and the edits match the plan's canonical text. No contradiction (laterality, orthostatic figures, MoCA subscores, medications against the drug output, rejected labels against the differential), no leakage, no stop-rule or sequence id error. No material error.
- Cosmetic (not counted): none.
- Checks re-run by the verifier: perfect_agent.py -v ok; mri_probe.py plain MRI only; test_case_guards -k (6 cases) 48 passed; case_io.py check schema and synonym guard OK, the only failures are the central test_guidance_claims PD rows (labs, ECG).
