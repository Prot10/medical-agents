# VASC-DEM-M05
Reviewer status: R1 not reviewed, R2 not reviewed (VASC-DEM has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | VASC-DEM was never annotated; no note ids exist for this case. All changes below come from the condition plan and my own reading. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `action_criteria[action-4-analyze-brain-mri].alternatives` | Plan C1: non-schema `sequences` key. | FIXED: `analyze_brain_mri {}`. |
| D | major | `action-9-search-medical-literature`, literature initial and fallback | Plan C2 leak. | FIXED: criterion deleted; initial null; fallback deleted. |
| D | major | `patient.history_present_illness` | Timeline leak: the HPI gave "His HbA1c is 8.2%", the result of the required lab panel. | FIXED: "His diabetes has been poorly controlled for some years"; em dash in the rewritten sentence replaced by a colon. |
| D | major | `patient.neurological_exam.mental_status` | Plan C4: MoCA and item losses in the exam. | FIXED: bedside observation (orientation, repeats questions), screening reported separately. |
| B | major | `initial_tool_outputs.clinical_assessment.findings`, `.impression`, `.criteria_met` | MoCA arithmetic: the listed losses (serial sevens 1/3, clock 1/3 and the rest) give 15/30, not 17 (13 years, no correction); impression argued the diagnosis ("suggests an underlying degenerative process with a superimposed vascular step"); `onset_within_3_months_of_stroke` and `pre_existing_decline_documented` are history, not test results. | FIXED: item-level findings with serial sevens 2/3 and clock 2/3 (13 points lost = 17/30); impression lists scores; the two history keys removed. |
| B | minor | `initial_tool_outputs.mri.findings[0].location`, HPI | Mild right leg weakness, increased tone and an extensor plantar are not explained by a pure VPL (sensory) lacune. | FIXED: lacune located in the left VPL "abutting the posterior limb of the internal capsule" (a thalamocapsular sensorimotor lacune); the VPL-versus-amnesia teaching point is unchanged. |
| D | major | `initial_tool_outputs.mri.impression`, `.additional_observations`, `.volumetrics` | Plan C5: "explain the sensory deficit and part of the dysexecutive impairment; the atrophy pattern indicates a coexisting degenerative process", "Two patterns coexist", nucleus explanation. | FIXED: numbered STRIVE-2 impression (index lacune, two lacunes, Fazekas 2, MTA 3 with temporoparietal atrophy, no microbleeds); MTA stated against the age cut-off. |
| D | major | `initial_tool_outputs.csf.interpretation`, `.special_tests` | CSF report gave the integrated diagnosis ("the diagnosis is mixed Alzheimer and vascular dementia") with cross-modality reasoning. | FIXED: values with "low" / "raised" flags only; dashes removed. |
| D | major | `initial_tool_outputs.specialized_test.impression`, `.quantitative_data` | Neuropsych attributed each pattern to a pathology ("points to hippocampal-diencephalic degeneration", "points to the vascular burden"). | FIXED: percentiles and a "Profile:" sentence. |
| D | minor | `initial_tool_outputs.ecg.findings[2]`, `.interpretation`; `initial_tool_outputs.advanced_imaging.impression` | ECG cited the admission telemetry and "the small-vessel (lacunar) mechanism established during the admission"; duplex "The lacunar mechanism stands." | FIXED: ECG read only (telemetry moved to `past_medical_history[0]` as history); duplex grades only. |
| B | major | `initial_tool_outputs.labs` | Plan C6: female Hb/Hct ranges in a man; creatinine 1.14 at 79 gives an eGFR of about 65, not 58; template values; interpretation with targets and "excluding reversible causes". | FIXED: male ranges, Hb 14.1, Hct 42.0; creatinine 1.24 (flagged) consistent with eGFR 58 (flagged, range ">=60"); WBC 7.6, Plt 214, MCV 87, Na 138, K 4.7, ALT 24, albumin 3.9, folate 8.7; summary rebuilt; "Flagged: ..." interpretation. |
| C | major | `action_criteria[action-8-analyze-csf]`, `followup_outputs[0]` | Plan C9: the biomarker step could only be met by CSF. | FIXED: criterion (id kept) with two alternatives, CSF special tests or `order_advanced_imaging` amyloid_PET; new positive florbetaben PET follow-up (Centiloid 74, binary read without disease name). Soft MRI before CSF added. |
| C | minor | `action-10-check-drug-interactions`, `initial_tool_outputs.drug_interactions`, `fallback_tool_outputs.drug_interactions` | Plan C3 group O: generic optional check and a false "no prohibitive interaction" fallback. | FIXED: optional `{}` kept; case-specific outputs keyed `donepezil` (no interacting drug; bradycardia monitoring) and `gliclazide` (perindopril potentiates sulfonylurea hypoglycaemia; eGFR 58; Beers; low-risk alternatives); fallback deleted. |
| D | minor | `fallback_tool_outputs.advanced_imaging`, `.labs`, `.ct`, `.echo` | Plan C7. | FIXED: two deleted; CT fallback shows this patient's lacunes, white matter change and medial temporal atrophy; echo `echo_type` TTE and descriptive impression. Holter fallback kept. |
| A | minor | `action_criteria[*]` | Plan C13. | FIXED: case-specific rationales and evidence; carotid criterion label and rationale say it was done at admission (optional kept). |
| B | minor | order, `stop_rule` | Plan C16. | FIXED: screen, neuropsych, labs, MRI, ECG, carotid, biomarker, drug check; stop rule = screen, labs, MRI, biomarker; `max_additional_actions` 1. |
| B | minor | `avoided_actions` | Plan C18. | FIXED: CT canonical; EEG, echo and monitoring rationales name his reasons (lacunar, telemetry and ECG in sinus). Echo and monitoring waste kept (plan: worked up at admission). |
| C | major | `ground_truth.assessment.required_recommendations` | Musts were diagnostic steps ("Take an informant history", "Test recognition memory", "Read the MRI") with generic management. | FIXED: explain mixed dementia [VASCOG_2014]; cholinesterase inhibitor for the AD component with titration and pulse checks; stop gliclazide, HbA1c about below 8.0% [ADA_2025_older_adults]; continue clopidogrel; BP below 130/80 from 150/82 with orthostatic checks; LDL below 70 (92 on rosuvastatin 20, carotid plaque); carer support, medicines supervision, gas safety, advance care planning. |
| C | minor | `prohibited_recommendations[2]` | Ambiguous wording ("at an HbA1c target that risks hypoglycaemia"). | FIXED: "Do not continue a sulfonylurea in a patient who cannot reliably recognise or report hypoglycaemia [ADA_2025_older_adults]". |
| C | major | `ground_truth.differential[0]`, `[1]` | Plan C8: both "alone" entries `moderate`. | FIXED: both `low`, features cite "amyloid biomarker" (either route). |
| B | minor | `red_herrings[0]`, `key_clinical_evidence[0]` | Referred to "a positive CSF profile" only; empty field path. | FIXED: "positive amyloid biomarker"; field path `patient.clinical_history.past_medical_history[0]`. |
| E | minor | `diagnosis.accepted[0]` | Em dash in the label. | FLAGGED only (ruling 3). |
| - | check | plan 3.6 | perfect_agent ok; probe: both biomarker alternatives answered by case data (CSF initial, PET follow-up); drug alternatives by the keyed outputs; CT by the case fallback; `case_io.py check` and test_case_guards list no failure naming M05. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The case stays mixed Alzheimer and vascular dementia in a 79-year-old man with two years of amnestic decline before a left thalamic lacune 11 weeks ago. The HPI no longer gives the HbA1c, and the lacune now abuts the internal capsule, which explains the mild right leg weakness and extensor plantar. Reports describe only their modality (CSF values without "the diagnosis is mixed", MRI with the STRIVE-2 grades and MTA 3, neuropsychology as a profile); the MoCA items now add up to 17/30, and creatinine was set to 1.24 so that eGFR 58 is arithmetically right. Amyloid status can be established by CSF or by a positive amyloid PET. The drug check is optional but now case-specific (gliclazide with perindopril and eGFR 58; donepezil). Musts: explain mixed dementia, cholinesterase inhibitor, stop gliclazide with an individualised HbA1c, continue clopidogrel, BP below 130/80, LDL below 70, carer and safety measures. Both "alone" alternatives are low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms (plan 5.1): this case's accepted list grants bare "vascular dementia", "multi-infarct dementia" etc. to a mixed-dementia label; add the mixed-dementia entry and stop crediting bare vascular dementia here.
- New citation key `[ADA_2025_older_adults]` (plan 5.4).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. Checked: MoCA arithmetic (13 lost, 17/30, 13 years); HPI no longer gives the HbA1c; lacune relocated abutting the posterior limb explains right leg weakness, tone, extensor plantar and circumduction while the VPL teaching point stands; C9 biomarker criterion (required, CSF initial and florbetaben PET follow-up both positive and consistent, soft MRI before CSF); group O drug outputs (perindopril-sulfonylurea hypoglycaemia, eGFR 58, donepezil pulse monitoring) agree with the medication list; creatinine 1.24 consistent with eGFR 58 at 79; male ranges; LDL below 70 justified by the carotid plaque; gliclazide must vs prohibition consistent; echo and monitoring waste kept per plan (lacunar, telemetry); both "alone" entries low.

Found: nothing that needed a change. No edits.

perfect_agent ok; `case_io.py check` and test_case_guards list no failure naming M05.

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `initial_tool_outputs.labs.panels.Vascular_risk[Total cholesterol]` | Total cholesterol 176 mg/dL did not equal LDL + HDL + TG/5 (169.4); the same lab-arithmetic class was fixed in M07-M10, P01, P02 and S06-S11 but not here. | FIXED: total cholesterol 169 mg/dL (flag unchanged; LDL, HDL and TG, which the musts and evidence quote, unchanged). |
| C | minor | `ground_truth.avoided_actions[avoid-waste-3-order-advanced-imaging].rationale`, `[avoid-waste-4-interpret-labs].rationale` | Plan C18: the MIBG and paraneoplastic/autoimmune rationales were still the August template text shared by M01-M06; the autoimmune one described "a chronic stepwise decline with a hypertensive imaging burden", which is wrong for this case. | FIXED: case-specific one-liners (no Lewy features; slow decline with one stroke-related step). |
| D | major | `initial_tool_outputs.clinical_assessment.criteria_met` | Plan 1.2 and C5 (no report states the severity): the screen's structured fields still carried independence_in_iadl_lost, i.e. the mild-versus-major threshold, the profile verdict or history items. Workers removed these keys in the other 19 cases; here they survived (the P03 worker flagged the question for a condition-wide decision). | FIXED: keys removed; `criteria_met` keeps domain impairment and cue-responsive recall. The informant FAQ score stays in the report as an instrument score. |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here mixed-dementia labels and F00.2 only; generic F01 entry excluded. A vascular-only answer ("vascular dementia", "VaD") no longer scores; accepted: "mixed dementia", "alzheimer vascular dementia" (both spellings), "alzheimer cerebrovascular disease" (both spellings). Code-alone limitation: an answer coded F01.50 still matches (CENTRAL).
- `ground_truth.diagnosis.accepted[0]`: em dash replaced by a colon or semicolon; wording and entity unchanged (no scoring effect: matching ignores punctuation).
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- `[ADA_2025_older_adults]` -> `[ADA_older_adults_2026]` in the HbA1c must (same target below about 8.0%; superseded edition, as in ALZ-EARLY).
- Lipid must: "Intensify lipid lowering to LDL below 70 mg/dL (current 92 mg/dL on rosuvastatin 20 mg, with carotid plaque), adding ezetimibe or increasing the statin [AHA_ASA_2021_secondary]." -> "Intensify lipid lowering to LDL below 55 mg/dL (current 92 mg/dL on rosuvastatin 20 mg, with carotid plaque): very high risk after an ischaemic stroke at 79 with hypertension and diabetes; add ezetimibe or increase the statin [ACC_AHA_dyslipidemia_2026]." Reason: the 2026 ACC/AHA multisociety dyslipidemia guideline (supersedes the 2018 cholesterol guideline on which the AHA 2021 LDL-below-70 figure rests) sets LDL below 55 mg/dL for clinical ASCVD at very high risk (two major ASCVD events, or one plus two or more high-risk conditions).
- `metadata.revision_reason`: the stale August literature/interaction audit text replaced by the round's (summary CENTRAL 9; not read by the harness).
- `metadata.fallback_tool_kinds`: ct normal->case (the fallback describes this patient, not a library normal; summary CENTRAL 9).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
