# PD-P04

## Reviewer notes
Reviewer status: R1 in_progress, R2 none | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 56aee7f4-5ebd-4591-9c75-21801a942cc6 | FIXED (plan D12) | `ground_truth.action_criteria[1]` (`action-4-interpret-labs`): required -> optional, label 'Copper studies if Wilson disease is still considered', rationale rewritten ([EASL_ERN_Wilson_2025]); `ground_truth.stop_rule.required_before_assessment` now [`action-1-analyze-brain-mri`]; `required_recommendations[1]` canonical (consider Wilson with onset at 41, now 42, slit-lamp normal, if screened ceruloplasmin with 24-h urinary copper first); `key_clinical_evidence[2]` and `differential[0].key_features` cite the copper values only 'if copper studies are obtained'; `metadata.difficulty_rationale` updated. `wilson disease` stays rejected. Optional chosen over recommended: no verified age threshold makes screening standard here. |
| 3ed94a70-4c7c-437f-ad9c-ca01654d7fd9 | FIXED (plan D13) | `required_recommendations[2]`: levodopa first line because the motor symptoms impair work and quality of life (dose and titration given), agonist or MAO-B inhibitor as alternatives by preference and risk, ICD/EDS warning for agonists [NICE_NG71]; `key_clinical_evidence[5]` rewritten to the same point. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| B | minor | patient.clinical_history.family_history[4] | 'No known family history of ... other movement disorders' beside a maternal uncle with an undiagnosed tremor (class D7) | FIXED: 'No known family history of Wilson's disease, dystonia or parkinsonism' |
| C | minor | ground_truth.sequence_constraints | Unsourced soft 'MRI before DaTscan' constraint (class D2) | FIXED: deleted |

## Changes
Young-onset PD at 42 stays the diagnosis and the MRI stays required (onset before 50). Wilson disease is now considered rather than mandatorily screened: the slit-lamp is normal, the copper studies are optional and no longer in the stop rule, and the must says that if screening is done, ceruloplasmin with 24-hour urinary copper is the first step (EASL-ERN 2025); the evidence and differential cite the normal copper values only if obtained. Treatment now starts with levodopa as first line because tremor and slowness impair his work (NICE NG71 1.3.1), with agonists and MAO-B inhibitors as alternatives to discuss and the impulse-control and sleepiness warning for agonists. The family history now reads 'no known family history of Wilson's disease, dystonia or parkinsonism', so it no longer contradicts the uncle's tremor, and the unsourced MRI-before-DaTscan constraint was removed.

## Verification
perfect_agent.py -v: ok (every required/recommended criterion answered from the case's own stored data). test_case_guards.py -k (six PD worker cases): 48 passed. case_io.py check: schema and synonym guard OK; the only failures naming PD are test_guidance_claims PD rows (central, plan CENTRAL 3) and a zero-cost required set in PD-RM05 (another worker's case).
Pass 1: 0 errors found
- Checked: copper studies optional and out of the stop rule (now [MRI], a required criterion); REQ[1] and REQ[2] canonical (D12, D13); evidence and differential copper values in the 'if obtained' form; 'no hepatic or psychiatric history' agrees with the HPI; family history D7; constraint deleted. No change.
Checks after pass 1: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
Pass 2: 1 errors found
- `ground_truth.assessment.required_recommendations[1]` said "at onset age 42", but the HPI dates the onset 14 months before this visit at 42 (about 41), as the dopa-responsive dystonia differential already says ("Onset at 41"). Changed to "Consider Wilson disease with onset at 41 (now 42): ..."; rulings file and the note row updated.
Checks after pass 2: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
Pass 3: 0 errors found
- Checked: copper studies optional, out of the stop rule (now [MRI], a required criterion); REQ[1] and REQ[2] per D12, D13 and both notes; copper and liver values cited only 'if obtained' (they are in the same stored labs report); 'no hepatic or psychiatric history' agrees with the HPI; family history D7; onset age 41 agrees with the dopa-responsive dystonia entry; constraint deleted. No change.
Checks after pass 3: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
Pass 4: 0 errors found
- Checked: copper studies optional and out of the stop rule (now [MRI], a required criterion); REQ[1] per D12 and the note (slit-lamp documented in the cranial-nerve exam; onset 14 months ago at 41); REQ[2] and KCE[5] per D13 and NICE NG71 1.3.1; copper and liver values only 'if obtained'; 'no hepatic or psychiatric history' and 'no dystonic feature' agree with the HPI and the dopa-responsive dystonia entry; family history D7; constraint deleted; matcher: 'Young-onset Parkinson's disease' matches, 'Wilson disease' does not. No change.
Checks after pass 4: perfect_agent.py -v ok; test_case_guards.py -k (six cases) 48 passed; case_io.py check: schema and synonym guard OK, the only PD failures are the two test_guidance_claims rows (central, plan CENTRAL 3).
