# NMDAR-ENC-RM02
Reviewer status: R1 none, R2 none (condition not reviewed in this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: condition not reviewed | - | - |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria` | Plan C1: non-schema `basic`, `screen_for`, exact literature `query`, MRI `protocol`, eleven-panel labs list. | FIXED: plan 3.2 arguments; the labs criterion adds `beta-hCG`, `MOG_IgG_cell_based` and `AQP4_IgG_cell_based` (plan per-case). |
| B | major | `ground_truth.action_criteria`, `followup_outputs` order | Literature first in the follow-ups, then DDI; no cEEG. | FIXED: criteria labs, MRI, CSF, EEG, pelvic US, cEEG, DDI, literature (ids kept); follow-ups cEEG, risperidone DDI, treatment literature, viral-differentiation literature. |
| C | major | `followup_outputs[0]` (new), criterion `ceeg-escalation` (new) | cEEG must with no cEEG report; two subclinical seizures on the routine EEG. | FIXED: 24 h cEEG, four left temporal seizures with bilateral spread (one with right face and arm twitching), GRDA, no extreme delta brush; recommended criterion. |
| B | major | `patient.clinical_history.medications` | HPI: risperidone 1 mg twice daily and oral levetiracetam started by the outside ED, lorazepam for sleep from the campus clinic; none listed (C17). | FIXED: lorazepam 0.5 mg at night as needed, levetiracetam 500 mg twice daily (dose not stated in the HPI; a standard starting dose chosen), risperidone 1 mg twice daily. |
| C | major | criterion `action-7-check-drug-interactions`, `followup_outputs` (risperidone DDI) | DDI recommended per C10 (risperidone); stored output claimed risperidone lowers thyroid hormone, quoted the patient's QTc, and "both can lower seizure threshold awareness". | FIXED: `{}` arguments, recommended; risperidone output in report voice (no PK interaction with levetiracetam or levothyroxine, additive sedation with lorazepam, QT class caution, antipsychotic intolerance, prolactin, CK/temperature after exposure, benzodiazepine alternatives). |
| D | minor | `initial_tool_outputs.drug_interactions` (new) | No generic DDI output for other drugs. | FIXED: general report from her medicines: oestrogen pill + IVIG thrombotic risk, ibuprofen + aciclovir, lorazepam + risperidone, levetiracetam + COC (no interaction), levothyroxine + steroids; D2 class warning; HBV screening; sulfonamide allergy note. |
| D | major | criterion `action-6-search-medical-literature` | Recommended literature step. | FIXED: optional, `{}`. Canonical initial literature output added. |
| C | major | `followup_outputs` (treatment literature) | Graus 2016 (a diagnostic paper) credited with a treatment protocol; Dalmau 2019 credited with "ICU in ~75%", "teratoma ~40%", "relapses ~12%", "rituximab preferred over cyclophosphamide" (unverified or wrong). | FIXED: Titulaer 2013 canonical finding, Abboud 2021 consensus, Dalmau 2019 described as a narrative update without numbers. |
| C | major | `followup_outputs` (viral-differentiation literature) | "Gable MS ... Annals of Neurology ... 1% had anti-NMDAR encephalitis" with EDB vs temporal periodic discharges: the citation and finding are fabricated. | FIXED: Gable MS, Clin Infect Dis 2012;54:899-904 (California Encephalitis Project: more frequent than any single viral aetiology under 30), Dalmau 2011 (prodrome 70%, clinical stages), Venkatesan 2013 (HSV PCR, empirical aciclovir). |
| B | blocker | `initial_tool_outputs.csf.special_tests`, `initial_tool_outputs.labs.panels` | CSF report "Pending" twice while labs gave CSF 1:64 in two panels (C4). | FIXED: CSF `NMDAR_antibodies` "Positive, titre 1:64 (...resulted day 5)", `Anti_NMDAR_antibodies` deleted; labs keep serum 1:320 only. Culture "Pending" resolved to "No growth at 72 hours". |
| B | major | `initial_tool_outputs.labs` | Exclusion-studies leak, duplicate inflammatory panel, anti-TPO and ANA inside the encephalitis panel, one-line paraneoplastic result, no beta-hCG, no MOG/AQP4 although the MRI shows multifocal white matter lesions. | FIXED: rebuilt per C5; new `Demyelinating disease antibodies (serum, cell-based assay)` (MOG-IgG, AQP4-IgG negative), `Onconeural antibodies (serum)`, `Other autoantibodies` (ANA 1:80), beta-hCG negative; values kept; plain interpretation. |
| B | minor | `initial_tool_outputs.ecg` | Finding "Sinus tachycardia at upper end of normal range" contradicts the rhythm (normal sinus rhythm 96); QTc 448 ms called borderline in a woman. | FIXED: "Sinus rhythm at 96 bpm"; QTc reported as normal; empty `clinical_correlation` removed. |
| D | minor | `initial_tool_outputs.eeg.impression` | Prose impression, not ACNS format. | FIXED: "This is an ABNORMAL EEG due to:" numbered list; content unchanged. |
| B | major | `initial_tool_outputs.body_imaging` | "Abnormal values: ... (H)" impression; lesion "possible calcification" while the musts plan teratoma removal (C12). | FIXED: echogenic Rokitansky nodule with shadowing calcification, no vascularity; impression "consistent with a mature cystic teratoma (dermoid)"; size 2.3 cm kept. |
| B | major | `fallback_tool_outputs.cardiac_monitoring`, `.advanced_imaging`, `.specialized_test` | Normal Holter (average 69) despite HR 65-115 lability; catch-all FDG-PET and neuropsychology fallbacks (C14). | FIXED: sinus rhythm with sinus tachycardia to 115 bpm (min 62, average 90); the other two null; `metadata.fallback_tool_kinds` updated. |
| C | major | `ground_truth.differential` | Template entries; ADEM/MOGAD and CNS vasculitis raised by the MRI report and the prior risperidone (NMS) not in the differential (rule 7). | FIXED: viral encephalitis, ADEM/MOGAD, primary CNS vasculitis, other AE (incl. DPPX), Hashimoto encephalopathy, psychiatric, NMS: all low with this case's data (NMS: 37.2 °C, CK 185 after two seizures, dyskinesias before risperidone). |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts ("levetiracetam or valproate" in a 23-year-old woman, CT CAP option, consults conditional on findings already present). | FIXED: M1, M2, M3 left ovarian teratoma removal, M4, M5, M6 ICU for GCS 12 and central hypoventilation, M7 with fertility, M8 lorazepam and stop risperidone with CK and temperature monitoring, VTE prophylaxis with review of the oestrogen pill (case-specific: IVIG, immobility, COC), M10 with gynaecology. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | P1 wording, P3 "young patient". | FIXED: canonical; P2, P4, P5 kept. |
| C | major | `ground_truth.key_clinical_evidence` | Template with wrong claims. | FIXED: six case-specific bullets (all six Graus groups, CSF 1:64, MRI with negative MOG/AQP4, EEG, teratoma, risperidone withdrawal). |
| B | minor | `ground_truth.red_herrings` | Prodrome data point "URI, fever, cough" (no fever in the HPI); hyponatraemia text; the MRI-pattern and risperidone traps named in metadata not listed. | FIXED: prodrome data point from the HPI with canonical interpretation; canonical hyponatraemia text; new MRI red herring (`mri.findings[0]`) and risperidone/NMS red herring. Psychiatric red herring kept (23, no psychiatric history). |
| E | minor | criteria `rationale`, `citations`, `expected_evidence` | Rationale = label; citation twins; generic evidence. | FIXED. |
| B | minor | `ground_truth.sequence_constraints`, `.stop_rule` | None; max 0. | FIXED: soft MRI before CSF; max 2. |
| B | minor | `metadata.difficulty_description`, `.difficulty_rationale` | Said the CSF antibody is pending and requires follow-up testing; "7 required tools, 3 red herrings". | FIXED: pending sentence removed; rationale updated (5 required actions, 5 red herrings). |

## Changes, in one paragraph a physician can read before re-reviewing

A 23-year-old woman with all six Graus groups, GCS 12 and central hypoventilation, multifocal periventricular and basal ganglia lesions, and risperidone started by an outside ED. Required: labs (now including MOG-IgG and AQP4-IgG, both negative), MRI before LP (soft), CSF, EEG and pelvic ultrasound; recommended: cEEG and the interaction check; optional: literature. The CSF report now carries its own result (anti-GluN1 1:64) and the labs only the serum titre (1:320). The medication list now holds the risperidone, levetiracetam and lorazepam the HPI describes. The ultrasound describes a 2.3 cm left ovarian mature cystic teratoma with characteristic features. A cEEG shows four left temporal seizures. The literature outputs no longer carry a fabricated Gable citation or unverified Dalmau 2019 percentages. Musts: aciclovir, steroids with IVIG or plasma exchange, left ovarian teratoma removal, levetiracetam or lacosamide without valproate, cEEG, ICU, escalation at 10-14 days, lorazepam with risperidone stopped and CK/temperature monitoring, and VTE prophylaxis with review of her oestrogen pill. The differential adds ADEM/MOGAD, CNS vasculitis, Hashimoto encephalopathy and NMS, all low with the excluding data stated.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used (plan CENTRAL 1): `[Gresa-Arribas_2014]`, `[Herman_2015]`, `[Dalmau_2019]`, `[Lejuste_2016]`.
- New criterion id `ceeg-escalation` (lower case; the schema rejects `cEEG-escalation`).

## Open questions for Andrea (judgment calls you could not settle)

- None. The levetiracetam dose (500 mg twice daily) is not stated in the HPI; I chose the usual starting dose for the medication list.

## Verification

Adversarial check (24 Oct 2026). Checked every own-finding row against the file: medication list now holds risperidone, levetiracetam, lorazepam and the combined pill named in the HPI; NMS red herring timing is right (oral and hand movements 5 days before, risperidone 2 days before); CSF/serum split (CSF 1:64, serum 1:320) correct; MOG-IgG and AQP4-IgG negative in labs and in the labs criterion; teratoma wording; cEEG left temporal with right face and arm twitching (contralateral, consistent); ICU for GCS 12 and central hypoventilation; VTE must consistent with the COC and IVIG; Gable MS, Clin Infect Dis 2012;54:899-904 verified. The MRI's worded imaging differential (ADEM, vasculitis) is allowed by the style guide (imaging differential) and is the case's own red herring, so it stays.

Found and fixed:
- `ground_truth.assessment.required_recommendations` (seizure must): the canonical "levetiracetam or lacosamide" ignored that she had her second convulsive seizure while already on levetiracetam 500 mg twice daily. Rewritten: increase levetiracetam (for example to 1500 mg twice daily), add lacosamide if seizures persist, avoid valproate, seizures respond mainly to immunotherapy.
- `initial_tool_outputs.mri.impression`: the impression ended without a full stop and did not state the haemorrhage result its own observations give; added "No haemorrhage on SWI." (needed for the HSV exclusion).
perfect_agent, case_io check and guards clean after the edits.

## Condition audit (24 Oct 2026)

Condition auditor, after the workers and verifiers. Uniformity checks over all 30 cases; changes made here through `case_io` (all re-checked: `perfect_agent.py` 30/30, `case_io.py check` and the case guards clean):
- `ground_truth.assessment.prohibited_recommendations[1]` and `[3]` (B/E, minor): the canonical P2 and P4 texts still carried an em dash before "antibody turnaround" and before "exclude mass effect", and an en dash in "1-2 weeks", while 18 other cases already had the dash-free canonical wording. Now "...high: antibody turnaround can take 1-2 weeks..." and "...new seizures: exclude mass effect first." Meaning unchanged.
- `followup_outputs[0].output.eeg_type` (A, minor): the continuous EEG report had no `eeg_type`, unlike the other 25 cEEG reports; set to `continuous_icu` so the report names the study it is (the MockServer discriminator reads this field). Content unchanged.
- `ground_truth.red_herrings[1].data_point` (B, minor): "previously well young adult" in a woman with treated hypothyroidism and migraine; now "young adult with no psychiatric history".
