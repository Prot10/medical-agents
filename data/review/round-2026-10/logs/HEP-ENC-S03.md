# HEP-ENC-S03
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| bb58b696-1042-44c8-a7ae-9d2b4769f69c | FIXED | `initial_tool_outputs.microbiology` now holds blood cultures only (E. coli in 2 of 2 sets at 48 hours, ceftriaxone-susceptible, ciprofloxacin-resistant; organism, Gram stain, susceptibility and impression agree). The urinalysis moved to `labs.panels.Urinalysis` (leukocyte esterase 2+, nitrites positive, bacteria 3+); the serum ethanol line was removed from the micro block (already in the labs). The urine follow-up (`request_urine_specimen`) now reports pyuria and >100,000 CFU/mL E. coli with the same susceptibilities, so the urine culture is positive in the only place it appears. |
| 1720c3d7-2a65-42de-ad87-5234966b22e5 | DECLINED in part (by design, ruling 4; plan C16) / FIXED in part / ALREADY-FIXED in part | Treatment is scored through the musts, never a tool call (DECLINED). FIXED: MUST-SEPSIS (`required_recommendations[0]`), a specific antibiotic must (`[1]`), and a hemodynamic/renal must (`[3]`: stop diuretics and propranolol, albumin 1 g/kg for two days, monitor creatinine and urine output); the ceftriaxone now sits in the musts and in a real drug-check output, not only inside a step. ALREADY-FIXED: the "hepatology and infectious diseases referral" criterion with no tool no longer exists in the case. |
| 998fed4f-012a-49fb-8333-d928f96b15a6 | FIXED | "Exclusion studies" block deleted; lactate 3.4 mmol/L (H) and magnesium 1.9 mg/dL in `labs.panels.BMP`; the lactate is in the expected evidence and in the sepsis must. |
| 85b833e1-e475-4ef3-ba3d-85c02aa0b0f1 | FIXED | Recomputed from bilirubin 12.4, INR 2.8, creatinine 1.6, sodium 126: MELD 32, MELD-Na 35; Child-Pugh C, 15. `accepted[0]` "Child-Pugh C, MELD-Na 35"; the MELD 20 in `past_medical_history[0]` dated "at her last clinic review"; the MELD-Na 24 panel deleted; score pearl added. ICD unchanged. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `followup_outputs` (`request_lactulose_rifaximin`, `request_thiamine_empiric`, `request_liver_transplant_evaluation`) | Ammonia trend after treatment, "thiamine given" and MELD panels via `interpret_labs` (C1, C2). | FIXED: deleted; thiamine and transplant referral are musts. |
| D | major | `action-3-search-medical-literature`, `initial_tool_outputs.literature_search` | Literature output echoed the expected evidence (C4). | FIXED: criterion deleted, initial null. |
| A | major | `action-5-interpret-labs` | Duplicate paracentesis via `interpret_labs` `{}` (C6). | FIXED: deleted; `action-9-order-microbiology` canonical, "Ascitic PMN 186 cells/mm3, below the 250 cells/mm3 threshold for SBP". |
| B | major | ascitic follow-up (trigger renamed `request_diagnostic_paracentesis`) | PMN and SAAG without units; SAAG 2.0 impossible with serum albumin 2.0 g/dL. | FIXED: units, protein 0.8, ascitic albumin 0.4 (SAAG 1.6), Gram stain, no growth at 48 hours. |
| A | minor | `action-8`, `action-9`, `action-10-order-microbiology` | `before_antimicrobials`/`tests` arguments; template expected evidence and rationales (C7, C17). | FIXED: specimen-only arguments; required labels; case results as expected evidence. |
| D | major | HPI, `neurological_exam.additional` | Urinalysis result and ammonia 168 in the patient block (C13). | FIXED: removed. |
| B | minor | `neurological_exam.mental_status` | GCS V3 with "incomprehensible speech" (V2). | FIXED: "Inappropriate words when aroused" (GCS 11 unchanged). |
| B | minor | `initial_tool_outputs.labs` | Template TSH 2.1 and zinc 82; no CRP; culture results in the lab interpretation (C7, C9). | FIXED: TSH 1.9, zinc 70, CRP 142 mg/L; summary and interpretation list only flagged lab values. |
| A | minor | `action-1-interpret-labs` | Criterion demanded 10 panels (C9). | FIXED: two core alternatives plus `urinalysis` (plan labs+); case expected evidence. |
| C | major | `required_recommendations` | "Lactulose to 2-4 stools" and "rifaximin" as if new (she takes it) (C3); albumin "if SBP is present" (PMN 186: moot); no sepsis, kidney-injury, sodium, beta-blocker, thiamine or transplant instruction. | FIXED: MUST-LACT with rifaximin continued; MUST-SEPSIS; antibiotic must with the resistance pattern; kidney/diuretic/propranolol/albumin/sodium/potassium must; MUST-THIA; MUST-TX with alcohol treatment; culture must; outpatient UTI must kept. |
| C | minor | `prohibited_recommendations` | Haloperidol advice; generic LP prohibition (C12). | FIXED: PROHIB-BZD; opioids with acetaminophen up to 2 g per day; LP line deleted; aminoglycoside line kept; fluoroquinolone prohibition added. |
| C | minor | DI follow-up `check_uti_antibiotic_selection` | "14 days IV ceftriaxone" fixed duration; speculative UTI prophylaxis "to prevent HE"; no beta-blocker or diuretic content. DI was required (C5). | FIXED: 7-14 days with oral step-down, piperacillin-tazobactam option, fluoroquinolone/aminoglycoside/fosfomycin exclusions, propranolol and diuretic holds; DI recommended (plan). |
| C | minor | `ground_truth.differential` | SBP moderate after PMN 186 (C14); "Septic shock / bacteremia" as an alternative although bacteremia is part of the label and she is not in shock. | FIXED: SBP low; entry recast as sepsis-associated encephalopathy as the sole cause (moderate, coexists); HRS key features updated. |
| B | minor | `initial_tool_outputs.ct` | Empty findings (C8). | FIXED: canonical normal findings; CT optional. |
| B | minor | `fallback_tool_outputs.ecg` | "Normal sinus rhythm. Sinus bradycardia" at 68 bpm in a patient with HR 116. | FIXED: sinus tachycardia 114. |
| B | major | `metadata.difficulty_description` | Described another case ("hepatitis B cirrhosis, spontaneous bacterial peritonitis as precipitant"). | FIXED; difficulty rationale updated. |
| E | minor | `accepted[0]` | "recurrent UTI driving inflammatory hyperammonemia"; em dash. | FIXED: "precipitated by E. coli urosepsis with bacteremia (recurrent UTI after a recent ciprofloxacin course)". |

## Changes, in one paragraph a physician can read before re-reviewing

The label now reads West Haven grade III, Child-Pugh C (15), MELD-Na 35 (bilirubin 12.4, INR 2.8, creatinine 1.6, sodium 126), precipitated by E. coli urosepsis with bacteremia after a recent ciprofloxacin course. Each specimen has its own consistent block: blood cultures grow E. coli in 2 of 2 sets, the urine grows the same ceftriaxone-susceptible, ciprofloxacin-resistant E. coli, and the paracentesis (PMN 186, sterile) excludes SBP; the urinalysis sits in the labs. The HPI no longer gives the urinalysis or ammonia. The lactate is now 3.4 mmol/L (raised) with CRP 142. The ammonia-trend, thiamine and MELD panels, the literature search and the duplicate labs-paracentesis criterion are gone. Musts: sepsis care with cultures then antibiotic within one hour, ceftriaxone (or piperacillin-tazobactam pending susceptibilities) narrowed to the results, no fluoroquinolone or aminoglycoside; stop diuretics and propranolol, albumin for the kidney injury, potassium and a sodium-correction limit; lactulose to 2-3 soft stools with rifaximin continued; thiamine; transplant assessment with alcohol treatment once sepsis is controlled; outpatient UTI review. The drug check is recommended and now carries this content.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1.
- `accepted[0]` changed under ruling 3 (C10); ICD and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- The empirical antibiotic must allows piperacillin-tazobactam when a resistant organism is suspected after the recent ciprofloxacin course (EASL 2018 considers recent antibiotic exposure a risk factor for resistant bacteria); confirm whether ceftriaxone alone should be the expected first choice.
- The bacteremia was kept (the original block and drug check, and the reviewer's note, describe it); the blood-culture block now reports it at a single 48-hour time point.
- New values (CRP 142, lactate 3.4, magnesium 1.9, TSH 1.9, zinc 70, ascitic WBC 340, protein 0.8, albumin 0.4, piperacillin-tazobactam susceptibility) are invented to fit the case.

## Verification

Adversarial verification, 23 Oct 2026.

- Notes: all four ids in the table. bb58b696 fixed (blood, urine and ascitic blocks each one specimen and one time point; E. coli with the same susceptibilities in blood and urine; no "no growth" urine block left). 1720c3d7: partly declined by design, MUST-SEPSIS and the haemodynamic/renal must added, referral criterion absent (ALREADY-FIXED confirmed). 998fed4f: lactate 3.4 (H). 85b833e1: MELD 32.0 -> 32, MELD-Na 34.9 -> 35 (Cr 1.6, bilirubin 12.4, INR 2.8, Na 126), Child-Pugh 15 C; label, key evidence and history agree.
- Found and FIXED:
  - (B, minor, `patient.clinical_history.past_medical_history[4]`) "Prior HE grade 1 (6 months ago)" while she takes lactulose and rifaximin as "HE secondary prophylaxis", which follows an overt episode; the worker fixed the same defect in S04 but not here (ruling 2, class). Now "Prior overt hepatic encephalopathy (6 months ago), on lactulose and rifaximin since".
  - (C, minor, `ground_truth.differential`, "Sepsis-associated encephalopathy as the sole cause") likelihood moderate although its own key features say asterixis and liver failure point to HE precipitated by the sepsis (ruling 7). Now low; key features unchanged.
- Not changed, noted: the HPI calls 104/64 "hypotension" (pre-existing wording; relative hypotension in cirrhosis, the sepsis must covers it).
- `perfect_agent.py HEP-ENC-S03 -v` passes; `case_io.py check` clean for the case.

## Auditor (24 Oct 2026)

- `key_clinical_evidence[0]`: the template pearl "HE is a clinical diagnosis: West Haven grading + evidence of liver dysfunction + exclusion of other causes of AMS ... (AASLD 2014)" survived here (S02-S05 only) and is replaced by the M01 canonical text "HE is a clinical diagnosis: West Haven grade, evidence of liver disease and exclusion of other causes of altered mental status (ACG 2026; EASL 2022)." The ammonia half of the old sentence is already carried by the K-AMM pearl. Removes a superseded citation and an em dash.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

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

- `ground_truth.action_criteria[action-1-interpret-labs]`.alternatives: was [CBC, CMP, coagulation, ammonia, urinalysis] | [CBC, BMP, LFTs, coagulation, ammonia, urinalysis]; now [CBC, CMP, coagulation, ammonia, urinalysis, CRP] | [CBC, CMP, coagulation, ammonia, urinalysis] | [CBC, BMP, LFTs, coagulation, ammonia, urinalysis].
- Decision: serve: new first alternative (old order kept as an alternative). The label names CRP and the work-up searches for an infective precipitant (EASL 2022 / ACG 2026); CRP was not in the order, so the CRP the evidence reads was not returned.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: cognitive_screen}`: Cognitive screening could not be completed: the patient could not sustain attention or follow the test instructions. No valid score was obtained. (fallback_tool_outputs.clinical_assessment). Why: GCS 11, disoriented to person, place and time, responding only to stimulation with inappropriate words: no MoCA can be completed.
- `order_specialized_test {test_type: neuropsych_battery}`: Formal neuropsychological testing could not be administered at this level of arousal and attention. No domain scores were obtained. (fallback_tool_outputs.specialized_test). Why: GCS 11, disoriented to person, place and time, responding only to stimulation with inappropriate words: a battery cannot be administered.
- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 30, ECOG 4. Severely disabled, completely bed-bound and dependent for all care. (followup_outputs[request_performance_status]). Why: Karnofsky 100 / ECOG 0 contradicts an inpatient confused, bed- or chair-bound patient.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: Timed gait and balance testing was not possible: unable to stand or walk. (followup_outputs[request_gait_and_balance_timed]). Why: stored exam gait: unable to stand or walk.
- `order_specialized_test {test_type: speech_language_evaluation}`: Abnormal speech and language evaluation: articulation not assessable at this level of arousal; inappropriate words only when aroused; does not follow commands. (followup_outputs[request_speech_language_evaluation]). Why: stored exam speech: articulation not assessable at this level of arousal; inappropriate words only when aroused.
- `analyze_eeg {eeg_type: continuous_icu}`: Continuous EEG monitoring over 24 hours: 1. Continuous generalized fronto-predominant triphasic waves at 1.5-2.5 Hz with anterior-to-posterior phase lag ... (fallback_tool_outputs.eeg). Why: the stored routine EEG is abnormal; a prolonged recording cannot show a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: 48-hour ambulatory EEG: 1. Continuous generalized fronto-predominant triphasic waves at 1.5-2.5 Hz with anterior-to-posterior phase lag, positive phase-2 ... (followup_outputs[request_ambulatory]). Why: the stored routine EEG is abnormal; a 48-hour recording cannot be normal.
- `order_advanced_imaging {modality: MR_spectroscopy}`: Abnormal MR spectroscopy: marked reduction of myo-inositol (mI/Cr 0.16) and choline (Cho/Cr 0.50) with an increased glutamine-glutamate (Glx) peak; NAA ... (fallback_tool_outputs.advanced_imaging). Why: characteristic test of the condition: reduced myo-inositol and choline with raised Glx.
- `order_body_imaging {study: pelvis_abdomen_ultrasound}`: Abdominal and pelvic ultrasound with Doppler: 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal vein. 4. Splenomegaly (15.5 cm). 5. ... (fallback_tool_outputs.body_imaging). Why: cirrhosis with large-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_CT}`: Contrast-enhanced CT of the abdomen and pelvis (arterial and portal venous phases): 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal ... (followup_outputs[request_pelvis_abdomen_ct]). Why: cirrhosis with large-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_MRI}`: Contrast-enhanced MRI of the abdomen and pelvis: 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal vein; gastro-oesophageal varices. 4. (followup_outputs[request_pelvis_abdomen_mri]). Why: cirrhosis with large-volume ascites: the library reports a normal liver and spleen.
- `interpret_labs {panels: [peripheral_smear]}`: Normocytic, normochromic red cells with occasional target cells; neutrophilia with toxic granulation and a left shift; platelets reduced in number, of normal ... (fallback_tool_outputs.labs[peripheral_smear]). Why: stored CBC: platelets 68, WBC 16.8: 'adequate platelets' contradicts it.
- `interpret_labs {panels: [procalcitonin]}`: 4.8 (fallback_tool_outputs.labs[procalcitonin]). Why: febrile urinary infection with tachycardia, hypotension and WBC 16.8.

Checks: `perfect_agent.py` pass; `test_case_guards.py -k HEP-ENC-S03` pass; the map verifier serves every listed term from the case; the snapshot of the 322 previously case-answered orders is unchanged.

Lab prose (25 Oct 2026, same pass): the fallback-labs interpretation now gives the smear as one sentence headed `Peripheral blood smear:` (commas, no semicolons), so an order for another panel no longer receives smear fragments; the smear rows are unchanged.
