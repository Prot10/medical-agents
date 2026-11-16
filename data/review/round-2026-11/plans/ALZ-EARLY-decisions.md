# ALZ-EARLY: decisions for the November 2026 round (16 Nov 2026)

85 notes, all R1 (NB-KSC3-TWUA-QDTM), in 19 cases (RM03, RM04, RP01-RP05, RS01-RS06, S01-S06).
No ALZ-EARLY case is in work/approved.txt. Andrea's rule applies: decide for the quality of the
dataset. NEEDS-ANDREA: none. Measurement scripts are in
/home/aprotani/review-round-2026-11/work/scratch/alz-lead/.

Sources checked this round (16 Nov 2026):
- NICE NG97 (2018), recommendations 1.2.14, 1.2.15 and 1.2.23 (nice.org.uk/guidance/ng97/chapter/recommendations).
  1.2.14: further tests only if they would help diagnose a subtype and knowing it would change
  management. 1.2.15: if the diagnosis is uncertain and AD is suspected, consider FDG-PET (perfusion
  SPECT if FDG-PET is unavailable) or CSF; if a diagnosis cannot be made after one of these tests,
  consider the other. 1.2.23: if FTD is suspected, use FDG-PET or perfusion SPECT.
- Rabinovici GD et al., updated AUC for amyloid and tau PET, Alzheimers Dement 2025;21:e14338
  (`[Appropriate_Use_Amyloid_PET]`): tau PET has 5 appropriate scenarios, among them MCI or dementia
  under 65 with suspected AD and anti-amyloid eligibility. Tau PET is therefore not labelled waste here.
- European Commission marketing authorisations: lecanemab (Leqembi) 15 Apr 2025 and donanemab
  (Kisunla) 24 Sep 2025 (Commission Decision C(2025) 6625), both for MCI or mild dementia due to AD
  with confirmed amyloid pathology in ApoE e4 non-carriers or heterozygotes. FDA: lecanemab 2023,
  donanemab 2024. Appropriate-use recommendations: Cummings J et al. 2023 (`[Lecanemab_AUR_2023]`),
  MMSE 22-30.
- Goldbrunner R et al., EANO guideline on meningiomas, Neuro Oncol 2021;23(11):1821-1834
  (doi 10.1093/neuonc/noab150): MRI is the diagnostic modality, and observation comes first for
  incidental asymptomatic meningioma.
- Bora E et al., Cognitive impairment in euthymic major depressive disorder: a meta-analysis,
  Psychol Med 2013;43(10):2017-2026 (doi 10.1017/S0033291712002085): deficits persist after
  remission.
- ADA, Older adults, Standards of Care 2026, Table 13.2 (`[ADA_older_adults_2026]`, verified in
  October): A1C below 8.0% for complex/intermediate health, which includes mild to moderate
  cognitive impairment.

---

1. **Neuropsychological flag notes are a display artifact (43 notes, 17 cases): CENTRAL.**
   Notes: every neuropsych-flag note in section 3 of the plan except c23ae468. I checked each row
   the note names against its own value and range
   (`np_print.py`, `np_flags.py`). The data already holds the flag the physician asks for. The flag
   the physician objected to belongs to the next row: the review app prints `abnormal` above
   `test`. The "overall abnormal = no" that RP03 (06bc0294) and S06 (4e456ba4) mention is the MMSE
   row (findings[0]), shown at the top. RP03 MMSE 25/30 is within 24-30 and S06 MMSE 28/30 is within
   24-30, both correctly "no". Dataset-wide check (1458 rows with a range and a flag): the only real
   mismatch is S06 TMT-B (decision 2). The other 14 hits are parser artifacts (z-scores, IQ above
   average, BP strings). Ruling: CENTRAL (CENTRAL.md item 2, render label keys first). No case change.

2. **S06 Trail Making Test Part B, 24th percentile against a 25th-75th range, flagged "no" (c23ae468): FIXED.**
   Set `abnormal` to "yes". The impression must agree: replace "Processing speed, executive
   function, and visuoconstructive ability are within the low-normal range." with "Processing speed
   (Trail Making A, 38th percentile) and visuoconstructive ability (Rey Complex Figure copy, 42nd
   percentile) are within the reference range; set-shifting (Trail Making B, 24th percentile) is
   just below it." The staging and label (amnestic MCI) do not change. Reason: a flag must agree
   with the report's own range (style guide, internal consistency). A remark kept for the record:
   25th-75th is the "average" band, not an impairment cutoff (conventional cutoffs are 1 to 1.5 SD,
   about the 16th or 7th percentile). The physicians accepted the stated ranges, so the ranges are
   not churned.

3. **Amyloid PET after a conclusive CSF (f05917ed RM03, f901b0ca RM04, 576cbc84 RP01, 8839e83f RP02, bd0e2f77 RP03, 7e7426ae RP05): FIXED by decisions 7 and 8. The stored report is kept.**
   The policy already has one optional criterion with two alternatives (CSF or amyloid PET). This
   is October Q3 and R1's July ruling ("if CSF biomarkers are already conclusive, amyloid PET is
   usually not required"), and NICE 1.2.15 says the second test is for the case where the first is
   not diagnostic. The second test is never credited (each criterion is claimed once). The gap was
   that it went unpenalised with `max_additional_actions` 1. With 0 (decision 7) it counts as an
   unjustified extra. The amyloid PET cannot be an avoided action in these cases, because it is an
   alternative of a criterion (addendum: never a criterion and an avoided action on the same call).
   The stored counterpart is kept and moved behind the credited steps (decision 8). Deleting it
   would send a positive-biology patient's amyloid PET order to the library's "amyloid-negative"
   report, the contradiction October Q3 removed.

4. **RP04 amyloid PET (970178c1): FIXED with an avoided action.**
   In RP04, amyloid PET is not a criterion: the required CSF answers both the prion question and
   amyloid status. Add `avoid-waste-<n>-order-advanced-imaging-amyloid-pet`, severity `waste`,
   `{"modality": "amyloid_PET"}`. Rationale: "The lumbar puncture this rapid course requires already
   establishes amyloid status, and at MMSE 18/30 he is outside the mild stage for which anti-amyloid
   treatment is licensed, so amyloid PET would not change management [Appropriate_Use_Amyloid_PET]
   [Lecanemab_AUR_2023]." This answers R1's "unless a specific residual uncertainty or
   management-changing indication remains": neither applies here.

5. **FDG-PET (b749efc2 RM03, 6ee54325 RM04, 4f25013c RP01, f1647683 RP02, 4ec3fae9 RP03, efa4da67 RP04, 1af2b7b1 RP05): FIXED.**
   Rule (NICE 1.2.14, 1.2.15, 1.2.23 and R1): FDG-PET is a conditional test for residual subtype
   uncertainty that would change management. It is not credited when the syndrome, the MRI and the
   amyloid biomarkers settle the diagnosis.
   - Remove the optional FDG criterion in P01, P02, RM04, RP01, RP02 and RP03 (in RP03 with its
     SPECT alternative). Physicians reviewed P01 and P02 in October; the class rule applies because
     their phenotype, MRI and conclusive CSF and amyloid PET match R1's stated reason.
   - Keep the optional FDG criterion in **P03** only. That case is frontal-variant AD with a paternal
     behavioural dementia, so bvFTD is the suspected alternative, and NICE 1.2.23 names FDG-PET for
     suspected FTD.
   - Add an avoided action (`waste`, `{"modality": "FDG_PET"}`) in the 22 cases with a typical
     (amnestic) syndrome and conclusive amyloid biomarkers: M02, M04, M05, P04, RM01, RM02, RM03,
     RM04, RP04, RP05, RS01-RS06, S01-S06. Canonical rationale: "In this amnestic presentation with
     supportive MRI, amyloid status (CSF or amyloid PET) is the confirmatory test; FDG-PET would not
     change the diagnosis or management [NICE_NG97]." RP05 adds: "a Lewy body question is answered
     by the DaTscan [NICE_NG97]." RP04 adds: "the prion question is answered by DWI and CSF RT-QuIC
     [CJD_2021]."
   - No label, and no criterion, in M01 and M03 (borderline CSF, intermediate likelihood: NICE 1.2.15
     allows the other test when the first is not diagnostic) and in P01, P02, RP01, RP02 and RP03
     (atypical phenotypes, where R1 grants that FDG is "potentially useful"). There an FDG order is
     an uncredited extra under decision 7.
   - The stored FDG reports stay (October Q4: the library's normal FDG would contradict an AD
     patient) and move to the on-request block (decision 8). "Remove" is therefore applied to the
     policy and the pathway order, not to the data. Each log says so.

6. **Perfusion SPECT (4997f3f5 RP03): FIXED, as a class in all 30 cases.**
   NICE 1.2.15 and 1.2.23 make SPECT the substitute only when FDG-PET is unavailable, and R1 rules
   "not both". Add an avoided action `waste`, `{"modality": "perfusion_SPECT"}`, in all 30 cases
   (P03 included, where FDG-PET is the credited study). Rationale: "Perfusion SPECT substitutes for
   FDG-PET only where FDG-PET is unavailable; it adds nothing to this work-up [NICE_NG97]." Tau PET
   gets no label (AUC 2025 appropriate scenarios). It stays uncredited.

7. **Stop rule (2e51aa05 RM03, 0fe88822 RM04, 7c1cca06 RP01, 44dd0687 RP02, 49af6c1f RP03, bac6d7b8 RP04, a4c820f0 RP05): FIXED, all 30 cases.**
   `max_additional_actions` 1 becomes 0, and `required_before_assessment` is unchanged. This undoes
   October C16.4, which kept 1 so that "a second biomarker or FDG is not punished": R1 now rules that
   exactly those must not be done. FTD, the sister condition, already uses 0, as do 191 cases
   dataset-wide. R1 asks what is exempt. In the reward (`policy_reward.py`, stopping) an action that
   matches a criterion is never counted, so the drug check, ECG, MMA, DaTscan, EEG, gait, visual
   fields, genetics and the first amyloid test are exempt wherever they are criteria. Only
   uncredited actions after the required set count. StopRule has no prose field to say this, so the
   clarification is CENTRAL (C3) and goes in each log.

8. **Pathway order: credited steps first, on-request answers last (all 30; physicians read the follow-ups as performed).**
   `followup_outputs` order: (a) follow-ups answering a criterion's first alternative, in criterion
   order; (b) the second-alternative amyloid counterpart; (c) the on-request answers that match no
   criterion: FDG (except P03), tau PET, SPECT, speech-language (except P02), performance status,
   gait (except RM02), extra visual fields (RP03), body ultrasound (RP01, RS04), and RP04's amyloid
   PET. Measured: 143 such follow-ups in the 30 ALZ cases, and 3085 in 554 of the 600 cases. That
   is why the display change is CENTRAL (C1). Re-run perfect_agent after reordering.

9. **Abnormal lab values shown as "clinical significance: none" (09f11b21 RM03, 500ac750 RM04, 5a9b098b RP01, 13bc971a RS01, 2919de25 RP05, 0d7c5fbb RS05): FIXED + CENTRAL display.**
   The data is null (77 abnormal rows in ALZ-EARLY, none filled). Per the addendum, fill
   `clinical_significance` on the abnormal rows that need management or explain a finding, using
   the canonical texts in plan C4, in every ALZ case (class). Leave the trivial rows null (sodium,
   chloride, BUN, glucose where an HbA1c row exists). The musts that these values require were
   checked: all exist (RM03 R7 TSH and R8 HbA1c; RM04 R1 levothyroxine and R2 IDA; RP01 R3 LDL;
   RS01 R4 LDL; RP05 R2 B12; RS05 R1 B12). No new must is needed, apart from the wording fixes in
   decision 11. The display half goes to CENTRAL.md item 1.

10. **"No medicine is approved for MCI" (ed848cd8 S06; class M01, M02, M03, M04, RM04): FIXED.**
    It is wrong since the anti-amyloid authorisations (FDA 2023 and 2024; EC Apr and Sep 2025). Replace
    the clause in the reassessment must (canonical text in plan C5), and in S06 also
    `metadata.key_educational_points[4]`. The prohibition ("Do not start a cholinesterase inhibitor or
    memantine ... neither is approved for MCI") and the KCE ("Cholinesterase inhibitors are not
    approved for MCI") are correct and stay.

11. **Glycaemic target (887d7401 RS05; class M02): FIXED.**
    ADA 2026 Table 13.2 sets A1C below 8.0% with mild to moderate cognitive impairment, and MCI
    qualifies. RS05's 7.3% is at target, so "improve glycaemic control" becomes "keep HbA1c at the
    individualised target below 8.0% (7.3% now) without hypoglycaemia, and do not intensify
    [ADA_older_adults_2026]". In M02, "HbA1c 7.3%, above her goal" contradicts the same target and
    becomes "HbA1c 7.3%, within the individualised target below 8.0% for an older adult with
    cognitive impairment [ADA_older_adults_2026]". The other glycaemic musts are neutral or correct and
    stay unchanged.

12. **RS06 MRI contrast (f9f5c37f): FIXED. Undoes October Q5 in part.**
    The required MRI criterion keeps only `{"contrast": false, "protocol": "dementia"}`. Add the new
    optional criterion `action-<n>-analyze-brain-mri-contrast`, `analyze_brain_mri`
    `{"contrast": true}`. Label: "Characterise the incidental extra-axial lesion with gadolinium MRI".
    Expected evidence: from the stored contrast report. Rationale: "The non-contrast dementia study shows a dural-based
    lesion; gadolinium characterises it before a plan of observation [EANO_meningioma_2021]." Add the
    soft constraint plain MRI before contrast MRI ("Contrast is given for the lesion the non-contrast
    study shows; it is not part of the dementia protocol."). Q5's own reason (contrast is not part of
    the dementia protocol) supports this. ACR, NICE and the pack call for non-contrast imaging. Must 4
    already asks for contrast MRI "if only a non-contrast study was done", so the new criterion makes
    that must satisfiable. Tier is optional, not recommended, because R1 calls it a conditional
    follow-up and EANO puts observation first. `[EANO_meningioma_2021]` is a new key (CENTRAL C5,
    pack allow-list). Run mri_probe.py after the change.

13. **RS06 red herring (03630de8): FIXED.**
    The first sentence of `red_herrings[0].correct_interpretation` becomes "Cognitive deficits during
    a depressive episode often improve with remission but can persist." The rest stays, because it
    gives the decisive point: decline continued through 8 months of sustained remission. Source:
    Bora 2013 (decision file only; a red herring needs no citation). Class grep across 600 cases for
    absolute recovery claims about depression: only RS06 (NPH-M09 and NPH-P05 are correct).

14. **S02 statin (9633e19d): FIXED, clarification only. The premise is not in the case.**
    `past_medical_history` lists no hyperlipidaemia and `medications` lists no statin, so the case is
    not inconsistent. To make the reasoning explicit, the statin clause becomes "he takes no statin:
    check a lipid profile and start a moderate-intensity statin, indicated by type 2 diabetes at 74
    with lacunes and moderate white matter disease". The rest of the must stays. No citation is
    added: the existing must had none, and the statin statement in the 2026 dyslipidemia guideline
    was not re-verified this round.

15. **Case comments (aff6e392 RM03, c7b35285 RM04, 12d38e8c RP01, 217c0224 RP02, 26c3a5c3 RP04, c6fb8b7a RP05, 1d6670ef RS01): NO-ACTION.**
    Praise, plus the over-testing remark that decisions 3 to 8 resolve. Log them with a pointer to
    those decisions.

16. **October decisions re-examined.**
    - Kept: Q1, Q2, Q3 (one amyloid criterion with two alternatives, counterparts authored), Q4
      (FDG authored everywhere, now as an on-request answer), Q6, C1-C15.
    - Changed: C16.4 / pack section 5 (max 1 becomes 0; decision 7); 3.1 row 8 (FDG optional
      criteria, now in P03 only; decision 5); Q5 (RS06; decision 12). Each change follows a
      physician ruling and NICE NG97 / AUC 2025, as above.
