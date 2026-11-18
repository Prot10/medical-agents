# PD-RM04

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 23ea4603-bba3-476f-924e-c64cd9855125 | FIXED (D16) | `ground_truth.assessment.required_recommendations[1]` rewritten: shoulder stiffness at least partly parkinsonian rigidity, restricted active and passive range suggests coexisting adhesive capsulitis, reassess both after dopaminergic treatment, continue physiotherapy, orthopedic review if the restriction persists. `prohibited_recommendations[0]` (ban on further shoulder injections or capsular procedures) deleted. `diagnosis.rejected`: `adhesive capsulitis` and `frozen shoulder` removed (D30). `differential[0].key_features` (possibly coexisting, does not explain the parkinsonism; low), `key_clinical_evidence[1]`, `red_herrings[0].correct_interpretation` and `.intended_effect`, `metadata.key_confounding_factor` aligned. `patient.neurological_exam.motor`: passive abduction also limited, with a capsular end feel. |
| 92ca20f9-f0d6-42d5-ba55-87a4e151622f | FIXED (D5) | `patient.neurological_exam.motor`: 'progressive decrement in amplitude and speed on repetitive finger tapping, hand opening-closing and pronation-supination on the left, milder on the right'. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | `ground_truth.action_criteria[0]` (action-1-analyze-brain-mri), `stop_rule` | Clinically typical asymmetric rest-tremor PD with no red flag: MRI was required and in the stop rule, against NICE NG71 1.2.9 (class D1) | FIXED: optional, canonical D1 label and rationale, citations [NICE_NG71][Postuma_2015][Schwarz_2014]; stop rule empty, max_additional_actions 2 |
| C | minor | `ground_truth.key_clinical_evidence[3]` | Swallow-tail line read as diagnostic support, and MRI no longer required (D9, D1) | FIXED: D1 'if MRI is obtained' form with D9 non-specific wording |
| C | minor | `ground_truth.differential[4]`, `[5]`, `[6]` | Vascular parkinsonism, MSA and PSP excluded on MRI findings that are now optional | FIXED: clinical features first, MRI as 'and, if imaged, ...' |
| C | minor | `ground_truth.key_clinical_evidence[4]` | Cites UPSIT 21/40 from an optional criterion without 'if obtained' (F4) | FIXED: '(UPSIT 21/40, if obtained)' |
| B | minor | `metadata.difficulty_rationale` | Said '1 required criterion (MRI)' | FIXED: no required criterion |
| B | minor | `fallback_tool_outputs.specialized_test` | Fallback speech-language report gives Boston Naming 53/60 (normal) while the neuropsychological battery gives 24/30 on the 30-item version (mildly reduced). Both are mild, and the fallback is served only for a speech-language order | FLAGGED, not changed |

## Changes
Approved before this round: no. The brain MRI is now optional and has left the stop rule, because this is clinically typical PD without red flags (NICE NG71 1.2.9). The case has no required test: the correct answer is a clinical diagnosis. MRI-based evidence and differential lines now say 'if imaged'. The swallow-tail sign is stated as non-specific. The motor exam documents bradykinesia with progressive decrement and adds limited passive shoulder abduction with a capsular end feel. The shoulder must no longer attributes the whole shoulder disorder to PD. It now says the stiffness is partly parkinsonian rigidity and that a coexisting adhesive capsulitis is possible, with both reassessed after dopaminergic treatment while physiotherapy continues and orthopedics reviews if needed. The ban on further shoulder treatment is gone. Adhesive capsulitis and frozen shoulder are no longer rejected answers, so 'PD with coexisting adhesive capsulitis' scores as correct (tested with DiagnosisCriterion.matches). The differential, red herring and evidence lines agree. Checks: perfect_agent and mri_probe pass, and so do test_case_guards and test_panel_case_contract.

## Verification
Pass 1: 0 errors found
- Checked: both notes applied as D16 and D5 ask (shoulder must, PRO[0] deleted, rejected labels, differential, red herring, evidence, passive range and decrement in the exam); MRI optional and out of the stop rule (D1); D9 swallow-tail wording; no leakage in the patient block or the MRI report; coexisting adhesive capsulitis answer matches, 'Adhesive capsulitis' alone does not. perfect_agent, mri_probe and test_case_guards pass. The Boston Naming difference (53/60 on the 60-item speech-language fallback, 24/30 on the 30-item battery) is two versions of the test, both mild, and stays as flagged.
- Cosmetic (not counted): none.
