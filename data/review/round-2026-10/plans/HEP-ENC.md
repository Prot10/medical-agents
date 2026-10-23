# HEP-ENC: condition plan for the October 2026 review round

This is the lead plan for the 30 hepatic encephalopathy cases (HEP-ENC-M01..M10, P01..P09,
S01..S11; there is no R-series). Workers follow it case by case so that every case reaches the same
decision. Read `ROUND_POLICY.md` and `PATTERNS.md` first; this plan does not repeat them.

**The notes.** All 88 are Reviewer 2 case comments with no field path; Reviewer 1 has not reviewed
HEP-ENC. Section 4 lists every note with the class (section 2) that resolves it.

**Case status.**
- P09, S01 and S09 were approved before this round: change them only for the real errors that
  section 4 names.
- S10 has no notes.

**Baseline (23 Oct 2026, before any edit).** `perfect_agent.py` passes 30/30. It warns in M01,
M02, M08, M09, M10, S01-S06 and S08 that the `interpret_labs` paracentesis criterion is answered by
the core lab report: its `{}` arguments match any labs call (C6).

**How to use this plan.**
1. Apply every class of section 2 to your case, in order. Use the canonical texts verbatim and fill
   the `<...>` slots from the case.
2. Apply the per-case decisions of section 4.
3. Rebuild `action_criteria`, `followup_outputs`, `sequence_constraints` and `stop_rule` as section
   3 says.
4. Run both checks, write the log and cite every note id.

Section 2 cites notes by their first 8 characters; section 4 gives the full ids. "F<n>" is the
current position of a follow-up and "a<n>" is criterion `action-<n>-...` as the case stands before
editing.

**Conventions for new text.**
- English, in the case's own spelling.
- No em or en dashes (write "to" or a hyphen).
- Units as the case already uses them.
- Invent no number the case does not need. A new value must be plausible, differ from the other
  cases, and agree with the rest of the case.

---

## 1. Governing guidelines and canonical facts

### 1.1 Sources and citation keys

| question | source | key |
| --- | --- | --- |
| Definitions, grading, covert/overt, ammonia, imaging triggers, lactulose target, rifaximin, theragnostic review | Bajaj JS, Jakab SS, Jesudian AB, et al. ACG Clinical Guideline: Hepatic Encephalopathy. Am J Gastroenterol 2026;121:588-618 | `[ACG_HE_2026]` (new) |
| Same, European view | Montagnese S et al. EASL CPG on the management of hepatic encephalopathy. J Hepatol 2022;77:807-824 | `[EASL_HE_2022]` (new) |
| West Haven grades, type A/B/C | Vilstrup H et al. Hepatology 2014;60:715-735; Ferenci P et al. Hepatology 2002;35:716-721 | `[AASLD_2014]`, `[Ferenci_2002]` |
| Ascites, paracentesis, SBP, albumin, AKI | EASL CPG decompensated cirrhosis, J Hepatol 2018;69:406-460; Biggins SW et al., Hepatology 2021;74:1014-1048 | `[EASL_decomp_2018]`, `[AASLD_ascites_2021]` (new) |
| Variceal bleeding | de Franchis R et al. Baveno VII, J Hepatol 2022;76:959-974 | `[Baveno_VII]` (new) |
| Alcohol-related hepatitis, withdrawal, Lille | EASL CPG alcohol-related liver disease, J Hepatol 2018;69:154-181; Louvet A et al., Hepatology 2007;45:1348-1354 | `[EASL_ALD_2018]`, `[Lille_2007]` (new) |
| Wernicke | Galvin R et al. EFNS guidelines, Eur J Neurol 2010;17:1408-1418 | `[EFNS_Wernicke_2010]` (new) |
| Status epilepticus (P06) | Glauser T et al. AES guideline, Epilepsy Curr 2016;16:48-61 | `[AES_2016]` (new) |
| Post-ictal CK (P06) | Brigo F et al. J Neurol 2015;262:251-257 | `[Brigo_2015]` (new) |
| Wilson disease (P04) | Schilsky ML et al. AASLD 2022 practice guidance, Hepatology 2023;77:1428-1455 (verify before use) | `[AASLD_Wilson_2022]` (new) |
| MELD-Na | Kim WR et al. NEJM 2008;359:1018-1026 | `[Kim_MELDNa_2008]` (new) |
| Background | Wijdicks EF. NEJM 2016;375:1660-1670 | `[Wijdicks_2016]` |

New keys go to CENTRAL 1.

**Which source governs.** ACG 2026 and EASL 2022 govern wherever they differ from the 2014
guideline: they are current, and the reviewer cites them.

**Superseded keys.** `[EASL_2010]` becomes `[EASL_decomp_2018]`; `[Bajaj_2011]` becomes
`[ACG_HE_2026]`.

**Citation lists** take one bracketed key per source and no free text. Delete "AASLD/EASL 2014 HE
practice guideline", "Bajaj 2011 HE management review", "Ferenci 2002 HE nomenclature/
quantification" and similar strings wherever they sit beside a key (29 cases).

### 1.2 Canonical facts

- **Covert and overt HE**
  - Covert HE is minimal HE or West Haven grade 1; overt HE is grade 2 or higher (ACG 2026 key
    concept 1).
  - Grade 2: lethargy, disorientation to time, asterixis. Grade 3: somnolent but rousable, grossly
    disoriented. Grade 4: coma.
  - Where a label gives a range, the exam must support the upper bound; otherwise use the lower.
- **Ferenci type**
  - A: acute liver failure.
  - B: portosystemic bypass without intrinsic liver disease.
  - C: cirrhosis, with or without a shunt.
- **Ammonia**
  - Ammonia neither grades nor confirms HE. Repeat levels never measure response (ACG 2026
    recommendation 5, key concept 14).
  - A normal ammonia in a confused cirrhotic should prompt a search for another cause (EASL 2022).
  - Reference range for the condition: **11-51 µmol/L**.
- **Lactulose and rifaximin**
  - Lactulose is titrated to **2-3 soft bowel movements per day** (ACG 2026 recommendation 10;
    EASL 2022). Over-titration causes dehydration, hypokalaemia and AKI.
  - Rifaximin 550 mg twice daily is added after a recurrent overt episode.
  - The response is reviewed for adherence and symptoms at 4-8 weeks (ACG 2026 key concept 8). It
    is not a 72-hour test.
- **Brain imaging and EEG**
  - Brain imaging is not routine in cirrhosis with confusion (ACG 2026 recommendation 6). Its
    triggers are a new focal deficit, seizure, head trauma, an atypical first episode, or no
    response to treatment.
  - CT cannot show restricted diffusion. Cirrhotic pallidal change is a T1 MRI hyperintensity, not
    a CT hypodensity. Putaminal CT hypodensity in Wilson disease is acceptable.
  - EEG in HE shows diffuse slowing, with or without triphasic waves. NCSE is excluded by the EEG,
    never by a benzodiazepine challenge.
- **Paracentesis**
  - Do a diagnostic paracentesis in every hospitalised cirrhotic with ascites who has
    encephalopathy, GI bleeding, infection, or worsening liver or renal function (EASL 2018; AASLD
    2021).
  - SBP is an ascitic PMN count of 250 cells/mm3 or more.
- **Infection**
  - Infection is the commonest precipitant of overt HE and can be occult.
  - Cultures are mandatory with fever, leucocytosis or a source. Otherwise they are a reasonable
    screen.
- **Zinc**
  - Zinc deficiency, not excess, is associated with HE (zinc is a cofactor of urea-cycle enzymes).
  - Excess zinc causes copper deficiency (anaemia, neutropenia, myeloneuropathy), not HE.
- **Post-ictal CK** rises after some hours and peaks at 24-72 hours (Brigo 2015).
- **Child-Pugh points**

  | | 1 point | 2 points | 3 points |
  | --- | --- | --- | --- |
  | Bilirubin (mg/dL) | <2 | 2-3 | >3 |
  | Albumin (g/dL) | >3.5 | 2.8-3.5 | <2.8 |
  | INR | <1.7 | 1.7-2.3 | >2.3 |
  | Ascites | none | mild | moderate/severe |
  | HE | none (minimal HE counts as none) | grade 1-2 | grade 3-4 |

  Class A is 5-6 points, B is 7-9, C is 10-15.
- **MELD and MELD-Na** (UNOS, as the reviewers computed)
  - MELD = round(10 x (0.957 ln Cr + 0.378 ln bili + 1.120 ln INR + 0.643)).
  - Values below 1 count as 1; creatinine is capped at 4.
  - If MELD > 11: MELD-Na = MELD + 1.32 x (137 - Na) - 0.033 x MELD x (137 - Na), with Na bounded
    to 125-137.

---

## 2. Error classes

Apply every class to every case unless the class says otherwise. Each class gives: what is wrong,
the notes, the fix and the canonical text.

### C1. Treatment, consults and treatment response delivered through diagnostic tools (ruling 4)

**What is wrong.** The generation panel's `common_followups` (CENTRAL 3) seeded every case with
follow-ups of three kinds:

- **Effects of management the agent has not yet recommended:**
  - `interpret_labs` `request_lactulose_rifaximin` (falling ammonia, GCS rise, "partial
    response");
  - `request_thiamine_empiric`;
  - `request_liver_transplant_evaluation`;
  - treatment or consult outputs: M04 nutrition and day-7 Lille; M06 potassium repletion; M08 AFP
    trend; M10 endoscopy consult; P09 partial response; S05 ceftriaxone and HBV resistance; S09
    48-hour repeat tap; S11 restart response.
- **Treatments filed as drug-interaction checks:** M03 (thyroid treatment, and a methadone check
  for a drug she does not take), M05 (pruritus), P04 (Wilson treatment), P05 (coeliac nutrition),
  P07 (CPAP) and S02 (rifaximin insurance).
- **Treatments filed as specialised tests, and drug challenges:**
  - specialised tests: S04 endoscopy, S06 withdrawal monitoring;
  - challenges: lorazepam during EEG (M01 F3, S08 F3) and naloxone (S07 F2);
  - P06 post-treatment EEGs (F2, F5).

**Notes.** dec0d57a, 22fa5945 (M01); e18c72da (M04); e9c07b1d (P01); 8ee3aef0 (P04); a4e6f322
(S07); 3559f393 (S02); and the C2 notes.

**Fix.**
- Delete the follow-ups that section 4 lists under "Delete", and any criterion that pointed at
  them. Never convert one into another tool call.
- Their content becomes a must or a prohibition (C16).
- Pre-treatment values that the diagnosis needs stay in the initial report of the right tool:
  - thiamine level in the M04, P05 and S06 initial labs;
  - Wilson MRI in P04 `mri`;
  - NCSE EEG in P06 `eeg`.
- Delete red herrings and pearls built on a challenge (M01 lorazepam, S07 naloxone).

### C2. Ammonia used as a treatment marker; reference range not uniform

**What is wrong.**
- Serial ammonia is reported as the measure of response in 26 cases.
- The reference range is:
  - 11-51 in 26 cases;
  - 11-45 in P07, where the same 48 µmol/L is described three ways;
  - 11-35 in S08-S10;
  - "umol/L" in S11.

**Notes.** cbd4a868 (M04), 3cb39ca8 (M05), 3e28b7bf (M06), 0ea62416 (M07), fa503581 (M08),
fea3c98c (M10), 1b529040 (P01), fbc4826d (P02), 8ee3aef0 (P04), 0f54d6e7 (P05), 68f03868 (P06),
8a4256a7, 41f02bb6 (P07), 65f1c0dd (S11).

**Fix.**
- Keep one admission ammonia in the core labs, range 11-51 µmol/L, with `is_abnormal` recomputed.
- Delete every serial value and every "ammonia falling to X confirms response" (HPI, key evidence,
  pearls, red herrings, expected evidence).

**K-AMM (pearl).** "An elevated ammonia neither grades nor confirms hepatic encephalopathy and
repeat levels are not used to guide treatment; a normal ammonia in a confused patient with
cirrhosis should prompt a search for another cause (ACG 2026 recommendation 5 and key concept 14;
EASL 2022)." `["[ACG_HE_2026]", "[EASL_HE_2022]"]`.

### C3. Lactulose target 2-4 or 3-4 stools per day

**What is wrong.**
- The musts give 2-4 in M01-M05, M07-M10, S02, S03, S05, S07 and S09-S11, and also in S11 F1 and
  M09 F3.
- M05 F1 gives 3-4; P09's musts give 3-4.
- P01-P03 give no target at all.

**Notes.** 0ea62416 (M07), 8479a4e1 (M08), d279f19b (M09), f4f73be0 (M10), 8da6b4b7 (P01),
9d18794f (P02), dac2b026 (P03), 7ed60ff7 (P09), a6ec2282 (S02), b177af3e (S11).

**MUST-LACT (all 30).** "Lactulose 25 mL every 1-2 hours until at least two soft bowel movements,
then titrated to 2-3 soft bowel movements per day (ACG 2026 recommendation 10; EASL 2022); avoid
over-titration, which causes dehydration, hypokalaemia and kidney injury."

**MUST-LACT-OVERUSE (M06, S02).** "Reduce lactulose to the dose that gives 2-3 soft bowel movements
per day (currently <n> loose stools per day with potassium <K>); correct potassium and volume, and
investigate persisting diarrhoea rather than attributing it to lactulose." In S02, add "including
stool testing for Clostridioides difficile after recent antibiotics".

**Rifaximin (recurrent episodes only).** "Rifaximin 550 mg twice daily with lactulose to prevent
recurrence (ACG 2026; EASL 2022)."

### C4. Literature search (ruling 5)

**What is wrong.**
- The literature search is required in M03, M05, M07, M09, M10, P02, P03, P08, P09, S07 and S11,
  and recommended elsewhere.
- The initial output echoes the expected evidence ("AASLD/EASL 2014 guidance retrieved...") in
  about 25 cases.
- Literature follow-ups stand in for consults (P02 psychiatry, P03 goals of care, S07 HCV
  treatment) or carry wrong claims (M05 zinc-arginase, S11 2-4).

**Notes.** cf6cd213 (M05), b177af3e (S11).

**Fix (all 30, as ALS).**
- Delete the criterion, set `initial_tool_outputs.literature_search` to null, and delete every
  literature follow-up.
- Their clinical content becomes musts.

### C5. Drug-interaction checks (ruling 6)

**What is wrong.**
- The check is required in 23 cases with no concrete interaction.
- The initial blocks in M01, S01 and S04-S08 are empty templates whose summary is the expected
  evidence.
- Some checks are treatments (C1).
- M02 F4 doses lorazepam; M09 F3 repeats the 2-4 target.

**Notes.** 9037c7e6 (M02), a8504264 (S04).

**Fix.**
- Each case gets one output: a follow-up whose trigger names the drugs (for example
  `check_clonazepam_quetiapine`).
- Set `initial_tool_outputs.drug_interactions` to null and place the follow-up last.
- The output lists only what changes management: the patient's medicines against the drugs in the
  musts, the allergies, and renal or hepatic dosing.
- **Tier.** Required only where section 4 names a concrete issue. Otherwise optional, with a short
  real output: "no clinically relevant interaction between lactulose, rifaximin and the current
  medicines; avoid sedatives".
- **Allergy wording.**
  - A non-severe penicillin rash does not contraindicate ceftriaxone (low cross-reactivity): give it
    with monitoring.
  - Penicillin anaphylaxis (P03) needs an alternative, or specialist advice before any beta-lactam.

### C6. Paracentesis duplicated, without ascites, or missing

**What is wrong.**
- An `interpret_labs` `{}` criterion duplicates the `order_microbiology` `ascitic_fluid` criterion,
  and their expected texts conflict (M01, M02, M08, M09, M10, S01-S06, S08, S09).
- `interpret_labs` taps are reported in patients without ascites (M05 F2, P01 F5, P02 F4, P05 F5,
  P06 F4).
- Ascites is present but there is no criterion, and the tap is filed under `interpret_labs` (M03,
  M07, P03, P04, P09, S07, S10, S11).

**Notes.** 6a7d6fa7 (M01), c0f7b456 (M02), d07af885 (P05), 65351710 (P06).

**Fix.**
- **Ascites present** (M01-M03, M07-M10, P03, P04, P09, S01-S11): one criterion,
  `order_microbiology` `{"specimen": "ascitic_fluid"}`, required.
  - Keep the existing id; new id `action-diagnostic-paracentesis`.
  - Label: "Diagnostic paracentesis: cell count with differential, total protein and albumin, Gram
    stain and culture in blood-culture bottles".
  - Expected evidence: "Ascitic PMN <n> cells/mm3, <above/below> the 250 cells/mm3 threshold for
    SBP".
  - Rationale: "Every hospitalised patient with cirrhosis, ascites and encephalopathy needs a
    diagnostic paracentesis to exclude SBP" `["[EASL_decomp_2018]", "[AASLD_ascites_2021]"]`.
  - Output: one `order_microbiology` follow-up, `request_diagnostic_paracentesis`, specimen
    `ascitic_fluid`.
- **No ascites** (M04, M05, M06, P01, P02, P05, P06, P07, P08): no criterion and no output. If
  M04's exam documents ascites, treat M04 as ascites present and log it.
- Delete every `interpret_labs` paracentesis criterion and follow-up.

### C7. Blood and urine cultures: tier, arguments, contradictory blocks

**What is wrong.**
- All 30 require blood cultures "before the first antimicrobial dose" and urine cultures, with
  `before_antimicrobials: true`, including afebrile patients with a normal WBC and no antibiotic
  anywhere in the case.
- Microbiology blocks contradict themselves:
  - S03 and S11 initial blocks (`blood_culture`) mix urinalysis, urine and blood cultures, lactate
    and ethanol.
  - S03 and S05 urine cultures are positive in one place and "no growth" in F6.
  - S05 shows E. coli in a blood block that excludes bacteraemia.
  - S01's ascitic culture reads "Pending, E. coli at 48 h" while its impression says isolated.
  - S09's Gram stain shows Gram-negative rods while its impression says "No organism isolated".
  - M09's admission labs report a urine culture "No growth at 24 hours" on the day it was sent.
  - Every block carries the same "No organism isolated to date. Specimen taken before the first
    antimicrobial dose."

**Notes.**
- Tier: 9a959a80 (M05), f90a4875 (M06), 5a318475 (M07), fed6c71c (M10), 72abc830 (P01), e4e6c46c
  (P02), 73e5a38f (P04), 7689f42d (P05), 780fd2f8 (P06), 409e1c57 (S07), 8465dace (P08).
- Integrity: b56d3db7 (M09), bb58b696 (S03), 2fd43a55 (S05), 170d2c1e (filed on S06, describes
  S05), d2b65d04 (S09).

**Tier rule.**
- **Required** when the temperature is 38.0 °C or more, the WBC is above 11 x10^9/L, or an
  infective precipitant is in the label or HPI: M02, M04, M08, M09, P09, S01-S05, S08, S09.
- **Recommended** otherwise: M01, M03, M05-M07, M10, P01-P07, S06, S07, S10, S11. P06's WBC of 11.2
  is post-ictal, and the note rules it.
- **P08:** blood cultures optional; delete the urine culture criterion and output (the urinalysis is
  clean).

**Criteria.**
- Arguments: `{"specimen": "blood_culture"}` and `{"specimen": "urine"}` only. Drop
  `before_antimicrobials` and the `tests` lists, which subset matching turned into three mandatory
  tests.
- **Required labels.** "Blood cultures, two sets, before the first antimicrobial dose" and
  "Urinalysis and urine culture before the first antimicrobial dose".
  - Must: "Blood, urine and ascitic cultures are drawn before the first antibiotic dose, which is
    not delayed for them."
- **Recommended labels.** "Blood cultures as part of the infection screen for an occult
  precipitant", and the same wording for urine culture.
  - Rationale: "Infection is the commonest precipitant of overt HE and can be occult in cirrhosis;
    this patient is afebrile with a normal white cell count and no focal source, so the screen is
    recommended rather than required (EASL 2022)."
  - Delete the culture musts, and delete "Do not hold antibiotics waiting for culture" where no
    infection is suspected.
- **Expected evidence:** the case's own result ("no growth at 48 hours", or "E. coli in 2 of 2
  sets, susceptible to ceftriaxone"), not the shared text.

**Blocks.**
- **One specimen per output.**
  - The initial `microbiology` holds blood cultures only.
  - Urine is follow-up `request_urine_specimen`, specimen `urine`.
  - Ascitic fluid is handled per C6.
  - Urinalysis, lactate and ethanol move to the labs.
- **One time point per block, consistent across organism, findings and impression.** Either a
  final organism with its susceptibility, or "no growth at 48 hours" with the organism null. Never
  "pending" beside a final result.
- "Collected before antibiotics" only when the case gives an antibiotic and the sample preceded it.
- No culture result in the admission panel.

### C8. Brain imaging and EEG reports

**What is wrong.**
- **MRI.**
  - MRI follow-ups are filed under `order_advanced_imaging` (M01 F6, M08 F4, P03 F1, P04 F1,
    P05 F2). In P04 and P05 the required `analyze_brain_mri` therefore gets a normal initial `mri`
    that contradicts the positive report.
  - M04 and P03-P05 MRIs contain the line "No mass, midline shift or herniation, the finding the
    lumbar puncture is gated on" (scoring rationale in the data).
- **CT.**
  - Empty `findings`.
  - "Restricted diffusion" appears on CT in 26 cases.
  - S04-S07 report pallidal or basal ganglia hypodensity.
- **M01** has a gadolinium MRI and an LP (CSF criterion, F8 "see impression") with no indication.
- **P07's EEG** calls a PDR of 8 Hz both "low-normal" and abnormal, with two normal ranges.

**Notes.** 22fa5945 (M01), 0a2f64af (M02, CT part), 0fffd88b (M04), caa0c178 (P05), d848bfa7
(P07).

**Fix.**
- **MRI.** One report per case, in `initial_tool_outputs.mri`:
  - P03: contrast MRI, no leptomeningeal enhancement or metastasis.
  - P04: Wilson pattern (T2 hyperintensity of the putamina, thalami and midbrain; pallidal T1
    hyperintensity).
  - P05: Wernicke pattern (symmetric T2/FLAIR hyperintensity of the medial thalami, periaqueductal
    grey and mammillary bodies).
  - P08: F1, moved to initial.
  - M04: its own report.
  - Delete the MRI follow-ups in cases without an MRI criterion (M01 F6, M08 F4, S08 F6, S10 F5);
    the fallback library answers an unrequested MRI.
  - Delete the "lumbar puncture is gated on" line.
  - Fill `findings` with one item per finding.
- **Normal CT.**
  - findings `[{"type": "normal", "location": "brain", "description": "No intracranial
    haemorrhage, mass, extra-axial collection or acute infarct. Grey-white differentiation
    preserved. Ventricles and sulci appropriate for age. No midline shift."}]`, impression "No
    acute intracranial abnormality." Keep a case-specific atrophy finding.
  - Delete "restricted diffusion" from every CT and the pallidal hypodensity in S04-S07. P04's
    putaminal hypodensity stays.
- **M01.** Delete the CSF criterion, F8 and the CT-before-CSF constraint; CT stays optional.
- **Tiers** (July 2026 guidance):
  - CT required in M10, P06, P08, P09, S11; optional elsewhere.
  - MRI required in M04, P03, P04, P05, P08.
  - EEG recommended where it exists; required in P06 (C15).
- **P07 EEG.** "Posterior dominant rhythm 7.5 Hz, below the adult lower limit of 8 Hz, with
  intermittent diffuse theta; mild diffuse slowing consistent with a metabolic encephalopathy."
  Classify it abnormal and state one normal range.
- **Continuous-EEG follow-ups** (M01 F3, P01 F3, S08 F3, S09 F4, S10 F3): delete any that hold a
  challenge or a post-treatment change. Otherwise merge the content into the initial `eeg` and
  delete the follow-up.

### C9. Laboratory reports: template carry-over, "Exclusion studies", duplicates

**What is wrong.**
- **Templates pasted by the July 2026 addition.**
  - TSH 2.1 mIU/L and "Serum zinc 82 µg/dL" in all 30.
  - Toxicology "Blood ethanol Not detected / UDS Negative" in 17.
  - An "Exclusion studies" block in 25, with values given as "Within reference range" (no number)
    and a templated `clinical_significance`.
- **Resulting contradictions.**
  - M03: TSH 8.4 vs 2.1.
  - M05: TSH 3.8 vs 2.1; zinc 180 vs 82.
  - P02: ethanol 22 vs not detected.
  - P05: B12 188 vs "normal"; magnesium reported twice.
  - P06: ethanol reported twice; CK "normal" after a GTC.
  - P07: TSH reported twice.
  - S03: lactate "normal" in hypotensive bacteraemia.
  - S08: ethanol 142 vs not detected.
  - M04, M07: glucose reported twice.
- **Missing values.** CRP is absent in 29 cases (present only in S09). M04 and P05 have no
  creatinine.
- **Over-strict criterion.** The core lab criterion demands 9-12 named panels, so subset matching
  fails a complete work-up that omits zinc.

**Notes.** b8fd889d (M03), da6eb54c, a11d6f3d (M05), 5fa6804b (P02), 067d3743 (P05), d4cc8148
(P06), 23004ad1 (P07), 998fed4f (S03), cb1f2bae (S08).

**Fix.**
- **One entry per analyte,** in its proper panel, each with a number, unit, range and correct flag.
- **Delete the "Exclusion studies" block.** Its analytes move to their panels with real values:
  - lactate raised in S03 (for example 3.4 mmol/L);
  - P06 CK by timing: raised if the GTC was more than about 6 hours before sampling; otherwise
    normal, with "CK peaks 24-72 h after a seizure (Brigo 2015)" in key evidence. Log FIXED or
    partly DECLINED accordingly.
- **Keep each case's own value:** M03 TSH 8.4 with fT4 0.7; M05 TSH 3.8 and zinc 180; P02 ethanol
  22; P05 B12 188 and a single magnesium; S08 ethanol 142.
- **Elsewhere,** report TSH, zinc and toxicology once each, with values that fit the case and differ
  between cases. Ethanol is detectable only where recent drinking is described.
- **Add CRP** in all 30, consistent with infection; **add creatinine** in M04 and P05.
- **Criterion `required_arguments`.**
  - Alternative 1: `{"panels": ["CBC", "CMP", "coagulation", "ammonia"]}`.
  - Alternative 2: `{"panels": ["CBC", "BMP", "LFTs", "coagulation", "ammonia"]}`.
  - Both alternatives add the case extras from section 4.
  - Label: "Core laboratory work-up: blood count, electrolytes, renal and liver function, glucose,
    INR, ammonia and CRP, with toxicology where alcohol or drugs are in question".
  - The report keeps the July results; the criterion no longer demands them (CENTRAL 4, Q4).
- **Summary fields.** `abnormal_values_summary` and `interpretation` list only flagged values.

### C10. MELD and Child-Pugh not derivable from the case's values

**What is wrong.** The stated scores disagree with the printed values in all 30. Examples:
- S01: MELD 22 stated, 36 computed.
- S04: 26 stated, 36 computed.
- S06: 24 stated, 34 computed.
- S08: 18 stated, 29 computed.
- M02 gives three figures and "Child-Pugh A".
- P03 states class A and class B.
- Most cases with grade 2 or worse HE plus ascites call themselves class B.

**Notes.** 0a2f64af (M02), d4a0da8d (S01), 632aabc9 (S02), 85b833e1 (S03), 0ddd13be (S04),
55bba229 (S05), 988c74d2 (filed on S06, describes S05), 5dd96024 (S08), 498272a4 (S09).

**Fix (all 30).** This is a reviewer-ruled class, so `accepted[0]` changes too (ruling 3; CENTRAL
6).
- Recompute with 1.2 from the printed labs: the HE points use the current grade, the ascites points
  use the exam.
- Replace every current score: in `accepted[0]`, history, key evidence, reports, pearls and musts.
  - `accepted[0]`: "Child-Pugh <class>, MELD-Na <n>".
  - Key evidence: "Child-Pugh <class> (<points>: bilirubin <x> <p>, albumin <x> <p>, INR <x> <p>,
    <ascites> <p>, HE grade <g> <p>); MELD-Na <n> (creatinine <x>, bilirubin <x>, INR <x>, sodium
    <x>)".
- A prior score stays only if dated as prior.
- Update musts whose indication depends on the class (transplant referral).
- Never change `icd_codes`.
- Section 4 gives the computed MELD and MELD-Na and the Child-Pugh class. Check the ascites and HE
  points against the exam.

### C11. HE grade and type labels

**What is wrong.**
- P01 is labelled "grade I-II, overt, evolving from covert".
- P03 is grade II but its red herring and a pearl call it covert.
- P08 says "type B/C" in pearls, key evidence, expected evidence and F2, but the patient has
  cirrhosis.

**Notes.** 41da0ede (P01), 4e8a2b60 (P03), ee768920 (P08).

**Fix.**
- **P01** `accepted[0]`: "Overt hepatic encephalopathy (West Haven grade II), cryptogenic cirrhosis
  (Child-Pugh B, MELD-Na 13), precipitated by clonazepam accumulation ...". Keep the rest of the
  precipitant text and confirm grade II from the exam.
- **P03** red herring: "A mildly raised ammonia does not grade HE; the grade is clinical (West
  Haven grade II, overt)". Delete "covert" from the pearl.
- **P08:** "type C" everywhere.
- **Pearl in P01, P03 and P07:** the covert/overt sentence of 1.2, `[ACG_HE_2026]`.

### C12. Boilerplate prohibitions that contradict the patient

**What is wrong.**
- **Benzodiazepine/haloperidol prohibition.** 25 cases carry "Do not prescribe benzodiazepines ...
  (use haloperidol ... for agitation)". It contradicts:
  - P02 (haloperidol dystonia);
  - P04 (Wilson extrapyramidal disease);
  - P06 (NCSE, where benzodiazepines are first-line);
  - M01, M02 and M04, which give or permit lorazepam.
- **Generic LP prohibition** in cases with no LP.
- **M08** both recommends and forbids an antidiarrhoeal.
- **Ceftriaxone with penicillin allergy:** S04, S08 and S11 give ceftriaxone despite the allergy,
  without comment.

**Notes.** dec0d57a (M01), 9037c7e6 (M02), 6cff687b (P02), b15cdee4 (P04), 18b8f3eb (M08),
a8504264 (S04), af008448 (S01, airway).

**Fix.**
- **PROHIB-BZD** (replaces prohibition 0): "Do not give benzodiazepines or other sedatives for
  agitation or sleep: they precipitate and prolong hepatic encephalopathy; manage agitation with
  reorientation, a safe environment and treatment of the precipitant (EASL 2022)."
- **PROHIB-BZD-WD** (M02, M04, S06, and any case with active withdrawal; replaces both
  benzodiazepine lines): "Do not give scheduled or long-acting benzodiazepines; treat alcohol
  withdrawal symptom-triggered with the lowest effective dose of lorazepam or oxazepam and close
  monitoring of consciousness (EASL ALD 2018)."
- **PROHIB-BZD-SZ** (P06): "Do not withhold a benzodiazepine for seizure termination because of
  hepatic encephalopathy (lorazepam 0.1 mg/kg IV, up to 4 mg per dose; AES 2016); avoid
  benzodiazepines for agitation or sedation."
- **LP and acetaminophen.** Delete the generic LP prohibition; P09 keeps its SDH-specific line.
  Write acetaminophen as "up to 2 g per day".
- **M08** must: "Hold sorafenib until the diarrhoea settles, then resume at a reduced dose with
  oncology; avoid loperamide while lactulose treats HE". Delete the "continue with antidiarrhoeal"
  alternative.
- **Penicillin rash with ceftriaxone** (S04, S08, S11, wherever a must gives ceftriaxone): append
  "the penicillin allergy (rash) is not a contraindication: cross-reactivity with ceftriaxone is
  low; give with monitoring".
- **S01 airway must:** "Protect the airway: GCS 10 with a diminished gag reflex, agitation, active
  variceal bleeding and tense ascites; intubate for airway protection before endoscopy rather than
  waiting for a GCS below 8 (Baveno VII)."

### C13. Timeline leaks in the patient block

**What is wrong.** The HPI or exam states results of scored studies: M01 urine toxicology; M02
ethanol 14 (twice); M04 CT; M05 ammonia, zinc; P01, P03, P07 and S02 ammonia, CT, EEG; P02
ammonia, valproate, and "lithium pending" beside a resulted 1.6; P04, P05, S01 and S04 ammonia; S03
urinalysis, ammonia; S05 urinalysis, ammonia, EEG, CT; S06 ethanol, ammonia; S07 ammonia, EEG,
"WBC normal".

**Notes.** 38ed2d53 (P02).

**Fix.**
- Remove the results and keep the facts ("recent drinking", "on valproate").
- Dated pre-encounter data stays: M07 EMS glucose, S10 labs from a week earlier, P08 prior MRIs and
  echo, M02 "MELD 18 three weeks ago".

### C14. Differential and red herrings not updated (ruling 7)

**What is wrong.**
- SBP stays moderate after PMN < 250 (S02, S03, S05, S06, S08, M08).
- M09 rates "HE without identified infection" high despite PMN 412.
- M10 rates ICH moderate after a normal CT, and uraemia moderate with Cr 1.3.
- S01 rates SDH moderate after a normal CT.
- P08 rates TIA and NCSE moderate after MRI and EEG.
- M01 lists hyponatraemia as an alternative.
- P09 calls the SDH the "primary cause".
- S02's red herring describes 37.x °C and a normal WBC; the case has 38.2 °C and leucocytosis.
- M08's red herring withholds antibiotics in a febrile patient.

**Notes.** b8268eb9 (S02), 391bf9ac (M08, red herring part).

**Fix.**
- Excluded alternatives become `low`, with `key_features` naming the excluding result.
- M01: hyponatraemia (Na 128) is a co-precipitant.
- P09: the chronic SDH is a concurrent contributor (`moderate`), not the primary cause.
- S02 red herring: "Fever 38.2 °C with leucocytosis after a recent respiratory illness may be
  attributed to a viral infection; with ascites and HE, SBP must still be excluded by
  paracentesis."
- M08: delete "withhold antibiotics" (C15).

### C15. Abnormal findings left without work-up

| case | fix | notes |
| --- | --- | --- |
| P06 | EEG `analyze_eeg` `{}` **required** and in the stop rule; initial `eeg` shows the pre-treatment NCSE (Salzburg criteria) | 68f03868 (context) |
| S05 | New `action-renal-ultrasound`, `order_body_imaging` `{"study": "pelvis_abdomen_ultrasound"}`, **required** (loin pain, AKI, E. coli UTI); initial `body_imaging` states hydronephrosis and perinephric collection present or absent, consistently | 36bd67da (filed on S06) |
| M06 | TIPS Doppler `order_body_imaging` `{"study": "pelvis_abdomen_ultrasound"}` **required**; F1 moves to initial `body_imaging`; velocity clearly patent (for example 120 cm/s, range stated) | 167526a9 |
| P08 | New `action-abdominal-shunt-imaging`, `order_body_imaging` `{"study": "pelvis_abdomen_CT", "contrast": true}`, alternatives `pelvis_abdomen_MRI` and `pelvis_abdomen_ultrasound`, **recommended** (optional if the HPI gives dated shunt imaging); initial `body_imaging` shows the splenorenal shunt | ee768920 (context) |
| M08 | Labs extra `urinalysis`; urine culture required; must "chest radiograph and examination for a source; start empirical antibiotics if fever persists without a source" (CENTRAL 5) | 391bf9ac |
| S02 | Must "stool testing for Clostridioides difficile toxin and a chest radiograph" (CENTRAL 5) | dd9192d8 |

### C16. Treatment musts; "No action delivers treatment" (ruling 4)

**Notes.** 43f8f665 (P09), 3559f393 (S02), 1720c3d7 (S03), e9c07b1d (P01).

**Ruling.** DECLINED by design: treatment is scored through the musts, never as a tool call. The S03
referral criterion "with no tool" no longer exists: ALREADY-FIXED, confirm.

**Fix.** Make each must specific and checkable. Canonical musts:
- **MUST-PRECIP:** "Identify and treat the precipitant: <precipitant and its specific treatment>."
- **MUST-SBP:** "Treat SBP with IV ceftriaxone 2 g daily (or cefotaxime), adjusted to culture, plus
  albumin 1.5 g/kg on day 1 and 1 g/kg on day 3; repeat paracentesis at 48 hours if there is no
  clinical improvement (EASL 2018)." Include the albumin only when Cr > 1 mg/dL or bilirubin > 4
  mg/dL.
- **MUST-VB:** "Variceal bleeding: vasoactive drug now, ceftriaxone 1 g daily for up to 7 days,
  restrictive transfusion to haemoglobin 7-8 g/dL, upper endoscopy within 12 hours after
  resuscitation (Baveno VII)."
- **MUST-SEPSIS** (S03, S05): "Sepsis care: cultures then IV antibiotic within one hour, volume
  with albumin, monitor lactate, urine output and creatinine, ICU review if hypotension persists
  (EASL 2018)."
- **MUST-K:** "Replace potassium to 4.0 mmol/L or more, because hypokalaemia increases renal
  ammoniagenesis; hold or reduce the responsible diuretic."
- **MUST-THIA:** "Give parenteral thiamine before any glucose." For Wernicke (P05, and M04 if
  suspected): "thiamine 200 mg IV three times daily (EFNS 2010)".
- **MUST-TX:** "Refer for liver transplant assessment: decompensated cirrhosis with overt HE,
  MELD-Na <n> (EASL 2018)." It replaces the deleted transplant panels.
- **MUST-THERAG** (P01): "Start lactulose titrated to 2-3 soft bowel movements per day, taper
  clonazepam under supervision, and review adherence and symptoms at 4-8 weeks; failure to improve
  with adherence should prompt reconsideration of the diagnosis (ACG 2026 key concept 8)."
- **M04 Lille:** "Calculate the Lille score on day 7 of prednisolone and stop it if the score is
  0.45 or more (Louvet 2007)."

### C17. Criterion mechanics, rationale, citations (own finding, all 30)

**What is wrong.** Every rationale repeats its label.

**Fix.**
- Write one sentence saying why the step is indicated in this patient, with its key.
- Apply the citation rules of 1.1.
- Core labs: "Confirms liver dysfunction and identifies metabolic and infective precipitants
  [ACG_HE_2026]".
- CT: "<the 1.2 trigger present>; excludes haemorrhage or mass [ACG_HE_2026]".
- EEG: "Diffuse slowing supports a metabolic encephalopathy and excludes non-convulsive seizures
  [EASL_HE_2022]".

---

## 3. Target pathway and tiers

### 3.1 `action_criteria` order (keep each `criterion_id`)

| order | tool / arguments | tier |
| --- | --- | --- |
| 1 | `interpret_labs` core (C9) | required, all 30 |
| 2 | `order_microbiology` `{"specimen": "blood_culture"}` | per C7 (P08 optional) |
| 3 | `order_microbiology` `{"specimen": "ascitic_fluid"}` | required with ascites (C6) |
| 4 | `order_microbiology` `{"specimen": "urine"}` | per C7 (P08 deleted) |
| 5 | `order_ct_scan` `{}` | required M10, P06, P08, P09, S11; optional elsewhere |
| 6 | `analyze_brain_mri` `{}` | required M04, P03, P04, P05, P08 |
| 7 | `analyze_eeg` `{}` (drop `eeg_type`, `duration`) | required P06; otherwise recommended where present |
| 8 | Case-specific steps (see note below) | as stated |
| 9 | `check_drug_interactions` | per C5 |
| - | `search_medical_literature`; `interpret_labs` paracentesis; M01 `analyze_csf` | deleted |

Case-specific steps (row 8):
- `order_body_imaging`: required in M06 and S05, recommended in P08.
- `neuropsych_battery`: required in P07, optional in P01.
- `genetic_panel:wilson`: recommended in P04.

### 3.2 Outputs

**`initial_tool_outputs`.**
- `labs`.
- `microbiology`, holding blood cultures only.
- `ct`.
- `mri`, in the MRI cases.
- `eeg`, in the EEG cases and P08.
- `body_imaging`, in M06, P08 and S05.
- `literature_search` and `drug_interactions`: null.

**`followup_outputs`, in this order.**
1. `request_diagnostic_paracentesis`.
2. `request_urine_specimen`.
3. The remaining diagnostic follow-ups: P04 Wilson genetics, P01 neuropsychology, P07 neuropsychology.
4. The drug-interaction output, last (two outputs in P02).

Everything else is deleted. `avoided_actions` is unchanged; check that none matches a kept
criterion.

### 3.3 Sequence constraints, stop rule, exemptions

- **Sequence constraints:** none. Delete M01's CT-before-CSF together with the CSF criterion; no
  reverse order is unsafe once no LP remains.
- **Stop rule:** `required_before_assessment` lists exactly the required ids after the rebuild.
  `max_additional_actions` stays 0.
- **Panel exemptions:** none. The panel requires `LABS` and `microbiology`, and every case keeps
  both.

---

## 4. Per-case index

Every case also gets all of sections 2 and 3, notably C3, C4, C12, C13 and C17.

Field key:
- **Scores** = computed MELD / MELD-Na and Child-Pugh class.
- **Cx** = cultures tier.
- **Tap** = paracentesis.
- **DI** = drug-interaction tier.
- **Labs+** = extras to the core lab arguments.
- **Delete** = follow-ups to delete.

### M01 (male 52; NAFLD cirrhosis; hypokalaemia, constipation, diuretic non-adherence; ascites)
**Notes.**
- dec0d57a-9b9d-4d31-9774-25307651d25a: C1, C12. Delete the lorazepam EEG challenge and its red
  herring; PROHIB-BZD.
- 22fa5945-b95c-4f89-998c-ed320ca71725: C8. Delete the MRI F6, the CSF criterion with its F8, and
  the CT-CSF constraint.
- 6a7d6fa7-7e8b-441a-b0f7-03310da85a3b: C6. Delete the labs paracentesis criterion; expected
  evidence PMN 82.

**Decisions.**
- Scores: MELD 20 / MELD-Na 26 (stated 14); Child-Pugh C.
- Cx recommended. Tap required. DI optional.
- Delete F1, F3, F4, F5, F6, F8.
- C13 urine toxicology.
- C14 hyponatraemia.

### M02 (male 61; alcohol cirrhosis, treated HCC; SBP PMN 310, rifaximin non-adherence, alcohol; sulfa rash)
**Notes.**
- 9037c7e6-c8e1-4af8-bc02-8036ff8952b1: C12 (PROHIB-BZD-WD), C5. Delete the lorazepam dosing in
  F4.
- c0f7b456-9ee5-41bf-b16c-d9a170d2dfaf: C6. Delete a5; expected evidence PMN 310; MUST-SBP.
- 0a2f64af-85e4-4452-aa5b-059960addfe5: C10, C8. CT findings.

**Decisions.**
- Scores: MELD 25 / MELD-Na 28; Child-Pugh C. Delete "A". "MELD 18 three weeks ago" stays.
- Cx required. Tap required.
- DI required: the sulfa allergy excludes co-trimoxazole prophylaxis; use a fluoroquinolone.
- Labs+ `toxicology`.
- Delete F2, F3, F5.
- C13 ethanol 14.

### M03 (female 57; HCV cirrhosis post-SVR; constipation, recent TMP-SMX; codeine intolerance; ascites)
**Notes.**
- b8fd889d-9eaa-47eb-8317-780425e3f589: C9. Keep TSH 8.4 with fT4 0.7; delete the 2.1.

**Decisions.**
- Scores: MELD 13 / MELD-Na 16 (stated 12); Child-Pugh B or C (labs 5 + ascites + 2), to compute.
- Cx recommended.
- Tap: new required criterion; F3 moves to microbiology.
- DI optional.
- Delete F1, F2, F4 (methadone carry-over), F5.
- Hypothyroidism treatment becomes a must.

### M04 (male 48; severe alcohol-related hepatitis on prednisolone, day 5; withdrawal CIWA 12; hypoglycaemia; T 38.4)
**Notes.**
- e18c72da-7bca-4bce-b650-93777dd208c9: C1, C16. Delete F5 (day-7 Lille); add the Lille must.
- cbd4a868-9a0a-4d05-bf35-562b65ffdd93: C2.
- 0fffd88b-115e-4978-a76e-04c353874861: C8. MRI and CT findings; delete the LP line.

**Decisions.**
- Add a creatinine (for example 0.9 mg/dL) and compute. Child-Pugh C. The label has no score: add
  none.
- Cx required. Tap: none unless the exam documents ascites.
- DI recommended (prednisolone; benzodiazepine choice in liver failure).
- Labs+ `thiamine_B1` (pre-treatment).
- Delete F1, F3, F4, F5.
- PROHIB-BZD-WD replaces lines 0 and 4. MUST-THIA.
- Duplicate glucose (C9). C13 CT leak.

### M05 (female 63; PBC cirrhosis; constipation; zinc supplements; no ascites)
**Notes.**
- da6eb54c-0ea1-4a46-af1a-b3ff58b35d1a: C9. Zinc 180 only.
- a11d6f3d-05b1-4f83-a87e-948173a73d25: C9. TSH 3.8 only.
- cf6cd213-14ff-477a-b87c-f896f7ceb04f: C4 and the label. Delete F3; the zinc-excess premise is
  wrong (1.2).
- 3cb39ca8-0502-4ffa-842b-44c54474b00b: C2.
- 9a959a80-2aff-49f2-9f3b-1d3b8953b5a4: C7. Recommended.

**Decisions.**
- Scores: MELD 16 / MELD-Na 17 (stated 15); Child-Pugh B (9).
- Cx recommended. Tap none (delete F2). DI optional.
- Labs+ `zinc`, `copper`.
- Delete F1, F2, F3, F4, F5. Pruritus management becomes a must.
- **Relabel** (ruling 3, CENTRAL 6, Q1): "Hepatic encephalopathy (West Haven grade II), primary
  biliary cholangitis cirrhosis (Child-Pugh B, MELD-Na 17), precipitated by constipation; excess
  zinc from over-the-counter supplements with secondary copper deficiency".
- Prohibition: "Stop the zinc supplements: excess zinc causes copper deficiency; do not start zinc
  without a documented deficiency".
- Delete the arginase claim everywhere. C13 ammonia and zinc leaks.

### M06 (male 55; post-TIPS alcohol cirrhosis; lactulose overuse 8-10 stools, K 2.6, pre-renal AKI; no ascites)
**Notes.**
- 3e28b7bf-e9cb-457a-b79d-7249dd50c413: C2.
- 167526a9-3633-4aee-b365-7b5ecf77bbcb: C15. TIPS Doppler required; velocity.
- f90a4875-04bb-4ca6-a73d-99babd903035: C7. Recommended.

**Decisions.**
- Scores: MELD 21 / MELD-Na 21 (stated 13); Child-Pugh C (label B).
- Cx recommended. Tap none.
- DI required (escitalopram QT risk with K 2.6).
- Move F1 to initial `body_imaging`. Delete F2, F3, F5.
- MUST-LACT-OVERUSE, MUST-K. Must: "if HE recurs despite lactulose and rifaximin, discuss TIPS
  reduction".

### M07 (female 44; NASH cirrhosis; insulin-induced hypoglycaemia; sulfa allergy; ascites)
**Notes.**
- 0ea62416-aa98-4374-a103-a97113084e95: C2, C3.
- 5a318475-2762-4603-aa62-372420761674: C7. Recommended.

**Decisions.**
- Scores: MELD 12 / MELD-Na 12 (stated 11); Child-Pugh B.
- Cx recommended. Tap: new required criterion; F3 moves to microbiology.
- DI required: F2 becomes a real check of insulin in cirrhosis.
- Delete F1, F4, F5.
- Duplicate glucose (C9). EMS glucose is legitimate history.

### M08 (male 58; alcohol cirrhosis, HCC on sorafenib; diarrhoea, K 2.8, low Mg, AKI; T 38.2; ascites)
**Notes.**
- 18b8f3eb-0dfc-403c-9717-174f0b8a9811: C12. Sorafenib and loperamide.
- 391bf9ac-87c1-4e37-abba-1f8d554ea43d: C15, C14. Source search; red herring.
- fa503581-0eb8-46bd-95a2-e0af7de59a9c: C2.
- 8479a4e1-ad25-4ecf-b4ec-6b3094a233e4: C3.

**Decisions.**
- Scores: MELD 23 / MELD-Na 25 (stated 16); Child-Pugh C (label B).
- Cx required. Tap required (keep a9, delete a5; PMN 188).
- DI recommended: F2 becomes real sorafenib content.
- Labs+ `urinalysis`.
- Delete F3, F4 (PRES MRI), F5 (AFP). A prior AFP may stay as dated history.
- MUST-K. Oncology review of the HCC.

### M09 (male 59; alcohol cirrhosis; SBP PMN 412; first episode)
**Notes.**
- d279f19b-bf5a-4594-83c8-fed93048a7d3: C3 (also the F3 warnings).
- b56d3db7-33fd-4c74-ac9c-a197b9c1198a: C7. Delete the urine culture from the admission panel.

**Decisions.**
- Scores: MELD 21 / MELD-Na 25 (stated 15); Child-Pugh C (label B).
- Cx required. Tap required (keep a8, delete a3). DI recommended.
- Delete F2.
- MUST-SBP with albumin (bilirubin 4.2).
- C14: the "without infection" entry becomes low.

### M10 (male 54; haemochromatosis cirrhosis; variceal bleed; first episode; lactate 3.6)
**Notes.**
- fea3c98c-d147-438b-99d9-9af32922ae04: C2. Delete F1.
- f4f73be0-a9ec-4bf5-ba94-dd96506e7aee: C3.
- fed6c71c-77b3-4526-a49f-1a2d5cd320e8: C7. Recommended; the bleed gets prophylaxis, not culture
  gating.

**Decisions.**
- Scores: MELD 22 / MELD-Na 24 (stated 16); Child-Pugh C.
- Cx recommended. Tap required (keep a8, delete a5).
- DI recommended: F4 real content (hold the beta-blocker in shock).
- Labs+ `type_and_screen`; drop `iron_studies` from the arguments.
- Delete F1, F3.
- MUST-VB. C14: ICH and uraemia become low.

### P01 (male 47; cryptogenic cirrhosis; clonazepam accumulation plus quetiapine; no ascites)
**Notes.**
- 41da0ede-9688-4af3-a323-4ca09fa4e4da: C11. Relabel to overt grade II.
- 8da6b4b7-dd75-496a-ae30-3570972bf616: C3.
- e9c07b1d-c5f5-4306-9be8-3360366f5b28: C1, C16. Delete F1; MUST-THERAG.
- 1b529040-e50b-4e63-a57a-49e804d3c2eb: C2.
- 72abc830-ec3d-46ca-b242-5c62c567586a: C7 (recommended), C6 (delete F5; no ascites).

**Decisions.**
- Scores: MELD 12 / MELD-Na 13; Child-Pugh B (7).
- Cx recommended. Tap none.
- DI required: F2 becomes `check_clonazepam_quetiapine`.
- PHES (F4, a5) becomes optional: psychometrics are for covert HE.
- Delete F1, F3 (if post-treatment), F5.
- C13 ammonia, CT and EEG leaks.

### P02 (female 52; alcohol cirrhosis; valproate, lithium with HCTZ, recent alcohol; haloperidol allergy; no ascites)
**Notes.**
- 5fa6804b-d170-4b9f-b3c9-8a27e73d39cc: C9. Ethanol 22 only.
- 38ed2d53-d3ee-4a16-adeb-ba440e700b49: C13. Delete "pending".
- 6cff687b-c064-4379-8af0-576e94210eee: C12. PROHIB-BZD.
- fbc4826d-6e7d-4c44-ad89-0d9c2cd79cf6: C2.
- 9d18794f-92c2-489f-bea4-78a827983896: C3.
- e4e6c46c-7ba6-4723-9ec4-3af4e7045af2: C7. Recommended.

**Decisions.**
- Scores: MELD 16 / MELD-Na 18 (stated 12); Child-Pugh B (8).
- Cx recommended. Tap none (delete F4).
- DI required: keep F1 (valproate) and F2 (lithium with HCTZ); the criterion takes either drug as an
  alternative.
- Labs+ `lithium_level`, `valproate_level`, `toxicology`.
- Delete F3, F4, F5.
- Musts: stop valproate, hold lithium and HCTZ, psychiatry review of the mood stabilisers.

### P03 (male 61; NASH cirrhosis; prostate cancer on enzalutamide; penicillin anaphylaxis; ascites)
**Notes.**
- 4e8a2b60-4d78-4a9d-b8c3-8a603cdeb5d8: C11.
- dac2b026-1842-4c69-9c92-623fbab39a1d: C3.

**Decisions.**
- Scores: MELD 13 / MELD-Na 13 (stated 11); Child-Pugh B or C, to compute. The case says A and B.
- Cx recommended. Tap: new required criterion; F4 moves to microbiology.
- DI recommended: F3 enzalutamide (CYP3A4 induction, seizure threshold).
- Move F1 into the initial `mri`. Delete F2, F5.
- Delete both LP prohibitions: the MRI excludes leptomeningeal disease.
- Goals-of-care must. No beta-lactam without allergy advice.
- C13 leaks.

### P04 (male 55; previously unrecognised Wilson disease with acute HE; ascites)
**Notes.**
- b15cdee4-1d9b-4a39-b382-9e1b4cdc719c: C12. PROHIB-BZD.
- 8ee3aef0-12c4-499c-b8a0-81305ca89342: C2, C1. Delete F3, which reports drugs never given.
- 73e5a38f-2f8b-4cce-91d1-755eb23b78b3: C7. Recommended.

**Decisions.**
- Scores: MELD 17 / MELD-Na 18; Child-Pugh C.
- Cx recommended. Tap: new required criterion. DI optional.
- Labs+ `ceruloplasmin`, `copper`.
- Move F1 into the initial `mri`, replacing the normal one. Keep F4 genetics (recommended).
- Delete F2, F3, F5.
- Musts: chelation (trientine or penicillamine) with specialist input; slit-lamp for
  Kayser-Fleischer rings; transplant assessment if decompensated (AASLD Wilson 2022).

### P05 (female 49; NASH cirrhosis with coeliac disease; Wernicke plus HE; no ascites)
**Notes.**
- 067d3743-f6a8-4de7-a323-459deef6c259: C9. B12 188 and magnesium, once each.
- caa0c178-d8a0-4638-955b-3f6a1c850639: C8. One Wernicke MRI in the initial `mri`.
- d07af885-7c9f-41a1-91ea-2df4f312a207: C6. Delete F5.
- 7689f42d-f242-4759-96ed-c9ffb100bc9c: C7. Recommended.
- 0f54d6e7-e379-44f5-9bd2-c0e723b7919e: C2. Delete F3.

**Decisions.**
- Add a creatinine consistent with 7 days of vomiting, then compute; Child-Pugh B (9).
- Cx recommended. Tap none. DI recommended (levothyroxine and calcium, if listed).
- Labs+ `thiamine_B1` (24 nmol/L, pre-treatment), `B12`.
- Delete F1, F2 (after the move), F3, F4, F5.
- MUST-THIA at the Wernicke dose, before glucose.

### P06 (male 44; alcohol cirrhosis; NCSE after a GTC, subtherapeutic levetiracetam; no ascites)
**Notes.**
- d4cc8148-f11f-4f95-bb2b-6297b231a507: C9. CK by timing (FIXED or partly DECLINED, Brigo 2015);
  ethanol once.
- 65351710-ec4b-4f3c-9299-2d3e9d9e4088: C6. Delete F4.
- 780fd2f8-e3bc-4b20-8d89-f21d2182c8d1: C7. Recommended.
- 68f03868-5416-43a3-8e3b-194ebe74ac2c: C2. Delete F3.

**Decisions.**
- Scores: MELD 21 / MELD-Na 23 (stated 12); Child-Pugh C (label B).
- Cx recommended (WBC 11.2 post-ictal). Tap none.
- DI required: F1 becomes a real antiseizure check (levetiracetam dosing; avoid valproate and
  enzyme inducers).
- EEG required, with the pre-treatment NCSE in the initial `eeg`. CT required.
- Delete F2, F3, F4, F5.
- PROHIB-BZD-SZ. Label unchanged (Q5).

### P07 (male 58; NASH cirrhosis, Child-Pugh A; covert HE, PHES -5; CPAP non-adherence; long-term PPI)
**Notes.**
- 8a4256a7-b206-42d6-abc1-e35dca3ed4f9: C2. Range 11-51; 48 is within range and unflagged;
  describe it once.
- d848bfa7-c3c4-47f4-8a89-5737561c8d21: C8. EEG.
- 23004ad1-6ca4-4915-859d-e6026a30fe85: C9. TSH once.
- 41f02bb6-fdeb-45c7-b2ec-b0ce03dae593: C2.

**Decisions.**
- Scores: MELD 7 / MELD-Na 7 (stated 8); Child-Pugh A (5).
- Cx recommended. Tap none. DI optional (F3 PPI as real deprescribing content).
- PHES stays required.
- Delete F2, F4, F5.
- Musts: CPAP adherence, PPI deprescribing, driving advice.
- C13 leaks.

### P08 (male 70; spontaneous splenorenal shunt, compensated cirrhosis; recurrent grade II episodes called TIA; sulfa allergy)
**Notes.**
- 8465dace-a469-4e91-9c69-c28052b0c7f5: C7. Delete the urine culture criterion and F5; blood
  cultures optional.
- ee768920-f1c3-4cd9-9e9f-1577dcd8a6fb: C11. Type C.

**Decisions.**
- Scores: MELD 8 / MELD-Na 8 (stated 7); Child-Pugh A (6).
- Tap none. DI optional (F3 with real content).
- CT and MRI required. Move F1 to the initial `mri` and F4 to the initial `eeg`.
- New shunt-imaging criterion (C15).
- Delete F2, F5.
- Must: discuss shunt embolisation with interventional radiology if HE recurs despite lactulose
  and rifaximin.
- C14: TIA and NCSE become low.

### P09 (female 62; alcohol cirrhosis; UTI; chronic left SDH; APPROVED)
**Notes.**
- 43f8f665-25a8-4a96-a335-24383a4eb220: C16. DECLINED by design; check that the musts match 1.2.
- 7ed60ff7-bd34-4957-bd71-f498f6391d85: C3. Change 3-4 to 2-3.

**Real-error changes only.**
- Delete F1 (treatment response).
- Delete the required literature criterion and F2.
- C10: Child-Pugh C, MELD-Na 18 (stated B and 14).
- Add the required paracentesis (ascites present).
- C14: SDH becomes a concurrent contributor.
- C2: ammonia range.

**Keep.** CT required; the SDH LP prohibition; F3 DI (required); Cx required; labs+ `urinalysis`.

### S01 (male 58; alcohol cirrhosis; variceal bleed and SBP PMN 342; APPROVED)
**Notes.**
- af008448-4abd-4572-972a-7183d2d0b079: C12. Airway must.
- d4a0da8d-3c01-43ff-948d-d43b2892d10f: C10.

**Real-error changes only.**
- Scores: MELD 36 / MELD-Na 38 (stated 22 and 28); Child-Pugh C stays.
- Delete F1, F3, F5.
- Delete the literature criterion; set the echoing initial output to null.
- Delete a5 (C6).
- The ascitic block gets one time point (C7).
- Move the empty initial DI to a real follow-up (DI recommended).

**Keep.** F4 cardiac monitoring, if its content is clean. Cx required; tap required (a9).

### S02 (male 64; alcohol cirrhosis; 10-day rifaximin gap, diarrhoea with K 3.2; T 38.2, WBC 13.6)
**Notes.**
- b8268eb9-d737-4a3f-9e74-d9a55e1e9584: C14. Red herring.
- 3559f393-0f92-41bc-8de4-6b194897fcf3: C16 (DECLINED by design), C1. Delete F5; a rifaximin
  restart with a supply plan becomes a must.
- a6ec2282-8ada-4f5c-ae0b-d64877fed336: C3. MUST-LACT-OVERUSE.
- 632aabc9-6d1c-409d-9713-25e61382f9af: C10.
- dd9192d8-7d9c-4451-b055-51a1d734dc19: C15. Musts for stool C. difficile testing and a chest
  radiograph.

**Decisions.**
- Scores: MELD 27 / MELD-Na 30 (stated 18 and 21); Child-Pugh C (label B).
- Cx required. Tap required (a9, delete a5; PMN 124). DI optional.
- Delete F2, F3, F4, F5.
- MUST-K; magnesium in the labs.

### S03 (female 52; alcohol cirrhosis; E. coli urosepsis; BP 104, HR 116, Cr 1.6)
**Notes.**
- bb58b696-1042-44c8-a7ae-9d2b4769f69c: C7. Split the blocks; one consistent positive urine
  culture.
- 1720c3d7-2a65-42de-ad87-5234966b22e5: C16, C15. Partly DECLINED by design; MUST-SEPSIS; the
  referral criterion is ALREADY-FIXED (confirm).
- 998fed4f-012a-49fb-8333-d928f96b15a6: C9. Lactate raised.
- 85b833e1-e475-4ef3-ba3d-85c02aa0b0f1: C10.

**Decisions.**
- Scores: MELD 32 / MELD-Na 35 (stated 20 and 24); Child-Pugh C.
- Cx required. Tap required (a9, delete a5). DI recommended (F3 antibiotic choice with AKI).
- Labs+ `urinalysis`.
- Delete F2, F4, F5.

### S04 (male 61; alcohol cirrhosis; variceal bleed; metformin; penicillin rash; WBC 12.4, lactate 4.8)
**Notes.**
- 0ddd13be-4d2f-4d09-beb7-bbd030a2a046: C10. Both "MELD-Na 26" and "CP 13" are wrong.
- a8504264-7337-4a7b-8ef3-beebe99a9b13: C12, C5. Allergy wording.

**Decisions.**
- Scores: MELD 36 / MELD-Na 37; Child-Pugh C.
- Cx required. Tap required (a9, delete a5).
- DI required (ceftriaxone with penicillin rash; stop metformin, lactate 4.8).
- Delete F2 (endoscopy), F3, F4, F5.
- MUST-VB.
- C8: delete the CT pallidal hypodensity.

### S05 (female 55; HBV cirrhosis; E. coli urosepsis; sulfonamide rash; T 38.6, WBC 18.2; right loin pain, Cr 1.8)
**Notes.**
- 55bba229-0455-4596-8c10-39f12c82e590: C10.
- 2fd43a55-218b-4224-b97a-4eaf95e96d28: C7. No organism in a blood block that excludes
  bacteraemia; E. coli in the urine, consistently.

**Notes filed on S06 that describe this case** (apply them here and cite them in this log as "filed
on S06"):
- 170d2c1e-6ee3-4a44-8b42-bb8380dad0b2: C7.
- 988c74d2-fcf4-4799-83bf-d3b8d83e8a81: C10.
- 36bd67da-e34c-41de-ac47-f01d82bd6d7e: C15. Renal ultrasound.

**Decisions.**
- Scores: MELD 30 / MELD-Na 32 (stated 18, and "10, B/C borderline"); Child-Pugh C.
- Cx required. Tap required (a9, delete a5).
- DI required (antiviral renal dosing with Cr 1.8; sulfonamide allergy).
- Labs+ `urinalysis`. New renal ultrasound, required.
- Delete F2 (its susceptibility goes into the urine block), F3, F4 (HBV DNA and adherence become a
  must), F5.
- MUST-SEPSIS.

### S06 (male 48; alcohol binge, non-adherence; grade IV coma, GCS 8)
**Notes.** All three describe S05, not S06. S06 has bilirubin 18.4, INR 3.4, Cr 1.4, no loin pain
and no UTI.
- 170d2c1e-6ee3-4a44-8b42-bb8380dad0b2: DECLINED for S06; applied to S05 (C7). Still check S06's
  own blocks.
- 988c74d2-fcf4-4799-83bf-d3b8d83e8a81: applied to S05 (C10). S06's own scores are also wrong:
  FIXED under C10.
- 36bd67da-e34c-41de-ac47-f01d82bd6d7e: DECLINED for S06; applied to S05 (C15).

**Decisions.**
- Scores: MELD 34 / MELD-Na 36 (stated 24); Child-Pugh C.
- Cx recommended. Tap required (a9, delete a5). DI optional (real follow-up).
- Labs+ `thiamine_B1` (initial value), `toxicology`.
- Delete F1, F3, F4 (withdrawal monitoring becomes a must), F5.
- PROHIB-BZD-WD. MUST-THIA. Must: intubate for airway protection (GCS 8).

### S07 (male 64; HCV cirrhosis; constipation and codeine; small ascites)
**Notes.**
- a4e6f322-2a12-44d9-aa4a-2a53f8996ca6: C1. Delete the naloxone F2.
- 409e1c57-932e-42bc-ac3a-53fa32a14a01: C7. Recommended.

**Decisions.**
- Scores: MELD 21 / MELD-Na 23 (stated 22); Child-Pugh C.
- Cx recommended. Tap: new required criterion; F1 moves to microbiology.
- DI required (codeine metabolites accumulate in cirrhosis).
- Delete F2, F3, F4, F5.
- Musts:
  - stop codeine;
  - low-dose naloxone only for clear opioid toxicity;
  - HCV treatment referral (no protease inhibitor in Child-Pugh B or C).
- C8: delete the CT pallidal hypodensity. C13 leaks.

### S08 (male 58; alcohol cirrhosis; GI bleed, hypokalaemia, alcohol, lactulose non-adherence; penicillin rash; WBC 14.2)
**Notes.**
- cb1f2bae-6883-45e7-9a83-6c6ebae05ed1: C9. Ethanol 142 only.
- 5dd96024-cbb1-4bb9-9fba-4a3ab26d515c: C10.

**Decisions.**
- Scores: MELD 29 / MELD-Na 32 (stated 18); Child-Pugh C (label B).
- Cx required. Tap required (a9, delete a5).
- DI required (ceftriaxone with penicillin rash).
- Labs+ `toxicology`.
- Delete F1, F3 (lorazepam challenge), F4, F5, F6 (MRI).
- Musts: MUST-VB if variceal, MUST-K, MUST-THIA. PROHIB-BZD-WD if withdrawal is described.
- Ammonia range 11-51.

### S09 (male 63; HCV cirrhosis, small HCC on the transplant list; SBP; sulfa anaphylaxis; APPROVED)
**Notes.**
- 498272a4-5a8b-486f-ad2e-c33988cac9f4: C10. Child-Pugh C, MELD-Na 28 (stated B and 16).
- d2b65d04-2478-457c-af46-3ee3825f36db: C7. Make the impression agree with the Gram stain:
  "Gram-negative rods seen; culture pending" with the organism null, or the final organism.

**Real-error changes only.**
- Delete F2, F5, F6. The 48-hour repeat tap goes into MUST-SBP.
- Delete the literature criterion and output.
- Delete a5.
- Change 2-4 to 2-3.
- Ammonia range 11-35 becomes 11-51.
- Delete F4 only if it is post-treatment.

**Keep.** F3 DI (required: no co-trimoxazole). Cx required; tap required (a9).

### S10 (female 52; NASH cirrhosis; furosemide hypokalaemia, lactulose non-adherence; ascites; no notes)
**Decisions.**
- Scores: MELD 19 / MELD-Na 21 (stated 14); Child-Pugh C (label B).
- Cx recommended. Tap: new required criterion; F4 moves to microbiology.
- DI required: merge F2 (metformin) and F6 (diuretics) into one real check.
- Delete F1, F3 (if post-treatment), F5 (MRI), and the merged-away DI follow-up.
- MUST-K. Ammonia range 11-51. Change 2-4 to 2-3.
- The labs from a week earlier stay, dated.

### S11 (female 67; autoimmune hepatitis cirrhosis; constipation, lactulose non-adherence; penicillin rash; small ascites)
**Notes.**
- b177af3e-1030-40f2-aa3d-bc4183e890aa: C3, C4. Delete F1.
- 65f1c0dd-9492-466b-a72f-73360c71870c: C2. Delete F4.

**Decisions.**
- Scores: MELD 15 / MELD-Na 16 (stated 13); Child-Pugh B or C (labs 5 + 2 + HE), to compute.
- Cx recommended. Tap: new required criterion; F3 moves to microbiology.
- DI recommended (F2 with the case's immunosuppressants).
- CT required.
- Split the mixed initial micro block (C7). Write "µmol/L".

---

## 5. CENTRAL requests

1. **Citation allow-list.**
   - Add `[ACG_HE_2026]`, `[EASL_HE_2022]`, `[EASL_decomp_2018]`, `[AASLD_ascites_2021]`,
     `[Baveno_VII]`, `[EASL_ALD_2018]`, `[Lille_2007]`, `[EFNS_Wernicke_2010]`, `[AES_2016]`,
     `[Brigo_2015]`, `[AASLD_Wilson_2022]` and `[Kim_MELDNa_2008]`.
   - Retire `[EASL_2010]` and `[Bajaj_2011]`.
2. **Criteria pack `dataset-generation/criteria_packs/HEP-ENC.md`.** Update it to:
   - set the lactulose target at 2-3 stools a day;
   - define covert HE as minimal or grade 1;
   - state that ammonia does not grade or titrate;
   - limit imaging to the ACG triggers;
   - drop the literature requirement;
   - require the drug-interaction check only for a concrete interaction;
   - tier cultures as in C7;
   - require paracentesis whenever ascites is present;
   - delete the hard CT/MRI-before-CSF constraint (line 51).
3. **`conditions.yaml` HEP-ENC `common_followups`.**
   - Remove `request_lactulose_rifaximin`, the `interpret_labs` `request_sbp_paracentesis`,
     `request_thiamine_empiric`, `request_liver_transplant_evaluation` and the EEG benzodiazepine
     challenge.
   - These seeded C1 in all 30 cases.
4. **Lab criterion matching** (as ALS CENTRAL 4).
   - Make `_contains_required` use `normalize_analyte`, so that `CMP` matches `BMP` + `LFTs` and
     `coagulation` matches `INR`.
   - Until then HEP-ENC uses the two-alternative core of C9.
5. **Core vocabulary** (needed by M08 and S02, after the reviewer notes).
   - Add `chest_xray` to `order_body_imaging`.
   - Add a `stool` specimen (C. difficile toxin/PCR) to `order_microbiology`. It exists only in the
     general_medicine pack; per CLAUDE.md, a term NeuroBench needs goes in the core block, with its
     library report and the `tool_io.py` mirror.
   - Optional: AFP in `interpret_labs`.
6. **`accepted[0]` changes under ruling 3.**
   - Severity numbers change in all 30 (C10). M05 and P01 are relabelled (C11).
   - No ICD or synonym change: the HE label tokens are unchanged.
7. **Review app.**
   - The three S06 notes describe S05: check the R2 note-to-case binding before the next round.
   - Show initial and follow-up outputs together, in criterion order (as ALS CENTRAL 1).
8. **Tests.**
   - No stored literature or drug-interaction output contains a criterion's `expected_evidence`.
   - No HEP-ENC case contains "2-4 soft", "the finding the lumbar puncture is gated on", or a CT
     impression with "restricted diffusion".
9. **`condition_tool_guidance.yaml` (`hepatic_encephalopathy`, July 2026).**
   - It requires cultures in all 30; C7 tiers them after 11 R2 notes.
   - It counts "13 with ascites"; ascites is present in 21.
   - The review app shows this guidance to reviewers.

---

## 6. Open questions for Andrea

- **Q1. M05 premise.** The reviewer ruled that the zinc-toxicity mechanism is wrong. The plan
  relabels the precipitant as constipation, with zinc excess and copper deficiency as an incidental
  supplement finding. The alternatives are a zinc-deficiency rewrite, or dropping the zinc thread.
  Confirm.
- **Q2. Culture tier.** The July guidance made cultures required in all 30. Eleven notes rule them
  not mandatory without infection. The plan requires them only with T ≥ 38.0 °C, WBC > 11 or an
  infective precipitant. Confirm the threshold; P06 (post-ictal WBC 11.2) and S04/S08 (bleeding
  with leucocytosis) are the edge cases.
- **Q3. Scores in `accepted[0]`.** Correcting the scores changes all 30 labels and moves most cases
  from class B to C. The alternative is to drop the scores from `accepted[0]` and keep them in key
  evidence. Should MELD 3.0 (OPTN since 2023) replace MELD-Na? The reviewers used classic MELD-Na.
- **Q4. Core lab criterion.** The plan requires CBC, CMP (or BMP + LFTs), coagulation, ammonia and
  the case extras. TSH, zinc, toxicology, magnesium and lactate stay in the report but not in the
  criterion, against the July core list. CRP is added to every report but not required. Confirm.
- **Q5. P06 label.** The ground truth is NCSE with concurrent HE, under the HE condition. Keep it as
  a deliberate mimic case, or make HE primary with NCSE as a co-diagnosis?
- **Q6. Small ascites (S07, S11).** Paracentesis is required per EASL 2018 and AASLD 2021. Confirm
  that an ultrasound-guided tap of small ascites is intended.
- **Q7. Literature.** The plan deletes it in all 30, including the approved P09, S01 and S09, as in
  ALS Q3. Confirm, or keep an optional criterion with no required query.
