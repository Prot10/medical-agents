# NPH: condition summary of the October 2026 review round

Condition auditor, 24 October 2026. Sources: the plan (`plans/NPH.md`), the 30 case logs
(`logs/NPH-*.md`, each with a worker table, a verifier section and, for 23 cases, a
"Condition audit" section), and scripted checks over the 30 case files (M01 to M10, P01 to P09,
S01 to S11). NPH has never been annotated by a physician: there is no `notes/NPH.md` or `.json`,
so there are no note ids to rule on. Every change comes from the lead survey, the workers, the
verifiers or this audit. All 30 cases are `draft`; none was approved before the round.

## Final state

- `perfect_agent.py` on all 30 ids: 30/30 pass.
- `case_io.py check` on all 30 ids: schema OK and synonym guard OK for every case. The suite's 15
  failures are elsewhere and none names an NPH case.
- `test_case_guards -k NPH`: 60 passed.
- `discriminator_defects` (not yet run on NPH by the suite, since NPH is not in
  `DISCRIMINATOR_CONDITIONS`): exactly one defect in each of the 30 cases. It is the post-tap
  follow-up's `assessment_type` "gait_and_balance_timed (post-tap reassessment)", which is a prose
  value by design (plan C6). The routing it relies on works today, but NPH cannot join the guard
  until R4 lands or the guard exempts timing follow-ups (see CENTRAL below).
- Scripted uniformity checks, all clean after the audit fixes:
  - Criteria in pathway order with plan 3.1 tiers.
    - Required in every case: MRI, baseline `gait_and_balance_timed` and CSF.
    - Post-tap reassessment: recommended, trigger `request_post_reassessment`.
    - MoCA: optional, trigger `request_moca_cognitive_screen`.
    - Labs: optional, except recommended in M04, M07, M08 and S08.
    - Spine MRI: recommended in M04 and P03, optional in M07 and M10.
    - P08 extended drainage: recommended.
    - P09 AD biomarkers and neuropsychological battery: optional.
    - P01 AD biomarkers: recommended.
    - P06: the cytology alternatives sit on the required CSF criterion.
  - Sequence constraints are exactly the two canonical ones: MRI before CSF (hard) and baseline gait before CSF
    (soft), with the plan's reasons. No constraint names the post-tap or P08 drainage criterion.
  - Stop rule: the three required ids, allowance 1.
  - Literature: no criterion and no output anywhere.
  - Drug checks:
    - no criterion except P06's optional `action-drug-interaction-tamoxifen`, an accepted deviation;
    - outputs are null except P06's initial `drug_interactions`.
  - Avoided actions:
    - EEG, ECG, echo, CT, cardiac monitoring, advanced imaging and the neuropsychological battery
      are `waste` (the battery entry is absent in P09);
    - the generic CSF assays are `waste` everywhere with 14-3-3, RT-QuIC, oligoclonal bands, the
      meningitis panel and HSV PCR (after this audit, see A4).
  - Fallbacks:
    - `echo_type` TTE and `monitor_type` holter_24h;
    - every CT fallback describes the patient's own ventricles.
  - VCI likelihood in the differential agrees with the Fazekas grade in all 30 cases.
  - Prohibitions:
    - the canonical ventriculomegaly-alone prohibition is in all 30, with at most 5 prohibitions
      per case;
    - the AD prohibition appears only in M04, P01 and P09.
  - Every case-specific must from the plan is present.
  - Labs:
    - HbA1c reference is "<5.7" wherever HbA1c appears;
    - RPR and HIV sit in a `Serology` panel wherever they appear (after A5).
  - MoCA: every follow-up's Attention subscore matches its findings under the MoCA scoring rules
    (after A1); the subscores sum to the total in all 30.

## Error classes and how each was fixed

The counts give the number of case logs that cite each class. The plan's C1 to C20 are applied
uniformly.

| Class | Cases | Fix |
| --- | --- | --- |
| C1 Literature search as a clinical step, with leaks | 30 | Literature criteria and outputs removed (rulings 1 and 5). |
| C2 Drug-interaction checks as perioperative management | 26 | Removed. Anticoagulant handling moved into musts and prohibitions with ASRA 2018 facts: DOAC hold at least 72 h, restart no sooner than 6 h, no bridging. P06's tamoxifen and duloxetine check is kept as optional. |
| C3 Patient block gives imaging measurements and the referral diagnosis | 30 | Evans index, callosal angle, DESH, "NPH evaluation" and "tap trial" removed from the CC, HPI and PMH. Outside imaging is described qualitatively. M09 keeps an older Evans 0.30, which documents change. |
| C4 Exam gives gait and cognitive results | 30 | Exams are qualitative. TUG, 10-m walk and MoCA numbers moved to the baseline gait report and to a MoCA follow-up. |
| C5 Reports state the diagnosis, tap verdict or management | 27 | Each report gives its own modality's findings. The CSF report gives the tap figures without a verdict. |
| C6 Baseline gait report already contains the post-tap result | 30 | Baseline-only gait report. A new `request_post_reassessment` follow-up (prose `assessment_type`, see R4) repeats the measures, and a new recommended criterion scores it. |
| C7 MRI reports with missing markers, spine content or impossible values | 30 | Every MRI gives technique, Evans index above 0.3, temporal horns with an MTA or hippocampal score, callosal angle, DESH status, Fazekas grade, aqueduct and fourth ventricle. Spine findings moved to spine MRI follow-ups. |
| C8 Imaging carry-over in the PD cases | 3 | M05 and P02 MRIs no longer name Parkinson's disease from the nigral signal (finding only). P07 MRI drops the cross-study commentary and gives the midbrain-to-pons value as a diameter ratio. |
| C9 Lab template carry-over | 30 | Removed the "Baseline workup" HIV rows with templated significance, prose references and interpretive summaries. `clinical_significance` is null everywhere. Labs are case-specific: M07 B12 and MMA, M08 coagulation and platelets. |
| C10 Advanced imaging and neuropsych would be contradicted by the library | 13 | Waste entries added. Copathology cases that need them have authored outputs (P01, P09). |
| C11 Musts are process steps | 30 | Musts are case management: shunt referral with counselling, comorbidity actions, falls prevention. |
| C12 Wrong prohibition criterion and AD carry-over | 30 | The wrong "DESH, callosal angle and triad required" prohibition was replaced by the canonical ventriculomegaly-alone prohibition. The AD prohibition is kept only where AD is in question. |
| C13 Differential not at the assessment-time view | 30 | Likelihoods set for the state after MRI, gait and tap. VCI follows Fazekas. |
| C14 Spine imaging with a spinal mimic | 3 | Authored spine MRI follow-ups and tiers per 3.1 (M04, P03, M07/M10). |
| C15 P07 breast-cancer carry-over | 1 | Removed. The PSP label is weighed with Massey 2013, midbrain-to-pons ratio below 0.52. |
| C16 P08 drainage hijacking the index tap | 1 | A drainage follow-up with trigger `repeat_csf_analysis`, scored by a recommended criterion. No constraint names it. |
| C17 CSF follow-ups must repeat the whole tap report | 3 | Follow-ups carry the full report. |
| C18 Fallbacks contradict the case | 30 | CT fallbacks show the patient's own ventricles, with burr holes where relevant. Echo and monitor discriminators are set. |
| C19 Metadata and criterion text | 20 | Canonical sequence reasons, stop rule, tier sentences and case-specific rationales. |
| C20 Red herrings | 16 | Data points made visible and interpretations rewritten. Neuropathy red herrings deleted where the exam has no neuropathy signs (plan Q7 default). |

### Auditor findings (this pass)

| Id | Class | Cases | Change |
| --- | --- | --- | --- |
| A1 | MoCA attention subscore not derivable from the findings | M07, M08, M09 | Findings reworded so the MoCA rules give the stored 4/6, 4/6 and 3/6 (forward 1, backward 1, tapping 1 with 0 for 2 or more errors, serial 7s 3/2/1). M07 and M08: digits backward failed and two serial-7 errors. M09: two letter-tapping errors added. Totals unchanged. |
| A2 | Post-tap rationale copied verbatim | P03, P04, P05, P06, P07 | Each sentence is now case-specific: tap volume, and what the reassessment separates (myelopathy, bvFTD, the SAH, carcinomatosis, the PSP label). |
| A3 | `[Tisell_2011]` cited for the tap test | M07, M08, M09, M10, P01 | Removed from `action-4-analyze-csf.citations`. The pack entry is Tisell 2011, shunt surgery with white matter changes, and these rationales are about the tap response only. S09 and S11 keep it: their rationales are about white matter. The plan's table wrongly lists Tisell as "tap-test predictors" (CENTRAL). |
| A4 | HSV PCR missing from the generic CSF waste entry | S06 to S11 | Added. It was already present in the other 24 cases. |
| A5 | RPR, and in P09 also HIV, listed under `Metabolic` | P09, S01 to S05 | Moved to `Serology`. Values unchanged. |
| A6 | Interpretive clause in the exam | P03 | "could reflect myelopathy or peripheral neuropathy" removed from `neurological_exam.sensory`. It stated the differential that red herring 2 tests. |

Checked and left unchanged:
- M05 exam, "Minimal response to today's levodopa dose (on medication)": an observation consistent
  with the HPI (good initial response, now declining) and the ON-state baseline.
- The em dashes still in unedited patient text in M01 to M06, P03, P04 and P06, left by policy.
- Citation-key style: M07 to M10, P01 and S06 to S11 use pack keys only, and the others use
  `[Nakajima_2021]`. Both are valid until R2 lands.
- Template gait numbers recur in M02, M10, P05, P09, S01 and S02 (baseline TUG 28 s, 10-m walk
  22 s, 2-hour TUG 22 s). They are plausible and agree within each case.
- HIV and RPR were removed in M07 to M10, P01 and P02 but kept elsewhere. This is acceptable
  variation in a reversible-cause screen.

## Counts

- Notes: FIXED 0, ALREADY-FIXED 0, DECLINED 0, BLOCKED 0. There is no notes file.
- Own findings:
  - fixed: 560 worker-table rows, all FIXED; verifier fixes in 27 of the 30 cases (3 had none);
    26 field edits by the auditor in 23 cases (A1 to A6);
  - flagged: 4 classes, all central (discriminator guard, citation keys, pack text, library
    normals). No case-level item is left open.
- Cases changed: 30 of 30.
- Approved cases changed: 0. No NPH case was approved.

## DECLINED and BLOCKED notes

None. No note ids exist.

Deviations from the plan that the workers or verifiers logged and kept on purpose:
- M04: DESH kept, and the AD prohibition kept.
- M06: CHA2DS2-VASc 2.
- M08: Child-Pugh B with score 7, derived from the stored values; the plan said A.
- M09: the ex vacuo differential entry added.
- M10: a 1-hour value.
- P04: PSP carry-over removed.
- P06: duloxetine and tamoxifen interaction kept as optional.
- P07: MDS-PSP caveat.
- P08: 24-hour values.
- S09: hip weakness removed.
- S10: CHA2DS2-VASc 4.

## CENTRAL requests (consolidated)

1. **R1.** Add G91.3 to the accepted codes for M09 (post-traumatic hydrocephalus), then run
   `apply_diagnosis_synonyms.py`.
2. **R2.** Add the citation keys `[Nakajima_2021]`, `[Halperin_2015]`, `[ASRA_2018]` and
   `[Massey_2013]`, then correct the NPH criteria pack:
   - `[Relkin_2005]` pages should be S4-S16;
   - `[Marmarou_2005]` should be "The value of supplemental prognostic tests for the preoperative
     assessment of idiopathic normal-pressure hydrocephalus", S17-S28 (the pack lists the wrong
     title and S1-S52);
   - line 30 attributes the tap test to Tisell and says "opening pressure must be <25 cmH2O"; the
     tap test is Marmarou 2005, and the pressure criterion is Relkin 2005;
   - the tap-test "sensitivity ~50-80%" should become the F4 figures;
   - the required-tools list and tiers are superseded.
   The NPH plan's table entry "Tisell 2011: tap-test predictors" is also wrong. Tisell 2011 is
   about shunting with white matter changes (J Neurosurg 2011;114:1432-1438).
3. **R3.** Add `lumbar_drain` to `analyze_csf.source`, with its library entry and the `tool_io.py`
   mirror, so P08's drainage can be told apart from the tap.
4. **R4.** Add an assessment timing discriminator (enum `baseline` / `post_intervention`, or a
   scorer discriminator). Without it:
   - the post-tap criterion is credited by the baseline call alone;
   - NPH cannot join `DISCRIMINATOR_CONDITIONS`: all 30 cases fail `discriminator_defects` only
     on the prose post-tap `assessment_type`.
   When R4 lands, migrate the 30 follow-ups to the vocabulary value plus the timing field. Until
   then, an exemption in the guard for timing follow-ups is the alternative.
5. **R5.** In the MockServer `is_repeat_call`, count only earlier calls answered by the same
   discriminator value.
6. **R6.** Move the reasoning out of `accepted[0]` in P06 and P07 in a central relabel.
7. **R7.** Add condition-keyed library normals, or mark them. Today the library's normal MoCA,
   neuropsychological battery, DaTscan and amyloid reports contradict copathology cases that lack
   their own output.
8. **R8.** Add a realistic-context mode to `perfect_agent`. Also, `-v` prints "<- ?" for
   `None`-valued fields: serialise with `exclude_none` so the display is not mistaken for a miss.
9. Add a CPIC key (Goetz MP et al., Clin Pharmacol Ther 2018;103:770-777) for the P06 tamoxifen and CYP2D6 interaction. The optional criterion has no citation, and the duloxetine must cites CPIC in words only.

## Open questions for Andrea

1. **Copathology referral.** Should copathology cases (P01, P04, P09, M05, P02) score an
   unconditional shunt referral with counselling, as now, or a referral conditional on goals of
   care?
2. **Post-tap tier.** Should the post-tap reassessment become `required` once R4 can tell it apart
   from the baseline?
3. **DOAC hold.** The cases use ASRA 2018, which holds apixaban and rivaroxaban for at least 72 h
   before a neuraxial puncture. Some services use 48 h for a diagnostic LP. Confirm ASRA.
4. **P09 biomarker platform.** The CSF AD biomarker limits are written as assay-specific
   (Lumipulse-type cut-offs). Should a particular platform be named?
5. **Template gait numbers.** Six cases share the same baseline values. Diversify them in a later
   round, or accept them as plausible?
