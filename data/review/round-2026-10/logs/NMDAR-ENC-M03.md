# NMDAR-ENC-M03
Reviewer status: none (condition not reviewed in this round; July 2026 tool review only) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: condition not reviewed | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-2-analyze-csf]` | Non-schema `basic` key: the required CSF criterion was unreachable (C1). | FIXED: `special_tests` alternatives per plan 3.2. |
| A | major | `action_criteria[action-1/4/5/7/8]` | `protocol: standard`, eleven-panel list, `contrast: false`, exact `query`, `screen_for` (C1). | FIXED: minimal arguments per plan 3.2 (labs with beta-hCG, TSH/thyroid alternatives). |
| D | blocker | `initial_tool_outputs.literature_search`, `.drug_interactions` | Placeholder literature ("Confirms diagnostic criteria...") and a DDI block repeating the criterion's expected evidence (C3; guard failing). | FIXED: canonical literature output; DDI in report voice from her medicines (COC with IVIG thrombosis risk and with steroids, metformin hyperglycemia, albuterol hypokalemia, lorazepam sedation, acyclovir), tetracycline allergy, D2 class warning, HBV screening. Guard passes. |
| C | major | `action_criteria[action-7-search...]`, `[action-8-check...]` | Literature and DDI `recommended` (rulings 5, 6). | FIXED: both `optional`, last. |
| B | blocker | `initial_tool_outputs.csf.special_tests`, `.labs.panels` | CSF antibody "Pending" (two keys) while labs gave the CSF titer 1:160 (C4). | FIXED: `NMDAR_antibodies` "Positive, titer 1:160 (... resulted day 6)"; result in the interpretation; CSF entries removed from labs; bacterial culture "No growth at 48 hours" (was "Pending (no growth at 24 hours)" in a report finalized on day 6). |
| B | minor | `initial_tool_outputs.csf` (C17) | Cell count, IgG index and OCB copied from M01 (12 cells, 0.72, "2 faint bands"); glucose ratio 0.61 did not compute (56.2/102 = 0.55) and the lab serum glucose is 109. | FIXED: WBC 24 cells/uL (82% lymphocytes), IgG index 0.75, one CSF-restricted band; CSF glucose 66.5 mg/dL with ratio 0.61 against serum 109 (a ratio near 0.5 is not a feature of the disease, plan 1.2). |
| C | major | `initial_tool_outputs.body_imaging`, new `followup_outputs[1]`, new criterion `pelvic-mri-characterization` | The ultrasound lesion is equivocal (dermoid or hemorrhagic cyst), so whether a teratoma must be removed was undecidable; impression in lab template. | FIXED: ultrasound impression indeterminate with a pelvic MRI recommendation; recommended pelvic MRI criterion (`{study: pelvis_abdomen_MRI}`) answered by a new report: 1.2 cm left lesion with macroscopic fat, calcified focus, no enhancing solid tissue, consistent with a mature cystic teratoma; soft constraint ultrasound before MRI. (Plan id `pelvic-MRI-characterisation` is not a valid lowercase id; American spelling kept.) |
| B | minor | `patient.clinical_history.social_history.occupation` | "nurse" while the HPI describes her teaching position, classroom and lesson (template carry-over). | FIXED: "primary school teacher". |
| B | minor | `patient.clinical_history.medications` | Lorazepam 0.5 mg as needed (HPI, benzodiazepine-positive screen) missing. | FIXED: added. |
| B | minor | `initial_tool_outputs.eeg.findings[1]`, `.impression` | "Possible electrographic seizure" in findings, definite in the impression; prose impression. | FIXED: electroclinical seizure with behavioral arrest; numbered impression, "No extreme delta brush". |
| B | minor | `followup_outputs[0].output.impression` (cEEG) | Impression called the pattern "extreme delta brush" while the finding says "suggestive of but not fully developed"; GPD correlation listed prion disease and metabolic causes (differential in a report). | FIXED: impression "suggestive of but not fully developed extreme delta brush"; correlation emptied. |
| D | minor | `initial_tool_outputs.mri.impression` | "No evidence of hemorrhagic encephalitis to suggest HSV" (reasoning). | FIXED: numbered modality-pure impression with one hedged sentence. |
| B | minor | MRI right medial temporal vs EEG left temporal seizures | Laterality differs between MRI and EEG. | FLAGGED, kept: anti-NMDAR encephalitis is a diffuse process and MRI signal need not match the EEG focus; the left facial droop fits the right-sided MRI signal. Not a flip of the same finding. |
| B | major | `initial_tool_outputs.labs` | Duplicates, "Exclusion studies", "Reviewed inflammatory markers", CSF entries (C5). | FIXED: panels rebuilt per C5 (beta-hCG negative, onconeural, neuronal-surface, HIV, ANA; ammonia kept in Other). Values unchanged. |
| C | major | `fallback_tool_outputs` | Fallback ECG rate 68 and Holter average 70 contradicted HR 88-118 (C14); FDG-PET and neuropsychology fallbacks; `proposed` text. | FIXED: `initial_tool_outputs.ecg` sinus tachycardia 104; telemetry fallback to 118; advanced imaging, specialized test and ECG fallbacks null; `proposed` emptied; `fallback_tool_kinds` updated. |
| C | major | `action_criteria` order, `sequence_constraints`, `stop_rule` | C6, C18. | FIXED: labs, MRI, CSF, EEG, ultrasound, cEEG, pelvic MRI, DDI, literature; soft MRI-before-CSF and ultrasound-before-pelvic-MRI; stop rule five ids, max 2. |
| E | minor | `action_criteria[*]` | Rationale = label, citation twins, generic evidence (C16). | FIXED. |
| C | major | `assessment.required_recommendations` | Template musts (C9). | FIXED: M1, M2, M3 removal of the left ovarian teratoma, M4 without valproate, M5, M6 ward (alert, HR to 118: no ICU feature of the plan rule), M7, M8 lorazepam, M10 with gynecology. |
| C | minor | `assessment.prohibited_recommendations` | "young patient", dashes. | FIXED: canonical P1-P5. |
| C | major | `ground_truth.differential` | Template, not updated (C8). | FIXED: all `low` with case data. |
| C | major | `ground_truth.key_clinical_evidence` | Template with wrong claims (C15). | FIXED: six case-specific bullets. |
| B | minor | `ground_truth.red_herrings` | Template interpretations ("CK typically >1000", "Mild hyponatremia is a recognized SIADH complication"). | FIXED per C15; "Mild hyponatremia (131)" is correctly graded and kept; "previously well" is correct here (no psychiatric history) and kept. |
| E | minor | `metadata.distinguishing_features`, `.clinical_setting` | "pending antibodies"; setting "emergency_department_to_ICU" while the case meets no ICU criterion. | FIXED: wording updated; setting "emergency_department"; `last_revised`, `revision_reason`. |

## Changes, in one paragraph a physician can read before re-reviewing

Required work-up in order: serum labs, contrast MRI, CSF, routine EEG, pelvic ultrasound (soft MRI before LP). The ultrasound now reads as an indeterminate 1.2 cm left ovarian echogenic shadowing focus, and a new recommended pelvic MRI characterizes it as a mature cystic teratoma (macroscopic fat, calcification, no enhancing solid tissue), so the musts now include its removal. Continuous EEG is recommended (left temporal seizures, periodic discharges, incipient delta-beta short of EDB); DDI and literature are optional and last. The CSF report gives the final CSF anti-GluN1 result (1:160) with a 24-cell lymphocytic pleocytosis and IgG index 0.75; labs were regrouped with beta-hCG, onconeural and neuronal-surface panels. Her occupation now matches the HPI and lorazepam is on the medication list. Musts: acyclovir, methylprednisolone with IVIG or PLEX, laparoscopic ovary-sparing teratoma removal, levetiracetam or lacosamide without valproate, cEEG, neurology ward with cardiac monitoring, escalation at 10-14 days, lorazepam first, neurology with psychiatry and gynecology. Differential all low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used: `[Gresa-Arribas_2014]`, `[Venkatesan_2013]`, `[Herman_2015]`, `[Abboud_2021]` (plan 5.1).
- Plan ids `cEEG-escalation` and `pelvic-MRI-characterisation` contain capitals and fail the criterion-id pattern; this case uses `pelvic-mri-characterization` (the cEEG criterion keeps its existing id `action-6-analyze-eeg`).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case against the plan.
- Checked: pelvic MRI criterion and follow-up exist, are ordered after the ultrasound (soft constraint), and the MRI report supports the removal must; ultrasound impression is indeterminate as the plan requires; CSF numbers distinct, ratio 66.5/109 = 0.61; culture final; lorazepam on the list matches the benzodiazepine-positive screen; occupation matches the HPI; hyponatraemia 131 correctly graded mild with no M9; tetracycline allergy no conflict; ward level of care consistent with the plan rule. Checks and guards clean.
- Found: ANA 1:80 with a mother with SLE, mimic absent from the differential (ruling 7).
- Changed: added differential entry "Neuropsychiatric systemic lupus erythematosus" (low).
- Accepted as is: MRI right versus EEG left laterality (flagged by the worker; different phenomena, not a flipped finding).

## Condition audit (24 Oct 2026)

Condition auditor, after the workers and verifiers. Uniformity checks over all 30 cases; changes made here through `case_io` (all re-checked: `perfect_agent.py` 30/30, `case_io.py check` and the case guards clean):
- `initial_tool_outputs.body_imaging` (finding and impression), `followup_outputs[1]` (pelvic MRI finding, impression and measurements), the tumour and pelvic-MRI criteria' `expected_evidence` and `key_clinical_evidence` (B, minor, C17 template carry-over): the left ovarian lesion was 1.2 cm, the same size as M01's teratoma. Now 1.5 cm on ultrasound and 1.5 x 1.2 cm on MRI everywhere it appears; nothing else changed.

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
- `order_body_imaging study=chest_abdomen_pelvis_CT` -> `followup_outputs[order_chest_abdomen_pelvis_ct]`: CT chest/abdomen/pelvis shows the teratoma seen on the stored ultrasound.
- `order_advanced_imaging modality=whole_body_FDG_PET` -> `followup_outputs[order_whole_body_fdg_pet]`: whole-body PET/CT: non-avid fat-containing adnexal lesion.
- `obtain_tissue_diagnosis procedure=resection` -> `followup_outputs[order_resection]`: resection pathology: mature teratoma with neuroglial tissue.
- `labs:AED_levels` -> fallback labs panel `Antiseizure medication levels`: antiseizure drug levels: none detected (no antiseizure drug prescribed).
- `labs:valproate_level` -> fallback labs panel `Antiseizure medication levels`: antiseizure drug levels: none detected (no antiseizure drug prescribed).

Checks: `perfect_agent.py` ok; `test_case_guards.py -k NMDAR-ENC` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
