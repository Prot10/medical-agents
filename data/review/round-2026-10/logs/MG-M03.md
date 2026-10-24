# MG-M03
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MG) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance for myasthenia_gravis (no paraneoplastic panel, mediastinal imaging in every case, SFEMG when RNS is negative), applied through the condition plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search` | Leak guard failure (class B): summary and finding were the literature criterion's `expected_evidence`. | FIXED: canonical plan text with three correctly cited results; query re-keyed; criterion optional, last. Guard passes. |
| B | major | `initial_tool_outputs.ct`, `followup_outputs` (`request_thymectomy_evaluation`) | Plan H3: chest CT under the head CT tool plus a duplicate body-imaging follow-up with "Surgical approach feasible" and "Tissue diagnosis recommended" (a resectable encapsulated thymoma goes to resection without biopsy). | FIXED: one `initial_tool_outputs.body_imaging` (region "mediastinum chest", CT, contrast true): 2.2 x 1.8 x 2.0 cm encapsulated nodule "most consistent with a thymoma", upper-lobe emphysema, pertinent negatives, no management. `initial_tool_outputs.ct` null; `fallback_tool_outputs.ct` plain normal head CT. New `request_mediastinum_mri` follow-up with the same nodule. Red herring `field_path` moved to `initial_tool_outputs.body_imaging.findings`. |
| A | major | `followup_outputs` (`request_prostate_cancer_paraneoplastic`), `initial_tool_outputs.labs.panels["Paraneoplastic Panel"]` | Plan H9 and fact 4: PSA plus paraneoplastic panel follow-up, and an initial Hu/Yo/VGCC panel, in MG (Reviewer 2: no paraneoplastic panel). | FIXED: both deleted; the low-risk prostate cancer stays as history. |
| C | major | `initial_tool_outputs.labs`, `ground_truth.key_clinical_evidence` | Anti-titin row (not orderable; at 67 not a thymoma marker by itself, fact 4); "Late-onset MG (>50y) commonly presents with thymoma" (wrong: late-onset MG is mostly non-thymomatous); titin "non-negotiable" line. | FIXED: titin row and the lines removed; summary as out-of-range list; interpretation pattern recital with a hedged antibody comment. |
| B | major | `initial_tool_outputs.labs.panels["Exclusion studies"]` | Class G TSH stub. | FIXED: Thyroid Panel with TSH 2.4 mIU/L and free T4 1.1 ng/dL. |
| B | minor | `initial_tool_outputs.specialized_test` | "Brief facilitation followed by exhaustion" (ambiguous with LEMS facilitation); recommended actions named antibodies, CT and SFEMG. | FIXED: post-exercise repair of decrement with 5% CMAP increment (no facilitation), exhaustion to 16%; technique line; numbered impression; no recommended actions. |
| B | major | `followup_outputs` (`request_tiotropium_interactions_mg`) | Fact 23: "anticholinergic tiotropium may reduce efficacy of cholinergic pyridostigmine at NMJ" (tiotropium is an M3 antagonist with no nicotinic action). | FIXED: rewritten and moved to `initial_tool_outputs.drug_interactions["pyridostigmine"]`: no NMJ interaction, tiotropium may blunt airway muscarinic effects, continue both; caution with bronchial secretions in COPD; other medicines none. |
| A | major | `followup_outputs` (`request_steroid_diabetes_interaction`) | Plan C: steroid hyperglycaemia filed as a drug check with treatment advice. | FIXED: deleted; glucose monitoring and insulin adjustment are in the steroid must. |
| A | minor | `followup_outputs` (`request_analyze_ecg`), `action-8-analyze-ecg` | Plan I: ECG stub ("see impression", rate 0) whose finding was the expected text; no drug in the case needs an ECG. | FIXED: output and optional criterion deleted; the case fallback normal ECG answers an ECG order. |
| D | major | `patient.neurological_exam.additional` | NIF -40 cmH2O and FVC 68% in the exam (class K). | FIXED: removed; SpO2 and absence of distress kept. |
| B | major | `patient.physical_exam`, `followup_outputs` (`request_respiratory_function`) | No weight; FVC 1.9 L contradicted the exam's 68%; no MEP, % predicted or mL/kg. | FIXED: "Weight 92 kg, height 175 cm" (BMI 30.1); FVC 2.45 L (68% predicted, 27 mL/kg), FEV1 1.42 L (51%, GOLD 2 as in the history), FEV1/FVC 0.58, MIP -40, MEP 62 cmH2O, ABG with mild hypoxaemia; impression separates obstruction from muscle weakness. Chest exam (wheeze) added to `physical_exam.respiratory`. |
| B | minor | `followup_outputs` (`request_emg_single_fiber`) | Blocking in 70% of pairs is implausible for a mean MCD of 72. | FIXED: muscle named (left orbicularis oculi), 16 of 20 pairs above the limit, blocking 7 of 20. |
| A | minor | `metadata.actions_withdrawn` | Ice-pack test withdrawn while he has fatigable left-predominant ptosis. | FIXED: `request_ice_pack_test` (left MRD1 1.5 to 4.0 mm) and `action-ice-pack-test` recommended; entry removed. |
| A | major | `ground_truth.action_criteria` | Class A template, drug check required with telithromycin, literature recommended. | FIXED: labs `["anti_AChR","TSH"]`; RNS required; SFEMG optional (RNS diagnostic); ice pack recommended; mediastinal imaging required (CT, chest CT, mediastinal MRI); respiratory recommended; drug check optional `{}`; literature optional last. |
| C | major | `ground_truth.sequence_constraints`, `stop_rule` | Shared constraint; drug check in the stop rule; max 0. | FIXED: `labs -> SFEMG`, `RNS -> SFEMG` soft; stop rule labs, RNS, imaging; max 2. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "Substitute with macrolide or beta-lactam" for COPD exacerbation (macrolides worsen MG; beta-lactam penicillins excluded by his allergy); telithromycin; shared set. | FIXED: canonical drug and steroid prohibitions and "Do not prescribe a penicillin (documented hives)". |
| C | major | `ground_truth.assessment.required_recommendations` | Musts that were tests (confirm AChR, CT); no pyridostigmine or steroid plan. | FIXED: pyridostigmine with COPD caution; thymoma resection referral with pulmonary pre-assessment and pre-operative IVIG or PLEX; prednisone per fact 18 with glucose plan and insulin; azathioprine after TPMT/NUDT15 if long term; MG-safe antibiotic plan for COPD exacerbations (doxycycline; no penicillins); respiratory monitoring thresholds. |
| C | minor | `ground_truth.differential` | LEMS moderate with "anti-VGCC negative expected" after an RNS without facilitation; brainstem stroke cited an MRI. | FIXED: LEMS low with the RNS, reflex, CT and antibody evidence; brainstem key features cite the prior MRI as history. |
| C | minor | `ground_truth.key_clinical_evidence`, `red_herrings` | Shared template lines; red-herring wording. | FIXED: five case-specific lines; red-herring interpretations reworded. |
| C | minor | `ground_truth.avoided_actions[*]` | `[Wolfe_2016]` on waste rationales. | FIXED: case rationales, Jacob 2025 in text, citations empty. |

## Changes, in one paragraph a physician can read before re-reviewing

A 67-year-old man with COPD (GOLD 2), type 2 diabetes, low-risk prostate cancer and penicillin allergy, with fatigable ptosis, diplopia, chewing fatigue and nasal speech. The work-up: AChR binding 0.9 nmol/L with raised blocking and modulating antibodies, normal thyroid function, HbA1c 7.8%; RNS decrement 14% masseter and 11% nasalis with normal CMAPs and no facilitation; a positive left ice-pack test; contrast mediastinal CT with a 2.2 cm encapsulated anterior mediastinal nodule most consistent with thymoma and upper-lobe emphysema; spirometry showing obstruction plus reduced MIP and MEP. The paraneoplastic panel, PSA follow-up, titin, ECG stub and steroid-diabetes "interaction" are gone; the tiotropium check now states the correct pharmacology. Musts: pyridostigmine with COPD caution, thymoma resection after pulmonary assessment with pre-operative IVIG or PLEX, prednisone per the start-low rule with an insulin plan, azathioprine after TPMT if needed, an MG-safe non-penicillin antibiotic plan for COPD exacerbations, and respiratory monitoring thresholds.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Criteria pack keys `[Jacob_2025]`, `[Evoli_2019]`, `[Lawn_2001]` (named in rationale text only) (plan CENTRAL 1).
- `icd_codes[0]` G70.01 for a stable new diagnosis (plan CENTRAL 2; unchanged).

## Open questions for Andrea (judgment calls you could not settle)

None.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the plan (M03 entry), the diff and the whole final case. No notes file exists for MG. Every FIXED finding is in the file: canonical literature (leak guard passes); chest CT moved to body imaging (encapsulated 2.2 cm anterior mediastinal nodule, emphysema) with a consistent MRI follow-up; paraneoplastic panel and PSA follow-up deleted; titin and the "late-onset MG commonly presents with thymoma" line gone; tiotropium check rewritten to the correct pharmacology (M3 antagonist, no nicotinic action); steroid-diabetes "interaction" and ECG stub deleted with their criterion; NIF/FVC out of the exam; respiratory report separates obstruction from muscle weakness (2.45 L / 92 kg = 27 mL/kg). Penicillin allergy: no must names a penicillin, the antibiotic must names doxycycline, and the macrolide alternative of the old prohibition is gone. LEMS lowered with the RNS (5% increment), reflex and CT evidence. Musts fit the thymoma and his diabetes.

Found and changed: the patient has benign prostatic hyperplasia on tamsulosin, and pyridostigmine is contraindicated in mechanical urinary obstruction; the drug check listed tamsulosin as "no interaction" without the BPH caution. Added a warning to `initial_tool_outputs.drug_interactions.pyridostigmine.warnings` (confirm no urinary retention before starting). The drug criterion stays optional (the caution does not change the treatment choice).

Noted, not changed: BMI 92/1.75^2 = 30.0 against 30.1 in demographics (rounding, no clinical consequence).

Checks after the change: `perfect_agent.py MG-M03 -v` passes, `case_io.py check` clean for the case, case guards pass.

## Condition audit (MG auditor, 24 Oct 2026)

- patient.neurological_exam.cranial_nerves: 'limited adduction of left eye' with diplopia on left lateral gaze (HPI: looking to the left) is inconsistent; now limited abduction; levator excursion replaced by MRD1 (left 1.5, right 3.0 mm) matching the ice-pack baseline. FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.

## Close-out (24 Oct 2026)

- `ground_truth.diagnosis.icd_codes[0]` G70.01 -> G70.00. ICD-10-CM G70.01 is myasthenia gravis with (acute) exacerbation, including crisis; this is a new or stable presentation, not an exacerbation. G70.01 stays accepted as a secondary code (plans/MG-decisions.md, Q2).
- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG']; icd_codes = ['G70.00', 'G70.0', 'G70.01']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-1-interpret-labs]`.alternatives: was [anti_AChR, TSH]; now [anti_AChR, TSH, HbA1c] | [anti_AChR, TSH].
- Decision: serve: new first alternative (old order kept as an alternative). A must plans prednisone around HbA1c 7.8% and the key evidence relies on it; the HbA1c was not returned by the antibody and thyroid order.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.
