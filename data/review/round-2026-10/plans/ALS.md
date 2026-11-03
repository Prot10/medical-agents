# ALS: condition plan for the October 2026 review round

Lead plan for the 30 ALS cases (ALS-M01..M08, ALS-P01..P09, ALS-RM11, ALS-RS11, ALS-S01..S11).
Workers follow it case by case so that every case reaches the same decision. Read
`ROUND_POLICY.md` and `PATTERNS.md` first; this plan does not repeat them. All 245 Reviewer 1 notes
are listed in section 4 with the class (section 2) that resolves them. Reviewer 2 has not reviewed
ALS yet (pending on M01 and M08 only).

Baseline measured on 23 October 2026 before any edit: `perfect_agent.py` passes 30/30 (it copies
the criteria's own arguments, so it does not catch the matching defects in class C16).

Section 2 cites notes by the first 8 characters of their id; section 4 gives every full id under its
case.

How to use this plan:

1. Apply every class in section 2 to your case, in the order listed, using the canonical text
   verbatim where a canonical text is given (fill the `<...>` slots from the case).
2. Then apply the per-case decisions of section 4.
3. Rebuild `action_criteria`, `followup_outputs` and `sequence_constraints` exactly as section 3 says.
4. Run both checks, write the log, cite every note id of the case.

Conventions for all new text: English, the case's spelling, no em dashes or en dashes, "x ULN" for
multiples, units as the case already uses them. Do not invent numbers that the case does not need;
where a class asks you to add a normal result, choose a plausible value inside the reference range
that differs from the other cases and agrees with age, sex, renal function and medicines.

---

## 1. Governing guidelines and canonical facts

### 1.1 Which guideline governs what

| question | governing source | citation key |
| --- | --- | --- |
| Diagnosis | Gold Coast criteria 2020 (Shefner JM et al., Clin Neurophysiol 2020;131:1975-1978) | `[Gold_Coast_2020]` |
| Electrodiagnosis | Awaji recommendations 2008 (de Carvalho M et al., Clin Neurophysiol 2008;119:497-503) | `[Awaji_2008]` |
| Diagnostic work-up (which mimic tests, CSF only when atypical) | EFNS guideline on the clinical management of ALS (Andersen PM et al., Eur J Neurol 2012;19:360-375) | `[EFNS_ALS_2012]` (new key, CENTRAL) |
| Management (riluzole, MDT, NIV, gastrostomy, disclosure) | EAN guideline on the management of ALS 2024 (Van Damme P et al., Eur J Neurol 2024;31:e16264) | `[EAN_ALS_2024]` (new key, CENTRAL) |
| MDT organisation, review interval, respiratory and nutrition care | NICE NG42, Motor neurone disease: assessment and management (2016, updated 2019) | `[NICE_NG42]` (new key, CENTRAL) |
| NIV thresholds, gastrostomy timing | AAN practice parameter update 2009 (Miller RG et al., Neurology 2009;73:1218-1226) | `[AAN_2009]` |
| NIV survival benefit | Bourke SC et al., Lancet Neurol 2006;5:140-147 | `[Bourke_2006]` (new key, CENTRAL) |
| Genetic testing | Roggenbuck J et al., Evidence-based consensus guidelines for ALS genetic testing and counseling, Ann Clin Transl Neurol 2023;10:2074-2091 | `[ALS_genetics_2023]` (new key, CENTRAL) |
| Riluzole dosing, monitoring, interactions | Riluzole Summary of Product Characteristics (Rilutek SmPC) | `[Riluzole_SmPC]` (new key, CENTRAL) |
| Review article, background only | Brown RH, Al-Chalabi A, NEJM 2017;377:162-172 | `[Brown_2017]` |

Where Gold Coast and Awaji/El Escorial categories diverge, Gold Coast governs the diagnosis (it is
the current criterion and the one the reviewers apply). Awaji categories ("possible", "probable",
"definite") may be named only as a secondary description and only where the data meet them; never
call a first EMG with active denervation in one region "definite".

Citation format in `citations` lists: one bracketed key per source, from the table above, no bare
duplicates (`"Awaji_2008"` next to `"[Awaji_2008]"`), no free text (`"Gold Coast; EAN 2024; NICE
NG42"` is removed everywhere). `[EAN_ALS_2024]` replaces the existing non-allow-listed variants.

### 1.2 Canonical facts (use these, do not restate them differently)

- **Gold Coast 2020**: progressive motor impairment documented by history or repeated examination,
  preceded by normal motor function; plus upper and lower motor neuron dysfunction in at least one
  body region, or lower motor neuron dysfunction in at least two body regions; plus investigations
  excluding other disease processes. Body regions: bulbar, cervical, thoracic, lumbosacral.
- **EMG lower motor neuron evidence**: chronic neurogenic change (large, long-duration or unstable
  motor unit potentials, reduced recruitment) together with active denervation (fibrillation
  potentials or positive sharp waves). Awaji 2008: fasciculation potentials count as active
  denervation in a muscle that shows chronic neurogenic change. Complex fasciculations alone, or
  fasciculations without chronic change, raise concern but are not diagnostic.
- **Mimics the EMG/NCS excludes**: multifocal motor neuropathy (conduction block, slowed motor
  conduction), demyelinating or sensorimotor neuropathy (abnormal sensory or motor conduction),
  myopathy (myopathic units). Normal sensory responses also argue against SBMA (Kennedy disease),
  which has a sensory neuronopathy and no upper motor neuron signs.
- **MRI**: brain and spine MRI exclude structural, vascular, demyelinating, inflammatory and
  neoplastic mimics. Corticospinal tract T2/FLAIR hyperintensity or a motor-cortex low T2 rim is
  supportive at most and never confirmatory. Cervical spondylosis is common at this age and does not
  explain bulbar signs or denervation in thoracic, lumbosacral or bulbar muscles.
- **CK**: mild to moderate elevation is common in ALS (denervation). A CK above 5x ULN is higher than
  usual: say so, name a myopathic contributor to consider (statin myopathy when the patient takes a
  statin), and state that the neurogenic EMG pattern argues against a primary myopathy.
- **CSF**: not part of the routine work-up; only for a specific inflammatory, infectious or
  neoplastic mimic (EFNS 2012, July 2026 tool review: M04, M08, P03, P05, P06 only). CSF does not
  diagnose ALS.
- **Respiratory function** (staging, not diagnosis): FVC lower limit 80% predicted; SNIP lower limit
  70 cmH2O in men and 60 cmH2O in women; MIP and NIF are reported as negative pressures and the
  dataset uses -60 cmH2O as the lower limit (a value closer to zero, such as -52, is weaker; see
  open question Q4). AAN 2009 markers of respiratory insufficiency that prompt NIV discussion:
  orthopnoea, FVC below 50% predicted, SNIP below 40 cmH2O, MIP weaker than -60 cmH2O, abnormal
  nocturnal oximetry. Monitor FVC and SNIP about every 3 months (NICE NG42). NIV prolongs survival
  and improves quality of life (Bourke 2006), most clearly without severe bulbar dysfunction.
- **Gastrostomy**: discuss early in bulbar disease and with weight loss; place it while FVC is above
  50% predicted (AAN 2009).
- **Riluzole** (SmPC): 50 mg every 12 hours. Measure serum transaminases before starting, monthly for
  the first 3 months, every 3 months for the rest of the first year, periodically thereafter; stop if
  ALT rises above 5x ULN. Warn the patient to report any febrile illness (neutropenia: check the white
  cell count). Metabolised by CYP1A2: inhibitors (fluvoxamine, ciprofloxacin, enoxacin and other
  quinolones) can raise exposure; inducers (cigarette smoke, rifampicin, omeprazole, charcoal-grilled
  food) can lower it. Caution with other hepatotoxic drugs and heavy alcohol use. An oral suspension
  exists for patients who cannot swallow tablets safely. Wrong claims to remove everywhere: grapefruit
  as a CYP1A2 modulator, alcohol "via CYP1A2 inhibition", caffeine "induces CYP1A2", levothyroxine or
  metformin "CYP1A2/hepatic interaction", riluzole as a serotonergic drug, riluzole as a QTc-prolonging
  drug, warfarin "CYP1A2 competition" as an established interaction, natalizumab "lymphopenia"
  (natalizumab causes lymphocytosis), invented methotrexate monitoring intervals.
- **Edaravone and AMX0035**: AMX0035 (Relyvrio) was withdrawn from the market in April 2024 after
  the PHOENIX trial; it is never mentioned. Edaravone is not recommended by EAN 2024 and is not offered
  as an "alternative" inside an interaction check. Treatment alternatives never appear in a drug
  interaction output.
- **Tofersen**: FDA accelerated approval April 2023, EU authorisation 2024 under exceptional
  circumstances, only for ALS with a SOD1 pathogenic variant; it is a specialist-centre decision
  and is not proposed before ALS is established (P08).
- **Genetic testing**: offered with pre-test counselling to people with ALS (2023 consensus); it
  follows the clinical and electrodiagnostic assessment and never establishes the diagnosis by
  itself. The ALS panel reported in this dataset is: C9orf72 repeat expansion (repeat-primed PCR) plus
  sequencing of SOD1, TARDBP, FUS and TBK1. First-degree relatives of a carrier have a 50% chance
  of carrying the variant; predictive testing follows counselling, and testing of minors is normally
  deferred until they can decide for themselves.
- **Spinal anatomy**: in adults the cord ends at about L1-L2; findings at L3-S1 are cauda equina or
  roots, never "cord".

---

## 2. Error classes in this condition

Each class: what is wrong, where (notes and cases), the decided fix, canonical text. Apply every
class to every case unless the class says otherwise.

### C1. Pathway order is not diagnostic order (PATTERNS 1, ALS 79/29)

- **Wrong**: the follow-ups ("Diagnostic pathway, Step N") start with the riluzole interaction check,
  a literature search, respiratory function and genetics, while EMG/NCS, brain MRI, spine MRI and
  labs sit only in the initial work-up; `action_criteria` lists literature and riluzole as actions 1
  and 2.
- **Notes**: every "pathway skips the core work-up", "riluzole check should not be Step 1", "respiratory
  is staging, place it after the core", "genetics after diagnosis" note and every case comment about
  the pathway; listed per case in section 4. All 30 cases.
- **Fix**: rebuild `action_criteria` order, `followup_outputs` order and `sequence_constraints` exactly
  as section 3. The diagnostic core stays in `initial_tool_outputs` (EMG under `specialized_test`,
  brain MRI under `mri`, spine MRI under `body_imaging`, labs under `labs`, CSF under `csf`): it is
  matched robustly there, and the UI fix that shows the initial work-up in criterion order is a
  CENTRAL request. The follow-ups then hold only post-diagnostic steps in clinical order:
  respiratory function, genetic panel, riluzole interaction check. Log each pathway note FIXED
  with "action criteria reordered (EMG, brain MRI, spine MRI, labs first); follow-ups now respiratory,
  genetics, riluzole; literature removed; sequence constraints EMG before genetics and riluzole".

### C2. Literature search used as a clinical step and as a scoring echo (PATTERNS 1, ruling 5)

- **Wrong**: `action-1-search-medical-literature` (recommended, exact query string that no agent will
  reproduce) in all 30; its `expected_evidence` is echoed verbatim in the stored initial
  `literature_search` output in 16 cases (M01-M04, RM11, RS11, S01-S09, S11). Case-specific literature
  follow-ups stand in for clinical actions: M05 "neurosurgery_consultation_deferred", M06
  "search_als_ra_comorbidity", M07 "search_lead_toxicity_als", M08 "search_als_ms_concurrent", P01
  "search_benign_fasciculation_als_distinction", P02 "genetic_counseling_c9orf72", P03
  "search_mmn_als_misdiagnosis", P04 "search_flail_arm_als", P05 "search_als_hiv_comorbidity", P06
  "search_mgus_als_association", P07 "search_als_post_polio_differential", P08 "search_sod1_a4v_prognosis"
  and "genetic_counseling_sod1", P09 "search_als_ftd_c9orf72", S10 "genetic_counseling_referral_c9orf72".
  Because the MockServer serves the first stored literature entry to any query, every agent search
  received the leaking text. P04's flail-arm entry also cites El Escorial.
- **Notes**: cb8459b2 (M05), c5bda677 (M06), 27fe005e and 30c38fd0 (M07), ebf2dc98 (M08), 92755ec0,
  d92369d6 and 8ad11950 (P01), 5ae3cc00 and 5132b5f5 (P03), 959fb8c4 and 039f6452 (P04), 0ca4443e
  (P05), 5c89246b and 59b49bd2 (P06), 1138cdf4 and bb7e1af1 (P07), 38d2fb67 (P08), f29aca3a and
  9e59c630 (P09), 3d89340e (S10); the pathway case comments.
- **Fix (all 30)**: delete criterion `action-1-search-medical-literature`; set
  `initial_tool_outputs.literature_search` to null; delete every `search_medical_literature`
  follow-up. Do not add a replacement literature criterion. An agent that still searches gets the
  library's general literature output (no penalty beyond the stop rule). The clinical content of the
  deleted consult-like follow-ups becomes musts or prohibitions: M05 lumbar-surgery prohibition (C14),
  P02/P08/S10 genetic counselling musts (C10), P01 repeat EMG must (C7). P01 note 8ad11950 ("soften
  complex fasciculations are pathological regardless") is resolved by deletion of that output, and
  the same softened statement goes into P01's key evidence (section 4).

### C3. Drug-interaction check misplaced and wrong (PATTERNS 1, 2; rulings 4, 6)

- **Wrong**: the riluzole check is Step 1 or 2; every output lists AMX0035 as an alternative (30/30),
  several list edaravone; S08 names Relyvrio; P08 checks tofersen; M07 offers AMX0035 "if alcohol
  cessation is not achievable"; M08 "AMX0035 reasonable given polypharmacy"; S10 adds C9orf72 trial
  enrolment; wrong mechanisms listed in 1.2 appear in M01, M02, M07, M08, P02, P09, S02, S06, S07,
  S08, S09, S10; S03, S05 and S10 carry an initial `drug_interactions` block named "general" that
  shadows the follow-up and repeats the expected text (grapefruit, CYP1A2); every case's criterion
  `expected_evidence` says "alcohol and grapefruit-juice avoidance (CYP1A2 modulators)".
- **Notes**: all "Remove AMX0035" notes and all "riluzole ... should not be Step 1" notes; mechanism
  notes 4fdb755c and 8b821a0b (levothyroxine), 5c9f1969 (metformin), 7949f4b4 (escitalopram),
  8c1a9e6d (warfarin), f1998fc1 and ce3bced0 (S10 caffeine and trial), dc07427d (M07), 53da6db5 (M08),
  1a295b03 and c26321cf (S03, S05 empty/duplicate block), 9200b13f and a332a5e7 (P02), 5db6492b and
  af695bda (P08).
- **Fix**:
  - `initial_tool_outputs.drug_interactions` = null in all 30 (S03, S05, S10 lose their "general"
    block); the riluzole follow-up is the only stored interaction output and it is last in the list.
  - Criterion `action-2-check-drug-interactions` (alternatives unchanged: `check_drug_interactions`
    `{"drug": "riluzole"}`): importance `recommended` in every case where riluzole is a must;
    `required` only in M06 (methotrexate, see section 4); `optional` in P01; deleted together with
    its follow-up in P02 and P08 (riluzole and tofersen are not indicated there).
  - Rewrite every riluzole output with the structure below. Remove AMX0035, Relyvrio, edaravone,
    tofersen, trial enrolment and every wrong mechanism of 1.2. Keep only true, case-specific points.
  - Canonical output structure (fields as the existing output uses them):
    - `interactions`: one entry per patient medicine (and alcohol or smoking when relevant), each
      stating "no clinically significant interaction expected" or the real point (table below).
    - `summary`: "No interaction requires a change to riluzole 50 mg twice daily. Measure liver
      transaminases before the first dose, monthly for the first 3 months, every 3 months for the rest
      of the first year and periodically thereafter; stop riluzole if ALT exceeds 5x ULN. Report any
      febrile illness (check the white cell count for neutropenia)." Replace the first sentence when
      the case has a real point (table below).
    - `alternatives`: empty list, or remove the field if the schema allows.
  - Case-specific real content (the only medicine-level statements allowed):
    | case | real content |
    | --- | --- |
    | M03 | apixaban (CYP3A4/P-gp) and metoprolol: no interaction; 1-2 drinks nightly: advise reducing alcohol because riluzole can raise transaminases |
    | M04 | tamoxifen can raise transaminases: monitor LFTs as scheduled and share results with oncology; existing regimen note kept: sertraline is a moderate CYP2D6 inhibitor and can lower endoxifen, flag to oncology |
    | M06 | methotrexate and riluzole can both raise transaminases: coordinate LFT monitoring with rheumatology and review the methotrexate dose if ALT rises; alendronate: oral bisphosphonates need an upright posture and can injure the oesophagus, review if swallowing worsens |
    | M08 | natalizumab: no pharmacokinetic interaction; rare natalizumab liver injury, so LFT monitoring covers both; natalizumab causes lymphocytosis, interpret the white cell count accordingly |
    | P05 | bictegravir/emtricitabine/tenofovir alafenamide: no clinically significant interaction expected; continue ART unchanged |
    | P09 | quetiapine and sertraline: no clinically significant interaction expected (sertraline is not a relevant CYP1A2 inhibitor); choking episodes: use riluzole oral suspension if tablets cannot be swallowed safely |
    | S01, S08, M02 | atorvastatin can raise transaminases: interpret LFTs with both drugs in mind |
    | S02 | levothyroxine: no interaction; alendronate: review with the prescriber because dysphagia with choking raises the risk of oesophageal injury |
    | S08 | warfarin: no established interaction; check the INR within 1-2 weeks of starting riluzole, as after any new long-term medicine |
    | S09 | omeprazole is a CYP1A2 inducer and may modestly lower riluzole exposure, no dose change; levothyroxine: no interaction |
    | all others | each listed medicine: no clinically significant interaction expected |
  - Criterion text (all cases that keep it):
    - `label`: "Check riluzole against the current medicines, alcohol use and liver function before the first dose, once the diagnosis is established"
    - `rationale`: "Riluzole is metabolised by CYP1A2 and can raise liver transaminases, so the medicine list, alcohol use and baseline liver function are reviewed before treatment. <one sentence with the case's real point, or: No current medicine interacts with it.>"
    - `expected_evidence`: a short paraphrase of the case's real content, not a copy of the output summary.
    - `citations`: `["[Riluzole_SmPC]", "[EAN_ALS_2024]"]`

### C4. Respiratory function treated as diagnosis, and abnormal results left without action (PATTERNS 1, 2)

- **Wrong**: respiratory testing is placed before the diagnostic core and framed as diagnostic;
  reduced values (16 cases) are labelled "baseline" with no referral; impressions are bare "Abnormal
  values:" lists; P06 FVC 80% and SNIP 70 (man) called "all values within normal limits"; SNIP
  reference for women is >70 in M01, M04, M06, M08, P02, P05, P07 and >60 in S02, S04, S07, S09;
  MIP/NIF sign conventions differ.
- **Notes**: every respiratory placement note; f47e4e04 (RS11), 3073e9a1 (S02), 7cf92fbd (S04),
  bc8ef2aa (S06), c925df65 (S09), 5d1141b1 (S11), 72b81b92 (P06), e76c4980 (P02), abedfbbf (P08).
- **Fix**:
  - Criterion `action-7-order-specialized-test` (alternatives unchanged, `{"test_type":
    "respiratory_function"}`): `recommended`; `optional` in P02 and P08. Never required. This
    overrides criteria pack section 6 (CENTRAL).
    - `label`: "Baseline respiratory function (FVC and SNIP, with MIP where available) to stage respiratory muscle involvement and plan monitoring and NIV"
    - `rationale`: "Respiratory function does not diagnose ALS. Once ALS is supported it stages respiratory muscle weakness, sets the baseline for 3-monthly monitoring and identifies patients who need early referral for NIV."
    - `citations`: `["[AAN_2009]", "[EAN_ALS_2024]", "[NICE_NG42]"]`
  - Output: reference ranges FVC >=80% predicted, SNIP >=70 cmH2O (men) or >=60 cmH2O (women), MIP
    and NIF "-60 cmH2O or more negative"; `is_abnormal` per these ranges. Keep the stored values.
    Impression wording by category (no management, no NIV advice inside the report):
    - normal: "FVC <x>% predicted and SNIP <y> cmH2O are within normal limits; baseline for serial monitoring."
    - borderline (P06): "FVC 80% predicted and SNIP 70 cmH2O are at the lower limit of normal."
    - reduced: "Reduced FVC (<x>% predicted) and SNIP (<y> cmH2O)<, MIP/NIF <z> cmH2O>, indicating inspiratory muscle weakness."
  - Respiratory category per case (from the stored values; women's SNIP limit 60):
    - **normal**: M02, M04, M07, P01, P02, P05, P08, S01, S03, S05, S07, S08, S10
    - **borderline**: P06
    - **reduced, no AAN NIV marker**: M05, M06, M08, P03, P04, P07, P09, RM11, S02, S04, S06
    - **reduced with an AAN NIV marker**: M01 (MIP -48, NIF -52), M03 (NIF -55), RS11 (SNIP 38),
      S09 (NIF -48), S11 (NIF -52; SNIP 68 below the men's limit, FVC 80 at the limit)
  - Musts and prohibitions by category: section 2 C10 (MUST-RESP, PROHIB-RESP).

### C5. Genetic panel: placement, completeness and impressions (PATTERNS 1, 3)

- **Wrong**: genetics appears as an early pathway step; S02-S07 report only C9orf72 under a test called
  an ALS panel; M05, M06, M08, P01, P03-P07, RM11, RS11, S01, S09, S11 report C9orf72 and SOD1 only;
  negative impressions read "All values within normal limits"; M07's impression says "Pathogenic
  ALS-associated variant identified" while every result is negative; S10's positive impression is an
  "Abnormal values" list.
- **Notes**: all genetics placement notes; 77d7fcd4 (M07), de40b53e, 140104fe, 56bf56d7, a147095c,
  86d87968, 3234e797 (C9-only, S02-S07), e37b6b6b (S09), 9a2859dd (S11), 7bc08482 (S08, complete),
  6fa1a30b (P02).
- **Fix**:
  - Criterion `action-8-order-specialized-test` (`{"test_type": "genetic_panel:ALS"}`): `optional`
    in sporadic cases; `recommended` in P02, P08, P09, S10 (family history). Never required.
    - `label`: "ALS gene panel (C9orf72 repeat expansion; SOD1, TARDBP, FUS and TBK1) after pre-test genetic counselling, once the clinical and electrodiagnostic assessment is complete"
    - `rationale` sporadic: "Genetic testing does not make the diagnosis. It is offered with counselling to people with ALS because a pathogenic variant changes counselling for relatives and may open gene-targeted treatment or trials."
    - `rationale` familial: the sporadic text plus "The family history of <relative and disease> makes a monogenic cause likely."
    - `citations`: `["[ALS_genetics_2023]", "[EAN_ALS_2024]"]`
  - Output: report all five genes in every case. Add the missing genes as "No pathogenic or likely
    pathogenic variant detected". Canonical negative impression: "No pathogenic C9orf72 repeat
    expansion. No pathogenic or likely pathogenic variant in SOD1, TARDBP, FUS or TBK1. A negative
    result does not exclude a genetic contribution; post-test counselling recommended." Positive
    impression names only the finding and the other genes' result, for example S10: "Pathogenic
    C9orf72 hexanucleotide repeat expansion (<n> repeats). No pathogenic or likely pathogenic variant
    in SOD1, TARDBP, FUS or TBK1. Post-test genetic counselling recommended." No diagnosis, prognosis,
    tofersen or trial text inside the report.

### C6. EMG/NCS report incomplete or carrying cross-step advice (PATTERNS 3, 5)

- **Wrong**: motor NCS (CMAP amplitude, conduction velocity, distal latency, conduction block) missing
  in P07, P09, S04, S05, S07; conduction block not stated in S03; "Pulmonary function testing
  recommended." in `recommended_actions` of M01-M08 and P03-P07 (cross-step hint); P02's report
  explains fasciculations "in context of thyrotoxicosis" (cross-modality synthesis) and says "median
  sural normal".
- **Notes**: dcd17b55 (S03), 01ec92d7 (S04), 008369f3 (S05), fe18f6ef (S07), plus case comments
  4d9b6abe, d44d11a1, 2666c318.
- **Fix**: add a "Motor NCS" finding where missing: "Median, ulnar, peroneal and tibial motor
  studies: CMAP amplitudes <normal | reduced in the wasted muscles, with values>, distal latencies and
  conduction velocities normal (or no worse than expected for the CMAP loss), no conduction block and
  no temporal dispersion." Make the impression state "No conduction block" explicitly in every case.
  Delete "Pulmonary function testing recommended." from every EMG report; keep a repeat-EMG
  recommendation only where the report itself is uncertain (P01, P02, P08). P02: remove both
  thyrotoxicosis mentions from the EMG, change "median sural normal" to "sural normal".
- EMG criterion text (all cases, `required`, `{"test_type": "emg_ncs"}`):
  - `label`: "EMG and nerve conduction studies of the bulbar, cervical, thoracic and lumbosacral regions to document lower motor neuron involvement and exclude conduction block and neuropathy"
  - `rationale`: "EMG/NCS confirms lower motor neuron involvement beyond the clinically affected muscles and excludes the main treatable mimics: multifocal motor neuropathy with conduction block, demyelinating or sensorimotor neuropathy and myopathy. Gold Coast 2020 accepts EMG evidence of lower motor neuron dysfunction, and Awaji 2008 counts fasciculation potentials as active denervation in muscles with chronic neurogenic change."
  - `expected_evidence`: case-specific, one sentence naming the regions with active and chronic denervation, conduction (no block) and sensory result.
  - `citations`: `["[Gold_Coast_2020]", "[Awaji_2008]"]`

### C7. Diagnosis overcalled (PATTERNS 2, ALS 23/5)

- **Cases and notes**: P01 (dd04fa1d, 92755ec0, ba745e79, 3e9a616b), P02 (1bca43b9, b11bd1f7, 9db62330,
  948c5c90, 2da3016c, 785155c1), P08 (c15f3a46, 2e11ab82, d469d924, 41f0232d, 3fcc8e64).
- **Fix**: the label changes and the full rewrites are in section 4 (P01, P02, P08). Each label change
  is listed under CENTRAL. Elsewhere, remove "definite" wording that the data do not support
  (EMG `regions_denervated` strings such as M03's "bulbar definite, cervical definite" become
  "bulbar, cervical, thoracic; lumbosacral early"). M03's label "clinically definite" is left as it is
  (Awaji definite is met: UMN and LMN signs in bulbar and two spinal regions; no reviewer ruled it).

### C8. Differential not updated after the work-up (PATTERNS 2, ALS 24)

- **Wrong**: mimics the work-up excludes stay `moderate` or `high`; ALS phenotypes (progressive
  bulbar palsy, flail arm) are listed as competing diagnoses; P03 lists the target diagnosis itself
  as "very_high"; `key_features` cite results the case does not contain ("anti-GM1 negative" in 19
  cases where anti-GM1 was never tested, "androgen receptor CAG repeat normal" in RM11, RS11, S01,
  S03, S08, S10, P08 and M01 where it was never tested, "paraneoplastic panel negative" in S11,
  "blood lead ... distinguish" in M07).
- **Notes**: 36d1f205 (P03), a04ceac5 (P04), 7e2fad0b (P05), e6f29c98 (P06), 6e3e812d (P07), 256e78eb
  (P09), c2bde008 (RM11), ec0eb223 (S02), 3412b2ae (S04), 1aeafbd1 (S06), 0ef6c4bc (S07), 8ad9e0ff
  (S09), cd0a30d7 and 7b9a0161 (S10), 3403f58a (S11), and the case comment b67bcf6e (P04).
- **Fix**:
  - Every entry the results exclude: `low` (or `very_low` when nothing supports it) with
    `key_features` "supports: ...; against: ..." citing only data present in the case.
  - Remove "progressive bulbar palsy" entries (M01, M03, S02, S04, S09), "flail arm variant" entries
    (M02, P01) and P03's "lower motor neuron-predominant ALS variant" as competing diagnoses: they are
    ALS phenotypes.
    Mention the phenotype in the key evidence instead ("bulbar-onset ALS phenotype").
  - Never list the target diagnosis in the differential.
  - MMN entries: `key_features` "against: upper motor neuron signs, normal motor conduction velocities
    and no conduction block<, bulbar involvement>". Add "anti-GM1 negative" only in P03 and P06, where
    the labs contain it.
  - Kennedy disease entries (men only): `key_features` "against: upper motor neuron signs and normal
    sensory responses (SBMA is a pure lower motor neuron disorder with sensory neuronopathy)". Delete
    the entry in women (M01).
  - Per-case likelihoods: section 4.

### C9. CK above 5x ULN called typical (PATTERNS 2, ALS 5)

- **Cases**: M02 (920, 5.3x, atorvastatin), M07 (892, 5.1x), P04 (1120, 6.4x), RS11 (1240, 7.1x), S01
  (920, 5.3x, atorvastatin), S08 (920, 5.3x, atorvastatin), S10 (1240, 7.1x). All other cases are at or
  below 5x (RM11 4.9x, P03 4.8x, P07 4.8x, S03 4.8x).
- **Notes**: 3b7649bf (P04), 3f2fafd2 (RS11), cba80908 (S01), 18b94541 (S08), 4c973d17 (S10), c04b142c
  (M02 red herring), and the P04 case comment b67bcf6e.
- **Fix**: the "2-5x ULN" pearl is replaced in every case by the CK pearl of C14 (two variants by
  ratio). Lab output: CK row unchanged, `clinical_significance` null, the lab interpretation lists
  "CK <value> U/L (<ratio>x ULN)". M02's red herring (c04b142c) uses the canonical >5x wording.
  Keep the stored CK values (the notes cite them); identical values across cases (920 in M02, S01, S08;
  1240 in RS11, S10) are logged as a minor own finding, not changed.

### C10. Safety and supportive actions missing (PATTERNS 1, ALS 8)

Musts are rebuilt from the canonical set below in every confirmed-ALS case (all except P02 and
P08; P01 uses its own set in section 4). Order of musts: MUST-DX, MUST-RESP, MUST-BULBAR (if any),
MUST-RILUZOLE, case-specific medicine musts, MUST-MDT, MUST-GEN, other case-specific musts.

- **MUST-DX**: "Make and explain the diagnosis of ALS by Gold Coast 2020 criteria: progressive <onset
  region> weakness with upper motor neuron signs (<signs from the exam>) and lower motor neuron
  involvement in <regions> on examination and EMG, with mimics excluded by MRI and blood tests;
  disclose it in a planned face-to-face discussion with the patient and family."
- **MUST-RESP** by category (C4):
  - normal: "Repeat FVC and SNIP about every 3 months and ask at each review about orthopnoea, morning headache, daytime sleepiness and unrefreshing sleep, referring for NIV assessment when these appear or values fall."
  - borderline (P06): "FVC 80% predicted and SNIP 70 cmH2O are at the lower limit of normal: repeat them within 3 months and ask about orthopnoea and sleep-related symptoms of hypoventilation."
  - reduced: "Refer to the respiratory/NIV service now because FVC (<x>% predicted) and SNIP (<y> cmH2O) are already reduced; screen for orthopnoea and nocturnal hypoventilation with overnight oximetry or capnography, and repeat FVC and SNIP within 3 months."
  - reduced with an AAN marker: "Refer to the respiratory/NIV service now and discuss NIV: <value> meets an AAN 2009 marker of respiratory insufficiency; assess orthopnoea and overnight oximetry or capnography to time NIV, and repeat FVC and SNIP within 3 months."
- **MUST-BULBAR**:
  - dysphagia or choking documented (M01, M03, M06, P09, S02, S09): "Arrange a speech and language therapy swallowing assessment now (aspiration risk, safe food and fluid consistencies) and a dietetic review with baseline weight, and discuss gastrostomy early, while FVC is above 50% predicted."
  - bulbar signs without dysphagia, meaning dysarthria, tongue atrophy or palatal weakness on the exam (M04, M05, M07, M08, P03, P07, RM11, RS11, S01, S03, S04, S06): "Arrange a speech and language therapy assessment of speech and swallowing, with communication support, and monitor weight and swallowing at each review."
  - tongue fasciculations alone or no bulbar finding (M02, P01, P02, P04, P05, P06, P08, S05, S07, S08, S10, S11): no bulbar must.
- **MUST-RILUZOLE**: "Offer riluzole 50 mg twice daily. Measure liver transaminases before the first dose, monthly for 3 months, every 3 months for the rest of the first year and periodically thereafter; stop riluzole if ALT exceeds 5x the upper limit of normal, and ask the patient to report any febrile illness so that neutropenia can be excluded."
- **Case-specific medicine musts** (only these): M03 "Advise reducing alcohol (currently 1-2 drinks nightly) while taking riluzole; apixaban needs no change."; M06 "Coordinate liver-function monitoring with rheumatology because methotrexate and riluzole can both raise transaminases, and review oral alendronate given dysphagia."; S02 "Review oral alendronate with the prescriber because dysphagia with choking raises the risk of oesophageal injury."; S08 "Check the INR within 1-2 weeks of starting riluzole."; P09 "Use riluzole oral suspension if tablets cannot be swallowed safely." (P09 keeps MUST-RILUZOLE as well).
- **MUST-MDT**: "Refer to a specialist ALS multidisciplinary team (neurologist, specialist nurse, respiratory, speech and language therapy, dietetics, physiotherapy, occupational therapy and palliative care), reviewed about every 2 to 3 months, with an early, patient-paced discussion of advance care planning."
- **MUST-GEN** sporadic: "Offer genetic counselling and, if the patient wishes, ALS genetic testing, explaining the implications for relatives." Familial and positive cases: section 4.
- **Prohibitions** (`prohibited_recommendations`), rebuilt per case:
  - PROHIB-IMM (all confirmed ALS): "Do not treat ALS with corticosteroids, IVIG or plasma exchange: they have no benefit." (P03: own wording, section 4.)
  - PROHIB-RESP: normal and borderline: "Do not stop respiratory monitoring because the baseline values are normal."; reduced (both reduced categories): "Do not wait for FVC to fall below 50% or for respiratory symptoms before referring for NIV assessment."
  - PROHIB-SWALLOW (dysphagia cases only): "Do not delay the swallowing assessment in a patient who is already choking or coughing on food or fluids."
  - PROHIB-SURG only where the case's own imaging shows the degenerative finding; name the level from
    the spine report. Cervical: M01, M06 (rheumatoid cervical disease), P01, P04, RM11: "Do not refer
    for cervical spine surgery on the basis of the <level> spondylotic changes: they do not explain the
    <bulbar signs | denervation in other regions>." Lumbar: M02, M05, S11: "Do not refer for lumbar
    spine surgery on the basis of the <level> degenerative changes: they do not explain the upper motor
    neuron signs or denervation beyond the lumbosacral roots." Delete the cervical-surgery prohibition
    from every other case.
  - PROHIB-FUNC only where the case has an anxiety or depressive disorder in its history or an
    anxiety red herring: M04 (anxiety disorder), M08 (depression), P01, P08, S07 (P02 has its own
    wording in section 4): "Do not attribute the progressive weakness<, wasting> or bulbar signs to
    anxiety<, depression> or a functional disorder." Delete it in the other 24 cases.
- **Notes resolved here**: 2255e7cd and 97ab4bf6 (M03 swallowing), be2f32e2, f4d90fdc, ea2c5a1d (P09
  swallowing, capacity), 60e02483 (RS11 speech and swallowing), 1dc3dd2e and 7d6955d4 (S09), 35534ccc
  and 4d9b6abe (S04 wording), 82664160 (P03 IVIG), 4cd32c3e (S10), 73e83884 (P08 cascade), the reduced
  respiratory notes of C4, 948c5c90 and 9200b13f (P02), 5db6492b and d469d924 (P08), 8e2d2d77 (M07).

### C11. Narrative contradicts reports, and timeline leaks in the patient block (PATTERNS 3; leakage policy)

- **Wrong** (HPI states results of studies the case scores, or contradicts them):
  - M01: "PCP ordered cervical spine MRI which showed moderate spondylosis" (spine MRI scored).
  - M02: lumbar MRI result, "elevated CK ... 920 U/L" (spine MRI and labs scored).
  - M03: "Brain MRI performed by his cardiologist showed no infarct but ... corticospinal tracts".
  - M04: brain and spine MRI result; "Paraneoplastic antibody panel was ordered and results are pending"
    while the labs report negative anti-Hu and anti-Yo (note e8775879).
  - M05: lumbar MRI result with stenosis levels.
  - M06: rheumatologist's EMG findings and "CK ... 580 U/L"; family history lists the husband (note 32a75e60).
  - M08: "brain MRI shows no PML lesions" and "New MRI brain and cervical spine was ordered".
  - P01: "A repeat EMG has been ordered." and the reasoning sentence "The upper motor neuron signs are
    subtle and lower motor neuron signs are confined to one region ...".
  - P02: TSH 0.1 and free T4 2.1 values and the reasoning about thyrotoxic myopathy (labs scored).
  - P05: "MRI spine was obtained and showed ...", "CD4 count 520 cells/uL argues against ..." (reasoning).
  - P06: "Anti-MAG and anti-GM1 antibodies are pending." while labs report anti-GM1 and omit anti-MAG (note 69cfac89).
  - RM11: "elevated CK at 860 U/L", "MRI cervical spine shows moderate multilevel spondylosis", "EMG is
    scheduled." (notes 0e1a7582, f71232f0).
  - P03: red herring says "Low-titer anti-GM1 (1:100)" pointing at the labs, which report the repeat
    as negative (<1:100).
  - P04: past medical history names the phenotype ("Flail arm syndrome ... noted 12 months ago").
  - M07: genetic impression contradicts results (C5); P07 "cord signal at L3-S1" (C12); S08 brain finding
    in the spine report (C12); S04 musts claim documented dysphagia (C10); S11 differential claims a
    paraneoplastic panel (C8).
- **Fix rule**: delete the result and any reasoning sentence; keep the referral reason and who
  referred, in neutral words ("Her primary care physician referred her for neurological evaluation.").
  Prior studies dated before the encounter that the case does not score stay (P01 normal EMG 2 years
  ago, P03 EMG and anti-GM1 1:100 at the MMN diagnosis 14 months ago, P07 old polio EMG, M08 MRI 14
  months ago, M07 occupational blood lead 28 mcg/dL, S02 and S09 historical thyroid tests, S11 oncology
  imaging 8 months ago and PSA). Where a "pending" test exists, report it in the lab output and delete
  the "pending" sentence (M04 paraneoplastic, P06 anti-MAG). Exam `additional` fields that summarise
  ("Combined upper and lower motor neuron signs on examination", "Young patient with ... family history
  of ALS") are trimmed to findings only where they synthesise a diagnosis (RM11, S04, S10, P09,
  P05, S03, S05, S07; leave plain findings).

### C12. Imaging reports mixed between brain and spine, and anatomy errors (PATTERNS 3)

- **Wrong**: identical impression copied into the brain MRI and the spine MRI (M04, M05, M06, P01, P04,
  P05, P06); spine content in the brain report (M05 lumbar, M06 RA pannus, M07 L5-S1, P01 C5-C6, P04
  cervical cord, P05 cord, P06 cord, S11 lumbar facets, note b1d11959); brain content in the spine
  report (M04, M05, P01, P04, S08 motor cortex, note d91f9116); impression numbering broken (M01 "1 ...
  3.", M02 "1 ... 4.", spine impressions starting at "2." in M01, M02, P07, RM11, S08, S11);
  `body_imaging.region` always "cervical and thoracic spine" even where lumbar levels are described
  (M02, M05, S11); `findings[].description` holding JSON dumps (`{"size": ...`,
  `"signal_characteristics"`) in M01, M02, M05, M06, M07, P01, P04, P05, RM11, S11; non-contrast spine
  reporting "no leptomeningeal enhancement" (S11 note ad563de2, P05); P07 "chronic spinal cord
  signal change at L3-S1" (notes eb171932, 03220c38); M03 brain report "important given
  anticoagulation" and M07 "no lead encephalopathy" (cross-modality reasoning); red-herring
  `field_path` pointing to `mri` for a spine finding (M05, RM11).
- **Fix**: brain MRI reports only brain and brainstem (corticospinal tract signal, motor cortex,
  exclusion of structural, vascular, demyelinating, neoplastic lesions); spine MRI reports only spine
  and cord. Rewrite each impression as a numbered list starting at 1. Set `body_imaging.region` to the
  levels actually described ("cervical, thoracic and lumbosacral spine" in M02, M05, S11). Replace
  JSON-dump descriptions with plain sentences. A non-contrast study never comments on enhancement:
  remove the phrase, or, where a leptomeningeal question exists (M04 breast cancer, P05 HIV), state
  that gadolinium was given and keep the statement consistently in the protocol fields. P07: "chronic
  signal change in the cauda equina roots at L3-S1 consistent with old poliomyelitis" or, if the
  author meant the anterior horn, place it in the lower thoracic cord and conus; choose the cauda
  equina wording. Remove M03 "important given anticoagulation" and M07 "no lead encephalopathy". Fix
  the red-herring `field_path` to `initial_tool_outputs.body_imaging` (M05, RM11).
- Brain MRI criterion (all cases, `required`, alternatives `[{"tool_name": "analyze_brain_mri", "required_arguments": {}}]`):
  - `label`: "Brain MRI to exclude structural, vascular, demyelinating, inflammatory or neoplastic causes of the upper motor neuron or bulbar signs"
  - `rationale`: "MRI does not confirm ALS. It excludes brain and brainstem lesions that can cause upper motor neuron or bulbar signs<; case clause, for example: including metastasis or leptomeningeal disease after breast cancer (M04), MS activity and PML on natalizumab (M08), HIV-related CNS disease (P05), vascular lesions with atrial fibrillation (M03)>; corticospinal tract signal change, when present, is supportive only."
  - `citations`: `["[EFNS_ALS_2012]", "[Gold_Coast_2020]"]`
- Spine MRI criterion (all cases, `required`, alternatives `[{"tool_name": "order_body_imaging", "required_arguments": {"study": "spine_MRI"}}]`):
  - `label`: "Spine MRI of the cervical and thoracic cord, and of the lumbosacral spine when lower limb signs need it, to exclude compressive myelopathy, radiculopathy and other cord lesions"
  - `rationale`: "Cervical spondylotic myelopathy with radiculopathy is the commonest structural mimic of combined upper and lower motor neuron signs in the limbs. Spine MRI excludes it, but incidental spondylosis does not explain bulbar signs or denervation in other regions and must not delay the ALS work-up."
  - `citations`: `["[EFNS_ALS_2012]", "[Gold_Coast_2020]"]`
- Notes: 82961391 (M02 MRI role), ea4bbcb7 (M03 MRI role), 78281d7e (M01 spine framing), d91f9116 and
  29717cf6 (S08), b1d11959 and ad563de2 (S11), eb171932 and 03220c38 (P07).

### C13. Lab report structure, engineering leakage and criterion matching (PATTERNS 3, 5)

- **Wrong**: panels named "Exclusion studies" (27 cases, Free T4 as the string "Within reference
  range" and `clinical_significance` "Ordered to exclude an alternative cause; the result does not
  support one, which is what this case's diagnosis rests on"), "Reviewer baseline rule-out additions"
  (29 cases), "Mimic exclusion" (P04, P05, S06; TSH as a string; TSH duplicated in P04);
  interpretation "Rule-out studies do not confirm ALS. Targeted abnormalities are listed above." in
  all 30 (names the diagnosis); CBC, renal or liver results missing in many outputs although the
  criterion requires CBC and CMP (S01, S04, P01, P02 and others); P06 lab row "TSH (POEMS
  endocrinopathy)"; S11 ALT and ALP inside "Neuromuscular_Panel"; P03 criterion asks
  `anti_GM1_IgM`, which does not fold to the vocabulary term "anti-GM1 IgM" (an agent ordering the
  advertised term misses the required criterion); P05 has no current viral load or CD4; M07 has no
  blood lead in the labs; P06 has no anti-MAG.
- **Fix, output**: rebuild `initial_tool_outputs.labs.panels` with these panel names (only the ones the
  case has): "Complete blood count" (haemoglobin, WBC, platelets), "Comprehensive metabolic panel"
  (sodium, potassium, creatinine, glucose, calcium, albumin, ALT, AST, ALP, bilirubin), "Creatine
  kinase", "Thyroid function" (TSH and free T4, both numeric), "Vitamins" (vitamin B12, folate),
  "Inflammatory markers" (ESR, CRP), then the case's own panels ("Paraneoplastic antibodies",
  "Serum protein electrophoresis and immunofixation", "HIV", "Anti-GM1 IgM", "Androgen receptor CAG
  repeat", "Blood lead", "Rheumatology" for M06). Keep every stored value; add missing core analytes
  with normal values; numeric values only; no duplicates; `clinical_significance` null for normal
  rows and a short factual phrase for abnormal rows ("Above reference range"), never a sentence about
  the case's diagnosis. `abnormal_values_summary` lists the abnormal rows with values. Canonical
  `interpretation`: "Abnormal: <each abnormal analyte with value and unit; CK also with its multiple
  of ULN>. All other results are within reference ranges." Never name ALS or a mimic in the lab
  interpretation.
- **Fix, criterion** `action-5-interpret-labs` (`required`): `required_arguments.panels` =
  `["CBC", "CK", "TSH", "vitamin_B12"]` plus the case analytes below, spelled exactly as the
  vocabulary advertises. Where the vocabulary has several names for one assay, add one alternative per
  name (same other panels).
  | case | added analyte(s) | alternatives |
  | --- | --- | --- |
  | M04 | paraneoplastic panel | three alternatives: `paraneoplastic_panel`, `paraneoplastic`, `paraneoplastic_antibodies` |
  | P02 | `free_T4` | one |
  | P03 | `"anti-GM1 IgM"` | one |
  | P04 | `"androgen receptor CAG repeat"` | one |
  | P05 | `HIV` | one |
  | P06 | `SPEP`, `IFE`, `serum_free_light_chains`, `anti_MAG` | one |
  | all others | none | one |
  - `label`: "Blood tests for treatable mimics and a pre-treatment baseline: full blood count, renal and liver function, electrolytes and calcium, CK, thyroid function, vitamin B12 and folate, ESR and CRP<; plus case tests>"
  - `rationale`: "These tests exclude metabolic, endocrine, nutritional and inflammatory mimics and give the liver and blood-count baseline needed before riluzole; phenotype-specific tests are added only when the case raises that mimic<: case clause>."
  - `citations`: `["[EFNS_ALS_2012]"]`
- **CSF output** (M04, M08, P03, P05, P06): remove Python dict dumps and "CSF does not confirm ALS";
  numeric values with units; interpretation states the CSF findings only. CSF criterion
  `action-9-analyze-csf` stays `optional`; P03's `{"special_tests": []}` becomes `{}`; keep the others'
  special tests (M04 cytology and flow cytometry, M08 oligoclonal bands, IgG index, JCV PCR, P05
  HIV_RNA, P06 cytology and flow cytometry) and check that the output reports each one.
- Notes: e8775879 (M04 pending), 69cfac89 (P06 anti-MAG), 8e2d2d77 and 30c38fd0 (M07 lead), 0ca4443e
  (P05 viral load and CD4: report them inside the "HIV" panel, see CENTRAL for vocabulary).

### C14. Templated musts, prohibitions and teaching pearls (PATTERNS 4, 5)

- **Wrong**: the same 7-8 musts in all 30, most of them diagnostic actions ("Perform EMG/NCS ...",
  "Obtain brain MRI to exclude structural mimics (cervical myelopathy, ...)" which brain MRI cannot
  exclude, a lab must listing HIV, RPR, SPEP, anti-GM1 and "androgen receptor CAG repeat in males" in
  women too, "Measure baseline respiratory function", "Apply Awaji-Shima 2008 / Gold Coast 2020");
  irrelevant prohibitions (cervical surgery without spondylosis, functional dismissal without any
  psychiatric element; "Do not continue oral feeding without a swallowing assessment given documented
  dysphagia" in S04, which has no dysphagia); pearls with engineering text ("July 2026 review applied end to end ..." in all
  30), the "2-5x ULN" CK pearl in all 30, an El Escorial "bulbar plus at least 2 spinal regions
  satisfies" EMG pearl, "Normal sensory NCS ... pivotal" where sensory NCS are abnormal (M02, M05, M08,
  S06, note 5c698397), a spondylosis pearl where the imaging shows none.
- **Fix, musts and prohibitions**: delete all existing musts and prohibitions and rebuild from C10
  plus section 4. Diagnostic actions are criteria, not musts (exception: the repeat-EMG musts of P01,
  P02, P08, which are follow-up actions).
- **Fix, key_clinical_evidence** (rebuild; 4 to 7 pearls; case values filled in):
  - K-GC (all confirmed ALS): "Gold Coast 2020: ALS needs progressive motor impairment with upper and lower motor neuron dysfunction in at least one body region, or lower motor neuron dysfunction in at least two, after other diseases are excluded. Here: <UMN signs> with lower motor neuron involvement in <regions>."
  - K-EMG (all): "EMG lower motor neuron evidence is chronic neurogenic change with active denervation; by Awaji 2008 fasciculation potentials count as active denervation in a muscle with chronic neurogenic change."
  - K-NCS, normal sensory: "Normal motor conduction velocities without conduction block argue against multifocal motor neuropathy, and normal sensory responses argue against a sensorimotor neuropathy or SBMA."
  - K-NCS, reduced sural (M02, M05, M08, S06): "Mildly reduced sural responses fit a coexisting length-dependent neuropathy<, here diabetic (S06)> and do not explain widespread motor denervation; motor conduction is normal with no conduction block."
  - K-CK at or below 5x: "CK <value> U/L (<ratio>x ULN): mild to moderate elevation is common in ALS from denervation and does not by itself suggest a myopathy." Omit when CK is normal (P02).
  - K-CK above 5x: "CK <value> U/L is <ratio>x ULN, higher than usual in ALS: consider a myopathic contributor clinically<, including statin myopathy on atorvastatin>, while the neurogenic EMG pattern with fasciculations and upper motor neuron signs argues against a primary myopathy."
  - K-RESP: "<FVC and SNIP values and category>. AAN 2009 markers that prompt NIV discussion are orthopnoea, FVC below 50% predicted, SNIP below 40 cmH2O, MIP weaker than -60 cmH2O or abnormal overnight oximetry; NIV prolongs survival and improves quality of life (Bourke 2006)."
  - K-SPINE only where spondylosis or lumbar degeneration is on the case's imaging: "Spondylotic changes are common at this age; they cannot explain <bulbar signs | denervation in thoracic, lumbosacral or bulbar muscles>."
  - K-BULBAR only in bulbar-onset or dysphagia cases: "Bulbar involvement carries a worse prognosis and an aspiration risk; swallowing assessment and early gastrostomy discussion, while FVC is above 50% predicted, are priorities."
  - K-GEN only in familial or positive cases: section 4.
  - Delete the "July 2026 review" pearl, the El Escorial EMG pearl and the generic "2-5x" pearl.

### C15. Red herrings misframed or misplaced

- **Notes**: c04b142c (M02 CK), c37f2d88 (M05 lumbar stenosis), 1b14a503 (M06 RA), 8e2d2d77 (M07 lead),
  62cb7f37 (M08 MS), dfaf2518 (P05 HIV), 2da3016c (P02 anxiety), c66738c7 (S07 anxiety).
- **Fix**: each red herring's `correct_interpretation` says what the confounder can and cannot explain,
  using only the case's data (the reviewers' wording in each note is the content to use). `location`
  and `field_path` point to where the data point really is. S07: add a red herring for the anxiety
  disorder if absent: data_point "Anxiety disorder", location "Past medical history", field_path
  `patient.clinical_history.past_medical_history`, intended_effect "Tempts the agent to attribute
  symptoms to health anxiety", correct_interpretation "Anxiety can heighten symptom vigilance but
  cannot produce Babinski and Hoffman signs, tongue fasciculations or multi-region EMG denervation;
  the full ALS work-up is required regardless."

### C16. Criterion mechanics and citation format

- Brain MRI `{}` (was `{"contrast": true, "protocol": "standard"}`: an agent ordering a correct
  non-contrast MRI failed a required criterion); spine `{"study": "spine_MRI"}` (was `contrast: false`);
  labs per C13; CSF P03 `{}`; DI and other criteria unchanged.
- `label` and `rationale` differ (they were identical in all 30): use the C3-C6, C12, C13 texts.
- `citations` per section 1.1 format.
- Keep every `criterion_id` unchanged (the literature id disappears; nothing is renumbered).

### C17. Template carry-over and record errors

- M01 (woman): delete the Kennedy differential entry and "no gynecomastia" from the exam.
- M06: move "Husband: alive, type 2 diabetes" out of `family_history` (note 32a75e60); if the
  living situation needs it, `social_history.living_situation` "Lives with her husband".
- "androgen receptor CAG repeat in males" lab must: deleted with C14.
- Metadata claims that the data do not support (M03 notes "Rapid progression indicated by high NfL",
  no NfL in the case): reword to what the case contains. Do not add review notes to metadata.

---

## 3. Target pathway and tiers

### 3.1 `action_criteria` order and tiers (identical in every case unless the table says otherwise)

| order | criterion_id | tool / required_arguments | tier |
| --- | --- | --- | --- |
| 1 | `action-6-order-specialized-test` | `order_specialized_test` `{"test_type": "emg_ncs"}` | required |
| 2 | `action-3-analyze-brain-mri` | `analyze_brain_mri` `{}` | required |
| 3 | `action-4-order-body-imaging` | `order_body_imaging` `{"study": "spine_MRI"}` | required |
| 4 | `action-5-interpret-labs` | `interpret_labs` per C13 | required |
| 5 | `action-9-analyze-csf` (M04, M08, P03, P05, P06 only) | `analyze_csf` per C13 | optional |
| 6 | `action-7-order-specialized-test` | `order_specialized_test` `{"test_type": "respiratory_function"}` | recommended (optional in P02, P08) |
| 7 | `action-8-order-specialized-test` | `order_specialized_test` `{"test_type": "genetic_panel:ALS"}` | optional (recommended in P02, P08, P09, S10) |
| 8 | `action-2-check-drug-interactions` | `check_drug_interactions` `{"drug": "riluzole"}` | recommended (required M06, optional P01, deleted P02 and P08) |
| - | `action-1-search-medical-literature` | deleted in all 30 | - |

### 3.2 Follow-ups and initial outputs

- `followup_outputs` order: respiratory function, genetic panel, riluzole interaction check (P02 and
  P08: respiratory, genetic). Delete every literature follow-up.
- `initial_tool_outputs`: `specialized_test` (EMG), `mri`, `body_imaging`, `labs`, `csf` (5 cases)
  stay; `literature_search` = null and `drug_interactions` = null in all 30.
- `avoided_actions`: keep the eight waste items (EEG, ECG, echocardiogram, cardiac monitoring, CT,
  amyloid PET, DaTscan, FDG PET) unchanged. Do not add CSF as waste this round (open question Q8).

### 3.3 Sequence constraints (new in every case; all `soft`)

1. `before_criterion_id` `action-6-order-specialized-test`, `after_criterion_id`
   `action-8-order-specialized-test`, reason "Genetic testing follows the clinical and
   electrodiagnostic assessment and pre-test counselling; it does not make the diagnosis.",
   citations `["[ALS_genetics_2023]"]`.
2. Where `action-2-check-drug-interactions` exists: before `action-6-order-specialized-test`, after
   `action-2-check-drug-interactions`, reason "Riluzole is considered only after the clinical and
   electrodiagnostic assessment supports ALS.", citations `["[EAN_ALS_2024]"]`.

No hard constraints: no reverse order is unsafe in this condition.

### 3.4 Stop rule

Unchanged: `required_before_assessment` = action-3, action-4, action-5, action-6;
`max_additional_actions` = 0.

### 3.5 Panel exemptions

None needed: the generation panel requires specialized_test, MRI, body_imaging and labs, all kept;
literature is not panel-required. If a worker removes anything else, add the exemption and log it.

---

## 4. Per-case index

Each case: the notes (with the class that resolves each), survey findings, and the decisions that are
specific to the case. Every case also gets all of section 2 and 3. "Resp" = respiratory category of
C4; "Bulbar" = MUST-BULBAR variant of C10.

### ALS-M01 (woman, 62, bulbar onset; R1 needs_changes, R2 pending)
- Notes: a4f2f7d7-3db5-4e46-a063-f6b850457c5b C1; 44072246-f418-4f13-8e78-702080e6b3d3 C1, C3; 7f4e889f-784b-45e2-a28c-12441a846039 C1, C4; 6a8c17dc-1b00-4571-97a2-b9cdd3293dfc C1, C5; 78281d7e-581b-464f-810d-cdfb684881fd C12 (spine framed as mimic exclusion; spondylosis does not explain bulbar signs: rationale text of C12 and K-SPINE); e39e5677-3386-4fa6-adab-01540f6118d8 C1.
- Survey: literature initial echoes expected text; DI lists grapefruit, levothyroxine CYP1A2, AMX0035, edaravone; EMG has the PFT hint; brain MRI numbering "1 ... 3.", spine numbering starts at "2.", JSON-dump descriptions; HPI leak (cervical MRI result); Kennedy entry and "no gynecomastia" in a woman (C17); resp MIP -48, NIF -52, SNIP 48 (women limit 60), FVC 72.
- Decisions: Resp = reduced with AAN marker (MIP -48 cmH2O). Bulbar = dysphagia (choking on thin liquids). PROHIB-SURG cervical (spondylosis). Differential: cervical spondylotic myelopathy low (does not explain bulbar signs or tongue denervation); delete the "progressive bulbar palsy" entry; MMN low with C8 wording; myasthenia gravis low (against: tongue atrophy, fasciculations, EMG denervation); delete Kennedy. Keep K-BULBAR and K-SPINE.

### ALS-M02 (man, 58, limb onset; R1 needs_changes)
- Notes: 48e28c3c-7c64-4210-933f-6cba6ee108da C1; 27adc963-aeb2-4a5e-95e1-f803b060889d C1 (EMG first; EMG text already shows multi-region active and chronic change); 81aad685-02fa-4795-a247-34da189eb8e9 C1, C3; f3825c75-09df-4ea2-8ff8-e05d432f9bd2 C1, C4; 77948566-be4b-441d-8ce0-a7a2eb9399a9 C1, C5; c04b142c-9259-4485-860e-b00292be8d5a C9, C15 (CK red herring: "CK 920 U/L is 5.3x ULN, higher than usual in ALS; statin myopathy can contribute, but the neurogenic EMG pattern, fasciculations, preserved sensation and upper motor neuron signs argue against a primary myopathy"); 82961391-3081-41be-92f0-0d024951c17f C12 (MRI supportive, not confirmatory: brain MRI rationale and report wording); e04aa960-9f76-4a7f-bedb-a5acb384fd96 C1.
- Survey: atorvastatin; CK 5.3x; HPI leaks CK 920 and lumbar MRI result (C11); spine region wrong (lumbar levels described, set "cervical, thoracic and lumbosacral spine"); sural mildly reduced (K-NCS reduced-sural variant); DI metformin "hepatic" claim; Resp normal (FVC 81, SNIP 72).
- Decisions: Resp = normal. Bulbar = none (no bulbar symptoms or signs). PROHIB-SURG lumbar (L4-L5 degenerative disc disease). Differential: cervical radiculopathy / myelopathy low (does not explain thoracic and lumbosacral denervation); add lumbar radiculopathy low (the case raises it); add statin-associated myopathy low (supports: CK 5.3x on atorvastatin; against: neurogenic EMG, fasciculations, UMN signs); IBM low; delete the "flail arm variant" entry; MMN low; myasthenia gravis very_low.

### ALS-M03 (man, 65, bulbar onset, atrial fibrillation on apixaban, lives alone; R1 needs_changes)
- Notes: 0b0e9b4c-4820-4156-9474-fc3e254783d8 C1; 58cf87ba-7f2f-47ae-98df-2d3ebeccd299 C1, C3; 0ba850d5-eefe-40f3-9b64-87ec1a0cd0d5 C1, C6 (EMG required first); 077c2cc4-793d-48e5-9181-669f94947af2 C1, C4; 2255e7cd-9288-465f-8968-4386905b2d03 C10 (swallowing as an early safety must: MUST-BULBAR dysphagia, placed second in the musts after MUST-DX and MUST-RESP; mention that he lives alone); 5c29680e-032c-4cdd-a68e-0ceef347bd01 C1, C5; ea4bbcb7-e208-4d41-8967-e7c60ffe62d2 C12 (brain MRI rationale: vascular mimics with AF); 97ab4bf6-1a0c-467f-8981-6c6769ec109e C1, C10.
- Survey: HPI leak (cardiologist's brain MRI result); brain report "important given anticoagulation"; DI apixaban; alcohol 1-2 drinks nightly; EMG `regions_denervated` "definite" wording (C7); metadata NfL claim (C17); Resp NIF -55, SNIP 41, FVC 68.
- Decisions: Resp = reduced with AAN marker (NIF -55 cmH2O). Bulbar = dysphagia. Case medicine must (alcohol, apixaban). Differential: delete "progressive bulbar palsy" entry; brainstem stroke low (AF; MRI excludes infarct); MMN low. Keep label (clinically definite is met).

### ALS-M04 (woman, 55, breast cancer in remission on tamoxifen and sertraline; R1 needs_changes)
- Notes: c7a0d7f8-ddb8-41f6-b17b-7d55dd2e9cd1 C1; b8ed6243-1422-4877-80f4-115e52d9ff05 C1, C3; 74fd510e-c9d0-439d-95d3-cbe0bc756d8e C13 (CSF kept optional and targeted to the leptomeningeal/paraneoplastic question; rationale says CSF does not diagnose ALS); 1af03245-5363-4229-839a-db8c1405e006 C1, C5; a578c958-8aa3-47c7-a142-f28c1d50a9d6 C1, C4; e8775879-6037-47e6-9e6a-f968ff243422 C11 (delete the "pending" sentence; the labs report anti-Hu and anti-Yo negative inside "Paraneoplastic antibodies"); 991657f8-6496-4db0-8a4d-5bdba698876a C1.
- Survey: HPI leaks brain and spine MRI result; same impression in brain and spine (C12); brain content in the spine report; CSF dict dumps; Resp normal (FVC 84, SNIP 76).
- Decisions: Resp = normal. Bulbar = signs without dysphagia (mild tongue atrophy). Lab criterion with three paraneoplastic alternatives. Brain MRI and spine MRI: state that gadolinium was given (leptomeningeal question) and keep both reports region-pure. Differential: paraneoplastic motor neuronopathy low (antibodies negative, CSF cytology negative, classic EMG); leptomeningeal metastasis very_low; MMN low. CSF criterion rationale: "the breast cancer history raises a leptomeningeal or paraneoplastic question; CSF does not diagnose ALS".

### ALS-M05 (man, 68, lower-limb onset, prior prostatectomy; R1 needs_changes)
- Notes: 25b4daef-5de6-4228-a670-118e0eceefe4 C1; 361a9f2b-bd65-4d95-9a57-b8aed9d80fcf C1, C3; cb8459b2-d53b-4ef9-ade5-4b55d8cd33dd C2 (literature "neurosurgery consultation deferred" deleted; becomes PROHIB-SURG lumbar); c37f2d88-f303-4a6f-8071-bde40f6e4567 C15 (lumbar stenosis red herring wording from the note; field_path to body_imaging, C12); a49854ff-936d-457c-b149-2af8dc8cdeba C1, C4; ada8601b-01a5-4c15-b965-bcab17b7ca06 C1, C5; f6fe970a-aeda-4e3d-9d52-5bf863bc17e8 C1, C2.
- Survey: HPI leak (lumbar MRI result); lumbar content in the brain report; same impression in both; spine region must include lumbosacral; sural mildly reduced; Resp FVC 79, SNIP 62 (men).
- Decisions: Resp = reduced. Bulbar = signs without dysphagia (mild tongue atrophy; he denies dysarthria and dysphagia). PROHIB-SURG lumbar (L3-L4 and L4-L5 stenosis). Differential: lumbar spinal stenosis with radiculopathy low (does not explain bilateral Babinski, tongue fasciculations or cervical and thoracic denervation); diabetic amyotrophy low (keep: he has type 2 diabetes); hereditary spastic paraparesis, primary lateral sclerosis and adult-onset SMA very_low with key_features from the case.

### ALS-M06 (woman, 71, rheumatoid arthritis on methotrexate; R1 needs_changes)
- Notes: 8aa7101a-bc57-4cc9-94ef-a0641d0a81bd C1; cc56c62e-8bd2-4f25-ac16-0e43b5e9de83 C1, C3; c5bda677-7348-4edf-a4de-681b25afd0f1 C2 (literature "ALS-RA comorbidity" deleted); 1b14a503-d29c-4bb0-a114-f557ba88279b C15 (RA as confounder: ESR/CRP and joint deformity from RA; RA does not explain tongue fasciculations, UMN signs, preserved sensation and multi-region denervation); ba26957f-69df-45b7-a3d0-b7696f11f5c7 C1, C4; 7a4732cf-c441-4a48-866c-ac49a58b4d5e C1, C5; 32a75e60-527e-46c1-80c0-8421d70be186 C17 (husband out of family history); b9c53147-2daf-4e26-a7d8-7e5a6f62f17b C1.
- Survey: HPI leaks the rheumatologist's EMG findings and CK 580; RA pannus in the brain report; DI invents "LFT every 2 weeks"; mild dysphagia to solids; alendronate; Resp FVC 76, SNIP 55 (women).
- Decisions: DI criterion `required` (methotrexate and riluzole both raise transaminases; management changes: coordinated LFT monitoring and methotrexate dose review). Resp = reduced. Bulbar = dysphagia. Case medicine must (methotrexate coordination and alendronate). PROHIB-SURG cervical (mild C3-C6 degenerative foraminal narrowing; the spine report excludes RA pannus at C1-C2). The brain MRI impression currently reads "No cervical cord compression from RA pannus": it is a spine statement, rewrite the brain report (C12). Differential: rheumatoid muscle/tendon disease low; vasculitic neuropathy low; IBM low; cervical myelopathy from RA very_low (no pannus, no cord compression); methotrexate myopathy very_low.

### ALS-M07 (man, 59, former firefighter, prior blood lead 28 mcg/dL; R1 needs_changes)
- Notes: 27fe005e-a718-4108-aca8-c77a7b4ca8ab C1, C2; 30c38fd0-2fc6-432f-84b8-312ca957e8d3 C2, C13 (literature deleted; repeat blood lead added to the labs); 308c92ea-5846-4b3a-b4e3-30691890bd4a C1, C3; 77d7fcd4-8486-4032-b6d4-55294300d585 C5 (impression corrected to the canonical negative text); fddd54d3-679b-441d-b6f7-d44432ece288 C1, C4; 8e2d2d77-b90d-47c8-8c86-1c2e2844cf9f C13, C15, C8 (add "Blood lead" panel to the labs with a repeat value consistent with the prior 28 mcg/dL, for example 24 mcg/dL, reference <5 mcg/dL, abnormal; and state in the red herring and differential that the EMG shows multi-region anterior horn cell denervation with normal sensory studies and no conduction slowing or block, which lead neuropathy does not produce, and that lead does not cause upper motor neuron signs); dc07427d-dc87-48ba-88f4-251cfb917757 C3 (AMX0035 line deleted); 2308b1c4-78be-4366-9e6d-287156990a1a C1.
- Survey: CK 5.1x (C9); brain report "no lead encephalopathy" and L5-S1 content (C12); Resp normal (FVC 82, SNIP 74). The HPI's prior lead level stays (occupational health, before the encounter, not scored).
- Decisions: Lab criterion core only (blood lead is in the output but not required: the prior level is already known). Add a must: "Refer to occupational health to stop further lead exposure and repeat the blood lead level; the lead level does not explain the upper and lower motor neuron syndrome." Resp = normal. Bulbar = signs without dysphagia (subtle left tongue atrophy). Differential: lead toxic motor neuropathy low (with the note's reasoning); MMN low; hereditary motor neuropathy, cervical myelopathy and IBM low or very_low with key_features from the case.

### ALS-M08 (woman, 63, relapsing-remitting MS on natalizumab, JCV antibody positive; R1 needs_changes, R2 pending)
- Notes: 52d9a7bf-e7aa-4e20-a4fd-7b254bd71c3e C1; 25746607-f788-44a3-9a59-95c6588f18e2 C1, C3; ebf2dc98-1e0a-43e2-9380-23de02e2f9bf C2; 62cb7f37-9f98-447d-bfa2-289347b89291 C15 (MS as confounder: stable lesions explain baseline spasticity and sensory symptoms, not tongue atrophy and fasciculations, new wasting or multi-region denervation); eb63c44b-a324-4e0a-b71e-07ae0a81f62f C1, C4; 53da6db5-a4bb-4da1-8f0e-0c89f5b24c81 C3; 123f27f8-88f9-4791-a3f2-f58649d6b7c0 C1, C5; 7d69e683-31be-48d9-b6aa-98002e294a7b C1.
- Survey: HPI leaks the current brain MRI result and "New MRI ... was ordered"; DI "lymphopenia" error; sural mildly reduced; CSF dict dumps; dysarthria present; Resp FVC 78, SNIP 60 (women: at the limit; FVC reduced).
- Decisions: Resp = reduced. Bulbar = signs without dysphagia. Brain MRI with gadolinium (MS activity and PML question), region-pure. Add a prohibition: "Do not treat the new tongue wasting, fasciculations and multi-region denervation as an MS relapse with corticosteroids." Add a must: "Inform the MS team; decisions on continuing natalizumab (JCV antibody positive) stay with them." Differential: MS relapse low; PML very_low (MRI and JCV PCR negative); MMN low.

### ALS-P01 (man, 52, early limb onset after a benign fasciculation syndrome diagnosis; R1 needs_changes)
- Notes: dd04fa1d-5520-44cf-b473-44d5d6bc5d40 C7 (label); 92755ec0-38eb-48e7-8b12-979108e33695 C1, C2, C7 (repeat EMG as a key action); d92369d6-0b68-4c28-b664-06c3b36e07eb C2, C7; 8ad11950-ddca-4e21-af5a-3f5f73180f0d C2 (statement deleted with the literature output; key evidence uses the softened wording below); 0f3c6f3c-3d94-4219-bb84-3d86c9b183c8 C1, C3; ba745e79-d2d0-4ca1-ae6c-21ae45c57129 C7, C10 (repeat EMG and close follow-up must); c2c49db5-2f22-4b15-8bb1-5ce40d23048f C1, C4; 3b92882f-d181-4b84-8463-4cdb4d254fdc C3; 3e9a616b-5243-400a-8b3c-b5a823a67ee8 C1, C7.
- Survey: EMG shows active and chronic denervation in the right cervical region only, complex fasciculations elsewhere; UMN signs: right Hoffman, brisk reflexes, plantars equivocal; HPI leak "A repeat EMG has been ordered" and reasoning sentence; spine content (C5-C6 foraminal) in the brain report; same impression in both; Resp normal (FVC 86, SNIP 82).
- Decisions:
  - Label: `accepted[0]` = "Amyotrophic lateral sclerosis (ALS), early limb-onset, possible ALS by Awaji criteria" (keep `icd_codes[0]` G12.21; do not touch appended synonyms; CENTRAL).
  - DI criterion `optional`; genetics optional; resp recommended.
  - Musts (replace C10's set): (1) "Explain that the findings raise strong concern for early ALS (upper motor neuron signs with active and chronic denervation in the right cervical region and complex fasciculations elsewhere) and that confirmation needs follow-up." (2) "Repeat EMG/NCS in about 3 months with clinical review, looking for active denervation spreading beyond the cervical region." (3) MUST-RESP normal. (4) "Discuss riluzole and its monitoring now, to start when the diagnosis is confirmed at review." (5) "Refer to the specialist ALS clinic for follow-up and multidisciplinary support." (6) MUST-GEN sporadic.
  - Prohibitions: "Do not reassure him on the basis of the earlier benign fasciculation syndrome diagnosis: new weakness, wasting, upper motor neuron signs and denervation override it."; PROHIB-SURG cervical (foraminal changes); PROHIB-FUNC; PROHIB-IMM.
  - Key evidence adds: "Complex fasciculations raise concern for motor neuron disease, especially with weakness, atrophy and chronic neurogenic change, but are not diagnostic alone; progression on repeat EMG confirms the diagnosis."
  - Differential: benign fasciculation syndrome low (new wasting, UMN signs, denervation); MMN low; cervical radiculopathy low; delete "flail arm" if present.

### ALS-P02 (woman, 49, C9orf72 expansion, father died of ALS, post-radioiodine on levothyroxine; R1 needs_changes)
- Notes: 1bca43b9-d0b4-415c-abb7-9eedb23fba0c C7 (relabel); b11bd1f7-cb85-4893-84ce-a56cc4966ded C7, C10 (thyrotoxicosis is the leading explanation; correction first); 9db62330-df12-4537-b776-663ba6ee3f08 C6, C7 (EMG impression: no current electrodiagnostic evidence of ALS; repeat only if objective progression); 9200b13f-974c-4bb0-96cd-311d14d6a302 C3, C10 (DI criterion and output deleted; replaced by thyroid correction, counselling, follow-up); 6fa1a30b-0d45-4a44-b76f-c11f74706554 C5, C7 (carrier status separated from diagnosis); 948c5c90-11c4-49ee-bb8e-0ebc8a6c15ea C10 (musts below); 2da3016c-756b-4c74-9eec-87ab3c3b55fa C15 (red herring rewritten); e76c4980-b433-4630-a780-9880ffc7d1f3 C4 (respiratory optional, baseline only, not ALS management); a332a5e7-9489-415d-be1f-3155e2772691 C3; 785155c1-e3e9-44e8-902e-59eba7f0d219 C7.
- Survey: HPI leaks TSH 0.1 and free T4 2.1 and reasoning (C11); labs: TSH and free T4 abnormal, TSI 180% positive, CK normal, no CBC/CMP (C13); EMG simple fasciculations, no denervation, motor NCS normal, median SNAPs 18 and 16 uV called mildly reduced, "median sural" typo; no UMN signs; right thenar "suggestion of atrophy"; differential cites "objective EMG denervation" and "UMN signs" that do not exist.
- Decisions:
  - Label: `accepted[0]` = "Thyrotoxicosis from levothyroxine over-replacement in a C9orf72 repeat-expansion carrier, ALS criteria not met"; `icd_codes[0]` = "E05.90". Do not hand-edit the appended G12.21 synonyms and codes; CENTRAL must strip them and add E05.90 synonyms (otherwise an agent answering "ALS" still matches). If `case_io.py check` fails on the synonym guard, log BLOCKED for that line only.
  - Criteria: EMG, brain MRI, spine MRI, labs required (labs add `free_T4`); respiratory optional; genetics recommended (father with ALS); DI deleted. Sequence constraint 1 only.
  - EMG impression: "No fibrillation potentials, positive sharp waves or chronic neurogenic change. Simple fasciculation potentials in the right first dorsal interosseous and both gastrocnemii. Motor conduction normal with no conduction block. Median sensory amplitudes at the lower limit (18 and 16 uV), sural normal. No current electrodiagnostic evidence of motor neuron disease; repeat if objective weakness or wasting progresses."
  - Musts: (1) "Treat the thyrotoxicosis: reduce the levothyroxine dose with endocrinology input (TSH 0.1 mIU/L, free T4 2.1 ng/dL after radioiodine; TSI remains positive, so ask endocrinology to consider residual Graves activity) and recheck TSH and free T4 in 6 to 8 weeks." (2) "Explain that ALS is not established: there are no upper motor neuron signs and EMG shows only simple fasciculations without denervation; reassess strength and fasciculations once she is euthyroid." (3) "Provide post-test genetic counselling about the C9orf72 expansion (ALS and frontotemporal dementia risk); offer counselling to adult first-degree relatives, and defer predictive testing of her teenage children until they can decide for themselves." (4) "Record an objective neurological baseline (MRC grades in named muscles, reflexes, ALSFRS-R) and review in clinic, repeating EMG only if objective weakness, wasting or upper motor neuron signs develop." (5) "Continue support for anxiety and depression, acknowledging her fear of ALS."
  - Prohibitions: "Do not diagnose ALS or start riluzole on the basis of C9orf72 carrier status and fasciculations."; "Do not attribute the weakness to anxiety before the thyroid excess is corrected and she is reassessed."
  - Red herring rewrite: data_point "Anxiety and hypervigilance about her father's ALS"; correct_interpretation "Anxiety can amplify symptom perception, but the current medical explanation for weakness and fasciculations is thyrotoxicosis; ALS is not confirmed (no UMN signs, no EMG denervation)." Add a second red herring: data_point "C9orf72 pathogenic repeat expansion", location "Genetic panel", field_path the genetic follow-up output, intended_effect "Tempts the agent to label symptomatic ALS from carrier status", correct_interpretation "Carrier status is a genetic risk, not a diagnosis; Gold Coast criteria are not met."
  - Differential: early symptomatic C9orf72 ALS low (against: no UMN signs, normal CK, EMG without denervation); benign fasciculations amplified by anxiety moderate; median neuropathy at the wrist (carpal tunnel syndrome) low (right thenar weakness and borderline median sensory amplitudes); MMN very_low (normal motor conduction, no block); delete "Familial ALS without C9orf72", "FTD precursor" and "hereditary motor neuropathy / juvenile SMA" (its key_features cite UMN signs she does not have).
  - Key evidence (replace C14 set): thyrotoxicosis as a reversible cause of weakness and fasciculations; simple vs complex fasciculations and the EMG criteria for LMN involvement; carrier status is risk, not diagnosis (Gold Coast not met); C9orf72 penetrance is age-dependent and incomplete, so counselling matters; predictive testing of minors deferred.

### ALS-P03 (man, 48, presumed MMN on monthly IVIG; R1 needs_changes)
- Notes: 5ae3cc00-ba7c-4f43-8baa-755644c9222f C1, C2; 5132b5f5-5889-43a2-a721-6054ea88992f C2, C1 (EMG with conduction-block assessment first); 36d1f205-80dd-4342-8629-68d890a4c349 C8 (MMN low); 82664160-0b6a-43db-9470-d913dced4be4 C10 (IVIG); 85ffa448-a614-4ff5-9fb6-b6475417e7c2 C1, C3; 6a7a419f-e0f0-438d-87af-60bdf74b1e4c C1, C4; 9c473821-f7fa-4586-b632-80ce21e171e1 C3; dc29ac03-4453-4ec2-8c8b-559856dc67e9 C1, C8.
- Survey: criterion asks `anti_GM1_IgM` (C13 spelling); labs report repeat anti-GM1 negative (<1:100); red herring says "Low-titer anti-GM1 (1:100)" at the labs (C11); differential lists "ALS with coincidental low-titer anti-GM1" very_high (target in differential); CSF criterion `[]`; Resp FVC 74, SNIP 58.
- Decisions: lab criterion adds `"anti-GM1 IgM"`; CSF `{}`. Red herring: data_point "Prior low-titer anti-GM1 IgM (1:100) at the original MMN diagnosis", location "HPI", field_path `patient.history_present_illness`, correct_interpretation "A low titre is non-specific; the repeat is negative and the NCS show no conduction block." Musts add: "Stop the monthly IVIG: there is no conduction block or other evidence of an immune motor neuropathy, and IVIG has no role in ALS." Prohibition replaces PROHIB-IMM: "Do not continue IVIG or start other immunotherapy as treatment for ALS." Resp = reduced. Bulbar = signs without dysphagia (tongue atrophy, reduced palatal elevation). Differential: delete the target entry and the "lower motor neuron-predominant ALS variant" entry (an ALS phenotype); MMN low (UMN signs, bulbar involvement, progression despite IVIG, repeat anti-GM1 negative, no block); inflammatory myopathy low; hereditary motor neuropathy very_low.

### ALS-P04 (man, 56, flail-arm phenotype; R1 needs_changes)
- Notes: 959fb8c4-81e1-4e44-9344-a79599881d67 C1, C2; 039f6452-f616-4742-a272-0a5128b5d6bd C2 (flail-arm literature deleted; phenotype named in key evidence); a04ceac5-9896-4629-adf7-746ba554eafb C8 (MMN low); 3b7649bf-37e6-4f4d-8428-6c4833a9bbd0 C9; eac9df83-0f72-4205-a644-e0312d1ef61a C1, C3; bc7959ee-02bf-49de-b4ff-ec615f25f5c7 C1, C4; c1e85ca9-5d63-450d-ab12-85b0d936e3a2 C3; b65f7002-dcc1-411e-887b-9ff8cefaeb7c C1, C5; b67bcf6e-7587-421b-8df5-9cf8163a7c2f C1, C8, C9.
- Survey: CK 6.4x; "Mimic exclusion" panel with TSH duplicated; criterion adds androgen receptor CAG repeat (Kennedy question in a man with arm-predominant LMN signs: keep); spine content in the brain report, same impression in both; spondylosis; Resp FVC 78, SNIP 68 (men).
- Decisions: lab criterion adds `"androgen receptor CAG repeat"`. Resp = reduced. Bulbar = none. PROHIB-SURG cervical. Patient block: past medical history names the phenotype ("Flail arm syndrome ... noted 12 months ago"): reword to "Bilateral arm weakness and wasting noted 12 months ago, initially attributed to bilateral rotator cuff pathology" (C11). Differential: MMN low; brachial amyotrophy / Hirayama disease very_low (age, bilateral, UMN signs, MRI); cervical radiculopathy low; IBM low; CIDP low; add Kennedy disease very_low (the labs test the CAG repeat, which is normal; UMN signs). Key evidence names the flail-arm (brachial amyotrophic diplegia) phenotype and its slower course without numbers that the case does not support.

### ALS-P05 (woman, 46, HIV on bictegravir/emtricitabine/TAF, suppressed; R1 needs_changes)
- Notes: a22b4336-665b-4e6e-b946-e29d0a559e9b C1 (CSF and HIV tests acceptable as targeted mimic exclusion); 783c430e-8ad7-42fa-bb4a-99e0ae4b999d C1, C3; dfaf2518-daab-4389-83d7-217ce7b41a31 C15 (HIV as confounder); 7e2fad0b-5b8d-4135-b383-ed05af0041f4 C8 (HIV motor neuronopathy low); 0ca4443e-beb3-4120-a560-8a04cd9e40e4 C2, C13 (HIV viral load and CD4 reported in the labs); 1b1dcc51-9d21-4a84-a669-ceb71d93c945 C1, C4; cc45e126-5d7e-4289-a71a-e9dffe3445f5 C3; a2fa5560-e498-400a-bce2-2ebd8dbf08a6 C1.
- Survey: HPI leaks the spine MRI result and reasoning (C11); "Mimic exclusion" panel with TSH as a string; HIV panel shows viral load undetectable but no CD4; CSF HIV RNA; cord content in the brain report; same impression in both; non-contrast spine claims enhancement findings; Resp normal (FVC 82, SNIP 71).
- Decisions: lab criterion adds `HIV`; "HIV" panel reports plasma HIV-1 RNA (undetectable) and CD4 count (numeric, normal, consistent with the history). Brain MRI with gadolinium (lymphoma, toxoplasmosis, PML question). Resp = normal. Bulbar = none. Add a must: "Continue the current antiretroviral regimen and share the diagnosis with the HIV team." Differential: HIV-associated motor neuronopathy low; vacuolar myelopathy very_low; PML and CNS lymphoma very_low.

### ALS-P06 (man, 53, IgM kappa MGUS; R1 needs_changes)
- Notes: 5c89246b-87bf-4f24-a00c-29be0629f99a C1, C2; 59b49bd2-7c68-4e1d-bd79-d935921b0faf C2; e6f29c98-29bf-4091-a96a-94a54b89e5f6 C8 (MGUS neuropathy low); 69cfac89-8f57-4bd5-ad99-d1684a82f666 C11, C13 (anti-MAG reported negative in the labs, "pending" sentence deleted); bdc518b8-679f-454d-8f57-6a55af80c4dd C1, C3; 72b81b92-5b22-4fa9-9bf2-0f633603a5ed C4 (borderline wording); f378b998-dfcb-4d06-a109-5cd3914f8055 C3; e1da1f92-fbbf-45c4-b8b6-867da83a4544 C1.
- Survey: lab row "TSH (POEMS endocrinopathy)" renamed "TSH"; no CBC or CMP; cord content in the brain report; same impression in both; CSF dict dumps; Resp FVC 80, SNIP 70 (men).
- Decisions: lab criterion adds `SPEP`, `IFE`, `serum_free_light_chains`, `anti_MAG`; labs report anti-MAG negative. Resp = borderline. Bulbar = none. Add a must: "Continue haematology surveillance of the IgM MGUS; it does not explain the motor syndrome." Differential: MGUS-associated (anti-MAG) neuropathy low; POEMS very_low (no polyneuropathy, kappa light chain); Waldenstrom-related neuropathy very_low; MMN low.

### ALS-P07 (woman, 61, childhood poliomyelitis; R1 needs_changes)
- Notes: 1138cdf4-aac3-47e3-a816-394f28b496bd C1, C2; bb7e1af1-6266-447b-bf14-3d635136fd5f C2 (EMG compares new findings with the polio distribution: expected_evidence names new denervation outside the polio-affected limb); 6e3e812d-59a1-429b-bde4-4469864fa78d C8 (PPS alone low); eb171932-ffd7-4d83-948f-2d56c07ef471 C12 (cauda equina wording); 83e32792-5000-491c-9a9f-d05801feee44 C1, C3; aaf06f54-0c97-4659-924a-c0b89f8b1e9d C1, C4; a9be1de4-3f9e-4863-8c69-5c0e5123bbc7 C3 (note sits on the literature step: AMX0035 removed from every output); 827a1fee-11ff-4d2d-b00e-78a55c3ab5ba C1, C5; 03220c38-efa5-4017-82f7-5e2b0db68e59 C1, C12.
- Survey: EMG lacks motor NCS (C6); spine impression numbering starts at "2."; Resp FVC 72, SNIP 52 (women).
- Decisions: Resp = reduced. Bulbar = signs without dysphagia (new tongue atrophy). Differential: post-polio syndrome alone low (new bulbar and UMN signs, denervation outside the polio distribution, rapid progression); plexopathy, IBM, cervical myelopathy, MMN low with key_features from the case.

### ALS-P08 (man, 45, retired elite swimmer, paternal uncle died of ALS, SOD1 A4V; R1 needs_changes)
- Notes: c15f3a46-9f5f-4bd2-a4ac-31457c8f77f1 C7 (relabel); 38d2fb67-30c3-4d31-af3d-e4080a890549 C1, C2; 5db6492b-4d77-49d0-84ab-6ca97ebcc23c C3, C10 (tofersen check deleted); 2e11ab82-94e5-47df-9209-63b79c592f5c C7, C10 (repeat EMG in 6-8 weeks); 41f0232d-0688-4547-8da3-1dbda7fecc74 C7, C14 (UMN evidence equivocal: key evidence and differential say so); 73e83884-ca8b-4a40-82b8-9c3c0d0b7e47 C10 (cascade counselling of his first-degree relatives); d469d924-1774-4629-8a0e-d0814638440c C7, C10 (musts below); abedfbbf-c714-40fd-9796-c251721aedb3 C4 (respiratory optional baseline); af695bda-96d6-42e7-8257-cf5b24d9b34f C3; 3fcc8e64-533c-4ea1-9d8b-b287dfd01ea9 C7.
- Survey: EMG complex fasciculations in two regions, no definite fibrillations, "repeat in 6-8 weeks"; no UMN signs (reflexes 3+ from 2+, plantars flexor); differential keeps "familial ALS non-SOD1" high after SOD1 positive; Kennedy entry cites an untested CAG repeat; Resp normal (FVC 92, SNIP 88).
- Decisions:
  - Label: `accepted[0]` = "Suspected early ALS in a SOD1 A4V pathogenic-variant carrier, Gold Coast criteria not yet met"; keep `icd_codes[0]` G12.21 (CENTRAL lists the label change; open question Q2).
  - Criteria: EMG, brain MRI, spine MRI, labs required; respiratory optional; genetics recommended; DI deleted with its follow-up. Sequence constraint 1 only.
  - Musts: (1) "Explain that the SOD1 A4V variant is pathogenic and that ALS is suspected but not established, and arrange post-test genetic counselling." (2) "Offer counselling to his first-degree relatives, each of whom has a 50% chance of carrying the variant, with predictive testing only after counselling." (3) "Record an objective neurological baseline (MRC grades in named muscles, reflexes, ALSFRS-R), interpreted against his athletic baseline." (4) "Complete brain and spine MRI and the blood tests for mimic exclusion before any ALS-specific treatment decision." (5) "Repeat EMG/NCS in 6 to 8 weeks with clinical review, looking for active denervation, spread and definite upper motor neuron signs." (6) "Refer to a specialist ALS centre now so that tofersen can be discussed as soon as ALS is established, and trials for SOD1 carriers considered."
  - Prohibitions: "Do not start riluzole or tofersen before ALS is established clinically and electrodiagnostically."; "Do not attribute the symptoms to detraining or anxiety without the repeat EMG and review."
  - Differential: delete "Familial ALS, non-SOD1" and "Sporadic ALS with coincidental family history" (the SOD1 result settles the genotype); add "Benign fasciculations with detraining atrophy in a former athlete" moderate; hereditary spastic paraparesis with motor neuron involvement low; Kennedy disease very_low with C8 wording; distal hereditary motor neuropathy very_low.
  - Key evidence: SOD1 A4V is an aggressive variant; carrier status does not establish ALS; UMN evidence is currently equivocal (relative hyperreflexia, flexor plantars); serial EMG and examination decide; tofersen only once ALS is established, by a specialist centre.

### ALS-P09 (man, 67, established bvFTD, father with possible FTD/ALS, C9orf72 expansion; R1 needs_changes)
- Notes: f29aca3a-db40-4bc8-8a12-75b1a4a3ba36 C1, C2; 9e59c630-20e4-45d0-8b43-80f5edb052e3 C2; be2f32e2-98df-4506-a4e7-eb3e91e4a7d9 C10 (swallowing must); f4d90fdc-0d8e-4b32-934a-df2aef81e024 C10 (capacity and caregiver must); 63064137-c9ed-4736-90d2-d8d7c855da82 C1, C3; 50cff411-3df1-49fe-a927-d887c4b6125b C1, C4; 256e78eb-adf7-42ab-b3f6-f49c2a865cc5 C8 (isolated bvFTD low); 75e4abdc-8e8d-49e8-9e78-f8756613a2f9 C3; ea2c5a1d-2c98-496b-9d9c-92aebde6b38e C10.
- Survey: EMG lacks motor NCS (C6); DI calls riluzole serotonergic and QTc-prolonging (C3); choking episodes; Resp FVC 70, SNIP 48.
- Decisions: genetics recommended. Resp = reduced. Bulbar = dysphagia. Musts add: "Assess decision-making capacity for each major decision (riluzole, genetic testing, NIV, gastrostomy), involve his wife as caregiver, and plan advance decisions early while he can contribute." and "Offer genetic counselling to his first-degree relatives about the C9orf72 expansion (ALS and frontotemporal dementia risk)." Case medicine must (oral suspension). Differential: isolated bvFTD with coincidental motor decline low; delete entries that are the target phenotype.

### ALS-RM11 (man, 64, retired mechanic, cervical spondylosis; R1 needs_changes)
- Notes: 0e1a7582-3e73-49c7-8eda-ec7d5d37cfd7 C11 (delete "EMG is scheduled." and the CK and MRI results from the HPI; the EMG result belongs to the work-up); 05603637-ba9e-428a-a591-ab61b2526ecc C1; c2bde008-f975-448f-a471-5c4ba546632e C8 (CSM low); 67ade2c9-94fd-47c0-b9bf-323117e7e88a C1, C3; d979b5dc-a8b9-4e96-963a-eefb72e2ebdd C1, C4; 9b390d90-e4e5-43ff-a511-4da5fc8b0dc4 C3; de4d37e7-f08e-41ce-8b81-d78b878da744 C1, C5; f71232f0-869a-4af9-ba55-952a5199d88d C1, C11.
- Survey: red-herring field_path points to `mri` (C12); spine numbering starts at "2."; exam `additional` synthesis; Kennedy entry cites an untested CAG repeat; no dysphagia ("no dysphagia yet"), tongue fasciculations; Resp FVC 76, SNIP 60.
- Decisions: Resp = reduced. Bulbar = signs without dysphagia (mild palatal weakness; "no dysphagia yet"). PROHIB-SURG cervical. Differential: cervical spondylotic myelopathy low (does not explain tongue fasciculations, bulbar, thoracic and lumbosacral denervation with normal sensory studies); Kennedy disease very_low (C8 wording); MMN low.

### ALS-RS11 (man, 60, bulbar and limb; R1 needs_changes)
- Notes: 9623c8f0-2b2e-4bdb-840c-5c71238991f7 C1; b2f269e0-c43e-43bb-84e0-5e86610d0fe5 C1, C3; f47e4e04-fcc5-47fc-a7f5-f8e7a7610a37 C4, C10 (respiratory referral and NIV now); 60e02483-4c45-496b-ae8b-78eee133af2e C10 (speech and swallowing must); 3f2fafd2-3f8e-4db8-baaa-c322b25ba9be C9; dda6c14d-0a00-4867-a391-af5ee87c5904 C3; 10f5015a-8f6e-4140-9f4f-18607f998cd8 C1, C5; d76bd1fb-a16c-4b3b-91da-903729a617eb C1.
- Survey: CK 7.1x; Resp FVC 64, SNIP 38; dysarthria, tongue atrophy, reduced palatal elevation, no reported dysphagia.
- Decisions: Resp = reduced with AAN marker (SNIP 38 cmH2O). Bulbar = signs without dysphagia (note asks aspiration-risk monitoring: use the signs variant and add "and monitor for aspiration"). Differential: Kennedy very_low (C8 wording); MMN low.

### ALS-S01 (man, 58, on atorvastatin; R1 needs_changes)
- Notes: 2f8554cc-e73a-4b67-bb1b-79654ca218f9 C1; 6c4e6bd6-0841-4774-a9d3-913a918b1ded C1, C3; cba80908-ce68-45d4-a85a-3910319e8ca9 C9 (statin context); 4d83e271-9b37-4f1e-af28-21d924b84d6f C1, C4; 12755d6e-6f26-418b-bbd6-75f34a5e5f19 C3; 2fab0386-647b-491c-a53c-1b6522a941a0 C1, C5; cebdf45d-ca48-4810-bd83-0437e64de918 C1.
- Survey: CK 5.3x; labs lack CBC and CMP; Kennedy entry cites an untested CAG repeat; Resp normal (FVC 82, SNIP 74).
- Decisions: Resp = normal. Bulbar = signs without dysphagia (bilateral tongue atrophy). Differential: statin-associated myopathy low (add: CK 5.3x on atorvastatin, against neurogenic EMG and UMN signs); Kennedy very_low; MMN low.

### ALS-S02 (woman, 62, bulbar onset, levothyroxine, alendronate; R1 needs_changes)
- Notes: 94252428-71a6-4cfd-9188-9cb6d74f0d43 C1; 4fdb755c-8cdf-4385-8724-946b70e91ae8 C1, C3 (levothyroxine not CYP1A2); 3073e9a1-a2e1-4cc9-a582-f85063743afd C4, C10; de40b53e-4a47-48e3-9aa9-c0ab8b3a5b00 C5 (full panel); ec0eb223-b51f-436d-b5ae-2f7a83b2448a C8 (PBP is a phenotype); 5609768e-5365-4b6c-a1bd-e0da827b2696 C3; 5e7f8b26-12a3-4f83-98b3-460f46856723 C1.
- Survey: C9-only genetics; choking with thin liquids; Resp FVC 68, SNIP 42.
- Decisions: Resp = reduced. Bulbar = dysphagia. Case medicine must (alendronate). Differential: delete the PBP entry; others per C8.

### ALS-S03 (man, 55; R1 needs_changes)
- Notes: 97ae7f3b-16ad-4ecf-b94f-6eb7e46702dd C1; dcd17b55-4f67-442a-9334-b2ac7d5d1818 C6 (state no conduction block); be205e95-71b1-4415-b0a3-55a8066a12fa C1, C3; 1a295b03-b3a4-4d69-8903-f8991e1c95f6 C3 (initial "general" block deleted; one consistent riluzole output); c6663c68-f289-45ac-8e0a-fe821c516625 C1, C4; 140104fe-d7c1-4430-b740-79535a641633 C5; 606775a0-7d41-4db9-9f22-2379797cf15c C1.
- Survey: C9-only genetics; Kennedy entry cites an untested CAG repeat; Resp normal (FVC 84, SNIP 76).
- Decisions: Resp = normal. Bulbar = signs without dysphagia (bilateral tongue atrophy). Differential: Kennedy very_low; MMN low.

### ALS-S04 (woman, 70, bulbar and limb, no dysphagia documented; R1 needs_changes)
- Notes: 9f81aef5-a257-4bf1-ae15-5de78168d7b5 C1; 01ec92d7-5996-4119-93b6-0017b98cae94 C6 (motor NCS); 99db8ba8-61a6-4113-8220-6b129ca397d4 C1, C3; 7cf92fbd-8fa0-4b0e-8961-0797795fef40 C4, C10; 35534ccc-a1e1-4626-8ca0-31f6c4269f7b C10 (no dysphagia in the history: use the bulbar-signs must "bulbar symptoms requiring swallowing-risk assessment"; do not add dysphagia to the history); 56bf56d7-d683-4602-a09e-a35b26f7e978 C5; 3412b2ae-fd64-41ef-b935-aa45aab0ba14 C8 (PBP phenotype); 4d9b6abe-1d63-4de3-afc8-b60301f17a6a C1, C6, C10.
- Survey: C9-only genetics; exam `additional` synthesis; Resp FVC 70, SNIP 46.
- Decisions: Resp = reduced. Bulbar = signs without dysphagia. No PROHIB-SWALLOW. Differential: delete the PBP entry.

### ALS-S05 (man, 53, no medicines; R1 needs_changes)
- Notes: b0f4ba1d-9b74-43bc-94cb-da220f6a608f C1; 008369f3-aa8d-432e-95d9-d558c738ef80 C6 (motor NCS with CMAP, velocities, no block); 9cc1c53f-4d21-4e6f-8f48-1b67c55ab497 C1, C3; c26321cf-5650-4c79-a459-f89776ef4bbe C3 (initial "general" block deleted); 8681a0e0-7baa-40a8-a926-512d776a671f C1, C4; a147095c-563e-465c-b003-f599222637d3 C5; 0864c29f-0820-4fea-a408-1e3702d762fb C3; d44d11a1-5727-420b-b621-64d0c07f426f C1, C6.
- Survey: C9-only genetics; Resp normal (FVC 88, SNIP 80).
- Decisions: Resp = normal. Bulbar = none. DI output: no current medicines; generic content only.

### ALS-S06 (man, 67, type 2 diabetes on metformin; R1 needs_changes)
- Notes: dc71d342-4c33-44ec-8bb8-47eeadff8848 C1; 1aeafbd1-dcbe-498c-b433-7db37d478383 C8 (diabetic amyotrophy low); 5c698397-3606-4914-b00a-18a1f7c69696 C14 (reduced-sural pearl variant); 5c9f1969-1afa-4619-90c1-d117121985a2 C1, C3 (metformin: no interaction; LFTs are for riluzole); bc8ef2aa-46ff-4856-a219-6fc09001522b C4, C10; 86d87968-f7ad-4329-acb9-2ef1225bd95d C5; e6e83f3d-880d-4262-85ac-39fe125a2c98 C3; e1dc4944-d7fd-4e53-adf6-7b2418cd5d44 C1.
- Survey: "Mimic exclusion" panel with TSH as a string; mild distal sensory loss; sural mildly reduced; C9-only genetics; dysarthria mild; Resp FVC 78, SNIP 62.
- Decisions: Resp = reduced. Bulbar = signs without dysphagia. Differential: diabetic lumbosacral radiculoplexus neuropathy (amyotrophy) low; diabetic length-dependent neuropathy as a coexisting condition (not an alternative): say so in key evidence.

### ALS-S07 (woman, 50, anxiety disorder on escitalopram; R1 needs_changes)
- Notes: c6e254ac-760f-4ca3-a01a-c68755b41a37 C1; fe18f6ef-828e-484f-bfba-068c63ac158f C6; 7949f4b4-0594-4e58-89b8-e2681078e02d C1, C3 (riluzole not serotonergic); c66738c7-1f13-4a53-8173-a2e041e3670d C15 (anxiety red herring added); 1335871c-a9dc-4803-b97e-6bb95abd175b C1, C4; 3234e797-519b-42fd-8f72-700313f01092 C5; 0ef6c4bc-ba44-47ae-95c6-8043706657f7 C8 (familial ALS: move to low; complete panel negative); 4e7e33b6-2034-463e-81d3-c799f8c7c835 C3; 2666c318-b24e-43a3-a6cf-cae6fe2a993f C1, C3, C5, C6.
- Survey: EMG lacks motor NCS; C9-only genetics; tofersen sentence in a pearl (delete); genetic must present; Resp normal (FVC 90, SNIP 82).
- Decisions: genetics optional (no family history; young-ish onset is mentioned in the rationale as a reason to offer it). Resp = normal. Bulbar = none. PROHIB-FUNC kept. Differential: familial ALS low (no family history; full panel negative).

### ALS-S08 (man, 58, warfarin and atorvastatin; R1 needs_changes)
- Notes: 553b128b-525a-47e3-8c7c-a25bd14b20f6 C1; d91f9116-520b-4938-be51-4e67baa7aea5 C12 (motor-cortex finding moved to the brain report); 8c1a9e6d-942f-4f92-8732-bd43a906bb22 C1, C3 (INR monitoring, no CYP1A2 claim); 1466a4e8-45bf-4ebc-82e9-f7941e9f8153 C3; 18b94541-6b04-47b5-bf6d-7b3c41d7409f C9, C14; 8e1531cb-44a9-46f4-8c15-e38068eb698a C1, C4; 7bc08482-8baf-4871-8ef7-876e2bbdbbfa C5 (panel already complete: add TBK1 if missing; optional and after diagnosis); 29717cf6-fbe1-4f9e-8933-8727148963f3 C1, C12.
- Survey: CK 5.3x; Relyvrio named; Kennedy entry cites an untested CAG repeat; Resp normal (FVC 82, SNIP 74).
- Decisions: Resp = normal. Bulbar = none. Case medicine must (INR). Differential: statin myopathy low (add if missing); Kennedy very_low.

### ALS-S09 (woman, 64, professional singer, bulbar onset, levothyroxine and omeprazole; R1 needs_changes)
- Notes: bf54e165-59c0-4534-b21d-e982d0655ee6 C1; c925df65-e437-4ed5-bb53-ca473069944f C4, C10; 1dc3dd2e-5b3b-4bc0-b7c2-5052d9d1e64c C10 (swallowing must visible early); 8b821a0b-6345-4993-b543-f545741db394 C1, C3; 8ad9e0ff-42cd-40a9-aee1-9e93fb54d084 C8 (PBP phenotype); e37b6b6b-f2e3-4708-bf10-ac353c41983b C5 (full panel); 3a038a83-299d-4a52-ae2b-543144a91259 C3; 7d6955d4-b5cf-4a9f-bbfd-98195994dfaa C1, C10.
- Survey: coughing with thin liquids; Resp FVC 76, SNIP 54, NIF -48; omeprazole is a real CYP1A2 inducer.
- Decisions: Resp = reduced with AAN marker (NIF -48 cmH2O). Bulbar = dysphagia (coughing on thin liquids). Add to MUST-BULBAR: "with voice and communication support given her profession". Differential: delete the PBP entry.

### ALS-S10 (man, 47, father died of ALS, C9orf72 expansion; R1 needs_changes)
- Notes: 7b72cef4-5247-4c46-b77e-af86e1c73811 C1, C2; 3d89340e-2c98-4de6-b4d2-0e11504fcb83 C2, C10 (genetic counselling becomes musts); cd0a30d7-2946-40b6-af42-51b501f1e347 C8 (sporadic ALS removed or very_low); 7b9a0161-19d9-4225-8a2b-bfcd0a6c1eae C8 (SOD1/TARDBP/FUS familial ALS very_low after negative results); f1998fc1-d800-438b-8e19-0e2419983c7f C1, C3 (caffeine claim removed); ce3bced0-9018-4b36-a8c4-9fcc21f5837e C3 (AMX0035 and trial enrolment removed); 4c973d17-6bcd-4659-b1c7-7dd017a051bf C9; 7e057d60-892c-4a89-9476-11dc5ac4e0b7 C1, C4; 4cd32c3e-4c48-4d34-9ac3-09de33eae298 C10; 09bdd00d-51f7-45a4-9a68-1060d7f38aa4 C1.
- Survey: initial "general" DI block; CK 7.1x; positive genetic impression in "Abnormal values" format; exam `additional` synthesis; Kennedy entry cites an untested CAG repeat; no bulbar symptoms ("no dysphagia, dysarthria"); Resp normal (FVC 91, SNIP 86).
- Decisions: genetics recommended. Resp = normal. Bulbar = none. Musts replace MUST-GEN with: "Provide post-test genetic counselling about the C9orf72 expansion, including the frontotemporal dementia risk." ; "Offer counselling to his first-degree relatives, each of whom has a 50% chance of carrying the expansion, with predictive testing only after counselling." ; "Perform baseline cognitive and behavioural screening (for example ECAS) because of the C9orf72-associated frontotemporal dementia risk." ; "Discuss eligibility for C9orf72-targeted clinical trials at the specialist centre." Differential: sporadic ALS with coincidental family history deleted (the diagnosis is C9orf72-associated familial ALS); other familial genotypes very_low; Kennedy very_low.

### ALS-S11 (man, 72, low-risk prostate cancer on active surveillance, right foot drop; R1 needs_changes)
- Notes: b8d3cf2b-8578-4e9d-836f-573a99f3ad13 C1; b1d11959-748b-450e-90f6-4b84a6554ca0 C12 (lumbar findings moved to the spine report); ad563de2-8dcb-4d59-a6a8-716bde92e819 C12 (non-contrast spine: enhancement phrase removed); 3403f58a-341b-41de-8ccb-be549826142e C8 (paraneoplastic low; the "panel negative" claim removed, no panel added); 5d1141b1-9051-4d06-bc23-4b494622e2b6 C4, C10; 5e8eb882-00ca-4ece-b99e-824074848006 C1, C3; 9a2859dd-6e23-4489-bb39-3465b5ba6df9 C5; 74bcf306-63f8-41c1-be26-4d7ef1cdb561 C3; 30c54a7e-3dc1-47b8-a944-f40bdc8aca65 C1, C4, C8, C12.
- Survey: spine region must include lumbosacral; Resp FVC 80, SNIP 68, NIF -52; ALT and ALP inside "Neuromuscular_Panel".
- Decisions: Resp = reduced with AAN marker (NIF -52 cmH2O). Bulbar = none. PROHIB-SURG lumbar (L4-L5 and L5-S1 foraminal and facet changes; right foot drop is not an L5 radiculopathy when UMN signs and multi-region denervation are present). Differential: paraneoplastic motor neuronopathy low (Gleason 6 on active surveillance, stable PSA, no metastasis on spine imaging, classic EMG; no paraneoplastic panel was done, so do not claim one); lumbar radiculopathy / cauda equina low; delete "Diabetic amyotrophy" (he has no diabetes); MMN low; IBM very_low.

---

## 5. CENTRAL requests (outside the case files)

1. **Review UI**: show `initial_tool_outputs` and `followup_outputs` together in criterion order, so
   that the core work-up (EMG, MRI, spine MRI, labs) reads as Steps 1-4. Every ALS pathway note
   (79) depends on it for the display.
2. **Criteria pack `dataset-generation/criteria_packs/ALS.md`**: section 6 makes respiratory function
   required in S and P cases, which the reviewers overruled (staging, recommended); the required
   literature search is gone; genetic testing is offered to everyone with counselling (2023
   consensus) but stays optional in the work-up unless familial; add the citation keys
   `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]`,
   `[Bourke_2006]` to section 8.
3. **Diagnosis synonyms**:
   - P02: `icd_codes[0]` becomes E05.90. Strip the appended G12.21 labels ("amyotrophic lateral
     sclerosis", "ALS", "motor neuron disease", "motor neurone disease", "MND") and codes (G12.2,
     G12.20, G12.23, G12.24, G12.25) from ALS-P02, which `apply_diagnosis_synonyms.py` cannot remove
     (it only adds); add an E05.90 entry restricted to `conditions: [als]` if wanted (labels such as
     "thyrotoxicosis", "levothyroxine over-replacement"); decide whether an answer of "ALS" with a
     thyrotoxicosis mention should match (open question Q1).
   - P01 and P08: labels changed under G12.21, no synonym change needed.
4. **Lab vocabulary and matching**: `_contains_required` compares assay names with `_fold` only, while
   tool validation accepts any `normalize_analyte` spelling. Make criterion matching use
   `normalize_analyte` (and the `_ANALYTE_SYNONYMS`) for assay lists, so `paraneoplastic` and
   `paraneoplastic_panel`, `LFT` and `LFTs`, or `CMP` against `BMP` plus `LFTs`, compare equal. Until
   then the ALS lab criteria use the minimal core of C13 and one alternative per synonym. Add plasma
   `HIV_viral_load` and `CD4_count` to `interpret_labs` (P05 reports them inside the "HIV" panel).
5. **MockServer**: the initial `literature_search` and `drug_interactions` blocks are served for any
   query or drug, so a case-specific literature output leaked to every search. This round removes them
   in ALS; a central guard (or a test) that a stored literature output never contains a criterion's
   `expected_evidence` would stop it recurring.
6. **Fallback library**: no ALS change requested (literature now comes from the library's general
   output; check that it does not cite El Escorial as current or name AMX0035).
7. **Test**: a test that no ALS case mentions AMX0035/Relyvrio, grapefruit as a CYP1A2 modulator, or
   "July 2026 review" would keep the class closed.

---

## 6. Open questions for Andrea

- **Q1. P02 label.** Reviewer 1 ruled that P02 is not ALS. The plan relabels it inside condition `als`
  as "Thyrotoxicosis from levothyroxine over-replacement in a C9orf72 repeat-expansion carrier, ALS
  criteria not met" with E05.90. Alternatives: keep it as a deliberate "ALS mimic" case with a
  non-ALS ground truth (as planned), or move it to another condition. Also: should an agent answer
  containing both "ALS" and "thyrotoxicosis" count as correct?
- **Q2. P08 label.** Kept under G12.21 as "Suspected early ALS in a SOD1 A4V pathogenic-variant
  carrier, Gold Coast criteria not yet met". An alternative is a carrier code (for example Z15.89 in
  ICD-10-CM) with ALS as a differential, which would make "ALS" a wrong answer.
- **Q3. Literature criterion.** The plan removes it in all 30 (ruling 5 allows removal; the exact
  query match made the optional version meaningless). Confirm, or prefer an optional criterion with
  no required query.
- **Q4. MIP/NIF convention.** The dataset uses -60 cmH2O as the lower limit for both sexes and all
  ages; published normal values are sex- and age-dependent and usually stronger. Accept -60 as a
  dataset convention (it is the AAN 2009 NIV marker), or set sex-specific limits?
- **Q5. Core studies in the initial work-up.** The plan keeps EMG, MRI, spine MRI and labs in
  `initial_tool_outputs` and relies on the central UI fix for the display. EMG and spine MRI could be
  moved to follow-ups (they have discriminators); brain MRI and labs cannot be matched robustly that
  way. Keep as planned?
- **Q6. Drug interaction tier.** Required only in M06 (methotrexate). M04 (tamoxifen) and M03
  (nightly alcohol) are kept recommended. Agree?
- **Q7. Genetic panel tier.** Optional in sporadic cases (reviewer wording), recommended in the four
  familial cases, although the 2023 consensus offers testing to everyone. Agree?
- **Q8. CSF as waste.** CSF is not routine in typical ALS. Should the 25 cases without a CSF
  indication get `analyze_csf` as a waste avoided action (not done this round)?
- **Q9. P01 riluzole timing.** Gold Coast is met at presentation (UMN signs and active plus chronic
  denervation in the cervical region), but the reviewer asked for caution, so the plan defers
  riluzole to confirmation at the 3-month review and makes the interaction check optional. Agree?
