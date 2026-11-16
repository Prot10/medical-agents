# MS-RR: November 2026 decisions (lead, 16 Nov 2026)

118 notes, all from R1 (NB-KSC3-TWUA-QDTM), none from R2, in all 30 cases. No MS-RR case is in
`work/approved.txt`. Each entry below gives the notes, the decision, the reason and the citation.
"Measured" counts come from scripts in `work/scratch/msrr-lead/` (`measure.py`, `dmt.py`, `xcond.py`)
run on the working tree of 16 Nov 2026 (after commits 393c547e LIT and 71517e55 MRI-CONTRAST).

Sources verified this session (web search, 16 Nov 2026):
- [McDonald_2024] Montalban X et al. Lancet Neurol 2025;24(10):850-865, doi 10.1016/S1474-4422(25)00270-4.
  Secondary sources checked for the rule in D3: Practical Neurology news item on the publication;
  the 2026 *Brain* review "Progress divides the room" (flow chart: "After a typical attack, the
  criteria are met with four or more involved regions. With two or three regions, they are met with
  DIT, CVS or CSF"; in RIS "four or more regions alone are not sufficient"); a review key-points box
  ("In a typical presentation, lesions in at least four of five ..."). Adult MOG-IgG testing:
  "should be considered ... in older children or adults with clinical and/or MRI features
  suggestive of MOGAD" (Cohen JA, Mult Scler 2025, doi 10.1177/13524585251351860, and the Neurology
  "Application of the 2024 McDonald Criteria" table).
- [NICE_NG220] section "Relapse and exacerbation": rule out infection, particularly urinary tract and
  respiratory infection, before diagnosing a relapse; assess and offer treatment for relapses that
  affect usual tasks "as early as possible and within 14 days of onset of symptoms"; not all relapses
  need steroids; offer oral methylprednisolone 0.5 g daily for 5 days; consider IV 1 g daily for 3-5
  days when oral has failed or is not tolerated, or for admission with a severe relapse or for
  monitoring of conditions such as diabetes. (NICE NG220 PDF, nice.org.uk; QS108 statement 5.)
- Product labels: OCREVUS (ocrelizumab) US prescribing information: perform HBV screening before
  initiation; live or live-attenuated vaccines at least 4 weeks and non-live vaccines at least 2
  weeks before initiation (quantitative serum immunoglobulin screening before the first dose is
  stated by the label summary on drugs.com). TECFIDERA (dimethyl fumarate) US PI section 2.2: CBC
  including lymphocyte count before initiation; aminotransferases, alkaline phosphatase and total
  bilirubin before initiation. ZEPOSIA (ozanimod) US PI: ECG, CBC with lymphocytes, liver tests,
  VZV antibodies when there is no confirmed varicella history or vaccination (vaccinate and wait 4
  weeks), fundus examination; EU SmPC: first-dose 6-hour monitoring only in patients with certain
  pre-existing cardiac conditions. Fingolimod US PI: 6-hour first-dose monitoring in all patients,
  ECG before dosing and at the end of observation. Ponesimod US PI: "First Dose Monitoring in
  Patients with Certain Preexisting Cardiac Conditions".
- [Fowler_2009] Fowler CJ, Panicker JN, Drake M, et al. A UK consensus on the management of the
  bladder in multiple sclerosis. J Neurol Neurosurg Psychiatry 2009;80(5):470-477, doi
  10.1136/jnnp.2008.159178 (test for UTI, ISC if post-void residual over 100 mL, then
  antimuscarinic); updated UK expert consensus Br J Nurs 2022;31(Sup3):S1, same algorithm; a 2024
  review (PMC11528427) advises weighing bladder capacity, flow and symptoms rather than the 100 mL
  cut-off alone.
- [EHA_ESMO_PCNSL_2024] Ferreri AJM, Illerhaus G, Doorduijn JK, et al. Primary central nervous
  system lymphomas: EHA-ESMO Clinical Practice Guideline. Ann Oncol 2024;35(6):491-507, doi
  10.1016/j.annonc.2023.11.010: "Corticosteroid therapy before tissue biopsy should be avoided
  whenever clinically possible [IV, D]. In case of clinical deterioration, urgent biopsy should be
  carried out before the start of corticosteroids [IV, A]." EANO 2015 (Hoang-Xuan K et al., Lancet
  Oncol 2015): "If clinically possible, steroids should be avoided before [biopsy] (good practice
  point)."
- [Allen_2012] Allen LM, Hasso AN, Handwerker J, Farid H. Sequence-specific MR imaging findings that
  are useful in dating ischemic stroke. RadioGraphics 2012;32(5):1285-1297, doi 10.1148/rg.325115760
  (MRI signal of an infarct evolves with time; DWI can be falsely negative in posterior circulation
  stroke). Cited for "normal ADC at one week and enhancement do not by themselves exclude a subacute
  infarct", not for exact day counts.
- [AHA_2021_SecPrev] Kleindorfer DO, Towfighi A, Chaturvedi S, et al. 2021 Guideline for the
  prevention of stroke in patients with stroke and transient ischemic attack. Stroke
  2021;52:e364-e467 (vascular imaging of the head and neck after a suspected ischaemic event).
  Well-known reference; not re-opened this session.

---

1. **LIT, 31 notes** (one per case on the stored literature follow-up, plus RP02 26f64ab1 on the
   literature criterion; RS05 "np" read as "no"). Decision: FIXED by class LIT, commit 393c547e.
   Measured: 0 literature criteria, 0 literature follow-ups, 0 non-null initial or fallback literature
   outputs in all 30 cases. Nothing to do; do not add any back. Citation: ROUND_POLICY ruling 5,
   NOVEMBER_ADDENDUM class 1.

2. **MRI-CONTRAST, 30 notes** (one per case on `initial_tool_outputs.mri`). Decision: FIXED by class
   MRI-CONTRAST (commit 71517e55, `plans/MRI-CONTRAST-decisions.md`). Measured: all 30 initial MRIs
   are now `contrast_used: false` with no gadolinium text, every case has an `analyze_brain_mri`
   follow-up `request_contrast_mri` with `contrast_used: true`, and every MRI criterion orders
   `{contrast: true, protocol: ms}`; `mri_probe_all.txt` lists all 30. Workers re-run `mri_probe.py`
   only if they touch an MRI.

3. **Four regions without DIT applies to a typical presentation only** (P03 62865b19; class covers
   the puzzle cases P01, P02, P03). Decision: FIXED. The 2024 criteria let lesions in 4-5 regions
   suffice after a typical attack; in RIS and non-specific presentations DIS must be completed by
   DIT, positive CSF or CVS. P01, P02 and P03 present with vertigo, fatigue and transient
   paraesthesias or clumsiness (non-specific), so their KCE lines "with four regions DIT is not
   required" and P03's must "4 of 5, so DIT is not required" are wrong for them. Each has DIT on the
   MRI (simultaneous enhancing and non-enhancing lesions), so the diagnosis stands. This revises
   October decision C1 and pack section 1.3, which gave the 4-5 region rule without the "typical
   presentation" condition: the guideline says otherwise, the physician is right. The other 27 cases
   present with a typical attack (optic neuritis, partial myelitis, brainstem or cerebellar syndrome,
   tumefactive attack) and keep the 4-5 region wording. Citation [McDonald_2024].

4. **Uncertain earlier episodes are not proven attacks** (M04 b0c42fef, P01 8396c5dc, P02 4fc5612f,
   RS04 c2cb2aec). Decision: FIXED, as a class. An earlier episode is written as an "earlier attack"
   only when it had objective findings at the time or leaves a residual sign on today's exam
   attributable to it (RAPD or pallor after optic neuritis, residual Babinski, paraparesis, sensory
   level). A purely subjective episode, or one attributed to another cause without objective
   corroboration, is a "possible earlier attack", and no must, prohibition or KCE line counts it in
   an attack total ("three attacks in 8 months"). Musts that state disease activity list the current
   attack, possible earlier episodes as such, and MRI activity. The formulation must asks for "MS by
   the 2024 McDonald criteria"; a relapsing-remitting course may be named but is not demanded where
   the attack history is uncertain (P01's request; the scorer already accepts "multiple sclerosis"
   and "MS", so no synonym change). Measured instances: M01 (must "three attacks in 14 months" counts
   the 14-month hand tingling attributed to carpal tunnel), M03 (KCE "Prior attack" for an untested
   hand episode), M04 (must[1], must[3], KCE[1]), P01 (KCE[0] "Attacks:", must "recurrent attacks"),
   P02 (KCE[0], must[2]), RS04 (must[2]), RM01 and RM02 (KCE[0] "earlier attack" for a subjective
   episode). Workers check every other count with the rule (RS02, RS03, RS05, RS06, S01-S06 cite
   residual signs and stay unless the residual is absent). Citation [McDonald_2024] (MS rests on
   DIS and DIT; past events need objective corroboration to be counted, as in Thompson 2018).

5. **Pre-DMT screening is drug-specific** (24 notes: M01 9aac7870, M02 f67f4b40, M03 93f50957, M04
   4fd4a20e, P01 08a37986, P02 b3e864f0, RM03 d5d8ad08, RM04 7667e073, RP01 af8dc3ff, RP02 c1fa2929,
   RP03 5303a100, RP04 9b069b39, RP05 99088fd7, RS01 57aa1800, RS02 5d08d9ce, RS03 3a28a3e0, RS04
   d196fb36, RS05 8d8410b0, RS06 43400e82, S01 09a248b7, S02 3d927c95, S03 e5700afc, S04 1d31027a,
   S05 f3f11452, S06 b2ed8a7b). Decision: FIXED in all 30 (measured: 30 of 30 have the universal
   HBsAg/anti-HBc/HCV/VZV must; P03 and P05 have no note but the same defect). One must, built from
   the canonical text in plan section 2 C5: the checks the case's favoured drug requires (from its
   own DMT must or drug-check output), and "or the checks the chosen alternative requires". HCV is
   not kept as a universal item. Also fix the drug-check outputs that state the universal list as a
   rule (P03, P04, P05 measured). Citation: product labels above; [NICE_NG220] (DMT through the MS
   team).

6. **Urinary infection before steroids: assess, do not wait for a culture** (P04 bc2383f3, P05
   222ff635, RM04 42b55638, RP05 ae3e77f6, RS02 55123805, RS03 414f3aaa, S03 b2269e22, S04 2f73da0e,
   and M01 8d31a900 for its infection clause). Decision: FIXED in the 13 measured cases with a
   steroid must gated on urine tests (M01, M02, M03, P04, P05, RM04, RP05, RS02, RS03, S02, S03, S04,
   S06). NICE says rule out infection before diagnosing a relapse; it does not require a negative
   culture before treatment, and a negative dipstick does not exclude UTI. Canonical text in C6.
   M01's request "retain infection exclusion before steroids" is compatible (the assessment stays,
   the wait for a culture goes). Citation [NICE_NG220], [Fowler_2009] (test for UTI first in bladder
   symptoms).

7. **Steroids for a relapse beyond 14 days are an individual decision** (M01 8d31a900). Decision:
   FIXED, as a class over the relapses that began more than 14 days before assessment: M01 (6
   weeks), M02 (3 weeks), P04 (16 days), P05 (3 weeks), RM04 (3 weeks), RP04 (6 weeks), RP05 (3
   weeks). NICE asks for assessment and treatment within 14 days of onset and says not all relapses
   need steroids; beyond that window the decision weighs whether the deficit is still progressing or
   disabling, current activity on MRI (an enhancing symptomatic lesion) and the patient's preference.
   The must keeps the regimen (oral 500 mg x5 days first line, IV 1 g x3-5 days for severe relapse,
   inpatient care or monitoring needs). Tumefactive cases follow D10 instead. Citation [NICE_NG220].

8. **Intermittent self-catheterisation only for a confirmed raised residual** (S02 d39dab89, S03
   572f1efc, S04 5ddb7080). Decision: FIXED in all 12 measured PVR musts (M01, M02, M03, P04, P05,
   RM04, RS02, RS03, S02, S03, S04, S06). The UK consensus does use a residual over 100 mL as the ISC
   threshold, so the number is not wrong, but one bladder scan is not enough: the must asks for a
   residual measured (repeated if raised) and ISC teaching through the continence or urology team
   when a raised residual is confirmed and symptomatic. Canonical text in C8. This applies the
   physician's ruling within the guideline (not a decline). Citation [Fowler_2009].

9. **S1P first-dose monitoring is not universal** (RS06 31eb1284; RP05 99088fd7 for its cardiac
   clause). Decision: FIXED. RS06 drug-check warning and RP05 prohibition[3] are rewritten: baseline
   ECG before any S1P modulator; first-dose monitoring for all patients with fingolimod; for
   ozanimod and ponesimod (and other S1P modulators per their labels) only with the pre-existing
   cardiac conditions the label lists. Measured: only these two statements assert it for the whole
   class (RS02, RS03, RS05 outputs say it of fingolimod only, which is correct). Citation: fingolimod,
   Zeposia and ponesimod labels.

10. **Tumefactive lesions: steroid decision, CSF cytology, biopsy** (RP01 25994494, RP02 64579059,
    RP03 b3996cce). Decisions:
    - A negative CSF cytology and flow cytometry do not exclude lymphoma, so they are not a
      sufficient gate for corticosteroids (RP01; same must and prohibition in RM01 and RM02, measured).
      Canonical text C10a: decide corticosteroids with neurosurgery and neuro-oncology after CSF has
      been taken; if neoplastic suspicion remains, stereotactic biopsy before corticosteroids unless
      deterioration makes waiting unsafe.
    - RP02 (4.1 cm, 6 mm shift, papilloedema, LP contraindicated, imaging indeterminate): the musts
      make tissue the precondition of treatment, so the biopsy criterion becomes **required** and
      enters `required_before_assessment`; the musts allow corticosteroids without waiting when
      deterioration makes it unsafe (EHA-ESMO wording). The alternative (soften the musts to keep
      biopsy recommended) is clinically worse: with LP impossible and lymphoma not excluded, tissue
      is the only route to the diagnosis.
    - RP03 (GCS 8, medullary lesion): biopsy stays recommended; the must becomes an urgent joint
      decision: urgent biopsy of the accessible right temporal lesion before corticosteroids is
      preferred, but if she deteriorates before tissue can be taken, corticosteroids are not delayed.
      Prohibition[2] is reworded to match. This keeps October C1b (Hardy 2013) and follows the
      physician on timing.
    Citation [EHA_ESMO_PCNSL_2024], [Hardy_2013].

11. **Pre-LP safety with a tumefactive lesion** (RM01 7a15f67e, RM02 aac7f149). Decision: FIXED for
    the three tumefactive cases that keep a CSF criterion (RM01, RM02, RP01): the constraint
    `action-1-analyze-brain-mri` -> `action-5-analyze-csf` becomes **hard** (an LP before the scan of
    a 4.2 cm lesion is unsafe), its reason names the checks, and a must requires the documented
    pre-LP assessment (no midline shift, no effacement of basal cisterns or fourth ventricle, no
    papilloedema, stable consciousness). Their MRI and fundoscopy already document these (measured:
    "without midline shift", "no papilloedema" in all three). RP02 and RP03 keep LP as a
    contraindicated avoided action. The 25 non-tumefactive cases keep the soft constraint.
    Citation: ROUND_POLICY (hard only when the reverse order is unsafe); [Hardy_2013] for the
    tumefactive work-up; no LP-specific guideline is cited.

12. **RP03 reversible postoperative causes** (RP03 f273dd7b). Decision: FIXED. New must: immediate
    check of capillary glucose (glibenclamide), oxygenation and ventilation by arterial blood gas,
    residual anaesthetic, opioid or neuromuscular-blocker effect from the anaesthetic record, sodium,
    and an acute vascular event on the diffusion and gadolinium MRI. New **required** criterion
    `action-abg` (`interpret_labs` `{panels: ["ABG"]}`, vocabulary term exists) with a stored
    follow-up blood gas that excludes hypercapnia and hypoxia as the cause; add it to the stop rule.
    Prohibition[1] keeps its point once these are checked. Citation: none needed beyond standard
    postoperative care; the must names checks, not a guideline threshold.

13. **RP03 OCB references with no LP** (RP03 7f4a6c46). Decision: FIXED. Remove "The absent
    oligoclonal bands do not count against NMOSD, so the CBA result carries the exclusion" from the
    NMOSD entry and "and absent bands" from the MOGAD entry; the CSF content stays only in
    `fallback_tool_outputs.csf` (October L), which an agent reaches only by doing the contraindicated
    LP. RP02 measured: no OCB reference in its ground truth.

14. **AQP4-IgG/MOG-IgG is targeted** (S06 9b6ac8b8, S06 aa109b3c, S05 35951e23). Decision: FIXED,
    and the October tier rule (C3, pack section 2: recommended whenever optic neuritis or myelitis is
    in the history) is revised. The 2024 criteria advise MOG-IgG testing in adults with features
    suggestive of MOGAD, and R1's July guidance already said "when the presentation is atypical".
    New rule: `required` with a red flag (unchanged: M04, RM01, RM02, RP01, RP02, RP03, RP05, RS01);
    `recommended` with a feature suggestive of NMOSD or MOGAD but no red flag (simultaneous optic
    neuritis and myelitis in one attack, optic disc swelling, painful tonic spasms): M03 (right colour
    desaturation with the myelitis), P04, RM04, S02, S03, S04, S05; `optional` in the other typical
    presentations: M01, M02, P05, RP04, RS02, RS03, RS05, RS06, S01, S06; none (no criterion, stored
    negative follow-up kept) in P01, P02, P03, RM03, RS04. Counts: 8 required, 7 recommended, 10
    optional, 5 none. Rationales say "targeted"
    and that a negative CBA lowers but does not exclude NMOSD or MOGAD; delete "settles it before
    DMT" and the prohibition "Do not start a DMT before NMOSD and MOGAD are excluded" (S05, S06). S06
    prohibition[0] drops the AQP4 result (an agent may not order it now). P04 prohibition[1]
    (natalizumab or S1P before AQP4 CBA) stays: P04 keeps the assay recommended and those drugs can
    worsen NMOSD. Citation [McDonald_2024], [Wingerchuk_2015], [Banwell_2023_MOGAD].

15. **P05 natalizumab and platform prohibitions** (P05 36c0f924). Decision: FIXED. Delete
    prohibition[2] (no platform therapy) and replace prohibition[3] with "Do not start natalizumab
    without an explicit PML benefit-risk discussion: her anti-JCV index of 2.84 is in the high-risk
    range (above 1.5)". The must keeps the preference for an anti-CD20 antibody. This revises the
    October P05 line ("keep T8") on the physician's ruling: a high index raises PML risk but is not an
    absolute contraindication (natalizumab label: risk stratification by index, duration, prior
    immunosuppression). Citation: natalizumab label (via the case's own drug output), [NICE_NG220].

16. **RS01 vascular assessment** (RS01 ca5f6a94). Decision: FIXED. Sudden onset on waking at 61 with
    hypertension and dyslipidaemia is a red flag for a brainstem infarct; normal ADC a week later and
    enhancement do not exclude a subacute infarct. Add a **required** criterion `action-vascular-imaging`
    (`order_advanced_imaging` `{modality: MR_angiography}`) with a stored normal head-and-neck MRA
    follow-up (vertebrobasilar system patent, no basilar stenosis), in the stop rule; rewrite the
    lacunar-infarct differential and the KCE ADC line; delete the echo and cardiac-monitoring waste
    labels (their "not an infarct" rationale is the disputed premise; the stored echo and Holter
    fallbacks are normal and stay unscored). October plan's RS01 line ("DWI shows no restriction:
    low") is revised. Measured with the class heuristic: no other MS-RR case has a sudden-onset
    deficit at 50 or over with vascular risk (RP05 is 54 with risk factors but progressive over 3
    weeks; RP04 47, 6 weeks progressive). Citation [AHA_2021_SecPrev], [Allen_2012].

17. **RM04 CT label and hypercalcaemia** (RM04 0f34eee4). Decision: FIXED. `order_ct_scan` images
    head and neck only (tool contract), so the label does not penalise chest CT; reword the rationale
    to "Head CT ...". Because the case says the PTH-independent hypercalcaemia "still needs its own
    work-up", add an optional criterion `action-chest-ct` (`order_body_imaging` `{study: chest_CT}`)
    with a stored chest CT report (no hilar or mediastinal adenopathy, no parenchymal nodules or mass)
    and a must to investigate the hypercalcaemia separately (chest imaging, PTH-related peptide and
    1,25-dihydroxyvitamin D through endocrinology). Class: 18 of 27 CT waste rationales say "CT"
    without "head": change to "Head CT" (wording only).

18. **S03 ancestry** (S03 d26941cf). Decision: DECLINED. The note says the patient is of East Asian
    descent; `patient.demographics.ethnicity` is "African American" in S03 (also at base 06b74446),
    and no field of S03 mentions East Asian descent (S02 and RS02 are the East Asian patients). NMOSD
    is relatively more frequent in people of African and Asian ancestry (Wingerchuk_2015 context), so
    the sentence is correct for this patient. The note is likely about another case; it asks for no
    change in S03. If the AQP4 rationale is rewritten under D14 the ancestry clause may stay.

19. **Pack, guidance and claims follow-up**: CENTRAL items in plan section 4 (pack sections 1.3, 1.9,
    2, 3, 8; condition_tool_guidance `interpret_labs` response counts; test_guidance_claims). No
    synonym, vocabulary, library or code change is needed for any MS-RR note.

20. **October decisions revised in this round** (each with its reason above): C1/pack 1.3 (D3),
    C3/pack AQP4 tier rule (D14), pack section 8 musts (D5, D6, D8), pack 1.9 steroid gate (D10),
    October P05 T8 (D15), October RS01 stroke line and its echo/monitoring waste labels (D16).
    Kept: everything else, including C1b Hardy_2013, LP contraindicated in RP02/RP03, the MRI
    contrast pairs and the CSF tiers.
