# SYNC-CARD-S05
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `followup_outputs` literature (`search_literature_as_syncope`), `action-5-search-medical-literature` | Required literature criterion; its follow-up repeated the expected_evidence (leak guard failure) and cited "Natural history of adults with asymptomatic, hemodynamically significant aortic stenosis" as JACC 2000 for the 3-year survival after syncope (wrong source and year; that figure is the classic Ross and Braunwald natural-history series). | FIXED: optional, canonical rationale, out of the stop rule; follow-up rewritten with ESC/EACTS 2021 (intervention criteria, TAVI at 75 or more) and ESC 2018 (echo Class I) only, placed last. |
| E | major | `fallback_tool_outputs.drug_interactions.general`, `fallback_tool_outputs.literature_search` | "(agent not specified on this case's primary pathway)"; "No directly applicable ... evidence" followed by a recommendation. | FIXED: drug fallback is a `medication_list_review`; literature fallback deleted. |
| C | major | `action-6-check-drug-interactions`, `followup_outputs` drug | Required with no drug; output warned about diuretics he does not take. | FIXED: recommended (plan B) with alternatives amlodipine and lisinopril, one follow-up each, reviewing his actual four drugs (vasodilators in severe AS, nitrates and PDE5 inhibitors, penicillin allergy). |
| C | minor | `action-2-interpret-labs` | Pinned CBC, BMP, Mg, troponin and glucose. | FIXED: recommended `panels: [BMP]`; expected_evidence normal electrolytes and creatinine 1.1, troponin not elevated, BNP 312. |
| B | major | `followup_outputs` monitoring, `action-4-order-cardiac-monitoring` | Criterion pinned telemetry only; trigger lacked the holter token; no case fallback (the library is also normal here, but plan E applies). | FIXED: alternatives telemetry, holter_24h, holter_48h; trigger `request_telemetry_holter_monitoring`; impression begins "Inpatient telemetry, 24 h"; same recording as `fallback_tool_outputs.cardiac_monitoring`. |
| B | minor | `followup_outputs[0]` (echo) | No echo_type, TAPSE, stroke volume, LVOT statement (needed to exclude HOCM, which the differential relies on). | FIXED: echo_type TTE; no dynamic LVOT obstruction or SAM, SVi 44 mL/m2, TAPSE 22 mm, no mass. |
| B | minor | `patient.neurological_exam.additional` | "narrow pulse pressure noted" with 118/78 mmHg (pulse pressure 40). | FIXED: phrase removed. |
| C | major | `followup_outputs` tilt | Tilt performed in severe AS; avoided as harm (plan J: delete). | FIXED: follow-up deleted. |
| C | major | `ground_truth.assessment` | Musts restated scored tests ("Obtain echocardiogram urgently", "Recognize BNP"); "Admit ... to exclude concurrent arrhythmia"; no driving or exertion advice; prohibitions of tilt and exercise (tests, already avoided) and of discharge "without echocardiographic assessment". | FIXED: musts are diagnosis, admission until the Heart Team decision, Heart Team with TAVI favoured at 78 including coronary assessment and planning CT, caution with vasodilators, no strenuous exertion or driving until treated. Prohibitions: discharge before the decision, deconditioning attribution, potent vasodilators. |
| C | major | `ground_truth.differential` | Arrhythmic syncope moderate after normal ECG conduction and telemetry; HOCM excluded by a Valsalva murmur sign not in the case. | FIXED: arrhythmic low with the telemetry evidence; HOCM cites the echo (no LVOT obstruction, no SAM); PE cites the normal RV. |
| H | minor | all `action_criteria[*]`, `avoided_actions` | "ESC 2018 §x" and "Locati 2014" citations; rationale equal to label; avoided rationales cited "ACC/AHA Class III" without a key. | FIXED: keys only, real rationales naming ESC 2018 / ESC/EACTS 2021; avoided reasons name the diagnosis; CT waste reason cites NG232. |
| A | minor | `stop_rule`, `sequence_constraints` | Stop rule required the literature and drug checks; `max_additional_actions: 0`; no constraints. | FIXED: ECG, TTE, monitoring; 2; soft ECG before TTE and before monitoring. |
| L | minor | `ground_truth.red_herrings[0]` | data_point paraphrased. | FIXED: quotes the HPI. |
| E | minor | `ground_truth.key_clinical_evidence`, `metadata` | Em dashes; "required tool count is 6". | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The 78-year-old man with exertional syncope and a classic aortic stenosis murmur keeps his presentation and results: ECG with LVH and strain, severe high-gradient aortic stenosis on TTE (AVA 0.7 cm2, mean 52 mmHg, Vmax 4.6 m/s, LVEF 62%, now also stating no LVOT obstruction) and 24 h of normal inpatient telemetry (Holter accepted). Required: ECG, TTE, monitoring. Recommended: BMP and a medication review naming amlodipine or lisinopril. The guideline lookup is optional and its report now cites only ESC/EACTS 2021 and ESC 2018 correctly. Tilt and exercise remain harm (the stored tilt report was removed); brain MRI, EEG, CSF and head CT are waste. Musts: diagnosis, admission until the Heart Team decision, Heart Team with TAVI favoured at 78 with coronary assessment and planning CT, cautious vasodilators, no strenuous exertion or driving until treated. The arrhythmic alternative is now low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: "cardiac syncope" still accepted for this case; not hand-edited.
- Plan C3: a tilt order (avoided as harm) now gets the library's normal tilt report.

## Open questions for Andrea (judgment calls you could not settle)

None.
