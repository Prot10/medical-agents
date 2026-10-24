# SYNC-CARD-S04
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.clinical_history` (medications, past_medical_history, family_history, social_history) | Record copied from S02 (same seven drugs and doses, PMH wording, "father died suddenly at 58", retired accountant, smoking history) (plan M). | FIXED: his own record: telmisartan, indapamide (added 4 months ago), linagliptin, atorvastatin, paracetamol; PMH with CKD 3b by eGFR, knee osteoarthritis, hearing loss; new family and social history. HPI sentence on medication changes updated to name indapamide. The new record explains his Na 123, Mg 1.6 and urate 8.4. |
| B | major | `followup_outputs[1]`, `action-4-order-cardiac-monitoring` | Holter numbers copied from S02 (average 34, range 26-40, minimum 26 at 02:18); 24 h Holter under a telemetry label pinned to holter_24h. | FIXED: alternatives telemetry, holter_24h, holter_48h; "Inpatient telemetry, 24 h" with his own numbers (average 36, range 29-43, 4.8 s pause at 03:50, presyncope at 30 bpm on walking); same recording as the fallback. |
| D | major | `initial_tool_outputs.literature_search`, `initial_tool_outputs.drug_interactions.general` | Literature output equal to its key; drug block the bare key "Hold AV-nodal blockers" (he takes none). | FIXED: both deleted; one ESC/EACTS 2021 and ESC 2021 pacing follow-up added last. |
| E | major | `fallback_tool_outputs.literature_search`, `fallback_tool_outputs.drug_interactions.general` | "No directly applicable ... evidence"; "(agent not specified on this case's pathway)". | FIXED: literature fallback deleted; drug fallback is a `medication_list_review` (indapamide hyponatraemia; vasodilators in severe AS; latex allergy). |
| C | major | `action-5-check-drug-interactions`, `action-6-search-medical-literature` | Drug check recommended with no drug; literature recommended. | FIXED: both optional (plan B, A); drug alternative `{drug: indapamide}` with its follow-up. |
| C | minor | `action-2-interpret-labs` | Pinned CBC, BMP, Mg, troponin. | FIXED: recommended `panels: [BMP]`; expected_evidence Na 123, Mg 1.6 on indapamide. |
| B | major | `initial_tool_outputs.labs.panels.BMP` | Na 123, Cl 96, CO2 22: anion gap 5. Interpretation used the history ("at or above baseline 1.6", "poorly controlled"). | FIXED: Cl 88, CO2 26 (gap 9), consistent with a thiazide-like diuretic; interpretation states values and eGFR. |
| B | minor | `patient.vitals.hr` | HR 45 while the ECG escape is 32 bpm. | FIXED: 33. |
| B | major | `initial_tool_outputs.ecg` | "Low-voltage QRS in limb leads" with echo LVH (contradiction and an unintended amyloid flag); "raising concern for torsades"; LAFB diagnosed inside an LBBB escape; rhythm "junctional/ventricular" with a 148 ms LBBB QRS. | FIXED: findings only, ventricular escape. |
| B | minor | `initial_tool_outputs.eeg.artifacts[0]` | Artifact "from scalp contusion" placed at T4/T6 while the contusion is parietal. | FIXED: P4. |
| B | major | `followup_outputs[0]` (echo) | AVA 0.9 with "moderate-to-severe" and no gradients; numbers overlapping S02 (LVEF 40%). | FIXED: full TTE report with his own numbers (Vmax 4.4 m/s, mean 46 mmHg, AVA 0.8 cm2, LVEF 46%, septum 1.4 / PW 1.3 cm, LAVI 42, TAPSE 19 mm, PASP 38 mmHg); the CMR volumes moved to match (160/86 mL, EF 46%, mass 186 g) and its interpretive phrases removed. |
| C | minor | `action-8-order-ct-scan`, `followup_outputs` CT, must | Head CT criterion cited [Strickberger_2006] and was repeated as a must; CT impression had a management sentence. | FIXED: rationale cites NICE NG232 (age 82, LOC, head strike); CT moved to `initial_tool_outputs.ct`; must deleted (plan I). |
| C | major | `followup_outputs` tilt and exercise, `avoided_actions` | Tilt and a Bruce test performed in complete heart block with severe AS (plan J, M). | FIXED: follow-ups deleted; tilt and exercise avoided as harm. EEG and brain MRI added as waste. |
| H | minor | all `action_criteria[*]` | "§" citations; rationale equal to label. | FIXED. New optional CMR criterion `action-7-order-advanced-imaging` (plan tier: CMR optional) so the stored CMR is scored, not just served. |
| A | minor | `stop_rule`, `sequence_constraints` | `max_additional_actions: 0`; no constraints. | FIXED: 2; soft ECG before TTE and before monitoring. |
| C | major | `ground_truth.assessment` | Musts "Urgent permanent pacing", "Hold AV-nodal blockers" (none taken), head CT; no valve plan, no latex precaution, no hyponatraemia plan; tilt prohibition (a test). | FIXED: musts are diagnosis, monitored bed with pads, dual-chamber pacemaker with latex precautions, Heart Team with TAVI favoured at 82, stop indapamide and correct sodium by no more than 10 mEq/L in 24 h with magnesium, hold telmisartan, driving. Prohibitions: AV-nodal drugs before pacing, fast sodium correction, vasodilators, discharge before pacing. |
| C | major | `ground_truth.differential` | VT moderate after telemetry; AS "should be confirmed on echo" though the echo stages it; orthostatic mechanism (two antihypertensives, hyponatraemia) not discussed. | FIXED: AS moderate (staged, contributing), VT low, orthostatic hypotension added as low, drug-induced block very low. |
| L | minor | `ground_truth.red_herrings` | Head-strike red herring now wrong (CT is indicated). | FIXED: replaced by the sodium of 123; greying-out red herring quotes the HPI. |
| E | minor | `metadata.clinical_pearls[3]` | "moderate-to-severe AS" as a Class I intervention indication. | FIXED: symptomatic severe AS. |

## Changes, in one paragraph a physician can read before re-reviewing

The 82-year-old man who collapsed walking to the bathroom and struck his head now has his own record (telmisartan, indapamide added 4 months ago, linagliptin), which explains his sodium of 123 and magnesium of 1.6. Required: ECG (complete AV block, wide LBBB escape at 32 bpm), TTE (severe calcific AS with AVA 0.8 cm2, mean gradient 46 mmHg, LVEF 46%) and inpatient telemetry (Holter accepted: escape 29-43 bpm, presyncope at 30 bpm, a 4.8 s pause); none of these numbers is shared with S02 any longer. Recommended: BMP and a head CT within 8 hours (NICE NG232). CMR, the medication review and the guideline lookup are optional; tilt and exercise are harm, EEG, brain MRI and CSF waste. Musts: diagnosis, monitored bed with pacing pads, dual-chamber pacemaker with latex precautions, Heart Team with TAVI favoured, stop indapamide with slow sodium correction, hold telmisartan, driving advice.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: generic synonyms and R55 still accepted; not hand-edited.
- Plan C3: tilt and exercise orders now get the library's normal reports; both are avoided as harm here.

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. Decision taken: the new medication list was built to explain the case's existing abnormal sodium, magnesium and urate rather than changing those values, so the hyponatraemia became a management must.
