# FEPI-TEMP: condition plan, November 2026 round

Lead plan for the 30 `focal_epilepsy_temporal` cases. Read `ROUND_POLICY.md` (October contract,
still in force; helpers now under `data/review/round-2026-11/bin/`), `NOVEMBER_ADDENDUM.md`, the
October plan `round-2026-10/plans/FEPI-TEMP.md` (its canonical facts 1-20 stay valid unless this
plan says otherwise) and `plans/FEPI-TEMP-decisions.md` (numbered decisions D1-D36, with the
reasons and citations; this plan says what to do). 213 notes, all R1, all 30 cases. No
FEPI-TEMP case is approved. Base for workers: HEAD 71517e55 (LIT and MRI-CONTRAST done).

Workers: edit only through `case_io` load/save; after every case run
`uv run python -I data/review/round-2026-11/bin/perfect_agent.py CASE -v`,
`uv run python -I data/review/round-2026-11/bin/case_io.py check CASE`, and
`mri_probe.py CASE` after any MRI edit. Write the case log with every note id of section 3.
English, American spelling as the cases use, no em dashes, no review text in `metadata`.
Keep each `criterion_id`; new criteria get the ids given here. New criteria and avoided actions
carry one bracketed key. Every new stored report is case-specific (age, sex, side, timeline) and
must not copy numbers from another case.

## 1. Governing guidelines and canonical facts

October facts 1-20 (October plan section 1.2) and the pack (`criteria_packs/FEPI-TEMP.md`) stay,
with these November changes:

1. Diagnosis certainty: DNET, ganglioglioma, FCD and FCD IIIa are histological diagnoses (WHO
   CNS5 2021; ILAE FCD 2011/2022). Without tissue the label says "presumed" (tumours) or
   "suspected" (FCD) and carries no CNS WHO grade.
2. Tissue: no standalone diagnostic brain biopsy when clinical, MRI and EEG findings are
   concordant; histology comes from a therapeutically indicated resection (D3, D4).
3. HLA-B*15:02 (and HLA-A*31:01) testing is tied to the decision to start carbamazepine or
   oxcarbazepine in at-risk ancestry [CPIC_2018]: a prohibition, never an unconditional must (D6).
4. Valproate: not first-line for focal epilepsy; in anyone who could become pregnant it is
   avoided unless nothing else works, within a pregnancy prevention programme [NICE_NG217_2025],
   [AAN_AES_SMFM_2024], FDA boxed warning, MHRA/EMA 2024. Case text states the clinical rule,
   not the UK procedure (D7).
5. Unilateral manual automatisms are usually ipsilateral and lateralize weakly alone; dystonic
   posturing, late forced version, clonic jerking and Todd paresis are contralateral
   [Lateralization_2005] (D10).
6. Prolactin is interpretable only 10-20 minutes after a suspected seizure and never separates
   seizure from syncope [AAN_prolactin_2005]; P05's 22-minute sample is at most supportive.
7. Routine EEG in pregnancy: neither hyperventilation nor photic stimulation [IFCN_ILAE_EEG_2023].
8. Pregnancy test in a woman of childbearing age at a first ED seizure or before an ASM start or
   switch [ACEP_seizure_2004]; required by the valproate and topiramate PPPs.
9. Levetiracetam and topiramate have laboratory reference ranges, not established therapeutic
   ranges: interpret a level with dose, timing, adherence and renal function.
10. Primary ASM prophylaxis in seizure-free brain-tumour patients is not recommended
    [SNO_EANO_prophylaxis_2021].
11. Intracranial EEG is not useful in diagnosing hypothalamic hamartoma epilepsy; neuropsychology
    and endocrinology are part of the presurgical work-up [HH_consensus_2026].
12. Enzyme inducers lower lacosamide exposure by about 15-25% [Lacosamide_label].
13. Eclampsia can present without hypertension or proteinuria and up to 6 weeks postpartum
    [ACOG_HTN_2020]; postpartum CVT needs venous imaging when suspected [AHA_CVT_2024].
14. Imaging before LP in suspected encephalitis with impaired consciousness may be CT or MRI;
    CSF and acyclovir are not delayed for MRI [IDSA_enc_2008, ABN_enc_2012].
15. The stop rule is diagnostic completeness only; treatment is assessed in the musts and is
    never delayed by the scoring (no treatment action exists).

## 2. Classes

Counts are measured with scripts in `work/scratch/fepi-lead/` (`measure*.py`, `av_tissue.py`).

### LIT (73 notes, 30 cases) - D1
Done by commit 393c547e: 0 literature outputs or criteria in the 30 cases (verified). Residue to
delete: `metadata.case_body_concerns` lines in P02 and P03 that describe a literature step.
Rule every LIT note FIXED: "class LIT, commit 393c547e; no literature output or criterion left".
Other conditions: done centrally (416 cases).

### MRI-CONTRAST (11 notes, 11 cases) - D2
Verified: M05, P02, RM02, RM03, RM04, RP01, RP03, RS01, S02, S03, S06 have initial
`contrast_used: false` and a `request_contrast_mri` follow-up with `true`. Rule FIXED: "class
MRI-CONTRAST, commit 71517e55". M04 adds a new pair (class M04 below). Run `mri_probe.py`.

### BIOPSY (36 notes, 23 cases with notes; applied to 29) - D3
Measured: 28/30 cases store stereotactic and open biopsy follow-ups (not P04, RP02); 0 avoided
tissue actions in the whole dataset (also NMDAR-ENC 18, SE 6, GLIO-HG 3 cases: CENTRAL 6).
Fix in every case except RP03: two avoided actions, severity `harm`:
- `avoid-harm-stereotactic-biopsy`: `obtain_tissue_diagnosis {procedure: stereotactic_biopsy}`
- `avoid-harm-open-biopsy`: `obtain_tissue_diagnosis {procedure: open_biopsy}`
Rationale (fill the slot; one sentence, case-specific):
`A standalone <stereotactic|open> biopsy of the <lesion/site> adds procedural risk (hemorrhage, infection, deficit) without diagnostic gain: <the concordant clinical, MRI and EEG findings | the positive serum LGI1 antibody | the positive CSF HSV-1 PCR | the video-EEG> establish the diagnosis, and any histology comes from a therapeutically indicated resection.`
Case variants: M05 adds hemorrhage risk of a cavernoma; RS01 the hypothalamus; RS02 surgery under
anaesthesia at 33 weeks; P03 "the events are functional seizures on video-EEG"; tumour cases see
TUMOUR. Citation per lesion (one key): HS and MRI-negative `[ILAE_MRI_2019]`; FCD, tumours
`[Blumcke_2017]`; M05 `[Cavernoma_2017]`; P02 `[Graus_2016]`; RP01 `[IDSA_enc_2008]`; P03
`[ILAE_PNES_2013]`; RM02 `[TSC_2021]`; RS01 `[HH_consensus_2026]`; RP05 `[Encephalocele_2015]`.
Resection (own extension, D3): `avoid-harm-resection`: `obtain_tissue_diagnosis {procedure:
resection}` severity `harm` in M01, M02, M03, P01, P02, P03, P05, RM01, RM02, RM03, RP01, RP02,
RS02, RS03, RS05, S01, S04, S05, rationale
`No surgical indication at this encounter: <the epilepsy is newly diagnosed and untreated | controlled | the seizures are acute symptomatic | the events are functional>; resection is considered only after presurgical evaluation of drug-resistant epilepsy.`
cite `[Kwan_2010]`. Never label resection where surgery is part of the plan (M04, M05, RM04, RP03,
RP04, RP05, RS01, RS04, P04, S02, S03, S06). Check that no criterion matches these calls.

### TUMOUR (5 notes; applied to S02, S03, S06, RM04, M04) - D4
Replace the surgical must with:
`Refer for multidisciplinary epilepsy-surgery evaluation aiming at complete (maximal safe) resection of the <site> lesion, which also gives the histological diagnosis; a standalone biopsy only if resection is unsafe or tissue would change management.`
S02 and S03 add the neuropsychology clause of NEUROPSY; M04 and RM04 keep their language-mapping
clause.

### TEE (3 notes, 3 cases) - D5
RM02, RP02, RS05: add `avoid-waste-tee`: `order_echocardiogram {echo_type: TEE}` severity
`waste`, rationale `No embolic, valvular or structural question that needs a transesophageal study; <case reason>.`
cite `[NICE_NG217_2025]` (RP02 `[ESC_PE_2019]`, RM02 `[TSC_2021]`). Leave TTE as it is.

### HLA (5 notes; 7 cases) - D6
In M02, M04, M05, P04, RS05, S04, S06 delete the must `Test HLA-B*15:02 before any carbamazepine
or oxcarbazepine.` and add the prohibition:
`Do not start carbamazepine or oxcarbazepine without first testing HLA-B*15:02, given <his|her> <East Asian|South Asian|Southeast Asian> ancestry (HLA-A*31:01, which predicts carbamazepine hypersensitivity in any ancestry, can be tested at the same time).`
Delete any existing prohibition that says the same less well. KCE mentions of HLA: say "before
carbamazepine or oxcarbazepine". Do not touch ancestry (it is in demographics).

### VPA (1 note; 19 prohibitions) - D7
Replace the MHRA-procedure prohibition in M01, M02, M03, M04, M05, P01, RM01, RM03, RM04, RP02,
RP05, RS03, RS05, S01, S02, S03, S04, S05, S06 with, for women:
`Do not start valproate: it is not first-line for focal epilepsy, and in a woman who could become pregnant its teratogenic and neurodevelopmental risks restrict it to cases where nothing else works, within a pregnancy prevention programme.`
for men:
`Do not start valproate: it is not first-line for focal epilepsy, where lamotrigine or levetiracetam is preferred.`
RS01's paternal-risk must stays.

### LABSIG (15 notes; 21 cases with null abnormal rows) - D8
Fill `clinical_significance` (one short sentence, no case diagnosis, no drug prescription) on:
M03 vitamin D 23 ("Below range; documented vitamin D insufficiency on supplementation; relevant to
bone health on long-term ASM therapy"); P02 sodium 126 ("Moderate hyponatremia; needs assessment
of volume status, osmolality and urine sodium; carbamazepine can contribute"), chloride 94, LGI1
IgG 1:320 ("Positive neuronal surface antibody by cell-based assay; supports an antibody-mediated
process in the appropriate clinical setting"); P05 prolactin (fact 6 wording); RM02 valproate 38
("Below the reference range with reported missed doses; review adherence"); RM02 TSH 4.8 only if
out of range; RM03 phenytoin total 4.2 and free 0.5 ("Subtherapeutic total and free phenytoin;
consistent with missed doses"), CK 485 and lactate 3.8 ("Consistent with a recent convulsion"),
WBC 12.8 (same); RM04 Hb, MCV, ferritin, TSAT ("Microcytic anemia with low ferritin: iron
deficiency; persistent despite oral iron"); RP01 CRP 18.4, WBC 12.4, neutrophils 78% ("Mild
nonspecific inflammatory response"), glucose 168 and HbA1c 6.8 ("Hyperglycemia on dexamethasone"),
RP02 D-dimer 4850 ("Markedly raised; with the clinical picture, requires urgent imaging for venous
thromboembolism"), levetiracetam 8.2 ("Below the laboratory reference range; no established
therapeutic range: interpret with dose timing, adherence and renal function"); RP03 levetiracetam
5.9 (same wording plus reported missed doses), TSH 6.8 ("Raised TSH on checkpoint inhibitors:
repeat with free T4"); RP04 sodium 134 ("Mild hyponatremia on carbamazepine with prior
oxcarbazepine-induced hyponatremia: repeat and monitor"); RS02 levetiracetam 5.8 ("Below range
after missed doses and with increased clearance in the third trimester"); RS03 bicarbonate 21
("Mildly low; topiramate causes a normal-anion-gap acidosis: recheck before any dose increase"),
topiramate 3.2 ("Below the laboratory range; consistent with 100 mg/day and no missed doses;
not a measure of adequacy alone"); RS04 sodium 134 ("Mild hyponatremia on high-dose
carbamazepine: monitor during changes"), Hb 11.4/MCV 78 if anemia is in the KCE. Leave trivial
borderline rows null (glucose 102-142 without diabetes question, Mg 2.3, S05 bicarbonate 21,
S02/S03 MCV). Fix the KCE and musts these values need (RS03: topiramate level KCE no longer says
missed doses; RP02 KCE "low level" qualified). Log: FIXED, "CENTRAL 3 display: null shown as
none".

### NEUROPSY-FLAG (3 notes) - D9
M05, P01, P04: ALREADY-FIXED (rows already `abnormal: yes`; no global flag) + CENTRAL 3.

### LAT (4 notes; 13 cases) - D10
Flip the automatism hand to the focus side in every mention in M01, M02, M04, M05, RM02, RM04,
RP03, RP04, RP05, RS01, RS05, S01, S06 (grep `left hand|left-hand|right hand|right-hand` in the
whole case, including EEG/video-EEG semiology, KCE, differential, red herrings, chief complaint).
Keep contralateral signs as they are (RM04 right head version and right arm clonic jerking).
RP03: the slow head turn flips with the hand. Do not flip tongue-bite side or Todd paresis. A KCE
about the sign uses:
`<Left|Right>-hand automatisms are usually ipsilateral to the onset but lateralize weakly on their own; localization rests on the concordant MRI and EEG.`
M04 also: interictal sharp waves to the left mid temporal region (phase reversal T3, field to T5
and F7) in EEG findings, impression and criterion evidence; KCE adds "the epileptogenic zone is
defined at presurgical evaluation".

### DXCERT (labels, 9 cases) - D11
New `accepted[0]` (do not touch synonyms after it; CENTRAL 2):
- S02: `Focal epilepsy of right temporal lobe origin due to a right mesial temporal low-grade glioneuronal tumor (presumed DNET), with a focal-to-bilateral tonic-clonic seizure`
- S03: `Focal epilepsy of right mesial temporal lobe origin due to a low-grade glioneuronal tumor (presumed DNET)`
- S06: `Focal epilepsy of left temporal lobe origin due to a left inferior temporal low-grade glioneuronal tumor (presumed DNET)`
- RM04: `Focal epilepsy of left temporal lobe origin (lateral neocortical TLE with auditory aura) due to a left superior temporal gyrus low-grade epilepsy-associated tumor (presumed ganglioglioma or DNET)`
- M04: `Focal epilepsy of left temporal lobe origin (suspected focal cortical dysplasia)`
- P04: `Drug-resistant focal epilepsy of right temporal lobe origin, nonlesional on 1.5T epilepsy-protocol MRI (3T MRI not tolerated)`
- RP03: `Focal epilepsy of left temporal lobe origin secondary to left temporal melanoma metastasis`
- RS01: `Drug-resistant focal epilepsy with left temporal lobe seizures and left mesial temporal sclerosis in a patient with a hypothalamic hamartoma and gelastic seizures (dual pathology)`
- RS02: `Focal epilepsy of right temporal lobe origin with right mesial temporal sclerosis and presumed remote calcified neurocysticercosis, presenting at 33 weeks gestation`
Align every other mention (KCE, musts "probable DNET", differential, metadata difficulty text) to
the same certainty; no "CNS WHO grade" anywhere in RM04; keep ganglioglioma a `moderate`
differential in S02, S03, S06 and RM04 (DNET there).

### DIFF (8 notes; applied to the cases listed) - D12
Keep the likelihood; rewrite key_features so no test is said to exclude what it cannot:
- PNES, no habitual event captured (M01, M02, M04): `<features> make PNES unlikely as the explanation of these events; coexisting functional seizures cannot be excluded without capturing a habitual event, so video-EEG is indicated if the events change or persist despite treatment.`
- PNES with a captured event (M03): `The ambulatory EEG recorded a habitual event with right anterior temporal ictal onset; this makes PNES unlikely as the explanation, although coexisting functional seizures are not excluded.`
- P05 syncope: `Considered after a slump with jerking and a paternal cardiac death; highly unlikely after a normal ECG, Holter, echocardiogram and tilt test, epileptiform discharges on EEG and right HS on MRI; an intermittent arrhythmia is not categorically excluded and would be reconsidered if events change.` PNES entry: drop the prolactin argument.
- RM03 NCSE: `GCS 8 after lorazepam improving to 13 within 45 minutes and a later routine EEG without seizures make ongoing NCSE unlikely; it cannot be excluded for the earlier obtunded period, so urgent (continuous) EEG is needed if consciousness stops improving.`
- RP03 ICI encephalitis: `Normal CSF cells and negative neuronal antibodies make it unlikely; the enlarging metastasis explains the seizures; reconsider if symptoms progress or fail to improve with seizure and tumor treatment.`
- RS02 eclampsia (differential and KCE[0]): `A convulsion at 33 weeks is treated as eclampsia until proven otherwise; normal blood pressure, urine protein/creatinine, platelets, creatinine and liver enzymes and her habitual aura make it unlikely, but atypical eclampsia without hypertension or proteinuria occurs, so obstetric monitoring continues.`
- RS03 CVT: `Postpartum seizure with headaches raises it; normal flow voids on routine MRI are not enough, and MR venography shows <the stored normal result>.`
- RS03 late postpartum eclampsia: `Possible up to six weeks postpartum; normal blood pressure, platelets, renal and liver tests and urine protein/creatinine and her habitual aura make it unlikely; serial blood pressure at the postpartum review.`

### KCE (5 notes) - D13
M02 KCE[2]: `Two morning awakenings with tongue bite and muscle soreness suggest possible nocturnal convulsive seizures.` and must[5] "given possible nocturnal convulsions". RM01 KCE[4]:
`CT shows the catheter in place and no hydrocephalus, which makes shunt failure less likely but does not exclude it; comparison with prior imaging and neurosurgical review are needed if headaches or cognitive change persist.`
P05 KCE[5], labs criterion evidence and PNES differential:
`The ED prolactin of 48 ng/mL was drawn 22 minutes after the convulsive episode, just outside the 10-20 minute window, so it is at most supportive; prolactin does not separate a seizure from syncope or exclude PNES.`

### TIMING (4 notes) - D14
RM03 7d9daed6, RP01 03911b8d, S01 e1e2f67a: NO-ACTION + CENTRAL 4 (verify the musts say "without
waiting"; RP01 and RM03 already do; S01 adds nothing). RP02 78946c3e: FIXED by the RP02 entry.

### STOPSUB (2 notes) - D15
P01 8e90d267, RP01 adaf74ab: ALREADY-FIXED (criteria carry `eeg_type`) + CENTRAL 3.

### PREG (1 note; 10 cases) - D16
New criterion `action-labs-hcg`, `recommended`, `interpret_labs {panels: ["beta-hCG"]}`, label
`Pregnancy test (beta-hCG)`, evidence `Serum beta-hCG negative.`, rationale case-specific
(first seizure in a woman of childbearing age / before starting or switching an ASM / valproate
or topiramate PPP), cite `[ACEP_seizure_2004]` (RM02, RS04 `[MHRA_VPA_2024]`, RS03
`[MHRA_TPM_2024]`). Stored data: a `beta-hCG` panel in the initial labs with one row
`Beta-hCG (serum)` `<5 mIU/mL` (ref <5), not abnormal. Cases: M01, M02, P01, RP05, RM02, RS03, RS04,
S02, S04, S06 (S02 and S06 already hold a pregnancy row: move it into a `beta-hCG` panel, do not
duplicate). Check with a served-answer probe that the hCG order gets that panel and the old lab
orders still get theirs. Not in the stop rule.

### NEUROPSY (3 notes) - D17
RS01: new `action-neuropsych-presurgical` `recommended` `order_specialized_test {test_type:
neuropsych_battery}` with a new stored follow-up (trigger `request_neuropsych_for_surgical_evaluation`):
22-year-old right-handed man, prior hypothalamic Gamma Knife at 5, left HS: verbal memory below
average (left temporal), processing speed and executive weaknesses, no global impairment; in a
neuropsychologist's voice; cite `[HH_consensus_2026]`. S02 and S03 surgical must adds:
`presurgical evaluation including neuropsychology (verbal and nonverbal memory) and, where the planned resection makes it relevant, language lateralization (fMRI or Wada); left-handedness does not establish language dominance.`

## 2b. Case-specific fixes (decisions 18-35)
Listed in the per-case index; canonical wording is in the decisions file entry named there.
## 3. Per-case index (all 30 cases; none approved)

Ruling per note (full note id), then the class findings that apply to the case without a note. "LIT" = FIXED by class LIT, commit 393c547e (checked: no literature output or criterion left). "MRI-CONTRAST" = FIXED by class MRI-CONTRAST, commit 71517e55 (checked: plain initial `false`, gadolinium follow-up `true`).

### FEPI-TEMP-M01 (approved: no)
- `715be7bd-99c0-4306-ace6-35f36886488f`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- `017610be-8f4d-4f18-b40b-4538cc9f7ca2`: FIXED (LAT D10): automatisms to the right hand everywhere
- `deb665fd-f57b-4d3a-a28a-39ec528c65be`: FIXED (DIFF D12): PNES canonical, no habitual event captured
- `b0e1e671-a2d5-4822-a52f-e87b73a16b87`: FIXED: LIT
- `9126bbdf-436b-41c6-8ba6-1f9723408419`: FIXED: LIT
- Class findings: LAT; DIFF; BIOPSY+resection; VPA (woman); PREG.

### FEPI-TEMP-M02 (approved: no)
- `68819f64-51b1-4df7-8ddb-cb3f0f0cf11f`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- `ad4f9105-2741-4642-bee3-f507472e8392`: FIXED (LAT D10): automatisms to the right hand
- `9c483898-d516-443c-b6ad-e5f304522a9e`: FIXED (DIFF D12): PNES canonical
- `6a18310d-1242-4969-86c7-6cc04f00cf74`: FIXED (HLA D6) must -> prohibition; ancestry part DECLINED (demographics: East Asian)
- `adb731fc-f3f8-46af-bfc1-d1cc3f2a018d`: FIXED (KCE D13): "possible nocturnal convulsive seizures" in KCE[2] and must[5]
- `5aff7824-b49d-4c75-8e8c-6ef02eb10773`: FIXED: LIT
- `6c227c22-b10f-4265-9661-0a9fc2adb915`: FIXED: LIT
- Class findings: LAT; DIFF; KCE; HLA; BIOPSY+resection; VPA (woman); PREG.

### FEPI-TEMP-M03 (approved: no)
- `e2fbf6a4-39c1-4469-85aa-dcd37580d391`: FIXED: LIT
- `1e078577-f312-417f-8439-e2127a1f8fc0`: FIXED: LIT
- `795145e1-3cd1-4ef0-a680-d36705bdd7d6`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- `dad7c7ae-bbb8-4f18-a287-83134b428b3b`: FIXED (LABSIG D8, D35): vitamin D row filled; vitamin D must; CENTRAL 3 display
- Class findings: DIFF (PNES captured-event wording); BIOPSY+resection; VPA (man); LABSIG vitamin D.

### FEPI-TEMP-M04 (approved: no)
- `177debf6-f444-4b6c-945e-9f94efdf9d91`: FIXED: LIT
- `d0c253aa-31b9-4db7-9fda-b1c1ee4f90dc`: FIXED: LIT
- `925fd6d6-7f90-402c-aaa7-de3c44f1364c`: FIXED: LIT
- `59a8a93b-db9d-4615-ba87-28ac40a7fe0b`: FIXED (D30): outside MRI about nine months ago (HPI, PMH, MRI comparison, red herring)
- `bbebeeda-97cd-42a6-b8fe-1f7823adb728`: FIXED (D30): HARNESS technique line
- `f6c4443b-9d20-4708-9349-8530b2b0bb18`: FIXED (D30, D11): gadolinium pair + recommended contrast criterion; neuroradiology must; label suspected FCD
- `1c67f44f-290e-41a1-a961-7118702d5e11`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open (only if a specific surgical or oncological indication; resection unlabelled)
- `a97c6c3b-d895-47de-aa79-3c13c3c3485a`: FIXED (LAT D10): left-hand automatisms; sharp waves T3 max (field T5, F7)
- Class findings: LAT + EEG location; DXCERT; TUMOUR must wording; DIFF (PNES); HLA; BIOPSY (no resection label); VPA (man); new MRI pair (MRI-CONTRAST procedure, mri_probe).

### FEPI-TEMP-M05 (approved: no)
- `0d700e35-643d-4c9c-afa6-8d8c6ccaad24`: FIXED: MRI-CONTRAST
- `0a5a3164-9cf2-4573-8360-c067b69d8e0a`: ALREADY-FIXED (D9): rows already abnormal=yes, no global flag; CENTRAL 3
- `7148d479-77bd-4754-bce2-729630cc40e0`: FIXED: LIT
- `21261dfe-cf24-4185-83ca-df65a82ea731`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open (cavernoma hemorrhage risk)
- `aa57706a-28a6-407f-bab2-edc1fc2e95ee`: FIXED (HLA D6) must -> prohibition
- `7be21889-a4b5-4953-a95e-c8b44297f004`: FIXED: LIT
- Class findings: LAT (left-hand automatisms with right focus: flip to right); HLA; BIOPSY (no resection label); VPA (woman); neuropsych flag CENTRAL.

### FEPI-TEMP-P01 (approved: no)
- `f2ef4af0-42d0-424f-a3cd-dbee3a6c66c8`: FIXED: LIT
- `1e26e813-0b64-413e-b607-0517a4a75082`: ALREADY-FIXED (D9); CENTRAL 3
- `0e91c265-beaa-4afc-af19-a458dc027b2f`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- `8e90d267-c051-4b33-9403-463e877b4f74`: ALREADY-FIXED (D15): stop rule keys routine and video criteria with eeg_type; CENTRAL 3
- `08546875-590a-4bc8-849b-3c0d02e82d0b`: FIXED: LIT
- Class findings: BIOPSY+resection; VPA (woman); PREG.

### FEPI-TEMP-P02 (approved: no)
- `0e5c9991-05e4-4fe7-a59f-bef6331d206d`: FIXED: LIT
- `06d10635-5ba8-4043-802b-b2be541121ab`: FIXED: LIT
- `0bb5b735-1ad2-447d-9c4e-8da41324bc62`: FIXED (LABSIG D8) + hyponatremia must (D32); CENTRAL 3
- `3f653640-be1d-4bad-98f8-19ce49fafe75`: FIXED (LABSIG D8): LGI1 row filled; CENTRAL 3
- `9b59000c-23d1-4de6-97ae-fcdea37645c1`: FIXED: MRI-CONTRAST
- `322e3ebd-dfea-434f-9649-b87697a0a607`: FIXED (D32): mechanism-based hyponatremia must; osmolality/urine sodium stored + recommended criterion
- `cae950a1-0ca9-4110-ad97-567dc8dd7de1`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open (positive serum LGI1)
- `faf23617-4b58-4ca1-8829-affac45e2dff`: FIXED: LIT
- Class findings: BIOPSY+resection; LABSIG; LIT metadata residue (delete the case_body_concerns literature line).

### FEPI-TEMP-P03 (approved: no)
- `944c307b-fa13-4eea-a39c-90ceb614bc6a`: FIXED: LIT
- `1328f06b-b6af-4382-be72-eb93c653bf39`: FIXED: LIT
- `982692f3-a754-4537-a504-91b05dc61629`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open (functional seizures on video-EEG)
- Class findings: BIOPSY+resection; LIT metadata residue.

### FEPI-TEMP-P04 (approved: no)
- `a0aed3e6-472f-435d-939e-0e47478a0839`: FIXED: LIT
- `9df51056-01f3-444a-b389-db1fea4c2588`: ALREADY-FIXED (D9); CENTRAL 3
- `fbad255d-ca6a-47f3-a44d-515058210db7`: FIXED: LIT
- `f69f3cc3-6b28-4697-b0a5-366d7ada5512`: FIXED: onset and first MRI both "two and a half years ago" (HPI; check PMH)
- `753c02d4-11a1-4f7f-b9ea-5c4be2308dff`: FIXED (DXCERT D11): nonlesional on 1.5T label; CENTRAL 2
- `9ba5595d-d42f-47cd-8a01-b217971c91ef`: FIXED (HLA D6) must -> prohibition
- Class findings: BIOPSY (no stored biopsy; add the two avoided actions anyway); HLA; DXCERT; P04 chronology.

### FEPI-TEMP-P05 (approved: no)
- `254836e2-8323-415c-b295-3083c1dd1279`: FIXED (KCE D13, fact 6): prolactin qualified in KCE, criterion evidence, PNES differential, row significance
- `09eefe19-6ce9-4e14-8599-75f5b7a12030`: FIXED: LIT
- `a2e33c1b-4f34-4c61-b4a3-c95541514c90`: FIXED (DIFF D12): syncope "highly unlikely"
- `300f3229-5325-4b67-a033-4ea5404c337c`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- `4f347644-d944-49ed-b2d0-b560d1825540`: FIXED (D18): ECG optional, out of stop rule (overrides October C8)
- `4076ba14-8e7a-4643-9aa4-462161dfc0ac`: FIXED (D18): video-EEG recommended, out of stop rule
- `3d763637-b1ee-4db1-863c-5850329b81d4`: FIXED: LIT
- Class findings: BIOPSY+resection; DIFF; KCE prolactin; tiers D18.

### FEPI-TEMP-RM01 (approved: no)
- `11aee0f0-8dc2-49aa-9937-5f073e4cc831`: FIXED (KCE D13, D28): KCE rewritten; must on prior-imaging comparison and neurosurgical review
- `60ee35f8-32d4-42ee-915a-87e7b2e71447`: FIXED (D28): pre-MRI valve model, MR conditions, setting record; post-MRI check
- `320a069a-ff3b-42b4-a18a-c643079f983c`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- `000a4e76-590b-436f-9b57-d18db175e019`: FIXED: LIT
- `e7dc96c3-a3cb-4077-8066-4df76f1ef017`: FIXED: LIT
- `4fc551fe-4c6f-45d3-b1d9-250f870392e9`: FIXED: LIT
- Class findings: BIOPSY+resection; VPA (man); KCE; D28.

### FEPI-TEMP-RM02 (approved: no)
- `349818ac-2f2b-4b4a-9b44-07f0c71c61f3`: FIXED: MRI-CONTRAST
- `eb350688-acea-4fea-8d96-6a457f2a5361`: FIXED (LABSIG D8); CENTRAL 3
- `a7f7e00b-aa7b-4562-b8d6-b6a03896a939`: FIXED in part (D29): individual risk-benefit + PPP added; the switch itself kept (NICE NG217 2025, MHRA/EMA 2024): partly DECLINED
- `6bcac12f-192c-4572-8ca4-7f81d37052c6`: FIXED (TEE D5): TEE waste
- `d491c15a-66cd-4ee7-8524-04b9bca052bb`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open (tuber)
- `f675935a-3765-437b-96ca-003faf362a85`: FIXED: LIT
- `ded698de-84b3-4998-b28d-8b67523a04cf`: FIXED: LIT
- `75594d57-a7cd-4ecd-85d8-e0ba2fcde735`: FIXED: LIT
- Class findings: LAT; BIOPSY+resection; TEE; PREG; LABSIG; D29.

### FEPI-TEMP-RM03 (approved: no)
- `819d3efe-c281-43d7-9a51-2ec486fe14b2`: FIXED: LIT
- `f61d914b-5079-48b5-b102-fac71238a2e5`: FIXED: LIT
- `bcf111dd-9317-4c4c-a932-9935174ccda5`: FIXED (LABSIG D8); CENTRAL 3
- `7aac832f-1e7b-44b1-823a-9a441714be1f`: FIXED: MRI-CONTRAST
- `b8774a1b-8338-4c12-97f6-99503d8bf146`: FIXED (D31): second convulsion without recovery when EMS arrived, then lorazepam
- `23af9681-ed87-4a5e-860c-0928b2ef1a84`: FIXED (DIFF D12, D31): NCSE wording; airway, neuro observations, conditional urgent EEG must
- `7d9daed6-c9c0-4268-b7c5-a71f751f7775`: NO-ACTION (D14): stop rule is diagnostic only, musts already say do not delay; CENTRAL 4
- `c180d2db-0209-45f8-86bd-310ef8f3f90f`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open (ECCL)
- `52e4ccf2-240f-4e72-9ac0-f4f2aa206a19`: FIXED (class LIT, commit 393c547e): ECCL literature output removed
- `24bf9bbd-b121-42e9-9386-50a2b872b285`: FIXED: LIT
- Class findings: BIOPSY+resection; VPA (man); LABSIG (phenytoin, CK, lactate); DIFF; D31.

### FEPI-TEMP-RM04 (approved: no)
- `0cf4c2e3-7f67-4fdd-a834-f306ea456aae`: FIXED: MRI-CONTRAST
- `8388f9f6-45b1-4f1c-98d7-c834c2638e48`: FIXED (DXCERT D11): presumed ganglioglioma or DNET, no grade (overrides October C6); CENTRAL 2
- `ce4fad4e-fef0-4dc9-ba82-771d494fd119`: FIXED (LABSIG D8): anemia/iron rows filled; GI must exists; CENTRAL 3
- `00249710-737a-42cf-93e3-16a07fa15f3f`: FIXED: LIT
- `64facd48-7b17-45fa-a116-523509705bc0`: FIXED: LIT
- `705d6671-4025-4544-8f8b-82e3b1c1eff1`: FIXED: LIT
- Class findings: LAT (keep right head version and right arm clonic); DXCERT; TUMOUR; BIOPSY (no resection label); VPA (man); LABSIG.

### FEPI-TEMP-RP01 (approved: no)
- `f0915ecb-f3c2-49e6-8ccd-5c4c2c3eb167`: FIXED: LIT
- `7049facd-8a37-4999-a28f-f6fc0b0895d8`: FIXED: LIT
- `f531ef06-21d7-49a6-ad9d-722bb0770f28`: FIXED: MRI-CONTRAST
- `583b91c2-a8ed-43a7-bf9c-475be3db6942`: FIXED (D19): optional imaging-before-LP criterion (CT or MRI) + hard constraint; MRI->CSF removed
- `adaf74ab-19fc-4da9-b634-fc99ec7b67da`: ALREADY-FIXED (D15): stop rule keys the continuous_icu criterion; CENTRAL 3
- `03911b8d-9402-43ca-81d1-cdc8d45b2c4a`: NO-ACTION (D14): acyclovir/SE musts already "without waiting"; CENTRAL 4
- `9a000203-49b4-44b9-b12b-05b6f5ec2810`: FIXED (LABSIG D8); CENTRAL 3
- `b60fbd8a-9ee7-4a9c-b61b-47e267edc314`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open (positive CSF HSV-1 PCR)
- `c54b12b9-b754-4f49-8ee1-d18649648922`: FIXED: LIT
- Class findings: BIOPSY+resection; LABSIG; D19.

### FEPI-TEMP-RP02 (approved: no)
- `9d0e5380-ae1e-4ef3-bb95-80e4727d893b`: FIXED: LIT
- `a598b629-8c54-4fd1-9cb3-e71c01b4bb32`: FIXED (LABSIG D8): D-dimer row filled; CENTRAL 3
- `78946c3e-95a5-4762-b8c3-1c13ea60b331`: FIXED (D20): CTA first in criteria + soft constraints; empiric anticoagulation must; stop-rule timing part CENTRAL 4
- `ae306531-8980-4e76-a002-4497d9e13df7`: FIXED (LABSIG D8, D20): level qualified (no therapeutic range) in row, KCE, evidence
- `54a0e930-b5a4-41d9-a054-d1bbc1e581cb`: FIXED (D20): routine EEG recommended and out of the stop rule; ambulatory required
- `9f64da60-9038-4049-b2a1-f94deac47cf3`: FIXED (D20): convulsive semiology attributed to roommate account and event diary
- `02536f90-3380-4973-9442-c701dbf6a773`: FIXED (TEE D5): TEE waste
- `d2ad939c-5557-4fff-8f30-b6c430731e3a`: FIXED (VPA D7): jurisdiction-neutral prohibition (class, 19 cases)
- `7a342e80-6f30-45b2-8924-df3488f96fd9`: FIXED: LIT
- `c6c6711b-69fb-4ed6-8472-b4ba91b32b9b`: FIXED: LIT
- `a1f981cb-a45b-4ebd-8ab3-58a9274b6758`: FIXED: LIT
- Class findings: BIOPSY (no stored biopsy) + resection; TEE; VPA (man); LABSIG; D20.

### FEPI-TEMP-RP03 (approved: no)
- `63960600-6dc5-476a-9e68-533e6c5d557b`: FIXED: LIT
- `eec987aa-b816-4fbb-adbf-fce9a3ddadf5`: FIXED: LIT
- `8ff025b4-83da-4ef1-b322-e34f584c4fc6`: FIXED: LIT
- `81b2b522-e7cb-47e0-8dee-ebe40f0650ae`: FIXED (D21): recommended video-EEG criterion
- `6f89d2a1-7ce6-4361-b454-ec6a8373a3f6`: FIXED (DXCERT D11): ICI clause dropped from label; CENTRAL 2
- `ae100235-db1e-487f-beb2-454a8475e3cb`: FIXED (D21): KCE on prophylaxis not recommended (SNO/EANO 2021); HPI factual
- `9a33accb-2872-4ed5-ab5f-38f2f8d39232`: FIXED: MRI-CONTRAST
- `06bda243-cd73-411f-b7e1-6f6aef29ec73`: FIXED (D21): ICI continuation decided at MDT
- `866290ba-82b6-40cd-89c5-726f707571cc`: FIXED (DIFF D12, D21): conditional ICI differential; steroid prohibition reworded
- Class findings: LAT (hand and slow head turn); DXCERT; DIFF; LABSIG (levetiracetam, TSH); no biopsy label (D3 exception); D21.

### FEPI-TEMP-RP04 (approved: no)
- `ff8e8ce1-5318-455a-bec7-77cb93b31b87`: FIXED: LIT
- `829826dd-4edb-498f-bd8a-1f7dc8f16a89`: FIXED: LIT
- `0621d8e0-052d-40b5-9909-a004a0c584a1`: FIXED (D22): resection extent individualized; hippocampus-limited prohibition deleted
- `6571ab91-531b-4a93-9297-ab20e0d4868b`: ALREADY-FIXED (D11): MRI "possibly FCD type IIIa", label "suspected"; surgical musts fixed under 0621d8e0
- `fd653fe7-19b4-4d05-be08-2d99c22bdd8d`: FIXED (LABSIG D8): sodium row; sodium monitoring must kept; CENTRAL 3
- `3e0134ae-a14d-4fe0-ab71-7327f05353aa`: FIXED (D22): inducers lower lacosamide 15-25%; additive sodium-channel effects
- `7f425884-e4c3-4cbd-98e2-d906cfa08a0c`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- `621e716f-0f57-4083-a2c1-094dbc141e8a`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- `de703336-534a-485a-94cc-5e1debceb824`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open (note filed on the resection prohibition, which D22 deletes)
- Class findings: LAT; BIOPSY (no resection label); LABSIG; D22.

### FEPI-TEMP-RP05 (approved: no)
- `df195b2f-2de7-4a11-af6d-b2ed8505db3f`: FIXED: LIT
- `f309f93e-bdc0-4a3f-8cf0-ebb49846b30d`: FIXED: LIT
- `ce97d212-a024-44ba-8290-0eb6aa241c48`: FIXED: LIT
- `d90d6600-9587-47d8-bc2a-7fa758b82e8b`: FIXED (D23): early discussion with surgery centre; referral if seizures continue
- `c9507886-0a8f-44a9-b06d-21531d90af80`: FIXED (D23): recommended MRV criterion + stored MRV; conditional LP opening pressure in must
- `fb9d9625-c754-4473-a0a5-83a64e0b85e0`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open (encephalocele)
- `b18ca2f1-6568-43c5-8786-6e8e9a44cac9`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open (encephalocele)
- `2011eddd-6a6d-44a7-9cca-fccbaf68e857`: FIXED (D23): full-thickness middle cranial fossa floor defect
- Class findings: LAT; BIOPSY (no resection label); VPA (woman); PREG; D23.

### FEPI-TEMP-RS01 (approved: no)
- `a76e2fe3-2c72-4ec2-9e01-98db4e0139a1`: FIXED: LIT
- `ff428acc-88c5-4a96-9ff9-d4e72d01722f`: FIXED: LIT
- `7ee70785-4ec6-4282-9ac5-220c487932ed`: FIXED (DXCERT D11): causal "secondary to" dropped, dual pathology kept; CENTRAL 2
- `b69115d8-627d-4ccc-acd5-dbbab80529c1`: FIXED (D24): intracranial EEG not routine (HH consensus 2026)
- `bc558a72-9454-4b2d-bcca-eea0b1b208d5`: FIXED (NEUROPSY D17): recommended neuropsych criterion + new stored report
- `28f64ad1-4be5-4095-8043-7ae0cb911917`: FIXED: MRI-CONTRAST
- `f566b2d3-dc9e-4f2b-af2b-1fe9e223211e`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open (hypothalamus)
- `f94e99ad-a6b0-42a3-8f59-1525c090cb81`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open (hypothalamus)
- `3d552490-9ade-4cd1-8b18-b29dfba72b9b`: FIXED (D24): repeat radiosurgery conditional on prior dose/fields review
- Class findings: LAT; DXCERT; BIOPSY (no resection label); NEUROPSY; D24.

### FEPI-TEMP-RS02 (approved: no)
- `d330a224-394b-4799-bed1-27d0411ace36`: FIXED: LIT
- `55180e09-2886-4781-b46a-6722fc950405`: FIXED: LIT
- `dba0eeb9-2629-43cb-bdd9-aa5acab7fe92`: FIXED (DIFF D12, KCE D13): eclampsia differential and KCE[0]
- `60ae567c-165d-48df-930f-6d38d9129cb2`: FIXED (D25): magnesium if eclampsia suspected clinically, including atypical
- `025465ed-16e7-4ad4-946c-a1a551117404`: FIXED (D25): photic stimulation not performed (pregnancy; Peltola 2023)
- `f55eb305-f959-43f8-89f2-be369da89f8d`: FIXED (D25): optional CT criterion served by the case CT fallback
- `67484266-e0e7-4fbe-b8b1-de1ebe28cebc`: FIXED (LABSIG D8); CENTRAL 3
- `03c72e26-3873-4e19-b696-ef1f41c11767`: FIXED (DXCERT D11): presumed NCC, no causal claim; CENTRAL 2
- Class findings: BIOPSY+resection; DXCERT; DIFF; KCE; LABSIG; D25.

### FEPI-TEMP-RS03 (approved: no)
- `4be83fe8-fb1f-415f-b031-ec700c19a240`: FIXED: LIT
- `7ab97c72-7549-4013-8ddb-5a21daeaa2d0`: FIXED: LIT
- `6e8cff87-2ab8-49a9-85fd-48c066e72d34`: FIXED (D26): IR 50 mg twice daily; HPI explains the dose ceiling
- `549292c1-9061-44a3-8d97-053688739b5c`: FIXED (DIFF D12, D26): recommended MRV criterion + stored normal MRV
- `bd456258-6d07-4116-bd79-ac462f753445`: FIXED (DIFF D12, D26): postpartum preeclampsia labs added; obstetric review and serial BP must
- `492937af-43d8-410c-96f0-ba7bde6b4511`: FIXED (LABSIG D8, D26): bicarbonate row; recheck before topiramate increase must
- `6af81874-9821-4703-b944-f1e6b1edb10a`: FIXED (LABSIG D8): consistent with dose; October "missed doses" reversed in labs and KCE
- `aeb93cd1-4e28-4444-9150-03bbf19da1f6`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- `76235bed-e38b-4b82-bc27-67e1fbf64748`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- Class findings: BIOPSY+resection; VPA (woman); PREG; DIFF; LABSIG; D26.

### FEPI-TEMP-RS04 (approved: no)
- `1bfeac03-786b-46a3-befd-aff6f6a53524`: FIXED: LIT
- `435c1a44-8457-464c-ad52-a8d95595b70b`: FIXED: LIT
- `a59ef5a3-67ab-465a-90cd-e3524d909499`: FIXED (D27): ASM trial chronology in HPI
- `5f1e70d9-123d-4788-83d5-918b7d4d332a`: FIXED (LABSIG D8, D27): sodium row; monitoring in the rationalization must
- `2508252d-c49f-4628-bca6-94a68e2c6c9f`: FIXED (D27): staged, supervised rationalization
- `09c35528-3662-4c82-8e3f-0eb87c7256a6`: FIXED (D27, PREG D16): reproductive history; shared-decision contraception; hCG criterion
- `7c6e211f-e85f-45c3-b2b6-8efd31821a5b`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- `010a6303-df11-4c56-86fc-6b12049dc550`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- Class findings: BIOPSY (no resection label); PREG; LABSIG; D27.

### FEPI-TEMP-RS05 (approved: no)
- `29fada5d-c985-4e9d-aea0-75096f5d8f27`: FIXED: LIT
- `4a631479-293f-49da-811d-3bb474324856`: FIXED: LIT
- `5479d55f-3dd3-440e-81aa-8c42bb62bf19`: FIXED (HLA D6): prohibition with HLA-A*31:01 clause
- `f5970455-ca97-446c-84d0-b6b44079ca4c`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open + resection harm (treatment-naive)
- `de44b8b5-592a-4bdf-ba72-503f2acde8e1`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open (note misfiled on the TEE step; text is the biopsy demand)
- `85512f5e-58e2-4679-9239-1285d2226e5e`: FIXED (TEE D5): TEE waste
- Class findings: LAT; HLA; TEE; BIOPSY+resection; VPA (man).

### FEPI-TEMP-S01 (approved: no)
- `8896de5c-0588-484d-b8dc-b182305fa086`: FIXED: LIT
- `22693011-def7-46e9-b8eb-d0e92aaf7353`: FIXED: LIT
- `86eeff1f-ed05-4f14-85ba-f2eb05fe58e7`: FIXED (LAT D10): left-hand automatisms and canonical KCE
- `b98605a5-f86d-4a18-9e0b-cbff7ffdfcca`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- `0368fbac-2327-43c2-a0f8-b6ab9b5f006c`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- `e1e2f67a-d16d-483f-b7e2-a23018e9031f`: NO-ACTION (D14): stop rule governs diagnostic completion only; CENTRAL 4
- Class findings: LAT; BIOPSY+resection; VPA (man).

### FEPI-TEMP-S02 (approved: no)
- `79f6580e-814d-4764-97af-0dd73e3ba2c5`: FIXED: LIT
- `8e59b5dc-6aa7-484f-9ec6-501de96dd222`: FIXED: LIT
- `b872a6c7-d86f-4b57-b272-e4346fa8daf2`: FIXED (DXCERT D11): presumed DNET (overrides October D2); CENTRAL 2
- `92195484-10b9-48c2-bbfa-955c215aa976`: FIXED (TUMOUR D4, BIOPSY D3)
- `3e1f7693-a938-4f94-949b-b488bccf368e`: FIXED (TUMOUR D4, BIOPSY D3)
- `914006ad-66be-4383-8ad8-4a000a752da1`: FIXED (NEUROPSY D17): neuropsychology and individualized language lateralization in the surgical must
- `ca64a5ae-539e-402c-91e1-3dae6b7c8680`: FIXED: MRI-CONTRAST
- Class findings: DXCERT; TUMOUR; NEUROPSY; BIOPSY; VPA (woman); PREG (move the existing pregnancy row); D33 wording (same COC text as S04).

### FEPI-TEMP-S03 (approved: no)
- `82f4b80d-33ec-4a38-acba-120804a23a5e`: FIXED: LIT
- `069ee177-0a7c-4655-a655-1b3a229696ec`: FIXED: LIT
- `dbefe268-6267-449c-a4e4-a0d498a4ee7d`: FIXED (DXCERT D11): presumed DNET; CENTRAL 2
- `a1784b94-92f7-4ba8-8f1f-6a36faf5b795`: FIXED: MRI-CONTRAST
- `9b3cb044-d968-48d1-8366-7bc58cc4636a`: FIXED (TUMOUR D4, BIOPSY D3)
- `483070f9-7376-46c8-bd7d-fe7bed7e7188`: FIXED (NEUROPSY D17)
- Class findings: DXCERT; TUMOUR; NEUROPSY; BIOPSY; VPA (man).

### FEPI-TEMP-S04 (approved: no)
- `472d4795-3e4b-4b06-9df7-c40182d40b72`: FIXED: LIT
- `08cdfd73-cbdb-445f-99b5-5d6834c72e2f`: FIXED: LIT
- `404a1855-07f2-488f-8502-7a2fee18c094`: FIXED (HLA D6); surname/ancestry part DECLINED (demographics: Southeast Asian (Lao))
- `9a147be9-5285-4e37-836d-66c0d90ca048`: FIXED (D33): standard titration, maintenance by response (also S02)
- `1255373f-241e-458f-b179-13ec76141124`: FIXED (PREG D16): recommended hCG criterion + stored negative hCG
- `b4cb7aaf-204b-4cb2-9e83-c6e384d4db19`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- `f89332a4-f05b-439d-8f88-e5d8b98b969a`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- Class findings: HLA; BIOPSY+resection; VPA (woman); PREG; D33.

### FEPI-TEMP-S05 (approved: no)
- `cdda040a-a017-46cc-9572-fbe5c3051786`: FIXED: LIT
- `335f4a86-0ea6-461c-b241-4cfe52d208a9`: FIXED: LIT
- `69ab2354-d7ed-4a6a-b90f-68f97ce33cdd`: FIXED: LIT
- `51cb6971-7fed-4919-8dc2-c9fa81cda6a5`: FIXED (D34): reworded stroke prohibition
- `3596b174-d606-4fd2-b17e-de00b4e549e0`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- `50699ff2-0812-4499-bb1e-cb00837c6be7`: FIXED (BIOPSY D3): two harm avoided actions, stereotactic and open
- Class findings: BIOPSY+resection; VPA (man); D34.

### FEPI-TEMP-S06 (approved: no)
- `2e6dc1ea-51bc-4c5a-b2d9-a2cb08ad36d7`: FIXED: LIT
- `88f3adf9-d14e-4df4-afd2-24a1e4ac6688`: FIXED: LIT
- `76151661-ef28-4f44-891a-35a9b16208cd`: FIXED (DXCERT D11): presumed DNET; CENTRAL 2
- `51ecb5b2-6a17-4e52-b5e8-60567eb1ed6f`: FIXED: MRI-CONTRAST
- `b43646cf-6cf1-4f1e-a89b-0b6536e16e82`: FIXED (TUMOUR D4, BIOPSY D3)
- `4958762a-be33-4f73-878a-240ffacc1f46`: FIXED (TUMOUR D4, BIOPSY D3)
- Class findings: LAT; DXCERT; TUMOUR; HLA; BIOPSY; VPA (woman); PREG (move the existing row).
## 4. CENTRAL requests

1. **Criteria pack and allow-list** (`criteria_packs/FEPI-TEMP.md`, orchestrator): add the new
   keys of the decisions file header (`HH_consensus_2026`, `SNO_EANO_prophylaxis_2021`,
   `AAN_AES_SMFM_2024`, `AHA_CVT_2024`, `ACEP_seizure_2004`, `Lacosamide_label`,
   `EAU_hyponatremia_2014`, `Friedman_IIH_2013`, `WHO_CNS5_2021`, `CDC_USMEC_2024`; verify the four
   marked "label"); update section 1 (presumed/suspected labels, no grade), section 2 (literature
   gone; PREG hCG recommended in 10; P05 video recommended and ECG optional; RP02 routine EEG
   recommended; RP03 video recommended; RS01 neuropsychology recommended; new MRV in RP05 and RS03;
   M04 contrast MRI; RS02 CT optional; RP01 imaging-before-LP criterion), section 3/4 (biopsy and
   resection `harm`, TEE `waste`, HLA as prohibition, jurisdiction-neutral valproate rule,
   photic stimulation contraindicated in pregnancy), section 5 (RP01 hard constraint on the
   imaging criterion; RP02 CTA-first soft constraints), section 8 (canonical musts of this plan).
2. **Synonyms / labels** (`diagnosis_synonyms.yaml`, `apply_diagnosis_synonyms.py --check`):
   `accepted[0]` changes in S02, S03, S06, RM04, M04, P04, RP03, RS01, RS02 (class DXCERT). Check
   that no granted synonym or rejected label contradicts the new wording (e.g. RP03 rejected
   "checkpoint inhibitor encephalitis" now agrees with the label; M04 "nonlesional"/"mri negative"
   rejected vs P04's new "nonlesional" label is per case, fine) and that "presumed DNET"/"suspected
   FCD" answers still score.
3. **Review app display** (`web-review`, `review_api`): null `clinical_significance` and
   `contrast_used` print "none" (show "not stated"); lab and neuropsychology rows print the flag
   above the test name (print `test` first; per-row abnormal flag visible); the stop-rule panel
   shows only tool names (show each criterion's label and arguments, e.g. `analyze_eeg
   {eeg_type: video}`). Notes affected: 15 LABSIG, 3 NEUROPSY-FLAG, 2 STOPSUB.
4. **Harness documentation / review app text**: state that the stop rule measures diagnostic
   completeness before the final assessment and never delays treatment, which is scored only in
   the assessment musts (4 timing notes). A future harness could add an interim-management action
   (acyclovir, anticoagulation, benzodiazepine) scored by timing; not needed for this round.
5. **Guidance claims** (`test_guidance_claims.py`, condition_tool_guidance FEPI responses): ECG
   and video-EEG counts change (P05 ECG optional, video recommended; RP03 video recommended);
   lab criteria counts change (PREG +10, P02 hyponatremia +1); literature counts are 0. Maintain
   centrally after the round.
6. **Cross-condition classes** (for the other leads / orchestrator): unlabelled stored biopsy
   follow-ups in NMDAR-ENC (18 cases), SE (6), GLIO-HG (3, check: tissue often required there);
   unlabelled TEE follow-ups in GBS (1), SE (3), VASC-DEM (4); MHRA "under 55" valproate wording
   in MIG-AURA (5); unilateral-automatism side vs focus in any SE or FND case that describes them.
7. **Guard suggestion** (`test_case_guards.py`): a stored `obtain_tissue_diagnosis` or TEE
   follow-up that no criterion orders must be matched by an avoided action (or be explicitly
   exempted), so a served invasive study is never unscored.

## 5. Open questions

None for Andrea. Judgment calls decided in the decisions file (severity `harm` for biopsy and
resection, `waste` for TEE, the resection extension, the PREG scope, RP03 biopsy exception, the
label wordings). Worker cautions:
- LAT flips touch many fields: diff the case text for every "left/right hand" afterwards and
  re-check red-herring `field_path`/`data_point` pairs.
- New stored reports (M04 gadolinium MRI, RS01 neuropsychology, RP05 and RS03 MRV, RS03 extra
  labs, P02 osmolality/urine sodium, hCG rows) must be served to their criterion's first
  alternative (`perfect_agent.py -v`) and must not capture an existing order (served-answer probe).
- PREG and P02 labs: one sentence per panel in `interpretation`, no semicolons (lab serving cuts
  on them).
- RP01: confirm with `perfect_agent.py` that a CT-first trace and an MRI-first trace both satisfy
  the new hard constraint and that LP-first violates it.

<!-- PLAN COMPLETE -->
