# MS-RR-RP05
Reviewer status: R1 not reviewed, R2 not reviewed (no MS-RR notes file this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.key_clinical_evidence[6]`, `followup_outputs` | KCE cited reduced RNFL on OCT and a prolonged P100 on VEP that no tool served (class R). | FIXED: OCT follow-up (left pRNFL 71 um, temporal 44 um, GCIPL 63 um; right 95/80 um; no macular oedema) and VEP follow-up (left P100 131 ms, right 106 ms); optional `action-oct`, `action-vep`. |
| B | major | `patient.neurological_exam.sensory`, `history_present_illness` | Right leg weakness and Babinski with right pinprick loss: no single cord lesion explains ipsilateral pyramidal and spinothalamic loss, while the spine shows a right T6-T7 lateral column lesion; "band-like" numbness from mid-thigh distally. | FIXED: partial right hemicord pattern (right light touch, vibration and proprioception loss; left leg pinprick and temperature loss; no truncal level); HPI says numbness of the right leg from mid-thigh down. Spine lesions described as lateral and dorsal columns. |
| B | minor | `patient.history_present_illness` | Patient named ("Mr. Derrick Barnes"); "controlled vascular risk factors" with BP 158/94 and HbA1c 7.4%. | FIXED: name removed; "controlled" deleted. |
| C | major | `ground_truth.key_clinical_evidence` | "DIS across periventricular, juxtacortical, infratentorial and cord ... DIT by enhancing lesions" without the F4 point; "OCB present in ~95% of MS"; "three regions"; engineering "July 2026" lines; DMT choice lines. | FIXED: six observable lines: syndrome and prior episodes, DIS 5 of 5 regions, the age-over-50 additional evidence (cord lesions and positive CSF), coexisting small-vessel lesions, mimic exclusion, B12/homocysteine and vitamin D. |
| D | major | `initial_tool_outputs.mri.impression`, `.recommended_actions` | Impression ended with a differential sentence; report recommended the spine MRI (next-step leak). | FIXED: five numbered findings with one hedged read; recommendation removed. The hedged observation on the deep lesions is kept (red herring). |
| D | minor | `initial_tool_outputs.csf` | Myelin basic protein (F6); no kFLC; glucose ratio with an explanation; recital interpretation. | FIXED: MBP deleted; kFLC index 27.5 (reference <6.1); CSF ACE given a value; pattern interpretation. |
| D | minor | `initial_tool_outputs.labs` | AQP4/MOG reported in the interpretation without rows; abnormal summary with causal labels; ESR/CRP filed as "Vascular risk markers". | FIXED: Neuroimmunology panel with the two CBA rows (significance null); plain summary and interpretation; panel renamed "Inflammatory and other markers". |
| D | minor | `followup_outputs` spine | Lesion rows with empty descriptions; the cervical lesion was "left lateral column" in findings and "lateral and dorsal" in the impression. | FIXED: descriptions with position, enhancement and cross-section; columns consistent; no-compression observation added. |
| A | major | `ground_truth.action_criteria` | Template criteria: literature with a long query required, drug check with non-schema keys required, labs with 9 analytes, CSF optional with three assays. | FIXED per plan A2-A8 and tier table: brain MRI, spine MRI, labs `[CBC, vitamin_B12, TSH, HIV]` and `action-aqp4-mog-cba` required; CSF two alternatives recommended (F4); VEP, OCT optional; drug check `{}` recommended; literature `{}` optional last. |
| A | minor | `ground_truth.stop_rule`, `sequence_constraints` | Literature and drug check required before assessment, max 0; constraint cited McDonald 2017. | FIXED: brain MRI, spine MRI, labs, AQP4/MOG; max 3; soft MRI-before-CSF with the canonical reason. |
| C | major | `followup_outputs` drug check | "Amlodipine + fingolimod: additive bradycardic effect" (false, F11); "metformin + dimethyl fumarate ... both depend on renal clearance"; class-level DMT screen not tied to the immediate decision. | FIXED: check of the methylprednisolone pulse against metformin (hyperglycaemia, capillary glucose, correction insulin, fall on stopping), hydrochlorothiazide (potassium), amlodipine (blood pressure) and atorvastatin; infection screen; oral methylprednisolone and PLEX as alternatives. |
| D | major | `followup_outputs` literature | Kis 2008 cited with a wrong title; Reich 2018 and MAGNIMS 2016 summaries with case-like claims (OCB ~95%); 2017 framing. | FIXED: Montalban 2025, Kis 2008 J Neurol with its real title, Geraldes 2018 Nat Rev Neurol; general summary; last in the pathway. |
| C | major | `ground_truth.differential` | Small-vessel disease "high", NMOSD and vasculitis "moderate" after a work-up that argues against them (ruling 7); spinal cord infarction, compressive myelopathy and syphilis absent although the history raises them. | FIXED: all low with the case's results (small-vessel disease noted as probably coexisting for the deep lesions); cord infarction, compressive myelopathy, neurosyphilis added; B12 ICD E53.8. |
| C | major | `ground_truth.assessment.required_recommendations` | Ten musts, mostly diagnostic steps (DIS, DIT, morphology, AQP4 test, JCV test); generic IVMP "once the diagnosis is established" with no glucose plan in a diabetic; "supplement vitamin D" without a value. | FIXED: seven musts: formulation with the F4 evidence; relapse pulse after excluding urinary infection with glucose and potassium plan; post-void residual for the urgency; DMT by activity with infection risk; pre-DMT screening; vascular risk optimisation with values; vitamin D replacement and methylmalonic acid for the low-normal B12. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Natalizumab JCV prohibition with no anti-JCV result; fingolimod prohibition based on the false amlodipine claim. | FIXED: JCV prohibition deleted; fingolimod/S1P prohibition tied to treated sleep apnoea and diabetic macular oedema risk; small-vessel and left eye prohibitions reworded to the case; T7, T11, T12, T13 kept. |
| C | minor | `ground_truth.avoided_actions[*]` | Generic rationales; McDonald 2017, MAGNIMS 2016, Reich 2018 citations. | FIXED: case-tied rationales; `[Wattjes_2021]` for CT, none for EEG, echo, monitoring. |
| B | minor | `ground_truth.red_herrings` | Em dashes, "concurrent MS" framing, B12 data point in two clauses. | FIXED: rewritten in the case's terms; field paths unchanged. |
| B | minor | `metadata.difficulty_description`, `difficulty_rationale` | Described OCB as "the adjudicator" and "6 required tools". | FIXED: rewritten. |
| E | minor | `fallback_tool_outputs.echo` | `echo_type` missing. | FIXED: `TTE`. |
| E | minor | patient fields, CT and ECG fallbacks | Em dashes. | FIXED: replaced. |

## Changes, in one paragraph a physician can read before re-reviewing

This is late-onset relapsing-remitting MS at 54 in a man with hypertension, diabetes, dyslipidaemia and 18 pack-years. The exam now fits the spine MRI: a right T6-T7 lateral and dorsal column lesion gives right leg weakness, a right Babinski and right dorsal column loss with left leg pinprick loss, and an enhancing left C4-C5 lesion explains the Lhermitte sign. The OCT (left pRNFL 71 um) and VEP (left P100 131 ms) the evidence cited are now served, and they confirm that the left eye episode 8 months ago was an optic neuropathy, not hypertensive retinopathy. Lesions are in five regions. Because of his age and vascular risk, the evidence states the additional support the 2024 criteria advise: two cord lesions and positive CSF (six restricted bands, kFLC 27.5). CSF is recommended. AQP4/MOG CBA is required and negative. The punctate deep lesions are described as probably coexisting small-vessel disease. The drug check is recommended and now covers what matters before the steroid pulse: hyperglycaemia on metformin, potassium on hydrochlorothiazide and blood pressure. The false amlodipine-fingolimod bradycardia claim is gone. Musts:
- diagnosis by the 2024 criteria with the age-related evidence;
- methylprednisolone after excluding urinary infection, with a glucose and potassium plan;
- post-void residual;
- high-efficacy DMT by activity;
- pre-DMT screening;
- blood pressure, LDL and HbA1c optimisation;
- vitamin D replacement and methylmalonic acid for the low-normal B12.

The differential lists small-vessel disease, cord infarction, NMOSD, MOGAD, PACNS, B12 deficiency, compression, syphilis and sarcoidosis, all low with reasons.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]`, `[Petzold_2017]` to the MS-RR criteria pack (plan 5.1).
- Diagnosis synonyms: G35.B/G35.C and "demyelinating disease" (plan Q, 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- None needing Andrea's information. Decided: the sensory exam was changed to a partial right hemicord pattern (left leg pinprick loss) so it matches the right T6-T7 lesion. The HPI's right-leg numbness and paraesthesias are kept as dorsal column symptoms. The earlier right hand episode is kept as history only: no current lesion is named as its cause, and the diagnosis does not depend on it. The drug check covers the steroid pulse, as the plan asks (steroids with metformin), not the DMT class.
