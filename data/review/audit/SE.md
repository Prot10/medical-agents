# NeuroBench v5 audit — SE (status epilepticus)

Auditor: condition-audit pass. Scope: all 30 `SE-*` case files (M01–M09, P01–P08, S01–S12,
RS11), read field-by-field against `dataset-generation/criteria_packs/SE.md` and
`dataset-generation/TOOL_REPORT_STYLE_GUIDE.md`.

Mechanical gates (whole set): coherence validator **0 issues** on all 30; schema validation
**passes** on all 30; tool-vocab check passes (516/516 dataset-wide). Leakage detector raised
candidates on M01–M07, P03, P05, P07, S09, S10 — each judged individually; all are KEPT Kind-2
(EEG naming electrographic NCSE/status per the criteria pack; CSF organism/antibody confirmatory;
population-keyed literature). Per task brief these were NOT chased to zero.

## Findings

| case_id | dim | severity | region.field path | finding | action | detail |
|---|---|---|---|---|---|---|
| SE-M05 | D | minor | initial_tool_outputs.eeg.findings[0].morphology | EEG finding morphology said extreme delta brush "— highly specific for anti-NMDAR encephalitis"; EEG cannot name the antibody disease (style guide: strip disease names from EEG) | FIXED | Removed the disease-naming clause; kept the morphologic description. EEG impression was already clean. |
| SE-M08 | B | minor | followup_outputs[0].output.impression | MRI impression states rCBV "ratio 0.8" but the structured finding and differential_by_imaging both state 0.6 | FIXED | Corrected impression 0.8 → 0.6 to match the two concordant fields; qualitative "low rCBV" read unchanged |
| SE-P08 | A/B | major | followup_outputs[0].output.classification | EEG `classification:"normal"` but impression says "This is an ABNORMAL EEG" with diffuse theta slowing/post-ictal recovery | FIXED | Set classification → "abnormal"; the enum contradicted its own impression+findings |
| SE-S01 | D | minor | initial_tool_outputs.ct.additional_observations[0] | CT report asserted "SE due to medication non-adherence and alcohol" — cross-modality etiology a CT cannot determine | FIXED | Stripped the etiology line; kept within-CT "No structural cause of SE identified" (also in the clean impression) |
| SE-S03 | D | minor | initial_tool_outputs.ct.additional_observations[1] | CT report asserted "No new acute lesion - SE from metabolic precipitant (hyponatremia, UTI)" | FIXED | Trimmed to "No new acute lesion"; kept "Old right MCA stroke - known epileptogenic substrate" (within-CT chronic finding) |
| SE-S10 | D | minor | initial_tool_outputs.ct.additional_observations | CT report asserted "SE from toxicologic cause" and named "TCA + MDMA combination toxidrome" (cross-modality; references tox screen) | FIXED | Emptied additional_observations; the clean impression carries the within-CT read |
| SE-M02 | C | major | ground_truth (differential[0], red_herrings[1], optimal_actions[2].expected_finding) | GT repeatedly calls levetiracetam level "subtherapeutic" and builds a red herring on it, but the actual lab is LEV 24 mcg/mL (ref 12-46), `is_abnormal:false` — i.e. THERAPEUTIC. The "subtherapeutic AED" distractor premise is contradicted by the case data | FLAGGED | Cannot resolve without choosing whether the lab value or the GT narrative is correct (changing either alters meaning). Human must reconcile |
| SE-P05 | C | major | patient (mydriasis 7mm) vs ground_truth.key_reasoning_points (DUMBELS "miosis") | Case presents persistent mydriasis (attributed to central nicotinic effect) while the reasoning mnemonic lists miosis as the expected cholinergic sign; OP poisoning classically causes miosis | FLAGGED | Clinical-plausibility call. May be intentionally atypical (puzzle), but the presentation/reasoning mismatch needs a clinician's adjudication; do not change presentation |
| SE-M01 | B | minor | ground_truth.optimal_actions[7].tool_parameters | Step 7 action+output = "CT chest/abdomen/pelvis with contrast" for SCLC search, but tool_parameters `modality:"FDG_PET"` (a brain/metabolic study, not body CT) | FLAGGED | tool_parameters changes scoring semantics; vocab has no clean "body CT" option. Flag-don't-fix |
| SE-M05 | B | minor | ground_truth.optimal_actions[6].tool_parameters | Step 7 action+output = "Pelvic MRI" for ovarian teratoma, but tool_parameters `modality:"MR_angiography"` (a vascular study) | FLAGGED | Wrong modality for the stated purpose; vocab lacks a pelvic-MRI option. Affects scoring; flag-don't-fix |
| SE-P04 | B | minor | case_id prefix vs ground_truth.primary_diagnosis/icd_code | SE-prefixed case has primary_diagnosis = acute MCA ischemic stroke with IIC LPDs (ICD I63.512), not frank SE | FLAGGED | Likely intentional stroke-vs-NCSE puzzle, but confirm the gold answer/scoring handles a non-SE primary dx under an SE prefix |
| SE-RS11 | B | minor | case_id prefix vs case content | "RS" (reverse/mimic) prefix but the case is a genuine, textbook JME breakthrough SE — not a pseudo-status/metabolic mimic | FLAGGED | Prefix-content mismatch; the two true SE mimics are P02 (PNES) and P04 (stroke). Mimic mis-prefixing is a judgment call |
| SE-P03 | B/C | minor | patient.history_present_illness vs ground_truth.differential[1] | HPI states TTM at 36°C, but the differential's "Hypothyroidism-... wait, Hypothermia-induced burst-suppression" entry (likelihood high) keys off 33°C; at 36°C that mechanism is far less likely | FLAGGED | Internal 36°C vs 33°C inconsistency undercuts a "high"-likelihood differential premise. Reconcile the TTM target |
| SE-S02 | C | minor | ground_truth.optimal_actions[6].expected_finding vs followup_outputs[3] | Step 7 expected_finding says autoimmune panel "Negative on this draw; rules out autoimmune flare", but the actual panel has Anti-GAD65 2.4 U/mL POSITIVE (ref <1.0) | FLAGGED | Low-titer GAD65 may be nonspecific, but the GT "negative" text is factually wrong vs its own data. Human call |
| SE-S04 | B | nit | fallback_tool_outputs.specialized_test.test_type | `electroencephalogram_quantitative` not in the closed specialized_test vocab (also S06) | FLAGGED | Free-text fallback test_type label outside vocabulary; vocab validator does not gate fallback labels |
| SE-S03/S05/S07/S08/S09/S10/S11/S12/RS11 | B | nit | fallback_tool_outputs.specialized_test.test_type | Various non-vocab fallback test_type labels: transcranial_doppler (S03), nerve_conduction_study (S05/P06), neuropsychological_testing (S07/S09/S12/RS11), fetal_monitoring (S08), renal_function_assessment (S10/P08), dialysis_adequacy_assessment (S11) | FLAGGED | Same class as S04; fallback labels are free text and not in TOOL_PARAMETER_VOCABULARY.md specialized_test list |
| SE-M03/M04/M06/M08/S01–S12/P01/P06/P07/P08/RS11 | B/E | minor | ground_truth.useless_tools (order_specialized_test polysomnography) | Recurring copy-paste: `test_type:"polysomnography"` carries the rationale "DaTscan / dopamine transporter imaging has no role in SE…" — rationale names the wrong modality | FLAGGED | Systematic templated mismatch across ~21 SE cases; the rationale text does not describe polysomnography. Mechanical but the correct rationale text is a rewrite decision |
| SE-M04/M07/S01–S08 (multiple) | B | nit | initial_tool_outputs.labs.abnormal_values_summary | `abnormal_values_summary` array omits several values that `interpretation` lists as (H)/(L) (e.g. M04 omits BUN/Glucose; M07 omits Glucose; S-series omit WBC/Glucose) and sometimes includes non-abnormal AED levels | FLAGGED | Curated-summary vs full-interpretation drift; widespread in M/S cases. Cosmetic, not load-bearing |
| SE-M07 | C | major | patient.history_present_illness | "Right frontal tumor… contralateral (left) arm involvement - note she is right-handed so this would affect her dominant hand" — a right-handed person's dominant hand is the RIGHT, not the left | FLAGGED | Factual error in HPI teaching text; the left arm is the non-dominant hand. In case body → note for human, don't rewrite |
| SE-S11 | B/E | minor | patient.history_present_illness vs exam.additional | "last had dialysis 4 days ago (his Monday session was missed and it is now Wednesday)" = 2-day interval, not 4; exam.additional says "missed dialysis 2 days" | FLAGGED | Temporal contradiction (4 vs 2 days); the correct interval is ambiguous |
| SE-M09 | B | minor | initial_tool_outputs.eeg (findings[0].frequency vs impression) | EEG finding[0] "1.5-2.0 Hz" but the same report's impression says "1.8-2.5 Hz" (LPDs concordant) | FLAGGED | Within-report frequency discrepancy; correct value not unambiguous |
| SE-P04 | B | minor | initial_tool_outputs.eeg.background.anterior_rhythms vs findings/impression | Background calls the pattern "Generalized periodic discharges (GPDs)" but findings+impression call it left-hemisphere "lateralized periodic discharges (LPDs)" | FLAGGED | GPD vs LPD is a meaningful EEG distinction; the lateralized read matches the left-MCA clinical picture |
| SE-M08 | B | nit | ground_truth.red_herrings[0].field_path | field_path `initial_tool_outputs.ct.findings[2]` points to "no epidural/subdural hematoma"; the contusion it describes is findings[1] | FLAGGED | Off-by-one index in a red-herring pointer; descriptor only |
| SE-M08 | B | nit | ground_truth.optimal_actions[5].expected_finding vs followup CSF | Step 6 expected_finding "toxo PCR may be negative (low sensitivity)" but the actual CSF Toxoplasma PCR is POSITIVE | FLAGGED | Hedged expected_finding vs realized positive result; minor |
| SE-M01/M05/S01/S02/S04/S05/S06/S07/S08/S09/S10/S11/P04/P05/P08/RS11 | D | minor | patient.history_present_illness / neurological_exam.additional | HPI/exam routinely contain etiology synthesis, numbered differentials, mechanism teaching, or management directives that pre-empt the agent (e.g. S07 numbered "(1)(2)(3)" precipitants; P02 exam "incompatible with epileptic seizure"; P08 HPI "BENZODIAZEPINE-RESISTANT SE from isoniazid toxicity") | FLAGGED | Case-body leakage of the answer/reasoning; style guide governs tool reports but this pre-empts the diagnostic task. Pervasive across SE; reviewer should decide policy. Noted (not in tool reports, so flag-don't-fix) |
| SE-P06 | D | minor | initial_tool_outputs.eeg.background.anterior_rhythms / findings[0].morphology | EEG structured fields name "classic sporadic CJD pattern" / "typical sCJD PSWCs"; EEG should not deliver the disease verdict (RT-QuIC/biopsy confirm) | FLAGGED | Impression itself is clean (PSWCs described without "CJD"). Borderline — PSWC-CJD is a recognized real-report association; flagged per task ("flag EEG that names the underlying cause") |
| SE-P07 | D | nit | initial_tool_outputs.eeg.background.anterior_rhythms | EEG background calls triphasic-wave pattern "classic hepatic encephalopathy pattern" | NOTED | Impression is clean; triphasic waves are a standard metabolic EEG descriptor and morphology field hedges ("seen in hepatic encephalopathy and other metabolic encephalopathies"). Borderline-acceptable Kind-2 |
| SE-RS11 | D | nit | initial_tool_outputs.eeg.impression / findings[0] | Impression "characteristic of idiopathic generalised epilepsy"; finding names "JME pattern" / "consistent with known JME diagnosis" | NOTED | Patient has a confirmed prior video-EEG JME dx, so referencing the prior same-modality study is allowed; borderline disease-naming, not fixed |
| SE-M05 | D | minor | followup_outputs[0].output.findings[1] (type / signal_characteristics) | MRI structured finding type "Basal ganglia FLAIR signal — anti-NMDAR involvement" and "additional feature of anti-NMDAR encephalitis" name the antibody disease in MRI | FLAGGED | MRI impression is properly hedged ("consistent with limbic encephalitis; differential autoimmune/paraneoplastic and infectious"); the per-finding disease label over-commits. Conservative flag (not fixed) |
| SE-M05 | E | nit | ground_truth.contraindicated_actions | Haloperidol-avoidance warning appears twice (items 1 and 4, near-duplicate wording) | FLAGGED | Duplicated guidance; cosmetic |
| SE-P07/P08/RS11 | A/E | nit | metadata (teaching_points / pitfalls / clinical_pearl) | These three cases carry extra metadata keys absent from the other 27 SE cases | FLAGGED | Schema-optional extra keys; harmless but inconsistent across the condition set |
| SE-P01 | B | nit | patient.clinical_history.past_medical_history | PMH lists "Non-alcoholic steatohepatitis (NASH)" in a patient with 20-yr heavy alcohol use (HPI says "hepatic steatosis") — NASH is by definition non-alcoholic | FLAGGED | Terminology tension; could be a coexisting label. Note only |

## Cross-cutting observations (no action)

- **EEG electrographic calls are KEPT** per the criteria pack: NCSE/electrographic status,
  LPDs/GPDs/PSWCs, Salzburg/IIC framing, extreme delta brush, burst-suppression, triphasic-wave
  morphology, benzodiazepine-trial response. The disease-naming residue flagged above (anti-NMDAR,
  sCJD, HE, IGE/JME) lives in structured `background`/`findings`/`morphology` fields, not the cleaned
  impressions.
- **Confirmatory results KEPT (not leakage)**: CSF HSV-1 PCR (M06), CSF/serum anti-NMDAR (M05),
  CSF anti-Hu (M01, P01), CSF/serum anti-LGI1 (S12), CSF RT-QuIC/14-3-3/tau (P06), cholinesterase
  (P05), isoniazid level + pyridoxine (P08), Toxoplasma serology/PCR (M08).
- **Literature `summary`/`results` are population-keyed**, never a case-specific verdict — verified
  across all cases that order it (the detector flags on disease keywords are these generic statements).
- **Differential ordering**: all cases sort likelihood descending; likelihood/category/condition/
  difficulty enums valid.
- **Sequence constraints**: cases without mass effect use `order_ct_scan → analyze_csf` (hard);
  cases with mass/edema (M02, M08, S07, M09) correctly use `analyze_brain_mri → analyze_csf` or list
  `analyze_csf` as harmful_tools (M02, M09, P-series LP-contraindicated cases).
- **Pregnancy/ESRD/cirrhosis-adjusted lab reference ranges** are correctly applied (S08 Hgb/Cr in
  pregnancy; S11 Hgb in ESRD; P07 albumin/INR in cirrhosis).
- `check_drug_interactions` gives category-level management (allowed); routine-panel
  `clinical_significance` is `null`; specialized serology carries hedged templated comments (M01, M05).

## Tally

- Cases audited: **30** (SE-M01–M09, SE-P01–P08, SE-S01–S12, SE-RS11) — every field of every case read.
- Findings: **~33 distinct items** — 0 blocker, **4 major** (P08 EEG classification [FIXED];
  M02 subtherapeutic-LEV contradiction; P05 mydriasis-vs-miosis; M07 dominant-hand error),
  the remainder minor/nit/noted.
- Fixed: **6** — SE-M05 (EEG disease-naming), SE-M08 (rCBV 0.8→0.6), SE-P08 (EEG classification
  normal→abnormal), SE-S01 / SE-S03 / SE-S10 (CT etiology-assertion Kind-1 leakage stripped).
- Flagged: rest (judgment calls / case-body / cross-case / scoring-semantic).
- Self-verify: coherence stayed **0** and schema **valid** on all 6 edited files; only the 6
  SE files above were changed; no-trailing-newline + literal-unicode convention preserved.

## Top clinical flags for human adjudication

1. **SE-M02 (major)** — ground_truth calls levetiracetam "subtherapeutic" and builds a red herring on
   it, but the lab is LEV 24 mcg/mL (therapeutic, `is_abnormal:false`). The distractor premise is
   contradicted by the data; reconcile the lab value or the GT narrative.
2. **SE-P05 (major)** — patient has mydriasis 7mm throughout while the reasoning mnemonic expects
   miosis; organophosphate poisoning classically causes miosis. Decide whether the atypical
   presentation is intentional or an error.
3. **SE-M07 (major)** — HPI claims left-arm seizure involvement "would affect her dominant hand" in a
   right-handed patient (dominant hand is the right). Factual error in case-body teaching text.
4. **SE-P03** — TTM stated at 36°C but the differential's high-likelihood "hypothermia-induced
   burst-suppression" entry is premised on 33°C; reconcile the temperature.
5. **SE-P04 / SE-RS11 (prefix)** — P04 is an SE-prefixed case whose primary dx is stroke (I63.512);
   RS11 carries a reverse/mimic "R" prefix but is a genuine JME breakthrough SE. Confirm both are
   intentional and scored correctly.
6. **Pervasive case-body leakage (D)** — across most M/S/P HPIs and exam `additional` fields, the
   etiology, numbered differential, mechanism, and management are pre-stated, pre-empting the agent's
   reasoning. Reviewer should decide whether to neutralize this before clinician validation.
7. **Systematic polysomnography/DaTscan rationale copy-paste** — ~21 cases pair
   `test_type:"polysomnography"` with a DaTscan rationale; a templated batch fix would clean all at once.
