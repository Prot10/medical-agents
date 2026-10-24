# BACT-MEN-S02
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| d0c1d5e4-e8b3-4dde-8e68-2ebb58f90bf7 | FIXED | Plan C1. Post-treatment `request_repeat_lp` deleted, so its wrong comparators (34 vs 35 cmH2O, 3200 vs 3474) go with it. Index CSF moved from `initial_tool_outputs.csf` (now null) to `followup_outputs[2]` (`analyze_csf`, trigger `request_lumbar_puncture`), after the CT; `-v` confirms action-3 receives it and the hard CT-before-CSF constraint is now satisfiable in pathway order. Post-treatment `request_repeat_labs_24h` deleted (ruling 4). |
| 792e734f-3498-4183-b30d-6fe44ae12566 | FIXED | Papilloedema removed: `patient.neurological_exam.cranial_nerves` now "Fundoscopy limited by photophobia and poor cooperation; no papilledema seen on the views obtained." The CT "no cerebral edema" beside an opening pressure of 35 cmH2O stays (not contradictory, plan 4 S02). The imaging-first decision no longer rests on papilloedema; see Open questions for why the CT stays required (A, focal sign) instead of the plan's B. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.sequence_constraints`, `action-4-order-ct-scan`, must, prohibition | IDSA 2004 imaging list ("altered mental status ... age >60"); once papilloedema goes, the remaining WHO 2025 criterion in the record is the focal motor sign in `neurological_exam.motor` ("Moves all four extremities spontaneously but less so on the right side"). | FIXED as decision A on the focal sign: HARD CT before CSF with the canonical WHO reason (NICE 1.4.7 agrees), SOFT blood cultures before CT, canonical A label, expected evidence, must and prohibition; CT stays required and in `stop_rule`. |
| C | major | `ground_truth.assessment.required_recommendations` | Template vancomycin plus ceftriaxone; no Listeria cover for a diabetic patient (plan 4.0 S02: yes, diabetes, Q7). | FIXED: canonical base regimen and ampicillin must "because of diabetes mellitus"; narrowing must (penicillin MIC 0.06 susceptible by CLSI meningitis breakpoints; stop ampicillin). |
| C | major | `ground_truth.assessment` | Dexamethasone template must and the "Do NOT discontinue dexamethasone ... Gram stain" prohibition (plan C5). | FIXED: prohibition deleted; canonical C5 must plus "Continue for 4 days: Streptococcus pneumoniae is identified." |
| C | major | `ground_truth.assessment.required_recommendations` | BP 90/54 after a 1 L bolus, HR 116, blood lactate 4.1 mmol/L: sepsis with hypotension and no resuscitation action anywhere. | FIXED: must for crystalloid, vasopressors to MAP 65 mmHg or more if hypotension persists, repeat lactate (Surviving Sepsis Campaign 2021). |
| C | minor | `ground_truth.assessment.required_recommendations` | No source control for the purulent maxillary and ethmoid sinusitis; the focal sign with a sinus source raises subdural empyema, which a non-contrast CT can miss. | FIXED: ENT drainage must; conditional must for contrast MRI if the asymmetry persists or she fails to improve; new differential entry. |
| A | major | `followup_outputs` (`request_pcr_panel`, `request_audiometry`), `initial_tool_outputs.literature_search`, literature criterion | PCR filed under `interpret_labs`, audiometry as `baep`, literature step expecting IDSA 2004/ESCMID/De Gans with an initial output echoing the expected evidence (plan C8, C9). | FIXED: all deleted; PCR result kept inside the index CSF report; hearing must added. |
| D | major | index CSF | Culture "S. pneumoniae isolated at 18 hours" at the index LP; latex antigen; lactate reference "<2.1" and ">4 strongly supports bacterial meningitis"; RBC 5 "traumatic"; ratio paired with serum glucose 218 while the panel says 213 (plan C7). | FIXED: culture "Pending"; latex removed; canonical lactate and RBC strings; ratio 0.05 recomputed from 11.4/213 with the WHO reference; interpretation reduced to values and pattern. |
| B | major | blood cultures | No culture interval; serotype 3 reported at once; aerobic bottles 1 and 2 plus an anaerobic bottle at 5 days; narrowing and interpretability boilerplate; em dashes in susceptibility keys (plan C6). | FIXED: two sets positive at 12 and 15 hours, identified at 24 hours, susceptibilities at 48 hours with CLSI meningitis interpretation; canonical impression. `collected_before_antimicrobials` true kept (no antibiotic before collection). |
| D | major | CT | Impression "demonstrates no contraindication to lumbar puncture" (plan C3); finding text began "density:". | FIXED: findings-only impression; finding description cleaned. |
| B | minor | `initial_tool_outputs.labs` | Male reference ranges for a woman (haemoglobin 13.5-17.5 made 13.0 "low"; haematocrit, creatinine); anion gap 22 (137 - 96 - 19), above what lactate 4.1 explains (plan C12); no HIV result. | FIXED: female ranges (Hb 12.0-15.5, now normal; Hct 36.0-46.0; creatinine 0.5-1.1); chloride 102 (anion gap 16); HIV 1/2 Ag/Ab non-reactive; abnormal summary and interpretation rebuilt. Liver tests were already present. |
| B | minor | `patient.history_present_illness` | "the worst headache of her life" undeclared (plan C11); arrival vitals 39.8 C, HR 118, BP 92/58 against `vitals` 39.5, 116, 90/54. | FIXED: "a severe, rapidly worsening diffuse headache"; HPI arrival values aligned to `vitals`. |
| B | minor | `patient.neurological_exam.sensory` | "Withdraws symmetrically to painful stimuli" against `motor` "Localizes to pain bilaterally" and GCS M5. | FIXED: "Responds to painful stimuli in all four extremities." |
| C | major | `ground_truth.differential` | Viral meningitis and HSV moderate after a pyogenic CSF with S. pneumoniae (plan C10). | FIXED: excluded entries low or very low with the excluding data; added subdural empyema or cerebritis (low). |
| B | minor | `ground_truth.red_herrings[0]` | Sinus thickening "on MRI" with no MRI (plan C11). | FIXED: points at the CT findings (`followup_outputs[1].output.findings`). |
| C | minor | `followup_outputs[3]` (drug check) | Checked only dexamethasone, with a vancomycin CNS-penetration line and an irrelevant rifampicin line (plan C9). | FIXED: checks ceftriaxone, ampicillin and dexamethasone against metformin, aspirin, lisinopril, renal function, hypotension and her latex allergy; criterion stays recommended with concrete expected evidence. |
| A | minor | citations, `key_clinical_evidence`, metadata | IDSA 2004 and free-text citations; C17 template lines and duplicate WHO line; stale `case_body_concerns` about the literature tool; "5 required tools; 1 red herrings". | FIXED: `[WHO_Meningitis_2025]`; C17 replacements; concern cleared; "4 required tools; 1 red herring". |

## Changes, in one paragraph a physician can read before re-reviewing
The pathway is now blood tests, blood cultures, non-contrast CT, the index LP (the post-treatment repeat LP and the 24-hour repeat labs are gone), then a drug check. Papilloedema is removed from the examination (10 hours of illness). The CT stays required before the LP because the examination records less movement of the right limbs than the left, a focal neurological sign under WHO 2025 Annex A.4 (NICE 1.4.7 agrees); blood cultures and antibiotics come before the CT. The CSF reports values and pattern with culture pending and S. pneumoniae on multiplex PCR; blood cultures grow S. pneumoniae at 12 and 15 hours, penicillin-susceptible by CLSI meningitis breakpoints. Musts: ceftriaxone with ampicillin (diabetes), dexamethasone for 4 days, sepsis resuscitation for BP 90/54 with lactate 4.1, ENT drainage of the sinus source, contrast MRI if the asymmetry persists or she fails to improve, droplet precautions and audiology. Lab reference ranges are now female, chloride was corrected so the anion gap is 16, and HIV (non-reactive) was added.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys `[NICE_NG240]` (used in the constraint) and `[WHO_Meningitis_2025]` for the criteria pack allow-list (plan 5.1). Surviving Sepsis Campaign 2021 is cited in must text only.

## Open questions for Andrea (judgment calls you could not settle)
- Plan 4.0 marks S02 as B (sinus CT recommended) after the papilloedema is removed. The examination, however, records "Moves all four extremities spontaneously but less so on the right side", a focal neurological sign, which WHO 2025 Annex A.4 and NICE 1.4.7 both list as an imaging-first trigger. I kept the CT required with the hard constraint (A on the focal sign) rather than delete a recorded sign to fit the plan. The alternative is to make the motor examination symmetric and apply B; the lead should decide which way S02 goes.
- The contrast MRI must is conditional (persisting asymmetry or no improvement) and has no criterion or stored MRI output; if the lead prefers an MRI criterion, an MRI report would have to be authored.

## Verification
Adversarial verification, 23 October 2026. Checked: both note ids present; repeat LP and 24-hour labs gone; papilloedema removed from the examination and from every ground-truth text; index CSF after the CT in the pathway, `-v` serves `request_lumbar_puncture` to action-3; HARD CT before CSF with the canonical WHO reason and SOFT blood cultures before CT. Confirmed in `git show HEAD` that "Moves all four extremities spontaneously but less so on the right side" is original data, not added, so the worker's decision A (focal sign) against the plan's B is grounded in the record; it stays an open question for the lead. Recomputed anion gap 16 (137 - 102 - 19), ratio 0.05 (11.4/213, the BMP glucose), female reference ranges. No IDSA 2004, "age >", ">0.6", "traumatic", narrowing or LP-safety text left.
Found and changed:
- `ground_truth.assessment.required_recommendations` (sepsis must): the labs show platelets 147, fibrinogen 179 mg/dL (low), INR 1.3 and D-dimer 4.0 in a hypotensive patient, and nothing in the case addressed it (class of note 46d5c362 in S04: a falling fibrinogen is the discriminating value). Added to the existing must: repeat platelets, fibrinogen, INR and D-dimer, naming a sepsis-associated coagulopathy that may progress to DIC. Not called overt DIC: the ISTH overt-DIC score is about 2.
Not changed (judgment, noted for the lead): ampicillin 2 g every 4 hours with creatinine 1.5 mg/dL (eGFR about 45 by CKD-EPI 2021). Full dosing in the first 24 hours of meningitis is usual and the drug step says to review it if renal function worsens.
Re-run: `perfect_agent.py BACT-MEN-S02 -v` ok; `case_io.py check` clean for the case.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (6 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients
- Must added: resuscitate the hypotension before the lumbar puncture (WHO 2025 A.1.1: no LP with haemodynamic compromise requiring stabilisation)

Re-run: `perfect_agent.py` ok; `case_io.py check` clean for the case; BACT-MEN case guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality 'MRI', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
