# ISCH-STR-M02
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| f9ddb5ea-7835-4e8c-8253-b67625de22b6 | FIXED | `patient.neurological_exam.cranial_nerves`: "Left lower facial droop ... with forehead and eye closure spared". Same class checked across the exam: `mental_status` "Writing shows mild right-hand clumsiness" (right hand is unaffected) replaced by normal right-hand writing; `metadata.difficulty_description` "right-sided neglect" corrected to left-sided. |
| b798000b-b61d-4b76-8fdd-ff4eda0e651a | FIXED | HPI verdict "placing her outside the standard IV alteplase window" removed (times and the 03:00 bathroom visit kept). New recommended criterion `ct-perfusion-extended-window` and follow-up `request_ct_perfusion` (`followup_outputs[1]`): small deep deficit, core 2 mL, Tmax above 6 s 3 mL, mismatch 1 mL, ratio 1.5; the 10 mL mismatch volume is not reached, so EXTEND criteria fail. Decision must, LKW must (both the 23:00 and the 03:00 estimates), wake-up prohibition, key evidence (C3 canonical) and clinical pearl 1 address both limbs. |
| eae4a343-7b3f-48eb-b231-9c299243a6b1 | FIXED | `action_criteria` reordered NCCT, labs, ECG, CTA, MRI (optional), CTP, TTE, monitoring, drug check, literature (optional); `followup_outputs` CTA, CTP, TTE, Holter, drug check, literature; thrombophilia follow-up removed; soft constraints replace the template hard NCCT-to-drug-check constraint. NCCT, labs and ECG stay in `initial_tool_outputs` (they are answered there); showing them as numbered steps is the CENTRAL UI request. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.neurological_exam.additional` | NIHSS 6 does not match the exam. | FIXED: exam made scorable (arm and leg drift, ataxia in proportion to weakness, language normal, month and age correct) and recounted: NIHSS 9 (gaze 1, visual 1 for extinction, facial 1, left arm 1, left leg 1, sensory 1, dysarthria 1, extinction 2 for visual and tactile); updated in LKW must and key evidence. |
| C | minor | `patient.neurological_exam.mental_status` | "occasional word-finding pauses" in a right-handed patient with a right subcortical lesion. | FIXED: language stated as normal (language item 0). |
| D | major | `initial_tool_outputs.ct.findings[3..4]`, `.additional_observations[1]` | The NCCT report carried the CTA results (M1 and carotid stenoses) and an aortic arch finding a head NCCT cannot see; the CTA follow-up had an empty findings list. | FIXED: both CTA findings and the arch observation moved to the CTA follow-up; NCCT impression numbered without them. |
| D | major | `followup_outputs[0].output.recommended_actions`, `.angiography_findings`, `.impression` | Management text ("thrombolysis is not excluded...", "not a mechanical thrombectomy candidate", "no thrombectomy target"); "symptomatic-appearing" stenosis; impression in lower case without numbering. | FIXED: recommended_actions emptied, management phrase removed, impression opens with the right M1 40-50% stenosis, then no LVO, carotids, no dissection. |
| B | major | `initial_tool_outputs.labs.panels.BMP` | Anion gap 139 - 94 - 21 = 24 with no explanation. | FIXED: chloride 104 (normal), gap 14; abnormal list and interpretation updated. |
| B | major | `initial_tool_outputs.labs.panels.CBC`, `.BMP` creatinine | Male reference ranges for haemoglobin, haematocrit, RBC and creatinine in a woman; RBC 4.65 x MCV 96.5 gives Hct 44.9, not the stored 39.6. | FIXED: female ranges (Hb 12.0-15.5, Hct 34.9-44.5, RBC 3.92-5.13, creatinine 0.59-1.04); RBC 4.10 so Hct = RBC x MCV. |
| B | major | `patient.clinical_history.past_medical_history[4]`, HPI, drug check | "CKD stage 3a" with baseline creatinine 1.4 mg/dL in a 58-year-old woman is eGFR about 44 (CKD-EPI 2021), stage 3b; today's 1.5 gives about 40. | FIXED: stage 3b with eGFR in PMH, HPI, drug check, key evidence; metformin 1000 mg/day ceiling stated in the drug check. |
| B | major | `followup_outputs[3]` (Holter) | 72-hour recording labelled `holter_24h` (no 72 h type exists); "847 PACs" template value called frequent; interpretive "irritable atrial substrate". | FIXED: 48-hour recording, `holter_48h` in output, `tool_parameters` and the first criterion alternative (plus holter_24h, telemetry); events kept (longest AF 45 s at hour 38), PACs 612 in 48 h called occasional, PVCs 19; impression opens "Recorded on the stroke unit after admission, 48 hours." |
| B | minor | `followup_outputs[2]` (echo) | "Abnormal values: ... (H)" impression; LAVI without unit. | FIXED: real TTE impression, unit, thrombus statement, `tool_parameters` echo_type TTE. |
| B | major | `initial_tool_outputs.mri.impression` | Impression omitted the acute infarct. | FIXED: numbered impression naming the acute right corona radiata infarct first. |
| C | major | drug-check output | CKD statement in `contraindications`; warfarin as an equal alternative. | FIXED: aspirin stop, no other interaction, dose rationale (one of three criteria), metformin limit, DOAC alternatives; contraindications state none identified with platelets and INR. |
| C | major | literature output | Fabricated "2019 AHA/ASA Guideline Update: Wake-up Stroke Management"; one-limb summary. | FIXED: WAKE-UP, EXTEND, AHA/ASA 2026 with full references; general summary; criterion optional with `required_arguments` {}, last. |
| C | major | `ground_truth.assessment` | Template musts (door-to-needle, pre-IVT BP, generic secondary prevention, "Adjust contrast use for CKD"); no decision; prohibitions on CKD contrast and large-infarct anticoagulation; 140/90 prohibition. | FIXED: LKW/NIHSS, decision, telemetry, apixaban 5 mg twice daily within 48 h with aspirin stopped (CHA2DS2-VASc 5, HAS-BLED 2), ezetimibe added to rosuvastatin to LDL below 70, risk factors with antihypertensives resumed after 48 to 72 h; C5 canonical prohibition; CKD and large-infarct prohibitions removed; wake-up prohibition covers both limbs. |
| C | minor | `ground_truth.differential` | Pure lacunar "high" despite a 2.1 cm lesion, a 40-50% parent M1 stenosis and AF on Holter; key features not updated to the results. | FIXED: lacunar moderate; each entry states the supporting and excluding results. |
| E | minor | `ground_truth.key_clinical_evidence` | Off-pathway lines x3, July 2026 tier line, CKD "renal-protective strategy" line. | FIXED: removed or replaced; NIHSS, C3 wake-up, Holter with scores, CKD line added. |
| A | minor | criteria, avoided actions | Free-text citation, duplicate and superseded keys; labels identical to rationales. | FIXED. |
| B | minor | `initial_tool_outputs.ecg`, echo chambers | ECG intervals, rate and voltages and the echo LAVI/septum are identical to M01 (template values). | FLAGGED: values are plausible and internally consistent, left unchanged to avoid churn. |

## Changes, in one paragraph a physician can read before re-reviewing

The facial palsy is now left-sided and the whole exam is consistent with the right corona radiata infarct (left neglect, normal language and right-hand writing); recounted NIHSS 9. The HPI keeps the 23:00 and 03:00 times without concluding eligibility. The pathway runs NCCT, labs, ECG, CTA, new CT perfusion (core 2 mL, mismatch 1 mL, ratio 1.5, fails the 10 mL mismatch volume of EXTEND), optional MRI, TTE (recommended), 48-hour Holter (required) and the apixaban check; the thrombophilia panel is removed and the literature step is optional. The NCCT no longer contains the CTA findings, which now sit in the CTA report (no LVO, right M1 40-50% stenosis), stripped of management text. Labs now use female reference ranges, chloride 104 (anion gap 14), RBC consistent with Hct; CKD is restaged 3b (creatinine 1.4 to 1.5 mg/dL in a 58-year-old woman). The Holter is a 48-hour study with one 45-second AF episode. Musts: LKW and NIHSS, explicit decision (no IVT on either limb, no EVT), stroke-unit telemetry, apixaban 5 mg twice daily within 48 h with aspirin stopped (CHA2DS2-VASc 5, HAS-BLED 2), ezetimibe added for LDL 132 to target below 70, risk factors and antihypertensives resumed after 48 to 72 h. The 140/90 and CKD-contrast prohibitions are gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[AHA_ASA_Stroke_2026]`, `[AHA_ASA_2021_secondary]` for the criteria-pack allow-list (plan 5.1).
- Review UI: initial work-up (NCCT, labs, ECG) shown as numbered steps in criterion order (note eae4a343; plan 5.2).
- `accepted[0]` contains an em dash; left untouched per ruling 3.

## Open questions for Andrea (judgment calls you could not settle)

- Anticoagulation rests on a single 45-second AF episode (burden below 0.1%) in a deep infarct with intracranial atherosclerosis. AF of 30 seconds or more meets the AF definition and the plan (C6) anticoagulates; some stroke neurologists would weigh the subclinical burden and the small-vessel phenotype. Please confirm with R2.
- NIHSS item 3 scored 1 for visual extinction (NIHSS instruction) in addition to item 11; without it the total is 8.
- CKD restaged from 3a to 3b to match the creatinine values; the alternative is to lower the stored creatinine to about 1.2 to 1.3 mg/dL.

## Verification
Adversarial verifier, 23 October 2026. Checked: all 3 note ids in the table; left lower facial droop with forehead spared, whole exam left-sided, gaze difficulty to the left (eyes toward the right lesion); HPI verdict removed with times kept; CTP fails EXTEND on mismatch volume (1 mL); CTA is the first follow-up and NCCT, labs, ECG stay initial (CENTRAL UI request logged). NIHSS 9 recounted from the final exam; female reference ranges, gap 139 - 104 - 21 = 14, RBC x MCV = Hct; eGFR about 44 and 40 by CKD-EPI 2021 for creatinine 1.4 and 1.5 at 58 (stage 3b consistent in PMH, HPI, labs criterion, drug check, key evidence); CHA2DS2-VASc 5 and HAS-BLED 3/2 recomputed; one apixaban dose-reduction criterion; deep 2.1 cm infarct is ELAN moderate (deep MCA branch), so within 48 h is right; 48-hour Holter type, duration, criterion alternative and impression agree; differential matches the results (M1 40-50% below the TOAST 50% threshold). Found no error requiring a change. The anticoagulation decision on a single 45-second AF episode stays an open question as the worker logged. `perfect_agent.py -v` and `case_io.py check` clean.

## Condition audit
Condition auditor, 23 October 2026 (cross-case uniformity pass over all 30 ISCH-STR cases).
- Template carry-over (PATTERNS 4), the worker's FLAGGED own finding, now FIXED: the ECG, echo and Holter values were identical in M01, M02 and M03. `initial_tool_outputs.ecg`: rate 84 (triage HR 87), PR 184 ms, QRS 90 ms, QTc 447 ms, SV1 + RV5 41 mm, interpretation "at 84 bpm". Echo follow-up: LAVI 39 mL/m2 (still mildly dilated), septum 1.2 cm, LVEF 60% in `chambers`, `ejection_fraction` and impression; criterion `action-8-order-echocardiogram` expected evidence updated to LAVI 39 and LVEF 60%. Holter follow-up: average 79 bpm (range 55-121 bpm) in events, findings, impression and `heart_rate_range`. No interpretation, decision or must depends on these values. Both checks clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The I63 category no longer appends mechanism labels ("embolic", "cardioembolic", "lacunar") or the bare label "stroke" (which matched "haemorrhagic stroke" or "stroke mimic"); mechanism labels and code families now sit on the specific codes.
- labels removed: "embolic stroke", "cardioembolic stroke", "lacunar stroke", "lacunar infarct", "stroke"
- codes removed: I63.4, I63.3, I63.2, I63.0, I63.1, I63.8, I63.81, I63.89
- codes added: I63.51
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

Decisions: `plans/ISCH-STR-decisions.md`.

- Echo output: added `echo_type` "TTE" to the stored echocardiogram report (the schema now keeps the field and the MockServer routes TTE/TEE/bubble orders by it; the value was only in `tool_parameters`).
- Secondary prevention must: states that the single 45-second episode meets the 30-second definition of AF and that anticoagulation after stroke does not depend on AF burden (decision OQ4a; AHA/ASA 2021).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although this case contradicts it (diagnosis, history, medications or a stored finding) now get a case-specific report; every other off-pathway order still gets the library normal. No tier, criterion, diagnosis or existing output changed.

- `order_advanced_imaging modality=MR_angiography` -> `followup_outputs[order_mr_angiography]`: MR angiography showing the vessel lesion on the stored CTA.
- `order_advanced_imaging modality=cerebral_angiography` -> `followup_outputs[order_cerebral_angiography]`: catheter angiography showing the vessel lesion on the stored CTA.
- `order_advanced_imaging modality=carotid_duplex` -> `followup_outputs[order_carotid_duplex]`: carotid and vertebral duplex consistent with the stored CTA.
- `order_advanced_imaging modality=transcranial_doppler` -> `followup_outputs[order_transcranial_doppler]`: transcranial Doppler consistent with the stored CTA.
- `order_advanced_imaging modality=perfusion_MRI` -> `followup_outputs[order_perfusion_mri]`: perfusion MRI mirroring the stored CT perfusion.
- `order_echocardiogram echo_type=TEE` -> `followup_outputs[order_tee]`: TEE consistent with the stored echocardiogram.
- `order_echocardiogram echo_type=bubble_study` -> `followup_outputs[order_bubble_study]`: bubble study consistent with the stored echocardiogram.
- `order_advanced_imaging modality=cardiac_MRI` -> `followup_outputs[order_cardiac_mri]`: cardiac MRI consistent with the stored echocardiogram.
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[order_performance_status]`: performance status KPS 60, ECOG 2 for the documented deficits.
- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `followup_outputs[order_gait_and_balance_timed]`: timed gait as on the examination.
- `perform_clinical_assessment assessment_type=cognitive_screen` -> `followup_outputs[order_cognitive_screen]`: baseline cognitive screen as documented in the mental status examination.
- `order_specialized_test test_type=neuropsych_battery` -> `followup_outputs[order_neuropsych_battery]`: neuropsychological battery impaired or not testable, as the documented deficits.
- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: speech and language evaluation reflecting the documented speech and language deficits.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k ISCH-STR` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
