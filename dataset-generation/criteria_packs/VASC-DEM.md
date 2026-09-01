# Criteria pack: Vascular dementia (major vascular cognitive disorder)

**ICD-10:** F01.50 (vascular dementia, unspecified severity, without behavioural disturbance;
use F01.51 where behavioural disturbance is present), I67.3 (progressive vascular
leukoencephalopathy / Binswanger), I69.3x (sequelae of cerebral infarction) for the
post-stroke subtype
**Condition enum:** `NeurologicalCondition.VASCULAR_DEMENTIA`
**Case ID prefix:** `VASC-DEM`

---

> **Authored on the clinical tool review, July 2026.** Both reviewers asked for peripheral
> neuropathy to be dropped — "too broad a category", and Reviewer 1 filed the removal as an
> `error` reading `SOSTITUIRE PATOLOGIA` — and for vascular dementia to take its place, so that
> the four major dementias (AD, FTD, DLB, VaD) are all represented and the benchmark can score
> the differential *among* them rather than each in isolation. That differential is the axis
> this pack is built around: every case must make the vascular attribution explicit, and three
> of the nine puzzle cases resolve to mixed Alzheimer-and-vascular pathology, which is a
> diagnosis in its own right and not a tie-break.

## 1. Diagnostic criteria

Major vascular cognitive disorder requires **both** a cognitive syndrome and evidence that
cerebrovascular disease accounts for it.

**Cognitive syndrome** — decline from a previous level in ≥1 domain, documented on a validated
instrument, severe enough to compromise independence in instrumental activities. The
characteristic profile is **executive/processing-speed predominant**: slowed set-shifting,
impaired working memory and reduced verbal fluency, with recognition memory and cued recall
relatively preserved. That asymmetry against the amnestic profile of Alzheimer's disease is
the clinical discriminator [VASCOG_2014] [DSM5].

**Vascular attribution** — one of:
- a **temporal relationship**: onset of the deficit within 3 months of a documented stroke, or
  an abrupt/stepwise course with each step dated to a cerebrovascular event
  [NINDS_AIREN_1993];
- a **lesion pattern sufficient to explain the deficit** even without a clinical stroke
  history: multiple large-vessel infarcts; a single infarct in a strategic site (anterior or
  paramedian thalamus, genu of the internal capsule, caudate, angular gyrus, basal forebrain);
  extensive confluent white matter hyperintensity (Fazekas 3) with multiple lacunes; or
  extensive haemorrhagic lesions [VASCOG_2014] [AHA_ASA_2011_VCI].

**Imaging is where the attribution is made, and it must be reported in STRIVE-2 terms**: white
matter hyperintensity of presumed vascular origin with a Fazekas grade, recent small
subcortical infarcts, lacunes (counted and located), cerebral microbleeds with their
distribution (deep = hypertensive arteriopathy; strictly lobar = amyloid angiopathy), enlarged
perivascular spaces, cortical superficial siderosis, and the atrophy pattern [STRIVE_2].
Where the microbleeds are strictly lobar and accompanied by cortical superficial siderosis,
apply the **Boston criteria v2.0** for cerebral amyloid angiopathy — a vascular cause, but one
that changes management in the opposite direction from an embolic one [Boston_v2].

**The diagnosis is excluded** when the deficit is fully explained by another disorder, and it
is **not** excluded by coexisting Alzheimer pathology: where both are present the diagnosis is
mixed disease.

## 2. Standard workup hierarchy

These tiers are defaults. Two things move per case, both stated in the case's own
`action_criteria`: the **embolic workup** (ECG, monitoring, echocardiography, carotid duplex)
is required only where the lesion pattern is embolic, because that is where an occult source
converts management from risk-factor control to anticoagulation; and **CSF or amyloid
biomarkers** are required only where mixed Alzheimer pathology is the question being asked.

**Required (REQUIRED tier — must be called):**
- `perform_clinical_assessment` (`assessment_type: cognitive_screen`) — the diagnosis begins
  with a documented deficit on a validated instrument, not with imaging. Report the total, the
  per-domain breakdown, and whether delayed recall improves with cueing: the
  executive-predominant profile with cue-responsive recall is the discriminator against AD.
  In the subcortical subtype add `gait_and_balance_timed`, where a short-stepped wide-based
  gait with preserved arm swing is part of the syndrome and separates it from the gait of NPH
  and of parkinsonian disorders [VASCOG_2014] [AAN_MCI_2018]
- `analyze_brain_mri` (`protocol: dementia`, or `stroke` where an acute event is being dated)
  — the vascular attribution *is* the imaging. Must include FLAIR (WMH, Fazekas), T2/T1
  (lacunes, cavitation), DWI (to establish that lesions are chronic) and **SWI or GRE**, without
  which microbleeds and cortical superficial siderosis are invisible and amyloid angiopathy
  cannot be recognised. Report the medial temporal atrophy grade alongside the vascular burden
  — the two together are what distinguish pure vascular from mixed disease [STRIVE_2]
  [VASCOG_2014]
- `interpret_labs` — two jobs, both mandatory, and the panel is named rather than generic.
  Exclusion of reversible cognitive impairment: `TSH`, `B12`, `folate`, `RPR`, `HIV`, `CBC`,
  `CMP`. Characterisation of the vascular substrate that will be treated: `HbA1c`,
  `lipid_panel`. Add `homocysteine` only where a young or otherwise unexplained small-vessel
  burden is present; add `ESR`/`CRP` only where vasculitis is genuinely on the differential
  [AAN_MCI_2018] [AHA_ASA_2011_VCI]

**Recommended (RECOMMENDED tier — expected workup hygiene):**
- `order_specialized_test` (`test_type: neuropsych_battery`) — formal multi-domain testing
  where the screen is borderline (MoCA 23-26) or where the profile must be documented for
  follow-up; it is the instrument that settles an executive-versus-amnestic attribution the
  screen cannot [VASCOG_2014]
- `order_advanced_imaging` (`modality: carotid_duplex`) — where cortical or cortico-subcortical
  infarcts are present, to identify extracranial large-artery stenosis as the mechanism
  [AHA_ASA_2021_secondary]
- `analyze_ecg` — for atrial fibrillation as the embolic source in a multi-territory infarct
  pattern, and for the left ventricular hypertrophy of chronic hypertension. Recommended in
  the embolic subtypes, **not** part of the workup of pure subcortical small-vessel disease
  [AHA_ASA_2021_secondary]
- `search_medical_literature` — confirm the diagnostic criteria applied and current
  secondary-prevention targets
- `check_drug_interactions` — anticholinergic burden is a reversible contributor to cognitive
  impairment in this population, and antiplatelet/anticoagulant selection interacts with the
  microbleed burden

**Optional (OPTIONAL tier — defensible if performed):**
- `order_advanced_imaging` (`modality: MR_angiography`) — intracranial large-artery stenosis or
  dissection where the infarct pattern suggests it [AHA_ASA_2021_secondary]
- `order_advanced_imaging` (`modality: FDG_PET`) — where the AD-versus-vascular attribution is
  unresolved after MRI and testing: a temporoparietal pattern supports AD, patchy multifocal
  hypometabolism following the white matter lesions supports vascular disease [VASCOG_2014]
- `order_advanced_imaging` (`modality: amyloid_PET`) — where mixed pathology is the specific
  question and CSF is declined or unavailable
- `analyze_csf` (`special_tests: Abeta42, Abeta42_40_ratio, phospho_tau`) — same question as
  amyloid PET, cheaper, and adds cell count and protein where inflammatory small-vessel disease
  is being excluded
- `order_cardiac_monitoring` — prolonged ambulatory monitoring for paroxysmal atrial
  fibrillation after multi-territory infarcts with a negative ECG [AHA_ASA_2021_secondary]
- `order_echocardiogram` (`echo_type: TTE`) — a cardioembolic source in the multi-infarct
  subtype
- `order_specialized_test` (`test_type: genetic_panel:CADASIL`) — NOTCH3 sequencing where onset
  is under 60 with migraine with aura, a family history of stroke or early dementia, and
  anterior temporal pole or external capsule white matter involvement
- `order_ct_scan` — **only** where MRI is contraindicated (pacemaker, severe claustrophobia).
  A CT can show old infarcts and gross white matter change but cannot show microbleeds or
  siderosis, so it cannot exclude amyloid angiopathy; a case that resorts to CT must say so
  [STRIVE_2]

## 3. Tools that are typically USELESS for this condition

- `analyze_eeg` — no diagnostic role in vascular dementia. It belongs on the differential of a
  rapidly progressive or fluctuating course (CJD, non-convulsive status, toxic-metabolic
  encephalopathy); outside that indication it is cost without yield [VASCOG_2014]
- `order_advanced_imaging` (`modality: DaTscan`) — a presynaptic dopaminergic study answers the
  DLB/parkinsonism question, not the vascular one; useless unless spontaneous parkinsonism or
  fluctuating cognition with hallucinations is present
- `order_advanced_imaging` (`modality: MIBG_scan`) — cardiac sympathetic imaging is a DLB test
- `order_advanced_imaging` (`modality: tau_PET`) — research use; does not change management here
- `order_advanced_imaging` (`modality: MR_spectroscopy`, `perfusion_MRI`, `CT_perfusion`) —
  tumour, metabolic and acute-reperfusion tools; no role in the diagnosis of an established
  chronic vascular cognitive disorder
- `order_body_imaging`, `order_microbiology`, `obtain_tissue_diagnosis` — no specimen and no
  extracranial imaging is part of this workup; a brain biopsy is reserved for suspected CNS
  vasculitis or amyloid-beta-related angiitis, neither of which is this condition
- `order_specialized_test` (`test_type: emg_ncs`, `polysomnography`, `tilt_table`) — peripheral
  nerve, sleep and autonomic studies answer other questions. Polysomnography is defensible only
  where REM sleep behaviour disorder is reported, i.e. where DLB is the real question
- `interpret_labs` (`panels: paraneoplastic_panel`, `autoimmune_encephalitis_panel`) — an
  untargeted autoimmune or paraneoplastic battery in a chronic stepwise decline with a
  hypertensive imaging burden is the archetypal expensive miss [AAN_MCI_2018]

## 4. Tools that are HARMFUL / contraindicated

- `analyze_csf` where the presentation includes an acute lobar haemorrhage or where imaging
  shows significant mass effect — the LP adds risk without changing the diagnosis
- No other member of the tool set carries a safety concern here; the harm in this condition is
  therapeutic rather than diagnostic (anticoagulating a patient whose lobar microbleeds and
  siderosis indicate amyloid angiopathy), and that belongs in
  `assessment.prohibited_recommendations` [Boston_v2]

## 5. Sequence constraints

- `perform_clinical_assessment` → `analyze_brain_mri` (`soft`): the deficit is documented before
  it is attributed; imaging read without a cognitive profile invites over-attribution of
  incidental white matter change [VASCOG_2014]
- `analyze_brain_mri` → `analyze_csf` (`soft`): exclude mass effect and lobar haemorrhage before
  an LP
- `analyze_ecg` → `order_cardiac_monitoring` (`soft`): prolonged monitoring is for the patient
  whose surface ECG did not already show the arrhythmia [AHA_ASA_2021_secondary]

## 6. Subtype variations (S/M/P)

Subtype here means the **vascular mechanism**, which is what makes this condition scoreable
where "peripheral neuropathy" was not. Each case names its mechanism, and the mechanism
determines which optional tools become required.

- **Subcortical ischaemic (small-vessel) vascular dementia** — confluent WMH plus multiple
  lacunes, hypertension and diabetes, insidious-to-stepwise course, gait involvement early.
  Embolic workup NOT required; `gait_and_balance_timed` is.
- **Multi-infarct dementia** — chronic infarcts in more than one arterial territory. ECG
  required; carotid duplex required; monitoring or echocardiography required where the ECG is
  in sinus rhythm and the source is still unexplained.
- **Strategic single-infarct dementia** — one infarct in the anterior/paramedian thalamus, genu
  of the internal capsule, caudate or angular gyrus, with a deficit disproportionate to lesion
  volume. The reasoning point is anatomical, not quantitative.
- **Post-stroke dementia** — deficit dated to within 3 months of a documented stroke; the
  NINDS-AIREN temporal criterion is the discriminator [NINDS_AIREN_1993].
- **Mixed Alzheimer and vascular** — both burdens present. CSF biomarkers or amyloid PET
  required, because the answer is *both* and an agent that commits to one is wrong.
- **Cerebral amyloid angiopathy** — strictly lobar microbleeds with cortical superficial
  siderosis; SWI is mandatory and anticoagulation is contraindicated [Boston_v2].
- **Hereditary small-vessel disease (CADASIL)** — under 60, migraine with aura, family history,
  anterior temporal pole involvement; `genetic_panel:CADASIL` required in that case.

Difficulty maps onto these: **S** = one unambiguous mechanism; **M** = two plausible
attributions (usually vascular vs degenerative) resolvable with the standard workup;
**P** = the attribution requires a biomarker, a genetic test, or the recognition of an
amyloid-angiopathy pattern that inverts management.

**Two cases in the set are deliberately not straightforward vascular dementia, and that is the
point of them.** `VASC-DEM-M01` has a Fazekas 2 burden with an executive profile but has *not*
lost instrumental independence: its ground-truth diagnosis is **mild** vascular cognitive
impairment (F06.7), because the mild/major threshold is functional and calling it a dementia
would be wrong. `VASC-DEM-P08` cannot have an MRI — a non-MR-conditional pacemaker — so its
diagnosis is reached on CT, duplex and pacemaker interrogation, and its ground truth requires
the agent to state what CT cannot exclude. Both are scored on getting the qualification right,
not the label.

## 7. Common red-herring categories

- **Incidental white matter change** — Fazekas 1-2 hyperintensity is common in treated
  hypertensives and does not by itself explain a dementia; over-attribution is the commonest
  error this condition tests.
- **Low B12 in an elderly patient** — a contributor worth correcting, not the explanation, and
  it does not exclude a vascular cause.
- **A remembered "small stroke"** — an undocumented event years earlier does not satisfy the
  temporal criterion; the criterion asks for a documented one.
- **Hippocampal atrophy alongside vascular burden** — points to mixed disease, not to
  Alzheimer's disease instead of vascular.
- **Atrial fibrillation as an incidental finding** — present in a patient whose imaging shows
  pure small-vessel disease with no infarcts; it changes stroke prevention but it is not the
  mechanism of this dementia.
- **Apathy read as depression** — the frontal-subcortical apathy of small-vessel disease is
  routinely mistaken for a mood disorder, and an antidepressant trial delays the diagnosis.
- **A normal MoCA** — insufficiently sensitive to executive impairment in a high-baseline
  patient; the functional history outweighs it.

## 8. Allowed citations

- `[VASCOG_2014]` — Sachdev P, Kalaria R, O'Brien J, et al. Diagnostic criteria for vascular
  cognitive disorders: a VASCOG statement. Alzheimer Dis Assoc Disord 2014;28:206-218
- `[NINDS_AIREN_1993]` — Román GC, Tatemichi TK, Erkinjuntti T, et al. Vascular dementia:
  diagnostic criteria for research studies. Report of the NINDS-AIREN International Workshop.
  Neurology 1993;43:250-260
- `[AHA_ASA_2011_VCI]` — Gorelick PB, Scuteri A, Black SE, et al. Vascular contributions to
  cognitive impairment and dementia: a statement for healthcare professionals from the AHA/ASA.
  Stroke 2011;42:2672-2713
- `[STRIVE_2]` — Duering M, Biessels GJ, Brodtmann A, et al. Neuroimaging standards for research
  into small vessel disease — advances since 2013 (STRIVE-2). Lancet Neurol 2023;22:602-618
- `[Boston_v2]` — Charidimou A, Boulouis G, Frosch MP, et al. The Boston criteria version 2.0
  for cerebral amyloid angiopathy. Lancet Neurol 2022;21:714-725
- `[AAN_MCI_2018]` — Petersen RC, Lopez O, Armstrong MJ, et al. Practice guideline update
  summary: Mild cognitive impairment. Neurology 2018;90:126-135
- `[AHA_ASA_2021_secondary]` — Kleindorfer DO, Towfighi A, Chaturvedi S, et al. 2021 Guideline
  for the Prevention of Stroke in Patients With Stroke and Transient Ischemic Attack. Stroke
  2021;52:e364-e467
- `[ESO_2021_SVD]` — Wardlaw JM, Debette S, Jokinen H, et al. ESO Guideline on covert cerebral
  small vessel disease. Eur Stroke J 2021;6:CXI-CLXII
- `[DSM5]` — American Psychiatric Association. Diagnostic and Statistical Manual of Mental
  Disorders, 5th ed. Major vascular neurocognitive disorder. 2013
