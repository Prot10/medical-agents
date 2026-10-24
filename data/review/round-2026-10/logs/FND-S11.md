# FND-S11
Reviewer status: R1 not reviewed, R2 not reviewed (no FND notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.neurological_exam.motor`, `initial_tool_outputs.clinical_assessment` | "POSITIVE Hoover sign bilaterally" for a patient whose weakness is in the hands: the Hoover sign tests hip extension and cannot apply (plan fact 2, H); the only other "sign" counted was normal grip when unobserved, which is supportive only. | FIXED: Hoover removed; collapsing (give-way) weakness of both hands documented; the gait that breaks into a normal pace when she sees a friend counted as distractibility; full grip when unobserved and patchy sensory loss listed as supportive; legs 5/5 stated. |
| E | minor | `patient.neurological_exam.additional` | Duplicated history sentence ("Multiple prior presentations ... Patient has extensive prior negative neurology workup."), with counts (visual loss x2, arm weakness x3) that differ from the HPI's list. | FIXED: removed from the examination; replaced by "No event observed during the examination." The HPI keeps the history. |
| E | minor | `patient.neurological_exam.reflexes`, `.sensory`, `.gait` | "Hoffman" misspelt; em dash; scare-quoted 'weakness'. | FIXED: "Hoffmann"; same findings reworded. |
| C | major | `initial_tool_outputs.clinical_assessment` | Meta keys; impression leak "No further investigation is required...". | FIXED (plan H): library keys; 2 validated signs; canonical impression with "No event was observed during the examination." |
| B | major | `initial_tool_outputs.eeg` | Capitals ("NO EEG CHANGE"); "confirms preserved consciousness" (interpretation beyond the recording); impression without canonical opening and final period. | FIXED (plan J): one habitual episode (motionless, eyes closed, 3 min 12 s, answered "yes" to a question midway, typical per husband) with time; 72-hour record; canonical NORMAL video-EEG impression. |
| A | major | `ground_truth.action_criteria` | Template tiers (literature and drug `recommended`, video-EEG `optional`), labels equal rationales. | FIXED (plan 3.2): exam (required), video-EEG `action-4` (required), drug check (optional), new `action-neuropsych-battery` (optional), literature (optional), last. No MRI criterion (plan: none). |
| A | minor | `ground_truth.stop_rule` | Exam only. | FIXED: exam and video-EEG; max 0. |
| B | major | `followup_outputs[0]` (`review_prior_negative_workup`) | A literature search disguising a chart review (ruling 4), reusing PMID 30503873 for a different title. | FIXED: deleted; its clinical point (continuity of specialist follow-up to limit repeated emergency work-ups) became a must. |
| D | major | `initial_tool_outputs.literature_search` | Absent; the literature criterion was answered by the disguised follow-up. | FIXED: canonical output (plan B). |
| D | minor | `initial_tool_outputs.drug_interactions` | Medication list only, with the leak warning; the venlafaxine-naproxen bleeding pair missing (plan C, fact 16). | FIXED: SNRI with NSAID GI bleeding interaction; venlafaxine discontinuation and blood pressure warning. |
| C | major | `ground_truth.assessment` | Template musts and prohibitions (plan D). | FIXED: DX (mixed), COMM with her MS concern addressed, PHYSIO, PSY (depression and somatic symptom disorder), RESCUE, continuity of care with one neurology clinician; prohibitions P1 (adding repeats of her earlier investigations), P2, P3, P5, P6, P7. |
| C | major | `ground_truth.differential` | Epileptic seizures `moderate` ("convulsive-appearing events": the events are motionless); MS citing an MRI the case does not contain; template structural, neuropathy, autoimmune encephalitis and malingering rows; cervical cord, the mimic bilateral hand weakness raises, missing. | FIXED (plan F, S11): focal seizures `low` (canonical feature); MS `low` on clinical incompatibility and her prior normal work-ups; added cervical myelopathy or radiculopathy `low`; template rows deleted. |
| D | major | `ground_truth.key_clinical_evidence` | Template items with the composition leak. | FIXED: five case-specific items. |
| C | minor | `ground_truth.red_herrings` | Generic data points. | FIXED: MS fear from online reading, ten years of normally investigated presentations, depression with maternal somatization disorder, empty nest with marital tension. |
| C | minor | `ground_truth.avoided_actions[*]` | `[Stone_2018]`, generic rationales. | FIXED (plan L): same 7 waste ids, `[Espay_2018]` / `[Stone_2016]`, patient-specific rationales. |
| D | minor | `fallback_tool_outputs` | Specialized-test, advanced-imaging and drug stubs; echo "benign incidental finding" unnamed. | FIXED (plan G): stubs nulled and removed from `metadata.fallback_tool_kinds`; echo names trace physiological mitral regurgitation, `echo_type: TTE`, kind `normal`. |
| E | minor | `metadata.notes`, `difficulty_rationale`, `revision_reason` | Template; "Intensive outpatient program needed" as a note. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing
The examination no longer claims a bilateral Hoover sign for hand weakness (the sign tests the hip); it now documents collapsing weakness of both hands and a careful wide-based gait that normalizes when she sees a friend, with full grip when unobserved and patchy non-anatomical sensory loss as supportive features, and normal reflexes without Hoffmann or Babinski signs. The video-EEG is now required and records one typical episode (motionless, eyes closed, 3 min 12 s, she answered a question during it) without ictal change. The disguised "review prior work-up" literature step is gone; its point became a must for continuity of care with one neurology clinician. The medication check names the venlafaxine-naproxen bleeding risk. The differential holds focal seizures, MS (her stated fear) and cervical myelopathy or radiculopathy, all `low` on case findings. Musts: positive diagnosis, explanation that addresses her MS concern, FND physiotherapy, psychological therapy for depression and somatic symptom disorder, a written event plan and continuity of care; prohibitions P1 (including repeats of her earlier investigations), P2, P3, P5-P7.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- None beyond the plan's condition-wide list.

## Open questions for Andrea (judgment calls you could not settle)
- None. Cervical myelopathy or radiculopathy was added to the differential beyond the plan's list because bilateral hand weakness in a 45-year-old raises it; it is `low` on examination grounds and no imaging criterion was added.

## Checks
- `perfect_agent.py FND-S11 -v`: ok; exam and video-EEG receive the stored clinical assessment and video-EEG.
- `case_io.py check FND-S11`: schema and synonym guard OK; no failure names FND-S11 or the condition.
- `test_case_guards.py -k FND-S11`: pass.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case against the plan (section 4 S11) and PATTERNS.md.
- Confirmed: Hoover removed for hand weakness and replaced by collapsing weakness (the plan's option), unobserved full grip supportive only, the duplicated history sentence removed from the exam; EEG event matches the HPI; venlafaxine-naproxen pair correct; disguised chart-review follow-up turned into a continuity-of-care must; no MRI criterion as planned, with the added cervical myelopathy or radiculopathy row `low` on examination grounds; diagnosis unchanged.
- Found and fixed: `avoid-waste-4-order-ct-scan.rationale` said "No head injury or new focal sign" although the presentation is a new bilateral hand weakness; now "No head injury, and the new hand weakness carries positive functional signs without an upper motor neuron sign".
- Checks after my edits: `perfect_agent.py -v` ok (each required and recommended call served by the case's own stored report, not a fallback; the "<- ?" source label is a dump-format artefact, confirmed by executing the calls through the environment); `case_io.py check` schema and synonym guard OK, no test failure names the case; `test_case_guards.py -k` pass; discriminator guard (FND not yet enabled) run by hand: clean.
- Flagged for the condition lead (not changed, plan class L governs all 30): ECG kept as `waste` in event cases. NICE CG109 and NG217 advise a 12-lead ECG after a first transient loss of consciousness or suspected first seizure; where the events are unrecorded before admission the lead may prefer to drop the ECG avoided action rather than penalize it.

## Condition audit

2026-10-24, FND condition auditor.

- `action-1-search-medical-literature.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.
