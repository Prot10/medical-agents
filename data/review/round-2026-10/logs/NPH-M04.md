# NPH-M04
Reviewer status: R1 none, R2 none (NPH has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `nph`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for NPH. The case was corrected against plan NPH (classes C1 to C20) and the July 2026 tool review. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search`, criterion `action-1-search-medical-literature` | Recommended literature criterion with a leaking stored output (C1). | FIXED: criterion deleted; initial and fallback literature null. |
| C | minor | `followup_outputs[0]` (`request_drug_interactions_gabapentin_shunt`) | Perioperative gabapentin advice as a tool result (C2). | FIXED: deleted; drug-interaction outputs null; gabapentin must added (C2 canonical). |
| D | major | `patient.chief_complaint`, `patient.history_present_illness` | Complaint asked "whether this is NPH or Alzheimer's"; HPI "admitted for NPH evaluation", outside Evans 0.32 and callosal angle 88 degrees, "concerned this could be NPH", outpatient MoCA 22/30 equal to the baseline, and TSH 1.8 although thyroid labs are now a recommended step (C3, C4, timeline leak). | FIXED: complaint keeps her fear of Alzheimer's disease (the anchor) without naming NPH; HPI says the outside MRI was reported as showing enlarged ventricles (images not available); MoCA and TSH sentences removed; PMH "currently euthyroid" removed so the labs answer it. |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG 24 s, 10-metre walk 19 s and the MoCA profile in the exam (C4). | FIXED: qualitative gait; "formal cognitive screening reported separately". |
| D | blocker | `initial_tool_outputs.clinical_assessment` | Pre-tap call returned the post-tap result and a verdict (C6). | FIXED: baseline only (TUG 24 s, 10-metre walk 19 s in 27 steps, turn 6 steps, MoCA 22/30); `criteria_met` and `pre_post_comparison` null. |
| A | major | `followup_outputs` | No post-tap reassessment, no cognitive screen, no spine study (C6, C14). | FIXED: `[0]` cognitive screen (MoCA 22/30 itemised to sum 22, recall 3/5 free and 5/5 cued); `[1]` cervical spine MRI (`request_spine_MRI`, region spine, modality MRI: post-discectomy C5-C6 with patent canal, normal cord signal, mild residual right C5-C6 foraminal narrowing matching the residual C6 radiculopathy); `[2]` post-tap reassessment (TUG 20.5 s at 2 h, 19 s at 24 h, 10-metre walk 15.5 s, MoCA 23; identical to CSF). |
| C | major | `initial_tool_outputs.mri` | Brain MRI report contained a cervical spine finding and a "Cervical spine MRI" impression item (C7); no technique, temporal horns, hippocampi, aqueduct, Fazekas grade. | FIXED: spine content removed (now in the spine MRI); technique; Evans 0.32; DESH stated with both components (the report already described tight convexity sulci with Sylvian widening); callosal angle 88 (acute); temporal horns out of proportion to hippocampi (MTA 1); Fazekas 1; patent aqueduct; no obstruction; descriptive impression. |
| D | major | `initial_tool_outputs.csf.interpretation`, `.special_tests` | Prose with "improved" (C5); differential "Lymphocyte". | FIXED: canonical interpretation (21% at 24 h); special_tests figures; "Lymphocytes". |
| C | minor | `initial_tool_outputs.labs` | HIV under "Baseline workup" (C9). | FIXED: `Serology` panel; all `clinical_significance` null; interpretation leads with the thyroid result. |
| C | major | `ground_truth.action_criteria` | Labs optional with four named panels although thyroid status is the case's reversible question; no spine, cognitive or post-tap criterion. | FIXED: MRI (required), labs `{}` (recommended, thyroid status, plan M04), baseline gait (required), cognitive screen (optional), cervical spine MRI `action-spine-mri` `order_body_imaging {"study": "spine_MRI"}` (recommended), CSF (required), post-tap (recommended); case-specific rationales and evidence. |
| B | minor | `ground_truth.sequence_constraints`, `.stop_rule`, `.avoided_actions` | As M01. | FIXED: canonical constraints; stop rule three ids, max 1; three waste entries added, rationales rewritten. |
| C | major | `ground_truth.assessment.required_recommendations` | Process musts (C11). | FIXED: referral on the 21% response, DESH with acute callosal angle and normal-pressure CSF; gabapentin review with the dose unchanged across the tap; confirm euthyroid status; falls prevention (two falls). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Wrong DESH/triad prohibition (C12). | FIXED: LP-before-MRI; canonical ventriculomegaly-alone; AD prohibition kept but rewritten for this patient (AD is the stated worry, so it is in question here); cervical-disease prohibition; normal ageing. |
| C | major | `ground_truth.differential` | CSM and VCI `high`; PD, AD, atrophy `moderate` after the work-up (C13). | FIXED: CSM `low` citing the spine MRI and the absent UMN signs; VCI `low` (Fazekas 1); PD, AD (MTA 1, cued recall despite maternal AD), atrophy (DESH) and secondary hydrocephalus `low`. |
| C | major | `ground_truth.key_clinical_evidence` | Template items (DESH required, 50-80% sensitivity, tier sentence). | FIXED: six case items. |
| B | minor | `ground_truth.red_herrings` | Myelopathy data_point ("decompression / fusion for spondylotic myelopathy") does not match the PMH; interpretations did not cite the spine MRI or the TSH. | FIXED: data_points quote the PMH entries; interpretations name the cervical MRI and TSH 1.8 with free T4 1.3. |
| B | minor | `fallback_tool_outputs.ct`, `.echo` | Normal-ventricle CT; no `echo_type` (C18). | FIXED: ventriculomegaly CT (Evans about 0.32); "TTE". |
| E | minor | `metadata` | Stale vocab gap, counts, variant description. | FIXED. |
| - | check | plan 3.6 | perfect_agent ok (spine MRI from `followup[1]`, post-tap from `followup[2]`); guards pass; hijack probe as M01; `interpret_labs {"panels": ["TSH", "free_T4"]}` returns the case panel. Patient grep clean. Pre-existing em dashes in unedited HPI sentences left. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The patient block keeps her fear of Alzheimer's disease but no longer names NPH, quotes the outside Evans index or callosal angle, or gives the MoCA, TUG or a TSH value. The brain MRI drops its cervical spine content and now reports Evans 0.32, DESH (tight convexity sulci with enlarged Sylvian fissures, as the old text described), an acute callosal angle of 88 degrees, enlarged temporal horns with MTA 1, Fazekas 1 and a patent aqueduct. A new recommended cervical spine MRI shows the C5-C6 discectomy with a patent canal and normal cord signal, and the differential now has recurrent myelopathy low. Thyroid labs are recommended and normal on levothyroxine. The baseline gait (TUG 24 s, 10-metre walk 19 s, MoCA 22/30) is separate from the post-tap reassessment and CSF report (TUG 20.5 s at 2 hours, 19 s at 24 hours, 21%; 10-metre walk 15.5 s; MoCA 23). Literature and drug-check steps are gone. Musts: shunt referral, gabapentin review with constant dosing across the tap, euthyroid confirmation, falls prevention. All alternatives are low after the work-up.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R2: `[Nakajima_2021]` not yet in the NPH criteria pack.
- Plan R4: post-tap criterion shares the baseline pattern.

## Open questions for Andrea (judgment calls you could not settle)

- Plan deviation, decided: the plan lists M04 among the cases without DESH (C7), but the original MRI described "moderate tight sulci at high convexity with sylvian fissure widening", which is DESH. I kept DESH present (both components stated) rather than editing a finding out; nothing for Andrea to decide unless the lead wants all no-DESH cases uniform.
- AD prohibition: the plan keeps it only in P01 and P09; I kept a rewritten one here because the chief complaint makes Alzheimer's disease the patient's explicit worry, which is the situation the plan's "wherever AD is in question" rule describes.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the whole final case and its diff against fa1d22e6.
- Checked: the deviation from the plan (DESH kept) is correct: the original MRI described "tight sulci at high convexity with sylvian fissure widening", which are both DESH components. Spine content is out of the brain MRI and in a recommended cervical spine MRI served by the case (probe: `order_body_imaging {"study": "spine_MRI"}` returns the follow-up); its right C5-C6 foraminal narrowing matches the residual right C6 radiculopathy. Thyroid labs recommended and normal; euthyroid and gabapentin musts present; gabapentin 300 mg three times daily = 900 mg/day as the key evidence says. Figures identical across reports (TUG 24 to 20.5 s = 15%, to 19 s = 21%; 10-metre walk 19 to 15.5 s = 18%). The kept AD prohibition is reasonable (the chief complaint makes AD the patient's stated worry).
- Found and fixed (B, minor): the cognitive-screen attention item read "4/6: one letter-tapping error, serial sevens 2/3"; under MoCA rules one tapping error still scores 1, which makes 5/6 and a total of 23, not 22. Now "two letter-tapping errors", so the items sum to 22.
- Found and fixed (B, minor): the spine MRI gave a C5-C6 canal AP diameter of 11 mm (relative stenosis range) beside "canal patent ... no canal stenosis". Now 13 mm.
- perfect_agent -v ok, case_io check clean for the case, test_case_guards pass.

## Close-out (24 Oct 2026)

Condition close-out (`plans/NPH-decisions.md`); no clinical data the agent receives changed.
- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions nph`): code G91.0 removed (ICD-10-CM communicating hydrocephalus, which covers secondary NPH, a different entity from iNPH); labels unchanged, G91.2 and G91.9 accepted.
- Checks: `perfect_agent.py -v` pass, `case_io.py check` clean, `test_case_guards -k NPH-` pass. Not yet in `DISCRIMINATOR_CONDITIONS`: the post-tap follow-up's prose `assessment_type` is deliberate until the timing discriminator lands (CENTRAL C2 in the decisions file).
