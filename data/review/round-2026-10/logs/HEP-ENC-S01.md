# HEP-ENC-S01
Reviewer status: R1 not reviewed, R2 approved | Approved before this round: yes

Changes are limited to the real errors named in plan section 4 (S01) and the errors listed under Own findings.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| af008448-4abd-4572-972a-7183d2d0b079 | FIXED | `ground_truth.assessment.required_recommendations[5]` replaced by the C12 airway must: "Protect the airway: GCS 10 with a diminished gag reflex, agitation, active variceal bleeding and tense ascites; intubate for airway protection before endoscopy rather than waiting for a GCS below 8 (Baveno VII)." The endoscopy must (`[0]`) now also says "with the airway protected". |
| d4a0da8d-3c01-43ff-948d-d43b2892d10f | FIXED | Recomputed from the printed values (bilirubin 18.6, INR 3.2, creatinine 1.8, sodium 124): MELD 36, MELD-Na 38; Child-Pugh C, 15 points. `accepted[0]` now "Child-Pugh C, MELD-Na 38"; the MELD 22 in `past_medical_history[0]` and the HPI is dated "at his last clinic review"; the MELD-Na 28 panel (`request_liver_transplant_evaluation`) is deleted; a score pearl with the components is added to `key_clinical_evidence`. ICD codes unchanged. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `followup_outputs` (`request_lactulose_rifaximin`, `request_thiamine_empiric`, `request_liver_transplant_evaluation`) | Ammonia trend after treatment, an "IV thiamine administered" panel and a MELD panel delivered through `interpret_labs` (ruling 4; C1, C2). | FIXED: all three deleted. Thiamine and lactulose remain musts. |
| D | major | `action-3-search-medical-literature`, `initial_tool_outputs.literature_search` | Literature output echoed the expected evidence (ruling 5, C4). | FIXED: criterion deleted, initial output null. |
| D | major | `initial_tool_outputs.drug_interactions` | Empty DI template whose summary was the expected evidence (C5). | FIXED: initial null; real follow-up `check_propranolol_terlipressin_ceftriaxone` (hold propranolol and diuretics, terlipressin and the sodium of 124, no ceftriaxone interaction, thiamine before dextrose, no sedatives); DI stays recommended. |
| A | major | `action-5-interpret-labs` | Duplicate paracentesis criterion through `interpret_labs` with `{}` arguments (matched by the core labs), carrying treatment text (C6). | FIXED: deleted (and from the stop rule). The single paracentesis criterion `action-9-order-microbiology` (`{"specimen": "ascitic_fluid"}`, required) has the canonical label and "Ascitic PMN 342 cells/mm3, above the 250 cells/mm3 threshold for SBP". |
| B | major | ascitic follow-up (trigger renamed `request_diagnostic_paracentesis`) | Culture "Pending, E. coli at 48h" beside "E. coli isolated"; PMN and SAAG without units; SAAG 2.1 impossible with a serum albumin of 1.8 g/dL (C7). | FIXED: one time point (E. coli at 48 hours, ceftriaxone-susceptible), units, Gram stain, ascitic albumin 0.3 g/dL with SAAG 1.5 g/dL, protein 0.9 g/dL. |
| B | minor | `initial_tool_outputs.microbiology`, urine follow-up | "No growth reported at the time of this encounter" template (C7). | FIXED: blood "no growth at 48 hours (two sets)"; urine microscopy and "no growth at 48 hours". |
| A | minor | `action-8`, `action-9`, `action-10-order-microbiology` | `before_antimicrobials`/`tests` arguments; label-only rationales (C7, C17). | FIXED: specimen-only arguments; required labels (WBC 14.2, SBP); case expected evidence; culture timing must added. |
| C | major | `ground_truth.assessment.required_recommendations[0]` | Variceal bleeding without a vasoactive drug, and endoscopy without timing (Baveno VII). | FIXED: "Start a vasoactive drug now ... upper endoscopy with band ligation within 12 hours ... airway protected (Baveno VII)". Transfusion and ceftriaxone/albumin musts unchanged. |
| C | major | `required_recommendations[3]` | "Add rifaximin" although he already takes it; no lactulose target (C3). | FIXED: retention enema until oral or nasogastric dosing is safe, then MUST-LACT (2-3 soft stools); "Continue rifaximin". |
| C | major | `required_recommendations` | Spironolactone and furosemide not stopped in hemorrhagic shock with creatinine 1.8, sodium 124 and potassium 3.1; no potassium or sodium-correction instruction. | FIXED: new must (stop diuretics, potassium to 4.0 or more, sodium rise no more than 8 mEq/L in 24 hours). |
| C | minor | `prohibited_recommendations` | Benzodiazepine line advised haloperidol; generic LP prohibition with no LP; acetaminophen dose unstated (C12). | FIXED: PROHIB-BZD; LP line deleted; acetaminophen "up to 2 g per day". |
| B | major | `accepted[0]`, `neurological_exam.mental_status`, red herring, metadata | "West Haven grade III-IV" while he localizes pain and is combative (grade III; plan 1.2: a range needs the exam to support the upper bound); GCS E2V3M5 with "incomprehensible sounds" (V2) and "unable to state name correctly". | FIXED: grade III in the label, red herring and difficulty description; exam "Opens eyes to pain; responds to voice with inappropriate words" (E2 V3, GCS 10 unchanged). HE Child-Pugh points unchanged (3). |
| D | major | `patient.history_present_illness` | "His ammonia is 187 µmol/L" (scored lab in the HPI, C13); "febrile (37.8°C)". | FIXED: ammonia sentence removed; "with a temperature of 37.8°C". |
| B | minor | `initial_tool_outputs.labs` | "Exclusion studies" block with magnesium and lactate "Within reference range" in hemorrhagic shock; template TSH 2.1 and zinc 82; no CRP (C9). | FIXED: magnesium 1.8 mg/dL, lactate 3.9 mmol/L (H), CRP 68 mg/L (H), TSH 2.6, zinc 61; summary and interpretation list every flagged value. |
| A | minor | `action-1-interpret-labs` | Criterion demanded 9 panels (C9); the label's "ethanol 168" needs toxicology. | FIXED: two core alternatives plus `toxicology`; canonical label; case expected evidence. |
| B | minor | `initial_tool_outputs.ct` | Empty findings (C8). | FIXED: canonical normal findings; impression "No acute intracranial abnormality." CT stays optional with a rationale (no focal deficit; coagulopathy and found at home). |
| E | minor | `initial_tool_outputs.eeg.findings[0]` | Morphology sentence duplicated; "continuous during wakefulness" in a GCS 10 patient. | FIXED: one sentence; "continuous throughout the recording". |
| C | minor | `ground_truth.differential` | SDH left moderate after a normal CT (C14); hepatorenal syndrome moderate while he is in hemorrhagic shock (HRS-AKI cannot be diagnosed in shock). | FIXED: both low, with the excluding facts. |
| C | minor | `key_clinical_evidence[3]` | "SBP and variceal bleed coexist in roughly a third of severe HE cases" (unsupported figure). | FIXED: infection in about a fifth of cirrhotics admitted with GI bleeding; antibiotic prophylaxis (Baveno VII). Score pearl and K-AMM added. |
| B | minor | `red_herrings[0].correct_interpretation` | "ammonia 187 ... confirm HE" (ammonia does not confirm HE). | FIXED. |
| B | minor | `followup_outputs` telemetry (`request_cardiac_monitoring`) | Kept per plan, but it reported improvement "with transfusion and IV fluids" (treatment response), "HE autonomic dysfunction", and a non-vocabulary monitor type. | FIXED: 12-hour telemetry, sinus tachycardia 112-132, QTc 440, no arrhythmia; `monitor_type` "telemetry"; placed last as monitoring. |
| B | minor | `fallback_tool_outputs.ecg` | Normal sinus rhythm at 73 bpm in a patient with HR 124. | FIXED: sinus tachycardia 122, QTc 440. |
| E | minor | `ground_truth.action_criteria[*]`, `metadata.difficulty_*` | Label-copy rationales, free-text citations, description of deleted steps (C17). | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The case is unchanged in substance: grade III HE in Child-Pugh C alcoholic cirrhosis precipitated by variceal bleeding, E. coli SBP and alcohol. The label now reads West Haven grade III (he localizes pain and is combative) and Child-Pugh C, MELD-Na 38 (bilirubin 18.6, INR 3.2, creatinine 1.8, sodium 124); the MELD 22 in the history is dated as the last clinic review. The ammonia trend, thiamine and MELD panels, the literature search and the duplicate labs-paracentesis criterion are gone; the ascitic report now gives one time point (E. coli at 48 hours, ceftriaxone-susceptible, PMN 342) and a SAAG compatible with the serum albumin. The HPI no longer gives the ammonia and no longer calls 37.8°C febrile. Labs: magnesium 1.8, lactate 3.9 (raised, in shock), CRP 68, and non-template TSH and zinc. Musts: a vasoactive drug and endoscopy within 12 hours (Baveno VII), restrictive transfusion, ceftriaxone with albumin, lactulose enemas then 2-3 soft stools with rifaximin continued, thiamine before dextrose, the reviewer's airway must (intubate for airway protection before endoscopy), cultures before antibiotics, and stopping the diuretics with potassium replacement and a sodium-correction limit. The drug check is now a real output. SDH and hepatorenal syndrome are low in the differential. Telemetry stays as monitoring without treatment-response claims.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_decomp_2018]`, `[AASLD_ascites_2021]`, `[Baveno_VII]`.
- `accepted[0]` changed under ruling 3 (C10 scores, and grade III-IV to III per plan 1.2); ICD codes and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- `toxicology` was added to the core lab criterion although plan section 4 lists no extras for S01: the label itself cites ethanol 168, as in M02, S06 and S08, which the plan does give toxicology.
- The label changed from grade III-IV to grade III (plan 1.2 rule on ranges). If you prefer to keep a range, the exam would need a grade IV feature, which it does not have.
- Telemetry is kept (plan: keep F4 if clean) and placed after the drug check, following ROUND_POLICY (safety checks, then monitoring), rather than plan 3.2's "drug check last". It has no criterion.
- New values (CRP 68, lactate 3.9, magnesium 1.8, TSH 2.6, zinc 61, ascitic WBC 520, protein 0.9, albumin 0.3, telemetry rates) are invented to fit the case.

## Verification

Adversarial verification, 23 Oct 2026 (approved case).

- Notes: both ids in the table. af008448 fixed (airway must rewritten around the gag reflex and the bleed, Baveno VII states intubation before endoscopy with altered consciousness). d4a0da8d fixed: MELD 36.1 -> 36, MELD-Na 37.6 -> 38 (Na 124 bounded to 125), Child-Pugh 15 C; the label, key evidence and history agree, and no MELD 22/28 remains as a current score.
- Cross-field: ascitic block at one time point (E. coli at 48 h, PMN 342, SAAG 1.5 = 1.8 - 0.3), blood and urine sterile, ceftriaxone 2 g for SBP; grade III supported by the exam (E2V3M5, localizes, combative); SDH and HRS low after the work-up; DI output real and consistent with the allergies (none) and medications; telemetry follow-up has no criterion and no treatment-response claim.
- Found and FIXED (C, major, `ground_truth.assessment.required_recommendations[4]`): the case has a glucose of 58 mg/dL in a GCS 10 patient (in the labs, the expected evidence and the DI output, which already proposes dextrose), but no must corrected it; the only must was "IV thiamine 500 mg before any dextrose". Now: "Correct the glucose of 58 mg/dL with IV dextrose without delay, giving IV thiamine 500 mg first or with it (heavy alcohol use), and monitor capillary glucose." This is a missing required action (PATTERNS 1), so it justifies a change in an approved case.
- Not changed, noted: the urine drug screen reports "ethanol metabolites" (a standard UDS does not test ethanol; pre-existing, minor); the 1.5-2.5 Hz continuous triphasic EEG is unchanged from the approved version.
- `perfect_agent.py HEP-ENC-S01 -v` passes; `case_io.py check` clean for the case.

## Auditor (24 Oct 2026)

- `action-1-interpret-labs`: `toxicology` replaced by `tox_screen` in both alternatives. The tool advertises only `tox_screen` (`toxicology` is an accepted alias that `BaseTool` does not rewrite), and `_contains_required` folds case and underscores only, so an agent ordering the advertised `tox_screen` failed this required criterion; checked by direct call. `tox_screen` is the corpus spelling (18 criterion alternatives against 8). S01 is approved, but the `toxicology` term was added in this round (see the A row above), so this corrects the round's own change, not the approved policy. Same fix in M02, S01, S06 and S08.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.90
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

- `ground_truth.diagnosis.icd_codes[0]` K72.91 (hepatic failure with coma) to K72.90: grade III (GCS 10, rousable) is not coma; only S06 (grade IV) keeps K72.91. Synonym check clean.
- `required_recommendations`: added an alcohol-withdrawal must (ethanol 168 mg/dL, heavy daily drinking; symptom-triggered lorazepam or oxazepam if withdrawal develops, EASL ALD 2018) and MUST-TX (transplant assessment once bleed and SBP are controlled, MELD-Na 38, with alcohol use disorder treatment). Both were lost when the round deleted the case's transplant panel under C1 without the replacement must C16 requires; the other actively drinking Child-Pugh C cases (S04, S06, S08) carry them. PROHIB-BZD kept: it forbids benzodiazepines for agitation or sleep, which remains right; the new must covers withdrawal. Approved case: changed for a regression introduced this round.

Checks: `perfect_agent.py` pass; `case_io.py check` schema and synonym guard OK, no test failure names this case; leak guard clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-1-interpret-labs]`.alternatives: was [CBC, CMP, coagulation, ammonia, tox_screen] | [CBC, BMP, LFTs, coagulation, ammonia, tox_screen]; now [CBC, CMP, coagulation, ammonia, tox_screen, CRP] | [CBC, CMP, coagulation, ammonia, tox_screen] | [CBC, BMP, LFTs, coagulation, ammonia, tox_screen].
- Decision: serve: new first alternative (old order kept as an alternative). The label names CRP and the work-up searches for an infective precipitant (EASL 2022 / ACG 2026); CRP was not in the order, so the CRP the evidence reads was not returned.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.
- Approved case: changed for a real inconsistency (the policy's own order did not return what its evidence cites), so it goes back to re-review for this criterion only.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: cognitive_screen}`: Cognitive screening could not be completed: the patient could not sustain attention or follow the test instructions. No valid score was obtained. (fallback_tool_outputs.clinical_assessment). Why: GCS 10, combative, unable to state his name correctly or follow any command reliably: no MoCA can be completed.
- `order_specialized_test {test_type: neuropsych_battery}`: Formal neuropsychological testing could not be administered at this level of arousal and attention. No domain scores were obtained. (fallback_tool_outputs.specialized_test). Why: GCS 10, combative, unable to state his name correctly or follow any command reliably: a battery cannot be administered.
- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 30, ECOG 4. Severely disabled, completely bed-bound and dependent for all care. (followup_outputs[request_performance_status]). Why: Karnofsky 100 / ECOG 0 contradicts an inpatient confused, bed- or chair-bound patient.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: Timed gait and balance testing was not possible: too confused and uncooperative to stand. (followup_outputs[request_gait_and_balance_timed]). Why: stored exam gait: too confused and uncooperative to stand.
- `order_specialized_test {test_type: speech_language_evaluation}`: Abnormal speech and language evaluation: dysarthric; inappropriate words only; does not follow commands reliably. (followup_outputs[request_speech_language_evaluation]). Why: stored exam speech: dysarthric; inappropriate words only.
- `analyze_eeg {eeg_type: continuous_icu}`: Continuous EEG monitoring over 24 hours: 1. Continuous generalized fronto-predominant triphasic waves at 1.5-2.5 Hz with anterior-to-posterior phase lag. 2. ... (fallback_tool_outputs.eeg). Why: the stored routine EEG is abnormal; a prolonged recording cannot show a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: 48-hour ambulatory EEG: 1. Continuous generalized fronto-predominant triphasic waves at 1.5-2.5 Hz with anterior-to-posterior phase lag. 2. Generalized ... (followup_outputs[request_ambulatory]). Why: the stored routine EEG is abnormal; a 48-hour recording cannot be normal.
- `order_advanced_imaging {modality: MR_spectroscopy}`: Abnormal MR spectroscopy: marked reduction of myo-inositol (mI/Cr 0.16) and choline (Cho/Cr 0.50) with an increased glutamine-glutamate (Glx) peak; NAA ... (fallback_tool_outputs.advanced_imaging). Why: characteristic test of the condition: reduced myo-inositol and choline with raised Glx.
- `order_body_imaging {study: pelvis_abdomen_ultrasound}`: Abdominal and pelvic ultrasound with Doppler: 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal vein; recanalized paraumbilical vein. 4. (fallback_tool_outputs.body_imaging). Why: cirrhosis with large-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_CT}`: Contrast-enhanced CT of the abdomen and pelvis (arterial and portal venous phases): 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal ... (followup_outputs[request_pelvis_abdomen_ct]). Why: cirrhosis with large-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_MRI}`: Contrast-enhanced MRI of the abdomen and pelvis: 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal vein; gastro-oesophageal varices ... (followup_outputs[request_pelvis_abdomen_mri]). Why: cirrhosis with large-volume ascites: the library reports a normal liver and spleen.
- `interpret_labs {panels: [peripheral_smear]}`: Macrocytic red cells with occasional target cells and stomatocytes; neutrophilia with toxic granulation and a left shift; platelets reduced in number, of ... (fallback_tool_outputs.labs[peripheral_smear]). Why: stored CBC: platelets 56, MCV 104, WBC 14.2: 'adequate platelets' contradicts it.
- `interpret_labs {panels: [CDT]}`: 2.9 (fallback_tool_outputs.labs[CDT]). Why: 35 years of heavy drinking, drinking in the days before admission.
- `interpret_labs {panels: [procalcitonin]}`: 1.6 (fallback_tool_outputs.labs[procalcitonin]). Why: fever 37.8 C, WBC 14.2 and haemodynamic compromise.

Checks: `perfect_agent.py` pass; `test_case_guards.py -k HEP-ENC-S01` pass; the map verifier serves every listed term from the case; the snapshot of the 322 previously case-answered orders is unchanged.

Lab prose (25 Oct 2026, same pass): the fallback-labs interpretation now gives the smear as one sentence headed `Peripheral blood smear:` (commas, no semicolons), so an order for another panel no longer receives smear fragments; the smear rows are unchanged.
