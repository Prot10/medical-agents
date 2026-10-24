# HEP-ENC-M08
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 18b8f3eb-0dfc-403c-9717-174f0b8a9811 | FIXED | The DI output no longer offers "continue sorafenib with anti-diarrheal (loperamide)". `followup_outputs[2]` warns that loperamide counteracts lactulose. The must is "Hold sorafenib until the diarrhea settles, then decide with oncology whether to resume it at a reduced dose; avoid loperamide while lactulose treats HE" (`required_recommendations[6]`). The prohibitions are "Do not give loperamide while lactulose is treating HE" and "Do not resume sorafenib at full dose ...". Nothing in the case now both recommends and forbids an antidiarrheal. |
| 391bf9ac-87c1-4e37-abba-1f8d554ea43d | FIXED | Source search: the labs now carry a urinalysis (negative), which is also in the core-lab criterion arguments. The urine culture (`action-10-order-microbiology`) is required. New must `required_recommendations[3]`: chest radiograph, examination and stool C. difficile testing, with empirical antibiotics if the fever persists without a source. A chest radiograph and a stool specimen cannot be ordered in the core vocabulary, so they are musts (see CENTRAL). Red herring `red_herrings[1]` no longer withholds antibiotics. AFP: the 3-month AFP panel follow-up is deleted, the prior AFP 1620 ng/mL stays as dated history in `patient.neurological_exam.additional`, the current AFP 2840 stays in the admission labs (`panels.Tumour markers`), and an oncology restaging must addresses the rise (`required_recommendations[7]`). |
| fa503581-0eb8-46bd-95a2-e0af7de59a9c | FIXED | The serial ammonia follow-up `request_lactulose_rifaximin` (86 to 52 to 34) is deleted. One admission ammonia (86, range 11-51) stays in `panels.Ammonia`. The K-AMM pearl was added, and the differential no longer cites "ammonia elevation" or "rapid lactulose response". |
| 8479a4e1-ad25-4ecf-b4ec-6b3094a233e4 | FIXED | The lactulose must targets 2-3 soft bowel movements per day (ACG 2026 rec. 10; EASL 2022) and avoids over-titration (`required_recommendations[5]`). It is adapted to the case: no loading doses while he already has 3-5 watery stools a day. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `action-5-interpret-labs`, `action-9-order-microbiology`, `followup_outputs[0]` | The paracentesis was duplicated: an `interpret_labs` `{}` criterion matched any labs call, and its expected text conflicted with the microbiology one (C6). The ascitic block read "No growth at 5 days" beside "No organism isolated to date". | FIXED: a5 deleted. a9 is kept with arguments `{"specimen": "ascitic_fluid"}` and the canonical label, expected evidence and rationale. The output is renamed `request_diagnostic_paracentesis`, with one time point (no growth at 48 h), cell counts (WBC 410, PMN 188), total protein 1.7, and an ascitic albumin of 0.6 that is consistent with the serum albumin of 2.3 and the SAAG of 1.7. |
| C | major | `ground_truth.diagnosis.accepted[0]`, `past_medical_history[0]` | Scores were not derivable: "Child-Pugh B, MELD 16". The computed values are MELD 23, MELD-Na 25, Child-Pugh C 14 (C10). The label grade was "II-III". | FIXED: the label now reads "West Haven grade III ... Child-Pugh C, MELD-Na 25 ... concurrent fever with SBP excluded (ascitic PMN 188)". The exam supports the upper bound (disoriented to time and place, eyes open to voice), so the plan rule 1.2 sets grade III. The undated score was removed from the PMH, and a score pearl was added. |
| B | minor | `patient.neurological_exam.mental_status` | GCS 12 (E3V4M5), although he holds his arms out for asterixis and attempts serial 7s, so he obeys commands. | FIXED: GCS 13 (E3V4M6). |
| D | major | `action-3-search-medical-literature`, `initial_tool_outputs.literature_search` | A literature criterion whose initial output echoed its expected evidence (C4). | FIXED: the criterion was deleted and the initial output set to null. |
| C | major | `followup_outputs` (`order_advanced_imaging` `request_mri_brain_sorafenib_pres`, `interpret_labs` `assess_hcc_prognosis`) | An MRI with no criterion, filed under advanced imaging (C8), and an AFP/MELD panel used as a prognosis step (C1). | FIXED: both deleted. The fallback library answers an unrequested MRI. |
| C | major | `followup_outputs[2]` (DI) | Prescriptive alternatives and BCLC text, "Child-Pugh B acceptable", no QT warning despite K 2.8 and Mg 1.5, and nothing on spironolactone or omeprazole. | FIXED: real content (sorafenib QT with low K and Mg; sorafenib not recommended in Child-Pugh C; spironolactone with K replacement; omeprazole risks in cirrhosis; no lactulose or rifaximin interaction; loperamide and sedative warnings). Recommended, placed last. |
| B | minor | `initial_tool_outputs.labs` | An "Exclusion studies" lactate with no value; template TSH 2.1 and zinc 82; AFP, INR and ammonia filed under LFTs; no CRP; interpretive summary entries ("AKI on CKD", "HCC marker elevated") (C9). | FIXED: lactate 1.7; TSH 2.7; zinc 63; CRP 38 mg/L (febrile); urinalysis panel; AFP, INR and ammonia in their own panels; summaries list only flagged values without interpretation. |
| B | minor | `initial_tool_outputs.ct` | Empty findings, "restricted diffusion" on CT, and an MRI-sensitivity essay (C8). | FIXED: canonical normal CT. |
| D | minor | `initial_tool_outputs.eeg.findings[1].morphology` | "not fully classic but suggestive". | FIXED: "not fully classic". |
| B | minor | `initial_tool_outputs.microbiology`, `followup_outputs[1]` | Template "No organism isolated to date. Specimen taken before the first antimicrobial dose" with no antibiotic in the case. | FIXED: one time point (no growth at 48 h); `collected_before_antimicrobials` null. |
| C | major | `assessment.required_recommendations` | Lactulose 2-4; no fever source search; magnesium and potassium must without a target; AKI must with no diuretic withdrawal while he takes spironolactone; no C. difficile testing despite diarrhoea with fever on a PPI; PPI with no indication. | FIXED: MUST-PRECIP; K/Mg must (target 4.0, ECG, hold spironolactone); AKI must (EASL 2018); source search must; culture must (required tier); lactulose must; sorafenib must; oncology must; omeprazole deprescribing must. |
| C | minor | `assessment.prohibited_recommendations` | The benzodiazepine line recommended haloperidol; generic LP line; acetaminophen dose not stated (C12). | FIXED: PROHIB-BZD, the opioid line with acetaminophen up to 2 g per day, the loperamide line, and a sorafenib full-dose line. LP line deleted. |
| C | minor | `ground_truth.differential` | SBP moderate after PMN 188 (C14); sorafenib toxicity excluded by a "rapid lactulose response" the case no longer shows; ICD G92 for PRES. | FIXED: SBP low with excluding results; PRES entry with BP 126/76 and ICD I67.83; sepsis-associated encephalopathy from another source added (low); brain metastasis ICD C79.31 with CT. |
| A | minor | all `action_criteria` | Rationales repeated the labels; mixed citation strings; `before_antimicrobials` and `tests` arguments; the lab criterion demanded nine panels (C7, C9, C17). | FIXED: per plan 3.1. Order: labs, blood cultures, tap, urine, CT (optional), EEG (recommended), DI (recommended). Stop rule: labs, blood, tap, urine. |
| E | minor | `metadata.difficulty_description`, `difficulty_rationale` | "borderline SBP PMN 188", "PRES vs HE", "5 required tools (labs, CT, lit ...)". | FIXED: reworded to the rebuilt case. |

## Changes, in one paragraph a physician can read before re-reviewing

The case is now graded West Haven III (disoriented to time and place, eyes open to voice; GCS corrected to 13 because he obeys commands), Child-Pugh C 14, MELD-Na 25. The work-up has four required steps (core labs with urinalysis, blood cultures, diagnostic paracentesis, urine culture) and three non-required ones: CT (optional), EEG (recommended) and the sorafenib medication review (recommended, last). The serial ammonia, the PRES MRI, the AFP prognosis panel and the literature step are gone. The paracentesis shows PMN 188 with a negative culture, the blood and urine cultures and the urinalysis are negative, CRP is 38, and lactate is normal. The musts are:
- treat the diarrhoea-driven hypokalaemia (to 4.0) and hypomagnesaemia with ECG monitoring;
- stop spironolactone and replace volume for the AKI;
- search for the fever source (chest radiograph, stool C. difficile), with empirical antibiotics if the fever persists without one;
- titrate lactulose to 2-3 soft stools a day without loading, and continue rifaximin;
- hold sorafenib, without loperamide, and decide on a reduced-dose restart with oncology;
- oncology restaging for the AFP rise from 1620 to 2840;
- stop the omeprazole.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Core vocabulary (plan CENTRAL 5): `chest_xray` in `order_body_imaging` and a `stool` specimen (C. difficile toxin/PCR) in `order_microbiology`. Both are needed for the source search here; until then they are a must.
- Optional (plan CENTRAL 5): AFP as an orderable `interpret_labs` term. The current AFP is reported inside the core lab panel.
- New citation keys per plan 1.1.
- `accepted[0]` changed under ruling 3 (C10 scores and grade III; plan CENTRAL 6). No ICD or synonym change.

## Open questions for Andrea (judgment calls you could not settle)

- Sorafenib: the plan's must said "resume at a reduced dose with oncology". With the recomputed Child-Pugh C (14) and a rising AFP, systemic therapy is generally not recommended (BCLC D: best supportive care). I wrote the must as "decide with oncology whether to resume it at a reduced dose", and I made the oncology must weigh further therapy against Child-Pugh C liver function. Confirm.
- MUST-LACT was adapted: the canonical loading (25 mL every 1-2 hours) is unsafe in a patient who already has 3-5 watery stools a day, so the must says to titrate without loading. Other workers may have used the verbatim text in diarrhoeal cases.
- Grade III replaces the II-III range under plan rule 1.2, which moves the HE points to 3. Child-Pugh is C either way (13 or 14).
- Transplant referral was not added: he has HCC beyond Milan, which is outside standard transplant criteria.

## Verification

Adversarial verifier, 23 Oct 2026. Read the log, the full diff and the final case.
- The four notes are confirmed fixed:
  - Nothing both recommends and forbids loperamide.
  - The fever has a source-search must, urinalysis and a required urine culture, and the red herring no longer withholds antibiotics.
  - The AFP rise is addressed by an oncology must; the prior value is dated history.
  - There is no serial ammonia, and the lactulose target is 2-3.
- Scores were recomputed: MELD 23, MELD-Na 25 (Na 133), and Child-Pugh C 14. Grade III fits E3, disorientation to time and place, and asterixis, per the plan's upper-bound rule.
- Paracentesis arithmetic checked (SAAG 2.3 - 0.6 = 1.7). The cultures are required (T 38.2). The stop rule lists exactly the four required ids. The drug-interaction check routes correctly for "sorafenib" and "omeprazole".
- Found and fixed: `metadata.difficulty_description` still said "Moderate HE" after the relabel to West Haven grade III. It now reads "West Haven grade III HE".
- Checked and agreed: no transplant must (HCC beyond Milan, Child-Pugh C 14); empirical antibiotics only if the fever persists without a source, as the plan rules (C15).
- `perfect_agent.py HEP-ENC-M08 -v` passes; `case_io.py check` reports no failure naming the case.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Central vocabulary wired (24 Oct 2026)

`chest_xray` (`order_body_imaging`) and `stool` (`order_microbiology`, C. difficile GDH antigen and toxin B PCR) are now core terms, so the fever-source must (note 391bf9ac) becomes two scored actions.
- New criteria after the urine culture, both recommended, `[EASL_HE_2022]`: `action-chest-xray` `{"study": "chest_xray"}` (expected "No consolidation or effusion") and `action-stool-c-difficile` `{"specimen": "stool"}` (expected "C. difficile GDH antigen negative and toxin B gene PCR not detected"; rationale: three weeks of watery diarrhoea with fever on omeprazole and lactulose).
- New `followup_outputs[2]` `request_chest_xray` (no consolidation or effusion, mildly elevated hemidiaphragms from ascites) and `[3]` `request_stool_c_difficile` (both assays negative), before the drug check.
- `assessment.required_recommendations[3]` now: "Fever without a source on the cultures, urinalysis, chest radiograph and stool C. difficile testing: re-examine for a source, and start empirical antibiotics if the fever persists without one."
- `differential[1].key_features`: "Chest and stool sources still to be checked" replaced by the negative results. `red_herrings[1].correct_interpretation` adds "(all negative here)".
- AFP (plan CENTRAL 5, optional): not made a criterion. HCC surveillance is not part of the HE work-up, the AFP sits in its own panel of the core labs as a result (no leak of the HE diagnosis), and the AFP rise is handled by the oncology must. No change.
- Re-run: `perfect_agent.py HEP-ENC-M08 -v` ok (both new criteria served by their follow-ups); `case_io.py check` schema OK, synonym guard OK, no test failure names the case.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

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
