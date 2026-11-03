# Library contradictions, group 2: ALZ-EARLY, FTD, ISCH-STR, NMDAR-ENC, SE (25 Oct 2026)

Brief: `data/review/round-2026-10/LIBRARY_CONTRADICTIONS_BRIEF.md`. Map:
`data/review/round-2026-10/plans/LIBRARY-group2-map.yaml`. 1266 case-specific reports in all 150
cases (ALZ-EARLY 121, FTD 75, ISCH-STR 327, NMDAR-ENC 395, SE 348), written through `case_io.py`
as follow-ups (discriminated studies) or case fallback panels (labs). Each case log has a
"Library contradictions (25 Oct 2026)" section listing every report with its reason.

Checks after the last edit:
- Map verifier: 1291 listed (case, term) pairs, 0 answered by the library.
- Served-answer diff against HEAD over every advertised order (all enum values, labs panel by
  panel, CSF special tests): in all 150 cases the only changed answers are the new
  library-to-case ones ("other changed answers: 0"). No tier, criterion, diagnosis or stored
  output changed.
- `perfect_agent.py`: 150/150 pass. `test_case_guards.py -k <condition>`: 240 passed per condition.
- Lab prose: each new panel carries one sentence without semicolons, so a panel ordered alone
  receives only its own sentence.

Not done here: merging the map into `agent-platform/config/tools/library_contradictions.yaml`
(left to the coordinator), and the library defects noted under "Central".

## Central (library defects seen in every condition)
- `labs:AED_levels` reports six antiseizure drugs as therapeutic, and `labs:valproate_level` and
  `labs:lithium_level` report therapeutic levels, in patients who take none of them. Fixed here
  only where the condition makes the order likely (NMDAR-ENC, SE; lithium also NMDAR-ENC-P07); in
  ALZ-EARLY, FTD and ISCH-STR they are still library-answered. Better fixed once in the library
  (report "not detected" unless the case lists the drug).
- `order_cardiac_monitoring device_interrogation` describes a device in patients without one.
  Only SE-M07 (who has a device-related history) got a case report.
- `order_body_imaging chest_CT` with no chest-CT follow-up is served by a stored
  chest-abdomen-pelvis follow-up (ISCH-STR RP02 and RS04 now answer a chest CT with the CAP
  report of the gravid uterus; its chest rows are normal). Routing behaviour, not a contradiction.
- `obtain_tissue_diagnosis` does not route on `site`: any resection order gets the stored resection.

## ALZ-EARLY (30 cases; 121 reports)
### Terms judged contradictory, every case (`all_cases`)
- `tau_PET`: early-onset AD with positive amyloid biomarkers; a normal tau PET contradicts the
  stored biomarkers. Reports follow the stored FDG-PET distribution (Braak-pattern temporoparietal
  uptake); the two low-positive amyloid MCI cases (M01, S06) get borderline-positive tau.
- `perfusion_SPECT`: hypoperfusion matching the stored FDG hypometabolism (RP03 stores its own).
- `speech_language_evaluation`: the stored neuropsychology documents anomia and reduced fluency;
  the library reports normal language (P02 stores its own).
### In some cases (`cases`)
- `performance_status` (24 dementia-stage cases): Karnofsky 70/ECOG 1 (60/2 rapidly
  progressive). Left to the library in the MCI cases M01-M04, RM04 and S06, which document
  preserved independence, so Karnofsky 100 is not contradicted (doubt: some MCI reviewers score 90).
- `gait_and_balance_timed` (M05, RP05, RS02, RS04): the examined gait abnormality.
- History: pelvis ultrasound states hysterectomy/BSO or cholecystectomy (RP01, RS04); M04
  anti-parietal-cell and anti-intrinsic-factor positive (atrophic gastritis with B12 deficiency);
  RP03 perimetry matching the bilateral lower-quadrant defect on confrontation.

## FTD (30 cases; 75 reports)
### `all_cases`
- `performance_status`: every case documents functional decline; the library gives Karnofsky 100.
- `speech_language_evaluation`: reduced verbal fluency and naming as in the stored neuropsychology
  (S11, S12 store their own).
### `cases`
- `gait_and_balance_timed` (M03, M07, P04, P08, S01, S04, S07, S09): parkinsonian or other
  examined gait abnormality.
- `labs:CDT` raised (S01, S05, S09: escalating daily drinking); `labs:HbA1c` (S01, S05: type 2
  diabetes on metformin); P03 RF and anti-CCP positive (treated rheumatoid arthritis);
  S07 low plasma progranulin (stored pathogenic GRN variant).

## ISCH-STR (30 cases; 327 reports)
### `all_cases`
- `performance_status`: every case has an acute deficit; Karnofsky 100/ECOG 0 contradicts the
  exam. Scores from the exam: 20/4 (RP01, RS04 obtunded), 30/4 (unable to walk), 50/3 (walks with
  assistance: P02, RS03, S06, M04), 60/2 (M01-M03, P01, RM04, RP05), 70/1 (P05, RM01, RP02, RP04),
  90/0 (RM02, RM03).
### `cases`
- Vessel imaging (`MR_angiography` where not stored, `cerebral_angiography`, `carotid_duplex`,
  `transcranial_doppler`): the library reports normal vessels while the stored CTA (RP02: MRA)
  shows the occlusion, stenosis, dissection or moyamoya. Reports mirror the stored lesion; duplex
  gives velocities consistent with its grade, TCD only for intracranial or haemodynamically
  significant lesions. Left to the library where the stored CTA is normal or shows nothing
  relevant (P03, RP03, RP04, RP05, S06).
- Perfusion (`CT_perfusion` where not stored, `perfusion_MRI`): a deficit in the infarct
  territory of the stored MRI, qualitative (core and Tmax regions, no invented volumes); perfusion
  MRI copies the stored CTP in M01-M03, P04, P05. Left to the library in M04, P01, RM02-RM04,
  RP05, S06 (small, old or no infarct; doubt).
- Heart (`TEE`, `bubble_study`, `TTE`, `cardiac_MRI`): 19 cases whose stored echo shows LV
  hypertrophy, atrial dilatation, reduced EF, valve disease, PFO or vegetation; the library
  reports a normal heart. Reports repeat the stored structure; PFO with shunt in P01 (with atrial
  septal aneurysm) and RP01; P03 bicuspid valve with mobile vegetation on cardiac MRI; S03 dense
  spontaneous echo contrast in the appendage, no thrombus; RS02 TTE from the stored TEE.
- RM01 `continuous_icu`, `video`, `ambulatory` EEG: mirror the stored abnormal routine EEG (left
  frontocentral delta, sharp transients), no events.
- Bedside: `gait_and_balance_timed` abnormal (11 cases) or not testable (14); cognitive screen
  (19), neuropsychological battery (abbreviated impaired battery in P05, RP04, RP05, RS05; not
  completed in acutely aphasic or inattentive cases), speech-language evaluation (19, RS04 not
  testable), perimetry (P04, P05, RS01, RS03, S02, S03, S04) matching the documented deficits.
- Pregnancy: RP02 (18 weeks) and RS04 (15 weeks) get a positive beta-hCG and abdominal-pelvic
  imaging showing the gravid uterus. Thoracic surgery: RS02 (sternotomy, aortic arch graft, the
  left carotid dissection flap) and RS03 (oesophagectomy with gastric conduit, jejunostomy) chest
  and abdominal imaging.

## NMDAR-ENC (30 cases; 395 reports)
### `all_cases`
- `FDG_PET` (frontotemporal hypermetabolism, parieto-occipital hypometabolism, lateralised as the
  stored MRI/EEG), `ambulatory` EEG (mirrors the stored continuous EEG, no video),
  `cognitive_screen` baseline and `post_intervention` (impaired, persisting during admission),
  `neuropsych_battery` (not completable or impaired), `performance_status` (dependency documented),
  `valproate_level` and `AED_levels` (only the drugs the patient takes; others not detected).
### `cases`
- `speech_language_evaluation` (29; P01 has normal speech and is left to the library),
  `gait_and_balance_timed` (27; P01, P04, RP01 have a normal stored gait).
- Teratoma cases: whole-body PET, pelvic CT/MRI, CAP CT and resection pathology show the
  teratoma on the stored ultrasound (16-18 cases).
- Chronic lesions: P03, RP02, RP03 head CT; P03, RP03 MRS and perfusion MRI of the
  encephalomalacia. RP02 lung mass on chest imaging, benzodiazepines on the tox screen;
  RP03 coronary stent on coronary angiography/CTA and HbA1c 6.3%; P07 prolactin raised on
  risperidone and lithium not detected; RS02 SARS-CoV-2 on throat swab; RS04 VEP and perimetry
  abnormal (bilateral visual loss).

## SE (30 cases; 348 reports)
### `all_cases`
- `ambulatory` EEG (mirrors the stored continuous EEG, video wording removed), `performance_status`
  (Karnofsky 20-30, ECOG 4), `gait_and_balance_timed`, `cognitive_screen`, `neuropsych_battery`,
  `speech_language_evaluation` (not testable while intubated or post-ictal; observed state from
  the exam), `lithium_level` (not detected), `valproate_level` and `AED_levels` (arrival sample:
  only the drugs the patient takes).
### `cases`
- Cognitive screen `post_intervention` (M04, M09, P06, P03, M07); P02 `functional_neuro_signs`
  positive; HbA1c (M01, M02, M04, M06, S03, S11); ANA positive (M03, S04); S08 beta-hCG (28
  weeks); P08 IGRA positive.
- Structural causes: brain FDG-PET (13 cases), perfusion MRI and MRS, FET-PET (S07), amyloid and
  tau PET and perfusion SPECT (M09), CTP (P04); biopsy or resection pathology for GBM (M02, S07),
  toxoplasmosis (M08), HSV (M06), prion disease (P06); M05 whole-body PET and ovarian teratoma
  resection; M01, P01 chest imaging; abdominal imaging P07 (cirrhosis), S11 (small kidneys), S08
  (gravid uterus), P01 (steatosis); cardiac: TEE/bubble (M07, P03, M09), cardiac MRI, coronary
  imaging and chest radiograph (M07, P03), M07 device interrogation.

## Terms left to the library on purpose
Normal or not contradicted by the case: CK, prolactin and tox screens in SE except where
documented; CSF in cases without stored CSF; cooperation-dependent tests (audiometry, spirometry,
exercise tests) in the acutely ill; exercise echo (ISCH-STR); lymph node biopsy; most immunology
and genetic panels with no positive history; AED, valproate and lithium levels in ALZ-EARLY, FTD
and ISCH-STR (library defect, Central).

## Doubts for the physicians
- SE: AED levels assume an arrival sample before ED loading doses; CK, prolactin, tox screen
  (EMS benzodiazepines) left normal; ictal perfusion/FDG changes in cases without a structural
  lesion (e.g. S02, S09 hippocampal sclerosis) left to the library; P05 organophosphate EMG/RNS
  left to the library; S11 urinalysis left normal despite small kidneys; coronary findings for M07,
  P03 and FDG/perfusion patterns are inferred, not stored.
- ISCH-STR: perfusion left normal in M04, P01, RM02-RM04, RP05, S06; RS04 bubble study and the
  cases without stored PFO answered "no shunt"; duplex velocities, TCD and cardiac MRI values are
  inferred from the stored CTA/echo grades; neuropsychology "not completed" in mildly impaired
  acute cases (M01-M03) could be argued either way; KPS scores are bedside estimates; beta-hCG
  values (24800 at 18 weeks, 41200 at 15 weeks) are typical, not stored; CDT in RP01 left normal.
- NMDAR-ENC: FDG pattern inferred from the stored MRI/EEG; lithium fixed only in P07.
- ALZ-EARLY: performance status left at Karnofsky 100 in six MCI cases; tau PET distribution
  inferred from the stored FDG-PET.
- FTD: CDT raised only where heavy drinking is documented.

## Per case (reports added; full reasons in each case log)

### ALZ-EARLY
- M01 (3): tau_PET, perfusion_SPECT, speech_language_evaluation
- M02 (3): tau_PET, perfusion_SPECT, speech_language_evaluation
- M03 (3): tau_PET, perfusion_SPECT, speech_language_evaluation
- M04 (5): tau_PET, perfusion_SPECT, speech_language_evaluation, labs anti_parietal_cell, labs anti_intrinsic_factor
- M05 (5): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status, gait_and_balance_timed
- P01 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- P02 (3): tau_PET, perfusion_SPECT, performance_status
- P03 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- P04 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- RM01 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- RM02 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- RM03 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- RM04 (3): tau_PET, perfusion_SPECT, speech_language_evaluation
- RP01 (5): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status, pelvis_abdomen_ultrasound
- RP02 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- RP03 (4): tau_PET, speech_language_evaluation, performance_status, visual_field_perimetry
- RP04 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- RP05 (5): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status, gait_and_balance_timed
- RS01 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- RS02 (5): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status, gait_and_balance_timed
- RS03 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- RS04 (6): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status, gait_and_balance_timed, pelvis_abdomen_ultrasound
- RS05 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- RS06 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- S01 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- S02 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- S03 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- S04 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- S05 (4): tau_PET, perfusion_SPECT, speech_language_evaluation, performance_status
- S06 (3): tau_PET, perfusion_SPECT, speech_language_evaluation

### FTD
- M01 (2): speech_language_evaluation, performance_status
- M02 (2): speech_language_evaluation, performance_status
- M03 (3): speech_language_evaluation, performance_status, gait_and_balance_timed
- M04 (2): speech_language_evaluation, performance_status
- M05 (2): speech_language_evaluation, performance_status
- M06 (2): speech_language_evaluation, performance_status
- M07 (3): speech_language_evaluation, performance_status, gait_and_balance_timed
- M08 (2): speech_language_evaluation, performance_status
- M09 (2): speech_language_evaluation, performance_status
- M10 (2): speech_language_evaluation, performance_status
- P01 (2): speech_language_evaluation, performance_status
- P02 (2): speech_language_evaluation, performance_status
- P03 (5): speech_language_evaluation, performance_status, labs RF, labs anti_CCP, labs autoimmune_basic
- P04 (3): speech_language_evaluation, performance_status, gait_and_balance_timed
- P05 (2): speech_language_evaluation, performance_status
- P06 (2): speech_language_evaluation, performance_status
- P07 (2): speech_language_evaluation, performance_status
- P08 (3): speech_language_evaluation, performance_status, gait_and_balance_timed
- S01 (5): speech_language_evaluation, performance_status, gait_and_balance_timed, labs CDT, labs HbA1c
- S02 (2): speech_language_evaluation, performance_status
- S03 (2): speech_language_evaluation, performance_status
- S04 (3): speech_language_evaluation, performance_status, gait_and_balance_timed
- S05 (4): speech_language_evaluation, performance_status, labs CDT, labs HbA1c
- S06 (2): speech_language_evaluation, performance_status
- S07 (4): speech_language_evaluation, performance_status, gait_and_balance_timed, labs plasma_progranulin
- S08 (2): speech_language_evaluation, performance_status
- S09 (4): speech_language_evaluation, performance_status, gait_and_balance_timed, labs CDT
- S10 (2): speech_language_evaluation, performance_status
- S11 (1): performance_status
- S12 (1): performance_status

### ISCH-STR
- M01 (12): MR_angiography, cerebral_angiography, carotid_duplex, perfusion_MRI, TEE, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation
- M02 (13): MR_angiography, cerebral_angiography, carotid_duplex, transcranial_doppler, perfusion_MRI, TEE, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation
- M03 (12): MR_angiography, cerebral_angiography, carotid_duplex, perfusion_MRI, TEE, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation
- M04 (6): MR_angiography, cerebral_angiography, carotid_duplex, performance_status, gait_and_balance_timed, speech_language_evaluation
- M05 (11): MR_angiography, cerebral_angiography, carotid_duplex, transcranial_doppler, CT_perfusion, perfusion_MRI, TEE, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed
- P01 (8): MR_angiography, cerebral_angiography, carotid_duplex, TEE, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed
- P02 (11): MR_angiography, cerebral_angiography, carotid_duplex, transcranial_doppler, CT_perfusion, perfusion_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation
- P03 (6): CT_perfusion, perfusion_MRI, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed
- P04 (12): MR_angiography, cerebral_angiography, transcranial_doppler, perfusion_MRI, TEE, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, visual_field_perimetry
- P05 (7): MR_angiography, cerebral_angiography, perfusion_MRI, performance_status, neuropsych_battery, speech_language_evaluation, visual_field_perimetry
- RM01 (11): MR_angiography, cerebral_angiography, carotid_duplex, transcranial_doppler, CT_perfusion, perfusion_MRI, continuous_icu, video, ambulatory, performance_status, speech_language_evaluation
- RM02 (7): MR_angiography, cerebral_angiography, carotid_duplex, TEE, bubble_study, cardiac_MRI, performance_status
- RM03 (5): MR_angiography, cerebral_angiography, carotid_duplex, transcranial_doppler, performance_status
- RM04 (6): MR_angiography, cerebral_angiography, carotid_duplex, transcranial_doppler, performance_status, gait_and_balance_timed
- RP01 (14): MR_angiography, cerebral_angiography, carotid_duplex, transcranial_doppler, CT_perfusion, perfusion_MRI, TEE, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation
- RP02 (12): cerebral_angiography, carotid_duplex, transcranial_doppler, CT_perfusion, perfusion_MRI, performance_status, speech_language_evaluation, labs beta-hCG, pelvis_abdomen_ultrasound, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT
- RP03 (7): CT_perfusion, perfusion_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation
- RP04 (7): CT_perfusion, perfusion_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation
- RP05 (5): performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation
- RS01 (15): MR_angiography, cerebral_angiography, carotid_duplex, transcranial_doppler, CT_perfusion, perfusion_MRI, TEE, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, visual_field_perimetry
- RS02 (17): MR_angiography, cerebral_angiography, carotid_duplex, transcranial_doppler, CT_perfusion, perfusion_MRI, bubble_study, TTE, cardiac_MRI, performance_status, gait_and_balance_timed, speech_language_evaluation, chest_xray, chest_CT, chest_abdomen_pelvis_CT, mediastinum_CT, chest_CTA
- RS03 (18): MR_angiography, cerebral_angiography, CT_perfusion, perfusion_MRI, TEE, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, visual_field_perimetry, chest_xray, chest_CT, chest_abdomen_pelvis_CT, mediastinum_CT, pelvis_abdomen_CT
- RS04 (16): MR_angiography, cerebral_angiography, carotid_duplex, transcranial_doppler, CT_perfusion, perfusion_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs beta-hCG, pelvis_abdomen_ultrasound, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT
- RS05 (12): MR_angiography, cerebral_angiography, transcranial_doppler, CT_perfusion, perfusion_MRI, TEE, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery
- S01 (14): MR_angiography, cerebral_angiography, carotid_duplex, transcranial_doppler, CT_perfusion, perfusion_MRI, TEE, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation
- S02 (15): MR_angiography, cerebral_angiography, carotid_duplex, transcranial_doppler, CT_perfusion, perfusion_MRI, TEE, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, visual_field_perimetry
- S03 (15): MR_angiography, cerebral_angiography, carotid_duplex, transcranial_doppler, CT_perfusion, perfusion_MRI, TEE, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, visual_field_perimetry
- S04 (15): MR_angiography, cerebral_angiography, carotid_duplex, transcranial_doppler, CT_perfusion, perfusion_MRI, TEE, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, visual_field_perimetry
- S05 (13): MR_angiography, cerebral_angiography, carotid_duplex, transcranial_doppler, CT_perfusion, perfusion_MRI, TEE, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery
- S06 (5): TEE, bubble_study, cardiac_MRI, performance_status, gait_and_balance_timed

### NMDAR-ENC
- M01 (15): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs AED_levels, labs valproate_level
- M02 (10): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, labs AED_levels, labs valproate_level
- M03 (14): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, pelvis_abdomen_CT, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs AED_levels, labs valproate_level
- M04 (15): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs AED_levels, labs valproate_level
- M05 (10): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, labs AED_levels, labs valproate_level
- P01 (13): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs AED_levels, labs valproate_level
- P02 (11): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, resection, labs AED_levels, labs valproate_level
- P03 (12): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, order_ct_scan, MR_spectroscopy, perfusion_MRI, labs valproate_level
- P04 (14): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, speech_language_evaluation, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs AED_levels, labs valproate_level
- P05 (10): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, labs AED_levels, labs valproate_level
- P06 (15): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs AED_levels, labs valproate_level
- P07 (16): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs prolactin, labs lithium_level, labs valproate_level
- P08 (15): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs AED_levels, labs valproate_level
- RM01 (10): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, labs AED_levels, labs valproate_level
- RM02 (15): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs AED_levels, labs valproate_level
- RM03 (10): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, labs AED_levels, labs valproate_level
- RP01 (9): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, speech_language_evaluation, labs AED_levels, labs valproate_level
- RP02 (15): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, order_ct_scan, chest_xray, mediastinum_CT, chest_CTA, whole_body_FDG_PET, labs tox_screen, labs valproate_level
- RP03 (15): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, order_ct_scan, MR_spectroscopy, perfusion_MRI, coronary_angiography, coronary_CTA, labs HbA1c, labs valproate_level
- RS01 (15): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs AED_levels, labs valproate_level
- RS02 (9): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, throat_swab
- RS03 (10): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, labs AED_levels, labs valproate_level
- RS04 (12): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, vep, visual_field_perimetry, labs AED_levels, labs valproate_level
- S01 (15): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs AED_levels, labs valproate_level
- S02 (15): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs AED_levels, labs valproate_level
- S03 (15): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs AED_levels, labs valproate_level
- S04 (15): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs AED_levels, labs valproate_level
- S06 (15): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs AED_levels, labs valproate_level
- S09 (15): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs AED_levels, labs valproate_level
- S10 (15): FDG_PET, ambulatory, cognitive_screen, cognitive_screen post_intervention, neuropsych_battery, performance_status, gait_and_balance_timed, speech_language_evaluation, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT, whole_body_FDG_PET, resection, labs AED_levels, labs valproate_level

### SE
- M01 (15): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs AED_levels, labs valproate_level, labs HbA1c, FDG_PET, chest_xray, mediastinum_CT, chest_CTA, whole_body_FDG_PET
- M02 (14): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs valproate_level, labs HbA1c, FDG_PET, MR_spectroscopy, stereotactic_biopsy, open_biopsy, resection
- M03 (9): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs valproate_level, labs ANA
- M04 (12): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, cognitive_screen post_intervention, labs lithium_level, labs valproate_level, labs HbA1c, FDG_PET, perfusion_MRI
- M05 (12): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs AED_levels, labs valproate_level, FDG_PET, whole_body_FDG_PET, resection
- M06 (13): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs AED_levels, labs valproate_level, labs HbA1c, FDG_PET, stereotactic_biopsy, open_biopsy
- M07 (17): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, cognitive_screen post_intervention, labs lithium_level, labs AED_levels, labs valproate_level, TEE, bubble_study, cardiac_MRI, coronary_angiography, coronary_CTA, chest_xray, device_interrogation
- M08 (14): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs AED_levels, labs valproate_level, FDG_PET, perfusion_MRI, MR_spectroscopy, stereotactic_biopsy, open_biopsy
- M09 (16): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, cognitive_screen post_intervention, labs lithium_level, labs AED_levels, labs valproate_level, FDG_PET, amyloid_PET, tau_PET, perfusion_SPECT, TEE, bubble_study
- P01 (15): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs AED_levels, labs valproate_level, chest_xray, mediastinum_CT, chest_CTA, whole_body_FDG_PET, pelvis_abdomen_ultrasound, pelvis_abdomen_MRI
- P02 (9): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, functional_neuro_signs, labs lithium_level, labs valproate_level
- P03 (17): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, cognitive_screen post_intervention, labs lithium_level, labs AED_levels, labs valproate_level, FDG_PET, TEE, bubble_study, cardiac_MRI, coronary_angiography, coronary_CTA, chest_xray
- P04 (12): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs AED_levels, labs valproate_level, FDG_PET, perfusion_MRI, CT_perfusion
- P05 (9): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs AED_levels, labs valproate_level
- P06 (13): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, cognitive_screen post_intervention, labs lithium_level, labs AED_levels, labs valproate_level, FDG_PET, stereotactic_biopsy, open_biopsy
- P07 (13): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs AED_levels, labs valproate_level, pelvis_abdomen_ultrasound, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT
- P08 (10): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs AED_levels, labs valproate_level, labs IGRA
- RS11 (8): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs valproate_level
- S01 (7): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level
- S02 (8): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs valproate_level
- S03 (11): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs valproate_level, labs HbA1c, FDG_PET, perfusion_MRI
- S04 (8): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs ANA
- S05 (9): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs AED_levels, labs valproate_level
- S06 (9): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs AED_levels, labs valproate_level
- S07 (15): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs valproate_level, FDG_PET, perfusion_MRI, MR_spectroscopy, amino_acid_PET, stereotactic_biopsy, open_biopsy, resection
- S08 (13): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs valproate_level, labs beta-hCG, pelvis_abdomen_ultrasound, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT
- S09 (8): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs valproate_level
- S10 (9): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs AED_levels, labs valproate_level
- S11 (14): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs AED_levels, labs valproate_level, labs HbA1c, pelvis_abdomen_ultrasound, pelvis_abdomen_CT, pelvis_abdomen_MRI, chest_abdomen_pelvis_CT
- S12 (9): ambulatory, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, speech_language_evaluation, labs lithium_level, labs valproate_level, FDG_PET
