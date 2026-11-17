# PD-S04

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM) | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 5ee462a7-598c-4fbb-8638-ae9ea3fcc1ba | FIXED (D1) | Brain MRI (ground_truth.action_criteria[0], action-1-analyze-brain-mri) changed from required to optional, relabelled 'Consider brain MRI only if an atypical feature or another structural question arises', rationale and citations now NICE NG71 and MDS 2015; stop rule required_before_assessment emptied (max_additional_actions 2). KCE[3] and differential [2] vascular and [3] MSA now rest on the clinical features, with MRI findings only 'if imaged'. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | metadata.difficulty_rationale | Said '1 required criterion (MRI)' | FIXED |
| C | minor | metadata.estimated_complexity | Described the case by its 'normal structural imaging'; imaging is now optional | FIXED |
| B | minor | patient.chief_complaint vs history_present_illness | Chief complaint 'worsening over the past two years', HPI onset two and a half years ago; compatible (worsening vs first notice) | no change |
| A | minor | whole case | Class LIT checked: no literature criterion or stored literature output remains (class LIT, commit 393c547e) | no change |

## Changes
This is clinically typical asymmetric rest-tremor PD with no red flag, so brain MRI is now optional and no longer needed before the diagnosis is submitted (NICE NG71 1.2.9); the case has no required test (smell test and medication review stay optional). The MRI evidence line and the vascular and MSA differential entries now argue from the clinical features, with the MRI only 'if imaged'. The stored reports and the musts, including the driving must, are unchanged. metadata.difficulty_rationale, revision_reason and last_revised (2026-11-16) updated.

## Verification
perfect_agent.py: ok (empty required work-up, submits directly). mri_probe.py: stored plain MRI answers the optional criterion. test_case_guards.py -k PD-S01..S06: 48 passed. case_io.py check: schema and synonym guard OK; the only failure naming PD is test_panel_case_contract for PD-RM05 (not this case).
Pass 1: 0 errors found
- Note 5ee462a7 (FIXED, D1) checked and correct: MRI optional with the D1 label and rationale, stop rule empty, KCE[3] and differential [2], [3] in the D1 form; UPSIT result written 'when tested' in REQ[0].
Cosmetic (not counted): none.
Checks after pass 1: perfect_agent.py -v ok; every optional criterion probed and answered by its own stored output (no fallback, no avoided-action match); test_case_guards -k PD-S01..S06: 48 passed; case_io.py check: schema and synonym guard OK, the only failures are the central test_guidance_claims PD rows (labs, ECG), which name other PD cases.
Pass 2: 0 errors found
- Note ruling re-checked against plan D1/D2 and NICE NG71 1.2.9-1.2.10: correct; the case does what the note asks (imaging optional, out of the stop rule, evidence and differential in the D1 'if imaged' form, no must cites imaging, no imaging-before-DaTscan constraint, no literature step).
- Pass-1 smell-test supportive-criterion wording checked against MDS 2015 (olfactory loss on a validated test is supportive criterion 4; two supportive with no red flag = clinically established) and the UPSIT age/sex bands: correct.
- Checked: laterality of exam, DaTscan and fallback levodopa challenge; handedness vs micrographia; medications vs musts, prohibitions and the stored drug-interaction output (no expected-evidence echo); avoided actions vs criteria (no overlap); no answer leakage in the patient block; every optional criterion probed and answered by its own stored output (no fallback, no avoided-action match).
Cosmetic (not counted): none.
Checks after pass 2: perfect_agent.py -v ok; test_case_guards -k PD-S01..S06: 48 passed; case_io.py check: schema and synonym guard OK, the only failures are the central test_guidance_claims PD rows (labs, ECG), which name other PD cases.
- Condition audit (17 Nov 2026): `ground_truth.key_clinical_evidence[1]` gave the UPSIT score of the optional smell test without the 'if obtained' form (plan F4; S01-S03, RS01, RS05, M05 and RM04 already use it). Added ', if obtained' after the score. No other change. perfect_agent passes; case_io check: no failure names this case apart from the centrally maintained test_guidance_claims.

Pass 4: 0 errors found
Pass 4 (focused verifier, 17 Nov 2026) checked the condition-audit change: `ground_truth.key_clinical_evidence[1]` now gives the UPSIT score of the optional olfactory-test criterion in the 'if obtained' form (plan F4); the score matches the stored UPSIT report, the criterion expected_evidence and the diagnosis must ('when tested'). perfect_agent passes; test_case_guards passes for the case. No change.
