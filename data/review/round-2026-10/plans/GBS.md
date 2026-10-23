# GBS: condition plan for the October 2026 review round

This is the lead plan for the 30 Guillain-Barre syndrome cases (GBS-M01..M03, P01..P03, S01..S04,
RM11..RM16, RP11..RP16, RS11..RS18). Workers follow it case by case so that every case reaches the
same decision. Read `ROUND_POLICY.md` and `PATTERNS.md` first; this plan does not repeat them.

**The notes.** All 68 are Reviewer 2 case comments with no field path; Reviewer 1 has not reviewed
GBS. Section 4 lists every note with the class (section 2) that resolves it.

**Case status.**
- Reviewer 2 approved RP16, RS12, S02, S03 and S04 (with notes), and PATTERNS.md counts 7 approved
  GBS cases: treat S01 and RS18 (no notes) as approved too. Change approved cases only for the real
  errors this plan names (the class errors of section 2 are real errors: they break the harness or
  contradict the governing guideline).
- M02 is `in_progress` with Reviewer 2: fix it like the others.

**Baseline (24 Oct 2026, before any edit).** `perfect_agent.py` passes 30/30. All 30 cases carry
the same 8 criteria (a1 labs, a2 EMG/NCS, a3 CSF, a4 respiratory function, a5 literature, a6 DDI,
a7 ECG, a8 telemetry); RM14, RS12, RS13, RP16 and RS18 add a9 optional contrast spine MRI. Every
case has the same two sequence constraints (the first one names the wrong criterion) and the same
stop rule with `max_additional_actions: 0`.

**How to use this plan.**
1. Apply every class of section 2 to your case, in order. Use the canonical texts verbatim and fill
   the `<...>` slots from the case.
2. Apply the per-case decisions of section 4.
3. Rebuild `action_criteria`, `followup_outputs`, `sequence_constraints` and `stop_rule` as section
   3 says.
4. Run `perfect_agent.py <CASE> -v` and `case_io.py check <CASE>`, write the log and cite every note
   id with its ruling.

Section 2 cites notes by their first 8 characters; section 4 gives the full ids. "F<n>" is the
current position of a follow-up and "a<n>" is criterion `action-<n>-...` as the case stands before
editing.

**Conventions for new text.**
- English, in the case's own spelling.
- No em or en dashes (write "to" or a hyphen).
- Units as the case already uses them (cmH2O, mL/kg, mg/dL, cells/mm3).
- Invent no number the case does not need. A new value must be plausible, differ from the other
  cases, and agree with the rest of the case (for example FVC in L, % predicted and mL/kg must be
  arithmetically consistent with the weight).

---

## 1. Governing guidelines and canonical facts

### 1.1 Sources (citation keys)

| Key | Full reference | Use |
|---|---|---|
| [EAN_PNS_2023] | van Doorn PA, Van den Bergh PYK, Hadden RDM, et al. European Academy of Neurology/Peripheral Nerve Society Guideline on diagnosis and treatment of Guillain-Barre syndrome. J Peripher Nerv Syst 2023;28:535-563 (also Eur J Neurol 2023;30:3646-3674) | Governing guideline: diagnosis, tests, treatment, monitoring |
| [Leonhard_2019] | Leonhard SE, Mandarakas MR, Gondim FAA, et al. Diagnosis and management of Guillain-Barre syndrome in ten steps. Nat Rev Neurol 2019;15:671-683 | Red flags, respiratory monitoring, variants |
| [Brighton_2011] | Sejvar JJ, Kohl KS, Gidudu J, et al. Guillain-Barre syndrome and Fisher syndrome: case definitions and guidelines for collection, analysis, and presentation of immunization safety data. Vaccine 2011;29:599-612 | Levels of diagnostic certainty (the only certainty scheme cases may quote) |
| [Lawn_2001] | Lawn ND, Fletcher DD, Henderson RD, Wolter TD, Wijdicks EFM. Anticipating mechanical ventilation in Guillain-Barre syndrome. Arch Neurol 2001;58:893-898 | 20/30/40 rule; >30% fall in VC |
| [Walgaard_2010] | Walgaard C, Lingsma HF, Ruts L, et al. Prediction of respiratory insufficiency in Guillain-Barre syndrome. Ann Neurol 2010;67:781-787 | EGRIS |
| [Walgaard_2011] | Walgaard C, Lingsma HF, Ruts L, van Doorn PA, Steyerberg EW, Jacobs BC. Early recognition of poor prognosis in Guillain-Barre syndrome. Neurology 2011;76:968-975 | mEGOS (uses clinical diarrhoea history, not serology) |
| [Walgaard_2021] | Walgaard C, Jacobs BC, Lingsma HF, et al. Second intravenous immunoglobulin dose in patients with Guillain-Barre syndrome with poor prognosis (SID-GBS): a double-blind, randomised, placebo-controlled trial. Lancet Neurol 2021;20:275-283 | No second IVIg course |
| [Wakerley_2014] | Wakerley BR, Uncini A, Yuki N; GBS Classification Group. Guillain-Barre and Miller Fisher syndromes: new diagnostic classification. Nat Rev Neurol 2014;10:537-544 | Variant definitions (MFS, PCB, bifacial weakness with paraesthesias, paraparetic) |
| [Schneider_2021] | Schneider BJ, Naidoo J, Santomasso BD, et al. Management of immune-related adverse events in patients treated with immune checkpoint inhibitor therapy: ASCO guideline update. J Clin Oncol 2021;39:4073-4126 | ICI-related GBS (RP11 only) |
| [Haanen_2022] | Haanen J, Obeid M, Spain L, et al. Management of toxicities from immunotherapy: ESMO Clinical Practice Guideline. Ann Oncol 2022;33:1217-1238 | ICI-related GBS (RP11 only) |

- Replace every free-text citation string (`van_den_Berg_2014`, `GBS criteria pack §2`, unkeyed
  author-year strings) with keys from this table. `[van_den_Berg_2014]` (van den Berg B, Walgaard C,
  Drenthen J, et al. Nat Rev Neurol 2014;10:469-482) may stay only as a secondary key next to
  [EAN_PNS_2023], written in full the first time a case uses it (note c0279d2a).
- `[Hadden_1998]`, `[Asbury_1990]`, `[Sharshar_2003]` and `[Yuki_2012]` remain allowed but are no
  longer primary: cite [EAN_PNS_2023] for any statement it covers.

### 1.2 Canonical facts (state them this way in every case)

**Diagnosis.**
- Required features [EAN_PNS_2023, Brighton_2011]: progressive, bilateral, relatively symmetric
  weakness of the limbs (legs only in the paraparetic variant; none in MFS and the cranial
  variants), with decreased or absent reflexes in the weak limbs. Nadir between 12 hours and 28 days
  (write "within 4 weeks"). A course longer than 4 weeks to nadir is not GBS (acute-onset CIDP is
  then the leading consideration).
- Red flags that call for an alternative or for imaging [EAN_PNS_2023, Leonhard_2019]: sensory
  level, extensor plantars, hyperreflexia, marked persistent asymmetry, bladder or bowel dysfunction
  at onset, fever at onset, CSF cells >50/mm3, severe pulmonary dysfunction with little limb
  weakness, severe sensory signs with little weakness, nadir <24 h or progression >4 weeks.
- CSF: albuminocytological dissociation (raised protein, cells usually <5/mm3; 5-50/mm3 compatible
  but should prompt consideration of an alternative; >50/mm3 suggests another diagnosis). Normal
  protein in the first week does not exclude GBS.
- EMG/NCS supports the diagnosis and may be normal in the first week (repeat at 2-3 weeks if
  needed). Electrodiagnostic subtyping (AIDP, AMAN, AMSAN) is not required for diagnosis or
  treatment and is not advised for routine decisions [EAN_PNS_2023]. A subtype label in a case is
  allowed only if the case's own NCS numbers meet it.
- Certainty: quote Brighton 2011 levels only, and only once per case, consistent with the data
  (level 1: clinical features + CSF cells <50 and raised protein + NCS consistent; level 2: clinical
  features + either CSF cells <50 with raised protein or, if CSF not done or normal, NCS consistent;
  level 3: clinical features only). Brighton does not apply to a patient without limb weakness;
  MFS has its own Brighton definition.
- Variant definitions [Wakerley_2014]: MFS (ophthalmoplegia, ataxia, areflexia, no limb weakness);
  PCB (oropharyngeal, neck and arm weakness with arm areflexia, legs spared); bifacial weakness with
  paraesthesias (facial diplegia, distal paraesthesias, reduced reflexes, no limb weakness);
  paraparetic (weakness and areflexia restricted to the legs).

**Tests.**
- Routine blood tests [EAN_PNS_2023]: full blood count, glucose, electrolytes, renal function, liver
  tests, CK. Abnormal liver tests and hypoalbuminaemia are associated with a worse course.
- Anti-ganglioside antibodies: anti-GQ1b only when MFS or an MFS-spectrum overlap is suspected
  (anti-GT1a in PCB); not advised for typical sensorimotor GBS, for subtyping or for prognosis
  [EAN_PNS_2023]. A positive result never establishes the diagnosis on its own.
- Antecedent-infection serology is not needed for the diagnosis. Prognostic models (mEGOS) use the
  clinical history of diarrhoea, not serology [Walgaard_2011]. A positive IgM is not proof of an
  active infection or of the trigger.
- Nodal/paranodal antibodies (anti_NF155, anti_CNTN1) only when an autoimmune nodopathy is
  suspected (severe, treatment-refractory, tremor, ataxia, relapse).

**Respiratory and autonomic monitoring.**
- Report bedside respiratory function as: FVC in L, % predicted and mL/kg (weight required), MIP
  (NIF) and MEP in cmH2O, single breath count when the case uses it, and change from the previous
  measurement. Values below reference are flagged L, never H, and never "within normal limits".
- ICU-level monitoring and intubation planning [Lawn_2001, EAN_PNS_2023, Leonhard_2019]: FVC <20
  mL/kg, MIP weaker than -30 cmH2O (i.e. between -30 and 0), MEP <40 cmH2O, a fall in VC of more
  than 30%, single breath count <20, bulbar dysfunction with weak cough or pooled secretions,
  autonomic instability, or rapid progression. Reviewer 2's ruling (note 2a09feee): FVC <60%
  predicted calls for ICU-level monitoring. Clinical signs of respiratory distress, hypoxaemia or
  hypercapnia mean intubation regardless of the numbers. The decision is never one threshold:
  write it as trend + bulbar function + cough + secretions + fatigue (note 9dc82346).
- EGRIS [Walgaard_2010] may be quoted when the case gives days from onset to admission, facial
  and/or bulbar weakness and MRC sum score.
- Cardiac: continuous inpatient telemetry with blood pressure monitoring while weakness progresses
  (autonomic instability); a 12-lead ECG at baseline is recommended.

**Treatment (assessment text only; ROUND_POLICY ruling 4, never a tool call).**
- IVIg 0.4 g/kg/day for 5 days (2 g/kg total) started within 2 weeks of onset, or plasma exchange
  200-250 mL/kg in 5 sessions within 4 weeks, for patients unable to walk unaided (GBS disability
  score 3 or more). Consider in ambulant patients with rapid progression, bulbar, autonomic or
  respiratory involvement. Not advised in grade 1-2 patients within 2 weeks of onset unless they
  progress. No preference between IVIg and PE; do not give IVIg directly after PE; no second IVIg
  course [Walgaard_2021].
- MFS: IVIg and PE are not routinely advised; admit and monitor for overlap with GBS or Bickerstaff
  brainstem encephalitis (limb weakness, bulbar or respiratory involvement, reduced consciousness).
- Corticosteroids: strong recommendation against oral corticosteroids, weak recommendation against
  IV methylprednisolone [EAN_PNS_2023]. Exception: ICI-related GBS (RP11), where ASCO and ESMO
  advise IVIg or PE together with methylprednisolone and holding the checkpoint inhibitor.
- Plasma exchange cautions (relative, not contraindications unless the case gives a source):
  haemodynamic instability, active bleeding or full anticoagulation, sepsis, difficult venous
  access; ACE inhibitors held 24 h before albumin-replacement PE (bradykinin reactions).
- Neuromuscular blockade: avoid succinylcholine in GBS (hyperkalaemia from denervation).

**Weight.** The demographics schema has no weight field. Put weight and height in
`patient.physical_exam["general"]` as "Weight <kg> kg, height <cm> cm", consistent with the case's
BMI.

---

## 2. Error classes

### C1. Respiratory values labelled normal, flagged H, or without weight (13 notes)
Notes: 1b3ba3ad, 9dc82346 (M02); 38ccdb70 (M03); 2a09feee (RM11); a2cd5342 (RM12); 2f754e55
(RM13); 61e678b0 (RM14); 33eaec73 (RM16); b0808edf (RP11); d4baaeb9 (RP12); ed62b4ac (RP14);
0a7f2022 (RP15); 693830c4 (RP16). Survey: "All values within normal limits" for FVC 55-94% in 16
cases, low values flagged "(H)" elsewhere, no weight anywhere.

Decided fix:
- Add weight and height (section 1.2) and compute mL/kg.
- Rewrite the respiratory follow-up in the canonical format below. Ventilated cases (RS13, RS16,
  RS17, RS18, S03) report the last pre-intubation values and say the patient is now ventilated;
  ventilator settings are not a respiratory-function result.
- Remove spirometry numbers and interpretive phrases from the patient block ("AT INTUBATION
  THRESHOLD", "just above intubation threshold", "These values are concerning", "Precautionary
  admission warranted"): the numbers are the result of a4 (timeline leak). Keep clinical signs
  (dyspnoea, weak cough, SpO2, accessory muscle use, staccato speech).
- Fix arithmetic: % predicted = measured / predicted (RM12: 2.8 / 4.2 is 67%, not "2.6 L 62%"; pick
  one pair and make every field agree).
- Where values meet any ICU trigger of section 1.2, the assessment must contain "Admit to ICU-level
  monitoring" with the triggers named; where the trend is falling (M02: FVC 2.0 to 1.6 L, NIF -32 to
  -24), add the escalation must "Plan elective intubation if FVC falls below 20 mL/kg, MIP weaker
  than -30 cmH2O, or bulbar function, cough or secretions worsen".
- Change a4 expected_evidence to the canonical text.

Canonical a4 label: "Bedside respiratory function (FVC, MIP, MEP), repeated serially while weakness
progresses".
Canonical a4 expected_evidence: "FVC in L, % predicted and mL/kg, MIP and MEP, with the trend;
ICU-level monitoring if FVC <20 mL/kg or <60% predicted, MIP weaker than -30 cmH2O, MEP <40
cmH2O, a fall of more than 30%, or bulbar weakness with weak cough".
Canonical follow-up text: "Bedside respiratory function <time>: FVC <x> L (<y>% predicted;
<z> mL/kg at <w> kg) L. MIP <a> cmH2O L. MEP <b> cmH2O L. <Change: FVC <x0> L to <x> L over <t> h
(<p>% fall).> Cough <weak/effective>." Omit "L" on values within reference; omit the change
sentence when there is one measurement.

### C2. Ganglioside antibodies requested, served or interpreted against the guideline (7 notes)
Notes: a69c5ec7 (M02); 4d885b61 (M03); ae0f3536 (RM11); 09291641, ee1e4f06 (P01); 22430160
(RS11); 39b7526d in part (RM12, anti-GT1a unreachable). Survey: a1 requires `anti-GM1 IgM` in all
30 cases while the follow-ups report IgG; the trigger `request_anti_ganglioside_panel` is never
reached by `panels: ['anti-GM1 IgM']` (no shared token); positive results sit uninterpreted.

Decided fix:
- Remove `anti-GM1 IgM` from a1 in all 30 cases (section 3.1).
- Typical sensorimotor GBS (every case except P01, RM12, RM15, RS11, RS15, RS18): delete the
  ganglioside follow-up and every statement that depends on it (KCE pearls, labels such as
  "anti-GM1 / GD1a positive" or "multi-antibody positive", NCS structured fields that cite
  anti-GM1). Replace the pearl with the canonical pearl below where the case had a ganglioside
  pearl.
- MFS-spectrum and PCB cases (P01, RM12, RM15, RS11, RS15, RS18): keep one follow-up with the
  antibodies that matter (anti-GQ1b IgG; anti-GT1a IgG in PCB), trigger renamed
  `request_anti_gq1b_gt1a_ganglioside_panel`, `tool: interpret_labs`. Until CENTRAL request 1 adds a
  vocabulary term, add no criterion for it: the follow-up is reachable when the agent writes
  "GQ1b", "GT1a" or "ganglioside" in `clinical_context` (worker verifies with the probe). Mark the
  missing criterion BLOCKED in the log, citing CENTRAL 1.
- Every positive result that stays is interpreted in the assessment (pearl or differential).

Canonical pearl: "Anti-ganglioside antibodies are not needed to diagnose typical GBS; anti-GQ1b is
tested when Miller Fisher syndrome or an overlap is suspected [EAN_PNS_2023]."

### C3. Unsupported or over-read antecedent infections (8 notes)
Notes: 6644822c (M01); 40837d83 (M03); 39b7526d in part (RM12, "post-CMV probable"); 8241358d
(RM16); bc02717e (RS12); 4021807f (S02); 3c94e91e (S03); e48d42bd (S04). Survey: unorderable infection serology sits
in the initial labs (Campylobacter: M01, M02, P01, P02, P03, RM11, S01, S03; Mycoplasma: M03, RS17;
CMV: RM12; CMV/EBV/HSV: RM16; EBV: S02; influenza PCR: S04).

Decided fix:
- Delete antecedent-infection serology and PCR from current-encounter lab reports. The antecedent is
  history (what the patient reports, or a test done before the encounter and named as such).
- Labels and KCE name an antecedent only as the history supports it: "after a diarrhoeal illness",
  "after an upper respiratory infection", "after culture-confirmed Campylobacter enteritis" (P03,
  S01 only, where a prior stool culture is history). Otherwise no trigger in the label.
- Remove musts and expected_evidence that demand trigger identification or stool culture; remove
  the "stool culture / Campylobacter serology if recent diarrhea" clause from a1.
- A diarrhoea history counts for mEGOS; say so where a pearl discusses prognosis.

Canonical pearl: "The antecedent infection is a history finding; serology is not needed for the
diagnosis, and a positive IgM does not prove the trigger."

### C4. Variant label not met by the case's own findings (8 notes)
Notes: 0b90c02f, 0ddd925b (RM14); e89ffe81 (RM15); c1f03f5c (RS11); 98e9377c (RS15); 8e2833d3
(RP12); 9fee5e3b (RP13); 9f5f1a74, cfa3beb7 (RM13, RP15: course longer than 4 weeks or no arm
weakness). Decided fix: make the findings meet the label, or change the label to what the findings
meet, per section 4. Rule: prefer editing the case so it is a clean example of the condition it
claims (ROUND_POLICY: a label changes only when ruled wrong); drop electrodiagnostic subtype words
when the NCS does not meet them. Every change propagates to HPI, exam, NCS impression and
structured fields, KCE and differential.

### C5. Differential and mimics left unresolved after the work-up (12 notes)
Notes: 7b88d7ad (RM12); 3b0554e2 (RM13); ef2c7677 (RP11); e5ca0f0c in part (RP12); e7f671d6
(RP13); 797f335a in part (RP14); 9f5289ae (RS13); 7fcdfb5c, b578810b (RS15); 10c8e5fc (RS16);
dfea15bf, 86ecf008 (RS17). Decided fix (ROUND_POLICY ruling 7): the differential is the
assessment-time view. A mimic stays moderate or high only if the case leaves it open; otherwise
either add the test that excludes it (criterion + follow-up, section 3) or lower it with a reason in
`reasoning` naming the finding that excludes it. Remove "Critical illness polyneuropathy" from
non-ICU cases or set it very_low with "no ICU course before onset". Acute-onset CIDP stays at low
(it cannot be excluded at presentation; reassess at 8 weeks).

### C6. Red herrings missing, dangling or not distractors (5 notes + survey)
Notes: b2c102d6 (RM11, unilateral facial palsy); 8241358d (RM16); 682d7003 (RS14 vaccine); dfea15bf
(RS17); e7f671d6 (RP13). Survey: M01 RH 2 cites a lumbosacral MRI that does not exist; P01 RH is
albuminocytological dissociation (a supporting finding, not a distractor); empty RH in RM11, RM16,
RP12, RP13, RS11, RS14-RS17, S01-S04. Decided fix: every red herring names a finding present in the
case, says why it misleads and what resolves it; delete RH entries without a source in the case.
Cases with no genuine distractor may keep an empty list (do not invent one).

### C7. Timeline leaks and editorialising in the patient block (5 notes + survey)
Notes: d8e03a5d (RS13); 91de81af (RP14); 797f335a in part (RP14); 09291641 (P01 "pending");
72d65aba (RS16). Survey: spirometry in the patient block in about 24 cases
(C1); P01, P03, RM13, RP11, RP14, RS16 leaks listed in section 4; editorial phrases. Decided fix: delete results of scored studies from the patient
block; keep prior results only where the case does not score ordering them and they are dated as
prior; one time point per exam (date-stamp "Day <n>:" when the case spans days); delete editorial
sentences.

### C8. Safety-cap claims and treatment statements without a source (5 notes)
Notes: b71e3c4f (RP11 steroids); c7fc4320 (RM14 PE and breastfeeding); 442f0e51 (RP15 PE in
transplant); e62f0ba4 (RM15 "if confirmed"); 8018be9e (P03 grade 1). Survey: "Do not give
corticosteroids as monotherapy" in all 30; "Do not combine IVIG and PE in sequence"; "Do not start
IVIG without checking renal function and IgA"; DDI follow-ups that call PE "contraindicated"
(RP15, RS16) or prescribe management (RM13 FFP, RS17 switch antibiotic, RP16 hold vincristine).
Decided fix:
- Replace the steroid prohibition with the canonical one (RP11 excepted, section 4).
- Replace "Do not combine IVIG and PE in sequence" with "Do not give IVIg directly after plasma
  exchange, and do not give a second IVIg course [EAN_PNS_2023, Walgaard_2021]".
- Replace "Do not start IVIG without checking renal function and IgA" with "Check renal function
  before IVIg" (IgA: open question 3).
- Treatment musts follow section 1.2: IVIg or PE only when the case meets the indication; in grade
  1-2 patients the scored behaviour is admission and monitoring with treatment on progression.
- DDI outputs are category-level and sourced; "contraindicated" only with a source, otherwise
  "relative caution".

Canonical steroid prohibition: "Do not treat with corticosteroids: oral corticosteroids are
strongly advised against and IV methylprednisolone is not recommended [EAN_PNS_2023]."

### C9. Wrong-tool, unreachable, placeholder or unsafe follow-ups (4 notes + survey)
Notes: e5ca0f0c (RP12 edrophonium); 682b32b6 (RS14 head CT); c0279d2a in part (M02 empty step 5);
24f4abe2 (P02 CMV PCR unreachable). Survey:
- Brain MRI served under `order_advanced_imaging` (RM15 `request_brain_mri`, RS11
  `request_brain_mri`, RS15 `request_brain_mri_gadolinium`, RP13 `order_mri_brain`): move to
  `analyze_brain_mri`, or delete when no criterion or must needs it.
- Chest CT under `order_ct_scan` (RS11 `request_chest_imaging`): move to `order_body_imaging`
  study `chest_CT` if kept.
- Barium swallow under `interpret_labs` (RM12 `request_swallowing_eval`): delete (a swallow study
  is not in the vocabulary; the swallow assessment is a must, not a tool).
- Edrophonium (RM15 F6, RP12 F3): delete. Where an NMJ mimic needs excluding, use
  `repetitive_nerve_stimulation`, `ice_pack_test`, `emg_single_fiber` and `anti_AChR`/`anti_MuSK`/
  `anti_LRP4` labs, each as its own follow-up.
- Placeholder ECG follow-ups (`request_analyze_ecg` with rate 0 and the expected_evidence pasted as
  text) in P01, P03, RS18: write a real ECG report or delete (the initial ECG output serves a7).
- Empty literature and DDI follow-ups (`search_gbs_treatment`, `check_ivig_drug_interactions`
  placeholders): delete, or fill per section 3.2.
- RS14 head CT F5 and RP14 EEG F5: delete RS14 F5; keep RP14 EEG only if a criterion or must needs
  it (it does not: delete; the prior EEG is history).
- P02: CSF CMV PCR is not in the vocabulary; see section 4.

### C10. Lab and CSF expected evidence copied from a template (3 notes + survey)
Notes: ee1e4f06 in part (P01 "mild leukocytosis" vs WBC 9.2); 261fe3e8 (RS14); bfc49d34 (P02 cells
<10 vs 22). Survey: a1 expected_evidence "Mild leukocytosis / elevated inflammatory markers
reflecting antecedent infection; ganglioside antibodies for variant typing; trigger identification
(Campylobacter, CMV, EBV, Mycoplasma, HIV)" in all 30; a3 "cell count <10/uL" in all 30; HIV
"Non-reactive" with the leaky clinical_significance "Ordered to exclude an alternative cause; the
result does not support one, which is what this case's diagnosis rests on" in 29 cases (P02 is HIV
positive). Decided fix: canonical a1 and a3 texts (section 3.1); delete the leaky
clinical_significance sentence everywhere (routine labs have `clinical_significance: null`);
expected_evidence names what this case's labs actually show where it differs from the canonical.

### C11. Literature and certainty statements (2 notes + survey)
Notes: c0279d2a (M02); 605dea03 (P03). Survey: in about 25 cases the initial literature output
echoes a5's expected_evidence verbatim with `evidence_level: "guideline recommendation"` and source
`van_den_Berg_2014` (scoring-key leak). Decided fix: literature becomes optional and last (section
3); its output is the population-keyed canonical summary of section 3.2 with [EAN_PNS_2023]; quote
Brighton levels only per section 1.2, once per case.

### C12. Telemetry and monitoring outputs that run into the future (survey, ROUND_POLICY ruling 4)
Survey: telemetry reports span 72-240 h and report treatment (atropine, labetalol, transvenous
pacing, nitroprusside, "metoprolol held") in M02, RS13, RS16, S01, S03 and others. Decided fix:
report the first 24 h of monitoring at the time of assessment, findings only, no treatment; keep
the case's autonomic findings that fall within 24 h. a8 expected_evidence follows.

Canonical a8 expected_evidence: "Continuous telemetry with blood pressure monitoring: <the case's
24-hour findings>; autonomic instability (rate and blood pressure lability, bradyarrhythmia)
requires continued monitoring while weakness progresses".

### C13. Prior-coagulation and LP safety (1 note + survey)
Note: b902ee1c (RP16). Survey: RM13 (INR 1.9, platelets 88), RS16 (apixaban, aspirin, ticagrelor),
RP13 (new atrial fibrillation; check the medication list for an anticoagulant). Decided fix: hard
sequence constraint a1 before a3 (labs including CBC and coagulation before the LP) in RP16, RM13,
RS16, and RP13 if anticoagulated; add `coagulation` to a1 panels in those cases; RS16 also requires
a6 (DDI) before a3 (hard). Delete treatment steps (transfusion, FFP) from follow-ups; the
assessment may say "correct coagulopathy before LP" where the values require it.

---

## 3. Target pathway and tiers

### 3.1 Criteria (keep the criterion ids; order = clinical order)

Order the criteria so "Optimal actions 1..N" in the review app read in clinical order. Keep the
existing ids even when the position changes.

1. **a2 EMG/NCS** (required). Args `{'test_type': 'emg_ncs'}`. Label "Nerve conduction studies and
   needle EMG". expected_evidence: "Polyradiculoneuropathy pattern (demyelinating or axonal
   features, absent F-waves, sural sparing where present); may be normal in the first week".
2. **a3 CSF** (required). Args `{}` (add `special_tests` only where section 4 says). Label "Lumbar
   puncture for CSF cell count, protein and glucose". expected_evidence: "Albuminocytological
   dissociation: raised protein with cells <5/mm3 (5-50/mm3 compatible but prompts an alternative;
   >50/mm3 suggests another diagnosis); protein may be normal in the first week".
3. **Mimic-exclusion criteria the case raises** (recommended unless section 4 says required):
   contrast spine MRI (`order_body_imaging`, `spine_MRI`, contrast true) only for a red flag of
   section 1.2 (keep a9 as optional where it exists, with its reason); brain MRI (`analyze_brain_mri`)
   for brainstem or Bickerstaff differential or reduced consciousness; RNS / ice pack / AChR-MuSK-LRP4
   for an NMJ mimic; CK and `myositis_panel` for a myopathy mimic; AQP4/MOG cell-based for a cord
   signal (RS18). New ids continue after a9 (`action-10-...`).
4. **a1 labs** (required). Args `{'panels': ['CBC', 'CMP', 'CK']}` (add `coagulation` per C13).
   Label "Baseline blood tests: full blood count, renal function and electrolytes, liver tests,
   albumin, glucose and CK". expected_evidence: "Baseline values before treatment; abnormal liver
   tests or low albumin mark a higher risk of a severe course; no metabolic or toxic alternative".
   Drop `HIV`, `inflammatory_markers` and `anti-GM1 IgM` from the required args. HIV becomes a
   recommended criterion only where the case gives a risk (none currently; P02 is known positive).
5. **a4 respiratory function** (required; canonical text C1).
6. **a8 telemetry** (required; canonical text C12) and **a7 ECG** (recommended, unchanged label).
7. **a6 DDI**: required only when the medication list contains a concrete interaction with the
   planned work-up or treatment (ROUND_POLICY ruling 6): an anticoagulant or antiplatelet (LP, PE),
   an ACE inhibitor (albumin PE), a calcineurin inhibitor or other nephrotoxic drug (IVIg),
   an immune checkpoint inhibitor (hold), vincristine or other neurotoxic chemotherapy, a statin
   where myopathy is in the differential, a QT-prolonging drug with autonomic QT prolongation.
   Expected required in RM13, RP11, RP13, RP15, RP16, RS16, RS17; workers check the medication list
   of every other case and record the decision in the log. Otherwise optional. Label "Check the
   medication list for interactions with <the case's drugs> before <LP / IVIg / PE>".
8. **a5 literature**: optional, last. Label "Optional literature search on <the case's specific
   question>". expected_evidence general (section 3.2).

Variant cases (P01 MFS, RS11 bifacial, RM12 and RS15 PCB, RM15 cranial) keep a2-a4 and a8 required;
a4 stays required because overlap with respiratory involvement is the main risk.

### 3.2 Outputs
- Initial outputs serve the first order of each tool; follow-ups serve repeat or specific orders.
  The ganglioside follow-up exists only per C2.
- Literature output (initial, one per case): population-keyed, general, no case-specific numbers,
  e.g. "Guidelines for adults with GBS who cannot walk unaided advise IVIg 2 g/kg over 5 days within
  2 weeks of onset or plasma exchange within 4 weeks, with no preference between them; a second IVIg
  course is not advised [EAN_PNS_2023, Walgaard_2021]". Case-specific population allowed (HIV, MFS,
  transplant, ICI, postpartum) if general. `evidence_level` describes the source ("guideline"), not
  the scoring key.
- DDI output: category-level interactions only, each with a source or "relative caution"; no
  management instructions.
- Routine labs: `clinical_significance: null`.

### 3.3 Sequence constraints, stop rule, exemptions
- Delete the constraint `action-2 -> action-6` (it names EMG where the reason is respiratory).
- Keep `action-1 -> action-6` soft only where a6 is required.
- Hard constraints only per C13 (labs before LP; RS16 DDI before LP).
- Stop rule: `required_before_assessment` = the required criteria only (never a5; a6 only where
  required); `max_additional_actions: 3` (allows the recommended and optional criteria plus one
  repeat).
- Avoided actions: keep EEG, echocardiogram and CT head as waste unless the case needs them
  (RS17 EEG and brain MRI, RP13 and P01 brain MRI: remove from waste where they become criteria).
  Brain MRI is waste only where nothing in the case raises a brainstem or central differential.
- `panel_required_exemptions`: none expected (LABS, CSF, specialized_test and cardiac_monitoring
  stay required in every case). If a worker removes a panel-required tool, add the exemption with
  the note id.

---

## 4. Per-case index

Approved cases are marked (A). "Classes" lists the classes to apply beyond the universal ones (C1,
C2, C3, C7, C8, C9, C10, C11, C12 apply wherever the survey found the pattern; check every case).

### M01 (post-URI AIDP)
- Notes: 6644822c-c4a8-4823-a15c-5d41c800d454 (C3): Campylobacter attribution vs URI history.
- Decisions: keep the URI history (no diarrhoea added); delete Campylobacter serology from labs;
  label "Guillain-Barre syndrome (acute inflammatory demyelinating polyradiculoneuropathy) after an
  upper respiratory infection"; rewrite KCE 1 and 4 without Campylobacter/anti-GM1. Delete
  ganglioside follow-up (C2). Median CMAP 4.2 mV labelled reduced with a normal limit >4: give a
  value below the limit (for example 3.1 mV) or drop "reduced". Delete "This is the most alarming
  finding". RH: delete RH 2 (no lumbosacral MRI); keep RH 1 only if WBC 11.2/CRP/ESR stay in the
  labs, with its resolution. FVC 58% at presentation: ICU-level must (C1).

### M02 (post-diarrhoeal AIDP, in_progress)
- Notes: 1b3ba3ad-b993-4b76-86b8-189db252739b (C1, falling FVC/NIF needs escalation);
  9dc82346-524b-4736-871e-1e299ba7da4a (C1, multi-factor decision); a69c5ec7-f70b-4d93-b4f8-2e148173298b
  (C2); 3776d769-9d0e-4822-b9db-54d368d24e96 (EDX severity mismatch, no median CMAP value);
  c0279d2a-1ef6-4ce9-a048-c60652e75c44 (C11 citations and certainty, C9 empty step 5).
- Decisions: ICU-level and elective-intubation musts per C1 with the trend; NCS structured field
  severity "Severe" to match the impression, add median CMAP values (for example 3.4 mV, lower limit
  4.0); label without "secondary axonal injury" unless the repeat NCS stays and is scored (the
  repeat NCS follow-up shows falling CMAP: keep it as a repeat-NCS follow-up, label may keep "with
  secondary axonal features" since the repeat shows it); delete Campylobacter serology, keep the
  diarrhoea history (mEGOS). Citations per section 1.1; Brighton level 1 stated once. Fill or
  delete the empty literature follow-up (section 3.2). KCE 3 "even when bedside FVC is initially
  reassuring" contradicts the values: rewrite.

### M03 (AIDP on diabetic neuropathy)
- Notes: 38ccdb70-95de-45cf-a8b2-90ae9d840ff2 (C1, FVC 67% flagged H);
  4d885b61-9917-46f5-bff1-71edfd6450cf (C2, GD1b); 40837d83-a9d7-4f45-9c41-11b33a4d1760 (C3,
  Mycoplasma IgM).
- Decisions: flag L; delete ganglioside follow-up; delete Mycoplasma IgM from labs; KCE 4
  ("aggressive infection or DKA workup") replace with glucose monitoring during illness. Top
  differential "Acute worsening of diabetic polyneuropathy" high: lower to low with reason (acute
  4-limb weakness, areflexia, bifacial weakness, CSF dissociation, demyelinating NCS).

### P01 (Miller Fisher syndrome)
- Notes: 09291641-c07a-4c19-99e2-89d0e22d238c (C2/C7, GQ1b in initial labs vs "pending");
  ee1e4f06-6611-455e-8eb5-b0b4e84a33e0 (C2 order GQ1b alone, drop broad panel and "variant typing",
  fix "anti-GM1 IgM"; C10 "mild leukocytosis" vs WBC 9.2; C3 diarrhoea conditional).
- Decisions: GQ1b out of the initial labs into the C2 follow-up (`request_anti_gq1b_gt1a_ganglioside_panel`,
  GQ1b IgG positive with the case's titre; drop Campylobacter IgG); delete "Anti-GQ1b result
  pending" and "Triad: ..."; label keeps "anti-GQ1b positive" only if the follow-up stays (it does).
  Add brain MRI criterion (`analyze_brain_mri`, recommended; KCE 3 already asks for it) served by
  the existing brain MRI follow-up (rename trigger `order_brain_mri_brainstem`); remove brain MRI
  from waste if listed. Musts: replace "Initiate IVIG..." with "IVIg and plasma exchange are not
  routinely advised in MFS; admit and monitor for limb weakness, bulbar or respiratory involvement
  or reduced consciousness [EAN_PNS_2023]". Mental status "Confused about why he cannot walk":
  rewrite as "Alert and fully oriented" (confusion would raise BBE). RH (albuminocytological
  dissociation) is not a distractor: delete. NCS structured note ("cranial nerve and dorsal root
  ganglion level"): delete the interpretation (Kind 1). Placeholder ECG follow-up (C9).

### P02 (HIV-associated AIDP)
- Notes: 4a3dc6d5-b69a-44f8-b2b2-1921b2afcdfd (C10, HIV non-reactive in an HIV-positive patient);
  24f4abe2-1aa4-4007-bc14-3112e507776f (C9, CSF lacks CMV PCR and cytology required by must 4);
  bfc49d34-c6be-433d-996a-c1b365171a2d (C10, expected cells <10 vs 22).
- Decisions: delete HIV antibody from labs; add `HIV_viral_load` to the labs report (recommended
  criterion `interpret_labs {'panels': ['HIV_viral_load']}` with undetectable result and CD4 380);
  a3 args `{'special_tests': ['cytology']}` and CSF report with cytology negative and lymphocyte
  differential; CMV PCR stays out (CENTRAL 4) and must 4 becomes "Exclude CMV polyradiculitis:
  unlikely with CD4 380 and undetectable viral load, lymphocytic not neutrophilic CSF; send CSF CMV
  PCR" (the must may name a test the agent cannot order). a3 expected_evidence: "Raised protein
  with 10-50 cells/mm3, compatible with HIV-associated GBS but prompting exclusion of CMV
  polyradiculitis and lymphoma". Delete Campylobacter IgM (C3); keep the GI history. KCE 4 (IVIg
  preferred to avoid removing antiretrovirals) unsourced: delete. Left facial and ptosis: make
  facial weakness bilateral-asymmetric or keep unilateral with RH (same class as RM11).

### P03 (early GBS, ambulant)
- Notes: 8018be9e-37f0-4fa0-b466-58d5b1c7e7bd (C8, grade 1, treatment not advised);
  605dea03-950a-4786-8757-63d98f7ae6d3 (C11, Brighton level and 12 vs 4 weeks contradictions).
- Decisions: add mild distal weakness (for example ankle dorsiflexion 4+/5, finger abduction 4+/5)
  so the case meets the required features (C4); GBS disability grade 1 stays (walks, could run
  with difficulty: state the grade). Musts: "Admit for serial respiratory and autonomic monitoring;
  IVIg is not routinely advised in mildly affected patients within 2 weeks of onset; treat if she
  loses the ability to walk unaided or develops bulbar, respiratory or autonomic involvement
  [EAN_PNS_2023]". Brighton level 2 (normal CSF, NCS consistent) stated once; "nadir within 4
  weeks" everywhere. Delete "NCS was ordered" (C7); delete Campylobacter IgM and anti-GM1 from labs
  (C2, C3; the prior stool culture stays as history). Placeholder ECG (C9).

### RM11 (post-diarrhoeal AIDP with left facial palsy)
- Notes: 2a09feee-d8ae-4553-a841-33cca7c377e0 (C1, FVC 65% "normal"; ICU at <60%; weight);
  b2c102d6-ed63-4c0c-8b40-436212532917 (C6, unilateral facial palsy unresolved);
  ae0f3536-786c-4083-bcd9-2132b3746b6f (C2, pearl 3).
- Decisions: keep unilateral facial palsy and add RH "Unilateral facial palsy: may suggest Bell's
  palsy or a brainstem lesion, but facial involvement in GBS is often asymmetric and the limb,
  reflex, CSF and NCS findings place it in the polyradiculoneuropathy". Delete "FVC 65%" from HPI
  and patient block (C1/C7). Pearl 3 replaced with the C2 pearl; pearl 2 on Campylobacter rewritten
  per C3. Delete Campylobacter IgM and ganglioside follow-up.

### RM12 (PCB variant)
- Notes: a2cd5342-e2a0-444d-ae96-622cecab7def (C1, FVC 67%/NIF -30 "normal", 2.8 vs 2.6 L, weight);
  39b7526d-309e-44bf-9f6a-8c28786a621f (C2/C3, anti-GT1a and CMV PCR unreachable, "post-CMV
  probable"); 7b88d7ad-6228-4237-9df3-c574b6cfc2e3 (C5, MG and botulism moderate).
- Decisions: label "Guillain-Barre syndrome, pharyngeal-cervical-brachial variant"; delete CMV IgM
  from labs and "CMV serology and PCR" from the must; keep GT1a in the C2 follow-up (BLOCKED
  criterion, CENTRAL 1). MG: add a recommended criterion `interpret_labs {'panels': ['anti_AChR']}`
  (negative follow-up) and state the NCS RNS result if the NCS already reports it; then MG low.
  Botulism: lower to low with reason (areflexia with demyelinating NCS, no pupillary involvement,
  raised CSF protein, no food or wound exposure in the history). Delete the barium swallow
  follow-up (C9); the swallow assessment stays a must. Brain MRI: KCE 4 asks for it; add
  `analyze_brain_mri` recommended criterion with a normal follow-up, or delete KCE 4 (worker's
  choice; log it).

### RM13 (AIDP with liver disease)
- Notes: 9f5f1a74-9634-4250-bf7c-7b90c41fa661 (C4, 6-week progression fails <=4 weeks);
  2f754e55-6dae-4b9f-94af-e88c1a1419c0 (C1, FVC 58%/NIF -26 "normal", no escalation, weight);
  3b0554e2-c324-4db0-aac9-389d1d4f4fb7 (C5, statin or inflammatory myopathy unresolved).
- Decisions: shorten the course: bronchitis about 4 weeks before, weakness for 3 weeks with nadir
  now (move every "6 weeks"/"7 weeks" consistently; acute-onset CIDP low). Myopathy: delete the
  myopathic needle EMG features (short polyphasic units; NCS QD "mixed ... myopathic") and make the
  needle EMG neurogenic or reduced recruitment only; CK mildly raised (for example 410 U/L) with
  myoglobin deleted; add recommended `interpret_labs {'panels': ['myositis_panel']}` criterion with a
  negative follow-up; differential "statin-associated or inflammatory myopathy" low with reason
  (areflexia, CSF dissociation, demyelinating NCS, CK only mildly raised); a6 DDI required
  (atorvastatin). Ammonia: HPI says not elevated, labs say 68 H: make them agree. INR 1.9, platelets
  88: C13 hard labs-before-LP; `coagulation` in a1; delete the FFP instruction from the DDI output.
  Delete "Serum CK markedly elevated on admission" (C7). ICU-level must (C1).

### RM14 (postpartum GBS)
- Notes: 0b90c02f-9ca4-42f3-919a-349b87c851f1 (C4, AMSAN label vs demyelinating numbers);
  c7fc4320-dbc5-47d8-9bc9-af521f53717a (C8, breastfeeding and PE interruption claim unsourced);
  0ddd925b-9d4d-4ced-bd25-3e9f4ecec9d6 (C4, "generalized" while legs only);
  61e678b0-bba0-4d15-be7d-9168e980716c (C1).
- Decisions: the NCS numbers are demyelinating: label "Guillain-Barre syndrome (acute inflammatory
  demyelinating polyradiculoneuropathy), postpartum"; NCS QD rewritten to demyelinating, no
  "generalized" and no "AMSAN". Arms: give mild arm involvement consistent with grip 80% (for
  example finger abduction 4/5, grip 4/5) and reduced arm reflexes (biceps and brachioradialis 1+),
  so the case meets the required features; keep legs-predominant wording. Breastfeeding: delete the
  "PE interrupts breastfeeding 24-48 h" claim; the must becomes "Breastfeeding can continue with
  IVIg or plasma exchange; review each co-medication for lactation safety" with source LactMed
  (NIH Drugs and Lactation Database, immune globulin) or drop the source sentence if the worker
  cannot cite it (open question 5). Delete GM1/GD1a follow-up (C2). Keep a9 spine MRI optional
  (spinal anaesthesia RH).

### RM15 (isolated bilateral ptosis with areflexia)
- Notes: e89ffe81-0d83-4cdc-a95b-78daf43baa89 (C4, not a variant as written; MG high);
  e62f0ba4-b211-41b2-a224-f289d6b4436a (C8, "immunotherapy if confirmed" undefined).
- Decisions (open question 1 asks Andrea to confirm): keep G61.0 and make the case a recognised
  MFS-spectrum presentation, "acute ptosis" variant of anti-GQ1b antibody syndrome: GQ1b IgG
  positive in the C2 follow-up; label "Anti-GQ1b antibody syndrome (acute bilateral ptosis with
  areflexia), Guillain-Barre syndrome spectrum". MG: add recommended `anti_AChR` lab criterion
  (negative), delete the edrophonium follow-up, keep RNS in the NCS output; MG lowered to low with
  reason (no fatigability, no diurnal variation, normal RNS, negative AChR, areflexia). Brain MRI
  follow-up moved to `analyze_brain_mri` (recommended criterion: midbrain lesion in the
  differential). Must 4 becomes "No IVIg or plasma exchange while deficits stay restricted
  (EAN/PNS: not routinely advised in MFS-spectrum disease); admit and monitor for ophthalmoplegia,
  bulbar, limb or respiratory involvement".

### RM16 (AIDP with sensory ataxia)
- Notes: 33eaec73-0153-4ec7-8201-655a987b4078 (C1, FVC 55%/NIF -26 "normal", weight);
  8241358d-e1bf-4e8a-8aa1-745e10dfe385 (C6/C3, no red herrings; triple IgM).
- Decisions: the triple CMV/EBV/HSV IgM becomes the red herring, kept as prior serology in the HPI
  dated before the encounter: "Low-level IgM to CMV, EBV and HSV: simultaneous positivity is
  typical of cross-reactivity or polyclonal activation, not of three active infections, and does
  not change the diagnosis". The T4 temperature level (resolved as patchy on detailed exam) is a
  second RH resolved by the spine MRI. Ganglioside follow-up deleted (typical sensorimotor). FVC 55%
  is below 60%: ICU-level must. The CSF report spans two LPs (day 1 and day 14): keep only the LP at
  assessment time (C7). DDI: macrolide course finished; a6 optional unless a current drug
  interacts.

### RP11 (ICI-related GBS)
- Notes: b71e3c4f-c56f-462a-8d65-179237c24a65 (C8, steroid must needs named source);
  b0808edf-ad61-4485-9159-9d887dae9bbe (C1, FVC 60%/NIF -28 "normal"); ef2c7677-21ab-4a3b-aaf5-f38e219673af
  (C5, ICI-MG high unexcluded).
- Decisions: keep steroids as a must with [Schneider_2021, Haanen_2022]: "Hold pembrolizumab
  permanently; give IVIg or plasma exchange together with IV methylprednisolone (ICI-related GBS,
  ASCO and ESMO guidance)"; the canonical steroid prohibition does not apply (write instead "Do not
  rechallenge with the checkpoint inhibitor"). Doses in open question 4. ICI-MG: the NCS already
  reports no decrement; add recommended `anti_AChR` criterion (negative); lower to low with reason.
  irAE myositis/myocarditis: CK and troponin in labs (add `troponin` to the labs report); differential
  moderate only if CK or troponin is raised in the case. TSH 14.0 out of the patient block (C7; it
  stays in the labs). FVC 60% at threshold: ICU-level must. a6 required (pembrolizumab,
  lenvatinib). Delete the dexamethasone mention from the DDI output unless sourced.

### RP12 (severe AIDP with left ptosis)
- Notes: 8e2833d3-10bd-48c5-8534-cab79697b031 (C4, label says unilateral facial, exam shows no
  facial weakness but left ptosis); d4baaeb9-ead9-4dae-b089-ab2fcfe8fb3c (C1, FVC 58%/NIF -28
  "normal"; ICU must without intubation criteria; weight); e5ca0f0c-2750-4743-9e2b-8ebb8de3ab25 (C9,
  edrophonium redundant and unsafe; C5, ptosis: Horner or oculomotor in differential or RH).
- Decisions: label to the exam: "Guillain-Barre syndrome, severe acute inflammatory demyelinating
  polyradiculoneuropathy with left ptosis"; delete edrophonium follow-up (AChR, MuSK, RNS, SFEMG
  and ice pack are already negative: keep them as separate follow-ups only if criteria use them,
  otherwise state RNS in the NCS report). Add to the differential "Horner syndrome" very_low (pupils
  equal) and "Partial oculomotor palsy" very_low (full eye movements, pupils spared), or one RH
  "Unilateral ptosis" with that resolution. Respiratory: ICU-level must with the C1 trigger list
  and "intubate if FVC <20 mL/kg, MIP weaker than -30 cmH2O, or respiratory distress". KCE 2 (MRI
  brain for asymmetric cranial findings): keep only if a brain MRI criterion is added; otherwise
  delete (worker logs the choice).

### RP13 (sensory-predominant early AIDP, cervical stenosis)
- Notes: 9fee5e3b-336c-4934-9753-945eec5ee2c9 (C4/C7, reflexes 2+ "NO areflexia" vs HPI areflexia
  day 2; must conditional on areflexia); e7f671d6-6bae-4ec1-8f3c-ea42e39cf75e (C5/C6, cervical
  stenosis, asymmetric left hand, no spine imaging, no RH).
- Decisions: exam is the day-2 exam: reflexes reduced (biceps 1+, knee 1+, ankle absent), and the
  normal day-1 reflexes stay in the HPI as history; delete the conditional must. Add recommended
  contrast spine MRI criterion (`order_body_imaging`, `spine_MRI`, contrast true; reason: known
  cervical stenosis with asymmetric hand symptoms) with a follow-up showing stable degenerative
  stenosis without cord compression or signal change, and nerve root enhancement if consistent.
  RH: "Known cervical canal stenosis and chronic right foot drop" and "Wake-up onset in a patient
  with atrial fibrillation", each resolved. Brain MRI follow-up moved to `analyze_brain_mri` with a
  recommended criterion (stroke work-up for wake-up asymmetric deficit). a6 required (check
  propranolol, citalopram, solifenacin and any anticoagulant; C13 if anticoagulated). Ganglioside
  follow-up deleted.

### RP14 (GBS presenting with SIADH)
- Notes: 91de81af-b530-4c9f-b3d0-a6095eef7cd4 (C7, day 1 reflexes stated two ways);
  ed62b4ac-1d07-4a36-8d70-f1962cc4a05b (C1, FVC 68%/NIF -30 "normal"; weight, BMI 29.8);
  797f335a-8ac9-4a20-ae17-6874e4bccdee (C7/C5, 3 of 5 musts already done or unorderable; brain MRI
  in history but waste; osmotic demyelination moderate).
- Decisions: day 1 reflexes "diminished" in both places. Musts: delete the completed ones (sodium
  correction, SIADH work-up, brain MRI); keep current-encounter musts (GBS treatment decision, slow
  sodium correction target as a monitoring must, telemetry). Brain MRI and EEG stay history (done
  before the neurology question; not scored); delete the EEG follow-up (C9). Delete the day-1 CSF
  result from the HPI (C7; a3 serves it). Osmotic demyelination lowered to very_low (MRI without
  ODS, lower motor neuron signs, CSF dissociation); "Primary SIADH" high reworded as "SIADH as the
  sole cause" low (cannot explain areflexic weakness); autoimmune encephalitis low (encephalopathy
  resolved with sodium).

### RP15 (AIDP after lung transplant)
- Notes: 442f0e51-6754-4fe5-a785-0af4ea5a8ae8 (C8, PE "contraindicated" unsourced);
  cfa3beb7-266a-49de-aaba-dd681716dc75 (C4, insidious ~4 weeks, no arm weakness);
  0a7f2022-ff9e-4a61-aa25-1e4d627b0a66 (C1).
- Decisions: course 2 weeks to presentation with clear progression and nadir now; the "week 3"
  reflex time point becomes "today"; add mild arm weakness (shoulder abduction 4+/5, grip 4+/5) and
  reduced arm reflexes. NCS: delete "asymmetric left greater than right" (symmetric). PE: "relative
  caution (infection risk with central access, haemodynamic instability); IVIg is the practical
  first choice here" with no "contraindicated"; align pearl 2. a6 required (tacrolimus with IVIg:
  renal function; mycophenolate). Prior serum CMV/EBV PCR stays as dated history.

### RP16 (A) (AMAN during ALL induction)
- Notes: b902ee1c-59e1-43f5-9e02-dd2f3600727e (C13, LP without platelet gate; transfusion step after
  LP); 693830c4-671d-4855-99ba-1d17edef7a68 (C1, FVC 62%/NIF -30 "normal" with legs 0/5, arms 3/5;
  no intubation must; weight).
- Decisions: hard a1 -> a3, `coagulation` in a1; delete the transfusion step. ICU-level must and
  intubation-criteria must. AMAN label stays (NCS meets it: unexcitable motor nerves, normal
  sensory); delete "anti-GM1 / GD1a positive" from the label and the ganglioside follow-up; KCE 1
  rewritten "The pure motor axonal NCS pattern with normal sensory studies defines AMAN". a6
  required (vincristine; L-asparaginase coagulopathy); delete "hold vincristine" management from
  the DDI output (it may say "vincristine neurotoxicity overlaps"). Keep a9 spine MRI optional.

### RS11 (bilateral facial palsy)
- Notes: c1f03f5c-5825-4c73-9861-1a3e3111f6c7 (C4, "no limb weakness" vs 4/5 motor; no sensory
  signs for "bifacial weakness with paraesthesias"); 22430160-f2dc-4969-ad80-707f33b703cf (C2, GQ1b
  1:40 uninterpreted).
- Decisions: make it bifacial weakness with paraesthesias: limbs 5/5, add distal paraesthesias in
  the HPI and mild distal vibration loss, reduced reflexes kept; label "Guillain-Barre syndrome,
  bifacial weakness with paraesthesias variant". GQ1b negative in the C2 follow-up (GQ1b is not the
  marker of this variant). Lyme: add recommended criterion `interpret_labs {'panels':
  ['Lyme_serology']}` (negative). Chest CT follow-up moved to `order_body_imaging` `chest_CT` with
  an optional criterion (sarcoidosis) or deleted; brain MRI follow-up moved to `analyze_brain_mri`
  (recommended; facial nerve enhancement is Kind 2). Delete the editorial "bilateral Bell's palsy is
  rare..." sentence (C7).

### RS12 (A) (AIDP after spinal surgery)
- Notes: bc02717e-84d6-48c6-8e9e-7df79a49237e (C3, single loose stool as trigger; stool culture not
  orderable).
- Decisions: label "Guillain-Barre syndrome (acute inflammatory demyelinating
  polyradiculoneuropathy) after spinal surgery"; the single loose stool is history and named as
  non-specific; delete any stool culture or Campylobacter requirement. Keep a9 spine MRI optional
  (surgical complication RH). DDI output on DVT prophylaxis: keep only as category-level.

### RS13 (severe AIDP after head trauma)
- Notes: d8e03a5d-cbfa-435b-aa48-631f00e62672 (C7/C12, day 2 framing vs day 6-12 data);
  bff624ff-29ed-42e4-a6df-d534121ee014 (CSF protein with 450 RBC from SAH);
  9f5289ae-40c4-43c9-82c8-0b80ecf87a67 (C5, CIP and sepsis not separated).
- Decisions: the assessment is hospital day 2; every output reports day 2 or earlier: telemetry
  first 24 h, respiratory before intubation, no day 5-10 events. CSF: add "RBC 450/mm3; at about
  1 mg/dL protein per 1000 RBC this accounts for under 1 mg/dL of the protein" (Kind 2) so the
  dissociation stands. CIP: very_low with reason "onset on day 2, before the 1-2 weeks of critical
  illness CIP needs"; fever 37.9 and WBC 19.2: RH "Leucocytosis and low-grade fever after trauma and
  crush injury" resolved by the absent infective source and the CSF; keep CK 20,518 as crush injury
  with "rhabdomyolysis" in the differential low (areflexia and demyelinating NCS). Keep a9.

### RS14 (classic AIDP, recent vaccine)
- Notes: 682b32b6-3e9e-4445-a841-7e6e80c4d080 (C9, head CT unindicated); 261fe3e8-852a-437b-8501-ffefd465163e
  (C10, a1 expects leukocytosis and trigger serology not in the case); 682d7003-ed74-4dfd-95e5-b48a7d770687
  (C6, influenza vaccine after onset as red herring).
- Decisions: delete the head CT follow-up; canonical a1. RH "Seasonal influenza vaccine 4 days ago:
  weakness began 7 days ago, so the vaccine followed onset and is not the trigger; the pneumonia 3
  weeks ago is the likely antecedent". Ganglioside follow-up deleted.

### RS15 (isolated bulbar presentation)
- Notes: 98e9377c-e0d0-4bf6-8007-28afb8fdb3b0 (C4, 5/5 limbs, reflexes 2+, no polyneuropathy; pearl 2
  false); 7fcdfb5c-5437-4e9a-bdf6-5ca43ce03ea9 (C5, MG high unexcluded);
  b578810b-e5f5-41d9-a0f8-cf6df20c6bbf (C5, weight loss, anaemia, albumin 2.9 without neoplastic
  differential; prior episode 3 years ago).
- Decisions (open question 1): make it PCB: add neck flexion weakness and proximal arm weakness
  (shoulder abduction 4/5) with absent arm reflexes, legs normal with reflexes preserved; label
  "Guillain-Barre syndrome, pharyngeal-cervical-brachial variant (anti-GT1a positive)" with GT1a in
  the C2 follow-up; NCS: delete "positive sharp waves in thoracic and lumbar paraspinal muscles"
  (that is a motor neuron disease pattern) and describe upper-limb involvement. Pearl 2 rewritten
  (bulbar reflexes do not distinguish GBS from MG; areflexia in weak arms and normal RNS do). MG:
  recommended `anti_AChR`, `anti_MuSK` lab criterion (negative) and `ice_pack_test` optional;
  RNS of facial and trapezius in the NCS report; MG low. Weight loss: reduce to what 2 weeks of
  dysphagia explains (for example 4 kg), albumin and haemoglobin consistent with poor intake; add
  "Malignancy (paraneoplastic bulbar syndrome)" low with an optional `chest_abdomen_pelvis_CT`
  criterion or a reason. Prior episode: keep, add "Recurrent GBS or autoimmune nodopathy" low to the
  differential; optional `anti_NF155`, `anti_CNTN1` lab criterion. Brain MRI follow-up moved to
  `analyze_brain_mri` (recommended; prior stroke, brainstem differential).

### RS16 (severe AIDP after MI and PCI)
- Notes: 72d65aba-ba1c-4a4a-a449-dcef1c6d1585 (MRC 54/60 vs quadriplegia);
  10c8e5fc-f42c-4caa-b1f6-b277f911f261 (C5, HIT moderate without platelets or heparin data;
  procalcitonin and CRP uninterpreted).
- Decisions: MRC sum score consistent with quadriplegia (for example 14/60). HIT: CBC shows a
  normal platelet count with no fall; lower HIT to very_low with reason, or delete it. Procalcitonin
  1.69 and CRP 28.4: RH "Raised procalcitonin and CRP after MI and PCI: post-procedural
  inflammation; no infective focus; CSF acellular". Initial NCS: a bedside NCS that was performed
  (use the current repeat-NCS content as the initial output; delete "not performed" and the repeat
  follow-up). Delete "LP eventually performed. Multiple ganglioside antibodies positive" and the
  family-refusal sentence (C7); label without "multi-antibody positive". Respiratory: report the
  pre-intubation values. a6 required, hard a6 -> a3 and a1 -> a3 (apixaban, aspirin, ticagrelor;
  lisinopril with PE); delete "PE contraindicated" (relative caution); telemetry first 24 h without
  "metoprolol held".

### RS17 (severe AIDP after Mycoplasma pneumonia, encephalopathy at onset)
- Notes: dfea15bf-7e8c-4f20-9a07-854630c3101f (C5/C6, fever, confusion to unresponsive, neck
  rigidity, asymmetric facial and arm signs unresolved; no RH); 86ecf008-a989-4553-b0d0-9215a82c22b3
  (C5, encephalitis/ADEM moderate without brain MRI, listed waste, and without EEG).
- Decisions: add `analyze_brain_mri` as a required criterion (encephalopathy with fever) with a
  normal or non-specific follow-up, and `analyze_eeg` recommended (diffuse slowing, no epileptiform
  activity); remove both from waste. Encephalitis/ADEM lowered to low after normal MRI and acellular
  CSF; add "Bickerstaff brainstem encephalitis / GBS overlap" low. RH block: "Fever and confusion
  at onset: sepsis-associated encephalopathy from pneumonia, resolved with treatment; CSF acellular
  excludes meningitis"; "Neck stiffness: no meningitis on CSF"; "Asymmetric facial droop: facial
  involvement in GBS can be asymmetric". Mycoplasma IgM deleted from labs (C3); antecedent stays as
  the clinical pneumonia; delete the "Mycoplasma serology and PCR" must. a6 required (azithromycin
  with QTc 464; levofloxacin given earlier); the DDI output reports the QT interaction, no
  "switch to doxycycline" instruction. Telemetry first 24 h; respiratory pre-intubation values.

### RS18 (A, no notes) (severe AIDP with ophthalmoplegia and cord signal)
- Decisions: class fixes only: placeholder ECG follow-up (C9), empty DDI follow-up, literature
  optional (Bell palsy literature follow-up may stay as the case-specific general output),
  respiratory pre-intubation (already partly), telemetry first 24 h, ganglioside follow-up kept per
  C2 (ophthalmoplegia; results negative). The must "Brain and cervical spine MRI" needs a brain MRI:
  add `analyze_brain_mri` recommended with a normal follow-up, or reword the must to the spine MRI
  only. The must "Send anti-AQP4 and anti-MOG": add a recommended criterion `interpret_labs
  {'panels': ['AQP4_IgG_cell_based', 'MOG_IgG_cell_based']}` with negative results. Keep a9.

### S01 (A, no notes) (severe post-Campylobacter AIDP)
- Decisions: class fixes only: delete spirometry and "AT INTUBATION THRESHOLD" from the patient
  block and HPI (C1/C7; the HPI's FVC sentence goes), weight consistent with 22 mL/kg (about 82 kg)
  in physical_exam.general, delete Campylobacter serology and the ganglioside follow-up (the prior
  culture stays as history; label keeps "after culture-confirmed Campylobacter enteritis"), telemetry
  first 24 h, NCS structured field "risk of secondary axonal injury with anti-GM1" deleted.

### S02 (A) (severe AIDP after URI)
- Notes: 4021807f-930a-4d1a-87c6-f44df643af6a (C3, antecedent unresolved; EBV IgM positive called
  "none"; trigger identification required but impossible).
- Decisions: delete EBV IgM from labs; delete the trigger-identification requirement; antecedent is
  the URI history; delete the GD1b ganglioside follow-up; "FVC at triage 1.6 L" out of the HPI.

### S03 (A) (severe AIDP after bloody diarrhoea)
- Notes: 3c94e91e-ec7a-4812-8d8a-81013bf1c4dd (C3, precipitant asserted but not tested).
- Decisions: HPI "consistent with Campylobacter (no stool culture obtained but presentation
  classic)" becomes "a bloody diarrhoeal illness 3 weeks ago (no stool culture obtained)"; label
  unchanged (no organism named); delete Campylobacter serology and the ganglioside follow-up; add arm
  strength to the motor exam (consistent with the severity, for example shoulder abduction 3/5, grip
  3+/5); respiratory pre-intubation values (no "post-intubation" FVC); telemetry first 24 h without
  pacing or nitroprusside; literature output general (no case-specific prognosis figures).

### S04 (A) (severe AIDP after influenza A)
- Notes: e48d42bd-8ab5-4cc3-a053-396b3ef2bc40 (C3, positive influenza PCR now means active infection;
  T 37.4, WBC 12.2; no antiviral or isolation).
- Decisions: date the swab to the earlier illness: HPI "URI 2 weeks ago; influenza A PCR positive at
  his GP practice at that time"; delete the PCR from the current labs; WBC 12.2 stays with the
  stress response explanation or is lowered. Label keeps "after influenza A". DDI: the
  succinylcholine warning stays (well established) with a category-level wording; metoprolol only if
  autonomic bradycardia is in the case.

---

## 5. CENTRAL requests

1. **Vocabulary (costs.yaml, tool_io mirror, fallback library):** add `anti_GQ1b_IgG` and
   `anti_GT1a_IgG`, or one `anti_ganglioside_panel` (GM1, GD1a, GD1b, GQ1b, GT1a, IgG and IgM), to
   `interpret_labs`. Needed for P01, RM12, RM15, RS11, RS15, RS18 criteria (BLOCKED until then).
   Consider whether `anti-GM1 IgM` (a multifocal motor neuropathy test) should stay.
2. **Vocabulary:** antecedent-infection tests are not orderable (Campylobacter serology, stool
   culture, CMV IgM and PCR, EBV, Mycoplasma serology and PCR, influenza PCR). The guideline does not
   require them for GBS; the round removes them from cases. Decide whether a `stool_culture` term
   (in `order_microbiology`) and a `Mycoplasma_serology` term are wanted for other conditions.
3. **Vocabulary:** `botulinum_toxin_assay` (serum and stool) for the botulism mimic (RM12, RS15,
   S01 differentials); until then botulism is lowered by clinical reasons.
4. **Vocabulary:** CSF `CMV_PCR` in `analyze_csf` special tests (HIV, transplant: P02, RP15).
5. **Schema:** a `weight_kg` (and `height_cm`) field in demographics; respiratory mL/kg and IVIg
   dosing depend on it. Until then weight goes in `physical_exam.general`.
6. **Synonyms (diagnosis_synonyms.yaml):** every GBS case accepts "acute motor axonal neuropathy",
   "AMAN", "miller fisher syndrome" and "AIDP" for G61.0, so a typical AIDP case accepts "Miller
   Fisher syndrome" and the MFS case accepts "AIDP". Decide whether variant labels should be
   accepted only in the matching cases (per-case accepted list) or kept as code-level acceptance.
7. **Criteria pack `dataset-generation/criteria_packs/GBS.md`:** align with this plan: EAN/PNS 2023
   as governing source; the 20/30/40 rule as FVC <20 mL/kg, MIP weaker than -30, MEP <40 (the pack
   and the a4 template say "VC <40% predicted", which is wrong); ganglioside testing only for MFS
   and PCB; no antecedent serology or stool culture in the required work-up; literature optional,
   DDI conditional; allowed citations per section 1.1.
8. **conditions.yaml `guillain_barre` common_followups:** `request_respiratory_monitoring` is listed
   under `interpret_labs` and `request_spine_mri_contrast` under `order_advanced_imaging`; correct to
   `order_specialized_test` and `order_body_imaging`.
9. **Fallback library:** the `respiratory_function` normal report format should carry FVC L, %
   predicted, mL/kg, MIP, MEP so that any generated report follows C1.
10. **Tests/CI:** a check that fails when an `order_specialized_test` respiratory output says "All
    values within normal limits" with FVC below 80% predicted, or flags a low value "(H)"; a check
    for the leaky clinical_significance sentence "which is what this case's diagnosis rests on"
    (29 GBS cases; probably other conditions too).
11. **Followup matcher:** the generic trigger `request_anti_ganglioside_panel` shares no meaningful
    token with `anti-GM1 IgM`; once CENTRAL 1 lands, make sure the new term's tokens match the
    renamed trigger.
12. **Review UI:** show the weight line and the respiratory change sentence prominently in the
    respiratory step; display followups in criterion order (already done in commit 048571f9 for
    the initial work-up).

---

## 6. Open questions for Andrea

1. **RM15 and RS15 diagnosis.** Reviewer 2 allows "add deficits, a positive antibody, or change the
   diagnosis". The plan keeps G61.0 and edits the cases (RM15 to an anti-GQ1b acute ptosis
   presentation; RS15 to PCB with arm involvement). Alternative: relabel RM15 as ocular myasthenia
   and RS15 as an MG or motor neuron disease case, which would move them out of GBS. Confirm the
   edit route.
2. **ICU threshold FVC <60% predicted.** Reviewer 2 states it (note 2a09feee); the published
   triggers are absolute (FVC <20 mL/kg, MIP, MEP, >30% fall). The plan applies both. Confirm that
   <60% predicted stays a hard trigger in the scoring text, or only a reason for closer monitoring.
3. **IgA before IVIg.** The cases prohibit IVIg "without checking IgA". Current practice and
   EAN/PNS 2023 do not require routine IgA screening; the plan rewrites the prohibition to renal
   function only and does not add IgA to a1. Confirm, or keep IgA as a recommended test.
4. **RP11 ICI-GBS doses.** ASCO 2021 and ESMO 2022 advise IVIg or PE with methylprednisolone (ASCO
   gives 2-4 mg/kg/day or a pulse of 1 g/day for 5 days). The plan writes the must without a dose.
   Confirm whether a dose should be scored.
5. **RM14 breastfeeding source.** LactMed (immune globulin, plasma exchange) is the intended source
   for "breastfeeding can continue". Confirm LactMed may be cited as a key (`[LactMed]`), or drop the
   statement to "review co-medications for lactation safety".
6. **HIV in the baseline labs.** The plan removes HIV from the required lab args (EAN/PNS lists HIV
   only where risk). This changes 29 cases. Confirm, or keep HIV as recommended in all.
7. **Subtype labels.** EAN/PNS advises against routine electrodiagnostic subtyping. The plan keeps
   subtype words in labels only where the NCS meets them (for example RP16 AMAN, most cases AIDP).
   Confirm, or strip subtype words from all labels for uniformity.
