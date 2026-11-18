# VASC-DEM-S09

## Reviewer notes
Reviewer status: R1 in_progress, no R2 | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| b763111e-d07f-413d-b170-abb7493361c4 | FIXED (plan C4, D4, D11) | ground_truth.action_criteria[action-9-analyze-ecg].importance recommended -> required, rationale adds that the rhythm decides antiplatelet vs anticoagulant; stop_rule.required_before_assessment += action-9-analyze-ecg; assessment.required_recommendations[0] -> "Continue single antiplatelet therapy (aspirin 100 mg) ... if the ECG and the aetiological work-up identify no indication for anticoagulation"; new required_recommendations[1] "If the ECG and vessel imaging show no cause, arrange echocardiography and prolonged rhythm monitoring, which would change the antithrombotic choice [AHA_ASA_2021_secondary]" (echo, monitoring and MRA criteria stay optional) |
| 4bfc7ab6-e8ef-4efa-b328-c6167b5ca708 | FIXED (plan C2, D2) | ground_truth.action_criteria[action-5-order-specialized-test].importance required -> recommended; removed from stop_rule.required_before_assessment (now screen, labs, MRI, ECG); label "...to characterise the amnestic profile..."; rationale "Characterises the storage-type amnesia ... and sets a baseline for her fitness to practise and for memory rehabilitation; the screen, the informant history and the MRI establish the disorder [VASCOG_2014]" |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | initial_tool_outputs.specialized_test.findings[*].reference_range | Plan C6: percentile ranges "25th-75th percentile" | FIXED: "9th percentile or above (25th-75th average)"; no row in the 9th-24th band, flags unchanged |
| C | minor | ground_truth.differential[Subcortical ischaemic VaD].key_features | "exclude the diffuse subcortical mechanism" overstates (plan C8) | FIXED: "make the diffuse subcortical mechanism unlikely" |
| C | minor | ground_truth.avoided_actions | Plan C11: stored perfusion SPECT unlabelled | FIXED: avoid-waste-perfusion-spect ([NICE_NG97]); the structured headache history stays unlabelled (reasonable, past migraine) |

## Changes
The diagnosis (strategic thalamic infarct dementia) is unchanged. The 12-lead ECG is now required and must be done before the diagnosis is submitted, because the infarct was never investigated; the stop rule is now screen, labs, MRI and ECG. The formal neuropsychological battery is recommended rather than required: it characterises the storage-type amnesia and sets a baseline for fitness to practise, but the screen, the husband's history and the MRI establish the disorder. Aspirin is continued only if the ECG and the aetiological work-up find no indication for anticoagulation, and a new must asks for echocardiography and prolonged monitoring if the ECG and vessel imaging show no cause. Perfusion SPECT is now labelled waste; battery reference ranges follow the AACN labels (no score changes its flag). Checks: perfect_agent.py passes; test_case_guards for the case passes; case_io check: schema and synonym guard OK, no test failure names the case. No MRI edited.

## Verification
Pass 1: 0 errors found
- Checked: b763111e FIXED (ECG required and in the stop rule; antiplatelet must conditional; conditional echo/monitoring must, with optional echo, monitoring and MRA criteria to serve it), 4bfc7ab6 FIXED (battery recommended, out of the stop rule). No battery row in the 9th-24th band; SPECT labelled, headache history unlabelled per plan. MoCA losses add to 23. perfect_agent ok; case_io check and test_case_guards pass.
Cosmetic (not counted): none.
Pass 2: 0 errors found
- Checked: b763111e FIXED (ECG required and in the stop rule; antiplatelet must conditional on no anticoagulation indication; plan C4 conditional echo/monitoring must, served by the optional MRA, TTE and 14-day monitor), 4bfc7ab6 FIXED (battery recommended, out of the stop rule). MoCA losses (recall 5, orientation 2) add to 23; no battery row in the 9th-24th band; SPECT labelled, headache history unlabelled per plan. perfect_agent ok; test_case_guards -k S09 pass.
Cosmetic (not counted): none.
