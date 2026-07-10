# Criteria pack: High-grade glioma (glioblastoma, IDH-mutant astrocytoma grade 3)

**ICD-10:** C71.x
**Condition enum:** `NeurologicalCondition.BRAIN_TUMOR_GLIOMA`
**Case ID prefix:** `GLIO-HG`

---

## 1. Diagnostic criteria

WHO 2021 CNS tumor classification integrates histology and molecular markers
(IDH mutation status, 1p/19q codeletion, MGMT methylation, ATRX, H3K27M,
TERT promoter). Pre-operative imaging-based suspicion of high-grade glioma:
contrast-enhancing mass with central necrosis, surrounding T2/FLAIR
hyperintense edema, mass effect, restricted diffusion at edges, elevated
rCBV on perfusion, elevated Cho/NAA ratio on MRS, ring enhancement.
Definitive diagnosis = tissue (biopsy or resection). High-grade = WHO
grades 3-4 (IDH-mutant astrocytoma CNS WHO grade 3, glioblastoma; note "anaplastic astrocytoma" is the retired WHO-2016 synonym).

## 2. Standard workup hierarchy

**Required:**
- `analyze_brain_mri` (with and without gadolinium contrast; include diffusion, FLAIR) — characterize lesion, edema, mass effect, enhancement pattern [Stupp_2005]
- `interpret_labs` (CBC, CMP, coagulation; type & screen pre-op) — anticipated surgery, possibly steroids
- `search_medical_literature` — WHO classification, Stupp protocol, surgical referral criteria
- Specialist referral *(clinical action — `tool_name: null`, no tool call)* — neurosurgery + neuro-oncology REQUIRED for tissue diagnosis and treatment planning

**Recommended:**
- `order_advanced_imaging` (`modality: perfusion_MRI`) — high rCBV supports high-grade; useful when biopsy planning targeted to highest-grade region [Law_2003]
- `order_advanced_imaging` (`modality: MR_spectroscopy`) — elevated Cho/NAA + lipid-lactate peaks support malignancy; differentiates from radiation necrosis post-treatment [Bulik_2013]
- `analyze_brain_mri` (functional/DTI sequences for tractography) — if eloquent cortex involvement, surgical planning

**Optional:**
- `order_ct_scan` — only as emergency or pre-op planning (acute hemorrhage, intra-op navigation)
- `check_drug_interactions` — for anti-epileptics (levetiracetam often preferred), steroids, anti-emetics

## 3. Tools that are typically USELESS

- `analyze_eeg` — only if seizures (focal new-onset seizure in adult >40 should always prompt MRI to rule out tumor — but EEG itself is not diagnostic of tumor)
- `analyze_csf` — DANGEROUS in mass effect (see harmful); even when safe, low yield for primary brain tumor diagnosis
- `analyze_ecg` — unrelated to diagnosis
- `order_echocardiogram` — unrelated unless paraneoplastic suspected
- `order_cardiac_monitoring` — unrelated
- `order_advanced_imaging` (`modality: amyloid_PET / DaTscan / FDG_PET routine`) — not first-line; FDG-PET sometimes useful for grading but limited by physiologic cortical uptake
- `order_advanced_imaging` (`modality: carotid_duplex / transcranial_doppler`) — irrelevant

## 4. Tools that are HARMFUL / contraindicated

- `analyze_csf` — LP in suspected brain tumor with mass effect risks herniation. Contraindicated whenever imaging shows midline shift, basal cistern effacement, or significant mass effect [Hasbun_2001]

## 5. Sequence constraints

- `analyze_brain_mri` → `analyze_csf` (`hard`): MRI MUST precede LP in any suspected mass lesion; LP rarely indicated regardless [Hasbun_2001]
- `analyze_brain_mri` → surgical biopsy/resection (`hard`): adequate pre-operative imaging is standard of care [Stupp_2005]

## 6. Subtype variations

- **M (mild):** small, less aggressive features, possibly IDH-mutant astrocytoma CNS WHO grade 3; standard workup
- **S (standard):** typical glioblastoma with classic ring-enhancing necrotic mass; standard workup
- **P (progressive / aggressive):** large mass, multicentric, brainstem/eloquent location, rapid growth; same diagnostic workup + urgent surgical/radiation referral
- **R (reverse / mimic):** abscess (restricted diffusion centrally, surrounding edema — different DWI signature), demyelinating lesion (tumefactive MS), metastasis (usually multiple, gray-white junction), lymphoma (centrally restricted, less peripheral edema, HIV/immunocompromised), radiation necrosis (post-RT context); workup adds blood cultures (abscess), HIV (lymphoma), CT chest/abd/pelvis (metastatic), oligoclonal bands (tumefactive MS)

## 7. Common red-herring categories

- **Subacute headache** — many causes; new headache with focal signs or in adult >50 demands MRI
- **Seizure in adult** — broad differential, but tumor must be excluded with MRI
- **Steroid response** — improvement with steroids does NOT distinguish tumor from MS or lymphoma (all can respond)
- **Ring enhancement** — broad differential (tumor, abscess, MS, metastasis, radiation necrosis); needs additional features (perfusion, spectroscopy, DWI, clinical context)
- **Single MRI** — sometimes can't distinguish radiation necrosis from progression; serial MRI or PET helpful

## 8. Allowed citations

- `[WHO_2021]` — Louis DN et al. The 2021 WHO classification of tumors of the central nervous system. Neuro-Oncol 2021;23:1231-1251
- `[Stupp_2005]` — Stupp R et al. Radiotherapy plus concomitant and adjuvant temozolomide for glioblastoma. NEJM 2005;352:987-996
- `[Law_2003]` — Law M et al. Glioma grading: sensitivity, specificity, and predictive values of perfusion MR imaging and proton MR spectroscopy. AJNR 2003;24:1989-1998
- `[Bulik_2013]` — Bulik M et al. Potential of MR spectroscopy for assessment of glioma grading. Clin Neurol Neurosurg 2013;115:146-153
- `[Hasbun_2001]` — Hasbun R et al. Computed tomography of the head before lumbar puncture in adults with suspected meningitis. NEJM 2001;345:1727-1733
- `[NCCN_CNS]` — NCCN Clinical Practice Guidelines in Oncology: Central Nervous System Cancers (current version)
