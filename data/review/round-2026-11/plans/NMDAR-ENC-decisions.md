# NMDAR-ENC: decisions, November 2026 round (lead, 17 Nov 2026)

All 35 notes are from R2 (NB-87MF-FBTV-TPWE). 11 are plain approvals. Each decision below covers
a class: it applies to every case of the condition that has the defect, approved cases included.
Approved cases are changed only where they carry the same defect. In the 11 approved cases that
defect is the template musts, which carry numbers the physician ruled wrong. Case-level detail is in
`NMDAR-ENC.md` section 3.

Sources were checked on 17 Nov 2026 (WebSearch). Each item lists what was checked:
- **Graus F et al., Lancet Neurol 2016;15:391-404** (PMC5066574). Verified verbatim: "CSF herpes
  simplex virus PCR can be negative if done too early (eg, within 24 h), and this test should be
  repeated if the clinical suspicion remains high."
- **Abboud H et al., JNNP 2021;92:757-768** (doi 10.1136/jnnp-2020-325300). Verified verbatim:
  - "PLEX (5-10 sessions every other day)".
  - "If there is no clinical, radiological, or electrophysiological improvement by the end of the
    initial treatment cycle, add IVIG or PLEX."
  - "Consider IVIG first in agitated patients and in those with bleeding disorders."
  - "Consider PLEX first in patients with severe hyponatraemia, high thromboembolic (or cancer)
    risk, and if there is associated brain or spinal demyelination."
  - IVIG "may also worsen coexisting hyponatraemia due to volume expansion".
  - Second line after 2-4 weeks without response to optimised first-line therapy.
  - Prior to CSF analysis, the usual practice is CNS-dose IV aciclovir plus standard coverage for
    bacterial meningitis.
  - Combined steroid with IVIG or PLEX from the start is an option.
- **Abboud, R2's reading, not reached in the search snippets:** methylprednisolone 1 g/day for
  3-7 days, IVIG 2 g/kg over 2-5 days, cyclophosphamide 600-1000 mg/m², box 1 item 9 (combined
  therapy for severe presentations) and item 13 (bridging). These come from the physician's own
  reading of the cited paper, and none contradicts a verified passage. They are adopted as the
  physician's ruling. The Abboud companion paper (JNNP 2021;92:897-907) confirms that oral
  prednisone was the most popular bridging therapy, followed by periodic IVIG.
- **van de Beek D et al., ESCMID guideline on acute bacterial meningitis, Clin Microbiol Infect
  2016;22 Suppl 3:S37-S62** (doi 10.1016/j.cmi.2016.01.007). Verified: treatment by age and local
  resistance; Listeria cover above 50 years (the UK uses above 60); vancomycin added where
  pneumococcal beta-lactam resistance is a concern.
- **NICE NG240 (2024):** a cephalosporin may be given when a penicillin allergy reaction is not
  severe.
- **Stanford Health Care empirical guide, an IDSA-based hospital implementation:**
  - meropenem 2 g every 8 hours plus vancomycin for a non-severe cephalosporin allergy;
  - moxifloxacin plus vancomycin, with co-trimoxazole for Listeria, for a severe beta-lactam
    allergy.
- **Spasovski 2014, Lejuste 2016, ASCO irAE 2021, Titulaer 2013 and Armangue 2018** were verified
  in October; these are pack allow-list keys.

---

1. **MRI contrast header** (S03 7907651d, S04 0d6e3601, S06 1d9f3e58, S09 f0dd0c07, S10 18186d99,
   and the MRI sub-points of P01, P06, RP01, RP02, RP03, RS01, RS03, RS04 and M05).
   - Ruling: ALREADY-FIXED by the MRI-CONTRAST class (commit 71517e55).
   - Evidence: `mri_probe.py` on all 30 cases, run 17 Nov 2026.
     - The initial MRI is the plain study (`contrast_used: false`, no gadolinium text).
     - The `request_contrast_mri` follow-up is the gadolinium study (`contrast_used: true`).
     - The required criterion `{contrast: true}` receives the gadolinium study in all 30 cases.
   - No action.

2. **M1 aciclovir, PCR repeat wording** (every non-approval verdict).
   - Ruling: FIXED, all 30 cases. Replace "repeat the PCR on a second CSF sample if the first LP was
     within 72 hours of onset" with the Graus 2016 wording, cited "(Graus 2016)".
   - Where the LP was 2 days or less after neurological onset (RS03, RP02), the must states the
     repeat explicitly and continues aciclovir until it returns.
   - M05 asked as an alternative to cite Solomon 2012 for the 72-hour rule. The 72-hour rule goes,
     so Solomon is not needed. The M05 note also cited a "step 11" Solomon output: that was a
     literature output, removed in the LIT class (commit 393c547e; the 06b74446 copy of M05 holds
     it), so that sub-point is ALREADY-FIXED.
   - October conflict: October attributed the 72-hour rule to Venkatesan 2013 and Solomon 2012.
     The physician's wording is the cited diagnostic standard of this condition and is not
     contradicted by either source, so the physician's ruling wins.

3. **M1 empirical bacterial meningitis cover** (M01, M02, M03, M04, M05, P01, P02, P04, P05, P06,
   RM01, RM03, RP01, RP02, RP03, RS01, RS02, RS03, RS04).
   - Ruling: FIXED, all 30 cases (class).
   - Reason: Abboud (verified): CNS-dose aciclovir and standard bacterial cover are started before
     the CSF is analysed. The must is time-limited: "until the CSF cell count, Gram stain and
     culture exclude bacterial infection". At assessment time the CSF reports are in hand, so the
     agent states that cover stops (or continues for another indication).
   - Regimen by allergy and age (ESCMID 2016, NICE NG240, IDSA-based implementation):
     - (a) no beta-lactam allergy, under 50 and not immunosuppressed: ceftriaxone 2 g IV every 12
       hours with vancomycin;
     - (b) non-severe penicillin or amoxicillin rash: the same, since a cephalosporin is
       acceptable;
     - (c) cephalosporin hives (M01, S02): meropenem 2 g IV every 8 hours with vancomycin;
     - (d) 50 or older, or after high-dose steroids (RS02): add Listeria cover. That is amoxicillin
       2 g IV every 4 hours without a penicillin allergy (RP01, RS02), or co-trimoxazole with a
       penicillin allergy (RM03, RP02, RP03).
     - Valproate (RS02): no carbapenem, because carbapenems sharply lower valproate levels (the
       case's own interaction step).
   - RP02: ceftriaxone is already in must 8 for the aspiration pneumonia. The must says that it is
     also the meningitis cover until the culture is negative, with co-trimoxazole for Listeria.
   - RS03: the new chest CT shows aspiration (decision 12), so ceftriaxone continues as treatment
     of the aspiration pneumonia.

4. **M2 first-line doses** (all non-approval verdicts; class in all 30).
   - Ruling: FIXED in all 30: IV methylprednisolone 1 g daily for 3 to 7 days; IVIG 2 g/kg over 2
     to 5 days; plasma exchange 5 to 10 sessions every other day (Abboud 2021).
   - The same "5 to 7 exchanges" text is corrected in the drug-interaction outputs of P04, RM03,
     RP01, RP02, RS01, RS03, RS04 and S01 (`alternatives`).
   - The `proposed` strings (5-day methylprednisolone, IVIG 0.4 g/kg/day for 5 days) lie inside the
     Abboud ranges and stay.

5. **M2 combined versus sequential start** (M01, P01, P02, P04, P06, RM01, RM03, RP01, RP02, RP03,
   RS01, RS03, RS04).
   - Ruling: FIXED.
     - Sequential start in P01, P04, RM03 and RP01: methylprednisolone first, adding the named
       agent if there is no improvement by the end of the steroid course (Abboud items 7-8). The
       physician ruled each mild or ward-level and asked "justify or change"; we change, because
       these four have no ICU criterion, dysautonomia or recurrent seizures with fluctuating
       consciousness.
     - Combined start in the other 26, with the severity reason written into the must (Abboud box
       1 item 9). RP02 already has steroids first, adding IVIG or PLEX for severity; it keeps that
       wording with the reason.

6. **M2 IVIG versus PLEX trade-off** (all non-approval verdicts).
   - Ruling: FIXED, all 30. The must names the patient's factors on both sides and the preferred
     agent, with the precaution for the alternative.
   - Rule, applied in order (Abboud, verified wording):
     - (1) Brain or spinal demyelination: PLEX (RS04 bilateral optic neuritis; RS02 tract lesions).
     - (2) Sodium below 125 mmol/L without marked dysautonomia: PLEX (M01).
     - (3) Agitation or dysautonomia: IVIG. Monitor sodium when Na is below 135. With a thrombotic
       factor, add hydration, a slow infusion and VTE prophylaxis, and stop oestrogen.
     - (4) Otherwise, sodium below 130 or a high thromboembolic or cancer risk: PLEX (M05, P01, P04,
       RP01, RP02).
     - (5) Otherwise, either agent.
   - Exceptions: RM03 gets IVIG despite rule 4, because its orthostatic hypotension argues against
     PLEX volume shifts (physician: "record the divergence"). It also checks osmolality before a
     sodium fall is treated. RP02 gets PLEX despite dysautonomia, because active cancer, age 76 and
     the IVIG AKI risk with lisinopril in CKD outweigh it.
   - The per-case table is in plan section 2, K3.

7. **Bridging therapy** (M01, M02, M05, P01, P02).
   - Ruling: FIXED, as a new must in every case except RP02, which already has the oral taper.
   - Canonical text: "After the acute course, bridge with a gradual oral prednisone taper, or
     monthly IVIG or IV methylprednisolone, while recovery or second-line therapy takes effect
     (Abboud 2021)."
   - Pneumocystis prophylaxis is added only in RP02 (decision 19).

8. **M7 escalation timing and cyclophosphamide dose** (all non-approval verdicts; class in all
   30).
   - Ruling: FIXED. "If there is no clinical or radiological improvement 2 to 4 weeks after
     completion of first-line therapy, escalate to rituximab (375 mg/m² weekly for 4 doses or 1000
     mg twice 2 weeks apart, after hepatitis B screening) and/or IV cyclophosphamide 600 to 1000
     mg/m² monthly<; discuss fertility preservation before cyclophosphamide> (Abboud 2021)."
   - P02 and RP02 keep "consider escalation at the earlier end of this window" for ICU-level
     disease.
   - October conflict: October wrote "10 to 14 days (Abboud 2021)". That is a misattribution: the
     verified Abboud text says 2-4 weeks, so we correct it. October's cyclophosphamide figure (750
     mg/m²) lies within the range the physician gives.

9. **Hyponatraemia correction limit** (M05; class M01, M04, M05, RM03, S06, S09, S10).
   - Ruling: FIXED by attribution, the option the physician offered. Where a case had "no more than
     10 mmol/L in 24 hours", write "correct slowly, by no more than 10 mmol/L in the first 24 hours
     (Spasovski 2014), to avoid osmotic demyelination".
   - Spasovski 2014 is the pack's verified hyponatraemia guideline. Attribution keeps a checkable
     number and is better than softening it.

10. **Benzodiazepines first and avoiding antipsychotics** (M05, P01).
    - Ruling: FIXED, class in every case whose agitation must says it: append "(Lejuste 2016)".
    - RP01 and RP02 have no such must, so they are untouched.
    - The P1 prohibition rests on the same source, but no note asked about it, so it is not churned.

11. **Tumour screen after a first negative study**:
    - M02, P05: pelvic MRI.
    - RM01, RS04: pelvic MRI and CAP CT.
    - M05: CAP CT, which the physician offered as "consider".
    - RS03: chest CT.
    - RM03, RP01: whole-body FDG-PET.
    - RS02: pelvic ultrasound.
    - RM03, RS02: mammography.
    Ruling: FIXED, except mammography, which is CENTRAL.
    - Reason: Abboud box 1 item 6. Targeted screening first, pelvic MRI if equivocal, CT- or
      MRI-based general screening for extragonadal germ cell tumours, whole-body PET after a
      negative CT when cancer suspicion is high, and mammography because CT is insensitive for
      early breast cancer.
    - Each new study is a `recommended` criterion with a stored follow-up (normal unless stated in
      the plan), and the tumour must is reworded to match. P03 and RP03 (post-HSV, not
      tumour-associated: Armangue 2018) are unchanged.
    - October conflict: the pack's M3 templates ("repeat pelvic imaging if poor response or
      relapse"; "no further tumour imaging is needed" in men) are replaced by the physician's
      ruling. Abboud's screening algorithm says otherwise, and October gave no source for the
      deferral.

12. **RS03 chest CT** (NB-87M:NMDAR-ENC-RS03).
    - Ruling: FIXED. Add a recommended criterion with alternatives `{study: chest_CT}` and `{study:
      chest_abdomen_pelvis_CT}`, served by one stored contrast CAP CT.
    - The CT shows a dependent right lower lobe consolidation consistent with aspiration, and no
      mediastinal or retroperitoneal mass or lymphadenopathy.
    - Reason: desaturation to 71%, vomiting, neutrophilia and a wide A-a gradient (decision 22);
      plus the extragonadal germ cell question (Abboud).

13. **Pelvic MRI as an OR alternative of pelvic ultrasound** (M01 action 5).
    - Ruling: FIXED, class: in the 20 women aged 12-44 whose required tumour criterion is pelvic
      ultrasound, add `{study: pelvis_abdomen_MRI}`.
    - The 20: M01, M02, M04, P01, P04, P05, P06, P07, P08, RM01, RM02, RS01, RS04, S01, S02, S03,
      S04, S06, S09, S10.
    - Excluded: M03, where pelvic MRI is the separate characterisation step after an equivocal
      ultrasound (soft sequence).
    - Reason: Abboud and the July 2026 tool review ("pelvic and abdominal imaging (MRI, CT, or
      ultrasound)").
    - Each case must store a pelvic MRI whose findings match the ultrasound, checked with `served()`.

14. **Teratoma resection as a recommended `obtain_tissue_diagnosis` criterion** (M01).
    - Ruling: DECLINED.
    - Reason: ROUND_POLICY rule 4 and POLICY_AUTHORING_GUIDE. Treatment is never a tool call, and
      tumour removal is management, already required by must 3. The histology does not change the
      diagnosis: CSF anti-GluN1 makes it definite (Graus 2016).
    - The stored resection report stays, so a premature order gets a realistic report, but it earns
      no credit. Must 3 is satisfiable as a recommendation, so it is not "unsatisfiable".

15. **Immunotherapy before the antibody result in P01 and P04** (NB-87M P01, P04; also
    `prohibited_recommendations[1]`).
    - Ruling: FIXED.
    - P01: reword the must and P2 on the Graus 2016 criteria for possible autoimmune encephalitis
      (subacute psychiatric and cognitive change with seizures, alternatives reasonably excluded)
      and Abboud's "highly suspected, infection excluded on basic CSF".
    - P04: before the antibody result, neither the possible nor the probable criteria are met (no
      focal sign, EEG-confirmed seizure, pleocytosis or suggestive MRI). We take the physician's
      first option, which is the clinically sounder one: start immunotherapy once the CSF anti-GluN1
      result is available. The CSF report carries it, so at assessment the disease is definite.
    - P04's P2 becomes: do not delay immunotherapy now that CSF anti-GluN1 is positive, for example
      while waiting for repeat testing, serum confirmation or the teratoma operation.

16. **P04 brain FDG-PET** (NB-87M:NMDAR-ENC-P04).
    - Ruling: FIXED, as an `optional` criterion `{modality: FDG_PET}`. P04 already stores an
      abnormal brain FDG-PET (frontal hypermetabolism, parieto-occipital hypometabolism).
    - Reason: Abboud box 1 item 5 (PET when suspicion is high and the other studies are
      uninformative).
    - October and July conflict: the pack says that FDG-PET is "not a case criterion". That was a
      general removal; this is one case that fits the Abboud indication, and the same reviewer asks
      for it. It applies to P04 only.

17. **RP01 diagnosis standard** (NB-87M:NMDAR-ENC-RP01).
    - Ruling: FIXED, by the confirmatory-test option, which is compatible with October Q1.
    - The CSF `NMDAR_antibodies` result states that the positive cell-based assay (1:4) was
      confirmed by a tissue-based assay at the reference laboratory: rat brain immunohistochemistry
      with the neuropil pattern of NMDAR antibodies. That is Graus 2016's confirmatory test for a
      phenotype that does not fit. Key evidence bullet 2 says why it was done.
    - No vocabulary term exists to order a tissue-based assay separately (CENTRAL 2). Reference
      laboratories run it as a confirmatory test on the same sample, so stating it in the CSF result
      is realistic.
    - The phenotype is not rewritten: that would undo October Q1 (a recast that rests on Graus 2016
      and Gresa-Arribas 2014).

18. **RP01 vascular imaging and stroke** (NB-87M:NMDAR-ENC-RP01).
    - Ruling: FIXED.
      - Add a recommended criterion `{modality: MR_angiography}`, with a stored MRA: no stenosis,
        occlusion or vascular malformation of the intracranial or cervical arteries.
      - A CTA alternative is added only if a probe shows the case can serve a CTA report.
      - The stroke differential stays `low`, with the MRA in its key features.
      - The ADC argument is softened: ADC can pseudo-normalise in a subacute infarct.
      - Must 2: steroids are started once vascular imaging has excluded a stroke.
    - The requested sequence constraint is DECLINED, because immunotherapy is not a criterion. The
      order is encoded in the must.
    - Also FIXED for RP01: gastric protection (a proton pump inhibitor) while aspirin and
      high-dose steroids are given (RP01 DDI step). The same class applies to RP03 (aspirin).

19. **RP02 fixes** (NB-87M:NMDAR-ENC-RP02).
    - Ruling: FIXED, all of the following:
      - Creatinine clearance: creatinine goes from 1.3 to 1.5 mg/dL, flagged high and listed in the
        abnormal summary and the interpretation. Cockcroft-Gault (age 76, 77.2 kg) then gives 46
        mL/min. Musts 2 and 5 say "about 46 mL/min (Cockcroft-Gault)". This keeps the case's
        renal-dosing teaching and the DDI bands (30-50, 25-50) with one data change instead of four
        text changes.
      - Babinski laterality: right Babinski, left plantar equivocal, contralateral to the left
        temporal lesion and the right-limb seizures. The worker checks the EEG and HPI for the
        seizure side.
      - Repeat PCR: the LP was within about 24 hours of onset. HSV is less likely (afebrile, normal
        medial temporal lobes), but steroids are starting, so continue aciclovir and repeat the
        HSV PCR before stopping it.
      - Must 3: PLEX 5-10; agent PLEX (decision 6).
      - Add Pneumocystis prophylaxis while prednisone stays at 20 mg/day or more for 4 weeks or
        longer: co-trimoxazole, renally adjusted, with potassium monitoring on lisinopril (ASCO irAE
        2021, the case's governing irAE guideline). Add glucose and sodium monitoring.
    - Bacterial cover: decision 3.

20. **RP03 coronary angiography and coronary CTA** (NB-87M:NMDAR-ENC-RP03).
    - Ruling: FIXED. Two avoided actions, severity `harm`, as the physician asks:
      - `order_advanced_imaging {modality: coronary_angiography}`;
      - `order_advanced_imaging {modality: coronary_CTA}`.
    - Rationale: no chest pain or ischaemic ECG change. They are an invasive procedure, or iodinated
      contrast and radiation, in an agitated encephalopathic patient.
    - Citation: Gulati M et al. 2021 AHA/ACC chest pain guideline (Circulation 2021;144:e368-e454),
      under which coronary testing needs a chest-pain or ischaemia indication. The worker verifies
      it before citing; if it cannot be verified, the worker uses no citation key rather than an
      unverified one, and says so in the log.
    - No criterion matches these calls.

21. **Glucose ratio pairing** (S03 7907651d, S04 0d6e3601; class M01, P01, S01, S02).
    - Ruling: FIXED. The CSF report's paired serum glucose takes the labs value, and the ratio is
      recomputed to two decimals:
      - M01: 95, ratio 0.67;
      - P01: 100, ratio 0.58;
      - S01: 106, ratio 0.58;
      - S02: 114, ratio 0.58;
      - S03: 104, ratio 0.58;
      - S04: 96, ratio 0.67.
    - October conflict (P01, kept as "different sampling times"): reversed. The review app shows
      no sampling time, so a reviewer cannot tell, and the physician ruled the mismatch an error in
      S03 and S04.
    - The same defect exists in MS-RR (7) and ALZ-EARLY-P02 (1); that is reported, and is theirs to
      fix.

22. **RS03 blood gas** (NB-87M:NMDAR-ENC-RS03).
    - Ruling: FIXED.
      - pH 7.16, from HCO3 18 and pCO2 52 in the same post-ictal draw. The mixed acidosis fits a
        lactate of 8.1.
      - Add "on 4 L/min nasal oxygen (FiO2 about 0.36)".
      - Update the abnormal summary and the interpretation.
    - With an FiO2 of 0.36 the A-a gradient is about 120 mmHg. That is wide, and it is explained by
      the aspiration the chest CT now shows (decision 12).

23. **Lateralisation in M03 and M04** (NB-87M M03, M04).
    - Ruling: FIXED by the physician's second option: state the discordance in key clinical
      evidence. It is compatible with October, which kept the sides.
    - Text: "The equivocal <side> medial temporal MRI signal and the <other side> temporal EEG
      seizures [and PET] are discordant; anti-NMDAR encephalitis is a diffuse process in which
      lateralised findings need not agree, and neither side indicates a focal lesion."
    - Aligning the sides would rewrite 3 to 4 reports without a clinical gain. The M03 MRI is
      equivocal ("may represent artifact"), and M03's left lower facial droop matches the right MRI.
    - The scan found no other unilateral discordance: P01 has incidental foci, RM02 bilateral MRI.

24. **Template post-intervention cognitive screen** (P01; class).
    - The same text is in all 30 cases.
    - Ruling: FIXED where it contradicts the baseline screen (P01, P04, RP01). Write "repeat bedside
      screen during the admission: findings unchanged from the baseline screen", with the baseline's
      deficits: P01 MoCA-level deficits; P04 disorientation to date and executive deficits; RP01
      fluent aphasia with impaired comprehension.
    - It must report no treatment effect (ROUND_POLICY rule 4).
    - The other 27 baselines are severe or not completed, so "persisting marked impairment" is
      consistent there: NO-ACTION.

25. **Performance status versus gait** (P06; class P08, RM03).
    - Ruling: FIXED. Where the exam and the timed gait test show independent or supervised walking,
      the performance-status row "confined to bed or chair ... mobilises only with assistance"
      becomes "walks with supervision; up and about less than half of waking hours".
    - ECOG 3 and Karnofsky stay unless the self-care row disagrees.

26. **P06 EEG versus exam** (NB-87M:NMDAR-ENC-P06).
    - Ruling: FIXED by linking the events, the clinically better option, because the staring with
      oromandibular automatisms is the seizure semiology.
      - The routine EEG states that no clinical event occurred during the recording.
      - The cEEG states that some of the 5 seizures (the worker chooses 2) had staring and
        oromandibular automatisms and the rest had no clinical correlate.
      - Mirror the change in the ambulatory EEG follow-up, which copies the cEEG.

27. **New fever on arrival** (RS04; class M01).
    - Ruling: FIXED. Where the HPI says that fever is denied and the arrival temperature is 38.0 C
      or more, add "she is febrile (<T> C) on arrival, a new fever". Mirror it in `patient.hpi`.

28. **Infection screen in RS02** (NB-87M:NMDAR-ENC-RS02).
    - Ruling: FIXED. Two recommended criteria, `order_microbiology {specimen: urine}` and
      `{specimen: blood_culture}`, each with a stored result:
      - urine culture: no significant growth;
      - blood cultures: no growth at 48 hours.
    - Add a low-likelihood differential entry for intercurrent catheter-associated or line
      infection.
    - The pack's "blood cultures not indicated without sepsis" rule does not apply: this patient
      has fever, CRP 50 and a catheter.

29. **RS04 meningoencephalitis pattern** (NB-87M:NMDAR-ENC-RS04).
    - Ruling: FIXED.
    - Add neurosarcoidosis to the differential (`low`, after the results).
    - Add recommended criteria:
      - serum ACE `{panels: [ACE]}`, stored normal;
      - CSF flow cytometry `{special_tests: [flow_cytometry]}`: the initial CSF report carries a
        polyclonal, non-malignant result;
      - CAP CT (decision 11): no hilar or mediastinal lymphadenopathy.
    - Must 2 gives PLEX for the bilateral optic neuritis, with levetiracetam dosed after each
      exchange.

30. **RM01 MOG overlap and ANA** (NB-87M:NMDAR-ENC-RM01).
    - Ruling: FIXED.
      - Add a recommended criterion `{panels: [MOG_IgG_cell_based]}`, with a stored "MOG and AQP4
        antibodies (serum, cell-based assay)" panel, both negative.
      - Fill the ANA row's `clinical_significance` with "Low-titre ANA, frequent in healthy adults;
        interpret with anti-dsDNA and ENA".
      - Add anti-dsDNA and ENA (negative) to that panel.
      - Add NPSLE to the differential (`low`).
      - Add holding ibuprofen during aciclovir and steroids to must 1. The same class applies to
        RM02.

31. **M05 musts** (NB-87M:NMDAR-ENC-M05).
    - Ruling: FIXED.
      - Must 3: "a negative scrotal ultrasound does not exclude an extragonadal germ cell tumour",
        with a contrast CAP CT criterion and its report (decision 11).
      - Must 6: "high-dependency or ICU care according to airway status and seizure control"
        (Abboud ICU indications).
      - Must 8: add (Lejuste 2016).
      - Must 9: decision 9.
      - Bridging: decision 7.
    - Step 10 cyclophosphamide misquote and step 11 Solomon: ALREADY-FIXED (LIT, commit 393c547e).

32. **P02 hyponatraemia must** (NB-87M:NMDAR-ENC-P02).
    - Ruling: FIXED. "Monitor serum sodium daily and correct the mild hyponatraemia (131 mmol/L)
      slowly, with fluid restriction if it follows an SIADH pattern; IVIG can worsen it (Abboud
      2021)."
    - Must 3 (orchiectomy): NO-ACTION, which the physician confirmed.

33. **PLEX drug dosing** (RS02, RS04). Ruling: FIXED.
    - RS02: give valproate doses after each exchange, and time enoxaparin around catheter placement.
    - RS04: give levetiracetam after each exchange.

34. **Plain approvals** (P03, P07, P08, RM02, S01, S02, S03, S04, S06, S09, S10 policy verdicts with
    no comment). Ruling: NO-ACTION for the notes themselves. The class decisions above still apply
    to these cases; each such change is named in the per-case index.

35. **RP03 FDG-PET impression** (own finding). The last sentence is garbled ("mildly reduced
    uptake in the right frontal gliosis in the left frontal, insular...").
    - Rewrite it: markedly reduced uptake in the left frontal, insular, anterior and mesial temporal
      encephalomalacia, and mildly reduced uptake at the right frontal gliosis.
    - The hypermetabolism statement is limited to the right temporal cortex, so it does not
      contradict the right frontal gliosis.
