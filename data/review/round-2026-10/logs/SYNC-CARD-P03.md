# SYNC-CARD-P03
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for SYNC-CARD) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | blocker | initial_tool_outputs.ecg | ECG at 38.6 C showed only a saddle-back pattern, "In isolation, this ECG would be read as normal"; the type 1 pattern existed only in a repeat-ECG follow-up that `analyze_ecg` (one parameter, `clinical_context`) cannot target | FIXED (plan P03/O): the index ECG now shows a spontaneous fever-associated coved type 1 pattern in V1-V2 (2.4 / 2.1 mm, 2.8 mm in high V1), QTc 408 ms |
| A | blocker | followup_outputs[repeat ECG, ajmaline, EP study] | Repeat ECG with "Long QT syndrome excluded" / "argues against ARVC"; ajmaline test and EP study stored under `analyze_ecg` (not in the vocabulary) | FIXED (plan F, O): all three deleted; ajmaline challenge written as a prohibition (no drug challenge after a documented type 1 pattern, ESC 2022) |
| D | major | initial_tool_outputs.mri | MRA content in a brain MRI report | FIXED (plan N): MRA observation and impression clause removed; brain MRI made waste |
| B | major | followup_outputs[monitoring] | `monitor_type` "Continuous telemetry" (not a vocabulary value), trigger `request_holter`; text said the type 1 pattern was absent at 38.6 C | FIXED (plan E): `monitor_type` telemetry, 72 h, trigger `request_telemetry_holter_monitoring`, events with timestamps tracking temperature; same report as `fallback_tool_outputs.cardiac_monitoring` |
| D | major | followup_outputs[TTE] | Placeholder equal to the criterion key ("Structurally normal heart (typical of channelopathy) vs evidence of myocarditis") | FIXED (plan G): full normal TTE report (`echo_type` TTE, LVEF 60% biplane, LVEDD 49 mm, walls 9 mm, LA 35 mm, RV 36 mm, TAPSE 24 mm, PASP 24 mmHg); fallback echo LVEF aligned to 60% |
| D | major | initial_tool_outputs.drug_interactions, fallback_tool_outputs.drug_interactions | Initial block was the key; fallback was titled "medications contraindicated in Brugada syndrome", announcing the diagnosis to any drug query | FIXED (plan B): both now a neutral medication-list review (no medications); per-drug follow-up for paracetamol/acetaminophen |
| D | major | initial_tool_outputs.literature_search, fallback_tool_outputs.literature_search | Initial block was the key (leak guard failure); fallback cited an Antzelevitch title that cannot be verified as given | FIXED (plan A): initial replaced by the neutral syncope-evaluation answer (see CENTRAL in P02); Brugada content moved to one follow-up `search_literature_brugada` citing ESC 2022 (Zeppenfeld) and Postema 2009, placed last; fallback deleted |
| A | major | ground_truth.action_criteria[literature] | Recommended | FIXED: optional, canonical rationale |
| A | minor | ground_truth.action_criteria[drug] | Recommended with no `drug` | FIXED (plan B tier optional): alternatives {drug: paracetamol}, {drug: acetaminophen} (the drug the musts start; he takes none) |
| A | minor | ground_truth.action_criteria[labs] | CBC+BMP+Mg+troponin pinned | FIXED (plan C): recommended, `panels: [BMP]` |
| A | major | ground_truth.action_criteria[monitoring] | Pinned holter_24h | FIXED: telemetry, holter_24h, holter_48h |
| B | minor | ground_truth.action_criteria[*].expected_evidence | ECG evidence "may be subtle when afebrile"; drug evidence named "serotonergic agents" (not a Brugada concern) | FIXED: evidence per criterion matches the stored reports; serotonergic agents removed everywhere (plan P03) |
| E | minor | all criteria | rationale equal to label; free-text section citations and "Locati 2014" | FIXED: real rationales; citations reduced to [ESC_2018] |
| A | major | ground_truth.sequence_constraints, stop_rule | None; stop rule max 0 | FIXED: soft ECG before TTE and before monitoring; stop rule ECG + monitoring, max 3 |
| C | major | ground_truth.assessment.prohibited_recommendations | Blanket "class IA" ban (quinidine, class IA, is the recommended drug for storm); "serotonergic agents"; tilt prohibition (a test); flecainide "only as diagnostic challenge" | FIXED: prohibitions name the brugadadrugs.org avoid list; no drug challenge; no discharge while febrile; no antiseizure drugs |
| C | major | ground_truth.assessment.required_recommendations | No ICD class, no paracetamol, no quinidine option, no driving advice | FIXED: see Changes |
| C | major | ground_truth.avoided_actions | No EEG, brain MRI or exercise avoidance | FIXED: EEG, brain MRI, exercise stress test waste; CT, CSF, tilt reasons name the diagnosis (CT: no NICE NG232 criterion despite the forehead abrasion) |
| C | major | ground_truth.differential | LQTS high, CPVT and myocarditis moderate after the work-up excludes them; prior "vasovagal" attribution not in the differential; LQTS coded I49.8 | FIXED (plan K): all low with the excluding result; vasovagal/orthostatic syncope added; LQTS code I45.81 |
| D | minor | ground_truth.red_herrings | "Coworkers initially attribute to febrile seizure" not in the HPI; ECG herring no longer true | FIXED: data_points quoted from the HPI; ECG herring replaced by the prior normal afebrile ECG in the HPI |
| D | minor | initial_tool_outputs.labs.abnormal_values_summary | "CRP 32 (elevated, consistent with influenza)" interpretive | FIXED: plain list |
| D | minor | followup_outputs[genetic].interpretation | Lab-style "Abnormal values: ..." | FIXED: genetic report voice with hedged templated comment; kept as the last non-literature follow-up, not a criterion (plan F) |
| E | minor | metadata.clinical_pearls, diagnostic_traps, difficulty_rationale | Unsupported figures ("up to 2% of febrile patients", convulsive syncope "up to 12%"), "provocation testing is required"; stale counts | FIXED |

## Changes, in one paragraph a physician can read before re-reviewing
38-year-old Filipino-American nurse with four collapses, all during fever, witnessed pulselessness, a father dead in his sleep at 42 and a brother with fever-related syncope. The index ECG at 38.6 C now shows a coved type 1 Brugada pattern (2.4 and 2.1 mm in V1-V2) with normal QTc; the repeat-ECG, ajmaline and EP-study follow-ups are gone. Inpatient telemetry (72 h) shows polymorphic ectopy and NSVT that track temperature; TTE and CMR are normal; labs show influenza A with normal troponin and electrolytes. Required: ECG and monitoring; recommended: TTE, labs (BMP), CMR; optional: drug review (paracetamol) and literature. EEG, brain MRI, exercise test, tilt, head CT and CSF are waste. Musts: paracetamol and cooling now; monitored bed with defibrillator; ICD (ESC 2022 IIa, type 1 pattern with arrhythmic syncope); brugadadrugs.org avoidance list; quinidine for storm; genetic counselling, SCN5A testing and cascade screening of brother and daughter; antipyresis for future fevers; driving restriction. Prohibitions: no ST-elevating drugs, no drug challenge, no discharge while febrile, no antiseizure drugs.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- As in P02: per-drug and per-entity literature follow-ups need a neutral `initial_tool_outputs` answer, otherwise the MockServer's tier 2 serves the first follow-up to any query (the Brugada guideline to a search on "syncope", the paracetamol review to any drug).
- Plan C2: sodium-channel-blocker challenge and inherited-arrhythmia genetic panel are not in the vocabulary; the genetic result stays under `interpret_labs` (panel `genetic`) as the plan rules.
- Plan C1: the diagnosis block accepts the generic "cardiac syncope".

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the whole final case against the plan (P03 bullets, sections A-O) and the log.
- Confirmed: index ECG at 38.6 C carries the coved type 1 pattern (2.4/2.1 mm, 2.8 mm high V1) with QTc 408 ms and no "read as normal" sentence; repeat-ECG, ajmaline and EP follow-ups gone; MRI has no MRA content and is waste; monitoring is `telemetry` 72 h with the same report as the fallback; TTE is a full report (PASP 24 mmHg agrees with TR 2.2 m/s); tiers match the plan's Brugada row (required ECG and monitoring; recommended TTE, BMP, CMR; optional drug check and literature; tilt, exercise, MRI, EEG avoided); stop rule = the two required criteria, max 3; no "serotonergic" text; literature is the last follow-up and cites ESC 2022 and Postema 2009 correctly; red-herring data_points are verbatim from the HPI; musts cover paracetamol, ICD (IIa), brugadadrugs.org, genetic counselling with cascade screening, driving.
- Found and fixed:
  1. A (discriminator), minor: `fallback_tool_outputs.echo` had no `echo_type` and said "Normal transthoracic echocardiogram", so it answered any TEE, bubble or exercise-echo order with a TTE text (PATTERNS 5; P03 was the only SYNC-CARD case with such a fallback). Set to null (the TTE follow-up answers TTE orders, the library answers the others) and removed `echo` from `metadata.fallback_tool_kinds`.
  2. K, minor: the LQTS differential cited "no QT prolongation or torsades on telemetry", which the telemetry report does not state. Rewritten to cite the 12-lead QTc 408 ms and the fever-dependent ectopy with coved ST elevation that the telemetry does report.
- Re-ran `perfect_agent.py SYNC-CARD-P03 -v` (ok), `case_io.py check` (clean for this case) and the case guards (pass).

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: "brugada syndrome" only; bare "brugada" retired (it credits "Brugada phenocopy").
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-1-analyze-ecg citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2022_VA_SCD]']; action-5-order-advanced-imaging citations ['[ESC_2018]'] -> ['[ESC_2022_VA_SCD]']; action-6-check-drug-interactions citations ['[ESC_2018]'] -> ['[ESC_2022_VA_SCD]', '[Postema_2009]']; avoid-waste-1-order-ct-scan citations ['[ESC_2018]'] -> ['[NICE_NG232]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-P03` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure report, supine values = the presenting vitals; No orthostatic fall in blood pressure and no excessive heart rate rise on active standing. |
| `ground_truth.action_criteria[action-orthostatic-blood-pressure]` | added, recommended, after the ECG criterion [ESC_2018] (decisions CENTRAL 1: orthostatic BP in every initial evaluation) |
| `followup_outputs[4] (`request_genetic_testing`)` | moved from `interpret_labs` (the decisions-file placeholder until C2) to `order_specialized_test` `genetic_panel:inherited_arrhythmia`; same genes and results, rows as findings, the interpretation as the impression |
| `ground_truth.action_criteria[action-genetic-panel]` | added, recommended [ESC_2022_VA_SCD]; the assessment must on genetic counselling and testing is unchanged |
| `followup_outputs[6] (`request_sodium_channel_blocker_challenge`)` | added: 'not performed, deferred by the clinical team' report |
| `ground_truth.avoided_actions[avoid-harm-sodium-channel-blocker-challenge]` | added, severity harm [ESC_2022_VA_SCD]; encodes the existing prohibited recommendation |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.

Correction to the decisions file: it said no genetic result was stored in this case; one was, under `interpret_labs`. It is moved, not rewritten.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-2-interpret-labs]`.alternatives: was [BMP]; now [BMP, magnesium, troponin] | [BMP].
- Decision: serve: new first alternative (old order kept as an alternative). The label accepts troponin and magnesium with the electrolytes (myocarditis during the febrile illness) and the evidence reads both; same decision as SYNC-CARD-P02.
- Scoring: none (recommended criterion; any call matching the old order still matches).

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 80, ECOG 1 during the febrile illness (fallback_tool_outputs.clinical_assessment). Why: rule 2: the library reports Karnofsky 100 with no complaints in a febrile man with influenza who collapsed today.
- `order_specialized_test {test_type: exercise_stress_test}`: not performed, deferred by the clinical team (followup_outputs[7] request_exercise_stress_test). Why: the library answers with a generic normal exercise test (10.4 METs) in a febrile patient with a type 1 Brugada pattern and fever-related polymorphic ventricular ectopy, in whom exercise testing is not done; the order is answered as deferred, as the stored drug challenge is.
- `order_echocardiogram {echo_type: exercise_echo}`: not performed, deferred by the clinical team (fallback_tool_outputs.echo). Why: same reason as the exercise test: the library reports a normal stress study without arrhythmia in a febrile patient with fever-related polymorphic NSVT.
- `order_microbiology {specimen: throat_swab}`: influenza A RNA detected, group A Streptococcus negative (fallback_tool_outputs.microbiology). Why: rule 3: the stored rapid antigen test is positive for influenza A; the library reports respiratory viral PCR not detected.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
