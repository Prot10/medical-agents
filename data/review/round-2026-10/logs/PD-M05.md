# PD-M05
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plans/PD.md (classes C1 to C22, per-case entry PD-M05) and the July 2026 tool review. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `required_recommendations[0]`, `key_clinical_evidence` | "Clinically established PD" with "olfactory loss and PSG-confirmed RBD" as the two supportive criteria: RBD is a prodromal marker and the anosmia is self-reported, so at most one supportive criterion (rest tremor) is present (C6, F1). | FIXED: must "Diagnose clinically probable PD (MDS 2015) ..." naming RBD and smell loss as prodromal markers; constipation no longer "supportive". |
| B | minor | `patient.neurological_exam.motor` | "Minimal resting tremor ... during sustained posture": a rest tremor cannot be seen during posture. | FIXED: "Minimal 4 Hz rest tremor of the left hand seen on one occasion with the hand resting in the lap". |
| B | major | `key_clinical_evidence[3]`, `[4]` | "Normal autonomic battery" and "normal cognition on neuropsych battery": neither test is in the case (C15). | FIXED: deleted; evidence restates patient data, the MRI and the PSG only. |
| A | major | `action-2-search-medical-literature`, `followup_outputs[0]` | Required literature criterion with an exact `query`; summary restating the policy (C1). | FIXED: criterion and follow-up deleted; literature initial and fallback null; removed from the stop rule. |
| A | major | `action-3-check-drug-interactions`, `followup_outputs[1]` | Required with exact arguments, no dopamine blocker on the list (ruling 6); output with agonist and MAO-B "alternatives", antipsychotic advice and a "none currently prescribed in this case" contraindication block (C2). | FIXED: optional, `{}`; single output `initial_tool_outputs.drug_interactions.general` (amlodipine and orthostasis, no D2 blocker, clonazepam with untreated OSA, sulfonamide allergy not relevant); follow-up deleted; fallback null. |
| C | major | `action-4-order-specialized-test` | PSG optional with generic expected evidence, although violent dream enactment injured his wife, the study was deferred, and his known OSA is an RBD mimic (plan M05). | FIXED: recommended; label, rationale (`[Berg_2015]`) and expected evidence from the report; trigger `request_sleep_study`. |
| D | minor | PSG follow-up | RSWA stated as "Present" against a non-existent "AASM <30%" threshold; no statement on respiratory events (C10). | FIXED: RSWA 46% of REM epochs against the SINBAR 27% threshold; video behaviors "none preceded by an apnea, hypopnea or respiratory arousal"; AHI 7.2 (mild OSA), SpO2 nadir 91%, PLMI 11; C10 impression. |
| A | major | `action-1-analyze-brain-mri.alternatives`, `initial_tool_outputs.mri` | `{"contrast": false, "protocol": "standard"}` (C5); MRA line on a standard protocol, "no abnormal enhancement" without contrast, "to suggest vascular parkinsonism" (C12). | FIXED: `{}`, canonical label and rationale, `[Postuma_2015]` (no SWI nigrosome finding); MRA, enhancement and interpretive wording deleted. |
| B | major | `followup_outputs` (missing) | No stored DaTscan: the library default (normal) is an MDS absolute exclusion and would contradict the label (C8). | FIXED: stored C8 binary report (right putamen 0.98, left 1.33, contralateral to the worse left side) with `request_datscan`; DaTscan `waste` (`avoid-waste-datscan`, NICE NG71: the clinical diagnosis is clear). Placed last in the follow-up list because no criterion orders it. |
| B | minor | `followup_outputs` (missing) | Exam MoCA 27/30 against the library battery's 28/30 (C9). | FIXED: stored battery within normal limits (MoCA 27/30, low-average phonemic fluency, GDS 4/15); no criterion. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts (apply criteria, review drugs, "initiate levodopa or agonist"); no RBD or OSA management (C16). | FIXED: four musts: probable PD; levodopa start with the agonist warning (69); RBD treatment with bed-partner safety and melatonin before clonazepam (untreated OSA); readdress the OSA (CPAP or positional therapy). |
| C | minor | `prohibited_recommendations` | Overlapping antipsychotic and antiemetic templates with em dashes. | FIXED: canonical D2 prohibition; MSA/DLB overcall prohibition rewritten from the case's data; anticholinergic prohibition kept. |
| C | major | `ground_truth.differential` | MSA-P and DLB `moderate` after a work-up and history that exclude them (C13); MSA entry cited "preserved blood pressure responses" not measured. | FIXED: MSA, DLB, PSP and vascular `low` with excluding data; DIP `very_low`. |
| B | minor | `red_herrings` | Location "initial_tool_outputs.specialized_test" and path `followup_outputs[2].output.findings` pointing at the wrong stored outputs (C14). | FIXED: akinetic-rigid phenotype (`neurological_exam.motor`); OSA repointed to `past_medical_history[3]`; added the rotator cuff repair (`past_medical_history[4]`), to which he first attributed the stiffness. |
| A | minor | `fallback_tool_outputs.advanced_imaging`, `.echo`, `.cardiac_monitoring`, `.ecg` | Amyloid fallback "does not resolve the current diagnostic question" (C11); no `echo_type`; Holter "only benign incidental findings" (C17). | FIXED: amyloid fallback null (waste entry kept); TTE with concrete text; Holter impression names the premature atrial complexes; ECG text concrete; `fallback_tool_kinds.cardiac_monitoring` "normal". |
| B | minor | `avoided_actions`, `stop_rule` | Generic rationales; `max_additional_actions` 0; stop rule listed literature and drug ids (C20). | FIXED: case-specific rationales; DaTscan, autonomic and tilt waste added; stop rule MRI only, allowance 2; no sequence constraint (no DaTscan criterion). |
| E | minor | `metadata.primary_teaching_point`, `.difficulty_rationale`, `.revision_reason`, `.last_revised` | Teaching point called hyposmia a marker to "recognise"; shared engineering text (C19). | FIXED: describe the edited case; 2026-10-24. |
| - | check | plan 3.6 | perfect_agent ok (MRI initial, PSG `request_sleep_study`); case_io check: no failure names PD-M05; test_case_guards pass; discriminator_defects empty. Routing: DaTscan, PSG and battery serve the case; MIBG, amyloid and FDG the library; drug calls for levodopa and rasagiline serve the case output. | - |

## Changes, in one paragraph a physician can read before re-reviewing

A 69-year-old man with left-predominant akinetic-rigid parkinsonism, a minimal rest tremor, 2.5 years of violent dream enactment, self-reported anosmia, constipation and known untreated mild OSA. The label is now clinically probable PD, not established: RBD is a prodromal marker and an unmeasured smell loss is not a supportive criterion, so only the rest tremor counts. The policy is MRI required (any protocol) and video-PSG recommended (violent RBD, OSA as its mimic, a deferred study), with an optional medication review; literature is gone and a DaTscan is waste (the clinical diagnosis is clear), though a stored abnormal scan answers it. The PSG now quantifies RSWA (46% of REM epochs) and states that the behaviors are not linked to respiratory events beside mild OSA (AHI 7.2). The evidence no longer cites an autonomic battery or neuropsychology that the case never contained. The musts add levodopa with the agonist warning, RBD treatment with bed-partner safety (melatonin first because clonazepam can worsen his apnoea) and renewed OSA treatment. MSA-P and DLB are now low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[NICE_NG71]` is not yet in the PD criteria pack.
- Plan R4: the anosmia is only self-reported; an `olfactory_test` term would let a validated smell test add a supportive criterion.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case (plan Q1 to Q6 apply).

## Verification

Adversarial verifier, 24 Oct 2026. No PD notes file. Read the whole final case and the diff. The only patient change is the rest-tremor sentence (a rest tremor cannot be seen during sustained posture), which is a real error and now reads correctly. Checked: probable PD with RBD and self-reported smell loss as prodromal markers only; no "autonomic battery" or "neuropsych" evidence remains; PSG recommended and served by the case report (RSWA 46%, behaviours not linked to respiratory events, AHI 7.2); musts that rest on the PSG cite a recommended criterion; laterality (worse left, right putaminal SBR 0.98 on the stored waste DaTscan); red-herring paths point at the right PMH indices; MRA and enhancement lines gone; stop rule MRI only, no sequence constraint (no DaTscan criterion). All logged FIXED rows hold.

Found: nothing that needed a change. Checks after the verification edits: `perfect_agent.py -v` passes, `case_io.py check` names no failure for this case, `test_case_guards` pass.

## Condition audit

2026-10-24, PD condition auditor.

- `patient.neurological_exam.mental_status`: "two points on letter fluency" exceeded the 1-point fluency item. Now one point each on letter fluency, abstraction and delayed recall (27/30), consistent with the low-average FAS and preserved memory on the battery. The MoCA verbal fluency item is worth 1 point, abstraction 2, delayed recall 5, serial subtraction 3, clock 3 and trail-making 1, so the losses must be itemised within these maxima and add up to the stated total.

After the edits: `perfect_agent.py` 30/30 PD pass; every stored follow-up of the 30 cases is served for its own discriminator (MockServer probe); `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k PD-` 60 passed.

## Close-out (24 Oct 2026)

Decisions in `plans/PD-decisions.md`.

- Accepted codes are now G20.A1 (PD without dyskinesia, without mention of fluctuations; also PD NOS) and G20; G20.A2, G20.B1, G20.B2 (motor complications the case does not have) and G20.C ("Parkinsonism, unspecified", not PD) are no longer accepted. Labels unchanged.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Batch-5 vocabulary (25 Oct 2026)

Commit c02f3050 added `cysticercosis_serology`, `IGRA` (interpret_labs), `olfactory_test` (order_specialized_test) and `levodopa_challenge` (perform_clinical_assessment); `HBV_DNA` (interpret_labs) was added the same day for this round. The requests are now wired into the case.

- New optional criterion `olfactory-test` (`order_specialized_test {test_type: olfactory_test}`, `action_criteria[2]`, before the medication review) and its follow-up `request_olfactory_test_upsit` (`followup_outputs[3]`): UPSIT 16/40, in the anosmic range, below the normal range for age and sex. Before, an olfactory order got the library's normosmia (35/40), which contradicts the smell loss in the history. Optional: the test can add an MDS supportive criterion but changes no management. No scoring change for an agent that does not order it.
- `ground_truth.assessment.required_recommendations[0]`: rewritten so the smell loss counts as a supportive criterion once a validated test confirms it (UPSIT 16/40), instead of saying it cannot be tested.
- `ground_truth.key_clinical_evidence[1]`: rewritten so the smell loss counts as a supportive criterion once a validated test confirms it (UPSIT 16/40), instead of saying it cannot be tested.
- `ground_truth.key_clinical_evidence[5]`: rewritten so the smell loss counts as a supportive criterion once a validated test confirms it (UPSIT 16/40), instead of saying it cannot be tested.
