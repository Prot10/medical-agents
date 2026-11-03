# PD-M03
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plans/PD.md (classes C1 to C22, per-case entry PD-M03) and the July 2026 tool review. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.history_present_illness` | "His wife believes the gait changes preceded the medication initiation, though she is not entirely certain": impossible with metoclopramide for 3 years and a 12 to 14 month motor history, and the base of evidence lines (C15). | FIXED: clause deleted; the sentence ends "despite being on a stable dose of metoclopramide." |
| A | major | `action-3-search-medical-literature`, `followup_outputs[0]` | Required literature criterion with an exact `query`; summary prescribing "a trial of discontinuation ... alongside DaTscan for definitive differentiation" (C1, style guide). | FIXED: criterion and follow-up deleted; literature initial and fallback null; removed from the stop rule. |
| A | major | `action-2-check-drug-interactions`, `followup_outputs[1]` | Exact `drug`/`current_medications` arguments; output with a false "metformin may reduce levodopa absorption" and trimethobenzamide offered as an alternative (C2). | FIXED: `{}`, required (metoclopramide); single output `initial_tool_outputs.drug_interactions.general` (metoclopramide C2 sentence, tamsulosin and lisinopril with orthostasis, EU contraindication, boxed warning, domperidone and erythromycin QT, aspirin allergy noted as not relevant); follow-up deleted; fallback null. |
| A | major | `action-1-analyze-brain-mri.alternatives` | `{"contrast": false, "protocol": "standard"}` (C5). | FIXED: `{}`, canonical label and rationale, `[Postuma_2015]`. |
| C | major | `action-4-order-advanced-imaging` | DaTscan optional while the label rests on it, and it is the only biomarker in this case (C8). | FIXED: required, in the stop rule, case-specific text; trigger `request_datscan`; C8 binary report with SBRs (right putamen 1.02, left 1.29, caudates preserved); laterality checked (right deficit opposite the worse left side and the left-hand tremor his wife reports). |
| C | minor | `initial_tool_outputs.mri` | Evans 0.29 called "borderline" and ventricles "mildly out of proportion" to sulci, an NPH lure no other field uses; "abnormal enhancement" on a non-contrast study (C12). | FIXED: Evans 0.29 kept (normal), ventricles "proportionate to sulci" in the finding, observations, volumetrics and impression; enhancement wording deleted; numbered impression. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts; "premotor features (RBD, constipation, hyposmia) preceding metoclopramide" although he denies dream enactment and reports no smell loss (C6, C15, C16). | FIXED: five musts: C6 M03 diagnostic must naming only the DaTscan; stop metoclopramide with the gastroenterologist, watching his weight (8 lb lost); reassess after withdrawal; levodopa once stopped with lying and standing BP (tamsulosin, lisinopril); physiotherapy and fall prevention (two near-falls, two steps of retropulsion). No agonist must (age 75). |
| C | minor | `prohibited_recommendations` | Overlapping antiemetic and antipsychotic prohibitions. | FIXED: canonical D2 prohibition; levodopa-with-metoclopramide and anticholinergic prohibitions kept. |
| C | major | `ground_truth.differential` | DIP `high`, vascular `moderate` after the work-up; NPH entry "need to inspect" (C13). | FIXED: all `low` with excluding data; DIP "coexisting contributor"; ET `very_low`. |
| D | major | `key_clinical_evidence` | "July 2026" engineering lines (C4); RBD on polysomnography and premotor features claimed (none in the case); "symmetric onset". | FIXED: six case-specific lines, including that the history gives no non-motor marker and the DaTscan is the only biomarker. |
| B | minor | `red_herrings` | Interpretation claimed RBD, constipation and hyposmia before the drug. | FIXED: metoclopramide (`medications[0]`) and family tremor (`family_history[2]`) with corrected interpretations. |
| B | minor | `avoided_actions`, `sequence_constraints`, `stop_rule` | One-phrase rationales; constraint cited Schwarz; `max_additional_actions` 0 (C20). | FIXED: case-specific rationales; autonomic and tilt waste added; MRI before DaTscan soft; stop rule MRI, DaTscan, medication review; allowance 2. |
| A | minor | `fallback_tool_outputs.echo`, `.ecg`, `.cardiac_monitoring` | No `echo_type`; ECG rate 88 against HR 68; Holter "only benign findings" (C17). | FIXED: TTE with concrete text; ECG "Sinus rhythm 68/min ..."; Holter impression names the premature atrial complexes; `metadata.fallback_tool_kinds.cardiac_monitoring` "normal". |
| E | minor | `metadata.difficulty_rationale`, `.revision_reason`, `.last_revised` | Shared engineering text (C19). | FIXED per plan, 2026-10-24. |
| - | check | plan 3.6 | perfect_agent ok (MRI initial, DaTscan `request_datscan`, medication review initial); case_io check: no failure names PD-M03 (only the PD-P03 leak test, another worker's case); test_case_guards pass; discriminator_defects empty. Routing: DaTscan from the case; PSG and battery from the library (normal), which fits a history without dream enactment and MMSE 28/30; drug calls for levodopa and rasagiline serve the case output. | - |

## Changes, in one paragraph a physician can read before re-reviewing

A 75-year-old man with bilateral, slightly left-predominant bradykinesia and rigidity after three years of metoclopramide, with no dream enactment and no reported smell loss. The impossible timeline sentence (gait change before a drug started two years earlier than the symptoms) is gone. The policy is MRI (required, any protocol), DaTscan (required: here it is the only marker of a degenerative process) and medication review (required); literature is gone. The MRI now reports normal-sized, proportionate ventricles (Evans 0.29) without an enhancement line. The DaTscan gives right putamen 1.02 and left 1.29 with caudate sparing, binary impression. The musts rest on the DaTscan alone, add stopping metoclopramide (weight watched), reassessment after withdrawal, levodopa only once it is stopped with lying and standing BP on tamsulosin and lisinopril, and physiotherapy for his near-falls. The false metformin-levodopa interaction and the trimethobenzamide alternative are removed. All mimics are low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[NICE_NG71]` is not yet in the PD criteria pack.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case (plan Q1 to Q6 apply).

## Verification

Adversarial verifier, 24 Oct 2026. No PD notes file. Read the whole final case and the diff. The only HPI change is the deleted timeline clause, as logged. Checked: no RBD, PSG or hyposmia claim remains in musts, evidence, red herrings or metadata; laterality (worse left, right putaminal SBR 1.02); MRI Evans 0.29 proportionate everywhere; drug output covers all six drugs and the aspirin allergy; differential low; tiers and stop rule per plan. All logged FIXED rows hold.

Found and changed:
- `avoid-waste-5-analyze-ecg` contradicted the must "domperidone where available after an ECG for the QTc" (same class as M01). Removed.
- `differential[Essential tremor].key_features` and `red_herrings[1].correct_interpretation` asserted "no postural or action tremor", which the examination never tests or records (it records only the absence of rest tremor and an endorsed occasional hand tremor). Rewritten as "No postural or action tremor is described in the history or on examination; ...". Checks after the verification edits: `perfect_agent.py -v` passes, `case_io.py check` names no failure for this case, `test_case_guards` pass.

## Close-out (24 Oct 2026)

Decisions in `plans/PD-decisions.md`.

- Accepted codes are now G20.A1 (PD without dyskinesia, without mention of fluctuations; also PD NOS) and G20; G20.A2, G20.B1, G20.B2 (motor complications the case does not have) and G20.C ("Parkinsonism, unspecified", not PD) are no longer accepted. Labels unchanged.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: MDS-UPDRS III 27/132 OFF, 16/132 ON (41%) (fallback_tool_outputs.clinical_assessment). Why: rule 3: the stored exam documents parkinsonism; the library reports MDS-UPDRS III 3/132 with no parkinsonian signs.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: TUG 13.0 s, 10 m 0.99 m/s, Berg 50/56 (followup request_gait_and_balance_timed). Why: rule 3: the stored gait exam (arm swing, stride, turns, pull test) is abnormal; the library reports a normal gait, turns in 3 steps and Berg 56/56.
- `order_specialized_test {test_type: speech_language_evaluation}`: hypophonia, articulation precise (64 dB SPL), no aphasia (fallback_tool_outputs.specialized_test). Why: rule 3: the stored exam records hypophonia; the library reports no motor speech disorder.
- `order_specialized_test {test_type: olfactory_test}`: UPSIT 24/40 (severe microsmia) (followup request_olfactory_test). Why: rule 1: olfactory loss is a supportive feature of PD; the library reports normosmia (UPSIT 35/40).
- `order_advanced_imaging {modality: MIBG_scan}`: early H/M 1.40, delayed 1.20, washout 41% (fallback_tool_outputs.advanced_imaging). Why: rule 1: cardiac sympathetic denervation is a supportive criterion of PD; the library reports normal uptake (H/M 2.4/2.6).
- `interpret_labs {panels: [HbA1c]}`: HbA1c 6.9% (treated diabetes) (fallback_tool_outputs.labs[HbA1c]). Why: rule 2: type 2 diabetes on treatment; the library reports 5.4%.

Checks: `perfect_agent.py` 30/30 PD pass; `test_case_guards.py -k PD-` and `pytest agent-platform/tests -k PD-` 300 passed (`test_grpo_rollout.py` not collected: training extra not installed); every criterion's served output unchanged (snapshot before/after); synonym guard 0 changes; no new report repeats a 60-character window of any `expected_evidence`; every listed term is answered without the library.
