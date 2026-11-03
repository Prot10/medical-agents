# ISCH-STR-M01
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 06456aa6-f505-4f49-b220-158a054d7df8 | FIXED | HPI verdict "placing him outside the standard IV tPA window" removed (`patient.history_present_illness`; times kept). New recommended criterion `ct-perfusion-extended-window` (`order_advanced_imaging` modality `CT_perfusion`) and follow-up `request_ct_perfusion` (`followup_outputs[1]`): matched deficit, core 6 mL, Tmax above 6 s 7 mL, mismatch 1 mL, ratio 1.17, so EXTEND criteria are not met. Decision must, wake-up prohibition, key evidence (C3 canonical) and clinical pearl 2 now address both limbs (FLAIR positive; sleep midpoint 02:15, 5 h 25 min before arrival; no LVO so the perfusion limb applies; CTP fails). |
| a46588b0-d665-4f1a-b171-ed189be9ca6e | FIXED | NIHSS recounted from the exam: 9 (gaze 1, visual 1 for visual extinction per the NIHSS item 3 instruction, facial palsy 1, right arm 1, right leg 1, language 1, dysarthria 1, extinction and inattention 2 for visual plus tactile extinction). Exam made explicit so every item is scorable (`patient.neurological_exam.mental_status`, `.cranial_nerves`, `.motor`, `.coordination`, `.additional`); total updated in LKW must and key evidence. The reviewer's orientation point is not scored: NIHSS 1b asks the month and age, not the year, so the exam now states he answers both correctly (1b 0) and the year error stays as a mental-status finding; past-pointing in proportion to weakness scores 0 for ataxia. |
| 9c627e7e-de27-444d-881f-4619f7b832d2 | FIXED | `initial_tool_outputs.labs.panels.BMP` chloride 101 to 91 mEq/L, flagged low; anion gap 125 - 91 - 25 = 9. Abnormal list and interpretation updated. |
| 6feeb306-8789-4d4c-ac6c-7f5c82227d14 | FIXED | `followup_outputs` reordered: CTA, CTP, TTE, Holter, apixaban check, literature; hypercoagulability follow-up removed. `action_criteria` reordered NCCT, labs, ECG, CTA, MRI (optional), CTP, TTE, monitoring, drug check, literature (optional). Soft constraints NCCT before CTA, CTA before CTP, echo and monitoring, monitoring before the anticoagulant check; the template hard NCCT-to-drug-check constraint removed. |
| df9be70d-251c-41d3-9761-664de7040cd6 | FIXED | The "below 140/90" prohibition replaced by the canonical AHA/ASA 2026 COR 3 No Benefit text (BP 183/98, neither IVT nor EVT). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.labs.panels.CBC` | Hb 12.4 with Hct 43.1 (Hct about 3 x Hb expected; RBC x MCV gave 40.6). | FIXED: Hct 37.2% (L), RBC 3.91 (Hct = RBC x MCV), abnormal list and interpretation updated. |
| B | minor | drug-check output | Creatinine 1.52 and eGFR 52 in the drug check vs creatinine 1.4 in the labs; "meets one criterion (creatinine 1.52)". | FIXED: output uses creatinine 1.4 mg/dL (CKD 3a), meets none of the three dose-reduction criteria. PMH "eGFR 52" kept as the baseline value. |
| C | major | drug-check output | Rivaroxaban "eGFR 52 allows full dose" (dosing uses creatinine clearance); warfarin offered as an equal alternative. | FIXED: rewritten per C7: aspirin stop, no other interaction with his list, apixaban 5 mg twice daily dose rationale, no bridging, DOAC alternatives with CrCl dose rules. |
| B | major | `patient.neurological_exam.cranial_nerves` | "extinguishes left visual stimulus on double simultaneous stimulation on the right" and "incomplete rightward gaze on leftward saccades" are garbled for a left hemisphere lesion. | FIXED: right hemifield extinction; incomplete rightward gaze overcome by the oculocephalic maneuver (partial gaze palsy). |
| B | minor | `patient.clinical_history.past_medical_history` | Stocking pinprick loss "consistent with known neuropathy" but no neuropathy in PMH. | FIXED: appended "Diabetic peripheral neuropathy" (index 6, so red herring field_path PMH[5] is unchanged). |
| D | major | `initial_tool_outputs.ct.impression`, `.additional_observations[0]` | NCCT template management text ("does not justify withholding treatment", "Nothing on this study contraindicates intravenous thrombolysis..."). | FIXED: canonical normal impression with ASPECTS 10; "no hyperdense vessel sign" added as an observation. |
| B | major | `initial_tool_outputs.mri.impression` | Impression omitted the acute infarct. | FIXED: numbered impression naming the acute left MCA superior division infarct, no haemorrhagic transformation, MRA finding, Fazekas 2. |
| C | minor | `initial_tool_outputs.mri.findings[0].location` | "superior parietal lobule" is not superior-division territory. | FIXED: precentral and postcentral gyri (posterior frontal and anterior parietal cortex); same wording in the CTP. |
| B | major | `followup_outputs[0]` (CTA) | `contrast_used` false; stenosis "60-70%" straddling the 70% treatment threshold while musts said "60-69%"; "hypoechoic" plaque (ultrasound term) in key evidence. | FIXED: contrast true; stenosis stated as approximately 65% (NASCET, moderate category) in findings, impression, criterion, musts and key evidence; numbered impression with "No large vessel occlusion". |
| B | minor | `followup_outputs[2]` (echo) | "Abnormal values: ... (H)" impression; LAVI without unit; no thrombus statement though the criterion expected one. | FIXED: real TTE impression, unit added, thrombus/vegetation statement, `tool_parameters` echo_type TTE. |
| B | minor | `followup_outputs[3]` (Holter) | Did not state when it was recorded. | FIXED: impression opens "Recorded on the stroke unit after admission, 24 hours.", numbered; criterion alternatives holter_24h, holter_48h, telemetry. |
| C | major | `followup_outputs` (literature) | Cited AHA/ASA 2019 and summarised that FLAIR positivity ends thrombolysis eligibility (one limb only). | FIXED: WAKE-UP, EXTEND (with EXTEND criteria) and AHA/ASA 2026 with full references; general summary; criterion optional, `required_arguments` {} (an exact query string could never match), placed last. |
| C | major | `followup_outputs` (hypercoagulability), criterion `action-5-interpret-labs` | Thrombophilia panel orphan in a 67-year-old with two identified mechanisms; lipid/HbA1c criterion duplicated the admission labs (perfect-agent warning). | FIXED: both removed (C9). |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts (door-to-needle, pre-IVT BP, generic secondary prevention) in a patient not receiving IVT; no decision stated; carotid must with no timing; no statin, risk-factor or hyponatraemia action. | FIXED: LKW/NIHSS must, decision must, stroke-unit telemetry must, apixaban must (CHA2DS2-VASc 5, HAS-BLED 3 after aspirin stops, within 48 h for a moderate infarct, stop aspirin, no bridging), carotid revascularization 2 days to 2 weeks with the COR 3 emergent-CEA statement, statin intensification (ezetimibe added to rosuvastatin 20 mg; rosuvastatin 40 mg avoided with CKD) to LDL below 70, risk factors, sodium evaluation and correction limit. NCCT-first and glucose musts kept. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "Avoid full-dose iodinated contrast in CKD..." contradicts the required CTA; large-infarct anticoagulation prohibition irrelevant (moderate infarct); wake-up prohibition on one limb. | FIXED: CKD prohibition removed; large-infarct prohibition removed; wake-up prohibition rewritten for both limbs. |
| C | minor | `ground_truth.differential` | Lacunar infarct "moderate" despite a 2.8 cm cortical infarct; hyponatraemia (a red herring) not in the metabolic mimic entry. | FIXED: lacunar low with reasons; metabolic mimic entry names sodium 125. |
| E | minor | `ground_truth.key_clinical_evidence` | "Off-pathway modality" lines x3, "Tier per the July 2026 clinical review", CKD "mandates contrast caution". | FIXED: removed or replaced; NIHSS itemisation, C3 wake-up statement, Holter with CHA2DS2-VASc/HAS-BLED, sodium line added. |
| C | minor | `ground_truth.red_herrings[0]` | Sodium 125 called "mild". | FIXED: "moderate". |
| A | minor | all criteria and avoided actions | Free-text citation string, duplicate keys, `[AHA_ASA_2019]`/`[AHA_ASA_2014]`; label identical to rationale. | FIXED: `[AHA_ASA_Stroke_2026]` or `[AHA_ASA_2021_secondary]` (plus `[Sanna_2014]`), one each; rationales give reasons. |
| E | minor | `metadata.difficulty_rationale`, `metadata.clinical_pearls[1]` | "CKD limiting contrast use"; pearl said FLAIR positivity means the window has passed. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The pathway now runs NCCT, core labs, ECG, CTA, then CT perfusion (new, recommended), with MRI optional, then TTE (recommended) and inpatient Holter (required), and the apixaban check last among the required steps; the thrombophilia panel, the separate lipid/HbA1c step and the literature step as a clinical action are gone (one optional literature output with correct WAKE-UP, EXTEND and AHA/ASA 2026 references remains). The HPI keeps the times but no longer concludes eligibility. Both wake-up limbs are addressed: FLAIR is positive, and the new CTP, done 5 h 25 min after the sleep midpoint in a patient without a large vessel occlusion, shows a matched 6 mL core with 1 mL mismatch (ratio 1.17), so no IV thrombolysis; no thrombectomy. The exam was made scorable and the NIHSS is 9 (itemised). Labs: chloride 91 (anion gap 9), Hct 37.2 and RBC 3.91 consistent with Hb 12.4; creatinine 1.4 used everywhere. The CTA reports contrast and a 65% NASCET left ICA stenosis; the MRI and echo impressions name their findings. Musts: LKW and NIHSS, the explicit reperfusion decision, stroke-unit telemetry, apixaban 5 mg twice daily within 48 h with aspirin stopped (CHA2DS2-VASc 5, HAS-BLED 3), left carotid revascularization between 2 days and 2 weeks (emergent CEA not beneficial), ezetimibe added to rosuvastatin 20 mg (40 mg is best avoided with CKD) with escalation if LDL stays at or above 70, risk-factor control with antihypertensives resumed after 48 to 72 h, and evaluation and slow correction of the sodium of 125. The 140/90 prohibition is replaced by the AHA/ASA 2026 COR 3 No Benefit statement, and the CKD contrast prohibition is gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[AHA_ASA_Stroke_2026]`, `[AHA_ASA_2021_secondary]` need the criteria-pack allow-list (plan section 5.1).
- Review UI: show the initial work-up (NCCT, labs, ECG) as numbered steps in criterion order (plan section 5.2).
- `accepted[0]` contains an em dash; left untouched per ruling 3.

## Open questions for Andrea (judgment calls you could not settle)

- NIHSS item 3: I scored the visual extinction 1 under item 3 as the NIHSS instructions direct, and again within item 11; if the panel prefers to score extinction only under item 11, the total is 8.
- CTA stenosis set to "approximately 65%" (was "60-70%") so the carotid decision falls clearly in the 50-69% category; this changes a stored value.
- Plan open question 4: CTP was written to fail EXTEND so the existing "no IVT" story stands.

## Verification
Adversarial verifier, 23 October 2026. Checked: every note id (5) is in the table and each FIXED claim holds in the file (no HPI verdict; CTP follow-up and recommended criterion fail EXTEND with core 6 mL, mismatch 1 mL, ratio 1.17; NIHSS 9 recounted item by item from the final exam and identical in exam, LKW must and key evidence; chloride 91 gives gap 9; CTA first follow-up; COR 3 BP prohibition in place, consistent with the must that resumes amlodipine and losartan after 48 to 72 h). Cross-field: Hct 37.2 = 3 x Hb and = RBC x MCV; creatinine 1.4 everywhere; sleep midpoint 02:15 and 5 h 25 min recomputed; CHA2DS2-VASc 5 and HAS-BLED 4/3 recomputed from the record; apixaban dose criteria correct; carotid 50-69% revascularization claim matches AHA/ASA 2021 (COR 1 with patient factors, perioperative risk below 6%); laterality consistent with a left hemisphere lesion; red-herring field paths resolve; sequence constraints and stop rule reference existing required criteria. Found no error requiring a change. Noted, not changed: the 2.8 cm precentral/postcentral infarct is classed ELAN moderate (apixaban within 48 h); with a 6 mL core this is defensible, but a reader who counts two cortical branches would call it major (day 6 to 7). `perfect_agent.py -v` and `case_io.py check` clean.

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
