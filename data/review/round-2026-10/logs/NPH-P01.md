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
