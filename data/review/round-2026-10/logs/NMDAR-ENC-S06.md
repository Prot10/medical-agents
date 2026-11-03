# NMDAR-ENC-S06
Reviewer status: R1 not reviewed, R2 not reviewed (no `notes/NMDAR-ENC.md`: condition not reviewed this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | None: condition not reviewed. All changes below are the plan's class fixes (plan section 2, S06 entry) and my own findings. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria` | C1: non-schema `basic` and `screen_for`, exact literature `query`, `protocol: standard`, 11-panel labs list. | FIXED: plan 3.2 arguments. |
| D | blocker | `followup_outputs` literature | C3: placeholder literature output; leak guard failed. | FIXED: canonical literature plus Schmitt 2012. Guard passes. |
| D/C | major | `followup_outputs` DDI (`request_drug_interactions`) | The output listed a proposed regimen with "No significant interactions" and a management line ("Blood pressure management required..."). She takes no medicines, and the real issues (steroids with K 3.2, aciclovir hydration against fluid restriction, IVIG and measured sodium) were missing. | FIXED: rewritten in report voice with those points, the D2 class warning, HBV before rituximab and the codeine intolerance; trigger renamed `request_check_drug_interactions` for consistency (matching is by tool). |
| C | major | literature and DDI criteria | C2, C10: both `recommended`. | FIXED: both `optional`, `{}`; literature last. |
| B | blocker | `initial_tool_outputs.csf`, `.labs` | C4: CSF antibody in two CSF keys (`NMDAR_antibodies`, `anti_NMDAR_antibody`) and in the labs panel `Anti-Neuronal_Autoantibody_Confirmation`. | FIXED: one CSF key with the final result (1:64), once in `interpretation`; CSF value removed from labs. |
| C | major | `initial_tool_outputs.csf.glucose`, `.glucose_ratio` | CSF glucose 48 mg/dL with ratio 0.44: a low ratio is not a feature of anti-NMDAR encephalitis and points to bacterial, mycobacterial, fungal or carcinomatous meningitis (plan 1.2). | FIXED: glucose 66 mg/dL, ratio 0.61 with serum 108. Culture "Pending" becomes "No growth at 48 hours"; IgG index "(markedly elevated)" becomes the reference statement; cell differential in `cell_count`. |
| B | minor | `labs.panels.Serum anti-GluN1 IgG (cell-based assay)` | Serum 1:640 is off the CSF doubling series (1:64). | FIXED: serum 1:512. |
| D/B | major | `initial_tool_outputs.labs` | C5: leaky `Exclusion studies`; `Reviewed inflammatory markers` with "Within reference range" instead of values; duplicate anti-TPO; a BMP without chloride, bicarbonate, BUN or calcium; no hepatic panel, free T4, beta-hCG, CK, AMPA antibody; summary with interpretive parentheticals ("severe SIADH", "post-ictal"). Na 126 without osmolality. | FIXED: canonical panels with values. New values: Hct 40.1, Cl 92, HCO3 24, BUN 7, Ca 9.1, liver panel and albumin normal, CRP 3 mg/L, ESR 12, free T4 1.1, AMPA negative, onconeural panel, beta-hCG negative, CK 288. Also a `Sodium work-up` panel: serum osmolality 262, urine osmolality 410, urine sodium 48, random cortisol 21.4. Plain recital. |
| C | major | `action_criteria` (new `siadh-workup`) | Na 126 (moderate) needs an SIADH work-up (plan 3.2). | FIXED: recommended `siadh-workup`, `{panels: [serum_osmolality, urine_osmolality]}`, answered by the initial labs report (the perfect-agent warning about the shared report is expected). |
| B/D | major | `initial_tool_outputs.mri` | Terse report; the impression named only the "subtle frontal subcortical changes" and omitted the bilateral medial temporal signal (impression omitting its key finding). | FIXED: full findings (T1/T2/FLAIR/DWI/contrast), observations (no haemorrhage on SWI, no mass effect) and an impression that names both findings. |
| B/D | minor | `initial_tool_outputs.eeg` | Empty background, no artifacts, impression "Severely abnormal EEG. One electrographic seizure captured" without the extreme delta brush. | FIXED: background, muscle artifact, seizure correlate; ABNORMAL numbered impression; limitations "Continuous EEG monitoring recommended." |
| D/C | major | `fallback_tool_outputs.ecg`, `.advanced_imaging`, `.specialized_test`, `.cardiac_monitoring` | C14: normal ECG at 85 bpm against HR 128; catch-all PET and neuropsychology fallbacks; Holter average 73. | FIXED: initial ECG sinus tachycardia 126 bpm, normal intervals; ECG fallback, PET and specialized fallbacks null; telemetry fallback 104-136 bpm. CT head fallback kept. `fallback_tool_kinds` updated. |
| D/C | major | `initial_tool_outputs.body_imaging` | C12: a single line "4.5 x 3.8 cm complex cystic mass" and a lab-template impression; nothing characteristic of a teratoma although the musts plan its removal. | FIXED: full report: Rokitansky nodule with shadowing, echogenic lines and dots, fat-fluid level, no vascularity; right ovary and uterus normal; radiology impression. |
| C | major | `followup_outputs`, criteria | C7: cEEG must without a cEEG follow-up. | FIXED: 24 h cEEG (four left temporal seizures, extreme delta brush); `ceeg-escalation` recommended. |
| C | major | order, `sequence_constraints`, `stop_rule` | C6, C18. | FIXED: labs, MRI, CSF, EEG, tumour, cEEG, SIADH, DDI, literature; follow-ups cEEG, DDI, literature; soft MRI before CSF; five required ids, max 2. |
| C | major | `ground_truth.differential` | C8 template. | FIXED: all `low` with this case's evidence. |
| C | major | `ground_truth.assessment` | C9 template; hyponatraemia and hypokalaemia not managed. | FIXED: M1, M2, M3 left teratoma removal, M4 without valproate, M5, M6 ICU (HR 128, BP 162/98 from a 110/70 baseline, diaphoresis, fever, seizures, hyponatraemia; the plan's ruling), M7, M8, M9 (SIADH: fluid restriction, hypertonic saline if seizures recur, at most 10 mmol/L in 24 h, aciclovir in isotonic saline), potassium replacement, M10. Canonical P1, P3. |
| C | major | `ground_truth.key_clinical_evidence` | C15 template. | FIXED: seven case-specific bullets, including the SIADH bullet. |
| B/C | minor | `ground_truth.red_herrings` | Prodrome data_point "URI, fever, cough" (HPI: fever, headache, fatigue); "Mild hyponatremia (sodium 126)" is moderate. | FIXED: data_points from the HPI and labs; canonical prodrome and hyponatraemia interpretations; psychiatric red herring names the urgent-care "drug-induced psychosis" label. |
| B | major | `patient.history_present_illness`, `patient.chief_complaint` | Timeline did not add up: "16-day history" but a 5-day prodrome, a 3-4 day interval and behaviour change starting 12 days ago (about 21 days). | FIXED: "three-week history"; chief complaint "for 12 days after a flu-like illness". |
| C/B | minor | rationales, citations, `metadata.difficulty_rationale` | C16; "6 required tools". | FIXED; 5 required. |

## Changes, in one paragraph a physician can read before re-reviewing
NMDAR-ENC-S06 is a 27-year-old woman with paranoia and hallucinations, echolalia, convulsive seizures, orofacial dyskinesias and dysautonomia, CSF anti-GluN1 1:64 (serum now 1:512) and a 4.5 cm left ovarian teratoma that now has characteristic ultrasound features; label unchanged. The timeline now works (three weeks overall, 12 days of behaviour change). The CSF glucose ratio was 0.44, which points away from the diagnosis; it is now 0.61. The labs are complete and carry an SIADH work-up for the sodium of 126 (serum osmolality 262, urine osmolality 410, urine sodium 48, cortisol normal), scored by a new recommended criterion. The MRI and EEG reports are now full reports whose impressions name the medial temporal signal and the extreme delta brush. An initial ECG (sinus tachycardia 126) replaces a contradictory normal fallback. A 24-hour cEEG shows four left temporal seizures. Musts add ICU care, SIADH management within the 10 mmol/L limit with aciclovir in isotonic saline, and potassium replacement. DDI and literature are optional.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: keys used `[Gresa-Arribas_2014]`, `[Herman_2015]`, `[Abboud_2021]`, `[Lejuste_2016]`, `[Spasovski_2014]`.
- To the lead: criterion ids `ceeg-escalation` (the plan's `cEEG-escalation` fails the schema) and `siadh-workup` (the plan named none).

## Open questions for Andrea (judgment calls you could not settle)
None. I decided these myself:
- ICU level of care follows the plan's S06 ruling. Strictly, HR 128 is under the plan's 130 threshold, but she has hypertension 50 mmHg above baseline with diaphoresis, fever, recurrent seizures and moderate hyponatraemia.
- The SIADH values (serum osmolality 262, urine osmolality 410, urine sodium 48, cortisol 21.4) are new and chosen to be consistent with sodium 126 and euvolaemia.

## Verification
Checked against the plan (sections 1.2, 2, 3, 4) and the final case file: every own-finding row of the log against the file; criteria order, tiers and minimal arguments (plan 3.2); stop rule (five required ids, max 2) and the soft MRI-before-CSF constraint; one CSF anti-GluN1 key with titre on the same doubling series as serum and no CSF entry in the labs; labs panels, `is_abnormal` flags and plain-recital summaries; laterality across exam, MRI, EEG and cEEG; allergies and medication list against musts and DDI output; musts against prohibitions and avoided actions; differential likelihoods against the results; red-herring data_points against the HPI; literature and DDI outputs for leakage (case guards pass). No reviewer notes exist for this condition, so there is no note id to account for.
Arithmetic checked: calculated serum osmolality (2 x Na + glucose/18 + BUN/2.8) matches the stored value; anion gap normal; CSF glucose ratio matches CSF/serum glucose; the SIADH values (low serum osmolality, urine osmolality above 100, urine sodium above 30, normal TSH, free T4 and cortisol) fit the sodium.
Found and changed:
- `initial_tool_outputs.eeg.findings[1]`: the structured fields were swapped (`frequency` held the rhythm, `morphology` held the seizure count and duration), against the convention of the other reports in this batch. Swapped back; morphology now "Evolving rhythmic ... theta".
- `initial_tool_outputs.labs.panels.Sodium work-up` urine sodium `reference_range`: "random; >30 with low serum osmolality is inappropriate natriuresis" is interpretation inside a lab report (kind 1 leakage toward the SIADH criterion). Now "No fixed reference range (random sample)".
`perfect_agent.py -v` and `case_io.py check` clean after the edits.
Checked and kept: ICU level of care (the plan's rule includes labile BP with diaphoresis; BP 162/98 against a 110/70 baseline with fever and seizures).

## Condition audit (24 Oct 2026)

Condition auditor, after the workers and verifiers. Uniformity checks over all 30 cases; changes made here through `case_io` (all re-checked: `perfect_agent.py` 30/30, `case_io.py check` and the case guards clean):
- `ground_truth.assessment.prohibited_recommendations[1]` and `[3]` (B/E, minor): the canonical P2 and P4 texts still carried an em dash before "antibody turnaround" and before "exclude mass effect", and an en dash in "1-2 weeks", while 18 other cases already had the dash-free canonical wording. Now "...high: antibody turnaround can take 1-2 weeks..." and "...new seizures: exclude mass effect first." Meaning unchanged.

## Close-out (24 Oct 2026)

- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions autoimmune_encephalitis_nmdar`): the generic G04.81 labels "autoimmune encephalitis", "antibody mediated encephalitis" and "autoimmune limbic encephalitis" and code G04.90 are no longer accepted, because every token of the first two occurs in "anti-LGI1 autoimmune encephalitis" or "seronegative autoimmune encephalitis" (alternatives the work-up excludes), limbic encephalitis is a different syndrome (Graus 2016) and G04.90 is unspecified encephalitis. Added "glun1 encephalitis", "nr1 encephalitis" and code G04.8. `accepted[0]` and `icd_codes[0]` unchanged. Decisions: `plans/NMDAR-ENC-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

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
- `labs:AED_levels` -> fallback labs panel `Antiseizure medication levels`: antiseizure drug levels: none detected (no antiseizure drug prescribed).
- `labs:valproate_level` -> fallback labs panel `Antiseizure medication levels`: antiseizure drug levels: none detected (no antiseizure drug prescribed).

Checks: `perfect_agent.py` ok; `test_case_guards.py -k NMDAR-ENC` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
