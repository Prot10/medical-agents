# SYNC-CARD-RM01
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for SYNC-CARD) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | blocker | followup_outputs[brain MRI] | MRI "normal brainstem" while the case requires and keys on a brainstem lesion; MRA content in a brain MRI report | FIXED (plan RM01): dorsal medullary, bilateral left > right, non-expansile T2/FLAIR hyperintensity without restricted diffusion, faint enhancement (left-predominance matches the reduced left gag); MRA removed; small vessel disease and atrophy kept |
| B | major | patient.history_present_illness, chief_complaint | 18 minutes of CPR with intubation and full recovery in 2 h: a cardiac arrest, not a syncope-like event, and inconsistent with the rest of the case | FIXED (plan RM01): apnoeic bradycardia and brief asystole recovering with bag-mask ventilation; no intubation, no CPR |
| A | blocker | followup_outputs[interpret_labs polysomnography], followup_outputs[order_specialized_test polysomnography] | PSG data stored under `interpret_labs`; the real PSG output was a placeholder equal to the key | FIXED (plan F): full attended PSG report under `order_specialized_test` (AHI 68/h, central 54/h, obstructive 4/h, no Cheyne-Stokes, nadir SpO2 52%, tcCO2 61 mmHg, pauses up to 9.6 s after central apnoeas, no epileptiform activity); interpret_labs copy deleted; PSG required |
| A | blocker | followup_outputs[order_ct_scan chest CT] | Chest CT stored under the head-CT tool | FIXED (plan F): moved to `initial_tool_outputs.body_imaging` (chest, CT, contrast); added follow-ups for `chest_CTA` and `mediastinum_CT` with the same mass, because the library answered those orders with a normal chest study that contradicts the case; new required criterion `action-11-tumour-search-chest-ct` (chest_CT, chest_abdomen_pelvis_CT, chest_CTA, mediastinum_CT) |
| D | major | followup_outputs[literature x2] | Invented or unverifiable references (Matsumoto 2023, Saiz 2020, Dalmau 2019 "35 patients", Graus 2021 attributed to J Neurol) and patient-specific management summaries | FIXED (plan A): one follow-up citing Graus 2021 (Neurol Neuroimmunol Neuroinflamm 2021;8:e1014) with general content, trigger `search_literature_anti_hu_paraneoplastic_brainstem`, last; neutral initial literature answer; criterion optional, out of the stop rule |
| A | major | followup_outputs[amiodarone drug check] | Amiodarone review in a case where no one proposes amiodarone (plan F) | FIXED: deleted; drug criterion optional with methylprednisolone / IVIG and one follow-up each; neutral medication-list review as initial and fallback |
| D | major | initial_tool_outputs.labs.panels["Exclusion studies"] | Engineering text ("which is what this case's diagnosis rests on") and troponin "Within reference range" contradicting troponin I 0.08 in the same report | FIXED: block deleted; magnesium 2.0 placed in an Electrolytes panel |
| D | minor | initial_tool_outputs.labs.abnormal_values_summary | Interpretive annotations ("suggesting chronic hypoventilation", "post-CPR", "stress hyperglycemia", "subclinical hypothyroidism") | FIXED: plain values; BMP bicarbonate relabelled Total CO2 (distinct from the calculated ABG HCO3) |
| C | major | initial_tool_outputs.csf, avoided_actions | CSF was an avoided action whose rationale admitted it is informative here | FIXED (plan J): avoidance removed; optional criterion `action-12-analyze-csf`; initial CSF output with lymphocytic pleocytosis, protein 68, CSF-restricted OCB, IgG index 0.82 |
| A | major | ground_truth.action_criteria[brain MRI] | `required_arguments` used `sequences`, which the tool does not accept | FIXED: any brain MRI accepted |
| A | major | ground_truth.action_criteria[monitoring] | holter_24h pinned, labelled telemetry; output a 24 h Holter | FIXED (plan E): telemetry, holter_24h, holter_48h; output "Inpatient telemetry with impedance respiration and oximetry, 48 h" with time-stamped apnoea-desaturation-arrest sequences; same as fallback |
| A | minor | ground_truth.action_criteria[head CT] | Optional "head CT if MRI not available": CT cannot show the lesion and no NG232 criterion | FIXED: criterion deleted; head CT waste |
| A | minor | ground_truth.action_criteria[labs] | CBC+BMP+Mg+troponin+paraneoplastic pinned | FIXED (plan C): required `panels: [paraneoplastic_panel]`; antibody interpretation in templated hedged voice |
| B | minor | followup_outputs[TTE] | No echo_type, empty valves | FIXED: full TTE report, same values (LVEF 55%, LA 42 mm, PASP 32 mmHg) |
| C | major | ground_truth.assessment | Musts restated tests (MRI, PSG, antibodies); pacing framed as a bridge; no ventilation, tissue diagnosis, immunotherapy detail, swallow safety, driving | FIXED (plan I): see Changes |
| C | major | ground_truth.differential | OSA high, SND and stroke moderate after PSG/MRI; SND cited an EP study (not in the case); nocturnal seizure missing | FIXED (plan K): all low with excluding results; nocturnal seizure, MSA and bulbar myasthenia added (low) |
| E | minor | ground_truth.key_clinical_evidence | "this is a SYNC-CARD mimic" engineering text | FIXED: rewritten clinically |
| D | minor | ground_truth.red_herrings | data_points paraphrased | FIXED: quoted; TSH herring added (the case's own difficulty description names it) |
| A | major | sequence_constraints, stop_rule | None; stop rule with literature and drug, max 0 | FIXED: soft ECG before TTE and monitoring; stop rule = all 7 required criteria, max 3 |
| C | minor | avoided_actions | No EEG or tilt avoidance | FIXED: EEG waste (PSG montage covers nocturnal seizure), tilt waste, CT waste |
| A | minor | fallback_tool_outputs.advanced_imaging | Stub with `modality` "MRI" (not an advanced-imaging term) | FIXED: deleted; library answers |

## Changes, in one paragraph a physician can read before re-reviewing
71-year-old former heavy smoker with two apnoeic unresponsive episodes in sleep, the second with bradycardia and brief asystole reversed by bag-mask ventilation, and a month of progressive dysphagia. Pathway: ECG (normal), inpatient telemetry with respiration and oximetry (sleep-only sinus arrests up to 12.8 s after prolonged apnoea and desaturation), TTE (no structural cause), brain MRI (dorsal medullary rhombencephalitis pattern), polysomnography (severe central sleep apnoea, pauses after central apnoeas), anti-Hu high titre, chest CT (3.4 cm subcarinal mass with nodes). All seven are required; CSF (inflammatory), drug review and literature are optional; head CT, EEG and tilt are waste. Musts: monitored bed with capnography; nocturnal NIV with backup rate (CPAP alone inadequate); pacing only if asystole persists despite ventilation; EBUS-TBNA and oncology referral with FDG-PET staging; IV methylprednisolone then IVIG or plasma exchange alongside tumour treatment; swallow assessment; no respiratory depressants; no driving. Prohibitions: no OSA/CPAP-only framing, no pacemaker as sole treatment, no respiratory depressants, no delay of tumour work-up.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan C2: whole-body FDG-PET for tumour search is not in the vocabulary (`FDG_PET` is the cerebral scan); tumour search is scored on chest CT variants only, and FDG-PET staging is a must.
- Library: an off-pathway `order_body_imaging` order returns a normal report; I stored chest_CTA and mediastinum_CT follow-ups so the mass is not contradicted. Other body studies (mediastinum_MRI) would still receive a normal library report.
- Neutral initial literature and drug answers (see P02 CENTRAL).
- Synonyms (plan C1): accepted labels include generic "sleep related bradyarrhythmia" and "nocturnal asystole"; the lead should decide whether those are specific enough.

## Open questions for Andrea (judgment calls you could not settle)
- Plan Q1 (dataset design, needs Andrea): this anti-Hu brainstem encephalitis with central sleep apnoea and sleep asystole is a neurological cause of syncope-like events. It stays in SYNC-CARD per the plan; whether it should move to a paraneoplastic/autoimmune condition is a dataset-structure choice only Andrea can make.
- Source fidelity: the case is seeded from PMC11623976 (MedCaseReasoning, CC-BY). The plan's changes (no prolonged CPR, a dorsal medullary MRI lesion) may depart from the published case; I could not open the source to check. If fidelity to the source matters for this dataset, Andrea should confirm.

## Verification
Adversarial verifier, 24 Oct 2026. Read the whole final case (patient block, every output, ground truth) against the plan (RM01 bullets, sections A-O) and the log.
- Confirmed: HPI no longer describes 18 min of CPR or intubation; MRI shows the dorsal medullary lesion (left-predominant, matching the reduced left gag) with no MRA content; PSG is a full report under `order_specialized_test` and its arithmetic holds (AHI 68 = central 54 + obstructive 4 + hypopnoea 10); no interpret_labs PSG copy remains; chest CT is under `order_body_imaging` with the required tumour-search criterion; amiodarone follow-up gone; CSF optional with an inflammatory output and no CSF avoidance; labs required `paraneoplastic_panel`; MRI, PSG and antibody musts gone; no Matsumoto, Saiz or Dalmau references; Graus 2021 content is correct (anti-Hu high risk above 70%, definite PNS needs the cancer); OSA low and nocturnal seizure present; musts cover tumour search with EBUS-TBNA and oncology, immunotherapy, NIV with pacing only if asystole persists, monitored bed; stop rule = the seven required criteria, max 3.
- Found and fixed:
  1. B (lab arithmetic), major: ABG pH 7.32 with PaCO2 52 mmHg and HCO3 28.5 mEq/L is impossible (Henderson-Hasselbalch gives pH 7.36). PaCO2 set to 57 mmHg (pH 7.32 recomputes exactly), which fits the chronic hypoventilation (PSG awake tcCO2 50, peak 61 mmHg); BMP total CO2 set to 30 mEq/L to agree with HCO3 28.5 plus dissolved CO2. Summary and interpretation updated.
  2. K (mimic the case raises), minor: the PSG states "no Cheyne-Stokes periodicity" and BNP is 145 pg/mL, but heart-failure central apnoea was absent from the differential. Added as low: LVEF 55%, no crescendo-decrescendo pattern, and hypercapnia (heart-failure central apnoea is hypocapnic).
  3. D, minor: the routine EEG's limitations ended "Extended overnight EEG with concurrent cardiorespiratory monitoring may provide additional diagnostic information", a pointer from a waste study to the required PSG. Deleted.
  4. D, minor: the ECG interpretation offered "may reflect body habitus or pericardial effusion" for the limb-lead low voltage (a differential inside the report; the echo shows no effusion). Now "Low voltage in the limb leads, a nonspecific finding." The red-herring sentence quoted from the same field is unchanged.
  5. B, minor: telemetry `heart_rate_range.min` was 0 (an asystole counted as a heart rate). Set to 32 bpm, the slowest sinus rate the report describes; the pauses stay reported as events (follow-up and fallback).
  6. C, minor: the TTE criterion rationale cited "ESC 2018 Class I when structural disease is suspected after an apparent cardiac arrest", a wording the guideline does not have and a framing the edited HPI no longer supports. Rewritten.
- Open questions: Q1 (whether the case belongs in SYNC-CARD) stays for Andrea, as the plan says. Source fidelity stays as well: only Andrea can say whether departures from the PMC11623976 seed matter.
- Re-ran `perfect_agent.py SYNC-CARD-RM01 -v` (each criterion receives its own report), `case_io.py check` (clean for this case) and the case guards (pass).

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- Labels: the case now scores the paraneoplastic cause: anti-Hu or paraneoplastic brainstem encephalitis labels; "central sleep apnoea/apnea", "sleep apnea syncope", "nocturnal asystole" and "sleep related bradyarrhythmia" retired (they credit heart-failure CSA, OSA or intrinsic sinus node disease, all in the differential); G47.31 (idiopathic CSA) and G47.37 dropped. Q1 (placement) and Q2 (source fidelity) decided in plans/SYNC-CARD-decisions.md: stays in SYNC-CARD as the neurological mimic; the seed is adapted, not reproduced.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-2-interpret-labs citations ['[ESC_2018]'] -> ['[Graus_2021]']; action-11-tumour-search-chest-ct citations ['[ESC_2018]'] -> ['[Graus_2021]']; action-12-analyze-csf citations ['[ESC_2018]'] -> ['[Graus_2021]']; avoid-waste-2-order-ct-scan citations ['[ESC_2018]'] -> ['[NICE_NG232]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-RM01` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.

## Vocabulary wiring (24 Oct 2026)

Central vocabulary (batch 4: orthostatic_blood_pressure, electrophysiology_study, sodium_channel_blocker_challenge, genetic_panel:inherited_arrhythmia and :cardiomyopathy, whole_body_FDG_PET; SYNC-CARD decisions CENTRAL 1).

| field path | change |
| --- | --- |
| `initial_tool_outputs.clinical_assessment` | added: orthostatic_blood_pressure report, supine values = the presenting vitals; No orthostatic fall in blood pressure and no excessive heart rate rise on active standing. |
| `ground_truth.action_criteria[action-orthostatic-blood-pressure]` | added, recommended, after the ECG criterion [ESC_2018] (decisions CENTRAL 1: orthostatic BP in every initial evaluation) |
| `followup_outputs[10] (`request_whole_body_fdg_pet_ct`)` | added: whole_body_FDG_PET report consistent with the stored chest CT |
| `ground_truth.action_criteria[action-whole-body-fdg-pet]` | added, optional [Graus_2021] |
| `ground_truth.assessment.required_recommendations[3]` | removed the clause "; whole-body FDG-PET for staging": staging is now an action criterion, not a must |

Scoring change for re-review: new criteria are recommended or optional, so no required work-up changed.
