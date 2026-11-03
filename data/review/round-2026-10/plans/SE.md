# SE: condition plan for the October 2026 review round

Lead plan for the 30 status epilepticus cases (SE-M01..M09, P01..P08, RS11, S01..S12). Read
`ROUND_POLICY.md` and `PATTERNS.md` first; this plan does not repeat them.

All 24 notes are from Reviewer 2 and cover 14 cases. Notes-file status: approved M03, M04, M06,
M07, P01, RS11, S01, S06, S07, S09; needs changes S03, S04, S08, S12. The other 16 cases have no
notes; PATTERNS counts 26 R2 approvals, so treat them as approved. In approved cases fix only real
errors; every class in section 2 is a real error (template carry-over, leaks, impossible outputs,
outputs that report treatment), so it applies to approved cases too. Log why.

Baseline (24 October 2026, before any edit):
- `perfect_agent.py` passes 30/30. With `-v` it warns that duplicate lab criteria are answered by
  the initial labs (M03, M05, M08, M09, P05, P07, P08, S01, S03, S04, S05, S06, S10) and that S02
  has two literature criteria. C4 removes the duplicates.
- `pytest agent-platform/tests/test_case_guards.py -k SE-` fails in 10 cases (M01, M04, M05, P01,
  P04, S01, S04, S05, S11, S12): initial `drug_interactions` or `literature_search` "general"
  outputs, or fallback drug and literature outputs, repeat a criterion's `expected_evidence`.
  C8 and C9 remove them; the guard must pass in all 30 after your edit.
- The EEG criterion is hijacked in most M and P cases: the follow-up trigger
  `request_continuous_eeg_monitoring` shares the token "continuous" with the `eeg_type`
  `continuous_icu`, so a correct cEEG order receives the post-treatment follow-up instead of the
  initial EEG (followup_matcher overrides the initial output on a specific re-order). C4 fixes it.

Use: apply every class of section 2 that names your case (canonical text verbatim, `<...>` slots
filled from the case), then the case items of section 4, rebuild criteria, follow-ups,
constraints and stop rule per section 3, run both checks (`perfect_agent.py <ID> -v`, the case
guards, and `case_io.py check`), and write `logs/{CASE_ID}.md` citing every note id with its
ruling. Section 2 cites notes by 8-character prefix; section 4 gives full ids.

New text: English, US spelling as the cases use, no em or en dashes. New numbers must be
plausible for the patient and differ from case to case (no template values). Doses go in musts as
mg/kg with the maximum dose, because the case has no weight field.

---

## 1. Governing guidelines and canonical facts

### 1.1 Sources (allow-listed keys first; the rest need the CENTRAL allow-list request in section 5)

Allow-listed in `criteria_packs/SE.md`:
- `[Brophy_2012]` Brophy GM et al. Guidelines for the evaluation and management of status
  epilepticus. Neurocrit Care 2012;17:3-23.
- `[ILAE_2015_SE]` Trinka E et al. A definition and classification of status epilepticus. Report
  of the ILAE Task Force. Epilepsia 2015;56:1515-1523.
- `[Glauser_2016]` Glauser T et al. Evidence-based guideline: treatment of convulsive status
  epilepticus in children and adults (AES). Epilepsy Curr 2016;16:48-61.
- `[ESETT_2019]` Kapur J et al. Randomized trial of three anticonvulsant medications for status
  epilepticus. N Engl J Med 2019;381:2103-2113.
- `[Salzburg_NCSE_2015]` Leitinger M et al. Salzburg Consensus Criteria for non-convulsive status
  epilepticus: approach to clinical application. Epilepsy Behav 2015;49:158-163.
- `[Shorvon_2011]` Shorvon S, Ferlisi M. The treatment of super-refractory status epilepticus: a
  critical review of available therapies and a clinical treatment protocol. Brain
  2011;134:2802-2818.

To add (CENTRAL 1). Workers may cite these keys now; the allow-list follows centrally:
- `[ACNS_2021]` Hirsch LJ et al. American Clinical Neurophysiology Society's Standardized Critical
  Care EEG Terminology: 2021 version. J Clin Neurophysiol 2021;38:1-29.
- `[Spasovski_2014]` Spasovski G et al. Clinical practice guideline on diagnosis and treatment of
  hyponatraemia. Eur J Endocrinol 2014;170:G1-G47.
- `[Verbalis_2013]` Verbalis JG et al. Diagnosis, evaluation, and treatment of hyponatremia:
  expert panel recommendations. Am J Med 2013;126(10 Suppl 1):S1-S42.
- `[EFNS_Wernicke_2010]` Galvin R et al. EFNS guidelines for diagnosis, therapy and prevention of
  Wernicke encephalopathy. Eur J Neurol 2010;17:1408-1418.
- `[Lheureux_2009]` Lheureux PE, Hantson P. Carnitine in the treatment of valproic acid-induced
  toxicity. Clin Toxicol 2009;47:101-111.
- `[Graus_2016]` Graus F et al. A clinical approach to diagnosis of autoimmune encephalitis.
  Lancet Neurol 2016;15:391-404.
- `[Graus_2021]` Graus F et al. Updated diagnostic criteria for paraneoplastic neurologic
  syndromes. Neurol Neuroimmunol Neuroinflamm 2021;8:e1014.
- `[Titulaer_2013]` Titulaer MJ et al. Treatment and prognostic factors for long-term outcome in
  patients with anti-NMDA receptor encephalitis. Lancet Neurol 2013;12:157-165.
- `[Irani_2011]` Irani SR et al. Faciobrachial dystonic seizures precede Lgi1 antibody limbic
  encephalitis. Ann Neurol 2011;69:892-900.
- `[Tunkel_2008]` Tunkel AR et al. The management of encephalitis: clinical practice guidelines by
  the IDSA. Clin Infect Dis 2008;47:303-327.
- `[Fugate_2015]` Fugate JE, Rabinstein AA. Posterior reversible encephalopathy syndrome. Lancet
  Neurol 2015;14:914-925.
- `[Hermann_2021]` Hermann P et al. Biomarkers and diagnostic guidelines for sporadic
  Creutzfeldt-Jakob disease. Lancet Neurol 2021;20:235-246.
- `[Vilstrup_2014]` Vilstrup H et al. Hepatic encephalopathy in chronic liver disease: 2014
  practice guideline by AASLD and EASL. Hepatology 2014;60:715-735.
- `[AASLD_ascites_2021]` Biggins SW et al. Diagnosis, evaluation, and management of ascites,
  spontaneous bacterial peritonitis and hepatorenal syndrome: 2021 AASLD practice guidance.
  Hepatology 2021;74:1014-1048.
- `[EASL_decomp_2018]` EASL Clinical Practice Guidelines for the management of patients with
  decompensated cirrhosis. J Hepatol 2018;69:406-460.
- `[ACOG_PB222_2020]` ACOG Practice Bulletin No. 222: Gestational hypertension and preeclampsia.
  Obstet Gynecol 2020;135:e237-e260.
- `[Magpie_2002]` Magpie Trial Collaborative Group. Lancet 2002;359:1877-1890.
- `[AHA_Stroke_2019]` Powers WJ et al. Guidelines for the early management of patients with acute
  ischemic stroke: 2019 update. Stroke 2019;50:e344-e418.
- `[ERC_ESICM_2021]` Nolan JP et al. European Resuscitation Council and European Society of
  Intensive Care Medicine guidelines 2021: post-resuscitation care. Intensive Care Med
  2021;47:369-421.
- `[Frontera_2016]` Frontera JA et al. Guideline for reversal of antithrombotics in intracranial
  hemorrhage. Neurocrit Care 2016;24:6-46.
- `[Eddleston_2008]` Eddleston M et al. Management of acute organophosphorus pesticide poisoning.
  Lancet 2008;371:597-607.
- `[Boyer_2005]` Boyer EW, Shannon M. The serotonin syndrome. N Engl J Med 2005;352:1112-1120.
- `[LaFrance_2013]` LaFrance WC Jr et al. Minimum requirements for the diagnosis of psychogenic
  nonepileptic seizures: a staged approach. Epilepsia 2013;54:2005-2018.

No allow-listed or added source covers isoniazid (P08) or TCA (S10) toxicology; state the facts
below without a citation key rather than inventing one.

### 1.2 Canonical facts (use these; do not restate them differently)

Definitions and EEG
- Convulsive SE: t1 5 minutes (treat), t2 30 minutes (long-term consequences). Focal SE with
  impaired awareness: t1 10 minutes, t2 over 60 minutes. Absence SE: t1 10-15 minutes
  [ILAE_2015_SE].
- NCSE on EEG in a patient without known epileptic encephalopathy: epileptiform discharges over
  2.5 Hz, or 2.5 Hz or less with typical spatiotemporal evolution, subtle ictal phenomena, or
  clinical and EEG improvement after IV ASM [Salzburg_NCSE_2015].
- EEG wording per [ACNS_2021]: LPDs, GPDs, LRDA, GRDA, "+F", "+R", ictal-interictal continuum
  (IIC). Not "contralateral activation pattern" or other invented terms.
- Continuous video-EEG for at least 24 hours in comatose patients or when NCSE is suspected, and
  during anaesthetic infusion and its weaning [Brophy_2012]. The EEG order in every case is
  `analyze_eeg` with `eeg_type` `continuous_icu` (or `video`), not `routine`, when the patient is
  not back to baseline.

Lateralization
- Ictal head and gaze deviation in a focal-onset seizure points away from the focus (left
  hemisphere focus: rightward deviation). Postictal gaze preference and a destructive lesion point
  toward the lesion. Clonic activity and postictal (Todd) weakness are contralateral to the focus;
  hyperreflexia and an extensor plantar response are contralateral to the hemispheric lesion.
- FBDS (LGI1) are contralateral to the involved hemisphere [Irani_2011].

Treatment (musts only; never a tool call)
- First line: IV lorazepam 0.1 mg/kg (maximum 4 mg per dose, may repeat once after 5 to 10
  minutes), or IV diazepam 0.15-0.2 mg/kg (maximum 10 mg per dose), or IM midazolam 10 mg when
  weight is over 40 kg and there is no IV access [Glauser_2016].
- Second line, equivalent efficacy [ESETT_2019]: levetiracetam 60 mg/kg (maximum 4500 mg),
  fosphenytoin 20 mg PE/kg (maximum 1500 mg PE), valproate 40 mg/kg (maximum 3000 mg). Lacosamide
  was not studied in ESETT; it is an alternative, not a trial-proven equivalent. Choose by the
  case's contraindications (valproate: liver disease, hyperammonemia, pregnancy, mitochondrial
  disease; fosphenytoin: arrhythmia, AV block, hypotension, sodium-channel toxin overdose).
- Refractory SE (failed benzodiazepine and one second-line drug): anaesthetic infusion
  (midazolam, propofol or ketamine) with intubation and cEEG [Brophy_2012]; super-refractory SE
  over 24 hours of anaesthesia [Shorvon_2011].
- Point-of-care glucose in every patient; IV dextrose when below 60 mg/dL, with IV thiamine
  first or together where alcohol misuse or malnutrition is suspected; never delay glucose for
  thiamine [Brophy_2012].
- Wernicke: thiamine 500 mg IV three times daily for 2 to 3 days, then 250 mg daily
  [EFNS_Wernicke_2010].
- Acyclovir 10 mg/kg IV every 8 hours, adjusted for renal function, started on suspicion of HSV
  encephalitis without waiting for PCR [Tunkel_2008].
- Hyponatremia with seizures: 150 mL of 3% saline over 20 minutes, repeated up to twice while
  checking sodium, target a rise of 5 mmol/L in the first hour; do not exceed 10 mmol/L in the
  first 24 hours and 8 mmol/L in each further 24 hours; in patients at high risk of osmotic
  demyelination (alcohol misuse, malnutrition, hypokalemia, liver disease, sodium 105 or below) aim
  for at most 8 mmol/L in 24 hours [Spasovski_2014; Verbalis_2013].
- Valproate-associated hyperammonemic encephalopathy: stop valproate, give IV L-carnitine
  [Lheureux_2009]; pick a non-valproate second-line ASM.
- Eclampsia: IV magnesium sulfate 4-6 g load over 15 to 20 minutes then 1-2 g/h, reduced with
  oliguria or raised creatinine, monitoring reflexes, respiration and urine output [Magpie_2002;
  ACOG_PB222_2020]; treat severe hypertension (160/110 or higher); delivery after maternal
  stabilization; benzodiazepines and a second-line ASM for seizures that continue despite
  magnesium. Nimodipine is not a teratogen and has no place in this plan; do not mention it.
- Organophosphate: atropine titrated to drying of bronchial secretions, pralidoxime per local
  protocol, benzodiazepines for seizures [Eddleston_2008].
- Isoniazid: IV pyridoxine gram for gram of isoniazid ingested, 5 g IV when the amount is unknown,
  with benzodiazepines; phenytoin is ineffective. The diagnosis is clinical; no isoniazid level is
  in the vocabulary.
- TCA cardiotoxicity: IV sodium bicarbonate for QRS over 100 ms or ventricular arrhythmia;
  phenytoin and fosphenytoin are avoided (sodium-channel blockade); benzodiazepines first.
- Serotonin syndrome: benzodiazepines, active cooling, cyproheptadine [Boyer_2005].
- Anticoagulant-associated SDH: reverse warfarin with 4-factor PCC plus IV vitamin K
  [Frontera_2016].
- Post-arrest: multimodal neuroprognostication no earlier than 72 hours after return of
  circulation and after sedation is cleared, using bilaterally absent N20, highly malignant EEG,
  NSE, CT or MRI; status myoclonus in the first 72 hours is one of these predictors
  [ERC_ESICM_2021]. Myoclonus alone never ends care.

Work-up
- Labs in every SE: point-of-care glucose, CBC, electrolytes with calcium, magnesium, renal and
  hepatic function, ASM levels in every patient already on an ASM, toxicology when the cause is
  not evident, beta-hCG only in women of reproductive age without known pregnancy [Brophy_2012].
  After convulsive SE expect lactic acidosis and CK rise.
- Non-contrast CT after stabilization; MRI when SE is new-onset, unexplained or refractory, or
  encephalitis, autoimmune disease or tumor is suspected; not required when the cause is already
  established (R2 guidance, July 2026).
- CSF when the cause is unclear, without delay with fever or immunosuppression, after imaging when
  mass effect is possible; LP is contraindicated with mass effect or midline shift, platelets
  below 50 x10^9/L, or uncorrected coagulopathy (R2 guidance; [Tunkel_2008]).
- Blood cultures only where infection is suspected (fever, leukocytosis, a source, or
  immunosuppression with sepsis features). Seizure-related hyperthermia (37.5-38.5 C within hours
  of a convulsion, without a source) is not an indication by itself.

### 1.3 Canonical text

T-LABS (core labs criterion; keep its id; adapt the extras)
- `label`: "Emergency laboratory work-up: glucose, CBC, electrolytes, magnesium, renal and hepatic
  function<, extras>"
- `required_arguments`: `{"panels": ["CBC", "CMP", "magnesium", <extras>]}`, where extras are
  only: `AED_levels` when on an ASM; `tox_screen` when the cause is not evident from the history;
  `ammonia` in liver disease or valproate; `coagulation` on anticoagulants, liver disease or HELLP;
  `beta-hCG` in women of reproductive age without known pregnancy. Lactate, ABG and CK may be
  reported in the output but are not required arguments.
- `rationale`: "Glucose, electrolyte, renal and hepatic derangements are reversible causes of
  seizures and decide the ASM and its dose<; case reason for each extra> [Brophy_2012]."
- `expected_evidence`: the case's real findings, one clause each, with numbers.

T-EEG (keep its id)
- `label`: "Continuous video-EEG to confirm <non-convulsive SE / ongoing seizures / the event
  type> and monitor treatment"
- `required_arguments`: `{"eeg_type": "continuous_icu"}`; add a `video` alternative. P02 (event
  characterization): `video` with a `continuous_icu` alternative.
- `rationale`: "<NCSE / persistent impaired consciousness> needs EEG confirmation; continuous
  monitoring for at least 24 hours [Brophy_2012]; terminology [ACNS_2021]."

T-CT (keep its id): `label` "Non-contrast head CT after stabilization", `rationale` "Excludes
hemorrhage, mass or edema that would change management, and must precede any LP [Brophy_2012]."

T-MUST-BZD (where the HPI does not say benzodiazepines were already given adequately): "Give a
benzodiazepine now: IV lorazepam 0.1 mg/kg (maximum 4 mg per dose, repeat once), or IM midazolam
10 mg without IV access [Glauser_2016]." Where the HPI says first-line was given, the must is the
next tier instead.

T-MUST-2L: "Load a second-line ASM: <drug and dose from 1.2, chosen for the case>, and avoid
<drug> because <case reason> [ESETT_2019]."

T-MUST-cEEG: "Continue video-EEG for at least 24 hours after clinical and electrographic seizure
control [Brophy_2012]."

T-HYPERTHERMIA red herring (RS11 and any convulsive case with 37.5-38.5 C and no source):
"Temperature <value> C within hours of prolonged convulsions with no source and normal <WBC /
procalcitonin>: seizure-related hyperthermia, not infection."

T-PSG avoided action (replaces the DaTscan rationale under the polysomnography entry):
"Polysomnography studies sleep disorders and has no role in the acute evaluation of status
epilepticus."

T-LIT (literature output, initial or follow-up, any query): 3 to 6 sentences in general cited
voice on the case's topic, from facts in 1.2 with their keys; no patient values, no "this
patient", no criterion's expected text, nothing that names the diagnosis beyond the topic the
query asks about. Example for an SE query: "Convulsive status epilepticus is treated at 5 minutes
with an adequately dosed benzodiazepine [Glauser_2016]. Levetiracetam, fosphenytoin and valproate
were equally effective as second-line agents in ESETT [ESETT_2019]. Seizures continuing after
both tiers are refractory and are treated with an anaesthetic infusion under continuous EEG
[Brophy_2012]."

T-DDI (drug check output): interactions only, each as "<drug A> + <drug B>: <mechanism>;
<effect>; <management>", for the patient's own drugs and the ASMs a clinician would consider. No
treatment plan, no doses for the condition, no diagnosis.

---

## 2. Error classes in this condition

### C1. "Exclusion studies" and "Mimic exclusion" blocks (PATTERNS template carry-over; all 30; notes 0aed33a9 M03, 54e2cb28 S03, f6c10984 S04)
Every case has a serum lab block of analytes reported "Within reference range" or "No abnormality
identified" with no number, and the clinical_significance "Ordered to exclude an alternative
cause; the result does not support one, which is what this case's diagnosis rests on". M03, M05
and P06 also have a "Mimic exclusion" block ("Reported negative in this case's own workup;
excludes this reversible mimic"). Both contradict the real panels (M03 urinalysis 2+ protein and
RBC casts; S03 UTI urinalysis; S04 ESR and autoimmune "normal" against dsDNA 142, C3 48, C4 6).
Fix (HEP-ENC C9 precedent): delete both blocks. Report each analyte once, in its proper panel,
with value, unit, range and flag consistent with the case physiology (lactate high and ABG
acidotic after convulsive SE; S08 haptoglobin low; S05 thiamine low; urinalysis abnormal in UTI
cases; RS11 troponin coherent with the rest). Drop entries already reported elsewhere, and drop
analytes that are not indicated; remove them from the criterion's `required_arguments` too. CSF
assays placed in serum labs (M05 oligoclonal_bands, M06 cytology and autoimmune_panel, P06
HSV_PCR) leave the labs; report them in the CSF output if a CSF criterion exists, else drop.

### C2. beta-hCG in patients who cannot or need not be tested (PATTERNS template carry-over)
Remove from panels, outputs and labels: P01, RS11 (note 64b7befa), S01 (note 138b30a5), S06, S10
(male); S07 (woman 68); S08 (known 28-week pregnancy). Keep with a real negative value (mIU/mL,
reference below 5): M03, M05, P02, P08, S02, S04.

### C3. Template blood cultures and "before antimicrobials" (PATTERNS meningitis carry-over; notes b1f48e5f M06, e89c4880 M07, 0dd7682a P01, e610cd86 RS11, 59001cc7 S03, 5daa0f16 S12, 0afbb493 M04)
The microbiology criterion reads "Draw two sets of blood cultures before antimicrobials" with
expected "Growth identifies the organism", copied from the meningitis panel.
- Delete criterion, follow-up and any musts about it: M01, M02, M07, M08, P01, P06, RS11, S12, and
  S01 (urine template).
- Keep with case-specific text: M05 blood cultures recommended (39.1 C); M06 blood cultures recommended, `before_antimicrobials` removed from
  `required_arguments`, output says collected during TMP-SMX day 12, no growth; S05 blood
  cultures recommended; P07 ascitic fluid required, blood cultures recommended and reported
  pending or negative; delete P07's "Blood Culture E. coli" lab panel (wrong tool). M04 urine
  culture recommended, negative (as now). M09 urine culture required. S03 urine culture required,
  `before_antimicrobials` removed; output: E. coli over 10^5 CFU/mL, resistant to TMP-SMX,
  susceptible to ceftriaxone, collected on day 4 of TMP-SMX.
- Add blood cultures, recommended, in S03 (urosepsis with SE) and S04 (febrile on prednisone),
  ordered after the core labs.
- RS11: 38.1 C is seizure-related hyperthermia (T-HYPERTHERMIA); the HPI states the temperature
  was normal before the seizure; no infective work-up.

### C4. Outputs that report treatment effects, and treatment criteria disguised as labs (ruling 4)
- Delete post-treatment lab follow-ups: `request_aed_optimization` (M02, M03, M04, M06, P05, P06,
  P07, P08, RS11, S01, S03, S04, S05, S06, S07, S08, S09, S11); M09 "Coagulation After Reversal";
  P01 "thiamine optimization"; P04 "AED Level Post-Loading"; P07 "Ammonia After Treatment" and
  "Ascitic fluid at 48h".
- Delete `request_continuous_eeg_monitoring` follow-ups that report response to treatment, in
  every case. Keep only diagnostic manoeuvres, with a trigger that a plain cEEG order cannot match
  (no token "continuous", "eeg", "monitoring", "video", "icu"): P01 benzodiazepine trial
  (`trigger_action` "benzodiazepine_trial"); P03 propofol weaning ("sedation_wean"); M07 and P03
  natural post-anoxic evolution at 24 to 72 hours only if no treatment is reported in it. P02 event
  capture: merge into the initial EEG output.
- Delete criteria that are treatment under a lab tool, and move their content to musts: P07 a7
  (SBP treatment), P08 a7 (bicarbonate), S03 a7 (UTI antibiotics), S06 a6 and S10 a7
  (rhabdomyolysis management), M09 a9 (treat UTI), P05 a8 (cholinesterase recovery).
- Delete duplicate lab criteria answered by the initial labs and fold their arguments into
  T-LABS: S01 a7, S05 a7, M08 a5, M09 a6, P07 a6. For the other duplicates the perfect agent
  flags (M03 a6, M05 a6, P03 a7, P05 a8, P08 a7, S03 a7, S04 a9, S06 a6, S10 a7), keep only a
  criterion whose panel is a real second-tier test not in the initial labs (autoimmune or
  paraneoplastic panel, served by a follow-up); else delete.
- Drug-check outputs and expected texts that are treatment plans (M09, P05, P08, S04, S06, S10,
  S11, S12) become T-DDI content.

### C5. Orphan follow-ups and contradictory LP (PATTERNS contradictions; notes aeb5068c S07, 7fb2fc52 S08, fc4e7dc6 S06)
- Delete `request_lp_autoimmune` CSF follow-ups with no criterion: P05, P07, RS11, S01, S02, S03,
  S05, S06 (its "slightly xanthochromic" with 0 RBC goes with it), S07, S08, S09, S10.
- Orphan autoimmune-panel lab follow-ups (M02, M04, M07, P04, P08): delete; none of these needs a
  second-tier antibody panel.
- Other orphans to delete: M01 advanced_imaging "paraneoplastic_cancer_search"; M05 pelvic
  advanced_imaging (the body imaging criterion covers it); P02 psychology literature, P02 MRI
  follow-up if MRI stays optional with no criterion output, P02 serial prolactin (prolactin goes
  into the initial labs, see section 4); P04 tPA drug check; P05 intermediate syndrome; S11
  hyperkalemia drug check; P06 palliative literature and "ECG (QTc)" lab panel (wrong tool); S12
  "LGI1 antibody (CSF)" inside serum labs (wrong tool; move to the CSF output); RS11 serial
  troponin; M08 toxoplasma serology (attach to the second-tier labs criterion, see section 4).
- LP as avoided action: S07 `analyze_csf` severity `contraindicated` (mass with 4 mm midline
  shift); S08 and P07 `harm`. S08 rationale must not say "abnormal coagulation" (INR 1.0): "LP is
  not indicated: the seizures are explained by eclampsia, and platelets are 88 x10^9/L in HELLP."
  The S07 MRI-before-CSF hard constraint is already absent (aeb5068c ALREADY-FIXED in part).

### C6. Laterality (PATTERNS internal consistency; notes 0bc30365 S03, 4ccf5d55 S09, 19c53320 S12)
Apply 1.2 Lateralization. Per case:
- S03: right MCA lesion, so ictal EEG right-hemisphere predominant evolving to bilateral; ictal
  gaze leftward; delete "contralateral activation pattern".
- S09: left temporal focus; CC and HPI "left-sided" clonic activity become "right-sided"; ictal
  gaze rightward.
- S12: left temporal focus; FBDS move to the right face and arm in CC, HPI, exam and outputs.
- S07: right frontal glioblastoma, right frontal (F4) onset; CC and HPI "right arm" become "left
  arm"; the leftward ictal gaze is already correct.
- M02: right temporal glioblastoma; ictal gaze leftward; left-sided weakness and extensor plantar.
- M03: left temporal (T3-T5) NCSE; the intermittent "left gaze preference" becomes rightward
  ictal deviation.
- M04: rightward gaze matches a left-hemisphere post-stroke focus; the EEG "GPDs on the right
  hemisphere", "right > left" is a contradiction: GPDs are generalized; rewrite as GPDs with left
  predominance or as left LPDs, matching the exam.
- M09: right frontoparietal SDH, right temporoparietal NCSE; "3+ right" reflexes and the right
  extensor plantar move to the LEFT (the left arm drift is already correct); ictal gaze leftward.
- P01: right temporo-occipital focus (T4-O2); the ictal "right eye deviation" becomes leftward in
  HPI, exam and EEG; the left facial droop is already correct.
- P03: bursts are left-hemisphere predominant, so the periodic arm flexion and facial twitching
  move from the left to the right arm and face.
- P04: left MCA stroke; facial droop and weakness on the right in exam and HPI.
- M01: keep the left gaze preference as a red herring, fix its ADD line to say why it does not
  lateralize; delete "left arm restlessness".
- M06: consistent; no change.
Imaging and EEG are the anchor; signs move, the lesion does not.

### C7. Patient block leaks (style guide; PATTERNS leaks)
- Chief complaint states EEG results: P01, P02, P03, P04 ("GPDs" is also wrong; the EEG shows
  LPDs), P07, P08. Rewrite as the presenting problem.
- HPI quotes the expected EEG read: P03, P04, P05, P07. Remove.
- Exam leaks: M04 "hyponatremia present"; RS11 "levetiracetam UNDETECTABLE". Remove.
- Prior pre-encounter results stay (they are history): P06 prior EEG and MRI, S12 prior LGI1
  titre, S08 prior lamotrigine level, M09 prior INR.
- Reports doing the agent's work: M01 and M02 ECG "safe to load (second-line) AED" becomes a plain
  ECG read; S08 MRI "confirms PRES not infarction" becomes the finding (no diffusion restriction,
  vasogenic edema); P02 prolactin reference range "expected >36 ... post-GTCS" becomes a plain
  range; RS11 EEG "expected JME interictal baseline" and "characteristic of idiopathic generalised
  epilepsy" become descriptions; P01 EEG "IIC criterion met" becomes the ACNS description; P08 EEG
  must not report response to lorazepam or fosphenytoin unless the HPI says they were given (it
  does: keep as history in the HPI, not in the EEG).

### C8. Literature (ruling 5; leak guard)
Every literature criterion becomes `optional`, leaves `required_before_assessment`, and its
follow-up goes last. Delete every initial `literature_search` and the fallback literature outputs
with engineering text; rewrite remaining outputs per T-LIT. Specific content:
- S08: delete "nimodipine teratogenic" (note 09924507), fabricated delivery thresholds, and
  "lamotrigine >6"; use the eclampsia facts in 1.2.
- S04: valproate is withheld in valproate-associated hyperammonemic encephalopathy, with
  L-carnitine [Lheureux_2009] (note efb6cbfc).
- S03 and S06: sodium per 1.2 (note 5ff3c70f): drug-check and literature outputs say the same
  limit as the musts.
- S02: two literature criteria; keep one (optional).

### C9. Drug check (ruling 6; leak guard)
Tier by concrete interaction that changes management:
- Required: M02 (dexamethasone and enzyme-inducing ASM), M04 (carbamazepine SIADH, switch), M07
  and P03 (amiodarone and phenytoin), M08 (antiretrovirals or pyrimethamine and enzyme inducers),
  M09 (warfarin with ibuprofen and with ASMs), P07 (hepatic dosing; avoid valproate), S02 (prior
  phenytoin SJS), S04 (valproate, carbamazepine SJS allergy), S06 (MDMA, serotonergic drugs), S08
  (magnesium with labetalol or nifedipine; lamotrigine in pregnancy), S09 (clarithromycin and
  carbamazepine), S10 (TCA and sodium-channel ASMs), S11 (renal dosing and dialysis removal of
  levetiracetam).
- Recommended: M03, M06, P04, P05, P06, P08, RS11, S01, S03, S05, S07.
- Optional: M01, M05, P01, P02, S12.
Content fixes: S07 enzyme inducers lower dexamethasone exposure (not temozolomide; she is on
bevacizumab); M07 and P03 phenytoin does not prolong QT: the risk is hypotension, bradycardia and
AV block during loading, and amiodarone inhibits phenytoin metabolism via CYP2C9 (raising levels);
S02 adds a prohibition of phenytoin and fosphenytoin (documented SJS); S04 carbamazepine SJS
allergy: avoid aromatic ASMs (phenytoin, fosphenytoin, carbamazepine, oxcarbazepine, lamotrigine
loading not relevant acutely). Delete every initial `drug_interactions` "general" output and
fallback drug outputs with engineering text ("agent not specified on this case's pathway").

### C10. Case fallbacks
Delete per-case `advanced_imaging` and `specialized_test` fallbacks whose values are not
vocabulary or do not match the tool ("MRI brain", "CT chest", "fetal_monitoring",
"transcranial_doppler" under specialized_test, and similar); the library answers. Make the ECG,
Holter and echo fallbacks consistent with the patient: M04 and M09 atrial fibrillation; M07
post-MI with ICD (paced or with Q waves as the history says); P03 post-arrest findings.

### C11. Avoided-action text
The polysomnography entry carries the DaTscan rationale in 23 cases: replace with T-PSG. Remove
unbracketed duplicate citations ("Brophy_2012" beside "[Brophy_2012]", at least M01 and one other
case) everywhere in the case.

### C12. Stop rule
`max_additional_actions` is 0 in all 30: set 1. `required_before_assessment` is exactly the
required criteria after this round.

### C13. Sequence constraints
- CT before CSF `hard` in every case with a CSF criterion (M01, M03, M04, M05, M06, M08, P01, P06,
  P08, S04, S12); add it to P08. Keep MRI before CSF `hard` in M08 (ring-enhancing lesions).
- Labs before drug check: `soft` and only where renal, hepatic or level data change the choice
  (M04, M06, M09, P07, S09, S11); delete elsewhere.
- ECG before drug check: `hard` becomes `soft` (S10 stays `hard`: phenytoin with QRS widening is
  unsafe). P02 EEG before drug check: `soft`. Delete P04 MRI before drug check.
- No constraint involving literature.

### C14. Differential not updated (ruling 7)
Rank every entry against the whole work-up, including follow-ups that remain. Known cases: P01 HSV
and seronegative autoimmune encephalitis "high" become low (negative PCR, anti-Hu positive);
alcohol withdrawal low. M01 stroke and HSV low. M04 UTI-precipitated seizure low (negative
cultures and procalcitonin). M02 sepsis low. RS11 delete "BAL pending" (the tox screen reports
ethanol). Each `key_features` names the result that rules it in or out.

### C15. Clinical and data errors (per case)
- S03 (note 5ff3c70f): Na 129 is not severe and rarely causes SE: set Na 121 (with a plausible
  serum osmolality and urine studies), update `accepted[0]` "(Na 129)" to "(Na 121)" as an
  entity that is not real otherwise (log, CENTRAL 3). Musts, drug check and literature give the
  limits in 1.2 (10 in 24 h; 8 if high risk); she is 72 with dehydration, not high-risk by
  default.
- M04 (note 0afbb493): Na 132 cannot cause NCSE: set Na 123, update `accepted[0]` "(Na 132)" to
  "(Na 123)" (log, CENTRAL 3); a 3% saline must then fits (1.2); delete "Treat UTI empirically";
  red herring on 37.6 C rewritten: "Temperature 37.6 C is not a fever; cultures and
  procalcitonin are negative."
- M03 (note adc24e17): "prednisone 30 mg daily, day 10 of a taper" everywhere; delete
  "low-dose" and "high-dose"; differential entry says steroid-associated hypertension, not
  "high-dose steroid".
- S04 (notes efb6cbfc, f6c10984): add prednisone (dose from the HPI, else 40 mg daily) to the
  medication list; delete the "VPA post-IV loading 82" panel (ruling 4; she must not receive
  valproate); literature per C8.
- S01 (note 35db0801): MRI report becomes normal (no mesial temporal DWI or FLAIR change); MRI
  optional; expected text "normal".
- P01 (note 53545e21): delete the FDG-PET criterion and follow-up (CT already shows a 4.2 cm
  hilar mass); add a must: "Arrange tissue diagnosis of the hilar mass (EBUS-guided or
  bronchoscopic biopsy) with oncology [Graus_2021]." Optionally an `obtain_tissue_diagnosis`
  `lymph_node_biopsy` criterion, recommended, with a pathology output (small cell carcinoma).
  "NASH" with heavy alcohol use becomes "alcohol-related steatosis".
- S08 (note 09924507): see C8; haptoglobin low; musts per 1.2 (magnesium with renal caution,
  severe-range BP treatment, delivery after stabilization with obstetrics, continuous fetal
  monitoring).
- M07 (note e89c4880 and survey): arrest 5 days earlier, discharged on day 4: delete "Maintain
  targeted temperature management goals"; musts per 1.2 post-arrest (re-arrest work-up,
  multimodal prognostication, ASM); delete the "additive QT prolongation" prohibition rationale
  (C9).
- M05: CSF criterion `special_tests` uses `NMDAR_antibodies` (not oligoclonal bands); pelvic
  imaging alternatives `pelvis_abdomen_MRI`, `pelvis_abdomen_ultrasound`, `pelvis_abdomen_CT`;
  deduplicate the haloperidol items (one prohibition: neuroleptics worsen NMDAR encephalitis and
  risk NMS).
- P02: prolactin is diagnostic: initial labs report prolactin at baseline range 20 minutes after
  the event (normal values do not exclude epileptic seizures; LaFrance_2013); include it in
  T-LABS extras.
- P05 and P07 labels contain a future or treatment clause (P05 "complicated by intermediate
  syndrome at 48 hours"; P07 "resolving with ammonia correction"); keep the labels, no 48-hour or
  post-treatment outputs; CENTRAL 3 proposes the label trim.

---

## 3. Target pathway and tiers

### 3.1 `action_criteria` order and tiers (keep ids)

1. Core labs (T-LABS), required, all 30. In infection cases (M06, P07, S03, S04, S05) the
   microbiology criterion follows the labs.
2. Non-contrast CT (T-CT), required, all 30.
3. EEG (T-EEG), required, all 30. (Order labs, CT, EEG reflects stabilize-and-image while cEEG is
   set up; none is a hard constraint.)
4. ECG where it changes the ASM: required S10, S11 (placed right after labs), M07, P03;
   recommended S09, P04; optional M01, M02. Others have no ECG criterion.
5. MRI: required M01, M02, M03, M05, M06, M08, P01, P04, P06, S02, S04, S05, S07, S08, S12;
   recommended M04, M07, M09, P03, P07, S11; optional P02, RS11, S01, S03, S06, S09. S10 none.
6. CSF: required M01, M03, M05, M06, M08, P01; recommended P06, S04, S12; optional M04, P08.
7. Second-tier antibody or infection labs: required M01, M05, P01, S12 (paraneoplastic or
   autoimmune panel), M08 (toxoplasma serology and HIV studies); recommended M03, S02, S04.
8. Body or pelvic imaging: M01, M05 required; P01 required (chest CT).
9. Other studies: M07 and P03 SSEP (`order_specialized_test`) per 1.2, recommended in M07,
   required in P03; P04 CTA (advanced imaging) recommended and echo recommended; P05 `respiratory_function`
   recommended (cholinesterase is CENTRAL 2);
   microbiology per C3; P01 tissue diagnosis recommended if added.
10. Drug check, tier per C9.
11. Literature, optional, last.

### 3.2 Follow-ups

Same order as the criteria. Initial outputs: labs, CT, EEG (and ECG where required); no initial
`literature_search` or `drug_interactions`. A follow-up exists only to answer a criterion or a
plausible diagnostic order; no follow-up reports a treatment effect. Triggers must not share a
meaningful token with the core EEG or lab orders (C4).

### 3.3 Sequence constraints: section 2 C13.

### 3.4 Stop rule and avoided actions: C12; polysomnography per C11; LP per C5.

---

## 4. Per-case index

Notes are full ids; "C" refers to section 2. Every case also gets: C1, C4 (delete
`request_aed_optimization` and the post-treatment cEEG follow-up where present), C8, C9 tier,
C10, C11, C12, C13, C14 and section 3. Below are the case-specific items.

### SE-M01 (man 65, NCSE, anti-Hu limbic encephalitis, suspected SCLC; no notes)
- C3 delete blood cultures a12. C9 optional. C5 delete "paraneoplastic_cancer_search".
- C6 keep left gaze preference as red herring, fix its ADD line; delete "left arm restlessness".
- C7 ECG "safe to load second-line AED" becomes a plain read. C14 stroke and HSV low.
- Leak guard fails (initial drug or literature output). Literature a9 optional.

### SE-M02 (man 58, NCSE, glioblastoma recurrence with edema; no notes)
- C3 delete a9 blood cultures. C5 delete orphan autoimmune-panel follow-up.
- C6 ictal gaze leftward; left-sided weakness and extensor plantar.
- C7 ECG "safe to load AED". C9 required (dexamethasone, enzyme inducers). C14 sepsis low.
- MRI follow-up "Expected encephalomalacic changes" becomes a finding without "expected".

### SE-M03 (woman 42, NCSE, PRES from hypertension, on prednisone taper; R2 approved)
- 0aed33a9-15ce-4875-9146-967f896dbe63: C1 (urinalysis keeps 2+ protein and RBC casts in its own
  panel; the duplicate autoimmune entries go), FIXED.
- adc24e17-c7b6-435c-85e7-0c0285ac63ae: C15 (prednisone 30 mg, day 10 of a taper), FIXED.
- C2 keep beta-hCG negative. C6 ictal gaze rightward. C9 recommended. Antibody panel recommended.
- Duplicate lab a6: keep only if it is a second-tier panel with its own follow-up.

### SE-M04 (man 71, NCSE, carbamazepine SIADH, post-stroke focus; R2 approved)
- 0afbb493-4142-40fd-8184-68d92edcaae5: C15 (delete "Treat UTI", UTI low in the differential,
  red herring rewritten) and C3 (urine culture recommended, negative), FIXED. Na 132 to 123 with
  label update (C15, CENTRAL 3).
- C5 delete orphan autoimmune-panel follow-up. C6 gaze rightward; EEG GPD contradiction.
- C7 exam "hyponatremia present" removed. C10 ECG AF. Leak guard fails (literature).
- CSF optional; MRI recommended; drug check required.

### SE-M05 (woman 34, NMDAR encephalitis with NCSE, right ovarian teratoma; no notes)
- C1 Mimic exclusion block too; oligoclonal_bands out of serum labs. C2 keep beta-hCG.
- C3 blood cultures recommended (39.1 C, HR 114): case text, no `before_antimicrobials`, no growth.
  C5 delete pelvic advanced imaging.
- C15 CSF `NMDAR_antibodies`, pelvic imaging alternatives, one haloperidol prohibition.
- Leak guard fails. C9 optional. Antibody panel required.

### SE-M06 (man 66, HSV-1 encephalitis with right temporal NCSE, on TMP-SMX; R2 approved)
- b1f48e5f-741d-47db-9b1d-6de79c73e787: C3 (blood cultures recommended, `before_antimicrobials`
  removed, output says drawn on TMP-SMX day 12), FIXED.
- C1 cytology and autoimmune_panel out of serum labs (into the CSF report). C6 no change.
- Labs before drug check soft (renal acyclovir dosing). C9 recommended. Lab a9 optional: delete
  if duplicate.

### SE-M07 (woman 55, post-anoxic NCSE, OHCA 5 days earlier, ICD, amiodarone; R2 approved)
- e89c4880-d209-4f46-9f12-bdb7fef8c30e: C3 delete blood cultures a10 (afebrile, WBC 9.4), FIXED.
- C15 delete TTM must; post-arrest musts per 1.2; C9 required with corrected
  phenytoin-amiodarone content; delete the QT prohibition rationale.
- MRI recommended; SSEP a5 recommended; ECG a8 required; C10 ECG fallback post-MI with ICD.
- C5 delete orphan autoimmune-panel follow-up. NSE output only if CENTRAL 2 adds the term.

### SE-M08 (man 48, CNS toxoplasmosis reactivation with NCSE and head injury; no notes)
- C3 delete blood cultures a10. Duplicate lab a5 folded into T-LABS or turned into the
  second-tier toxoplasma serology and HIV studies criterion served by the toxo follow-up (C5).
- EBV CSF PCR moves into the CSF report as a free-text result only if the CSF tool vocabulary
  allows it; else drop (CENTRAL 2 `EBV_PCR`). MRI before CSF hard stays. C9 required.

### SE-M09 (woman 77, acute-on-chronic SDH, NCSE, INR 4.8 from ibuprofen-warfarin, UTI, hyponatremia; no notes)
- C4 delete "Coagulation After Reversal" follow-up, a9 "treat UTI" (becomes a must), duplicate
  a6. Urine culture a10 required.
- C6 reflexes and plantar to the left, gaze leftward. Prior INR stays (C7).
- C9 required (T-DDI, not reversal plan; reversal is a must per [Frontera_2016]). C10 AF fallback.
- MRI recommended. Labs before drug check soft.

### SE-P01 (man 52, anti-Hu limbic encephalitis, IIC, suspected SCLC; R2 approved)
- 53545e21-f6fc-4235-912f-ae1e080a0b63: C15 (delete FDG-PET criterion a8 and follow-up; tissue
  diagnosis must), FIXED.
- 0dd7682a-cb97-468f-8bab-2d62f60d883a: C3 delete blood cultures a13 (afebrile, on acyclovir),
  FIXED.
- C2 remove beta-hCG. C4 delete "thiamine optimization"; keep the benzodiazepine-trial follow-up
  with trigger "benzodiazepine_trial". C6 gaze. C7 CC and EEG "IIC criterion met". C14.
- C15 "alcohol-related steatosis". C9 optional. Leak guard fails.

### SE-P02 (woman 38, prolonged PNES with comorbid JME on lamotrigine; no notes)
- C7 CC states EEG result. Event capture merged into the initial EEG (video-EEG, no
  electrographic correlate, normal background).
- C15 prolactin in the initial labs; delete serial prolactin, psychology literature and MRI
  follow-ups (MRI optional). C2 keep beta-hCG. C9 optional; EEG before drug check soft.
- Prohibition: escalation to anaesthetic infusion or intubation for PNES [LaFrance_2013].

### SE-P03 (man 62, post-anoxic myoclonic SE, burst suppression, propofol, hypothermia; no notes)
- C4 keep the propofol-weaning follow-up with trigger "sedation_wean"; delete other post-treatment
  cEEG. C6 myoclonus side matches the bursts. C7 CC and HPI EEG quotes.
- C9 required (amiodarone if listed; propofol with ASMs). SSEP a5 required; ECG a10 required;
  MRI recommended; duplicate lab a7 deleted. Prognostication timing per 1.2. C10 fallbacks.

### SE-P04 (woman 44, acute left MCA stroke with LPDs on the IIC; no notes)
- C7 CC "GPDs" (wrong and a leak) and HPI EEG quote. C6 right facial droop and weakness.
- C4 delete "AED Level Post-Loading"; C5 delete orphan autoimmune panel and tPA drug check.
- C13 delete MRI before drug check. ECG and echo and CTA recommended. C9 recommended. Leak guard
  fails. Musts: stroke care per [AHA_Stroke_2019]; LPDs alone on the IIC: an ASM trial is
  reasonable, anaesthetic escalation is not [ACNS_2021; Brophy_2012].

### SE-P05 (man 29, organophosphate cholinergic toxidrome with seizures; no notes)
- C4 delete a8 (cholinesterase recovery), `request_aed_optimization`, intermediate-syndrome
  follow-up. C5 delete the CSF follow-up. C7 HPI EEG quote. Specialized test a7
  (`respiratory_function`) stays recommended: baseline FVC and negative inspiratory force now, with
  the output reporting today's values only (no 24 to 96 hour course).
- Musts per [Eddleston_2008]. Drug check recommended (avoid succinylcholine, which is prolonged).
  Label kept (CENTRAL 3). Cholinesterase is CENTRAL 2.

### SE-P06 (woman 67, sporadic CJD with superimposed left temporal NCSE; no notes)
- C1 Mimic exclusion block; HSV_PCR out of serum labs (into the CSF report). C3 delete
  blood cultures a10. C5 delete palliative literature and "ECG (QTc)" lab panel.
- Prior EEG and MRI stay in the history. CSF recommended (RT_QuIC, 14_3_3_protein, total_tau)
  [Hermann_2021]. C9 recommended. Follow-up "CJD background unchanged as expected" goes with C4.

### SE-P07 (man 74, hepatic encephalopathy, Child-Pugh C, SBP, triphasic waves; no notes)
- C3 ascitic fluid required early; blood cultures recommended; delete the "Blood Culture E. coli"
  lab panel. C4 delete a7 (SBP treatment, into musts per [AASLD_ascites_2021]), duplicate a6,
  "Ammonia After Treatment", "Ascitic fluid at 48h". C5 delete CSF follow-up; LP `harm`.
- C7 CC and HPI EEG. C9 required (avoid valproate; hepatic dosing). Labs before drug check soft.
- Musts: lactulose and rifaximin [Vilstrup_2014], albumin in SBP [EASL_decomp_2018]. Label kept
  (CENTRAL 3).

### SE-P08 (woman 31, isoniazid toxicity with refractory SE; no notes)
- C4 delete a7 (bicarbonate) and the isoniazid level (reference-lab result) output. CT before
  CSF hard added (C13). CSF optional. C5 delete orphan autoimmune follow-up.
- C7 CC states EEG; EEG must not report drug response (C7). C2 keep beta-hCG. C9 recommended.
- Musts per 1.2 (pyridoxine, benzodiazepine; phenytoin ineffective, as a prohibition).

### SE-RS11 (man 36, GCSE from levetiracetam non-adherence in JME, sleep deprivation; R2 approved)
- e610cd86-6e11-463e-badd-26edb62f9147: C3 delete blood cultures a8; 38.1 C explained by
  T-HYPERTHERMIA; HPI states normal temperature before the seizure, FIXED.
- 64b7befa-8b73-42ea-82cc-dd9f718691ea: C2 remove beta-hCG, FIXED.
- C5 delete CSF follow-up and serial troponin; troponin in labs coherent (C1). C7 exam
  "levetiracetam UNDETECTABLE" removed; EEG wording. C14 delete "BAL pending".
- MRI optional; lab a7 optional: delete if duplicate. C9 recommended.

### SE-S01 (man 32, GCSE from subtherapeutic valproate in JME; R2 approved)
- 35db0801-2557-4c9e-8ec5-18728e2ff75b: C15 MRI normal and optional, FIXED.
- 138b30a5-840a-4ab0-a7a4-5e85454eef99: C2 remove beta-hCG, FIXED.
- C3 delete the template urine microbiology a9. C4 delete duplicate a7. C5 delete CSF follow-up.
- Leak guard fails. C9 recommended.

### SE-S02 (woman 28, focal SE with bilateral spread, right TLE, hippocampal sclerosis; no notes)
- C8 keep one literature criterion (optional). C9 required; add the phenytoin and fosphenytoin
  prohibition (prior SJS). C2 keep beta-hCG. Antibody lab a7 recommended. C5 delete CSF follow-up.
- ICD G41.2 for a convulsive focal-to-bilateral SE (CENTRAL 3).

### SE-S03 (woman 72, GCSE from hyponatremia with UTI, post-stroke epilepsy; R2 needs changes)
- 54e2cb28-c7c9-4689-9691-01eb5d96bb24: C1 (Exclusion block deleted; urinalysis abnormal once),
  FIXED.
- 5ff3c70f-1fdf-4429-a3ab-d42da89c191e: C15 sodium limits consistent in musts, drug check and
  literature; Na 121 with label update, FIXED.
- 59001cc7-8a23-4b60-a60b-d4b00245492f: C3 urine culture required without
  `before_antimicrobials`, positive E. coli resistant to TMP-SMX; blood cultures recommended,
  FIXED.
- 0bc30365-55ba-4b61-b412-c7fda6cef28a: C6 right-hemisphere EEG, leftward gaze, invented term
  removed, FIXED.
- C4 delete a7 (UTI antibiotics into a must). C5 delete CSF follow-up. MRI optional. C9
  recommended.

### SE-S04 (woman 45, GCSE, subtherapeutic valproate and valproate hyperammonemia, SLE on prednisone; R2 needs changes)
- efb6cbfc-69ba-442d-92c8-460dd15d8e14: delete the "VPA post-IV loading 82" panel; literature
  says withhold valproate and give L-carnitine [Lheureux_2009]; prohibition of valproate stays,
  FIXED.
- f6c10984-e730-4cad-9723-22936efdabd2: C1 (Exclusion block deleted; SLE panel values stand),
  FIXED.
- Add prednisone to the medication list (C15). C3 add blood cultures recommended (febrile,
  immunosuppressed). C9 required with the carbamazepine SJS allergy. CSF recommended. Antibody
  panel recommended. Duplicate a9 deleted. C2 keep beta-hCG. Leak guard fails.

### SE-S05 (man 58, alcohol withdrawal SE with Wernicke encephalopathy; no notes)
- C1 thiamine low in its panel (not "within range"). C4 delete duplicate a7 and
  `request_aed_optimization`. C5 delete CSF follow-up. Blood cultures a9 recommended.
- Musts: thiamine per [EFNS_Wernicke_2010] before or with glucose; benzodiazepines. Leak guard
  fails. C9 recommended.

### SE-S06 (man 24, MDMA SE with Na 124, hyperthermia, serotonin syndrome; R2 approved)
- fc4e7dc6-33ac-4f40-895d-807c185627f5: C5 delete the orphan CSF follow-up (xanthochromia with 0
  RBC), FIXED.
- C2 remove beta-hCG. C4 delete a6 (rhabdomyolysis management, into musts). Sodium per 1.2.
- C9 required (T-DDI). MRI optional. Musts per [Boyer_2005] and [Spasovski_2014].

### SE-S07 (woman 68, focal SE with spread, subtherapeutic levetiracetam, peritumoral edema; R2 approved)
- aeb5068c-eaea-42f6-af39-49f7b7c11740: C5 delete the CSF follow-up; add avoided `analyze_csf`
  `contraindicated`; the MRI-before-CSF hard constraint is already absent, FIXED.
- C2 remove beta-hCG. C6 left arm. C9 recommended with the dexamethasone
  (not TMZ) interaction. ICD G41.2 (CENTRAL 3).

### SE-S08 (woman 35, 28 weeks, eclampsia with HELLP and breakthrough epilepsy, low lamotrigine; R2 needs changes)
- 7fb2fc52-87d3-4104-a2e3-b6460207a16c: C5 delete the CSF step; add avoided `analyze_csf` `harm`
  with the corrected rationale, FIXED.
- 09924507-a7db-44f6-865e-303eb0ed1c34: C8 delete the nimodipine line and the fabricated
  thresholds, FIXED.
- C2 remove beta-hCG. C1 haptoglobin low. C7 MRI "confirms PRES". C10 delete "fetal_monitoring"
  fallback. Musts per 1.2 eclampsia. C9 required. MR venography a8 stays optional (venous
  sinus thrombosis is a pregnancy differential). Prior lamotrigine level stays.

### SE-S09 (man 52, carbamazepine toxicity from clarithromycin, left temporal epilepsy; R2 approved)
- 4ccf5d55-1293-4b28-9225-d7ff7e5a84a9: C6 right-sided clonic activity and rightward gaze, FIXED.
- C5 delete CSF follow-up. MRI optional. ECG recommended. C9 required. Labs before drug check
  soft. ICD G41.2 (CENTRAL 3).

### SE-S10 (man 19, TCA and MDMA toxicity with QRS widening; no notes)
- C2 remove beta-hCG (label "here male, n/a" goes too). ECG a4 right after labs; ECG before drug
  check stays hard. C4 delete a7. C5 delete the CSF follow-up ("serum tox confirms TCA").
- C9 required. Musts per 1.2 TCA; prohibition phenytoin and fosphenytoin.

### SE-S11 (man 61, uremic SE after missed hemodialysis, K 6.8; no notes)
- ECG a4 right after labs, required. C5 delete the hyperkalemia drug check follow-up. C9
  required (renal dosing; dialysis removes levetiracetam). Labs before drug check soft.
- MRI recommended. Musts: urgent hemodialysis, hyperkalemia treatment. Leak guard fails.

### SE-S12 (woman 47, FBDS status from anti-LGI1 relapse during prednisone taper; R2 needs changes)
- 5daa0f16-4a86-4afc-bc36-0d89ba15c089: C3 delete blood cultures a9 (afebrile, WBC 7.8), FIXED.
- 19c53320-5fe4-4264-a98f-32347a37ef93: C6 FBDS on the right face and arm, FIXED.
- C5 "LGI1 antibody (CSF)" leaves the serum labs (into the CSF report). CSF a5 recommended (LGI1
  CSF is often normal; serum is the sensitive test [Irani_2011]). Antibody panel required. C9
  optional. Prior titre stays. Leak guard fails. ICD G41.2 for FBDS (CENTRAL 3).
- Musts: high-dose steroids (IV methylprednisolone) for the relapse [Graus_2016]; ASMs alone
  rarely control FBDS [Irani_2011].

---

## 5. CENTRAL requests

1. Criteria pack `dataset-generation/criteria_packs/SE.md`: allow-list the keys in 1.1 "To add";
   replace "literature required" and "drug check required" with rulings 5 and 6; add the
   canonical facts of 1.2 (lateralization, hyponatremia limits, post-arrest prognostication
   timing, blood cultures only with suspected infection, beta-hCG only in women of reproductive
   age); remove the template blood-culture block and the Exclusion studies block from the
   generator for SE.
2. Vocabulary (`costs.yaml` and the `tool_io.py` mirror): lab `cholinesterase` (plasma and RBC)
   for P05; lab `NSE` for M07 and P03 (ERC-ESICM prognostication); CSF special test `EBV_PCR`
   for M08. No `isoniazid_level`: P08 is diagnosed clinically.
3. Labels and codes: (a) S03 `accepted[0]` "(Na 129)" to "(Na 121)" and M04 "(Na 132)" to "(Na
   123)", changed by the workers as entities that are not real at those values; refresh
   synonyms. (b) S02, S07, S09 (focal to bilateral convulsive SE) and S12 (FBDS status) carry
   G41.2 (complex partial SE) first with NCSE synonyms: recode to G41.8 (S12, S02 if focal
   impaired awareness predominates) or G41.0 (S07, S09), and prune NCSE synonyms. (c) P05 and P07
   labels: trim the future or treatment clause ("complicated by intermediate syndrome at 48 hours";
   "resolving with ammonia correction"); the P04 and P07 synonym prune already pending in
   CENTRAL_PENDING stays.
4. Generator template: the cEEG follow-up trigger `request_continuous_eeg_monitoring` shares a
   token with `eeg_type` `continuous_icu` and hijacks the EEG criterion; the matcher could
   exclude enum tokens of the core order from follow-up matching, or the generator must not emit
   such triggers.
5. Review UI: show initial outputs and follow-ups in criterion order (already requested).

## 6. Open questions for Andrea

None that need information only Andrea has. Decided here, for the record: label number changes in
S03 and M04 are made in the case and listed in CENTRAL 3; ICD recodes are central (CENTRAL 3b),
not worker edits; P05 and P07 labels are kept by the workers and their trim is a central
proposal.
