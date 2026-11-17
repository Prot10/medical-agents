# MG: decisions of the November 2026 round (lead, 17 Nov 2026)

Base: the working tree of branch fix/review-round-2026-11 after class LIT (393c547e) and
MRI-CONTRAST. 40 notes, all from R2 (NB-87MF-FBTV-TPWE), in 29 cases. MG-RM12 has no note.
Approved before this round (`work/approved.txt`): MG-RM13, MG-RM14, MG-RM15, MG-RS11.
Measurements: `plans/MG.md` section 2. Scripts and outputs:
`/home/aprotani/review-round-2026-11/work/scratch/mg-lead/` (`survey_mg.py` -> `survey.txt`,
`classes_mg.py` -> `classes_out.txt`, `struct_mg.py` -> `struct_out.txt`, `resp_mg.py`).

Note: the persisted copy of `notes/MG.md` I first read was cut at 63 KB; I re-read the end of
the file and the JSON (`notes/MG.json`), so the S05 items on HbA1c, monitoring and unsourced
figures are included.

## Sources

Verified this round (WebSearch, 17 Nov 2026):
- Jacob S, Farrugia ME, Hewamadduma C, et al. Association of British Neurologists (ABN)
  autoimmune myasthenia gravis management guidelines (2025 update). Pract Neurol
  2025;25(5):422-437, doi 10.1136/pn-2025-004655 (PMID 40940171). The abstract confirms what
  changed since 2015: daily steroids, not alternate-day, are standard; early thymectomy is
  emphasised; early rituximab is supported (within 1 year of generalized onset). The full text
  was not reachable. For its detailed rules I rely on two things: the October round's full-text
  reading (`round-2026-10/plans/MG-decisions.md`: RNS first and SFEMG if available; contrast brain
  and orbit MRI only after negative serology and neurophysiology; thymic imaging in all patients;
  thymectomy recommended under 50 and discussed at 50-65; inpatient care at FVC below 30 mL/kg;
  ICU at FVC below 20 mL/kg or a fall of more than 30%), and the reviewer's quotations, given with
  full citations. Those quotations cover: neurophysiology always in antibody-negative suspected
  MG; the outpatient, inpatient and ocular steroid protocols; the pyridostigmine maximum of
  360 mg/day with review above 300; ECG before pyridostigmine; IVIG 1 g/kg for significant bulbar
  weakness without ventilatory failure and 2 g/kg in crisis, by ideal body weight, with hepatitis
  B/C serology and IgG first; the clinical ICU criteria and the single-breath count below 25;
  early non-steroidal immunosuppression in diabetes and ischaemic heart disease; oncology
  referral for thymoma; SLT swallowing assessment for inpatients with bulbar symptoms.
- Narayanaswami P, Sanders DB, Wolfe G, et al. International Consensus Guidance for Management of
  Myasthenia Gravis: 2020 Update. Neurology 2021;96:114-122 (ICG 2020). Recommendation 1a was
  verified verbatim: "In nonthymomatous, generalized MG patients with AChR-Ab, aged 18-50 years,
  thymectomy should be considered early in the disease". MGTX enrolled patients under 65.
  Thymectomy "may be considered" in generalized MG without detectable AChR-Ab if immunotherapy
  fails, and in AChR-positive ocular MG that does not respond. Its Table 1 lists drugs to use with
  caution (beta-blockers, statins, iodinated contrast); I take this from the reviewer.
- Fionda L, Alboini PE, Antozzi C, et al. Italian recommendations for the diagnosis and treatment
  of myasthenia gravis. Neurol Sci 2026;47(4):353, doi 10.1007/s10072-026-08964-y (PMID 41857416;
  correction Neurol Sci 2026;47:483). This updates Evoli 2019. Bibliographic record verified. The
  statement contents I cite (serology statements 5, 6, 8; prevention statements 1, 2, 4;
  vaccination statement 3; severity statements 1, 2) are the reviewer's quotations.
- Rozanolixizumab (FcRn antagonist): FDA 2023 and EMA January 2024 approval for adults with
  AChR- or MuSK-antibody-positive generalized MG (UCB announcement; Rozanolixizumab: First
  Approval, PMC10590285).

Standard references used without re-verification this round: Evoli A et al., Neurol Sci
2019;40:1111-1124. Sanders DB et al., Neurology 2016;87:419-425. Lawn ND et al., Arch Neurol
2001;58:893-898. Relling MV et al., CPIC guideline for thiopurine dosing based on TPMT and NUDT15
genotypes, 2018 update, Clin Pharmacol Ther 2019;105:1095-1105. Virani SS et al., 2023
AHA/ACC/ACCP/ASPC/NLA/PCNA guideline for chronic coronary disease, Circulation
2023;148:e9-e119.

## Decisions

**D1. Display misalignment of result rows (REPORT-CONTRADICTION, review-ui-artifact).**
Notes: d6d236df (M01), 4baca060 (M02), 4257311d (M03).
Decision: CENTRAL, no data change. I checked M03 (RNS rows; respiratory FVC 2.45 L, FEV1
1.42 L, ratio 0.58) and the triage row for M01/M02. Every stored row pairs `test`, `result` and
`significance` correctly, and agrees with the impression and the red herrings. The app prints keys
alphabetically (`result`, `significance` above `test`), so each value appears above its own label.
The agent receives each row as one object and is not affected. This is already CENTRAL.md item 2.
Workers re-check the four blocks of each case against the impression before ruling.

**D2. Neurophysiology tier in seropositive MG (TIER).** Notes: S05 and the verdicts of RM11,
RM16, RP11, RP13, RS12, RS13, RS15, RS17, S01, S02, S03, S04.
Decision: RNS (and the ocular RNS-or-SFEMG criterion) goes from required to recommended in every
new diagnosis with unequivocal AChR or MuSK antibodies. The criterion leaves the stop rule. It
stays required in five kinds of case:
- seronegative and LRP4 cases (P01, P04, RP14);
- LEMS (P02, RM13);
- RP12 (needle EMG answers bulbar-onset ALS, per the reviewer);
- RM12 (the NCS decides a GBS relapse, which is CONTRA3's alternative);
- RS16 (needle EMG with RNS for the head-drop differential: neck extensor myopathy, ALS);
- M02 (AChR 0.6 nmol/L against <0.5, a low positive, in SLE/Sjogren overlap; the NCS excludes the
  Sjogren neuropathy that its own minor-salivary-gland note discusses).
Applied without a note to M01, M03, P03 and RS14, and to RS11 (approved). For RS11 this is a tier
change only, made for consistency with the reviewer's identical S05 ruling.
Reason: per the reviewer's quotation, ABN 2025 makes neurophysiology mandatory in antibody-negative
suspected MG. With a positive RIA the diagnosis is serological, and RNS is good practice but is
not needed to diagnose or to decide management. This reverses October Q7 ("RNS required in 27").
That decision rested on "RNS is the initial neurophysiological test", which is about which test
comes first, not about whether a seropositive patient needs one.
Consequence: every "before AChR antibody testing and neurophysiology" prohibition in a downgraded
case becomes "before AChR antibody testing (and neurophysiology when serology is negative)".

**D3. SFEMG sequence-constraint reason (UNSOURCED-RULE 6, SEQUENCE).** Note: 4382d2ff (M01); class
in 21 cases. The note offers two options: remove the SFEMG step, or reword the constraint. Decision:
reword, and move the SFEMG follow-up after the core work-up (in M01 it is follow-up 0, "Step 1").
The stored SFEMG report stays because the library normal would contradict an AChR-positive patient
(October D13). SFEMG stays optional where RNS is diagnostic (October decision kept). Canonical
reasons:
- labs -> SFEMG: "Serology comes first: with positive AChR antibodies SFEMG is rarely needed,
  while every antibody-negative patient needs neurophysiology, RNS first and SFEMG where expertise
  is available (Jacob 2025)."
- RNS -> SFEMG: "RNS is the initial neurophysiological test; SFEMG is considered when RNS is
  normal and suspicion persists, where expertise is available (Jacob 2025)."
Also fix the RS17 key evidence and the P03 rationale that carry the old wording.

**D4. Outpatient steroid prohibition "above 20 mg/day" (UNSOURCED-RULE 1).** Notes: f70a2727
(P01) and the verdicts of P01, P03, P04, RM11, RM16, RP11, RP12, RP13, RP14, RS12, RS13, RS14,
RS15, RS16, RS17, S01, S02, S03, S04, S05. Present in 25 cases (all except M04, P02, RM13, RM14,
RM15); 0 elsewhere in the dataset.
Decision: delete it everywhere. Replace it per setting (canonical texts in MG.md section 1, S1-S4):
- outpatient generalized: ABN titration as a must (S1), with prohibition P1;
- significant bulbar weakness or admission: inpatient initiation (Evoli 2019) and the ABN
  inpatient titration as a must (S2), with prohibition P2;
- ocular (S05; RS11 approved, unchanged): the ABN ocular protocol (S3), with no prohibition. The
  prohibition is deleted because 20 mg/day is the ocular target, not a ceiling;
- already on steroids or moot (RM11 EPOCH pulses, RS13 on 25 mg): delete the prohibition; the
  must carries the rule.
Reason: the 20 mg/day figure appears in no source. In Fionda 2026 it is only the dose above which
vaccine response falls (prevention statement 4). This reverses the October canonical text (pack
section 4), which had no citation.

**D5. Steroid starting dose (MUST-WRONG).** Class: "10-20 mg/day" in 15 musts (classes_out.txt).
Decision: start prednisone (or prednisolone) 5-10 mg daily. Outpatients increase by 5 mg every
3-5 days to 30 mg daily in generalized MG; doses up to 1 mg/kg, not above 60 mg, only after
specialist discussion; worsening is expected at days 5-10. Inpatients increase by 5 mg on
alternate days, or after IVIG or PLEX from 10 mg by 5-10 mg every second day to 30 mg. Ocular
patients go to 20 mg daily (maximum 0.5 mg/kg, not above 30 mg). Daily dosing, not alternate-day
(ABN 2025 abstract). Keep the drug name the case uses.

**D6. Thymectomy age wording (UNSOURCED-RULE 2, citation swap).** Notes: verdicts of RM11, RM16,
RP13, RS13, RS15, RS16, RS17, S02, S04 (also MGTX citations in M02, RM12, RM14).
Decision: "MGTX 18-65" is the trial's enrolment range, not a recommendation. By age:
- 18-49: "offer thymectomy early, once MG is controlled" (ICG 2020 rec 1a; ABN 2025);
- 50-65: "discuss thymectomy", stating that ICG 2020 found no benefit at 50 or over in the post hoc
  analysis while ABN 2025 advises discussion at 50-65. At 60 and over, also record that the
  Italian flowchart diverts these patients (Evoli 2019);
- over 65 without thymoma: not routinely indicated.
Any thymoma: thymectomy at any age, with oncology referral (ABN 2025; ICG 2020). MuSK MG: not
indicated (ICG 2020). Seronegative MG: not routinely indicated without thymoma (no data, ABN
2025); it may be considered if immunotherapy fails (ICG 2020). This replaces October facts 20 and
Q22 (RS15 "refer at 53"), which rested on the enrolment range read as an indication. Approved
RM14 ("discuss thymectomy after recovery ... MGTX", at 55) is left as it is: the verb is already
"discuss" and the case is approved.

**D7. Pyridostigmine ceiling (UNSOURCED-RULE 3).** Notes: verdicts of P04, RM11 (class: P03,
RM12). Decision: "maximum 360 mg/day, with specialist review above 300 mg/day (ABN 2025)"; delete
"360-480". Evoli 2019 tops out at 90 mg five times daily, which is consistent.

**D8. Respiratory escalation thresholds (UNSOURCED-RULE 4).** Notes: verdicts of RP11, RS12, RS14,
RS17 (class: 16 cases carry -30/40 or 20/30/40).
Decision: musts, key evidence, criterion rationales and the RS14 respiratory impression use the
ABN criteria (canonical R1 in MG.md). ICU or HDU referral when FVC is below 20 mL/kg or has fallen
by more than 30%, the patient cannot complete a sentence, uses accessory muscles, or cannot clear
secretions. Inpatient care for FVC below 30 mL/kg, a single-breath count below 25, or significant
bulbar symptoms. MIP and MEP are still measured and trended, but carry no numeric threshold.
Reason: the 20/30/40 rule (Lawn 2001) comes from a GBS cohort, and the governing MG guideline
uses FVC and clinical criteria. The reviewer's ruling stands, since the guideline does not say
otherwise. Approved RM14 and RM15 are not changed: their decisions (FVC 16.6 and 12.9 mL/kg)
meet the ABN criterion anyway.

**D9. Beta-blocker absolutes (UNSOURCED-RULE 5).** Notes: 53d0cb94 (P04 contra 4), 51d18b0e (M04
must 7), RP13 verdict (must 2).
Decision: ICG 2020 Table 1 grades beta-blockers "use with caution", so they are reviewed, not
banned or replaced by rule. P04: delete contra 4; must 4 says "if blood pressure treatment needs
intensifying, prefer another class (beta-blockers are used with caution in MG)". M04 must 7: "Once
she is stable, review metoprolol (beta-blockers are used with caution in MG): keep the lowest
effective dose, or switch to a class without neuromuscular effect if weakness persists". RP13
must 2: "ask ophthalmology to consider replacing timolol drops with a non-beta-blocker
glaucoma treatment".

**D10. Unlabelled off-pathway served reports (AVOIDED-MISSING).** Notes: 7f7f43d1 (M03), bfbee1e2
(M02), 8e6fd5cf (P04), verdicts of M04, P02, P03, RM11, RP12, RP13, RP14, RS13, RS16.
Decision: every stored report that answers an order the policy neither asks for nor labels gets a
label. Waste avoided actions:
- levodopa challenge where there are no parkinsonian signs, or at this admission (RS14, RS16);
- timed gait and balance battery;
- `speech_language_evaluation` (a language battery that never assesses swallowing; see D11);
- SSEP, cognitive screen and neuropsychological battery;
- DaTscan, MIBG and olfactory test in established PD (RP12);
- polysomnography when residual AHI is below 5 (P04);
- minor salivary gland biopsy in established Sjogren (M02);
- pelvis and abdomen MRI for known prostate cancer on active surveillance (M03);
- brain or orbit MRI where the ABN trigger is not met and no criterion uses it (RP11, RP12, RP13,
  RS13, RS15, RM11 (re-ordering last week's MRI));
- whole-body FDG-PET for a thymoma, or when no tumour is in question (RP11, S01, S03);
- chest X-ray after a chest CT (RP11, RM13);
- ice-pack test in known MG (M04, RM14);
- orthostatic blood pressure where there is no autonomic question (RM14, RM15, RM16);
- SFEMG after a diagnostic RNS with positive VGCC (P02);
- cervical spine CT after a cervical MRI (RS16);
- repeat muscle biopsy (RS14; one was done last month).
One harm label: invasive coronary angiography in stable, asymptomatic coronary disease (RS16). It
is an invasive procedure with iodinated contrast (ICG 2020 Table 1) and has no indication (AHA/ACC
2023 chronic coronary disease guideline).
Optional criteria instead of labels: the RP12 levodopa challenge (it documents that the bulbar
deficit does not respond; the reviewer offered optional), the RP14 brain MRI with MRA (APS stroke
question), the RS16 brain and cervical MRI (cervical myelopathy), the RS12 brain MRI (brainstem
small-vessel differential, already "if obtained"), and the RM16 SFEMG.
The notes say "remove the step" (M03). That is read as labelling: the stored report stays, so a
wasted order is not answered by a contradicting library normal (October practice), and it moves
to the end of the follow-up list. M04: remove the cardiac-monitoring waste label, since the musts
send her to ICU or HDU. Approved RM13, RM14 and RM15: add only these labels, an additive change
kept consistent with the other 27 cases.

**D11. Swallow assessment (UNSATISFIABLE, vocab gap).** Notes: 6e3dd7da (M04), 8e6fd5cf (P04 part),
verdicts of RM11, RP12, RP13, RP14, RS12, RS13, RS14, RS15, RS16, RS17, S01, S02, S03, S04.
Decision: CENTRAL (vocabulary), with an interim fix. Neither vocabulary has a swallow term.
`speech_language_evaluation` is defined as motor speech and language, so rewriting it into a
swallow study would contradict the catalogue the agent reads. That is declined, and it is labelled
waste (D10). The musts asking for an SLT swallow assessment stay: ROUND_POLICY rule 4 places
specialist input in the musts, and a recommendation satisfies them. Request a
`swallow_assessment` term (CENTRAL C1). Once it exists, add a recommended criterion
`action-swallow-assessment` with a stored bedside swallow report in every case whose musts demand
one (the list is in MG.md section 4).

**D12. ECG before pyridostigmine (NEW:missing-action).** Notes: verdicts of RM16, RP11-RP14,
RS12-RS17, S01-S05.
Decision: every new diagnosis that starts or continues pyridostigmine gets the ECG in the
pyridostigmine must (canonical M1) and a recommended `action-baseline-ecg` criterion
(`analyze_ecg`, no arguments). Where the case stores no ECG, add a plain 12-lead report
consistent with the patient (heart rate, medicines). A case fallback ECG may be promoted to
`initial_tool_outputs.ecg`. This is done so that no must demands an unscored study. Excluded:
LEMS cases (ECG already required), crisis cases on pyridostigmine (M04, RM14, RM15) and the
approved RS11.

**D13. Pre-treatment screening and steroid monitoring (pretreatment-screening-missing).** 16
verdicts. Decision: add canonical text S5 to the immunosuppression must of every non-approved case
that plans steroids or a steroid-sparing agent. It covers HbA1c, lipids, BP and weight before
steroids; hepatitis B and C serology, TB (IGRA) and HIV before immunosuppression; vaccinations at
least four weeks before (HPV up to 45 in women, Fionda 2026 vaccination statement 3); periodic BP,
glucose, weight and eye checks, with calcium, vitamin D and DEXA (Fionda 2026 prevention
statements 1-2); an ophthalmological check before high-dose steroids in thyroid eye disease or
ocular hypertension (RM16, RP13). In inpatients it is phrased "without delaying urgent treatment".
These are management statements, not tests (as MS-RR N4 handled pre-DMT screening). No criterion
is added.

**D14. Early non-steroidal immunosuppression.** Notes: verdicts of S03, S04, RS12, RS13, RS16,
RP12, RP13. Decision: "start azathioprine early alongside the steroid" where there is diabetes,
ischaemic heart disease, BMI over 25 with insulin resistance, established steroid toxicity, or age
over about 70 (ABN 2025; Fionda 2026 prevention statement 1). Keep TPMT. NUDT15 is kept as
"TPMT (and NUDT15 where available)". The reviewer remark on RP14 is DECLINED in that part, because
CPIC 2019 recommends NUDT15 genotyping before thiopurines. It is not wrong, only absent from the
two MG guidelines.

**D15. IVIG and pre-operative rescue (MUST-WRONG).** Notes: verdicts of S01, S03, RS12, RS14, RP11.
Decision: IVIG is dosed by ideal body weight (Devine), after hepatitis B and C serology and an IgG
level. The dose is 1 g/kg over 2-3 days for significant bulbar weakness without ventilatory
failure, and 2 g/kg in crisis or impending crisis (ABN 2025). Pre-operative IVIG or PLEX is given
on clinical indication; optimum MG control comes before surgery even at the cost of delay. S03:
about 146 g (IBW 73 kg at 178 cm), not 175 g. Workers recompute every stated gram dose.

**D16. Cell-based panel in seronegative MG (TIER, missing alternative).** Notes: b093a449 (P01),
verdicts of P01, RP14, P04.
- P01, RP14: the CBA criterion (`action-7-interpret-labs`) becomes required, with `panels:
  [clustered_AChR_cell_based]`, and `clustered_MuSK_cell_based` is added once CENTRAL C2 lands.
  LRP4 becomes its own recommended criterion (`action-lrp4-antibody`, panels `[anti_LRP4]`), never
  an equivalent. The CBA is added to the stop rule.
- P04: split the stored panel into an LRP4 panel and a cell-based clustered AChR (and clustered
  MuSK) panel, so each order receives only what it names. LRP4 stays required, since the label
  rests on it. The CBA becomes a new recommended criterion (`action-cell-based-panel`). The OR
  equivalence the reviewer asked for is declined: its premise was that an agent ordering clustered
  AChR would see the LRP4 result, which is a serving artefact that the split removes.
Divergence recorded in the rationale: ABN includes LRP4 in the panel; Fionda 2026 statement 6 says
LRP4 "may be tested".

**D17. Mediastinal MRI alternative (missing-alternative).** Notes: verdicts of P04, RM11, RP11,
RP12, RP13, RP14 (class: M04, P03, RM12).
Decision: add `order_body_imaging{study: mediastinum_MRI, contrast: true}` to every thymic-imaging
criterion that lacks it (ABN accepts CT or MRI). Where the CT shows a thymoma, hyperplasia or
another mediastinal finding (P03, RP11, RM12, RM11 residual lymphoma node), first store a
consistent MRI report, so the library normal never answers. Approved RM14 and RM15 (optional
criteria) are not changed.

**D18. Respiratory function tier.** Notes: verdicts of RP12, RS12, S01, S03.
Decision: required when there is significant bulbar weakness (dysphagia, choking, aspiration,
nasal regurgitation, weight loss), breathlessness, or a must that acts on the measured values.
Recommended for mild bulbar fatigue alone (chewing, nasal voice) in outpatients, and optional in
ocular MG. A required criterion joins the stop rule. Measured list: MG.md C11.

**D19. Stop rules keyed on a tool name (STOP-RULE).** Notes: verdicts of M04, P01, P02, P04, RM11.
Decision: ALREADY-FIXED in the data. `required_before_assessment` lists criterion ids, and those
criteria carry their `test_type` or `panels`; the scorer keys on criterion ids. The app shows only
the tool name (CENTRAL.md item 3). What still applies is done: the P01 CBA joins the stop rule,
and each tier change updates its stop rule. M04: the initial `specialized_test` output becomes the
respiratory function report and the RNS moves to a follow-up (NEW:first-order-result), so the
"Initial workup" no longer shows a test the policy calls waste.

**D20. MG-RP13 label (DX-CERTAINTY, synonym-icd).** Note: RP13 verdict. Decision: change accepted[0]
to "New-onset AChR antibody-positive generalized myasthenia gravis (MGFA class IIb) superimposed
on long-standing ptosis and ophthalmoparesis previously labelled CPEO; a coexisting mitochondrial
myopathy is not excluded without muscle biopsy". This is the reviewer's wording plus "without
muscle biopsy", which stays true once the optional biopsy (below) exists. CPEO stays out of
`rejected`.
The muscle biopsy is added as an optional criterion. Its stored report shows no ragged-red fibres,
no excess of COX-negative fibres for age, and no mtDNA deletion on long-range PCR. The CPEO
differential then says "muscle biopsy, if obtained, shows no mitochondrial pathology".
CENTRAL C4 covers the synonyms. Add "AChR antibody positive myasthenia gravis" and "seropositive
myasthenia gravis"/"seropositive MG", scoped to AChR-positive cases. Drop G70.01 from G70.00 cases
(see D21).

**D21. G70.01 in stable cases (synonym-icd).** Note: RP13 verdict. Decision: CENTRAL C4, condition
wide. Stop granting G70.01 to the 27 G70.00 cases and keep it only for M04, RM14 and RM15.
ICD-10-CM G70.01 means "with (acute) exacerbation", which a new or stable presentation is not.
This reverses the scoring part of October Q2 ("stable cases still accept G70.01"). The code is a
weight-0 component under scorer v2, so the change is about correctness, not score.

**D22. MG-RS14 scenario (SCENARIO, DIFFERENTIAL, REPORT-CONTRADICTION).** Note: RS14 verdict. The
note offers two options. Decision: keep the PSP-type signs (the case is seeded from a real report,
PMC3148447) and make the case coherent.
- Add to the exam the fatigability that the musts assert: speech becomes more nasal and less
  intelligible on sustained counting, and tongue and jaw weaken with repetition. No ptosis.
- Replace the PSP differential entry with "coexisting atypical parkinsonism (PSP-like): possible,
  not excluded". It cites the supranuclear-pattern downgaze, astonished facies, frontal release
  signs, freezing, modest levodopa response and dysexecutive features, and notes that a normal
  midbrain-to-pons ratio does not exclude PSP. Keep the statement that it does not explain the
  relapsing fatigable bulbar weakness.
- Remove "progressive supranuclear palsy" and "PSP" from `rejected` (a possible coexisting
  condition is never rejected). Check the change with `DiagnosisCriterion.matches`.
- State that the brisk masseter reflex fits the upper motor neuron or frontal picture of the
  parkinsonian syndrome rather than MG, and that the isolated left upper limb areflexia is not
  explained by MG and needs separate assessment.
- The brain MRI becomes recommended. Its report gets findings and additional observations that
  agree with the impression, and a stated `contrast_used` (check with `mri_probe`).
- Remove the " L" appended to the MIP and MEP results.
- Musts: rituximab screening (HBV, HCV, HIV, VZV serology, IGRA, CD19 count, serum
  immunoglobulins; vaccinations at least four weeks before; lamivudine prophylaxis if HBsAg or
  anti-HBc is positive). TORCH is omitted because it is a pregnancy screen and irrelevant in a
  75-year-old man. FcRn antagonist escalation (rozanolixizumab is approved for MuSK-positive
  generalized MG). Levodopa continued via the nasogastric tube without interruption.
- Citations: Sanders 2016 for the MuSK pyridostigmine and PLEX statements; ICG 2020 for rituximab
  and for no thymectomy.

**D23. MG severity scales.** Notes: 7f7f43d1 (M03), verdicts of RP11 and RP13. Decision: FIXED as a
must, applied to the class (every non-approved MG case, LEMS excluded): "Record the MGFA class
(here <class>) and a baseline MG-ADL, with QMG where available, to follow treatment against the
ABN goal of MG-ADL 0-1 (Fionda 2026 severity statements 1-2; Jacob 2025)". No action criterion:
MGFA and MG-ADL are scored from the history and examination already in the patient block. QMG
would need a catalogue term whose prose cannot name the disease. This is not requested centrally
(noted in MG.md section 5).

**D24. Citation swaps (Sanders 2016, MGTX).** Notes: verdicts of RS14, RS16, S01, S03, S05 and the
thymectomy notes. Decision: thymoma thymectomy cites ABN 2025 and ICG 2020. Non-thymomatous
thymectomy cites ICG 2020 rec 1a and ABN. Ocular MG cites the ICG 2020 ocular section. Early
steroid-sparing therapy cites ABN. MuSK rituximab and no-thymectomy cite ICG 2020. Sanders 2016
stays for the MuSK pyridostigmine and PLEX statements and for general management where nothing
newer is cited. `[Wolfe_2016]` keys stay only on thymectomy statements.

**D25. Iodinated contrast caution.** Note: 9a202945 (P04). Decision: FIXED narrowly. The P04 thymic
CT rationale gains "iodinated contrast is used with caution in MG (ICG 2020 Table 1) and does not
replace the indication". The P04 must listing MG-worsening drugs adds "iodinated contrast (used
with monitoring)". The CT action is not changed, as the note asks. The other cases already have
the pack rule; no churn.

**D26. TRAb in the S02 thyroid criterion.** Note: S02 verdict. Decision: `required_arguments.panels`
becomes `[anti_AChR, TSH, TRAb]` (single alternative), because the expected evidence and the Graves
orbitopathy differential rest on TRAb (Evoli 2019: thyroid antibodies in all). Workers confirm
with a served probe that TRAb is a stored row. RM16 (TRAb-positive Graves) gets the same check: if
its evidence cites TRAb, add TRAb to its alternatives.

**D27. Unsourced figures in S05.** Note: S05 verdict. Decision: contra 3 becomes "Do not take a
normal RNS as evidence against ocular MG; RNS is often normal in purely ocular disease, and SFEMG
of a facial muscle is more sensitive". Remove "~80%" (ice-pack sensitivity) and "~50%"; use Evoli
2019 instead (improvement of more than 2 mm is positive; NPV 94%). No other MG case carries these
figures (grep).

**D28. Other case-specific musts.**
- RP14: repeat AChR and MuSK in about 6 months (Evoli 2019); repeat neurophysiology at a
  specialised centre if the case stays triple seronegative or borderline, with exclusion of mimics
  (Fionda 2026 statement 8); the thymectomy sentence per D6.
- RS16: an atorvastatin statement (continue for the coronary disease; review if weakness worsens;
  statins are used with caution, ICG 2020 Table 1); the drug check goes from optional to
  recommended.
- RP12: contra 4 talks about ptosis and diplopia the patient does not have; it becomes "fatigable
  bulbar weakness".
- RP11, S01, S03: thoracic oncology referral for the thymoma (ABN).
- RS14: as in D22.

**D29. Literature (LIT).** Note: b3dbe81b (M03). Decision: ALREADY-FIXED by class LIT (commit
393c547e). No MG case stores a literature output or criterion (grep, 17 Nov 2026).

**D30. Approvals.** Notes: RM13, RM14, RM15, RS11 verdicts with no comment. NO-ACTION on the notes.
Class changes applied in these approved cases: D10 labels (RM13, RM14, RM15) and the D2 tier (RS11).
