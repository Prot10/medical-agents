# VASC-DEM: decisions for the November 2026 round

Lead decisions for the 75 R1 notes (NB-KSC3-TWUA-QDTM) in the 30 VASC-DEM cases. No VASC-DEM case is
on work/approved.txt. No case file changed since base 06b74446 (verified with `git log 06b74446..HEAD`
on the VASC-DEM files), so the reviewer saw the current data, and class LIT has already removed every
literature step. The October decisions (round-2026-10/plans/VASC-DEM-decisions.md and
VASC-DEM.md) were never physician-reviewed. Where a note reverses one, the October rule is
re-examined below and the physician ruling wins unless a guideline clearly says otherwise. None of
the reversals below fails that test.

Sources verified on 16 Nov 2026 (WebSearch; no case text was searched):
- VasCog-2-WSO Criteria Consortium; Sachdev PS et al. Revised diagnostic criteria for vascular
  cognitive impairment and dementia: the VasCog-2-WSO criteria. JAMA Neurol 2025;82(11):1103-1112,
  doi 10.1001/jamaneurol.2025.3242. Imaging that supports a vascular cause includes two or more
  lacunes outside the brainstem, or one lacune with extensive WMH. Extensive and confluent WMH may
  correspond to Fazekas 2-3 (periventricular 3 and/or deep 2-3). A single strategic infarct (e.g.
  thalamus) may suffice. Mixed and multifactorial causes are explicitly allowed, and AD biomarkers
  are optional. New key `[VasCog2_WSO_2025]`.
- Sachdev P et al. VASCOG statement, Alzheimer Dis Assoc Disord 2014;28:206-218: the mild-disorder
  threshold is about 1 SD below norms. Probable VCD needs supporting neuroimaging (`[VASCOG_2014]`,
  already allow-listed).
- Guilmette TJ et al. AACN consensus conference statement on uniform labeling of performance test
  scores. Clin Neuropsychol 2020;34(3):437-453. Percentile labels: 25th-75th average, 9th-24th low
  average, 2nd-8th below average, below the 2nd exceptionally low. The 8th percentile is the
  conventional cut-off for impaired performance. New key `[AACN_labels_2020]`.
- Mancuso M et al. Monogenic cerebral small-vessel diseases: diagnosis and therapy. EAN consensus.
  Eur J Neurol 2020;27(6):909-927: "There is no evidence contraindicating the use of triptans in
  patients with CADASIL with migraine" (100% agreement). New key `[EAN_monogenic_SVD_2020]`.
- 2024 ESC AF guideline (`[ESC_AF_2024]`, Eur Heart J 2024;45:3314). Device-detected subclinical AF
  must be confirmed by a professional reviewing the intracardiac electrograms. A DOAC "may be
  considered" in asymptomatic device-detected subclinical AF with elevated thromboembolic risk and
  no high bleeding risk (IIb, B; ARTESIA, NOAH-AFNET 6).
- Indik JH et al. 2017 HRS expert consensus statement on MRI and radiation exposure in patients with
  CIEDs. Heart Rhythm 2017;14:e97-e153. MRI with a non-MR-conditional system is reasonable under a
  dedicated protocol (asynchronous pacing in pacing-dependent patients, with staff able to place a
  temporary pacer). New key `[HRS_MRI_CIED_2017]`.
- Levine GN et al. Management of patients at risk for and with LV thrombus: AHA scientific
  statement. Circulation 2022;146:e205-e223. A DOAC is a reasonable alternative to warfarin, OAC is
  typically given for 3 months after MI, and repeat imaging at 3 months with the same or a better
  modality is favoured. New key `[AHA_LV_thrombus_2022]`.
- NICE CG115 (2011) rec 1.3.4.5: consider inpatient or residential assisted withdrawal with a history
  of withdrawal seizures or delirium tremens; rec 1.3.4.6: lower threshold for older or cognitively
  impaired people. New key `[NICE_CG115]`.
- Already allow-listed and unchanged: `[AHA_ASA_2021_secondary]`, `[AHA_ASA_2022_ICH]`,
  `[ADA_older_adults_2026]`, `[Boston_v2]`, `[STRIVE_2]`, `[NICE_NG97]`, `[AAN_MCI_2018]`.

## D1. Timed gait tier (TIER-a): FIXED, class in all 11 cases with a gait criterion
Notes: ea5c0723 (M01), 19c0c7e0 (M02), ae5091af (P07), 326d4d6e (S01), 338e7d25 (S02).
Decision: `gait_and_balance_timed` is never required. It is recommended where the exam shows a gait
abnormality (M02, P01, P05, P06, P07, S01, S02, S03, S04, S05) and optional in M01 (normal gait, no
complaint). It leaves every stop rule (M02, P07, S01-S05).
Reason: timed testing characterises the gait and measures fall risk, but no criterion (VASCOG 2014,
VasCog-2-WSO 2025) needs it for the diagnosis. Bedside gait examination is part of the neurological
exam the agent already sees. This reverses October pack s.2 and C14 ("required in the subcortical
syndromes"), which had no guideline basis for a timed test as a diagnostic requirement. S03, S04
and S05 have no note but carry the same defect (class).

## D2. Neuropsychological battery tier (TIER-b): FIXED, recommended in 10 cases; required kept in P07
Notes: 2914e61e (M04), 2d3cca35 (M06), 6f7d7387 (P01), 6cdaae35 (P06), dc590435 (P09),
4bfc7ab6 (S09), 4bc866bf (S10).
Decision: change `neuropsych_battery` from required to recommended and drop it from the stop rule in
M04, M06, P01, P06, P09, S09 and S10 (notes) and in M01, M02 and P02 (class). It stays **required in
P07**.
Reason: VASCOG 2014 and DSM-5-TR accept "standardized neuropsychological testing or, in its absence,
another quantified clinical assessment". A validated screen with an informant functional scale and
the MRI establishes the disorder. The battery characterises it, sets a baseline and serves
rehabilitation and return-to-work decisions. P07 is the exception that the physician's own reasoning
implies: the screen there is normal (MoCA 26/30, the case's red herring), so the battery's
executive measures (Zoo Map 1st, Wisconsin 2/6 categories, against premorbid IQ 128) are the only
objective evidence of the deficit. Without them the diagnosis cannot responsibly be made. For M01 (mild
VCI) the battery is the baseline for the 12-month reassessment. Under D6 it shows only low-average
scores, so it cannot be a prerequisite. In P02 the driving must is reworded so that it does not
depend on battery percentiles (D11).

## D3. Amyloid biomarker, FDG-PET and NOTCH3 tiers (TIER-c, d, e): FIXED
Notes: 689eb2a3 (M05), 86da537c (M07), d520c5af (M08), 77025126 (P01), 1d95402c (P02), 9b4a12d4
(P02 FDG), 5d26a29f (P06 NOTCH3).
Decision:
- The amyloid criterion (CSF or amyloid PET) goes from required to recommended in M05, M07, P01 and
  P02, and to optional in M08. It leaves every stop rule. The CSF harm label stays in M08 and P02
  (LP declined, and edoxaban in M08).
- P02 FDG-PET goes from recommended to optional.
- P06 NOTCH3 (`genetic_panel:CADASIL`) goes from required to recommended and leaves the stop rule.
  P05 NOTCH3 stays required (a cysteine-altering variant is the diagnosis, VASCOG/VasCog-2 genetic
  criterion).
- Every must, key evidence item and prohibition that makes the biomarker decisive is reworded so
  that it is satisfiable without it: "positive amyloid biomarker" in the mixed-dementia musts
  (M05, M07, M08, P01, P02); the P01 kce0 "the storage amnesia is the finding that demands the
  biomarker"; the M07 statement that amyloid status decides the cholinesterase inhibitor; the P01
  prohibition "when Alzheimer pathology is biomarker-confirmed". Canonical must head:
  "Name mixed Alzheimer and vascular dementia: <the clinical Alzheimer features> with <the vascular
  burden> [VASCOG_2014]; an amyloid biomarker, if obtained, adds certainty to the Alzheimer component."
Reason: VasCog-2-WSO makes AD biomarkers optional, and NICE NG97 (1.2.14) uses a further subtype test
only when it would help diagnose the subtype and would change management. A cholinesterase inhibitor
is offered for the clinical diagnosis of AD and mixed dementia (NICE NG97 1.5) without a biomarker.
This reverses October C9 and pack s.2 ("required"). The October basis was the lead's view and not a
guideline. In M08 a declined LP plus a strong clinical and MRI picture make PET optional (R1).

## D4. ECG and stroke aetiological work-up (TIER-f): FIXED, 4 cases
Notes: 11986a51 (M04), 4ed18eeb (P09), b763111e (S09).
Decision: the ECG goes from recommended to required and into the stop rule where an ischaemic infarct
(clinical, or new on this MRI) has had no ECG or rhythm assessment before this encounter. These are
M04, P09 and S09 (notes) and **S01** (class: two TIA-like lacunar events, "neither investigated").
In M04 the cervical-vessel criterion (MRA or duplex) also goes from recommended to required and
into the stop rule. TTE and prolonged monitoring stay optional in M04, P09 and S09, and the three
cases get the must: "If the ECG and vessel imaging show no cause, arrange echocardiography and
prolonged rhythm monitoring, which would change the antithrombotic choice [AHA_ASA_2021_secondary]."
The ECG stays recommended where the HPI documents an admission rhythm assessment: M05 (48 h
telemetry), S11 (72 h telemetry, TTE) and M09 (ICH). No ECG criterion is added in S10 (ECG, telemetry
and duplex at admission), P01 or P07 (lacunar strokes years ago, already on clopidogrel).
Reason: AHA/ASA 2021 recommends an ECG for every patient with ischaemic stroke or TIA (class 1) and
non-invasive cervical carotid imaging (class 1). Echo and prolonged monitoring are conditional (2a)
when the first steps are unrevealing. R1's M04 rider ("should not all be prerequisites") is met
because only ECG and vessel imaging enter the stop rule. S01 has no note, but its events were never
investigated: same defect (class). No carotid criterion is added in S01, because the events were
2-3 years ago, outside the window where a stenosis would change management.

## D5. Stop rules keyed on the specific study (STOP-RULE kind 2): ALREADY-FIXED + CENTRAL
Notes: f569e1c8 (P05), 6331cc50 (S06), 2c6f29cf (S07), f33e4140 (S08), 77ee2163 (S11).
Decision: the data already does what the notes ask. Each stop-rule id points to a criterion whose
`required_arguments` name the study (P05 `genetic_panel:CADASIL`; S06, S07, S08, S11
`carotid_duplex`; S07 `event_monitor_30d`; S08 MR_angiography). A neuropsych order cannot satisfy
the NOTCH3 criterion, and a Holter order cannot satisfy the 30-day criterion. The MockServer's
monitoring tiers also never serve a 30-day report to a Holter order (tool-contract.md). The review
app shows only the tool-named criterion id: that display is CENTRAL.md item 3. Criterion ids are not
renamed (ROUND_POLICY keeps ids stable). Logs state the checked arguments.
Addition (own finding, CAROTID-ALT): in M03, S06, S07 and S11 the required carotid criterion
accepts only the duplex. In M05 (optional) the same applies. Each case stores an MRA of the neck that
agrees with the duplex (checked: M03 about 30% left, S06 right 30-40%, S07 under 30%, S11 right 50-60%,
M05 left 30-40%). Add `order_advanced_imaging {"modality": "MR_angiography"}` as a second
alternative in these 5 cases, as M04, M06 and M10 already do. Reason: AHA/ASA 2021 recommends
non-invasive cervical imaging (duplex, CTA or MRA) without preferring one, so an agent that chooses
MRA did the required work. This still meets R1's "only the carotid assessment should satisfy it". S08
keeps its separate recommended MRA criterion and the duplex-before-MRA constraint (f33e4140), because
there the MRA confirms a severe duplex stenosis before surgery.

## D6. Neuropsychological percentile labelling (NP-CUTOFF): FIXED, class in all 30
Note: 1b7abe7c (M01; first half).
Decision: rewrite every percentile row in VASC-DEM batteries (initial or follow-up
`order_specialized_test` neuropsych outputs) to the AACN 2020 labels:
- `reference_range`: "9th percentile or above (25th-75th average)".
- `abnormal`: "yes" at the 8th percentile or below; "low average" for the 9th-24th; "no" at the 25th
  or above.
- Impression sentences that call a 9th-24th percentile score impaired or reduced say "low average"
  instead. Sentences about scores at or below the 8th stay as they are.
- Rows that are not percentiles (FAQ, pass/fail, IQ) keep their ranges.
Measured: 43 rows between the 9th and 24th percentile are flagged "yes" against a 25th-75th range,
in 25 cases (M01 3, M02 2, M07 3, M08 2, P03 4, P04 2, P08 3, S01 2, S06 4, S07 3, others 1 each;
M01's TMT-B 16th, SDMT 18th, FAS 22nd). After the fix M01's battery reads as low-average set-shifting,
speed and fluency.
Reason: AACN 2020 uniform labelling, with the 8th percentile as the usual impairment cut-off. VASCOG
2014 sets mild impairment at about 1 SD below norms (the 16th percentile), so the 16th-22nd are not
"unequivocal pathological impairment" (R1). Cross-condition: ALZ-EARLY has 57 rows in the 9th-24th
band flagged "yes". There R1 asked to flag the 24th "below the stated range" (c23ae468), which was
consistent with the range then stated. That is an open cross-condition consistency item (plan
section 5), not a VASC-DEM change.

## D7. Lacune counts (LACUNE-COUNT): FIXED, 3 cases
Notes: 593a77db (S03), 1aa45a50 (S05). Class: P06.
Measured by script over all 30 MRI reports (bilateral sites counted as 2): S03 says "8 lacunes" and
lists 7. S05 says "7" and lists 6. P06 says "9" and lists "thalami, putamina, pons, corona radiata"
(7 if each plural is bilateral). The other 19 reports with lacunes agree.
Decision: keep the count, which appears in the findings, impression, criteria expected_evidence and
key evidence, and add the missing site(s) to the findings `location` and the impression list. The
site must be a deep site that changes no localising argument in the case: S03 "left putamen";
S05 "left caudate head"; P06 an explicit list with counts per site summing to 9 (e.g. "both thalami,
both putamina, pons, both coronae radiatae, left caudate head, right internal capsule"). Then grep the
case for every other lacune count and site list. Reason: internal consistency (style guide).

## D8. Diagnostic certainty and imaging sufficiency (DX-CERTAINTY, IMG-SUFF): FIXED
Notes: 1b7abe7c (M01, second half), 265d87a9 (M01), dc52b75a (M02), ec3158d4 (M04), 801c6a8c (M05),
beb3f9ea (M06), 57eb5732 (M07), 7b4f4fe3 (M08), b7821cae (M08), a1dd74ae (M10), 10679dcb (M10),
88d4951c (P02), b5638ec2 (P06), 54d36054 (P08), 4ed18eeb (P09, mechanism part), 3a1edd9d (S01),
5a3125af (P05). Class: M02 rh0, M03 rh1, P01 (kce0, rh0, dd0, dd1, proh0), S06 dd3.
Rule: vascular attribution rests on concordance of the cognitive and functional syndrome, the
neurological findings, the time course and the imaging (VasCog-2-WSO). No lesion burden is by itself
"sufficient" or "required", and no single feature (absent MTA, recognition memory, symmetry,
territory) proves or excludes a mechanism. Canonical replacement for a sufficiency sentence: "<burden>
supports a vascular contribution; the attribution rests on its concordance with the <profile> and the
<course> [VasCog2_WSO_2025]."
Label changes (`accepted[0]`, entity and ICD unchanged; CENTRAL list):
- M01: "Mild vascular cognitive impairment (mild vascular cognitive disorder), most likely due to
  moderate cerebral small-vessel disease; the threshold for dementia is not met".
- M02: "Vascular dementia: subcortical ischaemic (small-vessel) type from untreated hypertension,
  with a possible alcohol-related contribution to the cognitive decline and a coexisting
  alcohol-related cerebellar syndrome and sensory polyneuropathy contributing to the gait disorder".
- M06: "Vascular dementia after perioperative border-zone infarction: bilateral cortical and internal
  border-zone infarcts during prolonged hypotension at aortic valve replacement, predominantly
  haemodynamic, with perioperative embolism not excluded".
- M10: "Vascular dementia: multi-infarct type with two coexisting potential stroke mechanisms,
  untreated atrial fibrillation and severe symptomatic right internal carotid stenosis".
- P06: "...hyperhomocysteinaemia; CADASIL unlikely and not genetically confirmed" (replaces "CADASIL
  excluded").
- P08: "Vascular dementia: multi-infarct type with two coexisting potential mechanisms, left internal
  carotid atherosclerosis and device-detected paroxysmal atrial fibrillation; diagnosed on CT because
  MRI could not be performed safely".
- S08 (class with 7c250244): "Vascular dementia: multi-infarct type, most likely from severe right
  internal carotid stenosis, with a haemodynamic (internal border-zone) component". No dated
  ipsilateral event is documented, so "symptomatic" is unproven (R1).
Labels unchanged (the notes target text, not the entity): M07, M08, P02 (retain mixed; see D9).
Per-case text targets are in the plan index.

## D9. Accepted alternative in P02; differential in M07 and M08 (DIFFERENTIAL): FIXED + CENTRAL
Notes: 88d4951c (P02), 57eb5732 (M07), 7b4f4fe3 (M08).
Decision: in P02 R1 rules that posterior-predominant AD (PCA phenotype) with coexisting severe SVD is
also correct. The answer names both components, so it is a variant of the mixed answer and not an
AD-only answer. CENTRAL (synonyms): accept for P02 only the labels "posterior cortical atrophy small
vessel disease", "alzheimer small vessel disease", "alzheimers small vessel disease"; check them under
scorer v2 against the P02 rejected list and the AD-only mimic answers. In the case: the P02
differential entry "Posterior cortical atrophy (Alzheimer disease) without significant vascular
contribution" stays low, and its key_features drop "a genuine second contributor" for "the Fazekas 3
burden with two lacunes may contribute, but its clinical weight is uncertain when visuospatial
function leads and processing speed is preserved". M07 and M08: add or reword a differential entry
"Alzheimer disease with concomitant cerebral small-vessel disease (no clinically significant vascular
contribution)", likelihood moderate. Key features: progressive amnestic course without a vascular step
(M07); no cortical infarct and moderate deep SVD (M08). Accepted labels are not extended: R1 calls
it a reasonable alternative, not an equally correct answer.

## D10. Alcohol in M02: FIXED
Notes: dc52b75a, ad9a7f1e, b6795cb2.
- Musts and key evidence that say alcohol explains only the gait (must0, kce0 "the temporal test is
  decisive", rh0 "independently sufficient") are reworded. Alcohol-related cognitive impairment is a
  plausible contributor (continued 40 g/day); vascular dementia stays the leading diagnosis.
- Differential dd0 (alcohol as sole cause) stays low and says "less likely as the sole cause"
  instead of "excluded". dd1 Wernicke-Korsakoff stays low, with "absent confabulation and normal
  mamillary bodies lower suspicion but do not exclude it; the executive-predominant profile with
  preserved recognition makes it unlikely". The prohibition "Do not treat an unconfirmed Korsakoff
  syndrome as established in the absence of confabulation and with normal mamillary bodies" is
  reworded the same way.
- New must, replacing must2: "Arrange assessment for medically assisted alcohol withdrawal, as an
  inpatient or under close supervision given his previous withdrawal seizure and older age, rather
  than abrupt unsupervised cessation, with a specialist alcohol service supporting abstinence;
  continue thiamine [NICE_CG115]."
- The prohibition "Do not give glucose-containing fluids without thiamine cover" is replaced by
  "Do not delay glucose for hypoglycaemia while waiting for thiamine; give parenteral thiamine
  promptly alongside it." The case states "a withdrawal seizure six years ago and two withdrawal episodes" (checked).

## D11. Management musts made individualised (MUST-WRONG, UNSOURCED-RULE): FIXED
Each canonical text is in the plan index. In summary:
- M03 (b4d1f1bf, f301a8f4): oral anticoagulation for the LV thrombus, warfarin INR 2-3 or a DOAC as
  a reasonable alternative chosen on her circumstances, typically for 3 months; repeat cardiac imaging
  at about 3 months to decide duration; review aspirin with cardiology (old infarct, no recent ACS or
  stent: anticoagulant monotherapy is usual); heart-failure referral for EF 38%
  [AHA_LV_thrombus_2022] [AHA_ASA_2021_secondary]. The must "Stop aspirin when warfarin is started"
  and the prohibition on aspirin are reworded to the cardiology review. The prohibition on
  prolonged monitoring is deleted. The monitoring waste label is removed (prolonged monitoring would
  matter if stopping anticoagulation were considered later). No criterion is added (not needed now).
- M05 (82baa9d2): "Review gliclazide: assess hypoglycaemia episodes, glucose monitoring and supervised
  administration, set an individualised HbA1c target of about below 8.0%, and replace the sulfonylurea
  with a lower-hypoglycaemia-risk agent if hypoglycaemia risk is high, keeping glycaemic control
  [ADA_older_adults_2026]." The prohibition becomes "Do not continue the sulfonylurea without a
  hypoglycaemia-risk review." kce4 is reworded to match.
- M06 (b9531b5a, e55a303a): BP "Individualise blood pressure for secondary prevention after
  border-zone infarction: lower towards the usual target only as tolerated, guided by symptoms and
  orthostatic measurements, avoiding symptomatic or orthostatic hypotension
  [AHA_ASA_2021_secondary]." Furosemide: "Review furosemide with cardiology: assess the current
  indication, volume status, orthostatic BP, renal function and electrolytes, and reduce or stop it if
  no indication remains." The prohibitions "Do not drive the systolic below 120 mmHg" and kce3
  ("inverts the usual advice ... target individualised upward") go. The furosemide prohibition
  becomes "without reviewing its indication". Class: the fixed "about 120 mmHg" floor in M10 and S08
  musts and pack s.7 is unsourced. It becomes "avoiding symptomatic and orthostatic hypotension
  until the stenosis is treated".
- M10 (10679dcb, deb7367b): "Refer urgently to the vascular team to assess eligibility for carotid
  revascularisation of the 80-90% right ICA stenosis: the last ipsilateral event was 5 months ago, so
  the expected benefit is smaller than after a recent event; weigh disability, life expectancy,
  operative risk and optimised medical therapy [AHA_ASA_2021_secondary]." Antithrombotic: "Start a
  DOAC for the atrial fibrillation (e.g. apixaban 5 mg twice daily: no dose-reduction criterion met)
  and agree the antiplatelet plan with vascular surgery: anticoagulant monotherapy is generally
  reasonable for the stable femoropopliteal bypass, and peri-procedural antiplatelet needs follow the
  carotid decision [ESC_AF_2024]."
- P04 (ead8156d): "Arrange an urgent multidisciplinary reassessment of anticoagulation: the prior
  anticoagulation-associated lobar haemorrhage, 17 strictly lobar microbleeds and disseminated
  cortical superficial siderosis strongly favour avoiding long-term anticoagulation, weighed against
  her embolic risk (CHA2DS2-VA 3) [AHA_ASA_2022_ICH]." LAAO: "Refer for evaluation of left atrial
  appendage occlusion, including the short-term antithrombotic therapy it requires
  [AHA_ASA_2022_ICH] [ESC_AF_2024]." Prohibition 0 becomes "Do not continue apixaban unchanged
  without that reassessment".
- P05 (c7d6ad9b, 5a3125af): CADASIL is not a contraindication to triptans [EAN_monogenic_SVD_2020].
  New must: "Review sumatriptan with her neurologist: triptans are not contraindicated by CADASIL
  itself, but her previous transient hemipareses, whether ischaemic events or motor aura, are
  labelled contraindications; meanwhile use a non-vasoconstrictive acute treatment (paracetamol or an
  NSAID, with an antiemetic if needed) and continue propranolol." No aspirin as a routine substitute.
  The triptan prohibition is reworded to the hemipareses. rh0 is reworded: "mechanism uncertain
  without contemporaneous imaging; CADASIL-related ischaemic events and motor aura are both possible".
  The "complicated migraine" prohibition becomes "Do not dismiss the transient hemipareses as
  complicated migraine without considering ischaemic events". The P05 drug-interaction output is
  rewritten to give the label contraindications (stroke or TIA, hemiplegic migraine) and not CADASIL.
  This reverses pack s.4 and s.7 ("no triptans in CADASIL"): the October rule had no source and EAN
  2020 contradicts it.
- P08 (696e12fd, 58df8274): "Have the stored atrial electrograms reviewed to confirm atrial
  fibrillation; if confirmed, decide on anticoagulation with him and his wife on stroke risk (age 79,
  hypertension, prior ischaemic events) against bleeding risk: a DOAC (e.g. apixaban 5 mg twice daily,
  no reduction criterion) is reasonable for episodes under 24 hours but not mandatory, and aspirin
  stops if a DOAC starts [ESC_AF_2024]." Prohibition 3 is reworded to "if anticoagulation is started".
  MRI: the harm label stays (D12).
- P09 (4ed18eeb): "Start a single antiplatelet (aspirin 75-100 mg or clopidogrel 75 mg daily) if the
  ECG and the aetiological work-up identify no indication for anticoagulation; an artery of Percheron
  infarct can be cardioembolic as well as small-vessel [AHA_ASA_2021_secondary]." With D4.
- S05 (d9a59fff): "Reassess long-term anticoagulation: establish from the ablation record and ECGs
  whether atrial fibrillation was ever documented, and weigh his stroke risk (CHA2DS2-VA 3) and the
  risk of AF after flutter ablation against bleeding risk (age 82, falls, deep microbleeds, alcohol);
  if continued, 5 mg twice daily is the correct dose (only the age criterion is met) [ESC_AF_2024]."
  This replaces musts 1 and 2. The prohibition becomes "Do not stop apixaban solely because of falls
  or a few deep microbleeds [ESC_AF_2024]". This reverses the October S05 decision, which October
  queued for this review: the ESC rule "decide on CHA2DS2-VA, not rhythm" concerns AF ablation and
  does not settle isolated typical flutter without documented AF.
- S08 (7c250244): "Refer promptly to the vascular team: clarify whether the stenosis is symptomatic
  (the cognitive step three months ago was not a documented ipsilateral event, and MRI cannot date
  the chronic infarcts) and assess procedural risk, function and expected benefit before any
  revascularisation [AHA_ASA_2021_secondary]." The prohibition "Do not defer carotid revascularisation
  because the presentation is cognitive..." becomes "Do not dismiss the 70-80% stenosis without a
  vascular-team assessment because the presentation is cognitive or because of age alone".
- M08 (b7821cae, 7b4f4fe3): kce2 becomes "strictly deep microbleeds do not overturn the indication;
  lobar microbleeds or siderosis would raise the intracranial bleeding concern and need an
  individualised risk assessment". Must1 becomes "MRI shows no cortical or territorial infarct, so a
  cardioembolic multi-infarct dementia is not supported, although a contribution of atrial
  fibrillation cannot be excluded; anticoagulation continues". The prohibition "Do not attribute the
  dementia to atrial fibrillation when there is no infarct on MRI" goes.

## D12. On-request follow-ups and their labels (NEW:remove-pathway-steps, AVOIDED-MISSING): FIXED + CENTRAL
Notes: 74a16658 (P08), 2f5910a5 and 75e30bee (S04), 57709b24 (S06), fa0764bd (S07), dd0174a0 (S08),
db0cbe3b (S11).
Measured: 233 stored follow-ups in 30 VASC-DEM cases match no criterion and no avoided action
(dataset-wide 3001 in 550 cases; levodopa challenge 151, cerebral angiography 62, perfusion SPECT 62,
DTI 58, EP study 25, TEE 25 unlabelled).
Decision ("remove" applied to the policy and the pathway order, not to the data):
1. Do not delete the stored reports. The library normal would contradict these patients: normal
   catheter angiography with a carotid stenosis, normal SSEP and skin biopsy with a polyneuropathy,
   a normal EP study in paced complete AV block, normal MRI-based reports for a patient who cannot be
   scanned. This follows ALZ-EARLY decision 8.
2. Add avoided labels per the plan's table C11 (severity by study), so that ordering is penalised.
   Invasive studies without indication (EP study, catheter angiography, coronary angiography) are
   harm. Any MR study in P08 is harm. Iodinated-contrast studies in M03 (documented contrast allergy)
   are harm. Low-yield non-invasive studies are waste. Studies that are reasonable for this patient
   or that R1 kept (carotid-stenosis catheter angiography in M10, P08, S08 and S11; TEE in P08, S08
   and S11; TCD; speech-language; visual fields; headache history; EMG in neuropathy cases) stay
   unlabelled.
3. Reorder `followup_outputs`: credited follow-ups in criterion order first, then the on-request
   block.
4. CENTRAL: the review app should show follow-ups that match no criterion in a separate "Answered on
   request (not part of the pathway)" block. That is the display R1 is reacting to.
Never a criterion and an avoided label on the same call: the MRA is a criterion alternative where
D5 adds it, and it then gets no label.

## D13. Labels softened to conditional (AVOIDED-MISSING direction 1): FIXED
- P03 EEG (dfcba78d): delete `avoid-waste-1-analyze-eeg`. Add an optional criterion
  `action-eeg-tfne` `analyze_eeg {}` answered by the case's own normal routine EEG (move the EEG
  fallback to `initial_tool_outputs.eeg`; it already names `eeg_type: routine`). Expected evidence:
  "Normal routine EEG; a normal interictal recording does not exclude focal sensory seizures".
  Reason: R1, and the case's own differential[2] (focal sensory seizures, "an EEG becomes
  reasonable"). P04 (also CAA with cSS) keeps its EEG waste label: its rationale records "no episodes and no
  seizure" (checked).
- S11 monitoring (ddd47148): delete the monitoring waste label. Add an optional criterion
  `action-prolonged-monitoring` `order_cardiac_monitoring {}` with a stored 30-day event monitor in
  sinus rhythm (`monitor_type: event_monitor_30d`, no AF; new initial output; keep the Holter
  fallback). Reason: R1. AHA 2021 makes prolonged monitoring reasonable when the mechanism is
  uncertain. Here a moderate ipsilateral stenosis makes it optional, not recommended.
- M03 monitoring: D11.
- P08 MRI (58df8274): the label stays `harm` with a new rationale. Severity stays harm because the
  HRS 2017 pathway needs device identification, protocol and specialist presence, which no tool call
  can express, and CT, duplex and interrogation already answer the questions. New rationale: "MRI is
  not needed for this work-up (CT, duplex and device interrogation answer it), and with a
  non-MR-conditional system of unidentified make in a pacing-dependent patient it could proceed only
  after device identification and a specialist MR safety assessment, under a dedicated protocol at an
  experienced centre [HRS_MRI_CIED_2017]." The same label covers the MR modalities (D12). The
  prohibition stays as it is: it is already conditional ("no device documentation").

## D14. Interpreter-administered testing in M09 (NEW:interpreter-cognitive-testing): FIXED
Note: 5cbbc199. Decision: the screen and the battery are given by a Mandarin-speaking examiner with a
validated Mandarin instrument and Chinese norms: "MoCA (Mandarin version)"; "Boston Naming Test
(Chinese version, Mandarin norms)" for the "Culture-fair naming (Mandarin)" row. "With the family
interpreting" goes from `scores.assessment_language` and `neurological_exam.mental_status`, which say
"examined in Mandarin by a Mandarin-speaking examiner". The social-history line (the family
interprets in daily life) stays. The screen criterion's label and rationale name a validated
first-language instrument with a qualified examiner or professional interpreter. The existing
prohibition already forbids interpreting scores without first-language norms. S04 was checked: its
screen uses a trained interpreter (Punjabi-adapted MoCA), and only the history is interpreted by the
daughter-in-law. No change there. Dataset-wide grep for family interpreters: only M09 and S04.

## D15. Notes answered by the display (flag shifted by one row): CENTRAL
- M09 e8dbcb56 ("48° false??"): the only "48" in the target is "Culture-fair naming (Mandarin),
  48th percentile, abnormal: no". That is in range and correct. The next object is the FAQ row
  "abnormal: yes", which prints above its own label, so a reader pairs "48th" with "yes". Ruling
  CENTRAL (CENTRAL.md item 2), with the check stated. The row is renamed by D14. If Andrea can ask
  R1, confirm the intent (open question).
- P07 dc877a4d (premorbid IQ 128 to abnormal "no"): the row is already "no". The next row (FAQ 23/30)
  is "yes". Ruling CENTRAL (item 2).

## D16. Remaining text notes: FIXED
- M04 ec3158d4: kce4 and kce1 reworded. Absent MTA and normal delayed recall make typical AD less
  likely but do not exclude early or atypical (non-amnestic) AD. The abrupt onset, stable course,
  Gerstmann syndrome and the matching infarct strongly favour a vascular cause. Musts and
  prohibitions that say "not Alzheimer disease" become "a vascular cause is strongly favoured". The
  M04 `rejected` labels "alzheimer"/"alzheimers" stay, because an AD-only answer remains wrong.
- M05 801c6a8c: kce0 to kce2 and the differential reworded. Impaired recognition strongly supports
  an amnestic neurodegenerative process but is not disease-specific. A VPL lacune makes isolated
  strategic amnesia unlikely, but stroke-related network effects may add to the decline.
- M06 beb3f9ea: kce0, rh1 and dd2 reworded. Symmetric border-zone infarcts after documented
  prolonged hypotension strongly support a haemodynamic mechanism. Watershed infarction can also be
  embolic or mixed, and perioperative embolism is not excluded. dd2 stays low. The prohibition
  "the mechanism is haemodynamic" becomes "no cardioembolic source requiring anticoagulation has been
  found".
- S02 d16d609a: dd2 and rh1 reworded. OSA is associated with WMH and SVD and may contribute to the
  vascular injury and the cognitive impairment. It stays low as the sole explanation.
- S02 368be191: kce2 becomes "Passed performance-validity measures make the scores interpretable;
  they do not separate vascular impairment from depression, which rests on the clinical, functional
  and imaging picture". Criterion rationale action-6 is reworded the same way.
- S04 9d79fcb4: dd2, kce3 and must4 reworded. B12 deficiency is probable, not established: eGFR 58
  can raise MMA and homocysteine, and diabetes is a major cause of the polyneuropathy.
  Supplementation and monitoring stay.
- P04 7abe5c12: Trail Making B becomes "Oral Trail Making Test Part B". The SDMT row becomes
  "Symbol Digit Modalities Test (oral response; scanning the key still requires vision)". The
  impression and the adaptations field say that the oral SDMT is interpreted with caution because of
  the dense right homonymous hemianopia. The criterion expected_evidence follows.
- P06 b5638ec2: label (D8). Musts and prohibitions that depend on the NOTCH3 result are reworded
  so that they hold without it (D3).

## D17. Declined notes
None. Every note is applied, ruled ALREADY-FIXED, or ruled CENTRAL where the data was checked and
found correct. Partial departures, each with its guideline: P07 keeps the battery required (D2,
outside the scope of any note); the P08 MRI label keeps severity harm while its rationale follows
R1 (D13); the step-removal notes are applied as labels plus reordering, not deletion (D12).

## D18. October decisions changed (all reasons above)
Pack s.2 tiers (gait C14, neuropsychology, ECG, amyloid C9, FDG in P02, NOTCH3 in P06); pack s.3 EEG
waste (P03), monitoring waste (S11, M03); s.4 triptans in CADASIL; s.7 the BP 120 floor, S05
apixaban, M03 warfarin-only, carotid timing wording (M10, S08), the device-detected AF DOAC must
(P08). Kept from October: max_additional_actions 1 (no note asks); RPR/HIV off the panel; CSF harm
in M08 and P02; CSF waste in CAA; the P08 MRI harm severity.
