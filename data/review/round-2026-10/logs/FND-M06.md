# FND-M06
Reviewer status: R1 none, R2 none (no notes file for FND) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case. The physician input for FND is the July 2026 tool guidance (plan 1.3), applied through the plan.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | Editorial clause "(which is treatable and would support his disability claim) rather than to a functional cause" names the answer; "He has not had any prior PNES episodes" names the diagnosis. | FIXED: "He has applied for disability benefits and is desperate for an explanation of the episodes."; "He has had no episodes of this kind before." Facts kept (plan M06). |
| C | major | `initial_tool_outputs.clinical_assessment` (plan H) | Meta keys; the single "finding" was the HPI sentence; impression stated that video-EEG "is required in this case rather than optional" (policy leak). | FIXED: canonical shape; normal interictal examination; reported semiology of the new events from the witness account versus his documented seizures; no event was seen by the examiner (`functional_seizure_semiology_observed: false`); event-based impression worded for reported semiology. |
| B | major | `initial_tool_outputs.eeg` (plan J) | Background note "consistent with right MTS substrate" (cross-modality); interictal discharges only in the impression; event without time; impression not in the ABNORMAL format; em dashes. | FIXED: 48-hour video-EEG; right anterior temporal sharp-and-slow-wave discharges and right temporal theta as findings; the 3 min 12 s new-type event with time, no ictal change, no post-event slowing, persistent PDR; canonical "This is an ABNORMAL video-EEG due to: ..." impression. |
| B | minor | `initial_tool_outputs.labs` (plan K) | TSH and B12 "Within reference range" without units, with the template `clinical_significance`; summary with interpretation ("diabetic baseline"); "Prolactin (post-new-episode)" without timing. | FIXED: TSH 2.4 mIU/L and B12 438 pg/mL; all values kept; panels regrouped; prolactin labelled 20 minutes after a new-type event; plain summary and interpretation. |
| C | major | `followup_outputs[0]` `levetiracetam_mood_effects` (plan C) | A plan, not a check: "Consider adding SSRI for depression" (he has no depression), lamotrigine switch as an alternative; no initial drug output. | FIXED: deleted; new initial output (metformin + empagliflozin, levetiracetam with no interaction; levetiracetam mood effects and no abrupt withdrawal in established epilepsy; weekend binge drinking caution). |
| D | major | `followup_outputs[1]` `mixed_epilepsy_pnes_literature` (plan B) | Empty literature stub with a reused PMID (26276867). | FIXED: deleted; canonical `initial_tool_outputs.literature_search`. |
| A | major | `ground_truth.action_criteria` (plan 3.2) | Video-EEG optional in a dual-diagnosis case where only a recording separates recurrence from functional events; labs criterion (`AED_levels`) already answered in the HPI (level therapeutic); literature recommended. | FIXED: exam required, video-EEG required, drug check recommended, labs criterion deleted, optional neuropsychology, literature optional last; stop rule exam + video-EEG. |
| C | major | `ground_truth.assessment` (plan D) | Template musts (physiotherapy for a non-motor case, neuropsychology, video-EEG as a must); the prohibition "Do not start or continue long-term anti-epileptic drugs" contradicts his established epilepsy; no driving advice. | FIXED: DX (coexisting with epilepsy), EPI (continue levetiracetam, do not escalate), COMM, PSY, RESCUE (M06 variant), COMORB (commercial driving); prohibitions P1, P2, P3, P5 and P6 in the M06 wording, P7, and "Stop or taper levetiracetam because the new events are functional". |
| C | major | `ground_truth.differential` (plan F) | Epileptic seizures `high` after the recording; malingering `very_low` resting on an unperformed symptom-validity test; template structural and autoimmune rows; frontal hypermotor seizures (the classic scalp-EEG-negative mimic) absent. | FIXED: "Recurrence of known right TLE (new seizure type)" `low`; "Frontal lobe (hypermotor) seizures" `low` (duration, wakefulness, eyes closed, persistent PDR); malingering `low` with the disability claim named; template rows deleted. |
| D | major | `ground_truth.key_clinical_evidence` (plan E) | Template items with leaks and limb-sign claims. | FIXED: five case-specific items. |
| B | minor | `ground_truth.red_herrings` | Generic data points; stressor field path. | FIXED: father with epilepsy (real), the licence and disability claim (`social_history.recent_stressor`, both the stress and the feigning trap), and the established epilepsy with interictal discharges (plan E keeps it). |
| C | minor | `ground_truth.avoided_actions` (plan L) | `[Stone_2018]`; generic rationales. | FIXED: patient-specific rationales, `[Espay_2018]` / `[Stone_2016]`. |
| B | major | `fallback_tool_outputs.mri` | No case MRI, so a brain MRI order was answered by the library normal report, contradicting his known right mesial temporal sclerosis. | FIXED: case fallback MRI with stable right MTS (unchanged from 3 years ago, no new lesion); `fallback_tool_kinds.mri` "case". |
| C | minor | `fallback_tool_outputs.ct` | Template right frontal calcified granuloma (identical to M04) with "no enhancement" on a non-contrast CT: a second potential epileptogenic lesion invented in a man with right temporal epilepsy. | FIXED: normal CT fallback; kind "normal". |
| E | minor | `metadata.difficulty_rationale`, `revision_reason` | Template text. | FIXED: case-specific; `last_revised` 2026-10-24. |
| A | minor | `fallback_tool_outputs` (plan G) | `specialized_test`, `advanced_imaging` template fallbacks; echo without `echo_type`. | FIXED: nulled and removed from `fallback_tool_kinds`; echo `echo_type: TTE`. |

## Changes, in one paragraph a physician can read before re-reviewing

This is a dual-diagnosis case: established right temporal lobe epilepsy with mesial temporal sclerosis, seizure-free on levetiracetam, and new events with eyes closed, back arching, 2-5 minutes and rapid recovery. The policy requires the examination and a video-EEG and recommends the medicine review; the labs criterion (already answered by the therapeutic level in the history), neuropsychology and literature are gone or optional. The HPI no longer says he wants epilepsy "rather than a functional cause". The video-EEG is now an abnormal report with right anterior temporal sharp-and-slow-wave discharges and theta, and one new-type event recorded without ictal change or post-event slowing. The structured examination documents a normal interictal examination and the reported semiology, without claiming an observed event. The drug review no longer proposes an SSRI or lamotrigine; it warns about levetiracetam mood effects and abrupt withdrawal. Musts: dual diagnosis, continue levetiracetam without escalation, explanation, psychological therapy, an event plan with rescue only for his known seizure type, and commercial driving advice; prohibitions include stopping levetiracetam and escalating antiseizure drugs for the new events. Recurrence of his TLE, frontal hypermotor seizures and malingering (disability claim) are all `low`. An off-pathway brain MRI now shows his known MTS instead of a library normal.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used: `[Avbersek_2010]`, `[Kutlubaev_2018]`, `[Stone_2016]` (plan 5.1).
- EEG routing (plan 5.3): a `routine` EEG order would be served this video-EEG with its event.

## Open questions for Andrea (judgment calls you could not settle)

None. M-PSY reads "assess and treat any comorbid anxiety or depression" because the case documents distress but no named psychiatric diagnosis. The added prohibition on stopping levetiracetam mirrors M-EPI and closes the obvious wrong turn after a functional diagnosis.

## Verification
Checked the log against the file (worker edits are in commit b8be2153; diffed against its parent): read the whole final case, the patient-block diff, criteria tiers and order against plan 3.2 and the case entry in plan 4, sequence constraints and stop rule, musts and prohibitions against avoided actions, differential against the returned results, lab arithmetic and ranges, laterality, leak guard. No reviewer notes exist for FND, so there is no note id to account for. perfect_agent.py -v, case_io.py check and test_case_guards pass after my changes.
Dual diagnosis handled consistently: M-EPI, the M06 wording of P5, P6 and M-RESCUE, the added prohibition of stopping levetiracetam, the abnormal EEG with the new-type event without ictal change, the case MRI fallback showing the known right MTS, malingering low with the disability claim named. The removal of the labs criterion matches the plan (level already in the HPI).
Found and fixed (C, minor): M-COMM (`ground_truth.assessment.required_recommendations[2]`) said "show the positive signs", but he has no functional sign and no event was observed at the bedside. Now "explain how the recorded new event differs from his epileptic seizures".

## Condition audit

2026-10-24, FND condition auditor.

- `action-neuropsych-battery.label`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-1-search-medical-literature.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.

## Close-out (24 Oct 2026)

Andrea's FND ruling of 24 Oct 2026 and the close-out decisions (`plans/FND-decisions.md`). What changed and why:

- `action-4-analyze-eeg` (video-EEG) required -> optional, removed from the stop rule; rationale now says what the diagnosis rests on without the recording (ILAE 2013 levels).
- M-DX must, COMM must, red-herring interpretations and metadata no longer say the diagnosis rests on the video-EEG: they rest on the positive signs and the event semiology, with video-EEG confirmation where recorded (open question 8).
- Diagnosis synonyms scoped by phenotype (`diagnosis_synonyms.yaml` F44 entries; a label or code naming another presentation must not score): removed "non-epileptic seizures", "functional movement disorder", "functional weakness"; added "nonepileptic seizures"; codes removed F44.4, F44.7, F44.6.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FND-` passes, now including the discriminator guard.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `video`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- metadata.revision_reason: "October 2026 review round: criteria, outputs and assessment rebuilt to the FND criteria pack tiers with the dual-diagnosis variants. Close-out 24 Oct 2026: video-EEG optional and red-flag tests recommended, per the July 2026 agreement with the physicians that the examination is the only required diagnostic act." -> "October 2026 review round: criteria, outputs and assessment rebuilt to the FND required, recommended and optional tiers with the dual-diagnosis variants. Close-out 24 Oct 2026: video-EEG optional and red-flag tests recommended, per the July 2026 agreement with the physicians that the examination is the only required diagnostic act."

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 90 -> 94.9 kg, height 175 -> 175 cm, BMI 29.4 -> 31 (the prompt shows height, weight and BMI).
- Why: rule 3: past history 'Obesity' with stored BMI 29.4; BMI raised to 31.0 at the default height.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although the case contradicts it now get a case-specific report (library answers stay for everything else).

- `analyze_eeg eeg_type=routine (and sleep_deprived, served by the routine report)` -> `fallback_tool_outputs.eeg`: abnormal routine EEG: occasional right anterior temporal sharp-and-slow waves and intermittent right temporal theta. Why: the stored video-EEG shows about 6 right anterior temporal discharges per hour, awake and asleep, unchanged from the prior study; the library reports a normal routine EEG.
- `analyze_eeg eeg_type=ambulatory` -> `followup_outputs[request_ambulatory]`: abnormal 48-hour ambulatory EEG: intermittent right anterior temporal discharges and slowing. Why: the stored video-EEG shows frequent right temporal interictal discharges; the library reports a normal ambulatory EEG.

Checks: `perfect_agent.py` pass; `test_case_guards.py -k FND-M06` pass; map verify (map_FND) problems 0; criterion-answer snapshot unchanged.
