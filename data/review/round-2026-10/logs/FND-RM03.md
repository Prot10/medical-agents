# FND-RM03
Reviewer status: R1 none, R2 none (FND was never reviewed; no notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `ground_truth.action_criteria` | Template criteria (plan class A): literature and drug check `recommended` with the shared labels, video-EEG and labs `optional`, labels equal to rationales, citations "positive FND signs; AAN functional seizures guideline 2025" and "FND criteria pack ..." strings. | FIXED: rebuilt per plan 3.1/3.2 in order exam (required), labs `["sodium","serum_osmolality","urine_osmolality"]` (recommended, CMP dropped: the question is the sodium and osmolalities), video-EEG (required), drug check (required), new optional `action-neuropsych-battery`, literature (optional, last). Short imperative labels, case-specific rationales and expected evidence, sourced citations. |
| A | major | `ground_truth.stop_rule` | Stop rule listed only the exam although video-EEG and drug check are now required. | FIXED: `required_before_assessment` = exam, video-EEG, drug check; `max_additional_actions` 0. |
| D | major | `followup_outputs[0]` (literature) | Fabricated sources ("Edwards and Bhatia JNNP 2012", "Zuberi Epilepsia 2016"), "Espay ... BMJ 2018" misattribution, case-specific conclusions (plan class B). | FIXED: follow-up deleted; canonical `initial_tool_outputs.literature_search` (7 rows) keyed by the criterion query. |
| B | major | `followup_outputs[1]` (drug check) | Sertraline-only "plan" output citing the urine osmolality (cross-modality), proposing bupropion and mirtazapine; desmopressin with polydipsia (the real, contraindicated interaction) only as a warning; initial output null. | FIXED: follow-up deleted; new `initial_tool_outputs.drug_interactions.general` lists the three medicines verbatim, desmopressin with water loading (SmPC contraindication), desmopressin with sertraline, sertraline with ondansetron (serotonergic, QT); no dose, start or alternative. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts: diagnosis-by-exclusion and video-EEG musts, neuropsychology "recommended tier" must, two long duplicates; desmopressin never stopped. | FIXED: M-DX (mixed), M-COMM, M-PHYSIO, M-PSY (GAD, compulsive drinking, depression screen), M-RESCUE, stop desmopressin, fluid restriction with serial sodium and sertraline review. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "per Stone 2018" citations; "start or continue" antiseizure drugs. | FIXED: P1, P2, P3, P5, P6, P7, "Continue desmopressin", and a case-specific "Give hypertonic saline for the events" (the confounder's trap). |
| D | major | `initial_tool_outputs.clinical_assessment` | Meta keys in `criteria_met`; fragment findings ("...wavering that does not follow a cerebellar pattern;" / "performance improves with distraction."); midline splitting counted; impression ending "No further investigation is required to make the diagnosis..." (key leak). | FIXED: canonical shape; 5 validated signs counted (Hoover, collapsing weakness, entrainment, distractibility, dragging gait); midline splitting and Romberg as supportive; observed event; event-based impression. |
| C | major | `patient.neurological_exam.motor`, `initial_tool_outputs.clinical_assessment` | Hoover sign described inversely ("when testing left hip flexion, involuntary extension is palpable in the contralateral right hip", which is the finding of genuine effort). | FIXED: "left hip extension is weak on direct testing but full during right hip flexion against resistance". |
| C | minor | `patient.neurological_exam.gait` | "Markedly antalgic pattern, dragging the left leg with circumduction": antalgic means pain-avoiding and circumduction is a pyramidal feature, both contradicting a dragging monoplegic gait. | FIXED: "drags the left leg behind her with the foot kept in contact with the floor, without circumduction". |
| D | major | `patient.neurological_exam.additional` | Lab result and its interpretation in the exam ("serum sodium was checked and was 131 mEq/L ... may be contributing to persistent mild hyponatremia"), the scored lab. | FIXED: both sentences removed. |
| B | minor | `initial_tool_outputs.eeg` | Impression omitted the captured events and lacked a final period; em dashes in event types; event 2 (reported leg weakness) presented as a seizure-like event. | FIXED: canonical impression naming three habitual events plus one push-button event; event types relabelled, times and durations in `frequency`; event 4 state and morphology made explicit (alpha before onset). |
| E | minor | `initial_tool_outputs.labs` | `abnormal_values_summary` carried interpretation ("maximally dilute"); urine osmolality under a "Serum_Osmolality" panel. | FIXED: factual list; panel renamed "Osmolality"; interpretation a plain recital. Values unchanged (checked: calculated osmolality 270 vs measured 268; Hct/Hb 3.0, MCHC 33). |
| C | major | `ground_truth.differential` | Epileptic seizures `moderate` after a normal video-EEG; MS and structural lesion cited a brain MRI not in the pathway; neuropathy cited "(when obtained)" EMG, which is avoided; autoimmune encephalitis and malingering (no incentive) template rows; no hyponatremic-seizure entry although the case is built on it. | FIXED: epileptic seizures `low` (canonical key feature), new "Hyponatremia-provoked seizures" `low`, "MS or another spinal cord lesion" `low` citing the exam (ipsilateral all-modality loss incompatible with a cord lesion); other rows deleted. |
| B | major | `ground_truth.red_herrings[0]` | "Family history of MS" red herring while the family history says "No known family history of multiple sclerosis". | FIXED: deleted (plan E). |
| B | minor | `ground_truth.red_herrings` | Generic data points ("Family history of epilepsy in a relative", "Pre-existing psychiatric diagnosis (anxiety or depression)"); "Stone 2018" citation; the central confounder (sodium 129) absent. | FIXED: data points name the grandmother, GAD, neglect and separation; new red herring for the ED sodium. |
| E | major | `ground_truth.key_clinical_evidence` | Template items including the "Interim composition decision, August 2026" engineering leak, the "OPTIONAL" item and Stone 2018 claims. | FIXED: 5 case-specific items. |
| C | minor | `ground_truth.avoided_actions[*]` | `[Stone_2018]` (non-existent paper); generic rationales; CT rationale ignored the normal outside CT. | FIXED: `[Espay_2018]` or `[Stone_2016]`, patient-specific rationales; all kept as waste. |
| B | minor | `fallback_tool_outputs.specialized_test`, `.advanced_imaging`, `.echo` | `test_type: ''` with "the negative result is itself a harm" leak; `modality: ''`; echo without `echo_type`. | FIXED: specialized_test and advanced_imaging nulled and removed from `metadata.fallback_tool_kinds`; echo `echo_type: TTE`. CT, CSF, echo, Holter fallbacks kept. |
| C | minor | `metadata.clinical_pearls` | Pearl from a fabricated source ("share underlying mechanisms of somatization"); Hoover described inversely; midline splitting called a positive sign. | FIXED: pearls rewritten (hyponatremia threshold, urine osmolality, desmopressin contraindication, correct Hoover, midline splitting supportive). |
| E | minor | `metadata.difficulty_description`, `.difficulty_rationale`, `.revision_reason` | Template rationale naming "MRI + basic labs"; description did not name the desmopressin. | FIXED: rewritten for the case; `last_revised` 2026-10-24. |

## Changes, in one paragraph a physician can read before re-reviewing

The work-up now reads: the functional-signs examination (required), serum sodium with serum and urine osmolality (recommended), video-EEG of the habitual events (required), the medication review (required), an optional neuropsychology battery and an optional literature search last. The examination report counts five validated signs (Hoover sign, now described correctly, collapsing weakness, tremor entrainment, distractibility, dragging gait without circumduction), lists midline sensory splitting and Romberg swaying as supportive only, and documents the witnessed event; the sodium value and its interpretation were removed from the exam. The video-EEG impression now names the three habitual events and the push-button leg-weakness event, all without ictal change. Labs are unchanged in value (sodium 131, serum osmolality 268, urine osmolality 62). The drug check now reports the real problem, desmopressin with primary polydipsia (an SmPC contraindication) together with sertraline, plus sertraline with ondansetron. Musts: positive diagnosis of mixed FND, explanation, physiotherapy, psychological therapy with treatment of anxiety and the compulsive drinking, an event plan without benzodiazepines, stop desmopressin, fluid restriction with serial sodium and a sertraline review. Prohibitions add continuing desmopressin and hypertonic saline for the events. The differential is epileptic seizures, hyponatremia-provoked seizures and MS or cord lesion, all low. The false "family history of MS" red herring is gone; the sodium 129 is now the named red herring.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used per plan 1.1: `[Daum_2014]`, `[Stone_2016]` (plan CENTRAL 1). Free-text citations: "Spasovski G et al. Eur J Endocrinol 2014;170:G1-G47" (hyponatremia guideline) and "Desmopressin (DDAVP) SmPC, contraindications".
- EEG routing (plan CENTRAL 3): a `routine` EEG order receives the stored video-EEG with its four events.

## Open questions for Andrea (judgment calls you could not settle)

None open. Decisions taken:
- Plan 4 lists the RM03 musts as DX, COMM, PSY, RESCUE plus two; I added M-PHYSIO because she has functional left leg weakness with a dragging gait, which is the plan's own motor-phenotype rule (M-PHYSIO "motor phenotype"; M01, a mixed case, has it).
- The HPI keeps the outside emergency department sodium of 129 mEq/L: it is a dated prior result from another encounter and the recommended lab criterion scores a current sodium with both osmolalities, which the HPI does not give.
- The added prohibition on hypertonic saline is my own: it is the specific wrong treatment the hyponatremia confounder invites.

## Verification

`perfect_agent.py FND-RM03 -v`: ok; the exam gets the clinical assessment, the lab call gets the stored panel with the osmolalities, `eeg_type: video` gets the stored video-EEG, the drug check gets `initial_tool_outputs.drug_interactions.general`. `case_io.py check FND-RM03`: schema and synonym guard OK; the only failures naming FND are the literature leaks of FND-M09, P08, S06 and S10 (other workers' cases). `test_case_guards.py -k FND-RM03`: 2 passed. No new em or en dashes (the only one left is in `diagnosis.accepted[0]`, not edited per ruling 3).

## Condition audit

2026-10-24, FND condition auditor.

- `action-neuropsych-battery.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-1-search-medical-literature.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `ground_truth.differential[2].key_features`: "loss of all sensory modalities" contradicted the examination, which preserves proprioception; now lists the modalities lost.
- `initial_tool_outputs.clinical_assessment` finding: "Loss of all sensory modalities ... with proprioception preserved" was self-contradictory; now names the modalities lost.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.

## Close-out (24 Oct 2026)

Andrea's FND ruling of 24 Oct 2026 and the close-out decisions (`plans/FND-decisions.md`). What changed and why:

- `action-4-analyze-eeg` (video-EEG) required -> optional, removed from the stop rule; rationale now says what the diagnosis rests on without the recording (ILAE 2013 levels).
- M-DX must, COMM must, red-herring interpretations and metadata no longer say the diagnosis rests on the video-EEG: they rest on the positive signs and the event semiology, with video-EEG confirmation where recorded (open question 8).
- Diagnosis synonyms scoped by phenotype (`diagnosis_synonyms.yaml` F44 entries; a label or code naming another presentation must not score): added "psychogenic nonepileptic seizures", "dissociative seizures", "nonepileptic seizures", "functional limb weakness", "functional motor disorder", "functional tremor".
- The medicine review stays required as a management act (ruling); listed for the physicians in `plans/FND-decisions.md`.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FND-` passes, now including the discriminator guard.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `video`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although the case contradicts it now get a case-specific report (library answers stay for everything else).

- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `fallback_tool_outputs.clinical_assessment`: timed gait and balance: 16.0 s TUG, left leg dragged behind with the foot on the floor, without circumduction. Why: the exam documents an abnormal gait; the library reports a normal timed gait (TUG 9.1 s).
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[request_performance_status]`: Karnofsky 70, ECOG 2. Why: the history documents limited activity; the library reports Karnofsky 100, ECOG 0, working.
- `order_specialized_test test_type=neuropsych_battery` -> `followup_outputs[request_neuropsych_battery]`: cognition within normal limits; severe anxiety, mild depressive symptoms and elevated dissociative experiences; validity passed. Why: the history documents anxiety, depression or trauma-related symptoms; the library reports no significant mood or anxiety symptoms.

Checks: `perfect_agent.py` pass; `test_case_guards.py -k FND-RM03` pass; map verify (map_FND) problems 0; criterion-answer snapshot unchanged except `action-neuropsych-battery`, which the library answered before and the new report now answers.
