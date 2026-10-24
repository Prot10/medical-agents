# FND-M01
Reviewer status: R1 none, R2 none (no notes file for FND) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case. The physician input for FND is the July 2026 tool guidance (plan 1.3), applied through the plan.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.neurological_exam.motor`, `initial_tool_outputs.clinical_assessment.findings` | Hoover sign described inverted ("during testing of right hip flexion, involuntary contralateral hip extension is noted"): that is the normal synkinesis of the good leg, not the functional sign. | FIXED: "Right hip extension is weak on direct testing but returns to full strength during left hip flexion against resistance". |
| B | minor | `patient.neurological_exam.motor` | Give-way weakness reported in both legs while HPI, Hoover sign and gait all concern the right leg only. | FIXED: give-way in right hip flexion and knee extension, left leg 5/5; tone stated for all limbs. |
| C | minor | `patient.neurological_exam.motor` | Tremor said to "entrain to distraction testing" (entrainment is to an externally cued rhythm). | FIXED: tremor of both arms takes on the rhythm of foot tapping cued by the examiner, diminishes in conversation. |
| C | major | `initial_tool_outputs.clinical_assessment` (plan H) | Meta keys in `criteria_met`; low-specificity signs (midline splitting, heel-shin inconsistency) counted, 7 "signs"; impression ended with the key leak "No further investigation is required...". | FIXED: canonical shape; 5 validated signs (Hoover, collapsing weakness, dragging gait, entrainment, distractibility); supportive features listed and not counted; observed event recorded (`functional_seizure_semiology_observed: true`); event-based impression. |
| B | major | `initial_tool_outputs.labs` (plan K) | Unexplained Na 149 (outside ED BMP normal per HPI); Hct 44.8 against MCV x RBC 42.2 and MCHC 29.7. | FIXED: Na 140 (normal), RBC 4.62, Hct 39.6 (85.7 x 4.62 / 10; MCHC 33.6); abnormal summary emptied; interpretation "All results within reference ranges." |
| B | major | `initial_tool_outputs.mri` (plan I) | Report "without and with contrast", `post_contrast` field, while the criterion is `contrast: false`. | FIXED: non-contrast report (T1, T2/FLAIR, DWI, SWI), impression "Normal non-contrast MRI of the brain...". MRIReport has no `contrast_used` field, so the technique is stated in the impression only. |
| B | minor | `initial_tool_outputs.eeg.impression` (plan J) | Impression omitted the three captured events and lacked a final period; event 3 had no duration. | FIXED: canonical impression naming the three events; event 3 "lasting about 5 minutes"; event 1 type "shaking". |
| C | major | `initial_tool_outputs.drug_interactions` (plan C) | Output only listed the medicines with the leak warning "...is a prescribing decision, not an output of this check"; escitalopram with ibuprofen and the as-needed lorazepam not identified. | FIXED: escitalopram + ibuprofen (GI bleeding), lorazepam + dicyclomine (minor additive CNS effects), lorazepam and escitalopram warnings, report-voice summary. |
| D | major | `followup_outputs[0]` (plan B) | Literature follow-up with fabricated content ("moderate effect sizes for seizure reduction"), misattributed "Espay ... BMJ 2018". | FIXED: deleted; one canonical `initial_tool_outputs.literature_search` keyed by the criterion query. |
| A | major | `ground_truth.action_criteria` (plan A, 3.2) | Template tiers (literature and drug check recommended, video-EEG optional), labels equal to rationales, "positive FND signs; AAN ..." citations, "FND criteria pack" strings. | FIXED: exam required, video-EEG required (`eeg_type: video`), drug check recommended, labs optional, MRI optional (`{contrast: false}`, any protocol), new optional `action-neuropsych-battery`, literature optional and last; short labels, patient-specific rationales, source keys; stop rule now exam + video-EEG. |
| C | major | `ground_truth.assessment` (plan D) | Seven musts with two duplicates, a neuropsychology must mis-tiered "recommended", a video-EEG test as a must, "Do NOT make the diagnosis by exclusion"; prohibitions citing "Stone 2018", EMG/NCS duplicate of the avoided actions. | FIXED: musts DX (signs and recorded events), COMM, PHYSIO, PSY (anxiety), RESCUE; prohibitions P1, P2, P3, P5, P6, P7. |
| C | major | `ground_truth.differential` (plan F) | Epileptic seizures `moderate` after a normal video-EEG; structural lesion "excluded" by an MRI not in the scored pathway; neuropathy "(when obtained) normal EMG/NCS" (EMG avoided); autoimmune encephalitis "(when obtained)"; malingering resting on a symptom-validity test never done. | FIXED: epileptic seizures `low` (canonical key feature plus semiology); MS `low` and structural brain or cord lesion `low`, both citing the examination; neuropathy, autoimmune encephalitis and malingering deleted. |
| D | major | `ground_truth.key_clinical_evidence` (plan E) | Generic items including the "Interim composition decision" leak, the "OPTIONAL" item and "Stone 2018" claims. | FIXED: five case-specific items. |
| B | minor | `ground_truth.red_herrings` (plan E) | "Family history of epilepsy" red herring while the FH says "No known family history of epilepsy"; trauma item cited Stone 2018; generic data points. | FIXED: epilepsy item deleted; the MS, psychiatric and adversity items now name the case data. |
| C | minor | `ground_truth.avoided_actions` (plan L) | Citations `[Stone_2018]` (not a real paper); generic rationales. | FIXED: `[Espay_2018]` / `[Stone_2016]`, patient-specific rationales; all kept as waste. |
| C | minor | `metadata.clinical_pearls` | Hoover pearl described the normal synkinesis as the sign; midline splitting called a positive sign; prolactin "remains normal after PNES" overclaims. | FIXED: Hoover, midline splitting and prolactin pearls corrected (plan 1.2 facts 2, 3, 6). |
| E | minor | `metadata.difficulty_rationale`, `metadata.revision_reason` | Template text ("comorbid SLE", "MRI + basic labs") and a revision reason now false ("every instrumental test optional"). | FIXED: case-specific rationale; revision reason and `last_revised` updated. |
| A | minor | `fallback_tool_outputs` (plan G) | `specialized_test` fallback with `test_type: ''` and the "itself a harm" leak; `advanced_imaging` modality `MRI_brain_functional`; drug fallback "(agent not specified...)"; echo without `echo_type`. | FIXED: the three nulled and removed from `metadata.fallback_tool_kinds`; echo `echo_type: TTE`. |

## Changes, in one paragraph a physician can read before re-reviewing

The policy now asks for the examination and a video-EEG (both required), a recommended medicine review, and leaves labs, a non-contrast brain MRI, neuropsychology and a literature search optional and uncredited. The examination was corrected: the Hoover sign is now described the right way (right hip extension weak on direct testing, full during left hip flexion), give-way weakness is confined to the right leg, and the arm tremor entrains to a cued rhythm. The structured examination counts five validated signs and lists midline splitting, heel-shin inconsistency and Romberg sway as supportive only, with the observed event. The video-EEG impression now names the three recorded events without ictal change. The sodium of 149 became 140 and the CBC is arithmetically consistent; the MRI report is non-contrast. The drug review names the escitalopram-ibuprofen bleeding risk and the as-needed lorazepam. Musts: positive diagnosis, explanation, functional-motor physiotherapy, psychological therapy with treatment of anxiety, and an event plan without benzodiazepines; prohibitions: further investigation without a new question, dismissive explanation, invasive tests, starting antiseizure drugs, benzodiazepines or intubation for a typical event, and gadolinium. Epileptic seizures are `low` after the video-EEG; MS and a structural lesion are `low` on examination grounds.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys used per plan 1.1: `[Daum_2014]`, `[Stone_2016]` (plan 5.1).
- MRIReport has no `contrast_used` field (only CTReport does), so plan I's `contrast_used: false` cannot be stored for an MRI; the technique is stated in the impression. Consider adding the field to MRIReport.
- EEG routing (plan 5.3): a `routine` EEG order would be served this video-EEG with its events.

## Open questions for Andrea (judgment calls you could not settle)

None. Placement decision: optional labs and MRI sit after the drug check and before neuropsychology and literature in `action_criteria`, since plan 3.1 places only required or recommended red-flag tests second.
