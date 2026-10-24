# HEP-ENC-S04
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 0ddd13be-4d2f-4d09-beb7-bbd030a2a046 | FIXED | Recomputed from bilirubin 14.8, INR 3.1, creatinine 2.1, sodium 129: MELD 36, MELD-Na 37; Child-Pugh C, 15 points (bilirubin, albumin 1.9, INR, moderate ascites and grade III HE each 3), as the reviewer computed. `accepted[0]` "Child-Pugh C, MELD-Na 37"; the MELD-Na 26 in `past_medical_history[0]` and the HPI is dated "at his last clinic review"; the "MELD-Na 26 / Child-Pugh 13" panel (`request_liver_transplant_evaluation`) is deleted; score pearl added. ICD unchanged. |
| a8504264-7337-4a7b-8ef3-beebe99a9b13 | FIXED | MUST-VB (`required_recommendations[0]`) now ends "the penicillin allergy (rash) is not a contraindication: cross-reactivity with ceftriaxone is low; give with monitoring" (C12); the empty DI block is replaced by a real follow-up `check_ceftriaxone_penicillin_allergy_metformin` that addresses the allergy first; DI criterion `action-4` is now required (plan: concrete issues) with that expected evidence; new prohibition "Do not withhold ceftriaxone because of the penicillin rash"; pearl on cross-reactivity added. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `followup_outputs` (`request_upper_gi_endoscopy`, `request_lactulose_rifaximin`, `request_thiamine_empiric`, `request_liver_transplant_evaluation`) | Endoscopic band ligation filed as a specialised test; ammonia, creatinine and lactate response to treatment; MELD panel (ruling 4, C1, C2). | FIXED: deleted. Endoscopy within 12 hours is in MUST-VB. The pre-treatment magnesium 1.4 and zinc 58 from the deleted nutrition panel moved into the core labs (case values kept, C9); thiamine and folate levels dropped (thiamine is a must). |
| D | major | `action-3-search-medical-literature`, `initial_tool_outputs.literature_search` | Literature output echoed the expected evidence (C4). | FIXED: deleted / null. |
| D | major | `initial_tool_outputs.drug_interactions` | Empty DI template whose summary was the expected evidence (C5). | FIXED: null; real follow-up placed last (ceftriaxone and allergy, metformin, propranolol, lisinopril, diuretics, terlipressin and sodium, thiamine, sedatives). |
| A | major | `action-5-interpret-labs` | Duplicate paracentesis via `interpret_labs` `{}` (C6). | FIXED: deleted; `action-9-order-microbiology` canonical with "Ascitic PMN 186 cells/mm3, below the 250 cells/mm3 threshold for SBP". |
| B | minor | ascitic follow-up (renamed `request_diagnostic_paracentesis`), blood and urine blocks | Values without units; "Pending, no growth at 48h"; template text (C7). | FIXED: units, Gram stain, one time point (48 h); urine microscopy added. |
| A | minor | `action-8`, `action-9`, `action-10-order-microbiology` | `before_antimicrobials`/`tests` arguments; template rationales (C7, C17). | FIXED: specimen-only; required labels (WBC 12.4); case results as expected evidence; culture must. |
| C | major | `required_recommendations` | No vasoactive drug, no endoscopy timing; "treat SBP if present" (PMN 186); "lactulose enemas" without a target (C3); "rifaximin" as if new; no airway, potassium/magnesium, lisinopril or transplant instruction. | FIXED: MUST-VB; airway must (GCS 10 with active upper GI bleed, intubate before endoscopy, as the S01 note rules for the same situation); stop metformin and hold propranolol, lisinopril and diuretics; potassium, magnesium and sodium-correction must; enemas then MUST-LACT with rifaximin continued; thiamine kept; MUST-TX with alcohol treatment. |
| C | major | `patient.clinical_history.medications` (lisinopril) | ACE inhibitor in decompensated cirrhosis with ascites, hypotension and kidney injury, never addressed. | FIXED: held in the must and in the drug check (EASL 2018). |
| D | major | `medications[Metformin].indication` | "Type 2 diabetes (CONTRAINDICATED in cirrhosis, lactic acidosis risk)": the case's teaching point inside the patient block. | FIXED: "Type 2 diabetes". |
| D | major | HPI, `neurological_exam.mental_status` | "Ammonia is 194 µmol/L" in the HPI (C13); "West Haven grade 3." in the exam (the grade the agent must assign). | FIXED: both removed. |
| B | minor | `past_medical_history[3]` | "Hepatic encephalopathy grade 1 (8 months ago)" while he takes lactulose and rifaximin as secondary prophylaxis "following an episode" (overt). | FIXED: "Overt hepatic encephalopathy (8 months ago), on lactulose and rifaximin since". |
| B | major | `accepted[0]` | "West Haven grade III-IV" with GCS 10, localizing to pain (grade III; plan 1.2). | FIXED: grade III. |
| B | minor | `initial_tool_outputs.labs` | "Exclusion studies" magnesium "within range" while the case's nutrition panel gave 1.4; template TSH 2.1 and zinc 82 against the case's 58; no CRP (C9). | FIXED: magnesium 1.4 (L), zinc 58 (L), TSH 2.4, CRP 18; summary and interpretation list flagged values only. |
| A | minor | `action-1-interpret-labs` | 9-panel criterion (C9). | FIXED: two core alternatives; case expected evidence. |
| B | minor | `initial_tool_outputs.ct` | Empty findings; "bilateral basal ganglia hypodensity" (cirrhotic pallidal change is a T1 MRI sign, not a CT hypodensity; C8). | FIXED: canonical normal findings plus mild atrophy; hypodensity deleted. |
| C | minor | `prohibited_recommendations` | Haloperidol advice and an absolute benzodiazepine ban in a daily drinker whose last drink was yesterday; generic LP prohibition; metformin line cited "sepsis"; transfusion line phrased as an instruction. | FIXED: PROHIB-BZD-WD; opioids with acetaminophen up to 2 g per day; LP line deleted; metformin and transfusion lines rewritten. |
| C | minor | `ground_truth.differential` | SBP moderate after PMN 186 (C14); "hepatorenal syndrome from hypovolemia" (HRS excludes shock) moderate. | FIXED: both low with the excluding facts; SDH and Wernicke key features updated. |
| B | minor | `fallback_tool_outputs.ecg` | Normal sinus rhythm 74 bpm with HR 122. | FIXED: sinus tachycardia 120. |
| E | minor | `metadata.difficulty_*`, criterion rationales, citations | "Aggressive ammonia reduction"; label-copy rationales (C17). | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The label reads West Haven grade III, Child-Pugh C (15), MELD-Na 37, precipitated by variceal hemorrhage, with metformin a separate concern (lactate 4.8 with kidney injury). The patient block no longer gives the ammonia, the West Haven grade or the "contraindicated" note on metformin; the prior HE episode is called overt, consistent with secondary prophylaxis. Required: core labs, blood and urine cultures, a diagnostic paracentesis (PMN 186, no SBP) and a medication review; EEG recommended; CT optional and without the pallidal hypodensity. The endoscopy "test", the treatment-response, nutrition and MELD panels and the literature search are gone; magnesium 1.4 and zinc 58 now sit in the core labs, with CRP 18. Musts: vasoactive drug, ceftriaxone with the penicillin-rash statement, restrictive transfusion and endoscopy within 12 hours (Baveno VII); airway protection before endoscopy; cultures before antibiotics; stop metformin and hold propranolol, lisinopril and the diuretics; potassium, magnesium and a sodium-correction limit; lactulose enemas then 2-3 soft stools with rifaximin continued; thiamine; transplant assessment with alcohol treatment. The benzodiazepine prohibition is the withdrawal version (last drink yesterday).

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1 (`[Baveno_VII]`, `[EASL_ALD_2018]` among them).
- `accepted[0]` changed under ruling 3 (C10, and grade III-IV to III per plan 1.2); ICD and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- PROHIB-BZD-WD was used instead of PROHIB-BZD (plan section 4 names neither for S04): he drinks daily and last drank yesterday (ethanol 48), so withdrawal is expected within 24-72 hours and an absolute benzodiazepine ban could be harmful.
- The airway must was added by analogy with the S01 reviewer note (GCS 10 with an active upper GI bleed); he has melena, not hematemesis, so you may prefer "consider" rather than "intubate".
- New values (CRP 18, TSH 2.4, ascitic RBC and Gram stain) are invented; magnesium 1.4 and zinc 58 come from the case's own deleted nutrition panel.

## Verification

Adversarial verification, 23 Oct 2026.

- Notes: both ids in the table. 0ddd13be: MELD 36.4 -> 36, MELD-Na 37.1 -> 37 (Cr 2.1, bilirubin 14.8, INR 3.1, Na 129), Child-Pugh 15 C; no "26" or "13" left as a current score. a8504264: the allergy is addressed in MUST-VB, the required DI output, a prohibition and a pearl, consistently.
- Cross-field: grade III supported (GCS 10, does not know his name); ascitic PMN 186 with SAAG 1.5 (1.9 - 0.4); blood and urine sterile; ethanol 48 with last drink yesterday fits PROHIB-BZD-WD; the airway must matches Baveno VII (intubation before endoscopy with altered consciousness); no avoided action matches a kept criterion.
- Found and FIXED (D, minor, `patient.history_present_illness`): the worker removed the metformin teaching note from the medication list but left the same cue in the HPI ("He also continues metformin despite cirrhosis."), which flags the red herring the case scores. Now "He also takes metformin for type 2 diabetes."
- `perfect_agent.py HEP-ENC-S04 -v` passes; `case_io.py check` clean for the case.

## Auditor (24 Oct 2026)

- `key_clinical_evidence[0]`: the template pearl "HE is a clinical diagnosis: West Haven grading + evidence of liver dysfunction + exclusion of other causes of AMS ... (AASLD 2014)" survived here (S02-S05 only) and is replaced by the M01 canonical text "HE is a clinical diagnosis: West Haven grade, evidence of liver disease and exclusion of other causes of altered mental status (ACG 2026; EASL 2022)." The ammonia half of the old sentence is already carried by the K-AMM pearl. Removes a superseded citation and an em dash.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.90
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

- `ground_truth.diagnosis.icd_codes[0]` K72.91 to K72.90: grade III (GCS 10) is not coma. Synonym check clean.

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
