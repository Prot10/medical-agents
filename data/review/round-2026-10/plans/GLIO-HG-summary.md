# GLIO-HG: condition summary of the October 2026 review round

Condition auditor, 24 October 2026. Scope: the 30 cases GLIO-HG-M01..M05, P01..P05, RM01..RM04,
RP01..RP04, RS01..RS06, S01..S06. Checked against `ROUND_POLICY.md`, `PATTERNS.md`, the condition plan
`plans/GLIO-HG.md`, the notes file `notes/GLIO-HG.json` (72 Reviewer 2 notes; Reviewer 1 has none)
and the 30 case logs.

## Final state

- `perfect_agent.py` on all 30 ids: 30/30 pass.
- `case_io.py check` on all 30 ids: schema OK for all 30 and synonym guard OK. No test failure names
  a GLIO-HG case. The suite has 118 failures elsewhere, from other conditions mid-edit and from
  central claim tests.
- `test_case_guards.py -k GLIO-HG`: 60 passed.
- Each of the 72 note ids appears in exactly one case log, the log of its own case, with a ruling.
  No log cites another case's note id, and the notes file has no id without a log entry.
- Scripted checks over the 30 files, after the audit fixes:
  - **Literature:** no `search_medical_literature` criterion, output or fallback.
  - **Tissue:**
    - `initial_tool_outputs.tissue_diagnosis` is null everywhere.
    - Tissue is served only by `obtain_tissue_diagnosis` follow-ups, one per procedure in the
      criterion.
    - The integrated diagnosis and molecular findings are identical across procedures.
    - The procedure order matches the plan's groups A-D.
    - The assay lists match C4, and every required assay has a report row.
    - No IDH-wildtype case requires 1p/19q.
  - **Seizures:**
    - The seizure-class musts and prohibitions match C5.
    - An EEG criterion exists only in M01, RP02, RM04, RP04 and RS03.
    - No seizure-class case penalises the EEG as waste.
    - No fallback EEG is normal in a hemispheric mass with oedema.
  - **Performance status:** required in RM01, RP01, RP04, RS06, S04 and S06, and recommended in the
    others.
  - **Sequence and stopping:**
    - fMRI and DTI follow the plan, with soft constraints to tissue.
    - Hard MRI-to-tissue and labs-to-tissue constraints are in all 30.
    - The stop rule equals the required criteria in all 30, and `max_additional_actions` is 0.
  - **Drug check:**
    - It is optional and last: RS06 is recommended per the plan, and RM04 is recommended as a logged
      deviation.
    - No check proposes temozolomide before tissue.
    - Every allergy agrees with the drug check and the musts.
  - **Avoided actions:**
    - LP harm, with the canonical C17 rationale, is in every case except RP03 (CSF cytology is
      recommended there).
    - The cardiac waste rationale is canonical.
  - **Differential:** no differential entry is moderate or high after tissue.
  - **Labs and consistency:**
    - Lab flags, anion gaps and MCHC are in range.
    - Midline-shift laterality is consistent.
    - Every red-herring `field_path` is set.
    - Wherever papilloedema is documented, the CSF opening pressure is raised.
  - **Text:**
    - The string "(agent not specified on this case's pathway)" no longer appears in any GLIO-HG
      file.
    - No text field contains "this case", "the panel", "criterion" or "scored" engineering text.

## Error classes found in this condition and how each was fixed

The class codes are those of the plan (section 2). The August rewrite generated all 30 cases from one
template, so most cases shared most classes.

| class | what was wrong | how it was fixed (all 30 unless stated) |
| --- | --- | --- |
| C1 Literature as a clinical step | `search_medical_literature` was a required criterion in the stop rule, and its outputs had invented figures and echoed criteria. | Criteria and outputs deleted, along with fallback literature outputs (P02-P05 at audit). Discriminating content moved into the rationales of the perfusion and spectroscopy criteria. |
| C2 Tissue upfront | The integrated diagnosis was in `initial_tool_outputs.tissue_diagnosis`, with template meta-text. | Initial tissue set to null. Layered WHO CNS5 reports are served only as `obtain_tissue_diagnosis` follow-ups, one per procedure, with real sites and an extent-of-resection row. |
| C3 Resection versus biopsy | Biopsy only, or the two treated as interchangeable without a reason. | Group A (resectable: `resection`, then `stereotactic_biopsy`), B (deep or eloquent: biopsy first), C (multifocal: biopsy, then cytoreduction) or D (cord: open biopsy scored as resection). The surgery must matches the group. |
| C4 Assay lists | Lists could not produce the diagnosis: 1p/19q required in IDH-wildtype cases; no sequencing at 55 or under; no ATRX, CDKN2A/B, TERT, EGFR or +7/-10 where the grade depends on them; H3 K27 missing in midline cases. | Per-entity lists from the plan, each assay reported in its own row, S05's engineering molecular rows replaced. RP03 now has CDKN2A/B homozygous deletion (grade 4). P05 and RP04 have case-specific lists. |
| C5 Seizure prophylaxis versus treatment | Template levetiracetam "prophylaxis" musts, including in patients who had no seizure; normal EEGs; EEG penalised as waste. | Three classes. Treat: antiseizure must, enzyme inducers avoided. No seizure: a prohibition on prophylaxis [AIOM_brain]. Uncertain spell: EEG recommended, treatment only if the spell is epileptic. EEG waste entries removed where EEG is indicated. Fallback EEGs made abnormal (focal slowing): M04, RS05 and RS06 by their verifiers, M05, P04, P05, S05 and S06 at audit. |
| C6 fMRI and DTI | fMRI filed as `perfusion_MRI`, DTI only in impressions, unscored. | Retagged `functional_MRI` and `DTI_tractography` follow-ups with recommended criteria and soft constraints to tissue, only where eloquent cortex or tracts lie close to the lesion (plan list). RP03's misfiled fMRI deleted. |
| C7 Performance status | Absent, so the treatment must could not be read. | `action-performance-status` with a follow-up derived from the exam: required at 65 or over (RM01, RP01, RP04, RS06, S04, S06), recommended otherwise. Pre-illness KPS in social history labelled as such. Treatment musts read the current KPS. |
| C8 HPI leaks the MRI | HPIs said "MRI showed an enhancing lesion" or "imaging revealed an intracranial abnormality". | Outpatient imaging reduced to a non-contrast CT with mass and oedema, or to the referral reason. P02's "CT revealed an enhancing lesion" fixed at audit. |
| C9 Report content | Impressions with management advice, cross-modality text, "suggesting" clauses, MRS "normal <1.5", EEG clinical essays. | Numbered, imaging-only impressions. Values kept and interpretive clauses removed. ACNS-format EEG lists. At audit, the trailing "Tissue diagnosis recommended" sentence was removed from the M01-M05 MRI impressions, for uniformity with the other 25. |
| C10 Labs | Impossible or inconsistent values; interpretive summaries ("likely non-fasting"); no type and screen or beta-hCG where the criterion or patient needs one. | Values recomputed (anion gap, MCHC, PT/INR), flags corrected, plain summaries. Type and screen in the labs panel, beta-hCG in women of child-bearing age. |
| C11 Template Stupp and steroid musts | One Stupp must and one dexamethasone must for every patient, whatever the age, KPS, entity or current steroid. | Canonical dexamethasone must (only for symptomatic oedema, with a taper), or the RP03 prednisone text. Entity-specific treatment musts by age, KPS and MGMT status: Stupp; hypofractionated with temozolomide; supportive care at KPS 40; DMG; IDH-mutant grade 3; cord-tolerant dose in RM02. Contraception and sperm banking before temozolomide where relevant. |
| C12 Differential, red herrings, key evidence | Mimics at moderate or high after tissue; key features copied from other cases; red herrings empty or with empty paths. | Rewritten from each case's own findings with discriminators. No entry above low. Red herrings for each built-in mimic. Empty paths set at audit in P02, RP02, RS01, RS02, RS03 and RS04. |
| C13 Drug checks | Temozolomide, lomustine, bevacizumab or PCV checked before tissue; allergies conflated; generic alternatives. | Rewritten for the drugs the patient actually takes or starts now (dexamethasone, levetiracetam, the home medicines), with the documented allergies. Optional criterion last. At audit, the temozolomide-before-tissue proposals in RS02 and RS04 were rewritten, and the RS03 wording changed. |
| C14 Consults or treatments filed as tools | Metadata and criteria listed "neurosurgery consult" or "neuro-oncology consult" as tools. | Moved into musts (MDT, neuro-oncology referral after the integrated diagnosis); metadata rewritten. |
| C15 Vocabulary gaps | Markers that cannot be ordered (chromogranin, synaptophysin, PAX8, TTF-1, thyroglobulin, H3 G34, metanephrines). | Stated in musts and as findings rows, never in `molecular_assays`. RS01 gained `action-paraganglioma-genetics` (SDHD). Listed under CENTRAL. |
| C16 Engineering text | "as stated in this case's diagnosis", "This case does not record the value", "(agent not specified on this case's pathway)". | Rewritten in report voice. A grep at audit finds no engineering text. |
| C17 Lumbar puncture | A CSF result served in patients with mass effect; generic harm rationales; LP prohibited in RP03, where it is safe and indicated. | CSF follow-ups deleted and the harm rationale made canonical (shift, effacement, papilloedema or cord block). In RP03 the harm entry is replaced by recommended CSF cytology with a hard MRI-first constraint. At audit, fallback CSF opening pressure was raised where papilloedema is documented (RM03, RS02, RS03, RS04, as S02-S06 already had). |
| Exam laterality and language (survey) | Laterality flips (facial droop, quadrantanopia), and aphasic signs in right-hemisphere tumours with left-dominant language. | Fixed by the workers and verifiers (RP02, RP04, S01-S04). At audit: RS01, RS02 and RP02 have fluent language, and P03 has slowed responses with intact naming. RM04's anomia is kept, per the plan. |

## Audit findings fixed (stragglers)

All were saved through `case_io`, and each is appended to its case log under "Condition audit
(24 Oct 2026)".

- **M01-M05:** the trailing sentence recommending tissue was removed from the MRI impression (C9
  uniformity). The style guide allows the sentence, so this is a consistency choice, not an error fix.
- **M03:** `metadata.difficulty_description` no longer says that imaging confirms the high-grade
  etiology.
- **P02-P05:** the generic fallback `literature_search` was set to null, and removed from
  `metadata.fallback_tool_kinds` where it was listed (C1).
- **Empty red-herring paths now set** (C12): P02[1], RP02[0], RS01[0], RS01[1], RS02[0], RS03[0],
  RS04[0].
- **P02 HPI:** "CT head revealed an enhancing brain lesion" became "a right frontal mass with
  surrounding edema" (C8).
- **Fallback EEG:** in M05, P04, P05, S05 and S06, a normal study became focal polymorphic slowing
  over the lesion with no epileptiform discharges (C5 class). `fallback_tool_kinds` was updated in
  M05 and P04.
- **Fallback CSF opening pressure with papilloedema:** RM03 is now 28, RS02 24, RS03 25 and RS04
  24 cm H2O, with an interpretation that the pressure is elevated (C17 class).
- **RS02 and RS04:** the drug check proposed temozolomide before any tissue (C13). It now checks
  dexamethasone and levetiracetam with the home medicines. RS02's treatment must gains
  contraception during and after temozolomide.
- **RS03:** the drug-check contraindication no longer presupposes concomitant temozolomide.
- **Language in right-hemisphere tumours with left-dominant language:** RS01, RS02 and RP02 now
  have fluent language. P03 has slowed responses with intact naming, and its HPI, key evidence and
  performance-status output agree.
- **`metadata.condition_name`:**
  - M05: retired "anaplastic astrocytoma, WHO grade 3" became "astrocytoma, IDH-mutant, CNS WHO
    grade 3".
  - RP03: "astrocytoma with protoplasmic features" became "astrocytoma, IDH-mutant, CNS WHO grade 4,
    with leptomeningeal dissemination".

## Checked and left as is

- Em dashes that were already in patient prose and in fallback echo and Holter text: they are
  correct prose and were left alone to avoid churn. New text has none.
- `metadata.condition_name` uses mixed separators and is absent in 8 cases. It is display metadata
  and does not score.
- About 20 cases keep diagnostic musts of the form "Obtain MRI ... / Obtain pre-operative labs ...",
  and about 10 have had them removed. Both forms are correct, and the musts duplicate the required
  criteria (open question below).
- Templated but correct shared phrasing, such as the lymphoma and demyelination key features: each
  matches its own MRI.
- RP03's fallback CSF can never be served, because a CSF follow-up exists and the matcher serves it
  first.
- S01: the generic `order_specialized_test` fallback stays FLAGGED. It is a benchmark-wide fallback
  pattern.
- Prior MRIs mentioned in the HPIs of P03, P04, P05 and RM01: they predate the illness or are old,
  normal studies, not leaks.
- RS05 `metadata.real_seed_note`: provenance metadata.

## Counts

- **Reviewer notes:** 72 in total.
  - FIXED: 72. In 2 of them (M03 aed4aacd, RM03 1a5bdcb8) the empty-tool-field part was
    ALREADY-FIXED.
  - DECLINED: 0.
  - BLOCKED: 0.
- **Own findings in the case logs:** 551 FIXED and 1 FLAGGED (S01, generic specialized-test
  fallback).
- **Condition-audit findings:** 18 cases touched at audit. Distinct straggler fixes: 9 classes, about
  40 field edits, all fixed and none flagged.
- **Cases changed this round:** 30 of 30.
- **Approved cases changed:** 0. No GLIO-HG case was approved before this round.

## DECLINED and BLOCKED notes

None.

## CENTRAL requests (consolidated)

1. **Criteria-pack allow-list** (`criteria_packs/GLIO-HG.md`):
   - Add `[AIOM_brain]` (used in almost every case), `[vandenBent_2025]` (RS04), `[ACR_contrast]`
     (M03), `[EANO_PCNSL_2015]` (P02) and `[Wingerchuk_2015]` (RM02).
   - Add an ESCMID brain abscess key (Bodilsen J et al., Clin Microbiol Infect 2024;30:66-89) for
     the blood-culture and antibiotic-timing items in P01, P03 and P04.
   - Add a citation for the spinal-block LP harm in RM02 (`[Hasbun_2001]` concerns intracranial
     herniation).
   - Perry 2017 (cited in an RS06 must).
   - Supersede the pack's "literature required" position (ruling 5).
2. **Synonyms** (`diagnosis_synonyms.yaml`):
   - Remove "glioblastoma", "GBM", "glioma who grade 4", "grade 4 glioma" and "astrocytoma grade 4"
     from the IDH-mutant astrocytoma cases (M04, M05, RP03) and from the diffuse midline glioma
     (P05). Give each entity its own set, for example "astrocytoma IDH-mutant grade 3/4".
   - Remove "astrocytoma grade 4" from the IDH-wildtype glioblastoma set.
   - Add "gliosarcoma" for RM04.
   - "h3 k27m altered glioma" should become, or gain, "h3 k27 altered glioma" (P05).
   - Add the HIV-associated variants for P02: "AIDS-related primary CNS lymphoma", "HIV-associated
     CNS lymphoma", "EBV-positive diffuse large B-cell lymphoma of the CNS".
   - Re-expand the RP03 synonyms from its new label.
3. **Labels (ruling 3).** Applied: RS04, RP03, RM04 (gliosarcoma as histology only) and P05 ("Diffuse
   midline glioma, H3 K27-altered, CNS WHO grade 4 (thalamic)"). Still to do centrally:
   - M02: suffix "(high-grade glioma)" becomes "(left temporal lobe)".
   - M05: drop the "ATRX-loss" qualifier.
   - Normalise "WHO grade" to "CNS WHO grade" across accepted[0] if matching survives.
4. **Vocabulary:**
   - `open_biopsy` procedure (RM02).
   - Chromogranin A and synaptophysin IHC (RS01); PAX8, TTF-1 and thyroglobulin IHC (RP01).
   - H3 G34 status assay (RS01, RS03).
   - DNA methylation profiling (RM02, RM03).
   - Plasma free metanephrines panel for `interpret_labs` (RS01).
   - An `order_microbiology` specimen for a brain abscess aspirate (P04).
   - `flow_cytometry` exists only for `analyze_csf`, which is acceptable for P02.
5. **Generator-level fix:** the engineering string "(agent not specified on this case's pathway)" is
   in `fallback_tool_outputs.drug_interactions` of 120 case files in other conditions (none in
   GLIO-HG now).
6. **Fallback library:** check that the benchmark fallback for `search_medical_literature` returns no
   glioma-specific text that echoes a criterion. The case outputs are now gone.
7. **Review UI:** show the initial and follow-up outputs in criterion order, so reviewers see the
   tissue result under the tissue action.

## Open questions for Andrea (consolidated)

1. **AIOM edition** (plan question 1): which edition should `[AIOM_brain]` name, 2023 or 2026? The
   reviewer's Quesito 1 and 23 numbering needs re-verifying.
2. **`max_additional_actions`** (plan question 4): keep 0, or allow 1 as ISCH-STR did, now that each
   case has several recommended criteria?
3. **Performance status** (plan question 5): required only at 65 or over (applied), or required in
   all 30?
4. **Biopsy in group A** (plan question 7): stereotactic biopsy currently earns full credit as the
   second alternative for resectable lesions. Should it earn reduced credit, or be dropped?
5. **Confirm the plan's assumptions:**
   - RM04: glioblastoma label with gliosarcoma as the histology (plan question 2).
   - RP03: grade 4 through CDKN2A/B homozygous deletion (plan question 3).
   - P02: label kept, not renamed to the WHO-HAEM5 form (plan question 6).
6. **P04 blood cultures:** required in P04 (febrile, odontogenic source) but recommended in P01 and
   P03. Align them, or keep the difference?
7. **RM02:**
   - The H3 status (K27M not detected) is authored, not taken from the source report (PMC7642760).
     If the source tumour was H3-altered, the label would change.
   - The cord-tolerant dose and the optional spinal perfusion and MRS are in-round decisions.
8. **S05:** the ECG waste entry was removed, against the plan, because ESC 2022 recommends a
   pre-operative ECG when cardiovascular risk factors are present. Keep this?
9. **Diagnostic musts:** "Obtain MRI ... / Obtain pre-operative labs ..." stays in about 20 cases and
   was removed in about 10. Should they be removed everywhere (they duplicate criteria) or kept?
10. **Smaller in-round decisions to confirm:**
    - RM04: the drug check is recommended rather than optional.
    - RS05: the EEG has no criterion and is not penalised.
    - RP04 and P05: H3 K27 and MGMT are not required, respectively.
    - RS06: should awake mapping at 71 carry the RS05 feasibility qualifier?
    - P03: the ESCMID antibiotic-timing must sits outside the glioma guidelines.
