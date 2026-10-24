# ISCH-STR-P04
Reviewer status: R1 none, R2 in_progress | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 132ec224-5224-4bc8-9fa3-04d82c292e25 | FIXED | `followup_outputs` reordered: CTA, CT perfusion, TTE, 48-hour Holter, apixaban check, literature. `action_criteria` in the same order (NCCT, labs, ECG, CTA, MRI optional, CTP, TTE, monitoring, drug check, literature). Soft constraints NCCT before CTA, CTA before CTP, CTA before echo and monitoring, monitoring before the anticoagulant check. The Holter report opens "Recorded on the stroke unit after admission, 48 hours." |
| 6d879e51-c6a6-4300-bed5-7f328173be9b | FIXED | Decision must (`required_recommendations[5]`), prohibition 0, key evidence item 3 and pearl 3 state the gate: the perfusion IVT limb (EXTEND, within 9 hours of the sleep midpoint, about 03:05) applies only to patients not eligible for thrombectomy, and she is eligible; the DWI-FLAIR limb is closed (FLAIR-positive) and its MRI must not delay thrombectomy. |
| db9768a7-2e38-4c21-99df-f5410eb9763c | FIXED | Note text is truncated at source after "CONTRAINDICATED sets a fl"; treated, as the plan says, as the BP floor. EVT must (`required_recommendations[6]`): BP at or below 185/110 mmHg before thrombectomy (192/104 on arrival, IV labetalol or nicardipine), systolic not targeted below 140 mmHg after successful recanalization. The thrombolysis-only BP must and the prohibition "Do NOT aggressively lower blood pressure below 140-150 mmHg systolic" were removed (plan C5: EVT case, the C4 BP must governs). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | Last two sentences gave the team's verdict ("Standard IV tPA is not administered ... definitively outside the 4.5-hour window") and listed the ordered NCCT, CTA and CTP. | FIXED: both sentences removed (plan C10); the times stay. |
| C | major | `patient.neurological_exam.additional`, `mental_status` | NIHSS 20 not derivable. Recount: LOC questions 1, gaze 2, visual 2, face 1 (flattened nasolabial fold = minor), left arm 4, left leg 3 (trace hip flexion), sensory 2, extinction 2 = 17. "Oriented to person and place" left item 1b undefined. | FIXED: itemised NIHSS 17; mental status states month incorrect, age correct. 17 repeated in LKW must, EVT must, key evidence, difficulty text. EVT thresholds still met (NIHSS 10 or more). |
| B | minor | `patient.neurological_exam.additional` | LKW to arrival "approximately 8 hours" (23:00 to 07:40 is 8 h 40 min); no pre-stroke mRS although thrombectomy requires it. | FIXED: "8 hours 40 minutes"; "Pre-stroke modified Rankin Scale 0 (fully independent)" added (history: ambulating normally at baseline). |
| B | minor | `patient.neurological_exam.reflexes` | "hyporeflexic acutely (2+)" (2+ is normal). | FIXED: "1+ (hyporeflexic acutely)". |
| B | major | `initial_tool_outputs.ct.findings[1]`, `.impression` | ASPECTS 7 with points deducted for only two regions (insula, lentiform = 8); frontoparietal grey-white loss contradicted the MRI and CTP (cortex spared, core confined to lentiform and posterior insula); impression item 4 "no significant established infarct core" contradicted item 3. | FIXED: cortical change removed, ASPECTS 8; impression renumbered with the small vessel change. |
| D | minor | `initial_tool_outputs.mri` | Teaching text ("indicating lesion age greater than 4.5-6 hours", "large surrounding penumbra", "cortical penumbra remains viable": DWI cannot show penumbra). | FIXED: FLAIR "matching the DWI lesion (no DWI-FLAIR mismatch)"; cortical finding renamed "without diffusion restriction"; numbered impression. |
| D | minor | CTP follow-up `findings[2]` | "Core volume 18 mL is well below the 70 mL threshold used in extended-window selection criteria" (selection reasoning in a report). | FIXED: metric only. |
| A | major | Holter follow-up, criterion `action-11` | 48-hour recording labelled `holter_24h`; heart-rate range without min/max. | FIXED: `monitor_type` holter_48h; range 54-116, average 76; criterion alternatives holter_48h, holter_24h, telemetry; impression gives burden and episodes. |
| C | major | drug-check follow-up and `action-9` | Alteplase/thrombectomy checklist for a patient who receives no IVT; "metformin should be held for 48 hours" after contrast (not required with normal eGFR); "up to 5%" angioedema figure. | FIXED: recommended (plan C7), `drug: apixaban`, placed after monitoring: interactions with atorvastatin, amlodipine, lisinopril, metformin, glipizide; full-dose criteria; no antiplatelet; sulfonamide allergy irrelevant; metformin need not be withheld with normal eGFR. |
| C | major | `ground_truth.assessment.required_recommendations` | No anticoagulation must despite AF; must named carotid duplex (no criterion; CTA covered the neck); the 1.8/15 mL thresholds attached to tissue selection without the EVT gate; no hyperglycaemia management. | FIXED: LKW/NIHSS, NCCT, glucose with treatment to 140-180 mg/dL, CTA, CTP (DEFUSE 3 thresholds correctly for thrombectomy), decision, EVT with BP, stroke unit telemetry, apixaban 5 mg twice daily (CHA2DS2-VASc 6, HAS-BLED 2) within 48 hours for a moderate final infarct or day 6-7 if major, no heparin bridge, atorvastatin 80 mg (LDL 118, diabetes, carotid and aortic plaque), long-term BP and diabetes targets. Carotid duplex must removed. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Two overlapping anchoring prohibitions; "no tPA before NCCT" in a no-IVT case; "do not skip perfusion imaging" overstated. | FIXED: four prohibitions (no IVT with reasons; do not declare her ineligible for all reperfusion; do not skip CTA; do not delay thrombectomy for MRI). |
| A | major | criteria tiers | CTP optional while it selects the treatment; literature recommended; separate lipid/HbA1c criterion (already in admission bloods, plan C9). | FIXED: CTP required; literature optional and last; `action-6-interpret-labs` removed. |
| C | minor | `ground_truth.differential` | Large-artery atherosclerosis "moderate", cryptogenic "low", Todd's "low" after CTA and Holter settled the mechanism. | FIXED: low, very low, very low with case data. |
| E | minor | `ground_truth.key_clinical_evidence` | Template and "Tier per the July 2026 clinical review" lines. | FIXED: rebuilt, with the C3 canonical wake-up sentence. |
| B | minor | literature follow-up | DAWN thresholds garbled; the 2019 AHA line misquoted 6-24 h as Class I. | FIXED: DAWN groups stated correctly; DEFUSE 3; WAKE-UP (excluded thrombectomy candidates); no case verdict. |
| B | minor | echo follow-up | No `echo_type`; impression unnumbered. | FIXED: `echo_type` TTE in output and `tool_parameters`, trigger `request_tte_echocardiogram`; numbered impression. |
| E | minor | `metadata.case_body_concerns`, `difficulty_rationale`, `difficulty_description` | Stale mock-server note (perfusion_MRI trigger that does not exist); rationale listed literature, drug check, MRI and carotid duplex as required. | FIXED: concerns emptied; descriptions aligned. |
| A | minor | citations | Free-text guideline string, duplicate `[AHA_ASA_2019]`, `[AHA_ASA_2014]`, `[DAWN_2018]` twice. | FIXED: one key per source. |
| C | minor | `labs.abnormal_values_summary` | Interpretive text ("stress hyperglycemia vs inadequate control"). | FIXED: factual list. |

## Changes, in one paragraph a physician can read before re-reviewing

The pathway now reads NCCT, labs, ECG, CTA and CT perfusion first (all required), then TTE and 48-hour Holter (required), the apixaban check (recommended), MRI optional and literature optional last; the HPI no longer states the treatment verdict or the imaging orders. NIHSS is 17 (itemised), pre-stroke mRS 0 is recorded, and the NCCT reads ASPECTS 8 with the cortical change removed to match MRI and CTP. The musts state the decision: no IV thrombolysis (beyond 4.5 hours, FLAIR-positive, and the perfusion limb applies only to thrombectomy-ineligible patients) and thrombectomy for the right M1 occlusion (core 18 mL, mismatch 100 mL, ratio 6.6, about 9 hours, DEFUSE 3 and DAWN met), with BP at or below 185/110 before and systolic not driven below 140 after recanalization. AF found on the 48-hour Holter now leads to apixaban 5 mg twice daily with ELAN timing, plus atorvastatin 80 mg, glucose 140-180 mg/dL and long-term risk-factor targets. The 140-150 systolic floor and the carotid duplex must are gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[AHA_ASA_Stroke_2026]`, `[AHA_ASA_2021_secondary]` per plan section 1.1.
- `condition_tool_guidance.yaml`: CTP is required here although the July answers made it optional (plan section 5.7 notes this departure).
- `accepted[0]` contains an em dash and "extended-window thrombectomy candidate by DAWN/DEFUSE-3 perfusion criteria"; it is still accurate and was left unchanged (label policy).

## Open questions for Andrea (judgment calls you could not settle)

- NIHSS facial palsy scored 1 because the exam says "flattening of the nasolabial fold" (the NIHSS example of minor paralysis). If R2 reads the droop as partial paralysis (2), the total is 18; no decision changes.
- The ELAN timing in the anticoagulation must depends on the final infarct after thrombectomy, which the case does not show; the must gives both branches.

## Verification

Adversarial verifier, 23 October 2026. Checked: follow-up and criterion order (CTA and CTP before echo and Holter), the Holter timing (episodes on night 1 and day 2 after admission, burden 30 min of 48 h), the sleep midpoint (23:00 to 07:10 gives 03:05, 4 h 35 min before the 07:40 arrival) and both IVT limbs, the EVT and pre-EVT BP musts, the removal of the 140 floor; NIHSS 17 recount (LOC questions 1, gaze 2, visual 2, face 1, arm 4, leg 3, sensory 2, extinction 2); DAWN and DEFUSE 3 thresholds and trial figures in the literature output; ASPECTS 8 against the CT, CTP and MRI core locations; CHA2DS2-VASc 6; apixaban dose criteria; ELAN timing for a deep MCA infarct over 1.5 cm (moderate); lab arithmetic.

Found and changed:
- `ground_truth.differential[5].key_features` still described a "focal cortical-subcortical infarct on DWI" after the worker had made the infarct deep (lentiform nucleus and posterior insula, cortex spared). Now "the right M1 occlusion and the focal right MCA infarct on imaging exclude a metabolic cause."

No other error found. `perfect_agent.py ISCH-STR-P04 -v` passes; `case_io.py check` clean for the case.

## Condition audit
Condition auditor, 23 October 2026 (cross-case uniformity pass over all 30 ISCH-STR cases).
- Literature criterion: `required_arguments` was the exact query string "extended window thrombectomy and thrombolysis selection in wake-up stroke", which no free-text agent query can equal; now {} as in the other cases (optional tier unchanged). Both checks clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The I63 category no longer appends mechanism labels ("embolic", "cardioembolic", "lacunar") or the bare label "stroke" (which matched "haemorrhagic stroke" or "stroke mimic"); mechanism labels and code families now sit on the specific codes.
- labels removed: "embolic stroke", "cardioembolic stroke", "lacunar stroke", "lacunar infarct", "stroke"
- codes removed: I63.4, I63.3, I63.2, I63.0, I63.1, I63.8, I63.81, I63.89
- codes added: I63.51
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
