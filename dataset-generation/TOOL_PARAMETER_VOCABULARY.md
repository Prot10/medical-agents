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
| `pure_tone_audiometry` | Formal pure-tone audiometry | Sensorineural hearing loss (bacterial meningitis) |
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
| `FDG_PET` | 18F-FDG PET | AD vs FTD pattern, paraneoplastic, glioma grading |
| `DaTscan` | Dopamine transporter SPECT | PD vs essential tremor vs MSA-C |
| `MIBG_scan` | Cardiac 123I-MIBG | PD vs MSA differentiation (autonomic) |
| `perfusion_MRI` | DSC / ASL perfusion MRI (brain) | Tumor grading, ischemia, MELAS |
| `cardiac_MRI` | Cardiac MRI with LGE | Cardiac syncope substrate, ARVC, myocarditis |
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
