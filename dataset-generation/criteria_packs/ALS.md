# Criteria pack: Amyotrophic Lateral Sclerosis (ALS)

**ICD-10:** G12.21
**Condition enum:** `NeurologicalCondition.ALS`
**Case ID prefix:** `ALS`

Updated 24 Oct 2026 to the rulings of the October 2026 physician-review round
(`data/review/round-2026-10/plans/ALS.md`, `ALS-summary.md`) and to the decisions on its open
questions (`plans/ALS-decisions.md`).

---

## 1. Diagnostic criteria

Gold Coast criteria 2020 govern the diagnosis [Gold_Coast_2020]: progressive
motor impairment documented by history or repeated examination, preceded by
normal motor function; plus upper and lower motor neuron dysfunction in at
least one body region, or lower motor neuron dysfunction in at least two body
regions; plus investigations excluding other disease processes. Body regions:
bulbar, cervical, thoracic, lumbosacral.

Electrodiagnosis follows Awaji 2008 [Awaji_2008]: EMG lower motor neuron
evidence is chronic neurogenic change (large, long-duration or unstable motor
unit potentials, reduced recruitment) together with active denervation
(fibrillation potentials or positive sharp waves); fasciculation potentials
count as active denervation in a muscle that shows chronic neurogenic change.
Complex fasciculations alone, or fasciculations without chronic change, raise
concern but are not diagnostic. A region counts for lower motor neuron
dysfunction only with clinical weakness and wasting, or EMG chronic change plus
active denervation; fibrillations alone are described as "active denervation
also in ...".

Where Gold Coast and Awaji/El Escorial categories diverge, Gold Coast governs.
Awaji categories ("possible", "probable", "definite") may be named only as a
secondary description and only where the data meet them; never call a first
EMG with active denervation in one region "definite". El Escorial is not cited
as the current criterion.

## 2. Standard workup hierarchy

Canonical criterion order (the review app reads it as the work-up sequence):
EMG/NCS, brain MRI, spine MRI, labs, (CSF where indicated), respiratory
function, genetic panel, riluzole interaction check.

**Required:**
- `order_specialized_test` (`test_type: emg_ncs`): bulbar, cervical, thoracic and lumbosacral regions; documents lower motor neuron involvement and excludes multifocal motor neuropathy with conduction block, demyelinating or sensorimotor neuropathy and myopathy. Normal sensory responses also argue against SBMA (Kennedy disease) [Gold_Coast_2020] [Awaji_2008]
- `analyze_brain_mri` (`{}`, contrast not required unless the case raises a leptomeningeal, MS/PML or HIV question): excludes brain and brainstem structural, vascular, demyelinating, inflammatory or neoplastic causes of the upper motor neuron or bulbar signs. MRI does not confirm ALS; corticospinal tract T2/FLAIR signal or a motor-cortex low T2 rim is supportive at most [EFNS_ALS_2012] [Gold_Coast_2020]
- `order_body_imaging` (`study: spine_MRI`): cervical and thoracic cord, and the lumbosacral spine when lower limb signs need it, to exclude compressive myelopathy, radiculopathy and other cord lesions. It is a **separate study** from the brain MRI (the brain tool has no spine parameter). Incidental spondylosis does not explain bulbar signs or denervation in other regions and must not delay the work-up [EFNS_ALS_2012] [Gold_Coast_2020]
- `interpret_labs` (core `CBC`, `CK`, `TSH`, `vitamin_B12`, plus renal and liver function, electrolytes and calcium, folate, ESR and CRP; phenotype-specific tests only when the case raises that mimic: paraneoplastic panel, free T4, anti-GM1 IgM, androgen receptor CAG repeat in men, HIV, SPEP/IFE/free light chains/anti-MAG, blood lead): excludes metabolic, endocrine, nutritional and inflammatory mimics and gives the liver and blood-count baseline needed before riluzole [EFNS_ALS_2012]

**Recommended:**
- `order_specialized_test` (`test_type: respiratory_function`): FVC and SNIP, with MIP where available. Staging, never diagnosis and never required: once ALS is supported it stages respiratory muscle weakness, sets the baseline for 3-monthly monitoring and identifies patients who need early NIV referral. Optional where ALS is not established (mimic or carrier cases) [AAN_2009] [EAN_ALS_2024] [NICE_NG42]
- `check_drug_interactions` (`drug: riluzole`): last step, after the diagnosis is established, wherever riluzole is a must. **Required** only when the case has a concrete interaction that changes management (e.g. methotrexate: both raise transaminases); omitted when riluzole is not indicated (ALS not established). Riluzole is not deferred once Gold Coast is met: it is offered at diagnosis [Riluzole_SmPC] [EAN_ALS_2024]

**Optional:**
- `order_specialized_test` (`test_type: genetic_panel:ALS`): C9orf72 repeat expansion plus SOD1, TARDBP, FUS and TBK1, after pre-test genetic counselling, once the clinical and electrodiagnostic assessment is complete. Genetic testing does not make the diagnosis; it is offered with counselling to people with ALS. **Recommended** in familial cases (first-degree or other relative with ALS or FTD); **required** where the result decides the label or a must (a carrier case, or post-test counselling of relatives about the variant found), and then also in the stop rule when the label names the genotype [ALS_genetics_2023] [EAN_ALS_2024]
- `analyze_csf`: only for a specific inflammatory, infectious or neoplastic mimic the case raises (leptomeningeal disease after cancer, MS/PML on natalizumab, HIV, MMN or paraproteinaemic neuropathy); CSF does not diagnose ALS [EFNS_ALS_2012]

**Not a clinical step:** `search_medical_literature` is not part of the pathway (October 2026 ruling 5): no literature criterion, no literature follow-up, `initial_tool_outputs.literature_search` null.

## 3. Tools that are typically USELESS

The eight waste avoided actions used across the condition:

- `analyze_eeg`: no role in ALS diagnosis; non-cortical motor disease
- `analyze_ecg`: unrelated unless comorbid cardiac disease
- `order_echocardiogram`: unrelated
- `order_cardiac_monitoring`: unrelated
- `order_ct_scan`: MRI is standard; CT only if MRI contraindicated
- `order_advanced_imaging` (`modality: amyloid_PET`, `DaTscan`, `FDG_PET`): none indicated for typical ALS

`analyze_csf` is not routine (section 2, optional only for a named mimic). It is not listed as waste: an unindicated LP is already penalised by the stop rule (`max_additional_actions` 0), and a waste entry would contradict the five cases that order it. Waste avoided actions cite [EFNS_ALS_2012] (the diagnostic-investigation guideline), not [AAN_2009].

## 4. Tools that are HARMFUL / contraindicated

(none routinely; ALS workup has no major harmful tool calls)

## 5. Sequence constraints

Both `soft` (no reverse order is unsafe in this condition):

- `order_specialized_test` (`emg_ncs`) → `order_specialized_test` (`genetic_panel:ALS`): genetic testing follows the clinical and electrodiagnostic assessment and pre-test counselling; it does not make the diagnosis [ALS_genetics_2023]
- `order_specialized_test` (`emg_ncs`) → `check_drug_interactions` (`riluzole`): riluzole is considered only after the clinical and electrodiagnostic assessment supports ALS [EAN_ALS_2024]

Stop rule: `required_before_assessment` = EMG/NCS, brain MRI, spine MRI, labs.

## 6. Subtype variations

- **M (mild):** typical presentation, single-region onset; standard workup
- **S (standard):** multi-region or bulbar onset; standard workup. Respiratory function stays recommended (staging), not required
- **P (progressive / puzzle):** rapid progression, respiratory involvement or a mimic; standard workup, respiratory function recommended. Genetic panel recommended when the family history is positive (required when the result decides the label or a must); optional with counselling otherwise. A P case may be an ALS mimic labelled with the mimic's own code (P02 thyrotoxicosis, E05.90) or a carrier who does not meet Gold Coast (P08, Z15.89), as other conditions file their mimic cases
- **R (reverse / mimic):** the case is NOT ALS. Typical mimics are MMN with conduction block (treatable), Kennedy disease (men only), IBM, cervical myelopathy, post-polio, thyrotoxicosis. For R cases the action policy adds rule-out criteria: anti-GM1 antibodies (under labs), repeat EMG with NCS for conduction block, spine MRI. Where ALS is not established, respiratory function and genetics are optional and the riluzole check is omitted

## 7. Common red-herring categories and pitfalls

- **Prior benign fasciculation diagnosis:** never closes the door on ALS; repeat EMG mandatory
- **CK elevation:** mild to moderate elevation is common in ALS from denervation and does not by itself suggest a myopathy. A CK above 5x ULN is higher than usual: say so, consider a myopathic contributor (statin myopathy on a statin), and note that the neurogenic EMG pattern argues against a primary myopathy
- **Cervical spine degeneration on MRI:** common at this age; does not explain bulbar signs or denervation in thoracic, lumbosacral or bulbar muscles. No surgical referral on the basis of it
- **Normal initial EMG:** early ALS can have a normal EMG; serial studies are needed
- **Symmetric weakness:** uncommon in ALS but does occur, especially the flail-arm variant
- **Anxiety or depression in the history:** can heighten symptom vigilance but cannot produce upper motor neuron signs or multi-region denervation
- **ALS phenotypes are not differentials:** progressive bulbar palsy, flail arm and LMN-predominant ALS are phenotypes, not competing diagnoses; Kennedy disease appears only in men
- **Spinal anatomy:** the adult cord ends at about L1-L2; findings at L3-S1 are cauda equina or roots, never "cord"
- **Reports stay region-pure:** brain MRI reports brain and brainstem only; spine MRI reports spine and cord only; a non-contrast study never comments on enhancement
- **CK above 5x ULN on a statin:** add a must to review the statin (pause and recheck CK in 2 to 6 weeks)
- **Pseudobulbar affect or cognitive change:** add a must for a validated cognitive and behavioural screen (ECAS) and for explaining and treating the affect [EAN_ALS_2024] [NICE_NG42]
- **Riluzole facts (SmPC):** 50 mg every 12 hours; transaminases before the first dose, monthly for 3 months, every 3 months for the rest of the first year, then periodically; stop if ALT exceeds 5x ULN; report febrile illness (neutropenia). CYP1A2 inhibitors (fluvoxamine, quinolones) raise exposure, inducers (smoking, rifampicin, omeprazole) lower it. Never claim grapefruit as a CYP1A2 modulator, riluzole as serotonergic or QTc-prolonging, levothyroxine or metformin CYP1A2 interactions, or natalizumab "lymphopenia" (it causes lymphocytosis)
- **Treatments never offered:** AMX0035 (Relyvrio, withdrawn April 2024) is never mentioned; edaravone is not recommended by EAN 2024 and never appears as an alternative inside an interaction check; tofersen only for a SOD1 pathogenic variant, as a specialist-centre decision after ALS is established
- **Respiratory reference values (dataset convention):** FVC >=80% predicted; SNIP >=70 cmH2O in men, >=60 cmH2O in women; MIP/NIF -60 cmH2O or more negative for both sexes (a deliberate single cut-off: it is the AAN 2009 NIV marker, not a sex-specific normal limit, which is higher in men). AAN 2009 markers that prompt NIV discussion: orthopnoea, FVC below 50% predicted, SNIP below 40 cmH2O, MIP weaker than -60 cmH2O, abnormal nocturnal oximetry [AAN_2009] [Bourke_2006]

## 8. Allowed citations

- `[Gold_Coast_2020]`: Shefner JM et al. A proposal for new diagnostic criteria for ALS. Clin Neurophysiol 2020;131:1975-1978
- `[Awaji_2008]`: de Carvalho M et al. Electrodiagnostic criteria for diagnosis of ALS. Clin Neurophysiol 2008;119:497-503
- `[EFNS_ALS_2012]`: Andersen PM et al. EFNS guidelines on the clinical management of amyotrophic lateral sclerosis (MALS). Eur J Neurol 2012;19:360-375
- `[EAN_ALS_2024]`: Van Damme P et al. European Academy of Neurology (EAN) guideline on the management of amyotrophic lateral sclerosis in collaboration with European Reference Network for Neuromuscular Diseases (ERN EURO-NMD). Eur J Neurol 2024;31(6):e16264
- `[NICE_NG42]`: NICE guideline NG42. Motor neurone disease: assessment and management. 2016, updated 2019
- `[AAN_2009]`: Miller RG et al. Practice Parameter update: The care of the patient with amyotrophic lateral sclerosis: drug, nutritional, and respiratory therapies (an evidence-based review). Neurology 2009;73:1218-1226 (riluzole, NIV thresholds, gastrostomy timing; not diagnostic work-up)
- `[Bourke_2006]`: Bourke SC et al. Effects of non-invasive ventilation on survival and quality of life in patients with amyotrophic lateral sclerosis. Lancet Neurol 2006;5:140-147
- `[ALS_genetics_2023]`: Roggenbuck J et al. Evidence-based consensus guidelines for ALS genetic testing and counseling. Ann Clin Transl Neurol 2023;10:2074-2091
- `[Riluzole_SmPC]`: Riluzole (Rilutek) Summary of Product Characteristics
- `[Brown_2017]`: Brown RH, Al-Chalabi A. Amyotrophic Lateral Sclerosis. NEJM 2017;377:162-172 (review, background only)
- `[ENCALS_2018]`: Westeneng HJ et al. Prognosis for patients with ALS: the ENCALS prediction model. Lancet Neurol 2018;17:423-433
