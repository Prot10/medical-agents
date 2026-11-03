# ALS: October 2026 review round, condition summary

Condition audit, 23 Oct 2026 (first pass by the ALS lead, second pass by the condition auditor on
retry). Scope: the 30 ALS cases (M01-M08, P01-P09, RM11, RS11, S01-S11), the plan `plans/ALS.md`,
`PATTERNS.md`, the 30 logs and `notes/ALS.json` (245 notes, all from R1; R2 has not reviewed ALS).

## Checks (re-run after the second pass)

- `perfect_agent.py` on all 30 ids: 30/30 pass.
- `case_io.py check` on all 30 ids: schema OK for all 30, synonym guard OK. Two tests fail in the
  suite; case_io reports that no failure names an ALS case (other conditions are mid-edit).
- Scripted uniformity checks across the 30 cases (scripts re-written for this pass, not reused).
  Everything below holds, or differs only by a deviation documented in the case log:
  - criterion order and tiers (plan 3.1), `alternatives` and `required_arguments` (brain MRI `{}`,
    spine `{"study": "spine_MRI"}`, lab core `CBC, CK, TSH, vitamin_B12` plus the case analytes,
    M04 with three paraneoplastic alternatives), canonical labels, rationales and citations;
  - follow-up order (respiratory, genetics, riluzole; P02 and P08 without riluzole); no literature
    follow-up; `initial_tool_outputs.literature_search` and `drug_interactions` null; CSF only in
    M04, M08, P03, P05 and P06;
  - the two soft sequence constraints with canonical reasons and citations (constraint 1 only in
    P02 and P08); stop rule (action-3 to action-6, `max_additional_actions` 0); eight waste avoided
    actions (P09 has 7 and S11 has 5, both logged as open questions);
  - respiratory output: reference ranges (FVC >=80%, SNIP >=70 men / >=60 women, MIP/NIF -60 cmH2O
    or more negative), `is_abnormal` recomputed from each row's range, impression by category;
  - MUST-RILUZOLE, MUST-MDT, MUST-GEN (sporadic), MUST-RESP by category, MUST-BULBAR by variant,
    PROHIB-IMM, PROHIB-RESP, PROHIB-SWALLOW only in dysphagia cases, PROHIB-SURG cervical/lumbar
    and PROHIB-FUNC exactly in the plan's case lists;
  - K-EMG verbatim; K-CK band and ratio match the stored CK/ULN in every case, and the lab
    interpretation gives the same ratio; K-NCS reduced-sural variant in M02, M05, S06 (M08 has its
    own sural pearl); respiratory, CK and medicine values quoted in musts, pearls and expected
    evidence match the stored reports;
  - lab panels: core panels present, numeric values except qualitative antibody results, no
    duplicate analytes, `is_abnormal` agrees with every numeric range, no ALS or mimic named in
    the interpretation;
  - genetic output: five genes reported, canonical negative impression in every negative case (M01's
    also names UBQLN2 and VCP);
  - differentials: target and ALS phenotypes absent, no Kennedy entry in women, no untested
    anti-GM1 or CAG-repeat claim (P08 states the CAG repeat was not tested), no `high` likelihood
    left in a confirmed-ALS case;
  - red-herring `field_path`s resolve; the riluzole output lists every patient medicine;
  - brain and spine reports region-pure, spine `region` includes lumbosacral where lumbar levels
    are described, no enhancement claim in a non-contrast spine study;
  - pronoun/sex and age consistency in ground truth and reports; no "or SBMA" or gynaecomastia in
    women;
  - banned strings absent everywhere: AMX0035, Relyvrio, edaravone, grapefruit, "July 2026",
    El Escorial, "2-5x", "Exclusion studies", "Reviewer baseline", "Rule-out studies", "Mimic
    exclusion", lymphopenia, JSON dumps, "Pulmonary function testing recommended" (S07's only
    "serotonergic" hit is the correct negative statement);
  - HPI and chief complaint: no result of a scored study, no "pending"/"ordered" sentences; ALS is
    named only as a family history or the patient's fear (P01, P02, P07, P08, S07, S08, S10).
- Note coverage: all 245 note ids appear in exactly one log, the log of their own case, each in
  one table row with a ruling.

## Error classes and how each was fixed (plan C1-C17, plus the auditor classes)

- **C1 Pathway order.** In every case the action criteria were reordered into diagnostic order:
  EMG, brain MRI, spine MRI and labs (required), then the post-diagnostic steps: respiratory
  (recommended), the genetic panel (optional, or recommended in P02, P08, P09 and S10) and the
  riluzole check (recommended; required in M06, optional in P01, deleted in P02 and P08). Two
  soft constraints were added: EMG before genetics and EMG before the riluzole check. The
  follow-ups were reordered to match.
- **C2 Literature as a clinical step and a scoring echo.** The literature criterion and every
  literature output were deleted in all 30 cases; the initial literature block is null. The
  clinical content of deleted consult-like searches became musts or prohibitions (M05 lumbar
  surgery, P01 repeat EMG, P02/P08/S10 genetic counselling).
- **C3 Drug-interaction check.** Now the last step, after the diagnosis. AMX0035/Relyvrio,
  edaravone, tofersen, trial enrolment, grapefruit and the wrong mechanisms (levothyroxine,
  metformin, caffeine, warfarin, serotonergic, QTc, natalizumab "lymphopenia") were removed. Each
  output was rewritten for the case's own medicines with the SmPC LFT schedule, the 5x ULN stop
  threshold and the neutropenia warning; the case-specific points of plan C3 are present.
- **C4 Respiratory treated as diagnosis.** Recommended staging, never required (optional in P02,
  P08). Canonical references (SNIP 70 men, 60 women; MIP/NIF -60 cmH2O), impressions by category,
  MUST-RESP and PROHIB-RESP by category. First-pass auditor fix: 18 cases had no `is_abnormal` on
  their respiratory rows (M01-M06 used a `flag` key; M07, M08, P01-P04, S06-S11 had none); all 30
  now carry it, computed from each row's range, values and impressions unchanged.
- **C5 Genetic panel.** All five genes reported with the canonical negative impression or the
  case's positive result (P02 and P09 C9orf72, P08 SOD1 A4V, S10 C9orf72). Optional with
  counselling, recommended in the familial cases. M01 keeps UBQLN2 and VCP in addition.
- **C6 EMG/NCS report.** Impressions restated from the findings, motor NCS added with named
  nerves where missing, "No conduction block" stated in every impression, the "PFT recommended"
  cross-step hint removed. Workers and verifiers removed chronic-change overclaims (thoracic or
  bulbar regions where only fibrillations or fasciculations were recorded) in the EMG impressions
  and EMG expected evidence of M01-M06, RS11, S01-S11.
- **C6b (auditor, second pass) LMN regions in MUST-DX and K-GC.** The S-series and RS11 verifiers
  had narrowed MUST-DX and K-GC to the regions where lower motor neuron dysfunction is shown
  (clinical weakness and wasting, or EMG chronic change plus active denervation, Gold Coast 2020),
  naming the rest as "active denervation also in ...". Fourteen cases still claimed regions,
  mostly thoracic, on fibrillations alone: M02, M03, M04, M05, M06, M07, M08, P03, P04, P05, P06,
  P07, P09 and RM11. The same wording is now used in all 30 cases (28 field edits, no stored
  result changed, Gold Coast still met in each; M03's "clinically definite" still holds). Logged
  under "Condition audit, second pass" in each of the 14 logs. M01 keeps four regions (thoracic
  MUP abnormality and lumbosacral reduced recruitment are recorded).
- **C7 Diagnosis overcalled.** P01 relabelled "possible ALS by Awaji criteria" and P08
  "Suspected early ALS ... Gold Coast criteria not yet met" (both G12.21); P02 relabelled
  thyrotoxicosis from levothyroxine over-replacement in a C9orf72 carrier (E05.90). M03's EMG
  "definite" region wording removed. See CENTRAL 3 and Q1/Q2.
- **C8 Differential not updated.** Mimics excluded by the work-up lowered with case-data-only
  `key_features`; ALS phenotypes (progressive bulbar palsy, flail arm, LMN-predominant) and the
  target removed; Kennedy removed in women; mimics the case raises added (statin myopathy in M02,
  S01, S08; residual Graves in P02; lumbar radiculopathy; Kennedy very_low in P04 with the CAG
  repeat tested).
- **C9 CK above 5x ULN.** K-CK by ratio; the >5x pearl (with statin context on atorvastatin) in
  M02, M07, P04, RS11, S01, S08, S10; lab interpretation states the ratio.
- **C10 Safety and supportive musts.** Rebuilt from the canonical set (MUST-DX, RESP, BULBAR,
  RILUZOLE, case medicine musts, MDT, GEN; PROHIB-IMM, RESP, SWALLOW, SURG, FUNC) with the
  documented case adaptations (M03 and P09 put swallowing before respiratory per the reviewer's
  "early safety" request; P01, P02, P08, S10 have their own sets).
- **C11 Narrative leaks and contradictions.** Results of scored studies, "pending"/"scheduled"
  sentences, reasoning sentences and diagnosis-naming phrases removed from HPIs and exam
  summaries; M04 paraneoplastic and P06 anti-MAG now reported in the labs.
- **C12 Imaging mixed between brain and spine.** Reports separated and renumbered, JSON dumps
  replaced, spine region widened where lumbar levels are described, P07 anatomy corrected
  (conus and cauda equina ventral roots), gadolinium stated where the case raises a
  leptomeningeal, MS/PML or HIV question (brain M04, M08, P05, P06; spine M04, P05), red-herring
  paths corrected.
- **C13 Lab structure and leakage.** Canonical panels with numeric values; engineering text
  removed; case analytes added (anti-GM1 IgM in P03, CAG repeat in P04, HIV RNA and CD4 in P05,
  SPEP/IFE/FLC/anti-MAG in P06, paraneoplastic in M04, blood lead in M07, TSI in P02, INR in S08).
- **C14 Templated pearls.** Rebuilt from K-GC, K-EMG, K-NCS, K-CK, K-RESP, K-SPINE, K-BULBAR and
  case pearls. First-pass auditor fix: "or SBMA" removed from the K-NCS pearl in the 8 women's
  cases that carried it (M01, M04, P05, P07, S02, S04, S07, S09).
- **C15 Red herrings.** Reframed as confounders with correct field paths; S07 anxiety and P02
  carrier-status red herrings added.
- **C16 Criterion mechanics.** Brain MRI `{}`, spine `spine_MRI`, lab vocabulary spellings,
  bracketed allow-list citation keys, labels separate from rationales. First-pass auditor fix:
  M01 brain MRI rationale punctuation.
- **C17 Template carry-over.** M01 Kennedy entry and "no gynecomastia" removed, M06 husband moved
  out of family history, M03 NfL metadata claim reworded. Repeated values (ESR 8, CRP 2, B12 420,
  folate 10; CK 920 in M02, S01, S08; CK 1240 in RS11, S10) kept per plan and flagged.

## Counts

| item | count |
| --- | --- |
| Reviewer notes (all R1) | 245 |
| FIXED | 245 |
| ALREADY-FIXED | 0 |
| DECLINED | 0 |
| BLOCKED | 0 |
| Own findings in the workers' tables: FIXED | 407 |
| Own findings in the workers' tables: FLAGGED | 28 |
| Verifier findings fixed (Verification sections) | 26 |
| Auditor findings fixed, first pass | 3 classes, 27 field edits in 22 cases |
| Auditor findings fixed, second pass | 1 class (C6b), 28 field edits in 14 cases |
| Auditor findings flagged | 2 (waste-action citation; pre-round em dashes in P01 and P04 EMG text) |
| Cases changed | 30 of 30 (25 also touched by the condition audit) |
| Approved cases changed | 0 (no ALS case was approved before this round) |

## DECLINED and BLOCKED notes

None. All 245 R1 notes were ruled FIXED. The one place where a ruling could not be completed
inside the case file is P02's synonym list (CENTRAL 3): the label and `icd_codes[0]` are changed,
but the appended G12.21 synonyms still let a plain "ALS" answer score as correct until the central
synonym change is made.

## Auditor flags (not changed)

- All eight waste avoided actions cite `[AAN_2009]` in all 30 cases. AAN 2009 covers NIV,
  gastrostomy and riluzole, not diagnostic waste; `[EFNS_ALS_2012]` fits better. Plan 3.2 keeps
  the avoided actions unchanged, so this is left for one central edit (CENTRAL 8).
- P01 and P04 EMG findings carry em dashes in stored text from before this round (P01 also in
  its EMG impression); patient blocks in many cases carry pre-round em dashes too. Left alone to
  avoid churn; no new em or en dash was added this round.

## CENTRAL requests (consolidated)

1. **Review UI.** Show `initial_tool_outputs` and `followup_outputs` together in criterion order,
   so the core work-up (EMG, brain MRI, spine MRI, labs) reads as steps 1-4. All 79 pathway notes
   depend on this for display.
2. **Criteria pack `dataset-generation/criteria_packs/ALS.md`.** Section 6: respiratory is
   recommended staging, not required; remove the literature step; genetics optional with
   counselling, recommended in familial cases. Section 8: add `[EFNS_ALS_2012]`,
   `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]` and `[Bourke_2006]`
   (already used in the cases).
3. **Diagnosis synonyms.** P02: strip the appended G12.21 labels ("amyotrophic lateral
   sclerosis", "ALS", "motor neuron disease", "motor neurone disease", "MND") and codes (G12.2,
   G12.20, G12.23, G12.24, G12.25), which `apply_diagnosis_synonyms.py` cannot remove; add an
   E05.90 entry restricted to `conditions: [als]` (e.g. "thyrotoxicosis", "levothyroxine
   over-replacement"). P01 and P08 need no synonym change.
4. **Lab matching and vocabulary.** Make `_contains_required` use `normalize_analyte` and
   `_ANALYTE_SYNONYMS` so paraneoplastic/paraneoplastic_panel, LFT/LFTs and CMP vs BMP plus LFTs
   compare equal; add `HIV_viral_load` and `CD4_count` to `interpret_labs` (P05 reports them
   inside "HIV").
5. **MockServer guard.** A test that a stored literature or interaction output never contains a
   criterion's `expected_evidence` (the initial blocks are served for any query or drug).
6. **Fallback library.** Check that the general literature output does not cite El Escorial as
   current or name AMX0035.
7. **Tests.** A banned-string test for ALS cases (AMX0035/Relyvrio, grapefruit as a CYP1A2
   modulator, "July 2026 review", El Escorial as current, "or SBMA" in women); update the
   `test_guidance_claims` tier counts for the new ALS tiers.
8. **Waste-action citations.** Replace `[AAN_2009]` with `[EFNS_ALS_2012]` on the eight waste
   avoided actions across the condition in one central edit, if agreed.
9. **Metadata.** `metadata.revision_reason` template text ("targeted CSF/labs") should be
   refreshed centrally (metadata only, not shown or scored).

## Open questions for Andrea (consolidated)

Condition-wide (plan section 6):

- **Q1. P02.** Keep P02 in `als` as a mimic case labelled thyrotoxicosis from over-replacement in
  a C9orf72 carrier? Should an answer naming both ALS and thyrotoxicosis count as correct? E05.90
  alone, or with T38.1X5A? (The verifier notes that 100 mcg levothyroxine is not a high dose, so
  residual Graves activity, now a low differential, is a real alternative.)
- **Q2. P08.** Keep G12.21 with "suspected early ALS, criteria not yet met", or code carrier
  status (Z15.89), which would make "ALS" a wrong answer?
- **Q3.** Confirm the literature criterion is removed in all 30.
- **Q4.** Keep -60 cmH2O as the MIP/NIF limit for both sexes as a dataset convention? It drives
  S11's AAN-marker category (NIF -52 with FVC 80% and SNIP 68).
- **Q5.** Keep EMG, brain MRI, spine MRI and labs in `initial_tool_outputs`, relying on the UI fix?
- **Q6.** Drug-interaction check required only in M06; M03 (alcohol) and M04 (tamoxifen) stay
  recommended. Agree?
- **Q7.** Genetics optional in sporadic, recommended in familial cases. S10 and P09 have
  C9orf72-dependent musts with only a recommended panel: should the panel be required there?
- **Q8.** Should the 25 cases without a CSF indication list `analyze_csf` as waste?
- **Q9.** P01: riluzole deferred to confirmation at 3 months although Gold Coast is met, and the
  repeat EMG is a must, not a criterion (same repeat-EMG question in P08).
- **Q10 (new, second pass).** Confirm the region rule now used in all 30 MUST-DX and K-GC texts:
  a region counts for lower motor neuron dysfunction only with clinical weakness and wasting or
  EMG chronic change plus active denervation; fibrillations alone are named as "active
  denervation also in ...". Tongue atrophy with fasciculations is counted clinically (M04, M07).

Case-level judgement calls:

- **Labels.** M07 "probable progressing to definite": no study documents the progression;
  suggest dropping "progressing to definite".
- **Musts and prohibitions added beyond the plan (keep or drop?):** musts M05 falls, S08 INR;
  prohibitions P06 rituximab, P07 PPS anchoring, P09 FTD anchoring, S06 diabetic neuropathy.
- **Musts possibly missing:** M04 share the diagnosis and LFT plan with oncology; M02 statin
  pause and CK recheck; RM11 alcohol; RS11 cognitive/behavioural screening and pseudobulbar affect;
  S05 bulbar must for subclinical bulbar involvement; M03 apixaban interruption around
  gastrostomy; P04 liquid riluzole.
- **Changed stored values (confirm):** sural SNAPs lowered in M02 and M05 to match "mildly
  reduced" (one sural wording for M02, M05, M08, S06?); P03 "possible partial conduction block"
  added to the earlier EMG history; S10 motor NCS without numbers and a myopathy differential;
  S11 spine level findings, motor NCS, a skull-base negative and a second red herring; S06 and
  S07 MUP data added so the findings support the impression.
- **M08 respiratory.** FVC 78% reduced, SNIP 60 at the women's limit; "reduced" must kept with
  adapted wording.
- **EMG chronic change in RM11 and P09** is claimed only in the hand muscles; add MUP data
  elsewhere if a four-region chronic picture is wanted.
- **P03.** Is the repeat anti-GM1 drawn on IVIG interpretable? The case does not rely on it.
- **P05.** HIV background (undetectable, CD4 above 500) stays in the HPI while current values are
  a lab criterion.
- **P07.** Accept the conus and ventral-root wording instead of "cauda equina signal", and the
  reading of the earlier EMG as confined to the left leg.
- **Avoided actions.** P09 has 7 waste items (no ECG; adding it needs a fallback ECG report).
  S11 has 5 (no amyloid PET, DaTscan or FDG-PET; FDG-PET is arguable with a cancer history).
- **Thin HPIs.** S03, S04 and S05 have no MRC grades and no bulbar or weight history.
- **S09.** "Hypoglossal nuclei T2 signal" is not an established MRI sign; consider deleting it.
- **M01.** UBQLN2 and VCP kept in the genetic output beyond the five-gene panel.
- **Template carry-over values (ESR, CRP, B12, folate, CK).** Keep, or vary in a later pass?
- **Spelling.** Canonical texts are British (orthopnoea, counselling, haemorrhage) and some reports
  American; cosmetic.
