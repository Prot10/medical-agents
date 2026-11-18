# MIG-AURA-M07

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| a6bcf14f-b136-46f7-b13d-7466e8af31cc | FIXED (class LIT, commit 393c547e) | Literature criterion and follow-up removed by the class; re-checked: no `search_medical_literature` string left in the case. |
| fee18a5b-9547-4fbf-8991-a98e7856b8d7 | ALREADY-FIXED (plan D7) | `ground_truth.stop_rule` unchanged. MRI (`action-4-analyze-brain-mri`) and MRA (`action-mra`) are recommended criteria; `policy_reward.py` counts as "extra" only actions that match no criterion, so assessment + MRI + MRA is not penalised. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| E | minor | metadata.case_body_concerns | Authoring-process text ("Useless-tool entries dropped ... per authoring guide") sits in metadata, which physicians see; the same generated line exists across the condition, so it is left for a central sweep. | FLAGGED |
| - | - | whole case | Read in full (patient, outputs, criteria, musts, prohibitions, differential, red herrings, metadata); no other PATTERNS error found: single attack correctly 1.5.2, exertional red flags justify MRI and MRA (ICHD-3 4.2 comment), CT in A&E already done so repeat CT as waste is consistent. | - |

## Changes
No change to the case file this round beyond the class LIT removal of the literature step (commit 393c547e). The stop-rule note is already satisfied: brain MRI and head and neck MRA are recommended criteria, and the scorer credits them and never counts them as extra actions, so completing both before reassurance and return-to-running advice is not penalised.

## Verification
perfect_agent.py MIG-AURA-M07 -v: ok. test_case_guards (-k my six ids): 48 passed. case_io.py check: schema OK, synonym guard OK, no failure names this case (the only condition failure is test_no_review_process_text[MIG-AURA-P05], another worker's case).
Pass 1: 0 errors found
- Checked: both notes ruled; no literature string left; MRI and MRA are recommended criteria and the scorer never counts them as extra (policy_reward.py stopping block), so the ALREADY-FIXED ruling of fee18a5b holds. perfect_agent -v ok; test_case_guards -k (six ids) 48 passed; case_io check: no failure names this case.
Pass 2: 0 errors found
- Checked: both notes ruled; ALREADY-FIXED for fee18a5b verified against policy_reward.py (stopping counts only actions matching no criterion; MRI and MRA are recommended); no literature string left; case read in full, no contradiction found.
- Re-checked by pass 2: perfect_agent.py -v ok; test_case_guards -k (six ids) 48 passed; case_io check: schema OK, synonym guard OK, no test failure names this case.
Pass 3: 0 errors found
- Checked: every note ruled and the ruling holds; diff read and final case read in full; no contradiction, leakage, template carry-over or em dash in new text found; no literature string left.
- Re-checked by pass 3: perfect_agent.py -v ok; test_case_guards -k (six ids) 48 passed. ALREADY-FIXED for fee18a5b verified in policy_reward.py (stopping counts only actions matching no criterion).
Pass 4: 0 errors found
- Checked: both notes ruled and the rulings hold (ALREADY-FIXED for fee18a5b re-verified in policy_reward.py: stopping counts only actions matching no criterion, and MRI and MRA are recommended); diff is the LIT removal only; final case read in full; no contradiction, leakage or literature string.
- Re-run by pass 4: perfect_agent.py -v ok; test_case_guards -k (six ids) 48 passed; case_io check: schema OK, synonym guard OK, no test failure names this case.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.
Pass 5: 0 errors found
- Checked the only change after the last clean pass: metadata.case_body_concerns deletion (condition audit) checked against git diff 06b74446: only the generation-pipeline line was removed, the field is [] and no other field changed with it.
- perfect_agent.py -v ok; test_case_guards -k (M01..M08) 64 passed.
Cosmetic (not counted): none.
