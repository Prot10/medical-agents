# Criteria pack: Alzheimer's disease (MCI due to AD and mild dementia due to AD)

**ICD-10-CM, per case:** G31.84 for mild cognitive impairment due to AD; G30.0 for dementia due
to AD with symptom onset before 65 years; G30.1 with onset at 65 or later (age at **onset**, not at
the visit, decides). G30.9 (unspecified) and G30.8 (atypical presentations) are accepted synonyms,
not primary codes.
**Condition enum:** `NeurologicalCondition.ALZHEIMERS_EARLY`
**Case ID prefix:** `ALZ-EARLY`

Updated 24 Oct 2026 to the rulings of the October 2026 physician-review round
(`data/review/round-2026-10/plans/ALZ-EARLY.md`, `ALZ-EARLY-summary.md`) and to the decisions on
its open questions (`plans/ALZ-EARLY-decisions.md`).

---

## 1. Diagnostic criteria

**Clinical diagnosis (governs every label in this condition).** Dementia due to AD per NIA-AA 2011
[NIA_AA_2011]; MCI due to AD per Albert 2011 [NIA_AA_MCI_2011].

- **MCI:** concern about a change in cognition; impairment in one or more domains beyond age and
  education norms; **independence in functional abilities preserved** (the patient may be slower,
  less efficient or use aids and reminders); not demented.
- **Dementia:** the cognitive impairment interferes with work or usual activities. Operational rule:
  instrumental independence is **lost** when another person has taken over, or must supervise, at
  least one complex activity (finances, medicines, driving, cooking safety, work duties) because of
  cognition, or there are repeated safety incidents (getting lost or car accidents, missed medicines
  with consequences, stove left on, scams). It is **preserved** when errors are isolated and the
  patient's own strategies (calendar, pill box, phone reminders) compensate them. HPI, the
  `independence_in_instrumental_activities_lost` field, the clinical-assessment and
  neuropsychology impressions, the label, the ICD code and the musts carry one staging.
- **MCI biomarker likelihood (Albert 2011):** intermediate when one biomarker category is positive
  or only one is tested, or neuronal injury is borderline; high when an amyloid marker and a neuronal
  injury marker (CSF tau, clear hippocampal atrophy, FDG hypometabolism) are both positive.

**Biomarker description (NIA-AA 2018, AA 2024).** A = amyloid (CSF Abeta42 or Abeta42/40 ratio,
amyloid PET); T = phosphorylated tau (CSF p-tau, tau PET); N = neurodegeneration (MRI atrophy, FDG
hypometabolism, CSF total tau) [NIA_AA_2018]. The Alzheimer's Association 2024 revision [AA_2024]
treats one abnormal Core 1 biomarker (amyloid PET, CSF Abeta42/40, CSF p-tau181/Abeta42 or
t-tau/Abeta42) as sufficient for the biological diagnosis; the International Working Group 2024
[IWG_2024] requires a clinical phenotype as well. Every case here is symptomatic, so both agree on
the cases' diagnoses. Decision (Q1, Oct 2026): labels follow the clinical criteria above; reports
and impressions name the measured profile ("decreased Abeta42/40 ratio with p-tau within the
laboratory range") and say "A+T+" or "biomarker-confirmed" only when amyloid and p-tau are both
abnormal. A report without an Abeta40 value states no ratio.

**Atypical phenotypes.** Posterior cortical atrophy [PCA_consensus_2017]; logopenic variant PPA
[PPA_2011] (a PPA with preserved instrumental function is not staged as dementia); behavioural or
dysexecutive AD [bvAD_2015], with bvFTD excluded by AD biomarkers [FTDC_2011].

## 2. Standard workup hierarchy

Order of `action_criteria` and `followup_outputs`: clinical assessment, neuropsychology, labs (MMA
reflex), structural imaging, case-specific studies (visual fields, gait/tap test), amyloid status,
FDG-PET, EEG/DaTscan exceptions, genetics, drug check, ECG. No literature step.

**Required:**
- `perform_clinical_assessment` (`assessment_type: cognitive_screen`) — instrument and score, domains, cueing, informant report and functional staging per section 1 [NIA_AA_2011] [NIA_AA_MCI_2011]
- `order_specialized_test` (`test_type: neuropsych_battery`) — domain profile with age-, education- and language-appropriate norms; variant-specific subtests (visuospatial for PCA; naming, repetition and comprehension for lvPPA; executive for frontal AD) [NIA_AA_2011]
- `interpret_labs` (CBC, CMP, TSH, B12, folate, homocysteine, magnesium, ESR, CRP; RPR/HIV where risk) — reversible contributors [AAN_dementia_2018]; values, units, ranges and flags only (`clinical_significance` null)
- `analyze_brain_mri` (non-contrast dementia protocol) — medial temporal atrophy (Scheltens MTA), small-vessel disease (STRIVE terms, Fazekas), microbleed distribution, NPH signs, mass [NIA_AA_2011] [STRIVE_2013]; `order_ct_scan` only when MRI is contraindicated (RS05)

**Recommended:**
- `interpret_labs` (`panels: ["MMA"]`) — when serum B12 is low-normal (about 300 pg/mL or below) [BSH_B12_2014]. NICE NG239 (2024) treats 180-350 ng/L as indeterminate; with a normal homocysteine in the panel, a B12 of 300-350 pg/mL needs no MMA criterion in this dataset [NICE_NG239]

**Optional:**
- Amyloid status, one criterion with two alternatives: `analyze_csf` (`special_tests: Abeta42, Abeta42_40_ratio, phospho_tau, total_tau`) or `order_advanced_imaging` (`modality: amyloid_PET`). One conclusive test is enough; it is indicated when the diagnosis remains uncertain after clinical, neuropsychological and MRI assessment, in young onset or atypical presentations, or when anti-amyloid treatment is considered [NIA_AA_2018] [Appropriate_Use_Amyloid_PET]. Both alternatives have a case-authored concordant result in every case. RP04 is the exception: CSF is **required** and single-alternative, with 14-3-3 and RT-QuIC, because the question is sporadic CJD [CJD_2021]
- `order_advanced_imaging` (`modality: FDG_PET`, perfusion SPECT as substitute) — atypical variants or an AD versus FTD/DLB question [Foster_2007]. Every case authors an FDG-PET result (criterion or not), so an unanticipated order never receives the library's normal scan
- `order_specialized_test` (`test_type: genetic_panel:early_onset_AD`; P03 also `genetic_panel:FTD`) — young onset or autosomal-dominant pattern, after pre-test counselling [ACMG_NSGC_2011] [Bateman_2012]
- `check_drug_interactions` (`drug: donepezil`) — dementia-staged cases only, after the diagnosis; **required** only with a concrete interaction (QT-prolonging co-medication, strong CYP2D6 inhibitor): P04, RP02, RP03. Never in MCI cases
- `analyze_ecg` — only with donepezil plus a QT-prolonging drug (P04, RP02)
- `analyze_eeg` — RP04 (periodic complexes, CJD) and RP05 (recurrent unresponsive spells) [NICE_NG217]
- `order_specialized_test` visual fields / OCT (PCA, P01), `perform_clinical_assessment` `gait_and_balance_timed` with tap test (RM02) [iNPH_2005]

## 3. Tools that are typically USELESS

- `analyze_eeg` — non-specific in AD, except the two cases above
- `analyze_ecg` — unrelated, except donepezil with a QT-prolonging drug
- `order_echocardiogram`, `order_cardiac_monitoring` — unrelated
- `order_ct_scan` — MRI is preferred; CT only if MRI is contraindicated
- `order_advanced_imaging` (`modality: DaTscan`) — only with parkinsonism or a DLB question
- `order_advanced_imaging` (`modality: MR_spectroscopy / perfusion_MRI`) — research only
- `search_medical_literature` — never a clinical step (ruling 5); no criterion, no stored output

## 4. Tools that are HARMFUL / contraindicated

- MRI in a patient with an MRI-unsafe device (RS05): avoided action, CT is the structural study
- Otherwise none; LP is safe once imaging excludes mass effect

## 5. Sequence constraints (all soft)

- Structural imaging before `analyze_csf`: exclude mass effect before LP [NIA_AA_2011]
- Clinical assessment before the amyloid criterion: "Amyloid biomarkers are interpreted against an established clinical syndrome; they are not a screening test." [Appropriate_Use_Amyloid_PET]
- Neuropsychological battery before a genetic panel: "Genetic testing follows the clinical diagnosis and pre-test counselling." [ACMG_NSGC_2011]
- Stop rule: `required_before_assessment` = the required criteria; `max_additional_actions` 1

## 6. Subtype variations

- **M:** MCI due to AD or mild dementia with vascular or metabolic contributors; biomarkers optional
- **S:** typical amnestic mild dementia due to AD
- **P:** atypical (PCA, lvPPA, frontal) or autosomal-dominant early-onset AD; FDG-PET and genetics optional
- **R:** a mimic or contributor raised and weighed (NPH, CJD, DLB, depression, B12, thyroid, sedatives, meningioma), with AD as the diagnosis

## 7. Common red herrings and pitfalls

- **Staging:** MCI versus mild dementia is decided by instrumental function (section 1), not by the MMSE
- **Cholinesterase inhibitors in MCI:** not approved and not routinely recommended; prohibition "Do not start a cholinesterase inhibitor or memantine as routine treatment for mild cognitive impairment" [AAN_dementia_2018]. In mild AD dementia offer an AChEI after checking pulse, conduction and medicines [NICE_NG97]; memantine only for moderate or severe AD
- **Donepezil pharmacology:** CYP2D6 and CYP3A4 (not CYP2C19); bradycardia, heart block, QT prolongation; amlodipine does not slow the heart; tamsulosin is not anticholinergic; PPIs do not reduce donepezil absorption; levetiracetam does not lower the seizure threshold (bupropion and tramadol do)
- **Sedatives:** zolpidem and benzodiazepines are a deprescribing must with a taper [Beers_2023], not an interaction finding
- **Subclinical hypothyroidism** (TSH above range, free T4 normal): repeat TSH and free T4 with TPO antibodies in 2 to 3 months; no levothyroxine under TSH 10 mIU/L in older adults; not a reversible cause of dementia [ETA_SCH_2013] [TRUST_2017]
- **B12:** low-normal B12 is indeterminate (MMA, homocysteine); B12 deficiency with raised MMA is a treatable contributor, not an alternative to AD [BSH_B12_2014]
- **Microbleeds:** lobar points to CAA (relevant to anti-amyloid safety), deep to hypertensive arteriopathy [Boston_CAA_2022]
- **Ventriculomegaly:** Evans index above 0.3 is ventriculomegaly; DESH and an acute callosal angle support iNPH; a negative tap test lowers but does not exclude it [iNPH_2005] [iNPH_Japan_2021]
- **Contrast:** not part of the dementia MRI; no enhancement statements when `contrast` is false
- **CT:** states only qualitative medial temporal volume loss, no MTA grade without coronal reformats
- **Hippocampal atrophy in the elderly:** also in normal ageing; graded quantitatively (MTA 2 or more)
- **Vague family history of dementia; APOE e4:** risk factors, not diagnostic tests
- **DLB features** (fluctuations, hallucinations, RBD, parkinsonism): DLB low unless present [DLB_2017]
- **Differential at assessment time:** a mimic the work-up excludes is `low` with what excludes it

## 8. Allowed citations

- `[NIA_AA_2011]` — McKhann GM et al. The diagnosis of dementia due to Alzheimer's disease: recommendations from the NIA-AA workgroups. Alzheimers Dement 2011;7(3):263-269
- `[NIA_AA_MCI_2011]` — Albert MS et al. The diagnosis of mild cognitive impairment due to Alzheimer's disease: recommendations from the NIA-AA workgroups. Alzheimers Dement 2011;7(3):270-279
- `[NIA_AA_2018]` — Jack CR Jr et al. NIA-AA Research Framework: toward a biological definition of Alzheimer's disease. Alzheimers Dement 2018;14(4):535-562
- `[AA_2024]` — Jack CR Jr et al. Revised criteria for diagnosis and staging of Alzheimer's disease: Alzheimer's Association Workgroup. Alzheimers Dement 2024;20(8):5143-5169
- `[IWG_2024]` — Dubois B et al. Alzheimer disease as a clinical-biological construct: an International Working Group recommendation. JAMA Neurol 2024 (published online November 2024), doi 10.1001/jamaneurol.2024.3770
- `[AAN_dementia_2018]` — Petersen RC et al. Practice guideline update summary: mild cognitive impairment. Neurology 2018;90(3):126-135 (the current AAN MCI guideline; there is no "2023 AAN MCI guideline")
- `[NICE_NG97]` — NICE guideline NG97. Dementia: assessment, management and support for people living with dementia and their carers. 2018
- `[Appropriate_Use_Amyloid_PET]` — Rabinovici GD et al. Updated appropriate use criteria for amyloid and tau PET: a report from the Alzheimer's Association and Society for Nuclear Medicine and Molecular Imaging Workgroup. Alzheimers Dement 2025;21(1):e14338; J Nucl Med 2025;66(Suppl 2):S5-S31. Until October 2026 this key cited Johnson KA et al., Alzheimers Dement 2013;9(1):e1-e16, which the 2025 criteria supersede; every statement cited with the key holds under both
- `[Foster_2007]` — Foster NL et al. FDG-PET improves accuracy in distinguishing frontotemporal dementia and Alzheimer's disease. Brain 2007;130(10):2616-2635
- `[PCA_consensus_2017]` — Crutch SJ et al. Consensus classification of posterior cortical atrophy. Alzheimers Dement 2017;13(8):870-884
- `[PPA_2011]` — Gorno-Tempini ML et al. Classification of primary progressive aphasia and its variants. Neurology 2011;76(11):1006-1014
- `[bvAD_2015]` — Ossenkoppele R et al. The behavioural/dysexecutive variant of Alzheimer's disease: clinical, neuroimaging and pathological features. Brain 2015;138(9):2732-2749
- `[FTDC_2011]` — Rascovsky K et al. Sensitivity of revised diagnostic criteria for the behavioural variant of frontotemporal dementia. Brain 2011;134(9):2456-2477
- `[DLB_2017]` — McKeith IG et al. Diagnosis and management of dementia with Lewy bodies: fourth consensus report of the DLB Consortium. Neurology 2017;89(1):88-100
- `[CJD_2021]` — Hermann P et al. Biomarkers and diagnostic guidelines for sporadic Creutzfeldt-Jakob disease. Lancet Neurol 2021;20(3):235-246
- `[iNPH_2005]` — Relkin N et al. Diagnosing idiopathic normal-pressure hydrocephalus. Neurosurgery 2005;57(3 Suppl):S4-S16
- `[iNPH_Japan_2021]` — Nakajima M et al. Guidelines for management of idiopathic normal pressure hydrocephalus (third edition). Neurol Med Chir (Tokyo) 2021;61(2):63-97
- `[Boston_CAA_2022]` — Charidimou A et al. The Boston criteria version 2.0 for cerebral amyloid angiopathy. Lancet Neurol 2022;21(8):714-725
- `[STRIVE_2013]` — Wardlaw JM et al. Neuroimaging standards for research into small vessel disease and its contribution to ageing and neurodegeneration. Lancet Neurol 2013;12(8):822-838
- `[ACMG_NSGC_2011]` — Goldman JS et al. Genetic counseling and testing for Alzheimer disease: joint practice guidelines of the ACMG and NSGC. Genet Med 2011;13(6):597-605
- `[Bateman_2012]` — Bateman RJ et al. Clinical and biomarker changes in dominantly inherited Alzheimer's disease. N Engl J Med 2012;367(9):795-804
- `[BSH_B12_2014]` — Devalia V et al. Guidelines for the diagnosis and treatment of cobalamin and folate disorders. Br J Haematol 2014;166(4):496-513
- `[NICE_NG239]` — NICE guideline NG239. Vitamin B12 deficiency in over 16s: diagnosis and management. 2024
- `[ETA_SCH_2013]` — Pearce SH et al. 2013 ETA guideline: management of subclinical hypothyroidism. Eur Thyroid J 2013;2(4):215-228
- `[TRUST_2017]` — Stott DJ et al. Thyroid hormone therapy for older adults with subclinical hypothyroidism. N Engl J Med 2017;376(26):2534-2544
- `[ATA_hypothyroidism_2014]` — Jonklaas J et al. Guidelines for the treatment of hypothyroidism. Thyroid 2014;24(12):1670-1751 (overt hypothyroidism and levothyroxine dosing)
- `[Beers_2023]` — American Geriatrics Society 2023 updated AGS Beers Criteria for potentially inappropriate medication use in older adults. J Am Geriatr Soc 2023;71(7):2052-2081
- `[ADA_older_adults_2026]` — American Diabetes Association Professional Practice Committee. 13. Older adults: Standards of Care in Diabetes-2026. Diabetes Care 2026;49(Suppl 1):S277-S296 (A1C below 8.0% for complex/intermediate health including mild to moderate cognitive impairment, Table 13.2)
- `[AHA_secondary_stroke_2021]` — Kleindorfer DO et al. 2021 Guideline for the prevention of stroke in patients with stroke and transient ischemic attack. Stroke 2021;52(7):e364-e467
- `[ACC_AHA_dyslipidemia_2026]` — Blumenthal RS et al. 2026 ACC/AHA/AACVPR/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA Guideline on the management of dyslipidemia. Circulation 2026;153(17):e1154-e1276; J Am Coll Cardiol 2026, doi 10.1016/j.jacc.2025.11.016
- `[BSG_IDA_2021]` — Snook J et al. British Society of Gastroenterology guidelines for the management of iron deficiency anaemia in adults. Gut 2021;70(11):2030-2051
- `[NICE_NG217]` — NICE guideline NG217. Epilepsies in children, young people and adults. 2022
- `[CLARITY_AD_2023]` — van Dyck CH et al. Lecanemab in early Alzheimer's disease. N Engl J Med 2023;388(1):9-21 (only where a case discusses anti-amyloid treatment)
- `[Lecanemab_AUR_2023]` — Cummings J et al. Lecanemab: appropriate use recommendations. J Prev Alzheimers Dis 2023;10(3):362-377 (as above)

**Superseded (do not cite; kept for traceability):**
- `[ADA_older_adults_2025]` — ADA. 13. Older adults: Standards of Care in Diabetes-2025. Diabetes Care 2025;48(Suppl 1):S266-S282. Superseded by the 2026 edition (same A1C targets); M05, RP04 and RP05 re-cited 24 Oct 2026
- `[AHA_ACC_cholesterol_2018]` — Grundy SM et al. 2018 AHA/ACC guideline on the management of blood cholesterol. Circulation 2019;139(25):e1082-e1143. Retired by the 2026 dyslipidemia guideline; RP01 re-cited 24 Oct 2026
- `[McKeith_2017_DLB]` — alias of `[DLB_2017]`; use `[DLB_2017]`
