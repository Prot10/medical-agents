# SYNC-CARD-RS01
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `action-6-search-medical-literature`, `stop_rule` | Literature search required and in the stop rule (plan A, ruling 5). | FIXED: optional, canonical rationale, removed from the stop rule. |
| C | major | `followup_outputs` literature (both) | Invented sources (Michaelsson 2020, Sheldon 2021 "Neurology", Park and Smith 2022) and patient-specific conclusions ("1-2 mL ... far below", "normal EEG supports cardiac"). | FIXED: rewritten as general evidence from ESC 2021 pacing and ESC 2022 VA (device choice and aetiology in AV block under 60, LMNA) and from the ASRA 2017 LAST advisory (Neal 2018) and El-Boghdadly 2018; both placed last. |
| C | major | `action-9-order-specialized-test` (tilt), `avoided_actions` | Tilt was a criterion (plan RS01: delete, make waste). | FIXED: criterion deleted; `avoid-waste-5-tilt-table`. Tilt follow-up rewritten (no em dash, passive 20-min tilt, HR 40-42 in complete AV block). |
| C | major | `avoided_actions` | EEG, tilt and exercise not penalised; reasons did not name the diagnosis. | FIXED: six waste entries (brain MRI, head CT, CSF, EEG, tilt, exercise), each naming complete AV block with a likely inherited conduction disease. Head CT reason cites NICE NG232 (lowered to the couch, no head injury, no anticoagulant). |
| B | minor | `followup_outputs` (new) exercise test | A wasted exercise order would have received the library's normal sinus-rhythm report, contradicting the case. | FIXED: case-consistent exercise follow-up added (complete AV block persists, escape 40 to 54 bpm, stopped early). |
| B | major | `action-4-order-cardiac-monitoring`, monitoring follow-up | Criterion pinned holter_24h with a telemetry label; output a 24 h Holter with "stair climbing" and "14:15 PM"; interpretive QTc sentence; no case fallback (plan E). | FIXED: alternatives telemetry, holter_24h, holter_48h; output "Inpatient telemetry, 24 h" with the same numbers (average 40, 34-48 bpm, 3.8 s pause at 04:47), ambulation on the ward, min/max in `heart_rate_range`; same recording as `fallback_tool_outputs.cardiac_monitoring`. |
| A | minor | echo follow-up | No `echo_type`; no TAPSE, PASP, LAVI, wall motion; template impression. | FIXED: full TTE report (LVEF 58% biplane, septum 0.9 cm, LA 3.4 cm and LAVI 26, mild posterior leaflet prolapse, TAPSE 22 mm, PASP 24 mmHg), `echo_type: TTE`, no diagnosis sentence. |
| C | major | CMR follow-up impression | "No evidence of myocarditis, sarcoidosis" over basal septal mid-wall LGE, which is the pattern of both sarcoidosis and lamin A/C disease; "likely representing focal fibrosis of the conduction system region" is interpretation. | FIXED: impression describes the pattern only (focal linear basal septal mid-wall LGE, no oedema, normal volumes). |
| C | minor | `action-2-interpret-labs` | Pinned CBC, BMP, Mg and troponin. | FIXED: recommended, `panels: [BMP]` (plan C); no Lyme exposure in the record, so Lyme serology is not accepted. Off-pathway lab follow-up renamed into vocabulary panels (`Lyme_serology`, `inflammatory_markers`, `ACE`). |
| C | major | `action-5-check-drug-interactions`, drug follow-ups | Required with no drug; expected evidence "assess lidocaine dosing for LAST exclusion". Cyclobenzaprine, whose product label lists heart block and conduction disturbances as contraindications, was not addressed anywhere. | FIXED: recommended (plan B), alternatives escitalopram and cyclobenzaprine; follow-ups for escitalopram, cyclobenzaprine and lidocaine in report voice; medication-list review as `fallback_tool_outputs.drug_interactions`. |
| A | minor | all criteria | Free-text "ESC 2018 §x" and "Locati 2014" citations; rationale equal to label. | FIXED: keys only; real rationales. |
| D | minor | `stop_rule`, `sequence_constraints` | `max_additional_actions: 0`, no constraints. | FIXED: required ECG, TTE, monitoring; 3 additional actions; soft ECG before TTE and before monitoring. |
| C | major | `ground_truth.assessment` | No device-choice reasoning despite father's sudden death at 45, grandmother paced at 60 and septal LGE (likely laminopathy); no genetic testing or cascade screening; cyclobenzaprine continued; "Do not delay pacing while awaiting tilt-table" and duplicate driving prohibition. | FIXED: musts are recognition of the arrest mechanism, monitored bed with pacing back-up, device this admission (ESC 2021 Class I), ICD with pacing capability favoured given the likely laminopathy (ESC 2021 IIa; ESC 2022), genetic testing (LMNA, SCN5A) with cascade screening, FDG-PET if genetics negative (HRS 2014), stop cyclobenzaprine and review escitalopram, driving. Prohibitions: vasovagal/LAST attribution and discharge, AV-nodal blockers, antiseizure drugs, discharge before device. |
| C | major | `ground_truth.differential` | Vasovagal "high" and LAST and VT "moderate" after a work-up that excludes them; the inherited conduction disease, sarcoid and Lyme carditis missing (plan K). | FIXED: LMNA or other inherited conduction disease high, cardiac sarcoidosis moderate (pattern fits, not excluded), Lyme carditis low, vasovagal low, LAST low (ICD T41.3X5A), VT/VF low, PE very low (normal RV, SpO2 98%), seizure very low. |
| B | minor | `key_clinical_evidence`, `red_herrings` | "1 mL of 1%" stated as the total dose, while the HPI records 1 mL at the first point and an unquantified second injection. | FIXED: "two small intramuscular injections of 1% lidocaine" throughout; red herring interpretations rewritten; new red herring for the near-syncope attributed to anxiety. |
| E | minor | `metadata.fallback_tool_kinds`, `difficulty_rationale` | Fallback kinds missing for the new fallbacks; rationale did not mention the device decision. | FIXED. |
| B | major | `initial_tool_outputs.drug_interactions` | With no initial drug output, the MockServer served the first stored drug follow-up (e.g. this case's own named-drug review) to a check of any other drug, such as verapamil. | FIXED: the medication-list review is stored as `initial_tool_outputs.drug_interactions` as well as the fallback, so an unnamed drug receives the list review and the named-drug follow-ups still match their own drug. |

## Changes, in one paragraph a physician can read before re-reviewing

The 38-year-old woman with a pulseless, non-shockable arrest during trigger point injections has complete AV block with a narrow escape at 38 bpm. Required: ECG, TTE and immediate in-hospital telemetry (Holter accepted), which now shows 24 h of persistent complete AV block with pauses to 3.8 s and no VT. Recommended: BMP, cardiac MRI (AV block under 60, ESC 2021 IIa) and a medication review that names escitalopram (QTc 492 ms) or cyclobenzaprine (labelled contraindication in heart block). The CMR no longer claims to exclude sarcoidosis over a basal septal mid-wall scar. The tilt criterion is gone; tilt, exercise, EEG, brain MRI, head CT and CSF are waste. The assessment now treats this as a likely familial conduction disease (father's sudden death at 45, grandmother paced at 60): device this admission, ICD with pacing capability favoured, LMNA/SCN5A testing with cascade screening, FDG-PET if genetics is negative, stop cyclobenzaprine, driving advice. Vasovagal, LAST and VT are low; sarcoidosis moderate; Lyme carditis low. Literature is optional, with real guideline sources.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: generic synonyms ("cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "conduction disease syncope") and R55 are still accepted, and the I44 block also accepts "mobitz ii" and "second degree av block" for a complete-block case; not hand-edited.
- Plan C2: no cardiac genetic panel (`inherited_arrhythmia` / `cardiomyopathy`) in the vocabulary, so LMNA/SCN5A testing lives in a must only.

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. Decisions taken:
- Drug check kept `recommended` as the plan tiers it, although the cyclobenzaprine contraindication is concrete: stopping it is a must, and the pacing or ICD decision does not depend on the review.
- Cardiac sarcoidosis left `moderate`, not low: the CMR pattern fits it and no pathway result excludes it; the FDG-PET must covers it.

## Verification

Checked (24 Oct 2026, adversarial pass): the log against the diff from fa1d22e6 and the whole final case; patient block unchanged; ECG, telemetry (case fallback identical), echo, CMR arithmetic (LVEF (118-51)/118 = 57%, RVEF 54%), tilt and exercise follow-ups against the vitals and the ECG; drug outputs against the medication list; musts against prohibitions and avoided actions; differential against the results; stop rule, sequence constraints, pathway order (literature last); banned strings; leak guard.

Found and changed:
- `red_herrings[0..2].data_point` were paraphrases, not quotes from the field (plan L). Now quote the HPI ("She reported anxiety about the procedure but agreed to proceed.", "1 mL of lidocaine was injected intramuscularly") and the PMH ("Mitral valve prolapse noted incidentally on echocardiogram 3 years ago").
- Literature follow-up `search_pacing_av_block_young_adults_lamin`: the ESC 2022 LMNA finding misstated the IIa criterion ("pacing indication or other high-risk feature"); now the 5-year risk of 10% or more with a manifest phenotype (NSVT, LVEF below 50% or AV conduction delay). The summary said an ICD is considered "when a laminopathy is likely or confirmed"; the guideline applies to LMNA mutation carriers, so it now says that and adds genetic testing when a familial conduction disease is suspected.
- Escitalopram drug follow-up quoted this patient's QTc (492 ms) and rhythm, an ECG result inside a drug report: rewritten as the general QT caution (prolonged QTc, bradycardia or pauses).

Confirmed correct, no change: cyclobenzaprine label contraindication; lidocaine maximum 4.5 mg/kg (300 mg); CHB tiers per plan; sarcoid kept moderate with the FDG-PET must. perfect_agent clean, `case_io.py check` clean for this case, leak guard passes.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).
- Literature follow-up trigger `search_lidocaine_toxicity_cardiac_arrest` renamed to `search_lidocaine_local_anaesthetic_systemic_toxicity`. Why: the old trigger's meaningful tokens were generic (management, guidelines, diagnosis, syncope, literature), so a generic query hit the disease-specific report; the new tokens are the condition names, so only a query naming the condition reaches it.

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: complete heart block labels only (Mobitz II and second-degree labels removed: a different grade); I44.30 kept, I44.1, I44.39, I45.9 and R55 dropped.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-3-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2021_Pacing]']; action-8-order-advanced-imaging citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]']; avoid-waste-2-order-ct-scan citations ['[ESC_2018]'] -> ['[NICE_NG232]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-RS01` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure 'Active stand test not performed. Deferred by the clinical team.' (haemodynamically unstable or high-grade AV block at presentation: standing is not safe); no criterion |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.

| field path | change |
| --- | --- |
| `followup_outputs[11]` (`request_electrophysiology_study`) | added: 'Electrophysiology study not performed. Deferred by the clinical team.' The documented rhythm already settles management, and the library's normal study (normal AV conduction and sinus node function, nothing inducible) would contradict the case; no criterion |

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-6-search-medical-literature` label: "Guideline lookup on device choice (optional)" -> "Guideline lookup on device choice"

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 80, ECOG 1 (fallback_tool_outputs.clinical_assessment). Why: rule 2: the library reports Karnofsky 100 with no complaints in a woman with exertional near-syncope who arrested today in complete heart block.
- `order_echocardiogram {echo_type: TEE}`: mild posterior mitral leaflet prolapse, otherwise normal (fallback_tool_outputs.echo). Why: rule 3: the stored TTE shows mild posterior mitral leaflet prolapse; the library TEE reports a structurally normal mitral valve.
- `order_echocardiogram {echo_type: bubble_study}`: mild mitral prolapse, no shunt (followup_outputs[12] request_bubble_study). Why: rule 3: the stored TTE shows mild posterior mitral leaflet prolapse; the library reports a structurally normal mitral valve.
- `order_echocardiogram {echo_type: exercise_echo}`: persistent complete AV block, escape 40 to 54 bpm, stopped early (followup_outputs[13] request_exercise_echo). Why: rule 3: the stored exercise test shows persistent complete AV block with chronotropic incompetence; the library reports a normal study at 9.5 METs.
- `interpret_labs {panels: [lipid_panel]}`: LDL 168 mg/dL, total cholesterol 246 mg/dL (fallback_tool_outputs.labs['lipid_panel']). Why: rule 2: hyperlipidaemia managed with lifestyle measures only, no lipid-lowering drug; the library reports a normal lipid panel.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
