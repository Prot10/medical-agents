# SYNC-CARD-RP03
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | minor | `patient.clinical_history.family_history[1]` | Father's sudden arrest "while sleeping" is the pattern of LQT3 or Brugada, not CPVT, whose events are adrenergic. | FIXED: "while jogging". |
| B | major | `followup_outputs[3]` (CMR), `action-6` expected_evidence | CMR reported mid-wall LGE at the papillary muscle and inferolateral wall with raised native T1, while the criterion expected "structurally normal heart"; LGE with MAD is the arrhythmic-MVP substrate and contradicts the CPVT requirement of a structurally normal heart. | FIXED (plan K option): LGE and abnormal T1 removed; mild prolapse (3 mm) and 4 mm MAD kept; arrhythmic MVP with MAD added to the differential as low. |
| B | major | `followup_outputs[1]`, `action-4-order-cardiac-monitoring`, `fallback_tool_outputs.cardiac_monitoring` | A 72 h outpatient Holter (school, playground) stored as `holter_24h` for a patient who should be monitored in hospital; criterion pinned holter_24h with label "Telemetry and Holter"; it showed bidirectional VT, pre-empting the exercise test. | FIXED (plan E): alternatives telemetry, holter_24h, holter_48h; output "Inpatient telemetry, 48 h" showing exertion-related polymorphic couplets and one 5-beat polymorphic NSVT during stair walking with physiotherapy; same recording as the case fallback. The exercise test remains the diagnostic step. |
| B | minor | `followup_outputs[2]` (exercise test) | A 22-beat run called "sustained"; esmolol bolus (management) in the report; closing sentence named "catecholaminergic arrhythmia". | FIXED: non-sustained, esmolol removed, diagnosis sentence removed; numbered impression; quantitative data completed. |
| C | minor | `followup_outputs[0]` (TTE) | Measurements without units; no echo_type. | FIXED: units, echo_type TTE, RV/RA, PASP; impression in echo voice. |
| D | minor | `initial_tool_outputs.ecg` | "QTc 448 ms, upper limit of normal, borderline" (normal for a woman); speculative origin of PVCs. | FIXED: categorical findings and interpretation. |
| B | minor | `initial_tool_outputs.labs` | Summary lines carried diagnoses ("iron-deficiency anemia", "anisocytosis"); "Troponin I (high-sensitivity)" with ng/mL range. | FIXED: factual summary, pattern-level interpretation, "Troponin I". |
| C | major | `action-2-interpret-labs` | Recommended with CBC, BMP, Mg, troponin pinned; policy-text expected_evidence. | FIXED (plan C): `panels: [BMP]`; expected_evidence from the values. |
| C | major | `followup_outputs[6]` (genetic panel, interpret_labs) | Genetic test stored as a lab follow-up; variant p.Arg4159Cys unverifiable; summary line labelled "CPVT type 1 (H)". | FIXED (plan F): kept as the last clinical follow-up and not a criterion; variant changed to the well-described RYR2 c.13489C>T (p.Arg4497Cys); hedged association sentence; trigger `request_genetic_testing_inherited_arrhythmia_panel`. |
| C | major | `action-7-check-drug-interactions`, `followup_outputs[4..5]`, drug initial and fallback | Required; nadolol report claimed nadolol prolongs QT with escitalopram and raises sumatriptan levels (both wrong). | FIXED (plan B): optional, alternatives nadolol and propranolol; both reports corrected (nadolol renally excreted, no QT effect; the triptan interaction is propranolol-rizatriptan); medication-list review in initial and fallback. |
| C | major | `action-8-search-medical-literature`, `followup_outputs[7]` | Required; cited a "JACC 2023" cohort and a "Heart Rhythm 2024" meta-analysis that could not be verified. | FIXED: optional, canonical rationale; ESC 2022 content only, last. |
| A | minor | `sequence_constraints`, `stop_rule`, `citations`, `rationale` | No constraints; literature and drug check in the stop rule; `max_additional_actions: 0`; "§" and Locati citations; rationale equal to label. | FIXED: soft ECG before TTE and monitoring, hard TTE before exercise test; stop rule ECG, TTE, telemetry, exercise test, 3; keys only; real rationales. |
| C | major | `ground_truth.assessment` | Musts lacked titration to maximal dose, repeat exercise test, flecainide, ICD position, cascade screening of the children and anaemia treatment; "EP consult for ICD"; "Do not call `order_specialized_test`" and tilt prohibition. | FIXED (plan): musts are diagnosis, monitored bed, nadolol or propranolol to maximal tolerated dose, repeat exercise test on therapy, flecainide for breakthrough, exercise restriction, no first-line ICD (ESC 2022), genetic counselling and cascade screening (sister, two children), treat and investigate the iron deficiency, driving. Prohibitions: anaemia, panic or epilepsy attribution and antiseizure drugs, ICD without beta-blocker, sympathomimetics, sport clearance. |
| C | major | `avoided_actions`, tilt follow-up | No EEG or tilt penalty; tilt follow-up referred to isoproterenol (plan J). | FIXED: EEG and tilt waste; tilt follow-up deleted (the library's normal tilt is consistent with her); MRI, CT (NICE NG232: standing-height fall, GCS 15, age 38) and CSF rationales name CPVT. |
| C | major | `ground_truth.differential` | LQTS high, ARVC and HCM moderate after the work-up; epilepsy argued from the off-pathway EEG; arrhythmic MVP (raised by the MRI), anaemia and panic missing. | FIXED (plan K): all low with the excluding results; arrhythmic MVP with MAD, and anaemia or panic, added. |
| L | minor | `ground_truth.red_herrings` | Red herring 0 cited the EEG; data_points paraphrased. | FIXED: quoted data_points; interpretations without the EEG; anaemia-attribution red herring added. |
| E | minor | `metadata.clinical_pearls`, `difficulty_description`, `diagnostic_traps` | "Bidirectional VT is pathognomonic" (also digoxin toxicity, Andersen-Tawil); description relied on ambulatory monitoring; "borderline QTc". | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The 38-year-old woman with three exertional collapses and a father who died suddenly while jogging at 45 now has four required steps: ECG (normal, QTc 448 ms, isolated PVCs), TTE (structurally normal apart from mild mitral prolapse), inpatient telemetry (Holter accepted) and an exercise test after the echo, which reproduces ectopy escalating to bidirectional and polymorphic VT with presyncope; BMP and cardiac MRI are recommended, the beta-blocker review and literature optional. The MRI no longer reports papillary-muscle LGE, which contradicted the structurally normal heart CPVT requires; it keeps the mild prolapse and a 4 mm annular disjunction, and arrhythmic MVP is now a low differential. Telemetry is an inpatient recording with exertion-only polymorphic ectopy instead of an outpatient 72 h Holter. The genetic report (RYR2 p.Arg4497Cys) is the last follow-up, not a criterion. The musts are nadolol or propranolol to the maximal tolerated dose with a repeat exercise test, flecainide for breakthrough, exercise restriction, no first-line ICD, genetic counselling with cascade screening of her sister and children, treatment of the iron deficiency and driving advice. LQTS, ARVC, HCM, Brugada, anaemia or panic and epilepsy are low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: `accepted` carries "supraventricular tachycardia", "SVT", "AVNRT", "tachyarrhythmia" and the generic syncope labels, and the codes include I47.1; a CPVT case should not accept SVT or AVNRT. Not hand-edited.
- Plan C2: no inherited-arrhythmia genetic panel exists in the vocabulary, so the RYR2 result stays an `interpret_labs` follow-up with no criterion.

## Open questions for Andrea (judgment calls you could not settle)

None. Decided here: the MRI LGE was removed rather than keeping a structurally abnormal heart, because the CPVT label requires a structurally normal heart and the criterion already expected one.
