# SYNC-CARD-M02
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search` | Repeated the literature criterion's expected_evidence (leak guard failure). | FIXED: deleted. |
| D/E | major | `initial_tool_outputs.drug_interactions.general`, `fallback_tool_outputs.drug_interactions.general` | Empty template blocks; fallback "(agent not specified on this case's pathway)". | FIXED: both replaced by a `medication_list_review` (thiazide hyponatraemia and K/Mg loss, no AV-nodal blocker before pacing, levetiracetam has no conduction or QT effect, glipizide hypoglycaemia as a cause of transient loss of consciousness). |
| C | major | `action-6-search-medical-literature`, `fallback_tool_outputs.literature_search` | Literature recommended (ruling 5); the fallback held real guideline content as a fallback. | FIXED: optional with the canonical rationale; fallback deleted; one guideline follow-up added last (ESC 2021 pacing Class I and IIa imaging under 60; 2018 ACC/AHA/HRS bradycardia guideline, Kusumoto, Circulation 2019). |
| B | major | `patient.clinical_history.medications` | HPI says levetiracetam 500 mg twice daily started 3 days ago and the labs report a level, but the medication list lacked it (plan C). | FIXED: added as `medications[8]`. |
| B | major | `action-2-interpret-labs.expected_evidence` | Claimed "mild hypokalaemia and hypomagnesaemia"; the panel shows K 4.3 and Mg 1.8 (normal) and sodium 128 mEq/L, which the case never addressed. | FIXED: expected_evidence names the sodium 128 on a thiazide and normal K/Mg; lab interpretation adds that K, Mg and troponin are normal. |
| C | major | `action-2-interpret-labs` | Plan sets labs to recommended BMP because K and Mg are normal; the BMP shows sodium 128 mEq/L on hydrochlorothiazide, which changes management (hold the thiazide, correct before implantation). | FIXED: required, `panels: [BMP]` (deviation from plan, see Open questions). |
| C | major | `sequence_constraints[0]` | Hard labs-before-monitoring constraint. | FIXED: deleted; soft ECG before TTE and before monitoring. |
| A | minor | `stop_rule` | `max_additional_actions: 0`. | FIXED: 2. |
| B | minor | `initial_tool_outputs.ecg` | "Borderline QTc prolongation" in findings vs "(prolonged)" in intervals; PR 220 ms not stated in the interpretation; em dash. | FIXED: findings and intervals give QTc 486 ms with QRS 156 ms; interpretation states the constant PR 220 ms. ECG expected_evidence rewritten. |
| B | minor | `followup_outputs[0]` (echo) | Echo numbers identical to M01 and M03, no echo_type, TAPSE, PASP or masses (plan M, G). | FIXED: own values (LVEF 53% biplane, septum 1.2 cm, LVEDD 4.9 cm, LA 3.9 cm, LAVI 33, TAPSE 22 mm, PASP 27 mmHg, normal valves); echo-voice impression; expected_evidence updated. |
| B | major | `followup_outputs[1]`, `action-4-order-cardiac-monitoring` | Criterion pinned `holter_24h` while labelled telemetry; event marker and diary wording of an outpatient Holter; heart-rate range without min and max (plan E). | FIXED: alternatives telemetry, holter_24h, holter_48h; output is "Inpatient telemetry, 24 h" (trigger `request_telemetry_holter_monitoring`), symptom reported to the nurse, range 32-72; same recording in `fallback_tool_outputs.cardiac_monitoring`. |
| C | major | `followup_outputs[2]` (CMR), `action-9-order-advanced-imaging` | CMR showed mid-wall basal septal LGE "at the level of the bundle of His" and then stated "no evidence of sarcoidosis": in a 55-year-old with AV block that pattern is typical of cardiac sarcoid and would demand FDG-PET, which the case never addresses. | FIXED: CMR rewritten as the IIa study it is (no LGE, no oedema, mild LVH, LVEF 53%), so the degenerative label holds; criterion kept recommended (age under 60), rationale and expected_evidence rewritten. Cardiac sarcoidosis added to the differential as low. |
| C | minor | `followup_outputs[5]` (tilt) | Garbled values ("45 minutes without syncope minutes", "Not performed qualitative"); not an isoproterenol tilt despite the plan's wording. | FIXED: rewritten as a clean negative 45-min passive tilt. Tilt avoided as waste. |
| B | minor | `followup_outputs[6]` (exercise) | `quantitative_data` gave a single "rate 48". | FIXED: protocol, resting/peak rates and BP; impression numbered. Exercise avoided as waste. |
| H | minor | all `action_criteria[*]` | Free-text "ESC 2018 §x" and "Locati 2014" citations; rationale equal to label; drug criterion with no drug. | FIXED: keys only, real rationales; drug alternatives `{drug: hydrochlorothiazide}`, `{drug: levetiracetam}` with one follow-up each. |
| C | major | `avoided_actions` | EEG, brain MRI, tilt and exercise not penalised (plan J). | FIXED: four waste entries naming the diagnosis; CT rationale per NICE NG232. |
| C | major | `ground_truth.assessment` | No pacing must ("Cardiology / EP consult"); no plan for the levetiracetam the referring doctor started; LP prohibition boilerplate; "antiepileptic drugs" prohibition ignored that she already takes one. | FIXED: musts are diagnosis, monitored bed with transcutaneous pacing back-up, dual-chamber pacemaker with latex precautions (documented latex allergy), hold the thiazide and correct sodium gradually, convulsive syncope and review levetiracetam with neurology to stop it, driving. Prohibitions: escalating antiseizure drugs, atropine as definitive therapy, starting AV-nodal/rate-slowing drugs, discharge before pacing; LP deleted. |
| C | major | `ground_truth.differential` | SND and VT moderate after monitoring excluded both; seizure and orthostatic entries cited the off-pathway EEG and tilt; vasovagal said "supine" (no supine event in the HPI). | FIXED: SND low (non-conducted P waves at a sinus rate of 74-78), VT low; other entries cite history, ECG and telemetry; sarcoidosis added low. |
| L | minor | `ground_truth.red_herrings[1]` | Red herring in the initial EEG, a non-criterion tool (plan L). | FIXED: replaced by the levetiracetam prescription (`patient.clinical_history.medications[8]`). |
| E | minor | `ground_truth.key_clinical_evidence`, `metadata` | Pearl "normal EEG"; "Up to 12%" figure without source; rationale counted 5 required tools and the EEG red herring. | FIXED: rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

The 55-year-old woman with Mobitz II and bifascicular block now has four required steps (ECG, BMP, TTE, inpatient telemetry with Holter accepted), CMR recommended because the block appears before 60, a recommended medication review naming hydrochlorothiazide or levetiracetam, and an optional guideline lookup. Her levetiracetam, started three days ago, is now in the medication list and is a red herring. The BMP is required because it shows sodium 128 mEq/L on a thiazide; the old key wrongly claimed low potassium and magnesium, which are normal. The echo has its own values (LVEF 53%, mild LVH). The CMR no longer shows septal mid-wall enhancement (which would have required a sarcoid work-up) and now excludes an infiltrative or inflammatory substrate. Telemetry documents frequent Mobitz II with pauses up to 5.2 s coinciding with dizziness. EEG, brain MRI, tilt and exercise testing are waste. Musts: diagnosis, monitored bed with pacing back-up, dual-chamber pacemaker with latex precautions, hold the thiazide and correct sodium gradually, convulsive syncope with a neurology review to stop levetiracetam, and driving advice. Sinus node dysfunction and VT are low; sarcoidosis is added as low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: generic synonyms ("cardiac syncope", "bradyarrhythmia", ...) and R55 still accepted; not hand-edited.
- Plan C3: library tilt and monitoring normals contradict the case; per-case outputs used.

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. Deviations from the lead plan, decided for dataset quality:
- Labs required (plan: recommended BMP). The plan's reason (K and Mg normal) is right, but the BMP also shows sodium 128 mEq/L on hydrochlorothiazide, which a must now acts on.
- Medication-list review stored in `initial_tool_outputs.drug_interactions` as well as the fallback, as in M01: otherwise an unnamed drug receives the first drug follow-up.
- Tilt and exercise follow-ups kept and cleaned rather than deleted, so a wasted order gets this patient's values instead of the library's normal report.
- CMR rewritten to show no enhancement: the plan keeps CMR recommended, and a CMR that shows a sarcoid-like pattern while the label is degenerative conduction disease is internally inconsistent.

## Verification

Adversarial verifier, 24 Oct 2026. No reviewer notes exist for SYNC-CARD. Checked every own-findings row against the file and the whole final case: levetiracetam in the medication list and as red herring (`medications[8]` resolves), sodium 128 and normal K/Mg against the labs criterion and musts, telemetry numbers (atrial 74-78, ventricular 32-72, pauses), echo and CMR (no LGE) against the differential, latex precautions against the allergy, sequence constraints, stop rule, avoided actions. The deviation making the BMP required (sodium 128 on a thiazide acted on by a must) is clinically sound and was left.

Found and changed:
- Template carry-over in the labs of this 55-year-old woman: male reference ranges for Hb (13.5-17.5), Hct (38.3-48.6) and creatinine (0.7-1.3), with Hct 45.9% against Hb 13.9 and creatinine 1.2 identical to M01 and M03. Set Hb range 12.0-15.5, Hct 41.7% (range 35.5-44.9), creatinine 0.9 mg/dL (range 0.6-1.1); none of these values is referenced elsewhere in the case.
- QTc 486 ms was copied from M01 (same value, same wide-QRS wording). Changed to 478 ms in the ECG findings, interpretation and intervals (the ECG expected_evidence does not cite the QTc).
- Tilt follow-up baseline (146/86 mmHg, HR 54) was identical to M01's and M03's tilt reports. Set to 140/84 mmHg and HR 52, consistent with her vitals (143/85) and the ECG ventricular rate (52).

Re-run: perfect_agent clean, case_io check clean for this case, leak guard passes.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).
- red herring 0 `data_point` now quotes the HPI verbatim ("she was unresponsive and her arms were shaking for approximately 5 to 10 seconds").

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: Mobitz II and high-grade AV block labels only (complete heart block labels and I44.2 removed: monitoring shows no complete block); bare "second degree av block" retired (it credits Mobitz I); I44.30 kept, I44.39, I45.9 and R55 dropped.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-3-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2021_Pacing]']; action-9-order-advanced-imaging citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]']; avoid-waste-1-order-ct-scan citations ['[ESC_2018]'] -> ['[NICE_NG232]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-M02` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.
