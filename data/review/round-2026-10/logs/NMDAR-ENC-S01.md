# NMDAR-ENC-S01
Reviewer status: R1 not reviewed, R2 not reviewed (NMDAR-ENC has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | none: condition not reviewed. All changes below come from the condition plan (classes C1-C18, per-case index entry S01) and my own reading. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[*].alternatives` | Plan C1: `basic`, `screen_for`, `protocol: standard`, 11-panel list, `contrast: false` on the ultrasound, exact literature query. | FIXED: plan 3.2: labs alt A/B with `beta-hCG` (woman of 24); MRI `{contrast: true}`; CSF HSV_PCR + NMDAR_antibodies + OCB or IgG_index; EEG routine/video/continuous_icu; `{study: pelvis_abdomen_ultrasound}`; DDI and literature `{}`. |
| C | blocker | `followup_outputs` (literature, drug interactions) | Plan C3: placeholder outputs that repeat the criteria's expected evidence ("Confirms diagnostic criteria, treatment sequence..."); the case failed `test_any_query_outputs_do_not_leak_expected_evidence`. | FIXED: literature with real sources (Graus 2016, Gresa-Arribas 2014, Titulaer 2013, Dalmau 2011); DDI from her medicines (ethinylestradiol-methylprednisolone, COC-IVIG thrombosis, cetirizine-lorazepam sedation, levetiracetam none), D2 class warning, HBV screening before rituximab. Leak guard passes. |
| B | minor | `initial_tool_outputs.labs.panels.CBC[Hematocrit]`, `.abnormal_values_summary` | Plan S01: Hb 14.2 g/dL with Hct 35.4% (L) is inconsistent. | FIXED: Hct 42.4% (normal); summary updated. |
| D | major | `initial_tool_outputs.labs` | Plan C4/C5: CSF anti-NMDAR 1:320 in two serum panels; serum antibody twice; anti-TPO and ANA inside the encephalitis panel; "Exclusion studies" with HIV and a one-line "paraneoplastic_panel"; duplicate inflammatory panel; no beta-hCG. | FIXED: panels CBC, BMP, Hepatic, Coagulation, Inflammatory markers, Thyroid function, Thyroid autoantibodies, `Serum anti-GluN1 IgG (cell-based assay)` (1:160), neuronal-surface (5), onconeural (7, negative), Systemic autoimmunity (ANA), Infection serology (HIV), Toxicology (UDS, alcohol), beta-hCG (negative), Other (CK). Plain recital. |
| B | minor | `initial_tool_outputs.csf.glucose_ratio`, `.special_tests`, `.interpretation` | Ratio printed 0.59 although 62/98 is 0.63; two keys for the antibody; interpretation listed values only. | FIXED: ratio 0.63; one `NMDAR_antibodies` key in canonical form (1:320); pattern interpretation. |
| D | minor | `initial_tool_outputs.mri.impression` | Differential reasoning ("makes HSV encephalitis less likely but does not exclude it"). | FIXED: numbered impression with sizes and one hedged sentence ("An infectious encephalitis cannot be excluded on imaging."). |
| D | minor | `initial_tool_outputs.eeg.impression`, `.findings[1]` | Plan C13: "diffuse cortical dysfunction with epileptogenic activity"; seizures called subclinical though they occurred during behavioral arrest (exam: staring episodes). | FIXED: "This is an ABNORMAL EEG due to:" list; seizure correlate recorded. The limitations line recommending cEEG stays (plan S01). |
| B | major | `followup_outputs` (new cEEG), `ground_truth.action_criteria[ceeg-escalation]` | Plan C7/S01: two electrographic seizures with no cEEG follow-up. | FIXED: 24-h cEEG (EDB, GRDA, six left temporal seizures, four with behavioral arrest, no status); `ceeg-escalation` recommended. |
| D | major | `initial_tool_outputs.body_imaging.findings[0]`, `.impression` | Plan C12: "Abnormal values: ... (H)" template impression; the "teratoma" had "mild internal vascularity" and no characteristic features. | FIXED: Rokitansky nodule with shadowing, echogenic lines and dots, fat-fluid level, no internal vascularity; radiology-voice impression. |
| D | minor | `initial_tool_outputs.ecg.rate`, `.interpretation` | ECG rate 112 against vitals HR 114. | FIXED: 114. |
| C | major | `ground_truth.action_criteria[action-6...]`, `[action-7...]` | Ruling 5/6: literature and DDI `recommended`. | FIXED: both `optional`; follow-ups ordered cEEG, DDI, literature. |
| B | minor | criteria order, `.sequence_constraints`, `.stop_rule`, rationales, evidence, citations | Plan C6/C16/C18: rationale copied from label; free-text citations; stop rule max 0; no sequence constraint. | FIXED: labs, MRI, CSF, EEG, ultrasound, cEEG, DDI, literature (ids unchanged); soft MRI-before-CSF; stop rule five ids, max 2; case-anchored text; bracketed keys. |
| C | major | `ground_truth.assessment.required_recommendations`, `.prohibited_recommendations` | Plan C9 template ("paired CSF and serum" diagnostic must, "levetiracetam or valproate", "transvaginal and/or CAP CT"); em dashes in prohibitions. | FIXED: M1 (fever 38.4), M2, M3 removal of the right ovarian teratoma, M4 (no ASM yet: start levetiracetam or lacosamide, avoid valproate), M5 cEEG, M6 ward (rule: HR peaks at 130, no diaphoresis, no hypoventilation), M7 with fertility discussion, M8 lorazepam, stop the COC with VTE prophylaxis, neurology with psychiatry and gynecology. Canonical P1-P5. |
| C | major | `ground_truth.differential` | Plan C8 template (HSV `high`, other AE `moderate`). | FIXED: all `low` with case evidence: HSV/viral, bacterial meningoencephalitis (fever, WBC 11.2; lymphocytic CSF, cultures negative), other antibody encephalitis, psychiatric, drug-induced/NMS. |
| C | major | `ground_truth.key_clinical_evidence` | Plan C15 template ("100% sensitive", "~50% of young women"). | FIXED: six case-specific bullets. |
| C | minor | `ground_truth.red_herrings` | Prodrome described as "URI, fever, cough" with "redirect the workup" wording; psychiatric herring cites hallucinations not in this HPI; hyponatremia and CK templated. | FIXED: canonical prodrome, hyponatremia (133) and CK (179, `Other[0]`) interpretations; psychiatric herring matches the HPI. |
| D | major | `fallback_tool_outputs.advanced_imaging`, `.specialized_test`, `.cardiac_monitoring`, `metadata.fallback_tool_kinds` | Plan C14: FDG-PET and neuropsychology catch-alls; "Normal 24-hour Holter" with average 69 against HR 114-130. | FIXED: first two null; telemetry with sinus tachycardia to 130 bpm; kinds updated. |
| E | minor | `metadata.difficulty_rationale` | "5 required tools". | FIXED. |
| - | check | - | `perfect_agent.py -v`: ok; all required/recommended criteria answered by case data (cEEG by its follow-up). Guards 2 passed (the leak guard now passes). `case_io.py check`: nothing names S01. | - |

## Changes, in one paragraph a physician can read before re-reviewing

A 24-year-old woman on a combined oral contraceptive, three weeks after a febrile upper respiratory illness, with paranoia, paraphasic speech, two generalized seizures, orofacial dyskinesias, choreoathetosis, fluctuating consciousness, fever 38.4 and autonomic instability: anti-NMDAR encephalitis (CSF anti-GluN1 1:320, serum 1:160) with a 1.8 cm right ovarian mature cystic teratoma. Findings are unchanged; the hematocrit now matches the hemoglobin, the CSF glucose ratio is stated correctly (0.63), the serum labs no longer carry the CSF antibody and add onconeural antibodies and a negative beta-hCG, and the teratoma has characteristic ultrasound features without internal vascularity. A 24-hour cEEG exists (six left temporal seizures) and is a recommended escalation. Literature and drug checks are optional and now give real sources and her real interactions. Musts: acyclovir, steroids with IVIG or PLEX, teratoma removal, start levetiracetam or lacosamide, cEEG, ward with cardiac monitoring, escalation with fertility discussion, lorazepam, stop the contraceptive with VTE prophylaxis. The differential is all low and adds bacterial meningoencephalitis.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation registry (plan CENTRAL 1): new keys used here: `[Gresa-Arribas_2014]`, `[Herman_2015]`, `[Abboud_2021]`, `[Venkatesan_2013]`.

## Open questions for Andrea (judgment calls you could not settle)

- None. Decisions: (1) M6 is the ward wording by the plan's rule (HR peaks at 130, not above; labile BP without diaphoresis; no hypoventilation), although `metadata.clinical_setting` says "emergency_department_to_ICU". (2) The stop-the-contraceptive must is mine, as in RS01 (IVIG plus immobility plus estrogen). (3) The "mild bilateral facial weakness" in the cranial nerve exam is unusual for this disease but not contradictory; left unchanged.

## Verification

Adversarial verifier, 24 Oct 2026. No reviewer notes exist for NMDAR-ENC. Checked every own-finding row against the file and read the whole final case.
- Confirmed: Hct 42.4 with Hb 14.2 and removed from the abnormal summary; ECG rate 114 equals vitals HR; CSF ratio 62/98 = 0.63 and one antibody key (1:320); serum labs hold serum 1:160 only, beta-hCG negative; right ovarian 1.8 cm teratoma with characteristic features matches the removal must and the criterion; cEEG consistent with routine (left temporal seizures, EDB); placeholder literature/DDI outputs replaced with real sources and her real medicines (ACE-inhibitor angioedema allergy: no conflict with any must). Leak guard passes. Ward wording follows the plan's rule (HR max 130, not above).
- Found: nothing requiring a change.
- Re-run: `perfect_agent.py NMDAR-ENC-S01 -v` ok; `case_io.py check` nothing names S01; case guards pass.

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
