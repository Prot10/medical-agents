# SE-S03
Reviewer status: R1 none, R2 needs_changes (2 issue, 2 note) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 54e2cb28-c7c9-4689-9691-01eb5d96bb24 | FIXED | `initial_tool_outputs.labs.panels["Exclusion studies"]` deleted (C1). Urinalysis appears once, abnormal (leukocyte esterase and nitrite positive, WBC >50/hpf, many bacteria; "Gram-negative rods" moved to the urine culture's Gram stain). Magnesium 1.9 and an arterial gas (pH 7.22, pCO2 38, pO2 62, HCO3 15) reported with values; ammonia dropped (no liver disease, no valproate) and removed from the criterion. |
| 5ff3c70f-1fdf-4429-a3ab-d42da89c191e | FIXED | One correction limit throughout: 8 mmol/L in the first 24 hours, because hypokalemia (K 3.4) makes her high risk [Verbalis_2013]. Musts, prohibition and the literature output (rewritten per T-LIT: 3% saline boluses, 10 then 8 mmol/L per 24 h in general, 8 in high-risk patients) agree; the drug-check output no longer states a correction rate at all (T-DDI: interactions only), so it cannot contradict. Plan C15: sodium 129 changed to 121 (129 is not severe and rarely causes SE), with serum osmolality 262, urine osmolality 420, urine sodium 22, BUN 34; `diagnosis.accepted[0]` "(Na 129)" to "(Na 121)" (CENTRAL). |
| 59001cc7-8a23-4b60-a60b-d4b00245492f | FIXED | Urine culture criterion (action-8, required) now `{"specimen": "urine"}` without `before_antimicrobials`; output moved from the initial block to a follow-up: E. coli >10^5 CFU/mL resistant to TMP-SMX and ampicillin, susceptible to ceftriaxone, `collected_before_antimicrobials` false, "collected on day 4 of oral TMP-SMX"; expected text names the organism as the precipitating source. Blood cultures added as a recommended criterion (`action-9-order-microbiology-blood`, `blood_culture`, no growth to date, drawn on TMP-SMX) (plan C3). |
| 0bc30365-55ba-4b61-b412-c7fda6cef28a | FIXED | Lesion side kept (imaging is the anchor). EEG rewritten: continuous 2.5-3.5 Hz discharges right hemisphere predominant with evolution and bilateral spread, over right hemisphere slowing; "contralateral activation pattern" deleted from the criterion. Ictal gaze in the exam changed from rightward to leftward (away from the right-hemisphere focus) (plan C6). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.clinical_history.medications` | TMP-SMX (day 4) in the HPI but not in the medication list. | FIXED: added (160/800 mg twice daily, day 4). |
| C | major | `followup_outputs` `request_aed_optimization`, `request_continuous_eeg_monitoring` | "Sodium 4 h post-hypertonic saline", "levetiracetam post-loading", post-hydration creatinine and a post-treatment EEG reported management not yet recommended (ruling 4, C4); the EEG trigger hijacked the cEEG order. | FIXED: both deleted. |
| C | major | criterion action-7 "Empiric UTI antibiotics" under `interpret_labs` | Treatment disguised as a lab (ruling 4, C4). | FIXED: deleted; antibiotic change is a must (stop TMP-SMX, IV ceftriaxone after cultures). |
| C | minor | CSF follow-up `request_lp_autoimmune` | Orphan CSF result with no criterion (C5). | FIXED: deleted. |
| C | minor | labs `CK` | CK 1640 "rhabdo" at 25 minutes of seizure: implausibly early. | FIXED: CK 286 U/L; "rhabdomyolysis" removed from must and expected text. |
| B | minor | labs CMP | Chloride, bicarbonate and BUN absent; lactate 7.8 with no acid-base data. | FIXED: chloride 86, bicarbonate 15, anion gap 20, BUN 34, calcium, albumin, liver tests; ABG consistent with HCO3 15. CRP 96 and procalcitonin 1.8 added (consistent with urosepsis). |
| C | major | `assessment` | Lorazepam without maximum although 2 mg (below dose) had failed; "Load IV levetiracetam" without dose; 3% saline 100 mL without repeat rule; "IV fluids for rhabdomyolysis"; expected and literature text "followed by fluid restriction", wrong in hypovolemic hyponatremia. | FIXED: full-dose lorazepam with immediate second-line [Glauser_2016]; 3% saline 150 mL, up to three, target +5 in the first hour [Spasovski_2014]; 8 mmol/L limit with potassium replacement and overcorrection watch [Verbalis_2013]; T-MUST-2L levetiracetam 60 mg/kg (max 4500 mg), avoid fosphenytoin (sulfamethoxazole, amlodipine) and carbamazepine or oxcarbazepine [ESETT_2019]; stop TMP-SMX, ceftriaxone; hold metformin and renal dosing; T-MUST-cEEG. Prohibition of fluid restriction added. |
| C | major | drug-check follow-up | A treatment plan for hyponatremia (rates, boluses) under the drug tool; no ASM interactions (C9). | FIXED: T-DDI content (TMP and metformin, TMP natriuresis and creatinine, sulfamethoxazole and phenytoin, fosphenytoin and amlodipine, levetiracetam, ceftriaxone; carbamazepine, oxcarbazepine and eslicarbazepine contraindicated in hyponatremia). Recommended (C9). |
| C | major | literature criterion action-6 | Required and in the stop rule (ruling 5); empty summary; "UTI causing SIADH-type effect" unsourced. | FIXED: optional, last, out of the stop rule; T-LIT [Spasovski_2014; Verbalis_2013]. |
| C | major | `ground_truth.differential` | Recurrent stroke and sepsis-alone "moderate" after CT and labs; "Levetiracetam level pending" although the level is reported (C14). | FIXED: low or very low with the deciding result. |
| B | minor | `red_herrings[0]` | "Suggests sepsis requiring sepsis bundle" while urosepsis is real and does need treatment; pointer to the whole labs block. | FIXED: the herring is now the fever pointing to CNS infection and an LP, resolved by the proven urinary source; `field_path` `patient.vitals.temp`. |
| B | minor | `patient.neurological_exam.motor` | "Todd's paresis expected". | FIXED: "pre-existing residual left arm weakness". |
| D | minor | CT `additional_observations` | "Old right MCA stroke - known epileptogenic substrate" (clinical interpretation in a CT report). | FIXED: removed; finding describes the encephalomalacia with ex vacuo change. |
| B | minor | `sequence_constraints[0]` | Labs before drug check, not listed for S03 in plan C13. | FIXED: deleted. |
| A | minor | `fallback_tool_outputs` | CT perfusion (prose modality) and transcranial Doppler under specialized test answer any order of their tool; ECG at 78 bpm with HR 128 (C10). | FIXED: deleted; ECG fallback sinus tachycardia 124 with nonspecific T flattening (K 3.4); kinds updated. |
| C | minor | avoided action polysomnography | DaTscan rationale (C11). | FIXED: T-PSG. |
| E | minor | labels, rationales, EEG arguments, MRI | Rationales copied from labels; EEG without `eeg_type`; MRI recommended although plan rates it optional; MRI cited Glauser. | FIXED: T-LABS (extra AED_levels), T-CT, T-EEG, MRI optional [Brophy_2012]. |
| B | minor | order; `stop_rule` | Allowance 0; literature, drug check and the fake antibiotic criterion in the stop rule (C12). | FIXED: labs, urine culture, blood cultures, CT, EEG, MRI, drug check, literature; stop rule = the 4 required criteria, allowance 1. |

## Changes, in one paragraph a physician can read before re-reviewing
A 72-year-old woman with post-stroke epilepsy (right MCA infarct) on levetiracetam, in convulsive SE after an underdosed prehospital lorazepam 2 mg, with 4 days of a UTI treated with oral TMP-SMX (now on the medication list). Sodium is now 121 (was 129) with serum osmolality 262, urine osmolality 420 and urine sodium 22: hypovolemic hyponatremia, with trimethoprim as a contributor; potassium 3.4. The urine grows E. coli resistant to TMP-SMX (collected on day 4 of it); blood cultures are recommended and show no growth to date. The EEG is right hemisphere predominant with bilateral spread, and the ictal gaze is leftward, matching the lesion. Post-treatment labs and EEG, the orphan CSF and the antibiotic-as-lab criterion are gone; literature is optional. Musts: full-dose lorazepam, 3% saline boluses with an 8 mmol/L in 24 h limit (hypokalemia = high risk), potassium replacement and overcorrection watch, levetiracetam 60 mg/kg, stop TMP-SMX and give ceftriaxone, hold metformin, cEEG; prohibitions include fluid restriction and carbamazepine or oxcarbazepine.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 3a: `ground_truth.diagnosis.accepted[0]` changed "(Na 129)" to "(Na 121)"; refresh the synonym entry if it keys on the label.
- Plan CENTRAL 1: allow-list `[ACNS_2021]`, `[Spasovski_2014]`, `[Verbalis_2013]` for SE; this case cites them.

## Open questions for Andrea (judgment calls you could not settle)
None. Decided, and differing from the plan's wording: the plan says "she is 72 with dehydration, not high-risk by default", but her potassium is 3.4, and hypokalemia is a listed risk factor for osmotic demyelination [Verbalis_2013], so the 8 mmol/L in 24 h limit applies; this also matches the musts the reviewer saw. Urinalysis is reported in the core labs but is not a required argument (the plan's T-LABS extras list excludes it); the urinary source is scored through the required urine culture.

## Verification
`perfect_agent.py SE-S03 -v`: pass; labs, CT and `continuous_icu` EEG from the initial outputs; urine and blood cultures from their follow-ups by specimen; drug check from its follow-up. `test_case_guards -k SE-S03` and the red-herring path test: pass. `case_io.py check SE-S03`: schema and synonym guard OK; no failure names SE-S03.

## Verification (adversarial verifier, 24 Oct 2026)
The worker's own check section above was a self-check, so the case was verified in full. Checked all four notes: urinalysis reported once and abnormal (no Exclusion block); one 8 mmol/L in 24 h limit in musts, prohibition and literature, justified by K 3.4 (hypokalemia is a listed osmotic-demyelination risk factor; the plan's own 1.2 list includes it), and the drug check states no rate; urine culture without `before_antimicrobials`, `collected_before_antimicrobials` false, E. coli resistant to TMP-SMX as the precipitating source; EEG right-hemisphere predominant, gaze leftward, invented term gone. Arithmetic: anion gap 121 - 86 - 15 = 20; pH 7.22 from HCO3 15 and pCO2 38; calculated osmolality 2 x 121 + 192/18 + 34/2.8 = 265 against measured 262 (plausible). Found and fixed: `initial_tool_outputs.labs.abnormal_values_summary` listed "Urine osmolality 420" and "Urine sodium 22" while both rows are `is_abnormal` false; removed from the abnormal summary (they remain in the panel, the interpretation and the expected text). The pre-existing em dash in the CT impression was left (old text). `perfect_agent.py SE-S03 -v`, the case guards and `case_io.py check SE-S03`: clean after the edit.

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
