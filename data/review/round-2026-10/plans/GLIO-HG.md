# GLIO-HG: condition plan for the October 2026 review round

Lead plan for the 30 GLIO-HG cases (M01..M05, P01..P05, RM01..RM04, RP01..RP04, RS01..RS06,
S01..S06). Read `ROUND_POLICY.md` and `PATTERNS.md` first; this plan does not repeat them.

All 72 notes are from Reviewer 2 and all are `needs_changes`. They cover 25 cases. S02, S03, S04,
S05 and S06 have no note, but the classes below apply to them in full: the August rewrite built
all 30 from the same text.

Baseline (24 October 2026, before any edit): `perfect_agent.py` passes 26 of 30. P01, P02, P03 and
S04 fail with `action-3-search-medical-literature (recommended) ... answered by the case
fallback_tool_outputs`. Class C1 removes the cause. No GLIO-HG case is modified in git.

How to use this plan:
1. Apply the classes in section 2 that name your case. Use the canonical text verbatim and fill
   the `<...>` slots.
2. Apply the decisions for your case in section 4.
3. Rebuild criteria, follow-ups, constraints and the stop rule per section 3.
4. Run `perfect_agent.py CASE -v`, `case_io.py check CASE` and
   `uv run pytest agent-platform/tests/test_case_guards.py -q -k CASE`.
5. Write `logs/{CASE_ID}.md`, citing every note id with its ruling.

Notes refer to fields by the numbering the reviewer saw:
- "Required action N" is criterion `action-N-*`; ids keep the v1 step numbers.
- "must N" is `required_recommendations[N-1]`.
- "Step N" is `followup_outputs[N-1]`; find it by content.
- "Required actions 4 and 5 have an empty tool field" (M03, RM01, RM03) refers to v1 null-tool
  consult steps that the v2 migration already removed. Log it ALREADY-FIXED, and check that the
  referral it stood for is a must.
- "Teaching pearls" are no longer in the case. Log a pearl-only clause ALREADY-FIXED. Apply the
  same correction to any field that still carries the claim, usually `key_clinical_evidence` or a
  red herring.

New text must be in English, keep each field's existing spelling and use no em or en dashes. New
values must be plausible for the patient's age, sex and medicines, and must differ from the shared
template values.

---

## 1. Governing guidelines and canonical facts

### 1.1 Which source governs what

| question | source | key |
| --- | --- | --- |
| Entity names, grading, integrated layered report | WHO CNS5: Louis DN, Perry A, Wesseling P, et al. Neuro Oncol 2021;23:1231-1251 | `[WHO_2021]` |
| Molecular testing, surgery, radiotherapy and chemotherapy by entity, KPS threshold | EANO 2021: Weller M, van den Bent M, Preusser M, et al. Nat Rev Clin Oncol 2021;18:170-186 | `[EANO_2021]` |
| BRAF V600E testing (RS04) | EANO update 1: van den Bent MJ, Franceschi E, Touat M, et al. Neuro Oncol 2025;27:331-337 | `[vandenBent_2025]` (CENTRAL: pack allow-list) |
| Surgery as first option; no antiseizure prophylaxis; antiseizure therapy after seizures | AIOM, Linee guida Neoplasie cerebrali (Quesito 1, Quesito 23, supportive-care text) | `[AIOM_brain]` (CENTRAL: pack allow-list; edition is an open question) |
| Temozolomide chemoradiation | Stupp R et al. N Engl J Med 2005;352:987-996 | `[Stupp_2005]` |
| Perfusion grading threshold rCBV 1.75 | Law M et al. AJNR 2003 | `[Law_2003]` (glioma grading only, never abscess perfusion) |
| MRS | Bulik M et al. 2013 | `[Bulik_2013]` |
| Imaging before LP | Hasbun R et al. NEJM 2001 | `[Hasbun_2001]` (LP safety only) |
| Contrast allergy premedication (M03) | ACR Manual on Contrast Media | `[ACR_contrast]` (CENTRAL) |
| PCNSL management (P02) | EANO PCNSL guideline: Hoang-Xuan K et al. Lancet Oncol 2015;16:e322-e332 | `[EANO_PCNSL_2015]` (CENTRAL) |

Rules:
- `WHO_CNS5` in a citation list becomes `[WHO_2021]`.
- Each list gets one bracketed key per source. The current lists carry both `"[X]"` and `"X"`;
  keep only `"[X]"`.
- Cite AIOM by question number only where the reviewer gave it (Q1, Q23). Cite the
  supportive-care text without a number.
- `[NCCN_CNS]` stays only on pre-operative laboratory and staging claims. Waste rationales cite
  `[EANO_2021]`.
- `[Stupp_2005]` on the MRI criterion is wrong; replace it with `[EANO_2021]`.

### 1.2 Canonical facts

Entities (WHO CNS5). Write "CNS WHO grade", with Arabic numerals.
- **Glioblastoma, IDH-wildtype, CNS WHO grade 4.** An adult diffuse astrocytic glioma, IDH-wildtype
  and H3-wildtype, with at least one of the following: microvascular proliferation, necrosis, TERT
  promoter mutation, EGFR amplification, or +7/-10.
  - The molecular criteria alone give grade 4 even without MVP or necrosis.
  - Giant cell glioblastoma and gliosarcoma are histological subtypes of this entity, not separate
    integrated diagnoses.
- **Astrocytoma, IDH-mutant, CNS WHO grade 2, 3 or 4.** Usually ATRX loss, and 1p/19q intact.
  - Homozygous CDKN2A/B deletion gives grade 4 whatever the histology.
  - Without the deletion, grade 4 needs MVP or necrosis.
  - "Glioblastoma, IDH-mutant", "anaplastic astrocytoma" and "diffuse astrocytoma" are retired
    terms. Never write them as current names. "Diffuse astrocytoma, IDH-mutant, grade 2" becomes
    "Astrocytoma, IDH-mutant, CNS WHO grade 2".
- **Diffuse midline glioma, H3 K27-altered, CNS WHO grade 4.** Thalamus, brainstem, spinal cord
  or other midline structures. H3 K27M mutation or loss of H3K27me3.
  - A midline tumour that is H3-wildtype and IDH-wildtype with GBM features is glioblastoma,
    IDH-wildtype. Its report must state that H3 K27 was tested and found wildtype.
- **Oligodendroglioma** needs IDH mutation plus 1p/19q codeletion. It is not this condition's
  answer.
- **Testing (EANO 2021)**:
  - IDH (IHC R132H, with sequencing when the IHC is negative and the patient is under 55) in every
    diffuse glioma.
  - ATRX in every diffuse glioma.
  - H3 K27 in every midline diffuse glioma.
  - CDKN2A/B in every IDH-mutant astrocytoma.
  - MGMT promoter methylation in every glioblastoma.
  - 1p/19q only where the tumour is IDH-mutant (oligodendroglioma versus astrocytoma).

Surgery (AIOM Q1; EANO 2021):
- Maximal safe resection is the first option whenever site and clinical condition allow.
- Stereotactic biopsy is for deep or midline lesions (thalamus, brainstem), multifocal disease,
  suspected lymphoma, or a patient unfit for craniotomy.
- In an eloquent lesion, functional MRI and DTI tractography plan the resection. Awake mapping
  needs a patient who can do the intraoperative language tasks.

Seizures:
- No seizure history: no prophylactic antiseizure medication (AIOM Q23, strong recommendation
  against).
- One or more seizures: antiseizure treatment, with levetiracetam preferred and enzyme inducers
  (phenytoin, carbamazepine, phenobarbital) avoided because they interact with dexamethasone and
  temozolomide (AIOM supportive care; EANO 2021). This is treatment. Never call it "prophylaxis".
- EEG has no role in tumour diagnosis. It is indicated only to characterise uncertain spells or
  altered consciousness.

Steroids:
- Dexamethasone for symptomatic vasogenic oedema, at the lowest effective dose, tapered after
  surgery.
- When primary CNS lymphoma is a live possibility, hold steroids until the biopsy unless
  herniation is impending (EANO PCNSL 2015).

Lumbar puncture:
- LP is harm when the MRI shows any of the following: midline shift, cistern or fourth-ventricle
  effacement, hydrocephalus, papilloedema, or a spinal block.
- Otherwise LP is waste, unless leptomeningeal or lymphomatous spread is in question and the MRI
  shows no herniation risk (RP03).

Treatment after the integrated diagnosis (musts only, never tools):
- **Glioblastoma, IDH-wildtype, age 70 or under, KPS 70 or more**: radiotherapy 60 Gy in 30
  fractions with concomitant and adjuvant temozolomide (Stupp 2005; EANO 2021).
- **Glioblastoma, over 70 or KPS under 70**: hypofractionated radiotherapy (40 Gy in 15 fractions),
  combined with temozolomide or as temozolomide alone when MGMT is methylated, or radiotherapy
  alone when MGMT is unmethylated (EANO 2021).
- **Astrocytoma, IDH-mutant, grade 3**: radiotherapy followed by adjuvant temozolomide (EANO
  2021).
- **Astrocytoma, IDH-mutant, grade 4**: managed like glioblastoma (EANO 2021).
- **Diffuse midline glioma, H3 K27-altered**: focal radiotherapy, and a clinical trial where one
  is available (EANO 2021).

Laboratory arithmetic (use it whenever you touch a panel):
- Anion gap = Na - (Cl + HCO3), within 8 to 16.
- MCHC is 32 to 36 g/dL (MCHC = Hb / Hct x 100), so Hct is about 3 x Hb.
- PT and INR must agree.
- Flag `is_abnormal` from the reference range.
- `clinical_significance` is `null` unless the value matters, and then it says how.

---

## 2. Error classes in this condition

Each class lists the cases it applies to. "All" means all 30. Note ids are 8-character prefixes;
section 4 lists them per case.

### C1. Literature search as a clinical step (ruling 5; all 30; covers P04 16cb2bae, the literature parts of M01 df9e2c08, RS04 a091c170, RM03 55929ced)

- Delete every `search_medical_literature` criterion (26 are required and 4 recommended).
- Remove those ids from `stop_rule.required_before_assessment` and from every sequence constraint.
- Delete every literature follow-up, and set `initial_tool_outputs.literature_search` and the
  fallback to `null`. Only P04 has an initial one.
- Where a literature output carried a clinical fact the case needs, move the fact into the
  rationale of the criterion it supports, with the correct key. Examples: "homozygous CDKN2A/B
  deletion confers grade 4" in M04, and "BRAF V600E discriminates PXA" in RS04.
- This removes the four baseline perfect-agent failures.

### C2. Tissue diagnosis served in the initial work-up (RP02 39e8c0d3 ruled as a class; all 30)

- Move `initial_tool_outputs.tissue_diagnosis` to a `followup_outputs` entry with
  `tool_name: obtain_tissue_diagnosis`, and set the initial field to `null`.
- Add one follow-up for each procedure the criterion accepts. Each follow-up's `procedure` field
  must equal that alternative's `procedure`.
  - The mock server matches tissue by `procedure`, so a `stereotactic_biopsy` output does not
    answer a `resection` order.
  - The resection output may give a larger specimen and an extent-of-resection line. The
    integrated diagnosis and the molecular results are identical.
- Delete the template meta-text from the tissue impression in every case: "The layered report is
  what the WHO CNS5 classification requires ... not merely the label." The impression becomes
  `Integrated diagnosis: <integrated_diagnosis>.` plus at most one sentence on MGMT status.
- `findings` and `molecular_findings` must not list "Microscopic description", "Original biopsy
  review" or cyst fluid as a molecular finding. Histology belongs in `histological_diagnosis` and
  in one `findings` row named `Histology`.

### C3. Procedure: resection versus biopsy (AIOM Q1; M04 457ccd8f, M05 615481ca, RM04 2cd403c7, RS02 7fdc5cfc, RS03 d061a446, M01 6ef98175, RS06 76ce5cab; all 30)

Today all 30 tissue criteria use `stereotactic_biopsy` alone, and the label says "Obtain tissue
(stereotactic biopsy)". Rebuild them by site.

| group | cases | alternatives, in order |
| --- | --- | --- |
| A: lobar supratentorial or cerebellar, resectable | M01, M02, M03, M04, M05, RM03, RM04, RP01, RP02, RS01, RS02, RS03, RS04, RS05, RS06, S01, S02, S03, S04, S05, S06 | `resection`, then `stereotactic_biopsy` |
| B: abscess against tumour | P01, P03, P04 | `stereotactic_biopsy` (aspiration and biopsy with frozen section, Gram stain and culture), then `resection` |
| C: deep, midline, multifocal or lymphoma | P05 (thalamus), RM01 (pons), P02 (suspected PCNSL), RP04 (multicentric, dominant lesion), RP03 (multifocal with leptomeningeal spread) | `stereotactic_biopsy`, then `resection` only in RP03 and RP04 (debulking of the dominant lesion); P05, RM01 and P02 accept biopsy alone |
| D: intramedullary | RM02 | `resection`, meaning open biopsy or debulking through laminectomy; CENTRAL asks for an `open_biopsy` term |

Canonical criterion label and rationale, group A (one sentence each, no dashes):
> Label: `Obtain tissue by maximal safe resection of the <site> lesion, or stereotactic biopsy if resection is not safely feasible, for an integrated histomolecular diagnosis`
> Rationale: `Surgery is the first option for a resectable glioma and should be as extensive as safely possible (AIOM Q1; EANO 2021). Only tissue establishes the integrated diagnosis and the molecular results that select treatment.`

For groups B, C and D, write the label with the procedure in the order given above. Give the
reason resection is not first: "deep thalamic location", "pontine location", "suspected lymphoma,
where resection brings no benefit", "multicentric disease", or "abscess remains possible and
aspiration is diagnostic and therapeutic".

Canonical surgery must:
- Group A:
  > `Refer urgently to neurosurgery for maximal safe resection of the <site> lesion<, with preoperative functional MRI and DTI tractography and intraoperative mapping | >, with stereotactic biopsy if resection is not safely feasible; send the specimen for an integrated histomolecular diagnosis (WHO CNS5).`
- Groups B, C and D: the same structure with the group's procedure.
- Remove every must that makes biopsy and resection interchangeable ("stereotactic biopsy or
  maximal safe resection").

Expected evidence for the tissue criterion: `Integrated diagnosis <label> with <the case's key
molecular results>`. Delete the template clause "with the molecular findings that determine the
protocol".

### C4. Molecular assay lists cannot produce the diagnosis (PATTERNS 1; M02 695c1dcf, M03 aed4aacd, RS01 32b30a51, RS02 c27c5e41, RS03 b0d00a8d, RS05 65ef42fb, S01 7d836e30, M04 af437c8f, M05 618200ca, RP03 4ebbab11, RM01 16e1c115, RM02 a02b3fb0, RM03 55929ced, P02 20ea01fe, RP04 0c2fc022, RS04 a091c170; all 30)

`required_arguments.molecular_assays` is a minimum subset: an agent that orders more still
matches. Set it per entity and put the same list in every alternative.

| entity in the case | minimum list |
| --- | --- |
| GBM IDH-wildtype, non-midline, MVP or necrosis on histology, age 55 or over | `IDH1_IHC`, `ATRX_IHC`, `MGMT_methylation` |
| same, under 55 | add `IDH1_IDH2_sequencing` |
| GBM IDH-wildtype without MVP or necrosis (a molecular GBM) | add `TERT_promoter`, `EGFR_amplification`, `chr7_gain_chr10_loss` |
| any midline case (P05, RM01, RM02, RM03 when the vermis is involved) | add `H3K27_status` and `IDH1_IDH2_sequencing` |
| Astrocytoma, IDH-mutant (M04, M05, RP03) | `IDH1_IHC`, `IDH1_IDH2_sequencing`, `ATRX_IHC`, `1p_19q_codeletion`, `CDKN2A_B_deletion`, `MGMT_methylation` |
| PCNSL (P02) | `CD20_IHC`, `EBER_ISH` |
| melanoma exclusion (RP04) | the GBM list plus `SOX10_IHC`, `Melan_A_HMB45_IHC` |
| PXA in the differential (RS04) | the GBM list plus `BRAF_V600` |

Rules:
- Remove `1p_19q_codeletion` from the required list in IDH-wildtype cases. The report may still
  contain it.
- The tissue report must have one `findings` row and one `molecular_findings` entry for **every**
  assay in the list. Use the same assay names as the vocabulary, written readably ("IDH1 R132H
  IHC", "IDH1/IDH2 sequencing", "ATRX IHC", "CDKN2A/B", "H3 K27M / H3K27me3", "BRAF V600E").
- Results must be consistent with the entity. An IDH-wildtype GBM is ATRX retained. A midline
  IDH-wildtype GBM reads "H3 K27M not detected; H3K27me3 retained".
- Specific results:
  - M04: CDKN2A/B "no homozygous deletion"; grade 4 rests on the MVP and necrosis already in its
    histology.
  - M05: CDKN2A/B "no homozygous deletion", so grade 3 stands.
  - RP03: CDKN2A/B "homozygous deletion detected", so grade 4; see section 4.
- The criterion's label lists the assays it requires in words. Delete the template sentence
  "Imaging establishes a suspicion; only tissue establishes the diagnosis, and the molecular
  result selects the treatment" from label and rationale.

### C5. Antiseizure prophylaxis versus treatment (AIOM Q23 and supportive care; M01 67871b5a, M03 f535a55b, M05 0c310d30, P04 ab9b72cb, P05 9046c896, RM01 61968ced, RM03 1a5bdcb8, RS06 39805cb7, RS05 79fc1c6f, RM04 16ac8653, RP01 7dc06c7a, RP04 eb3f1800; all 30)

Classify each case from its own history. These are the decisions:

| class | cases |
| --- | --- |
| documented seizure: treat | M02 (focal right-hand clonic seizure), M04, P01, P03, RP01, RP03 (on levetiracetam: continue), RP04 (speech arrest with staring), RS01 (check the HPI; treat if a seizure is recorded, otherwise use the no-seizure class), RS02, RS03, RS04 (on levetiracetam: continue), RS05, S01, S02, S03, S04 |
| probable seizures: characterise and treat | RM04 (three stereotyped staring spells with lip-smacking) |
| uncertain spells: characterise, do not prophylax | M01 (brief staring), RP02 (10-second staring spell with amnesia) |
| no seizure: prohibit prophylaxis | M03, M05, P02, P04, P05, RM01, RM02, RM03, RS06, S05, S06 |

Canonical texts:
- **Treat** (must):
  > `Start antiseizure treatment with levetiracetam for the documented <seizure description>; this is treatment of tumour-related epilepsy, not prophylaxis. Avoid enzyme-inducing antiseizure drugs (phenytoin, carbamazepine, phenobarbital), which lower dexamethasone and chemotherapy exposure.`
  - For a patient already on levetiracetam, use `Continue levetiracetam ...` and add the dose
    review.
- **Probable** (must):
  > `Treat the stereotyped <description> spells as probable focal impaired-awareness seizures: obtain an EEG to characterise them and start levetiracetam; avoid enzyme-inducing antiseizure drugs.`
- **Uncertain** (must):
  > `Characterise the <description> spells with an EEG; start levetiracetam only if they are judged to be seizures, not as prophylaxis.`
- **No seizure** (prohibition):
  > `Do not start prophylactic antiseizure medication: the patient has had no seizure, and AIOM recommends against prophylaxis in brain tumour patients without a seizure history.`
  - Also remove levetiracetam from the `proposed` field of the drug-interaction output and from
    every expected evidence that mentions it.
  - In P05, remove it from the action-8 expected evidence.
- The existing prohibition on enzyme-inducing AEDs stays only in the treat, probable and
  uncertain classes. In the no-seizure class it is covered by the prophylaxis prohibition; delete
  it there.

EEG tier:
- `analyze_eeg` becomes a **recommended** criterion (`action-eeg-characterise-spells`) in M01,
  RP02, RM04 and RP04. It stays optional or absent elsewhere.
- In RS03 the EEG becomes a recommended criterion because of the LPDs; see C9.
- Remove `analyze_eeg` from `avoided_actions` in M04, RM04, RP04 and RS05, where seizures are
  present.
- Where no seizure and no spell exists, the EEG waste entry may stay. Its rationale: `EEG has no
  role in the diagnosis of a brain tumour without seizures or altered consciousness (EANO 2021)`.

### C6. Functional MRI and DTI tractography: mislabelled, missing or unscored (M01 6ef98175, RM04 b8bef5c9, RS02 6e655625, RS03 d061a446, RS05 666dbf49, RS06 76ce5cab, M05 615481ca)

The 13 follow-ups tagged `perfusion_MRI` that return BOLD or DTI content need fixing: M01, M02,
M03, P01, P03, RM01, RM03, RP01, RP02, RP03, RS01, RS02, RS03 (the second advanced-imaging
follow-up). So do the follow-ups tagged `fMRI_BOLD`, which is out of vocabulary: RS04, S01, S02,
S03, S04.

**Decision rule.** Add functional imaging when both conditions hold:
- the resection is planned (group A); and
- the MRI reports involvement of, or proximity (within about 1 cm or "abutting") to, any of:
  - primary motor cortex or the corticospinal tract;
  - dominant-hemisphere language cortex (Broca, Wernicke, the arcuate fasciculus);
  - the optic radiation.

When it applies:
- Retag the language or motor mapping output as `modality: functional_MRI`.
- Move tract content into a separate `modality: DTI_tractography` follow-up.
- Each gets a **recommended** criterion: `action-fmri-functional-mapping` with
  `{"modality": "functional_MRI"}`, and `action-dti-tractography` with
  `{"modality": "DTI_tractography"}`.
- Only fMRI for cortex-only proximity, only DTI for tract-only involvement (for example the S06
  optic radiation), both when both apply.
- Add soft constraints from fMRI to tissue and from DTI to tissue.
- The impression reports distances and laterality index only. Never write a surgical
  recommendation.

When it does not apply (groups B, C, D, or no eloquent structure), delete the mislabelled
follow-up.

Per-case results (workers confirm from the MRI and log it):
- Both: M01, M02, M03, M04 (motor), M05, RS02, RS03, RS05, RS06, S01, S02, S03, S04, RP02, RS04.
- DTI only (optic radiation): S06.
- Apply the rule from the MRI: RP01, RS01, S05.
- RM04: see section 4.
- Delete: P01, P03, RM01, RM03, RP03.

Must wording: name fMRI and DTI in the surgery must (C3) only when the criteria exist.

### C7. Performance status absent (RP04 0289beef as a class; all 30)

- Add `perform_clinical_assessment` with `{"assessment_type": "performance_status"}` as criterion
  `action-performance-status`:
  - **required** in RP04 (the ruling) and in patients aged 65 or over (RM01, RP01, RS06, S04,
    S06; open question 5);
  - **recommended** in all the others.
- Required means it joins the stop rule.
- Author a `followup_outputs` entry for it. Give the KPS and ECOG at this visit, derived from the
  recorded examination and function, with a one-line basis such as "requires occasional
  assistance, cares for most needs: KPS 60, ECOG 2". No treatment recommendation.
- A KPS line in the social history is pre-illness history; label it so.
- Treatment musts (C11) read their KPS threshold from this value.

### C8. HPI leaks the MRI the agent must order (leakage policy; all cases with an outpatient MRI)

Outpatient or "initial" MRI results appear in the HPI of M01, M02, M03, M04, M05, RM04, RS05 (also
"Repeat MRI on admission confirms ...") and S06, and RP02 has "initial imaging revealed".
- Replace each with an outside **non-contrast CT** that shows a mass or hypodensity with oedema,
  plus the case's real midline shift. Do not mention enhancement, necrosis, diffusion or tumour
  type.
- P01 and P04 already have a non-contrast CT called "ring-enhancing" (P01 e25c4336). Rewrite it as
  "a hypodense lesion with surrounding oedema".
- The prior studies in RS01, RS04, RP03, P05 and RP01 are history before the encounter and stay.
  Check that none states the current MRI result.
- RS05 HPI says "was started on dexamethasone". Keep it, and turn the dexamethasone must into
  "continue at the lowest effective dose".

### C9. Report content: impressions, cross-modality text, templates (TOOL_REPORT_STYLE_GUIDE; RS03 f4b30a6a, M02 152c009f, RP01 6538e4db, RP02 41984330, RM02 7dbf817c)

- **EEG**: the impression lists every abnormality in the findings, in ACNS terms, with no
  clinical correlation essay.
  - RS03: the impression must state "lateralized periodic discharges (LPDs) at 1 to 1.5 Hz over
    the right frontocentral region (F4, C4)", and `analyze_eeg` becomes a recommended criterion
    (`action-eeg-characterise-spells` id reused).
  - S01: the sharp waves must be in the impression.
  - S04: delete "correlate with seizure".
  - RS01 and S03: write the impression from their own findings, not the template sentence.
  - RP02: the equivocal sharp transients must sit over the lesion side (right frontocentral), or
    the report must say they are contralateral.
- **MRI**: impressions report imaging only. Delete "consistent with the clinical ...", dental
  speculation (P01), management advice, and "Tissue diagnosis recommended".
  - RS05: the optic radiation runs in the sagittal stratum, not the posterior limb of the
    internal capsule.
  - S01: the midline shift must agree between CT (7 mm) and MRI (8 mm); use the MRI value in
    both.
- **Action-1 expected evidence (template in 20 cases)**: write it from this case's own MRI, using
  the real enhancement pattern, necrosis or its absence, diffusion pattern and shift. M02, RP01
  and RP02 currently expect necrosis or rim restriction their MRI denies.
- **Labs expected evidence**: the template "identify any coagulopathy, electrolyte derangement"
  becomes the case's actual result, for example "Sodium 129 mmol/L requires work-up before
  dexamethasone and surgery" or "No contraindication to surgery".
- **`type_and_screen` `clinical_significance`** (template in about 20 cases): set it to `null`.

### C10. Laboratory values impossible or inconsistent (M03 881deadb, P01 83979d94, P03 dde4d001, S01 73339f93; survey)

| case | defect | fix |
| --- | --- | --- |
| M01 | anion gap -3 | Cl to about 101, so the gap is about 12 |
| M03 | Na 129, Cl 109, HCO3 27, gap -7 | keep Na 129 (flag it); Cl about 95, HCO3 about 24; `clinical_significance` "hyponatraemia, assess volume status, serum and urine osmolality and urine sodium before dexamethasone and surgery"; add a hyponatraemia work-up must |
| P01 | Na 147, gap 30; MCHC 31.4 | normal Na about 140 and Cl about 103; MCHC into range |
| P03 | Na 148 with significance "none" | normalise to about 141 |
| S01 | Na 152; Hct 38.5 with Hb 14.7; PT 13.6 high with normal INR | Na normal; Hct about 44; PT within range |
| S02 | Na 130 unexplained; MCHC 38.6 | normalise Na unless the case uses it; Hct to bring MCHC into range |
| S04 | gap 17; MCHC 39 | fix Cl or HCO3; Hct |
| RS01, RS03, S01 | `chr7_gain_chr10_loss` row under "Exclusion studies" in labs | delete the row (RS01 e649546c, RS03 92ef1523) |
| P02, RP03 | no coagulation panel although surgery is planned | add PT, INR, aPTT within range |

After every change, recompute the `abnormal_values_summary` and the `interpretation`.

### C11. Template "Stupp" and steroid musts (all 30)

- Replace the shared must ("Plan multimodal treatment ... Stupp protocol ...") with the
  entity-specific line from section 1.2, conditional on the integrated diagnosis and the KPS from
  C7:
  > `After the integrated diagnosis, refer to the neuro-oncology multidisciplinary team; <entity-specific standard from 1.2>.`
- In M04, M05, RP03 (IDH-mutant), P05 and RM01/RM02 (if H3-altered) and P02 (lymphoma), the Stupp
  wording is wrong and must go.
- Dexamethasone must:
  > `Start dexamethasone for symptomatic vasogenic oedema (for example 4 mg every 6 to 8 hours after a loading dose when mass effect is marked) at the lowest effective dose, with glucose monitoring and gastric protection, and taper after surgery.`
  - P02 and RP03 use their own text (section 4).

### C12. Differential, red herrings and key evidence (ruling 7; P01 d3ff3f30, P03 1163206c and 76e5c5d3, P04 16cb2bae and 33019b2d, P05 bc69f5ec and e8cfa028, RP01 786de7f4, RP02 2b8748f1, RP03 928080d2, RS04 d02be965 and a091c170)

- **Generic appended entries**:
  - Merge duplicate entities (P03 has abscess and demyelination twice each).
  - Delete the ground truth from its own differential (RS04 "Conventional glioblastoma", RM04
    "Glioblastoma classic variant").
  - Set every likelihood at the assessment-time view.
- **Retired names** in differentials: "anaplastic astrocytoma" and "diffuse astrocytoma" become
  "Astrocytoma, IDH-mutant, CNS WHO grade 3" and "... grade 2".
- **Imaging does not grade or exclude**:
  - Delete "rCBV excludes abscess", "decisively", and "confirm high-grade features".
  - Perfusion and MRS "support" a high-grade neoplasm and "target the biopsy". Tissue decides.
- **Red herrings**: rewrite each `correct_interpretation` from the findings the case prints:
  - P01: thin smooth ring, central restricted diffusion, WBC 11.2.
  - P03: equivocal diffusion, shaggy ring.
  - P04: delete the "steroid-mediated cytokine release" clause, since no steroid has been given.
  - P05: perfusion as biopsy targeting.
  - RP01: thyroglobulin.
  - RS01: skull-base lesion.

### C13. Drug-interaction outputs disagree with the patient (ruling 6; M01 df9e2c08, M02 152c009f, M03 0bcfaf79; survey RP01, RP02, RM04 and others)

- `check_drug_interactions` stays **optional** in all cases, except **recommended** in RS06
  (hydroxychloroquine and QT). It goes last in the pathway.
- The output must match `patient.clinical_history.allergies` and `medications`:
  - Delete every "penicillin allergy, verify sulfonamide" sentence unless the patient has a
    penicillin allergy.
  - M01: the allergy is tetracycline.
  - M02: NKDA, a 47-year-old man, so delete the pregnancy line.
  - M03: a contrast reaction, not penicillin.
- `proposed` contains dexamethasone, plus levetiracetam only in the treat, probable or uncertain
  class (C5), plus the patient's relevant medicines.
- No sentence repeats any criterion's expected evidence (PATTERNS 5 guard).

### C14. Consults and treatments filed as tools (ruling 4; survey)

Convert or delete:
- P01 `interpret_labs` follow-ups: the blood cultures become an `order_microbiology`
  `blood_culture` follow-up. The infectious-disease consult and dental evaluation become musts.
- P03 `interpret_labs`: blood cultures go to microbiology as above. The "demyelination work-up"
  is deleted, or becomes a must if the case needs it.
- P02: the `interpret_labs` PET-CT is deleted.
- RP01: the `interpret_labs` thyroid ultrasound becomes a must, or `order_body_imaging` if the
  vocabulary has the study.
- RS01: the `interpret_labs` catecholamine work-up becomes the C15 genetics criterion and a
  must (plasma free metanephrines as a must).

In P01, P03 and P04, blood cultures are a **recommended** criterion `action-blood-cultures`
(`order_microbiology`, `{"specimen": "blood_culture"}`). P04 keeps its required microbiology
criterion as it is; check it is the culture of the aspirate and that its label says so.

### C15. Case-specific vocabulary gaps

- RS01: add `order_specialized_test` `{"test_type": "genetic_panel:hereditary_paraganglioma"}`,
  recommended, as `action-paraganglioma-genetics`.
- Chromogranin and synaptophysin IHC (RS01), and PAX8, TTF-1 and thyroglobulin IHC (RP01), are
  not orderable. State the need in a must and in the log, and list it under CENTRAL. Do not put
  them in `molecular_assays`.

### C16. Engineering leakage

- S05 `molecular_findings` contains "as stated in this case's diagnosis" and "This case does not
  record the value". Replace these with real results per C4.
- Grep every text field for "this case", "the panel", "criterion", "scored" and "metadata", and
  rewrite any hit in report voice.

---

## 3. Target pathway and tiers

### 3.1 `action_criteria` order and tiers (keep existing ids; new ids as given)

| # | criterion | tier | notes |
| --- | --- | --- | --- |
| 1 | `action-1-analyze-brain-mri` (`contrast: true, protocol: tumor`) | required | RM02: spine MRI first, then brain MRI (see 4) |
| 2 | `action-6` perfusion_MRI | recommended | not in P05 waste list conflict: see 4 |
| 3 | `action-7` MR_spectroscopy | recommended | |
| 4 | `action-eeg-characterise-spells` | recommended | only M01, RP02, RM04, RP04, RS03 |
| 5 | CT chest abdomen pelvis (`action-8-order-body-imaging` or existing id) | optional | required in RP04, recommended in RP01 and RS01; delete in P05 |
| 6 | `action-blood-cultures` | recommended | only P01, P03, P04 |
| 7 | `action-2-interpret-labs` (`CBC, BMP, coagulation, type_and_screen`) | required | |
| 8 | `action-performance-status` | recommended, or required per C7 | |
| 9 | `action-fmri-functional-mapping`, `action-dti-tractography` | recommended | per C6 |
| 10 | case-specific: `action-csf-cytology` (RP03), `action-paraganglioma-genetics` (RS01), P04 microbiology | as given in section 4 | |
| 11 | tissue criterion | required | per C3, C4 |
| 12 | `check_drug_interactions` | optional (RS06 recommended) | last |

### 3.2 Follow-ups and initial outputs

- `initial_tool_outputs` keep MRI, labs, ECG if present, and EEG if present. In the RM04 and RP04
  cases, where the EEG becomes recommended, author a fresh EEG output consistent with the spells:
  focal slowing over the lesion, and sharp waves if they fit. Tissue and literature are `null`.
- `followup_outputs`, in order: perfusion, MRS, CT CAP, blood cultures, performance status, fMRI,
  DTI, case-specific (CSF in RP03, genetics in RS01), tissue (one per procedure), drug check last.
- Delete these follow-ups:
  - literature;
  - mislabelled imaging under C6;
  - consult and treatment follow-ups under C14;
  - the CSF follow-ups in P02 and RM02 (C17);
  - the duplicate perfusion in P02;
  - the duplicate non-contrast spine MRI in RM02.
- Each `trigger_action` is a short snake-case description of the order.

### 3.3 Sequence constraints (replace the single template soft constraint)

| before | after | severity |
| --- | --- | --- |
| `action-1-analyze-brain-mri` | tissue | **hard** (`Biopsy or resection without contrast MRI cannot target the enhancing tumour or plan the approach (EANO 2021)`) |
| `action-2-interpret-labs` | tissue | **hard** (`Coagulation, platelets and type and screen must be known before a neurosurgical procedure`) |
| fMRI or DTI (where present) | tissue | soft |
| RM02 spine MRI | tissue | hard |
| `action-1-analyze-brain-mri` | `action-csf-cytology` (RP03) | hard (`Imaging excludes herniation risk before lumbar puncture [Hasbun_2001]`) |

### 3.4 Stop rule, avoided actions

- `required_before_assessment` lists `action-1`, `action-2` and the tissue criterion, plus
  required case-specific criteria: RP04 CT CAP and performance status, the required performance
  status cases of C7, P04 microbiology, and the RM02 spine MRI. Literature is never in it.
- `max_additional_actions`: keep 0 (as ALS, BACT-MEN and HEP-ENC did); open question 4.
- `avoided_actions`:
  - echo and Holter stay waste, with rationale `No cardiac question in this presentation`.
  - `analyze_csf`: harm with the C17 rationale, except RP03.
  - EEG: per C5.
  - P05 keeps its advanced-imaging waste entries only if they do not penalise the recommended
    perfusion and MRS. If they do, delete them; workers check the `required_arguments`.

### C17. Lumbar puncture (P02 5481518a, RM02 fea3f998, RP03 753d78af; all 30)

- Harm rationale, canonical:
  > `Lumbar puncture is contraindicated with <the case's finding: N mm midline shift / fourth-ventricle effacement / papilloedema>: the pressure gradient risks herniation [Hasbun_2001].`
- Where the MRI shows none of the harm findings, the entry becomes `waste`: `CSF is low-yield in a
  parenchymal tumour`. Decide this per case from the MRI.
- P02: delete the CSF follow-up, because 6 mm shift and papilloedema make it harm. The diagnosis
  comes from the biopsy.
- RM02: delete the CSF follow-up. Rewrite the harm rationale and the prohibition for a spinal
  block: `Lumbar puncture below an expanded cord with near-complete effacement of the
  subarachnoid space risks neurological deterioration (spinal coning)`.
- RP02: the MRI has 3 mm shift and mild effacement of the frontal horn. Keep harm, citing the
  mass effect, and delete the CSF follow-up, since the case does not need CSF.
- RP03: see section 4.

---

## 4. Per-case index

Each case lists note ids (ruling in brackets), then survey findings. Apply classes C1, C2, C3,
C4, C5, C7, C9 (action-1 and labs templates, type and screen), C11, C12 (generic entries), C13
and C16 to every case. Section 4 lists only what is case-specific.

### GLIO-HG-M01 (woman, 52, left temporal GBM IDH-wildtype, uncertain staring spells)
- 67871b5a (APPLY): uncertain class. Remove the treat must and add the uncertain must and the
  recommended EEG criterion; the initial EEG shows left temporal delta and no epileptiform
  discharges.
- 6ef98175 (APPLY): retag the mislabelled step as functional_MRI; split the arcuate DTI into
  DTI_tractography, with its findings in the findings field. Group A resection.
- df9e2c08 (APPLY): the allergy is tetracycline. The literature part is covered by C1.
- Survey: anion gap -3 (C10); HPI outpatient MRI (C8); occupation consistent with M02? check
  that the "English teacher" detail is hers.

### GLIO-HG-M02 (man, 47, left temporal GBM, focal right-hand clonic seizure)
- 695c1dcf (APPLY): C4 list, adding IDH1_IDH2_sequencing (under 55).
- 152c009f (APPLY): NKDA; delete the penicillin and pregnancy lines. Action-1 expected evidence
  without necrosis.
- Survey:
  - Seizure documented, no treat must: add it (C5).
  - accepted[0] suffix "(high-grade glioma)" is not a site. CENTRAL asks for "(left temporal
    lobe)".
  - HPI MRI leak (C8).

### GLIO-HG-M03 (woman, 54, left temporal GBM, contrast allergy, hyponatraemia)
- 6defe1f8 (APPLY):
  - Specify the allergy as "iodinated contrast (urticaria)" if the history allows, otherwise ask
    in the log.
  - Add a must: `Before gadolinium MRI and contrast CT, review the prior contrast reaction: a prior reaction to iodinated contrast is not a contraindication to gadolinium; for contrast CT give corticosteroid and antihistamine premedication or use an alternative study [ACR_contrast].`
  - The drug check must mention the allergy.
- 881deadb (APPLY): C10 values and hyponatraemia must.
- f535a55b (APPLY): no-seizure class.
- 0bcfaf79 (APPLY): one occupation. Keep the social history (IT project manager) and rewrite the
  HPI's teaching details. Delete the penicillin text.
- aed4aacd (APPLY): C4 list. The empty-tool part is ALREADY-FIXED.
- Survey: HPI MRI leak.

### GLIO-HG-M04 (man, 38, right frontal astrocytoma IDH-mutant grade 4, focal seizures)
- 457ccd8f (APPLY): group A resection, with fMRI and DTI motor mapping (C6).
- af437c8f (APPLY): add CDKN2A_B_deletion to the list and the report: "no homozygous deletion";
  grade 4 rests on MVP and necrosis.
- Survey:
  - Treat class: recast "post-operative prophylaxis" as continued treatment.
  - Remove the EEG waste entry.
  - C11: no Stupp; IDH-mutant grade 4 managed like GBM.
  - The synonyms "glioblastoma" and "GBM" are wrong (CENTRAL).
  - HPI MRI leak.

### GLIO-HG-M05 (man, 45, left frontoparietal astrocytoma IDH-mutant grade 3, no seizures)
- 618200ca (APPLY): CDKN2A_B_deletion "no homozygous deletion", so grade 3 is established.
  Rewrite the key evidence that claims "lacks all grade-4 features" to cite the result.
- 0c310d30 (APPLY): no-seizure class. Remove must 5 and the levetiracetam proposal.
- 615481ca (APPLY): group A resection. Add fMRI (premotor) and DTI (corona radiata and CST)
  criteria and outputs. Must 2 becomes the C3 must.
- Survey:
  - The HPI "MRI brain with gadolinium ... radiologist raised concern for a glioma" is a C8 leak.
  - Must 6 duplicates the "no therapy before tissue" prohibition; delete the must.
  - The required molecular list in must 3 follows C4.
  - Synonym "glioblastoma" is wrong (CENTRAL).

### GLIO-HG-P01 (man, 48, right frontotemporal GBM mimicking abscess, GTC seizure)
- d3ff3f30 (APPLY): rewrite the red herring (C12).
- e25c4336 (APPLY): change the CT to a hypodense lesion with oedema (C8).
- 83979d94 (APPLY): C10.
- Survey:
  - Group B.
  - Blood cultures to microbiology; ID consult and dental evaluation become musts (C14).
  - Delete the mislabelled perfusion.
  - Delete the dental speculation from the MRI impression.
  - MCHC 31.4.
  - Treat class.

### GLIO-HG-P02 (man, 56, EBV-associated PCNSL, new HIV/AIDS)
- 5481518a (APPLY): delete the CSF follow-up; harm stays. The diagnosis comes from the biopsy.
- 5dae46fc (APPLY): one steroid must: `Withhold corticosteroids until the stereotactic biopsy is obtained, because they can render lymphoma non-diagnostic; give dexamethasone first only if herniation is impending [EANO_PCNSL_2015].` Delete the loading-dose must.
- 20ea01fe (APPLY): `molecular_assays` `CD20_IHC`, `EBER_ISH`. The report gives CD20 positive,
  EBER positive, Ki-67, and flow cytometry on tissue if wanted as a finding row. Group C biopsy
  only.
- Survey:
  - Replace the Stupp must with: `Refer to haematology and neuro-oncology for high-dose methotrexate-based induction, and start antiretroviral therapy with infectious-disease input [EANO_PCNSL_2015].`
  - Delete the duplicate toxoplasmosis differential entry, the duplicate perfusion follow-up and
    the `interpret_labs` PET-CT.
  - Add a coagulation panel.
  - No-seizure class.
  - The accepted label wording is open question 6.

### GLIO-HG-P03 (man, 48, right frontotemporal GBM mimicking abscess, focal-to-bilateral seizure)
- 1163206c (APPLY): rewrite both red herrings from the printed MRI; histology is diagnostic.
- 76e5c5d3 (APPLY): merge the duplicated abscess and demyelination entries.
- dde4d001 (APPLY): one occupation (history teacher, matching the HPI). Na normalised.
- Survey: group B; blood cultures; delete the demyelination work-up follow-up and the mislabelled
  perfusion; treat class.

### GLIO-HG-P04 (man, 55, right temporoparietal GBM, abscess on the differential, no seizures)
- ab9b72cb (APPLY): no-seizure class.
- 16cb2bae (APPLY): delete "excludes abscess" and "decisively", and the Law attribution (C1,
  C12). Must 1 says perfusion supports the neoplasm and the tissue with microbiology decides.
- 33019b2d (APPLY): delete the steroid clause.
- Survey:
  - Group B.
  - Delete the initial literature_search.
  - The microbiology criterion stays required and must be the aspirate culture.
  - Add the blood-culture recommended criterion.
  - The HPI CT is called ring-enhancing (C8).

### GLIO-HG-P05 (woman, 30, right thalamic diffuse midline glioma H3 K27M-altered)
- 9046c896 (APPLY): no-seizure class. Remove levetiracetam from step 4 and from the action-8
  expected evidence.
- bc69f5ec (APPLY): rewrite the red herrings as biopsy targeting; H3 K27 status defines the
  entity.
- e8cfa028 (APPLY):
  - Low-grade glioma becomes low, since the entity is fixed by H3 K27 and the MRI enhancement.
  - Thalamic infarction becomes very low, since there is no restricted diffusion and a 3-week
    progression.
  - MS stays low.
- Survey:
  - Group C biopsy only.
  - The assay list adds H3K27_status and IDH1_IDH2_sequencing.
  - Delete the optional CT criterion and its follow-up.
  - C11 (DMG).
  - Synonyms include "glioblastoma" (CENTRAL).
  - Check that the waste entries do not hit the recommended perfusion and MRS.

### GLIO-HG-RM01 (man, 67, pontine GBM IDH-wildtype, H3-wildtype)
- 16e1c115 (APPLY): add H3K27_status and IDH1_IDH2_sequencing. The report reads "H3 K27M not
  detected; H3K27me3 retained", which makes it GBM, IDH-wildtype, rather than DMG. Group C biopsy
  only.
- 61968ced (APPLY): no-seizure class. The empty-tool part is ALREADY-FIXED. Musts 1 and 3 without
  an action become musts, not criteria; check they are management and not tests.
- Survey:
  - Fourth-ventricle compression makes the LP harm.
  - Performance status required (67).
  - Delete the mislabelled perfusion.
  - The `analyze_brain_mri` follow-up must be checked for a duplicate of the initial MRI; delete
    it if it is one.

### GLIO-HG-RM02 (woman, 34, cervical intramedullary GBM IDH-wildtype)
- a02b3fb0 (APPLY): add H3K27_status and IDH1_IDH2_sequencing. The report states H3 wildtype, or
  the entity changes, which would be BLOCKED.
- fea3f998 (APPLY): delete the CSF follow-up; spinal-block harm rationale (C17).
- 7dbf817c (APPLY):
  - Rewrite action-1 as the exclusion of intracranial disease, with expected evidence "no
    intracranial lesion" from its own brain MRI.
  - The brain MRI output's first finding ("bilateral occipital, epicranial") must be checked and
    made a plausible normal or incidental report.
- 15ee9c7d (APPLY): one contrast spine MRI (`action-2-order-body-imaging`), first in criteria and
  follow-ups. Delete the non-contrast duplicate.
- Survey: group D (`resection` as open biopsy); hard spine MRI to tissue; no-seizure class;
  CENTRAL `open_biopsy`.

### GLIO-HG-RM03 (woman, 21, right cerebellar and vermian GBM IDH-wildtype, early hydrocephalus)
- 55929ced (APPLY): add IDH1_IDH2_sequencing (under 55) and H3K27_status (vermis); the report
  reads H3 wildtype.
- 1a5bdcb8 (APPLY): no-seizure class. The empty-tool part is ALREADY-FIXED.
- Survey:
  - Group A resection, which also relieves the fourth-ventricle compression. Add a must on
    managing the hydrocephalus (external ventricular drain or resection).
  - The LP is harm.
  - Delete the mislabelled perfusion.

### GLIO-HG-RM04 (man, 57, right temporal GBM with gliosarcoma histology, probable focal seizures)
- 16ac8653 (APPLY): probable class. Recommended EEG criterion and a new EEG output; remove the
  EEG waste entry.
- 2cd403c7 (APPLY): group A resection.
- b8bef5c9 (APPLY):
  - Replace `action-8-analyze-brain-mri` (standard, sequences DTI/fMRI) with
    `action-fmri-functional-mapping` (language laterality; the lesion is in the non-dominant
    hemisphere, laterality index 0.86 left) and `action-dti-tractography` (optic radiation and
    the right-sided tracts), both recommended.
  - Move the `analyze_brain_mri` follow-up content into the two advanced-imaging outputs.
  - Delete the right-arcuate explanation of the anomia. The word-finding difficulty is explained
    by mass effect, oedema or seizures, not by a right tract. Write that in key evidence.
- Survey:
  - The DDI criterion is recommended now; make it optional unless a concrete interaction exists
    (ruling 6).
  - Label per open question 2. Delete the "Glioblastoma, classic variant" differential entry.
  - HPI MRI leak.

### GLIO-HG-RP01 (woman, 68, right temporal GBM, prior thyroid cancer, focal motor seizure)
- 786de7f4 (APPLY):
  - One thyroglobulin story: the HPI's "undetectable" six months ago against the panel value of
    3.2 ng/mL after hemithyroidectomy.
  - Resolve with the residual-tissue argument (values up to 5 to 10 ng/mL), moved into the red
    herring from the deleted literature.
  - Fix the flag and the reference range to the hemithyroidectomy context.
- 7dc06c7a (APPLY): treat class (a 30-second left-hand focal motor seizure); add the must.
- 6538e4db (APPLY): action-1 expected evidence from its MRI (patchy marginal enhancement, no
  necrosis).
- Survey:
  - CT CAP becomes recommended.
  - The `interpret_labs` thyroid ultrasound becomes a must (C14).
  - PAX8, TTF-1 and thyroglobulin IHC go to CENTRAL.
  - Performance status required.
  - fMRI and DTI by rule.
  - Delete the penicillin and sulfonamide sentence unless it is true.

### GLIO-HG-RP02 (woman, 44, right frontal precentral GBM; tumefactive MS and tuberculoma considered)
- 39e8c0d3 (APPLY, as class C2).
- 41984330 (APPLY): action-1 expected evidence from its MRI (no central restricted diffusion,
  minimal rim restriction, central FLAIR hypointensity).
- 2b8748f1 (APPLY, the differential option):
  - Add tumefactive demyelination with its discriminators: incomplete ring, the second left
    frontal lesion and the sister's MS for it; rCBV 4.2 and Cho/NAA 5.2 against it. Likelihood
    low after the work-up.
  - Add tuberculoma, with prior pulmonary TB for it and the perfusion and spectroscopy against
    it. Likelihood low.
  - Add a red herring for the family history of MS and the second lesion.
- Survey:
  - Uncertain class for the staring spell, with a recommended EEG. EEG laterality per C9.
  - Delete the CSF follow-up (C17).
  - Group A, fMRI and DTI motor.
  - HPI "initial imaging" leak (C8).
  - Delete the penicillin and sulfonamide sentence unless it is true.

### GLIO-HG-RP03 (man, 31, IDH-mutant astrocytoma with leptomeningeal dissemination, on prednisone, VP shunt)
- 4ebbab11 (APPLY, add-CDKN2A/B option):
  - CDKN2A/B is "homozygous deletion detected", giving "Astrocytoma, IDH-mutant, CNS WHO grade
    4, with leptomeningeal dissemination".
  - Delete "Grade 2 (with features of higher-grade behavior)", the cyst-fluid row and the
    original-biopsy row from `molecular_findings`. Keep the original biopsy in the HPI or history.
  - Change accepted[0] per ruling 3 (label not supported by the data; CENTRAL; open question 3).
- 753d78af (APPLY):
  - Move analyze_csf out of the harm list.
  - Add a recommended `action-csf-cytology`: `analyze_csf` `{"special_tests": ["cytology", "flow_cytometry"]}`, with a hard MRI-to-CSF constraint.
  - Author a CSF output: raised protein, atypical glial cells on cytology, no monoclonal B cells
    on flow. Mild papilloedema and the shunt are noted in the rationale: the MRI shows no
    herniation risk and the shunt is functioning.
- 928080d2 (APPLY):
  - Add CNS lymphoma to the differential: steroid response, then a non-diagnostic biopsy, for
    it; IDH-mutant tissue and negative flow against it. Likelihood low.
  - Recast must 3: `Do not start dexamethasone; continue prednisone without abrupt withdrawal, at the lowest dose that controls symptoms, and plan tissue sampling knowing that steroids can make a lymphoma biopsy non-diagnostic.`
- Survey:
  - Continue levetiracetam (treat class, continue form).
  - Group C, biopsy then resection.
  - Coagulation panel.
  - C11 IDH-mutant grade 4.
  - Delete the mislabelled perfusion.
  - The second `analyze_brain_mri` follow-up: check for a duplicate (delete it) or keep it as a
    spine MRI under `order_body_imaging` if it reports the spine.
  - Synonym "glioblastoma" is wrong (CENTRAL).

### GLIO-HG-RP04 (man, 52, multicentric GBM, melanoma excluded, speech arrest)
- 0c2fc022 (APPLY): add SOX10_IHC and Melan_A_HMB45_IHC to the list and to the report (SOX10
  negative, Melan-A and HMB-45 negative). Must 6 names the markers that exist. Drop H3K27_status
  if there is no midline lesion.
- eb3f1800 (APPLY): treat class (speech arrest with staring); recommended EEG and a new output;
  remove the EEG waste entry.
- 0289beef (APPLY): required performance status, with an output derived from the current
  examination (hemiparesis, quadrantanopia, cognitive decline). The social-history KPS 80 is
  labelled pre-illness.
- Survey: CT CAP stays required; group C, biopsy of the dominant lesion then resection; the
  treatment must uses the KPS.

### GLIO-HG-RS01 (man, 35, right frontotemporal GBM, hereditary paraganglioma syndrome)
- e649546c (APPLY): delete the chr7/10 lab row.
- 32b30a51 (APPLY): C4 list with IDH sequencing (under 55).
- 075ad500 (APPLY):
  - The skull-base lesion is located at the right jugular foramen in the posterior cranial
    fossa. Delete "middle cranial fossa". It is a jugular foramen paraganglioma.
  - Attribute the deficits it can explain: lower cranial nerves and the right sensorineural
    hearing loss.
  - The proptosis and the V2, V3 and acuity deficits need a lesion at the orbit, cavernous sinus
    or skull base. Either extend the paraganglioma report (petrous apex to the cavernous sinus)
    or remove the deficits it cannot produce. Log which.
  - The red herring no longer dismisses it.
  - Add `action-paraganglioma-genetics` (recommended), and musts for a skull-base team referral
    and plasma free metanephrines before any anaesthesia.
  - Chromogranin IHC goes to CENTRAL.
- Survey:
  - CT CAP becomes recommended.
  - The catecholamine `interpret_labs` follow-up is converted (C14).
  - EEG template impression (C9).
  - Seizure: the HPI denies prior seizures; check the presenting event and classify it.

### GLIO-HG-RS02 (man, 59, right frontal precentral GBM, focal-to-bilateral seizure)
- 7fdc5cfc (APPLY): group A resection; must 1 per C3.
- c27c5e41 (APPLY): C4 list.
- 6e655625 (APPLY): retag the step as functional_MRI plus DTI_tractography, with recommended
  criteria.
- Survey: treat class; the second DDI follow-up merges into one.

### GLIO-HG-RS03 (woman, 31, right precentral GBM, focal-to-bilateral seizure, LPDs)
- 92ef1523 (APPLY): delete the chr7/10 lab row.
- b0d00a8d (APPLY): C4 list with IDH sequencing.
- f4b30a6a (APPLY, the impression-plus-action option):
  - The LPDs go in the impression.
  - Recommended `action-eeg-characterise-spells`, with the label changed to "EEG to characterise
    the post-ictal state".
  - Add a must: `Continue EEG monitoring given LPDs after a first seizure, and escalate antiseizure treatment if electrographic seizures appear.`
- d061a446 (APPLY): group A resection; fMRI and DTI (CST thinning) as recommended criteria.
- Survey: treat class.

### GLIO-HG-RS04 (man, 52, left parietal GBM with giant cell histology, prior seizure on levetiracetam)
- d02be965 (APPLY):
  - The integrated diagnosis becomes "Glioblastoma, IDH-wildtype, CNS WHO grade 4". The
    histology line reads "glioblastoma with giant cell features".
  - accepted[0] changes accordingly (ruling 3, CENTRAL).
  - Delete the "Conventional glioblastoma" differential entry.
- a091c170 (APPLY): add BRAF_V600 to the list and the report (BRAF V600E not detected). Add PXA to
  the differential at low (`[vandenBent_2025]`).
- Survey:
  - Continue levetiracetam and recast "seizure prophylaxis" in the history as treatment after a
    GTC seizure.
  - The fMRI_BOLD follow-up is retagged (C6).
  - Merge the two DDI follow-ups.
  - The prior acyclovir course is history.

### GLIO-HG-RS05 (man, 64, left temporal GBM, aphasia, speech arrest)
- 79fc1c6f (APPLY): treat class. Must 4 becomes the treat must.
- 65ef42fb (APPLY): C4 list.
- 666dbf49 (APPLY):
  - Add functional_MRI (language) and DTI_tractography (arcuate, optic radiation) as recommended
    criteria and outputs.
  - Must 2 becomes: `Refer urgently to neurosurgery for maximal safe resection of the left temporal lesion with preoperative functional MRI and DTI tractography; awake language mapping is limited by the current comprehension and naming deficits, so the approach (awake mapping, asleep resection with subcortical monitoring, or biopsy) is decided after neurosurgical and neuropsychological assessment.`
- Survey:
  - HPI outpatient MRI and the repeat-MRI sentence (C8).
  - Dexamethasone already started: continue (C8).
  - Remove the EEG waste entry.
  - MRI optic radiation anatomy (C9).
  - MRI impression item 2, "consistent with the clinical quadrantanopia", is cross-modality;
    delete the clinical clause.
  - The aspirin discontinuation must stays.

### GLIO-HG-RS06 (woman, 71, left temporoparietal GBM, anomia, on hydroxychloroquine)
- 39805cb7 (APPLY): no-seizure class; delete levetiracetam from step 4.
- 76ce5cab (APPLY): group A resection; fMRI (Wernicke, angular gyrus) and DTI (arcuate, optic
  radiation) recommended.
- Survey:
  - DDI recommended (hydroxychloroquine and QT).
  - Performance status required.
  - C11 over-70 regimen.
  - Delete "consistent with the clinical ..." from the MRI impression.

### GLIO-HG-S01 (man, 58, right precentral GBM, focal-to-bilateral seizure)
- 7d836e30 (APPLY): C4 list.
- 73339f93 (APPLY): Hct about 44; PT normal.
- Survey:
  - Na 152 normalised.
  - Delete the chr7/10 lab row.
  - EEG sharp waves in the impression.
  - CT and MRI shift agree.
  - fMRI_BOLD retagged; treat class.

### GLIO-HG-S02 (woman, 64, right precentral and insular GBM, focal-to-bilateral seizure; no notes)
- Survey:
  - Na 130 normalised unless used.
  - MCHC 38.6.
  - fMRI_BOLD retagged.
  - Treat class.
  - Occupation: check "high school math teacher" against the social history.

### GLIO-HG-S03 (man, 52, right frontal GBM, focal-to-bilateral seizure; no notes)
- Survey: EEG template impression (C9); fMRI_BOLD retagged; treat class.

### GLIO-HG-S04 (man, 71, right frontoparietal GBM, GTC seizure; no notes)
- Survey:
  - Baseline perfect-agent failure (C1).
  - Anion gap 17; MCHC 39.
  - EEG "correlate with seizure" (C9).
  - fMRI_BOLD retagged.
  - Merge the two DDI follow-ups.
  - Treat class.
  - Performance status required.
  - C11 over-70 regimen.

### GLIO-HG-S05 (man, 60, left parietal GBM, no seizures; no notes)
- Survey:
  - Engineering text in `molecular_findings` (C16).
  - No-seizure class.
  - fMRI and DTI by rule.
  - The ECG waste entry stays.

### GLIO-HG-S06 (woman, 67, left occipital GBM, visual field deficit, no seizures; no notes)
- Survey:
  - HPI outpatient MRI (C8).
  - Delete "consistent with the clinical ..." from the MRI impression.
  - DTI only (optic radiation).
  - No-seizure class.
  - Performance status required.
  - The early obstructive dilatation of the occipital horn makes the LP harm.

Coverage check: 72 note ids, all cited above. M01 3, M02 2, M03 5, M04 2, M05 3, P01 3, P02 3,
P03 3, P04 3, P05 3, RM01 2, RM02 4, RM03 2, RM04 3, RP01 3, RP02 3, RP03 3, RP04 3, RS01 3,
RS02 3, RS03 4, RS04 2, RS05 3, RS06 2, S01 2.

---

## 5. CENTRAL requests (outside the case files)

1. **Criteria pack allow-list** (`criteria_packs/GLIO-HG.md`): add `[AIOM_brain]` (AIOM Linee guida
   Neoplasie cerebrali), `[vandenBent_2025]`, `[ACR_contrast]` and `[EANO_PCNSL_2015]`. Supersede
   the pack's "literature required" position (ruling 5).
2. **Synonyms** (`diagnosis_synonyms.yaml`):
   - "glioblastoma", "GBM" and "astrocytoma grade 4" are appended to IDH-mutant astrocytoma
     cases (M04, M05, RP03) and to the diffuse midline glioma (P05). They are wrong for both
     entities; give each its own synonym set.
   - "astrocytoma grade 4" is wrong for an IDH-wildtype GBM. Remove it from the GBM set.
3. **Label changes (ruling 3)**:
   - RS04: "Glioblastoma, IDH-wildtype, CNS WHO grade 4".
   - RP03: "Astrocytoma, IDH-mutant, CNS WHO grade 4 with leptomeningeal dissemination".
   - RM04 per open question 2.
   - M02 site suffix "(high-grade glioma)" to "(left temporal lobe)".
   - Normalise "WHO grade" to "CNS WHO grade" across accepted[0] if the synonyms tool keeps
     matching.
4. **Vocabulary**:
   - an `open_biopsy` procedure (RM02 intramedullary);
   - chromogranin and synaptophysin IHC (RS01);
   - PAX8, TTF-1 and thyroglobulin IHC (RP01, metastasis exclusion);
   - confirm that `flow_cytometry` on tissue exists, or accept it as a findings row only (P02).
5. **Fallback library**: the benchmark fallback for `search_medical_literature` must not return
   glioma-specific text that echoes any criterion. Check this after C1 removes the case outputs.
6. **Review UI**: show initial and follow-up outputs in criterion order, so reviewers see the
   tissue result under the tissue action.

## 6. Open questions for Andrea

1. **AIOM edition**: the reviewer cites Quesito 1 and Quesito 23 and asks for the numbering to be
   re-verified against the 2026 edition, while the tool guidance says "AIOM 2023". Which edition
   should the `[AIOM_brain]` key name?
2. **RM04 label**: gliosarcoma is a histological subtype of glioblastoma, IDH-wildtype, in WHO
   CNS5, the same logic as the RS04 ruling. Should accepted[0] become "Glioblastoma, IDH-wildtype,
   CNS WHO grade 4" with gliosarcoma in the histology line? The plan assumes yes.
3. **RP03 grade**: the plan adds CDKN2A/B homozygous deletion, which makes it grade 4, as the
   reviewer's data suggest. The alternative is grade 2 with the contradicting features removed.
4. **`max_additional_actions`**: keep 0, or 1 as ISCH-STR did, now that each case has several
   recommended criteria?
5. **Performance status as required at 65 or over**: is age a good proxy, or should it be
   required in all 30 (treatment choice always depends on KPS)?
6. **P02 label**: keep "Primary CNS lymphoma (EBV-associated DLBCL) in the setting of newly
   diagnosed HIV/AIDS", or use the WHO name "EBV-positive diffuse large B-cell lymphoma of the CNS,
   HIV-associated"?
7. **Biopsy as an equal alternative in group A**: the plan accepts `stereotactic_biopsy` as a
   second alternative with full credit for resectable lesions. Should it instead earn reduced
   credit or be dropped, with resection alone accepted?
