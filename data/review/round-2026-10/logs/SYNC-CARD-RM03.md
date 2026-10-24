# SYNC-CARD-RM03
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for SYNC-CARD) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | followup_outputs[order_ct_scan], ground_truth.action_criteria[head CT] | Head CT follow-up was a placeholder equal to the key ("Rule out traumatic intracranial haemorrhage"); optional criterion although a temple bruise on aspirin alone at 58 meets no NICE NG232 criterion | FIXED (plan G, J): follow-up and criterion deleted; head CT waste (the normal fallback head CT answers an order) |
| B | major | initial_tool_outputs.ecg | "Sinus bradycardia at 46 bpm" with 3:2 Mobitz II: 46 bpm is the ventricular rate | FIXED: sinus rhythm, atrial rate 70, ventricular rate 46; "consistent with prior anteroseptal infarction versus septal fibrosis" reduced to "Q waves in V1-V3"; em dash removed |
| A | major | followup_outputs[monitoring], ground_truth.action_criteria[monitoring] | Ambulatory 24 h Holter with a patient diary in an admitted patient; holter_24h pinned | FIXED (plan E): inpatient telemetry 48 h with time stamps, symptom reported to the nurse; alternatives telemetry, holter_24h, holter_48h; same report as fallback monitoring |
| D | major | initial_tool_outputs.labs.panels["Exclusion studies"] | Engineering text ("which is what this case's diagnosis rests on") with magnesium "Within reference range" | FIXED: block deleted; magnesium 2.1 mg/dL in an Electrolytes panel |
| B | minor | initial_tool_outputs.labs.panels.Cardiac[troponin] | Troponin 0.04 flagged normal against a reference of <0.04 | FIXED: 0.02 ng/mL |
| A | minor | ground_truth.action_criteria[labs] | CBC+BMP+Mg+troponin pinned | FIXED (plan C): recommended, `panels: [BMP]` |
| A | major | ground_truth.action_criteria[drug], followup_outputs[drug] | Required with no `drug`; output titled "in a patient with Mobitz type II AV block" served to any drug query | FIXED (plan B, recommended): `{drug: atenolol}`; follow-up rewritten without the diagnosis, trigger `check_atenolol_interactions`; neutral medication-list review as initial and fallback |
| D | major | followup_outputs[literature x2] | Hypothyroidism references that cannot be verified as given; pacing follow-up with an empty summary and an unverifiable 1995 progression figure; literature required and in the stop rule | FIXED (plan A): optional; one follow-up citing ESC 2021 pacing, ESC 2018 syncope and ACC/AHA/HRS 2018 bradycardia, trigger `search_literature_mobitz_pacing`, last; hypothyroidism follow-up deleted; neutral initial literature |
| A | major | ground_truth.action_criteria[exercise test] | Recommended exercise test in symptomatic Mobitz II | FIXED (plan J): criterion deleted, exercise test waste; stored report kept with peak HR corrected to 44% of predicted (was 39%) |
| B | minor | followup_outputs[CMR] | Native T1 1120 ms identical to RS02/RS03 (plan M); impression omitted the LAD-territory scar | FIXED: T1 1090 ms; impression lists scar, LV size and EF |
| B | minor | followup_outputs[TTE] | No echo_type, empty valves, no LA or wall thickness | FIXED (plan G): full TTE report, same LVEF 38%, LVEDD 58 mm, TAPSE 20 mm, RVSP 32 mmHg |
| C | major | ground_truth.assessment.required_recommendations | "Hold AV-nodal blockers" without naming atenolol; no device choice despite LVEF 38%; no ischaemic evaluation of an LAD scar; aspirin not addressed | FIXED (plan RM03): see Changes |
| A | minor | ground_truth.assessment.prohibited_recommendations | "Do not call ..." engineering text; tilt prohibition | FIXED (plan H, I): deleted |
| C | minor | ground_truth.avoided_actions | No EEG, tilt, exercise or head CT avoidance; reasons did not name the diagnosis | FIXED: six waste entries, each naming the diagnosis |
| C | major | ground_truth.differential | VT moderate after telemetry; SSS "SNRT and EP help clarify" (not in the case); atenolol, TSH and family conduction disease missing | FIXED (plan K): VT and SSS low with telemetry results; atenolol-related block, subclinical hypothyroidism (low) and familial conduction disease (moderate) added |
| D | minor | ground_truth.red_herrings | data_points paraphrased; "normal EEG" (non-criterion tool) cited | FIXED: five quoted herrings (jerks, head strike, clinic seizure label, TSH, anaemia) |
| E | minor | all criteria, key_clinical_evidence | rationale equal to label; section citations, [Locati_2014], [Strickberger_2006]; "Head CT is justified by the head strike" | FIXED |
| A | major | ground_truth.sequence_constraints, stop_rule | None; stop rule with drug and literature, max 0 | FIXED: soft ECG before TTE and monitoring; stop rule ECG, TTE, monitoring, max 3 |

## Changes, in one paragraph a physician can read before re-reviewing
58-year-old man on atenolol, amlodipine and aspirin with three abrupt collapses in two months (one seated, one on stairs), brief jerks and a temple bruise. ECG: sinus rhythm 70 with 3:2 Mobitz II (ventricular rate 46), RBBB, LAFB and Q waves V1-V3; telemetry 48 h: frequent Mobitz II and high-grade block with 4.2 s (symptomatic) and 3.8 s pauses, no VT; TTE: LVEF 38% with anteroseptal and apical hypokinesis; CMR: LAD-territory scar into the septum. Required: ECG, TTE, monitoring; recommended: BMP, CMR, atenolol review; optional: literature; waste: brain MRI, CSF, head CT (no NG232 criterion), EEG, tilt, exercise test. Musts: monitored bed with pacing pads; permanent pacing without waiting for washout; CRT rather than RV pacing for LVEF below 40% (ESC 2021); hold atenolol, then an HFrEF beta-blocker and guideline therapy; coronary angiography; continue aspirin and atorvastatin; ECG screening of relatives; driving restriction until 1 week after implantation. Prohibitions: no AV-nodal blockers before pacing, no antiseizure drugs, no discharge without a pacing plan, no deferral of pacing for TSH or atenolol.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Neutral initial literature and drug answers kept (see P02 CENTRAL).
- Plan C2: coronary angiography is not in the vocabulary, so the ischaemic evaluation is a must, not a criterion.
- Synonyms (plan C1): generic "cardiac syncope" and "bradyarrhythmia" accepted.

## Open questions for Andrea (judgment calls you could not settle)
- I added musts the plan did not list because the case's own data require them: CRT instead of RV pacing (LVEF 36-38%, ESC 2021 Class I), holding atenolol, and coronary angiography for the LAD scar. A cardiologist should confirm. Whether a CRT-D rather than CRT-P is preferable (ischaemic scar, LVEF just above 35%, syncope) is left open; ESC 2022 recommends programmed ventricular stimulation in prior MI with unexplained syncope, but here the syncope is explained by documented high-grade block.
- Family history (father's sudden death at 52, brother paced at 55) suggests familial conduction disease alongside the ischaemic scar; I added relative screening as a must. Andrea may prefer to drop the family history instead.
