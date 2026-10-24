# NMDAR-ENC-RP02
Reviewer status: R1 none, R2 none (condition not reviewed in this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: condition not reviewed | - | - |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria` | Plan C1: non-schema `basic`, `screen_for`, `drug`, MRI `protocol`, exact literature `query`, eleven-panel labs list. | FIXED: plan 3.2 arguments; labs (age 76) add `paraneoplastic_panel` and `autoimmune_encephalitis_panel`. |
| B | blocker | `initial_tool_outputs.csf.special_tests.NMDAR_antibodies`, `initial_tool_outputs.labs.panels` | CSF report "Positive" without titre while the labs carried the CSF titre 1:32 (C4). | FIXED: CSF "Positive, titre 1:32 (cell-based assay, IgG anti-GluN1)"; labs keep the serum result (negative) only. |
| B | major | `initial_tool_outputs.csf.glucose`, `.glucose_ratio`, `.special_tests.CSF_lactate` | Glucose 38 mg/dL (ratio 0.35) and lactate 4.1 point to bacterial, mycobacterial or carcinomatous meningitis and conflict with the label. | FIXED: glucose 64 mg/dL (ratio 0.59); lactate deleted; second cytology "no malignant cells" added; culture "No growth at 72 hours". |
| C | major | `ground_truth.assessment.required_recommendations` | Template: testicular ultrasound at 76 with known lung cancer, "levetiracetam or valproate" with lamotrigine, aciclovir every 8 h in CKD 3, no nivolumab decision, no treatment of the aspiration pneumonia. | FIXED: withhold nivolumab (ASCO 2021); M1 every 12 h (CrCl about 45 mL/min); ASCO steroid wording with IVIG or plasma exchange; CT restaging must; M4 with renal levetiracetam dose and the lamotrigine clause; M5; ICU with airway assessment for GCS 7; aspiration pneumonia with a cephalosporin after a non-severe penicillin rash; baclofen and clorazepate review; consider early escalation; oncology and critical care. |
| C | major | `patient.clinical_history.medications` vs differential and musts | Baclofen 30 mg/day (renally cleared) and clorazepate in CKD 3 with myoclonus and triphasic discharges: a real toxic mimic, unaddressed. | FIXED: toxic-metabolic differential entry with the excluding data, sedative review must, DDI line. |
| C | major | criterion `action-8-check-drug-interactions`, `initial_tool_outputs.drug_interactions` (new), DDI follow-up | DDI must be required (C10); no generic output; follow-up claimed steroids lower lamotrigine levels by 20-30% (unsupported), listed rituximab as an alternative, em dashes. | FIXED: required, `{}`; general report (lamotrigine-valproate, levetiracetam and aciclovir renal dosing, steroid-nivolumab, baclofen accumulation, lisinopril and IVIG, D2 class warning, cephalosporin after a non-severe penicillin rash, HBV screening); follow-up in report voice with IVIG or plasma exchange as the alternative. |
| D | major | criterion `action-7-search-medical-literature`, literature follow-up | Literature recommended; output had unsourced titles ("Lancet Oncology 2022 consensus") with unverified figures. | FIXED: optional, `{}`; Schneider (ASCO) 2021, Sechi 2020, Graus 2021; canonical initial literature output. |
| B | major | `initial_tool_outputs.body_imaging` | Contrast `false` against a contrast criterion; "No ovarian or testicular mass (not applicable: male patient)"; "in the setting of decreased level of consciousness" and "correlate clinically" (C13); em dashes. | FIXED: contrast CT report with structured findings and a numbered impression. |
| D | minor | `initial_tool_outputs.eeg.impression` | Prose impression attributing the focal changes to the epidermoid (cross-modality, C13). | FIXED: ACNS numbered impression; findings unchanged. |
| D | minor | `followup_outputs[0].output.impression` (cEEG) | Not in ACNS form. | FIXED: numbered impression with extreme delta brush and three subclinical seizures. |
| B | minor | `initial_tool_outputs.mri.impression`, `.additional_observations` | Prose impression listing diseases; no statement on cortical or deep grey matter diffusion, which the CJD differential needs. | FIXED: numbered impression; "No cortical or deep grey matter diffusion restriction" added. |
| B | major | `initial_tool_outputs.labs` | Exclusion-studies leak, duplicate CRP and anti-TPO, GABA-B and AMPA under "Additional", GAD65 in the onconeural panel, ESR only in "Reviewed inflammatory markers", parenthetical comments in the summary. | FIXED: rebuilt per C5 with the case's values; lamotrigine level kept in `Drug levels`. |
| B | major | `fallback_tool_outputs.cardiac_monitoring`, `.advanced_imaging`, `.specialized_test`, `.echo` | Normal Holter (average 68) against heart rate 55-110 with diaphoresis; catch-all FDG-PET and neuropsychology fallbacks (C14); normal LV against ECG LVH. | FIXED: Holter with sinus tachycardia to 110 bpm (min 55, average 84); the two catch-alls null; echo mild concentric LVH with the existing aortic sclerosis; `metadata.fallback_tool_kinds` updated. |
| C | major | `ground_truth.differential` | Template (HSV high, other AE moderate, psychiatric, drug psychosis); no NCSE/structural epilepsy, leptomeningeal carcinomatosis, antibody-negative ICI encephalitis or toxic encephalopathy. | FIXED: seven low entries with the case's data (NCSE or post-ictal state, HSV/VZV, leptomeningeal carcinomatosis or metastases, antibody-negative ICI encephalitis, classical paraneoplastic encephalitis, CJD with 24-hour onset, toxic-metabolic). |
| C | major | `ground_truth.key_clinical_evidence` | Template with wrong claims and young-woman tumour text. | FIXED: six case-specific bullets including the irAE framing. |
| B | major | `ground_truth.red_herrings` | Prodrome red herring although the HPI denies fever, cough and infection (C15); no epilepsy, lung-cancer, periodic-discharge or serum-negative traps. | FIXED: prodrome deleted; canonical hyponatraemia; structural epilepsy (`past_medical_history[2]`); known lung cancer (`body_imaging.findings[0]`); triphasic GPDs and myoclonus (`eeg.findings[3]`); negative serum assay. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | P1 wording, P3 "young patient"; no checkpoint-inhibitor prohibition. | FIXED: canonical P1-P5, plus "Do not continue nivolumab while the encephalitis is active". |
| B | minor | `ground_truth.avoided_actions[2..3].rationale` | Amyloid PET "in a young patient"; DaTscan rationale cites orofacial dyskinesias that are absent. | FIXED. |
| E | minor | criteria `rationale`, `citations`, `expected_evidence` | Rationale = label; citation twins. | FIXED. |
| B | minor | `ground_truth.sequence_constraints`, `.stop_rule` | None; max 0. | FIXED: soft MRI before CSF only (CT head done in the ED); max 2. |
| E | minor | `initial_tool_outputs.ecg`, `metadata.case_body_concerns[0].detail`, `.difficulty_rationale` | Empty clinical_correlation; em dash; "7 required tools, 2 red herrings". | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 76-year-old man on his 14th cycle of nivolumab for regressing lung squamous carcinoma presents with 24 hours of mutism, GCS 7, myoclonus, heart-rate lability, CKD stage 3, lamotrigine for remote epidermoid-related epilepsy, and baclofen and clorazepate. The CSF now carries its own anti-GluN1 result (1:32; serum negative). Its glucose is normal (ratio 0.59), the lactate that pointed to bacterial or carcinomatous meningitis is gone, and a second cytology is negative. Required: serum labs including onconeural and neuronal-surface panels, MRI before LP (soft), CSF, EEG, CT restaging of the chest, abdomen and pelvis (regressing tumour, aspiration consolidation, no new tumour), and the interaction check. Recommended: cEEG (extreme delta brush, three subclinical seizures). Optional: literature. Musts:
- withhold nivolumab;
- aciclovir every 12 hours;
- methylprednisolone 1 g for 3 to 5 days, adding IVIG or plasma exchange;
- levetiracetam at a renal dose, avoiding valproate with lamotrigine;
- cEEG and ICU with airway assessment;
- a cephalosporin for the aspiration pneumonia despite the penicillin rash;
- review of baclofen and clorazepate;
- early escalation if there is no response.

The differential covers NCSE from the epidermoid, HSV, leptomeningeal carcinomatosis, antibody-negative checkpoint encephalitis, classical paraneoplastic encephalitis, CJD and baclofen or metabolic toxicity, all low with the excluding data.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used (plan CENTRAL 1): `[ASCO_irAE_2021]`, `[Graus_2021]`, `[Gresa-Arribas_2014]`, `[Herman_2015]`, `[Titulaer_late_2013]`.
- `metadata.case_body_concerns[0]` (routing to a checkpoint-inhibitor pack) kept: a routing decision for the condition owner. The case policy now encodes nivolumab withdrawal and the immunotherapy interactions that the concern said were missing.

## Open questions for Andrea (judgment calls you could not settle)

- The must "reduce baclofen rather than stopping it abruptly, and review clorazepate" is my addition (baclofen accumulates in CKD and causes encephalopathy with myoclonus). Tell me if you prefer it as a recommendation outside the scored musts.
- Should steroids be given with IVIG or plasma exchange from the start, or steroids first and then IVIG or plasma exchange? The plan (ASCO) gives methylprednisolone first and adds IVIG or plasma exchange if there is no improvement. I added IVIG or plasma exchange from the start because the encephalitis is severe and antibody-positive, which ASCO also covers. Tell me if you want steroids-first only.

## Verification

Adversarial check (24 Oct 2026). Whole final case read (large rewrite, numbers changed). Checked: CSF glucose 64 / serum 108 (ratio 0.59), lactate removed, two negative cytologies, CSF 1:32 with serum negative; CrCl about 45 mL/min is consistent with age 76, creatinine 1.3 and BMI 24 (Cockcroft-Gault at about 70 kg gives 48), so aciclovir every 12 hours and levetiracetam 250-750 mg twice daily are right; lamotrigine level 7.8 within range; DDI required with real pairs from his list (lamotrigine, baclofen, clorazepate, lisinopril, bisoprolol, nivolumab); cephalosporin after a non-severe penicillin rash is acceptable; CAP CT shows regressing primary and the aspiration consolidation that the pneumonia must treats; cEEG (extreme delta brush, left temporal seizures) consistent with the routine EEG's left temporal sharp waves; literature verified (Schneider 2021 ASCO; Sechi E, Neurology 2020;95:e2442-e2452; Graus 2021). Left Babinski with a left temporal lesion is pre-existing in this real-case seed (PMC5471763) and the patient is encephalopathic; left unchanged.

Found and fixed:
- `patient.clinical_history.social_history.smoking`: "quit 3 years ago at cancer diagnosis" contradicted the cancer diagnosis 14 months ago in the past medical history; now "quit 14 months ago at cancer diagnosis".

The worker's two open questions are resolved here rather than left for Andrea:
1. The baclofen/clorazepate review must stays as a scored must: baclofen is renally cleared and accumulates in CKD 3 with encephalopathy and myoclonus, the case raises it in the differential and a red herring, and reducing rather than stopping abruptly is the safe action (withdrawal seizures).
2. Steroids with IVIG or plasma exchange from the start stays: ASCO 2021 for severe (grade 3-4) immune-related encephalitis gives methylprednisolone 1 g daily for 3 to 5 days plus IVIG or plasma exchange for severe or progressing symptoms or antibody-positive disease; GCS 7 with CSF anti-GluN1 qualifies, and the must also covers the add-on-if-no-improvement reading.
perfect_agent, case_io check and guards clean after the edit.

## Condition audit (24 Oct 2026)

Condition auditor, after the workers and verifiers. Uniformity checks over all 30 cases; changes made here through `case_io` (all re-checked: `perfect_agent.py` 30/30, `case_io.py check` and the case guards clean):
- `ground_truth.assessment.prohibited_recommendations[1]` and `[3]` (B/E, minor): the canonical P2 and P4 texts still carried an em dash before "antibody turnaround" and before "exclude mass effect", and an en dash in "1-2 weeks", while 18 other cases already had the dash-free canonical wording. Now "...high: antibody turnaround can take 1-2 weeks..." and "...new seizures: exclude mass effect first." Meaning unchanged.
- `followup_outputs[0].output.impression` (E, minor): added the template closing "Clinical correlation recommended." (plan C7 template).

## Close-out (24 Oct 2026)

- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions autoimmune_encephalitis_nmdar`): the generic G04.81 labels "autoimmune encephalitis", "antibody mediated encephalitis" and "autoimmune limbic encephalitis" and code G04.90 are no longer accepted, because every token of the first two occurs in "anti-LGI1 autoimmune encephalitis" or "seronegative autoimmune encephalitis" (alternatives the work-up excludes), limbic encephalitis is a different syndrome (Graus 2016) and G04.90 is unspecified encephalitis. Added "glun1 encephalitis", "nr1 encephalitis" and code G04.8. `accepted[0]` and `icd_codes[0]` unchanged. Decisions: `plans/NMDAR-ENC-decisions.md`.
- `metadata.case_body_concerns`: the entry proposing a checkpoint-inhibitor pack removed. Decision: the case stays in this condition (anti-GluN1 positive in CSF; ICI-associated anti-NMDAR encephalitis is anti-NMDAR encephalitis, Graus 2021), and the policy already encodes nivolumab withdrawal (ASCO 2021) and the interactions the concern said were missing.
