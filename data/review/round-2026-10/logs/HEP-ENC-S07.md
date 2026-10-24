# HEP-ENC-S07
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| a4e6f322-2a12-44d9-aa4a-2a53f8996ca6 | FIXED | The naloxone challenge follow-up (`order_specialized_test`, trigger `request_naloxone_opioid_reversal`) deleted, with the difficulty text that relied on it ("partial naloxone reversal distinguishes opioid vs ammonia contribution"). Naloxone now appears only as a must: reserved for clear opioid toxicity, in small titrated doses because regular codeine risks withdrawal, and "not a diagnostic test for hepatic encephalopathy". The opioid-versus-HE question is answered by the exam (pupils 3 mm reactive, RR 16, asterixis) and EEG, stated in `differential[0]` and the new red herring on the opiate screen. |
| 409e1c57-932e-42bc-ac3a-53fa32a14a01 | FIXED | Blood (`action-7-order-microbiology`) and urine (`action-8-order-microbiology`) cultures are now recommended as an infection screen (afebrile 36.8 °C, WBC 5.4, no source), with specimen-only arguments (no `before_antimicrobials`, no test lists) and the case's own results as expected evidence; their blocks report one time point ("no growth at 48 hours") with `collected_before_antimicrobials` null, since no antimicrobial is given. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | blocker | `patient.clinical_history.medications` (codeine, glipizide) | Medication indications gave the answer: codeine "CONTRAINDICATED in cirrhosis (opioid accumulation, worsens HE)", glipizide "hypoglycemia risk in cirrhosis". | FIXED: "Abdominal pain", "Type 2 diabetes". |
| D | major | `patient.history_present_illness` | Timeline leaks (C13): ammonia 164, "EEG shows classic triphasic waves", "WBC is normal", "urine drug screen is positive for codeine/opiates". | FIXED: all removed; "He has had no fever" kept. |
| D | minor | `patient.neurological_exam.mental_status`, `.coordination` | Exam stated the grade ("West Haven grade 2-3") and an interpretation ("ataxia likely from encephalopathy rather than focal cerebellar lesion"). | FIXED: grade removed; "Drowsy, opens eyes to voice" added to explain E3; dysmetria described as bilateral and symmetric. |
| C | major | `ground_truth.diagnosis.accepted[0]` | "Grade II-III": the exam (somnolent, E3, disoriented to place and time, oriented to person only) meets grade III, so per plan 1.2 the upper bound applies; "ammonia 164" in the label; scores not derivable (C10: stated Child-Pugh C, MELD-Na 22). | FIXED: "Hepatic encephalopathy (West Haven grade III), hepatitis C cirrhosis (Child-Pugh C, MELD-Na 23), precipitated by constipation and codeine accumulation". Child-Pugh C 13, MELD 21, MELD-Na 23 in `key_clinical_evidence[0]`; the prior "MELD-Na 22" in the HPI and history is dated to his last hepatology review. ICD codes and synonyms unchanged. |
| B | major | `patient.clinical_history.past_medical_history[3]`, transplant panel | Prior HE recorded as one "grade 1" episode, while he takes rifaximin for secondary prophylaxis and the transplant panel counted two prior overt episodes. | FIXED: "Overt hepatic encephalopathy, two prior episodes (the last, grade 2, 4 months ago, resolved with lactulose; rifaximin added after it)". |
| C | major | `followup_outputs` (`request_lactulose_rifaximin`, `request_liver_transplant_evaluation`) | Serial ammonia 164 to 38 with stool counts after a lactulose increase, and a transplant "panel" (C1, C2). | FIXED: both deleted; content in MUST-LACT, rifaximin and MUST-TX musts. |
| C | major | `followup_outputs` (`request_hcv_daa_therapy`), `action-3-search-medical-literature`, `initial_tool_outputs.literature_search` | Required literature search with an echoing initial output (C4); the HCV follow-up stood in for a treatment plan and was wrong: it named glecaprevir/pibrentasvir as preferred in decompensated cirrhosis, where NS3/4A protease inhibitors are contraindicated. | FIXED: criterion, follow-up and initial output deleted; HCV must: sofosbuvir/velpatasvir (with ribavirin where tolerated), no protease inhibitor in Child-Pugh B or C, timing planned with transplant listing. |
| A | minor | `followup_outputs` (`request_sbp_paracentesis`, `interpret_labs`) | Ascites present but no paracentesis criterion; the tap was filed under `interpret_labs` with a "within normal limits" summary (C6). | FIXED: new required criterion `action-diagnostic-paracentesis` (`order_microbiology`, `ascitic_fluid`), expected "Ascitic PMN 114 cells/mm3, below the 250 cells/mm3 threshold for SBP"; the result moved to an `order_microbiology` follow-up `request_diagnostic_paracentesis` (ultrasound-guided tap of small ascites, cell counts, total protein 1.9 g/dL, ascitic albumin 1.1 g/dL from the existing SAAG 1.3, Gram stain, culture at 48 hours). |
| D | major | `initial_tool_outputs.drug_interactions`, `action-4-check-drug-interactions` | Empty DI template whose summary was the expected evidence (C5). | FIXED: initial null; one follow-up `check_codeine_glipizide_omeprazole`, placed last, with real content (codeine to morphine accumulation, glipizide hypoglycemia, PPI association with HE and SBP). Required per plan (codeine is a precipitant). |
| B | major | `initial_tool_outputs.labs` | "Exclusion studies" with magnesium and lactate "Within reference range"; template TSH 2.1 and zinc 82; no CRP; HCV genotype flagged abnormal; ethanol with the unit inside the value (C9). | FIXED: magnesium 1.9 mg/dL (BMP), lactate 1.3 mmol/L and CRP 4 mg/L added; TSH 2.6, zinc 61; genotype not flagged; ethanol "<10 (not detected)" mg/dL; summary and interpretation list every flagged value. |
| A | minor | `action-1-interpret-labs` | Nine named panels demanded (C9). | FIXED: two-alternative core; canonical label and rationale. |
| B | major | `initial_tool_outputs.ct` | Empty findings; "Bilateral globus pallidi hypodensity" (C8). | FIXED: canonical normal finding plus mild atrophy; hypodensity deleted. CT stays optional (no ACG trigger). |
| B | minor | `initial_tool_outputs.eeg` | Background 2.0-4.0 Hz theta-delta but a finding "theta slowing 4-6 Hz"; no clinical-correlation close. | FIXED: the slowing finding now matches the background (2.0-4.0 Hz); triphasic waves attenuated by alerting; impression closes with "consistent with a toxic-metabolic cause. Clinical correlation recommended." |
| C | major | `ground_truth.assessment.required_recommendations` | Lactulose 2-4 stools (C3); acetaminophen "2-3 g/day"; "address constipation directly" not checkable; no plan for glipizide or omeprazole; no transplant referral; DAA must without regimen constraints. | FIXED: 10 musts (precipitants with enema and impaction check, MUST-LACT, rifaximin, acetaminophen up to 2 g, naloxone only for toxicity, glipizide to insulin, omeprazole review, MUST-TX MELD-Na 23, HCV regimen, education of patient and wife). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Benzodiazepine line advised haloperidol (C12); generic LP prohibition with no LP; duplicate opioid lines. | FIXED: PROHIB-BZD; one opioid line with acetaminophen up to 2 g per day; NSAID line kept; LP and duplicate lines deleted. |
| C | major | `ground_truth.differential` | Codeine toxicity left moderate as primary cause; SBP "paracentesis if ascites" without the result; "recurrent HCV cirrhosis decompensation" is not an alternative cause of encephalopathy (C14). | FIXED: codeine toxicity as sole cause low (no toxidrome); SBP low (PMN 114); HCV entry replaced by glipizide hypoglycemia (glucose 84), intracranial hemorrhage and NCSE, each low with the excluding finding; alcohol very low. |
| C | minor | `ground_truth.red_herrings` | Empty although the opiate screen is a natural distractor. | FIXED: red herring on the positive urine opiate screen. |
| E | minor | criteria, citations, pearls, metadata | Rationale = label; free-text citations; "(AASLD 2014)" pearls; em dashes; metadata described the naloxone challenge and 4 required tools. | FIXED: one-sentence rationales with keys; pearls rewritten (score, clinical diagnosis with grade III criterion, K-AMM, precipitants, opioid pharmacology); metadata updated; no em dashes remain. |

## Changes, in one paragraph a physician can read before re-reviewing

The policy now requires the core laboratory work-up, a diagnostic paracentesis of the small ascites (ultrasound-guided; PMN 114 cells/mm3, no SBP) and a medication review, and recommends blood and urine cultures as an infection screen (afebrile, WBC 5.4) and the EEG; CT is optional. The naloxone challenge, the serial ammonia, the transplant panel and the literature searches (one of which wrongly recommended glecaprevir/pibrentasvir in decompensated cirrhosis) are gone. The patient block no longer gives away the answer: the codeine and glipizide indications no longer say "contraindicated in cirrhosis" or "hypoglycemia risk", and the HPI no longer reports the ammonia, EEG, WBC or opiate screen. The label reads West Haven grade III (somnolent, disoriented to place and time), Child-Pugh C (13), MELD-Na 23; the prior history now states two overt episodes, consistent with rifaximin. Labs replace the "Exclusion studies" block with magnesium 1.9 and lactate 1.3, add CRP 4, and use case-specific TSH and zinc. The CT loses the pallidal hypodensity and the EEG's two slowing frequencies agree. The drug check covers codeine accumulation, glipizide and omeprazole. Musts: stop codeine and relieve the constipation, lactulose to 2-3 stools, continue rifaximin, acetaminophen up to 2 g per day, naloxone only for true opioid toxicity, glipizide to insulin, omeprazole review, transplant referral (MELD-Na 23), HCV treatment with sofosbuvir/velpatasvir and no protease inhibitor, education of patient and wife. Prohibitions: sedatives, opioids, NSAIDs.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_decomp_2018]`, `[AASLD_ascites_2021]`.
- `accepted[0]` changed (grade II-III to III per plan 1.2; scores per C10); ICD codes and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- Grade III rather than the plan's implicit range: the exam (E3, oriented to person only) meets the AASLD 2014 operative criterion for grade III (disorientation also for space). Child-Pugh is C at either grade (13 vs 12 points).
- Paracentesis of small ascites is required (plan Q6); the output states an ultrasound-guided tap.
- New values are invented as C9 instructs and carry no diagnostic weight: magnesium 1.9, lactate 1.3, CRP 4, TSH 2.6, zinc 61, ascitic total protein 1.9 g/dL (above 1.5, so no primary SBP prophylaxis is triggered) and ascitic albumin 1.1 g/dL.
- The HCV must cites AASLD-IDSA HCV guidance, which is not in the HEP-ENC allow-list; it is a must (free text), not a criterion citation.

## Verification
Adversarial check (23 Oct 2026) of the final case against the log, the plan and the notes.
- Notes: both ids present and FIXED in the file: no naloxone follow-up, criterion or pearl remains (naloxone appears only in the must reserving it for clear opioid toxicity); blood and urine cultures recommended with specimen-only arguments and one-time-point blocks.
- Checked: MELD 21, MELD-Na 23 (Cr 1.0, bilirubin 6.8, INR 2.0, Na 134) and Child-Pugh C 13 (small ascites 2, grade III 3) recomputed; grade III supported by the exam (drowsy, E3, oriented to person only); SAAG 1.3 = 2.4 - 1.1; ascitic protein 1.9 so no primary prophylaxis is due; no ammonia, EEG, WBC or opiate result in the patient block; codeine and glipizide indications neutral; HCV must (sofosbuvir/velpatasvir, no protease inhibitor in Child-Pugh B/C) is correct per AASLD-IDSA; DI required (codeine is a precipitant) per plan; stop rule = the three required ids; CT optional with no ACG trigger; differential all low with the deciding finding; no em dashes or template residues.
- Found: nothing requiring a change. No edit made.
- perfect_agent -v and case_io check clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

- Leak guard (Andrea, 24 Oct 2026: any-query outputs must not repeat any criterion's expected evidence, including their own): `ground_truth.action_criteria[action-4-check-drug-interactions].expected_evidence` reworded as the conclusion a grader checks, in words not shared with the stored `check_drug_interactions` follow-up, whose report text is unchanged; clinical content unchanged.
- HCV must: free-text citation completed to "(AASLD-IDSA HCV guidance, 2023 update)" (`[AASLD_IDSA_HCV_2023]`, Clin Infect Dis 2023, doi:10.1093/cid/ciad319); content checked against it (sofosbuvir/velpatasvir with ribavirin in decompensated cirrhosis, no NS3/4A protease inhibitor in Child-Pugh B or C).

Checks: `perfect_agent.py` pass; `case_io.py check` schema and synonym guard OK, no test failure names this case; leak guard clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
