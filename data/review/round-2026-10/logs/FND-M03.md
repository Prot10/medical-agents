# FND-M03
Reviewer status: R1 none, R2 none (no notes file for FND) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case. The physician input for FND is the July 2026 tool guidance (plan 1.3), applied through the plan.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | blocker | `initial_tool_outputs.eeg` (plan J) | The stored EEG was the prior 30-minute routine outpatient EEG with no events (already reported in the HPI), although he was admitted for continuous video-EEG and the criterion orders `eeg_type: video`; its limitations recommended video-EEG. | FIXED: replaced by a 48-hour inpatient video-EEG recording two habitual events (times, durations, semiology from the HPI and exam) without ictal change and without post-event focal slowing after the event followed by right arm weakness; canonical impression. The routine EEG stays in the HPI as history. |
| B | minor | `patient.history_present_illness` | Opening said "three witnessed episodes" while the HPI then describes at least seven; "He notes that ... though he has not explicitly recognized this pattern" contradicts itself. | FIXED: "recurrent witnessed episodes of shaking"; "His wife has noticed that his symptoms worsen...". |
| C | major | `initial_tool_outputs.clinical_assessment` (plan H) | Meta keys; equivocal Hoover sign counted among 5 "signs"; midline splitting counted twice; key leak in the impression. | FIXED: canonical shape; Hoover reported equivocal and not counted (`hoover_sign_positive: false`); 3 validated signs (collapsing weakness, entrainment of the event movements, distractibility); hemisensory midline split, gait and coordination as supportive; observed event; event-based impression. |
| B | major | `initial_tool_outputs.labs` (plan K) | Hct 42.3 against MCV x RBC 37.7; female Hb/Hct reference ranges for a man; summary with interpretation. | FIXED: RBC 5.18 (42.3 / 81.7 x 10; MCHC 33.3), male ranges (Hb 13.5-17.5, Hct 41-53, RBC 4.5-5.9); Na 132 kept (plan K) and named as an SSRI caution in the drug output; plain summary. |
| B | major | `initial_tool_outputs.mri` (plan I) | "without and with gadolinium"; no findings block. | FIXED: non-contrast report with T1, T2/FLAIR, DWI, SWI findings, symmetric hippocampi; impression names no infarct, hemorrhage, mass, cortical or white matter lesion. |
| C | major | `initial_tool_outputs.drug_interactions` (plan C) | Medicine list only with the "prescribing decision" leak; escitalopram + sumatriptan not identified. | FIXED: escitalopram + sumatriptan (serotonergic, rare), escitalopram 20 mg QT and hyponatremia cautions, dicyclomine anticholinergic effects. |
| D | major | `followup_outputs[0]` (plan B) | Literature follow-up misattributing Hallett 2022 ("new subtypes and shared mechanisms") to Espay 2018; misstated ILAE levels. | FIXED: deleted; canonical `initial_tool_outputs.literature_search`. |
| A | major | `ground_truth.action_criteria` (plan A, 3.2) | Template tiers; video-EEG optional though admitted for it; MRI optional though a post-event deficit with word-finding difficulty and an MRI ordered but not done. | FIXED: exam required, MRI recommended (`{contrast: false}`, any protocol), video-EEG required, drug check optional, labs optional, optional neuropsychology, literature optional last. Soft constraint exam before MRI; stop rule exam + video-EEG. |
| C | major | `ground_truth.assessment` (plan D) | Template musts and prohibitions ("Stone 2018", duplicates, mis-tiered neuropsychology, video-EEG as a must). | FIXED: DX, COMM, PHYSIO, PSY (anxiety, trauma-informed), RESCUE; prohibitions P1, P2, P3, P5, P6, P7. |
| C | major | `ground_truth.differential` (plan F) | Epileptic seizures `moderate`; template structural, neuropathy, autoimmune encephalitis and malingering rows; no postictal paresis although the case raises it. | FIXED: epileptic seizures `low`; new "Postictal (Todd) paresis" `low` (no ictal change, no post-event slowing, collapsing weakness); "Structural lesion of the left hemisphere" `low` citing the recommended MRI; template rows deleted. |
| D | major | `ground_truth.key_clinical_evidence` (plan E) | Template items with leaks. | FIXED: five case-specific items. |
| B | minor | `ground_truth.red_herrings` | Generic data points; stressor field path. | FIXED: maternal aunt with epilepsy (real, kept), anxiety and depression, marital conflict (`social_history.psychosocial`); added the normal routine EEG as a red herring (pack 7, "normal initial workup"). |
| C | minor | `ground_truth.avoided_actions` (plan L) | `[Stone_2018]`; generic rationales; CT rationale ignored the normal urgent-care CT. | FIXED: patient-specific rationales, `[Espay_2018]` / `[Stone_2016]`. |
| E | minor | `metadata.difficulty_rationale`, `revision_reason` | Template text. | FIXED: case-specific; `last_revised` 2026-10-24. |
| A | minor | `fallback_tool_outputs` (plan G) | `specialized_test`, `advanced_imaging`, `drug_interactions` template fallbacks; echo without `echo_type`. | FIXED: three nulled and removed from `fallback_tool_kinds`; echo `echo_type: TTE`. |

## Changes, in one paragraph a physician can read before re-reviewing

The case now stores the inpatient video-EEG he was admitted for (48 hours, two habitual events with forced eye closure and preserved responsiveness, no ictal change, no slowing after the event followed by right arm weakness) instead of the earlier routine EEG, which remains in the history. The policy requires the examination and the video-EEG and recommends one non-contrast brain MRI after the examination, because events followed by right arm weakness and word-finding difficulty raise a left hemisphere lesion or Todd paresis; the MRI is normal on T1, FLAIR, DWI and SWI. Labs, the drug review (escitalopram with sumatriptan), neuropsychology and literature are optional. The structured examination reports the Hoover sign as equivocal and does not count it; it counts collapsing weakness, entrainment of the event movements and distractibility. The CBC is consistent and uses male ranges. Musts: positive diagnosis, explanation, physiotherapy, trauma-informed psychological therapy with treatment of anxiety, and an event plan; prohibitions are the canonical set. Epileptic seizures, Todd paresis and a structural left hemisphere lesion are all `low`.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- EEG routing (plan 5.3), concrete here: an `eeg_type: routine` order is now served this video-EEG with its events, although the HPI says the routine EEG recorded none. An `eeg_type` discriminator, or a routine interictal normal report for this case, is needed.
- New citation keys used: `[Daum_2014]`, `[Stone_2016]` (plan 5.1).

## Open questions for Andrea (judgment calls you could not settle)

None. The recommended MRI criterion takes `{contrast: false}` without a protocol, so an epilepsy or stroke protocol order also counts (plan 3.2 names only the contrast argument).

## Verification
Checked the log against the file (worker edits are in commit b8be2153; diffed against its parent): read the whole final case, the patient-block diff, criteria tiers and order against plan 3.2 and the case entry in plan 4, sequence constraints and stop rule, musts and prohibitions against avoided actions, differential against the returned results, lab arithmetic and ranges, laterality, leak guard. No reviewer notes exist for FND, so there is no note id to account for. perfect_agent.py -v, case_io.py check and test_case_guards pass after my changes.
The stored EEG is now the inpatient video-EEG with two events and no post-event slowing; the routine EEG stays in the HPI. Hoover is equivocal and not counted (3 signs remain); RBC 5.18 x 81.7 / 10 = 42.3, MCHC 33.3, male ranges; exam before MRI constraint correct; Todd paresis added low.
Found and fixed:
- (C, minor) `ground_truth.differential[0].key_features` did not address the case's own epileptic red flag: the prodrome of a rising chest sensation with fear resembles a mesial temporal aura. Added: in both recorded events it was followed by bilateral asynchronous shaking with forced eye closure and preserved responsiveness without ictal change, which argues against a focal seizure with bilateral motor spread.
- (B, minor) `initial_tool_outputs.labs.panels.Other[0]` prolactin reference range 3.0-27.0 is a female range in a man; now 2.0-18.0 (value 13.2 stays normal).

## Condition audit

2026-10-24, FND condition auditor.

- `action-2-check-drug-interactions.label`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-6-interpret-labs.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-6-interpret-labs.label`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-neuropsych-battery.label`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-1-search-medical-literature.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.

## Close-out (24 Oct 2026)

Andrea's FND ruling of 24 Oct 2026 and the close-out decisions (`plans/FND-decisions.md`). What changed and why:

- `action-5-analyze-eeg` (video-EEG) required -> optional, removed from the stop rule; rationale now says what the diagnosis rests on without the recording (ILAE 2013 levels).
- M-DX must, COMM must, red-herring interpretations and metadata no longer say the diagnosis rests on the video-EEG: they rest on the positive signs and the event semiology, with video-EEG confirmation where recorded (open question 8).
- Diagnosis synonyms scoped by phenotype (`diagnosis_synonyms.yaml` F44 entries; a label or code naming another presentation must not score): added "psychogenic nonepileptic seizures", "dissociative seizures", "nonepileptic seizures", "functional limb weakness", "functional motor disorder", "functional tremor".
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FND-` passes, now including the discriminator guard.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `video`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- metadata.revision_reason: "October 2026 review round: brain MRI recommended for the post-event deficit; criteria, outputs and assessment rebuilt to the FND criteria pack tiers. Close-out 24 Oct 2026: video-EEG optional and red-flag tests recommended, per the July 2026 agreement with the physicians that the examination is the only required diagnostic act." -> "October 2026 review round: brain MRI recommended for the post-event deficit; criteria, outputs and assessment rebuilt to the FND required, recommended and optional tiers. Close-out 24 Oct 2026: video-EEG optional and red-flag tests recommended, per the July 2026 agreement with the physicians that the examination is the only required diagnostic act."
