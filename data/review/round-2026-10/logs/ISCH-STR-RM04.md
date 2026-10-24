# ISCH-STR-RM04
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| a220ccd8-21c0-4902-9469-5c12ffba0249 | FIXED | `patient.neurological_exam.additional`: "NIHSS score: 2 (limb ataxia 2: right arm and right leg; all other items 0; gait ataxia is not scored)." Same total in must [0] and key evidence [1], which also explains that gait and truncal ataxia are not on the scale. |
| d0aedb17-7635-4f4c-8147-4c2f2297d05b | FIXED (V4 extension kept) | Plan option kept: the intradural V4 extension explains the absent PICA opacification. Must [2]: aspirin for at least 3 months, no anticoagulation (SAH risk in intradural dissection), CADISS and the AHA/ASA COR 2a recommendation cover extracranial dissection only. Must [1] (decision): IVT not given because the intradural extension makes benefit uncertain with SAH risk. Drug check (`followup_outputs[1].output`) no longer offers apixaban or warfarin and warns that anticoagulation is generally avoided in intradural dissection. New prohibition [0]: no anticoagulation. Key evidence [4], [5]; literature summary states the trials do not cover intradural dissection. CTA and MRI impressions now say "into the intradural V4 segment". |
| 17db3372-9b52-4cf4-92c8-f669fd646b25 | FIXED | `initial_tool_outputs.mri.impression` item 2 adds "The T1-hyperintense (methemoglobin) hematoma indicates a dissection several days old, older than the hyperacute infarct" (a within-imaging statement; the report does not cite the history). Key evidence [3] links it to the neck pain that began 3 days earlier. The `subacute` label in `findings[0].signal_characteristics.T1_fat_sat` is kept, as the reviewer judged it right. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts (NCCT first, LKW for eligibility, CTA for thrombectomy, T1 fat-sat MRI as a must, lipid-lowering for a non-atherosclerotic mechanism, CADISS "3-6 months"); no stated reperfusion decision (plan C4); no telemetry must (C2). | FIXED: seven musts: LKW and NIHSS, decision (no IVT, no EVT, with reasons), aspirin without anticoagulation, stroke unit with telemetry and cerebellar swelling watch with early neurosurgery, stop ibuprofen, follow-up vessel imaging at 3 to 6 months, avoid heavy lifting and neck manipulation. Statin must removed (plan C6: LDL 118 mg/dL at 34 without an atherosclerotic mechanism). |
| C | major | `ground_truth.assessment.prohibited_recommendations` | "Below 140/90" prohibition (plan C5); generic tPA-before-CT and "do not delay CT for history" prohibitions. | FIXED: canonical COR 3 BP prohibition (BP 144/88, neither IVT nor EVT); no-anticoagulation prohibition; LP prohibition reworded (CT within 6 hours negative, herniation risk); thunderclap prohibition kept. |
| B | major | `followup_outputs` (hypercoagulability panel) | Orphan thrombophilia panel (plan C9). | FIXED: removed. |
| A | major | `ground_truth.action_criteria`, `followup_outputs` order | Echo, Holter, literature, drug check, thrombophilia first, CTA last (plan C1). | FIXED: criteria NCCT, labs, ECG, CTA, MRI, drug check, echo, monitoring, literature; follow-ups CTA, drug check, echo, Holter, literature; ids unchanged. |
| C | minor | `ground_truth.action_criteria[action-4-analyze-brain-mri]` | MRI optional although CT is insensitive in the posterior fossa and only equivocal here; DWI defines the infarct size that sets the swelling risk. | FIXED: recommended, `required_arguments` {}; see Open questions. |
| C | minor | `ground_truth.action_criteria[action-8, action-9]` | Echo and Holter required although the dissection explains the infarct. | FIXED: recommended (plan 3.1); monitoring alternatives holter_24h, holter_48h, telemetry; `tool_parameters` added to both follow-ups. |
| C | major | `followup_outputs[4].output` (literature) | "VAD accounts for 10-25% of strokes under 45" (that is cervical artery dissection overall); CADISS given a non-existent "Final Results" title; a 2019 guideline cited for dissection antithrombotics and thrombectomy. | FIXED: Biller 2014 statement with its real title; CADISS 2015 real title, noting intracranial dissection was not studied; Kleindorfer 2021 dissection recommendation (COR 2a); criterion optional, `required_arguments` {}, last. |
| B | minor | `patient.neurological_exam.cranial_nerves` | "Mild right facial hypohidrosis noted on forehead" with no ptosis or miosis and no medullary lesion: unexplained by the PICA cerebellar infarct and not a Horner syndrome. | FIXED: sentence removed. |
| B | minor | `patient.neurological_exam.gait` | "Romberg positive with eyes closed" in cerebellar ataxia (Romberg tests proprioception; he cannot stand feet together with eyes open). | FIXED: "Unable to stand with feet together even with eyes open, swaying to the right; Romberg test not interpretable." |
| B | minor | `followup_outputs[0].output.findings[2]` (CTA) | "Right PICA territory supplied via basilar perforators" (basilar perforators do not supply the PICA territory); finding typed "Normal" while describing PICA occlusion. | FIXED: "Absent opacification of the distal right PICA, consistent with occlusion"; right AICA listed patent; type "Posterior circulation". Impression numbered and naming the intradural extent. |
| C | major | `ground_truth.differential` | Cerebellar haemorrhage "high" and SAH "moderate" although excluded by CT ("no xanthochromia on imaging" is meaningless). | FIXED: cerebellar haemorrhage very low; SAH low with the intradural rupture risk named and the 6-hour CT and CTA as evidence; vestibular neuritis very low; atherosclerosis, cardioembolism low; basilar occlusion very low. |
| C | minor | `ground_truth.key_clinical_evidence` | "Posterior circulation stroke causes ... NOT contralateral hemiparesis" (false: brainstem strokes cause crossed hemiparesis); CADISS "3-6 months, choice by infarct size"; off-pathway and July-review engineering lines (plan C17). | FIXED: nine case-specific pearls (presentation, NIHSS limits, prodrome, hematoma age, intradural extension, IVT, no basilar occlusion, swelling, inflammatory markers). |
| C | minor | `ground_truth.red_herrings[0].correct_interpretation` | Attributed CRP 1.4 and ESR 22 at 2 hours to infarction (an acute-phase response does not appear within 2 hours). | FIXED: nonspecific, cannot reflect the infarct at 2 hours, no systemic features of vasculitis. |
| C | minor | `ground_truth.avoided_actions[avoid-harm-1-analyze-csf].rationale` | "Transtentorial herniation" from LP with a posterior fossa lesion (the risk is tonsillar). | FIXED: reworded; citations of all avoided actions `[AHA_ASA_Stroke_2026]`. |
| B | minor | `followup_outputs[3].output.impression` (Holter) | No admission framing. | FIXED: "Recorded on the stroke unit after admission, 24 hours." |
| A | minor | `ground_truth.action_criteria[*]`, `sequence_constraints`, `stop_rule` | Label equals rationale; duplicated `[AHA_ASA_2019]` and free-text citations; template hard constraint; stop rule with echo and Holter and 0 extra actions. | FIXED: distinct labels and rationales; 2026/2021 keys; soft NCCT before CTA, CTA before echo and monitoring; stop rule NCCT, labs, ECG, CTA, drug check, `max_additional_actions` 1. |
| E | minor | `metadata.difficulty_rationale` | Listed "MR_angiography or carotid_duplex" as required tools. | FIXED: describes the current tiers and the intradural decision. |

## Changes, in one paragraph a physician can read before re-reviewing

A 34-year-old man with a right PICA cerebellar infarct from a right vertebral artery dissection extending from V3 into the intradural V4 segment, 2 hours after a thunderclap headache during heavy squats, after 3 days of neck pain. The NIHSS is now 2 (limb ataxia 2), and the case says that gait ataxia is not on the scale. The unexplained forehead hypohidrosis and the misapplied Romberg are gone. The work-up reads NCCT, admission bloods, ECG and CTA (required), MRI (recommended, because CT is equivocal in the posterior fossa), the ibuprofen drug check (required), then echo and rhythm monitoring (recommended) and optional literature. The thrombophilia panel is removed. The MRI impression explains that the T1-bright hematoma is several days older than the hyperacute infarct, and a pearl links this to the 3-day neck pain. The decision is now explicit: no IV thrombolysis, because the intradural extension makes the benefit uncertain and carries a subarachnoid haemorrhage risk; no thrombectomy, because the basilar artery is patent. Management is aspirin without anticoagulation for at least 3 months (the trials and the guideline recommendation cover extracranial dissection only), stopping ibuprofen, a stroke unit with telemetry, watching for cerebellar swelling with early neurosurgical involvement, follow-up vessel imaging and activity advice. Haemorrhage and SAH are now low or very low in the differential.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: I63.011 appends "lateral medullary syndrome", "wallenberg syndrome" and "lateral medullary infarct" to this case, which has a PICA cerebellar infarct and no medullary lesion (MRI: no brainstem infarct). An agent naming Wallenberg syndrome would be credited. Restrict those labels to cases with a lateral medullary infarct (for example M04). The I63 category also appends "lacunar stroke", "cardioembolic stroke" and "embolic stroke" to every ISCH case, which credits a wrong mechanism.
- Citation keys `[AHA_ASA_Stroke_2026]`, `[AHA_ASA_2021_secondary]` (plan section 5.1).

## Open questions for Andrea (judgment calls you could not settle)

- IVT decision: the guideline rates thrombolysis in known or suspected intracranial dissection as of uncertain usefulness. Following the plan ("intradural extension weighs against IVT"), the must says do not give it, although he is within 4.5 hours with a disabling gait ataxia. A reviewer may prefer "may be considered after discussing the uncertain benefit". No prohibition forbids IVT, so an assessment that gives it is not marked contraindicated.
- MRI is recommended here, not optional as in plan section 3.1, because CT is equivocal in the posterior fossa and the infarct size governs the swelling watch.

## Verification
Adversarial check (23 October 2026). Read the log, the diff, the patient block, every tool output and the ground truth.
- Notes: all three ids present and fixed as claimed. a220ccd8: NIHSS 2 (limb ataxia 2) in the exam, must [0] and key evidence [1]; gaze-evoked nystagmus correctly unscored. d0aedb17: V4 extension kept; aspirin only, no anticoagulation, CADISS and the COR 2a recommendation limited to extracranial dissection in must [2], key evidence [4], drug check and literature; IVT decision addresses the intradural extension. 17db3372: MRI impression and key evidence [3] explain the subacute hematoma by the 3 days of neck pain.
- Cross-field: dissection extent (V3 at the atlantoaxial level into V4, 3.5 cm) agrees in CTA, MRI and musts; PICA non-opacification in CTA and MRI; basilar patent (no EVT); BP 144/88 with the COR 3 prohibition and no reperfusion; LP prohibition and harm avoided action agree; differential matches the work-up (haemorrhage very low, SAH low). Literature references verified (Biller 2014 statement title, CADISS 2015, Kleindorfer 2021).
- Judgment accepted, not changed: "do not give IVT" for an intradural dissection is stronger than the guideline's uncertain-benefit wording but follows plan section 4 and is already an open question; MRI recommended (posterior fossa) is sound.
- No changes made. `perfect_agent.py ISCH-STR-RM04 -v` passes; `case_io.py check` clean for the case.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The I63 category no longer appends mechanism labels ("embolic", "cardioembolic", "lacunar") or the bare label "stroke" (which matched "haemorrhagic stroke" or "stroke mimic"); mechanism labels and code families now sit on the specific codes.
No medullary infarct: lateral medullary/Wallenberg labels are now scoped to M04; PICA/cerebellar labels scoped to this case.
- labels removed: "embolic stroke", "cardioembolic stroke", "lacunar stroke", "lacunar infarct", "stroke", "lateral medullary syndrome", "wallenberg syndrome", "lateral medullary infarct"
- labels added: "PICA infarct", "cerebellar infarct"
- codes removed: I63.4, I63.5, I63.3, I63.2, I63.1, I63.8, I63.81, I63.89
- codes added: I63.01
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

Decisions: `plans/ISCH-STR-decisions.md`.

- Echo output: added `echo_type` "TTE" to the stored echocardiogram report (the schema now keeps the field and the MockServer routes TTE/TEE/bubble orders by it; the value was only in `tool_parameters`).
- IVT decision must reworded: intradural extension has uncertain benefit in the guideline, so withholding is the safer choice for an NIHSS 2 ataxic deficit (decision OQ2).
- Must added: atorvastatin 80 mg for LDL 118 mg/dL (AHA/ASA 2021 COR 1, SPARCL) (decision OQ4g).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
