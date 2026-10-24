# Criteria pack: Multiple Sclerosis, relapsing-remitting

**ICD-10-CM:** G35.A (relapsing-remitting multiple sclerosis). The flat G35 code was retired on
1 Oct 2025; FY2026 splits it into G35.A relapsing-remitting, G35.B0-G35.B2 primary progressive,
G35.C0-G35.C2 secondary progressive and G35.D MS, unspecified. Every MS-RR case has `icd_codes[0]`
G35.A. Accepted synonyms (`diagnosis_synonyms.yaml`, G35 entry, 24 Oct 2026): multiple sclerosis,
MS, relapsing(-)remitting multiple sclerosis, RRMS; codes G35, G35.A, G35.D. The progressive codes
and the label "demyelinating disease" (G37.9, an Excludes1 of G35.A, whose tokens occur in an
NMOSD, MOGAD or ADEM answer) are not accepted.
**Condition enum:** `NeurologicalCondition.MULTIPLE_SCLEROSIS` (`multiple_sclerosis`)
**Case ID prefix:** `MS-RR`

Updated 24 Oct 2026 to the October 2026 review round (`data/review/round-2026-10/plans/MS-RR.md`,
`MS-RR-summary.md`) and its close-out (`plans/MS-RR-decisions.md`). The diagnostic text now follows
the 2024 revision of the McDonald criteria; the 2017 criteria are cited only where a text explains
what changed.

---

## 1. Diagnostic criteria (2024 McDonald revision, [McDonald_2024])

Diagnosis needs a typical clinical or MRI picture, dissemination in space (DIS), dissemination in
time (DIT) where section 1.3 requires it, and no better explanation.

1.1 **Regions.** Five DIS regions: periventricular, cortical/juxtacortical, infratentorial, spinal
cord, optic nerve. The optic nerve counts when shown by MRI (T2 signal or enhancement), OCT
(inter-eye difference of at least 6 um in pRNFL or at least 4 um in GCIPL) or VEP (prolonged P100).
Symptomatic and asymptomatic lesions both count. "Subcortical" or "deep white matter" is not a
region; the callososeptal interface belongs to the periventricular region.

1.2 **DIS** needs at least 2 of the 5 regions (never "three regions establish DIS").

1.3 **When DIT is needed.** With lesions in 4 or 5 regions, DIS with no better explanation
establishes MS: no DIT and no CSF are needed. With 2 or 3 regions, DIS is completed by any one of:
DIT (simultaneous gadolinium-enhancing and non-enhancing lesions on one scan, or a new T2 or
enhancing lesion on a later scan), positive CSF (CSF-restricted oligoclonal bands or an elevated
kappa free-light-chain index), or a central vein sign in at least six lesions.

1.4 **Age 50 or over, or vascular risk factors.** The criteria recommend (do not mandate)
additional supporting evidence (a spinal cord lesion, positive CSF or the central vein sign),
because non-specific white matter lesions are common (RS01, RP05). In migraine (P01, P02, P03) the
cases use the cord lesion or CSF as supporting evidence by clinical prudence, not as a criteria
requirement.

1.5 **T1 hypointense lesions ("black holes")** indicate chronic tissue damage and do not count for
DIT.

1.6 **CSF.** Positive CSF = at least two CSF-restricted oligoclonal bands (isoelectric focusing with
paired serum) or a kFLC index above the laboratory's validated cutoff (the report states its own,
e.g. "reference < 6.1"). The IgG index is supportive only. Myelin basic protein has no diagnostic
role. Typical MS CSF: WBC 0-15/uL lymphocytic (over 50/uL argues against MS), protein normal or
mildly raised (< 70 mg/dL). OCB are absent in about 5-10% of people with MS: a negative result never
excludes MS.

1.7 **Acute optic neuritis timeline.** In the first weeks the disc is normal (retrobulbar) or
mildly swollen; pallor appears after about 4-6 weeks. Acute OCT: pRNFL normal or increased
(swelling), GCIPL normal or minimally reduced; thinning develops over 1-3 months [Petzold_2017].
Thinning or pallor in the first 3 weeks belongs only to an eye with a documented earlier episode,
and the report attributes it to that episode. VEP: prolonged P100 in the affected eye.

1.8 **NMOSD and MOGAD discriminators** [Wingerchuk_2015], [Banwell_2023_MOGAD]. NMOSD:
longitudinally extensive myelitis (3 or more contiguous segments, central), area postrema syndrome,
severe or bilateral optic neuritis, OCB usually absent, AQP4-IgG by cell-based assay. MOGAD: optic
neuritis with perineural enhancement and long optic-nerve lesions, conus involvement, ADEM-like
lesions, MOG-IgG by (live) cell-based assay. MS cord lesions: short (under 2 segments),
peripheral or dorsolateral, less than half the cross-section.

1.9 **Tumefactive lesions** [Hardy_2013]. Open-ring enhancement with the open side toward the
cortex, less mass effect than size predicts, peripheral restricted diffusion, other typical MS
lesions and CSF-restricted OCB favour demyelination. While primary CNS lymphoma or glioma is not
excluded, corticosteroids are withheld until CSF cytology and flow cytometry, or tissue, are
obtained (steroids can make lymphoma non-diagnostic); dexamethasone only for impending herniation,
after neurosurgical discussion. Disease-modifying therapy waits until MS is confirmed (DIS and DIT
met). LP is contraindicated with midline shift, effaced basal cisterns, a posterior fossa mass
compressing the fourth ventricle, or papilloedema with a mass lesion.

## 2. Work-up hierarchy (as applied in the 30 cases, 24 Oct 2026)

Pathway order (`followup_outputs` and `action_criteria`): brain MRI, spine MRI, mimic labs,
AQP4/MOG, CSF, VEP, OCT, advanced imaging, body CT, biopsy, drug check, literature last.

**Required (all 30):**
- `analyze_brain_mri` `{contrast: true, protocol: ms}`: MS protocol (3D FLAIR, T2, DWI, pre- and
  post-gadolinium T1; SWI optional for the central vein sign) [McDonald_2024], [Wattjes_2021]. A
  brain MRI report describes the brain and at most the upper cervical cord in its field of view;
  it never reports thoracic cord.
- `order_body_imaging` `{contrast: true, study: spine_MRI}`: cervical and thoracic cord with
  gadolinium, ideally in the same session [McDonald_2024], [Wattjes_2021]. Not a second
  `analyze_brain_mri`.
- `interpret_labs` `{panels: [CBC, vitamin_B12, TSH, HIV]}`: the mimic-exclusion panel. The stored
  initial labs carry the full first-line panel (CBC, ESR, CRP, CMP, calcium, glucose, TSH, B12, HIV
  and what the case adds), never the AQP4/MOG results.

**AQP4-IgG and MOG-IgG by cell-based assay** (`action-aqp4-mog-cba`, `interpret_labs`, alternatives
`{panels: [AQP4_IgG_cell_based, MOG_IgG_cell_based]}`, `{panels: [AQP4_IgG, MOG_IgG]}`,
`{panels: [NMO_MOG]}`) [Wingerchuk_2015], [Banwell_2023_MOGAD]:
- `required` with a red flag: severe optic neuritis (20/200 or worse, or hand motions), bilateral
  optic neuritis, LETM, area postrema or brainstem-encephalitic syndrome, tumefactive lesion,
  encephalopathy, onset at 50 or later: M04, RM01, RM02, RP01, RP02, RP03, RP05, RS01 (8);
- `recommended` when optic neuritis or myelitis is part of the current attack or the history,
  without a red flag: M01, M02, M03, P04, P05, RM04, RP04, RS02, RS03, RS05, RS06, S01-S06 (17);
- none otherwise: P01, P02, P03, RM03, RS04 (5).
The results are a `followup_outputs` entry (`interpret_labs`, trigger
`request_aqp4_mog_cell_based_assay`, panel `Neuroimmunology`), never rows of the initial labs: the
first `interpret_labs` order receives the whole initial payload, so rows stored there would answer
the assay without its being ordered. The five cases without a criterion store the same negative
follow-up, so an agent that orders the assay receives its result rather than the first-line panel
again.

**CSF** (`action-5-analyze-csf`, alternatives `{special_tests: [oligoclonal_bands]}` or
`{special_tests: [kappa_free_light_chain_index]}`, with paired serum) [McDonald_2024]:
- `recommended` (8) where CSF changes the decision or excludes a mimic: P01, P02, P03 (migraine
  lesion puzzle), RM01, RM02, RP01 (tumefactive: cytology, flow cytometry and OCB), RS01, RP05
  (over 50 with vascular risk);
- `optional` in the other 20 (4-5 regions, or DIS with DIT already on MRI);
- never required; contraindicated in RP02 and RP03 (section 4).
Every stored CSF report carries a kFLC index.

**Optional:**
- `order_specialized_test` `{test_type: vep}` (18: M01-M04, P01-P04, RM04, RP04, RP05, RS03,
  S01-S06) [McDonald_2024] and `{test_type: optical_coherence_tomography}` (14: M01, M02, M04, P04,
  RM04, RP04, RP05, RS03, S01-S06) [Petzold_2017], [McDonald_2024], where the case relies on the
  optic nerve as a region or the library normal would contradict a documented optic neuropathy.
- Tumefactive cases: `order_advanced_imaging` `{modality: MR_spectroscopy}` (RM01, RM02, RP01, RP02,
  RP03) and `{modality: perfusion_MRI}` (RP02) [Wattjes_2021], [Hardy_2013];
  `order_body_imaging` `{study: chest_abdomen_pelvis_CT}` (RP01, metastasis in the differential)
  [Hardy_2013]; `obtain_tissue_diagnosis` `{procedure: stereotactic_biopsy}` optional in RM01,
  recommended in RP02 and RP03 (LP contraindicated, imaging indeterminate) [McDonald_2024],
  [Hardy_2013]. The biopsy report states the histology only (active demyelination with relative
  axonal preservation, CD68 macrophages with myelin debris, perivascular T cells, Creutzfeldt
  astrocytes; CD20 and IDH1 immunohistochemistry), never the integrated diagnosis.
- `check_drug_interactions` `{}`: optional; recommended in RP03 and RP05 (high-dose steroids with
  oral hypoglycaemics). A management act, after the diagnostic core, never in the stop rule.
- `search_medical_literature` `{}`: optional in all 30, last, with empty expected evidence; its
  stored outputs give general, correctly cited evidence (2024 criteria), never the case's findings.

**Stop rule:** `required_before_assessment` = the required criteria only (brain MRI, spine MRI,
labs, plus AQP4/MOG where required); `max_additional_actions` 2 in the S, RS, M, RM03 and RM04
cases, 3 in the P and RP cases and in RM01 and RM02.

No case has a future-data follow-up (no 3-month repeat MRI, no post-steroid MRI, no steroid trial):
the agent assesses at the index encounter.

## 3. Tools that are typically USELESS (waste avoided actions)

- `analyze_eeg` (28 cases): no diagnostic role. Not avoided in RM01 (first generalised seizure) or
  RP03 (post-operative coma), whose EEG fallbacks fit the case (RM01 right hemispheric slowing
  without epileptiform discharges; RP03 diffuse slowing, no status).
- `order_ct_scan` (27): MRI is the study; CT is not avoided in RM01, RP02 and RP03, where an
  emergency head CT is appropriate, and their CT fallbacks show the lesion [Wattjes_2021].
- `order_echocardiogram`, `order_cardiac_monitoring` (30): no cardiac question.
- `order_advanced_imaging` `{modality: FDG_PET}` (26): no role in MS diagnosis [Wattjes_2021].
- `analyze_ecg` (P04 only, a waste avoided action); no case has an ECG or EEG criterion.
- Peripheral tests (EMG/NCS, nerve or muscle biopsy) and SSEP: not stored and not scored.

## 4. Harmful or contraindicated (avoided actions and prohibitions)

- `analyze_csf` `{}` is a `contraindicated` avoided action in RP02 (4.1 cm mass, 6 mm midline
  shift, papilloedema) and RP03 (3.8 cm posterior fossa lesion compressing the fourth ventricle);
  their CSF content lives in `fallback_tool_outputs.csf` so an agent that does the LP still gets a
  coherent report. RM01, RM02 and RP01 have mild mass effect without shift or papilloedema: LP is
  allowed after the MRI.
- Prohibitions (canonical, every case): "Do not diagnose MS based on non-specific white-matter
  lesions alone without meeting the 2024 revised McDonald criteria and excluding mimics" (28) and
  "Do not use chronic oral corticosteroids as maintenance treatment for MS: they do not prevent
  relapses or disability and cause cumulative harm" (30). Live vaccines after B-cell depletion or
  S1P modulators (27); spinal-cord MRI not to be omitted with myelopathic signs (17); teriflunomide
  without contraception only in women of child-bearing potential (15); case-specific ones (cephalosporin
  allergy, gadolinium with an iodinated-contrast allergy, natalizumab with anti-JCV index above 1.5,
  ELISA AQP4/MOG assays, steroids before tissue in tumefactive cases).
- Drug facts the cases must respect: amlodipine does not cause bradycardia; corticosteroids do not
  reduce combined oral contraceptive efficacy; topiramate does not cause lymphopenia; high-dose
  steroids raise glucose (insulin cover with oral hypoglycaemics) and add GI-bleeding risk with
  NSAIDs (PPI); teriflunomide is teratogenic and raises ethinylestradiol and levonorgestrel
  exposure; natalizumab PML risk rises with anti-JCV index above 1.5, treatment over 2 years and
  prior immunosuppression.

## 5. Sequence constraints (all soft)

- `action-1-analyze-brain-mri` before `action-5-analyze-csf` wherever CSF is a criterion: brain
  imaging before lumbar puncture to exclude a mass lesion with herniation risk.
- `action-1-analyze-brain-mri` before `action-biopsy` (RM01, RP02, RP03): target and trajectory
  come from the MRI.
No hard constraint remains (the LP in RP02 and RP03 is an avoided action instead).

## 6. Subtype variations

- **S (straightforward):** typical attack (often optic neuritis or partial myelitis) after an
  earlier attack, lesions in 4-5 regions.
- **M (moderate):** first recognised attack with earlier subclinical lesions or an earlier
  unrecognised attack; M04 severe optic neuritis (AQP4/MOG required).
- **P (diagnostic puzzle):** migraine or a vestibular label with "non-specific" outside lesions
  (P01-P03: OCB negative, CSF recommended, the initial MRI carries typical lesions and DIT); P04,
  P05 atypical or highly active disease (P05 anti-JCV index 2.84: anti-CD20 over natalizumab).
- **Tumefactive** (RM01, RM02, RP01, RP02, RP03; label "... (tumefactive variant)"): section 1.9,
  AQP4/MOG required, MRS optional, biopsy by case.
- **Late onset** (RS01 61, RP05 54): section 1.4.
- **R series** (RM, RP, RS): seeded from published case reports (`generation_method:
  real_case_seed`). Every R case is labelled relapsing-remitting MS; the "R" marks the source, not
  a mimic. There is no NMOSD, MOGAD, ADEM or CIS case in MS-RR: those entities are differential
  entries only, and their labels are not accepted.

## 7. Common red-herring categories

- **"Non-specific" outside MRI or a migraine label** (P01-P03): the MS-protocol study shows typical
  lesions.
- **OCB-negative MS** (P01-P03, RP04): does not exclude MS.
- **Age over 50 with vascular risk** (RS01, RP05): small-vessel disease and lacunar stroke are
  argued against by lesion shape and site, absent diffusion restriction, cord lesions and CSF.
- **Low-normal B12** (RS06 228 pg/mL): does not explain enhancing brain lesions and OCB.
- **Low vitamin D, ANA at low titre, hypercalcaemia with neurosarcoidosis in the differential
  (RM04)**: only where the labs carry that row.
- **Family history of Behcet disease** (RM01): no oral or genital ulcers, no uveitis.
- **Tumefactive lesion read as a tumour**: section 1.9.

## 8. Musts (canonical)

- Formulation: "State relapsing-remitting MS by the 2024 McDonald criteria, naming the regions that
  give DIS and, where needed, what gives DIT or positive CSF (here ...)", completed per case with
  its regions.
- Relapse treatment for a relapse that affects function [NICE_NG220]: methylprednisolone oral
  500 mg daily for 5 days, or IV 1 g daily for 3-5 days (IV when oral is unsuitable, has failed or
  the relapse is severe); exclude infection first (urinalysis with bladder symptoms); plasma
  exchange for a severe relapse that does not respond. Tumefactive cases with lymphoma not yet
  excluded: withhold corticosteroids until CSF cytology and flow cytometry or tissue.
- DMT: "Offer disease-modifying therapy after diagnosis, choosing efficacy by disease activity
  (<the case's markers>)", with pregnancy plans and contraception only in women of child-bearing
  potential.
- Pre-DMT screening matched to the drug class: HBsAg, anti-HBc, HCV, VZV IgG (HIV is already in the
  mimic panel), live vaccines at least 4-6 weeks before starting.
- One or two case-specific musts (post-void residual and antimuscarinic or intermittent
  catheterisation for bladder symptoms, carbamazepine for painful tonic spasms, vitamin D only
  with a low value, driving advice with a hemianopia, smoking cessation in a smoker).
No must orders a diagnostic test (AQP4/MOG, MRI, OCT live in action criteria).

## 9. Allowed citations

- `[McDonald_2024]`: Montalban X, Lebrun-Frenay C, Oh J, et al. Diagnosis of multiple sclerosis:
  2024 revisions of the McDonald criteria. Lancet Neurol 2025;24(10):850-865, doi
  10.1016/S1474-4422(25)00270-4. Governs diagnosis.
- `[Wattjes_2021]`: Wattjes MP, Ciccarelli O, Reich DS, et al. 2021 MAGNIMS-CMSC-NAIMS consensus
  recommendations on the use of MRI in patients with multiple sclerosis. Lancet Neurol
  2021;20(8):653-670, doi 10.1016/S1474-4422(21)00095-8. Governs the MRI protocol and the role of
  other imaging.
- `[NICE_NG220]`: National Institute for Health and Care Excellence. Multiple sclerosis in adults:
  management. NICE guideline NG220, June 2022; diagnosis recommendations amended June 2026 to refer
  to the 2024 McDonald criteria. Governs relapse treatment, DMT and monitoring.
- `[Wingerchuk_2015]`: Wingerchuk DM, Banwell B, Bennett JL, et al. International consensus
  diagnostic criteria for neuromyelitis optica spectrum disorders. Neurology 2015;85(2):177-189.
- `[Banwell_2023_MOGAD]`: Banwell B, Bennett JL, Marignier R, et al. Diagnosis of myelin
  oligodendrocyte glycoprotein antibody-associated disease: International MOGAD Panel proposed
  criteria. Lancet Neurol 2023;22(3):268-282.
- `[Petzold_2017]`: Petzold A, Balcer LJ, Calabresi PA, et al. Retinal layer segmentation in
  multiple sclerosis: a systematic review and meta-analysis. Lancet Neurol 2017;16(10):797-812.
- `[Hardy_2013]`: Hardy TA, Chataway J. Tumefactive demyelination: an approach to diagnosis and
  management. J Neurol Neurosurg Psychiatry 2013;84(9):1047-1053, doi 10.1136/jnnp-2012-304498
  (PMID 23334629). Cited for the diagnostic approach to a tumefactive lesion (imaging, the
  malignancy differential), the decision to biopsy, and deferring DMT until MS is confirmed.
- `[Reich_2018]`: Reich DS, Lucchinetti CF, Calabresi PA. Multiple sclerosis. N Engl J Med
  2018;378(2):169-180. General statements only.

Literature outputs may also name by author and year the papers above and Thompson 2018 (below)
when explaining what the 2024 revision changed.

**Superseded keys (do not cite on a criterion):**
- `[McDonald_2017]`: Thompson AJ, Banwell BL, Barkhof F, et al. Diagnosis of multiple sclerosis:
  2017 revisions of the McDonald criteria. Lancet Neurol 2018;17(2):162-173. Superseded by
  `[McDonald_2024]` (four DIS regions, OCB as a substitute for DIT); only a text that explains what
  changed may refer to it.
- `[MAGNIMS_2016]`: Filippi M, Rocca MA, Ciccarelli O, et al. MRI criteria for the diagnosis of
  multiple sclerosis: MAGNIMS consensus guidelines. Lancet Neurol 2016;15(3):292-303. Superseded by
  `[McDonald_2024]` for the regions and `[Wattjes_2021]` for the protocol.
- "MAGNIMS-CMSC-NAIMS 2024/2025": no such document exists; use `[Wattjes_2021]`.
