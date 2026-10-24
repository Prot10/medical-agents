# MG: condition summary, October 2026 review round

Condition auditor, 24 Oct 2026. Scope: the 30 MG cases (M01-M04, P01-P04, RM11-RM16, RP11-RP14,
RS11-RS17, S01-S05). I read plan `plans/MG.md`, ROUND_POLICY, PATTERNS and all 30 logs, checked
the plan's decisions by script across the 30 files (criteria tiers, stop rules, sequence
constraints, citations, prohibitions and musts, patient-block leaks, discriminators, body-imaging
region and contrast, differential), read the inconsistent cases in full and fixed the stragglers
through `case_io`. Every changed case's log ends with a "Condition audit (MG auditor, 24 Oct
2026)" section that lists what changed and why.

Final state of the 30 cases:
- `perfect_agent.py`: 30/30 pass. The only remaining warnings are the `mediastinum_MRI` alternatives answered by the library's normal mediastinal MRI. That report is consistent with the cases without thymoma (CENTRAL 12).
- `case_io.py check`: schema OK for all 30 and the synonym guard OK. No test failure names an MG case; the 15 failures belong to other conditions or to central claim tests.
- Hand-run discriminator guard (`discriminator_defects` from `test_case_guards.py`; MG is not in `DISCRIMINATOR_CONDITIONS`): 0 defects in 30 cases. Before the audit, 12 cases had defects.
- Case guards `-k MG-`: 60 passed.

## Reviewer notes

There is no notes file for MG (R1 and R2 have not reviewed it), so no reviewer note ids exist.

| Ruling | Count |
|---|---|
| FIXED | 0 |
| ALREADY-FIXED | 0 |
| DECLINED | 0 |
| BLOCKED | 0 |

There are no DECLINED or BLOCKED notes.

## Counts

- Own findings in the worker logs: 511 rows, all FIXED and none left FLAGGED in the tables. By class: A 75, B 107, C 208, D 85, E 29. The plan classes F-N are logged under these labels.
- Adversarial verifier corrections: 22 itemised fixes, in P03, P04, RM11, RM12, RM13, RM15 and S01-S05.
- Auditor corrections: 45 changes in 24 cases (M01, M02, M03, P01, P02, RM11, RM13, RM14, RM15, RM16, RP11, RP12, RP13, RP14, RS12, RS13, RS15, RS16, RS17, S01, S02, S03, S04, S05).
- Cases changed in the round: 30/30 against the pre-round base `fa1d22e6`. 27 differ from the checkpoint commit `1fd43d22`.
- Approved cases changed: 0. All 30 MG cases were `draft` before the round and are still `draft`.

## Error classes found and how each was fixed

These are the plan's section 2 classes. The workers fixed each one case by case, and the verifiers checked the fixes.

- **A. Template criteria and tiers.** The same six to eight criteria were stamped on every case. They were rebuilt per plan section 3:
  - The labs criterion is `["anti_AChR","TSH"]` with subset matching. MuSK is its own required criterion only in AChR-negative cases (P01, P04, RP14, RS14). LRP4 or the cell-based assay is used only in double-seronegative cases.
  - Literature was deleted in S cases, and is optional and last elsewhere.
  - Drug-check tiers follow table 3.2, with logged deviations in P03 and RS13 (recommended because of a concrete interaction).
  - Labels are imperative and differ from the rationales.
- **B. Scoring key in literature and drug outputs.** Each case keeps at most one literature output, in report voice, with correct citations (the canonical text, or the LEMS text in P02 and RM13). The invented-journal follow-ups were deleted.
- **C. Drug-check outputs.** There is one output per real interaction, with the patient's own medication list, written in checker voice. Treatment-plan "checks" were deleted (P01, RM14, S01, RM12, S03, S04, the P02 duplicate). Telithromycin is gone.
- **D. Shared prohibitions and musts.**
  - The canonical steroid, functional-attribution and drug prohibitions replace the seven identical ones.
  - Musts that were diagnostic tests were deleted.
  - The thymectomy musts follow plan fact 20. M03 has a resection must for its thymoma. M04 has no thymectomy must (diagnosed 6 years ago, outside MGTX). RS15 has the must (bulbar-only MG is generalized).
- **E. Shared key evidence and avoided actions.** The titin and "all MG require CT chest" pearls were rewritten. Waste items now carry case rationales and no [Wolfe_2016].
- **F. Head-CT fallback wording.** Replaced by a plain normal head CT report.
- **G. Lab stub rows.** Replaced by real values, units and ranges. Every "All normal" panel was itemised.
- **H. Unreachable, shadowed or misrouted reports.**
  - RNS reports were merged.
  - Duplicate respiratory follow-ups were deleted.
  - Chest CTs moved from the head-CT tool to `order_body_imaging`.
  - Body-imaging contrast was set to true everywhere except RM16, where it is withheld for overt hyperthyroidism.
  - Prose discriminators were replaced by vocabulary values.
  - Serology moved into the initial labs. RS14 keeps MuSK in a follow-up, against leakage.
  - Biopsies are now `obtain_tissue_diagnosis`.
  - Misplaced tests were moved, and follow-ups that were not indicated were deleted.
- **I. Stub outputs.** The ice pack, SFEMG, respiratory, mitochondrial and ECG reports now carry patient-specific values.
- **J. Treatment disguised as a test.** Every listed item was deleted and turned into a must.
- **K. Patient-block leaks.** NIF and FVC numbers were removed (scripted check: none left). AChR results stay only as prior history in the known-MG cases. The RS14 HPI was rewritten, and P02 lost its EMG sentence. The extra top-level patient keys were merged and dropped (scripted check: none left).
- **L. Unit and logic errors.** Blocking antibody is in %, each case uses one laboratory's ranges, NIF and FVC readings are consistent, and mL/kg is computed against the stated weight. Weight is present wherever there is a respiratory criterion.
- **M. Differential not updated.** Lowered per ruling 7 (scripted check: mostly low or very_low). The only high entries are justified: RM15 aspiration, a coexisting precipitant, and M04's crisis entry.
- **N. Citations.** [Wolfe_2016] appears only on thymectomy and mediastinal criteria (scripted check). Keys missing from the pack are cited by author in the text.

Classes that survived in some cases were fixed at audit:

- **Fallback discriminators.**
  - `fallback_tool_outputs.echo` had an empty `echo_type`, and `fallback_tool_outputs.advanced_imaging` an empty modality. The RS11-RS16 verifiers had fixed this only in their own cases.
  - Fixed: `echo_type` set to `TTE` in 11 cases (RM15, RM16, RP11, RP12, RP13, RS17, S01-S05).
  - The empty advanced-imaging fallback was removed in 5 cases (RM15, RM16, RP12, RP13, RP14), so the library serves the normal report for the study actually ordered.
- **Sequence constraints (plan 3.3).**
  - The soft labs -> SFEMG constraint was missing in RP11-RP14.
  - Both labs -> SFEMG and RNS -> SFEMG were missing in RS12, RS13, RS15 and RS16.
  - Added with the plan's reasons.
- **Citation scope (plan 1.1).**
  - [Sanders_2016] (management) was cited for antibody testing in RM16 and RP11-RP14. Replaced by [Punga_2022].
  - [Sanders_2016] was removed from the RP14 SFEMG criterion.
  - [Gilhus_2016] (an MG review) was removed from the 10 LEMS criteria of P02, as the RM13 verifier had done in RM13.
- **Ocular-motility laterality.** These exam sentences gave diplopia on the wrong side for the muscle named:
  - M02: right eye adduction weakness with diplopia on rightward gaze. Now left eye adduction weakness.
  - M03: limited adduction of the left eye with diplopia looking left. Now limited abduction of the left eye.
  - P01: right eye adduction lag tested on rightward gaze. Now leftward gaze.
- **Ptosis measure.** M01, M03 and RM11 gave levator excursion in the exam while the ice-pack report measures MRD1. The exam now gives MRD1 values that match the ice-pack baseline.

## Fixed by the auditor (beyond the classes above)

- **MG-RM13: amifampridine ECG wording.**
  - Must [1] and the drug output said "repeat ECG after titration". Plan fact 24 has the same wording.
  - The EU SmPC (section 4.4) asks for clinical and ECG monitoring at initiation and yearly thereafter, and an ECG at once if arrhythmia is suspected.
  - Both texts now say that, as P02 already did.
- **MG-RM15.** The `metadata.actions_withdrawn` entry for the ice pack ("recommended here") was stale: a ventilated crisis has no ice-pack criterion. Emptied.
- **MG-RM14.** The labs criterion now also accepts `["CBC","CMP","CRP"]`, as M04 and RM15 accept CMP for BMP.
- **MG-RS17 and MG-S05.** The body-imaging region changed from "mediastinum" to "chest, anterior mediastinum". The `chest_CT` alternative is now answered by the case's own CT chest report, as in S01-S04, instead of a library normal report.

## Checked and confirmed uniform (no change needed)

- **Stop rules.** `required_before_assessment` equals the required set in all 30 cases. `max_additional_actions` is 1 in S cases and 2 elsewhere.
- **Literature.** Optional and last, or deleted, in every case.
- **[Wolfe_2016].** Only on mediastinal and thymectomy criteria.
- **Patient block.**
  - No NIF, FVC or cmH2O values.
  - No extra top-level patient keys.
  - Weight present wherever there is a respiratory criterion.
- **Body-imaging contrast.** True everywhere except RM16, which is justified.
- **Drug-check tiers.** Match table 3.2, apart from the logged P03 and RS13 deviations.
- **Pathways.** Crisis pathway in M04, RM14 and RM15. LEMS pathway in P02 and RM13: chest CT, then FDG-PET, then tissue, then ECG before amifampridine.
- **Left as is:**
  - Pre-existing em dashes in prose the round did not rewrite.
  - "within reference range" phrases inside lab interpretations.
  - Literature fallbacks that say "no directly applicable evidence" in cases that also have an initial literature output.
  - Stale `metadata.fallback_tool_kinds.advanced_imaging` in M01-M04 and P01. No code reads that field.
  - The library FDG_PET is a brain PET, so it does not contradict the thymomas in M01, M03 and P03.

## Decisions taken at audit

Each decision settles an item a log left open, following Andrea's rule to decide for dataset quality.

- **RP14.** Plasma exchange is preferred over IVIG in APS because of thrombotic risk. It is kept as a preference in the must, not as a prohibition, because some centres give slow IVIG with prophylaxis. The echo deletion is accepted: there is no murmur or cardiac symptom.
- **RS16.** MGFA IIIa is kept for 2/5 neck extensors with mild bulbar symptoms. The class is not scored, and IIIa is the closer reading. The statin is kept, with the association noted in the drug output.
- **RS15.** The thymectomy must is kept. Bulbar-only MG is generalized, which falls within MGTX classes II-IV.
- **RS14.** MuSK is kept in a follow-up, so the result is returned only when MuSK is ordered (leakage).
- **RS13.** The deviations are accepted:
  - The drug check is recommended because of hydroxychloroquine.
  - No orbit MRI criterion: two normal orbital MRIs are already in the history.
- **P01, P02, RM11, RM12, RM13, RM14, RM15, RM16, RP11-RP13, P03.** The worker decisions recorded in the logs are accepted as logged. The P01 and P02 questions had already been resolved by their verifiers.
- **Plan fact 24.** Its ECG wording ("after titration") is wrong and should be read as the EU SmPC wording above (CENTRAL 11).

## CENTRAL requests (consolidated)

1. **Criteria pack `dataset-generation/criteria_packs/MG.md`.**
   - Add keys for sources now cited by author in the text:
     - Jacob 2025 (ABN guidance)
     - Evoli 2019
     - Narayanaswami 2021
     - Wolfe 2019
     - Titulaer 2011 (Lancet Neurol)
     - EFNS paraneoplastic 2011 (Titulaer, Eur J Neurol)
     - Oh 2005
     - Lawn 2001 (shared with GBS)
     - an ESUR contrast media guideline key (RM16)
     - Ho 2017 (natalizumab PML, P03)
     - Higuchi 2011 and Zisimopoulou 2014 (LRP4, P04)
   - Correct the [Punga_2022] title: Lancet Neurol 2022;21:176-188, on epidemiology, diagnostics and biomarkers.
   - Correct the [Vincent_2003] year: Nat Rev Immunol 2002.
   - Record that literature and drug checks are no longer required by default, drop telithromycin, and restrict [Wolfe_2016] to thymectomy.
2. **ICD order.** 24 stable cases carry `icd_codes[0] = G70.01` ("with exacerbation") where G70.00 fits. G70.01 fits only M04, RM14 and RM15, and arguably RS14. A batch reorder needs approval (ROUND_POLICY 3), so it was left unchanged. S05 already has G70.00.
3. **Synonyms (`diagnosis_synonyms.yaml`).**
   - Split ocular and generalized MG: "ocular myasthenia gravis" is accepted in every generalized case, and "generalized myasthenia gravis" in RS11 and S05, so the distinction is never scored.
   - Drop the bare "MG".
   - Add:
     - "myasthenic crisis" (G70.01; RM14, RM15)
     - "myasthenic exacerbation" (M04)
     - "seronegative myasthenia gravis" or "double-seronegative generalized myasthenia gravis" (P01, RP14)
     - "paraneoplastic Lambert-Eaton myasthenic syndrome" and "LEMS with small cell lung cancer" (P02, RM13)
   - Consider a MuSK-MG label (RS14).
4. **`conditions.yaml`, myasthenia_gravis.**
   - `common_followups` lists stale names: `request_pulmonary_function` under interpret_labs, and `request_thymectomy_evaluation` under order_ct_scan.
   - The CSF note becomes "no CSF".
5. **Guidance claims (`condition_tool_guidance.yaml`, `test_guidance_claims.py`).**
   - Mediastinal CT is required in new-diagnosis MG.
   - P02 and RM13 use chest CT, with FDG-PET and tissue required.
   - Mediastinal CT is optional in M04, RM14 and RM15.
   - RM16's mediastinal criterion does not require contrast.
6. **Library (`fallback_library.yaml`).** Neutral head-CT normal wording at library level, if the "does not address the question" phrase comes from there.
7. **Vocabulary.**
   - `anti_titin` and `anti_RyR` are not orderable. They are optional additions as thymoma markers; until then the titin rows were removed in RM11 and S03.
   - There is no `endotracheal_aspirate` microbiology specimen; RM15 uses `sputum`.
8. **Harness or resolver (P04).** One `interpret_labs` call that lists `anti_AChR`, `anti_MuSK`, `anti_LRP4` and `TSH` is answered by the LRP4 follow-up alone, so the agent does not see the AChR, MuSK and thyroid report it ordered. Scoring is unaffected. Consider merging a set-valued lab follow-up with the initial report.
9. **Tests.** Add MG to `DISCRIMINATOR_CONDITIONS` in `agent-platform/tests/test_case_guards.py`. The guard now passes on all 30 MG cases (hand-run).
10. **SFEMG library normal (M04).** An SFEMG order in M04 is answered by the library's normal SFEMG, which a severe AChR-positive exacerbation would not produce. It is a waste avoided action there, so it is left as is; a library-level note may be enough.
11. **Plan fact 24.** Correct "ECG after titration" to "clinical and ECG monitoring at initiation and yearly thereafter, ECG at once if arrhythmia is suspected" (EU SmPC 4.4) for future rounds.
12. **`mediastinum_MRI` warnings.** The perfect-agent warnings for the `mediastinum_MRI` alternatives (library normal mediastinal MRI) are consistent with the cases without thymoma. Silence them centrally if wanted.

## Open questions for Andrea

1. **Composition.** P02 and RM13 are LEMS (G73.1), and M04, RM14 and RM15 are an exacerbation or crisis in already-diagnosed MG, a management task rather than a diagnosis. All five are kept with their labels and with the LEMS and crisis pathways of plan 3.5. Should LEMS move to a separate NMJ condition, and should the crisis cases become a management subtype? This is a benchmark-design choice only Andrea can make.
2. **ICD reorder (CENTRAL 2).** Do you approve setting G70.00 first in the 24 stable new-diagnosis cases? ROUND_POLICY 3 blocks workers from doing it.
