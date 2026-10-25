# PD-M04
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plans/PD.md (classes C1 to C22, per-case entry PD-M04) and the July 2026 tool review (labs optional and targeted, ECG and EEG removed). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | minor | `patient.neurological_exam.additional` | UPSIT 28/40 called "mild hyposmia"; for a 64-year-old man it is moderate microsmia (F1, C6). | FIXED: "moderate microsmia for age and sex". |
| A | major | `action-2-search-medical-literature`, `followup_outputs[0]` | Required literature criterion with an exact `query`; output misattributes titles to Marshall 2009 and Tolosa 2021 and states DaTscan is "the definitive discriminating test" (C1). | FIXED: criterion and follow-up deleted, literature initial and fallback null, removed from the stop rule. |
| A | major | `action-3-check-drug-interactions`, `followup_outputs[1]` | Required with exact `drug` and `current_medications` arguments; no dopamine-blocking drug in the list, so not a required step (ruling 6, C2); output with non-patient MAO-inhibitor text and agonist alternatives. | FIXED: optional, `{}`; single output `initial_tool_outputs.drug_interactions.general` (propranolol blunts the heart-rate response, amlodipine adds to orthostatic falls, no D2 blocker, daily alcohol, sulfonamide allergy not relevant); follow-up deleted, fallback null. |
| A | major | `action-1-analyze-brain-mri.alternatives` | `{"contrast": false, "protocol": "standard"}` (C5). | FIXED: `{}`; canonical label and rationale; citations `[Postuma_2015]` and `[Schwarz_2014]` (the report gives the SWI nigrosome finding). |
| C | minor | `initial_tool_outputs.mri` | "No abnormal enhancement following gadolinium" on a non-contrast study; "against NPH" and "no vascular parkinsonism pattern" in observations and impression (C12, Kind 1). | FIXED: gadolinium line deleted; observations and impression state the imaging findings (no lacunes, no confluent white matter disease, no disproportionate ventricles); SWI left-predominant nigrosome loss kept (contralateral to the worse right side). |
| D | minor | `initial_tool_outputs.labs` | Ceruloplasmin and RPR padding at 64 without a question; interpretation "hyperthyroidism excluded ... no metabolic or toxic mimic" (C11). | FIXED: ceruloplasmin and RPR rows removed (B12 kept); interpretation "All results within reference ranges."; criterion `action-4-interpret-labs` (TSH) stays optional with its own rationale and expected evidence (TSH 2.6, free T4 1.2). |
| C | major | `action-6-order-advanced-imaging`, DaTscan follow-up | Scan optional, yet the musts said "Order DaTscan ... establishes PD"; report with "comma-shaped ... dot-like" interpretation (C8). | FIXED: stays optional (re-emergent rest tremor and decrement make PD clinically clear; NICE NG71); report binary with SBRs (left putamen 0.92, right 1.41, caudates preserved); trigger `request_datscan`; no must, prohibition or evidence line depends on it any longer. |
| C | major | PSG follow-up | One conditional sentence ("a strong premotor synucleinopathy biomarker") instead of a report (C10). | FIXED: full report (TST 348 min, efficiency 82%, RSWA 34%, soft talking and right-arm jerks on video, AHI 2.9, SpO2 nadir 92%, PLMI 8) with the C10 impression; criterion stays optional (8 months of sleep talking and limb movements), rationale cites `[Berg_2015]`; trigger `request_sleep_study`. |
| B | minor | `followup_outputs` (missing) | Exam MoCA 27/30 against the library's 28/30 battery (C9). | FIXED: stored battery within normal limits with MoCA 27/30 and GDS 2/15; no criterion. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts required a DaTscan and a TSH that are optional criteria; "hyposmia" read from an unqualified UPSIT; no treatment (C6, C8.6, C16). | FIXED: four musts: clinically established PD with the two supportive criteria named (rest tremor, UPSIT microsmia) and coexisting ET; levodopa start with the agonist warning (64 years); continue propranolol for the postural tremor with lying and standing BP; ask about injurious dream enactment and bedroom safety. |
| C | minor | `prohibited_recommendations` | ET-misattribution prohibition cited the DaTscan; overlapping antipsychotic and anticholinergic templates ("aged over 65" at 64). | FIXED: canonical D2 prohibition; ET-misattribution prohibition rests on the clinical signs only. |
| C | major | `ground_truth.differential` | ET `high`, dystonic tremor `moderate` after the work-up (C13). | FIXED: ET `low` "coexists" (explains the postural tremor, not the new signs); dystonic tremor `low`; others `low` or `very_low` with excluding data, none relying on the optional DaTscan. |
| D | major | `key_clinical_evidence` | "July 2026" lines (C4); DaTscan "definitive" and laterality lines and a TSH line built on optional results. | FIXED: five lines from the exam, the UPSIT and the required MRI. |
| B | minor | `red_herrings` | Interpretations cited "an abnormal DaTscan confirms"; em dashes in data points. | FIXED: interpretations rest on the clinical signs and UPSIT; data points rewritten without dashes. |
| A | minor | `fallback_tool_outputs.advanced_imaging` | Amyloid PET fallback "does not resolve the current diagnostic question" (C11). | FIXED: null (the library answers per modality); amyloid and FDG waste entries kept. |
| A | minor | `fallback_tool_outputs.ecg`, `.cardiac_monitoring`, `.echo` | ECG "sinus bradycardia 57 ... beta-blocker" at a resting HR of 62; Holter "sinus bradycardia ... consistent with beta-blocker use" (average 61); no `echo_type` (C17). | FIXED: ECG "Sinus rhythm 62/min ..."; Holter impression and rhythm summary factual; TTE with concrete text. |
| B | minor | `avoided_actions`, `sequence_constraints`, `stop_rule` | Labs-before-drug constraint with an unfitting reason; Schwarz cited for MRI before DaTscan; `max_additional_actions` 0 (C20). | FIXED: one soft MRI-before-DaTscan constraint (canonical reason); stop rule MRI only, allowance 2; autonomic and tilt waste added; EEG, CSF, ECG and amyloid rationales made case-specific. |
| E | minor | `metadata.key_confounding_factor`, `.difficulty_rationale`, `.revision_reason`, `.last_revised` | Confounder named the DaTscan as discriminating; shared engineering text (C19). | FIXED: describe the edited case; 1 required criterion; 2026-10-24. |
| - | check | plan 3.6 | perfect_agent ok (MRI from the initial output; no recommended criterion); case_io check: no failure names PD-M04; test_case_guards pass; discriminator_defects empty. Routing: DaTscan, PSG, battery and labs serve the case; MIBG, amyloid and FDG go to the library; drug calls for levodopa and rasagiline serve the case output. | - |

## Changes, in one paragraph a physician can read before re-reviewing

A 64-year-old man with 20 years of essential tremor on propranolol now has a new right-hand re-emergent rest tremor, right-predominant rigidity and decrement, micrographia and UPSIT 28/40 (now read as moderate microsmia for age and sex). The policy is MRI required (any protocol) with optional TSH, optional DaTscan (the clinical picture is clear, so NICE NG71 does not ask for it), optional video-PSG for 8 months of sleep talking and limb movements, and an optional medication review (no dopamine blocker on the list); the literature step is gone. The MRI keeps its left-predominant nigrosome loss on SWI and loses the gadolinium line. The PSG is now a full report (RSWA 34%, no apnoea) and a normal battery matches MoCA 27. The musts diagnose clinically established PD on two supportive criteria (rest tremor and validated microsmia) with ET coexisting, start levodopa with the agonist warning, continue propranolol for the postural tremor with lying and standing BP, and address dream enactment safety. Nothing scored now depends on the optional DaTscan or TSH. ET is low and coexisting; dystonic tremor is low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[NICE_NG71]` is not yet in the PD criteria pack.
- Plan R4: the UPSIT is stated in the exam; an `olfactory_test` term would let a validated smell test be ordered.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case (plan Q1 to Q6 apply).

## Verification

Adversarial verifier, 24 Oct 2026. No PD notes file. Read the whole final case and the diff. The only patient change is the UPSIT wording (28/40 is moderate microsmia for a 64-year-old man on the UPSIT norms, so "clinically established PD" on rest tremor plus validated olfactory loss is supported). Checked: laterality (right signs, left SWI nigrosome loss, left putaminal SBR 0.92); no must, prohibition, evidence line or differential entry depends on the optional DaTscan or TSH; labs trimmed and interpretation neutral; PSG and battery consistent with the history and MoCA 27; ECG and Holter fallbacks at HR 62; tiers, stop rule and the single soft constraint per plan. All logged FIXED rows hold.

Found and changed:
- `avoid-waste-6-order-advanced-imaging` (FDG-PET) rationale said "DaTscan is the appropriate and indicated modality", contradicting the optional DaTscan and its rationale that the scan is not needed here. Rewritten: "FDG-PET has no role in separating PD from essential tremor; the examination already makes PD clinically clear". Checks after the verification edits: `perfect_agent.py -v` passes, `case_io.py check` names no failure for this case, `test_case_guards` pass.

## Condition audit

2026-10-24, PD condition auditor.

- `action-6-order-advanced-imaging.rationale`: "so the scan is optional" was tier wording in clinical text; now "so the scan is not needed to make the diagnosis". Tier unchanged (optional).
- `ground_truth.differential` "Enhanced physiologic tremor": ICD code G25.1 is drug-induced tremor; changed to G25.2 (other specified forms of tremor).
- `fallback_tool_outputs.csf.glucose_ratio`: 0.65 did not match the stored serum glucose (CSF 65 / serum 96 mg/dL = 0.68); now 0.68.

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

- `fallback_tool_outputs.specialized_test` (was null) is now an `olfactory_test` report, served only to an olfactory order: the examination already reports UPSIT 28/40 (moderate microsmia); an olfactory order now receives that same result instead of the library's normosmia. No criterion: the test is done, a repeat is not indicated.
