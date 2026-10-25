# NMDAR-ENC-P07
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for NMDAR-ENC) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: condition not reviewed | - | - |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A | blocker | `action-2-analyze-csf`, `action-4-interpret-labs`, `action-1-analyze-brain-mri`, `action-5-order-body-imaging`, `action-7-search-medical-literature`, `action-8-check-drug-interactions` | Non-schema keys (`basic`, `drug`, `screen_for`), `protocol: standard`, exact `query`, 11-panel list (C1). | FIXED: plan 3.2 arguments; labs alternatives with `beta-hCG` (woman of 25); CSF with oligoclonal bands or IgG index; EEG routine, video or continuous; DDI and literature `{}`. |
| B | blocker | `initial_tool_outputs.csf.special_tests` | CSF anti-NMDAR "Pending" in two keys while the labs gave the CSF titer 1:32; culture pending (C4). | FIXED: one key `NMDAR_antibodies` = "Positive, titer 1:32 (cell-based assay, IgG anti-GluN1; reference laboratory, resulted day 6)"; `anti_NMDAR_antibody` deleted; culture final; glucose ratio names the serum glucose (94 mg/dL); RBC unit. |
| B/D | major | `initial_tool_outputs.labs.panels` | CSF titer in the labs, serum titer twice, "Exclusion studies" leak, empty inflammatory markers, anti-TPO twice, CK under Toxicology, quetiapine level "not detected" while she takes 200 mg (C4, C5). | FIXED: plan panels (CBC, BMP, coagulation, CRP and ESR with values, thyroid function with free T4, thyroid antibodies, serum anti-GluN1 1:80 once, neuronal-surface panel, onconeural panel, connective tissue screen with ANA, anti-dsDNA, anti-Sm, C3 and C4, HIV, toxicology, lamotrigine level, beta-hCG negative, CK under Other); quetiapine level deleted; plain recital. |
| B | major | `patient.clinical_history.medications` | Quetiapine listed at 100 mg while the HPI says it was raised to 200 mg; risperidone 1 mg missing (C17). | FIXED: quetiapine 200 mg at bedtime; risperidone 1 mg added; indications in the prescriber's words. |
| B | minor | `patient.clinical_history.social_history.illicit_drugs`, labs summary | Urine THC positive "(residual)" with last use a month ago in an occasional user, which a urine screen would not detect. | FIXED: social history gives use 3 days before presentation (per her mother); "(residual)" removed. |
| B | minor | `patient.neurological_exam.motor` | NMS is a named red herring but the exam did not state rigidity either way. | FIXED: "Tone normal; no rigidity" (the existing exam already said tone normal). |
| D | minor | `initial_tool_outputs.mri.impression` | "Clinical and CSF correlation essential" (C13). | FIXED: radiology impression; signal characteristics and negatives filled. |
| D | minor | `initial_tool_outputs.eeg` | Limitation inside the impression, prose impression, empty background. | FIXED: artifact moved to `limitations`; "This is an ABNORMAL EEG due to:" numbered; background filled. |
| B/D | major | cEEG follow-up `request_continuous_eeg` | Empty background, one-line impression (C7). | FIXED: background; extreme delta brush from hour 12, two right temporal subclinical seizures (4-6 Hz evolving theta) and slowing; template impression. |
| D | major | `initial_tool_outputs.body_imaging` | Lab-template impression; "complex mass with solid-cystic components" without teratoma features (C12). | FIXED: Rokitansky nodule with shadowing and fat-fluid level, no vascularity; impression "consistent with a mature cystic teratoma (dermoid)"; uterus and abdomen described. |
| C | major | DDI follow-up `request_drug_interactions_check`, criterion `action-8-check-drug-interactions` | Only DDI output was a follow-up reachable by trigger alone, with a doubtful claim (steroids raise lamotrigine clearance) and dashes; criterion recommended with non-schema arguments (C10). | FIXED: content moved to `initial_tool_outputs.drug_interactions.general` in report voice and the follow-up deleted: valproate doubles lamotrigine (halve the dose), no lamotrigine gaps (re-titration and rash risk), estrogen contraceptives lower lamotrigine, quetiapine with risperidone (QTc, sedation, EPS/NMS), sedation with lorazepam, steroid hypokalemia and mood elevation, hypokalemia adds to QTc; D2 class warning, valproate, HBV screen, cyclophosphamide fertility. The steroid-lamotrigine clearance claim was dropped. Criterion `required` (ruling 6, C10), `{}`, in the stop rule. |
| B | major | `fallback_tool_outputs.ecg`, `.cardiac_monitoring` | Fallback ECG at 88 bpm and Holter (49-113, average 78) against HR 118 (C14). | FIXED: fallback ECG null; `initial_tool_outputs.ecg` sinus tachycardia 118, QTc 446 ms; telemetry fallback (92-132, average 112). |
| C | major | `fallback_tool_outputs.advanced_imaging`, `.specialized_test` | Catch-all fallbacks (C14). | FIXED: null; `fallback_tool_kinds` updated; fallback DDI `proposed` "". |
| D | major | `initial_tool_outputs.literature_search` | Placeholder (C3). | FIXED: canonical literature plus Schmitt 2012; literature optional, `{}`, last. |
| C | major | `assessment.required_recommendations` | Template musts, including "levetiracetam or valproate" in a woman on lamotrigine (C9). | FIXED: M1, M2, left teratoma removal, M4 with both valproate clauses and "continue lamotrigine without interruption", M5, M6 ICU (labile blood pressure 118-142 with diaphoresis meets the rule's trigger; seizures on cEEG), M7 with fertility preservation, M8 lorazepam first with "stop risperidone and taper quetiapine, monitor CK and temperature", M10. |
| C/E | minor | `assessment.prohibited_recommendations` | Template P1 and P3 ("in a young patient"). | FIXED: canonical P1-P5. |
| C | major | `ground_truth.differential` | Templated likelihoods; no bipolar relapse (C8). | FIXED: all low with this case's evidence: HSV, other antibody-mediated encephalitis, bipolar disorder relapse (F31.9), drug-related (cannabis psychosis, NMS with tone, CK and temperature values), neuropsychiatric SLE (ANA 1:80, aunt with SLE). |
| C | major | `ground_truth.key_clinical_evidence` | Template with wrong claims (C15). | FIXED: six case-specific bullets. |
| C | minor | `ground_truth.red_herrings` | "Previously well young adult" in a woman with bipolar disorder; hyponatremia template; the variant's NMS and cannabis confounders not listed (C15). | FIXED: the psychiatric red herring is now the known bipolar disorder; canonical hyponatremia; THC screen, antipsychotic exposure with CK 198, and ANA 1:80 added. |
| C | minor | criteria `rationale`, `citations`, `expected_evidence` | C16. | FIXED. |
| A | minor | order, `sequence_constraints`, `stop_rule` | C6, C18. | FIXED: labs, MRI, CSF, EEG, pelvic US, cEEG, DDI, literature; soft MRI-before-CSF; six required ids (DDI included), max 2. |
| B | minor | `metadata.difficulty_rationale`, `.difficulty_variant_description` | "2 red herrings", "severe multistage syndrome". | FIXED. |
| E | minor | whole case | American-spelled case; canonical texts British. | FIXED: new text in the case's spelling. |

## Changes, in one paragraph a physician can read before re-reviewing
NMDAR-ENC-P07 is a 25-year-old woman with bipolar II disorder whose episode became atypical: echolalia, stereotypies, orofacial movements, chorea and autonomic lability. Her medication list now matches the HPI: lamotrigine, quetiapine 200 mg and the newly added risperidone. The CSF reports the final result: anti-GluN1 positive at 1:32, with a near-normal routine CSF. Serum (1:80) is the only antibody entry in the rebuilt labs, which keep a low-titer ANA with negative lupus serology and add a negative beta-hCG. The cannabis screen now fits recent use three days earlier. The pelvic ultrasound describes a 4.1 cm left mature cystic teratoma. The continuous EEG shows extreme delta brush and two subclinical right temporal seizures. An ECG at 118 bpm replaces the fallback at 88 bpm. The drug-interaction check is now required and is stored as an initial report. It covers valproate raising lamotrigine, keeping lamotrigine without gaps, and the two antipsychotics together. Treatment follows the canonical musts with ICU care. Antiseizure treatment avoids valproate and keeps lamotrigine. Lorazepam comes first; risperidone is stopped, quetiapine tapered, and CK and temperature monitored. Bipolar relapse, cannabis psychosis, NMS and neuropsychiatric lupus are low-likelihood differentials and red herrings.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys used and not yet in the allow-list: `[Gresa-Arribas_2014]`, `[Herman_2015]` (plan CENTRAL 1).
- The plan's criterion id `cEEG-escalation` fails the lowercase id pattern; the existing id `action-6-analyze-eeg` was kept.

## Open questions for Andrea (judgment calls you could not settle)
None. Two calls are logged here. First, the cannabis timing: the plan offered adding cannabis to the history or making the screen negative. The history already had it, but "last used 1 month ago" in an occasional user cannot give a positive urine screen, so I moved last use to 3 days before presentation and kept the variant's cannabis red herring. Second, the "quetiapine not detected" level contradicted the dose and was not a standard test, so I deleted it rather than invent non-adherence.

## Verification
Adversarial verifier, 24 Oct 2026. Checked against the plan (sections 1-4 and the per-case bullet) and ROUND_POLICY: every own-finding row against the file; criterion tiers, minimal arguments, order and ids; soft MRI-before-CSF constraint and stop rule (five required ids, max 2); CSF report carries the only CSF titre and the labs only the serum titre; musts against allergies, medications and level-of-care rule; prohibitions P1-P5; differential and key evidence against the final reports; red-herring field paths; fallbacks; a word-level diff of every changed string against HEAD (to catch accidental edits in correct prose); citation format and new-text dashes. No reviewer notes exist for NMDAR-ENC, so the notes table is complete. `perfect_agent.py -v` passes and `case_io.py check` reports no failure naming the case (case guards included).

Found and changed:
- `action-8-check-drug-interactions.citations` cited `[Graus_2016]` (diagnostic criteria) for drug interactions, a key cited for a claim it does not make (plan 1.1). FIXED: `[Lejuste_2016]` (antipsychotic intolerance, the interaction that drives the plan).
- `metadata.fallback_tool_kinds.cardiac_monitoring` FIXED to "sinus_tachycardia".
- Confirmed: medication list (quetiapine 200 mg, risperidone 1 mg) matches the HPI; DDI required per C10 and in the stop rule; lamotrigine clauses in M4; NMS argued against with stored tone, CK and temperature; cannabis timing consistent with a positive screen; ANA red herring path valid.

## Condition audit (24 Oct 2026)

Condition auditor, after the workers and verifiers. Uniformity checks over all 30 cases; changes made here through `case_io` (all re-checked: `perfect_agent.py` 30/30, `case_io.py check` and the case guards clean):
- `ground_truth.stop_rule.required_before_assessment` (A, minor): it listed the required drug-interaction criterion as a sixth id, while plan 3.5 sets the five diagnostic ids and RP02 (the other case with a required DDI) follows it. The stop rule names the evidence needed before the diagnosis is submitted; the DDI is a pre-treatment check whose omission is already penalised by required coverage. Removed `action-8-check-drug-interactions` from the stop rule; the criterion stays `required`.

## Close-out (24 Oct 2026)

- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions autoimmune_encephalitis_nmdar`): the generic G04.81 labels "autoimmune encephalitis", "antibody mediated encephalitis" and "autoimmune limbic encephalitis" and code G04.90 are no longer accepted, because every token of the first two occurs in "anti-LGI1 autoimmune encephalitis" or "seronegative autoimmune encephalitis" (alternatives the work-up excludes), limbic encephalitis is a different syndrome (Graus 2016) and G04.90 is unspecified encephalitis. Added "glun1 encephalitis", "nr1 encephalitis" and code G04.8. `accepted[0]` and `icd_codes[0]` unchanged. Decisions: `plans/NMDAR-ENC-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-4-interpret-labs]`.alternatives: was [CBC, CMP, TSH, anti_TPO, HIV, NMDAR_IgG_cell_based, beta-hCG] | [CBC, CMP, thyroid, anti_TPO, HIV, NMDAR_IgG_cell_based, beta-hCG]; now [CBC, CMP, TSH, anti_TPO, HIV, NMDAR_IgG_cell_based, beta-hCG, CK, ANA, tox_screen] | [CBC, CMP, TSH, anti_TPO, HIV, NMDAR_IgG_cell_based, beta-hCG] | [CBC, CMP, thyroid, anti_TPO, HIV, NMDAR_IgG_cell_based, beta-hCG].
- Decision: serve: new first alternative (old order kept as an alternative). The rationale screens toxic and lupus-related causes: a must monitors CK, the NMS and lupus differentials and two red herrings rely on CK 198 and ANA 1:80, and the evidence reads the urine THC.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although this case contradicts it (diagnosis, history, medications or a stored finding) now get a case-specific report; every other off-pathway order still gets the library normal. No tier, criterion, diagnosis or existing output changed.

- `order_advanced_imaging modality=FDG_PET` -> `followup_outputs[order_fdg_pet]`: brain FDG-PET: frontotemporal hypermetabolism with parieto-occipital hypometabolism, distributed as the stored MRI and EEG.
- `analyze_eeg eeg_type=ambulatory` -> `followup_outputs[order_ambulatory]`: ambulatory EEG mirroring the stored continuous EEG (no video).
- `perform_clinical_assessment assessment_type=cognitive_screen` -> `followup_outputs[order_cognitive_screen]`: baseline cognitive screen as documented in the mental status examination.
- `perform_clinical_assessment assessment_type=cognitive_screen timing=post_intervention` -> `followup_outputs[order_cognitive_screen_post_intervention]`: repeat screen during the admission: persisting impairment.
- `order_specialized_test test_type=neuropsych_battery` -> `followup_outputs[order_neuropsych_battery]`: neuropsychological battery not completable or impaired in the acute encephalopathy.
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[order_performance_status]`: performance status KPS 30, ECOG 4 for the documented dependency.
- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `followup_outputs[order_gait_and_balance_timed]`: timed gait not testable or impaired, as on the examination.
- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: speech and language evaluation reflecting the documented speech disturbance.
- `order_body_imaging study=pelvis_abdomen_CT` -> `followup_outputs[order_pelvis_abdomen_ct]`: pelvic CT shows the teratoma seen on the stored ultrasound.
- `order_body_imaging study=pelvis_abdomen_MRI` -> `followup_outputs[order_pelvis_abdomen_mri]`: pelvic MRI shows the teratoma seen on the stored ultrasound.
- `order_body_imaging study=chest_abdomen_pelvis_CT` -> `followup_outputs[order_chest_abdomen_pelvis_ct]`: CT chest/abdomen/pelvis shows the teratoma seen on the stored ultrasound.
- `order_advanced_imaging modality=whole_body_FDG_PET` -> `followup_outputs[order_whole_body_fdg_pet]`: whole-body PET/CT: non-avid fat-containing adnexal lesion.
- `obtain_tissue_diagnosis procedure=resection` -> `followup_outputs[order_resection]`: resection pathology: mature teratoma with neuroglial tissue.
- `labs:prolactin` -> fallback labs panel `Prolactin`: prolactin elevated on risperidone.
- `labs:lithium_level` -> fallback labs panel `Lithium`: lithium not detected (not on lithium).
- `labs:valproate_level` -> fallback labs panel `Antiseizure medication levels`: antiseizure drug levels: only the drugs the patient takes.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k NMDAR-ENC` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
