# PD-S02

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM) | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 9e04baa6-725a-41b1-b868-dca3f91bd599 | FIXED (D1) | Brain MRI (ground_truth.action_criteria[0], action-1-analyze-brain-mri) changed from required to optional, relabelled 'Consider brain MRI only if an atypical feature or another structural question arises', rationale and citations now NICE NG71 and MDS 2015; stop rule required_before_assessment emptied (max_additional_actions 2). KCE[3] and differential [2] vascular, [3] MSA and [4] PSP now rest on the clinical features, with MRI findings only 'if imaged'; metadata.key_educational_points[2] no longer says MRI is important to exclude causes. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | metadata.difficulty_rationale | Said '1 required criterion (MRI)' | FIXED |
| C | minor | metadata.key_educational_points[2] | Said MRI 'is important to exclude structural causes', contradicting the optional tier (NICE NG71 1.2.9) | FIXED |
| C | minor | fallback_tool_outputs.labs.panels.HbA1c[0].clinical_significance | Null for an abnormal HbA1c 7.0% in known type 2 diabetes on metformin; labs are not a criterion and no management depends on it | FLAGGED |
| A | minor | whole case | Class LIT checked: no literature criterion or stored literature output remains (class LIT, commit 393c547e) | no change |
| B | major | ground_truth.assessment.required_recommendations[0], ground_truth.key_clinical_evidence[1] | Verifier pass 1: the case stores a validated smell test (followup request_olfactory_test, UPSIT 25/40, severe microsmia), which is an MDS 2015 supportive criterion, yet the diagnostic must and KCE[1] said rest tremor is the one supportive criterion with only levodopa able to add one | FIXED: both now say olfactory loss on a validated test, if obtained (UPSIT 25/40, severe microsmia), is a second supportive criterion and makes it clinically established (as in PD-S04..S06); revision_reason updated |

## Changes
This is clinically typical asymmetric rest-tremor PD with no red flag, so brain MRI is now optional and no longer needed before the diagnosis is submitted (NICE NG71 1.2.9); the case has no required test. The MRI evidence line and the vascular, MSA and PSP differential entries now argue from the clinical features, with the MRI only 'if imaged', and the educational point on MRI says the same. The stored MRI report, the oxybutynin must and the other musts are unchanged. metadata.difficulty_rationale, revision_reason and last_revised (2026-11-16) updated.

## Verification
perfect_agent.py: ok (empty required work-up, submits directly). mri_probe.py: stored plain MRI answers the optional criterion. test_case_guards.py -k PD-S01..S06: 48 passed. case_io.py check: schema and synonym guard OK; the only failure naming PD is test_panel_case_contract for PD-RM05 (not this case).
Pass 1: 1 errors found
- Note 9e04baa6 ruling (FIXED, D1) checked and correct: MRI optional with the D1 label and rationale, stop rule empty with max 2, KCE and differential in the D1 'if imaged' form, no must cites the MRI, no MRI->DaTscan constraint, no literature step left.
- Error (internal contradiction): stored validated smell test (UPSIT 25/40, severe microsmia) is an MDS supportive criterion, but REQ[0] and KCE[1] denied a second supportive criterion. Fixed in REQ[0], KCE[1] and metadata.revision_reason.
Cosmetic (not counted): none.
Checks after pass 1: perfect_agent.py -v ok; every optional criterion probed and answered by its own stored output (no fallback, no avoided-action match); test_case_guards -k PD-S01..S06: 48 passed; case_io.py check: schema and synonym guard OK, the only failures are the central test_guidance_claims PD rows (labs, ECG), which name other PD cases.
Pass 2: 0 errors found
- Note ruling re-checked against plan D1/D2 and NICE NG71 1.2.9-1.2.10: correct; the case does what the note asks (imaging optional, out of the stop rule, evidence and differential in the D1 'if imaged' form, no must cites imaging, no imaging-before-DaTscan constraint, no literature step).
- Pass-1 smell-test supportive-criterion wording checked against MDS 2015 (olfactory loss on a validated test is supportive criterion 4; two supportive with no red flag = clinically established) and the UPSIT age/sex bands: correct.
- Checked: laterality of exam, DaTscan and fallback levodopa challenge; handedness vs micrographia; medications vs musts, prohibitions and the stored drug-interaction output (no expected-evidence echo); avoided actions vs criteria (no overlap); no answer leakage in the patient block; every optional criterion probed and answered by its own stored output (no fallback, no avoided-action match).
Cosmetic (not counted): none.
Checks after pass 2: perfect_agent.py -v ok; test_case_guards -k PD-S01..S06: 48 passed; case_io.py check: schema and synonym guard OK, the only failures are the central test_guidance_claims PD rows (labs, ECG), which name other PD cases.
