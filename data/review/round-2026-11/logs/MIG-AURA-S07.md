# MIG-AURA-S07

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| b32b7c1a-ea21-4c2f-b112-22029a55fe83 | FIXED (class LIT, commit 393c547e) | Nothing left to change: no search_medical_literature criterion, follow-up or stored output remains in the case (checked); a literature query gets the neutral library text. |
| 801e6db7-677f-4f1c-959f-fb43b9ad6faf | FIXED | ground_truth.assessment.required_recommendations[3] now reads: "If topiramate is chosen, start it only under the topiramate pregnancy prevention programme with a contraceptive method unaffected by enzyme induction: a copper IUD, a levonorgestrel IUS, or medroxyprogesterone acetate injection used with condoms. Topiramate is treated as a potential enzyme inducer at any dose, so pills and the etonogestrel implant are not adequate." (FSRH CEU 2022; MHRA DSU 2024; plan D3). REQ0's switch list (POP, implant, LNG-IUS, copper IUD after stopping Yasmin) concerns the aura, not topiramate, and stays (plan D3). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | none | followup_outputs[0].output | Checked for class TOPI-CONTRA: the drug report concerns Yasmin and the triptans and gives no topiramate contraception statement; nothing to correct | no change |
| C | minor | ground_truth.avoided_actions (cardiac-monitoring and EEG waste entries) | The citation is [ICHD_3], which does not address Holter or EEG use in migraine with aura (the rationales are correct). The same template is in other MIG-AURA cases, so it is a condition-level citation question for the lead | FLAGGED |
| B | minor | fallback_tool_outputs.eeg | The impression says "awake and drowsy EEG" but background.sleep_features reports sleep spindles (stage N2). Shared fallback template; served only for an EEG the case lists as waste | FIXED (verification pass 1: impression now "Normal awake, drowsy and light sleep EEG") |
| E | minor | metadata.case_body_concerns | Authoring-process text ("Useless-tool entries dropped ...") in metadata, which physicians see. Present in every MIG-AURA case; left for the lead to decide centrally | FLAGGED |

## Changes
Not approved before this round (R1 in progress). The literature search step was removed by the class LIT change. Following the reviewer, the topiramate must (required_recommendations[3]) no longer offers the etonogestrel implant: if topiramate is chosen, it is started only under the pregnancy prevention programme with a copper IUD, a levonorgestrel IUS or medroxyprogesterone acetate injection with condoms, because FSRH treats topiramate as a potential enzyme inducer at any dose. The advice to stop Yasmin and switch to a progestogen-only method or an IUD (for the aura) is unchanged. Nothing else changed.

## Verification
Pass 1: 0 errors found
- Every note id has a ruling and each was checked against the case, the plan (D1, D2, D3, D4, D7, D8) and the scorer (policy_reward.py 138-146 for the stop-rule note where present). No literature string left. perfect_agent.py -v passes and test_case_guards passes for this id.
Cosmetic (not counted): fallback_tool_outputs.eeg.impression said "Normal awake and drowsy EEG" while background.sleep_features reports vertex waves and sleep spindles (stage N2); impression now "Normal awake, drowsy and light sleep EEG. No epileptiform discharges and no focal slowing." (the worker's FLAGGED own finding, now FIXED).

Pass 2: 0 errors found
- Notes b32b7c1a (FIXED, class LIT; none left) and 801e6db7 (FIXED: REQ3 is the D3 canonical must word for word; REQ0's implant option concerns the aura and stays per D3) confirmed against the annotation file and plan. Whole case reread: right-field aura with left-sided headache, 3-5 acute-medication days, the AHS 2021 thresholds, the triptan prohibition and the drug report agree; no leakage.
- Checks re-run on 17 Nov 2026: perfect_agent.py -v passes (every criterion answered by the case's own data, none by the case fallback or the library); case_io.py check: schema and synonym guard OK, no test failure names this case; test_case_guards -k for S06-S11 passes (599 passed). No literature string left; no em dash or non-ASCII character in text added this round.
Cosmetic (not counted): none.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.
Pass 5: 0 errors found
- Scope: the only change after the last clean pass is the condition-audit class fix (metadata.case_body_concerns). Checked in the diff: the generation-pipeline line was the only entry, the field is now [], no other field changed after pass 4, and no 'Useless-tool' text remains anywhere in the case.
- Checks: perfect_agent.py MIG-AURA-S07 -v passes; test_case_guards -k (8 cases) 64 passed.
Cosmetic (not counted): none.
Pass 6: 0 errors found
- Scope: pass 5 was clean and nothing was written to the case after it (git diff of the case shows only the earlier round changes, the case file is older than the pass-5 log entry); nothing to re-verify.
- Checks: perfect_agent.py MIG-AURA-S07 -v passes; test_case_guards -k (8 cases) 64 passed.
Cosmetic (not counted): none.
