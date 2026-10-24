# NPH-S11
Reviewer status: R1 none, R2 none (NPH has no notes file; only the July 2026 tool review applies) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | NPH was not annotated in this round; no note id exists for this case. The July 2026 tool review (`condition_tool_guidance.yaml` key `nph`) is applied through the plan classes below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A/C | major | `ground_truth.action_criteria[action-1-search-medical-literature]`, `stop_rule`, `followup_outputs[0]` (`request_literature_search`), `fallback_tool_outputs.literature_search` | Literature search `required` and in the stop rule; follow-up repeated the old "sensitivity 50-80%" and an empty Williams finding (C1, ruling 5, F4). | FIXED: criterion, follow-up and the "general" literature fallback deleted; id removed from the stop rule; `fallback_tool_kinds.literature_search` removed. |
| D | major | `patient.history_present_illness`, `.chief_complaint` | HPI quoted the index MRI (Evans 0.36, callosal angle 72 degrees, DESH) and "admitted for inpatient tap trial evaluation", "referred for inpatient tap trial"; chief complaint "referred for tap test evaluation" (C3). | FIXED: outside MRI reported qualitatively (images not available), referral question. The CT of 3 years ago ("minimal periventricular leukoaraiosis") and the outpatient MMSE 25/30 stay: both precede the encounter and differ from the index results (C3, C4). |
| B | minor | `patient.clinical_history.past_medical_history`, `.history_present_illness` | "Diet-controlled" diabetes while on metformin (C9). | FIXED: "Type 2 diabetes mellitus on metformin" in both. |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG 26 s, 10-m walk 19 s, turn step count, MoCA 23/30 with domain losses and fluency count in the exam (C4). The listed losses (3 + 2 + 1) also did not sum to 23. | FIXED: qualitative gait and mental status; numbers moved to the baseline report and the cognitive-screen follow-up, with subscores that sum to 23. |
| D | blocker | `initial_tool_outputs.clinical_assessment` | Baseline report carried the post-tap result and "positive tap test" (C5, C6). | FIXED: baseline only (TUG 26 s with cane, 10-m walk 19 s in 29 steps, turn 8 steps, MoCA 23/30). |
| A | major | `followup_outputs` | No post-tap reassessment, no case cognitive screen (C6). | FIXED: `request_moca_cognitive_screen` (MoCA 23/30; attention, executive and fluency 9 words as in the original exam; recall 3/5 free, 5/5 cued) and `request_post_reassessment` (TUG 21 s at 2 h, 17 s at 24 h, 10-m 13 s, MoCA 26). |
| D | minor | `initial_tool_outputs.csf.interpretation` | Already figure-based; brought to the canonical form (C5). | FIXED: values kept (40 mL, 26/21/17 s, 19/13 s, MoCA 23/26); percentages checked (19%, 35%, 32%); CSF/serum glucose 68/108 = 0.63 consistent with the labs. |
| C/D | major | `initial_tool_outputs.mri` | "No abnormal enhancement on post-contrast sequences" (contrast is not needed, C7); periventricular rim called "consistent with transependymal CSF seepage" (mechanism read into the image); "Fazekas grade 2 ... no confluent" with deep foci described as scattered; no temporal horns, fourth ventricle or MTA. | FIXED: technique line without contrast; periventricular halo described, not interpreted; Fazekas 2 stated as periventricular halo with non-confluent subcortical foci, no lacunes; temporal horns, fourth ventricle, MTA 1 added; canonical impression. The red herring's `field_path` still points at `findings[6]`, the white matter finding. |
| B | minor | `initial_tool_outputs.labs` | HbA1c reference "<6.5" unflagged at 6.4% (C9); interpretive interpretation; RPR and HIV under Metabolic. | FIXED: HbA1c reference <5.7%, flagged high; glucose labelled fasting; Serology panel; `clinical_significance` null; pattern-only interpretation and abnormal summary. |
| B | major | `fallback_tool_outputs.ct` | Normal ventricles in the CT fallback (C18). | FIXED: canonical CT fallback (Evans about 0.36). |
| E | minor | `fallback_tool_outputs.echo`, `.cardiac_monitoring`, `.ecg` | "age-appropriate", "without haemodynamic significance" phrasing; no `echo_type`; removed `clinical_correlation`. | FIXED: findings stated; `echo_type: TTE`. |
| C | major | `ground_truth.assessment.required_recommendations` | Five process musts and "recognise that the white matter changes are a distractor" (not management) (C11). | FIXED: referral (35% TUG, DESH, normal-pressure CSF) and falls prevention (two near-falls, freezing, cane). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "Do not diagnose iNPH ... without confirming DESH, callosal angle <90, normal opening pressure and clinical triad" is wrong under F1 and F2 (C12). | FIXED: canonical ventriculomegaly prohibition; small-vessel prohibition reworded to include not withholding referral for Fazekas 2 change [Tisell_2011]; diabetes and ageing prohibition shortened; LP-before-MRI kept. |
| C | major | `ground_truth.differential` | VCI high, AD and PD moderate after DESH and a 35% tap (C13). | FIXED: VCI moderate (Fazekas 2); AD (mother with memory problems, MTA 1), PD, atrophy and spondylotic myelopathy low with case data. |
| B | minor | `ground_truth.red_herrings[0].correct_interpretation` | Called Fazekas 2 "mild ... age-appropriate" and said the tap "confirms iNPH". | FIXED: one sentence, Fazekas 2 non-confluent without lacunes, does not explain the ventricles or the tap response, does not preclude shunting. |
| C/E | major | `ground_truth.key_clinical_evidence` | Triad and DESH as requirements, "sensitivity 50-80%", tier sentence (C19). | FIXED: rebuilt from F1 to F5 with case figures and the Tisell 2011 white-matter line. |
| A | minor | `ground_truth.action_criteria`, `.avoided_actions`, `.stop_rule`, `.sequence_constraints` | Labels equal to rationales, `NPH_pack`, fixed lab panels, generic waste rationales, allowance 0. | FIXED per plan 3.1 to 3.5. |
| E | minor | `patient...family_history`, `...social_history.alcohol`, HPI, `metadata` | Em dashes; stale `vocab_gap`; counts; "Clean textbook straightforward" description and a comparison with other cases. | FIXED; `last_revised` 2026-10-24. |

## Changes, in one paragraph a physician can read before re-reviewing

A 70-year-old woman with hypertension and type 2 diabetes on metformin and 18 months of magnetic gait with freezing, urge incontinence and slowed thinking. The HPI no longer gives the index MRI measurements or the tap-trial referral; the CT of 3 years ago and the outpatient MMSE 25/30 stay as prior history. Pathway: brain MRI (required; Evans 0.36, both DESH components, callosal angle 72 degrees, temporal horns enlarged, flow void, Fazekas 2 non-confluent without lacunes, MTA 1; no contrast), optional labs (fasting glucose 108 mg/dL and HbA1c 6.4% now flagged), baseline timed gait (required; TUG 26 s with cane, 10-m walk 19 s), optional MoCA (23/30, attention and executive deficits with relatively preserved recall), CSF tap test (required; opening pressure 13 cmH2O, normal content, 40 mL) and post-tap reassessment (recommended; TUG 17 s at 24 hours, 35% faster; MoCA 26). The required literature step was removed. Musts: neurosurgical referral for a programmable-valve shunt, falls prevention. Prohibitions: tap before MRI, iNPH from ventriculomegaly alone, attributing the syndrome to small-vessel disease or withholding referral for it (Tisell 2011), attributing the gait to diabetes or age. Differential: VCI moderate, the rest low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R2: `[Nakajima_2021]` cited before the key exists in the pack.
- Plan R4, R5, R7 as in NPH-S08.

## Open questions for Andrea (judgment calls you could not settle)

None. A falls must was added beyond the plan's "referral" pick because the case documents two near-falls, freezing and a cane.

## Verification

Checked against `plans/NPH.md` (sections 2 to 4 and the per-case entry), ROUND_POLICY and PATTERNS; NPH has no notes file, so there is no note id to account for. Read the whole final case (flattened, every field) and compared it with the pre-round version (`1fd43d22~1`). Verified: patient block free of Evans, callosal angle, DESH, NPH, hydrocephalus, tap, shunt, TUG and MoCA results; literature and drug-interaction outputs null with no such follow-ups; MoCA subscores sum to the total and match the exam orientation; TUG and 10-m percentages recomputed from the stored seconds and identical in the baseline report, the CSF report, the post-tap follow-up and the criteria; CSF/serum glucose ratio consistent with the lab glucose; Evans index identical in the MRI, CT fallback (within 0.01), criteria and key evidence; Fazekas grade matches the VCI likelihood (plan C13); musts, prohibitions and differential match plan section 4; discriminator values (`holter_24h`, `TTE`, CSF assay terms) are vocabulary terms; criteria order and tiers per plan 3.1, constraints per 3.4, stop rule per 3.5. Hijack check (MockServer through `NeuroBenchEnvironment`): cognitive screen then "baseline timed gait before tap test" returns the baseline (no `pre_post_comparison`); after the CSF call "post-tap reassessment at 24 hours" returns the follow-up; "repeat timed gait after lumbar puncture" re-serves the baseline (plan R5, already logged). `perfect_agent.py -v`, `case_io.py check` and `test_case_guards -k` pass after the changes below.

Found and changed:
- `ground_truth.action_criteria[action-post-tap-gait-reassessment].rationale`: template sentence (C19); rewritten for her cane, 40 mL tap and Fazekas 2 change.
- `initial_tool_outputs.labs.panels`: the HbA1c row sat in the BMP panel, which does not contain HbA1c; moved unchanged to the Metabolic panel (as in NPH-S09).
- Kept: `[Tisell_2011]` on the CSF criterion and in the small-vessel prohibition, where the case question is the white matter change. The outpatient MMSE 25/30 in the HPI is a different instrument from the index MoCA 23/30 and stays (C4).
- Nothing else found.

## Condition audit (NPH auditor, 24 Oct 2026)
- `analyze_csf {"special_tests": ["HSV_PCR"]}` added to `avoid-waste-generic-csf-assays`, as in the other 24 NPH cases (plan 3.3, PCR panels).
- Checks after the edits: `perfect_agent.py` passes for all 30 NPH cases, `case_io.py check` clean.

## Close-out (24 Oct 2026)

Condition close-out (`plans/NPH-decisions.md`); no clinical data the agent receives changed.
- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions nph`): code G91.0 removed (ICD-10-CM communicating hydrocephalus, which covers secondary NPH, a different entity from iNPH); labels unchanged, G91.2 and G91.9 accepted.
- `key_clinical_evidence`: the 10% TUG threshold is no longer attributed to `[Nakajima_2021]`, which sets no numeric tap-test cut-off; it is stated as a commonly used threshold that no guideline fixes (the tap protocol keeps its Nakajima citation where the sentence states it).
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

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
