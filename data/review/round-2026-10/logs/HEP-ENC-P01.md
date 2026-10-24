# HEP-ENC-P01
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 41da0ede-9688-4af3-a323-4ca09fa4e4da | FIXED | `ground_truth.diagnosis.accepted[0]` relabelled "Overt hepatic encephalopathy (West Haven grade II), cryptogenic cirrhosis (Child-Pugh B, MELD-Na 13), ..." (C11). The grade I-II band and "evolving from covert/minimal HE" are gone. For grade II to hold, `patient.neurological_exam.mental_status` now reads lethargic, disoriented to time and oriented to place and person, with asterixis. The old "disoriented x2 (time and place)" met the grade III criterion of spatial disorientation (AASLD/EASL 2014 operative criteria). The covert/overt pearl was added to `key_clinical_evidence` (ACG 2026 key concept 1). |
| 8da6b4b7-dd75-496a-ae30-3570972bf616 | FIXED | `assessment.required_recommendations[1]` is MUST-LACT: 2-3 soft bowel movements per day (ACG 2026 rec. 10; EASL 2022), with the over-titration warning. `required_recommendations[2]` is MUST-THERAG and repeats the 2-3 target. The old "lactulose 30 mL TID" has no target and is gone. |
| e9c07b1d-c5f5-4306-9be8-3360366f5b28 | FIXED (treatment as tool: DECLINED by design, C16) | Deleted the `interpret_labs` `request_lactulose_rifaximin` follow-up, which reported GCS 12 to 14 and resolved asterixis at 72 h before the agent acted. Deleted the old must "observe for clinical improvement as diagnostic of HE". MUST-THERAG replaces it: review adherence and symptoms at 4-8 weeks, and reconsider the diagnosis if he does not improve (ACG 2026 KC 8). The theragnostic pearl and the red herrings no longer call the lactulose response diagnostic. The case scores treatment through musts, not through a tool call (ruling 4). |
| 1b529040-e50b-4e63-a57a-49e804d3c2eb | FIXED | Serial ammonia (68 to 42 µmol/L at 72 h) deleted with that follow-up (C2). One admission ammonia (68, range 11-51, flagged) stays, now in its own `labs.panels.Ammonia`. K-AMM pearl added. The ammonia red herring (`red_herrings[1]`) is repointed to that panel and no longer uses ammonia to grade. |
| 72abc830-ec3d-46ca-b242-5c62c567586a | FIXED | He is afebrile (37.0 °C), WBC 6.8, CRP 2.6, with no source. Blood cultures (`action-8-order-microbiology`) and urine culture (`action-9-order-microbiology`) are now `recommended`, with arguments `{"specimen": ...}` only and the C7 recommended label and rationale. Both are out of the stop rule. The "before the first antimicrobial dose" wording, `before_antimicrobials` and the culture-gating text are gone, and `collected_before_antimicrobials` is null because the case gives no antibiotic. There is no ascites on exam (C6), so the `interpret_labs` `request_sbp_paracentesis` follow-up (PMN 38 from a "minimal ascites" tap) is deleted, and no paracentesis criterion is added. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.clinical_history.medications[0]`, `history_present_illness` | Clonazepam 0.5 mg nightly cannot plausibly give a serum level of 84 ng/mL. Expected steady state is about 5 ng/mL, and roughly 15 ng/mL even with a 2-3 fold longer half-life in cirrhosis. So the "accumulation" precipitant did not hold together pharmacologically. | FIXED: five weeks before admission his primary care physician increased the dose from 0.5 mg nightly to 1 mg twice daily for anxiety (medication entry and HPI). Accumulation over the following weeks fits the 3-week decline and the 84 ng/mL level. The level, the label and the rest of the precipitant story are unchanged. |
| B | minor | `patient.neurological_exam.mental_status` | GCS 12 (E3V4M5) does not fit a patient who does finger-nose testing and is examined for asterixis. Both need him to obey commands (M6). | FIXED: GCS 13 (E3V4M6), lethargic, opens eyes to voice. |
| D | major | `history_present_illness`, `neurological_exam.additional` | Timeline leaks (C13): "His ammonia is only mildly elevated at 68 µmol/L. His CT and EEG show non-specific changes", and "Urine drug screen positive benzodiazepines". | FIXED: results removed. The facts stay: medication history and absence of stigmata. |
| D | major | `action-3-search-medical-literature`, `initial_tool_outputs.literature_search` | Recommended literature search, whose stored output echoed the expected evidence (C4). | FIXED: criterion deleted and output set to null. The fallback stays for an unprompted search. |
| B | major | `followup_outputs` (`analyze_eeg` `request_continuous_eeg`) | Serial EEG reporting improvement "after clonazepam reduction", which is a post-treatment change (C8). | FIXED: deleted. The admission EEG in `initial_tool_outputs.eeg` is unchanged. |
| C | major | `followup_outputs` (DI), `action-4-check-drug-interactions` | The DI output prescribed doses: a "0.25 mg every 2 weeks" taper that cannot be done over 2-4 weeks, mirtazapine, and lorazepam 0.25-0.5 mg. It also called buspirone a drug with "minimal hepatic metabolism", which is wrong (buspirone is extensively metabolised by CYP3A4 and is reduced in hepatic impairment). Its expected evidence was generic. | FIXED: the check stays required (C5: the sedatives are the precipitant). The trigger is renamed `check_clonazepam_quetiapine` and the output is rewritten: clonazepam CYP3A4 accumulation in cirrhosis, additive quetiapine CNS depression, spironolactone with lactulose fluid and electrolyte risk, no lactulose or rifaximin interaction, withdrawal-seizure risk of an abrupt stop or of flumazenil, and avoidance of other sedatives. It now sits last in the pathway, with case-specific expected evidence. |
| C | major | `followup_outputs` (PHES), `action-5-order-specialized-test` | PHES done during an overt grade II episode with sedative effect was used to "confirm minimal HE" and to show that the prior MCI was covert HE. Psychometric batteries are validated for covert HE and cannot be interpreted during overt HE. The report also had unnamed rows and only 4 of the 5 PHES subtests. | FIXED: tier `optional` (plan). The report names all five subtests with their SD points (sum -7, `test_type` `neuropsych_battery`) and records the testing conditions. Its impression says the score shows current impairment and cannot establish a covert baseline. Label, rationale and expected evidence are reframed. The label no longer rests on "PHES -7". A new must asks for psychometric reassessment after recovery. |
| B | minor | `initial_tool_outputs.labs` | "Exclusion studies" block (magnesium, lactate as "Within reference range"). Template TSH 2.1 and zinc 82. INR and ammonia under LFTs. No CRP. Summary called albumin 3.0 "low-normal" and commented on the ammonia (C9). | FIXED: magnesium 2.0 mg/dL, lactate 1.1 mmol/L, CRP 2.6 mg/L, TSH 2.7, zinc 71, each with a range. INR moved to Coagulation and ammonia to its own panel. Ethanol given as "<10 mg/dL". Summaries list only flagged values. |
| A | minor | `action-1-interpret-labs` | Required 9 named panels (C9). | FIXED: the two C9 alternatives with no case extras (none listed in plan section 4). The clonazepam level stays in the report, which is returned whole. |
| B | minor | `initial_tool_outputs.ct` | Empty findings and "restricted diffusion" on CT (C8). | FIXED: an atrophy finding (kept as case-specific, without disproportionate ventriculomegaly, which fits the NPH differential) plus the canonical normal finding. The phrase "ventricles and sulci appropriate for age" is dropped because it contradicts the atrophy. |
| B | minor | `initial_tool_outputs.microbiology`, urine follow-up | Templated "No organism isolated to date. Specimen taken before the first antimicrobial dose" in a case with no antibiotic. | FIXED: "no growth at 48 hours" as a single time point. Urine microscopy result added (no pyuria). |
| C | minor | `assessment.required_recommendations` | Rifaximin was mandated at a first overt episode. "PHES to confirm covert HE" was set during the overt episode. The clonazepam taper had no starting point. There was no transplant referral although cirrhosis is decompensated (diuretic-treated ascites, overt HE). | FIXED: rifaximin removed (plan: recurrent episodes only). The musts are now MUST-PRECIP (reduce to the previous 0.5 mg, hold while drowsy, taper over 2-4 weeks, stop quetiapine), MUST-LACT, MUST-THERAG, psychometric reassessment after recovery, the etiology work-up (kept, made specific) and MUST-TX (MELD-Na 13). |
| C | minor | `assessment.prohibited_recommendations` | Benzodiazepine line recommending haloperidol (C12). Generic LP prohibition with no LP. Acetaminophen dose unspecified. Flumazenil not addressed in a long-term benzodiazepine user. | FIXED: PROHIB-BZD. Opioid line now says acetaminophen up to 2 g per day. LP line deleted. Abrupt-stop line now also covers flumazenil. Ammonia and cholinesterase-inhibitor lines reworded. |
| C | minor | `ground_truth.differential` | "Benzodiazepine accumulation as sole cause" was `high` although the label makes it the precipitant of HE. Alzheimer key features cited PHES and the lactulose response as diagnostic (ruling 7). | FIXED: benzodiazepine-only `moderate`, with the features that point to concurrent HE. Alzheimer and occult-alcohol key features rewritten from the case's results (ethanol <10). |
| A | minor | all `action_criteria`, citations | Rationales repeated the labels. Citation lists mixed keys and free text. The CT label said "before any LP" in a case with no LP (C17). | FIXED: one-sentence rationales with keys, plan labels, and criteria in plan 3.1 order (labs, blood cultures, urine, CT, EEG, PHES, DI). Follow-ups ordered urine, PHES, DI. |
| A | minor | `ground_truth.stop_rule` | Required ids included the two culture criteria, which are no longer required. | FIXED: `required_before_assessment` = labs and DI, the only two required criteria. `max_additional_actions` 0. |
| E | minor | `metadata.difficulty_description`, `difficulty_rationale` | Described the therapeutic trial as the diagnostic tool, and "5 required tools + PHES + serial EEG". | FIXED: reworded to the rebuilt policy. |

## Changes, in one paragraph a physician can read before re-reviewing

The label is now overt HE, West Haven grade II, in cryptogenic cirrhosis (Child-Pugh B 7, MELD-Na 13), precipitated by clonazepam accumulation with quetiapine. The exam was changed to support grade II: he is lethargic, GCS 13 (E3V4M6), disoriented to time only, with asterixis. The clonazepam history now says the dose was raised five weeks ago from 0.5 mg nightly to 1 mg twice daily, so the serum level of 84 ng/mL is plausible. The HPI and exam no longer give the ammonia, CT, EEG or drug-screen results. Several deleted items reported treatment effects or did not belong in the pathway: the 72-hour "lactulose plus rifaximin" panel (GCS 14, ammonia 42), the post-reduction EEG, the paracentesis (there is no ascites), and the literature search. The pathway is now core labs (required; one ammonia, clonazepam level, real magnesium, lactate, CRP, TSH and zinc values), blood and urine cultures (recommended: he is afebrile, WBC 6.8, no source), CT (optional; atrophy, no acute lesion), EEG (recommended), PHES (optional), and a medication review of clonazepam and quetiapine in cirrhosis (required, last). The PHES report now says it was done during the acute encephalopathy and cannot diagnose covert HE. The musts are:
- reduce and then taper clonazepam;
- stop quetiapine;
- lactulose to 2-3 soft stools a day;
- review at 4-8 weeks;
- psychometric reassessment after recovery;
- etiology work-up of the "cryptogenic" cirrhosis;
- transplant referral.

The prohibitions cover sedatives for agitation, sedating opioids, an abrupt clonazepam stop or flumazenil, grading by ammonia, and a cholinesterase inhibitor. Rifaximin is no longer required.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1 (`[ACG_HE_2026]`, `[EASL_HE_2022]`).
- `accepted[0]` changed under ruling 3 (C10 scores and C11 grade; plan CENTRAL 6). No ICD or synonym change; the label now begins "Overt hepatic encephalopathy", which the existing synonym "overt hepatic encephalopathy" already covers.

## Open questions for Andrea (judgment calls you could not settle)

- Clonazepam dose: I changed the history to a dose increase five weeks ago (0.5 mg nightly to 1 mg twice daily). That keeps the 84 ng/mL level and the accumulation precipitant pharmacologically credible. The alternative is to keep 0.5 mg nightly and lower the level to about 15-20 ng/mL, which would weaken the precipitant. Confirm.
- Orientation: to support the plan's grade II, I changed "disoriented x2 (time and place)" to disoriented to time only. Under the AASLD/EASL 2014 operative criteria, disorientation to place is grade III. If you prefer the original exam, the label should be grade III instead.
- Ascites points: he takes spironolactone for previously documented mild ascites but has none on exam. Following the plan, I scored ascites from the exam (1 point, Child-Pugh 7). Scoring it as controlled mild ascites would give 8, still class B, so the label does not change.
- Transplant referral: I added MUST-TX (decompensated cirrhosis with overt HE and diuretic-treated ascites). Although the episode has a reversible sedative precipitant, this follows M07. Drop it if you consider a drug-precipitated first episode with MELD-Na 13 below the referral threshold.

## Verification

Adversarial verifier, 23 Oct 2026. Read the log, the full diff, the old patient block and the final case.
- The five notes are confirmed fixed:
  - The label is "Overt ... West Haven grade II". The exam now supports it: disoriented to time only, lethargic, with asterixis.
  - MUST-LACT gives 2-3.
  - The 72-hour response panel is deleted and MUST-THERAG reviews at 4-8 weeks.
  - There is one ammonia.
  - The cultures are `recommended` and out of the stop rule.
  - The paracentesis is deleted: there is no ascites on exam, as the plan says.
- Scores were recomputed: MELD 12, MELD-Na 13 (Na 136); Child-Pugh B 7, or 8 if the ascites is scored as diuretic-controlled. The class is the same either way.
- The PHES subtest points sum to -7. The clonazepam dose increase makes 84 ng/mL plausible. The drug-interaction check routes correctly for "clonazepam" and "quetiapine". The stop rule equals the required ids (labs and the drug-interaction check).
- Found and fixed:
  - **Red herring.** `red_herrings[2].intended_effect` said the trap was to "miss underlying covert HE", which contradicts the overt grade II label (C11). It now says "miss the concurrent hepatic encephalopathy".
  - **Fallback MRI.** It said "ventricles and sulci appropriate for age", against the CT's atrophy "more than expected for age". The worker had dropped the same phrase from the CT for this reason. It now states the same atrophy without disproportionate ventriculomegaly.
- Left as is, by the plan:
  - MUST-LACT and MUST-THERAG overlap: both mention lactulose to 2-3, and the plan asks for both verbatim.
  - The drug-interaction label mentions rifaximin, which is harmless.
- `perfect_agent.py HEP-ENC-P01 -v` passes; `case_io.py check` reports no failure naming the case.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
