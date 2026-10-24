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
