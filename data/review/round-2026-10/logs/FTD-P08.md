# FTD-P08
Reviewer status: R1 not reviewed (no FTD notes file), R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none | - | `data/review/round-2026-10/notes/` holds no FTD file; every change below is a lead-plan (`plans/FTD.md`) or own finding |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.action_criteria[action-4-order-specialized-test]`, `stop_rule` | Plan P08 / section 1.2 item 10: respiratory function required and in the stop rule, framed as diagnostic "given confirmed motor neuron disease" | FIXED: `recommended`, out of the stop rule, ALS-plan staging label, rationale and citations (`[AAN_2009]`, `[EAN_ALS_2024]`, `[NICE_NG42]`) |
| D | major | `followup_outputs[request_ftd_mnd_respiratory_function]` | Impression carried a management threshold ("NIV initiation threshold not yet reached") and `recommended_actions` a monitoring plan; MIP given against a %-predicted norm | FIXED: findings with ALS-plan reference ranges (FVC >=80%, SNIP >=60 cmH2O in women, MIP -60 cmH2O or more negative), reduced-category impression, actions emptied. Verified MIP -44 cmH2O, which meets an AAN 2009 marker |
| C | major | `ground_truth.assessment.required_recommendations` | Plan C9/P08: "given confirmed C9orf72 expansion" (optional result); "Order C9orf72 genetic testing" and "Perform EMG/NCS" (actions, not recommendations); FVC 50% threshold only; no MDT, riluzole or NIV must; the anxiety must duplicated a prohibition | FIXED: seven musts (ALS-FTD diagnosis with Rascovsky and Gold Coast evidence and disclosure; why anxiety and benign fasciculation syndrome do not explain it; MND MDT with speech and swallowing, dietetics, caregiver support and a behaviour plan without ChEI/memantine; discuss riluzole with LFT schedule; NIV referral on the MIP marker; safety and capacity; counselling before testing, with the brother and adult children) |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Plan C10 wording; CK prohibition worded as "Do not dismiss ... as a primary myopathy"; no NIV-delay prohibition although a marker is met | FIXED: C10 ChEI/memantine wording, benzodiazepine line keeps the respiratory risk, CK line reworded, ALS-plan PROHIB-RESP (reduced) added |
| D | major | `ground_truth.action_criteria[action-9-search-medical-literature]`, `initial_tool_outputs.literature_search` | Plan C1: literature required and in the stop rule; output keyed to the answer ("FTD-MND C9orf72"), empty summary, findings stating C9orf72 frequencies and survival | FIXED: canonical bvFTD text with the FTD-MND variant (`[Strong_2017]`), keyed "bvFTD with motor neuron disease"; criterion optional, last, `{}`; leak guard passes |
| B | major | `initial_tool_outputs.clinical_assessment` | Plan C3: hyperorality finding held the anecdote sentence, perseveration finding the repeated-questions sentence, executive finding cut at ";"; duplicated MoCA line; template impression | FIXED: one finding per feature (6 present), informant, screen (MoCA 23/30, FAB 12/18), functional decline; canonical impression |
| A/B | major | `initial_tool_outputs.labs` | Plan C5: one "Dementia_and_Metabolic_Workup" panel plus "Reviewed_FTD_panel_additions"; unrequested free T4 with a normal TSH, aldolase, magnesium and vitamin D; RPR/HIV in the baseline; no MCV, urea, eGFR, calcium, ALP, bilirubin, albumin | FIXED: standard panels with stored values kept and missing analytes added; CK in its own "Muscle enzymes" panel (ordered by the criterion); RPR/HIV moved to a keyed follow-up; the other extras deleted |
| B | minor | `patient.clinical_history.medications`, `.past_medical_history` | The HPI says magnesium was started and two antidepressant trials failed, but neither appears in the history | FIXED: magnesium oxide added to medications; the two trials (sertraline, then bupropion) added to the history |
| D | minor | `patient.history_present_illness`, `patient.neurological_exam` | Narrator hint "unaware of any genetic link between ALS and dementia"; "highly significant"; `additional` restated the history; interpretive "suggests mild retrieval deficit rather than storage failure" in the exam; jaw jerk repeated under motor; "Hoffman" | FIXED: hints removed; facts from `additional` (same two meals, repeated questions, recent-memory lapses) moved to the HPI; `additional` now holds the informant and weight; no dysphagia, weight loss or orthopnoea stated (bulbar and respiratory musts depend on it); "Hoffmann" |
| D | minor | `followup_outputs[request_optional_counselled_ftd_genetics]`, `[request_ftd_mnd_emg_ncs]`, `initial_tool_outputs.mri`, `followup_outputs[request_optional_fdg_pet]` | Template "Abnormal values: ..." genetics impression in capitals; "This is an ABNORMAL electrodiagnostic study"; unnumbered MRI and FDG impressions | FIXED: report-voice numbered impressions; genetics adds a post-test counselling note; EMG states no conduction block |
| B | minor | `followup_outputs[request_reviewed_neuropsych_battery]` | Bedside MoCA and FAB inside the battery; FBI and FrSBe as percentiles; "(neurologist's note)" cross-reference; impression cut without the canonical ending | FIXED: battery scores only, FBI total and FrSBe T-scores, canonical ending (C13) |
| C | minor | `ground_truth.action_criteria[action-8-order-advanced-imaging]`, `followup_outputs` | Plan C6: no perfusion SPECT alternative | FIXED: SPECT alternative with an authored follow-up concordant with the FDG result; FDG stays optional (the MRI already shows the pattern) |
| B | minor | `fallback_tool_outputs.ct`, `.advanced_imaging`, `.drug_interactions` | Plan C6 | FIXED: CT shows the MRI's frontal and anterior temporal atrophy (kind `case`); off-pathway advanced imaging and "agent not specified" drug check deleted (no drug criterion) |
| C | major | `ground_truth.differential` | Plan C11: "ALS without FTD" and frontal AD moderate after the work-up | FIXED: ALS without FTD low, AD low, anxiety or depression low, benign fasciculation syndrome very low; cervical myeloradiculopathy added very low; PSP to very low |
| D | major | `ground_truth.key_clinical_evidence` | Plan C12: "making respiratory function testing a load-bearing required step"; FDG line (optional result); "the puzzle is solved only by" essay voice | FIXED: seven lines (bvFTD criteria; Gold Coast with ALS-FTD per Strong 2017; NCS; anxiety; CK pearl; respiratory values with AAN markers; family history) |
| C | minor | `ground_truth.action_criteria[*]`, `avoided_actions` | Plan C4 labels and rationales; EMG cited only `[Bang_2015]`; labs cited `[AAN_dementia_2018]` | FIXED: canonical labels; EMG text and citations from plans/ALS.md C6 plus `[Strong_2017]`; labs `[NICE_NG97]`, `[SNLG_ISS_2024]`, `[EAN_ALS_2024]`; avoided CT cites `[NICE_NG97]` |
| C | minor | `ground_truth.action_criteria` order, `sequence_constraints` | Plan C15: no constraints | FIXED: order assessment, neuropsych, labs, MRI, EMG, respiratory, FDG/SPECT, genetics, literature; soft assessment before genetics `[ACMG_NSGC_2011]` and EMG before genetics `[EAN_ALS_2024]` |
| E | minor | `ground_truth.red_herrings`, `metadata` | Red herrings cited aldolase (now deleted) and a lab index; notes absent; citation gap text outdated | FIXED: red herrings reworded with the new field path; notes, difficulty rationale, educational points and citation gap rewritten |

## Changes, in one paragraph a physician can read before re-reviewing
This remains ALS-FTD in a 56-year-old woman whose fasciculations were blamed on anxiety. The patient block now records the magnesium she was given and the two failed antidepressant trials, and it states no choking, weight loss or orthopnoea. The informant assessment scores all six Rascovsky features. The blood panel is the standard set plus CK (318 U/L, 1.7x ULN); syphilis and HIV serology answer only a targeted order. EMG stays required. Respiratory function is now recommended staging rather than a required diagnostic step. Its report gives values against reference ranges and has no management advice: FVC 72% upright and 63% supine, SNIP 52 cmH2O, MIP -44 cmH2O. FDG-PET (or SPECT), the counselled FTD-ALS panel (C9orf72 expansion) and literature stay optional, and genetics comes after the clinical assessment and EMG. The musts no longer assume a genetic result. They ask for:
- the ALS-FTD diagnosis and its disclosure;
- why anxiety does not explain it;
- an MND multidisciplinary team with speech and swallowing care and caregiver support;
- a discussion of riluzole with liver monitoring;
- NIV referral now, because the MIP meets an AAN 2009 marker;
- safety and capacity;
- counselling for her brother and adult children.

ALS without dementia and frontal AD are now low in the differential.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms (plan section 5 item 3): add "ALS-FTD", "FTD-ALS", "FTD with motor neuron disease", "ALS with frontotemporal dementia", "ALS-FTSD" for this case, and decide whether G12.21 is an accepted secondary code.
- Citation keys used that the criteria pack does not list: `[SNLG_ISS_2024]`, `[Strong_2017]`, `[ACMG_NSGC_2011]`, `[NICE_NG97]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[AAN_2009]`, `[Gold_Coast_2020]`, `[Awaji_2008]`.
- `condition_tool_guidance.yaml` `ftd:`: record P08 respiratory function as recommended, plus EMG as required (plan section 5 item 6).

## Open questions for Andrea (judgment calls you could not settle)
- The NIV must quotes MIP -44 cmH2O, which comes from the recommended (not required) respiratory test. Plan P08 asked for this wording once the cmH2O value was verified, but C9 says no must should depend on a non-required result. Two options: keep it (current), or use "Arrange respiratory follow-up and discuss NIV when markers are met" so that an agent who skips the test is not penalised.
- The case has seven musts, above the plan's 4 to 6. Plan P08 itself adds the MDT, riluzole and NIV musts; I folded caregiver support and speech and swallowing care into the MDT must instead of adding more.

## Verification
Adversarial verifier, 24 Oct 2026. There is no FTD notes file. I read the log, the diff and the whole final case.

Confirmed:
- Gold Coast wording is correct.
- AAN 2009 NIV markers: FVC <50%, SNIP <40 cmH2O, MIP weaker than -60 cmH2O, orthopnoea, nocturnal oximetry.
- The riluzole monitoring matches the SmPC: ALT monthly for 3 months, then 3-monthly for the first year; stop above 5x ULN; neutropenia warning.
- EMG stays required and precedes genetics. Respiratory function is recommended and out of the stop rule.
- Magnesium and the antidepressant trials are now in the history.

Found and fixed:
1. Major, class: `genetic_panel:FTD` is the most likely genetic order in an FTD case. The library answered it "C9orf72 repeat length normal", which contradicts the case. Added it as a second alternative of `action-5-order-specialized-test`, with follow-up `request_optional_counselled_ftd_gene_panel`: the same >600-repeat expansion, GRN and MAPT negative. Label and expected evidence are adjusted to cover both panels.
2. Major: `patient.neurological_exam.mental_status` contradicted itself and the total. "2 on delayed recall (recalls 1/5 at 5 minutes)" is impossible, because a recall of 1/5 loses 4 points. With 3 executive points and 1 for abstraction, the losses could not sum to MoCA 23/30.
   - Now: recall 3/5 (the other 2 recognised with cues) and 2 points on abstraction. That gives 3 + 2 + 2 = 7, so 23/30 holds. It also fits the neuropsychology, where delayed free recall is at the 22nd percentile and recognition at the 85th.
   - The clinical-assessment executive finding and the bedside-screen line were changed to match.
3. Minor: the respiratory report called 2.58 to 2.24 L "a fall of 13 percentage points". It is 9 points of % predicted (72 to 63), or a 13% relative fall. It now reads "a 13% fall on lying flat".
4. Worker open question settled (C9: no must may depend on a non-required result): the NIV must now asks for the baseline respiratory assessment, referral and an NIV discussion once an AAN marker is met. It adds "if measured, the MIP of -44 cmH2O already meets one, so referral is due now". An agent that skipped the recommended test is no longer held to a value it never saw. The 7-must count is kept, since plan P08 itself adds the MDT, riluzole and NIV musts.

- Checks run after the changes: `perfect_agent.py -v` passes, `case_io.py check` names no failure for this case, `test_case_guards` (leak, followup, banned-string) passes. I also called the MockServer directly with FDG_PET, perfusion_SPECT, amyloid_PET, DaTscan, CSF AD markers, genetic_panel:FTD and genetic_panel:ALS, emg_ncs, respiratory_function, the neuropsych battery, targeted RPR/HIV, the baseline labs, CT and literature, to check that every plausible order gets a report consistent with the case.

For the FTD lead (class): any FTD case with an authored genetic result has the same defect if it authors only one of `genetic_panel:FTD` / `genetic_panel:ALS`. The library answers the other one with a normal C9orf72 and a normal panel. Check the other C9orf72 cases (for example M02, S03, S05, S10) and every case whose authored panel is positive.
