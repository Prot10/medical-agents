# SE-S04
Reviewer status: R1 none, R2 needs_changes (2 issue notes) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| efb6cbfc-69ba-442d-92c8-460dd15d8e14 | FIXED | The `request_aed_optimization` follow-up ("Valproate post-IV loading (20 mg/kg)" 82, post-treatment ammonia and glucose) deleted (ruling 4). The literature output rewritten per T-LIT: valproate-associated hyperammonemia is managed by withdrawing valproate and giving IV L-carnitine [Lheureux_2009] (the "do not stop valproate" sentence is gone). Prohibition "Do not reload or continue valproate" kept and cited; a matching must stops valproate and gives L-carnitine 100 mg/kg (max 6 g) then 15 mg/kg every 4 h; the second-line must avoids valproate. The drug check lists valproate with hyperammonemia as a contraindication. |
| f6c10984-e730-4cad-9723-22936efdabd2 | FIXED | `initial_tool_outputs.labs.panels["Exclusion studies"]` deleted (C1). ESR reported once with a value (64 mm/h, high), the SLE panel values stand (dsDNA 142, C3 48, C4 6), magnesium 1.9 and an arterial gas (pH 7.15, pCO2 50, pO2 60, HCO3 17) with values, beta-hCG <2 mIU/mL; "autoimmune_panel" and "autoimmune_encephalitis_panel" removed from the first-line labs; the serum neural antibody panel is a separate recommended follow-up (negative). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.clinical_history.medications` | Prednisone 40 mg daily (in the HPI and exam) missing from the medication list (plan C15). | FIXED: added (day 10); PMH lists the prednisone and the class III nephritis with baseline creatinine. |
| D | major | `initial_tool_outputs.drug_interactions.general`; fallback drug output | Initial drug output repeated the criterion's expected text (L-carnitine plan) and failed the leak guard; fallback had engineering text (C8, C9). | FIXED: deleted; T-DDI follow-up: aromatic ASMs contraindicated by carbamazepine SJS, valproate contraindicated by hyperammonemia, phenytoin and prednisone, levetiracetam (renal dosing), lacosamide, valproate and carbapenems; hydroxychloroquine seizure-threshold and QT warning, valproate teratogenicity, steroid hyperglycemia. Required (C9). |
| C | major | `followup_outputs` `request_continuous_eeg_monitoring` | Post-treatment EEG course (ruling 4, C4); hijacked the cEEG order. | FIXED: deleted. |
| C | major | CSF criterion action-6 and output | Fever since the day before the seizure (38.2 C, now 38.6 C) on prednisone 40 mg: the plan rates CSF recommended, but the plan's own rule (CSF without delay with fever or immunosuppression) makes it a must-exclude; the CSF was keyed on `autoimmune_panel`; the output was "xanthochromic tinge" with 2 RBC (same class as SE-S06 note fc4e7dc6) and held a "not routinely measured" anti-dsDNA line. | FIXED: CSF required, `special_tests` HSV_PCR (alternative meningitis_panel), cited [Tunkel_2008; Brophy_2012]; output clear and colorless, lymphocytic differential, Gram stain, culture, HSV PCR and multiplex meningitis PCR negative, NMDAR negative, oligoclonal bands negative; CT before CSF hard kept. |
| C | major | microbiology | No blood cultures in a febrile immunosuppressed patient (plan C3). | FIXED: recommended `action-10-order-microbiology` (`blood_culture`), drawn before antimicrobials, no growth to date. CRP 9, procalcitonin 0.08 and a urinalysis without pyuria added so the fever's source can be judged. |
| C | major | criterion action-9 | Serum antibody panel `required` and answered by the deleted exclusion block (C4). | FIXED: recommended, served by its own negative serum panel follow-up [Graus_2016]. |
| C | minor | labs `CK` | CK 2640 at about 30 minutes of seizure: implausibly early. | FIXED: CK 410 U/L. |
| B | minor | labs CMP | Bicarbonate, chloride, BUN, albumin and liver tests absent with lactate 8.8; ammonia filed under "AED_Levels". | FIXED: CMP completed (bicarbonate 17, anion gap 19, albumin 3.2); ammonia in its own panel; INR 1.0 added (LP safety); urinalysis with proteinuria and hematuria (nephritis). |
| D | minor | CT `additional_observations`, finding text; MRI finding type | "SLE related chronic changes", "SLE vasculitis", "SLE-related white matter disease" (clinical diagnosis named by imaging). | FIXED: nonspecific white matter change; MRI adds pertinent negatives (no enhancement, no PRES pattern). |
| C | major | `assessment` | Lorazepam without maximum; levetiracetam without dose; "Check beta-hCG" as a must (a test, in the labs); no L-carnitine dose; "Rheumatology consult" only. | FIXED: T-MUST-BZD (no prehospital benzodiazepine was given); T-MUST-2L levetiracetam 60 mg/kg (max 4500 mg), avoiding valproate and fosphenytoin; stop valproate and L-carnitine [Lheureux_2009]; T-MUST-cEEG; refractory escalation; continue prednisone with rheumatology and renal dosing. Prohibitions merged: valproate, aromatic ASMs, cyclophosphamide or pulse steroids without evidence of NPSLE, delaying seizure control. |
| C | major | `ground_truth.differential` | CNS lupus and SLE autoimmune encephalitis "moderate" after MRI, CSF and panel (C14); PRES and transient post-convulsive hyperammonemia not considered. | FIXED: lupus and autoimmune encephalitis low with the results; PRES low (MRI); post-convulsive hyperammonemia low; infection low with CSF and culture results. |
| C | major | literature criteria and outputs | Literature required and in the stop rule; second literature output (SLE) with unsourced claims, empty summary (ruling 5). | FIXED: one optional criterion, last, out of the stop rule; SLE literature deleted. |
| B | minor | `sequence_constraints[1]` | Labs before drug check `hard` "beta-hCG and ammonia". | FIXED: `soft`, reason the ammonia, valproate level and creatinine decide the drug (plan C13's own criterion). |
| A | minor | `red_herrings[0].field_path`; fallbacks | Pointer to the whole labs block; "MRI brain" advanced imaging and quantitative EEG under specialized test answer any order of their tool; ECG rate 59 with HR 136 (C10). | FIXED: `panels.SLE markers[0]`; fallbacks deleted; ECG fallback sinus tachycardia 128 with incomplete RBBB; kinds updated. |
| C | minor | avoided action polysomnography | DaTscan rationale (C11). | FIXED: T-PSG. |
| E | minor | labels, rationales, EEG | Rationales copied from labels; EEG without `eeg_type`; impression wording. | FIXED: T-LABS (extras AED_levels, ammonia, beta-hCG), T-CT, T-EEG, MRI [Brophy_2012; Fugate_2015]; EEG impression in ACNS form with artifact limitation. |
| B | minor | order; `stop_rule` | Allowance 0; literature in the stop rule (C12). | FIXED: labs, blood cultures, CT, EEG, MRI, CSF, antibody panel, drug check, literature; stop rule = the 6 required criteria, allowance 1. |

## Changes, in one paragraph a physician can read before re-reviewing
A 45-year-old woman with generalized epilepsy on valproate, SLE with class III nephritis on hydroxychloroquine and prednisone 40 mg (now on the medication list), carbamazepine SJS, in convulsive SE with no prehospital benzodiazepine and a fever that began the day before. Labs report each analyte once: valproate 36 with ammonia 84, creatinine 1.4, post-convulsive lactic acidosis, active lupus serology with proteinuria, raised ESR, normal procalcitonin, negative beta-hCG. Because she is febrile on steroids, CSF is now required (mild nonspecific lymphocytic pleocytosis, all infection tests negative) and blood cultures recommended (no growth). MRI shows nonspecific white matter change and peri-ictal thalamic signal, no PRES, infarct or cerebritis; serum and CSF antibodies are negative. The post-loading valproate level, post-treatment EEG and the second literature output are gone. Musts: lorazepam, levetiracetam 60 mg/kg avoiding valproate and the aromatic ASMs, stop valproate with L-carnitine, cEEG, refractory escalation, continue prednisone with rheumatology. The SLE flare is a red herring for the cause of SE.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: allow-list `[ACNS_2021]`, `[Lheureux_2009]`, `[Tunkel_2008]`, `[Graus_2016]`, `[Fugate_2015]` for SE; this case cites them.

## Open questions for Andrea (judgment calls you could not settle)
None. Decided, against the plan's tier: CSF is required, not recommended, because the fever began before the seizure in a patient on prednisone 40 mg, which is the plan's own indication for CSF "without delay"; the result rules infection out. The labs-before-drug-check constraint is kept as `soft` although S04 is not in the plan's C13 list, because the ammonia and valproate level decide the drug, which is the C13 criterion itself.

## Verification
`perfect_agent.py SE-S04 -v`: pass; labs, CT and `continuous_icu` EEG from the initial outputs; blood cultures, MRI, CSF, antibody panel and drug check from their follow-ups. `test_case_guards -k SE-S04` and the red-herring path test: pass. `case_io.py check SE-S04`: schema and synonym guard OK; no failure names SE-S04 (an alternative-served check on the meningitis_panel alternative was fixed by reporting the multiplex PCR).

## Verification (adversarial verifier, 24 Oct 2026)
The worker's own check section above was empty, so the case was verified in full. Checked both notes: no post-loading valproate panel anywhere, literature says withdraw valproate with L-carnitine [Lheureux_2009] (dose 100 mg/kg, max 6 g, then 15 mg/kg every 4 h, correct), the valproate prohibition, the stop-valproate must and the drug-check contraindication agree; no Exclusion block, ESR, dsDNA, C3, C4 each once with values and flags. Prednisone is on the medication list and in the PMH consistently with the HPI (40 mg, started 10 days ago). Arithmetic: anion gap 137 - 101 - 17 = 19; pH 7.15 from HCO3 17 and pCO2 50; CSF glucose ratio 116/214 = 0.54. The worker's CSF upgrade to required (fever before the seizure on prednisone) is sound and CT before CSF is hard. Found and fixed: the fever (38.2 C the day before, 38.6 C now) was left without an explanation once every infection test was negative, and the CSF pleocytosis was not addressed in the infection entry; `ground_truth.differential` "CNS infection in an immunosuppressed patient" `key_features` now also names the multiplex PCR, attributes the fever to the active SLE flare (ESR 64 with CRP only 9) and calls the mild lymphocytic pleocytosis nonspecific after prolonged convulsions in active SLE. `perfect_agent.py SE-S04 -v`, the case guards and `case_io.py check SE-S04`: clean after the edit.

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
