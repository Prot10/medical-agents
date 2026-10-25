# FTD-P01
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for FTD) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes exist for FTD. The physician input is Reviewer 1's July 2026 tool rulings (`condition_tool_guidance.yaml` `ftd:`), applied through plans/FTD.md. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `action-9-check-drug-interactions`, `initial_tool_outputs.drug_interactions` | The drug-interaction tool was used as a toxicity test. Its required arguments included a free-text `indication` that no call can match. Its output held the valproate level, ammonia and liver results, plus a doctor's plan with L-carnitine doses and ChEI text (C2). | FIXED: the criterion id is kept, now `interpret_labs [valproate_level, ammonia]`, required. A keyed follow-up `request_valproate_level_ammonia` holds the authored values (trough 68 mcg/mL, ammonia 38 mcg/dL, liver chemistry normal). The same panel sits in the initial labs so that a combined order returns it. The drug-check output and the "agent not specified" fallback are deleted. |
| B | major | `initial_tool_outputs.labs` | C5: no folate, platelets, LFTs (other than inside the drug output), calcium or albumin; CBC/BMP-prefixed names; `Reviewed_FTD_panel_additions`; unrequested copper and ceruloplasmin; free T4; RPR and HIV with no risk factor. The ammonia reference range was 11-35 in the labs but "about 32" in the drug output. | FIXED: rebuilt per C5 with the case values (WBC 6.4, Na 139, creatinine 0.9, TSH 2.6, B12 514, ESR 11, CRP 1.6); missing analytes added as normal. A "Valproate and ammonia" panel was added with a single 11-35 range. Copper, ceruloplasmin and free T4 deleted. RPR/HIV moved to keyed follow-up `request_rpr_hiv_serology`. |
| D | major | `patient.history_present_illness`, `.neurological_exam.mental_status`, `.additional` | The MoCA 26/30 with item losses, and the synthesis "This score is NEAR NORMAL; it significantly underestimates...", appeared in the HPI, the exam and `additional`. | FIXED: the score is removed from the patient block and returned by `perform_clinical_assessment`. `additional` now holds exam content (informants, no asterixis or myoclonus). |
| D | major | `patient.clinical_history.family_history` | "Possible FTD misdiagnosed as schizophrenia" gave the agent the inference the case tests. | FIXED: removed; the father's history is kept as given. |
| B | major | `initial_tool_outputs.clinical_assessment` | C3 template: informant false although two informants give the history; apathy false despite loss of all interest in the literary community; the fixed meals were scored as dietary change; the findings were cut-off HPI sentences; the screen line was duplicated. | FIXED: one finding per feature. Present: disinhibition, apathy, stereotyped behaviour and a dysexecutive bedside profile, so 4 of 6. Empathy not established. Dietary change absent (the fixed meals are a ritual). Informant, psychiatric-history, screen and function lines added. Informant true. Canonical impression. |
| B | major | `initial_tool_outputs.mri`, `action-6-analyze-brain-mri` | The MRI expected evidence asked for "bilateral frontal and/or anterior temporal atrophy" against a normal MRI. The report had no findings entries and an unterminated impression. | FIXED: the report has a frontal/temporal finding (volumes in the lower range for age, no definite lobar atrophy) and a hippocampal/posterior finding, with a numbered impression. The expected evidence now matches the report. |
| C | major | `action-7-order-advanced-imaging` | FDG-PET was optional, so with a normal MRI the policy could only reach possible bvFTD while the label says probable. There was no SPECT alternative and the advanced-imaging fallback was off-pathway (C6, C7). | FIXED: recommended (plan C7, Q2), with a `perfusion_SPECT` alternative and authored follow-up `request_perfusion_spect`. The FDG report is rewritten in modality voice with values unchanged, and its impression states that the pattern is consistent with FTLD. Fallback deleted. |
| A | major | `action-8-search-medical-literature`, literature follow-up | Literature was required, query-specific and in the stop rule (C1). The follow-up had an unverifiable PMID and title, a "mean diagnostic delay of 3-5 years", and text echoing the case ("Normal MRI ... should trigger FDG-PET"). | FIXED: optional, `required_arguments: {}`, last, out of the stop rule. A canonical output combining the psychiatric-mimic and familial variants (`[Ducharme_2020]`, `[Pottier_2016]`) is in `initial_tool_outputs.literature_search`. The follow-up is deleted. |
| D | minor | `followup_outputs` neuropsych | No domain keys; capitals and claims such as "masking real impairment" and "the key diagnostic finding"; no memory or visuospatial domain, although the criterion's evidence rests on their sparing (C13). | FIXED: one domain per finding, existing scores unchanged. Added normal episodic memory (RAVLT) and figure copy, consistent with the bedside 4/5 recall and normal clock. The MoCA repeat line was removed. C13 ending. |
| D | minor | `followup_outputs` genetic panel | Template impression ("Abnormal values: ... (H)"); em dashes. | FIXED: per-gene report, heterozygous C9orf72 expansion (result unchanged), inheritance and counselling sentence. |
| C | major | `ground_truth.assessment` | Musts: "FDG-PET and genetic testing are diagnostic" (genetics is optional and not needed for the clinical diagnosis); duplicate template musts; no must on valproate continuation; template prohibitions (C9, C10). | FIXED: five musts. (1) Rascovsky with certainty level and normal-MRI point. (2) Why bipolar relapse does not explain it, coordinating with psychiatry. (3) Valproate toxicity excluded, so continue it. (4) Safety and capacity for a man living alone. (5) Genetic counselling before testing. Canonical ChEI/memantine texts; antipsychotic and benzodiazepine kept; added "do not stop or switch valproate on the mildly raised ammonia alone". |
| C | major | `ground_truth.differential` | Bipolar relapse rated "high" and AD and valproate "moderate" after a work-up that excludes them; "Familial bvFTD" listed as a competing diagnosis although it is the diagnosis itself (C11). | FIXED: bipolar relapse low, valproate hyperammonaemia very low, AD very low, primary psychiatric very low, each with the excluding data; the familial entry removed (it is the diagnosis; the genetics criterion covers it). |
| C | minor | `key_clinical_evidence`, `red_herrings`, `metadata` | KCE lines cited the "criteria pack" and the July review. Notes said "social cognition testing is pathognomonic" and "C9orf72 is the normal-MRI FTD mutation". `fallback_tool_kinds` listed deleted fallbacks. | FIXED: five KCE lines from the pathway's results. The ammonia red herring was added (`initial_tool_outputs.labs.panels.Valproate and ammonia[1]`). Notes and difficulty rationale rewritten: C9orf72 is kept, because the case does author a C9orf72 result, and is described as associated with slow progression and little atrophy. Kinds pruned. |
| C | minor | criteria text, citations, constraints, fallbacks | `rationale` was a copy of `label`; free-text citation duplicates; `[AAN_dementia_2018]` on the labs, the valproate criterion and CT; the perfusion-MRI rationale assumed FDG had been done; the CT fallback did not say CT is insensitive; the CSF fallback had empty `special_tests` (C4, C15). | FIXED: canonical labels with case rationales; `[NICE_NG97]`/`[SNLG_ISS_2024]`; soft constraint clinical assessment before genetic panel (`[ACMG_NSGC_2011]`). Order: assessment, neuropsych, labs, valproate/ammonia, MRI, FDG (recommended), genetics (optional), literature (optional). CT fallback impression completed; CSF fallback deleted. |

## Changes, in one paragraph a physician can read before re-reviewing

A 54-year-old novelist with bipolar II, stable on valproate for 15 years, has had 18 months of disinhibition, loss of interest, stereotyped writing, television and eating rituals, and loss of insight. His former partner and his publisher give the history. His father was institutionalised in his 50s with "schizophrenia". The patient block no longer prints the MoCA or the inference that the father had FTD. The required pathway is: informant-based assessment (4 of 6 Rascovsky features; MoCA 26/30), neuropsychology (severe social-cognition and real-world executive impairment, memory and visuospatial function normal), the reversible-cause blood panel (normal), and valproate level with ammonia. The valproate step is now ordered as a lab test rather than a drug-interaction check: the trough is therapeutic and ammonia is only mildly raised. MRI is normal. FDG-PET or perfusion SPECT is now recommended, because with a normal MRI it is the imaging support that probable bvFTD needs; it shows right-predominant frontal hypometabolism. Counselled genetic testing (C9orf72 expansion) and literature are optional. The musts ask for the certainty level, why bipolar relapse and valproate are excluded, continuation of valproate, safety and capacity for a man living alone, and counselling before genetic testing.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- The criterion id `action-9-check-drug-interactions` is kept (plan) although the criterion is now `interpret_labs`. Rename it to `action-valproate-level-ammonia` if ids are allowed to change in a later round.
- `condition_tool_guidance.yaml` `ftd:`: record FDG-PET as recommended in P01 (plan Q2, departing from Reviewer 1's "optional").
- Citation keys used: `[NICE_NG97]`, `[SNLG_ISS_2024]`, `[Ducharme_2020]`, `[Pottier_2016]`, `[ACMG_NSGC_2011]`, `[Foster_2007]`. The valproate criterion carries no key.

## Open questions for Andrea (judgment calls you could not settle)

- Plan Q2 (FDG-PET recommended with a normal MRI) is applied as the plan proposes. If you keep Reviewer 1's "optional", revert `action-7-order-advanced-imaging.importance` and the musts still hold.
- The plan said the notes mention C9orf72 "although no genetic result is authored". In fact a C9orf72 expansion is authored in the optional genetic follow-up, so the mention was kept and reworded rather than removed. With that result the case would reach definite bvFTD (Rascovsky 2011), while `accepted[0]` says probable. I left `accepted[0]` unchanged, as required, and the musts ask for "probable ..., definite if a pathogenic variant is found".
- Two normal neuropsychology domains (RAVLT delayed recall 11/15, Rey copy 34/36) were authored so that the battery shows the memory and visuospatial sparing that the criterion and the Rascovsky feature rely on.

## Verification

`perfect_agent.py FTD-P01 -v`: ok. Assessment, labs and MRI come from `initial_tool_outputs`; neuropsych, valproate/ammonia and FDG from `followup_outputs[0,1,3]`. Probes: a valproate/ammonia order reaches its follow-up; a baseline order returns the C5 panels; RPR/HIV, perfusion SPECT and the gene panel reach their follow-ups; a valproate drug check reaches the library ("no interaction"); any literature query returns the canonical output. `case_io.py check FTD-P01`: schema OK, and no failure names the case. `test_case_guards -k FTD-P01`: 2 passed. No em dashes remain.

## Verification (adversarial verifier, 24 Oct 2026)

Note: the section above was written by the worker as a self-check; this is the independent verification. Checked against the pre-round file, the plan (P01, C2, C7) and the whole final case: patient diff (MoCA and the "misdiagnosed FTD" inference removed), the valproate criterion now `interpret_labs [valproate_level, ammonia]` (id kept), FDG recommended with the SPECT alternative, MoCA 26/30 arithmetic (4 single-point losses), musts versus the valproate prohibition (consistent), differential and red herrings. MockServer probes: valproate first or second, baseline and CT all reach the intended outputs.

Found and fixed:
- B major, ammonia unit (labs panel and follow-up, `abnormal_values_summary` twice, the criterion's expected evidence, the red-herring data point): 38 "mcg/dL" with a reference range of 11-35, which is the umol/L range (the mcg/dL range is about 15-60, so 38 mcg/dL would be normal). Unit set to umol/L everywhere; 38 umol/L stays mildly raised.
- B minor, `fallback_tool_outputs.ct`: a 3 mm calcified right frontal granuloma that the MRI does not show (same class as plan C6 for S04). Removed; impression completed; `fallback_tool_kinds.ct` "incidental" -> "normal".
- C minor, must 1: the certainty level presumed the recommended FDG result ("probable with frontal hypometabolism"). Now "possible on the clinical features with a normal MRI; probable once functional imaging shows frontal hypometabolism; definite if a pathogenic variant is found" (plan C9: no must depends on a non-required result).
- C minor, KCE 5 stated the optional gene result (C12). Now supports offering counselling, testing optional.
- C minor, literature source: Pottier 2016 title corrected to "Genetics of FTLD: overview and what else we can do with genetic data" (J Neurochem 138 Suppl 1:32-53).

`perfect_agent.py FTD-P01 -v`: ok. `case_io.py check FTD-P01`: schema OK, no failure names the case. `test_case_guards -k FTD-P01`: passed.

## Condition audit (FTD auditor, 24 Oct 2026)

- B, major, `followup_outputs`: an order of `genetic_panel:ALS` fell to the benchmark library, which reports a normal C9orf72 and so contradicted the expansion on this case's FTD panel. Added follow-up `request_als_gene_panel_c9orf72` (`test_type: genetic_panel:ALS`) with the same C9orf72 expansion and SOD1, TARDBP and FUS negative, as P04 and P05 already have. No criterion changed. FIXED.
- `perfect_agent.py` and `case_io.py check` were re-run on all 30 FTD cases after the changes and are clean; `test_case_guards.py -k FTD` passes (60 tests).

## Close-out (24 Oct 2026)

Decisions in `plans/FTD-decisions.md`. Changes:

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (the report is a transthoracic study). The MockServer routes echo reports by this field; without it the normal TTE fallback answered a TEE order too (PATTERNS section 5; FTD added to `DISCRIMINATOR_CONDITIONS`).
- Criterion id `action-9-check-drug-interactions` -> `action-valproate-level-ammonia` (the criterion orders interpret_labs, not a drug check; stop rule updated); summary CENTRAL 9.
- Synonyms (`G31.09` entry, applied with `--prune --conditions ftd`): "pick disease" and "pick's disease" (retired) and the code G31.01 are no longer accepted. Pick disease is one FTLD-tau pathology that no case establishes, and G31.01 is where ICD-10-CM codes primary progressive aphasia, so a PPA answer coded G31.01 scored as correct here.

Checks: `perfect_agent.py` and `case_io.py check` clean; `test_case_guards.py -k FTD-` passes, including `test_routed_outputs_name_their_study`.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although this case contradicts it (diagnosis, history, medications or a stored finding) now get a case-specific report; every other off-pathway order still gets the library normal. No tier, criterion, diagnosis or existing output changed.

- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: speech-language findings matching the stored neuropsychology (reduced verbal fluency; naming as tested).
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[order_performance_status]`: performance status of the case's functional decline instead of Karnofsky 100.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k FTD` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
