# FND-P01
Reviewer status: no reviewer notes for FND (R1 and R2 never reviewed this condition) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input is the July 2026 tool guidance (plan 1.3), applied through the plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.action_criteria[action-5-analyze-eeg]` | Video-EEG optional although the events (2-3 a week, shaking with eyes closed) are the paroxysmal phenotype the pack requires it for. | FIXED: required, canonical expected evidence, ILAE 2013 / AAN 2025 rationale; in the stop rule. |
| B | major | `initial_tool_outputs.eeg` | A "4-hour" routine-duration recording capturing two events of a 2-3-per-week disorder; artifact field asserted "confirming absence of epileptiform correlate"; impression not in canonical form. | FIXED: 72-hour inpatient video-EEG, event times and durations in the findings, artifact impact descriptive only, canonical NORMAL video-EEG impression naming both events. |
| C | major | `ground_truth.action_criteria[action-4-analyze-brain-mri]`, `initial_tool_outputs.mri` | MRI criterion although a normal outpatient brain and spine MRI exists; the stored report was a gadolinium brain plus cervical and lumbar spine study in a patient with a contrast reaction. | FIXED: criterion deleted; `avoid-waste-repeat-brain-mri` added (plan) and `avoid-waste-repeat-spine-mri` (own finding, same reason); stored MRI is now a non-contrast brain report unchanged from the outpatient study. |
| D | major | `initial_tool_outputs.clinical_assessment` | Meta keys in `criteria_met`; findings were sentence fragments ("However, ..."); 6 signs counted, including the equivocal Hoover, midline splitting and non-dermatomal loss; leak "No further investigation is required...". | FIXED: canonical shape; 3 rule-in signs (collapsing weakness, tremor entrainment, distractibility); Hoover reported equivocal and not counted; sensory and gait features supportive. |
| D | major | `followup_outputs[0]` (literature) | Fabricated attribution ("Espay ... Lancet Neurol 2018;17:84-98, new subtypes", which is Hallett 2022); unsupported "40% improve". | FIXED: deleted; `initial_tool_outputs.literature_search` is the canonical plan 2B output (all rows); criterion optional, last. |
| C | major | `initial_tool_outputs.drug_interactions` | Empty list with the leak warning; the serotonergic cluster, sedative load and bleeding risk were missed. | FIXED: duloxetine + cyclobenzaprine + sumatriptan (serotonergic), pregabalin + cyclobenzaprine (sedation), duloxetine + ibuprofen (GI bleeding); warnings for duloxetine tremor, pregabalin ataxia, cyclobenzaprine anticholinergic effects. Criterion recommended. |
| C | major | `ground_truth.assessment` | Seven template musts (video-EEG as a must, neuropsychology "recommended", duplicates); prohibitions cite "per Stone 2018" and forbid ASM "start or continue". | FIXED: M-DX (mixed), M-COMM, M-PHYSIO, M-PSY (depression and GAD), M-RESCUE; P1 naming repeat MRI and NCS, P2, P3, P5, P6, P7. |
| C | major | `ground_truth.differential` | Epileptic seizures `moderate` after the recorded events; template stroke, structural, neuropathy ("when obtained" EMG) rows; MND and myelopathy, raised by the referral, absent. | FIXED: epileptic seizures low (fact 8); MS or inflammatory myelopathy low; MND low; organic tremor low (duloxetine named). Template rows deleted. |
| E | major | `ground_truth.key_clinical_evidence` | Eight template items (Interim composition leak, OPTIONAL item, Stone 2018). | FIXED: six case-specific items. |
| B | major | `ground_truth.red_herrings[1]` | "Family history of epilepsy" although the family history says none. | FIXED: deleted; MS red herring made concrete; equivocal Hoover and fibromyalgia attribution added; psychiatric red herring made concrete. |
| A | minor | `ground_truth.avoided_actions[*]` | `[Stone_2018]`; generic rationales. | FIXED: `[Espay_2018]` / `[Stone_2016]`, patient-specific rationales. |
| A | minor | `fallback_tool_outputs` | specialized_test leak ("negative result is itself a harm", `test_type: ''`), advanced_imaging `MRI_brain_functional`, drug check "(agent not specified...)"; echo without `echo_type`. | FIXED: three nulled and removed from `metadata.fallback_tool_kinds`; echo `echo_type: TTE`; normal CT and CSF kept. |
| E | minor | `metadata.estimated_complexity`, `difficulty_rationale`, `red_herrings`, `revision_reason` | "extensive negative workup needed" contradicts the policy; red herrings named a vitamin D level and a lumbar disc finding not in the case. | FIXED: rewritten. |
| A | minor | `ground_truth.action_criteria` | Labels equal rationales; "FND criteria pack - ..." citations. | FIXED: short labels, distinct rationales; optional neuropsychology criterion added. |

## Changes, in one paragraph a physician can read before re-reviewing

A 40-year-old woman with fibromyalgia, depression and anxiety has 8 months of leg weakness (now in a wheelchair), a coarse hand tremor and shaking events, after a normal outpatient brain and spine MRI, nerve conduction studies and bloods. The required work-up is now the examination for positive signs (collapsing weakness, tremor entrainment, distractibility; Hoover equivocal; normal tone, reflexes and plantars) and a 72-hour video-EEG that records two habitual events (7 minutes of irregular shaking with eyes closed, 2 minutes of hand tremor) without ictal change. The MRI criterion is gone: repeating the brain or spine MRI is now scored as waste, and the stored report is a non-contrast brain study (she reacted to contrast). The medication review (recommended) now reports the serotonergic combination of duloxetine, cyclobenzaprine and sumatriptan, sedation with pregabalin and cyclobenzaprine, and duloxetine-ibuprofen bleeding risk. Musts: positive diagnosis of mixed FND, explanation with written information, specialist physiotherapy, psychological therapy with treatment of depression and anxiety, and a written plan for events without benzodiazepines. Differential: epileptic seizures, MS or myelopathy, motor neuron disease and organic tremor, all low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- EEG routing (plan 5.3): EEG reports carry no `eeg_type`, so a `routine` EEG order is answered with this stored 72-hour video-EEG and its events.
- Citation keys (plan 5.1): `[Stone_2016]` used.

## Open questions for Andrea (judgment calls you could not settle)

None open. Decisions taken and their reasons:
- Added `avoid-waste-repeat-spine-mri` beside the plan's repeat brain MRI waste: the outpatient spine MRI was also normal and nothing in the examination raises a new cord question.
- The plan's class L says stored outputs of avoided actions stay null, while its P01 entry asks for a non-contrast brain report matching the prior. I kept the stored report (section 4 governs), so an agent that repeats the MRI gets a report consistent with the history rather than a generic one.
- The bilateral dragging gait is recorded as supportive, not as the validated "dragging monoplegic gait", because it is bilateral and non-patterned.

## Verification

Adversarial check (24 Oct 2026) of the log against the case and against the pre-round version (`b8be2153^`). What I checked: the patient block (unchanged, as the log implies); the deleted MRI criterion and the two new repeat-study wastes against the history (normal outpatient brain and spine MRI and NCS) and against the stop rule (no MRI left in it); the stored non-contrast MRI against the contrast reaction; P1 naming the repeat MRI and NCS; the EEG (72-hour recording, two events with times and durations, canonical impression, no "functional" or "PNES" in the report); the signs count (3: collapsing weakness, entrainment, distractibility; Hoover equivocal and not counted; midline split, vibration split and the bilateral non-patterned gait supportive), which matches the exam text; the drug output against the medication list verbatim and fact 16 (serotonergic triad, sedative pair, SNRI-NSAID bleeding); musts against prohibitions (no contradiction); the differential (epileptic seizures low after the recorded events; MS/myelopathy, MND and organic tremor low with this case's findings); every log claim marked FIXED.

Found: nothing that needed a change. One wording note left as is: the M-DX must counts the 2-minute hand-tremor episode among the "two habitual events"; the 7-minute shaking event alone reaches the ILAE documented level, so the must stays correct. No change. Checks re-run after the changes: `perfect_agent.py -v` ok, `case_io.py check` clean for this case (schema, synonym guard, no failing test names it), `test_case_guards.py -k` passed. The diagnosis label, `icd_codes` and synonyms are unchanged from before the round; no new em dashes or `Stone_2018` strings.
