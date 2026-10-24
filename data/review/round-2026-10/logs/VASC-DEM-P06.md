# VASC-DEM-P06
Reviewer status: R1 none, R2 none (VASC-DEM has no notes file; never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer note exists for this case or condition. All changes below come from the condition plan (classes C1-C20) and from my own audit. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-4-analyze-brain-mri].alternatives` | Plan C1: non-schema `sequences` key. | FIXED: `analyze_brain_mri {}`; label, rationale, evidence rewritten. |
| D | major | `action-7-search-medical-literature`, literature outputs | Plan C2 leak. | FIXED: criterion deleted, initial null, fallback deleted. |
| B | minor | `action-8-check-drug-interactions`, drug fallback | Plan C3 group D. | FIXED: criterion and fallback deleted; initial null. |
| D | major | `patient.neurological_exam.mental_status` | Plan C4: MoCA in the exam. | FIXED: bedside observation. |
| C | major | `initial_tool_outputs.clinical_assessment` | MoCA arithmetic: the listed losses plus month gave raw 19, and 9 years of schooling adds 1 (would be 20/30); "fluency 7 animals" is not the MoCA item; impression gave the severity and the puzzle framing. | FIXED: abstraction 1/2 added so raw 18 + 1 = 19/30 (total unchanged); letter fluency 7 words; `education_adjusted` states the point added; impression lists results only. |
| D | major | `initial_tool_outputs.specialized_test.impression` | "A genuine ... Limited schooling does not account for the deficit" (conclusion). | FIXED: profile on education-adjusted norms, validity measures passed, FAQ 20/30. |
| D | major | `initial_tool_outputs.mri` | Plan C5: observations cited retinopathy and macroalbuminuria (cross-modality), argued against CADASIL and called the pattern hypertensive; volumetrics "Absent, against CADASIL", "extreme for age"; impression "hypertensive rather than a hereditary signature ... alongside grade 3 retinopathy". | FIXED: STRIVE-2 numbered impression and descriptive observations (anterior temporal pole and U-fibre sparing stated as findings). |
| C | major | `initial_tool_outputs.labs`, `action-3` evidence, KCE | UACR 148 mg/g called "macroalbuminuria" (A3 is 300 mg/g or more; 148 is A2) while the case leans on macroalbuminuria; Hct 47.8% called "secondary erythrocytosis" but it is normal on the male range (41-53%); ALT 52 above the 10-40 range but not flagged; eGFR 54 inconsistent with creatinine 1.42 at 54 years (CKD-EPI 2021 about 59); female Hb/Hct ranges; interpretive `clinical_significance` on homocysteine, ESR, APL, UACR; template values; interpretive narrative. | FIXED: UACR 386 mg/g (A3, so the existing "macroalbuminuria" statements in differential and KCE hold); erythrocytosis claim removed everywhere; ALT flagged; eGFR 59 with range ">=60"; male ranges, Hct 46.9; WBC 8.9, Plt 274, MCV 96, Na 141, K 3.9, albumin 4.2, folate 6.1 (heavy alcohol); `clinical_significance` null; interpretation lists flagged values only. |
| C | minor | `initial_tool_outputs.labs.panels`, `followup_outputs` | Plan C15: CRP missing; APL one line; young-SVD assays inside "Reversible_cause_screen". | FIXED: panel `Homocysteine_inflammatory_antiphospholipid` (homocysteine 18.6 high, ESR 12, CRP 4, lupus anticoagulant, anticardiolipin and anti-beta2-GPI negative) in initial labs and as a follow-up for the targeted order (as in P05). |
| C | major | `followup_outputs[NOTCH3]` | Plan C20: impression attributed the disease to hypertension, cocaine, OSA, smoking and lipids (cross-modality) and told the clinician what not to report; VUS row written as a verdict. | FIXED: laboratory voice: no pathogenic variant; VUS c.3058G>A p.(Ala1020Thr) not cysteine-altering; result does not support a genetic diagnosis of CADASIL; VUS not for predictive testing of relatives (standard laboratory caveat). |
| B | minor | `ground_truth.red_herrings[1].field_path`, `.location` | Pointed to `initial_tool_outputs.specialized_test.findings[2]` (the neuropsych FAS row), not to the NOTCH3 report. | FIXED: `followup_outputs[2].output.findings[2]`; red herring 0 field path `family_history[0]`. |
| C | major | `ground_truth.action_criteria` | Plan C14, C15: no gait or young-SVD criterion; NOTCH3 label cited migraine with aura and anterior temporal pole involvement, neither present. | FIXED: `action-9-perform-clinical-assessment-gait` (recommended, authored output: TUG 17.4 s, 0.71 m/s, seven-step turn, tandem impossible); `action-10-interpret-labs-young-svd` (recommended); NOTCH3 relabelled for this patient (age 54, father's stroke at 55). Order: screen, gait, neuropsych, labs, young-SVD, MRI, NOTCH3. |
| A | minor | `ground_truth.action_criteria[*]` | Plan C13. | FIXED: case rationales and evidence; bracketed keys only. |
| B | minor | `ground_truth.sequence_constraints`, `.stop_rule` | Plan C16. | FIXED: soft MRI before NOTCH3; max 1; required set unchanged. |
| C | major | `ground_truth.differential` | Plan C8: "Hypertensive SVD" very_high was the diagnosis itself; CADASIL and cocaine `moderate` after the work-up. | FIXED: entry deleted; CADASIL and cocaine `low` with updated key features. |
| B | minor | `metadata.vascular_mechanism` | "cadasil" for a sporadic SVD case (plan C20). | FIXED: "svd". |
| B | major | `fallback_tool_outputs` | Plan C7 giveaways; library ECG would be a normal ECG in a man with LVH; echo fallback "mild" LVH and "No cardioembolic source". | FIXED: advanced_imaging and labs deleted; CT rewritten for this patient; ECG fallback (sinus 88, LVH with strain); echo moderate concentric LVH, mildly dilated LA, descriptive impression. `metadata.fallback_tool_kinds` updated. |
| C | major | `ground_truth.assessment.required_recommendations` | Four musts were tool steps; "treat every acquired driver" unspecific; BP 186/108 with grade 3 retinopathy (flame haemorrhages, exudates) not handled as hypertension-mediated acute organ damage. | FIXED: six musts: diagnosis with VUS explanation; same-day assessment and controlled lowering of BP, then target below 130/80 with renal monitoring and adherence plan [ESO_2021_SVD]; statin (LDL 158) [AHA_ASA_2011_VCI]; smoking, alcohol, cocaine; CPAP; practical support. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | "Do not stop investigating the acquired causes because a genetic test has been sent" was not checkable; no covert-SVD antiplatelet prohibition (no clinical stroke). | FIXED: replaced by "Do not start an antiplatelet for covert small-vessel disease alone [ESO_2021_SVD]."; VUS and BP items reworded. |
| B | minor | `ground_truth.key_clinical_evidence[0]`, `[3]` | Dashes; "quantifiable in five organs". | FIXED: reworded (eye, kidney, heart, blood). |
| E | minor | `ground_truth.diagnosis.accepted[0]`, `clinical_assessment.findings[*]` | Em dashes in untouched strings (label not editable here). | FLAGGED. |
| - | check | plan 3.6 | perfect_agent.py ok (gait, young-SVD and NOTCH3 from follow-ups; others initial); `test_case_guards -k VASC-DEM-P06` 2 passed; `case_io.py check` no failure names P06; `sequences` 0. | - |

## Changes, in one paragraph a physician can read before re-reviewing

Same case: a 54-year-old builder with three years of subcortical decline, sixteen years of poorly treated hypertension (186/108 today, grade 3 retinopathy), past cocaine, untreated OSA, smoking and heavy drinking, a father dead of stroke at 55; MRI shows Fazekas 3 disease sparing the anterior temporal poles and NOTCH3 shows only a non-cysteine VUS. The exam no longer gives the MoCA and the MoCA now adds up (raw 18 plus the education point). Reports describe only their own findings; the NOTCH3 report reads as a laboratory report. Lab corrections: urinary ACR is now 386 mg/g so "macroalbuminuria" is true, the erythrocytosis claim is gone (Hct is normal for a man), ALT 52 is flagged, eGFR 59 matches the creatinine. A gait assessment and the young-onset SVD screen (homocysteine raised, inflammatory and antiphospholipid tests negative) are recommended steps. The differential no longer lists the diagnosis itself; CADASIL and cocaine arteriopathy are low. Musts now name the BP emergency handling (same-day assessment, controlled lowering, then below 130/80), statin, smoking, alcohol, cocaine, CPAP and support; no antiplatelet for covert SVD.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation key used: `[Rutten_2019]` (plan 5.4). The same-day BP must rests on ESH 2023 (Mancia G et al., J Hypertens 2023;41:1874-2071, hypertension-mediated organ damage, retinal haemorrhages); I cited the allow-listed `[ESO_2021_SVD]` for the long-term target. Consider allow-listing `[ESH_2023]`.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial check, 24 Oct 2026. Read the log, the diff and the final patient, ground truth, reports and follow-ups. Verified: UACR 386 mg/g supports "macroalbuminuria" (A3) wherever it is stated; eGFR 59 matches creatinine 1.42 at 54 (CKD-EPI 2021); Hct 46.9 with Hb 15.6 on male ranges, no erythrocytosis claim left; MoCA arithmetic (12 points lost, raw 18 + 1 = 19/30) and exam (month incorrect) agree; NOTCH3 VUS c.3058G>A p.(Ala1020Thr) is a correct codon translation and is non-cysteine; red herring path `followup_outputs[2].output.findings[2]` points at the VUS row; `metadata.vascular_mechanism` "svd"; the "Hypertensive SVD" self-entry removed and CADASIL and cocaine arteriopathy low; no clinical stroke in the history, so the covert-SVD antiplatelet prohibition applies; BP must (controlled same-day lowering of 186/108 with grade 3 retinopathy) agrees with the "not abruptly" prohibition; MRI report descriptive.
Found: nothing that needed a change. The citation of `[ESO_2021_SVD]` for the acute BP step and `[AHA_ASA_2011_VCI]` for the statin are the closest allow-listed keys; the worker's CENTRAL request for `[ESH_2023]` stands. perfect_agent.py pass; case_io.py check: schema OK, no failure names P06.

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | minor | `initial_tool_outputs.clinical_assessment.findings[Memory].performance` | Plan C5 (screen gives scores only): "— retrieval pattern" was an interpretive label left in the screen, removed in the other cases' screens. | FIXED: "2/5 unaided, 4/5 cued" (scores only; also removes the em dash). |
| D | major | `initial_tool_outputs.clinical_assessment.criteria_met` | Plan 1.2 and C5 (no report states the severity): the screen's structured fields still carried independence_in_iadl_lost, executive_predominant_profile, onset_before_60, i.e. the mild-versus-major threshold, the profile verdict or history items. Workers removed these keys in the other 19 cases; here they survived (the P03 worker flagged the question for a condition-wide decision). | FIXED: keys removed; `criteria_met` keeps domain impairment and cue-responsive recall. The informant FAQ score stays in the report as an instrument score. |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.
