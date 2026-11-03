# BACT-MEN: condition plan for the October 2026 review round

Lead plan for the 30 bacterial meningitis cases (BACT-MEN-M01..M05, P01..P05, RM01..RM04,
RP01..RP05, RS01..RS05, S01..S06). Workers follow it case by case so that every case reaches the
same decision. Read `ROUND_POLICY.md` and `PATTERNS.md` first; this plan does not repeat them. All 97
Reviewer 2 notes (all cases `needs_changes`) are listed in section 4 under their case, with the class
of section 2 that resolves them. Reviewer 1 has no BACT-MEN notes.

Baseline measured on 23 October 2026 before any edit: `perfect_agent.py` passes 30/30, but it passes
the criterion label as `clinical_context`, and every label says "LP", so in 18 cases action-3 is
answered by the post-treatment repeat LP (`request_repeat_lp`), not by the index LP (class C1). In
M04, RM04 and RP05 it is answered by a "CSF culture result" follow-up. A pass is therefore not
evidence that the right report is served: always read the `-v` lines.

How to use this plan:

1. Apply every class in section 2 to your case, in order, using the canonical text verbatim where
   one is given (fill `<...>` from the case).
2. Apply the per-case decisions of section 4 (imaging decision, Listeria cover, regimen, notes).
3. Rebuild `action_criteria`, `followup_outputs`, `initial_tool_outputs` and `sequence_constraints`
   as section 3 says.
4. Run `perfect_agent.py CASE -v` and `case_io.py check CASE`; confirm action-3 is answered by
   `request_lumbar_puncture`. Write the log; cite every note id of the case.

Conventions for new text: English, the case's spelling, no em or en dashes (write "0.5 to 0.8"),
"IV", "every 6 hours". Do not invent numbers the case does not need; where a class asks for a new
normal result, choose a plausible value inside the reference range that agrees with age, sex,
renal function and medicines.

---

## 1. Governing guidelines and canonical facts

### 1.1 Which source governs what

| question | source | key |
| --- | --- | --- |
| Community-acquired adult disease: imaging before LP, therapy, steroids, CSF values | WHO guidelines on meningitis diagnosis, treatment and care, 2025 (ISBN 978-92-4-010804-2) | `[WHO_Meningitis_2025]` |
| Concordant UK source, only where in scope | NICE NG240, 19 March 2024 | `[NICE_NG240]` (new) |
| Healthcare-associated ventriculitis and meningitis (EVD, shunt, post-neurosurgery, nosocomial, post-neuraxial procedure) | IDSA 2017 (Tunkel AR et al., Clin Infect Dis 2017;64:e34-e65) | `[IDSA_2017_HCVM]` (new) |
| Pneumococcal susceptibility | CLSI M100 meningitis breakpoints | `[CLSI_M100]` (new) |
| Listeria Gram stain sensitivity (about 33%) only | Brouwer MC et al., 2012 | `[Brouwer_2012]` |
| Dexamethasone trial (background) | De Gans J, van de Beek D, NEJM 2002 | `[De_Gans_2002]` |
| Cryptococcal meningitis in HIV (P03) | WHO cryptococcal disease guidelines, June 2022 | `[WHO_Cryptococcal_2022]` (new) |
| Tuberculous meningitis (P02) | WHO consolidated TB guidelines, Module 4: treatment and care | `[WHO_TB_Module4]` (new, edition to confirm) |

Scope rules (Reviewer 2 rulings): WHO 2025 section 1.7 excludes hospital-acquired, nosocomial and
healthcare-associated meningitis; NICE NG240 excludes intracranial shunts, previous neurosurgery,
brain tumours and people with immunodeficiency (asplenia, immunosuppressive therapy, HIV). So:

- M05 (EVD), RS04 (hospital day 18): IDSA 2017 only. RS02 (VP shunt): WHO 2025 for the disease,
  IDSA 2017 for the shunt. RP02 (after dural puncture): IDSA 2017 for the regimen, WHO A.4 for
  imaging. Immunocompromised hosts (M01-M04, RM01-RM03, RP03, RS03, RS05): WHO 2025 only.
- Where WHO and NICE diverge (severe immunocompromise is a WHO imaging trigger, not a NICE one),
  **WHO governs** and the rationale says so in one sentence.
- IDSA 2004 and ESCMID 2016 are superseded: remove `[IDSA_2004]` from criteria, avoided actions and
  constraints, and the free-text duplicates ("IDSA 2004 §V", "De Gans 2002") from `citations`.

### 1.2 Canonical facts (use these, do not restate them differently)

**Imaging before LP (WHO 2025 Annex A.4).** Cranial imaging is not performed routinely; where readily
accessible it precedes LP if, at presentation: GCS below 10; focal neurological signs; cranial nerve
deficits; papilloedema; new-onset seizures in adults; or a severe immunocompromised state. NICE
NG240 1.4.7: risk factors for an evolving space-occupying lesion, new focal neurological features,
abnormal pupillary reactions, GCS 9 or less, or a progressive and sustained or rapid fall in
consciousness; NICE 1.4.6: do not routinely image before LP; NICE 1.4.8: take bloods, give
antibiotics and stabilise before imaging. **Not criteria in either source: age, "altered mental
status", confusion, diabetes.** Criteria are judged on what is known before the scan.
Severe immunocompromise (Reviewer 2): yes for asplenia (M02, M03 rulings) and advanced HIV with
CD4 68 (RS04); no for prednisone 7.5 mg (M04, RS05), prednisone with weekly methotrexate (RS05),
diabetes (S01, S03), HIV with CD4 312 (RP03), inhaled steroids, undiagnosed CVID (RP01).

**Listeria risk factors.** WHO 2025 section 1.6.5: age over 60, pregnancy, immunocompromised state;
Reviewer 2 counts diabetes mellitus among them (M02, M03, RM01, RM02, RM03 notes) while not counting
it as *severe* immunocompromise for imaging. Any one present: ampicillin or amoxicillin 2 g IV every
4 hours is added to the empirical regimen (WHO strong; NICE 1.6.6). The empirical choice is made
before results, so a negative Listeria PCR does not remove the indication. Age threshold is over 60,
never "over 50". With a genuine penicillin allergy, Listeria cover is co-trimoxazole (NICE NG240).

**Empirical regimen, community-acquired.** Ceftriaxone 2 g IV every 12 hours or cefotaxime 2 g IV
every 6 hours within 60 minutes of clinical suspicion (WHO strong; NICE 1.4.1, 1.6.3), after blood
cultures, never delayed for imaging or LP. Vancomycin is conditional: only where pneumococcal
resistance to penicillin or third-generation cephalosporins is highly prevalent locally (WHO
conditional), so it is never a must on its own. Cephalosporin hypersensitivity (S01, RP02):
meropenem 2 g IV every 8 hours (covers Listeria) with vancomycin.

**Empirical regimen, healthcare-associated (IDSA 2017).** Vancomycin plus cefepime, ceftazidime or
meropenem (meropenem 2 g IV every 8 hours with Gram-negative rods, RS04); remove or replace devices.

**Dexamethasone.** 10 mg IV every 6 hours from just before or with the first antibiotic dose; up
to 4 days only for S. pneumoniae or Hib; stopped for any other organism (WHO 2025; NICE NG240
1.8.3). Not for Gram-negative HCA meningitis (RS04 ruling) or cryptococcal disease; TB has its own
regimen.

**CSF reference values (WHO 2025 A.2.2).** CSF:blood glucose ratio normal 0.5 to 0.8, 0.4 or less
abnormally low. RBC up to 5 cells/microL normal in adults (never "traumatic tap" for 0 to 5).
Lactate: WHO gives no threshold; print "(local laboratory reference <3.5 mmol/L)" in every case.
Gram stain sensitivity: about 85% with wide confidence limits (WHO 2025); Listeria about 33%
(Brouwer 2012). Antigen detection is not among WHO 2025 Box 3.1 recommendations and a positive
result needs culture or molecular confirmation. Multiplex PCR panels do not target S. suis,
Proteus, Klebsiella or other Enterobacterales except E. coli K1.

**Susceptibility (CLSI meningitis breakpoints, S. pneumoniae).** Penicillin: susceptible at MIC 0.06
mg/L or less, resistant at 0.12 or more, no intermediate category. Ceftriaxone: susceptible 0.5 or
less, intermediate 1, resistant 2 or more.

**Targeted therapy durations (NICE NG240).** N. meningitidis 5 days; S. pneumoniae 14 days; Hib 10
days; GBS 14 days; L. monocytogenes 21 days. Write a duration only where the case already states one
or a note asks for it.

**Repeat LP.** Only for no clinical recovery on treatment (WHO: 1 week; ESCMID: 48 hours), therapeutic
LP in cryptococcal meningitis, or serial EVD sampling; never routine when improving.

**Hearing.** Formal audiological assessment before discharge, within 4 weeks of being well enough to
test (NICE NG240): a must, not a tool call.

---

## 2. Error classes in this condition

Notes are cited by their first 8 characters; section 4 gives every full id under its case.

### C1. Index CSF in the initial work-up, repeat LP as the first pathway step (PATTERNS 1; leakage)

- **Wrong**: the index CSF is in `initial_tool_outputs.csf` in 29 cases (not P05). In 19 the first
  follow-up is a post-treatment `request_repeat_lp`: the pathway starts after treatment, the HARD
  constraint is broken before step 2, and the matcher serves the repeat LP to any call that says "LP"
  or "lumbar puncture" (it outranks the initial output). Repeat comparators are wrong (S02, S03).
  Repeat labs (P01, RP02, S02, S04) report treatment the agent has not recommended (ruling 4).
- **Notes**: 607514ae, 9cd4cb49, e5f3a2fd, 8f123213, d0c1d5e4, a20ec899, ece53ab1; pathway parts of
  8c9b0d93 (RM01), 1a8db197 (RM03), 10d64799 (RP02), 00b8d7a0 (RS01), 93e3b1e8 (RP05), 8f75c86a
  (RP04, analyze_csf and MRI never executed), 53397644 (P03, unsatisfiable).
- **Fix (all 30)**:
  1. Move `initial_tool_outputs.csf` to a new follow-up `{tool_name: analyze_csf, trigger_action:
     request_lumbar_puncture}` and set the initial `csf` to null. It is the first `analyze_csf`
     follow-up in the list, placed after the CT where a CT precedes LP. With no initial output the
     harness serves the first unserved follow-up to a bare call, and `request_lumbar_puncture` wins a
     call that names LP. (Checked on a scratch copy of M01: action-3 then receives the index LP.)
  2. Delete the repeat LP follow-up in every case except P03 (therapeutic LP, cryptococcal
     meningitis). Where one is kept, its trigger must carry no LP token: `request_therapeutic_csf_drainage`.
  3. Delete `request_repeat_labs`, `request_repeat_labs_24h`, `request_repeat_labs_48h`,
     `request_repeat_inflammatory_markers` and any post-treatment output.
  4. Where a "CSF culture result" follow-up exists (M04, RM04, RP05), keep it as the second
     `analyze_csf` follow-up, trigger `request_csf_culture_final_report`, containing only the final
     culture identification and susceptibility with the interval ("final report at 48 hours"), not
     a copy of the whole CSF or its interpretation.
  5. In the index CSF, culture reads "Pending" (or "Pending; preliminary growth of <Gram morphology>
     at <n> hours" only if that interval is stated). The multiplex PCR result stays in the index
     report: it answers the `meningitis_panel` the criterion orders.

### C2. Imaging before LP judged on IDSA 2004 criteria (PATTERNS 4 outdated guideline; rulings 1, 8)

- **Wrong**: 27 cases require `order_ct_scan {contrast: false}` with a HARD constraint CT before CSF;
  the CT rationale, the must "Obtain CT head before LP because imaging-first criteria are present
  (altered mental status, ... age >60)", the matching prohibition, a key evidence line and the
  constraint reason all rest on IDSA 2004 ("age >60" in 24 cases, "age >50" in 21). Where a real
  criterion applies, the case names the wrong one. M04 images before treating.
- **Notes**: 287dc755, 18203dd9, f1a4e06a, 17b31064, 5968179a, 2b68c562, 4b70b40c, af3519cd,
  1491cdf3, f73b0114, b760f9e4, 36e776d3; imaging parts of 4b829a78 (P02), 53397644 (P03), 7fdda22c
  (RM04), 65ca8833 (RP01), 10d64799 (RP02), c666b874 (RP03), 8f75c86a (RP04), 93e3b1e8 (RP05),
  00b8d7a0 (RS01), 4f49ce3e (RS02); 792e734f, e0e65ec2 (papilloedema timing), 01bdb495 (S06 GCS).
- **Decision per case**: table 4.0, one of:
  - **A. Imaging-first criterion present**: keep `action-N-order-ct-scan` required, keep the HARD
    constraint CT before CSF with the canonical reason, add a SOFT constraint blood cultures before
    CT, rewrite label, must and prohibition with the canonical texts.
  - **B. No criterion, but CT has another indication** (parameningeal or skull-base source, shunt,
    implant): keep the CT criterion (tier in 4.0), delete the HARD constraint, add the SOFT constraint
    blood cultures before CT, rewrite its label for the real indication, order it after the CSF.
  - **C. No criterion and no other indication**: delete the CT criterion and the HARD constraint,
    remove the id from `required_before_assessment`, delete the CT follow-up, add the avoided action
    (S05 precedent). Panel: CT is optional for this condition, so no exemption is needed.
- **Canonical texts** (A):
  - Constraint reason (hard, `before` = CT, `after` = action-3-analyze-csf, citations
    `["[WHO_Meningitis_2025]"]`, add `"[NICE_NG240]"` only when NICE agrees and the case is in its
    scope): "Under WHO 2025 Annex A.4 cranial imaging is not performed routinely; where readily
    accessible it precedes lumbar puncture when any of these is present at presentation: Glasgow
    Coma Score below 10, focal neurological signs, cranial nerve deficits, papilloedema, new-onset
    seizures in adults, or a severe immunocompromised state. Here: <limb and finding>. <One of:
    'NICE NG240 1.4.7 agrees (<limb>).' / 'NICE NG240 does not cover this patient (<reason>).' /
    'NICE NG240 1.4.7 lists no trigger here; WHO 2025 governs this benchmark.'> Blood cultures and
    the first antibiotic dose with dexamethasone come before imaging, which must not delay them."
  - Soft constraint (`before` = action-2-order-microbiology, `after` = CT criterion, citations
    `["[WHO_Meningitis_2025]"]`): "Blood cultures are taken, and empirical antibiotics with
    dexamethasone given, before cranial imaging; imaging must not delay treatment (WHO 2025; NICE
    NG240 1.4.8)."
  - CT label and rationale: "Non-contrast CT head before lumbar puncture because <limb> (WHO 2025
    Annex A.4), to exclude a mass lesion, midline shift, basal cistern effacement or obstructive
    hydrocephalus; it follows blood cultures and the first antibiotic dose." Expected evidence:
    "Presence or absence of a space-occupying lesion, midline shift, basal cistern effacement or
    hydrocephalus that would contraindicate lumbar puncture." Citation `[WHO_Meningitis_2025]`.
  - Must (replaces the template must): "Take blood cultures and give the first dose of empirical
    antibiotics with dexamethasone before cranial imaging; obtain a CT head before lumbar puncture
    because <limb> (WHO 2025 Annex A.4); neither imaging nor lumbar puncture may delay treatment."
  - Prohibition (replaces the template prohibition): "Do not perform lumbar puncture before cranial
    imaging in this patient: <limb> is an imaging-first criterion under WHO 2025 Annex A.4."
- **Canonical texts** (B and C):
  - Must: "Proceed to lumbar puncture without prior cranial imaging: no WHO 2025 Annex A.4 criterion
    is present (GCS <n>, no focal signs, no cranial nerve deficit, no papilloedema, no new seizure,
    not severely immunocompromised). Age, confusion and diabetes are not imaging criteria."
  - Prohibition: "Do not delay lumbar puncture or antibiotics to obtain a CT head: cranial imaging is
    not routine before lumbar puncture (WHO 2025 Annex A.4; NICE NG240 1.4.6) and no imaging-first
    criterion is present."
  - Avoided action (C only): `{tool_name: order_ct_scan, required_arguments: {contrast: false}}`,
    id `avoid-waste-<n>-order-ct-scan`, severity `waste`, citations `["[WHO_Meningitis_2025]"]`,
    rationale "CT before lumbar puncture is not indicated: no WHO 2025 Annex A.4 criterion is present
    (<same list as the must>). Imaging here only delays the lumbar puncture."
  - B label: "Non-contrast CT of the head with bone windows through the <paranasal sinuses / temporal
    bones / skull base> to identify the parameningeal source; it is not a prerequisite for lumbar
    puncture here (no WHO 2025 Annex A.4 criterion)."
- **Record fixes the decision depends on** (C12): explicit GCS with correct components (M02, RS02,
  RS04, S06), progressive fall in consciousness stated (M01), papilloedema removed where the timeline
  cannot carry it (S02, S04).

### C3. CT reports written for a procedure already done, and contrast mismatches (PATTERNS 3)

- **Wrong**: 28 CT impressions end "No contraindication to lumbar puncture" or "Safe to proceed with
  lumbar puncture" (a management conclusion, after two LPs given C1). `contrast_used: false` with
  post-contrast enhancement in P02, P03, RP03, RS02, RS04, S04. RM01 findings against impression; S04
  CT against MRI on hydrocephalus.
- **Notes**: 48cfc7b4, ec012471, e5f3a2fd (CT part), 0b615209, 48f9e0bd; CT parts of 8c9b0d93
  (RM01), 1a8db197 (RM03), 4f49ce3e (RS02).
- **Fix**: impressions state findings only ("No mass lesion, midline shift, basal cistern effacement
  or hydrocephalus."). Delete every LP-safety sentence. Non-contrast CT: remove enhancement findings
  (a non-contrast CT cannot show them; keep `contrast_used: false` because the criterion orders
  `contrast: false`). Make findings, impression and any MRI agree (RM01: keep the oedema and write
  "mild diffuse cerebral oedema without herniation"; S04: align the CT with the MRI).

### C4. Empirical regimen: template vancomycin plus ceftriaxone, no Listeria cover, allergy conflicts

- **Wrong**: about 20 cases mandate "vancomycin 15-20 mg/kg + ceftriaxone 2 g" regardless of host,
  allergy or setting (drug outputs copy it); Listeria cover missing despite risk factors (often named
  by the case's own literature); ceftriaxone mandated despite allergy (S01, RP02); two regimens in
  RS04; no targeted therapy in RS01.
- **Notes**: 5b00931d, 7a7f4ab9, aedde17d, 690ddd54, ba73014b, 7a299941, 95fadb54; regimen parts of
  8c9b0d93 (RM01), 6e436225 (RM02), 1a8db197 (RM03), 10d64799 (RP02), 779f9ec1 (RS03), 00b8d7a0
  (RS01), 93e3b1e8 (RP05 age threshold).
- **Fix**: replace the template must with the canonical musts below; the Listeria line goes where
  4.0 says "yes"; rewrite every drug-interaction `proposed` and `alternatives` to the same regimen.
- **Canonical musts**:
  - Base: "Give ceftriaxone 2 g IV every 12 hours (or cefotaxime 2 g IV every 6 hours) within 60
    minutes of clinical suspicion, after blood cultures and without waiting for imaging or lumbar
    puncture (WHO 2025, strong recommendation; NICE NG240 1.4.1 and 1.6.3). Add vancomycin only where
    pneumococcal resistance to penicillin or third-generation cephalosporins is highly prevalent
    locally (WHO 2025, conditional recommendation)."
  - Listeria: "Add ampicillin 2 g IV every 4 hours for Listeria monocytogenes cover because of <risk
    factor(s)> (WHO 2025, strong recommendation; NICE NG240 1.6.6)."
  - Cephalosporin hypersensitivity: "Give meropenem 2 g IV every 8 hours with vancomycin within 60
    minutes, withholding ceftriaxone for the documented <reaction> (meropenem also covers Listeria);
    narrow to the isolate's susceptibilities."
  - Healthcare-associated (M05, RS04): "Give vancomycin plus <meropenem 2 g IV every 8 hours |
    cefepime 2 g IV every 8 hours> within 60 minutes, after cultures (IDSA 2017)."
  - Targeted (keep or add one per case): "Narrow therapy once the organism and susceptibilities are
    known: <agent> for <duration per 1.2>."

### C5. Dexamethasone without a stop rule, or given where it does not belong

- **Wrong**: the template must "continue q6h for 4 days in confirmed pneumococcal meningitis" and
  prohibition "Do NOT discontinue dexamethasone solely because the Gram stain is negative ..." (20
  cases) are applied to Listeria (M04, RS05), Hib (RM01, framed as pneumococcal), S. suis (RM04), GBS
  (RS01), meningococcus (S05), Gram-negative HCA (RS04), TB (P02) and cryptococcal disease (P03).
- **Notes**: add8da9a, b31acc34, 7754d72d; dexamethasone parts of 8c9b0d93, 7fdda22c, 00b8d7a0,
  95fadb54, 4b829a78, 53397644.
- **Fix**: delete the template prohibition in all 30. Replace the dexamethasone must with:
  "Give dexamethasone 10 mg IV every 6 hours, starting shortly before or with the first antibiotic
  dose; continue for a maximum of 4 days if S. pneumoniae or H. influenzae type b is identified, and
  stop it once another organism is identified (WHO 2025; NICE NG240 1.8.3)." Then add the case line:
  pneumococcal and Hib cases "Continue for 4 days: <organism> is identified."; other organisms
  "Stop dexamethasone on identification of <organism> (WHO 2025; NICE NG240 1.8.3)." plus, in M04 and
  RS05, a prohibition "Do not continue adjunctive dexamethasone after Listeria monocytogenes is
  identified." RS04: replace with "Adjunctive dexamethasone is not indicated once Gram-negative
  bacillary healthcare-associated meningitis is established." M05: no adjunctive dexamethasone must
  (her maintenance dexamethasone for the tumour is a separate matter). P02 and P03: C15.
- Key evidence "Adjunctive dexamethasone (10 mg IV q6h x 4 days) ... reduces mortality ... in
  pneumococcal meningitis (De Gans 2002)" becomes the canonical sentence above.

### C6. Microbiology reports: timing, pre-treatment flag, boilerplate, organism fields (PATTERNS 3)

- **Wrong**: `collected_before_antimicrobials: true` with "taken before the first antimicrobial dose,
  so the isolate is interpretable" after oral antibiotics or prophylaxis (M01, M02, M03, M05, P04,
  RM01, RM03, RP01, RP02, RP03, RS04, S03, S06; check every history). "Susceptibilities ... are what
  allow empirical therapy to be narrowed" (M02, M03, M04, M05, P05, RP01, S01, S02, S05) is the
  agent's reasoning. Results without a plausible interval (M04 36 and 40 h; P04 "no growth at 5 days"
  upfront; S06). Organism field against findings (M05, RS01, RS05). MIC 0.12 "intermediate" (M02, M03).
- **Notes**: 40333f34, f9aa2045, 0dc0699d, 534b9cf8, 44bb31ec, deec2d03, 9dbac2c3, 790f6cf0;
  microbiology parts of 17b31064, 1b519f0a, 1a8db197, 65ca8833, 10d64799, 00b8d7a0.
- **Fix**:
  1. `collected_before_antimicrobials` is false whenever any antimicrobial (oral course,
     prophylaxis, perioperative, empirical) was taken in the 7 days before collection; state it in
     one line: "Collected before the first IV dose; patient had taken <drug, dose> for <n> days."
     Breakthrough on prophylaxis gets the matching susceptibility line (M05 add TMP-SMX; RS04 already
     resistant to TMP-SMX).
  2. Impression: "<Organism> isolated from <n> of <n> sets at <h> hours; susceptibilities as listed."
     Delete the narrowing and interpretability sentences everywhere.
  3. Every culture result states its interval. Results the agent could not have at the work-up
     decision are reported as available at that interval ("no growth at 48 hours; final report at 5
     days"). The harness serves one blood_culture report per case (the `specimen` discriminator), so
     there is never a preliminary and a final blood culture follow-up.
  4. Organism field equals what the findings show; blood and CSF isolates are not mixed (M05: blood
     no growth both sets; the CSF MSSA goes in the EVD CSF report).
  5. Pneumococcal MICs interpreted with CLSI meningitis breakpoints (1.2).
  6. M04 only (note 40333f34): blood cultures report "No growth at 12 hours; final pending", so
     Listeria is established by the CSF PCR and the CSF culture final report.

### C7. CSF reports: wrong references and interpretive text (PATTERNS 3; leakage kind 1)

- **Wrong**: ratio reference "normal >0.6" (24 cases); RBC 2 to 5 "likely traumatic" (17); lactate
  reference "<2.1" (7) against "<3.5"; interpretations that conclude the diagnosis, pre-empt red
  herrings (M05) or explain panel limits in the result (RM04, RS04); P01 ratio miscomputed; RP05 panel
  silent on non-coverage; RP04 nasal beta-2 transferrin filed as CSF; antigen treated as confirmatory.
- **Notes**: 0bea8222, dbadc9d1, fe5ef318, 931b0cb7, c51315fe, dfe98540, eb13717f, 5cef0a0c; CSF parts
  of 1b519f0a, 7fdda22c, 93e3b1e8, 8f75c86a, c666b874.
- **Fix (canonical strings)**:
  - `glucose_ratio`: "<r> (CSF <x> mg/dL / blood <y> mg/dL; reference 0.5 to 0.8, 0.4 or less
    abnormally low)". Recompute r from the paired values, and use the same paired blood glucose as the
    lab panel.
  - RBC 0 to 5: "<n> cells/microL (within normal limits)".
  - Lactate: "<x> mmol/L (local laboratory reference <3.5 mmol/L)".
  - Interpretation: values and pattern only ("Neutrophilic pleocytosis, raised protein, low glucose
    ratio, Gram-positive diplococci on Gram stain."). No diagnosis, no organism inference beyond what
    the stain or PCR shows, no comment on red herrings, no partial-treatment speculation.
  - Panel result for an organism the panel does not target: "No panel target detected (targets: <list>)."
    The limitation goes in key evidence or a red herring ("a negative multiplex panel never excludes
    Gram-negative bacillary meningitis"), not in the result.
  - Antigen results: keep only where the case uses them deliberately (P01 negative antigen); never
    as the confirming test.

### C8. Studies filed under the wrong tool (PATTERNS 3, 5)

- **Wrong**: CSF PCR under `interpret_labs` `request_pcr_panel` (18 cases); audiometry as
  `order_specialized_test` `baep` (18); under `interpret_labs` also RM01 susceptibility, RS02 shunt
  tap, P02 AFB culture, P03 fungal culture, P02 and P03 ophthalmology.
- **Notes**: 1b519f0a (step 4 redundant); 4f49ce3e (shunt tap).
- **Fix**: delete `request_pcr_panel` (the result lives in the index CSF report, C1); delete
  `request_audiometry` and add the hearing must (1.2): "Arrange formal audiological assessment
  before discharge, and within 4 weeks of being well enough to test (NICE NG240)." Fold RM01
  susceptibility into the blood culture report. RS02 shunt tap becomes an `analyze_csf` follow-up
  `request_shunt_tap` after the index LP (values per section 4). P02 and P03 final cultures: C15.
  Ophthalmology follow-ups: delete; fundoscopy findings belong to the examination.

### C9. Literature and drug-interaction steps (rulings 5, 6; PATTERNS 1, 5)

- **Wrong**: literature criterion recommended in all 30, expecting IDSA 2004, ESCMID 2016, De Gans
  2002; initial literature (M03, P02, P03, S02, S04) echoes it; S06's ESCMID finding is fabricated.
  P01's initial drug block is empty with the expected text as summary. Drug outputs discuss allergies
  the patient lacks (M01, M02, M03), ignore the real one (S01), or use another eGFR (M04).
- **Notes**: 7d5f57bb, ec9ec4dd, 4bb54e3c, 0b3c686b, d308acf2, eed97d31, efd95172; literature parts of
  1b519f0a, 8c9b0d93, 779f9ec1, 7a299941.
- **Fix**:
  1. Delete every `search_medical_literature` criterion, follow-up and initial output (same decision
     as ALS; ruling 5 allows removal). No replacement criterion.
  2. Set `initial_tool_outputs.drug_interactions` to null. `check_drug_interactions` tier per 4.0:
     required only for a concrete allergy, interaction or renal dosing issue; otherwise recommended.
     Expected evidence names the concrete issue, never "No prohibitive interactions; confirmation of
     standard guideline-directed empiric regimen".
  3. Its output checks the case's real regimen (C4) against the real allergies and medicines, and
     agrees with `patient`. Delete filler ("oral contraceptives, not applicable", "valproic acid, not
     currently applicable") and formulary text.
  4. Its follow-up goes after the diagnostic core in the pathway order.

### C10. Differential not updated, or missing the entity the case raises (ruling 7)

- **Wrong**: about 15 cases keep the boilerplate list (viral meningitis and HSV moderate, TB and
  cryptococcal low, SAH very low) after a bacterial CSF with a named organism. Missing entities: M02,
  S04 meningococcal disease; RM03 NPH; RS03 Listeria, GCA; RS01 cervical epidural abscess, vertebral
  osteomyelitis, septic facet arthritis. P05 "status epilepticus" after 90 seconds; P02 and P03 rank
  the wrong infection high.
- **Notes**: 258fbb73, db9626f9, f7d51db9; differential parts of 1a8db197, 779f9ec1, 00b8d7a0, 5d084eab.
- **Fix**: each entry's likelihood reflects the whole case; an alternative the work-up excludes is
  `low` with the excluding result in `key_features` ("excluded: neutrophilic CSF with ratio 0.17 and
  Listeria on PCR"). Add the missing entities above. Spell out "coagulase-negative staphylococci".
  Keep five or six entries.

### C11. Red herrings: undeclared, contradicted, or pointing at a study that does not exist

- **Wrong**: undeclared "worst headache of (his/her) life" (M01, P03, RS03, RS05, S02, S03, S04,
  S05, S06); M01 fever premise contradicted; "sinus mucosal thickening on MRI" with no MRI (M01, M03,
  P01, RM01, RP01, RP02, S01, S02, S03; P05 "confirmed on MRI"); RM03 cites enhancement no study shows;
  RS03 has no block; undeclared absent meningism (RS04) and petechial rash (M02); RP05 glucose trap
  its data cannot produce.
- **Notes**: 3f36b65f, 657dd5f2, 361efa4f; red-herring parts of 17b31064, 5d084eab, 1a8db197,
  779f9ec1, 93e3b1e8.
- **Fix**: rephrase "worst headache of his life" to "a severe, rapidly worsening diffuse headache"
  unless SAH is declared as a red herring (it is not in any case). Point `field_path` at the field
  that holds the finding (sinus thickening is on the CT: `followup_outputs[<ct>].output.findings`);
  delete a red herring whose premise the case contradicts, or fix the premise. Add the missing blocks
  per section 4.

### C12. Patient-record contradictions, arithmetic and narrative leaks (PATTERNS 3; leakage)

- **Notes**: 0b3c686b, d308acf2, eed97d31 (allergy contradictions), 065288ba (occupation), 89cd41ac
  (exposure stated twice), e7625084 (HPI names the differential), c4589441 (irrelevant ethnicity),
  efd95172 (eGFR), 1b2bea2e and 17b31064 (anion gap), 36e776d3, 01bdb495 (GCS components), 792e734f,
  e0e65ec2 (papilloedema at 10 and 18 hours), 3f67586c (serogroup B against MenACWY); RP04 differential
  summing to 104%, RS02 GCS (4f49ce3e), RP03 pauci-cellular CSF (c666b874).
- **Fix**: one version of each fact across patient, reports and ground truth. GCS total equals its
  components and the narrative (V4 confused, V3 inappropriate words, V2 incomprehensible sounds; M5
  localises, M4 withdraws). Anion gap 8 to 16 with the lactate the case reports. eGFR by CKD-EPI 2021
  from the case's creatinine, age and sex. Papilloedema is removed where the illness is shorter than
  days. Narrative ends at findings, never names the competing diagnoses.
- Labs (class extension, all 30): action-1 orders `HIV` and `CMP`, but 28 lab outputs report no HIV
  result and 15 no liver tests. Add a "HIV-1/2 antigen/antibody: non-reactive" line (known HIV: CD4
  and viral load as the case states) and the missing ALT, AST, bilirubin, albumin values, consistent
  with the case.

### C13. Imaging reports in the initial work-up with diagnostic conclusions (leakage kind 1)

- **Wrong**: initial MRI in M04, M05, P02, P03, RM02, RP03, RP04, RS02, RS04, S04, some stating the
  diagnosis or disarming a red herring (M04, M05); initial CT in M05, P02, P03, P05; EEG in P05;
  microbiology in P02, P03, P04.
- **Notes**: 7efcfd89, ab5bdd8e; the "initial workup" parts of 53397644 and 8f75c86a.
- **Fix**: move every initial output except `labs` to a follow-up (MRI `request_mri_brain_contrast`,
  CT `request_ct_head`, EEG `request_eeg`, microbiology `request_blood_cultures`), in pathway order.
  Each of these tools then has a single follow-up, which the harness serves to a bare call. Reduce
  impressions to findings: no differential, no diagnosis, no management.

### C14. Missing actions for complications, source and host (PATTERNS 1, 2)

- **Notes**: 46d5c362, 45c01665 (DIC and shock), c4b392de (catheter), 575f933d (ENT, skull-base CT,
  MRV); 95fadb54 (cryptococcal antigenaemia), 93e3b1e8 (contrast MRI with venography), 00b8d7a0 (spine
  MRI, ulcer), 779f9ec1 (steroid plan, GCA), 3f67586c (MenB).
- **Fix**: criteria where a tool exists (section 3 and 4), musts otherwise. Canonical musts:
  - DIC: "Treat as septic shock with overt DIC: fluid resuscitation and vasopressors to a mean
    arterial pressure of at least 65 mmHg, serial platelets, fibrinogen, INR and D-dimer with
    replacement for bleeding or procedures, serial mapping of purpura, and assess for adrenal
    haemorrhage (Waterhouse-Friderichsen) if shock persists."
  - Source control: "Remove or replace the <device> as soon as antibiotics have started."
  - ENT: "ENT assessment for drainage of the <sinus/mastoid> source and of the bony defect."

### C15. Pyogenic boilerplate in the TB and cryptococcal cases, and contradictory LP bullets

- **Wrong**: P02 (TB) and P03 (cryptococcal) keep pyogenic prohibitions (Gram stain dexamethasone,
  "oral antibiotics alone", "imaging shows mass effect" against their own imaging) and a pneumococcal
  literature action; P02's contrast urticaria is unaddressed beside a required contrast MRI.
- **Notes**: 4b829a78, 53397644.
- **Fix**: delete the pyogenic prohibitions and the "Do NOT proceed to lumbar puncture: imaging shows
  mass effect" bullet; keep the single LP position the teaching pearl states (communicating
  hydrocephalus without a mass lesion or shift is not a contraindication). Rewrite musts per 1.1
  sources (section 4). State the contrast reaction (iodinated) and that gadolinium was given (P02).

### C16. Healthcare-associated cases written as community-acquired (rulings 1, 8)

- **Notes**: 00ce9e6f, 33d97134, 5b645ba4, 931b0cb7; 95fadb54 (RS04), 4f49ce3e (RS02 shunt).
- **Fix**: IDSA 2017 citations; CSF sampled from the EVD (M05) with the label proposed in 33d97134;
  CSF interpretation against post-neurosurgical expectations (IDSA 2017: cell counts and glucose are
  less discriminating after neurosurgery; culture is the reference); the CT before CSF constraint in
  M05 is SOFT (sampling an EVD carries no herniation risk) and cites IDSA 2017.

### C17. Key clinical evidence template lines (grep the left text, replace in every case)

| template starts | replacement |
| --- | --- |
| "CT before LP is mandated when any imaging-first criterion" | the A or B/C must sentence of C2 |
| "Empiric coverage must include vancomycin + ceftriaxone" | "Empirical therapy is ceftriaxone or cefotaxime within 60 minutes, with ampicillin when a Listeria risk factor (age over 60, pregnancy, immunocompromise) is present; vancomycin only where pneumococcal resistance is locally prevalent (WHO 2025)." |
| "A negative CSF Gram stain (sensitivity ~60-90%" | "A negative Gram stain does not exclude bacterial meningitis: sensitivity is about 85% with wide confidence limits (WHO 2025), lower after antibiotics; culture and multiplex PCR establish the organism." |
| "CSF:serum glucose ratio <0.4" | "A CSF:blood glucose ratio of 0.4 or less is abnormally low (WHO 2025 A.2.2) and is more informative than the absolute value, above all in hyperglycaemia." |
| "Antibiotic timing matters" / "Antibiotics MUST precede imaging or LP" | "Antibiotics are given within 60 minutes of suspicion; neither imaging nor lumbar puncture may delay them (WHO 2025; NICE NG240 1.4.1)." |
| "Adjunctive dexamethasone (10 mg IV q6h" | the C5 must sentence |
| "In advanced HIV, bacterial meningitis can present with pauci-cellular CSF" (high-count cases) | delete |

--- | --- |
| "CT before LP is mandated when any imaging-first criterion is present (altered mental status, ...)" | the A or C must sentence of C2 |
| "Empiric coverage must include vancomycin + ceftriaxone in adults; add ampicillin for Listeria coverage if age >50 or immunocompromised." | "Empirical therapy is ceftriaxone or cefotaxime within 60 minutes, with ampicillin when a Listeria risk factor (age over 60, pregnancy, immunocompromise) is present; vancomycin only where pneumococcal resistance is locally prevalent (WHO 2025)." |
| "A negative CSF Gram stain (sensitivity ~60-90% ...) ... multiplex PCR or antigen testing retains sensitivity." | "A negative Gram stain does not exclude bacterial meningitis: sensitivity is about 85% with wide confidence limits (WHO 2025), lower after antibiotics; culture and multiplex PCR establish the organism." |
| "CSF:serum glucose ratio <0.4 is more reliable ..." | "A CSF:blood glucose ratio of 0.4 or less is abnormally low (WHO 2025 A.2.2) and is more informative than the absolute value, above all in hyperglycaemia." |
| "Antibiotics MUST precede imaging or LP if either would delay treatment >60 minutes." | "Antibiotics are given within 60 minutes of suspicion; neither imaging nor lumbar puncture may delay them (WHO 2025; NICE NG240 1.4.1)." |
| "In advanced HIV, bacterial meningitis can present with pauci-cellular CSF ..." (cases with a high count) | delete |

---

## 3. Target pathway and tiers

### 3.1 `action_criteria` order and tiers (keep ids; new ids are descriptive)

| order | criterion | tool / required_arguments | tier |
| --- | --- | --- | --- |
| 1 | `action-1-interpret-labs` | unchanged panels | required |
| 2 | `action-2-order-microbiology` | unchanged `{specimen: blood_culture, before_antimicrobials: true, tests: [...]}` | required |
| 3 | CT (A cases) | `order_ct_scan {contrast: false}` | required |
| 4 | `action-3-analyze-csf` | unchanged arguments (M05: EVD label) | required |
| 5 | CT (B cases), MRI, MR venography, spine MRI, immunology labs | per 4.0 | per 4.0 |
| 6 | `check_drug_interactions` | `{}` | per 4.0 |
| - | `search_medical_literature` | deleted in all 30 | - |

Labels of action-1, 2 and 3 already follow the July 2026 tool guidance: keep them, but remove
`[IDSA_2004]` and free-text duplicates from `citations`.

### 3.2 Follow-ups and initial outputs

- `initial_tool_outputs`: only `labs` stays; `csf`, `ct`, `mri`, `eeg`, `microbiology`,
  `literature_search`, `drug_interactions` become null (C1, C9, C13). `fallback_tool_outputs`
  unchanged unless they contradict the case.
- `followup_outputs` order: blood cultures (`request_blood_cultures`); CT (A cases); index LP
  (`request_lumbar_puncture`); CSF culture final report (M04, RM04, RP05 only); CT (B cases); MRI;
  MR venography; spine MRI; EEG (P05); other diagnostic labs (immunoglobulins, RPR, CrAg); shunt tap
  (RS02); drug-interaction check. Nothing else.
- Deleted everywhere: `request_repeat_lp` (except P03, renamed), repeat labs, `request_pcr_panel`,
  `request_audiometry`, `request_ophtho`, literature follow-ups, `request_sensitivity_testing`.
- `avoided_actions`: keep the waste items with citation `[WHO_Meningitis_2025]` and rationales true
  for the patient; add the CT waste item in C cases (M05 echocardiogram stays waste: no bacteraemia).

### 3.3 Sequence constraints

- A cases: HARD CT before `action-3-analyze-csf` and SOFT `action-2-order-microbiology` before CT
  (C2 texts).
- B cases: SOFT `action-2-order-microbiology` before CT only.
- M05: SOFT CT before CSF (C16) and SOFT blood cultures before CT.
- No constraint involves the literature or drug-interaction criteria.

### 3.4 Stop rule

`required_before_assessment` = the required criteria after the edit (remove the CT id in C cases,
add new required ids). `max_additional_actions` stays 0.

### 3.5 Panel

The generation panel requires labs, CSF and microbiology, all kept; CT, MRI and EEG are optional. No
exemption is needed.

---

## 4. Per-case index

### 4.0 Decision table

Imaging: A = imaging-first criterion (limb named), B = CT kept for another indication, C = no CT.
Listeria: risk factor that makes ampicillin a must ("no" = base regimen only). DDI: tier of
`check_drug_interactions` and the concrete reason when required.

| case | imaging | Listeria cover | regimen notes | DDI |
| --- | --- | --- | --- | --- |
| M01 | A: severe immunocompromise (asplenia, hypogammaglobulinaemia); NICE limb: progressive fall in consciousness | yes: immunocompromise | base | recommended |
| M02 | A: asplenia (WHO); NICE no trigger, WHO governs | yes: diabetes, immunocompromise | base; droplet must (rash) | recommended |
| M03 | A: asplenia (WHO); NICE no trigger, WHO governs | yes: age 68, diabetes, asplenia | base | recommended (allopurinol with ampicillin rash) |
| M04 | A: left CN VI palsy (WHO cranial nerve deficit; NICE new focal feature) | yes: age 71, diabetes, prednisone | base; stop dexamethasone on Listeria | required: CKD 3a dosing (eGFR 54) |
| M05 | SOFT CT before EVD sampling (IDSA 2017) | no (HCA) | vancomycin plus cefepime or meropenem; EVD removal or replacement | recommended |
| P01 | C | no | base | recommended |
| P02 | A: bilateral CN VI and left CN VII palsies (WHO cited for LP safety only) | n/a (TB) | per C15 and P02 entry | required: rifampicin induces levothyroxine metabolism |
| P03 | A: papilloedema (WHO) with WHO's qualifier that LP with opening pressure and CrAg must not be delayed | n/a (cryptococcal) | per P03 entry | recommended |
| P04 | C | no | base | recommended |
| P05 | A: new-onset seizure in an adult and focal signs | yes: age 64 | base | recommended |
| RM01 | A: asplenia (WHO; NICE does not cover) | yes: diabetes, asplenia | base; continue dexamethasone 4 days (Hib) | recommended |
| RM02 | A: focal signs and severe immunosuppression (cyclophosphamide, high-dose prednisolone) | yes: age 61, diabetes, immunosuppression | base | recommended |
| RM03 | A: asplenia and left extensor plantar | yes: age 74, diabetes, asplenia | base | recommended |
| RM04 | A: bilateral CN VIII deficit (WHO lists cranial nerve deficits without qualification; open question Q4) | yes: diabetes | base; stop dexamethasone on S. suis | recommended |
| RP01 | C | no | base | recommended |
| RP02 | A: papilloedema | covered by meropenem | meropenem 2 g IV every 8 hours plus vancomycin (ceftriaxone hypersensitivity; IDSA 2017 post-procedural) | required: ceftriaxone allergy, current sub-meningeal meropenem dose |
| RP03 | A: new-onset seizures in an adult; 2.5 cm frontal lesion | yes: HIV | base | recommended |
| RP04 | B: skull-base CT for the cribriform defect (required) | no | base | recommended |
| RP05 | A: focal signs (left Babinski, facial droop, gaze deviation) | yes: diabetes | ceftriaxone plus ampicillin, or co-trimoxazole if the penicillin allergy is judged genuine | required: reported penicillin allergy |
| RS01 | C | yes: diabetes | base, then penicillin G or ampicillin for GBS | recommended |
| RS02 | A: GCS below 10 after the record fix; shunt assessment (IDSA 2017) | no | base | recommended |
| RS03 | C (prednisolone 30 mg about 2 weeks; open question Q5) | yes: age 74, prednisolone | base | recommended |
| RS04 | A: GCS 9 (E2 V2 M5) and severe immunocompromise (CD4 68) | covered by meropenem | meropenem 2 g IV every 8 hours plus vancomycin (IDSA 2017); remove catheter | required: AKI with tenofovir |
| RS05 | C | yes: age 78, prednisone and methotrexate | base; stop dexamethasone on Listeria | required: penicillins reduce methotrexate clearance |
| S01 | B: sinus CT for the source (recommended) | covered by meropenem | meropenem plus vancomycin (cephalosporin hives) | required: cephalosporin allergy |
| S02 | B: sinus CT for the source (recommended), after papilloedema removal | yes: diabetes | base | recommended |
| S03 | B: CT with bone windows (required) plus contrast MRI and MR venography (required) | yes: age 62, diabetes | base | recommended |
| S04 | B: temporal bone CT (recommended), after papilloedema removal; MRI kept required | yes: diabetes | ceftriaxone (non-severe penicillin rash is not a contraindication) plus co-trimoxazole for Listeria | required: penicillin allergy |
| S05 | C (already) | no | base; stop dexamethasone on meningococcus | recommended |
| S06 | C (optional CT becomes waste) | no | base | recommended |

### BACT-MEN-M01 (man, 55, asplenia and hypogammaglobulinaemia, 2 days of amoxicillin; R2 needs_changes)

- 3f36b65f-bd2d-492b-a0f3-52f4fd4b55ed: C11, rephrase the headache.
- 0b3c686b-9355-48de-8b37-9f2b8f10512d: C9/C12, keep NKDA; drug step "No known drug allergies;
  beta-lactam allergy history explicitly investigated and negative".
- 287dc755-179b-4e4f-a5e9-827ed5d04837: C2 A; mental status states the progressive fall (alert at
  baseline, drowsy by evening, difficult to rouse by morning, GCS 12 on arrival).
- 607514ae-6b9c-4540-8437-cba254ec14cb: C1, delete the repeat LP.
- 48cfc7b4-7b9d-46dc-bf38-0d9597053aed: C3 and C1.
- 5b00931d-6c6b-4ef2-90be-f01e6e073737 and 7a7f4ab9-524e-42cb-b50c-3fb8c51652de: C4 with Listeria.
- 657dd5f2-3c47-44dc-bf09-8292240d0237: C11, withdraw the low-grade fever red herring; the sinus red
  herring points at the CT.

### BACT-MEN-M02 (woman, 42, post-traumatic asplenia, diabetes, 3 days of amoxicillin, petechial rash)

- d308acf2-10de-4fbb-bc5a-d0b1d21a218d, eed97d31-7a7d-4b9e-a852-674e40d85c0d: C9/C12, the drug step
  discusses her contrast allergy, not a penicillin allergy.
- 18203dd9-813a-4f7c-9bc1-41eba2c7caa8: C12, record GCS (E4 V4 M6 = 14); C2 decision rests on asplenia.
- ec012471-c7cc-4e0b-bc6e-32be63a27b0d: C3 and C1.
- aedde17d-13ba-4817-aa43-6cd6ee20e34e: C4 with Listeria.
- 258fbb73-7240-4970-a845-b76b667543e1: C10, add "Meningococcal disease (meningococcal sepsis with or
  without meningitis)" moderate, excluded by N. meningitidis not detected on PCR and S. pneumoniae in
  blood; droplet must (section 4.0).
- f1a4e06a-fa5d-47ee-9477-ca4ffecacad5: C2 A, reviewer's wording is the canonical reason.
- 17b31064-1cb3-4c0c-b825-3fd2016e74f0: C11 (declare the petechial rash as a red herring), C12 (anion
  gap: lower chloride to give 12 to 14), C2, C6 (MIC 0.12 penicillin-resistant by meningitis
  breakpoints, explains amoxicillin failure; ceftriaxone adequate).

### BACT-MEN-M03 (man, 68, asplenia, diabetes, 2 days of amoxicillin, tetracycline photosensitivity)

- 790f6cf0-c6d4-4ffe-99f4-2492093ab211: C6, penicillin MIC 0.12 "resistant (CLSI meningitis
  breakpoints)".
- e5f3a2fd-93dc-4200-b4ff-bd654cf1485e: C1 and C3.
- 5968179a-9eb3-4dc1-a385-eed5502dba63: C2 A with the reviewer's reason; WHO governs over NICE.
- 690ddd54-22f7-4bed-8d03-328d7a84eedb, ba73014b-7f14-4e98-96e9-a86cb3caf5d8: C4, three Listeria
  risk factors.
- 1b519f0a-f3aa-4663-98b1-ef203ddd28c3: C9 (delete initial literature), C1, C7 (antigen and PCR now
  answer the LP order), C8, C4, C6 (pre-antimicrobial flag), drug step allergy text (C9).

### BACT-MEN-M04 (man, 71, Listeria, prednisone 7.5 mg, diabetes, CKD)

- efd95172-e71d-43de-8adf-eb84bec994d1: C12, "Chronic kidney disease stage 3a, estimated GFR 54
  mL/min/1.73m2"; re-derive ampicillin and vancomycin dosing in the drug step.
- 89cd41ac-a333-4a79-806c-af6985404bfb: C12, exposure only in social history.
- 2b68c562-0b82-4234-ba73-93cb134c3c4d: C2 A on the CN VI palsy; fix the must and prohibition too.
- 4b70b40c-2d2f-4cdc-99bf-a31d0ccdcaf2: C2 (soft blood cultures before CT), C3, C1 (CT before LP in
  the list).
- 40333f34-5eb6-42f3-9683-ecab5d1cb9f0: C6 item 6.
- 7efcfd89-6216-478e-818b-1f1e222d3abe: C13.
- add8da9a-5e0f-4bf3-bd35-2e177edf1022: C5 with the Listeria stop must and prohibition.
- 7d5f57bb-28fb-4126-975f-02c61f457f20: C9, literature criterion deleted.
- 0bea8222-5baa-445f-abd1-6c0b876388c6, dbadc9d1-3fcb-4106-b891-cd410cf24a9d, fe5ef318-b083-4055-bd5e-b55ec2a47390: C7.

### BACT-MEN-M05 (woman, 44, EVD after glioblastoma resection, MSSA ventriculitis, TMP-SMX prophylaxis)

- Governing: IDSA 2017 (C16). CT, MRI and EVD CSF move to follow-ups (C13, C1: trigger
  `request_evd_csf_sample` for the index CSF, since there is no LP).
- 00ce9e6f-d7e1-4422-8df9-7723dcfa25ea: C16, CT and CSF in the pathway; SOFT constraint, IDSA 2017.
- 33d97134-f643-4376-ba4d-15f1e91f338d: C16, reviewer's EVD label.
- f9aa2045-68a6-4c45-9749-4c41d53041d2, 0dc0699d-a3bd-4c33-bc40-cb1183d04100: C6 (blood no growth;
  MSSA with TMP-SMX susceptibility in the EVD CSF; prophylaxis stated).
- ab5bdd8e-4df6-43a0-a70f-92a59f0c1c3c: C13.
- c51315fe-3ac8-4de7-b517-a1023da7e3bc: C7.
- e7625084-1890-4e7a-be6b-b6f4cc22c282: C12, delete the last two HPI sentences.
- 5b645ba4-9928-4940-84fe-88218424bdb8: C16, delete the WHO key evidence line.
- 931b0cb7-571e-452f-924b-28428c638556: C7 and C16.
- c4589441-e45b-4f70-a86d-e2b989a4b022: C12, remove "East Asian".
- f7d51db9-d1eb-47b7-ae09-f4762b4f8d7d: C10, spell out.

### BACT-MEN-P01 (man, 35, healthy, Gram stain and antigen negative, PCR positive)

- ece53ab1-9242-4a2c-8a40-bdc635ad3b02: C1, delete the repeat LP and the repeat labs (an improving,
  treated patient has no indication); culture of the index specimen reports S. pneumoniae at 36 hours.
- ec9ec4dd-2739-4e0d-9ac1-048810797b5f: C9.
- 9cd4cb49-c9e4-40a0-8674-1384032c1ba2: C1; constraint deleted (C).
- af3519cd-e7f4-437e-bd5e-8b6f6357463c: C2 C.
- dfe98540-6f4b-4c7d-9fff-5bf9ab41437d: C7, ratio 0.51 from 52.5/102 and one paired glucose across
  CSF and labs.
- 1b2bea2e-4c9b-4f32-894a-759a979a2842: C12, chloride about 95.
- eb13717f-b30a-46cd-9312-01e09a92d84a: C7 lactate reference.
- 5cef0a0c-9a53-4990-b225-15663de01074: C7, reviewer's replacement interpretation; keep the negative
  antigen.
- 065288ba-3ffc-4a92-8fea-a8ab8d6b6e8a: C12, "High school mathematics teacher".

### BACT-MEN-P02 (woman, 42, tuberculous meningitis, A17.0, contrast urticaria, levothyroxine)

- 4b829a78-0714-4017-b03c-ec3d9b634b2a: C15 (one LP position; pyogenic prohibitions and the
  pneumococcal literature action deleted), C2 A with the reviewer's reason (cranial nerve palsies;
  communicating hydrocephalus without shift does not contraindicate LP), C12 contrast reaction.
- Musts per `[WHO_TB_Module4]`: start HRZE without waiting for culture; adjunctive dexamethasone
  tapered over 6 to 8 weeks; CSF AFB smear, Xpert MTB/RIF Ultra and mycobacterial culture; HIV test;
  chest imaging; notify public health. AFB culture result moves from `interpret_labs` into the index
  CSF report as "Pending (mycobacterial culture, final at up to 6 weeks)" (C8); the CSF
  vocabulary has no mycobacterial term (CENTRAL). Ophthalmology follow-up deleted (C8).
- Differential: acute bacterial meningitis falls to low with the excluding data (C10). Open question
  Q1 on the label.

### BACT-MEN-P03 (man, 48, cryptococcal meningoencephalitis, untreated advanced HIV, B45.1)

- 53397644-08bd-4739-8019-50c5fc9047ac: C15 (delete "Do NOT proceed to lumbar puncture"; keep the
  therapeutic LP bullet), C1 and C13 (CSF, CT, MRI out of the initial work-up), C2 A on papilloedema
  with WHO's HIV qualifier in the reason.
- Musts per `[WHO_Cryptococcal_2022]`: induction with single high-dose liposomal amphotericin B 10
  mg/kg plus 14 days of flucytosine 100 mg/kg/day and fluconazole 1200 mg/day (2 weeks of liposomal
  amphotericin B 3 to 4 mg/kg/day with flucytosine is an accepted alternative); therapeutic LP when
  opening pressure is 25 cmH2O or more, repeated daily until stable; no corticosteroids; ART 4 to 6
  weeks after starting antifungal therapy. Keep the repeat LP as `request_therapeutic_csf_drainage`.
- Differential: TB falls to low or moderate with the excluding data (C10). Open question Q1.

### BACT-MEN-P04 (man, 33, partially treated pneumococcal meningitis, amoxicillin 4 days)

- deec2d03-a0be-4278-be8a-4ae8b2df98e8: C6, cultures "no growth at 48 hours; final at 5 days" with
  the interval; microbiology moves to a follow-up (C13).
- Imaging C (alert, no criterion). The must on
  "pneumococcal urinary antigen" becomes "multiplex PCR" (1.2, antigen tests).

### BACT-MEN-P05 (woman, 64, focal seizure and right hemiparesis, GCS 11)

- 5d084eab-ee89-4a4b-856b-f04cbe38e5c3: C10, "Acute ischaemic stroke with a post-ictal deficit";
  C11, delete "and confirmed on MRI".
- Already has the index CSF as `request_csf_analysis`: rename to `request_lumbar_puncture` and put it
  after the CT. CT and EEG move from the initial work-up (C13); EEG stays optional.

### BACT-MEN-RM01 (man, 52, asplenia, Hib, sulfonamide allergy, amoxicillin)

- 8c9b0d93-e27c-438c-9fba-e5d3264746a9: C5 ("S. pneumoniae or H. influenzae type b" wording,
  continue 4 days); C11 sinus red herring; C1 (CT first in the A order, CSF out of the initial
  work-up); C3 (oedema findings against impression); C4 (no vancomycin, add ampicillin); C9.

### BACT-MEN-RM02 (man, 61, prednisolone 20 mg after a 60 mg pulse, cyclophosphamide 10 days ago)

- 6e436225-b347-4cca-89c1-627ff45ae9e8: scope WHO only (1.1); C4 with ampicillin, vancomycin
  conditional (ceftriaxone MIC 0.5 or less). MRI stays recommended, moves to a follow-up (C13).

### BACT-MEN-RM03 (woman, 74, ITP splenectomy, NPH-like presentation, amoxicillin-clavulanate 3 days)

- 1a8db197-d724-4a60-a5e0-3e6e62616063: scope WHO only; C11 NPH interpretation with the reviewer's
  text; C10 add NPH at high as ruled (it is the mimic the case is built on), with
  key_features naming the CSF that shows it is not the sole cause, and drop cryptococcal meningitis; C4 with ampicillin; C1 and C3; C6 "before first intravenous dose;
  patient had received oral amoxicillin-clavulanate for 3 days prior".

### BACT-MEN-RM04 (man, 56, S. suis, bilateral CN VIII deficit, pig handling)

- 7fdda22c-2f7d-4caf-ae22-e4656a3e30b5: C2 A per 4.0 (the must "CT before LP is not mandated ..." is rewritten; if Andrea answers
  Q4 the other way, keep C with the reviewer's softened wording and the stated reason that cochlear
  injury is not a sign of mass effect); C7 panel result "No panel target detected"; C5 reassessment
  on S. suis; hearing must already present, keep it in the canonical wording.
- CSF culture speciation follow-up becomes `request_csf_culture_final_report` (C1 item 4).

### BACT-MEN-RP01 (woman, 49, undiagnosed CVID, amoxicillin-clavulanate 5 days)

- 65ca8833-9e95-4d73-8436-55ec977ec77a: C2 C; C6 "false, 5 days of oral amoxicillin-clavulanate
  before sampling".
- The label names CVID: add `interpret_labs {panels: [quantitative_Ig]}` as required (id
  `action-5-interpret-labs-immunoglobulins`) answered by the existing `request_immunoglobulin_levels`.

### BACT-MEN-RP02 (woman, 22, post-dural-puncture pneumococcal meningitis, ceftriaxone allergy, on meropenem 1 g)

- 10d64799-c48c-4aaa-984c-1519f29d9f52: C4 (meropenem 2 g plus vancomycin, ceftriaxone withheld);
  C1 (CT before LP in the list); C2 A on papilloedema; C6 "false, on meropenem and vancomycin at the
  time of sampling"; medication entry "meropenem 1 g every 8 hours, prophylactic dosing with
  sub-meningeal CSF exposure".

### BACT-MEN-RP03 (man, 42, HIV CD4 312, seizures, frontal lesion, co-trimoxazole and fluconazole)

- c666b874-9e5a-4a0f-a451-fe497e3f3e87: C2 A on seizures and the lesion; C12 pauci-cellular CSF:
  state partial treatment by co-trimoxazole 960 mg daily (antipneumococcal) in the CSF context and
  the history; keep CD4 312. C6 pre-antimicrobial flag false. C3 contrast mismatch.

### BACT-MEN-RP04 (man, 28, recurrent pneumococcal meningitis, CSF rhinorrhoea)

- 8f75c86a-41e8-45e9-a036-98ce1b1e9cf3: beta-2 transferrin out of the CSF report into its own step
  with turnaround (needs CENTRAL vocabulary; until it exists, remove it from the CSF and log the
  case BLOCKED on that item, never file it under another assay); C2 B (skull-base CT required for the
  defect, HARD constraint deleted); C1 and C13 (CSF and MRI become pathway steps); C12 differential
  to 100% with a monocyte line. Immune work-up follow-up gets a recommended `interpret_labs`
  criterion (`quantitative_Ig`, `complement`).

### BACT-MEN-RP05 (man, 54, Klebsiella, otomastoiditis, focal signs, glucose 312, penicillin allergy unclear)

- 93e3b1e8-570a-4b6f-8c6c-90366179e2a7: C7 panel coverage text and red herring "a negative multiplex
  panel never excludes Gram-negative bacillary meningitis"; add `analyze_brain_mri {contrast: true}`
  and `order_advanced_imaging {modality: MR_venography}` as required with musts (subdural empyema,
  abscess, sigmoid sinus thrombosis); C11 glucose pearl reworded ("in hyperglycaemia the ratio, not
  the absolute value, is decisive; here 8 over 312 gives 0.026"); C1; C2 A on focal signs ("age >50"
  deleted); Listeria threshold over 60 (ampicillin still indicated on diabetes, 4.0).

### BACT-MEN-RS01 (man, 59, GBS, 15 days of torticollis, venous stasis ulcer)

- 00b8d7a0-db3d-4b7d-8f3c-5e3cc009d410: C6 organism "Streptococcus agalactiae"; C1 delete repeat LP;
  add `order_body_imaging {study: spine_MRI, contrast: true}` required (cervical epidural abscess,
  vertebral osteomyelitis, septic facet arthritis) and those three in the differential; C4/C5
  targeted GBS therapy (penicillin G or ampicillin 14 days, gentamicin optional first days;
  dexamethasone stopped on GBS); C2 C; wound assessment, culture and source control must, ulcer
  named as the portal in key evidence (`wound_swab` needs CENTRAL; until then a must only).

### BACT-MEN-RS02 (man, 38, VP shunt, pneumococcal, chronic left hemiparesis)

- 4f49ce3e-d3e3-4e3c-b82e-d8b1924cb62e: shunt tap moved to `analyze_csf` `request_shunt_tap` with
  values that keep a plausible ventriculo-lumbar gradient (raised cells and protein, low glucose,
  sterile culture) or stated as taken after 48 hours of therapy (C8); C3 contrast mismatch; C2 A
  with the reviewer's rescue: record GCS below 10 (E2 V3 M4 = 9) and rewrite mental status and motor
  text to match (eyes open to pain only, inappropriate words, withdraws to pain; chronic left
  weakness), shunt assessment per IDSA 2017.

### BACT-MEN-RS03 (man, 74, prednisolone 30 mg for "PMR", IgA MGUS)

- 779f9ec1-e8f6-4601-8700-9943f3c27e6d: C4 with ampicillin; Listeria into the differential; GCA
  declared as a red herring with the interpretation, plus a must for temporal artery assessment
  after the acute phase; prednisolone plan "resume or taper prednisolone at the end of the
  dexamethasone course; do not stop abruptly"; add the red-herring block (PMR label, IgA MGUS,
  intrathecal IgA synthesis); C9 literature deleted; age threshold over 60. Imaging C (Q5).

### BACT-MEN-RS04 (woman, 25, HIV CD4 68, treated TBM, hospital day 18, Proteus, urinary catheter)

- Read in full. Accepted labels include Listeria and "community acquired" synonyms (CENTRAL).
- 95fadb54-c24c-468f-a321-41a70d579120: C4 (delete vancomycin plus ceftriaxone, meropenem first),
  C5 (dexamethasone not indicated), C14 (serum CrAg 1:4: pre-emptive fluconazole and repeat CSF CrAg
  as musts).
- c4b392de-6b45-48f8-abbf-2bdb62280cce: C14 catheter removal or replacement.
- 36e776d3-230f-41dc-95a3-8476bd91ab74: C12 GCS E2 V2 M5 = 9 (incomprehensible sounds, localises);
  C2 A on GCS below 10 and CD4 68.
- 0b615209-0fd8-4228-bd20-ec129a3e7d14: C3.
- 534b9cf8-0ada-477c-badf-35843aa8e7f1: C6 "false, on cotrimoxazole prophylaxis"; isolate resistant to
  TMP-SMX explains the breakthrough.
- 361efa4f-ffce-4125-8eca-d9cca632a699: C17 delete the pauci-cellular pearl; C11 declare absent
  meningism as a red herring.

### BACT-MEN-RS05 (woman, 78, Listeria, prednisone 7.5 mg and methotrexate)

- b31acc34-bc1e-4e06-95ec-a642788726a4: C5 (stop on Listeria).
- b760f9e4-ea41-474b-bd8b-5c886f0e75ea: C2 C (constraint and CT criterion removed, waste added).
- 44bb31ec-78d2-41bf-bec1-ddc7c92d6884: C6 bottle count.

### BACT-MEN-S01 (man, 45, cephalosporin hives, sinus source)

- 7a299941-e461-4153-87d4-2cd3be3784a9: C4 meropenem plus vancomycin; narrow to penicillin G or
  ampicillin on susceptibility; drug step checks the antibiotics (C9).
- 8f123213-29b0-45d0-b081-df1013d4bb05: C1.
- 7e72aa2c-a9db-4ad5-8f48-18fe26b39079: the note is a ruling on the label (ruling 3): change
  "(otogenic/sinugenic source)" to "(sinugenic source)" in `accepted[0]`, remove "otogenic" from the
  ground truth, and log it; `icd_codes[0]` stays G00.1, so the synonyms are unaffected.
- 1491cdf3-4b2c-4b48-8981-e8764909734d: C2, B (sinus CT recommended, no HARD constraint).

### BACT-MEN-S02 (woman, 38, sinusitis 4 days, diabetes, BP 90/54)

- d0c1d5e4-e8b3-4dde-8e68-2ebb58f90bf7: C1 (repeat LP deleted, so the comparators go with it).
- 792e734f-3498-4183-b30d-6fe44ae12566: C12 remove the papilloedema (replace with "discs not
  visualised clearly owing to photophobia" or normal fundi); CT "no cerebral oedema" vs opening
  pressure 35 stays (not contradictory). Imaging B.

### BACT-MEN-S03 (man, 62, sinus source, ethmoid bone erosion)

- 575f933d-efaf-4ee0-b722-ffd5bca2057e: C14, add `analyze_brain_mri {contrast: true}` and
  `order_advanced_imaging {modality: MR_venography}` required; CT kept required as B with bone
  windows; ENT must.
- a20ec899-5b21-412b-958f-51268a8bac67: C1 (repeat LP deleted).
- f73b0114-418c-40ae-98fc-628eac2aea85: C2, B (no HARD constraint).

### BACT-MEN-S04 (man, 38, pneumococcal ventriculitis, cochlear implant, penicillin rash, DIC)

- db9626f9-ba27-491e-97a8-0acc7313b152: C10 add meningococcal disease at high as ruled, key_features
  naming the rash and the S. pneumoniae isolate; droplet must.
- e0e65ec2-ac48-45a7-af36-ae5db8379cd8: C12 papilloedema replaced by sluggish pupils and the raised
  opening pressure; imaging B.
- 48f9e0bd-a9df-4860-b937-4989f5c4aca6: C3.
- 46d5c362-1a51-4992-a83e-83a1dcca9a2e: C14 septic shock with overt DIC.
- MRI with a cochlear implant: the MRI report states the implant is MRI-conditional and the
  manufacturer protocol was followed (or the worker logs the conflict).

### BACT-MEN-S05 (woman, 19, meningococcal, dormitory, MenACWY at 11)

- Read in full. Already C for imaging; vancomycin MIC line "Not applicable" stays (Gram-negative).
- 3f67586c-846f-4a99-b0a8-400c58349e37: C12/C14, state that MenACWY does not cover serogroup B, so
  this is not vaccine failure; MenB vaccine bears on what contacts are offered.
- 7754d72d-0dce-4fe1-949d-75b4610f9a36: C5, stop dexamethasone on meningococcal confirmation.
- 45c01665-cad3-4c28-ad27-95f662ae2d29: C14 DIC as present.
- Also: labs lack HIV and LFT (C12 labs); "worst of her life" (C11).

### BACT-MEN-S06 (man, 50, pneumococcal, otitis treated 3 weeks ago)

- 9dbac2c3-8927-4f9b-9bdb-b47a78656ba6: C1 (CSF out of the initial work-up; culture pending; PCR
  answers the LP's panel), C6 (blood culture intervals stated).
- 01bdb495-bfb3-4588-a022-02fdadebcdd0: C12 GCS 15 (E4 V5 M6).
- 4bb54e3c-d711-48a2-b480-737bc71867d9: C9 (literature deleted, so the fabricated finding goes).
- Imaging C: optional CT criterion deleted, waste added.

---

## 5. CENTRAL requests (outside the case files)

1. **Citation keys** for the criteria pack allow-list: `[NICE_NG240]`, `[IDSA_2017_HCVM]`,
   `[CLSI_M100]`, `[WHO_Cryptococcal_2022]`, `[WHO_TB_Module4]` (edition to confirm), and
   `[WHO_Meningitis_2025]`, which the cases use but the pack lacks.
2. **Criteria pack `BACT-MEN.md`**: replace the IDSA 2004 imaging list (age over 60) with WHO 2025
   Annex A.4 and NICE 1.4.7; regimen, Listeria threshold, dexamethasone stop rule, scope rules and
   CSF reference values as in 1.2.
3. **`conditions.yaml`** bacterial_meningitis `common_followups`: remove `request_repeat_lp`,
   `request_pcr_panel` and `request_audiometry`, the generators of C1 and C8.
4. **Vocabulary** (`costs.yaml`, `tool_io.py` mirror, fallback library): `order_specialized_test`
   `audiometry`; `analyze_csf` `mycobacterial_panel` (AFB smear, Xpert MTB/RIF Ultra, culture),
   `fungal_culture`, `india_ink`, `lactate`, `ADA`; `interpret_labs` `beta2_transferrin` (RP04),
   `serum_cryptococcal_antigen` (RS04, P03, RM02), `CD4_count`, `HIV_viral_load` (also asked by ALS);
   `order_microbiology` `wound_swab` (RS01) and `sputum` (P02) moved from the general_medicine pack.
5. **Diagnosis synonyms**: `G00.8` carries Listeria labels, so Proteus (RS04), Klebsiella (RP05)
   and S. suis (RM04) accept "listeria meningitis". Listeria meningitis is A32.1: move the labels to
   an `A32.1` entry, recode M04 and RS05 to A32.1, give `G00.8` neutral labels, consider G00.2 for
   S. suis, and strip the appended Listeria labels from RS04, RP05, RM04 (the script only adds).
   `G00` adds "community acquired bacterial meningitis" to the healthcare-associated M05 and RS04.
6. **Follow-up matcher**: an LP call token-matches `request_repeat_lp`, which outranks the initial
   output, so every agent writing "lumbar puncture" received the post-treatment repeat LP first. A
   test that no repeat-study trigger shares a meaningful token with the index study of the same tool
   would stop this in other conditions.
7. **Review UI**: criterion order for initial and follow-up outputs (already requested); only `labs`
   stays initial in BACT-MEN.
8. **Fallback library**: check CSF, CT and literature fallbacks for "normal >0.6", "traumatic tap",
   "No contraindication to lumbar puncture" and IDSA 2004 criteria.
9. **Test**: no BACT-MEN case contains "age >60" or "age >50" as a criterion, "normal >0.6",
   "likely traumatic" for 5 RBC or fewer, or the narrowing boilerplate.

---

## 6. Open questions for Andrea

- **Q1.** P02 (TB, A17.0) and P03 (cryptococcal, B45.1) stay in `bacterial_meningitis` as mimics with
  their own pathways (ruling 3). Move them to another condition instead?
- **Q2.** CT as `waste` in no-criterion cases (P01, P04, RP01, RS01, RS03, RS05, S05, S06), following
  S05; or no avoided action, only the must and prohibition?
- **Q3.** WHO 2025 governs where it diverges from NICE (asplenia as an imaging trigger: M02, M03,
  RM01, RM03), as the reviewer proposed. Confirm the benchmark is WHO-first.
- **Q4.** RM04 bilateral CN VIII deficit: CT required (WHO lists cranial nerve deficits without
  qualification), or the reviewer's alternative, no CT with the reason that cochlear injury is not a
  sign of mass effect?
- **Q5.** RS03 prednisolone 30 mg for about two weeks is not counted as WHO's severe
  immunocompromise (consistent with M04 and RS05), so no pre-LP CT. Doses of 20 mg or more for 14
  days are often called high-level immunosuppression. Confirm.
- **Q6.** S02 and S04 papilloedema removed (10 and 18 hours of illness), turning both from A to B;
  or extend the prodrome and keep the CT requirement?
- **Q7.** Diabetes as a Listeria risk factor (Reviewer 2, five notes) makes ampicillin a must in 18
  cases, including S02 (38) and RP05 (54). Confirm this reading of WHO 2025 section 1.6.5.
- **Q8.** Recode M04 and RS05 to A32.1 and RM04 to G00.2 without a reviewer ruling (CENTRAL 5)?
- **Q9.** Literature criterion removed in all 30, as in ALS. Confirm.
