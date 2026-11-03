# MG: decisions on the open questions (24 Oct 2026)

Andrea, 24 Oct 2026: resolve every open point "nel modo migliore per la qualità del dataset". Each
entry gives the question, the decision, the reason with its source, and what changed where.
Per-case detail is in each case log under "Close-out (24 Oct 2026)". Nothing is committed.

Sources checked on 24 Oct 2026:
- Jacob S, Farrugia ME, Hewamadduma C, et al. ABN autoimmune myasthenia gravis management
  guidelines (2025 update). Pract Neurol 2025;25:422-437, doi 10.1136/pn-2025-004655, read in full
  text. Verified: AChR by RIA or CBA first, MuSK if negative, thyroid function in all, the
  high-sensitivity CBA panel (clustered AChR, clustered MuSK, LRP4) before calling MG seronegative;
  "striated muscle, titin, are unlikely to be diagnostically helpful"; RNS first, SFEMG if
  available, pyridostigmine held 12 h; contrast brain and orbit MRI only after negative serology
  and neurophysiology; thymic imaging (CT or MRI) in all patients with suspected MG irrespective
  of distribution or serology, chest X-ray insufficient; Tensilon no longer recommended;
  thymectomy recommended for AChR-positive patients under 50, discussed at 50-65, all thymomas,
  not in MuSK MG, no data in seronegative MG, worth considering in AChR-positive ocular MG within
  2-3 years; inpatient care for FVC below 30 mL/kg, ICU referral for FVC below 20 mL/kg or a fall
  of more than 30%; IVIG and plasma exchange equally effective, plasma exchange best avoided in
  sepsis.
- Evoli A et al., Neurol Sci 2019;40:1111-1124 (doi 10.1007/s10072-019-03746-1); Narayanaswami P
  et al., Neurology 2021;96:114-122 (doi 10.1212/WNL.0000000000011124); Wolfe GI et al., Lancet
  Neurol 2019;18:259-268 (MGTX extension, benefit at 5 years); Punga AR et al., Lancet Neurol
  2022;21:176-188 (title "Epidemiology, diagnostics, and biomarkers of autoimmune neuromuscular
  junction disorders"); Titulaer MJ et al., Lancet Neurol 2011;10:1098-1107; Titulaer MJ et al.,
  EFNS Task Force, Eur J Neurol 2011;18:19-e3 (CT thorax, then FDG-PET if negative; LEMS screening
  for 2 years); Oh SJ et al., Muscle Nerve 2005;32:515-520; Higuchi O et al., Ann Neurol
  2011;69:418-422; Zisimopoulou P et al., J Autoimmun 2014;52:139-145 (LRP4 in 18.7% of
  double-seronegative sera, 7-32.7% by country); Ho PR et al., Lancet Neurol 2017;16:925-933.
  Bibliographic records verified; the ESUR thyroid statement is cited from van der Molen AJ et al.,
  Eur Radiol 2004;14:902-907 and the ESUR v10 guidelines (full text not retrieved).
- ICD-10-CM: G70.00 myasthenia gravis without (acute) exacerbation; G70.01 with (acute)
  exacerbation (includes crisis); G73.1 Lambert-Eaton syndrome in neoplastic disease; G70.80
  Lambert-Eaton syndrome, unspecified.

## Open questions (summary section "Open questions for Andrea")

1. **Composition: LEMS (P02, RM13) and the known-MG exacerbation and crisis cases (M04, RM14,
   RM15) in the MG condition.** Decision: keep all five, with their labels and pathways. Reason:
   the generator spec for this condition defines these subtypes (pack section 6: P "crisis", R
   "Lambert-Eaton myasthenic syndrome" as the mimic), and the dataset builds mimic cases with the
   mimic's own code in most conditions (ALS-P02 E05.90 was kept the same way, plans/ALS-decisions.md
   Q1). LEMS is the classic MG mimic, so its two cases test the condition's central
   discrimination (facilitation, VGCC, tumour search). The crisis cases test respiratory staging,
   precipitant recognition and an MG-safe plan, which the pack and ABN 2025 make part of MG care.
   Moving them would change the 20 x 30 design, which a close-out does not do. No information only
   Andrea has is needed. Change: none; pack section 6 records the composition.
2. **ICD reorder G70.01 -> G70.00 in the stable cases (summary CENTRAL 2).** Decision: applied in
   20 cases (M01, M02, M03, P03, RM11, RM12, RM16, RP11, RP12, RP13, RS12, RS13, RS14, RS15, RS16,
   RS17, S01, S02, S03, S04). Reason: ICD-10-CM G70.01 is "with (acute) exacerbation", which a new
   presentation is not. RS14 (relapsing bulbar episodes, first diagnosis now) is a new diagnosis
   too. M04, RM14 and RM15 (impending or established crisis in known MG) keep G70.01. P01, P04,
   RP14, RS11 and S05 already had G70.00. Scoring: stable cases still accept G70.01 (a coding
   nuance of a worsening presentation, not a different entity); the three crisis cases no longer
   accept G70.00, because "without exacerbation" negates what they test.

## Summary CENTRAL items

3. **Synonyms (CENTRAL 3).** Applied in `diagnosis_synonyms.yaml` and expanded with `--prune
   --conditions myasthenia_gravis` (30 cases); `--check` clean.
   - The G70 category now grants only "myasthenia gravis", "autoimmune myasthenia" and G70.0.
   - "generalized/generalised myasthenia gravis", "generalized MG", "generalised MG": every MG case
     except the ocular RS11 and S05 (bulbar-only RS15 and MuSK RS14 are generalized by MGFA).
   - "ocular myasthenia gravis", "ocular myasthenia", "ocular MG": RS11 and S05 only (it was
     accepted in all 28 generalized cases).
   - Bare "MG" retired (added to `RETIRED`): a one-token label matched any answer mentioning MG,
     e.g. "LEMS, not MG". Two-token forms replace it where scoped.
   - "myasthenic crisis", "myasthenic exacerbation", "impending myasthenic crisis", "MG crisis",
     "MG exacerbation": M04, RM14, RM15. The summary proposed crisis for RM14 and RM15 and
     exacerbation for M04; M04 also gets crisis because its MIP -32, MEP 38 and bulbar weakness
     meet impending-crisis criteria, its differential rates "evolving myasthenic crisis" high and
     its musts are ICU care with IVIG or PLEX.
   - "seronegative myasthenia gravis", "seronegative MG": P01, RP14. "double seronegative
     myasthenia gravis/MG": P01, P04, RP14 (P04 is AChR- and MuSK-negative, LRP4-positive).
     "LRP4 myasthenia gravis", "LRP4 antibody positive myasthenia gravis", "LRP4 MG": P04.
     "MuSK myasthenia gravis", "MuSK antibody positive myasthenia gravis", "anti-MuSK myasthenia
     gravis", "MuSK MG": RS14 (the summary's "consider a MuSK-MG label").
   - G73.1: "paraneoplastic lambert eaton myasthenic syndrome" and "LEMS with small cell lung
     cancer" added (P02, RM13).
   - Scan of all 30 against accepted[0]: the only synonyms naming a different subtype were the
     ocular/generalized pair and bare "MG"; both fixed. Residual limit, same as GBS: a wrong-subtype
     answer that contains "myasthenia gravis" (e.g. "ocular myasthenia gravis" in a generalized
     case) still scores through the generic label, and G70.00 credits any MG subtype through the
     code; this needs the per-case rejected-token scorer already in CENTRAL_PENDING.
4. **Labels (ruling 3).** MG-P03 `accepted[0]` relabelled "Myasthenia gravis, AChR
   antibody-positive, generalized (MGFA Class IIb), with thymoma, concurrent with
   relapsing-remitting multiple sclerosis on natalizumab". Reason: the case's own mediastinal CT
   shows a 2.8 cm thymoma and its must refers her for thymectomy, so "possible drug-associated
   autoimmunity" is a speculative attribution the data no longer support (the worker flagged it
   and left it under ruling 3; GBS-RP15 dropped a speculative attribution the same way). Other
   labels checked against their data and kept (RM11 "paraneoplastic in context of peripheral
   T-cell lymphoma" is hedged and reflects an association the case discusses).
5. **Criteria pack (CENTRAL 1, 11).** `dataset-generation/criteria_packs/MG.md` rewritten to the
   plan and summary: governing-source map, serology and neurophysiology facts, thymic imaging in
   every new diagnosis, tiers and variant pathways (seronegative, MuSK, ocular, crisis, LEMS),
   waste list (emg_ncs is no longer called useless: routine NCS accompany RNS), treatment
   statements (thymectomy per MGTX and ABN 2025, steroid and drug prohibitions, ICU thresholds,
   pregnancy, amifampridine with the corrected SmPC ECG wording), soft sequence constraints, stop
   rule, pitfalls and wrong facts. Allow-list: the four keys the cases cite ([Gilhus_2016],
   [Punga_2022], [Sanders_2016], [Wolfe_2016]) plus every source the cases cite by author, each
   with a full reference: [Jacob_2025], [Evoli_2019], [Narayanaswami_2021], [Wolfe_2019],
   [Gilhus_2019], [Higuchi_2011], [Zisimopoulou_2014], [Titulaer_2011], [EFNS_paraneoplastic_2011],
   [Titulaer_2011_DELTAP], [Oh_2005], [Firdapse_SmPC], [Lawn_2001], [ESUR_contrast], [Ho_2017];
   [Punga_2022] title and [Vincent_2003] year (2002) corrected; [Jaretzki_2000_MGFA] kept. No key
   is superseded; [Sanders_2016] is read with its 2020 update. Literature and drug checks are no
   longer required by default, telithromycin is gone, [Wolfe_2016] is restricted to thymectomy.
6. **Generator (CENTRAL 4).** `conditions.yaml` myasthenia_gravis block: stale follow-ups
   replaced (`request_pulmonary_function` under interpret_labs -> `request_respiratory_function`
   under order_specialized_test; `request_thymectomy_evaluation` under order_ct_scan ->
   `request_mediastinal_ct` under order_body_imaging; MuSK follow-up limited to AChR-negative
   patients, LRP4 to double-seronegative); CSF dropped from the optional modalities ("no CSF");
   `icd_code` G70.00; key findings that contradicted the pack corrected (RNS decrement
   "pathognomonic", SFEMG ">95%" as gold standard, the Tensilon test, anti-striational antibodies,
   "paraneoplastic antibody panel" in seronegative MG, "borderline" AChR, a LEMS-like facilitation
   "MG variant"); the thymic CT findings moved from `ct` to `body_imaging`; the three difficulty
   presentations no longer contain AChR, MuSK, RNS, SFEMG or CT results.
7. **Guidance claims (CENTRAL 5).** `build_condition_tool_guidance.py` MG responses updated and
   regenerated with `--write`; claim table in `test_guidance_claims.py` updated: brain MRI is an
   action in 3 cases (required in P03, optional in RS14 and P02), mediastinal CT required in 27
   (all new diagnoses, the two LEMS cases through the chest-CT criterion) and optional in the
   three crisis cases, RNS required in 27, SFEMG in 25 (required 3, an alternative to RNS in the 2
   ocular cases, recommended 3, optional 17). `test_guidance_claims.py` passes.
8. **Library head-CT wording (CENTRAL 6).** Closed: `fallback_library.yaml` does not contain "does
   not address the question"; the phrase came from the case fallbacks, which the round fixed.
9. **Vocabulary anti_titin, anti_RyR (CENTRAL 7).** Not requested. ABN 2025: titin and
   striational antibodies "are unlikely to be diagnostically helpful"; no MG case needs them (the
   titin rows were removed in RM11 and S03).
10. **`endotracheal_aspirate` (CENTRAL 7).** Keep `sputum` in RM15: the laboratory test is the same
    lower respiratory tract culture and Gram stain (CPT 87070 + 87205). Listed below as an
    optional vocabulary note.
11. **P04 LRP4 follow-up answers a combined order (CENTRAL 8).** Harness change, not made here;
    listed below. Scoring is unaffected.
12. **Discriminators (CENTRAL 9, brief 5b).** The hand-run guard found 0 defects in 30 cases; MG
    added to `DISCRIMINATOR_CONDITIONS` in `test_case_guards.py`; `test_case_guards.py -k MG-`
    90 passed.
13. **M04 SFEMG library normal (CENTRAL 10).** Kept: SFEMG is a waste avoided action in M04, so the
    report an agent receives after a wasteful order does not affect any criterion. Library note
    below.
14. **`mediastinum_MRI` perfect-agent warnings (CENTRAL 12).** Kept. The perfect-agent
    warnings come only from cases without a thymoma, where the library's normal mediastinal MRI
    agrees with the case's normal CT. In the thymoma cases that offer an MRI alternative, the
    case's own report answers it.
15. **CENTRAL_PENDING "MG-RS15 Neostigmine challenge".** Stale: the round deleted the neostigmine
    follow-up (plan H5); no MG case stores a prose `test_type`, and neostigmine is not a
    vocabulary term (not orderable, like edrophonium). The orchestrator can remove the item.

## Auditor flags ("left as is") and worker questions

16. **Pre-existing em dashes in prose the round did not rewrite:** kept (churn only; none in a
    label or a new text).
17. **"within reference range" inside lab interpretations:** kept (report voice, correct).
18. **Literature fallbacks "No directly applicable evidence" (M01, M03, M04, RM13):** kept. The
    MockServer answers every literature query from the case's initial literature output when one
    exists, so these fallbacks are never served (the central unreachable-fallback test will catch
    them); the text is neutral and says nothing about the case.
19. **Stale `metadata.fallback_tool_kinds.advanced_imaging` (M01-M04, P01):** kept; no code reads
    it and the same pattern exists in the closed conditions.
20. **Library FDG_PET is a brain PET:** no contradiction with the thymomas (FDG-PET is waste in
    MG). No change.
21. **Stale `metadata.citation_gap` in P04:** emptied (it gave Higuchi 2011 as Muscle Nerve and
    Zhang 2012 as Nature Communications, and the gap is closed by the pack).
22. **Worker questions already settled at audit, confirmed:** P01 (MuSK as its own required
    criterion, ice pack optional because ptosis appears only after 90 s of upgaze, no thymectomy
    must: ABN 2025 finds no data for thymectomy in seronegative MG); P02 (FDG-PET required after a
    negative CT, EFNS 2011; DELTA-P in key evidence); RP14 (plasma exchange preferred to IVIG in
    APS, as a preference); RS13 (drug check recommended for hydroxychloroquine; no third orbit
    MRI); RS14 (MuSK in a follow-up against leakage); RS15 (thymectomy must at 53: MGTX 18-65,
    ABN "discussed at 50-65"); RS16 (MGFA IIIa, statin kept with the association noted).
    Ocular cases (RS11, S05) keep no thymectomy must: ABN 2025 and the 2020 update make it an
    option in AChR-positive ocular MG, not a requirement.

## CENTRAL (for the vocabulary/code agent and the orchestrator; not changed here)

- Harness/matcher (MG-P04): one `interpret_labs` call listing `anti_AChR`, `anti_MuSK`,
  `anti_LRP4` and `TSH` is answered by the LRP4 follow-up alone, so the agent does not see the
  AChR, MuSK and thyroid results it ordered. Merge a set-valued lab follow-up with the initial
  report (same root as SE CENTRAL 5).
- Vocabulary, optional: `order_microbiology` specimen `tracheal_aspirate` (lower respiratory
  culture in a ventilated patient, CPT 87070 + 87205, priced as `sputum`), or a comment in
  `costs.yaml` that `sputum` covers it. Case: MG-RM15. Not blocking.
- Library, optional: the library SFEMG default is a normal study; a known AChR-positive patient
  would not have one (MG-M04, where SFEMG is a waste action). Not blocking.
- Scorer: per-case rejected tokens (already pending) would let the ocular cases reject
  "generalized" and the generalized cases reject "ocular".
- CENTRAL_PENDING: remove the "MG-RS15 Neostigmine challenge" item (item 15) and add MG to the
  conditions whose discriminator data are closed.

## Files changed

- Cases: all 30 MG cases (synonyms); `icd_codes[0]` in the 20 cases of Q2; MG-P03 label;
  MG-P04 metadata. Logs: "Close-out (24 Oct 2026)" appended to all 30.
- `agent-platform/config/policies/diagnosis_synonyms.yaml` (G70 and G73.1 entries, `MG` retired).
- `dataset-generation/criteria_packs/MG.md`; `dataset-generation/config/conditions.yaml`
  (myasthenia_gravis block).
- `agent-platform/scripts/review/build_condition_tool_guidance.py` (MG responses),
  `agent-platform/config/review/condition_tool_guidance.yaml` (regenerated),
  `agent-platform/tests/test_guidance_claims.py` (MG claims),
  `agent-platform/tests/test_case_guards.py` (MG in `DISCRIMINATOR_CONDITIONS`).

## Still for Andrea or the physicians

Nothing blocks. MG has never been physician-reviewed: schedule it for the next round. Scoring
changes to point the reviewers at: ocular and generalized labels are now scoped; bare "MG" no
longer scores; the crisis cases no longer accept G70.00; G70.00 is the primary code of every
stable case.
