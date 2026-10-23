# ISCH-STR-S02
Reviewer status: R1 none, R2 approved | Approved before this round: yes

Approved case: every change below corrects a real error (pathway order, numbers, guideline, internal contradiction, engineering text) or applies a plan class that the reviewer's notes in sibling cases ruled on.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 799ea64c-2db4-41ee-b333-47fec8c75b2e | FIXED | Plan C16: CTA stays required (an M1 thrombectomy candidate within the window; the MRI/MRA is an optional study that must not delay reperfusion). The must "Adjust contrast use for CKD stage 3a" is replaced by "Proceed with CTA without waiting for creatinine; a prior mild contrast reaction and CKD stage 3a do not justify delaying vessel imaging. Give premedication only if it causes no delay, and have treatment for a reaction at hand." CTA criterion rationale and a key-evidence line state the same. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `followup_outputs` order, `ground_truth.action_criteria` order | Echo, Holter, hypercoagulability panel, apixaban check and literature before the CTA (C1). | FIXED: follow-ups CTA, TTE, Holter, apixaban check, literature; criteria NCCT, labs, ECG, CTA, MRI (optional), echo, monitoring, drug check, literature. Ids kept. |
| D | major | `patient.history_present_illness` | "well within the thrombolytic treatment window" (eligibility verdict, C10). | FIXED: times kept, verdict removed. |
| B | major | `initial_tool_outputs.labs` Chloride 109 | Anion gap 129 - 109 - 24 = -4 (C14). | FIXED: chloride 96 mEq/L (L), gap 9; summary and interpretation updated. |
| B | major | `initial_tool_outputs.mri.findings[0]`, `.impression` | FLAIR "subacute onset (>2 hours)" at 2 h 22 with T1/T2 change and sulcal effacement (C12); impression omitted the acute infarct and asserted chronic small vessel disease and a remote right caudate lacune absent from the findings. | FIXED: DWI-FLAIR mismatch, no T1/T2 change, no mass effect; impression names the acute superior division infarct, the M1/M2 occlusion and no haemorrhage; unsupported chronic findings removed (so no prior infarct needs adding to the history). |
| C | minor | `patient.neurological_exam.additional`, `.mental_status` | NIHSS 16 not itemised; complete right hemianopia reported together with visual extinction in the same field (untestable), and a superior division infarct does not explain a complete hemianopia; LOC questions not scoreable from "not oriented to date". | FIXED: right inferior homonymous quadrantanopia (parietal optic radiation), visual and tactile extinction; mental status "cannot state the month or her age"; NIHSS 16 itemised (LOC questions 2, gaze 1, visual 1, face 1, right arm 3, right leg 3, sensory 1, language 2, extinction 2). Total unchanged. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts without a decision; duplicated BP musts; "If no tPA, permissive hypertension up to ~220/110" in a patient who receives IVT (C4, C5). | FIXED: LKW/NIHSS; decision (IVT after BP lowering, EVT for the M1/M2 occlusion without waiting); door-to-needle; one BP must naming 206/105; contrast must (C16); glucose 240 to 140-180; stroke unit telemetry; rate control (she takes no rate-control drug); troponin; sodium 129 recheck; apixaban 5 mg twice daily day 6 to 7 with CHA2DS2-VASc 7 and HAS-BLED 4, no bridge, stop aspirin; warfarin-discontinuation counselling; lipid intensification (LDL 118 on rosuvastatin 20). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Two "below 140/90" prohibitions (C5) in an IVT/EVT case; vague "do not delay anticoagulation indefinitely". | FIXED: removed; BP-threshold, anticoagulation-timing, aspirin-alone and thrombectomy-delay prohibitions. |
| C | minor | `initial_tool_outputs.labs` Troponin I 0.05 (H); ECG 106 bpm, HR 114 | Abnormal results without action (C14). | FIXED: troponin and rate-control musts. |
| D | major | `initial_tool_outputs.ct` | NCCT template management text (C11). | FIXED: canonical impression with ASPECTS 10; "No hyperdense vessel sign" observation added. |
| B | major | `followup_outputs[0]` (CTA) | `contrast_used` false; impression omitted the occlusion and said "for procedural planning". | FIXED: contrast true; impression opens with the distal M1 occlusion extending into the superior M2 division; arch variant stated without management wording. |
| B | minor | `initial_tool_outputs.ecg.findings` | "Left atrial enlargement by P-terminal force criteria" in atrial fibrillation (no P waves). | FIXED: finding removed. |
| B | minor | `followup_outputs[1]` (TTE) | "Abnormal values: ... (H)" impression (C11); no `echo_type`. | FIXED: numbered echo impression (LVEF 58%, LVH, grade II diastolic dysfunction, LAVI 42 moderate, moderate MR, TR 2.9 m/s, trivial effusion); `tool_parameters.echo_type` TTE. |
| B | major | `followup_outputs[2]` (Holter) | 48-hour recording labelled `holter_24h`; no admission timing (C2). | FIXED: `monitor_type` and `tool_parameters` holter_48h; opens "Recorded on the stroke unit after admission, 48 hours."; criterion alternatives holter_48h, holter_24h, telemetry. |
| B | major | `followup_outputs[3]` (apixaban check) | Creatinine quoted as 1.4 (labs 1.3); dosing advice placed in `contraindications`; glipizide hypoglycaemia note irrelevant to apixaban. | FIXED: contraindications empty (none exists); dose criteria with her real values in warnings; aspirin interaction; her other medicines listed; bruising on warfarin addressed. Criterion recommended (C7), after monitoring. |
| C | major | `followup_outputs[4]` (literature) | ELAN timing misstated (48 h "minor", 6-7 d "moderate"); a fabricated ESO 2023 "Klijn" NIHSS rule with day 12-14; superseded 2019 guidance. | FIXED: ELAN (Fischer, NEJM 2023) stated correctly and OPTIMAS (Werring, Lancet 2024); general summary. Criterion optional, last, `required_arguments` {}. |
| B | minor | removed hypercoagulability follow-up | Orphan thrombophilia panel (C9). | FIXED: deleted. |
| A | minor | `ground_truth.action_criteria`, `sequence_constraints`, `stop_rule`, `avoided_actions` | Label = rationale, duplicate `[AHA_ASA_2019]`, free-text citation, hard NCCT-to-drug-check constraint, allowance 0 (C17, 3.3, 3.4). | FIXED: distinct labels/rationales, case-specific evidence, `[AHA_ASA_Stroke_2026]`; soft NCCT before CTA, CTA before echo, CTA before monitoring; stop rule NCCT, labs, ECG, CTA; allowance 1. |
| C | minor | `ground_truth.differential` | Hypertensive ICH left "low" after CT excluded it. | FIXED: very_low; key features tied to the stored results. |
| E | minor | `ground_truth.key_clinical_evidence` | Engineering lines and generic template pearls (C17). | FIXED: case-specific evidence; AHA/ASA 2026 sequencing line kept. |

## Changes, in one paragraph a physician can read before re-reviewing

The case keeps its story (left-handed woman, AF off warfarin for 4 months, distal left M1 occlusion into the superior M2 division, BP 206/105, CKD 3a, mild contrast reaction) and now states the acute decision: lower BP below 185/110, give IV thrombolysis at 2 hours 22 minutes (INR 1.1), and proceed to thrombectomy without waiting, with CTA obtained without waiting for creatinine despite the mild contrast reaction (premedication only if it costs no time). The work-up runs NCCT, labs, ECG, CTA, then TTE, stroke-unit monitoring and the apixaban review; the thrombophilia panel is gone and literature is optional. Fixes to the data: chloride 96 (anion gap 9), MRI hyperacute (DWI-FLAIR mismatch) with an impression that names the infarct and no unsupported chronic findings, CTA contrast recorded with the occlusion first in the impression, P-terminal force removed from an AF ECG, the 48-hour Holter labelled as such, and the right visual deficit made a lower quadrantanopia so that visual extinction is testable (NIHSS still 16, now itemised). Secondary prevention: apixaban 5 mg twice daily on day 6 to 7 (CHA2DS2-VASc 7, HAS-BLED 4), aspirin stopped, counselling on her warfarin discontinuation, and lipid intensification; troponin, rate control, glucose and sodium are addressed.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[AHA_ASA_Stroke_2026]` used throughout (plan section 5.1).
- Synonym list includes "lacunar stroke"/"lacunar infarct" for a cortical cardioembolic infarct (plan section 5.3 owner).

## Open questions for Andrea (judgment calls you could not settle)

- The visual deficit was changed from a complete right hemianopia to an inferior quadrantanopia in an approved case, because a complete hemianopia makes the recorded visual extinction untestable and fits the superior division infarct poorly. If R2 prefers to keep the hemianopia, the visual extinction must go instead (item 11 becomes 1, visual 2, total unchanged at 16).
- ELAN category: the DWI lesion spans several cortical branches of the superior division, which I classified as major (day 6 to 7). A reader who treats the superior division as one cortical branch would call it moderate (within 48 hours).

## Verification
Adversarial verifier, 23 October 2026. Approved case: read the log, the patient-block diff against HEAD and the whole final case.

Checked: note 799ea64c (C16 must, CTA rationale and key evidence; no CKD prohibition left); the patient-block changes are limited to the HPI eligibility verdict, the NIHSS itemisation, the quadrantanopia replacing a hemianopia that made the recorded visual extinction untestable, and "cannot state the month or her age"; NIHSS 16 recounted (questions 2, gaze 1, visual 1, face 1, arm 3, leg 3, sensory 1, language 2, extinction 2); anion gap 129 - 96 - 24 = 9; CHA2DS2-VASc 7 (heart failure, hypertension, age 65 to 74, diabetes, stroke 2, female sex); HAS-BLED 4 (uncontrolled hypertension, stroke, age, aspirin; creatinine 1.3 does not meet the renal item); apixaban standard dose (age 68, creatinine 1.3); BP, glucose, sodium, rate-control and troponin musts match the stored values; prohibitions do not contradict the musts; order, tiers, constraints and stop rule per plan.

Found and fixed:
- `initial_tool_outputs.labs` CBC: MCV 90.1 is not derivable from Hct 37.8 / RBC 3.87 (= 97.7). MCV set to 97.7 (normal; MCHC 32.3); the low RBC flag stands. Pre-existing arithmetic error, corrected as a real error in an approved case.
- `required_recommendations[10]`: "prior stroke" in the HAS-BLED reasons read as a previous stroke; now "this stroke".

`perfect_agent.py -v` passes; `case_io.py check` is clean for this case.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The I63 category no longer appends mechanism labels ("embolic", "cardioembolic", "lacunar") or the bare label "stroke" (which matched "haemorrhagic stroke" or "stroke mimic"); mechanism labels and code families now sit on the specific codes.
- labels removed: "lacunar stroke", "lacunar infarct", "stroke"
- codes removed: I63.5, I63.3, I63.2, I63.0, I63.1, I63.8, I63.81, I63.89
- codes added: I63.41
- `case_io.py validate` OK; `perfect_agent.py` passes.
