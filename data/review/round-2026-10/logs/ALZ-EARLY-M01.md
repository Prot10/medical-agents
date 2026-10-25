# ALZ-EARLY-M01
Reviewer status: R1 needs_changes, R2 pending | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 5daf3975-06a2-42b1-a4b1-5a3b9ee1693f | FIXED | `ground_truth.diagnosis.accepted[0]` now "Amnestic multidomain mild cognitive impairment, suspected Alzheimer disease pathology (intermediate likelihood) with vascular contribution" (G31.84 kept). CSF interpretation (`followup_outputs[2].output.interpretation`) names the measured profile (borderline decreased Abeta42/40, tau within range) and no A+T+ claim; criterion `action-8-analyze-csf.expected_evidence` says "amyloid positivity without established tau pathology"; differential, red herrings and KCE no longer speak of "biomarker positivity" or "positive amyloid biomarkers". |
| 78693860-5477-4c03-99cd-40b80525f219 | FIXED | Donepezil drug-check follow-up deleted (was `followup_outputs[2]`); `initial_tool_outputs.drug_interactions` and `fallback_tool_outputs.drug_interactions` null. Prohibition added: no cholinesterase inhibitor or memantine as routine treatment for MCI (replaces the memantine-at-mild-stage prohibition). KCE on AChEI first-line replaced by the MCI fact. |
| 88980d7d-da48-4a76-9c3c-d4ae9ef6f728 | FIXED | `action-8-analyze-csf` relabelled "Establish amyloid status with CSF biomarkers or amyloid PET when the result would change management", optional, two alternatives (CSF special_tests, `order_advanced_imaging` amyloid_PET); new rationale (one conclusive test, needed only for residual uncertainty or a treatment decision). Amyloid PET follow-up authored (`followup_outputs[3]`, low-positive, Centiloid 31) so the alternative returns the case's biology, not the library's negative default. Must "single case-designated optional biomarker route" replaced by the canonical amyloid-testing must. |
| dd4d5e93-45bd-419e-8839-8f65cc44ff03 | FIXED | Criterion `action-9-check-drug-interactions` removed from `ground_truth.action_criteria`. |
| c0c9b572-c97f-40fb-a3ef-fa43238e800d | FIXED | Summary comment; covered by the four rows above (label reframed as suspected AD pathology, donepezil step removed, PET as optional alternative). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.history_present_illness`, `initial_tool_outputs.clinical_assessment.findings[3]` | Staging ambiguous: billing errors reported with no statement of who now manages finances. | FIXED: HPI adds that he set up automatic payments, still manages the accounts himself with no further errors in three months, and his wife has not taken over (plan 1.2 preserved-IADL rule). Informant finding rewritten from the informant's account rather than a copied HPI sentence. |
| E | major | `initial_tool_outputs.clinical_assessment.impression`, `.scores` | Template impression with engineering sentences ("the threshold is functional, and this assessment is where it is decided", "This assessment is the step that makes the syndrome measurable"); em dash in the staging score. | FIXED: impression per C3 skeleton from this case's findings (MMSE 26/30, recall 1/3 to 2/3 with cues, fluency, informant, preserved IADL); score text without dash. Cueing field true kept (consistent with 1/3 to 2/3). |
| E | minor | `initial_tool_outputs.clinical_assessment.findings[2]` | Sentence truncated ("Naming intact for common objects;"). | FIXED: completed. |
| C | minor | `followup_outputs[0].output.impression` (neuropsych) | "Storage-type memory deficit" not supported (no recognition measure; bedside cueing helped); Rey Complex Figure delayed recall listed as executive function. | FIXED: storage claim removed, Rey delayed recall described as visual memory, Trail B as set-shifting; neuropsych conclusion "consistent with amnestic multi-domain mild cognitive impairment" added (Kind 2, allowed by style guide). |
| B | minor | `followup_outputs[2].output` (CSF) | 14-3-3 and RT-QuIC in a non-rapid case; "(N/A PMN/N/A lymph)" artefact; analyte keys not in vocabulary names. | FIXED per C6: special_tests keys `Abeta42`, `Abeta40`, `Abeta42_40_ratio`, `phospho_tau`, `total_tau` with values unchanged; 14-3-3 and RT-QuIC removed; interpretation rewritten as a pattern statement. |
| C | major | `initial_tool_outputs.mri.additional_observations`, `.impression` | Bilateral parietal microbleeds called "likely hypertensive" (lobar distribution points to CAA, Boston 2.0); "No abnormal meningeal enhancement" with `contrast: false`; prose impression. | FIXED: "Three lobar microbleeds ... no deep microbleeds"; enhancement phrase deleted; numbered impression including "a lobar distribution raises cerebral amyloid angiopathy". |
| C | major | `ground_truth.action_criteria` | MMA follow-up existed without a criterion; B12 305 pg/mL on 12 years of metformin with reduced toe vibration. | FIXED: new `action-10-interpret-labs-mma` (recommended, `{"panels": ["MMA"]}`), placed after labs; follow-up moved to `followup_outputs[1]`, trigger `request_mma_methylmalonic_acid`, panel key `MMA`, interpretation states the value. |
| A | minor | `ground_truth.action_criteria[*].citations`, `.rationale` | Duplicate bare keys ("NIA_AA_2011" next to "[NIA_AA_2011]"); rationale identical to label. | FIXED (C13): one bracketed key each; patient-specific rationales; expected_evidence made case-specific (clinical assessment, neuropsych, labs, MRI). |
| C | major | `ground_truth.assessment.required_recommendations` | Musts restated tool steps (labs, MRI, cognitive battery); smoking cessation for a man who quit 20 years ago; engineering must. | FIXED (C12): five musts: disclosure of MCI with suspected AD pathology and planning; 6-12 month reassessment plus exercise; vascular risk management with his values (HbA1c 7.3%, BP 135/77, statin, CPAP); driving and finance safety; amyloid testing only if it changes management. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Generic five-item template (benzodiazepine, antipsychotic not relevant). | FIXED: MCI AChEI/memantine prohibition; named antimuscarinic prohibition (BPH, tamsulosin is not anticholinergic); do not attribute to OSA, mood or aging alone. |
| C | major | `ground_truth.differential[0]`, `[3]`, `[4]` | VCI `high` while AD pathology is the main driver; key features cited "biomarker positivity"; reversible-causes entry said labs "are needed" although they are returned; depression entry ignored GDS 6/15. | FIXED: VCI moderate as contributor; reversible causes cite TSH, B12 with normal MMA and homocysteine, OSA; depression entry cites GDS 6/15 and denial of low mood. |
| B | minor | `ground_truth.key_clinical_evidence` | Storage-type pearl (not true here), APOE pearl (no APOE in case), AChEI first-line pearl (MCI). | FIXED: four items: MMSE insensitivity (kept), mixed pathology with lobar microbleeds/CAA, low-normal B12 on metformin, AChEI not for MCI. |
| B | minor | `ground_truth.red_herrings[0..1]` | Cited "positive amyloid biomarkers" not in the required pathway; location "Social history" for a past-medical-history item. | FIXED: reworded to hippocampal atrophy and amnestic profile; location "Past medical history". |
| D | minor | `fallback_tool_outputs.literature_search` | Literature fallback retained (C8). | FIXED: null. |
| B | minor | `fallback_tool_outputs.ecg.rate` | Rate 82 vs resting HR 68. | FIXED: 70. |
| B | minor | `ground_truth.sequence_constraints`, `.stop_rule` | Only MRI-before-CSF; `max_additional_actions` 0. | FIXED: added soft clinical assessment before biomarker criterion; `max_additional_actions` 1. |
| B | minor | `metadata.difficulty_rationale`, `.key_educational_points[5]` | Described CSF as the only route and said CSF and PET must not be ordered together. | FIXED: reworded to the two-alternative rule. |
| B | minor | `initial_tool_outputs.labs.panels.BMP` | The criterion orders CMP but the report holds a BMP (no liver panel). | FLAGGED: left as is; adding unrequested values would be invention and nothing in the case depends on liver tests. |
| - | check | plan 3.6 | Probed the MockServer: `order_advanced_imaging {"modality": "amyloid_PET"}` returns the authored positive PET (not fallback); `analyze_csf` returns the CSF follow-up; `interpret_labs {"panels": ["methylmalonic_acid"]}` returns the MMA follow-up. perfect_agent.py ok; test_case_guards pass for this case. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The case stays mild cognitive impairment, now labelled "amnestic multidomain MCI, suspected Alzheimer disease pathology (intermediate likelihood) with vascular contribution". The HPI says the two billing errors were isolated and he now uses automatic payments and still manages the accounts himself, so instrumental independence is explicitly preserved. The bedside assessment impression is rewritten from the case's own findings (MMSE 26/30, recall 1/3 improving to 2/3 with cues). The donepezil drug check is gone, replaced by a prohibition on starting a cholinesterase inhibitor or memantine in MCI and a must for 6 to 12 month reassessment with exercise. Amyloid status is one optional step that can be met by CSF or amyloid PET; the CSF (unchanged values: Abeta42 465, ratio 0.060 borderline decreased, p-tau181 52 and t-tau 345 within range) no longer contains 14-3-3 or RT-QuIC, and a low-positive amyloid PET (Centiloid 31) answers the PET alternative. MMA (0.17, normal) is now a recommended criterion for the low-normal B12 on long-term metformin. The MRI now calls the three parietal microbleeds lobar, raising cerebral amyloid angiopathy, and drops the enhancement statement. Musts and prohibitions were rebuilt for this patient (vascular risk values, CPAP, driving and finances, no antimuscarinic for BPH); vascular cognitive impairment is moderate as a contributor.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonym re-run for the new `accepted[0]` (plan 5.1). The G31.84 entry currently grants "alzheimer disease", "alzheimer dementia", "dementia due to alzheimer", "posterior cortical atrophy", "benson syndrome", "early onset alzheimer" and the G30.x codes to this MCI case; those should not be accepted for an MCI label.
- New citation keys used: `[NIA_AA_MCI_2011]`, `[STRIVE_2013]`, `[BSH_B12_2014]`, `[Boston_CAA_2022]`, `[Beers_2023]` (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case beyond plan Q1 (2018 vs 2024 biological criteria); the text is written to be true under both.

## Verification
Adversarial check, 24 Oct 2026. Read the log, the diff and the whole final case.
- Notes: all five ids present; each FIXED claim holds in the file (label reframed with intermediate likelihood, drug check criterion, follow-up, initial and fallback outputs gone, two-alternative biomarker criterion with an authored PET answer, MCI prohibition and musts).
- Cross-field: MMSE arithmetic (date 1, recall 2, serial sevens 1 = 26/30) matches exam, assessment and neuropsych; CSF ratio 465/7800 = 0.060 matches; cueing field true matches 1/3 to 2/3 with cues; ECG fallback rate 70 vs HR 68; red-herring field paths point to the lacune and the OSA entries; MRI microbleeds lobar with no deep microbleeds; no post-contrast text; no 14-3-3 or RT-QuIC; no literature or drug output left; onset age 67, G31.84 correct for MCI.
- Found and fixed: informant finding dated the billing errors "six months ago" while the HPI says "over the past six months"; reworded to "in the past six months".
- Accepted as is: BMP under a CMP criterion (flagged by the worker, nothing depends on liver tests). The safety must cites [AAN_dementia_2018], whose counselling and functional-assessment recommendations cover it loosely; no change.
- perfect_agent.py ok; case_io.py check clean for this case; test_case_guards pass.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine_ESR_CRP` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (2 places: the labs criterion label and metadata), the wording the other six cases already use.
- `BMP` completed to `CMP` with normal liver tests (total protein 7.0, albumin 4.1, AST 22, ALT 25, ALP 81, bilirubin 0.7): the labs criterion orders a CMP, so the authored report has to carry the hepatic part; no field_path points into the panel.
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.
- This supersedes the worker's FLAGGED row on `labs.panels.BMP`: the liver values are the normal results a CMP order returns, not new findings, and every other CMP case in the condition carries them.
- Normal values in `Magnesium_homocysteine_ESR_CRP` varied (Magnesium 2.0 to 2.2, ESR 12 to 9, CRP 1.8 to 1.6), all still within the case's reference ranges: the same numbers (magnesium 2.0, homocysteine 10.2, ESR 12, CRP 1.8) had been copied into up to 13 cases, a template artefact raised by the S01 worker; no text cites the changed values.
- CBC indices made consistent (MCV = hematocrit x 10 / RBC): RBC 5.13 to 4.57, MCV 96.1 to 88.0; values within reference ranges and cited nowhere else in the case.
- Checks re-run after these additions: perfect_agent.py, case_io.py check and test_case_guards clean.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`apply_diagnosis_synonyms.py --prune --conditions alzheimers_early`): MCI labels only. Removed "alzheimer disease", "alzheimer's disease", "alzheimers disease", "alzheimer dementia", "dementia due to alzheimer", "posterior cortical atrophy", "benson syndrome", "early onset alzheimer" and the codes G30.0, G30.1, G30.8, G30.9, F00, because every "dementia due to Alzheimer disease" answer contains those tokens and would have scored an overcall of this MCI case as correct.
- Added follow-up `order_advanced_imaging` FDG_PET (trigger `order_fdg_pet`, no criterion), after the amyloid-status follow-ups: a case-specific Alzheimer-type metabolic report concordant with the MRI and stage. Before, an FDG order returned the library's normal scan, contradicting the case (summary Q4). Probed: FDG and amyloid PET orders each return their own report, in either order.
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-10-interpret-labs-mma]`.expected_evidence: was "Methylmalonic acid 0.17 umol/L, normal: no functional B12 deficiency"; now "Methylmalonic acid 0.17 umol/L, normal: no functional deficiency".
- Decision: reword evidence (cited result comes from another criterion's order). The criterion is the MMA order: the B12 level comes from the dementia screen order, so the evidence now reads only the MMA result and what it means.
- Scoring: none (evidence only; the reward does not read it).

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although this case contradicts it (diagnosis, history, medications or a stored finding) now get a case-specific report; every other off-pathway order still gets the library normal. No tier, criterion, diagnosis or existing output changed.

- `order_advanced_imaging modality=tau_PET` -> `followup_outputs[order_tau_pet]`: case-specific tau-positive flortaucipir PET with the distribution of the stored FDG-PET pattern.
- `order_advanced_imaging modality=perfusion_SPECT` -> `followup_outputs[order_perfusion_spect]`: regional hypoperfusion matching the stored FDG-PET hypometabolism.
- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: language findings of the stored neuropsychological battery (naming, fluency) in the speech-language format.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k ALZ-EARLY` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
