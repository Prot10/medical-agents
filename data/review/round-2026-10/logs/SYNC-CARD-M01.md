# SYNC-CARD-M01
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search`, `initial_tool_outputs.drug_interactions` | Both initial blocks repeated the expected_evidence of their criteria (plan A, B). | FIXED: literature block deleted; the empty "general" drug block replaced (see below). |
| C | major | `action-6-search-medical-literature` | Literature scored as a recommended work-up step (ruling 5). | FIXED: `optional`, canonical rationale, neutral expected_evidence; one guideline follow-up added last (`followup_outputs[8]`, ESC 2021 pacing and ESC 2018 syncope content, no patient conclusion). |
| E | major | `fallback_tool_outputs.literature_search`, `fallback_tool_outputs.drug_interactions.proposed` | "Not retrieved on this pathway" and "No new antiarrhythmic drug initiated on this pathway" pipeline text (plan H). | FIXED: literature fallback deleted (library answers); drug fallback rewritten. |
| C | minor | `action-5-check-drug-interactions` | No drug named; the stored output was an empty template. | FIXED: alternatives `{drug: hydrochlorothiazide}`, `{drug: clopidogrel}` (no rate-slowing or QT drug in the list; these are the two drugs whose review changes management). Follow-ups `check_hydrochlorothiazide` (thiazide K/Mg loss, ARB and metformin interactions, ACE-inhibitor angioedema note for losartan, no AV-nodal blockers before pacing) and `check_clopidogrel_aspirin` (DAPT and device-pocket haematoma; single antiplatelet usually enough > 12 months after PCI). `initial_tool_outputs.drug_interactions` and `fallback_tool_outputs.drug_interactions` both hold the same `medication_list_review`, so an unnamed drug gets the patient's real list review. |
| B | major | `initial_tool_outputs.labs.panels.CBC[2]` | Hb 12.8 g/dL with Hct 44.5% is impossible (plan C). | FIXED: Hct 38.4%, flagged low; summary and interpretation updated. |
| C | minor | `action-2-interpret-labs` | Pinned CBC and troponin that drive no decision. | FIXED: `panels: [BMP, magnesium]` (required: K 3.2 and Mg 1.7 on a thiazide). |
| C | major | `sequence_constraints[0]` | Hard labs-before-monitoring constraint (unsafe order, ESC 2018 Class I immediate monitoring). | FIXED: deleted; soft ECG before TTE and ECG before monitoring added. |
| A | minor | `stop_rule` | `max_additional_actions: 0`. | FIXED: 2; required list = the four required criteria. |
| B | major | `followup_outputs[1]`, `action-4-order-cardiac-monitoring` | Criterion pinned `holter_24h`, label said telemetry, output was a 48 h Holter (plan E). | FIXED: alternatives telemetry, holter_24h, holter_48h; output is "Inpatient telemetry, 48 h" with trigger `request_telemetry_holter_monitoring`; events now day-stamped, pauses stated as non-conducted P waves at a constant sinus rate, minimum HR 28 attributed to 3:1 conduction (a 5.8 s pause cannot give a rate of 28). `fallback_tool_outputs.cardiac_monitoring` set to the same recording. |
| B | minor | `followup_outputs[0]` (echo) | Echo numbers identical to M02 and M03 (LVEF 50%, IVS 1.3, LA 4.1); no echo_type, TAPSE, PASP or masses (plan M, G). | FIXED: own values consistent with prior LAD infarct, hypertension and the CMR (LVEF 47% biplane, IVS 1.4 cm, LVEDD 5.5 cm, LA 4.3 cm, LAVI 38, TAPSE 21 mm, PASP 31 mmHg, AV Vmax 1.7 m/s); numbered echo-voice impression. Echo expected_evidence updated. |
| D | minor | `initial_tool_outputs.ecg.interpretation` | Prognosis sentence ("significant risk of progression to complete heart block", plan O). | FIXED: categorical rhythm and conduction statement only. ECG expected_evidence rewritten without the em dash. |
| A | major | `followup_outputs` (interpret_labs `request_electrophysiology_study`) | EP study stored under interpret_labs (plan F). | FIXED: deleted. |
| C | major | `followup_outputs[5]` (tilt) | Isoproterenol provocation in ischaemic heart disease (plan J). | FIXED: rewritten as a negative 40-min passive tilt with no pharmacological provocation, rather than deleted, so a wasted tilt order gets this patient's bradycardic values instead of the library's HR 68 (see Open questions). Tilt avoided as waste. |
| B | minor | `followup_outputs[6]` (exercise) | `quantitative_data.rate` 88 contradicted a peak ventricular rate of 59; impression called 2:1 block "Mobitz type II pattern". | FIXED: quantitative data (protocol, rates, BP) and impression rewritten; findings kept. Exercise test avoided as waste (pacing indication established). |
| C | minor | `action-10-order-advanced-imaging` | CMR recommended "if EP and echo are inconclusive" at age 62 with a known ischaemic substrate. | FIXED: optional, rationale per ESC 2021 IIa (AV block under 60). Follow-up moved after monitoring. |
| C | major | `followup_outputs[2]` (CMR) | Patchy mid-wall basal septal LGE "at the level of the bundle of His" with the statement "no features of infiltrative cardiomyopathy or sarcoidosis": that LGE pattern in AV block is the typical sarcoid pattern and would oblige an FDG-PET work-up the case never resolves (same defect in M02). | FIXED: septal finding deleted; impression lists the LAD scar, LVH and no non-ischaemic enhancement; CMR expected_evidence rewritten. |
| H/E | minor | all `action_criteria[*].citations`, `rationale` | Free-text "ESC 2018 §x" and "Locati 2014" citations; rationale equal to label. | FIXED: keys only (`[ESC_2018]`; Locati dropped from the telemetry criterion because it concerns external prolonged monitoring); real rationales written. |
| C | major | `avoided_actions` | EEG, brain MRI, tilt and exercise test not penalised (plan J); CT rationale did not apply NICE NG232. | FIXED: waste entries for EEG, brain MRI, tilt_table, exercise_stress_test added, each naming the diagnosis; CT rationale rewritten (under 65, no anticoagulant, no head injury). |
| C | major | `ground_truth.assessment` | No pacing must (only "consult cardiology"), no disposition with pacing back-up; LP prohibition boilerplate; "further AV-nodal blockers" though he takes none. | FIXED: musts now diagnosis, monitored bed with transcutaneous pacing back-up, dual-chamber permanent pacemaker (ESC 2021 Class I), hold thiazide and replete K/Mg, convulsive syncope not epilepsy, driving (Group 1 one week after implant). Prohibitions: antiseizure drugs, discharge before pacing, starting AV-nodal/rate-slowing drugs, driving; LP deleted. |
| C | major | `ground_truth.differential` | VT high and SND moderate after a work-up that excludes both; seizure, vasovagal and orthostatic entries cited the off-pathway EEG and tilt. | FIXED: VT low (no VT in 48 h, LVEF 47%), SND low (pauses from non-conducted P waves, no sinus arrest); other entries cite history and telemetry only. |
| C | minor | `ground_truth.key_clinical_evidence` | "Class I indication ... pacemaker consideration"; "EP study and ICD candidacy should be addressed". | FIXED: rewritten from the pathway results; no ICD indication with LVEF 47% and no VT. |
| L | minor | `ground_truth.red_herrings[1]` | Red herring in the output of a non-criterion tool (initial EEG, plan L); red herring 0 cited the EEG. | FIXED: EEG red herring deleted; red herring 0 interpretation cites telemetry. |
| E | minor | `metadata.clinical_pearls`, `difficulty_rationale`, `fallback_tool_kinds` | "pathognomonic", "most common cause of seizure misdiagnosis"; rationale counted 5 required tools and the EEG red herring. | FIXED: wording tempered; rationale and fallback kinds updated. |

## Changes, in one paragraph a physician can read before re-reviewing

The 62-year-old man with trifascicular disease and paroxysmal Mobitz II now has four required steps: ECG, electrolytes and magnesium, TTE and immediate inpatient telemetry (telemetry first, Holter accepted), with soft constraints ECG before TTE and before monitoring and no labs-before-monitoring constraint. The telemetry report is a truthful 48 h inpatient recording: three Mobitz II episodes with 2:1 and 3:1 conduction, pauses of 5.8, 4.1 and 3.6 s from non-conducted P waves, one coinciding with near-syncope, no VT, no sinus arrest. The echo has its own values (LVEF 47%, anterior-apical hypokinesis, septum 1.4 cm). The haematocrit is corrected to 38.4%. The CMR keeps the LAD scar and LVH but no longer reports septal mid-wall enhancement, a sarcoid-type pattern the case never worked up. The EP study stored as a lab panel is gone; CMR and the literature lookup are optional; the drug review is recommended and names hydrochlorothiazide or clopidogrel. EEG, brain MRI, tilt and exercise testing are now waste; the tilt report no longer uses isoproterenol. The musts are: diagnosis, monitored bed with pacing back-up, dual-chamber permanent pacemaker (ESC 2021 Class I), hold the thiazide and replete potassium and magnesium, convulsive syncope rather than epilepsy, and driving advice. VT and sinus node dysfunction are now low in the differential.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: the accepted list still carries "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "conduction disease syncope" and R55 among the codes; not hand-edited.
- Plan C3: the library tilt report (HR 68, normal) and normal monitoring contradict this case; handled per case here.
- Matcher behaviour seen here: with no initial drug output, a call naming an unstored drug (e.g. atropine) was answered by the first drug follow-up, not by `fallback_tool_outputs.drug_interactions`. Plan B step 4 relies on the fallback; it only works when the medication review also sits in `initial_tool_outputs.drug_interactions`. Worth stating in the plan for the other workers.

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. Two deviations from the lead plan, decided for dataset quality:
- Plan B step 1 says delete `initial_tool_outputs.drug_interactions`. I deleted the leaking "general" block but stored the medication-list review there (identical to the fallback), because otherwise an unnamed drug receives the hydrochlorothiazide follow-up. The text repeats no expected_evidence (leak guard passes).
- Plan J says delete the isoproterenol tilt follow-up. I kept a tilt report rewritten without isoproterenol (passive phase only), because deleting it makes the library answer a wasted tilt order with a normal HR of 68 in a patient whose rate is 51-54. The exercise-test follow-up is kept for the same reason, with its numbers corrected.

## Verification

Adversarial verifier, 24 Oct 2026. No reviewer notes exist for SYNC-CARD (no notes file), so the check covered the own-findings table, the plan's per-case index and the whole final case. Checked: every row of the table against the file (literature and drug blocks, labs tier and panels, monitoring alternatives and the telemetry output, fallback recording, echo values, CMR rewrite, deleted EP-study follow-up, tilt without isoproterenol, sequence constraints, stop rule, avoided actions, musts and prohibitions, differential, red herring paths); internal consistency of ECG, telemetry, echo and CMR numbers; leak guard; banned strings. The two logged deviations (medication review kept in `initial_tool_outputs.drug_interactions`; tilt and exercise reports kept with corrected values rather than deleted) are sound and were left.

Found and changed:
- `initial_tool_outputs.labs.panels.CBC[2]`: Hct 38.4% sits inside the stated range 38.3-48.6 but was flagged abnormal and listed "(L)" in the summary and interpretation. Set `is_abnormal` false and removed it from `abnormal_values_summary` and `interpretation` (value unchanged, consistent with Hb 12.8).
- Literature follow-up (`search_pacing_indications_av_block_bifascicular`): result 2 said an EP study "is recommended" (Class I, B) in syncope with bifascicular block; the ESC 2021 Class I, B recommendation is pacing when the EP study shows HV of 70 ms or more or infra-Hisian block. Reworded to that. Result 3 said asymptomatic Mobitz II or CHB on monitoring is "diagnostic ... Class I"; ESC 2018 gives Class I to symptom-rhythm correlation and IIa to asymptomatic Mobitz II, CHB or pauses over 3 s. Rewritten with both classes.

Re-run: perfect_agent clean, case_io check clean for this case, leak guard passes.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).
- red herring 0 `data_point` now quotes the HPI verbatim ("the patient exhibited brief jerking movements ... 10-15 seconds"); the old text was a paraphrase.

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: Mobitz II and high-grade AV block labels only (complete heart block labels and I44.2 removed: monitoring shows no complete block); bare "second degree av block" retired (it credits Mobitz I); I44.30 kept, I44.39, I45.9 and R55 dropped.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-3-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2021_Pacing]']; action-10-order-advanced-imaging citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]']; avoid-waste-1-order-ct-scan citations ['[ESC_2018]'] -> ['[NICE_NG232]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-M01` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure report, supine values = the presenting vitals; No orthostatic fall in blood pressure and no excessive heart rate rise on active standing. |
| `ground_truth.action_criteria[action-orthostatic-blood-pressure]` | added, recommended, after the ECG criterion [ESC_2018] (decisions CENTRAL 1: orthostatic BP in every initial evaluation) |
| `followup_outputs[9] (`request_electrophysiology_study`)` | added: electrophysiology_study report. Infra-Hisian conduction disease: HV interval 82 ms, with 2:1 infra-Hisian block during incremental atrial pacing at 500 ms. |
| `ground_truth.action_criteria` | no electrophysiology criterion: the documented AV block (or VT) already settles the device decision; the stored report only keeps a library normal from contradicting the case |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-10-order-advanced-imaging` label: "Cardiac MRI to characterise the substrate (optional)" -> "Cardiac MRI to characterise the substrate"
- criterion `action-6-search-medical-literature` label: "Guideline lookup on pacing indications (optional)" -> "Guideline lookup on pacing indications"

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-2-interpret-labs]`.expected_evidence: was "Potassium 3.2 mEq/L and magnesium 1.7 mg/dL at the lower limit on hydrochlorothiazide, both to be corrected; troponin I not elevated"; now "Potassium 3.2 mEq/L and magnesium 1.7 mg/dL at the lower limit on hydrochlorothiazide, both to be corrected".
- Decision: trim evidence. The July 2026 tool review ruled that syncope panels name only the assay that changes management (condition_tool_guidance.yaml); the label names electrolytes and magnesium, so the normal troponin is incidental and trimmed. The cardiac-markers panel stays servable.
- Scoring: none (evidence only; the reward does not read it).

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 80, ECOG 1, exertional limitation and recurrent falls (fallback_tool_outputs.clinical_assessment). Why: rule 2: the library reports Karnofsky 100 with no complaints in a man with exertional dyspnoea and three syncopal falls.
- `order_echocardiogram {echo_type: TEE}`: LVEF 47% with anterior-apical hypokinesis and concentric LVH, no thrombus or shunt (fallback_tool_outputs.echo). Why: rule 3: the stored TTE shows LVEF 47% with LAD-territory hypokinesis and LVH; the library TEE reports a normal heart.
- `order_echocardiogram {echo_type: bubble_study}`: same LV findings as the TTE, no right-to-left shunt (followup_outputs[10] request_bubble_study). Why: rule 3: the stored TTE is abnormal (LVEF 47%, regional hypokinesis, LVH); the library bubble study reports a normal heart.
- `order_echocardiogram {echo_type: exercise_echo}`: exercise-induced 2:1 AV block with presyncope, fixed anterior-apical hypokinesis, submaximal (followup_outputs[11] request_exercise_echo). Why: rule 3: the stored TTE (LVEF 47%, regional hypokinesis) and stored exercise test (exercise-induced 2:1 AV block) contradict a normal exercise echo with 9.5 METs.
- `order_advanced_imaging {modality: coronary_CTA}`: patent LAD stent and mild non-obstructive plaque, calcium score 412 (fallback_tool_outputs.advanced_imaging). Why: rule 2: prior anterior STEMI with PCI to the LAD; the library reports no plaque and calcium score 0.
- `order_advanced_imaging {modality: coronary_angiography}`: patent LAD stent, non-obstructive disease elsewhere, LVEDP 17 mmHg (followup_outputs[12] request_coronary_angiography). Why: rule 2: prior anterior STEMI with an LAD stent; the library reports normal coronaries.
- `order_specialized_test {test_type: polysomnography}`: severe obstructive sleep apnoea, AHI 34/h, nadir SpO2 81% (fallback_tool_outputs.specialized_test). Why: rule 2: known obstructive sleep apnoea with inconsistent CPAP use; the library reports AHI 2.1/h.
- `order_specialized_test {test_type: emg_ncs}`: mild length-dependent sensorimotor axonal polyneuropathy (followup_outputs[13] request_emg_ncs). Why: rule 2: type 2 diabetes for six years with reduced vibration at the malleoli and ankle reflexes 1+; the library reports normal nerve conduction.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
