# NMDAR-ENC-S04
Reviewer status: R1 not reviewed, R2 not reviewed (no `notes/NMDAR-ENC.md`: condition not reviewed this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | None: condition not reviewed. All changes below are the plan's class fixes (plan section 2, S04 entry) and my own findings. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria` | C1: non-schema `basic` and `screen_for`, exact literature `query`, `protocol: standard`, 11-panel labs list. | FIXED: plan 3.2 arguments (labs A/B with `beta-hCG`; MRI `{contrast: true}`; CSF A/B; EEG routine/video/continuous_icu; `{study: pelvis_abdomen_ultrasound}`; DDI and literature `{}`). |
| D | blocker | `followup_outputs` literature and DDI | C3 placeholder literature and DDI repeating expected_evidence; leak guard failed. | FIXED: canonical literature plus Schmitt 2012; DDI in report voice from her list (progestin-only pill unaffected by non-inducing antiseizure drugs, steroid-albuterol potassium, steroid glucose, aciclovir hydration, additive sedation with melatonin, D2 class warning, HBV before rituximab, cyclophosphamide contraception, penicillin allergy not relevant). Guard passes. |
| C | major | literature and DDI criteria | C2, C10: both `recommended`. | FIXED: both `optional`, `{}`; literature last. |
| B | blocker | `initial_tool_outputs.csf.special_tests`, `.labs.panels` | C4: CSF anti-NMDAR twice in the CSF report and three times in the labs. | FIXED: one CSF `NMDAR_antibodies` final result, once in `interpretation`; CSF entries removed from labs; one serum entry 1:128. |
| B | minor | `initial_tool_outputs.csf` | C17: 75 cells, IgG index 0.91, 5 bands and the titre pair serum 1:128 / CSF 1:256 copied S02 exactly. Ratio 0.61 for 64.7/102 (= 0.63). Opening pressure 24 called "elevated". | FIXED: 31 cells/uL (88% lymphocytes, 8% monocytes, 4% neutrophils), protein 49.6 mg/dL, 3 CSF-restricted bands, IgG index 0.78, CSF titre 1:64 (serum stays 1:128, same doubling series); ratio 0.63; "24 cmH2O". Criterion, key evidence and interpretation follow. |
| D/B | major | `initial_tool_outputs.labs` | C5: leaky `Exclusion studies`, duplicate inflammatory panel, anti-TPO in the autoimmune panel, no beta-hCG. | FIXED: canonical panel set; Sodium stays `BMP[0]` for the red herring; CK `Other[0]`. Plain recital. |
| B | minor | `labs.panels.CBC` Hematocrit, `labs.panels.Other` ANA | Hb 14.1 with Hct 38.6 gives MCHC 36.5; ANA "1:40 (weak positive)" was flagged normal against a "<1:40" reference. | FIXED: Hct 41.8 (MCHC 33.7); ANA `is_abnormal` true and in the summary. |
| B | major | `patient.history_present_illness` | Timeline could not happen: a 5-day prodrome starting 2 weeks before, behaviour change 4 days after recovery (about day -5), yet seizures on days -8 and -6 and "ten days" of behavioural disturbance. | FIXED: prodrome about two and a half weeks before, behaviour change "a few days later" (about day -10), seizures on days -5 and -3. |
| B | minor | `patient.social_history.occupation`, `metadata.case_variant_notes` | "data analyst" living in a university dormitory and attending classes with professors. | FIXED: "graduate student in data science". |
| B | minor | `patient.clinical_history.medications` | Over-the-counter melatonin in the HPI, not on the list; the HPI said "no new medications". | FIXED: melatonin 3 mg nightly listed; HPI "no new medications other than the melatonin". |
| B | minor | `patient.neurological_exam.cranial_nerves` | "Mild right lower facial weakness" while the MRI signal is right insular-opercular and the EEG seizures right temporal. | FIXED: left lower facial weakness. |
| B/D | minor | `initial_tool_outputs.eeg` | The seizures were called "subclinical" although they "occurred during episodes of behavioral arrest"; impression not in ABNORMAL format; limitations prescribed "response to therapy" monitoring. | FIXED: "Three electrographic seizures", clinical correlate behavioural arrest; ABNORMAL numbered impression; limitations "Continuous EEG monitoring recommended." |
| B | minor | `initial_tool_outputs.ecg` | C17: 118 bpm vs vitals 109. | FIXED: 109 bpm. |
| D/C | major | `initial_tool_outputs.body_imaging` | C12 lab-template impression; C17 2.3 cm copied from S02; "internal vascularity present" does not fit a mature teratoma; the prior cyst (PMH) not addressed. | FIXED: 2.8 cm lesion with fat-containing mural nodule and calcification, no vascularity; comparison row (outside ultrasound 2 years ago, no images); radiology impression. |
| C | major | `followup_outputs`, `action_criteria` | C7: cEEG must without a cEEG follow-up. | FIXED: 24 h cEEG follow-up (right temporal, eight seizures, five with behavioural arrest, extreme delta brush); `ceeg-escalation` recommended. |
| C | major | order, `sequence_constraints`, `stop_rule` | C6, C18. | FIXED: canonical order; soft MRI before CSF; five required ids, max 2. |
| D/C | major | `fallback_tool_outputs` | C14: FDG-PET and neuropsychological catch-all fallbacks; Holter average 72 vs HR to 128. | FIXED: null; telemetry 86-128 bpm; `fallback_tool_kinds` updated. |
| C | major | `ground_truth.differential` | C8 template. | FIXED: all `low` with case evidence; neuropsychiatric SLE added (weak ANA, aunt with SLE). |
| C | major | `ground_truth.assessment` | C9 template musts. | FIXED: M1, M2, M3 left teratoma removal, M4 without valproate, M5, M6 ICU (labile BP with diaphoresis, HR to 128, recurrent seizures), M7, M8, M10. Canonical P1, P3. No M9: sodium 133 is mild. |
| C | major | `ground_truth.key_clinical_evidence` | C15 template. | FIXED: six case-specific bullets. |
| B/C | minor | `ground_truth.red_herrings` | Psychiatric data_point listed hallucinations, which the HPI does not describe; hyponatraemia interpretation template; CK "typically >1000". | FIXED: data_point from the HPI; canonical hyponatraemia (graded mild, 133) and CK interpretations. |
| C | minor | rationales, citations | C16. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing
NMDAR-ENC-S04 is a 27-year-old graduate student with all six Graus groups, CSF anti-GluN1 now 1:64 (serum 1:128) and a left ovarian mature cystic teratoma (now 2.8 cm, no vascularity, possibly the cyst seen 2 years ago); label unchanged. The HPI timeline now works (prodrome about 2.5 weeks before, behaviour change about 10 days before, seizures on days -5 and -3), melatonin is listed, and the facial weakness is on the left to match the right-hemisphere MRI and EEG findings. CSF values are no longer a copy of S02, and the glucose ratio, haematocrit and ANA flag are corrected. A 24-hour cEEG follow-up exists and is recommended. The differential is all low, with neuropsychiatric SLE added. Musts follow the canonical set with ICU care for dysautonomia and recurrent seizures. DDI and literature are optional.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: keys used `[Gresa-Arribas_2014]`, `[Herman_2015]`, `[Abboud_2021]`, `[Lejuste_2016]`.
- To the lead: criterion id `ceeg-escalation` (the plan's `cEEG-escalation` fails the schema).

## Open questions for Andrea (judgment calls you could not settle)
None. I decided these myself:
- I changed the CSF titre from 1:256 to 1:64 so that S04 does not repeat the S02 pair (plan C17). Serum above CSF is also the usual relation.
- I kept the family history of SLE, though S02 and S03 also have it. It is plausible, and the differential now addresses it.

## Verification
Checked against the plan (sections 1.2, 2, 3, 4) and the final case file: every own-finding row of the log against the file; criteria order, tiers and minimal arguments (plan 3.2); stop rule (five required ids, max 2) and the soft MRI-before-CSF constraint; one CSF anti-GluN1 key with titre on the same doubling series as serum and no CSF entry in the labs; labs panels, `is_abnormal` flags and plain-recital summaries; laterality across exam, MRI, EEG and cEEG; allergies and medication list against musts and DDI output; musts against prohibitions and avoided actions; differential likelihoods against the results; red-herring data_points against the HPI; literature and DDI outputs for leakage (case guards pass). No reviewer notes exist for this condition, so there is no note id to account for.
The facial-weakness side change (right to left) is correct: the MRI insular-opercular signal and the EEG seizures are right-sided and no other exam sign is lateralised. The HPI timeline now holds (prodrome days -17 to -12, behaviour change about day -10, seizures days -5 and -3). Sodium 133 is mild hyponatraemia, so keeping its red herring without M9 or an SIADH criterion follows the plan.
Found and changed:
- `initial_tool_outputs.ecg.intervals`: PR 152 ms and QTc 448 ms were identical to S02 and S03 (template carry-over). Now PR 158 ms, QTc 436 ms.
`perfect_agent.py -v` and `case_io.py check` clean after the edit.

## Condition audit (24 Oct 2026)

Condition auditor, after the workers and verifiers. Uniformity checks over all 30 cases; changes made here through `case_io` (all re-checked: `perfect_agent.py` 30/30, `case_io.py check` and the case guards clean):
- `ground_truth.assessment.prohibited_recommendations[1]` and `[3]` (B/E, minor): the canonical P2 and P4 texts still carried an em dash before "antibody turnaround" and before "exclude mass effect", and an en dash in "1-2 weeks", while 18 other cases already had the dash-free canonical wording. Now "...high: antibody turnaround can take 1-2 weeks..." and "...new seizures: exclude mass effect first." Meaning unchanged.
