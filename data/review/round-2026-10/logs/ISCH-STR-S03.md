# ISCH-STR-S03
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 0a65085d-a1e9-4f73-90ea-47405aec24d8 | FIXED | Plan C16: CTA stays required. Prohibition "Do not give full-dose contrast in CKD without renal protection" removed; canonical must added ("Proceed with CTA without waiting for creatinine; a prior mild contrast reaction and CKD stage 3a do not justify delaying vessel imaging. Give premedication only if it causes no delay, and have treatment for a reaction at hand."). The drug review (`followup_outputs[1]`) states that metformin need not be withheld for contrast at his renal function. CTA criterion rationale and a key-evidence line say the same. |
| d3d1bb91-dfc2-4522-9c4e-d16366e45dda | FIXED | `patient.history_present_illness`: the 09:00 anchor is kept and the caller is his brother ("his brother spoke to him on the phone at approximately 09:00"); the mother's death from stroke stays in the family history. Stale `metadata.case_body_concerns` entry removed. |
| 20b2416f-f0b0-4392-b596-48a725e636b6 | FIXED | `patient.neurological_exam.cranial_nerves`: "Conjugate left gaze deviation present; can cross midline with oculocephalic maneuver" (gaze 1); key evidence states the toward-the-lesion rule. Stale `metadata.case_body_concerns` entry removed. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `followup_outputs` order, `ground_truth.action_criteria` order | Echo, Holter, thrombophilia panel, literature and drug check before the CTA (C1). | FIXED: follow-ups CTA, drug review, TTE, Holter, literature; criteria NCCT, labs, ECG, CTA, MRI (optional), drug review, echo, monitoring, literature. Ids kept. |
| B | major | `initial_tool_outputs.labs` | Female reference ranges in a man (Hb 12.0-16.0, Hct 36-46, RBC 3.92-5.13, creatinine 0.59-1.04: template carry-over); Hct 35.7 with Hb 13.2 (should be about 3 x Hb); anion gap 145 - 97 - 22 = 26 (C14). | FIXED: male ranges (Hb 13.5-17.5, Hct 38.3-48.6, RBC 4.35-5.65, creatinine 0.74-1.35); Hct 39.5, RBC 4.5 (MCV 87.5 consistent); Hb 13.2 now flagged low; chloride 108 (H), gap 15; summary and interpretation updated. |
| B | minor | `patient.history_present_illness` | "mildly hypertensive at 192/104" against vitals 190/100; 192/104 is not mild. | FIXED: "His blood pressure was 190/100 mmHg." |
| B | minor | `patient.clinical_history.medications` (warfarin) | Listed with a daily frequency although stopped. | FIXED: frequency "not taken; self-discontinued 3 weeks ago". |
| C | minor | `patient.neurological_exam.additional`, `.mental_status` | NIHSS 16 not itemised; "right-sided neglect on line bisection" in a dominant hemisphere lesion with a right hemianopia (a hemianopic bisection error is not neglect); LOC questions not scoreable from "not oriented to time". | FIXED: line-bisection neglect removed (tactile extinction kept, item 11 = 1); mental status "states his age but not the month"; NIHSS 16 itemised (LOC questions 1, gaze 1, visual 2, face 2, right arm 3, right leg 3, sensory 1, language 2, extinction 1). Total unchanged. |
| B | major | `initial_tool_outputs.mri` | FLAIR "developing hyperintensity" with T2 change and ventricular compression at 2 h 28 (C12); impression omitted the M1 occlusion and asserted chronic small vessel disease and an old right basal ganglia lacune absent from the findings (C11). | FIXED: DWI-FLAIR mismatch, no T1/T2 change, no mass effect; impression names the acute infarct, the proximal M1 occlusion and no haemorrhage; unsupported chronic findings removed. |
| D | major | `initial_tool_outputs.ct` | NCCT template management text (C11). | FIXED: canonical impression, ASPECTS 10; "No hyperdense vessel sign" observation. |
| B | major | `followup_outputs[0]` (CTA) | `contrast_used` false; impression omitted the occlusion (C11). | FIXED: contrast true; impression opens with the proximal M1 occlusion. |
| C | major | `followup_outputs[1]` (drug review) | The contraindication field held an "INR must be confirmed" instruction; alternatives were thrombectomy and anticoagulation advice (management leakage). | FIXED: warfarin stopped 3 weeks ago (no residual effect; INR decides), his other medicines, metformin with contrast in CKD 3a, bruising warning; contraindications empty (none exists); tenecteplase alternative. Criterion required per plan C7, placed after the CTA. |
| B | minor | `followup_outputs[2]` (TTE) | "Abnormal values: ... LVEF 38% (H)" impression; LV thrombus, the question the case itself raises, not reported. | FIXED: numbered impression (LVEF 38% global hypokinesis, LVH, no LV thrombus, LAVI 42 with spontaneous echo contrast, moderate MR, RV mildly dilated, trace effusion); finding "No left ventricular apical thrombus seen"; `tool_parameters.echo_type` TTE. |
| D | minor | `followup_outputs[3]` (Holter) | Impression attributed NSVT to "underlying cardiomyopathy" (cross-modality) and judged rate control; 218 PVCs (0.2%) called "frequent"; no admission timing (C2). | FIXED: "Recorded on the stroke unit after admission, 24 hours."; burden, rates, NSVT and PVCs (occasional) only; `tool_parameters.monitor_type` holter_24h; alternatives holter_24h, holter_48h, telemetry. |
| C | major | `followup_outputs[4]` (literature) | ELAN timing misstated; a JACC 2020 "Yao X" citation that cannot be verified; superseded 2019 timing. | FIXED: ELAN and OPTIMAS stated correctly; general summary. Criterion optional, last, `required_arguments` {}. |
| B | minor | removed hypercoagulability follow-up | Orphan thrombophilia panel (C9). | FIXED: deleted. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts without a decision; diagnostic acts as musts ("Evaluate for concurrent LV thrombus on echocardiography", "Assess thrombectomy eligibility"); vague DOAC renal dosing (C4, C6). | FIXED: LKW/NIHSS; decision (IVT after BP lowering with INR 1.2; EVT for the M1 occlusion without waiting); door-to-needle; BP must (190/100); contrast must; stroke unit telemetry; rate control with carvedilol; troponin (0.08); apixaban 5 mg twice daily day 6 to 7, CHA2DS2-VASc 5, HAS-BLED 2, no bridge; adherence counselling; lipid intensification (LDL 139 on rosuvastatin 20). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "below 140/90" (C5), CKD contrast prohibition (C16), "Do not delay anticoagulation indefinitely". | FIXED: removed; BP threshold, anticoagulation timing, thrombectomy delay, and no diltiazem or verapamil in HFrEF added. |
| C | major | `ground_truth.differential` | LV thrombus left "high" although the work-up is meant to look for it. | FIXED: echo now reports none, so LV thrombus is low with the reason; others tied to stored results. |
| A | minor | criteria labels, citations, constraints, stop rule | Label = rationale, duplicate `[AHA_ASA_2019]`, free-text citation, hard template constraint, allowance 0 (C17, 3.3, 3.4). | FIXED: distinct labels, case-specific evidence, `[AHA_ASA_Stroke_2026]`; soft NCCT before CTA, CTA before echo and monitoring; stop rule NCCT, labs, ECG, CTA, drug review; allowance 1. |
| E | minor | `ground_truth.key_clinical_evidence`, `metadata.clinical_pearls[3]`, `metadata.difficulty_rationale` | Engineering lines, template pearls, ELAN timing misstated in the pearl. | FIXED: case-specific evidence; pearl states ELAN timing correctly; rationale names the warfarin and contrast questions. |

## Changes, in one paragraph a physician can read before re-reviewing

The story stands (55-year-old man, AF with warfarin stopped 3 weeks ago for bruising, HFrEF, CKD 3a, mild contrast reaction, proximal left M1 occlusion at 2 hours 28 minutes), with the 09:00 anchor now a call with his brother and the gaze deviation toward the lesion (left). The NIHSS stays 16 and is itemised; the line-bisection "neglect" was removed because a right hemianopia, not neglect, explains a bisection error in a dominant lesion. Labs now use male reference ranges, Hct 39.5 matches Hb 13.2, and chloride 108 gives a normal anion gap. NCCT is a clean normal report (ASPECTS 10); MRI is hyperacute (DWI-FLAIR mismatch) and names the occlusion; CTA records contrast and opens with the M1 occlusion; the echo reports LVEF 38% without LV thrombus. The work-up runs NCCT, labs, ECG, CTA, the drug review (required: warfarin no longer active, INR 1.2), then echo and monitoring. Musts: lower BP from 190/100, IV thrombolysis, thrombectomy without waiting, CTA without delay despite CKD and the contrast reaction, telemetry, carvedilol rate control (no diltiazem or verapamil in HFrEF), repeat troponin, apixaban 5 mg twice daily on day 6 to 7, adherence counselling and lipid intensification.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[AHA_ASA_Stroke_2026]` used throughout (plan section 5.1).
- Generator: CBC and creatinine female reference ranges were applied to a male patient here; worth a condition-wide check of `reference_range` against `demographics.sex`.

## Open questions for Andrea (judgment calls you could not settle)

- The drug review is required per plan C7 (warfarin listed, stopped 3 weeks ago). One could argue the INR in the core labs already settles eligibility and the review is only recommended; I followed the plan.

## Verification
Adversarial verifier, 23 October 2026. Read the log, the diff and the whole final case.

Checked: note d3d1bb91 (09:00 call now with his brother; mother's stroke stays in the family history), note 20b2416f (left gaze deviation, gaze 1), note 0a65085d (C16 must; CKD prohibition gone; metformin and contrast correctly stated for eGFR 30 or more); male reference ranges, Hct 39.5 against Hb 13.2, MCV 87.5 against Hct/RBC, anion gap 15; NIHSS 16 recounted (questions 1, gaze 1, visual 2, face 2, arm 3, leg 3, sensory 1, language 2, extinction 1 tactile only, coherent with the hemianopia); CHA2DS2-VASc 5 and HAS-BLED 2; IVT with INR 1.2 after warfarin stopped 3 weeks ago; drug review required and placed after the CTA (plan C7); no diltiazem or verapamil in HFrEF; LV thrombus lowered after the echo shows none.

Found and fixed:
- `patient.history_present_illness`: "brought to the emergency department by his daughter" contradicted the same paragraph (the daughter called 911 and EMS transported him). Now "brought to the emergency department by ambulance".
- `initial_tool_outputs.mri.findings[0]` and `.impression`: the infarct was confined to frontal, precentral, parietal cortex and insula with borders "superior division" territory, which does not explain the complete right homonymous hemianopia scored as visual 2 (a deficit no lesion explains, PATTERNS 3; the worker removed the same mismatch in S02). With a proximal M1 occlusion and no M2 filling, the location now reads "left parietal lobe including the deep parietal white matter" and the borders "left MCA vascular territory"; the impression says the same. Size and all other findings unchanged.
- `required_recommendations[8]`: HAS-BLED reason "prior stroke" now "this stroke".

`perfect_agent.py -v` passes; `case_io.py check` is clean for this case.

## Condition audit
Condition auditor, 23 October 2026 (cross-case uniformity pass over all 30 ISCH-STR cases).
- Template carry-over (PATTERNS 4): the 24-hour Holter repeated S02's average ventricular rate and range (92 bpm, 58-134 bpm). Now 97 bpm (range 64-138 bpm) in events, findings, impression and `heart_rate_range`; criterion `action-9-order-cardiac-monitoring` expected evidence "average 97 bpm". Consistent with the arrival rate of 108 and daytime rates above 110 bpm; the rate-control must quotes neither number.
- Echo `chambers` "Left Atrial Volume Index" was the unitless template value "42" (identical in S02, S03, S04). Now "46 mL/m2 (moderately dilated)", and the impression reads 46 mL/m2; "moderately dilated" in the criterion and key evidence still holds. Both checks clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The I63 category no longer appends mechanism labels ("embolic", "cardioembolic", "lacunar") or the bare label "stroke" (which matched "haemorrhagic stroke" or "stroke mimic"); mechanism labels and code families now sit on the specific codes.
- labels removed: "lacunar stroke", "lacunar infarct", "stroke"
- codes removed: I63.5, I63.3, I63.2, I63.0, I63.1, I63.8, I63.81, I63.89
- codes added: I63.41
- `case_io.py validate` OK; `perfect_agent.py` passes.
