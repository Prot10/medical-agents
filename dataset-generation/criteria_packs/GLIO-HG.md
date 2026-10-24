# Criteria pack: High-grade glioma (glioblastoma, IDH-mutant astrocytoma grade 3 and 4, diffuse midline glioma)

**ICD-10:** C71.x (C72.0 for the spinal cord). ICD-10 codes the site, not the entity: the integrated
WHO CNS5 diagnosis is carried by the label.
**Condition enum:** `NeurologicalCondition.BRAIN_TUMOR_GLIOMA`
**Case ID prefix:** `GLIO-HG`

Revised 24 October 2026 (close-out of the October 2026 review round; rulings in
`data/review/round-2026-10/plans/GLIO-HG.md` and `plans/GLIO-HG-decisions.md`). Where this pack and an
older case text disagree, this pack governs.

---

## 1. Diagnostic criteria (WHO CNS5 [WHO_2021])

Write "CNS WHO grade" with Arabic numerals. Retired names ("glioblastoma, IDH-mutant", "anaplastic
astrocytoma", "diffuse astrocytoma") are never current names.

- **Glioblastoma, IDH-wildtype, CNS WHO grade 4**: adult diffuse astrocytic glioma, IDH-wildtype and
  H3-wildtype, with microvascular proliferation, necrosis, TERT promoter mutation, EGFR amplification
  or +7/-10 (the molecular criteria alone give grade 4). Giant cell glioblastoma and gliosarcoma are
  histological subtypes of this entity, not separate integrated diagnoses.
- **Astrocytoma, IDH-mutant, CNS WHO grade 2, 3 or 4**: usually ATRX loss and 1p/19q intact.
  Homozygous CDKN2A/B deletion gives grade 4 whatever the histology; otherwise grade 4 needs
  microvascular proliferation or necrosis.
- **Diffuse midline glioma, H3 K27-altered, CNS WHO grade 4**: thalamus, brainstem, spinal cord or
  other midline structure, with H3 K27M or loss of H3K27me3. A midline tumour that is H3-wildtype and
  IDH-wildtype with glioblastoma features is glioblastoma, IDH-wildtype, and its report states that H3
  K27 was tested.
- **Oligodendroglioma** needs IDH mutation and 1p/19q codeletion; it is not this condition's answer.
- Imaging (contrast MRI, perfusion, spectroscopy) reaches a suspicion only; the integrated diagnosis
  comes from tissue. Management without tissue is reserved for prohibitive operative risk or a typical
  large lesion with rapid deterioration and very unfavourable prognosis [WHO_2021; EANO_2021].
- Mimic cases in this condition: abscess (P01, P03, P04), primary CNS lymphoma (P02, labelled with its
  own entity), tumefactive demyelination and tuberculoma (RP02), metastasis (RP01, RP04, RS01).

## 2. Standard workup hierarchy

Criterion order in every case is the clinical order below; follow-ups are listed in the same order,
tissue near the end and the drug check last.

**Required:**
- `analyze_brain_mri` (`contrast: true, protocol: tumor`): standardised brain tumour protocol, without
  and with gadolinium [EANO_2021]. Cord tumour (RM02): contrast `order_body_imaging` `spine_MRI`
  first, then brain MRI to exclude intracranial disease.
- `interpret_labs` (`CBC, BMP, coagulation, type_and_screen`; beta-hCG in women of child-bearing age):
  pre-operative safety [NCCN_CNS].
- `perform_clinical_assessment` (`assessment_type: performance_status`): current KPS and ECOG from the
  examination, never the pre-illness value. Required in all 30 cases (24 Oct 2026): every treatment
  branch after the integrated diagnosis is chosen on age and KPS, KPS below 70 being the unfavourable
  threshold [EANO_2021].
- `obtain_tissue_diagnosis`: one alternative per acceptable procedure, the same assay list in each.
  - Group A (resectable): `resection`, then `stereotactic_biopsy`. Maximal safe resection is the first
    option whenever site and clinical condition allow [AIOM_brain; EANO_2021]; the resection preference
    is carried by the surgery must, not by withholding credit for a biopsy (both obtain diagnostic
    tissue, and the choice is a management decision, ruling 4).
  - Group B (deep or eloquent, thalamus, brainstem): `stereotactic_biopsy` first.
  - Group C (multifocal, suspected lymphoma, unfit): biopsy, then cytoreduction where appropriate.
  - Group D (intramedullary cord): open biopsy, scored as `resection` until an `open_biopsy` term exists.
  - Assays [EANO_2021]: IDH1 R132H IHC in every diffuse glioma, with IDH1/IDH2 sequencing when the
    IHC is negative at 55 or under; ATRX in every diffuse glioma; MGMT promoter methylation in every
    glioblastoma (not required in diffuse midline glioma); H3 K27 in every midline tumour; CDKN2A/B in
    every IDH-mutant astrocytoma; 1p/19q only when the tumour is IDH-mutant; TERT, EGFR and +7/-10
    where the grade depends on them; BRAF V600E where epithelioid or giant cell histology raises it
    [vandenBent_2025]. Lymphoma: CD20 and EBER [EANO_PCNSL_2015]. Melanoma exclusion: SOX10 and
    Melan-A/HMB-45. Markers outside the vocabulary (chromogranin, synaptophysin, PAX8, TTF-1,
    thyroglobulin, H3 G34, methylation profiling) are stated in musts and findings rows, never in
    `molecular_assays`.
- Case-specific: HIV testing when lymphoma is suspected in an immunodeficient host (P02); systemic CT
  where a metastasis must be excluded before a primary brain tumour is diagnosed (RP04).

**Recommended:**
- `order_advanced_imaging` `perfusion_MRI` (rCBV; grading threshold 1.75 for glioma only, never for
  abscess) [Law_2003] and `MR_spectroscopy` [Bulik_2013]. Optional in the cord tumour (RM02): spinal
  perfusion and spectroscopy are not validated for grading.
- `order_advanced_imaging` `functional_MRI` and `DTI_tractography`: only where eloquent cortex or a
  major tract lies close to the lesion; soft constraint before tissue. Awake mapping needs a patient
  who can do the intraoperative language tasks.
- `analyze_eeg`: only to characterise uncertain spells or altered consciousness (M01, RP02, RM04, RP04,
  RS03). EEG has no role in tumour diagnosis; it is never required and never waste where indicated.
- `order_microbiology` `blood_culture`: when a brain abscess is on the differential (P01, P03, P04),
  drawn before antibiotics. Not required: the decisive microbiology is the aspirate culture taken with
  the stereotactic procedure [ESCMID_BA_2024].
- `order_body_imaging` `chest_abdomen_pelvis_CT`: recommended where metastasis is a live alternative
  (prior cancer, multifocal disease: RP01, RS01, P02 for systemic lymphoma), required in RP04, optional
  otherwise.
- `analyze_csf` with cytology: only where leptomeningeal spread is in question and imaging shows no
  herniation risk (RP03), after MRI (hard).

**Optional:**
- `check_drug_interactions`: the drugs the patient takes or starts now (dexamethasone, levetiracetam,
  home medicines) against the documented allergies; never temozolomide or other chemotherapy before
  tissue. Recommended only with a concrete interaction (RM04: dexamethasone with oral glucose-lowering
  drugs and aspirin before craniotomy; RS06: hydroxychloroquine and QT). Always last.
- `order_ct_scan`: emergency or navigation only.

**Not a clinical step (superseded):**
- `search_medical_literature` was listed as required in the August 2026 pack. Superseded by ruling 5 of
  the October 2026 round: no literature criterion, output or fallback in any GLIO-HG case.
- Specialist referral (neurosurgery, neuro-oncology, multidisciplinary tumour board) is a must, never a
  tool call.
- fMRI and DTI as MRI annotations (August 2026 note): superseded, they are `order_advanced_imaging`
  modalities `functional_MRI` and `DTI_tractography`.

## 3. Tools that are typically USELESS

- `analyze_csf`: waste in a parenchymal tumour without herniation signs (low yield); harm when any
  herniation sign is present (section 4).
- `order_echocardiogram`, `order_cardiac_monitoring`: waste, rationale "No cardiac question in this
  presentation".
- `analyze_ecg`: no diagnostic role, but a pre-operative 12-lead ECG is indicated in patients with
  cardiovascular risk factors before intermediate- or high-risk surgery [ESC_NCS_2022], so it is waste
  only in a young patient without risk factors (P05).
- `analyze_eeg` in a patient without seizures or altered consciousness: waste.
- `order_advanced_imaging` `amyloid_PET`, `DaTscan`, `carotid_duplex`, `transcranial_doppler`:
  irrelevant. `FDG_PET` is not an adequate tracer for a primary brain tumour; amino-acid PET
  (`amino_acid_PET`, FET or methionine) is the tracer with an established role, chiefly for
  pseudoprogression after chemoradiotherapy (RANO) [EANO_2021].

## 4. Tools that are HARMFUL / contraindicated

- `analyze_csf` (harm) when the MRI shows midline shift, cistern or fourth-ventricle effacement,
  hydrocephalus, papilloedema, or a spinal block. Canonical rationale: "Lumbar puncture is
  contraindicated with <finding>: the pressure gradient risks herniation [Hasbun_2001]". Below an
  expanded cord with near-complete effacement of the subarachnoid space: "risks neurological
  deterioration (spinal coning)" [Hollis_1986]. A case that forbids the LP never serves a CSF result.

## 5. Sequence constraints

- `analyze_brain_mri` -> tissue (`hard`): biopsy or resection cannot target the enhancing tumour or plan
  the approach without contrast MRI [EANO_2021].
- `interpret_labs` -> tissue (`hard`): coagulation, platelets and type and screen are known before a
  neurosurgical procedure [NCCN_CNS].
- `functional_MRI` / `DTI_tractography` -> tissue (`soft`), where present.
- Contrast spine MRI -> tissue (`hard`) in the cord tumour (RM02).
- `analyze_brain_mri` -> `analyze_csf` (`hard`) wherever a CSF criterion exists (RP03) [Hasbun_2001].
- Stop rule: the required criteria (MRI, labs, performance status, tissue, plus case-specific required
  criteria); `max_additional_actions` 0. Recommended and optional criteria are credited by the reward
  and never count as additional actions, so a larger allowance would only excuse unlisted orders.

## 6. Management musts (never tools)

- Seizures: a documented seizure is treated (levetiracetam preferred; avoid phenytoin, carbamazepine
  and phenobarbital, which interact with dexamethasone and temozolomide); this is treatment, never
  "prophylaxis". No seizure: no prophylactic antiseizure medication (strong recommendation against)
  [AIOM_brain]. Uncertain spell: EEG recommended, treatment only if the spell is epileptic.
- Steroids: dexamethasone for symptomatic vasogenic oedema at the lowest effective dose, tapered after
  surgery; held until biopsy when lymphoma is a live possibility unless herniation is impending
  [EANO_PCNSL_2015].
- Surgery: maximal safe resection when feasible; referral to neurosurgery and to the neuro-oncology
  multidisciplinary team after the integrated diagnosis.
- Treatment by entity [EANO_2021]: glioblastoma at 70 or under with KPS 70 or more, 60 Gy in 30
  fractions with concomitant and adjuvant temozolomide [Stupp_2005]; over 70 or KPS under 70,
  hypofractionated radiotherapy (40 Gy in 15 fractions) with temozolomide [Perry_2017], temozolomide
  alone when MGMT is methylated, or radiotherapy alone when unmethylated; very poor KPS, supportive
  care. IDH-mutant astrocytoma grade 3: radiotherapy then adjuvant temozolomide; grade 4: as
  glioblastoma. Diffuse midline glioma: focal radiotherapy and a clinical trial where available.
  Contraception and fertility counselling before temozolomide where relevant.
- Abscess on the differential: antimicrobials may be withheld until aspiration in a patient without
  severe disease when neurosurgery is possible within about 24 hours (conditional, low); otherwise
  start them at once [ESCMID_BA_2024].
- Contrast allergy (M03): premedication and monitoring per [ACR_contrast].

## 7. Subtype variations

- **M (mild):** smaller lesion, possibly IDH-mutant astrocytoma grade 3 or 4; standard workup.
- **S (standard):** typical glioblastoma with a necrotic ring-enhancing mass; standard workup.
- **P (progressive or puzzle):** large, multicentric, deep or abscess-like; same workup with the
  case-specific additions above.
- **R (reverse or mimic):** abscess (central restricted diffusion), tumefactive demyelination
  (open ring; AQP4 and MOG serology where the cord or optic nerve is involved [Wingerchuk_2015]),
  metastasis (gray-white junction, prior cancer), lymphoma (homogeneous enhancement, immunodeficiency),
  radiation necrosis (post-treatment).

## 8. Pitfalls and red herrings

- The HPI never contains the contrast MRI, perfusion, spectroscopy or tissue result; at most an
  outpatient non-contrast CT with a mass and oedema, or the referral reason.
- A tool report states what its modality shows: no integrated diagnosis from imaging, no management
  advice, no "suggesting" clauses; MRS reports values, not "normal below 1.5".
- Steroid response does not distinguish tumour from demyelination or lymphoma.
- Ring enhancement has a broad differential; perfusion, spectroscopy, DWI and context narrow it.
- A pre-illness KPS in the social history is not the current KPS.
- No fallback EEG is normal in a hemispheric mass with oedema (focal slowing over the lesion).
- A case-level fallback is served for any order of its tool, so a generic report of one test type
  (a normal neuropsychological screen, a DaTscan) is left null and the benchmark library answers by
  parameter.

## 9. Allowed citations

Every key cited in a GLIO-HG case is listed here. Checked on 24 October 2026.

- `[WHO_2021]`: Louis DN, Perry A, Wesseling P, et al. The 2021 WHO classification of tumors of the
  central nervous system: a summary. Neuro Oncol 2021;23:1231-1251.
- `[EANO_2021]`: Weller M, van den Bent M, Preusser M, et al. EANO guidelines on the diagnosis and
  treatment of diffuse gliomas of adulthood. Nat Rev Clin Oncol 2021;18:170-186.
- `[vandenBent_2025]`: van den Bent MJ, et al. Updated EANO guideline on rational molecular testing of
  gliomas, glioneuronal, and neuronal tumors in adults for targeted therapy selection, Update 1. Neuro
  Oncol 2025;27(2):331-337. doi:10.1093/neuonc/noae213. Only BRAF V600E testing has proven clinical
  benefit among the targets reviewed.
- `[AIOM_brain]`: AIOM (with AINR, AIRO, SIAPEC-IAP, SIN, SINch, SIRM). Linee guida Neoplasie
  cerebrali, aggiornamento 2026. Sistema Nazionale Linee Guida, Istituto Superiore di Sanita, LG 266;
  first published 22 July 2020, last updated 27 August 2026. Cited for surgery as the first option, as
  extensive as safely possible, and for the strong recommendation against antiseizure prophylaxis in
  patients without seizures. Reviewer 2 cited these as Quesito 1 and Quesito 23 of the edition then
  current; the 2026 numbering could not be checked (the ISS PDF was not retrievable), so case text
  cites AIOM by topic, without question numbers.
- `[Stupp_2005]`: Stupp R, Mason WP, van den Bent MJ, et al. Radiotherapy plus concomitant and adjuvant
  temozolomide for glioblastoma. N Engl J Med 2005;352:987-996. Treatment musts only; superseded as a
  citation for the MRI criterion (use [EANO_2021]).
- `[Perry_2017]`: Perry JR, Laperriere N, O'Callaghan CJ, et al. Short-course radiation plus
  temozolomide in elderly patients with glioblastoma. N Engl J Med 2017;376:1027-1037.
- `[Law_2003]`: Law M, Yang S, Wang H, et al. Glioma grading: sensitivity, specificity, and predictive
  values of perfusion MR imaging and proton MR spectroscopic imaging compared with conventional MR
  imaging. AJNR Am J Neuroradiol 2003;24:1989-1998. Glioma grading only.
- `[Bulik_2013]`: Bulik M, Jancalek R, Vanicek J, et al. Potential of MR spectroscopy for assessment of
  glioma grading. Clin Neurol Neurosurg 2013;115:146-153.
- `[Hasbun_2001]`: Hasbun R, Abrahams J, Jekel J, Quagliarello VJ. Computed tomography of the head
  before lumbar puncture in adults with suspected meningitis. N Engl J Med 2001;345:1727-1733. LP safety
  with intracranial mass effect only.
- `[Hollis_1986]`: Hollis PH, Malis LI, Zappulla RA. Neurological deterioration after lumbar puncture
  below complete spinal subarachnoid block. J Neurosurg 1986;64:253-256 (compressive deterioration in
  7 of 50 patients). LP below a spinal block (RM02).
- `[EANO_PCNSL_2015]`: Hoang-Xuan K, Bessell E, Bromberg J, et al. Diagnosis and treatment of primary
  CNS lymphoma in immunocompetent patients: guidelines from the European Association for
  Neuro-Oncology. Lancet Oncol 2015;16:e322-e332.
- `[ESCMID_BA_2024]`: Bodilsen J, D'Alessandris QG, Humphreys H, et al. European Society of Clinical
  Microbiology and Infectious Diseases guidelines on diagnosis and treatment of brain abscess in
  children and adults. Clin Microbiol Infect 2024;30:66-89. doi:10.1016/j.cmi.2023.08.016.
- `[ESC_NCS_2022]`: Halvorsen S, Mehilli J, Cassese S, et al. 2022 ESC Guidelines on cardiovascular
  assessment and management of patients undergoing non-cardiac surgery. Eur Heart J
  2022;43:3826-3924. Pre-operative ECG with risk factors.
- `[ACR_contrast]`: ACR Committee on Drugs and Contrast Media. ACR Manual on Contrast Media. American
  College of Radiology, current edition (2024). Premedication after a prior contrast reaction (M03).
- `[Wingerchuk_2015]`: Wingerchuk DM, Banwell B, Bennett JL, et al. International consensus diagnostic
  criteria for neuromyelitis optica spectrum disorders. Neurology 2015;85:177-189 (RM02 serology).
- `[NCCN_CNS]`: NCCN Clinical Practice Guidelines in Oncology: Central Nervous System Cancers (current
  version). Pre-operative laboratory and staging claims only; waste rationales cite [EANO_2021].
