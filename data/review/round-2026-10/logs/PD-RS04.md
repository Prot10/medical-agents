# PD-RS04
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plans/PD.md (classes C1 to C23, per-case entry PD-RS04, C21 and C22) and the July 2026 tool review (MRI required; ECG, EEG, autonomic and tilt testing removed; labs, neuropsychology and genetics optional and targeted). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.history_present_illness`, `.clinical_history.past_medical_history`, `.clinical_history.medications` | Same patient as RS03: "Mrs. Delgado", same PMH (Roux-en-Y bypass, cholecystectomy 2 years ago) and the same five medicines at identical doses (C22, template carry-over). | FIXED: surname Ortega; bypass and cholecystectomy removed from the PMH (and the bypass line from the drug output); insulin glargine 22 units, metoprolol succinate 25 mg, levothyroxine 100 mcg; glucose 156 mg/dL (RS03 142). |
| C | blocker | `patient.history_present_illness`, `.chief_complaint`, `.neurological_exam.*`, `.social_history` | Labelled PD and straightforward, but a 4-month subacute course with three falls, "vertigo" on rising, a wide-based gait, a "jerky" bilateral tremor and symmetric signs (C21). | FIXED (plan C21): 20-month history, right-hand rest tremor first and a milder left-hand tremor after a year; unsteadiness on turning without vertigo or falls; narrow-based gait, pull test two steps with unaided recovery; right-predominant bradykinesia and rigidity; "jerky" deleted; lying and standing figures added (148/88 HR 64 to 140/84 HR 70) because metoprolol and urgency make the autonomic status a question. |
| B | minor | `patient.neurological_exam.mental_status` | MoCA 24/30 with only four lost points listed. | FIXED: six points listed (trail, cube, clock, phonemic fluency, two on recall). |
| A | major | `action-3-search-medical-literature`, two literature follow-ups | Required literature criterion; outputs authored by "Various", a nonexistent "MDS Clinical Criteria ... updated 2023", and the seed's "self-mutilation" search (C1). | FIXED: criterion and both follow-ups deleted; initial and fallback literature null. |
| A | major | `action-2-check-drug-interactions`, drug follow-up | Required with an exact `drug` string; "borderline orthostatic BP drop" with no figures in the case; post-bariatric line after the bypass is removed; dosing before meals contradicts the canonical start with food (C2). | FIXED: `check_drug_interactions {}`, `optional`; one stored output: fluoxetine C2 sentence, metoprolol orthostatic sentence, fluoxetine raising metoprolol (CYP2D6), metformin and B12; follow-up deleted, fallback null. |
| A | major | `action-1-analyze-brain-mri` | Required `{"contrast": false, "protocol": "standard"}` (C5); generic evidence; bare key. | FIXED: `analyze_brain_mri {}`; canonical label and rationale; evidence restates the report. |
| B | minor | `initial_tool_outputs.mri` | Finding typed "Normal brain parenchyma" while describing white matter hyperintensities "in the setting of hypertension and diabetes" (clinical reference); Fazekas "1-2" in one place and "scattered" in another; impression omits the white matter finding; "no mesial temporal sclerosis" irrelevant to the indication. | FIXED: one white matter finding (punctate, Fazekas 1) without clinical reference; impression names it; the mesial temporal line removed. |
| C | minor | `action-4-interpret-labs`, `initial_tool_outputs.labs` | Generic criterion; RPR and ceruloplasmin padding at 68; "Abnormal values" interpretation; HbA1c range "<5.7 (normal), <7.0 (diabetic target)" and "(target <7.0%)" in the summary. | FIXED: optional, one-item alternatives (`vitamin_B12`, `TSH`, `thyroid`), rationale (metformin lowers B12; treated hypothyroidism), evidence from the stored values; RPR and ceruloplasmin removed; values and flags only; HbA1c range "<5.7". |
| C | major | `followup_outputs` neuropsych | "Abnormal values" impression (C10); animals 14 against a ">14" range flagged normal. | FIXED: C10 impression (impaired processing speed and set-shifting, mildly reduced phonemic fluency, preserved learning: frontal-subcortical MCI profile), GDS 6/15 added, ranges and flags aligned; criterion stays `optional` (MoCA 24 with a memory complaint and depression, plan condition met); trigger `request_neuropsych_testing`. |
| C | major | `ground_truth.avoided_actions`, `followup_outputs` (missing) | No stored DaTscan: the library would return "normal" (C8). | FIXED: DaTscan `waste` with a stored C8 report (left putamen 0.94, right 1.31; left deficit opposite the worse right side). |
| E | minor | every criterion `rationale`, `citations` | Rationale a copy of the label; bare keys (C3). | FIXED. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts; "Confirm clinically established PD" (C6, C16). | FIXED: five musts: C6 probable PD; levodopa start with lying and standing BP on metoprolol; agonist caution (68 years); active treatment of depression and follow-up of the cognitive complaint (MCI, not dementia); physiotherapy and speech therapy. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Overlapping D2 prohibitions with an em dash. | FIXED: canonical D2 prohibition; anticholinergic prohibition kept (MoCA 24). |
| B | major | `ground_truth.differential`, `.red_herrings` | A metoclopramide DIP entry and red herring ("brief metoclopramide course mentioned") while the HPI denies any exposure, plus a duplicate DIP entry (C14); no ICD codes. | FIXED: metoclopramide entry and red herring deleted; one DIP entry `very_low`; ET `low` (mother); depression with psychomotor slowing (F32.A) `low` "coexists"; vascular, DLB `very_low`, MSA `low`; red herrings: mother's ET (`family_history[0]`) and depression (`past_medical_history[3]`). |
| D | major | `ground_truth.key_clinical_evidence` | Two "July 2026" engineering sentences (C4); "clinically established PD". | FIXED: five case-specific lines. |
| B | minor | `ground_truth.avoided_actions` | One-phrase rationales; no autonomic or tilt guard. | FIXED: case-specific rationales; DaTscan, autonomic and tilt `waste` added. |
| B | minor | `ground_truth.sequence_constraints`, `.stop_rule` | "Drug check before labs" constraint; stop rule with literature and drug; 0 extra actions (C20). | FIXED: no constraint; stop rule MRI; 2. |
| A | minor | `fallback_tool_outputs.echo`, `.ecg` | Echo without `echo_type`; ECG rate 72 against a resting HR of 64 (C17). | FIXED: TTE with concrete text; ECG "Sinus rhythm 64/min, normal axis and intervals, no ST change." |
| E | minor | `metadata.difficulty_description`, `.difficulty_rationale`, `.revision_reason`, `.last_revised` | "Postural instability", "falls", "autonomic borderline findings" no longer true; shared engineering text (C19). | FIXED. `difficulty` stays `moderate`. |
| - | check | plan 3.6 | perfect_agent ok (MRI from the initial output); case_io check: no failure names PD-RS04; test_case_guards 2 passed. Routing: battery and DaTscan return the case reports; labs return the stored panel; `drug: levodopa` and `drug: rasagiline` return the case output; library PSG (normal) fits a history without dream enactment; library orthostatic BP fits the added figures. | - |

## Changes, in one paragraph a physician can read before re-reviewing

This case was a copy of RS03 (same surname, history, medicines and a subacute course with falls) that met several MDS red flags. It now describes a different 68-year-old woman, Mrs. Ortega, a retired professor with diabetes, treated hypothyroidism, hypertension on metoprolol and depression on fluoxetine (no bariatric surgery), with 20 months of right-predominant parkinsonism: pill-rolling rest tremor of the right hand, a milder left-hand tremor after a year, decrement, rigidity, micrographia, hypophonia, unsteadiness on turning without falls, a narrow-based gait, no orthostatic fall, and a memory complaint with MoCA 24/30 while still independent. The policy is MRI only (required); B12 and thyroid labs, a neuropsychological battery (now a frontal-subcortical MCI profile with preserved learning, GDS 6/15) and a medication review are optional; literature is gone and the DaTscan is waste (stored abnormal report). The metoclopramide red herring, which the history itself denied, is replaced by the mother's ET and the depression. The musts are probable PD (not "established"), levodopa start with standing BP checks on metoprolol, agonist caution, treatment of depression with follow-up of cognition, and therapy referrals.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[NICE_NG71]` (levodopa and agonist musts, DaTscan waste) is not yet in the PD criteria pack.
- Plan R5: library MIBG default normal (not on this pathway).

## Open questions for Andrea (judgment calls you could not settle)

- Plan Q3 applies (RS03 and RS04 rewritten to typical PD rather than dropped). The seed (`metadata.source_pmcid` PMC8271262) no longer describes the case content; the provenance field was kept as the seed record.

## Verification (adversarial verifier, 24 Oct 2026)
- Read the log, the diff and the whole final case (C21 and C22 rewrite: high risk). No PD notes file exists.
- Checked: surname Ortega (not Delgado), no bypass or cholecystectomy anywhere (PMH, drug output, differential, metadata); doses differ from RS03; 20-month history, no falls, no vertigo, narrow-based gait, right-predominant signs; orthostatic figures consistent across exam, differential and evidence; MoCA 24 with six points listed, matching the stored battery; labs criterion panel names (`vitamin_B12`, `TSH`, `thyroid`) in the vocabulary and the stored values match its expected evidence; metoclopramide red herring and duplicate DIP entry gone; probable PD.
- Found and FIXED:
  - `ground_truth.differential` (DLB) `key_features` claimed "parkinsonism for 20 months before any cognitive complaint"; the HPI does not date the memory complaint, so the timing was unsupported. Reduced to what the case shows: no dementia (manages finances and medications), no fluctuations, hallucinations or dream enactment.
  - `initial_tool_outputs.mri.findings[0].signal_characteristics.T2` read "No focal or confluent signal abnormalities" while `findings[1]` reports punctate white matter hyperintensities (internal inconsistency). Now limited to the deep grey nuclei, brainstem and cerebellum.
- Checks re-run after verification: `perfect_agent.py -v` pass; `case_io.py check` schema OK, no failure names the case; `test_case_guards -k` pass; MockServer routing: DaTscan, MIBG and amyloid return their own modality (case or library), PSG and battery return the case report where stored, `check_drug_interactions` with `drug: levodopa` and `drug: rasagiline` return the case output, labs route to the stored panel where one exists; grep for established / gadolinium / "Abnormal values:" / Lewy / serotonin syndrome / Tier per / July 2026 / dashes: only allowed hits.

## Condition audit

2026-10-24, PD condition auditor.

- `fallback_tool_outputs.csf`: CSF glucose 62 mg/dL with ratio 0.6 did not fit the stored serum glucose of 156 mg/dL (true ratio 0.40). Glucose now 94 mg/dL (ratio 0.6), interpretation states the CSF glucose is in proportion to the raised serum glucose.
- `initial_tool_outputs.drug_interactions.general.interactions[0]`: same fluoxetine sentence fix as RS03 (avoid with rasagiline, 5-week washout after fluoxetine).

After the edits: `perfect_agent.py` 30/30 PD pass; every stored follow-up of the 30 cases is served for its own discriminator (MockServer probe); `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k PD-` 60 passed.
