# MIG-AURA-S10

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional). Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 5b8ab438-ba51-42b5-a481-e7d8832beeb0 | FIXED | ground_truth.assessment.required_recommendations[2] now reads: "If topiramate is chosen, start it only under the topiramate pregnancy prevention programme with a contraceptive method unaffected by enzyme induction: a copper IUD, a levonorgestrel IUS, or medroxyprogesterone acetate injection used with condoms. Topiramate is treated as a potential enzyme inducer at any dose, so pills and the etonogestrel implant are not adequate. Her partner's vasectomy counts only if he is her sole partner and azoospermia was confirmed after the procedure; otherwise use one of the methods above." followup_outputs[0].output.warnings[0]: "reduces the efficacy of oral contraceptive pills at higher doses" became "at doses of 200 mg/day or more; FSRH advises treating it as a potential enzyme inducer at any dose" (FSRH CEU 2022; plan D3). |
| 335b1fbd-c03e-4922-8f69-b50beb248540 | ALREADY-FIXED | No change. action-2-check-drug-interactions is recommended; the scorer counts only actions that match no criterion against max_additional_actions (policy_reward.py 138-146: `extra = sum(not positive[index] ...)`, where positive means the action matched a criterion), so one drug check after the clinical assessment is credited and stopping stays 1.0 (plan D7). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | none | ground_truth.diagnosis.accepted[0] | "preventive therapy indicated" kept: 2-4 severe attacks a month with MIDAS grade IV meet the AHS 2021 offer threshold (plan D8) | no change |
| C | minor | ground_truth.avoided_actions (cardiac-monitoring and EEG waste entries) | The citation is [ICHD_3], which does not address Holter or EEG use in migraine with aura (the rationales are correct). The same template is in other MIG-AURA cases, so it is a condition-level citation question for the lead | FLAGGED |
| B | minor | fallback_tool_outputs.eeg | The impression says "awake and drowsy EEG" but background.sleep_features reports sleep spindles (stage N2). Shared fallback template; served only for an EEG the case lists as waste | FIXED (verification pass 1: impression now "Normal awake, drowsy and light sleep EEG") |
| E | minor | metadata.case_body_concerns | Authoring-process text ("Useless-tool entries dropped ...") in metadata, which physicians see. Present in every MIG-AURA case; left for the lead to decide centrally | FLAGGED |

## Changes
Not approved before this round (R1 in progress). The literature search criterion was removed by the class LIT change. Following the reviewer, the topiramate must (required_recommendations[2]) no longer offers the etonogestrel implant: topiramate is started only under the pregnancy prevention programme with a copper IUD, a levonorgestrel IUS or medroxyprogesterone acetate injection with condoms, and her partner's vasectomy counts only if he is her sole partner and azoospermia was confirmed after the procedure. The drug-check report now says that the pill interaction evidence is for 200 mg/day or more and that FSRH advises treating topiramate as a potential enzyme inducer at any dose. The stop-rule note needed no change: the drug check is a recommended step and is credited, never counted as an extra action.

## Verification
Pass 1: 0 errors found
- Every note id has a ruling and each was checked against the case, the plan (D1, D2, D3, D4, D7, D8) and the scorer (policy_reward.py 138-146 for the stop-rule note where present). No literature string left. perfect_agent.py -v passes and test_case_guards passes for this id.
Cosmetic (not counted): fallback_tool_outputs.eeg.impression said "Normal awake and drowsy EEG" while background.sleep_features reports vertex waves and sleep spindles (stage N2); impression now "Normal awake, drowsy and light sleep EEG. No epileptiform discharges and no focal slowing." (the worker's FLAGGED own finding, now FIXED).

Pass 2: 0 errors found
- Note 5b8ab438 FIXED: REQ2 is the D3 canonical must plus the vasectomy condition the note asks for, and FU0 warnings[0] carries the FSRH any-dose caution. Note 335b1fbd ALREADY-FIXED: verified in policy_reward.py 138-146 that only actions matching no criterion count as extra (positive[] is set by criterion_matches over all tiers), so the recommended drug check after the assessment keeps stopping at 1.0. Label 'preventive therapy indicated' kept per D8 (AHS offer threshold; MIDAS 24 is grade IV).
- Checks re-run on 17 Nov 2026: perfect_agent.py -v passes (every criterion answered by the case's own data, none by the case fallback or the library); case_io.py check: schema and synonym guard OK, no test failure names this case; test_case_guards -k for S06-S11 passes (599 passed). No literature string left; no em dash or non-ASCII character in text added this round.
Cosmetic (not counted): none.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.

Pass 5: 0 errors found
- Verified the only change made after the last 0-error pass (Pass 2): the condition-audit deletion of the generation-pipeline line in metadata.case_body_concerns. git diff confirms the field is now an empty list, no other metadata key changed, no "Useless-tool" string remains in the case, and no clinical field depends on the deleted text. Correct per ROUND_POLICY 'How to edit' and the November addendum (no process text in metadata). No ruling changes.
- Checks re-run on 17 Nov 2026: perfect_agent.py -v passes; test_case_guards -k for S08-S11 passes (32 passed).
Cosmetic (not counted): perfect_agent.py -v labels the clinical-assessment source "?" (its _source helper compares against an exclude_none dump of initial_tool_outputs); the check passes, so this is a helper display quirk, not a case defect.
