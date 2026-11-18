# SYNC-CARD-P01

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-8-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R2 needs_changes | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| c90f3000-61f8-484a-831a-1daac428a1f6 | FIXED | `ground_truth.assessment.required_recommendations[8]`: DR-ICD2 text (Group 1 after 3 months, EHRA 2009 consensus; Group 2 permanently restricted; national licensing rules) (C5, D8). |
| NB-87M:SYNC-CARD-P01:policy_verdict | FIXED, except invasive-angiography-after-CTA label DECLINED | New `avoided_actions` `avoid-waste-bubble-study`, `avoid-waste-polysomnography`, `avoid-waste-electrophysiology-study` (ESC 2018; ESC 2022 IIb for PES after an established secondary-prevention ICD indication). Exercise echo: added as alternative 2 (`order_echocardiogram {echo_type: exercise_echo}`) of `ground_truth.action_criteria[7]` (`action-6-order-specialized-test`), rather than waste (D4). Invasive angiography after CTA: no label, because an avoided action cannot be conditional and would penalise invasive angiography as the first and only coronary test, which `action_criteria[6]` accepts (D5). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | `ground_truth.avoided_actions` (new `avoid-waste-tee`) | Class C3: the fallback TEE answered an order with no label | FIXED (waste, canonical rationale) |
| A | minor | `followup_outputs` order | Exercise echo and genetic panel (pathway studies) sat after the off-pathway EPS | FIXED (TTE, telemetry, CMR, coronary CTA, invasive angiography, exercise test, exercise echo, gene panel, drug checks, then EPS, bubble study, polysomnography) |
| E | minor | `metadata.revision_reason`, `metadata.last_revised` | Updated | FIXED |

## Changes
The driving must now gives the correct source: Group 1 driving may resume 3 months after a secondary-prevention ICD (EHRA 2009 consensus), Group 2 driving is permanently restricted, and national licensing rules apply; ESC 2018 is no longer cited for it. An exercise echocardiogram is now accepted as the monitored exercise test (same criterion, still after the transthoracic echo by the existing hard constraint), so ordering both exercise studies scores the second as an unjustified extra test. Bubble study, polysomnography, electrophysiology study (PES after an established secondary-prevention ICD indication is only Class IIb, ESC 2022) and TEE are labelled waste. Invasive angiography after a coronary CTA is not labelled, because a label cannot depend on order and would penalise invasive angiography chosen as the only coronary test; the second coronary study is already scored as unjustified. Follow-ups were reordered so the pathway studies come before the off-pathway ones.

CENTRAL: C2 key `[EHRA_2009_ICD_Driving]` (Vijgen 2009, Europace 2009;11:1097-1107) for the driving must; C3 pack text sec.5 driving (D8).

## Verification
Pass 1: 0 errors found
- Checked DR-ICD2 driving text, the waste labels (EPS with ESC 2022 IIb, bubble study, polysomnography with OSA in the history, TEE), the exercise echo as an alternative of action-6 under the existing hard TTE-first constraint (the order gets the stored exercise echo), and the declined invasive-angiography label (D5); perfect_agent -v and test_case_guards pass.
Pass 2: 0 errors found
- Focused verifier: no change was made after Pass 1 (0 errors), so nothing was left unverified. Re-ran perfect_agent -v and test_case_guards: both pass.
- Condition auditor, 17 Nov 2026, blind leak pass: a check_drug_interactions output (served to any drug query, including a first call before any test) quoted the ECG result: sertraline follow-up "QTc 448 ms on the current ECG" (expected evidence of action-1-analyze-ecg). Now "check the QTc on the current ECG". perfect_agent, test_case_guards -k, case_io check clean.
Pass 4: 0 errors found
- Verified the condition-audit leak fix (followup check_sertraline warning now 'check the QTc on the current ECG'; no ECG value left in any drug output, initial/fallback/followups re-read; the 448 ms value stays only in the ECG output, criterion-0 evidence and differential key features). Drug criterion evidence (CYP2D6, conditional QT risk) still carried. perfect_agent.py -v passes; test_case_guards.py -k (64 tests for the 8 SYNC-CARD pass-4 cases) passes. Nothing changed.
