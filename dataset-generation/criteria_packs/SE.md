# Criteria pack: Status epilepticus

**ICD-10:** G41.x by type: G41.0 convulsive (including focal onset evolving to bilateral
convulsive SE), G41.2 complex partial (focal NCSE), G41.8 other (generalized NCSE, myoclonic SE,
faciobrachial dystonic seizure status), G41.9 unspecified. Mimic and comorbidity cases carry the
code of the scored diagnosis (PNES F44.5, hepatic encephalopathy K72.90, toxic causes T-codes),
and a case whose underlying disease is already in the history is coded by the part the case scores
(SE-P04 R56.9, SE-P06 G41.2).
**Condition enum:** `NeurologicalCondition.STATUS_EPILEPTICUS`
**Case ID prefix:** `SE`

Revised 24 October 2026 (review-round close-out) from `data/review/round-2026-10/plans/SE.md`
section 1 and the decisions in `plans/SE-decisions.md`. Rulings 4 to 8 of
`data/review/round-2026-10/ROUND_POLICY.md` apply: treatment and referrals are musts, never tool
calls; literature is never a clinical step; the drug check is tiered by a concrete interaction.

---

## 1. Diagnostic criteria

ILAE 2015 operational definitions [ILAE_2015_SE]:
- Convulsive SE: t1 5 minutes (treat), t2 30 minutes (long-term consequences).
- Focal SE with impaired awareness: t1 10 minutes, t2 over 60 minutes.
- Absence SE: t1 10 to 15 minutes.
- Refractory SE: seizures continue after an adequately dosed benzodiazepine and one second-line
  ASM. Super-refractory SE: continuing or recurring 24 hours or more after starting anaesthetic
  therapy [Shorvon_2011].

NCSE on EEG in a patient without a known epileptic encephalopathy: epileptiform discharges over
2.5 Hz, or 2.5 Hz or less with typical spatiotemporal evolution, subtle ictal phenomena, or clinical
and EEG improvement after IV ASM [Salzburg_NCSE_2015]. EEG wording per [ACNS_2021] (LPDs, GPDs,
LRDA, GRDA, "+F", "+R", ictal-interictal continuum); no invented terms such as "contralateral
activation pattern".

Lateralization (signs follow the lesion and the EEG; the lesion never moves to fit the signs):
- Ictal head and gaze deviation in a focal-onset seizure points away from the focus; postictal
  gaze preference and a destructive lesion point toward it.
- Clonic activity and postictal (Todd) weakness are contralateral to the focus; hyperreflexia and
  an extensor plantar response are contralateral to the hemispheric lesion.
- FBDS (LGI1) are contralateral to the involved hemisphere [Irani_2011].

## 2. Standard work-up hierarchy

Pathway order: core labs, CT, EEG (stabilize and image while cEEG is set up); ECG where it decides
the ASM; MRI; CSF; second-tier antibody or infection studies; body imaging; other studies;
drug check; literature last.

**Required in every case:**
- `interpret_labs` core panel `["CBC", "CMP", "magnesium"]`, plus only: `AED_levels` in a patient on
  an ASM; `tox_screen` when the cause is not evident; `ammonia` in liver disease or valproate use;
  `coagulation` on anticoagulants, liver disease or HELLP; `beta-hCG` only in women of reproductive
  age without a known pregnancy. Point-of-care glucose in every patient. Lactate, ABG and CK may be
  reported, are not required arguments, and are raised after convulsive SE [Brophy_2012]. Every
  analyte is reported once, in its own panel, with value, unit, range and flag; no "Exclusion
  studies" or "Mimic exclusion" block.
- `order_ct_scan` non-contrast, after stabilization: excludes hemorrhage, mass or edema and
  precedes any LP [Brophy_2012].
- `analyze_eeg` with `eeg_type` `continuous_icu` (alternative `video`; event characterization in
  suspected PNES: `video` first): continuous video-EEG for at least 24 hours in comatose patients,
  when NCSE is suspected, and during anaesthetic infusion and its weaning [Brophy_2012]. The
  initial EEG output is that recording; no follow-up EEG reports the response to treatment. A
  diagnostic benzodiazepine trial or a sedation wean is a separate follow-up with a trigger that a
  plain cEEG order cannot match.

**Required or recommended by indication:**
- `analyze_brain_mri`: required when SE is new-onset, unexplained or refractory, or encephalitis,
  autoimmune disease or tumor is suspected; recommended or optional when the cause is already
  established; absent in toxic SE with an evident cause (R2 guidance, July 2026).
- `analyze_csf`: required when the cause is unclear, without delay with fever or
  immunosuppression; always after imaging when mass effect is possible [Brophy_2012; Tunkel_2008].
  LP is an avoided action (`contraindicated` or `harm`) with mass effect or midline shift,
  platelets below 50 x10^9/L, uncorrected coagulopathy, or when the cause is established and LP
  adds only risk (eclampsia with HELLP, decompensated cirrhosis).
- `interpret_labs` second-tier panels (`autoimmune_encephalitis_panel`, `paraneoplastic_panel`,
  toxoplasma serology and HIV studies) as their own criterion, served by their own follow-up, not
  folded into the core labs: required where the case is autoimmune, paraneoplastic or
  opportunistic; recommended where autoimmune encephalitis is the treatable mimic [Graus_2016;
  Graus_2021].
- `order_microbiology`: only where infection is suspected (fever with a source, leukocytosis,
  immunosuppression with sepsis features); never "before antimicrobials" in a patient already on
  them. Seizure-related hyperthermia (37.5 to 38.5 C within hours of convulsions, no source) is
  not an indication.
- `analyze_ecg`: required where it decides the ASM or the antidote (TCA with QRS widening,
  hyperkalemia, amiodarone or post-arrest); recommended where a drug interaction or stroke makes it
  relevant; otherwise absent.
- `order_specialized_test` `ssep`: post-anoxic cases inside the prognostication window only (see
  section 7); not when the patient has woken.
- Body imaging for an occult tumor (ovarian teratoma, lung cancer) where the antibody points to one.

**Drug check (`check_drug_interactions`)**, ruling 6: required only where the patient's own drugs,
allergy, renal or hepatic function change the ASM (dexamethasone and enzyme inducers, carbamazepine
SIADH, amiodarone and phenytoin, antiretrovirals, warfarin, hepatic dosing, prior SJS, MDMA and
serotonergic drugs, magnesium with antihypertensives, clarithromycin and carbamazepine, TCA and
sodium-channel ASMs, dialysis removal of levetiracetam); recommended or optional otherwise. Output
in T-DDI form: "<drug A> + <drug B>: <mechanism>; <effect>; <management>", no treatment plan, no
diagnosis. Phenytoin does not prolong QT; with amiodarone the risks are hypotension, bradycardia and
AV block during loading, and amiodarone raises phenytoin levels (CYP2C9). Enzyme inducers lower
dexamethasone exposure.

**Literature (`search_medical_literature`)**, ruling 5: optional at most, outside the stop rule,
last in the pathway, no sequence constraint. Output in general cited voice, no patient values, no
criterion's expected text.

## 3. Treatment facts the musts use (never a tool call)

- First line: IV lorazepam 0.1 mg/kg (maximum 4 mg per dose, may repeat once after 5 to 10
  minutes), or IV diazepam 0.15 to 0.2 mg/kg (maximum 10 mg per dose), or IM midazolam 10 mg when
  weight is over 40 kg and there is no IV access [Glauser_2016].
- Second line, equivalent efficacy [ESETT_2019]: levetiracetam 60 mg/kg (maximum 4500 mg),
  fosphenytoin 20 mg PE/kg (maximum 1500 mg PE), valproate 40 mg/kg (maximum 3000 mg). Lacosamide
  was not studied in ESETT. Choose by contraindication (valproate: liver disease, hyperammonemia,
  pregnancy, mitochondrial disease; fosphenytoin: arrhythmia, AV block, hypotension,
  sodium-channel toxin overdose, prior aromatic-ASM SJS).
- Refractory SE: anaesthetic infusion (midazolam, propofol or ketamine) with intubation and cEEG
  [Brophy_2012].
- Glucose below 60 mg/dL: IV dextrose, with IV thiamine first or together where alcohol misuse or
  malnutrition is suspected; never delay glucose for thiamine [Brophy_2012].
- Wernicke: IV thiamine at least 200 mg three times daily before carbohydrate [EFNS_Wernicke_2010];
  500 mg three times daily is common practice but is not the EFNS dose.
- Acyclovir 10 mg/kg IV every 8 hours, renally adjusted, on suspicion of HSV encephalitis
  [Tunkel_2008].
- Hyponatremia with seizures: 150 mL of 3% saline over 20 minutes, up to twice while checking
  sodium, target a 5 mmol/L rise in the first hour; at most 10 mmol/L in the first 24 hours and
  8 mmol/L in each further 24 hours; at most 8 mmol/L in 24 hours with a demyelination risk factor
  (alcohol misuse, malnutrition, hypokalemia, liver disease, sodium 105 or below)
  [Spasovski_2014; Verbalis_2013].
- Valproate-associated hyperammonemic encephalopathy: stop valproate, IV L-carnitine
  [Lheureux_2009]; choose a non-valproate second-line ASM.
- Eclampsia: IV magnesium sulfate 4 to 6 g over 15 to 20 minutes, then 1 to 2 g/h, reduced with
  oliguria or raised creatinine, with reflex, respiratory and urine-output monitoring
  [Magpie_2002; ACOG_PB222_2020]; treat BP 160/110 or higher; delivery after maternal
  stabilization; benzodiazepine and a second-line ASM only for seizures that continue on magnesium.
  Nimodipine is not part of this plan.
- Organophosphate: atropine titrated to drying of bronchial secretions, pralidoxime per local
  protocol, benzodiazepines; avoid succinylcholine [Eddleston_2008].
- Isoniazid: IV pyridoxine gram for gram, 5 g when the amount is unknown, with a benzodiazepine;
  phenytoin is ineffective; routine screens miss isoniazid and the diagnosis is clinical (no key:
  state the facts without a citation).
- TCA cardiotoxicity: IV sodium bicarbonate for QRS over 100 ms or ventricular arrhythmia;
  benzodiazepines first; phenytoin and fosphenytoin avoided [Body_2011_TCA].
- Serotonin syndrome: benzodiazepines, active cooling, cyproheptadine [Boyer_2005].
- Warfarin-associated intracranial hemorrhage: 4-factor PCC with IV vitamin K [Frontera_2016].
- Anti-LGI1 relapse with FBDS: high-dose corticosteroids; ASMs alone rarely control FBDS
  [Irani_2011; Graus_2016].
- Post-arrest: multimodal prognostication no earlier than 72 hours after return of circulation and
  after sedation clears (bilaterally absent N20, highly malignant EEG, NSE, CT or MRI; status
  myoclonus within 72 hours is one predictor) [ERC_ESICM_2021]. Myoclonus alone never ends care;
  a patient who has woken is not prognosticated.

## 4. Tools that are typically waste

- `order_echocardiogram`, `order_cardiac_monitoring`: only with a cardiac question (arrest, stroke
  source, arrhythmia).
- `order_advanced_imaging` amyloid PET, DaTscan, carotid duplex, transcranial Doppler: no acute
  role. MR venography only where venous sinus thrombosis is a real differential (pregnancy).
- Polysomnography (avoided action text, T-PSG): "Polysomnography studies sleep disorders and has
  no role in the acute evaluation of status epilepticus."
- MRI in toxic SE with an evident cause.

## 5. Harmful or contraindicated

- LP with mass effect or midline shift, platelets below 50 x10^9/L or uncorrected coagulopathy
  (`contraindicated`); LP where the cause is established and it adds only risk (`harm`).
- Phenytoin or fosphenytoin in sodium-channel toxin overdose (TCA), in isoniazid toxicity (no
  effect), and after aromatic-ASM SJS; valproate in liver failure, hyperammonemia, pregnancy and
  POLG disease; neuroleptics in NMDAR encephalitis (NMS risk); anaesthetic escalation or
  intubation for PNES [LaFrance_2013] or for LPDs alone on the ictal-interictal continuum
  [ACNS_2021; Brophy_2012].

## 6. Sequence constraints

- Treatment is simultaneous with the work-up; benzodiazepines are never delayed for diagnostics
  [Brophy_2012] (a must, not a constraint).
- `order_ct_scan` -> `analyze_csf`: `hard` in every case with a CSF criterion; MRI -> CSF `hard`
  where ring-enhancing lesions make herniation possible.
- `interpret_labs` -> `check_drug_interactions`: `soft`, only where renal, hepatic or level data
  decide the drug.
- `analyze_ecg` -> `check_drug_interactions`: `soft`; `hard` only where an ASM is unsafe with the
  ECG finding (TCA with QRS widening).
- No constraint involves literature.
- Stop rule: `required_before_assessment` equals the required criteria; `max_additional_actions` 1.

## 7. Subtype variations

- **M:** NCSE with an underlying cause (encephalitis, tumor, metabolic, post-anoxic, structural).
- **S:** convulsive SE with a precipitant (non-adherence, metabolic, toxic, eclampsia, uremia).
- **P:** refractory, toxic or diagnostically difficult SE, and mimics on the ictal-interictal
  continuum (hepatic encephalopathy with triphasic GPDs, LPDs after stroke, PNES).
- **R:** reverse or mimic cases; the key tool is video-EEG.

## 8. Red-herring categories and pitfalls

- Cessation of convulsions does not exclude NCSE.
- An ASM level "in range" does not exclude breakthrough seizures.
- Normal routine labs do not exclude autoimmune or structural causes.
- Temperature 37.5 to 38.5 C within hours of convulsions without a source and with normal WBC or
  procalcitonin is seizure-related hyperthermia (T-HYPERTHERMIA), not infection.
- Triphasic morphology does not separate metabolic encephalopathy from NCSE; reactivity, evolution
  and a benzodiazepine trial under EEG do.
- Template carry-over found in October 2026: beta-hCG in men or in known pregnancy, meningitis
  blood cultures "before antimicrobials" in afebrile patients, post-treatment level and EEG
  follow-ups, the DaTscan rationale under polysomnography, ECG reports that say an ASM is "safe to
  load", MRI reports that "confirm" the diagnosis.

## 9. Allowed citations

Status epilepticus
- `[Brophy_2012]` - Brophy GM, Bell R, Claassen J, et al. Guidelines for the evaluation and
  management of status epilepticus. Neurocrit Care 2012;17:3-23. **Governs** evaluation and
  refractory management (no NCS update as of 24 Oct 2026; the 2026 NCS guideline covers
  neuroprognostication in SE only).
- `[ILAE_2015_SE]` - Trinka E, Cock H, Hesdorffer D, et al. A definition and classification of
  status epilepticus: report of the ILAE Task Force on Classification of Status Epilepticus.
  Epilepsia 2015;56:1515-1523.
- `[Glauser_2016]` - Glauser T, Shinnar S, Gloss D, et al. Evidence-based guideline: treatment of
  convulsive status epilepticus in children and adults: report of the Guideline Committee of the
  American Epilepsy Society. Epilepsy Curr 2016;16:48-61. **Governs** first-line treatment.
- `[ESETT_2019]` - Kapur J, Elm J, Chamberlain JM, et al. Randomized trial of three anticonvulsant
  medications for status epilepticus. N Engl J Med 2019;381:2103-2113.
- `[Salzburg_NCSE_2015]` - Leitinger M, Beniczky S, Rohracher A, et al. Salzburg Consensus
  Criteria for Non-Convulsive Status Epilepticus: approach to clinical application. Epilepsy Behav
  2015;49:158-163. (Reference corrected 24 Oct 2026; the earlier pack gave "Epilepsia
  2015;56:1411-1416".)
- `[Shorvon_2011]` - Shorvon S, Ferlisi M. The treatment of super-refractory status epilepticus: a
  critical review of available therapies and a clinical treatment protocol. Brain
  2011;134:2802-2818.
- `[ACNS_2021]` - Hirsch LJ, Fong MWK, Leitinger M, et al. American Clinical Neurophysiology
  Society's Standardized Critical Care EEG Terminology: 2021 version. J Clin Neurophysiol
  2021;38:1-29.
- `[ERC_ESICM_2021]` - Nolan JP, Sandroni C, Bottiger BW, et al. European Resuscitation Council and
  European Society of Intensive Care Medicine guidelines 2021: post-resuscitation care. Intensive
  Care Med 2021;47:369-421.
- `[LaFrance_2013]` - LaFrance WC Jr, Baker GA, Duncan R, et al. Minimum requirements for the
  diagnosis of psychogenic nonepileptic seizures: a staged approach. Epilepsia 2013;54:2005-2018.

Causes and their management
- `[Spasovski_2014]` - Spasovski G, Vanholder R, Allolio B, et al. Clinical practice guideline on
  diagnosis and treatment of hyponatraemia. Eur J Endocrinol 2014;170:G1-G47.
- `[Verbalis_2013]` - Verbalis JG, Goldsmith SR, Greenberg A, et al. Diagnosis, evaluation, and
  treatment of hyponatremia: expert panel recommendations. Am J Med 2013;126(10 Suppl 1):S1-S42.
- `[EFNS_Wernicke_2010]` - Galvin R, Brathen G, Ivashynka A, et al. EFNS guidelines for diagnosis,
  therapy and prevention of Wernicke encephalopathy. Eur J Neurol 2010;17:1408-1418.
- `[Lheureux_2009]` - Lheureux PE, Hantson P. Carnitine in the treatment of valproic acid-induced
  toxicity. Clin Toxicol 2009;47:101-111.
- `[Graus_2016]` - Graus F, Titulaer MJ, Balu R, et al. A clinical approach to diagnosis of
  autoimmune encephalitis. Lancet Neurol 2016;15:391-404.
- `[Graus_2021]` - Graus F, Vogrig A, Muniz-Castrillo S, et al. Updated diagnostic criteria for
  paraneoplastic neurologic syndromes. Neurol Neuroimmunol Neuroinflamm 2021;8:e1014.
- `[Titulaer_2013]` - Titulaer MJ, McCracken L, Gabilondo I, et al. Treatment and prognostic
  factors for long-term outcome in patients with anti-NMDA receptor encephalitis: an observational
  cohort study. Lancet Neurol 2013;12:157-165.
- `[Irani_2011]` - Irani SR, Michell AW, Lang B, et al. Faciobrachial dystonic seizures precede
  Lgi1 antibody limbic encephalitis. Ann Neurol 2011;69:892-900.
- `[Tunkel_2008]` - Tunkel AR, Glaser CA, Bloch KC, et al. The management of encephalitis: clinical
  practice guidelines by the Infectious Diseases Society of America. Clin Infect Dis
  2008;47:303-327.
- `[Fugate_2015]` - Fugate JE, Rabinstein AA. Posterior reversible encephalopathy syndrome:
  clinical and radiological manifestations, pathophysiology, and outstanding questions. Lancet
  Neurol 2015;14:914-925.
- `[Hermann_2021]` - Hermann P, Appleby B, Brandel JP, et al. Biomarkers and diagnostic guidelines
  for sporadic Creutzfeldt-Jakob disease. Lancet Neurol 2021;20:235-246.
- `[Vilstrup_2014]` - Vilstrup H, Amodio P, Bajaj J, et al. Hepatic encephalopathy in chronic
  liver disease: 2014 practice guideline by the AASLD and the EASL. Hepatology 2014;60:715-735.
- `[AASLD_ascites_2021]` - Biggins SW, Angeli P, Garcia-Tsao G, et al. Diagnosis, evaluation, and
  management of ascites, spontaneous bacterial peritonitis and hepatorenal syndrome: 2021 practice
  guidance by the AASLD. Hepatology 2021;74:1014-1048.
- `[EASL_decomp_2018]` - European Association for the Study of the Liver. EASL Clinical Practice
  Guidelines for the management of patients with decompensated cirrhosis. J Hepatol
  2018;69:406-460.
- `[ACOG_PB222_2020]` - American College of Obstetricians and Gynecologists. Gestational
  hypertension and preeclampsia: ACOG Practice Bulletin No. 222. Obstet Gynecol
  2020;135:e237-e260.
- `[Magpie_2002]` - Magpie Trial Collaborative Group. Do women with pre-eclampsia, and their
  babies, benefit from magnesium sulphate? The Magpie Trial: a randomised placebo-controlled trial.
  Lancet 2002;359:1877-1890.
- `[Frontera_2016]` - Frontera JA, Lewin JJ 3rd, Rabinstein AA, et al. Guideline for reversal of
  antithrombotics in intracranial hemorrhage. Neurocrit Care 2016;24:6-46.
- `[Eddleston_2008]` - Eddleston M, Buckley NA, Eyer P, Dawson AH. Management of acute
  organophosphorus pesticide poisoning. Lancet 2008;371:597-607.
- `[Boyer_2005]` - Boyer EW, Shannon M. The serotonin syndrome. N Engl J Med 2005;352:1112-1120.
- `[Body_2011_TCA]` - Body R, Bartram T, Azam F, Mackway-Jones K. Guidelines in Emergency Medicine
  Network (GEMNet): guideline for the management of tricyclic antidepressant overdose. Emerg Med J
  2011;28:347-368. (Verified 24 Oct 2026; allow-listed for SE-S10, not yet cited in a case.)
- `[EANO_2021]` - Weller M, van den Bent M, Preusser M, et al. EANO guidelines on the diagnosis and
  treatment of diffuse gliomas of adulthood. Nat Rev Clin Oncol 2021;18:170-186. (SE-M02.)
- `[AHA_ASA_Stroke_2026]` - Prabhakaran S, Gonzalez NR, Zachrison KS, et al. AHA/ASA guideline for
  the early management of patients with acute ischemic stroke. Stroke 2026 (full entry in the
  ISCH-STR pack). (SE-P04.)
- `[HIV_OI_guideline]` - Panel on Guidelines for the Prevention and Treatment of Opportunistic
  Infections in Adults and Adolescents With HIV. NIH, CDC, HIV Medicine Association of the IDSA.
  Toxoplasma gondii encephalitis section, clinicalinfo.hiv.gov (living guideline; cite with the
  access date). (SE-M08; allow-listed, not yet cited in a case.)

Superseded
- `[AHA_Stroke_2019]` - Powers WJ et al. Guidelines for the early management of patients with
  acute ischemic stroke: 2019 update. Stroke 2019;50:e344-e418. Superseded by
  `[AHA_ASA_Stroke_2026]`; not cited in any SE case.
