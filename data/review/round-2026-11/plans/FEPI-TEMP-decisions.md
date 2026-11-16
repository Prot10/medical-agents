# FEPI-TEMP: November 2026 decisions (lead, 16 Nov 2026)

Scope: 213 R1 notes (NB-KSC3-TWUA-QDTM) in all 30 cases; no FEPI-TEMP case is approved
(work/approved.txt has none). Base: HEAD 71517e55 (LIT and MRI-CONTRAST classes committed).
Every decision gives note ids (first 8 characters; full ids in the plan's per-case index), the
decision, the reason and the citation. Keys in brackets are in the criteria-pack allow-list
(section 9 of `criteria_packs/FEPI-TEMP.md`); keys marked NEW are added by CENTRAL 1 with the
full reference given here (each verified by web search on 16 Nov 2026 unless marked "label").

New keys (CENTRAL 1):
- RS02 photic stimulation uses the existing `[IFCN_ILAE_EEG_2023]` (Peltola 2023); no new key.
- `[HH_consensus_2026]` NEW: International consensus on the evaluation and management of
  hypothalamic hamartomas: results from a modified Delphi survey. Neurology 2026 (PMC13031823).
- `[SNO_EANO_prophylaxis_2021]` NEW: Walbert T, Harrison RA, Schiff D, et al. SNO and EANO practice
  guideline update: anticonvulsant prophylaxis in patients with newly diagnosed brain tumors.
  Neuro-Oncology 2021;23(11):1835-1844.
- `[AAN_AES_SMFM_2024]` NEW: Pack AM, Oskoui M, Williams Roberson S, et al. Teratogenesis, perinatal,
  and neurodevelopmental outcomes after in utero exposure to antiseizure medication: practice
  guideline from the AAN, AES and SMFM. Neurology 2024;102(11):e209279.
- `[AHA_CVT_2024]` NEW: Saposnik G, Bushnell C, Coutinho JM, et al. Diagnosis and management of
  cerebral venous thrombosis: a scientific statement from the AHA. Stroke 2024;55(3):e77-e90.
- `[ACEP_seizure_2004]` NEW: ACEP Clinical policy: critical issues in the evaluation and management
  of adult patients presenting to the emergency department with seizures. Ann Emerg Med
  2004;43:605-625 (Level B: pregnancy test in women of childbearing age).
- `[Lacosamide_label]` NEW: lacosamide prescribing information (FDA label section 12.3: 15-20% lower
  lacosamide concentrations with carbamazepine, phenytoin or phenobarbital; EU SmPC section 4.5:
  about 25% lower exposure in adults).
- `[EAU_hyponatremia_2014]` NEW (label, standard reference): Spasovski G, Vanholder R, Allolio B, et al.
  Clinical practice guideline on diagnosis and treatment of hyponatraemia. Eur J Endocrinol
  2014;170(3):G1-G47.
- `[Friedman_IIH_2013]` NEW (label, standard reference): Friedman DI, Liu GT, Digre KB. Revised
  diagnostic criteria for the pseudotumor cerebri syndrome in adults and children. Neurology
  2013;81(13):1159-1165.
- `[WHO_CNS5_2021]` NEW (label, standard reference): Louis DN, Perry A, Wesseling P, et al. The 2021
  WHO Classification of Tumors of the Central Nervous System: a summary. Neuro Oncol
  2021;23(8):1231-1251.
- `[CDC_USMEC_2024]` NEW (label, standard reference): Nguyen AT, Curtis KM, Tepper NK, et al. U.S.
  Medical Eligibility Criteria for Contraceptive Use, 2024. MMWR Recomm Rep 2024;73(4):1-126.

Entries marked "label" are standard references I did not re-open this round; CENTRAL 1 asks the
orchestrator to verify them before adding them to the allow-list (workers may use them).

## Class decisions

1. **LIT** (73 notes, all 30 cases: every bare "remove"/"no"/"no search literature" note, plus
   RM03 52e4ccf2 on the ECCL search returning general references). FIXED by class LIT (commit
   393c547e), verified by script: no `search_medical_literature` output (initial, follow-up,
   fallback) or criterion is left in the 30 cases. Residue: two `metadata.case_body_concerns`
   lines (P02, P03) still describe a literature step; delete them (metadata is shown to
   physicians). This reverses October open question 1 (one neutral literature block kept): the
   physician ruled twice (October Reviewer 1, November R1) that literature is not a patient
   step; ROUND_POLICY rule 5 already allowed removal.

2. **MRI-CONTRAST** (11 notes: M05, P02, RM02, RM03, RM04, RP01, RP03, RS01, S02, S03, S06).
   FIXED by class MRI-CONTRAST (commit 71517e55), verified by script: each initial MRI now has
   `contrast_used: false` and no gadolinium text, and a `request_contrast_mri` follow-up carries
   `contrast_used: true`. P02 9b59000c offered "or remove the observation": the pair keeps the
   post-gadolinium finding in the gadolinium study, which is the better option (the study exists).
   M04 gets a new gadolinium study under decision 30 (no note on its flag; it had no gadolinium).

3. **BIOPSY: standalone brain biopsy is an avoided action** (31 notes in 23 cases plus the 5
   tumour notes of decision 4; RS05 de44b8b5 is filed on the TEE step but its text is this
   demand). Measured: 28/30 cases store a stereotactic and an open biopsy follow-up (all except
   P04, RP02), none labelled; no case in the dataset has an `obtain_tissue_diagnosis` avoided
   action. Decision: add two avoided actions, `obtain_tissue_diagnosis {procedure:
   stereotactic_biopsy}` and `{procedure: open_biopsy}`, severity `harm`, in 29 cases (all but
   RP03), with a case-specific rationale (canonical text in the plan, class BIOPSY). Severity:
   `harm` (material procedural risk, no diagnostic gain) rather than `contraindicated`: the
   dataset uses `contraindicated` for an act unsafe because of a specific feature of the patient;
   here the problem is lack of indication, as with RS02's gadolinium (`harm`). RP03 is excluded:
   in an enlarging metastasis on checkpoint inhibitors tissue can be needed to separate
   progression from pseudoprogression or radiation necrosis, an MDT decision (ASCO_irAE_2021);
   no note asks for it there. The stored biopsy reports stay (an agent that orders one still gets
   a coherent result). Citations: HS cases `[ILAE_MRI_2019]`; lesional and tumour cases
   `[Blumcke_2017]`; cavernoma `[Cavernoma_2017]`; LGI1 `[Graus_2016]`; HSV `[IDSA_enc_2008]`;
   PNES `[ILAE_PNES_2013]`; TSC `[TSC_2021]`; hamartoma `[HH_consensus_2026]`; encephalocele
   `[Encephalocele_2015]`; RS02 (pregnant) `[ILAE_MRI_2019]` like the other HS cases.
   Own extension (RS05 f5970455 names surgery too): `obtain_tissue_diagnosis {procedure:
   resection}` severity `harm` in the 18 cases with no surgical indication at this encounter
   (M01, M02, M03, P01, P02, P03, P05, RM01, RM02, RM03, RP01, RP02, RS02, RS03, RS05, S01,
   S04, S05): every one is treatment-naive, controlled, acute or a mimic, and their case
   fallback answers a resection order with an anterior temporal lobectomy specimen. Cases where
   surgery is the plan (M04, M05, RM04, RP04, RP05, RS01, RS04, P04, S02, S03, S06, RP03) keep
   resection unlabelled. Cross-condition: unlabelled biopsy follow-ups also in NMDAR-ENC (18
   cases), SE (6), GLIO-HG (3, where tissue is usually required): CENTRAL 6.

4. **Lesional tumours: maximal safe resection, not standalone biopsy** (S02 92195484, 3e1f7693;
   S03 9b3cb044; S06 b43646cf, 4958762a). FIXED: the surgical must becomes the canonical
   "multidisciplinary epilepsy-surgery evaluation aiming at complete resection, which gives the
   histological diagnosis; standalone biopsy only if resection is unsafe or tissue would change
   management" (plan, class TUMOUR); biopsies labelled per decision 3. Same must wording in
   RM04 and M04 (presumed low-grade lesion). Source: `[Blumcke_2017]`, `[Engel_2003]`.

5. **TEE** (RM02 6bcac12f, RP02 02536f90, RS05 85512f5e). FIXED: avoided action
   `order_echocardiogram {echo_type: TEE}` severity `waste` in the three cases that store a TEE.
   `waste`, not `harm`: R1 calls it "low yield" in RP02; TEE risk is small, and a 0.35 cap for
   one echo would outweigh far riskier errors. TTE stays as it is (RS05 already waste; RM02 adult
   rhabdomyoma surveillance and RP02 echo are not labelled: TSC 2021 and ESC 2019 leave TTE to
   clinical need). Cross-condition: 8 more unlabelled TEE follow-ups (GBS 1, SE 3, VASC-DEM 4):
   CENTRAL 6.

6. **HLA-B*15:02** (M02 6a18310d, M05 aa57706a, P04 9ba5595d, RS05 5479d55f, S04 404a1855).
   FIXED for all 7 cases holding the must (M02, M04, M05, P04, RS05, S04, S06): the must becomes a
   prohibition, canonical text in the plan (class HLA), which adds HLA-A*31:01 as R1 suggests in
   RS05. Reason: CPIC 2018 ties testing to the decision to start carbamazepine or oxcarbazepine
   in at-risk ancestry; with lamotrigine or levetiracetam planned, an unconditional must demands
   a test the plan does not need. This respects October fact 10 ("must or prohibition") and C17
   (no HLA vocabulary term). DECLINED in part: S04's "ancestry inferred from the surname" and M02's
   "ancestry undocumented": `patient.demographics.ethnicity` states "Southeast Asian (Lao)" and
   "East Asian", and the agent sees demographics. `[CPIC_2018]`.

7. **Valproate prohibition wording** (RP02 d2ad939c). FIXED in all 19 prohibitions that quote the
   UK MHRA "under 55, two specialists" rule (M01, M02, M03, M04, M05, P01, RM01, RM03, RM04, RP02,
   RP05, RS03, RS05, S01-S06): replaced by jurisdiction-neutral canonical texts (women / men, plan
   class VPA). Reason: RP02 is set in the United States and the MHRA procedure is UK law; none of
   the cases needs the procedure, only the clinical rule, which NICE NG217 (2025), the AAN/AES/SMFM
   2024 guideline and the FDA boxed warning share. RS01's must informing a man of the paternal
   risk (MHRA and EMA 2024) stays: it is counselling content, true everywhere. MIG-AURA has 5 more
   MHRA lines: CENTRAL 6. `[NICE_NG217_2025]`, `[AAN_AES_SMFM_2024]`.

8. **Abnormal lab rows with null clinical_significance** (M03 dad7c7ae, P02 0bb5b735 and
   3f653640, RM02 eb350688, RM03 bcf111dd, RM04 ce4fad4e, RP01 9a000203, RP02 a598b629 and
   ae306531, RP04 fd653fe7, RS02 67484266, RS03 492937af and 6af81874, RS04 5f1e70d9). FIXED
   with the CENTRAL display remark (null printed as "none"): fill `clinical_significance` of each
   named row with a short factual interpretation that does not name the case diagnosis (plan
   class LABSIG gives the text per row), and fix the must the value needs. Measured: 64 abnormal
   rows with null significance in 21 cases; besides the named ones, the plan lists the rows that
   need management or explain a finding (ASM levels, sodium, CK/lactate after the convulsion,
   TSH on ICI, anaemia); trivial ones (glucose 102-142, Mg 2.3, bicarbonate 21 in S05, MCV 78) stay
   null. Two clinical corrections ride on it: RP02 levetiracetam has no established therapeutic
   range (interpret with dose timing, adherence, renal function: ILAE TDM practice; R1 ae306531);
   RS03 topiramate 3.2 on 100 mg/day is consistent with the dose and she denies missed doses, so
   October's "points to missed doses" is reversed (R1 6af81874).

9. **Neuropsychology "global abnormal = no"** (M05 0a5a3164, P01 1e26e813, P04 9df51056).
   ALREADY-FIXED + CENTRAL: the reports have no global flag; each cited row (BVMT-R, RCFT, Benton)
   is already `abnormal: "yes"` against its 40-60 T range; the first row shown is FSIQ (normal).
   CENTRAL 3: review app should show test name first and per-row flags.

10. **Lateralization of manual automatisms** (M01 017610be, M02 ad4f9105, M04 a97c6c3b, S01
    86eeff1f). FIXED as a class. Unilateral manual automatisms are usually ipsilateral to the
    onset; contralateral dystonic posturing, late forced version and Todd paresis are
    contralateral `[Lateralization_2005]`. Measured: 13/30 cases describe automatisms in the hand
    contralateral to the MRI/EEG focus without comment (M01, M02, M04, M05, RM02, RM04, RP03,
    RP04, RP05, RS01, RS05, S01, S06), a template error (expected discordance is a minority).
    Decision: flip the automatism hand to the focus side in every mention of these 13 cases
    (chief complaint, HPI, exam, EEG and video-EEG semiology, KCE, differential, red herrings),
    keeping genuinely contralateral signs (dystonia, head version, clonic arm, Todd paresis);
    RP03's slow (non-forced) head turn is ipsilateral too and flips with the hand. Any KCE on the
    sign uses the canonical text (plan). M04: the interictal sharp waves move to the left mid
    temporal region (phase reversal T3, field to T5 and F7), matching the posterior superior
    temporal lesion; the KCE says localization rests on MRI-EEG concordance and the epileptogenic
    zone is defined at presurgical evaluation.

11. **Diagnosis certainty (labels)**. FIXED as label changes (CENTRAL 2, synonyms check):
    - S02 b872a6c7, S03 dbefe268, S06 76151661: "...due to a <side> <site> low-grade
      glioneuronal tumor (presumed DNET)". Reverses October D2 because the physician rules it and
      WHO CNS5 makes DNET a histological (integrated) diagnosis; the MRI is characteristic, not
      diagnostic, and ganglioglioma stays in the differential. `[WHO_CNS5_2021]`.
    - RM04 8388f9f6: "...low-grade epilepsy-associated tumor (presumed ganglioglioma or DNET)",
      no grade. Reverses October C6: a CNS WHO grade needs histology.
    - M04 (f6c4443b, class): "(suspected focal cortical dysplasia)", like P01 and RP04; the MRI
      itself says a low-grade tumour cannot be excluded.
    - P04 753c02d4: "Drug-resistant focal epilepsy of right temporal lobe origin, nonlesional on
      1.5T epilepsy-protocol MRI (3T MRI not tolerated)".
    - RP03 6f89d2a1: drop "(with concurrent suspected immune-related neurotoxicity from
      checkpoint inhibitors)"; it is a differential (and already a rejected label).
    - RS01 7ee70785: "Drug-resistant focal epilepsy with left temporal lobe seizures and left
      mesial temporal sclerosis in a patient with a hypothalamic hamartoma and gelastic seizures
      (dual pathology)". October D3 is kept for the term (two separate lesions), but "secondary
      to" is dropped: secondary epileptogenesis or propagation cannot be told from independent
      generators before presurgical evaluation.
    - RS02 03c72e26: "Focal epilepsy of right temporal lobe origin with right mesial temporal
      sclerosis and presumed remote calcified neurocysticercosis, presenting at 33 weeks
      gestation". The association is possible, not proven; serology is negative (IDSA 2018:
      calcified NCC is often seronegative), so "presumed".
    - RP04 6571ab91: ALREADY-FIXED (MRI "possibly FCD type IIIa", label "suspected"); its
      surgical musts are fixed under decision 22.

12. **Differential wording: no categorical exclusion by a test that cannot exclude** (M01
    deb665fd, M02 9c483898, P05 a2e33c1b, RM03 23af9681, RP03 866290ba, RS02 dba0eeb9, RS03
    549292c1 and bd456258). FIXED with canonical texts (plan class DIFF), extended to the same
    PNES template in M03 and M04. Likelihood stays `low`; the text says what makes it unlikely and
    what would reopen it. Diagnosis-level "excluded" statements that rest on imaging the case
    actually has (e.g. "MTS without tumor: excluded as the sole substrate") stay.

13. **Key clinical evidence corrections** (M02 adb731fc, RM01 11aee0f0, S01 86eeff1f, RS02
    dba0eeb9, P05 254836e2). FIXED: "possible nocturnal convulsive seizures" (M02 KCE and must);
    CT does not exclude shunt malfunction (RM01, canonical in plan); S01 lateralization (decision
    10); RS02 KCE[0] "make eclampsia unlikely"; P05 prolactin drawn at 22 minutes is outside the
    10-20 minute window and is at most supportive `[AAN_prolactin_2005]` (the October pack rule
    itself): remove "argues against" from KCE, criterion evidence and the PNES differential.

14. **Treatment timing vs stop rule** (RM03 7d9daed6, RP01 03911b8d, S01 e1e2f67a; RP02
    78946c3e in part). NO-ACTION on the case data + CENTRAL 4. The stop rule only says which
    studies must be resulted before the final assessment; the harness has no treatment action,
    so nothing in the scoring delays treatment, and the musts already say "without waiting" (RP01
    acyclovir, RM03 ASM restart). CENTRAL 4: say so in the review app's stop-rule panel and in
    the harness doc. RP02's clinical content (empiric anticoagulation, PE first) is FIXED under
    decision 20.

15. **Stop rule EEG subtypes** (P01 8e90d267, RP01 adaf74ab). ALREADY-FIXED + CENTRAL 3: the stop
    rules key on criteria whose arguments carry `eeg_type` (P01 routine + video; RP01
    continuous_icu); the MockServer routes by `eeg_type`. The app shows only the tool name.
    RP02 54a0e930 and RP03 81b2b522 are FIXED under decisions 20 and 21.

16. **Pregnancy test in women of childbearing potential** (S04 1255373f). FIXED as class PREG:
    a `recommended` criterion `interpret_labs {panels: ["beta-hCG"]}` with a stored negative
    result in its own `beta-hCG` panel, in the women of childbearing potential whose pregnancy
    status is not established and who start or switch an ASM or present with a first convulsion:
    M01, M02, P01, RP05, RM02 (valproate), RS03 (topiramate, postpartum), RS04 (valproate), S02,
    S04, S06 (S02 and S06 already store a row: move or alias it so the order serves it).
    `[ACEP_seizure_2004]`; valproate and topiramate pregnancy prevention programmes
    `[MHRA_VPA_2024]`, `[MHRA_TPM_2024]`. Not added: M05 (HPI states she is not pregnant), P03,
    P04 (established, on a COC; no ASM start), RP03, RS02 (pregnant).

17. **Presurgical neuropsychology and language lateralization** (RS01 bc558a72, S02 914006ad,
    S03 483070f9). RS01 (presurgical admission, drug-resistant): FIXED with a `recommended`
    `order_specialized_test {test_type: neuropsych_battery}` criterion and a new case-specific
    stored report, as in P04, RP04, RS04 `[HH_consensus_2026]` (the consensus rates preoperative
    neuropsychology important). S02, S03 (first convulsion, referral stage): FIXED in the surgical
    must ("presurgical evaluation including neuropsychology (verbal and nonverbal memory) and,
    where the planned resection makes it relevant, language lateralization (fMRI or Wada); his
    left-handedness does not establish language dominance"), no criterion: these tests are done
    at the surgical centre after referral, not in this encounter, and R1 asks for them to be
    individualised.

## Case decisions

18. **P05** (4076ba14, 4f347644). Video-EEG `required` -> `recommended`, ECG `required` ->
    `optional`; stop rule = MRI + routine EEG. Overrides October C8 with reason: the routine EEG
    already shows right anterior temporal sharp-and-slow waves and the MRI right HS, so the
    epilepsy diagnosis is secure without event capture (NICE NG217: video-EEG when the diagnosis
    remains uncertain); a normal 12-lead ECG, Holter, TTE and tilt test were done 1-2 months ago,
    so a repeat ECG is acceptable, not mandatory (R1 July ruling: ECG optional). Prohibition [0]
    keeps its content but cites the routine EEG and MRI, and the video-EEG only "when done".

19. **RP01** (583b91c2, 03911b8d). New `optional` criterion `action-imaging-before-lp`
    (alternatives `order_ct_scan {}` and `analyze_brain_mri {}`) and the hard constraint becomes
    `action-imaging-before-lp -> action-4-analyze-csf`; the MRI -> CSF constraint is deleted.
    Reason: the scorer orders the first call matching each criterion, and one call may match two
    criteria, so CT-first or MRI-first both satisfy the safety rule and LP before any imaging
    still caps; ABN 2012 and IDSA 2008 accept CT to exclude mass effect before LP and warn
    against delaying CSF and acyclovir for MRI. Not extended to P02 and RP03: no urgency for CSF
    there and the MRI is required first anyway (RP03's lesion is the mass in question).

20. **RP02** (78946c3e, 54a0e930, 9f64da60, 02536f90, d2ad939c, a598b629, ae306531). Criteria
    order: labs, ECG, CT pulmonary angiography first; soft constraints `action-11 (CTA) ->
    action-3 (MRI)` and `-> action-8 (ambulatory EEG)`, `[ESC_PE_2019]`. Routine EEG `required` ->
    `recommended` and out of the stop rule (ambulatory EEG is the decisive study; R1). Must:
    "start anticoagulation without waiting for imaging when clinical probability is high or
    intermediate and bleeding risk is acceptable" (ESC 2019 class I). Ambulatory EEG report: the
    convulsive semiology comes from the roommate's account and the push-button diary, with EMG
    artifact over the evolving discharge. TEE waste (decision 5); valproate (7); labs (8).

21. **RP03** (81b2b522, 6f89d2a1, ae100235, 06bda243, 866290ba). Add `recommended` video-EEG
    criterion `{eeg_type: video}` (the stored 72-hour study captured nine seizures; the routine EEG
    has no epileptiform discharges); not in the stop rule (the events were witnessed on
    examination). Label (decision 11). KCE: primary ASM prophylaxis in a seizure-free patient with
    brain metastases is not recommended `[SNO_EANO_prophylaxis_2021]` (Level A); after her
    seizures, treatment is indicated; the HPI stays factual. Must [1]: "decide with oncology,
    after multidisciplinary review of progression versus pseudoprogression and of immune-related
    adverse events, whether to continue, hold or modify ipilimumab and nivolumab"
    `[ASCO_irAE_2021]`. ICI-encephalitis differential conditional (DIFF). The categorical
    steroid prohibition [3] becomes "do not start high-dose corticosteroids for presumed
    checkpoint-inhibitor encephalitis while CSF is non-inflammatory and the seizures are
    explained by the metastasis; reassess if symptoms progress".

22. **RP04** (0621d8e0, de703336, 3e0134ae, 7f425884, 621e716f, fd653fe7, 6571ab91). Surgical
    musts: "present at the epilepsy surgery conference; the extent of resection (anterior
    temporal lobectomy including the temporopolar abnormality, or a more selective approach) is
    individualized after language lateralization and memory assessment"; delete the
    "hippocampus-limited resection" prohibition. The physician is right that no guideline
    mandates ATL over SAH; including the pole is a reasonable option, not a rule. de703336 (on
    that prohibition) carries the biopsy text: FIXED by decision 3. DDI report: enzyme inducers
    lower lacosamide exposure by 15-25% `[Lacosamide_label]`, and the sodium-channel effects add
    (dizziness, diplopia, PR prolongation).

23. **RP05** (d90d6600, c9507886, 2011eddd). Must: "start first-line ASM and discuss early with
    an epilepsy surgery centre (encephalocele-associated TLE responds well to resection or
    disconnection); refer for presurgical evaluation if seizures continue on an appropriate ASM"
    `[Encephalocele_2015]`; she is not drug-resistant. IIH: add a `recommended`
    `order_advanced_imaging {modality: MR_venography}` criterion with a stored MRV (bilateral
    transverse sinus narrowing, no thrombosis), and the neuro-ophthalmology must adds "measure
    CSF opening pressure by lumbar puncture if papilledema is confirmed, and treat confirmed
    intracranial hypertension before any skull-base repair" `[Friedman_IIH_2013]`. CT: "focal
    full-thickness defect of the floor of the middle cranial fossa (greater sphenoid wing)".

24. **RS01** (b69115d8, 3d552490, bc558a72). Delete "intracranial EEG may be needed to define the
    contribution of each" (the consensus rates intracranial EEG not useful in HH diagnosis
    `[HH_consensus_2026]`); keep "invasive EEG only if a separate temporal epileptogenic zone
    remains a management-changing question". Laser ablation or resection first; repeat
    radiosurgery conditional on review of the prior Gamma Knife dose, fields and residual
    anatomy. Neuropsychology criterion (decision 17).

25. **RS02** (025465ed, 60ae567c, f55eb305, dba0eeb9, 67484266, 03c72e26). EEG: photic
    stimulation "not performed (pregnancy)": the IFCN-ILAE minimum standards list pregnancy as a
    contraindication to IPS as well as to hyperventilation `[IFCN_ILAE_EEG_2023]` (verified;
    the triage doubt was wrong). Must [0]: "urgent obstetric and fetal assessment; serial blood
    pressure and preeclampsia laboratory monitoring; give magnesium sulfate if eclampsia is
    suspected clinically, including an atypical presentation without hypertension or
    proteinuria" `[ACOG_HTN_2020]`. CT: `optional` criterion `order_ct_scan {}` answered by the
    existing case fallback (calcified granulomas) `[IDSA_NCC_2018]`; its rationale says it may be
    deferred after delivery.

26. **RS03** (6e8cff87, 549292c1, bd456258, 492937af, 6af81874). Medication: "Topiramate
    (immediate release) 50 mg twice daily"; HPI: a trial of 200 mg/day at age 20 caused
    word-finding difficulty and paresthesia, so she stayed on 100 mg/day accepting rare auras.
    Add a `recommended` MR venography criterion with a stored normal MRV `[AHA_CVT_2024]` (six
    weeks postpartum, headaches, a convulsion). Labs: add platelets, creatinine, AST/ALT and urine
    protein/creatinine (normal) to the stored labs and the labs criterion; must: "postpartum
    obstetric review with serial blood pressure" `[ACOG_HTN_2020]`. Must: recheck bicarbonate
    before raising topiramate (carbonic anhydrase inhibition).

27. **RS04** (a59ef5a3, 09c35528, 2508252d, 5f1e70d9). HPI: chronology of failed adequate trials
    (doses, durations, adherence, outcomes) meeting Kwan 2010. History: reproductive history,
    current contraception and pregnancy intentions; hCG (decision 16). Musts: "highly effective
    contraception not affected by her enzyme inducers (copper or levonorgestrel IUD, or depot
    medroxyprogesterone), chosen with her" `[CDC_USMEC_2024]`; staged rationalization, one drug
    at a time under supervision (introduce the replacement, withdraw valproate gradually, then a
    slow phenobarbital taper), with sodium monitoring on carbamazepine.

28. **RM01** (60ee35f8, 11aee0f0). Must: "before the 3T MRI, identify the shunt valve model and
    its MR conditions and record a programmable valve's setting; check and reset it after the
    scan". KCE (DIFF/KCE canonical); must: "compare the CT with prior imaging and obtain
    neurosurgical review if headaches or cognitive change persist".

29. **RM02** (a7f7e00b). Must reworded: "plan a switch from valproate to lamotrigine or
    levetiracetam by cross-titration after an individual risk-benefit discussion; while valproate
    continues, keep her in the pregnancy prevention programme". The switch stays: NICE NG217 (2025)
    and MHRA/EMA 2024 say valproate must not continue in a woman who can become pregnant unless
    nothing else is suitable; R1's individualisation is added, not the switch removed (PARTLY
    DECLINED: the switch itself remains, with that citation).

30. **M04** (59a8a93b, bbebeeda, f6c4443b). Chronology: the outside MRI moves to about nine months
    ago, when he sought care for headaches and the first spells, in HPI, PMH, MRI comparison line
    and red herring. Technique line: "3T dedicated epilepsy protocol (HARNESS-MRI: 1 mm isotropic
    3D T1 and 3D FLAIR, high-resolution coronal T2 perpendicular to the hippocampal long axis,
    DWI)" `[ILAE_MRI_2019]`. Add a gadolinium study (MRI-CONTRAST pair: initial `false`, new
    follow-up `true`, no enhancement, lesion unchanged) with a `recommended` criterion
    `{contrast: true}`, because the report itself leaves a low-grade tumour open (ILAE 2019:
    contrast when a tumour is suspected); must: "review the MRI with expert neuroradiology at the
    epilepsy surgery conference". Label (decision 11). The 12 other initial MRIs without a
    technique line say "epilepsy protocol" elsewhere or not at all; not a note, left (NO-ACTION).

31. **RM03** (b8774a1b, 23af9681). HPI: when EMS arrived he was still unresponsive and had a second
    convulsion without regaining consciousness, for which EMS gave IV lorazepam 2 mg (status
    epilepticus criteria met; treatment appropriate). Must: "protect the airway (GCS 8 on
    arrival), keep neurological observations, and obtain an urgent, preferably continuous, EEG if
    consciousness does not return to baseline". NCSE differential conditional (DIFF).

32. **P02** (322e3ebd, 0bb5b735, 3f653640). Must: "assess the hyponatremia (volume status, serum
    and urine osmolality, urine sodium, symptoms) and treat by mechanism (fluid restriction for
    euvolemic SIADH), monitor sodium, and taper carbamazepine to a non-inducing ASM that does not
    lower sodium" `[EAU_hyponatremia_2014]`; add serum osmolality, urine osmolality and urine
    sodium (SIADH pattern) to the stored labs and as a `recommended` criterion
    `interpret_labs {panels: [serum_osmolality, urine_osmolality, urine_sodium]}`.

33. **S04** (9a147be9) and S02 (same text). Must: "lamotrigine with the standard slow titration
    (rash risk); ethinylestradiol lowers lamotrigine levels, so the maintenance dose is adjusted to
    response and levels, which rise in the pill-free week" `[Sabers_2003]`.

34. **S05** (51cb6971). Prohibition: "Do not treat the postictal dysphasia as a stroke (no
    thrombolysis) once it is established as postictal: it followed a witnessed seizure, resolved
    within minutes and MRI shows no restricted diffusion; a persistent or atypical deficit still
    needs urgent stroke assessment."

35. **M03** (dad7c7ae). Vitamin D row filled; must: "continue vitamin D supplementation and recheck
    the level (bone health on long-term ASM therapy)"; satisfiable because the history documents
    the insufficiency and the supplement.

36. **M05, RS05, others**: no case-specific decision beyond the classes.

## Declined, in full or in part
- S04 404a1855 and M02 6a18310d, the "ancestry undocumented / inferred from surname" part:
  demographics state the ancestry (decision 6).
- RM02 a7f7e00b, the request not to mandate the switch: the switch remains (decision 29).
- Nothing else is declined. Three notes are ALREADY-FIXED with a CENTRAL display remark
  (decision 9), two stop-rule notes ALREADY-FIXED + CENTRAL (15), four timing notes NO-ACTION +
  CENTRAL (14), RP04 6571ab91 ALREADY-FIXED (11).

## Conflicts with October, resolved
LIT vs open question 1 (1); HLA vs fact 10 / C17, kept as prohibition (6); DNET labels vs D2
and RM04 grade vs C6 (11); dual pathology vs D3, term kept, causality dropped (11); P05 ECG vs
C8 and prolactin use (13, 18); RS03 "missed doses" (8); RP04 resection extent (22).

## NEEDS-ANDREA
None: every point is decided on clinical grounds.
