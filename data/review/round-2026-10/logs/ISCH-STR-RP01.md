# ISCH-STR-RP01
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 97a9f686-9003-4e92-bf27-c87f7ac74397 | FIXED | Thiamine row ("Not resulted", flagged normal) removed from `initial_tool_outputs.labs.panels["Toxicology and Other"]`. The reviewer's "add an action that gives thiamine" is met as a must, because treatment is never a tool call (ROUND_POLICY ruling 4): must [3] "Give high-dose IV thiamine ... before any further glucose-containing fluid", plus prohibition [3] "Do not give glucose-containing fluids before thiamine". The HPI's "forced diuresis" became "Intravenous fluids were started". Wernicke stays in the differential (low) as a concurrent risk, and key evidence [4] explains it. |
| 55e9c9c7-878d-4ff6-bd00-0621498ac03c | FIXED | Thrombectomy is now an explicit must [2]: proceed for the basilar artery occlusion, NIHSS 14, pre-stroke mRS 0 (HPI now states she is fully independent and works full time), PC-ASPECTS 6, within 24 hours of LKW, AHA/ASA 2026 §4.7.3 COR 1, with pre-procedure BP at or below 185/110 and no systolic target below 140 after recanalization. PC-ASPECTS is computed: both cerebellar hemispheres (1 + 1) and pons (2) give 10 - 4 = 6 (medulla not scored); it is stated in the CTA (new source-image finding and impression item 2) and the MRI impression. Decision must [1]. As a procedure it is a must, not a tool criterion (ruling 4). |
| 19d1e303-10d4-4d11-8a30-e2b91f384b1f | FIXED | The governing LKW is 23:00 the previous evening. The HPI now states the bedtime and that at 10:30 she "still could not walk without help and the nystagmus persisted" (no return to baseline). The exam summary says "partial improvement of ataxia (still unable to walk unaided)". Must [0] (LKW and NIHSS) and must [1] (no IVT, because more than 15 hours have passed and she never returned to baseline). Prohibition [2]: do not treat 14:00 as a new onset. A red herring for the 14:00 deterioration and key evidence [1]. The drug-check output (`followup_outputs[1]`) names the 4.5-hour window and the rule that only a full return to baseline resets LKW. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | Conclusion "raised concern for an evolving posterior circulation event rather than simple alcohol intoxication" (leaks the diagnosis); "early cerebrovascular disease in the mother" (stroke at 68 is not early) with a DVT hint. | FIXED: replaced by "She was urgently re-evaluated."; family history stays in its list. |
| C | major | `patient.neurological_exam.mental_status` | GCS 11 (E3 V3 M5) contradicts the text (follows one-step commands = M6; confused but oriented to self = V4). | FIXED: GCS 13 (E3 V4 M6); "arousable to loud voice" (sternal rub removed, so LOC 1 matches); "cannot give the month or her age" added for item 1b. |
| C | minor | `patient.neurological_exam.additional`, `.motor`, `.cranial_nerves` | NIHSS 14 not itemised; face and drift not documented. | FIXED: recount gives 14 (LOC 1, questions 2, commands 1, gaze 1 for the sixth nerve palsies, face 1, each arm 1, each leg 1, limb ataxia 2, dysarthria 2); exam now documents mild bilateral lower facial weakness and drift of all four limbs; key evidence [3]. |
| B | major | `initial_tool_outputs.mri.additional_observations` | "Compared to initial MRI obtained 8 hours earlier, falsely negative" and "confirming persistent occlusion": no earlier MRI exists in the history. | FIXED: comparison removed, MRA "consistent with occlusion"; metadata difficulty text no longer relies on an earlier MRI. |
| B | minor | `followup_outputs[0].output` (CTA) | `contrast_used` false; "Dense basilar sign noted on non-contrast CT" contradicts the NCCT ("not hyperdense") and is cross-modality. | FIXED: true; sentence removed; numbered impression adds PC-ASPECTS 6 on source images. |
| D | major | `initial_tool_outputs.ct` | NCCT template management text ("in basilar", "does not justify withholding treatment", "must not delay angiography", "would mandate neurosurgical consultation rather than thrombolysis", "Nothing on this study contraindicates..."). | FIXED: anatomical observations, brainstem beam-hardening limit stated; canonical posterior-circulation impression without ASPECTS. |
| B | major | `initial_tool_outputs.labs.panels["Exclusion studies"]`, `followup_outputs` hypercoagulability panel, criterion `action-5-interpret-labs` | Exclusion panel with leakage `sig` ("which is what this case's diagnosis rests on"), stating homocysteine "within reference range" against 18.6 in the follow-up; secondary-prevention lab criterion answered by the initial labs (plan baseline warning); orphan thrombophilia panel with factor V Leiden. | FIXED: exclusion panel, criterion and follow-up removed (plan C9: not indicated in this mechanism; lipids are in the admission bloods). |
| B | minor | `followup_outputs[2].output` (echo) | Impression "Abnormal values: ... (H)"; shunt not graded; LAVI without unit. | FIXED: real impression (PFO with moderate shunt on Valsalva, no atrial septal aneurysm; mild concentric LVH, LVEF 60%, grade I diastolic dysfunction; no thrombus); `tool_parameters` TTE. |
| B | minor | `followup_outputs[3].output` (Holter) | 48-hour recording typed `holter_24h`; impression concluded "no arrhythmic source for cardioembolism". | FIXED: `holter_48h` (output, `tool_parameters`, criterion first alternative; holter_24h and telemetry as alternatives); impression opens "Recorded on the stroke unit after admission, 48 hours."; min/max heart rate added. |
| C | major | `followup_outputs[1].output` (drug check) | Alteplase checklist silent on the time window. | FIXED: window and LKW rule first; sertraline bleeding, sulfonamide allergy, BP limits; tenecteplase and direct thrombectomy as alternatives. Criterion recommended (plan C7), placed after CTA. |
| C | major | `followup_outputs[4].output` (literature) | ATTENTION and BAOCHE dated 2023, BAOCHE attributed to Langezaal (BASICS); "mortality approaches 85-95%" claim. | FIXED: ATTENTION (Tao C et al.) and BAOCHE (Jovin TG et al.), NEJM 2022, correct effect sizes; mortality claim removed; criterion optional, `required_arguments` {}, last. |
| C | major | `ground_truth.assessment` | Template musts (door-to-needle, pre-IVT BP, generic secondary prevention); 140/90 BP prohibition; template tPA and anticoagulation prohibitions. | FIXED: nine musts (LKW and NIHSS, decision, EVT with BP, thiamine, swallow and airway, stroke unit with telemetry and cerebellar swelling watch, alcohol withdrawal with K and Mg replacement, mechanism with probably incidental PFO and ambulatory monitoring, antiplatelet after 24-hour imaging with atorvastatin 80 mg for LDL 138, BP below 130/80, smoking and alcohol cessation); four case-specific prohibitions. |
| C | major | `ground_truth.differential` | "Top-of-the-basilar syndrome from cardioembolism" high (a mechanism, not an alternative, and no thalamic or PCA lesion); ethanol "below threshold" (metadata concern); "Percheron ... from venous origin" (Percheron is arterial, and there is no thalamic lesion). | FIXED: intoxication low (intoxicated, but focal signs and the occlusion exclude it), Wernicke low, dissection, haemorrhage and hepatic encephalopathy very low. |
| C | minor | `ground_truth.key_clinical_evidence` | "Thrombectomy benefit extends well beyond 24h" (false); DAWN/DEFUSE pearl for an anterior-circulation window; off-pathway and July-review lines. | FIXED: eight case-specific pearls. |
| C | minor | `ground_truth.red_herrings[1]` | DVT red herring pointed toward hypercoagulability work-up. | FIXED: PFO probably incidental, thrombophilia testing not needed acutely; new red herring for the 14:00 deterioration. |
| A | minor | `ground_truth.action_criteria`, `sequence_constraints`, `stop_rule`, `avoided_actions` | Order inverted (plan C1); label equals rationale; duplicated `[AHA_ASA_2019]`; hard template constraint; EEG rationale with em dash and a hedge. | FIXED: NCCT, labs, ECG, CTA, MRI (optional), drug check (recommended), echo (required), monitoring (required), literature (optional); soft constraints per plan 3.3; stop rule NCCT, labs, ECG, CTA, echo, monitoring, max 1; 2026 key on avoided actions. |
| E | minor | `metadata.case_body_concerns` | Ethanol differential concern. | FIXED in the differential; list emptied. |
| B | minor | `initial_tool_outputs.labs.abnormal_values_summary` | Interpretive labels "(acute intoxication)", "(macrocytosis)". | FIXED: "(elevated)". |

## Changes, in one paragraph a physician can read before re-reviewing

A 50-year-old woman with alcohol use disorder was found unrousable at 07:00 after going to bed at 23:00. She improved partially by 10:30 (she still could not walk and the nystagmus persisted), then deteriorated at 14:00. CTA now shows a mid-to-distal basilar occlusion with PC-ASPECTS 6 on source images (MRI DWI gives the same). The decision is explicit: last known well is 23:00 the previous evening, so no IV thrombolysis; thrombectomy proceeds (NIHSS 14, pre-stroke mRS 0, PC-ASPECTS 6, within 24 hours). The exam is consistent: GCS 13 (E3 V4 M6) and NIHSS 14, itemised. The HPI no longer announces the diagnosis, and the MRI no longer compares itself with an MRI that never happened. Thiamine is given before glucose, and the unresulted thiamine row is gone. The musts add swallowing and airway care, alcohol withdrawal monitoring with potassium and magnesium replacement, a cerebellar swelling watch, and secondary prevention once 24-hour imaging excludes haemorrhage. The PFO is called probably incidental (RoPE 4), with prolonged rhythm monitoring after discharge. The thrombophilia panel, the exclusion-studies scaffold and the secondary-prevention lab criterion are removed. Echo and Holter are required, and the Holter is now typed as the 48-hour study it is. The literature output cites ATTENTION and BAOCHE correctly (NEJM 2022) and is optional.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: the I63 category appends "lacunar stroke", "lacunar infarct" and "cardioembolic stroke" to this basilar occlusion case; a wrong mechanism would be credited.
- Citation keys `[AHA_ASA_Stroke_2026]`, `[AHA_ASA_2021_secondary]` (plan section 5.1).

## Open questions for Andrea (judgment calls you could not settle)

- PC-ASPECTS 6 is exactly at the EVT threshold. I set the value from the lesions already in the MRI and added a matching CTA source-image finding, so that the decision can be made without the optional MRI. The NCCT stays normal, which is plausible given posterior fossa beam hardening. A reviewer may prefer the NCCT to show subtle change as well.
- The left lateral medullary infarct lies in vertebral/PICA territory, outside a mid-basilar occlusion; I kept it as embolic debris through the dominant left vertebral artery and did not change the imaging.

## Verification
Adversarial check (23 October 2026). Read the log, the diff, the patient block, every tool output and the ground truth.
- Notes: all three ids present. 97a9f686 (thiamine row removed; thiamine-before-glucose must and prohibition), 55e9c9c7 (EVT must with NIHSS 14, mRS 0, PC-ASPECTS 6, §4.7.3), 19d1e303 (LKW 23:00 declared, no return to baseline, drug check names the window) are fixed as claimed.
- Recounted: NIHSS 14 (LOC 1, questions 2, commands 1, gaze 1 for isolated sixth nerve palsies per the NIHSS rule, face 1, arms 1 + 1, legs 1 + 1, ataxia 2, dysarthria 2); GCS 13 (E3 V4 M6) matches the text. PC-ASPECTS 6 (both cerebellar hemispheres 1 + 1, pons 2; medulla is not scored) is correct and agrees between CTA source images and DWI. RoPE 4 is correct. Hb/Hct and MCV/RBC arithmetic consistent.
- Found and fixed: (1) must [1] said LKW was "more than 15 hours" before the 14:00 deterioration; 23:00 to 14:00 is 15 hours: corrected. (2) Plan 1.2 requires every wake-up or unknown-onset case to address both extended-window limbs; she was found unrousable after sleep, and the case did not say why the extended window does not apply: must [1] now states she is a thrombectomy candidate and the decision falls about 11 hours after the sleep midpoint (03:00). (3) NCCT observations repeated grey-white preservation and qualified the posterior fossa line ("no cerebellar hypodensity with mass effect"), which read as hedged: merged and made categorical.
- Left as the worker's open question: a normal NCCT about 15 hours after LKW next to CTA source-image hypoattenuation and FLAIR-positive cerebellar infarcts is plausible (posterior fossa insensitivity, CTA-SI more sensitive) but a reviewer may prefer subtle CT change.
- `perfect_agent.py ISCH-STR-RP01 -v` passes; `case_io.py check` clean for the case.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The I63 category no longer appends mechanism labels ("embolic", "cardioembolic", "lacunar") or the bare label "stroke" (which matched "haemorrhagic stroke" or "stroke mimic"); mechanism labels and code families now sit on the specific codes.
- labels removed: "embolic stroke", "cardioembolic stroke", "lacunar stroke", "lacunar infarct", "stroke"
- codes removed: I63.4, I63.5, I63.3, I63.0, I63.1, I63.8, I63.81, I63.89
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

Decisions: `plans/ISCH-STR-decisions.md`.

- Echo output: added `echo_type` "TTE" to the stored echocardiogram report (the schema now keeps the field and the MockServer routes TTE/TEE/bubble orders by it; the value was only in `tool_parameters`).
- MRI: the left lateral medullary infarct removed from findings, DWI line, impression and the MRI criterion evidence (the medulla is not basilar territory; CTA shows patent vertebral arteries); PC-ASPECTS 6 unchanged. NCCT posterior fossa line now says no definite cerebellar hypodensity with cerebellum and brainstem limited by beam hardening (decision OQ8b).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
