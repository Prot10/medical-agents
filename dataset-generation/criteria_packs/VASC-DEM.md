# Criteria pack: Vascular dementia (major vascular cognitive disorder)

**ICD-10-CM, per case:** F01.50 (vascular dementia, unspecified severity, without behavioural
disturbance) for every major vascular cognitive disorder, mixed cases included; F06.7 (mild
neurocognitive disorder due to a known physiological condition; F06.70 since FY2023) for mild
vascular cognitive impairment (VASC-DEM-M01); I67.850 (CADASIL) for the hereditary case
(VASC-DEM-P05). Accepted synonym codes are set in `diagnosis_synonyms.yaml` per mechanism (F01.1
multi-infarct, F01.2 and I67.3 subcortical small-vessel, I68.0 amyloid angiopathy, F00.2 mixed
Alzheimer and vascular). F01 and F06.7 never grant each other: the severity is the label.
**Condition enum:** `NeurologicalCondition.VASCULAR_DEMENTIA`
**Case ID prefix:** `VASC-DEM`

Updated 24 Oct 2026 to the October 2026 review round (`data/review/round-2026-10/plans/VASC-DEM.md`,
`VASC-DEM-summary.md`) and to the decisions on its open questions (`plans/VASC-DEM-decisions.md`).
No physician has reviewed this condition yet: every ruling below comes from the round's lead
survey, workers, verifiers, auditor and close-out.

---

> **Authored on the clinical tool review, July 2026.** Both reviewers asked for peripheral
> neuropathy to be dropped ("too broad a category"; Reviewer 1 filed the removal as an `error`
> reading `SOSTITUIRE PATOLOGIA`) and for vascular dementia to take its place, so that the four
> major dementias (AD, FTD, DLB, VaD) are all represented and the benchmark can score the
> differential among them. Five of the thirty cases resolve to mixed Alzheimer and vascular
> pathology, which is a diagnosis in its own right and not a tie-break.

## 1. Diagnostic criteria

Vascular cognitive disorder requires a cognitive syndrome and evidence that cerebrovascular disease
accounts for it [VASCOG_2014] [DSM5].

**Severity (the condition's central skill).** Mild vascular cognitive disorder (VCI without
dementia, F06.7): decline in one or more domains with preserved independence in instrumental
activities, possibly with compensatory strategies. Major vascular cognitive disorder (vascular
dementia, F01): decline sufficient to interfere with independence. The severity is the assessment's
conclusion from the history and the informant: no tool report states it, and no report may say
"the threshold for dementia is met / not met".

**Cognitive profile.** Typically executive and processing-speed predominant (slowed set-shifting,
working memory, verbal fluency) with recognition memory and cued recall relatively preserved; a
strategic infarct gives the profile of its site (amnesia from the anterior thalamus, Gerstmann
syndrome from the angular gyrus, abulia from the capsular genu).

**Vascular attribution** [VASCOG_2014] [NINDS_AIREN_1993] [AHA_ASA_2011_VCI]: a temporal relation to
a documented stroke (onset within 3 months, or stepwise steps dated to events), or a lesion pattern
sufficient to explain the deficit (multiple territorial infarcts; a strategic infarct in the
anterior or paramedian thalamus, capsular genu, caudate, angular gyrus or basal forebrain;
extensive confluent WMH with multiple lacunes; extensive haemorrhagic lesions).

**Imaging is reported in STRIVE-2 terms** [STRIVE_2]: WMH of presumed vascular origin with a
Fazekas grade, recent small subcortical infarcts, lacunes counted and located, microbleeds with
their distribution (deep: hypertensive arteriopathy; strictly lobar: amyloid angiopathy), enlarged
perivascular spaces, cortical superficial siderosis, infarcts with territory, atrophy and the MTA
score. A radiological criterion may be stated as such ("Findings fulfil Boston criteria v2.0 for
probable cerebral amyloid angiopathy"); the dementia diagnosis, sufficiency for the syndrome, the
mechanism of decline and management may not.

**Cerebral amyloid angiopathy (Boston v2.0)** [Boston_v2]: age 50 or more; two or more strictly
lobar haemorrhagic lesions (ICH, microbleeds, cSS foci, cSAH), or one lobar lesion plus one white
matter feature (severe centrum semiovale PVS, multispot WMH); no deep haemorrhagic lesion or other
cause.

**CADASIL** [Rutten_2019]: NOTCH3 cysteine-altering variant; EGFr domains 1-6 carry the more severe
phenotype. Canonical variant in VASC-DEM-P05: `NOTCH3 c.544C>T p.(Arg182Cys)`, exon 4, EGFr 4. A
non-cysteine variant of uncertain significance (P06) does not make the diagnosis.

**Mixed disease.** Coexisting Alzheimer pathology does not exclude the vascular diagnosis; where an
amyloid biomarker is positive with a significant vascular burden the diagnosis is mixed Alzheimer
and vascular dementia. A vascular-only or Alzheimer-only answer is wrong in a mixed case and is not
credited by the synonyms.

## 2. Standard workup hierarchy

Order of `action_criteria` and `followup_outputs` (the review app reads it as the work-up
sequence): cognitive screen; gait; neuropsychology; labs (young-SVD panel, MMA); MRI (CT only in
P08); mechanism studies (ECG, carotid duplex or MRA, TTE, monitoring); amyloid biomarker; FDG-PET;
NOTCH3; drug-interaction check. **No literature criterion, initial output or fallback** (ruling 5).

**Required in every case:**
- `perform_clinical_assessment` (`assessment_type: cognitive_screen`): total, domain sub-scores,
  education correction; no severity label, no "vascular pattern". The neurological exam's
  `mental_status` is a bedside observation ending "Formal cognitive screening reported separately";
  it never gives the score [VASCOG_2014]
- `interpret_labs` (`panels: [CBC, CMP, TSH, B12, folate, HbA1c, lipid_panel]`): reversible
  contributors plus the vascular risk that will be treated [AAN_MCI_2018] [AHA_ASA_2011_VCI].
  **RPR and HIV are not in the required panel** (decision Q1, Oct 2026: AAN 2001 "screening for
  syphilis ... is not justified unless clinical suspicion for neurosyphilis is present" and NICE
  NG97 do not test routinely) [AAN_dementia_2001] [NICE_NG97]; they are required only with a risk
  factor or young onset without another explanation (P06: onset before 55, past cocaine use). The
  stored labs output may still report them. Add `homocysteine`, `ESR`, `CRP`, `antiphospholipid`
  as a separate recommended criterion in young small-vessel disease (P05, P06); `MMA` (recommended)
  when B12 is about 250 pg/mL or below with metformin or neuropathy (S04) [BSH_B12_2014]. Values,
  units, ranges and flags only; `clinical_significance` null; `interpretation` recites the flagged
  values without targets or dosing. Ranges: Hb men 13.5-17.5, women 12.0-16.0 g/dL; Hct about 3 x
  Hb; HDL men >40, women >50 mg/dL; eGFR >=60 (CKD-EPI 2021); INR in a Coagulation panel; total
  cholesterol = LDL + HDL + TG/5
- `analyze_brain_mri` with `required_arguments` `{}` (never `sequences`, `protocol` or `contrast`:
  no real call can match them). The report may name its sequences (SWI or GRE is needed for
  microbleeds and cSS) [STRIVE_2]. P08 (MR-unsafe pacemaker): `order_ct_scan {}` required and MRI
  is avoided as harm

**Per case (tiers are set by the case's syndrome and mechanism):**
- Gait, `perform_clinical_assessment` (`assessment_type: gait_and_balance_timed`): required in the
  subcortical syndromes with gait involvement (M02, P07, S01-S05); recommended where the narrative
  or exam shows gait involvement (P01, P05, P06) or the test is a normal baseline (M01); absent
  otherwise. The report gives time, cadence, step length, TUG, turns, Romberg and observation, no
  diagnostic argument
- Neuropsychology, `order_specialized_test` (`test_type: neuropsych_battery`): required where the
  screen cannot settle severity or profile (M01, M02, M04, M06, P01, P02, P06, P07, P09, S09, S10),
  recommended elsewhere; domain scores and a confidence-qualified profile, never the disease or the
  dementia threshold
- ECG (`analyze_ecg {}`): for every patient with an ischaemic infarct, clinical or imaging
  (AHA 2021); required where the mechanism is embolic or AF is in question, recommended after
  lacunar, strategic or post-stroke infarcts, optional before a cholinesterase inhibitor with a
  rate-control drug (M07, M08, with an authored AF report) [AHA_ASA_2021_secondary]
- Cervical vessels (`order_advanced_imaging` `carotid_duplex` or `MR_angiography`): required in the
  multi-infarct and territorial post-stroke cases (M03, M10, P08, S06, S07, S08, S11); recommended
  after a single cortical or border-zone infarct (M04, M06) and for the posterior circulation (P09,
  S08 MRA); optional where the admission work-up covered it (M05, S09). One criterion with both
  alternatives where either answers the question (M04, M06, M10). Not after a deep hypertensive ICH
  (M09: waste).
  Reports give velocities, NASCET-equivalent percentage and plaque, no threshold statement.
  Thalamoperforating arteries (artery of Percheron) are below MRA resolution
- TTE (`order_echocardiogram`): required with a known cardiac source to characterise (M03 LV
  thrombus, M06 after valve surgery); optional after embolic-pattern, cortical or thalamic infarcts
  (it is reasonable, 2a, after ischaemic stroke, so it is not waste there unless the admission
  work-up already answered it, as the S10 and S11 histories record); waste where no ischaemic
  infarct needs a source (covert SVD, CAA, ICH, mixed, CADASIL) [AHA_ASA_2021_secondary]
- Prolonged monitoring (`order_cardiac_monitoring`): required where it is the decisive study (S07
  30-day event monitor; P08 pacemaker interrogation, `{}` with a descriptive `monitor_type`);
  optional after strategic or cortical infarcts with a normal ECG (M04, P09, S09); waste where AF is
  already on the ECG or a severe stenosis explains the pattern [AHA_ASA_2021_secondary]
- Amyloid biomarker: in mixed cases one criterion with two alternatives, `analyze_csf
  {"special_tests": ["Abeta42", "Abeta42_40_ratio", "phospho_tau"]}` and `order_advanced_imaging
  {"modality": "amyloid_PET"}`, both answered by concordant case data (M05, M07, P01, required);
  amyloid PET only where LP is declined or would need anticoagulation interrupted (M08, P02, with
  CSF avoided as harm and a concordant CSF follow-up authored). MCI (M01): CSF optional, biomarkers
  are not routine [AAN_MCI_2018]. CAA (P03, P04): CSF is waste (the diagnosis rests on MRI); P03
  amyloid PET optional. PET reports are binary ("Positive"/"Negative") with the visual read
- FDG-PET: optional (M07, M08), recommended in the posterior-predominant mixed case (P02); the
  style-guide wording "consistent with an Alzheimer-type metabolic profile" is the limit
- NOTCH3 (`order_specialized_test` `genetic_panel:CADASIL`): required in P05 and P06 (onset under
  60, family history or severe early SVD) [Rutten_2019]
- `check_drug_interactions` (ruling 6): recommended, one alternative per drug, only with a concrete
  interaction that changes management (warfarin or a DOAC with aspirin; a cholinesterase inhibitor
  with bisoprolol or diltiazem; edoxaban dose against Cockcroft-Gault CrCl): M03, M07, M08, M10,
  P08, S06, S07. Optional `{}` with case content where a medicine matters but does not change the
  plan (M05 gliclazide, P04 apixaban in CAA, P05 sumatriptan and sertraline, P09 zolpidem, S05
  apixaban). No criterion otherwise, and **never a `drug_interactions` fallback**. The stored output
  states the pair, mechanism and consequence in report voice, never a criterion's expected evidence

**Fallbacks:** no `advanced_imaging`, `labs` or literature fallback. The CT fallback describes the
patient's own CT with no time or comparison reference ("already obtained", "as on MRI"). Holter,
ECG and echo fallbacks match the patient (an AF patient's fallback Holter shows AF).

## 3. Tools that are typically USELESS (avoided as waste)

- `analyze_eeg`: no diagnostic role outside a rapidly progressive or fluctuating course [VASCOG_2014]
- `order_advanced_imaging` `DaTscan` and `MIBG_scan`: DLB tests; waste unless parkinsonism,
  fluctuations or hallucinations are present (each case gives its own reason)
- `interpret_labs` `paraneoplastic_panel`, `autoimmune_encephalitis_panel`: no subacute course,
  seizures or inflammatory CSF; the rationale names the case's own reason
- `order_ct_scan` when MRI is available and not contraindicated (28 cases): "MRI is available and
  not contraindicated; CT cannot show microbleeds, siderosis or small lacunes" [STRIVE_2]
- `order_echocardiogram`, `order_cardiac_monitoring`: only per section 2
- `order_advanced_imaging` `carotid_duplex` after a deep hypertensive ICH (M09)
- `analyze_csf` in CAA without acute haemorrhage (P03, P04): **waste, not harm**. CSF in CAA shows
  reduced Abeta40 and Abeta42, so "CSF cannot separate vascular from parenchymal amyloid" is wrong;
  the LP is simply not needed for a diagnosis that rests on MRI [Boston_v2]
- `order_advanced_imaging` `tau_PET`, `MR_spectroscopy`, `perfusion_MRI`, `CT_perfusion`;
  `order_body_imaging`, `order_microbiology`, `obtain_tissue_diagnosis`; EMG, polysomnography and
  tilt table: no role here

## 4. Tools that are HARMFUL

- `analyze_csf` where the patient has declined LP or would need anticoagulation interrupted for it
  (M08 on edoxaban, P02 after lumbar fusion), and with acute lobar haemorrhage or mass effect
- `analyze_brain_mri` with a non-MR-conditional device (P08)
- The main harms here are therapeutic and live in `assessment.prohibited_recommendations`
  (anticoagulating probable CAA where avoidable; aspirin for covert SVD alone; triptans in
  CADASIL; stopping anticoagulation for falls or sinus rhythm after ablation)

## 5. Sequence constraints and stop rule

All soft; both ids must exist:
- cognitive screen before MRI (all; P08 screen before CT) [VASCOG_2014]
- MRI before CSF where a CSF alternative exists (M01, M05, M07, P01)
- ECG before prolonged monitoring (M04, P08, P09, S07, S09) [AHA_ASA_2021_secondary]
- MRI before NOTCH3 (P05, P06); carotid duplex before MRA (S08); labs before MMA (S04)

Stop rule: `required_before_assessment` = the required criteria; `max_additional_actions` 1 (as in
ALZ-EARLY and ISCH-STR: one defensible extra order, such as an MMA at a borderline B12, is not
penalised).

## 6. Subtypes (vascular mechanism) and difficulty

`metadata.vascular_mechanism`: `svd` (M01, M02, P06, P07, S01-S05), `multi_infarct` (M03, M10, P08,
S06, S07, S08), `strategic` (M04, P09, S09, S10), `post_stroke` (M05, M09, S11), `hypoperfusion`
(M06), `mixed` (M07, M08, P01, P02), `caa` (P03, P04), `cadasil` (P05). M05 is labelled mixed.

- **Subcortical small-vessel:** confluent WMH plus lacunes; gait required; embolic work-up not
  required (ECG recommended after clinical lacunar events, S01).
- **Multi-infarct:** ECG and cervical-vessel imaging required; monitoring or TTE per section 2.
- **Strategic single infarct:** the reasoning point is anatomical; ECG recommended, TTE and
  monitoring optional.
- **Post-stroke:** the NINDS-AIREN temporal criterion is the discriminator [NINDS_AIREN_1993].
- **Hypoperfusion:** border-zone infarcts after documented hypotension; cervical vessels
  recommended, individualised BP target.
- **Mixed:** amyloid biomarker per section 2; the answer is both.
- **CAA:** strictly lobar haemorrhagic lesions with cSS; SWI essential.
- **CADASIL:** under 60, migraine with aura, family history, anterior temporal pole and external
  capsule involvement.

Two cases are deliberately not plain vascular dementia: M01 is mild VCI (F06.7; functional
independence preserved), and P08 is reached on CT, duplex and pacemaker interrogation because MRI
is contraindicated, and must state what CT cannot exclude (CAA stays moderate in its
differential).

## 7. Management facts the musts use (assessment, not tools; ruling 4)

- **Blood pressure:** after ischaemic stroke or TIA below 130/80 mmHg, lowered gradually, checking
  orthostatic BP in older or frail patients [AHA_ASA_2021_secondary]; after ICH below 130/80
  [AHA_ASA_2022_ICH]; covert SVD: treat hypertension to the same target, **no antiplatelet for covert
  SVD alone** [ESO_2021_SVD]; border-zone infarcts or an untreated severe stenosis (M06, M10, S08):
  individualise, avoid systolic below about 120 and orthostatic hypotension. Severe hypertension
  with grade 3 retinopathy and renal involvement (P06) is malignant hypertension: same-day hospital
  assessment, mean arterial pressure down 20-25% over several hours, then below 130/80 over weeks
  [ESC_HTN_emergencies_2019] [ESH_2023].
- **Lipids** (decision, Oct 2026: the 2026 ACC/AHA dyslipidemia guideline supersedes the LDL basis of
  AHA 2021): clinical ASCVD (ischaemic stroke, MI, symptomatic PAD) with two major events, or one
  plus two or more high-risk conditions (age 65 or more, hypertension, diabetes, current smoking,
  heart failure, LDL 100 or more despite statin plus ezetimibe), or CKD: **LDL goal below 55 mg/dL**,
  high-intensity statin then ezetimibe and/or a PCSK9 antibody; other clinical ASCVD below 70 mg/dL
  [ACC_AHA_dyslipidemia_2026]. The eight atherosclerotic stroke cases (M03, M05, M10, P08, S06, S07,
  S08, S11) carry the below-55 goal. Lacunar and cardioembolic stroke cases are given a
  high-intensity statin [AHA_ASA_2021_secondary]; covert SVD is primary prevention. After ICH,
  continue an indicated statin; no statin prohibition in CAA [AHA_ASA_2022_ICH]. Labs reports never
  state a target.
- **Glycaemia:** older adult with cognitive impairment: individualised HbA1c below about 8.0%, avoid
  hypoglycaemia, deprescribe sulfonylureas or insulin where hypoglycaemia occurs
  [ADA_older_adults_2026].
- **AF:** DOAC in preference to warfarin and stop aspirin without a separate indication; apixaban
  2.5 mg twice daily only with two of age 80 or more, weight 60 kg or less, creatinine 1.5 mg/dL or
  more; edoxaban 30 mg with CrCl 15-50 mL/min, weight 60 kg or less or a strong P-gp inhibitor
  (Cockcroft-Gault, not eGFR; weights are in `physical_exam.general`) [AHA_ASA_2021_secondary].
  Falls, age, cognitive impairment and a few deep microbleeds do not by themselves withhold
  anticoagulation; after ablation decide on CHA2DS2-VA, not rhythm (S05) [ESC_AF_2024].
- **LV thrombus after MI (M03):** warfarin INR 2-3 for at least 3 months; heart-failure referral for
  EF below 40% [AHA_ASA_2021_secondary].
- **Carotid:** symptomatic 70-99% within 6 months: CEA, ideally within 2 weeks; 50-69%: vascular-team
  decision on patient factors, never "below the threshold"; beyond 6 months manage as asymptomatic
  (P08) [AHA_ASA_2021_secondary].
- **CAA:** stop an antiplatelet without indication, avoid anticoagulation where possible, consider
  LAAO for AF (P04, 2b), BP below 130/80, warn that TFNE are not TIAs [AHA_ASA_2022_ICH] [Boston_v2].
- **CADASIL:** genetic counselling and cascade testing; no triptans or ergots [Rutten_2019].
- **Cognitive drugs:** in pure VaD a cholinesterase inhibitor or memantine is off-label with modest
  benefit ("may be considered"); in mixed cases a cholinesterase inhibitor is offered for the
  Alzheimer component, checking pulse and ECG with rate-control drugs [NICE_NG97].

## 8. Red herrings and pitfalls

- Incidental Fazekas 1-2 WMH in a treated hypertensive does not by itself explain a dementia.
- A normal screen in a high-baseline patient (P07: GP MoCA 26/30 in the HPI) does not outweigh the
  functional history.
- Hippocampal atrophy with a vascular burden points to mixed disease.
- Low-normal B12 is a contributor to check (MMA), not the explanation.
- AF with pure SVD imaging changes stroke prevention, not the mechanism.
- Apathy of SVD read as depression.
- An undocumented "small stroke" does not satisfy the temporal criterion.
- Template carry-over found in this condition: female ranges in men, identical normal values across
  cases, INR in the CMP, interpretive lab text, sinus-rhythm fallbacks in AF patients, "already
  obtained" CT text.

## 9. Allowed citations

- `[VASCOG_2014]` — Sachdev P, Kalaria R, O'Brien J, et al. Diagnostic criteria for vascular
  cognitive disorders: a VASCOG statement. Alzheimer Dis Assoc Disord 2014;28(3):206-218
- `[NINDS_AIREN_1993]` — Román GC, Tatemichi TK, Erkinjuntti T, et al. Vascular dementia:
  diagnostic criteria for research studies. Report of the NINDS-AIREN International Workshop.
  Neurology 1993;43(2):250-260
- `[AHA_ASA_2011_VCI]` — Gorelick PB, Scuteri A, Black SE, et al. Vascular contributions to
  cognitive impairment and dementia: a statement for healthcare professionals from the AHA/ASA.
  Stroke 2011;42(9):2672-2713
- `[STRIVE_2]` — Duering M, Biessels GJ, Brodtmann A, et al. Neuroimaging standards for research
  into small vessel disease: advances since 2013. Lancet Neurol 2023;22(7):602-618
- `[Boston_v2]` — Charidimou A, Boulouis G, Frosch MP, et al. The Boston criteria version 2.0 for
  cerebral amyloid angiopathy: a multicentre, retrospective, MRI-neuropathology diagnostic accuracy
  study. Lancet Neurol 2022;21(8):714-725
- `[AAN_MCI_2018]` — Petersen RC, Lopez O, Armstrong MJ, et al. Practice guideline update summary:
  mild cognitive impairment. Neurology 2018;90(3):126-135
- `[AAN_dementia_2001]` — Knopman DS, DeKosky ST, Cummings JL, et al. Practice parameter: diagnosis
  of dementia (an evidence-based review). Report of the Quality Standards Subcommittee of the AAN.
  Neurology 2001;56(9):1143-1153 (B12 and thyroid screening; syphilis screening only with clinical
  suspicion)
- `[NICE_NG97]` — NICE guideline NG97. Dementia: assessment, management and support for people
  living with dementia and their carers. 2018
- `[AHA_ASA_2021_secondary]` — Kleindorfer DO, Towfighi A, Chaturvedi S, et al. 2021 Guideline for
  the prevention of stroke in patients with stroke and transient ischemic attack. Stroke
  2021;52(7):e364-e467
- `[AHA_ASA_2022_ICH]` — Greenberg SM, Ziai WC, Cordonnier C, et al. 2022 Guideline for the
  management of patients with spontaneous intracerebral hemorrhage. Stroke 2022;53(7):e282-e361
- `[ESO_2021_SVD]` — Wardlaw JM, Debette S, Jokinen H, et al. ESO guideline on covert cerebral small
  vessel disease. Eur Stroke J 2021;6(2):CXI-CLXII
- `[ESC_AF_2024]` — Van Gelder IC, Rienstra M, Bunting KV, et al. 2024 ESC Guidelines for the
  management of atrial fibrillation developed in collaboration with EACTS. Eur Heart J
  2024;45(36):3314-3414
- `[ACC_AHA_dyslipidemia_2026]` — Blumenthal RS et al. 2026
  ACC/AHA/AACVPR/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA Guideline on the management of dyslipidemia.
  Circulation 2026;153(17):e1154-e1276; J Am Coll Cardiol 2026, doi 10.1016/j.jacc.2025.11.016
- `[ADA_older_adults_2026]` — American Diabetes Association Professional Practice Committee. 13.
  Older adults: Standards of Care in Diabetes-2026. Diabetes Care 2026;49(Suppl 1):S277-S296
- `[ESH_2023]` — Mancia G, Kreutz R, Brunström M, et al. 2023 ESH Guidelines for the management of
  arterial hypertension. J Hypertens 2023;41(12):1874-2071
- `[ESC_HTN_emergencies_2019]` — van den Born BJH, Lip GYH, Brguljan-Hitij J, et al. ESC Council on
  hypertension position document on the management of hypertensive emergencies. Eur Heart J
  Cardiovasc Pharmacother 2019;5(1):37-46
- `[Rutten_2019]` — Rutten JW, Van Eijsden BJ, Duering M, et al. The effect of NOTCH3 pathogenic
  variant position on CADASIL disease severity: NOTCH3 EGFr 1-6 pathogenic variant are associated
  with a more severe phenotype and lower survival compared with EGFr 7-34 pathogenic variant. Genet
  Med 2019;21(3):676-682
- `[BSH_B12_2014]` — Devalia V, Hamilton MS, Molloy AM. Guidelines for the diagnosis and treatment
  of cobalamin and folate disorders. Br J Haematol 2014;166(4):496-513
- `[DSM5]` — American Psychiatric Association. Diagnostic and Statistical Manual of Mental
  Disorders, Fifth Edition, Text Revision (DSM-5-TR). 2022. Major and mild vascular
  neurocognitive disorder

Superseded (do not cite in new text):
- `[ADA_2025_older_adults]` — superseded by `[ADA_older_adults_2026]` (same target); replaced in
  all VASC-DEM cases on 24 Oct 2026
- The 2018 AHA/ACC cholesterol guideline (never cited here) — superseded by
  `[ACC_AHA_dyslipidemia_2026]`
- The July 2026 tiers "`search_medical_literature` recommended" and "`check_drug_interactions`
  recommended in every case" — superseded by rulings 5 and 6 of the October 2026 round
