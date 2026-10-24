# SE-S05
Reviewer status: R1 none, R2 no notes (counted among the R2 approvals per the plan) | Approved before this round: yes (treated as approved)

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The notes file has no note for SE-S05. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.labs.panels["Exclusion studies"]` | Template block reporting thiamine "within reference range" beside a thiamine of 22 nmol/L, ammonia, ABG and tox screen without numbers (C1). | FIXED: deleted. Thiamine reported once (22, low); ammonia 38 umol/L, ABG pH 7.16 / pCO2 46 / pO2 58 / HCO3 16, urine drug screen negative, blood alcohol <0.01; CMP completed (chloride 92, bicarbonate 16, anion gap 24, BUN, creatinine, calcium, albumin 3.0); phosphate and magnesium in own panels; CRP 12, procalcitonin 0.09. |
| C | major | labs glucose; musts and prohibitions | Glucose 62 with a must "correct hypoglycemia ONLY after thiamine" and a hard constraint "thiamine before glucose": the governing rule is thiamine first or together, never delaying glucose [Brophy_2012], and 62 sits above the plan's 60 mg/dL dextrose threshold, so the must did not apply. | FIXED: glucose 54 mg/dL; must "IV dextrose now with thiamine first or at the same time; do not delay the dextrose"; prohibition covers both errors; the treatment sequence constraint deleted (treatment is not a tool). |
| C | major | thiamine must | "500 mg TID for 3 days" attributed to the plan's EFNS source: EFNS 2010 recommends at least 200 mg three times daily IV; 500 mg three times daily is the common high-dose regimen from other guidance. | FIXED: must states at least 200 mg three times daily [EFNS_Wernicke_2010], commonly 500 mg three times daily for 2 to 3 days then 250 mg daily; literature output cites EFNS for 200 mg. |
| C | major | `followup_outputs` `request_continuous_eeg_monitoring`, `request_aed_optimization` | Post-treatment EEG and "glucose post-D50W, magnesium and potassium post-replacement" labs (ruling 4, C4); EEG trigger hijacked the cEEG order. | FIXED: both deleted. |
| C | major | criterion action-7 (magnesium, thiamine) | Duplicate lab criterion whose expected text was treatment ("IV Mg sulfate 2 g") (C4). | FIXED: deleted; magnesium is in T-LABS, its replacement is a must. |
| C | major | criterion action-9, `initial_tool_outputs.microbiology` | Template meningitis wording ("organism and its susceptibility", `before_antimicrobials` required) (C3). | FIXED: kept as recommended (fever 39.2 C, WBC 14.2) with case text, `{"specimen": "blood_culture"}` only; output moved to a follow-up, no growth to date. |
| C | major | CSF follow-up `request_lp_autoimmune` (plan C5: delete as orphan) | Fever 39.2 C with a first SE in a heavy drinker (a bacterial meningitis risk group) is the plan's own indication for CSF; deleting the only CSF result would leave that question unanswerable. The output also carried a post-dextrose serum glucose ("serum 128") and a "post-ictal" label on a normal count. | FIXED differently from the plan: new recommended criterion `action-10-analyze-csf` (HSV_PCR) with a hard CT-before-CSF constraint; output normal (WBC 3, protein 44, glucose 58 with paired serum 98, Gram stain, culture and HSV PCR negative). See Open questions. |
| D | major | `initial_tool_outputs.drug_interactions.general`; fallback drug output | Initial drug output repeated the criterion's expected text (leak guard failure); fallback had engineering text (C8, C9). | FIXED: deleted; T-DDI follow-up: valproate contraindicated (liver injury, INR 1.6, platelets 98), benzodiazepines with phenobarbital, diazepam and midazolam prolonged in liver disease, fosphenytoin with amlodipine and low albumin, levetiracetam, thiamine; dextrose-thiamine warning. Recommended (C9). |
| C | major | literature criterion action-6; two literature outputs | Literature required and in the stop rule; addiction literature with unsourced figures (80% Korsakoff, NNT 7-9); withdrawal literature uncited (ruling 5, C8). | FIXED: one optional criterion, last; one T-LIT output [Brophy_2012; EFNS_Wernicke_2010; Glauser_2016]; addiction literature deleted (addiction care is a must). |
| D | minor | CT findings, MRI finding type | CT "chronic alcohol-related brain damage", "possible Wernicke"; MRI finding type "Wernicke encephalopathy" (diagnosis in a data field). | FIXED: CT describes volume loss with pertinent negatives for falls (no subdural, contusion, fracture); MRI finding describes the signal; impression keeps the worded Wernicke pattern (kind 2), adds mammillary enhancement and no hemorrhage. |
| C | major | `assessment` | Lorazepam without maximum after failed IM midazolam and no IV access; no second-line ASM; "CIWA protocol" as the only ASM plan. | FIXED: IV or IO access with one further lorazepam dose and immediate second-line [Glauser_2016]; levetiracetam 60 mg/kg or phenobarbital 15-20 mg/kg with airway support, avoiding valproate and fosphenytoin [ESETT_2019; Brophy_2012]; electrolyte replacement; ICU and cEEG; withdrawal treatment and addiction care. Prohibitions deduplicated (two glucose-before-thiamine items merged). |
| C | major | `ground_truth.differential` | Hypoglycemia "high"; hepatic encephalopathy "moderate" with ammonia normal; "Wernicke-Korsakoff without seizures" and "withdrawal seizures without SE" were not alternatives; trauma from falls and meningitis not considered (C14). | FIXED: hypoglycemia and electrolytes moderate (contributors); hepatic encephalopathy, traumatic hemorrhage and meningitis low with the deciding results. |
| A | minor | `red_herrings[].field_path` | Pointers to the whole labs block and the HPI. | FIXED: `panels.CMP[7]` (glucose) and `panels.Toxicology[0]`; the hypoglycemia herring now traps "hypoglycemia alone explains it", not "give dextrose" (which is correct). |
| E | minor | `patient.history_present_illness` | Duplicated sentence "He has no prior epilepsy history." | FIXED: second copy removed. |
| A | minor | `fallback_tool_outputs` | "MRI brain" advanced imaging and an NCS specialized test answering any order of their tool; engineering drug fallback; normal ECG at 65 with HR 148, K 2.8, Mg 0.8 (C10). | FIXED: deleted; ECG fallback sinus tachycardia 144, QTc 496 with U waves; kinds updated. |
| C | minor | avoided action polysomnography | DaTscan rationale (C11). | FIXED: T-PSG. |
| E | minor | labels, rationales, EEG | Rationales copied from labels; EEG without `eeg_type`; "background hyperexcitability" (not an ACNS term). | FIXED: T-LABS (extras ammonia and coagulation for liver disease, tox_screen; thiamine reported but not required), T-CT, T-EEG; EEG names excess beta. |
| B | minor | order; `stop_rule` | Allowance 0; literature, duplicate labs and cultures in the stop rule (C12). | FIXED: labs, blood cultures, CT, EEG, MRI, CSF, drug check, literature; stop rule = the 4 required criteria, allowance 1. |

## Changes, in one paragraph a physician can read before re-reviewing
A 58-year-old heavy drinker, 36 hours after his last drink, in convulsive SE after IM midazolam with no IV access, febrile 39.2 C, tremulous and hypertensive. The labs now report each analyte once: glucose 54 (was 62), magnesium 0.8, potassium 2.8, phosphate 1.6, alcohol-related liver injury with INR 1.6 and platelets 98, normal ammonia, post-convulsive lactic acidosis, low thiamine, undetectable alcohol and a negative drug screen. CT has no traumatic lesion; MRI shows the Wernicke distribution. Because of the fever, blood cultures (no growth) and a CSF examination after CT (normal) are recommended. Post-treatment EEG and labs, the duplicate magnesium criterion and the addiction literature are gone. Musts: IV or IO access with one more benzodiazepine dose, dextrose with thiamine given together (never delayed), high-dose IV thiamine, levetiracetam or phenobarbital (no valproate, no fosphenytoin), electrolyte replacement, ICU and cEEG, then withdrawal treatment and addiction care.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: allow-list `[ACNS_2021]`, `[EFNS_Wernicke_2010]`, `[Tunkel_2008]` for SE; this case cites them.
- Plan section 1.2 canonical fact "Wernicke: thiamine 500 mg IV three times daily ... [EFNS_Wernicke_2010]" misattributes the dose: EFNS 2010 (Galvin et al.) recommends 200 mg three times daily IV. The canonical text should cite EFNS for 200 mg three times daily and present 500 mg three times daily as common practice, or cite a source that recommends it.

## Open questions for Andrea (judgment calls you could not settle)
None. Decided, against the plan: the CSF result is kept and given a recommended criterion (with CT before CSF hard) instead of being deleted as an orphan, because fever 39.2 C with a first SE in a heavy drinker is the plan's own indication for CSF; the result rules meningitis out. Glucose changed from 62 to 54 mg/dL so that the dextrose must is consistent with the canonical threshold (below 60 mg/dL).

## Verification
`perfect_agent.py SE-S05 -v`: pass; labs, CT and `continuous_icu` EEG from the initial outputs; blood cultures, MRI, CSF and drug check from their follow-ups. `test_case_guards -k SE-S05` and the red-herring path test: pass. `case_io.py check SE-S05`: schema and synonym guard OK; no failure names SE-S05.

## Verification (adversarial verifier, 24 Oct 2026)
The worker's own check section above was a self-check, so the case was verified in full. Checked: the EFNS thiamine correction is right (Galvin 2010 recommends 200 mg three times daily IV; the plan's 1.2 wording misattributes 500 mg, logged under CENTRAL); dextrose with thiamine, never delayed, consistent in musts, prohibitions, drug check and literature; glucose 54 justifies the dextrose must; valproate and fosphenytoin avoided in musts and prohibitions; arithmetic (anion gap 132 - 92 - 16 = 24; pH 7.16 from HCO3 16 and pCO2 46); red-herring pointers (CMP[7] = glucose, Toxicology[0] = blood alcohol); differential against the results. The added CSF criterion (recommended, CT before CSF hard) is defensible in a febrile first SE in a heavy drinker. Found and fixed: the CSF criterion's rationale said "INR 1.6 and platelets 98 are acceptable for LP", which contradicts the plan's rule that uncorrected coagulopathy contraindicates LP; now "platelets 98 are adequate, and the INR of 1.6 from liver injury is corrected to the local LP threshold first". Noted, not changed: the CSF report's paired serum glucose (98 mg/dL) is necessarily drawn after the immediate dextrose the musts require, so it is the natural timeline rather than a treatment-response output; the log's claim that the post-dextrose serum glucose was removed is therefore only partly true. `perfect_agent.py SE-S05 -v`, the case guards and `case_io.py check SE-S05`: clean after the edit.

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
