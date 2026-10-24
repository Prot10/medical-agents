# HEP-ENC-M04
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| e18c72da-7bca-4bce-b650-93777dd208c9 | FIXED | The `interpret_labs` follow-up `assess_lille_score` (day-7 bilirubin 11.2, Lille 0.28: data from the future) deleted. The day-7 reassessment is now a must: "Calculate the Lille score on day 7 of prednisolone and stop it if the score is 0.45 or more (Louvet 2007)" (`ground_truth.assessment.required_recommendations[7]`). The steroid red herring (`red_herrings[0]`) now points to the day-7 Lille score instead of an already-known result. The other treatment-response follow-ups were deleted with it (`request_thiamine_empiric`, `request_nutritional_support` with post-repletion electrolytes): ruling 4. |
| cbd4a868-9a0a-4d05-bf35-562b65ffdd93 | FIXED | The serial ammonia follow-up (`request_lactulose_rifaximin`, 82 to 54 µmol/L at 48 h) deleted; one admission ammonia (82 µmol/L, range 11-51) stays in `initial_tool_outputs.labs.panels.LFTs`. K-AMM pearl added as `key_clinical_evidence[1]`; the core-lab expected evidence says ammonia supports but does not grade HE. |
| 0fffd88b-115e-4978-a76e-04c353874861 | FIXED | MRI (`initial_tool_outputs.mri`): the "No mass, midline shift or herniation, the finding the lumbar puncture is gated on" line deleted; `findings` filled (no restricted diffusion or hemorrhage; no T2/FLAIR change in the medial thalami, mammillary bodies, periaqueductal gray or tectal plate, no mammillary enhancement; mild bilateral pallidal T1 hyperintensity; mild atrophy) with a numbered impression; technique line added. CT (`initial_tool_outputs.ct`): canonical normal finding plus mild atrophy; "restricted diffusion" removed from the impression. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.history_present_illness`, `past_medical_history[0]`, `neurological_exam.additional` | Timeline impossible: admitted 5 days ago yet last drink 48 hours ago (drinking on day 3 of an inpatient stay), with withdrawal now. | FIXED: admitted 2 days ago a few hours after his last drink, prednisolone started on admission; withdrawal at 48 h fits. The Lille must keeps day 7. |
| C | major | `past_medical_history[0]`, `history_present_illness` | Maddrey discriminant function 38 not derivable from bilirubin 14.8 mg/dL and INR 2.4 (which give about 75 to 90). | FIXED: prothrombin time 25.0 s (control 12.0 s) added to a new `Coagulation` panel with the INR; Maddrey 75 on admission in the history; derivation in `key_clinical_evidence[2]`. |
| D | major | `patient.history_present_illness` | "CT head is without acute changes" stated a scored study (C13). | FIXED: removed. |
| C | major | `ground_truth.diagnosis.accepted[0]` | Grade "II-III" while the exam supports grade II (disoriented to time only, oriented to person and place, asterixis); "glucose 62-64" built on a duplicate analyte; "critical" overstated for glucose 64. | FIXED: "West Haven grade II"; "hypoglycemia (glucose 64 mg/dL) as co-precipitants"; underlying cirrhosis named. No score added (plan M04). |
| A | minor | `action-3-search-medical-literature`, `initial_tool_outputs.literature_search` | Literature output echoed the expected evidence (C4). | FIXED: criterion deleted, output null. |
| C | major | `action-4-check-drug-interactions`, `followup_outputs` (`check_alcohol_withdrawal_he_interaction`) | Required check with template expected evidence about lactulose and rifaximin; the output dosed lorazepam and phenobarbital (management) and advised against "withholding seizure prophylaxis" (C5). | FIXED: recommended (plan); alternatives name lorazepam, oxazepam, chlordiazepoxide, diazepam, prednisolone; one output `check_lorazepam_oxazepam_chlordiazepoxide_prednisolone`, placed last, with the real content (accumulating benzodiazepines to avoid, lorazepam or oxazepam preferred, no relevant interaction with prednisolone, phenobarbital caution). |
| B | major | `initial_tool_outputs.labs` | "Exclusion studies" block (lactate without a value); template TSH 2.1 and zinc 82; glucose reported twice (64 and 62); no creatinine and no CRP; thiamine labelled "serum" with the whole-blood TDP range; summary missed most flagged values (C9). | FIXED: lactate 1.8 mmol/L, CRP 48 mg/L, BUN 7 and creatinine 0.9 mg/dL added; TSH 1.6, zinc 66; single glucose 64 (BMP); thiamine relabelled "whole blood thiamine pyrophosphate" in a `Vitamins` panel; summary and interpretation list every flagged value. Ethanol "not detected" kept (last drink 48 h ago). |
| A | minor | `action-1-interpret-labs` | Ten named panels demanded. | FIXED: two-alternative core with `thiamine_B1` (plan Labs+). |
| C | major | `action-8`, `action-9-order-microbiology` | Arguments carried `before_antimicrobials` and test lists; generic expected evidence; blocks said "No organism isolated to date" (C7). | FIXED: required (T 38.4, WBC 18.6), specimen-only arguments, canonical labels, case results ("no growth at 48 hours"; "no pyuria"). `collected_before_antimicrobials` true, since the musts now start empirical antibiotics after cultures. |
| C | major | `ground_truth.assessment.required_recommendations` | Lactulose 2-4 stools (C3); rifaximin in a first episode; withdrawal must preferred phenobarbital, clonidine or gabapentin, contradicting the prohibition; no infection plan in a febrile, tachycardic patient on prednisolone; no nutrition plan in a malnourished patient. | FIXED: thiamine 200 mg IV three times daily before glucose (EFNS 2010), glucose after thiamine with monitoring, potassium, magnesium and phosphorus replacement with refeeding watch, MUST-LACT, symptom-triggered lorazepam or oxazepam in a monitored bed, infection must (cultures, chest radiograph, empirical antibiotics reviewed at 48 h), culture timing, Lille day 7, nutrition without protein restriction, alcohol use disorder treatment. Rifaximin dropped (first episode). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Two contradictory benzodiazepine lines (haloperidol for agitation; scheduled benzodiazepines "at moderate CIWA") (C12); generic LP prohibition with no LP. | FIXED: PROHIB-BZD-WD replaces both; opioid line with acetaminophen up to 2 g per day; LP line deleted; thiamine-before-glucose line kept; no protein restriction added. |
| C | minor | `ground_truth.differential` | Hypoglycemia (64 mg/dL) moderate as an alternative; sepsis entry without the culture results; Wernicke key features rested only on the level. | FIXED: hypoglycemia low as sole cause; sepsis moderate with negative cultures and the remaining chest-source question; Wernicke high with Caine criteria and MRI insensitivity; withdrawal marked concurrent. |
| C | minor | `ground_truth.red_herrings` | The central trap of the case (attributing everything to withdrawal and giving scheduled long-acting benzodiazepines) was not encoded. | FIXED: red herring added on `patient.neurological_exam.mental_status`. |
| B | minor | `patient.neurological_exam.additional` | "Low BMI 22.8" (a normal BMI); ascites status unstated though it decides the paracentesis. | FIXED: "BMI 22.8, but temporal wasting and muscle loss indicate malnutrition"; "without shifting dullness". |
| E | minor | criteria, citations, pearls, metadata | Rationale = label; free-text citations; "(AASLD 2014)"; metadata described a required CT and literature search. | FIXED: one-sentence rationales with keys; K-AMM and score pearl; Wernicke pearl; metadata updated. EEG impression closes with "Clinical correlation recommended." |

## Changes, in one paragraph a physician can read before re-reviewing

The policy requires the core labs with thiamine, blood and urine cultures before antibiotics (he is febrile at 38.4 °C with WBC 18.6 on prednisolone) and a brain MRI for the Wernicke question; EEG and a benzodiazepine drug check are recommended, CT optional. The timeline now holds: he was admitted 2 days ago, hours after his last drink, and started prednisolone on admission, so withdrawal 48 hours after the last drink is in its usual window; the HPI no longer gives the CT result. The day-7 Lille panel, the serial ammonia, the post-thiamine glucose and the post-repletion electrolytes are gone, as is the literature search. Labs gain creatinine 0.9, BUN 7, prothrombin time 25.0 s, CRP 48 and lactate 1.8, lose the duplicate glucose and the "Exclusion studies" block, and give case-specific TSH and zinc; the Maddrey score in the history (75) is now derivable from the printed values, and Child-Pugh C (12), MELD-Na 29 are in the pearls. The label reads West Haven grade II (the exam supports grade II, not III). MRI and CT have real findings; the MRI shows no Wernicke signal change (which does not exclude it) and bilateral pallidal T1 hyperintensity. Musts: thiamine 200 mg IV three times daily before glucose, glucose correction and monitoring, potassium, magnesium and phosphorus replacement, lactulose to 2-3 stools, symptom-triggered lorazepam or oxazepam in a monitored bed, infection screen with chest radiograph and empirical antibiotics reviewed at 48 hours, Lille on day 7, nutrition without protein restriction, alcohol use disorder treatment. Prohibitions: scheduled or long-acting benzodiazepines, opioids, glucose before thiamine, protein restriction.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_ALD_2018]`, `[EFNS_Wernicke_2010]`.
- `accepted[0]` changed (grade II-III to II per plan 1.2; duplicate glucose range removed); ICD codes and synonyms unchanged.
- The infection must names a chest radiograph, which no tool can order (plan CENTRAL 5, `chest_xray` in `order_body_imaging`).

## Open questions for Andrea (judgment calls you could not settle)

- Timeline: I moved the admission from 5 to 2 days ago rather than moving the last drink to 5 days ago, because withdrawal delirium starting 5 days after the last drink would be atypical and the case is built on concurrent withdrawal. The plan header's "day 5" is therefore now "day 2" of prednisolone.
- Thiamine dose follows the plan (EFNS 2010, 200 mg IV three times daily); the old must gave 500 mg three times daily (Royal College of Physicians practice), which is also widely used.
- Empirical antibiotics: the must starts them after cultures because fever, tachycardia and leukocytosis on prednisolone cannot yet be attributed to the hepatitis or to withdrawal; cultures are negative at 48 hours, so the antibiotics would then be reviewed. A reviewer may prefer cultures and observation without antibiotics.
- The drug check is recommended per plan; ruling 6 would also allow required, since the choice of benzodiazepine in liver failure is a hepatic-dosing issue that changes management.
- The bilateral pallidal T1 hyperintensity on MRI is a new, typical cirrhosis finding added to give the MRI real findings; it does not change the diagnosis.

## Verification

Checked (adversarial verifier, 23 Oct 2026): all three note ids (e18c72da, cbd4a868, 0fffd88b) are in the table and fixed in the file (no day-7 panel; Lille is a must; one admission ammonia; MRI and CT have findings, no "gated on" line, no "restricted diffusion" on CT). Recomputed: Maddrey 4.6 x (25.0 - 12.0) + 14.8 = 74.6, stated 75; Child-Pugh C 12 (bilirubin 14.8, albumin 2.0, INR 2.4, no ascites, grade II); MELD 26, MELD-Na 29. Timeline holds (admitted 2 days ago hours after the last drink; withdrawal at 48 h; prednisolone day 2, so the steroid-psychosis entry's "two days" agrees). No ascites (no shifting dullness), so no tap, per plan. Cultures required (38.4 °C, WBC 18.6) with antibiotics after cultures in the musts; thiamine 200 mg IV three times daily (EFNS 2010); prohibitions and musts on benzodiazepines agree (symptom-triggered lorazepam or oxazepam only).

Found: (1) `differential[0]` was "Alcohol withdrawal syndrome with delirium tremens" (high) while the label, red herring and musts describe moderate withdrawal (CIWA 12) as a concurrent co-precipitant; calling it delirium tremens overstates the label and blurs the case's own trap (attributing all the confusion to withdrawal). (2) `red_herrings[1].field_path` pointed at the whole BMP panel.

Changed: `differential[0]` is now "Alcohol withdrawal syndrome (concurrent)", ICD F10.230, likelihood high kept (it is present), key features state CIWA 12 as moderate withdrawal and progression to delirium tremens (48-96 h) as the risk to monitor. `red_herrings[1].field_path` is `initial_tool_outputs.labs.panels.BMP[6]` (glucose 64). `perfect_agent.py` and `case_io.py check` clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

- Leak guard (Andrea, 24 Oct 2026: any-query outputs must not repeat any criterion's expected evidence, including their own): `ground_truth.action_criteria[action-4-check-drug-interactions].expected_evidence` reworded as the conclusion a grader checks, in words not shared with the stored `check_drug_interactions` follow-up, whose report text is unchanged; clinical content unchanged.
- No transplant must added: the Lille must already sets the next decision while the response to prednisolone is pending (auditor flag, decided keep).

Checks: `perfect_agent.py` pass; `case_io.py check` schema and synonym guard OK, no test failure names this case; leak guard clean.

## Central vocabulary wired (24 Oct 2026)

`chest_xray` is now a core `order_body_imaging` study, so the chest radiograph named in the infection must is a scored action.
- New criterion `action-chest-xray` (recommended), `order_body_imaging {"study": "chest_xray"}`, placed after the urine culture; citations `[EASL_HE_2022]`, `[EASL_ALD_2018]`; expected evidence "No consolidation or effusion".
- New `followup_outputs[1]` `request_chest_xray` (region chest, modality xray): clear lungs, no effusion or pneumothorax, normal heart size; impression findings only. Placed after the urine culture, before the drug check.
- `assessment.required_recommendations[5]`: the radiograph is no longer listed as a step inside the must; antibiotics are reviewed at 48 hours "with the culture and chest radiograph results".
- `differential[3].key_features`: "a chest source is not yet excluded" replaced by the radiograph result; the entry stays moderate (occult infection on corticosteroids not excluded by early cultures).
- Re-run: `perfect_agent.py HEP-ENC-M04 -v` ok (action-chest-xray <- followup[1]); `case_io.py check` schema OK, synonym guard OK, no test failure names the case.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
