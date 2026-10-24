# NPH-S08
Reviewer status: R1 none, R2 none (NPH has no notes file; only the July 2026 tool review applies) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | NPH was not annotated in this round; no note id exists for this case. The July 2026 tool review (`condition_tool_guidance.yaml` key `nph`) is applied through the plan classes below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A/C | major | `ground_truth.action_criteria[action-1-search-medical-literature]`, `followup_outputs[0]` (`request_hypothyroidism_cognitive_contribution`) | Literature search as a recommended clinical step; the follow-up was the thyroid-contribution question disguised as a search (C1, ruling 5). | FIXED: criterion and follow-up deleted; initial and fallback `literature_search` null. The thyroid point is now the recommended labs, a must, a prohibition, a differential entry and the red herring. |
| C | minor | `followup_outputs[1]` (`request_levothyroxine_perioperative`) | Drug check carried perioperative anaesthetic advice, no interaction (C2). | FIXED: deleted; `drug_interactions` null. |
| D | major | `patient.history_present_illness` | HPI gave the thyroid result the recommended labs return ("TSH 1.8 mIU/L, well controlled", identical to the lab value) and the outside CT as "significant ventriculomegaly" (C3, timeline leak). | FIXED: thyroid function "not rechecked for over a year" (which is what makes the lab criterion recommended); outside CT reported qualitatively, images not available; referral question. The fall that caused the contusion is now explicit (she struck her forehead in one of the falls). |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG 26 s, 10-m walk 20 s, MoCA 22/30 and recall 2/5 in the exam (C4). | FIXED: qualitative gait only (en-bloc turning added, consistent with the report); "formal cognitive screening reported separately". |
| D | blocker | `initial_tool_outputs.clinical_assessment` | Baseline report contained the post-tap result, `criteria_met` keys and the engineering sentence (C5, C6). | FIXED: baseline only (TUG 26 s without aid, 10-m walk 20 s in 30 steps, turn 7 steps, MoCA 22/30), descriptive impression. |
| A | major | `followup_outputs` | No post-tap reassessment, no case cognitive screen (C6). | FIXED: `request_moca_cognitive_screen` (MoCA 22/30, subscores sum to 22, recall 2/5 free and 4/5 cued, orientation 6/6 as in the exam) and `request_post_reassessment` (TUG 19 s at 2 h, 17 s at 24 h, 10-m 13 s, MoCA 25, as in the CSF report). |
| D | major | `initial_tool_outputs.csf.interpretation`, `.special_tests` | "Positive tap trial" verdict (C5). | FIXED: canonical figures-only text; values kept (40 mL, 26/19/17 s, 20/13 s, MoCA 22/25). Percentages checked: 27%, 35%, 35%. |
| C/D | major | `initial_tool_outputs.mri` | Missing technique, temporal horns, fourth ventricle, Fazekas, MTA, no-obstruction line; "transependymal" in the impression; no statement on post-traumatic change although she had a head contusion (C7). | FIXED: full marker set, stored values kept (Evans 0.38, DESH, callosal angle 73 degrees, flow void), Fazekas 1, MTA 1, no subdural collection, contusion or haemosiderin; canonical impression. |
| B | minor | `initial_tool_outputs.labs` | HIV "Baseline workup" panel with interpretive significance; RPR under Metabolic (C9). | FIXED: Serology panel, `clinical_significance` null, pattern-only interpretation; values unchanged. |
| C | minor | `ground_truth.action_criteria[action-3-interpret-labs]` | Optional labs with a fixed panel list although the case's red herring is hypothyroidism (C9: S08 recommended). | FIXED: `interpret_labs {}`, recommended, label "Thyroid function and targeted labs for reversible contributors". |
| B | major | `fallback_tool_outputs.ct` | CT fallback reported normal ventricles (C18). | FIXED: canonical CT fallback (Evans about 0.38, no fracture or contusion). |
| A | minor | `fallback_tool_outputs.echo`, `.ecg` | No `echo_type`; removed `clinical_correlation` field on the ECG. | FIXED. |
| C | major | `ground_truth.assessment.required_recommendations` | Four process musts and a generic referral (C11). | FIXED: referral (35% TUG, DESH, normal-pressure CSF), confirm euthyroid status and continue levothyroxine 75 mcg, falls prevention (three falls, lives alone). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Wrong triad/DESH requirement; AD prohibition copied (C12). | FIXED: canonical ventriculomegaly prohibition; AD prohibition removed; hypothyroidism prohibition added; normal-ageing prohibition kept (her PCP attributed the symptoms to ageing) and reworded; LP-before-MRI kept. |
| C | major | `ground_truth.differential` | VCI high, PD, AD and atrophy moderate after DESH and a 35% tap; hypothyroidism, the case's own red herring, absent (C13, ruling 7). | FIXED: all low with case data; hypothyroid cognitive impairment added (low, TSH and free T4 normal); secondary hydrocephalus reasoning names the contusion that post-dated onset. |
| B | minor | `ground_truth.red_herrings` | Thyroid red herring relied on the HPI TSH, now removed. | FIXED: interpretation cites the lab report (TSH 1.8, free T4 1.2). Added a second red herring for the head contusion (visible in the HPI): it post-dated the gait decline by 20 months and the MRI shows no post-traumatic change. |
| C/E | major | `ground_truth.key_clinical_evidence` | Triad and DESH as requirements, "sensitivity 50-80%", tier sentence (C19). | FIXED: rebuilt from F1 to F5 with case figures. |
| A | minor | `ground_truth.action_criteria`, `.avoided_actions`, `.stop_rule`, `.sequence_constraints` | Labels equal to rationales, `NPH_pack`, generic waste rationales, stop allowance 0. | FIXED per plan 3.1 to 3.5 (ids kept; cognitive screen and post-tap criteria added; advanced imaging, neuropsych, generic CSF assays as waste). |
| E | minor | `patient.history_present_illness`, `...family_history`, `metadata` | Em dashes; stale phase-contrast `vocab_gap`; counts of removed tools; "Straightforward ... florid" description for a `moderate` case. | FIXED; `last_revised` 2026-10-24. |

## Changes, in one paragraph a physician can read before re-reviewing

A 72-year-old woman with two years of magnetic gait with freezing, urge incontinence and executive slowing, on levothyroxine. The HPI no longer gives her TSH (thyroid function now "not rechecked for over a year") or the outside CT finding; it makes explicit that the minor head contusion four months ago came from one of her falls. Pathway: brain MRI (required; Evans 0.38, both DESH components, callosal angle 73 degrees, temporal horns enlarged, flow void, Fazekas 1, MTA 1, no subdural collection or post-traumatic change), recommended labs (TSH 1.8 mIU/L, free T4 1.2 ng/dL, otherwise normal), baseline timed gait (required; TUG 26 s, 10-m walk 20 s), optional MoCA (22/30 with cueing benefit), CSF tap test (required; opening pressure 13 cmH2O, normal content, 40 mL) and post-tap reassessment (recommended; TUG 17 s at 24 hours, 35% faster; MoCA 25). Literature and the levothyroxine drug check were removed. Musts: neurosurgical referral for a programmable-valve shunt, confirm euthyroid status and continue levothyroxine 75 mcg, falls prevention. Prohibitions: tap before MRI, iNPH from ventriculomegaly alone, blaming hypothyroidism, blaming ageing. Differential all low, including hypothyroid cognitive impairment and post-traumatic hydrocephalus.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R2: `[Nakajima_2021]` cited before the key exists in the pack.
- Plan R4 and R5: post-tap criterion shares the baseline pattern; "repeat gait after lumbar puncture" re-serves the baseline (no leak).
- Plan R7: an `order_specialized_test {neuropsych_battery}` order (waste) is answered by the library with "Cognitive performance within normal limits across all domains", which contradicts the case's MoCA 22/30. The same holds for every NPH case without an authored battery.

## Open questions for Andrea (judgment calls you could not settle)

None.

## Verification

Checked against `plans/NPH.md` (sections 2 to 4 and the per-case entry), ROUND_POLICY and PATTERNS; NPH has no notes file, so there is no note id to account for. Read the whole final case (flattened, every field) and compared it with the pre-round version (`1fd43d22~1`). Verified: patient block free of Evans, callosal angle, DESH, NPH, hydrocephalus, tap, shunt, TUG and MoCA results; literature and drug-interaction outputs null with no such follow-ups; MoCA subscores sum to the total and match the exam orientation; TUG and 10-m percentages recomputed from the stored seconds and identical in the baseline report, the CSF report, the post-tap follow-up and the criteria; CSF/serum glucose ratio consistent with the lab glucose; Evans index identical in the MRI, CT fallback (within 0.01), criteria and key evidence; Fazekas grade matches the VCI likelihood (plan C13); musts, prohibitions and differential match plan section 4; discriminator values (`holter_24h`, `TTE`, CSF assay terms) are vocabulary terms; criteria order and tiers per plan 3.1, constraints per 3.4, stop rule per 3.5. Hijack check (MockServer through `NeuroBenchEnvironment`): cognitive screen then "baseline timed gait before tap test" returns the baseline (no `pre_post_comparison`); after the CSF call "post-tap reassessment at 24 hours" returns the follow-up; "repeat timed gait after lumbar puncture" re-serves the baseline (plan R5, already logged). `perfect_agent.py -v`, `case_io.py check` and `test_case_guards -k` pass after the changes below.

Found and changed:
- `ground_truth.action_criteria[action-post-tap-gait-reassessment].rationale`: template sentence (C19); rewritten for her unaided TUG, 40 mL tap and freezing.
- `ground_truth.action_criteria[action-4-analyze-csf].citations`: `[Tisell_2011]` removed (not a tap-test source; ruling 8).
- `ground_truth.red_herrings[1].data_point`: "Minor head contusion four months ago" no longer appears anywhere the agent can see: the worker rewrote the HPI to "Four months ago she struck her forehead in one of the falls". Set the data point to that HPI text (C20: the data point must be visible). `red_herrings[0].data_point` likewise set to the PMH text "Hypothyroidism (well-controlled)".
- Nothing else found: the TSH removed from the HPI (it was the result of the now-recommended labs) and the "not rechecked for over a year" wording are correct.

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
