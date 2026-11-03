# FTD: round 2026-10 summary

Condition auditor, 24 Oct 2026. Scope: 30 cases (M01-M10, P01-P08, S01-S12), plan `plans/FTD.md`,
logs `logs/FTD-*.md`. FTD has no notes file, so no reviewer note id applies; every case log records
"Reviewer notes: none".

Final state: `perfect_agent.py` 30/30. `case_io.py check` is clean: schema and synonym guard OK, and
none of the 15 failures in the wider suite names an FTD case. `test_case_guards.py -k FTD` passes
(60 tests). The 26 case logs this audit touched end with a "Condition audit (FTD auditor, 24 Oct 2026)"
entry that lists what changed and why.

## 1. Error classes and how each was fixed

| class | defect | fix applied (workers and verifiers) |
| --- | --- | --- |
| C1 | Literature search required, echoing the answer ("Confirms Rascovsky 2011 criteria ..."), management essays as follow-ups | Optional, last, out of the stop rule in all 30 cases; canonical general text per syndrome (bvFTD; familial, AD-versus-FTD, psychiatric-mimic and FTD-MND variants; svPPA; nfvPPA); essay follow-ups deleted |
| C2 | Drug-interaction outputs wrong; the tool used for levels and plans | Kept only where a concrete interaction exists (all optional; M08 recommended); outputs rewritten without ChEI or plan text; levels moved to `interpret_labs` (M05 lithium, P01 valproate and ammonia) |
| C3 | Auto-generated clinical assessment contradicting the history | One finding per Rascovsky feature, then informant, bedside screen and functional decline; `criteria_met` agrees with the findings; canonical impression; Gorno-Tempini keys in S11 and S12 |
| C4 | Templated labels and rationales | Canonical labels; case-specific rationales and expected evidence; bracketed citation keys only; `[AAN_dementia_2018]` retired |
| C5 | Labs incomplete, padded, with the `Reviewed_FTD_panel_additions` leak | Canonical baseline panel (CBC, CMP, TSH, B12, folate, ESR, CRP) with values kept; extras (RPR/HIV, levels, copper, progranulin) in keyed follow-ups; eGFR recomputed |
| C6 | Fallbacks contradicting the case | Advanced-imaging and unspecified drug fallbacks deleted; CT and MRI fallbacks consistent with the case |
| C7 | Functional-imaging tier | FDG-PET recommended in P01, P02, P05 and P07 (plan Q2); optional elsewhere; perfusion SPECT declared and authored as the alternative |
| C8 | Copied "mild bilateral upper-extremity rigidity" red herring | Removed with its KCE and red-herring entry where the case did not use it; kept and made consistent (no tremor, no bradykinesia) where it did |
| C9 | Template musts, or musts presuming an optional result | Case-specific musts (4-6; P08 has 7, explained in its log); none depends on an optional result |
| C10 | Overstated ChEI and memantine prohibitions | Canonical texts in 30/30 (no benefit, NICE NG97, behavioural worsening only for ChEIs) |
| C11 | Differential not at assessment time | Likelihoods use only results the required pathway returns |
| C12 | KCE and notes citing results that do not exist | Rewritten; no amyloid claim without an amyloid result |
| C13 | Truncated or templated neuropsychology impressions | Complete impressions with the canonical ending; battery values consistent with the impression |
| C14 | "No primitive reflexes" against a recorded snout or grasp reflex | Contradicting phrase removed; reflexes on the reflex or additional line |
| C15 | Missing sequence constraints | Soft only: MRI before CSF, CT before MRI (M09), EMG before genetics (P08), clinical assessment before genetics wherever a genetics criterion exists |

### Stragglers fixed by this audit (all through `case_io`)

- **Bedside screen results in the examination** (18 cases: M01-M06, P03-P08, S01-S06). These cases
  kept the MoCA, MMSE or FAB totals, item losses, fluency counts and clock or pentagon results in
  `patient.neurological_exam.mental_status`. Those are the results of the required
  `perform_clinical_assessment` (ROUND_POLICY timeline-leak rule). The other 12 FTD cases, and
  VASC-DEM and ALZ-EARLY, had already moved them out. Removed; the behavioural observations, insight
  and frontal signs stay. Every removed value is already in the clinical assessment output. This
  settles the six FLAGGED worker rows in S01-S06.
- **ALS gene panel contradicting the case** (M02, P01, S03, S05, S10). An order of
  `genetic_panel:ALS` fell to the library, which reports a normal C9orf72, against the case's
  authored expansion. Added follow-up `request_als_gene_panel_c9orf72` with the same expansion and
  SOD1, TARDBP and FUS negative, as P04 and P05 already had.
- **M06 known GRN carrier**: an FTD panel order returned the library's normal panel. Added
  `request_ftd_gene_panel_known_grn` reporting the known heterozygous GRN c.709-1G>A variant. It is
  not scored.
- **CSF fallback with empty `special_tests`** (M03, M05, M06, P03, P04, P05, P06, S11). It answered
  any CSF order without a stored result, so the ordered assays were missing from the report.
  Deleted with its kind key, as in M07, M09, M10, P01 and P02; the library now answers per assay
  (probed).
- **Placeholder literature fallback** ("Recommend correlating with current society guidelines";
  M01, M05, P03, P07, P08, S01): deleted with its kind key, as in the other cases.
- **`metadata.fallback_tool_kinds`** omitted the existing cardiac-monitoring fallback (S03, S05):
  added.
- **Plan C15 MRI-before-CSF constraint** was missing for the AD-biomarker criterion in P03 and P06
  and for `action-csf-opportunistic-pcr` in M08: added, soft, `[NICE_NG97]`, with the existing
  reasons.
- **Literature `source` fields** were citation keys (`[Rascovsky_2011]` or `Rascovsky_2011`) in 25
  cases, three styles across the condition: they now give the full reference, as M07-P02 did.
- **"Hoffman"** corrected to "Hoffmann" (M01, M02, S11, S12).

### Checked uniform, left as is

- Canonical prohibitions are in 30/30 cases. Literature is optional and last wherever present. Each
  stop rule equals its required set, with `max_additional_actions: 0`. Every constraint is soft and
  points to existing ids, and every genetics criterion has the assessment-before-genetics constraint.
- There is no `Reviewed_FTD_panel_additions`, "Confirms Rascovsky", `AAN_dementia_2018` or
  "IMPORTANT CLINICAL NOTE".
- Musts in P05 and P07 are conditional on the FDG result (P01 and P02 were already fixed). MoCA and
  MMSE item sums match the totals where itemised. Drug outputs carry no ChEI text; the P03 dose line
  is a QTc label warning.
- Genetic-counselling musts follow the genetics criterion: familial, onset before about 60, or MND.
  M06 (known carrier) and S11 (behavioural-change counselling) differ for stated reasons.
- Follow-up display order (keyed lab extras after imaging in some cases) was not changed. Order
  matters only for same-tool follow-ups, whose relative order is already correct.
- Pre-existing em dashes in sentences nobody rewrote were left, as were "Clinical correlation
  recommended" in CSF interpretations, the S12 library normal CT, P04 copper in mcg/dL, and the
  S11/S12 speech-language criterion placed before labs.

## 2. Counts

- Reviewer notes: none exist for FTD. FIXED 0, ALREADY-FIXED 0, DECLINED 0, BLOCKED 0.
- Workers' and verifiers' own findings (log tables): 543 FIXED, 8 FLAGGED.
  - 6 FLAGGED: the exam screen in S01-S06, now fixed by this audit.
  - 2 FLAGGED: the S03 and S05 label certainty, plan Q1, still open.
- Condition-audit findings: 9 straggler classes, all fixed, none flagged. They touched 26 cases: all
  except M07, M09, M10 and P02.
- Cases changed in the round: 30 of 30. Approved cases changed: 0, since all 30 are `draft`.

## 3. DECLINED and BLOCKED notes

None.

## 4. CENTRAL requests (consolidated)

1. **Criteria pack** `criteria_packs/FTD.md` (plan 5.1): literature optional and last. Replace
   `AAN_dementia_2018` with `NICE_NG97`, `SNLG_ISS_2024` and `Frisoni_2024`. Add a PPA section
   (Gorno-Tempini features, `speech_language_evaluation`).
2. **Citation keys** to register:
   - `[SNLG_ISS_2024]`, `[Ducharme_2020]`, `[Frisoni_2024]`, `[Strong_2017]`, `[Boxer_2013]`,
     `[Ulugut_2020]`, `[Postuma_2015]` (P04), `[Awaji_2008]` (P08).
   - Optional: `[EACS_2023]` (M08 HIV criteria now carry `citations: []`), `[EFNS_Wernicke_2010]`
     (M07), and an ED key for the M09 toxicology criterion.
   - Confirm that `[NICE_NG97]`, `[ACMG_NSGC_2011]`, `[Amyloid_PET_AUC_2025]`, `[EAN_ALS_2024]`,
     `[NICE_NG42]`, `[AAN_2009]` and `[Gold_Coast_2020]` are registered (P08
     `metadata.citation_gap`).
3. **Synonyms** (`diagnosis_synonyms.yaml`, G31.09):
   - S11 (svPPA) and S12 (nfvPPA) accept bvFTD labels through the code expansion, so a bvFTD answer
     scores as correct. They need per-variant accepted labels ("semantic dementia", "svPPA",
     "semantic variant PPA"; "nfvPPA", "progressive non-fluent aphasia", "agrammatic PPA") and the
     bvFTD labels removed.
   - P08: add "ALS-FTD", "FTD-ALS", "FTD with motor neuron disease", "ALS with frontotemporal
     dementia", "ALS-FTSD", and decide on G12.21 as a secondary code.
   - S09 `accepted[0]` contains an em dash. This is cosmetic.
4. **perfect_agent.py**: exercise every declared alternative (perfusion SPECT, CSF AD markers,
   amyloid PET) and flag answers from the library.
5. **Fallback library**:
   - FDG-PET, perfusion SPECT, amyloid PET and DaTscan default to normal studies.
   - `genetic_panel:FTD` and `genetic_panel:ALS` default to a normal C9orf72, so every
     C9orf72-positive case must author both panels (done here). A guard could check that a case with
     an authored pathogenic genetic result covers every panel that includes that gene.
   - The drug-check default "no clinically significant interaction" lacks SSRI class warnings:
     hyponatraemia with a thiazide (M07), QT and sedation with quetiapine (P02).
6. **MockServer** (harness):
   - Add a `drug` discriminator for `check_drug_interactions` follow-ups. Today tier 2 serves the
     single stored report (sertraline) for any drug: M01, M05, S01, S02, S09.
   - Merge the initial and keyed lab outputs when one order combines the baseline panel with a keyed
     panel (M05, P03, P04, S01).
   - A bare `analyze_csf` takes the only CSF follow-up (P03).
7. **`condition_tool_guidance.yaml` `ftd:`** (and `test_guidance_claims.py`):
   - FDG-PET recommended in P01, P02, P05 and P07.
   - S06 MRI avoided action changed from harm to waste.
   - P08: EMG required, respiratory function recommended.
   - S11 and S12: `speech_language_evaluation` recommended.
   - M08: CSF required set `[HIV_RNA]`, with JCV PCR and cryptococcal antigen optional.
8. **Vocabulary**: no lab panel for carbohydrate-deficient transferrin (M07; the value was removed).
9. **Criterion ids** kept although the criterion is now a lab order: M05 `action-8-check-drug-interactions`
   (lithium) and P01 `action-9-check-drug-interactions` (valproate, ammonia). Rename them if ids may
   change.
10. **Leak guard** (plan 5.7): also catch the paraphrase "Confirms Rascovsky 2011 criteria ..." in
    other conditions' templates.
11. **Review UI**: `criteria_met` keys are per syndrome (Gorno-Tempini in S11 and S12), so the UI
    must not assume Rascovsky keys.
12. **New dataset-wide guards suggested by this audit**:
    - (a) `patient` must not carry the totals of a bedside screen when `perform_clinical_assessment`
      is a criterion.
    - (b) `metadata.fallback_tool_kinds` must match the non-null fallbacks.
    - (c) A literature `source` should be a reference, not a citation key. Other conditions still
      have 61 bracketed and 10 bare-key sources.

## 5. Open questions for Andrea (consolidated)

Where a point could be settled for dataset quality, the round already decided it; these are the
calls to confirm or reverse.

- **Q1. Level of certainty** (plan Q1).
  - M06 is a known GRN carrier with the syndrome, which is definite bvFTD by Rascovsky 2011, but its
    `accepted[0]` says probable. Its must already states the definite category. Recommendation: a
    reviewer ruling to make M06 "definite".
  - P01, P03, S03 and S05 reach definite only if the agent orders the optional genetic test.
    Recommendation: keep "probable".
- **Q2. FDG-PET recommended** in P01, P02, P05 and P07 (applied; Reviewer 1 said optional). If FDG
  stays optional, P05 and P07 should be relabelled possible bvFTD.
- **Q3-Q6 of the plan**: decided as the plan proposed.
  - S06 MRI changed from harm to waste.
  - M08 CSF set decided by the normal white matter and CD4 680.
  - Per-syndrome `criteria_met` keys for PPA.
  - CT is waste where MRI is done (required only in S06 and M09).
- **Bedside screen out of the exam** (this audit, 18 cases): confirm. The alternative is the plan's
  C3 reading that the screen belongs to the examination. That would put the scores back in all 30
  cases and make the required assessment step uninformative.
- **Genetics threshold**: sporadic cases with onset at 59-64 have no genetics criterion and no
  counselling must (M01, M03, M05, M09, M10, P06, S02, S04, S06, S09). S01 (58) and S08 (onset 54)
  have both. Confirm, or add optional genetics to every case with onset before 65.
- **Values changed or authored that no reviewer has seen**:
  - M05 creatinine changed from 1.4 to 1.24 to match eGFR 64.
  - M10 Benton changed from 30/54 to 42/54, and famous faces moved below the 5th percentile.
  - P01 has two normal neuropsychology domains authored.
  - P05 FDG changed from borderline to mild, definite hypometabolism.
  - This audit authored the ALS panels in M02, P01, S03, S05 and S10, and the M06 GRN panel.
  - Acceptable?
- **P02 apathy**: counted as present, which gives 5 of 6 features. Read as narrowed interests it
  would be 4; nothing else changes.
- **P08**:
  - The NIV must quotes MIP -44 cmH2O from the recommended (not required) respiratory test: keep it,
    or make it generic.
  - The case has seven musts.
- **M06**: no AD biomarker criterion was added (GRN carrier with a concordant frontal syndrome).
  Add an optional amyloid step if wanted.
- **S09**: "advanced stage" in the label after a 2-year course is generous but defensible; it was
  not changed.
