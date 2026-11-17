# VASC-DEM: lead plan for the November 2026 round

Lead plan for the 30 VASC-DEM cases (M01-M10, P01-P09, S01-S11). Workers read ROUND_POLICY.md
(October, still in force), work/NOVEMBER_ADDENDUM.md, and `VASC-DEM-decisions.md` next to this file.
That file holds the numbered decisions D1-D18 with reasons and verified sources. Helpers:
`data/review/round-2026-11/bin/` (case_io.py, perfect_agent.py, caselog.py, mri_probe.py). Run
Python as `uv run python -I` from the repository root.

- Notes: 75, all from R1 (NB-KSC3-TWUA-QDTM), in all 30 cases. There are none from R2.
- Approved cases (work/approved.txt): **none in VASC-DEM**.
- Base state, measured 16 Nov 2026:
  - No VASC-DEM case file has changed since 06b74446.
  - Class LIT is done: no literature criterion or output is left.
  - No VASC-DEM brain MRI reports gadolinium, so class MRI-CONTRAST does not touch these cases. If
    a worker edits an MRI anyway, run mri_probe.py.
  - Every case has `max_additional_actions` 1, which stays (October Q2; no note asks for a change).
- Scratch scripts (work/scratch/vascdem-lead/): overview_vd.py (criteria, stop rule, sequence,
  avoided, follow-ups, musts for all 30), dumpcase.py, onrequest.py (follow-ups that match no
  criterion and no avoided action).
  - Full reads: M01, M09, P08, S05 (patient, all initial outputs, ground truth).
  - Targeted reads: S04 (patient and initial outputs), P04 battery, the P02/P07/M02 screens and
    batteries, and the HPI and PMH stroke history of ten cases.
- Conventions: British spelling (ischaemic, haemorrhage), no em or en dashes in new text, and keep
  every `criterion_id`. New criteria and avoided actions take the ids given here.

## 1. Governing guidelines and canonical facts

| question | source | key |
| --- | --- | --- |
| Vascular attribution, mild vs major, mixed causes, AD biomarkers optional | VasCog-2-WSO, JAMA Neurol 2025;82:1103-1112; VASCOG 2014 | `[VasCog2_WSO_2025]` (new) `[VASCOG_2014]` |
| Neuropsych score labels (9th-24th low average; the 8th percentile is the impairment cut-off) | Guilmette 2020, Clin Neuropsychol 34:437 | `[AACN_labels_2020]` (new) |
| Stroke work-up: ECG and cervical imaging class 1; echo and prolonged monitoring conditional; carotid revascularisation; BP; antiplatelets | Kleindorfer 2021 | `[AHA_ASA_2021_secondary]` |
| LV thrombus: warfarin or DOAC, ~3 months, repeat imaging at ~3 months | Levine 2022 AHA statement | `[AHA_LV_thrombus_2022]` (new) |
| Device-detected AF: confirm on electrograms; DOAC "may be considered" (IIb) | ESC AF 2024 | `[ESC_AF_2024]` |
| MRI with a non-MR-conditional CIED: reasonable only under protocol | Indik 2017 HRS | `[HRS_MRI_CIED_2017]` (new) |
| CADASIL: triptans not contraindicated by CADASIL itself | Mancuso 2020 EAN | `[EAN_monogenic_SVD_2020]` (new) |
| Assisted alcohol withdrawal with a past withdrawal seizure | NICE CG115 1.3.4.5-6 | `[NICE_CG115]` (new) |
| CAA, LAAO, ICH BP | Greenberg 2022 | `[AHA_ASA_2022_ICH]` |
| Diabetes in older adults | ADA 2026 s.13 | `[ADA_older_adults_2026]` |

The new keys go in the pack allow-list (CENTRAL 4). Cite them only where the canonical text below
does.

Canonical facts:
- Vascular attribution rests on concordance of the cognitive and functional syndrome, the neurological
  signs, the time course and the imaging. No lesion burden is "sufficient" or "required" by itself.
  Extensive WMH (Fazekas 2-3), two or more lacunes, one lacune with extensive WMH, or a strategic
  infarct support it.
- Timed gait, the neuropsych battery, amyloid biomarkers, FDG-PET and NOTCH3 in sporadic young SVD
  characterise the disease or add certainty. None is a prerequisite for the diagnosis. Exceptions:
  NOTCH3 in P05, where it is the diagnosis, and the battery in P07, where the screen is normal.
- An ECG is required after any ischaemic infarct that has not had one, plus cervical imaging when
  the event is recent. Echo and prolonged monitoring are conditional.
- A stored report is an answer served on request. It does not mean the study was done. Ordering an
  unlabelled on-request study is penalised only through the stop rule.
- The review app prints `abnormal` above `test` and prints null as "none" (addendum).

## 2. Classes

Every class applies to all 30 cases. The cases listed are the measured ones.

### C1. TIER-GAIT (D1). Notes: ea5c0723, 19c0c7e0, ae5091af, 326d4d6e, 338e7d25
Measured: 11 cases have a gait criterion. It is required in M02, P07 and S01-S05, recommended in
M01, P01, P05 and P06.
Fix: required -> recommended in M02, P07, S01, S02, S03, S04, S05. In M01, recommended -> optional.
P01, P05 and P06 stay recommended. Remove the gait criterion id from `required_before_assessment` in
M02, P07 and S01-S05. Rationale text (adapt): "Timed testing quantifies the <gait finding> and the
falls risk; the diagnosis does not depend on it [VASCOG_2014]." M01: "Gait and examination are
normal; a timed baseline is optional."

### C2. TIER-NEUROPSYCH (D2). Notes: 2914e61e, 2d3cca35, 6f7d7387, 6cdaae35, dc590435, 4bfc7ab6, 4bc866bf
Measured: the battery is required in 11 cases (M01, M02, M04, M06, P01, P02, P06, P07, P09, S09,
S10).
Fix: required -> recommended and out of the stop rule in M01, M02, M04, M06, P01, P02, P06, P09,
S09 and S10. **P07 stays required.** Label stays. Rationale (adapt): "Characterises the <profile>
and sets a baseline for <rehabilitation / work / driving / follow-up>; the screen, the informant
history and the MRI establish the disorder [VASCOG_2014]." Any must that cites battery percentiles
is reworded to the screen or exam finding (P02 driving must: "visuospatial impairment on testing"
instead of "at the 1st-3rd percentile").

### C3. TIER-BIOMARKER (D3). Notes: 689eb2a3, 86da537c, d520c5af, 77025126, 1d95402c, 9b4a12d4, 5d26a29f
Tier changes, each out of the stop rule:

| case | criterion | from | to |
| --- | --- | --- | --- |
| M05 | `action-8-analyze-csf` | required | recommended |
| M07 | `action-6-analyze-csf` | required | recommended |
| P01 | `action-6-analyze-csf` | required | recommended |
| P02 | `action-6-order-advanced-imaging` (amyloid PET) | required | recommended |
| M08 | `action-6-order-advanced-imaging` (amyloid PET) | required | optional |
| P02 | `action-7-order-advanced-imaging` (FDG-PET) | recommended | optional |
| P06 | `action-6-order-specialized-test` (NOTCH3) | required | recommended |

Keep the CSF harm labels (M08, P02). Keep the sequence MRI -> CSF (soft).
Reword every must, kce and prohibition that makes the biomarker decisive (list in section 3). Canonical
must head for the mixed cases: "Name mixed Alzheimer and vascular dementia: <amnestic storage-type
profile, MTA grade, pre-stroke course as the case has them> with <vascular burden> [VASCOG_2014];
an amyloid biomarker, if obtained, adds certainty to the Alzheimer component." A cholinesterase
inhibitor must is kept, with no biomarker condition [NICE_NG97].

### C4. ECG-AETIOLOGY (D4). Notes: 11986a51, 4ed18eeb, b763111e
Measured: an ischaemic infarct with no prior ECG or rhythm work-up is found in M04 (never
investigated), P09 (index admission: CT and bloods only), S09 (no ECG in the history) and S01 (two
events, "neither investigated").
- ECG recommended -> required and added to the stop rule: M04 `action-9-analyze-ecg`, P09
  `action-9-analyze-ecg`, S09 `action-9-analyze-ecg`, S01 `action-9-analyze-ecg`.
- M04 `action-6-cervical-vessel-imaging`: recommended -> required, added to the stop rule.
- New must in M04, P09 and S09: "If the ECG and vessel imaging show no cause, arrange echocardiography
  and prolonged rhythm monitoring, which would change the antithrombotic choice
  [AHA_ASA_2021_secondary]."
- Unchanged: M05, S11, M09 (ECG recommended; admission rhythm assessment or ICH); S10, P01, P07 (no
  ECG criterion).

### C5. STOP-RULE (D1-D5). Notes: all tier notes plus f569e1c8, 6331cc50, 2c6f29cf, f33e4140, 77ee2163
New `required_before_assessment`, using the ids in each file:

| cases | required_before_assessment |
| --- | --- |
| M01, M02, M05, M07, M08, P01, P02, P06, S02, S03, S04, S05, S10 | screen, labs, MRI |
| M03 | unchanged (screen, labs, MRI, ECG, carotid, TTE) |
| M04 | screen, labs, MRI, ECG, cervical vessels |
| M06 | screen, labs, MRI, ECG, TTE |
| P07 | screen, labs, MRI, neuropsych |
| P09, S09, S01 | screen, labs, MRI, ECG |
| M09, M10, P03, P04, P05, P08, S06, S07, S08, S11 | unchanged |

The study-specific notes (P05, S06, S07, S08, S11) are ALREADY-FIXED: the criteria already name
`genetic_panel:CADASIL`, `carotid_duplex`, `event_monitor_30d` and `MR_angiography`. Each log states
the argument checked. The display is CENTRAL.md item 3.
CAROTID-ALT (own finding, D5): add `{"tool_name": "order_advanced_imaging", "required_arguments":
{"modality": "MR_angiography"}}` as a second alternative to the carotid criterion in M03
(`action-6-order-advanced-imaging`), M05 (`action-6-order-advanced-imaging`, optional), S06
(`action-6`), S07 (`action-6`) and S11 (`action-6`). The stored MRA follow-up answers it. Check that
its impression agrees with the duplex (checked at base). Update the label to "Image the cervical
carotid arteries (duplex or MR angiography)".

### C6. NP-CUTOFF (D6). Note: 1b7abe7c
Measured: 43 rows between the 9th and 24th percentile flagged "yes" against "25th-75th percentile",
in 25 cases. Every VASC-DEM percentile row uses that range.
Fix, in every neuropsych output (initial or follow-up) of all 30:
- percentile rows: `reference_range` = "9th percentile or above (25th-75th average)";
- `abnormal` = "yes" at the 8th percentile or below, "low average" for the 9th-24th, "no" at the
  25th or above;
- impression or quantitative_data wording for a 9th-24th score: "low average" (not "impaired",
  "reduced", "mildly reduced");
- non-percentile rows (FAQ, validity, IQ, MET) keep their ranges.
Then re-read the criterion `expected_evidence` and the musts for the same wording. M01 battery
impression (canonical): "Set-shifting (Trail Making B 16th percentile), processing speed (SDMT 18th)
and letter fluency (22nd) in the low-average range. Delayed free recall, recognition and naming
within normal limits. Informant FAQ 2/30. Performance-validity measures passed. Profile: low-average
processing speed and executive function with preserved recall and recognition memory."

### C7. LACUNE-COUNT (D7). Notes: 593a77db, 1aa45a50
Measured: S03 (8 stated, 7 listed), S05 (7 stated, 6 listed), P06 (9 stated, 7 listed); the other 19
agree. Fix: keep the count and add the missing site(s) to the findings `location` and the impression
list:
- S03: add "left putamen".
- S05: add "left caudate head".
- P06: "both thalami, both putamina, pons, both coronae radiatae, left caudate head, right internal
  capsule".
Then grep the case for every lacune count and site list (key evidence, expected_evidence, metadata).

### C8. DX-CERTAINTY and IMG-SUFF (D8). Notes: see D8
Labels (`accepted[0]`) change in M01, M02, M06, M10, P06, P08 and S08 to the exact strings in D8.
Never touch the synonym labels after it. Run case_io check, which includes the scorer-v2 guard.
Sufficiency text measured by script (categorical.txt): M01 rh1 and kce1 ("requires a confluent
burden"); M02 rh0 ("independently sufficient"); M03 rh1 ("cannot explain a dementia"); P01 kce0, rh0,
dd0, dd1, proh0; S01 kce0; S06 dd3. Replace with the canonical concordance sentence (D8). S10 kce4
("not sufficient ... by itself") is consistent and stays.

### C9. DIFFERENTIAL (D9, D10, D16)
M02 dd0 and dd1; M04 dd0 and kce1/kce4; M05 dd0, dd2 and kce0-2; M06 dd2 and rh1; M07 and M08 new
or reworded moderate entry "Alzheimer disease with concomitant cerebral small-vessel disease (no
clinically significant vascular contribution)"; P02 dd1; S02 dd2 and rh1; S04 dd2. Likelihoods stay
as they are except the M07 and M08 entries (moderate).

### C10. MUST-INDIVIDUALISE and UNSOURCED-RULE (D10, D11)
Canonical texts are in D10 and D11 (M02, M03, M05, M06, M08, M10, P04, P05, P08, P09, S05, S08).
Class: the fixed "systolic below about 120 mmHg" floor goes in M06, M10 and S08 (musts and
prohibitions). The replacement is "avoiding symptomatic and orthostatic hypotension" plus, in M10
and S08, "until the stenosis is treated".

### C11. ON-REQUEST follow-ups (D12). Notes: 74a16658, 2f5910a5, 75e30bee, 57709b24, fa0764bd, dd0174a0, db0cbe3b
Measured (onrequest.py): 233 stored follow-ups in the 30 cases match no criterion and no avoided
action. Dataset-wide there are 3001 in 550 cases.
Fix, per case:
1. Keep every stored report.
2. Add one avoided action per study listed below for that case. Id: `avoid-<severity>-<term>`, e.g.
   `avoid-waste-perfusion-spect`, `avoid-harm-electrophysiology-study`. `required_arguments` names
   the term (`modality`, `test_type`, `assessment_type`, `echo_type`, `study`). Use the case-specific
   rationale pattern below.
3. Reorder `followup_outputs`: credited follow-ups in criterion order, then all on-request ones.
4. Run perfect_agent: no criterion alternative may match a new label.

Severity table (rationale skeleton; add the case's reason):

| study | severity | rationale | exceptions (unlabelled unless stated) |
| --- | --- | --- | --- |
| perfusion_SPECT | waste | "Perfusion SPECT adds nothing to the MRI in vascular cognitive impairment [NICE_NG97]." | none |
| tau_PET | waste | "Tau PET is not part of the clinical work-up [VasCog2_WSO_2025]." | none |
| DTI_tractography, functional_MRI, MR_spectroscopy, MR_venography, perfusion_MRI | waste | "A research or problem-solving sequence that does not change diagnosis or management [STRIVE_2]." | P08: harm (MR, see below) |
| CT_perfusion | waste | "Perfusion imaging is for acute stroke; these infarcts are chronic [AHA_ASA_2021_secondary]." | M03: harm (iodinated contrast with a documented allergy) |
| cardiac_MRI | waste | "No cardiac question that TTE has not answered." | M03 unlabelled (LV thrombus, CMR can be useful [AHA_LV_thrombus_2022]); P08 harm |
| levodopa_challenge | waste | "No rigidity, bradykinesia or rest tremor on examination; there is no parkinsonism to test." | none (no case has parkinsonism; checked) |
| electrophysiology_study | harm | "Invasive intracardiac study with no arrhythmic indication." | none |
| cerebral_angiography (catheter) | harm | "Invasive angiography carries a stroke risk; non-invasive vessel imaging answers the question [AHA_ASA_2021_secondary]." | M10, P08, S08, S11 unlabelled (carotid stenosis under revascularisation assessment; R1 kept it in P08, S08, S11) |
| coronary_angiography | harm | "Invasive coronary study with no cardiac indication in this work-up." | M03 unlabelled (new EF 38% after an unrecognised MI) |
| coronary_CTA | waste | "No cardiac indication in this work-up." | M03: harm (contrast allergy) |
| TEE (`order_echocardiogram {"echo_type": "TEE"}`) | waste | "<AF / LV thrombus> already settles anticoagulation; TEE would not change management." | only where no echo wildcard label exists: M03, M10, S06, S07 waste; S01 waste ("lacunar events; no cardioembolic question"); P08, S08, S11, M04, M06, P09, S09 unlabelled |
| ssep, skin_biopsy_iencf | waste | "The polyneuropathy (or its absence) is clinically evident; neither test informs the cognitive diagnosis." | none |
| emg_ncs | waste in P02 only | "No neuropathy or radiculopathy on examination." | M02, M08, P01, S01, S04 unlabelled (neuropathy on exam) |
| tilt_table | waste | "No syncope or orthostatic symptoms requiring tilt testing." | |
| amyloid_PET (P04 only) | waste | "Probable CAA rests on MRI (Boston v2.0); amyloid PET would not change management [Boston_v2]." | |
| order_body_imaging chest_CTA, mediastinum_CT, chest_xray, pelvis_abdomen_CT, pelvis_abdomen_MRI, spine_CT (P02) | waste | "No chest, abdominal or spinal indication in this work-up." | M08 spine_CT unlabelled (active lumbar stenosis); pelvis_abdomen_ultrasound unlabelled (S03 CKD, M08 urinary symptoms); P08 MRI studies harm |
| P08 all MR: cardiac_MRI, DTI, perfusion_MRI, MR_angiography, functional_MRI, MR_spectroscopy, MR_venography, spine_MRI, mediastinum_MRI, pelvis_abdomen_MRI, peripheral_nerve_MRI | harm | D13 MRI rationale. Put them as alternatives of the existing `avoid-harm-1-analyze-brain-mri` (one entry, one rationale) | |
| gait, neuropsych (M03), speech_language_evaluation, visual_field_perimetry, structured_headache_history_ichd3, polysomnography, respiratory_function, orthostatic_blood_pressure, transcranial_doppler | unlabelled | reasonable or rehabilitative | |
| MR_angiography (M03, M05, S06, S07, S11) | becomes a criterion alternative (C5) | | |

Per-case on-request list (follow-up index at base: term). Workers label per the table:
- M01: 1 SPECT, 3 DTI. M02: 1 SPECT, 2 levodopa, 4 EMG (unlabelled), 5 SSEP, 6 skin biopsy, 7 DTI.
- M03: 0 SPECT, 1 neuropsych (unl.), 2 gait (unl.), 3 levodopa, 4 cardiac MRI (unl.), 5 coronary angio
  (unl.), 6 coronary CTA (harm), 7 DTI, 8 CT perfusion (harm), 9 perfusion MRI, 10 MRA (criterion),
  11 cerebral angio (harm), 12 fMRI. TEE: none stored, but add the TEE waste label.
- M04: 1 SPECT, 2 speech (unl.), 3 DTI, 4 CT perfusion, 5 perfusion MRI.
- M05: 1 SPECT, 2 tau, 3 gait (unl.), 4 levodopa, 6 SSEP, 7 DTI, 8 MRA (criterion), 9 cerebral angio.
- M06: 1 SPECT, 2 gait (unl.), 3 levodopa, 4 cardiac MRI, 5 DTI, 6 CT perfusion, 7 perfusion MRI,
  8 chest CTA, 9 mediastinum CT, 10 chest X-ray.
- M07: 1 tau, 2 gait (unl.), 3 levodopa, 5 cardiac MRI, 6 EP study, 7 speech (unl.), 8 DTI.
- M08: 2 tau, 3 gait, 4 levodopa, 6 cardiac MRI, 7 EP study, 8 speech, 9 EMG (unl.), 10 DTI, 11 spine
  CT (unl.), 12 pelvis MRI, 13 pelvis CT, 14 pelvis US (unl.).
- M09: 0 SPECT, 1 gait, 2 levodopa, 4 cardiac MRI, 5 speech, 6 SSEP, 7 DTI, 8 CT perfusion, 9 perfusion MRI.
- M10: 1 SPECT, 2 gait, 3 levodopa, 4 cardiac MRI, 5 EP study, 6 visual fields (unl.), 7 DTI,
  8 CT perfusion, 9 perfusion MRI, 10 cerebral angio (unl.), 11 TCD (unl.). TEE waste label added.
- P01: 2 SPECT, 3 tau, 4 levodopa, 6 speech, 7 EMG (unl.), 8 DTI.
- P02: 2 tau, 4 EMG (waste), 5 PSG (unl.), 6 DTI, 7 spine CT (waste).
- P03: 1 SPECT, 3 DTI, 4 CT perfusion, 5 perfusion MRI.
- P04: 1 SPECT, 2 amyloid PET (waste), 3 gait, 4 levodopa, 6 cardiac MRI, 7 EP study, 8 visual fields
  (unl.), 9 DTI, 10 CT perfusion, 11 perfusion MRI.
- P05: 3 SPECT, 4 levodopa, 5 speech, 6 headache history (unl.), 7 DTI.
- P06: 3 SPECT, 4 levodopa, 6 cardiac MRI, 7 speech, 8 PSG, 9 respiratory, 10 orthostatic BP (all three
  unl.), 11 tilt table (waste), 12 DTI.
- P07: 1 SPECT, 2 levodopa, 4 DTI.
- P08 (74a16658: R1 Steps 11, 14, 18-30 = fu 2, 5, 9-21): 0 SPECT (waste), 1 gait, 2 levodopa (waste),
  3 TEE (unl.), 4 cardiac MRI (harm), 5 EP study (harm), 6 speech, 7 CT perfusion (waste), 8 cerebral
  angio (unl.), 9-14 MR modalities (harm), 15 chest CTA, 16 mediastinum CT, 17 chest X-ray (waste),
  18-21 MR body studies (harm).
- P09: 0 SPECT, 1 headache history (unl.). S01: 1 SPECT, 2 levodopa, 3 TEE (waste), 4 EMG (unl.), 5 DTI.
- S02: 1 SPECT, 2 levodopa, 4 speech, 5 PSG, 6 respiratory, 7 DTI. S03: 1 SPECT, 2 levodopa, 4 speech,
  5 DTI, 6 pelvis CT (waste), 7 pelvis US (unl.).
- S04 (2f5910a5, 75e30bee): 2 SPECT, 3 levodopa, 5 EMG (unl.), 6 SSEP (waste), 7 skin biopsy (waste), 8 DTI.
- S05: 1 SPECT, 2 levodopa, 4 cardiac MRI, 5 speech, 6 respiratory, 7 DTI, 8 chest CTA.
- S06 (57709b24: fu 0, 2, 3, 4, 6, 7, 8, 10, 11): 0 SPECT, 1 gait, 2 levodopa, 3 cardiac MRI, 4 EP study,
  5 speech, 6 DTI, 7 CT perfusion, 8 perfusion MRI, 9 MRA (criterion), 10 cerebral angio (harm),
  11 fMRI. TEE waste label added.
- S07 (fa0764bd: fu 0, 2-6, 8): 0 SPECT, 1 gait, 2 levodopa, 3 TEE (waste), 4 DTI, 5 CT perfusion,
  6 perfusion MRI, 7 MRA (criterion), 8 cerebral angio (harm).
- S08 (dd0174a0: fu 1, 3, 5-7, 9-11, 14-16): 1 SPECT, 2 gait, 3 levodopa, 4 TEE (unl.), 5 cardiac MRI,
  6 coronary angio (harm), 7 coronary CTA (waste), 8 speech, 9 DTI, 10 CT perfusion, 11 perfusion MRI,
  12 cerebral angio (unl.), 13 TCD (unl.), 14 chest CTA, 15 mediastinum CT, 16 chest X-ray.
- S09: 0 SPECT, 1 headache history. S10: 0 SPECT, 1 gait, 2 levodopa, 4 speech, 5 DTI.
- S11 (db0cbe3b: fu 0, 2, 4-7, 10): 0 SPECT, 1 gait, 2 levodopa, 3 TEE (unl.), 4 SSEP, 5 DTI, 6 CT perfusion,
  7 perfusion MRI, 8 MRA (criterion), 9 cerebral angio (unl.), 10 fMRI.
Note: where a case already has a wildcard `order_echocardiogram {}` or `order_cardiac_monitoring {}`
waste label, do not add a narrower duplicate.

### C12. AVOIDED-SOFTEN (D13). Notes: dfcba78d, ddd47148, f301a8f4, 58df8274
- P03: delete `avoid-waste-1-analyze-eeg` (note that the CSF label is mis-named `avoid-harm-1-analyze-csf`
  with severity waste; leave its id). Add optional `action-eeg-tfne` `analyze_eeg {}`, with expected
  evidence "Normal routine EEG; a normal interictal recording does not exclude focal sensory seizures",
  citation `[Boston_v2]`. Move `fallback_tool_outputs.eeg` to `initial_tool_outputs.eeg` unchanged.
- S11: delete the `order_cardiac_monitoring` waste label. Add optional `action-prolonged-monitoring`
  `order_cardiac_monitoring {}`. Author `initial_tool_outputs.cardiac_monitoring`: 30-day event
  monitor, `monitor_type: event_monitor_30d`, `duration_hours: 720`, sinus rhythm, no AF, no pauses.
  Keep the Holter fallback. Soft constraint: ECG before monitoring.
- M03: delete `avoid-waste-6-order-cardiac-monitoring` and prohibition 0 (D11). No criterion.
- P08: new rationale on `avoid-harm-1-analyze-brain-mri` (D13). Add the MR alternatives (C11).

### C13. INTERPRETER (D14). Note: 5cbbc199. M09 only (S04 checked: trained interpreter already).

### C14. DISPLAY-SHIFT (D15). Notes: e8dbcb56 (M09), dc877a4d (P07): CENTRAL, data checked correct.

## 3. Per-case index

Ruling words: FIXED, ALREADY-FIXED, CENTRAL, DECLINED, NEEDS-ANDREA, NO-ACTION. "Class" lists the
class findings in the case even without a note. No case is approved.

### VASC-DEM-M01 (approved: no)
- 1b7abe7c-6bd9-461b-821c-182be40a65e6: FIXED (C6, D6, D8). Percentile rows and impression (canonical text in C6). Label ->
  "Mild vascular cognitive impairment (mild vascular cognitive disorder), most likely due to moderate
  cerebral small-vessel disease; the threshold for dementia is not met". Must0 "this is mild vascular
  cognitive impairment, not dementia" -> "...most likely mild vascular cognitive impairment, not
  dementia: low-average executive and speed scores and MoCA 24/30 below expectation for 17 years of
  education, with preserved instrumental independence (FAQ 2/30) [VasCog2_WSO_2025]".
- ea5c0723-b694-4846-807b-861807c3b6fe: FIXED (C1). Gait `action-4-perform-clinical-assessment` -> optional.
- 265d87a9-5cb7-471b-8d01-f023b94bb911: FIXED (C8). rh1 correct_interpretation and kce1: delete "requires a confluent burden".
  New text: "Fazekas 2 change and one lacune support a vascular contribution but do not by themselves
  establish it; the attribution rests on its concordance with the executive and speed profile and the
  course [VasCog2_WSO_2025]."
- Class: C2 (battery -> recommended, out of the stop rule); C11 (SPECT, DTI waste); prohibition "Do not
  dismiss ... when formal testing shows objective executive impairment" -> "...when testing shows
  low-average executive scores below expectation for her education".

### VASC-DEM-M02 (approved: no)
- dc52b75a-aede-4452-bf92-4db2a6d396f5: FIXED (D8, D10). Label per D8; must0, kce0 and rh0 reworded (alcohol may contribute to
  the cognition).
- ad9a7f1e-c362-4ed0-8cba-218f552eac6c: FIXED (D10). dd1 and the Korsakoff prohibition reworded.
- b6795cb2-0286-4186-9f0e-c073448d3ca9: FIXED (D10). Must2 replaced by the assisted-withdrawal must; the glucose prohibition
  replaced.
- 19c0c7e0-97a3-4476-9233-9543c217b3c2: FIXED (C1, C5). Gait -> recommended, out of the stop rule.
- Class: C2 (battery -> recommended); C6 (FAS 9th, RAVLT 17th -> "low average"); C8 rh0; C11.

### VASC-DEM-M03 (approved: no)
- b4d1f1bf-0d3d-4959-ab55-4caaae1a4dba: FIXED (D11). Must0 -> "Anticoagulate for the LV apical thrombus with warfarin (INR 2-3)
  or a DOAC as a reasonable alternative chosen on her circumstances, typically for 3 months; repeat
  cardiac imaging at about 3 months to guide duration; refer to heart failure for EF 38%
  [AHA_LV_thrombus_2022] [AHA_ASA_2021_secondary]." Must1 -> "Review aspirin with cardiology when
  anticoagulation starts: with an old infarct and no recent coronary syndrome or stent, anticoagulant
  monotherapy is usual." Prohibition 1 -> "Do not continue aspirin with the anticoagulant without a
  cardiology review of the coronary indication."
- f301a8f4-9621-49b2-8d74-8e7dd01f08fa: FIXED (D11, C12). Prohibition 0 deleted; the monitoring waste label removed.
- Class: C5 CAROTID-ALT (MRA alternative); C8 rh1 ("cannot explain a dementia" -> "supports at most a
  minor small-vessel contribution"); C11 (incl. harm for CT perfusion, coronary CTA and cerebral angio
  because of the contrast allergy; TEE waste).

### VASC-DEM-M04 (approved: no)
- 2914e61e-79a9-417f-807f-af359ea82c2c: FIXED (C2). Battery -> recommended, out of the stop rule; rationale "return to teaching,
  driving and rehabilitation".
- 11986a51-9598-4ea2-bf28-dc9cdc584f9b: FIXED (C4). ECG and cervical vessels -> required, in the stop rule; conditional
  echo/monitoring must added; echo and monitoring stay optional.
- ec3158d4-68fd-4d64-81bf-6363a0acbabd: FIXED (D16). kce4 -> "Preserved medial temporal lobes make typical Alzheimer disease less
  likely but do not exclude early or atypical forms; here the abrupt onset, stable course, Gerstmann
  syndrome and the matching infarct strongly favour a vascular cause." kce1: delete "delayed recall is
  the first domain to fail" and say "amnestic presentations are typical of AD, but non-amnestic
  variants exist". Must0 "not Alzheimer disease" -> "a vascular cause is strongly favoured over
  Alzheimer disease"; the reason list stays.
- Class: C6 (no 9th-24th rows; range strings only); C11.

### VASC-DEM-M05 (approved: no)
- 689eb2a3-69ca-477e-af32-0c67d39ce3ba: FIXED (C3). CSF/PET criterion -> recommended, out of the stop rule; musts per C3 head.
- 82baa9d2-f417-4255-9c26-cfdb810c6d42: FIXED (D11). Gliclazide must and prohibition; kce4 -> "Hypoglycaemia risk on a
  sulfonylurea with cognitive impairment makes the diabetes regimen a target of review".
- 801c6a8c-31a0-49dc-9c17-c13006ef67e2: FIXED (D16). kce0 drops "make this mixed disease" as a proof; kce1 "cannot account for"
  -> "makes an isolated strategic amnesia unlikely, though stroke-related network effects may add to
  the decline"; kce2 "forces the second diagnosis" -> "strongly supports an amnestic
  neurodegenerative process; it is not disease-specific"; dd0, dd2 and rh1 aligned.
- Class: C5 CAROTID-ALT (optional criterion); C6 (BNT 20th); C11.

### VASC-DEM-M06 (approved: no)
- beb3f9ea-5276-4557-bd06-e1c4126b00fe: FIXED (D8, D16). Label per D8; kce0, rh1, dd2 and prohibition 2 reworded.
- b9531b5a-9fbd-4177-a446-dad85d2e2f1c: FIXED (D11). BP must; prohibition 1 deleted; kce3 deleted or reworded to "Blood pressure
  is individualised to avoid symptomatic and orthostatic hypotension".
- e55a303a-4229-4a1e-8e06-cff0ba71eee8: FIXED (D11). Furosemide review must; prohibition 3 reworded.
- 2d3cca35-9625-4127-bc20-947e5f69160c: FIXED (C2). Battery -> recommended, out of the stop rule.
- Class: C6 (RAVLT 24th); C11 (TEE stays unlabelled: prosthetic valve, embolism not excluded).

### VASC-DEM-M07 (approved: no)
- 57eb5732-5d16-4a48-b712-ad3caefcecc8: FIXED (D9). Label kept. New moderate differential entry (D9). Must0 per the C3 head, with
  "Fazekas 2, two lacunes and one deep microbleed support a small-vessel contribution of uncertain
  clinical weight". Prohibition 0 "when both are demonstrated" -> "when both are supported".
- 86da537c-1633-436e-9d65-3ead969ca85b: FIXED (C3). Criterion -> recommended, out of the stop rule; delete any text that makes
  amyloid status decide the cholinesterase inhibitor (grep "cholinesterase" and "biomarker").
- Class: C6 (TMT-B 9th, SDMT 12th, BNT 18th); C11 (EP study harm).

### VASC-DEM-M08 (approved: no)
- d520c5af-e7a1-49d9-896e-98e295bece28: FIXED (C3). Amyloid PET -> optional, out of the stop rule; CSF harm stays.
- 7b4f4fe3-4af8-4da2-b79f-0cfced2e1160: FIXED (D9, D11). Label kept; must0 per the C3 head; must1 reworded (D11); the prohibition
  "Do not attribute the dementia to atrial fibrillation when there is no infarct on MRI" deleted;
  moderate differential entry added.
- b7821cae-39d4-4dc2-8551-ee9cbe4814d2: FIXED (D11). kce2 reworded.
- Class: C6 (BNT 12th, SDMT 10th); C11.

### VASC-DEM-M09 (approved: no)
- 5cbbc199-74a7-450b-a112-5265e6063459: FIXED (D14). Screen `scores.assessment_language` -> "Mandarin, by a Mandarin-speaking
  examiner (MoCA Mandarin version, Chinese norms)"; the `impression` names the version;
  `neurological_exam.mental_status` "examined in Mandarin with the family interpreting" -> "examined
  in Mandarin by a Mandarin-speaking examiner"; battery row "Culture-fair naming (Mandarin)" ->
  "Boston Naming Test (Chinese version, Mandarin norms)"; the battery quantitative_data norms ->
  "Chinese norms, administered in Mandarin by a Mandarin-speaking examiner". Criterion label and
  rationale add: "a validated first-language instrument given by a qualified examiner or with a
  professional interpreter; family interpretation is not equivalent".
- e8dbcb56-f54a-4d77-b634-6010d485e52b: CENTRAL (D15, CENTRAL.md item 2). Checked: 48th percentile, abnormal "no", in range; the
  next row's "yes" prints above its own label. The row is renamed under 5cbbc199.
- Class: C6 (RAVLT 18th); C11.

### VASC-DEM-M10 (approved: no)
- 10679dcb-0aaf-462f-95f0-2f37339d7db5: FIXED (D11). Revascularisation must (eligibility assessment, 5 months); prohibition 3
  "planned carotid surgery" -> "possible carotid surgery".
- deb7367b-e3d2-440e-9c06-5544f5909a44: FIXED (D11). DOAC plus the antiplatelet plan with vascular surgery; prohibition 1 kept
  ("outside a defined peri-procedural plan").
- a1dd74ae-ffb5-48a0-af3b-56f56b794190: FIXED (D8). Label; must0 -> "Diagnose multi-infarct vascular dementia with two coexisting
  potential stroke mechanisms, atrial fibrillation and the right carotid stenosis: the right PCA
  infarct lies outside the carotid territory and supports an additional embolic source, while the
  right MCA and border-zone infarcts may reflect haemodynamic compromise, artery-to-artery embolism
  or cardioembolism [VASCOG_2014]"; kce0 and dd0 aligned (drop "AF cannot explain").
- Class: C10 (the 120 floor in the BP must and prohibition 2); C6 (RAVLT 20th); C11 (TEE waste;
  cerebral angio and TCD unlabelled).

### VASC-DEM-P01 (approved: no)
- 6f7d7387-0d03-46c5-ba44-4515524f3ae8: FIXED (C2). Battery -> recommended, out of the stop rule.
- 77025126-2b0b-45af-9c4d-2b5345315ed9: FIXED (C3, C8). Biomarker -> recommended, out of the stop rule; kce0 rewritten without
  "demands the biomarker" or "built to punish"; rh0, dd0, dd1 and proh0 per the concordance rule;
  proh1 -> "Do not withhold a cholinesterase inhibitor because a vascular diagnosis has been made, when
  the amnestic syndrome indicates an Alzheimer component"; must0 per the C3 head.
- Class: C6 (BNT 14th); C11.

### VASC-DEM-P02 (approved: no)
- 88d4951c-9d08-4ff0-8efa-ee2ad5062e16: FIXED + CENTRAL (D9). Label kept; dd1 key_features per D9; must0 hedged on the vascular
  weight; synonym request CENTRAL 2.
- 1d95402c-08dc-4ed8-8a0d-c982bae5a43c: FIXED (C3). Amyloid PET -> recommended, out of the stop rule; CSF harm stays; must0 per
  the C3 head.
- 9b4a12d4-f05a-442d-b640-2ac66e55ea77: FIXED (C3). FDG -> optional.
- Class: C2 (battery -> recommended; driving must reworded); C6 (TMT-B 20th); C11 (EMG and spine CT
  waste).

### VASC-DEM-P03 (approved: no)
- dfcba78d-d775-4f63-8146-0a0ea483d313: FIXED (C12). EEG label removed; optional EEG criterion with the stored routine EEG.
- Class: C6 (SDMT 9th, FAS 14th, RAVLT 21st, BNT 22nd); C11.

### VASC-DEM-P04 (approved: no)
- ead8156d-9f72-415a-b0e5-d2ccb1b08c8d: FIXED (D11). Musts 1 and 2 and prohibition 0 reworded (multidisciplinary reassessment,
  LAAO evaluation with peri-procedural antithrombotics).
- 7abe5c12-2d92-4eb8-abf7-bb7c9b12e055: FIXED (D16). Oral Trails B; SDMT qualified; impression and adaptations; expected_evidence.
- Class: C6 (FAS 10th, RAVLT 19th); C11 (amyloid PET waste, EP study harm).

### VASC-DEM-P05 (approved: no)
- c7d6ad9b-7ce2-4674-824e-0432127e5464: FIXED (D11). Sumatriptan must; triptan prohibition -> "Do not continue triptans or start
  ergots before specialist review of the transient hemipareses, which are labelled contraindications
  whether ischaemic or hemiplegic"; drug-interaction output reworded (no CADASIL contraindication).
- 5a3125af-33a7-49d8-a51a-bc3e0fdcdd22: FIXED (D11). rh0 correct_interpretation (uncertain mechanism); the "complicated migraine"
  prohibition reworded; check the key evidence for "were infarcts".
- f569e1c8-5c84-4176-90ac-882b1025c2aa: ALREADY-FIXED + CENTRAL (C5). The NOTCH3 criterion already requires
  `genetic_panel:CADASIL`; display item 3.
- Class: C1 (gait already recommended); C6 (RAVLT 20th); C11.

### VASC-DEM-P06 (approved: no)
- b5638ec2-1f2c-4a78-8557-d9bf056f4662: FIXED (D8). Label "...; CADASIL unlikely and not genetically confirmed". Must0 ->
  "...CADASIL is unlikely but not excluded: NOTCH3 testing is reasonable given onset before 55 and his
  father's stroke at 55, and a non-cysteine-altering variant of uncertain significance does not
  establish it [VASCOG_2014] [Rutten_2019]"; prohibition 0 kept.
- 5d26a29f-61b3-466a-9668-004ba7788a94: FIXED (C3). NOTCH3 -> recommended, out of the stop rule; MRI -> NOTCH3 soft constraint kept.
- 6cdaae35-2c5d-4a57-bd71-488eef840364: FIXED (C2). Battery -> recommended, out of the stop rule.
- Class: C7 (9 lacunes); C6 (RAVLT 18th); C11 (tilt table waste).

### VASC-DEM-P07 (approved: no)
- ae5091af-b3b8-4ab6-b338-507704e63278: FIXED (C1). Gait -> recommended, out of the stop rule.
- dc877a4d-76f1-4260-878d-ac41ac49efea: CENTRAL (D15). Checked: premorbid IQ 128 is already abnormal "no" (range "not
  applicable"); the next row (FAQ 23/30) is "yes".
- Class: battery stays required (D2); C6 (SDMT 22nd); C11.

### VASC-DEM-P08 (approved: no)
- 696e12fd-3c4c-4980-b431-f57b1480d6ca: FIXED (D11). DOAC must (electrogram review, risk-based); prohibition 3 conditional.
- 58df8274-f2d7-4a4f-9d9f-4d17872f4c1e: FIXED (D13). MRI label rationale rewritten; severity harm kept (reason in D13); MR
  modalities added as alternatives.
- 54d36054-5cb7-4469-9ab0-3fedb3fd3123: FIXED (D8). Label; must0 adds "...and that the carotid atherosclerosis and device-detected
  AF are coexisting potential mechanisms whose share in each infarct cannot be assigned"; kce and dd
  aligned (grep "carotid" and "atrial").
- 74a16658-11cd-4724-8602-5a8061d142bf: FIXED + CENTRAL (C11). Labels and reorder; stored reports kept (the library would serve
  normal MRI reports to a patient who cannot be scanned); display CENTRAL 1.
- Class: C6 (BNT 10th, SDMT 11th, RAVLT 20th).

### VASC-DEM-P09 (approved: no)
- 4ed18eeb-28eb-46a8-9ab3-f9b76482d081: FIXED (C4, D11). ECG -> required and in the stop rule; antiplatelet must conditional;
  conditional echo/monitoring must; dd and kce aligned (AOP mechanism small-vessel or cardioembolic).
- dc590435-cb3d-44d8-aaeb-93a62c7649bd: FIXED (C2). Battery -> recommended, out of the stop rule.
- Class: C11.

### VASC-DEM-S01 (approved: no)
- 3a1edd9d-d0b8-4c1a-ac0a-72403f89e62f: FIXED (C8). kce0 -> "Vascular attribution rests on concordance: two dated stepwise
  declines after probable lacunar events, a dysexecutive retrieval profile, a subcortical gait and a
  Fazekas 3 burden with five lacunes [VasCog2_WSO_2025]."
- 326d4d6e-2158-4ca9-80e0-bbd8324fc71f: FIXED (C1). Gait -> recommended, out of the stop rule.
- Class: C4 (ECG -> required, in the stop rule); C6 (RAVLT 12th, Rey 20th); C11 (TEE waste).

### VASC-DEM-S02 (approved: no)
- d16d609a-293e-40d9-a6ff-598c9ebcd3c8: FIXED (D16). dd2 and rh1 (OSA can contribute to WMH and SVD).
- 368be191-3ff4-4cd6-880f-4ef815c25066: FIXED (D16). kce2 and the battery criterion rationale.
- 338e7d25-e993-4cb1-87a9-7791e0b80cf5: FIXED (C1). Gait -> recommended, out of the stop rule.
- Class: C6 (RAVLT 18th); C11.

### VASC-DEM-S03 (approved: no)
- 593a77db-8038-4921-a5f7-8ce76c9fd5c2: FIXED (C7). Add "left putamen"; recheck the impression, expected_evidence and kce.
- Class: C1 (gait -> recommended, out of the stop rule); C6 (RAVLT 15th); C11.

### VASC-DEM-S04 (approved: no)
- 9d79fcb4-14fc-4e7e-99fe-f5927d52bc6a: FIXED (D16). dd2 -> "probable functional B12 deficiency: B12 244 pg/mL on 22 years of
  metformin with raised MMA and homocysteine, both of which eGFR 58 can also raise; diabetes is a major
  cause of the polyneuropathy"; kce3 and must4 "probable deficiency", replacement and monitoring kept.
- 2f5910a5-9e3a-4f4b-940b-0526f0ac9e59: FIXED + CENTRAL (C11). SSEP waste, moved to the on-request block.
- 75e30bee-f1ef-4fd4-94b0-335ba1f2e578: FIXED + CENTRAL (C11). SSEP and skin biopsy waste, reorder.
- Class: C1 (gait -> recommended, out of the stop rule); C6 (RAVLT-equivalent 16th); C13 checked (no
  change).

### VASC-DEM-S05 (approved: no)
- d9a59fff-be3b-45a5-841d-8fd49c5285e8: FIXED (D11). The anticoagulation reassessment must replaces musts 1-2; prohibition 1 per D11;
  must0's "checking the interaction with apixaban" kept.
- 1aa45a50-09ad-4392-9142-04f0cb25c229: FIXED (C7). Add "left caudate head".
- Class: C1 (gait -> recommended, out of the stop rule); C6 (no 9th-24th rows); C11.

### VASC-DEM-S06 (approved: no)
- 57709b24-0f36-4b78-900b-624257a0b522: FIXED + CENTRAL (C11). Labels and reorder for fu 0, 2, 3, 4, 6, 7, 8, 10, 11; TEE waste.
- 6331cc50-1d68-4082-a75b-76b1ea279852: ALREADY-FIXED + CENTRAL (C5). The criterion requires `carotid_duplex`; MRA alternative
  added (CAROTID-ALT), which is still a carotid assessment.
- Class: C8 dd3; C6 (SDMT 10th, BNT 12th, RAVLT 20th, JLO 15th).

### VASC-DEM-S07 (approved: no)
- 2c6f29cf-7333-4ef0-8ca2-452a72d6c204: ALREADY-FIXED + CENTRAL (C5). `carotid_duplex` and `event_monitor_30d` already required;
  a Holter order neither matches the criterion nor receives the 30-day report (MockServer tiers);
  MRA alternative added.
- fa0764bd-4448-4868-b94c-58847c5fc7f8: FIXED + CENTRAL (C11). Labels and reorder for fu 0, 2-6, 8.
- Class: C6 (SDMT 9th, Rey 10th, RAVLT 22nd).

### VASC-DEM-S08 (approved: no)
- 7c250244-21c7-43f1-8eba-42d59b549e95: FIXED (D11, D8). Vascular-team must; prohibition 3 reworded; label per D8; kce and the
  teaching points that call the stenosis "symptomatic" or the step "the event" reworded.
- f33e4140-cdb0-45ea-a946-3a42ef75f1c9: ALREADY-FIXED + CENTRAL (C5). `carotid_duplex` required, the MRA criterion and the
  constraint already name `MR_angiography`.
- dd0174a0-5114-4771-a81d-c9f7d1e75488: FIXED + CENTRAL (C11). Labels and reorder; cerebral angio, TEE and TCD stay unlabelled.
- Class: C10 (the 120 floor in must1 and prohibition 0 -> "aggressively ... symptomatic or orthostatic
  hypotension"); C6 (RAVLT 19th).

### VASC-DEM-S09 (approved: no)
- b763111e-d07f-413d-b170-abb7493361c4: FIXED (C4). ECG -> required, in the stop rule; conditional echo/monitoring must; the
  antiplatelet must becomes "if no indication for anticoagulation is identified".
- 4bfc7ab6-e8ef-4efa-b328-c6167b5ca708: FIXED (C2). Battery -> recommended, out of the stop rule.
- Class: C11.

### VASC-DEM-S10 (approved: no)
- 4bc866bf-172d-435a-9dff-658aa4b6b7db: FIXED (C2). Battery -> recommended, out of the stop rule.
- Class: C6 (RAVLT 20th); C11.

### VASC-DEM-S11 (approved: no)
- 77ee2163-9fb5-4b05-875b-2365c0e8b65d: ALREADY-FIXED + CENTRAL (C5). `carotid_duplex` already required; MRA alternative added.
- ddd47148-a4fc-4453-add6-c575843cf168: FIXED (C12). Monitoring waste removed; optional prolonged-monitoring criterion with a
  stored 30-day monitor.
- db0cbe3b-2adb-49ce-b7c4-ebf05079cb37: FIXED + CENTRAL (C11). Labels and reorder for fu 0, 2, 4-7, 10.
- Class: C6 (RAVLT 22nd).

## 4. CENTRAL requests

1. **Review app** (web-review CaseDetail.tsx): show follow-ups that match no criterion in a separate
   block, "Answered on request (not part of the pathway)", after the pathway steps. Notes 74a16658,
   2f5910a5, 75e30bee, 57709b24, fa0764bd, dd0174a0, db0cbe3b. 3001 such follow-ups dataset-wide.
   CENTRAL.md items 2 (row key order: e8dbcb56, dc877a4d) and 3 (stop-rule ids without the argument:
   f569e1c8, 6331cc50, 2c6f29cf, f33e4140, 77ee2163) apply as written.
2. **Synonyms** (`diagnosis_synonyms.yaml`): for VASC-DEM-P02 only, accept "posterior cortical atrophy
   small vessel disease", "alzheimer small vessel disease" and "alzheimers small vessel disease"
   (88d4951c). Check them under scorer v2 against the P02 rejected list and AD-only answers, then
   re-apply with `--prune --conditions vascular_dementia`. Label changes (`accepted[0]` only, entity
   and codes unchanged): M01, M02, M06, M10, P06, P08, S08 (D8).
3. **Library**: none needed. Stored reports are kept wherever the library normal would contradict
   the patient.
4. **Criteria pack** (`dataset-generation/criteria_packs/VASC-DEM.md`, close-out):
   - s.2 tiers per D1-D4. Gait is never required. The battery is recommended, required only when
     the screen is normal (P07). Amyloid is recommended, optional in M08. FDG in P02 is optional.
     NOTCH3 is required only in P05. The ECG is required after an infarct with no rhythm assessment,
     plus cervical imaging if recent. Carotid criteria take duplex or MRA.
   - s.3: EEG is optional with TFNE (P03). Monitoring is optional where the mechanism is uncertain
     (S11). Add the on-request study table (C11).
   - s.4 and s.7: delete "no triptans or ergots in CADASIL" (EAN 2020); delete the BP 120 floor; add
     the LV thrombus DOAC option, the device-detected AF rule and the flutter-ablation
     reassessment; reword carotid timing as eligibility assessment.
   - s.1: VasCog-2-WSO concordance; AACN score labels.
   - Allow-list `[VasCog2_WSO_2025]`, `[AACN_labels_2020]`, `[AHA_LV_thrombus_2022]`,
     `[HRS_MRI_CIED_2017]`, `[EAN_monogenic_SVD_2020]`, `[NICE_CG115]` with the references in the
     decisions file.
5. **Review-app guidance** (`condition_tool_guidance.yaml`): VASC-DEM has no entries (October s.4).
   Nothing to answer.
6. **Guard suggestion** (tests): a stored follow-up whose study is invasive (`electrophysiology_study`,
   `cerebral_angiography`, `coronary_angiography`, `levodopa_challenge`) and that matches no criterion
   carries an avoided label. Dataset-wide unlabelled counts: 25, 62, 15 and 151.
7. **Cross-condition** (ALZ-EARLY; the other leads): 57 ALZ-EARLY percentile rows in the 9th-24th band
   are flagged "yes" against the 25th-75th range, which ALZ kept at R1's own request (c23ae468).
   VASC-DEM adopts the AACN labels (D6). One convention across the dementia conditions should be
   chosen centrally.

## 5. Open questions

- None that only Andrea can settle. Two items for the re-review, decided here:
  - P07 keeps the battery required against the class rule (D2).
  - P08 keeps MRI as harm with R1's conditional rationale (D13).
- M09 e8dbcb56 ("48° false??") was ruled on the most likely reading, a flag read off the next row
  (D15). If Andrea can ask R1, confirm that the note did not mean something else about the naming
  test.
- Cross-condition percentile convention (CENTRAL 7).

## 6. Checks for workers

After each case:
- `uv run python -I data/review/round-2026-11/bin/perfect_agent.py <id> -v`: pass. Every required
  and recommended criterion is served by a case output. No new avoided label matches a criterion
  alternative.
- `uv run python -I data/review/round-2026-11/bin/case_io.py check <id>`.
- If the MRI was edited (C7), run mri_probe.py.
- Grep the case for the old wording after each text class (C6 "impaired" for 9th-24th scores, C8
  "sufficient", C10 "120").

<!-- PLAN COMPLETE -->
