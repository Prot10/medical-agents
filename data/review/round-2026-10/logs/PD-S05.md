# PD-S05
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plans/PD.md (classes C1 to C23, per-case entry PD-S05) and the July 2026 tool review (MRI required; ECG, EEG, autonomic and tilt testing removed; labs, neuropsychology and genetics optional and targeted). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | blocker | `ground_truth.action_criteria[action-3-search-medical-literature].expected_evidence`, `assessment.required_recommendations[0]`, `key_clinical_evidence[0]`, `differential[ET, MSA]`, `red_herrings[0]` | "Clinically established PD (two supportive features: hyposmia and dramatic levodopa response)": the patient has never taken levodopa, and his smell loss is self-reported, not a validated test (C6, C15, F1). | FIXED: every levodopa-response and hyposmia-as-supportive claim deleted; clinically probable PD (rest tremor the only supportive criterion, no red flag). |
| A | major | `action-3-search-medical-literature`, `followup_outputs[0]` | Required literature criterion with an exact `query` string; its output called RBD a supportive criterion and stated a "90%" hyposmia figure as a supportive-criterion fact (C1, ruling 5). | FIXED: criterion and follow-up deleted, removed from the stop rule; initial and fallback literature null. |
| A | major | `action-2-check-drug-interactions`, `followup_outputs[1]` | Required drug check with exact `drug` and `current_medications` strings; output with em dashes and an irrelevant selegiline "serotonergic" warning (C2). | FIXED: `check_drug_interactions {}`, tier `optional`; one stored output `initial_tool_outputs.drug_interactions.general` (amlodipine orthostatic C2 sentence; non-selective MAOI contraindication; metformin, rosuvastatin, pantoprazole no relevant interaction; iron and protein, nausea, sleep attacks, ICD warnings); follow-up deleted, fallback null. |
| A | major | `action-1-analyze-brain-mri.alternatives` | `{"contrast": false, "protocol": "standard"}` not matched by a plain MRI order (C5). | FIXED: `analyze_brain_mri {}`; canonical label and rationale; citations `[Postuma_2015]` and `[Schwarz_2014]` (the report gives an SWI nigrosome finding). |
| B | minor | `initial_tool_outputs.mri.findings[0].signal_characteristics.SWI` | Nigrosome conspicuity "at the lower limit of normal on the right", ipsilateral to the right-sided signs; nigral loss is expected contralaterally (left). | FIXED: "on the left"; expected_evidence restates it; impression given its final period. |
| D | major | `followup_outputs` DaTscan | Interpretive report: "comma-shaped" pattern, putamen-to-caudate ratios against a ">2.0" norm, em dash impression, `quantitative_data` null (C8). | FIXED: C8 binary report: left posterior putamen SBR 0.98, right 1.32 (normal >1.50), caudates 2.17 and 2.46, "Presynaptic dopaminergic deficit"; tracer "123I-ioflupane SPECT"; trigger kept (routes by `modality`). |
| C | minor | `action-4-order-advanced-imaging` | Optional DaTscan with generic label, rationale and the shared generic expected_evidence; bare duplicate key (C3, C8). | FIXED: stays `optional` per plan; case-specific label, rationale (postural tremor and maternal ET raise ET; clinically likely PD, so optional) [NICE_NG71], expected_evidence restating the stored figures. |
| D | major | `ground_truth.key_clinical_evidence` | Two "July 2026" engineering sentences (C4); DaTscan laterality line built on an optional study ("confirms") (C8 rule 6); em dashes; "conclusively". | FIXED: five case-specific lines restating patient data and the required MRI. |
| C | major | `ground_truth.assessment.required_recommendations` | Six generic or false musts (C16). | FIXED: five musts: probable-PD diagnostic must (postural component and self-reported smell loss addressed), canonical levodopa start, agonist caution (age 67), lying and standing BP during titration (amlodipine), PT/OT/SLT. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Generic prohibitions with em dashes. | FIXED: canonical D2-blocker prohibition; anticholinergic prohibition at 67. |
| C | major | `ground_truth.differential[Essential tremor]` | ET `moderate` (C13). | FIXED: `low`, postural component explained; MSA, PSP and vascular `key_features` rewritten without the levodopa claim and em dashes. |
| B | minor | `ground_truth.red_herrings` | Interpretation relied on the non-existent levodopa response; em dash. | FIXED: postural tremor interpretation rewritten; maternal ET (`family_history[1]`) added as a second red herring. |
| B | minor | `ground_truth.sequence_constraints`, `.stop_rule` | Constraint cited `[Schwarz_2014]` for an ordering reason; stop rule listed drug and literature ids; `max_additional_actions` 0 (C20). | FIXED: canonical soft MRI-before-DaTscan constraint `[Postuma_2015]`; stop rule MRI only; 2. |
| C | minor | `ground_truth.avoided_actions` | Generic rationales; no autonomic or tilt guard (3.3). | FIXED: case-specific rationales; added autonomic and tilt waste (DaTscan is optional, not waste). |
| E | minor | `patient.history_present_illness` | Em dash; "He denies acting out dreams during sleep, though his wife has not observed any such behavior" (illogical "though"). | FIXED: semicolon; "and his wife has not observed any such behavior". |
| A | minor | `fallback_tool_outputs.ecg`, `.echo` | ECG rate 73 against HR 74; echo without `echo_type` (C17). | FIXED: ECG "Sinus rhythm 74/min, normal axis and intervals, no ST change."; echo `TTE`, EF 62%. |
| E | minor | criterion `rationale`, `citations`; `metadata.estimated_complexity`, `.difficulty_rationale`, `.revision_reason`, `.last_revised` | Rationale copied from label, bare keys (C3); "levodopa-responsive" complexity text with an em dash; shared engineering metadata (C19). | FIXED. |
| - | check | plan 3.6 | perfect_agent ok; case_io check: no failure names PD-S05; test_case_guards pass; discriminator_defects empty. Routing: DaTscan returns the case report; PSG and battery return library normals (no dream enactment, MMSE 29/30); MIBG, amyloid, FDG, orthostatic BP library; `drug: levodopa` and `drug: rasagiline` return the case output. | - |

## Changes, in one paragraph a physician can read before re-reviewing

This 67-year-old man has an 18-month right-predominant tremor-onset parkinsonism (pill-rolling rest tremor with re-emergence, decrement, cogwheel rigidity, micrographia, hypophonia) with a mild 6-8 Hz postural tremor component, self-reported smell loss and a mother with ET. The case claimed "clinically established PD" on hyposmia and a "dramatic levodopa response", but he has never taken levodopa and the smell loss was never tested: he is now clinically probable PD. The policy is a brain MRI (required, any protocol; the SWI nigrosome remark now sits on the left, opposite his signs) with an optional DaTscan for the mixed tremor (report now binary with binding ratios, left putamen 0.98) and an optional medication review naming amlodipine. The literature step is gone. The musts are the probable-PD diagnosis, levodopa titrated to 300 mg/day, the agonist ICD/EDS warning, lying and standing BP during titration, and PT/OT/SLT. ET is now low; the red herrings are the postural tremor and the maternal ET.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[NICE_NG71]` (DaTscan criterion, levodopa, agonist and therapy musts) is not yet in the PD criteria pack.
- Plan R4: an `olfactory_test` term would let an agent validate the reported smell loss as a supportive criterion.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case (plan Q1 to Q6 apply).

## Verification
- Checked against the committed rewrite (diff from b8be2153^, field by field), plans/PD.md section 4 entry and classes C1 to C23. No notes file exists for PD, so there is no note id to account for. Tools re-run 24 Oct 2026: perfect_agent ok, case_io check (no failure names the case), test_case_guards pass (leak, followup, banned strings), and a MockServer routing script (MRI or CT, DaTscan, MIBG, amyloid, FDG, PSG, battery, orthostatic BP, labs, ECG, drug check for levodopa and for rasagiline).
- Confirmed every row: all claims of a levodopa response and of validated hyposmia removed (grep for "established", "dramatic", "supportive" in clinical fields finds only the probable-PD wording); SWI nigrosome remark now on the left, contralateral to the right-sided signs, and restated in the MRI evidence with `[Schwarz_2014]`; DaTscan optional, binary report, left putamen 0.98, routed by modality despite its long trigger; soft MRI-before-DaTscan constraint with both ids present; ET `low`; both red herrings point to real fields; the only patient change is the em dash and the "though" wording in the HPI.
- Key evidence and musts cite no optional result (the DaTscan laterality line is gone). Library battery (MoCA 28) agrees with the exam MMSE 29/30; library PSG agrees with the denial of dream enactment.
- Found nothing to correct. No change made.

## Condition audit

2026-10-24, PD condition auditor.

- `followup_outputs[0].trigger_action`: `request_optional_datscan_for_live_degenerative_differential` carried a tier word; renamed `request_datscan` (the name the other PD cases use). Routing by `modality` `DaTscan`, unchanged.

After the edits: `perfect_agent.py` 30/30 PD pass; every stored follow-up of the 30 cases is served for its own discriminator (MockServer probe); `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k PD-` 60 passed.

## Close-out (24 Oct 2026)

Decisions in `plans/PD-decisions.md`.

- Accepted codes are now G20.A1 (PD without dyskinesia, without mention of fluctuations; also PD NOS) and G20; G20.A2, G20.B1, G20.B2 (motor complications the case does not have) and G20.C ("Parkinsonism, unspecified", not PD) are no longer accepted. Labels unchanged.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
