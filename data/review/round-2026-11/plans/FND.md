# FND: condition plan for the November 2026 review round

Lead plan for the 30 `functional_neurological_disorder` cases. Read `round-2026-10/ROUND_POLICY.md`,
`work/NOVEMBER_ADDENDUM.md`, `plans/FND-decisions.md` (the reasons and citations: this plan does
not repeat them), `criteria_packs/FND.md`, `docs/benchmark/tool-contract.md` and
`TOOL_REPORT_STYLE_GUIDE.md` first. 73 notes, all from R1, in 30 cases. No FND case is approved.
Helpers are in `data/review/round-2026-11/bin/` (`case_io.py`, `perfect_agent.py`, `caselog.py`,
`mri_probe.py`). Run `uv run python -I` from `/home/aprotani/projects/ma-round11`.

Use:
1. Apply every class of section 2 that names your case. Use the canonical text verbatim, with the
   `<...>` slots filled from the case.
2. Then apply the section 3 entry for the case. For the four rewritten cases (S02, S03, S04,
   RS02), build the case to the specification in 3.R.
3. Order `action_criteria` and `followup_outputs` as in 2.ORDER. Keep every existing
   `criterion_id`.
4. Run `perfect_agent.py CASE -v`, `case_io.py check CASE`, and `mri_probe.py CASE` after any MRI
   edit. With `-v`, confirm that each required or recommended criterion receives the case's own
   report.
5. Write the log with `caselog.py`. Every note id of the case goes in it, with the ruling of
   section 3.

American spelling (hyponatremia, behavior), as in the cases. No em or en dashes in new text. The
existing labels keep their " — " separator. Nothing about the review process goes in `metadata`.

---

## 1. Governing guidelines and canonical facts

| question | governing source | key |
| --- | --- | --- |
| Positive diagnosis, coexistence with neurological disease | Espay 2018; DSM-5 criterion B | `[Espay_2018]`, `[DSM5_FND]` |
| Validated signs | Daum 2014; Hoover in suspected stroke, McWhirter 2011 | `[Daum_2014]`, `[McWhirter_2011]` |
| Certainty of functional seizures | ILAE 2013 (LaFrance) | `[ILAE_PNES_2013]` |
| Evaluation and drugs in functional seizures | AAN 2025 (Tolchin, Neurology 2026;106:e214466) | `[AAN_Functional_Seizures_2025]` |
| ECG after (apparent) TLoC | NICE CG109 1.1.2.2 | `[NICE_CG109]` |
| Acute focal deficit, glucose, reperfusion decision | AHA/ASA 2026 (Prabhakaran, Stroke 2026;57:e316-e436) | `[AHA_ASA_Stroke_2026]` |
| Natalizumab PML risk | McGuigan 2016 (free text, pack) | none |
| Hyponatremia correction | Spasovski 2014 (free text, pack) | none |
| Refeeding | NICE CG32 (free text, pack) | none |
| Benzodiazepine taper | Joint Clinical Practice Guideline on Benzodiazepine Tapering, J Gen Intern Med 2025 | free text |
| Rehabilitation | Nielsen 2015; Nicholson C et al. J Neurol Neurosurg Psychiatry 2020;91:1037-1045 (OT consensus) | `[Nielsen_2015]`, free text |
| Alcohol | WHO AUDIT manual (Babor 2001): 8-15 hazardous, 16-19 harmful, 20 or more possible dependence; DSM-5 AUD needs 2 of 11 criteria | free text |

Canonical facts. They add to the October list (`round-2026-10/plans/FND.md` 1.2), which is still
in force except fact 9 (replaced by F7 below):
- F1. The ILAE levels. If no clinician witnessed a habitual event, the history alone gives
  "possible" functional seizures. A typical event witnessed by a clinician, with an EEG without
  ictal activity, gives "probable" or "clinically established". A habitual event on video-EEG
  without ictal change gives "documented".
- F2. AAN 2025: "may obtain video-EEG of all typical seizure-like episodes where feasible".
  Evaluate for co-occurring epilepsy (about 22%, Kutlubaev 2018). Taper antiseizure drugs that
  have no other indication.
- F3. NICE CG109: a 12-lead ECG for everyone with transient loss of consciousness, apparent loss
  included. It screens for long QT, pre-excitation, Brugada pattern and heart block.
- F4. Positive signs do not exclude a coexisting acute lesion. A new focal deficit of 7 days or
  less is imaged (MRI with DWI; non-contrast CT is acceptable within the acute stroke window).
- F5. An early DWI-negative MRI does not exclude ischemic stroke. The stroke team makes the
  reperfusion decision from the deficit, the imaging, the time from onset and eligibility,
  after a glucose check.
- F6. Chronic hyponatremia with primary polydipsia: once desmopressin is stopped, a water diuresis
  can correct sodium too fast. Limit the rise to 10 mmol/L in the first 24 h and 8 mmol/L in each
  further 24 h (Spasovski 2014).
- F7. Long-term benzodiazepines: the taper takes months. Start with reductions of about 5-10%
  every 2-4 weeks and adjust to withdrawal symptoms (Joint guideline 2025). Carbamazepine and
  phenytoin induce diazepam metabolism, so diazepam levels rise as they are withdrawn.
- F8. Entrainment means the tremor adopts the imposed rhythm. A tremor that only stops during the
  task shows suppression or distractibility.
- F9. An AUDIT of 14 is hazardous use, not alcohol use disorder. Somatic symptom disorder needs
  DSM-5 criterion B (disproportionate thoughts, anxiety or behaviour), not a PHQ-15 score.

---

## 2. Classes

### LIT (34 notes, 30 cases). FIXED by class LIT, commit 393c547e
Measured: 0 of 30 FND cases, and 0 of 600, still have a literature criterion or output. In every
log, rule each LIT note FIXED ("class LIT, commit 393c547e; checked: no literature criterion or
output left"). Add nothing back.

### VEEG (11 notes: M01, M02, M03, M04, M06, RP01, RP03, S05, S06, S09, S11)
Measured (`measure_fnd.py`): 22 paroxysmal cases today. After the rewrites, 18 remain. All have a
stored video-EEG, all are optional, and none is in a stop rule. "Clinician witnessed an event"
here means `criteria_met.functional_seizure_semiology_observed` is true. That holds in M01, M02,
M03, M04, RM01, RM03, RP03, RS01, RS03, RS04, S01 and S09. It is false in M06, P01, RP01, S05,
S06 and S11.

Rule:
- **required**: M04, M06, P01, RP01, S05, S06, S11. Add the EEG criterion id to
  `required_before_assessment`.
- **recommended**: M01, M02, M03, RM01, RM03, RP03, RS01, RS03, RS04, S01, S09.

Canonical rationale, required (no event seen): "No habitual event has been seen by a clinician,
only described by <witness>, so the history supports functional seizures only at the possible
level; a habitual event recorded on video-EEG without ictal change documents the diagnosis and
screens for co-occurring epilepsy<, before ...>. (ILAE 2013; AAN 2025)". M04 instead: "The
observed event (eyelid flutter with brief unresponsiveness and immediate recovery, some events
triggered by light) cannot be separated at the bedside from absence seizures or eyelid myoclonia,
and the examination has no positive functional sign, so only a habitual event recorded on
video-EEG, with hyperventilation and photic stimulation, can establish the diagnosis (ILAE 2013;
AAN 2025)". M06 adds "in a man with established right temporal lobe epilepsy and interictal
discharges", and RP01 adds "before 26 years of antiseizure treatment is withdrawn".
Canonical rationale, recommended: "A typical event was witnessed on examination, which supports
the diagnosis at the clinically established level; recording a habitual event on video-EEG raises
it to documented and screens for co-occurring epilepsy, as the AAN guideline advises where
feasible (ILAE 2013; AAN 2025)."
Citations: `[ILAE_PNES_2013]`, `[AAN_Functional_Seizures_2025]`. Delete October's sentence
"Without the recording ... (LaFrance 2013)" wherever it appears. M-DX in the required cases says
"... and the habitual event recorded on video-EEG without ictal change". In recommended cases it
keeps "confirmed on video-EEG where recorded". Check that KCE, `difficulty_rationale` and the
differential do not still call the EEG optional.

### ECG (1 note: M01 f4d98130; class over 14 cases)
Measured: an ECG criterion exists in M01, M02, M04, RM01, S01, S05, S06, S09 and S11 (all
optional) and in P08 (optional). All but P08 are answered only by the template fallback "Normal
ECG". Events with apparent unresponsiveness (from the HPI and the exam text): M01, M02, M04, RM01,
RM03, RP01 (unresponsive type), RP03, RS01, RS03, S01, S05, S06, S09, S11. Events with preserved
awareness (no TLoC): P01, RS04, and today's S02, S03 and S04.

Rule:
- **required**: M01, M02, M04, RM01, RM03, RP03, RS01, S01, S05, S06, S09, S11. Add `action-ecg`
  to the stop rule. Create the criterion where it is missing (RM03, RP03, RS01) with id
  `action-ecg`.
- **recommended**: RP01, RS03 (new `action-ecg`).
- Unchanged: waste in M05, M06, M09, P07, S07, S10; optional in P08.

Canonical criterion: label "12-lead ECG"; tool `analyze_ecg {}`; citations `[NICE_CG109]`.
Rationale: "Her events include apparent loss of responsiveness; NICE advises a 12-lead ECG for
everyone with transient loss of consciousness, to look for a cardiac cause such as long QT,
pre-excitation, a Brugada pattern or heart block." Use "His" where male. Add "and her medicines
include <QT drug>" where it applies: RS01 metoclopramide with Mg 1.6, RM03 ondansetron, RM01
risperidone. Expected evidence: "<rhythm and rate>, normal PR, QRS and QTc".

Data: store a case-specific `initial_tool_outputs.ecg` in each required or recommended case, with
the rate equal to the vitals heart rate (plus or minus 5), a QTc consistent with the medicines and
electrolytes, and an `interpretation` in report voice. Keep RM01's incomplete RBBB, and move it
from the fallback into the initial output. Null the fallback `ecg` in those cases. Never reuse the
template "Normal ECG" text verbatim.

### ACUTE: acute focal deficit imaging (notes M05 eea4cf43, P08 c86161fb, S06 95524722, S10 f63f04c2, RS04 dc83c17b, S07 cd3460cf)
Measured onset at presentation: P08 3 h, S06 24 h, S07 24 h, M05 48 h, S10 2 days, S05 3 days,
RS04 5 days. Every other motor case has a course of 3 weeks or more. Today every MRI among them
is recommended, and none is in a stop rule.

Rule: brain MRI with DWI, non-contrast (`analyze_brain_mri {contrast: false}`), is **required** in
M05, S05, S06, S10 and RS04. In P08 the existing alternatives are MRI `{}` and CT
`{contrast: false}`. In S07, `action-spine-mri` (`order_body_imaging {study: spine_MRI}`) is
required and the brain MRI stays optional. Each goes into the stop rule. Keep the soft constraint
"examination before MRI". Canonical rationale: "A new focal deficit of <n hours or days> is imaged
whatever the examination shows: positive functional signs do not exclude a coexisting acute
<infarct | demyelinating lesion | cord lesion>, since functional disorder coexists with
neurological disease (Espay 2018; AHA/ASA 2026)." Citations: `[Espay_2018]`,
`[AHA_ASA_Stroke_2026]`; S07 `[Espay_2018]` only. The stored MRI must state DWI/ADC (already true
in all of them; confirm with `mri_probe.py`).

### LABS: safety labs (notes RM01 3cf7ca94, RM03 a27b6739, RP02 d7351c00, RS01 2cc08f36, P08 c86161fb)
Required, and into the stop rule: P08 `action-5-interpret-labs` (glucose), RM01
`action-sodium-osmolality`, RM03 `action-5-interpret-labs`, RP02 `action-4-interpret-labs`,
RS01 `action-5-interpret-labs`. The stored panels already exist. Check that each criterion's
`expected_evidence` cites only panels its own order names (SKILL_NOTES, lab routing). Rewrite the
rationale to say "safety" ("must be measured, not assumed"), with the source: Spasovski 2014 for
RM01 and RM03, NICE CG32 for RP02 and RS01, AHA/ASA 2026 for P08.

### MUST: musts rewritten or added (canonical text)
- **P08 M1** (replace): "Manage as a suspected acute stroke: check capillary glucose before any
  reperfusion decision, obtain emergency brain imaging, and ask the stroke team to decide on
  thrombolysis from the deficit, the imaging, the time from onset and eligibility; a normal early
  diffusion-weighted MRI does not exclude ischemic stroke, and positive functional signs alone do
  not decide it."
- **M09 M3** (replace): "Review the natalizumab risk with her MS team: a JC virus antibody index of
  2.8 after 4 years of treatment means a high PML risk, so discuss switching or extended-interval
  dosing with MRI surveillance; if PML cannot be excluded on the MRI, withhold the next infusion
  pending specialist evaluation. Do not change treatment because of the functional weakness."
- **RM03 M6** (replace): "Restrict fluid intake after stopping desmopressin, measure serum sodium
  every 4 to 6 hours with a fluid balance and urine output chart for the first 48 hours, and keep
  the rise in sodium to no more than 10 mmol/L in the first 24 hours and 8 mmol/L in each further
  24 hours, since a water diuresis can correct chronic hyponatremia too fast; review sertraline (a
  cause of SIADH) with her psychiatrist." M5 ("Stop desmopressin ...") stays.
- **RP01 M4** (replace): "Taper and stop carbamazepine and phenytoin one at a time under
  neurological supervision once the events are documented as functional on video-EEG with no
  evidence of epilepsy; then taper diazepam slowly over months, starting with reductions of about
  5 to 10% of the dose every 2 to 4 weeks adjusted to withdrawal symptoms, and watch for rising
  diazepam levels and sedation as the enzyme-inducing carbamazepine and phenytoin are withdrawn."
  The drug-check output must contain the induction interaction (carbamazepine and phenytoin with
  diazepam: CYP3A4 and CYP2C19 induction).
- **MDT** (P01, RP02, RS01; replaces the M-PHYSIO must): "Refer to a specialist multidisciplinary
  rehabilitation service for functional neurological disorder (physiotherapy, occupational
  therapy with a functional independence and equipment plan, and psychological therapy), given
  <her disability: P01 three months of full-time wheelchair use with help for transfers and daily
  activities; RP02 and RS01 four months unable to stand, starting once medically stable>." Cite
  Nielsen 2015 and Nicholson 2020 in the log, not in the must.
- **GI** (RP02, extending M5; RS01, a new must): "Refer for gastroenterology evaluation of the
  intractable vomiting before attributing it to the functional disorder." RP02 M5 keeps the
  endocrine and gynecological evaluation of the primary amenorrhea.

### ENTRAIN (note M03 32418708; class measured over 11 cases)
Measured: 11 cases flag `tremor_entrainment_positive` or use the word. M03 has only suppression
wording, so it must change. S06's text is inconsistent ("stops" in the motor text, "entrains" in
`additional`), and is fixed to entrainment throughout. P01 ("entrains briefly before stopping") is
correct. The rest describe adoption of the rhythm. Details are in decisions 12.

### DX: labels (S09 7a56c480, S11 e3a99195, RP02 f6abbf49)
New accepted[0] labels, which are label changes for CENTRAL C2:
- S09: "Functional neurological disorder — right-sided functional hemimotor syndrome and PNES, with
  comorbid PTSD and hazardous alcohol use".
- S11: "Functional neurological disorder — recurrent PNES and functional bilateral hand weakness,
  with comorbid depression".
- RP02: "Functional neurological disorder with functional limb weakness, in severe malnutrition
  with intractable vomiting under evaluation".
Edit only accepted[0]. Do not touch the synonym labels after it. Grep each case for the old
phrases (KCE, differential, musts, `metadata.condition_name`, `sub_domain`) and align them.

### DUP: four replaced cases (S02 c932b147, S03 51a5ef69, S04 b3db95ab, RS02 825561cd)
Measured: HPI and exam token Jaccard 0.42-0.43 between every pair of S01-S04, with identical
criteria sets. S01 and S03 are in the test split, S02 and S04 in train. RS02 and RP03 share
PMC9552981. Specifications are in 3.R.

### AVOID: P07 (4f56047d, 2604d242)
Add `avoid-waste-mibg-scan` (`order_advanced_imaging {modality: MIBG_scan}`) and
`avoid-waste-levodopa-challenge` (`perform_clinical_assessment {assessment_type:
levodopa_challenge}`), severity waste, citation `[Espay_2018]`. Rationales: "Parkinson's disease
is established and stable; cardiac MIBG cannot separate a functional tremor from parkinsonian
progression." and "A levodopa challenge measures her known levodopa-responsive parkinsonism and
cannot separate the new functional tremor from it." Move both stored follow-ups after the
credited steps.

### ORDER (all cases): criteria and follow-up order
Use this order:
1. Examination (P08: glucose first, then the examination).
2. Required safety tests: ECG, labs, acute imaging.
3. Recommended imaging.
4. Video-EEG.
5. Drug check.
6. Neuropsychology.
7. On-request answers that match no criterion (performance status, cognitive screen, P07
   levodopa challenge and MIBG, skin biopsy), last.

Keep the soft constraints that exist. Add no constraint on an optional criterion.

### STOP (all cases)
`required_before_assessment` = every required criterion id, and `max_additional_actions` stays 0.
For each "allow" note, the log says: "the test is a <recommended/optional> criterion, and actions
matching a criterion are never counted as extra (`policy_reward.py`, stopping); display: CENTRAL
C1".

---

## 3. Per-case index (all 30; no case is approved)

The LIT ruling of section 2 applies to every LIT note listed. "Required" = the criterion becomes
required and enters the stop rule.

**FND-M01**
- f20dfdfa-c265-4339-b145-edb2bbccdcab (lit): FIXED, LIT.
- ccddb06a-ad4f-47c6-a96e-7b43f5450c98 (stop rule): FIXED, VEEG. `action-5-analyze-eeg` becomes
  recommended (event witnessed).
- f4d98130-b464-427f-a70c-aed28fd1d75b (ECG): FIXED, ECG. `action-ecg` becomes required, with a
  stored ECG.
- Stop rule: exam and ECG.

**FND-M02**
- ea6a9490-55f2-4ae1-b465-fcb4bd259d6d: FIXED, LIT.
- 52f87e18-d04f-4d32-a0ef-bac0d18e4883: FIXED, VEEG. Video-EEG becomes recommended. The taper
  must keeps "once the events are securely diagnosed as functional (ideally with a habitual event
  documented on video-EEG)".
- Class ECG: required.
- Stop rule: exam, drug check, ECG.

**FND-M03**
- fd6b12e4-a61a-4d8d-a9bd-5852e4b478df and 06d86723-7c9f-4e07-89b5-02ee96d764dd: FIXED, LIT.
- 3327b25f-0090-4904-b36a-3a09695c1c15: FIXED, VEEG plus STOP. The MRI stays recommended (the
  subacute post-event deficit). Video-EEG becomes recommended.
- 32418708-6942-4b51-b24e-96b215dd9077: FIXED, ENTRAIN. Change the finding, the flag, the count,
  the impression, M-DX, KCE and the exam `expected_evidence`. The HPI already describes
  suppression.
- No ECG: the events have preserved responsiveness.

**FND-M04**
- 30667d14-c75b-4d3e-969b-e432be789704 and 80fea3da-bfa5-40ae-814e-9c8633ef8582: FIXED, LIT.
- 6a40c3ea-beba-4019-8b02-a23bb34772d4: FIXED, VEEG. `action-4-analyze-eeg` becomes required,
  with the M04 rationale. Confirm that the stored EEG lists hyperventilation and photic
  stimulation.
- Class ECG: required.
- Stop rule: exam, video-EEG, ECG.
- In the differential, "Absence epilepsy or eyelid myoclonia" stays low, citing the recording.

**FND-M05**
- 82744d6f-48de-4093-b30c-b04238c6e0af and b9f0043f-0537-4034-96fc-246819bd0b03: FIXED, LIT.
- eea4cf43-6ef6-44a1-bdc5-6b1b807599d1: FIXED, ACUTE. `action-4-analyze-brain-mri` becomes
  required.
- Stop rule: exam and MRI.
- The labs stay recommended. ECG stays waste: no TLoC.

**FND-M06**
- 546d3260-e538-4cef-82e0-50b885b08a98: FIXED, LIT.
- a37be9ec-168a-403a-bf52-20d3ad1ed453: FIXED, VEEG. `action-4-analyze-eeg` becomes required
  (M06 rationale).
- Stop rule: exam and video-EEG. ECG stays waste.

**FND-M09**
- 95e72dff-2634-4a25-bc51-8decfc8fdcac and ef67e7eb-6e5e-4367-bbff-8c5012840d94: FIXED, LIT.
- 35795128-9486-4448-845c-827ebc2c5343: FIXED. `action-4-analyze-brain-mri` (`contrast: true`)
  becomes required, and M3 becomes the MUST text.
- e7afa7b4-2462-4cbe-b3d7-751217d8168f: FIXED, class MRI-CONTRAST. Checked: the initial study is
  plain with FLAIR and DWI compared with the prior; the gadolinium follow-up has
  `contrast_used: true`.
- Stop rule: exam and MRI.

**FND-P01**
- b7b2460d-344d-4a91-86c4-1fee2f8d2475: FIXED, LIT.
- a8a1624e-b1b7-4cbc-8fad-79ed53bcac0a: FIXED, MDT. The must replaces the M-PHYSIO must (M2).
- Class VEEG: `action-5-analyze-eeg` becomes required (no event witnessed).
- Stop rule: exam and video-EEG. No ECG: awareness is retained.

**FND-P07**
- 3a7cedc9-ba33-4303-8416-cc281132c636: FIXED, LIT.
- a383af93-db33-4fbf-9c6c-4e37303b2c25: FIXED (decision 10). Document collapsing weakness of the
  left arm (exam text, finding, `give_way_weakness: true`, count 4, M-DX). The MRI stays
  recommended.
- 4f56047d-ac28-43f6-a926-786d0906a19d and 2604d242-ec20-47b5-b5b7-0ab709ed8a1a: FIXED, AVOID.

**FND-P08**
- 7942bc89-912f-4b38-8bd7-cdc5ecd88b60: FIXED, LIT.
- c86161fb-1e63-4264-9ac0-7312185c5234: FIXED, LABS plus ACUTE plus MUST. Glucose
  (`action-5-interpret-labs`) and imaging (`action-4-analyze-brain-mri`) become required, and M1
  is replaced.
- Stop rule: glucose, exam, imaging. The CTA and the ECG stay optional.

**FND-RM01**
- 18418180-1168-4313-bb17-e1f62cfdd234: FIXED, LIT.
- 3cf7ca94-cfd3-498c-ab7a-a248242d7843: FIXED, LABS. `action-sodium-osmolality` becomes required.
- Class ECG: required (risperidone in the rationale; keep the incomplete RBBB).
- Class VEEG: recommended.
- Stop rule: exam, sodium, ECG.

**FND-RM02**
- 7db59db3-25ec-41b0-a077-3af9fdd02fa5: FIXED, LIT.
- No class finding: the MRI stays recommended.

**FND-RM03**
- 50e42ac1-cfd9-4f21-888f-189b2dfe43a9: FIXED, LIT.
- a27b6739-f7dd-4af1-9b91-5d0119d1a63d: FIXED, LABS plus MUST. `action-5-interpret-labs` becomes
  required, and M6 is replaced.
- Class ECG: new required `action-ecg` (ondansetron).
- Class VEEG: recommended.
- Stop rule: exam, drug check, labs, ECG.

**FND-RP01**
- dc91a67d-76bd-48fd-b5fe-cb19d92f7eee: FIXED, LIT.
- 4943e745-944a-4cb1-b882-371018f345e9: FIXED, VEEG. `action-4-analyze-eeg` becomes required, and
  its evidence names both event types.
- 549d0ba9-4eee-4a59-90e8-d172c59ace36: FIXED, MUST RP01 M4. Add the induction interaction to the
  drug-check output.
- Class ECG: new recommended `action-ecg`.
- Stop rule: exam, drug check, video-EEG.

**FND-RP02**
- 71b3a3cf-1351-48d3-b20a-1ee6a6843e83: FIXED, LIT.
- d7351c00-4787-40ef-b3f1-1e96eed4f7cb: FIXED, LABS. `action-4-interpret-labs` becomes required.
  Thiamine and refeeding are already in M4.
- f6abbf49-6a51-4105-a75e-d83dae4b29a6: FIXED, DX plus GI. Change M-DX to the functional limb
  weakness only. Differential: add "Hypothalamic-pituitary disorder (primary amenorrhea with absent
  puberty, vomiting and weight loss)", low, key features "head CT normal; needs endocrine
  evaluation and pituitary imaging if gonadotropins are low"; and "Upper gastrointestinal disease
  (peptic ulcer, motility disorder)", low, key features "treated empirically for peptic ulcer
  without endoscopy; gastroenterology evaluation pending".
- Class MDT: replaces M2.
- Stop rule: exam and labs.

**FND-RP03**
- 4dc5ddb4-dad0-41b7-b408-61c61e631a68: FIXED, LIT.
- 384cf96b-5922-4590-8dfd-2fc3ed87d928: FIXED, VEEG plus STOP. The MRI stays recommended, and
  video-EEG becomes recommended.
- Class ECG: new required `action-ecg` (apparent unresponsiveness phase).
- Stop rule: exam, drug check, ECG.
- Keep RP03 unchanged otherwise. Its pair RS02 is replaced.

**FND-RS01**
- 2b7000f8-6d09-47fd-a2be-3b7c6ca5f296: FIXED, LIT.
- 2cc08f36-b79f-4ae0-bdc7-b086ec1d5f63: FIXED, LABS. `action-5-interpret-labs` becomes required.
- Class ECG: new required `action-ecg` (metoclopramide, Mg 1.6).
- Class VEEG: recommended.
- Class MDT and GI: musts.
- Stop rule: exam, drug check, labs, ECG.

**FND-RS02**
- ed1c0cbd-fdcd-48c1-a879-7aec3815426b: FIXED, LIT (also moot after the rewrite).
- 825561cd-6cf4-4930-9310-eab4b29492b7: FIXED, DUP. Rewrite to 3.R RS02.
- e5a7863c-f0de-46f1-beb8-f4540c8b51a4: DECLINED. The note copies the RS01 note (BMI 14.8,
  nasogastric feeding), but the RS02 patient has BMI 28.3 and no feeding tube.

**FND-RS03**
- 64653b84-2c6b-46b3-bf87-284839cbc92a: FIXED, LIT.
- Class VEEG: recommended.
- Class ECG: new recommended `action-ecg` (outside cardiac work-up 6 months ago).

**FND-RS04**
- efb943da-7b3a-49d1-a461-6fcc4fb2cdfd: FIXED, LIT.
- dc83c17b-29fe-4568-b98f-dc02917651a1: FIXED, ACUTE. `action-4-analyze-brain-mri` becomes
  required.
- Class VEEG: recommended. No ECG: aware during events.
- Stop rule: exam and MRI.

**FND-S01**
- c8b24f69-26eb-411e-8eb7-681163c62d96: FIXED, LIT.
- Class ECG: required. Class VEEG: recommended.
- S01 stays the reference case of the S series and is not rewritten.
- Stop rule: exam and ECG.

**FND-S02**
- cd93e93c-a6f5-484e-98d2-8b00740fd80f: FIXED, LIT.
- c932b147-ba9b-4e2d-aed4-9d1f512e580d: FIXED, DUP. Rewrite to 3.R S02.

**FND-S03** (test split)
- 99505307-c430-4dd7-a96e-628a4905e9d0: FIXED, LIT.
- 51a5ef69-73de-4038-8bf1-4cfc7d5be8f6: FIXED, DUP. Rewrite to 3.R S03.

**FND-S04**
- 9ca356f3-f610-454d-855f-314321297ec5: FIXED, LIT.
- b3db95ab-56b2-4faa-b918-94da7e39f52d: FIXED, DUP. Rewrite to 3.R S04.

**FND-S05**
- 53b45079-87e7-43cd-b046-e696ec4fa2b0: FIXED, LIT.
- 4b564a53-7606-440e-ac78-a22c17c22cfe: FIXED, VEEG. `action-5-analyze-eeg` becomes required.
- Class ACUTE: MRI required. Class ECG: required.
- Stop rule: exam, MRI, ECG, video-EEG.

**FND-S06**
- f1700eb4-53cf-49e0-aa31-7a2ae7cf35f9: FIXED, LIT.
- 95524722-958b-4ae5-97ae-1eda2398ebd0: FIXED, ACUTE plus VEEG. MRI and video-EEG both become
  required.
- c45e58d5-01c1-43e8-9978-5f485d5edb13: FIXED (decision 12): state the inconsistency.
- Class ENTRAIN: entrainment throughout. Class ECG: required.
- Stop rule: exam, MRI, ECG, video-EEG.

**FND-S07**
- 4e4c7f64-6fae-43e4-8dc1-e953d459571f: FIXED, LIT.
- cd3460cf-ef35-47cb-a82f-388e448d2fb7: FIXED, ACUTE. `action-spine-mri` becomes required; the
  brain MRI stays optional.
- Stop rule: exam and spine MRI.

**FND-S09**
- 03adcbc7-b5eb-4337-a0b4-3c0806c30658: FIXED, LIT.
- 7896a50e-1daa-40bf-9b80-bf8d45b4f5a9: FIXED, VEEG. Video-EEG becomes recommended (episode
  observed on the ward).
- 7a56c480-eb38-44dc-bda8-82b604243713: FIXED, DX (hazardous alcohol use).
- Class ECG: required.
- Stop rule: exam and ECG.

**FND-S10**
- 320b9e74-3b17-4136-8777-85d6e1f04f6f: FIXED, LIT.
- f63f04c2-b063-4309-a8c8-666c49392caa: FIXED, ACUTE. The MRI becomes required.
- 5e190f36-d854-459f-9a5e-9928f037e074: FIXED (decision 12), social history.
- Stop rule: exam and MRI.

**FND-S11**
- 48159203-521c-4e99-8cee-9685ac8d68b4: FIXED, LIT.
- b7bfdbac-1e1d-49b5-8616-109c078f70cd: FIXED, VEEG. `action-4-analyze-eeg` becomes required.
- e3a99195-0f15-4413-a203-8233013eff7b: FIXED, DX. Remove SSD from the label and from M3.
- Class ECG: required.
- Stop rule: exam, ECG, video-EEG.

### 3.R Specifications for the four replaced cases
Common to all four:
- Keep `case_id`, `condition`, `encounter_type`, `review_status: draft`, `schema_version`.
- Rewrite `patient` and every output, criterion, avoided action, must, prohibition, differential,
  KCE, red herring and `metadata` text. Drop the old video-EEG, the old MRI and every trace of the
  old scenario.
- Grep the finished case for "PNES", "shaking", "seizure", "levetiracetam", "Hoover", "EGPA" and
  "vasculitis". Each surviving hit must belong to the new scenario.
- Use the October canonical musts M-DX, M-COMM, M-PSY and M-PHYSIO (the motor cases), and
  prohibitions P1, P2, P3 and P7 (`round-2026-10/plans/FND.md` 2.D).
- Waste: `emg_ncs`, `ssep`, `FDG_PET`, `analyze_csf`, `order_ct_scan`, `order_echocardiogram`,
  `order_cardiac_monitoring` and `analyze_ecg` (no TLoC), each with a patient-specific rationale.
- Stop rule: the required criteria, `max_additional_actions: 0`.
- No patient text may name the diagnosis or a result the agent orders.
- Set `metadata.generation_method`: "synthetic" for S02, S03 and S04; "real_case_seed" for RS02,
  with `source`, `source_pmcid` PMC10416532 and `source_license` "CC-BY 4.0".
- Write `difficulty_rationale` for the new case.
- `icd_codes[0]`: F44.4 (S02, S03, S04) and F44.6 (RS02).

**S02**. Functional tremor, train split. 34-year-old woman, elementary school teacher.
- Patient: 2 months of bilateral hand tremor, abrupt onset after a minor car accident, with
  remissions. She is on sertraline 100 mg.
- Exam: an 8 Hz tremor of both arms, variable in frequency and amplitude. It entrains to a 3 Hz
  tap with the other hand, pauses during ballistic movements, and coactivation is felt at the
  wrist. Strength, tone, reflexes and gait are normal, and there is no bradykinesia.
- Criteria:
  - required: exam (`functional_neuro_signs`; findings entrainment, distractibility, variability;
    count 2: tremor entrainment, distractibility).
  - recommended: `interpret_labs {panels: ["TSH"]}` (new-onset tremor; stored normal TSH and free
    T4). Verify that TSH is a priced panel; if not, raise CENTRAL.
  - recommended: drug check (the sertraline tremor question; the stored output names SSRI-induced
    tremor as a possible contributor).
  - optional: neuropsychology.
  - waste: also DaTscan (no parkinsonism) and brain MRI (`analyze_brain_mri {}`; no focal sign).
- Label: "Functional neurological disorder — functional tremor of both arms".
- Differential, all low with key features: enhanced physiological or SSRI-induced tremor (entrains
  and is distractible, abrupt onset), essential tremor, hyperthyroidism (normal TSH), Parkinson's
  disease.
- Musts: M-DX, M-COMM, M-PHYSIO (functional tremor retraining), M-PSY (the accident-related
  anxiety).

**S03**. Functional gait disorder, test split. 28-year-old woman.
- Patient: 3 weeks of a slow, effortful gait with sudden knee buckling, no falls and no injury,
  after starting a new job. No sphincter or sensory symptoms.
- Exam:
  - excessive slowness with a "walking on ice" pattern;
  - knee buckling with recovery before falling;
  - gait that improves during a dual task (serial 7s);
  - Hoover negative bilaterally (strength 5/5 on testing), normal tone, reflexes, plantars,
    coordination and sensation;
  - Romberg with large sway that lessens with distraction.
- Criteria:
  - required: exam (`functional_neuro_signs`, plus findings for the gait signs; count 2:
    distractibility of gait, inconsistency between examination and function).
  - recommended: `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`, with
    stored timed walks that vary more than 30% between trials and improve with dual tasking.
  - optional: spine MRI and brain MRI.
  - waste: also DaTscan.
- Label: "Functional neurological disorder — functional gait disorder".
- Differential, all low: cervical myelopathy (normal reflexes and sensation), cerebellar ataxia
  (normal coordination, no truncal ataxia when distracted), orthostatic tremor, myopathy.
- Musts: M-DX, M-COMM, M-PHYSIO (gait retraining), M-PSY.
- Cite Daum 2014 and Nielsen 2015. The "walking on ice" and knee-buckling signs are in Daum 2014's
  gait section; the worker confirms that before citing.

**S04**. Functional fixed dystonia, train split. 22-year-old man, restaurant manager.
- Keep his PTSD after witnessing a fatal accident 8 weeks ago (nightmares and flashbacks).
- Patient: 5 weeks ago he bruised his right wrist on a door at work. Within 2 days a fixed flexed
  posture of the right wrist and fingers followed, with pain. On sertraline.
- Exam:
  - fixed flexion posture present at rest from onset;
  - variable resistance to passive extension that increases with attempted movement;
  - collapsing weakness of right finger extension;
  - no sensory trick, no task specificity;
  - normal reflexes; no skin, temperature or swelling changes (CRPS Budapest criteria not met);
  - normal elsewhere.
- Criteria:
  - required: exam (`functional_neuro_signs`; count 2: give-way weakness, inconsistency).
  - optional: brain MRI (a structural cause of hemidystonia is not suggested).
  - recommended: drug check (sertraline; no dopamine antagonist exposure, which excludes an
    acute dystonic reaction).
  - waste: also DaTscan.
- Label: "Functional neurological disorder — functional fixed dystonia of the right hand".
- Differential, all low: CRPS, possibly coexisting (Budapest criteria not met), primary focal
  dystonia (fixed at rest from onset, which focal dystonia is not), drug-induced dystonia, a
  structural lesion.
- Musts: M-DX, M-COMM, M-PHYSIO (with occupational therapy), M-PSY (trauma-focused therapy for
  PTSD).
- Prohibitions: add "Immobilize the hand in a cast or splint for the fixed posture".
- The worker verifies Schrag A et al. Brain 2004;127:2360-2372 (fixed dystonia) before citing it.

**RS02**. Functional visual loss, record-derived, train split. Seed `FND-RM11.json`
(PMC10416532, CC BY 4.0).
- Case: a 42-year-old woman, fiduciary accountant. Chronic left facial pain diagnosed as
  trigeminal neuralgia from age 31, treated with glycerol injection, microvascular decompression,
  radiosurgery and electrode implantation. Visual disturbance from 36, reaching no light
  perception in both eyes by 39. She is referred for a disability-benefit review.
- Exam: no light perception reported in either eye, yet:
  - brisk direct and consensual pupillary responses;
  - optokinetic nystagmus elicited;
  - eyes follow a moving mirror;
  - normal fundi;
  - left corneal anesthesia with punctate keratitis.
- Criteria:
  - required: exam (`functional_neuro_signs`; findings for the visual signs).
  - required: brain MRI `{contrast: false}`. Bilateral occipital (cortical) blindness spares the
    pupils, so it must be excluded. Stored: normal occipital cortex and optic pathways.
  - recommended: `order_specialized_test {test_type: vep}` (stored normal pattern VEP) and
    `{test_type: optical_coherence_tomography}` (stored normal macula and RNFL).
  - optional: `visual_field_perimetry` (stored: non-physiological or unreliable responses);
    neuropsychology.
  - drug check: optional.
- Label: "Functional neurological disorder with functional visual loss (bilateral functional
  blindness)".
- Differential:
  - cortical blindness, low (normal MRI);
  - bilateral optic neuropathy or retinal disease, low (normal fundi, OCT and VEP);
  - neurotrophic keratopathy after trigeminal procedures, present but explaining only the left
    surface findings;
  - factitious disorder or malingering, low: the benefit review is noted, but nothing shows
    intentional production, and the signs cannot decide it.
- Musts: M-DX, M-COMM, M-PSY (with chronic pain management), "Ophthalmology care of the left
  neurotrophic keratitis (lubrication, corneal protection)", and "Document the positive diagnosis
  for the disability review without labelling the symptoms feigned".
- Prohibitions: P1, P2, P3, P7, plus "Diagnose a factitious disorder or malingering without
  evidence of intentional symptom production".
- R series: the record-derived content follows the paper. No invented results beyond normal
  reports of studies the paper says were normal.
- Remove RS02 from the PMC9552981 pairing in metadata.

---

## 4. CENTRAL requests

- C1. Review app (`web-review`, stop-rule panel), with harness doc (`docs/benchmark` or the
  harness contract): say that actions matching a recommended or optional criterion never count
  against `max_additional_actions`. Fifteen FND stop-rule notes read the 0 as a ban. Same request
  as FEPI-TEMP CENTRAL 4 and FTD C3.
- C2. `diagnosis_synonyms.yaml`, F44 group, re-applied with `--prune --conditions
  functional_neurological_disorder`, then `--check`:
  - Remove S02, S03, S04 and RS02 from `F44+seizures`.
  - Remove RS02 from `F44+motor`. Keep S02, S03 and S04 in it (F44.4).
  - Add S02 and S04 to `F44+movement`.
  - New `F44+dystonia` for S04: "functional dystonia", "functional fixed dystonia".
  - New `F44+gait` for S03: "functional gait disorder".
  - New `F44+vision` for RS02: "functional visual loss", "functional blindness", "functional
    vision loss"; codes F44.6, F44.4.
  - Test every new label with `DiagnosisCriterion.matches` against the neighbouring mimics:
    "cortical blindness" must not match "functional blindness", and dystonia labels must be checked
    against PD.
  - Label changes to accepted[0] (no synonym change needed): S09, S11, RP02, and the four
    rewrites.
- C3. Tier counts after this round, for `condition_tool_guidance.yaml` FND `our_response`,
  `test_guidance_claims.py` FND claims, `criteria_packs/FND.md` sections 2, 3, 5, 6 and 8, and the
  `conditions.yaml` FND key_findings ("Video-EEG ... optional study"):
  - Required: exam 30.
  - Video-EEG: required 7 (M04, M06, P01, RP01, S05, S06, S11), recommended 11.
  - ECG: required 12, recommended 2, waste in M05, M06, M09, P07, S07, S10 and the S02, S03, S04
    and RS02 rewrites, optional in P08.
  - Brain MRI required 8 (M05, M09, P08, S05, S06, S10, RS04, RS02). Spine MRI required 1 (S07).
  - Labs required 5 (P08, RM01, RM03, RP02, RS01).
  - Drug check required 5 (M02, RM03, RP01, RP03, RS01). S03 and RS02 leave with the rewrites.
  The guidance answer must drop "no instrumental test is required in any case" and "Efficient
  traces stop after the examination". The pack drops canonical October fact 9 ("tapered over
  weeks"). The pack phenotype list adds tremor, gait, dystonia and vision.
- C4. Vocabulary (`costs.yaml`, `tool_io.py` mirror, library): LH, FSH and estradiol panels for the
  endocrine evaluation of primary amenorrhea (RP02), only if Andrea wants it scored. Until then it
  is a must. Confirm that `TSH` is a priced panel for S02.
- C5. Pack allow-list: add Nicholson 2020 (OT consensus), the Joint benzodiazepine tapering
  guideline 2025, WHO AUDIT (Babor 2001), Schrag 2004 (fixed dystonia), Pozuelo Moyano 2023
  (RS02 source), and NICE CG32 as a key.
- C6. `test_case_guards.py` banned strings for FND: "thrombolysis is not indicated" (P08 now
  clean; also in ISCH-STR-RP02, for its lead) and "slowly over weeks" (as a benzodiazepine taper).
- C7. Splits: S03 is in the test split and is rewritten. `split_manifest.json` is unchanged (same
  id and condition), but any frozen test results for FND-S03 are stale.

## 5. Open questions

None block the work. For Andrea, as information (decisions file, last section): the change of the
FND construct to "examination plus guideline-mandated safety tests", and the four replaced cases,
one of them (S03) in the test split. If Andrea wants FND to stay "examination only", the reversal
is: VEEG, ECG, ACUTE and LABS tiers back to recommended, and the stop rules back to the
examination plus the drug check. That would go against the physician rulings.

<!-- PLAN COMPLETE -->
