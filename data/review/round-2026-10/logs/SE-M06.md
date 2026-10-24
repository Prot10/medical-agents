# SE-M06
Reviewer status: R1 none, R2 approved (1 note) | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| b1f48e5f-741d-47db-9b1d-6de79c73e787 | FIXED | Criterion action-10 (blood cultures) is now `recommended`, its required arguments are `specimen: blood_culture` only (`before_antimicrobials` and the template `tests` removed), and label, rationale and expected evidence are case-specific: fever 38.4 C with leukocytosis, cultures drawn although he is on day 12 of TMP-SMX, "no growth to date" [Tunkel_2008]. `initial_tool_outputs.microbiology`: `collected_before_antimicrobials` false; impression "Two sets of blood cultures drawn on day 12 of oral trimethoprim-sulfamethoxazole: no growth to date. Prior antimicrobial exposure lowers the yield." (C3). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.labs.panels["Exclusion studies"]` | Template block reporting magnesium, lactate, ABG and the CSF tests cytology and autoimmune_panel in the serum labs (C1). | FIXED: deleted; magnesium 2.0 with a value, chloride and a hepatic panel added; cytology and the neuronal antibody panel are reported in the CSF only (plan). Lactate and ABG dropped (not indicated, SpO2 97%). |
| D | minor | `initial_tool_outputs.labs.panels.Toxicology[1]` | A "TMP-SMX serum creatinine interaction" note posing as a lab row (interpretation in a lab report). | FIXED: deleted; the fact lives in the drug check. |
| B | minor | CSF follow-up | RBC "(traumatic vs blood-brain barrier disruption)", "low-normal" and "elevated" interpretations in value fields; label promised enterovirus PCR, cytology and autoimmune panel that were missing; special tests keyed by free text. | FIXED: values only; special tests keyed by vocabulary terms (HSV_PCR, meningitis_panel incl. VZV and enterovirus, CMV_PCR, autoimmune_panel, NMDAR_antibodies, cytology); criterion requires HSV_PCR. Trigger renamed `request_lp_hsv_pcr`. |
| C | major | `followup_outputs` `request_continuous_eeg_monitoring`, `request_aed_optimization` | EEG "NCSE suppressed after lorazepam + levetiracetam" and post-treatment levels reported treatment effects (ruling 4, C4); the EEG trigger hijacked the cEEG order. | FIXED: both deleted; the `continuous_icu` order receives the initial EEG. |
| C | minor | criterion action-9 (serum autoimmune panel) | Optional duplicate of the CSF antibody panel, answered by the template exclusion row; expected text described a repeat draw after treatment. | FIXED: deleted (plan: delete if duplicate). The post-HSV NMDAR risk stays in the key evidence. |
| C | major | drug-check follow-up, criterion action-6 | Missed the decisive interaction (TMP-SMX inhibits CYP2C9 and raises phenytoin levels); "acyclovir + metformin" presented as an interaction. | FIXED: T-DDI content (TMP-SMX with phenytoin; fosphenytoin with atorvastatin; levetiracetam none, renal dosing; valproate; lacosamide PR; acyclovir with TMP-SMX nephrotoxicity and creatinine secretion; trimethoprim with lisinopril hyperkalemia; metformin hold if renal function falls). Recommended (C9). Labs before drug check soft kept (renal dosing). |
| C | major | literature follow-up, criterion action-7 | Literature required, in the stop rule, triggered by `request_infectious_disease_consultation`, unsourced journal finding (C8). | FIXED: optional, last; trigger `request_hsv_encephalitis_literature`; T-LIT content cited [Tunkel_2008], [ESETT_2019], [Brophy_2012]. |
| B | minor | `patient.neurological_exam.reflexes` | "Right Babinski equivocal" with a right temporal lesion and left arm drift: the plantar sign was on the wrong side. | FIXED: "Left Babinski equivocal" (see Open questions; the plan said C6 no change, which I kept for the gaze). |
| D | minor | `patient.neurological_exam.additional` | "consistent with ongoing temporal lobe ictal activity" (interpretation in the exam). | FIXED: automatisms described only. |
| D | minor | MRI follow-up | "cytotoxic edema", "true restricted diffusion", and a teaching paragraph on HSV versus autoimmune distribution in the impression. | FIXED: signal descriptions; impression keeps the imaging differential only. |
| B | minor | EEG initial | LPDs called "triphasic"; no video correlate. | FIXED: sharply contoured LPDs; video correlate of the automatisms; numbered ACNS impression. |
| C | major | `required_recommendations` | Lorazepam without maximum; acyclovir without renal adjustment or duration; levetiracetam without dose; "continuous EEG to monitor NCSE response". | FIXED: T-MUST-BZD; acyclovir 10 mg/kg every 8 hours renally adjusted, 14 to 21 days [Tunkel_2008]; fluids and creatinine monitoring with a TMP-SMX review; T-MUST-2L levetiracetam 60 mg/kg max 4500 mg, avoiding fosphenytoin because of TMP-SMX; T-MUST-cEEG. |
| C | minor | `prohibited_recommendations[2]` | "phenytoin in fever + dehydration without cardiac monitoring" was not the case's risk. | FIXED: "Do NOT stop acyclovir early once HSV-1 PCR is positive"; the phenytoin risk is in the must. |
| C | major | `ground_truth.differential` | Other viral, autoimmune and bacterial causes "moderate" after a positive HSV-1 PCR and negative cultures (C14). | FIXED: other viral very_low, autoimmune low (post-HSV NMDAR noted), bacterial very_low; TMP-SMX aseptic meningitis added (very_low); abscess and metabolic very_low. |
| A | minor | `red_herrings[0].field_path` | Pointed at the whole medication list. | FIXED: `medications[3]` (TMP-SMX). |
| A | minor | `fallback_tool_outputs.advanced_imaging`, `.specialized_test` | Prose modality "FDG-PET brain" and non-vocabulary "Neuropsychological screening battery" (C10). | FIXED: deleted; `fallback_tool_kinds` updated; Holter fallback reads rhythm only. |
| C | minor | avoided action polysomnography | DaTscan rationale (C11). | FIXED: T-PSG text. |
| E | minor | criteria labels/rationales, labs and EEG arguments, MRI citation | Rationales copied from labels; lactate, ABG, CRP, procalcitonin and AED_levels (no ASM at home) as required lab arguments; EEG without `eeg_type`; MRI cited Glauser (treatment); em dashes. | FIXED: T-LABS (no extras), T-CT, T-EEG, MRI [Brophy_2012; Tunkel_2008]; em dashes removed throughout. |
| B | minor | order; `stop_rule` | Not the diagnostic order; allowance 0; literature, drug check and cultures in the stop rule (C12). | FIXED: labs, blood cultures, CT, EEG, MRI, CSF, drug check, literature; stop rule = 5 required, allowance 1. |

## Changes, in one paragraph a physician can read before re-reviewing
A 66-year-old man with 2 weeks of memory loss and confusion, on day 12 of TMP-SMX for a UTI, has a seizure without return to baseline, oral and hand automatisms, fever 38.4 C, left arm drift and now a left (not right) equivocal Babinski. Labs show leukocytosis and raised CRP, ESR and procalcitonin with normal renal function; the template exclusion block is gone and cytology and antibodies appear only in the CSF. EEG: right temporal focal electrographic SE with LPDs. MRI: right mesial temporal, insular and cingulate change. CSF: lymphocytic, HSV-1 PCR positive, other PCRs and antibodies negative. Blood cultures are recommended, drawn on TMP-SMX, and negative. Post-treatment EEG and levels are gone. The drug check now names TMP-SMX raising phenytoin levels. Musts: lorazepam, acyclovir 14 to 21 days renally dosed, fluids, levetiracetam (not fosphenytoin), cEEG.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: allow-list `[ACNS_2021]` and `[Tunkel_2008]` for SE; this case cites them.

## Open questions for Andrea (judgment calls you could not settle)
- The plan says "C6 no change". I kept the right gaze preference (toward a destructive right temporal lesion or postictal, plausible), but changed the equivocal Babinski from right to left because it sat on the same side as the lesion while the arm drift is on the left. Revert if you read the case otherwise.
- Serum autoimmune panel criterion (action-9) deleted as a duplicate of the CSF antibody panel, as the plan allowed.

## Verification
`perfect_agent.py SE-M06 -v`: pass; labs, blood cultures and CT from initial outputs, EEG initial for `continuous_icu`, MRI, CSF (HSV_PCR) and drug check from follow-ups. `pytest -k "SE-M06 or red_herring"` (case guards incl. leak guard, red-herring paths): pass. `case_io.py check SE-M06`: schema and synonym guard OK; no failure names SE-M06.

## Verification (adversarial verifier, 24 Oct 2026)
Checked: note b1f48e5f: blood cultures criterion recommended, `specimen: blood_culture` only, case-specific label, rationale and evidence; the stored report says `collected_before_antimicrobials` false and drawn on day 12 of TMP-SMX, no growth to date. Exclusion block gone, cytology and antibodies only in the CSF; drug check names TMP-SMX raising phenytoin levels and the acyclovir nephrotoxicity overlap, consistent with the must that avoids fosphenytoin; literature optional and last; post-treatment EEG and levels deleted; duplicate serum panel deleted; differential updated after a positive HSV-1 PCR; labs before drug check soft and CT before CSF hard; stop rule equals the 5 required criteria. The Babinski move to the left (worker's open question) is correct: right temporal lesion with left arm drift; hyperreflexia and extensor plantar are contralateral to a hemispheric lesion (plan 1.2). The right gaze preference stays (toward a destructive right temporal lesion or postictal, plan says no change); this settles the worker's open question, nothing is left for Andrea.
Found and fixed:
- B minor `patient.neurological_exam.mental_status` and `prohibited_recommendations[1]`: "GCS 10 (E3V3M4)" while the same field says he follows simple one-step commands inconsistently (M6) and has no verbal output beyond mumbling (V2). FIXED: "GCS 11 (E3V2M6)" in the exam and "GCS 11" in the LP prohibition.
Checks re-run after my edits: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, `test_case_guards -k` pass.

## Close-out (24 Oct 2026)
Decisions in `plans/SE-decisions.md`.
- synonyms: the G41 category no longer grants the type codes G41.0, G41.2 and G41.8 (a type code is granted only by the case's own code, so an answer coded with the wrong SE type no longer scores by code); `apply_diagnosis_synonyms.py --prune --conditions status_epilepticus` removed G41.0 and G41.8 from `ground_truth.diagnosis.icd_codes`. Labels unchanged.
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, SE case guards pass, `apply_diagnosis_synonyms.py --check --conditions status_epilepticus` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
