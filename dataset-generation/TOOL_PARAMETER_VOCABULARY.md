# Tool parameter vocabulary

This document defines the **closed** parameter vocabulary the gold-trajectory
authoring fleet (and any downstream agent) must use for the two catchall
diagnostic tools. Strict adherence keeps every `(tool_name, tool_parameters)`
pair globally comparable across cases and lets cost lookup, metric aggregation,
and inter-rater agreement work without per-case synonym normalization.

> **This is now machine-enforced.** `agent-platform/config/tools/costs.yaml` is the single
> source of truth: `tools/vocabulary.py` reads it, the tool schemas generate their `enum`s
> from it, and `agent-platform/scripts/validation/validate_cases.py` checks every case
> against it. A term cannot exist in this document without also having a price and a tool
> that can order it. `agent-platform/tests/test_case_tool_contract.py` fails if the three
> ever disagree again.
>
> They did disagree, for a long time: the tool schemas exposed 6 of the 11 modalities and 9
> of the 19 test types below, so ground-truth values that were legal here were unorderable by
> the agent, and `CostTracker` — which read `imaging_type` while every case wrote `modality`
> — silently priced the wrong workup in 293 of 600 cases.
>
> To add a term: add the row to `costs.yaml`, then add it here. Nothing else.

**Rule:** if a case's optimal_actions, useless_tools, or harmful_tools cite
`order_specialized_test` or `order_advanced_imaging`, the value of
`tool_parameters["test_type"]` or `tool_parameters["modality"]` MUST come from
the lists below. This document is the source of truth for case authoring and
review.

Non-catchall tools (`analyze_brain_mri`, `analyze_eeg`, `analyze_csf`, etc.) are not
vocabulary-constrained in the same way, but their parameters are still checked:

* a key must be either a real parameter of that tool (see `ToolRegistry`) or a **documented
  descriptive annotation** — the per-tool allowlist lives in `ANNOTATION_KEYS` in
  `agent-platform/scripts/validation/validate_cases.py`. Annotations record clinical intent
  the tool does not take as an argument (`sequences`, `region`, `indication`); `CostTracker`
  ignores them. One canonical spelling each.
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
`special_tests`, or the basics get charged a second time.

`ground_truth.tool_parameters` is an **annotation of intent, not a complete tool call** — a
missing `clinical_context` is expected and fine. An unknown key is not.

---

## `order_specialized_test`

`tool_parameters["test_type"]` ∈

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

---

## `order_advanced_imaging`

`tool_parameters["modality"]` ∈

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
| `chest_CT` | Thoracic CT | Lung parenchyma, an intrathoracic mass |
| `chest_CTA` | Thoracic CT angiography | Pulmonary embolism, aortic dissection, when either must be confirmed or excluded rapidly. `order_ct_scan` images the head and neck only and cannot answer this |
| `chest_abdomen_pelvis_CT` | Staging / occult-primary CT, one acquisition | Paraneoplastic tumour search (anti-NMDAR, anti-Hu); excluding an extracranial primary before calling a lesion a primary brain tumour |
| `mediastinum_CT` / `_MRI` | Anterior mediastinum | Thymoma / thymic hyperplasia in myasthenia gravis — chest radiograph does not substitute |
| `spine_MRI` / `_CT` | Spinal cord and column | Cord compression, transverse myelitis, spinal tumour — the mimics of ascending flaccid weakness |
| `peripheral_nerve_MRI` / `_ultrasound` | Nerve / nerve root | Root enhancement, nerve enlargement (GBS vs acute-onset CIDP) |

`contrast` is a boolean modifier, as for brain MRI and CT.

### `order_microbiology.specimen`

| Value | Specimen | When |
|---|---|---|
| `blood_culture` | Two sets, with susceptibility | Suspected bacterial meningitis, sepsis, SBP |
| `whole_blood_pcr` | Meningococcus / pneumococcus PCR | Meningitis where culture may be negative |
| `throat_swab` | Meningococcal culture | Suspected meningococcal disease |
| `urine` | Urinalysis + culture | Infection screen as an HE precipitant |
| `ascitic_fluid` | Diagnostic paracentesis: PMN count, protein, culture | Every patient with ascites and altered mental status |

`before_antimicrobials` is a boolean: yield collapses once treatment has started, and the
report must state it rather than leave it inferred.

### `obtain_tissue_diagnosis`

`procedure` is `resection`, `stereotactic_biopsy` or `lymph_node_biopsy` (endobronchial needle
aspiration or surgical nodal sampling — the low-risk route to histological confirmation of a
systemic disease when the accessible node is not the symptomatic organ, e.g. hilar nodes in
cardiac sarcoidosis rather than an endomyocardial biopsy). A purely histological pattern needs
no molecular assay. `molecular_assays` is a list drawn from
`IDH1_IHC`, `IDH1_IDH2_sequencing`, `ATRX_IHC`, `1p_19q_codeletion`, `CDKN2A_B_deletion`,
`TERT_promoter`, `EGFR_amplification`, `chr7_gain_chr10_loss`, `H3K27_status`,
`MGMT_methylation`, `BRAF_V600`. Each assay is in the list because it changes management, not
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
