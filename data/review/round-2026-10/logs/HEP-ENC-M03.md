# HEP-ENC-M03
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| b8fd889d-9eaa-47eb-8317-780425e3f589 | FIXED | Duplicate TSH 2.1 mIU/L (`initial_tool_outputs.labs.panels.TSH`) deleted together with the "Exclusion studies" block; the Thyroid panel keeps TSH 8.4 µIU/mL with free T4 0.7 ng/dL. The levothyroxine increase that sat in a drug-interaction follow-up (`request_thyroid_treatment`, ruling 4) is now a must; the hypothyroid red herring (`red_herrings[1]`) points at `initial_tool_outputs.labs.panels.Thyroid[0]`. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.diagnosis.accepted[0]`, `past_medical_history[0]` | "Child-Pugh B, MELD 12" not derivable: computed Child-Pugh B (9), MELD 13, MELD-Na 16 (C10). | FIXED: label "Child-Pugh B, MELD-Na 16"; history score dated ("at her last clinic review"); score pearl added. |
| B | major | `patient.clinical_history.medications` | Methadone 80 mg daily (social history, HPI, exam, toxicology) and the trimethoprim-sulfamethoxazole started a week ago (HPI) were missing from the medication list. | FIXED: both added. The plan calls the methadone check a carry-over "for a drug she does not take"; she does take it (see Open questions). |
| C | major | `followup_outputs` (lactulose/rifaximin, thyroid treatment, methadone check, literature) | Ammonia 72 to 44 "post-lactulose increase + rifaximin" (C1, C2); levothyroxine dosing filed as a drug check; methadone check that ordered an ECG; literature follow-up (C4). | FIXED: all deleted; a single real drug-interaction follow-up placed last. |
| C | major | `followup_outputs` (`interpret_labs` paracentesis) | Ascites present but the tap was filed under `interpret_labs` with no criterion (C6). | FIXED: new required `action-diagnostic-paracentesis` (`order_microbiology`, `ascitic_fluid`); the report (PMN 45, SAAG 1.6) moved to microbiology with total protein 1.3 g/dL, ascitic albumin 1.2 g/dL, Gram stain and one culture time point. |
| D | major | `action-3-search-medical-literature` | Required literature search (C4). | FIXED: deleted (no initial output existed). |
| C | major | `action-4-check-drug-interactions` | Required with template expected evidence; the real interaction (trimethoprim with spironolactone, hyperkalaemia; with methadone, QT) was absent. | FIXED: recommended (plan says optional; see Open questions), alternatives name the drugs, output with real content. |
| C | major | `ground_truth.assessment` | Lactulose 2-4 stools (C3); "Rifaximin ... restart if interrupted" and a prohibition about rifaximin with TMP-SMX although she is not on rifaximin; counselling to avoid broad-spectrum antibiotics for "gut flora"; boilerplate opioid prohibition contradicting methadone maintenance; generic LP prohibition. | FIXED: MUST-LACT; precipitant must (constipation, lactulose adherence, treat the UTI); rifaximin added because the episode occurred on lactulose prophylaxis; stop TMP-SMX at course end and check potassium; levothyroxine adjustment with recheck at 6-8 weeks; continue methadone without abrupt change; MUST-TX (MELD-Na 16, decompensated). Prohibitions: PROHIB-BZD; no additional opioids or sedatives beyond methadone, acetaminophen up to 2 g per day; LP and rifaximin lines deleted. |
| B | major | `initial_tool_outputs.labs` | "Exclusion studies" block; template zinc 82; no CRP; toxicology reference range "Methadone maintenance - expected" (interpretation in the range field) with a positive screen flagged normal (C9). | FIXED: magnesium 2.0 mg/dL and lactate 1.1 mmol/L with ranges, CRP 4.0 mg/L, zinc 70; drug screen reference "Negative", positive flagged; summary and interpretation complete. |
| A | minor | `action-1-interpret-labs` | 9 named panels demanded. | FIXED: two-alternative core. |
| C | major | `action-7`, `action-8-order-microbiology` | Cultures required "before the first antimicrobial dose" in an afebrile patient with WBC 6.2 (C7). | FIXED: recommended screen, specimen-only arguments; urine rationale names the UTI treated this week. |
| B | major | `initial_tool_outputs.microbiology`, urine follow-up | "Specimen taken before the first antimicrobial dose" while she has been on trimethoprim-sulfamethoxazole for a week; "No organism isolated to date". | FIXED: `collected_before_antimicrobials` false for blood, urine and ascitic specimens, stated in the impressions; one time point. |
| B | minor | `initial_tool_outputs.ct` | Empty findings; "restricted diffusion" on CT (C8). | FIXED: canonical normal CT plus mild atrophy. |
| C | minor | `ground_truth.differential` | Hypothyroid encephalopathy left moderate; "rapid lactulose response" (a deleted follow-up) used as evidence; SBP entry conditional ("if ascites present") though ascites is documented; methadone not considered. | FIXED: hypothyroid encephalopathy low (contributor); opioid toxicity added (low); SBP low with PMN 45; MCI entry without the response argument. |
| C | minor | `ground_truth.red_herrings`, `metadata.difficulty_description` | Metadata names a "methadone red herring" that did not exist; the opioid-positive screen is a real distractor. | FIXED: red herring added (opioid-positive screen on maintenance, therapeutic level). |
| C | minor | `key_clinical_evidence[3]` (old) | "Broad-spectrum antibiotics disrupt the gut microbiome on which lactulose/rifaximin efficacy depends; ... under-recognized HE precipitant" overstated a speculative mechanism. | FIXED: hedged pearl; label precipitant text kept (see Open questions). |
| E | minor | criteria, citations, pearls, metadata | Rationale = label; free-text citations; "(AASLD 2014)". | FIXED: one-sentence rationales with keys, K-AMM, score pearl, difficulty rationale updated. |

## Changes, in one paragraph a physician can read before re-reviewing

The policy requires the core labs and a diagnostic paracentesis (ascitic PMN 45 cells/mm3, no SBP), and recommends blood and urine cultures as an infection screen, the EEG and a drug check; CT is optional. The duplicate TSH 2.1 is gone, so the thyroid panel reads only TSH 8.4 with free T4 0.7. The literature search, the serial ammonia, the levothyroxine "drug check" and the methadone check are deleted. The medication list now includes the methadone maintenance (80 mg daily) and the trimethoprim-sulfamethoxazole started a week ago, which the history already described; since she is on that antibiotic, every culture is marked as collected during therapy. The label reads Child-Pugh B (9 points), MELD-Na 16. Labs gain magnesium, lactate, CRP and a case-specific zinc, and the opioid-positive drug screen is flagged with a plain reference range; a red herring now covers it (therapeutic level, no toxicity). The drug check reports the trimethoprim-spironolactone hyperkalaemia risk and the possible QT effect with methadone. Musts: lactulose to 2-3 stools, treat constipation and the UTI and check lactulose adherence, add rifaximin (recurrence on lactulose), stop TMP-SMX at the end of the course and check potassium, increase levothyroxine with recheck at 6-8 weeks, continue methadone unchanged, and transplant referral. Prohibitions: sedatives, and no opioids beyond her methadone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_decomp_2018]`, `[AASLD_ascites_2021]`.
- `accepted[0]` changed under ruling 3 (C10 scores); ICD codes and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- Plan M03 calls F4 a methadone check "for a drug she does not take". Methadone 80 mg daily is in the social history, HPI, exam and toxicology; only the medication list lacked it. I deleted F4 as planned (it ordered an ECG and declared the level "no evidence of accumulation") but added methadone to the medication list and folded the relevant content into the new drug check.
- Plan M03 says DI optional. I made it recommended: trimethoprim-sulfamethoxazole with spironolactone is a documented hyperkalaemia interaction that changes management (stop the antibiotic at course end, check potassium).
- The label's precipitant "recent TMP-SMX antibiotic use (gut microbiome disruption reducing lactulose efficacy)" is a speculative mechanism; the better-supported precipitants are the constipation, missed doses and the UTI itself. I kept the label text apart from the scores (ruling 3) and dropped "rifaximin" from it, since she is not on rifaximin. A reviewer may want the precipitant reworded.
- Cultures stay recommended per plan, although the HPI contains a urinary tract infection (C7's "infective precipitant in the HPI" would make them required). She is afebrile, WBC 6.2, and already on treatment.
- Rifaximin was added as a must on the reading that lactulose "HE prophylaxis" means a prior overt episode; the history does not state the prior episode explicitly.

## Verification

Checked (adversarial verifier, 23 Oct 2026): note b8fd889d is in the table and fixed (TSH reported once, 8.4 with free T4 0.7; the red herring points at `Thyroid[0]`; the levothyroxine change is a must, not a drug check). Recomputed: Child-Pugh B 9 (bilirubin 2.2, albumin 2.8, INR 1.4, mild ascites, grade II), MELD 13, MELD-Na 16, consistent in label, key evidence and MUST-TX. Grade II fits the exam. Methadone and trimethoprim-sulfamethoxazole, already in the history, are now in the medication list, so `collected_before_antimicrobials` false on all three specimens is consistent. Ascitic PMN 45, SAAG 1.6 = 2.8 - 1.2; ascitic protein 1.3 g/dL does not meet the primary-prophylaxis criteria here (Child-Pugh 9 but bilirubin 2.2, creatinine 0.9, sodium 134). Drug-check content (trimethoprim-spironolactone hyperkalaemia, QT with methadone) is real and agrees with the allergies (codeine intolerance) and medicines. Differential updated to the results; no musts contradict prohibitions; no leakage in the patient block.

Found, not changed: the label keeps "recent TMP-SMX antibiotic use (gut microbiome disruption reducing lactulose efficacy)" as a precipitant while the case's own pearl (`key_clinical_evidence[5]`) calls that evidence limited, and antibiotics that reduce colonic flora are otherwise used to treat HE. The better-supported precipitants (constipation, missed doses, the urinary tract infection) are in the musts. Ruling 3 forbids rewording `accepted[0]` without a reviewer ruling, and the worker already raised it under Open questions; I support rewording the precipitant clause to "constipation, missed lactulose doses and a urinary tract infection under treatment" if Andrea agrees.

Changed: nothing. `perfect_agent.py` and `case_io.py check` clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

- Leak guard (Andrea, 24 Oct 2026: any-query outputs must not repeat any criterion's expected evidence, including their own): `ground_truth.action_criteria[action-4-check-drug-interactions].expected_evidence` reworded as the conclusion a grader checks, in words not shared with the stored `check_drug_interactions` follow-up, whose report text is unchanged; clinical content unchanged.
- `ground_truth.diagnosis.accepted[0]`: the speculative mechanism "(gut microbiome disruption reducing lactulose efficacy)" removed; TMP-SMX is now a possible contributor (UTI treated in the past week), constipation the precipitant. ICD unchanged (summary open question, M03 precipitant mechanism).

Checks: `perfect_agent.py` pass; `case_io.py check` schema and synonym guard OK, no test failure names this case; leak guard clean.
