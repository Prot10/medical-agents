# GBS: condition summary of the October 2026 review round

Condition auditor, 24 October 2026. Sources: the plan (`plans/GBS.md`), the 30 case logs
(`logs/GBS-*.md`, each with a worker table, a verifier section and, for 20 cases, a "Condition
audit (24 Oct 2026)" section), the notes (`notes/GBS.json`, 68 notes, all from Reviewer 2) and
scripted checks over the 30 case files.

## Final state

- `perfect_agent.py` on all 30 ids: 30/30 pass. `case_io.py check` on all 30 ids: schema OK for
  every case, synonym guard OK, and no test failure names a GBS case or the condition (the suite's
  other failures belong to conditions still being edited and to the central claim tests).
  `pytest agent-platform/tests/test_case_guards.py -k GBS`: 60 passed (leak, follow-up and
  banned-string guards).
- Every one of the 68 note ids appears in exactly one log (its own case), in exactly one table row,
  with a ruling.
- Scripted uniformity checks over the 30 files (all clean after the audit fixes below):
  - Template strings gone everywhere: `anti-GM1 IgM`, bare `van_den_Berg_2014`, "GBS criteria pack",
    `[EAN_PNS_GBS_2023]`, "which is what this case's diagnosis rests on", "corticosteroids as
    monotherapy", "Do not combine IVIG and PE", IgA prohibitions, "guideline recommendation" as an
    evidence level, "VC <40%", "variant typing", "trigger identification", "intubation threshold",
    "CONTRAINDICATED", "off-pathway", "which agents to taper", "(N/A PMN/N/A lymph)", the old
    trigger `request_anti_ganglioside_panel`, `request_repeat_ncs`, edrophonium follow-ups.
  - No antecedent-infection serology or PCR in any current-encounter lab report. Campylobacter is
    named only where a prior stool culture is history (P03, S01) or as a red herring's intended
    effect (RS12).
  - Ganglioside follow-ups exist only in P01, RM12, RM15, RS11, RS15, RS18, all with trigger
    `request_anti_gq1b_gt1a_ganglioside_panel` and tool `interpret_labs`; no criterion scores them
    (BLOCKED on CENTRAL 1). Every positive result is interpreted.
  - Criteria: a2, a3 (with the case-specific exceptions below), a1, a4 and a8 required; a7
    recommended; a5 optional and last in all 30. a1 args are `CBC, CMP, CK` (plus `coagulation` in
    RM13, RP16, RS13, RS16 and `troponin` in RP11). Canonical a1/a2/a3/a4 labels and evidence,
    except where the case's own data differ and the text says so (P01, P02, P03, RM13, RM15, RP11,
    RP12, RP13, RP14, RP15, RP16, RS13, RS16).
  - Order: NCS first, then CSF, then mimic-exclusion criteria, labs, respiratory, telemetry, ECG,
    DDI, literature, in 23 cases. Logged departures: P01 (brain MRI first, posterior fossa stroke
    before LP), RS12 (spine MRI first, before LP near a fresh laminectomy), RS13 (respiratory first,
    desaturating), RM13, RP16, RS16 (labs, and in RS16 the DDI, before the LP as the hard
    constraints require).
  - Sequence constraints: no `action-2 -> action-6` constraint anywhere. Hard constraints only in
    RM13, RP16 (labs before LP) and RS16 (labs and DDI before LP), per C13. Soft constraints: labs
    before DDI where a6 is required, RS12 spine MRI before LP, RS13 labs before LP.
  - Stop rule: `required_before_assessment` equals the set of required criteria in all 30;
    `max_additional_actions` is 3 everywhere.
  - Every case has weight and height in `patient.physical_exam.general`, consistent with the BMI.
    Every respiratory follow-up gives FVC in L, % predicted and mL/kg, MIP and MEP, flags low values
    L (the only "(H)" is a raised PaCO2), and none says "within normal limits". No spirometry in
    any patient block. Ventilated cases (RS13, RS16, RS17, RS18) report the last pre-intubation
    values.
  - ICU-level musts are present wherever a trigger is met (FVC <60% predicted or <20 mL/kg, MIP
    weaker than -30, MEP <40, bulbar weakness with weak cough); cases that meet none (M03, P01, P03,
    RM11, RM14, RM15, RP13, RP15, RS11, RS14) have a monitored bed with named escalation triggers.
    FVC <60% is an ICU-level trigger, never an intubation criterion (RP14, RP16 corrected by the
    verifiers).
  - Every telemetry report covers the first 24 hours, findings only, no treatment.
  - Brighton level quoted at most once per case, never in the variants without limb weakness.
  - Canonical steroid prohibition in 27 cases; RP15 and RP16 use it with a clause for maintenance
    or induction prednisone; RP11 (ICI-related GBS) has methylprednisolone as a must under
    ASCO 2021 / ESMO 2022 and "no ICI rechallenge" instead.
  - Brain MRI is served only by `analyze_brain_mri`, chest CT by `order_body_imaging`.

## Error classes and how each was fixed

| class | defect | notes | fix |
| --- | --- | --- | --- |
| C1 respiratory values | FVC 55-94% labelled "within normal limits" or low values flagged H; no weight, no mL/kg, no MEP; spirometry and "at intubation threshold" in the patient block; single-threshold intubation text; wrong 20/30/40 wording | 1b3ba3ad, 9dc82346, 38ccdb70, 2a09feee, a2cd5342, 2f754e55, 61e678b0, 33eaec73, b0808edf, d4baaeb9, ed62b4ac, 0a7f2022, 693830c4 | Weight and height in every case; canonical respiratory report with trend; patient block keeps clinical signs only; ICU-level musts with named triggers and multi-factor intubation musts; canonical a4. MIP/MEP reference ranges are age- and sex-specific lower limits (Evans and Whitelaw 2009). S01's FVC pair re-derived from 22 mL/kg; RS18's predicted FVC corrected by the verifier. |
| C2 ganglioside antibodies | `anti-GM1 IgM` required in all 30 while IgG was reported; trigger unreachable; positive results uninterpreted; panel "for variant typing" | a69c5ec7, 4d885b61, ae0f3536, 09291641, ee1e4f06, 22430160, 39b7526d | Removed from a1 in all 30. Panel deleted in the 24 typical cases with the canonical pearl; kept as anti-GQ1b/GT1a only in the six MFS-spectrum, PCB, bifacial and ophthalmoplegic cases, reachable by clinical_context; criterion BLOCKED (CENTRAL 1). Label suffix "anti-GM1 / GD1a positive" (RP16) and "multi-antibody positive" (RS16) removed. |
| C3 antecedent infections | Unorderable Campylobacter, CMV, EBV, HSV, Mycoplasma serology and influenza PCR in current labs; labels asserting a trigger the history does not support; musts demanding trigger identification | 6644822c, 40837d83, 39b7526d, 8241358d, bc02717e, 4021807f, 3c94e91e, e48d42bd | Serology deleted from all current labs; antecedents named only as the history supports (URI, diarrhoeal illness, culture-confirmed enteritis in P03/S01, influenza swab dated to the GP visit in S04, triple IgM as dated prior serology and red herring in RM16); canonical antecedent pearl; mEGOS diarrhoea point where prognosis is discussed. 10 labels lost their trigger attribution. |
| C4 variant labels | AMSAN label on demyelinating numbers, "generalized" with legs only, no arm weakness, course >4 weeks, bifacial without paraesthesias, isolated bulbar or ptosis presentations | 0b90c02f, 0ddd925b, e89ffe81, c1f03f5c, 98e9377c, 8e2833d3, 9fee5e3b, 9f5f1a74, cfa3beb7 | Findings edited to meet the label (P03 mild weakness, RM14/RP15 arm involvement, RM13/RP15 course within 4 weeks, RS11 paraesthesias with 5/5 limbs, RS15 PCB with neck and arm weakness, RM15 anti-GQ1b positive) or label changed to the findings (RM14 AIDP, RP12 left ptosis). Subtype words kept only where the NCS meets them. |
| C5 differential not updated | Mimics left moderate/high after the work-up (MG, botulism, CIDP, myopathy, CIP, encephalitis, leptomeningeal disease, HIT, cervical stenosis) | 7b88d7ad, 3b0554e2, ef2c7677, e5ca0f0c, e7f671d6, 797f335a, 9f5289ae, 7fcdfb5c, b578810b, 10c8e5fc, dfea15bf, 86ecf008 | Either a test that excludes the mimic (AChR/MuSK/LRP4, RNS, ice pack, SFEMG, myositis panel, brain MRI, spine MRI, EEG, Lyme, AQP4/MOG, nodal antibodies, CSF cytology) as a new criterion with its own follow-up, or the likelihood lowered with the finding that excludes it. Acute-onset CIDP low with the 8-week reassessment in every case; CIP very_low with "no ICU course before onset". |
| C6 red herrings | Empty, dangling (non-existent MRI), or supporting findings mislabelled as distractors | b2c102d6, 8241358d, 682d7003, dfea15bf, e7f671d6 | Every red herring names a finding present in the case and how it resolves; non-existent ones deleted; P01 replaced with the ED stroke suspicion. |
| C7 timeline leaks and editorialising | Results of scored studies in the HPI/exam (CSF, MRI, AQP4, TSH, CK, antibodies), multiple time points in one exam, editorial sentences | d8e03a5d, 91de81af, 797f335a, 09291641, 72d65aba | Deleted; exams dated where a case spans days; prior studies kept only as dated history when not scored. |
| C8 treatment statements | Template steroid, IVIg-PE and IgA prohibitions; PE "contraindicated" unsourced; IVIg in grade 1 or MFS; breastfeeding claim; conditional immunotherapy | b71e3c4f, c7fc4320, 442f0e51, e62f0ba4, 8018be9e | Canonical prohibitions; IVIg or PE only with the indication, dose and timing; MFS-spectrum and grade 1-2 cases monitored with treatment on progression; RP11 ASCO/ESMO steroid must with doses; PE as relative caution with the reason; LactMed for IVIg in lactation. Succinylcholine prohibition added in 15 cases where intubation is possible. |
| C9 wrong-tool, placeholder, unsafe follow-ups | Brain MRI under advanced imaging, chest CT under CT, barium swallow as a lab, edrophonium, placeholder ECG/DDI/literature steps, unindicated head CT and EEG, CMV PCR unreachable | e5ca0f0c, 682b32b6, c0279d2a, 24f4abe2 | Moved to the right tool with a criterion, or deleted. Empty placeholders deleted in all cases. CSF CMV PCR BLOCKED (CENTRAL 4). |
| C10 lab and CSF template evidence | a1 expecting leukocytosis and trigger serology; a3 "cells <10"; HIV with the leaky clinical_significance in 29 cases; HIV non-reactive in an HIV-positive patient | ee1e4f06, 261fe3e8, bfc49d34, 4a3dc6d5 | Canonical a1/a3, case-specific where the data differ; leaky sentence deleted; HIV out of the required args; routine labs completed with liver tests, albumin, glucose and CK in every case. |
| C11 literature and certainty | Literature output echoing a5 (scoring-key leak) with a bare citation; Brighton levels quoted inconsistently | c0279d2a, 605dea03 | Population-keyed, sourced literature output; a5 optional and last; Brighton quoted once and consistent with the data. |
| C12 monitoring into the future | Telemetry over 48-240 h reporting atropine, labetalol, pacing, nitroprusside | (survey) | First 24 hours, findings only; canonical a8. Same class found and fixed in repeat NCS follow-ups at day 10-14 (M02, M03, S02, RS16; the index-order guard had failed), CSF "culture at 3 days / 48 h" (RS14 verifier; RM14, RS18 audit) and a day-12 NCS on a day-2 assessment (RS13). |
| C13 coagulation before LP | No platelet/INR gate; FFP and transfusion steps after the LP | b902ee1c | Hard labs-before-LP in RM13, RP16, RS16 (plus DDI-before-LP in RS16) with `coagulation` in a1; transfusion and FFP steps deleted. RP13 checked: no anticoagulant, no constraint needed. |
| Further classes found during the round | CSF:serum glucose ratios inconsistent with the serum glucose (M01, M02, M03, RS17, S04 and others); NCS reports titled NCS and EMG without needle EMG; "borderline QTc" at values that are normal for the sex; "sinus tachycardia" at rates below 100; a7 template evidence; "(agent not specified on this case's pathway)" in the DDI fallback; fallback CT/MRI/echo contradicting the case (RS13, RS16) | own findings | Fixed case by case; the a7 and DDI-fallback templates were finished by the audit (below). |

## Counts

- **Notes (68):** FIXED 64; FIXED with a BLOCKED part 4 (P01 ee1e4f06, P02 24f4abe2, RM12
  39b7526d, RM15 e89ffe81: the clinical fix is done, the scoring criterion waits for a vocabulary
  term); ALREADY-FIXED 0; DECLINED 0; BLOCKED as a whole 0. Where a note offered options the
  choice is logged (M01, M03, RM15, RP15, RS11, RS13, RS14, RS15, S03, S04 and others).
- **Own findings:** workers logged 459 FIXED findings (plus 3 tier decisions recorded without a
  change); verifiers found and fixed 32 more (in 21 cases); the audit fixed 29 items in 20 cases.
  Nothing was left FLAGGED as an error. Noted and deliberately left unchanged: P03 label
  "areflexia" with trace patellar and brachioradialis reflexes (label rule); RM13 absent sural
  SNAPs with intact sensation (subclinical diabetic neuropathy); S03 NCS without a needle EMG line
  (approved case, not needed by the criterion); RS18 HPI "lower facial weakness" against a
  cranial-nerve field with forehead involvement (approved case, original text); em dashes in
  `accepted[0]` of P02, RP11, RS18 (ruling 3); older em dashes in unchanged exam prose.
- **Cases changed:** 30 of 30.
- **Approved cases changed:** all 7 (RP16, RS12, S02, S03, S04 approved with notes; S01 and RS18
  counted as approved). Each change is a plan class error or a logged real error: spirometry
  leaks, antecedent serology, ganglioside panels, telemetry and NCS from the future, wrong flags,
  template criteria, missing ICU and intubation musts; RS12 also had a 12-hour nadir and RS18 had
  the spine MRI, brain MRI and AQP4 results in the HPI. All 7 need re-review.

## Audit fixes (logged in each case's "Condition audit" section)

- a7 expected_evidence was still the template "Sinus tachycardia or bradycardia; conduction or
  repolarisation abnormalities reflecting autonomic involvement" in M01, M02, M03, P02, RM11-RM16
  (the RP12 verifier had flagged it). Rewritten to what each ECG shows, with the rationale already
  used in RP12 and RP14-RP16.
- `fallback_tool_outputs.drug_interactions.general.proposed` "(agent not specified on this case's
  pathway)" in 15 cases (M01, M02, M03, P01, P02, P03, RM11, RM12, RM15, RP12, RP14, RS11, RS13,
  RS14, RS15): now "Medication list review", as the S01-S03 and RS18 workers had done.
- P02 ECG called QTc 452 ms in a woman "borderline": now normal (AHA/ACCF/HRS 2009; matches RM13
  and RP14).
- RM14 and RS18 CSF culture "no growth at 48 h" for an LP ordered at the assessment: now "no growth
  to date".
- RS16: the CSF was required before assessment while the verifier's must 3 makes the puncture
  conditional on an interval after apixaban (anti-Xa 112 ng/mL, on treatment) with dual antiplatelet
  therapy that cannot stop after the stent. a3 is now recommended and out of the stop rule; the hard
  labs-before-LP and DDI-before-LP constraints stay; KCE 1 states Brighton level 2 without the CSF,
  level 1 once obtained.

## DECLINED and BLOCKED notes

- DECLINED: none.
- BLOCKED parts (all on vocabulary; the clinical content is fixed):
  - P01 ee1e4f06 and RM15 e89ffe81: no `interpret_labs` term for anti-GQ1b IgG, so the anti-GQ1b
    order the musts describe cannot be scored. The follow-up is reachable when clinical_context
    names GQ1b or ganglioside (probed). CENTRAL 1.
  - RM12 39b7526d (and RS15 own finding): same for anti-GT1a IgG. CENTRAL 1.
  - P02 24f4abe2: CSF CMV PCR is not in the `analyze_csf` special tests; the must asks to send it
    and the differential lowers CMV on CD4, viral load and CSF pattern. CENTRAL 4.
  - Also unscored for the same reason (no note): RS11 and RS18 ganglioside follow-ups (negative).

## Departures from the plan (decided by workers or verifiers, reasons in the logs)

- M02, M03, S02: repeat NCS follow-ups deleted (future results that also answered the index order);
  M02 label drops "with secondary axonal injury".
- RS12, RS13, RS18: a9 contrast spine MRI raised from optional to recommended (red flags: pain and
  paralysis after spinal surgery; quadriparesis after a fall; sensory level with bladder
  dysfunction).
- RS13: respiratory function first in the order (desaturating bulbar patient).
- RS15: no ice pack test (no ptosis); SFEMG optional instead. RM12: brain MRI criterion added.
  RP12: brain MRI must deleted instead. RP11: brain MRI removed from waste without a criterion.
- a6 required beyond the plan's list in RS12 (lisinopril with albumin PE), RS13 (donepezil with
  succinylcholine, aspirin with haemorrhage) and S04 (metoprolol with autonomic bradycardia,
  metformin before IVIg, tamsulosin before PE); recommended in P02 and RM14; optional elsewhere
  with the reason logged.
- RS17: brain MRI required (encephalopathy with fever and neck stiffness), EEG recommended; the
  verifier replaced the worker's doxycycline must with QT monitoring (ATS/IDSA 2019 for severe CAP).
- RS16 (audit): CSF recommended, not required (see above).

## CENTRAL requests (consolidated)

1. Vocabulary: `anti_GQ1b_IgG` and `anti_GT1a_IgG` (or one `anti_ganglioside_panel`) in
   `interpret_labs`, with tokens that reach the trigger `request_anti_gq1b_gt1a_ganglioside_panel`
   (plan CENTRAL 1 and 11). Then add a recommended criterion in P01, RM12, RM15, RS15 and an
   optional one in RS11, RS18. Consider whether `anti-GM1 IgM` should stay in the vocabulary.
2. Vocabulary: CSF `CMV_PCR` in `analyze_csf` special tests (P02; RM16, RP15 and RS18 already carry
   a CMV PCR result in the stored CSF report that no order can request specifically).
3. Vocabulary: `botulinum_toxin_assay` (RM12, RS15 lowered botulism on clinical reasons). Decide on
   `stool_culture` and `Mycoplasma_serology` for other conditions (plan CENTRAL 2).
4. Schema: `weight_kg` and `height_cm` in demographics (weight is in `physical_exam.general` in all
   30).
5. Synonyms (`diagnosis_synonyms.yaml`): every GBS case accepts "AIDP", "AMAN", "acute motor axonal
   neuropathy" and "miller fisher syndrome" for G61.0, so MFS is accepted for AIDP, PCB (RM12,
   RS15) and bifacial (RS11) cases, and AIDP for the MFS case (P01). Decide per-case variant
   acceptance.
6. Labels changed under ruling 3 (16 cases; synonyms untouched; please re-run the expansion):
   M01, M02, RM11, RM12, RM13, RM14, RM15, RM16, RP12, RP16, RS11, RS12, RS13, RS15, RS16, RS17.
   Spelling is mixed ("Guillain-Barre" in M01, M02, RS17; "Guillain-Barré" elsewhere), and
   `accepted[0]` keeps an em dash in P02, RP11 and RS18; RP15 keeps a speculative "(likely immune
   dysregulation)". A central label pass could normalise these (suggested for RP11: "Guillain-Barré
   syndrome related to an immune checkpoint inhibitor (pembrolizumab)").
7. Citation registry: new keys `[LactMed]` (NIH Drugs and Lactation Database, immune globulin; RM14)
   and `[Walgaard_2010]` (EGRIS; RP16), plus the plan keys. The MIP/MEP lower limits follow Evans
   JA, Whitelaw WA, Respir Care 2009;54:1348-1359 (named in the logs, not cited in the cases). The
   succinylcholine prohibition (15 cases) carries no citation: add a source (for example product
   labelling for denervation hyperkalaemia) if one is wanted.
8. Criteria pack `dataset-generation/criteria_packs/GBS.md`: align with the plan (EAN/PNS 2023
   governing; 20/30/40 as FVC <20 mL/kg, MIP weaker than -30, MEP <40, not "VC <40%"; ganglioside
   testing only for MFS-spectrum and PCB; no antecedent serology or stool culture; literature
   optional, DDI conditional).
9. `conditions.yaml` guillain_barre common_followups: `request_respiratory_monitoring` belongs to
   `order_specialized_test`, `request_spine_mri_contrast` to `order_body_imaging`.
10. Fallback library: the `respiratory_function` normal report should carry FVC L, % predicted,
    mL/kg, MIP and MEP.
11. Tests/CI: a guard for respiratory outputs saying "within normal limits" with FVC below 80% or
    flagging low values "(H)"; a guard for the leaky clinical_significance sentence; a guard for
    "(agent not specified on this case's pathway)" in DDI fallbacks and for the a7 template text,
    both likely present in other conditions generated from the same template.
12. Review UI: show the weight line and the respiratory change sentence prominently; display
    follow-ups in criterion order.

## Open questions for Andrea

The plan's seven open questions were all decided in the cases under the 24 Oct rule; each is
listed so you can overrule it:

1. RM15 and RS15 stay G61.0 by the edit route (RM15 anti-GQ1b acute bilateral ptosis with
   areflexia; RS15 full PCB with arm involvement), not relabelled as MG or MND.
2. FVC <60% predicted is applied as an ICU-level monitoring trigger, not as an intubation
   criterion.
3. No IgA screening before IVIg; the prohibition is renal function only.
4. RP11 carries the ASCO 2021 methylprednisolone doses in the must.
5. LactMed is cited as `[LactMed]` in RM14 (no statement on plasma exchange and breastfeeding).
6. HIV is out of the required lab arguments in all 30 (P02 has its own HIV control criterion).
7. Subtype words stay in labels only where the NCS meets them.

What only you can settle:

- The seven reviewer-approved cases all changed. Confirm that they go back to Reviewer 2 for
  re-review (the logs list each change).
- CENTRAL 5 (variant synonyms) and CENTRAL 1 (ganglioside vocabulary) are design choices for the
  benchmark: until CENTRAL 1 lands, six cases contain an antibody step that no criterion scores.
