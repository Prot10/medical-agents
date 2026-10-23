# HEP-ENC-M09
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| d279f19b-bf5a-4594-83c8-fed93048a7d3 | FIXED | The lactulose must is now MUST-LACT, 2-3 soft bowel movements per day (`required_recommendations[2]`). The DI follow-up's "titrate to 2-4" warning is gone; the output was rewritten (`followup_outputs[2]`). No "2-4" remains in the case. |
| b56d3db7-33fd-4c74-ac9c-a197b9c1198a | FIXED | The "Microbiology" panel holding "Urine culture: No growth at 24 hours (final pending)" was deleted from the admission labs. The urine result now exists only in the `request_urine_specimen` follow-up, at one time point (no pyuria, no growth at 48 hours). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `action-3-interpret-labs`, `followup_outputs[0]` | The `interpret_labs` `{}` paracentesis criterion duplicated a8 and matched any labs call (C6). The ascitic block reported "Gram-negative rod, speciation pending" while its impression said "No organism isolated to date". | FIXED: a3 deleted. a8 has arguments `{"specimen": "ascitic_fluid"}`, the canonical label and the expected evidence "PMN 412 ... above the 250 threshold". The block has one time point: Gram stain negative, Gram-negative rods at 24 h with identification to follow, organism null; cell counts filled (WBC 680, PMN 412); ascitic albumin 0.6 consistent with SAAG 1.7 and serum albumin 2.3. |
| D | major | `action-4-search-medical-literature`, `followup_outputs[1]` | A required literature search citing EASL 2010 and AASLD 2014 (C4). | FIXED: deleted. Its content is now in MUST-SBP. |
| C | major | `ground_truth.diagnosis.accepted[0]`, HPI, PMH | "Child-Pugh B, MELD 15" (undated, in HPI and PMH). Computed: MELD 21, MELD-Na 25, Child-Pugh C 13 (C10). | FIXED: label "Child-Pugh C, MELD-Na 25 ... (ascitic PMN 412 cells/mm3)"; scores removed from HPI and PMH; score pearl added. |
| D | major | `patient.history_present_illness` | Timeline leak: "his white blood cell count was within normal limits, reassuring at first glance" gives a scored lab result and steers the reasoning (C13). | FIXED: removed; "Notably, he was afebrile on arrival." stays. |
| B | minor | `patient.neurological_exam.mental_status` | GCS 12 (E3V4M5), although asterixis is elicited on sustained arm extension, so he obeys commands. | FIXED: GCS 13 (E3V4M6). |
| B | minor | `initial_tool_outputs.labs` | "Exclusion studies" (magnesium, lactate with no values); template TSH 2.1 and zinc 82; INR and ammonia under LFTs; no CRP (C9). | FIXED: magnesium 1.8 mg/dL, lactate 1.9 mmol/L, TSH 1.8, zinc 61, CRP 46 mg/L (consistent with SBP); INR and ammonia in their own panels; summaries list only flagged values. |
| B | minor | `initial_tool_outputs.ct` | Empty findings; "restricted diffusion" on CT; "does not exclude early cerebral edema" (C8). | FIXED: normal finding plus the case's own mild cortical atrophy; impression "No acute intracranial abnormality. Mild generalized cortical atrophy." |
| B | minor | `initial_tool_outputs.microbiology`, `followup_outputs[1]` | Template "No organism isolated to date" with "pending". | FIXED: no growth at 48 h. `collected_before_antimicrobials` stays true, because the case gives ceftriaxone after sampling. |
| C | major | `followup_outputs[2]` (DI), `action-5-check-drug-interactions` | DI required with no management-changing interaction; ofloxacin alternative; lactulose 2-4; rifaximin; thiamine advice inside the DI. | FIXED: recommended (C5), placed last. New content: no cephalosporin interaction; hold diuretics during SBP; propranolol thresholds (EASL 2018, Baveno VII); PPI and allopurinol notes; nephrotoxin and sedative warnings. Expected evidence differs from the output text. |
| C | major | `assessment.required_recommendations` | A diagnostic step (paracentesis) listed as a must; ceftriaxone 1 g; rifaximin added at a first overt episode ("no prior episodes of overt HE"); 2-4 target; repeat tap at 48 h unconditional; no diuretic or NSBB plan, no SBP secondary prophylaxis, no transplant referral. | FIXED: MUST-SBP with albumin (bilirubin 4.2) and the conditional 48 h tap; culture must; MUST-LACT; MUST-THIA; diuretic and propranolol must; norfloxacin secondary prophylaxis; MUST-TX with alcohol-use assessment; pantoprazole review. Rifaximin removed. |
| C | minor | `assessment.prohibited_recommendations` | Benzodiazepine line framed for "alcohol withdrawal", although none is present; LP line with dashes. | FIXED: PROHIB-BZD; opioid line with acetaminophen up to 2 g per day; LP line kept as case-specific (no meningism, source found, coagulopathy) and consistent with `avoid-harm-1-analyze-csf`. |
| C | major | `ground_truth.differential` | "HE without identified infection" high and ICH and withdrawal moderate after the work-up (C14, ruling 7). | FIXED: all low, with the excluding results (PMN 412 with Gram-negative rods; CT without blood; undetectable ethanol, no withdrawal signs). |
| D | minor | `red_herrings[1]` | "Elevated ammonia confirms hyperammonemia consistent with HE"; field path pointed to `LFTs[6]`. | FIXED: K-AMM wording; path `labs.panels.Ammonia[0]`. Pearl 4 replaced by K-AMM. |
| A | minor | all `action_criteria` | Rationales repeated the labels; mixed citations; `before_antimicrobials` and `tests` arguments; nine-panel lab criterion (C7, C9, C17). | FIXED: per plan 3.1. Order: labs, blood, tap, urine, CT (optional), DI (recommended). Stop rule: labs, blood, tap, urine. |
| E | minor | `metadata.difficulty_rationale` | "paracentesis-as-labs, literature ... hepatology consult". | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

This is an afebrile SBP case with a normal white count. The work-up is core labs (CRP 46 added, ammonia once, no culture in the admission panel), blood cultures, diagnostic paracentesis and urine culture, all required because infection is the labelled precipitant. CT is optional and normal apart from mild atrophy. The medication review is recommended and comes last. The literature step and the duplicate labs paracentesis are gone. The ascitic report is internally consistent: PMN 412, Gram stain negative, Gram-negative rods at 24 hours with identification to follow. The label reads Child-Pugh C 13, MELD-Na 25. The musts are:
- ceftriaxone 2 g daily with albumin 1.5 and 1 g/kg, and a repeat tap at 48 hours if he does not improve;
- cultures before antibiotics;
- lactulose to 2-3 soft stools a day;
- thiamine before glucose;
- hold the diuretics, with thresholds for propranolol;
- SBP secondary prophylaxis;
- transplant referral with an alcohol assessment;
- review of the PPI.

Rifaximin is no longer mandated, because this is his first overt episode. The differential now rates the alternatives low, citing the results that exclude them.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1 (`[EASL_decomp_2018]` is used by the DI criterion).
- `accepted[0]` changed under ruling 3 (C10). No ICD or synonym change.

## Open questions for Andrea (judgment calls you could not settle)

- West Haven grade: the label says grade II. The exam ("difficult to rouse", E3, disoriented to time and place) could also be read as grade III. I kept grade II because "lethargic but arousable" is the grade II descriptor and no reviewer flagged it. Child-Pugh is C either way.
- The HPI's "Chest radiograph was clear" stays as pre-encounter ED history: a chest radiograph cannot be ordered in the core vocabulary, so it is not a scored-study leak.

## Verification

Adversarial verifier, 23 Oct 2026. Read the log, the full diff and the final case.
- Both notes confirmed fixed: no "2-4" anywhere; the admission panel has no culture row; the urine culture exists only in `request_urine_specimen` at one time point.
- Scores recomputed: MELD 21, MELD-Na 25 (Na 130); Child-Pugh C 13. MUST-SBP includes albumin correctly (bilirubin 4.2, creatinine 1.1). Ascitic block internally consistent (Gram stain negative, Gram-negative rods at 24 h, organism null; SAAG 2.3 - 0.6 = 1.7). The LP prohibition agrees with `avoid-harm-1-analyze-csf`, and no criterion requires an LP.
- Found and fixed, three items:
  1. **Grade versus exam (the worker's open question).** The HPI and the exam said "disoriented to time and place; oriented to person only". Under the AASLD/EASL 2014 operative criteria, disorientation to place is grade III, so the exam contradicted the labelled grade II. P01 and P02 in this batch resolved the same conflict by fixing the data, and ruling 3 says to fix the data, not the label. I did the same:
     - HPI: "lethargic, disoriented to time, and unable to give a reliable history";
     - `neurological_exam.mental_status`: "Disoriented to time (date, day and month); oriented to place and person".
     Label, Child-Pugh 13 and the differential are unchanged and now consistent. The open question is resolved unless Andrea prefers grade III; that would need the original exam, HE 3 points, and Child-Pugh 14, still C.
  2. **Fallback EEG.** `fallback_tool_outputs.eeg` was a normal EEG (PDR 9-10 Hz) in a patient with overt HE, while `metadata.fallback_tool_kinds.eeg` says "abnormal_nonspecific". An agent ordering an EEG would have received a report that contradicts the diagnosis. It is replaced by generalized theta slowing at 5-6 Hz with no epileptiform discharges. No criterion was added.
  3. **Fallback MRI.** It read "ventricles and sulci appropriate for age" against the CT's mild generalized cortical atrophy. It now states the mild atrophy.
- `perfect_agent.py HEP-ENC-M09 -v` passes; `case_io.py check` reports no failure naming the case.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

- `ground_truth.key_clinical_evidence[0]`: inserted the canonical pearl "HE is a clinical diagnosis: West Haven grade, evidence of liver disease and exclusion of other causes of altered mental status (ACG 2026; EASL 2022)." carried by the other 28 cases (auditor flag).

Checks: `perfect_agent.py` pass; `case_io.py check` schema and synonym guard OK, no test failure names this case; leak guard clean.
