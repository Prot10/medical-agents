# NMDAR-ENC-P01
Reviewer status: none (condition not reviewed in this round; July 2026 tool review only) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: condition not reviewed | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-2-analyze-csf]` | Non-schema `basic` key: the required CSF criterion was unreachable (C1). | FIXED: `special_tests` alternatives per plan 3.2. |
| A | major | `action_criteria[action-1/4/5/7/8]` | `protocol: standard`, eleven-panel list, `contrast: false`, exact `query`, `drug`/`screen_for` (C1). | FIXED: minimal arguments per plan 3.2 (labs with beta-hCG: woman of 22). |
| D | blocker | `initial_tool_outputs.literature_search`, `.drug_interactions` | Placeholder literature finding and a DDI summary restating the criterion's expected evidence (C3; guard failing). | FIXED: canonical literature (plus Schmitt 2012 and Lejuste 2016); DDI in report voice from her medicines (combined oral contraceptive with IVIG and steroids, sertraline and sodium, levetiracetam, acyclovir), aspirin allergy checked (no conflict), D2 class warning, HBV screening. Guard passes. DDI and literature `optional`, `{}`. |
| B | blocker | `initial_tool_outputs.csf.special_tests`, `.labs.panels` | CSF antibody "Pending" under two keys while the labs report gave the CSF titer 1:32 twice (C4). | FIXED: `NMDAR_antibodies` "Positive, titer 1:32 (... resulted day 8)"; result once in a full interpretation; culture final at 72 hours; CSF entries removed from labs. |
| B | major | `initial_tool_outputs.labs` | Duplicated inflammatory markers and serum antibody, "Exclusion studies", one-line autoimmune panel, no beta-hCG; interpretation "All values within normal limits." despite a positive serum antibody (C5). | FIXED: panels rebuilt per C5 (serum anti-GluN1 1:10, neuronal-surface and onconeural panels, ANA, HIV, toxicology, beta-hCG negative); abnormal values summary and interpretation written. |
| B | minor | `initial_tool_outputs.labs.panels.CBC` | WBC 10.1 with lymphocytes 3.2 and neutrophils 4.9 leaves 2.0 unexplained. | FIXED: WBC 8.6. |
| C | major | `initial_tool_outputs.body_imaging` | Vague 1.2 cm complex lesion "with a small echogenic focus" while the case intends a teratoma; lab-template impression "Abnormal values: ... (H)" (C12). | FIXED: 1.6 cm complex cystic lesion with a shadowing Rokitansky nodule and echogenic lines and dots; radiology impression "consistent with a mature cystic teratoma (dermoid)"; measurement added. |
| B | minor | `initial_tool_outputs.eeg.impression`, `.limitations` | One-line impression; management recommendation inside `limitations`. | FIXED: numbered "This is an ABNORMAL EEG due to:" impression (no seizures, no extreme delta brush); recommendation moved to `recommended_actions`. |
| B | minor | `followup_outputs[0]` (cEEG) | Impression outside the C7 template; cross-modality correlation "Progressive encephalopathy"; management line "Continue EEG monitoring." | FIXED: C7 template (one left frontotemporal seizure without clinical correlate, no extreme delta brush); correlation and recommendation emptied. |
| C | major | `fallback_tool_outputs` | Fallback ECG (rate 84) and Holter (min 49, average 69) unrelated to the case; FDG-PET and specialized-test fallbacks; DDI `proposed` engineering text (C14, C3). | FIXED: `initial_tool_outputs.ecg` normal sinus rhythm 91; telemetry fallback (72-112, average 90); advanced imaging, specialized test and ECG fallbacks null; `proposed` ""; `fallback_tool_kinds` updated. |
| C | major | `action_criteria` order, `sequence_constraints`, `stop_rule` | C6, C18 (no constraint, max 0). | FIXED: labs, MRI, CSF, EEG, ultrasound, cEEG, DDI, literature; soft MRI-before-CSF; stop rule five ids, max 2. |
| E | minor | `action_criteria[*]` | Rationale = label, citation twins, generic evidence (C16). | FIXED: case-specific evidence; CSF rationale states that the probable criteria are not met, so the CSF assay decides. |
| C | major | `assessment.required_recommendations` | Template musts (C9): paired-sample must, "levetiracetam or valproate" in a woman of 22, ICU for a patient with normal vitals and GCS, conditional gynecology consult despite a found teratoma; no word on the risperidone prescribed at urgent care. | FIXED: M1, M2, M3 removal of the left ovarian teratoma, M4 without valproate, M5, M6 ward, M7, M8 lorazepam first and do not start risperidone, M10 with gynecology. |
| C | minor | `assessment.prohibited_recommendations` | "young patient", dashes. | FIXED: canonical P1-P5. |
| C | major | `ground_truth.differential` | Template, not updated, HSV "high" (C8). | FIXED: all `low` with case data; neuropsychiatric SLE added (mother with SLE, ANA 1:40 borderline). |
| C | major | `ground_truth.key_clinical_evidence` | Template with wrong claims ("100% sensitive", EDB "highly specific (30-50%)", "~50% of young women", dyskinesias and dysautonomia she does not have) (C15). | FIXED: six case-specific bullets; the first states that she has at most three Graus groups and the second that the diagnosis rests on CSF anti-GluN1 1:32. |
| B | minor | `ground_truth.red_herrings[0]` | "previously well young adult" (she has generalized anxiety disorder); interpretation lists CSF pleocytosis and dyskinesias absent here. | FIXED: data point from the HPI; interpretation names her actual red flags. Added two red herrings present in the case: normal CSF cells with normal MRI, and the viral-like prodrome (RH_PRODROME_CI). |
| B | minor | `patient.clinical_history.social_history.occupation`, `patient.history_present_illness` | Occupation "graphic designer" while she lives in a campus dormitory, attends classes and has professors (C17); "upcoming final exams" vs midterms completed two weeks ago; double-hyphen dashes. | FIXED: "University student (graphic design)"; "midterm examinations"; dashes replaced by commas. |
| C | minor | `ground_truth.avoided_actions[avoid-waste-4]` | Rationale names orofacial dyskinesias she does not have. | FIXED: "movement disorders of autoimmune encephalitis" wording. |
| E | minor | `metadata.difficulty_rationale` | "1 red herrings"; no mention of what makes the puzzle. | FIXED: 3 red herrings, diagnosis resting on the CSF assay; `last_revised`, `revision_reason`. |
| B | minor | `initial_tool_outputs.csf.glucose_ratio` | Serum glucose 92 mg/dL at LP vs 100 mg/dL in labs. | FLAGGED, kept: different sampling times; ratio 0.63 normal either way. |
| C | minor | `patient.neurological_exam.mental_status` | Clock drawing "numbers clustered on the right side" hints at left neglect without other right-hemisphere signs. | FLAGGED, kept: pre-existing prose, compatible with diffuse encephalopathy. |

## Changes, in one paragraph a physician can read before re-reviewing

Required work-up in order: serum labs (with beta-hCG), contrast MRI, CSF, routine EEG, pelvic ultrasound (soft MRI before LP); continuous EEG is recommended and captures one left frontotemporal electrographic seizure; DDI and literature optional and last. The puzzle is kept: CSF has 3 cells with borderline IgG index and equivocal bands, MRI is essentially normal and she has at most three Graus groups, so the probable criteria are not met and the diagnosis rests on the CSF anti-GluN1 result (titer 1:32), now given in the CSF report; serum is positive only at 1:10. The ovarian lesion now has characteristic teratoma features (1.6 cm, shadowing Rokitansky nodule). Musts: acyclovir, methylprednisolone with IVIG or PLEX, ovary-sparing removal of the left teratoma, levetiracetam or lacosamide without valproate, cEEG, neurology ward with cardiac monitoring, escalation at 10-14 days, lorazepam first without starting the prescribed risperidone, neurology with psychiatry and gynecology. Differential all low, with neuropsychiatric lupus added. Occupation corrected to university student.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used: `[Gresa-Arribas_2014]`, `[Venkatesan_2013]`, `[Herman_2015]`, `[Abboud_2021]` (plan 5.1).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case against the plan.
- Checked: CSF result only in the CSF report (1:32), serum 1:10 in labs; WBC 8.6 now sums with the differential; characteristic teratoma features and removal must; cEEG seizure consistent with a routine EEG without epileptiform activity; NPSLE entry; risperidone must; aspirin allergy no conflict. Checks and guards clean.
- Found: (1) key evidence and the CSF rationale said "at most three" / "fewer than four" groups, so probable criteria were not met. That reasoning is wrong: Graus 2016 accepts three groups with a systemic teratoma, and she has a teratoma and an abnormal EEG, so three groups would meet the probable criteria. Counted from the exam she has two groups (psychiatric/cognitive and probable seizures; speech fluent, consciousness preserved, no dyskinesias or dysautonomia), which keeps the puzzle valid. (2) The ultrasound gave a 1.5 cm dominant follicle "consistent with normal menstrual cycle" and a secretory-phase endometrium in a woman on a combined oral contraceptive, which suppresses ovulation (pre-existing). (3) ANA 1:40 marked not abnormal against a reference of "<1:40". (4) The fallback telemetry showed tachycardia to 112 bpm in a patient with HR 91 and no autonomic signs, which would add an autonomic group the case denies.
- Changed: `ground_truth.key_clinical_evidence[0]` (two groups, fewer than the three that suffice with a teratoma); `action_criteria[action-2-analyze-csf].rationale` (same reasoning); `metadata.difficulty_rationale` ("only two of the six symptom groups"); `initial_tool_outputs.body_imaging` right ovary "a few small follicles", uterus "thin endometrium (4 mm), consistent with combined oral contraceptive use", impression item 2 "Right ovary and uterus normal."; labs ANA `reference_range` "<1:80"; `fallback_tool_outputs.cardiac_monitoring` sinus rhythm 62-98 bpm (average 80).
- Lead: plan section 4 (P01) says "fewer than 4 groups" for the probable criteria; the teratoma clause makes the threshold three groups in teratoma cases.

## Close-out (24 Oct 2026)

- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions autoimmune_encephalitis_nmdar`): the generic G04.81 labels "autoimmune encephalitis", "antibody mediated encephalitis" and "autoimmune limbic encephalitis" and code G04.90 are no longer accepted, because every token of the first two occurs in "anti-LGI1 autoimmune encephalitis" or "seronegative autoimmune encephalitis" (alternatives the work-up excludes), limbic encephalitis is a different syndrome (Graus 2016) and G04.90 is unspecified encephalitis. Added "glun1 encephalitis", "nr1 encephalitis" and code G04.8. `accepted[0]` and `icd_codes[0]` unchanged. Decisions: `plans/NMDAR-ENC-decisions.md`.
- `patient.neurological_exam.mental_status`: clock drawing "numbers clustered on the right side" (a left-neglect sign that no other finding supports) now "unevenly spaced numbers and misplaced hands", compatible with the diffuse encephalopathy. The two serum glucose values (92 at LP, 100 in labs) stay: different sampling times, ratio normal either way.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
