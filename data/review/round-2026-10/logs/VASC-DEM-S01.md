# VASC-DEM-S01
Reviewer status: R1 not reviewed, R2 not reviewed (VASC-DEM has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The condition has no reviewer notes. The plan's classes (C1-C7, C13, C14, C16, C18, C19 and the S01 index entry) were applied as classes (ruling 2); see Own findings. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | ground_truth.action_criteria[action-5-analyze-brain-mri].alternatives | Non-schema `sequences` key plus `protocol`/`contrast`: no real call could match (C1). | FIXED: `analyze_brain_mri {}`; label and rationale rewritten. |
| D | major | action-7-search-medical-literature; initial and fallback literature_search | Literature criterion leaking its expected evidence into its own output (C2). | FIXED: criterion deleted, initial null, fallback deleted. |
| C | minor | action-8-check-drug-interactions; fallback_tool_outputs.drug_interactions | Generic optional drug check and generic fallback; no interaction changes management (C3 group D). | FIXED: criterion and fallback deleted (initial already null). |
| D | major | patient.neurological_exam.mental_status | Gave MoCA 19/30 and item scores (C4). | FIXED: bedside observation, "Formal cognitive screening reported separately". |
| D | minor | patient.neurological_exam.sensory | "consistent with his diabetes" resolves the red herring in the exam. | FIXED: finding only. |
| D | major | initial_tool_outputs.clinical_assessment (impression, findings, criteria_met) | "retrieval pattern rather than the storage deficit of Alzheimer's disease", "functional independence lost", "GDS does not account for the profile"; IADL and executive-profile verdicts in criteria_met (C5). | FIXED: scores-only impression; criteria_met keeps impairment and cueing. |
| B | minor | initial_tool_outputs.clinical_assessment (findings, scores) | Listed items summed to 20, not 19; fluency given as "7 animals (normal >=14)" for the MoCA letter-F item. | FIXED: abstraction 1/2 added, domain rows sum to 19 (2+3+4+2+1+2+5); "7 F-words in 60 s"; orientation 5/6 matches the exam. |
| D | major | followup_outputs[gait].output.impression | Diagnostic label and essay against parkinsonism and NPH (C5). | FIXED: measurements and observations only. |
| B | minor | followup_outputs[gait].output.scores | 10 m walk 1.42 s/m (0.70 m/s) inconsistent with step 34 cm at 96 steps/min (0.54 m/s). | FIXED: cadence 124 steps/min (0.70 m/s); Romberg negative row added (as in the exam). |
| D | major | initial_tool_outputs.specialized_test.impression | "the opposite of the storage deficit seen in Alzheimer's disease" (C5). | FIXED: profile wording without disease names. |
| B | minor | initial_tool_outputs.labs | Female Hb/Hct ranges in a man; template values; eGFR 63 does not follow from creatinine 1.12 at 74 (CKD-EPI 2021 about 69); female creatinine range; "consistent with diabetic nephropathy", "above target", "excluding" (C6). | FIXED: male ranges, varied normals (Hct 42.1 for Hb 13.9), creatinine 0.70-1.30, eGFR 69 with ">=60", pattern-level interpretation and flagged summary. |
| D | major | initial_tool_outputs.mri (impression, observations, volumetrics) | "sufficient to account for the cognitive syndrome; no imaging evidence of an Alzheimer pattern, amyloid angiopathy or hereditary arteriopathy" (C5). | FIXED: numbered STRIVE-2 impression ending "consistent with severe cerebral small vessel disease". |
| B | minor | initial_tool_outputs.mri.additional_observations | "No external capsule pattern" contradicted finding[0] ("early involvement of the external capsules"); "no abnormal enhancement" in a non-contrast study. | FIXED: observation now "No anterior temporal pole white matter hyperintensity"; enhancement statement removed. |
| D | minor | fallback_tool_outputs (advanced_imaging, labs, ct, echo) | Off-pathway revealing text; echo "No cardioembolic source identified" (C7). | FIXED: advanced_imaging and labs deleted; CT rewritten for this patient (confluent hypodensity, lacunes, volume loss, CT limits); echo impression neutral with echo_type TTE; Holter kept (average HR 73 near his 74). metadata.fallback_tool_kinds updated. |
| C | major | ground_truth.assessment.required_recommendations | Musts restated the scored work-up (document deficit, exclude reversible causes, obtain MRI, assess gait) and gave no targets (C19). | FIXED: continue single antiplatelet for the probable lacunar events; BP below 130/80 gradually with orthostatic checks (168/92, adherence); atorvastatin 80 mg for LDL 118 on 40 mg; HbA1c about below 8.0% (8.4%) [ADA_2025_older_adults]; formal driving assessment; falls, urgency without anticholinergics, alcohol, carer support. Prohibitions unchanged. |
| C | major | (plan C19 for S01) | The plan lists S01 for "no antiplatelet for covert SVD". S01 is not covert: two transient right-hand clumsiness and dysarthria episodes, each followed by a step down, with lacunes in the left putamen and corona radiata, are clinical lacunar events, and he takes aspirin for them. | Not applied: aspirin continued as secondary prevention (AHA 2021); the existing prohibition of a second antiplatelet or anticoagulant stays. Told the lead in this log. |
| C | minor | ground_truth.action_criteria (new action-9-analyze-ecg), initial_tool_outputs.ecg | Two uninvestigated transient focal episodes and 31 years of hypertension, no ECG anywhere (AHA 2021: ECG after TIA or stroke). | FIXED: optional ECG criterion with a sinus rhythm, voltage-LVH output (no AF). Optional, not recommended, because the pack keeps ECG out of the pure subcortical work-up. Echo and monitoring stay waste with case-specific rationales. |
| A | minor | all criteria citations and rationales | Unbracketed duplicates; rationale equal to label (C13). | FIXED. |
| C | minor | avoided_actions rationales | Generic rationales; "MRI already obtained" (C18). | FIXED: case-specific; CT rationale per plan. |
| C | minor | criteria order, stop_rule (C16) | | FIXED: screen, gait, neuropsych, labs, MRI, ECG; screen before MRI kept; max_additional_actions 1. |

## Changes, in one paragraph a physician can read before re-reviewing
Diagnosis unchanged (subcortical ischaemic vascular dementia from hypertensive arteriopathy). The exam no longer gives the MoCA; the screen adds up to 19/30 and lists scores only. Gait, neuropsychology and MRI reports describe their own findings without naming the diagnosis or arguing against NPH, parkinsonism, Alzheimer disease or CAA; the MRI no longer contradicts itself on the external capsules. Labs use male ranges, an eGFR that follows from his creatinine (69) and a plain list of flagged values. The literature and drug-check steps are gone; an optional ECG (sinus rhythm, LVH by voltage) is added because his two transient episodes were never investigated. Musts now state his targets: continue aspirin for the probable lacunar events, BP below 130/80 lowered gradually with orthostatic checks, atorvastatin 80 mg for LDL 118, HbA1c about below 8.0%, a driving assessment, falls, bladder and carer measures.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms (plan 5.1): remove F06.7 from the F01 codes of this dementia case.
- Citation key `[ADA_2025_older_adults]` used in a must (plan 5.4).

## Open questions for Andrea (judgment calls you could not settle)
None. Decision recorded for the lead: plan C19's covert-SVD prohibition does not fit S01, which has clinical lacunar events (see Own findings).

## Verification
Adversarial verifier, 24 Oct 2026. Checked every Own-findings row against the file and the git diff: MRI `{}`; literature and drug-check criteria and fallbacks gone; MoCA domains sum to 19 and the lost points (3+3+2+1+1+1) give 19; gait 34 cm at 124 steps/min gives 0.70 m/s; male Hb/Hct ranges, Hct 42.1 for Hb 13.9, eGFR 69 follows from creatinine 1.12 at 74 (CKD-EPI 2021 about 69); MRI no longer contradicts itself on the external capsules; musts carry his numbers. The worker's decision not to apply the covert-SVD antiplatelet prohibition is sound: two dated transient right-hand and dysarthria episodes, each followed by a step down, with matching left putamen and corona radiata lacunes, are clinical lacunar events, and continuing aspirin is AHA 2021 secondary prevention. Guard tests pass.
Found and changed:
- Having accepted that the events were TIAs or minor lacunar strokes, the case still scored the ECG `optional` and TTE as waste. AHA/ASA 2021 recommends an ECG after ischaemic stroke or TIA (class 1) and calls TTE reasonable (2a), and the plan removed echo waste in S08 for that reason. action-9 ECG raised to `recommended` (rationale rewritten); `avoid-waste-6-order-echocardiogram` deleted (the normal echo fallback still answers an order). Monitoring waste kept: the events are explained by small-vessel disease, not cryptogenic.
- `metadata.key_educational_points[0]` said the attribution holds "without a stroke history", contradicting the case's own reading of the two events. Reworded.
- `fallback_tool_outputs.echo` was word-for-word identical across S01-S05 (template carry-over); LVEF set to 62% here.
Re-ran `perfect_agent.py -v` (pass) and `case_io.py check` (clean for this case).

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `initial_tool_outputs.labs.panels.Vascular_risk[Triglycerides]`, `.abnormal_values_summary`, `.interpretation`, labs criterion `expected_evidence` | Total cholesterol 206 did not equal LDL 118 + HDL 38 + TG 192/5 (194.4); TC 206 is flagged and quoted, so TG was the value to move. | FIXED: triglycerides 250 mg/dL everywhere it appears (still flagged high). |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here subcortical small-vessel labels and F01.2/I67.3. Generic labels "vascular dementia", "major vascular neurocognitive disorder", "major neurocognitive disorder due to vascular disease", "VaD"; codes F01.50, F01.51, F01.5, F01.9, F01.A0-C0.
- `ground_truth.diagnosis.accepted[0]`: em dash replaced by a colon or semicolon; wording and entity unchanged (no scoring effect: matching ignores punctuation).
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- `[ADA_2025_older_adults]` -> `[ADA_older_adults_2026]` in the HbA1c must (same target below about 8.0%; superseded edition, as in ALZ-EARLY).
- `metadata.fallback_tool_kinds`: ct normal->case (the fallback describes this patient, not a library normal; summary CENTRAL 9).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.
