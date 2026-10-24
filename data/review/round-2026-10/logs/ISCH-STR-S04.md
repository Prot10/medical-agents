# ISCH-STR-S04
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 5f9d3088-245e-4621-9be3-27a515be9e0a | FIXED | `patient.history_present_illness` (EMS "left gaze preference") and `patient.neurological_exam.cranial_nerves` ("Conjugate left gaze deviation; able to cross midline briefly with oculocephalic maneuver"; the contradictory "forced" removed, gaze item 1). Key evidence states the toward-the-lesion rule. Stale `metadata.case_body_concerns` entry removed. |
| 3f611291-2e78-48d2-82a3-183c423e4455 | FIXED | Must: "Lower blood pressure below 185/110 mmHg (196/111 on arrival) with IV labetalol or nicardipine before IV thrombolysis, then keep it below 180/105 mmHg for 24 hours; after successful recanalization do not target systolic blood pressure below 140 mmHg." The decision must makes IVT conditional on it; prohibition "Do not give IV thrombolysis while blood pressure is 185/110 mmHg or higher". Treatment is a must, not a tool action (ruling 4). |
| ec9af643-86d5-4252-a25e-43b65e25c514 | FIXED | Criterion `action-7-check-drug-interactions` now asks for the DOAC review (label, rationale and expected evidence about agent, dose and timing, no longer "tPA contraindications"), required per plan C7, placed after monitoring. Output `followup_outputs[3]` rewritten: contraindications list the timing restriction (not within 24 h of IVT, not before imaging excludes haemorrhagic transformation, day 6 to 7 for a major infarct by ELAN) and active bleeding; warnings give the dose criteria with her age and creatinine, the epistaxis and HAS-BLED 4 with the modifiable factors; her actual medicines; alternatives corrected (dabigatran dose wording, LAA occlusion only if anticoagulation proves impossible). The prohibition on early full-dose anticoagulation is rewritten to the same timing. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `followup_outputs` order, `ground_truth.action_criteria` order | Echo, Holter, thrombophilia panel, literature and drug check before the CTA (C1). | FIXED: follow-ups CTA, TTE, Holter, apixaban review, literature; criteria NCCT, labs, ECG, CTA, MRI (optional), echo, monitoring, drug review, literature. Ids kept. |
| B | major | `initial_tool_outputs.labs` Chloride 94 | Anion gap 138 - 94 - 25 = 19 (C14). | FIXED: chloride 100, gap 13; summary and interpretation updated. |
| B | minor | `initial_tool_outputs.labs` RBC 4.79 | MCV 79.3 inconsistent with Hct 38.9 / RBC 4.79 (= 81.2). | FIXED: RBC 4.9 (MCV 79.4); the low MCV is kept and now has an action (iron studies) given the recurrent epistaxis. |
| C | minor | `patient.neurological_exam.additional`, `.mental_status` | NIHSS 19 not itemised; "right hemineglect on visual field testing" in a patient with a complete right hemianopia (not testable) and a dominant lesion. | FIXED: neglect sentence removed (tactile extinction kept, item 11 = 1); mental status "cannot state the month or her age"; NIHSS 19 itemised (LOC questions 2, gaze 1, visual 2, face 2, right arm 4, right leg 3, sensory 2, language 2, extinction 1). Total unchanged. |
| B | major | `initial_tool_outputs.mri` | FLAIR "onset greater than 3 hours" at 2 h 22 with T2 change and ventricular effacement (C12); impression omitted the M1 occlusion and asserted chronic small vessel disease absent from the findings (C11). | FIXED: DWI-FLAIR mismatch, no T1/T2 change, no mass effect; impression names infarct, M1 occlusion, no haemorrhage. |
| D | major | `initial_tool_outputs.ct` | NCCT template management text (C11). | FIXED: canonical impression, ASPECTS 10; "No hyperdense vessel sign" observation. |
| B | minor | `followup_outputs[0]` (CTA) `impression` | Impression omitted the occlusion (contrast was already true). | FIXED: opens with the left M1 occlusion; plaque and arch atherosclerosis; no dissection. |
| B | minor | `followup_outputs[1]` (TTE) | "Abnormal values: ... (H)" impression (C11); no `echo_type`. | FIXED: numbered impression (LVH, LVEF 55%, grade II diastolic dysfunction, LAVI 42, appendage not seen, moderate MR, RVSP 38); `tool_parameters.echo_type` TTE. |
| D | minor | `followup_outputs[2]` (Holter) | "Suboptimal rate control" judgment; no admission timing (C2). | FIXED: opens "Recorded on the stroke unit after admission, 24 hours."; burden and rates (above 120 bpm for 3.2 h); `tool_parameters.monitor_type` holter_24h; alternatives holter_24h, holter_48h, telemetry. |
| B | major | `followup_outputs[3]` (apixaban review) | "CKD stage 3a" (not in her history: template from S02/S03), "CrCl 48" without a weight, "meets one criterion" naming none, glipizide-falls interaction. | FIXED: rewritten as in note ec9af643; renal dosing stated from age and creatinine only. |
| C | major | `followup_outputs[4]` (literature) | ELAN placed in Lancet Neurology and misstated; superseded 2019 timing; summary "larger infarctions 7-14 days". | FIXED: ELAN (NEJM 2023) and OPTIMAS stated correctly; the ESO 2022 secondary prevention guideline (Dawson) kept with its real title; general summary. Criterion optional, last, `required_arguments` {}. |
| B | minor | removed hypercoagulability follow-up | Orphan thrombophilia panel; her DVT 7 years ago does not make thrombophilia testing relevant to an AF cardioembolic stroke (C9). | FIXED: deleted. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts without a decision (C4, C6); "ENT consult" and "Consider WATCHMAN" phrased loosely. | FIXED: LKW/NIHSS; decision (IVT after BP lowering, EVT for M1 without waiting); door-to-needle; BP; telemetry; rate control (no rate-control drug, RVR on Holter); troponin; glucose 205; apixaban 5 mg twice daily on day 6 to 7 with CHA2DS2-VASc 9 and HAS-BLED 4; bleeding-source must (ENT, iron studies, BP; LAA occlusion only if anticoagulation fails); counselling; lipid intensification (LDL 136 on rosuvastatin 20). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "below 140/90" (C5); "Do not resume warfarin without addressing the underlying bleeding source" implied warfarin as the default. | FIXED: 140/90 removed; BP threshold, thrombectomy delay, anticoagulation timing, no antiplatelet alone or no anticoagulation, no warfarin when a DOAC is suitable. |
| C | minor | `metadata.clinical_pearls[1]` | CHA2DS2-VASc "7 ... age 65-74" for a 78-year-old. | FIXED: 9 (age 75 or more scores 2; aortic arch plaque on CTA counts as vascular disease). |
| A | minor | criteria labels, citations, constraints, stop rule | Label = rationale, duplicate `[AHA_ASA_2019]`, free-text citation, hard template constraint, allowance 0 (C17, 3.3, 3.4). | FIXED: distinct labels, case-specific evidence, `[AHA_ASA_Stroke_2026]`; soft constraints; stop rule NCCT, labs, ECG, CTA, drug review; allowance 1. |
| E | minor | `ground_truth.key_clinical_evidence` | Engineering lines and template pearls (C17). | FIXED: case-specific evidence including the ELAN classification of the infarct. |

## Changes, in one paragraph a physician can read before re-reviewing

The case keeps its story (78-year-old woman, AF, warfarin stopped 3 weeks ago for recurrent nosebleeds, left M1 occlusion at 2 hours 22 minutes, BP 196/111) with the gaze deviation corrected to the left and the NIHSS of 19 itemised (the unverifiable "neglect on visual field testing" in a hemianopic field removed). Data fixes: chloride 100 (anion gap 13), RBC 4.9 so the low MCV is arithmetically consistent, hyperacute MRI without the unsupported small vessel disease, CTA and echo impressions that state their findings. The work-up runs NCCT, labs, ECG, CTA, then echo and monitoring, then the required DOAC review. The musts state the decision (lower BP, IV thrombolysis, thrombectomy without waiting), telemetry, beta-blocker rate control, troponin and glucose, apixaban 5 mg twice daily from day 6 to 7 because the infarct is major by ELAN criteria (CHA2DS2-VASc 9, HAS-BLED 4), ENT assessment, iron studies and BP control so anticoagulation can continue, counselling, and lipid intensification. The DOAC review no longer invents CKD 3a and now lists the timing restriction and the bleeding risk.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[AHA_ASA_Stroke_2026]` used throughout (plan section 5.1).
- `Demographics` has no weight field; weight-based dosing (alteplase, tenecteplase, DOAC criteria) cannot be stated exactly in any ISCH case. Consider adding `weight_kg`.

## Open questions for Andrea (judgment calls you could not settle)

- Creatinine 1.3 mg/dL at 78 corresponds to an eGFR of about 42 (CKD G3b), but the history lists no CKD. I did not add a diagnosis; the musts and drug review use the creatinine value only.
- ELAN classification as major (frontal, parietal and insular cortex). If R2 reads this as a single superior division branch (moderate), the start would be within 48 hours.

## Verification
Adversarial verifier, 23 October 2026. Read the log, the diff and the whole final case.

Checked: note 5f9d3088 (left gaze preference in EMS text and exam, gaze 1), note 3f611291 (BP must naming 196/111, decision conditional on it, matching prohibition), note ec9af643 (criterion now a DOAC review, required, after monitoring; output lists her medicines, the timing restriction and active bleeding as contraindications, epistaxis and HAS-BLED); anion gap 13; MCV 79.4 from Hct 38.9 / RBC 4.9; NIHSS 19 recounted (questions 2, gaze 1, visual 2, face 2, arm 4, leg 3, sensory 2, language 2, extinction 1 tactile only); CHA2DS2-VASc 9 (heart failure, hypertension, age 75 or more, diabetes, stroke 2, aortic plaque, female sex); HAS-BLED 4 (uncontrolled hypertension, stroke, bleeding, age); apixaban dose criteria (age 78, creatinine 1.3, weight unknown: at most one); dabigatran and edoxaban wording; rate-control, troponin, glucose and bleeding-source musts; prohibitions consistent with the musts; order, tiers, constraints and stop rule per plan.

Found and fixed:
- `initial_tool_outputs.mri.findings[0]` and `.impression`: borders "left MCA superior division vascular territory" with a frontal, parietal and insular infarct did not explain the complete right homonymous hemianopia (visual 2). Borders now "left MCA vascular territory"; location and impression add "including the deep parietal white matter" (optic radiation pathway), consistent with a proximal M1 occlusion without distal opacification. Size unchanged; ELAN class (major) unchanged.
- `required_recommendations[8]`, `followup_outputs[3].output.warnings[1]`, `metadata.clinical_pearls[1]`: "prior stroke" in the HAS-BLED and CHA2DS2-VASc reasons now "this stroke" (she has no earlier stroke).

`perfect_agent.py -v` passes; `case_io.py check` is clean for this case.

## Condition audit
Condition auditor, 23 October 2026 (cross-case uniformity pass over all 30 ISCH-STR cases).
- Template carry-over (PATTERNS 4): the 24-hour Holter repeated S02/S03's average 92 bpm with minimum 58. Now 88 bpm (range 54-142 bpm) in events, findings, impression and `heart_rate_range`; criterion `action-9-order-cardiac-monitoring` expected evidence "average 88 bpm". The 3.2 hours above 120 bpm and the rate-control must are unchanged.
- Echo `chambers` "Left Atrial Volume Index" was the unitless template "42". Now "45 mL/m2 (moderately dilated)", impression 45 mL/m2. Both checks clean.

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
