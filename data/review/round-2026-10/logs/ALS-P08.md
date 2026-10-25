# ALS-P08
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

Note: this case was started in an earlier run that was interrupted before its log was written. I re-read the whole current file against the original (`git show HEAD`), kept the earlier edits that are correct, completed the remaining fixes and wrote this log for the case as a whole.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| c15f3a46-9f5f-4bd2-a4ac-31457c8f77f1 | FIXED | `ground_truth.diagnosis.accepted[0]` "Familial ALS, SOD1 A4V pathogenic variant, early symptomatic stage" -> "Suspected early ALS in a SOD1 A4V pathogenic-variant carrier, Gold Coast criteria not yet met"; `icd_codes[0]` G12.21 kept (plan Q2); appended synonyms not hand-edited. Key evidence, differential, red herrings and `metadata.notes` now say that carrier status and the current EMG do not establish ALS. |
| 38d2fb67-30c3-4d31-af3d-e4080a890549 | FIXED | Action criteria reordered (EMG, brain MRI, spine MRI, labs first); follow-ups now respiratory, genetics; literature removed (`search_sod1_a4v_prognosis`, `genetic_counseling_sod1` and criterion `action-1-search-medical-literature` deleted); sequence constraint EMG before genetics. Repeat EMG and close follow-up are musts 3 and 5 (a repeat study in 6-8 weeks cannot be a tool call in this encounter). |
| 5db6492b-4d77-49d0-84ab-6ca97ebcc23c | FIXED | Follow-up `check_tofersen_riluzole_interaction` and criterion `action-2-check-drug-interactions` deleted. Replaced by musts 1-2 (post-test and cascade counselling), 5 (repeat EMG/NCS in 6-8 weeks with clinical review) and 6 (specialist centre referral so tofersen is discussed once ALS is established); prohibition 1 "Do not start riluzole or tofersen before ALS is established clinically and electrodiagnostically." |
| 2e11ab82-94e5-47df-9209-63b79c592f5c | FIXED | `required_recommendations[4]` "Repeat EMG/NCS in 6 to 8 weeks with clinical review, looking for active denervation, spread and definite upper motor neuron signs."; EMG report keeps "Repeat study in 6-8 weeks recommended." (the report itself is uncertain); key evidence pearl 5 on serial EMG. |
| 41f0232d-0688-4547-8da3-1dbda7fecc74 | FIXED | Key evidence pearl 3 "Upper motor neuron evidence is currently equivocal: reflexes have risen from 2+ to 3+, but there are no Hoffman or Babinski signs and no spasticity."; red herring 2 on the relative hyperreflexia; HSP differential entry states "against: no spasticity, flexor plantar responses". The exam text itself is unchanged (it records findings, not a conclusion). |
| 73e83884-ca8b-4a40-82b8-9c3c0d0b7e47 | FIXED | `required_recommendations[1]` "Offer counselling to his first-degree relatives, each of whom has a 50% chance of carrying the variant, with predictive testing only after counselling."; family history entry left as written (the uncle is correctly a second-degree relative). |
| d469d924-1774-4629-8a0e-d0814638440c | FIXED | `required_recommendations` replaced by the six musts of the plan: post-test counselling with "suspected, not established"; cascade counselling; objective neurological baseline (MRC, reflexes, ALSFRS-R) against his athletic baseline; MRI and blood tests for mimic exclusion before any treatment decision; repeat EMG/NCS in 6-8 weeks; specialist centre referral. The old EMG must ("bulbar plus at least 2 spinal regions") and all other diagnostic musts are gone. |
| abedfbbf-c714-40fd-9796-c251721aedb3 | FIXED | Respiratory criterion `optional`, after the diagnostic core, label "Baseline respiratory function (FVC and SNIP) as an objective baseline while ALS is not established", rationale says it neither supports nor excludes ALS; output impression "FVC 92% predicted and SNIP 88 cmH2O are within normal limits; baseline for serial monitoring." |
| af695bda-96d6-42e7-8257-cf5b24d9b34f | FIXED | AMX0035 removed with the whole tofersen interaction output (see 5db6492b). |
| 3fcc8e64-533c-4ea1-9d8b-b287dfd01ea9 | FIXED | Same as c15f3a46 and 5db6492b: relabelled as SOD1 carrier with suspected early ALS; no riluzole or tofersen proposed now (prohibition 1). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `patient.history_present_illness` | "6-month history" but "fasciculations first in his calves 8 months ago" | FIXED: "6 months ago" |
| D | major | `patient.history_present_illness` | Reasoning paragraph interpreting the athletic baseline, detraining versus denervation, and the exam ("an interval increase, with no clear upper motor neuron signs yet") | FIXED: replaced by facts only (retired 2 years ago and trains much less; PCP recorded reflexes of 2+ before the symptoms) |
| D | minor | `patient.neurological_exam.additional` | Synthesis ("Calf atrophy may represent detraining vs true denervation") | FIXED: "Athletic build (former elite swimmer)." |
| B | major | `initial_tool_outputs.specialized_test.impression` | Impression claimed "chronic reinnervation changes" in the cervical region while the findings put the motor units at the upper limit of normal; with Awaji this would have counted the fasciculations as active denervation and met LMN criteria in that muscle | FIXED: impression restated from the findings, numbered, "no definite chronic neurogenic change"; within-modality "uncertain significance" and repeat study kept |
| B | minor | `initial_tool_outputs.specialized_test.findings[0]` | MUP amplitude "6-7 mV" in the first dorsal interosseous called upper limit of normal; most laboratories would call 6-7 mV enlarged, which contradicts the equivocal reading the case is built on | FIXED (this run): number removed, "Motor unit potentials at the upper limit of normal for amplitude and duration, stable, with full recruitment." |
| A/D | minor | `initial_tool_outputs.specialized_test` | `quantitative_data.diagnostic_uncertainty` "HIGH ... athlete baseline confounds interpretation"; motor NCS lacked distal latency and conduction block statement; bulbar and thoracic findings terse | FIXED: quantitative_data factual; motor NCS row per C6 with no conduction block; tongue/masseter and thoracic paraspinal findings stated |
| D | minor | `initial_tool_outputs.mri` | "a normal study does not exclude an early neurodegenerative or motor neuron process" (style guide strips this); JSON-like finding object | FIXED: plain pertinent negatives, impression "Normal brain MRI." |
| D | minor | `initial_tool_outputs.body_imaging.impression` | "no cord signal change to explain the deficit" (interpretive); no findings | FIXED: cord and canal findings, impression "Normal MRI of the cervical and thoracic spine: no cord compression or cord signal change." |
| A/B | major | `initial_tool_outputs.labs` | "Exclusion studies" with free T4 as a string and engineering text; "Reviewer baseline rule-out additions"; no blood count, renal or liver values although the criterion required CBC and CMP; interpretation names ALS | FIXED: canonical panels (CBC, CMP, CK, thyroid, vitamins, inflammatory markers), stored values kept, normal CBC/CMP and free T4 1.2 ng/dL added; interpretation "Abnormal: CK 420 U/L (2.4x ULN)." |
| B | minor | `followup_outputs` (genetics) | Only C9orf72 and SOD1; "p.A4V (most common SOD1 ALS mutation)"; impression "Pathogenic ALS-associated variant identified" | FIXED: five genes, SOD1 as c.14C>T, p.(Ala5Val) (legacy A4V), impression names only the finding and post-test counselling |
| A | minor | `ground_truth.action_criteria` | Brain MRI required `contrast: true`; spine `contrast: false`; labs list; free-text citations; label = rationale | FIXED per C16 and C13 |
| C | minor | `ground_truth.action_criteria` (respiratory, genetics) | Canonical rationales presuppose established ALS ("Once ALS is supported", "offered ... to people with ALS") | FIXED (this run): case-specific rationales, as in ALS-P02 |
| C | major | `ground_truth.differential` | "Familial ALS, non-SOD1" high and "Sporadic ALS with coincidental family history" moderate after a pathogenic SOD1 result; Kennedy entry cited an untested CAG repeat; distal HMN entry cited UMN signs he does not have | FIXED per plan: deleted the two genotype entries; added "Benign fasciculations with detraining atrophy in a former athlete" moderate; HSP low; Kennedy very_low (C8 wording plus X-linked inheritance cannot pass from a paternal uncle through the father; CAG repeat not tested); distal HMN very_low |
| C/E | major | `ground_truth.key_clinical_evidence` | Template pearls (Gold Coast met, EMG bulbar plus 2 regions, CK 2-5x, spondylosis that is not on his imaging, NIV thresholds, "July 2026 review" engineering text) | FIXED: seven pearls (A4V aggressiveness, carrier is not diagnosis, equivocal UMN evidence, EMG criteria and this study, serial EMG decides, tofersen only once ALS established, CK 2.4x non-specific) |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Cervical surgery (no spondylosis), respiratory deferral, functional dismissal of "bulbar" symptoms he does not have | FIXED: replaced by the plan's two prohibitions |
| C | minor | `ground_truth.red_herrings` | Empty although the case is built on two confounders | FIXED: athlete/detraining red herring and relative hyperreflexia red herring |
| E | minor | `metadata.notes`, `metadata.difficulty_rationale` | "Tofersen must be initiated urgently", "normal initial EMG", "5+ required tools" | FIXED: reworded to the new ground truth |
| B | minor | `fallback_tool_outputs.ecg.rate` | 82/min while the vitals record 58/min at rest in a former elite athlete | FIXED (this run): 60/min (sinus rhythm retained) |
| B | minor | `initial_tool_outputs.labs` | ESR 8, CRP 2, B12 420, folate 10 identical to many ALS cases | FLAGGED: stored values kept per plan |

## Changes, in one paragraph a physician can read before re-reviewing
This case is no longer labelled established familial ALS: the ground truth is suspected early ALS in a SOD1 A4V pathogenic-variant carrier, Gold Coast criteria not yet met (G12.21 kept). The HPI no longer interprets the athletic baseline or the exam, and its timeline is consistent (6 months). The EMG reports complex fasciculations in cervical and lumbosacral muscles, no definite fibrillations (possible sparse positive sharp waves in the right tibialis anterior), motor units at the upper limit of normal without definite chronic neurogenic change, normal conduction without block and normal sensory studies, and recommends a repeat study in 6-8 weeks. Brain and spine MRI are normal; the labs show only CK 420 U/L (2.4x ULN). The work-up is EMG, brain MRI, spine MRI and labs (required), then optional respiratory baseline and a recommended gene panel after counselling, which returns the SOD1 A4V variant with the other four genes negative. The literature searches and the tofersen/riluzole check are gone. Musts: explain that the variant is pathogenic but ALS is not established and arrange post-test counselling; cascade counselling of his first-degree relatives; objective neurological baseline; complete MRI and blood tests before any treatment decision; repeat EMG/NCS in 6-8 weeks; referral to a specialist ALS centre so that tofersen can be discussed once ALS is established. Prohibitions: no riluzole or tofersen before ALS is established; no attribution to detraining or anxiety without the repeat EMG and review.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Diagnosis label changed under G12.21 (plan section 5 item 3): no synonym change needed, but the appended synonyms ("ALS", "amyotrophic lateral sclerosis", ...) mean an agent answering "ALS" is scored correct; whether that is wanted is plan Q2.
- New citation keys used: `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`.
- Review UI: show the initial work-up and follow-ups in criterion order.
- `test_guidance_claims`: genetics recommended and respiratory optional here, which the July guidance text does not reflect (handled centrally after the round).

## Open questions for Andrea (judgment calls you could not settle)
- Plan Q2: keep G12.21 with the "suspected early ALS ... not yet met" label, or code carrier status (for example Z15.89) with ALS as a differential, which would make a plain "ALS" answer wrong.
- The repeat EMG, the central diagnostic action the reviewer asked for, is a must (6-8 weeks later) rather than a criterion, because a repeat study in the same encounter cannot be scored. Confirm that this is acceptable.

## Verification
Adversarial re-read of the whole final case against `git show HEAD`, the plan (C7, section 4 P08) and the ten R1 notes (all ids present).
- Notes: c15f3a46 and 3fcc8e64: `accepted[0]` is the plan's label, `icd_codes[0]` G12.21 kept, synonyms untouched, CENTRAL and Q2 logged. 38d2fb67, 5db6492b, af695bda: literature and tofersen check deleted, no `action-2` criterion and no interaction follow-up remain, only sequence constraint 1. 2e11ab82 and d469d924: the six plan musts are present verbatim; the repeat EMG is a must (a later encounter) and the EMG report itself keeps the repeat recommendation, which the plan allows for P08. 41f0232d: key evidence and red herring 2 call the UMN evidence equivocal. 73e83884: cascade counselling must. abedfbbf: respiratory optional and called a baseline only.
- Cross-field: no Hoffman or Babinski, flexor plantars and reflexes 2+ to 3+ agree with every pearl and differential entry; the EMG no longer contradicts itself (no definite fibrillations, no definite chronic change, so Awaji cannot count the fasciculations); HPI timeline 6 months throughout; CK 420/174 = 2.4x; fallback ECG rate 60 against resting HR 58; prohibition 1 (no riluzole or tofersen now) and must 6 (tofersen discussed once ALS is established) do not conflict.
- Clinical facts checked: SOD1 A4V aggressive, LMN-predominant; tofersen FDA accelerated approval April 2023 and EU authorisation 2024 for SOD1-ALS only; presymptomatic carrier treatment only in trials (ATLAS); Kennedy disease cannot pass from a paternal uncle through the father to a son (X-linked). Correct.
- Found: nothing to change.
- Checks run after verification: `perfect_agent.py -v` ok (every required and recommended criterion answered by the case's own data; the "<- ?" source marker for brain MRI, spine MRI and labs is the same in every ALS case and is not a fallback), `case_io.py check` schema OK, synonym guard OK, no test failure names the case. Grep for AMX0035, Relyvrio, edaravone, grapefruit, serotonergic, "July 2026", El Escorial, "Exclusion studies", "Reviewer baseline" and JSON dumps: none in the case (QTc appears only in the fallback ECG). No new em or en dash in the diff. Citations are bracketed allow-list keys only. Lab `is_abnormal` flags agree with every numeric reference range; ESR 8, CRP 2, B12 420 and folate 10 were already identical at HEAD in P05-P09 and RM11 (kept per plan C13, flagged by the worker).

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- action-8-order-specialized-test (genetic panel) importance recommended -> required; added to stop_rule.required_before_assessment (the label names the genotype).
- icd_codes[0] G12.21 -> Z15.89 (accepted[0] unchanged: 'Suspected early ALS .. Gold Coast criteria not yet met'); new synonym entry Z15.89 scoped to ALS-P08 (suspected ALS, prodromal ALS, possible ALS, suspected motor neuron disease, mild motor impairment); G12.21 synonyms pruned with apply_diagnosis_synonyms.py --prune --conditions als, so a plain 'ALS' answer no longer scores as correct for a carrier who does not meet Gold Coast.
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, ALS case guards pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-5-interpret-labs]`.alternatives: was [CBC, CK, TSH, vitamin_B12]; now [CBC, CK, TSH, vitamin_B12, CMP, folate, inflammatory_markers] | [CBC, CK, TSH, vitamin_B12].
- Decision: serve: new first alternative (old order kept as an alternative). The label and rationale name renal and liver function, calcium, folate, ESR and CRP (liver baseline before riluzole, inflammatory mimics); the order named only CBC, CK, TSH and B12, so the CMP and inflammatory results the evidence cites were not returned.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.
