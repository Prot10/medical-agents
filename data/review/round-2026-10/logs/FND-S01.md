# FND-S01
Reviewer status: R1 not reviewed, R2 not reviewed (FND has no notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.action_criteria[action-5-analyze-eeg]` | Video-EEG `optional` although she was admitted for video-EEG with daily events. | FIXED (plan 3.2): required, canonical expected_evidence, case rationale, in the stop rule. |
| B | minor | `initial_tool_outputs.eeg` | Impression "NORMAL EEG. A clinical seizure-like event was captured..." not in canonical form, no final period; finding unnamed ("Clinical event captured") with no time or duration; spindles "during drowsiness"; artifact field `note`. | FIXED (plan J): 24 h inpatient video-EEG; one habitual event (day 1, 1 min 30 s: arrhythmic waxing and waning shaking, forced eye closure, side-to-side head movements, answered to her name in parts), posterior alpha persisting, no postictal slowing; canonical impression; spindles in N2; artifact `description`. The event is the one witnessed at the examination (the exam states video-EEG was recording). |
| B | major | `initial_tool_outputs.mri` | Criterion orders `contrast: false`, but the report was "with and without contrast" with a post-contrast row. | FIXED (plan I): non-contrast technique line (T1, T2, FLAIR, DWI/ADC, SWI); enhancement statements removed. Criterion stays optional; required argument reduced to `{"contrast": false}` (the old `protocol: standard` would have failed any other non-contrast protocol). |
| D | major | `followup_outputs[0]` (literature) | Fabricated results: CODES "reduced seizure frequency" (it did not, on the primary outcome); "Espay ... Lancet Neurology 2018 ... new subtypes and shared mechanisms" (Hallett et al. 2022); summary echoing the scoring key. | FIXED (plan B): deleted; canonical initial literature output; fallback null. |
| D | major | `followup_outputs[1]`, `initial_tool_outputs.drug_interactions` | Follow-up was a plan ("Sertraline 150 mg daily (dose increase)", SNRI alternatives); initial output an empty list with the leak "...is a prescribing decision, not an output of this check". | FIXED (plan C): follow-up deleted; initial output lists her medicines verbatim, sertraline with ibuprofen (GI bleeding) and a dicyclomine anticholinergic note; optional criterion. |
| B | minor | `patient.clinical_history.social_history.recent_stressors` | "A new school principal" for a paralegal (the HPI says "a new supervisor"): template carry-over. | FIXED: "a new supervising attorney". |
| B | minor | `patient.neurological_exam.motor` | Hoover written in capitals with an em dash and without the weak voluntary hip extension it is compared with. | FIXED: "Hoover sign positive on the right: right hip extension is weak on direct testing but becomes full when she flexes the left hip against resistance." |
| C | major | `initial_tool_outputs.clinical_assessment` | Meta `criteria_met` keys; six "signs" counted including the midline-splitting sensory loss; findings were copied sentence fragments; leak sentence "No further investigation is required...". | FIXED (plan H): canonical shape; 4 rule-in signs (Hoover, collapsing weakness, dragging monoplegic gait, distractibility); observed event; supportive features not counted; event-based impression. |
| C | major | `ground_truth.assessment.*` | Template musts (duplicates, video-EEG and neuropsychology as musts) and prohibitions ("Stone 2018", "start or continue" antiseizure drugs). | FIXED (plan D): M-DX, M-COMM with addressing her fear of MS or a tumor, M-PHYSIO, M-PSY (GAD and depression), M-RESCUE; prohibitions P1 naming the repeat CT, P2, P3, P5, P6, P7. |
| C | major | `ground_truth.differential` | Epileptic seizures `moderate` after the work-up; MS, stroke and structural rows citing an MRI that is optional; neuropathy "(when obtained) EMG/NCS"; autoimmune encephalitis. | FIXED (plan F): epileptic seizures `low` (canonical, naming the grandmother's epilepsy); one row "MS, tumor or another structural lesion of the brain or spinal cord" `low` on clinical incompatibility. Stroke (4-week progressive course), neuropathy and encephalitis removed. |
| D | major | `ground_truth.key_clinical_evidence` | Template items including the "Interim composition decision" leak and "Stone 2018". | FIXED: five case-specific items. |
| B | major | `ground_truth.red_herrings` | "Family history of MS" cites data the FH denies; the epilepsy row was generic although the FH names a maternal grandmother; generic psychiatric and stressor rows. | FIXED: MS row deleted; epilepsy row names the grandmother; psychiatric and stressor rows name the case data; added her fear of MS or a tumor (trap: tests to reassure). |
| B | minor | `fallback_tool_outputs.ct` | A repeat CT would have reported a 3 mm right frontal calcified granuloma that neither the "normal" outside CT nor the MRI shows. | FIXED: normal CT with comparison to the outside study; `fallback_tool_kinds.ct` normal. The CT avoided action is now framed as a repeat study. |
| C | minor | `ground_truth.avoided_actions[*]` | Generic rationales, `[Stone_2018]`. | FIXED (plan L): patient-specific rationales, `[Espay_2018]` / `[Stone_2016]`; all stay `waste`. |
| D | minor | `fallback_tool_outputs.specialized_test`, `.advanced_imaging`, `.echo` | Empty discriminators and the "itself a harm" leak; echo without `echo_type`. | FIXED (plan G): null and removed from kinds; echo `TTE`. |
| B | minor | `metadata.difficulty_rationale`, `.key_positive_signs` | Template rationale ("normal MRI and supportive normal labs"); key signs listed midline splitting and "PNES on video-EEG". | FIXED: rationale rewritten; key signs list the validated ones. |
| - | check | probe | Exam, video-EEG, MRI (`contrast: false`), drug check and literature return the case's reports; CT and echo return the corrected fallbacks. perfect_agent `-v` ok; case guards pass; `case_io.py check` shows no failure naming FND-S01. | - |

## Changes, in one paragraph a physician can read before re-reviewing

Clinically unchanged: a 28-year-old paralegal with four weeks of right leg weakness and daily shaking episodes, a normal outside CT, admitted for video-EEG, afraid of multiple sclerosis or a tumor. The required work-up is the examination and the video-EEG, which records the witnessed habitual event (90 s of arrhythmic shaking with forced eye closure and side-to-side head movements) without ictal change. The examination counts four validated signs (right Hoover sign, collapsing weakness, dragging gait, distractibility); midline splitting is supportive only. The MRI, if ordered, is a non-contrast study and stays optional; a repeat CT is waste and its fallback is now normal like the outside study. The drug check (optional) reports sertraline with ibuprofen instead of a sertraline dose increase. Epilepsy and a structural lesion are low after the work-up. Musts: positive diagnosis, explanation that addresses her fear of MS or a tumor, physiotherapy, psychological therapy with treatment of anxiety and depression, and an event plan without benzodiazepines.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 3 (EEG routing) applies.
- New citation keys used: `[Stone_2016]`, `[Daum_2014]`, `[Avbersek_2010]`.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification
Checked: the log tables against the final file and `git diff`; every claimed FIXED item is present (criteria tiers, required arguments, stop rule, constraints, canonical literature and drug outputs, non-contrast MRI where stored, video-EEG report, exam report, musts, prohibitions, differential, key evidence, red herrings, avoided actions, nulled fallbacks and `fallback_tool_kinds`); medications on the list match the drug-check `proposed` string verbatim; no follow-ups remain; `accepted[0]`, ICD codes, `case_id` and `condition` unchanged; event counts and durations agree across exam, EEG, musts and key evidence; differential key features cite only required or recommended results; no FND banned strings. No reviewer notes exist for FND, so the notes table is correctly empty. Also found and fixed in all six: `metadata.revision_reason` still read "every instrumental test optional", which is false after this round, and `last_revised` was 2026-08-10; both set to the condition's round wording (as in the other FND cases) and 2026-10-24.

Found and fixed:
- E, minor, `patient.neurological_exam.motor`: the rewritten string kept an em dash; replaced with a semicolon.

Checked and accepted: the witnessed 90 s exam event is the 1 min 30 s habitual event on the video-EEG (the exam says the recording was running), consistent everywhere; the repeat-CT fallback is now normal and matches the outside CT.

After the edits: `perfect_agent.py -v` passes, `case_io.py check` shows no failure naming the case, and the case guards pass.

## Condition audit

2026-10-24, FND condition auditor.

- `action-4-analyze-brain-mri.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-neuropsych-battery.expected_evidence`: was empty; set to the wording the other optional batteries use.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.
