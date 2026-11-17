# MG-S05

## Reviewer notes
Reviewer status: R2 needs_changes (NB-87MF-FBTV-TPWE) | Approved before this round: no

| note id | ruling | what changed, field paths |
| --- | --- | --- |
| NB-87M:MG-S05:policy_verdict | FIXED | ground_truth.action_criteria[2] action-3-order-specialized-test: required -> recommended (both alternatives kept); removed from stop_rule; rationale per D2 |
| NB-87M:MG-S05:policy_verdict | FIXED | ground_truth.assessment.required_recommendations[1]: S3 ocular protocol (Jacob 2025; ICG 2020 ocular MG section) |
| NB-87M:MG-S05:policy_verdict | FIXED | ground_truth.assessment.prohibited_recommendations (old [0]): deleted (20 mg/day is the ocular target, not a ceiling) |
| NB-87M:MG-S05:policy_verdict | FIXED | ground_truth.assessment.required_recommendations[0]; initial_tool_outputs.ecg; action_criteria[4] action-baseline-ecg: M1; fallback ECG promoted (rate 68 = vitals); new recommended criterion |
| NB-87M:MG-S05:policy_verdict | FIXED | ground_truth.assessment.required_recommendations[2]: new: HbA1c, lipids, BP and weight before prednisone; HBV, HCV, TB, HIV and vaccinations if long-term immunosuppression is planned; steroid monitoring (Jacob 2025; Fionda 2026) |
| NB-87M:MG-S05:policy_verdict | FIXED | ground_truth.assessment.prohibited_recommendations[1]; key_clinical_evidence[0], [1], [2]: D27 wording: RNS often normal in ocular disease, SFEMG more sensitive; ice-pack above 2 mm, NPV 94% (Evoli 2019); ~80% and ~50% removed |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C clinical | minor | ground_truth.action_criteria[0] rationale; initial_tool_outputs.labs.interpretation | The same unsourced 'about half of ocular MG' AChR figure (D27 class within the case) | FIXED: figure removed; served interpretation says antibodies are detected less often in purely ocular than in generalized disease |
| C clinical | minor | ground_truth.action_criteria[1] action-2-order-specialized-test rationale | 'at least 2 mm' threshold | FIXED: 'more than 2 mm', NPV 94% (Evoli 2019), citation [Evoli_2019] |
| C clinical | minor | ground_truth.assessment.required_recommendations[3] | 'generalizes in about half, mostly within 2 years' had no citation | FIXED: (Jacob 2025), as in the criteria pack; figure kept |
| C clinical | minor | ground_truth.assessment.required_recommendations[6] | No MG severity recording (D23) | FIXED: G1, MGFA I |
| E language | minor | metadata.difficulty_rationale, last_revised, revision_reason | Stale 'three required steps' and review-log pointer | FIXED |
| A schema | minor | ground_truth.diagnosis.icd_codes | G70.01 ('with exacerbation') granted in a non-exacerbation presentation (D21) | FLAGGED: CENTRAL C4 (diagnosis_synonyms.yaml), not hand-edited |
| D leakage | minor | initial_tool_outputs.labs.interpretation | Myasthenia sentence served with every lab order | FIXED (verifier pass 1): sentence removed; earlier FLAGGED row superseded |

## Changes
With AChR binding antibody 2.9 nmol/L the diagnosis is serological, so neurophysiology (RNS or SFEMG, either accepted) is now recommended rather than required; an agent that confirms ocular MG by serology and the ice-pack test and images the thymus is no longer penalised. A baseline ECG (sinus 68/min) is stored and recommended before pyridostigmine. Management now follows ABN 2025: pyridostigmine after the ECG, up to 360 mg/day; if ptosis or diplopia stay disabling, prednisone 5-10 mg rising by 5 mg every 3-5 days to 20 mg (maximum 0.5 mg/kg, not above 30 mg), citing the ICG 2020 ocular section; the unsourced 20 mg/day prohibition is deleted; HbA1c, lipids and infection screening before steroids and steroid monitoring; MGFA I with a baseline MG-ADL. The RNS contraindication and the teaching pearls no longer quote unsourced sensitivity figures; the ice-pack test is described by the Evoli 2019 criterion (above 2 mm, negative predictive value 94%). Checks (17 Nov 2026): perfect_agent.py -v ok (every required and recommended criterion served by the case's own report); test_case_guards.py for the case passed; case_io.py check: no failure names the case. No brain MRI edited (mri_probe not needed). Class LIT: no literature criterion or stored literature output in the case (checked). Not an approved case.

## Verification
Pass 1: 1 errors found
- initial_tool_outputs.labs.interpretation: the closing sentence 'Acetylcholine receptor antibodies are detected less often in purely ocular than in generalized myasthenia' was served with every lab order, including a thyroid-only order (probe), naming myasthenia in a report the AChR order was not part of (answer leakage; the worker had only flagged it): sentence removed; probes of TSH-only, HbA1c-only and AChR+TSH orders now return only their own panels' sentences.
Cosmetic (not counted): none.
Rulings checked: the policy_verdict note ruling (FIXED) is right; every point of the note is applied as the plan says.
Checks after the verifier edits (17 Nov 2026): perfect_agent.py -v ok, every required and recommended criterion answered by its own stored report; test_case_guards.py -k (MG-RS17, MG-S01..S05) 48 passed; case_io.py check (run before the cosmetic ice-pack wording edit, which changes rationale text only): schema OK, synonym guard OK, no test failure names these cases.
Pass 2: 0 errors found
- Checked the pass-1 lab interpretation edit (AChR sentence removed): checked against every panel row and abnormal_values_summary (AChR binding 2.9 nmol/L, blocking 34%, all other panels normal), no myasthenia wording left in any lab text.
- Cosmetic (not counted): the stored ice-pack report impression still reads 'improvement in ptosis of at least 2 mm' while the criterion rationale says 'more than 2 mm'; the stored improvement exceeds 2 mm, so no conclusion changes.
- Checks (17 Nov 2026): perfect_agent.py -v ok; test_case_guards.py -k (MG-RS17, MG-S01..S05) 48 passed. No change made in pass 2.

## Class changes
- Synonyms (orchestrator, 17 Nov): G70.01 (with exacerbation) is no longer an accepted code in this stable case (diagnosis_synonyms.yaml G70.00 entry, MG CENTRAL C4); the code is a weight-0 component.
