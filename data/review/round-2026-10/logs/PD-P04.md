# PD-P04
Reviewer status: R1 none, R2 none (PD has no notes file; only the July 2026 tool review, `condition_tool_guidance.yaml` key `parkinsons`) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No physician note exists for PD. The case was corrected against plan PD (classes C1 to C23, per-case entry PD-P04) and the July 2026 tool review (MRI required, labs targeted, genetics optional only for young onset, ECG and EEG removed, autonomic and tilt testing removed). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `followup_outputs[0]` (`search_literature_young_onset_parkinsons_wilsons`), criterion `action-2-search-medical-literature` | Required literature criterion with an exact `query`; output with misattributed content (Postuma 2015 "Wilson's disease must be excluded", Tolosa "DaTscan confirms") and an empty summary (C1). | FIXED: criterion and follow-up deleted; removed from the stop rule. Literature outputs stay null. |
| C | major | `followup_outputs[1]` (`check_drug_interactions_levodopa_young_onset`), criterion `action-3-check-drug-interactions` | Required drug criterion with exact `drug` and `current_medications` strings; output as a follow-up with dosing advice and "agonists commonly preferred in younger patients" (C2). | FIXED: follow-up deleted; one `initial_tool_outputs.drug_interactions.general` (calcium carbonate: no relevant interaction; non-selective MAOI contraindication; levodopa initiation warning; agonist and MAO-B alternatives with their class warnings); criterion `check_drug_interactions {}`, `optional` (plan), last. |
| A | major | `ground_truth.action_criteria[action-1-analyze-brain-mri]` | Required `{"contrast": false, "protocol": "standard"}` (C5). | FIXED: `analyze_brain_mri {}`; rationale and evidence rewritten (C3). |
| C | major | `ground_truth.action_criteria[action-4-interpret-labs]` | Wilson screening `optional` with a three-panel argument and generic evidence, while musts and prohibitions required it. | FIXED: `required` with one-item alternatives (`ceruloplasmin`, `serum_copper`, `24h_urinary_copper`), EASL 2012 rationale (plan wording), evidence with the three values; added to the stop rule. |
| C | minor | `initial_tool_outputs.labs` | RPR without a risk factor (padding); copper studies in a "Young_Onset_Movement_Disorder_Workup" panel; interpretation repeating the values. | FIXED: RPR removed; panels `Copper_Studies` (ceruloplasmin, serum copper, urinary copper 24h collection) and `Vitamins` (B12); interpretation "All results within reference ranges." (C11). Each copper panel order routes to the case labs. |
| B | minor | `patient.neurological_exam.additional` | Slit-lamp result repeated from the cranial nerve exam. | FIXED: duplicate removed (kept in `cranial_nerves`). |
| C | minor | `initial_tool_outputs.mri` | MRA line on a standard protocol (C12); "no swallow-tail sign loss at 3T, though sensitivity is limited on this field strength" (sensitivity is higher at 3T, and a preserved nigrosome would argue against PD without a dedicated sequence); repeated impression. | FIXED: MRA and the generic "no structural explanation" line removed; nigrosome-1 "not assessed (no high-resolution nigral SWI sequence)"; concise impression. |
| D | major | `followup_outputs` DaTscan | Impression with an em dash and "consistent with"; "putamen-to-caudate ratios" of 2.6 to 2.8 called normal (the putamen-to-caudate ratio is normally about 1; the values were binding ratios). | FIXED: binary C8 report with SBRs (left putamen 1.3, right 2.0, caudates 2.7 and 2.9) and asymmetry index 42%; trigger `request_datscan`. The plan's "(contralateral to the clinically worse side)" was not put in the report, because a report may not cite the exam (style guide); the laterality fits the right-sided signs. |
| B | major | `followup_outputs` (no PSG) | Two witnessed dream-enactment episodes; the library PSG is normal (C9, plan P04). | FIXED: PSG follow-up `request_sleep_study` (RSWA 31% of REM epochs, one arm-waving episode with sleep talking, AHI 2.1/h, PLMI 4/h) and optional criterion `action-polysomnography` [Berg_2015]. |
| C | major | `ground_truth.assessment.required_recommendations` | "supportive criteria (micrographia, asymmetric onset, rest tremor, probable abnormal DaTscan)": only rest tremor is an MDS supportive criterion (F1); "with abnormal DaTscan establish" relied on an optional study (C8); generic medication must; levodopa-response must without a plan. | FIXED: five musts: clinically probable PD (rest tremor the only supportive criterion); Wilson screening recorded as making it unlikely; symptomatic treatment with levodopa, agonist or MAO-B and the ICD/EDS warning [NICE_NG71]; counselled genetics; RBD bedroom safety and exercise. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | DaTscan clause in the "do not dismiss as functional" prohibition (C8); anticholinergic prohibition too strong (anticholinergics remain an option for tremor in young patients without cognitive impairment); duplicates. | FIXED: two prohibitions: do not dismiss as functional (organic signs only), canonical D2-blocker prohibition. |
| C | major | `ground_truth.differential` | Wilson `high` although excluded in the same sentence; DRD, functional and genetic `moderate`; DaTscan cited as excluding evidence (C13). | FIXED: all `low` with excluding data from the exam, labs and MRI; monogenic PD described as a subtype, not an alternative. |
| C | major | `ground_truth.key_clinical_evidence` | "mandates Wilson's exclusion before any other diagnosis is accepted", "definitively exclude", DaTscan "confirms", "agonists typically preferred in young patients", genetics "regardless of family history, as de novo mutations occur", two "July 2026" sentences (C4, plan P04). | FIXED: seven case items in the plan's wording (probable PD; Wilson made unlikely; agonist, levodopa or MAO-B options; counselled genetics before 50). |
| B | minor | `ground_truth.red_herrings[*].correct_interpretation` | Both relied on an "abnormal DaTscan" (optional study). | FIXED: rewritten on the exam findings. |
| A | minor | `ground_truth.sequence_constraints`, `.stop_rule` | Labs-before-DaTscan constraint (plan: delete); stop rule listed the literature and drug ids; `max_additional_actions` 0 (C20). | FIXED: only MRI before DaTscan (soft, canonical reason); stop rule MRI and labs; `max_additional_actions` 2. |
| A | minor | `ground_truth.avoided_actions` | Generic rationales; no autonomic or tilt guard (plan 3.3). | FIXED: EEG, CSF, echo, monitoring and ECG rationales case-specific; autonomic testing and tilt table `waste` added. |
| A | minor | `fallback_tool_outputs.echo`, `.ecg` | Echo without `echo_type`; ECG carried the removed `clinical_correlation` key. | FIXED: `echo_type` "TTE" with concrete findings; ECG key removed and findings "Sinus rhythm 66/min, normal axis and intervals, no ST change." |
| E | minor | `metadata` | Difficulty text "3 required tool actions after the independent reviewer audit"; revision fields stale. | FIXED: rewritten; citation gap lists [EASL_Wilson_2012] and [NICE_NG71]; `last_revised` 2026-10-24. |
| - | check | plan 3.6 | perfect_agent ok (MRI and labs `<- ?` are the dump-comparison labels of initial outputs; the routing probe confirms the case MRI and labs answer, including each one-item copper order); case_io check clean; test_case_guards pass; routing: DaTscan, PSG, genetics and drug from the case; MIBG, FDG, amyloid, neuropsych (MoCA 29/30, normal library battery fits) and orthostatic (no orthostatic symptoms) from the library. Pre-existing em dashes in the unedited HPI and motor sentences left. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The policy now requires MRI and copper studies (ceruloplasmin, serum copper or 24-hour urinary copper, each counting on its own), with DaTscan, video-PSG, counselled genetics and the medication review optional; literature and the drug follow-up are gone. The DaTscan report is binary with binding ratios (left posterior putamen reduced). A PSG matching the two witnessed episodes of dream enactment was added (RSWA 31%, no apnoea). The MRI no longer reports an MRA or an inaccurate 3T nigrosome statement, and the labs lost the unindicated RPR. The diagnostic must is clinically probable PD: rest tremor is the only supportive criterion (micrographia, asymmetry and a DaTscan are not MDS supportive criteria). The other musts: Wilson screening recorded as making it unlikely, symptomatic treatment with levodopa, an agonist or an MAO-B inhibitor with the agonist ICD and sleepiness warning, counselled genetics before 50, RBD bedroom safety and exercise. The "do not dismiss as functional" prohibition rests on the organic signs, not on the DaTscan; the anticholinergic prohibition was dropped. All mimics are low with their excluding findings.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan R1: `[EASL_Wilson_2012]` and `[NICE_NG71]` used per the plan; not yet in the PD pack.

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case. Deviation from the plan's canonical DaTscan sentence: "(contralateral to the clinically worse side)" was left out of the report text, because TOOL_REPORT_STYLE_GUIDE forbids a report citing the exam; the side is consistent with the right-sided signs.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the checkpoint diff (b8be2153) and the whole final case. Checked: copper studies required with one-item alternatives and each copper order routes to the case labs (MockServer probe); values within range (ceruloplasmin 28 mg/dL, serum copper 88, urine 28 microg/24h) and repeated identically in criterion, musts, differential and evidence; slit-lamp in the exam; DaTscan deficit in the left putamen for right-sided signs, asymmetry index 42% arithmetically correct; PSG matches the two witnessed episodes; diagnostic must is clinically probable PD with rest tremor as the only supportive criterion and no red flag; no prohibition or evidence depends on the optional DaTscan.
Found and fixed:
- B minor, `ground_truth.differential[1].key_features` (dopa-responsive dystonia): "without diurnal fluctuation" asserted a history the case does not contain. Now "Onset at 41 with no dystonic posturing on examination (dopa-responsive dystonia usually begins in childhood with foot dystonia); ...".
- B minor, `metadata.key_educational_points[2]`: said a degenerative-versus-functional differential "is active", contradicting the DaTscan criterion rationale (parkinsonism clinically clear, scan optional). Reworded to match the rationale.
After the edit: perfect_agent ok; case_io check clean for PD-P04; test_case_guards pass; discriminator_defects empty.

## Condition audit

2026-10-24, PD condition auditor.

- `followup_outputs[2].trigger_action`: `request_optional_counselled_young_onset_pd_genetics` carried a tier word; renamed `request_counselled_pd_gene_panel`. Routing is by `test_type` (`genetic_panel:PD`), unchanged; the probe serves the stored panel.

After the edits: `perfect_agent.py` 30/30 PD pass; every stored follow-up of the 30 cases is served for its own discriminator (MockServer probe); `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k PD-` 60 passed.

## Close-out (24 Oct 2026)

Decisions in `plans/PD-decisions.md`.

- Accepted codes are now G20.A1 (PD without dyskinesia, without mention of fluctuations; also PD NOS) and G20; G20.A2, G20.B1, G20.B2 (motor complications the case does not have) and G20.C ("Parkinsonism, unspecified", not PD) are no longer accepted. Labels unchanged.
- Wilson guideline recited from `[EASL_Wilson_2012]` (superseded) to `[EASL_ERN_Wilson_2025]` (EASL-ERN Clinical Practice Guidelines on Wilson's disease, J Hepatol 2025;82:690-728) in the labs criterion, the must and the key evidence; the labs rationale drops the 2012 age window "from age 3 to 55" and names the first-line tests (ceruloplasmin, 24-hour urinary copper, slit-lamp search for Kayser-Fleischer rings). `metadata.citation_gap` cleared (both keys are in the pack now).
