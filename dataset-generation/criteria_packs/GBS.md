# Criteria pack: Guillain-Barré Syndrome (GBS)

**ICD-10:** G61.0 (ICD-10 files every GBS variant, Miller Fisher syndrome included, under G61.0)
**Condition enum:** `NeurologicalCondition.GUILLAIN_BARRE`
**Case ID prefix:** `GBS`

Updated 24 Oct 2026 to the rulings of the October 2026 physician-review round
(`data/review/round-2026-10/plans/GBS.md`, `GBS-summary.md`) and to the decisions on its open
questions (`plans/GBS-decisions.md`).

---

## 1. Diagnostic criteria and governing sources

**Which source governs what:**

- Diagnosis, tests, immunotherapy, respiratory monitoring: EAN/PNS 2023 [EAN_PNS_2023] (GRADE
  recommendations on treatment, good practice points on diagnosis and monitoring).
- Levels of diagnostic certainty: Brighton 2011 [Brighton_2011], the only certainty scheme a case
  may quote, at most once per case and consistent with the data.
- Variant definitions: Wakerley 2014 [Wakerley_2014].
- Miller Fisher syndrome (MFS) management: EAN/PNS 2023 does not address it; cite Leonhard 2019
  [Leonhard_2019] (treatment generally not recommended in pure MFS; monitor for overlap).
- Respiratory thresholds: the 20/30/40 rule is Lawn 2001 [Lawn_2001]; EAN/PNS 2023 adds the >30%
  FVC fall, SBC <20, FVC <=20 mL/kg for elective ventilation, and FVC <60% predicted as a predictor
  of ventilation (section 5).
- Checkpoint inhibitor-related GBS only: ASCO 2021 [Schneider_2021] and ESMO 2022 [Haanen_2022].

**Required features** [EAN_PNS_2023, Brighton_2011]: progressive, bilateral, relatively symmetric
weakness of the limbs (legs only in the paraparetic variant; none in MFS and the cranial variants),
with decreased or absent reflexes in the weak limbs; nadir between 12 hours and 28 days (write
"within 4 weeks"). Progression beyond 4 weeks is not GBS; beyond 8 weeks, or 3 or more
treatment-related fluctuations, is acute-onset CIDP.

**Red flags** that call for an alternative or for imaging [EAN_PNS_2023, Leonhard_2019]: sensory
level, extensor plantars, hyperreflexia, marked persistent asymmetry, bladder or bowel dysfunction
at onset, fever at onset, CSF cells >50/mm3, severe pulmonary dysfunction with little limb
weakness, severe sensory signs with little weakness, nadir <24 h, progression >4 weeks, reduced
consciousness (except in Bickerstaff brainstem encephalitis).

**CSF:** albuminocytological dissociation (raised protein, cells usually <5/mm3; 5-50/mm3
compatible but prompts consideration of an alternative; >50/mm3 suggests another diagnosis).
Protein may be normal in the first week.

**Electrodiagnosis** supports the diagnosis and may be normal in the first week (a repeat at 2-3
weeks is an assessment recommendation, never a stored result). Subtyping (AIDP, AMAN, AMSAN) is
not advised for routine decisions [EAN_PNS_2023]; a subtype word appears in a label only where the
case's own NCS numbers meet it.

**Variants** [Wakerley_2014]: MFS (ophthalmoplegia, ataxia, areflexia, no limb weakness);
incomplete MFS (acute ophthalmoparesis, acute ataxic neuropathy, acute ptosis); pharyngeal-
cervical-brachial (PCB: oropharyngeal, neck and arm weakness with arm areflexia, legs spared);
bifacial weakness with paraesthesias (no limb weakness); paraparetic. Brighton levels do not apply
to a patient without limb weakness.

## 2. Standard workup hierarchy

Canonical criterion order (the review app reads it as the work-up sequence): NCS/EMG, CSF,
mimic-exclusion criteria the case raises, labs, respiratory function, telemetry, ECG, drug
interaction check, literature. A case puts an earlier step first only for a logged safety reason
(brain MRI before LP for a posterior fossa stroke question, spine MRI before LP near a fresh
laminectomy, respiratory function first in a desaturating patient, labs and the drug check before
the LP when coagulation or antithrombotics are at issue).

**Required:**
- `order_specialized_test` (`test_type: emg_ncs`): "Nerve conduction studies and needle EMG";
  polyradiculoneuropathy pattern (demyelinating or axonal features, absent F-waves, sural sparing
  where present); may be normal in the first week [EAN_PNS_2023]
- `analyze_csf` (`{}`; `special_tests: [cytology]` only where the case needs it, e.g. HIV,
  leukaemia): cells, protein, glucose with a CSF:serum ratio consistent with the serum glucose;
  culture "no growth to date" [EAN_PNS_2023]. Recommended instead of required only where the LP is
  conditional (anticoagulation that cannot be stopped, RS16)
- `interpret_labs` (`panels: [CBC, CMP, CK]`, plus `coagulation` where C13 applies, `troponin`
  for checkpoint inhibitor overlap): baseline full blood count, renal function and electrolytes,
  liver tests, albumin, glucose and CK; abnormal liver tests or low albumin mark a higher risk of a
  severe course [EAN_PNS_2023]. `clinical_significance: null` on routine analytes
- `order_specialized_test` (`test_type: respiratory_function`): FVC in L, % predicted and mL/kg,
  MIP and MEP, with the trend, repeated serially while weakness progresses [Lawn_2001,
  EAN_PNS_2023]
- `order_cardiac_monitoring`: continuous telemetry with blood pressure monitoring; the report covers
  the first 24 hours, findings only [EAN_PNS_2023]

**Recommended:**
- `analyze_ecg`: baseline 12-lead ECG (rate, rhythm, QTc read against the sex-specific normal)
- Mimic-exclusion criteria the case itself raises (each with its own follow-up): contrast spine MRI
  (`order_body_imaging`, `study: spine_MRI`, `contrast: true`) for a red flag; `analyze_brain_mri`
  for a brainstem, Bickerstaff or posterior fossa question or reduced consciousness (required in
  encephalopathy with fever, RS17); `anti_AChR` (with `anti_MuSK` where bulbar) for a
  myasthenic mimic; `myositis_panel` for a myopathy mimic; `Lyme_serology` for facial diplegia;
  `AQP4_IgG_cell_based` and `MOG_IgG_cell_based` for a cord signal; `HIV_viral_load` and
  `CD4_count` in known HIV. `analyze_eeg` only for encephalopathy (RS17)

**Optional:**
- Ice pack test, single-fibre EMG, `anti_NF155`/`anti_CNTN1` (recurrence or autoimmune nodopathy),
  `paraneoplastic_panel`, chest CT for sarcoidosis, contrast spine MRI where the red flag is weak
  (RM14 spinal anaesthesia, RP16 leukaemic infiltration)
- `check_drug_interactions`: **required** only when the medication list has a concrete interaction
  with the planned work-up or treatment (anticoagulant or antiplatelet with LP or plasma exchange;
  ACE inhibitor with albumin plasma exchange; calcineurin inhibitor or other nephrotoxic drug with
  IVIg; checkpoint inhibitor; vincristine or L-asparaginase; statin with a myopathy differential;
  QT-prolonging drug with autonomic QT risk; succinylcholine risk with an interacting drug);
  recommended or optional otherwise, with the reason logged. Output category-level, each item with
  a source or "relative caution", no management instructions
- `search_medical_literature`: optional and last (ruling 5); population-keyed general evidence
  correctly cited, never the case's expected text

**Anti-ganglioside antibodies:** anti-GQ1b IgG only when MFS or an MFS-spectrum overlap is
suspected (anti-GT1a in PCB) [EAN_PNS_2023]; never for typical sensorimotor GBS, subtyping or
prognosis; a positive result never establishes the diagnosis and is always interpreted. The
follow-up uses trigger `request_anti_gq1b_gt1a_ganglioside_panel` and is unscored until the
vocabulary has the term (CENTRAL 1). `anti-GM1 IgM` is a multifocal motor neuropathy test and is
not used in GBS cases.

**Not in the current-encounter work-up:** antecedent-infection serology or PCR (Campylobacter, CMV,
EBV, HSV, Mycoplasma, influenza) and stool culture: specific testing is generally not clinically
useful for the diagnosis [EAN_PNS_2023]; the antecedent is history. HIV is not a routine baseline
test (EAN/PNS lists HIV among the differential infections, not as a routine test); add it only
with a risk the case states. IgA is not screened before IVIg (section 4).

## 3. Tools that are typically USELESS

Waste avoided actions used across the condition: `analyze_eeg`, `order_echocardiogram`,
`order_ct_scan`, `analyze_brain_mri` (only where nothing in the case raises a brainstem or central
question), `order_advanced_imaging` (`FDG_PET`, `MR_angiography`). Remove the waste entry wherever
the tool becomes a criterion.

## 4. Tools that are HARMFUL / contraindicated, and treatment statements

No diagnostic tool is harmful in typical GBS. Treatment lives in the assessment (ruling 4):

- IVIg 0.4 g/kg/day for 5 days (2 g/kg) within 2 weeks of onset, or plasma exchange 200-250 mL/kg
  in 5 sessions within 4 weeks, for patients unable to walk unaided (GBS disability score 3 or
  more); consider in ambulant patients with rapid progression or bulbar, autonomic or respiratory
  involvement; not advised in GBS-DS 1-2 within 2 weeks unless they progress. No preference between
  IVIg and PE; do not give IVIg directly after PE; no second IVIg course [EAN_PNS_2023,
  Walgaard_2021].
- MFS and incomplete MFS: IVIg and PE generally not recommended; admit and monitor for limb
  weakness, bulbar or respiratory involvement or reduced consciousness [Leonhard_2019].
- Canonical steroid prohibition: "Do not treat with corticosteroids: oral corticosteroids are
  strongly advised against and IV methylprednisolone is not recommended [EAN_PNS_2023]."
  Exception: checkpoint inhibitor-related GBS: hold the inhibitor permanently, IVIg or PE with IV
  methylprednisolone 2-4 mg/kg/day (pulse 1 g/day for 5 days may be considered in grade 3-4),
  slow taper; no rechallenge [Schneider_2021, Haanen_2022].
- "Check renal function before IVIg." No routine IgA screening: EAN/PNS 2023 does not ask for it;
  test only with a known IgA deficiency or a previous reaction to blood products.
- Plasma exchange cautions are relative unless sourced: haemodynamic instability, active bleeding or
  full anticoagulation, sepsis, difficult venous access; ACE inhibitors held 24 h before albumin PE.
- Avoid succinylcholine if intubation is needed (hyperkalaemia after denervation).
- Lactation: IVIg compatible with breastfeeding [LactMed].

## 5. Sequence constraints and respiratory rules

- `interpret_labs` (with `coagulation`) → `analyze_csf` (`hard`) where platelets, INR,
  fibrinogen or an anticoagulant make the LP unsafe without them (RM13, RP16, RS16);
  `check_drug_interactions` → `analyze_csf` (`hard`) with antithrombotics that need an interval
  or cannot stop (RS16). Spine MRI before LP (`soft`) near a recent spinal operation (RS12); labs
  before LP (`soft`) with traumatic haemorrhage on aspirin (RS13).
- `interpret_labs` → `check_drug_interactions` (`soft`) only where the drug check is required.
- Stop rule: `required_before_assessment` = the required criteria; `max_additional_actions: 3`.

**Respiratory report (canonical):** "Bedside respiratory function <time>: FVC <x> L (<y>%
predicted; <z> mL/kg at <w> kg) L. MIP <a> cmH2O L. MEP <b> cmH2O L. <Change sentence.> Cough
<weak/effective>." Weight and height go in `patient.physical_exam.general`. Values below reference
are flagged L, never H and never "within normal limits"; MIP/MEP reference values are age- and
sex-specific lower limits (Evans and Whitelaw, Respir Care 2009;54:1348-1359). Ventilated
patients report the last pre-intubation values. No spirometry in the patient block.

**ICU-level monitoring triggers:** FVC <20 mL/kg or <60% predicted (EAN/PNS 2023 reports FVC <60%
predicted as a predictor of ventilation; Reviewer 2 ruling), MIP weaker than -30 cmH2O, MEP <40
cmH2O [Lawn_2001], a fall of more than 30%, SBC <20, bulbar weakness with weak cough or pooled
secretions, autonomic instability, rapid progression [EAN_PNS_2023]. FVC <60% predicted is a
monitoring trigger, never an intubation criterion.

**Discordant band:** EAN/PNS 2023 states "MEP <30 cmH2O or MIP <40 cmH2O" as the point to consider
elective ventilation, transposing Lawn's 30/40. A case designed without an ICU trigger keeps MIP
stronger than -40 and MEP at 40 or more, and its escalation must names "MIP weaker than -40
cmH2O, MEP below 40 cmH2O" (the earlier of the two).

**Intubation:** never one threshold. Write it as trend + bulbar function + cough + secretions +
fatigue; clinical respiratory distress, hypoxaemia or hypercapnia mean intubation regardless of the
numbers; elective ventilation is considered when FVC <=20 mL/kg (almost inevitable at <=10 mL/kg)
[EAN_PNS_2023, Lawn_2001]. EGRIS [Walgaard_2010] may be quoted when the case gives days from onset
to admission, facial/bulbar weakness and MRC sum score; mEGOS [Walgaard_2011] uses the clinical
diarrhoea history, not serology.

## 6. Subtype variations

- **M (mild):** typical sensorimotor GBS; ICU-level or monitored-bed musts by the section 5 triggers
- **S (standard):** severe GBS, often meeting ICU triggers; IVIg or PE with dose and timing
- **P (progressive / puzzle):** variants (MFS, early ambulant GBS with Brighton level 2, HIV-
  associated GBS with pleocytosis)
- **R (reverse / mimic):** GBS with a mimic the case raises (stroke, myasthenia, myopathy, cord
  lesion, encephalitis, SIADH, ICI toxicity, transplant, malignancy); each mimic is excluded by its
  own criterion or lowered in the differential with the finding that excludes it. Acute-onset CIDP
  stays low with reassessment at 8 weeks; critical illness polyneuropathy very low with "no ICU
  course before onset"

## 7. Common red-herring categories and pitfalls

- **Normal CSF protein early** and **normal first-week NCS**: do not exclude GBS
- **Antecedent infection:** a history finding; "The antecedent infection is a history finding;
  serology is not needed for the diagnosis, and a positive IgM does not prove the trigger."
  Simultaneous IgM to several viruses is cross-reactivity, not three infections
- **Vaccine after onset** is not the trigger; seasonal influenza vaccine carries about one excess
  case per million [EAN_PNS_2023]
- **Unilateral facial palsy or ptosis:** facial involvement in GBS is often asymmetric; exclude
  Horner and oculomotor palsy on the exam
- **Template carry-over to avoid:** anti-GM1 IgM in a1; "trigger identification"; "VC <40%";
  "within normal limits" with FVC below 80%; low values flagged H; telemetry, repeat NCS or culture
  results dated after the assessment; treatment inside a tool report; Brighton quoted more than
  once; IgA prohibitions; "Do not combine IVIG and PE"
- **Every red herring** names a finding present in the case and how it resolves; none is invented
- **Labels:** "Guillain-Barré" spelling, no em dashes, no speculative attributions; a trigger is
  named only as the history supports it

## 8. Allowed citations

Every key cited in the 30 cases is listed here with its full reference.

- `[EAN_PNS_2023]`: van Doorn PA, Van den Bergh PYK, Hadden RDM, et al. European Academy of Neurology/Peripheral Nerve Society Guideline on diagnosis and treatment of Guillain-Barré syndrome. Eur J Neurol 2023;30:3646-3674 (also J Peripher Nerv Syst 2023;28:535-563). Governing guideline
- `[Leonhard_2019]`: Leonhard SE, Mandarakas MR, Gondim FAA, et al. Diagnosis and management of Guillain-Barré syndrome in ten steps. Nat Rev Neurol 2019;15:671-683 (red flags, monitoring, MFS management)
- `[Brighton_2011]`: Sejvar JJ, Kohl KS, Gidudu J, et al. Guillain-Barré syndrome and Fisher syndrome: case definitions and guidelines for collection, analysis, and presentation of immunization safety data. Vaccine 2011;29:599-612
- `[Lawn_2001]`: Lawn ND, Fletcher DD, Henderson RD, Wolter TD, Wijdicks EFM. Anticipating mechanical ventilation in Guillain-Barré syndrome. Arch Neurol 2001;58:893-898 (20/30/40 rule)
- `[Walgaard_2010]`: Walgaard C, Lingsma HF, Ruts L, et al. Prediction of respiratory insufficiency in Guillain-Barré syndrome. Ann Neurol 2010;67:781-787 (EGRIS)
- `[Walgaard_2011]`: Walgaard C, Lingsma HF, Ruts L, van Doorn PA, Steyerberg EW, Jacobs BC. Early recognition of poor prognosis in Guillain-Barré syndrome. Neurology 2011;76:968-975 (mEGOS)
- `[Walgaard_2021]`: Walgaard C, Jacobs BC, Lingsma HF, et al. Second intravenous immunoglobulin dose in patients with Guillain-Barré syndrome with poor prognosis (SID-GBS): a double-blind, randomised, placebo-controlled trial. Lancet Neurol 2021;20:275-283
- `[Wakerley_2014]`: Wakerley BR, Uncini A, Yuki N; GBS Classification Group. Guillain-Barré and Miller Fisher syndromes: new diagnostic classification. Nat Rev Neurol 2014;10:537-544
- `[Schneider_2021]`: Schneider BJ, Naidoo J, Santomasso BD, et al. Management of immune-related adverse events in patients treated with immune checkpoint inhibitor therapy: ASCO guideline update. J Clin Oncol 2021;39:4073-4126 (RP11 only)
- `[Haanen_2022]`: Haanen J, Obeid M, Spain L, et al. Management of toxicities from immunotherapy: ESMO Clinical Practice Guideline for diagnosis, treatment and follow-up. Ann Oncol 2022;33:1217-1238 (RP11 only)
- `[LactMed]`: Drugs and Lactation Database (LactMed). Bethesda (MD): National Institute of Child Health and Human Development; 2006-. Immune Globulin (NCBI Bookshelf NBK501437) (RM14)

Background only, not cited as primary (superseded by [EAN_PNS_2023] for every statement it covers):

- `[Asbury_1990]`: Asbury AK, Cornblath DR. Assessment of current diagnostic criteria for Guillain-Barré syndrome. Ann Neurol 1990;27 Suppl:S21-S24. Superseded
- `[Hadden_1998]`: Hadden RD, Cornblath DR, Hughes RA, et al. Electrophysiological classification of Guillain-Barré syndrome. Ann Neurol 1998;44:780-788. Superseded (subtyping not advised for routine decisions)
- `[Sharshar_2003]`: Sharshar T, Chevret S, Bourdain F, Raphaël JC. Early predictors of mechanical ventilation in Guillain-Barré syndrome. Crit Care Med 2003;31:278-283. Background (FVC <60% predicted as a predictor)
- `[Yuki_2012]`: Yuki N, Hartung HP. Guillain-Barré syndrome. N Engl J Med 2012;366:2294-2304. Background review
- `[van_den_Berg_2014]`: van den Berg B, Walgaard C, Drenthen J, et al. Guillain-Barré syndrome: pathogenesis, diagnosis, treatment and prognosis. Nat Rev Neurol 2014;10:469-482. Secondary key only, next to [EAN_PNS_2023]
