# NMDAR-ENC-M02
Reviewer status: none (condition not reviewed in this round; July 2026 tool review only) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: condition not reviewed | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-2-analyze-csf]` | Non-schema `basic` key made the required CSF criterion unreachable (C1). | FIXED: `special_tests` alternatives per plan 3.2. |
| A | major | `action_criteria[action-1-...]`, `[action-4-...]`, `[action-5-...]`, `[action-6-...]`, `[action-7-...]` | `protocol: standard`, eleven-panel list, `contrast: false` on ultrasound, exact literature `query`, `screen_for` (C1). | FIXED: minimal arguments (MRI `{contrast: true}`, labs core panels plus beta-hCG with TSH/thyroid alternatives, ultrasound `{study}`, DDI and literature `{}`). |
| C | major | `action_criteria[action-6-search-medical-literature]` | Literature `recommended` (ruling 5). | FIXED: `optional`, last. |
| C | minor | `action_criteria[action-7-check-drug-interactions]` | DDI criterion keyed to methylprednisolone; the real issue is current olanzapine (C10). | FIXED: `recommended`, `{}`, expected evidence on stopping olanzapine and steroid hyperglycemia on metformin. |
| D | major | `followup_outputs[0]` (olanzapine DDI) | Reachable only through an olanzapine-specific trigger, so a check on the acute-plan drugs got the empty fallback; warning quoted the patient's QTc (cross-modality). | FIXED: content moved to `initial_tool_outputs.drug_interactions.general` (served for any drug), rewritten in report voice with every medicine on the list (olanzapine, sertraline, metformin, albuterol, norethindrone, acyclovir), penicillin allergy, D2 class warning, NMS monitoring, HBV screening, benzodiazepine alternatives. Follow-up deleted. |
| C | major | `followup_outputs[1]` (literature) | Graus 2016 misquoted (MRI listed among the probable criteria), "Florance 2009 Neurology, Tumor-negative ..." is not a real title (Florance 2009 is Ann Neurol, paediatric), Titulaer second-line figures misquoted; non-schema result keys. | FIXED: replaced by the canonical literature output as `initial_tool_outputs.literature_search` (Graus 2016, Gresa-Arribas 2014, Titulaer 2013, Schmitt 2012, Lejuste 2016); follow-up deleted. |
| C | major | `followup_outputs`, criterion `ceeg-escalation` (new) | The must required continuous EEG but no cEEG report existed, so an order got the library's normal cEEG, contradicting the routine EEG seizure (C7). | FIXED: cEEG follow-up authored (24 h: moderate slowing, bifrontal GRDA, delta with beta short of EDB, three left temporal seizures, two with behavioral arrest); recommended criterion `ceeg-escalation` (the plan's `cEEG-escalation` is not a valid id: ids must be lowercase). |
| B | blocker | `initial_tool_outputs.csf.special_tests`, `.labs.panels` | CSF antibody "Pending" in two keys while labs gave the CSF titer (C4). | FIXED: one key `NMDAR_antibodies` "Positive, titer 1:32 (... resulted day 5)"; result in the CSF interpretation; CSF entries removed from labs. |
| B | minor | `initial_tool_outputs.csf` (C17) | CSF numbers copied from M01 (12 cells, IgG index 0.72, "2 faint bands") and titer pair 1:80/1:128 identical to M01; glucose ratio 0.61 did not compute (56.8/102 = 0.56). | FIXED: WBC 18 cells/uL (85% lymphocytes), IgG index 0.81, 3 CSF-restricted OCB, ratio 0.60 against the lab serum glucose 94; CSF titer 1:32 and serum titer 1:160 (CSF below serum, as usual). |
| B | major | `initial_tool_outputs.labs` | Duplicates, "Exclusion studies", "Reviewed inflammatory markers", CSF entries (C5); chloride 108 with Na 136 and HCO3 24 gives an anion gap of 4. | FIXED: panels rebuilt per C5 (incl. beta-hCG negative, onconeural panel, HIV, ANA, prolactin kept); chloride 102 (normal). |
| B | minor | `patient.clinical_history.social_history.occupation` | "marketing analyst" while the HPI describes her school and students (template carry-over). | FIXED: "high school teacher" (one field instead of two HPI sentences). |
| B | minor | `patient.clinical_history.medications` | Sertraline 50 mg though increased to 100 mg; olanzapine 5 mg nightly (started 5 days ago) missing. | FIXED: sertraline 100 mg; olanzapine added. |
| D | minor | `initial_tool_outputs.mri.impression` | HSV reasoning prose. | FIXED: numbered modality-pure impression with one hedged sentence (limbic encephalitis or post-ictal change). |
| B | minor | `initial_tool_outputs.eeg` | "Possible" seizure in findings vs "electrographic seizure" in the impression; "epileptogenic"; prose. | FIXED: 12-second electroclinical seizure during behavioral arrest; numbered "This is an ABNORMAL EEG due to:" impression with the delta-beta pattern short of EDB. |
| D | minor | `initial_tool_outputs.body_imaging` | Lab template impression "All values within normal limits."; left 1.2 cm "hypoechoic area". | FIXED: normal radiology impression; the area described as an anechoic thin-walled follicle or simple cyst. |
| B | minor | `initial_tool_outputs.ecg` | QTc 452 ms called "mildly prolonged" (borderline for a woman); interpretation omitted the rhythm. | FIXED: "Sinus tachycardia, rate 104. Borderline QTc (452 ms)." |
| C | major | `fallback_tool_outputs` | Holter "normal, average 69" vs HR 85-118; FDG-PET and neuropsychology fallbacks served for any modality/test; `proposed` engineering text (C14). | FIXED: telemetry fallback with tachycardia to 118; advanced imaging and specialized test fallbacks null; `proposed` emptied; `metadata.fallback_tool_kinds` updated. |
| C | major | `action_criteria` order, `sequence_constraints`, `stop_rule` | C6, C18. | FIXED: labs, MRI, CSF, EEG, ultrasound, cEEG, DDI, literature; soft MRI-before-CSF; stop rule five required ids, max 2. |
| E | minor | `action_criteria[*]` | Rationale = label; citation twins; generic evidence (C16). | FIXED. |
| C | major | `assessment.required_recommendations` | Template musts (diagnostic CSF must, valproate option, CT screening, conditional consults); no instruction to stop olanzapine (C9). | FIXED: M1, M2, M3 negative screen (woman under 45), M4 (avoid valproate), M5, M6 ward (no ICU features: alert, HR to 118), M7 with fertility discussion, M8 lorazepam and stop olanzapine with CK and temperature monitoring, M10 neurology with psychiatry. |
| C | minor | `assessment.prohibited_recommendations` | "young patient" wording, dashes. | FIXED: canonical P1-P5. |
| C | major | `ground_truth.differential` | Template, not updated (C8). | FIXED: all `low`; the drug entry states olanzapine 5 days, temperature 37.7 C, CK 200 U/L, no lead-pipe rigidity, no clonus. |
| C | major | `ground_truth.key_clinical_evidence` | Template with wrong claims (C15). | FIXED: six case-specific bullets (five Graus groups). |
| B | minor | `ground_truth.red_herrings` | "previously well young adult" (she has an anxiety disorder); CK interpretation "CK typically >1000". | FIXED per C15; CK red herring now names the olanzapine exposure. No hyponatremia red herring (Na 136). |
| E | minor | `metadata.difficulty_rationale`, `.moderate_features` | "7 required tools"; "pathognomonic extreme delta brush"; "pending antibody results". | FIXED; `last_revised`, `revision_reason` updated. |

## Changes, in one paragraph a physician can read before re-reviewing

Required work-up in order: serum labs, contrast MRI, CSF, routine EEG, pelvic ultrasound (soft MRI before LP); continuous EEG (new report: three left temporal seizures, extreme delta brush absent) and the drug-interaction check are recommended, literature optional. The CSF report now gives the final CSF anti-GluN1 result (positive, 1:32) with a lymphocytic pleocytosis of 18 cells/uL, IgG index 0.81 and 3 CSF-restricted bands; the serum titer is 1:160; labs were regrouped (beta-hCG negative, onconeural and neuronal-surface panels negative) and chloride corrected to 102. The medication list now shows sertraline 100 mg and olanzapine 5 mg, and the occupation matches the HPI (teacher). The interaction check is in report voice, available for any drug, and tells the agent to stop olanzapine. The fabricated literature follow-up was replaced by the canonical evidence. Musts: acyclovir, methylprednisolone with IVIG or PLEX, negative-screen tumor surveillance, levetiracetam or lacosamide without valproate, cEEG, ward admission with cardiac monitoring, escalation at 10-14 days, lorazepam first with olanzapine stopped and CK/temperature monitored, neurology with psychiatry. Differential all low with the NMS values.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used: `[Gresa-Arribas_2014]`, `[Venkatesan_2013]`, `[Herman_2015]`, `[Lejuste_2016]` (plan 5.1).
- Plan section 2 C7 names the new criterion id `cEEG-escalation`, which fails the criterion-id pattern `^[a-z][a-z0-9_.-]*$`; this case uses `ceeg-escalation`. The lead may want the plan corrected so every worker uses the same id.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case against the plan.
- Checked: all FIXED rows present (CSF numbers distinct from M01, ratio 56.8/94 = 0.60, chloride 102, olanzapine and sertraline 100 mg on the list, occupation, DDI content moved to the any-drug output and agreeing with the penicillin allergy, cEEG follow-up consistent with the routine EEG, five Graus groups supported by the exam, NMS entry values match vitals and labs, ECG 104 within 5 of HR 100). Checks and guards clean.
- Found: (1) the M8 must said "agitation, insomnia and catatonia" but she has no catatonic sign (template carry-over); (2) ANA 1:80 with a maternal aunt with SLE, a mimic absent from the differential (ruling 7).
- Changed: `assessment.required_recommendations` M8 now "Treat agitation and insomnia with benzodiazepines (lorazepam) first; stop olanzapine and monitor CK and temperature."; added differential entry "Neuropsychiatric systemic lupus erythematosus" (low).
