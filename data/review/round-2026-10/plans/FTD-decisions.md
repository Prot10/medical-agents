# FTD: decisions on the open questions (24 Oct 2026)

Andrea ruled on 24 Oct 2026: "per i punti aperti, risolvili nel modo migliore per la qualità del
dataset". Every item below is decided and, where it needed a change, applied. Per-case detail is in
each case log under "Close-out (24 Oct 2026)". FTD has no reviewer notes file; the binding clinician
input is Reviewer 1's July 2026 tool rulings (`condition_tool_guidance.yaml`, `ftd:`).

Sources checked on 24 Oct 2026: ICD-10-CM tabular G31.0 (G31.01 Pick's disease, inclusion terms
"primary progressive aphasia" and "progressive isolated aphasia"; G31.09 other frontotemporal
neurocognitive disorder); Pottier C et al., J Neurochem 2016;138(Suppl 1):32-53 (PubMed 27009575;
the pack's old "Curr Opin Neurol 2016" reference was wrong); ISS/SNLG guideline "Diagnosi e
trattamento di demenza e Mild Cognitive Impairment" (2024, GRADE-ADOLOPMENT of NICE NG97); NHS
GeneTYPES eligibility for FTD genomic testing (no testing on the FTD diagnosis alone; onset before
55, a family history suggesting a monogenic cause, or a first- or second-degree relative with MND);
Ducharme S et al., Brain 2020;143(6):1632-1650 (C9orf72 screening advised in all possible or probable
bvFTD, or suspected cases with strong psychiatric features); EACS Guidelines (current version 13.0,
2025). Rascovsky 2011, Gorno-Tempini 2011, Foster 2007, Bang 2015, Frisoni 2024, Strong 2017, Boxer
2013, Ulugut 2020, Postuma 2015, Gold Coast 2020, Awaji 2008, EAN 2024, NICE NG42 and AAN 2009 were
checked against their published bibliographic data.

## 1. Diagnosis synonyms (`diagnosis_synonyms.yaml`, FTD entries)

| entry | before | after | reason |
| --- | --- | --- | --- |
| `G31.09` | 8 labels incl. "pick disease", "pick's disease"; codes G31.0, G31.01; applied to all 30 | generic bvFTD labels only; code G31.0; `except_cases: [FTD-P08]` | Pick disease is one FTLD-tau pathology (Pick bodies) that no case establishes, and the C9orf72 and GRN cases (TDP-43) cannot have; G31.01 is the ICD-10-CM code of primary progressive aphasia, so a PPA answer coded G31.01 scored in every bvFTD case |
| `RETIRED` | | + "pick disease", "pick's disease" | so `--prune` strips them |
| `G31.09+mnd` (new) | | P08 only: FTD-MND, FTD-ALS, ALS-FTD, ALS-FTSD, bvFTD MND/ALS, frontotemporal dementia with motor neuron/neurone disease, ALS or amyotrophic lateral sclerosis | the case is FTD-MND; a bvFTD-only answer misses the component that drives EMG, riluzole and NIV, as SE-P06 and HEP-ENC-P04 require both components |
| `G31.01+svppa` (new) | S11 accepted all bvFTD labels | svPPA, semantic variant PPA / primary progressive aphasia, semantic PPA, semantic dementia | summary CENTRAL 3: a bvFTD answer scored as correct; "frontotemporal dementia" and "FTD" are token subsets of every bvFTD answer, so no generic FTD label is granted to a PPA case |
| `G31.01+nfvppa` (new) | S12 the same | nfvPPA, non-fluent / nonfluent / agrammatic variant PPA, agrammatic PPA, progressive non-fluent aphasia, PNFA | same |

Applied with `apply_diagnosis_synonyms.py --prune --conditions ftd` (30 cases); `--check` and
`--check --prune` are clean. Verified with `DiagnosisCriterion.matches`: by label, a bvFTD answer
no longer matches P08, S11 or S12; svPPA and nfvPPA answers match only their own case; lvPPA matches
neither; ALS-FTD matches P08.

G12.21 is not added to P08 (summary CENTRAL 3): an ALS-only answer coded G12.21 would then score.

Residual (scorer, code-alone matching, the CENTRAL_PENDING item): P08 still accepts a bvFTD-only
answer coded G31.09; S11 and S12 share G31.01, so a wrong-variant PPA answer (or "Pick's disease")
coded G31.01 scores in either.

## 2. Label and code changes (ruling 3)

- **M06 (Q1)**: `accepted[0]` "Behavioral variant frontotemporal dementia (bvFTD), probable,
  GRN-associated (with early corticobasal syndrome features)" -> "... (bvFTD), definite (known
  pathogenic GRN variant), with early corticobasal syndrome features". She has 5 of 6 Rascovsky
  features and a known pathogenic GRN c.709-1G>A variant from cascade testing: Rascovsky 2011
  definite bvFTD. Her must already stated it. G31.09 unchanged; scoring unchanged.
- **S11, S12**: `icd_codes[0]` G31.09 -> G31.01 (ICD-10-CM inclusion term "primary progressive
  aphasia"); `metadata` codes and the PPA entries of the differentials recoded (other PPA variants
  G31.01; S12's "Alzheimer disease (logopenic variant)" G30.9). With G31.09 a bvFTD answer coded
  G31.09 scored through the code.
- **M05, M07, M08, S09** (summary CENTRAL 3, cosmetic): the em dash in `accepted[0]` replaced by a
  comma. Token matching ignores punctuation.
- **S09 "advanced stage"**: kept (2-year course, FTLD-severity functional loss; defensible).

## 3. Open questions (summary section 5)

1. **Q1, level of certainty.** M06 definite (section 2). P01, P03, S03, S05, and every case whose
   pathogenic result comes only from the optional panel (C9orf72 in M02, P01, P04, P05, P07, P08,
   S03, S05, S10; GRN in P02, S07; MAPT in P03), stay "probable": the label states what the
   required (or recommended) data support. Pack section 1.
2. **Q2, FDG-PET recommended in P01, P02, P05, P07.** Keep. Their MRI is normal or equivocal, so
   without functional imaging they meet only possible bvFTD (Rascovsky 2011 requires imaging
   support for probable), and NICE NG97 recommends FDG-PET or perfusion SPECT when FTD is
   suspected and the subtype uncertain. Recommended is credited and never required, so an agent
   that stops at the MRI is not failed. Because this departs from Reviewer 1's "optional", the
   guidance entry for `order_advanced_imaging` is now `status: confirm` and asks the reviewer to
   rule; if they keep it optional, P05 and P07 (and P01, P02) are relabelled possible bvFTD.
3. **Q3, S06 MRI harm -> waste.** Confirmed: the patient declines MRI without sedation; the order is
   futile, not harmful.
4. **Q4, M08 CSF set.** Confirmed: `HIV_RNA` required (CSF escape is a treatable mimic despite a
   suppressed plasma viral load); JCV PCR and cryptococcal antigen optional with normal white
   matter and CD4 680. The four HIV-related criteria, which had `citations: []`, now cite
   `[EACS_2025]` (summary CENTRAL 2 asked for `[EACS_2023]`; 13.0 of 2025 is the current version).
5. **Q5, per-syndrome `criteria_met` keys** (Gorno-Tempini in S11, S12). Confirmed; the schema
   accepts them. The review UI must not assume Rascovsky keys (CENTRAL 8).
6. **Q6, CT waste where MRI is done.** Confirmed: CT is required only in S06 (MRI declined) and in
   the ED case M09 (before MRI), Reviewer 1's "alternative when MRI is unavailable".
7. **Genetics threshold.** Changed. The FTD consortium (Ducharme 2020) advises C9orf72 screening in
   all possible or probable bvFTD; UK eligibility (NHS GeneTYPES) requires onset before 55, a
   suggestive family history or MND; Reviewer 1 asked for optional genetics "mainly for young-onset
   disease, strong family history". Ordering a counselled panel in a sporadic young-onset bvFTD
   is therefore defensible and must not be penalised by the stop rule, but it is not expected.
   Decision: an optional `action-genetic-panel-optional` criterion (with a negative authored
   panel and the clinical-assessment-before-genetics soft constraint) in the 10 sporadic bvFTD
   cases with onset before 65 that had none: M01, M03, M05, M09, M10, P06, S02, S04, S06, S09.
   No counselling must there. Every bvFTD case now has an optional genetics criterion except M06
   (known carrier); the PPA cases have none (sporadic svPPA and nfvPPA, low yield). S01 (onset 56,
   no family history) keeps its optional panel; its counselling must is now conditional ("if
   genetic testing is considered ..."). P03 keeps its must: onset about 55 and a mother who died at
   51 make the family history uninformative.
8. **Bedside screen out of the examination** (18 cases). Confirmed: the scores are the result of the
   required `perform_clinical_assessment` (ROUND_POLICY timeline-leak rule); the examination keeps
   the behavioural observations and frontal signs.
9. **Values changed or authored that no reviewer has seen** (M05 creatinine 1.24 for eGFR 64, M10
   Benton 42/54 with famous faces below the 5th percentile, P01 normal domains, P05 FDG definite
   hypometabolism, ALS panels in M02, P01, S03, S05, S10, the M06 GRN panel). Accepted: each makes a
   report support its own impression or the case's authored genotype (CKD-EPI 2021 gives about 63
   for creatinine 1.24 at 66; preserved perception with impaired famous-face recognition is the
   associative prosopagnosia of the right temporal variant). Listed for re-review below.
10. **P02 apathy.** Counted present (5 of 6 features); 4 of 6 would change nothing.
11. **P08 NIV must quoting MIP -44 cmH2O.** Keep: the must is already generic first ("arrange
    baseline respiratory assessment ... discuss NIV once an AAN 2009 marker is met") and quotes the
    value only conditionally ("if measured"). Seven musts are justified by FTD-MND management
    (MDT, riluzole with monitoring, respiratory, safety, counselling).
12. **M06 AD biomarker.** None added: a known carrier with a concordant frontal syndrome is definite
    bvFTD; an amyloid order there is unjustified.

## 4. Auditor flags and CENTRAL items handled here

13. **Criterion ids (summary CENTRAL 9).** Renamed: M05 `action-8-check-drug-interactions` ->
    `action-lithium-level`, P01 `action-9-check-drug-interactions` -> `action-valproate-level-ammonia`
    (both order `interpret_labs`; stop rules updated; no constraint referenced them).
14. **Citation keys (CENTRAL 2).** All registered in the pack with full references:
    `[SNLG_ISS_2024]`, `[Ducharme_2020]`, `[Frisoni_2024]`, `[Strong_2017]`, `[Boxer_2013]`,
    `[Ulugut_2020]`, `[Postuma_2015]`, `[Awaji_2008]`, `[EACS_2025]`, plus the confirmed
    `[NICE_NG97]`, `[ACMG_NSGC_2011]`, `[Amyloid_PET_AUC_2025]`, `[EAN_ALS_2024]`, `[NICE_NG42]`,
    `[AAN_2009]`, `[Gold_Coast_2020]`. P08 `metadata.citation_gap` cleared. `[AAN_dementia_2018]`
    retired. `[EFNS_Wernicke_2010]` not added: no M07 criterion cites thiamine evidence (thiamine is
    a must). The M09 toxicology criterion stays uncited: no FTD guideline governs ED toxicology.
15. **Discriminators (step 5b).** The only defect was the untyped echo fallback in all 30 cases:
    `echo_type: TTE` set (each is a transthoracic report; a TEE order now gets the library TEE
    report). FTD added to `DISCRIMINATOR_CONDITIONS`; `test_routed_outputs_name_their_study` passes.
16. **Guidance (CENTRAL 7).** `build_condition_tool_guidance.py` FTD responses updated: labs (levels
    as labs), advanced imaging (FDG optional 26, recommended 4, `status: confirm` with the question,
    SPECT authored everywhere, amyloid 4, DaTscan P04), specialized tests (genetics optional in 27,
    counselling rule, P08 EMG required and respiratory recommended, speech-language in S11 and S12),
    clinical assessment (Rascovsky in 28, Gorno-Tempini in 2). YAML regenerated with `--write`;
    claim table rows rewritten and extended (genetics 27/0, EMG/respiratory, speech-language 2, PPA
    G31.01 2, FDG 26/4, SPECT 26/4, amyloid 4, DaTscan 1, no advanced required, baseline labs 30).
17. **Criteria pack (CENTRAL 1)** rewritten (below). **Generator** block (below).

## 5. Criteria pack, generator

- `dataset-generation/criteria_packs/FTD.md`: per-case ICD rule (G31.09 bvFTD and FTD-MND, G31.01
  PPA); bvFTD levels and the label rule; PPA, FTD-MND and psychiatric-mimic criteria; workup order
  and tiers as the cases now stand; literature optional and last; drug check only for a concrete
  interaction, never as a toxicity test; waste list and fallbacks; the four soft constraints and the
  stop rule; pitfalls (memory complaints, psychiatric history, normal MRI, rigidity, amyloid claims,
  canonical prohibitions, safety musts, SSRI interactions); allow-list with full references, the
  Pottier reference corrected, `[AAN_dementia_2018]` and the Lebert citation retired.
- `dataset-generation/config/conditions.yaml` (`frontotemporal_dementia` block): round header
  comment; the three difficulty presentations no longer contain MRI, FDG-PET, neuropsychology or
  pending genetic results (scored studies); the "asymmetric temporal atrophy mimicking early
  Alzheimer's" line now names left (svPPA) or right (right temporal variant) anterior temporal atrophy; CJD
  distinguished by RT-QuIC, not 14-3-3; genetics follow-up states the optional and counselling
  rules and the dual-panel rule; new follow-ups for the PPA speech-language evaluation and for
  targeted drug levels. No seeded literature, consult or drug-check-as-toxicity follow-up existed
  to remove.

## Files changed

- Cases: all 30 (echo discriminator; synonym re-expansion). Content: M06 (label), S11, S12 (code,
  differential codes), M05, M07, M08, S09 (label punctuation), M05, P01 (criterion ids), M01, M03,
  M05, M09, M10, P06, S02, S04, S06, S09 (optional genetics), S01 (must), M08 (citations), P08
  (metadata). Logs: all 30, "Close-out (24 Oct 2026)".
- `agent-platform/config/policies/diagnosis_synonyms.yaml` (FTD entries, RETIRED),
  `dataset-generation/criteria_packs/FTD.md`, `dataset-generation/config/conditions.yaml` (FTD
  block), `agent-platform/scripts/review/build_condition_tool_guidance.py` (FTD responses),
  `agent-platform/config/review/condition_tool_guidance.yaml` (regenerated),
  `agent-platform/tests/test_guidance_claims.py` (FTD rows), `agent-platform/tests/test_case_guards.py`
  (`DISCRIMINATOR_CONDITIONS` + FTD).

## Checks

`perfect_agent.py` 30/30; `case_io.py check` on all 30: schema and synonym guard OK, no failure names
an FTD case; `test_case_guards.py -k FTD-` 90 passed; `apply_diagnosis_synonyms.py --check
--conditions ftd` clean (also with `--prune`); `test_guidance_claims.py` and
`test_condition_tool_guidance.py` pass.

## Still for Andrea or the physicians

Nothing blocks. FTD has never been physician-reviewed; schedule it into the next review round. For
the reviewers: the FDG-PET departure (guidance `status: confirm`, Q2); M06 relabelled definite; the
PPA cases recoded G31.01 and no longer accepting FTD or bvFTD answers; P08 no longer accepting a
bvFTD-only answer by label; Pick disease labels and G31.01 no longer accepted in bvFTD; optional
genetics in 10 more cases; the values listed in section 3, item 9.

## CENTRAL (not made here; owners elsewhere)

1. **Vocabulary**: `interpret_labs` panel `CDT` (carbohydrate-deficient transferrin, serum, % of
   transferrin; biomarker of sustained heavy drinking) for FTD-M07 (alcohol use disorder with
   bvFTD; the value was removed for want of a term). Optional criterion only.
2. **Scorer**: code-alone matching (P08 bvFTD answers coded G31.09; svPPA and nfvPPA share G31.01).
   Same root as the CENTRAL_PENDING items on the ICD code alone.
3. **MockServer**: a `drug` discriminator for `check_drug_interactions` follow-ups (M01, M05, S01,
   S02, S09 serve the sertraline report for any drug; same as the ALZ-EARLY item); merge the
   initial and keyed lab outputs when one order combines the baseline panel with a keyed panel
   (M05, P03, P04, S01; same root as SE CENTRAL 5); a bare `analyze_csf` takes the only CSF
   follow-up (P03).
4. **Fallback library**: FDG-PET, perfusion SPECT, amyloid PET and DaTscan defaults are normal
   (FTD now authors FDG and SPECT everywhere); `genetic_panel:FTD` and `genetic_panel:ALS` default
   to a normal C9orf72, so a guard could check that a case with an authored pathogenic result covers
   every panel containing the gene; the drug-check default lacks SSRI class warnings (hyponatraemia
   with a thiazide, M07; QT and sedation with quetiapine, P02).
5. **perfect_agent.py**: exercise every declared alternative (SPECT, CSF AD markers, amyloid PET)
   and flag library answers (as in CENTRAL_PENDING).
6. **Leak guard**: also catch the paraphrase "Confirms Rascovsky 2011 criteria ..." in other
   conditions' templates.
7. **New dataset-wide guards**: (a) `patient` must not carry bedside-screen totals when
   `perform_clinical_assessment` is a criterion; (b) `metadata.fallback_tool_kinds` must match the
   non-null fallbacks; (c) a literature `source` is a reference, not a citation key (other
   conditions still have 61 bracketed and 10 bare-key sources).
8. **Review UI**: `criteria_met` keys are per syndrome (Gorno-Tempini in S11, S12); show the
   `confirm` badge for `ftd/order_advanced_imaging`.
