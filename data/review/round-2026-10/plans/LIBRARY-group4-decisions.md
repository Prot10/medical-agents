# Library contradictions, group 4: decisions (25 Oct 2026)

Conditions FEPI-TEMP, GLIO-HG, MIG-AURA, PD and VASC-DEM (150 cases). Map: `LIBRARY-group4-map.yaml`.
A script that uses the guard's own `contradicted_orders` and `library_answers` confirms that none of the
map's 1330 (case, order) pairs is answered by the library now.

- **Cases changed:** 125 of 150. All 30 cases changed in FEPI-TEMP, GLIO-HG, PD and VASC-DEM, and 5 in MIG-AURA.
- **Reports and lab panels added:** 1213.
- **Checks:**
  - 150/150 cases pass the perfect-agent check.
  - The case guards pass for the five prefixes.
  - A before/after snapshot of every criterion alternative is identical in every case, so no criterion answer changed.
  - No added text contains a 60-character window of a criterion's expected_evidence. The only exception is GLIO tissue copies, which repeat the stored tissue report verbatim.
- **Not touched:** tiers, criteria, diagnoses, initial outputs and the follow-ups already stored.

Map design, per condition:
- `all_cases` holds a term judged contradictory in at least half the condition's cases, and answered without the library in every non-excepted case.
- `except` is used only for GLIO-HG-RM02, an intramedullary cord tumour with no intracranial mass to image.

## Group-wide findings for the central merge

- **Library defect: drug levels.** `AED_levels`, `valproate_level` and `lithium_level` return therapeutic levels in patients who do not take these drugs. This group fixed the defect only where a patient takes a library-panel drug: all FEPI-TEMP cases (on antiseizure drugs) and GLIO-HG M04, RS04 and RP03 (on levetiracetam). Each case panel reports the patient's own drug and marks the others "Not detected". The other cases (most of PD and VASC-DEM, and many GLIO and MIG cases) still get the library's therapeutic levels. The fix should be central: a library default of "not detected", or drug-aware levels.
- **CT is not routed by contrast.** One fallback `ct` answers plain, contrast and CTA orders. Where the library's normal head CT contradicted a case, the stored CT describes the parenchymal finding, and a CTA order receives that report. A CT routed by `contrast` and `angiography` would let a case store a real CTA.
- **The fallback CSF answers every CSF order,** whatever the source or special tests. A case CSF must therefore carry every special test the case could plausibly be asked for (GLIO-HG-P02).
- **Venous duplex reports need `modality: duplex`** for the body-imaging study router (FEPI-TEMP).

## FEPI-TEMP (30 cases)

218 case-specific reports were added to 30 cases (241 map entries at case level). No criterion's served output changed: the before/after snapshot is identical for FEPI-TEMP. Generators, for reproducibility: `g4/fepi/fepi_apply.py` (with `fepi_eeg.py`, `fepi_other.py`, `fepi_misc.py`).

### Terms judged contradictory, and why

- **`analyze_eeg` `eeg_type=ambulatory`**: 28 cases. Changed in every case except M03 and RP02, which already stored one. Every case stores temporal discharges, slowing or periodic discharges. A 48-hour recording that includes sleep cannot be normal, so each report repeats that patient's own interictal findings: side, electrodes, rate and slowing.
  - No events are captured, except in four cases:
    - RP01: recurrent right temporal seizures and LPDs+F, as on its cEEG.
    - RP03: five events, at 3 to 5 a day.
    - P02: about 40 events, matching faciobrachial dystonic seizures (FBDS) at 20 to 40 a day; most are obscured by artifact.
    - RS01: three gelastic push-button events.
- **`eeg_type=video`** (also answers `continuous_icu`): 19 cases.
  - M01-M04, RM01-RM04, RP02, RP03, RS02, RS03, RS05, S01-S06.
  - Each report gives interictal findings only, "no habitual event captured over 72 hours", for patients with monthly or weekly seizures.
  - Two cases capture seizures because their stated frequency makes a seizure-free 72 hours implausible:
    - RM02, nearly daily: one left temporal seizure.
    - RP03, 3 to 5 a day: nine events.
- **`eeg_type=routine`**: 3 cases.
  - P02: moderate diffuse slowing, as on its video-EEG.
  - RP04: about 10 left anterior temporal discharges an hour awake; its outside EEG also showed left and right temporal sharp transients.
  - RS04: about 15 right temporal discharges an hour awake.
  - The routine report also answers `sleep_deprived` through the stand-in rule.
- **`order_advanced_imaging` `modality=FDG_PET`**: 11 cases where the library still answered.
  - M05, P03, RM01-RM04, RS02, RS03, RS05, S05, S06.
  - Interictal FDG-PET is the condition's characteristic presurgical test. Each report gives ipsilateral temporal hypometabolism; lesion cases add a photopenic focus at the lesion. Stored FDG reports in the other 19 cases already did the same.
- **`obtain_tissue_diagnosis`** (`resection`, `stereotactic_biopsy`, `open_biopsy`): 28 cases.
  - A brain specimen from a case with a stored substrate cannot be "no diagnostic abnormality". Substrates:
    - HS, ILAE type 1;
    - FCD IIb in M04, FCD I in P01, and FCD IIIa with HS in RP04;
    - cavernoma (M05);
    - cortical tuber (RM02);
    - ganglioglioma, WHO grade 1 (RM04);
    - DNET, WHO grade 1 (S02, S03, S06);
    - metastatic melanoma (RP03);
    - HSV-1 necrotizing encephalitis (RP01);
    - T-cell limbic inflammation (P02);
    - encephalocele (RP05);
    - hypothalamic hamartoma for the RS01 biopsies.
  - HS biopsies report neuronal loss with gliosis and say that the sample cannot be classified.
- **`order_specialized_test` `test_type=neuropsych_battery`**: 19 cases.
  - M01-M03, P02, P03, P05, RM01-RM03, RP01, RS01-RS03, RS05, S01-S05.
  - The condition's own stored batteries (M05, P01, P04, RP04, RP05, RS04) show material-specific memory deficits on the side of the lesion. The library's "all normal, MoCA 28/30" contradicts mesial temporal sclerosis and lesions.
  - Profiles:
    - right side: visual memory deficit; left side: verbal memory deficit;
    - P02: amnestic and limbic;
    - RM01: low average, right hemisphere and executive deficits;
    - RM03: intellectual-disability range;
    - RP01: testing could not be completed in the confusional state.
- **`perform_clinical_assessment` `cognitive_screen`** (baseline): 4 cases. Each score is derived from the exam:
  - P02: MoCA 17, against its MMSE of 22;
  - RM01: MoCA 24/30, as examined;
  - RM03: MoCA 15, developmental delay;
  - RP01: MoCA 7, acute confusion.
- **`interpret_labs` `AED_levels`**: 21 cases. The library panel shows therapeutic levels of six drugs at once, which no patient takes. The case panel reports the drug actually taken (P03 and P04 lamotrigine; RS01 levetiracetam and valproate) and "Not detected" for the rest.
- **`interpret_labs` `valproate_level`**: 28 cases, all except the patients on valproate (RM02, RS04 and RS01, whose answer is its own AED panel). The library's 75 mg/L contradicts patients not on valproate.
- **Other lab panels:**
  - `HbA1c`: M03 at 6.1% (metabolic syndrome on metformin, glucose 114) and RP04 at 6.9% (as in its history).
  - `beta-hCG` positive and `D_dimer` raised: RS02, at 33 weeks.
  - `iron_studies` with an iron-deficiency pattern: S02 and RS04 (both on iron, microcytic).
- **Echocardiography:**
  - `TTE` and `TEE` in RM02: residual rhabdomyoma, as in its history.
  - `TEE` in RP02 and RS05: they repeat their stored TTE (mitral prolapse; mild left atrial enlargement).
- **RP02 imaging:**
  - `chest_CT`: non-contrast, showing its stored infarct opacity.
  - `lower_extremity_venous_duplex`: left popliteal and calf vein DVT, matching the history and the PE.
- **RP03, metastatic melanoma (lungs, breast, liver, bone):**
  - `chest_abdomen_pelvis_CT` in the fallback slot, which also answers `chest_CT` and `pelvis_abdomen_CT`;
  - `chest_CTA`, `chest_xray`, `pelvis_abdomen_MRI` and `pelvis_abdomen_ultrasound`;
  - `whole_body_FDG_PET`, plus `MR_spectroscopy`, `perfusion_MRI` and `amino_acid_PET` of the brain metastasis.
- **RM04:** `MR_spectroscopy` of the mural nodule.

### Left to the library on purpose

- Routine and sleep-deprived EEG in P03, P04 and RS01. Their video-EEGs show occasional awake discharges (2 to 5 an hour), so a single normal routine recording is plausible.
- All tissue procedures in P04 and RP02. Both have an MRI-negative temporal lobe, so non-specific or normal histology is plausible. If the parent folds tissue into `all_cases`, these two are the exceptions.
- Neuropsychology:
  - M04, RM04, S06: the lesion is lateral or inferior neocortex, outside the mesial memory structures.
  - RP02: normal MRI.
  - RP03: acute oncological admission; bedside cognition is intact.
- `cognitive_screen` (MoCA 28) in every case whose exam is intact; P03 has an MMSE of 30.
- `MR_spectroscopy`, `perfusion_SPECT` and `functional_MRI` in mesial temporal sclerosis cases.
- `perfusion_MRI` and `amino_acid_PET` in DNET, cavernoma and ganglioglioma cases (low or variable values).
- Mediastinal and spine imaging in RP03 (sites not stated).
- `lymph_node_biopsy` and `temporal_artery_biopsy`.
- Lab panels: CK, prolactin, CBC, CMP, TSH and the other screening panels.
- ECG, Holter, CT, `bubble_study`, `exercise_echo`.

### Reports added per case

The case logs list each case's reports in "## Library contradictions (25 Oct 2026)", from `state/changes_FEPI-TEMP.json`.

### Doubts for the physicians

- **Video-EEG:** reports without seizures may understate yield in a monitoring unit. The seizures written for RM02 and RP03 are new findings, chosen to match the stated frequency and semiology.
- **FDG-PET in RS02 at 33 weeks' gestation:** the report gives the expected finding, but whether the study should be done at all is a safety question.
- **Biopsy of a sclerotic hippocampus:** this is not a real-world procedure. The reports describe what such a sample would show.
- **Two tissue subtypes inferred from MRI:** FCD IIb in M04 (transmantle sign) and FCD type I in P01 (temporopolar blurring).
- **RS01 (hypothalamic hamartoma with left mesial temporal sclerosis):** the resection order is answered with a left temporal lobectomy specimen (HS) and the biopsies with hamartoma tissue. Which target a resection order means is ambiguous.
- **RS03 (postpartum, breastfeeding):** prolactin would be raised, but "prolactin" is a banned string outside P05, so the library still answers.
- **RP03:** sizes and bone sites of the metastases (iliac wing, rib, avoiding the spine) are authored, because the case states only the organs involved.
- **RM02 (TSC):** renal angiomyolipomas are likely but not in the case, so abdominal imaging stays normal.
- **P01:** the history mentions mild mitral prolapse, but the stored TTE says the mitral valve is normal. This inconsistency predates this pass and was not changed.
- **Cross-routing:**
  - The RP02 non-contrast chest CT also answers a chest-abdomen-pelvis CT order.
  - The RP03 chest-abdomen-pelvis CT answers `chest_CT` and `pelvis_abdomen_CT`.

## GLIO-HG (30 cases), 25 Oct 2026

428 case-specific reports and lab panels were added to all 30 cases. The map has 11 `all_cases` terms with `except: [GLIO-HG-RM02]`, plus 174 case-level entries. Every case passes the perfect-agent check and the guards. The before/after snapshot of every criterion alternative (341 calls) is identical. The fabrication test passes; the tissue copies repeat the stored molecular results.

Generators: `g4/glio/gen_glio.py`, `glio_data.py`, `specs_glio.py`, `apply_glio.py`.

Every report is derived from what the case already stores: the MRI lesion (side, site, size, enhancement, mass effect, rCBV), the routine EEG, the exam and the history.

### Terms judged contradictory, and why

**Condition-wide terms** (map `all_cases`; RM02 is excepted):
- **Head CT, plain, contrast and CTA.** The library's normal head CT contradicts the stored mass. One fallback CT answers all three orders, because CT is not routed by contrast. It describes the lesion, its oedema, its shift and its calcification or haemorrhage as the MRI shows them.
  - P05 already stores a CT.
  - RM02's CT reports no intracranial abnormality, the stored occipital subcutaneous nodules and left parotid lesion, and that the cervical cord is outside the field of view.
- **Tissue, open_biopsy (29 cases).** The library returns a non-diagnostic open biopsy. Each case gets a copy of its stored resection or stereotactic report, with the procedure and specimen line changed. RM02 already stores an open biopsy.
- **Brain metabolic and vascular imaging (29 cases):** FDG_PET, amino_acid_PET, CT_perfusion, perfusion_SPECT and cerebral_angiography. The library reads them as normal, which contradicts a known enhancing mass. The reports follow the stored perfusion MRI (rCBV) and the lesion's site.
- **Prolonged EEG, video and ambulatory (all 30 cases).** The library reads them as normal, but every case stores an abnormal routine EEG. The reports keep the routine EEG's findings over 24 h (video) or 48 h (ambulatory). RS03's lateralized periodic discharges persist.

**RM02 exception.** RM02 has an intramedullary cervical cord tumour, so it has no intracranial mass to image. Its case-level entries are:
- CT, video and ambulatory EEG;
- ICHD-3 history;
- gait;
- stereotactic tissue: an image-guided needle-core copy of the stored open biopsy;
- SSEP, showing central conduction delay at the cervical cord;
- VEP, showing a delay in the left eye from the left optic pathway glioma.

**Terms driven by the exam or history** (case level):
- **ICHD-3 headache history (29 cases).** The library says "no headache", but the cases have progressive or positional headache, and some a prior migraine (RM02 has a migraine history only). RM01 stays with the library, because it reports no headache.
- **Cognitive screen (24 cases) and neuropsychological battery (24 cases).** MoCA items and domain z-scores follow the documented aphasia, neglect, memory or executive deficits. Where the case stores an MMSE, the score is kept.
- **Gait and balance, timed (24 cases).** These cases have hemiparesis, ataxia or a broad-based gait on exam.
- **Speech and language evaluation (11 cases).** Aphasia or dysarthria is documented.
- **Visual field perimetry (16 cases).** These cases have a homonymous field defect, a quadrantanopia or blind-spot enlargement on exam.
- **OCT (5 cases):** P02, RM03, RS02, RS03 and RS04, which have papilledema on fundoscopy.
- **DTI tractography (9 cases):** P01-P05, RM01, RP01, RP03 and RP04. These are deep, perirolandic, callosal, thalamic or brainstem lesions; the library reports intact tracts.

**Drugs and history** (case level):
- **AED_levels and valproate_level** (M04, RS04, RP03, which take levetiracetam). The library reports therapeutic levels of drugs the patient does not take. The case panel gives a levetiracetam level, with the other drugs not detected.
- **RM03 iron_studies:** the history records iron-deficiency anaemia, still on oral iron.
- **RP02 IGRA:** positive, matching the history of treated tuberculosis.
- **P02 (HIV; primary CNS lymphoma in the differential):**
  - a CSF fallback: lymphocytic pleocytosis, raised protein, EBV DNA and HIV RNA, rare atypical cells and no clonal population. The fallback CSF answers every CSF order.
  - whole-body FDG PET, abdominal ultrasound and abdominal MRI, which show the stored axillary nodes and splenomegaly.

**Stored findings** (case level):
- **RS01:**
  - audiometry, showing a right sensorineural hearing loss that matches the exam;
  - MR venography, showing compression of the right sigmoid sinus and jugular bulb by the stored jugular foramen mass;
  - whole-body FDG PET, showing the same mass with no other lesion.
- **RM01:** BAEP, showing a right pontine conduction delay.
- **RP02:** chest X-ray and chest CTA, showing the stored calcified right upper lobe granulomas.
- **RP03:** chest X-ray, showing the stored VP shunt tubing.
- **S05:** functional MRI, showing a displaced left hand motor area. The language areas are remote from the mass.

### Left to the library on purpose
- MR angiography, and MR venography except in RS01. A normal study is consistent with these intra-axial tumours.
- Functional MRI except in S05. These are right-hemisphere or deep lesions, where a normal map is plausible.
- DTI in RM02 and RM03: the supratentorial tracts are normal.
- The post-intervention cognitive screen.
- The cognitive screen in M04, P05, RM02, RM03, RS03 and S06: the exams are near normal.
- Gait in M01, M02, M03, M05, P01 and S06: the gait exam is normal.
- VEP in P03 and P05, which have a remote optic neuritis (see doubts).
- OCT in P04, P05 and RP02: borderline disc blurring.
- CSF in P05, RM02 and RP02.
- Whole-body PET in RP04, which has an indeterminate 1.3 cm liver lesion (see doubts).
- Incidental renal, ovarian and prostate cysts on abdominal ultrasound or MRI.
- EMG/NCS in RP03 (see doubts).
- HbA1c: the diabetic patients already store one.
- ANA in RS06, which has rheumatoid arthritis.
- Valproate and lithium levels in patients who do not take them. This is the central library defect.

### Doubts for the physicians
- Contrast and CTA orders get the non-contrast fallback CT, because CT is not routed by contrast. The report describes the lesion, not the vessels.
- RM02: a stereotactic biopsy of the cervical cord is not a standard procedure. The copy says "image-guided needle cores".
- The SUV, TBR, CBV, latency, MoCA, z-score and timed-gait numbers are synthetic. They are kept consistent with each case only.
- Perfusion SPECT: hypoperfusion over the lesion and its oedema is assumed. A high-grade tumour can also show focal hyperperfusion.
- The prolonged EEGs state "no clinical events". That is a new statement.
- P03's prolonged EEG captures no seizure.
- P02: the CSF EBV and HIV RNA values are invented, and a lumbar puncture may be unsafe with a 6 mm midline shift.
- S05: the fMRI distances are invented.
- RP04's liver lesion is left to the library's normal whole-body PET.
- Remote optic neuritis in P03 and P05: the VEP stays normal.
- RP03: EMG/NCS is left to the library; a physician should confirm that a normal study fits the case.
- RM03: the iron panel assumes the deficiency persists despite two years of oral iron.

## MIG-AURA (25 Oct 2026)

30 cases read. Typical migraine with aura has no structural finding, so the library normal reports
fit 25 cases; 30 reports were stored in 5 cases (P05, P07, P08, P09, RM11). All are case-level map
entries; no all-cases term.

### Terms judged contradictory

| Term | Cases | Why |
|---|---|---|
| `interpret_labs` coagulation | P05 | warfarin, INR 3.8 at last check, gum bleeding and epistaxis; library INR 1.0 |
| `order_specialized_test` visual_field_perimetry | P07, P08, RM11 | homonymous field defects on the stored exam (P07 dense left hemianopia, formally confirmed; P08 left inferior quadrantanopia; RM11 right restriction) |
| `order_echocardiogram` TEE | P07, P08 | P07 small PFO on the stored bubble study (library: intact septum); P08 mild concentric LVH on the stored TTE |
| `order_echocardiogram` bubble_study, exercise_echo | P08 | library LV "normal size"; stored TTE shows mild concentric LVH, grade I diastolic dysfunction |
| `order_advanced_imaging` FDG_PET, perfusion_MRI, CT_perfusion, perfusion_SPECT, DTI_tractography | P07, P08 | established 3.5 cm right occipital infarct (P07) and 6 cm right parieto-occipital stroke-like lesion (P08); library: symmetric, normal, optic radiations intact |
| `order_advanced_imaging` MR_spectroscopy | P07 | library "normal NAA" in an established infarct (P08 already stores its MRS) |
| `order_advanced_imaging` cerebral_angiography | P09 | 4 mm left MCA bifurcation aneurysm on the stored MRA; library "no aneurysm" |
| `analyze_eeg` routine (fallback, also answers sleep-deprived), ambulatory, video | P08 | no EEG stored; a 6 cm subacute cortical lesion with a normal EEG contradicts the case |
| `analyze_eeg` ambulatory | RM11 | stored routine and video EEGs show continuous left hemispheric slowing |
| `order_specialized_test` audiometry, muscle_biopsy | P08 | documented mild bilateral high-frequency SNHL; m.3243A>G MELAS (library: normal hearing, no RRF/COX-negative fibres) |
| `order_specialized_test` speech_language_evaluation; `perform_clinical_assessment` cognitive_screen, gait_and_balance_timed, performance_status | RM11 | confused, motor aphasia, right hemiparesis, bed-bound; library: no aphasia, MoCA 28/30, TUG 9.1 s, Karnofsky 100 |

### Left to the library on purpose

- S01-S11, M01-M08 and the other typical migraine-with-aura cases: library normal MRI, EEG, MRA, ECG, echo, labs and assessments match a disorder without structural findings.
- `genetic_panel:hemiplegic_migraine` negative in M03, P09 and RS11: most sporadic hemiplegic migraine is panel-negative, so a negative panel does not contradict the case.
- P02 (apixaban, PAF on ILR) coagulation: apixaban barely moves PT/INR; ECG, Holter and TTE normal match the stored sinus rhythm and normal heart.
- P05 ECG, Holter and TTE: the stored work-up and the outside Holter are normal.
- beta-hCG in OCP users and lipids on a statin: normal results are plausible.
- P06 (CADASIL) cognitive screen: the case records MoCA 28/30.
- RM11 AED_levels: the library returns therapeutic levels of six AEDs, but topiramate (her drug) is not in the panel; a central library defect, not fixed here.

### Doubts for the physicians

- P08 cognitive_screen and neuropsych_battery: the case records "slightly slow to respond" and school learning difficulty; the library MoCA 28/30 and an average-range battery may be too good. Not changed (no scores in the case).
- P08 perfusion terms: written as hyperperfusion of the subacute stroke-like lesion (the expected MELAS pattern at about day 10); please confirm the direction.
- P08 muscle_biopsy: written as ragged-red fibres, strongly SDH-reactive vessels and occasional COX-deficient fibres (the m.3243A>G pattern); the case states only the mother's biopsy.
- RM11 FDG_PET, perfusion terms and MR_spectroscopy: library normal during an acute hemiplegic attack with cortical swelling is unlikely, but the direction (hypo- or hyperperfusion, lactate) is uncertain; left to the library.
- Case fallbacks outside this pass: P07 fallback CT reads normal despite the established infarct; P09 orders for CTA are answered by the non-contrast fallback CT (no flag routing); P08 fallback CSF reads unremarkable where a CSF lactate rise is expected in MELAS.

## PD (30 cases; 170 reports added)

### Terms judged contradictory, and why
- **levodopa_challenge** (29 cases; RP04 already stores one; map `all_cases`). Rule 3: every case has parkinsonism on exam, but the library reports MDS-UPDRS III 3/132 with no signs. Idiopathic PD responds by 40-61%. P01 (MSA-P) responds by 13%, P02 (DLB) by 20%, P03 (PSP) by 7% and RP03 (MSA) by 11%; P03 and RP03 already take 600 mg/day with no benefit. Patients on levodopa (RM01, RM05, P03, RP03) are tested OFF after 12 h without it.
- **gait_and_balance_timed** (30 cases; map `all_cases`). Rule 3: the stored gait exam is abnormal in every case. Turns, pull-test steps, freezing, tandem and Romberg match each exam. Postural reflexes are called impaired only when the pull test needs 3 or more steps or the examiner has to catch the patient.
- **cognitive_screen** (25 cases with a stored MoCA). Rule 3: each report gives the stored total and the items lost. The library reports 28/30 with other items. P01, P02, P03 and RP01-RP03 also report the stored MMSE.
- **speech_language_evaluation** (27 cases). Rule 3: hypophonia is documented in the exam. Where the exam says "no dysarthria", the report gives hypophonia with precise articulation. RM01, RM05 and RP04 show mild hypokinetic dysarthria, P03 spastic dysarthria (PSP) and RP03 mixed hypokinetic-ataxic dysarthria (MSA).
- **MIBG_scan** (23 idiopathic PD cases still answered by the library). Rule 1, MDS supportive criterion: delayed H/M 1.12-1.41 (normal >1.60), the same reference as RP04.
- **olfactory_test** (11 cases: M01, M03, P02 (DLB), P04, RM01, RS02, RS03, RS04, S01, S02, S03). Rule 1: UPSIT 17-27/40.
- **autonomic_testing + tilt_table** (P02, RP01, RP02). Rule 3: the stored orthostatic test shows orthostatic hypotension. The reports show neurogenic orthostatic hypotension, with figures close to the stored ones.
- **orthostatic_blood_pressure** (P03, RS01, RS03, RS04, RM05). Rule 3: the reports carry the exam's numbers, and none shows orthostatic hypotension.
- **FDG_PET** (P01 putaminal; RP03 putaminal, cerebellar and pontine). Rule 1: MSA pattern, hedged.
- **analyze_eeg routine** (P02 DLB). Posterior dominant rhythm 6.5-7 Hz with posterior slowing and frontal intermittent rhythmic delta activity (a supportive biomarker).
- **HbA1c** (M01, M02, M03, RM01, RM04, RP05, RS02, S02, S03 6.9, S05 6.8). Rule 2: treated diabetes, values 6.7-7.8%.
- **BMP** (RP05, CKD stage 2). Creatinine 0.92 mg/dL, eGFR 64 and glucose 128 mg/dL. This one panel also answers creatinine and CMP orders.

### Mimics and terms left to the library on purpose
- MIBG stays normal in P03 (PSP). Olfaction stays normal in P01 (MSA) and P03 (PSP).
- M04 speech stays normal: the exam records normal volume. P02 speech is not described in the case.
- The cognitive screen stays with the library in M03, RS01, S01, S02 and S05: only an MMSE of 28-29 is stored.
- FDG stays normal in idiopathic PD. The genetic PD panel stays negative.
- PSG stays normal wherever RBD is denied (the library answers only those cases).
- The neuropsychological battery stays normal where MoCA or MMSE is at least 28.
- The ECG and the post-intervention cognitive screen stay with the library.

### Doubts for the physicians
- A reduced MIBG in early, mild PD (S cases): early disease can still show normal uptake. The values are mildly reduced.
- M01-M03 (metoclopramide-unmasked PD): the levodopa challenge assumes a response despite the D2 blockade.
- All challenge, gait, speech and UPSIT numbers are synthetic and only consistent with each exam.
- A library defect, for the central `library_contradictions.yaml`: AED_levels, valproate_level and lithium_level return therapeutic levels in patients who do not take those drugs (28-29 PD cases). This should be fixed centrally.

## VASC-DEM (30 cases), 25 Oct 2026

367 case-specific reports in 30 cases (all VASC-DEM cases changed). Map fragment: `map_VASC-DEM.json`; per-case lines: `changes_VASC-DEM.json`.

### Contradicted by the library, stored per case

**All cases (map `all_cases`):**
- `FDG_PET` and `perfusion_SPECT`: the library normal contradicts the infarcts, lacunes, haemorrhage cavities and white matter disease that every case stores. Each report gives a hedged pattern that follows the case's own lesions. FDG_PET: 27 cases (M07, M08 and P02 already stored one). perfusion_SPECT: 30.
- `performance_status`: the library reads KPS 100 / ECOG 0 and "working", for retired patients who are dependent in instrumental activities. 30.
- `exercise_stress_test`: the library describes a patient of about 50 in sinus rhythm at 10.4 METs. Each report uses the case's age, rhythm, gait and beta-blockade. 30.

**Case level:**

| Term | Cases | Why |
|---|---|---|
| `tau_PET` | M05, M07, M08, P01, P02 | Mixed AD/VaD cases with positive AD biomarkers |
| `amyloid_PET` | P04 | CAA with an occipital cavity; positive, posterior predominant |
| `neuropsych_battery` | M03 | |
| `gait_and_balance_timed` | 14 | The examination documents an abnormal gait |
| `levodopa_challenge` | 24 | Lower-body parkinsonism or gait apraxia: a poor response |
| `TEE` | 28 (not M04, P05, whose TTE is normal) | Derived from each stored TTE: AF appendage, prostheses, leads, LV thrombus in M03, arch atheroma in M10 and S08 |
| `cardiac_MRI` | 11, plus P08 "not performed" | |
| `coronary_angiography`, `coronary_CTA` | M03, S08 | Known coronary disease and CABG |
| `electrophysiology_study` | AF cases (M07, M08, M10, S06, P04), P08 (complete AV block) | |
| `speech_language_evaluation` | 14 | |
| `emg_ncs` | 6 | |
| `ssep` | 5 | |
| `skin_biopsy_iencf` | M02, S04 | Diabetic neuropathy |
| `visual_field_perimetry` | M10, P04 | Hemianopia |
| `polysomnography` | P02, P06, S02 | OSA |
| `respiratory_function` | P06, S02, S05 | S05 has COPD |
| `structured_headache_history_ichd3` | P05, P09, S09 | |
| `orthostatic_blood_pressure`, `tilt_table` | P06 | Supine BP 186/108 |
| `DTI_tractography` | 27 | Not P09 or S09; P08 "not performed" |
| `CT_perfusion` | 12 | Cortical or territorial infarcts and cavities |
| `perfusion_MRI` | 11, plus P08 "not performed" | Same cases as CT_perfusion |
| `MR_angiography` | M03, M05, S06, S07, S11, plus P08 "not performed" | |
| `cerebral_angiography` | 8 | |
| `transcranial_doppler` | M10, S08 | Severe right ICA stenosis |
| `functional_MRI` | M03, S06, S11, plus P08 "not performed" | |
| `MR_spectroscopy`, `MR_venography`, brain MRI fallback slot | P08 "not performed" | Non-MR-conditional pacemaker, pacing-dependent |
| `holter_24h` | P08 | Paced rhythm |
| Chest imaging | M06, S08, P08 (sternotomy, valve, leads); S05 (emphysema) | |
| `spine_MRI`, `spine_CT` | M08 (laminectomy), P02 (L4-S1 fusion) | |
| Pelvis/abdomen | S03 (CKD kidneys, BPH), M08 (prostate after radiotherapy); M01, S07 ultrasound only (hysterectomy) | |
| Labs: urinalysis glycosuria | M10, S04 | Empagliflozin |
| Labs: BNP | M03, M07, M08, M10, P04, S06 | |
| Labs: homocysteine | S04 | 17.8, as stored in its MMA follow-up |

**Body imaging detail:**
- Chest imaging for M06, S08 and P08 covers chest_xray, chest_CTA, mediastinum_CT and chest_abdomen_pelvis_CT. For S05 it covers chest_CTA and chest_abdomen_pelvis_CT.
- Spine imaging covers spine_MRI and spine_CT.
- Pelvis/abdomen imaging for S03 and M08 covers ultrasound, CT and MRI.
- P08 also gets "not performed" reports for spine_MRI, mediastinum_MRI, pelvis_abdomen_MRI and peripheral_nerve_MRI.

**Served by another stored report:**
- A chest_CT order is answered by the stored chest_abdomen_pelvis_CT report: the regions overlap, and a CT modality is served. No separate chest_CT report was stored.
- P08: telemetry, 48 h Holter, 14/30-day monitors and ILR orders are answered by the 24 h Holter.

### Left to the library on purpose
- **Amyloid PET:** pure VaD cases and M01 (normal CSF).
- **Tau PET:** pure VaD and CAA cases.
- **CSF:** pure VaD.
- **CT and perfusion MRI** in SVD-only cases: the lacunes are below perfusion resolution.
- **DaTscan:** normal or near-normal in vascular parkinsonism.
- **Carotid duplex** where the library serves it.
- **Labs:**
  - CADASIL panel outside P05 and P06; MMA; thiamine; homocysteine except S04.
  - Coagulation on DOACs: P04's stored coagulation is normal on apixaban.
- **ECG:** its 12 library cases.
- **Holter:** M04, P09 and S09 (longer sinus recordings are stored).
- **Library-level oddities, not case-specific:**
  - `device_interrogation` in the 29 cases with no device;
  - `AED_levels` returning "therapeutic" levels for non-users.
- **Doubts, kept as library:**
  - CDT (M02, P06), troponin, PTH, iron studies;
  - OCT, audiometry, MRS outside P08, autonomic testing;
  - ambulatory and video EEG;
  - the other body imaging studies.

### Doubts for the physicians
- M03 is allergic to iodinated contrast (urticaria), yet its CT perfusion, DSA, coronary angiography and coronary CTA reports read as performed.
- P08: is "not performed" the right answer for its MR studies, or should they report findings? Its 24 h Holter shows no AF despite a stored device AF burden of 2.1%, and it also answers 30-day/ILR orders.
- Invented details:
  - S08: graft anatomy (occluded vein graft to the RCA);
  - M03: mid-LAD occlusion and LV thrombus size;
  - coronary calcium scores.
- Mild LVH and LA size on cardiac MRI; BNP values in AF.
- PTH and homocysteine in CKD 3b (S03) were left to the library.
- FDG/SPECT impressions in the mixed cases say "consistent with an Alzheimer-type profile". This is a hedged pattern per the style guide; please confirm the wording.

## Reports added per case

Short labels; the full line per report (with where it is stored) is in each case log under "## Library contradictions (25 Oct 2026)".

### FEPI-TEMP

- FEPI-TEMP-M01 (7): analyze_eeg ambulatory; analyze_eeg video; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; interpret_labs AED_levels
- FEPI-TEMP-M02 (7): analyze_eeg ambulatory; analyze_eeg video; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; interpret_labs AED_levels
- FEPI-TEMP-M03 (7): analyze_eeg video; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; interpret_labs AED_levels; interpret_labs HbA1c
- FEPI-TEMP-M04 (6): analyze_eeg ambulatory; analyze_eeg video; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; interpret_labs AED_levels
- FEPI-TEMP-M05 (6): analyze_eeg ambulatory; order_advanced_imaging FDG_PET; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; interpret_labs AED_levels
- FEPI-TEMP-P01 (5): analyze_eeg ambulatory; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; interpret_labs AED_levels
- FEPI-TEMP-P02 (8): analyze_eeg routine; analyze_eeg ambulatory; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; perform_clinical_assessment cognitive_screen; interpret_labs valproate_level
- FEPI-TEMP-P03 (7): analyze_eeg ambulatory; order_advanced_imaging FDG_PET; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; interpret_labs AED_levels
- FEPI-TEMP-P04 (2): analyze_eeg ambulatory; interpret_labs AED_levels
- FEPI-TEMP-P05 (6): analyze_eeg ambulatory; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; interpret_labs AED_levels
- FEPI-TEMP-RM01 (9): analyze_eeg ambulatory; analyze_eeg video; order_advanced_imaging FDG_PET; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; perform_clinical_assessment cognitive_screen; interpret_labs AED_levels
- FEPI-TEMP-RM02 (9): analyze_eeg ambulatory; analyze_eeg video; order_advanced_imaging FDG_PET; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; order_echocardiogram TTE; order_echocardiogram TEE
- FEPI-TEMP-RM03 (9): analyze_eeg ambulatory; analyze_eeg video; order_advanced_imaging FDG_PET; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; perform_clinical_assessment cognitive_screen; interpret_labs valproate_level
- FEPI-TEMP-RM04 (8): analyze_eeg ambulatory; analyze_eeg video; order_advanced_imaging FDG_PET; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; interpret_labs AED_levels; order_advanced_imaging MR_spectroscopy
- FEPI-TEMP-RP01 (7): analyze_eeg ambulatory; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; perform_clinical_assessment cognitive_screen; interpret_labs AED_levels
- FEPI-TEMP-RP02 (5): analyze_eeg video; interpret_labs valproate_level; order_echocardiogram TEE; order_body_imaging chest_CT; order_body_imaging lower_extremity_venous_duplex
- FEPI-TEMP-RP03 (15): analyze_eeg ambulatory; analyze_eeg video; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; interpret_labs valproate_level; order_body_imaging chest_abdomen_pelvis_CT; order_body_imaging chest_xray; order_body_imaging chest_CTA; order_body_imaging pelvis_abdomen_MRI; order_body_imaging pelvis_abdomen_ultrasound; order_advanced_imaging MR_spectroscopy; order_advanced_imaging perfusion_MRI; order_advanced_imaging amino_acid_PET; order_advanced_imaging whole_body_FDG_PET
- FEPI-TEMP-RP04 (7): analyze_eeg routine; analyze_eeg ambulatory; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; interpret_labs valproate_level; interpret_labs HbA1c
- FEPI-TEMP-RP05 (5): analyze_eeg ambulatory; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; interpret_labs AED_levels
- FEPI-TEMP-RS01 (6): analyze_eeg ambulatory; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; interpret_labs AED_levels
- FEPI-TEMP-RS02 (10): analyze_eeg ambulatory; analyze_eeg video; order_advanced_imaging FDG_PET; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; interpret_labs valproate_level; interpret_labs beta-hCG; interpret_labs D_dimer
- FEPI-TEMP-RS03 (8): analyze_eeg ambulatory; analyze_eeg video; order_advanced_imaging FDG_PET; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; interpret_labs valproate_level
- FEPI-TEMP-RS04 (6): analyze_eeg routine; analyze_eeg ambulatory; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; interpret_labs iron_studies
- FEPI-TEMP-RS05 (9): analyze_eeg ambulatory; analyze_eeg video; order_advanced_imaging FDG_PET; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; interpret_labs AED_levels; order_echocardiogram TEE
- FEPI-TEMP-S01 (7): analyze_eeg ambulatory; analyze_eeg video; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; interpret_labs AED_levels
- FEPI-TEMP-S02 (8): analyze_eeg ambulatory; analyze_eeg video; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; interpret_labs AED_levels; interpret_labs iron_studies
- FEPI-TEMP-S03 (7): analyze_eeg ambulatory; analyze_eeg video; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; interpret_labs AED_levels
- FEPI-TEMP-S04 (7): analyze_eeg ambulatory; analyze_eeg video; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; interpret_labs AED_levels
- FEPI-TEMP-S05 (8): analyze_eeg ambulatory; analyze_eeg video; order_advanced_imaging FDG_PET; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; order_specialized_test neuropsych_battery; interpret_labs AED_levels
- FEPI-TEMP-S06 (7): analyze_eeg ambulatory; analyze_eeg video; order_advanced_imaging FDG_PET; obtain_tissue_diagnosis resection; obtain_tissue_diagnosis stereotactic_biopsy; obtain_tissue_diagnosis open_biopsy; interpret_labs AED_levels

### GLIO-HG

- GLIO-HG-M01 (14): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; neuropsych_battery; speech_language_evaluation; visual_field_perimetry
- GLIO-HG-M02 (14): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; neuropsych_battery; speech_language_evaluation; visual_field_perimetry
- GLIO-HG-M03 (14): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; neuropsych_battery; speech_language_evaluation; visual_field_perimetry
- GLIO-HG-M04 (12): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; gait_and_balance_timed; labs AED_levels
- GLIO-HG-M05 (13): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; neuropsych_battery; speech_language_evaluation
- GLIO-HG-P01 (13): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; DTI_tractography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; neuropsych_battery
- GLIO-HG-P02 (21): order_ct_scan; obtain_tissue_diagnosis open_biopsy; obtain_tissue_diagnosis resection; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; DTI_tractography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery; visual_field_perimetry; optical_coherence_tomography; analyze_csf; whole_body_FDG_PET; pelvis_abdomen_ultrasound; pelvis_abdomen_MRI
- GLIO-HG-P03 (14): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; DTI_tractography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery
- GLIO-HG-P04 (15): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; DTI_tractography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery; visual_field_perimetry
- GLIO-HG-P05 (12): obtain_tissue_diagnosis open_biopsy; obtain_tissue_diagnosis resection; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; DTI_tractography; video EEG; ambulatory EEG; structured_headache_history_ichd3; gait_and_balance_timed
- GLIO-HG-RM01 (16): order_ct_scan; obtain_tissue_diagnosis open_biopsy; obtain_tissue_diagnosis resection; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; DTI_tractography; video EEG; ambulatory EEG; cognitive_screen; gait_and_balance_timed; neuropsych_battery; speech_language_evaluation; baep
- GLIO-HG-RM02 (8): order_ct_scan; obtain_tissue_diagnosis stereotactic_biopsy; video EEG; ambulatory EEG; structured_headache_history_ichd3; gait_and_balance_timed; ssep; vep
- GLIO-HG-RM03 (14): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; gait_and_balance_timed; visual_field_perimetry; optical_coherence_tomography; labs iron_studies
- GLIO-HG-RM04 (15): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery; speech_language_evaluation; visual_field_perimetry
- GLIO-HG-RP01 (15): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; DTI_tractography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery; speech_language_evaluation
- GLIO-HG-RP02 (16): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery; chest_xray; chest_CTA; labs IGRA
- GLIO-HG-RP03 (17): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; DTI_tractography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery; speech_language_evaluation; chest_xray; labs AED_levels
- GLIO-HG-RP04 (15): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; DTI_tractography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery; visual_field_perimetry
- GLIO-HG-RS01 (16): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery; audiometry; MR_venography; whole_body_FDG_PET
- GLIO-HG-RS02 (15): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery; visual_field_perimetry; optical_coherence_tomography
- GLIO-HG-RS03 (13): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; gait_and_balance_timed; visual_field_perimetry; optical_coherence_tomography
- GLIO-HG-RS04 (17): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery; speech_language_evaluation; visual_field_perimetry; optical_coherence_tomography; labs AED_levels
- GLIO-HG-RS05 (15): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery; speech_language_evaluation; visual_field_perimetry
- GLIO-HG-RS06 (15): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery; speech_language_evaluation; visual_field_perimetry
- GLIO-HG-S01 (13): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery
- GLIO-HG-S02 (14): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery; visual_field_perimetry
- GLIO-HG-S03 (13): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery
- GLIO-HG-S04 (14): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery; visual_field_perimetry
- GLIO-HG-S05 (15): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3; cognitive_screen; gait_and_balance_timed; neuropsych_battery; visual_field_perimetry; functional_MRI
- GLIO-HG-S06 (10): order_ct_scan; obtain_tissue_diagnosis open_biopsy; FDG_PET; amino_acid_PET; CT_perfusion; perfusion_SPECT; cerebral_angiography; video EEG; ambulatory EEG; structured_headache_history_ichd3

### MIG-AURA

- MIG-AURA-P05 (1): labs coagulation
- MIG-AURA-P07 (8): visual_field_perimetry; TEE; FDG_PET; perfusion_MRI; CT_perfusion; perfusion_SPECT; DTI_tractography; MR_spectroscopy
- MIG-AURA-P08 (14): EEG routine; EEG ambulatory; EEG video; visual_field_perimetry; audiometry; muscle_biopsy; bubble_study; TEE; exercise_echo; FDG_PET; perfusion_MRI; CT_perfusion; perfusion_SPECT; DTI_tractography
- MIG-AURA-P09 (1): cerebral_angiography
- MIG-AURA-RM11 (6): EEG ambulatory; visual_field_perimetry; speech_language_evaluation; cognitive_screen; gait_and_balance_timed; performance_status

### PD

- PD-M01 (7): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; olfactory_test; MIBG_scan; HbA1c 7.1%
- PD-M02 (6): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; MIBG_scan; HbA1c 7.4%
- PD-M03 (6): levodopa_challenge; gait_and_balance_timed; speech_language_evaluation; olfactory_test; MIBG_scan; HbA1c 6.9%
- PD-M04 (4): levodopa_challenge; gait_and_balance_timed; cognitive_screen; MIBG_scan
- PD-M05 (5): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; MIBG_scan
- PD-P01 (5): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; FDG_PET
- PD-P02 (7): levodopa_challenge; gait_and_balance_timed; cognitive_screen; olfactory_test; autonomic_testing; tilt_table; analyze_eeg routine
- PD-P03 (5): levodopa_challenge; gait_and_balance_timed; cognitive_screen; orthostatic_blood_pressure; speech_language_evaluation
- PD-P04 (6): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; olfactory_test; MIBG_scan
- PD-RM01 (7): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; olfactory_test; MIBG_scan; HbA1c 7.8%
- PD-RM02 (5): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; MIBG_scan
- PD-RM03 (5): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; MIBG_scan
- PD-RM04 (6): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; MIBG_scan; HbA1c 6.8%
- PD-RM05 (6): levodopa_challenge; gait_and_balance_timed; cognitive_screen; orthostatic_blood_pressure; speech_language_evaluation; MIBG_scan
- PD-RP01 (6): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; autonomic_testing; tilt_table
- PD-RP02 (6): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; autonomic_testing; tilt_table
- PD-RP03 (5): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; FDG_PET
- PD-RP04 (3): gait_and_balance_timed; cognitive_screen; speech_language_evaluation
- PD-RP05 (7): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; MIBG_scan; HbA1c 7.2%; BMP
- PD-RS01 (5): levodopa_challenge; gait_and_balance_timed; orthostatic_blood_pressure; speech_language_evaluation; MIBG_scan
- PD-RS02 (7): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; olfactory_test; MIBG_scan; HbA1c 6.7%
- PD-RS03 (6): levodopa_challenge; gait_and_balance_timed; cognitive_screen; orthostatic_blood_pressure; olfactory_test; MIBG_scan
- PD-RS04 (7): levodopa_challenge; gait_and_balance_timed; cognitive_screen; orthostatic_blood_pressure; speech_language_evaluation; olfactory_test; MIBG_scan
- PD-RS05 (5): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; MIBG_scan
- PD-S01 (5): levodopa_challenge; gait_and_balance_timed; speech_language_evaluation; olfactory_test; MIBG_scan
- PD-S02 (6): levodopa_challenge; gait_and_balance_timed; speech_language_evaluation; olfactory_test; MIBG_scan; HbA1c 7.0%
- PD-S03 (7): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; olfactory_test; MIBG_scan; HbA1c 6.9%
- PD-S04 (5): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; MIBG_scan
- PD-S05 (5): levodopa_challenge; gait_and_balance_timed; speech_language_evaluation; MIBG_scan; HbA1c 6.8%
- PD-S06 (5): levodopa_challenge; gait_and_balance_timed; cognitive_screen; speech_language_evaluation; MIBG_scan

### VASC-DEM

- VASC-DEM-M01 (7): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; TEE; DTI_tractography; pelvis_abdomen_ultrasound
- VASC-DEM-M02 (10): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; levodopa_challenge; TEE; emg_ncs; ssep; skin_biopsy_iencf; DTI_tractography
- VASC-DEM-M03 (18): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; neuropsych_battery; gait_and_balance_timed; levodopa_challenge; TEE; cardiac_MRI; coronary_angiography; coronary_CTA; DTI_tractography; CT_perfusion; perfusion_MRI; MR_angiography; cerebral_angiography; functional_MRI; BNP
- VASC-DEM-M04 (8): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; speech_language_evaluation; DTI_tractography; CT_perfusion; perfusion_MRI
- VASC-DEM-M05 (12): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; tau_PET; gait_and_balance_timed; levodopa_challenge; TEE; ssep; DTI_tractography; MR_angiography; cerebral_angiography
- VASC-DEM-M06 (15): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; gait_and_balance_timed; levodopa_challenge; TEE; cardiac_MRI; DTI_tractography; CT_perfusion; perfusion_MRI; chest_abdomen_pelvis_CT; chest_CTA; mediastinum_CT; chest_xray
- VASC-DEM-M07 (12): perfusion_SPECT; performance_status; exercise_stress_test; tau_PET; gait_and_balance_timed; levodopa_challenge; TEE; cardiac_MRI; electrophysiology_study; speech_language_evaluation; DTI_tractography; BNP
- VASC-DEM-M08 (18): perfusion_SPECT; performance_status; exercise_stress_test; tau_PET; gait_and_balance_timed; levodopa_challenge; TEE; cardiac_MRI; electrophysiology_study; speech_language_evaluation; emg_ncs; DTI_tractography; spine_MRI; spine_CT; pelvis_abdomen_MRI; pelvis_abdomen_CT; pelvis_abdomen_ultrasound; BNP
- VASC-DEM-M09 (13): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; gait_and_balance_timed; levodopa_challenge; TEE; cardiac_MRI; speech_language_evaluation; ssep; DTI_tractography; CT_perfusion; perfusion_MRI
- VASC-DEM-M10 (17): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; gait_and_balance_timed; levodopa_challenge; TEE; cardiac_MRI; electrophysiology_study; visual_field_perimetry; DTI_tractography; CT_perfusion; perfusion_MRI; cerebral_angiography; transcranial_doppler; urinalysis; BNP
- VASC-DEM-P01 (10): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; tau_PET; levodopa_challenge; TEE; speech_language_evaluation; emg_ncs; DTI_tractography
- VASC-DEM-P02 (10): perfusion_SPECT; performance_status; exercise_stress_test; tau_PET; TEE; emg_ncs; polysomnography; DTI_tractography; spine_MRI; spine_CT
- VASC-DEM-P03 (8): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; TEE; DTI_tractography; CT_perfusion; perfusion_MRI
- VASC-DEM-P04 (15): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; amyloid_PET; gait_and_balance_timed; levodopa_challenge; TEE; cardiac_MRI; electrophysiology_study; visual_field_perimetry; DTI_tractography; CT_perfusion; perfusion_MRI; BNP
- VASC-DEM-P05 (8): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; levodopa_challenge; speech_language_evaluation; structured_headache_history_ichd3; DTI_tractography
- VASC-DEM-P06 (13): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; levodopa_challenge; TEE; cardiac_MRI; speech_language_evaluation; polysomnography; respiratory_function; orthostatic_blood_pressure; tilt_table; DTI_tractography
- VASC-DEM-P07 (7): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; levodopa_challenge; TEE; DTI_tractography
- VASC-DEM-P08 (28): brain MRI; FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; gait_and_balance_timed; levodopa_challenge; TEE; cardiac_MRI; electrophysiology_study; speech_language_evaluation; CT_perfusion; cerebral_angiography; DTI_tractography; perfusion_MRI; MR_angiography; functional_MRI; MR_spectroscopy; MR_venography; holter_24h; chest_abdomen_pelvis_CT; chest_CTA; mediastinum_CT; chest_xray; spine_MRI; mediastinum_MRI; pelvis_abdomen_MRI; peripheral_nerve_MRI
- VASC-DEM-P09 (6): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; TEE; structured_headache_history_ichd3
- VASC-DEM-S01 (8): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; levodopa_challenge; TEE; emg_ncs; DTI_tractography
- VASC-DEM-S02 (10): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; levodopa_challenge; TEE; speech_language_evaluation; polysomnography; respiratory_function; DTI_tractography
- VASC-DEM-S03 (11): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; levodopa_challenge; TEE; speech_language_evaluation; DTI_tractography; pelvis_abdomen_MRI; pelvis_abdomen_CT; pelvis_abdomen_ultrasound
- VASC-DEM-S04 (12): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; levodopa_challenge; TEE; emg_ncs; ssep; skin_biopsy_iencf; DTI_tractography; urinalysis; homocysteine
- VASC-DEM-S05 (12): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; levodopa_challenge; TEE; cardiac_MRI; speech_language_evaluation; respiratory_function; DTI_tractography; chest_abdomen_pelvis_CT; chest_CTA
- VASC-DEM-S06 (17): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; gait_and_balance_timed; levodopa_challenge; TEE; cardiac_MRI; electrophysiology_study; speech_language_evaluation; DTI_tractography; CT_perfusion; perfusion_MRI; MR_angiography; cerebral_angiography; functional_MRI; BNP
- VASC-DEM-S07 (13): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; gait_and_balance_timed; levodopa_challenge; TEE; DTI_tractography; CT_perfusion; perfusion_MRI; MR_angiography; cerebral_angiography; pelvis_abdomen_ultrasound
- VASC-DEM-S08 (20): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; gait_and_balance_timed; levodopa_challenge; TEE; cardiac_MRI; coronary_angiography; coronary_CTA; speech_language_evaluation; DTI_tractography; CT_perfusion; perfusion_MRI; cerebral_angiography; transcranial_doppler; chest_abdomen_pelvis_CT; chest_CTA; mediastinum_CT; chest_xray
- VASC-DEM-S09 (6): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; TEE; structured_headache_history_ichd3
- VASC-DEM-S10 (9): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; gait_and_balance_timed; levodopa_challenge; TEE; speech_language_evaluation; DTI_tractography
- VASC-DEM-S11 (14): FDG_PET; perfusion_SPECT; performance_status; exercise_stress_test; gait_and_balance_timed; levodopa_challenge; TEE; ssep; DTI_tractography; CT_perfusion; perfusion_MRI; MR_angiography; cerebral_angiography; functional_MRI
