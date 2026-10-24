# Criteria pack: Myasthenia Gravis

**ICD-10-CM:** G70.00 (myasthenia gravis without acute exacerbation) for a new or stable
presentation; G70.01 (with acute exacerbation, includes myasthenic crisis) only for an exacerbation
or crisis. Lambert-Eaton myasthenic syndrome cases filed under this condition use G73.1
(Lambert-Eaton syndrome in neoplastic disease) or G70.80 (unspecified).
**Condition enum:** `NeurologicalCondition.MYASTHENIA_GRAVIS`
**Case ID prefix:** `MG`

Updated 24 Oct 2026 to the rulings of the October 2026 review round (`data/review/round-2026-10/
plans/MG.md`, `MG-summary.md`) and to the decisions on its open questions (`plans/MG-decisions.md`).
No physician has reviewed the MG cases yet; the physician input is the July 2026 tool review
(Reviewer 2, `agent-platform/config/review/condition_tool_guidance.yaml`).

---

## 1. Diagnostic criteria and governing sources

**Which source governs what:**

- Diagnosis, serology order, neurophysiology and thymic imaging: ABN 2025 [Jacob_2025] and the
  Italian recommendations [Evoli_2019]. Thymectomy: MGTX [Wolfe_2016] with its extension
  [Wolfe_2019] and ABN 2025.
- Management (steroids, steroid-sparing agents, IVIG and plasma exchange, crisis): international
  consensus guidance [Sanders_2016] and its 2020 update [Narayanaswami_2021]; ABN 2025 for the
  inpatient thresholds and crisis care.
- MGFA clinical classification: [Jaretzki_2000_MGFA].
- Overview and antibody biology: [Gilhus_2016], [Gilhus_2019], [Punga_2022] (epidemiology,
  diagnostics and biomarkers; not a treatment guideline), [Vincent_2003] (pathophysiology only).
- LRP4 antibodies: [Higuchi_2011], [Zisimopoulou_2014].
- LEMS (cases P02, RM13): [Titulaer_2011] (diagnosis and treatment), [EFNS_paraneoplastic_2011]
  (tumour screening), [Titulaer_2011_DELTAP] (SCLC probability), [Oh_2005] (RNS facilitation
  cut-off), amifampridine EU SmPC [Firdapse_SmPC].
- Respiratory thresholds: [Lawn_2001] (20/30/40 rule, GBS cohort, applied to neuromuscular
  respiratory failure) and ABN 2025 (FVC below 20 mL/kg or a fall of more than 30% prompts ICU
  referral).
- Iodinated contrast in overt hyperthyroidism (RM16): [ESUR_contrast].
- Natalizumab PML risk (P03): [Ho_2017].

**Diagnosis:** fluctuating, fatigable weakness of ocular (ptosis, diplopia), bulbar, neck, limb or
respiratory muscles, supported by antibodies and/or neurophysiology. Ocular MG is MGFA class I;
any non-ocular weakness (bulbar-only, neck extensor or limb) is generalized (classes II-V, "a"
limb-predominant, "b" oropharyngeal/respiratory-predominant). About 50% of ocular AChR-positive
patients generalize within 2 years [Jacob_2025].

**Serology** [Jacob_2025, Evoli_2019, Punga_2022]:
- AChR binding antibody by radioimmunoassay or cell-based assay (not ELISA) first; positive in
  about 85% of generalized and about 50% of ocular MG.
- MuSK when AChR is negative (many laboratories test both together).
- High-sensitivity cell-based panel (clustered AChR, clustered MuSK, LRP4) when standard tests
  are negative and suspicion stays high; seronegative MG is diagnosed only after it. LRP4
  antibodies occur in a minority of double-seronegative patients, with wide variation between
  cohorts [Zisimopoulou_2014]; never quote a single figure.
- Units: AChR binding and MuSK in nmol/L; AChR blocking and modulating antibodies in %. One
  laboratory's reference range per case. A value above the stated range is positive, never
  "borderline".
- Thyroid function in every patient [Jacob_2025]; thyroid antibodies (anti-TPO, TRAb) when
  thyroid disease is suspected or known.
- Anti-striated muscle, anti-titin and anti-RyR antibodies are unlikely to be diagnostically
  helpful [Jacob_2025]; they are not orderable and never a criterion. No paraneoplastic panel in
  MG (LEMS: P/Q-type VGCC and SOX1 only).
- CK and troponin only with immune checkpoint inhibitor exposure.

**Neurophysiology** [Jacob_2025]:
- Repetitive nerve stimulation (RNS) first, at 2-3 Hz (2-5 Hz acceptable): a decrement above 10%
  between the 1st and 4th (or 5th) response is abnormal; test clinically weak muscles, include a
  facial (nasalis or orbicularis oculi) and a proximal muscle (trapezius, deltoid), warm the limb
  to 32-34 C and hold pyridostigmine for at least 12 hours. Sensitivity about 75% in generalized
  and under 50% in ocular MG. Routine NCS accompany it (normal baseline CMAP amplitudes argue
  against LEMS and exclude a neuropathy).
- Single-fibre EMG (jitter, blocking) is abnormal in over 90% of MG but not specific (also in
  neuropathy, myopathy and motor neuron disease). It is the study when RNS is normal and the
  diagnosis is still open, and in seronegative patients.
- LEMS: low baseline CMAP amplitudes, slow-rate decrement and an increment of at least 60% after
  10 s of maximal exercise or at 20-50 Hz [Oh_2005] (100% is the classic, less sensitive
  cut-off; brief exercise is preferred to painful 50 Hz stimulation).
- The edrophonium (Tensilon) test is no longer recommended [Jacob_2025] and is not orderable. The
  ice-pack test is for ptosis only (improvement of MRD1 or palpebral fissure of at least 2 mm
  after 2-5 min of ice).

**Imaging:**
- Thymic imaging (CT with contrast or MRI of the mediastinum) in every patient with suspected MG,
  irrespective of distribution or serology; a chest X-ray does not substitute [Jacob_2025].
  Iodinated contrast has rare reports of MG worsening and is still used, with monitoring; it is
  withheld in overt hyperthyroidism [ESUR_contrast].
- Contrast brain and orbit MRI only after negative serology and negative neurophysiology, or when
  the case raises a central or orbital mimic (MS or PML, orbitopathy, restrictive orbit,
  brainstem lesion) [Jacob_2025]. Never first line.
- FDG-PET belongs to the LEMS tumour search (chest CT negative or equivocal) [EFNS_paraneoplastic_2011];
  it has no role in MG.
- CSF has no role in MG (Reviewer 2): no MG case orders CSF studies.

## 2. Standard workup hierarchy

Canonical criterion and follow-up order (the review app reads it as the work-up sequence): AChR
binding antibody with thyroid function; RNS; MuSK (if AChR negative), then the cell-based panel or
LRP4 (if double seronegative); SFEMG (RNS normal or seronegative); ice-pack test (ptosis only; may
come first as a bedside test); mediastinal CT with contrast; respiratory function (staging; first
when the patient is bulbar or breathless); brain MRI only where section 1 allows; drug
interaction check (pre-treatment safety); literature last.

**Required:**
- `interpret_labs` (`panels: [anti_AChR, TSH]`, subset matching, so ordering MuSK alongside still
  matches) [Jacob_2025]. `anti_MuSK` is its own required criterion only in AChR-negative cases;
  `anti_LRP4` or `clustered_AChR_cell_based` is required only where the label rests on it (LRP4
  MG), recommended in other double-seronegative cases.
- `order_specialized_test` (`test_type: repetitive_nerve_stimulation`) in every new diagnosis.
  Ocular cases use one required neurophysiology criterion with RNS and SFEMG as alternatives.
- `order_specialized_test` (`test_type: emg_single_fiber`): required in seronegative cases and
  wherever RNS is normal and the label rests on SFEMG; recommended when RNS is normal or
  equivocal with positive serology; optional when RNS is already diagnostic.
- `order_body_imaging` (`study: mediastinum_CT`, `contrast: true`; alternatives `chest_CT` and
  `mediastinum_MRI` with contrast) in every new diagnosis [Jacob_2025]; contrast not required where
  it is contraindicated (RM16).

**Recommended:**
- `order_specialized_test` (`test_type: ice_pack_test`) only with ptosis on examination.
- `order_specialized_test` (`test_type: respiratory_function`) in generalized MG; required in
  crisis or impending crisis and wherever bulbar or respiratory weakness is present and the case
  reports FVC or MIP results; optional in ocular MG.

**Optional:**
- `check_drug_interactions` (ruling 6): required only with a concrete interaction that changes
  management (a precipitating fluoroquinolone in crisis; amifampridine with the patient's
  medicines; hydroxychloroquine or pilocarpine with pyridostigmine; a beta-blocker in a patient
  starting treatment); recommended for a relevant caution (neuromuscular blocker in an intubated
  patient, timolol drops, metoprolol, vincristine, natalizumab); optional or absent otherwise
  (oral contraceptive, levothyroxine, metformin, amlodipine, losartan, statins, aspirin, insulin).
  Never a generic pyridostigmine list without one of the patient's own medicines. Telithromycin
  is withdrawn and is never listed.
- `search_medical_literature`: optional and last (ruling 5), or absent; its stored output cites
  section 8 sources in report voice and never repeats a criterion's expected evidence.
- `analyze_ecg`: required before amifampridine (LEMS); otherwise only with a cardiac question.
- `analyze_brain_mri`: only where section 1 allows (P03 required; LEMS staging optional).
- Specialist referral, thymectomy, IVIG, plasma exchange and drug choices are musts in the
  assessment, never tool calls.

**Variant pathways:**
- **Seronegative or LRP4 (P01, P04, RP14):** AChR + TSH required, MuSK required, CBA or LRP4
  required (P04) or recommended, RNS required, SFEMG required, mediastinal CT required.
- **MuSK-positive (RS14):** MuSK required (the label rests on it), RNS with facial muscles
  required, SFEMG recommended, mediastinal CT required (Reviewer 2 asks for thymic imaging in
  every case, although MuSK MG has no thymoma association), respiratory function required, brain
  MRI optional, no ice pack without ptosis.
- **Ocular (RS11, S05):** AChR + TSH required, neurophysiology required (RNS or SFEMG), ice pack
  recommended, mediastinal CT required, respiratory function optional.
- **Known MG in exacerbation or crisis (M04, RM14, RM15):** respiratory function first
  (required); precipitant search (drug check of the offending drug required when it is a
  fluoroquinolone); labs required as an infection and electrolyte panel (`[CBC, BMP]` or
  `[CBC, CMP]`, plus CRP where used); urine or respiratory microbiology and chest X-ray
  recommended; AChR repeat optional; RNS and SFEMG are waste ("Electrodiagnostic confirmation is
  not needed in a known AChR-positive patient in crisis and delays treatment"); mediastinal CT
  optional where prior thymic imaging or thymectomy is documented and the precipitant is
  explained.
- **LEMS (P02, RM13):** labs `[anti_VGCC_PQ, anti_SOX1]` (VGCC alone where SOX1 is already
  known) required; RNS with post-exercise facilitation required; chest CT with contrast
  (alternatives chest-abdomen-pelvis CT, mediastinal CT) required; FDG-PET required when the CT
  is negative or equivocal [EFNS_paraneoplastic_2011]; tissue diagnosis (lymph node biopsy with
  TTF1 and chromogranin/synaptophysin IHC) required for a new tumour, recommended for a
  recurrence; amifampridine drug check and a baseline ECG required; autonomic testing, SFEMG and
  literature optional.

## 3. Tools that are typically USELESS

Waste avoided actions used across the condition, each with a case-specific rationale citing
[Jacob_2025] (never [Wolfe_2016]): `analyze_eeg`, `analyze_csf`, `order_advanced_imaging`
(`FDG_PET`) outside LEMS, `analyze_brain_mri` where nothing raises a central or orbital mimic,
`order_echocardiogram` and `order_cardiac_monitoring` without a cardiac question. In crisis cases
RNS and SFEMG. Remove the waste entry wherever the tool is a criterion of the case (P03 MRI, LEMS
FDG-PET, RS14 MRI). `emg_ncs` is not waste: routine NCS accompany RNS.

## 4. Tools that are HARMFUL / contraindicated, and treatment statements

No diagnostic tool is harmful in MG. Treatment lives in the assessment (ruling 4):

- Pyridostigmine 30-60 mg three to five times daily titrated to effect (doses above 360 mg/day
  rarely add benefit [Jacob_2025]); cholinergic crisis is unlikely at 240 mg/day or less and is
  recognised by muscarinic signs (sweating, salivation, diarrhoea, bradycardia, miosis).
- Canonical steroid prohibition: "Do not start high-dose prednisone (above 20 mg/day) as an
  outpatient; start low and titrate, or start high dose only with inpatient monitoring, because
  initial steroid-induced worsening can precipitate crisis." Pyridostigmine does not prevent it.
  Steroid-sparing agent (azathioprine first line, after TPMT or NUDT15 testing; mycophenolate or
  methotrexate as alternatives) when steroids are needed long term [Sanders_2016,
  Narayanaswami_2021, Jacob_2025].
- Thymectomy: any thymoma (irrespective of antibody status or severity); non-thymomatous
  AChR-positive generalized MG aged 18-65, as early as possible (MGTX benefit to 5 years)
  [Wolfe_2016, Wolfe_2019; ABN 2025: recommended under 50, discussed at 50-65]. Not indicated in
  MuSK MG; no data in seronegative MG; may be considered in AChR-positive ocular MG within 2-3
  years [Jacob_2025]. Pre-operative IVIG or plasma exchange only with significant bulbar or
  respiratory weakness [Sanders_2016].
- IVIG 2 g/kg over 2-5 days or plasma exchange (five exchanges) for crisis, impending crisis,
  severe bulbar weakness or before surgery in unstable patients; equally effective; renal
  function and thrombotic risk checked before IVIG; plasma exchange best avoided in sepsis
  [Jacob_2025]. IgA testing is not a gate.
- ICU or HDU referral: FVC below 20 mL/kg or a fall of more than 30% [Jacob_2025]; MIP weaker than
  -30 cmH2O, MEP below 40 cmH2O [Lawn_2001]; bulbar weakness with a weak cough or pooled
  secretions, hypercapnia or distress. Inpatient care for FVC below 30 mL/kg or significant
  bulbar symptoms [Jacob_2025]. Pulse oximetry is a late marker. Pyridostigmine is commonly held
  while intubated (secretions).
- Canonical drug prohibition (name only drugs relevant to the patient plus the classic set):
  "Avoid fluoroquinolones, aminoglycosides, macrolides and IV magnesium unless no alternative
  exists and the patient is monitored; use non-depolarising neuromuscular blockers only at reduced
  dose with quantitative monitoring." Also avoid botulinum toxin, D-penicillamine and immune
  checkpoint inhibitors; use with caution beta-blockers (timolol drops included),
  hydroxychloroquine and chloroquine, procainamide, quinine, statins (case reports), iodinated
  contrast.
- Pregnancy: azathioprine and prednisone acceptable; mycophenolate and methotrexate teratogenic
  (contraception, washout before conception); pyridostigmine compatible; IV magnesium for
  pre-eclampsia contraindicated in MG. Combined oral contraceptives have no clinically important
  interaction with pyridostigmine; ethinylestradiol increases prednisone exposure.
- Amifampridine (LEMS): start 15 mg/day in divided doses, EU maximum 60 mg/day; contraindicated in
  epilepsy, congenital long QT and with drugs with a known QT-prolonging potential; clinical and
  ECG monitoring at initiation and yearly thereafter, ECG at once if arrhythmia is suspected
  [Firdapse_SmPC]. Seizure risk rises with dose. Treat the tumour first: LEMS often improves with
  SCLC treatment [Titulaer_2011].

## 5. Sequence constraints and stop rule

All soft; no hard constraint in this condition.
- `interpret_labs` (AChR) -> `emg_single_fiber`: "AChR antibody testing precedes single-fibre
  EMG; SFEMG is reserved for seronegative patients or a normal RNS (Jacob 2025)."
- `repetitive_nerve_stimulation` -> `emg_single_fiber`: "Repetitive nerve stimulation is done
  first; SFEMG follows when RNS is normal (Jacob 2025)." No constraint when the case has no SFEMG
  criterion.
- AChR-negative cases: AChR labs -> MuSK (and -> LRP4 where scored).
- LEMS: chest CT -> FDG-PET, chest CT -> tissue diagnosis (FDG-PET -> tissue where only PET shows
  the target).
- Crisis: `respiratory_function` -> mediastinal CT.
- Never a constraint involving literature or a recommended drug check.
- Stop rule: `required_before_assessment` = the required criteria; `max_additional_actions` 1 in
  S cases, 2 elsewhere (sending AChR and MuSK together is common practice).

## 6. Subtype variations

- **M (mild / moderate):** new generalized AChR-positive MG with a comorbidity that shapes
  management (thymoma, polyautoimmunity, COPD, diabetes), or a known-MG exacerbation (M04).
- **S (standard):** classic generalized or ocular AChR-positive MG, thymic imaging required,
  thymectomy per section 4.
- **P (puzzle):** seronegative, LRP4 or a concurrent disease that masks MG (MS on natalizumab,
  anxiety), and LEMS presented as the myasthenic mimic (P02).
- **R (reverse / mimic):** MG mistaken for its mimics (CPEO, Brown syndrome, PD, thyroid eye
  disease, GBS relapse, vincristine neuropathy, functional dysphonia), MuSK MG, crisis cases, and
  LEMS with recurrent SCLC (RM13). Each mimic is excluded by its own criterion or lowered in the
  differential with the finding that excludes it.

## 7. Common red-herring categories and pitfalls

- **Negative AChR antibodies** do not exclude MG: MuSK, then the cell-based panel.
- **Normal RNS** does not exclude MG: SFEMG is more sensitive (and less specific).
- **LEMS against MG:** proximal leg weakness, areflexia, autonomic symptoms and low CMAPs with
  facilitation point to LEMS; ocular onset and decrement without facilitation to MG.
- **Stress, fatigue, anxiety or a prior functional diagnosis:** fluctuation and fatigability are
  the MG signature; "Do not attribute fatigable ptosis, diplopia or bulbar weakness to a
  functional or <mimic> cause before AChR antibody testing and neurophysiology."
- **Wrong facts to keep out of every case:** tiotropium "antagonises the NMJ" (it is a muscarinic
  M3 antagonist); metoprolol "prolongs QT"; alemtuzumab "treats myasthenic disorders" (MG has
  been reported after it); azathioprine "teratogenic"; "MGTX 5-year, Lancet Neurology 2022" (it
  is Lancet Neurol 2019); "MMF NEJM 2008" (the MMF trials are Neurology 2008); "Rule of 20-30:
  intubate if NIF <-20"; "HCQ used in NMJ protocols"; "RNS decrement pathognomonic"; "SFEMG gold
  standard"; telithromycin as a current drug; the Tensilon test.
- **Template carry-over to avoid:** spirometry, NIF or MEP numbers in the patient block when
  respiratory function is a criterion; scored serology or imaging results in the HPI; a head-CT
  report holding the thymic CT; a fallback that comments on its own relevance ("does not address
  the question"); "All normal" panels without analytes.

## 8. Allowed citations

Every key cited in the 30 cases (`[Gilhus_2016]`, `[Punga_2022]`, `[Sanders_2016]`,
`[Wolfe_2016]`) is listed here with its full reference, together with the sources the cases cite
by author in their text. None is superseded; `[Sanders_2016]` is read together with its 2020
update `[Narayanaswami_2021]`.

- `[Jacob_2025]`: Jacob S, Farrugia ME, Hewamadduma C, et al. Association of British Neurologists (ABN) autoimmune myasthenia gravis management guidelines (2025 update). Pract Neurol 2025;25:422-437. doi:10.1136/pn-2025-004655. Governing source for diagnosis, thymic imaging and inpatient care
- `[Evoli_2019]`: Evoli A, Antonini G, Antozzi C, et al. Italian recommendations for the diagnosis and treatment of myasthenia gravis. Neurol Sci 2019;40:1111-1124. doi:10.1007/s10072-019-03746-1
- `[Sanders_2016]`: Sanders DB, Wolfe GI, Benatar M, et al. International consensus guidance for management of myasthenia gravis: executive summary. Neurology 2016;87:419-425
- `[Narayanaswami_2021]`: Narayanaswami P, Sanders DB, Wolfe G, et al. International consensus guidance for management of myasthenia gravis: 2020 update. Neurology 2021;96:114-122. doi:10.1212/WNL.0000000000011124
- `[Wolfe_2016]`: Wolfe GI, Kaminski HJ, Aban IB, et al. Randomized trial of thymectomy in myasthenia gravis (MGTX). N Engl J Med 2016;375:511-522. Cited only for thymectomy and the thymic-imaging decision
- `[Wolfe_2019]`: Wolfe GI, Kaminski HJ, Aban IB, et al. Long-term effect of thymectomy plus prednisone versus prednisone alone in patients with non-thymomatous myasthenia gravis: 2-year extension of the MGTX randomised trial. Lancet Neurol 2019;18:259-268
- `[Jaretzki_2000_MGFA]`: Jaretzki A 3rd, Barohn RJ, Ernstoff RM, et al. Myasthenia gravis: recommendations for clinical research standards. Neurology 2000;55:16-23 (MGFA clinical classification)
- `[Gilhus_2016]`: Gilhus NE. Myasthenia gravis. N Engl J Med 2016;375:2570-2581 (review)
- `[Gilhus_2019]`: Gilhus NE, Tzartos S, Evoli A, Palace J, Burns TM, Verschuuren JJGM. Myasthenia gravis. Nat Rev Dis Primers 2019;5:30 (review)
- `[Punga_2022]`: Punga AR, Maddison P, Heckmann JM, Guptill JT, Evoli A. Epidemiology, diagnostics, and biomarkers of autoimmune neuromuscular junction disorders. Lancet Neurol 2022;21:176-188 (not a treatment guideline)
- `[Vincent_2003]`: Vincent A. Unravelling the pathogenesis of myasthenia gravis. Nat Rev Immunol 2002;2:797-804 (the key keeps its historical name; the paper is 2002; pathophysiology only)
- `[Higuchi_2011]`: Higuchi O, Hamuro J, Motomura M, Yamanashi Y. Autoantibodies to low-density lipoprotein receptor-related protein 4 in myasthenia gravis. Ann Neurol 2011;69:418-422
- `[Zisimopoulou_2014]`: Zisimopoulou P, Evangelakou P, Tzartos J, et al. A comprehensive analysis of the epidemiology and clinical characteristics of anti-LRP4 in myasthenia gravis. J Autoimmun 2014;52:139-145
- `[Titulaer_2011]`: Titulaer MJ, Lang B, Verschuuren JJ. Lambert-Eaton myasthenic syndrome: from clinical characteristics to therapeutic strategies. Lancet Neurol 2011;10:1098-1107
- `[EFNS_paraneoplastic_2011]`: Titulaer MJ, Soffietti R, Dalmau J, et al. Screening for tumours in paraneoplastic syndromes: report of an EFNS Task Force. Eur J Neurol 2011;18:19-e3 (CT thorax first, FDG-PET if negative; in LEMS repeat screening for 2 years)
- `[Titulaer_2011_DELTAP]`: Titulaer MJ, Maddison P, Sont JK, et al. Clinical Dutch-English Lambert-Eaton Myasthenic syndrome (LEMS) tumor association prediction score accurately predicts small-cell lung cancer in the LEMS. J Clin Oncol 2011;29:902-908
- `[Oh_2005]`: Oh SJ, Kurokawa K, Claussen GC, Ryan HF Jr. Electrophysiological diagnostic criteria of Lambert-Eaton myasthenic syndrome. Muscle Nerve 2005;32:515-520 (60% increment)
- `[Firdapse_SmPC]`: Firdapse (amifampridine) 10 mg tablets, Summary of Product Characteristics, European Medicines Agency (sections 4.2-4.5: dosing, contraindications, ECG monitoring)
- `[Lawn_2001]`: Lawn ND, Fletcher DD, Henderson RD, Wolter TD, Wijdicks EFM. Anticipating mechanical ventilation in Guillain-Barré syndrome. Arch Neurol 2001;58:893-898 (20/30/40 rule; shared with GBS)
- `[ESUR_contrast]`: van der Molen AJ, Thomsen HS, Morcos SK; Contrast Media Safety Committee, European Society of Urogenital Radiology (ESUR). Effect of iodinated contrast media on thyroid function in adults. Eur Radiol 2004;14:902-907; and ESUR Guidelines on Contrast Agents, version 10.0 (2018): iodinated contrast is not given in manifest hyperthyroidism (RM16)
- `[Ho_2017]`: Ho PR, Koendgen H, Campbell N, Haddock B, Richman S, Chang I. Risk of natalizumab-associated progressive multifocal leukoencephalopathy in patients with multiple sclerosis: a retrospective analysis of data from four clinical studies. Lancet Neurol 2017;16:925-933 (P03)
