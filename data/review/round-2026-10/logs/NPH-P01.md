# NPH-P01
Reviewer status: R1 not reviewed, R2 not reviewed (NPH has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | NPH was never annotated; no note ids exist. The July 2026 tool review (Reviewer 1, `condition_tool_guidance.yaml` key `nph`) is applied through the condition plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | criterion `action-1-search-medical-literature`, `followup_outputs` (`request_literature_nph_alzheimer_copathology`, `request_multidisciplinary_conference`) | Literature search as a recommended step; a multidisciplinary conference / goals-of-care step disguised as a literature search. | FIXED (C1): criterion and both follow-ups removed; goals of care moved into the counselling must. |
| D | major | `patient.history_present_illness`, `.chief_complaint` | "Evans index now 0.37" and "His neurologist suspects superimposed NPH on Alzheimer's". | FIXED (C3): qualitative outside-MRI sentence; referral question; the AD anchor and the missing biomarkers are kept. |
| B | minor | HPI | "Urinary incontinence began acutely" sits badly with an insidious iNPH course (F1). | FIXED: "Urinary urgency began four months ago and has progressed to daily incontinence". |
| B | major | `patient.neurological_exam.mental_status` | "Oriented to person only" and "moderate aphasia" are incompatible with MoCA 16/30 with 0/5 recall (orientation would score 0 to 1/6, leaving at most 19 points for every other domain despite executive, spatial and language deficits). | FIXED: "oriented to place but not to date", "mild anomia"; MoCA moved to the follow-up with subscores that sum to 16 (orientation 3/6). |
| D | major | `patient.neurological_exam.gait`, `.mental_status` | TUG 42 s and MoCA 16/30 in the exam. | FIXED (C4): qualitative only. |
| B | major | `initial_tool_outputs.mri` | "Moderate cortical atrophy" alongside tight high-convexity sulci (DESH) is internally inconsistent; callosal angle 86 degrees called "equivocal" although below 90 it is supportive; duplicate periventricular finding; Fazekas "2-3"; no technique, aqueduct, MTA. | FIXED (C7): mild generalised volume loss with disproportionate hippocampal atrophy (MTA 3), mild DESH, callosal angle 86 degrees, Fazekas 2, patent aqueduct, comparison with the 14-month-old MRI (Evans 0.28); canonical impression. |
| D | major | `initial_tool_outputs.clinical_assessment` | Baseline report contained the post-tap result, "positive tap test" and engineering `criteria_met`. | FIXED (C6): baseline only (TUG 42 s with walker, 10-m walk not measurable, turn 9 steps, falls, retropulsion). |
| B | major | `followup_outputs` AD biomarker output | Contained only assays and a garbled interpretation of numbers without analyte names; an agent ordering tap plus biomarkers would receive no tap result (C17). | FIXED (C17): repeats the full tap report and adds Abeta42 448 (low), Abeta42/40 0.045 (low), p-tau181 78 (raised), total tau 682 (raised, age-adjusted reference) with the A+T+ interpretation. |
| A | major | criterion `action-7-analyze-csf` | Pattern required total tau and lacked the Abeta42/40 alternative. | FIXED (C17): recommended, alternatives `["Abeta42_40_ratio", "phospho_tau"]` and `["Abeta42", "phospho_tau"]`, case-specific label, rationale and evidence. |
| D | minor | `initial_tool_outputs.labs` | HIV "Baseline workup" row and RPR (template). | FIXED (C9). |
| A | major | `ground_truth.action_criteria`, `followup_outputs` | No cognitive screen or post-tap reassessment; rationales repeated labels. | FIXED: MRI, labs (optional), baseline gait, MoCA (optional), CSF (required, `{}`), AD biomarkers (recommended), post-tap reassessment (recommended). |
| C | minor | `followup_outputs` (amyloid and FDG PET) | No case output for amyloid or FDG PET, so the library would return normal scans contradicting the A+T+ profile (C10). | FIXED: authored amyloid PET (binary positive read) and FDG PET (temporoparietal and posterior cingulate hypometabolism, hedged pattern read); both are waste in `avoided_actions`. |
| C | major | `ground_truth.assessment.required_recommendations` | Four process musts and a generic referral; no copathology counselling, no falls must despite six falls. | FIXED (C11): referral; counselling with goals of care; continue donepezil and memantine; falls prevention. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Wrong DESH/triad criterion; "normal ageing" template. | FIXED (C12): canonical text; AD-attribution prohibition reworded for a patient already diagnosed; no withholding of referral because of AD. |
| C | major | `ground_truth.differential` | VCI "high", "AD alone" "high", PD and atrophy "moderate" after a positive tap. | FIXED (C13): AD alone low, VCI moderate (Fazekas 2), PD low, atrophy low, secondary hydrocephalus low. |
| B | minor | `fallback_tool_outputs.ct`, `.drug_interactions`, `.cardiac_monitoring`, `.echo` | CT fallback normal; empty drug-interaction stub; Holter "benign"; no `echo_type`. | FIXED (C2, C18). |
| B | minor | `sequence_constraints`, `stop_rule`, `key_clinical_evidence`, `red_herrings`, `metadata` | Non-canonical reasons; allowance 0; tier sentence and sensitivity 50-80%; red herring argued from "DESH" and "extended drainage" the case lacks. | FIXED (C19, C20). |

## Changes, in one paragraph a physician can read before re-reviewing
The patient block no longer gives the new Evans index, the referring neurologist's suspected diagnosis, the TUG or the MoCA, and the mental status now fits a MoCA of 16 (oriented to place, not date; mild anomia). The MRI compares with the scan 14 months earlier: Evans 0.28 to 0.37, callosal angle 86 degrees, a mild DESH pattern, hippocampal atrophy MTA 3 with only mild generalised loss, Fazekas 2, patent aqueduct. The gait report is the baseline only (TUG 42 s with walker; timed walk impossible because of freezing); the CSF report and a separate reassessment give TUG 37 s at 2 hours and 34 s at 24 hours (19%) and MoCA 16 to 17. CSF Alzheimer biomarkers from the same tap are recommended and show an A+T+ profile, served together with the full tap report; amyloid and FDG PET, if ordered, agree with it but are waste. The literature and conference steps are gone. Musts: shunt referral, counselling that benefit will be mainly gait and continence with goals agreed with the family, continuing donepezil and memantine, falls prevention. The differential puts "AD alone" low and keeps vascular cognitive impairment moderate.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- R2: `[Nakajima_2021]` (referral must, soft sequence reason) is not yet in the NPH criteria pack.
- R4: post-tap reassessment criterion shares the baseline pattern.
- R7: the library would still answer `tau_PET` and `perfusion_SPECT` with normal reports, contradicting the A+T+ profile; a condition-keyed library tier or "not performed" answers would close it.

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the patient block, every stored output and the ground truth. Checked: the mental status (oriented to place not date, mild anomia) matches the itemised MoCA (orientation 3/6, naming 2/3, subscores sum to 16); the temporal horn enlargement is reported as in keeping with MTA 3 hippocampal atrophy, so the supportive features rest on the acute callosal angle and mild DESH, which is what the must and the key evidence cite; the AD-biomarker follow-up repeats the full tap report (C17) with Abeta42, Abeta42/40, p-tau181 and total tau, and the criterion's two alternatives match the vocabulary; amyloid and FDG PET follow-ups agree with the A+T+ profile while the modality stays waste; tap figures agree across CSF report, biomarker follow-up, reassessment, criteria and must (TUG 42 to 37 to 34 s, 12% and 19%; walk not measurable; MoCA 16 to 17); prohibitions keep the AD-attribution item and add the no-withholding item; differential per plan (AD alone low, VCI moderate with Fazekas 2). MockServer probe: plain CSF call returns the tap report without biomarkers; the biomarker call returns the follow-up. `perfect_agent.py -v`, `case_io.py check` and `test_case_guards` clean. No error found; no change made.

## Condition audit (NPH auditor, 24 Oct 2026)
- `[Tisell_2011]` removed from `action-4-analyze-csf.citations`: the pack entry is Tisell 2011, shunt surgery in hydrocephalus with white matter changes, and this rationale is about the tap response only; `[Marmarou_2005]` (tap test) stays.
- Checks after the edits: `perfect_agent.py` passes for all 30 NPH cases, `case_io.py check` clean.

## Close-out (24 Oct 2026)

Condition close-out (`plans/NPH-decisions.md`); no clinical data the agent receives changed.
- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions nph`): code G91.0 removed (ICD-10-CM communicating hydrocephalus, which covers secondary NPH, a different entity from iNPH); labels unchanged, G91.2 and G91.9 accepted.
- `key_clinical_evidence`: "(Marmarou 2005)" written as the key `[Marmarou_2005]`.
- Checks: `perfect_agent.py -v` pass, `case_io.py check` clean, `test_case_guards -k NPH-` pass. Not yet in `DISCRIMINATOR_CONDITIONS`: the post-tap follow-up's prose `assessment_type` is deliberate until the timing discriminator lands (CENTRAL C2 in the decisions file).

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (timing discriminator, NPH R4; decisions Q2 and CENTRAL C2). No clinical text changed.

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment.timing` | added `baseline` |
| `followup_outputs[2]` (`request_post_reassessment`) | `assessment_type` "gait_and_balance_timed (post-tap reassessment)" -> `gait_and_balance_timed`; `timing: post_intervention` added |
| `ground_truth.action_criteria[action-6-perform-clinical-assessment]` | `required_arguments.timing: baseline` (the schema default, so a call that omits it still matches; a post-tap call no longer does) |
| `ground_truth.action_criteria[action-post-tap-gait-reassessment]` | `required_arguments.timing: post_intervention`; importance recommended -> required (Reviewer 1: gait before and after the tap) |
| `ground_truth.sequence_constraints` | soft: `action-4-analyze-csf` before `action-post-tap-gait-reassessment` [Nakajima_2021] |
| `ground_truth.stop_rule.required_before_assessment` | `action-post-tap-gait-reassessment` added |

Scoring change for re-review: the post-tap reassessment is now required and is credited only by a call with `timing: post_intervention`; the baseline order is answered by the baseline report and the reassessment order by the post-tap report (MockServer secondary discriminator).

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 50, ECOG 3; requires considerable assistance and frequent care (fallback_tool_outputs.clinical_assessment). Why: the library gives Karnofsky 100 / ECOG 0 (no evidence of disease, working) in a symptomatic patient.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: MDS-UPDRS III 26 to 25 (4%); gait, gait initiation, turning and postural stability unchanged; no clinically meaningful levodopa response (below 30%) (followup_outputs[5] request_levodopa_challenge). Why: the library describes a normal motor examination and gait; this patient has a gait disorder, and the challenge shows little or no levodopa response.
- `order_specialized_test {test_type: neuropsych_battery}`: amnestic (hippocampal-type) deficit with impaired recognition, plus executive, naming and visuospatial deficits (fallback_tool_outputs.specialized_test). Why: the library reports normal cognition in every domain; this patient has documented cognitive impairment on the stored bedside screen.
- `order_specialized_test {test_type: exercise_stress_test}`: treadmill test not performed (unable to walk safely on a treadmill (severe freezing; walks only with a walker)); non-diagnostic (followup_outputs[6] request_exercise_stress_test). Why: the library describes a 9.5-minute Bruce protocol at 10.4 METs; this patient's gait disorder (magnetic gait with falls) does not allow it.
- `order_echocardiogram {echo_type: exercise_echo}`: exercise not performed (unable to walk safely on a treadmill (severe freezing; walks only with a walker)); resting findings as on the stored TTE (followup_outputs[7] request_exercise_echo). Why: the library describes 9.5 METs on a treadmill with a normal echo; this patient's gait disorder does not allow it.
- `order_advanced_imaging {modality: tau_PET}`: tau-positive: medial and lateral temporal, parietal and precuneus retention (fallback_tool_outputs.advanced_imaging). Why: the library is negative; the stored CSF shows a reduced Abeta42/40 ratio with raised phosphorylated tau and the stored amyloid and FDG PET are abnormal.
- `order_advanced_imaging {modality: perfusion_SPECT}`: bilateral temporoparietal and posterior cingulate hypoperfusion (followup_outputs[8] request_perfusion_spect). Why: the library reports normal perfusion; the stored FDG-PET shows bilateral temporoparietal and posterior cingulate hypometabolism.
- `order_specialized_test {test_type: speech_language_evaluation}`: mild anomia with semantic paraphasias; motor speech normal (followup_outputs[9] request_speech_language_evaluation). Why: the library reports normal naming; the examination documents anomia in conversation.
- Checks: perfect agent ok; case guards pass; criteria answers unchanged.
