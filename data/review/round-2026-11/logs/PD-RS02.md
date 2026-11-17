# PD-RS02

## Reviewer notes
Reviewer status: R1 in_progress | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 0d17ed0e-8fa2-4edf-8aca-bdbefb964bba | FIXED (D27) | `ground_truth.assessment.prohibited_recommendations[1]` D27 canonical; `ground_truth.red_herrings[0].correct_interpretation` (no longer 'shunt failure would enlarge the ventricles and cause headache ... or a gait apraxia'); `ground_truth.differential[0]` key_features with the caveat, likelihood very_low -> low; `ground_truth.key_clinical_evidence[2]` aligned |
| 6029713d-ef69-49b2-8f82-cf3380c1a7b6 | FIXED (D27) | `ground_truth.assessment.required_recommendations[1]` D27 canonical (pre-MRI device verification, post-MRI check and reprogramming) |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| B | minor | metadata.difficulty_description, metadata.difficulty_rationale | Said the MRI 'answers' shunt failure (categorical) | FIXED ('makes unlikely'; programmable-valve question noted) |
| B | minor | metadata.revision_reason, metadata.last_revised | Updated | FIXED |
| A | minor | initial_tool_outputs.mri.contrast_used | Null on a plain study (shown as 'none'); no gadolinium content, so not in the MRI-CONTRAST class | FLAGGED (display) |
| - | - | whole case | MRI stays required (VP shunt, plan C1). Checked: MoCA 27 subscores, battery, DaTscan laterality, drug output, no literature output | no change |

## Changes
The shunt prohibition no longer claims that shunt failure necessarily enlarges the ventricles or causes headache: shunt revision is not to be arranged without evidence of malfunction, normal ventricles (Evans 0.27) without headache, nausea or visual symptoms make shunt failure unlikely but do not completely exclude it, and the MRI is compared with previous surveillance imaging with neurosurgical review if symptoms or findings raise concern. The red herring, the shunt-failure differential (now low rather than very low) and the evidence line say the same. The shunt must now asks, before the MRI, for the valve model, its MR conditional status and programmability and the current setting, and after the MRI for a check and reprogramming per the manufacturer's protocol. The MRI stays required because of the shunt; PD remains the diagnosis.

## Verification
perfect_agent.py -v: ok; mri_probe.py: plain MRI only, no gadolinium content; test_case_guards.py -k (6 cases): 48 passed; case_io.py check: schema and synonym guard OK, no failure names this case (remaining failures: test_guidance_claims PD rows, central, and PD-RM05 zero-cost required set, another worker's case).

Pass 1: 0 errors found
- Re-read the notes, rulings, plan entries and the diff, and read the final case in full. Every note has a correct FIXED ruling, and the edits match the plan's canonical text. No contradiction (laterality, orthostatic figures, MoCA subscores, medications against the drug output, rejected labels against the differential), no leakage, no stop-rule or sequence id error. No material error.
- Cosmetic (not counted): none.
- Checks re-run by the verifier: perfect_agent.py -v ok; mri_probe.py plain MRI only; test_case_guards -k (6 cases) 48 passed; case_io.py check schema and synonym guard OK, the only failures are the central test_guidance_claims PD rows (labs, ECG).
