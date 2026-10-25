# ISCH-STR-RS02
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 7eec1867-16a9-40a2-943c-b133ceb449d3 | FIXED | Every "within 14 days" exclusion removed: musts[7] ("recent major surgery as an absolute contraindication ... within 14 days") and prohibitions[5] and [7] deleted; `key_clinical_evidence[5]` ("Recent major surgery is a contraindication to IV tPA") rewritten. Decision must (`required_recommendations[1]`) now withholds IVT on the reviewer's ground: an actively dissected left CCA with opacified false lumen and about 80 percent true lumen stenosis arising near a six-week-old arch graft, treated like aortic dissection; it states that 6 weeks is outside the 14-day exclusion. Prohibitions: "Do not give IV thrombolysis through an actively dissected common carotid artery arising near a six-week-old aortic arch graft" and "Do not justify withholding thrombolysis by the 14-day surgical rule: the operation was 6 weeks (42 days) ago". Drug-check output keeps the correct "outside the 14-day high-risk window". See Open questions. |
| 212fe881-8bf4-422d-8971-03660d1dcb86 | FIXED | Crescendo TIA made explicit: `key_clinical_evidence[0]` (teaching pearl), prohibition "Do not manage recurrent transient deficits in a patient with a known carotid abnormality as outpatient observation", `red_herrings[0]` retargeted to the five attacks managed as outpatient follow-up (field path the HPI). CTA criterion rationale and expected evidence and `key_clinical_evidence[3]` say the CTA confirms and characterises the lesion first seen after surgery. HPI "adjacent to the vascular graft" became "beyond the vascular graft" to agree with the CTA (entry 7 cm distal to the anastomosis). |
| 4e5a5ed6-4e5c-4de3-b114-ba3bccf25371 | FIXED | Thrombectomy must replaced by the plan's canonical text (`required_recommendations[2]`): vascular surgery, cardiothoracic surgery and neurointervention; emergent endarterectomy within 48 hours not beneficial (§4.12, COR 3 No Benefit); stenting if events recur despite antithrombotic therapy. Decision must says thrombectomy is not indicated (no intracranial LVO, inflow limitation); prohibition "Do not perform emergent carotid endarterectomy within 48 hours"; `key_clinical_evidence[4]`. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.neurological_exam` | NIHSS 8 not derivable (C13): the exam supports face 1, arm 2 (3/5 proximal), leg 1, sensory 1, dysarthria 1 (HPI "difficulty speaking clearly"); ataxia limited by weakness scores 0. | FIXED: exam states the drifts, mild dysarthria and ataxia not out of proportion to weakness; "NIHSS 6 (facial palsy 1, right arm 2, right leg 1, sensory 1, dysarthria 1)"; 6 in the LKW must. No threshold depends on it (no LVO). |
| B | minor | `initial_tool_outputs.mri.findings[0].location` | Precentral-only infarct does not explain the right arm and leg sensory loss (PATTERNS 3). | FIXED: lesion includes the adjacent postcentral gyrus (superior division territory); size unchanged. |
| B | major | `initial_tool_outputs.mri.findings[0].signal_characteristics`, `.additional_observations[3]`, `.impression` | FLAIR "suggesting onset beyond 3 hours" at about 3 hours with T1 and T2 change (C12); observation cited the clinical history ("despite history of transient episodes"). | FIXED: faint FLAIR and T2 change less conspicuous than DWI, no T1 change; "No chronic territorial or lacunar infarcts"; numbered impression. |
| D | major | `initial_tool_outputs.ct.additional_observations[0]`, `[4]`, `.impression` | NCCT template management text; a head CT describing "post-surgical appearances of the recent thoracic procedure" (C11). | FIXED: canonical impression with ASPECTS 10; observation 4 "No extra-axial collection and no pneumocephalus". |
| B | major | `followup_outputs[0]` (CTA) `contrast_used`, `findings[0].size`, `findings[2]`, `impression` | `contrast_used` false; size said the dissection runs "from the junction with the aortic arch graft" while the description puts the entry 7 cm distal to it; arch extension not addressed in the impression. | FIXED: contrast true; length about 5 cm from the mid-CCA entry into the proximal ICA; graft finding states no flap or false lumen in the graft or native aorta; numbered impression opening with the dissection. |
| C | major | `followup_outputs[1]` (echo), criterion `action-8-order-echocardiogram` | Criterion required a TEE and its label said "transthoracic"; the stored report was a TTE template ("Abnormal values ... (H)", LAVI without unit, "prosthetic aortic graft ... no paravalvular leak", which applies to valves, not an arch graft). | FIXED: real TEE report (no LA or appendage thrombus, intact septum on saline contrast, arch graft intact without flap, collection or vegetation, LVEF 58 percent); `tool_parameters.echo_type` TEE; criterion recommended, label "transoesophageal". |
| D | minor | `followup_outputs[2]` (Holter) | No admission timing (C2); heart-rate range average only. | FIXED: opens "Recorded on the stroke unit after admission, 24 hours."; min 54, max 108 from the stored events; `tool_parameters.monitor_type` holter_24h; alternatives holter_24h, holter_48h, telemetry. |
| C | major | `followup_outputs[3]` (drug check) | Heparin check silent on his recent bypass heparin exposure (rapid-onset HIT), on the rest of his list and on the antiplatelet alternative (C7). | FIXED: interactions with aspirin (stop while anticoagulated) and the rest of his list; warnings on rapid-onset HIT with repeat platelets at 24 h, the 42-day surgical interval, haemoglobin 12.4, aPTT target without bolus; DAPT with pantoprazole and argatroban as alternatives. Trigger `check_heparin_aspirin_dissection`; criterion recommended, `drug` heparin. |
| B | minor | removed `followup_outputs` hypercoagulability panel | Orphan thrombophilia panel received by no criterion (C9). | FIXED: deleted. |
| C | major | `followup_outputs[4]` (literature) | Fabricated sources: "Defined group, multi-institutional review, Annals of Vascular Surgery 2020" recommending anticoagulation for iatrogenic dissection; "Pham MH ... J NeuroInterv Surg 2019" (the real Pham review is Neurosurgery 2011) (C8). | FIXED: CADISS (Lancet Neurol 2015), TREAT-CAD (Lancet Neurol 2021), Pham 2011 (Neurosurgery 68:856); general summary. Criterion optional, last, `required_arguments` {}. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts: door-to-needle and pre-IVT BP in a patient who is not thrombolysed; prolonged monitoring for paroxysmal AF; "per mechanism"; no dissection antithrombotic or haemodynamic BP must (C4, C6). | FIXED: LKW/NIHSS, decision, surgical discussion, stroke unit telemetry, dissection antithrombotic for 3 months (heparin then oral anticoagulant after events on aspirin, DAPT as alternative, platelets at 24 h), avoid BP lowering (pressure-dependent perfusion across the 80 percent stenosis), atorvastatin 80 mg for LDL 128 with PAD and diabetes. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | 140/90 prohibition (C5); large-infarct anticoagulation template (C6). | FIXED: canonical COR 3 No Benefit prohibition; large-infarct template removed; endarterectomy, crescendo-TIA and IVT prohibitions added. |
| C | major | `ground_truth.differential` | Postoperative cardioembolism "high" and postoperative AF "moderate" after TEE and monitoring exclude them (ruling 7). | FIXED: both low with the excluding results; graft infection and watershed entries tied to the stored data. |
| E | minor | `ground_truth.key_clinical_evidence` | Three "Off-pathway modality" lines, the July 2026 tier line, DAWN/DEFUSE 6 to 24 hour and normal-sinus-rhythm template pearls (C17). | FIXED: case-specific pearls (crescendo TIA, LKW reset, 14-day rule, CTA confirmation, no LVO, haemodynamic BP); TOAST, iatrogenic dissection, co-occurring AF and AHA/ASA 2026 sequencing lines kept. |
| A | minor | `ground_truth.action_criteria`, `sequence_constraints`, `stop_rule` | CTA after echo, Holter, panel, literature, drug check (C1); labels equal rationales; `[AHA_ASA_2019]`, `[Sanna_2014]` and free-text citations; hard template constraint; allowance 0. | FIXED: order NCCT, labs, ECG, CTA, MRI (optional), TEE, monitoring, drug check (recommended), literature (optional); ids kept; distinct labels and rationales; 2026 and 2021 keys; soft NCCT before CTA, CTA before echo and monitoring; stop rule NCCT, labs, ECG, CTA; allowance 1; avoided actions recited with the 2026 key. |
| E | minor | `initial_tool_outputs.labs.abnormal_values_summary`; `metadata.difficulty_rationale` | "LDL 128 (above target)" and similar interpretive flags; rationale named a "recent-surgery tPA contraindication". | FIXED: factual flags (values unchanged); rationale states the real reason IVT is withheld. |

## Changes, in one paragraph a physician can read before re-reviewing

A 70-year-old man 6 weeks after total aortic arch replacement had five transient right hemiparetic episodes in two weeks, managed as outpatient follow-up, and now a persistent deficit since 09:00 (arrival 12:05, NIHSS 6 on the recounted exam). The case now teaches that sequence as a crescendo TIA. The work-up reads NCCT (canonical, ASPECTS 10), labs, ECG, CTA (contrast recorded; left common carotid dissection with opacified false lumen and about 80 percent true lumen stenosis, entry 7 cm beyond the anastomosis, arch graft intact, no intracranial occlusion), then a real TEE report, stroke-unit monitoring and the heparin check; the thrombophilia panel and two fabricated references are gone. The 14-day surgical rule no longer appears as a reason: thrombolysis is withheld for the dissected carotid near the fresh graft, and thrombectomy is not indicated (no LVO). Musts: surgical and neurointerventional discussion (no emergent endarterectomy, stenting if events recur), stroke unit telemetry, anticoagulation for the dissection after events on aspirin (heparin, then oral, aspirin stopped; DAPT as alternative; platelets at 24 hours for rapid-onset HIT), no BP lowering while perfusion depends on the stenosis, atorvastatin 80 mg. Postoperative embolism and AF are low in the differential after TEE and monitoring.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `icd_codes[0]` I97.811 is "intraoperative cerebrovascular infarction during other surgery"; this infarct occurred 6 weeks after surgery from a carotid dissection (I63.x with I77.71, or I97.820 postprocedural infarction following cardiac surgery if the dissection is counted as a surgical complication). Not changed (no reviewer ruling, ruling 3); the label and synonym owner should decide.
- Citation keys `[AHA_ASA_Stroke_2026]`, `[AHA_ASA_2021_secondary]` (plan section 5.1).
- EchoReport has no `echo_type` field; set in `tool_parameters` only.

## Open questions for Andrea (judgment calls you could not settle)

- Plan open question 2 stands: the guideline names aortic arch dissection as the contraindication; here the CTA and TEE show the arch graft intact and the dissection starting 7 cm beyond the anastomosis. The case withholds thrombolysis on R2's reasoning (hazard of a lytic in an actively dissected CCA in continuity with fresh aortic surgery). Please confirm with R2; if not, the decision must becomes "give" and the prohibition goes.
- Anticoagulation (heparin then oral) is chosen over aspirin plus clopidogrel because events recurred on aspirin and TREAT-CAD did not show aspirin non-inferior; both are COR 2a options and the must names DAPT as the alternative.

## Verification
Adversarial verifier, 23 October 2026. Read the log, the diff and the whole final case (large rewrite, NIHSS changed 8 to 6).
- Notes: 7eec1867 (no 14-day claim left as a reason; the two remaining mentions say 42 days is outside it), 212fe881 (crescendo TIA pearl, prohibition, red herring, CTA rationale) and 4e5a5ed6 (surgical discussion must with §4.12 COR 3) are FIXED as logged. No note missing.
- NIHSS 6 recounted from the exam (face 1 on smiling, arm 2 drifting to the bed with effort against gravity, leg 1, sensory 1, dysarthria 1); every NIHSS mention says 6 and no threshold depends on it. Infarct now includes the postcentral gyrus, explaining the sensory loss. CTA, TEE and Holter reports agree with the criteria; CADISS (Lancet Neurol 2015;14:361), TREAT-CAD (Lancet Neurol 2021;20:341) and Pham 2011 (Neurosurgery 68:856) are correct. Differential timing ("4 weeks later") matches the HPI.
- Found: the haemodynamic BP must said "hold amlodipine and losartan if pressure falls", implying the home antihypertensives continue otherwise, while the canonical prohibition (BP 162/88, no reperfusion) says not to start or restart antihypertensives in the first 48 to 72 hours. Changed `required_recommendations[5]` to "hold amlodipine and losartan for the first 48 to 72 hours, and avoid hypotension and dehydration", which agrees with the prohibition and with the pressure-dependent perfusion argument. No other change; perfect_agent and case_io check clean.

## Open questions resolved (24 Oct 2026)

Decisions: `plans/ISCH-STR-decisions.md`.

- Echo output: added `echo_type` "TEE"; strict xfail removed from `test_echo_type_routing.py`.
- ICD code I97.811 (intraoperative infarction) replaced by I63.232 (left carotid stenosis/occlusion, as the other carotid dissection cases); synonyms regenerated (I97.811 entry removed, RS02 added to I63.232+dissection, 'perioperative stroke' and 'postprocedural stroke' retired) (decision X2).
- IVT decision reversed to give: the CTA itself excludes extension into the graft, anastomoses and native aorta, so the aortic arch dissection contraindication R2 invoked does not apply; extracranial dissection and surgery 42 days ago are not contraindications; disabling deficit at about 3 hours, BP 162/88. Changed: decision must, stroke-unit must, antithrombotic must (start after 24-hour imaging), BP must (post-IVT limits without further lowering), prohibitions (removed the no-IVT and the no-reperfusion BP prohibition; 14-day prohibition now forbids withholding IVT; added the 24-hour antithrombotic prohibition), key evidence 2 and 7, difficulty rationale, drug-check criterion evidence and a drug-check warning (decision OQ3a).

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
- `order_advanced_imaging modality=CT_perfusion` -> `followup_outputs[order_ct_perfusion]`: CT perfusion deficit in the infarct territory on the stored MRI.
- `order_advanced_imaging modality=perfusion_MRI` -> `followup_outputs[order_perfusion_mri]`: perfusion MRI deficit in the infarct territory on the stored MRI.
- `order_echocardiogram echo_type=bubble_study` -> `followup_outputs[order_bubble_study]`: bubble study consistent with the stored echocardiogram.
- `order_echocardiogram echo_type=TTE` -> `followup_outputs[order_tte]`: TTE consistent with the stored TEE.
- `order_advanced_imaging modality=cardiac_MRI` -> `followup_outputs[order_cardiac_mri]`: cardiac MRI consistent with the stored echocardiogram.
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[order_performance_status]`: performance status KPS 30, ECOG 4 for the documented deficits.
- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `followup_outputs[order_gait_and_balance_timed]`: timed gait as on the examination.
- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: speech and language evaluation reflecting the documented speech and language deficits.
- `order_body_imaging study=chest_xray` -> `followup_outputs[order_chest_xray]`: chest radiograph: sternotomy and arch graft (arch replacement 6 weeks ago).
- `order_body_imaging study=chest_CT` -> `followup_outputs[order_chest_ct]`: chest CT: arch graft and the left carotid dissection on the stored CTA.
- `order_body_imaging study=chest_abdomen_pelvis_CT` -> `followup_outputs[order_chest_abdomen_pelvis_ct]`: CT chest, abdomen and pelvis: arch graft and sternotomy.
- `order_body_imaging study=mediastinum_CT` -> `followup_outputs[order_mediastinum_ct]`: mediastinal CT: arch graft.
- `order_body_imaging study=chest_CTA` -> `followup_outputs[order_chest_cta]`: chest CTA: arch graft and the left carotid dissection.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k ISCH-STR` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
