# FND-S02
Reviewer status: R1 not reviewed, R2 not reviewed (FND has no notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.neurological_exam.motor`, `initial_tool_outputs.clinical_assessment.findings` | Hoover sign described against "voluntary right hip flexion"; the sign compares weak voluntary hip extension with involuntary extension during contralateral hip flexion. | FIXED: "voluntary right hip extension is weak on direct testing, but involuntary right hip extension is strong when she flexes the left hip against resistance"; capitals and em dash removed. |
| B | minor | `patient.neurological_exam.sensory` | Loss "of the entire right leg to the inguinal crease" that also "splits the trunk exactly at the midline": the leg pattern does not reach the trunk. | FIXED: "the entire right leg up to the inguinal crease, with a sharp non-dermatomal boundary at the crease". |
| C | major | `ground_truth.action_criteria[action-5-analyze-eeg]` | Video-EEG `optional` in a patient admitted with recurrent shaking events. | FIXED (plan 3.2): required, canonical expected_evidence, case rationale (aunt with generalized epilepsy), in the stop rule. |
| B | major | `initial_tool_outputs.eeg` | A "single 60-minute routine video-EEG" suggesting prolonged monitoring; "NO electrographic correlate" in capitals; beta "likely related to anxious state or sertraline use" (attribution outside the modality); unnamed event finding. | FIXED (plan J): 24 h inpatient video-EEG with one habitual event (day 1, 1 min 15 s, eyes closed, answering questions), posterior alpha discernible, no postictal slowing; canonical impression; attribution removed; limitation cleared. |
| B | major | `initial_tool_outputs.mri` | Criterion orders `contrast: false` but the report states "with and without gadolinium" and "No enhancing lesions post-gadolinium". | FIXED (plan I): non-contrast technique line, enhancement statements removed; criterion stays optional with `{"contrast": false}` only. |
| D | major | `followup_outputs[0]` (literature) | CODES misreported as reducing seizure frequency; Espay misattributed to the Hallett 2022 Lancet Neurology review; summary near the scoring key. | FIXED (plan B): deleted; canonical initial literature output; fallback null. |
| D | major | `followup_outputs[1]`, `initial_tool_outputs.drug_interactions` | Follow-up a prescribing plan ("Sertraline 150 mg daily (dose increase)", paroxetine, SNRIs); initial output empty with the "prescribing decision" leak. | FIXED (plan C): follow-up deleted; initial output with her medicines verbatim, sertraline with ibuprofen (GI bleeding) and sertraline with hydroxyzine (QT, sedation; hydroxyzine 100 mg daily adult maximum); optional criterion. |
| C | major | `initial_tool_outputs.clinical_assessment` | Meta keys; six "signs" counted including midline splitting and distraction-dependent proprioception; fragments; leak sentence. | FIXED (plan H): 4 rule-in signs (Hoover, collapsing weakness, dragging monoplegic gait without circumduction, distractibility); observed event; supportive features not counted; canonical impression. |
| C | major | `ground_truth.assessment.*` | Template musts and prohibitions. | FIXED (plan D): M-DX, M-COMM, M-PHYSIO, M-PSY (GAD, re-establishing the lapsed psychiatric follow-up, trauma-informed care for the childhood abuse), M-RESCUE; P1 naming the repeat CT, P2, P3, P5, P6, P7. |
| C | major | `ground_truth.differential` | Epileptic seizures `moderate` after the work-up; MRI-based key features with an optional MRI; neuropathy "(when obtained)"; encephalitis. | FIXED (plan F): epileptic seizures `low`; acute ischemic stroke `low` (wake-up onset raises an ACA stroke; reflexes, plantars, Hoover, no circumduction argue against); MS or cord lesion `low` on clinical grounds. Neuropathy and encephalitis removed. |
| D | major | `ground_truth.key_clinical_evidence` | Template items with the "Interim composition decision" leak. | FIXED: four case-specific items. |
| B | major | `ground_truth.red_herrings` | "Family history of MS" absent (FH denies MS); epilepsy row generic; psychiatric and stressor rows generic. | FIXED: MS row deleted; the others name the case data (aunt with GTC epilepsy on levetiracetam; GAD, past depression, childhood abuse; work, relationship and friend's illness). |
| C | minor | `metadata.clinical_pearls[1]`, `[3]` | "A family history of epilepsy does not increase the patient's own risk..." is wrong (it modestly raises the prior); "eyes closed ... strongly suggests PNES" overstates a single feature. | FIXED: both pearls reworded. |
| C | minor | `ground_truth.avoided_actions[*]` | Generic rationales, `[Stone_2018]`. | FIXED (plan L): patient-specific, `[Espay_2018]` / `[Stone_2016]`; CT framed as a repeat of the normal ED scan. |
| D | minor | `fallback_tool_outputs.specialized_test`, `.advanced_imaging`, `.echo` | Empty discriminators and the "itself a harm" leak; echo without `echo_type`. | FIXED (plan G): null and removed from kinds; echo `TTE`. |
| B | minor | `metadata.difficulty_rationale` | Template ("supportive normal labs"; no labs). | FIXED. |
| - | check | perfect_agent / guards | perfect_agent `-v`: exam and video-EEG answered by the case's outputs, ok; case guards pass; `case_io.py check` shows no failure naming FND-S02. | - |

## Changes, in one paragraph a physician can read before re-reviewing

Clinically unchanged: a 34-year-old teacher with right leg weakness noticed on waking three weeks ago and shaking episodes every two to three days, a normal ED CT, an aunt with generalized epilepsy and a history of childhood abuse. The Hoover sign is now described correctly (weak voluntary hip extension against strong involuntary extension), and the sensory loss ends at the inguinal crease rather than splitting the trunk. The required work-up is the examination and a 24 h video-EEG that records one habitual event (75 s of generalized shaking with the eyes closed, answering questions) without ictal change. Four validated signs are counted; the sensory pattern is supportive only. MRI stays optional and is a non-contrast report. The drug check (optional) reports sertraline with ibuprofen and with hydroxyzine instead of a sertraline dose increase. Epilepsy, stroke and a structural lesion are low after the work-up. Musts: positive diagnosis, explanation, physiotherapy, psychological therapy with re-established psychiatric follow-up and trauma-informed care, and an event plan.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 3 (EEG routing) applies.
- New citation keys used: `[Stone_2016]`, `[Daum_2014]`, `[Avbersek_2010]`.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification
Checked: the log tables against the final file and `git diff`; every claimed FIXED item is present (criteria tiers, required arguments, stop rule, constraints, canonical literature and drug outputs, non-contrast MRI where stored, video-EEG report, exam report, musts, prohibitions, differential, key evidence, red herrings, avoided actions, nulled fallbacks and `fallback_tool_kinds`); medications on the list match the drug-check `proposed` string verbatim; no follow-ups remain; `accepted[0]`, ICD codes, `case_id` and `condition` unchanged; event counts and durations agree across exam, EEG, musts and key evidence; differential key features cite only required or recommended results; no FND banned strings. No reviewer notes exist for FND, so the notes table is correctly empty. Also found and fixed in all six: `metadata.revision_reason` still read "every instrumental test optional", which is false after this round, and `last_revised` was 2026-08-10; both set to the condition's round wording (as in the other FND cases) and 2026-10-24.

Found and fixed:
- E, minor, `patient.neurological_exam.motor`: em dash left in the rewritten string; replaced with a comma clause.
- E, minor, `metadata.clinical_pearls[1]`: British "favours" in new text in an American-spelling case; now "favors".

Checked and accepted: a maternal aunt is correctly called second-degree; the hydroxyzine adult maximum of 100 mg daily is correct; the inguinal sensory boundary is consistent across exam, report, key evidence and the SSEP rationale.

After the edits: `perfect_agent.py -v` passes, `case_io.py check` shows no failure naming the case, and the case guards pass.

## Condition audit

2026-10-24, FND condition auditor.

- `action-4-analyze-brain-mri.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-neuropsych-battery.expected_evidence`: was empty; set to the wording the other optional batteries use.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.

## Close-out (24 Oct 2026)

Andrea's FND ruling of 24 Oct 2026 and the close-out decisions (`plans/FND-decisions.md`). What changed and why:

- `action-5-analyze-eeg` (video-EEG) required -> optional, removed from the stop rule; rationale now says what the diagnosis rests on without the recording (ILAE 2013 levels).
- M-DX must, COMM must, red-herring interpretations and metadata no longer say the diagnosis rests on the video-EEG: they rest on the positive signs and the event semiology, with video-EEG confirmation where recorded (open question 8).
- Diagnosis synonyms scoped by phenotype (`diagnosis_synonyms.yaml` F44 entries; a label or code naming another presentation must not score): removed "functional movement disorder"; added "psychogenic nonepileptic seizures", "dissociative seizures", "nonepileptic seizures", "functional limb weakness", "functional motor disorder".
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FND-` passes, now including the discriminator guard.
