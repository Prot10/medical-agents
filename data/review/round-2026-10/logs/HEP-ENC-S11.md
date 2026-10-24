# HEP-ENC-S11
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| b177af3e-1030-40f2-aa3d-bc4183e890aa | FIXED | The lactulose must now uses the canonical text (titrated to 2-3 soft bowel movements per day, ACG 2026 recommendation 10, EASL 2022, with the over-titration warning). The literature follow-up quoting the 2014 "2-4 stools" finding (`request_literature_search_he_management`) is deleted, along with `action-3-search-medical-literature` (C4). No "2-4" remains in the case. |
| 65f1c0dd-9492-466b-a72f-73360c71870c | FIXED | The ammonia-trend follow-up (`request_lactulose_restart_treatment_response`: 58 to 34 µmol/L with GCS 14 at 36 hours) is deleted (C1, C2). A new prohibition forbids serial ammonia to guide lactulose titration (ACG 2026 recommendation 5); the red herring and the ammonia pearl cite ACG 2026 recommendation 5 and key concept 14. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.diagnosis.accepted[0]` | "Grade II-III" and "Child-Pugh B, MELD 13" from an earlier visit (C10; plan 1.2). | FIXED: West Haven grade III (lethargic, disoriented to time and place, GCS 12); Child-Pugh C (10: bilirubin 2.8 2, albumin 2.9 2, INR 1.5 1, small ascites 2, HE 3), MELD 15, MELD-Na 16; derivation in `key_clinical_evidence[0]`; the prior score in `past_medical_history[0]` dated to her last hepatology review and removed from the HPI. |
| B | minor | `past_medical_history[0]` | "on azathioprine and prednisone taper" while the medication list gives prednisone 5 mg maintenance. | FIXED: "maintained on azathioprine and low-dose prednisone". |
| B | major | `initial_tool_outputs.microbiology` | The `blood_culture` block mixed lactate, "Pending - no growth at 48 hours" blood cultures and a urinalysis, with the template "No organism isolated to date" and `collected_before_antimicrobials` true in a case with no antibiotic (C7). | FIXED: blood block reports two sets, no growth at 48 hours, flag null; lactate 1.4 mmol/L moved to the labs; the urinalysis moved to the urine follow-up (microscopy without pyuria, culture no growth at 48 hours). |
| A | major | `followup_outputs` (`request_paracentesis_sbp_exclusion`) | Paracentesis served through `interpret_labs` with no criterion (C6). | FIXED: `order_microbiology` `ascitic_fluid` follow-up (`request_diagnostic_paracentesis`): WBC 130, PMN 44 cells/mm3, protein 1.1 g/dL, ascitic albumin 1.3 g/dL (from SAAG 1.6), Gram stain and culture negative, ultrasound-guided for the small ascites; new required criterion `action-diagnostic-paracentesis`. |
| A | minor | `action-6`, `action-7-order-microbiology` | Cultures required with `before_antimicrobials` and test lists in an afebrile patient with WBC 5.2 (C7). | FIXED: recommended, specimen-only arguments, canonical labels, case-specific expected evidence. |
| C | major | `followup_outputs` (DI), `action-4-check-drug-interactions` | DI advised haloperidol for agitation (C12), had a generic expected evidence, and missed the constipating calcium carbonate, the long-term steroid and the diuretics during poor intake. | FIXED: trigger `check_azathioprine_prednisone_calcium_carbonate_diuretics`, placed last, recommended (plan): calcium carbonate constipation, immunosuppression and infection, no abrupt prednisone withdrawal, diuretics held during the episode, penicillin rash not a contraindication to ceftriaxone if one is needed; haloperidol line deleted. |
| B | minor | `initial_tool_outputs.labs` | "umol/L"; template TSH 2.1 and zinc 82; no CRP or lactate in the labs (C9). | FIXED: µmol/L; TSH 2.8, zinc 63; panel "Lactate and CRP" (lactate 1.4, CRP 2 mg/L); summaries rebuilt. |
| A | minor | `action-1-interpret-labs` | Nine named panels demanded (C9). | FIXED: two-alternative core; canonical label and rationale. |
| C | minor | `action-2-order-ct-scan` | Required (plan keeps it), but the label claimed CT is "mandatory given coagulopathy" before proceeding. | FIXED: label "Non-contrast CT head"; rationale names why it is required here (lives alone, unwitnessed fall possible, platelets 102, INR 1.5). |
| C | major | `ground_truth.assessment.required_recommendations` | Lactulose "every 4-6 hours ... 2-4 stools" (C3); a paracentesis must that duplicates a criterion; no plan for diuretics, steroids, calcium carbonate, living alone or transplant. | FIXED: 8 musts: precipitants, MUST-LACT, lactulose by tube or enema with airway monitoring, rifaximin, hold diuretics then restart at 100:40, continue immunosuppression without abrupt steroid withdrawal, discharge adherence plan with supervision at home, transplant referral (MELD-Na 16). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Benzodiazepine line without the canonical text; generic LP line; "do not attribute AMS to HE without excluding" and "do not anchor on ammonia" are reasoning, not recommendations (C12). | FIXED: PROHIB-BZD; opioid line with acetaminophen up to 2 g per day; no serial ammonia to guide titration (note 65f1c0dd); the other three deleted. |
| C | minor | `ground_truth.differential` | SBP "moderate" before the tap result (C14); azathioprine neurotoxicity "excluded by ... response to lactulose" (post-treatment). | FIXED: SBP low with PMN 44; sepsis-associated encephalopathy added (low, immunosuppressed but no inflammatory response); azathioprine excluded by dose and duration. |
| D | minor | `key_clinical_evidence`, `red_herrings` | Pearl "Autoimmune hepatitis is an under-represented etiology in the HEP-ENC dataset" (author note); "(AASLD 2014)" citations; "umol/L"; em dashes. | FIXED: pearls rewritten (score, clinical diagnosis, K-AMM, precipitants, adherence, immunosuppression and occult infection); red herring cites ACG 2026 and grade III. |
| E | minor | HPI, social history, gait, metadata | Em dashes in new-to-edit text; metadata listed the literature search as required and a lactulose response. | FIXED: punctuation; metadata difficulty fields updated; no em dashes remain. |

## Changes, in one paragraph a physician can read before re-reviewing

The policy requires the core laboratory work-up, the diagnostic paracentesis (PMN 44 cells/mm3, no SBP) and a CT head (she lives alone, platelets 102, INR 1.5); blood and urine cultures and a medication review are recommended. The literature search with its "2-4 stools" quote and the post-lactulose ammonia trend are gone. The label reads West Haven grade III, Child-Pugh C (10), MELD-Na 16, precipitated by constipation and lactulose non-adherence; "Child-Pugh B, MELD 13" is dated to her last hepatology review. The mixed microbiology block is split into blood cultures, urine and labs (lactate 1.4, CRP 2). The drug check now names calcium carbonate as constipating, the infection and steroid issues of azathioprine and prednisone, and holding the diuretics, and no longer recommends haloperidol. Musts: treat the precipitants, lactulose to 2-3 stools (by tube or enema if she cannot swallow) with airway monitoring, rifaximin, hold the diuretics then restart at 100:40, keep the immunosuppression without abrupt steroid withdrawal, an adherence and home-supervision plan, transplant referral. Prohibitions: sedatives, opioids, serial ammonia to guide treatment.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_decomp_2018]`, `[AASLD_ascites_2021]`; `[Bajaj_2011]` retired from this case.
- `accepted[0]` changed under ruling 3 (C10 scores, grade III per plan 1.2); ICD codes and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- Plan Q6: the paracentesis is required although the ascites is small (EASL 2018, AASLD 2021); the report states an ultrasound-guided tap.
- The plan's penicillin-rash clause applies wherever a must gives ceftriaxone; no must gives an antibiotic here (PMN 44, bilirubin 2.8 below the threshold for primary SBP prophylaxis), so the clause sits in the drug-check warnings instead.
- The diuretic hold, the steroid-continuity must and the home-supervision must are new clinical content; trim them if the case should stay on the two precipitants.
- Grade III rather than II: disoriented to place, lethargic and following commands inconsistently. Child-Pugh is C (10) at grade III; at grade II it would be 9, class B.
- New values carry no diagnostic weight: TSH 2.8, zinc 63, CRP 2, ascitic albumin 1.3 g/dL (derived from SAAG 1.6).

## Verification
Adversarial check (23 Oct 2026) of the final case against the log, the plan and the notes.
- Notes: both ids present and FIXED in the file: no "2-4" anywhere, the literature follow-up and criterion are gone, MUST-LACT is canonical; the ammonia-trend follow-up is gone and a prohibition forbids serial ammonia to guide titration.
- Checked: MELD 15, MELD-Na 16 (Cr 0.8 counted as 1, bilirubin 2.8, INR 1.5, Na 136) and Child-Pugh C 10 (small ascites 2, grade III 3) recomputed; grade III fits the exam (lethargic, disoriented to time and place, inconsistent commands); µmol/L; the mixed microbiology block is split; SAAG 1.6 = 2.9 - 1.3; CT required per plan with a case-specific rationale; DI recommended per plan; stop rule = the three required ids; no em dashes or template residues.
- Found and changed: B, major, `fallback_tool_outputs.eeg` (left from before the round): the case has no EEG output of its own, so an agent ordering an EEG received a normal awake EEG with a 9-10 Hz posterior dominant rhythm, which contradicts grade III HE (and the metadata kind said "abnormal_nonspecific"). Added `initial_tool_outputs.eeg` consistent with the exam (generalized 2.5-4 Hz theta-delta slowing without a posterior dominant rhythm, intermittent fronto-predominant triphasic waves attenuated by alerting, no epileptiform discharges or seizures, toxic-metabolic encephalopathy); fallback `eeg` set to null and removed from `metadata.fallback_tool_kinds`. No EEG criterion added (the plan has none for S11).
- perfect_agent -v and case_io check clean after the edit.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
