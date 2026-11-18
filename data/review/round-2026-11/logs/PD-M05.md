# PD-M05

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM) | Approved before this round: no

| note id | ruling | what changed, field paths |
| --- | --- | --- |
| b468a5e6-6b4b-4443-9059-26dda843bb31 | FIXED | patient.demographics.handedness 'right' became 'left'; patient.history_present_illness '69-year-old right-handed' became 'left-handed'; patient.neurological_exam.additional 'Handwriting sample shows micrographia, more pronounced with the left hand.' became 'Handwriting sample (left, dominant hand) shows micrographia.' Of the note's two options this is the clinically consistent one (plan D8). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C clinical | major | ground_truth.action_criteria[0] (action-1-analyze-brain-mri); ground_truth.stop_rule | MRI required and in the stop rule in clinically typical PD with no red flag (class TIER-MRI, plan D1) | FIXED (optional, D1 label and rationale [NICE_NG71][Postuma_2015]; required_before_assessment empty, max_additional_actions 2) |
| D leakage | minor | ground_truth.key_clinical_evidence[3], [4]; ground_truth.differential[0], [2], [3]; ground_truth.red_herrings[0].correct_interpretation | Evidence, differential and red herring rested on the now-optional MRI | FIXED (KCE[4] D1 form; other lines 'if imaged') |
| E language | minor | metadata.difficulty_rationale, revision_reason, last_revised | Counted '1 required criterion (MRI)' | FIXED |

## Changes
He is now left-handed, as his writing with the left hand and left-hand micrographia require; the exam names the handwriting sample as from his dominant left hand. Brain MRI is now optional and out of the stop rule: clinically typical PD with no red flag, NICE NG71 1.2.9. An agent that makes the clinical diagnosis earns full credit, and an MRI order is credited as optional. Evidence, differential and red-herring lines lead with clinical features and mention the MRI only 'if imaged'. Video-polysomnography stays recommended (violent dream enactment beside untreated sleep apnea). Checks: perfect_agent.py -v ok; test_case_guards.py for PD-M01, PD-M02, PD-M03, PD-M04, PD-M05 and PD-P01: 48 passed; case_io check: schema and synonym guard OK, the only failures naming PD are test_guidance_claims (maintained centrally, plan CENTRAL 3) and test_panel_case_contract on PD-RM05 (another worker's case). No MRI report edited (mri_probe run on M01: case MRI served). Not an approved case. Literature (class LIT): no literature criterion or stored literature output in the case (checked).

## Verification
Pass 1: 1 errors found
- F4: ground_truth.key_clinical_evidence[1] stated the UPSIT result of the optional olfactory-test criterion as fact (REQ[0] already said 'when tested'); it now reads 'UPSIT 16/40, if obtained'.
- Handedness (D8) checked across HPI, demographics and examination: consistent. D1 lines checked.
- Checks after the fixes: perfect_agent.py -v ok; test_case_guards.py -k for PD-M01..M05 and PD-P01: 48 passed; case_io check: schema and synonym guard OK, the only failures naming PD are test_guidance_claims (central, plan CENTRAL 3).
Pass 2: 0 errors found
- Re-checked note b468a5e6 (D8: left-handed in demographics, HPI and the handwriting sample; no other handedness mention in the file), D1 lines and F4 wording; served outputs. No change.
- Checks after pass 2: perfect_agent.py -v ok for all six; test_case_guards.py -k for PD-M01..M05 and PD-P01: 48 passed; case_io check: schema and synonym guard OK, the only failures naming PD are test_guidance_claims (central, plan CENTRAL 3: labs and ECG counts); mri_probe: the case MRI answers every MRI order.
Pass 3: 0 errors found
- Re-read the whole case against D1 and D8: left-handed in demographics, HPI and the handwriting sample; no other handedness mention; optional MRI, empty stop rule, 'if imaged' lines in KCE[3], KCE[4], differential [0], [2], [3] and red herring [0]; UPSIT 'if obtained' (optional criterion) and the recommended PSG result cited in REQ[2] and REQ[3] (allowed by F4); MDS 2015 count (one supportive criterion, no red flag: probable; validated anosmia would make it established); MoCA arithmetic (27/30); aspirin in the drug output is on the medication list. No change.
- Checks after pass 3: perfect_agent.py -v ok for all six (MRI served from the case slot, confirmed with mri_probe); test_case_guards.py -k for PD-M01..M05 and PD-P01: 48 passed; case_io check: schema and synonym guard OK, the only failures naming PD are test_guidance_claims (central, plan CENTRAL 3: labs and ECG counts).
