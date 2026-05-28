# NeuroBench v5 — ALS case audit

Auditor: automated field-by-field audit per `.claude/skills/neurobench-case-audit/SKILL.md`.
Scope: all 30 `ALS-*` cases. Clinical reference: `dataset-generation/criteria_packs/ALS.md`.
Realism reference: `dataset-generation/TOOL_REPORT_STYLE_GUIDE.md`.

Mechanical validators (all 30 cases): coherence validator **0 issues** every case; schema
`NeuroBenchCase.model_validate_json` **passes** every case; tool-vocab validator reports
**no ALS findings**; answer-leakage detector flags only 2 candidates (ALS-P02, ALS-S10),
both general/population-keyed C9orf72 literature summaries that are legitimately KEPT.

No inline fixes were made: every issue found is a judgment call (clinical plausibility,
realism boundary, subtype labeling, or metadata semantics) that the conservative fix policy
requires be FLAGGED, not edited. Lab `is_abnormal` flags were programmatically checked against
numeric reference ranges across all initial + followup panels — zero true mismatches (NIF
negative-pressure entries are correctly flagged once the ">-70 cmH2O = stronger" convention is
applied).

| case_id | dim | severity | region.field path | finding | action | detail |
|---|---|---|---|---|---|---|
| ALS-M07,P06,P05,P09,M08,M06 (+others) | D | minor | initial_tool_outputs.specialized_test.quantitative_data / findings[].finding | EMG reports embed explicit named-mimic refutation essays and case-answer naming (e.g. `als_features: "PRESENT"`, `anti_mag_features: "ABSENT"`, `poems_features: "ABSENT"`, `lead_neuropathy_features: "ABSENT"`, "Normal sensory NCS excludes these diagnoses", "MS does not cause lower motor neuron signs"). EMG may reach a hedged within-modality conclusion, but these go beyond the style guide's "at most ONE hedged alternative sentence" and do the agent's differential-resolution work. | FLAGGED | Recurring pattern across the EMG `quantitative_data`/findings of most ALS cases. Borderline Kind-1 leakage; judgement needed on whether to trim the explicit "excludes X / als_features PRESENT" phrasing to pure electrophysiological description. Detector does not catch these (within `order_specialized_test`). |
| ALS-M07,P02,P08,P09 | A/E | minor | metadata.case_body_concerns[0] | The templated genetic-panel `case_body_concern` ("ALS genetic panel is wired to interpret_labs rather than order_specialized_test") is stale: M07 has NO genetic-panel followup at all; P02/P08/P09 deliver the genetic result in the **initial labs** panel, not via an interpret_labs followup. | FLAGGED | Metadata semantics — do not rewrite per fix policy. The concern text is accurate for the other 26 cases (genetic via interpret_labs followup). Verified programmatically. |
| ALS-RM11, ALS-RS11 | C | minor | case_id prefix vs criteria_packs/ALS.md §6 | Criteria pack §6 defines the `R` subtype as "reverse/mimic — the case is NOT ALS". Both ALS-R cases ARE ALS (RM11 limb-onset ALS; RS11 classic advanced ALS). Here `R` = real-seeded (v2 lineage), per CLAUDE.md case-ID convention, NOT reverse/mimic. | FLAGGED | The two meanings of `R` collide. Either the pack's subtype note is misleading for this dataset, or ALS lacks a true mimic case. No genuine ALS-mimic ("not ALS") case exists in the ALS- set. Human design decision. |
| ALS-S10 | C | minor | initial_tool_outputs.labs.Neuromuscular_Panel CK | CK 1240 U/L ≈ 7.1× ULN (ref 38-174). | FLAGGED | Exceeds the 2–5× ULN band the case's own key_reasoning_points cite as "consistent with ALS"; pack says >10× suggests myopathy. Defensible in young-onset/rapidly-progressive C9orf72 ALS but at the high edge — plausibility check for a clinician. |
| ALS-P04 | C | minor | initial_tool_outputs.labs.Neuromuscular_Panel CK | CK 1120 U/L ≈ 6.4× ULN (ref 38-174). | FLAGGED | Same as S10 — above the 2–5× band the case asserts. Flail-arm ALS with massive cervical denervation can run higher; mild internal tension with the templated reasoning point. |
| ALS-P08 | B | minor | ground_truth.differential | Primary dx is SOD1 A4V ALS, confirmed POSITIVE in the **initial** labs (Familial_ALS_Panel). Yet "Familial ALS, non-SOD1 (C9orf72/TARDBP/FUS)" is ranked `high` and "Sporadic ALS" `moderate` in the differential — inconsistent with data already on hand. | FLAGGED | Defensible as pre-test reasoning state, but a clinician reading the case sees the genetic answer and the differential side-by-side. Also: differential key_features cite an androgen-receptor CAG result that is NOT in the case's labs panel. |
| ALS-M02 | B | minor | ground_truth.differential[3].key_features vs neurological_exam | Exam states "No bulbar findings" / "Tongue midline, no atrophy or fasciculations"; flail-arm differential entry asserts "bulbar UMN signs present". | FLAGGED | Internal contradiction between differential prose and the exam. Likely templated leakage from a bulbar case. Judgement (touches ground_truth meaning) — flag, don't edit. |
| ALS-P03 | B | minor | ground_truth.differential | Lists both "ALS with coincidental low-titer anti-GM1" (very_high) and "Lower motor neuron-predominant ALS variant" (moderate) as separate entries when primary dx is ALS — partially redundant (both are ALS). Ordering itself is valid (descending). | FLAGGED | Differential-construction judgement; not a mechanical error. |
| ALS-P05 | C | minor | initial_tool_outputs.labs.Neuromuscular_Panel "JC virus serology" | JC virus serology Positive (1:64) flagged `is_abnormal=true`, ref "Negative preferred". JC seropositivity is common (~50-60% of adults) and clinically relevant mainly for natalizumab-associated PML risk — this patient is on HIV ART, not natalizumab. | FLAGGED | Contrived/low-relevance inclusion and an unusual "abnormal" framing for a population-prevalent antibody. Clinician plausibility note. |
| ALS-P01 | C | nit | difficulty / case_id "P" subtype | Difficulty `diagnostic_puzzle`; "P" prefix. Pack defines P = "progressive (rapid progression OR respiratory involvement)". This case is a benign-fasciculation-vs-ALS puzzle with NORMAL respiratory function (FVC 86%, SNIP 82). | FLAGGED | The dataset's P set is used more broadly (puzzle/progressive) than the pack's narrow P definition. Loose-but-consistent convention; noted, not actioned. |
| ALS-M01 | E | nit | initial_tool_outputs.mri.differential_by_imaging | `differential_by_imaging` is `[]` while the MRI `impression` text gives a worded imaging differential (wallerian degeneration / demyelination / other). Same pattern in M02/M03/etc. | FLAGGED | Stylistic — the structured field is empty but the prose carries the differential. Not load-bearing; no fix. |
| ALS-M04, M03 (+others) | C | nit | optimal_actions step 3 panels vs initial_tool_outputs.labs | Gold action step 3 lists RPR (and a full panel incl. HbA1c, Free T4) but the actual initial labs panel omits RPR in several cases. | FLAGGED | The rendered labs panel is a representative subset of the gold-action panel list; acceptable simulation. Noted for completeness. |
| ALS-M01 (+ all M/S/P) | C | nit | optimal_actions step 6 tool_parameters genetic list | Gold step-6 genetic panel lists "C9orf72, SOD1, TARDBP, FUS, **TBK1**" but the rendered genetic panels test C9orf72/SOD1/TARDBP/FUS/UBQLN2/VCP (no TBK1). | FLAGGED | Minor mismatch between the gold-action gene list and the simulated panel contents; both are plausible ALS gene sets. No fix. |
| (all 30) | D | info | initial_tool_outputs.* normal/incidental reports | EEG/ECG/echo/CT/cardiac-monitoring fallback and incidental reports are modality-faithful, terse, no cross-modality synthesis. CSF NfL, genetic, and antibody confirmatory results are within-modality (Kind-2) and correctly KEPT. | (none) | No Kind-1 leakage in non-EMG reports. |

## Tally

- **Cases audited:** 30 / 30 (ALS-M01–M08, ALS-P01–P09, ALS-RM11, ALS-RS11, ALS-S01–S11), every field read.
- **Findings by severity:** blocker 0; major 0; minor 9; nit 4; info 1.
- **Fixed vs flagged:** **0 fixed, 14 flagged.** No unambiguous mechanical error was found, so per the
  conservative fix policy nothing was edited inline.
- **Validators:** coherence **0** (all 30, unchanged — never touched); schema **passes** (all 30);
  tool-vocab **no ALS issues**; leakage detector **2 intentional candidates** (P02, S10 — general
  C9orf72 literature, KEPT).
- **Files changed by this audit:** none (zero ALS- files edited; unicode/newline conventions preserved
  trivially). 

### Top clinical-correctness flags for human adjudication

1. **EMG within-modality differential-refutation essays** (M06, M07, M08, P05, P06, P07 and others):
   EMG `quantitative_data`/findings name the case answer ("als_features: PRESENT") and argue named
   mimics away ("excludes these diagnoses", "MS does not cause LMN signs"). Decide whether these
   exceed the style guide's single-hedged-sentence allowance and should be reduced to pure
   electrophysiological description.
2. **`R` subtype mismatch** (RM11, RS11): the criteria pack labels `R` as a non-ALS mimic, but both
   ALS-`R` cases are genuine ALS (real-seeded). The ALS set therefore has no true "not-ALS" mimic case.
   Decide whether the pack §6 note or the dataset composition should change.
3. **High CK values** (S10 = 1240 U/L ≈7×ULN; P04 = 1120 ≈6.4×ULN): both exceed the 2–5× ULN band
   the cases themselves cite as "consistent with ALS." Confirm clinical plausibility for young-onset /
   flail-arm ALS or adjust toward the stated band.
4. **ALS-P08 differential vs confirmed genetics**: SOD1 A4V positive in initial labs while "non-SOD1
   familial ALS" is ranked `high` in the differential, and a CAG-repeat result cited in differential
   key_features is absent from the labs panel. Confirm intended pre-test framing.
5. **ALS-M02 bulbar contradiction**: differential prose asserts "bulbar UMN signs present" but the
   exam documents no bulbar findings / normal tongue. Reconcile.
