# NMDAR-ENC-M05
Reviewer status: none (condition not reviewed in this round; July 2026 tool review only) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: condition not reviewed | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-2-analyze-csf]` | Non-schema `basic` key: the required CSF criterion was unreachable (C1). | FIXED: `special_tests` alternatives per plan 3.2. |
| A | major | `action_criteria[action-1/4/5/7/8]` | `protocol: standard`, eleven-panel list, `contrast: false`, exact `query`, `screen_for` (C1). | FIXED: minimal arguments (labs without beta-hCG: male); scrotal ultrasound `{study: testicular_ultrasound}`. |
| D | blocker | `initial_tool_outputs.drug_interactions` | Empty block whose summary and contraindication repeated the criterion's expected evidence (C3; guard failing). | FIXED: report voice from his medicines (zopiclone with benzodiazepines, levetiracetam, steroid effects, aciclovir), D2 class warning, HBV screening. Guard passes. Criterion `optional`, `{}`. |
| D | major | `patient.clinical_history.medications` | Zopiclone indication "to be discontinued given likely autoimmune encephalitis" (diagnosis leak); ED levetiracetam loading dose listed as a home medication (C17). | FIXED: prescriber's indication only; levetiracetam moved to the HPI ("In the emergency department he received a 1500 mg IV loading dose of levetiracetam"). |
| A | minor | `patient.age`, `.ethnicity`, `.hpi`, `.occupation`, `.pmh`, `.presenting_complaint`, `.sex` | Stray keys outside the patient schema duplicating the HPI and PMH; social history in one `note`. | FIXED: deleted; social history split into keys; dashes in HPI, PMH and exam replaced. |
| B | blocker | `initial_tool_outputs.csf.special_tests`, `.labs.panels` | CSF antibody "Pending" (two keys) while labs gave the CSF titre 1:80 (C4). | FIXED: `NMDAR_antibodies` "Positive, titre 1:80 (... resulted day 7)"; result in a full interpretation; CSF entries removed from labs. |
| B | minor | `initial_tool_outputs.csf`, `.labs` (C17) | Labs and CSF copied from M04 (Hb 13.1, Hct 40.5 on female ranges, Na 129, CK 148, CRP 0.8, ESR 22; 14 cells, IgG index 0.74) in a man; TSH and free T4 also identical. | FIXED: male CBC (Hb 15.2, Hct 45.1, male ranges), Na 128, Cl 95, HCO3 23, creatinine 0.95, CRP 0.6, ESR 14, TSH 2.4, free T4 1.2, CK 212 (ref 40-200); CSF 21 cells (90% lymphocytes), IgG index 0.79, 4 CSF-restricted bands, glucose ratio 0.63. |
| B | major | `initial_tool_outputs.labs` | Duplicates, "Exclusion studies", one-line autoimmune panel, CSF entries (C5); no osmolality for Na below 130. | FIXED: panels rebuilt per C5 plus serum osmolality 264 (calculated about 266), urine osmolality 388, urine sodium 41. |
| C | major | new criterion `siadh-osmolality-workup` | Moderate hyponatraemia without its work-up. | FIXED: recommended, answered by the labs report. |
| B | major | `initial_tool_outputs.mri.findings`, `.impression` | Findings showed only a left lesion while the impression said "bilateral" and "symmetric" (and left-predominant); impression argued against HSV. | FIXED: right hippocampal finding added (0.9 x 0.5 cm, same signal), impression numbered "bilateral, left-predominant", one hedged sentence. Matches the bitemporal EEG and the red herring "bilateral temporal MRI changes". |
| B | minor | `initial_tool_outputs.eeg` | PDR "6-7 Hz theta" vs finding "5-6 Hz, no PDR"; finding text "more consistent with encephalopathy than primary epilepsy" (diagnostic); impression one line. | FIXED: PDR absent with 5-6 Hz theta; interpretive sentence removed; numbered impression. |
| B | minor | `followup_outputs[0]` (cEEG) | Impression "Subclinical seizures on continuous EEG" outside the template; dash. | FIXED: C7 template (five bitemporal seizures without clinical correlate, no EDB). |
| C | major | `followup_outputs` literature (second-line, aciclovir) | Unsourced results: "2-4 weeks" before escalation, "additional 30-40% of non-responders achieve good outcomes" (not in Titulaer 2013), aciclovir stop rule "course >7-10 days" and "confirm anti-NMDAR antibodies before stopping" (not guideline). | FIXED: kept both topics, optional and last; sourced findings (Titulaer 2013, Abboud 2021 for second-line at about 2 weeks; Solomon 2012 and Venkatesan 2013 for aciclovir). Canonical literature added as `initial_tool_outputs.literature_search` for other queries. |
| D | minor | `initial_tool_outputs.body_imaging.impression` | Lab template "All values within normal limits." | FIXED: "Normal scrotal ultrasound. No testicular mass or microlithiasis." |
| C | major | `fallback_tool_outputs` | Fallback ECG rate 84 and Holter average 76 contradicted HR 112 (C14); FDG-PET and specialized-test fallbacks; `proposed` text. | FIXED: `initial_tool_outputs.ecg` sinus tachycardia 112; telemetry fallback; advanced imaging, specialized test and ECG fallbacks null; `fallback_tool_kinds` updated. |
| C | major | `action_criteria` order, `sequence_constraints`, `stop_rule` | C6, C18. | FIXED: labs, MRI, CSF, EEG, scrotal ultrasound, cEEG, SIADH, DDI, literature; soft MRI-before-CSF; stop rule five ids, max 2. |
| E | minor | `action_criteria[*]` | Rationale = label, citation twins, generic evidence (C16). | FIXED (British spelling). |
| C | major | `assessment.required_recommendations` | Must "testicular ultrasound and contrast-enhanced CT CAP" in a 30-year-old man with a normal scrotal ultrasound; urology/oncology consult for an excluded tumour; "levetiracetam or valproate"; no level of care despite GCS 12 (C9, C11). | FIXED: M1, M2, M3 male negative screen, M4 levetiracetam maintenance or lacosamide, M5, M6 ICU for GCS 12 after recurrent seizures with airway assessment, M7, M8 lorazepam first and stop zopiclone, M9 moderate hyponatraemia (fluid restriction, 10 mEq/L per 24 h limit), M10 neurology with psychiatry. |
| C | minor | `assessment.prohibited_recommendations` | "young patient", dashes. | FIXED: canonical P1-P5. |
| C | major | `ground_truth.differential` | Template, not updated (C8). | FIXED: all `low`; drug entry explains the ankle clonus (no serotonergic drug); LGI1 noted as the other hyponatraemic limbic encephalitis, excluded by the panel. |
| C | major | `ground_truth.key_clinical_evidence` | Template with wrong claims (C15). | FIXED: six case-specific bullets. |
| C | minor | `ground_truth.red_herrings[3]` | "Approximately 35% of cases are male": about 19% in Titulaer 2013 (81% female). | FIXED: "about one in five patients ... was male (Titulaer 2013)". |
| B | minor | `ground_truth.red_herrings[0,1,2,4,5]` | "hallucinations, bizarre behavior" not in the HPI; "Mild hyponatremia (129)"; CK template naming dyskinesias he does not have; HSV interpretation with "cortical ribboning on DWI" and "HSV PCR negative confirms"; zopiclone "with apparent initial improvement" (not in the HPI) and an unsupported hypothalamic claim. | FIXED: data points and interpretations rewritten from the case data (CK now 212). |
| E | minor | `metadata.difficulty_description`, `.difficulty_rationale` | "Antibodies pending", dashes; "6 required tools, 3 red herrings". | FIXED; `last_revised`, `revision_reason`. |

## Changes, in one paragraph a physician can read before re-reviewing

Required work-up in order: serum labs, contrast MRI, CSF, routine EEG, scrotal ultrasound (soft MRI before LP); continuous EEG (five bitemporal electrographic seizures) and the SIADH osmolality set are recommended; DDI and literature optional and last. The CSF report gives the final CSF anti-GluN1 result (titre 1:80) with 21 cells, IgG index 0.79 and 4 CSF-restricted bands; the copied female-range labs were replaced by distinct male values (Na 128 with serum osmolality 264, urine osmolality 388, urine sodium 41; CK 212). The MRI now shows the bilateral left-predominant medial temporal signal its impression described. The levetiracetam loading dose moved from the medication list to the HPI and the zopiclone indication no longer names the diagnosis. Musts: aciclovir, methylprednisolone with IVIG or PLEX, no further tumour imaging after a normal scrotal ultrasound unless the course is atypical, levetiracetam maintenance or lacosamide, cEEG, ICU/neurocritical care for GCS 12 with airway assessment, escalation at 10-14 days, lorazepam first and zopiclone stopped, SIADH treatment with the correction limit, neurology with psychiatry. The CT CAP and urology/oncology musts were removed. Differential all low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used: `[Gresa-Arribas_2014]`, `[Venkatesan_2013]`, `[Herman_2015]`, `[Spasovski_2014]`, `[Abboud_2021]` (plan 5.1).
- `ground_truth.diagnosis.accepted[0]` contains an em dash between "encephalitis" and "tumour-negative (idiopathic), male patient"; left untouched per ruling 3 (label not wrong). The lead may want it reworded centrally.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case against the plan.
- Checked: male ranges and values distinct from M04; osmolality consistent with Na 128 (calculated about 266); levetiracetam moved to the HPI; zopiclone indication clean; MRI findings now bilateral as the impression says; testicular ultrasound criterion and male negative-screen must; ICU must matches GCS 12 per the plan rule; literature follow-ups checked against Solomon 2012, Venkatesan 2013, Titulaer 2013 and Abboud 2021 (correct, sourced, optional, last); NMS/serotonin entry explains the ankle clonus. Checks and guards clean.
- Found: `initial_tool_outputs.csf.opening_pressure` "20 cmH2O (mildly elevated)": 20 cmH2O is within the adult normal range (other cases of the condition call 20 normal).
- Changed: opening pressure label now "20 cmH2O (normal)".
- Accepted as is: label em dash in `diagnosis.accepted[0]` (worker listed it under CENTRAL; ruling 3).
