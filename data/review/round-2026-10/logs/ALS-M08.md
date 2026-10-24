# ALS-M08
Reviewer status: R1 needs_changes, R2 pending | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 52d9a7bf-e7aa-4e20-a4fd-7b254bd71c3e | FIXED | Plan C1: `ground_truth.action_criteria` reordered (EMG, brain MRI, spine MRI, labs, optional CSF first); `followup_outputs` now respiratory, genetics, riluzole; literature removed; soft sequence constraints EMG before genetics and before riluzole |
| 25746607-f788-44a3-9a59-95c6588f18e2 | FIXED | Riluzole-natalizumab check moved to the last criterion and last follow-up, after the diagnostic core and labs (C3); constraint `action-6` before `action-2` |
| ebf2dc98-1e0a-43e2-9380-23de02e2f9bf | FIXED | Follow-up `search_als_ms_concurrent` and criterion `action-1-search-medical-literature` deleted (C2); the core actions it displaced are criteria 1-4 |
| 62cb7f37-9f98-447d-bfa2-289347b89291 | FIXED | `red_herrings[0].correct_interpretation` rewritten with the note's wording (stable lesions explain baseline spasticity and sensory symptoms, not tongue atrophy/fasciculations, new wasting, widespread fasciculations or multi-region denervation); `differential[0]` MS relapse moderate -> low; new prohibition against treating the new syndrome as an MS relapse with corticosteroids; MS pearl in `key_clinical_evidence` |
| eb63c44b-a324-4e0a-b71e-07ae0a81f62f | FIXED | Respiratory follow-up placed after the diagnostic core; criterion relabelled as staging (`recommended`); output reference ranges corrected (women's SNIP limit 60, was ">70") and impression rewritten (FVC reduced, SNIP at the lower limit); MUST-RESP referral and PROHIB-RESP added (C4, C10) |
| 53da6db5-a4bb-4da1-8f0e-0c89f5b24c81 | FIXED | "AMX0035 reasonable alternative given polypharmacy" removed (`alternatives` = []); wrong "natalizumab lymphopenia" corrected to lymphocytosis; canonical summary with LFT schedule; escitalopram, lisinopril, vitamin D listed as no interaction |
| 123f27f8-88f9-4791-a3f2-f58649d6b7c0 | FIXED | Genetics criterion stays `optional`, placed after the core, with constraint EMG before genetics; output now reports all five genes and the canonical negative impression (C5) |
| 7d69e683-31be-48d9-b6aa-98002e294a7b | FIXED | Same as 52d9a7bf: core block (EMG/NCS, brain and spine MRI, targeted labs) leads the pathway |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | Timeline leak: "brain MRI shows no PML lesions" (brain MRI is scored) and "New MRI brain and cervical spine was ordered"; "JCV index elevated, consistent with natalizumab treatment" is wrong (seropositivity reflects prior JC virus infection) | FIXED: replaced by "Her JC virus antibody index is elevated and is monitored because of the PML risk on natalizumab." (prior MRI 14 months ago kept as history) |
| B | major | `initial_tool_outputs.mri` | Impression and findings disagreed (new low T2 motor-cortex rim vs "new hyperintensity" in "anterior corticospinal tracts"); interpretive "iron deposition pattern in UMN degeneration"; caps; gadolinium not stated outside a field note | FIXED: three findings (stable MS lesions with no enhancement; precentral low T2; corticospinal tract hyperintensity), post-gadolinium statement, numbered impression with an imaging differential only |
| B | minor | `initial_tool_outputs.body_imaging` | Empty findings; generic impression | FIXED: cervical and thoracic cord findings (no demyelinating cord lesion, no compression), numbered impression |
| B | major | `initial_tool_outputs.specialized_test` | Impression claimed positive sharp waves and chronic reinnervation in all four regions (findings show chronic change only in cervical and lumbosacral muscles); sensory finding referred to an undocumented "prior study"; PFT hint | FIXED: impression matches findings; sensory finding states normal median, ulnar, left sural and mildly reduced right sural; motor NCS adds normal distal latencies and no temporal dispersion; recommended_actions emptied (C6) |
| A | major | `initial_tool_outputs.csf.interpretation` | Python dict dumps and "CSF does not confirm ALS" | FIXED: plain interpretation; IgG index numeric 0.64 (reference <0.70); special tests kept (C13) |
| A/B | major | `initial_tool_outputs.labs` | "Exclusion studies" (Free T4 as a string, case-level significance), "Reviewer baseline rule-out additions", interpretation names ALS; no WBC, platelets, renal or liver values | FIXED: panels rebuilt per C13 (stored values kept; normal WBC, platelets, CMP, free T4 1.1 ng/dL added); CK 498 U/L stated as 2.9x ULN |
| C | major | `ground_truth.action_criteria` | Brain MRI `contrast/protocol` arguments, spine `contrast: false`, nine exact lab panels; label = rationale; mixed citations | FIXED: C16 arguments and canonical texts; CSF criterion kept optional with its special tests and a case rationale (PML question) |
| C | major | `ground_truth.assessment` | Generic musts (diagnostic actions, "androgen receptor CAG repeat in males" in a woman); cervical-surgery prohibition with no spondylosis | FIXED: rebuilt per C10 plus the plan's MS-team must and MS-relapse prohibition; PROHIB-FUNC (depression) kept per plan |
| C | major | `ground_truth.differential` | MS relapse left moderate after the work-up; PML low despite negative MRI and JCV PCR; MMN absent | FIXED: MS relapse low, PML very_low, MMN low (C8 wording), cervical demyelinating myelopathy and combined demyelination very_low, functional very_low |
| C | minor | `ground_truth.key_clinical_evidence` | Engineering "July 2026 review" pearl; El Escorial-style EMG pearl; "normal sensory NCS ... pivotal" although the right sural is reduced; spondylosis pearl without spondylosis | FIXED: K-GC, K-EMG, adapted sural pearl, K-CK (2.9x), K-RESP, MS pearl |
| C | minor | `key_clinical_evidence[2]` | Plan's canonical reduced-sural pearl says "fit a coexisting length-dependent neuropathy"; here only the right sural is reduced, which is not a length-dependent pattern | FIXED with adapted wording ("minor, non-specific sensory finding"); see Open questions |
| E | minor | `metadata.difficulty_rationale` | "literature search essential" no longer true | FIXED |
| B | minor | `initial_tool_outputs.labs` | B12 420, folate 10, ESR 8, CRP 2 are identical to ALS-M07 (template carry-over) | FLAGGED, not changed (plan: keep stored values) |

## Changes, in one paragraph a physician can read before re-reviewing
The pathway now starts with EMG/NCS, brain MRI (with gadolinium), spine MRI and blood tests, then optional CSF (for the PML and MS-activity questions), baseline respiratory function, an optional gene panel and the riluzole check last; the ALS-MS literature step is gone. The HPI no longer reports the result of the brain MRI the agent must order. The brain MRI report is internally consistent: stable MS lesions without enhancement, no PML lesion, new symmetric precentral low T2 signal and corticospinal tract change separate from the known lesion. The spine MRI shows no cord lesion. The EMG impression matches its findings (active denervation in four regions, chronic change in cervical and lumbosacral muscles, no conduction block, mildly reduced right sural only). The CSF and lab reports are rewritten in plain form with the same values. The riluzole check removes AMX0035 and corrects natalizumab "lymphopenia" to lymphocytosis. MS relapse is now low and PML very low; the red herring explains what MS can and cannot account for. Musts: diagnosis and disclosure, respiratory referral because FVC is already reduced (SNIP at the lower limit), speech and swallowing assessment for dysarthria and tongue atrophy, riluzole with LFT schedule, MDT, genetic counselling, and informing the MS team about natalizumab; prohibitions include treating the new syndrome as an MS relapse with steroids.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]` (plan section 5 item 2).
- UI: show `initial_tool_outputs` in criterion order (plan section 5 item 1).

## Open questions for Andrea (judgment calls you could not settle)
- Respiratory category: the plan classes M08 as "reduced" (FVC 78%), but SNIP 60 cmH2O equals the women's lower limit. I kept the "reduced" must (refer to the respiratory/NIV service now) but worded it as "FVC already reduced, SNIP at the lower limit" rather than the canonical "FVC and SNIP are already reduced". Confirm the referral threshold for an FVC just below 80% with bulbar signs.
- The plan's reduced-sural pearl (K-NCS sural) was adapted because only the right sural is reduced; the lead may want one wording for all four reduced-sural cases (M02, M05, M08, S06).

## Verification
Adversarial verifier, 23 October 2026. Checked: all 8 note ids present; each FIXED claim against the file (criteria order and tiers, CSF optional with oligoclonal bands, IgG index and JCV PCR all reported in the CSF output; riluzole output with natalizumab lymphocytosis and no AMX0035; women's SNIP limit 60; genetic panel five genes; MS red herring and MS relapse low); HPI no longer reports the scored brain MRI; EMG impression vs findings; CK 498/170 = 2.9x ULN; musts vs prohibitions; forbidden strings: none.
Found and fixed:
- B, major, laterality (pre-existing, not caught by the worker): the known MS plaque was a "right corticospinal tract" lesion in the brain, said to explain her right leg spasticity, right extensor plantar and right hemibody numbness. A supratentorial corticospinal lesion causes contralateral signs, so the lesion must be left-sided. Changed "right" to "left" for the brain lesion in `patient.history_present_illness`, `initial_tool_outputs.mri.findings[0].location`, `findings[2].signal_characteristics.T2` and both mentions in `mri.impression`. The clinical findings (right leg, right hemibody) are unchanged.
- C, minor, `ground_truth.key_clinical_evidence[5]`: "Multiple sclerosis does not produce lower motor neuron signs" is an overstatement (root exit zone plaques can rarely cause segmental amyotrophy); reworded to "does not explain lower motor neuron signs in several regions".
Perfect-agent and case_io check re-run: clean.

## Condition audit (ALS lead, 23 Oct 2026)
- `followup_outputs[0].output.findings[*].is_abnormal` added (rows carried no abnormality marker), set from each row's reference range as plan C4 prescribes, so all 30 respiratory reports mark abnormal values the same way (values and impression unchanged).

## Condition audit, second pass (ALS auditor, 23 Oct 2026)
- C, minor, `ground_truth.assessment.required_recommendations[0]` (MUST-DX) and `ground_truth.key_clinical_evidence[0]` (K-GC): both claimed lower motor neuron involvement in the thoracic region (and in some cases other regions) "on examination and EMG", but thoracic paraspinals (T6-T8) show fibrillations only. Regions now: bulbar (tongue atrophy and dysarthria, EMG fibrillations), cervical and lumbosacral, with active denervation also in thoracic paraspinal muscles. Gold Coast 2020 counts lower motor neuron dysfunction in a region only with clinical weakness and wasting, or with EMG chronic neurogenic change plus active denervation in that region. The S-series and RS11 verifiers applied this to MUST-DX and K-GC; this case still claimed regions that rest on active denervation alone, so the same wording is now used across all 30 ALS cases. No stored result changed; Gold Coast stays met (upper and lower motor neuron dysfunction in the cervical region, or lower motor neuron dysfunction in two regions). FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 ALS cases after the change: clean.

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, ALS case guards pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
