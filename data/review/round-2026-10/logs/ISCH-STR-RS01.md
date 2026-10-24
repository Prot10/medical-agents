# ISCH-STR-RS01
Reviewer status: R1 none, R2 approved | Approved before this round: yes

Approved case: every change below corrects an error (R2's six notes, or a defect class the plan assigns to all 30 cases); correct prose was left alone.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 0bc84371-e88e-42f8-8db0-ec94169413e5 | FIXED | Decision must (`ground_truth.assessment.required_recommendations[1]`): IVT given and thrombectomy for the left M1 occlusion (NIHSS 16, pre-stroke mRS 0, ASPECTS 10, within 6 hours), without waiting for the response to IVT; BP must includes the post-recanalization floor; prohibition "Do not delay thrombectomy to observe the response to IV thrombolysis"; `key_clinical_evidence[1]` states the class 1 indication. Pre-stroke mRS 0 added to `patient.neurological_exam.additional` (independent, lives alone) so the criterion is checkable. |
| d923cc86-8992-4e53-9234-5635dbccafce | FIXED | `followup_outputs[0].output.impression` (CTA) opens with "Complete occlusion of the proximal left M1 segment..."; the generator fix is in CENTRAL. |
| dc0e0aee-915f-4ad2-941d-3f4c96c3eefd | FIXED | Anticoagulation must (`required_recommendations[7]`): apixaban 5 mg twice daily with CHA2DS2-VASc 7 (hypertension, age 65 to 74, diabetes, female sex, stroke 2, vascular disease from the carotid plaque, as the reviewer counted) and HAS-BLED 4 (stroke, bleeding history counting the gingival bleeding, age over 65, aspirin); timing by infarct size (major infarct on the DWI, so day 6 to 7 per ELAN, within 48 hours if the 24-hour post-thrombectomy imaging shows only a minor or moderate final infarct); no heparin bridge; stop aspirin. |
| eea99434-9e3e-4f83-8aeb-315349b70086 | FIXED | `patient.clinical_history.past_medical_history[7]` added: "Old right basal ganglia lacunar infarct seen on previous brain imaging; no known prior stroke or TIA". `initial_tool_outputs.mri.impression` no longer asserts "Chronic small vessel ischemic disease" (no white matter change is described). `key_clinical_evidence[6]` explains the recurrence and the CHA2DS2-VASc points. |
| 22f804cf-b35c-4afd-8295-f118ccea8c2a | FIXED | Rate-control must (`required_recommendations[5]`): up-titrate diltiazem or add a beta-blocker cautiously, avoiding hypotension, with the perfusion reason the reviewer gave. Holter impression no longer judges rate control (management). |
| 3c9586d9-8055-487a-8356-f00cfaf365c6 | FIXED | Troponin must (`required_recommendations[6]`, canonical C14 text: demand ischaemia from rapid AF, does not delay reperfusion); ECG criterion rationale names the troponin; `key_clinical_evidence[8]`. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.neurological_exam.cranial_nerves` | "Rightward gaze preference" in a left MCA infarct; a destructive left hemispheric lesion deviates the eyes to the left (C15). | FIXED: "Leftward gaze preference; gaze to the right is only partially overcome on oculocephalic maneuver". |
| C | major | `patient.neurological_exam.additional`, `.mental_status`, `.motor`, `.cranial_nerves` | NIHSS 16 not derivable from the exam (C13): no dysarthria documented, item 1b ambiguous, MRC 1/5 arm could score 4, field cut grade unstated. | FIXED: exam made unambiguous for the stated total: states age but not month (1b 1), partial right homonymous hemianopia (1), arm and leg fall to the bed with no effort against gravity (3 each), mild-to-moderate dysarthria (1); itemised "NIHSS 16 (LOC questions 1, gaze 1, visual fields 1, facial palsy 2, right arm 3, right leg 3, sensory 1, language 2, dysarthria 1, extinction and inattention 1)". |
| B | minor | `patient.clinical_history.past_medical_history[2]` | Diabetes "diet-controlled" while she takes metformin 500 mg twice daily. | FIXED: "on metformin". |
| D | major | `initial_tool_outputs.ct.additional_observations[0]`, `.impression` | NCCT template management text ("does not justify withholding treatment", "Nothing on this study contraindicates intravenous thrombolysis...") (C11). | FIXED: canonical impression "1. No acute intracranial haemorrhage. 2. No established infarct, no hyperdense vessel sign and no mass lesion. ASPECTS 10."; observation reworded. |
| B | major | `initial_tool_outputs.mri.findings[0].signal_characteristics`, `.mass_effect`, `.impression` | FLAIR "suggesting onset greater than 3 hours" at 2 h 52 with T1 hypointensity and T2 hyperintensity (C12); impression omitted the M1 occlusion found by its own MRA. | FIXED: faint FLAIR and T2 change less conspicuous than DWI, no T1 change, minimal sulcal effacement; numbered impression names the infarct, the M1 occlusion, no haemorrhage and the old lacune. |
| B | major | `followup_outputs[0]` (CTA) `contrast_used` | false for a CT angiogram (C11). | FIXED: true. |
| B | minor | `followup_outputs[1]` (TTE) | Impression "Abnormal values: LVEF 52% (H)..." flagged a low-normal LVEF high; LAVI without unit; one finding line (C11); no `echo_type`. | FIXED: real numbered impression (concentric LVH, LVEF 52 percent, mildly dilated LA, mild-to-moderate MR, aortic sclerosis, appendage not seen); findings by structure; `tool_parameters.echo_type` TTE. |
| D | minor | `followup_outputs[2]` (Holter) | Rate-control judgement in the impression; no admission timing (C2); heart-rate range only average. | FIXED: opens "Recorded on the stroke unit after admission, 24 hours."; min 58 and max 142 added from the stored events; `tool_parameters.monitor_type` holter_24h; criterion alternatives holter_24h, holter_48h, telemetry. |
| C | major | `followup_outputs[3]` (drug check), criterion `action-7-check-drug-interactions` | Alteplase checklist whose `contraindications` listed non-contraindications; metformin "held for contrast" claim; ignored the apixaban she needs with diltiazem and aspirin (C7). | FIXED: rewritten for apixaban against her list (diltiazem modest exposure increase, stop aspirin, no interaction with the rest, dose-reduction criteria not met, sulfonamide allergy irrelevant, aspirin not an IVT contraindication); trigger `check_apixaban_diltiazem_aspirin`; criterion recommended with `drug` apixaban, placed after echo and monitoring. |
| B | minor | removed `followup_outputs` hypercoagulability panel | Orphan thrombophilia panel received by no criterion, not indicated in AF cardioembolism (C9). | FIXED: deleted. |
| C | major | `followup_outputs[4]` (literature), criterion `action-6-search-medical-literature` | Recommended literature step; a fabricated source ("Goshua G, Endotheliopathy and platelet dysfunction as hallmarks of fatal COVID-19, JAMA Intern Med 2020"; the real Goshua 2020 paper is in Lancet Haematology with another title); summary beyond the sources (C8). | FIXED: that result deleted; Merkler 2020 and Xie 2022 kept; summary general. Criterion optional, last, `required_arguments` {}. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts (generic LKW, "verify anticoagulation status; INR/anti-Xa needed" after warfarin, prolonged monitoring for paroxysmal AF in known AF, "per mechanism") (C2, C4, C6). | FIXED: case-specific LKW/NIHSS, decision, dose and door-to-needle, BP (182/98 is within 185/110; below 180/105 for 24 h; no systolic target below 140 after recanalization), stroke unit telemetry, rate control, troponin, apixaban, adherence, lipid intensification (LDL 138 on rosuvastatin 20 with carotid plaque and diabetes). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "below 140/90" prohibition in a case that receives IVT and EVT (C5); generic large-infarct anticoagulation prohibition. | FIXED: 140/90 removed; anticoagulation prohibition rewritten to the 24-hour and imaging rule with no bridging; thrombectomy-delay prohibition added. |
| C | minor | `ground_truth.differential[0]` | Large artery atherosclerosis left moderate after CTA showed 30 and 40 percent plaque (ruling 7). | FIXED: low, with the CTA data; haemorrhage and glucose entries tied to the stored results. |
| E | minor | `ground_truth.key_clinical_evidence` | Three "Off-pathway modality" engineering lines, the July 2026 tier line, a normal-sinus-rhythm pearl in an AF case, DAWN/DEFUSE 6 to 24 hour pearl at 2 h 52, "post-COVID AF" (AF is 5 years old) (C17). | FIXED: case-specific evidence (window, EVT indication, localisation, hyperacute imaging, silent infarct, rate and troponin, COVID context); TOAST, AF-risk, DOAC and AHA/ASA 2026 sequencing lines kept. |
| A | minor | `ground_truth.action_criteria`, `sequence_constraints`, `stop_rule` | CTA after echo, Holter, literature and drug check (C1); labels identical to rationales; `[AHA_ASA_2019]` and free-text citations; echo and Holter required; hard NCCT-to-drug-check constraint; allowance 0. | FIXED: order NCCT, labs, ECG, CTA, MRI (optional), echo, monitoring (both recommended), drug check, literature (optional); ids kept; distinct labels and rationales; keys `[AHA_ASA_Stroke_2026]`, `[AHA_ASA_2021_secondary]`; soft NCCT before CTA, CTA before echo, CTA before monitoring; stop rule NCCT, labs, ECG, CTA; `max_additional_actions` 1; avoided actions recited with the 2026 key. |
| E | minor | `initial_tool_outputs.labs.abnormal_values_summary` | "HbA1c 7.2% (suboptimally controlled diabetes)" interpretive. | FIXED: factual flags only; values unchanged. |

## Changes, in one paragraph a physician can read before re-reviewing

The clinical story is unchanged: a 68-year-old woman with AF who stopped warfarin 6 months ago, last known well 09:00, arriving at 11:52 with a left M1 occlusion. The exam now matches the lesion (leftward gaze preference) and sums to the stated NIHSS 16 item by item; her diabetes is on metformin and the old right basal ganglia lacune is in the history as a silent prior infarct. Reports were corrected: canonical NCCT (ASPECTS 10, no management text), MRI with only faint FLAIR change at under 3 hours and an impression naming the M1 occlusion without the unsupported small vessel line, CTA with contrast recorded and the occlusion first in the impression, a real TTE impression, and a Holter report recorded on the stroke unit without management. The work-up reads NCCT, labs, ECG, CTA, then echo, monitoring, the apixaban interaction check (recommended) and an optional COVID literature search; the orphan thrombophilia panel and a fabricated reference are gone. The musts now state IV thrombolysis plus thrombectomy without waiting, door-to-needle under 60 minutes, BP limits, stroke unit telemetry, rate control, repeat troponin, apixaban 5 mg twice daily with CHA2DS2-VASc 7 and HAS-BLED 4 timed by infarct size per ELAN with aspirin stopped and no bridging, adherence support, and intensified lipid lowering.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Generator (R2, d923cc86): CTA impressions omit the principal finding and CTA `contrast_used` is false; the echo template prints "Abnormal values ... (H)" and flags low-normal LVEF (plan section 5.5).
- Citation keys `[AHA_ASA_Stroke_2026]`, `[AHA_ASA_2021_secondary]` (plan section 5.1).
- Synonyms appended to `accepted` include "lacunar stroke" and "lacunar infarct" for a cardioembolic M1 infarct (plan section 5.3 owner).
- EchoReport has no `echo_type` field; set in `tool_parameters` only.

## Open questions for Andrea (judgment calls you could not settle)

- CHA2DS2-VASc 7 counts the carotid bifurcation plaque as vascular disease, as R2 did; under the strict definition (MI, peripheral artery disease, aortic plaque) the score is 6. Either way anticoagulation is indicated.
- HAS-BLED 4 does not count "uncontrolled hypertension": 182/98 is an acute-phase reading, and her chronic control is not documented.
- The PMH line for the old lacune says "seen on previous brain imaging" (plan C10 wording) so that the history does not report the result of this encounter's MRI.

## Verification
Adversarial verifier, 23 October 2026. Approved case: read the log, the diff and the whole final case.
- Notes: 0bc84371, d923cc86, dc0e0aee, eea99434, 22f804cf, 3c9586d9 all FIXED as logged (EVT decision must, CTA impression opens with the M1 occlusion, CHA2DS2-VASc 7 and HAS-BLED 4 itemised, old lacune in the PMH and the small vessel line gone from the MRI impression, rate-control and troponin musts). No note missing.
- Checked: apixaban 5 mg twice daily (age 68, creatinine 0.94, no dose-reduction pair); ELAN "major" is right for a superior-division cortical plus deep MCA infarct; INR 1.0, platelets 218, glucose 172 in the decision must match the labs; anion gap 15, Hct about 3 x Hb; Holter 58 to 142 matches its events; Merkler 2020 (OR 7.6) and Xie 2022 (HR 1.52) are correctly cited.
- Found: the NIHSS itemisation gives facial palsy 2, but the exam still read "Right lower facial droop with forehead sparing", which a reader can score 1 (total 15). Changed `patient.neurological_exam.cranial_nerves` to "Marked right lower facial weakness (near-complete paralysis of the lower face) with forehead sparing." so the stated NIHSS 16 is derivable (C13). No other change; perfect_agent and case_io check clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The I63 category no longer appends mechanism labels ("embolic", "cardioembolic", "lacunar") or the bare label "stroke" (which matched "haemorrhagic stroke" or "stroke mimic"); mechanism labels and code families now sit on the specific codes.
- labels removed: "lacunar stroke", "lacunar infarct", "stroke"
- codes removed: I63.5, I63.3, I63.2, I63.0, I63.1, I63.8, I63.81, I63.89
- codes added: I63.41
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

Decisions: `plans/ISCH-STR-decisions.md`.

- Echo output: added `echo_type` "TTE" to the stored echocardiogram report (the schema now keeps the field and the MockServer routes TTE/TEE/bubble orders by it; the value was only in `tool_parameters`).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
