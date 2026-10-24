# VASC-DEM-S03
Reviewer status: R1 not reviewed, R2 not reviewed (VASC-DEM has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The condition has no reviewer notes. The plan's classes (C1-C8, C13, C14, C16, C18, C19 and the S03 index entry) were applied as classes (ruling 2); see Own findings. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | ground_truth.action_criteria[action-5-analyze-brain-mri].alternatives | Non-schema `sequences` key plus `protocol`/`contrast`: no real call could match (C1). | FIXED: `analyze_brain_mri {}`; label and rationale rewritten. |
| D | major | action-7-search-medical-literature; initial and fallback literature_search | Literature criterion leaking its expected evidence into its own output (C2). | FIXED: criterion deleted, initial null, fallback deleted. |
| C | minor | action-8-check-drug-interactions; fallback_tool_outputs.drug_interactions | Generic drug check and fallback (C3 group D). | FIXED: deleted. |
| D | major | patient.neurological_exam.mental_status | Gave MoCA 21/30 and item losses (C4). | FIXED: bedside observation, "Formal cognitive screening reported separately". |
| D | major | initial_tool_outputs.clinical_assessment (impression, criteria_met) | "Functional independence is lost. The profile is subcortical."; IADL and executive verdicts in criteria_met (C5). | FIXED: scores-only impression; criteria_met keeps impairment and cueing. |
| B | minor | initial_tool_outputs.clinical_assessment (findings, scores) | Listed losses gave raw 22 (23 corrected), not 21; fluency given as animals for the MoCA letter-F item. | FIXED: full MoCA domains 2+3+4+2+1+3+5 = raw 20, plus 1 for 10 years of education = 21 (serial sevens 2/3 and abstraction 1/2 made explicit); "10 F-words". |
| D | major | followup_outputs[gait].output.impression | "part of the subcortical vascular syndrome rather than an incidental orthopaedic problem" (C5). | FIXED: measurements only; cadence 116 steps/min added, consistent with 28 cm steps at 0.54 m/s. |
| D | major | initial_tool_outputs.specialized_test.impression | "the profile remains clearly subcortical ... Low education does not account for the deficit" (C5). | FIXED: education-adjusted profile wording. |
| B | major | initial_tool_outputs.labs (CBC) | Hb 11.8 with Hct 41.6 (C6: Hct must be about 35-36%); female Hb/Hct ranges in a man; template values. | FIXED: Hct 35.6 (flagged), male ranges, varied normal values (WBC 5.6, Plt 196, MCV 86, Na 140, K 4.7, ALT 14, albumin 3.8, folate 10.3). |
| B | minor | initial_tool_outputs.labs.CMP (creatinine, eGFR) | Creatinine 1.92 gives CKD-EPI 2021 eGFR about 35 at 78, not the 38 stated in the history and report; female creatinine range; eGFR ">60". | FIXED: creatinine 1.80 (eGFR 38, matching the history), range 0.70-1.30, eGFR ">=60". |
| D | minor | initial_tool_outputs.labs.interpretation | "confirms stage 3b CKD", "consistent with renal disease", "near but not at the target", "excluding reversible causes" (C6). | FIXED: pattern-level recital of flagged values. |
| D | major | initial_tool_outputs.mri (impression, observations) | "The burden accounts for both the cognitive syndrome and the gait disorder"; Boston criteria and "no abnormal enhancement" in a non-contrast study (C5). | FIXED: numbered STRIVE-2 impression; the deep-microbleed pattern hedged as "consistent with hypertensive arteriopathy" (imaging pattern). |
| B | minor | initial_tool_outputs.mri.additional_observations | The NPH differential and red herring rely on "no disproportionately enlarged subarachnoid space", which the report never stated. | FIXED: observation added (proportionate Sylvian fissures and convexity sulci, no DESH, callosal angle 112 degrees). |
| D | minor | fallback_tool_outputs (advanced_imaging, labs, ct, echo, cardiac_monitoring) | Off-pathway revealing text; echo "No cardioembolic source identified"; Holter average 72 vs his 68 on carvedilol (C7). | FIXED: advanced_imaging and labs deleted; CT rewritten for this patient; echo neutral with echo_type TTE; Holter average 66. metadata.fallback_tool_kinds updated. |
| C | major | ground_truth.differential[Normal pressure hydrocephalus] | Moderate although the imaging excludes it (C8). | FIXED: low. |
| C | major | ground_truth.assessment | Musts restated the scored work-up; "lower BP toward target" without a target; no falls measures although TUG is 24.6 s; no covert-SVD antiplatelet prohibition (C19). | FIXED: NPH distinction on imaging, no tap test; immediate falls measures with orthostatic BP and review of tamsulosin, carvedilol and furosemide; BP below 130/80 gradually, consider ACE inhibitor or ARB for hypertensive kidney disease with creatinine and potassium monitoring [ESO_2021_SVD]; statin intensity for CKD 3b and LVH; iron studies for the anaemia; home safety and carer support. Prohibition added: no antiplatelet for covert SVD alone [ESO_2021_SVD]. |
| A | minor | all criteria citations and rationales | Unbracketed duplicates; rationale equal to label (C13). | FIXED. |
| C | minor | avoided_actions rationales | Generic text; "MRI already obtained" (C18). | FIXED: case-specific; CT rationale per plan. Echo and monitoring waste kept (no clinical stroke). |
| C | minor | criteria order, stop_rule (C16) | | FIXED: screen, gait, neuropsych, labs, MRI; screen before MRI kept; max_additional_actions 1. |

## Changes, in one paragraph a physician can read before re-reviewing
Diagnosis unchanged (subcortical ischaemic vascular dementia from severe hypertensive arteriopathy, with gait failure). The exam no longer gives the MoCA; the screen adds up to 21/30 with the education point. Reports no longer say that the burden explains the cognition and gait; the MRI adds the measurements that separate this from NPH (proportionate sulci, no DESH, callosal angle 112 degrees). The anaemia is now consistent (Hb 11.8, Hct 35.6, male ranges), and creatinine is 1.80 so that the eGFR of 38 follows from it. Literature and drug-check steps are gone; NPH is low in the differential. Musts now address the falls risk now (including orthostatic BP and tamsulosin, carvedilol and furosemide), BP below 130/80 lowered gradually with consideration of RAS blockade for his kidney disease, statin intensity, iron studies for the anaemia and home safety; a prohibition on an antiplatelet for covert small-vessel disease is added.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms (plan 5.1): remove F06.7 from the F01 codes of this dementia case.

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial verifier, 24 Oct 2026. Checked every Own-findings row against the file and the git diff: MRI `{}`; literature and drug check gone; MoCA domains give raw 20 plus 1 = 21 and the lost points (3+2+2+1+1+1) agree; gait 28 cm at 116 steps/min gives 0.54 m/s; Hb 11.8 with Hct 35.6 flagged on male ranges; creatinine 1.80 gives CKD-EPI 2021 eGFR 38 at 78, matching the history; MRI now carries the NPH-discriminating measurements that the differential, red herring and must rely on (proportionate sulci, no DESH, callosal angle 112 degrees, Evans 0.30); NPH low; Holter fallback average 66 fits carvedilol and HR 68; musts (falls with tamsulosin, carvedilol and furosemide review, BP below 130/80, RAS blockade with monitoring, iron studies) agree with the prohibitions (no anticoagulation, no covert-SVD antiplatelet, no precipitous BP drop). Guard tests pass. No error found.
Changed: nothing. His echo fallback keeps LVEF 60% with mild concentric hypertrophy, which matches his documented LV hypertrophy; the other cases' copies were varied.
Re-ran `perfect_agent.py -v` (pass) and `case_io.py check` (clean for this case).

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `initial_tool_outputs.labs.panels.Vascular_risk[Total cholesterol]` | Total cholesterol 178 mg/dL did not equal LDL + HDL + TG/5 (168.8); the same lab-arithmetic class was fixed in M07-M10, P01, P02 and S06-S11 but not here. | FIXED: total cholesterol 169 mg/dL (flag unchanged; LDL, HDL and TG, which the musts and evidence quote, unchanged). |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.
