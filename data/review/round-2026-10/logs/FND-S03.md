# FND-S03
Reviewer status: R1 not reviewed, R2 not reviewed (FND has no notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.clinical_history.medications` | The HPI says she was started on levetiracetam 500 mg twice daily for suspected seizures (and still takes it: "reports no change"), but the medication list omits it, so no drug check could see it and no must withdrew it. Same defect the plan fixes in M02. | FIXED: levetiracetam 500 mg twice daily added (indication: suspected seizures, started empirically at urgent care two weeks ago). |
| C | major | `ground_truth.action_criteria[action-2-check-drug-interactions]`, `.sequence_constraints`, `.stop_rule`, `.assessment` | With an antiseizure drug started for the events, this is the plan's taper variant (3.5), not a "recommended" lorazepam review. | FIXED (plan deviation, see Open questions): drug check required (levetiracetam and lorazepam), soft constraint video-EEG before drug check (AAN 2025; Oto 2005), in the stop rule; M-ASM "Taper and stop levetiracetam under neurological supervision..."; P5 "...or stop it abruptly". |
| C | major | `ground_truth.action_criteria[action-5-analyze-eeg]` | Video-EEG `optional` although she was admitted for continuous video-EEG. | FIXED (plan 3.2): required, canonical expected_evidence, case rationale, in the stop rule. |
| B | minor | `initial_tool_outputs.eeg` | Impression with "NO EEG correlate" in capitals, no final period, not in canonical form; one unnamed finding for three events; beta "likely secondary to anxiety or medication effect". | FIXED (plan J): three habitual events with times and durations (1 min 50 s, 2 min 35 s, 1 min 10 s), canonical impression, attribution removed, N2 wording. |
| B | major | `initial_tool_outputs.mri` | Criterion orders `contrast: false`; report was "with and without gadolinium" with a post-contrast row and a bundled MRA. | FIXED (plan I): non-contrast technique line, enhancement and MRA removed; optional criterion with `{"contrast": false}` only. |
| D | major | `followup_outputs[0]` (literature) | CODES misreported; "Espay ... BMJ 2018" is Aybek and Perez, BMJ 2022. | FIXED (plan B): deleted; canonical initial literature output. |
| D | major | `initial_tool_outputs.drug_interactions`, `fallback_tool_outputs.drug_interactions` | Initial output empty with the "prescribing decision" leak; fallback "(agent not specified on this case's pathway)". | FIXED (plan C, G): initial output with her four medicines, sertraline with lorazepam (minor), levetiracetam behavioural and mood cautions with gradual withdrawal, lorazepam benzodiazepine cautions, dicyclomine anticholinergic note; fallback null and removed from kinds. |
| B | minor | `patient.clinical_history.social_history.living_situation` | "Lives with her partner" and "recently separated from her partner" in the same field. | FIXED: lives alone since the separation 3 weeks before admission. |
| B | minor | `patient.neurological_exam.sensory`, `.additional` | Whole-leg loss to the inguinal crease "with midline splitting on the trunk" (the leg pattern does not reach the trunk); "Hoover sign POSITIVE" in capitals. | FIXED: boundary at the inguinal crease in both fields; lowercase. |
| C | major | `initial_tool_outputs.clinical_assessment` | Meta keys; seven "signs" counted including midline splitting, non-anatomical sensory loss (counted twice) and tubular fields; leak sentence. | FIXED (plan H): 4 rule-in signs (Hoover, collapsing weakness, dragging gait, distractibility); tubular field not tested at two distances listed as supportive; observed event; canonical impression. |
| C | major | `ground_truth.assessment.*` | Template musts and prohibitions. | FIXED (plan D): M-DX, M-COMM, M-PHYSIO, M-PSY (GAD and depression), M-ASM (levetiracetam), M-RESCUE, plus no as-needed lorazepam for the events with a gradual taper with her psychiatrist (plan fact 16); P1 naming the repeat CT, P2, P3, P5 with "abruptly", P6, P7. |
| C | major | `ground_truth.differential` | Epileptic seizures `moderate`; MRI-based key features with an optional MRI; neuropathy, encephalitis and malingering (no external incentive beyond medical leave) template rows. | FIXED (plan F): epileptic seizures `low` (no change on levetiracetam, canonical feature); acute ischemic stroke `low` (sudden onset at work); MS or structural lesion `low` on clinical grounds. Other rows removed. |
| D | major | `ground_truth.key_clinical_evidence` | Template items with the "Interim composition decision" leak. | FIXED: five case-specific items. |
| B | major | `ground_truth.red_herrings` | "Family history of epilepsy" cites data the FH denies. | FIXED (plan E): deleted; psychiatric and stressor rows name the case data; added the empirical levetiracetam start. |
| C | minor | `ground_truth.avoided_actions[*]` | Generic rationales, `[Stone_2018]`. | FIXED (plan L): patient-specific, `[Espay_2018]` / `[Stone_2016]`; CT framed as a repeat of the urgent care scan. |
| D | minor | `fallback_tool_outputs.specialized_test`, `.advanced_imaging`, `.echo` | Empty discriminators and the "itself a harm" leak; echo without `echo_type`. | FIXED (plan G). |
| B | minor | `metadata.difficulty_rationale`, `.key_positive_signs` | Template rationale; key signs listed midline splitting. | FIXED. |
| - | check | perfect_agent / guards | perfect_agent `-v` ok in the order exam, video-EEG, drug check, each answered by the case's own output; case guards pass; `case_io.py check`: no failure names FND-S03. | - |

## Changes, in one paragraph a physician can read before re-reviewing

Clinically unchanged: a 28-year-old teacher with two weeks of right leg weakness and daily shaking events after separating from her partner, a normal urgent care CT, and levetiracetam started empirically. The levetiracetam the HPI describes is now on the medication list, which makes this a taper case: the required work-up is the examination, a 48 h video-EEG recording three habitual events without ictal change, and then a medicine review that sets up the levetiracetam withdrawal and flags the as-needed lorazepam. The examination counts four validated signs (right Hoover sign, collapsing weakness, dragging gait, distractibility); the inguinal sensory boundary and an untested tubular field are supportive only. MRI stays optional and is now a non-contrast brain report without MRA. Epilepsy, stroke and a structural lesion are low after the work-up. Musts add a supervised levetiracetam taper and no lorazepam for the events; prohibitions include stopping the antiseizure drug abruptly.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 3 (EEG routing) applies.
- New citation keys used: `[Stone_2016]`, `[Daum_2014]`, `[Avbersek_2010]`, `[Oto_2005]`.
- Lead: plan 3.2 lists S03 as "recommended (lorazepam PRN)"; with the levetiracetam restored it belongs in the taper group with M02, RP01, RP03, RS02 (required drug check, video-EEG before drug check). The pack counts in CENTRAL 1 and 4 change by one.

## Open questions for Andrea (judgment calls you could not settle)

- Resolved by the worker, deviating from the plan: the drug check is required (not recommended) and M-ASM applies, because the HPI records an empirical levetiracetam start that the medication list had dropped (the plan's own M02 decision for the same defect). To revert: remove levetiracetam from `medications`, set the drug check to recommended, drop the constraint, M-ASM and "abruptly".

## Verification
Checked: the log tables against the final file and `git diff`; every claimed FIXED item is present (criteria tiers, required arguments, stop rule, constraints, canonical literature and drug outputs, non-contrast MRI where stored, video-EEG report, exam report, musts, prohibitions, differential, key evidence, red herrings, avoided actions, nulled fallbacks and `fallback_tool_kinds`); medications on the list match the drug-check `proposed` string verbatim; no follow-ups remain; `accepted[0]`, ICD codes, `case_id` and `condition` unchanged; event counts and durations agree across exam, EEG, musts and key evidence; differential key features cite only required or recommended results; no FND banned strings. No reviewer notes exist for FND, so the notes table is correctly empty. Also found and fixed in all six: `metadata.revision_reason` still read "every instrumental test optional", which is false after this round, and `last_revised` was 2026-08-10; both set to the condition's round wording (as in the other FND cases) and 2026-10-24.

Found and fixed:
- B, minor, `patient.clinical_history.medications[Levetiracetam].indication`: "started empirically at urgent care two weeks ago" put the start at symptom onset, before the events began ("over the following days") and before the urgent care visit; now "started empirically at urgent care after the events began".
- E, minor, `initial_tool_outputs.drug_interactions` summary and warning: British "behavioural" in an American-spelling case; now "behavioral".

Checked and accepted: the worker's taper-variant deviation (levetiracetam restored to the list, drug check required, soft video-EEG before drug-check constraint, M-ASM, P5 "or stop it abruptly") is clinically right: the HPI records an empirical levetiracetam start she is still taking, which is the plan's own M02 situation (AAN 2025; Oto 2005). Constraint ids exist and the stop rule lists all three required criteria. "Her psychiatrist" is kept here (prior psychiatric notes are documented).

After the edits: `perfect_agent.py -v` passes, `case_io.py check` shows no failure naming the case, and the case guards pass.

## Condition audit

2026-10-24, FND condition auditor.

- `action-4-analyze-brain-mri.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-neuropsych-battery.expected_evidence`: was empty; set to the wording the other optional batteries use.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.
