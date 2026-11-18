# MG-S02

## Reviewer notes
Reviewer status: R2 needs_changes (NB-87MF-FBTV-TPWE) | Approved before this round: no

| note id | ruling | what changed, field paths |
| --- | --- | --- |
| NB-87M:MG-S02:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.action_criteria[1] action-2-order-specialized-test: required -> recommended; removed from stop_rule; rationale per D2 |
| NB-87M:MG-S02:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.action_criteria[0] action-1-interpret-labs: required_arguments.panels [anti_AChR, TSH] -> [anti_AChR, TSH, TRAb] (single alternative, D26); label and rationale name TRAb; citations add [Evoli_2019] [Jacob_2025] |
| NB-87M:MG-S02:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.required_recommendations[3]; key_clinical_evidence[3]; action_criteria[3] rationale: T1 at 29 (ICG 2020 rec 1a, ages 18-50; Jacob 2025), MGTX 18-65 removed; citations [Jacob_2025] [Narayanaswami_2021] |
| NB-87M:MG-S02:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.prohibited_recommendations[0]: P1 replaces the 20 mg/day outpatient prohibition |
| NB-87M:MG-S02:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.required_recommendations[1], [2]: S1 (5-10 mg, +5 mg every 3-5 days to 30 mg) with steroid-sparing clause; S5 with HPV vaccination and steroid monitoring |
| NB-87M:MG-S02:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.required_recommendations[0]; initial_tool_outputs.ecg; action_criteria[6] action-baseline-ecg: M1; case fallback ECG promoted (rate 69 -> 68 to match vitals); new recommended criterion |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C clinical | minor | ground_truth.sequence_constraints[0], [1] | Unsourced 'SFEMG is reserved for seronegative patients' reasons (C3, D3) | FIXED: Q1 texts; SFEMG follow-up moved from followup_outputs[0] to [2] |
| C clinical | minor | ground_truth.action_criteria[4] action-7-order-specialized-test | Rationale cited the Lawn 20/30/40 GBS rule (C7, D8) | FIXED: ABN escalation criteria; stays recommended (chewing fatigue and nasal voice only, D18) |
| C clinical | minor | ground_truth.avoided_actions | Stored speech_language_evaluation report served unlabelled (C9, D11) | FIXED: avoid-waste-speech-language-evaluation; follow-up last |
| C clinical | minor | ground_truth.assessment.required_recommendations[7] | No MG severity recording (D23) | FIXED: G1, MGFA IIb |
| C clinical | minor | ground_truth.assessment.prohibited_recommendations[2]; key_clinical_evidence[2] | Neurophysiology presented as needed with positive serology (D2) | FIXED |
| E language | minor | metadata.difficulty_rationale, last_revised, revision_reason | Stale 'three required studies' and review-log pointer | FIXED |
| A schema | minor | ground_truth.diagnosis.icd_codes | G70.01 ('with exacerbation') granted in a non-exacerbation presentation (D21) | FLAGGED: CENTRAL C4 (diagnosis_synonyms.yaml), not hand-edited |
| D leakage | minor | initial_tool_outputs.labs.interpretation | The closing sentence about AChR antibodies in myasthenia is served with every single-panel lab order (e.g. a thyroid-only order); the same template sentence is in every MG case | FLAGGED: class for the MG lead (rewrite to one sentence per panel or drop) |
| C clinical | minor | ground_truth.action_criteria action-3-order-specialized-test rationale | 'SFEMG is reserved for a normal RNS or seronegative disease' attributed to Jacob 2025 (class C3) | FIXED (verifier pass 1) |
| D leakage | minor | initial_tool_outputs.labs.interpretation | Myasthenia sentence served with every lab order | FIXED (verifier pass 1): sentence removed; earlier FLAGGED row superseded |

## Changes
With AChR antibodies at 8.7 nmol/L repetitive nerve stimulation is now recommended rather than required; the stop rule requires serology and thymic imaging. The serology criterion now names the TSH receptor antibody, on which the Graves orbitopathy differential rests (TRAb 0.4 IU/L, negative). A baseline ECG (sinus 68/min) is stored and recommended before pyridostigmine, and the SFEMG report follows the core results with sourced constraint reasons. Management now follows ABN 2025: pyridostigmine 30 mg three to four times daily after the ECG, up to 360 mg/day; prednisone from 5-10 mg, rising by 5 mg every 3-5 days to 30 mg if symptoms persist, with no full-dose start (the unsourced 20 mg/day prohibition is gone); screening before immunosuppression including HPV vaccination, and steroid monitoring; early thymectomy at 29 under ICG 2020 recommendation 1a and ABN, with pre-operative IVIG or plasma exchange only on clinical indication; MGFA IIb with a baseline MG-ADL. The speech and language battery is labelled waste. The optional swallow assessment awaits a new vocabulary term (CENTRAL). Checks (17 Nov 2026): perfect_agent.py -v ok (every required and recommended criterion served by the case's own report); test_case_guards.py for the case passed; case_io.py check: no failure names the case. No brain MRI edited (mri_probe not needed). Class LIT: no literature criterion or stored literature output in the case (checked). Not an approved case.

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
