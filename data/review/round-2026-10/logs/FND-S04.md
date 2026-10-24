# FND-S04
Reviewer status: R1 not reviewed, R2 not reviewed (FND has no notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.neurological_exam.motor`, clinical assessment Hoover finding | Hoover compared with "voluntary right hip flexion ... 2/5"; the sign compares weak voluntary hip extension with involuntary extension during contralateral hip flexion. | FIXED: "voluntary right hip extension is weak (2/5) on direct testing, but involuntary right hip extension is full when he flexes the left hip against resistance". |
| B | minor | `patient.neurological_exam.additional` | Entrainment "during contralateral hand tapping" while both arms were shaking (not a possible test); "asynchronous, irregular, side-to-side head movements" garbled. | FIXED: shaking entrained to a rhythm tapped with his left foot; sentence separates the arm shaking from the head movements. |
| C | major | `ground_truth.action_criteria[action-5-analyze-eeg]` | Video-EEG `optional` with two to four events a day. | FIXED (plan 3.2): required, canonical expected_evidence, case rationale, in the stop rule. |
| B | minor | `initial_tool_outputs.eeg` | No event findings (`findings: []`), impression not canonical ("NO epileptiform correlate", no final period), beta "likely medication-related (benzodiazepine use)". | FIXED (plan J): 24 h inpatient video-EEG with two habitual events (day 1, 50 s and 2 min 10 s), posterior alpha persisting, no postictal slowing; canonical impression; attribution removed. |
| B | major | `initial_tool_outputs.mri` | Criterion orders `contrast: false`; report "with gadolinium", "No enhancing lesions post-gadolinium", bundled MRA. | FIXED (plan I): non-contrast technique line, enhancement and MRA removed; optional criterion `{"contrast": false}`. |
| D | major | `followup_outputs[0]` (literature) | "Perez DL et al. JNNP 2021, Consensus recommendations" and "Nielsen 2015 ... systematic review" misattributed; summary near the scoring key. | FIXED (plan B): deleted; canonical initial literature output. |
| D | major | `followup_outputs[1]` (drug check) | Prescribing plan ("Sertraline 150 mg daily (dose increase)", paroxetine, venlafaxine, fluoxetine); no initial drug output. | FIXED (plan C): deleted; initial output lists his medicines verbatim, sertraline with lorazepam (minor), lorazepam benzodiazepine cautions, the antidepressant boxed warning under 25 years, dicyclomine anticholinergic note; criterion recommended (lorazepam PRN). |
| C | major | `initial_tool_outputs.clinical_assessment` | Meta keys; nine "signs" counted including midline splitting, a commentary sentence and a coordination fragment; leak sentence. | FIXED (plan H): 5 rule-in signs (Hoover, collapsing weakness, dragging gait, distractibility, entrainment); observed events; supportive features not counted; canonical impression. |
| C | major | `ground_truth.assessment.*` | Template musts and prohibitions. | FIXED (plan D): M-DX, M-COMM addressing his fear of MS or epilepsy without insisting on a stress cause, M-PHYSIO, M-PSY (PTSD after witnessing the fatal accident, trauma-focused, with depression and anxiety), M-RESCUE, plus no as-needed lorazepam for the events with a gradual taper (plan fact 16); P1 naming the repeat CT, P2, P3, P5, P6, P7. |
| C | major | `ground_truth.differential` | Epileptic seizures `moderate`; stroke row (6-week progressive course does not raise it); MRI-based features with an optional MRI; neuropathy and encephalitis rows. | FIXED (plan F): epileptic seizures `low`; MS or structural lesion of brain or cord (including a hemicord pattern, raised by the abdominal sensory level) `low` on clinical grounds. Others removed. |
| D | major | `ground_truth.key_clinical_evidence` | Template items with the "Interim composition decision" leak. | FIXED: four case-specific items. |
| B | minor | `ground_truth.red_herrings` | Generic data points (the FH epilepsy row is real here: maternal aunt). | FIXED: rows name the case data; added his fear of MS or epilepsy and his rejection of a stress explanation. |
| C | minor | `metadata.clinical_pearls[1]`, `[3]` | Hoover sign "high sensitivity" (63% in McWhirter 2011); "early diagnosis and communication are the most important prognostic factors" overstated. | FIXED: "high specificity and moderate sensitivity"; shorter duration associated with better prognosis, communication supports engagement. |
| C | minor | `ground_truth.avoided_actions[*]` | Generic rationales, `[Stone_2018]`. | FIXED (plan L): patient-specific, `[Espay_2018]` / `[Stone_2016]`; CT framed as a repeat. |
| D | minor | `fallback_tool_outputs.specialized_test`, `.advanced_imaging`, `.echo` | Empty discriminators and the "itself a harm" leak; echo without `echo_type`. | FIXED (plan G). |
| B | minor | `metadata.difficulty_rationale` | Template rationale. | FIXED. |
| - | check | perfect_agent / guards | perfect_agent `-v` ok (exam, video-EEG, drug check each from the case's own output); case guards pass; `case_io.py check`: no failure names FND-S04. | - |

## Changes, in one paragraph a physician can read before re-reviewing

Clinically unchanged: a 22-year-old man with six weeks of right leg weakness and daily shaking episodes that began two weeks after he witnessed a fatal pedestrian accident, with nightmares and flashbacks since, a normal outside CT, an aunt with epilepsy, and lorazepam as needed. The Hoover sign is now described correctly and the entrainment test is one he could perform during bilateral arm shaking. The required work-up is the examination and a 24 h video-EEG recording two habitual events without ictal change; five validated signs are counted and the midline-splitting sensory loss is supportive only. MRI stays optional and is a non-contrast brain report without MRA. The drug check (recommended) flags the as-needed lorazepam and the antidepressant warning under 25 years instead of a sertraline dose increase. Epilepsy and a structural lesion are low after the work-up. Musts: positive diagnosis, an explanation that addresses his fear without insisting on stress, physiotherapy, trauma-focused therapy for PTSD with his depression and anxiety, an event plan, and no lorazepam for the events.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 3 (EEG routing) applies.
- New citation keys used: `[Stone_2016]`, `[Daum_2014]`, `[Avbersek_2010]`.

## Open questions for Andrea (judgment calls you could not settle)

- None. The lorazepam must goes beyond the plan's S04 entry; it is plan fact 16 applied to the drug check the plan makes recommended, and the same must is used in RS04 and S03.

## Verification
Checked: the log tables against the final file and `git diff`; every claimed FIXED item is present (criteria tiers, required arguments, stop rule, constraints, canonical literature and drug outputs, non-contrast MRI where stored, video-EEG report, exam report, musts, prohibitions, differential, key evidence, red herrings, avoided actions, nulled fallbacks and `fallback_tool_kinds`); medications on the list match the drug-check `proposed` string verbatim; no follow-ups remain; `accepted[0]`, ICD codes, `case_id` and `condition` unchanged; event counts and durations agree across exam, EEG, musts and key evidence; differential key features cite only required or recommended results; no FND banned strings. No reviewer notes exist for FND, so the notes table is correctly empty. Also found and fixed in all six: `metadata.revision_reason` still read "every instrumental test optional", which is false after this round, and `last_revised` was 2026-08-10; both set to the condition's round wording (as in the other FND cases) and 2026-10-24.

Found and fixed:
- C, minor, lorazepam must: "review it with his psychiatrist" presumed a psychiatrist the case never names; now "his prescriber".

Checked and accepted: the sertraline boxed warning under 25 years is correct and worded differently from the criterion's expected evidence; PTSD in M-PSY follows the plan (witnessed death, intrusions and nightmares for 8 weeks); the hemicord mention in the MS or structural row is consistent with the abdominal midline sensory boundary; entrainment by foot tapping during bilateral arm shaking is a feasible test.

After the edits: `perfect_agent.py -v` passes, `case_io.py check` shows no failure naming the case, and the case guards pass.
