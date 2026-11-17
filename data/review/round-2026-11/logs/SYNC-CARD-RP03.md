# SYNC-CARD-RP03

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-8-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed, field paths |
| --- | --- | --- |
| d08aab43-e04e-41e3-8889-62b6e06babee | CENTRAL | The stored data were consistent: RYR2 row 'Pathogenic'; KCNJ2 row 'No pathogenic variants detected'; the 'Pathogenic' and 'Positive for pathogenic RYR2 variant' seen next to KCNJ2 belong to the next row, 'Overall panel result', because the review app prints interpretation and result above the test name. To prevent the misreading, the four empty per-gene interpretations (CASQ2, TRDN, CALM1, KCNJ2) now read 'Negative'. Reason: web-review/src/components/cases/CaseDetail.tsx: print a row's label key (test) before interpretation, result and abnormal (plan CENTRAL C1d, D20). (followup_outputs[6].output.findings) |
| 8baf17ba-b962-4925-bbd2-568da02ac658 | FIXED | The exercise echocardiogram is now an accepted alternative of the exercise-test criterion (it answers the same question in CPVT). A second exercise study after the first claims no criterion, so it lowers tool accuracy and counts as an extra action against the stop rule. Not removed (plan D3): a stored report is only the answer served if an agent orders that test, not a step taken; deleting it would let the benchmark library answer with a normal report that contradicts this patient (library_contradictions.yaml, test_library_never_answers_a_contradicted_order). The physician's point is applied as an avoided-action label. (ground_truth.action_criteria[5].alternatives[1]) |
| 14be9288-6d0a-4b3f-baf6-d0e4add27bf8 | FIXED | Bubble study labelled waste (no stroke, TIA, unexplained hypoxaemia or suspected shunt). Not removed (plan D3): a stored report is only the answer served if an agent orders that test, not a step taken; deleting it would let the benchmark library answer with a normal report that contradicts this patient (library_contradictions.yaml, test_library_never_answers_a_contradicted_order). The physician's point is applied as an avoided-action label. (ground_truth.avoided_actions[5]) |
| c42c1ec4-446c-4413-8f37-e393e21895e1 | FIXED | Cascade genetic testing and clinical evaluation (ECG and exercise testing) of all first-degree relatives, naming her mother, her sister and both children; the genetic-panel rationale and key evidence [5] now name the mother too. (ground_truth.assessment.required_recommendations[7]) |
| 99f45b73-bb55-4b95-86a8-93180445e69b | FIXED | Must rewritten per BSG 2021 (Snook 2021): review dose, timing and adherence of oral iron; intravenous iron if oral iron is ineffective, not tolerated or inappropriate; investigate the cause (menstrual losses, coeliac serology, gastrointestinal evaluation as indicated). (ground_truth.assessment.required_recommendations[8]) |
| NB-87M:SYNC-CARD-RP03:policy_verdict | NO-ACTION | Verdict without comment; its needs_revision dimensions are covered by the five notes of this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C clinical | minor | ground_truth.action_criteria[7].rationale; ground_truth.key_clinical_evidence[5] | Cascade testing named the sister and children only (class of note c42c1ec4). Both now name the mother, the sister and both children | FIXED |
| E language | minor | ground_truth.action_criteria[5].label | With the exercise echo accepted as an alternative, the label now reads 'Monitored exercise test (exercise ECG or exercise echocardiography)' | FIXED |
| B consistency | minor | ground_truth.avoided_actions[6] | TEE (fallback) served without a label (class C3). Now avoid-waste-tee | FIXED |

## Changes
Cascade genetic testing and clinical evaluation now cover every first-degree relative, her mother included. The iron-deficiency must follows BSG 2021: review the oral iron, give intravenous iron only if oral iron is ineffective, not tolerated or inappropriate, and investigate the cause. The exercise echocardiogram is now an accepted alternative of the required exercise test, so a second exercise study after the first earns nothing and counts against the stop rule; its stored report stays, as an answer if ordered. The bubble study and TEE are labelled as waste. In the genetic report the per-gene negative rows now say 'Negative'; the data were already consistent (RYR2 pathogenic, KCNJ2 negative) and the misreading comes from the review app printing the result above the gene name, a display fix requested centrally. 

Checks: perfect_agent.py -v ok; every new label and alternative probed through NeuroBenchEnvironment (each order is served the case's own report and matches only its intended criterion or avoided entry); test_case_guards.py -k for the six RP01-RP05/RS01 ids: 48 passed; case_io.py check: schema and synonym guard OK, no test failure names these cases. No MRI touched.

## Verification
Pass 1: 0 errors found
- Checked all six notes: the genetic report rows (RYR2 pathogenic, four per-gene rows now 'Negative', overall row pathogenic) agree with the impression; the exercise echo alternative is served its own report, which carries the exercise-induced bidirectional and polymorphic VT; cascade screening names the living mother, sister and both children (father deceased) in R7, the genetic-panel rationale and KCE[5]; the iron must follows BSG 2021 and matches the history (intermittent oral iron, dose recently increased). Observation for the lead (pre-existing, not changed): `rejected` contains 'iron deficiency anaemia', so an answer such as 'CPVT with coexisting iron deficiency anaemia' is vetoed by DiagnosisCriterion.matches (tested: False) although R8 asks the agent to treat the anaemia; 'CPVT, not iron deficiency anaemia' scores.
- Re-checked: perfect_agent.py -v ok (each criterion receives the report carrying its expected evidence; no avoided entry matches a criterion call); test_case_guards.py -k for the six RP01-RP05/RS01 ids: 48 passed; case_io.py check: schema and synonym guard OK, no test failure names these cases.
Cosmetic (not counted): none.
Pass 2: 0 errors found
- Nothing changed after pass 1 (0 errors), so no field needed re-verification. Re-ran perfect_agent.py -v: ok; test_case_guards.py -k for the six RP01-RP05/RS01 ids: 48 passed.
Cosmetic (not counted): none.
