# SYNC-CARD-RS03
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | echo, monitoring and CMR follow-ups (plan M) | Values copied from RS02: LVEF 42%, LA 4.1 cm, septum 1.3 cm, mean AV gradient 18 mmHg; Holter average 37, range 30-44, 3.8 s pause; CMR native T1 1120 ms, LV mass 148 g. | FIXED: own echo (LVEF 45% biplane, LVEDD 5.3 cm, LA 4.3 cm and LAVI 38, septum 1.2 cm, mild AS Vmax 2.9 m/s, mean 19 mmHg, AVA 1.5 cm2, mid anteroseptal hypokinesis and post-surgical septal motion matching the CMR scar, TAPSE 18 mm, PASP 30); own telemetry (average 34, 28-41 bpm, 5.2 s pause in sleep, 4.4 s pause awake with presyncope); own CMR (native T1 1095 ms, LVEDV 168 mL, LVESV 94 mL, LVEF 44%, LV mass 136 g). |
| B | minor | `initial_tool_outputs.ecg`, `patient.vitals.hr`, labs | ECG rate 38, atrial rate 82 and QTc 492 ms identical to RS01/RS02; labs shared RS02's K 4.6, Cl 101, WBC 6.8, platelets 198, BNP 312, CK-MB 3.1, Mg 1.9, TSH 3.1; ECG rhythm "junctional/ventricular" for an infra-Hisian escape; old expected evidence said "~35 bpm". | FIXED: ECG rate 35 (vitals HR 35), atrial rate 88, QTc 478 ms, rhythm "ventricular escape"; labs K 4.3, Cl 103, WBC 7.4, platelets 224, BNP 268, CK-MB 2.6, Mg 2.0, TSH 1.9 (summary and interpretation updated). Tilt and exercise heart rates aligned with the new escape rate. |
| C | major | `avoided_actions` CT, `action-9-order-ct-scan` (new) | Head CT avoided with the reason "without LOC", but he lost consciousness for 15-20 s at 72 and struck his right temple: NICE NG232 indicates a CT within 8 hours. | FIXED: recommended criterion; CT report in `initial_tool_outputs.ct` (no haemorrhage, collection or fracture; right temporal scalp swelling); CT fallback removed. |
| C | major | `action-6-search-medical-literature`, `stop_rule`, literature follow-up | Literature required and in the stop rule; the follow-up cited a non-existent EHJ 2021 review and gave patient-level management. | FIXED: optional, canonical rationale; follow-up rewritten from ESC 2021 pacing, Zeltser 2004 (drug-related AV block persisting after withdrawal) and ACC/AHA/HRS 2018 (pacing mode with LVEF 36-50%); placed last. |
| C | minor | `action-2-interpret-labs` | Pinned CBC, BMP, Mg, troponin; expected evidence "Troponin negative" while the stored troponin is 0.05 ng/mL (raised). | FIXED: recommended, `panels: [BMP, troponin]`; expected evidence states the raised troponin with normal CK-MB. Troponin kept as a targeted assay (exertional chest tightness after CABG). |
| B | major | `action-4-order-cardiac-monitoring`, monitoring follow-up | Criterion pinned holter_24h under a telemetry label; no case fallback (plan E). | FIXED: alternatives telemetry, holter_24h, holter_48h; "Inpatient telemetry, 24 h"; same recording as the monitoring fallback. |
| C | major | `action-5-check-drug-interactions`, atenolol follow-up | Required without a drug; output claimed amlodipine adds negative chronotropic and dromotropic effects (a dihydropyridine has none of relevance); "Agent selection per cardiology evaluation". | FIXED: recommended, `drug: atenolol`; output in report voice (label contraindication, renal excretion in CKD, additive hypotension only); medication-list review as the drug fallback (metformin and contrast, aspirin at implant). |
| C | minor | CMR follow-up | "No features of sarcoidosis, amyloidosis, or ARVC" and "at the level of the bundle of His" are interpretation; em dash. | FIXED: findings only. Criterion optional (age 72). |
| C | minor | tilt, exercise follow-ups | "qualitative" garbage values; em dash; exercise "suggestive of demand ischemia". | FIXED: cleaned; both avoided as waste. |
| C | major | `avoided_actions` | Only CT and CSF; EEG, brain MRI, tilt and exercise not penalised. | FIXED: CSF, EEG, brain MRI, tilt, exercise as waste, each naming complete heart block with an infranodal escape. |
| C | major | `ground_truth.assessment` | "Cardiology / EP consult" instead of a pacing decision; no guidance on atenolol versus pacing; troponin rise ignored; duplicate driving prohibition. | FIXED: musts are recognition, monitored bed with pads and temporary wire if needed, stop atenolol without waiting for washout (ESC 2021), permanent pacing this admission (Class I), physiological pacing with LVEF 45% (ACC/AHA/HRS 2018 IIa), ischaemia evaluation of the raised troponin, driving. Prohibitions: AV-nodal blockers before pacing, waiting for washout, discharge before pacing. |
| C | major | `ground_truth.differential` | VT moderate after telemetry; SSS justified by "paroxysmal AF with conversion pauses" that is nowhere in the case; atenolol as a cause and the patient's own aortic stenosis not discussed. | FIXED: drug-induced block (low, infranodal escape), ACS (low, small troponin rise), VT (low), SSS (low, sinus 76-104 bpm), aortic stenosis (very low, mild), vasovagal and orthostatic (very low). |
| L | major | `red_herrings` | "Brief disorientation post-event" contradicts the HPI ("no period of confusion, disorientation"); "Patient denies any preceding symptoms" is not quoted from the HPI. | FIXED: the disorientation red herring deleted; the prodrome one quotes "without any preceding cry, warning, or abnormal movements"; red herrings added for "which he attributed to aging" and the mild aortic stenosis in the history. |
| A | minor | all criteria, `stop_rule`, `sequence_constraints` | Free-text section citations, rationale equal to label, `max_additional_actions: 0`, no constraints. | FIXED: keys only, real rationales, stop rule ECG/TTE/monitoring with 3 additional actions, soft ECG before TTE and before monitoring. |
| E | minor | `key_clinical_evidence`, `metadata` | "Holter and EP study are confirmatory" (no EP study in the vocabulary or the pathway). | FIXED: key evidence rewritten from the case's results; fallback kinds and difficulty rationale updated. |
| B | major | `initial_tool_outputs.drug_interactions` | With no initial drug output, the MockServer served the first stored drug follow-up (e.g. this case's own named-drug review) to a check of any other drug, such as verapamil. | FIXED: the medication-list review is stored as `initial_tool_outputs.drug_interactions` as well as the fallback, so an unnamed drug receives the list review and the named-drug follow-ups still match their own drug. |

## Changes, in one paragraph a physician can read before re-reviewing

The 72-year-old man after CABG who collapsed while seated has complete heart block with a wide RBBB-morphology escape at 35 bpm (infranodal), on atenolol. Required: ECG, TTE, inpatient telemetry (Holter accepted); recommended: BMP with troponin, a head CT for loss of consciousness with a temple strike at 72 (NICE NG232), and a review of atenolol. His echo, telemetry, CMR, ECG and labs no longer copy RS02: LVEF 45% with anteroseptal hypokinesis matching a small CMR scar, mild AS, pauses of 5.2 s and 4.4 s (the second with presyncope), troponin 0.05 ng/mL with normal CK-MB. CMR and the literature lookup are optional; CSF, EEG, brain MRI, tilt and exercise are waste. Musts: monitored bed with pacing back-up, stop atenolol without waiting for washout, permanent pacing this admission with physiological pacing for LVEF 45%, ischaemia evaluation of the troponin rise, driving advice. The differential now discusses atenolol, ACS and his aortic stenosis, all low or very low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: generic synonyms and R55 still accepted, and the I44 block accepts "mobitz ii" and "second degree av block" for a complete-block case; not hand-edited.
- Plan (lead): section 3 lists head CT as avoided in this subtype, but RS03 meets the plan's own NG232 rule (65 or over, loss of consciousness, head strike).

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. Deviations from the lead plan, decided for dataset quality:
- Head CT recommended instead of avoided (NICE NG232).
- Labs pinned as BMP plus troponin, because the stored troponin is raised and the patient has exertional chest tightness after CABG.
- The patient record (HPI, history, medications) was not rewritten: it already differs from RS02 (CABG, diabetes, atenolol, witnessed seated collapse); only the copied numbers were changed.

## Verification

Checked (24 Oct 2026, adversarial pass): the log against the diff from fa1d22e6; that no echo, telemetry, CMR, ECG or lab number still equals RS02 (plan M); CMR arithmetic ((168-94)/168 = 44%, echo 45%); telemetry timestamps against the 6:30 PM presentation; telemetry fallback identical to the follow-up; head CT tier (NICE NG232, LOC with a temple strike at 72: correct); troponin 0.05 ng/mL flagged and reflected in the labs criterion, the differential and the ischaemia must; atenolol must vs the "do not wait for washout" prohibition (consistent); Zeltser 2004 citation exists (J Am Coll Cardiol 2004;44:105-108); red herring quotes match the HPI and PMH.

Found and changed:
- CMR `LV_mass` "136 g (upper normal)": 136 g is mid-range for a man; label corrected to "(normal)".

perfect_agent clean, `case_io.py check` clean for this case, leak guard passes.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: complete heart block labels only (Mobitz II and second-degree labels removed: a different grade); I44.30 kept, I44.1, I44.39, I45.9 and R55 dropped.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-9-order-ct-scan citations ['[ESC_2018]'] -> ['[NICE_NG232]']; action-3-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2021_Pacing]']; action-8-order-advanced-imaging citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-RS03` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure 'Active stand test not performed. Deferred by the clinical team.' (haemodynamically unstable or high-grade AV block at presentation: standing is not safe); no criterion |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.

| field path | change |
| --- | --- |
| `followup_outputs[8]` (`request_electrophysiology_study`) | added: 'Electrophysiology study not performed. Deferred by the clinical team.' The documented rhythm already settles management, and the library's normal study (normal AV conduction and sinus node function, nothing inducible) would contradict the case; no criterion |
