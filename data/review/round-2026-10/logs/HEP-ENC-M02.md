# HEP-ENC-M02
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 9037c7e6-c8e1-4af8-bc02-8036ff8952b1 | FIXED | Both benzodiazepine lines of `ground_truth.assessment.prohibited_recommendations` (the "do not prescribe ... use haloperidol" line and the "lowest doses of lorazepam ONLY for severe withdrawal" line) replaced by the single PROHIB-BZD-WD line (no scheduled or long-acting benzodiazepines; symptom-triggered lowest dose of lorazepam or oxazepam with monitoring of consciousness). The withdrawal must no longer recommends phenobarbital, gabapentin or clonidine. The drug-interaction follow-up (former step 4, `check_alcohol_withdrawal_risk`) no longer doses lorazepam: it is now `check_ceftriaxone_ciprofloxacin_propranolol` with a benzodiazepine warning consistent with the prohibition (C5). |
| c0f7b456-9ee5-41bf-b16c-d9a170d2dfaf | FIXED | Duplicate `interpret_labs` paracentesis criterion `action-5-interpret-labs` deleted (and from the stop rule). The single paracentesis criterion `action-9-order-microbiology` (required, `{"specimen": "ascitic_fluid"}`) expects "Ascitic PMN 310 cells/mm3, above the 250 cells/mm3 threshold for SBP"; the treatment plan moved to MUST-SBP (ceftriaxone, albumin 1.5 g/kg day 1 and 1 g/kg day 3, since creatinine 1.4 and bilirubin 5.2). |
| 0a2f64af-85e4-4452-aa5b-059960addfe5 | FIXED | Scores: the past medical history now gives the dated prior "MELD 18 at hepatology review 3 weeks ago" (matching the HPI); the transplant panel with MELD-Na 22 (`request_liver_transplant_evaluation`) deleted; `accepted[0]` reads Child-Pugh C, MELD-Na 28 and the components are in `key_clinical_evidence[2]` (Child-Pugh 14 points; MELD 25, MELD-Na 28 from creatinine 1.4, bilirubin 5.2, INR 2.2, sodium 130). CT: findings filled with the canonical normal text plus diffuse atrophy; "restricted diffusion" removed. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness`, `social_history.alcohol`, `neurological_exam.additional` | Serum ethanol 14 mg/dL (a scored labs result) stated three times in the patient block (C13). | FIXED: removed; "admits drinking the day before admission" kept. |
| C | major | `followup_outputs` (lactulose/rifaximin, thiamine, transplant panel) | Treatment response (ammonia 88 to 52 to 38), a thiamine level and a transplant score panel delivered through `interpret_labs` (ruling 4, C1, C2). | FIXED: deleted; content moved to musts (rifaximin restart, MUST-THIA, MUST-TX). |
| D | major | `initial_tool_outputs.literature_search`, `action-3-search-medical-literature` | Literature output echoed the expected evidence (C4). | FIXED: criterion deleted, initial output null. |
| C | major | `action-4-check-drug-interactions` | Required with a template expected evidence about "sedatives"; the concrete issue (sulfonamide allergy excludes co-trimoxazole SBP prophylaxis) was absent (C5, plan M02). | FIXED: required, alternatives name the SBP antibiotics and prophylaxis drugs; output flags co-trimoxazole as contraindicated, fluoroquinolone alternative, ciprofloxacin-propranolol, beta-blocker review in SBP, benzodiazepine warning. |
| C | major | `ground_truth.assessment.required_recommendations` | Lactulose 2-4 stools (C3); thiamine dose tied to a deleted lab; no secondary SBP prophylaxis though the allergy is the point of the drug check; no beta-blocker review during SBP with creatinine 1.4 and BP 102/68; no transplant referral; withdrawal must contradicted the benzodiazepine prohibition. | FIXED: MUST-SBP, culture timing must, MUST-LACT, rifaximin restart with a supply plan, MUST-THIA, fluoroquinolone secondary prophylaxis (no co-trimoxazole), daily BP and creatinine with propranolol held if SBP < 90 mmHg or AKI (Baveno VII), withdrawal monitoring with alcohol use disorder treatment after recovery (EASL ALD 2018), MUST-TX (MELD-Na 28). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Generic LP prohibition with no LP; acetaminophen dose unstated. | FIXED: LP line deleted; opioid line with acetaminophen up to 2 g per day; "do not delay antibiotics" kept (infection present); co-trimoxazole prohibition added (allergy). |
| B | major | `initial_tool_outputs.labs` | "Exclusion studies" with magnesium and lactate as "Within reference range"; template TSH 2.1 and zinc 82; no CRP; summary incomplete (C9). | FIXED: magnesium 1.7 mg/dL (BMP), lactate 1.9 mmol/L, CRP 64 mg/L (raised, consistent with SBP), TSH 2.6, zinc 61; summary and interpretation list every flagged value. |
| A | minor | `action-1-interpret-labs` | Criterion demanded 9 named panels. | FIXED: two alternatives with `toxicology` as the case extra (plan M02 Labs+). |
| B | minor | `initial_tool_outputs.microbiology`, ascitic and urine follow-ups | "No organism isolated to date" beside "Pending (24-48h)"; Gram stain listed but null; ascitic values without units (C7). | FIXED: one time point per block (no growth at 48 hours; culture-negative neutrocytic ascites), units, Gram stain, SAAG with ascitic albumin 0.2 g/dL; "collected before antimicrobials" true, since the case gives ceftriaxone after the cultures. |
| A | minor | `action-8`, `action-9`, `action-10-order-microbiology` | Arguments carried `before_antimicrobials` and test lists (C7). | FIXED: specimen only; required tier kept (WBC 12.4, infective precipitant); case-specific expected evidence. |
| B | minor | `initial_tool_outputs.eeg.impression` | "Benzodiazepine challenge not performed" in an EEG report; no clinical-correlation close. | FIXED: removed; close added. |
| C | minor | `ground_truth.differential` | "Septic encephalopathy from SBP" listed high as an alternative to the label it is part of; SDH entry assumed an "unwitnessed fall" the history does not give. | FIXED: sepsis-associated encephalopathy as the sole cause low; alcohol withdrawal kept moderate as a concurrent risk (not excluded by any result) with intoxication excluded by ethanol; SDH low citing the negative CT. |
| C | minor | `ground_truth.red_herrings[0]` | Correct interpretation used "ammonia 88" as proof of HE (C2). | FIXED: argument rests on asterixis, fetor, SBP and the rifaximin gap. |
| E | minor | criteria rationales and citations; `key_clinical_evidence`; `metadata` | Rationale = label; free-text citations; "(AASLD 2014)"; metadata called 37.9 °C fever and described deleted steps; "Mild facial symmetry intact". | FIXED: one-sentence rationales with keys; K-AMM and score pearl; metadata reworded; "Face symmetric". |

## Changes, in one paragraph a physician can read before re-reviewing

The policy requires the core labs with toxicology, blood and urine cultures before antibiotics, a diagnostic paracentesis (ascitic PMN 310 cells/mm3: SBP, culture-negative at 48 hours) and a drug check of the SBP antibiotics against his sulfonamide allergy; EEG is recommended and CT optional. The literature search, the serial ammonia panel, the thiamine panel, the transplant score panel and the duplicate `interpret_labs` paracentesis are gone, and the patient block no longer gives the ethanol result. The label reads Child-Pugh C (14 points), MELD-Na 28; the history keeps the dated MELD 18 from three weeks ago. Labs gain magnesium 1.7, lactate 1.9, CRP 64 and case-specific TSH and zinc in place of the "Exclusion studies" block; the CT has real findings without "restricted diffusion". The benzodiazepine contradiction is resolved with one line: no scheduled or long-acting benzodiazepines, symptom-triggered lowest-dose lorazepam or oxazepam for withdrawal. Musts: ceftriaxone with albumin (EASL 2018), cultures before antibiotics without delay, lactulose to 2-3 stools, rifaximin restart with a supply plan, thiamine before glucose, fluoroquinolone secondary SBP prophylaxis (no co-trimoxazole), daily BP and creatinine with propranolol held if hypotension or AKI, withdrawal monitoring and alcohol use disorder treatment, and transplant referral.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_decomp_2018]`, `[AASLD_ascites_2021]`, `[Baveno_VII]`.
- `accepted[0]` changed under ruling 3 (C10 scores); ICD codes and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- Plan M02 says "Delete 'A'" (a Child-Pugh A label). The case as it stood had no Child-Pugh A anywhere (it said C in the label and history); nothing to delete.
- The ascitic culture is reported negative at 48 hours (culture-negative neutrocytic ascites, treated as SBP) rather than inventing an organism; a positive culture would let the policy test culture-adjusted therapy, if you prefer that.
- New laboratory values (magnesium 1.7, lactate 1.9, CRP 64, TSH 2.6, zinc 61) are invented as C9 instructs.

## Verification

Checked (adversarial verifier, 23 Oct 2026): all three note ids (9037c7e6, c0f7b456, 0a2f64af) are in the table and fixed in the file (one benzodiazepine line, PROHIB-BZD-WD; no lorazepam dosing in the drug check; one `ascitic_fluid` criterion expecting PMN 310; MUST-SBP with albumin, justified by creatinine 1.4 and bilirubin 5.2; CT findings without "restricted diffusion"; the only other MELD is the dated "MELD 18 three weeks ago"). Recomputed: Child-Pugh C 14 (bilirubin 5.2, albumin 2.1, INR 2.2, moderate ascites, grade III), MELD 25, MELD-Na 28, consistent everywhere. Grade III matches the exam (GCS 11, disoriented x3). The ethanol result no longer appears in the patient block; cultures required (WBC 12.4, SBP) with `collected_before_antimicrobials` true and ceftriaxone given after them; SAAG 1.9 = 2.1 - 0.2; the drug check content agrees with the sulfonamide allergy and the medication list; secondary prophylaxis with a fluoroquinolone is consistent with the co-trimoxazole prohibition. The plan's "delete A" had nothing to act on in the edited file (no Child-Pugh A remains).

Found: the drug-check warning on the non-selective beta-blocker gave a sodium threshold of 125 mmol/L; EASL 2018 (and AASLD 2021) reduce or stop the NSBB with persistent hypotension, hyponatraemia below 130 mmol/L or AKI.

Changed: `followup_outputs[2].output.warnings[1]` (trigger `check_ceftriaxone_ciprofloxacin_propranolol`) now reads "sodium falls below 130 mmol/L". `perfect_agent.py` and `case_io.py check` clean.

## Auditor (24 Oct 2026)

- `action-1-interpret-labs`: `toxicology` replaced by `tox_screen` in both alternatives. The tool advertises only `tox_screen` (`toxicology` is an accepted alias that `BaseTool` does not rewrite), and `_contains_required` folds case and underscores only, so an agent ordering the advertised `tox_screen` failed this required criterion; checked by direct call. `tox_screen` is the corpus spelling (18 criterion alternatives against 8). Same fix in M02, S01, S06 and S08.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.
