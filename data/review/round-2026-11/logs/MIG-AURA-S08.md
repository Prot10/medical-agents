# MIG-AURA-S08

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| a36f4096-376b-4a7d-8c7c-34f7480618ff | FIXED (class LIT, commit 393c547e) | Nothing left to change: no search_medical_literature criterion, follow-up or stored output remains in the case (checked); a literature query gets the neutral library text. |
| 69bca92e-1c6d-4657-be1d-a5e537ac3631 | NO-ACTION | Approval of patient.chief_complaint; unchanged. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | none | ground_truth.assessment.required_recommendations[1] | Sumatriptan dosing, timing after the aura and second dose after 2 hours checked against the SmPC; correct | no change |
| C | minor | ground_truth.avoided_actions (echo and cardiac-monitoring waste entries) | The citation is [ICHD_3], which does not address PFO screening or Holter use; the rationale itself names MIST, PRIMA and PREMIUM. The same template is in other MIG-AURA cases, so it is a condition-level citation question for the lead | FLAGGED |
| E | minor | metadata.case_body_concerns | Authoring-process text ("Useless-tool entries dropped ...") in metadata, which physicians see. Present in every MIG-AURA case; left for the lead to decide centrally | FLAGGED |

## Changes
Not approved before this round (R1 in progress). The literature search step was removed by the class LIT change, and the reviewer approved the chief complaint. I read every field again and found no error: the case content is unchanged this round apart from the literature removal.

## Verification
Pass 1: 0 errors found
- Both notes have a ruling and the rulings are right (a36f4096 FIXED by class LIT, no literature string left; 69bca92e NO-ACTION, approval). Whole case reread: no class finding, no contradiction, no leakage. perfect_agent.py -v and test_case_guards pass.
Cosmetic (not counted): none.

Pass 2: 0 errors found
- Notes a36f4096 (FIXED, class LIT; none left) and 69bca92e (NO-ACTION, approval) confirmed. Whole case reread: no class finding (no topiramate, no TIA text), sumatriptan plan and the optional drug check are consistent; no leakage.
- Checks re-run on 17 Nov 2026: perfect_agent.py -v passes (every criterion answered by the case's own data, none by the case fallback or the library); case_io.py check: schema and synonym guard OK, no test failure names this case; test_case_guards -k for S06-S11 passes (599 passed). No literature string left; no em dash or non-ASCII character in text added this round.
Cosmetic (not counted): none.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.

Pass 5: 0 errors found
- Verified the only change made after the last 0-error pass (Pass 2): the condition-audit deletion of the generation-pipeline line in metadata.case_body_concerns. git diff confirms the field is now an empty list, no other metadata key changed, no "Useless-tool" string remains in the case, and no clinical field depends on the deleted text. Correct per ROUND_POLICY 'How to edit' and the November addendum (no process text in metadata). No ruling changes.
- Checks re-run on 17 Nov 2026: perfect_agent.py -v passes; test_case_guards -k for S08-S11 passes (32 passed).
Cosmetic (not counted): perfect_agent.py -v labels the clinical-assessment source "?" (its _source helper compares against an exclude_none dump of initial_tool_outputs); the check passes, so this is a helper display quirk, not a case defect.
