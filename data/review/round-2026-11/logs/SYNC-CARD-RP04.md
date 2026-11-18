# SYNC-CARD-RP04

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-7-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed, field paths |
| --- | --- | --- |
| 014edfe5-ce37-4362-820a-6b3f3de13a03 | FIXED | R0, key_clinical_evidence[0], differential[0].key_features and red_herrings[0].correct_interpretation now say that normal routine and ambulatory EEGs do not exclude epilepsy and that the loop recorder (complete AV block with asystole in three typical witnessed episodes) is the decisive evidence; antiseizure-drug failure is no longer presented as evidence against epilepsy (action_criteria[2] rationale and expected_evidence reworded: the levels document exposure before withdrawal). (ground_truth.assessment.required_recommendations[0]) |
| NB-87M:SYNC-CARD-RP04:policy_verdict | FIXED | Avoided actions (comment-less needs_revision): the served electrophysiology study was the only unlabelled off-pathway report; it is now labelled waste (avoided_actions[7]), and the served exercise echocardiogram waste like the exercise test (avoided_actions[8]). (ground_truth.avoided_actions[7]) |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C clinical | minor | ground_truth.action_criteria[2].expected_evidence | 'events on adequate dosing' carried the same drug-failure argument the note rejects. Now 'both within range: no toxic level to explain conduction slowing' | FIXED |
| C clinical | minor | ground_truth.assessment.required_recommendations[5] | Driving must attributed the pacemaker interval to the ESC 2018 main text; now the canonical DR-PM text (ESC 2018 Practical Instructions, Group 1 after 1 week, Group 2 once device function is confirmed; plan C5) | FIXED |
| B consistency | minor | ground_truth.avoided_actions[8] | Exercise echo (fallback) served without a label while the exercise test is waste (plan D4). Now avoid-waste-exercise-echo | FIXED |

## Changes
The reasoning no longer treats normal EEGs as excluding epilepsy or the failure of antiseizure drugs as evidence against it. The diagnosis must, the key evidence, the epilepsy differential and the epilepsy red herring now say that normal routine and ambulatory EEGs do not exclude epilepsy and that the decisive evidence is the loop recorder, which recorded complete AV block with asystole during three typical witnessed episodes. The drug-level criterion now says the levels document exposure before withdrawal. The driving must is attributed to the ESC 2018 Practical Instructions. The electrophysiology study and exercise echocardiogram served if ordered are labelled as waste. 

Checks: perfect_agent.py -v ok; every new label and alternative probed through NeuroBenchEnvironment (each order is served the case's own report and matches only its intended criterion or avoided entry); test_case_guards.py -k for the six RP01-RP05/RS01 ids: 48 passed; case_io.py check: schema and synonym guard OK, no test failure names these cases. No MRI touched.

## Verification
Pass 1: 0 errors found
- Checked the canonical sentence in R0, KCE[0], differential[0] and red_herrings[0], and that no other field still argues from normal EEGs or drug failure (grep of the case); the AED-levels criterion rationale and expected_evidence; DR-PM driving text; the EPS label against its stored report (not performed) and the exercise echo label against the fallback.
- Re-checked: perfect_agent.py -v ok (each criterion receives the report carrying its expected evidence; no avoided entry matches a criterion call); test_case_guards.py -k for the six RP01-RP05/RS01 ids: 48 passed; case_io.py check: schema and synonym guard OK, no test failure names these cases.
Cosmetic (not counted): none.
Pass 2: 0 errors found
- Nothing changed after pass 1 (0 errors), so no field needed re-verification. Re-ran perfect_agent.py -v: ok; test_case_guards.py -k for the six RP01-RP05/RS01 ids: 48 passed.
Cosmetic (not counted): none.
