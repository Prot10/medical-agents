# HEP-ENC-S05
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 55bba229-0455-4596-8c10-39f12c82e590 | FIXED | Recomputed from bilirubin 9.8, INR 2.4, creatinine 1.8, sodium 131: MELD 30, MELD-Na 32; Child-Pugh C, 15 points (bilirubin, albumin 2.2, INR, moderate ascites and grade III HE each 3), as the reviewer computed. `accepted[0]` "Child-Pugh C, MELD-Na 32"; the "Child-Pugh B, MELD 18" in `past_medical_history[0]` and the HPI is dated "at her last clinic review"; the "MELD-Na 18 / Child-Pugh 10, B/C borderline" panel (`request_liver_transplant_evaluation`) is deleted; score pearl added. ICD unchanged. |
| 2fd43a55-218b-4224-b97a-4eaf95e96d28 | FIXED | Each specimen now has its own block at one time point. `initial_tool_outputs.microbiology` is blood cultures only: "no growth at 48 hours (two sets)", organism null, no "E. coli isolated" impression. The urinalysis moved to `labs.panels.Urinalysis`. The urine follow-up (`request_urine_specimen`) reports pyuria with WBC casts and >100,000 CFU/mL E. coli at 48 hours, ceftriaxone- and ciprofloxacin-susceptible; the separate ceftriaxone/urosepsis follow-up that repeated it is deleted, so the urine culture is positive in the only place it appears. |
| 170d2c1e-6ee3-4a44-8b42-bb8380dad0b2 (filed on S06) | FIXED | Same defect in this case (urine positive in the micro block and step 2, "no growth" in step 6; colony count inside a "pending" result): resolved as for 2fd43a55, one urine block with identification at 48 hours. |
| 988c74d2-fcf4-4799-83bf-d3b8d83e8a81 (filed on S06) | FIXED | Same values and same request as 55bba229 (Child-Pugh C 15, MELD around 30, MELD-Na higher): resolved as above, MELD-Na 32. |
| 36bd67da-e34c-41de-ac47-f01d82bd6d7e (filed on S06) | FIXED | New required criterion `action-renal-ultrasound` (`order_body_imaging {"study": "pelvis_abdomen_ultrasound"}`) with an initial `body_imaging` report: enlarged right kidney with reduced corticomedullary differentiation (pyelonephritis), no hydronephrosis, no calculus, no renal or perinephric collection; known 1.8 cm segment VI HCC; patent portal vein; moderate ascites; splenomegaly. The must on antibiotics adds "drain any obstruction or collection the ultrasound shows"; a differential entry (obstructive pyelonephritis or renal/perinephric abscess, low) and a pearl state why. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `followup_outputs` (`request_lactulose_rifaximin`, `request_hbv_resistance_assessment`, `request_liver_transplant_evaluation`, `request_ceftriaxone_urosepsis`) | Ammonia trend after treatment, an HBV resistance panel, a MELD panel and a treatment-labelled culture repeat through tools (ruling 4; C1, C2). | FIXED: deleted. The susceptibilities now sit in the urine block; HBV DNA 340 on treatment and adherence are a must; transplant referral is MUST-TX. |
| D | major | `action-3-search-medical-literature`, `initial_tool_outputs.literature_search` | Literature output echoed the expected evidence (C4). | FIXED: criterion deleted, initial null. |
| D | major | `initial_tool_outputs.drug_interactions` | Empty DI template (C5). | FIXED: null; real follow-up `check_tenofovir_ceftriaxone_sulfonamide_allergy` placed last (tenofovir disoproxil every 48 hours at clearance 30-49 or switch to TAF/entecavir, never interrupted; no co-trimoxazole; furosemide tolerated; hold propranolol and diuretics; review omeprazole; no ceftriaxone interaction; no sedatives). `action-4` is now required (plan: renal antiviral dosing and sulfonamide allergy). |
| A | major | `action-5-interpret-labs` | Duplicate paracentesis via `interpret_labs` (C6). | FIXED: deleted; `action-9-order-microbiology` canonical, "Ascitic PMN 162 cells/mm3, below the 250 cells/mm3 threshold for SBP". |
| B | minor | ascitic follow-up (trigger renamed `request_diagnostic_paracentesis`) | Values without units; no ascitic albumin, Gram stain or time point. | FIXED: units, protein 0.9, ascitic albumin 0.8 (SAAG 1.4 with serum 2.2), Gram stain negative, no growth at 48 hours. |
| A | minor | `action-8`, `action-9`, `action-10-order-microbiology` | `before_antimicrobials`/`tests` arguments; template rationales (C7, C17). | FIXED: specimen-only arguments; required labels; case expected evidence; C7 culture must. |
| D | major | HPI, `neurological_exam.additional` | Urinalysis, ammonia 156 ("markedly elevated", with an em dash), triphasic EEG and normal CT in the HPI; urinalysis repeated in the exam (C13). | FIXED: removed. |
| B | minor | `neurological_exam.mental_status` | GCS V3 while the text describes confused speech (V4). | FIXED: GCS 12 (E3V4M5); grade III unchanged (somnolent, disoriented). |
| B | minor | `initial_tool_outputs.labs` | "Exclusion studies" block; template TSH 2.1 and zinc 82; no CRP; AFP inside the hepatitis B panel; culture results in the interpretation (C7, C9). | FIXED: magnesium 1.8, lactate 2.9 (H), CRP 186 (H) added; TSH 1.6, zinc 64; AFP in its own panel; urinalysis panel; summary and interpretation list flagged lab values only. |
| A | minor | `action-1-interpret-labs` | Criterion demanded many named panels (C9). | FIXED: two core alternatives plus `urinalysis` (plan labs+); case expected evidence. |
| B | minor | `initial_tool_outputs.ct` | Pallidal hypodensity on CT (C8). | FIXED: canonical normal findings plus mild atrophy; CT optional (no focal sign). |
| C | major | `required_recommendations` | Lactulose "2-4 stools" (C3); "albumin if SBP" (PMN 162, moot); no sepsis, kidney-injury, potassium, tenofovir dosing, SBP prophylaxis, omeprazole or transplant instruction. | FIXED: MUST-SEPSIS; ceftriaxone adjusted to susceptibilities with drainage if needed; culture must; diuretic/propranolol hold with albumin 1 g/kg and potassium; MUST-LACT with rifaximin continued; tenofovir renally adjusted, never stopped, HBV DNA and adherence; ciprofloxacin primary SBP prophylaxis (protein 0.9, bilirubin 9.8, creatinine 1.8) instead of co-trimoxazole; stop omeprazole unless indicated; MUST-TX (MELD-Na 32, HCC within Milan). |
| C | minor | `prohibited_recommendations` | Haloperidol advice; generic LP prohibition with no LP (C12). | FIXED: PROHIB-BZD; opioids with acetaminophen up to 2 g per day; LP line deleted; "do not stop HBV antiviral" kept; co-trimoxazole and nephrotoxic-drug prohibitions added. |
| C | minor | `ground_truth.differential` | SBP moderate after PMN 162 (C14); "bacteremia/sepsis" moderate with blood cultures sterile; alcohol without the ethanol result. | FIXED: SBP low; entry recast as sepsis-associated encephalopathy as the sole cause (moderate, coexists); HBV flare low (low-level viremia); alcohol very low (ethanol not detected); new obstructive pyelonephritis/abscess entry, low. |
| B | minor | `fallback_tool_outputs.ecg` | Normal sinus rhythm 82 bpm with HR 114. | FIXED: sinus tachycardia 112. |
| B | major | `metadata.difficulty_description`, `difficulty_rationale` | "SBP/UTI coexistence" (PMN 162 excludes SBP); described deleted steps. | FIXED: describes this case. |
| E | minor | `accepted[0]` | Child-Pugh B; em dash. | FIXED: "Hepatic encephalopathy (West Haven grade III), hepatitis B cirrhosis (Child-Pugh C, MELD-Na 32), precipitated by E. coli urosepsis (right pyelonephritis); ascites mandates SBP exclusion." |

## Changes, in one paragraph a physician can read before re-reviewing

The label now reads West Haven grade III, Child-Pugh C (15), MELD-Na 32 (bilirubin 9.8, INR 2.4, creatinine 1.8, sodium 131), precipitated by E. coli right pyelonephritis; the "Child-Pugh B, MELD 18" in the history is dated as the last clinic review. The HPI no longer gives the urinalysis, ammonia, EEG or CT. Each specimen has one block at one time point: blood cultures sterile at 48 hours, urine >100,000 CFU/mL E. coli (ceftriaxone- and ciprofloxacin-susceptible), paracentesis PMN 162 and sterile (no SBP); the urinalysis sits in the labs, with CRP 186 and lactate 2.9 added. A required renal and abdominal ultrasound (reviewer note filed on S06) shows a swollen right kidney without hydronephrosis or collection. The ammonia-trend, HBV-resistance, MELD and repeated-culture outputs and the literature search are gone; CT is optional and no longer shows a pallidal hypodensity. The drug check is required and real: tenofovir dosing for the kidney injury, the sulfonamide allergy (no co-trimoxazole; furosemide is tolerated), holding propranolol and diuretics, omeprazole. Musts: sepsis care, ceftriaxone narrowed to the results with drainage if needed, cultures before antibiotics, albumin and potassium with diuretics and propranolol held, lactulose to 2-3 soft stools with rifaximin continued, tenofovir continued and renally adjusted with HBV DNA and adherence checked, ciprofloxacin SBP prophylaxis, omeprazole review, transplant assessment (HCC within Milan).

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1.
- `accepted[0]` changed under ruling 3 (C10); ICD and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- The renal ultrasound is required and was added on the strength of note 36bd67da, filed on S06 (the reviewer describes this case's values: right loin pain, creatinine 1.8, bilirubin 9.8); please confirm the S06 notes belong to S05.
- Primary SBP prophylaxis with ciprofloxacin is a must (ascitic protein below 1.5 g/dL with bilirubin above 3 and creatinine above 1.2; EASL 2018); some would leave it to discharge planning.
- Tenofovir: the must allows either dose extension or a switch to tenofovir alafenamide or entecavir; confirm whether one should be expected.
- New values (CRP 186, lactate 2.9, magnesium 1.8, TSH 1.6, zinc 64, ascitic albumin 0.8, urine microscopy, the ultrasound measurements, ECG rate 112) are invented to fit the case.

## Verification

Adversarial verification, 23 Oct 2026.

- Notes: all five ids in the table (two on S05, three filed on S06). 55bba229 / 988c74d2: MELD 30.5 -> 30, MELD-Na 32.0 -> 32 (Cr 1.8, bilirubin 9.8, INR 2.4, Na 131), Child-Pugh 15 C. 2fd43a55 / 170d2c1e: blood sterile in its only block, E. coli only in the urine block, no "pending" beside a result. 36bd67da: required renal ultrasound with a consistent report (no hydronephrosis or collection; differential entry low).
- Cross-field: grade III supported (E3, disoriented to place and time); ascitic PMN 162 with SAAG 1.4 (2.2 - 0.8); tenofovir disoproxil every 48 h at clearance 30-49 is correct; ciprofloxacin primary SBP prophylaxis criteria (protein 0.9 with bilirubin above 3 and creatinine 1.8) are met; the sulfonamide allergy excludes co-trimoxazole and the DI output says furosemide is tolerated; HPI free of urinalysis, ammonia, EEG and CT results.
- Found and FIXED:
  - (B, minor, `patient.clinical_history.past_medical_history[4]`) "Hepatic encephalopathy grade 1 (5 months ago)" while she takes lactulose and rifaximin as "HE secondary prophylaxis" (same class the worker fixed in S04). Now "Overt hepatic encephalopathy (5 months ago), on lactulose and rifaximin since".
  - (C, minor, `ground_truth.differential`, "Sepsis-associated encephalopathy as the sole cause") moderate although blood cultures are sterile and its own key features point to HE precipitated by the sepsis (ruling 7). Now low.
- Not changed, noted: the history still calls the HCC "Barcelona A" (staged when she was Child-Pugh B); with Child-Pugh C now, BCLC stage depends on transplant candidacy, which the MUST-TX already addresses.
- `perfect_agent.py HEP-ENC-S05 -v` passes; `case_io.py check` clean for the case.

## Auditor (24 Oct 2026)

- `key_clinical_evidence[0]`: the template pearl "HE is a clinical diagnosis: West Haven grading + evidence of liver dysfunction + exclusion of other causes of AMS ... (AASLD 2014)" survived here (S02-S05 only) and is replaced by the M01 canonical text "HE is a clinical diagnosis: West Haven grade, evidence of liver disease and exclusion of other causes of altered mental status (ACG 2026; EASL 2022)." The ammonia half of the old sentence is already carried by the K-AMM pearl. Removes a superseded citation and an em dash.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

- HBV must: citation updated from "EASL 2017 hepatitis B guideline" to "EASL 2025 hepatitis B guideline" (`[EASL_HBV_2025]`, J Hepatol 2025, doi:10.1016/j.jhep.2025.03.018), which supersedes 2017; the content (tenofovir disoproxil interval by creatinine clearance or a switch to tenofovir alafenamide or entecavir) is consistent with it. Criterion order (required renal ultrasound before the optional CT) kept: obstructed pyelonephritis needs source control before an optional head CT.

Checks: `perfect_agent.py` pass; `case_io.py check` schema and synonym guard OK, no test failure names this case; leak guard clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `initial_tool_outputs.body_imaging.modality` "ultrasound with Doppler" -> `ultrasound` (a body-imaging modality term; the Doppler or contrast detail stays in the findings and the `contrast` field).
- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Minor non-specific finding.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
