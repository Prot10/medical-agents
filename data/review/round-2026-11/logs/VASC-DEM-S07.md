# VASC-DEM-S07

## Reviewer notes
Reviewer status: R1 in_progress, no R2 | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 2c6f29cf-7333-4ef0-8ca2-452a72d6c204 | ALREADY-FIXED + CENTRAL (plan C5, D5) | Checked: action-6-order-advanced-imaging requires {modality: carotid_duplex}; action-7-order-cardiac-monitoring requires {monitor_type: event_monitor_30d}; both in the stop rule. Harness probe: holter_24h and holter_48h orders match no criterion and receive the library normal Holter, not the 30-day report. Added MR_angiography alternative to action-6 (CAROTID-ALT; stored MRA under 30% right, agrees with the duplex); label -> "Image the cervical carotid arteries (duplex or MR angiography) ...". Display: CENTRAL.md item 3 |
| fa0764bd-4448-4868-b94c-58847c5fc7f8 | FIXED + CENTRAL (plan C11, D12) | ground_truth.avoided_actions: added avoid-waste-perfusion-spect, avoid-waste-levodopa-challenge, avoid-waste-tee (echo_type TEE), avoid-waste-dti-tractography, avoid-waste-ct-perfusion, avoid-waste-perfusion-mri, avoid-harm-cerebral-angiography. Reviewer steps 9, 11-15, 17 = base follow-ups 0, 2-6, 8 (checked by content). Stored reports kept; followup_outputs: request_mr_angiography first, then on-request. Display: CENTRAL 1 |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | initial_tool_outputs.specialized_test.findings, .impression, .quantitative_data.pattern | Plan C6: SDMT 9th, Rey copy 10th, RAVLT delayed recall 22nd flagged 'yes' against 25th-75th; impression called them impaired/reduced | FIXED: AACN ranges and labels (those three "low average"; TMT-B 6th stays "yes"); impression: executive impairment with low-average speed, visuoconstruction and free recall |
| C | minor | ground_truth.action_criteria[action-8-order-specialized-test].expected_evidence, .label | Evidence called the low-average scores deficits | FIXED: "Executive impairment (Trail Making B 6th percentile) with low-average processing speed, visuoconstruction and free recall..."; label "characterise the profile" |
| C | minor | ground_truth.assessment.required_recommendations[4]; prohibited_recommendations[4] | "visuoconstructional deficit" / "visuospatial deficit is documented" rested on a low-average Rey copy | FIXED: "visuoconstructional errors on testing" / "visuospatial errors are documented on testing" (MoCA cube and clock errors remain) |
| C | minor | ground_truth.differential[Subcortical ischaemic VaD, Large-artery atherosclerosis].key_features | Plan C8: "far below the threshold for attributing a dementia to small-vessel disease"; "no single artery can supply" | FIXED: Fazekas 1 with one thalamic lacune is not the extensive burden that supports a subcortical cause [VasCog2_WSO_2025]; "a single stenosed artery does not explain infarcts in opposite hemispheres" |
| C | minor | ground_truth.assessment.required_recommendations[4] | Must names formal visual field testing, which no criterion orders | FLAGGED, kept: it is a referral for the pre-driving assessment, not a current work-up step; a perimetry order now gets the library full-field report, consistent with fields full on confrontation |

## Changes
The diagnosis (multi-infarct cardioembolic vascular dementia with paroxysmal AF found on 30-day monitoring) and the required work-up are unchanged. Checked for the reviewer: the stop rule already demands a carotid duplex and a 30-day event monitor, and a Holter order neither satisfies the criterion nor receives the 30-day recording. The carotid criterion now also accepts MR angiography of the neck, whose stored report agrees with the duplex. The studies the reviewer asked to remove (perfusion SPECT, levodopa challenge, TEE, DTI, CT and MR perfusion, catheter angiography) are kept only as answers to an explicit order and are now penalised (catheter angiography as harm, the rest as waste); the follow-up list shows the credited MR angiography first. The battery uses the AACN 2020 labels (SDMT 9th, Rey copy 10th and delayed recall 22nd are low average; Trail Making B 6th remains impaired), and the impression, criterion evidence, driving must and driving prohibition were reworded to match. Two differential entries no longer claim a lesion-burden threshold. Checks: perfect_agent.py passes; test_case_guards for the case passes; case_io check: schema and synonym guard OK, no test failure names the case. No MRI edited.

## Verification
Pass 1: 0 errors found
- Checked: 2c6f29cf ALREADY-FIXED (duplex and event_monitor_30d required; probe: holter_24h and holter_48h get the library normal Holter, never the 30-day AF report), fa0764bd FIXED (steps 9, 11-15, 17 = fu 0, 2-6, 8 labelled). CHA2DS2-VA 4 and apixaban dose correct; right-sided visual episode matches the left PCA infarct; battery labels, impression, evidence, driving must and prohibition agree. perfect_agent ok; case_io check and test_case_guards pass.
- CENTRAL (observation, pre-existing): an untyped echo order is served the stored TEE follow-up (see S11 log).
Cosmetic (not counted): none.
Pass 2: 0 errors found
- Checked: 2c6f29cf ALREADY-FIXED (carotid_duplex and event_monitor_30d required and in the stop rule; MRA alternative agrees); fa0764bd FIXED (base fu 0, 2-6, 8 = steps 9, 11-15, 17, labelled; gait and MRA kept). MoCA losses add to 21; CHA2DS2-VA 4 and apixaban dose correct; left PCA infarct matches the right-field episode, right MCA infarct the left arm deficit; battery labels, impression and evidence agree; red-herring PMH index 3 is the visual episode. The visual-field must is a pre-driving referral (kept, as pass 1). perfect_agent ok; test_case_guards -k S07 pass.
Cosmetic (not counted): none.
