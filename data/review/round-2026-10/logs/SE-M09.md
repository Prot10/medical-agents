# SE-M09
Reviewer status: R1 not reviewed, R2 not reviewed (no notes; counted among the R2 approvals per plan) | Approved before this round: yes (per plan)

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | The notes file has no note for SE-M09. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| B | major | `patient.neurological_exam.reflexes`, `cranial_nerves` | With a right SDH and a right temporoparietal NCSE focus, the case had hyperreflexia and an extensor plantar on the RIGHT and ictal gaze deviation to the RIGHT (plan C6). | FIXED: 3+ left, 2+ right, left Babinski. Intermittent eye deviation is now leftward, away from the focus. The left facial droop and left arm drift were already correct. |
| D | minor | `patient.neurological_exam.additional` | "consistent with ongoing NCSE" was the answer, written into the exam. | FIXED: removed; the staring episodes are described without interpretation. |
| A/C | major | `initial_tool_outputs.labs` | Template "Exclusion studies" (ammonia, magnesium, lactate, ABG, tox screen without values) (C1). INR was written "4.8 / CRITICAL" with a three-part range, there was no PT, and no liver tests although a CMP was ordered. | FIXED: block deleted. Magnesium 1.8, chloride 97, liver tests and albumin added (normal), plus lactate 2.3 (H). Coagulation is PT 47.6 s, INR 4.8 and PTT 38 s with plain ranges. The summary and interpretation are a recital. Panel names carry their abbreviations. |
| A/C | major | `action-6-interpret-labs`, `action-9-interpret-labs`, follow-up `request_anticoagulant_reversal` | a6 (coagulation) duplicated the initial labs. Its expected text was a target, not a finding. a9 "Urine culture and treat UTI" was a treatment disguised as an empty lab order. The "Coagulation After Reversal" follow-up reported the INR after 4F-PCC, a treatment effect (ruling 4, plan C4). | FIXED: all three deleted. Coagulation is folded into a2 (T-LABS extra, warfarin). UTI treatment is a must. Reversal and its target are musts and a prohibition [Frontera_2016]. |
| A | major | `action-2-interpret-labs` | It asked for ammonia, AED levels (she takes no ASM), lactate, ABG, tox screen and urinalysis. | FIXED: T-LABS with CBC, CMP, magnesium and coagulation. The urinalysis stays in the report, and the urine study is scored by a10. |
| D | minor | `initial_tool_outputs.ct` | "Neurosurgery consultation recommended" (a referral in a report, style guide). The finding type was "uncal herniation warning". | FIXED: referral removed. Findings now give the density of each component, early uncal herniation and the 8 mm shift. The impression is unchanged in substance. |
| C | minor | `initial_tool_outputs.eeg` | 1.8-2.5 Hz rhythmic sharp waves were called NCSE without the spatiotemporal evolution Salzburg requires at 2.5 Hz or less. The LPDs had "evolving ictal morphology". | FIXED: evolution from 1.5 to 2.5 Hz with spread to C4, in recurrent runs over most of the recording; LPDs described plainly; focal NCSE named. |
| B/D | major | EEG follow-up `request_continuous_eeg_monitoring`, MRI follow-up | The EEG follow-up was a post-operative recording ("NCSE resolved post-SDH evacuation and AED treatment"). The MRI was post-operative ("residual 4 mm collection, midline shift resolved"). Both report the effect of treatment (ruling 4), and the EEG trigger took over the cEEG criterion. The MRI also called the atrophy right-hemispheric "chronic cortical injury" in a woman with Alzheimer's disease, and quoted "Boston criteria: possible CAA", which is wrong: multiple strictly lobar microbleeds with cognitive impairment would be probable CAA under Boston 2.0. | FIXED: EEG follow-up deleted. The MRI is rewritten as the pre-operative study (trigger `request_mri_brain_swi`): acute-on-chronic SDH with 8 mm shift and no infarct, generalized and hippocampal atrophy (MTA 3), Fazekas 3, and strictly lobar microhemorrhages with CAA in the imaging differential, without a Boston grade. |
| C | minor | `action-4-analyze-brain-mri` | MRI was recommended before the urgent evacuation of a 12 mm SDH with herniation. CT is the study that decides acute care. | FIXED: optional (deviation from plan 3.1, see Open questions). Its result informs the later anticoagulation decision. |
| D/C | major | DDI follow-up, a5 | The output carried reversal agents (4F-PCC, vitamin K) and a DOAC recommendation, which is a treatment plan (plan C9). The expected text said the protein-binding displacement "explains INR elevation" and added reversal. Interactions with the ASMs and with lisinopril and donepezil were missing. | FIXED: T-DDI. Warfarin + ibuprofen (platelet, GI, transient displacement, variable INR); ibuprofen + lisinopril (renal); warfarin with phenytoin, valproate and carbamazepine; levetiracetam none; donepezil + phenytoin bradycardia; levetiracetam renal dosing. Required. Leak guard passes. |
| C | major | `assessment.required_recommendations` | There was "Treat UTI" with no agent, a reversal must without a PCC dose or target, levetiracetam without dose or renal adjustment, and no cEEG, analgesic or ACE-inhibitor action. | FIXED: T-MUST-BZD; vitamin K 10 mg IV + 4F-PCC 35 units/kg (INR 4-6, max 3500) with repeat INR and target < 1.4 [Frontera_2016]; T-MUST-2L levetiracetam 60 mg/kg (max 4500), maintenance by CrCl, avoiding fosphenytoin and valproate (warfarin interaction, platelets); evacuation after correction; T-MUST-cEEG; hold warfarin, stop ibuprofen, acetaminophen, hold lisinopril; IV ceftriaxone 1 g daily after culture; anticoagulation decision after evacuation. |
| C | minor | `assessment.prohibited_recommendations` | The INR target "<1.5" was not the Frontera threshold. | FIXED: < 1.4. Added: no FFP when PCC is available [Frontera_2016]. The LP prohibition also names the INR. |
| B | minor | urine culture follow-up | It carried an editorial note ("TMP raises creatinine artifactually"), and the microscopy that was ordered was not reported. | FIXED: plain susceptibilities and a microscopy line. a10 kept required (fever 38.2 C, pyuria, nitrite; no antibiotics yet), placed after the EEG, with case-specific label and expected text. |
| D | major | literature follow-up, a8 | Literature was required. Its output was this case's restart plan ("4-8 weeks", apixaban) and repeated a8's text. | FIXED: optional and last. T-LIT on reversal [Frontera_2016] and on resumption in general terms; trigger renamed. |
| C | major | `ground_truth.differential` | Stroke and UTI delirium were "moderate" after the CT and EEG exclude them (ruling 7). | FIXED: all low, each with the result that excludes it. An "SDH mass effect without seizures" entry was added (the EEG excludes it). |
| A | minor | `sequence_constraints`, `stop_rule`, avoided actions | The labs-before-DDI constraint was hard, with a reason about reversal. The stop rule listed literature and the duplicate a6, with `max_additional_actions` 0. The PSG entry carried the DaTscan rationale. The echo and Holter rationales said "no cardiac comorbidity" in a patient with AF. | FIXED: soft, with the INR and renal reason (C13); stop rule lists the 5 required criteria, max 1; T-PSG; echo and Holter rationales rewritten for known AF; the LP harm rationale names the INR. |
| B | minor | `fallback_tool_outputs` | There were FDG-PET ("Not performed") and neuropsychology fallbacks (C10). The Holter impression read "consistent with known AF on warfarin" (cross-modality). The echo was "near-normal ... benign incidental finding" with a normal LA in AF. The CSF ratio was 0.6 against a serum glucose of 92. | FIXED: advanced_imaging and specialized_test set to null; Holter impression is the rhythm only; echo has a mildly dilated LA and a plain impression; CSF ratio 0.67; `fallback_tool_kinds` updated. |

## Changes, in one paragraph a physician can read before re-reviewing
SE-M09 is unchanged in substance: focal NCSE from an acute-on-chronic right SDH in a 77-year-old woman with Alzheimer's disease on warfarin, with INR 4.8 after 10 days of ibuprofen, a febrile E. coli UTI and Na 130. The signs now match the right-sided lesion: left hyperreflexia and Babinski, and leftward ictal gaze. Everything that reported treatment was removed (INR after PCC, post-operative EEG and MRI). The MRI is now pre-operative and optional; it shows strictly lobar microhemorrhages that matter for the later anticoagulation decision. The labs are a real CMP with PT/INR. The drug check covers warfarin with ibuprofen and with each candidate ASM, ibuprofen with lisinopril, and donepezil. The musts give vitamin K with 4F-PCC to INR < 1.4 before evacuation [Frontera_2016], levetiracetam with renal maintenance, ceftriaxone after the urine culture, and cEEG. The prohibitions forbid LP, FFP when PCC is available, NSAIDs, and early warfarin. Literature is optional and general. The differential is ranked against the results.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: `[ACNS_2021]` and `[Frontera_2016]` are cited and need the allow-list.
- Plan CENTRAL 3b: G41.2 (complex partial SE) is a fair first code for focal NCSE; no change requested.
- Label note: `accepted[0]` says "supratherapeutic warfarin (INR 4.8) from ibuprofen-warfarin interaction". Ibuprofen's effect on the INR is modest and variable (its main hazard is pharmacodynamic), so the label overstates the mechanism. The DDI output states it accurately. A central label edit to "... on warfarin with concurrent ibuprofen (INR 4.8) ..." would be more precise. Not changed here (ruling 3).

## Open questions for Andrea (judgment calls you could not settle)
None open. One deviation from plan 3.1, decided here: MRI is `optional`, not `recommended`. With a 12 mm acute-on-chronic SDH, 8 mm shift and early uncal herniation, the CT decides reversal and evacuation, and an MRI before surgery would only delay them. Its content (lobar microhemorrhages) bears on the later anticoagulation decision, not on the diagnosis.

## Verification
Adversarial verification, 24 Oct 2026. Checked: laterality (right SDH and right T4-P4 NCSE; left hyperreflexia, left Babinski, left drift, left facial droop, leftward ictal gaze) in exam and EEG; removal of every treatment-effect output (post-PCC INR, post-operative EEG and MRI); PCC dose (35 units/kg for INR 4-6, maximum 3500) and INR target below 1.4 [Frontera_2016]; LP harm avoided action against the prohibitions; urine culture required with no antibiotic given before it; MRI optional (deviation from plan, endorsed: CT decides reversal and evacuation in a 12 mm SDH with herniation); drug-check content; differential all low with the excluding result; follow-up order; stop rule; lab flags. Found and changed: chloride 97 (range 98-107) was flagged low in the summary and interpretation but `is_abnormal` was false; now true. Considered and left: "word-finding difficulty" with a right-hemisphere focus in a right-handed woman is explained by her moderate Alzheimer's disease and global encephalopathy, not a laterality error. perfect_agent ok; case guards pass; case_io check clean for this case.

## Close-out (24 Oct 2026)
Decisions in `plans/SE-decisions.md`.
- synonyms: the G41 category no longer grants the type codes G41.0, G41.2 and G41.8 (a type code is granted only by the case's own code, so an answer coded with the wrong SE type no longer scores by code); `apply_diagnosis_synonyms.py --prune --conditions status_epilepticus` removed G41.0 and G41.8 from `ground_truth.diagnosis.icd_codes`. Labels unchanged.
- label (`ground_truth.diagnosis.accepted[0]`): "precipitated by supratherapeutic warfarin (INR 4.8) from ibuprofen-warfarin interaction" -> "on warfarin with a supratherapeutic INR (4.8) and added bleeding risk from concurrent ibuprofen". Ibuprofen raises bleeding risk mainly through platelet COX-1 inhibition and mucosal injury, with a variable and usually modest INR effect (the case's own drug-check output says so), so the label no longer attributes the INR to the NSAID (SE summary CENTRAL 3c).
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, SE case guards pass, `apply_diagnosis_synonyms.py --check --conditions status_epilepticus` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `continuous_icu`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## EEG and labs after routing (25 Oct 2026)

Commit 317e46db routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG) and serves an `interpret_labs` order only the stored panels it names. Decisions for the condition in `plans/SE-routing-decisions.md`.

- EEG: a routine order received the library's normal routine EEG, which contradicts the case. Added `fallback_tool_outputs.eeg` with `eeg_type` `routine` (the stored continuous_icu recording cut to a 30-minute portable recording without video, technologist notes for the clinical events, activation not performed): recurrent right temporal-parietal seizures over most of the record (focal NCSE), LPDs, right hemisphere suppression with diffuse slowing. No criterion, tiers and the reward-relevant policy unchanged; the clinically correct test stays the continuous EEG of `action-1-analyze-eeg`. A `continuous_icu` or `video` order still receives `initial_tool_outputs.eeg`.
- Labs: no SE lab criterion of this case cites a result its own order does not return; no change.
- Checks: `perfect_agent.py -v` pass; `case_io.py check` schema and synonym guard OK, no test failure names the case; probe: routine (omitted and explicit) order -> the new case fallback, `continuous_icu` and `video` -> the stored index recording; every number in each lab criterion's evidence is in what its order returns.

## Matcher fix (25 Oct 2026)

The lab matcher now keeps a urine or CSF row out of a blood order: a urinalysis, urine sodium or urine osmolality row answers only an order that names the urine assay, so a CBC or CMP order no longer returns the urine results. The lab criterion therefore names the urine assays its expected evidence cites.

- `ground_truth.action_criteria[action-2-interpret-labs]`: new first alternative `{panels: ['CBC', 'CMP', 'magnesium', 'coagulation', 'urinalysis']}` (adds `urinalysis`); the previous orders stay as alternatives, so every call that matched before still matches. The expected evidence reads pyuria, nitrite and gram-negative rods, which the first order received only through two matcher defects fixed on 25 Oct 2026: a urine row answered a blood-count or metabolic order (`Urine WBC` as WBC, `Urine sodium` as sodium, a urine creatinine ratio as creatinine), and the unit `mg/dL` read as magnesium. Scoring: cost reference only (the policy's reference order is fuller); coverage unchanged.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although this case contradicts it (diagnosis, history, medications or a stored finding) now get a case-specific report; every other off-pathway order still gets the library normal. No tier, criterion, diagnosis or existing output changed.

- `analyze_eeg eeg_type=ambulatory` -> `followup_outputs[order_ambulatory]`: ambulatory EEG mirroring the stored continuous EEG (no video).
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[order_performance_status]`: performance status KPS 20, ECOG 4 during the admission.
- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `followup_outputs[order_gait_and_balance_timed]`: timed gait not testable, as on the examination.
- `perform_clinical_assessment assessment_type=cognitive_screen` -> `followup_outputs[order_cognitive_screen]`: baseline cognitive screen not testable in the documented mental state.
- `order_specialized_test test_type=neuropsych_battery` -> `followup_outputs[order_neuropsych_battery]`: neuropsychological battery not testable in the documented mental state.
- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: speech and language evaluation not testable in the documented mental state.
- `perform_clinical_assessment assessment_type=cognitive_screen timing=post_intervention` -> `followup_outputs[order_cognitive_screen_post_intervention]`: repeat cognitive screen impaired or not testable, in keeping with the documented dementia or brain injury.
- `labs:lithium_level` -> fallback labs panel `Lithium`: lithium not detected (not prescribed).
- `labs:AED_levels` -> fallback labs panel `Antiseizure medication levels`: antiseizure drug levels: none detected (no antiseizure drug prescribed).
- `labs:valproate_level` -> fallback labs panel `Antiseizure medication levels`: antiseizure drug levels: none detected (no antiseizure drug prescribed).
- `order_advanced_imaging modality=FDG_PET` -> `followup_outputs[order_fdg_pet]`: brain FDG-PET abnormal where the stored MRI shows the lesion.
- `order_advanced_imaging modality=amyloid_PET` -> `followup_outputs[order_amyloid_pet]`: amyloid PET positive in Alzheimer's dementia.
- `order_advanced_imaging modality=tau_PET` -> `followup_outputs[order_tau_pet]`: tau PET positive in Alzheimer's dementia.
- `order_advanced_imaging modality=perfusion_SPECT` -> `followup_outputs[order_perfusion_spect]`: perfusion SPECT: temporoparietal hypoperfusion and the subdural collection.
- `order_echocardiogram echo_type=TEE` -> `followup_outputs[order_tee]`: TEE consistent with the stored TTE.
- `order_echocardiogram echo_type=bubble_study` -> `followup_outputs[order_bubble_study]`: bubble study consistent with the stored TTE.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k SE` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
