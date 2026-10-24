# SYNC-CARD-P04
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for SYNC-CARD) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | followup_outputs[exercise test] | Report said QTc "fails to shorten" while its own numbers shortened (512 to 492 ms at peak), and "expected <430 ms at this heart rate" was an invented threshold | FIXED: QTc 512 (rest), 520, 528, 535 ms with rising HR, 505 ms at 4 min recovery; quantitative_data and impression rewritten in report voice |
| B | major | patient.clinical_history.past_medical_history[0] | "diagnosed at age 15 after three witnessed convulsive episodes" contradicts the HPI (diagnosis after the first collapse at the swim meet; episodes at 15, 16, 17, 19) | FIXED: "after a witnessed convulsive collapse at a swim meet"; red herring updated to quote it |
| B | major | followup_outputs[monitoring] | `monitor_type` "Continuous telemetry" (not a vocabulary value); PVC burden 84/48 h called 0.06% (0.04% at 74 bpm) | FIXED (plan E): `monitor_type` telemetry, trigger `request_telemetry_holter_monitoring`, min/max HR added, 0.04%, impression numbered; same report as fallback monitoring |
| C | minor | initial_tool_outputs.ecg.findings[4] | "normal <440 ms female" (the upper limit in women is 460 ms) | FIXED |
| A | major | ground_truth.action_criteria[monitoring] | telemetry only | FIXED: telemetry, holter_24h, holter_48h |
| A | major | ground_truth.action_criteria[literature] | Required and in the stop rule; follow-up cited two papers that cannot be verified (EHJ 2019 "systematic review", JACC 2020) and an empty summary | FIXED (plan A): optional; follow-up rewritten from ESC 2022 and ESC 2018, trigger `search_literature_long_qt_lqts`, last; neutral initial literature answer added (see CENTRAL in P02) |
| A | major | ground_truth.action_criteria[drug], followup_outputs[drug] | Required with no `drug`; the only drug output was titled "in setting of suspected congenital long QT syndrome" and was served to any drug query | FIXED (plan B, recommended): alternatives nadolol, propranolol, levetiracetam with one follow-up each; QT list kept as a follow-up under `check_qt_prolonging_drug_list_crediblemeds` without the diagnosis; neutral medication-list review as initial and fallback |
| A | minor | ground_truth.action_criteria[labs] | CBC+BMP+Mg+troponin+beta-hCG pinned | FIXED (plan C): recommended, `panels: [BMP]`; Mg, troponin and beta-hCG accepted (age 19, not required) |
| A | major | ground_truth.sequence_constraints, stop_rule | None; stop rule included literature and drug check, max 0 | FIXED: soft ECG before TTE and monitoring, hard TTE before exercise test; stop rule ECG, TTE, monitoring, max 3 |
| C | major | ground_truth.assessment.required_recommendations | Musts restated tests (measure QTc, confirm K/Mg, order exercise test); no beta-blocker drug or class, no ICD position, no levetiracetam plan, no driving advice | FIXED (plan I): see Changes |
| C | minor | ground_truth.assessment.prohibited_recommendations | Tilt prohibition (a test); reliance on the KCNQ1 result, which is not part of the scored pathway | FIXED: tilt removed (remains an avoided action); the levetiracetam statement rests on K, Mg and pharmacology |
| C | major | ground_truth.differential | Epilepsy high, CPVT and vasovagal moderate after the work-up excludes them; acquired LQTS coded T36.9XXA | FIXED (plan K): all low with excluding results; acquired LQTS coded I45.81 |
| D | minor | ground_truth.red_herrings | data_points paraphrased | FIXED: quoted from the fields |
| E | minor | all criteria | rationale equal to label; section citations and "Locati 2014" | FIXED |
| B | minor | followup_outputs[TTE] | No `echo_type`, LA and TAPSE missing | FIXED: echo_type TTE, LA 3.2 cm, TAPSE 23 mm |
| D | minor | followup_outputs[genetic].interpretation | No hedged templated comment | FIXED; kept as the last non-literature follow-up, not a criterion (plan F) |
| E | minor | metadata.clinical_pearls[1,4], key_clinical_evidence | "Up to 30%" misdiagnosis and "5-fold" risk figures without a source | FIXED: figures removed |

## Changes, in one paragraph a physician can read before re-reviewing
19-year-old with four collapses since 15 during exertion or emotion, preceded by palpitations, labelled epilepsy on levetiracetam; maternal uncle drowned at 28. ECG QTc 510 ms (diagnostic of LQTS at 480 ms or more, ESC 2022); telemetry 48 h with persistent QTc 498-514 ms and a run of torsades; normal TTE; the exercise test (recommended, after a hard TTE-first constraint) now shows QTc prolonging with exercise and 505 ms at 4 min recovery with exercise-induced polymorphic VT. Required: ECG, TTE, monitoring; recommended: BMP, exercise test, drug review (nadolol, propranolol or levetiracetam); optional: EEG, literature. Musts: monitored admission; nadolol or propranolol titrated to the maximum tolerated dose; QT-drug avoidance and prompt K/Mg correction during illness; ICD not first-line (after arrest or recurrence on beta-blocker; LCSD option); neurology review to taper levetiracetam; genetic counselling and cascade screening including the brother and mother; avoid swimming alone and strenuous exercise until treated; driving restriction. The differential is updated; the PMH no longer contradicts the HPI.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Neutral initial literature and drug answers kept so that disease-specific follow-ups are not served to every query (see P02 CENTRAL).
- Plan C1/C2: "cardiac syncope" synonym; LQTS genetic panel not in the vocabulary (result stays under `interpret_labs` panel `genetic`, plan F).

## Open questions for Andrea (judgment calls you could not settle)
None. Note for the lead: the plan keeps the exercise test recommended. I applied it, with the rationale that the resting QTc already establishes the diagnosis; some clinicians would defer exercise testing until on a beta-blocker in a patient with QTc above 500 ms and recent arrhythmic syncope, which is why it is not required.
