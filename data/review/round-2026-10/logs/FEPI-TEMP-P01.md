# FEPI-TEMP-P01
Reviewer status: R1 none, R2 none (no notes file for FEPI-TEMP) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case. The physician input for FEPI-TEMP is the July 2026 tool guidance (plan 1.3), applied through the plan.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | blocker | `initial_tool_outputs.mri` (plan P01) | The MRI was reported "MRI-negative ... no cortical malformation" while the label says "suspected focal cortical dysplasia on 3T epilepsy-protocol MRI"; gadolinium line in a non-lesional study; asymmetry index 0.03 does not match 3.2/3.3 cm3. | FIXED: 3T epilepsy-protocol technique line (no contrast); new first finding of subtle right temporal pole gray-white blurring with subcortical FLAIR hyperintensity, suspicious for FCD; the two nonspecific white matter foci kept (enhancement line deleted, differential essay replaced by one observation); index -0.015 by (L - R)/(L + R); numbered impression. |
| C | major | `ground_truth.diagnosis.accepted[0]`, `icd_codes[0]` (plan 5.4) | "Drug-resistant" and `G40.219` although she has never taken an antiseizure medication. | FLAGGED: label not edited by workers; CENTRAL request 4 (plan decision). |
| B | minor | `patient.history_present_illness`, `social_history.occupation` (plan R) | Surname "Delgado" duplicates M01 (also a teacher); occupation "graduate student" vs teacher in the HPI. | FIXED: "Ms. Montoya" (unused in the dataset); occupation "Elementary school teacher (currently on medical leave)". |
| B | minor | `followup_outputs` drug check | Penicillin allergy written as "hives" (patient lists "rash"); claim that female sex and age under 30 are rash risk factors for lamotrigine; dicyclomine not checked. | FIXED: "rash"; claim deleted; dicyclomine line; ethinylestradiol effect on lamotrigine stated per fact 8; oxcarbazepine contraceptive effect added. Criterion optional with the canonical evidence. |
| E | minor | `followup_outputs` neuropsychology | Impression in lab voice ("Abnormal values: ... (H) ... (L)"); PRI 114 flagged abnormal. | FIXED: neuropsychologist's summary; PRI `abnormal: no` (high average is not a deficit). |
| D | minor | `followup_outputs` FDG-PET | "Asymmetry index 0.82 (normal >0.90)" is a ratio. | FIXED: uptake ratio 0.84 (also no longer shared with other cases). Optional. |
| D | minor | `followup_outputs` video-EEG | Ictal semiology missing; impression ends with a comparison line to the routine EEG. | FIXED: semiology of both seizure types in `clinical_correlation`; comparison line removed (the interictal finding still notes the variants on the prior routine EEG). |
| D | minor | `initial_tool_outputs.eeg.artifacts[1]` | Teaching remark ("could be confused ... by less experienced readers"). | FIXED: report voice. |
| C | major | `followup_outputs` literature (plans A, O) | Required; Beyenburg 2005 with a wrong journal entry, a Psychiatric Times piece and "So & Lee, Epilepsia 2014" (not verifiable); empty summary. | FIXED: optional and last; Fisher 2017, Bernasconi 2019, Blumcke 2011; general summary. |
| B | minor | `initial_tool_outputs.ecg` | Interval set shared with other cases. | FIXED: 84/min, PR 148, QRS 86, QTc 414. |
| A | major | `ground_truth.action_criteria` (plans E, H, T, 3.2) | MRI `contrast: true`; literature, drug check, ECG required; PET recommended; doubled citations; template evidence. | FIXED: MRI `{protocol: epilepsy}`, routine EEG and video-EEG required; ECG, PET, neuropsychology, drug check, literature optional; one key each; evidence from the stored reports; order MRI, routine EEG, video-EEG, ECG, PET, neuropsychology, drug check, literature; `followup_outputs` in the same order. |
| A | major | `ground_truth.sequence_constraints`, `stop_rule` (plans C, D) | Template MRI -> drug check constraint; stop rule with literature, drug check, ECG, max 0. | FIXED: constraint deleted; stop rule MRI, routine EEG, video-EEG, max 2. |
| C | major | `ground_truth.assessment` (plan L) | Musts applied drug-resistance criteria, presurgical referral, video-EEG, 3T MRI and PET (work-up, and wrong: no ASM ever given); prohibition about a "third AED". | FIXED: musts lamotrigine first line (anxiety disorder, sertraline compatible), contraception and folic acid, revisit the panic diagnosis with psychiatry, taper as-needed lorazepam, driving (she still drives); prohibitions: escalating anxiolytics, accepting the normal routine EEG, LP, valproate. No SUDEP must (no tonic-clonic seizures, not drug-resistant). |
| C | major | `ground_truth.differential` (plan P) | Panic disorder and PNES `moderate` after video-EEG captured five electrographic seizures; tumor entry reasons from a "normal MRI"; cardiac mimic raised by the history (MVP, palpitations) absent. | FIXED: panic `low`, PNES `very_low`, with the excluding findings; tumor and LGI1 entries rewritten from the case data; arrhythmia entry added (`very_low`, normal Holter and ECG). |
| C | major | `ground_truth.key_clinical_evidence` (plan G, S) | Drug-resistance and PET-for-MRI-negative lines contradict the case; "most common cause of medically refractory panic" overclaims; engineering lines. | FIXED: rewritten from the case data (semiology, ictal fear vs panic, normal routine EEG, MRI, never on an ASM). |
| C | minor | `ground_truth.red_herrings` | The benign-variant routine EEG, the case's main EEG pitfall, had no red herring. | FIXED: added at `initial_tool_outputs.eeg.findings[0]`; the existing HPI red herring still holds its data point. |
| C | minor | `ground_truth.avoided_actions` | Template rationales. | FIXED: case-specific (prior echo with MVP, normal Holter already done); all four wastes kept. |
| B | minor | `metadata.red_herrings`, `case_body_concerns`, `difficulty_rationale` | Listed a prolactin level and a urine drug screen that the case does not contain, an "MRI-negative" study and "two failed AEDs"; resolved occupation audit flag. | FIXED: those entries removed or rewritten; the drug-resistance audit flag kept until CENTRAL changes the label. |
| A | minor | `fallback_tool_outputs.echo` | No `echo_type`. | FIXED: `TTE`. |

## Changes, in one paragraph a physician can read before re-reviewing

Ms. Montoya (renamed from a duplicate), a 29-year-old teacher, has two years of ictal fear, epigastric rising, olfactory hallucinations and episodes with automatisms and postictal confusion, treated as refractory panic disorder; she has never taken an antiseizure medication. The policy requires the epilepsy-protocol MRI, the routine EEG and video-EEG; ECG, FDG-PET, neuropsychology, drug check and literature are optional, and the stop rule allows two extra actions. The MRI now matches the label: a 3T epilepsy-protocol study with subtle right temporal pole gray-white blurring and subcortical FLAIR signal suspicious for focal cortical dysplasia, normal hippocampi and two incidental white matter foci. The routine EEG remains normal with benign variants (now a red herring); video-EEG captured five right anterior temporal seizures. Drug-resistance and presurgical musts were removed: musts are lamotrigine as first line (anxiety disorder, sertraline compatible), contraception and folic acid, revisiting the panic diagnosis with psychiatry, tapering lorazepam, and driving advice; valproate and anxiolytic escalation are prohibited. Panic and PNES are now `low` and `very_low`, and an arrhythmia entry reflects the normal Holter and ECG. Literature cites real ILAE sources.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Label (plan 5.4): accepted[0] "Focal epilepsy of right temporal lobe origin with suspected focal cortical dysplasia on 3T epilepsy-protocol MRI, misdiagnosed as refractory panic disorder", `icd_codes[0]` `G40.209`; `G40.219` (intractable) is wrong because no ASM was ever given. The case data now support every other part of the current label.
- Synonyms (plan 5.6): "mesial temporal lobe epilepsy" and "mesial temporal sclerosis epilepsy" are wrong for a temporopolar dysplasia with normal hippocampi; idiopathic `G40.009`/`G40.019`.
- Citation keys outside the pack allow-list used per plan 1.1: `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[NICE_NG217_2025]`.
- `perfect_agent.py -v` prints `<- ?` for the MRI because of a null `size` in the hippocampal finding (exclude_none comparison); the environment serves the stored MRI (checked directly). Cosmetic tool issue.

## Open questions for Andrea (judgment calls you could not settle)

None. Decisions: lamotrigine is named in the must rather than "lamotrigine or levetiracetam" because her anxiety disorder makes levetiracetam's psychiatric adverse effects relevant (plan: "first-line ASM (lamotrigine, sertraline compatible)"); PNES is `very_low` rather than `low` because all five habitual events had an electrographic onset; no surgical referral must, since she is not drug-resistant (FDG-PET and neuropsychology stay optional for a later presurgical work-up).

## Verification

Adversarial check, 24 Oct 2026 (uncommitted diff read in full against fa1d22e6).
- Checked: rename (Montoya) and occupation agree; the MRI now shows the suspected right temporopolar FCD with normal hippocampi (index -0.015 matches 3.2/3.3 cm3) and no contrast; video-EEG counts (3 focal aware + 2 focal impaired-awareness = 5) agree across the findings, impression, criterion evidence and differential; penicillin "rash" is consistent; no drug-resistance, presurgical or SUDEP must; lamotrigine must matches the drug output and titration; the lorazepam taper and the panic re-evaluation are present; differential tiers reflect video-EEG; red herrings hold; tiers and stop rule per plan; the label stays for CENTRAL 4.
- Found: the FDG-PET uptake ratio 0.84 duplicated M03's fallback PET (0.84), although both logs claimed their value was unique; `metadata.last_revised` (2026-08-10) and `revision_reason` were not updated.
- Changed: PET uptake ratio 0.83 in `followup_outputs[1]` (finding and impression) and in `action-6-order-advanced-imaging.expected_evidence`; `metadata.last_revised` 2026-10-24 with a revision reason for this round. `perfect_agent.py -v` and `case_io.py check` clean; case guards pass.

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.
- Video-EEG follow-up and criterion: "rare" discharges at 2-8 per hour are "occasional" (ACNS 2021: rare is under 1 per hour).
- Literature follow-up (served for any query): the FCD classification result with temporopolar blurring and the summary line on "subtle focal cortical dysplasia" pointed at this case's MRI finding; removed, MRI-protocol result now names HS and FCD together.

## Close-out (24 Oct 2026)

Condition close-out (`plans/FEPI-TEMP-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G40 entries, re-applied with `--prune --conditions focal_epilepsy_temporal`): labels now focal epilepsy, temporal lobe epilepsy, TLE, epilepsy temporal lobe; removed mesial temporal sclerosis epilepsy (no hippocampal sclerosis on MRI); mesial temporal lobe epilepsy (the onset zone is not mesial); focal seizures; focal onset seizures; focal impaired awareness seizures (seizure-type labels, retired: their tokens occur in an acute symptomatic or functional-seizure answer). Codes: G40.2, G40.1, G40.9 plus G40.209, G40.109, G40.909 (not intractable); the idiopathic G40.009 and G40.019 removed and the intractable codes removed.
- Label (summary CENTRAL 4): "drug-resistant" removed (no ASM ever given): accepted[0] "Focal epilepsy of right temporal lobe origin with suspected focal cortical dysplasia on 3T epilepsy-protocol MRI, misdiagnosed as refractory panic disorder"; icd_codes[0] G40.219 -> G40.209. The resolved AUDIT-FLAG removed from `metadata.case_body_concerns`.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FEPI-TEMP-` passes, now with the discriminator guard and the FEPI-TEMP banned strings.
