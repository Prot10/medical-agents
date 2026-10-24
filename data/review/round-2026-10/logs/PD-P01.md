# PD-P01
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plans/PD.md (classes C1 to C22, per-case entry PD-P01, classes C7 and 3.3) and the July 2026 tool review. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.assessment.required_recommendations`, `metadata.clinical_notes`, `.teaching_points` | Label rested on a "poor levodopa response" although he has never had levodopa (C7). Clinically established MSA needs that response, so the case supports only clinically probable MSA-P. | FIXED: must "Diagnose clinically probable MSA-P (MDS 2022)", naming nOH, parkinsonism, early falls, erectile dysfunction before 60 and the putaminal MRI marker, and stating that levodopa responsiveness is still unknown; new must for a levodopa trial up to 1000 mg/day with lying and standing BP; notes and teaching points no longer claim a levodopa response or stridor. |
| A | major | `action-3-search-medical-literature`, `followup_outputs[0]` | Required literature criterion with an exact `query`; output cited a nonexistent "Koga 2023" and restated the policy (C1). | FIXED: criterion and follow-up deleted; literature initial and fallback null. |
| A | major | `action-2-check-drug-interactions`, `initial_tool_outputs.drug_interactions` | Exact `drug` argument; output listed his own drugs as "proposed" and had no interactions, so the review found nothing (C2). | FIXED: recommended, `{}`; single output (proposed carbidopa-levodopa): tamsulosin, lisinopril and sildenafil add to the orthostatic fall, PEG no interaction, midodrine warning (supine hypertension, no dose within 4 h of lying down), antimuscarinic warning; drug fallback null and dropped from `fallback_tool_kinds`. |
| A | major | `action-1-analyze-brain-mri`, `initial_tool_outputs.mri` | `{"contrast": false, "protocol": "standard"}` (C5). "Post-gadolinium" and "vascular parkinsonism" lines; impression ended in a "putaminal rim sign-associated neurodegenerative disorder" differential; "No features of NPH" (C12). | FIXED: `{}`, canonical label and rationale, `[Postuma_2015]` `[Wenning_2022]`, expected evidence from the report. Gadolinium and interpretive lines deleted. Impression numbered: MSA-P-compatible pattern, normal-ageing variant not excluded. |
| D | minor | `followup_outputs` MIBG | Impression with an em dash and hedged wording; `quantitative_data` null; long trigger name (C11). | FIXED: "Normal cardiac MIBG uptake (early H/M 2.15, delayed H/M 2.02, washout 28%)."; quantitative data filled; trigger `request_mibg`. Criterion stays optional, with its own rationale (preserved in MSA, reduced in PD). |
| B | major | `followup_outputs` (missing) | No stored DaTscan: the library normal scan is an MDS exclusion for any synucleinopathy and would contradict the label (C8). | FIXED: DaTscan `waste` (`avoid-waste-datscan`, "A DaTscan does not separate PD from MSA or PSP [Marshall_2009]"); stored C8 MSA-form report (bilateral, relatively symmetric, putamen and caudate; SBRs 0.94/0.99 and 1.62/1.70) with `request_datscan`, placed after the criteria-served outputs. |
| B | major | `followup_outputs` (missing) | Autonomic testing and tilt-table calls reached the library ("Normal ... No evidence of autonomic failure"), which contradicts the documented nOH. | FIXED: both added as waste with the plan 3.3 rationale; stored reports consistent with the exam (tilt fall 40/24 mmHg at 3 min, HR rise 7/min; cardiovagal and adrenergic failure; QSART normal). A stored orthostatic BP report (`request_orthostatic_bp`) restates the exam values and adds a 3-minute reading. |
| B | minor | `followup_outputs` (missing) | Exam MoCA 25/30 with Trail Making B and phonemic fluency errors against the library's normal battery (C9). | FIXED: stored battery (impaired TMT-B and FAS, preserved memory, naming and visuospatial function, GDS 4/15); no criterion. |
| B | minor | `patient.history_present_illness` | "civil engineer ... difficulty concentrating at work" against social history "retired civil engineer". | FIXED: "retired civil engineer"; "difficulty concentrating when reading". |
| C | major | `ground_truth.differential` | PD with autonomic features `high`, PSP `moderate`, no ICD codes, while the exam and MRI argue against both (C13). | FIXED: PD `low` (three MDS 2015 red flags, no supportive criterion); PSP `low` (no vertical gaze palsy, midbrain 130 mm2); DLB, vascular `low`; DIP `very_low`; ICD codes added. |
| C | minor | `prohibited_recommendations` | Generic templates. | FIXED: canonical D2 prohibition (C16); no further drugs that worsen orthostatic hypotension; no antimuscarinic before the post-void residual is known. |
| C | minor | `required_recommendations` | No orthostatic, bladder or falls management. | FIXED: nOH must (review tamsulosin, daytime lisinopril and sildenafil, non-drug measures, midodrine or droxidopa with supine monitoring); post-void residual before any prostate surgery; physiotherapy and multidisciplinary follow-up. |
| B | major | `red_herrings` | Metoclopramide exposure (he denies it) and "asymmetric onset" (the exam is symmetric) (C14). | FIXED: replaced with BPH on tamsulosin as the explanation of the bladder symptoms (`past_medical_history[1]`) and lisinopril as the explanation of the orthostatic hypotension (`past_medical_history[5]`). |
| D | major | `key_clinical_evidence` | Claimed a levodopa response; generic lines. | FIXED: seven lines from the exam, history and MRI, ending with "no levodopa trial yet". |
| A | minor | `fallback_tool_outputs.echo`, `.ecg`, `.ct`, `.eeg` | No `echo_type`; ECG rate 67 against HR 68 and generic text; CT "benign" granuloma; EEG impression named a theta variant with no finding (C17). | FIXED: TTE with concrete text; ECG 66/min concrete; CT "likely an old granuloma"; EEG impression plain normal. |
| B | minor | `avoided_actions`, `sequence_constraints`, `stop_rule` | Generic rationales (the ECG one claimed a "regular pulse" not recorded); stop rule listed literature and drug ids (C20). | FIXED: case-specific rationales; stop rule MRI only, allowance 2; no sequence constraint (no DaTscan criterion). |
| E | minor | `metadata` | Citation gap named Gilman 2008 and other packs; shared engineering text (C19). | FIXED: citation gap names `[Wenning_2022]` only; difficulty rationale, revision reason and clinical notes describe the edited case; 2026-10-24. `case_body_concerns` kept. |
| - | check | plan 3.6 | perfect_agent ok (MRI initial, drug review initial); case_io check: no failure names PD-P01; test_case_guards pass; discriminator_defects empty. Routing: DaTscan, MIBG, battery, orthostatic BP, autonomic testing and tilt serve the case; PSG, amyloid, FDG, genetics and labs the library; drug calls for any agent serve the case output. | - |

## Changes, in one paragraph a physician can read before re-reviewing

A 60-year-old man has 18 months of symmetric bradykinesia and rigidity without rest tremor. He has had four backward falls, symptomatic neurogenic orthostatic hypotension (34/26 mmHg at 1 minute, heart rate up only 4/min), urgency with incomplete emptying, erectile dysfunction from 57 and an MSA-pattern putaminal MRI. The label is now clinically probable MSA-P (MDS 2022): he has never had levodopa, so the earlier "poor levodopa response" was removed and a levodopa trial is now a must. The policy keeps MRI required (any protocol) and a medication review recommended. That review now names the drugs on his list that worsen the orthostatic fall: tamsulosin, lisinopril and sildenafil. Cardiac MIBG stays optional and its report is now binary (normal). The literature step is gone. DaTscan, autonomic testing and tilt testing are waste, but each has a stored report that matches the case. The musts add orthostatic management, a post-void residual before any prostate surgery, and falls and multidisciplinary care. PD and PSP are now low. The red herrings are now the prostate and lisinopril explanations that the history itself offers.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[Wenning_2022]` (MDS 2022 MSA criteria) and `[NICE_NG71]` are not yet in the PD criteria pack.
- Plan R6: the diagnosis ICD is G90.3 (`icd_codes[0]`, not changed here); ICD-10-CM codes MSA-P as G23.2. Please align the synonyms entry and `icd_codes`.
- Library: the `autonomic_testing` and `tilt_table` defaults say "no autonomic failure". A case with documented orthostatic hypotension must store its own report, as this one now does; a guard for this could catch the others.

## Open questions for Andrea (judgment calls you could not settle)

- Plan Q1: the case keeps its PD prefix with an MSA-P label (`metadata.case_body_concerns`); re-prefixing changes `case_id` and is outside this round.
- Should the medication review be required rather than recommended? Tamsulosin, lisinopril and sildenafil each worsen the nOH that has already caused near-syncope. I followed the plan (recommended): no D2 blocker is involved, and the nOH must already asks for the same review.

## Verification

Adversarial verifier, 24 Oct 2026. No PD notes file. Read the whole final case and the diff. Patient changes ("retired", "when reading") match the social history and are logged. Checked against MDS 2022: autonomic dysfunction (34/26 mmHg at 1 minute), parkinsonism, supportive features (postural instability with falls within 3 years, erectile dysfunction at 57, jerky irregular postural tremor), no levodopa trial, so clinically probable MSA-P is the right category and "poor levodopa response" appears nowhere as a fact. Arithmetic of the stored orthostatic, tilt and autonomic reports (38/28 and 40/24 mmHg falls, heart-rate rises 6 and 7/min, ratio 0.16) agrees with the exam and vitals; QSART normal fits preganglionic failure; MIBG binary and normal; DaTscan stored in the symmetric MSA form; red herrings now real case data; PD red-flag count (three) correct. All logged FIXED rows hold.

Found and changed:
- `initial_tool_outputs.mri.findings[1].signal_characteristics.T1_sagittal` said the cerebellar vermis and hemispheres "appear mildly reduced in volume", while the volumetrics (15th percentile), the impression and the MRI expected evidence say low normal, and the exam has no cerebellar sign. Rewritten "at the low end of normal volume".

Noted, not changed: the ECG stays waste (near-syncope 6 months ago was already evaluated, no palpitations or cardiac history); the worker's open question on the medication-review tier stands as logged. Checks after the verification edits: `perfect_agent.py -v` passes, `case_io.py check` names no failure for this case, `test_case_guards` pass.

## Condition audit

2026-10-24, PD condition auditor.

- `patient.neurological_exam.mental_status`: MoCA 25/30 named only two impaired items (trail-making B, phonemic fluency), worth 2 points at most. Now itemised: one point each on trail-making, serial subtraction, letter fluency, abstraction and delayed recall, which adds up to 25 and agrees with the MMSE losses (serial sevens, recall). The MoCA verbal fluency item is worth 1 point, abstraction 2, delayed recall 5, serial subtraction 3, clock 3 and trail-making 1, so the losses must be itemised within these maxima and add up to the stated total.

After the edits: `perfect_agent.py` 30/30 PD pass; every stored follow-up of the 30 cases is served for its own discriminator (MockServer probe); `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k PD-` 60 passed.

## Close-out (24 Oct 2026)

Decisions in `plans/PD-decisions.md`.

- Stays in condition parkinsons with its case id as a PD-mimic case (ROUND_POLICY ruling 3; orchestrator decision); `metadata.case_body_concerns` and `citation_gap` cleared (decided; `[Wenning_2022]` is in the pack). Primary code stays G90.3 (ICD-10-CM FY2026 codes MSA there). Synonyms: G23.2 added (WHO ICD-10 and ICD-10-GM MSA-P; ICD-10-CM striatonigral degeneration) and the label "striatonigral degeneration"; "MSA-P" and "multiple system atrophy parkinsonian type" now sit on a case-scoped entry. No PD label or G20 code is accepted; a plain Parkinson's disease answer does not score.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
