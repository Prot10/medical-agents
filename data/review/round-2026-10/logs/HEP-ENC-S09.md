# HEP-ENC-S09
Reviewer status: R1 not reviewed, R2 approved | Approved before this round: yes (changes limited to real errors; each is listed below)

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 498272a4-5a8b-486f-ad2e-c33988cac9f4 | FIXED | One set of scores derived from the printed values: Child-Pugh C (14: bilirubin 4.6 3, albumin 2.4 3, INR 2.1 2, moderate ascites 3, HE grade III 3), MELD 25, MELD-Na 28 (Na 131). `accepted[0]` now reads "Child-Pugh C, MELD-Na 28"; derivation in `key_clinical_evidence[0]`; "Child-Pugh B, MELD 16" in `past_medical_history[0]` dated to his last transplant clinic review; the follow-up giving MELD 22 / MELD-Na 25 (`request_liver_transplant_evaluation`) deleted (C1). The transplant-team must now quotes MELD-Na 28. |
| d2b65d04-2478-457c-af46-3ee3825f36db | FIXED | The ascitic block (`followup_outputs[0]`, now trigger `request_diagnostic_paracentesis`) reports one time point that agrees with itself: `gram_stain` "Gram-negative rods", `organism` "Escherichia coli", susceptibility (cefotaxime, ceftriaxone, ciprofloxacin S), culture "Escherichia coli at 48 hours", and a specific numbered impression (PMN 380, Gram-negative rods, E. coli, SAAG 1.9, protein 1.1, collected before antibiotics). The E. coli identification comes from the deleted 48-hour repeat-tap panel, so no new organism was invented. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.clinical_history.medications`, `past_medical_history` | Sofosbuvir/velpatasvir listed as a current daily medication with the indication "SVR12 achieved": a completed course cannot be ongoing after SVR12. | FIXED: removed from medications; `past_medical_history[1]` "Hepatitis C treated with sofosbuvir/velpatasvir, sustained virologic response (SVR12) achieved". |
| C | major | `followup_outputs` (`request_lactulose_rifaximin`, `request_continuous_eeg`, `request_liver_transplant_evaluation`, `request_sbp_repeat_paracentesis`) | Treatment response through diagnostic tools (C1, C2): ammonia at 12 h and 24 h; a 24-hour EEG "improving from baseline"; a transplant score panel with AFP; a 48-hour repeat tap after antibiotics. | FIXED: all four deleted (plan: delete F2, F5, F6, and F4 because it is post-treatment). The 48-hour repeat tap is in the SBP must; the E. coli result moved to the initial tap report (see d2b65d04). |
| D | major | `initial_tool_outputs.literature_search`, `action-3-search-medical-literature` | Literature output echoed the expected evidence (C4). | FIXED: criterion deleted, output null. |
| A | minor | `action-5-interpret-labs` | Duplicate `interpret_labs` `{}` paracentesis criterion answered by the core labs, with an expected text ("start ceftriaxone + albumin") that is management (C6). | FIXED: deleted; single criterion `action-9-order-microbiology` (required), expected "Ascitic PMN 380 cells/mm3, above the 250 cells/mm3 threshold for SBP; Gram-negative rods, Escherichia coli on culture". |
| A | major | `action-4-check-drug-interactions` | Expected evidence was the generic template ("Sedating/CNS-depressant medications identified...") and did not match its own output (the sulfa/cefotaxime check). | FIXED: expected evidence and label describe the output; citation `[EASL_decomp_2018]`. Output unchanged (kept per plan), moved last. |
| B | minor | `followup_outputs[2].output.alternatives[0]` | The drug check offered "Ceftriaxone 1g IV q24h" while the SBP must gives 2 g daily. | FIXED: "Ceftriaxone 2 g IV every 24 hours"; the rest of the output unchanged. |
| A | minor | `action-8`, `action-9`, `action-10-order-microbiology` | Arguments carried `before_antimicrobials` and test lists that subset matching turns into mandatory sub-tests (C7). | FIXED: specimen-only arguments; required tier kept (fever 38.4 °C, WBC 11.8, SBP); case-specific expected evidence and canonical labels. |
| B | minor | `initial_tool_outputs.microbiology`, urine follow-up | Template "No organism isolated to date. Specimen taken before the first antimicrobial dose." with "No growth reported at the time of this encounter" (C7). | FIXED: one time point, "no growth at 48 hours"; urine microscopy added (no pyuria, bilirubin positive, consistent with the dark urine). |
| B | major | `initial_tool_outputs.labs` | Ammonia range 11-35 in "umol/L" (C2); "Exclusion studies" with magnesium and lactate "Within reference range" and no numbers; template TSH 2.1 and zinc 82 (C9). | FIXED: 11-51 µmol/L; magnesium 1.8 mg/dL (CMP) and lactate 1.6 mmol/L (inflammatory panel) with ranges; TSH 1.6, zinc 66; summaries list every flagged value. |
| A | minor | `action-1-interpret-labs` | Nine named panels demanded (C9). | FIXED: two-alternative core; canonical label and rationale. |
| C | major | `ground_truth.diagnosis.accepted[0]` | "Grade II-III" while the exam (somnolent, GCS 10, disoriented to time and place) meets grade III and the reviewer's own Child-Pugh count uses 3 HE points (plan 1.2: a range takes the upper bound when the exam supports it). | FIXED: "West Haven grade III". ICD codes and synonyms unchanged. |
| C | major | `ground_truth.assessment.required_recommendations` | Lactulose 2-4 stools (C3); "albumin per protocol" not checkable; no secondary SBP prophylaxis plan in a patient whose sulfa anaphylaxis excludes co-trimoxazole; no plan for carvedilol with creatinine 1.6 or for the PPI. | FIXED: MUST-SBP with albumin (creatinine above 1, bilirubin above 4) and the 48-hour repeat tap, cultures before antibiotics, MUST-LACT, rifaximin, creatinine and carvedilol monitoring (Baveno VII), long-term norfloxacin or ciprofloxacin prophylaxis (no co-trimoxazole), omeprazole review, transplant-team update with MELD-Na 28. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Benzodiazepine line advised haloperidol (C12); generic LP prohibition with no LP; acetaminophen dose unstated. | FIXED: PROHIB-BZD; opioid line with acetaminophen up to 2 g per day; LP line deleted; co-trimoxazole prohibition added (sulfa anaphylaxis). |
| E | minor | criteria rationales, citations, pearls | Rationale = label; free-text citations beside keys (C17); "(AASLD 2014)" pearl; no ammonia pearl. | FIXED: one-sentence rationales with keys; pearl 1 cites ACG 2026 / EASL 2022; score pearl and K-AMM added. Metadata difficulty rationale updated. |

Not changed (approved case, no error found): HPI, exam, CT and initial EEG reports, the drug-interaction output apart from the ceftriaxone dose, differential, avoided actions.

## Changes, in one paragraph a physician can read before re-reviewing

The policy keeps its approved shape (core labs, blood and urine cultures, the diagnostic paracentesis and the sulfa-allergy antibiotic check required; EEG recommended; CT optional) minus the literature search and the duplicate labs paracentesis. The serial ammonia, the 24-hour EEG, the transplant score panel and the 48-hour repeat tap are gone because they report the response to treatment; the repeat tap is now part of the SBP must. The ascitic report agrees with itself: Gram-negative rods, E. coli at 48 hours with susceptibilities, PMN 380. Sofosbuvir/velpatasvir is no longer a current medication (his treatment ended with SVR12). The label reads West Haven grade III, Child-Pugh C (14), MELD-Na 28. Labs use the 11-51 µmol/L ammonia range and give numbers for magnesium (1.8) and lactate (1.6). Musts: ceftriaxone (or cefotaxime) with albumin on days 1 and 3 and a repeat tap at 48 hours if no improvement, cultures first, lactulose to 2-3 stools, rifaximin, carvedilol review with creatinine monitoring, long-term norfloxacin or ciprofloxacin prophylaxis, omeprazole review, transplant-team update. Prohibitions: sedatives, opioids, co-trimoxazole.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_decomp_2018]`, `[AASLD_ascites_2021]`.
- `accepted[0]` changed under ruling 3 (C10 scores; grade range to III per plan 1.2); ICD codes and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- The approved case is changed beyond the plan's S09 list in four places, each a real error: the ongoing sofosbuvir/velpatasvir after SVR12, the DI criterion's expected evidence that did not match its output, the "Exclusion studies" values without numbers, and the label's grade range. Revert any you consider churn.
- The ascitic report now gives the final E. coli at 48 hours (the plan allowed this or "culture pending"); this keeps the 48-hour convention used by every other block in the condition.
- New values (magnesium 1.8, lactate 1.6, TSH 1.6, zinc 66, ascitic albumin 0.5 g/dL derived from the existing SAAG 1.9) carry no diagnostic weight.

## Verification
Adversarial check (23 Oct 2026) of the final case against the log, the plan and the notes; approved case, so only real errors were considered.
- Notes: both ids present and FIXED in the file: Child-Pugh C 14 and MELD 25 / MELD-Na 28 (Cr 1.6, bilirubin 4.6, INR 2.1, Na 131) recomputed and identical in label, key evidence and the transplant-team must; the ascitic block (Gram-negative rods, E. coli at 48 hours with susceptibilities, PMN 380) agrees with itself and with the criterion's expected evidence.
- Checked the churn: the HPI, exam, CT, EEG and differential are unchanged from the approved version (git diff); the changes outside the plan list (sofosbuvir/velpatasvir moved from current medications to history after SVR12, DI expected evidence matched to its output, numeric magnesium and lactate, grade III) are each a real error and logged. MUST-SBP includes albumin (Cr above 1, bilirubin above 4) and the 48-hour repeat tap; co-trimoxazole is prohibited consistently with the sulfa anaphylaxis; stop rule = the five required ids.
- Not changed (approved text, not a real error): pre-existing em dashes and "uV" in unchanged strings, the fallback ECG rate (65 vs HR 88), the differential's instruction-style key features.
- Found: nothing requiring a change. No edit made. perfect_agent -v and case_io check clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.
