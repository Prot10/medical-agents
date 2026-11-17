# PD-S06

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM) | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 5dcbd891-3b5f-4672-89f1-bafa55583171 | FIXED (D1, D2) | Head CT (ground_truth.action_criteria[0], action-3-order-ct-scan) changed from required to optional, relabelled 'Consider non-contrast head CT only if structural imaging becomes indicated (MRI declined for claustrophobia)', rationale NICE NG71 and MDS 2015 with the lower CT sensitivity noted; stop rule required_before_assessment emptied; the soft CT-before-DaTscan constraint deleted; KCE[4] stated as 'if obtained'; metadata.panel_required_exemptions.analyze_brain_mri kept, reworded. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| B | major | patient.demographics.handedness, patient.history_present_illness | Recorded right-handed, yet she 'has stopped using left-handed scissors' and has smaller handwriting with left-sided PD (class D8 from note b468a5e6 on PD-M05) | FIXED |
| C | minor | metadata.panel_required_exemptions.analyze_brain_mri | Called CT 'required'; reworded to optional | FIXED |
| C | minor | metadata.difficulty_rationale | Said '1 required criterion (CT)' | FIXED |
| A | minor | whole case | Class LIT checked: no literature criterion or stored literature output remains (class LIT, commit 393c547e) | no change |

## Changes
This is clinically typical asymmetric rest-tremor PD with no red flag; MRI was declined for claustrophobia, and head CT is now optional rather than required, since structural imaging is not needed to diagnose typical PD (NICE NG71 1.2.9); it is no longer needed before the diagnosis is submitted, and the soft rule that CT must precede the DaTscan was deleted. The CT evidence line is stated as 'if obtained'. The patient is now recorded as left-handed (demographics and HPI), consistent with her left-handed scissors and her smaller handwriting on the affected left side. The stored CT report, the DaTscan and the musts are unchanged. metadata.difficulty_rationale, revision_reason and last_revised (2026-11-16) updated.

## Verification
perfect_agent.py: ok (empty required work-up, submits directly). test_case_guards.py -k PD-S01..S06: 48 passed. case_io.py check: schema and synonym guard OK; the only failure naming PD is test_panel_case_contract for PD-RM05 (not this case).
Pass 1: 0 errors found
- Note 5dcbd891 (FIXED, D1, D2) checked and correct: CT optional with the D1 S06 label and rationale, stop rule empty, CT->DaTscan constraint deleted, KCE[4] 'if obtained', panel_required_exemptions.analyze_brain_mri kept; D8 handedness change consistent with the exam (left-sided signs, micrographia) and the left-handed scissors; DaTscan laterality (right putamen, left-sided signs) consistent.
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
