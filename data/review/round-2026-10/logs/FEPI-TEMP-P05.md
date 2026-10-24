# FEPI-TEMP-P05
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for FEPI-TEMP) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance for focal_epilepsy_temporal (condition_tool_guidance.yaml), applied through plans/FEPI-TEMP.md. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.history_present_illness`, `patient.neurological_exam.additional`, `ground_truth.red_herrings[0]` | The one convulsive episode was "brief slumping with 15-20 seconds of rhythmic right arm jerking": unilateral right arm clonic activity points to the left hemisphere (contralateral), against a right temporal focus, and it is not the "focal-to-bilateral tonic-clonic evolution" the label states. | FIXED: the episode starts with the habitual aura and staring, then slump, leftward head turn (contralateral version), bilateral stiffening and jerking more marked on the left for about 40 seconds and 20 minutes of confusion; ED attribution to convulsive syncope kept as the red herring, rewritten in both fields and in red herring [0]. |
| B | major | `initial_tool_outputs.ecg.findings[0]`, `.interpretation`, `ground_truth.red_herrings[1]` | "First-degree AV block (PR 194 ms; upper limit 200 ms)" is self-contradictory: first-degree AV block is PR above 200 ms. | FIXED: "PR interval 194 ms, at the upper limit of normal; no AV block"; interpretation "Normal sinus rhythm, 68/min" with the intervals; red herring [1] data point and interpretation match (path unchanged, still holds the PR finding). |
| D | minor | `patient.history_present_illness` | "12-lead ECG (borderline findings, see below)" pointed at the result of a study the case scores. | FIXED: "a 12-lead ECG". |
| B | minor | `patient.clinical_history.social_history.driving` | "Drives to work daily; has self-restricted driving" contradicts itself. | FIXED: "Drove to work daily; has not driven since the second episode" (HPI agrees). |
| B | major | `initial_tool_outputs.labs` | Prolactin "drawn 22 minutes after witnessed convulsive episode in ED" sat in today's panel although the only convulsive episode was 3 months ago. | FIXED: row and summary say it is the emergency department sample from 3 months ago; interpretation separates current normal values from that result (plan class M keeps this one timed level). |
| C | major | `initial_tool_outputs.mri` | Gadolinium lines in an HS case (class E); "No evidence of dual pathology" while the report shows HS plus a separate temporopolar scar, which is dual pathology by definition (Blumcke 2011). | FIXED: post-gadolinium entries and enhancement lines removed; dual-pathology line replaced by a normal left hippocampus line; impression names the dedicated epilepsy-protocol sequences, both volumes and the index (0.18 = (3.3 - 2.3)/5.6). |
| D | minor | `initial_tool_outputs.eeg` | "2-hour routine study" (routine EEG is 20 to 40 minutes). | FIXED: routine 40-minute recording with drowsiness and stage 2 sleep; impression and limitations agree. |
| C | major | `followup_outputs[request_video_eeg]` | 72 hours with two habitual events for a man with 11 events in 6 months and no activation; semiology in the `state` field; no ECG channel result in a seizure-versus-syncope study; em dash. | FIXED: 5-day study with partial sleep deprivation; events on days 3 and 5; semiology in `clinical_correlation`; new finding for the ECG channel (ictal sinus tachycardia to 98/min, no bradycardia or asystole); numbered impression. |
| D | minor | `fallback_tool_outputs.advanced_imaging.impression` | "concordant with right temporal EEG focus" is cross-modality synthesis. | FIXED: PET findings only. Kept as fallback behind the FDG_PET waste action. |
| A | major | `fallback_tool_outputs.specialized_test` | `test_type: "not_specified"` (class Q). | FIXED: null; `metadata.fallback_tool_kinds.specialized_test` removed. |
| D | blocker | `followup_outputs[search_seizure_syncope_differentiation]` | Sources without authors (class O), unverified sensitivity figures, prolactin said to separate seizure from syncope. | FIXED: Brignole 2018 ESC syncope, Chen 2005 AAN prolactin (does not separate seizure from syncope), Marson 2021 SANAD II, stated accurately; no criterion's expected evidence repeated; moved last. |
| C | major | `followup_outputs[check_drug_interactions_...]` | Em dashes; no mention of the PR interval with lacosamide, which the output offered as an alternative. | FIXED: real check against lisinopril and atorvastatin, inducers lower atorvastatin, lacosamide PR warning with his PR of 194 ms, lamotrigine rash warning, levetiracetam mood effects. |
| C | major | `followup_outputs` (order) | Literature first, drug check second, video-EEG last. | FIXED: video-EEG, drug check, literature. |
| C | major | `ground_truth.action_criteria` | MRI `{contrast: true}`; literature and drug check required; template evidence (EEG, video, labs, ECG); rationale = label; duplicate citations. | FIXED per plan: MRI `{protocol: epilepsy}`, routine EEG, video-EEG, ECG required; drug check recommended; labs and literature optional; evidence names the stored results; one key each. Order MRI, routine EEG, video-EEG, labs, ECG, drug check, literature. Ids kept. |
| C | minor | `ground_truth.sequence_constraints` | MRI -> drug check soft with a non-canonical reason and the false Glauser 2017 key. | FIXED: kept (drug check recommended) with the canonical reason and `[NICE_NG217_2025]`. |
| C | major | `ground_truth.stop_rule` | Literature and drug check listed; max 0. | FIXED: MRI, routine EEG, video-EEG, ECG; max 2. |
| C | major | `ground_truth.assessment.required_recommendations` | Video-EEG must (scored work-up), two "Recognize ..." musts that are diagnostic insight, and a prolactin must claiming it separates seizure from syncope (wrong, Chen 2005); "levetiracetam or lacosamide preferred" against first-line guidance; no SUDEP. | FIXED: four musts: lamotrigine or levetiracetam first line without inducers (atorvastatin); driving; SUDEP (he has had a focal to bilateral tonic-clonic seizure); tell him and cardiology that the events are epileptic so the syncope work-up closes. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Wording ("when EEG confirms"), event recorder listed with pacemaker. | FIXED: pacemaker or loop recorder, antiarrhythmics, EP study or ablation, inducers with atorvastatin; first prohibition states the video-EEG basis. |
| C | major | `ground_truth.differential` | Convulsive syncope `high`, vasovagal and PNES `moderate` after a negative cardiac work-up and a video-EEG capture (class P). | FIXED: arrhythmic and vasovagal syncope `low`, PNES and TIA `very_low`, frontal `low`, each with the excluding finding. |
| C | major | `ground_truth.key_clinical_evidence` | Engineering lines (class G); prolactin called a marker against syncope (fact 11); em dash. | FIXED: seven case lines; prolactin argues against PNES only. |
| C | minor | `ground_truth.avoided_actions[*]` | Generic rationales and `[AAN_2007]` everywhere. | FIXED: case-specific rationales; CSF and CT waste kept (elective, MRI available, no emergency indication), FDG_PET waste with the canonical rationale. |
| E | minor | `metadata.difficulty_description`, `.difficulty_rationale` | Prolactin as a seizure-versus-syncope discriminator, tool-count engineering wording, em dashes. | FIXED: clinical description. |

## Changes, in one paragraph a physician can read before re-reviewing

A 55-year-old man with a remote head injury has six months of stereotyped events (rising epigastric sensation, deja vu, staring with oroalimentary and right-hand automatisms, about 5 minutes of confusion) and one convulsive episode, now described as a focal to bilateral tonic-clonic seizure (leftward head turn, bilateral stiffening and jerking for about 40 seconds, 20 minutes of confusion), that the ED called convulsive syncope; cardiology found nothing. The scored work-up is an epilepsy-protocol MRI (right hippocampal sclerosis plus a remote right temporal pole scar, no gadolinium), a routine 40-minute EEG with right anterior temporal sharp-and-slow waves, a 5-day video-EEG recording two habitual seizures with right temporal onset and sinus tachycardia without asystole on the ECG channel, and a 12-lead ECG whose PR of 194 ms is now correctly called upper-normal rather than first-degree block. The drug check (atorvastatin with inducers, lacosamide and PR) is recommended; labs and literature are optional. The ED prolactin of 48 ng/mL at 22 minutes is kept as evidence against PNES only. Musts: lamotrigine or levetiracetam without inducers, driving, SUDEP, closing the syncope work-up with cardiology; the cardiac-intervention prohibitions stay.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Criteria pack allow-list: `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]` (plan CENTRAL 2). The literature output cites Brignole 2018 (`[ESC_syncope_2018]`), Chen 2005 (`[AAN_prolactin_2005]`) and Marson 2021 (`[SANAD2_2021]`) from the plan's list.

## Open questions for Andrea (judgment calls you could not settle)

None. Departures from the plan: the prolactin must was deleted rather than reworded, because interpreting a lab is not management (the corrected statement lives in the key evidence, the labs criterion and the differential); the convulsive episode was rewritten so that the semiology is concordant with the right temporal focus and supports the label's focal to bilateral tonic-clonic evolution.

## Verification

Adversarial check, 24 Oct 2026. Read the log, the diff and the whole final case. Checked: the rewritten convulsive episode (leftward version, left-predominant jerking) is concordant with the right temporal focus in HPI, exam, KCE and red herring [0]; PR 194 ms is called upper-normal with no AV block in the ECG, its criterion and red herring [1] (path still holds that finding); the prolactin row is the only one kept, timed at 22 minutes, and every mention says it argues against PNES and does not separate seizure from syncope (fact 11, Chen 2005); volumetric index 1.0/5.6 = 0.18 is right; video-EEG ECG channel, impression and evidence agree; the drug output matches lisinopril and atorvastatin; differential is the post-video-EEG view; the literature output states Brignole 2018, Chen 2005 and SANAD II correctly.
Found and fixed: (1) class H not finished: the labs and ECG criteria still listed `[NICE_NG217_2025]` and the unbracketed `NICE_NG217_2025`; the unbracketed duplicates removed. (2) The CT waste rationale said "no head injury" in a man whose history has a head injury at 38; now "no recent head injury". `perfect_agent.py -v`, `case_io.py check` and the case guards pass after the edit.

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.
- `action-8-interpret-labs.rationale`: engineering prefix or tier wording removed (was "Optional: nothing in the history suggest...").
- `action-4-search-medical-literature.rationale`: engineering prefix or tier wording removed (was "Optional background; the diagnosis rests...").
- Routine and video-EEG and the EEG criterion: "frequent" discharges at 8-22 per hour are "occasional" (ACNS 2021).

## Close-out (24 Oct 2026)

Condition close-out (`plans/FEPI-TEMP-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G40 entries, re-applied with `--prune --conditions focal_epilepsy_temporal`): labels now focal epilepsy, temporal lobe epilepsy, TLE, epilepsy temporal lobe, mesial temporal lobe epilepsy, MTLE (added), mesial temporal sclerosis epilepsy; removed focal seizures; focal onset seizures; focal impaired awareness seizures (seizure-type labels, retired: their tokens occur in an acute symptomatic or functional-seizure answer). Codes: G40.2, G40.1, G40.9 plus G40.209, G40.109, G40.909 (not intractable); the idiopathic G40.009 and G40.019 removed and the intractable codes removed.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FEPI-TEMP-` passes, now with the discriminator guard and the FEPI-TEMP banned strings.
