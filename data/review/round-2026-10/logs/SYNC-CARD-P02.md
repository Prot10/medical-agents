# SYNC-CARD-P02
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for SYNC-CARD) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | followup_outputs[TTE] chambers / findings / impression | Valsalva LVOT gradient 62 mmHg (already obstructive, so exercise echo was not indicated) and a lab-style "Abnormal values: ..." impression; numbers disagreed with the exercise echo (rest 18 vs 38 mmHg, septum 21 vs 19 mm, LA 41 vs 43 mm, LVEF 60 vs 68%) | FIXED (plan P02/G): full TTE report in echo voice, `echo_type` TTE, LVEF 65% biplane, septum 21 mm / posterior wall 12 mm, LVEDD 42 mm, LA 41 mm, TAPSE 22 mm, PASP 32 mmHg, gradient 24 mmHg rest / 38 mmHg Valsalva, SAM, MR mild to moderate; exercise echo aligned (rest 24 mmHg, LA 41 mm, septum 21 mm, LVEF 65%) and peak 96 mmHg kept |
| C | minor | followup_outputs[exercise echo, exercise stress test] | Peak HR 148 called "85% of age-predicted maximum" (220-55 = 165, so 90%) | FIXED in both reports |
| D | minor | followup_outputs[exercise stress test].impression | Teaching sentence "Electrocardiographic and haemodynamic report only, an outflow-tract gradient requires simultaneous imaging" | FIXED: deleted; numbered impression |
| B | major | followup_outputs[monitoring] | 24 h Holter under a telemetry label; "brisk walking" timestamps; PVC 1,847/24 h called 2.1% (arithmetic gives 1.7%) | FIXED (plan E): one output "Inpatient telemetry, 48 h", `monitor_type` telemetry, trigger `request_telemetry_holter_monitoring`, NSVT during supervised stair walking, 4,476 PVCs in 48 h = 2.1%; same report stored as `fallback_tool_outputs.cardiac_monitoring` |
| B | major | patient.clinical_history.medications | HPI says levetiracetam 500 mg twice daily was prescribed and two doses taken, but the medication list lacked it (same class as plan C for M02) | FIXED: added; must to stop it; prohibition rewritten |
| B | minor | patient.clinical_history.social_history.occupation | "social worker" while the HPI and exercise history make him a high school basketball coach | FIXED: "High school basketball coach" |
| D | major | initial_tool_outputs.drug_interactions | Empty "general" block whose summary was the criterion key | FIXED (plan B): replaced by a real medication-list review; per-drug follow-ups `check_amlodipine_interactions`, `check_losartan_interactions`; the same review stored as fallback |
| A | major | ground_truth.action_criteria[drug] | No `drug` argument, recommended | FIXED: required, alternatives {drug: amlodipine}, {drug: losartan} (plan B tier table) |
| C | major | followup_outputs[tilt] | Tilt with isoproterenol text in obstructive HCM | FIXED: follow-up deleted; avoided action `avoid-harm-3-tilt-table` (harm) |
| C | major | ground_truth.action_criteria[literature], stop_rule | Literature required and in the stop rule; output cited two unverifiable papers (Heart 2020, Epilepsy & Behavior 2019) | FIXED (plan A): optional, out of the stop rule, follow-up rewritten with ESC 2023 cardiomyopathies, O'Mahony 2014 and ESC 2018 content, placed last |
| D | major | initial_tool_outputs.literature_search, followup_outputs[literature].trigger_action | With no initial literature output the MockServer serves the only literature follow-up to ANY query, so the HCM guideline text (naming the diagnosis) answered every search; the trigger `search_literature_hcm_syncope` also matched any query containing "syncope" | FIXED: neutral ESC 2018 / ACC-AHA-HRS 2017 syncope-evaluation answer stored as `initial_tool_outputs.literature_search.general`; HCM follow-up trigger renamed `search_literature_hypertrophic_cardiomyopathy_hcm`, so only a query naming HCM receives it (probed) |
| A | minor | ground_truth.action_criteria[labs] | CBC+BMP+Mg+troponin pinned | FIXED (plan C): recommended, `panels: [BMP]`; troponin and Mg accepted in the label |
| A | major | ground_truth.action_criteria[monitoring] | Pinned holter_24h while labelled telemetry | FIXED: alternatives telemetry, holter_24h, holter_48h |
| E | minor | all criteria `rationale` | Equal to `label`; free-text "ESC 2018 §x" and "Locati 2014" in citations | FIXED: real rationales naming the guideline; citations reduced to keys ([ESC_2018]); Locati dropped from the telemetry criterion (it concerns prolonged external monitoring, not in-hospital telemetry) |
| A | major | ground_truth.sequence_constraints | Empty | FIXED: soft ECG before TTE, soft ECG before monitoring, hard TTE before exercise echo |
| A | minor | ground_truth.stop_rule | Listed literature; max_additional_actions 0 | FIXED: every required criterion (ECG, TTE, monitoring, CMR, exercise echo, drug check), max 3 |
| E | minor | ground_truth.assessment.prohibited_recommendations | "Do not call `order_specialized_test` ..." engineering text and a tilt prohibition (a test, not management) | FIXED: deleted (tilt is now an avoided action) |
| C | major | ground_truth.assessment.required_recommendations | CMR must restated a scored test; no vasodilator withdrawal, no Risk-SCD, no driving advice, no levetiracetam withdrawal | FIXED: musts rewritten (see Changes) |
| C | major | ground_truth.avoided_actions | No EEG, brain MRI or tilt avoidance | FIXED: EEG waste, brain MRI waste, tilt harm; CT and CSF reasons name the diagnosis |
| C | major | ground_truth.differential | ARVC high, CPVT and coronary moderate after the work-up excludes them; hypertensive heart disease (the obvious LVH mimic in a man with 10 years of hypertension) missing | FIXED: all low with the excluding result; hypertensive heart disease added (low) |
| D | minor | ground_truth.red_herrings | Red herring on the EEG (not a criterion tool, plan L); data_points not quoted from the field | FIXED: EEG herring deleted; HPI and ECG data_points quoted verbatim; urgent-care seizure label added as a herring |
| B | minor | followup_outputs[CMR] | Native T1 1120 ms identical to RS02/RS03 (plan M); no RV statement although CMR is the ARVC discriminator | FIXED: T1 1095 ms; RV finding added (normal RVEF 58%, no LGE) |
| E | minor | metadata.clinical_pearls[2], difficulty_rationale | "nearly pathognomonic" overstated (MVP murmur also increases); stale counts | FIXED |

## Changes, in one paragraph a physician can read before re-reviewing
55-year-old basketball coach with two exertional collapses with brief jerks, family history of sudden death, treated at urgent care with levetiracetam. The TTE now shows asymmetric septal hypertrophy 21 mm with SAM and a gradient of 24 mmHg at rest and 38 mmHg with Valsalva, so exercise echocardiography is the indicated provocation (ESC 2023 Class I) and shows 96 mmHg with a hypotensive BP response and NSVT at presyncope; a hard constraint puts the TTE before it. Monitoring is 48 h inpatient telemetry (Holter accepted) with recurrent NSVT; CMR shows 23 mm septum, 12% LGE and a normal RV. The drug review is required and scored on amlodipine or losartan (both vasodilators to stop); bare drug calls get a medication-list review. Literature is optional. Tilt is a harmful avoided action; EEG and brain MRI are waste. Musts: monitored admission; stop amlodipine and losartan and start a non-vasodilating beta-blocker (verapamil or diltiazem if not tolerated); HCM Risk-SCD (about 14% with the stored values, above 6%) with ICD to be considered (ESC 2023 IIa); avoid dehydration; stop levetiracetam; septal reduction discussion if symptoms persist; exercise restriction; genetic counselling and family screening; driving restriction. Levetiracetam was added to the medication list and the occupation corrected. The differential is updated to the results.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan B step 4 does not work as written: with no `initial_tool_outputs.drug_interactions`, the MockServer serves the FIRST drug follow-up (tier 2 of `resolve_followup`) to any unnamed drug, so a metoprolol check returned the amlodipine review and the case-level fallback is never reached. I stored the medication-list review as `initial_tool_outputs.drug_interactions` (and as the fallback); drug-named calls still reach their own follow-up. The lead should apply the same in every case with per-drug follow-ups.
- Same mechanism for literature (plan A step 2): deleting every initial literature block makes the single stored literature follow-up the answer to every query, which hands the named diagnosis to any search. I kept a neutral initial literature answer (general syncope evaluation, no diagnosis) and gave the disease-specific follow-up a trigger that names the disease. Recommend the same condition-wide.
- Diagnosis synonyms: "cardiac syncope" accepted (plan C1, generic label).

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the whole final case against the plan (P02 bullets, sections A-O) and the log.
- Confirmed: Valsalva gradient 38 mmHg (below 50) in TTE chambers, findings, impression and the criterion; exercise echo 96 mmHg with hard TTE-before-exercise-echo; drug criterion required with amlodipine and losartan; tilt deleted and harm; literature optional, last, out of the stop rule; stop rule = the six required criteria, max 3; telemetry arithmetic (4,476 / about 213,000 beats = 2.1%); levetiracetam in the list; occupation fixed. HCM Risk-SCD recomputed from the stored values (age 55, MWT 21 mm, LA 41 mm, gradient 38 mmHg, NSVT, syncope): 8.8% without and 13.6% with the family history, so the must's "above 6%, ICD to be considered (ESC 2023 IIa)" holds either way. The worker's CENTRAL claim about tier 2 of `resolve_followup` (no initial output: the first stored follow-up answers any call) is correct per `followup_matcher.py`.
- Found and fixed:
  1. D, minor: TTE impression ended "Consider exercise echocardiography to assess provocable obstruction", a management pointer to a required criterion. Deleted.
  2. D, major: the medication-list review (initial and fallback drug output, served for any drug at any time, also before the echo) said "in a patient whose echocardiogram shows dynamic LVOT obstruction". Summary rewritten conditionally ("relevant if dynamic LVOT obstruction is present").
  3. B, minor: the exercise echo said "semi-supine bicycle, then upright post-exercise imaging" with "9 min, 7.2 METs". A bicycle test is not reported in METs from minutes, and 9 min of Bruce is about 10 METs. Changed to an upright treadmill (Bruce) test of 6 min 30 s, 7.2 METs, imaging at rest and immediately after exercise.
  4. M (template carry-over), minor: the stand-alone exercise ECG follow-up (`exercise_stress_test`, off-pathway) copied every number of the exercise echo (duration, METs, HR 148, BP 140/84 to 118/72, NSVT 8 beats at 192 bpm, 14 PVCs). Gave it its own values (6 min 10 s, 7.0 METs, HR 145 = 88% of 165, BP 142/86 to 122/74, NSVT 7 beats at 188 bpm, 11 PVCs).
  5. B, minor: the lab criterion's expected_evidence said "Normal ... magnesium" while the panel flags magnesium 2.3 mg/dL high. Rewritten to "Potassium 4.0 and troponin I normal, magnesium not low".
  6. C, minor: metadata.clinical_pearls[4] said the risk profile "warrants ICD implantation"; ESC 2023 makes it IIa (should be considered). Reworded.
- Re-ran `perfect_agent.py SYNC-CARD-P02 -v` (ok) and `case_io.py check` (clean for this case).

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: HCM labels kept (the disease is named; obstruction is scored by the required exercise echo), plus "obstructive hypertrophic cardiomyopathy".
- "ESC/EACTS 2021" renamed "ESC/EACTS 2025" (2025 ESC/EACTS valvular guideline, Praz 2025, supersedes 2021): `.ground_truth.sequence_constraints[2].reason`.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-3-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2023_Cardiomyopathy]']; action-5-order-advanced-imaging citations ['[ESC_2018]'] -> ['[ESC_2023_Cardiomyopathy]']; action-6-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2023_Cardiomyopathy]']; action-7-check-drug-interactions citations ['[ESC_2018]'] -> ['[ESC_2023_Cardiomyopathy]']; avoid-waste-1-order-ct-scan citations ['[ESC_2018]'] -> ['[ESC_2018]', '[NICE_NG232]']; action-3-order-echocardiogram->action-6-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2023_Cardiomyopathy]', '[ESC_EACTS_2025_VHD]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-P02` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure report, supine values = the presenting vitals; Systolic fall of 12 mmHg at 1 minute of active standing, below the threshold for orthostatic hypotension (20/10 mmHg); no excessive heart rate rise. |
| `ground_truth.action_criteria[action-orthostatic-blood-pressure]` | added, recommended, after the ECG criterion [ESC_2018] (decisions CENTRAL 1: orthostatic BP in every initial evaluation) |
| `followup_outputs[9] (`request_cardiomyopathy_gene_panel`)` | added: genetic_panel:cardiomyopathy report. Heterozygous pathogenic MYBPC3 variant c.1504C>T (p.Arg502Trp) |
| `ground_truth.action_criteria[action-genetic-panel]` | added, recommended [ESC_2023_Cardiomyopathy]; the assessment must on genetic counselling and testing is unchanged |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-2-interpret-labs]`.alternatives: was [BMP]; now [BMP, magnesium, troponin] | [BMP].
- Decision: serve: new first alternative (old order kept as an alternative). The label accepts troponin and magnesium with the electrolytes and the evidence reads both.
- Scoring: none (recommended criterion: coverage unchanged, not in the cost reference).

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 80, ECOG 1 (fallback_tool_outputs.clinical_assessment). Why: rule 2: the library reports Karnofsky 100 with no complaints in a man with progressive exertional dyspnoea and two exertional syncopes.
- `order_specialized_test {test_type: tilt_table}`: not performed, deferred by the clinical team (fallback_tool_outputs.specialized_test). Why: the library answers with a generic normal tilt (118/74 mmHg, 68 bpm) in a patient with dynamic LVOT obstruction, in whom tilt testing is avoided; the order is answered as deferred.
- `order_echocardiogram {echo_type: TEE}`: asymmetric septal hypertrophy, SAM with posteriorly directed MR, no thrombus (fallback_tool_outputs.echo). Why: rule 3: the stored TTE shows asymmetric septal hypertrophy 21 mm with SAM; the library TEE reports a normal heart.
- `order_echocardiogram {echo_type: bubble_study}`: asymmetric septal hypertrophy with SAM, no right-to-left shunt (followup_outputs[10] request_bubble_study). Why: rule 3: the stored TTE shows hypertrophic septum with SAM; the library reports a normal heart.
- `order_specialized_test {test_type: polysomnography}`: moderate obstructive sleep apnoea, AHI 22/h (followup_outputs[11] request_polysomnography). Why: rule 2: known obstructive sleep apnoea on nightly CPAP; the library reports AHI 2.1/h.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
