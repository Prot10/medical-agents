# HEP-ENC-P07
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 8a4256a7-b206-42d6-abc1-e35dca3ed4f9 | FIXED | Ammonia range set to the condition's 11-51 µmol/L (`initial_tool_outputs.labs.panels.LFTs[5]`); 48 is within range and no longer flagged; removed from `abnormal_values_summary`; the HPI sentence "48 µmol/L, at the upper limit of normal (lab ULN 45 µmol/L)" deleted; the 4-week follow-up with range 11-45 deleted. |
| d848bfa7-c3c4-47f4-8a89-5737561c8d21 | FIXED | EEG (`initial_tool_outputs.eeg`): posterior dominant rhythm 7.5 Hz, below the adult lower limit of 8 Hz (one normal limit stated, in background, finding and impression), with intermittent diffuse theta; impression "mild diffuse slowing consistent with a metabolic encephalopathy"; classification abnormal, now consistent with the findings. |
| 23004ad1-6ca4-4915-859d-e6026a30fe85 | FIXED | "Exclusion studies" block deleted, so TSH appears once (TSH panel, 1.8 mIU/L, replacing the template 2.1); magnesium 2.0, lactate 1.1, B12 410 and folate 9.8 now have values in their panels. |
| 41f02bb6-fdeb-45c7-b2ec-b0ce03dae593 | FIXED | The ammonia is described one way everywhere: 48 µmol/L within the 11-51 range. Panel unflagged; HPI statement deleted; red herring `red_herrings[1]` now reads "Ammonia 48 µmol/L (within the 11-51 reference range)" with the interpretation that a normal ammonia neither excludes nor confirms HE; the label's "ammonia borderline" became "ammonia within the reference range". |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness`, `neurological_exam.mental_status` | Timeline leaks: "psychometric testing reveals mild impairment", the ammonia, "CT head essentially normal", "EEG shows subtle slowing"; the exam reported Digit Symbol 28 and NCT-A 38 s, i.e. the PHES subtests the required criterion orders (C13). | FIXED: removed; the HPI keeps the clinical story. |
| B | major | `neurological_exam.mental_status` | "GCS 14 (E4V4M6)" with "Oriented to person, place, time" (V4 means confused). | FIXED: GCS 15 (E4V5M6). |
| B | minor | `initial_tool_outputs.labs.panels.Sleep` | CPAP download (use 3.2 h/night, T90 18%) reported as laboratory results by `interpret_labs`. | FIXED: moved to the HPI as last week's sleep-clinic download (pre-encounter device data, not a scored study); panel deleted. |
| C | major | `diagnosis.accepted[0]`, history | "Child-Pugh A, MELD 8" undated; computed Child-Pugh A (5), MELD 7, MELD-Na 7 (C10); "Covert/minimal"; "precipitated by CPAP non-compliance (nocturnal hypoxemia impairs ammonia metabolism) and long-term PPI use (gut dysbiosis)" states speculative mechanisms as fact. | FIXED: label "Covert hepatic encephalopathy (PHES -5) in well-compensated NASH cirrhosis (Child-Pugh A, MELD-Na 7), with untreated obstructive sleep apnea ... and long-term PPI use as contributors; ammonia within the reference range"; history score removed. |
| C | major | `followup_outputs` (CPAP "drug check", 4-week response panel, transplant MELD panel, literature output) and `action-3-search-medical-literature` | CPAP optimisation filed as a drug check; PHES and ammonia 4 weeks "after rifaximin + CPAP" (treatment response); a MELD-Na panel; literature output echoing the expected evidence (C1, C2, C4). | FIXED: deleted; literature criterion deleted, `initial_tool_outputs.literature_search` null. |
| B | minor | `followup_outputs` PHES | Findings rows without test names; test_type "PHES — covert HE evaluation"; norms given as "threshold 29 s for age-58". | FIXED: one row per subtest with its result, `test_type` `neuropsych_battery`, PHES -5 below the -4 cut-off; neuropsychometry may name the profile (minimal HE). Criterion stays required. |
| C | major | `action-4-check-drug-interactions`, PPI follow-up | Required with template expected evidence; PPI output claimed SIBO and urease mechanisms as fact and prescribed a 4-week reassessment (C5). | FIXED: optional (plan), alternatives omeprazole, metformin, lactulose; output `check_omeprazole_metformin_lactulose`: no interaction with lactulose, PPI association with HE and SBP, step-down options, metformin in compensated cirrhosis, no sedative hypnotics. |
| C | major | `action-8`, `action-9-order-microbiology` | Blood and urine cultures required "before the first antimicrobial dose" in an afebrile outpatient with a 6-week covert cognitive change, WBC 5.6, CRP 2.2. | FIXED: specimen-only arguments, both optional (the plan says recommended; see Open questions); blocks "no growth at 48 hours". |
| B | minor | `initial_tool_outputs.ct` | Empty findings; "restricted diffusion" on CT (C8). | FIXED: canonical normal CT. |
| B | minor | `initial_tool_outputs.labs` | Template zinc 82; no CRP; summary listed CPAP data and missed Hb, platelets and glucose. | FIXED: zinc 70, CRP 2.2; summary and interpretation list the flagged values only. |
| A | minor | `action-1-interpret-labs` | 11 named panels demanded. | FIXED: two-alternative core (C9). |
| C | major | `assessment` | Must "PHES testing" (a test); "Trial lactulose 30 mL TID" with a 4-6 week PHES retest; boilerplate haloperidol line; generic LP prohibition; vague cholinesterase line. | FIXED: musts: lactulose for covert HE affecting work, titrated to 2-3 soft stools, review at 4-8 weeks (ACG 2026 key concept 8; the canonical hourly loading of MUST-LACT is for overt episodes and was not used, see Open questions); CPAP adherence with sleep medicine; PPI deprescribing; driving counselling, documented. Prohibitions: PROHIB-BZD, sedating opioids (acetaminophen up to 2 g per day), dismissing complaints because ammonia is normal or class A, cholinesterase inhibitor for presumed Alzheimer disease; LP line deleted. |
| C | minor | `ground_truth.differential` | "Review home medications", "Screen with PHQ-9", "AD workup if PHES improves" written as plans, not assessment-time views (ruling 7). | FIXED: entries state what the case shows (CPAP data, no sedatives, no low mood, course and PHES). |
| E | minor | criteria, pearls, citations, metadata | Rationale = label; "(AASLD)" pearl; free-text citations; covert/overt definition missing (C11). | FIXED: rationales with keys; K_CLIN, K-AMM, score line, covert/overt pearl, covert HE prevalence pearl cited to EASL 2022; metadata updated. |

## Changes, in one paragraph a physician can read before re-reviewing

The policy now requires the core labs and the PHES, recommends the EEG, and leaves CT, cultures and the medication review optional. The ammonia is reported once, 48 µmol/L within the 11-51 range and unflagged, and every description of it agrees; TSH appears once. The EEG now reports a posterior rhythm of 7.5 Hz, below the 8 Hz adult limit, with diffuse theta. The HPI and exam no longer give the psychometric, ammonia, CT or EEG results, the GCS is 15 to match full orientation, and the CPAP download moved from the lab report to the history. The treatment-response panel, the CPAP "drug check", the MELD panel and the literature search are deleted; the PHES report lists each subtest. The label reads covert HE (PHES -5), Child-Pugh A, MELD-Na 7, with OSA and long-term PPI use as contributors. Musts: lactulose titrated to 2-3 soft stools with review at 4-8 weeks, CPAP adherence, PPI deprescribing, driving counselling. Prohibitions: sedatives, sedating opioids, dismissing the complaints, cholinesterase inhibitors.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`.
- `accepted[0]` changed under ruling 3 (C10 scores; "ammonia borderline" per notes 8a4256a7 and 41f02bb6); ICD codes unchanged.
- Synonyms: `accepted` carries the appended synonym "overt hepatic encephalopathy" in this covert-HE case (it comes from `diagnosis_synonyms.yaml` by ICD code). An agent answering "overt HE" would score here although the case is covert by definition (ACG 2026 key concept 1). Consider a per-case exclusion or a covert-specific synonym set.

## Open questions for Andrea (judgment calls you could not settle)

- Cultures: the plan tiers them recommended for P07. I made them optional: this is a 6-week covert cognitive change in an afebrile outpatient with normal WBC and CRP and no source; the infection screen of C7 belongs to overt episodes. If the condition should stay uniform, set both back to recommended.
- Lactulose must: I did not use MUST-LACT verbatim; its "25 mL every 1-2 hours until two soft bowel movements" loading is for an overt episode, not outpatient covert HE. The must keeps the 2-3 stools target and the warning on over-titration.
- Child-Pugh HE points: scored 1 (no clinically evident encephalopathy: oriented, no asterixis). The wife's account of sleep inversion and irritability could be read as West Haven grade 1; counting it would give Child-Pugh B (7). The plan computed A (5).

## Verification

Adversarial check, 23 Oct 2026. Read the log, the diff and the whole final case. Recomputed: Child-Pugh A 5, MELD 7, MELD-Na 7 (Na 140). All four notes are fixed everywhere: ammonia 48 within 11-51, unflagged, described identically in the panel, the interpretation, the red herring and the label, and absent from the HPI; one TSH (1.8); the EEG gives one normal limit (8 Hz) and a 7.5 Hz rhythm, consistent with the abnormal classification. The GCS now matches full orientation, and the PHES subtests no longer leak from the exam. Two deviations from the plan were checked and accepted as clinically better, both logged by the worker: cultures optional rather than recommended (an afebrile outpatient with a 6-week covert change, normal WBC and CRP, no source), and the PHES criterion ordered before the EEG (psychometric testing is the diagnostic test for covert HE; the EEG is supportive). The lactulose must keeps the 2-3 target without the overt-episode hourly loading, which is correct for outpatient covert HE. The covert-case synonym "overt hepatic encephalopathy" is correctly sent to CENTRAL. Found nothing to change. `perfect_agent.py` and `case_io.py check` clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
Covert HE: "overt hepatic encephalopathy" no longer granted (`except_cases`); "covert/minimal hepatic encephalopathy" scoped to this case.
- labels removed: "overt hepatic encephalopathy", "hepatic coma"
- labels added: "covert hepatic encephalopathy", "minimal hepatic encephalopathy"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-8-order-microbiology` rationale: "Optional: a 6-week covert cognitive change in an afebrile outpatient with a normal white cell count and CRP and no source; the infection screen belongs to overt episodes." -> "A 6-week covert cognitive change in an afebrile outpatient with a normal white cell count and CRP and no source; the infection screen belongs to overt episodes."
- criterion `action-9-order-microbiology` rationale: "Optional: a 6-week covert cognitive change in an afebrile outpatient with a normal white cell count and CRP and no source; the infection screen belongs to overt episodes." -> "A 6-week covert cognitive change in an afebrile outpatient with a normal white cell count and CRP and no source; the infection screen belongs to overt episodes."
- criterion `action-2-order-ct-scan` rationale: "Optional: no focal deficit, seizure or head trauma; a structural cause of a 6-week cognitive change is unlikely, but imaging is reasonable before attributing it to covert HE." -> "No focal deficit, seizure or head trauma; a structural cause of a 6-week cognitive change is unlikely, but imaging is reasonable before attributing it to covert HE."
