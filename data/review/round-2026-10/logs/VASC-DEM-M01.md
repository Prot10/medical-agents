# VASC-DEM-M01
Reviewer status: R1 not reviewed, R2 not reviewed (VASC-DEM has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | VASC-DEM was never annotated; no note ids exist for this case. All changes below come from the condition plan (classes C1-C19) and my own reading. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-5-analyze-brain-mri].alternatives` | Plan C1: `required_arguments` carried `sequences`, `protocol`, `contrast`; `sequences` is not a tool parameter, so no real call could match the required MRI. | FIXED: one alternative `analyze_brain_mri {}`. |
| D | major | `ground_truth.action_criteria[action-8-search-medical-literature]`, `initial_tool_outputs.literature_search`, `fallback_tool_outputs.literature_search` | Plan C2 / ruling 5: literature criterion whose expected evidence was copied into its own output (guard leak). | FIXED: criterion deleted, initial output null, fallback deleted. |
| C | minor | `ground_truth.action_criteria[action-9-check-drug-interactions]`, `fallback_tool_outputs.drug_interactions` | Plan C3 group D: generic optional drug check and a generic "no prohibitive interaction" fallback; ramipril, atorvastatin and calcium/vitamin D carry no interaction that changes management. | FIXED: criterion and fallback deleted; initial output stays null. |
| D | major | `patient.neurological_exam.mental_status` | Plan C4: exam gave the MoCA total and item losses, the result of the required screen. | FIXED: bedside observation only, "Formal cognitive screening reported separately." |
| B | minor | `initial_tool_outputs.clinical_assessment.findings[0]` | Serial sevens "4/5" cannot lose a MoCA point (4-5 correct scores 3/3), yet the 24/30 total counts one lost point there. | FIXED: "3 of 5 correct subtractions (2/3 points)"; findings completed per MoCA item (orientation 6/6, naming, repetition, abstraction, clock) so the item sum is 24. |
| D | major | `initial_tool_outputs.clinical_assessment.impression`, `initial_tool_outputs.specialized_test.impression`, `initial_tool_outputs.mri.impression`, `.additional_observations[0,3]`, `.findings[0].signal_characteristics.T2_FLAIR`, `initial_tool_outputs.csf.interpretation` | Plans C5/C17: every report stated the severity ("mild vascular cognitive impairment, not vascular dementia", "below the threshold at which small-vessel disease alone accounts for a dementia", "matches a patient who is still functionally independent", "not attributable to Alzheimer's disease", "Serial reassessment is the appropriate management", "not an Alzheimer pattern"). | FIXED: modality-only reports: screen lists total, item losses, cueing, FAQ, GDS; neuropsych lists percentiles and a "Profile:" sentence without disease name; MRI numbered STRIVE-2 impression (Fazekas 2 P2/D2, one 5 mm right corona radiata lacune, PVS grade 1, no microbleeds or cSS, MTA 1); CSF values with "within reference ranges". Em dashes removed from the CSF special tests and MRI volumetrics. |
| D | minor | `followup_outputs[0].output.impression`, `.findings[4]`, `.scores.10_metre_walk` | Gait report closed with a diagnostic argument ("consistent with a small-vessel burden that has not yet produced a clinical syndrome"); 10-metre walk in "s per metre". | FIXED: measurements only (TUG 11.8 s, 9.8 s over 10 m = 1.02 m/s, SPPB 11/12, step length 48 cm, dual-task cost 12% with reference). |
| B | minor | `initial_tool_outputs.labs` | Plan C6: template values (WBC 6.8, Hct 41.6, Plt 238, MCV 88, Na 139, K 4.2, ALT 22, albumin 4.1, folate 11.8), eGFR range ">60", female HDL range ">40", interpretive `interpretation` ("above target", "no reversible cause"). | FIXED: WBC 5.9, Hct 40.8 (3 x Hb 13.6), Plt 264, MCV 91, Na 141, K 4.4, ALT 17, albumin 4.3, folate 14.2; eGFR ">=60"; HDL ">50" (56 not flagged); interpretation "Flagged: total cholesterol 202 mg/dL (high), LDL cholesterol 112 mg/dL (high). Other results within reference ranges." Female Hb/Hct ranges kept (correct). |
| D | minor | `fallback_tool_outputs.advanced_imaging`, `.labs`, `.ct` | Plan C7: fallbacks revealing the order was off-pathway ("non-contributory", "better characterised on the MRI already obtained"). | FIXED: advanced imaging and labs fallbacks deleted; CT fallback rewritten as this patient's non-contrast CT (periventricular and deep hypodensity, small right corona radiata lacune, mild volume loss). |
| A | minor | `fallback_tool_outputs.echo` | No `echo_type`; impression "No cardioembolic source identified." | FIXED: `echo_type` "TTE"; impression describes the study (EF 60%, mild concentric LVH, aortic sclerosis, no thrombus or shunt). Echo and Holter fallbacks kept: consistent with the case (regular pulse 72, no stroke). |
| C | major | `ground_truth.action_criteria[action-7-analyze-csf]` | Plan C9: CSF biomarkers `recommended` in mild cognitive impairment, where AAN 2018 does not recommend routine biomarkers. | FIXED: `optional`, label and rationale reworded; output unchanged in values. |
| C | major | `ground_truth.action_criteria[action-4-perform-clinical-assessment]` | Plan C14: gait required although she has no gait complaint and the test is normal. | FIXED: `recommended`, label and rationale case-specific (mildly reduced step length on examination). |
| A | minor | all `action_criteria[*].rationale`, `.citations` | Plan C13: rationale identical to label; bare duplicate citation keys. | FIXED: case-specific one-sentence rationales; one bracketed key each; expected_evidence rewritten with the case values. |
| B | minor | `ground_truth.action_criteria` order, `sequence_constraints`, `stop_rule` | Plan C16: order was screen, labs, gait, MRI, neuropsych, CSF; no MRI-before-CSF constraint; `max_additional_actions` 0. | FIXED: order screen, gait, neuropsych, labs, MRI, CSF (ids unchanged); soft MRI before CSF added; stop rule = screen, neuropsych, labs, MRI; `max_additional_actions` 1. |
| B | minor | `ground_truth.avoided_actions[*].rationale` | Plan C18: CT rationale said "the MRI already obtained"; generic rationales. | FIXED: CT canonical rationale; EEG, echo and monitoring rationales name this patient's reason (slow non-fluctuating course; no infarct, regular pulse). Echo and monitoring waste kept (no stroke, plan section 4). |
| C | major | `ground_truth.assessment.required_recommendations` | Musts restated tool steps ("Exclude reversible causes", "Obtain MRI", "Document the cognitive profile") and the generic biomarker must. | FIXED (C9, C19): five musts: disclose mild VCI not dementia with the functional evidence [VASCOG_2014]; canonical AAN 2018 must (no AD attribution, reassess in 12 months, biomarker if amnestic evolution); BP below 130/80 gradually from 138/82 on ramipril 5 mg [ESO_2021_SVD]; statin adjusted to overall cardiovascular risk (LDL 112 on atorvastatin 20; covert SVD sets no own LDL target) [ESO_2021_SVD]; exercise at least twice weekly [AAN_MCI_2018]. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Cholinesterase prohibition argued from "no Alzheimer biology" (an optional test); no antiplatelet prohibition for covert SVD. | FIXED: AChEI or memantine not indicated in mild VCI [AAN_MCI_2018]; added "Do not start an antiplatelet for covert small-vessel disease alone [ESO_2021_SVD]"; other prohibitions kept. |
| C | major | `ground_truth.differential[0]`, `[1]` | Plan C8: "Vascular dementia (major)" moderate although independence is preserved; AD key features relied on CSF (now optional). | FIXED: VaD low; AD key features cite cue-responsive recall, normal recognition, MTA 1, "CSF, if obtained, normal". |
| B | minor | `ground_truth.key_clinical_evidence[3]`, `red_herrings[0]`, `metadata.key_educational_points[2]` | Relied on a normal CSF biomarker profile as the way to close the AD question. | FIXED: reworded to the AAN 2018 position and the memory profile; red herring `field_path` set to `patient.clinical_history.family_history[0]`. |
| A | minor | `metadata.fallback_tool_kinds` | Listed the deleted fallbacks. | FIXED: entries for advanced_imaging, drug_interactions, labs, literature_search removed. |
| E | minor | `ground_truth.diagnosis.accepted[0]` | Label contains an em dash ("... small-vessel disease — the threshold for vascular dementia is not met"). | FLAGGED: label not edited (ruling 3). |
| - | check | plan 3.6 | perfect_agent ok; every required/recommended criterion answered by case data (probe: screen, gait follow-up, neuropsych, labs, MRI; optional CSF answered by the case CSF); echo, CT and Holter answered by the case fallbacks; test_case_guards pass; `case_io.py check` lists no failure naming M01. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The case remains mild vascular cognitive impairment in a 69-year-old retired pharmacist (MoCA 24/30, executive and processing-speed slowing, informant FAQ 2/30, Fazekas 2 with one lacune). No report now states the severity or the diagnosis: the examination no longer gives the MoCA, and the screen, neuropsychology, MRI, CSF and gait reports describe only their measurements (the MoCA item breakdown was corrected: serial sevens 3/5 correct, the only way that item loses a point). The MRI criterion now matches any MRI order. CSF Alzheimer biomarkers are optional (AAN 2018: not routine in MCI) and the timed gait test is recommended; the literature and drug-interaction steps are gone. The musts are management: explain mild VCI rather than dementia, no Alzheimer attribution with 12-month reassessment and a biomarker only if the profile turns amnestic, BP below 130/80 mmHg from 138/82, statin adjusted to cardiovascular risk (LDL 112 on atorvastatin 20 mg), and exercise; new prohibitions on antiplatelets for covert SVD and on cholinesterase inhibitors or memantine. Vascular dementia is low on the differential. Lab normals were de-templated and the female HDL and eGFR ranges corrected.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms (plan 5.1): the `F06.7` entry appends `F01.50` to this case's `icd_codes` and the umbrella label "vascular cognitive impairment"; a vascular dementia answer should not be credited for this mild case.
- `accepted[0]` contains an em dash; harmless for matching, but the label could lose the dash centrally.
- `perfect_agent.py -v` prints "<- ?" for initial outputs that contain null fields (`_source` compares against `model_dump(exclude_none=True)`); the outputs are case data (not fallback), confirmed by probing.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. Checked: no note ids exist (unreviewed condition); every plan class claimed (C1, C2, C3 D, C4, C5/C17, C6, C7, C8, C9, C13, C14, C16, C18, C19) is applied in the file; MoCA item arithmetic (losses 1+1+1+3 = 6, 24/30, 17 years, no correction) matches findings, impression and expected evidence; female Hb/Hct/HDL ranges and flags; criteria order and soft MRI-before-CSF constraint; stop rule = the four required ids; musts and prohibitions do not contradict each other or the avoided actions; differential matches the final evidence; no report states the severity or the diagnosis; fallback kinds match the remaining fallbacks.

Found and changed:
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | minor | `initial_tool_outputs.labs.panels.Reversible_cause_screen[Vitamin B12]`, `action_criteria[action-3-interpret-labs].expected_evidence` | B12 296 pg/mL sits in the 200-300 borderline band where methylmalonic acid is usually checked, yet the case scores it as "normal" and nothing addresses it (PATTERNS: comorbid contributor dismissed). | FIXED: value 438 pg/mL (clearly normal), expected evidence updated. |

perfect_agent ok; `case_io.py check` and test_case_guards list no failure naming M01.

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `initial_tool_outputs.labs.panels.Vascular_risk[HDL cholesterol]` | Total cholesterol 202 did not equal LDL 112 + HDL 56 + TG 126/5 (193.2); TC 202 is flagged and quoted in the evidence and interpretation, so HDL was the value to move. | FIXED: HDL 65 mg/dL (normal on the female range, not quoted anywhere else). |
| C | minor | `ground_truth.avoided_actions[avoid-waste-3-order-advanced-imaging].rationale`, `[avoid-waste-4-interpret-labs].rationale` | Plan C18: the MIBG and paraneoplastic/autoimmune rationales were still the August template text shared by M01-M06; the autoimmune one described "a chronic stepwise decline with a hypertensive imaging burden", which is wrong for this case. | FIXED: case-specific one-liners (no Lewy features; slow two-year decline in an independent woman, not a subacute syndrome). |
| D | major | `initial_tool_outputs.clinical_assessment.criteria_met` | Plan 1.2 and C5 (no report states the severity): the screen's structured fields still carried independence_in_iadl_lost (false), executive_predominant_profile, i.e. the mild-versus-major threshold, the profile verdict or history items. Workers removed these keys in the other 19 cases; here they survived (the P03 worker flagged the question for a condition-wide decision). | FIXED: keys removed; `criteria_met` keeps domain impairment and cue-responsive recall. The informant FAQ score stays in the report as an instrument score. |
| D | minor | `initial_tool_outputs.specialized_test.quantitative_data.functional_status` | Plan C17: "independent by informant report" verbalised the severity in the neuropsychology report. | FIXED: "informant FAQ 2/30" (the instrument score). |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml F06.7 entry, applied with `--prune --conditions vascular_dementia`): the umbrella "vascular cognitive impairment" (it also matches a dementia answer) and the codes F01.50 (vascular dementia) and G31.84 (MCI of any cause, including Alzheimer) are no longer accepted; "mild vascular neurocognitive disorder", "vascular cognitive impairment no dementia" and F06.70 (FY2023 code) added. A dementia overcall no longer scores.
- `ground_truth.diagnosis.accepted[0]`: em dash replaced by a colon or semicolon; wording and entity unchanged (no scoring effect: matching ignores punctuation).
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- `metadata.revision_reason`: the stale August literature/interaction audit text replaced by the round's (summary CENTRAL 9; not read by the harness).
- `metadata.fallback_tool_kinds`: ct normal->case (the fallback describes this patient, not a library normal; summary CENTRAL 9).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.
