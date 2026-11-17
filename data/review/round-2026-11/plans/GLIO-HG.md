# GLIO-HG round plan (November 2026)

Lead plan for the 30 GLIO-HG cases. Read `data/review/round-2026-10/ROUND_POLICY.md`, then
`work/NOVEMBER_ADDENDUM.md`, and keep the October plan (`round-2026-10/plans/GLIO-HG.md`) and the
pack (`dataset-generation/criteria_packs/GLIO-HG.md`) in force. Decisions with reasons and sources
are in `GLIO-HG-decisions.md` (D1 to D11).

Facts about the notes:
- All 10 notes are from R2 (NB-87MF-FBTV-TPWE) and cover 5 cases (S02 to S06).
- R2 read a build from before October, so 5 notes are already fully fixed and 2 are fixed in part.
- No GLIO-HG case is in `work/approved.txt`.
- Baseline on 17 Nov 2026: perfect_agent 30/30.
- Measurement scripts are in `work/scratch/glio-lead/` (`measure.py`, `table1.py`, `labs_chk.py`).

Helpers are in `data/review/round-2026-11/bin/`: `case_io.py`, `perfect_agent.py`, `caselog.py`
and `mri_probe.py`. After any MRI edit, run `mri_probe.py` on the case, and edit both the plain
study and the gadolinium study. In new text use no em dashes, US spelling as in these cases, and
keep criterion ids unchanged.

## 1. Governing guidelines and canonical facts

| question | source | key |
| --- | --- | --- |
| Entity, grade, integrated diagnosis | WHO CNS5 (Louis 2021) | `[WHO_2021]` |
| Testing, surgery, treatment by age and KPS (cut-off 70) | EANO 2021 (Weller, Nat Rev Clin Oncol 18:170) | `[EANO_2021]` |
| Short-course RT 40 Gy/15 with TMZ, patients 65 or over | Perry, NEJM 2017;376:1027 | `[Perry_2017]` |
| Aspirin stopped at least 7 days before intracranial neurosurgery (high bleeding risk, Class I C) | ESC 2022 non-cardiac surgery, Eur Heart J 43:3826 | `[ESC_NCS_2022]` |
| Platelet transfusion for antiplatelet-associated ICH needing neurosurgery; test platelet function first; not for NSAIDs | Frontera, Neurocrit Care 2016;24:6-46 | `[Frontera_2016]` (CENTRAL 1) |
| Abscess aspiration within about 24 h | ESCMID 2024 | `[ESCMID_BA_2024]` |
| PCNSL imaging and steroids | EANO PCNSL 2015 | `[EANO_PCNSL_2015]` |

Canonical facts:
- Glioblastoma, IDH-wildtype, aged 70 or under with KPS 70 or more: the standard is 60 Gy in 30
  fractions with temozolomide.
  - Over 70, or KPS under 70: hypofractionated radiotherapy.
  - From age 65, Perry 2017 makes 40 Gy in 15 fractions with temozolomide an evidence-based
    option. Its benefit is largest when MGMT is methylated.
- Aspirin: stop at least 7 days before a planned craniotomy or stereotactic biopsy.
  - Urgent surgery does not wait for the washout: operate with platelet function testing where
    available and platelet transfusion ready.
  - NSAIDs act reversibly: stop them now. No platelet transfusion is given for them.
- A homonymous field defect localises to the retrochiasmal pathway. The MRI that explains it names
  the involved segment: temporal stem (Meyer loop), sagittal stratum (optic radiation) or
  occipital cortex.
- Tumour reaching the corpus callosum:
  - limits the safe extent of resection;
  - keeps lymphoma in the pre-biopsy differential, although callosal spread is also typical of
    glioblastoma.
- Differential likelihood is the assessment-time view (ruling 7), so an alternative that tissue
  excludes stays very_low or low.

## 2. Classes

### C1 MRI-CONTRAST (D1)
- Notes: 4022233f (S03), 365d96f2 (S04), c011f7ee (S05), f987e3d1 (S06).
- Measured: all 30 cases already have the pair (plain initial `contrast_used: false`, gadolinium
  follow-up `true`), and every MRI criterion orders `contrast: true`.
- Fix: none (ALREADY-FIXED, commit 71517e55).

### C2 FIELD-LOCALISATION (D2)
- Note: 36546be3 (S02, hemianopia part).
- Measured: 10 of 30 cases have a field defect. The MRI is silent on the visual pathway in P04,
  S02 and S04. Outside the condition, VASC-DEM-S11 has the same defect.
- Fix: R2's option A. Both MRI studies name the optic-radiation segment, in the oedema `FLAIR`
  signal and in the impression. In S02 the DTI row and the DTI expected evidence also change.
- Canonical text: in D2.

### C3 ANTIPLATELET-TIMING (D5)
- Note: f465277d (S04).
- Measured: 9 cases take aspirin before neurosurgery (all 9 in GLIO-HG across the 600 cases).
  - P03, RM01, S02, S04 and S05 have no interval.
  - RM04, RP01, RP04 and RS05 already state about 7 days.
  - Ibuprofen-only cases already stop it now. P05 used ibuprofen and has no must.
- Fix: a must (R2's option A), not a tool and not text in the operative report.
  - Variant A (planned surgery): RM01, S04, S05.
  - Variant B (urgent surgery): S02, P03.
  - P05: an NSAID stop must.
- Canonical text: in D5.

### C4 FMRI-UNSCORED (D6)
- Note: 1e375c3a (S05).
- Measured: S05 is the only case with an fMRI follow-up that meets rule C6 (hand motor area 9 mm
  from the margin) and has no criterion. The other unscored DTI follow-ups answer off-pathway orders
  in group B and C cases.
- Fix: recommended criterion, soft constraint, pathway order and must wording.

### C5 DIFFERENTIAL-CALLOSAL (D7)
- Note: 35803946 (S03).
- Fix: the PCNSL `key_features` name the callosal extension in S03 and M04. Likelihood stays
  very_low (partial DECLINE, ruling 7). The display question goes to CENTRAL 3.

### C6 CALLOSAL-RESECTION (D8)
- Note: 35803946 (S03).
- Measured: the tumour (not the oedema) reaches the corpus callosum in S03, M04 and M05.
- Fix: a clause in the surgery must. In S03, also the resection extent row.

### C7 TREATMENT-65-70 (D9)
- Note: a1f18356 (S06).
- Measured: S06 is the only case aged 65 to 70 with KPS 70 or more.
- Fix: the treatment must becomes a discussion of Stupp versus Perry, with the MGMT remark. Key
  clinical evidence item 7 changes to match.

### C8 VENTRICLE-ENTRAPMENT (D10)
- Note: a1f18356 (S06).
- Measured: positive ventricular obstruction in 6 MRIs. P05, RM01 and RM03 already have a must. S02
  is covered in part, and S03 and S06 have none.
- Fix: a canonical must in S03 and S06, and a clause added to the S02 must.

### C9 CBC / ASSAY LIST / PERFORMANCE STATUS (D3, D4)
- Notes: b63e4af9 (S02), and the language part of 36546be3.
- Measured:
  - MCHC and anion gap are clean in 30/30.
  - The tissue label matches its arguments in 30/30.
  - Performance status is required in 30/30.
- Fix: none (ALREADY-FIXED in October).

## 3. Per-case index (all 30; none approved)

Every changed case:
- runs `perfect_agent.py CASE -v` and `case_io.py check CASE`, plus `mri_probe.py CASE` if an MRI
  was touched;
- writes `data/review/round-2026-11/logs/{CASE}.md` with every note id of the case.

"Class" lines are findings with no note in that case.

### GLIO-HG-M01
- No note. NO-ACTION. The field defect is only "questionable", and the temporal-lobe FLAIR already
  covers Meyer loop, as the DTI shows.

### GLIO-HG-M02
- No note. NO-ACTION.

### GLIO-HG-M03
- No note. NO-ACTION. The MRI names Meyer loop.

### GLIO-HG-M04
Class:
- C6: add the callosal clause to the surgery must (`required_recommendations[0]`), and check that
  the resection report does not claim removal of the genu component.
- C5: rewrite the PCNSL `key_features` with the M04 text from D7.

### GLIO-HG-M05
Class:
- C6: add the callosal clause to the surgery must (FLAIR infiltration to the posterior body), and
  check the resection report for consistency.

### GLIO-HG-P01
- No note. NO-ACTION.

### GLIO-HG-P02
- No note. NO-ACTION. Lymphoma is the answer here.

### GLIO-HG-P03
Class:
- C3 variant B: replace "Hold aspirin before the neurosurgical procedure; ..." with the variant-B
  must ("aspiration and biopsy", "because the aspirate should be obtained within about 24 hours").
  Also stop the over-the-counter ibuprofen named in the HPI.

### GLIO-HG-P04
Class:
- C2: in both MRI studies, the FLAIR of the right temporal-parietal white matter and the impression
  name "the superior fibers of the right optic radiation", which explains the left inferior
  quadrantanopia.
- Check that the stored DTI follow-up and the perimetry agree.

### GLIO-HG-P05
Class:
- C3: add the must "Avoid ibuprofen and other NSAIDs before the stereotactic biopsy and while on
  dexamethasone; use paracetamol for headache."

### GLIO-HG-RM01
Class:
- C3 variant A ("stereotactic biopsy"): replace "Hold aspirin, taken for primary prevention, before
  the stereotactic biopsy."

### GLIO-HG-RM02
- No note. NO-ACTION.

### GLIO-HG-RM03
- No note. NO-ACTION. The hydrocephalus must already exists.

### GLIO-HG-RM04
- No note. NO-ACTION. The aspirin must already states about 7 days.

### GLIO-HG-RP01
- No note. NO-ACTION. The aspirin must already states about 7 days.

### GLIO-HG-RP02
- No note. NO-ACTION.

### GLIO-HG-RP03
- No note. NO-ACTION.

### GLIO-HG-RP04
- No note. NO-ACTION. The aspirin must already states 7 days, and the PCNSL entry is already argued
  from imaging.

### GLIO-HG-RS01
- No note. NO-ACTION.

### GLIO-HG-RS02
- No note. NO-ACTION. The callosal signal is oedema.

### GLIO-HG-RS03
- No note. NO-ACTION.

### GLIO-HG-RS04
- No note. NO-ACTION.

### GLIO-HG-RS05
- No note. NO-ACTION. The aspirin must already states 7 to 10 days.

### GLIO-HG-RS06
- No note. NO-ACTION. Age 71: the hypofractionated must, citing Perry 2017, is already present.

### GLIO-HG-S01
- No note. NO-ACTION. The callosal signal is oedema, and the ibuprofen must is correct.

### GLIO-HG-S02
Notes:
- 36546be3-bfd0-4395-af96-c665d7713f60:
  - hemianopia part FIXED (C2, D2), language part ALREADY-FIXED (D3);
  - plain and gadolinium MRI: the oedema finding's `FLAIR` and `location`, and impression item 2,
    name the right temporal stem and sagittal stratum (optic radiation);
  - DTI follow-up: optic-radiation row, impression item 2, and the `action-dti-tractography`
    `expected_evidence`;
  - `key_clinical_evidence[5]` wording on the optic radiation, to match.
- b63e4af9-3655-477c-b5ce-fca8be1e9121: ALREADY-FIXED (D4). Hb 14.1 / Hct 43.2 / RBC 4.65; ATRX is
  in both the label and the arguments; `action-performance-status` is required and is in the stop
  rule.

Class:
- C3 variant B: replace "Stop primary-prevention aspirin and as-needed ibuprofen now, ...". Keep the
  clause "and avoid them while on dexamethasone".
- C8: the monitored-bed must reads "... for the early right uncal herniation and the trapped right
  temporal horn; ...".

### GLIO-HG-S03
Notes:
- 4022233f-0d83-4640-9087-04f19ab96492: ALREADY-FIXED (C1). The plain initial is `false`, the FU0
  gadolinium study is `true`, and `action-1` orders contrast.
- 35803946-1534-47a0-bd45-bcc0f320096c:
  - FIXED in part (C5, C6): the PCNSL `key_features` use the S03 text from D7;
  - the surgery must gets the callosal clause;
  - the resection report's "Extent of resection" row uses the D8 text;
  - DECLINED in part: the likelihood stays very_low (ruling 7, assessment-time view; tissue shows
    glioblastoma, and the necrotic ring is atypical of PCNSL); the display question goes to
    CENTRAL 3.

Class:
- C8: add the entrapment must for "early trapping of the right lateral ventricle".

### GLIO-HG-S04
Notes:
- 365d96f2-6f2b-4f95-b763-a59bd5cd6f6d: ALREADY-FIXED (C1).
- f465277d-b437-4b01-a66f-58396cb39d9b: FIXED (C3 variant A, "craniotomy", "and the
  over-the-counter ibuprofen"; keep "and avoid them while on dexamethasone").
  - The must replaces `required_recommendations[3]`.
  - The operative entry is unchanged: R2's option B is not taken, because of ruling 4 (D5).
  - The platelet-function assay goes to CENTRAL 2.

Class:
- C2: in both MRI studies, the oedema `FLAIR` and impression item 2 name "the right sagittal stratum
  (optic radiation)".

### GLIO-HG-S05
Notes:
- c011f7ee-37ac-4adb-88ae-bbdab0a53443: ALREADY-FIXED (C1). The red herring cites the contrast MRI,
  which the criterion now receives.
- 1e375c3a-6405-458b-81bb-ccb98dc26878: FIXED (C4, D6).
  - Add `action-fmri-functional-mapping` (recommended), placed before `action-dti-tractography`.
  - Move the fMRI follow-up (now FU18) to before the DTI follow-up.
  - Add a soft constraint fMRI -> `action-10-obtain-tissue-diagnosis`.
  - The surgery must names "preoperative functional MRI and DTI tractography and intraoperative
    subcortical mapping".
  - The operative `site` text stays.
  - The "empty tool fields" were a stale review-app build: the constraints carry valid ids
    (verified).

Class:
- C3 variant A: replace the aspirin must ("Stop the aspirin started for presumed TIA: the deficit is
  explained by the tumor, and schedule the craniotomy at least 7 days ...").

### GLIO-HG-S06
Notes:
- f987e3d1-7e31-42ae-becd-8fb2959bdd82: ALREADY-FIXED (C1).
- a1f18356-a409-41ef-9564-d395861c0bf2: FIXED (C7, C8; D9, D10).
  - The treatment must becomes the D9 discussion (Stupp versus Perry, unmethylated MGMT). It is not
    a switch, because EANO 2021 keeps 70 as the cut-off. That part is DECLINED and the reason is
    logged.
  - Add the entrapment must for the occipital horn.
  - Change `key_clinical_evidence[6]` to match.
  - "A treatment-planning step" is a must, not a tool (ruling 4).

## 4. CENTRAL requests

1. Pack allow-list (`criteria_packs/GLIO-HG.md` section 9): add `[Frontera_2016]`: Frontera JA,
   Lewin JJ 3rd, Rabinstein AA, et al. Guideline for reversal of antithrombotics in intracranial
   hemorrhage. Neurocrit Care 2016;24:6-46. Extend the `[ESC_NCS_2022]` scope to "aspirin stopped at
   least 7 days before intracranial neurosurgery". Add to section 6: "Aspirin before neurosurgery:
   stop at least 7 days before planned surgery; urgent surgery proceeds with platelet function
   testing and platelet transfusion ready".
2. Vocabulary (`costs.yaml`, `interpret_labs`): a `platelet_function` panel (PFA-100 or VerifyNow
   aspirin assay), with a library normal and the `tool_io.py` mirror. This would let the aspirin
   cases score a pre-operative platelet-function step. It is not needed for this round.
3. Review app (`web-review`, CaseDetail): label the differential likelihood "assessment-time
   likelihood (after the work-up)" and state that the labelled diagnosis is not listed. R2 read an
   all-very_low differential as "no information" (S03).
4. Outside GLIO-HG (for the orchestrator):
   - VASC-DEM-S11: a field defect with no visual-pathway structure in its MRI (class C2).
   - 26 of 278 CBC or BMP sets in other conditions have MCHC or anion gap out of range (for
     example SYNC-CARD-P01 MCHC 30.6, SYNC-CARD-M01 anion gap 18): `labs_chk.py ""`.

## 5. Open questions

None for Andrea. What re-review should check:
- R2 may still want the PCNSL likelihood raised (D7 declines it with ruling 7).
- R2 may want the operative report itself to state the aspirin interval (D5 keeps it in the musts,
  per ruling 4).

<!-- PLAN COMPLETE -->
