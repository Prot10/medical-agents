# SE-S06
Reviewer status: R1 none, R2 approved (1 note) | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| fc4e7dc6-33ac-4f40-895d-807c185627f5 | FIXED | The CSF follow-up `request_lp_autoimmune` ("slightly xanthochromic" with 0 RBC) deleted: it had no criterion (orphan, plan C5), and the head CT shows diffuse edema with sulcal effacement, which argues against an LP in the emergency work-up. The CNS infection differential now says the LP is deferred because of the edema. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.labs.panels["Exclusion studies"]` | Template block with ammonia, magnesium, ABG, beta-hCG and urinalysis "within reference range" and no numbers (C1); beta-hCG in a man (C2). | FIXED: deleted; magnesium 2.1, ABG pH 7.13 / pCO2 44 / pO2 56 / HCO3 14, urinalysis with dipstick blood 3+ and 0-2 RBC/hpf (myoglobinuria), protein 1+; serum osmolality 258, urine osmolality 480, urine sodium 58 (inappropriate ADH effect of MDMA); CMP completed (chloride, bicarbonate, anion gap 23, BUN, calcium 8.2, albumin, AST 142, ALT 88); phosphate 5.2; ammonia and beta-hCG dropped and removed from the criterion. |
| D | minor | labs toxicology | "MDMA (amphetamine screen)" names the drug in an immunoassay result. | FIXED: "Urine amphetamines (immunoassay)" positive; cocaine, opiates, cannabinoids, benzodiazepines, tricyclics negative; blood alcohol undetectable. |
| B | minor | `patient.history_present_illness` | Hyponatremia 124 without the water intake that explains it. | FIXED: the friend reports hours of dancing and heavy water intake. |
| D | minor | EEG finding | Beta finding "consistent with sympathomimetic toxidrome" names the cause in a data field. | FIXED: "Excess diffuse beta activity"; impression in ACNS form with an artifact limitation. |
| C | major | `followup_outputs` `request_continuous_eeg_monitoring`, `request_aed_optimization` | Post-treatment EEG course and 6 h post-treatment labs (ruling 4, C4); the EEG trigger hijacked the cEEG order. | FIXED: both deleted. |
| C | major | criterion action-6 "Rhabdomyolysis and AKI management" under `interpret_labs` | Treatment posing as a lab, required and in the stop rule (C4). | FIXED: deleted; fluids titrated to urine output with sodium checks, potassium treatment and nephrology are a must. |
| C | major | drug-check follow-up `request_hyponatremia_hyperthermia_treatment` | A treatment plan under the drug tool (C9). | FIXED: T-DDI content: MDMA with buspirone (stop buspirone), other serotonergic agents (tramadol, meperidine, fentanyl, linezolid, methylene blue), cyproheptadine (oral or nasogastric, sedation), levetiracetam renal dosing, fosphenytoin less effective; succinylcholine (potassium 5.6, rhabdomyolysis) and antipsychotics contraindicated; antipyretics warning. Required (C9), trigger `request_serotonergic_interaction_check`. |
| C | major | literature criterion action-5; two literature outputs | Literature required and in the stop rule; rhabdomyolysis literature unsourced; serotonin-syndrome literature with an empty summary (ruling 5, C8). | FIXED: one optional criterion, last; one T-LIT output [Boyer_2005; Spasovski_2014]; rhabdomyolysis literature deleted. |
| C | minor | MRI follow-up and criterion | Placeholder impression "May show cerebral edema; not initial priority". | FIXED: real optional MRI report (diffuse mild swelling, faint cortical FLAIR signal, no restricted diffusion, enhancement or herniation); criterion optional [Brophy_2012]. |
| C | major | `assessment` | Lorazepam without dose or maximum; 3% saline 100 mL without repeat rule or target; "cooling blankets alone" prohibition wording; no second-line ASM; hyperkalemia untreated; no paralysis rule above 41.1 C. | FIXED: lorazepam 0.1 mg/kg (max 4 mg, repeat once) or IM midazolam [Glauser_2016]; 3% saline 150 mL over 20 min up to three, +5 in the first hour, no more than 10 in 24 h [Spasovski_2014]; active cooling with nondepolarizing paralysis and intubation above 41.1 C, stop serotonergic drugs, cyproheptadine 12 mg then 2 mg every 2 h [Boyer_2005]; levetiracetam 60 mg/kg (max 4500 mg) with renal maintenance [ESETT_2019]; fluids with sodium checks, ECG and potassium; ICU and cEEG [Brophy_2012]. Prohibitions: sodium over 10 mmol/L in 24 h, antipsychotics, succinylcholine, relying on antipyretics, further serotonergic drugs. |
| C | major | `ground_truth.differential` | Water intoxication/SIADH "very_high" and heat stroke "high" as alternatives although they are parts of the accepted diagnosis (C14); no CNS infection entry. | FIXED: hyponatremia alone low (Hunter criteria met), exertional heat stroke moderate (overlapping contributor), other sympathomimetic low, NMS very low, CNS infection low (LP deferred for edema), IGE very low. |
| A | minor | `red_herrings[].field_path` | Pointers to the whole labs block and the whole medication list. | FIXED: `initial_tool_outputs.labs.panels.Toxicology[0]` and `patient.clinical_history.medications[0]` (buspirone). |
| B | minor | `sequence_constraints[0]` | Labs before drug check `hard` (C13). | FIXED: deleted. |
| A | minor | `fallback_tool_outputs` | "CT chest" (prose modality) under advanced imaging and quantitative EEG under specialized test answer any order of their tool; ECG at 71 bpm with HR 146 and K 5.6; incidental-sinus MRI fallback (C10). | FIXED: advanced imaging, specialized test and MRI fallbacks deleted (MRI has its follow-up); ECG fallback sinus tachycardia 144 with peaked T waves; kinds updated. |
| C | minor | avoided action polysomnography | DaTscan rationale (C11). | FIXED: T-PSG. |
| E | minor | labels, rationales, EEG arguments | Rationales copied from labels; EEG without `eeg_type`. | FIXED: T-LABS (extra tox_screen), T-CT, T-EEG with `continuous_icu` and `video` alternatives [Brophy_2012; ACNS_2021]. |
| B | minor | order; `stop_rule` | Allowance 0; literature and the treatment criterion in the stop rule (C12). | FIXED: labs, CT, EEG, MRI, drug check, literature; stop rule = the 4 required criteria, allowance 1. |

## Changes, in one paragraph a physician can read before re-reviewing
A 24-year-old man on buspirone, 8 hours after MDMA with hours of dancing and heavy water intake, in convulsive SE with 40.2 C, mydriasis, clonus and rigidity. The labs now report each analyte once: sodium 124 with low serum osmolality and inappropriately concentrated urine, potassium 5.6, phosphate 5.2, creatinine 2.2, CK 8640 with dipstick blood and no red cells, lactate 11.4 with pH 7.13, a positive amphetamine immunoassay and other drugs negative. CT shows mild diffuse edema; the EEG shows generalized electrographic SE with excess beta. The orphan CSF result (xanthochromic with 0 RBC), the post-treatment EEG and labs, the rhabdomyolysis "lab" criterion and its literature are gone. The drug check is now an interaction list (buspirone, serotonergic analgesics, succinylcholine, antipsychotics). Musts: lorazepam, 3% saline boluses within 10 mmol/L in 24 h, active cooling with paralysis above 41.1 C, stop serotonergic drugs and cyproheptadine, levetiracetam with renal dosing, fluids with sodium checks and potassium treatment, ICU and cEEG.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: allow-list `[ACNS_2021]`, `[Spasovski_2014]` and `[Boyer_2005]` for SE; this case cites them.

## Open questions for Andrea (judgment calls you could not settle)
None. Decided: the 24-hour limit is 10 mmol/L (not 8) because he has no high-risk factor for osmotic demyelination (acute hyponatremia, normal potassium, no alcohol use disorder or malnutrition); the existing "8 mmol/L" prohibition was replaced by the canonical 10. CK 8640 kept although early, because MDMA hyperthermia with hours of exertion produces rhabdomyolysis before the seizure, unlike the cases where CK was lowered.

## Verification
`perfect_agent.py SE-S06 -v`: pass; labs, CT and `continuous_icu` EEG from the initial outputs, drug check from its follow-up. `test_case_guards -k SE-S06` and the red-herring path test: pass. `case_io.py check SE-S06`: schema and synonym guard OK; no failure names SE-S06.

## Verification (adversarial verifier, 24 Oct 2026)
The worker's own check section above was a self-check, so the case was verified in full. Checked: note fc4e7dc6 (orphan CSF follow-up gone; no xanthochromia text anywhere; LP deferral stated in the differential); no beta-hCG; the 10 mmol/L limit in musts, prohibition, literature and key evidence (no high-risk factor; acute hyponatremia); drug check is T-DDI content; anion gap 124 - 87 - 14 = 23 and pH 7.13 from HCO3 14 and pCO2 44. Found and fixed: (1) the new serum osmolality 258 mOsm/kg was below the calculated value (2 x 124 + 186/18 + 26/2.8 = 268), an impossible negative osmolal gap of about 10; set to 270 (still low) in the Osmolality panel, `abnormal_values_summary`, `interpretation`, the labs criterion's `expected_evidence` and `key_clinical_evidence[0]`. (2) The literature output's Hunter criteria sentence was garbled and incomplete (omitted tremor with hyperreflexia and made hyperthermia with hypertonia sufficient without clonus); rewritten as the four Hunter rules [Boyer_2005]. Both are errors in text the worker introduced, so the edit in this approved case is warranted. `perfect_agent.py SE-S06 -v`, the case guards and `case_io.py check SE-S06`: clean after the edit.

## Close-out (24 Oct 2026)
Decisions in `plans/SE-decisions.md`.
- synonyms: the G41 category no longer grants the type codes G41.0, G41.2 and G41.8 (a type code is granted only by the case's own code, so an answer coded with the wrong SE type no longer scores by code); `apply_diagnosis_synonyms.py --prune --conditions status_epilepticus` removed G41.2 and G41.8 from `ground_truth.diagnosis.icd_codes`. Labels unchanged.
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, SE case guards pass, `apply_diagnosis_synonyms.py --check --conditions status_epilepticus` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `continuous_icu`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## EEG and labs after routing (25 Oct 2026)

Commit 317e46db routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG) and serves an `interpret_labs` order only the stored panels it names. Decisions for the condition in `plans/SE-routing-decisions.md`.

- EEG: a routine order received the library's normal routine EEG, which contradicts the case. Added `fallback_tool_outputs.eeg` with `eeg_type` `routine` (the stored continuous_icu recording cut to a 30-minute portable recording without video, technologist notes for the clinical events, activation not performed): continuous generalized 2-4 Hz spike-and-wave during convulsions (electrographic SE), excess beta, heavy artifact. No criterion, tiers and the reward-relevant policy unchanged; the clinically correct test stays the continuous EEG of `action-1-analyze-eeg`. A `continuous_icu` or `video` order still receives `initial_tool_outputs.eeg`.
- Labs `action-2-interpret-labs`: unserved result cited in `expected_evidence`: CK 8640, lactate 11.4, uric acid (Other), serum osmolality 270 (Osmolality), phosphate 5.2 (Phosphate). EXTEND with CK: a must and the criterion's own rationale use CK 8640 for the rhabdomyolysis; the CK order also returns the lactate stored with it. TRIM serum osmolality and phosphate (incidental; the sodium and the served urine studies carry the hyponatremia). Scoring change: yes.
  - action-2-interpret-labs required_arguments.panels ['CBC', 'CMP', 'magnesium', 'tox_screen'] -> ['CBC', 'CMP', 'magnesium', 'tox_screen', 'CK']
  - action-2-interpret-labs label -> 'Emergency laboratory work-up: glucose, CBC, electrolytes, magnesium, renal and hepatic function, toxicology, CK'
  - action-2-interpret-labs expected_evidence: 'Sodium 124 with serum osmolality 270, urine osmolality 480 and urine sodium 58; potassium 5.6, phosphate 5.2, creatinine 2.2; CK 8640 with dipstick blood and no RBC; lactate 11.4 with pH 7.13; urine amphetamines positive, other drugs negative' -> 'Sodium 124 with urine osmolality 480 and urine sodium 58; potassium 5.6 and creatinine 2.2; CK 8640 with dipstick blood and no RBC; lactate 11.4 with pH 7.13; urine amphetamines positive, other drugs negative'
- Checks: `perfect_agent.py -v` pass; `case_io.py check` schema and synonym guard OK, no test failure names the case; probe: routine (omitted and explicit) order -> the new case fallback, `continuous_icu` and `video` -> the stored index recording; every number in each lab criterion's evidence is in what its order returns.

## Matcher fix (25 Oct 2026)

The lab matcher now keeps a urine or CSF row out of a blood order: a urinalysis, urine sodium or urine osmolality row answers only an order that names the urine assay, so a CBC or CMP order no longer returns the urine results. The lab criterion therefore names the urine assays its expected evidence cites.

- `ground_truth.action_criteria[action-2-interpret-labs]`: new first alternative `{panels: ['CBC', 'CMP', 'magnesium', 'tox_screen', 'CK', 'urinalysis', 'urine_osmolality', 'urine_sodium']}` (adds `urinalysis`, `urine_osmolality`, `urine_sodium`); the previous orders stay as alternatives, so every call that matched before still matches. The expected evidence reads urine osmolality 480, urine sodium 58 and dipstick blood without red cells, which the first order received only through two matcher defects fixed on 25 Oct 2026: a urine row answered a blood-count or metabolic order (`Urine WBC` as WBC, `Urine sodium` as sodium, a urine creatinine ratio as creatinine), and the unit `mg/dL` read as magnesium. Scoring: cost reference only (the policy's reference order is fuller); coverage unchanged.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-7-analyze-brain-mri` label: "MRI brain if encephalopathy persists after correction (optional)" -> "MRI brain if encephalopathy persists after correction"
