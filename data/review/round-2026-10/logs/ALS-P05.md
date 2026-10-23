# ALS-P05
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| a22b4336-665b-4e6e-b946-e29d0a559e9b | FIXED | Action criteria reordered (EMG, brain MRI, spine MRI, labs first, then optional CSF); follow-ups now respiratory, genetics, riluzole; literature removed; sequence constraints EMG before genetics and riluzole. CSF (HIV-1 RNA) and the HIV labs kept as targeted mimic exclusion, as the note allows (`ground_truth.action_criteria`, `followup_outputs`, `ground_truth.sequence_constraints`). |
| 783c430e-8ad7-42fa-bb4a-99e0ae4b999d | FIXED | Riluzole/Biktarvy check is now the last follow-up and the last criterion (`action-2-check-drug-interactions`, recommended), with a soft constraint EMG before it. |
| dfaf2518-daab-4389-83d7-217ce7b41a31 | FIXED | `ground_truth.red_herrings[0]` rewritten: HIV is a confounder; suppressed plasma HIV-1 RNA with CD4 520, CSF HIV-1 RNA not detected, no cord/white matter/enhancing lesion, normal sensory studies and multi-region anterior horn cell denervation argue against HIV neuropathy, vacuolar myelopathy or opportunistic CNS disease. |
| 7e2fad0b-5b8d-4135-b383-ed05af0041f4 | FIXED | `ground_truth.differential`: HIV-associated motor neuronopathy moderate -> low with supports/against from the case data; vacuolar myelopathy, PML, CNS lymphoma, CMV polyradiculomyelopathy and ART toxic neuropathy very_low. |
| 0ca4443e-beb3-4120-a560-8a04cd9e40e4 | FIXED | Literature follow-up `search_als_hiv_comorbidity` deleted; `initial_tool_outputs.labs.panels.HIV` now reports plasma HIV-1 RNA (<20 copies/mL, not detected) and CD4 count 520 cells/uL; lab criterion adds `HIV`. |
| 1b1dcc51-9d21-4a84-a669-ceb71d93c945 | FIXED | Respiratory criterion recommended, staging text (not diagnostic), placed after the diagnostic core; follow-up first in the post-diagnostic list; impression "FVC 82% predicted and SNIP 71 cmH2O are within normal limits; baseline for serial monitoring." |
| cc45e126-5d7e-4289-a71a-e9dffe3445f5 | FIXED | AMX0035 removed from the interaction output (`followup_outputs[2].output.alternatives` = []); output rewritten to the case's real content (ART and amlodipine: no clinically significant interaction; ART unchanged). |
| a2fa5560-e498-400a-bce2-2ebd8dbf08a6 | FIXED | Same pathway fix as a22b4336 (core EMG/NCS, brain and spine MRI, targeted labs, optional CSF for the HIV mimic first). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | initial_tool_outputs.mri.impression | Brain MRI impression was the spine impression ("No cord signal change. No cord compression..."); brain report carried no brain impression | FIXED: brain-only report, post-gadolinium technique stated, numbered impression |
| B | major | initial_tool_outputs.body_imaging | Non-contrast spine study reported "No leptomeningeal enhancement"; finding description was a JSON dump; "No HIV vacuolar myelopathy pattern" named a diagnosis | FIXED: `contrast` true, technique stated, plain-sentence findings, normal 1-line impression |
| B | minor | initial_tool_outputs.specialized_test.impression | Impression cited positive sharp waves and bulbar chronic reinnervation that the findings did not contain; "Pulmonary function testing recommended." cross-step hint | FIXED: impression restated from the findings; motor NCS localised (left median and ulnar CMAPs reduced); sensory nerves named; recommended_actions emptied |
| D | major | patient.history_present_illness | Spine MRI result and reasoning sentences ("not typical of HIV myelopathy", "CD4 520 argues against") leaked scored results and the conclusion | FIXED: results and reasoning deleted; neutral referral kept; HIV clinic history (undetectable VL, CD4 >500) kept as background |
| D | minor | patient.neurological_exam.additional | Diagnostic synthesis ("combined upper and lower motor neuron signs") | FIXED: findings only |
| B/C | major | initial_tool_outputs.labs | "Exclusion studies" and "Mimic exclusion" panels with TSH and free T4 as strings; no CBC or metabolic panel; interpretation named ALS; no CD4 | FIXED: canonical panels, numeric values, core analytes added (normal, plausible for a 46-year-old woman on TAF), CD4 added; serum glucose 94 mg/dL agrees with the CSF/serum ratio 0.66 |
| A | minor | initial_tool_outputs.csf.interpretation | Python dict dumps and "CSF does not confirm ALS" | FIXED: factual pattern statement; protein 48 mg/dL described as mildly raised |
| B | minor | followup_outputs (genetics) | Panel reported C9orf72 and SOD1 only; impression "All values within normal limits" | FIXED: five genes, canonical negative impression |
| B | minor | followup_outputs (respiratory) | SNIP reference ">70 cmH2O women" | FIXED: >=60 cmH2O (women), is_abnormal per row |
| C | major | ground_truth.assessment | Musts were diagnostic actions plus a generic lab list (androgen receptor CAG repeat in a woman); prohibitions on cervical surgery (no spondylosis on imaging) and functional dismissal (no psychiatric history) irrelevant | FIXED: rebuilt per plan C10 (MUST-DX, MUST-RESP normal, MUST-RILUZOLE, ART must, MUST-MDT, MUST-GEN; PROHIB-IMM, PROHIB-RESP normal) |
| E | minor | ground_truth.key_clinical_evidence | "July 2026 review applied end to end" engineering pearl, generic 2-5x CK pearl, El Escorial EMG pearl | FIXED: rebuilt per C14 plus one HIV pearl |
| C | minor | ground_truth.differential | Mimics raised in the HPI (CMV radiculopathy, lymphoma) were not in the differential; MMN absent for asymmetric hand wasting | FIXED: added, with likelihoods reflecting the completed work-up |
| A | minor | ground_truth.action_criteria | Brain MRI criterion required `contrast: true, protocol: standard` (a correct non-contrast order failed it); spine required `contrast: false`; free-text citations; label = rationale | FIXED: per plan C16 |
| E | minor | metadata.difficulty_rationale, metadata.notes | Claimed the case requires literature support; "confirms ALS" | FIXED: reworded to what the case contains |
| E | minor | patient.neurological_exam.gait | Existing em dash in "Mildly spastic — note: ..." | FLAGGED: correct prose, left unchanged to avoid churn |

## Changes, in one paragraph a physician can read before re-reviewing
The work-up now reads EMG/NCS, brain MRI, spine MRI and blood tests first (all required), then optional CSF for the HIV question, then the post-diagnostic steps: respiratory function (recommended), genetic panel (optional, after counselling) and the riluzole interaction check (recommended), with soft constraints putting EMG before genetics and riluzole. The literature search is gone. The HPI no longer reports the spine MRI result or reasons about it. Brain and spine MRI are now separate, region-pure, post-gadolinium reports (brain: subtle corticospinal tract signal only; spine: normal). Labs are complete (blood count, metabolic panel, CK 624 U/L = 3.7x ULN, thyroid, B12, folate, ESR, CRP) and show plasma HIV-1 RNA undetectable with CD4 520 cells/uL; CSF HIV-1 RNA is not detected. The EMG impression now matches its findings (bulbar, cervical, thoracic and lumbosacral denervation, no conduction block, normal sensory studies). The interaction check states that Biktarvy and amlodipine do not interact with riluzole and gives the SmPC monitoring schedule; AMX0035 is gone. Musts: disclose the Gold Coast diagnosis, 3-monthly FVC/SNIP, riluzole with LFT monitoring, continue ART and inform the HIV team, MDT, genetic counselling. HIV-related diagnoses are low or very low, each with the data that exclude it.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- New citation keys used: `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]` (plan section 5.2).
- `interpret_labs` vocabulary: add `HIV_viral_load` and `CD4_count` (plan section 5.4); until then the lab criterion asks `HIV` and the panel named "HIV" reports both.
- Review UI: show the initial work-up and the follow-ups together in criterion order (plan section 5.1).

## Open questions for Andrea (judgment calls you could not settle)
- The HPI keeps the HIV clinic background ("undetectable viral load and CD4 counts above 500 cells/uL at her HIV clinic reviews") while the lab criterion asks for current HIV values. I kept both: the background is routine HIV care, and the reviewer (0ca4443e) asked for current viral load and CD4 in the work-up. Confirm that this is not a timeline leak.
- CSF protein 48 mg/dL is kept as stored and described as mildly raised; it fits ALS and does not change the case.

## Verification
Adversarial re-read of the whole final case against `git show HEAD`, the plan (C1-C17, section 4 P05) and the eight R1 notes (all eight ids are in the table).
- Notes: pathway (a22b4336, 783c430e, a2fa5560): criteria are EMG, brain MRI, spine MRI, labs (required), CSF (optional), respiratory (recommended), genetics (optional), riluzole (recommended); follow-ups respiratory, genetics, riluzole; no literature; two soft constraints. dfaf2518 and 7e2fad0b: red herring and HIV entries say what the data exclude (plasma and CSF HIV-1 RNA, CD4 520, MRI, sensory studies). 0ca4443e: "HIV" panel reports plasma HIV-1 RNA and CD4; `HIV` is a costs.yaml term. 1b1dcc51: respiratory normal (FVC 82, SNIP 71, women limit 60). cc45e126: AMX0035 gone. All confirmed.
- Cross-field: left-sided onset, left Babinski and left tongue fasciculations agree across exam, EMG, MUST-DX and key evidence; CK 624/170 = 3.7x; CSF glucose 62 with serum 94 gives the stored ratio 0.66; post-gadolinium technique is stated in both brain and spine reports and `body_imaging.contrast` is true; the interaction output covers both medicines (Biktarvy, amlodipine); musts and prohibitions do not conflict; no allergen is mandated. The HPI keeps the HIV-clinic background (undetectable, CD4 above 500): routine HIV care, not a scored-result leak (worker's open question; I agree).
- Clinical facts checked: HIV-associated ALS-like syndrome mainly with uncontrolled viraemia; toxic neuropathy belongs to the older d-drug nucleosides, not TAF regimens; CMV polyradiculomyelopathy needs profound immunosuppression. Correct.
- Found: nothing to change.
- Checks run after verification: `perfect_agent.py -v` ok (every required and recommended criterion answered by the case's own data; the "<- ?" source marker for brain MRI, spine MRI and labs is the same in every ALS case and is not a fallback), `case_io.py check` schema OK, synonym guard OK, no test failure names the case. Grep for AMX0035, Relyvrio, edaravone, grapefruit, serotonergic, "July 2026", El Escorial, "Exclusion studies", "Reviewer baseline" and JSON dumps: none in the case (QTc appears only in the fallback ECG). No new em or en dash in the diff. Citations are bracketed allow-list keys only. Lab `is_abnormal` flags agree with every numeric reference range; ESR 8, CRP 2, B12 420 and folate 10 were already identical at HEAD in P05-P09 and RM11 (kept per plan C13, flagged by the worker).

## Condition audit (ALS lead, 23 Oct 2026)
- `ground_truth.key_clinical_evidence[2]` (K-NCS): "or SBMA" removed. SBMA is X-linked and affects men; the plan's C8 already drops the Kennedy entry in women, so the pearl named a mimic that cannot apply (flagged by the S02, S04, S07 and S09 verifiers as a class).

## Condition audit, second pass (ALS auditor, 23 Oct 2026)
- C, minor, `ground_truth.assessment.required_recommendations[0]` (MUST-DX) and `ground_truth.key_clinical_evidence[0]` (K-GC): both claimed lower motor neuron involvement in the thoracic region (and in some cases other regions) "on examination and EMG", but the tongue shows fibrillations and fasciculations without chronic change or wasting, and the T7 paraspinals show fibrillations only. Regions now: cervical and lumbosacral (tibialis anterior: mildly enlarged MUPs with sparse fibrillations), with active denervation also in bulbar (tongue) and thoracic paraspinal muscles. Gold Coast 2020 counts lower motor neuron dysfunction in a region only with clinical weakness and wasting, or with EMG chronic neurogenic change plus active denervation in that region. The S-series and RS11 verifiers applied this to MUST-DX and K-GC; this case still claimed regions that rest on active denervation alone, so the same wording is now used across all 30 ALS cases. No stored result changed; Gold Coast stays met (upper and lower motor neuron dysfunction in the cervical region, or lower motor neuron dysfunction in two regions). FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 ALS cases after the change: clean.

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- HPI: prior viral load and CD4 values removed (current values are scored through the labs criterion).
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, ALS case guards pass.
