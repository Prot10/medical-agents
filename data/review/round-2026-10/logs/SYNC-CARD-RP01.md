# SYNC-CARD-RP01
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.clinical_history.medications`, `patient.history_present_illness`, `social_history.living_situation` | The HPI says magnesium sulfate was started at the referring hospital and the drug review treats it as running, but it was not in the medication list; breastfeeding (needed for the beta-blocker must, and stated in the monitoring report) was never documented, and she was "preparing a bottle". | FIXED: magnesium sulfate 4 g load then 1 g/h added; "bottle of expressed breast milk"; breastfeeding recorded. |
| B | minor | `initial_tool_outputs.labs` | Magnesium 2.8 mg/dL is implausibly low on a loading dose plus infusion and sat inside the BMP panel; troponin named "high sensitivity" with a conventional ng/mL range; summary lines carried diagnoses ("iron deficiency anemia", "exogenous magnesium sulfate", "likely residual gestational"). | FIXED: magnesium 4.4 mg/dL in its own panel; "Troponin I"; factual summary and pattern-level interpretation. |
| D | minor | `initial_tool_outputs.ecg.findings`, `intervals` | Interpretive findings ("could represent a normal female variant or ... RV pathology", "may warrant further evaluation"); QTc 452 called borderline prolonged (normal for a woman). | FIXED: categorical findings (V1-V3 T-wave inversion without RBBB, possible epsilon wave, LBBB/inferior-axis PVCs); plain intervals. ECG expected_evidence without the "ARVC pattern" verdict. |
| B | major | `action-4-order-cardiac-monitoring`, `followup_outputs[1]`, `fallback_tool_outputs.cardiac_monitoring` | Criterion pinned `holter_24h` while labelled telemetry (plan E); PVC burden 5.6% inconsistent with 4,832 PVCs at 78 bpm average (4.3%); "patient diary" in an admitted patient; fallback null (library normal recording). | FIXED: alternatives telemetry, holter_24h, holter_48h; output "Inpatient telemetry, 24 h", burden 4.3%, timed symptomatic runs reported to the nurse, heart-rate min/max; same recording as the case fallback; trigger `request_telemetry_holter_monitoring`. |
| C | minor | `followup_outputs[0]` (TTE) | No echo_type, LA, wall thickness, RVOT size or PASP (plan G). | FIXED: echo_type TTE; RV basal 43 mm, RVOT PLAX 31 mm, LV wall 8 mm, LA 32 mm, PASP 24 mmHg, no mass; numbered impression. |
| C | minor | `followup_outputs[2]` (CMR) | Native T1 of the thin RV free wall reported as a value (not reliably measurable); impression otherwise sound. | FIXED: RV T1 value removed; findings restructured (dyskinesia, fat, LGE, volumes); impression kept in substance. |
| C | major | `action-2-interpret-labs` | Pinned CBC, BMP, Mg, troponin, BNP, urinalysis; expected_evidence was policy text. | FIXED (plan C): `panels: [BMP, magnesium, urinalysis]`; rationale (arrhythmia electrolytes, infusion level, pre-eclampsia exclusion); expected_evidence from the values. |
| C | major | `sequence_constraints` | Hard labs-before-monitoring (unsafe order). | FIXED: deleted; soft ECG before TTE and before monitoring; hard TTE before exercise test. |
| C | minor | `action-6-order-specialized-test` | Exercise test recommended. | FIXED (plan): optional; rationale notes telemetry already captured NSVT and testing 10 days after caesarean section can be deferred. Report rewritten in test voice. |
| C | major | `action-7-check-drug-interactions`, `followup_outputs[4..6]`, `initial_tool_outputs.drug_interactions`, `fallback_tool_outputs.drug_interactions` | Required with no drug; single magnesium report speculated that magnesium "may mask arrhythmia" and quoted Mg 2.8. | FIXED (plan B): recommended, alternatives metoprolol and propranolol, each reviewed for lactation (LactMed) and the actual list; magnesium sulfate follow-up rewritten (level 4.4, toxicity thresholds, reflex monitoring); medication-list review in initial and fallback. |
| C | major | `action-8-search-medical-literature`, literature follow-ups | Required and in the stop rule; the eclampsia follow-up cited invented sources (a JACC 2021 case series of 14 women, a Heart Rhythm 2022 systematic review). | FIXED: optional, canonical rationale; eclampsia follow-up deleted; one follow-up with the 2010 Task Force Criteria and ESC 2022 content, last. |
| A | minor | `stop_rule`, `citations`, `rationale` | Literature and drug check in the stop rule, `max_additional_actions: 0`; "§" and duplicate Locati citations; rationale equal to label. | FIXED: required list = ECG, labs, TTE, telemetry, CMR; 3; keys only (Locati dropped: it concerns prolonged external monitoring); real rationales. |
| C | major | `ground_truth.assessment` | Musts were "CMR for ARVC" (a scored test), "EP consult for ICD", "Exclude eclampsia, PE and PPCM"; no exercise restriction, magnesium stop, contraception or driving advice; "Do not call `order_specialized_test`" engineering text; tilt prohibition (a test). | FIXED: musts are definite ARVC by 2010 TFC (two major criteria), monitored bed with defibrillator, stop magnesium (eclampsia excluded), ICD before discharge (ESC 2022), metoprolol or propranolol (LactMed), lifelong restriction of competitive and endurance exercise, genetic counselling and cascade screening starting with the symptomatic sister, contraception and pregnancy counselling, driving. Prohibitions: eclampsia/epilepsy and antiseizure drugs, discharge before ICD, atenolol/nadolol/sotalol in breastfeeding, return to endurance exercise. |
| C | major | `avoided_actions` | No EEG or tilt penalty; brain MRI rationale contradicted itself ("appropriate during initial postpartum work-up"). | FIXED: EEG and tilt waste added; MRI, CT and CSF rationales name ARVC and the excluding data (normal BP, no proteinuria, normal referring CT). |
| C | major | `ground_truth.differential` | Eclampsia and PPCM left high, PE and channelopathy moderate after a work-up that excludes them; PE argued from tests not on the pathway; idiopathic RVOT VT, the classic ARVC mimic, missing. | FIXED: all alternatives low with the excluding results (BP and urine; LVEF 58-60% and BNP 89; SpO2, PASP and symptomatic NSVT; QTc 452 and structural RV disease); RVOT VT added as low. |
| L | minor | `ground_truth.red_herrings` | Red herring 1 cited the off-pathway EEG; red herring 0 cited MRI; data_points paraphrased. | FIXED: data_points quoted from the chief complaint and HPI; interpretations cite BP, urine, telemetry and CMR. |
| C | minor | `ground_truth.key_clinical_evidence`, `metadata.difficulty_description`, `difficulty_rationale` | Generic statements; description relied on the normal EEG and "follow-up Holter". | FIXED: rewritten from the pathway results. |
| E | minor | `initial_tool_outputs.eeg.background.sleep_features` | Sleep spindles described "in drowsiness". | FIXED: "in drowsiness and light sleep". |

## Changes, in one paragraph a physician can read before re-reviewing

The 29-year-old woman 10 days after caesarean section, referred as "postpartum seizures, rule out eclampsia", now has five required steps: ECG (V1-V3 T-wave inversion without RBBB, possible epsilon wave), electrolytes, magnesium and urinalysis (magnesium 4.4 mg/dL on the infusion now recorded in her medication list; urine protein-to-creatinine 0.18), TTE, inpatient telemetry (Holter accepted) and cardiac MRI. Telemetry now reports a consistent PVC burden (4,832, 4.3%) and two symptomatic NSVT runs; the MRI meets the major imaging criterion (RVEDVI 112 mL/m2, RVEF 39%, regional dyskinesia), so with the ECG the 2010 Task Force diagnosis is definite. The exercise test and literature lookup are optional; the drug review is recommended and names metoprolol or propranolol for a breastfeeding mother. EEG, tilt, brain MRI, head CT and CSF are waste. The musts are: definite ARVC rather than eclampsia or epilepsy, monitored bed, stop magnesium, ICD before discharge, breastfeeding-compatible beta-blocker, exercise restriction, genetic counselling and cascade screening (sister with palpitations), contraception and pregnancy counselling, driving. Eclampsia, peripartum cardiomyopathy, PE, channelopathy and epilepsy are now low, and idiopathic RVOT VT is added as low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: `accepted` still carries the generic "cardiac syncope"; not hand-edited.
- Plan C2: no cardiomyopathy genetic panel exists, so genetic testing is a must only.

## Open questions for Andrea (judgment calls you could not settle)

None. Decided here: the exercise test follow-up is kept (optional criterion, protected by a hard TTE-first constraint) although it was performed 10 days after surgery; its rationale says it can be deferred. Driving advice uses the 3-month interval after an ICD for an arrhythmic event (ESC 2018).

## Verification

Adversarial verification, 24 Oct 2026 (diff against fa1d22e6; the batch-4 checkpoint commit holds the worker's edit).

Checked: no reviewer notes for SYNC-CARD. 2010 Task Force arithmetic: T-wave inversion V1-V3 without RBBB at age 29 is a major repolarisation criterion; regional RV dyskinesia with RVEDVI 112 mL/m2 (female threshold 100) and RVEF 39% (threshold 40) is a major imaging criterion, so "definite" is correct; the possible epsilon wave is not counted. Telemetry PVC burden (4,832 at 78 bpm over 24 h = 4.3%) and CMR volumes are consistent. Magnesium 4.4 mg/dL is plausible on a 4 g load plus 1 g/h. LactMed facts in musts and prohibition (metoprolol and propranolol acceptable; atenolol, nadolol and sotalol avoided) are correct; ICD "should be considered" after arrhythmic syncope in ARVC (ESC 2022) matches the must. Labs pin BMP, magnesium and urinalysis (plan C); exercise test optional with hard TTE-first constraint; drug check recommended with metoprolol and propranolol; differential all low with excluding results present in the stored outputs (BP, UPCR 0.18, platelets and liver enzymes, LVEF, BNP 89, PASP 24). Red herrings quote the chief complaint and HPI verbatim. Guards pass.

Found and fixed (timeline, dim B, major):
- The worker's added "magnesium started at the referring hospital about 5 hours ago" could not coexist with "two episodes ... over the past 6 hours" (first at 10:00, second at 15:30, magnesium started only after the second) or with the exam "approximately 40 minutes after the most recent event", which left no time for EMS, the referring hospital work-up, CT and transfer. Now: episodes "today" (`patient.history_present_illness`), magnesium "about 3 hours ago" (`patient.clinical_history.medications[4].indication`), exam "approximately 4 hours after the most recent event" (`patient.neurological_exam.mental_status`). The 24 h telemetry times (03:22, 11:40, 16:05 of the following day) remain consistent.

perfect_agent.py SYNC-CARD-RP01 -v: ok. case_io.py check: clean for this case.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).
- Literature follow-up trigger `search_arvc_diagnosis_management` renamed to `search_arvc_arrhythmogenic_right_ventricular_cardiomyopathy`. Why: the old trigger's meaningful tokens were generic (management, guidelines, diagnosis, syncope, literature), so a generic query hit the disease-specific report; the new tokens are the condition names, so only a query naming the condition reaches it.

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.
