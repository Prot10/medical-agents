# ALZ-EARLY-RM01
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 0941bb75-edbd-4f1a-8927-1856cc084c13 | FIXED | `ground_truth.diagnosis.accepted[0]` "Mild cognitive impairment due to Alzheimer's disease (amnestic, multi-domain)" became "Early-onset Alzheimer disease (mild dementia, amnestic) with cerebrovascular contribution"; `icd_codes[0]` G31.84 became G30.0 (onset at 61) and the duplicate G30.0 was dropped from the tail. `clinical_assessment.criteria_met.independence_in_instrumental_activities_lost` true, stage "mild dementia", impression names the losses (medicine reminders, finances and appointments, stove incidents); neuropsych impression harmonised to mild dementia. The MCI synonym labels after `accepted[0]` were not hand-edited: CENTRAL. |
| b2c0d3cc-0f52-4afb-8d26-e451fbea4353 | FIXED | `initial_tool_outputs.mri.impression` item 2 names Fazekas grade 2 white matter hyperintensities and the 4 mm chronic left putaminal lacune as moderate small vessel disease; MRI criterion expected evidence and label include it; label names the cerebrovascular contribution; must on vascular risk with LDL 148 mg/dL (start a statin) and blood pressure; VCI differential and KCE[1] state it as a contributor. |
| 2e39ab2d-23f2-4d5d-a5e5-0470e3f6556f | FIXED | Now staged as mild dementia, so the donepezil check stays as an optional post-diagnostic step, last in the order, `{"drug": "donepezil"}`; output rewritten (`followup_outputs[4]`, trigger `check_drug_interactions_donepezil`): the false claim that amlodipine slows the heart rate is gone; pulse 72; aspirin GI mechanism; no CKD dose change. Canonical dementia AChEI must added. |
| 262248db-5ae4-4c26-b958-793fc54bdeea | FIXED | Literature follow-up (which cited a non-existent "2023 AAN MCI guideline" recommending AChEI first-line) deleted; no literature criterion existed; `initial`/`fallback` literature already null. KCE item "Cholinesterase inhibitors are first-line..." deleted. |
| 9229c61a-cc7c-44bb-97a8-437eed578bea | FIXED | `initial_tool_outputs.mri.additional_observations[0]` "No mass lesions or abnormal enhancement post-gadolinium" became "No mass lesion". |
| 175f3c29-8209-4e0c-b5b6-91b6b0138110 | FIXED | Summary comment (staging, cerebrovascular contribution): resolved by 0941bb75 and b2c0d3cc. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `patient.neurological_exam.mental_status`, `clinical_assessment.findings` | MMSE "24/30" with points lost summing to 5 (orientation 2, recall 2, serial sevens 1) while 0/3 objects were recalled (3 points). | FIXED: "delayed recall (3)", "Recalled 0/3 objects at 5 minutes, and none with category cues." |
| B | major | `initial_tool_outputs.labs` (creatinine), `patient...past_medical_history[2]` | Creatinine 1.1 mg/dL in a 62-year-old woman gives eGFR about 57 (CKD-EPI 2021, G3a), contradicting "CKD stage 2, stable". | FIXED: creatinine 0.98 mg/dL (in range), eGFR 65 mL/min/1.73m2 added (G2, consistent with the history); abnormal summary and interpretation recite BUN, cholesterol and LDL only, without "consistent with CKD 2". Panel renamed Comprehensive Metabolic Panel with total protein, albumin, ALT, AST, ALP, bilirubin (normal). |
| C | major | `followup_outputs[1]` CSF | 14-3-3, RT-QuIC and NfL in a non-rapid case; no Abeta40 behind the stated ratio; "(normal)" in the cell count (C6). | FIXED: routine AD panel only, Abeta40 8020 added (385/8020 = 0.048), vocabulary keys, references aligned with the condition (Abeta42 >600, ratio >0.065), pattern interpretation. |
| B | major | `action-9-analyze-csf` | "single optional biological-confirmation route"; amyloid PET got the library's negative report (C2). | FIXED: two alternatives, canonical label, rationale, expected evidence; new follow-up `order_amyloid_pet` (positive, Centiloid 74). Probe of every alternative: CSF <- `followup_outputs[1]`, PET <- [2], gene panel <- [3], drug check <- [4]; no library answer. |
| C | major | `ground_truth.differential`, `red_herrings` | DLB and FTD left `moderate` with template key features; VCI said "No significant cerebrovascular burden on MRI" despite Fazekas 2 and a lacune. The case (seeded from a DLB report, `metadata.source_original_diagnosis`) contains mild fluctuations, hypnagogic images, positional dizziness and an uncle with PD, which the differential did not weigh. | FIXED: DLB low with what raises it and what argues against it (images only hypnagogic and recognized, no RBD, no parkinsonism, storage-type deficit, MTA 2, AD CSF), co-pathology and reassessment stated; FTD low; VCI "as the sole cause" low, with small vessel disease named as contributor; depression and reversible causes reworded from case data. New red herring for the Lewy-type features. |
| C | major | `ground_truth.assessment` | Musts restated tool steps and the engineering biomarker must; no stove, medicine or finance safety measures; no vascular must despite untreated LDL 148 and a lacune; generic prohibitions (anticholinergics, benzodiazepines). | FIXED: musts for informant history, disclosure and planning, concrete safety (cooking, blister pack, finances, driving), canonical biomarker and AChEI musts, vascular risk (statin, BP), lying and standing BP for positional lightheadedness on amlodipine, follow-up for Lewy features. Prohibitions: depression attribution, antipsychotic for hypnagogic images (Lewy sensitivity), memantine at the mild stage. |
| C | minor | `followup_outputs[0].output.impression` | Rey Complex Figure delayed recall listed as executive function; "amnestic MCI". | FIXED: visual memory item separated; numbered impression; mild dementia wording. |
| D | minor | gene panel follow-up | Finding "value" was the criterion's expected-evidence sentence. | FIXED: APP, PSEN1, PSEN2 negative; expected evidence states the result; rationale explains the weak family history. |
| C | minor | `ground_truth.key_clinical_evidence` | MMSE-normal-range, storage-deficit, APOE, B12 (B12 is 310) and AChEI-first-line template items. | FIXED: four case-specific items (staging, vascular copathology, Lewy features, one biomarker test). |
| A | minor | criteria citations, rationales, order; constraints; stop rule | Duplicate keys, rationale = label, MRI-before-LP reason said "particularly in older patients" for a 62-year-old, `max_additional_actions` 0. | FIXED: one key each, case-specific rationales, order per plan 3.1, MRI-before-CSF reason shortened, assessment-before-biomarker and battery-before-genetics added, `max_additional_actions` 1. |
| C | minor | `avoided_actions[0]` | Generic ECG rationale. | FIXED: case-specific (no QT drug; positional symptoms need orthostatic BP). |
| E | minor | `metadata.difficulty_description`, `difficulty_rationale`, `key_educational_points` | Engineering wording. | FIXED. `source_original_diagnosis` (provenance) left unchanged. |

## Changes, in one paragraph a physician can read before re-reviewing

The case is restaged as mild Alzheimer dementia with a cerebrovascular contribution (G30.0, onset at 61): she needs reminders for medicines and help with finances and appointments and has left the stove on, and the clinical assessment, neuropsychological impression and label now agree. The MMSE item arithmetic was corrected (0/3 recall). The MRI names Fazekas 2 small vessel disease and the putaminal lacune, and a must asks for a statin for LDL 148 mg/dL and blood pressure control. Creatinine was corrected to match the stable CKD stage 2 in the history. The CSF now contains only the Alzheimer panel, with Abeta40 behind its ratio. CSF or amyloid PET can establish amyloid status (optional, one test enough; a concordant positive PET was added). The literature step citing a non-existent AAN guideline is gone, the MRI no longer mentions gadolinium, and the donepezil check is an optional last step with correct pharmacology (amlodipine does not slow the heart). Because the history carries Lewy-type features (mild fluctuations, hypnagogic images, positional dizziness, uncle with PD), DLB stays in the differential at low likelihood with the reasons, a red herring explains them, the antipsychotic prohibition is tied to Lewy sensitivity, and follow-up for core DLB features and lying/standing BP are musts.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: label and primary code changed from MCI (G31.84) to mild dementia (G30.0). The labels appended by the old G31.84 entry ("mild cognitive impairment", "MCI", "amnestic mild cognitive impairment", "amnestic MCI", "prodromal alzheimer", "mild cognitive impairment due to alzheimer") are still in `accepted` and would credit an MCI answer; please re-run `apply_diagnosis_synonyms.py --prune --cases ALZ-EARLY-RM01` (plan 5.1). G30.0 also grants "posterior cortical atrophy" and "benson syndrome" to this amnestic case.
- Citation keys used: `[STRIVE_2013]`, `[ACMG_NSGC_2011]`, `[NICE_NG97]` (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- None needing Andrea. Decided: DLB is `low` rather than `moderate`. She has one possible core feature (mild fluctuations) and no indicative biomarker, so she does not meet probable DLB (McKeith 2017), and the Alzheimer CSF and storage-type profile support AD as primary. Lewy co-pathology is acknowledged in the differential and in a follow-up must.
- Decided: corrected the creatinine rather than the CKD stage, because the history, the drug check and the "stable" course all assume stage 2.

## Verification
Adversarial verifier, 24 Oct 2026. Checked every note row (0941bb75, b2c0d3cc, 2e39ab2d, 262248db, 9229c61a, 175f3c29): label and G30.0 (onset 61), IADL field true with the losses named, Fazekas 2 and the putaminal lacune in findings and impression, LDL statin must, donepezil check optional and last with correct pharmacology (amlodipine statement correct, pulse 72 matches the vitals), no literature output, no gadolinium. Checked the creatinine correction: CKD-EPI 2021 for creatinine 0.98 mg/dL, woman, 62 years gives 65 mL/min/1.73 m2, consistent with stable CKD stage 2. CSF ratio 385/8020 = 0.048. Both biomarker alternatives have case-authored outputs. The MCI synonym labels still in `accepted` are correctly left to CENTRAL.

Found and fixed:
- B, minor, `patient.neurological_exam.additional` and `clinical_assessment.findings[2]`: MoCA "attention (4/6)" cannot be right in this exam (digit span forward 6 and backward 3 both pass the MoCA items, and one serial-seven error still scores 3/3, so at most the letter-tapping point can be lost), and the orientation loss (wrong day of the week) was not counted, so the stated items did not add up to 20. Now attention 5/6 (letter-tapping errors) and orientation 5/6: recall 5 + visuospatial/executive 3 + attention 1 + orientation 1 = 10, 20/30.
- E, minor, `action-7-interpret-labs.expected_evidence`: "in an untreated hypertensive patient" was wrong (she takes amlodipine); now "in a hypertensive patient not taking a statin".
No other change. Both checks clean for the case; case guards pass.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium and Homocysteine` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'lasting power of attorney' (UK instrument) changed to 'durable power of attorney' in this US-setting case (1 place).
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.
- Normal values in `Magnesium and Homocysteine` varied (Magnesium 2.0 to 1.8, Homocysteine 10.2 to 11.1), all still within the case's reference ranges: the same numbers (magnesium 2.0, homocysteine 10.2, ESR 12, CRP 1.8) had been copied into up to 13 cases, a template artefact raised by the S01 worker; no text cites the changed values.
- Checks re-run after these additions: perfect_agent.py, case_io.py check and test_case_guards clean.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`--prune --conditions alzheimers_early`): removed mild cognitive impairment labels (MCI, amnestic MCI, prodromal alzheimer, MCI due to alzheimer); "posterior cortical atrophy" and "benson syndrome"; code G30.1 (onset before 65); code G30.8 (atypical presentations only). Now: codes ['G30.0', 'G30.9', 'F00']; labels after accepted[0]: ['alzheimer disease', "alzheimer's disease", 'alzheimers disease', 'alzheimer dementia', 'dementia due to alzheimer', 'early onset alzheimer'].
- Added follow-up `order_advanced_imaging` FDG_PET (trigger `order_fdg_pet`, no criterion), after the amyloid-status follow-ups: a case-specific Alzheimer-type metabolic report concordant with the MRI and stage. Before, an FDG order returned the library's normal scan, contradicting the case (summary Q4). Probed: FDG and amyloid PET orders each return their own report, in either order.
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-7-interpret-labs]`.alternatives: was [CBC, CMP, TSH, B12, folate, homocysteine, magnesium, ESR, CRP]; now [CBC, CMP, TSH, B12, folate, homocysteine, magnesium, ESR, CRP, lipid_panel] | [CBC, CMP, TSH, B12, folate, homocysteine, magnesium, ESR, CRP].
- Decision: serve: new first alternative (old order kept as an alternative). The rationale measures lipids as vascular risk and a must starts a statin for LDL 148; the lipid panel was not returned.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.
