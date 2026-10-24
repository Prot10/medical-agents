# FND-M04
Reviewer status: R1 none, R2 none (no notes file for FND) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case. The physician input for FND is the July 2026 tool guidance (plan 1.3), applied through the plan.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `initial_tool_outputs.eeg` (plan J) | Thin report: no activating procedures although events follow bright light and absences are the mimic; impression in capitals ("NO EEG CHANGE"), event without time; em dashes. | FIXED: 24-hour video-EEG with hyperventilation (two trials), photic stimulation 1-30 Hz and eye closure, all without discharges or events; the 32-second habitual event (kept) with time, semiology and no generalized spike-and-wave; canonical impression. |
| C | major | `initial_tool_outputs.clinical_assessment` (plan H) | Meta keys; "findings" were history items (duration, denial of incontinence) presented as signs; impression said "video-EEG is required in this case rather than optional" (policy leak). | FIXED: canonical shape; normal motor and sensory examination; observed event recorded (`functional_seizure_semiology_observed: true`); no-sign impression adapted to the observed event (exam text describes an event, plan H). |
| C | major | `initial_tool_outputs.drug_interactions` (plan C) | Medicine list only, with the "prescribing decision" leak; escitalopram + sumatriptan not named. | FIXED: escitalopram + sumatriptan (serotonergic, rare), escitalopram cautions. |
| D | major | `followup_outputs[0]` `patient_education_fnd_pnes` (plan B, ruling 4) | Patient education disguised as a literature search, with an empty summary and a reused PMID (26276867). | FIXED: deleted; the education content is M-COMM; canonical `initial_tool_outputs.literature_search`. |
| A | major | `ground_truth.action_criteria` (plan A, 3.2) | Video-EEG optional in a purely paroxysmal case; literature and drug check recommended; template labels and citations. | FIXED: exam required (citations Avbersek 2010, AAN 2025), video-EEG required with an activation-specific expected evidence, drug check optional, optional neuropsychology, literature optional last; stop rule exam + video-EEG. |
| C | major | `ground_truth.assessment` (plan D) | Template musts including physiotherapy for a patient with no motor symptom, the semiology must and the video-EEG must; template prohibitions. | FIXED: DX (recorded event with normal activation), COMM, PSY (anxiety, fear of epilepsy), RESCUE; prohibitions P1, P2, P3, P5, P6, P7. No PHYSIO (no motor phenotype). |
| C | major | `ground_truth.differential` (plan F) | Epileptic seizures `moderate`; MS, structural lesion, autoimmune encephalitis and malingering template rows with no basis in the case; the actual mimic (absence epilepsy, eyelid myoclonia) absent. | FIXED: epileptic seizures `low`; new "Absence epilepsy or eyelid myoclonia" `low` citing the recorded event and normal activation; template rows deleted. |
| D | major | `ground_truth.key_clinical_evidence` (plan E) | Template items with leaks; limb-sign items in a case with no limb sign. | FIXED: five case-specific items. |
| B | minor | `ground_truth.red_herrings` | Generic data points; stressor field path. | FIXED: febrile convulsions and the aunt with epilepsy (real, kept per plan), anxiety, the stressors (`social_history.recent_stressor`); added the light-triggered events. |
| C | minor | `ground_truth.avoided_actions` (plan L) | `[Stone_2018]`; generic rationales. | FIXED: patient-specific rationales, `[Espay_2018]` / `[Stone_2016]`. |
| C | minor | `fallback_tool_outputs.ct` | Off-pathway CT reported a 3 mm right frontal calcified granuloma: a potentially epileptogenic lesion in a woman whose events include head turning, i.e. a mimic created by an unscored report that no part of the policy handles; it also claimed "no enhancement" on a non-contrast CT. | FIXED: normal CT fallback; `fallback_tool_kinds.ct` "normal". |
| E | minor | `metadata.difficulty_rationale`, `revision_reason` | Template text ("family history of MS, antipsychotic exposure, comorbid SLE"). | FIXED: case-specific; `last_revised` 2026-10-24. |
| A | minor | `fallback_tool_outputs` (plan G) | `specialized_test`, `advanced_imaging`, `drug_interactions` template fallbacks; echo without `echo_type`. | FIXED: three nulled and removed from `fallback_tool_kinds`; echo `echo_type: TTE` (its named finding, trace physiological mitral regurgitation, kept). |

## Changes, in one paragraph a physician can read before re-reviewing

This is a purely paroxysmal case (eyelid flutter with brief unresponsiveness, some after bright light), so the policy requires the examination and a video-EEG and leaves the drug review, neuropsychology and literature optional; there is no MRI or lab criterion. The video-EEG now reads as a full report: 24 hours, hyperventilation twice, photic stimulation and eye closure without discharges, and the 32-second habitual event without generalized spike-and-wave or other ictal change. The structured examination reports a normal motor and sensory examination and the observed event, without claiming a limb sign. The patient-education "literature" follow-up is gone. Musts: positive diagnosis on the recorded event, explanation, psychological therapy for anxiety and her fear of epilepsy, and an event plan; no physiotherapy, since she has no motor symptom. The differential keeps epileptic seizures `low` and adds absence epilepsy or eyelid myoclonia `low`; febrile convulsions, the aunt with epilepsy and light-triggered events are red herrings. The off-pathway CT no longer shows a frontal calcified granuloma.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used: `[Avbersek_2010]`, `[Stone_2016]` (plan 5.1).
- EEG routing (plan 5.3): a `routine` EEG order would be served this video-EEG with its event.

## Open questions for Andrea (judgment calls you could not settle)

None. `metadata.notes` (an authoring note from generation) was left as it is.

## Verification
Checked the log against the file (worker edits are in commit b8be2153; diffed against its parent): read the whole final case, the patient-block diff, criteria tiers and order against plan 3.2 and the case entry in plan 4, sequence constraints and stop rule, musts and prohibitions against avoided actions, differential against the returned results, lab arithmetic and ranges, laterality, leak guard. No reviewer notes exist for FND, so there is no note id to account for. perfect_agent.py -v, case_io.py check and test_case_guards pass after my changes.
Purely paroxysmal case with no limb sign: the structured exam counts 0 signs, the EEG carries hyperventilation, photic stimulation and eye closure, no PHYSIO must, no MRI or lab criterion, absence epilepsy or eyelid myoclonia added low. The CT fallback granuloma removal is justified (an unscored epileptogenic lesion).
Found and fixed:
- (C, minor) M-COMM (`ground_truth.assessment.required_recommendations[1]`) said "show the positive signs", but this patient has none. Now "show how the recorded event and the normal EEG support it".
- (B, minor) `ground_truth.red_herrings[1].correct_interpretation` said "Diagnosis requires positive rule-in signs on examination", contradicting the case (diagnosis rests on the recorded event). Now: "The diagnosis rests on the habitual event recorded on video-EEG without ictal change; the anxiety is a treatment target."
Left as is: `red_herrings[0]` combines the febrile convulsions (past medical history) and the aunt (family history) under the family-history field path; the schema allows one path, and the content is correct.
