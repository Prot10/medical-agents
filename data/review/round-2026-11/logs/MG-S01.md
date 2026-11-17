# MG-S01

## Reviewer notes
Reviewer status: R2 needs_changes (NB-87MF-FBTV-TPWE) | Approved before this round: no

| note id | ruling | what changed, field paths |
| --- | --- | --- |
| NB-87M:MG-S01:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.action_criteria[1] action-2-order-specialized-test: required -> recommended; rationale: good practice with positive serology, mandatory when antibodies are negative [Jacob_2025]; removed from stop_rule |
| NB-87M:MG-S01:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.action_criteria[4] action-7-order-specialized-test: recommended -> required; added to stop_rule; Lawn 20/30/40 rationale replaced by ABN escalation criteria; evidence adds the single-breath count |
| NB-87M:MG-S01:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.required_recommendations[0]: T3 (thoracic surgery and thoracic oncology, Jacob 2025; ICG 2020) + I1 (1 g/kg over 2-3 days, IBW 59.5 kg, about 60 g, after HBV/HCV serology and IgG, or 5 plasma exchanges) + FVC/MIP before anaesthesia and anaesthetist informed (merged from old must 2) |
| NB-87M:MG-S01:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.required_recommendations[2], [3]: S2 (inpatient 5-10 mg, +5 mg alternate days to 30 mg) with the steroid-sparing clause; S5 inpatient form with HPV vaccination |
| NB-87M:MG-S01:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.prohibited_recommendations[0]: P2 replaces the 20 mg/day outpatient prohibition |
| NB-87M:MG-S01:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.required_recommendations[1]; initial_tool_outputs.ecg; action_criteria[6] action-baseline-ecg: M1 (ECG before pyridostigmine, 360 mg/day maximum); case fallback ECG promoted (rate set to 74 to match vitals), new recommended criterion |
| NB-87M:MG-S01:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.required_recommendations[5]: swallow must reworded as a speech and language therapy swallowing assessment (Jacob 2025); criterion CENTRAL C1 |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C clinical | minor | ground_truth.sequence_constraints[0], [1] | 'SFEMG is reserved for seronegative patients' reasons, unsourced (C3, D3) | FIXED: Q1 texts, [Jacob_2025]; SFEMG follow-up moved from followup_outputs[0] to [3], after ice pack, mediastinal MRI and respiratory function |
| C clinical | minor | ground_truth.action_criteria[3] action-4-order-body-imaging | Rationale cited Sanders 2016 and [Wolfe_2016] for thymoma resection (D24) | FIXED: Jacob 2025; ICG 2020, citations [Jacob_2025] [Narayanaswami_2021] |
| C clinical | minor | ground_truth.avoided_actions avoid-waste-3-order-advanced-imaging | A stored whole-body FDG-PET follow-up was served unlabelled (label covered FDG_PET only) (C9, D10) | FIXED: alternative modality whole_body_FDG_PET added; rationale [Jacob_2025]; follow-up moved last |
| C clinical | minor | ground_truth.avoided_actions | Stored speech_language_evaluation report served unlabelled (C9, D11) | FIXED: avoid-waste-speech-language-evaluation (waste, [Jacob_2025]); follow-up moved to the end |
| C clinical | minor | ground_truth.assessment.required_recommendations[7] | No MG severity recording (D23) | FIXED: G1, MGFA IIb to III (as the label) |
| C clinical | minor | ground_truth.assessment.prohibited_recommendations[2] | 'before AChR antibody testing and neurophysiology' after the RNS downgrade (D2) | FIXED: '(and neurophysiology when serology is negative)' |
| C clinical | minor | ground_truth.key_clinical_evidence[2], [4] | RNS presented as part of what establishes the diagnosis; pre-operative IVIG/PLEX stated as routine | FIXED: serology establishes, RNS supports; rescue on clinical indication with oncology referral |
| E language | minor | metadata.difficulty_rationale, last_revised, revision_reason | Described the October state and pointed to a review log | FIXED |
| A schema | minor | ground_truth.diagnosis.icd_codes | G70.01 ('with exacerbation') granted in a non-exacerbation presentation (D21) | FLAGGED: CENTRAL C4 (diagnosis_synonyms.yaml), not hand-edited |
| D leakage | minor | initial_tool_outputs.labs.interpretation | The closing sentence about AChR antibodies in myasthenia is served with every single-panel lab order (e.g. a thyroid-only order); the same template sentence is in every MG case | FLAGGED: class for the MG lead (rewrite to one sentence per panel or drop) |
| C clinical | minor | ground_truth.action_criteria action-3-order-specialized-test rationale | 'SFEMG is reserved for a normal RNS or seronegative disease' attributed to Jacob 2025 (class C3) | FIXED (verifier pass 1) |
| D leakage | minor | initial_tool_outputs.labs.interpretation | Myasthenia sentence served with every lab order | FIXED (verifier pass 1): sentence removed; earlier FLAGGED row superseded |

## Changes
With AChR antibodies at 12.4 nmol/L the diagnosis is serological, so repetitive nerve stimulation is now recommended rather than required and no longer gates the assessment; the stop rule requires serology with thyroid function, thymic imaging and respiratory function, which became required because her bulbar weakness and reduced MIP decide pre-operative rescue. A baseline ECG (sinus 74/min, normal intervals) is stored and recommended before pyridostigmine. The SFEMG report now follows the core results, and both constraint reasons say what ABN 2025 says. Management now follows ABN 2025: thymectomy for the thymoma with thoracic oncology referral, MG optimised first and IVIG 1 g/kg by ideal body weight (about 60 g) after hepatitis serology and IgG, or plasma exchange, on clinical indication; pyridostigmine 30 mg three to four times daily after the ECG, up to 360 mg/day; prednisone started in hospital at 5-10 mg and raised to 30 mg (the unsourced 20 mg/day prohibition is replaced by 'no outpatient start with significant bulbar weakness', Evoli 2019); screening before immunosuppression with HPV vaccination and steroid monitoring; an SLT swallowing assessment; MGFA IIb to III with a baseline MG-ADL. Whole-body FDG-PET and the speech and language battery are labelled waste. The orderable swallow assessment awaits a new vocabulary term (CENTRAL). Checks (17 Nov 2026): perfect_agent.py -v ok (every required and recommended criterion served by the case's own report); test_case_guards.py for the case passed; case_io.py check: no failure names the case. No brain MRI edited (mri_probe not needed). Class LIT: no literature criterion or stored literature output in the case (checked). Not an approved case.

## Verification
Pass 1: 2 errors found
- ground_truth.action_criteria action-3-order-specialized-test (SFEMG) rationale still said 'SFEMG is reserved for a normal RNS or seronegative disease (Jacob)', the rule the reviewer found Jacob 2025 does not state (note 4382d2ff, class C3/D3 not applied to the criterion rationale): reworded to 'considered when RNS is normal and suspicion persists, where expertise is available (Jacob 2025)', citation [Jacob_2025] added.
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
