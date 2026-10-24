# SYNC-CARD-S01
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search` | Finding and summary equal to the literature criterion's expected_evidence (leak guard failure). | FIXED: deleted; one ESC 2021 / ESC 2018 guideline follow-up added last in `followup_outputs`. |
| E | major | `fallback_tool_outputs.literature_search`, `fallback_tool_outputs.drug_interactions.general` | "No directly applicable ... evidence" text; "(agent not specified on this case's pathway)". | FIXED: literature fallback deleted (library answers); drug fallback replaced by a `medication_list_review`. |
| C | major | `action-6-search-medical-literature` | Literature recommended. | FIXED: optional, canonical rationale. |
| C | major | `initial_tool_outputs.drug_interactions`, `action-5-check-drug-interactions` | Initial block listed the medications with no review; criterion named no drug. | FIXED: initial block deleted; alternative `{drug: metoprolol}`; follow-up `check_metoprolol` and fallback carry the review (metoprolol slows AV conduction; apixaban plus aspirin bleeding; apixaban dose check; no bridging; metformin and eGFR). |
| C | minor | `action-2-interpret-labs` | Pinned CBC, BMP, Mg and troponin. | FIXED: recommended, `panels: [BMP]` (plan C); expected_evidence states K 4.4, creatinine 1.3, troponin not elevated. |
| B | major | `initial_tool_outputs.labs.panels.BMP` | Na 135, Cl 91, CO2 22: anion gap 22 with nothing to explain it. | FIXED: Na 137, Cl 101, CO2 24 (gap 12), all normal; summary and interpretation updated. |
| B | minor | `initial_tool_outputs.labs.panels.CBC` | Hct 38.1% with Hb 13.9 g/dL. | FIXED: Hct 41.6%. |
| B | minor | `initial_tool_outputs.labs.panels.Cardiac_markers` | Troponin I 0.04 against a reference "<0.04" flagged abnormal with "warrants serial testing", an ambiguity no criterion resolves. | FIXED: 0.02 ng/mL, not elevated (ischaemic cause excluded consistently with the ECG and differential). |
| B | minor | `patient.vitals.hr` | HR 45 while the ECG escape is 35 bpm and telemetry never exceeds 42 bpm. | FIXED: 36. |
| D | minor | `initial_tool_outputs.ecg` | "(likely rate-related or ischemic)", "(borderline prolonged)", "(widened, consistent with ventricular escape)" interpretive annotations. | FIXED: findings only. |
| C | major | `followup_outputs` CT, new `action-9-order-ct-scan` | He is 70, lost consciousness, struck his forehead (laceration, subgaleal swelling) and takes apixaban: NICE NG232 indicates a head CT within 8 h. The red herring called the head CT reflexive and the plan lists head CT as avoided. | FIXED: recommended criterion; CT report moved to `initial_tool_outputs.ct` and reworded (no fracture, subgaleal swelling); red herring replaced. See Open questions. |
| B | major | `followup_outputs[0]` (echo) | Wall motion null while the CMR shows mid-anterior hypokinesis after an LAD PCI; LVEDD 5.4 cm called dilated (normal for a man); no echo_type, TAPSE, PASP, gradients. | FIXED: full TTE report (LVEF 45% biplane, mid-anterior hypokinesis, septum 1.2 / PW 1.1 cm, LAVI 38, AV sclerosis Vmax 1.7 m/s, TAPSE 21 mm, PASP 34 mmHg), no diagnosis sentence. |
| B | major | `followup_outputs[1]`, `action-4-order-cardiac-monitoring` | 24 h Holter under a criterion labelled "continuous inpatient telemetry" pinned to holter_24h; no symptom-rhythm correlation. | FIXED: alternatives telemetry, holter_24h, holter_48h; output "Inpatient telemetry, 24 h" with the same rates (28-42, average 36, 4.2 s pause at 03:42 in sleep) plus two seated lightheaded episodes at 30-32 bpm; same recording as `fallback_tool_outputs.cardiac_monitoring`. |
| D | minor | `followup_outputs` CMR | "No features of ARVC, sarcoidosis, or infiltrative cardiomyopathy" exclusion sentence over a septal mid-wall LGE; anatomical interpretation of the His bundle. | FIXED: findings-only impression (mid-anterior subendocardial scar; small insertion-point mid-wall enhancement); CMR optional (age 70). |
| C | minor | `followup_outputs` tilt and exercise | Tilt and Bruce test performed in persistent complete heart block (plan J, M). | FIXED: both follow-ups deleted; both avoided as waste. |
| D | minor | `followup_outputs` brain MRI | "age-appropriate" wording only; off-pathway. | FIXED: wording; kept as off-pathway report. |
| H | minor | all `action_criteria[*]` | Free-text "ESC 2018 §x" and "Locati 2014" citations; rationale equal to label. | FIXED: keys only; real rationales. |
| A | minor | `stop_rule`, `sequence_constraints` | `max_additional_actions: 0`; no constraints. | FIXED: 2; soft ECG before TTE and before monitoring. |
| C | major | `avoided_actions` | Only CSF avoided. | FIXED: CSF, EEG, brain MRI, tilt and exercise as waste, each naming the diagnosis. |
| C | major | `ground_truth.assessment` | "Cardiology / EP consult" as a must; no pacing must; no handling of the beta-blocker, apixaban plus aspirin, or LVEF 45%; duplicated driving prohibition. | FIXED: musts are diagnosis, monitored bed with pacing pads and temporary pacing if unstable, permanent pacemaker this admission with the pacing mode chosen for LVEF 45%, hold metoprolol without delaying pacing, peri-procedural apixaban without bridging and review of aspirin (ESC 2024 AF), driving. Prohibitions: AV-nodal drugs before pacing, discharge before pacing, delaying pacing, heparin bridging. |
| C | major | `ground_truth.differential` | VT moderate after a work-up that excludes it; "EP study" cited though not on the pathway; beta-blocker-induced block not discussed. | FIXED: VT low (telemetry, LVEF); all entries cite pathway results; beta-blocker-induced AV block added as low. |
| L | minor | `ground_truth.red_herrings` | "Past palpitations attributed to anxiety" is not in the case; head-CT red herring now wrong. | FIXED: palpitation red herring quotes the HPI; metoprolol and the V4-V6 ST depression added. |
| C | minor | `ground_truth.key_clinical_evidence`, `metadata` | "Holter and EP study are confirmatory"; difficulty rationale and pearls. | FIXED: rewritten; `fallback_tool_kinds` updated. |

## Changes, in one paragraph a physician can read before re-reviewing

The 70-year-old man with prior LAD PCI, paroxysmal AF on metoprolol, apixaban and aspirin collapsed while seated and struck his forehead. Required steps are the ECG (complete AV block, wide escape at 35 bpm with RBBB morphology and left axis), the TTE (LVEF 45% with mild mid-anterior hypokinesis, no valve disease) and inpatient telemetry (Holter accepted: persistent complete block, escape 28-42 bpm, lightheadedness at 30-32 bpm, a 4.2 s pause in sleep, no VT). Recommended: BMP (normal potassium, corrected anion gap, troponin not elevated), a head CT within 8 hours (age over 65, loss of consciousness, anticoagulant; NICE NG232) and a medication review naming metoprolol. CMR and the guideline lookup are optional; EEG, brain MRI, CSF, tilt and exercise are waste, and the tilt and exercise reports were removed. Musts: diagnosis, monitored bed with pacing pads, permanent pacemaker this admission with the pacing mode chosen for LVEF 45%, hold metoprolol without delaying pacing, apixaban without heparin bridging and review of the aspirin, driving advice.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: generic synonyms ("cardiac syncope", "bradyarrhythmia" ...) and R55 still accepted; not hand-edited.
- Plan C3: an off-pathway tilt order now gets the library's normal tilt (HR 68), which contradicts persistent complete heart block. The plan deleted the case's tilt report; a library "no study stored" answer would fix this.
- Plan (lead): section 3 lists head CT as avoided for S01, but the case meets the plan's own NG232 rule twice (age 65 or over with loss of consciousness; anticoagulated). M03's worker made the same deviation.

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. Deviations from the lead plan, decided for dataset quality:
- Head CT recommended instead of avoided (NICE NG232, as above).
- Troponin set below the 99th percentile instead of exactly at it, so the case does not leave an unresolved ACS question that no criterion addresses.
