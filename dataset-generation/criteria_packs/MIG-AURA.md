# Criteria pack: Migraine with aura

**ICD-10:** G43.1x (ICD-10-CM G43.109 typical and brainstem aura, G43.409 hemiplegic migraine,
G43.609 migrainous infarction; mimic cases carry the mimic's own code)
**Condition enum:** `NeurologicalCondition.MIGRAINE_WITH_AURA`
**Case ID prefix:** `MIG-AURA`

Revised 24 October 2026 (review-round close-out, `data/review/round-2026-10/plans/MIG-AURA.md`
and `MIG-AURA-decisions.md`). The condition has no physician notes; the July 2026 tool review
(Reviewer 1) and the round plan govern.

---

## 1. Diagnostic criteria [ICHD_3]

**1.2 Migraine with aura.** A: at least two attacks fulfilling B and C. B: one or more fully
reversible aura symptoms (visual, sensory, speech and/or language, motor, brainstem, retinal).
C: at least three of six: (1) at least one aura symptom spreads gradually over 5 min or more;
(2) two or more aura symptoms occur in succession; (3) each individual aura symptom lasts 5-60
min (motor up to 72 h); (4) at least one aura symptom is unilateral; (5) at least one aura
symptom is positive; (6) the aura is accompanied or followed within 60 min by headache. D: not
better accounted for by another ICHD-3 diagnosis. The diagnosis is clinical: no test confirms it.

Codes used in the cases: 1.2.1 migraine with typical aura (1.2.1.1 with headache, 1.2.1.2 typical
aura without headache); 1.2.2 migraine with brainstem aura (at least two of dysarthria, vertigo,
tinnitus, hypacusis, diplopia, ataxia not attributable to sensory deficit, decreased level of
consciousness; no motor or retinal symptoms); 1.2.3 hemiplegic migraine (1.2.3.1 familial,
1.2.3.2 sporadic); 1.4.1 status migrainosus; 1.4.2 persistent aura without infarction; 1.4.3
migrainous infarction; 1.4.4 migraine aura-triggered seizure; 1.5.2 probable migraine with aura.

- A single attack that otherwise fulfils the criteria is **1.5.2 probable migraine with aura**,
  never 1.2.1 (M01, M07).
- **Migrainous infarction (1.4.3)** needs an attack typical of previous attacks except that one or
  more aura symptoms persist beyond 60 min, and an ischaemic infarct in the relevant area on
  imaging, not better accounted for by another cause. A 20-minute aura with an infarct is not
  migrainous infarction. Never write "1.4.1" for it (that is status migrainosus).
- **Migralepsy (1.4.4):** a seizure during, or within 1 h of, an aura.
- "Confusional aura" is not an ICHD-3 aura type; decreased consciousness is one brainstem symptom
  and two are needed for 1.2.2.
- **DWI.** A normal DWI excludes an acute infarct; it does not exclude a TIA (TIA is by definition
  without infarction). The distinction from TIA is clinical: positive symptoms, gradual spread over
  minutes, succession of symptoms, previous identical attacks. Never write "normal DWI excludes TIA".

## 2. Standard workup hierarchy

**Required in every case:**
- `perform_clinical_assessment` `assessment_type: structured_headache_history_ichd3`: the ICHD-3
  elements one by one with the patient's own data (attack count, each C criterion true or false
  with the count, examination, the SNNOOP10 flags present or absent by name). July 2026 ruling.

**Imaging, only for red flags** (Evans 2020 [AHS_neuroimaging_2020], grade A: no imaging for
migraine with a normal examination and no atypical feature):
- `analyze_brain_mri` (`required_arguments: {}`): recommended for first aura, aura over 60 min,
  motor, brainstem or isolated aphasic aura, change in aura pattern, first aura over 50, exertional
  or thunderclap onset, side-locked aura; required where the case turns on an infarct, a
  stroke-like lesion, an aneurysm or a seizure (P01, P03, P07, P08, P09, RM11). MRI is preferred to
  CT. Typical-aura S cases have no imaging criterion.
- Vessel imaging is a separate study, never text inside a brain MRI report:
  `order_advanced_imaging` `MR_angiography` (required P03, P07, P09; recommended M03, M07, P01,
  P02, RS11) and `MR_venography` (required RM11: cortical oedema and seizure on a combined pill).

**Staging and confirmatory studies, case by case:** labs (ESR/CRP in a first aura over 50;
antiphospholipid panel only in an infarct work-up; lactate and CK when MELAS is in question),
EEG only for a witnessed seizure (RM11), cardiac monitoring and echocardiography only in an infarct
or AF work-up (P02, P03, P05, P07) or MELAS cardiomyopathy screening (P08 TTE and ECG), MR
spectroscopy (P08), genetic tests (NOTCH3 in P04 and P06, m.3243A>G in P08), neuropsychology (P06).

**Pre-treatment safety:** `check_drug_interactions` with `{"drug": ...}` alternatives. Required
only when a concrete interaction or contraindication changes management (combined hormonal
contraception in migraine with aura; triptans after stroke, in hemiplegic or brainstem aura or with
an aneurysm; rizatriptan with propranolol; anticoagulant with NSAID or paracetamol; lactation;
sertraline with a triptan where the patient asks); otherwise recommended or optional. ROUND_POLICY 6.

**Never a clinical step:** `search_medical_literature` is optional at most, takes no arguments,
comes last and is never in the stop rule (ROUND_POLICY 5). Genetic counselling, specialist
referral and hemiplegic migraine gene testing (no vocabulary term yet) are musts, not tool calls.

## 3. Tools that are typically USELESS (waste avoided actions)

- `order_ct_scan`: less sensitive than MRI; not indicated in typical aura [AHS_neuroimaging_2020]
- `analyze_csf`: only for suspected SAH, meningitis or a pressure disorder [ICHD_3]
- `analyze_eeg`: only when a seizure is in question [ICHD_3]
- `order_echocardiogram`: no routine bubble echo or PFO screening; PFO closure does not treat
  migraine ([PREMIUM_2017], [PRIMA_2016], [MIST_2008]). A PFO matters only after a cryptogenic
  stroke under 60.
- `order_cardiac_monitoring`: only when cardioembolism is in question [ICHD_3]
- `order_advanced_imaging` `MR_angiography` where no vessel question exists [AHS_neuroimaging_2020]
- MRI in typical-aura S cases: no avoided action (the stop rule of 0 already penalises it; the July
  ruling makes MRI optional for red flags, decided 24 Oct 2026)

## 4. Treatment statements (musts and prohibitions; no treatment tool)

- **Acute:** NSAID or aspirin with an antiemetic; a triptan at headache onset, not during the aura
  (a dose in the aura is ineffective, not harmful) [AHS_2021] [NICE_CG150].
- **Triptans contraindicated** after stroke or TIA (including an imaging-proven infarct), in
  ischaemic heart disease, peripheral vascular disease and uncontrolled hypertension; avoided by
  label in hemiplegic migraine and migraine with brainstem aura (NSAID plus antiemetic instead).
  CADASIL: no evidence contraindicates them, but vasoconstrictive drugs are not first-line acute
  treatment (VASCERN CADASIL recommendations 2023). Rizatriptan 5 mg with propranolol; sumatriptan
  needs no adjustment. Triptan with SSRI or SNRI: allowed with counselling, the serotonin syndrome
  risk is low [AHS_triptan_SSRI_2010]. Ergots never within 24 h of a triptan.
- **Preventive** (AHS 2021 thresholds): offer at 6 or more monthly headache days, 4 or more with
  some disability, or 3 or more with severe disability; consider at 4-5 days, 3 with some or 2 with
  severe disability, and for prolonged, frequent, hemiplegic or brainstem aura or after migrainous
  infarction [AHS_2021]. Oral agents by evidence grade [Silberstein_2012] (propranolol, topiramate,
  candesartan off label, amitriptyline); NSAIDs, magnesium and riboflavin [Holland_2012] only for
  those. CGRP monoclonal antibodies: a first-line option in the EHF 2022 update [Sacco_2022]; NICE
  funding requires at least 4 migraine days a month and at least 3 failed preventives (NICE TA659,
  TA682, TA764). A single attack or about one attack a month without disability: diary, no
  preventive.
- **Topiramate and valproate:** topiramate only within the pregnancy prevention programme with
  highly effective contraception (IUD or implant; topiramate reduces the efficacy of oral and
  progestogen-only pills) [MHRA_topiramate_2024]; valproate never for migraine prevention in a
  woman who can become pregnant. Candesartan only with reliable contraception.
- **Hormonal contraception:** combined methods (pill, patch, ring) are UKMEC category 4 in migraine
  with aura at any age, and category 4 under 6 weeks postpartum while breastfeeding; progestogen-only
  pill, implant, injectable and LNG-IUD are UKMEC 2; copper IUD UKMEC 1. After stroke: copper IUD 1,
  LNG-IUD 2, POP and implant 2 to start and 3 to continue, DMPA 3, CHC 4 [UKMEC_2025]. Write
  "UKMEC category 4", never "category 3-4". Consensus on stroke risk: [Sacco_2017].
- **HRT:** migraine with aura is not a contraindication; prefer transdermal oestradiol at the lowest
  effective dose with micronised progesterone or an LNG-IUS, and review if the aura changes
  [NICE_NG23]. Never prohibit HRT for the aura alone.
- **Antithrombotics:** none for presumed TIA when the episodes have the features of aura and imaging
  shows no infarct. After stroke: single antiplatelet long term, DAPT only in the short window after
  a minor stroke [AHA_ASA_2021_secondary]; AF: anticoagulate by CHA2DS2-VA, not indicated at 0
  [ESC_AF_2024]; alcohol reduction reduces AF recurrence [Voskoboinik_2020].
- **Unruptured aneurysm:** BP control, smoking cessation, neurovascular referral; screening only
  with two or more affected first-degree relatives [AHA_UIA_2015].
- **CADASIL, MELAS:** genetic counselling for relatives (before testing in an unaffected person at
  risk) [EAN_CADASIL_2020]; MELAS care per [MMS_2017] (cardiac, hearing and diabetes screening;
  valproate contraindicated; L-arginine in stroke-like episodes is consensus with low evidence).

## 5. Sequence constraints (all soft)

- Structured history before brain MRI in every case with an MRI criterion.
- Brain MRI before vessel imaging where both are criteria (P03, P07, P09, RM11).
- Brain MRI before echo and cardiac monitoring (P02 loop recorder, P03, P07).
- Brain MRI before genetic testing (P04, P06, P08).
- No constraint involves the literature or drug criteria. No hard constraint in this condition.
- Stop rule: the required criteria only; `max_additional_actions` 0 in S cases, 1 elsewhere.

## 6. Subtype variations

- **S (standard):** typical aura, normal examination; history plus acute and contraceptive plan,
  no imaging.
- **M (moderate):** one red flag or management issue (first attack, motor or brainstem aura,
  prolonged aura, combined pill, SSRI); MRI recommended, vessel imaging where the flag is vascular.
- **P (puzzle):** late-onset aura versus TIA, AF or anticoagulation, migrainous infarction, CADASIL,
  MELAS, aneurysm. Mimic cases (P06 CADASIL, P07 cardioembolic stroke, P08 MELAS) carry the mimic's
  own label and code and stay in this condition (decided 24 Oct 2026, as in ALS-P02).
- **R (reverse / rare):** hemiplegic migraine, migralepsy.

## 7. Red herrings and pitfalls

- First aura in an older adult: exclude TIA and stroke; a typical march does not prove migraine.
- Aura without headache: possible (1.2.1.2) but exclude TIA, especially over 50.
- Non-specific white matter hyperintensities are common in migraine; the CADASIL pattern is
  anterior temporal pole and external capsule involvement.
- A small PFO is common and is not the mechanism when AF is documented.
- Template errors to avoid: vessel findings inside brain MRI reports; combined-pill or ergot
  prohibitions where the patient takes neither; HRT prohibited for aura; "category 3-4";
  "1.4.1" for migrainous infarction; triptan advice for the aura phase.

## 8. Allowed citations

Every key cited in a MIG-AURA case must be here. References checked 24 Oct 2026.

- `[ICHD_3]`: Headache Classification Committee of the International Headache Society. The International Classification of Headache Disorders, 3rd edition. Cephalalgia 2018;38(1):1-211. doi 10.1177/0333102417738202
- `[AHS_neuroimaging_2020]`: Evans RW, Burch RC, Frishberg BM, et al. Neuroimaging for migraine: the American Headache Society systematic review and evidence-based guideline. Headache 2020;60(2):318-336. doi 10.1111/head.13720
- `[AHS_2021]`: Ailani J, Burch RC, Robbins MS; Board of Directors of the American Headache Society. The American Headache Society Consensus Statement: update on integrating new migraine treatments into clinical practice. Headache 2021;61(7):1021-1039. doi 10.1111/head.14153
- `[Silberstein_2012]`: Silberstein SD, Holland S, Freitag F, et al. Evidence-based guideline update: pharmacologic treatment for episodic migraine prevention in adults. Neurology 2012;78(17):1337-1345 (erratum 2013 on pindolol, clonidine and nicardipine levels)
- `[Holland_2012]`: Holland S, Silberstein SD, Freitag F, et al. Evidence-based guideline update: NSAIDs and other complementary treatments for episodic migraine prevention in adults. Neurology 2012;78(17):1346-1353. Cite only for NSAIDs, magnesium, riboflavin and other complementary treatments
- `[Sacco_2022]`: Sacco S, Amin FM, Ashina M, et al. European Headache Federation guideline on the use of monoclonal antibodies targeting the calcitonin gene related peptide pathway for migraine prevention: 2022 update. J Headache Pain 2022;23:67. doi 10.1186/s10194-022-01431-x. CGRP antibodies only (first-line option); not the NICE funding criteria
- `[Sacco_2017]`: Sacco S, Merki-Feld GS, Ægidius KL, et al. Hormonal contraceptives and risk of ischemic stroke in women with migraine: a consensus statement from the European Headache Federation (EHF) and the European Society of Contraception and Reproductive Health (ESC). J Headache Pain 2017;18:108. doi 10.1186/s10194-017-0815-1
- `[UKMEC_2025]`: College of Sexual and Reproductive Healthcare. UK Medical Eligibility Criteria for Contraceptive Use (UKMEC 2025). BMJ Sex Reprod Health 2026;52:1-138. doi 10.1136/bmjsrh-2026-UKMEC. Supersedes UKMEC 2016; the migraine, stroke and postpartum categories above are unchanged
- `[NICE_CG150]`: National Institute for Health and Care Excellence. Headaches in over 12s: diagnosis and management. Clinical guideline CG150, 2012, last updated 2021
- `[NICE_NG23]`: National Institute for Health and Care Excellence. Menopause: identification and management. NICE guideline NG23, 2015, updated 2024
- `[MHRA_topiramate_2024]`: Medicines and Healthcare products Regulatory Agency. Topiramate (Topamax): introduction of new safety measures, including a Pregnancy Prevention Programme. Drug Safety Update 2024;17(11), 20 June 2024
- `[AHS_triptan_SSRI_2010]`: Evans RW, Tepper SJ, Shapiro RE, Sun-Edelstein C, Tietjen GE. The FDA alert on serotonin syndrome with use of triptans combined with selective serotonin reuptake inhibitors or selective serotonin-norepinephrine reuptake inhibitors: American Headache Society position paper. Headache 2010;50(6):1089-1099. doi 10.1111/j.1526-4610.2010.01691.x
- `[EHF_EAN_2021]`: Eigenbrodt AK, Ashina H, Khan S, et al. Diagnosis and management of migraine in ten steps. Nat Rev Neurol 2021;17(8):501-514. doi 10.1038/s41582-021-00509-5 (EHF and EAN endorsed consensus; general diagnosis and management, not a cardiovascular statement)
- `[PREMIUM_2017]`: Tobis JM, Charles A, Silberstein SD, et al. Percutaneous closure of patent foramen ovale in patients with migraine: the PREMIUM trial. J Am Coll Cardiol 2017;70(22):2766-2774
- `[PRIMA_2016]`: Mattle HP, Evers S, Hildick-Smith D, et al. Percutaneous closure of patent foramen ovale in migraine with aura, a randomized controlled trial. Eur Heart J 2016;37(26):2029-2036
- `[MIST_2008]`: Dowson A, Mullen MJ, Peatfield R, et al. Migraine Intervention With STARFlex Technology (MIST) trial. Circulation 2008;117(11):1397-1404
- `[ESC_AF_2024]`: Van Gelder IC, Rienstra M, Bunting KV, et al. 2024 ESC Guidelines for the management of atrial fibrillation developed in collaboration with EACTS. Eur Heart J 2024;45(36):3314-3414 (CHA2DS2-VA)
- `[Voskoboinik_2020]`: Voskoboinik A, Kalman JM, De Silva A, et al. Alcohol abstinence in drinkers with atrial fibrillation. N Engl J Med 2020;382(1):20-28. doi 10.1056/NEJMoa1817591
- `[AHA_ASA_2021_secondary]`: Kleindorfer DO, Towfighi A, Chaturvedi S, et al. 2021 Guideline for the prevention of stroke in patients with stroke and transient ischemic attack. Stroke 2021;52(7):e364-e467
- `[AHA_UIA_2015]`: Thompson BG, Brown RD Jr, Amin-Hanjani S, et al. Guidelines for the management of patients with unruptured intracranial aneurysms. Stroke 2015;46(8):2368-2400. doi 10.1161/STR.0000000000000070
- `[EAN_CADASIL_2020]`: Mancuso M, Arnold M, Bersano A, et al. Monogenic cerebral small-vessel diseases: diagnosis and therapy. Consensus recommendations of the European Academy of Neurology. Eur J Neurol 2020;27(6):909-927. doi 10.1111/ene.14183 (its migraine-treatment wording could not be checked; cite the VASCERN 2023 recommendations for triptans)
- `[MMS_2017]`: Parikh S, Goldstein A, Karaa A, et al. Patient care standards for primary mitochondrial disease: a consensus statement from the Mitochondrial Medicine Society. Genet Med 2017;19(12). doi 10.1038/gim.2017.107
- `[Charles_2017]`: Charles A. The pathophysiology of migraine: implications for clinical management. Lancet Neurol 2018;17(2):174-182 (online November 2017). Pathophysiology only; never for PFO, HRT or drugs

Named in case text without a key (cite by author and journal): VASCERN, Do's and Don'ts CADASIL
(ERN Rare Vascular Diseases, April 2023); NICE TA659 (galcanezumab), TA682 (erenumab), TA764
(fremanezumab); LactMed (NIH) for lactation; CRYSTAL AF (Sanna T et al., N Engl J Med 2014);
PHASES (Greving JP et al., Lancet Neurol 2014); MELAS stroke-like episodes (Ng YS et al., Wellcome
Open Res 2019); WHO MEC 5th edition 2015 (a 6th edition was published in November 2025; its
migraine categories were not checked, so UKMEC 2025 governs).

**Superseded (do not cite; kept for traceability):**
- `[AAN_2000]`: Silberstein SD; Quality Standards Subcommittee of the AAN. Practice parameter: evidence-based guidelines for migraine headache (an evidence-based review). Neurology 2000;55(6):754-762. It covers acute and preventive treatment, not neuroimaging (the US Headache Consortium imaging guideline was separate). Replaced on 24 Oct 2026 in all cases by [AHS_neuroimaging_2020] for imaging and CT/MRA waste, by [ICHD_3] for CSF, EEG, echo, monitoring and OCT waste, and by [AHS_2021] / [Silberstein_2012] for treatment
- `[UKMEC_2016]`: FSRH. UK Medical Eligibility Criteria for Contraceptive Use, 2016 (amended September 2019). Superseded by [UKMEC_2025]
- `[WHO_MEC_2015]`: WHO. Medical eligibility criteria for contraceptive use, 5th edition, 2015. Superseded by the 6th edition (2025); named in text only
