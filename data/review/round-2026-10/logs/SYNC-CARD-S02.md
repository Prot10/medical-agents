# SYNC-CARD-S02
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search`, `initial_tool_outputs.drug_interactions.general` | Literature finding and summary equal to the expected_evidence (leak guard failure); drug block was the bare text "Hold AV-nodal blockers", the key of the drug criterion. | FIXED: both deleted; one ESC 2021 pacing / ESC/EACTS 2021 guideline follow-up added last. |
| E | major | `fallback_tool_outputs.literature_search`, `fallback_tool_outputs.drug_interactions.general` | "No directly applicable ... evidence"; "(agent not specified on this case's pathway)". | FIXED: literature fallback deleted; drug fallback is a `medication_list_review` (amlodipine, losartan and tamsulosin lower blood pressure in severe AS; losartan and potassium; metformin dose at eGFR 30-45; cephalosporin allergy and cefazolin). |
| C | major | `action-6-search-medical-literature`, `action-5-check-drug-interactions` | Literature recommended; drug check recommended with no drug while he takes no AV-nodal blocker. | FIXED: literature optional (canonical rationale); drug check optional (plan B) with alternatives amlodipine, losartan and one follow-up each. |
| C | minor | `action-2-interpret-labs` | Pinned CBC, BMP, Mg, troponin; expected_evidence generic. | FIXED: recommended `panels: [BMP]`; expected_evidence K 5.3 on losartan, creatinine 1.8. |
| B | minor | `initial_tool_outputs.labs.panels.BMP` | Sodium 146 with chloride 104 and CO2 23 (gap 19), unexplained hypernatraemia. | FIXED: sodium 140; summary and interpretation updated ("indices suggesting iron deficiency" interpretation removed). |
| B | minor | `patient.vitals.hr` | HR 45 while the ECG escape is 32 bpm and telemetry never exceeds 40. | FIXED: 33. |
| B | major | `initial_tool_outputs.ecg` | "Low-voltage QRS in limb leads" alongside LVH by voltage (contradictory, and an unintended amyloid flag); right axis with an LBBB escape; "increasing risk of polymorphic VT" interpretation. | FIXED: low voltage removed, normal axis, interpretive clause removed. |
| D | minor | `initial_tool_outputs.eeg.limitations` | "a non-epileptic etiology is favored" (cross-modality conclusion). | FIXED: removed. |
| B | major | `followup_outputs` CT, `patient.neurological_exam.additional` | CT reported a right temporal scalp haematoma while the HPI has him landing on his right side and the exam records only hip tenderness; no NG232 criterion. | FIXED: exam states no scalp wound; CT is a normal non-contrast report kept as an off-pathway answer; head CT avoided as waste. |
| B | major | `followup_outputs[0]` (echo) | Lab-style fields, no echo_type, TAPSE, stroke volume, wall motion. | FIXED: full TTE report (Vmax 4.3 m/s, mean 42 mmHg, AVA 0.9 cm2, annular calcification, LVEF 40% global hypokinesis, septum 1.4 / PW 1.3 cm, TAPSE 16 mm, PASP 48 mmHg), no diagnosis sentence. |
| B | major | `followup_outputs[1]`, `action-4-order-cardiac-monitoring` | 24 h Holter during "wheelchair transport" (an inpatient) under a telemetry label pinned to holter_24h; "frequent PVCs, 0.5%" for 186 beats (0.4%). | FIXED: alternatives telemetry, holter_24h, holter_48h; output "Inpatient telemetry, 24 h" with S02's own rates kept (26-40, average 34, 5.8 s pause at 02:18), near-syncope at 28 bpm added; same recording as the fallback. |
| D | minor | `followup_outputs` CMR | "consistent with reactive fibrosis at the conduction system level", "no features of infiltrative cardiomyopathy" interpretations; LVEDV 185 mL called increased. | FIXED: findings-only impression; CMR optional (age 74). |
| C | major | `followup_outputs` tilt and exercise, `avoided_actions` | Tilt performed in severe AS; exercise report "not performed" stored as a result; exercise not avoided. | FIXED: both follow-ups deleted; tilt and exercise test avoided as harm (severe symptomatic AS). |
| H | minor | all `action_criteria[*]` | "ESC 2018 §x", "Locati 2014" citations; rationale equal to label. | FIXED. |
| A | minor | `stop_rule`, `sequence_constraints` | `max_additional_actions: 0`; no constraints. | FIXED: 2; soft ECG before TTE and before monitoring. |
| C | major | `ground_truth.assessment` | No valve-intervention must; "Restage AS on echo" (a scored test) and "Hold AV-nodal blockers" (he takes none); no handling of vasodilators with BP 94/55, of the cephalosporin allergy at device implantation, or of the microcytic anaemia; tilt prohibition (a test). | FIXED: musts are diagnosis (CHB plus severe AS), monitored bed with pacing pads, permanent pacing with CRT or conduction-system pacing considered at LVEF 40%, Heart Team TAVI or SAVR, hold amlodipine and tamsulosin and review losartan, non-cephalosporin device prophylaxis, investigate the microcytic anaemia, driving. Prohibitions: AV-nodal drugs before pacing, vasodilators, discharge before pacing, cephalosporin prophylaxis. |
| C | major | `ground_truth.differential` | VT moderate after telemetry; SSS cited SNRT/EP study (not on the pathway); severe AS "may be under-staged" although the echo stages it. | FIXED: AS moderate (contributing mechanism, staged), VT and SSS low with the telemetry evidence. |
| L | minor | `ground_truth.red_herrings` | field_path without index; data_point not quoted. | FIXED: point to `past_medical_history[1]` and the ECG interpretation with quoted text. |
| E | minor | `ground_truth.key_clinical_evidence`, `metadata` | Tilt-only evidence; difficulty rationale with 4-5 required tools. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The 74-year-old man with exertional syncope on the stairs has complete AV block with a wide LBBB-morphology escape at 32 bpm and severe calcific aortic stenosis (AVA 0.9 cm2, mean gradient 42 mmHg, Vmax 4.3 m/s, LVEF 40%). Required: ECG, TTE and inpatient telemetry (Holter accepted: persistent block, escape 26-40 bpm, near-syncope at 28 bpm, a 5.8 s pause, three brief NSVT runs). BMP is recommended (K 5.3 on losartan, creatinine 1.8; the impossible sodium was corrected). CMR, the medication review and the guideline lookup are optional. Tilt and exercise testing are harm; EEG, brain MRI, CSF and head CT are waste (he did not strike his head; the CT's scalp haematoma was removed and the exam now says so). Musts: diagnosis of both mechanisms, monitored bed with pacing pads, permanent pacing with CRT or conduction-system pacing considered at LVEF 40%, Heart Team TAVI or SAVR, hold amlodipine and tamsulosin and review losartan, non-cephalosporin device prophylaxis, work-up of the microcytic anaemia, driving.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: generic synonyms and R55 still accepted; not hand-edited.
- Plan C3: an off-pathway tilt or exercise order gets the library's normal report; both are avoided as harm here, and the case's tilt report was deleted per the plan.

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. Decisions taken: head CT made waste rather than kept with an unexplained scalp haematoma (no head strike in the history or exam); microcytic anaemia added as a must because it changes the pre-TAVI plan and the case left it unaddressed.
