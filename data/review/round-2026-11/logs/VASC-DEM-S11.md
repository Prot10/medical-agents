# VASC-DEM-S11

## Reviewer notes
Reviewer status: R1 in_progress, no R2 | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 77ee2163-9fb5-4b05-875b-2365c0e8b65d | ALREADY-FIXED + CENTRAL (plan C5, D5) | Checked: action-6-order-advanced-imaging (stop rule) already required {modality: carotid_duplex}. Added {modality: MR_angiography} alternative (CAROTID-ALT; stored MRA right 50-60%, left under 30%, agrees with the duplex); label -> "Image the cervical carotid arteries (duplex or MR angiography): the result of the acute carotid study is not available". Display: CENTRAL.md item 3 |
| ddd47148-a4fc-4453-add6-c575843cf168 | FIXED (plan C12, D13) | ground_truth.avoided_actions: avoid-waste-7-order-cardiac-monitoring deleted; new optional ground_truth.action_criteria[action-prolonged-monitoring] order_cardiac_monitoring {} (label "Consider prolonged ambulatory rhythm monitoring (about 30 days) if the stroke mechanism remains uncertain", [AHA_ASA_2021_secondary]); new initial_tool_outputs.cardiac_monitoring (event_monitor_30d, 720 h, sinus rhythm, no AF, no pauses); new soft sequence_constraints[1] ECG (action-5) before monitoring; Holter fallback kept |
| db0cbe3b-2adb-49ce-b7c4-ebf05079cb37 | FIXED + CENTRAL (plan C11, D12) | ground_truth.avoided_actions: added avoid-waste-perfusion-spect, avoid-waste-levodopa-challenge, avoid-waste-ssep, avoid-waste-dti-tractography, avoid-waste-ct-perfusion, avoid-waste-perfusion-mri, avoid-waste-functional-mri. Reviewer steps 7, 9, 11-14, 17 = base follow-ups 0, 2, 4-7, 10 (checked by content). TEE (step 10) and catheter angiography (step 16), kept by the reviewer, unlabelled: avoid-waste-6-order-echocardiogram narrowed from {} to {echo_type: TTE} (its rationale is a repeat TTE). followup_outputs: request_mr_angiography first. Display: CENTRAL 1 |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | ground_truth.avoided_actions[avoid-waste-6-order-echocardiogram].alternatives | The wildcard repeat-echo label also penalised a TEE, which the reviewer kept and plan D12 leaves unlabelled | FIXED: narrowed to {echo_type: TTE}. Side effect (noted): an echo order without echo_type is now unlabelled and receives the stored TEE follow-up |
| C | minor | initial_tool_outputs.specialized_test.findings; action-7 label | Plan C6: RAVLT delayed recall 22nd flagged 'yes' against 25th-75th | FIXED: AACN ranges on percentile rows; 22nd "low average"; label "characterise the profile" |

## Changes
The diagnosis (post-stroke vascular dementia after a right MCA superior division infarct) and the required work-up (screen, labs, MRI, carotid imaging) are unchanged. Checked for the reviewer: the required carotid criterion already demanded a carotid duplex; it now also accepts MR angiography of the neck, whose stored report agrees with the duplex. Prolonged rhythm monitoring is no longer labelled low-yield: it is an optional step to consider if the mechanism remains uncertain, answered by a new 30-day event monitor in sinus rhythm, after the ECG. The studies the reviewer asked to remove (perfusion SPECT, levodopa challenge, SSEP, DTI, CT and MR perfusion, fMRI) are kept only as answers to an explicit order and are labelled waste; TEE and catheter angiography stay unlabelled, and the repeat-echo waste label now names TTE only. The battery's delayed recall (22nd percentile) is labelled low average. Checks: perfect_agent.py passes; test_case_guards for the case passes; case_io check: schema and synonym guard OK, no test failure names the case. No MRI edited; the new monitoring output was checked through the harness (30-day order and untyped order receive it, a Holter order receives the stored 24 h Holter).

## Verification
Pass 1: 0 errors found
- Checked: 77ee2163 ALREADY-FIXED (duplex + MRA alternative, MRA 50-60% agrees with duplex), ddd47148 FIXED (monitoring label removed; optional criterion served the new 30-day sinus-rhythm monitor; ECG-before-monitoring soft constraint, both ids exist), db0cbe3b FIXED (steps 7, 9, 11-14, 17 = fu 0, 2, 4-7, 10 labelled waste; TEE and catheter angiography unlabelled). The repeat-TTE label narrowed to {echo_type: TTE} still matches an untyped echo order under the reward (schema default TTE, policy_reward._schema_defaults). Battery labels correct. perfect_agent ok; case_io check and test_case_guards pass.
- CENTRAL (mock_server.py, observation, pre-existing): an echo order without echo_type (schema default TTE) is served the stored TEE follow-up, while an explicit TTE order gets the case fallback TTE; same in S07. The default TTE should take the TTE answer.
Cosmetic (not counted): avoid-waste-levodopa-challenge rationale said "slowed left-sided movement", not in the exam; now "the left-sided weakness and spastic left arm tone".
Pass 2: 0 errors found
- Checked: 77ee2163 ALREADY-FIXED (duplex required, MRA alternative 50-60% agrees), ddd47148 FIXED (waste label removed; optional action-prolonged-monitoring served by the new 30-day sinus-rhythm monitor; ECG-first soft constraint, ids exist), db0cbe3b FIXED (fu 0, 2, 4-7, 10 = steps 7, 9, 11-14, 17 labelled; TEE and catheter angiography unlabelled; repeat-echo label narrowed to TTE). MoCA losses add to 20; Bells 3 left omissions flagged against "difference under 3"; RAVLT 22nd low average. perfect_agent ok; test_case_guards -k S11 pass.
Cosmetic (not counted): none.
