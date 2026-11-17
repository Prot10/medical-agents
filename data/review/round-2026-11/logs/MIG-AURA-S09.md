# MIG-AURA-S09

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 70750e29-6230-46c1-af71-afbe4c5ef7e9 | FIXED (class LIT, commit 393c547e) | Nothing left to change: no search_medical_literature criterion, follow-up or stored output remains in the case (checked); a literature query gets the neutral library text. |
| 96e9ad91-eced-40c3-9af2-6362f76dbdff | NO-ACTION | Approval of patient.chief_complaint; unchanged. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.assessment.prohibited_recommendations[0] | Class TIA-CERT (plan D4, from note b37e0b4d and others): the prohibition rested partly on "the MRI at the time showed no infarct", which implies that a normal MRI argues against TIA. Reworded so it rests on the clinical features of the episode (positive visual disturbance spreading over 20 minutes and followed by headache, identical to her usual attacks) and states that a normal MRI excludes infarction, not TIA | FIXED |
| C | minor | ground_truth.differential[2].key_features | Same class: "MRI at the time reported normal" was listed among the features against TIA with no limit; added "(this excludes an infarct, not a TIA; the clinical features decide)" | FIXED |
| C | none | ground_truth.assessment.required_recommendations[1], followup_outputs[0].output.interactions[2] | Checked for class TOPI-CONTRA: topiramate is paired with her levonorgestrel IUS, which FSRH accepts with an enzyme inducer; no implant or dose-threshold claim | no change |
| C | minor | ground_truth.avoided_actions (cardiac-monitoring and EEG waste entries) | The citation is [ICHD_3], which does not address Holter or EEG use in migraine with aura (the rationales are correct). The same template is in other MIG-AURA cases, so it is a condition-level citation question for the lead | FLAGGED |
| B | minor | fallback_tool_outputs.eeg | The impression says "awake and drowsy EEG" but background.sleep_features reports sleep spindles (stage N2). Shared fallback template; served only for an EEG the case lists as waste | FIXED (verification pass 1: impression now "Normal awake, drowsy and light sleep EEG") |
| E | minor | metadata.case_body_concerns | Authoring-process text ("Useless-tool entries dropped ...") in metadata, which physicians see. Present in every MIG-AURA case; left for the lead to decide centrally | FLAGGED |

## Changes
Not approved before this round (R1 in progress). The literature search step was removed by the class LIT change, and the reviewer approved the chief complaint. Applying the condition-wide TIA ruling, the prohibition of antithrombotic therapy (prohibited_recommendations[0]) now rests on the clinical features of the episode once queried as TIA (a positive visual disturbance spreading over 20 minutes and followed by headache, the same as her usual attacks) and says that a normal MRI excludes infarction, not TIA. The TIA entry of the differential says the same about the old normal MRI. Diagnosis, work-up, preventive plan and other musts are unchanged.

## Verification
Pass 1: 0 errors found
- Every note id has a ruling and each was checked against the case, the plan (D1, D2, D3, D4, D7, D8) and the scorer (policy_reward.py 138-146 for the stop-rule note where present). No literature string left. perfect_agent.py -v passes and test_case_guards passes for this id.
Cosmetic (not counted): fallback_tool_outputs.eeg.impression said "Normal awake and drowsy EEG" while background.sleep_features reports vertex waves and sleep spindles (stage N2); impression now "Normal awake, drowsy and light sleep EEG. No epileptiform discharges and no focal slowing." (the worker's FLAGGED own finding, now FIXED).

Pass 2: 0 errors found
- Notes 70750e29 (FIXED, class LIT; none left) and 96e9ad91 (NO-ACTION, approval) confirmed. Class TIA-CERT: PRO0 follows the D4 established-case wording and its features match the HPI (left-field episode 4 years ago, 20 minutes, followed by headache) and the clinical assessment; differential[2] states the DWI limit. The topiramate plan relies on her LNG-IUS, which FSRH accepts with an enzyme inducer; the drug report gives no 200 mg threshold or implant claim.
- Checks re-run on 17 Nov 2026: perfect_agent.py -v passes (every criterion answered by the case's own data, none by the case fallback or the library); case_io.py check: schema and synonym guard OK, no test failure names this case; test_case_guards -k for S06-S11 passes (599 passed). No literature string left; no em dash or non-ASCII character in text added this round.
Cosmetic (not counted): none.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.

Pass 5: 0 errors found
- Verified the only change made after the last 0-error pass (Pass 2): the condition-audit deletion of the generation-pipeline line in metadata.case_body_concerns. git diff confirms the field is now an empty list, no other metadata key changed, no "Useless-tool" string remains in the case, and no clinical field depends on the deleted text. Correct per ROUND_POLICY 'How to edit' and the November addendum (no process text in metadata). No ruling changes.
- Checks re-run on 17 Nov 2026: perfect_agent.py -v passes; test_case_guards -k for S08-S11 passes (32 passed).
Cosmetic (not counted): perfect_agent.py -v labels the clinical-assessment source "?" (its _source helper compares against an exclude_none dump of initial_tool_outputs); the check passes, so this is a helper display quirk, not a case defect.
