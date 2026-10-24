# GLIO-HG: decisions on the open questions (24 October 2026)

Andrea, 24 Oct 2026: resolve every open point "nel modo migliore per la qualità del dataset". Each
entry gives the question, the decision, the reason with its source, and what changed where. Sources
were checked on 24 Oct 2026; full references are in `dataset-generation/criteria_packs/GLIO-HG.md`
section 9.

Verified facts used below:
- AIOM, Linee guida Neoplasie cerebrali: SNLG (Istituto Superiore di Sanita) LG 266, first published
  22 July 2020, last updated 27 August 2026 (`LG_266_neoplasie_cerebrali_agg2026.pdf`; aiom.it lists it
  as the 2026 edition). The PDF itself could not be retrieved (ISS server refused the download, over
  10 MB for the fetcher), so the Quesito numbers of the 2026 update were not checked.
- Reward (`policy_reward.py` lines 122-129): recommended and optional criteria are credited and never
  count as additional actions; `max_additional_actions` only tolerates unlisted orders. An action
  criterion has no partial credit: an alternative either matches fully or not at all.
- RM02 source (PMC7642760; Radiol Case Rep 2020;16:72-77, case 1): 34-year-old woman with NF1,
  IDH-wildtype glioblastoma of the cervical cord to the lower medulla; "No IDH, BRAF nor H3 K27M
  mutations were found".
- ESCMID 2024 brain abscess guideline (Bodilsen J et al., Clin Microbiol Infect 2024;30:66-89):
  antimicrobials may be withheld until aspiration or excision in patients without severe disease if
  neurosurgery can be carried out within reasonable time, preferably within 24 hours (conditional,
  low); aspiration or excision as soon as possible (strong). No blood-culture recommendation was found
  in the guideline summaries consulted.
- RESBIOP (ENCRAM 2202, NCT06146725): no guideline or prospective study defines the optimal surgery
  (resection or biopsy) for glioblastoma at 70 or over, with KPS 70 or less, or in some locations.
- ICD-10-CM C83.390 (primary CNS lymphoma) is a valid code since FY2025, C83.39 its non-billable parent.

## Open questions in the summary

**Q1. AIOM edition.** Decision: `[AIOM_brain]` names the 2026 update (SNLG LG 266, 27 Aug 2026), the
edition current today. Because the 2026 question numbering could not be checked, case text cites AIOM
by topic: "AIOM Q1" and "AIOM Q23" became "AIOM" in 23 cases (the sentence around each citation already
says what it supports: surgery as extensive as safely possible; no antiseizure prophylaxis without
seizures). The pack records that Reviewer 2 cited Quesito 1 and Quesito 23. Changed: 23 case files,
pack section 9.

**Q2. `max_additional_actions`.** Decision: keep 0 in all 30. Reason: recommended and optional criteria
are credited and are never "additional" in the reward, so the premise of the question (several
recommended criteria) does not need an allowance; 480 of 600 cases use 0. No change.

**Q3. Performance status.** Decision: required in all 30 (was required only at 65 or over).
Reason: Reviewer 2 (RP04 0289beef) asked for a required current-KPS action, and a note is a class
(ruling 2); EANO 2021 stratifies every treatment branch by KPS (below 70 unfavourable) at any age,
and the KPS is also what decides cytoreduction and trial eligibility in the young (P05, RM02). Age 65
was an arbitrary proxy. Changed: 24 cases (`action-performance-status` recommended to required, added
to the stop rule before tissue); generator block (`clinical_assessment` required); pack.

**Q4. Biopsy in group A.** Decision: keep `stereotactic_biopsy` as a full-credit alternative of the
tissue criterion. Reason: criteria have no partial credit, so "reduced credit" is not expressible;
dropping biopsy would score an agent who obtained diagnostic tissue as missing a required act and zero
its stopping component. The diagnostic act is obtaining tissue; resection versus biopsy is a
management decision (ruling 4), carried by each case's surgery must, which already follows AIOM (first
option, as extensive as safely possible) and EANO 2021. RESBIOP documents genuine equipoise in older or
lower-KPS patients. No change.

**Q5. Plan assumptions.**
- RM04: confirmed. WHO CNS5 lists gliosarcoma as a histological subtype of glioblastoma, IDH-wildtype;
  label kept, synonym "gliosarcoma" added for RM04 only.
- RP03: confirmed. Homozygous CDKN2A/B deletion gives CNS WHO grade 4 to an IDH-mutant astrocytoma
  whatever the histology (WHO CNS5); the case data agree.
- P02: label kept ("Primary CNS lymphoma (EBV-associated DLBCL) in the setting of newly diagnosed
  HIV/AIDS"). It is the clinically standard name and the scored answer does not depend on the WHO-HAEM5
  wording, which the synonyms now cover ("hiv associated cns lymphoma", "aids related cns lymphoma",
  "ebv positive diffuse large b cell lymphoma cns", case-scoped).

**Q6. P04 blood cultures required, P01 and P03 recommended.** Decision: recommended in all three.
Reason: in all three the abscess is a differential of a glioblastoma; the decisive microbiology is
Gram stain and culture of the aspirate taken with the stereotactic procedure (ESCMID 2024: aspiration
as soon as possible), and the final diagnosis does not depend on blood cultures. P04's low-grade fever
(37.9) does not change what establishes the diagnosis. Changed: P04 `action-10-order-microbiology`
recommended and out of the stop rule.

**Q7. RM02.** H3 status: confirmed from the source (case 1 of PMC7642760: no H3 K27M mutation), so the
label is right; the report's retained H3K27me3 also excludes the EZHIP route to a diffuse midline
glioma. Cord-tolerant dose and optional spinal perfusion and MRS: confirmed (spinal perfusion and
spectroscopy have no validated grading role; optional is the honest tier). The spinal-block LP harm
now cites `[Hollis_1986]` (7 of 50 patients deteriorated after LP below a complete block). Changed:
RM02 avoided action citation; pack.

**Q8. S05 ECG waste removed.** Decision: keep removed. Reason: ESC 2022 non-cardiac surgery guideline
recommends a pre-operative 12-lead ECG in patients with cardiovascular risk factors before
intermediate- or high-risk surgery; S05 is 60 with risk factors before craniotomy. Checked the class:
only P05 (30, no risk factors) keeps ECG as waste; no other case penalises it. Pack section 3 states the
rule. No case change.

**Q9. Diagnostic musts.** Decision: remove the musts that only restate a required criterion ("Obtain
MRI ... before any invasive procedure", "Obtain pre-operative labs ...", RP04 staging CT, RM02 spine and
brain MRI), and keep the management half of mixed musts. Reason: musts are management (ruling 4), the
hard MRI-to-tissue and labs-to-tissue constraints already encode the order, and 12 cases had already
dropped them, so the condition was inconsistent. Changed: 31 musts removed in 18 cases (P02-P05,
RM01-RM04, RP01-RP04, RS01-RS06); rewritten to their management content in RM04 (repeat platelet count,
stop aspirin), RP01 (stop aspirin) and RS05 (stop aspirin 7 to 10 days before craniotomy). P02's HIV,
CD4, viral load and toxoplasma must is kept (it adds what no criterion orders).

**Q10. Smaller decisions.**
- RM04 drug check recommended: confirmed (ruling 6 allows it with a concrete interaction:
  dexamethasone with metformin and sitagliptin at HbA1c 8.1%, aspirin before craniotomy).
- RS05 EEG with no criterion and no penalty: confirmed. A focal aware seizure is documented, so the
  antiseizure must applies without an EEG; ordering one is reasonable and not waste.
- RP04 H3 K27 and P05 MGMT not required: confirmed. RP04 is hemispheric (EANO 2021 asks H3 K27 in
  midline gliomas); MGMT has no treatment role in diffuse midline glioma.
- RS06 awake mapping: already qualified ("only if her naming and comprehension allow the intraoperative
  tasks, otherwise asleep resection with subcortical monitoring"). No change.
- P03 (and P01, P04) antibiotic timing: kept, now with the ESCMID 2024 condition (neurosurgery within
  about 24 hours, no severe disease) in the text; key `[ESCMID_BA_2024]` in the pack. Changed: P01 and
  P03 musts, P04 prohibition.

## Auditor flags

**S01 generic specialized-test fallback (FLAGGED).** Decision: fixed as a class. A case fallback is
served for any order of its tool (`mock_server._match_fallback_output` ignores `test_type` and
`modality`), so a generic "Study within normal limits" report with an empty or neuropsychological test
type answered an EMG, a genetic panel or a neuropsychological battery alike, and contradicted the
exam where cognition is impaired. Set to null in 29 cases (all but S06, whose perimetry report is
case-specific), with `metadata.fallback_tool_kinds` updated; the benchmark library now answers by
`test_type`. Same class: P05's fallback `advanced_imaging` was a normal DaTscan served for any modality
(amino-acid PET included), now null.

## Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions brain_tumor_glioma`)

- `C71` (now `conditions: [brain_tumor_glioma]`) keeps only "high grade glioma" and "malignant glioma",
  true of every entity in the condition, and code C71.9.
- `C71+glioblastoma`: "glioblastoma", "GBM", "glioblastoma idh wildtype", except M04, M05, RP03 (IDH-mutant
  astrocytoma) and P05 (diffuse midline glioma).
- `C71+grade4`: "grade 4 glioma", "glioma who grade 4", except M05 (grade 3) and RM01, RM03 (H3-wildtype
  midline glioblastomas, where "diffuse midline glioma ... grade 4" is the wrong answer the generic
  label would accept).
- Case-scoped: "gliosarcoma" (RM04), "astrocytoma idh mutant grade 4" (M04, RP03), "astrocytoma idh
  mutant grade 3" (M05), "diffuse midline glioma", "h3 k27 altered glioma", "h3 k27m altered glioma" (P05,
  replacing the unscoped C71.0 entry).
- `C72.0` (RM02): "spinal cord glioma" and "intramedullary glioma" removed (they accept a diffuse midline
  glioma or a low-grade glioma of the cord); now spinal cord or intramedullary glioblastoma,
  glioblastoma, GBM and the two generic labels.
- `C83.390` (P02): "cns lymphoma" removed (it accepts secondary CNS lymphoma, a different disease);
  "primary cns diffuse large b cell lymphoma" added; HIV-associated labels case-scoped (`C83.390+hiv`).
- RETIRED: "astrocytoma grade 4", "spinal cord glioma", "intramedullary glioma", "cns lymphoma".
- `--check --conditions brain_tumor_glioma` clean.

## Labels and codes (ruling 3)

- accepted[0] in 25 cases: "WHO grade" became "CNS WHO grade" (WHO CNS5 nomenclature; P05, RM04, RP03
  and RS04 already had it, P02 is a lymphoma). M02: suffix "(high-grade glioma)" became "(left temporal lobe)". M05: "ATRX-loss" qualifier
  dropped. ICD codes unchanged.

## Generator (`conditions.yaml`, `brain_tumor_glioma` only)

- Follow-ups re-pointed to the tools that perform the study: perfusion, MRS, fMRI and (new) DTI under
  `order_advanced_imaging`; CT CAP under `order_body_imaging` (only when metastasis is live); tissue
  under `obtain_tissue_diagnosis` with the entity assay rule and the resection-first rule (it was
  `interpret_labs` with 1p/19q for all); performance status added.
- Moderate and puzzle presentations no longer contain the MRI result (C8 leak); they give an outpatient
  non-contrast CT with mass and oedema.
- EEG comment corrected (never required; recommended only for uncertain spells); `clinical_assessment`
  required; lymphoma differential no longer says "resolves with steroids" (hold steroids before biopsy).

## Guidance claims

`order_advanced_imaging` response said perfusion and MRS are recommended "in all 30 cases"; they are
recommended in 29 and optional in RM02. Response updated in `build_condition_tool_guidance.py`, YAML
regenerated, claim table updated (perfusion 29/1, MRS 29/1). All glioma claims pass. (Regenerating also
picked up the GBS agent's pending builder edits.)

## Cases changed

All 30 (labels and synonyms in every case; performance status in 24; musts in 18; fallbacks in 29; P04
cultures; RM02 citation). Every case log has a "## Close-out (24 Oct 2026)" section. Checks:
`perfect_agent.py` 30/30; `case_io.py check` schema OK and synonym guard OK for all 30 (no failure
names a GLIO-HG case; the suite needs `--ignore test_grpo_rollout.py` in this environment, where
`torch` is not installed); `test_case_guards.py -k GLIO-HG-` 60 passed; synonym `--check` clean.

## Still needing Andrea or the physicians

- Nothing needs information only Andrea has.
- For Reviewer 2 at re-review: the AIOM Quesito numbers are no longer in the case text (the 2026 update
  could not be checked); performance status is now required in all 30; diagnostic musts were removed.

## CENTRAL

1. **Scorer (code):** the diagnosis matches on the ICD code alone (`DiagnosisCriterion.matches`), and
   C71.x codes the site, not the entity. A "glioblastoma, C71.1" answer therefore scores as correct in
   M04 (IDH-mutant astrocytoma, C71.1), and a "diffuse midline glioma, C71.7" answer in RM01. The label
   scoping above only takes effect once a case can require a label match (for example a per-case
   `label_required` flag, or ICD-O-3 morphology codes: 9440/3 glioblastoma, 9445/3 astrocytoma IDH-mutant
   grade 4, 9401/3 grade 3, 9385/3 diffuse midline glioma, 9680/3 DLBCL). Relates to the existing
   CENTRAL_PENDING scorer item.
2. **Vocabulary** (unchanged from the summary, not made here):
   - `obtain_tissue_diagnosis` procedure `open_biopsy` (RM02 intramedullary; now scored as `resection`).
   - `obtain_tissue_diagnosis` molecular assays: chromogranin A and synaptophysin IHC (RS01); PAX8,
     TTF-1 and thyroglobulin IHC (RP01, metastasis exclusion); H3 G34 status (RS01, RS03); DNA
     methylation profiling (RM02, RM03).
   - `interpret_labs` panel: plasma free metanephrines (RS01, paraganglioma syndrome).
   - `order_microbiology` specimen: brain abscess aspirate (P01, P03, P04; the aspirate culture is now
     only in the tissue report and the musts).
   - `flow_cytometry` exists only for `analyze_csf`: acceptable for P02 (findings row only).
3. **Mock server (code):** `_match_fallback_output` returns one case fallback for any `test_type` or
   `modality`; benchmark-wide, other conditions carry the same generic "Study within normal limits"
   specialized-test fallback. Either match by parameter or strip generic fallbacks dataset-wide.
4. **Fallback library:** checked; no glioma-specific literature text (summary CENTRAL 6 closed).
5. **Test environment:** `test_grpo_rollout.py` fails to collect without `torch`, which makes
   `case_io.py check` report "1 error" and run no tests; run it with the training extra installed.
