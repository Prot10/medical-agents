# PD-RS05

## Reviewer notes
Reviewer status: R1 in_progress | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 7d906e55-4818-4eaa-b036-d819fc5c57ec | FIXED (D1) | `ground_truth.action_criteria[0]` required -> optional, label 'Consider brain MRI only if an atypical feature or another structural question arises', rationale citing NICE NG71 and MDS 2015 (citations now [NICE_NG71], [Postuma_2015]; [Schwarz_2014] dropped with the old rationale); `ground_truth.stop_rule.required_before_assessment` -> []; `ground_truth.key_clinical_evidence[4]` D1 form; `ground_truth.differential[3]`, `[4]`, `[5]` key_features with MRI as 'and, if imaged' |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | ground_truth.key_clinical_evidence[2], [1] | The optional UPSIT result (25/40) was stated as established fact and KCE[1] said 'clinically probable' without the condition (plan F4) | FIXED ('if a smell identification test is obtained'; KCE[1] 'unless a validated smell test adds a second supportive criterion') |
| B | minor | metadata.difficulty_description, metadata.difficulty_rationale | 'with a normal brain MRI' and '1 required criterion (MRI)' | FIXED |
| B | minor | metadata.revision_reason, metadata.last_revised | Updated | FIXED |
| - | - | whole case | Checked: MoCA 28 subscores, DaTscan laterality, drug output agrees with codeine allergy and medications, no literature output, no gadolinium MRI | no change |

## Changes
The brain MRI is now optional and no longer required before the diagnosis: this is clinically typical asymmetric rest-tremor PD with no red flag (NICE NG71 1.2.9), so the case has no required test. The MRI evidence line and the vascular-parkinsonism, MSA and PSP differential entries now argue from the clinical findings, mentioning the MRI only 'if imaged'. The smell-test evidence now says that the UPSIT result upgrades probable to clinically established PD only if the (optional) test is obtained. Metadata no longer calls the MRI part of the pathway. Musts, prohibitions and reports are unchanged.

## Verification
perfect_agent.py -v: ok; mri_probe.py: plain MRI only, no gadolinium content; test_case_guards.py -k (6 cases): 48 passed; case_io.py check: schema and synonym guard OK, no failure names this case (remaining failures: test_guidance_claims PD rows, central, and PD-RM05 zero-cost required set, another worker's case).

Pass 1: 0 errors found
- Re-read the notes, rulings, plan entries and the diff, and read the final case in full. Every note has a correct FIXED ruling, and the edits match the plan's canonical text. No contradiction (laterality, orthostatic figures, MoCA subscores, medications against the drug output, rejected labels against the differential), no leakage, no stop-rule or sequence id error. No material error.
- Cosmetic (not counted): none.
- Checks re-run by the verifier: perfect_agent.py -v ok; mri_probe.py plain MRI only; test_case_guards -k (6 cases) 48 passed; case_io.py check schema and synonym guard OK, the only failures are the central test_guidance_claims PD rows (labs, ECG).
