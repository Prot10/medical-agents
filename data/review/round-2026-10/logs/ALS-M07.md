# ALS-M07
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 27fe005e-a718-4108-aca8-c77a7b4ca8ab | FIXED | Plan C1/C2: `ground_truth.action_criteria` reordered (EMG, brain MRI, spine MRI, labs first); `followup_outputs` now respiratory, genetics, riluzole; literature follow-up `search_lead_toxicity_als` and criterion `action-1-search-medical-literature` deleted; `sequence_constraints` EMG before genetics and riluzole |
| 30c38fd0-2fc6-432f-84b8-312ca957e8d3 | FIXED | Literature step deleted (C2). Targeted test added: `initial_tool_outputs.labs.panels["Blood lead"]` = 24 mcg/dL (ref <5, abnormal), consistent with the prior 28 mcg/dL in the HPI; reported in `abnormal_values_summary` and `interpretation` (C13) |
| 308c92ea-5846-4b3a-b4e3-30691890bd4a | FIXED | Riluzole check moved last (criterion order and follow-up order) with soft constraint `action-6` before `action-2`; criterion label/rationale/expected_evidence/citations rewritten (C3) |
| 77d7fcd4-8486-4032-b6d4-55294300d585 | FIXED | Genetic follow-up `impression` replaced by the canonical negative text; `findings` now list C9orf72 and SOD1, TARDBP, FUS, TBK1 separately, all negative; `recommended_actions` emptied (trial/therapy text removed) (C5) |
| fddd54d3-679b-441d-b6f7-d44432ece288 | FIXED | Respiratory follow-up moved after the diagnostic core (first follow-up, after EMG/MRI/spine/labs criteria); criterion relabelled as staging, `recommended`; output reference ranges and impression per C4 (normal category) |
| 8e2d2d77-b90d-47c8-8c86-1c2e2844cf9f | FIXED | Blood lead added to the labs (see 30c38fd0). `red_herrings[0]` rewritten with the note's reasoning (no UMN signs from lead; multi-region anterior horn cell denervation, normal sensory studies, no conduction slowing or block); `differential[0]` lead neuropathy moderate -> low with the same reasoning; new must (occupational health, follow blood lead) and new prohibition (no attribution to lead, no chelation); key evidence pearl on lead |
| dc07427d-dc87-48ba-88f4-251cfb917757 | FIXED | Riluzole output rewritten: "AMX0035 if alcohol cessation not achievable" removed (`alternatives` = []); wrong claim "alcohol ... via CYP1A2 inhibition" removed; alcohol line now: light intake, avoid heavy drinking because riluzole can raise transaminases; canonical monitoring summary |
| 2308b1c4-78be-4366-9e6d-287156990a1a | FIXED | Same as 27fe005e: core block (EMG/NCS, brain MRI, spine MRI, targeted labs) is criteria 1-4; follow-ups hold only respiratory, genetics, riluzole |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | Synthesis sentence "Examination shows combined upper and lower motor neuron signs." in the HPI | FIXED: deleted (C11) |
| B | minor | `patient.clinical_history.past_medical_history` | "Obesity class I" contradicts BMI 27.2 | FIXED: "Overweight (BMI 27)" |
| D | minor | `patient.clinical_history.social_history.occupational_exposures` | "occupational ALS risk factors reported" names the diagnosis in the patient block | FIXED: "Heavy metal (lead, mercury) and combustion product exposure during firefighting; formaldehyde" |
| B | major | `initial_tool_outputs.mri` | Brain report held spine content (L5-S1) and cross-modality "lead encephalopathy" statements; impression omitted its own corticospinal finding | FIXED: brain-only report, numbered impression (C12) |
| B | major | `initial_tool_outputs.body_imaging` | Region "cervical and thoracic spine" but the only finding was L5-S1; JSON dump in `description`; nothing said about the cord | FIXED: region "cervical, thoracic and lumbosacral spine", plain findings for cervical cord, thoracic cord/conus and L5-S1, numbered impression |
| B | minor | `initial_tool_outputs.specialized_test` | Impression claimed positive sharp waves and active plus chronic change in the thoracic region, findings show only fibrillations there; cross-step "Pulmonary function testing recommended." | FIXED: impression matches findings; "no conduction block and no temporal dispersion" added to motor NCS; recommended_actions emptied (C6) |
| A/B | major | `initial_tool_outputs.labs` | "Exclusion studies" with Free T4 as a string and a case-level significance sentence; "Reviewer baseline rule-out additions" panel name; interpretation names ALS; no renal, liver, electrolyte or WBC/platelet values although CBC and CMP were required | FIXED: panels rebuilt per C13 (stored values kept; added normal WBC, platelets, CMP, free T4 1.2 ng/dL; potassium 3.8 low-normal on hydrochlorothiazide), canonical interpretation |
| C | major | `ground_truth.action_criteria` | Brain MRI required `contrast: true, protocol: standard` (a correct non-contrast MRI failed); spine required `contrast: false`; labs required 9 panels by exact spelling; label = rationale everywhere; mixed citations | FIXED: C16 arguments, canonical labels/rationales/citations, case expected_evidence |
| C | major | `ground_truth.assessment` | Musts were diagnostic actions and generic; "androgen receptor CAG repeat" lab must; generic prohibitions (cervical surgery without spondylosis, functional dismissal without psychiatric history) | FIXED: rebuilt per C10 (DX, RESP normal, BULBAR signs, RILUZOLE, MDT, GEN, lead must); prohibitions IMM, RESP normal, lead/chelation |
| C | minor | `ground_truth.assessment.required_recommendations[1]` | He has CPAP-treated obstructive sleep apnoea, which can mask nocturnal hypoventilation | FIXED: one sentence added to MUST-RESP |
| C | major | `ground_truth.differential` | Lead neuropathy left moderate; MMN key_features cited "anti-GM1 negative" (never tested); blood lead key_features cited a test not in the work-up | FIXED: per C8 and the note; cervical myelopathy very_low (spine MRI normal) |
| C | minor | `ground_truth.key_clinical_evidence` | "July 2026 review" engineering pearl; generic "2-5x ULN" CK pearl although CK is 5.1x ULN (C9); El Escorial-style EMG pearl | FIXED: rebuilt per C14 (K-GC, K-EMG, K-NCS normal, K-CK above 5x, K-RESP, lead pearl); no K-SPINE (no spondylosis on imaging), no K-BULBAR (limb onset, no dysphagia) |
| E | minor | `metadata.difficulty_rationale` | "with literature support" no longer true | FIXED: "4 required tools" |
| C | minor | `ground_truth.diagnosis.accepted[0]` | "probable progressing to definite": the case shows UMN signs in two regions (cervical, lumbosacral), so Awaji "probable"; nothing documents progression to definite. Label not ruled on by a reviewer | FLAGGED (Open questions); not changed per ruling 3 |

## Changes, in one paragraph a physician can read before re-reviewing
The work-up now reads as a diagnostic pathway: EMG/NCS, brain MRI, spine MRI and blood tests are required actions 1-4, followed by baseline respiratory function (recommended staging), an optional ALS gene panel and the riluzole check (recommended, last); the literature step is gone. The brain MRI report describes only the brain (subtle corticospinal T2 signal, no structural lesion); the spine MRI covers the cervical and thoracic cord and the old L5-S1 surgery. The labs are reorganised into standard panels with a repeat blood lead of 24 mcg/dL (prior 28) and CK 892 U/L stated as 5.1x ULN. The EMG report keeps its findings and no longer recommends pulmonary tests. The genetic report is consistently negative across C9orf72, SOD1, TARDBP, FUS and TBK1. The riluzole check no longer offers AMX0035 or a false CYP1A2 alcohol mechanism. Lead toxicity is now low in the differential and in the red herring because lead does not produce UMN signs or this EMG pattern; a must refers him to occupational health and a prohibition rules out chelation or attributing the syndrome to lead. Musts and prohibitions follow the condition plan (disclosure, 3-monthly respiratory monitoring with a note on his CPAP-treated sleep apnoea, speech and swallowing assessment for tongue atrophy, riluzole with LFT schedule, MDT, genetic counselling).

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys used and not yet in criteria pack section 8: `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]` (plan section 5 item 2).
- UI: show `initial_tool_outputs` in criterion order (plan section 5 item 1).

## Open questions for Andrea (judgment calls you could not settle)
- Label `accepted[0]` "Amyotrophic lateral sclerosis (ALS), limb-onset, probable progressing to definite": the data meet Gold Coast and Awaji "clinically probable" (UMN plus LMN in cervical and lumbosacral regions; LMN only in thoracic and bulbar), and no repeat study documents progression to "definite". Suggest "Amyotrophic lateral sclerosis (ALS), limb-onset" if you agree; not changed because no reviewer ruled on the label. Scoring is unaffected (synonyms match).
- The blood lead is reported inside the lab block for any `interpret_labs` call, but it is not required by the lab criterion (plan: the prior level is known). Agree?

## Verification
Adversarial verifier, 23 October 2026. Checked: all 8 note ids present; each FIXED claim against the file (criteria order and tiers per plan 3.1, literature and initial DI blocks null, follow-ups respiratory, genetics, riluzole; genetic impression canonical negative with five genes; riluzole output without AMX0035 or the CYP1A2 alcohol claim; blood lead 24 mcg/dL in its own panel, in the summary and interpretation; lead red herring, differential (low) and pearl carry the note's reasoning); patient block (prior lead 28 mcg/dL kept as pre-encounter history, synthesis sentence gone, no result of a scored study); EMG findings vs impression (thoracic fibrillations only, bulbar fasciculations only, no block); MUST-DX regions (bulbar LMN stated as clinical, EMG regions cervical, thoracic, lumbosacral) and UMN signs vs exam; CK 892/174 = 5.1x ULN; spine region matches the L5-S1 finding; musts vs prohibitions (no contradiction; chelation prohibition consistent with the lead must); forbidden strings (AMX0035, grapefruit, July 2026, El Escorial, 2-5x, em dashes in new text): none. The label question (Awaji probable, not "progressing to definite") is correctly left to Andrea under ruling 3. Perfect-agent and case_io check clean. Found nothing that needed a change.

## Condition audit (ALS lead, 23 Oct 2026)
- `followup_outputs[0].output.findings[*].is_abnormal` added (rows carried no abnormality marker), set from each row's reference range as plan C4 prescribes, so all 30 respiratory reports mark abnormal values the same way (values and impression unchanged).

## Condition audit, second pass (ALS auditor, 23 Oct 2026)
- C, minor, `ground_truth.assessment.required_recommendations[0]` (MUST-DX) and `ground_truth.key_clinical_evidence[0]` (K-GC): both claimed lower motor neuron involvement in the thoracic region (and in some cases other regions) "on examination and EMG", but thoracic paraspinals (T7-T9) show fibrillations only, while MUST-DX and K-GC counted the thoracic region on EMG. Regions now: bulbar (clinical tongue atrophy and fasciculations), cervical and lumbosacral, with active denervation also in thoracic paraspinal muscles. Gold Coast 2020 counts lower motor neuron dysfunction in a region only with clinical weakness and wasting, or with EMG chronic neurogenic change plus active denervation in that region. The S-series and RS11 verifiers applied this to MUST-DX and K-GC; this case still claimed regions that rest on active denervation alone, so the same wording is now used across all 30 ALS cases. No stored result changed; Gold Coast stays met (upper and lower motor neuron dysfunction in the cervical region, or lower motor neuron dysfunction in two regions). FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 ALS cases after the change: clean.

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- accepted[0]: 'probable progressing to definite' -> 'probable ALS by Awaji criteria' (no study documents progression; UMN+LMN in cervical and lumbosacral, LMN only in bulbar).
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, ALS case guards pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
