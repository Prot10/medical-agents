# NPH-M08
Reviewer status: R1 not reviewed, R2 not reviewed (NPH has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | NPH was never annotated; no note ids exist. The July 2026 tool review (Reviewer 1, `condition_tool_guidance.yaml` key `nph`) is applied through the condition plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search`, `fallback_tool_outputs.literature_search`, criterion `action-1-search-medical-literature` | Literature search as a recommended step; `general` output repeated the criterion's expected evidence (leak-test failure). | FIXED (C1): criterion deleted, outputs null. |
| C | major | `followup_outputs[0]` (`request_drug_interactions_shunt_cirrhosis`) | Drug check used for perioperative surgical management ("correct INR to <1.3 with vitamin K, FFP", "hepatology clearance"). | FIXED (C2): deleted; the real point (platelets and INR are within LP thresholds) is now a recommended lab criterion and a prohibition. |
| D | major | `patient.chief_complaint`, `patient.history_present_illness` | Chief complaint listed the differential ("query NPH vs hepatic encephalopathy vs post-meningitis hydrocephalus"); HPI gave Evans 0.33, callosal angle 86 degrees, "meeting NPH criteria". | FIXED (C3): presenting problem only; qualitative outside-MRI sentence; hepatologist referral; no fluctuation or sleep inversion stated (supports the red herring with data). |
| B | major | `patient.clinical_history.past_medical_history`, HPI | "Compensated" cirrhosis, Child-Pugh A, while on lactulose and rifaximin for HE prophylaxis (a prior overt HE episode is decompensation). With bilirubin 1.4 (1), albumin 3.4 (2), INR 1.4 (1), no ascites (1), HE suppressed on medication (2), the stored values give Child-Pugh B, score 7. | FIXED: "Alcohol-related cirrhosis (Child-Pugh B, score 7; one episode of overt hepatic encephalopathy 2 years ago, on lactulose and rifaximin; no ascites; abstinent 5 years)"; varices on propranolol listed. The plan's "Child-Pugh A" is not derivable from the case's values (see Open questions). |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG, 10-m walk, MoCA and recall/trail-making results in the exam; interpretive "(suggests hepatic encephalopathy not active)". | FIXED (C4): qualitative only; numbers moved to the gait report and the MoCA follow-up. |
| E | minor | `patient.neurological_exam.sensory`, `.additional` | "(alcoholic)", "(cirrhosis)" interpretive parentheses. | FIXED: plain findings. |
| C | major | `initial_tool_outputs.mri` | "Mild leptomeningeal enhancement at the basal cisterns" implies contrast and an active meningeal process 8 years after recovery, which the normal CSF and the diagnosis contradict; no technique, temporal horns, DESH, aqueduct, MTA or cerebellum. | FIXED (C7): enhancement removed (non-contrast study, basal cisterns patent); Evans 0.33, callosal angle 86, temporal horns, DESH absent, Fazekas 1, aqueduct flow void, MTA 1, normal cerebellar volume; pallidal T1 hyperintensity kept as a descriptive finding; canonical impression. |
| D | major | `initial_tool_outputs.clinical_assessment` | Baseline report contained the post-tap result, "positive tap test", engineering `criteria_met` keys and the "case's own tap-trial report" sentence. | FIXED (C6): baseline only (TUG 27 s, 10-m walk 21 s/24 steps, turn 6 steps, falls, retropulsion). |
| B | minor | `initial_tool_outputs.csf` | RBC without unit; protein 58 mg/dL without the age-adjusted reference while the case calls the CSF normal. | FIXED (C5): "2 cells/mcL"; protein shows the age-adjusted reference (<60 mg/dL); canonical interpretation; MoCA and step counts in `special_tests`. |
| C | major | `initial_tool_outputs.labs` | HIV "Baseline workup" row; INR in the LFT panel; interpretive summary ("synthetic dysfunction"). | FIXED (C9): HIV removed; `coagulation` panel with INR 1.4 and PT 15.6 s; platelets 88 and INR 1.4 kept; ammonia 38 kept normal; pattern-only interpretation. |
| A | major | `ground_truth.action_criteria` | Plan 3.1 order and tiers missing; lab criterion asked TSH/B12/RPR/HIV; rationales repeated labels. | FIXED: MRI, labs (`{"panels": ["CBC", "coagulation"]}`, recommended), baseline gait, MoCA (optional), CSF, post-tap reassessment (recommended); case-specific rationales and evidence. |
| A | minor | `followup_outputs` | No outputs for the MoCA or the post-tap reassessment. | FIXED: `request_moca_cognitive_screen` and `request_post_reassessment` authored. |
| C | major | `ground_truth.assessment.required_recommendations` | Four process musts; secondary-NPH point stated as a classification note. | FIXED (C11): referral naming the post-meningitic antecedent with hepatology input; continue lactulose (2 to 3 stools) and rifaximin; falls prevention (3 falls documented). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Wrong DESH/triad criterion; AD and "normal ageing" prohibitions copied from the template. | FIXED (C12): canonical iNPH text; HE attribution prohibition; no transfusion before the tap at platelets 88 and INR 1.4 (F9). |
| C | major | `ground_truth.differential` | VCI "high", PD/AD/atrophy "moderate", the case's own diagnosis listed as an alternative ("post-meningitic hydrocephalus" moderate); HE and alcohol-related mimics absent. | FIXED (C13): covert HE / hepatocerebral degeneration low, iNPH low (antecedent exists), alcohol-related cerebellar degeneration low, VCI low (Fazekas 1), PD low, atrophy low. AD removed (no amnestic profile, MTA 1). |
| C | minor | `ground_truth.avoided_actions` | Advanced imaging, neuropsych battery and generic CSF assays not marked waste. | FIXED (3.3): added; all rationales case-specific. |
| B | minor | `fallback_tool_outputs.ct`, `.ecg`, `.echo`, `.cardiac_monitoring` | CT fallback with normal ventricles; ECG "borderline left-axis deviation" with axis "normal" and "benign incidental finding"; echo without `echo_type`. | FIXED (C18): CT shows Evans about 0.33; ECG descriptive normal; `echo_type: TTE`. |
| B | minor | `ground_truth.sequence_constraints`, `stop_rule`, `key_clinical_evidence`, `red_herrings`, `metadata` | Non-canonical reasons, allowance 0, sensitivity 50-80%, tier sentence, red herring arguing from DESH, stale vocab_gap. | FIXED (3.4, 3.5, C19, C20): canonical; HE red herring rewritten; pallidal T1 red herring added (visible in the MRI report). |

## Changes, in one paragraph a physician can read before re-reviewing
The patient block no longer lists the differential or the outside MRI measurements and no longer gives the timed gait or MoCA; the cirrhosis is described as it is (one overt hepatic encephalopathy episode on lactulose and rifaximin, no ascites, varices on propranolol, Child-Pugh B score 7 from the stored values). The MRI is a non-contrast iNPH read (Evans 0.33, callosal angle 86 degrees, temporal horns enlarged, no DESH, Fazekas 1, patent aqueduct, normal cerebellum, symmetric pallidal T1 hyperintensity) without the leptomeningeal enhancement that contradicted the diagnosis. Labs are recommended as the pre-tap safety question (platelets 88, INR 1.4, both within the thresholds) with a normal ammonia. The gait report is the baseline only; the CSF report gives normal pressure and content with the tap figures (TUG 27 to 21 s, 22%) and a separate reassessment returns them. Literature and drug-check steps are gone. Musts: shunt referral for post-meningitic secondary NPH with hepatology input, continuing HE prophylaxis, falls prevention. Prohibitions: the corrected iNPH criterion, no HE attribution without supporting signs, no transfusion before the tap.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- R2: `[Nakajima_2021]` (referral must, soft sequence reason) is not yet in the NPH criteria pack.
- R4: post-tap reassessment criterion shares the baseline pattern.
- `perfect_agent.py -v` prints "<- ?" for outputs with null fields (see NPH-M07); verified served by the case's own outputs with `MockServer.get_output`.

## Open questions for Andrea (judgment calls you could not settle)
None. Decision recorded: the plan asked for "Child-Pugh A", but the case's own values (bilirubin 1.4, albumin 3.4, INR 1.4, no ascites, encephalopathy suppressed on medication) score 7, Child-Pugh B. I kept the stored laboratory values and corrected the class rather than altering values to fit a label.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the pre-round diff of the patient block and labs, and the final MRI, CSF, gait, follow-ups, fallbacks and ground truth. The Child-Pugh decision is correct: bilirubin 1.4 mg/dL (1), albumin 3.4 g/dL (2), INR 1.4 (1), no ascites (1), encephalopathy controlled on medication (2) give 7, class B; the plan's "A" was not derivable. Tap figures agree across the CSF report, reassessment, criteria and must (TUG 27 to 23 to 21 s, 15% and 22%; 10-m walk 21 to 17 s, 19%); MoCA subscores sum to 21; platelets 88 and INR 1.4 sit in a `coagulation`/`CBC` pattern matching the recommended lab criterion and the no-transfusion prohibition (F9); lactulose target is 2 to 3 stools; the MRI is non-contrast and the leptomeningeal enhancement is gone; the differential no longer lists the case's own diagnosis. The added varices on propranolol are plausible for Child-Pugh B cirrhosis with platelets 88 and are consistent with every other field, so they stay. Found and fixed one language defect introduced by the edit: the exam stated "No asterixis" twice and also "No flapping tremor" (the same sign). `patient.neurological_exam.additional` now reads "No asterixis. Spider angiomata on the upper chest and palmar erythema. No fetor hepaticus, no ascites."; the duplicate "No asterixis." was removed from `mental_status`. `perfect_agent.py -v`, `case_io.py check` and `test_case_guards` clean after the change.

## Condition audit (NPH auditor, 24 Oct 2026)
- MoCA attention finding "Serial subtraction slow with one error; digit span backward 3." -> "Serial subtraction slow with two errors; digits backward failed." so the finding scores to the stored Attention subscore (4/6); totals unchanged.
- `[Tisell_2011]` removed from `action-4-analyze-csf.citations`: the pack entry is Tisell 2011, shunt surgery in hydrocephalus with white matter changes, and this rationale is about the tap response only; `[Marmarou_2005]` (tap test) stays.
- Checks after the edits: `perfect_agent.py` passes for all 30 NPH cases, `case_io.py check` clean.

## Close-out (24 Oct 2026)

Condition close-out (`plans/NPH-decisions.md`); no clinical data the agent receives changed.
- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions nph`): code G91.2 and the bare labels "normal pressure hydrocephalus" and "NPH" removed, because with token matching they credited "idiopathic NPH", the wrong answer for a case with an antecedent; now credits "secondary NPH" / "secondary normal pressure hydrocephalus", "communicating hydrocephalus", G91.0, G91.9 and labels naming the meningitic antecedent (`post-meningitic NPH`, `meningitis NPH` and their long forms).
- `key_clinical_evidence`: "(Marmarou 2005)" written as the key `[Marmarou_2005]`.
- Checks: `perfect_agent.py -v` pass, `case_io.py check` clean, `test_case_guards -k NPH-` pass. Not yet in `DISCRIMINATOR_CONDITIONS`: the post-tap follow-up's prose `assessment_type` is deliberate until the timing discriminator lands (CENTRAL C2 in the decisions file).

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (timing discriminator, NPH R4; decisions Q2 and CENTRAL C2). No clinical text changed.

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment.timing` | added `baseline` |
| `followup_outputs[1]` (`request_post_reassessment`) | `assessment_type` "gait_and_balance_timed (post-tap reassessment)" -> `gait_and_balance_timed`; `timing: post_intervention` added |
| `ground_truth.action_criteria[action-6-perform-clinical-assessment]` | `required_arguments.timing: baseline` (the schema default, so a call that omits it still matches; a post-tap call no longer does) |
| `ground_truth.action_criteria[action-post-tap-gait-reassessment]` | `required_arguments.timing: post_intervention`; importance recommended -> required (Reviewer 1: gait before and after the tap) |
| `ground_truth.sequence_constraints` | soft: `action-4-analyze-csf` before `action-post-tap-gait-reassessment` [Nakajima_2021] |
| `ground_truth.stop_rule.required_before_assessment` | `action-post-tap-gait-reassessment` added |

Scoring change for re-review: the post-tap reassessment is now required and is credited only by a call with `timing: post_intervention`; the baseline order is answered by the baseline report and the reassessment order by the post-tap report (MockServer secondary discriminator).
