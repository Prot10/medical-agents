# Criteria pack: Frontotemporal dementia (bvFTD, FTD-MND, semantic and non-fluent PPA)

**ICD-10-CM, per case:** G31.09 (other frontotemporal neurocognitive disorder) for behavioural
variant FTD, including FTD with motor neuron disease; G31.01 for the primary progressive aphasias
(svPPA, nfvPPA), because ICD-10-CM lists "primary progressive aphasia" as an inclusion term of
G31.01 (Pick's disease). G31.0 (category) is an accepted synonym of the bvFTD cases only.
**Condition enum:** `NeurologicalCondition.FTD`
**Case ID prefix:** `FTD`

Updated 24 Oct 2026 to the rulings of the October 2026 review round
(`data/review/round-2026-10/plans/FTD.md`, `FTD-summary.md`) and to the decisions on its open
questions (`plans/FTD-decisions.md`). Reviewer 1's July 2026 tool rulings
(`agent-platform/config/review/condition_tool_guidance.yaml`, `ftd:`) govern the tiers except
where section 2 says otherwise and why.

---

## 1. Diagnostic criteria

**bvFTD (FTDC, Rascovsky 2011) [Rascovsky_2011].**

- Possible bvFTD: progressive deterioration of behaviour or cognition with at least 3 of 6
  features, "early" meaning within the first 3 years: early disinhibition; early apathy or
  inertia; early loss of sympathy or empathy; perseverative, stereotyped or compulsive behaviour;
  hyperorality or dietary change; an executive-predominant neuropsychological profile with
  relative sparing of memory and visuospatial function.
- Probable bvFTD: possible bvFTD plus significant functional decline plus imaging consistent
  with bvFTD (frontal and/or anterior temporal atrophy on MRI or CT, or frontal and/or anterior
  temporal hypoperfusion or hypometabolism on SPECT or PET).
- Definite bvFTD: possible or probable bvFTD plus histopathology or a known pathogenic mutation.
  A known carrier who develops the syndrome (FTD-M06, GRN) is definite.
- Exclusions: a better non-degenerative or medical explanation, a better psychiatric
  explanation, or biomarkers strongly indicating Alzheimer disease or another neurodegenerative
  process.
- Labels state the level the case's required (and, where recommended, functional-imaging) data
  support. A level reached only through an optional test is not the label: the cases whose
  authored panel is pathogenic (C9orf72 in M02, P01, P04, P05, P07, P08, S03, S05, S10; GRN in
  P02 and S07; MAPT in P03) stay "probable" although that optional result would make them
  definite.

**PPA (Gorno-Tempini 2011) [Gorno_Tempini_2011].** Language is the most prominent deficit and the
main cause of impaired daily living.

- svPPA: impaired confrontation naming and impaired single-word comprehension, plus at least 3 of
  impaired object knowledge, surface dyslexia or dysgraphia, spared repetition and spared speech
  production. Imaging support: anterior temporal atrophy or hypometabolism.
- nfvPPA: agrammatism or effortful, halting speech with inconsistent speech sound errors (apraxia
  of speech), plus at least 2 of impaired comprehension of syntactically complex sentences, spared
  single-word comprehension and spared object knowledge. Imaging support: left posterior
  fronto-insular atrophy or hypometabolism. Underlying pathology is often PSP or CBD.
- lvPPA is usually Alzheimer pathology and belongs to ALZ-EARLY, not here.
- PPA cases are not scored against the Rascovsky features: their clinical-assessment output uses
  Gorno-Tempini keys in `criteria_met`.

**FTD with motor neuron disease (Strong 2017) [Strong_2017].** ALS by Gold Coast criteria
[Gold_Coast_2020] (EMG by Awaji [Awaji_2008]) plus bvFTD or PPA. EMG establishes lower motor
neuron involvement and is required; respiratory function is staging (recommended, never
required), as in ALS.

**Psychiatric mimics (Ducharme 2020) [Ducharme_2020].** New behavioural change after about 40 with
progressive functional decline is not explained by a prior, stable psychiatric illness; a normal
early MRI does not exclude bvFTD. Lithium toxicity (above 1.0 mmol/L) and valproate toxicity
(encephalopathy, hyperammonaemia, valproate-induced parkinsonism and cognitive decline) are
reversible mimics checked with `interpret_labs` (`lithium_level`; `valproate_level`, `ammonia`),
never with a drug-interaction check.

## 2. Standard workup hierarchy

Order of `action_criteria` and `followup_outputs`: clinical assessment, neuropsychology (and the
speech-language evaluation in PPA), reversible-cause labs and case-specific levels or serology,
structural imaging (CT first only in the ED case), EMG in FTD-MND, functional imaging, AD
biomarker, genetics, respiratory staging, drug check, literature last.

**Required:**
- `perform_clinical_assessment` (`assessment_type: cognitive_screen`) — informant history scored
  against the six Rascovsky features (one finding per feature, informant line, bedside screen with
  its score and lost domains, functional decline); Gorno-Tempini keys in S11 and S12. The bedside
  screen's scores belong to this output, not to `patient.neurological_exam` [Rascovsky_2011]
- `order_specialized_test` (`test_type: neuropsych_battery`) — executive and social-cognition
  profile, relative sparing of memory and visuospatial function; Reviewer 1 requires it in all 30
  cases, PPA included [Rascovsky_2011]
- `interpret_labs` (`panels: CBC, CMP, TSH, B12, folate, ESR, CRP`) — reversible contributors
  [NICE_NG97] [SNLG_ISS_2024]. CMP carries electrolytes, renal and liver function, calcium and
  glucose. P08 adds CK. Syphilis and HIV serology, copper, heavy metals, autoimmune antibodies,
  toxicology and progranulin are targeted extras, stored as keyed follow-ups and scored only where
  the presentation supplies the question
- `analyze_brain_mri` (`contrast: false, protocol: dementia`) — frontal and anterior temporal
  atrophy, exclusion of structural and vascular causes; gadolinium adds nothing [Rascovsky_2011]
  [NICE_NG97]. `order_ct_scan` is required instead only in S06 (claustrophobia, sedation declined;
  MRI is then a waste avoided action, not harm) and first, before MRI, in the ED case M09
- Case-specific required: `interpret_labs` `lithium_level` (M05), `valproate_level` and `ammonia`
  (P01), `tox_screen` and `BAL` (M09), `HIV_viral_load` and `CD4_count` (M08);
  `analyze_csf` `special_tests: [HIV_RNA]` (M08, CSF escape; JCV PCR and cryptococcal antigen are
  an optional criterion because the white matter is normal and the CD4 count is 680);
  `order_specialized_test` `emg_ncs` (P08)

**Recommended:**
- `order_advanced_imaging` (`modality: FDG_PET`, alternative `perfusion_SPECT`) in P01, P02, P05
  and P07, where the MRI is normal or equivocal: functional imaging is then the imaging support
  that probable bvFTD requires [Rascovsky_2011] [Foster_2007] [NICE_NG97]. This departs from
  Reviewer 1's "optional"; the guidance entry asks the reviewer to confirm it
- `order_specialized_test` (`test_type: speech_language_evaluation`) in S11 and S12: the variant
  features (naming, single-word comprehension, object knowledge, irregular-word reading,
  repetition, grammar, motor speech) [Gorno_Tempini_2011]
- `order_specialized_test` (`test_type: respiratory_function`) in P08 (staging) [AAN_2009]
- `check_drug_interactions` only in M08 (sertraline against bictegravir, emtricitabine and
  tenofovir alafenamide; no cobicistat in that regimen)

**Optional:**
- FDG-PET (alternative perfusion SPECT) in every other case; S12 stores perfusion SPECT with
  FDG-PET as its alternative. Every case authors both results, concordant with its MRI, so no
  functional-imaging order receives the library's normal scan [Foster_2007] [NICE_NG97]
- AD biomarker, one criterion with two alternatives (CSF `Abeta42`, `phospho_tau`[, `total_tau`]
  or `amyloid_PET`) where Alzheimer disease stays in the differential: M02, M04, P03, P06. A
  negative result makes Alzheimer pathology unlikely; it does not exclude FTLD [Frisoni_2024]
  [Amyloid_PET_AUC_2025]
- Genetics `genetic_panel:FTD` (P08 also `genetic_panel:ALS`), after counselling, in every bvFTD
  case (27 cases, all with onset before 65); never required or recommended. The FTD consortium
  advises C9orf72 screening in every possible or probable bvFTD [Ducharme_2020], while UK
  eligibility (NHS GeneTYPES) requires onset before about 55, a family history suggestive of FTD, ALS or
  early-onset dementia, or MND in the patient or a relative; the panel is therefore optional
  everywhere, and counselling is a must only where the UK criteria are met [Pottier_2016]
  [ACMG_NSGC_2011]. M06 (known GRN carrier) has no genetics criterion; S11 and
  S12 (sporadic PPA, low yield) have none. Any case with an authored pathogenic result also
  authors every panel that contains the gene (C9orf72 on both the FTD and the ALS panel)
- `interpret_labs` `plasma_progranulin` (P02 only; never in a known GRN carrier)
- `order_advanced_imaging` `DaTscan` (P04 only, known Parkinson's disease)
- `check_drug_interactions` with a concrete interaction only (sertraline in M01, M04, M05, S01,
  S02, S09; escitalopram in P03). Outputs name the agent without a dose, list interactions with
  the actual medication list, and carry no cholinesterase-inhibitor, genetics or surveillance text
- `search_medical_literature` — never a clinical step (ruling 5): optional, last, outside the stop
  rule, canonical general text per syndrome, no case finding and no phrase of any
  `expected_evidence`

## 3. Tools that are typically USELESS (waste avoided actions)

- `analyze_eeg`, `analyze_ecg`, `order_echocardiogram`, `order_cardiac_monitoring` — unrelated
- `order_ct_scan` — MRI is the study; CT only in S06 and M09 (section 2)
- `order_advanced_imaging` `DaTscan` (except P04), `MR_spectroscopy`, `perfusion_MRI`,
  `carotid_duplex` — not FTD tests (Reviewer 1); tau PET and vascular imaging are absent
- `analyze_csf` outside M08 and the AD-biomarker alternative — no criterion; the library answers
  per assay
- Case fallbacks for these tools are short normal reports with an exact discriminator
  (`echo_type: TTE`, `monitor_type: holter_24h`); there is no `advanced_imaging`, `csf`,
  `drug_interactions` or `literature_search` fallback

## 4. Tools that are HARMFUL / contraindicated

- None routinely. LP is safe once MRI excludes mass effect. MRI in S06 is futile (declined), not
  harmful: waste.

## 5. Sequence constraints (all soft; no order in this condition is unsafe in reverse)

- MRI before CSF (M08 and every AD-biomarker criterion with a CSF alternative): "Imaging first
  excludes a mass lesion before lumbar puncture and shows whether white-matter disease makes JCV
  testing relevant." [NICE_NG97]
- CT before MRI (M09): "In the emergency department CT is the first rapid study; MRI characterises
  the degenerative pattern afterwards." [NICE_NG97]
- EMG before genetics (P08): "The motor neuron diagnosis is established clinically and
  electrophysiologically before genetic testing is discussed." [EAN_ALS_2024]
- Clinical assessment before genetics (every genetics criterion): "Genetic testing follows the
  clinical diagnosis and counselling." [ACMG_NSGC_2011]
- No assessment-before-neuropsychology or assessment-before-MRI constraint: parallel ordering is
  normal practice.
- Stop rule: `required_before_assessment` = exactly the required criteria (no literature, no
  drug check); `max_additional_actions` 0.

## 6. Subtype variations

- **M:** bvFTD with a comorbid contributor or mimic weighed and excluded: small-vessel disease
  (M03), lithium (M05), alcohol (M07), HIV (M08), an ED presentation (M09), right temporal
  variant (M10) [Ulugut_2020], a known GRN carrier (M06)
- **P:** puzzles: normal or equivocal MRI (P01, P02, P05, P07: functional imaging recommended),
  psychiatric misdiagnosis, co-existing Parkinson's disease (P04) [Postuma_2015], APOE e4 with
  maternal AD (P06), FTD-MND (P08)
- **S:** probable bvFTD meeting Rascovsky (S01-S10); svPPA (S11) and nfvPPA (S12)

## 7. Common red herrings and pitfalls

- **Memory complaints and a failed bedside recall or clock** — common in bvFTD; the impression
  then says that memory and visuospatial items are impaired and Alzheimer disease stays in the
  differential until the battery or a biomarker settles it
- **"Depression" or a prior psychiatric diagnosis** — apathy is mistaken for depression; a
  late-life, progressive syndrome needs the neurodegenerative work-up [Ducharme_2020]
- **Normal MRI early** — common, especially with C9orf72; FDG-PET or SPECT supplies the imaging
  support
- **Negative family history** — most FTD is sporadic; a negative panel does not exclude FTLD
- **Mild symmetric rigidity** — kept only where coherent with the stage or genotype (S01, S04,
  S07, S09): "compatible with bvFTD and does not by itself call for dopamine transporter imaging"
- **Amyloid** — no case claims an amyloid result it did not author; "negative amyloid excludes
  neurodegeneration" is false
- **Treatment** — no disease-modifying therapy. SSRIs (sertraline, citalopram) or trazodone for
  disinhibition, compulsions and agitation. Canonical prohibitions in every case: "Do not start a
  cholinesterase inhibitor (donepezil, rivastigmine, galantamine): no benefit in FTD, NICE NG97
  advises against it, and it may worsen behaviour." and "Do not start memantine: a randomised
  trial showed no benefit in FTD and NICE NG97 advises against it." [NICE_NG97] [Boxer_2013].
  Antipsychotics only as a last resort; benzodiazepines risk falls and paradoxical
  disinhibition
- **Safety and capacity** are musts, never tool calls: driving, finances and fiduciary roles,
  firearms, work, lasting power of attorney, caregiver support
- **Drug interactions** — sertraline with NSAIDs or aspirin (bleeding), thiazides or lithium
  (hyponatraemia; lithium also serotonin toxicity), tramadol or triptans (serotonin toxicity);
  no clinically significant interaction with metformin, levothyroxine or methotrexate. The check
  is not a toxicity test
- **Differential at assessment time** — a mimic the required work-up excludes is `low`, with what
  excludes it

## 8. Allowed citations

Every key cited in the 30 cases is listed here with its full reference.

- `[Rascovsky_2011]` — Rascovsky K et al. Sensitivity of revised diagnostic criteria for the behavioural variant of frontotemporal dementia. Brain 2011;134(9):2456-2477
- `[Gorno_Tempini_2011]` — Gorno-Tempini ML et al. Classification of primary progressive aphasia and its variants. Neurology 2011;76(11):1006-1014
- `[Foster_2007]` — Foster NL et al. FDG-PET improves accuracy in distinguishing frontotemporal dementia and Alzheimer's disease. Brain 2007;130(10):2616-2635
- `[Pottier_2016]` — Pottier C, Ravenscroft TA, Sanchez-Contreras M, Rademakers R. Genetics of FTLD: overview and what else we can expect from genetic studies. J Neurochem 2016;138(Suppl 1):32-53, doi 10.1111/jnc.13622 (the reference previously given here, "Curr Opin Neurol 2016;29:710-718", was wrong)
- `[Bang_2015]` — Bang J, Spina S, Miller BL. Frontotemporal dementia. Lancet 2015;386(10004):1672-1682
- `[NICE_NG97]` — NICE guideline NG97. Dementia: assessment, management and support for people living with dementia and their carers. 2018 (baseline blood tests; FDG-PET or perfusion SPECT when FTD is suspected and the subtype is uncertain; no cholinesterase inhibitor or memantine in FTD)
- `[SNLG_ISS_2024]` — Istituto Superiore di Sanità. Linea guida "Diagnosi e trattamento di demenza e Mild Cognitive Impairment". Sistema Nazionale Linee Guida, 2024 (GRADE-ADOLOPMENT of NICE NG97; Reviewer 1's source for the laboratory panel)
- `[Frisoni_2024]` — Frisoni GB et al. European intersocietal recommendations for the biomarker-based diagnosis of neurocognitive disorders. Lancet Neurol 2024;23(3):302-312
- `[Amyloid_PET_AUC_2025]` — Rabinovici GD et al. Updated appropriate use criteria for amyloid and tau PET: a report from the Alzheimer's Association and Society for Nuclear Medicine and Molecular Imaging Workgroup. Alzheimers Dement 2025;21(1):e14338
- `[Ducharme_2020]` — Ducharme S et al. Recommendations to distinguish behavioural variant frontotemporal dementia from psychiatric disorders. Brain 2020;143(6):1632-1650
- `[ACMG_NSGC_2011]` — Goldman JS et al. Genetic counseling and testing for Alzheimer disease: joint practice guidelines of the American College of Medical Genetics and the National Society of Genetic Counselors. Genet Med 2011;13(6):597-605
- `[Strong_2017]` — Strong MJ et al. Amyotrophic lateral sclerosis - frontotemporal spectrum disorder (ALS-FTSD): revised diagnostic criteria. Amyotroph Lateral Scler Frontotemporal Degener 2017;18(3-4):153-174
- `[Boxer_2013]` — Boxer AL et al. Memantine in patients with frontotemporal lobar degeneration: a multicentre, randomised, double-blind, placebo-controlled trial. Lancet Neurol 2013;12(2):149-156
- `[Ulugut_2020]` — Ulugut Erkoyun H et al. A clinical-radiological framework of the right temporal variant of frontotemporal dementia. Brain 2020;143(9):2831-2843
- `[Postuma_2015]` — Postuma RB et al. MDS clinical diagnostic criteria for Parkinson's disease. Mov Disord 2015;30(12):1591-1601
- `[Gold_Coast_2020]` — Shefner JM et al. A proposal for new diagnostic criteria for ALS. Clin Neurophysiol 2020;131(8):1975-1978
- `[Awaji_2008]` — de Carvalho M et al. Electrodiagnostic criteria for diagnosis of ALS. Clin Neurophysiol 2008;119(3):497-503
- `[EAN_ALS_2024]` — Van Damme P et al. European Academy of Neurology (EAN) guideline on the management of amyotrophic lateral sclerosis in collaboration with European Reference Networks for Neuromuscular Diseases (ERN EURO-NMD). Eur J Neurol 2024;31(6):e16264
- `[NICE_NG42]` — NICE guideline NG42. Motor neurone disease: assessment and management. 2016 (updated 2019)
- `[EACS_2025]` — European AIDS Clinical Society. EACS Guidelines, version 13.0, 2025 (HIV-associated neurocognitive impairment, CSF viral escape, antiretroviral drug interactions; M08)
- `[AAN_2009]` — Miller RG et al. Practice parameter update: the care of the patient with amyotrophic lateral sclerosis: drug, nutritional, and respiratory therapies (an evidence-based review). Neurology 2009;73(15):1218-1226

Retired (no FTD case cites them since the October 2026 round):

- `[AAN_dementia_2018]` — Petersen RC et al., practice guideline update summary: mild cognitive impairment, Neurology 2018;90(3):126-135. It governs MCI, not FTD laboratory testing or sequencing; replaced by `[NICE_NG97]` and `[SNLG_ISS_2024]`
- Lebert F et al. on trazodone in FTD was cited as "J Neurol Neurosurg Psychiatry 2004"; the trial is Dement Geriatr Cogn Disord 2004;17(4):355-359. No case cites it now
