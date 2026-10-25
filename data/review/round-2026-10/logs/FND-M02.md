# FND-M02
Reviewer status: R1 none, R2 none (no notes file for FND) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case. The physician input for FND is the July 2026 tool guidance (plan 1.3), applied through the plan.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.clinical_history.medications` | HPI says levetiracetam 500 mg twice daily was started four weeks ago and the labs report a level, but the medication list omits it. | FIXED: levetiracetam 500 mg twice daily added (indication: presumed new-onset seizures, outside ED). |
| D | minor | `patient.history_present_illness` | "a prior episode of non-epileptic events at age 19" names the diagnostic category in the history. | FIXED: "a similar period of shaking episodes that resolved spontaneously without treatment". |
| B | major | `patient.neurological_exam.motor` | The right hand tremor of the chief complaint was never examined, so no tremor sign could be counted (plan names entrainment for M02). | FIXED: tremor examined: variable coarse right hand tremor that entrains to left-hand tapping and pauses during ballistic left-hand movements. |
| C | major | `initial_tool_outputs.clinical_assessment` (plan H) | Meta keys in `criteria_met`; 7 "signs" including low-specificity ones (midline splitting, distracted proprioception, variable resistance); fragment findings; key leak "No further investigation is required...". | FIXED: canonical shape; 5 validated signs (bilateral Hoover, collapsing weakness, tremor entrainment, distractibility, convergence spasm with miosis); supportive features listed and not counted; observed event recorded; event-based impression. |
| B | minor | `initial_tool_outputs.eeg` (plan J) | Events narrated inside the impression, `findings` empty, no "This is a NORMAL" opening; event 1 time 14:32 copied from M01. | FIXED: two event findings with times and durations (event 1 now 15:47), canonical impression. |
| E | minor | `initial_tool_outputs.labs` | Abnormal summary carried interpretation ("consistent with hyponatremia") and dashes. | FIXED: plain value list; interpretation names the two low values. Na 132 kept (plausible on sertraline, plan K) and named as an SSRI caution in the drug output. |
| B | major | `initial_tool_outputs.mri` (plan I) | Report "without and with gadolinium", "no abnormal enhancement", criterion `contrast: false`. | FIXED: non-contrast impression; enhancement statement removed. |
| C | major | `initial_tool_outputs.drug_interactions` (plan C) | Medicine list only, with the "prescribing decision" leak; levetiracetam missing; no serotonergic, bleeding or sedation interaction. | FIXED: sertraline + cyclobenzaprine (serotonergic), sertraline + ibuprofen (GI bleeding), additive sedation with lorazepam, cyclobenzaprine and levetiracetam; warnings for levetiracetam (mood, gradual withdrawal), lorazepam, SSRI hyponatremia. |
| C | blocker | `followup_outputs[0]` (plan B) | Literature follow-up with fabricated "NNT 5.7" in "JAMA Psychiatry", CODES said to reduce seizure frequency, Hallett 2022 attributed to "Espay 2018". | FIXED: deleted; one canonical `initial_tool_outputs.literature_search`. |
| A | major | `ground_truth.action_criteria` (plan A, 3.2) | Template tiers and labels; video-EEG optional although the events are the reason for admission; drug check not required although an antiseizure drug was started for the events. | FIXED: exam required, video-EEG required, drug check required, labs and MRI optional (MRI `{contrast: false}`, any protocol), new optional neuropsychology, literature optional and last. Soft constraint video-EEG before drug check; stop rule exam, video-EEG, drug check. |
| C | major | `ground_truth.assessment` (plan D) | Template musts (duplicates, mis-tiered neuropsychology, video-EEG as a must, no levetiracetam taper); prohibitions with "Stone 2018" and "start or continue" antiseizure drugs. | FIXED: DX, COMM, PSY (anxiety, trauma-informed), PHYSIO, ASM (taper and stop levetiracetam), RESCUE; prohibitions P1, P2, P3, P5 with "or stop it abruptly", P6, P7. |
| C | major | `ground_truth.differential` (plan F) | Epileptic seizures `moderate` after the video-EEG; MS and structural lesion resting on "excludes" by an optional MRI; neuropathy, autoimmune encephalitis and malingering template rows. | FIXED: epileptic seizures `low` (canonical plus semiology and no response to levetiracetam); structural brain or cord lesion `low` on examination grounds; new "Drug-induced tremor or serotonin toxicity" `low` (the drug output raises it); MS, neuropathy, autoimmune encephalitis, malingering deleted. |
| D | major | `ground_truth.key_clinical_evidence` (plan E) | Template items with the "Interim composition decision" leak, the OPTIONAL item and Stone 2018 claims. | FIXED: six case-specific items. |
| B | minor | `ground_truth.red_herrings` | Generic data points; stressor field path on the HPI although the stressor is in social history. | FIXED: grandmother with epilepsy (kept: it is in the FH), anxiety and depression, the separation (`social_history.stressors`); added the levetiracetam started on presumption. |
| C | minor | `ground_truth.avoided_actions` (plan L) | `[Stone_2018]` citations; generic rationales; CT rationale ignored the normal outside CT. | FIXED: patient-specific rationales, CT as a repeat of the normal outside CT (`[Stone_2016]`). |
| C | minor | `metadata.clinical_pearls` | "Up to 10-20% of patients referred to epilepsy monitoring units" understates the usual 20-40%; "making psychiatric evaluation essential" framed comorbidity as diagnostic. | FIXED: 20-40% of EMU admissions; comorbidity as a treatment target. |
| E | minor | `metadata.difficulty_rationale`, `revision_reason` | Template ("comorbid SLE", "MRI + basic labs"). | FIXED: case-specific; `last_revised` 2026-10-24. |
| A | minor | `fallback_tool_outputs` (plan G) | `specialized_test` (empty `test_type`, "itself a harm"), `advanced_imaging` (`MRI_brain_functional`), drug fallback "(agent not specified...)"; echo without `echo_type`. | FIXED: three nulled and removed from `fallback_tool_kinds`; echo `echo_type: TTE`. |

## Changes, in one paragraph a physician can read before re-reviewing

Levetiracetam, started at an outside ED for presumed seizures, is now on the medication list, and the work-up asks for the examination, a video-EEG and a medicine review before the taper (all required; review after the recording, soft constraint). Labs, a non-contrast brain MRI, neuropsychology and literature are optional. The HPI no longer labels her adolescent episodes "non-epileptic". The exam now documents the right hand tremor she complains of (entrains to left-hand tapping), and the structured examination counts five validated signs (bilateral Hoover, collapsing weakness, entrainment, distractibility, convergence spasm with miosis) with the observed event; low-specificity signs are listed as supportive. The video-EEG lists its two events without ictal change in findings, with a canonical impression; the MRI is non-contrast. The drug review now finds the sertraline-cyclobenzaprine serotonergic risk, sertraline-ibuprofen bleeding risk, additive sedation and SSRI hyponatremia. The fabricated CODES "NNT 5.7" literature follow-up is gone. Musts: positive diagnosis, explanation, psychological therapy (trauma-informed), functional-motor physiotherapy, taper and stop levetiracetam, event plan; prohibitions add "or stop it abruptly". Epileptic seizures are `low`; a drug-induced tremor or serotonin toxicity entry was added as `low`.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used per plan 1.1: `[Daum_2014]`, `[Stone_2016]`, `[Oto_2005]` (plan 5.1).
- Library `functional_neuro_signs` report: add `convergence_spasm_with_miosis` (plan 5.7); this case stores it.
- EEG routing (plan 5.3): a `routine` EEG order would be served this video-EEG with its events.

## Open questions for Andrea (judgment calls you could not settle)

None. The tremor examination was added because the chief complaint names the tremor and the plan counts entrainment for this case; the new sentence adds no new symptom.

## Verification
Checked the log against the file (worker edits are in commit b8be2153; diffed against its parent): read the whole final case, the patient-block diff, criteria tiers and order against plan 3.2 and the case entry in plan 4, sequence constraints and stop rule, musts and prohibitions against avoided actions, differential against the returned results, lab arithmetic and ranges, laterality, leak guard. No reviewer notes exist for FND, so there is no note id to account for. perfect_agent.py -v, case_io.py check and test_case_guards pass after my changes.
Levetiracetam is now on the medication list and in the drug output; the soft constraint video-EEG before drug check has the right direction; P5 carries "or stop it abruptly"; the drug output names the serotonergic, bleeding and sedation pairs and the SSRI hyponatremia that explains Na 132; Hb 12.6 / Hct 38.8 gives MCHC 32.5.
Found and fixed (E, minor): `patient.neurological_exam.additional` read "Bilateral arms could be gently repositioned and showed resistance to eye opening" (arms cannot resist eye opening). Now: "Her arms could be gently repositioned, and she resisted passive eye opening." Same fact, corrected grammar.

## Condition audit

2026-10-24, FND condition auditor.

- `action-6-interpret-labs.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-6-interpret-labs.label`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-4-analyze-brain-mri.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-4-analyze-brain-mri.label`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-neuropsych-battery.label`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-1-search-medical-literature.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.

## Close-out (24 Oct 2026)

Andrea's FND ruling of 24 Oct 2026 and the close-out decisions (`plans/FND-decisions.md`). What changed and why:

- `action-5-analyze-eeg` (video-EEG) required -> optional, removed from the stop rule; 1 soft constraint(s) naming it removed; rationale now says what the diagnosis rests on without the recording (ILAE 2013 levels).
- M-DX must, COMM must, red-herring interpretations and metadata no longer say the diagnosis rests on the video-EEG: they rest on the positive signs and the event semiology, with video-EEG confirmation where recorded (open question 8).
- M-ASM taper must now conditions the taper on a secure diagnosis, ideally documented on video-EEG.
- ECG avoided action `avoid-waste-1-analyze-ecg` (waste) replaced by an optional `action-ecg` criterion: the events are apparent unresponsiveness and NICE CG109 / NG217 advise a 12-lead ECG (open question 4).
- Drug-check rationale: the taper follows a secure diagnosis, not "once the events are recorded".
- Diagnosis synonyms scoped by phenotype (`diagnosis_synonyms.yaml` F44 entries; a label or code naming another presentation must not score): added "psychogenic nonepileptic seizures", "dissociative seizures", "nonepileptic seizures", "functional limb weakness", "functional motor disorder", "functional tremor".
- The medicine review stays required as a management act (ruling); listed for the physicians in `plans/FND-decisions.md`.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FND-` passes, now including the discriminator guard.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `video`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- metadata.revision_reason: "October 2026 review round: the medicine review before the levetiracetam taper required; criteria, outputs and assessment rebuilt to the FND criteria pack tiers. Close-out 24 Oct 2026: video-EEG optional and red-flag tests recommended, per the July 2026 agreement with the physicians that the examination is the only required diagnostic act." -> "October 2026 review round: the medicine review before the levetiracetam taper required; criteria, outputs and assessment rebuilt to the FND required, recommended and optional tiers. Close-out 24 Oct 2026: video-EEG optional and red-flag tests recommended, per the July 2026 agreement with the physicians that the examination is the only required diagnostic act."
