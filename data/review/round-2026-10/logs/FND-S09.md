# FND-S09
Reviewer status: R1 not reviewed, R2 not reviewed (no FND notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `initial_tool_outputs.literature_search`, `.drug_interactions` | Neither existed; the literature and drug criteria were answered only by disguised follow-ups. | FIXED: canonical literature output (plan B); drug output in `DrugInteractionResult` fields (plan C): sertraline with ibuprofen GI bleeding risk increased by alcohol; prazosin orthostatic caution; alcohol with sertraline sedation. |
| B | major | `followup_outputs[0]` (`va_fnd_ptsd_documentation`), `followup_outputs[1]` (`alcohol_counseling_referral`) | A literature search disguising VA documentation (reused PMID 30503873, empty summary) and a drug check that was a naltrexone prescription plan (ruling 4; plan B, C). | FIXED: both deleted; the alcohol content became the must "Assess alcohol use and offer a brief intervention." |
| A | major | `ground_truth.action_criteria` | Template tiers (literature and drug `recommended`, video-EEG and labs `optional`), labels equal rationales. | FIXED (plan 3.2): exam (required), labs `action-5` (recommended: CMP, magnesium, thiamine_B1), new optional `action-brain-mri`, video-EEG `action-4` (required), drug check (optional), new `action-neuropsych-battery` (optional), literature (optional), last. |
| A | minor | `ground_truth.stop_rule` | Exam only. | FIXED: exam and video-EEG; max 0. No sequence constraint (no required or recommended MRI). |
| B | major | `initial_tool_outputs.labs` | The labs criterion orders CMP, magnesium and thiamine, but the panel held "CMP: Within reference range" and "B12: Within reference range" with no units, no magnesium and no thiamine; template `clinical_significance` ("Ordered as part of the baseline workup..."); sodium and glucose duplicated outside the CMP; "GGT 88 (mildly elevated - alcohol use)" causal claim in the summary. | FIXED (plan K): full CMP with values and units (stored sodium 137 and glucose 96 kept), magnesium 2.0 mg/dL, whole-blood thiamine 96 nmol/L, B12 412 pg/mL; `clinical_significance` null; summary "GGT 88 U/L (H)"; prolactin row kept as measured with no interpretive claim. |
| B | major | `initial_tool_outputs.eeg` | Capitals ("NO EEG CHANGE", "NO EEG CORRELATE"), "muscle artifact ... suggesting voluntary muscle contraction" (an EEG cannot judge intent), impression not in canonical form. | FIXED (plan J): one habitual episode (motionless, eyes closed, 1 min 52 s, typical per partner) with time; persistent 10 Hz posterior rhythm; muscle artifact stated without inference; canonical NORMAL video-EEG impression. |
| C | major | `initial_tool_outputs.clinical_assessment` | Meta keys; fragments ("resolves when distracted by conversation."); 5 signs counted from split sentences; impression leak. | FIXED (plan H): library keys plus `functional_seizure_semiology_observed: true` (the ward episode was seen); 4 validated signs (Hoover, dragging gait, variability, tremor entrainment); hemisensory loss supportive; observed-event finding; canonical event-based impression. |
| B | minor | `patient.neurological_exam.motor`, `.gait`, `.sensory`, `.additional` | Hoover sign stated with only arm weakness described (the leg weakness on direct testing was missing); gait "dragging pattern with exaggerated hip hiking" (hip hiking is a circumducting, not a dragging, pattern); teaching parenthetical in sensory ("peripheral nerve would show stocking-glove loss..."); em dashes. | FIXED: right hip extension weak on direct testing stated; gait is a dragging monoplegic gait that normalizes with distraction; parenthetical removed; findings otherwise unchanged. |
| C | major | `ground_truth.assessment` | Template musts and prohibitions (plan D). | FIXED: DX (mixed), COMM, PHYSIO, PSY (trauma-focused therapy for PTSD), RESCUE, alcohol brief intervention; prohibitions P1, P2, P3, P5, P6, P7. |
| C | major | `ground_truth.differential` | Epileptic seizures `moderate` ("convulsive-appearing events": the events are motionless); template structural ("normal brain MRI": no MRI in the case), autoimmune encephalitis and malingering `very_low` rows. | FIXED (plan F, S09): post-traumatic epilepsy `low` (canonical feature); alcohol withdrawal seizures `low`; structural lesion `low` on examination grounds; malingering or factitious disorder `low`, naming the denied claim and the appeal. Autoimmune encephalitis deleted. |
| D | major | `ground_truth.key_clinical_evidence` | Template items with the composition leak. | FIXED: five case-specific items. |
| C | minor | `ground_truth.red_herrings` | One generic stressor row. | FIXED: blast mild TBI, denied claim and appeal, daily alcohol with raised GGT, combat PTSD. |
| C | minor | `ground_truth.avoided_actions[*]` | `[Stone_2018]`, generic rationales. | FIXED (plan L): same 8 waste ids, `[Espay_2018]` / `[Stone_2016]`, patient-specific rationales. |
| D | minor | `fallback_tool_outputs` | Specialized-test and advanced-imaging stubs; echo "benign incidental finding" not named in the impression. | FIXED (plan G): stubs nulled and removed from `metadata.fallback_tool_kinds`; echo names "trace physiological mitral regurgitation", `echo_type: TTE`, kind `normal`. |
| B | minor | `metadata.notes` | "Remote microhemorrhage is a red herring" although the case has no MRI report. | FIXED: note rewritten without it. |
| E | minor | `metadata.difficulty_rationale`, `revision_reason` | Template. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing
The case now requires the examination and a video-EEG and recommends a targeted metabolic panel (CMP, magnesium, thiamine) for a man who drinks daily and has unresponsive episodes. The examination counts four validated signs: right Hoover sign (with the leg weakness on direct testing now stated), a dragging monoplegic gait that normalizes with distraction, arm strength varying between 2/5 and 4/5, and an entraining variable-frequency tremor; the non-anatomical hemibody sensory loss is supportive. The ward episode (90 s, eyes closed, motionless, immediate recovery) is recorded as an observed event. The video-EEG records one typical episode with a persistent posterior rhythm and no ictal change, and no longer calls the muscle artifact "voluntary". The labs are now a real panel: normal electrolytes, glucose, calcium, magnesium and thiamine, blood alcohol zero, GGT 88 U/L. The differential holds post-traumatic epilepsy, alcohol withdrawal seizures, a structural lesion and malingering (naming the denied disability claim), all `low` with case reasons. Musts: positive diagnosis, explanation, FND physiotherapy, trauma-focused therapy for PTSD, a written event plan and a brief alcohol intervention; prohibitions P1-P3 and P5-P7. The VA documentation and naltrexone follow-ups are gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- None beyond the plan's condition-wide list.

## Open questions for Andrea (judgment calls you could not settle)
- Resolved here, departing from the plan: (1) the plan's musts for S09 omit M-PHYSIO, but he has functional right-sided weakness, a dragging gait and a functional tremor, so the motor phenotype rule of plan class D applies and M-PHYSIO is included; (2) the plan lists S09 under "no MRI criterion", but the pack makes one non-contrast MRI optional in the cases without a recommended scan, and a right-sided deficit progressing over 3 months after a blast injury makes one scan defensible; without a criterion that scan would be penalized as an unjustified extra action. An optional `action-brain-mri` (`{contrast: false}`, no stored output, library normal answers) was added; it carries no credit and is not in the stop rule. Revert by deleting that criterion if the lead prefers strict uniformity.

## Checks
- `perfect_agent.py FND-S09 -v`: ok; the exam, the labs order (CMP, magnesium, thiamine_B1) and the video-EEG receive the stored clinical assessment, the full lab panel and the video-EEG (verified through the environment).
- `case_io.py check FND-S09`: schema and synonym guard OK; no failure names FND-S09.
- `test_case_guards.py -k FND-S09`: pass.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case against the plan (section 4 S09) and PATTERNS.md.
- Confirmed: lab panel complete with units, magnesium and thiamine present for the criterion, GGT the only abnormal value with matching `is_abnormal`, `abnormal_values_summary` and interpretation; prolactin row without overclaim; EEG no longer infers "voluntary" contraction; observed ward event agrees with the exam text; added M-PHYSIO is required by plan class D for the motor phenotype; the optional brain MRI (beyond the plan) carries no credit, is not in the stop rule and is clinically defensible for a 3-month progressive hemiparesis; diagnosis unchanged.
- Found and fixed: the malingering row argued against feigning because "the symptoms began before the denial", but the HPI dates onset to when the claim process intensified, so the incentive predates the symptoms; the row now says timing does not separate them and rests on the absence of evidence of deception and the PTSD setting. The alcohol withdrawal row and its red herring said the episodes "recur regardless of drinking", which the HPI does not state; both now say they "recur(red) over 3 months while he continues to drink daily" (HPI: drinks 2-4 beers daily).
- Checks after my edits: `perfect_agent.py -v` ok (each required and recommended call served by the case's own stored report, not a fallback; the "<- ?" source label is a dump-format artefact, confirmed by executing the calls through the environment); `case_io.py check` schema and synonym guard OK, no test failure names the case; `test_case_guards.py -k` pass; discriminator guard (FND not yet enabled) run by hand: clean.
- Flagged for the condition lead (not changed, plan class L governs all 30): ECG kept as `waste` in event cases. NICE CG109 and NG217 advise a 12-lead ECG after a first transient loss of consciousness or suspected first seizure; where the events are unrecorded before admission the lead may prefer to drop the ECG avoided action rather than penalize it.

## Condition audit

2026-10-24, FND condition auditor.

- `action-5-interpret-labs.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-brain-mri.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-1-search-medical-literature.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.
