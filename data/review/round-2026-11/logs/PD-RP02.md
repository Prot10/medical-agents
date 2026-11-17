# PD-RP02

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| d6571979-2a68-4ef2-ba3c-a38b80c0b71d | FIXED (D22) | The note is anchored on REQ[1]; its text concerns REQ[0], the MIBG criterion and the evidence. `assessment.required_recommendations[0]` canonical D22 text (rest tremor is the one supportive criterion and enough for one red flag; no MIBG). `action_criteria[1]` (action-5-order-advanced-imaging, MIBG) recommended to optional, with new label and rationale ('may add support; not required and not definitive'). `key_clinical_evidence[2]` and `[4]` and `differential[0]` (MSA) cite the MIBG and UPSIT as 'if obtained'. |
| f4a8e329-6bfc-4f32-b39c-20cd00383c5a | FIXED (D22) | `key_clinical_evidence[1]`: 'severe; not classed as neurogenic or as a red flag until the beta-blocker is reviewed'. New must `assessment.required_recommendations[2]`: review metoprolol, flecainide and the AF regimen with cardiology, then repeat lying and standing BP and HR before classifying the OH as neurogenic. `differential[2]` (metoprolol-related OH): coexists and unresolved, likelihood low to moderate. REQ[1] keeps 'review metoprolol with his cardiologist'. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | `ground_truth.key_clinical_evidence[3]` | Swallow-tail line without its non-specificity (class D9) | FIXED: D9 canonical wording (MRI required here) |
| B | minor | `followup_outputs[8].output.impression` (autonomic_testing), `followup_outputs[9].output` (tilt_table) | The stored autonomic and tilt reports called the OH 'neurogenic' on the heart-rate response while metoprolol was not withheld, against the note | FIXED: impressions qualified for the beta-blocker; tilt finding 'metoprolol not withheld' added. Both orders remain waste |
| B | minor | `metadata.difficulty_description`, `metadata.difficulty_rationale` | Said the MIBG supplies the second supportive criterion; tier counts outdated | FIXED |

## Changes
Approved before this round: no. The diagnostic must now applies the MDS 2015 rule correctly: one red flag needs one supportive criterion, and the right-hand rest tremor already provides it. Whether the 42/30 mmHg orthostatic fall is the severe-autonomic-failure red flag cannot be decided while metoprolol may explain it and blunts the heart-rate response. A new must asks for a cardiology review of metoprolol, flecainide and the AF regimen, then repeat lying and standing BP and HR before the OH is called neurogenic. The evidence line, the metoprolol differential (now moderate, unresolved) and the stored autonomic and tilt reports (both waste orders) say the same. Cardiac MIBG is optional ('may add support; not required and not definitive'), and lines citing it read 'if obtained'. The swallow-tail sign is stated as non-specific. The label 'PD with early prominent autonomic failure' is unchanged (no note on it). Checks: perfect_agent passes, and so does test_case_guards.

## Verification
Pass 1: 0 errors found
- Checked: both notes applied as D22 (REQ[0] one supportive criterion, OH not classed as neurogenic or a red flag on metoprolol, new cardiology must, MIBG optional with 'if obtained' lines, autonomic and tilt reports qualified); D9 swallow-tail wording; no remaining 'neurogenic' claim about this patient's OH outside the general midodrine warning of the drug report; PRO[1] domperidone with flecainide kept (D4). perfect_agent and test_case_guards pass. The label 'PD with early prominent autonomic failure' stays (no note on it; constipation and RBD remain).
- Cosmetic (not counted): none.
