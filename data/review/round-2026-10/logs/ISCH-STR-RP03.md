# ISCH-STR-RP03
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 8b01e6c6-4870-4372-a193-d2c91130cbbd | FIXED | `patient.neurological_exam.mental_status`: GCS 14 (E4 V4 M6), as the reviewer reconstructed. The orientation text now says he gives his age but not the month or year (V4; LOC questions 1). Key evidence [1] states the GCS. |
| 7c967ef5-5b22-4f9e-b8ce-c4023ad5edc0 | FIXED | The VITT must is rewritten (must [4]): VITT follows adenoviral vector vaccines; mRNA was removed from the pairing. It states the three independent exclusions (inactivated vaccine; 24 to 48 hours, not 5 to 30 days; normal platelets 224 and D-dimer 250 µg/L), says no testing is needed, and adds reporting to the vaccine adverse-event system. The anti-PF4 row was removed from the thrombophilia follow-up. Key evidence [4], differential entry "VITT" (very low), prohibition [1] (no anti-PF4 testing) and red herring [0] say the same. The literature output that carried the VITT text was removed (orphan, mis-titled references). |
| 00e99485-c30f-47a3-ae33-63d943d100dc | FIXED | Added an `order_advanced_imaging` `MR_venography` follow-up: normal sinuses, deep veins and right convexity cortical veins, including those draining the infarct. Added a recommended criterion `mr-venography`. The reviewer's second point was also addressed: the infarct did not conform to an arterial territory, which argued against embolism. The MRI finding and impression now describe a territorial right MCA infarct (cortical and lenticulostriate branches: parietal cortex, subcortical white matter, corona radiata, posterior limb of the internal capsule). There is no persisting occlusion, the pattern of a recanalized embolus. Key evidence [3] explains why the venous mechanism is set aside: arterial territory, normal MRV, D-dimer 250. Differential: CVT very low. |
| 19ff066b-bde9-4228-aca4-f2520ebf9c47 | FIXED | Template LKW, door-to-needle and pre-IVT BP musts were removed. Must [0]: LKW is before the sensory prodrome, about 24 hours before arrival. The HPI now says the numbness persisted overnight and he went to bed with it at about 23:00, so waking hemiplegic does not reset LKW. Must [1] states the decision: no IVT (LKW about 24 hours, not an unknown-onset stroke, FLAIR positive, HI-1 transformation before treatment); no EVT (no occlusion). Prohibition [0] says the same. The drug check no longer screens tPA contraindications; it is now the antiplatelet check. |
| 3451a4bc-64f1-4ebf-b177-7ec7d4e8c9ab | FIXED | `patient.neurological_exam.cranial_nerves`: "Left lower facial weakness of upper motor neuron type ... with forehead sparing and full eye closure". |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.neurological_exam` (NIHSS) | NIHSS 16 was not itemised. A right parietal infarct with no neglect or extinction recorded; the visual fields were "difficult to assess". | FIXED: recount gives 16 (LOC questions 1, gaze 1 for the intermittent rightward preference he overcomes, facial palsy 2, left arm 4, left leg 4, sensory 2, dysarthria 1, extinction 1 for visual extinction on double simultaneous stimulation). Fields full to single stimuli; `additional` itemised; must [0] and key evidence [1]. |
| B | major | `initial_tool_outputs.ct` | NCCT template ("in the clinically implicated territory", "does not justify withholding treatment", "Nothing on this study contraindicates intravenous thrombolysis..."). It reported no infarct about 24 hours after LKW, although MRI shows a 4.2 x 3.1 cm infarct. | FIXED: evolving right MCA hypodensity (parietal cortex, subcortical white matter, corona radiata, posterior limb of internal capsule), ASPECTS 7 (M5, M6, IC), no haemorrhage, no hyperdense vessel. The petechial HI-1 change is left to SWI. |
| B | minor | `initial_tool_outputs.mri.findings[0].signal_characteristics.FLAIR` | "Possibly less than 12-24 hours in evolution" dated the infarct against an LKW that is about 24 hours. | FIXED: "less conspicuous than the DWI abnormality; no DWI-FLAIR mismatch". |
| D | major | `initial_tool_outputs.labs.panels["Exclusion studies"]` | Scaffolding panel with the leaking `sig` ("which is what this case's diagnosis rests on") duplicating the thrombophilia follow-up; the plan's baseline warning (aetiological criterion answered by the initial labs). | FIXED: panel removed. The thrombophilia follow-up trigger was renamed so that orders naming any of its assays reach it. Interpretive labels ("stress hyperglycemia") replaced by "(H)". |
| B | minor | `followup_outputs` CTA | `contrast_used` false. Impression "Completely normal" with a "vasculitis pattern" claim that CTA cannot make for small vessels. | FIXED: true. Impression: no occlusion, stenosis, dissection or aneurysm; normal arch. "No beading or segmental narrowing of the large intracranial arteries". |
| B | major | `followup_outputs` echo, criterion `action-9-order-echocardiogram` | Impression "Abnormal values: ... (H)". Shunt not graded. The criterion required `bubble_study: true` (not a tool parameter) with `echo_type: TEE`, while the stored study was a transthoracic bubble study. | FIXED: real report (large shunt, more than 30 microbubbles within 3 cycles after Valsalva; no atrial septal aneurysm; no thrombus or vegetation; LVEF 62%), `tool_parameters.echo_type` bubble_study. Added a TEE follow-up (PFO tunnel and septal anatomy, no LAA thrombus, no arch atheroma), as in P05. Criterion alternatives `bubble_study`, `TEE`; required. |
| B | major | `followup_outputs` Holter, criterion `action-10-order-cardiac-monitoring` | Criterion `event_monitor_30d` received a 48-hour Holter typed `holter_24h` (plan C2). | FIXED: `holter_48h` in the output, `tool_parameters` and the criterion's first alternative (holter_24h and telemetry as alternatives). Impression opens "Recorded on the stroke unit after admission, 48 hours."; min and max heart rate. Prolonged ambulatory monitoring became must [5]. |
| C | major | `followup_outputs` drug check | DAPT (aspirin plus clopidogrel) proposed for a NIHSS 16 stroke; ticagrelor and apixaban offered as alternatives. | FIXED: single antiplatelet (aspirin). Warnings: HI-1 does not preclude it; DAPT only for minor stroke or high-risk TIA; no anticoagulation without venous thrombosis or thrombophilia. Criterion recommended (plan C7), after the aetiological labs. |
| C | major | `followup_outputs` literature (2 outputs) | VITT output an orphan with mis-titled references; PFO output cited RESPECT's undetermined-mechanism HR 0.38 as the main result and the AAN 2020 advisory as an "AHA/ASA guideline" in Stroke. | FIXED: VITT output removed. PFO output corrected (CLOSE; RESPECT HR 0.55, and 0.38 for undetermined mechanism; Messe SR et al., Neurology 2020 practice advisory). Criterion optional, `required_arguments` {}, last. |
| C | major | `ground_truth.assessment` | Template musts (glucose, NCCT first, door-to-needle, pre-IVT BP, generic telemetry, generic secondary prevention with statin, "TEE + bubble, hypercoagulability, vessel imaging, CVST exclusion"), the 140/90 prohibition, the INR/platelet tPA list and the template anticoagulation prohibition. | FIXED: seven musts (LKW and NIHSS; decision; stroke unit with telemetry, swallow screen, IPC and rehabilitation; aspirin without DAPT or anticoagulation; VITT; prolonged ambulatory monitoring; PFO closure discussion with RoPE 9 and AAN 2020) and four prohibitions, including the canonical C5 BP text (BP 138/82, no reperfusion). |
| C | major | `ground_truth.differential` | Dissection, CVST and APS left "moderate" after the work-up excluded them; VITT, which the case raises, was missing. | FIXED: dissection, CVT, VITT, APS/thrombophilia and vasculitis very low, paroxysmal AF low, each with what excludes it. |
| C | minor | `ground_truth.key_clinical_evidence` | Template lines (WAKE-UP/EXTEND window, DAWN/DEFUSE "up to 24h", AF "required"), off-pathway and July-review lines. | FIXED: seven case-specific statements, including RoPE 9 computed from the record. |
| A | minor | `ground_truth.action_criteria`, `sequence_constraints`, `stop_rule`, `avoided_actions` | Labels equal rationales; duplicated or superseded keys; free-text citation string; hard template constraint; order not diagnostic. | FIXED: NCCT, labs, ECG, CTA, MRI (optional, `{}`), MRV (recommended), echo (required), monitoring (required), thrombophilia labs (recommended), drug check (recommended), literature (optional). Soft constraints per plan 3.3; stop rule NCCT, labs, ECG, CTA, echo, monitoring, max 1; 2026 key on the avoided actions. |
| E | minor | `ground_truth.red_herrings[0]` | "Inactivated COVID vaccines have not been associated with stroke" overstates the evidence. | FIXED: says they are not associated with VITT, the interval is too short and platelets and D-dimer are normal. |

## Changes, in one paragraph a physician can read before re-reviewing

A 36-year-old man had left arm and leg numbness at work 24 hours after an inactivated COVID-19 vaccine. It persisted overnight, and the next morning he woke with dense left hemiplegia. The exam is now internally consistent. GCS is 14 (E4 V4 M6). The facial weakness is of upper motor neuron type, with forehead sparing and full eye closure. Visual extinction is recorded, and NIHSS 16 is itemised. The imaging now tells one story. The NCCT shows the evolving right MCA infarct (ASPECTS 7), as expected about 24 hours after LKW. The MRI describes a territorial right MCA infarct (cortex to the posterior limb of the internal capsule) with HI-1 petechial transformation and no persisting occlusion. MR venography, newly added, is normal, so the venous infarct the reviewer raised is excluded. The decision is explicit: no IV thrombolysis (LKW about 24 hours, FLAIR positive, pre-treatment HI-1) and no thrombectomy (no occlusion). VITT is excluded on three grounds without testing, and the anti-PF4 assay is gone. The bubble study now grades a large shunt, and a TEE shows no atrial septal aneurysm. A 48-hour inpatient Holter, typed correctly, shows sinus rhythm, and the thrombophilia screen is negative. Management is single antiplatelet therapy (no DAPT, no anticoagulation) and prolonged ambulatory monitoring. PFO closure is discussed (RoPE 9, AAN 2020). The literature step is optional and correctly cited.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: the I63 list appends "cardioembolic stroke" and "lacunar stroke/infarct" to a PFO-related paradoxical embolism; "lacunar" is a wrong mechanism for a 4.2 cm territorial infarct.
- Citation keys `[AHA_ASA_Stroke_2026]`, `[AHA_ASA_2021_secondary]`, `[AAN_PFO_2020]` (plan section 5.1).
- Simulator: an `order_cardiac_monitoring` call with `event_monitor_30d` is answered with the stored 48-hour inpatient Holter, and a plain `TTE` call with the stored bubble study. In both cases the call asks for a different study than the one served.

## Open questions for Andrea (judgment calls you could not settle)

- To make the reviewer's mechanism point coherent, I rewrote the MRI distribution from "does not conform to a single territory, superficial MCA and borderzone" to a territorial right MCA infarct (cortical and lenticulostriate). The alternative was to keep the non-territorial description and argue it away; that would leave the imaging pointing at a venous mechanism the case rejects.
- The NCCT now shows the evolving infarct (ASPECTS 7). A normal CT about 24 hours after onset of a 4 cm infarct was not plausible, but the change makes the CT itself a further reason not to thrombolyse.
- Statin: LDL is 112 mg/dL. AHA/ASA 2021 recommends atorvastatin 80 mg after ischaemic stroke with LDL above 100 mg/dL and no major cardiac source, and a PFO is not usually counted as one. Plan C6 does not mandate a statin for a non-atherosclerotic mechanism, so I added no statin must. Please decide whether the PFO cases should carry one.
- A TTE order is served the bubble study but does not satisfy the echo criterion (alternatives bubble_study and TEE, as in P05). If you consider a TTE in a young stroke to include agitated saline by default, add `TTE` as a third alternative in both cases.

## Verification
Adversarial check (23 October 2026). Read the log, the diff, the patient block, every tool output and the ground truth.
- Notes: all five ids present and fixed as claimed. 8b01e6c6 (GCS 14, E4 V4 M6, orientation text matches), 7c967ef5 (VITT must restricted to adenoviral vectors with the three exclusions, anti-PF4 removed), 00e99485 (MR venography criterion and normal follow-up; territorial MCA infarct; key evidence on the venous mechanism), 19ff066b (LKW about 24 hours, no IVT, no EVT, template IVT musts removed), 3451a4bc (UMN facial weakness with forehead sparing and eye closure).
- Recounted: NIHSS 16 (questions 1, gaze 1, face 2, arm 4, leg 4, sensory 2, dysarthria 1, extinction 1); RoPE 9 correct. NCCT (ASPECTS 7: M5, M6, IC), MRI and key evidence describe the same territorial right MCA infarct; FLAIR no longer contradicts LKW; CTA contrast true; echo criterion alternatives exist in the vocabulary (`bubble_study`, `TEE`) and both follow-ups are served; Holter typed 48 h.
- Not changed, noted: the statin question (LDL 112 mg/dL, AHA/ASA 2021 atorvastatin for LDL above 100 without a major cardiac source) is a condition-level decision already raised as an open question; the MRI report line "dedicated MR venography not performed" is accurate for that study and the MRV is now orderable.
- No changes made. `perfect_agent.py ISCH-STR-RP03 -v` passes; `case_io.py check` clean for the case.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The I63 category no longer appends mechanism labels ("embolic", "cardioembolic", "lacunar") or the bare label "stroke" (which matched "haemorrhagic stroke" or "stroke mimic"); mechanism labels and code families now sit on the specific codes.
Paradoxical-embolism labels scoped to this case.
- labels removed: "cardioembolic stroke", "lacunar stroke", "lacunar infarct", "stroke"
- labels added: "paradoxical embolism", "paradoxical embolic stroke"
- codes removed: I63.4, I63.5, I63.3, I63.2, I63.0, I63.1, I63.8, I63.81, I63.89
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

Decisions: `plans/ISCH-STR-decisions.md`.

- Echo outputs: added `echo_type` "bubble_study" and "TEE" to the two stored echo reports; strict xfail removed from `test_echo_type_routing.py` (test passes).
- Must added: atorvastatin 80 mg for LDL 112 mg/dL after non-cardioembolic stroke (AHA/ASA 2021 COR 1, SPARCL) (decision OQ4g).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Minor non-specific finding.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-3-interpret-labs]`.alternatives: was [glucose, CBC, coagulation, creatinine, troponin]; now [glucose, CBC, coagulation, creatinine, troponin, ESR, CRP] | [glucose, CBC, coagulation, creatinine, troponin].
- Decision: serve: new first alternative (old order kept as an alternative). The vasculitis differential reads the mildly raised CRP and ESR.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.
