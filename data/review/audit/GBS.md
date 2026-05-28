# NeuroBench v5 audit — Guillain-Barré syndrome (GBS)

Scope: all 30 `GBS-*` case files in `data/neurobench_v5/cases/`. Every field of every
case read in full (patient, exam, all initial/followup/fallback tool outputs, entire
ground_truth, metadata) against `dataset-generation/criteria_packs/GBS.md`,
`TOOL_REPORT_STYLE_GUIDE.md`, and the `neuroagent_schemas` models.

Mechanical pre-checks (all 30 cases): coherence validator = 0 issues; schema
validation = pass; answer-leakage detector = 0 candidates; tool-vocab validator = no
GBS findings.

All 30 primary diagnoses are GBS (G61.0) — the `R`-prefixed cases are real-case-seeded
GBS variants with mimic-style red herrings, NOT cases whose true answer is a different
disease. No case has GBS as a wrong gold answer. CSF albuminocytologic dissociation,
NCS demyelinating/axonal patterns, ganglioside-antibody titres, and serial FVC/NIF are
within-modality confirmatory findings and were KEPT throughout (per scope note).

| case_id | dim | severity | region.field path | finding | action | detail |
|---|---|---|---|---|---|---|
| GBS-RS18 | A/B | major | followup_outputs[search_bell_palsy_gbs_overlap].output | `search_medical_literature` output used top-level key `conclusion` instead of schema-required `summary`; lacking `summary`, Pydantic's union mis-resolved the object to `CardiacMonitoringReport`, silently dropping both literature results and the query at runtime | FIXED | Renamed top-level `conclusion`→`summary`. Now resolves as `LiteratureSearchResult` with 2 results + summary intact. Only bare-form GBS literature output whose real content was being lost. |
| GBS-RS13 | E | minor | initial_tool_outputs.labs.abnormal_values_summary[1] | Summary listed "CRP 13.4 mg/dL"; the structured LabValue and `interpretation` both correctly use mg/L (CRP at 13.4 is mg/L; 13.4 mg/dL = 134 mg/L) | FIXED | Corrected display unit to mg/L to match the panel source of truth. No clinical-meaning change. |
| ALL 30 | A/B | major | followup_outputs[search_gbs_treatment / check_ivig_drug_interactions].output | Wrapped `{"general": {...}}` literature/drug-interaction followups (used in 28 of 30 cases for the boilerplate "no evidence retrieved" content) mis-resolve to `CardiacMonitoringReport` — the union expects a bare object, not a "general"-keyed dict | FLAGGED | Dataset-wide artifact of the documented "mirrored fallback into followup" migration (see each file's metadata.case_body_concerns). Affects ALL conditions, not just GBS; content is empty boilerplate so functionally inert. Out of conservative audit scope to mass-rewrite; needs a coordinated data-model/migration fix, not per-case edits. Distinct from the RS18 bare-form bug (fixed). |
| ALL 30 | C | major | ground_truth.optimal_actions[respiratory_function] vs followup_outputs | Bedside respiratory function (FVC/MIP/MEP/NIF) is delivered via an `interpret_labs` followup panel, not `order_specialized_test{test_type=respiratory_function}` as the criteria pack §2 mandates; an agent calling order_specialized_test{respiratory_function} hits the EMG/NCS output instead | FLAGGED | Pre-existing, self-documented in every file's metadata.case_body_concerns. Pathway/authoring issue, not a value error; left for the documented follow-up case-body pass. |
| GBS-RM11, RM12, RM13, RM14, RM15(n/a), RP11, RP12, RP14, RP15, RP16, RS15(n/a) | B | minor | followup_outputs[request_respiratory_monitoring].output.panels.Respiratory.FVC | Reduced FVC (e.g. 65%, 67%, 60%, 58% predicted) marked `is_abnormal=false` with `interpretation:"All values within normal limits"`, while the abnormal_values_summary simultaneously flags a declining trend; contrast M01/M02/RS12/RS14/S01/S02/S04 which correctly mark reduced FVC `is_abnormal=true` | FLAGGED | Inconsistent is_abnormal handling for sub-80%-predicted FVC across the RM/RP cases. Judgment on the correct threshold + part of the known respiratory-panel issue; not fixed to avoid regression. |
| GBS-RM13 | B/E | major | ground_truth.differential[Hepatic encephalopathy].key_features | key_features states "Encephalopathic features absent; bilirubin / ammonia not consistent" — but the case HAS baseline grade-1 hepatic encephalopathy (exam + HPI) and ammonia IS elevated (68 µmol/L, ref 11-35, is_abnormal=true) | FLAGGED | Differential rationale directly contradicts the case body. Touches ground_truth semantics → human adjudication of correct phrasing. |
| GBS-RM13 | C | major | patient.history_present_illness; difficulty/primary_dx | HPI states a 6-week progressive course yet asserts it "falls within the 4-week range required for the diagnosis" (6 ≠ ≤4); progression to nadir at 4-8 wk is subacute / >8 wk is CIDP. Pack nadir is 2-4 wk | FLAGGED | Internal contradiction + atypically long course for a GBS gold answer; clinician should adjudicate whether the GBS label and the "within 4-week" justification stand. |
| GBS-P02 | B | minor | patient.clinical_history / HPI vs labs.HIV.CD4 | History/HPI state CD4 380; labs report CD4 368 | FLAGGED | Small numeric mismatch (both <500, same direction); plausibly baseline-vs-current draw. Not fixed — unclear which is canonical and either edit changes a stated value. |
| GBS-P02 | C | minor | followup_outputs[csf].appearance | CSF "Clear, slightly xanthochromic" with RBC 0 and protein 88 — protein rarely high enough (<~150) to produce visible xanthochromia, and no blood | FLAGGED | Clinical-plausibility nit (contrast RM13/RS13 where xanthochromia is explained by jaundice/SAH). |
| GBS-P01 | C/D | minor | followup_outputs[request_literature_mfs].output | Literature result names "Miller Fisher syndrome" / anti-GQ1b and Bickerstaff — population-keyed, hedged, "clinical correlation required"; the case answer IS MFS | FLAGGED (intentional) | Stays population-level (no "this patient has MFS"); on the correct side of the leakage line. Noted as intentional, not a Kind-1 leak. |
| GBS-RP12 | C/E | minor | ground_truth.primary_diagnosis | Labelled "cranial-nerve variant (unilateral facial involvement)" but exam shows unilateral PTOSIS and explicitly "No facial weakness"; difficulty_description correctly says "unilateral ptosis" | FLAGGED | Parenthetical descriptor "facial" mismatches the ptosis presentation; touches primary_diagnosis text → do not edit; GBS cranial variant itself is correct. |
| GBS-RP11, RP13, RP15, RP16, S01, S04 | D | minor | initial_tool_outputs.ecg.findings[] | ECG `findings`/note reference non-cardiac context: a QT-prolonging drug by name (lenvatinib / citalopram / tacrolimus / daunorubicin-vincristine) or management ("avoid QT-prolonging medications") | FLAGGED | Style guide says ECG reports strip non-cardiac references + management. Borderline (within-cardiology QT-causation context); `interpretation` field itself stays clean. Consolidated; not edited to avoid overreach/regression. |
| GBS-RS11 | B/E | minor | followup_outputs[anti_ganglioside].abnormal_values_summary | Anti-GQ1b "Positive (1:40)" with is_abnormal=true, but summary tags it "(L)" (a positive antibody should not carry a low/down flag) | FLAGGED | Ambiguous whether "(L)" means "low titer" vs an erroneous direction flag; derived summary string only — left for reviewer. |
| GBS-RS15 | E | minor | initial_tool_outputs.specialized_test.impression | Garbled sentence: "Bilateral facial nerve motor responses incidentally show carpal tunnel syndrome pattern on median NCS" conflates facial nerve with median CTS finding | FLAGGED | Confusing prose (structured `findings` are correct); rewriting interpretive text risks overreach. |
| GBS-RP11, RP13 | C | minor | initial_tool_outputs.labs.panels.*.TSH.unit | TSH unit written "mIU/mL" (standard is mIU/L = µIU/mL; "mIU/mL" is ~1000× off); reference range 0.4-4.0 matches mIU/L | FLAGGED | Subtle clinical-units issue, applied consistently across exam + labs; RS18 correctly uses "µIU/mL". Not fixed — units judgment + touches lab value display. |
| GBS-M01 | C | minor | initial_tool_outputs.specialized_test.findings[Right median motor] | "CMAP amplitude 4.2 mV (reduced; normal >4 mV)" — 4.2 > 4, so labelling it "reduced" contradicts the stated cutoff | FLAGGED | Borderline-normal value called reduced; correct cutoff is a judgment (median CMAP LLN typically ~4 mV). |
| GBS-M02 | C | minor | difficulty / case_id `M` vs followup severity | "Mild" (M) subtype + difficulty "moderate", but followups show FVC 50%, NIF crossing threshold, hypertensive crisis, ICU telemetry — clinically severe | FLAGGED | Subtype-label vs clinical-trajectory mismatch; subtype taxonomy judgment, not a data fix. |
| GBS-P01 | C | minor | case_id `P` vs clinical content | Miller-Fisher case has NO limb weakness and normal respiratory function (FVC 91%); pack's `P` = "progressive/severe, ICU". Difficulty="diagnostic_puzzle" fits, severity does not | FLAGGED (light) | Dataset appears to use `P` for the puzzle tier here; pack `P` description is severity-based. Noted; ambiguous by design. |
| GBS-RM16, RS14 (+ others) | E | nit | metadata.difficulty_description vs ground_truth.red_herrings | difficulty_description narrates embedded red herrings (triple seropositivity, T4 pseudolevel, flu vaccine) while the structured `red_herrings` array is empty (difficulty_rationale "0 red herrings") | FLAGGED | Documentation gap; populating red_herrings is ground_truth authoring (judgment). |
| ALL with interpret_labs string panels | E | nit | followup_outputs[*].output.interpretation (10 files) | Doubled-unit artifact in auto-generated interpretation strings: value already contains the unit and the unit is appended again — "FVC 2.2 L L (H)", "NIF -28 cmH2O cmH2O (H)", "CD4 368 cells/mm3 cells/mm3 (L)", "SpO2 93% % (H)" | FLAGGED | Systematic generator cosmetic artifact (M01,M02,M03,P02,RS13,RS17,RS18,S01,S02,S04). Structured value+unit individually correct; display-only. Editing 10 files' derived strings is cosmetic with regression risk — flagged as one finding. |
| ALL fallback buckets | E | nit | fallback_tool_outputs.*.impression | British spelling ("haemorrhage", "organisation") in fallback boilerplate vs American spelling in case bodies | FLAGGED | Cosmetic terminology inconsistency confined to shared fallback boilerplate. |

## Tally

- Cases audited: **30 / 30** (every GBS- file, read in full).
- Findings by severity: **major 5** (RS18 schema mis-resolution [fixed]; dataset-wide
  wrapped-literature/drug mis-resolution; dataset-wide respiratory-via-interpret_labs
  pathway; RM13 differential-contradicts-body; RM13 6-week-course contradiction) ·
  **minor 11** · **nit 3**.
- Fixed vs flagged: **2 FIXED** (GBS-RS18 `conclusion`→`summary`; GBS-RS13 CRP mg/dL→mg/L)
  · everything else **FLAGGED**.
- Mechanical state after fixes: coherence **0** and schema **pass** on both edited files;
  full GBS set still coherence 0 / schema valid; only `GBS-RS13.json` and `GBS-RS18.json`
  changed (1 line each); literal-unicode and trailing-newline conventions preserved.

## Top clinical-correctness flags for human adjudication

1. **GBS-RM13** — differential entry "Hepatic encephalopathy / metabolic neuropathy"
   says "encephalopathic features absent; ammonia not consistent", but the patient has
   documented baseline hepatic encephalopathy and ammonia 68 µmol/L (elevated). The
   reasoning contradicts the case's own data.
2. **GBS-RM13** — 6-week progressive course is stated, then justified as "within the
   4-week range required for GBS" (it is not). A 4-8 week nadir is subacute and >8 weeks
   is CIDP; confirm the GBS gold answer and rewrite the timeline justification.
3. **GBS-RS18** (schema, FIXED) — the only bare-form literature followup with real
   content was being silently discarded at runtime (mis-resolved to a cardiac-monitoring
   object). Fixed; flagging for awareness that the same `summary`-key requirement should
   be checked in other conditions' bare-form literature outputs.
4. **Dataset-wide (not GBS-specific)** — the `{"general": {...}}`-wrapped
   literature/drug-interaction followups mis-resolve under the `FollowUpToolOutput.output`
   union. Empty boilerplate here, but the same wrapper is used across all conditions and
   warrants a coordinated data-model fix.
5. **GBS-RP12** — primary_diagnosis says "unilateral facial involvement" but the
   presentation is isolated unilateral ptosis with explicitly no facial weakness; confirm
   the descriptor (the GBS cranial-variant diagnosis is otherwise sound).
