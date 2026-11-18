# PD-RP05

## Reviewer notes
Reviewer status: R1 in_progress | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 61f2065e-38b7-4007-b3a2-b84430cb651c | FIXED (D25) | `ground_truth.action_criteria[1]` (action-5-order-advanced-imaging) recommended -> optional, label 'only if diagnostic uncertainty ... persists', rationale non-specific for PD [Marshall_2009]; `ground_truth.assessment.required_recommendations[1]` DaTscan clause dropped (rests on the clinical picture and MRI without lacunes); `ground_truth.differential[0]` and `[1]` DaTscan only 'if obtained'; `ground_truth.key_clinical_evidence[4]` 'If a DaTscan is obtained ... not specific for PD'; `ground_truth.red_herrings[0].correct_interpretation`; `ground_truth.avoided_actions[4]` (amyloid PET) rationale; `ground_truth.sequence_constraints[0]` soft MRI-before-DaTscan kept with the D2 reason and empty citations |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | ground_truth.key_clinical_evidence[3] | Swallow-tail sign presented as evidence without its limits (class D9) | FIXED (D9 canonical: not specific, not a diagnostic criterion) |
| B | minor | ground_truth.action_criteria[0].rationale | 'MRI is normal in PD' in a case whose MRI shows Fazekas 2 change and whose referral question is vascular | FIXED (rationale states the vascular question, lacunes, NPH and atypical signs; citations [NICE_NG71][Postuma_2015][Schwarz_2014]) |
| C | minor | ground_truth.key_clinical_evidence[1] | Optional UPSIT result stated as established (plan F4) | FIXED ('if a validated test is obtained') |
| C | minor | ground_truth.sequence_constraints[0] | Reason cited [Postuma_2015], which does not state the rule (D2) | FIXED (D2 case-specific reason, no citation) |
| B | minor | metadata.difficulty_rationale, metadata.revision_reason, metadata.last_revised | '1 recommended (DaTscan)' | FIXED |
| - | - | whole case | MRI stays required (vascular question, plan C1). Checked: DaTscan right-putamen deficit opposite the left-sided signs, nigrosome laterality right, MoCA 26 subscores, drug output (amantadine renal note, CKD 2), no literature output, no gadolinium MRI | no change |

## Changes
The DaTscan is now optional: the clinical picture (asymmetric, upper-limb predominant rest-tremor parkinsonism, insidious course, preserved lower-limb gait) and the MRI (Fazekas 2 without basal ganglia, thalamic or capsular lacunes) already favour PD over vascular parkinsonism, and an abnormal DaTscan is not specific for PD and does not exclude a vascular contribution. The must on the white matter change, the vascular and drug-induced differential entries, the red herring and the amyloid-PET waste rationale now rest on the clinical findings and the MRI; DaTscan and smell-test results appear only 'if obtained'. The swallow-tail evidence now says the sign is consistent with nigral degeneration but not specific and not a diagnostic criterion. The MRI stays required (vascular referral question) with a rationale that states it, and the soft rule 'MRI before DaTscan' is kept with a case-specific reason (a basal ganglia vascular lesion can itself reduce striatal binding).

## Verification
perfect_agent.py -v: ok; mri_probe.py: plain MRI only, no gadolinium content; test_case_guards.py -k (6 cases): 48 passed; case_io.py check: schema and synonym guard OK, no failure names this case (remaining failures: test_guidance_claims PD rows, central, and PD-RM05 zero-cost required set, another worker's case).

Pass 1: 0 errors found
- Checked the D25 ruling (DaTscan optional, REQ[1] without the DaTscan, vascular and drug-induced differential, red herring, amyloid-PET rationale), D9 swallow-tail wording, kept soft constraint (both ids exist, empty citations), MRI rationale, stop rule [MRI], MoCA subscores (sum 26), DaTscan and nigrosome laterality against the left-sided signs, drug output against medications and CKD 2, no leakage in the patient block or reports. No material error.
- Cosmetic (not counted): `ground_truth.action_criteria[1].rationale` "abnormal DaT scan" -> "abnormal DaTscan" (the case's spelling elsewhere).
- Checks re-run by the verifier: perfect_agent.py -v ok; mri_probe.py plain MRI only; test_case_guards -k (6 cases) 48 passed; case_io.py check schema and synonym guard OK, the only failures are the central test_guidance_claims PD rows (labs, ECG).
