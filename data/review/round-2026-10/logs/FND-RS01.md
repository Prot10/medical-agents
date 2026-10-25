# FND-RS01
Reviewer status: R1 none, R2 none (FND was never reviewed; no notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `ground_truth.action_criteria` | Template criteria (plan A): literature and drug check `recommended`, video-EEG and labs `optional`, labels equal to rationales, template citations. | FIXED: order exam (required), labs `["CMP","magnesium","phosphate","thiamine_B1"]` (recommended), video-EEG (required), drug check (required), new optional `action-neuropsych-battery`, literature (optional, last); case-specific labels, rationales, expected evidence, citations. |
| A | major | `ground_truth.stop_rule` | Only the exam although video-EEG and drug check are now required. | FIXED: exam, video-EEG, drug check; `max_additional_actions` 0. No sequence constraint (plan 3.3 limits video-EEG before drug check to the taper cases). |
| C | major | `followup_outputs[1]` (drug check) | Proposed sertraline, which she does not take; claimed metoclopramide "increases serotonin levels"; metoclopramide's real risks (extrapyramidal reactions, tardive dyskinesia, EMA dose and duration limit, epilepsy contraindication, QT) absent (plan C). | FIXED: deleted; `initial_tool_outputs.drug_interactions.general` lists her three medicines verbatim with those metoclopramide warnings and contraindications; no new drug or dose. |
| D | minor | `followup_outputs[0]` (literature) | Case-agnostic follow-up with paraphrased results and a summary echoing the policy (plan B). | FIXED: deleted; canonical `initial_tool_outputs.literature_search`. |
| B | major | `initial_tool_outputs.eeg` | Report did not describe the captured events (only a "Movement artifact" finding); impression not canonical and with an em dash; nothing marked it as a video recording. | FIXED: two event findings with times, durations, video semiology and the persisting posterior rhythm; canonical video-EEG impression; `background.continuity` added. Activating procedures, background and limitations kept. |
| D | major | `initial_tool_outputs.clinical_assessment` | Meta keys in `criteria_met`; non-dermatomal sensory loss and sensory inconsistency counted as rule-in signs; observed events not reported; key-leak impression. | FIXED: canonical shape; 3 validated signs (bilateral Hoover, collapsing weakness, distractibility); sensory findings and astasia-abasia supportive; observed event row; event-based impression; wasting and reflexes reported. |
| D | major | `initial_tool_outputs.labs` | Management text in `clinical_significance` and `interpretation` ("replace", "replace empirically before glucose", "not Wernicke encephalopathy"); magnesium omitted from the interpretation; phosphate, which the refeeding question needs and the criterion names, absent. | FIXED: `clinical_significance` null; plain interpretation; panels renamed (Magnesium_phosphate_thiamine, Prolactin); phosphorus 2.8 mg/dL (normal) added, the same value as the source-patient twin RP02. Other values unchanged. |
| B | minor | `patient.history_present_illness` | "Laboratory screening for infectious, metabolic, and autoimmune causes was non-revealing" against a current low magnesium, and a result of the scored labs. | FIXED: "Screening for infectious and autoimmune causes at the regional hospitals was reported as non-revealing." |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts; no thiamine, refeeding, eating-disorder or metoclopramide action. | FIXED: M-DX (mixed), M-COMM (interpreter, father), M-PHYSIO, M-PSY (depression), M-RESCUE, thiamine before glucose with magnesium replacement and refeeding monitoring, eating-disorder assessment, stop metoclopramide. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "per Stone 2018"; "start or continue" AEDs. | FIXED: P1 (naming repeat CT and spine MRI), P2, P3, P5, P6, P7, "Give glucose-containing fluids before thiamine", "Continue metoclopramide". |
| C | major | `ground_truth.differential` | Epileptic seizures `moderate` after recorded events; MS and structural rows citing a brain MRI not in the case; neuropathy citing an avoided EMG; encephalitis and malingering template rows; the drug, nutritional and referral mimics missing. | FIXED: epileptic seizures `low` (canonical), metoclopramide-induced movement disorder `low`, thiamine deficiency `low`, malnutrition myopathy `low`, spinal cord lesion `low`, early-onset psychosis `low`, eating disorder possibly coexisting `moderate`. |
| B | major | `ground_truth.red_herrings[0]` | "Family history of epilepsy" while the family history says "No family history of epilepsy". | FIXED: deleted; red herrings now the psychosis referral, wasting with reduced reflexes, and the depressive context. |
| A | minor | `ground_truth.avoided_actions` | No repeat-study waste although a spinal cord MRI was normal (plan L). | FIXED: added `avoid-waste-repeat-spine-mri`; existing items cite `[Espay_2018]`/`[Stone_2016]` with patient-specific rationales. |
| E | major | `ground_truth.key_clinical_evidence` | Template items with the "Interim composition decision" leak, OPTIONAL item and Stone 2018. | FIXED: 5 case-specific items. |
| B | minor | `fallback_tool_outputs` | specialized_test and advanced_imaging untyped with the leak sentence; echo without `echo_type`. | FIXED: nulled and removed from `fallback_tool_kinds`; echo `echo_type: TTE`. |
| E | minor | `metadata.difficulty_description`, `.difficulty_rationale` | "Normal investigations support the diagnosis" (diagnosis by exclusion) and template rationale. | FIXED: rewritten for the case; `last_revised` 2026-10-24. |

## Changes, in one paragraph a physician can read before re-reviewing

The pathway is the functional-signs examination, then magnesium, phosphate, thiamine and electrolytes (recommended), the video-EEG of the habitual events (required) and the medication review (required), with optional neuropsychology and literature last. The examination report counts the bilateral Hoover sign, collapsing leg weakness and distractibility, lists the sensory findings and astasia-abasia as supportive, describes the two events seen during the examination and records the wasting with 1+ leg reflexes. The video-EEG now reports the two events (60 and 75 seconds, closed eyes, asynchronous shaking) with the posterior rhythm persisting and no ictal change. The labs keep their values, lose the management text, and add a normal phosphorus (2.8 mg/dL) so the refeeding question is answerable. The drug check now addresses the real problem: metoclopramide 10 mg three times daily, a dopamine antagonist with extrapyramidal and tardive dyskinesia risk, an EMA weight-based ceiling she exceeds, an epilepsy contraindication and QT effects; the sertraline output for a drug she does not take is gone. Musts add an event plan, thiamine before glucose with magnesium replacement and refeeding monitoring, an eating-disorder assessment and stopping metoclopramide; prohibitions add continuing metoclopramide and glucose before thiamine. The differential (all low except a possibly coexisting eating disorder) now includes metoclopramide-induced movement disorder and the referral diagnosis of psychosis. A repeat spine MRI is scored as waste.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[Daum_2014]`, `[Stone_2016]`. Free-text: "NICE CG32 Nutrition support for adults", "Metoclopramide SmPC and EMA 2013 restriction".
- EEG routing (plan CENTRAL 3): a `routine` EEG order receives the stored video-EEG with its events.

## Open questions for Andrea (judgment calls you could not settle)

None open. Decisions taken:
- Phosphorus 2.8 mg/dL was added to the stored labs (the only new value): the recommended criterion names phosphate per plan 3.2, the refeeding must needs it, and the value matches the source-patient twin RP02 so the two cases do not diverge (plan 6.3).
- RS01 and RP02 already differ in history (mother's death 7 years vs 6 months ago, medication lists); per plan 6.3 I kept the existing data and invented nothing further.
- The plan's RS01 musts are "as RP02 plus RESCUE and stop metoclopramide"; RP02's primary-amenorrhea must does not apply because RS01 records no amenorrhea.

## Verification

`perfect_agent.py FND-RS01 -v`: ok; the lab call gets the stored panel with magnesium, phosphorus and thiamine, `eeg_type: video` gets the stored video-EEG, the drug check gets `initial_tool_outputs.drug_interactions.general`. `case_io.py check FND-RS01`: schema and synonym guard OK; the only FND failures are the literature leaks of FND-P08 and S10 (other workers' cases). `test_case_guards.py -k FND-RS01`: 2 passed.

## Condition audit

2026-10-24, FND condition auditor.

- `action-neuropsych-battery.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-1-search-medical-literature.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.

## Close-out (24 Oct 2026)

Andrea's FND ruling of 24 Oct 2026 and the close-out decisions (`plans/FND-decisions.md`). What changed and why:

- `action-4-analyze-eeg` (video-EEG) required -> optional, removed from the stop rule; rationale now says what the diagnosis rests on without the recording (ILAE 2013 levels).
- M-DX must, COMM must, red-herring interpretations and metadata no longer say the diagnosis rests on the video-EEG: they rest on the positive signs and the event semiology, with video-EEG confirmation where recorded (open question 8).
- Post-event prolactin 12 -> 64 ng/mL (abnormal) with an analytic note: metoclopramide 30 mg/day raises prolactin, so the level cannot be interpreted (open question 5); labs interpretation names it.
- Diagnosis synonyms scoped by phenotype (`diagnosis_synonyms.yaml` F44 entries; a label or code naming another presentation must not score): removed "functional movement disorder"; added "psychogenic nonepileptic seizures", "dissociative seizures", "nonepileptic seizures", "functional limb weakness", "functional motor disorder".
- The medicine review stays required as a management act (ruling); listed for the physicians in `plans/FND-decisions.md`.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FND-` passes, now including the discriminator guard.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `video`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although the case contradicts it now get a case-specific report (library answers stay for everything else).

- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `fallback_tool_outputs.clinical_assessment`: timed gait and balance: not completed TUG, when assisted to stand, marked swaying and lurching without a fall; no independent steps. Why: the exam documents an abnormal gait; the library reports a normal timed gait (TUG 9.1 s).
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[request_performance_status]`: Karnofsky 40, ECOG 3. Why: the history documents limited activity; the library reports Karnofsky 100, ECOG 0, working.
- `order_specialized_test test_type=neuropsych_battery` -> `followup_outputs[request_neuropsych_battery]`: cognition within normal limits; moderately severe depressive symptoms, mild anxiety and elevated dissociative experiences; validity passed. Why: the history documents anxiety, depression or trauma-related symptoms; the library reports no significant mood or anxiety symptoms.

Checks: `perfect_agent.py` pass; `test_case_guards.py -k FND-RS01` pass; map verify (map_FND) problems 0; criterion-answer snapshot unchanged except `action-neuropsych-battery`, which the library answered before and the new report now answers.
