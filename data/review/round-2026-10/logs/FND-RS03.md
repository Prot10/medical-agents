# FND-RS03
Reviewer status: R1 not reviewed, R2 not reviewed (FND has no notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.eeg` | The criterion orders a video-EEG, but the stored report was a "single routine recording" with an unnamed "clinical event captured"; impression did not open "This is a NORMAL ...", omitted the event description and lacked a final period; sleep spindles placed in drowsiness. | FIXED (plan J): 48 h inpatient video-EEG with ECG channel; two habitual events (day 1 1 min 40 s, day 2 2 min 50 s, eyes closed, bilateral arm shaking, responsive to her name in event 2) with persisting posterior alpha and no postictal slowing; ECG channel sinus rhythm 82 to 112/min, no pause; spindles in N2; canonical impression; limitation states the artifact. |
| C | major | `ground_truth.action_criteria[action-4-analyze-eeg]` | Video-EEG `optional` ("consider ... when ambiguous") in a case whose whole question is a doubted outside label of psychogenic seizures. | FIXED (plan 3.2): required, canonical expected_evidence, case rationale (ILAE documented level, AAN 2025 co-occurring epilepsy), added to `stop_rule.required_before_assessment`. |
| A | major | `ground_truth.action_criteria[*]` | Template criteria: label equal to rationale, "FND criteria pack ..." pseudo-citations, literature and drug check `recommended`. | FIXED (plan A, 3): order exam, video-EEG, drug check, MRI, neuropsychology, literature; short labels, patient-specific rationales and evidence; literature optional and last; drug check optional (plan); new optional `action-neuropsych-battery`. |
| C | minor | `ground_truth.action_criteria` (new `action-brain-mri`) | Twelve months of progressive right leg weakness with sensory symptoms: a single non-contrast MRI is defensible (pack section 2, Optional), but the plan lists RS03 with no MRI criterion, so such a scan counted as an unjustified action against `max_additional_actions: 0`. | FIXED: optional `action-brain-mri` (`{"contrast": false}`), no stored output (library normal answers it). See Open questions. |
| D | major | `followup_outputs[0]` (literature) | Misattributed source ("Espay ... Lancet Neurology 2018, new subtypes and shared mechanisms" is Hallett et al. 2022), summary repeating the scoring key ("CBT have the strongest evidence base"). | FIXED (plan B): follow-up deleted; canonical `initial_tool_outputs.literature_search` keyed by the criterion query; fallback null. |
| D | major | `followup_outputs[1]` (drug check) | Output was a prescribing plan (sertraline, duloxetine alternatives, escitalopram dose increase). | FIXED (plan C): deleted; `initial_tool_outputs.drug_interactions` lists her three medicines verbatim, the escitalopram with sumatriptan serotonergic interaction, an escitalopram QTc warning and a loperamide note, report-voice summary. |
| C | major | `initial_tool_outputs.clinical_assessment` | Meta `criteria_met` keys; seven "signs" counted including non-dermatomal sensory loss and pinprick variability (low specificity); Hoover described only as "involuntary hip extension" during contralateral flexion, without the weak voluntary hip extension on direct testing that the sign compares it with; leak sentence "No further investigation is required to make the diagnosis...". | FIXED (plan H): canonical shape; 5 rule-in signs counted (Hoover, collapsing weakness, dragging monoplegic gait, distractibility, entrainment); supportive features listed as not counted; observed event described; event-based impression; library criteria keys plus `functional_seizure_semiology_observed: true`. |
| B | minor | `patient.neurological_exam.motor`, `.additional` | Hoover described incompletely (as above); entrainment by "tapping the contralateral hand" during bilateral arm shaking is not a coherent test. | FIXED: Hoover reworded (weak right hip extension that becomes full with left hip flexion against resistance); entrainment by tapping with the right foot; "tremor" called shaking; em dash removed from the rewritten sentence. |
| C | major | `ground_truth.assessment.required_recommendations` | Seven template musts: two duplicates, video-EEG as a must, neuropsychological battery as a must ("recommended tier", pack says optional). | FIXED (plan D): M-DX (mixed phenotype, this case's signs and recorded events), M-COMM plus addressing her doubt with the recorded events and signs, M-PSY (generalized anxiety disorder worse since the separation), M-PHYSIO, M-RESCUE. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Eight template prohibitions citing the non-existent "Stone 2018"; "start or continue long-term" antiseizure drugs (she takes none); a duplicate EMG/biopsy item. | FIXED: canonical P1, P2, P3, P5, P6, P7. |
| C | major | `ground_truth.differential` | Template: epileptic seizures `moderate` after the work-up; stroke, "normal brain MRI" and "(when obtained) EMG/NCS" cited with no MRI or EMG in the pathway; autoimmune encephalitis; malingering on a symptom-validity test never done. Convulsive syncope (raised by her syncope admission) missing. | FIXED (plan F): epileptic seizures `low` (canonical key feature); convulsive syncope `low` (duration, closed eyes, responsiveness, posterior rhythm and sinus rhythm on the ECG channel); MS or structural lesion `low` (clinical incompatibility). Stroke, neuropathy, encephalitis and malingering removed (not raised; no external incentive). |
| D | major | `ground_truth.key_clinical_evidence` | Template items: the "Interim composition decision, August 2026" engineering leak, "Brain MRI and basic laboratory testing are OPTIONAL here", "Stone 2018" claims. | FIXED (plan E): five case-specific items (signs, recorded events, outside label, prior syncope, context as supportive). |
| B | major | `ground_truth.red_herrings` | "Family history of epilepsy in a relative" cites absent data (FH states no epilepsy); generic psychiatric and stressor data points; stressor "intended effect" framed abbreviating the work-up as the trap. | FIXED: FH row deleted; psychiatric and stressor rows name the case data; stressor trap is making the diagnosis from the stressor alone; added the outside label (plan) and the prior syncope with unrevealing cardiac work-up. |
| C | minor | `ground_truth.avoided_actions[*]` | Rationales generic ("adds no information beyond MRI" with no MRI), `[Stone_2018]` citations. | FIXED (plan L): patient-specific rationales; `[Stone_2016]` / `[Espay_2018]`. All stay `waste`. |
| D | minor | `fallback_tool_outputs.specialized_test`, `.advanced_imaging` | Specialized-test fallback with empty `test_type` and the leak "the negative result is itself a harm"; advanced-imaging fallback with empty `modality`. | FIXED (plan G): both null, removed from `metadata.fallback_tool_kinds`. |
| D | minor | `fallback_tool_outputs.echo` | "Benign incidental finding" not named; no `echo_type`. | FIXED: impression names trace physiological mitral regurgitation; `echo_type: TTE`; kind `normal`. |
| B | minor | `metadata.difficulty_description`, `.difficulty_rationale` | Cited a "normal MRI and supportive normal labs" that the case does not contain. | FIXED: rewritten for this case. |
| - | check | probe | `perform_clinical_assessment`, `analyze_eeg {video}`, `check_drug_interactions` (any drug) and `search_medical_literature` (any query) return the case's own reports; MRI and neuropsychology return library normals; TTE returns the case fallback. `perfect_agent.py -v`: exam and video-EEG answered by the case's outputs; ok. Case guards pass; `case_io.py check` shows no failure naming FND-RS03 (the remaining FND failures are the P08, S06, S10 leak guard of other workers' cases). | - |

## Changes, in one paragraph a physician can read before re-reviewing

The case is unchanged clinically (26-year-old woman, 12 months of shaking events and fluctuating right leg weakness, outside label of psychogenic seizures that she doubts, prior syncope admission with unrevealing cardiac work-up). The required work-up is now the examination and an inpatient video-EEG, which records two habitual events (bilateral arm shaking with the eyes closed, 1 min 40 s and 2 min 50 s, responsive to her name in the second) without ictal change, with a persisting posterior rhythm and sinus rhythm on the ECG channel. The examination report counts five validated signs (right Hoover sign, now described in full, collapsing weakness, dragging monoplegic gait, distractibility and entrainment during the witnessed event) and lists the midline-splitting sensory loss as supportive only. The drug check (optional) reports the escitalopram with sumatriptan serotonergic interaction; MRI without contrast and neuropsychology are optional; literature is optional and last. The differential is the post-work-up view: epileptic seizures low, convulsive syncope low, MS or a structural lesion low on clinical grounds. Musts are the positive diagnosis, the explanation that addresses her doubt with the recorded events and signs, psychological therapy with treatment of her anxiety, physiotherapy and an event plan without benzodiazepines; prohibitions are the canonical six.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 3 (EEG routing) confirmed here: `analyze_eeg {"eeg_type": "routine"}` returns the stored video-EEG with its two recorded events.
- New citation keys used: `[Stone_2016]`, `[Daum_2014]` (plan 1.1, keys marked (C)).

## Open questions for Andrea (judgment calls you could not settle)

- Resolved by the worker, deviating from the plan (which lists RS03 with no MRI criterion): an optional non-contrast brain MRI criterion was added. Twelve months of progressive right leg weakness with sensory symptoms makes one scan defensible (pack section 2, Optional, "a single scan is defensible but earns no diagnostic credit"), and S01-S04, with weeks of leg weakness, carry the same optional MRI. Without it a single defensible scan counted against `max_additional_actions: 0`. To revert, delete `action-brain-mri`. Lead to confirm for condition consistency.

## Verification
Checked: the log tables against the final file and `git diff`; every claimed FIXED item is present (criteria tiers, required arguments, stop rule, constraints, canonical literature and drug outputs, non-contrast MRI where stored, video-EEG report, exam report, musts, prohibitions, differential, key evidence, red herrings, avoided actions, nulled fallbacks and `fallback_tool_kinds`); medications on the list match the drug-check `proposed` string verbatim; no follow-ups remain; `accepted[0]`, ICD codes, `case_id` and `condition` unchanged; event counts and durations agree across exam, EEG, musts and key evidence; differential key features cite only required or recommended results; no FND banned strings. No reviewer notes exist for FND, so the notes table is correctly empty. Also found and fixed in all six: `metadata.revision_reason` still read "every instrumental test optional", which is false after this round, and `last_revised` was 2026-08-10; both set to the condition's round wording (as in the other FND cases) and 2026-10-24.

Found and fixed:
- B, minor, timeline: `patient.clinical_history.past_medical_history` dated the outside psychogenic-seizure diagnosis to "age 23", but she is 26 and the HPI says the episodes began a year ago, so the label could not predate the illness. Now "diagnosed at an outside facility during the current illness"; the matching red-herring `data_point` updated the same way.

Checked and accepted: the worker's added optional `action-brain-mri` (a deviation from plan 3.2, flagged for the lead): optional criteria carry no credit and no stop-rule penalty, the prohibition list does not forbid a first MRI, and there is no prior MRI, so it is clinically defensible. The convulsive-syncope row correctly cites the ECG channel stored in the video-EEG. The midline split of a whole-leg sensory loss is left as written (not anatomically impossible; supportive only).

After the edits: `perfect_agent.py -v` passes, `case_io.py check` shows no failure naming the case, and the case guards pass.

## Condition audit

2026-10-24, FND condition auditor.

- `action-brain-mri.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-neuropsych-battery.expected_evidence`: was empty; set to the wording the other optional batteries use.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.

## Close-out (24 Oct 2026)

Andrea's FND ruling of 24 Oct 2026 and the close-out decisions (`plans/FND-decisions.md`). What changed and why:

- `action-4-analyze-eeg` (video-EEG) required -> optional, removed from the stop rule; rationale now says what the diagnosis rests on without the recording (ILAE 2013 levels).
- M-DX must, COMM must, red-herring interpretations and metadata no longer say the diagnosis rests on the video-EEG: they rest on the positive signs and the event semiology, with video-EEG confirmation where recorded (open question 8).
- Diagnosis synonyms scoped by phenotype (`diagnosis_synonyms.yaml` F44 entries; a label or code naming another presentation must not score): added "psychogenic nonepileptic seizures", "dissociative seizures", "nonepileptic seizures", "functional limb weakness", "functional motor disorder", "functional tremor".
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FND-` passes, now including the discriminator guard.
