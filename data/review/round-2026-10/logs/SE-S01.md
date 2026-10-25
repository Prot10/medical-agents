# SE-S01
Reviewer status: R1 none, R2 approved (1 issue, 1 note) | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 35db0801-2557-4c9e-8ec5-18728e2ff75b | FIXED | MRI follow-up (`request_mri_brain_contrast`) rewritten as a normal study (no hippocampal or cortical FLAIR or DWI change, no enhancement, symmetric hippocampi), so it agrees with the expected text; criterion action-4 made `optional` (known JME with an explained trigger and a normal CT), label, rationale and `expected_evidence` "Normal MRI: no structural lesion, restricted diffusion or abnormal enhancement" (plan C15). |
| 138b30a5-840a-4ab0-a7a4-5e85454eef99 | FIXED | beta-hCG removed from the core-labs `required_arguments` and label, from the labs report (the template "Exclusion studies" block that held it is deleted), and the male-patient pregnancy-test sequence constraint is deleted (plan C2). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.labs.panels["Exclusion studies"]` | Template block with ammonia, ABG and tox screen "within reference range" without numbers, contradicting lactate 8.4 (an acidotic gas is expected) (C1). | FIXED: deleted. Each analyte reported once with value and range: ammonia 44 umol/L, ABG pH 7.17 / pCO2 48 / pO2 68 / HCO3 17 (Henderson-Hasselbalch consistent; mixed acidemia with SpO2 92%), urine drug screen cannabinoids positive (matches his cannabis use). The CMP was a BMP without liver tests: chloride, bicarbonate 17, anion gap 20, BUN, albumin, AST, ALT, alkaline phosphatase and bilirubin added (normal liver tests matter before reloading valproate). Magnesium in its own panel. |
| C | minor | labs `CK` | CK 2840 U/L "rhabdomyolysis" on the arrival sample, about 30 to 40 minutes into the convulsion: CK rises over hours, so this level is implausible at that time and drove an "aggressive hydration for rhabdomyolysis" must. | FIXED: CK 468 U/L (mildly raised); must turned into IV fluids with CK and creatinine rechecked over 24 to 48 hours. |
| C | major | `patient.vitals.temp` 38.4 C, WBC 16.8; differential "CNS infection" | Differential said "No fever"; the 38.4 C temperature had no explanation in the case. | FIXED: T-HYPERTHERMIA red herring added (field `patient.vitals.temp`); CRP 4 mg/L and procalcitonin 0.06 ng/mL added to the labs; HPI states no recent illness, fever or headache; CNS infection entry rewritten; prohibition of antibiotics or LP for this temperature alone. |
| B | minor | `patient.neurological_exam.reflexes` | "Hyperreflexia during postictal phase" while he arrives still convulsing (no postictal phase yet). | FIXED: "Not reliably assessable during continuous convulsive activity; plantar responses extensor bilaterally". |
| C | major | `followup_outputs` `request_continuous_eeg_monitoring`, `request_aed_optimization` | Post-treatment EEG and "valproate post-IV loading 78 / magnesium post-replacement" labs reported management the agent had not recommended (ruling 4, C4); the EEG trigger also hijacked the cEEG order. | FIXED: both deleted; a `continuous_icu` order receives the initial EEG. |
| C | major | criterion action-7 (magnesium, CK) | Duplicate lab criterion whose expected text was treatment ("IV magnesium repletion; aggressive IV fluids"), answered by the initial labs (C4). | FIXED: deleted; magnesium is in T-LABS, the treatment is a must. |
| C | major | criterion action-9, `initial_tool_outputs.microbiology` | Template urine culture "before the first antimicrobial dose" with a "urinary source" expected text in an afebrile-before-the-seizure man with no urinary symptoms (C3). | FIXED: criterion and output deleted. |
| C | minor | CSF follow-up `request_lp_autoimmune` | Orphan autoimmune CSF result with no criterion (C5). | FIXED: deleted; an LP order gets the library normal report. |
| D | major | `initial_tool_outputs.drug_interactions.general`, fallback drug and literature outputs | Initial drug-check "summary" repeated the criterion's expected text (leak guard failure); fallback drug output had engineering text "(agent not specified on this case's pathway)" (C8, C9). | FIXED: deleted; drug check served by a T-DDI follow-up (ethanol plus benzodiazepine respiratory depression, valproate with lorazepam and phenytoin, levetiracetam and lacosamide, drug-disease warning for sodium-channel blockers in IGE, valproate liver and ammonia warning). Recommended (C9). |
| C | major | literature criterion action-6 and two literature follow-ups | Literature `required` and in the stop rule; trigger `request_sah_guidelines`; unsourced management content (rhabdomyolysis fluid rates, "JME: valproate preferred") (ruling 5). | FIXED: one optional criterion, last, out of the stop rule; one T-LIT output cited to [ILAE_2015_SE], [Glauser_2016], [ESETT_2019], [Brophy_2012]; the rhabdomyolysis literature deleted. |
| C | major | `assessment.required_recommendations` | "Lorazepam 0.1 mg/kg first-line" without maximum although diazepam had already failed; "valproate 30-40 mg/kg + levetiracetam, both first-line per ESETT" misstates ESETT (one second-line drug, not both, and not first-line). | FIXED: one further benzodiazepine dose (lorazepam 0.1 mg/kg max 4 mg) with immediate second-line loading [Glauser_2016]; T-MUST-2L valproate 40 mg/kg (max 3000 mg) or levetiracetam 60 mg/kg (max 4500 mg), avoid fosphenytoin in JME [ESETT_2019]; T-MUST-cEEG; airway and respiratory monitoring on alcohol with refractory-SE escalation [Brophy_2012]; magnesium, fluids, CK and creatinine; adherence, alcohol and sleep. |
| E | minor | `assessment.prohibited_recommendations` | Three duplicate phenytoin or carbamazepine prohibitions; "Do NOT discharge without addressing non-adherence" (a must, not a prohibition). | FIXED: one merged prohibition; bicarbonate prohibition (from the key evidence); antibiotics or LP for seizure-related hyperthermia prohibited; adherence moved to a must. |
| C | major | `ground_truth.differential[0]` | Alcohol withdrawal "moderate" with a blood alcohol of 0.18 g/dL (still intoxicated) (C14). | FIXED: low, key features name the BAL; other entries cite the results that exclude them. |
| A | minor | `red_herrings[].field_path` | Pointed at the whole labs block. | FIXED: `panels.Toxicology[0]`, `panels.Other[0]`, `patient.vitals.temp`. |
| B | minor | `sequence_constraints[0]` | Labs before drug check justified by a pregnancy test in a man (C13). | FIXED: deleted; no constraint remains (no CSF criterion). |
| E | minor | criteria labels and rationales; EEG arguments | Rationales copied from labels; EEG without `eeg_type`; MRI cited Glauser (treatment). | FIXED: T-LABS (extras AED_levels, ammonia on valproate, tox_screen for alcohol and drug use; lactate, ABG and CK reported but not required), T-CT, T-EEG (`continuous_icu` with `video` alternative), MRI [Brophy_2012]. |
| E | minor | EEG `impression`, `findings` | Not in ACNS report form; frequency 2-4 Hz straddling the Salzburg 2.5 Hz threshold; no mention of the recording conditions during convulsions. | FIXED: ABNORMAL numbered impression (continuous generalized 2.5-4 Hz spike-and-wave and polyspike-and-wave, evolving, time-locked to the convulsions); myogenic artifact limitation. |
| A | minor | `fallback_tool_outputs.advanced_imaging`, `.specialized_test`, `.ecg` | Prose modality "MRI brain"; a neuropsychological-testing report served for any specialized test; normal ECG at rate 79 in a man with HR 132 (C10). | FIXED: advanced imaging and specialized test fallbacks deleted (library answers); ECG fallback sinus tachycardia 124; `fallback_tool_kinds` updated. |
| C | minor | avoided action polysomnography | DaTscan rationale (C11). | FIXED: T-PSG text. |
| B | minor | order; `stop_rule` | Not the diagnostic order; allowance 0 (C12). | FIXED: labs, CT, EEG, MRI, drug check, literature; follow-ups MRI, drug check, literature; stop rule = the 3 required criteria, allowance 1. |

## Changes, in one paragraph a physician can read before re-reviewing
The presentation is unchanged (32-year-old man with JME, convulsing for over 20 minutes after prehospital diazepam 10 mg), except that the HPI now states he was well that morning with no illness or fever and the reflex exam no longer describes a postictal phase he has not reached. The labs report every analyte once with values: valproate 28, blood alcohol 0.18 and urine cannabinoids, magnesium 1.4, post-convulsive lactic acidosis (lactate 8.4, bicarbonate 17, anion gap 20, pH 7.17), WBC 16.8, glucose 196, an early CK of 468 (was 2840, implausible at that time), normal liver tests, ammonia, CRP and procalcitonin; beta-hCG is gone. The 38.4 C temperature is a seizure-related hyperthermia red herring. The MRI is now normal and optional. Post-treatment EEG and labs, the template urine culture, the orphan CSF result and the duplicate lab criterion are removed. Required: labs, CT, continuous EEG; drug check recommended; literature optional. Musts: one more benzodiazepine dose with immediate second-line loading (valproate 40 mg/kg or levetiracetam 60 mg/kg, avoiding fosphenytoin in JME), cEEG, airway monitoring on alcohol with refractory escalation, magnesium and CK follow-up, adherence and triggers.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: allow-list `[ACNS_2021]` for SE; this case cites it.

## Open questions for Andrea (judgment calls you could not settle)
None. Decided: the first must allows one repeat benzodiazepine dose because only a single prehospital dose was given (AES 2016 permits one repeat), together with immediate second-line loading, rather than skipping to the second line only; the drug-disease warning on sodium-channel blockers in JME is stated in the drug check and prohibitions without a citation key, since no allow-listed source covers it.

## Verification
`perfect_agent.py SE-S01 -v`: pass; labs and CT from the initial outputs, `continuous_icu` EEG from the initial EEG, drug check from its follow-up. `test_case_guards -k SE-S01` and the red-herring path test: pass. `case_io.py check SE-S01`: schema and synonym guard OK; no failure names SE-S01.

## Verification (adversarial verifier, 24 Oct 2026)
The worker's own check section above was a self-check, so the case was verified in full. Checked: both notes against the file (MRI follow-up normal and the criterion optional with matching expected text; no beta-hCG in labels, arguments, outputs or constraints); every own finding against the final JSON; lab arithmetic (anion gap 136 - 99 - 17 = 20; Henderson-Hasselbalch pH 7.17 from HCO3 17 and pCO2 48); red-herring pointers (Toxicology[0] = blood alcohol, Other[0] = lactate); musts against prohibitions (fosphenytoin avoided in both, valproate reload consistent with normal liver tests and ammonia); differential against the results; no leftover template text (Exclusion block, post-treatment follow-ups, unbracketed citations, DaTscan text). Prose changes in this approved case are limited to the HPI fever clause and the reflex line, both justified. Found nothing to change. Not changed but noted: `metadata.revision_reason` still describes the deleted "reported as exclusions" block (metadata is not shown to the agent or reviewers; left for the central metadata refresh). `perfect_agent.py SE-S01 -v`, the case guards and `case_io.py check SE-S01`: clean.

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

- EEG: a routine order received the library's normal routine EEG, which contradicts the case. Added `fallback_tool_outputs.eeg` with `eeg_type` `routine` (the stored continuous_icu recording cut to a 30-minute portable recording without video, technologist notes for the clinical events, activation not performed): continuous generalized spike-and-wave evolving to polyspike-and-wave during convulsions (electroclinical SE), artifact-obscured. No criterion, tiers and the reward-relevant policy unchanged; the clinically correct test stays the continuous EEG of `action-1-analyze-eeg`. A `continuous_icu` or `video` order still receives `initial_tool_outputs.eeg`.
- Labs `action-2-interpret-labs`: unserved result cited in `expected_evidence`: lactate 8.4, CK 468 (Other), CRP and procalcitonin (Inflammatory markers). MOVE lactate into the served Arterial blood gas panel (blood gas analysers report it; the library ABG lists it), because a prohibition cites it; TRIM CK 468 (the must only rechecks CK) and CRP and procalcitonin (incidental; the no-antibiotics must stands on the absent source). Scoring change: no.
  - action-2-interpret-labs expected_evidence: 'Valproate 28 mcg/mL (subtherapeutic); blood alcohol 0.18 g/dL and urine cannabinoids positive; magnesium 1.4 mg/dL low; lactate 8.4 mmol/L with bicarbonate 17, anion gap 20 and pH 7.17 after the convulsion; WBC 16.8 and glucose 196; CK 468; ammonia 44, liver tests, creatinine, sodium, CRP and procalcitonin normal' -> 'Valproate 28 mcg/mL (subtherapeutic); blood alcohol 0.18 g/dL and urine cannabinoids positive; magnesium 1.4 mg/dL low; lactate 8.4 mmol/L with bicarbonate 17, anion gap 20 and pH 7.17 after the convulsion; WBC 16.8 and glucose 196; ammonia 44, liver tests, creatinine and sodium normal'
  - initial_tool_outputs.labs: Lactate 8.4 moved from panel 'Other' to 'Arterial blood gas'
- Checks: `perfect_agent.py -v` pass; `case_io.py check` schema and synonym guard OK, no test failure names the case; probe: routine (omitted and explicit) order -> the new case fallback, `continuous_icu` and `video` -> the stored index recording; every number in each lab criterion's evidence is in what its order returns.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although this case contradicts it (diagnosis, history, medications or a stored finding) now get a case-specific report; every other off-pathway order still gets the library normal. No tier, criterion, diagnosis or existing output changed.

- `analyze_eeg eeg_type=ambulatory` -> `followup_outputs[order_ambulatory]`: ambulatory EEG mirroring the stored continuous EEG (no video).
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[order_performance_status]`: performance status KPS 20, ECOG 4 during the admission.
- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `followup_outputs[order_gait_and_balance_timed]`: timed gait not testable, as on the examination.
- `perform_clinical_assessment assessment_type=cognitive_screen` -> `followup_outputs[order_cognitive_screen]`: baseline cognitive screen not testable in the documented mental state.
- `order_specialized_test test_type=neuropsych_battery` -> `followup_outputs[order_neuropsych_battery]`: neuropsychological battery not testable in the documented mental state.
- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: speech and language evaluation not testable in the documented mental state.
- `labs:lithium_level` -> fallback labs panel `Lithium`: lithium not detected (not prescribed).

Checks: `perfect_agent.py` ok; `test_case_guards.py -k SE` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
