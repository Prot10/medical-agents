# BACT-MEN-P01
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| ece53ab1-9242-4a2c-8a40-bdc635ad3b02 | FIXED | Repeat LP (`request_repeat_lp`) and repeat labs (`request_repeat_labs`) follow-ups deleted: an improving, treated patient has no indication, and the two contradicted each other. The index CSF report (now `followup_outputs[1]`, `request_lumbar_puncture`) carries the culture of the index specimen: "Streptococcus pneumoniae isolated at 36 hours" with penicillin and ceftriaxone MICs; Gram stain stays negative. |
| ec9ec4dd-2739-4e0d-9ac1-048810797b5f | FIXED | `initial_tool_outputs.drug_interactions` set to null. New follow-up `followup_outputs[2]` (`check_drug_interactions_meningitis_regimen`) checks the real regimen (ceftriaxone, conditional vancomycin, dexamethasone) against cetirizine, albuterol and ibuprofen (ibuprofen with dexamethasone: GI bleeding, stop it, use paracetamol) and the contrast reaction; its text does not restate the criterion. `action-5-check-drug-interactions` expected evidence names the concrete issue; tier stays recommended. |
| 9cd4cb49-c9e4-40a0-8674-1384032c1ba2 | FIXED | CSF moved out of the initial work-up (C1); the HARD CT-before-CSF constraint is deleted (`sequence_constraints` now empty) because the CT criterion is removed (C2 C). |
| af3519cd-e7f4-437e-bd5e-8b6f6357463c | FIXED | Reviewer's first option taken: `action-4-order-ct-scan` deleted, CT follow-up deleted, removed from `stop_rule.required_before_assessment`; avoided action `avoid-waste-6-order-ct-scan` added (waste); must "Proceed to lumbar puncture without prior cranial imaging ..." and prohibition "Do not delay lumbar puncture or antibiotics to obtain a CT head ..." replace the IDSA 2004 must and prohibition; key evidence line replaced. GCS 15 (E4 V5 M6) written into `neurological_exam.mental_status` so the must's statement is supported by the record. |
| dfe98540-6f4b-4c7d-9fff-5bf9ab41437d | FIXED | `glucose_ratio` = "0.51 (CSF 52.5 mg/dL / blood 102 mg/dL; reference 0.5 to 0.8, 0.4 or less abnormally low)"; "low-normal" and "borderline" removed; the lab panel glucose changed 94 -> 102 mg/dL (flagged H against 70-100) so one paired value is used. The repeat-LP part of the note lapses with the deletion of that study. |
| 1b2bea2e-4c9b-4f32-894a-759a979a2842 | FIXED | Chloride 107 -> 95 mEq/L (flagged L); anion gap 130 - (95 + 21) = 14; summary and interpretation updated. |
| eb13717f-b30a-46cd-9312-01e09a92d84a | FIXED | CSF lactate "3.8 mmol/L (local laboratory reference <3.5 mmol/L)"; interpretive text ("suggestive of bacterial etiology but overlap zone") removed. |
| 5cef0a0c-9a53-4990-b225-15663de01074 | FIXED | The quoted interpretation is `red_herrings[0].correct_interpretation` (the note anchors on `prohibited_recommendations[3]`): replaced with the reviewer's text verbatim; the negative antigen kept and named in the red herring. `prohibited_recommendations` entry now reads "a negative Gram stain or a negative antigen test" (no "normal CT", since no CT is done). Key evidence gains the antigen line (WHO 2025 Box 3.1 does not recommend antigen tests; positive result needs confirmation). |
| 065288ba-3ffc-4a92-8fea-a8ab8d6b6e8a | FIXED | `social_history.occupation` = "High school mathematics teacher"; the stale occupation flag in `metadata.case_body_concerns` removed. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A/B | major | `followup_outputs` (`request_pcr_panel`) | CSF multiplex PCR filed under `interpret_labs`, so the index CSF answering the `meningitis_panel` order had no panel result (plan C8) | FIXED: PCR result moved into the index CSF report; `request_pcr_panel` deleted; "HSV_PCR: Pending" removed (HSV is on the panel) |
| A | major | `followup_outputs` (`request_audiometry`) | audiometry filed as `baep` (plan C8) | FIXED: deleted; hearing must added (NICE NG240) |
| C | major | `required_recommendations` | template vancomycin plus ceftriaxone must; dexamethasone without stop rule; "de-escalate" without a target | FIXED: canonical base must (no Listeria risk factor at 35, healthy), canonical dexamethasone must with "Continue for 4 days: Streptococcus pneumoniae is identified", ceftriaxone 14 days, ibuprofen stopped during dexamethasone |
| C | minor | `prohibited_recommendations` | template "Do NOT discontinue dexamethasone solely because the Gram stain is negative" (plan C5) | FIXED: deleted |
| B | major | `followup_outputs` (literature), `action-6-search-medical-literature` | literature criterion expecting IDSA 2004, ESCMID 2016 | FIXED: deleted (ruling 5, plan C9) |
| B | minor | `ground_truth.red_herrings[2]` | "sinus mucosal thickening on MRI": there is no MRI, and the CT that held the finding is no longer part of the pathway | FIXED: red herring deleted |
| B | minor | `red_herrings[1].correct_interpretation` | prescribed fluid restriction for the hyponatraemia (a management claim not needed for the red herring) | FIXED: monitored and corrected alongside treatment; does not explain the syndrome |
| B | minor | blood culture follow-up | MICs as findings rows with no interpretation; anaerobic bottles "no growth at 5 days" reported at the assessment | FIXED: MICs in `susceptibility` with CLSI meningitis interpretations; anaerobic bottles "no growth at 48 hours"; impression "2 of 2 sets at 42 and 44 hours; final report at 5 days" |
| B | minor | index CSF `opening_pressure`, RBC | 24 cmH2O called "upper limit of normal" while the interpretation says raised; RBC "(normal)" | FIXED: "mildly elevated; normal 6-20 cmH2O"; RBC "within normal limits" |
| D | minor | index CSF `interpretation` | ended in a pattern statement | FIXED: values and stain/PCR/culture only, "Clinical correlation recommended" |
| B | minor | `initial_tool_outputs.labs` | HIV and liver tests ordered but absent | FIXED: HIV non-reactive, ALT, AST, ALP, bilirubin, albumin (normal) |
| C | minor | `ground_truth.differential` | viral meningitis and HSV moderate after S. pneumoniae on PCR and culture; cryptococcal meningitis irrelevant in a healthy host; meningococcal disease (droplet must, daycare contact) absent | FIXED: updated likelihoods with excluding results; cryptococcal removed, meningococcal meningitis added (low) |
| B | minor | `key_clinical_evidence` | IDSA 2004 template lines (CT age >60, vancomycin, Gram stain 60-90%, ratio <0.4, De Gans), WHO cultures line | FIXED: C17 replacements; new line on early bacterial meningitis with a modest CSF |
| B | minor | `avoided_actions` | `[IDSA_2004]` citations; PET rationale referring to CT and MRI | FIXED |
| B | minor | `metadata.difficulty_rationale` | "5 required tools; 3 red herrings" | FIXED: 3 required tools, 2 red herrings |

## Changes, in one paragraph a physician can read before re-reviewing
Only labs are given upfront (paired glucose now 102, chloride 95 for an anion gap of 14, HIV and liver tests added). No CT: he is alert with GCS 15 and has no WHO 2025 Annex A.4 or NICE 1.4.7 criterion, so CT is now a waste action and the musts say to go straight to lumbar puncture without delaying antibiotics. The pathway is blood cultures (S. pneumoniae in 2 of 2 sets at 42 and 44 hours, penicillin MIC 0.06 susceptible), the index LP (WBC 82 mixed, protein 88.4, ratio 0.51, lactate 3.8 against a local reference of <3.5, Gram stain and antigen negative, S. pneumoniae on multiplex PCR and in culture at 36 hours), and a recommended drug check that finds the ibuprofen-dexamethasone bleeding risk. The repeat LP, repeat labs, separate PCR step, audiometry and literature steps are gone. Musts: ceftriaxone within 60 minutes (vancomycin only for local resistance), dexamethasone for 4 days, ceftriaxone for 14 days, stop ibuprofen, droplet precautions, hearing assessment. The occupation is a mathematics teacher throughout, and the differential is updated to the results.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- None specific to this case beyond the condition-wide items in the plan (citation key `[NICE_NG240]` used in text).

## Open questions for Andrea (judgment calls you could not settle)
- The sinus mucosal thickening red herring lived only in the CT report; with CT now waste (plan C2 C, Q2) the CT follow-up is deleted and the red herring with it. If you would rather keep the CT as stored data for agents that order it anyway, the CT report (with the "no contraindication to lumbar puncture" sentence removed) and the red herring could be restored without changing any criterion.
- Paired glucose: the plan chose 102 mg/dL (ratio 0.51), which flags the lab glucose as high against the fasting range 70-100. The alternative (94, ratio 0.55) keeps it unflagged; both are in the normal ratio band the reviewer intended.

## Verification
Adversarial verifier, 23 October 2026. Read the whole final case, the notes file and the plan entry.
- All 9 note ids are in the table and each FIXED claim holds: repeat LP and repeat labs gone, index-specimen culture at 36 hours with Gram stain negative; initial drug block null and a real drug check (ibuprofen with dexamethasone) whose text does not echo the criterion; CT criterion, follow-up and HARD constraint removed, CT as waste with the canonical must and prohibition (plan C2 C); ratio 52.5/102 = 0.51 with one paired glucose in CSF and labs; chloride 95 gives anion gap 14; lactate local reference; reviewer's red-herring wording verbatim with the negative antigen kept; occupation "High school mathematics teacher" in both fields.
- Cross-field checks: GCS 15 (E4 V5 M6) supports the no-CT must; no Listeria risk factor at 35 and healthy, so no ampicillin must, correctly; `collected_before_antimicrobials` true agrees with the history (no antibiotics before arrival); differential excludes viral and meningococcal disease with the PCR and culture results; red-herring paths resolve.
- Found: the blood culture report grew S. pneumoniae in both aerobic bottles but `gram_stain` was null although `gram_stain` is ordered (same defect the M01 worker fixed). Set to "Gram-positive cocci in pairs from both positive aerobic bottles". `metadata.last_revised` set to 2026-10-23.
- `perfect_agent.py` ok (blood cultures, index LP, drug check); `case_io.py check` clean for this case.

## Condition audit (23 October 2026)
- Removed the stale `metadata.case_body_concerns[0]` ("check_drug_interactions was marked required with empty tool_parameters and no stored output ... reclassified to recommended"): the case now has a stored drug-check output, so the note is false; P02 and P03 verifiers removed the equivalent stale notes. No clinical field changed.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (4 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients
- Random blood glucose 102 mg/dL no longer flagged high: reference 70-140 mg/dL for a non-fasting sample

Re-run: `perfect_agent.py` ok; `case_io.py check` clean for the case; BACT-MEN case guards pass; synonym `--check` clean.
