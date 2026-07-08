# Tool parameter vocabulary

This document defines the **closed** parameter vocabulary the gold-trajectory
authoring fleet (and any downstream agent) must use for the two catchall
diagnostic tools. Strict adherence keeps every `(tool_name, tool_parameters)`
pair globally comparable across cases and lets cost lookup, metric aggregation,
and inter-rater agreement work without per-case synonym normalization.

**Rule:** if a case's optimal_actions, useless_tools, or harmful_tools cite
`order_specialized_test` or `order_advanced_imaging`, the value of
`tool_parameters["test_type"]` or `tool_parameters["modality"]` MUST come from
the lists below. This document is the source of truth for case authoring and
review.

Non-catchall tools (`analyze_brain_mri`, `analyze_eeg`, `analyze_csf`, etc.)
have free-form parameters — only the two catchalls are vocabulary-constrained.

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
| `mslt` | Multiple sleep latency test | Narcolepsy diagnosis (post-PSG) |
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

---

## `order_advanced_imaging`

`tool_parameters["modality"]` ∈

| Key | Description | Typical indication |
| --- | --- | --- |
| `amyloid_PET` | Amyloid-β PET (florbetapir, florbetaben, flutemetamol) | AD biomarker confirmation |
| `tau_PET` | Tau PET (flortaucipir) | AD tau staging, FTD tauopathy |
| `FDG_PET` | 18F-FDG PET | AD vs FTD pattern, paraneoplastic, glioma grading |
| `DaTscan` | Dopamine transporter SPECT | PD vs essential tremor vs MSA-C |
| `MIBG_scan` | Cardiac 123I-MIBG | PD vs MSA differentiation (autonomic) |
| `perfusion_MRI` | DSC / ASL perfusion MRI | Tumor grading, ischemia, MELAS |
| `MR_spectroscopy` | 1H-MRS | Tumor (NAA/Cho), MELAS, leukodystrophy |
| `MR_angiography` | MRA (TOF, contrast-enhanced) | Vascular workup without contrast |
| `MR_venography` | MRV | Cerebral venous sinus thrombosis |
| `carotid_duplex` | Carotid Doppler ultrasound | Carotid stenosis, ischemic stroke workup |
| `transcranial_doppler` | TCD | Vasospasm in SAH, sickle-cell risk |

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
