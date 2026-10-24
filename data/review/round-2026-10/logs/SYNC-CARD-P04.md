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

## Verification
Adversarial verifier, 24 Oct 2026. Read the whole final case against the plan (P04 bullets, sections A-O) and the log.
- Confirmed: PMH now agrees with the HPI (diagnosis after the swim-meet collapse); ECG QTc 510 ms with the 460 ms female limit; telemetry `telemetry` 48 h, PVC burden 84 / about 213,000 beats = 0.04%, same report as the fallback; exercise test QTc 512 to 535 ms then 505 ms at 4 min, peak 140 bpm; hard TTE before exercise test; labs recommended BMP only; exercise test recommended and EEG optional per the plan; drug criterion recommended with nadolol, propranolol, levetiracetam and one follow-up each; literature optional and last; stop rule = the three required criteria, max 3; KCNQ1 c.1781G>A gives p.Arg594Gln (codon 594 = c.1780-1782), consistent with the LQT1 phenotype (broad-based T waves, swimming and exertional triggers); differential all low with excluding results; musts match the plan (nadolol or propranolol Class I, QT-drug avoidance, K/Mg during illness, ICD not first-line, genetic and cascade testing, driving).
- Found and fixed:
  1. B, minor: the exercise-test impression and `reason_for_termination` said "Four-beat polymorphic VT at 140 bpm", confusing the sinus rate at onset with the VT rate (210 bpm in the findings). Both now read VT at 210 bpm arising at a sinus rate of 140 bpm.
- Not changed, for the lead: the plan keeps the exercise test recommended. It is performed unmedicated after telemetry has already captured torsades with QTc above 500 ms, and the stored result provokes polymorphic VT with hypotension. The diagnosis is already established by the resting QTc, so the test adds phenotype detail but not a management change; I would make it optional. I left the plan's tier because the plan decides tiers, and the worker raised the same point.
- Re-ran `perfect_agent.py SYNC-CARD-P04 -v` (ok), `case_io.py check` (clean for this case) and the case guards (pass).

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- `action-7-order-specialized-test` (exercise test) moved from recommended to optional, rationale rewritten: resting QTc 510 ms already establishes the diagnosis and telemetry captured torsades, so exercise testing is deferred until beta-blockade is established (ESC 2022 ventricular arrhythmia guideline; Fletcher 2013). The hard TTE-before-exercise constraint is kept. Why: recommending a stress test in a patient with documented torsades and unprotected long QT is unsafe.

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: congenital LQTS labels only (congenital, inherited, hereditary, LQT1, KCNQ1); bare "long qt syndrome" and "LQTS" retired because "acquired long QT syndrome", a mimic in this differential, contains their tokens.
- "ESC/EACTS 2021" renamed "ESC/EACTS 2025" (2025 ESC/EACTS valvular guideline, Praz 2025, supersedes 2021): `.ground_truth.sequence_constraints[2].reason`.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-1-analyze-ecg citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2022_VA_SCD]']; action-2-interpret-labs citations ['[ESC_2018]'] -> ['[ESC_2022_VA_SCD]']; action-7-order-specialized-test citations ['[ESC_2018]'] -> ['[ESC_2022_VA_SCD]', '[Fletcher_2013]']; action-6-check-drug-interactions citations ['[ESC_2018]'] -> ['[ESC_2022_VA_SCD]']; avoid-waste-3-order-ct-scan citations ['[ESC_2018]'] -> ['[NICE_NG232]']; action-3-order-echocardiogram->action-7-order-specialized-test citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2023_Cardiomyopathy]', '[ESC_EACTS_2025_VHD]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-P04` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure report, supine values = the presenting vitals; No orthostatic fall in blood pressure and no excessive heart rate rise on active standing. |
| `ground_truth.action_criteria[action-orthostatic-blood-pressure]` | added, recommended, after the ECG criterion [ESC_2018] (decisions CENTRAL 1: orthostatic BP in every initial evaluation) |
| `followup_outputs[8] (`request_genetic_testing`)` | moved from `interpret_labs` (the decisions-file placeholder until C2) to `order_specialized_test` `genetic_panel:inherited_arrhythmia`; same genes and results, rows as findings, the interpretation as the impression |
| `ground_truth.action_criteria[action-genetic-panel]` | added, recommended [ESC_2022_VA_SCD]; the assessment must on genetic counselling and testing is unchanged |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.

Correction to the decisions file: it said no genetic result was stored in this case; one was, under `interpret_labs`. It is moved, not rewritten.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- follow-up EEG `request_eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
