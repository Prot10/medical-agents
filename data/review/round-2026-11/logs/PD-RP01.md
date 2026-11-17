# PD-RP01

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 8352e97d-a39e-479d-8984-86f19f6c59fd | FIXED (D21) | `action_criteria[1]` (action-ecg-syncope) recommended to required. `stop_rule.required_before_assessment` = [action-1-analyze-brain-mri, action-ecg-syncope]. New recommended `action_criteria[4]` `eps-accessory-pathway` (order_specialized_test test_type electrophysiology_study; [ESC_SVT_2019][ESC_2018]), with stored `followup_outputs[2]` (trigger request_electrophysiology_study): single manifest right posteroseptal accessory pathway, anterograde ERP 310 ms, shortest pre-excited RR in induced AF 300 ms, no inducible AVRT with or without isoprenaline, low-risk properties; no management in the report. `assessment.required_recommendations[1]` canonical D21 text. `prohibited_recommendations[2]` = 'Do not consider the syncope evaluation complete after a negative Holter'. `key_clinical_evidence[3]`, `differential[1]`, `red_herrings[0]` and `[1]` rewritten. `diagnosis.rejected`: `wolff parkinson white` and `WPW` removed (D30). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | `ground_truth.assessment.required_recommendations[0]` | 'counterbalanced by two supportive criteria' implied that two are needed (F2) | FIXED: 'counterbalanced (one supportive criterion is enough; here rest tremor and olfactory loss on Sniffin' Sticks 6/12)' |
| B | minor | `followup_outputs[2]` (new EPS) | The plan suggested a left-lateral pathway, but the stored ECG has delta waves in I, aVL and V2-V6 and not V1, a pattern that fits a right posteroseptal pathway better (a left-lateral pathway gives negative delta waves in I and aVL) | FIXED: pathway written as right posteroseptal; the other values are the plan's |
| B | minor | `metadata.difficulty_rationale` | Tier counts outdated | FIXED: 2 required (MRI, ECG), 3 recommended (Holter, EPS, medication review) |

## Changes
Approved before this round: no. The two syncopes are no longer attributed definitively to orthostatic hypotension. Orthostatic hypotension stays the probable mechanism (both on standing, 32/20 mmHg fall with a heart-rate rise of 6/min). But the Holter captured only light-headedness, not a syncope, so it does not exclude a WPW-related arrhythmia. The must now asks for prompt cardiac electrophysiology review for accessory-pathway risk stratification, with ablation or further monitoring decided there. The 12-lead ECG is required and in the stop rule (ESC 2018: ECG in every syncope). A recommended electrophysiology study was added with a stored report. The report is invented for the benchmark (please check at re-review): single manifest right posteroseptal accessory pathway, anterograde ERP 310 ms, shortest pre-excited RR interval 300 ms in induced AF, no inducible AVRT, low-risk properties. The prohibition now reads 'Do not consider the syncope evaluation complete after a negative Holter'. The differential, evidence and red herrings say the same. WPW is a true coexisting condition and is no longer a rejected label, so 'PD; WPW syndrome' scores as correct while 'Wolff-Parkinson-White syndrome' alone does not (tested). The diagnostic must states that one supportive criterion counterbalances one red flag. Checks: perfect_agent passes, and so does test_case_guards.

## Verification
Pass 1: 0 errors found
- Checked: note 8352e97d applied as D21 (ECG required and in the stop rule, EPS recommended with a stored report, REQ[1], PRO[2], KCE[3], differential, both red herrings, WPW no longer rejected; 'PD with coexisting WPW' matches, 'Wolff-Parkinson-White syndrome' alone does not). The right posteroseptal pathway agrees with the stored ECG (delta waves positive in I and aVL, not in V1); the EPS report contains no management. Orthostatic values (26/16, 32/20 mmHg, HR +6) agree across exam, musts, evidence and differential. The OH is kept as a neurogenic red flag: no beta-blocker, so the heart-rate response (6/min for a 32 mmHg fall) is interpretable, unlike RP02. perfect_agent and test_case_guards pass.
- Cosmetic (not counted): none.
