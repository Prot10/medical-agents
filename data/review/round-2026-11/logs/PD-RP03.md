# PD-RP03

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 722c125f-0a79-41ae-92e7-53e7eedc5d1b | FIXED (D11) | `assessment.required_recommendations[4]` canonical D11 conditional text with the RP03 clause (severe OH) [Wenning_2022]. `required_recommendations[0]` now says the MDS 2022 criteria are met through the cerebellar route as well, so levodopa resistance need not be proven. |
| 8069f8d7-f9ef-4d36-a91e-9923071e7b87 | FIXED (D23) | The note is anchored on REQ[3]; its target is REQ[2]. In `assessment.required_recommendations[2]`, 'review tamsulosin and stop daytime amlodipine' is replaced by an individual review of amlodipine 10 mg, tamsulosin and propranolol with his cardiologist (coronary disease, supine hypertension 148/90 mmHg), with supine and standing pressure at each change. The propranolol taper is kept, conditional on cardiology confirming no coronary indication. The rest of REQ[2] is unchanged. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | `ground_truth.diagnosis.rejected` | `essential tremor` was rejected although the differential says the old ET 'may coexist': an answer naming MSA with a prior ET would have been vetoed (D30 rule). ET alone cannot match the MSA labels | FIXED: removed; tested that 'MSA ... with a prior essential tremor' matches and 'Essential tremor' and 'Parkinson's disease' do not |

## Changes
Approved before this round: no. Further levodopa titration is no longer a mandatory 'trial toward 1000 mg/day'. It is conditional on possible benefit and tolerance, with lying and standing BP at each step given the severe OH, and tapered slowly if there is no benefit. It is not needed for the diagnosis and must not delay fall prevention or the swallowing assessment. The diagnostic must says clinically established MSA is reached through the cerebellar route as well, so levodopa resistance does not need to be proven. The OH must no longer stops daytime amlodipine outright: amlodipine 10 mg, tamsulosin and propranolol are reviewed individually with his cardiologist, given his coronary disease and supine hypertension, with supine and standing pressure monitored at each change. Essential tremor is no longer a rejected label, because the differential allows it to coexist. MRI stays required (MDS 2022 MRI markers). Checks: perfect_agent passes, and so does test_case_guards.

## Verification
Pass 1: 0 errors found
- Checked: both notes applied as D11 and D23; ET removal from rejected is correct (the differential lets it coexist; 'MSA with prior essential tremor' matches, 'Essential tremor' does not). The neurogenic OH on propranolol is acknowledged in KCE[2] and the drug-contribution differential and rests also on supine hypertension, urge incontinence, stridor and the MRI markers, so it is not the RP02 situation. perfect_agent and test_case_guards pass.
- Cosmetic (not counted): `required_recommendations[0]` run-on sentence repaired (the cerebellar-route clause moved to the end, before the citation); content unchanged.
