# ALS-P02
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 1bca43b9-d0b4-415c-abb7-9eedb23fba0c | FIXED | `ground_truth.diagnosis.accepted[0]` "Familial ALS, C9orf72 pathogenic repeat expansion, early symptomatic onset" -> "Thyrotoxicosis from levothyroxine over-replacement in a C9orf72 repeat-expansion carrier, ALS criteria not met"; `icd_codes[0]` G12.21 -> E05.90. Appended ALS synonyms and G12.2x codes not hand-edited (CENTRAL) |
| b11bd1f7-cb85-4893-84ce-a56cc4966ded | FIXED | Thyroid correction is `required_recommendations[0]` (reduce levothyroxine with endocrinology, recheck TSH/free T4 in 6-8 weeks, consider residual Graves activity because TSI is positive); lab criterion now requires `free_T4`; thyrotoxicosis is the label; reassessment once euthyroid is must 2; pearl 1 |
| 9db62330-df12-4537-b776-663ba6ee3f08 | FIXED | `initial_tool_outputs.specialized_test.impression` replaced by the plan text ("... No current electrodiagnostic evidence of motor neuron disease; repeat if objective weakness or wasting progresses."); thyrotoxicosis mentions removed from findings (cross-modality); "median sural" -> "Sural normal"; `recommended_actions` = repeat only if objective progression |
| 9200b13f-974c-4bb0-96cd-311d14d6a302 | FIXED | Criterion `action-2-check-drug-interactions` and follow-up `check_riluzole_sertraline_interaction` deleted; replaced by musts for thyroid correction, genetic counselling, objective baseline with follow-up and EMG only if progression; prohibition "Do not diagnose ALS or start riluzole ..." |
| 6fa1a30b-0d45-4a44-b76f-c11f74706554 | FIXED | Genetic report states only the finding (positive C9orf72; other four genes negative) with no diagnosis; second red herring "C9orf72 pathogenic repeat expansion" (carrier status is risk, not diagnosis); pearl 3; differential "Early symptomatic C9orf72-associated ALS" low |
| 948c5c90-11c4-49ee-bb8e-0ebc8a6c15ea | FIXED | `required_recommendations` replaced by the five musts of the plan (thyroid correction, ALS not established and reassess when euthyroid, post-test counselling with relatives and deferral of testing in her teenage children, objective baseline and EMG only on progression, support for anxiety and depression); "Initiate riluzole" removed |
| 2da3016c-756b-4c74-9eec-87ab3c3b55fa | FIXED | `red_herrings[0]` rewritten with the note's wording: anxiety may amplify perception, thyrotoxicosis is the current medical explanation, ALS not confirmed (no UMN signs, no EMG denervation) |
| e76c4980-b433-4630-a780-9880ffc7d1f3 | FIXED | Respiratory criterion `optional`, relabelled "objective baseline while ALS is not established" with a rationale that it neither supports nor excludes ALS; output impression no longer framed as ALS management |
| a332a5e7-9489-415d-be1f-3155e2772691 | FIXED | AMX0035 removed with the whole riluzole output (see 9200b13f) |
| 785155c1-e3e9-44e8-902e-59eba7f0d219 | FIXED | Same as 1bca43b9, b11bd1f7 and 948c5c90: no ALS label, no riluzole, thyroid correction, counselling, neurological follow-up, repeat EMG only if it evolves |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | TSH 0.1 and free T4 2.1 values and reasoning about thyrotoxic myopathy/neuropathy (labs are scored), and "ordered electrodiagnostic testing" | FIXED: replaced by "Her primary care physician referred her for neurological evaluation." (fatigue, poor sleep, weight change and the levothyroxine history remain as clues) |
| D | minor | `patient.neurological_exam.additional` | Repeated the family history and anxiety as synthesis | FIXED: "Widespread visible fasciculations. Examination limited by marked anxiety and possible submaximal effort." |
| B | minor | `patient.clinical_history.past_medical_history` | "Mild obesity" with BMI 28.2 | FIXED: "Overweight (BMI 28)" |
| A/B | major | `initial_tool_outputs.labs` | No blood count, renal or liver values although CBC and CMP were required; template panel names; interpretation names ALS; TSI inside a "Neuromuscular" panel | FIXED: panels per C13 (stored values kept; normal CBC, CMP added); TSI in "Thyroid antibodies"; TSH/free T4 flagged low/high |
| B | minor | `initial_tool_outputs.body_imaging`, `initial_tool_outputs.mri` | Spine report had no findings and an interpretive "to explain the deficit"; brain finding location "Bilateral" | FIXED: plain normal spine findings with numbered impression; brain location "Brain and brainstem" |
| C | major | `ground_truth.differential` | Entries cited "objective EMG denervation" and "UMN signs" that the case does not contain; "Familial ALS without C9orf72" moderate after C9orf72 positive; MMN cited untested anti-GM1 | FIXED: plan set (early symptomatic C9orf72 ALS low; benign fasciculations amplified by anxiety moderate; carpal tunnel syndrome low; MMN very_low) |
| C | major | `ground_truth.key_clinical_evidence` | ALS template pearls (Gold Coast met, CK 2-5x, spondylosis, NIV thresholds, tofersen, engineering text) in a case that is not ALS | FIXED: five pearls of the plan (thyrotoxicosis, simple vs complex fasciculations, carrier is not diagnosis, penetrance and FTD risk, minors) |
| C | minor | `ground_truth.action_criteria[5]` (genetics) | Canonical sporadic rationale says testing is offered "to people with ALS", which she does not have | FIXED: case rationale (father with ALS; in a person without ALS this is predictive testing needing full counselling) |
| C | minor | `followup_outputs[1].output.findings[0]` | "70+ repeat expansions" without method | FIXED: "Pathogenic repeat expansion detected (repeat-primed PCR; more than 70 repeats)" |
| E | minor | `metadata.notes`, `metadata.difficulty_rationale` | Described the case as familial ALS and "genetic panel is required, 5+ required tools" | FIXED: reworded to the new ground truth |
| B | minor | `initial_tool_outputs.labs` | B12 420, folate 10, ESR 8, CRP 2 identical across many ALS cases | FLAGGED, not changed (plan: keep stored values) |

## Changes, in one paragraph a physician can read before re-reviewing
This case is no longer ALS. The ground truth is thyrotoxicosis from levothyroxine over-replacement (TSH 0.1, free T4 2.1, TSI still positive after radioiodine) in a C9orf72 repeat-expansion carrier whose father died of ALS; ALS criteria are not met because she has no upper motor neuron signs, a normal CK and an EMG with simple fasciculations only. The HPI no longer gives the thyroid results; the agent must order the labs (TSH and free T4 now required). The EMG impression states that there is no current electrodiagnostic evidence of motor neuron disease and drops its thyroid commentary. The work-up is EMG, brain MRI, spine MRI and labs, then optional respiratory baseline and a recommended gene panel after counselling; the literature and riluzole steps are deleted. Musts: correct the thyroid excess with endocrinology and recheck in 6-8 weeks; explain that ALS is not established and reassess when euthyroid; post-test genetic counselling including relatives, deferring testing of her teenage children; objective neurological baseline with EMG only if objective progression; support for anxiety and depression. Prohibitions: no ALS diagnosis or riluzole from carrier status and fasciculations; no attribution to anxiety before the thyroid is corrected.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Diagnosis synonyms (plan section 5 item 3): ALS-P02 still carries the appended G12.21 labels ("amyotrophic lateral sclerosis", "ALS", "motor neuron disease", "motor neurone disease", "MND") and codes G12.2, G12.20, G12.23, G12.24, G12.25, which I did not hand-edit. Until they are stripped, an agent answering "ALS" is scored correct. Add E05.90 synonyms if wanted ("thyrotoxicosis", "levothyroxine over-replacement", "iatrogenic hyperthyroidism"). The synonym guard passed with the new `accepted[0]` and `icd_codes[0]`.
- `test_guidance_claims` now reports ALS tier counts that differ from the review-app guidance (respiratory recommended 29/30, genetics optional 29/30, genetics recommended 1): the guidance text needs updating after the round (P02 is the first case changed; P08, P09, S10 will add more).
- Citation keys `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`.

## Open questions for Andrea (judgment calls you could not settle)
- Plan Q1: keep P02 inside condition `als` as a deliberate mimic case with a non-ALS ground truth, and decide whether an answer mentioning both ALS and thyrotoxicosis counts as correct.
- E05.90 (thyrotoxicosis, unspecified) is used as the plan says; ICD-10-CM would code iatrogenic over-replacement as thyrotoxicosis plus T38.1X5A (adverse effect of thyroid hormones). The label names over-replacement as the cause, but TSI is still positive, so residual Graves activity is not excluded (the must asks endocrinology to consider it). Accept the label as worded?

## Verification
Adversarial verifier, 23 October 2026. Checked: all 10 note ids present; label and E05.90 per plan, appended G12.21 synonyms untouched and listed under CENTRAL (until CENTRAL strips them an "ALS" answer still scores as correct: this remains the main open risk of the case); DI criterion and riluzole output deleted; respiratory optional, genetics recommended, sequence constraint 1 only; HPI no longer gives TSH/free T4 values; labs report TSH 0.1, free T4 2.1, TSI 180% consistently with the musts; EMG impression is the plan text, no thyroid commentary, "sural normal"; genetic report states only the finding; red herrings per plan; musts vs prohibitions consistent (no ALS diagnosis or riluzole; anxiety not blamed before thyroid correction); teenage children consistent with the social history; forbidden strings: none.
Found and fixed:
- C, minor, `ground_truth.action_criteria` `action-5-interpret-labs`: the canonical label ("a pre-treatment baseline") and rationale ("the liver and blood-count baseline needed before riluzole") contradict this case, where riluzole is prohibited. Label now "Blood tests for treatable mimics: ..."; rationale "These tests exclude metabolic, endocrine, nutritional and inflammatory mimics of motor neuron disease; ..." (case clause about free T4 kept).
- C, minor, `ground_truth.differential`: the case itself raises residual Graves activity (TSI still 180% after radioiodine, and the first must asks endocrinology to consider it), but the differential did not list it (ruling 7). Added "Persistent or recurrent Graves hyperthyroidism after radioiodine", low, with supports/against from the case. This also documents the worker's open question about the label; note that 100 mcg levothyroxine is not a high replacement dose, which makes residual Graves activity a real alternative for endocrinology to settle.
Perfect-agent and case_io check re-run: clean.

## Condition audit (ALS lead, 23 Oct 2026)
- `followup_outputs[0].output.findings[*].is_abnormal` added (rows carried no abnormality marker), set from each row's reference range as plan C4 prescribes, so all 30 respiratory reports mark abnormal values the same way (values and impression unchanged).

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The case is labelled thyrotoxicosis from levothyroxine over-replacement (E05.90), so the appended ALS synonyms let a plain "ALS" answer score as correct; its synonyms now come from a new E05.90 entry (`conditions: [als]`).
- labels removed: "amyotrophic lateral sclerosis", "ALS", "motor neuron disease", "motor neurone disease", "MND"
- labels added: "thyrotoxicosis", "levothyroxine over-replacement", "iatrogenic thyrotoxicosis", "levothyroxine induced thyrotoxicosis", "exogenous thyrotoxicosis"
- codes removed: G12.2, G12.20, G12.23, G12.24, G12.25
- codes added: E05.9
- `case_io.py validate` OK; `perfect_agent.py` passes.
