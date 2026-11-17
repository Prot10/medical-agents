# MG-RM12

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-5-search-medical-literature (optional); removed initial literature_search outputs: myasthenia gravis diagnosis and management. Any literature query is now answered by the neutral library text.
- Synonyms (orchestrator, 17 Nov): G70.01 (with exacerbation) is no longer an accepted code in this stable case (diagnosis_synonyms.yaml G70.00 entry, MG CENTRAL C4); the code is a weight-0 component.

## Reviewer notes
Reviewer status: no note this round | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| (none) | - | MG-RM12 has no reviewer note in the November round; every change below is a class finding of the MG plan or my own. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | ground_truth.action_criteria[3] (action-2-order-specialized-test) | RNS required with positive AChR antibodies (class C2) | No tier change (plan D2: the conduction studies decide a GBS relapse); rationale now says why it stays required |
| C | minor | ground_truth.sequence_constraints[0..1], ground_truth.action_criteria[5] | "SFEMG is reserved for seronegative patients" (unsourced; class C3) | FIXED: canonical Q1 reasons (Jacob 2025); SFEMG criterion and follow-up after the core work-up |
| C | major | ground_truth.assessment.required_recommendations[0] | Pyridostigmine ceiling "about 360-480 mg/day" (class C6, D7) | FIXED: canonical M1 (baseline ECG; 360 mg/day maximum, review above 300) |
| C | major | ground_truth.assessment.required_recommendations[3], prohibited_recommendations[1] | Steroid must without a starting dose or schedule, citing Sanders 2016; outpatient "above 20 mg/day" prohibition in an admitted patient with bulbar weakness (class C4, D4, D5) | FIXED: canonical S2 inpatient titration (with the after-IVIG/PLEX schedule) plus the steroid-sparing clause; prohibition now P2 (Evoli 2019) |
| C | major | ground_truth.assessment.required_recommendations[4], key_clinical_evidence[5], action_criteria[4].rationale | Thymectomy justified by MGTX (class C5, D6, D24) | FIXED: canonical T1 at 42 with thymic hyperplasia (ICG 2020 rec 1a; Jacob 2025); KCE and rationale cite ICG 2020 and ABN |
| C | major | ground_truth.assessment.required_recommendations[2], action_criteria[0].rationale | ICU thresholds MIP -30 / MEP 40 from the GBS Lawn 2001 cohort (class C7, D8) | FIXED: canonical R1; rationale lists the ABN inpatient (FVC below 30 mL/kg, single-breath count below 25) and ICU criteria |
| C | major | ground_truth.assessment.required_recommendations[1] | IVIG 2 g/kg by actual weight without ventilatory failure (FVC 31.3 mL/kg) (class I1, D15) | FIXED: PLEX or IVIG 1 g/kg over 2-3 days by IBW (71.2 kg at 176 cm, about 71 g) after hepatitis B/C serology and IgG, read in the light of the IVIG given 4 weeks ago (passively transferred antibodies); second course after the GBS course kept |
| C | major | initial_tool_outputs.ecg, ground_truth.action_criteria[6] | No ECG before pyridostigmine (class C12) | FIXED: case fallback ECG promoted (rate set to the recorded 72/min); fallback ecg and metadata.fallback_tool_kinds.ecg removed; new recommended action-baseline-ecg |
| B | major | ground_truth.action_criteria[4], followup_outputs[2], fallback_tool_outputs.body_imaging | No mediastinum_MRI alternative; the hyperplasia MRI existed only as a case fallback (class C15, D17) | FIXED: alternative added; MRI stored as followup_outputs[2] request_mediastinum_mri; fallback cleared; CT orders checked unchanged; citations [Jacob_2025], [Narayanaswami_2021] |
| D | minor | ground_truth.avoided_actions[6..8], [2] | Unlabelled served reports: gait battery, levodopa challenge, speech-language battery; stored whole-body FDG-PET (class C9) | FIXED: three waste labels, reports moved to followup_outputs[4..6]; whole_body_FDG_PET added to the PET waste label |
| B | minor | followup_outputs[0].output.findings[0..4] | " L" low flag appended to FVC, supine FVC, MIP, MEP and single-breath count results | FIXED: removed |
| B | minor | initial_tool_outputs.specialized_test.findings[1] | RNS report said conduction velocities normal and peroneal latency 6.1 ms; the stored NCS/EMG (case fallback, same day) reports mild slowing (peroneal 38 m/s) and 6.4 ms | FIXED: RNS NCS line aligned to the NCS/EMG values |
| C | major | ground_truth.assessment.required_recommendations[6] | No screening before long-term immunosuppression (class C13) | FIXED: canonical S5, inpatient form |
| C | minor | ground_truth.assessment.required_recommendations[7] | Inpatient with bulbar symptoms (nasal speech, jaw fatigue) and no swallow assessment (ABN, per the reviewer's quotation in other MG notes; class C10) | FIXED: SLT swallowing assessment must; orderable criterion pending CENTRAL C1 |
| C | minor | ground_truth.assessment.required_recommendations[8] | No MG severity record (class G1) | FIXED: MGFA IIb (as labelled), baseline MG-ADL, QMG where available |

## Changes
MG-RM12 (42-year-old man, new AChR-positive generalized MG with thymic hyperplasia 4 weeks after a GBS admission; no reviewer note, class changes only). The work-up keeps RNS with repeat conduction studies as required (it is what excludes a GBS relapse), and its conduction values now agree with the stored NCS/EMG. Thymic imaging also accepts contrast mediastinal MRI, which returns a stored MRI of the hyperplasia. A baseline ECG (sinus rhythm 72/min) is a new recommended step. SFEMG comes after the core work-up and both sequence reasons follow ABN 2025. The gait battery, levodopa challenge and speech-language battery are labelled waste, and whole-body FDG-PET joins the PET waste label. The respiratory report no longer carries stray " L" flags. Management: pyridostigmine with a baseline ECG and the 360 mg/day maximum; plasma exchange or IVIG 1 g/kg by ideal body weight (about 71 g) after hepatitis serology and IgG, read with the recent IVIG in mind; monitored bed with twice-daily FVC and the ABN ICU criteria; prednisone started in hospital at 5-10 mg (from 10 mg after IVIG or plasma exchange) to 30 mg, with the inpatient prohibition replacing "above 20 mg/day"; thymectomy offered early once stable (ICG 2020, ABN) instead of the MGTX wording; screening before immunosuppression; SLT swallowing assessment; MGFA class and baseline MG-ADL recorded.

## Verification
Pass 1: 0 errors found
- No reviewer note (rulings file empty, correct). Checked the class changes: RNS kept required (D2, GBS relapse question) with an explicit reason; RNS NCS values now agree with the stored NCS/EMG (peroneal 6.4 ms, 38 m/s); mediastinal MRI of the hyperplasia consistent with the CT; IVIG 1 g/kg by IBW 50 + 0.9 x (176 - 152.4) = 71.2 kg, about 71 g, correct; single-breath count 19 in the stored report matches must 2; FVC 2.6 L / 83.0 kg = 31.3 mL/kg and 57% of 4.6 L; S2 + P2 inpatient steroid wording; T1 at 42; R1; ECG at the recorded 72/min; stop-rule ids all required; sequence ids exist; no em dashes in new text.
- Cosmetic (not counted): none.
Checks after verification: perfect_agent.py -v pass; case_io.py check: no failure names this case; test_case_guards -k this id pass.
Pass 2: 0 errors found
- No change after the last zero-error pass (Pass 1 made no edit; no condition-audit or orchestrator entry), so nothing to re-verify.
- Checks: perfect_agent.py -v pass; test_case_guards -k (six MG cases) 48 passed.
Pass 3: 0 errors found
- No change after the last zero-error pass (no condition-audit or orchestrator entry), nothing to re-verify.
- Checks: perfect_agent.py -v ok; test_case_guards.py -k (the eight pass-3 ids) 64 passed.
