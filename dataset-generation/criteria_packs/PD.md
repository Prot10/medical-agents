# Criteria pack: Parkinson's disease

**ICD-10:** G20
**Condition enum:** `NeurologicalCondition.PARKINSONS`
**Case ID prefix:** `PD`

---

## 1. Diagnostic criteria

MDS Clinical Diagnostic Criteria for PD (Postuma 2015). **Clinically
established PD** requires (a) parkinsonism (bradykinesia + at least one of:
rest tremor 4-6 Hz, rigidity), (b) absolute exclusion of red flag features,
(c) ≥2 supportive criteria, AND (d) no red flags. Supportive: clear and
dramatic beneficial response to levodopa, levodopa-induced dyskinesia,
rest tremor of a limb, presence of olfactory loss or cardiac sympathetic
denervation on MIBG. Absolute exclusion: cerebellar abnormalities,
downward vertical supranuclear gaze palsy (PSP), restricted clinically to
the lower extremities for ≥3 years, treatment with dopamine receptor
blocker, absence of response to high-dose levodopa, cortical sensory loss,
imaging of presynaptic dopamine system showing normal binding (rules out
neurodegenerative parkinsonism). Diagnosis is **clinical** + sometimes
supported by DaTscan when clinical uncertainty.

## 2. Standard workup hierarchy

**Required:**
- `interpret_labs` (CBC, CMP, TSH, B12, copper/ceruloplasmin if <50, HIV/RPR if risk) — exclude reversible mimics and Wilson's disease in young; baseline pre-medication [Postuma_2015]
- `analyze_brain_mri` — exclude vascular parkinsonism, NPH, structural cause; PD is normal on MRI; SWI may show "swallow tail sign" loss in PD (substantia nigra) [Schwarz_2014]
- `search_medical_literature` — confirm MDS criteria, levodopa challenge protocol, treatment options
- `check_drug_interactions` — pre-treatment review (dopamine antagonists worsen PD; serotonergic drugs + selegiline interaction; rasagiline + meperidine; amantadine + anticholinergics in elderly)

**Recommended:**
- `order_advanced_imaging` (`modality: DaTscan`) — when clinical uncertainty between PD and essential tremor, drug-induced parkinsonism, or other; DaTscan abnormal in PD/atypical parkinsonism, normal in essential tremor / drug-induced / functional [Marshall_2009]
- `order_specialized_test` (`test_type: neuropsych_battery`) — baseline cognitive screen; PD-MCI screening

**Optional:**
- `order_specialized_test` (`test_type: polysomnography`) — REM sleep behavior disorder, very strong PD prodrome marker
- `order_specialized_test` (`test_type: autonomic_testing`) — for atypical features suggesting MSA
- Specialist referral *(clinical action — `tool_name: null`, no tool call)* — movement disorders subspecialist

## 3. Tools that are typically USELESS

- `analyze_eeg` — non-specific
- `analyze_csf` — no role in typical PD; α-syn seed amplification (RT-QuIC) is emerging research tool
- `analyze_ecg` — only baseline for medication safety
- `order_echocardiogram` — only if specific cardiac concern (some PD medications)
- `order_cardiac_monitoring` — unrelated
- `order_ct_scan` — MRI superior
- `order_advanced_imaging` (`modality: amyloid_PET / FDG_PET / others`) — DaTscan is the relevant modality; others usually not indicated
- `order_specialized_test` (`emg_ncs / muscle_biopsy`) — peripheral testing not relevant

## 4. Tools that are HARMFUL / contraindicated

- `check_drug_interactions` MUST flag dopamine antagonists (typical and atypical antipsychotics — quetiapine and clozapine relatively safer; metoclopramide and prochlorperazine are common iatrogenic causes)

## 5. Sequence constraints

- `interpret_labs` → start levodopa (`soft`): baseline labs before therapy
- `analyze_brain_mri` → diagnosis confirmation (`soft`): exclude secondary parkinsonism before committing to PD diagnosis

## 6. Subtype variations

- **M (mild):** early PD with unilateral signs, mild bradykinesia + rest tremor; standard workup, levodopa trial
- **S (standard):** classic PD with bilateral asymmetric signs, levodopa-responsive; standard workup
- **P (progressive / advanced):** moderate-advanced PD with motor fluctuations, dyskinesia, cognitive changes; same workup + medication optimization, advanced therapy evaluation (DBS, infusion)
- **R (reverse / mimic):** essential tremor (postural/action tremor, no bradykinesia, no rest tremor at rest, family history common, alcohol response), drug-induced parkinsonism (recent dopamine blocker exposure, often symmetric, often resolves), vascular parkinsonism (lower-body predominant, stepwise, MRI vascular changes), MSA (early dysautonomia, cerebellar features, poor levodopa response), PSP (vertical gaze palsy, early falls, axial > limb rigidity), corticobasal syndrome (asymmetric apraxia, cortical sensory loss, alien limb), DLB (early cognitive fluctuations and visual hallucinations); workup adds DaTscan (positive in PD/atypical, negative in essential tremor/drug-induced/vascular), MIBG (decreased in PD, normal in atypical parkinsonisms), polysomnography for RBD

## 7. Common red-herring categories

- **Symmetric onset** — less typical PD; consider atypical or drug-induced
- **Rapid progression / falls early** — red flag for atypical parkinsonism (PSP, MSA)
- **Early cognitive decline** — DLB on differential
- **Anti-emetic exposure (metoclopramide, prochlorperazine, promethazine)** — drug-induced parkinsonism; reversible
- **Normal DaTscan with parkinsonism** — vascular, drug-induced, functional, or essential tremor mistaken for PD
- **Family history of "tremor"** — could be ET or familial PD; clinical features distinguish

## 8. Allowed citations

- `[Postuma_2015]` — Postuma RB et al. MDS clinical diagnostic criteria for Parkinson's disease. Mov Disord 2015;30:1591-1601
- `[Berg_2015]` — Berg D et al. MDS research criteria for prodromal Parkinson's disease. Mov Disord 2015;30:1600-1611
- `[Marshall_2009]` — Marshall VL et al. Parkinson's disease is overdiagnosed clinically at baseline in diagnostically uncertain cases: a 3-year EU multicenter study with repeat (123I)FP-CIT SPECT. Mov Disord 2009;24:500-508
- `[Schwarz_2014]` — Schwarz ST et al. The "swallow tail" appearance of the healthy nigrosome — a new accurate test of Parkinson's disease. PLoS One 2014;9:e93814
- `[Postuma_2019]` — Postuma RB et al. The new diagnostic criteria for Parkinson's disease. Int Rev Neurobiol 2019;144:1-29
- `[Tolosa_2021]` — Tolosa E et al. Challenges in the diagnosis of Parkinson's disease. Lancet Neurol 2021;20:385-397
