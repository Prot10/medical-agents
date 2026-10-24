# FND-S05
Reviewer status: R1 not reviewed, R2 not reviewed (no FND notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search[...]` | Summary and only finding were the criterion's `expected_evidence` ("Confirms multidisciplinary CBT + physiotherapy..."); leak guard failed. | FIXED: plan class B canonical seven-row output and summary; literature criterion `optional`, last. |
| A | major | `ground_truth.action_criteria` | Template tiers: literature and drug check `recommended`, MRI and video-EEG `optional`; labels equal rationales; citation strings "positive FND signs; AAN ... 2025" and "FND criteria pack ...". | FIXED (plan A, 3.2): order exam (required), MRI `action-4` (recommended, `{contrast: false}`), video-EEG `action-5` (required), drug check (optional), new `action-neuropsych-battery` (optional), literature (optional); short labels, case-specific rationales with keys, case-specific `expected_evidence`. |
| A | minor | `ground_truth.sequence_constraints`, `stop_rule` | No constraint; stop rule only the exam. | FIXED: soft exam -> MRI; `required_before_assessment` exam and video-EEG; `max_additional_actions` 0. |
| B | major | `patient.neurological_exam.motor`, `initial_tool_outputs.clinical_assessment.findings[Hoover]` | Hoover described with the examiner's hand "under left heel during contralateral left leg flexion": the hand must be under the weak (right) heel while the left hip flexes. | FIXED: hand under the right heel during contralateral left hip flexion against resistance. |
| C | major | `initial_tool_outputs.clinical_assessment` | Meta keys in `criteria_met`; "However, ..." fragment; midline splitting counted among 4 rule-in signs; impression leak "No further investigation is required...". | FIXED (plan H): library keys; 3 validated signs (Hoover, collapsing weakness, distractible tremor); midline splitting and normal walking when unobserved listed as supportive, not counted; canonical impression, "No event was observed during the examination." |
| B | major | `initial_tool_outputs.eeg` | Event described as "right leg shaking" and "second event ... identical to previous" while the habitual events are bilateral arm shaking and only one event is reported; "unresponsiveness" contradicted by squeezing a hand on command; capitals; impression without final period; no recording duration. | FIXED (plan J): one habitual event (bilateral asynchronous arm shaking, eyes open, 2 min 35 s, hand squeeze on command, typical per roommate on video review) with time and duration; 48-hour wake and sleep recording; canonical NORMAL video-EEG impression. |
| B | major | `initial_tool_outputs.mri.impression` | "without and with contrast ... no abnormal enhancement" although the criterion is non-contrast (plan I). | FIXED: non-contrast report (T1, T2, FLAIR, DWI/ADC, SWI), no enhancement statements. |
| B | minor | `patient.chief_complaint` | "Sudden onset right leg weakness" contradicts the HPI ("developing over the past 3 days"). | FIXED: "Right leg weakness over 3 days and two episodes of unresponsiveness". |
| E | minor | `patient.neurological_exam.additional` | Repeated the HPI's prior episode inside the examination. | FIXED: removed; collapsing weakness and distractible tremor stated. |
| D | minor | `initial_tool_outputs.drug_interactions` | Medication list only, with the warning "...is a prescribing decision, not an output of this check". | FIXED (plan C): no clinically significant interaction; dicyclomine anticholinergic caution. |
| C | major | `ground_truth.assessment` | Seven template musts (video-EEG as a must, neuropsychology battery as "recommended tier", duplicates, "Do NOT make the diagnosis by exclusion"); prohibitions citing "Stone 2018" and forbidding "start or continue" ASM. | FIXED (plan D): musts DX (mixed), COMM, PHYSIO, PSY (anxiety), RESCUE; prohibitions P1, P2, P3, P5, P6, P7. |
| C | major | `ground_truth.differential` | Epileptic seizures `moderate` after a normal video-EEG; template autoimmune encephalitis, malingering (no incentive), neuropathy (EMG avoided) rows with "(when obtained)". | FIXED (plan F): epileptic seizures `low` (canonical feature plus open-eyes and command-following detail); MS `low` (prior remitting right leg episode, signs, MRI); stroke or structural lesion `low`; other rows deleted. |
| D | major | `ground_truth.key_clinical_evidence` | Eight template items including the "Interim composition decision" leak, the "OPTIONAL" item and "Stone 2018" claims. | FIXED (plan E): five case-specific items. |
| C | minor | `ground_truth.red_herrings` | Generic data points. | FIXED: GAD on sertraline, divorce and custody dispute, and new "eyes open and rolled back" (favours epilepsy; video-EEG decides). |
| C | minor | `ground_truth.avoided_actions[*]` | Cited the nonexistent `[Stone_2018]`; generic rationales. | FIXED (plan L): same 8 waste criteria and ids, `[Espay_2018]` / `[Stone_2016]`, patient-specific rationales. |
| D | minor | `fallback_tool_outputs.specialized_test`, `.advanced_imaging`, `.drug_interactions`, `.literature_search` | Empty `test_type`/`modality`, "agent not specified" and no-evidence stubs. | FIXED (plan G): nulled, removed from `metadata.fallback_tool_kinds`; echo fallback given `echo_type: TTE`. |
| E | minor | `metadata.difficulty_rationale`, `revision_reason` | Template; claimed "supportive normal labs" (no labs in the case). | FIXED: case-specific. |

## Changes, in one paragraph a physician can read before re-reviewing
The case now requires the examination and a video-EEG, and recommends one non-contrast brain MRI. The examination documents three validated signs (right Hoover sign, now described correctly with the hand under the right heel; collapsing weakness of the right leg; a right hand tremor that stops with serial 7s), with midline-splitting sensory loss and normal walking when unobserved listed as supportive only. The video-EEG now records one habitual event that matches the history (bilateral asynchronous arm shaking, eyes open, 2 min 35 s, hand squeeze on command, confirmed as typical by the roommate) without ictal change, in a normal 48-hour record. The MRI is justified by the remitting right leg episode two years earlier (demyelination question) and is reported as a normal non-contrast study. The chief complaint no longer says "sudden onset" (the HPI says 3 days). Epileptic seizures are `low` after the recording, with co-occurring epilepsy noted as possible; MS and stroke are `low` with case-specific reasons; template rows are removed. Musts are the positive diagnosis, explanation, FND physiotherapy, psychological therapy with treatment of her anxiety, and a written event plan; prohibitions are the plan's P1-P3 and P5-P7. Literature and drug-check outputs are canonical and no longer echo the scoring key.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- None beyond the plan's condition-wide CENTRAL list (pack keys `[Stone_2016]`, `[Daum_2014]`, `[Avbersek_2010]` used here are plan 1.1 (C) keys; EEG routing for a `routine` order, plan 5.3).

## Open questions for Andrea (judgment calls you could not settle)
- None.

## Checks
- `perfect_agent.py FND-S05 -v`: ok; exam served by `initial_tool_outputs.clinical_assessment`, MRI by `initial_tool_outputs.mri`, video-EEG by `initial_tool_outputs.eeg` (verified by executing each call through the environment).
- `case_io.py check FND-S05`: schema and synonym guard OK; no failure names FND-S05 (remaining condition-wide leak failures name M09, P08, S06, S10 only).
- `test_case_guards.py -k FND-S05`: pass.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case against the plan (section 4 S05, classes A-L) and PATTERNS.md.
- Confirmed: Hoover manoeuvre now correct in both exam and assessment; EEG event now matches the HPI (bilateral arm shaking, eyes open) instead of the old "right leg shaking"; non-contrast MRI with `contrast_used` absent and no enhancement text; literature and drug outputs differ from every `expected_evidence`; differential low after the recording; musts and prohibitions are the plan set; diagnosis label and codes unchanged; stop rule = required criteria; constraint exam -> MRI soft; no em dashes or banned strings in new text.
- Found and fixed: `action-4-analyze-brain-mri.rationale` called it "a first presentation" while citing the remitting episode two years earlier (now "Acute right leg weakness with a remitting episode..."); `avoid-waste-3-order-cardiac-monitoring.rationale` read "no pallor or collapse with rapid recovery", which seemed to deny her rapid recovery (now "2-3 minutes of bilateral shaking without pallor, not a brief collapse").
- Checks after my edits: `perfect_agent.py -v` ok (each required and recommended call served by the case's own stored report, not a fallback; the "<- ?" source label is a dump-format artefact, confirmed by executing the calls through the environment); `case_io.py check` schema and synonym guard OK, no test failure names the case; `test_case_guards.py -k` pass; discriminator guard (FND not yet enabled) run by hand: clean.
- Flagged for the condition lead (not changed, plan class L governs all 30): ECG kept as `waste` in event cases. NICE CG109 and NG217 advise a 12-lead ECG after a first transient loss of consciousness or suspected first seizure; where the events are unrecorded before admission the lead may prefer to drop the ECG avoided action rather than penalize it.
