# HEP-ENC-S08
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| cb1f2bae-6883-45e7-9a83-6c6ebae05ed1 | FIXED | The second toxicology panel (`initial_tool_outputs.labs.panels.Toxicology`, blood ethanol "Not detected", urine drug screen "Negative") deleted. The remaining panel, renamed `Toxicology`, keeps blood alcohol 142 mg/dL (reference range now "<10" instead of "0") and urine toxicology positive for ethanol; the core lab criterion now names `toxicology`. |
| 5dd96024-cbb1-4bb9-9fba-4a3ab26d515c | FIXED | One set of scores, derived from the printed values: Child-Pugh C (15: bilirubin 8.7, albumin 2.1, INR 2.8, moderate ascites, HE grade III, 3 points each), MELD 29, MELD-Na 32 (Na 128). `accepted[0]` now reads "Child-Pugh C, MELD-Na 32"; the derivation is `key_clinical_evidence[0]`; the "Child-Pugh B, MELD 18" in `past_medical_history[0]` is dated as his last clinic review; the follow-up giving MELD 26 / MELD-Na 29 (`request_liver_transplant_evaluation`) is deleted (C1); MUST-TX gives MELD-Na 32. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.history_present_illness` | "Blood was noted on rectal exam, confirming active lower GI blood loss": melena with BUN 64 and known varices indicates an upper GI source. | FIXED: "Melena was found on rectal examination."; label says "upper GI hemorrhage". |
| C | major | `followup_outputs` (`request_lactulose_rifaximin`, `request_thiamine_empiric`, `request_liver_transplant_evaluation`) | Treatment response (repeat ammonia 6 h after lactulose with stool counts), an empiric-thiamine panel and a transplant score panel delivered through `interpret_labs` (C1, C2). | FIXED: deleted; content in MUST-LACT, thiamine and MUST-TX musts. |
| C | major | `followup_outputs` (`request_continuous_eeg`) | Lorazepam 2 mg IV challenge during EEG "confirming non-ictal metabolic etiology" (C1, C8). | FIXED: deleted. The initial EEG already shows no epileptiform discharges; NCSE is excluded by the EEG, not by a benzodiazepine. |
| A | minor | `followup_outputs` (`request_mri_brain`) | MRI follow-up with no MRI criterion and Wernicke "excluded" by MRI (C8). | FIXED: deleted; the library answers an unrequested MRI. |
| D | major | `initial_tool_outputs.literature_search`, `action-3-search-medical-literature` | Literature output echoed the expected evidence (C4). | FIXED: criterion deleted, output null. |
| D | major | `initial_tool_outputs.drug_interactions`, `action-4-check-drug-interactions` | Empty DI template whose summary was the expected evidence (C5). | FIXED: initial null; one follow-up `check_ceftriaxone_metformin_lisinopril_propranolol`, placed last: ceftriaxone with the penicillin rash (low cross-reactivity, give with monitoring), metformin with lactate 4.2, propranolol and diuretics during the bleed, lisinopril contraindicated with ascites, terlipressin and sodium. Required per plan (C5, C12). |
| A | minor | `action-5-interpret-labs` | Duplicate `interpret_labs` `{}` paracentesis criterion (C6). | FIXED: deleted; single criterion `action-9-order-microbiology` (`ascitic_fluid`, required), expected "Ascitic PMN 180 cells/mm3, below the 250 cells/mm3 threshold for SBP". |
| B | major | ascitic follow-up | "Cell Count 180" and "PMN 180" (100% neutrophils), no units, culture "Pending" beside "No organism isolated to date" (C7). | FIXED: WBC 390, PMN 180 cells/mm3, total protein 1.2 g/dL, ascitic albumin 0.3 g/dL (SAAG 1.8 with serum albumin 2.1), Gram stain, culture no growth at 48 hours; trigger `request_diagnostic_paracentesis`. |
| C | minor | `action-8`, `action-10-order-microbiology` | Arguments carried `before_antimicrobials` and test lists; generic expected evidence (C7). | FIXED: required (WBC 14.2, GI bleed needing antibiotics), specimen-only arguments, canonical labels, case results; blocks report one time point, collected before antibiotics (ceftriaxone is in the musts). |
| B | major | `initial_tool_outputs.labs` | Ammonia range 11-35 in "umol/L" (C2); template TSH 2.1 and zinc 82; no CRP (C9). | FIXED: 11-51 µmol/L; TSH 1.8, zinc 57 µg/dL (low); CRP 38 mg/L added; summary and interpretation list every flagged value. |
| A | minor | `action-1-interpret-labs` | Nine named panels demanded (C9). | FIXED: two-alternative core plus `toxicology` (plan Labs+); canonical label and rationale. |
| D | minor | `initial_tool_outputs.eeg.impression`, `.ct.findings`, `.ecg.findings` | EEG impression "Non-convulsive status epilepticus excluded" (a clinical conclusion); CT atrophy "consistent with chronic liver disease and alcohol-related brain changes"; ECG "QTc ... common in cirrhosis (cirrhotic cardiomyopathy)" (interpretations beyond the modality); "uV". | FIXED: EEG states no epileptiform discharges or seizures and no EEG correlate of the jerks, "consistent with a toxic-metabolic cause", clinical correlation; CT and ECG findings descriptive; µV. |
| C | major | `ground_truth.assessment.required_recommendations` | "Endoscopy ... if bleeding source confirmed" without timing, vasoactive drug or airway; ceftriaxone without the allergy (C12); no lactulose target (C3); no rifaximin in a recurrent episode; no plan for metformin, lisinopril, propranolol, diuretics, magnesium, phosphate, withdrawal, SBP prophylaxis or transplant. | FIXED: 12 musts: MUST-VB with the penicillin-rash clause, intubation before endoscopy (Baveno VII), cultures before antibiotics, MUST-LACT, rifaximin, thiamine with dextrose for glucose 61, MUST-K with magnesium and phosphate, hold the five drugs and never restart lisinopril, withdrawal monitoring, primary SBP prophylaxis (protein 1.2 g/dL), alcohol-related hepatitis assessment, MUST-TX (MELD-Na 32) with alcohol treatment. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Benzodiazepine line advised haloperidol, while the differential advised "non-benzodiazepine-first" withdrawal management (C12); generic LP prohibition with no LP. | FIXED: PROHIB-BZD-WD; opioid line with acetaminophen up to 2 g per day; transfusion line rephrased (no transfusion above 8 g/dL, Baveno VII); LP line deleted. |
| C | major | `ground_truth.differential` | SBP moderate after PMN 180 (C14); withdrawal moderate with blood alcohol 142; SDH and Wernicke without the deciding findings; intoxication and NCSE (myoclonic jerks) not addressed. | FIXED: SBP, withdrawal, intoxication, SDH, NCSE and Wernicke all low, each with the finding that decides it. |
| C | minor | `ground_truth.red_herrings` | Empty although agitation in a drinker is the case's trap. | FIXED: red herring on the combative, alcohol-smelling presentation (sedation with benzodiazepines). |
| E | minor | criteria, citations, pearls, metadata | Rationale = label; free-text citations; "(AASLD 2014)" pearls; em dashes; metadata described a benzodiazepine challenge and 5 required tools. | FIXED: one-sentence rationales with keys; pearls rewritten (score, clinical diagnosis, K-AMM, precipitants, multiple precipitants, Baveno VII airway and prophylaxis); metadata updated; no em dashes remain. |

## Changes, in one paragraph a physician can read before re-reviewing

The policy now requires the core laboratory work-up with toxicology, blood and urine cultures before antibiotics (WBC 14.2, upper GI bleed), the diagnostic paracentesis (PMN 180 cells/mm3, no SBP) and a medication review; EEG is recommended (myoclonic jerks) and CT optional. The literature search, the duplicate labs paracentesis, the post-lactulose ammonia, the empiric-thiamine panel, the lorazepam EEG challenge, the transplant score panel and the MRI follow-up are gone. The HPI now describes melena (an upper GI source, not "lower GI blood loss"). The label reads West Haven grade III, Child-Pugh C (15), MELD-Na 32, precipitated by upper GI hemorrhage, hypokalemia, recent alcohol and lactulose non-adherence; "MELD 18" is dated to his last clinic review. Labs keep one toxicology panel (blood alcohol 142 mg/dL), use the 11-51 µmol/L ammonia range, add CRP 38 and replace the template TSH and zinc. The ascitic report now has a total WBC (390) distinct from the PMN (180), units and a final culture. The drug check covers ceftriaxone with the penicillin rash, metformin with lactate 4.2, lisinopril with ascites, propranolol and diuretics during the bleed. Musts: vasoactive drug, ceftriaxone (allergy not a contraindication), restrictive transfusion and endoscopy within 12 hours, intubation before endoscopy, cultures first, lactulose to 2-3 stools, rifaximin, thiamine with the dextrose, potassium, magnesium and phosphate, hold the five drugs, withdrawal monitoring, primary SBP prophylaxis, alcohol-related hepatitis assessment, transplant referral with alcohol treatment. Prohibitions: scheduled or long-acting benzodiazepines, opioids and sedatives, transfusion above 8 g/dL.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_decomp_2018]`, `[AASLD_ascites_2021]`, `[Baveno_VII]`.
- `accepted[0]` changed under ruling 3 (C10 scores, plan CENTRAL 6); ICD codes and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- PROHIB-BZD-WD is used although withdrawal is anticipated rather than present (blood alcohol 142 on arrival): he drinks daily, so symptom-triggered treatment will likely be needed within the admission, and the old haloperidol advice contradicted the case.
- The thiamine and folate values of the deleted `request_thiamine_empiric` follow-up were not moved into the admission labs (the plan does not ask for it in S08; thiamine is given empirically regardless).
- New values are invented as C9 instructs and carry no diagnostic weight: CRP 38, TSH 1.8, zinc 57, ascitic total WBC 390 and albumin 0.3 g/dL (derived from the existing SAAG 1.8).
- The intubation-before-endoscopy and alcohol-related hepatitis musts are new clinical content (Baveno VII; bilirubin 8.7 with AST 312 after daily heavy drinking); delete the second if the case should stay focused on the HE precipitants.

## Verification
Adversarial check (23 Oct 2026) of the final case against the log, the plan and the notes.
- Notes: both ids present and FIXED in the file: one toxicology panel (blood alcohol 142 mg/dL, urine ethanol positive), no "Not detected" panel; one score set, MELD 29, MELD-Na 32 (Cr 1.4, bilirubin 8.7, INR 2.8, Na 128) and Child-Pugh C 15 recomputed and identical in label, key evidence and MUST-TX; "MELD 18" dated.
- Checked: ammonia range 11-51 µmol/L; melena/upper GI source consistent in HPI, label and MUST-VB (ceftriaxone 1 g daily, Baveno VII, with the penicillin-rash clause); cultures required (WBC 14.2, bleed) with "collected before antibiotics" true only because the musts give ceftriaxone; ascitic WBC 390 / PMN 180, SAAG 1.8 = 2.1 - 0.3, protein 1.2 supports the primary prophylaxis must; PROHIB-BZD-WD agrees with the withdrawal must; lisinopril, metformin and diuretic holds agree between DI output and musts; stop rule = the five required ids; deleted lorazepam challenge and MRI follow-up are gone; no em dashes or template residues.
- Found: nothing requiring a change (the PMH does not list the prior HE episode the HPI describes; left as is, the HPI and the lactulose indication carry it). No edit made.
- perfect_agent -v and case_io check clean.

## Auditor (24 Oct 2026)

- `action-1-interpret-labs`: `toxicology` replaced by `tox_screen` in both alternatives. The tool advertises only `tox_screen` (`toxicology` is an accepted alias that `BaseTool` does not rewrite), and `_contains_required` folds case and underscores only, so an agent ordering the advertised `tox_screen` failed this required criterion; checked by direct call. `tox_screen` is the corpus spelling (18 criterion alternatives against 8). Same fix in M02, S01, S06 and S08.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.
