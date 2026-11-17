# MG-S03

## Reviewer notes
Reviewer status: R2 needs_changes (NB-87MF-FBTV-TPWE) | Approved before this round: no

| note id | ruling | what changed, field paths |
| --- | --- | --- |
| NB-87M:MG-S03:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.action_criteria[1] action-2-order-specialized-test: required -> recommended; removed from stop_rule |
| NB-87M:MG-S03:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.action_criteria[4] action-7-order-specialized-test: recommended -> required; added to stop_rule; ABN escalation criteria replace Lawn 20/30/40 |
| NB-87M:MG-S03:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.required_recommendations[0]: T3 with thoracic oncology (Jacob 2025; ICG 2020) + I1 2 g/kg over 2-5 days, about 146 g by IBW, after HBV/HCV serology and IgG, on clinical indication + anaesthetist clause (old musts 1-2 merged) |
| NB-87M:MG-S03:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.prohibited_recommendations[0]: P2 |
| NB-87M:MG-S03:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.required_recommendations[2], [3]: S2 + S4 (early azathioprine after TPMT, and NUDT15 where available, for type 2 diabetes and BMI 27.8; Jacob 2025; Fionda 2026); S5 inpatient form (HbA1c, lipids, screening, vaccinations, monitoring, DEXA) |
| NB-87M:MG-S03:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.required_recommendations[1]; initial_tool_outputs.ecg; action_criteria[6] action-baseline-ecg: M1 with heart-rate watch on metoprolol; fallback ECG promoted (rate 73 -> 68 to match vitals); new recommended criterion |
| NB-87M:MG-S03:policy_verdict | FIXED (+ CENTRAL C1 swallow criterion) | ground_truth.assessment.required_recommendations[6]: new SLT swallowing assessment must (food sticks, chewing fatigue); criterion CENTRAL C1 |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C clinical | minor | ground_truth.sequence_constraints[0], [1] | Unsourced SFEMG reasons (C3, D3) | FIXED: Q1 texts; SFEMG follow-up moved from followup_outputs[0] to [3] |
| C clinical | minor | ground_truth.action_criteria[3] action-4-order-body-imaging | Sanders 2016 / [Wolfe_2016] for thymoma resection (D24) | FIXED: Jacob 2025; ICG 2020 |
| C clinical | minor | ground_truth.avoided_actions avoid-waste-3-order-advanced-imaging | Stored whole-body FDG-PET served unlabelled (D10) | FIXED: whole_body_FDG_PET alternative; follow-up last |
| C clinical | minor | ground_truth.avoided_actions | Stored speech_language_evaluation served unlabelled (C9, D11) | FIXED: waste label |
| C clinical | minor | ground_truth.assessment.required_recommendations[8] | No MG severity recording (D23) | FIXED: G1, MGFA IIb |
| C clinical | minor | ground_truth.assessment.prohibited_recommendations[2]; key_clinical_evidence[2], [4] | Neurophysiology presented as needed; routine pre-operative rescue | FIXED |
| C clinical | minor | ground_truth.assessment.required_recommendations[5] (metoprolol review) | Checked against D9 (beta-blockers used with caution): already a review, not a ban | no change |
| E language | minor | metadata.difficulty_rationale, last_revised, revision_reason | Stale state and review-log pointer | FIXED |
| A schema | minor | ground_truth.diagnosis.icd_codes | G70.01 ('with exacerbation') granted in a non-exacerbation presentation (D21) | FLAGGED: CENTRAL C4 (diagnosis_synonyms.yaml), not hand-edited |
| D leakage | minor | initial_tool_outputs.labs.interpretation | The closing sentence about AChR antibodies in myasthenia is served with every single-panel lab order (e.g. a thyroid-only order); the same template sentence is in every MG case | FLAGGED: class for the MG lead (rewrite to one sentence per panel or drop) |
| C clinical | minor | ground_truth.action_criteria action-3-order-specialized-test rationale | 'SFEMG is reserved for a normal RNS or seronegative disease' attributed to Jacob 2025 (class C3) | FIXED (verifier pass 1) |
| D leakage | minor | initial_tool_outputs.labs.interpretation | Myasthenia sentence served with every lab order | FIXED (verifier pass 1): sentence removed; earlier FLAGGED row superseded |

## Changes
With AChR antibodies at 6.4 nmol/L repetitive nerve stimulation is now recommended rather than required; the stop rule requires serology, thymic imaging and respiratory function, now required because his bulbar weakness and reduced MIP decide pre-operative rescue. A baseline ECG (sinus 68/min on metoprolol) is stored and recommended before pyridostigmine; the SFEMG report follows the core results with sourced constraint reasons. Management now follows ABN 2025: thymectomy for the thymoma with thoracic oncology referral; MG optimised first, with IVIG 2 g/kg by ideal body weight (about 146 g, not 175 g) after hepatitis serology and IgG, or plasma exchange, on clinical indication; pyridostigmine after the ECG with heart-rate watch; prednisone started in hospital at 5-10 mg and raised to 30 mg, with azathioprine started early because of his diabetes and BMI; HbA1c, lipids, infection screening, vaccinations and steroid monitoring with bone densitometry; an SLT swallowing assessment; MGFA IIb with a baseline MG-ADL. The glucose and metoprolol musts are unchanged. Whole-body FDG-PET and the speech and language battery are labelled waste. The orderable swallow assessment awaits a new vocabulary term (CENTRAL). Checks (17 Nov 2026): perfect_agent.py -v ok (every required and recommended criterion served by the case's own report); test_case_guards.py for the case passed; case_io.py check: no failure names the case. No brain MRI edited (mri_probe not needed). Class LIT: no literature criterion or stored literature output in the case (checked). Not an approved case.

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
- Condition auditor, 17 Nov 2026 (blind leak pass): the stored check_drug_interactions output initial_tool_outputs.drug_interactions.pyridostigmine, interactions[1] named the patient's undiagnosed condition ("myasthenia gravis", "myasthenic weakness" or "MG"). The initial drug output answers the first drug query of any drug, and a follow-up answers a query naming one of the patient's own drugs, so an agent could read the diagnosis before any test (TOOL_REPORT_STYLE_GUIDE: a drug check never announces the diagnosis). Each mention was reworded to the mechanism ("disorders of neuromuscular transmission", "weakness from impaired neuromuscular transmission"); the interaction content, cautions and alternatives are unchanged. Present since 06b74446. Checks after the edit: perfect_agent.py ok; test_case_guards -k MG- passed.
Pass 3: 0 errors found
- Checked the condition-audit drug-check rewording against 06b74446 and HEAD: only the fields the audit names changed, the interaction content, cautions and alternatives are unchanged, the new wording is pharmacologically correct (the drug impairs neuromuscular transmission), no myasthenia/MG wording is left in the stored drug output, and it still agrees with the medication list and the criterion's expected evidence (ground truth, not shown to the agent). Field: interactions[1] (metoprolol). perfect_agent.py -v ok (mediastinum_MRI contrast alternative answered by a fallback where flagged, warning only); test_case_guards.py -k (MG-RS11, RS13..RS16, S03, S04) 56 passed. No change.

## Class changes
- Synonyms (orchestrator, 17 Nov): G70.01 (with exacerbation) is no longer an accepted code in this stable case (diagnosis_synonyms.yaml G70.00 entry, MG CENTRAL C4); the code is a weight-0 component.
