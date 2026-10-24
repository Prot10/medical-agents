# NMDAR-ENC-M04
Reviewer status: none (condition not reviewed in this round; July 2026 tool review only) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: condition not reviewed | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-2-analyze-csf]` | Non-schema `basic` key: the required CSF criterion was unreachable (C1). | FIXED: `special_tests` alternatives per plan 3.2. |
| A | major | `action_criteria[action-1/4/5/7/8]` | `protocol: standard`, eleven-panel list, `contrast: false`, exact `query`, `screen_for` (C1). | FIXED: minimal arguments per plan 3.2. |
| D | major | `patient.clinical_history.medications[Quetiapine].indication` | "to be discontinued given likely autoimmune encephalitis": the diagnosis in the patient block (C17). | FIXED: prescriber's indication only ("Provisional acute stress reaction with psychotic features, started by GP 2 days before presentation"). |
| A | minor | `patient.age`, `.ethnicity`, `.hpi`, `.occupation`, `.pmh`, `.presenting_complaint`, `.sex` | Stray keys outside the patient schema (ignored by the model, duplicated the HPI and PMH); social history held in one `note` string. | FIXED: stray keys deleted (content already in `demographics`, `history_present_illness`, `past_medical_history`, `chief_complaint`); social history split into keys; PMH dashes removed. |
| D | major | `followup_outputs[1]` (quetiapine DDI) | Reachable only through a quetiapine trigger; "Quetiapine x Anti-NMDAR encephalitis" names the diagnosis; summary "Expert consensus, Dalmau et al. Lancet Neurol 2011" is a citation the source does not support for this content. | FIXED: moved to `initial_tool_outputs.drug_interactions.general` (any drug) in report voice: quetiapine (seizure threshold, QTc, neuroleptic intolerance, discontinue), sertraline (SIADH, small QTc effect), steroid effects, levetiracetam, aciclovir; D2 class warning; NMS monitoring; HBV screening; lorazepam as alternative. Follow-up deleted. Criterion `recommended` per C10, `{}`. |
| C | minor | `followup_outputs` literature (`request_immunotherapy_first_line`) | Untitled summary result without a source. | FIXED: kept the topic, two sourced results (Titulaer 2013 figures per plan 1.2; Abboud 2021 consensus), placed last; canonical literature also stored as `initial_tool_outputs.literature_search` for any other query. Criterion `optional`. |
| B | blocker | `initial_tool_outputs.csf.special_tests`, `.labs.panels` | CSF antibody "Pending" (two keys) while labs gave the CSF titre 1:160 (C4). | FIXED: `NMDAR_antibodies` "Positive, titre 1:160 (... resulted day 6)"; result in the interpretation; CSF entries removed from labs. |
| B | minor | `initial_tool_outputs.csf.interpretation`, `.glucose_ratio` | Interpretation listed three values only; no glucose ratio. | FIXED: full pattern recital; ratio 0.68 against the serum glucose (96 mg/dL = 5.3 mmol/L). |
| B | major | `initial_tool_outputs.labs` | Duplicates, "Exclusion studies", one-line autoimmune panel, CSF entries (C5); no osmolality despite Na 129. | FIXED: panels rebuilt per C5 (neuronal-surface and onconeural panels, HIV, toxicology, beta-hCG negative, Other CK) plus serum osmolality 265 (calculated about 267), urine osmolality 412, urine sodium 46 (SIADH pattern). |
| C | major | new criterion `siadh-osmolality-workup` | Moderate hyponatraemia without its work-up (plan 3.2). | FIXED: recommended `{panels: [serum_osmolality, urine_osmolality]}`, answered by the labs report. |
| B | minor | `initial_tool_outputs.eeg.findings[1..2]`, `.impression` | Finding text "in the context of the clinical scenario raises concern for subclinical seizure activity" (cross-modality); dash; impression a single line. | FIXED: interpretive clause removed; numbered "This is an ABNORMAL EEG due to:" impression with "No electrographic seizures and no extreme delta brush recorded". |
| B | minor | `followup_outputs[0].output` (cEEG) | Impression "Subclinical electrographic seizures confirmed..." outside the template; dash. | FIXED: C7 template (severe slowing, right temporal rhythmic delta, three right temporal seizures without clinical correlate, no EDB). |
| B | minor | MRI left hippocampal signal vs EEG and cEEG right temporal | Laterality differs between MRI and EEG. | FLAGGED, kept: the disease is diffuse and the two findings are different phenomena; no field states the opposite side for the same finding. |
| D | minor | `initial_tool_outputs.body_imaging.impression` | Lab template ("Abnormal values: ... (H)") with a garbled sentence. | FIXED: radiology impression (3.8 cm left mature cystic teratoma with fat-containing nodule and shadowing calcification); "No free fluid" finding added. |
| C | major | `fallback_tool_outputs` | Fallback ECG rate 70 and Holter average 81 contradicted HR 108 (C14); FDG-PET and neuropsychology fallbacks; `proposed` text. | FIXED: `initial_tool_outputs.ecg` sinus tachycardia 108 with normal intervals; telemetry fallback; advanced imaging, specialized test and ECG fallbacks null; CT, echo kept; `fallback_tool_kinds` updated. |
| C | major | `action_criteria` order, `sequence_constraints`, `stop_rule` | C6, C18. | FIXED: labs, MRI, CSF, EEG, ultrasound, cEEG, SIADH, DDI, literature; soft MRI-before-CSF; stop rule five ids, max 2. |
| E | minor | `action_criteria[*]` | Rationale = label, citation twins, generic evidence (C16). | FIXED (British spelling throughout). |
| C | major | `assessment.required_recommendations` | Template musts (C9); quetiapine not stopped. | FIXED: M1 aciclovir, M2, M3 removal of the left ovarian teratoma, M4 without valproate, M5, M6 ward (GCS 13, HR 108: no ICU feature), M7, M8 lorazepam and stop quetiapine with CK/temperature monitoring, M9 moderate hyponatraemia (fluid restriction, sertraline review, at most 10 mEq/L per 24 h, the case's lab unit), M10 with gynaecology. |
| C | minor | `assessment.prohibited_recommendations` | "young patient", dashes. | FIXED: canonical P1-P5. |
| C | major | `ground_truth.differential` | Template, not updated (C8). | FIXED: all `low`; NMS entry states 2 days of quetiapine, 37.6 C, CK 148, normal tone. |
| C | major | `ground_truth.key_clinical_evidence` | Template with wrong claims (C15). | FIXED: six case-specific bullets. |
| B | minor | `ground_truth.red_herrings[0,1,2,4,5]` | "previously well young adult" (she has GAD); "Mild hyponatremia" for 129; CK template; quetiapine "with initial symptomatic improvement" (not in the HPI: she seized 2 days after starting it); CRP "7 mg/L" while the lab is 0.8 mg/dL (8 mg/L); interpretation said HSV is typically bilateral (HSV encephalitis is typically asymmetric). | FIXED: data points and interpretations per C15 and the case data. |
| E | minor | `metadata.difficulty_description`, `.difficulty_rationale` | "antibodies pending"; "7 required tools, 3 red herrings". | FIXED: reworded; 5 required tools, 6 red herrings; `last_revised`, `revision_reason`. |
| E | minor | `initial_tool_outputs.mri.additional_observations` | "No acute hemorrhage" in an otherwise British-spelled case. | FLAGGED, kept (pre-existing prose, no clinical error). |

## Changes, in one paragraph a physician can read before re-reviewing

Required work-up in order: serum labs, contrast MRI, CSF, routine EEG, pelvic ultrasound (soft MRI before LP); continuous EEG (three right temporal seizures without clinical correlate), the SIADH osmolality set and the drug-interaction check are recommended; literature optional and last. The CSF report gives the final CSF anti-GluN1 result (titre 1:160) with the full CSF pattern; labs were regrouped and now include serum osmolality 265, urine osmolality 412 and urine sodium 46 for the sodium of 129. The quetiapine indication no longer names the diagnosis, and stray duplicate patient fields were removed. The interaction check, in report voice, covers quetiapine and sertraline for any drug queried. Musts: aciclovir, methylprednisolone with IVIG or PLEX, laparoscopic ovary-sparing removal of the left ovarian teratoma, levetiracetam or lacosamide without valproate, cEEG, neurology ward with cardiac monitoring, escalation at 10-14 days, lorazepam first with quetiapine stopped, SIADH treatment with the correction limit, neurology with psychiatry and gynaecology. Differential all low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used: `[Gresa-Arribas_2014]`, `[Venkatesan_2013]`, `[Herman_2015]`, `[Spasovski_2014]`, `[Lejuste_2016]` (plan 5.1).

## Open questions for Andrea (judgment calls you could not settle)

- None. The case is written in British English, so the plan's canonical texts are used in British spelling here (aciclovir, titre, tumour, hyponatraemia).

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case against the plan.
- Checked: quetiapine indication no longer leaks the diagnosis; stray patient keys gone; DDI any-drug output covers quetiapine and sertraline; SIADH studies consistent with Na 129 (calculated osmolality about 267); CRP red herring 8 mg/L matches 0.8 mg/dL; cEEG right temporal seizures consistent with the routine right temporal IRDA; teratoma ultrasound consistent with the label and the removal must; musts M8 and M9 present. Checks and guards clean.
- Found: the HPI said "She had no prior psychiatric history" while the same HPI, the PMH and the medication list give generalised anxiety disorder on sertraline for 3 months (internal contradiction, pre-existing, missed by the worker).
- Changed: `patient.history_present_illness` sentence now "Apart from generalised anxiety, she had no prior psychiatric illness or psychiatric admission, no prior seizures, and no significant past medical history."

## Close-out (24 Oct 2026)

- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions autoimmune_encephalitis_nmdar`): the generic G04.81 labels "autoimmune encephalitis", "antibody mediated encephalitis" and "autoimmune limbic encephalitis" and code G04.90 are no longer accepted, because every token of the first two occurs in "anti-LGI1 autoimmune encephalitis" or "seronegative autoimmune encephalitis" (alternatives the work-up excludes), limbic encephalitis is a different syndrome (Graus 2016) and G04.90 is unspecified encephalitis. Added "glun1 encephalitis", "nr1 encephalitis" and code G04.8. `accepted[0]` and `icd_codes[0]` unchanged. Decisions: `plans/NMDAR-ENC-decisions.md`.
- `initial_tool_outputs.mri.additional_observations`: "No acute hemorrhage" to "No acute haemorrhage" (British spelling of the case; worker flag).
