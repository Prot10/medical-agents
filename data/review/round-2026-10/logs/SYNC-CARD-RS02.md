# SYNC-CARD-RS02
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `action-6-search-medical-literature`, `stop_rule`, literature follow-up | Literature required and in the stop rule; follow-up cited a non-existent Brignole 2018 review title and placed Sheldon 2002 (JACC) in "Neurology". | FIXED: optional, canonical rationale, out of the stop rule; follow-up rewritten from ESC 2021 pacing, ACC/AHA/HRS 2018 bradycardia (pacing mode with LVEF 36-50%) and ESC 2018; placed last. |
| C | major | `action-2-interpret-labs` | Pinned CBC, BMP, Mg, troponin with a generic expected evidence. | FIXED: recommended, `panels: [BMP, troponin]`. Troponin kept as a targeted assay (coronary disease; pembrolizumab four months ago, so immune-checkpoint myocarditis is a reversible cause to exclude); BMP for potassium and CKD 3b. Deviation from plan C (BMP only) explained below. |
| C | major | `action-9-order-ct-scan` (new), `avoided_actions`, CT output | Head CT was avoided as waste although he is 72, lost consciousness and has a right temporal contusion from the fall: NICE NG232 indicates a CT within 8 hours. | FIXED: new recommended criterion; the CT moved from the fallback to `initial_tool_outputs.ct` and rewritten (no haemorrhage or fracture, right temporal scalp swelling, the incidental 3 mm calcified granuloma kept). The CT waste entry removed. |
| B | minor | `initial_tool_outputs.ecg`, monitoring `rhythm_summary` | "Junctional escape" with a wide QRS of LBBB morphology; "junctional/ventricular" in the findings. | FIXED: "wide-complex escape rhythm" in ECG and telemetry; ECG interpretation keeps the measured values. |
| B | major | echo follow-up | No `echo_type`; values without units; wall motion null while the CMR shows basal inferior hypokinesis; no TAPSE, PASP. | FIXED: full TTE report keeping RS02's numbers (LVEF 42%, LVEDD 5.5 cm, LA 4.1 cm, septum 1.3 cm, AVA 1.6 cm2, mean 18 mmHg), with basal inferior hypokinesis, TAPSE 19 mm, PASP 34 mmHg. |
| B | major | `action-4-order-cardiac-monitoring`, monitoring follow-up | Criterion pinned holter_24h with a "Telemetry + Holter" label; no case fallback; no min/max in `heart_rate_range` (plan E). | FIXED: alternatives telemetry, holter_24h, holter_48h; "Inpatient telemetry, 24 h" with RS02's numbers (average 37, 30-44 bpm, 3.8 s pause at 04:15, two 3-beat NSVT runs); same recording as the monitoring fallback. |
| C | minor | CMR follow-up | "No features of sarcoidosis, amyloidosis, or acute myocarditis" and "fibrosis in the conduction system region" are interpretation. | FIXED: impression lists the findings (septal mid-wall LGE with T1 1120 ms, no oedema, inferior subendocardial scar, LVEF 42%). Criterion optional (age 72, plan). |
| C | major | `action-5-check-drug-interactions`, metoprolol follow-up | Required without a drug; output claimed amlodipine adds negative chronotropy (a dihydropyridine has no relevant AV-nodal effect); alternatives "per cardiology evaluation". | FIXED: recommended, `drug: metoprolol`; output in report voice (label contraindication in AV block without a pacemaker, additive hypotension only with amlodipine and lisinopril); medication-list review as the drug fallback. |
| C | minor | tilt follow-up | "qualitative" garbage values, em dash, "VASIS: not applicable" text. | FIXED: cleaned; tilt avoided as waste with a reason naming the hypotension and coronary disease. |
| B | minor | exercise follow-up (new) | A wasted exercise order would have received the library's normal sinus-rhythm report. | FIXED: case-consistent exercise follow-up (complete AV block, escape 37 to 46 bpm, flat BP, stopped early). |
| C | major | `avoided_actions` | Only CT and CSF; EEG, brain MRI, tilt and exercise not penalised; reasons generic. | FIXED: CSF, EEG, brain MRI, tilt, exercise as waste, each naming complete heart block with a wide-complex escape. |
| C | major | `ground_truth.assessment` | "Permanent pacing" without the urgency of a hypotensive wide-escape block, no pacing-mode decision with LVEF 42%, "Do not perform tilt-table" as a prohibition. | FIXED: musts are recognition, immediate bridge (pads, isoprenaline or temporary wire), monitored bed, permanent pacing this admission (ESC 2021 Class I), physiological ventricular pacing with LVEF 42% (ACC/AHA/HRS 2018 IIa), withhold metoprolol and hold antihypertensives while hypotensive, prophylaxis around the penicillin anaphylaxis, driving. Tilt prohibition deleted (it is an avoided action). |
| C | major | `ground_truth.differential` | SSS and VT left moderate after telemetry; immune-checkpoint myocarditis (pembrolizumab in the history) and recurrent PE (prior PE, cancer, dyspnoea) absent. | FIXED: all low with the excluding result named; checkpoint myocarditis and recurrent PE added; vasovagal very low. |
| L | minor | `red_herrings[0]` | data_point "near-syncopes attributed to deconditioning" is not what the HPI says (he attributes the dyspnoea and fatigue). | FIXED: quotes "which he attributes to deconditioning"; pembrolizumab red herring added. |
| A | minor | all criteria, `stop_rule`, `sequence_constraints` | Free-text section citations, rationale equal to label, `max_additional_actions: 0`, no constraints. | FIXED: keys only, real rationales, stop rule ECG/TTE/monitoring with 3 additional actions, soft ECG before TTE and before monitoring. |
| B | major | `initial_tool_outputs.drug_interactions` | With no initial drug output, the MockServer served the first stored drug follow-up (e.g. this case's own named-drug review) to a check of any other drug, such as verapamil. | FIXED: the medication-list review is stored as `initial_tool_outputs.drug_interactions` as well as the fallback, so an unnamed drug receives the list review and the named-drug follow-ups still match their own drug. |

## Changes, in one paragraph a physician can read before re-reviewing

The 72-year-old man after pembrolizumab with hypotensive complete heart block (wide LBBB-morphology escape at 38 bpm) now has three required steps (ECG, TTE, inpatient telemetry with Holter accepted) and three recommended ones: BMP with troponin (normal troponin against an infarct or checkpoint myocarditis), a head CT for loss of consciousness with a temporal contusion at 72 (NICE NG232), and a review of metoprolol. His numbers are unchanged (RS03 is the case that changes); the echo now reports units, basal inferior hypokinesis matching the CMR, TAPSE and PASP. CMR and the literature lookup are optional. CSF, EEG, brain MRI, tilt and exercise are waste. The musts add an immediate pacing bridge, physiological pacing for LVEF 42%, withholding metoprolol and the antihypertensives while hypotensive, antibiotic prophylaxis around his penicillin anaphylaxis and driving advice. All alternatives in the differential are low with the excluding result; checkpoint myocarditis and recurrent PE were added.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: generic synonyms and R55 still accepted, and the I44 block accepts "mobitz ii" and "second degree av block" for a complete-block case; not hand-edited.
- Plan (lead): section 3 lists head CT as avoided in this subtype, but RS02 meets the plan's own NG232 rule (65 or over, loss of consciousness, head strike), as M03 did.

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. Deviations from the lead plan, decided for dataset quality:
- Head CT recommended instead of avoided (NICE NG232, as above).
- Labs pinned as BMP plus troponin rather than BMP alone, because the pembrolizumab history makes troponin a targeted assay for a reversible cause of the block.
