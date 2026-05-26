# Criteria pack: Multiple Sclerosis, relapsing-remitting

**ICD-10:** G35
**Condition enum:** `NeurologicalCondition.MULTIPLE_SCLEROSIS`
**Case ID prefix:** `MS-RR`

---

## 1. Diagnostic criteria

McDonald 2017 criteria (Thompson 2018 publication): diagnosis requires
**dissemination in space (DIS)** and **dissemination in time (DIT)**, plus
exclusion of better explanation. For RRMS with typical clinical attack:
- 2 attacks + objective evidence of ≥2 lesions: clinical alone suffices
- 2 attacks + ≥1 lesion + reasonable historical attack: clinical alone
- 2 attacks + 1 lesion: DIS needed (additional MRI lesion in different MS region)
- 1 attack + ≥2 lesions: DIT needed (new T2 lesion on follow-up MRI OR
  simultaneous enhancing + non-enhancing lesions on same MRI OR CSF
  oligoclonal bands positive [new addition in 2017])
- 1 attack + 1 lesion: both DIS and DIT needed

MRI lesions count if in typical MS locations: periventricular, juxtacortical
or cortical, infratentorial, spinal cord. CSF oligoclonal bands +/-
IgG index elevated supports diagnosis (now substitutes for DIT in select
scenarios per McDonald 2017).

## 2. Standard workup hierarchy

**Required:**
- `analyze_brain_mri` (with gadolinium contrast, MS protocol including FLAIR, T2, DWI, post-contrast T1) — DIS, DIT (if enhancing + non-enhancing simultaneously), lesion characterization [McDonald_2017]
- `analyze_brain_mri` extending to cervical/thoracic spine — typical MS regions include cord; ~80% of MS patients have cord lesions [McDonald_2017]
- `analyze_csf` (`oligoclonal_bands, IgG_index, total protein, glucose, cells`) — OCBs supportive (sensitivity ~95% MS); can substitute for DIT per McDonald 2017 [McDonald_2017]
- `interpret_labs` (CBC, CMP, TSH, B12, ANA, NMO-IgG/aquaporin-4, MOG-IgG, HIV, RPR, vitamin D) — exclude mimics (NMOSD, neurosarcoidosis, B12 deficiency, syphilis); MOG/AQP4 critical to distinguish [Wingerchuk_2015]
- `search_medical_literature` — McDonald 2017, DMT options, NEDA-3 outcome
- `check_drug_interactions` — DMT initiation (interferon-β, glatiramer, dimethyl fumarate, fingolimod, natalizumab, ocrelizumab, ofatumumab, cladribine), live vaccines, JC virus risk

**Recommended:**
- `order_specialized_test` (`test_type: optical_coherence_tomography`) — RNFL thinning supports optic pathway involvement; useful even without overt optic neuritis [Petzold_2017]
- `order_specialized_test` (`test_type: vep`) — subclinical optic pathway involvement supports DIS

**Optional:**
- `consult_medical_specialist` — MS subspecialist for DMT decisions

## 3. Tools that are typically USELESS

- `analyze_eeg` — non-specific, no role in MS diagnosis
- `analyze_ecg` — only for baseline pre-DMT (fingolimod has bradyarrhythmia risk)
- `order_echocardiogram` — only if specific cardiac indication
- `order_cardiac_monitoring` — only for first-dose fingolimod monitoring
- `order_ct_scan` — MRI is superior; CT useless for MS plaques
- `order_advanced_imaging` (any modality except possibly perfusion) — none routinely indicated
- `order_specialized_test` (`emg_ncs / muscle_biopsy / nerve_biopsy / genetic_panel / etc.`) — peripheral testing not relevant to MS

## 4. Tools that are HARMFUL / contraindicated

- `analyze_csf` — exclude mass effect on MRI before LP (standard); generally safe in MS
- Specific DMTs contraindicated in JC virus + (natalizumab PML risk) — drug interactions tool should flag

## 5. Sequence constraints

- `analyze_brain_mri` → `analyze_csf` (`soft`): standard pre-LP imaging; particularly important in atypical features

## 6. Subtype variations

- **M (mild / CIS):** clinically isolated syndrome with first event; needs DIS+DIT (MRI+OCB) before MS diagnosis
- **S (standard / RRMS):** typical attacks with full or partial recovery, MRI evidence of DIS and DIT
- **P (progressive — but R is for relapses not progression here. P could be aggressive RRMS or transition to SPMS):** active inflammatory MS with multiple gadolinium-enhancing lesions; same workup + JC virus serology + earlier consideration of high-efficacy DMT
- **R (reverse / mimic):** NMOSD (AQP4+, longitudinally extensive transverse myelitis, area postrema syndrome, optic neuritis), MOGAD (MOG-IgG+, often bilateral optic neuritis, ADEM-like), neurosarcoidosis (basilar meningeal enhancement, elevated ACE, lymphopenia, mediastinal LN), CNS vasculitis, susac syndrome (triad: encephalopathy + branch retinal artery occlusion + sensorineural hearing loss), Behçet, ADEM (monophasic, often post-infectious); workup adds AQP4-IgG, MOG-IgG, ANA, ANCA, ACE, CT chest, audiometry, ophthalmology

## 7. Common red-herring categories

- **Single MRI lesion** — does not meet DIS; needs follow-up MRI or other evidence
- **OCB-negative MS** — possible (~5-10%); does not exclude MS
- **Older patient with first MS-like attack** — broaden differential (vascular, B12, neoplasm) significantly
- **"Multiple sclerosis" on prior MRI report** — radiology often suggests MS for non-specific WMH; clinical correlation required
- **Symmetric / large confluent lesions** — atypical; consider NMOSD, MOGAD, leukodystrophy
- **Cortical lesions seen** — McDonald 2017 includes them; previously underrecognized

## 8. Allowed citations

- `[McDonald_2017]` — Thompson AJ et al. Diagnosis of multiple sclerosis: 2017 revisions of the McDonald criteria. Lancet Neurol 2018;17:162-173
- `[Wingerchuk_2015]` — Wingerchuk DM et al. International consensus diagnostic criteria for neuromyelitis optica spectrum disorders. Neurology 2015;85:177-189
- `[MAGNIMS_2016]` — Filippi M et al. MRI criteria for the diagnosis of multiple sclerosis: MAGNIMS consensus guidelines. Lancet Neurol 2016;15:292-303
- `[Petzold_2017]` — Petzold A et al. Retinal layer segmentation in multiple sclerosis: a systematic review and meta-analysis. Lancet Neurol 2017;16:797-812
- `[Reich_2018]` — Reich DS, Lucchinetti CF, Calabresi PA. Multiple sclerosis. NEJM 2018;378:169-180
- `[Banwell_2023_MOGAD]` — Banwell B et al. Diagnosis of MOG antibody-associated disease: International MOGAD Panel proposed criteria. Lancet Neurol 2023;22:268-282
