# GLIO-HG: decisions, November 2026 round (17 Nov 2026)

Ten notes, all from R2 (NB-87MF-FBTV-TPWE), in five cases (S02 to S06). R2 annotated a build from
before October (S02 still showed Hb 15.8 / Hct 40.9, as at d1246ff3), so several notes are already
resolved. No GLIO-HG case is approved. Every class below was measured with
`work/scratch/glio-lead/measure.py` (`measure.json`, `table1.py`, `labs_chk.py`) over all 30 cases.
At the start, perfect_agent.py passes 30/30.

Sources verified on 17 Nov 2026:
- [ESC_NCS_2022] Halvorsen S et al. 2022 ESC Guidelines on cardiovascular assessment and management
  of patients undergoing non-cardiac surgery. Eur Heart J 2022;43:3826-3924. It recommends stopping
  aspirin for at least 7 days before surgery with a high bleeding risk, and its examples are
  intracranial and spinal neurosurgery (Class I, Level C; ACC key-points summary, Sep 2022). It also
  says aspirin is discontinued when the bleeding risk outweighs the cardiovascular benefit. The key
  is already on the pack allow-list.
- [Frontera_2016] Frontera JA, Lewin JJ 3rd, Rabinstein AA, et al. Guideline for reversal of
  antithrombotics in intracranial hemorrhage. Neurocrit Care 2016;24:6-46. It suggests platelet
  transfusion for aspirin- or ADP-inhibitor-associated intracranial haemorrhage that will undergo a
  neurosurgical procedure (conditional, moderate), recommends platelet function testing before
  transfusion where possible, and suggests against platelet transfusion for NSAID-related
  haemorrhage. The key is new (CENTRAL 1).
- [Perry_2017] Perry JR et al. N Engl J Med 2017;376:1027-1037. The trial enrolled patients aged 65
  or over. It compared 40 Gy in 15 fractions with and without temozolomide. Overall survival improved
  with temozolomide, and the gain was largest when MGMT was methylated. Already on the allow-list.
- [EANO_2021] Weller M et al. Nat Rev Clin Oncol 2021;18:170-186. For glioblastoma at age 70 or
  under with KPS 70 or more, the standard is 60 Gy in 30 fractions with temozolomide; above 70,
  treatment is hypofractionated. This is the October rule; it is unchanged.

## D1. MRI header "contrast used: none" (4022233f S03, 365d96f2 S04, c011f7ee S05, f987e3d1 S06)
Decision: ALREADY-FIXED by class MRI-CONTRAST (commit 71517e55; plan MRI-CONTRAST-decisions.md).
Measured in all 30 cases:
- every initial MRI is the plain study (`contrast_used: false`) and carries no gadolinium content;
- every case has a gadolinium follow-up (`contrast_used: true`, trigger `request_contrast_mri`);
  in RM02 it is FU1, after the spine study;
- every `action-1` criterion orders `contrast: true, protocol: tumor`, so the hard
  MRI-before-tissue constraint is met by the gadolinium study;
- the S05 and S06 red herrings, which cite contrast MRI, now agree with what the criterion
  receives.
No case change.

## D2. Field defect not localised by the MRI (36546be3 S02, hemianopia part)
Rule: when the examination records a homonymous field defect, the structural MRI names the
responsible segment of the retrochiasmal pathway, in its findings and in its impression. This
applies to both the plain study and the gadolinium study, and the MRI must agree with the DTI and
the perimetry reports.

Measured: 10 of the 30 cases have a field defect. P04, S02 and S04 have an MRI that names no
visual-pathway structure. In S02 and S04 only the DTI names the optic radiation, and in P04 only
the DTI and the perimetry do. The other 7 cases already name it. Across all 600 cases the defect
also occurs in VASC-DEM-S11 (not in this condition; reported to the orchestrator).

R2 offered two fixes: (A) the MRI describes posterior extension into the optic radiation, or
(B) the deficits are removed. Decision: option A. Reasons:
- The deficit is real in each case: confrontation and the stored perimetry agree, the S04 HPI has
  three days of left-sided visual blurring, and the S06-style field complaint is part of the
  scenario.
- The DTI already places the tract inside the oedema.
- Vasogenic oedema of the sagittal stratum is a sufficient cause.

Canonical text (both MRI studies; the `FLAIR` signal of the oedema finding, and impression item 2):
- S02: "... into the right temporal lobe, including the temporal stem and the sagittal stratum
  (optic radiation), and the right corona radiata ...". The DTI optic-radiation row becomes
  "Meyer loop and sagittal stratum fibers traverse the temporal and parietal FLAIR abnormality
  with reduced FA (0.38 versus 0.52 on the left); fibers continuous, displaced inferiorly; no tumor
  enhancement within the sagittal stratum". Rewrite DTI impression 2 and the `action-dti`
  expected evidence to match ("... continuous through the edematous temporal stem and sagittal
  stratum").
- S04: "... throughout the right frontal and parietal white matter, including the right sagittal
  stratum (optic radiation)". Add the same clause to impression 2.
- P04: "... involving right temporal-parietal white matter, including the superior fibers of the
  right optic radiation, ...". Add the same clause to the impression.

## D3. S02 paraphasias against left-lateralised language (36546be3, language part)
Decision: ALREADY-FIXED in October. `mental_status` now reads "Speech is fluent and grammatical
with no paraphasic errors; responses are slowed, with long pauses before answering". This is the
attentional and executive slowing that option A asks for, and the HPI describes pauses and loss of
the train of thought, not paraphasias.

## D4. S02 CBC, assay list, performance status (b63e4af9)
Decision: ALREADY-FIXED in October, all three parts. Each part was measured as a class:
- CBC: Hb 14.1, Hct 43.2 and RBC 4.65 now give MCHC 32.6. MCHC and the anion gap are in range in
  all 30 GLIO-HG CBC sets. Across all 600 cases, 26 of 278 sets are out of range, none of them in
  GLIO-HG; reported to the orchestrator.
- Assay list: the tissue label now names IDH1 R132H IHC, ATRX IHC and MGMT, and these equal the
  `molecular_assays` of both alternatives. The report has a row for each. No GLIO-HG tissue
  criterion names a marker its arguments lack (the two apparent hits, RS01 and RS03, are "H3 G34",
  which is in their lists). EANO 2021 does not require TERT, EGFR or +7/-10 when the histology
  already shows microvascular proliferation and necrosis, so they stay out of the minimum list
  (October C4).
- Performance status: `action-performance-status` is required in all 30 cases and is in the stop
  rule (October Q3). S02 has KPS 70, so the Stupp must applies.

## D5. Antiplatelet exposure before neurosurgery (f465277d S04; class ANTIPLATELET-TIMING)
Measured:
- Nine cases take aspirin and have a required neurosurgical tissue procedure. All are in GLIO-HG;
  no other condition has this combination.
- Four of them already state an interval of about 7 days: RM04, RP01, RP04 and RS05.
- Five have no interval: P03, RM01, S02, S04 and S05. In S04 the SWI shows intratumoral
  haemorrhage and the patient also takes over-the-counter ibuprofen.
- In the ibuprofen-only cases (M01, M02, M03, M04, P01, RS02, S01) ibuprofen is stopped now. That
  is correct, because the NSAID effect is reversible and no guideline sets a longer interval.
- P05 used over-the-counter ibuprofen (HPI) and has no NSAID must before her thalamic biopsy. She
  gets the ibuprofen-only stop must, as in the other ibuprofen cases.

R2 offered (A) a step that handles the antiplatelet agent before resection, or (B) a statement in
the operative entry explaining why surgery proceeded. Decision: option A, written as a must.
Reasons:
- Handling the drug is management, and treatment is never a tool (ruling 4).
- The tool vocabulary has no platelet-function assay (CENTRAL 2).
- A resection report that states "aspirin stopped 8 days before" would report management the agent
  has not yet recommended (ruling 4). So the operative entries stay as they are.

Canonical must, variant A (no impending herniation and no 24-hour aspiration window; RM01, S04,
S05):
> Stop <the primary-prevention aspirin | the aspirin started for presumed TIA><, and the
> over-the-counter ibuprofen,> now, and schedule the <craniotomy | stereotactic biopsy> at least
> 7 days after the last aspirin dose, because intracranial neurosurgery carries a high bleeding risk
> (ESC 2022); if neurological deterioration forces earlier surgery, operate with platelet function
> testing where available and platelet transfusion ready (Frontera 2016).

Canonical must, variant B (urgent surgery that cannot wait 7 days: S02, early uncal herniation;
P03, aspiration within about 24 hours under ESCMID 2024):
> Stop the primary-prevention aspirin<, and the as-needed ibuprofen,> now, but do not delay the
> urgent <resection | aspiration and biopsy> for a 7-day aspirin washout <because of the early
> uncal herniation | because the aspirate should be obtained within about 24 hours>; operate with
> platelet function testing where available and platelet transfusion ready (ESC 2022; Frontera 2016).

How the musts are changed:
- The new must replaces the case's existing aspirin must. Where the old must also gives the
  dexamethasone and GI-bleeding reason, keep that clause (S02, S04: "and avoid them while on
  dexamethasone").
- RM04, RP01, RP04 and RS05 already follow ESC 2022 and are not churned (NO-ACTION).
- P05 gets: "Avoid ibuprofen and other NSAIDs before the stereotactic biopsy and while on
  dexamethasone; use paracetamol for headache."

## D6. S05 "subcortical mapping" with no mapping study; constraints (1e375c3a)
Measured:
- S05 stores an fMRI follow-up (FU18, `functional_MRI`). It reports the right-hand motor area about
  9 mm from the enhancing margin, with reduced activation, and left language dominance remote from
  the mass. No criterion and no constraint uses it.
- The exam has right-sided weakness.
- The three sequence constraints carry valid criterion ids. The "empty tool fields" R2 saw came
  from a stale review-app build.

Decision: option A, because it is clinically better. October rule C6 asks for fMRI when motor
cortex lies within about 1 cm of the margin, and the hand area here is 9 mm away in a hemiparetic
patient. Changes:
- Add the recommended criterion `action-fmri-functional-mapping` (`order_advanced_imaging`,
  `{"modality": "functional_MRI"}`), placed before `action-dti-tractography`.
- Move the fMRI follow-up to just before the DTI follow-up.
- Add a soft constraint fMRI -> tissue: "Motor mapping plans the resection margin" [EANO_2021].
- The surgery must names "preoperative functional MRI and DTI tractography and intraoperative
  subcortical mapping".
- The operative `site` ("with subcortical mapping") stays. Subcortical mapping is intraoperative
  stimulation, it agrees with the must, and the preoperative studies now exist.

Criterion text:
- Label: "Order functional MRI (motor and language mapping) before resection of the left parietal
  tumor near the hand motor area".
- Rationale: "The hand motor area lies within about 1 cm of the enhancing margin in a patient with
  right-sided weakness; motor mapping defines the resection margin (EANO 2021)."
- Expected evidence: "Right-hand motor area in the left precentral gyrus displaced anteriorly about
  9 mm from the enhancing margin; left language dominance, remote from the mass".

Only S05 has an unscored fMRI that meets rule C6. The DTI follow-ups in P01 to P05, RM01, RP01, RP03
and RP04 are unscored on purpose: they are case-specific answers to off-pathway orders
(commit 4221abb6) in group B and C cases, where rule C6 does not apply. NO-ACTION.

## D7. Differential likelihoods and callosal involvement (35803946 S03, differential part)
R2 asks to lift primary CNS lymphoma above very_low because the tumour reaches the corpus callosum.
Decision: partly applied.
- Applied: the PCNSL `key_features` name the callosal extension as the feature that keeps lymphoma
  in the pre-biopsy differential, and say what excludes it.
- DECLINED: lifting the likelihood. Reasons:
  - Ruling 7 (October, in force) defines likelihood as the assessment-time view, after the
    results the pathway returns. In S03 the tissue shows a glial neoplasm (glioblastoma,
    IDH-wildtype), which excludes lymphoma.
  - Even before tissue, thick irregular ring enhancement with central necrosis and rim-only
    restriction in an immunocompetent patient is atypical of PCNSL. PCNSL typically shows
    homogeneous enhancement and diffuse restriction (EANO_PCNSL_2015), and callosal spread is
    equally typical of glioblastoma.
- R2's point that an all-very_low list "carries no information" is a display question. The review
  app does not say that the field is the post-work-up likelihood of the alternatives, nor that the
  labelled diagnosis is not listed (CENTRAL 3).

Canonical `key_features`:
- S03: "Callosal extension keeps lymphoma in the pre-biopsy differential, but he is immunocompetent
  and thick irregular ring enhancement with central necrosis and rim-only restricted diffusion are
  atypical of lymphoma; tissue shows a glial neoplasm".
- M04, the same class: "FLAIR extension along the callosal genu keeps lymphoma in the pre-biopsy
  differential, but he is immunocompetent and the partial ring with focal necrosis is atypical;
  GFAP-positive glial tissue excludes it".

Not applied elsewhere:
- RS02, S01, S05, S06: the callosal signal is vasogenic oedema.
- RS06: tracking along the tapetum.
- RP04: PCNSL already argued from imaging.
- P02: lymphoma is the answer.
All NO-ACTION.

## D8. Callosal extension in resection planning (35803946 S03, surgery part)
Rule: where the MRI describes tumour in the corpus callosum (enhancing tumour, or T2/FLAIR signal
described as infiltration rather than vasogenic oedema), the surgery must says so. Measured: S03
(enhancing mass "extending to the corpus callosum medially"), M04 (FLAIR along the genu "raises
concern for infiltration") and M05 (non-enhancing infiltrative mass with FLAIR to the posterior
body). Insert after the mapping clause of the surgery must: "recognising that the extension into
the corpus callosum limits the safe extent of resection". In S03, the resection report's extent row
becomes "Enhancing tumor resected; a thin enhancing rim left at the posterior margin facing the
precentral motor area and infiltrated tumor left at the medial callosal margin" (report content;
the MRI and DTI already show it). In M04 and M05, the worker checks that the resection report does
not claim a gross total removal of the callosal component.

## D9. S06 treatment planning at 67 with unmethylated MGMT (a1f18356, treatment part)
Measured:
- S06 is the only GLIO-HG glioblastoma aged 65 to 70 with KPS 70 or more (RM01 at 67 and RP01 at 68
  have KPS 40 and 60 and already get the hypofractionated branch).
- A treatment must exists (added in October), but it states the 70-or-under Stupp branch alone.

Decision: rewrite the must as a discussion, not a switch.
- Reasons: EANO 2021 uses 70 as the cut-off, so Stupp is guideline-concordant at 67 with KPS 80.
  Perry 2017 enrolled patients from age 65, and its benefit was largest in MGMT-methylated tumours.
  Both regimens are therefore evidence-based here, and the unmethylated MGMT promoter is what should
  be raised.
- "A treatment-planning step" is a must, not a tool (ruling 4).

Canonical must:
> After the integrated diagnosis, refer to the neuro-oncology multidisciplinary team; for
> glioblastoma, IDH-wildtype at age 67 with KPS 80 and an unmethylated MGMT promoter, discuss
> radiotherapy 60 Gy in 30 fractions with concomitant and adjuvant temozolomide (Stupp 2005; the
> EANO 2021 standard up to age 70) against hypofractionated radiotherapy 40 Gy in 15 fractions with
> temozolomide, an option from age 65 (Perry 2017), noting that the unmethylated MGMT promoter
> predicts a smaller benefit from temozolomide.

`key_clinical_evidence` item 7 changes to match: "... at 67 with KPS 80 and an unmethylated MGMT
promoter, standard chemoradiotherapy and short-course radiotherapy with temozolomide are both
options for the team".

The October cut-off at 70 for the other cases is not undone.

## D10. Ventricular entrapment with no management (a1f18356, occipital-horn part; class)
Measured: of the 30 MRIs, six describe a positive ventricular obstruction:
- P05, RM01, RM03: already have a hydrocephalus must.
- S02: early trapping of the right temporal horn; only the herniation must covers it.
- S03: early trapping of the right lateral ventricle; nothing covers it.
- S06: early obstructive dilatation of the occipital horn; covered only by the LP prohibition.

Decision: add a must to S06 and S03, using the wording already established in P05 and RM01:
> Observe neurologically for progression of the <early obstructive dilatation of the left occipital
> horn | early trapping of the right lateral ventricle> (worsening headache, vomiting, drowsiness,
> visual or pupillary change), with urgent CT if it occurs; resection of the mass relieves the
> obstruction, with neurosurgical CSF diversion if it progresses before surgery.

In S02, the monitored-bed must reads "... for the early right uncal herniation and the trapped right
temporal horn; ...", with the rest unchanged.

## D11. October decisions re-examined, none undone
- The 70-year cut-off for Stupp versus hypofractionation is kept (D9 adds the discussion only where
  the age-65 Perry population overlaps).
- The assessment-time likelihood convention (ruling 7) is kept (D7).
- Performance status stays required in all 30, and `max_additional_actions` stays 0.
- Literature criteria stay absent (class LIT): 0 literature outputs or criteria in GLIO-HG.

## NEEDS-ANDREA
None. Every decision rests on a cited guideline or on the case data.
