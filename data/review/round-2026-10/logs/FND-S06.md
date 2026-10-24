# FND-S06
Reviewer status: R1 not reviewed, R2 not reviewed (no FND notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search[...]` | Summary and only finding were the criterion's `expected_evidence`; leak guard failed (plan baseline). | FIXED: plan class B canonical seven-row output; literature criterion `optional`, last. |
| A | major | `ground_truth.action_criteria` | Template tiers (literature and drug check `recommended`, MRI and video-EEG `optional`), labels equal rationales, template citation strings. | FIXED (plan A, 3.2): exam (required), MRI `action-4` (recommended, `{contrast: false}`), video-EEG `action-5` (required), drug check (optional), new `action-neuropsych-battery` (optional), literature (optional); case-specific labels, rationales, keys and `expected_evidence`. |
| A | minor | `ground_truth.sequence_constraints`, `stop_rule` | None; stop rule exam only. | FIXED: soft exam -> MRI; `required_before_assessment` exam and video-EEG; max 0. |
| C | major | `patient.neurological_exam.motor`, `initial_tool_outputs.clinical_assessment` | "Arm drift: left arm rises with eyes closed": upward drift is a parietal or cerebellar sign, not a functional one, and with a left hemisensory loss it would point to a right parietal lesion (plan fact 2). | FIXED: replaced by drift without pronation of the left arm (a validated sign, Daum 2014), as the plan does for P08. |
| B | major | `patient.neurological_exam.motor`, clinical assessment Hoover finding | Hoover described as "hip extension 5/5 when right heel pressed down": the involuntary extension is felt under the weak (left) heel during right hip flexion. | FIXED: correct manoeuvre wording. |
| C | major | `initial_tool_outputs.clinical_assessment` | Meta `criteria_met` keys; fragments ("Dragging left leg with clutching posture;"); the same tapping test counted twice (distraction and entrainment); impression leak "No further investigation is required...". | FIXED (plan H): library keys; 4 validated signs (Hoover, drift without pronation, tremor entrainment with distractibility as one test, dragging monoplegic gait); non-anatomical hemisensory loss and normal walking when unobserved supportive, not counted; canonical impression. |
| E | minor | `patient.neurological_exam.coordination`, `.gait`, `.motor` | "Left leg: apparent inability but with Hoover sign normal" (garbled), em dash in the tremor sentence. | FIXED: heel-shin not assessable on the left because of the weakness; gait and tremor sentences rewritten without changing the findings. |
| E | minor | `patient.history_present_illness` | Ungrammatical sentence "She has a family history of maternal aunt with childhood epilepsy, which resolved, causing her significant concern." | FIXED: "Her maternal aunt had childhood epilepsy that later resolved, and this worries her." |
| B | minor | `initial_tool_outputs.eeg` | Capitals ("NO EEG CHANGE"), impression without the canonical opening and final period, no time or recording duration. | FIXED (plan J): one habitual event (staring with eyelid flutter, 1 min 40 s, identified by the patient as typical) with time; 24-hour wake and sleep record; canonical NORMAL video-EEG impression. |
| B | major | `initial_tool_outputs.mri` | "Normal brain MRI without and with contrast ... no abnormal enhancement" with a non-contrast criterion. | FIXED (plan I): non-contrast report with DWI/ADC and SWI. |
| D | minor | `initial_tool_outputs.drug_interactions` | Medication list only, with the leak warning; the real fluoxetine-sumatriptan serotonergic pair missing (plan C). | FIXED: serotonergic interaction; sumatriptan contraindicated in hemiplegic migraine and ischemic stroke or TIA; sulfonamide allergy note (sulfonamide group in sumatriptan, cross-reactivity not expected, already tolerated). |
| C | major | `ground_truth.assessment` | Seven template musts and eight template prohibitions (plan D). | FIXED: musts DX (mixed), COMM, PHYSIO, PSY (PTSD and depression, trauma-informed given the adolescent abuse), RESCUE; prohibitions P1, P2, P3, P5, P6, P7. |
| C | major | `ground_truth.differential` | Epileptic seizures `moderate` after a normal video-EEG, "convulsive-appearing events" (the events are staring spells); template structural, autoimmune encephalitis and malingering rows; hemiplegic migraine, the mimic the case raises, missing. | FIXED (plan F): focal impaired-awareness seizures `low`; hemiplegic migraine or prolonged aura `low` (migraine without aura, no headache, positive signs, normal MRI); stroke or TIA `low`; MS `low` (prior right leg episode, signs, MRI); template rows deleted. |
| D | major | `ground_truth.key_clinical_evidence` | Eight template items with the composition leak, OPTIONAL and Stone 2018 items. | FIXED: five case-specific items. |
| C | minor | `ground_truth.red_herrings` | Generic data points; stressor row duplicated the trauma row. | FIXED: aunt's resolved childhood epilepsy (real, kept), migraine-stroke concern (new), depression on fluoxetine, witnessed injury and abuse anniversary; duplicate removed. |
| C | minor | `ground_truth.avoided_actions[*]` | `[Stone_2018]`, generic rationales. | FIXED (plan L): same 8 waste ids, `[Espay_2018]` / `[Stone_2016]`, patient-specific rationales (CT: deficit over 24 h, no thrombolysis decision, MRI answers the stroke question). |
| D | minor | `fallback_tool_outputs` | Specialized-test, advanced-imaging, drug and literature stubs. | FIXED (plan G): nulled and removed from `metadata.fallback_tool_kinds`; echo fallback `echo_type: TTE`. |
| E | minor | `metadata.difficulty_rationale`, `revision_reason` | Template ("supportive normal labs" with no labs). | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing
The case now requires the examination and a video-EEG and recommends one non-contrast brain MRI for the stroke question raised by acute left hemiparesis in a migraineur. The examination counts four validated signs: left Hoover sign (manoeuvre now described correctly), drift without pronation of the left arm (replacing an "upward drift", which is a parietal sign and not a functional one), tremor entrainment and dragging monoplegic gait; the non-anatomical hemisensory loss and normal walking when unobserved are supportive only. The video-EEG records one habitual staring spell with eyelid flutter (1 min 40 s) without ictal change. The MRI report is a normal non-contrast study with DWI. The medication check now names the fluoxetine-sumatriptan serotonergic pair, the triptan contraindication in hemiplegic migraine and stroke, and the sulfonamide allergy. The differential adds hemiplegic migraine or prolonged aura (`low`), keeps stroke and MS `low`, and lowers focal seizures to `low` after the recording, with co-occurring epilepsy noted as possible. Musts: positive diagnosis, explanation, FND physiotherapy, trauma-informed psychological therapy treating PTSD and depression, written event plan; prohibitions P1-P3 and P5-P7.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- EEG routing (plan 5.3): a `routine` EEG order is answered with the stored video-EEG and its event (checked through the environment).

## Open questions for Andrea (judgment calls you could not settle)
- None.

## Checks
- `perfect_agent.py FND-S06 -v`: ok; the exam, MRI and video-EEG calls receive the stored clinical assessment, non-contrast MRI and video-EEG (verified through the environment).
- `case_io.py check FND-S06`: schema and synonym guard OK; no failure names FND-S06.
- `test_case_guards.py -k FND-S06`: pass.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case against the plan (section 4 S06) and PATTERNS.md.
- Confirmed: the exam rewrite (upward drift replaced by drift without pronation, Hoover felt under the weak left heel) keeps every other finding and makes the case coherent (an upward drift with left hemisensory loss would point to a right parietal lesion); hemiplegic migraine added `low` with the right argument (her migraine is without aura); serotonergic pair and triptan cautions correct; PTSD target supported by 6 weeks of nightmares and flashbacks after the injury; non-contrast MRI; EEG event matches the HPI; musts and prohibitions as planned; diagnosis unchanged; no banned strings or new em dashes.
- Found: no error requiring a change.
- Checks after my edits: `perfect_agent.py -v` ok (each required and recommended call served by the case's own stored report, not a fallback; the "<- ?" source label is a dump-format artefact, confirmed by executing the calls through the environment); `case_io.py check` schema and synonym guard OK, no test failure names the case; `test_case_guards.py -k` pass; discriminator guard (FND not yet enabled) run by hand: clean.
- Flagged for the condition lead (not changed, plan class L governs all 30): ECG kept as `waste` in event cases. NICE CG109 and NG217 advise a 12-lead ECG after a first transient loss of consciousness or suspected first seizure; where the events are unrecorded before admission the lead may prefer to drop the ECG avoided action rather than penalize it.

## Condition audit

2026-10-24, FND condition auditor.

- `action-1-search-medical-literature.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.
