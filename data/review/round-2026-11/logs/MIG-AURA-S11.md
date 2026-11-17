# MIG-AURA-S11

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 4929a69f-7e15-4005-ae76-1f0a6c4b4bb9 | FIXED (class LIT, commit 393c547e) | Nothing left to change: no search_medical_literature criterion, follow-up or stored output remains in the case (checked); a literature query gets the neutral library text. |
| f6ee93eb-f51b-45c2-8103-5e7a28d038d0 | NO-ACTION | Approval of patient.chief_complaint; unchanged. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | none | ground_truth.assessment, followup_outputs[0].output | Propranolol-rizatriptan 5 mg adjustment, ICHD-3 8.2 15-day threshold and the 10-day opioid/triptan overuse rule checked; correct. He is male, so class TOPI-CONTRA does not apply | no change |
| C | minor | ground_truth.avoided_actions (echo and cardiac-monitoring waste entries) | The citation is [ICHD_3], which does not address PFO screening or Holter use; the rationale itself names MIST, PRIMA and PREMIUM. The same template is in other MIG-AURA cases, so it is a condition-level citation question for the lead | FLAGGED |
| B | minor | fallback_tool_outputs.eeg | The impression says "awake and drowsy EEG" but background.sleep_features reports sleep spindles (stage N2). Shared fallback template; served only for an EEG the case lists as waste | FIXED (verification pass 1: impression now "Normal awake, drowsy and light sleep EEG") |
| E | minor | metadata.case_body_concerns | Authoring-process text ("Useless-tool entries dropped ...") in metadata, which physicians see. Present in every MIG-AURA case; left for the lead to decide centrally | FLAGGED |

## Changes
Not approved before this round (R1 in progress). The literature search step was removed by the class LIT change, and the reviewer approved the chief complaint. I read every field again and found no error: the case content is unchanged this round apart from the literature removal.

## Verification
Pass 1: 0 errors found
- Every note id has a ruling and each was checked against the case, the plan (D1, D2, D3, D4, D7, D8) and the scorer (policy_reward.py 138-146 for the stop-rule note where present). No literature string left. perfect_agent.py -v passes and test_case_guards passes for this id.
Cosmetic (not counted): fallback_tool_outputs.eeg.impression said "Normal awake and drowsy EEG" while background.sleep_features reports vertex waves and sleep spindles (stage N2); impression now "Normal awake, drowsy and light sleep EEG. No epileptiform discharges and no focal slowing." (the worker's FLAGGED own finding, now FIXED).

Pass 2: 0 errors found
- Notes 4929a69f (FIXED, class LIT; none left) and f6ee93eb (NO-ACTION, approval) confirmed. Whole case reread: acute-medication days (rizatriptan up to 4 plus co-codamol 6-8 = 10-12) and headache days (10-12, below the ICHD-3 8.2 threshold of 15) agree across the HPI, assessment, differential and musts; the propranolol-rizatriptan 5 mg rule agrees between the drug report, the must and the prohibition. Male patient: TOPI-CONTRA does not apply.
- Checks re-run on 17 Nov 2026: perfect_agent.py -v passes (every criterion answered by the case's own data, none by the case fallback or the library); case_io.py check: schema and synonym guard OK, no test failure names this case; test_case_guards -k for S06-S11 passes (599 passed). No literature string left; no em dash or non-ASCII character in text added this round.
Cosmetic (not counted): none.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.

Pass 5: 0 errors found
- Verified the only change made after the last 0-error pass (Pass 2): the condition-audit deletion of the generation-pipeline line in metadata.case_body_concerns. git diff confirms the field is now an empty list, no other metadata key changed, no "Useless-tool" string remains in the case, and no clinical field depends on the deleted text. Correct per ROUND_POLICY 'How to edit' and the November addendum (no process text in metadata). No ruling changes.
- Checks re-run on 17 Nov 2026: perfect_agent.py -v passes; test_case_guards -k for S08-S11 passes (32 passed).
Cosmetic (not counted): perfect_agent.py -v labels the clinical-assessment source "?" (its _source helper compares against an exclude_none dump of initial_tool_outputs); the check passes, so this is a helper display quirk, not a case defect.
