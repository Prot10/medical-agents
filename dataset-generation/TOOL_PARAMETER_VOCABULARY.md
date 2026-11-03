# Tool parameter vocabulary

This document defines the **closed** parameter vocabulary that clinical-policy
authors and downstream agents must use for the two catchall diagnostic tools. Strict
adherence keeps every `(tool_name, required_arguments)` pair globally comparable across cases and lets cost lookup, metric aggregation,
and inter-rater agreement work without per-case synonym normalization.

> **This is machine-enforced.** `agent-platform/config/tools/costs.yaml` is the pricing
> source of truth, tool schemas expose the accepted enums, policy patterns are checked by
> schema and contract tests, and every orderable term must have a defined cost.
>
> To add a term: add the row to `costs.yaml`, then add it here. Nothing else.

**Rule:** if an `action_criteria` or `avoided_actions` pattern cites
`order_specialized_test` or `order_advanced_imaging`, the value of
`required_arguments["test_type"]` or `required_arguments["modality"]` MUST come from
the lists below. This document is the source of truth for case authoring and
review.

Non-catchall tools (`analyze_brain_mri`, `analyze_eeg`, `analyze_csf`, etc.) are not
vocabulary-constrained in the same way, but their parameters are still checked:

* a key must be a real parameter of that tool's typed action schema. Clinical intent that
  does not affect execution belongs in the criterion label, evidence or rationale, not in a
  fabricated tool argument.
* an enum-typed parameter (`analyze_brain_mri.protocol`, `analyze_eeg.eeg_type`,
  `order_cardiac_monitoring.monitor_type`, …) must carry a legal value.

Two rules the whole laboratory vocabulary rests on:

* **One assay, one name.** `costs.yaml` may price several spellings of a name (`D-dimer` /
  `D_dimer`) and several *names* for one assay (`syphilis` / `RPR`, `paraneoplastic` /
  `paraneoplastic_panel`). `normalize_analyte()` folds both, so the score and the bill read them as
  one; `_ANALYTE_SYNONYMS` holds the second kind. Ground truth should use the canonical name — the
  one `lab_panels()` advertises.
* **One study, one tool.** Blood, urine and ascitic-fluid microbiology is
  `order_microbiology`, never an `interpret_labs` panel. Pricing the same study under two tools let
  either satisfy the ground truth.

`analyze_csf` deserves a note: `costs.yaml` prices the LP procedure together with cell count,
protein and glucose inside `analyze_csf.base`, and bills each entry of `special_tests`
separately. Put the always-done panel in the `basic` annotation and only billable assays in
`special_tests`, or the basics get charged a second time. Its optional `source` is
`lumbar_puncture` (default), `shunt_tap`, `external_ventricular_drain` or `lumbar_drain`
(extended lumbar drainage through a catheter, the drainage trial after a negative tap test; added
24 Oct 2026, NPH-P08), from the `analyze_csf.sources` block (priced at 0 except `lumbar_drain`,
CPT 62272 on top of `base`); a criterion names it only for a shunt tap, an EVD sample or a lumbar
drain. A stored CSF report states its `source` only when it is not a lumbar puncture. The October 2026 review added `mycobacterial_panel` (AFB smear, Xpert MTB/RIF Ultra,
mycobacterial culture), `fungal_culture`, `india_ink` and `ADA` to `special_tests`, and
`HIV_viral_load`, `CD4_count`, `beta2_transferrin`, `serum_cryptococcal_antigen` and `AFP` to the
laboratory panels (serum CrAg stays apart from the CSF `cryptococcal_antigen`: one specimen, one
tool). Its batch-2 conditions added `CMV_PCR` to `special_tests`, and `anti_GQ1b_IgG`,
`anti_GT1a_IgG` (two terms, not a ganglioside panel, which would price `anti-GM1 IgM` again),
`botulinum_toxin_assay` and `plasma_free_metanephrines` to the laboratory panels. Its batch-3
conditions added `toxoplasma_PCR` and `EBV_PCR` to `special_tests`, and `plasma_cholinesterase`
and `RBC_cholinesterase` (two assays, read differently in organophosphate poisoning), `NSE`
(post-arrest prognosis at 48 and 72 hours), `toxoplasma_IgG` and `urine_sodium` to the laboratory
panels. `B12` and `vitamin_B12` are one assay: `vitamin_B12` is advertised and `B12` resolves to
it through `_ANALYTE_SYNONYMS`. Batch 4 (24 Oct 2026) added `CDT` (carbohydrate-deficient
transferrin, FTD-M07). Batch 5 (25 Oct 2026) added `cysticercosis_serology` (serum Taenia
solium IgG, EITB or ELISA) and `IGRA` (QuantiFERON-TB Gold Plus or T-SPOT.TB), both for
FEPI-TEMP-RS02. Methylmalonic acid was already priced as `MMA`. `HBV_DNA` (quantitative hepatitis B viral load, HEP-ENC-S05) was added on the same day. One `panels` order that names assays stored in different payloads (the
first-line panels and a second-tier assay) receives each of them (`MockServer._merge_lab_order`).

`order_cardiac_monitoring.monitor_type` is `telemetry`, `holter_24h`, `holter_48h`,
`event_monitor_14d`, `event_monitor_30d`, `implantable_loop_recorder` or `device_interrogation`
(the stored diagnostics of a pacemaker, ICD or loop recorder already implanted; added on the
October 2026 review, VASC-DEM-P08). A stored monitoring report must carry its `monitor_type` as
one of these terms: the MockServer routes on it (see `docs/benchmark/tool-contract.md`).

A policy pattern's `required_arguments` is the minimum executable subset needed to match a
call. A missing optional runtime argument is expected; an unknown key is not.

---

## `order_specialized_test`

`required_arguments["test_type"]` ∈

| Key | Description | Notes |
| --- | --- | --- |
| `emg_ncs` | Standard nerve conduction studies + needle EMG | ALS / GBS / radiculopathy / peripheral neuropathy |
| `emg_single_fiber` | Single-fiber EMG | Myasthenia gravis (highest sensitivity) |
| `repetitive_nerve_stimulation` | RNS | MG (decrement), LEMS (incremental response) |
| `nerve_biopsy` | Sural / superficial peroneal nerve biopsy | Vasculitic / amyloid neuropathy |
| `muscle_biopsy` | Open or needle muscle biopsy | Myopathies, mitochondrial disease |
| `skin_biopsy_iencf` | Intraepidermal nerve fiber density | Small-fiber neuropathy |
| `neuropsych_battery` | Comprehensive cognitive testing | AD, FTD, NPH, MCI, FND |
| `polysomnography` | Overnight sleep study | RBD, OSA, narcolepsy |
| `tilt_table` | Head-up tilt table test | Syncope (vasovagal vs cardiac vs POTS) |
| `exercise_stress_test` | Graded exercise ECG stress test | Exertional syncope, ischemia, catecholaminergic arrhythmia |
| `vep` | Visual evoked potentials | MS optic pathway, demyelinating disease |
| `ssep` | Somatosensory evoked potentials | Myelopathy, brain death adjunct |
| `baep` | Brainstem auditory evoked potentials | Brainstem demyelination, CPA tumor |
| `autonomic_testing` | QSART, tilt-table-with-Valsalva panel | Autonomic neuropathy, MSA |
| `optical_coherence_tomography` | Retinal OCT | MS (RNFL thinning), optic neuritis |
| `visual_field_perimetry` | Humphrey/Goldmann VF | Chiasmal compression, MS |
| `ice_pack_test` | Bedside ice-pack ptosis test | MG (rapid screen) |
| `respiratory_function` | FVC, MIP/MEP, NIF | ALS respiratory monitoring, MG crisis risk |
| `minor_salivary_gland_biopsy` | Lip biopsy, focus score | Sjögren's confirmation |
| `audiometry` | Pure-tone and speech audiometry, tympanometry | Hearing loss after bacterial meningitis (WHO 2025, NICE NG240) |
| `speech_language_evaluation` | Speech-language pathology assessment: motor speech, grammar, naming, repetition, comprehension | Primary progressive aphasia variant (Gorno-Tempini 2011); not a second `neuropsych_battery` |
| `electrophysiology_study` | Invasive EP study: HV interval, sinus node recovery, programmed stimulation, accessory-pathway refractory period | Syncope with bifascicular block or prior infarction (ESC 2018), WPW risk stratification (ESC 2019 SVT) |
| `sodium_channel_blocker_challenge` | Ajmaline, flecainide or procainamide under 12-lead ECG with high precordial leads | Suspected Brugada syndrome with a non-diagnostic ECG (ESC 2022 VA/SCD) |
| `olfactory_test` | UPSIT or Sniffin' Sticks against age and sex norms | Hyposmia, a supportive MDS criterion of Parkinson's disease (Postuma 2015) |
| `genetic_panel:<panel>` | Targeted gene panel | See panel list below |

**Allowed genetic panels** (only these `<panel>` suffix values are valid):

| `<panel>` | Disease | Typical genes |
| --- | --- | --- |
| `ALS` | ALS / FTD-ALS | SOD1, C9orf72, TARDBP, FUS, TBK1 |
| `FTD` | Frontotemporal dementia | GRN, MAPT, C9orf72, CHMP2B |
| `HD` | Huntington's disease | HTT (CAG repeat) |
| `CADASIL` | Small-vessel ischemic disease | NOTCH3 |
| `CAA` | Cerebral amyloid angiopathy | APP |
| `early_onset_AD` | Early-onset Alzheimer | APP, PSEN1, PSEN2 |
| `hereditary_ataxia` | Spinocerebellar ataxias | SCA1–8, FRDA |
| `CMT` | Charcot-Marie-Tooth | PMP22, MPZ, GJB1, MFN2 |
| `HSP` | Hereditary spastic paraparesis | SPG4, SPG7, SPG11 |
| `mitochondrial` | Mitochondrial myopathy | mtDNA + nuclear |
| `MS_genetic_risk` | MS risk panel (research use only) | HLA-DRB1, etc. |
| `wilson` | Wilson disease | ATP7B |
| `porphyria` | Acute intermittent porphyria | HMBS, ALAS1, CPOX, PPOX |
| `small_fiber_neuropathy` | Hereditary small-fibre neuropathy | SCN9A, SCN10A, SCN11A |
| `PD` | Young-onset / monogenic Parkinson's | PRKN, PINK1, DJ-1, LRRK2, GBA, SNCA |
| `hereditary_paraganglioma` | Hereditary paraganglioma-phaeochromocytoma | SDHA/B/C/D, SDHAF2, VHL, RET, NF1, TMEM127, MAX, FH |
| `hemiplegic_migraine` | Familial and sporadic hemiplegic migraine | CACNA1A, ATP1A2, SCN1A, PRRT2 |
| `inherited_arrhythmia` | Long QT, Brugada, CPVT | KCNQ1, KCNH2, SCN5A, RYR2, CASQ2 and the minor channelopathy genes |
| `cardiomyopathy` | Arrhythmogenic, hypertrophic, dilated cardiomyopathy, laminopathy | PKP2, DSP, DSG2, LMNA, FLNC, MYH7, MYBPC3 and the sarcomere genes |

---

## `order_advanced_imaging`

`required_arguments["modality"]` ∈

| Key | Description | Typical indication |
| --- | --- | --- |
| `amyloid_PET` | Amyloid-β PET (florbetapir, florbetaben, flutemetamol) | AD biomarker confirmation |
| `tau_PET` | Tau PET (flortaucipir) | AD tau staging, FTD tauopathy |
| `FDG_PET` | 18F-FDG PET, brain | AD vs FTD pattern, paraneoplastic. NOT adequate for grading a primary brain tumour |
| `DaTscan` | Dopamine transporter SPECT | PD vs essential tremor vs MSA-C |
| `MIBG_scan` | Cardiac 123I-MIBG | PD vs MSA differentiation (autonomic) |
| `perfusion_MRI` | DSC / ASL perfusion MRI (brain) | Tumor grading, ischemia, MELAS |
| `cardiac_MRI` | Cardiac MRI with LGE | Cardiac syncope substrate, ARVC, myocarditis |
| `MR_spectroscopy` | 1H-MRS | Tumor (NAA/Cho), MELAS, leukodystrophy |
| `MR_angiography` | MRA (TOF, contrast-enhanced) | Vascular workup without contrast |
| `MR_venography` | MRV | Cerebral venous sinus thrombosis |
| `carotid_duplex` | Carotid Doppler ultrasound | Carotid stenosis, ischemic stroke workup |
| `transcranial_doppler` | TCD | Vasospasm in SAH, sickle-cell risk |
| `CT_perfusion` | CTP, automated core/penumbra | Extended-window thrombolysis, thrombectomy 6-24 h |
| `amino_acid_PET` | 11C-methionine or 18F-FET PET | High-grade glioma: active tumour vs necrosis/treatment effect, biopsy targeting. FDG is NOT adequate for primary brain tumours |
| `cardiac_FDG_PET` | 18F-FDG PET/CT, cardiac, with dietary suppression of myocardial glucose uptake | Active myocardial inflammation — cardiac sarcoidosis, myocarditis. A different study from `FDG_PET`, not the same scan read differently |
| `coronary_CTA` | Coronary CT angiography | Non-invasive coronary anatomy when ischaemia is suspected |
| `coronary_angiography` | Invasive catheter coronary angiography | Suspected myocardial ischaemia or infarction (ESC 2018 Class IIa in syncope). An angiographic finding alone does not establish the cause of a symptom |
| `functional_MRI` | BOLD fMRI, motor and language paradigms | Pre-surgical mapping and language lateralisation near eloquent cortex (high-grade glioma) |
| `DTI_tractography` | Diffusion tensor tractography | Corticospinal tract, arcuate fasciculus, optic radiations before resection |
| `whole_body_FDG_PET` | 18F-FDG PET/CT, skull base to mid-thigh | Occult-malignancy search in a paraneoplastic syndrome when CT is negative (Graus 2021). A different acquisition from the cerebral `FDG_PET` |

---

## Tools added after the July 2026 clinical tool review

The reviewers' structural finding: the action space could only image the brain and could not
obtain a specimen, so several conditions had a mandatory diagnostic step with no callable
act. Each new tool has one discriminating parameter backed by a `by_type` block, exactly like
`order_advanced_imaging`.

### `order_body_imaging.study`

Region and modality are one term, because a CT and an MRI of the same region are different
studies at different prices.

| Value | Study | When |
|---|---|---|
| `pelvis_abdomen_CT` / `_MRI` / `_ultrasound` | Pelvic + abdominal imaging | Ovarian teratoma in anti-NMDAR encephalitis; portosystemic shunts in refractory hepatic encephalopathy |
| `testicular_ultrasound` | Scrotal ultrasound | Selected male anti-NMDAR encephalitis tumour screening |
| `chest_CT` | Thoracic CT | Lung parenchyma, an intrathoracic mass |
| `chest_CTA` | Thoracic CT angiography | Pulmonary embolism, aortic dissection, when either must be confirmed or excluded rapidly. `order_ct_scan` images the head and neck only and cannot answer this |
| `chest_abdomen_pelvis_CT` | Staging / occult-primary CT, one acquisition | Paraneoplastic tumour search (anti-NMDAR, anti-Hu); excluding an extracranial primary before calling a lesion a primary brain tumour |
| `mediastinum_CT` / `_MRI` | Anterior mediastinum | Thymoma / thymic hyperplasia in myasthenia gravis — chest radiograph does not substitute |
| `spine_MRI` / `_CT` | Spinal cord and column | Cord compression, transverse myelitis, spinal tumour — the mimics of ascending flaccid weakness |
| `peripheral_nerve_MRI` / `_ultrasound` | Nerve / nerve root | Root enhancement, nerve enlargement (GBS vs acute-onset CIDP) |
| `lower_extremity_venous_duplex` | Compression and Doppler ultrasound of the leg veins | Deep vein thrombosis as the venous source of a paradoxical embolism (stroke with a PFO) |
| `chest_xray` | Two-view chest radiograph | First-line chest image, e.g. pneumonia in the infection screen of hepatic encephalopathy |
| `temporal_artery_ultrasound` | Temporal (and axillary) artery ultrasound | Halo sign in suspected giant cell arteritis |

`contrast` is a boolean modifier, as for brain MRI and CT.

### `order_microbiology.specimen`

| Value | Specimen | When |
|---|---|---|
| `blood_culture` | Two sets, with susceptibility | Suspected bacterial meningitis, sepsis, SBP |
| `whole_blood_pcr` | EDTA whole-blood PCR: N. meningitidis, S. pneumoniae, H. influenzae | Suspected meningococcal disease (NICE NG240), above all when the LP is deferred; meningitis where culture may be negative |
| `throat_swab` | Meningococcal culture | Suspected meningococcal disease |
| `urine` | Urinalysis + culture | Infection screen as an HE precipitant |
| `ascitic_fluid` | Diagnostic paracentesis: PMN count, protein, culture | Every patient with ascites and altered mental status |
| `sputum` | Gram stain and culture (AFB smear, mycobacterial culture on request) | Pneumonia as an infective precipitant; pulmonary TB with tuberculous meningitis |
| `stool` | C. difficile toxin PCR | Diarrhoea in the infection screen (hepatic encephalopathy on lactulose) |
| `wound_swab` | Culture of a wound or ulcer | A skin portal of entry (bacterial meningitis) |
| `brain_aspirate` | Gram stain, aerobic and anaerobic culture of aspirated brain-lesion material | Brain abscess on the differential of a ring-enhancing lesion. The aspiration is ordered through `obtain_tissue_diagnosis` and billed there |
| `tracheal_aspirate` | Gram stain and culture of endotracheal aspirate | Ventilator-associated pneumonia in an intubated patient (e.g. myasthenic crisis) |

`before_antimicrobials` is a boolean: yield collapses once treatment has started, and the
report must state it rather than leave it inferred.

### `obtain_tissue_diagnosis`

`procedure` is `resection`, `stereotactic_biopsy`, `open_biopsy` (through a laminectomy or
craniotomy, for a lesion a needle cannot reach safely and that is not to be resected, e.g. an
intramedullary spinal cord tumour), `temporal_artery_biopsy` (giant cell
arteritis) or `lymph_node_biopsy` (endobronchial needle
aspiration or surgical nodal sampling — the low-risk route to histological confirmation of a
systemic disease when the accessible node is not the symptomatic organ, e.g. hilar nodes in
cardiac sarcoidosis rather than an endomyocardial biopsy). A purely histological pattern needs
no molecular assay. `molecular_assays` is a list drawn from
`IDH1_IHC`, `IDH1_IDH2_sequencing`, `ATRX_IHC`, `1p_19q_codeletion`, `CDKN2A_B_deletion`,
`TERT_promoter`, `EGFR_amplification`, `chr7_gain_chr10_loss`, `H3K27_status`,
`MGMT_methylation`, `BRAF_V600`, and for the mimics of a glioma `CD20_IHC` and `EBER_ISH`
(primary CNS or EBV-associated lymphoma), `SOX10_IHC` and `Melan_A_HMB45_IHC` (metastatic
melanoma), `chromogranin_A_synaptophysin_IHC` (paraganglioma), `PAX8_IHC`, `TTF1_IHC` and
`thyroglobulin_IHC` (primary site of a metastatic carcinoma), and `H3G34_status` (diffuse
hemispheric glioma, H3 G34-mutant) and `DNA_methylation_profiling` (tumour class left open by
histology and targeted assays). Each assay is in the list because it changes management, not
to complete a taxonomy. MGMT must not be assessed by immunocytochemistry.

### `perform_clinical_assessment.assessment_type`

Deliberately small and non-overlapping with `order_specialized_test`: a full battery is
`neuropsych_battery`, bedside spirometry is `respiratory_function`, formal autonomic testing
is `autonomic_testing`. Duplicating a study under two tools would let either satisfy the
ground truth.

| Value | Assessment | When |
|---|---|---|
| `cognitive_screen` | MoCA / MMSE with informant history | First step in suspected cognitive decline, before imaging |
| `structured_headache_history_ichd3` | Headache and aura features against ICHD-3 | Migraine with aura — the actual confirmatory step |
| `gait_and_balance_timed` | Timed Up and Go, timed walk | NPH, before *and* after the CSF tap test (two assessments) |
| `functional_neuro_signs` | Hoover's sign, entrainment | Functional neurological disorder — a positive clinical diagnosis |
| `performance_status` | Karnofsky and ECOG at the visit | Treatment planning in high-grade glioma (KPS < 70 unfavourable) |
| `orthostatic_blood_pressure` | Supine BP and HR, then at 1 and 3 minutes of active standing | Initial evaluation of syncope (ESC 2018, Class I); antihypertensive or diuretic treatment |
| `levodopa_challenge` | MDS-UPDRS III OFF, then ON at peak effect of a supra-threshold levodopa dose, percent improvement | DBS candidacy (30% or more), a "poor levodopa response" red flag (MSA). One report with both states, not two `timing` orders |

`timing` (24 Oct 2026) is `baseline` (default) or `post_intervention`, from the `timings` block
(priced at 0). A stored assessment that repeats another after an intervention (the NPH gait after
the tap test) carries `timing: post_intervention`, the baseline report carries `timing: baseline`,
and the MockServer serves each for its own order. A criterion for the reassessment names
`timing: post_intervention`; one for the baseline may name `timing: baseline`, which the schema
default satisfies when the call leaves it out.

---

## Why this is closed

A few open-vocabulary entries would let two cases describe "the same test"
with slightly different strings (e.g., `EMG/NCS` vs `EMG and NCS` vs
`nerve conduction studies`) and the metric layer would see them as different
tools, inflating precision/recall noise. Closed vocabulary also pins cost
calculation: every entry above maps to a row in
`agent-platform/config/tools/costs.yaml` so `cost_efficiency` works without
fallback rates.

If the fleet finds a case that genuinely requires a test outside this list,
the agent must flag it in the case's `metadata.vocab_gap` rather than invent
a new value. We extend this list explicitly, after review.
