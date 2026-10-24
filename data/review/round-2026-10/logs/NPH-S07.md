# NPH-S07
Reviewer status: R1 none, R2 none (NPH has no notes file; only the July 2026 tool review applies) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | NPH was not annotated in this round; no note id exists for this case. The July 2026 tool review (`condition_tool_guidance.yaml` key `nph`) is applied through the plan classes below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A/C | major | `ground_truth.action_criteria[action-1-search-medical-literature]`, `followup_outputs[0]` (`request_sleep_apnea_cognitive_contribution`) | Literature search as a recommended clinical step; the follow-up was the OSA-contribution question disguised as a search (C1, ruling 5). | FIXED: criterion and follow-up deleted; initial and fallback `literature_search` null. The OSA point is now a must (continue CPAP), a prohibition, a differential entry and the red herring. |
| A | minor | `fallback_tool_outputs.drug_interactions` | Empty "general" drug-check block (C2). | FIXED: null; `metadata.fallback_tool_kinds.drug_interactions` removed. |
| D | major | `patient.history_present_illness` | Outside CT quoted with "Evans index estimated at 0.36" (the same value as the index MRI) and "referred for formal NPH workup and admitted for MRI and tap trial" (C3). | FIXED: CT reported qualitatively ("enlarged ventricles; the images are not available"), referral question instead of the diagnosis. The outside cognitive assessment (executive dysfunction, slowed processing) stays as prior history: no score, and the cognitive screen is optional. Falls stated as walking or turning falls without loss of consciousness. |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG 24 s, 10-m walk 18 s, MoCA 23/30, recall 2/5 and Trails B in the exam (C4). | FIXED: qualitative gait only (en-bloc turning added, consistent with the report); mental status "formal cognitive screening reported separately". Numbers moved to the baseline gait report and the cognitive-screen follow-up. |
| D | blocker | `initial_tool_outputs.clinical_assessment` | Baseline report contained the post-tap result, `criteria_met` verdict keys and the engineering sentence (C5, C6). | FIXED: baseline only (TUG 24 s, 10-m walk 18 s in 26 steps, turn 6 steps, MoCA 23/30), descriptive impression. |
| A | major | `followup_outputs` | No post-tap reassessment and no case cognitive screen (C6). | FIXED: `request_moca_cognitive_screen` (MoCA 23/30; subscores sum to 23; recall 2/5 free, 4/5 cued; orientation 6/6 as in the exam) and `request_post_reassessment` (TUG 18 s at 2 h, 16 s at 24 h, 10-m 12 s, MoCA 26, identical to the CSF report). |
| D | major | `initial_tool_outputs.csf.interpretation`, `.special_tests` | "Positive tap trial" verdict (C5). | FIXED: canonical figures-only text; stored values kept (38 mL, 24/18/16 s, 18/12 s, MoCA 23/26). Percentages checked: 25%, 33%, 33%. |
| C/D | major | `initial_tool_outputs.mri` | No technique, temporal horns, fourth ventricle, Fazekas grade, MTA or no-obstruction line; impression called the periventricular signal "transependymal" (C5, C7). | FIXED: full marker set with stored values kept (Evans 0.36, DESH, callosal angle 78 degrees, flow void); periventricular signal graded Fazekas 1 (caps and thin rim, punctate deep foci, no lacunes); MTA 1; canonical impression. |
| B | minor | `initial_tool_outputs.labs` | HIV in a "Baseline workup" panel with interpretive significance; RPR under Metabolic (C9). | FIXED: Serology panel, `clinical_significance` null, pattern-only interpretation; values unchanged. |
| B | major | `fallback_tool_outputs.ct` | CT fallback reported normal ventricles (C18). | FIXED: canonical CT fallback (Evans about 0.36). |
| A | minor | `fallback_tool_outputs.echo`, `.ecg` | Echo had no `echo_type`; ECG carried a removed `clinical_correlation` field. | FIXED: `echo_type: TTE`; ECG rewritten without it. |
| C | major | `ground_truth.assessment.required_recommendations` | Four process musts and a generic referral (C11). | FIXED: referral (33% TUG, DESH, normal-pressure CSF), continue CPAP, falls prevention (three falls). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Wrong "DESH, callosal angle <90 and triad required"; AD prohibition copied with no AD question (C12). | FIXED: canonical ventriculomegaly prohibition, AD prohibition removed, added "Do not attribute the cognitive decline to OSA in a CPAP-adherent patient"; normal-ageing prohibition reworded; LP-before-MRI kept. |
| C | major | `ground_truth.differential` | VCI high and PD, AD, atrophy moderate after DESH and a 33% tap (C13); OSA, the case's own red herring, absent (ruling 7). | FIXED: VCI low (Fazekas 1), PD, AD, atrophy and secondary hydrocephalus low; OSA-related cognitive impairment added, low. |
| C/E | major | `ground_truth.key_clinical_evidence` | Triad and DESH as requirements, "sensitivity 50-80%", tier sentence (C19). | FIXED: rebuilt from F1 to F5 with the case figures. |
| A | minor | `ground_truth.action_criteria`, `.avoided_actions`, `.stop_rule`, `.sequence_constraints` | Labels equal to rationales, `NPH_pack` citations, fixed lab panel list, generic waste rationales, stop allowance 0. | FIXED: plan 3.1 to 3.5 (ids kept; new `action-cognitive-screen`, `action-post-tap-gait-reassessment`; advanced imaging, neuropsych and generic CSF assays as waste). |
| B | minor | `ground_truth.red_herrings[0]` | `data_point` said "CPAP-treated" while the PMH says "CPAP-compliant". | FIXED: matches the PMH; interpretation one sentence. |
| E | minor | `patient.chief_complaint`, `.history_present_illness`, `...social_history.alcohol`, `metadata` | Em dashes; "Slow progressive"; stale phase-contrast `vocab_gap`; counts of removed tools; "Straightforward" description in a case of difficulty `moderate`. | FIXED: dashes replaced, "Slowly progressive", gap removed, counts and description updated, `last_revised` 2026-10-24. |

## Changes, in one paragraph a physician can read before re-reviewing

A 69-year-old man with two years of magnetic gait, urge incontinence and executive slowing, on CPAP for OSA. The patient block no longer gives the outside CT Evans index, the referral diagnosis, or the timed gait and MoCA results. Pathway: brain MRI (required; Evans 0.36, both DESH components, callosal angle 78 degrees, temporal horns enlarged, aqueductal flow void, Fazekas 1, MTA 1, no obstruction), optional targeted labs (normal), baseline timed gait (required; TUG 24 s, 10-m walk 18 s), optional MoCA (23/30, executive and retrieval deficits with cueing benefit), CSF tap test (required; opening pressure 16 cmH2O, normal content, 38 mL removed) and post-tap reassessment (recommended; TUG 16 s at 24 hours, 33% faster; MoCA 26). The literature step about OSA was removed and its point became management: musts are neurosurgical referral for a programmable-valve shunt, continue CPAP, falls prevention; prohibitions are tap before MRI, iNPH from ventriculomegaly alone, attributing the decline to OSA, or to ageing. Differential: VCI, PD, AD, OSA-related impairment, atrophy and secondary hydrocephalus, all low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R2: `[Nakajima_2021]` is cited in musts, evidence and the soft constraint before the key is in the criteria pack.
- Plan R4 and R5: the post-tap criterion shares the baseline pattern; "repeat gait after lumbar puncture" re-serves the baseline (no leak).
- Plan R7: the library answers a (waste) neuropsych battery order with a normal report, which contradicts his MoCA 23/30.

## Open questions for Andrea (judgment calls you could not settle)

None. Hydrochlorothiazide can add urinary frequency; it was left in the medication list without a must, since urge incontinence with a magnetic gait and a tap response is not explained by it.

## Verification

Checked against `plans/NPH.md` (sections 2 to 4 and the per-case entry), ROUND_POLICY and PATTERNS; NPH has no notes file, so there is no note id to account for. Read the whole final case (flattened, every field) and compared it with the pre-round version (`1fd43d22~1`). Verified: patient block free of Evans, callosal angle, DESH, NPH, hydrocephalus, tap, shunt, TUG and MoCA results; literature and drug-interaction outputs null with no such follow-ups; MoCA subscores sum to the total and match the exam orientation; TUG and 10-m percentages recomputed from the stored seconds and identical in the baseline report, the CSF report, the post-tap follow-up and the criteria; CSF/serum glucose ratio consistent with the lab glucose; Evans index identical in the MRI, CT fallback (within 0.01), criteria and key evidence; Fazekas grade matches the VCI likelihood (plan C13); musts, prohibitions and differential match plan section 4; discriminator values (`holter_24h`, `TTE`, CSF assay terms) are vocabulary terms; criteria order and tiers per plan 3.1, constraints per 3.4, stop rule per 3.5. Hijack check (MockServer through `NeuroBenchEnvironment`): cognitive screen then "baseline timed gait before tap test" returns the baseline (no `pre_post_comparison`); after the CSF call "post-tap reassessment at 24 hours" returns the follow-up; "repeat timed gait after lumbar puncture" re-serves the baseline (plan R5, already logged). `perfect_agent.py -v`, `case_io.py check` and `test_case_guards -k` pass after the changes below.

Found and changed:
- `ground_truth.action_criteria[action-post-tap-gait-reassessment].rationale`: template sentence shared by all NPH cases (C19); rewritten for his 38 mL tap.
- `ground_truth.action_criteria[action-4-analyze-csf].citations`: `[Tisell_2011]` (white matter changes paper, not a tap-test source) removed; `[Marmarou_2005]` kept (ruling 8).
- `ground_truth.red_herrings[0].data_point`: the log said it now "matches the PMH", but it read "apnoea" against the PMH "apnea"; set to the PMH text verbatim.
- `patient.history_present_illness`: the last sentence ("His primary care physician referred him for progressive gait difficulty with memory decline and urinary urgency") repeated the opening ("admitted following referral from his primary care physician for a two-year history of progressive gait difficulty, urinary incontinence, and cognitive decline"); deleted as a duplicated sentence (PATTERNS 5).
- Nothing else found.

## Condition audit (NPH auditor, 24 Oct 2026)
- `analyze_csf {"special_tests": ["HSV_PCR"]}` added to `avoid-waste-generic-csf-assays`, as in the other 24 NPH cases (plan 3.3, PCR panels).
- Checks after the edits: `perfect_agent.py` passes for all 30 NPH cases, `case_io.py check` clean.
