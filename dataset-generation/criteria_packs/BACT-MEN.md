# Criteria pack: Bacterial meningitis

**ICD-10:** G00.x (by organism), G00.9 (unspecified bacterial)
**Condition enum:** `NeurologicalCondition.BACTERIAL_MENINGITIS`
**Case ID prefix:** `BACT-MEN`

Updated 24 Oct 2026 to the rulings of the October 2026 physician-review round
(`data/review/round-2026-10/plans/BACT-MEN.md`, `BACT-MEN-summary.md`).

---

## 1. Diagnostic criteria and governing sources

**Which source governs what:**

- Community-acquired adult disease (imaging before LP, therapy, steroids, CSF values): WHO 2025
  [WHO_Meningitis_2025]. NICE NG240 [NICE_NG240] is the concordant UK source, cited only where the
  patient is in its scope.
- Healthcare-associated ventriculitis and meningitis (EVD, shunt, post-neurosurgery, nosocomial,
  post-neuraxial procedure): IDSA 2017 [IDSA_2017_HCVM].
- Pneumococcal susceptibility: CLSI M100 meningitis breakpoints [CLSI_M100].
- Tuberculous meningitis: WHO TB Module 4 [WHO_TB_Module4]; cryptococcal meningitis in HIV: WHO
  2022 [WHO_Cryptococcal_2022].
- Scope rules: WHO 2025 section 1.7 excludes hospital-acquired, nosocomial and healthcare-associated
  meningitis; NICE NG240 excludes intracranial shunts, previous neurosurgery, brain tumours and
  people with immunodeficiency (asplenia, immunosuppressive therapy, HIV). Where WHO and NICE diverge
  (severe immunocompromise is a WHO imaging trigger, not a NICE one), **WHO governs** and the
  rationale says so in one sentence.
- IDSA 2004 and ESCMID 2016 are superseded (section 8): never cite them in criteria, avoided actions
  or constraints.

Clinical syndrome: fever, headache, meningism and altered mental status (the classic triad is
present in a minority). Typical pyogenic CSF: turbid, raised opening pressure, neutrophilic
pleocytosis, raised protein, low glucose ratio, +/- positive Gram stain and culture; multiplex PCR is
useful when antibiotics have already been given. The Bacterial Meningitis Score (Nigrovic) stratifies
in children: low risk if all of: negative CSF Gram stain, CSF ANC <1000, CSF protein <80 mg/dL,
peripheral ANC <10,000, no seizure at presentation [Nigrovic_2007].

**CSF reference values (WHO 2025 A.2.2) [WHO_Meningitis_2025]:**

- CSF:blood glucose ratio normal 0.5 to 0.8; 0.4 or less is abnormally low. Report it with the paired
  values: "<r> (CSF <x> mg/dL / blood <y> mg/dL; reference 0.5 to 0.8, 0.4 or less abnormally low)",
  using the same blood glucose as the lab panel. Never "normal >0.6".
- RBC up to 5 cells/microL is normal in adults: "<n> cells/microL (within normal limits)"; never
  "traumatic tap" for 0 to 5.
- Lactate: WHO gives no threshold; print "(local laboratory reference <3.5 mmol/L)".
- Gram stain sensitivity about 85% with wide confidence limits (WHO 2025), lower after antibiotics;
  Listeria about 33% [Brouwer_2012].
- Antigen detection is not among the WHO 2025 Box 3.1 recommendations; a positive result needs
  culture or molecular confirmation and is never the confirming test.
- Multiplex PCR panels do not target S. suis, Proteus, Klebsiella or other Enterobacterales except
  E. coli K1. A non-target result reads "No panel target detected (targets: <list>)"; the limitation
  goes in key evidence or a red herring, not in the result.
- CSF interpretation states values and pattern only: no diagnosis, no organism inference beyond the
  stain or PCR, no partial-treatment speculation. After neurosurgery cell counts and glucose are less
  discriminating and culture is the reference (IDSA 2017).

**Susceptibility (CLSI meningitis breakpoints, S. pneumoniae) [CLSI_M100]:** penicillin susceptible
at MIC 0.06 mg/L or less, resistant at 0.12 or more, no intermediate category; ceftriaxone
susceptible 0.5 or less, intermediate 1, resistant 2 or more.

## 2. Standard workup hierarchy

Canonical criterion order (the review app reads it as the work-up sequence): labs, blood cultures,
CT (imaging-first cases only), index lumbar puncture, then source and complication studies (CT for
another indication, MRI, MR venography, spine MRI, immunology labs), drug-interaction check last.

**Required:**
- `interpret_labs` (CBC with differential, CMP including liver tests, lactate, procalcitonin, HIV; known HIV: CD4 and viral load as the case states): peripheral inflammatory response, sepsis and organ function, host factors [WHO_Meningitis_2025]
- `order_microbiology` (`specimen: blood_culture`): blood cultures before the first antibiotic dose. `before_antimicrobials: true` is a required argument only where the report flag is true; the flag is false whenever any antimicrobial (oral course, prophylaxis, perioperative, empirical) was taken in the 7 days before collection, stated in one line [WHO_Meningitis_2025]
- `analyze_csf` (`special_tests: meningitis_panel`): the index lumbar puncture (Gram stain, culture, cell count and differential, glucose with paired blood glucose, protein, lactate, multiplex PCR). Culture reads "Pending" in the index report; a final culture report is a separate later follow-up [WHO_Meningitis_2025]
- `order_ct_scan` (`contrast: false`): **required only when a WHO 2025 section A.4 imaging-first criterion is present** (see below); it follows blood cultures and the first antibiotic dose [WHO_Meningitis_2025]

**Imaging before LP (WHO 2025 section A.4) [WHO_Meningitis_2025]:** cranial imaging is not performed
routinely; where readily accessible it precedes LP if, at presentation: GCS below 10; focal
neurological signs; cranial nerve deficits; papilloedema; new-onset seizures in adults; or a severe
immunocompromised state. NICE NG240 1.4.7: risk factors for an evolving space-occupying lesion, new
focal neurological features, abnormal pupillary reactions, GCS 9 or less, or a progressive and
sustained or rapid fall in consciousness; NICE 1.4.6: do not routinely image before LP; NICE 1.4.8:
take bloods, give antibiotics and stabilise before imaging [NICE_NG240]. **Not criteria in either
source: age, "altered mental status", confusion, diabetes.** Criteria are judged on what is known
before the scan. Severe immunocompromise (Reviewer 2): yes for asplenia and advanced HIV (CD4 68);
no for prednisone 7.5 mg, prednisone with weekly methotrexate, diabetes, HIV with CD4 312, inhaled
steroids, undiagnosed CVID. WHO gives no steroid threshold (its example is organ transplantation):
where a patient meets the IDSA 2013 definition of high-level immunosuppression (prednisone 20 mg or
more daily for 14 days or more [IDSA_2013_Vaccination]) and has no other criterion, CT before LP is
neutral (no criterion, no waste avoided action; a must accepts either course with antibiotics first),
as in RS03 (prednisolone 30 mg for about two weeks).

**Lumbar puncture safety (WHO 2025 A.1.1; NICE NG240 1.4.11, 1.4.12):** no LP with a known or
suspected bleeding diathesis, infection at the puncture site, or haemodynamic or respiratory
compromise that needs stabilisation; NICE adds extensive or rapidly spreading purpura. Shock and
coagulopathy are stabilised and corrected first (a must; antibiotics never wait). Where spreading
purpura makes the LP unsafe at presentation (S05), the index LP is `optional`, out of the stop rule,
and blood cultures with blood PCR carry the diagnosis.

Per case, one of:
- **A. Imaging-first criterion present:** CT required, HARD constraint CT before CSF, SOFT
  constraint blood cultures before CT.
- **B. No criterion, but CT has another indication** (parameningeal or skull-base source, shunt,
  implant): CT kept (required or recommended per case) for that indication, ordered after the CSF,
  no HARD constraint, SOFT constraint blood cultures before CT. CT reports state findings only.
- **C. No criterion and no other indication:** no CT criterion; CT is a `waste` avoided action.

**Recommended / per case:**
- `check_drug_interactions` (`{}`): **required** only for a concrete allergy, interaction or renal dosing issue that changes management (e.g. cephalosporin or penicillin allergy, CKD dosing, rifampicin with levothyroxine, penicillins with methotrexate, AKI with tenofovir); otherwise **recommended**. The output checks the case's real regimen against the patient's real allergies, medicines and eGFR (CKD-EPI 2021); expected evidence names the concrete issue. Last in the pathway order [WHO_Meningitis_2025]
- `analyze_brain_mri` (contrast): for a delayed presentation, abscess suspicion or complications (subdural empyema, ventriculitis, cerebritis, venous sinus thrombosis); MRI > CT for these; tier per case [Brouwer_2012]
- Source and host studies where a tool exists, tier per case: MR venography, spine MRI (spinal infection), immunoglobulins (recurrent or CVID), syphilis serology in HIV, urine culture with a catheter, CSF from a shunt tap as an `analyze_csf` follow-up after the index LP

**Optional:**
- `analyze_eeg`: only if seizure activity or persistent altered mental status

**Not a clinical step:** `search_medical_literature` is not part of the pathway (October 2026
ruling 5): no literature criterion, no literature follow-up, `initial_tool_outputs.literature_search`
null. Only `labs` is an initial output; CSF, CT, MRI, EEG, microbiology and drug-interaction outputs
are follow-ups.

**Management is a must, never a tool call** (ruling 4):
- Empirical regimen, community-acquired: ceftriaxone 2 g IV every 12 hours or cefotaxime 2 g IV every 6 hours within 60 minutes of clinical suspicion, after blood cultures, never delayed for imaging or LP (WHO 2025 strong; NICE 1.4.1, 1.6.3). Vancomycin is conditional: only where pneumococcal resistance to penicillin or third-generation cephalosporins is highly prevalent locally, so never a must on its own. Cephalosporin hypersensitivity: meropenem 2 g IV every 8 hours (covers Listeria) with vancomycin
- **Listeria cover:** WHO 2025 (recommendation B.2 and its remarks) lists as risk factors age **over 60**, pregnancy, immunosuppressive therapy, organ transplantation, malignancy, advanced HIV disease, diabetes mellitus, end-stage kidney disease, liver cirrhosis and alcohol use disease (diabetes is a Listeria risk factor, not a *severe* immunocompromise for imaging). Any one present: add ampicillin or amoxicillin 2 g IV every 4 hours (WHO strong; NICE 1.6.6). The choice is made before results, so a negative Listeria PCR does not remove it. Never "over 50". With a genuine penicillin allergy, Listeria cover is co-trimoxazole (NICE NG240)
- Healthcare-associated (IDSA 2017): vancomycin plus cefepime, ceftazidime or meropenem (meropenem 2 g IV every 8 hours with Gram-negative rods); remove or replace devices
- **Dexamethasone:** 10 mg IV every 6 hours from just before or with the first antibiotic dose; continue up to 4 days only if S. pneumoniae or H. influenzae type b is identified; **stop it once another organism is identified** (WHO 2025; NICE NG240 1.8.3). Not for Gram-negative healthcare-associated meningitis or cryptococcal disease; TB has its own regimen. Do not continue it after Listeria is identified. In people living with HIV, WHO 2025 applies the recommendation only on ART with an undetectable viral load (below 50 copies/mL) and reports no proven benefit in advanced HIV disease (RP03: not given by default). Where a case continues it for a non-pneumococcal organism (S. suis, RM04), the must states the trade-off and cites [Mai_2007] and [van_Samkar_2015]
- Targeted durations (NICE NG240), written only where the case states one or a note asks: N. meningitidis 5 days; S. pneumoniae 14 days; Hib 10 days; GBS 14 days; L. monocytogenes 21 days
- Hearing: "Arrange formal audiological assessment before discharge, or within 4 weeks of discharge if it cannot be done before (WHO 2025, strong recommendation)": a must, not a tool call. WHO covers every adult with acute meningitis; NICE NG240 1.12.7 agrees but excludes immunocompromised and neurosurgical patients
- **Repeat LP:** only for no clinical recovery on treatment (WHO: 1 week), therapeutic LP in cryptococcal meningitis, or serial EVD sampling; never routine when improving. A kept repeat-LP follow-up carries no LP token in its trigger (`request_therapeutic_csf_drainage`)

## 3. Tools that are typically USELESS

- `order_ct_scan` (`contrast: false`) in type C cases: no section A.4 criterion and no other indication; imaging only delays the LP [WHO_Meningitis_2025]
- `analyze_ecg`: unrelated to meningitis diagnosis
- `order_echocardiogram`: only if endocarditis is suspected as a primary source (e.g. subacute streptococcal bacteraemia); waste otherwise
- `order_cardiac_monitoring`: unrelated
- `order_advanced_imaging` (any modality): none indicated; advanced imaging adds no diagnostic value in routine acute meningitis
- `order_specialized_test` (most types): most don't apply; audiometry is a must, not a scored test

Waste avoided actions cite `[WHO_Meningitis_2025]` with rationales true for the patient.

## 4. Tools that are HARMFUL / contraindicated

- `analyze_csf`: when imaging shows mass effect, midline shift, or basal cistern obliteration (LP can precipitate herniation). Communicating hydrocephalus without a mass lesion or shift is not a contraindication [WHO_Meningitis_2025]

## 5. Sequence constraints

- A cases: `order_ct_scan` → `analyze_csf` (`hard`): "Under WHO 2025 section A.4 cranial imaging is not performed routinely; where readily accessible it precedes lumbar puncture when any of these is present at presentation: Glasgow Coma Score below 10, focal neurological signs, cranial nerve deficits, papilloedema, new-onset seizures in adults, or a severe immunocompromised state. Here: <limb and finding>. <NICE NG240 1.4.7 agrees / does not cover this patient / lists no trigger here; WHO 2025 governs this benchmark.> Blood cultures and the first antibiotic dose with dexamethasone come before imaging, which must not delay them." [WHO_Meningitis_2025]
- A and B cases: `order_microbiology` (blood cultures) → `order_ct_scan` (`soft`): "Blood cultures are taken, and empirical antibiotics with dexamethasone given, before cranial imaging; imaging must not delay treatment (WHO 2025; NICE NG240 1.4.8)." [WHO_Meningitis_2025]
- EVD and other healthcare-associated cases: constraints are `soft` only (sampling an EVD carries no herniation risk) and cite `[IDSA_2017_HCVM]`
- No constraint involves the literature or drug-interaction criteria. Antibiotic timing (blood cultures before the first dose, antibiotics within 60 minutes and never delayed for imaging or LP) is a must, since treatment is not a tool call

Stop rule: `required_before_assessment` = the case's required criteria (no CT id in C cases);
`max_additional_actions` 0.

## 6. Subtype variations

- **M (mild):** community-acquired, immunocompetent adult, classic presentation; standard workup; imaging per section A.4
- **S (standard):** typical adult presentation, may have one risk factor for complicated course; standard workup; MRI or source CT per case
- **P (progressive / severe):** septic shock, severely reduced consciousness, focal signs, complications; CT before LP when an section A.4 criterion is present, MRI may be needed early, ICU-level care. Repeat LP only per the rule in section 2
- **R (reverse / mimic):** viral meningitis (lymphocytic predominance, normal glucose), TB meningitis (subacute, low glucose, high protein, lymphocytic; WHO TB Module 4), fungal (cryptococcal antigen; WHO 2022), drug-induced aseptic, partially-treated bacterial; healthcare-associated cases follow IDSA 2017. TB and cryptococcal cases carry no pyogenic prohibitions or dexamethasone template

## 7. Common red-herring categories and pitfalls

- **Recent antibiotic use:** converts CSF to a "partially treated" pattern (lower PMN%, may have negative Gram stain); does not exclude bacterial meningitis, and makes the blood culture `collected_before_antimicrobials` flag false
- **Petechial rash without fever:** could be other entities, but meningococcaemia must be excluded
- **CSF lymphocyte-predominant early:** possible in early bacterial meningitis (PMN shift happens in hours)
- **Negative Gram stain:** does not exclude bacterial meningitis (sensitivity about 85%, lower after antibiotics); culture and multiplex PCR establish the organism
- **Negative multiplex panel:** never excludes Gram-negative bacillary meningitis or S. suis (non-targets)
- **Normal CT:** does NOT prove safety of LP if clinical signs of herniation risk (papilloedema)
- **Headache wording:** "worst headache of his life" only when SAH is a declared red herring; otherwise "a severe, rapidly worsening diffuse headache"
- **Papilloedema:** not plausible after an illness of hours; remove it where the timeline cannot carry it
- **CT reports:** findings only ("No mass lesion, midline shift, basal cistern effacement or hydrocephalus."); never "No contraindication to lumbar puncture"; a non-contrast CT reports no enhancement
- **Differential:** an alternative the CSF and organism exclude is `low`, with the excluding result in `key_features`

## 8. Allowed citations

- `[WHO_Meningitis_2025]`: WHO guidelines on meningitis diagnosis, treatment and care. Geneva: World Health Organization; 2025 (ISBN 978-92-4-010804-2, verified 24 Oct 2026). Section references are to chapter 3 of the guideline: A.1.1 LP contraindications, A.2.2 CSF reference values, A.4 cranial imaging (a recommendation section, not an annex), B.2 antimicrobials and Listeria risk factors, B.3 corticosteroids, C.4 hearing loss; 1.6.5 Listeria background, 1.7 exclusion criteria
- `[NICE_NG240]`: NICE guideline NG240 (bacterial meningitis and meningococcal disease), 19 March 2024
- `[IDSA_2017_HCVM]`: Tunkel AR et al. IDSA clinical practice guidelines for healthcare-associated ventriculitis and meningitis. Clin Infect Dis 2017;64:e34-e65
- `[CLSI_M100]`: CLSI M100, Performance Standards for Antimicrobial Susceptibility Testing, 36th edition. Wayne, PA: Clinical and Laboratory Standards Institute; 2026 (replaces Ed35; meningitis breakpoints for S. pneumoniae)
- `[WHO_Cryptococcal_2022]`: WHO guidelines on cryptococcal disease in people living with HIV, June 2022
- `[WHO_TB_Module4]`: WHO consolidated guidelines on tuberculosis. Module 4: treatment and care. Geneva: World Health Organization; 2025 (ISBN 978-92-4-010724-3; released 15 April 2025, consolidating the earlier Module 4 documents)
- `[Brouwer_2012]`: Brouwer MC et al. Community-acquired bacterial meningitis in adults. NEJM 2012;367:146-156 (Listeria Gram stain sensitivity; complication imaging)
- `[De_Gans_2002]`: De Gans J, van de Beek D. Dexamethasone in adults with bacterial meningitis. NEJM 2002;347:1549-1556 (background only; the dexamethasone rule cites WHO 2025)
- `[Nigrovic_2007]`: Nigrovic LE et al. Clinical prediction rule for identifying children with CSF pleocytosis at very low risk of bacterial meningitis. JAMA 2007;297:52-60
- `[Mai_2007]`: Mai NTH, Chau TTH, Thwaites G, et al. Dexamethasone in Vietnamese adolescents and adults with bacterial meningitis. N Engl J Med 2007;357:2431-2440 (S. suis dexamethasone trade-off, RM04; cited in prose)
- `[van_Samkar_2015]`: van Samkar A, Brouwer MC, Schultsz C, van der Ende A, van de Beek D. Streptococcus suis meningitis: a systematic review and meta-analysis. PLoS Negl Trop Dis 2015;9(10):e0004191 (hearing loss in 53%; dexamethasone associated with less hearing loss; RM04, cited in prose)
- `[SSC_2021]`: Evans L, Rhodes A, Alhazzani W, et al. Surviving Sepsis Campaign: international guidelines for management of sepsis and septic shock 2021. Crit Care Med 2021;49(11):e1063-e1143 (S02, cited in prose)
- `[CDC_STI_2021]`: Workowski KA, Bachmann LH, Chan PA, et al. Sexually transmitted infections treatment guidelines, 2021. MMWR Recomm Rep 2021;70(4) (syphilis testing in people with HIV; RP03)
- `[Tebruegge_2008]`: Tebruegge M, Curtis N. Epidemiology, etiology, pathogenesis, and diagnosis of recurrent bacterial meningitis. Clin Microbiol Rev 2008;21(3):519-537 (immune work-up of recurrent meningitis; RP04)
- `[IDSA_2013_Vaccination]`: Rubin LG, Levin MJ, Ljungman P, et al. 2013 IDSA clinical practice guideline for vaccination of the immunocompromised host. Clin Infect Dis 2014;58(3):e44-e100 (definition of high-level immunosuppression; RS03, cited in prose)

**Superseded (do not cite; kept for traceability):**
- `[IDSA_2004]`: Tunkel AR et al. Practice guidelines for the management of bacterial meningitis. Clin Infect Dis 2004;39:1267-1284. Superseded by WHO 2025 / NICE NG240 (community-acquired) and IDSA 2017 (healthcare-associated)
- `[ESCMID_2016]`: van de Beek D et al. ESCMID guideline for diagnosis and treatment of acute bacterial meningitis. Clin Microbiol Infect 2016;22(Suppl 3):S37-62. Superseded by WHO 2025 for this benchmark
