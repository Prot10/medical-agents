# Criteria pack: Focal epilepsy, temporal lobe

**ICD-10-CM:** G40.209 (localization-related symptomatic epilepsy with complex partial seizures, not
intractable) by default; G40.219 (intractable) ONLY when two appropriately chosen, tolerated and
adequately dosed ASM schedules have failed [Kwan_2010] (non-adherence and subtherapeutic dosing do
not qualify; in the round: P04, RP04, RS01, RS04). Never the idiopathic G40.0 codes: every case is
structural or of unknown cause. Mimic cases keep the code of what they are: P02 G04.81 (anti-LGI1
encephalitis), P03 F44.5 (functional seizures in a patient with controlled mesial TLE), RP01 B00.4
(HSV-1 encephalitis with acute symptomatic NCSE). ICD-10-CM has no G41 category: status epilepticus
is coded inside G40 (G40.901 when unspecified).
**Condition enum:** `NeurologicalCondition.FOCAL_EPILEPSY_TEMPORAL` (`focal_epilepsy_temporal`)
**Case ID prefix:** `FEPI-TEMP`

Revised 24 October 2026 (close-out of the October 2026 review round, `data/review/round-2026-10/
plans/FEPI-TEMP.md` sections 1 to 3 and `FEPI-TEMP-decisions.md`). The statements below are the
plan's canonical facts; cite the key given, never a source outside section 9.

---

## 1. Diagnostic criteria

- **Epilepsy** [ILAE_def_2014]: two unprovoked seizures more than 24 h apart, or one unprovoked
  seizure with a recurrence risk of at least 60%, or an epilepsy syndrome. Stereotyped focal aware or
  impaired-awareness seizures before a first convulsion are prior seizures: the two-seizure criterion
  is met and the single-seizure rule is not needed.
- **Acute symptomatic seizures** (during an acute encephalitis, metabolic or toxic insult) are not
  epilepsy [ILAE_ASS_2010]; RP01 is that case.
- **Classification** [ILAE_2017]: focal onset with or without impaired awareness, focal to bilateral
  tonic-clonic. The 2025 ILAE update [ILAE_2025] keeps the structure and renames awareness as
  consciousness; the cases keep the 2017 wording, which every reader still understands.
- **Mesial TLE**: epigastric rising, deja vu, fear, olfactory aura, oral and manual automatisms;
  **lateral (neocortical) TLE**: auditory or vertiginous aura (RM04).
- **Hippocampal sclerosis on MRI** [ILAE_MRI_2019, ILAE_HS_2013]: hippocampal atrophy, T2/FLAIR
  hyperintensity, loss of internal architecture, often temporal horn enlargement. "Borderline volume,
  below HS threshold" is not HS.
- **Dual pathology** is HS plus a separate lesion outside the hippocampus (tumor, malformation, FCD
  type II, scar, tuber). HS with an associated temporal cortical abnormality is FCD type IIIa, a
  histological diagnosis; on MRI write "temporopolar gray-white blurring associated with HS, possibly
  FCD type IIIa" [ILAE_FCD_2011] (RP04).
- **Tumors without tissue** are named as presumed (RM04: "low-grade epilepsy-associated tumor,
  presumed ganglioglioma, CNS WHO grade 1"); WHO 2021 grades are arabic.
- **Lateralization** [Lateralization_2005]: unilateral manual automatisms are usually ipsilateral;
  dystonic limb posturing, late forced head version and Todd paresis are contralateral; postictal
  aphasia means the language-dominant hemisphere; oral automatisms and tongue-bite side do not
  lateralize. In a left-handed patient write "probably language-dominant" unless dominance was
  tested. Localization rests on EEG and MRI concordance.
- **Mimics with their own diagnosis**: anti-LGI1 encephalitis [Graus_2016, Irani_2011]
  (faciobrachial dystonic seizures, memory decline, hyponatremia; antibodies more often in serum than
  CSF; FBDS often lack an EEG correlate and respond to immunotherapy more than to ASMs; tumors under
  10%, thymoma: chest CT); HSV encephalitis [IDSA_enc_2008, ABN_enc_2012] (lymphocytic pleocytosis,
  raised protein, often red cells; acellular early or when immunosuppressed); functional seizures
  with epilepsy [ILAE_PNES_2013] (habitual events on video-EEG without ictal correlate).

## 2. Work-up hierarchy (as applied in the 30 cases, 24 Oct 2026)

**Imaging.**
- `analyze_brain_mri` `{protocol: epilepsy}` **required** in 26 cases: the first MRI is the
  dedicated study (3D T1 and 3D FLAIR about 1 mm, coronal T2 perpendicular to the hippocampus; 3T
  when available) [ILAE_MRI_2019]. It shows the labelled lesion with definite findings; an outside
  standard MRI belongs in the history only.
- Exceptions: RP01 and RP03 `{contrast: true}` (encephalitis after cancer treatment, a growing
  metastasis); P02 `{}` (any MRI answers the encephalitis question); RS02 at 33 weeks, non-contrast
  epilepsy protocol, with gadolinium a `harmful` avoided action [ACOG_imaging_2017, Ray_2016]; P04
  no MRI criterion (`panel_required_exemptions`: normal earlier 1.5T epilepsy-protocol MRI, 3T not
  tolerated, anesthesia declined).
- Gadolinium is not routine: added only when a tumor, vascular malformation, infection or
  inflammation is suspected (reports: "Post-contrast T1 sequences were added by the reviewing
  radiologist because a lesion was seen"). No gadolinium line in HS, FCD or MRI-negative reports.
- `order_ct_scan`: CT only when MRI is unavailable or contraindicated, or in an emergency (head
  injury, persistent deficit, no return to baseline, anticoagulation, shunt, cancer). Required in
  RM03 (fall with head injury, GCS 8; soft CT -> MRI), recommended in RM01 (VP shunt) and RP05
  (skull-base defect, bone windows), optional in P04. Waste elsewhere (21 cases).

**EEG** [IFCN_ILAE_EEG_2023]: routine awake EEG with drowsiness or sleep first; if non-diagnostic,
sleep-deprived, then ambulatory or video for event capture. One routine EEG shows interictal
discharges in roughly 30 to 50% of adults with epilepsy; a normal EEG does not exclude epilepsy.
- Routine: required in 23, optional in RP01.
- Sleep-deprived: recommended in 5 (M01, M02, M03, RM01, RP02), only after a non-diagnostic or
  equivocal routine EEG.
- Ambulatory: recommended in M03, required in RP02 (captures the events that make the diagnosis).
- Video-EEG: required only for event capture against panic or PNES (P01, P03), seizure versus
  syncope (P05), the LGI1 encephalitis (P02) and presurgical evaluation of drug-resistant epilepsy
  (P04, RP04, RS01, RS04); recommended in M05 and RP05.
- Continuous ICU EEG: only for suspected NCSE or unexplained encephalopathy; required in RP01
  [ACNS_2021, Salzburg_2015].
- Frequency words follow ACNS 2021: frequent at least 1 per minute, occasional at least 1 per hour,
  rare under 1 per hour. Sharp waves last 70 to 200 ms, spikes 20 to 70 ms.

**Laboratory studies** (Reviewer 1, July 2026: optional unless clinically indicated):
- Required only where the result is the case question: P02 (serum LGI1 antibodies and sodium; the
  antibody result is a follow-up served only to an order naming the panel), RM03 (phenytoin level,
  glucose, CK, lactate after a prolonged convulsion with head injury), RS02 (eclampsia screen at 33
  weeks: urine protein/creatinine, platelets, creatinine, liver enzymes; levetiracetam level).
- Recommended with a named indication (7): an ASM level after a breakthrough seizure (RM02, RP02,
  RP03, RP04, RS03), renal function before acyclovir (RP01), glucose on metformin (RS05).
- Optional in 15 first presentations without a provoking clue; none in 5 cases.
- **Prolactin** is not a routine test [AAN_prolactin_2005]: drawn 10 to 20 minutes after a suspected
  tonic-clonic or focal impaired-awareness seizure it helps against PNES; it does not separate seizure
  from syncope, and a level drawn hours later or after an aura has no value. Only P05 stores one
  (22 minutes after a witnessed convulsion).

**ECG** (Reviewer 1: optional): optional in the 19 cases that store one, required only in P05
(seizure versus syncope [ESC_syncope_2018]), recommended in RP02 (pulmonary embolism); none in the
9 established or tertiary cases [NICE_NG217_2025].

**CSF** (`analyze_csf`): required in P02 and RP01, recommended in RP03, always after imaging (hard
MRI -> CSF); waste elsewhere (26 cases).

**Presurgical studies** [Engel_2003, Willmann_2007]:
- `order_advanced_imaging` `{modality: FDG_PET}`: required in P04 (MRI-negative drug-resistant
  TLE); optional in M04, P01, P02, RP04, RP05, RS01, RS04. Waste in 18 first diagnoses or acute
  illnesses with a concordant MRI and EEG; `harmful` in pregnancy (RS02).
- `order_specialized_test` `{test_type: neuropsych_battery}`: recommended in presurgical
  drug-resistant cases (P04, RP04, RS04), optional in M05, P01, RP05.

**Other specific tests:** `order_body_imaging` `{study: chest_CTA}` required in RP02 (concurrent
pulmonary embolism) [ESC_PE_2019]; `{study: chest_CT}` recommended in P02 (thymoma screening).

**Knowledge tools** (round rulings 5 and 6):
- `check_drug_interactions`: required only for a documented interaction that changes the ASM choice
  or dose (7: combined hormonal contraception P04, RM02, S02, S04; anticoagulation RP02; inducer
  polytherapy RP04, RS04); recommended where a comedication matters only if an inducer or a specific
  agent is chosen (7: P02, P05, RM03, RM04, RP01, RP03, RS03); optional otherwise (16). It comes after
  the MRI and EEG.
- `search_medical_literature`: optional in all 30 and last. Every case carries the same neutral
  initial literature block (definition, classification, HARNESS-MRI, NICE first-line ASM, Kwan
  2010); lesion-specific follow-ups answer only a query that already names the lesion.

**Stop rule:** `required_before_assessment` lists exactly the required criteria;
`max_additional_actions` 1 for S cases, 2 otherwise.

## 3. Tools that are typically USELESS (waste avoided actions, case-specific rationales)

- `order_echocardiogram` (27 cases) and `order_cardiac_monitoring` (28): Reviewer 1 asked for their
  removal; no case orders them. P05 already had a normal cardiac work-up.
- `analyze_csf` without encephalitis, immunosuppression or cancer (26).
- `order_ct_scan` when MRI is available and no emergency criterion applies (21).
- `order_advanced_imaging` FDG-PET outside presurgical evaluation (18; harmful in RS02).

## 4. Harmful or contraindicated management (prohibitions, not tool calls)

- Valproate is not first-line for focal epilepsy; MHRA 2024 [MHRA_VPA_2024]: not started under 55
  unless two specialists document that nothing else works or is tolerated, and in women of
  childbearing potential only within a pregnancy prevention programme. Topiramate [MHRA_TPM_2024]:
  pregnancy prevention programme; avoid in pregnancy for epilepsy unless no alternative.
- Enzyme-inducing ASMs (carbamazepine, phenytoin, phenobarbital; oxcarbazepine and topiramate above
  200 mg/day weaker) with DOACs or warfarin [EHRA_DOAC_2021], chemotherapy, dexamethasone, statins,
  SSRIs or lamotrigine; with a tumor or planned oncologic therapy prefer a non-inducing ASM (the old
  "tumor -> consider carbamazepine" was wrong).
- Carbamazepine or oxcarbazepine (and phenytoin) without HLA-B*15:02 testing in a patient of East,
  Southeast or South Asian ancestry who never took them [CPIC_2018] (M02, M04, M05, P04, RS05, S04,
  S06; long-term users without reaction need no test). No HLA term exists: must or prohibition only.
- Albendazole or praziquantel for calcified neurocysticercosis, and any antiparasitic drug in
  pregnancy [IDSA_NCC_2018].
- Gadolinium in pregnancy unless it changes outcome [ACOG_imaging_2017, Ray_2016]; no FDG-PET in
  pregnancy.
- Lumbar puncture before imaging has excluded mass effect (P02, RP01, RP03), or in a shunted patient
  for routine seizure work-up (RM01).
- Benzodiazepine escalation for functional seizures (P03) [ILAE_PNES_2013].
- Treating ictal fear as panic disorder (P01).

## 5. Sequence constraints

- Hard: `MRI -> CSF` in P02, RP01, RP03 ("Exclude mass effect on imaging before lumbar puncture").
- Soft: `MRI -> drug check` only where the drug check is required or recommended ("Know the
  structural cause before finalizing the ASM and its interactions (a tumor or planned oncologic
  therapy favors non-inducing ASMs)"), cited [NICE_NG217_2025] (P02 [Graus_2016], RP01
  [IDSA_enc_2008]); RM03 soft `CT -> MRI` after the head injury.
- No constraint with literature, with an optional criterion, or that orders two EEG types.

## 6. Subtype variations

- **M (mild):** a first or early diagnosis with a dedicated MRI that shows the lesion; staged EEG.
- **S (standard):** first convulsion after months of unrecognized auras (two-seizure criterion met),
  mesial TLE with HS or a low-grade tumor; MRI and routine EEG suffice.
- **P (progressive / refractory or mimic):** drug-resistant epilepsy (P04: video-EEG, FDG-PET,
  neuropsychology, surgical evaluation), misdiagnosed epilepsy (P01, panic disorder), and mimics with
  their own label (P02 LGI1 encephalitis, P03 functional seizures with controlled MTLE, P05 seizure
  versus syncope).
- **R (record-derived):** RM, RP and RS cases seeded from open-access case reports: dual pathology
  (TSC, ECCL, hypothalamic hamartoma, neurocysticercosis, neonatal meningitis), pregnancy and
  postpartum, drug resistance, acute symptomatic NCSE (RP01), concurrent pulmonary embolism (RP02),
  metastasis on checkpoint inhibitors (RP03), temporal encephalocele (RP05).

## 7. Common red-herring categories and pitfalls

- **Single seizure does not equal epilepsy**, but prior stereotyped auras are prior seizures.
- **Normal MRI** does not exclude TLE when it was not an epilepsy-protocol study; MRI-negative TLE is
  a substantial minority of drug-resistant TLE (P04, RP02).
- **Normal interictal EEG** does not exclude epilepsy; benign variants (wicket spikes, small sharp
  spikes) are not epileptiform.
- **Prolactin**: see section 2; never "supports a convulsion" without the 10 to 20 minute timing,
  never against syncope.
- **Postictal Todd paresis** mimics stroke and is contralateral to the focus.
- **A seizure after 20 weeks of pregnancy or postpartum is eclampsia until proven otherwise**
  [ACOG_HTN_2020]; lamotrigine and levetiracetam clearance rise in pregnancy (monitor levels, raise
  the dose, reduce it after delivery) [AAN_WWE_2009].
- **Ethinylestradiol roughly halves lamotrigine** (levels rise in the pill-free week) [Sabers_2003];
  carbamazepine, oxcarbazepine, phenytoin, phenobarbital and topiramate above 200 mg/day reduce
  hormonal contraceptive efficacy; levetiracetam, lacosamide and lamotrigine do not.
- **Glauser 2013 evidence levels** [ILAE_drug_2013]: Level A for adults with focal seizures:
  carbamazepine, levetiracetam, phenytoin, zonisamide; lamotrigine and gabapentin Level A only in the
  elderly. Never "lamotrigine Level A" or "oxcarbazepine Level A" in an adult under 60 (guarded by
  `test_case_guards.py` banned strings).

## 8. Musts (canonical)

- First-line ASM [NICE_NG217_2025, SANAD2_2021]: "Start <lamotrigine or levetiracetam> as first-line
  monotherapy for focal epilepsy, chosen for <case reason>." (lamotrigine was superior in SANAD II;
  carbamazepine, oxcarbazepine, zonisamide, lacosamide are further options).
- Valproate prohibition in patients under 55 (section 4); women of childbearing potential: "Discuss
  contraception and pregnancy plans before choosing the ASM; start folic acid." [EURAP_2018]
- HLA-B*15:02 before carbamazepine or oxcarbazepine where section 4 applies.
- Driving: "Advise no driving until the locally applicable seizure-free interval is met and explain
  the duty to inform the licensing authority." (FAA medical certification for a US pilot, RP02).
- SUDEP [AAN_SUDEP_2017]: counsel every patient with focal to bilateral tonic-clonic seizures or drug
  resistance.
- Drug resistance (P04, RP04, RS01, RS04): referral to a comprehensive epilepsy center for presurgical
  evaluation [Kwan_2010, Engel_2003, Wiebe_2001, ERSET_2012]; lesional epilepsy amenable to surgery
  (M04, M05, RM04, RP05, S02, S03, S06): surgical evaluation of the lesion without "drug-resistant".
- Process steps already scored by a criterion (order MRI, EEG, PET, neuropsychology) are never musts.

## 9. Allowed citations

Every key the 30 cases cite is listed here with its verified reference (checked 24 Oct 2026).

- `[ILAE_def_2014]`: Fisher RS, Acevedo C, Arzimanoglou A, et al. ILAE official report: a practical
  clinical definition of epilepsy. Epilepsia 2014;55(4):475-482
- `[ILAE_2017]`: Fisher RS, Cross JH, French JA, et al. Operational classification of seizure types
  by the International League Against Epilepsy. Epilepsia 2017;58(4):522-530; Scheffer IE, Berkovic
  S, Capovilla G, et al. ILAE classification of the epilepsies. Epilepsia 2017;58(4):512-521. The
  seizure-type part is updated by `[ILAE_2025]`; the epilepsy classification is current
- `[ILAE_2025]`: Beniczky S, Trinka E, Wirrell E, et al. Updated classification of epileptic
  seizures: position paper of the International League Against Epilepsy. Epilepsia 2025, doi
  10.1111/epi.18338 (four classes kept; awareness becomes consciousness)
- `[ILAE_ASS_2010]`: Beghi E, Carpio A, Forsgren L, et al. Recommendation for a definition of acute
  symptomatic seizure. Epilepsia 2010;51(4):671-675
- `[NICE_NG217_2025]`: NICE guideline NG217. Epilepsies in children, young people and adults.
  Published April 2022, valproate and topiramate recommendations updated January 2025
- `[AAN_2007]`: Krumholz A, Wiebe S, Gronseth G, et al. Practice parameter: evaluating an apparent
  unprovoked first seizure in adults (an evidence-based review). Neurology 2007;69(21):1996-2007
- `[AAN_2015]`: Krumholz A, Wiebe S, Gronseth GS, et al. Evidence-based guideline: management of an
  unprovoked first seizure in adults. Neurology 2015;84(16):1705-1713
- `[ILAE_MRI_2019]`: Bernasconi A, Cendes F, Theodore WH, et al. Recommendations for the use of
  structural magnetic resonance imaging in the care of patients with epilepsy: a consensus report from
  the ILAE Neuroimaging Task Force. Epilepsia 2019;60(6):1054-1068 (HARNESS-MRI)
- `[IFCN_ILAE_EEG_2023]`: Peltola ME, Leitinger M, Halford JJ, et al. Routine and sleep EEG: minimum
  recording standards of the IFCN and the ILAE. Epilepsia 2023;64(3):602-618; Tatum WO, Rubboli G,
  Kaplan PW, et al. Clinical utility of EEG in diagnosing and monitoring epilepsy in adults. Clin
  Neurophysiol 2018;129(5):1056-1082
- `[ACNS_2021]`: Hirsch LJ, Fong MWK, Leitinger M, et al. American Clinical Neurophysiology Society's
  standardized critical care EEG terminology: 2021 version. J Clin Neurophysiol 2021;38(1):1-29
- `[Salzburg_2015]`: Leitinger M, Beniczky S, Rohracher A, et al. Salzburg consensus criteria for
  non-convulsive status epilepticus: approach to clinical application. Epilepsy Behav
  2015;49:158-163
- `[SANAD2_2021]`: Marson A, Burnside G, Appleton R, et al. The SANAD II study of the effectiveness
  and cost-effectiveness of levetiracetam, zonisamide, or lamotrigine for newly diagnosed focal
  epilepsy: an open-label, non-inferiority, multicentre, phase 4, randomised controlled trial. Lancet
  2021;397(10282):1363-1374
- `[ILAE_drug_2013]`: Glauser T, Ben-Menachem E, Bourgeois B, et al. Updated ILAE evidence review of
  antiepileptic drug efficacy and effectiveness as initial monotherapy for epileptic seizures and
  syndromes. Epilepsia 2013;54(3):551-563
- `[Kwan_2010]`: Kwan P, Arzimanoglou A, Berg AT, et al. Definition of drug resistant epilepsy:
  consensus proposal by the ad hoc Task Force of the ILAE Commission on Therapeutic Strategies.
  Epilepsia 2010;51(6):1069-1077
- `[Engel_2003]`: Engel J Jr, Wiebe S, French J, et al. Practice parameter: temporal lobe and
  localized neocortical resections for epilepsy. Neurology 2003;60(4):538-547
- `[Wiebe_2001]`: Wiebe S, Blume WT, Girvin JP, Eliasziw M. A randomized, controlled trial of surgery
  for temporal-lobe epilepsy. N Engl J Med 2001;345(5):311-318
- `[ERSET_2012]`: Engel J Jr, McDermott MP, Wiebe S, et al. Early surgical therapy for drug-resistant
  temporal lobe epilepsy: a randomized trial. JAMA 2012;307(9):922-930
- `[Willmann_2007]`: Willmann O, Wennberg R, May T, Woermann FG, Pohlmann-Eden B. The contribution of
  18F-FDG PET in preoperative epilepsy surgery evaluation for patients with temporal lobe epilepsy: a
  meta-analysis. Seizure 2007;16(6):509-520
- `[AAN_prolactin_2005]`: Chen DK, So YT, Fisher RS. Use of serum prolactin in diagnosing epileptic
  seizures: report of the Therapeutics and Technology Assessment Subcommittee of the AAN. Neurology
  2005;65(5):668-675
- `[Lateralization_2005]`: Loddenkemper T, Kotagal P. Lateralizing signs during seizures in focal
  epilepsy. Epilepsy Behav 2005;7(1):1-17
- `[ILAE_HS_2013]`: Blumcke I, Thom M, Aronica E, et al. International consensus classification of
  hippocampal sclerosis in temporal lobe epilepsy: a Task Force report from the ILAE Commission on
  Diagnostic Methods. Epilepsia 2013;54(7):1315-1329
- `[ILAE_FCD_2011]`: Blumcke I, Thom M, Aronica E, et al. The clinicopathologic spectrum of focal
  cortical dysplasias: a consensus classification proposed by an ad hoc Task Force of the ILAE
  Diagnostic Methods Commission. Epilepsia 2011;52(1):158-174 (updated by Najm I, Lal D, Alonso
  Vanegas M, et al. Epilepsia 2022;63(8):1899-1919; types I to III, IIIa included, unchanged)
- `[Blumcke_2017]`: Blumcke I, Spreafico R, Haaker G, et al. Histopathological findings in brain
  tissue obtained during epilepsy surgery. N Engl J Med 2017;377(17):1648-1656 (epilepsy-associated
  tumors)
- `[Cavernoma_2017]`: Akers A, Al-Shahi Salman R, Awad IA, et al. Synopsis of guidelines for the
  clinical management of cerebral cavernous malformations: consensus recommendations based on
  systematic literature review by the Angioma Alliance Scientific Advisory Board Clinical Experts
  Panel. Neurosurgery 2017;80(5):665-680
- `[Encephalocele_2015]`: Saavalainen T, Jutila L, Mervaala E, et al. Temporal anteroinferior
  encephalocele: an underrecognized etiology of temporal lobe epilepsy? Neurology
  2015;85(17):1467-1474
- `[ILAE_PNES_2013]`: LaFrance WC Jr, Baker GA, Duncan R, Goldstein LH, Reuber M. Minimum
  requirements for the diagnosis of psychogenic nonepileptic seizures: a staged approach. Epilepsia
  2013;54(11):2005-2018; Goldstein LH, Robinson EJ, Mellers JDC, et al. Cognitive behavioural therapy
  for adults with dissociative seizures (CODES). Lancet Psychiatry 2020;7(6):491-505
- `[AAN_SUDEP_2017]`: Harden C, Tomson T, Gloss D, et al. Practice guideline summary: sudden
  unexpected death in epilepsy incidence rates and risk factors. Neurology 2017;88(17):1674-1680
- `[CPIC_2018]`: Phillips EJ, Sukasem C, Whirl-Carrillo M, et al. Clinical Pharmacogenetics
  Implementation Consortium guideline for HLA genotype and use of carbamazepine and oxcarbazepine:
  2017 update. Clin Pharmacol Ther 2018;103(4):574-581
- `[Sabers_2003]`: Sabers A, Ohman I, Christensen J, Tomson T. Oral contraceptives reduce lamotrigine
  plasma levels. Neurology 2003;61(4):570-571
- `[EURAP_2018]`: Tomson T, Battino D, Bonizzoni E, et al. Comparative risk of major congenital
  malformations with eight different antiepileptic drugs: a prospective cohort study of the EURAP
  registry. Lancet Neurol 2018;17(6):530-538
- `[AAN_WWE_2009]`: Harden CL, Pennell PB, Koppel BS, et al. Practice parameter update: management
  issues for women with epilepsy, focus on pregnancy: vitamin K, folic acid, blood levels, and
  breastfeeding. Neurology 2009;73(2):142-149
- `[MHRA_VPA_2024]`: MHRA Drug Safety Update. Valproate: new safety and educational materials to
  support regulatory measures in men and women under 55 years of age. January 2024
- `[MHRA_TPM_2024]`: MHRA Drug Safety Update. Topiramate: introduction of new safety measures,
  including a Pregnancy Prevention Programme. June 2024
- `[ACOG_imaging_2017]`: ACOG Committee Opinion No. 723. Guidelines for diagnostic imaging during
  pregnancy and lactation. Obstet Gynecol 2017;130(4):e210-e216
- `[Ray_2016]`: Ray JG, Vermeulen MJ, Bharatha A, Montanera WJ, Park AL. Association between MRI
  exposure during pregnancy and fetal and childhood outcomes. JAMA 2016;316(9):952-961
- `[ACOG_HTN_2020]`: ACOG Practice Bulletin No. 222. Gestational hypertension and preeclampsia. Obstet
  Gynecol 2020;135(6):e237-e260
- `[Graus_2016]`: Graus F, Titulaer MJ, Balu R, et al. A clinical approach to diagnosis of autoimmune
  encephalitis. Lancet Neurol 2016;15(4):391-404
- `[Irani_2011]`: Irani SR, Michell AW, Lang B, et al. Faciobrachial dystonic seizures precede Lgi1
  antibody limbic encephalitis. Ann Neurol 2011;69(5):892-900
- `[IDSA_enc_2008]`: Tunkel AR, Glaser CA, Bloch KC, et al. The management of encephalitis: clinical
  practice guidelines by the Infectious Diseases Society of America. Clin Infect Dis
  2008;47(3):303-327
- `[ABN_enc_2012]`: Solomon T, Michael BD, Smith PE, et al. Management of suspected viral
  encephalitis in adults: Association of British Neurologists and British Infection Association
  National Guidelines. J Infect 2012;64(4):347-373
- `[ESC_syncope_2018]`: Brignole M, Moya A, de Lange FJ, et al. 2018 ESC guidelines for the diagnosis
  and management of syncope. Eur Heart J 2018;39(21):1883-1948
- `[IDSA_NCC_2018]`: White AC Jr, Coyle CM, Rajshekhar V, et al. Diagnosis and treatment of
  neurocysticercosis: 2017 clinical practice guidelines by the IDSA and the ASTMH. Clin Infect Dis
  2018;66(8):e49-e75
- `[Garcia_2014]`: Garcia HH, Nash TE, Del Brutto OH. Clinical symptoms, diagnosis, and treatment of
  neurocysticercosis. Lancet Neurol 2014;13(12):1202-1215
- `[TSC_2021]`: Northrup H, Aronow ME, Bebin EM, et al. Updated international tuberous sclerosis
  complex diagnostic criteria and surveillance and management recommendations. Pediatr Neurol
  2021;123:50-66
- `[EXIST3_2016]`: French JA, Lawson JA, Yapici Z, et al. Adjunctive everolimus therapy for
  treatment-resistant focal-onset seizures associated with tuberous sclerosis (EXIST-3). Lancet
  2016;388(10056):2153-2163
- `[ESC_PE_2019]`: Konstantinides SV, Meyer G, Becattini C, et al. 2019 ESC guidelines for the
  diagnosis and management of acute pulmonary embolism. Eur Heart J 2020;41(4):543-603 (still the
  current ESC edition; the 2026 AHA/ACC PE guideline does not change RP02's anticoagulation)
- `[EHRA_DOAC_2021]`: Steffel J, Collins R, Antz M, et al. 2021 European Heart Rhythm Association
  practical guide on the use of non-vitamin K antagonist oral anticoagulants in patients with atrial
  fibrillation. Europace 2021;23(10):1612-1676
- `[ASCO_irAE_2021]`: Schneider BJ, Naidoo J, Santomasso BD, et al. Management of immune-related
  adverse events in patients treated with immune checkpoint inhibitor therapy: ASCO guideline update.
  J Clin Oncol 2021;39(36):4073-4126

Free-text source cited by name in one case (no key): Carne RP, O'Brien TJ, Kilpatrick CJ, et al.
MRI-negative PET-positive temporal lobe epilepsy: a distinct surgically remediable syndrome. Brain
2004;127(10):2276-2285 (P04).

**Superseded or non-existent keys (do not use):**
- `[ILAE_drug_2017]`: cited a non-existent "Glauser 2017, Epilepsia 58:1235-1268"; the review is
  `[ILAE_drug_2013]`. No case cites it.
- `[ASCO_irAE_2018]`: Brahmer JR et al. J Clin Oncol 2018;36:1714-1768, superseded by
  `[ASCO_irAE_2021]` (RP03 recited 24 Oct 2026).
