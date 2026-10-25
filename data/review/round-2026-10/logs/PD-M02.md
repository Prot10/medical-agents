# PD-M02
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plans/PD.md (classes C1 to C22, per-case entry PD-M02) and the July 2026 tool review. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `action-3-search-medical-literature`, `followup_outputs[1]` | Required literature criterion with an exact `query`; output with a case-specific stepwise "approach" summary and a Berg "Nature Reviews Neurology 2021" citation not in the pack (C1). | FIXED: criterion and follow-up deleted, removed from the stop rule; literature initial and fallback null. |
| A | major | `action-2-check-drug-interactions`, `followup_outputs[0]` | Exact `drug`/`current_medications` arguments; output with "proposed: assessment of metoclopramide interactions", a case-diagnostic sentence ("regardless of the final diagnosis (PD vs DIP vs metoclopramide-unmasked PD)") and a prognostic rule (C2, style guide). | FIXED: `check_drug_interactions {}`, required; single output `initial_tool_outputs.drug_interactions.general` (metoclopramide C2 sentence, glipizide absorption with prokinetic changes, lisinopril with levodopa, EU contraindication with levodopa, boxed warning, domperidone QT, erythromycin QT and atorvastatin CYP3A4); follow-up deleted, fallback null. |
| A | major | `action-1-analyze-brain-mri.alternatives` | `{"contrast": false, "protocol": "standard"}` (C5). | FIXED: `{}`, canonical label and rationale, `[Postuma_2015]`. |
| C | major | `action-5-order-advanced-imaging.importance` | DaTscan optional while the label rests on it (C8). | FIXED: required, case-specific text, in the stop rule, trigger `request_datscan`. |
| D | minor | DaTscan follow-up | Prose "signal" block, em dash in the impression, no tracer or ratios. | FIXED: C8 binary report with SBRs (left putamen 1.12, right 1.36, caudates preserved); laterality checked (left deficit opposite the worse right side). |
| C | major | `initial_tool_outputs.mri` | Evans 0.31 called "upper limit of normal" and "ventricular enlargement ... ex vacuo"; "No abnormal enhancement following gadolinium" on a non-contrast study (C12). | FIXED: Evans 0.28 in the finding and a volumetrics block; finding "Ventricles proportionate to sulci"; gadolinium line deleted; numbered impression. |
| C | major | PSG follow-up | "Abnormal values" impression with inverted flags; RSWA reference "<15%"; video behaviour and sleep efficiency (72%) identical to PD-M01 (template carry-over) (C10). | FIXED: full report with SINBAR reference, sleep efficiency 68%, video "three episodes of kicking and arm movements with shouting" (matches the wife's "kicking and flailing"), AHI 3.8 (no OSA), SpO2 nadir 91%, PLMI 17; C10 impression; trigger `request_sleep_study`; criterion stays optional, rationale cites `[Berg_2015]`. |
| B | major | `followup_outputs` (missing) | Exam MoCA 25/30 against the library battery's MoCA 28/30 (C9). | FIXED: stored battery matching the MoCA losses (Trail Making B and Rey figure copy impaired, delayed recall low average with normal recognition, GDS 7/15 for the reported low mood); no criterion. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts; "premotor features (RBD, constipation, hyposmia) preceding metoclopramide" although her RBD (18 months) and smell loss (12 months) began after it (24 months) (C6, C15, C16). | FIXED: six musts: C6 M02 diagnostic must ("RBD and hyposmia are not drug effects"), stop metoclopramide with the gastroenterologist and glucose monitoring on glipizide, reassess after withdrawal, levodopa start with the agonist warning (age 64), assess and treat the low mood and anhedonia, RBD bed safety. |
| C | minor | `prohibited_recommendations` | Overlapping antiemetic and antipsychotic prohibitions. | FIXED: canonical D2 prohibition; levodopa-with-metoclopramide and anticholinergic prohibitions kept. |
| C | major | `ground_truth.differential` | DIP `high`, vascular `moderate` after the work-up (C13); no DLB entry although RBD and parkinsonism raise it; ET `very_low` despite a postural tremor and an affected brother. | FIXED: DIP `low` coexisting contributor; vascular, MSA, NPH, PSP `low` with excluding data; ET `low` "may coexist"; DLB `low` added. |
| D | major | `key_clinical_evidence` | "July 2026" engineering lines (C4); "symmetric onset"; "premotor features predate metoclopramide" (C15). | FIXED: seven case-specific lines, with the timeline stated as it is (RBD and smell loss after the drug; constipation before it but confounded). |
| B | minor | `red_herrings` | Interpretation repeated the "preceding" claim; generic paths. | FIXED: metoclopramide (`medications[0]`); brother's ET and her postural tremor (`family_history[2]`). |
| B | minor | `avoided_actions`, `sequence_constraints`, `stop_rule` | One-phrase rationales; constraint cited Schwarz; `max_additional_actions` 0 (C20, 3.3). | FIXED: case-specific rationales; autonomic and tilt waste added; MRI before DaTscan soft; stop rule MRI, DaTscan, medication review; allowance 2. |
| A | minor | `fallback_tool_outputs.echo`, `.ecg` | No `echo_type`; ECG rate 58 against HR 73 (C17). | FIXED: TTE with concrete text; ECG "Sinus rhythm 73/min, normal axis and intervals, no ST change." |
| E | minor | `metadata.key_confounders`, `.educational_value`, `.difficulty_rationale`, `.revision_reason`, `.last_revised` | "Borderline ventricular enlargement" no longer true; "prodromal features" emphasis; shared engineering text (C19). | FIXED: confounders and educational value describe the edited case; difficulty and revision text per plan; 2026-10-24. |
| - | check | plan 3.6 | perfect_agent ok (MRI initial, DaTscan `request_datscan`, medication review initial); case_io check: no failure names PD-M02 (the only PD failure is the PD-P03 leak test, another worker's case); test_case_guards pass; discriminator_defects empty. Routing: DaTscan, PSG and battery serve the case reports; drug calls for levodopa and rasagiline serve the case output; orthostatic BP goes to the library (no orthostatic symptoms; not a criterion). | - |

## Changes, in one paragraph a physician can read before re-reviewing

A 64-year-old woman with right-predominant bradykinesia and rigidity without rest tremor after two years of metoclopramide for diabetic gastroparesis, with dream enactment for 18 months, smell loss for a year and low mood. The policy is MRI (required, any protocol), DaTscan (required: current D2-blocker exposure makes pure drug-induced parkinsonism the alternative to exclude) and medication review (required), with optional video-PSG; literature is gone. The MRI now gives Evans 0.28 with proportionate ventricles and no gadolinium line. The DaTscan reports left putamen 1.12 and right 1.36 with caudate sparing, binary impression. The PSG shows RSWA in 68% of REM epochs with kicking and arm movements on video and no sleep apnoea. A stored battery matches her MoCA 25 and records mild depressive symptoms. The musts now rest on the DaTscan and on RBD and smell loss being non-drug effects, explicitly not on their "preceding" the drug (both began after it); they add stopping metoclopramide with glucose monitoring on glipizide, reassessment after withdrawal, levodopa once it is stopped, the agonist warning, treatment of the low mood and RBD bed safety. Drug-induced and vascular parkinsonism are now low; ET may coexist.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[NICE_NG71]` is not yet in the PD criteria pack.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case (plan Q1 to Q6 apply).

## Verification

Adversarial verifier, 24 Oct 2026. No PD notes file. Read the whole final case and the diff. Patient block unchanged. Checked: RBD (18 months) and smell loss (12 months) after metoclopramide (24 months) are never called "preceding"; laterality (worse right, left putaminal SBR 1.12); MRI Evans 0.28 in finding, volumetrics, impression and evidence; PSG flags and C10 impression (AHI 3.8, no OSA); battery against MoCA 25 losses and the reported low mood (GDS 7/15); drug output names her own glipizide, atorvastatin (with erythromycin), lisinopril, metformin, omeprazole, acetaminophen; differential low; tiers and stop rule per plan. All logged FIXED rows hold.

Found and changed:
- `avoid-waste-5-analyze-ecg` contradicted the must "domperidone where available after an ECG for the QTc" (same class as M01). Removed.

Noted, not changed: the MRI keeps a pre-existing "Normal substantia nigra signal on susceptibility-weighted imaging". A preserved nigrosome-1 is a recognised false negative in early PD, no field relies on it, and the DaTscan carries the diagnosis; changing it would be churn. Checks after the verification edits: `perfect_agent.py -v` passes, `case_io.py check` names no failure for this case, `test_case_guards` pass.

## Close-out (24 Oct 2026)

Decisions in `plans/PD-decisions.md`.

- Accepted codes are now G20.A1 (PD without dyskinesia, without mention of fluctuations; also PD NOS) and G20; G20.A2, G20.B1, G20.B2 (motor complications the case does not have) and G20.C ("Parkinsonism, unspecified", not PD) are no longer accepted. Labels unchanged.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Batch-5 vocabulary (25 Oct 2026)

Commit c02f3050 added `cysticercosis_serology`, `IGRA` (interpret_labs), `olfactory_test` (order_specialized_test) and `levodopa_challenge` (perform_clinical_assessment); `HBV_DNA` (interpret_labs) was added the same day for this round. The requests are now wired into the case.

- New optional criterion `olfactory-test` (`order_specialized_test {test_type: olfactory_test}`, `action_criteria[3]`, before the medication review) and its follow-up `request_olfactory_test_upsit` (`followup_outputs[3]`): UPSIT 19/40, severe microsmia, below the normal range for age and sex. Before, an olfactory order got the library's normosmia (35/40), which contradicts the smell loss in the history. Optional: the test can add an MDS supportive criterion but changes no management. No scoring change for an agent that does not order it.
- `ground_truth.assessment.required_recommendations[0]`: rewritten so the smell loss counts as a supportive criterion once a validated test confirms it (UPSIT 19/40), instead of saying it cannot be tested.
- `ground_truth.key_clinical_evidence[3]`: rewritten so the smell loss counts as a supportive criterion once a validated test confirms it (UPSIT 19/40), instead of saying it cannot be tested.
