# MG-RS17

## Reviewer notes
Reviewer status: R2 needs_changes (NB-87MF-FBTV-TPWE) | Approved before this round: no

| note id | ruling | what changed, field paths |
| --- | --- | --- |
| NB-87M:MG-RS17:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.action_criteria[1] action-2-order-specialized-test: required -> recommended; removed from stop_rule; rationale notes the very low ALS differential |
| NB-87M:MG-RS17:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.required_recommendations[3]; key_clinical_evidence[3]; action_criteria[3] action-3-order-body-imaging rationale: T2 at 60 with the Evoli clause; MGTX 18-65 removed; citations [Jacob_2025] [Narayanaswami_2021] |
| NB-87M:MG-RS17:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.prohibited_recommendations[0]: P2 (she is an inpatient with dysphagia to solids and a reduced gag: inpatient start, worker decision per plan) |
| NB-87M:MG-RS17:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.required_recommendations[1], [2]: S2 (5-10 mg, +5 mg alternate days to 30 mg) with steroid-sparing clause; S5 inpatient form, naming BMI 26.4 and family history of diabetes, with DEXA |
| NB-87M:MG-RS17:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.required_recommendations[4]: R1 (ABN ICU/HDU criteria) replaces MIP -30; impending crisis: IVIG 2 g/kg by IBW (about 114 g at 165 cm) after HBV/HCV serology and IgG, or 5 plasma exchanges |
| NB-87M:MG-RS17:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.required_recommendations[0]; initial_tool_outputs.ecg; action_criteria[6] action-baseline-ecg: M1 replaces 'maximum about 360 mg/day'; fallback ECG promoted (rate 74 = vitals); new recommended criterion |
| NB-87M:MG-RS17:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.required_recommendations[5]: SLT swallowing assessment wording; criterion CENTRAL C1 |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C clinical | major | ground_truth.action_criteria[4] action-7-order-specialized-test | Respiratory function recommended despite dysphagia and a reduced gag in an admitted patient; Lawn 20/30/40 rationale (C11, C7) | FIXED: required, in stop_rule, ABN criteria |
| C clinical | minor | ground_truth.sequence_constraints[0], [1]; key_clinical_evidence[2] | Unsourced 'SFEMG is reserved for seronegative patients' and '~85% sensitivity' (C3, D3, D27 class) | FIXED: Q1 texts; KCE[2] sourced to Jacob 2025 without the figure; SFEMG follow-up moved from [0] to [2] |
| C clinical | minor | ground_truth.avoided_actions | Stored speech_language_evaluation served unlabelled (C9) | FIXED: waste label; follow-up last |
| C clinical | minor | ground_truth.assessment.required_recommendations[7] | No MG severity recording (D23) | FIXED: G1, MGFA IIa |
| C clinical | minor | ground_truth.assessment.prohibited_recommendations[2] | Neurophysiology wording after the RNS downgrade (D2) | FIXED |
| E language | minor | metadata.difficulty_rationale, last_revised, revision_reason | Stale state and review-log pointer | FIXED |
| A schema | minor | ground_truth.diagnosis.icd_codes | G70.01 ('with exacerbation') granted in a non-exacerbation presentation (D21) | FLAGGED: CENTRAL C4 (diagnosis_synonyms.yaml), not hand-edited |
| D leakage | minor | initial_tool_outputs.labs.interpretation | The closing sentence about AChR antibodies in myasthenia is served with every single-panel lab order (e.g. a thyroid-only order); the same template sentence is in every MG case | FLAGGED: class for the MG lead (rewrite to one sentence per panel or drop) |
| C clinical | minor | ground_truth.action_criteria action-single-fiber-emg rationale | 'SFEMG is reserved for a normal RNS or seronegative disease' attributed to Jacob 2025 (class C3) | FIXED (verifier pass 1) |
| D leakage | minor | initial_tool_outputs.labs.interpretation | Myasthenia sentence served with every lab order | FIXED (verifier pass 1): sentence removed; earlier FLAGGED row superseded |

## Changes
With AChR antibodies at 8.7 nmol/L repetitive nerve stimulation is now recommended rather than required; the stop rule requires serology, thymic imaging and respiratory function, now required because she is admitted with dysphagia to solids and a reduced gag. A baseline ECG (sinus 74/min) is stored and recommended before pyridostigmine; the SFEMG report follows the core results with sourced constraint reasons. Management now follows ABN 2025: pyridostigmine 30 mg three to four times daily after the ECG, up to 360 mg/day; prednisone started in hospital at 5-10 mg and raised to 30 mg (the unsourced 20 mg/day prohibition is replaced by 'no outpatient start with significant bulbar weakness', Evoli 2019); screening before immunosuppression and steroid monitoring, with close glucose checks for her BMI and family history of diabetes; thymectomy discussed at 60, recording that ABN advises discussion at 50-65, ICG 2020 found no benefit at 50 or over and the Italian recommendations divert AChR-positive patients over 60; repeat FVC with the ABN ICU/HDU criteria and IVIG 2 g/kg by ideal body weight (about 114 g) or plasma exchange for impending crisis; an SLT swallowing assessment; MGFA IIa with a baseline MG-ADL. The speech and language battery is labelled waste. The orderable swallow assessment awaits a new vocabulary term (CENTRAL). Checks (17 Nov 2026): perfect_agent.py -v ok (every required and recommended criterion served by the case's own report); test_case_guards.py for the case passed; case_io.py check: no failure names the case. No brain MRI edited (mri_probe not needed). Class LIT: no literature criterion or stored literature output in the case (checked). Not an approved case.

## Verification
Pass 1: 2 errors found
- ground_truth.action_criteria action-single-fiber-emg (SFEMG) rationale still said 'SFEMG is reserved for a normal RNS or seronegative disease (Jacob)', the rule the reviewer found Jacob 2025 does not state (note 4382d2ff, class C3/D3 not applied to the criterion rationale): reworded to 'considered when RNS is normal and suspicion persists, where expertise is available (Jacob 2025)', citation [Jacob_2025] added.
- initial_tool_outputs.labs.interpretation: the closing sentence 'Acetylcholine receptor antibodies are found in most patients with generalized autoimmune myasthenia' was served with every lab order, including a thyroid-only order (probe), naming myasthenia in a report the AChR order was not part of (answer leakage; the worker had only flagged it): sentence removed; probes of TSH-only, HbA1c-only and AChR+TSH orders now return only their own panels' sentences.
Cosmetic (not counted): ice-pack criterion rationale 'at least 2 mm' changed to 'more than 2 mm' (Evoli 2019 positivity threshold; the stored improvement exceeds 2 mm either way).
Rulings checked: the policy_verdict note ruling (FIXED, swallow criterion CENTRAL C1) is right; every point of the note is applied as the plan says.
Checks after the verifier edits (17 Nov 2026): perfect_agent.py -v ok, every required and recommended criterion answered by its own stored report; test_case_guards.py -k (MG-RS17, MG-S01..S05) 48 passed; case_io.py check (run before the cosmetic ice-pack wording edit, which changes rationale text only): schema OK, synonym guard OK, no test failure names these cases.
Pass 2: 0 errors found
- Checked the pass-1 SFEMG criterion rationale (now the D3/Q1 wording, [Jacob_2025]; agrees with both sequence-constraint reasons, no 'reserved for seronegative' text left anywhere in the case) and the pass-1 lab interpretation edit (AChR sentence removed; interpretation checked row by row against the panels and abnormal_values_summary, no myasthenia wording left in any lab text); the cosmetic ice-pack 'more than 2 mm' rationale agrees with the stored improvement.
- Cosmetic (not counted): the stored ice-pack report impression still reads 'improvement in ptosis of at least 2 mm' while the criterion rationale says 'more than 2 mm'; the stored improvement exceeds 2 mm, so no conclusion changes.
- Checks (17 Nov 2026): perfect_agent.py -v ok; test_case_guards.py -k (MG-RS17, MG-S01..S05) 48 passed. No change made in pass 2.

## Class changes
- Synonyms (orchestrator, 17 Nov): G70.01 (with exacerbation) is no longer an accepted code in this stable case (diagnosis_synonyms.yaml G70.00 entry, MG CENTRAL C4); the code is a weight-0 component.
