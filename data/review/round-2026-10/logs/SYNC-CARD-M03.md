# SYNC-CARD-M03
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search`, `initial_tool_outputs.drug_interactions.general` | Both repeated their criteria's expected_evidence (leak guard failure). | FIXED: literature deleted; drug block replaced by a `medication_list_review` (also stored as the fallback). |
| E | major | `fallback_tool_outputs.drug_interactions.general.proposed` | "(agent not specified on this case's pathway)". | FIXED: replaced by the medication-list review (thiazide K/Mg loss, no AV-nodal blocker before pacing, glipizide hypoglycaemia, metformin and B12 with macrocytosis, aspirin continued at implant). |
| C | major | `fallback_tool_outputs.literature_search`, `action-6-search-medical-literature` | Literature recommended; fallback claimed "trifascicular block with syncope is a Class IIa indication" from the ACC/AHA/HRS bradycardia guideline (not what that guideline says: it recommends EP study or monitoring for bifascicular block with syncope). | FIXED: optional with the canonical rationale; fallback deleted; one ESC 2021 / ESC 2018 guideline follow-up added last. |
| B | major | `initial_tool_outputs.ecg` | ECG text and intervals identical to M01 (PR 224, QRS 148, QTc 486 "borderline") (plan M). | FIXED: own ECG (rate 54, PR 238 ms, QRS 142 ms, QTc 468 ms, axis -60, two PVCs), interpretation without prognosis or em dash; expected_evidence updated. |
| B | major | `initial_tool_outputs.labs.panels.BMP` | Sodium 146, chloride 89, CO2 25: anion gap 32 with a normal bicarbonate, impossible in this context; thiazides do not raise sodium. | FIXED: sodium 138 (normal), chloride 96 (L), CO2 30 (H), a hypochloraemic alkalosis consistent with K 3.2 on a thiazide; summary and interpretation updated. |
| B | minor | `initial_tool_outputs.labs.panels.CBC` | Hct 39.5% with Hb 14.6 g/dL. | FIXED: Hct 43.8%. |
| C | minor | `action-2-interpret-labs` | Pinned CBC and troponin. | FIXED: required `panels: [BMP, magnesium]` (K 3.2, Mg 1.5); expected_evidence states the values. |
| C | major | `sequence_constraints[0]` | Hard labs-before-monitoring constraint. | FIXED: deleted; soft ECG before TTE and before monitoring. |
| A | minor | `stop_rule` | `max_additional_actions: 0`. | FIXED: 2. |
| B | minor | `followup_outputs[0]` (echo) | Echo template identical to M01 and M02 (LVEF 50%, IVS 1.3, LA 4.1); no echo_type, TAPSE, Vmax. | FIXED: own values (LVEF 52%, septum 1.5 cm, LA 4.4 cm, LAVI 40, mild calcific AS with Vmax 2.7 m/s, mean 16 mmHg, AVA 1.5 cm2, matching the CMR's 2.8 m/s; PASP 32 mmHg kept). |
| B | major | `followup_outputs[1]`, `action-4-order-cardiac-monitoring` | 48 h Holter under a telemetry label; criterion pinned holter_24h; "187 PVCs in 24 hours" in a 48 h recording; minimum 38 bpm while the escape rhythm was 32 bpm; diary wording (plan E). | FIXED: alternatives telemetry, holter_24h, holter_48h; output "Inpatient telemetry, 48 h", PVCs per 48 h, range 32-82 bpm, pause described as 3.8 s at onset before a 32 bpm escape; same recording as `fallback_tool_outputs.cardiac_monitoring`. |
| C | major | `followup_outputs` CT, `action-11-order-ct-scan` (new) | He is 71, lost consciousness and struck his left temple (ecchymosis on exam; the stored CT shows subgaleal swelling): NICE NG232 indicates a head CT within 8 hours. The plan lists head CT as avoided here, which contradicts its own NG232 rule. | FIXED: new recommended criterion; the CT report moved to `initial_tool_outputs.ct` (served for any head CT order) and reworded (subgaleal haematoma, no fracture). See Open questions. |
| C | minor | `followup_outputs[5]` (tilt), `[6]` (exercise) | Tilt values with "qualitative" garbage; exercise "62% of age-predicted maximum" (98/149 = 66%) and `quantitative_data.rate` 52. | FIXED: tilt rewritten as a negative passive 45-min tilt; exercise percentages and quantitative data corrected. Both avoided as waste. |
| C | minor | `followup_outputs[2]` (CMR) | "No evidence of ... sarcoidosis" stated over patchy septal mid-wall LGE. | FIXED: impression describes the pattern (septal and RV insertion-point mid-wall enhancement, as seen in pressure-overload hypertrophy) without the exclusion claim. CMR optional (age 71). |
| D | minor | `initial_tool_outputs.eeg.artifacts[1]` | "Recommend dedicated cardiac evaluation" in an EEG artifact note (cross-modality hint). | FIXED: deleted. |
| H | minor | all `action_criteria[*]` | Free-text "ESC 2018 §x" and "Locati 2014" citations; rationale equal to label; drug criterion with no drug. | FIXED: keys only, real rationales; drug alternative `{drug: hydrochlorothiazide}` with its follow-up. |
| C | major | `avoided_actions` | Only CSF avoided; EEG, brain MRI, tilt and exercise not penalised. | FIXED: four waste entries naming the diagnosis. |
| C | major | `ground_truth.assessment` | No pacing must ("Cardiology / EP consult"); generic driving and electrolyte musts; LP prohibition boilerplate. | FIXED: musts are diagnosis, monitored bed with pacing back-up, dual-chamber pacemaker with latex precautions (documented latex allergy), hold the thiazide and replete K and Mg, convulsive syncope, driving (Group 1 one week after implant). Prohibitions: antiseizure drugs, AV-nodal/rate-slowing drugs before pacing, discharge before pacing, treating the events as orthostatic; LP and the duplicate driving prohibition deleted. |
| C | major | `ground_truth.differential` | VT and sick sinus syndrome moderate after a work-up that excludes them; entries cited EP study, EEG and tilt that are not on the pathway; the patient's mild AS not discussed. | FIXED: VT low, SSS low (nocturnal sinus slowing only, symptomatic pause from AV block); others cite history and telemetry; aortic stenosis added as low. |
| C | minor | `ground_truth.key_clinical_evidence` | "OSA contributes to nocturnal bradyarrhythmia and must be addressed" (the documented block was at 19:42, not nocturnal). | FIXED: replaced by the telemetry, AS and NG232 points. |
| L | minor | `ground_truth.red_herrings` | EEG red herring in a non-criterion tool; orthostatic red herring cited the tilt. | FIXED: EEG red herring deleted; orthostatic one cites seated events and telemetry; mild AS in the history added as a red herring. |
| E | minor | `metadata` | Unsourced "up to 12%" pearl; "Class I indication" for trifascicular block with syncope; difficulty rationale with 5 required tools. | FIXED: rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

The 71-year-old man with trifascicular disease now has four required steps (ECG, potassium and magnesium, TTE, inpatient telemetry with Holter accepted) and a recommended head CT, because he lost consciousness and struck his temple at 71 (NICE NG232). His ECG, echo and labs have their own numbers: PR 238 ms and QRS 142 ms; LVEF 52% with septum 1.5 cm and mild calcific aortic stenosis (AVA 1.5 cm2); K 3.2, Mg 1.5 with a hypochloraemic alkalosis on the thiazide (the impossible sodium 146 with chloride 89 is corrected). Telemetry captures 8 s of complete heart block with a 3.8 s pause and a 32 bpm escape during near-syncope. CMR and the literature lookup are optional; the drug review names hydrochlorothiazide. EEG, brain MRI, tilt and exercise are waste. Musts: diagnosis, monitored bed with pacing back-up, dual-chamber pacemaker with latex precautions, hold the thiazide and replete K and Mg, convulsive syncope, driving advice. VT and sick sinus syndrome are low; mild aortic stenosis is added to the differential and as a red herring.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: generic synonyms and R55 still accepted; not hand-edited.
- Plan (lead): section 3 lists head CT as avoided for M03, but the case meets the plan's own NG232 rule (age 65 or over, loss of consciousness, head strike). The same check is worth doing for every case aged 65 or over with a fall.

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. Deviations from the lead plan, decided for dataset quality:
- Head CT recommended instead of avoided (NICE NG232, as above).
- Medication-list review stored in `initial_tool_outputs.drug_interactions` as well as the fallback, as in M01 and M02.
- Tilt and exercise follow-ups kept and cleaned rather than deleted, so a wasted order gets this patient's values.

## Verification

Adversarial verifier, 24 Oct 2026. No reviewer notes exist for SYNC-CARD. Checked every own-findings row against the file and the whole final case: rewritten ECG (own intervals), corrected BMP (Na 138, Cl 96, CO2 30 with K 3.2), telemetry CHB episode, echo/CMR AS numbers, the new recommended head CT (the exam documents a left temporal ecchymosis from the fall at 71, so the NICE NG232 deviation from the plan is correct), latex precautions, sequence constraints, stop rule, avoided actions, red herring paths (`past_medical_history[4]` resolves).

Found and changed:
- AVA 1.5 cm2 was called "mild" aortic stenosis, but 1.5 cm2 is the upper bound of the ESC/EACTS 2021 moderate band (1.0-1.5); mild is above 1.5. Set AVA 1.6 cm2 in the echo valves and impression, the TTE expected_evidence, the aortic-stenosis differential entry and the red herring, so the "mild" grading holds with Vmax 2.7 m/s and mean 16 mmHg.
- Differential (sick sinus syndrome) cited a sinus rate rise "to 82-98 bpm"; 98 bpm comes only from the exercise test, which is an avoided action (plan K). Now cites 82 bpm on telemetry.
- Tilt follow-up baseline 146/86 mmHg was identical to M01 and M02; set to 138/82 mmHg (vitals 137/84; HR 54 kept, matching his vitals).
- Literature follow-up: the EP-study result and the monitoring result carried the same class errors as M01 (EP study "recommended" Class I; monitoring without symptoms "establishes" arrhythmic syncope). Reworded to pacing on an abnormal EP study (ESC 2021 I, B) and symptom correlation I / asymptomatic Mobitz II, CHB or pause over 3 s IIa (ESC 2018).

Re-run: perfect_agent clean, case_io check clean for this case, leak guard passes.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).
- red herrings 0 and 1 `data_point` now quote the HPI verbatim (the 10 to 15 second jerking; the PCP's "orthostatic hypotension" attribution and hydrochlorothiazide reduction).

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: keeps the Mobitz II and high-grade labels and, scoped to this case, the complete heart block labels and I44.2, because telemetry captures transient complete heart block.
- I44.39, I45.9 and R55 dropped.
- "ESC/EACTS 2021" renamed "ESC/EACTS 2025" (2025 ESC/EACTS valvular guideline, Praz 2025, supersedes 2021): `.ground_truth.action_criteria[3].rationale`.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-11-order-ct-scan citations ['[ESC_2018]'] -> ['[NICE_NG232]']; action-3-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_EACTS_2025_VHD]']; action-10-order-advanced-imaging citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-M03` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure report, supine values = the presenting vitals; No orthostatic fall in blood pressure and no excessive heart rate rise on active standing. |
| `ground_truth.action_criteria[action-orthostatic-blood-pressure]` | added, recommended, after the ECG criterion [ESC_2018] (decisions CENTRAL 1: orthostatic BP in every initial evaluation) |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.

| field path | change |
| --- | --- |
| `followup_outputs[8]` (`request_electrophysiology_study`) | added: 'Electrophysiology study not performed. Deferred by the clinical team.' The documented rhythm already settles management, and the library's normal study (normal AV conduction and sinus node function, nothing inducible) would contradict the case; no criterion |
