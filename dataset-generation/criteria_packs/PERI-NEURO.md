# Criteria pack: Peripheral neuropathy

**ICD-10:** G62.x, G63.x (multiple etiologies)
**Condition enum:** `NeurologicalCondition.PERIPHERAL_NEUROPATHY`
**Case ID prefix:** `PERI-NEURO`

---

## 1. Diagnostic criteria

AAN 2009 guidelines for distal symmetric polyneuropathy (DSP). Diagnosis is
**clinical + electrodiagnostic** + targeted etiologic workup. Classify by:
(a) fiber type — large fiber (numbness, weakness, reduced reflexes, EMG/NCS
abnormalities), small fiber (burning pain, autonomic features, EMG/NCS
often NORMAL; skin biopsy IENFD or QSART needed); (b) distribution —
symmetric distal (most common, "stocking-glove"), asymmetric/multifocal
(mononeuropathy multiplex — think vasculitis), proximal (CIDP, GBS); (c)
fiber predominance — sensory > motor > autonomic; (d) acuity — acute (GBS,
vasculitis, toxic), subacute (CIDP, paraneoplastic), chronic (diabetic,
idiopathic, hereditary). Diabetes mellitus is the most common cause in
developed countries (~50% of DSP); alcohol, B12 deficiency, monoclonal
gammopathy, hypothyroidism, medications, hereditary (CMT) make up much of
the rest.

## 2. Standard workup hierarchy

**Required (typical DSP):**
- `order_specialized_test` (`test_type: emg_ncs`) — characterize axonal vs demyelinating, distribution, severity; gold standard for large-fiber [AAN_2009]
- `interpret_labs` (CBC, CMP, fasting glucose + HbA1c, B12 + MMA, TSH, SPEP/IFE with immunofixation, urinalysis) — diabetes and B12 are leading reversible causes; SPEP/IFE for monoclonal gammopathy (MGUS-associated neuropathy, POEMS, AL amyloidosis) [AAN_2009]
- `search_medical_literature` — confirm AAN DSP guidelines, etiology-specific evaluations
- `check_drug_interactions` — toxic medications (chemotherapy especially platinum-based, taxanes, vincristine; nucleoside RT inhibitors; pyridoxine in megadose; metronidazole; nitrofurantoin; statins controversial)

**Required (small-fiber suspected):**
- `order_specialized_test` (`test_type: skin_biopsy_iencf`) — IENFD <97.5% lower limit for age supports small-fiber neuropathy [Lauria_2010]
- `order_specialized_test` (`test_type: autonomic_testing`) — QSART; supports small-fiber + dysautonomia

**Required (asymmetric / mononeuritis multiplex):**
- `interpret_labs` (ANA, ANCA, ESR/CRP, rheumatoid factor, anti-Hu/CV2/PNMA paraneoplastic) — vasculitic neuropathy workup [Said_2007]
- `order_specialized_test` (`test_type: nerve_biopsy`) — sural nerve biopsy when vasculitis suspected (necrotizing vasculitis on biopsy diagnostic)

**Recommended:**
- `analyze_brain_mri` — only if myelopathy/CNS involvement
- `order_specialized_test` (`test_type: genetic_panel:CMT`) — when family history positive or pes cavus / hammer toes / very young onset

**Optional:**
- `analyze_csf` — when CIDP suspected (albuminocytologic dissociation supports)
- `consult_medical_specialist` — neurology/rheumatology

## 3. Tools that are typically USELESS

- `analyze_eeg` — CNS test, irrelevant to peripheral disease
- `analyze_ecg` — only as baseline for autonomic involvement screen
- `order_echocardiogram` — only if amyloid cardiac involvement suspected
- `order_cardiac_monitoring` — only if dysautonomia with syncope/arrhythmia
- `order_ct_scan` — no role
- `order_advanced_imaging` (most) — none routinely indicated
- `analyze_brain_mri` (in typical distal symmetric polyneuropathy) — non-contributory

## 4. Tools that are HARMFUL / contraindicated

(none typically)

## 5. Sequence constraints

- `order_specialized_test` (`emg_ncs`) → `nerve_biopsy` (`soft`): EMG/NCS localizes and characterizes; if biopsy needed, NCS guides which nerve and helps interpretation
- `interpret_labs` (basic) → broader etiologic workup (`soft`): tier the workup — start broad, narrow based on initial results

## 6. Subtype variations

- **M (mild):** mild DSP with intact ADLs; standard workup minimum (labs + EMG)
- **S (standard):** typical DSP, identifiable common cause (diabetes, B12, alcohol); standard workup
- **P (progressive / disabling):** severe sensorimotor neuropathy, autonomic involvement, or rapid progression; expedited comprehensive workup including SPEP/IFE, vasculitis panel, paraneoplastic if appropriate; nerve biopsy if focal/asymmetric/atypical
- **R (reverse / mimic):** myelopathy mimicking peripheral disease, ALS (no sensory), CIDP (demyelinating, treatable), hereditary (CMT), small-fiber neuropathy (normal EMG/NCS — needs IENFD), pure motor neuropathy (MMN — anti-GM1, treatable!), tabes dorsalis (syphilis), B12 deficiency (sensory + posterior columns), heavy metal toxicity (arsenic, lead), porphyria; workup adds anti-GM1 (MMN!), heavy metals, treponemal serology, MRI cord, urine porphyrins

## 7. Common red-herring categories

- **Normal EMG/NCS** — does NOT exclude small-fiber neuropathy; need skin biopsy or autonomic testing
- **Pre-existing diabetes** — does not preclude another cause (especially with rapid progression, asymmetry, or atypical features — 30% of "diabetic" neuropathies have a second contributing cause)
- **Symptomatic improvement with gabapentin/duloxetine** — symptomatic only; doesn't address etiology
- **Negative SPEP** — does not exclude monoclonal protein; need IFE and serum free light chains for sensitivity
- **Sural-sparing pattern** — suggests proximal demyelinating cause (CIDP) — but sural may also be abnormal in CIDP

## 8. Allowed citations

- `[AAN_2009]` — England JD et al. Practice Parameter: evaluation of distal symmetric polyneuropathy. AAN, Neurology 2009;72:177-184
- `[Lauria_2010]` — Lauria G et al. European Federation of Neurological Societies / Peripheral Nerve Society Guideline on the use of skin biopsy in the diagnosis of small fiber neuropathy. J Peripher Nerv Syst 2010;15:79-92
- `[Said_2007]` — Said G. Vasculitic neuropathy. Curr Opin Neurol 2007;20:519-526
- `[Joint_Task_Force_2010_CIDP]` — Joint Task Force of the EFNS and PNS. European Federation of Neurological Societies/Peripheral Nerve Society guideline on management of chronic inflammatory demyelinating polyradiculoneuropathy. J Peripher Nerv Syst 2010;15:1-9
- `[Hanewinckel_2016]` — Hanewinckel R et al. The epidemiology and risk factors of chronic polyneuropathy. Eur J Epidemiol 2016;31:5-20
- `[Callaghan_2015]` — Callaghan BC et al. Diabetic neuropathy: clinical manifestations and current treatments. Lancet Neurol 2012;11:521-534
