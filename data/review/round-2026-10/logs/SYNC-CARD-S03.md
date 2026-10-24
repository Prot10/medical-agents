# SYNC-CARD-S03
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search`, `initial_tool_outputs.drug_interactions.general` | Literature finding and summary equal to the expected_evidence (leak guard failure); drug block was the drug criterion's key ("Hold AV-nodal blockers and review AAD; check digoxin level"); she takes no antiarrhythmic or digoxin. | FIXED: both deleted; one ESC 2021 pacing guideline follow-up added last. |
| E | major | `fallback_tool_outputs.literature_search`, `fallback_tool_outputs.drug_interactions.general` | "No directly applicable ... evidence"; "(agent not specified on this case's pathway)". | FIXED: literature fallback deleted; drug fallback is a `medication_list_review` (carvedilol recently doubled; metformin contraindicated at eGFR below 30; spironolactone with lisinopril; warfarin with allopurinol; uninterrupted warfarin at implant). |
| C | major | `action-5-check-drug-interactions`, `action-6-search-medical-literature` | Drug criterion with no drug; literature recommended. | FIXED: drug recommended with `{drug: carvedilol}` and its follow-up; literature optional (canonical rationale). |
| C | minor | `action-2-interpret-labs` | Pinned CBC, BMP, Mg, troponin; generic expected_evidence. | FIXED: recommended `panels: [BMP]`; expected_evidence Na 128, K 5.0, creatinine 2.0 (eGFR about 27, CKD-EPI 2021). |
| D | minor | `initial_tool_outputs.labs.interpretation` | "acute-on-chronic kidney injury above baseline", "metabolic acidosis/hypervolaemic pattern": interpretation using history the lab cannot know. | FIXED: values and eGFR only. CK-MB 5.2 set to 3.8 (normal) so the mild troponin rise reads as chronic injury, as the differential states. |
| B | minor | `patient.vitals.hr` | HR 45 while the ECG escape is 32 bpm. | FIXED: 32. |
| D | minor | `initial_tool_outputs.ecg` | "concerning for increased arrhythmic risk", "(likely demand ischemia secondary to bradycardia)"; right axis +120 with an LBBB-morphology escape. | FIXED: interpretive clauses removed; axis -40. |
| C | major | `followup_outputs` CT, new `action-9-order-ct-scan` | She is 66, lost consciousness, struck her right parietal scalp (contusion on exam) and takes warfarin with INR 2.5: NICE NG232 indicates a head CT within 8 h, and the case's own pearl says so. The plan lists head CT as avoided. | FIXED: recommended criterion; CT report moved to `initial_tool_outputs.ct`; the management phrase "requiring emergency neurosurgical intervention" removed. See Open questions. |
| B | major | `followup_outputs[0]` (echo) | Wall motion null while the CMR shows anterior and apical akinesis after CABG; lab-style fields; expected_evidence about LA appendage thrombus "if cardioversion considered" (TTE cannot exclude it, and no cardioversion is planned). | FIXED: full TTE report (LVEF 35% biplane, anterior and apical akinesis, inferior hypokinesis, no apical thrombus, moderate AS Vmax 2.8 m/s AVA 1.3 cm2, moderate MR, LAVI 48, TAPSE 15 mm, PASP 48 mmHg); expected_evidence rewritten. |
| B | major | `followup_outputs[1]`, `action-4-order-cardiac-monitoring` | 24 h Holter under a telemetry label pinned to holter_24h; the 02:18 / 5.8 s pause identical to S02 (template carry-over); "approximately 2% burden" for 342 PVCs at about 31 bpm (0.8%). | FIXED: alternatives telemetry, holter_24h, holter_48h; "Inpatient telemetry, 24 h" with S03's own numbers (average 31, range 25-38, 4.6 s pause at 04:05, symptomatic pauses 3.4 s and 4.1 s), PVC burden 0.8%; same recording as the fallback. |
| C | minor | `followup_outputs` tilt and exercise | Tilt and a Bruce test performed in complete heart block with LVEF 35% (plan J, M). | FIXED: both follow-ups deleted; both avoided as waste. |
| C | minor | `followup_outputs` CMR | Volumes labelled "significantly increased"; otherwise consistent (EF 35% from 215/140 mL). | FIXED: labels; CMR optional (age 66). |
| H | minor | all `action_criteria[*]` | "ESC 2018 §x", "Locati 2014" citations; rationale equal to label. | FIXED. |
| A | minor | `stop_rule`, `sequence_constraints` | `max_additional_actions: 0`; no constraints. | FIXED: 2; soft ECG before TTE and before monitoring. |
| C | major | `avoided_actions` | Only CSF avoided. | FIXED: CSF, EEG, brain MRI, tilt, exercise as waste, each naming the diagnosis. |
| C | major | `ground_truth.assessment` | "EP consult (likely CRT-D)" as a must; "review AAD" for a drug she does not take; no handling of carvedilol after pacing, metformin at eGFR 27, or warfarin with a head strike. | FIXED: musts are diagnosis, monitored bed with pads and defibrillation, CRT-D this admission (ESC 2021), hold carvedilol and resume it after pacing as HF therapy, uninterrupted warfarin once CT excludes haemorrhage, stop metformin and review spironolactone, driving. Prohibitions: AV-nodal drugs before pacing, heparin bridging, RV pacing alone, discharge before the device. |
| C | major | `ground_truth.differential` | VT high and ACS and drug-induced block moderate after a work-up that excludes them; SSS cited SNRT and EP study (not on the pathway). | FIXED: VT, drug-induced block and ACS low with the pathway evidence; SSS replaced by flutter with rapid conduction (very low, none conducted); vasovagal very low. |
| L | minor | `ground_truth.red_herrings` | data_points not quoted from the field. | FIXED: quoted; carvedilol dose increase added. |
| E | minor | `metadata.clinical_pearls`, `difficulty_rationale` | Lev disease attributed to calcific AS; CT pearl not tied to NG232. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The 66-year-old woman with ischaemic cardiomyopathy after CABG and chronic atrial flutter on carvedilol (recently doubled) and warfarin collapsed and struck her head. Required: ECG (complete AV block under flutter, wide LBBB-morphology escape at 32 bpm), TTE (LVEF 35% with anterior and apical akinesis, moderate AS and MR) and inpatient telemetry (Holter accepted: escape 25-38 bpm, symptomatic pauses of 3.4 and 4.1 s, only non-sustained VT); telemetry numbers are now her own, not S02's. Recommended: BMP (Na 128, K 5.0, creatinine 2.0, eGFR about 27), a head CT within 8 hours (warfarin, age over 65, loss of consciousness; NICE NG232) and a medication review naming carvedilol. CMR and the guideline lookup are optional; CSF, EEG, brain MRI, tilt and exercise are waste, and their stored tilt and exercise reports were removed. Musts: diagnosis, monitored bed with pads and defibrillation, CRT-D this admission, hold carvedilol and resume it after pacing, uninterrupted warfarin once the CT excludes haemorrhage, stop metformin and review spironolactone, driving advice.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: generic synonyms and R55 still accepted; not hand-edited.
- Plan C3: an off-pathway exercise order now receives the library's "Normal exercise stress test with good functional capacity", and a tilt order a normal tilt at HR 68, both contradicting persistent complete heart block with LVEF 35%. The case's own reports were deleted per plan M; a library "no study stored" answer is needed.
- Plan (lead): section 3 lists head CT as avoided for S03, but the case meets the plan's own NG232 rule twice (age 65 or over with loss of consciousness; anticoagulated).

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea. Deviations from the lead plan, decided for dataset quality: head CT recommended instead of avoided (NICE NG232); metformin and spironolactone added to the musts because her eGFR is about 27.

## Verification

Adversarial verifier, 24 Oct 2026. No reviewer notes exist for SYNC-CARD. Read the full final case against the log and plan.
- Checked: eGFR about 27 (CKD-EPI 2021, female, 66, creatinine 2.0: recomputed 27); anion gap 16; echo LVEF 35% vs CMR 215/140 mL (35%); telemetry numbers distinct from S02; CRT-D, uninterrupted warfarin after CT, metformin stop and spironolactone review against the drug output; head CT recommended (NG232: warfarin, 66, loss of consciousness, parietal strike) consistent across HPI, exam and CT; red-herring quotes present in the ECG interpretation and HPI; leak guard passes.
- Found and changed:
  - CBC and creatinine used male reference ranges in a woman (Hb 13.5-17.5, Hct 38.3-48.6, creatinine 0.7-1.3). Set to 12.0-16.0, 36.0-46.0 and 0.6-1.1; all flags unchanged (Hb 10.9, Hct 34.2 and creatinine 2.0 remain abnormal).
  - Echo aortic valve graded "moderate stenosis" with Vmax 2.8 m/s and mean gradient 18 mmHg, which are mild-range values (ESC/EACTS 2021 / EACVI-ASE: moderate is Vmax 3.0-3.9 m/s, mean 20-39 mmHg) while AVA 1.3 cm2 is moderate. Made the grading concordant: Vmax 3.1 m/s, peak 38 mmHg (4v2), mean 22 mmHg, AVA unchanged, in the valve field and the impression.
  - Family history "Father died suddenly at age 58, presumed cardiac death" was S02's line copied (template carry-over), and together with "Brother with dilated cardiomyopathy and ICD" it raised a familial (lamin A/C) cardiomyopathy with conduction disease that the case never addressed (no differential entry, no genetic must), next to a CMR showing septal mid-wall enhancement. Replaced the two lines with "Father died of a myocardial infarction at age 70" and "Brother with coronary artery disease, coronary bypass surgery at age 64"; mother and paternal uncle lines kept. No other field referred to them.
  - Head-CT criterion `action-9-order-ct-scan` cited [ESC_2018]; set to [] (NICE NG232 named in the rationale).
- perfect_agent -v and case_io check clean after the changes.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).
- Drug follow-ups and the fallback medication review: removed, where present, wording that asserted results the agent has not obtained ("while AV conduction disease is unpaced", "meets the labelled dose", device-implantation warnings, the eGFR-specific metformin line, cefazolin "for device implantation"). Each is now a conditional rule (e.g. contraindicated in second- or third-degree AV block without a pacemaker; apixaban 5 mg unless two of age 80 or over, weight 60 kg or less, creatinine 1.5 mg/dL or more; anticoagulation advice if a device is implanted). Why: a drug check must not disclose the conduction diagnosis or the management decision.
- `initial_tool_outputs.drug_interactions` set to the medication-list review (copy of the fallback). Why: without it, tier 2 answered an unrelated drug (probe: ibuprofen) with the first per-drug follow-up.
- Added "not performed" follow-ups for `tilt_table` and `exercise_stress_test` (RM04/RP02 format, "Deferred by the clinical team"). Why: otherwise the library returned a normal tilt (HR 68) or a normal exercise test (10.4 METs) in a patient with high-grade AV block, contradicting the case; both orders stay penalised as in the plan.

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: complete heart block labels only (Mobitz II and second-degree labels removed: a different grade); I44.30 kept, I44.1, I44.39, I45.9 and R55 dropped.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-9-order-ct-scan citations [] -> ['[NICE_NG232]']; action-3-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2021_Pacing]']; action-8-order-advanced-imaging citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]']; action-5-check-drug-interactions citations ['[ESC_2018]'] -> ['[ESC_2021_Pacing]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-S03` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure 'Active stand test not performed. Deferred by the clinical team.' (haemodynamically unstable or high-grade AV block at presentation: standing is not safe); no criterion |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.

| field path | change |
| --- | --- |
| `followup_outputs[8]` (`request_electrophysiology_study`) | added: 'Electrophysiology study not performed. Deferred by the clinical team.' The documented rhythm already settles management, and the library's normal study (normal AV conduction and sinus node function, nothing inducible) would contradict the case; no criterion |

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
