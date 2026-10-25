# ALZ-EARLY-P03
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| d82080e9-a7ba-4084-b8f3-c3e9064f28cb | FIXED | `initial_tool_outputs.clinical_assessment` rewritten as a frontal/dysexecutive profile from this case's exam: `amnestic_predominant_profile` false; findings now include behaviour and executive signs (disinhibition, utilization behaviour, go/no-go 4/10 errors, failed Luria sequence, applause sign, grasp and palmomental reflexes, limited insight), informant behavioural history, informant memory history and functional status; impression per C3 skeleton (executive, attention and recall impairment; cue benefit as recorded; 18 months of disinhibition, apathy and impulsive spending followed by memory decline). Storage-type and engineering sentences deleted. bvFTD differential updated (C11). |
| 0c77408a-5b72-402c-a6d7-079e865b96b2 | FIXED | `criteria_met.independence_in_instrumental_activities_lost` true; `scores["severity stage..."]` "mild dementia: instrumental independence lost"; impression names the losses (work, finances, meal planning). |
| 7d03b15b-df53-4abf-80ed-796985924b3e | FIXED | Genetic criterion `action-6-order-specialized-test` now has two alternatives, `genetic_panel:FTD` first and `genetic_panel:early_onset_AD`; new follow-up `request_genetic_panel_ftd` (C9orf72 repeat normal, GRN, MAPT, CHMP2B, TBK1 negative); label and rationale require pre-test counselling and explain the paternal behavioural dementia; canonical counselling must added; soft constraint battery before genetics. |
| b9ec2dbb-7284-42c6-930c-afdfd92ef698 | FIXED | `initial_tool_outputs.mri.additional_observations[1]` "No mass lesions or pathological enhancement post-gadolinium" became "No mass lesion". |
| be4f5858-e001-4a4b-850e-c4bae78c93b3 | FIXED | `ground_truth.key_clinical_evidence` rebuilt (4 items): canonical frontal-AD pearl, memory involvement plus biomarkers adjudicate atypical presentations, AD biomarkers exclude bvFTD under Rascovsky 2011, family history of behavioural dementia and genetic panel scope. Generic amnestic, APOE, B12 and AChEI items deleted. |
| d6c203e3-e64e-4bc2-8d67-08ea7b01d82e | FIXED | Summary comment (amnestic template sections): resolved by the notes above plus the template fixes in Own findings (criteria labels, musts, prohibitions, differential). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.history_present_illness` | "the language difficulties continued to progress": template carry-over from the lvPPA case; no language disorder in this case. | FIXED: "neither improved her behavioral symptoms, and venlafaxine was stopped." (venlafaxine is not on the medication list). |
| B | major | `action-9`, `initial_tool_outputs.csf` | Amyloid PET as the "single optional route"; a CSF order got the library's normal CSF (C2). | FIXED: two alternatives with canonical label, rationale (here: frontal AD versus bvFTD) and expected evidence; new `initial_tool_outputs.csf` concordant with the positive PET (Abeta42 468, Abeta40 11200, ratio 0.042, p-tau181 96, t-tau 612; normal cells, protein, glucose). Probe of every alternative: CSF <- initial, PET <- `followup_outputs[1]`, FDG <- [2], FTD panel <- [3], AD panel <- [4], donepezil check <- [5]; no library answer. |
| C | major | `action-11-check-drug-interactions` | Drug check had no case output at all (only the engineering fallback "(agent not specified...)") and `required_arguments` `{}`. | FIXED: `{"drug": "donepezil"}`, stays optional and last; new follow-up `check_drug_interactions_donepezil` with true content for her medicines (buspirone, levothyroxine, sumatriptan: no significant interaction), pulse 68, bradycardia and GI warnings; expected evidence worded differently from the output. Fallback drug check null. |
| B | major | `action-8.expected_evidence`, `action-10.expected_evidence` | MRI expected evidence claimed "typical AD-pattern temporoparietal volume loss" while the report states posterior parietal volume normal; FDG expected evidence omitted the dominant bifrontal pattern the report gives. | FIXED: both now state what the reports show. |
| C | major | `ground_truth.differential` | bvFTD `high` and psychiatric disorder `moderate` after a work-up that returns AD biomarkers, posterior hypometabolism and frontal release signs (C11). | FIXED: bvFTD low (clinical features listed; AD biomarkers are a Rascovsky exclusion criterion; FTD panel negative); psychiatric low (two failed antidepressants, frontal signs, atrophy); other entries reworded with case data. |
| C | major | `ground_truth.assessment` | Musts restated tool steps and the engineering biomarker must; no financial protection despite $8,000 impulsive spending; no work or driving advice; generic prohibitions (anticholinergics in a patient taking none). | FIXED: musts for informant history, disclosure and planning, financial protection, work and driving, canonical biomarker must, canonical dementia AChEI must with the FTD caveat (NICE NG97 does not recommend AChEI in FTD), genetic counselling, non-drug behavioural management and carer support. Prohibitions: depression attribution, antipsychotics for disinhibition, benzodiazepine for her anxiety, memantine at the mild stage. |
| D | minor | `followup_outputs[0..2]` | Neuropsych units ("40% commission errors %", "1 categories", FBI "32 points" but "32/72" in the impression); PET "STRONGLY POSITIVE" (not binary); tracers null. | FIXED: units corrected; numbered neuropsych impression; binary PET impression with SUVr and plaque density; tracers 18F-florbetapir and 18F-FDG; FDG impression numbered, same content. |
| D | minor | `followup_outputs` (AD gene panel) | Finding "value" was the criterion's expected-evidence sentence. | FIXED: APP, PSEN1, PSEN2 listed negative. |
| B | minor | `initial_tool_outputs.clinical_assessment.scores["Verbal fluency"]` | "8 items in 60 s" while the exam records 8 animals and 5 F-words. | FIXED. |
| B | minor | `initial_tool_outputs.labs` | "BMP" panel for a CMP order, no liver tests. | FIXED: CMP with total protein, albumin, ALT, AST, ALP, bilirubin added (normal); stored values unchanged. |
| B | minor | `fallback_tool_outputs.ecg.intervals.QRS` | Incomplete RBBB reported with QRS 83 ms. | FIXED: 104 ms. |
| D | minor | `fallback_tool_outputs.literature_search` | C8. | FIXED: null; fallback kinds for literature and drug check removed. |
| C | minor | `ground_truth.red_herrings` | Empty although the case is built on the FTD-like family history and the psychiatric misattribution. | FIXED: two red herrings (family history, depression diagnosis). |
| A | minor | criteria citations, rationales, order; `sequence_constraints`; `stop_rule` | Duplicate keys, rationale = label, no constraints, `max_additional_actions` 0. | FIXED: one bracketed key each, case-specific rationales, order per plan 3.1 (ids kept), three soft constraints (MRI before biomarker, assessment before biomarker, battery before genetics), `max_additional_actions` 1. |
| E | minor | `metadata.difficulty_rationale`, `key_educational_points[6]` | Engineering wording on the "only biomarker route". | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The clinical assessment now records this woman's frontal syndrome: disinhibition and utilization behaviour at the bedside, failed go/no-go and motor sequencing, applause sign, grasp and palmomental reflexes, MMSE 22 and MoCA 18 with executive and recall deficits, and her husband's account of 18 months of disinhibition, apathy and $8,000 of impulsive spending followed by memory decline. She cannot work or plan meals, so the stage is mild dementia (field set to true). The HPI no longer mentions a language disorder copied from the lvPPA case. The MRI no longer mentions gadolinium. Amyloid status can be established by CSF or amyloid PET (optional, one test enough); a concordant CSF result was added. Genetic testing (optional, after counselling) now covers FTD genes as well as APP/PSEN1/PSEN2, both negative. The donepezil check is optional, specific to her medicines and pulse. bvFTD and a psychiatric cause are now low, with the results that argue against them. Musts cover informant history, disclosure and planning, financial protection, work and driving, biomarker offer, a cholinesterase inhibitor once Alzheimer pathology is supported (not in FTD), genetic counselling and non-drug behavioural management with carer support; prohibitions cover depression attribution, antipsychotics for disinhibition, benzodiazepines and memantine at the mild stage.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: G30.0 grants "posterior cortical atrophy", "benson syndrome" and "early onset alzheimer" to this frontal-variant case (plan 5.1).
- Matcher: a `check_drug_interactions` call for rivastigmine is answered by the only stored drug-check follow-up (donepezil), because the trigger matcher falls back to the single follow-up of the tool. The output names donepezil, so it is not misleading, but a drug-keyed discriminator would be cleaner.
- Citation keys used: `[bvAD_2015]`, `[FTDC_2011]`, `[ACMG_NSGC_2011]`, `[NICE_NG97]`, `[Beers_2023]` (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- None needing Andrea. Decided: bvFTD set to `low` at assessment time (plan C11) because the pathway returns AD biomarkers; an agent that skips the optional biomarkers would reasonably keep bvFTD high, which the differential does not score.

## Verification
Adversarial verifier, 24 Oct 2026. Checked every note row (d82080e9, 0c77408a, 7d03b15b, b9ec2dbb, be4f5858, d6c203e3) against the file: frontal profile in the clinical assessment with `amnestic_predominant_profile` false, IADL field true, FTD panel as a second alternative with its own negative follow-up, counselling must and battery-before-genetics constraint, no gadolinium text, frontal-AD pearl, bvFTD in the differential (low, with the Rascovsky exclusion). Read the patient block, clinical assessment, labs, CSF (468/11200 = 0.042), MRI, neuropsych, PET, FDG, both gene panels, drug check (buspirone, levothyroxine, sumatriptan statements correct; pulse 68 matches the vitals), ECG fallback (QRS 104 ms with incomplete RBBB is consistent), criteria, musts, prohibitions, differential and red herrings. The HPI edit (venlafaxine stopped, no language disorder) is correct and the medication list agrees. Both biomarker alternatives have case-authored outputs.

Found and fixed:
- B, minor, `patient.neurological_exam.mental_status` and `clinical_assessment.findings[2]`: the MoCA deficits listed added up to 10 points for a score of 18/30. The exam itself records the two missing points (date wrong; three serial-seven errors), so they are now listed: serial subtraction 2/3 and orientation 5/6 (date). Recall 5 + trail 1 + fluency 1 + clock 1 + serial 1 + orientation 1 + abstraction 2 = 12, 18/30. MMSE breakdown (8 points, 22/30) was already correct.
No other change. Both checks clean for the case; case guards pass.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'lasting power of attorney' (UK instrument) changed to 'durable power of attorney' in this US-setting case (1 place).
- MMSE serial sevens: '2 points (3 errors)' corrected to '(2 errors)', since each error costs one point; total 22/30 unchanged (exam and findings[1]).
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.
- Normal values in `Magnesium_homocysteine` varied (Magnesium 2.0 to 2.2, Homocysteine 10.2 to 9.9), all still within the case's reference ranges: the same numbers (magnesium 2.0, homocysteine 10.2, ESR 12, CRP 1.8) had been copied into up to 13 cases, a template artefact raised by the S01 worker; no text cites the changed values.
- Checks re-run after these additions: perfect_agent.py, case_io.py check and test_case_guards clean.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`--prune --conditions alzheimers_early`): removed "posterior cortical atrophy" and "benson syndrome"; code G30.1 (onset before 65). Added frontal-variant labels ("frontal variant alzheimer", "behavioral/behavioural variant alzheimer", "dysexecutive alzheimer"). Now: codes ['G30.0', 'G30.9', 'F00', 'G30.8']; labels after accepted[0]: ['alzheimer disease', "alzheimer's disease", 'alzheimers disease', 'alzheimer dementia', 'dementia due to alzheimer', 'early onset alzheimer', 'frontal variant alzheimer', 'behavioral variant alzheimer', 'behavioural variant alzheimer', 'dysexecutive alzheimer'].
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although this case contradicts it (diagnosis, history, medications or a stored finding) now get a case-specific report; every other off-pathway order still gets the library normal. No tier, criterion, diagnosis or existing output changed.

- `order_advanced_imaging modality=tau_PET` -> `followup_outputs[order_tau_pet]`: case-specific tau-positive flortaucipir PET with the distribution of the stored FDG-PET pattern.
- `order_advanced_imaging modality=perfusion_SPECT` -> `followup_outputs[order_perfusion_spect]`: regional hypoperfusion matching the stored FDG-PET hypometabolism.
- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: language findings of the stored neuropsychological battery (naming, fluency) in the speech-language format.
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[order_performance_status]`: dementia-stage performance status (Karnofsky 70/ECOG 1; 60/2 in the rapidly progressive case) instead of Karnofsky 100.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k ALZ-EARLY` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
