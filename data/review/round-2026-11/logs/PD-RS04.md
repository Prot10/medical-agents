# PD-RS04

## Reviewer notes
Reviewer status: R1 in_progress | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 9d6d3209-37ba-49c1-b7cb-0e37160624e2 | FIXED (D1) | `ground_truth.action_criteria[0]` importance required -> optional, label 'Consider brain MRI only if an atypical feature or another structural question arises', rationale citing NICE NG71 and MDS 2015; `ground_truth.stop_rule.required_before_assessment` ['action-1-analyze-brain-mri'] -> []; `ground_truth.key_clinical_evidence[3]` D1 'if MRI is obtained' form; `ground_truth.differential[2]` (vascular) and `[3]` (MSA) key_features lead with clinical features, MRI as 'and, if imaged' |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| B | minor | metadata.difficulty_description, metadata.difficulty_rationale | Said 'with a normal brain MRI' (the MRI shows Fazekas 1 foci and is no longer in the pathway) and '1 required criterion (MRI)' | FIXED |
| B | minor | metadata.revision_reason, metadata.last_revised | Updated to describe the case as edited (2026-11-16) | FIXED |
| C | minor | initial_tool_outputs.labs.panels (Glucose 156, HbA1c 7.8) | Abnormal rows carry null clinical_significance (shown as 'none'); known treated diabetes, not raised by a reviewer, no management gap | FLAGGED (display, CENTRAL) |
| - | - | whole case | Checked: MoCA subscores sum to 24, orthostatic fall 8/4, DaTscan left-putamen deficit opposite the right-predominant signs, no literature output left (class LIT), no gadolinium MRI (MRI-CONTRAST n/a) | no change |

## Changes
The brain MRI is now optional and no longer has to be done before the diagnosis is submitted: this is clinically typical, asymmetric rest-tremor PD with no red flag, so the diagnosis is clinical (NICE NG71 1.2.9). The case therefore has no required test; an agent that diagnoses probable PD from the examination and gives the musts scores fully, while unjustified orders beyond two are still penalised. The MRI evidence line and the vascular-parkinsonism and MSA differential entries now argue from the clinical findings and mention the MRI only as 'if imaged'. The metadata description no longer calls the MRI normal. Nothing else changed (musts, prohibitions, reports, avoided actions as before).

## Verification
perfect_agent.py -v: ok; mri_probe.py: plain MRI only, no gadolinium content; test_case_guards.py -k (6 cases): 48 passed; case_io.py check: schema and synonym guard OK, no failure names this case (remaining failures: test_guidance_claims PD rows, central, and PD-RM05 zero-cost required set, another worker's case).

Pass 1: 0 errors found
- Re-read the notes, rulings, plan entries and the diff, and read the final case in full. Every note has a correct FIXED ruling, and the edits match the plan's canonical text. No contradiction (laterality, orthostatic figures, MoCA subscores, medications against the drug output, rejected labels against the differential), no leakage, no stop-rule or sequence id error. No material error.
- Cosmetic (not counted): none.
- Checks re-run by the verifier: perfect_agent.py -v ok; mri_probe.py plain MRI only; test_case_guards -k (6 cases) 48 passed; case_io.py check schema and synonym guard OK, the only failures are the central test_guidance_claims PD rows (labs, ECG).
