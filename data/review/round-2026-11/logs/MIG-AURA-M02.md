# MIG-AURA-M02

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM) | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 01f7876b-7c94-4cb2-83f6-f628f4ca56e0 | FIXED (class LIT, commit 393c547e) | Nothing left to remove: no search_medical_literature criterion, follow-up or stored output; fallback_tool_outputs.literature_search is null. No other change. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| - | - | - | Whole case read field by field: no class finding of the plan applies (no TIA prohibition, no antithrombotic, no topiramate must) and no PATTERNS error found. Timeline (travel 8 weeks ago, first attack 6 weeks ago), laterality (left visual field and left hand/cheek, right-sided headache), 6 of 6 C characteristics and the optional MRI tier are consistent. | none |

## Changes
No change to the case content in this round beyond the literature-search step removed by the class change (commit 393c547e), which the reviewer's note asked for. The physician will see the same history, examination, pathway and assessment as before.

## Verification
perfect_agent.py -v: ok (every required and recommended criterion served by its own report). test_case_guards.py -k <case>: pass. case_io.py check: schema OK, synonym guard OK, no failure names this case (one unrelated failure names MIG-AURA-P05). DiagnosisCriterion.matches re-checked on a plain correct answer after any label edit: True; TIA / mimic answers: False.
Pass 1: 0 errors found
- Rulings, case and checks verified: no literature step left, no class finding applies (no TIA prohibition, antithrombotic or topiramate text), laterality and timeline consistent.
Cosmetic (not counted): none.
Pass 2: 0 errors found
- Checked: only the LIT class touched the case; laterality (left field and left hand/cheek, right headache), timeline (Nigeria 8 weeks ago, first attack 6 weeks ago) and 6 of 6 C count consistent. Every note id has a ruling; no literature string left (fallback literature_search null); no new em dash; no answer leakage in the patient block or drug-check outputs.
Cosmetic (not counted): none.
Re-run at pass 2: perfect_agent.py -v ok (each required and recommended criterion receives the report carrying its expected evidence); test_case_guards -k for MIG-AURA-M01..M06: 48 passed; case_io.py check: schema OK, synonym guard OK, no failure names this case; mri_probe: no gadolinium text, no MRI pair needed; DiagnosisCriterion.matches: correct answer True, TIA / mimic False.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.
Pass 5: 0 errors found
- Checked the only change after the last clean pass: metadata.case_body_concerns deletion (condition audit) checked against git diff 06b74446: only the generation-pipeline line was removed, the field is [] and no other field changed with it.
- perfect_agent.py -v ok; test_case_guards -k (M01..M08) 64 passed.
Cosmetic (not counted): none.
