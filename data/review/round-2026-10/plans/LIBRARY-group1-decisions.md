# Library contradictions, group 1: ALS, FND, HEP-ENC, MS-RR, SAH (25 Oct 2026)

Brief: `data/review/round-2026-10/LIBRARY_CONTRADICTIONS_BRIEF.md`. Map:
`data/review/round-2026-10/plans/LIBRARY-group1-map.yaml`. 1016 case-specific reports in 145 of
the 150 cases (ALS 194, FND 94, HEP-ENC 383, MS-RR 96, SAH 249); MS-RR P01, P02, P03, RM03 and
RS04 needed none. Each changed case log has a "Library contradictions (25 Oct 2026)" section.

Checks after the last edit:
- The map verifier: every listed (case, term) is answered without the library (0 problems).
- `perfect_agent.py`: 150/150 pass.
- `test_case_guards.py -k <group>`: 1260 passed.
- Snapshot of every criterion's served answer: unchanged in ALS, HEP-ENC, MS-RR and SAH. In FND only
  `action-neuropsych-battery` changed in 28 cases. That criterion was answered by the library normal,
  which was the contradiction being fixed; the new report matches its expected evidence (FND section).
- Lab prose: every case fallback lab panel ordered alone receives only its own sentence. The HEP-ENC
  peripheral-smear sentence was rewritten as one sentence headed `Peripheral blood smear:` (commas,
  no semicolons or inner full stop), because `cut_prose` kept its fragments in single-panel orders
  for other assays. The ALS genetic and anti-CCP sentences now name their exact row tests.

Not done here: merging this map into `agent-platform/config/tools/library_contradictions.yaml`
(the guard's input), which is left to the coordinator.

Serving observation (HEP-ENC): `perform_clinical_assessment` with `assessment_type`
neuropsych_battery or speech_language_evaluation is out of vocabulary (they are
`order_specialized_test` terms); a direct MockServer call answers it with the cognitive-screen
report. `BaseTool` validation rejects such an order upstream, so the agent never sees it.

## ALS (30 cases; 194 reports in 30 cases)

28 cases are ALS. Two are excluded from `all_cases` (`except`):
- P02: thyrotoxicosis from levothyroxine over-replacement in a C9orf72 carrier, ALS criteria not met.
- P08: SOD1 carrier who does not meet the criteria.
For both, a normal single-fibre EMG, muscle biopsy and CSF neurofilament is the right answer.

### Terms judged contradictory, every ALS case (`all_cases`)
- `analyze_csf special_tests=[NfL]` and `[NfH]`. Raised CSF neurofilament light and phosphorylated
  heavy chain are characteristic of ALS; the library reports them normal. A case fallback CSF
  (normal cells, protein, glucose and OCB, raised NfL and pNfH) now covers 23 cases. M04, M08, P03,
  P05 and P06 already store a CSF that does not mention neurofilaments; it was left unchanged
  (never change another output), so those cases answer from their stored CSF, not the library.
- `order_specialized_test test_type=emg_single_fiber`. Reinnervation in ALS raises fibre density
  and jitter; the library reports normal jitter. Reports give raised fibre density, jitter and
  blocking in EDC, with mildly abnormal frontalis in the bulbar-onset cases.
- `order_specialized_test test_type=muscle_biopsy`. Neurogenic grouped atrophy and fibre-type
  grouping, no inflammation; the library reports normal muscle.
- `perform_clinical_assessment assessment_type=performance_status`. The library gives Karnofsky
  100 / ECOG 0; every ALS case documents disability. Scores derived from the history. P02 (KPS 90,
  ECOG 1) and P08 (KPS 90, ECOG 0) also store one, listed per case.

### Terms judged contradictory in some cases (`cases`)
- `perform_clinical_assessment gait_and_balance_timed` (23 cases with an abnormal stored gait:
  M01, M03, M04, M05, M08, P03, P05, P06, P07, P09, RM11, RS11, S01-S11): slowed timed walk and
  TUG matching the stored weakness and spasticity.
- `order_specialized_test speech_language_evaluation` (M01, M03, M06, M08, P09, RS11, S02, S04,
  S06, S09: the bulbar cases): mixed spastic-flaccid dysarthria as the exam stores it.
- `order_advanced_imaging DTI_tractography` (26 cases whose stored MRI shows corticospinal tract
  T2 hyperintensity; not P01, P02, P04, P08): reduced corticospinal FA. A normal DTI would
  contradict the stored MRI.
- `order_body_imaging spine_CT` (M01, M05, M07, RM11): the spondylosis the stored spine MRI shows.
- `order_specialized_test polysomnography` (M02, M07): obstructive sleep apnoea in the history.
- `interpret_labs HbA1c` (diabetes on treatment): M02 6.8%, M05 6.6%, RM11 6.9%, S06 7.6%.
- `interpret_labs RF` 96 IU/mL and `anti_CCP` 168 U/mL in M06 (seropositive rheumatoid arthritis).
- `interpret_labs TRAb` 3.9 IU/L in P02 (residual Graves activity, consistent with the stored TSI).
- `interpret_labs anti_JCV_antibody` index 2.4 in M08 (the history states it).
- `interpret_labs genetic` (C9orf72 expansion in P02, P09 and S10; SOD1 variant in P08) and `order_specialized_test
  genetic_panel:FTD` (P02, P09, S10: C9orf72 expansion), matching the stored ALS gene panel.
- P09 (ALS-FTD): `cognitive_screen` MoCA 18, `neuropsych_battery` behavioural-variant FTD profile,
  `FDG_PET` frontotemporal hypometabolism.
- S06 (diabetic neuropathy): `skin_biopsy_iencf` reduced distal IENFD, `nerve_biopsy` axonal loss.

### Terms left to the library on purpose
- RNS: a decrement occurs in only a subset of ALS patients, so a normal RNS is not a contradiction.
- MR spectroscopy, FDG-PET outside P09, levodopa challenge: not characteristic, or not expected abnormal.
- Spine CT in M02, M06, P01, P04, S11 (mild degenerative change only, consistent with a normal-for-age report).
- Body imaging after surgery or cancer, lipid panel on statins, venous duplex after a past DVT:
  a current normal is consistent with the history.
- NfL in M04, M08, P03, P05, P06: their stored CSF answers instead (see doubts).

### Doubts for the physicians
- The CSF fallback serves raised NfL/pNfH to any lumbar-puncture order in 23 cases (the CSF tool has
  no special-test discriminator). The stored CSFs of M04, M08, P03, P05, P06 omit neurofilaments.
- P08 exclusion: a symptomatic SOD1 carrier not meeting the criteria; check that normal
  single-fibre EMG and biopsy are right.
- KPS/ECOG and gait times are derived from the history, not recorded values.
- Whether DTI tractography is credible as a clinical test here (it is mostly a research tool).

## FND (30 cases; 94 reports in 30 cases)

All 30 cases have functional neurological disorder as the primary diagnosis, so there is no
condition-wide term (`all_cases: []`, no `except`). For FND a normal test is usually the right
answer; every contradiction below comes from the stored examination, the history or a comorbid
organic disease.

### Terms judged contradictory
- `perform_clinical_assessment assessment_type=gait_and_balance_timed` (25 cases: M01, M02, M03,
  M05, M09, P01, P07, P08, RM01, RM03, RP02, RP03, RS01, RS03, RS04, S01–S07, S09, S10, S11).
  The library reports TUG 9.1 s and Berg 56, but the stored exam documents dragging, astasia-abasia,
  wheelchair use or no weight-bearing. The reports give slow timed walks, or say the tests could not be
  completed in P01, RP02, RS01, S05 and S07. They record trial-to-trial variability (and a faster dual-task
  walk in M01, M02 and RM01) only where the exam documents inconsistency or a normal gait when the
  patient is distracted or unobserved; P07 and P08 report consistent trials. No report names FND.
- `perform_clinical_assessment assessment_type=performance_status` (26 cases: the gait set plus
  RS02, who stays in bed to avoid episodes). The library reports Karnofsky 100, ECOG 0 and working,
  but the histories document wheelchairs, inability to work and dependence. Scores: KPS 40/ECOG 3
  (RP02, RS01); KPS 50/ECOG 3 (P01, RS02, RS04, S04, S05, S07); KPS 60/ECOG 2 (M02, M03, RM01,
  S01, S02); KPS 80/ECOG 1 (S11); KPS 70/ECOG 2 for the rest.
- `order_specialized_test test_type=neuropsych_battery` (28 cases; not M06 or S07). The library line
  "no significant depressive or anxiety symptoms" contradicts the documented anxiety, depression,
  PTSD or trauma, dissociation and health anxiety. The reports keep cognition normal and
  performance validity passed. They give self-report scales from the history (GAD-7, PHQ-9, HADS,
  DES-II, PCL-5, PHQ-15, SHAI, SPIN, AUDIT in S09), with MoCA 26 and low-average speed and fluency in P07,
  and below-average speed, attention and executive scores in RM01 (schizophrenia). Stored as a follow-up.
- Comorbid organic disease, case-specific: listed below.

### Terms left to the library on purpose
- Routine, sleep-deprived, ambulatory and video EEG in the PNES cases other than M06: a normal
  interictal EEG is the expected result, and whether an event is captured is chance.
- Gait timing in M04, M06, RM02, RP01 and RS02 (normal or cautious gait without focal signs).
  Performance status in M04, M06, RM02 and RP01 (PNES only, normal function between events).
- Brain MRI in RP01 and S09 (head injury without lasting deficit). CDT in S09 (2-4 drinks a day;
  GGT already stored). RS02 CBC/eosinophils and ESR (treated EGPA, current activity unknown).
  OCT and visual field after retinal detachment (RP03, RS02). VEP, OCT, SSEP and spine MRI in M09:
  the spine criterion expects no new cord lesion, and the library's normal does not contradict
  established MS with no optic neuritis history stored.
- AED levels (library: therapeutic, consistent with the cases on AEDs). Cognitive screen except
  P07. Neuropsychology in M06 and S07 (no mood or anxiety history to contradict).

### Per case (besides gait / performance status / neuropsychology above)
- M05: `interpret_labs ANA` -> ANA 1:320 speckled (established SLE).
- M06: `analyze_eeg` routine (fallback slot; also answers sleep_deprived) and ambulatory
  (follow-up). Occasional right anterior temporal sharp-and-slow waves with right temporal theta, and
  no seizures or events, matching the stored video-EEG (about 6 discharges an hour, unchanged from the prior study).
- M09: `analyze_csf` (fallback) -> CSF-restricted OCB, IgG index 0.98, kFLC index 24.5, normal
  cells, protein and glucose, JCV PCR negative (8-year RRMS). `interpret_labs anti_JCV_antibody` ->
  positive, index 2.8 (the history states 2.8).
- P07 (known PD): levodopa challenge with MDS-UPDRS III 31 OFF and 17 ON, and the left action tremor
  unchanged; cognitive screen MoCA 26/30 (as the exam records); UPSIT 22/40; MIBG with delayed H/M 1.4.
- RM01: `interpret_labs prolactin` -> 58 ng/mL, random sample (on risperidone).
- RP03: EMG/NCS showing a moderate length-dependent axonal sensorimotor polyneuropathy; skin biopsy
  with distal IENFD 3.2/mm and normal proximal density (known diabetic neuropathy).
- RS02: HbA1c 7.6% (T2DM on metformin); EMG/NCS with a mild axonal polyneuropathy; skin biopsy with distal IENFD 4.8/mm.

### Snapshot
`snapshot.py diff FND` changes only `action-neuropsych-battery` (an optional criterion) in the 28
cases above. Its answer was the library normal, the very contradiction being fixed: "no mood or anxiety
symptoms" against a case built on anxiety, depression and trauma. The stored answer of every other
criterion is unchanged.

### Doubts for the physicians
- The scale of the Karnofsky/ECOG scores and the timed-gait numbers (invented values, chosen to fit
  each history).
- The neuropsych report now answers the optional criterion with mood and anxiety scales. Is that the
  profile its expected evidence asks for?
- RM01: is the raised prolactin a confounder for event classification? It is a random sample, not post-ictal.
- RS02: should the eosinophil count and ESR be case-specific (EGPA activity)?
- RP03 and RS02: is ophthalmic testing after retinal detachment worth a case-specific report?
- M06: the reports state there were no patient-marked events on ambulatory EEG. Should one functional
  event have been captured instead?

## HEP-ENC (30 cases)

All 30 cases are hepatic encephalopathy (HE) in cirrhosis. Several have a second process:
- P04: Wilson disease.
- P05: Wernicke encephalopathy.
- P06: non-convulsive status epilepticus (NCSE).
- P07: covert HE in a working patient, GCS 15, stored PHES -5.
- P08: a large spontaneous splenorenal shunt with preserved liver function.

None of these is a mimic that a normal result would fit, so `except` is empty. Reports were written by `$G1/HEP-ENC/gen_hep.py` and stored through `libfix.store` / `add_labs`. Tiers, criteria, diagnosis and existing outputs are untouched: the snapshot diff reports "changed: none".

### Terms judged contradictory, every case (`all_cases`)

1. **`perform_clinical_assessment` cognitive_screen.** Every case is encephalopathic. The library's MoCA 28/30 with full orientation is impossible.
   - Testable grade II cases (GCS 13-14, disoriented to time): MoCA 12-19/30, with points lost on attention, executive, recall and orientation items.
   - Grade III-IV or untestable cases: "could not be completed", stating the reason from the stored exam.
   - P07: 25/30, just below the cut-off.
2. **`perform_clinical_assessment` performance_status.** The library gives KPS 100 / ECOG 0.
   - Grade II: KPS 50 / ECOG 3 (P08: KPS 40).
   - Grade III: KPS 30 / ECOG 4.
   - Comatose (P06, S06): KPS 20.
   - P07: KPS 90 / ECOG 0.
3. **`order_specialized_test` neuropsych_battery.** The brief names neuropsychology in HE as characteristic.
   - Testable cases: slowed psychomotor speed, impaired attention and executive function, retrieval-type memory deficit, naming preserved.
   - Untestable cases: "not administered", with the reason.
   - P01 and P07 already store PHES batteries, which answer this term.
4. **`analyze_eeg` continuous_icu (also answers video) and ambulatory.** Every case stores an abnormal routine EEG.
   - The prolonged recordings copy its background and findings, keep the impression without "consistent with" wording, and add "persists throughout; no electrographic seizures" (and "no push-button events" for ambulatory).
   - P06: the NCSE pattern "present from the start of the recording". No treatment response was invented.
   - P07: stored as a 24-hour video-EEG.
   - S08: the sentence about jerks during the routine recording was dropped.
5. **`order_advanced_imaging` MR_spectroscopy.** This is the characteristic MRS pattern of HE: reduced mI/Cr and Cho/Cr, increased Glx, NAA preserved, no lactate. Severity is graded mild (P07), moderate (grade II) or marked (grade III-IV).
6. **`order_body_imaging` pelvis_abdomen ultrasound, CT and MRI, and chest_abdomen_pelvis_CT.** The library reports a normal liver and spleen with no ascites in patients with cirrhosis.
   - Each report gives cirrhotic morphology, spleen size (scaled to the stored platelet count), ascites as on the stored exam, known varices or a recanalized paraumbilical vein (caput medusae), and case features:
     - M02: treated 1.8 cm HCC with lipiodol.
     - M04: hepatomegaly and chronic pancreatitis.
     - M05: hepatomegaly and periportal nodes.
     - M06: TIPS.
     - M08: three HCC lesions, no venous invasion.
     - M10: iron overload.
     - P08: splenorenal shunt and 4 mm renal calculus.
     - S04: nodular hepatomegaly.
     - S05: segment VI HCC and right pyelonephritis.
     - S09: 2.1 cm segment V HCC.
     - S10: bariatric surgery.
   - Not stored where a study already exists: M06 and S05 have ultrasound; P08 has CT and MRI.
   - No CAP report is stored. The abdomen-pelvis CT (region `pelvis_abdomen`) answers the CAP order through `_body_study_matches`, verified for every case.
7. **`interpret_labs` peripheral_smear.** The stored platelet count is below 150 in all 30 cases, so the library's "adequate platelets" contradicts it. Each smear is written from the stored CBC: macrocytic when MCV > 100, target cells, neutrophilia (toxic granulation where an infection or alcoholic hepatitis is stored), reduced platelets.

### Terms judged contradictory in some cases (`cases`)

- **`perform_clinical_assessment` gait_and_balance_timed** and **`order_specialized_test` speech_language_evaluation**: all cases except P07, transcribed from the stored exam. P07's gait and speech are normal, so the library's reports fit.
- **HbA1c**, for treated or documented diabetes:

  | Case | HbA1c (%) |
  |---|---|
  | M01 | 6.9 |
  | M06 | 6.4 |
  | M07 | 7.2 |
  | M10 | 7.6 |
  | P08 | 6.6 |
  | P09 | 6.8 |
  | S02 | 7.0 |
  | S04 | 6.5 |
  | S07 | 7.8 |
  | S08 | 6.6 |
  | S09 | 7.1 |
  | S10 | 8.4 |

  The values are kept modest because cirrhosis and bleeding lower HbA1c. P07 already stores 7.4.
- **HCV antibody reactive**: M03 (SVR), S07 (untreated), S09 (SVR).
- **anti-HBc reactive**: S05 (HBV cirrhosis).
- **CDT elevated**, for heavy drinking in the last weeks: M04 3.6%, S01 2.9%, S04 3.2%, S08 3.1%, P02 2.4%.
- **Procalcitonin elevated**, for a stored bacterial infection: M02 0.9 (neutrocytic ascites), M09 1.4 (SBP with Gram-negative rods), S01 1.6, S03 4.8 (urosepsis), S05 6.2 (pyelonephritis).
- **ANA positive 1:160**: S11 (autoimmune hepatitis).
- **Ceruloplasmin low (15 mg/dL)**: M05. She has taken zinc for four months, with stored serum copper 68.
- **Polysomnography**: P07. Untreated OSA, CPAP worn 3.2 h per night, SpO2 below 90% for 18% of the night. Severe OSA (AHI 32) was stored.
- **analyze_brain_mri**: S08 and S10. Their only imaging is CT with mild atrophy. The MRI stores atrophy and subtle pallidal T1 hyperintensity, in the style of S11's MRI.

### Terms left to the library on purpose

- `cognitive_screen` with timing `post_intervention`: recovery after treatment is the expected course.
- Ascitic fluid microbiology in cases without stored ascites (M04-M06, P01, P02, P05, P07, P08): a non-SBP result fits.
- Procalcitonin in S02 and M08. Both are febrile with raised CRP, but every stored culture and ascitic count is negative.
- CDT in M02 (one day of drinking after six months sober), S03 (drinking two weeks ago) and S06 (binge after six months sober): a value near the cut-off is uncertain.
- AFP in M02 (treated HCC).
- Whole-body FDG-PET in M08 and P03.
- Urinalysis, ABG, vitamin D, ESR, chest imaging (only the chest_xray stored where a criterion needs it), echocardiography, orthostatic BP, levodopa challenge, other serologies and genetics: the library normal fits, or the case gives no ground for a specific value.

### Reports added per case (383 in total)

Every case gets these, unless noted:
- cognitive_screen, performance_status, cEEG and ambulatory EEG, MRS and peripheral smear;
- neuropsych_battery, except P01 and P07;
- gait and speech, except P07;
- abdominal US, CT and MRI, except as noted for M06, S05 and P08.

| Case | Reports | Additions |
|---|---|---|
| M01 | 13 | HbA1c |
| M02 | 13 | procalcitonin |
| M03 | 13 | HCV Ab |
| M04 | 13 | CDT |
| M05 | 13 | ceruloplasmin |
| M06 | 12 | HbA1c; no US |
| M07 | 13 | HbA1c |
| M08 | 12 | none |
| M09 | 13 | procalcitonin |
| M10 | 13 | HbA1c |
| P01 | 11 | no battery |
| P02 | 13 | CDT |
| P03 | 12 | none |
| P04 | 12 | none |
| P05 | 12 | none |
| P06 | 12 | none |
| P07 | 10 | video-EEG instead of cEEG; PSG; no gait, speech or battery |
| P08 | 11 | HbA1c; US only |
| P09 | 13 | HbA1c |
| S01 | 14 | CDT, procalcitonin |
| S02 | 13 | HbA1c |
| S03 | 13 | procalcitonin |
| S04 | 14 | HbA1c, CDT |
| S05 | 13 | anti-HBc, procalcitonin; no US |
| S06 | 12 | none |
| S07 | 14 | HbA1c, HCV Ab |
| S08 | 15 | HbA1c, CDT, brain MRI |
| S09 | 14 | HbA1c, HCV Ab |
| S10 | 14 | HbA1c, brain MRI |
| S11 | 13 | ANA |

### Doubts for the physicians

- **P03** (castration-resistant prostate cancer, PSA 18.4 on enzalutamide): the case does not say whether he has metastases. The abdominal CT and MRI state no lymphadenopathy and no focal bone lesion. Confirm, or add the metastatic sites.
- **S11**: ANA 1:160 in autoimmune hepatitis on azathioprine and prednisone. Titres may fall on treatment.
- **M02**: the MRI states no arterial enhancement or washout at the TACE site (a non-viable treated lesion). The CT leaves residual enhancement unassessable because of lipiodol. Confirm the intended HCC status.
- **M08**: HCC lesion sizes and segments are invented within BCLC B (beyond Milan, no vascular invasion). AFP rose from 1620 to 2840; whether the imaging should show progression is unstated.
- **S09**: the "small HCC within Milan" was given a size of 2.1 cm in segment V.
- **P06**: the ambulatory and continuous EEG copy the stored NCSE pattern "from the start of the recording". Any treatment response belongs to the pathway, not to the library fix.
- **Prolonged EEG in grade III-IV inpatients**: 48-hour ambulatory recordings are clinically implausible but are now answered consistently.
- **Library bug, not fixable here**: `perform_clinical_assessment` with `assessment_type` neuropsych_battery or speech_language_evaluation is out of vocabulary (they are `order_specialized_test` terms). A direct MockServer call returns the cognitive_screen MoCA report; `BaseTool` validation should stop such orders upstream.
- **Procalcitonin in S02 and M08**: left to the library (0.04) despite fever and CRP 52 and 38. Confirm.

## MS-RR (30 cases; 96 reports in 25 cases)

All 30 cases are relapsing-remitting MS, with no mimics, so the map has no `except` list and no term in `all_cases`. Every term below depends on the case. The criteria never use `perform_clinical_assessment` or SSEP. The VEP, OCT, MRS and perfusion criteria are answered by follow-ups that were already stored, and none of them changed (snapshot diff: none).

### Terms judged contradictory, and why

- **`order_specialized_test {test_type: visual_field_perimetry}`** (rule c). Each of these cases records a reduced acuity with an RAPD, or a homonymous field defect, in the affected eye. The library's full fields in both eyes contradict that. The mean deviation in each report is scaled to the stored acuity.
  - RM02 records a left homonymous hemianopia from its right parieto-occipital lesion, so its report shows a congruous left homonymous hemianopia.
  - RS01 has dense left amblyopia, so its report shows generalised depression.
- **`order_specialized_test {test_type: vep}`** (rule c).
  - P05 and RS02: prior right optic neuritis with residual signs, but no VEP stored. The reports show a delayed right P100.
  - RS01: amblyopia, so the report shows reduced amplitude with a normal latency.
- **`order_specialized_test {test_type: optical_coherence_tomography}`** (rule c). P05 and RS02 have temporal pallor after optic neuritis, so their reports show right RNFL and GCIPL thinning.
- **`order_specialized_test {test_type: ssep}`** (rule c). The library's normal SSEP contradicts cases where both of these are present:
  - the exam records a loss of vibration or joint position sense above the toe (ankle, knee, joint position sense);
  - the MRI stores a dorsal or dorsolateral cord lesion.

  The reports show the tibial P37 prolonged on that side, the lumbar N22 normal, and the median responses normal. The exception is RS06, whose left-hand sensory loss gives a left median N13-N20 delay. In the style of every evoked-potential report, they name the physiology and never MS.
- **`perform_clinical_assessment {assessment_type: gait_and_balance_timed}`** and **`{assessment_type: performance_status}`** (rule d). These are inpatient relapses with a gait disorder recorded in the exam. The library reports a TUG of 8 s and Karnofsky 100 / ECOG 0, which these cases contradict.
  - Most cases: Karnofsky 80 / ECOG 1.
  - Supervised walkers: Karnofsky 70 / ECOG 2.
  - RP03 (GCS 8, quadriparetic, in the ICU): Karnofsky 20 / ECOG 4, and gait cannot be tested.
  - `timing` is left empty, so the baseline and post_intervention orders both receive the report.
- **`analyze_eeg {eeg_type: video | ambulatory | continuous_icu}`** (rule c). RM01 and RP03 store an abnormal routine EEG with continuous slowing. A longer recording cannot have a normal background. In RP03 the cICU report also answers a video-EEG order (same study).
- **`order_advanced_imaging {modality: DTI_tractography}`**, **`{modality: perfusion_MRI}`** and **`{modality: FDG_PET}`** (rule c). These are the tumefactive cases, with a 2-4 cm enhancing lesion on the stored MRI.
  - DTI: RM01, RM02, RP01, RP02, RP03.
  - Perfusion: RM01, RM02, RP01, RP03 (RP02 already stores one).
  - FDG-PET: RP01 and RP03 (the others already store one).
  - The reports describe the lesion's own features: reduced FA or a displaced tract; a mildly raised rim rCBV with a hypoperfused centre; marginal FDG uptake below the cortex.
  - They name no diagnosis.
- **`perform_clinical_assessment {assessment_type: cognitive_screen}`**, **`order_specialized_test {test_type: neuropsych_battery}`** and **`{test_type: speech_language_evaluation}`** (rules c and d).
  - RP03, GCS 8: not testable.
  - RP05: the stored MMSE is 27 with word-finding difficulty. The reports give MoCA 25, slowed processing speed with reduced fluency, and mild anomia.
  - RS05: scanning dysarthria in the exam, so its speech report shows ataxic dysarthria.
- **`order_specialized_test {test_type: polysomnography}`** (rule b). RP05 has obstructive sleep apnoea on CPAP; the report is a diagnostic study with an AHI of 27.
- **`interpret_labs {panels: [iron_studies]}`** (rule b). S04 has a microcytic anaemia (Hb 10.9, MCV 77.6) and takes ferrous sulfate. The report shows an iron-deficient panel; the library's panel names are kept.

### Terms left to the library, and why

- **performance_status and gait** in cases with a normal gait (isolated optic neuritis, diplopia or sensory relapse: M04, P01-P03, RM02, RM03, RP01, RS01, RS04, S05). A normal or near-normal function is plausible there.
- **VEP**
  - RM03: keratoconus makes the pattern VEP unreliable either way.
  - RP03: unresponsive, and a flash VEP is not what the library reports.
  - Every case without an optic history: a normal VEP is plausible.
- **OCT** for M03: no optic history recorded.
- **Visual fields** for RM03, RP04, M02, RS02 and M03: acuity normal or recovered, with no field complaint.
- **SSEP** where the only sensory loss is vibration at the toes (M01, M03, S03, S04, S06): a normal tibial SSEP is possible.
- **iron_studies** for P01 and M02: no anaemia or iron history to contradict a normal panel.
- **MRS and DTI** in the typical small-lesion cases: normal or near-normal is plausible.
- **Cognition** in RM01: the exam is borderline.
- **Other terms**: spine CT, ECG, anti-JCV (no natalizumab), HbA1c (stored where the patient is diabetic), functional MRI, amino-acid PET. The CSF terms are left because a stored CSF report is served whole.

### Reports added, per case (96 reports in 25 cases)

| Case | Reports |
|---|---|
| M01 | fields, gait, PS |
| M02 | SSEP, gait, PS |
| M03 | gait, PS |
| M04 | fields |
| P04 | SSEP, fields, gait, PS |
| P05 | SSEP, fields, VEP, OCT, gait, PS |
| RM01 | DTI, perfusion, video EEG, ambulatory EEG, gait, PS |
| RM02 | fields, DTI, perfusion |
| RM04 | SSEP, fields, gait, PS |
| RP01 | DTI, perfusion, FDG-PET |
| RP02 | SSEP, DTI, gait, PS |
| RP03 | PS, gait, cognitive screen, neuropsych, speech, cICU EEG, ambulatory EEG, DTI, perfusion, FDG-PET |
| RP04 | SSEP, gait, PS |
| RP05 | SSEP, fields, gait, PS, polysomnography, cognitive screen, neuropsych, speech |
| RS01 | fields, VEP |
| RS02 | SSEP, VEP, OCT, gait, PS |
| RS03 | SSEP, fields, gait, PS |
| RS05 | speech, gait, PS |
| RS06 | SSEP, gait, PS |
| S01 | SSEP, fields, gait, PS |
| S02 | SSEP, fields, gait, PS |
| S03 | fields, gait, PS |
| S04 | fields, gait, PS, iron studies |
| S05 | SSEP, fields |
| S06 | gait, PS |

PS = performance status. Not changed: P01, P02, P03, RM03, RS04.

### Doubts for the physicians

1. **SSEP threshold.** Is loss of vibration at the ankle or above, together with a dorsal-column lesion, the right point to call the SSEP abnormal, with toe-only loss left normal?
2. **Tumefactive cases.** The perfusion (rim rCBV 1.2-1.5) and FDG (marginal uptake, central hypometabolism) reports are what tumefactive demyelination usually shows. Should they be more equivocal, so they do not make lymphoma or glioma easier to exclude than in practice?
3. **Gait numbers.** The TUG and Berg values were derived from a written exam; check whether they match the EDSS-like picture.
4. **RP03 bedside tests.** The orthostatic and other cooperation-dependent bedside assessments are left to the library. The library returns a normal cooperative exam that this patient could not perform. Should those orders get a "not testable" report too?
5. **RS01.** An amblyopic eye gives a reduced VEP amplitude with a normal latency and mild field depression. Confirm that this is wanted rather than the library's normal study.

## SAH (30 cases; 249 reports in 30 cases)

30 cases; all 30 changed; 249 reports added. Verify: 196 mapped orders, 0 answered by the library. Perfect agent 30/30, guards 240 passed, snapshot: no criterion answer changed. Scripts: `SAH/gen_sah.py`, `SAH/gen2_sah.py`, `SAH/fix_ct_region.py`, `SAH/fix_ldopa.py`.

### Terms judged contradictory
- `analyze_csf` (any source, any test; all cases): every case has subarachnoid blood on CT (P02 perimesencephalic too), so clear acellular CSF is impossible. One case fallback with no source answers LP, EVD and lumbar drain. Red cells without clearing, scaled to the Fisher grade; WBC, protein and opening pressure scaled the same way (higher with hydrocephalus; 38 cmH2O in P07, IIH). All onsets under 12 h, so spectrophotometry shows oxyhaemoglobin without bilirubin; M08 (sentinel bleed 3 days earlier) shows a bilirubin peak. RP11 (MS) adds oligoclonal bands, raised IgG index, JCV PCR negative. P01, P03 and P06 already store a CSF: untouched.
- `structured_headache_history_ichd3` (all cases): the library says no thunderclap onset, no red flags, no nausea or photophobia. Every HPI records a sudden worst-ever headache. Per-case report from the HPI: onset, course, associated features, prior headache pattern (migraine in M03, RM11, P01; IIH in P07; chronic headaches in P03), red flags. No diagnosis named.
- `performance_status` (27 cases; not P01-P03, which are ambulant and well): the library gives Karnofsky 100 to inpatients on bed rest. KPS 40/ECOG 3; 30/4 if confused (M03, M05, M07, P04); 50/3 for P07, RM11, RP11.
- `gait_and_balance_timed`, `orthostatic_blood_pressure`, `levodopa_challenge` (25 cases whose exam records gait not tested): the library reports normal walking, 3 minutes of symptom-free standing at 128/78 and normal postural reflexes. Reports say standing not attempted; supine BP is the arrival BP. RP11 (MS gait) and S07 walked: slow measured gait, orthostatic measured without a fall.
- `cognitive_screen`, `neuropsych_battery` (M03, M05, M07, P04; GCS 14, disoriented): library MoCA 28 and normal battery. MoCA 15-19 with attention, recall and orientation deficits; battery stopped early.
- `TEE`, `bubble_study`, `cardiac_MRI` (19 cases with an abnormal stored TTE): the library calls the heart normal. Each copies the stored TTE wall motion, LVEF and valves; TEE adds no thrombus and an intact septum; bubble study shows no shunt at rest; CMR shows oedema in the dysfunctional segments and no LGE (P08: small inferior scar).
- `HbA1c` (M04 7.8, RS12 8.6, S09 8.1): treated type 2 diabetes. S02 already records 7.4 in the HPI and stores it.
- Body US/CT/MRI (M05, S07 with PKD; P05 2 h postpartum): enlarged polycystic kidneys and liver cysts; enlarged postpartum uterus. The CT is stored with region pelvis_abdomen so a chest CT order still gets the library normal chest.
- P05: urinalysis (protein 2+, blood 1+; eclampsia with a seizure), beta-hCG 18,600 (2 h after delivery), OCT (mild RNFL thickening; exam: mild papilledema).
- P06: peripheral smear microcytic hypochromic (stored Hb 7.4, MCV 74, ferritin 4).
- P07 (IIH, chronic papilledema): OCT RNFL thickening, enlarged blind spots on perimetry, MR venography with bilateral transverse sinus narrowing and no thrombosis.
- P08 (STEMI 2 years ago, stented): coronary angiography and coronary CTA with a patent stent and non-obstructive disease.
- RP11 (MS on natalizumab, JCV index 3.2, bilateral disc pallor): anti-JCV positive 3.2, VEP with prolonged P100, OCT with RNFL thinning.
- S06 (4-6 beers daily, GGT 184): %CDT 2.6.

### Terms left to the library on purpose
- spine_MRI, spine_CT: spinal blood not documented anywhere.
- CT_perfusion, perfusion_MRI, perfusion_SPECT, MR_spectroscopy: no documented delayed ischaemia; TCD is stored where relevant.
- MR_venography except P07: no venous disease documented.
- Continuous ICU, video and ambulatory EEG: each case stores a normal routine EEG; a normal long recording is consistent with it.
- exercise_echo, exercise_stress_test: not performed in acute SAH; the case gives no exercise result to contradict.
- orthostatic_blood_pressure in P01, P02, P03, P07, RM11: ambulant; library values plausible after analgesia.
- functional_neuro_signs: normal is consistent with every case.
- Coronary angiography and CTA in the Takotsubo cases other than P08: normal coronaries are expected in Takotsubo.
- CDT in P04 (2-3 drinks daily, borderline); urinalysis in S09 (CKD, proteinuria not documented); haptoglobin and smear in P05 (HELLP not established).
- shunt_tap CSF source: no shunt in any case (the CSF fallback answers it anyway).

### Reports added per case
- SAH-M01 (9): CSF, performance_status, gait_and_balance_timed, TEE, bubble_study, cardiac_MRI, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-M02 (9): CSF, performance_status, gait_and_balance_timed, TEE, bubble_study, cardiac_MRI, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-M03 (8): CSF, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-M04 (10): CSF, performance_status, gait_and_balance_timed, TEE, bubble_study, cardiac_MRI, [HbA1c], structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-M05 (14): CSF, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, TEE, bubble_study, cardiac_MRI, chest_abdomen_pelvis_CT / pelvis_abdomen_CT, pelvis_abdomen_ultrasound, pelvis_abdomen_MRI, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-M06 (6): CSF, performance_status, gait_and_balance_timed, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-M07 (11): CSF, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, TEE, bubble_study, cardiac_MRI, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-M08 (6): CSF, performance_status, gait_and_balance_timed, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-P01 (1): structured_headache_history_ichd3
- SAH-P02 (2): CSF, structured_headache_history_ichd3
- SAH-P03 (1): structured_headache_history_ichd3
- SAH-P04 (11): CSF, performance_status, gait_and_balance_timed, cognitive_screen, neuropsych_battery, TEE, bubble_study, cardiac_MRI, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-P05 (15): CSF, performance_status, gait_and_balance_timed, TEE, bubble_study, cardiac_MRI, chest_abdomen_pelvis_CT / pelvis_abdomen_CT, pelvis_abdomen_ultrasound, pelvis_abdomen_MRI, [beta-hCG], [urinalysis], optical_coherence_tomography, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-P06 (9): performance_status, gait_and_balance_timed, TEE, bubble_study, cardiac_MRI, [peripheral smear], structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-P07 (6): CSF, performance_status, optical_coherence_tomography, visual_field_perimetry, MR_venography, structured_headache_history_ichd3
- SAH-P08 (11): CSF, performance_status, gait_and_balance_timed, TEE, bubble_study, cardiac_MRI, coronary_angiography, coronary_CTA, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-RM11 (6): CSF, performance_status, TEE, bubble_study, cardiac_MRI, structured_headache_history_ichd3
- SAH-RP11 (9): CSF, performance_status, gait_and_balance_timed, [anti_JCV_antibody], vep, optical_coherence_tomography, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-RS11 (9): CSF, performance_status, gait_and_balance_timed, TEE, bubble_study, cardiac_MRI, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-RS12 (10): CSF, performance_status, gait_and_balance_timed, TEE, bubble_study, cardiac_MRI, [HbA1c], structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-S01 (9): CSF, performance_status, gait_and_balance_timed, TEE, bubble_study, cardiac_MRI, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-S02 (9): CSF, performance_status, gait_and_balance_timed, TEE, bubble_study, cardiac_MRI, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-S03 (6): CSF, performance_status, gait_and_balance_timed, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-S04 (9): CSF, performance_status, gait_and_balance_timed, TEE, bubble_study, cardiac_MRI, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-S05 (6): CSF, performance_status, gait_and_balance_timed, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-S06 (10): CSF, performance_status, gait_and_balance_timed, TEE, bubble_study, cardiac_MRI, [CDT], structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-S07 (9): CSF, performance_status, gait_and_balance_timed, chest_abdomen_pelvis_CT / pelvis_abdomen_CT, pelvis_abdomen_ultrasound, pelvis_abdomen_MRI, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-S08 (9): CSF, performance_status, gait_and_balance_timed, TEE, bubble_study, cardiac_MRI, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-S09 (10): CSF, performance_status, gait_and_balance_timed, TEE, bubble_study, cardiac_MRI, [HbA1c], structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge
- SAH-S10 (9): CSF, performance_status, gait_and_balance_timed, TEE, bubble_study, cardiac_MRI, structured_headache_history_ichd3, orthostatic_blood_pressure, levodopa_challenge

### Doubts for the physicians
- Stored normal routine EEGs in the confused Hunt-Hess 3 cases (M03, M05, M07, P04) and in P05 (eclamptic seizure with PRES): a normal background is doubtful; continuous EEG was left consistent with them.
- P08: the territory of the old STEMI is not stated; mid RCA chosen, so the CMR scar is inferior.
- P07: transverse sinus narrowing on MRV is the usual IIH finding but not documented in the case.
- P05: OCT thickening follows the exam's mild papilledema; the mild right pelvicalyceal dilatation is physiological postpartum and invented.
- CSF numbers are scaled by Fisher grade, not taken from data; RP11 oligoclonal bands assumed from established MS.
- Levodopa challenge and orthostatic testing would not be done in acute SAH; reports say not performed rather than inventing results.
