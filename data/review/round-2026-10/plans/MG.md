# MG: condition plan for the October 2026 review round

Lead plan for the 30 `myasthenia_gravis` cases: M01..M04, P01..P04, RM11..RM16, RP11..RP14,
RS11..RS17, S01..S05. Read `ROUND_POLICY.md`, `PATTERNS.md`, `TOOL_REPORT_STYLE_GUIDE.md` and
`docs/benchmark/tool-contract.md` first; this plan does not repeat them.

There are no reviewer notes for MG (`notes/MG.md` and `notes/MG.json` do not exist). The physician
input is the July 2026 tool guidance for `myasthenia_gravis` in
`agent-platform/config/review/condition_tool_guidance.yaml` (Reviewer 2, summarised in 1.3) plus
ROUND_POLICY. Every finding below comes from the lead's survey. Each log has a "Reviewer notes"
section that says "No reviewer notes for this case".

Baseline (24 October 2026, before any edit): `perfect_agent.py` passes 30/30 with two warnings
(P01 action-7 clustered AChR is served by the same report as action-1; RS15 ice pack is served by
the neostigmine follow-up). The leak guard fails 6 cases: M01, M03, RM13, RM15, S01, S03 (the
initial literature output's summary is the `expected_evidence`). 27 cases carry the same
`labs -> RNS` soft constraint whose reason talks about SFEMG. Every stop rule has
`max_additional_actions: 0` and lists the literature and drug-check criteria as required.

Use: apply the classes of section 2 that name your case (canonical text verbatim, `<...>` slots
filled), then the case decisions of section 4; rebuild criteria, follow-up order, constraints and
stop rule per section 3; run
`uv run python data/review/round-2026-10/bin/perfect_agent.py CASE -v`,
`uv run python data/review/round-2026-10/bin/case_io.py check CASE` and
`uv run pytest agent-platform/tests/test_case_guards.py -q -k CASE`; write `logs/{CASE_ID}.md`.
Edit only through `case_io` load/save.

New text: English, American spelling as the cases already use (generalized, anemia, tumor), no em
or en dashes. New values must fit age, sex, weight and medicines, and must differ from the shared
template values (do not paste the same NIF, FVC or titre into five cases).

---

## 1. Governing guidelines and canonical facts

### 1.1 Which source governs what

| question | source | key |
| --- | --- | --- |
| Diagnosis, serology order, neurophysiology, imaging | Jacob S et al., Pract Neurol 2025;25:422-437 (ABN guidance); Evoli A et al., Neurol Sci 2019;40:1111-1124 (Italian recommendations) | `[Jacob_2025]`, `[Evoli_2019]` (CENTRAL; these are the July 2026 guidance sources) |
| Management of MG (steroids, immunosuppression, thymectomy indications, IVIG/PLEX, crisis) | International consensus guidance: Sanders DB et al., Neurology 2016;87:419-425, and its update Narayanaswami P et al., Neurology 2021;96:114-122 | `[Sanders_2016]` (pack), `[Narayanaswami_2021]` (CENTRAL) |
| Thymectomy in non-thymomatous AChR+ generalized MG | MGTX: Wolfe GI et al., N Engl J Med 2016;375:511-522; extension Wolfe GI et al., Lancet Neurol 2019;18:259-268 | `[Wolfe_2016]` (pack), `[Wolfe_2019]` (CENTRAL) |
| MGFA clinical classification | Jaretzki A et al., Neurology 2000;55:16-23 | `[Jaretzki_2000_MGFA]` (pack) |
| Overview, pathophysiology | Gilhus NE, N Engl J Med 2016;375:2570-2581 | `[Gilhus_2016]` (pack) |
| Antibody biomarkers, epidemiology | Punga AR, Maddison P, Heckmann JM, Guptill JT, Evoli A, Lancet Neurol 2022;21:176-188 ("Epidemiology, diagnostics, and biomarkers of autoimmune neuromuscular junction disorders") | `[Punga_2022]` (pack; title wrong in the pack, CENTRAL) |
| LEMS diagnosis and treatment (P02, RM13) | Titulaer MJ, Lang B, Verschuuren JJ, Lancet Neurol 2011;10:1098-1107 | `[Titulaer_2011]` (CENTRAL) |
| LEMS tumour screening | Titulaer MJ et al., Eur J Neurol 2011;18:19-e3 (EFNS paraneoplastic screening: CT thorax, then FDG-PET if negative, repeat every 3-6 months for 2 years) | `[EFNS_paraneoplastic_2011]` (CENTRAL) |
| DELTA-P score (SCLC probability in LEMS) | Titulaer MJ et al., J Clin Oncol 2011;29:902-908 | cite in text |
| RNS increment cut-off for LEMS (60%) | Oh SJ et al., Muscle Nerve 2005;32:515-520 | cite in text |
| Respiratory thresholds (20/30/40) | Lawn ND et al., Arch Neurol 2001;58:893-898 (GBS cohort, applied to neuromuscular respiratory failure) | `[Lawn_2001]` (CENTRAL, same key as the GBS plan) |
| Pathophysiology of antibodies only | Vincent A, Nat Rev Immunol 2002;2:797-804 | `[Vincent_2003]` (pack key; the paper is 2002) |

Pack keys allowed: `[Wolfe_2016]`, `[Sanders_2016]`, `[Jaretzki_2000_MGFA]`, `[Vincent_2003]`,
`[Gilhus_2016]`, `[Punga_2022]`. Rules:

- `[Wolfe_2016]` is cited only for thymectomy. It is wrong on serology, RNS, SFEMG, drug checks,
  avoided EEG/CSF/echo/MRI, respiratory testing and sequence constraints (all present now). Replace
  with `[Jacob_2025]`/`[Evoli_2019]` text citations for diagnostics, `[Sanders_2016]` for
  management, `[Jaretzki_2000_MGFA]` for class.
- One citation per source: delete duplicates such as `"[Wolfe_2016]"` next to `"Wolfe_2016"`.
- Until CENTRAL adds a key, cite the source in the rationale by author, journal and year and leave
  it out of `citations`.

### 1.2 Canonical clinical facts (use these; do not restate them differently)

**Serology**

1. First line is AChR binding antibody by RIA or cell-based assay (CBA), not ELISA. Positive in
   about 85% of generalized and about 50% of ocular MG. MuSK is tested in every AChR-negative case.
   A CBA for clustered AChR, MuSK and LRP4 follows in double-seronegative patients, with a repeat
   at about 6 months if negative. LRP4 antibodies are found in a minority of double-seronegative
   patients (prevalence varies widely between cohorts); never write "1-5%" or any single figure.
2. Units: AChR binding and MuSK in nmol/L; AChR blocking and modulating antibodies in % (never
   nmol/L). Keep one laboratory's reference range per case. Mayo-style: AChR binding <=0.02
   nmol/L, MuSK <=0.02 nmol/L. Other RIA laboratories: AChR binding <0.25 or <0.5 nmol/L. A value
   above the stated range is positive, not "borderline" (M02: 0.6 with <0.5 is positive).
3. Thyroid function (TSH, free T4) is tested in every MG case; thyroid antibodies (anti-TPO, TRAb)
   when thyroid disease is suspected or known.
4. Anti-titin and anti-RyR are thymoma markers in early-onset MG (onset under 50); in late-onset
   MG they are common without thymoma and do not by themselves mandate surgery. They are never a
   required criterion. No paraneoplastic panel in MG (LEMS cases: VGCC and SOX1 only).
5. CK and troponin only with immune checkpoint inhibitor exposure (no MG case has it).

**Neurophysiology**

6. RNS at 2-3 Hz (2-5 Hz acceptable): a decrement above 10% between the 1st and 4th (or 5th)
   response is positive. Test clinically weak muscles, limb warmed to 32-34 C, include a facial
   (nasalis/orbicularis) and the accessory nerve (trapezius); pyridostigmine held for at least
   12 h. Sensitivity about 75% in generalized, under 50% in ocular MG.
7. SFEMG (jitter, blocking) is positive in over 90% of MG but is not specific (abnormal in
   neuropathy, myopathy, MND). It is the study to order when RNS is normal and the diagnosis is
   still open, and in seronegative cases.
8. LEMS: low baseline CMAP amplitudes with a slow-rate decrement and post-exercise (10 s maximal
   contraction) or 20-50 Hz facilitation of at least 60% (Oh 2005; 100% is the classic, less
   sensitive cut-off). A 50 Hz study is painful: prefer brief exercise.
9. Edrophonium (Tensilon) is no longer available in most countries and is not orderable; delete it
   from every report and must. The ice-pack test is only for ptosis (improvement of MRD1 or
   palpebral fissure by at least 2 mm after 2-5 min of ice): never in a case without ptosis.

**Imaging**

10. Mediastinum CT with contrast (or MRI) in every confirmed MG to look for thymoma or thymic
    hyperplasia (Reviewer 2); a chest X-ray does not substitute. Iodinated contrast has rare
    reports of MG worsening: it is still used, with monitoring.
11. Brain and orbit MRI with contrast only after negative serology and negative neurophysiology,
    or when the case raises a central or orbital mimic (P03 MS/PML, RM16 orbitopathy, RS13
    restrictive orbit, RS14 brainstem). Never first line.
12. FDG-PET belongs to the LEMS work-up (CT negative or equivocal, or staging of a known tumour). In
    MG it is not indicated; `order_advanced_imaging` in MG is MRA/CTA only.
13. CSF has no role in MG (Reviewer 2: no MG case orders CSF); only for a Miller Fisher or CNS
    alternative the case raises.

**Respiratory staging (aligned with the GBS plan, class C1 there)**

14. `respiratory_function` reports FVC in L, % predicted and mL/kg (weight and height must be in
    `physical_exam["general"]` as "Weight <kg> kg, height <cm> cm", matching any BMI), MIP (NIF)
    and MEP in cmH2O, single-breath count if done, cough strength and the trend when repeated.
    Values below the predicted range are flagged L and never called "within normal limits" or
    "adequate". A MIP of -38 cmH2O is reduced (normal is more negative than about -60 to -80).
15. ICU-level monitoring or intubation planning if any: FVC <20 mL/kg (15 mL/kg the classic
    intubation level), MIP weaker than -30 cmH2O, MEP <40 cmH2O, a fall in VC of more than 30%,
    bulbar weakness with a weak cough or pooled secretions, hypercapnia or distress (the 20/30/40
    rule, Lawn 2001). Oxygen saturation and the ABG are late markers.
16. When `respiratory_function` is a criterion, the patient block must not contain spirometry,
    NIF or MEP numbers (current leak in 19 cases). Bedside observations (counts to 18 in one
    breath, weak cough) may stay only if they are not the scored result.

**Management (musts and prohibitions; never tool calls)**

17. Pyridostigmine 30-60 mg 3-5 times daily titrated to effect (max about 360-480 mg/day).
    Cholinergic crisis is unlikely at usual doses (240 mg/day or less); muscarinic signs
    (sweating, salivation, diarrhoea, bradycardia, miosis) point to it.
18. Steroids: in an outpatient start low and titrate (prednisone 10-20 mg/day, increasing by 5-10
    mg every 3-7 days) or give high dose only under inpatient monitoring, because high-dose
    initiation can transiently worsen MG within 1-2 weeks. Pyridostigmine does not prevent this.
    Steroid-sparing agent (azathioprine first line; mycophenolate, methotrexate alternatives) when
    steroids are needed long term. TPMT (or NUDT15) activity before azathioprine.
19. Pregnancy: azathioprine and prednisone are acceptable; mycophenolate and methotrexate are
    teratogenic and need contraception and a washout before conception. Pyridostigmine is
    compatible with pregnancy. IV magnesium for pre-eclampsia is contraindicated in MG. Combined
    oral contraceptives have no clinically important interaction with pyridostigmine; prednisone
    exposure is increased by ethinylestradiol (not the reverse).
20. Thymectomy: indicated for any thymoma (regardless of MG severity) and, per MGTX, for
    non-thymomatous AChR+ generalized MG aged 18-65 (benefit to 5 years in the extension). Not
    routine in MuSK, LRP4 or ocular MG outside trials. Pre-operative IVIG or PLEX only when bulbar
    or respiratory weakness is significant (Sanders 2016).
21. IVIG 2 g/kg over 2-5 days or PLEX 5 exchanges for crisis, impending crisis, severe bulbar
    weakness or before surgery in unstable patients. IgA level before IVIG is reasonable but not a
    gate (only IgA deficiency with anti-IgA antibodies matters); check renal function and
    thrombotic risk.
22. Drugs that worsen MG (FDA boxed warning for fluoroquinolones; aminoglycosides, IV magnesium,
    macrolides, telithromycin (withdrawn, never list it as a current risk), non-depolarising
    neuromuscular blockers (need reduced doses with quantitative monitoring; succinylcholine
    resistance), botulinum toxin, D-penicillamine, immune checkpoint inhibitors. Use with caution:
    beta-blockers including timolol eye drops, hydroxychloroquine and chloroquine, procainamide,
    quinine, statins (case reports), iodinated contrast.
23. Wrong facts to delete wherever found: tiotropium "antagonises the NMJ" (it is a muscarinic M3
    antagonist and has no nicotinic action; it may blunt muscarinic side effects of
    pyridostigmine); metoprolol "prolongs QT" (it does not; its MG risk is beta-blockade);
    alemtuzumab "treats myasthenic disorders" (it can induce autoimmune disease, and MG has been
    reported after it); azathioprine "teratogenic"; "MGTX 5-year, Lancet Neurology 2022";
    "MMF NEJM 2008" (the MMF trials are Neurology 2008); "Rule of 20-30: intubate if NIF <-20";
    "HCQ used in NMJ protocols".
24. Amifampridine (LEMS): start 15 mg/day in divided doses, EU maximum 60 mg/day (SmPC; US label
    up to 80-100 mg/day). Contraindicated in epilepsy and, per the EU SmPC, with drugs with a
    known QT-prolonging potential and with congenital long QT; ECG at start and after titration.
    Seizure risk rises with dose. Pyridostigmine may be added. Treat the tumour first: LEMS often
    improves with SCLC treatment.

### 1.3 July 2026 physician guidance (Reviewer 2, condition_tool_guidance.yaml)

Facts 1-13 above restate it (mediastinal imaging in all, MRI only after negative serology and
neurophysiology, no CSF, no paraneoplastic panel, fixed serology order, RNS technique, SFEMG when
RNS is negative, FDG-PET only for LEMS). Departures for LEMS and crisis cases are in 3.5; the
guidance-claim change is CENTRAL 5.

---

## 2. Error classes in this condition

No reviewer note ids exist. Each class lists its cases; the per-case index (section 4) is
authoritative when a case differs.

### A. Template criteria and tiers (all except M04, P02, RM13, RM14, RM15, RM16 partially)

Description: the same 6-8 criteria were stamped on every case: labs
`[anti_AChR, anti_MuSK, anti_LRP4, TSH]` required, RNS required, SFEMG recommended, mediastinum CT
required, literature required or recommended, pyridostigmine drug check with a generic
`screen_for` list required, respiratory recommended, ice pack recommended (R series). Labels equal
rationales.

Fix: rebuild per section 3. In short:

- Labs criterion `required_arguments.panels` = `["anti_AChR", "TSH"]` (subset matching, so an agent
  that also orders MuSK still matches). MuSK enters as a separate required criterion only when the
  case is AChR negative (P01, P04, RP14, RS14); LRP4 or `clustered_AChR_cell_based` required only
  when double seronegative and the label rests on it (P04 LRP4), recommended in P01 and RP14.
- Literature: delete the criterion, or keep it `optional`, last, with no `expected_evidence` that
  any stored output repeats. Default: delete in S cases, optional elsewhere.
- Drug check: per the table in 3.2; never the generic pyridostigmine list without a medication of
  the patient's own. Drop `telithromycin` from every `screen_for`.
- Label: a short imperative ("Order AChR binding antibody and thyroid function"); rationale: why,
  for this patient, with its source. Label and rationale must differ.

### B. Scoring key in literature and drug outputs (all; leak guard fails M01, M03, RM13, RM15, S01, S03)

Description: initial literature output summary is the `expected_evidence` ("MGFA classification
stages disease severity; thymectomy benefits AChR+ generalized MG (MGTX); IVIG/PLEX for crisis",
RM13 the 3,4-DAP sentence). Literature follow-ups invent journals and years (list in fact 23),
give patient-specific conclusions (RM15 atracurium, RP12, RP13), are empty, or have
`query` equal to the trigger slug (R series). Drug outputs have `proposed` equal to a trigger slug
or to a full treatment plan.

Fix: keep at most one literature output per case (initial `literature_search`), in report voice,
citing only sources from 1.1 with what each source says, nothing about this patient. Canonical
text (adapt the topic sentence to the case's question; keep the citations correct):

> "Consensus guidance (Sanders DB et al., Neurology 2016;87:419-425; update Narayanaswami P et
> al., Neurology 2021;96:114-122) recommends AChR antibody testing first, MuSK testing when AChR
> antibodies are absent, and electrodiagnostic confirmation by repetitive nerve stimulation or
> single-fibre EMG. Chest CT or MRI is recommended in all patients to detect thymoma. In the MGTX
> trial (Wolfe GI et al., N Engl J Med 2016;375:511-522) thymectomy improved outcomes over three
> years in non-thymomatous AChR-positive generalized MG aged 18-65."

LEMS variant (P02, RM13):

> "Titulaer MJ et al. (Lancet Neurol 2011;10:1098-1107) describe LEMS as proximal weakness,
> autonomic dysfunction and areflexia with P/Q-type VGCC antibodies in about 85-90%; about half of
> patients have small cell lung cancer. SOX1 antibodies favour an associated SCLC. CT of the thorax
> is the first screening study and FDG-PET is added when CT is negative, with repeat screening
> every 3-6 months for 2 years (EFNS 2011). Amifampridine is the first-line symptomatic
> treatment."

Delete other literature follow-ups. Drug outputs: section 2.C.

### C. Drug-check outputs wrong, empty or a treatment plan (all)

Fix: one stored drug output per real interaction, `proposed` = the drug the case needs (or the
offending drug), `current_medications` = the patient's list, findings in checker voice (severity,
mechanism, action). Delete: P01 `request_prednisone_azathioprine_plan`, RM14
`request_long_term_immunosuppression_plan`, S01 and RM12 IVIG checks, M03
`request_tiotropium_interactions_mg` (wrong fact) unless rewritten to fact 23, S03
`request_diabetes_management_steroids`, S04 `request_insulin_pump_steroid_interaction` (steroid
hyperglycaemia is a must, not an interaction check), P02 duplicate `request_3damp_treatment_lems`
merged with the amifampridine check. Correct per fact 19 (S01 OCP), 22, 23 (M03, P02 metoprolol
QT, P03 alemtuzumab). The output must agree with `patient.clinical_history.allergies` (M02 has a
sulfa allergy while taking celecoxib, a sulfonamide: the cross-reactivity with non-antibiotic
sulfonamides is low, so keep both but have the drug output or a must note it; do not delete the
allergy).

### D. Shared prohibitions and musts (about 23 cases with the 7 identical prohibitions)

Fix the shared set as follows (keep only those relevant to the case; add case-specific ones):

- DELETE "Do NOT start high-dose prednisone ... without hospitalization or pyridostigmine bridge".
  REPLACE with canonical:
  > "Do not start high-dose prednisone (above 20 mg/day) as an outpatient; start low and titrate,
  > or start high dose only with inpatient monitoring, because initial steroid-induced worsening
  > can precipitate crisis."
- DELETE "Do NOT attribute ... before completing serology + RNS + single-fiber EMG" (SFEMG is not
  required in AChR+ cases). REPLACE where a functional or mimic label is in play with:
  > "Do not attribute fatigable ptosis, diplopia or bulbar weakness to a functional or <mimic>
  > cause before AChR antibody testing and neurophysiology."
- Drug prohibition canonical (name only drugs relevant to this patient plus the classic set):
  > "Avoid fluoroquinolones, aminoglycosides, macrolides and IV magnesium unless no alternative
  > exists and the patient is monitored; use non-depolarising neuromuscular blockers only at
  > reduced dose with quantitative monitoring."
  Never list telithromycin.
- Musts that are diagnostic tests ("Single-fiber EMG if diagnostic uncertainty (here ...
  conclusive)", "Single-fiber EMG given diagnostic clarity already achieved", S02, S04 and every
  hit): delete; tests are criteria.
- Every generalized AChR+ case under 66 without thymoma has the thymectomy must (fact 20), every
  thymoma case "thoracic surgery referral for thymectomy" with pre-operative IVIG/PLEX only if
  bulbar or respiratory weakness. Ocular cases: pyridostigmine, then low-dose prednisone if
  symptoms persist; no thymectomy must.
- Steroid-sparing and TPMT before azathioprine where long-term immunosuppression is a must.
- S01 "consider non-hormonal contraception" (rationale wrong): replace with fact 19 (counsel on
  pregnancy planning; avoid mycophenolate and methotrexate; azathioprine acceptable).

### E. Shared key_clinical_evidence and avoided actions (about 24 cases)

- "Anti-titin or anti-RyR ... surgical referral non-negotiable": replace with fact 4 wording, or
  delete when titin is not in the case.
- "All confirmed MG require CT chest ...": replace with "Mediastinal CT with contrast is indicated
  in every patient with MG to detect thymoma."
- Avoided actions EEG, CSF, FDG_PET, brain MRI, echo, cardiac monitoring: keep as waste with a
  case rationale and `[Jacob_2025]` text citation, not `[Wolfe_2016]`. Remove any avoided action
  that the case's own pathway needs (P03 MRI, P02/RM13 FDG_PET, RP14 echo, RM16 orbit MRI if
  added, RS14 MRI if kept).

### F. Head-CT fallback wording (21 cases)

The `fallback_tool_outputs.ct` impression "Normal study, and it does not address the question this
patient's workup turns on" tells the agent it went off path. Replace with a plain report:
> "Non-contrast CT head: no acute intracranial abnormality. Impression: normal non-contrast CT of
> the head."
Same rule for any other fallback that comments on relevance.

### G. Lab stub rows and qualitative panels (17 + 11 cases, plus CBC/BMP "All normal")

Rows "Ordered to exclude an alternative cause; ... which is what this case's diagnosis rests on"
and "Ordered as part of the baseline workup ..." with value "Within reference range" and no unit:
give a real value, unit and reference range; `clinical_significance` null (or a short report-voice
note when abnormal). CBC, BMP or CMP reported as "All normal": list the analytes with values.

### H. Unreachable, shadowed or misrouted reports

1. M01, S01: the initial specialized_test (RNS decrement) is shadowed by an RNS follow-up holding a
   50 Hz study with no facilitation. Merge into one `repetitive_nerve_stimulation` report (initial
   or follow-up, one only): slow-rate decrement in a facial and a proximal muscle, normal baseline
   CMAP, no post-exercise facilitation (facts 6, 8).
2. RP11, RP12, RS12, RS14, RS16: duplicate `respiratory_function` follow-ups; the second is an
   unreachable stub. Delete it (keep the one with real values, fact 14).
3. Chest CT stored as `initial_tool_outputs.ct` (head CT tool) in M01, M03, RM12, RS12, S02, S03,
   S04: move the content to `order_body_imaging` (`study: mediastinum_CT`, region chest,
   `contrast: true`), merging with the `request_thymectomy_evaluation` body follow-up (one report);
   `initial_tool_outputs.ct` becomes a plain head CT or is deleted (fallback F covers head CT).
4. Body-imaging `contrast` false while the criterion requires true: P01, RM15, RS14, RS15, RS12
   follow-up. Set true unless the case has a contrast contraindication (none found).
5. Prose discriminators: P02 `'PET-CT (FDG)'` and RM13 `'PET-CT (FDG whole body)'` -> `FDG_PET`;
   `'Autonomic Function Testing'` -> `autonomic_testing`; S01 `'MRI chest'` under
   `order_advanced_imaging` -> delete (the CT answers; if kept, it is `order_body_imaging`
   `mediastinum_MRI`); RS14 `'FDG-PET brain'` -> delete; RS15 `'Neostigmine challenge'` -> delete
   (not orderable).
6. Serology in a follow-up behind a TSH stub (RP11, RP12, RP13, RP14, RS11, RS12, RS13, RS15,
   RS16, RS17 via `request_achr_musk_lrp4_antibodies` or `request_achR_antibodies`; RS14
   `request_musk_antibodies`): put all first-line serology of the case (AChR binding, MuSK if
   tested, thyroid) into `initial_tool_outputs.labs`, delete the follow-up. Keep `interpret_labs`
   follow-ups only for genuinely later assays (CBA panel in a double seronegative case, LRP4 in
   P04, anti-GQ1b in RS11 if kept).
7. Biopsy filed as labs: P02 `request_hilar_biopsy_result`, RM13 `request_sclc_biopsy_result` ->
   `obtain_tissue_diagnosis` (lymph_node_biopsy or the site the case names) with TTF1_IHC and
   chromogranin_A_synaptophysin_IHC findings, as a follow-up after the CT.
8. Misplaced tests: urine culture in labs (M04, RM14) -> `order_microbiology` specimen urine;
   NIF/FVC in labs (RM14) -> `respiratory_function` (ABG may stay in labs); S02 clinical activity
   score in labs -> delete (it is an exam score; put CAS in the exam or delete); P01 anti-cortactin
   (not orderable) -> delete.
9. Not indicated follow-ups: MuSK/LRP4/VGCC follow-ups in AChR-positive cases (M01, M02, RM11,
   RM12) -> delete; M03 `request_prostate_cancer_paraneoplastic` (PSA plus paraneoplastic panel)
   -> delete (known low-risk prostate cancer is history; no paraneoplastic panel in MG).

### I. Stub outputs that report the expected text (R series and M03)

Ice pack (8 R cases), respiratory, RS14 SFEMG, RP13 mitochondrial panel, M03 ECG: outputs whose
findings are "see impression" or the `expected_evidence`. Write patient-specific values: ice pack
MRD1 before and after in mm on the ptotic side(s); SFEMG muscle, mean MCD in microseconds against
the reference, % fibre pairs with increased jitter and blocking; respiratory per fact 14; ECG with
rate, rhythm, PR, QRS, QTc. Or delete the criterion and the output when the study is not indicated
(ice pack without ptosis).

### J. Treatment disguised as a test, or treatment-response outputs (ruling 4)

Delete and turn into musts (with dose, route, and condition):

- M02 `request_ivig_plasmapheresis` (post-IVIG NIF/FVC day 5)
- P01 `request_pyridostigmine_response`
- P03 `request_ivig_for_mg` (AChR after IVIG)
- RM11 `request_ivig_lymphoma_mg`
- RM14 `request_plasmapheresis`, `request_ivig_alternative`
- RM15 `request_plasmapheresis_evaluation` (empty)
- S03 `request_ivig_preop` (labs), S01 `request_ivig_preop` (drug check), RM12
  `request_ivig_for_mg_post_gbs`
- RS13 `request_pyridostigmine_trial` (drug check with a trial plan)

### K. Patient-block leaks (ruling: answer leakage)

- NIF/FVC values in the exam or HPI: M01, M02, M03, M04, P01, P02, P03, P04, RM11, RM12, RM13,
  RM14, RM15, RM16, RS17, S01, S02, S03, S04. Delete the numbers (fact 16); in crisis cases keep
  the bedside picture (respiratory rate, accessory muscles, weak cough, SpO2) since the scored
  result is the formal measurement.
- "AChR" results in the patient block (M04, P01, P03, P04, RM15, S04): legitimate only as prior
  history when the case does not score ordering the test. In M04, RM14, RM15 (known MG) the prior
  positive AChR stays as history and AChR testing is not scored (3.5). In P01, P04 prior negative
  results stay as history only if the current labs criterion is the CBA or LRP4 study, not AChR.
- S03 exam "anti-titin ordered": delete.
- RS14 HPI lists the whole work-up ("Single-fiber EMG was normal", chest CT, spirometry, CSF,
  FDG-PET, MRI): rewrite the HPI to presentation and prior history only.
- P02 HPI "repeat EMG suggested NMJ involvement" and a surveillance CT 6 weeks ago: delete the EMG
  sentence; keep the prior CT as history only if the current CT is still indicated (it is, for
  restaging: say "last CT 6 months ago" if needed so the current one is due).
- M04, RM14 "CT chest" in history: prior imaging, keep only as history consistent with 3.5.
- Extra top-level patient keys (`age`, `ethnicity`, `hpi`, `pmh`, `sex`) in RM15, RP11..RP14,
  RS11..RS16 are invisible to the agent and dropped on save. Before saving, move any content not
  already in `demographics`, `history_present_illness` or `clinical_history` there (ethnicity to
  `demographics`), and check the duplicate does not contradict the kept field.

### L. Unit, arithmetic and logic errors

- Blocking antibody in nmol/L (R series): convert to % (fact 2).
- MuSK reference <0.4 in one case and <=0.02 in another within the condition: use one laboratory
  per case (fact 2).
- RP11 "NIF -38 ... meets threshold for adequate": reduced (fact 14).
- S01: NIF -58 called borderline in one place and normal in the report, FVC without unit or %
  predicted: rewrite per fact 14 with one consistent set.
- M02: AChR 0.6 with reference <0.5 called "borderline": positive.
- RM15: labelled established AChR-positive but its labs show anti_AChR Negative: stored labs show
  the known positive titre (history) or the AChR row is removed; never negative.
- Every respiratory report: weight and height in `physical_exam["general"]`; mL/kg = litres x 1000
  / kg.

### M. Differential not updated (most)

Ruling 7: after the pathway results, LEMS is low or very_low when RNS shows no facilitation and
VGCC was not tested or is negative; Graves orbitopathy low when TRAb negative and orbits normal;
CPEO low when fatigability and positive AChR are shown. Key features say which result excludes
each alternative. The per-case index names the entries to lower (marked "M:").

### N. Citations (all)

Apply 1.1. Remove `[Wolfe_2016]` from every criterion other than thymectomy musts and the
mediastinal imaging rationale (thymectomy decision). Remove duplicate citation strings.

---

## 3. Target pathway and tiers

### 3.1 Pathway order (followup_outputs and action_criteria)

Standard (new presentation of suspected MG):

1. `interpret_labs` AChR binding (+/- modulating/blocking), thyroid function and antibodies.
2. `order_specialized_test` repetitive_nerve_stimulation.
3. `interpret_labs` MuSK (if AChR negative), then CBA panel or LRP4 (if double seronegative).
4. `order_specialized_test` emg_single_fiber (when RNS normal or seronegative).
5. `order_specialized_test` ice_pack_test (only with ptosis; may come first as a bedside test).
6. `order_body_imaging` mediastinum_CT with contrast.
7. `order_specialized_test` respiratory_function (staging; first when the patient is bulbar or
   breathless, see 3.5).
8. `analyze_brain_mri` only where 1.2 fact 11 allows.
9. `check_drug_interactions` (pre-treatment safety).
10. `search_medical_literature` last.

Crisis and LEMS orders: 3.5.

### 3.2 Criteria rules

- Labs: one required criterion `["anti_AChR", "TSH"]`, except known MG (crisis cases).
- RNS required in every new-diagnosis case except where the case's data make SFEMG the only
  diagnostic study; ocular cases use one required "neurophysiology" criterion with two
  alternatives (RNS, SFEMG) and both reports served.
- SFEMG: required in seronegative cases (P01, P04, RP14) and wherever RNS is normal and the label
  rests on SFEMG; recommended when RNS is normal but serology is positive; optional or deleted
  when RNS is already diagnostic (an extra SFEMG is not waste, but not recommended).
- Mediastinum CT with contrast required in every MG case except where 3.5 says otherwise;
  alternative `mediastinum_MRI` with contrast and `chest_CT` with contrast accepted.
- Respiratory: required in crisis or impending crisis (M04, RM14, RM15) and wherever bulbar or
  respiratory symptoms are present and the case states FVC or NIF results (RP11 breathlessness,
  RS14, RS15 if laryngeal weakness is marked); recommended in other generalized cases; optional
  in ocular cases (S05, RS11).
- Ice pack: recommended only with ptosis on exam; deleted otherwise (RS14, RS15, check RS13 and
  RS16 exam).
- Drug check tiers (ruling 6):

| tier | cases and drug |
| --- | --- |
| required | M04 ciprofloxacin (precipitant), RM14 ciprofloxacin (precipitant), P02 and RM13 amifampridine (with the case's medicines; ECG), M02 hydroxychloroquine and pilocarpine against pyridostigmine (HCQ can worsen MG; pilocarpine adds muscarinic load), RM16 pyridostigmine with propranolol and methimazole (beta-blocker caution) |
| recommended | RM15 neuromuscular blocker/anaesthetic in an intubated MG patient (`drug` the agent used, `current_medications` the list), S03 metoprolol, RP13 timolol eye drops, M04 metoprolol if on the list, RM11 vincristine with planned steroids |
| optional or delete | all others (no concrete interaction: OCP, levothyroxine, metformin, amlodipine, losartan, statins, psyllium, aspirin, insulin). Default delete when the patient has no medicines (RP11, S05) |

- Literature: optional at most, last (2.A).
- Ids: keep existing `criterion_id`s when a criterion stays; new criteria get descriptive ids
  (`action-musk-antibody`, `action-respiratory-first`).

### 3.3 Sequence constraints (all soft; no hard constraint in this condition)

- Replace the shared `labs -> RNS` constraint (wrong reason) with, where both exist:
  - `labs -> SFEMG` soft, reason "AChR antibody testing precedes single-fibre EMG; SFEMG is
    reserved for seronegative patients or a normal RNS (Jacob 2025)."
  - `RNS -> SFEMG` soft, reason "Repetitive nerve stimulation is done first; SFEMG follows when RNS
    is normal (Jacob 2025)."
- Where no SFEMG criterion exists, delete the constraint (labs and RNS can run in parallel).
- AChR-negative cases: `AChR labs -> MuSK` soft.
- LEMS: `chest CT -> FDG_PET` soft, `chest CT -> tissue diagnosis` soft.
- Crisis: `respiratory_function -> mediastinum CT` soft (stabilise and stage the airway first).
- Never a constraint involving literature or a recommended drug check.

### 3.4 Stop rule

- `required_before_assessment`: the required criteria only (never literature, never an optional or
  recommended criterion).
- `max_additional_actions`: 1 in S cases, 2 in M, P, RM, RP and RS cases (one reasonable extra
  study, e.g. SFEMG after a positive RNS, or MuSK alongside AChR). The current 0 penalises the
  common practice of sending AChR and MuSK together.

### 3.5 Variant pathways and tier table

**Generalized AChR+ (M01, M02, M03, P03, RM11, RM12, RM16, RP11, RP12, RP13, RS12, RS13, RS15,
RS16, RS17, S01, S02, S03, S04)**

| criterion | tier |
| --- | --- |
| labs AChR + TSH | required |
| RNS | required (RM11: required; add the RNS report if none exists, with the SFEMG kept recommended) |
| SFEMG | recommended only if the case's RNS is normal or equivocal; else optional or deleted |
| mediastinum CT contrast | required |
| respiratory_function | recommended (required RP11) |
| ice pack | recommended only with ptosis |
| drug check | 3.2 table |
| literature | optional, last |
| case-specific | P03 brain MRI required; RM16 TRAb/anti-TPO/free T4 kept in labs; RP13 mitochondrial panel optional only if the case keeps CPEO in the differential, with a real result |

**Seronegative or LRP4 (P01, P04, RP14)**: labs AChR + TSH required, MuSK required, CBA or LRP4
required (P04) or recommended (P01, RP14), RNS required, SFEMG required, mediastinum CT required,
respiratory recommended, ice pack recommended with ptosis, echo in RP14 optional (APS is not an MG
indication for echo unless the case shows a cardiac question).

**MuSK+ (RS14)**: labs AChR + TSH required, MuSK required (the label rests on it), RNS required
(facial muscles), SFEMG recommended, mediastinum CT required (MuSK MG has no thymoma association,
but Reviewer 2 asks for imaging in every case; keep required), respiratory required (bulbar,
elderly), brain MRI optional (brainstem mimic), no ice pack (no ptosis), no CSF, no FDG-PET.

**Ocular (S05, RS11)**: labs AChR + TSH required, neurophysiology required (alternatives RNS,
SFEMG), ice pack recommended (ptosis), mediastinum CT required, respiratory optional, anti-GQ1b
(RS11) optional only if Miller Fisher stays in the differential, drug check deleted unless a real
interaction exists.

**Known MG in exacerbation or crisis (M04, RM14, RM15)**: the diagnosis is the exacerbation or
crisis; AChR is known (history). Pathway: respiratory_function first (required); precipitant
search required (drug check of the offending drug: M04 and RM14 ciprofloxacin; RM15 the aspiration
and the anaesthetic/NMB drug, recommended); labs required with CBC, electrolytes including
magnesium and phosphate, CRP, renal function, ABG (`panels` subset e.g.
`["CBC", "BMP", "CRP"]`); infection work-up: `order_microbiology` urine (M04, RM14) or
respiratory (RM15) and `order_body_imaging` `chest_xray` (RM14, RM15) recommended; AChR repeat
optional (not required: the diagnosis is known); RNS not indicated in crisis (delete RNS and SFEMG
criteria in RM15, M04, and set them as waste avoided actions with rationale "Electrodiagnostic
confirmation is not needed in a known AChR-positive patient in crisis and delays treatment");
mediastinum CT required only if the history does not document prior thymic imaging or thymectomy
and the deterioration is unexplained, otherwise optional (RM15 post-thymectomy with aspiration:
optional; M04 and RM14: worker checks the history and logs the choice). Cholinergic crisis is
low in the differential at pyridostigmine 240 mg/day or less without muscarinic signs. Musts:
ICU admission, airway plan per fact 15, IVIG or PLEX, pyridostigmine commonly held while
intubated (secretions), stop the offending drug, treat infection with an MG-safe antibiotic (not a
fluoroquinolone, aminoglycoside or macrolide), steroids started or increased under ventilatory
monitoring.

**LEMS (P02, RM13)** (labels kept; composition question in section 6):

| criterion | tier |
| --- | --- |
| labs anti_VGCC_PQ + anti_SOX1 (+ AChR) | required (`["anti_VGCC_PQ", "anti_SOX1"]`) |
| RNS with post-exercise facilitation | required |
| chest_CT with contrast (alternatives chest_abdomen_pelvis_CT, mediastinum_CT) | required |
| FDG_PET | required only if the CT is negative or equivocal (P02: a hilar mass on CT makes PET staging recommended; RM13 recurrent SCLC: recommended) |
| tissue diagnosis (lymph node or lung biopsy, TTF1 and chromogranin/synaptophysin IHC) | required in P02 (new tumour), recommended in RM13 if recurrence is not already biopsy proven |
| amifampridine drug check | required |
| ECG | required (QT before amifampridine; P02 apixaban and metoprolol) |
| autonomic_testing | optional |
| SFEMG | optional (RM13) |
| literature | optional, last |

Musts: treat the SCLC (oncology), amifampridine titration per fact 24, DELTA-P documented,
pyridostigmine as add-on, IVIG for severe weakness; prohibitions: no amifampridine with epilepsy or
QT drugs; avoid IV magnesium, aminoglycosides, fluoroquinolones, NMBs. The guidance claim
"mediastinum CT in every case" is read as "chest CT" for LEMS (CENTRAL 5).

---

## 4. Per-case index

Every log: "Reviewer notes: No reviewer notes for this case." Classes listed apply in addition to
A, B, D, E, F, N, which apply to all cases unless stated.

### M cases

- **MG-M01** (52 M, AChR+ generalized IIb with thymoma, Hashimoto)
  - Leak guard fails (B): rewrite initial literature.
  - H1: merge the RNS initial and follow-up into one report with slow-rate decrement.
  - H3: chest CT from `initial_tool_outputs.ct` to body imaging, merged with the thymectomy body
    follow-up.
  - H9: delete `request_musk_antibodies`.
  - K: NIF in patient block.
  - Drug check: atorvastatin and levothyroxine, no concrete interaction: optional.
  - Musts: thymectomy (thymoma), anti-thyroid antibodies known; TPMT before azathioprine if used.
  - Respiratory recommended; SFEMG optional (RNS diagnostic); stop rule 3.4.
- **MG-M02** (48 F, AChR+ IIb, SLE/Sjogren)
  - J: delete `request_ivig_plasmapheresis`. H9: delete `request_musk_antibodies`.
  - L: AChR 0.6 with <0.5 is positive. K: NIF, FVC in patient block.
  - Drug check required: pyridostigmine with hydroxychloroquine and pilocarpine (3.2); C: sulfa
    allergy and celecoxib note.
  - Literature follow-up `request_literature_review_mg_sle`: delete (B).
  - M: lupus myositis low after normal CK.
  - Musts: thymectomy per MGTX (age 48, AChR+, no thymoma), steroid start per fact 18.
- **MG-M03** (67 M, AChR+ IIb with thymoma, COPD, diabetes, low-risk prostate cancer)
  - Leak guard fails (B). H3: chest CT from ct to body imaging. H9: delete
    `request_prostate_cancer_paraneoplastic`.
  - C: tiotropium check rewritten to fact 23 or deleted; steroid-diabetes check deleted (turn into
    a must: glucose monitoring and insulin adjustment with prednisone).
  - I: ECG stub `request_analyze_ecg`: write a real ECG or delete with the criterion (optional
    ECG has no indication here unless a drug needs it: delete).
  - K: NIF, FVC. Penicillin allergy: musts must not name a penicillin.
  - M: LEMS moderate -> low after RNS without facilitation. Thymectomy must (thymoma, fit for
    surgery per the case).
- **MG-M04** (60 F, known AChR+ MG, III, fluoroquinolone exacerbation)
  - Crisis pathway (3.5): respiratory required first; drug check ciprofloxacin required; labs
    required as infection/electrolyte panel (keep CBC, CMP, CRP, urinalysis; AChR optional); RNS
    not indicated (delete criterion, add waste avoided action); mediastinum CT per 3.5 rule.
  - H8: urine culture to `order_microbiology` urine (recommended).
  - K: NIF in patient block; prior "CT chest" and AChR kept as history.
  - Sequence: replace `respiratory -> drug check` with `respiratory -> mediastinum CT` if the CT
    stays; literature optional last.
  - Musts: stop ciprofloxacin, MG-safe antibiotic for the UTI (penicillin allergy: not a
    beta-lactam penicillin; choose by culture, e.g. nitrofurantoin or a cephalosporin with
    caution), IVIG or PLEX, ICU if fact 15 thresholds; metoprolol caution (fact 22).
  - M: differential ok in principle; beta-blocker contribution low, keep.

### P cases

- **MG-P01** (44 F, seronegative generalized, SFEMG diagnosis, anxiety)
  - Seronegative pathway: MuSK required, `clustered_AChR_cell_based` recommended (separate
    report, not the action-1 report: fixes the perfect-agent warning), SFEMG required, RNS
    required.
  - H8: anti-cortactin deleted. J: `request_pyridostigmine_response` deleted. C:
    `request_prednisone_azathioprine_plan` deleted; drug check optional (sertraline, clonazepam,
    pregabalin: no MG-relevant interaction; benzodiazepine respiratory caution can be a must).
  - Literature follow-ups (2) deleted. H4: body imaging contrast true.
  - K: NIF; prior negative AChR history allowed only because the current scored labs are
    repeated AChR plus MuSK and CBA (keep the history as "AChR binding negative at outside
    laboratory").
  - M: FND moderate -> low after SFEMG.
  - Thymectomy: not routine in seronegative MG; may be considered (Sanders 2016 says it may be
    considered in non-responders); no thymectomy must.
- **MG-P02** (72 M, paraneoplastic LEMS with new SCLC, AF on apixaban, metoprolol)
  - LEMS pathway (3.5). Labs `["anti_VGCC_PQ", "anti_SOX1"]` required.
  - Body imaging: chest_CT contrast required with alternatives; FDG_PET discriminator fixed (H5);
    autonomic discriminator fixed (H5), autonomic optional.
  - H7: `request_hilar_biopsy_result` to `obtain_tissue_diagnosis` required.
  - C: amifampridine check required (metoprolol is not QT-prolonging; apixaban no interaction);
    merge `request_3damp_treatment_lems`. ECG `request_apixaban_3dap_ecg` required, rename the
    trigger content as a baseline QTc ECG.
  - K: delete the HPI repeat-EMG sentence; surveillance CT 6 weeks ago (see K).
  - Sequence: replace `labs -> literature` with `chest CT -> FDG_PET` and `chest CT -> tissue`.
  - M: MG moderate -> low after facilitation and VGCC positive.
- **MG-P03** (38 F, AChR+ IIb with RRMS on natalizumab)
  - Brain MRI required (MS relapse and PML exclusion); MRI with gadolinium sequences as is.
  - J: `request_ivig_for_mg` deleted. C: natalizumab PML "check" deleted or turned into a must
    (JCV antibody index, PML vigilance); P03 alemtuzumab wording (fact 23) fixed in whichever
    output carries it; the pyridostigmine/MS check optional.
  - Body imaging shows a 2.8 cm anterior mediastinal mass: add must "thoracic surgery referral
    for thymectomy (thymoma)", and key evidence; differential gains thymoma-associated MG.
  - K: NIF; AChR history check.
  - M: MS relapse high -> low; PML moderate -> low if MRI shows no PML lesion.
- **MG-P04** (48 M, LRP4+ generalized, double seronegative)
  - Labs: AChR + TSH required, MuSK required (separate or in the same criterion as
    `["anti_AChR", "anti_MuSK", "TSH"]`; keep the existing action-1 form), LRP4 required
    (action-2, keep), SFEMG required, RNS required.
  - Ice pack recommended (left ptosis). Respiratory recommended.
  - Literature optional last; drug check optional (atorvastatin, lisinopril).
  - K: NIF, FVC; AChR history (prior negative) allowed only if consistent with the scored labs.
  - Sequence: `labs -> SFEMG` keep with corrected reason; add `labs -> LRP4` soft.
  - M: AChR+ MG and MuSK MG moderate -> very_low or deleted after negatives.

### RM cases

- **MG-RM11** (57 M, AChR+ IIb in peripheral T-cell lymphoma on EPOCH with vincristine)
  - RNS required: add an RNS report (initial or follow-up) consistent with the SFEMG; SFEMG
    recommended. Check what `initial_tool_outputs.specialized_test` holds and route it.
  - J: `request_ivig_lymphoma_mg` deleted. H9: `request_musk_antibodies` deleted.
  - Drug check recommended: vincristine and planned prednisone (vincristine neuropathy, not NMJ);
    etoposide/doxorubicin no NMJ effect.
  - Anti-titin: fact 4 (late onset, 57).
  - K: NIF. M: vincristine neuropathy moderate -> low; LEMS moderate -> low if no facilitation.
  - Musts: haematology co-management; thymic imaging still required.
- **MG-RM12** (42 M, AChR+ IIb four weeks after presumed GBS)
  - H3: chest CT from ct to body imaging, merged with the thymectomy follow-up.
  - H9: `request_musk_antibodies` deleted. J: IVIG drug check deleted (gabapentin, enoxaparin
    discontinued: no interaction; drug check deleted).
  - Literature follow-up `request_gbs_mg_literature` deleted.
  - K: NIF. M: recurrent GBS moderate -> low when the nerve conduction in the RNS study shows no
    demyelination; the RNS report must state the conduction findings.
  - Musts: thymectomy per MGTX (42, AChR+, no thymoma if CT normal).
- **MG-RM13** (68 F, LEMS with recurrent SCLC)
  - Leak guard fails (B, the 3,4-DAP sentence).
  - LEMS pathway (3.5): labs `["anti_VGCC_PQ", "anti_SOX1"]` required (subset; the current
    6-panel list is over-specific); FDG_PET discriminator fixed (H5) and tier recommended; chest
    CT required; H7: `request_sclc_biopsy_result` to `obtain_tissue_diagnosis` (recommended).
  - Autonomic discriminator fixed (H5), optional; SFEMG optional; respiratory follow-up kept only
    if a criterion or the differential needs it (recommended if dyspnoea in HPI, else delete).
  - Amifampridine check required with ondansetron (QT-prolonging: a real EU SmPC
    contraindication; must switch the antiemetic) and levothyroxine; ECG criterion added
    (required).
  - K: NIF. M: MG low, keep.
- **MG-RM14** (55 F, known AChR+ MG, crisis V, ciprofloxacin)
  - Crisis pathway (3.5): respiratory required first; drug check `drug: ciprofloxacin` required
    (replace the generic pyridostigmine check); labs as infection/electrolyte/ABG panel; urine
    microbiology and chest_xray recommended; AChR optional; mediastinum CT per 3.5.
  - J: `request_plasmapheresis`, `request_ivig_alternative` deleted; C:
    `request_long_term_immunosuppression_plan` deleted; literature follow-ups (2) deleted, the
    "Rule of 20-30" text removed (fact 23).
  - H8: NIF, FVC, ABG out of labs into respiratory (ABG may stay in labs); urine culture to
    microbiology.
  - K: NIF, FVC, CT chest in patient block.
  - M: cholinergic crisis moderate -> low (180 mg/day pyridostigmine); aspiration/sepsis keep per
    data.
  - Aspirin "GI intolerance" listed as an allergy: musts must not prescribe aspirin.
- **MG-RM15** (50 M, known AChR+ MG post-thymectomy, aspiration crisis, intubated, on
  mycophenolate and prednisolone)
  - Leak guard fails (B). Crisis pathway (3.5): RNS and SFEMG criteria deleted with waste avoided
    actions; their follow-ups deleted; respiratory required (ventilator mechanics: FVC and NIF
    on weaning trial); labs infection/electrolyte panel required; respiratory microbiology and
    chest_xray recommended; mediastinum CT optional (post-thymectomy, explained precipitant).
  - L: labs must not show AChR negative.
  - J: `request_plasmapheresis_evaluation` deleted. Drug check of the NMB recommended
    (`check_atracurium_in_mg` rewritten in checker voice: reduced dose, train-of-four
    monitoring); literature follow-up deleted (patient-specific atracurium conclusion).
  - H4: body imaging contrast true if kept. K: NIF, FVC, AChR, extra patient keys.
  - M: aspiration pneumonia high is the precipitant (keep); cholinergic crisis moderate -> low.
  - Musts: PLEX or IVIG, hold pyridostigmine while ventilated, antibiotic for aspiration
    pneumonia avoiding aminoglycosides, fluoroquinolones and macrolides, swallow assessment
    before oral intake.
- **MG-RM16** (38 F, AChR+ II-III with Graves disease, methimazole, propranolol)
  - Labs criterion keep thyroid antibodies (case-specific), but reduce `required_arguments` to
    `["anti_AChR", "TSH", "TRAb"]`; free T4/T3 and anti-TPO in the report.
  - Drug check required (propranolol; methimazole: no NMJ effect; propranolol is a beta-blocker
    caution, consider switching rate control).
  - Ice pack recommended (right ptosis). Orbit MRI with contrast optional (TAO coexisting).
  - Literature optional last. K: NIF.
  - M: TAO high -> moderate (coexisting); thyrotoxic myopathy low after normal CK.
  - Musts: thymectomy per MGTX (38, AChR+, CT without thymoma), endocrinology co-management;
    radioiodine can worsen orbitopathy (steroid cover) as a must only if the case discusses it.

### RP cases (R series: apply H6 serology relocation and K extra keys in all)

- **MG-RP11** (68 M, thymoma-associated AChR+ IIb, breathlessness, no medicines)
  - H6: serology to initial labs. H2: delete the second respiratory follow-up. L: NIF -38 is
    reduced. I: ice pack with real MRD1 values.
  - Respiratory required (breathlessness). Drug check deleted (no medicines).
  - Thymoma: thymectomy must (age 68 is not an exclusion for thymoma surgery); differential
    thymic carcinoma moderate stays only if CT is atypical.
  - Literature follow-up `search_thymoma_mg_management` deleted or the only literature output.
- **MG-RP12** (74 M, bulbar late-onset AChR+ MG, Parkinson disease, weight loss)
  - H6, H2, I as RP11. Ice pack only if the exam has ptosis.
  - Respiratory recommended (required if bulbar weakness with weak cough is documented).
  - Drug check optional (levodopa: no NMJ interaction); keep the metoclopramide prohibition
    (worsens parkinsonism; valid).
  - Literature output patient-specific conclusion removed (B).
  - M: ALS and PD bulbar moderate -> low; recurrent NSCLC moderate needs the CT to answer it (low
    if CT shows no lung lesion). Thymectomy: not routine after 65 without thymoma; no must.
- **MG-RP13** (53 F, AChR+ generalized long misdiagnosed as CPEO, timolol drops)
  - H6, I. Mitochondrial panel: keep optional only with a real negative result in the follow-up
    `request_genetic_panel_mitochondrial`; delete `request_mitochondrial_workup` (labs stub).
  - Drug check recommended: timolol eye drops (beta-blocker caution, fact 22).
  - Ice pack recommended (bilateral ptosis). Literature summary patient-specific: rewrite (B).
  - M: CPEO moderate -> low; KSS, OPMD low.
- **MG-RP14** (44 F, seronegative generalized, SFEMG diagnosis, antiphospholipid syndrome)
  - Seronegative pathway: MuSK required, CBA recommended, SFEMG required, RNS required.
  - H6: serology to initial labs. Echo optional (or delete, with its follow-up, unless the case
    raises a cardiac question). Drug check optional (prednisone and APS thrombosis risk is a must).
  - Sulfonamide allergy: musts must not name a sulfonamide.
  - M: APS CNS and MS moderate -> low after normal MRI (if MRI is in the case) or excluded by the
    pattern; MuSK MG moderate -> very_low after negative MuSK.

### RS cases (R series: apply H6 and K extra keys in all)

- **MG-RS11** (52 F, ocular AChR+ I)
  - Ocular pathway: neurophysiology required with alternatives SFEMG and RNS (add an RNS report,
    normal or mildly abnormal in facial muscles); SFEMG kept. Ice pack recommended if ptosis
    (exam check; "eyelid swelling" in CC is not ptosis, verify).
  - Anti-GQ1b follow-up: optional, keep only if Miller Fisher stays in the differential.
  - Respiratory optional; drug check deleted (amlodipine, HCTZ).
  - M: "Generalized MG progression risk" is not a differential diagnosis: delete it from the
    differential (put the generalization risk in key evidence); TED low after normal TFTs.
- **MG-RS12** (69 M, late-onset AChR+ generalized, lichen planus)
  - H3: chest CT from ct to body imaging (merge the thymectomy follow-up). H4: contrast true. H2:
    second respiratory follow-up deleted. I: ice pack with real values.
  - Drug check deleted (metformin, amlodipine, topical betamethasone).
  - Literature follow-up deleted.
  - Thymectomy: not routine at 69 without thymoma; no must.
- **MG-RS13** (47 F, AChR+ generalized misdiagnosed as acquired Brown syndrome, on prednisolone
  25 mg)
  - H6. J: `request_pyridostigmine_trial` deleted. Literature follow-ups (2) deleted; HCQ fact
    fixed if it appears (fact 23).
  - Ice pack only with ptosis (check the exam; vertical diplopia alone does not qualify).
  - Drug check optional (prednisolone 25 mg already started: a must on steroid-induced worsening
    monitoring instead).
  - Orbit MRI optional (restrictive mimic). M: Brown, TED, INO low.
  - Musts: thymectomy per MGTX (47, AChR+, no thymoma).
- **MG-RS14** (75 M, MuSK+ bulbar MG with ophthalmoplegia, no ptosis, parkinsonism)
  - MuSK pathway (3.5). H6: MuSK result into initial labs. K: rewrite HPI (whole work-up leak).
  - Delete: ice pack criterion and follow-up (no ptosis), the CSF initial output (fact 13; CSF
    stays only as a fallback normal), FDG-PET brain follow-up (H5), second respiratory follow-up
    (H2). H4: contrast true. I: SFEMG stub with real values (SFEMG in MuSK MG is often abnormal in
    facial muscles and may be normal in limb muscles).
  - Respiratory required. Brain MRI optional.
  - Drug check optional (levodopa).
  - M: PD bulbar, ALS moderate -> low; AChR MG moderate -> very_low (AChR negative).
  - Musts: MuSK MG responds poorly to pyridostigmine (cholinergic hypersensitivity) and well to
    PLEX and rituximab; thymectomy not indicated.
- **MG-RS15** (53 F, AChR+ MG with isolated hypophonia)
  - Delete the neostigmine follow-up (H5), the ice pack criterion and follow-up (no ptosis),
    which also resolves the perfect-agent warning.
  - H4: contrast true. Respiratory recommended (laryngeal weakness).
  - Drug check deleted (psyllium, docusate).
  - Musts: the ENT laryngoscopy must "already considered" rewritten as a must ("ENT laryngoscopy
    to exclude vocal fold paralysis or a structural lesion") or deleted if the case reports it in
    history.
  - M: functional aphonia moderate -> low.
- **MG-RS16** (73 M, AChR+ MG with head drop, Parkinson-like features)
  - H6, H2, I. Ice pack only with ptosis (exam check). Literature follow-ups (2) deleted.
  - Drug check optional (atorvastatin: statin caution case reports; metformin, amlodipine,
    aspirin none).
  - Respiratory recommended (neck extensor weakness often travels with respiratory weakness).
  - M: INEM moderate -> low after AChR+ and decrement in trapezius.
- **MG-RS17** (60 F, AChR+ generalized IIa, straightforward)
  - H6: `request_achR_antibodies` to initial labs. I: ice pack with real values (left ptosis).
  - K: NIF in patient block.
  - Drug check deleted (losartan). Literature optional last or deleted.
  - Musts: thymectomy per MGTX (60, AChR+, no thymoma if CT normal).

### S cases

- **MG-S01** (34 F, AChR+ IIb-III with 4.2 cm thymoma, on combined OCP)
  - Leak guard fails (B). H1: merge the RNS initial and follow-up (decrement visible).
  - H5: delete the `MRI chest` advanced imaging follow-up (or route as mediastinum_MRI if the
    case needs MRI to separate thymoma from thymic carcinoma; default delete).
  - Tensilon in the RNS report deleted (fact 9). L: NIF and FVC consistent (fact 14).
  - C: OCP check corrected (fact 19) and optional; IVIG pre-op drug check deleted (J), pre-op
    IVIG or PLEX becomes a must only if bulbar or respiratory weakness is marked.
  - Musts: thymectomy (thymoma), pregnancy counselling (fact 19), D fix for contraception.
  - K: NIF. Literature criterion recommended -> optional or deleted.
- **MG-S02** (29 F, AChR+ IIb without thymoma, post-Graves hypothyroid on levothyroxine)
  - H3: chest CT from ct to body imaging. H8: CAS out of labs; delete
    `request_graves_thyroid_eye_disease_exclusion` unless it holds TRAb (then keep TRAb in the
    initial labs).
  - Tensilon in the RNS report deleted. D: SFEMG must deleted.
  - Drug check deleted (levothyroxine: no interaction). Literature follow-up deleted.
  - K: NIF. M: Graves orbitopathy moderate -> low with normal orbits or TRAb negative.
  - Musts: thymectomy per MGTX (29); pregnancy counselling (fact 19).
- **MG-S03** (62 M, AChR+ IIb with 3.6 cm thymoma, metoprolol, metformin, levothyroxine)
  - Leak guard fails (B). H3: chest CT from ct to body imaging. J: `request_ivig_preop` (labs)
    deleted. C: diabetes steroid check deleted (must instead); metoprolol check recommended with
    fact 22/23 wording.
  - K: NIF; "anti-titin ordered" in exam deleted.
  - Musts: thymectomy (thymoma).
- **MG-S04** (45 F, AChR+ IIb without thymoma, type 1 diabetes, high anti-GAD65, codeine
  intolerance)
  - H3: chest CT from ct to body imaging. Tensilon in the RNS report deleted. D: SFEMG must
    deleted.
  - C: insulin-steroid check deleted (glucose monitoring must instead); codeine check optional
    (opioids cause respiratory depression; codeine is listed as an allergy (nausea): musts must
    not prescribe it).
  - K: NIF, AChR in patient block.
  - M: stiff-person syndrome low (no rigidity or spasms) with key features.
  - Musts: thymectomy per MGTX (45, AChR+, no thymoma).
- **MG-S05** (39 M, ocular AChR+ I, no medicines)
  - Ocular pathway: neurophysiology required with alternatives RNS and SFEMG (RNS normal is
    typical of ocular MG; add an SFEMG report showing increased jitter in frontalis or
    orbicularis oculi); ice pack recommended (right ptosis).
  - Labs criterion `["anti_AChR", "TSH"]` (drop MuSK from the required list).
  - Drug check deleted (no medicines). Literature deleted.
  - M: TED moderate -> low (normal TFTs, no proptosis); generalization risk is not a diagnosis:
    delete from the differential.
  - Musts: pyridostigmine, low-dose prednisone if symptoms persist (reduces generalization risk,
    cite Sanders 2016), no thymectomy must.

---

## 5. CENTRAL requests (outside the case files)

1. Criteria pack `dataset-generation/criteria_packs/MG.md`:
   - `[Punga_2022]` title is wrong: the paper is "Epidemiology, diagnostics, and biomarkers of
     autoimmune neuromuscular junction disorders", Lancet Neurol 2022;21:176-188, not a
     treatment guideline.
   - `[Vincent_2003]` cites Nat Rev Immunol 2002;2:797-804: fix the year in the key description.
   - Add keys: `[Jacob_2025]`, `[Evoli_2019]`, `[Narayanaswami_2021]`, `[Wolfe_2019]`,
     `[Titulaer_2011]`, `[EFNS_paraneoplastic_2011]`, `[Lawn_2001]` (shared with GBS).
   - Literature and drug check no longer required by default (ROUND_POLICY 5, 6); telithromycin
     removed from the screen_for list; `[Wolfe_2016]` restricted to thymectomy.
2. ICD codes: ICD-10-CM G70.00 is "without (acute) exacerbation", G70.01 "with (acute)
   exacerbation". 24 cases with stable new-onset MG carry `icd_codes[0] = G70.01`; only M04, RM14,
   RM15 (exacerbation, crisis) fit G70.01. Workers do not change `icd_codes[0]` (ROUND_POLICY 3);
   Andrea or a reviewer to approve a batch reorder to G70.00 first in the other cases.
3. Synonyms (`diagnosis_synonyms.yaml`, G70 group): "ocular myasthenia gravis" is accepted for
   generalized cases and "generalized myasthenia gravis" for ocular cases (S05, RS11), so the
   ocular/generalized distinction is never scored; bare "MG" is a single token that matches any
   submission containing "MG" (e.g. "MuSK MG" is fine, but also an abbreviation in another
   diagnosis). Proposal: split into G70.00 generalized and ocular groups (ocular: H-code not
   needed; ICD-10-CM has no ocular-specific code, so scope by case subtype) and drop bare "MG".
   For the crisis cases add "myasthenic crisis" (G70.01). For LEMS (G73.1): check the group
   accepts "Lambert-Eaton myasthenic syndrome" and "LEMS" with "paraneoplastic" optional.
4. `conditions.yaml` myasthenia_gravis `common_followups`: `request_pulmonary_function` under
   interpret_labs and `request_thymectomy_evaluation` under order_ct_scan are stale (respiratory
   is `order_specialized_test` respiratory_function; thymic imaging is `order_body_imaging`
   mediastinum_CT). `optional_modalities` note "CSF in RS14 only" becomes "no CSF" after RS14.
5. Guidance claims (`condition_tool_guidance.yaml`, `test_guidance_claims.py`): "mediastinum CT
   required in all 30" becomes: required in new-diagnosis MG; chest CT (not mediastinum CT) in
   the LEMS cases P02 and RM13; optional in RM15 (post-thymectomy crisis) and per-case in M04,
   RM14. Refresh the claims after the round.
6. Library (`fallback_library.yaml`): the head CT normal report and any library report that says
   the study "does not address the question" (class F) need neutral wording at the library level
   too, if the phrase comes from there.
7. Vocabulary: `anti_titin` and `anti_RyR` are not in `costs.yaml` (checked 24 Oct), yet RM11,
   S03 and the shared key evidence mention titin. Optional addition as thymoma markers (fact 4);
   until then workers remove titin rows from stored labs and keep any titin fact as history only.

---

## 6. Open questions for Andrea

1. Composition: P02 and RM13 are LEMS (G73.1) under the MG condition, and M04, RM14, RM15 are
   exacerbation or crisis in already-diagnosed MG (management, not diagnosis). Default this round:
   keep all five with their labels, LEMS and crisis pathways per 3.5. Alternative: move LEMS to a
   separate NMJ condition and keep crisis cases as a management subtype.
2. ICD reorder (CENTRAL 2): approve setting G70.00 first in the 24 stable cases? Workers leave
   G70.01 until approved.
