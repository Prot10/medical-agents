# VASC-DEM-S07
Reviewer status: R1 none, R2 none (VASC-DEM was never reviewed; no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No notes file exists for VASC-DEM. The condition plan's classes (C1-C19) were applied as class rulings (ROUND_POLICY ruling 2); every change is listed under Own findings. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A/C | blocker | ground_truth.action_criteria[action-4-analyze-brain-mri].alternatives | Non-schema `sequences` plus `protocol`/`contrast`: no real call could match (C1) | FIXED: `analyze_brain_mri {}` |
| D | major | ground_truth.action_criteria[action-9-search-medical-literature], initial_tool_outputs.literature_search, fallback_tool_outputs.literature_search | Literature criterion leaking its expected evidence into its own output (C2, ruling 5) | FIXED: criterion deleted, initial output null, fallback deleted |
| C/D | major | ground_truth.action_criteria[action-10-check-drug-interactions], initial_tool_outputs.drug_interactions, fallback_tool_outputs.drug_interactions | Optional `{}` check with generic text; generic "no prohibitive interaction" fallback while aspirin must be stopped when the DOAC starts (C3 group R) | FIXED: recommended; alternatives apixaban, rivaroxaban, edoxaban, dabigatran, warfarin; one output per drug (aspirin combination, label dosing rules, olmesartan/amlodipine/atorvastatin no interaction, sulphonamide allergy no cross-reactivity); fallback deleted |
| D | major | patient.neurological_exam.mental_status | MoCA total and items given upfront (C4) | FIXED: bedside observation; "No neglect on bedside cancellation" kept (an exam sign, not the screen) |
| B | major | initial_tool_outputs.clinical_assessment | MoCA 21/30 not derivable: the listed losses (trail, cube, digits backward, serial sevens, recall 2, orientation 1) total 7, giving 23/30; criteria_met carried IADL loss and stepwise course; impression "understating the decline", "neglect has resolved since the index stroke" (C4, C5) | FIXED: itemised by section with clock 2/3 and letter fluency 0/1 added (losses 3+2+1+2+1 = 9, 21/30); criteria_met keeps domain impairment and cue-responsive recall; impression gives total, losses, cueing, fluency, GDS |
| B | minor | initial_tool_outputs.specialized_test.findings[Bells] | Bells cancellation 2 omissions flagged abnormal against "0-1" while the bedside exam finds no neglect (Bells: 6 or more omissions suggest neglect) | FIXED: "2 omissions (both in the left field)", range "fewer than 6 omissions", abnormal no; impression "No neglect on cancellation" |
| D | major | initial_tool_outputs.specialized_test.impression | "The unevenness fits multiple discrete infarcts" (C5) | FIXED: profile only; premorbid estimate added to quantitative_data |
| B | major | initial_tool_outputs.cardiac_monitoring.findings, impression; ground_truth.red_herrings[0] | AF burden 4.9% impossible: the four episodes total 5 h 21 min over 26 analysed days (0.9%); impression "the embolic source ... converts management" (C5) | FIXED: burden 0.9% with the total duration; impression states episodes, longest, burden, symptom correlation; red herring text no longer quotes 4.9% |
| B | minor | initial_tool_outputs.mri.findings[1] | Left occipital infarct "including the calcarine lip" with full fields on confrontation and quadrant testing | FIXED: left lateral occipital cortex, calcarine cortex spared (the transient right-field blurring is the ischaemic event; the residual infarct is extrastriate). CT fallback uses the same anatomy |
| B | minor | initial_tool_outputs.mri.volumetrics.infarct_count, findings[2] | "Three chronic infarcts ... plus a left thalamic lacune" (four) while three lesions are listed | FIXED: two cortical plus one lacune; finding typed Lacune with its PCA perforator territory |
| D | major | initial_tool_outputs.mri (additional_observations, impression) | "the pattern of a proximal embolic source", "relevant to the safety of anticoagulation", "accounts for the episode misattributed to migraine", "supports the safety of anticoagulation" (C5) | FIXED: STRIVE-2 numbered impression; one hedged "suggestive of an embolic mechanism" kept (Kind 2) |
| D | major | initial_tool_outputs.ecg.interpretation | Essay on atrial cardiopathy and "the search must continue" (C5) | FIXED: rhythm, ectopy, LVH, no acute change |
| D | major | initial_tool_outputs.advanced_imaging.impression | "A large-artery mechanism is excluded, which strengthens the case for an occult cardioembolic source" (C5) | FIXED: per-side plaque, grade and PSV; PSV added to quantitative_data |
| B | major | initial_tool_outputs.labs | Template values (WBC 6.8, Hb 13.9, Hct 41.6, Plt 238, MCV 88, Na 139, K 4.2, ALT 22, albumin 4.1, folate 11.8); HDL range ">40" in a woman; eGFR ">60"; LDL 116 not derivable from TC 208, HDL 52, TG 132 (Friedewald 130); interpretive text on targets and anticoagulant dosing (C6) | FIXED: WBC 5.9, Hb 13.1, Hct 39.4, Plt 264, MCV 90, Na 140, K 4.0, ALT 17, albumin 4.0, folate 13.4; HDL 66 with range ">50" (208 - 66 - 132/5 = 116); eGFR ">=60" (creatinine 0.86 gives about 71-72 by CKD-EPI 2021, unchanged); flag-only interpretation |
| C | minor | patient.physical_exam | No weight for DOAC dosing | FIXED: "Weight 70 kg, height 165 cm" (BMI 25.7, matches 25.6; Cockcroft-Gault about 64 mL/min) |
| B/D | major | fallback_tool_outputs (advanced_imaging, labs, ct, echo) | "non-contributory" fallbacks; CT "better characterised on the MRI already obtained"; echo impression "No cardioembolic source identified" (C7) | FIXED: advanced_imaging and labs deleted; CT rewritten to this patient's lesions; echo impression modality-only with `echo_type` TTE; metadata.fallback_tool_kinds updated |
| C | major | ground_truth.assessment.required_recommendations | Musts restated criteria (ECG, monitoring, MRI, carotid) or the history already given; anticoagulation must without drug or dose; no BP or lipid must (C19) | FIXED: DOAC with CHA2DS2-VA 4 and the apixaban dose criteria, stop aspirin; BP below 130/80 gradually; high-intensity statin aiming at LDL below 70; reattribute the visual episode; formal visual fields and driving assessment |
| C | minor | ground_truth.assessment.prohibited_recommendations | No guard against withholding anticoagulation for a low-burden paroxysmal AF | FIXED: added "Do not withhold anticoagulation because the atrial fibrillation is paroxysmal or its burden is low [ESC_AF_2024]"; others kept |
| C/A | minor | ground_truth.action_criteria[*] | Rationale = label; unbracketed citations; verdicts in expected evidence (C13) | FIXED |
| C | minor | ground_truth.action_criteria order; sequence_constraints | Neuropsych last; no ECG-before-monitoring constraint (C16) | FIXED: screen, neuropsych, labs, MRI, ECG, duplex, monitoring, drug check; soft ECG before monitoring added |
| C | minor | ground_truth.red_herrings[1].field_path | Empty field path | FIXED: `patient.clinical_history.past_medical_history[3]` |
| C | minor | ground_truth.avoided_actions[*].rationale; stop_rule | Generic rationales, CT "already obtained"; max_additional_actions 0 (C16, C18) | FIXED |
| C | note | TTE | No TTE criterion although TTE is reasonable (2a) after embolic-pattern infarcts; the plan gives S07 none, and the case fallback echo (normal, consistent) answers an order without penalty | no change |
| C | check | 3.6 check | each criterion probed on a fresh environment | all required and recommended alternatives (five drug names included) answered by case outputs; no library answer |

## Changes, in one paragraph a physician can read before re-reviewing
The MRI criterion now matches any MRI order. The exam no longer gives the MoCA; the screen is itemised so that the total (21/30) adds up, with cue-responsive recall. The 30-day monitor now reports a 0.9% AF burden, which is what its four episodes (5 h 21 min over 26 days) amount to; the previous 4.9% was arithmetically impossible. The left occipital infarct spares the calcarine cortex, consistent with full visual fields, and the infarct count is two cortical plus a thalamic lacune. Reports state only their own findings. Labs have varied normal values, the female HDL range and an LDL consistent with the lipid panel. The literature step is gone; the drug check is recommended and keyed to the five oral anticoagulants. A weight (70 kg) supports DOAC dosing. Musts: DOAC (apixaban 5 mg twice daily) and stop aspirin, BP below 130/80, high-intensity statin, reattribution of the "migraine" episode, formal visual fields and driving assessment. A prohibition now guards against withholding anticoagulation for low-burden paroxysmal AF.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation key `[ESC_AF_2024]` used in a prohibition (plan 5.4).
- Synonyms per plan 5.1 (F06.7 in the `icd_codes` of a dementia case).

## Open questions for Andrea (judgment calls you could not settle)
- None.

## Verification
Adversarial verifier, 24 Oct 2026. No notes file for VASC-DEM. Read the final case and the diff. Checked: MoCA arithmetic (2+3+4+2+2+3+5 = 21/30); AF burden (38 + 220 + 12 + 51 = 321 min over 26 days = 0.86%, reported 0.9%); Friedewald LDL (208 - 66 - 26.4 = 116); female ranges; CHA2DS2-VA 4 (age 65-74, hypertension, stroke) and the apixaban dose criteria; Cockcroft-Gault at 70 kg (about 64 mL/min); sulphonamide allergy handled in the interaction output; occipital infarct sparing the calcarine cortex consistent with full fields; Bells omissions consistent with no neglect; red-herring paths (past_medical_history[3] is the visual episode); ECG-before-monitoring soft constraint; monitoring criterion stays required per plan.
Found and fixed: eGFR 72 did not match the CKD-EPI 2021 value for creatinine 0.86 mg/dL in a 73-year-old woman (71.3). Set `initial_tool_outputs.labs.panels.CMP[eGFR].value` to 71 and the labs criterion's expected evidence to "eGFR 71". The worker's log row "about 71-72" is superseded.
perfect_agent.py and case_io.py check clean for this case.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here multi-infarct labels and F01.1. Generic labels "vascular dementia", "major vascular neurocognitive disorder", "major neurocognitive disorder due to vascular disease", "VaD"; codes F01.50, F01.51, F01.5, F01.9, F01.A0-C0.
- `ground_truth.diagnosis.accepted[0]`: em dash replaced by a colon or semicolon; wording and entity unchanged (no scoring effect: matching ignores punctuation).
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- Lipid must: "Intensify lipid lowering from atorvastatin 20 mg to a high-intensity statin, aiming at LDL below 70 mg/dL (current 116 mg/dL) given the carotid plaque [AHA_ASA_2021_secondary]" -> "Intensify lipid lowering from atorvastatin 20 mg to a high-intensity statin, aiming at LDL below 55 mg/dL (current 116 mg/dL): very high risk after ischaemic strokes at 73 with hypertension and carotid plaque; add ezetimibe if the goal is not reached [ACC_AHA_dyslipidemia_2026]" Reason: the 2026 ACC/AHA multisociety dyslipidemia guideline (supersedes the 2018 cholesterol guideline on which the AHA 2021 LDL-below-70 figure rests) sets LDL below 55 mg/dL for clinical ASCVD at very high risk (two major ASCVD events, or one plus two or more high-risk conditions).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 68 -> 70 kg, height 163 -> 165 cm, BMI 25.6 -> 25.7 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 70 kg, height 165 cm.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.
