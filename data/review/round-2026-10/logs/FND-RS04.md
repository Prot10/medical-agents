# FND-RS04
Reviewer status: R1 not reviewed, R2 not reviewed (FND has no notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.action_criteria[action-5-analyze-eeg]` | Video-EEG `optional` in a patient treated with lorazepam for presumed seizures. | FIXED (plan 3.2): required, canonical expected_evidence, case rationale, in `stop_rule.required_before_assessment`. |
| B | major | `initial_tool_outputs.eeg` | Not identified as a video-EEG, unnamed "clinical event captured" finding, impression not in the canonical form and without a final period. | FIXED (plan J): 48 h inpatient video-EEG with ECG channel; two habitual events with times, durations and semiology (asynchronous shaking, pelvic thrusting, eyes closed and resisting opening; 2 min 20 s and 3 min 05 s), posterior alpha persisting, no postictal slowing; canonical impression; N2 sleep features added. |
| C | major | `ground_truth.action_criteria[action-4-analyze-brain-mri]` | MRI `optional` although the outside team considered stroke or demyelination and gave empirical dexamethasone; required argument `protocol: standard` would have failed a correct non-contrast `stroke` or `ms` order. | FIXED (plan 3.2): recommended, `{"contrast": false}` only; case rationale; soft constraint exam before MRI. |
| B | major | `initial_tool_outputs.mri` | The criterion orders a non-contrast MRI, but the report described a study "with and without gadolinium contrast", a post-contrast row and MRA sequences (no MRA criterion). | FIXED (plan I): non-contrast technique line (T1, T2, FLAIR, DWI/ADC, SWI), enhancement and MRA statements removed, impression "Normal non-contrast MRI of the brain...". |
| D | major | `followup_outputs[0]` (literature) | Fabricated or misattributed sources ("Stone J, Zeman A, Sharpe M ... Hoover sign ... 2002" with the McWhirter 2011 figures; LaFrance 2013 titled as a systematic review) and a summary echoing the scoring key. | FIXED (plan B): deleted; canonical initial literature output keyed by the criterion query; literature fallback null. |
| B | major | `followup_outputs[1]` (drug check) | Cross-modality "Current ECG shows normal QTc (418 ms)" with no ECG in the case; SSRI alternatives as prescribing advice; benzodiazepine issue missed. | FIXED (plan C): deleted; initial drug output lists her three medicines verbatim, escitalopram with naproxen (GI bleeding), escitalopram with clonazepam (minor), a benzodiazepine warning (no rescue use, gradual taper) and the escitalopram 20 mg maximum; criterion recommended with a case rationale. |
| B | minor | `patient.history_present_illness` | "Denies ... back pain" contradicts chronic low back pain treated with naproxen in the past history. | FIXED: "new back pain". |
| C | major | `initial_tool_outputs.clinical_assessment` | Meta `criteria_met` keys; findings were sentence fragments ("however, when distracted ..."); six "signs" counted, including midline-splitting sensory loss and a gait fragment; leak sentence "No further investigation is required...". | FIXED (plan H): canonical shape; 3 rule-in signs counted (Hoover, collapsing weakness, distractibility); observed events described; supportive features listed as not counted; event-based impression. The circumducting, variable gait is not counted as a dragging monoplegic gait (circumduction is not that sign). |
| B | minor | `patient.neurological_exam.additional` | Hoover described without the weak voluntary hip extension it is compared with, plus commentary ("demonstrating intact motor pathways"). | FIXED: weak right hip extension on direct testing, full involuntary extension during resisted left hip flexion. |
| C | major | `ground_truth.assessment.required_recommendations` | Seven template musts (duplicates, video-EEG as a must, neuropsychology as a must). | FIXED (plan D): M-DX, M-COMM, M-PHYSIO, M-PSY (recurrent depression and GAD), M-RESCUE, plus a case must not to use her as-needed clonazepam for the events and to taper it with her psychiatrist (plan fact 16; the drug check is recommended for this reason). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Template prohibitions with "Stone 2018", "start or continue" antiseizure drugs. | FIXED: canonical P1, P2, P3, P5, P6, P7, plus "Continue or restart empirical corticosteroids for presumed demyelination or stroke" (dexamethasone is not on the current list, so the plan's conditional "Stop dexamethasone" must does not apply; the prohibition covers it). |
| C | major | `ground_truth.differential` | Epileptic seizures `moderate` after the work-up; template structural, neuropathy "(when obtained) EMG/NCS" and autoimmune encephalitis rows. | FIXED (plan F): epileptic seizures `low` (canonical feature), acute ischemic stroke `low`, MS `low` (citing the resolved episodes in her twenties, the examination and the MRI), spinal cord lesion `low` (the inguinal sensory boundary raises it; unilateral all-modality loss, intact posterior columns, normal reflexes and bladder argue against). Neuropathy, encephalitis and the duplicate structural row removed. |
| D | major | `ground_truth.key_clinical_evidence` | Template items including the "Interim composition decision" leak and "Stone 2018" claims. | FIXED: five case-specific items. |
| B | major | `ground_truth.red_herrings` | "Family history of MS" and "family history of epilepsy" cite data the case denies ("No family history of epilepsy, multiple sclerosis, or stroke"); generic psychiatric and stressor rows; stressor trap framed as abbreviating the work-up. | FIXED: both FH rows deleted; psychiatric and stressor rows name the case data; added the outside lorazepam and dexamethasone, and the resolved episodes of weakness in her twenties (MS anchor). |
| C | minor | `ground_truth.avoided_actions[*]` | Generic rationales, `[Stone_2018]`. | FIXED (plan L): patient-specific rationales, `[Espay_2018]` / `[Stone_2016]`; all stay `waste`. |
| D | minor | `fallback_tool_outputs.specialized_test`, `.advanced_imaging`, `.echo` | Empty discriminators and the "negative result is itself a harm" leak; echo without `echo_type`. | FIXED (plan G): specialized-test and advanced-imaging fallbacks null and removed from `metadata.fallback_tool_kinds`; echo `echo_type: TTE`. |
| B | minor | `metadata.difficulty_description`, `.difficulty_rationale` | Template text ("supportive normal labs"; no labs in the case). | FIXED: rewritten. |
| - | check | probe | Exam, MRI (`contrast: false`, any protocol), video-EEG, drug check and literature return the case's own reports; perfect_agent `-v` ok in the order exam, MRI, video-EEG, drug check; case guards pass; `case_io.py check` shows no failure naming FND-RS04. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The case is unchanged clinically (40-year-old woman, five days of right leg weakness and shaking events after an argument, lorazepam and empirical dexamethasone at the outside hospital, clonazepam as needed). The required work-up is the examination and a 48 h video-EEG that records two habitual events (asynchronous generalized shaking with pelvic thrusting and the eyes held closed, 2 min 20 s and 3 min 05 s) without ictal change. A non-contrast brain MRI with diffusion is recommended once, after the examination, for the stroke and demyelination question the outside team raised; the stored report is now a non-contrast study with no MRA. The examination counts three validated signs (right Hoover sign, collapsing weakness, distractibility); the inguinal sensory boundary and the variable circumducting gait are supportive only. The drug check (recommended) reports escitalopram with naproxen and the benzodiazepine cautions for clonazepam, without the ECG value the case never measured. Stroke, MS, a cord lesion and epilepsy are all low after the work-up. Musts: positive diagnosis, explanation, physiotherapy, psychological therapy with treatment of depression and anxiety, an event plan, and no clonazepam for the events with a gradual taper; prohibitions include restarting empirical steroids.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 3 (EEG routing) applies: a `routine` EEG order returns the stored video-EEG.
- MRI routing does not discriminate contrast: `analyze_brain_mri {"contrast": true}` returns the stored non-contrast report. Harmless here (the report says no contrast was given), noted for the harness owners.
- New citation keys used: `[Stone_2016]`, `[Daum_2014]`, `[Avbersek_2010]` (plan 1.1).

## Open questions for Andrea (judgment calls you could not settle)

- None. The case-specific clonazepam must goes beyond the plan's RS04 entry; it applies plan fact 16 (benzodiazepine PRN: taper) and AAN 2025, and can be dropped without affecting anything else.

## Verification
Checked: the log tables against the final file and `git diff`; every claimed FIXED item is present (criteria tiers, required arguments, stop rule, constraints, canonical literature and drug outputs, non-contrast MRI where stored, video-EEG report, exam report, musts, prohibitions, differential, key evidence, red herrings, avoided actions, nulled fallbacks and `fallback_tool_kinds`); medications on the list match the drug-check `proposed` string verbatim; no follow-ups remain; `accepted[0]`, ICD codes, `case_id` and `condition` unchanged; event counts and durations agree across exam, EEG, musts and key evidence; differential key features cite only required or recommended results; no FND banned strings. No reviewer notes exist for FND, so the notes table is correctly empty. Also found and fixed in all six: `metadata.revision_reason` still read "every instrumental test optional", which is false after this round, and `last_revised` was 2026-08-10; both set to the condition's round wording (as in the other FND cases) and 2026-10-24.

Found and fixed:
- C, major, `ground_truth.differential["Spinal cord lesion"].key_features`: said the sensory loss "involves all modalities on the weak side with intact posterior columns", a self-contradiction (vibration and proprioception are intact; only light touch and pinprick are lost). Rewritten: light-touch and pinprick loss on the same side as the weakness with intact posterior columns is the reverse of a hemicord pattern, and reflexes, plantars and bladder are normal.
- B, minor, `patient.neurological_exam.sensory`: "(midline splitting pattern)" labelled a boundary at the inguinal crease, which is not midline splitting; parenthesis removed (the exam report and key evidence already say "ending at the inguinal crease").
- C, minor, clonazepam must: "review it with her psychiatrist" presumed a psychiatrist the case never names; now "her prescriber".

Checked and accepted: dexamethasone is not on the current list, so the "Continue or restart empirical corticosteroids" prohibition (rather than a "Stop dexamethasone" must) is the right reading of the plan; a 2-day course needs no taper. MRI routing that ignores `contrast` stays under the worker's CENTRAL note.

After the edits: `perfect_agent.py -v` passes, `case_io.py check` shows no failure naming the case, and the case guards pass.

## Condition audit

2026-10-24, FND condition auditor.

- `action-neuropsych-battery.expected_evidence`: was empty; set to the wording the other optional batteries use.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.

## Close-out (24 Oct 2026)

Andrea's FND ruling of 24 Oct 2026 and the close-out decisions (`plans/FND-decisions.md`). What changed and why:

- `action-5-analyze-eeg` (video-EEG) required -> optional, removed from the stop rule; rationale now says what the diagnosis rests on without the recording (ILAE 2013 levels).
- M-DX must, COMM must, red-herring interpretations and metadata no longer say the diagnosis rests on the video-EEG: they rest on the positive signs and the event semiology, with video-EEG confirmation where recorded (open question 8).
- Diagnosis synonyms scoped by phenotype (`diagnosis_synonyms.yaml` F44 entries; a label or code naming another presentation must not score): removed "functional movement disorder"; added "psychogenic nonepileptic seizures", "dissociative seizures", "nonepileptic seizures", "functional limb weakness", "functional motor disorder".
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FND-` passes, now including the discriminator guard.
