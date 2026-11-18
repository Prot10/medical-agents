# MIG-AURA-S02

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional). Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R1 in_progress | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 9328b8dc-2d6c-43b9-a876-ddcb28a9b70f | NO-ACTION (D2) | Approval of `patient.chief_complaint`; unchanged |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | ground_truth.action_criteria[0].rationale | Cited 'AAN 2000' for who needs imaging; Silberstein 2000 covers acute and preventive treatment, not neuroimaging (superseded in the pack, October decision on [AAN_2000]) | FIXED: replaced by the AHS neuroimaging evidence assessment (Evans RW et al., Headache 2020;60:318-336) |
| C | minor | ground_truth.diagnosis.accepted[0] | 'menstrually-related' is asserted while the case has no prospective diary (ICHD-3 appendix A1.2.0.2 needs attacks on day 1 plus or minus 2 in at least 2 of 3 documented cycles; the must itself asks for a diary to confirm). No reviewer ruled the label wrong, so accepted[0] is not changed | FLAGGED for re-review |
| C | minor | (class LIT check) | No search_medical_literature criterion or stored output left | confirmed, nothing added |
| C | minor | ground_truth.assessment.required_recommendations[2] | The diary must said 'at least 2-3 cycles'; ICHD-3 appendix A1.2.0 requires attacks on day 1 plus or minus 2 in at least 2 of 3 menstrual cycles, so a 2-cycle diary cannot confirm the pattern | FIXED (verification pass 3): 'for at least 3 cycles ... in at least 2 of 3 cycles, ICHD-3 appendix A1.2.0' |

## Changes
The physician's note approves the chief complaint and asks for nothing; the clinical content is unchanged. One citation was corrected: the rationale of the structured-history criterion cited the AAN 2000 practice parameter for the imaging decision, which that guideline does not cover; it now cites the AHS neuroimaging evidence assessment (Evans 2020) only. The literature step had already been removed (class LIT). Flagged for re-review, not changed: the label calls the migraine 'menstrually-related' before the diary the case asks for has confirmed the pattern.
Verification pass 3: the diary must now asks for at least three cycles, since the ICHD-3 menstrual criterion counts attacks in at least two of three cycles.

## Verification
Pass 1: 0 errors found
- Note ruling checked: NO-ACTION is right (the note approves the chief complaint and asks for nothing; plan D2).
- The only edit since the base besides class LIT is the imaging-citation correction in action_criteria[0].rationale (AAN 2000 to the AHS neuroimaging evidence assessment, Evans 2020), which matches the criteria pack section 8 and the October [AAN_2000] decision; no other AAN 2000 citation left. No literature criterion or output left. The 'menstrually-related' label flag is correctly left for re-review (no reviewer ruled the label; accepted[0] is not changed).
- Checks: perfect_agent.py MIG-AURA-S02 -v passes; test_case_guards -k MIG-AURA-S02 passes; case_io check names no failure for this case.
Cosmetic (not counted): none.
Pass 2: 0 errors found
- Note ruling NO-ACTION confirmed (approval of the chief complaint, plan D2). The only non-LIT edit is the imaging citation in action_criteria[0].rationale (AAN 2000 to Evans 2020, per criteria pack section 8); correct. Re-checked the musts and prohibitions (UKMEC 4 for combined hormonal contraception, triptan timing and doses, AHS 2021 prevention thresholds, medication-overuse limits), allergies and medications against the musts, the drug-check output against its expected evidence (no leakage), and the class scanner (no topiramate-implant, TIA, literature or over-certainty text).
- Checks: perfect_agent.py -v passes; test_case_guards -k passes.
Cosmetic (not counted): none.
Pass 3: 1 errors found
- ground_truth.assessment.required_recommendations[2] asked for a headache and menstrual diary 'for at least 2-3 cycles'; ICHD-3 appendix A1.2.0 (A1.2.0.1/A1.2.0.2) needs attacks on day 1 plus or minus 2 in at least 2 of 3 cycles, so two cycles cannot confirm the menstrual relation the label asserts. Changed through case_io to 'for at least 3 cycles to confirm the menstrual relation (attacks from 2 days before to 3 days after the onset of menses in at least 2 of 3 cycles, ICHD-3 appendix A1.2.0)'. No other case of the 600 has the "2-3 cycles" wording (searched).
- Checked and correct: note ruling NO-ACTION (approval of the chief complaint, D2); the Evans 2020 citation edit; criterion C 5 of 6; perimenstrual prophylaxis doses (frovatriptan 2.5 mg twice daily, zolmitriptan 2.5 mg two or three times daily, NICE CG150); UKMEC 4 must and prohibition; drug-check output against expected evidence (no leakage); BMI 24.1 and BP 112/70 consistent; no literature left.
- Checks: perfect_agent.py MIG-AURA-S02 -v passes (the criterion receives the clinical assessment); test_case_guards -k passes; case_io check names no failure for this case.
Cosmetic (not counted): none.
Pass 4: 0 errors found
- Note ruling NO-ACTION confirmed (approval of the chief complaint, plan D2). Read the case in full; the only non-LIT edits since 06b74446 (AAN 2000 to Evans 2020 in action_criteria[0].rationale, and in S02 the 3-cycle diary per ICHD-3 appendix A1.2.0) are correct. Checked criterion C counts, BMI, BP, onset ages and timeline, AHS 2021 prevention thresholds, triptan/NSAID/antiemetic doses, medication-overuse limits, UKMEC 4 must and prohibition, allergies and medications against the musts, avoided actions against criteria, differential against findings, drug-check output against expected evidence (no leakage), no literature left.
- Checks: perfect_agent.py -v passes (the criterion receives the clinical assessment); test_case_guards -k passes.
Cosmetic (not counted): none.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.
Pass 5: 0 errors found
- Scope: the only change after the last clean pass is the condition-audit class fix (metadata.case_body_concerns). Checked in the diff: the generation-pipeline line was the only entry, the field is now [], no other field changed after pass 4, and no 'Useless-tool' text remains anywhere in the case.
- Checks: perfect_agent.py MIG-AURA-S02 -v passes; test_case_guards -k (8 cases) 64 passed.
Cosmetic (not counted): none.
Pass 6: 0 errors found
- Scope: pass 5 was clean and nothing was written to the case after it (git diff of the case shows only the earlier round changes, the case file is older than the pass-5 log entry); nothing to re-verify.
- Checks: perfect_agent.py MIG-AURA-S02 -v passes; test_case_guards -k (8 cases) 64 passed.
Cosmetic (not counted): none.
