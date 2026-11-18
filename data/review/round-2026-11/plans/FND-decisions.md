# FND: decisions of the November 2026 round (lead, 16 Nov 2026)

Base: the working tree on 16 Nov 2026, after class LIT (393c547e) and class MRI-CONTRAST. All 73
notes come from R1 (NB-KSC3-TWUA-QDTM). They cover all 30 cases, and no FND case is approved
(`work/approved.txt` lists none). The 73 note ids in `notes/FND.json` match the annotation files
under `input/annotations/neurobench/` exactly. Measurements are in `plans/FND.md` section 2, and the
scripts are in `/home/aprotani/review-round-2026-11/work/scratch/fnd-lead/` (`overview_fnd.py`,
`measure_fnd.py`).

Scorer facts I checked before deciding:
- `policy_reward.py` lines 138-147: once the required set is done, only actions that match no
  criterion count as extra. Recommended and optional criteria are never penalised by
  `max_additional_actions: 0`. A note that only asks to "allow" a test that is already a
  recommended or optional criterion is therefore satisfied in the scoring. `StopRule` has no prose
  field to say so, which makes the explanation CENTRAL (FND.md section 4, C1).
- `required_before_assessment` lists criterion ids, so every criterion made `required` here goes
  into it.
- The MockServer routes `analyze_eeg` by `eeg_type` (tool-contract.md, 24 Oct), so a routine-EEG
  order no longer receives the stored video-EEG. October CENTRAL 1 is done.

Sources verified on 16 Nov 2026 (web search; no case text was searched):
- AAN 2025 (Tolchin et al., Neurology 2026;106(1):e214466). Clinicians obtain the history and
  semiology from patients and witnesses, including smartphone video, and "may obtain video-EEG of
  all typical seizure-like episodes where feasible". They evaluate for co-occurring epilepsy and
  psychiatric disorders, do not prescribe benzodiazepines or antiseizure drugs without another
  indication, and taper antiseizure drugs that have no other indication.
- ILAE 2013 (LaFrance et al., Epilepsia 2013;54:2005-2018), levels of certainty. Possible: the
  history from the patient or a witness only. Probable or clinically established: a clinician
  witnessed a typical event, with an EEG that shows no ictal activity. Documented: a habitual
  event recorded on video-EEG without ictal change.
- NICE CG109, recommendation 1.1.2.2 (already in the pack): a 12-lead ECG for everyone with
  transient loss of consciousness, apparent loss of consciousness included.
- AHA/ASA 2026 acute ischemic stroke guideline (Prabhakaran et al., Stroke 2026;57(8):e316-e436,
  doi 10.1161/STR.0000000000000513). Glucose is checked before thrombolysis. Thrombolysis is
  decided on whether the deficit is disabling, the imaging, the time from onset and eligibility.
  Extra imaging within 4.5 h must not delay treatment.
- Joint Clinical Practice Guideline on Benzodiazepine Tapering (ASAM with nine societies,
  including the AAN). J Gen Intern Med 2025, doi 10.1007/s11606-025-09499-2. After long-term use,
  start with reductions of 5-10% every 2-4 weeks, usually no faster than 25% every 2 weeks. Then
  adjust, and a taper can take months to years.
- Nicholson C et al. Occupational therapy consensus recommendations for functional neurological
  disorder. J Neurol Neurosurg Psychiatry 2020;91(10):1037-1045, doi 10.1136/jnnp-2019-322281.
- Pozuelo Moyano B et al. Clinical impact and misdiagnosis of functional ophthalmological
  symptoms: a case report. J Med Case Rep 2023;17:340, doi 10.1186/s13256-023-04063-0,
  PMC10416532. This is the unused seed `dataset-generation/seeds/functional_neurological_disorder/FND-RM11.json`.
  The journal is BMC open access, CC BY 4.0. The worker confirms the licence line on the PMC page
  before using it.

Sources cited from the existing allow-list (`criteria_packs/FND.md` section 9), not re-searched:
Espay 2018, Daum 2014, McWhirter 2011, Avbersek 2010, Kutlubaev 2018, Oto 2005, Nielsen 2015,
Spasovski 2014, McGuigan 2016, DSM-5. Two further sources are not in the pack and the worker
verifies them before citing (CENTRAL C5): the WHO AUDIT manual (Babor TF et al., 2nd ed., WHO
2001), with its zones 8-15 hazardous, 16-19 harmful and 20 or more possible dependence; and Schrag
A et al., Brain 2004;127:2360-2372, on fixed dystonia.

## 1. LIT: literature search (34 notes, 30 cases)
Notes: f20dfdfa, ea6a9490, fd6b12e4, 06d86723, 30667d14, 80fea3da, 82744d6f, b9f0043f, 546d3260,
95e72dff, ef67e7eb, b7b2460d, 3a7cedc9 ("nio"), 7942bc89, 18418180, 7db59db3, 50e42ac1, dc91a67d,
71b3a3cf, 4dc5ddb4, 2b7000f8, ed1c0cbd, 64653b84, efb943da, c8b24f69, cd93e93c, 99505307,
9ca356f3, 53b45079, f1700eb4, 4e4c7f64, 03adcbc7, 320b9e74, 48159203.
Decision: FIXED by class LIT, commit 393c547e. Checked on 16 Nov: no `search_medical_literature`
criterion and no initial, fallback or follow-up literature output in any of the 30 FND cases, and
none in the 600 cases (0). Workers add nothing back. Reason: ROUND_POLICY ruling 5 and the
November addendum.

## 2. VEEG: the video-EEG tier in the paroxysmal cases (notes ccddb06a M01, 52f87e18 M02, 3327b25f M03, 6a40c3ea M04, a37be9ec M06, 4943e745 RP01, 384cf96b RP03, 4b564a53 S05, 95524722 S06, 7896a50e S09, b7bfdbac S11)
Decision: FIXED, as a class rule over the paroxysmal cases (18 once the rewrites of decision 13
are done):
- **Required** where no habitual event was witnessed by a clinician in the case, or where the
  bedside semiology cannot separate the events from a named epileptic seizure type. Cases: M04
  (eyelid flutter with zero rule-in signs, some events light-triggered, an absence or
  eyelid-myoclonia mimic), M06 (established TLE with interictal discharges, new events not seen),
  P01, RP01 (no event seen, 26 years of treatment as epilepsy, withdrawal planned), S05 (no event
  seen, eyes open), S06 and S11 (staring or motionless spells not seen). In these cases the history
  supports functional seizures only at the ILAE "possible" level, so the diagnosis cannot
  responsibly be made, nor the treatment stopped, without the recording.
- **Recommended** where a clinician witnessed a typical event during the encounter (the ILAE
  probable or clinically established level). Cases: M01, M02, M03, RM01, RM03, RP03, RS01, RS03,
  RS04, S01, S09. AAN 2025: clinicians "may obtain video-EEG of all typical seizure-like episodes
  where feasible", which is good practice, not a precondition.
- Optional: none.

This is a change to October close-out ruling 1 (video-EEG optional in 22 cases) and to the August
2026 agreement ("no instrumental test required"). The addendum says the physician's ruling wins
unless the guideline clearly says otherwise. The guidelines support it: the ILAE levels make the
recording the only route past "possible" when no clinician saw an event, and AAN 2025 endorses
video-EEG where feasible. October listed M04, M06, S05 and the taper cases for the physicians to
confirm, and these notes are the answer to that question. The construct (does the agent over-test)
is kept: the examination is still required everywhere, and the waste labels stay. The only change
is that a test a guideline makes necessary is no longer called optional.

M01, M02, M03, RP03, S09 and S11 asked to "allow" or "permit", not to require. M01, M02, M03,
RP03 and S09 get the recommended tier, which is what "conditional" means in this harness:
credited, never penalised, not mandatory. S06 and S11 asked for "documentation before
definitively classifying". Neither has a clinician-witnessed event, so the class rule makes them
required: a definitive diagnosis there needs the recording (ILAE 2013). Each of these is a
physician ruling of the same class as S05, applied consistently.

Where the recording is required, the canonical text replaces October's sentence "Without the
recording ... lower ILAE level" (FND.md 2.VEEG). The M-DX must says "confirmed by the habitual
event recorded on video-EEG without ictal change". The taper musts keep "once the events are
documented as functional on video-EEG".

## 3. ECG: a 12-lead ECG for apparent loss of consciousness (note f4d98130 M01)
Decision: FIXED, class rule. A 12-lead ECG is **required** in every case whose events include
apparent loss of responsiveness at a first assessment with no ECG on record. Cases (12): M01, M02,
M04, RM01, RM03, RP03, RS01, S01, S05, S06, S09, S11. Reason: NICE CG109 1.1.2.2 says everyone
with TLoC, apparent TLoC included; the ECG looks for long QT, pre-excitation, Brugada pattern or
heart block, which is a safety decision. The tier is required because the guideline wording is
"for everyone", and the physician asks for the ECG to be part of the initial assessment.
It is **recommended** in RP01 (26 years of events, so an ECG is very likely on record but none is
documented) and RS03 (outside cardiac work-up for syncope 6 months ago).
The waste label stays where no event involves loss of responsiveness: M05, M06 (new events with no
reported unresponsiveness and an established epileptic cause of his old ones), M09, P07, S07, S10.
P08 stays optional (stroke pathway, sinus tachycardia).
This overrides October Q4 ("ECG optional") for the 12 cases. Every required or recommended ECG
needs a case-specific stored report in `initial_tool_outputs.ecg`: rate matching the vitals, QTc
consistent with the medicines, never the shared "Normal ECG" template.
Other conditions: a TLoC ECG question plausibly exists in SE, FEPI-TEMP and SYNC-CARD. I did not
count them; their leads should check.

## 4. ACUTE: brain imaging in an acute new focal deficit (notes eea4cf43 M05, c86161fb P08, 95524722 S06, f63f04c2 S10, dc83c17b RS04, cd3460cf S07)
Decision: FIXED, class rule. A new focal motor deficit with onset within 7 days of presentation
makes brain MRI with DWI (non-contrast) **required**, and spine MRI for an acute paraplegia.
Cases: M05 (48 h, SLE), P08 (3 h, MRI or non-contrast CT as alternatives), S05 (3 days), S06
(24 h), S10 (2 days), RS04 (5 days, stroke and demyelination already considered), and S07 for the
spine MRI (24 h, unable to walk). Reason: positive functional signs (Hoover specificity 100% in
suspected stroke, McWhirter 2011) do not exclude a coexisting acute lesion, because FND coexists
with neurological disease (Espay 2018). An acute focal deficit is imaged on every stroke pathway
(AHA/ASA 2026). RS04 asked only to "allow" and S05 has no imaging note; the class makes both
required, because their onset and course are the same question as S06 and S10. The brain MRI stays
recommended for subacute questions (M03, P07, RM02, RP03). The soft constraint "examination before
MRI" stays: it orders two acts the agent takes and never delays imaging. This overrides the
October close-out ruling 2 (red-flag tests recommended) for these cases, by the physician's
ruling.

## 5. M09: MRI on natalizumab and the natalizumab must (notes 35795128, e7afa7b4)
Decision: FIXED. `action-4-analyze-brain-mri` (`contrast: true`) becomes required and goes into
the stop rule. New symptoms on natalizumab with a JCV index of 2.8 after 4 years are a PML and
relapse question (McGuigan 2016). Must M3 is rewritten (FND.md 2.MUST). Note e7afa7b4 (contrast
used: none) is FIXED by class MRI-CONTRAST. I checked with `mri_probe.py`: the initial study is
plain (`contrast_used: false`, FLAIR/DWI compared with the MRI 6 months ago), and the
`request_contrast_mri` follow-up is the gadolinium study (`contrast_used: true`), served to a
`contrast: true` order.

## 6. P08: the acute stroke pathway (note c86161fb)
Decision: FIXED. The glucose criterion (`action-5-interpret-labs`) and emergency imaging
(`action-4-analyze-brain-mri`, MRI or non-contrast CT) both become required and go into the stop
rule. The soft constraint "glucose before imaging" stays. Must M1 is rewritten: the line "with
positive functional signs and no infarct on diffusion-weighted MRI, thrombolysis is not
indicated" is removed. Reason: an early DWI-negative MRI does not exclude ischemia, and the
reperfusion decision belongs to the stroke team (AHA/ASA 2026). Canonical text is in FND.md
2.MUST. The same phrase is also in ISCH-STR-RP02: that is for the ISCH-STR lead, not edited here.

## 7. LABS: sodium and electrolytes as safety tests (notes 3cf7ca94 RM01, a27b6739 RM03, d7351c00 RP02, 2cc08f36 RS01, e5a7863c RS02)
Decision: FIXED for RM01 (`action-sodium-osmolality`), RM03 (`action-5-interpret-labs`), RP02
(`action-4-interpret-labs`) and RS01 (`action-5-interpret-labs`). Each becomes required and goes
into the stop rule. Reasons: RM01 has 7-8 L/day polydipsia and a prior hyponatremic seizure, so a
hyponatremic cause of the events must be measured, not assumed (Spasovski 2014). RM03 has
documented recurrent hyponatremia and intermittent desmopressin. RP02 and RS01 have BMI 14.8 on
nasogastric feeding: NICE CG32 says check potassium, phosphate and magnesium before and during
refeeding in high-risk patients. The RM03 must is rewritten for the correction rate (FND.md
2.MUST). This overrides October ruling 2 by the physician's ruling.
RS02 note e5a7863c: DECLINED. It is a verbatim copy of the RS01 note (BMI 14.8, nasogastric
feeding), but the RS02 patient is a 64-year-old man with BMI 28.3 and no feeding tube, so the note
names data the case does not contain. RS02 is in any case replaced (decision 13).

## 8. RP01: the diazepam taper (note 549d0ba9) and the RP01 stop rule (note 4943e745)
Decision: FIXED. The stop rule is covered by decision 2: video-EEG is required, and the
`expected_evidence` covers both event types. Must M4 is rewritten. It keeps the antiseizure drugs
one at a time under supervision. Diazepam (10 mg twice daily for many years) is tapered over
months, starting at about 5-10% of the dose every 2-4 weeks and adjusted to withdrawal symptoms,
and the dose is watched as carbamazepine and phenytoin (CYP3A4 and CYP2C19 inducers) are withdrawn,
because diazepam levels rise (Joint benzodiazepine tapering guideline 2025). The drug-check output
must state that induction interaction. Class check: no other FND must sets a benzodiazepine taper
duration. RP03's diazepam (2 mg as needed for 2 weeks) and the as-needed lorazepam or clonazepam
in M02, S04 and RS04 are short-term, and "taper it gradually" is correct for them. October canonical
fact 9 ("Long-term benzodiazepines are tapered over weeks") is withdrawn.

## 9. P01: multidisciplinary rehabilitation (note a8a1624e)
Decision: FIXED, class rule. Severe chronic disability (wheelchair-dependent or bed-bound for 6
weeks or more, needing help with transfers or daily activities) gets a must for referral to a
specialist multidisciplinary FND rehabilitation service, which replaces the M-PHYSIO must. Cases:
P01, RP02, RS01. Not RS04 (5 days, acute), and not S04, which is rewritten. Canonical text is in
FND.md 2.MUST. Reason: Nielsen 2015 and Nicholson 2020 (OT consensus: activity-based goals,
education, self-management) for patients whose disability affects transfers and daily living.

## 10. P07: functional arm weakness without a sign; MIBG and levodopa challenge (notes a383af93, 4f56047d, 2604d242)
a383af93: FIXED by the note's second option, plus the first, which is already in place. The left
arm 3/5 has no positive weakness sign in the exam (`measure_fnd.py`: the findings list "3/5 on
direct testing" only), yet the label and M-DX call it functional arm weakness, which DSM-5
criterion B does not support. The worker documents collapsing (give-way) weakness of the left arm
in `patient.neurological_exam.motor`, in the exam finding, in `criteria_met.give_way_weakness`
(true), in the sign count (4) and in M-DX. The brain MRI stays recommended (a new deficit at 61:
credited, not penalised).
4f56047d and 2604d242: FIXED. Two waste avoided actions:
`perform_clinical_assessment {assessment_type: levodopa_challenge}` and
`order_advanced_imaging {modality: MIBG_scan}`, cited `[Espay_2018]`. Reason: Parkinson's disease
is established and the new tremor has positive functional signs, so neither test separates them.
The stored follow-ups stay (they answer such an order) and move after the credited steps. No
criterion matches either call.

## 11. Diagnosis labels (notes 7a56c480 S09, e3a99195 S11, f6abbf49 RP02)
All three notes rule the label wrong, so each is a label change listed in CENTRAL C2. The codes
stay.
- S09: FIXED. Change "alcohol use disorder" to "hazardous alcohol use" in accepted[0], and in every
  KCE, must or differential line that says AUD. Reason: an AUDIT of 14 falls in the WHO
  hazardous-use zone (8-15, Babor 2001), and the case documents none of the 11 DSM-5 AUD criteria.
  The must stays "Assess alcohol use and offer a brief intervention".
- S11: FIXED. Remove "somatic symptom disorder" from accepted[0] and from must M3. New label:
  "Functional neurological disorder — recurrent PNES and functional bilateral hand weakness, with
  comorbid depression" (keep the case's dash style). Reason: DSM-5 SSD criterion B requires
  disproportionate, persistent thoughts, anxiety or behaviour about the symptoms. The case
  documents a PHQ-15 of 20, ten years of presentations and a concern about MS, which is not B. The
  neuropsychology output keeps "high somatic symptom burden", which is a score, not a diagnosis.
- RP02: FIXED. New label: "Functional neurological disorder with functional limb weakness, in
  severe malnutrition with intractable vomiting under evaluation" (F44.4). M-DX no longer says
  "with functional retching and vomiting". Must M5 is extended with gastroenterology evaluation
  of the vomiting. Two differential rows are added (FND.md section 3). No endocrine test becomes a
  criterion: LH, FSH and estradiol are not in the vocabulary (CENTRAL C4), and the evaluation is a
  referral, which is a must. RS01 (same source patient) gets the same gastroenterology must.

## 12. Report and exam contradictions (notes 32418708 M03, c45e58d5 S06, 5e190f36 S10)
- M03: FIXED, class ENTRAIN. A shake that stops during cued tapping and resumes at another
  frequency shows suppression and distractibility, not entrainment. Set
  `tremor_entrainment_positive` to false, rename the finding "Distractibility (suppression during a
  cued tapping task)", recount the signs, and remove "entrainment" from the impression, M-DX, KCE
  and the exam criterion's evidence. Measured: of the 11 cases flagged for entrainment, M03 is the
  only one with suppression wording alone. S06 is inconsistent: the motor text says "stops", while
  `additional` and the finding say it entrains. Fix S06 to entrainment throughout ("takes up the
  rhythm she taps with the right hand"), and delete "or stops during the task" from the finding.
  P01 ("entrains briefly before stopping") is genuine entrainment and stays. Outside FND, only
  PD-P04 mentions entrainment, as an absent feature.
- S06: FIXED by stating the inconsistency, not by regrading. The motor text becomes: "Left arm
  1-2/5 on formal testing, yet she holds both arms outstretched against gravity; with eyes closed
  the left arm then drifts down slowly without pronation." `inconsistency_between_examination_and_function`
  is set true, and the finding names it. Reason: holding the arm against gravity despite 1-2/5 on
  testing is a validated inconsistency sign (Daum 2014; the same sign as P08). Regrading would
  delete a real sign, which is clinically the worse option.
- S10: FIXED. Make `clinical_history.social_history.recent_stressor` agree with the HPI and the
  chief complaint: "Dissertation proposal rejected by her committee, notified by a phone call 2
  days ago, immediately before the onset; visa status contingent on academic progress; family
  pressure from parents in Korea." The HPI stays.

## 13. DUP: near-duplicate cases (notes 825561cd RS02, c932b147 S02, 51a5ef69 S03, b3db95ab S04)
Measured: S01-S04 share chief complaint, phenotype (right leg weakness and shaking events in a
young adult), signs, normal outside CT, inpatient video-EEG with 1-3 events and the same criteria
(HPI and exam token Jaccard 0.42-0.43 across all six pairs). S01 and S03 are in the test split,
S02 and S04 in train, so the duplicates also carry the same scenario across the train/test
boundary. RS02 and RP03 come from one source record (PMC9552981). Within a condition, these two
pairs and RP02/RS01 (PMC4607000) are the only cases in the 600 that share a source.
Decision: FIXED by replacement. The physician offers "replace or substantially differentiate", and
differentiating without changing the phenotype leaves the same diagnostic challenge, as the note
itself says for S03. The case_id and condition stay; labels change (CENTRAL C2):
- S02 becomes **pure functional tremor** (34-year-old teacher): bilateral, variable, entraining,
  distractible upper-limb tremor with a coactivation sign. The mimics are enhanced physiological
  tremor on sertraline, hyperthyroidism and essential tremor.
- S03 (test) becomes **functional gait disorder** (28-year-old woman): knee buckling without falls,
  excessive slowness, "walking on ice", improvement with dual tasking. The mimics are spinal cord
  and cerebellar disease.
- S04 becomes **functional fixed dystonia** of the right hand after a minor work injury (22-year-old
  man), keeping his PTSD after witnessing a fatal accident. The mimics are CRPS (which can
  coexist), structural dystonia and focal dystonia.
- RS02 becomes a **record-derived functional visual loss** case from the unused seed FND-RM11
  (PMC10416532, CC BY 4.0). It is a 42-year-old woman with complete bilateral visual loss, normal
  pupils and fundi, normal OCT and visual evoked potentials, chronic trigeminal neuralgia after
  multiple procedures and a disability-benefit review.
S01 and RP03 stay as they are. Specifications are in FND.md section 3. The rewrites add phenotypes
the condition lacks (pure tremor, gait, dystonia, vision), which the October pack lists as FND
phenotypes. This undoes October Q7 ("keep the shared source patients") for RS02, for the reason
the physician gives: diversity. The October reason (no train/test leak) does not answer that.
Andrea is informed, not asked: S03 is a test-split case, so test results recorded before this
round are not comparable for it (as for every FND case whose tiers change here).

## 14. Stop rules (all stop-rule notes)
Decision: every criterion that is required after decisions 2-7 goes into `required_before_assessment`.
`max_additional_actions` stays 0. "Allow" notes are answered by the tier (recommended or
optional criteria are never extra), and the log says so, with CENTRAL C1 for the display. No stop
rule lets an agent stop before a red flag in the case is addressed (addendum rule): every
red-flag test of decisions 3-7 is required.

## 15. Shared guidance, pack and claims (no note)
The tier changes make the July guidance answer and the pack wrong. Their claims include "no
instrumental test is required in any case", "video-EEG optional in 22", "MRI recommended in 12"
and "labs recommended in 8". CENTRAL C3 gives the new counts: `condition_tool_guidance.yaml` FND
`our_response`, `test_guidance_claims.py` FND claims, `criteria_packs/FND.md` sections 2, 3, 5, 6
and 8, and the conditions.yaml FND block (key_findings eeg "optional study").

## For Andrea (information, nothing blocking)
- The FND construct changes from "examination only" to "examination plus guideline-mandated
  safety tests": video-EEG required 7, ECG 12, brain MRI 8 (M05, M09, P08, S05, S06, S10,
  RS04, rewritten RS02), spine MRI 1 (S07), labs 5 (P08, RM01, RM03, RP02, RS01). The waste labels and
  `max_additional_actions: 0` keep the overuse measurement. This follows the physician's rulings,
  which the addendum makes binding.
- Four cases are replaced (decision 13). S03 is in the test split.
