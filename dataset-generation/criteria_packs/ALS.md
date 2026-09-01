# Criteria pack: Amyotrophic Lateral Sclerosis (ALS)

**ICD-10:** G12.21
**Condition enum:** `NeurologicalCondition.ALS`
**Case ID prefix:** `ALS`

---

## 1. Diagnostic criteria

Awaji-shima 2008 (revised El Escorial) criteria. Diagnosis rests on (a)
clinical or electrophysiological evidence of LOWER motor neuron degeneration,
(b) clinical evidence of UPPER motor neuron degeneration, (c) progressive
spread within a region or to other regions, AND (d) absence of evidence of
other disease processes that could explain the picture (Awaji 2008; Gold
Coast criteria 2020 simplify by requiring UMN + LMN in ≥1 region or LMN in
≥2 regions). Fasciculation potentials with abnormal morphology are
electrodiagnostic equivalents of fibrillations under Awaji.

## 2. Standard workup hierarchy

**Required:**
- `order_specialized_test` (`test_type: emg_ncs`) — bulbar + ≥2 spinal regions; documents LMN signs (fibs/PSWs, complex fasciculation potentials, reduced motor unit recruitment) [Awaji_2008]
- `analyze_brain_mri` — exclude an *intracranial* structural mimic (MS, brainstem tumour, multi-infarct disease) [AAN_2009]
- `order_body_imaging` (`study: spine_MRI`) — cervical and thoracic cord, to exclude compressive myelopathy and radiculopathy. This is the mimic that must be excluded before a motor neuron disease diagnosis, and it is a **separate study**: it used to be carried as an `include_cervical_spine` annotation on the brain MRI, which the brain tool has no parameter for and drops, so the exclusion was neither orderable nor scoreable [AAN_2009]
- `interpret_labs` (CK, B12, TSH, HbA1c, +/- HIV, RPR) — exclude reversible mimics; CK often elevated 2–5×ULN in ALS, >10× suggests myopathy [AAN_2009]
- `search_medical_literature` — confirm diagnostic thresholds; document AAN practice parameter [AAN_2009]

**Recommended:**
- `order_specialized_test` (`test_type: respiratory_function`) — FVC + MIP/MEP at baseline (informs prognosis and riluzole timing) [AAN_2009]
- `order_specialized_test` (`test_type: genetic_panel:ALS`) — when family history positive or young onset (<45) [Brown_2017]
- `order_body_imaging` (`study: spine_MRI`, lumbar) — where the LMN signs are lumbosacral and a radiculopathy is the competing explanation. Never as a region annotation on the brain MRI

**Optional:**
- `check_drug_interactions` — if considering riluzole or edaravone

## 3. Tools that are typically USELESS

- `analyze_eeg` — no role in ALS diagnosis; non-cortical motor disease
- `analyze_csf` — non-specific; LP not part of routine ALS workup unless atypical features
- `analyze_ecg` — unrelated unless comorbid cardiac disease
- `order_echocardiogram` — unrelated
- `order_cardiac_monitoring` — unrelated
- `order_ct_scan` — MRI is standard; CT only if MRI contraindicated
- `order_advanced_imaging` (`modality: amyloid_PET / DaTscan / etc.`) — none indicated for typical ALS

## 4. Tools that are HARMFUL / contraindicated

(none routinely — ALS workup has no major harmful tool calls)

## 5. Sequence constraints

(none required clinically — EMG and MRI are independent prerequisites)

## 6. Subtype variations

- **M (mild):** typical presentation, single-region onset; standard workup
- **S (standard):** multi-region or bulbar onset; standard workup + respiratory function moves to REQUIRED
- **P (progressive):** rapid progression or respiratory involvement; add `order_specialized_test` (`respiratory_function`) at REQUIRED; consider genetic panel if young
- **R (reverse / mimic):** the case is NOT ALS — typical mimics are MMN with conduction block (treatable!), Kennedy disease, IBM, cervical myelopathy, post-polio. For R cases the action policy adds rule-out criteria: anti-GM1 antibodies (under labs), repeat EMG with NCS for conduction block, MRI cervical spine

## 7. Common red-herring categories

- **Prior benign fasciculation diagnosis** — never closes the door on ALS; repeat EMG mandatory
- **Mild CK elevation** — does NOT rule in myopathy; ALS CK is often elevated
- **Cervical spine degeneration on MRI** — coincidental in age group; does not explain bulbar signs
- **Normal initial EMG** — early ALS has normal EMG; serial studies needed (Awaji acknowledges this)
- **Symmetric weakness** — uncommon in ALS but does occur, especially flail-arm variant

## 8. Allowed citations

- `[Awaji_2008]` — de Carvalho M et al. Electrodiagnostic criteria for diagnosis of ALS. Clin Neurophysiol 2008;119:497-503
- `[AAN_2009]` — Miller RG et al. Practice Parameter update: The care of the patient with ALS. AAN Practice Parameter, Neurology 2009;73:1218-1226
- `[Gold_Coast_2020]` — Shefner JM et al. A proposal for new diagnostic criteria for ALS. Clin Neurophysiol 2020;131:1975-1978
- `[Brown_2017]` — Brown RH, Al-Chalabi A. Amyotrophic Lateral Sclerosis. NEJM 2017;377:162-172
- `[ENCALS_2018]` — Westeneng HJ et al. Prognosis for patients with ALS: the ENCALS prediction model. Lancet Neurol 2018;17:423-433
