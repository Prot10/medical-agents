# HEP-ENC-P04
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| b15cdee4-1d9b-4a39-b382-9e1b4cdc719c | FIXED | The boilerplate "Do not prescribe benzodiazepines ... (use haloperidol ...)" (`assessment.prohibited_recommendations[0]`) replaced by PROHIB-BZD (reorientation, safe environment, treat the precipitant), and a case-specific prohibition added: "Do not give haloperidol or other antipsychotics for agitation: they can markedly worsen the dystonia and parkinsonism of neurological Wilson disease." The drug-interaction output also warns against antipsychotics. |
| 8ee3aef0-12c4-499c-b8a0-81305ca89342 | FIXED | The `interpret_labs` follow-up `request_lactulose_rifaximin` (ammonia 78 to 46 "72h lactulose + rifaximin", "week 2 on trientine" response) deleted (C1, C2); the admission ammonia 78 µmol/L stays once in the core labs (range 11-51); K-AMM pearl added; the HPI no longer gives the ammonia. |
| 73e5a38f-2f8b-4cce-91d1-755eb23b78b3 | FIXED | Blood and urine culture criteria (`action-9`, `action-10-order-microbiology`) now recommended as an occult-infection screen with specimen-only arguments (afebrile, WBC 7.2, CRP 2.8, no antibiotic); blocks report "no growth at 48 hours" with `collected_before_antimicrobials` null; stop rule no longer lists them. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | blocker | `patient.clinical_history.past_medical_history[0]` | "Cryptogenic cirrhosis (later found to be Wilson's disease; Child-Pugh B, MELD 14)" gave the agent the answer and an underived score. | FIXED: "Cryptogenic cirrhosis (diagnosed 5 years ago)". |
| D | major | `patient.history_present_illness` | "His ammonia is moderately elevated" (timeline leak, C13). | FIXED: sentence removed. |
| B | minor | `patient.neurological_exam.additional` | "No jaundice" with bilirubin 3.2 mg/dL. | FIXED: "Mild scleral icterus". |
| C | major | `diagnosis.accepted[0]` | "Child-Pugh B" not derivable: computed Child-Pugh C (11: bilirubin 3.2 3, albumin 2.8 2, INR 1.7 2, mild ascites 2, grade II 2), MELD 17, MELD-Na 18 (C10). | FIXED: label "(West Haven grade II) ... cirrhosis (Child-Pugh C, MELD-Na 18)"; "plus acute hyperammonemia" dropped from the label (ammonia neither grades nor confirms HE); score line in key evidence. |
| B | major | `initial_tool_outputs.mri`, `followup_outputs[0]` (old) | The required `analyze_brain_mri` returned a normal template with the line "the finding the lumbar puncture is gated on", contradicting the Wilson MRI filed under `order_advanced_imaging` (C8). | FIXED: one MRI in `initial_tool_outputs.mri` with structured findings: putaminal, caudate and thalamic T2/FLAIR hyperintensity with putaminal T1 hypointensity, midbrain 'face of the giant panda' pattern (now described correctly as tegmental T2 hyperintensity sparing the red nuclei, not "central tegmental tract"), pallidal T1 hyperintensity, mild corticospinal tract T2 change, no restricted diffusion or enhancement. Advanced-imaging follow-up deleted. |
| B | minor | `initial_tool_outputs.ct` | Empty findings; "restricted diffusion" on CT (C8). | FIXED: structured findings (putaminal hypodensity kept per plan, normal otherwise); impression without diffusion. |
| E | minor | `initial_tool_outputs.eeg.findings[1]`, impression | "Triphasic-like ... more complete than typical atypical triphasics" (garbled); en dashes. | FIXED: "Triphasic waves ... with anterior-to-posterior phase lag". |
| B | major | `initial_tool_outputs.labs` | "Exclusion studies" block (magnesium, lactate without values); template TSH 2.1, zinc 82; no potassium (on spironolactone) and no CRP; 24-hour urine copper range "<100" (a diagnostic threshold, not a reference range); summary listed 5 of 12 flagged values (C9). | FIXED: potassium 3.8, magnesium 2.0, lactate 1.4, CRP 2.8, TSH 1.9, zinc 66; urine copper range 15-60 µg/24h; summary and interpretation list every flagged value. |
| A | minor | `action-1-interpret-labs` | 11 named panels demanded. | FIXED: two-alternative core plus `ceruloplasmin`, `copper` (plan Labs+). |
| C | major | `followup_outputs` (Wilson treatment DI, transplant MELD panel, literature initial output) and `action-4-search-medical-literature` | Treatment filed as a drug check (trientine, zinc dosing), a "liver transplant evaluation" lab panel reporting a MELD-Na of 16, literature output echoing the expected evidence (C1, C4). | FIXED: deleted; literature criterion deleted and `initial_tool_outputs.literature_search` null. Chelation and transplant assessment are musts. |
| C | major | paracentesis | Mild ascites on exam but no paracentesis anywhere (C6). | FIXED: new required `action-diagnostic-paracentesis` with a microbiology follow-up: PMN 64, total WBC 180, protein 1.4 g/dL, ascitic albumin 1.3 g/dL (SAAG 1.5), Gram stain negative, no growth at 48 hours. |
| C | minor | `followup_outputs` genetics | p.His1069Gln (the commonest European variant) in an Asian patient; "novel frameshift" with "compound heterozygous" asserted without phase; `quantitative_data` carried an interpretive diagnosis ("ATP7B mutations confirmed ... Wilson's disease gene"). | FIXED: c.2333G>T (p.Arg778Leu), the commonest East Asian variant, plus an exon 13 frameshift, both pathogenic; phase not determined; `test_type` `genetic_panel:wilson`; no quantitative interpretation. Criterion kept recommended. |
| C | major | `action-5-check-drug-interactions` | Required with template expected evidence and no case-specific interaction (C5). | FIXED: optional (plan), alternatives name the chelators, zinc, sertraline, lactulose, rifaximin; output `check_trientine_sertraline_lactulose` placed last: chelator spacing from food, zinc, iron and other medicines; sertraline dose and sodium in cirrhosis; slow chelator escalation; no interaction with lactulose or rifaximin. |
| C | major | `assessment` | Musts: "Lactulose + rifaximin" without target; "Confirm Wilson disease with ... slit-lamp KF rings" although the rings are already documented on slit lamp; "trientine preferred; penicillamine alternative"; no transplant assessment in Child-Pugh C. Prohibitions: generic LP line (no LP in the case); "Avoid copper-containing IV multivitamins until copper status defined" (it is defined). | FIXED: MUST-LACT; rifaximin add-on (episode on lactulose prophylaxis); precipitant must (untreated Wilson disease, no other precipitant found); chelation with trientine or D-penicillamine started low and escalated slowly with hepatology and neurology, zinc maintenance (AASLD Wilson 2022); MUST-TX (Child-Pugh C, MELD-Na 18) weighed against the response to chelation; low-copper diet; family screening starting with the sibling and children, targeted to the two variants. The Leipzig confirmation moved to a key-evidence pearl. Prohibitions: PROHIB-BZD, antipsychotics, sedating opioids (acetaminophen up to 2 g per day), the two prior labels, copper-containing supplements; LP line deleted. |
| B | minor | `differential`, `red_herrings`, `key_clinical_evidence[2]` (old) | "Young patient" and "<40" in a 55-year-old; "Exclude on labs" for metabolic causes; acquired hepatocerebral degeneration (the cirrhotic mimic the pallidal T1 change raises) absent (ruling 7). | FIXED: wording "at any age; late presentations after 40 occur"; metabolic entry cites creatinine 0.9 and TSH 1.9; Wilson entry cites the results; acquired hepatocerebral degeneration added as low. |
| E | minor | criteria, citations, metadata | Rationale = label; free-text citations; "trientine (not penicillamine)" in metadata. | FIXED: one-sentence rationales with keys; metadata difficulty fields updated. |

## Changes, in one paragraph a physician can read before re-reviewing

The patient block no longer says the cirrhosis was "later found to be Wilson's disease" or gives the ammonia; the exam now notes mild scleral icterus (bilirubin 3.2). The policy requires the core labs with ceruloplasmin and copper studies, a diagnostic paracentesis (ascitic PMN 64, no SBP) and the MRI; it recommends blood and urine cultures as an occult-infection screen and ATP7B testing; CT and the drug check are optional. The single MRI report now shows the Wilson pattern (putamina, caudate, thalami, midbrain 'face of the giant panda', pallidal T1), replacing the normal template that contradicted it. The ammonia-trend and trientine-response panel, the treatment "drug check", the transplant MELD panel and the literature search are deleted. The label reads grade II, Child-Pugh C (11 points), MELD-Na 18 (the case said Child-Pugh B). Labs gain potassium, magnesium, lactate and CRP and lose the "Exclusion studies" block. ATP7B shows p.Arg778Leu and an exon 13 frameshift (phase not determined). Musts: lactulose to 2-3 stools with rifaximin added, chelation started low and escalated slowly (trientine or D-penicillamine) then zinc, transplant assessment, low-copper diet, family screening. Prohibitions: sedatives, antipsychotics (Wilson movement disorder), sedating opioids, accepting the old labels, copper supplements.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_decomp_2018]`, `[AASLD_ascites_2021]`, `[AASLD_Wilson_2022]` (Schilsky ML et al., Hepatology 2023;77:1428-1455, the AASLD 2022 practice guidance; the plan asks to verify it: it is the published executive summary of that guidance).
- `accepted[0]` changed under ruling 3 (C10 scores; grade added); ICD codes and synonyms unchanged.

## Open questions for Andrea (judgment calls you could not settle)

- Age 55 for a first diagnosis of neurological Wilson disease is unusual but documented; I kept the age and corrected the "young patient" wording rather than changing demographics.
- The label keeps "Acute hepatic encephalopathy" and lists the Wilson features; the ICD codes stay HE codes (E83.01 Wilson disease is in the differential as the underlying cause). If the benchmark should score Wilson disease as part of the answer, that needs a synonym or label decision centrally.
- DI kept optional per plan; sertraline dosing in Child-Pugh C cirrhosis is a hepatic-dosing point that could justify recommended.
- `fallback_tool_outputs.mri` (normal template) is never served because `initial_tool_outputs.mri` exists; left unchanged.

## Verification

Adversarial check, 23 Oct 2026. Read the log, the diff and the whole final case. Recomputed: Child-Pugh C 11 (bilirubin 3.2 3, albumin 2.8 2, INR 1.7 2, mild ascites 2, grade II 2), MELD 17, MELD-Na 18 (Na 136): agrees with the label, key evidence and the transplant must. All three notes are fixed: the haloperidol boilerplate is gone and an antipsychotic prohibition specific to the Wilson movement disorder replaces it; the ammonia trend follow-up is deleted and the ammonia appears once (78, range 11-51); cultures are recommended with specimen-only arguments and out of the stop rule. Checked the Wilson content: the giant panda pattern description (tegmental T2 hyperintensity sparing the red nuclei and lateral substantia nigra), low ceruloplasmin and total serum copper, urine copper above twice the upper limit, low alkaline phosphatase, p.Arg778Leu in an Asian patient, chelator spacing and early neurological worsening, sertraline dose reduction in hepatic impairment: all correct. No EEG criterion existed before and none is needed (the initial EEG answers an unscored order).

Found and fixed one error: `key_clinical_evidence[5]` gave the ATP7B variants the full 4 Leipzig points, while the genetic report (correctly) says phase is not determined; 4 points require variants on both chromosomes. The pearl now gives the 8 points reached without genetics and says the variants add 4 once shown to be in trans. `perfect_agent.py` and `case_io.py check` clean after the edit.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

- Leak guard (Andrea, 24 Oct 2026: any-query outputs must not repeat any criterion's expected evidence, including their own): `ground_truth.action_criteria[action-5-check-drug-interactions].expected_evidence` reworded as the conclusion a grader checks, in words not shared with the stored `check_drug_interactions` follow-up, whose report text is unchanged; clinical content unchanged.
- `ground_truth.diagnosis.icd_codes` changed from [K72.90, K76.82] to [E83.01]; `accepted[1:]` re-derived from the new `E83.01` entry of `diagnosis_synonyms.yaml` (cases: [HEP-ENC-P04]) with `apply_diagnosis_synonyms.py --prune`: the generic HE labels and codes are gone, the accepted labels require Wilson disease and HE together. Reason: Wilson disease is the missing diagnosis the case is built on, and the generic labels let an answer of "hepatic encephalopathy" alone, or the code K72.90, score full diagnosis credit. `accepted[0]` unchanged.
- `fallback_tool_outputs.mri` set to null: a normal template ("appropriate for age") that is never served, because `initial_tool_outputs.mri` always answers `analyze_brain_mri`; it contradicted the case's MRI.

Checks: `perfect_agent.py` pass; `case_io.py check` schema and synonym guard OK, no test failure names this case; leak guard clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-2-order-ct-scan` rationale: "Optional: a new movement disorder warrants brain imaging, and MRI characterizes the deep grey matter far better than CT." -> "A new movement disorder warrants brain imaging, and MRI characterizes the deep grey matter far better than CT."

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-1-interpret-labs]`.alternatives: was [CBC, CMP, coagulation, ammonia, ceruloplasmin, copper] | [CBC, BMP, LFTs, coagulation, ammonia, ceruloplasmin, copper]; now [CBC, CMP, coagulation, ammonia, ceruloplasmin, copper, CRP] | [CBC, CMP, coagulation, ammonia, ceruloplasmin, copper] | [CBC, BMP, LFTs, coagulation, ammonia, ceruloplasmin, copper].
- Decision: serve: new first alternative (old order kept as an alternative). The label names CRP with the core bloods (infection is the precipitant to exclude) and the evidence reads it; CBC, CMP, coagulation and ammonia did not return the inflammatory panel.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: cognitive_screen}`: MoCA 15/30, below the normal range (26 or above), with impaired attention, executive function, delayed recall and orientation to time; naming preserved. (fallback_tool_outputs.clinical_assessment). Why: GCS 13, disoriented to time with slowed processing: a MoCA of 28/30 with full orientation is impossible.
- `order_specialized_test {test_type: neuropsych_battery}`: Abnormal neuropsychological profile dominated by slowed psychomotor speed and impaired attention and executive function, with a retrieval-type memory deficit ... (fallback_tool_outputs.specialized_test). Why: disoriented to time with slowed processing: a battery normal in every domain is impossible.
- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 50, ECOG 3. Requires considerable assistance and frequent supervision; capable of only limited self-care. (followup_outputs[request_performance_status]). Why: Karnofsky 100 / ECOG 0 contradicts an inpatient confused, bed- or chair-bound patient.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: Markedly slowed, wide-based gait with dystonic posturing and truncal ataxia: Timed Up and Go 24.8 s, walk speed 0.58 m/s; tandem gait not possible. (followup_outputs[request_gait_and_balance_timed]). Why: stored exam gait: dystonic, unsteady.
- `order_specialized_test {test_type: speech_language_evaluation}`: Abnormal speech and language evaluation: mild dysarthria with slow, effortful articulation; slowed output with word-finding difficulty; follows two-step ... (followup_outputs[request_speech_language_evaluation]). Why: stored exam speech: mild dysarthria with slow, effortful articulation; slowed output with word-finding difficulty.
- `analyze_eeg {eeg_type: continuous_icu}`: Continuous EEG monitoring over 24 hours: 1. Generalized theta-delta slowing at 4-6 Hz with a moderately disorganized background. 2. Intermittent ... (fallback_tool_outputs.eeg). Why: the stored routine EEG is abnormal; a prolonged recording cannot show a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: 48-hour ambulatory EEG: 1. Generalized theta-delta slowing at 4-6 Hz with a moderately disorganized background. 2. Intermittent fronto-central triphasic waves ... (followup_outputs[request_ambulatory]). Why: the stored routine EEG is abnormal; a 48-hour recording cannot be normal.
- `order_advanced_imaging {modality: MR_spectroscopy}`: Abnormal MR spectroscopy: reduction of myo-inositol (mI/Cr 0.28) and choline (Cho/Cr 0.58) with an increased glutamine-glutamate (Glx) peak; NAA preserved; no ... (fallback_tool_outputs.advanced_imaging). Why: characteristic test of the condition: reduced myo-inositol and choline with raised Glx.
- `order_body_imaging {study: pelvis_abdomen_ultrasound}`: Abdominal and pelvic ultrasound with Doppler: 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal vein. 4. Splenomegaly (13.6 cm). 5. ... (fallback_tool_outputs.body_imaging). Why: cirrhosis with small-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_CT}`: Contrast-enhanced CT of the abdomen and pelvis (arterial and portal venous phases): 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal ... (followup_outputs[request_pelvis_abdomen_ct]). Why: cirrhosis with small-volume ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_MRI}`: Contrast-enhanced MRI of the abdomen and pelvis: 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal vein. 4. Splenomegaly (13.6 cm). 5. ... (followup_outputs[request_pelvis_abdomen_mri]). Why: cirrhosis with small-volume ascites: the library reports a normal liver and spleen.
- `interpret_labs {panels: [peripheral_smear]}`: Normocytic, normochromic red cells with occasional target cells; normal white cell morphology; platelets reduced in number, of normal morphology, without ... (fallback_tool_outputs.labs[peripheral_smear]). Why: stored CBC: platelets 112: 'adequate platelets' contradicts it.

Checks: `perfect_agent.py` pass; `test_case_guards.py -k HEP-ENC-P04` pass; the map verifier serves every listed term from the case; the snapshot of the 322 previously case-answered orders is unchanged.

Lab prose (25 Oct 2026, same pass): the fallback-labs interpretation now gives the smear as one sentence headed `Peripheral blood smear:` (commas, no semicolons), so an order for another panel no longer receives smear fragments; the smear rows are unchanged.
