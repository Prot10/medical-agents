# SYNC-CARD-RS05
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | monitoring follow-up | VT described as LBBB morphology with inferior axis, the signature of an outflow-tract origin, in a case whose substrate is an inferior (RCA) infarct scar, where VT exits with a superior axis. | FIXED: RBBB morphology with superior axis, matching the inferior scar; expected evidence and key evidence updated. |
| C | major | monitoring follow-up, criterion | Both runs called "sustained", but the 18 s asymptomatic run is non-sustained by definition (under 30 s without haemodynamic compromise). | FIXED: hour 6, 32 s with near-syncope = sustained; hour 31, 18 s = non-sustained. |
| B | minor | monitoring follow-up | "First-degree AV block (PR 172 ms)" (a PR under 200 ms is normal; the ECG reads PR 168 ms normal); `heart_rate_range` keys "maximum"/"minimum" and max 196 above the fastest VT (192). | FIXED: "PR 168-172 ms"; keys min/max, max 192; output named "Inpatient telemetry, 48 h"; same recording as the monitoring fallback. |
| B | major | `action-3-order-cardiac-monitoring` | Only `telemetry` accepted (plan E). | FIXED: telemetry, holter_24h, holter_48h. |
| D | minor | `initial_tool_outputs.labs` | "serial testing required/warranted" inside the lab report (management instruction). | FIXED: removed; the troponin value and flag stay. beta-hCG stays in the output and is not required (plan). |
| C | major | `action-2-interpret-labs`, `sequence_constraints[0]` | Pinned CBC, BMP, Mg, troponin and BNP; hard labs-before-monitoring constraint (delaying monitoring for blood results is the unsafe order). | FIXED: required `panels: [BMP, magnesium]` (plan C); hard constraint deleted; soft ECG before TTE and before monitoring. |
| C | minor | echo follow-up | No `echo_type`; "severely reduced" for LVEF 32% (30-40% is moderately reduced); no TAPSE, thrombus statement. | FIXED: `echo_type: TTE`, "moderately to severely reduced (32%, previously 38%)", TAPSE 19 mm, no LV thrombus, regional abnormality unchanged in distribution. |
| C | major | `action-6-check-drug-interactions`, drug outputs | Required without a drug; one mixed follow-up; empty "general" fallback with "(agent not specified on this case's diagnostic pathway)" (plan B, H). | FIXED: required, alternatives carvedilol and metoprolol (plan B); follow-ups per beta-blocker and for amiodarone (the planned drug); medication-list review (dual beta-blockade, furosemide K/Mg loss, spironolactone with lisinopril once K is repleted, Class IC and sotalol cautions) stored as initial and fallback drug output. |
| C | major | `action-5-search-medical-literature`, `stop_rule`, literature outputs | Literature required and in the stop rule; follow-up cited "Zipes and Wellens 1998" under a wrong title and gave patient-level conclusions; fallback "No directly applicable ... evidence. Recommend ...". | FIXED: optional, canonical rationale; follow-up from ESC 2022 VA (ICD Class I; ablation over escalating AAD) and AHA/ACC/HRS 2017; fallback literature deleted (the library answers). |
| C | major | `ground_truth.assessment` | "Obtain serial troponin" must (a test as a must, plan I); "Electrophysiology consult for ICD evaluation" instead of the decision; "Do not perform tilt-table" as a prohibition; no ablation, ischaemia or driving detail. | FIXED: musts are diagnosis, monitored bed with pads and cardioversion for recurrence, K 4.0-5.0 and Mg repletion with furosemide review, secondary-prevention ICD before discharge (ESC 2022 Class I), single beta-blocker, amiodarone or ablation for recurrences, ischaemia evaluation (coronary angiography), driving (3 months after a secondary-prevention ICD, Group 1). Prohibitions: Class IC, sotalol, discharge without ICD plan, electrolytes as definitive therapy. |
| C | major | `avoided_actions` | Tilt and exercise not penalised. | FIXED: brain MRI, EEG, head CT (knee strike only, age 56, no anticoagulant), CSF, tilt, exercise as waste, each naming the diagnosis. |
| C | major | `ground_truth.differential` | ACS left moderate although the echo shows no new wall motion abnormality and the VT is scar-type monomorphic; dual beta-blockade not considered as a bradyarrhythmic mechanism. | FIXED: ACS low (ischaemia still evaluated by a must), electrolyte-only arrhythmia low, bradyarrhythmia from dual beta-blockade low (no pauses on telemetry), vasovagal and orthostatic very low. |
| L | minor | `red_herrings` | data_point merged two analytes under one field path. | FIXED: data_point "Potassium 3.2 mEq/L" at BMP[1]; red herring added for the palpitations attributed to anxiety. |
| A | minor | all criteria, `stop_rule` | Free-text section citations, rationale equal to label, `max_additional_actions: 0`. | FIXED: keys only, real rationales; stop rule lists the five required criteria with 3 additional actions. |

## Changes, in one paragraph a physician can read before re-reviewing

The 56-year-old woman with ischaemic cardiomyopathy (prior inferior STEMI, LVEF 32%) and syncope now has five required steps: ECG, potassium and magnesium (3.2 and 1.6 on furosemide), TTE, inpatient telemetry (Holter accepted) and a medication review that finds carvedilol and metoprolol taken together. Telemetry captures one sustained run of monomorphic VT at 188 bpm with near-syncope and one non-sustained run; the VT morphology is now RBBB with a superior axis, which fits the inferior scar (it was LBBB with an inferior axis, an outflow-tract pattern). The hard labs-before-monitoring constraint and the serial-troponin must are gone; literature is optional and correctly cited. Musts: monitored bed with cardioversion available, electrolyte repletion, secondary-prevention ICD before discharge (ESC 2022 Class I), one beta-blocker only, amiodarone or ablation for recurrences, ischaemia evaluation for the mildly raised troponin, driving advice. Class IC drugs and sotalol are prohibited. ACS is low with a must to evaluate ischaemia.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: this VT case accepts "supraventricular tachycardia", "SVT", "AVNRT" and I47.1 as synonyms, so an SVT answer scores as correct; and "cardiac syncope", "arrhythmic syncope", "tachyarrhythmia" are generic. Not hand-edited.

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea.
