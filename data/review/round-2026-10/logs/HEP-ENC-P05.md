# HEP-ENC-P05
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 067d3743-f6a8-4de7-a323-459deef6c259 | FIXED | "Exclusion studies" block deleted from `initial_tool_outputs.labs.panels`, so B12 appears once (Nutritional, 188 pg/mL, flagged low); the duplicate magnesium in the Nutritional panel deleted (BMP keeps 1.3 mg/dL); `abnormal_values_summary` and `interpretation` list each flagged analyte once. |
| caa0c178-d8a0-4638-955b-3f6a1c850639 | FIXED | The normal template MRI with the "lumbar puncture is gated on" line replaced in `initial_tool_outputs.mri` by the Wernicke study (periaqueductal and medial thalamic T2/FLAIR hyperintensity, mammillary body enhancement, pallidal T1 hyperintensity, no infarct) with structured findings; the `order_advanced_imaging` follow-up `request_mri_brain_wernicke` deleted. |
| d07af885-7c9f-41a1-91ea-2df4f312a207 | FIXED | No ascites is documented, so the `interpret_labs` paracentesis follow-up (`request_sbp_paracentesis`, PMN 72) is deleted and no paracentesis criterion is added (C6). |
| 7689f42d-f242-4759-96ed-c9ffb100bc9c | FIXED | Blood and urine culture criteria (`action-8`, `action-9-order-microbiology`) recommended as an occult-infection screen with specimen-only arguments (afebrile, WBC 5.8, CRP 4.1, no antibiotic); blocks report "no growth at 48 hours" with `collected_before_antimicrobials` null; removed from the stop rule. |
| 0f54d6e7-e379-44f5-9bd2-c0e723b7919e | FIXED | `interpret_labs` follow-up `request_lactulose_rifaximin` (ammonia 42 at 72 h) deleted (C1, C2); the admission ammonia 68 µmol/L stays once in the core labs; K-AMM pearl added; the HPI no longer gives the ammonia. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `followup_outputs` (`request_thiamine_empiric`, celiac nutrition DI), literature output and `action-4-search-medical-literature` | Thiamine and magnesium treatment and the 72-hour response delivered through `interpret_labs`; nutritional treatment filed as a drug check (whose content assumed a PPI she does not take); literature output echoing the expected evidence (C1, C4). | FIXED: deleted; literature criterion deleted, `initial_tool_outputs.literature_search` null. The pre-treatment thiamine 24 nmol/L stays in the initial labs; treatment is in the musts. |
| C | major | `diagnosis.accepted[0]`, `past_medical_history[0]`, HPI | "Child-Pugh B, MELD 13" undated and not derivable; no creatinine in the case (C9, C10). | FIXED: creatinine 1.3 mg/dL (female range 0.5-1.1) and BUN 30 mg/dL added, consistent with a week of vomiting; computed Child-Pugh B (9: bilirubin 2.4 2, albumin 2.6 3, INR 1.6 1, no ascites 1, grade II 2), MELD 18, MELD-Na 22; label "Child-Pugh B, MELD-Na 22"; history score removed. |
| D | major | `patient.history_present_illness` | "Her ammonia is 68 µmol/L" and "MELD 13" (timeline leak, C13). | FIXED: removed; HPI states she could not keep down her medicines during the vomiting (the basis of the precipitant must). |
| E | minor | `social_history.occupation`, `.alcohol` | "Nutritionist (ironic given celiac)"; "Never — NASH cirrhosis". | FIXED: "Nutritionist"; "Never". |
| B | major | `initial_tool_outputs.labs` | Template TSH 2.1 and zinc 82; no CRP; lactate "Within reference range" without value. | FIXED: TSH 3.2 (on levothyroxine), zinc 64, CRP 4.1 mg/L, lactate 1.6 mmol/L. |
| A | minor | `action-1-interpret-labs` | 12 named panels demanded. | FIXED: two-alternative core plus `thiamine_B1`, `B12` (plan Labs+). |
| B | minor | `initial_tool_outputs.ct`, `.eeg` | CT findings empty; EEG background "Symmetric with occasional asymmetries" contradicts itself; en dashes. | FIXED: canonical normal CT; EEG symmetry "Symmetric". |
| C | major | `action-5-check-drug-interactions` | Required with template expected evidence and no real content (C5). | FIXED: recommended (plan), alternatives name levothyroxine, calcium carbonate, ondansetron, thiamine, lactulose, rifaximin; output `check_levothyroxine_calcium_ondansetron_thiamine` placed last: calcium carbonate reduces levothyroxine absorption (separate by 4 hours), ondansetron QT risk with potassium 3.1 and magnesium 1.3, no interaction with thiamine, lactulose or rifaximin; avoid sedating antiemetics. |
| C | major | `assessment` | Thiamine 500 mg TID x3 then 250 mg daily (an accepted UK regimen) without the EFNS dose the plan sets; no magnesium, potassium, fluid or sodium-rate must despite Mg 1.3, K 3.1, Na 132 and pre-renal kidney injury; lactulose 30 mL TID without target; rifaximin listed as a new treatment although she takes it; no transplant referral for decompensated cirrhosis with recurrent HE; boilerplate haloperidol line; generic LP prohibition. | FIXED: MUST-THIA at 200 mg IV three times daily before glucose (500 mg TID accepted as an alternative, EFNS 2010); IV magnesium; MUST-K; rehydration with sodium rise of no more than 8 mEq/L in 24 hours; precipitant must (dehydration, hypokalemia, missed lactulose and rifaximin; restart rifaximin); MUST-LACT; ondansetron after electrolyte correction and QT check; folate, B12 and multivitamin with calcium separated from levothyroxine; gluten-free diet with dietitian; MUST-TX (MELD-Na 22). Prohibitions: PROHIB-BZD, sedating opioids (acetaminophen up to 2 g per day), dextrose before thiamine, under-dosing thiamine; LP line deleted. |
| C | minor | `ground_truth.differential` | Cerebellar stroke "MRI DWI to exclude" and brainstem encephalitis "MRI + CSF if indicated" written before the work-up; B12 188 with macrocytosis and distal vibration loss not considered (ruling 7). | FIXED: entries cite the MRI and the normal WBC/CRP; vitamin B12 deficiency neuropathy added as a moderate contributor. |
| C | minor | `key_clinical_evidence` | No pearl for magnesium and thiamine; "AASLD 2014" pearl. | FIXED: K_CLIN, K-AMM, score line, magnesium pearl added; existing Wernicke pearls kept. |
| E | minor | criteria, citations, metadata | Rationale = label; free-text citations. | FIXED: one-sentence rationales with keys; difficulty rationale updated. |

## Changes, in one paragraph a physician can read before re-reviewing

The policy now requires the core labs (with a pre-treatment thiamine level and B12) and the MRI, and recommends blood and urine cultures as an occult-infection screen, the EEG and a drug check; CT is optional. There is one MRI report, showing the Wernicke pattern (periaqueductal grey, medial thalami, enhancing mammillary bodies); the contradictory normal template is gone. The thiamine-treatment and ammonia-response panels, the nutrition "drug check", the paracentesis in a patient without ascites and the literature search are deleted. Each analyte appears once (B12 188 low, magnesium 1.3), and the panel gains creatinine 1.3 and BUN 30 (a week of vomiting), CRP, lactate and case-specific TSH and zinc. The label reads Child-Pugh B (9 points), MELD-Na 22. Musts: IV thiamine 200 mg three times daily before any glucose, IV magnesium, potassium, careful rehydration and sodium correction, treatment of the HE precipitants with lactulose titrated to 2-3 stools and rifaximin restarted, ondansetron after electrolyte correction and a QT check, folate, B12 and vitamins, gluten-free diet, transplant referral. Prohibitions: sedatives, sedating opioids, dextrose before thiamine, under-dosed thiamine.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EFNS_Wernicke_2010]`.
- `accepted[0]` changed under ruling 3 (C10 scores); ICD codes and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- The creatinine (1.3 mg/dL) and BUN (30 mg/dL) are new values the plan asked for; with them MELD-Na is 22, which makes the transplant referral a must. A lower creatinine would lower the score but not change the indication (decompensated cirrhosis with recurrent HE).
- The label leads with Wernicke encephalopathy under the HE condition; this is a deliberate concurrent-diagnosis case and the synonyms are HE terms, so an answer of "Wernicke encephalopathy" alone would not score. Confirm that is intended.
- The thiamine must accepts both the EFNS 200 mg TID and the 500 mg TID regimens, since both are guideline-supported.
- `fallback_tool_outputs.mri` (normal template) is never served because `initial_tool_outputs.mri` exists; left unchanged.

## Verification

Adversarial check, 23 Oct 2026. Read the log, the diff and the whole final case. Recomputed with the new creatinine 1.3: Child-Pugh B 9 (bilirubin 2.4 2, albumin 2.6 3, INR 1.6 1, no ascites 1, grade II 2), MELD 18, MELD-Na 22 (Na 132); label, key evidence, lab expected evidence and transplant must agree. All five notes are fixed: B12 and magnesium appear once each; one MRI (the Wernicke study) in `initial_tool_outputs.mri` with no gating line; no paracentesis output or criterion; cultures recommended; the ammonia trend is gone and the admission ammonia appears once. The thiamine must uses the EFNS dose before glucose; magnesium, potassium, rehydration and the restart of lactulose and rifaximin are present and consistent with the labs (K 3.1, Mg 1.3, Na 132, BUN 30). Drug-check content (calcium carbonate and levothyroxine, ondansetron QT with low K and Mg) is correct and matches the medication list.

Found and fixed one error the round left: the differential entry "Celiac-related neurological syndrome (gluten ataxia, peripheral neuropathy)" carried ICD G31.84 (mild cognitive impairment); changed to G32.81 (cerebellar ataxia in diseases classified elsewhere). `perfect_agent.py` and `case_io.py check` clean after the edit.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

- `fallback_tool_outputs.mri` set to null: an unreachable normal template that duplicated and could contradict the case's own MRI; `initial_tool_outputs.mri` always answers the order.

Checks: `perfect_agent.py` pass; `case_io.py check` schema and synonym guard OK, no test failure names this case; leak guard clean.
