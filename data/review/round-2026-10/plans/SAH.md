# SAH: condition plan for the October 2026 review round

Lead plan for the 30 SAH cases (M01..M08, P01..P08, RM11, RP11, RS11, RS12, S01..S10). Read
`ROUND_POLICY.md` and `PATTERNS.md` first; this plan does not repeat them.

All 44 notes are from Reviewer 2 (Reviewer 1 never reviewed SAH) and cover 23 cases. Notes-file
status: approved M05, M06, P01, P02, P05, RM11, RP11, S01, S04, S06, S07, S08, S09, S10; needs
changes M01, M02, M03, M04, M07, M08, P03, P08, RS12. P04, P06, P07, RS11, S02, S03, S05 have no
notes and no status in the notes file; PATTERNS says R2 approved 21 SAH cases, which matches the
14 above plus these 7, so treat them as probably approved. In approved cases fix only real errors
(the classes below are real errors), and log why.

Baseline (24 October 2026, before any edit): `perfect_agent.py` passes 30/30. With `-v` the NCCT
and labs criteria show `<- ?`: that is a display artefact of the script's `exclude_none`
comparison, not a missing output; confirm by content that the initial CT and labs answer them.

Use: apply every class of section 2 that names your case (canonical text verbatim, `<...>` slots
filled from the case), then the decisions of section 4, rebuild criteria, follow-ups, constraints
and stop rule per section 3, run both checks, write `logs/{CASE_ID}.md` citing every note id with
its ruling. Section 2 cites notes by 8-character prefix; section 4 gives full ids.

New text: English, US spelling as the cases use, no em or en dashes. New numbers must be plausible
for the patient and differ from case to case (no template values).

---

## 1. Governing guidelines and canonical facts

### 1.1 Sources

| question | source | key |
| --- | --- | --- |
| Diagnosis, securing, nimodipine, BP, hydrocephalus, DCI, sodium | Hoh BL et al. 2023 AHA/ASA guideline for aSAH, Stroke 2023;54:e314-e370 | `[Hoh_2023]` (governs) |
| Numeric pre-securing SBP target (historical), hypotonic fluids | Connolly ES et al., Stroke 2012;43:1711-1737 | `[Connolly_2012]` |
| CT sensitivity within 6 h | Perry JJ et al., BMJ 2011;343:d4277 (the CT-within-6-hours cohort; the pack mislabels the title, CENTRAL) | `[Perry_2011]` |
| Ottawa SAH Rule | Perry JJ et al., JAMA 2013;310:1248-1255 | `[Perry_2013]` (CENTRAL: allow-list) |
| Clinical grade | Hunt WE, Hess RM, J Neurosurg 1968;28:14-20 | `[Hunt_Hess_1968]` |
| CT blood and vasospasm | Fisher CM et al., Neurosurgery 1980;6:1-9 | `[Fisher_1980]` |
| Coiling versus clipping | ISAT, Molyneux A et al., Lancet 2002;360:1267-1274 | `[Molyneux_2002]` (CENTRAL) |
| QTc and torsades prevention | Drew BJ et al., Circulation 2010;121:1047-1060 | `[Drew_2010]` (CENTRAL) |
| Emergency headache evaluation | Edlow JA et al., Ann Emerg Med 2008;52:407-436 | `[Edlow_2008]` |

Rules:

- `[Hoh_2023]` governs every management statement. Where it and `[Connolly_2012]` differ (BP
  target), Hoh governs and Connolly is cited only for the historical numeric target.
- R2 also cites an ESO/EANS/ESMINT 2026 guideline ("within 24 h after ictus") and AANN 2025. Do not
  cite them in case text until Andrea confirms the references (section 6); the 24-hour window is
  already carried by `[Hoh_2023]`.
- One bracketed key per source in every `citations` list, no duplicates. Remove the free-text
  strings `"AHA/ASA aneurysmal subarachnoid hemorrhage guideline 2023"`, `"Connolly_2012"` and
  `"Hoh_2023"` (unbracketed) everywhere; they always sit next to the bracketed key.
- Do not attribute a claim to "AHA/ASA" or to a COR/LOE unless it is one of the facts in 1.2.

### 1.2 Canonical facts (use these; do not restate them differently)

- **Securing**: surgical or endovascular treatment of the ruptured aneurysm as early as feasible,
  preferably within 24 hours of onset (Hoh 2023, COR 1, LOE B-NR). No document gives 24-72 h or
  24-48 h. Technique is a joint neurosurgical and neurointerventional decision; in aneurysms
  suitable for both, coiling gave better one-year independent survival in ISAT.
- **Nimodipine**: early enteral nimodipine 60 mg every 4 hours for 21 days (Hoh 2023, COR 1, LOE
  A). If it causes hypotension, give 30 mg every 2 hours rather than stopping it. The FDA boxed
  warning is against injecting the capsule contents intravenously or parenterally; an IV infusion
  formulation exists in Europe, so "never give nimodipine intravenously" is wrong as written.
- **Blood pressure before securing**: control with short-acting titratable agents (Hoh 2023, COR 1,
  LOE C-EO per R2), no numeric target in 2023; SBP below 160 mmHg was reasonable in Connolly 2012
  (Class IIa, LOE C) and remains the common practice target. Avoid hypotension. Agents:
  nicardipine or clevidipine infusion, or labetalol IV boluses. Labetalol is not first choice with
  LVEF 40% or less, bradycardia, asthma, or acute cocaine toxicity. Hydralazine is not used.
- **Home antihypertensives** (decided for this condition):
  dihydropyridine CCB (amlodipine, nifedipine): withhold while on nimodipine (same class, additive
  hypotension; R2 P02 note); verapamil: withhold (additive hypotension, bradycardia, negative
  inotropy); ACE inhibitor, ARB, thiazide: may be withheld in the acute phase (additive
  hypotension, natriuresis); beta-blocker: continue unless bradycardia or hypotension, never stop
  abruptly, and always continue when it is AF rate control or post-MI therapy. Whenever a home
  agent is withheld and BP is above target, a must names the IV agent that replaces it.
- **Hydrocephalus**: urgent CSF diversion (EVD) for acute symptomatic hydrocephalus (Hoh 2023, COR
  1, LOE B-NR). Decision for this condition: radiological hydrocephalus with intraventricular blood,
  or with depressed consciousness, gets an EVD must; hydrocephalus alone with GCS 15 gets the
  conditional must (C6).
- **Diagnosis**: NCCT first. CT within 6 hours of onset on a modern scanner read by an experienced
  radiologist is close to 100% sensitive (Perry 2011); sensitivity falls after 6 hours (about 86%
  beyond 6 hours in that cohort) and markedly by days 5 to 7; anaemia lowers it at any time. After
  a negative CT, LP is indicated in patients presenting more than 6 hours from onset or with a new
  neurological deficit (Hoh 2023, COR 1, LOE B-NR, per R2); within 6 hours a negative CT has its
  highest negative predictive value. Spectrophotometric bilirubin needs about 12 hours to form and
  persists about two weeks or longer; oxyhaemoglobin alone appears earlier and also follows a
  traumatic tap. CTA after the NCCT; catheter DSA when CTA is negative or for treatment planning.
- **Ottawa SAH Rule** (Perry 2013): for alert patients aged 15 or more with a new severe
  non-traumatic headache peaking within one hour. Investigate if any of six: age 40 or more; neck
  pain or stiffness; witnessed loss of consciousness; onset during exertion; thunderclap onset
  (instantly peaking pain); limited neck flexion on examination. Not applicable with a new
  neurological deficit, previous aneurysm or SAH, known brain tumour, or recurrent similar
  headaches (3 or more episodes over 6 months or more).
- **DCI**: mainly days 3 to 14; frequent neurological examination is the core of surveillance; TCD
  is reasonable (COR 2a, so optional here). Maintain euvolaemia; prophylactic hypervolaemia
  (triple-H) is not recommended. Induced hypertension is for symptomatic DCI after securing.
- **QTc**: QTc 500 ms or more, or hypokalaemia, needs potassium at least 4.0 mmol/L, magnesium at
  least 2.0 mg/dL, no added QT-prolonging drugs and continuous ECG monitoring (practice targets;
  Drew 2010 for correcting K and Mg and avoiding QT drugs).
- **Apixaban reversal** (US andexanet label): low dose (400 mg IV bolus at 30 mg/min, then 4 mg/min
  for up to 120 minutes) when the last apixaban dose was 5 mg or less, or 8 hours or more before;
  high dose (800 mg bolus, then 8 mg/min) only when the last dose was more than 5 mg (or unknown)
  and less than 8 hours before (or at an unknown time). Alternative: four-factor PCC 50 IU/kg.
  Andexanet causes heparin resistance, which matters for an endovascular procedure. Idarucizumab
  is for dabigatran and vitamin K for warfarin; neither applies to apixaban.
- **Fisher grade** (1980): 1 no blood; 2 diffuse thin (<1 mm); 3 localized clot or thick layer
  (1 mm or more); 4 intracerebral or intraventricular clot. Grade 4 needs IVH or ICH on the CT.
- **Hunt-Hess**: 1 asymptomatic or mild headache, slight nuchal rigidity; 2 moderate to severe
  headache, nuchal rigidity, no deficit other than cranial nerve palsy; 3 drowsiness, confusion or
  mild focal deficit; 4 stupor, moderate to severe hemiparesis; 5 coma. "Alert and oriented x4"
  with GCS 15 cannot be grade 3. The grade is judged at examination, not from a brief LOC that has
  resolved.
- **Aneurysm size words**: "small" below 10 mm; do not call a 6 to 9 mm aneurysm "large".

### 1.3 Canonical text

Musts (`ground_truth.assessment.required_recommendations`). Keep the NCCT must and the sodium must
as they are. Replace the rest of the template as follows (the template has 8 or 9 entries; two are
duplicate 24-72 h securing musts).

- **MUST-CTA** (keep the existing CTA must in CT-positive cases; in P01, P03, P06 replace it with):
  "Obtain CT angiography of the head and neck once the lumbar puncture confirms subarachnoid
  blood, to identify the aneurysm."
- **MUST-NIMO** (replaces the nimodipine must): "Start enteral nimodipine 60 mg every 4 hours
  (orally or by nasogastric tube) as soon as aneurysmal SAH is confirmed and continue for 21 days;
  if it causes hypotension, give 30 mg every 2 hours rather than stopping it [Hoh_2023]."
- **MUST-SECURE** (replaces both 24-72 h musts, one entry): "Arrange urgent joint neurosurgical and
  neurointerventional review and secure the ruptured <location> aneurysm by endovascular coiling
  or microsurgical clipping as early as feasible, preferably within 24 hours of onset [Hoh_2023];
  the technique is chosen jointly from the aneurysm anatomy and the patient's condition."
  (Add "<, after anticoagulant reversal>" in M07, S04; "<, the ruptured aneurysm first>" where
  CTA shows more than one, M05 and S05.)
- **MUST-ICU** (replaces the "Admit to a neurocritical care unit ... (SBP target ...)" must):
  "Admit to a neurocritical care unit at a centre with neurosurgical and neurointerventional
  capability, with hourly neurological checks and continuous cardiac monitoring."
- **MUST-BP-A** (presenting SBP 160 or more): "Lower blood pressure now with a short-acting
  titratable intravenous agent (<agent>) until the aneurysm is secured, avoiding hypotension;
  the 2023 guideline sets no numeric target [Hoh_2023] and systolic pressure below 160 mmHg is the
  commonly used target [Connolly_2012]." `<agent>`: "nicardipine or clevidipine infusion, or
  labetalol boluses" by default; "nicardipine or clevidipine infusion" when LVEF is 40% or less
  (echo), with bradycardia, or with cocaine (S08 adds its own wording, section 4).
- **MUST-BP-B** (presenting SBP below 160): "Keep continuous blood pressure monitoring until the
  aneurysm is secured and treat any sustained rise with a short-acting titratable intravenous
  agent, avoiding hypotension [Hoh_2023]."
- **MUST-HOME** (only where the patient takes antihypertensives or other relevant drugs): one
  must per case, from the 1.2 rules, naming each drug: "<Withhold amlodipine while on nimodipine
  (additive dihydropyridine effect)>; <continue metoprolol (rate control) unless bradycardia or
  hypotension>; <withhold lisinopril during the acute phase and resume once stable>."
- **MUST-DCI** (replaces "Initiate daily transcranial Doppler monitoring days 4-14 ..."):
  "Monitor for delayed cerebral ischemia from day 3 to day 14 with frequent neurological
  examinations, with transcranial Doppler surveillance as a reasonable adjunct; maintain
  euvolemia and do not use prophylactic hypervolemia [Hoh_2023]."
- **MUST-EVD-NOW** (C6): "Urgent neurosurgical CSF diversion by external ventricular drain for
  the acute hydrocephalus <with intraventricular blood / with depressed consciousness>
  [Hoh_2023]<; reverse the anticoagulant first> ."
- **MUST-EVD-WATCH** (C6): "Urgent neurosurgical review of the hydrocephalus: hourly neurological
  checks and repeat CT on any decline in consciousness, with external ventricular drainage if it
  becomes symptomatic [Hoh_2023]."
- **MUST-QT** (C9): "QTc <N> ms<with potassium X mmol/L>: replete potassium to at least 4.0 mmol/L
  and magnesium to at least 2.0 mg/dL, avoid adding QT-prolonging drugs (for example ondansetron
  or haloperidol<, and review home drug>), and keep continuous ECG monitoring with daily QTc
  [Drew_2010]."
- **MUST-REVERSE** (M07, S04, replaces the generic "PCC, andexanet alfa, idarucizumab, or vitamin
  K" must): "Reverse apixaban now (last 5 mg dose <h> hours before arrival, anti-Xa <x> ng/mL):
  andexanet alfa low-dose regimen (400 mg IV bolus, then 4 mg/min for up to 120 minutes) or
  four-factor PCC 50 IU/kg; andexanet causes heparin resistance, which matters if coiling is
  planned. Stop apixaban; the timing of any restart is decided with neurosurgery and cardiology
  after the aneurysm is secured."
- **MUST-LVEF** (echo LVEF 40% or less: M05, M07, P04, P08, RS12): "LVEF <N>% from stress
  cardiomyopathy<, with moderate mitral regurgitation>: involve cardiology and neuroanesthesia
  before the securing procedure (hemodynamic plan, invasive arterial monitoring) and repeat
  echocardiography to document recovery."
- **MUST-ALCOHOL** (S06, RS12, P04): "Daily alcohol use: give thiamine before glucose and monitor
  for alcohol withdrawal with a validated scale, using the lowest effective benzodiazepine dose so
  that the neurological examination is not masked."

Prohibitions (`prohibited_recommendations`). Keep: LP before NCCT; LP when CT confirms SAH with
mass effect, IVH or hydrocephalus; antiplatelets before securing; NSAIDs before securing;
catheterization for neurogenic troponin. Replace:

- IV nimodipine: "Do not inject the contents of nimodipine capsules intravenously or by any other
  parenteral route (risk of cardiovascular collapse); give nimodipine enterally."
- BP: "Do not leave severe hypertension untreated before the aneurysm is secured, and do not lower
  blood pressure to the point of hypotension."

Key clinical evidence (`key_clinical_evidence`), replace these three template pearls:

- 24-72 h pearl -> "Securing the ruptured aneurysm by coiling or clipping as early as feasible,
  preferably within 24 hours of onset, reduces rebleeding, which carries high mortality."
- vasospasm/TCD pearl -> "Delayed cerebral ischemia occurs mainly between days 3 and 14; frequent
  neurological examination is the core of surveillance and transcranial Doppler is a reasonable
  adjunct."
- CT sensitivity pearl -> "Non-contrast CT is close to 100% sensitive within 6 hours of onset on a
  modern scanner read by an experienced radiologist; sensitivity falls after 6 hours and markedly
  by days 5 to 7, and anemia lowers it, so a negative CT does not exclude SAH in late presenters."
- LP pearl -> "After a negative CT, lumbar puncture is indicated when the patient presents more
  than 6 hours after onset or has a new neurological deficit; spectrophotometric bilirubin needs
  about 12 hours to form and persists for about two weeks or longer."

Keep the other seven template pearls (they are correct).

Criteria text (replace label-copied `rationale` fields; keep labels unless stated):

| criterion | rationale | expected_evidence |
| --- | --- | --- |
| NCCT | "Non-contrast head CT is the first study in suspected SAH: it shows subarachnoid blood and its distribution, intraventricular blood and hydrocephalus." | case-specific: "<Fisher grade N SAH in ...; hydrocephalus yes/no>" or "<no subarachnoid hyperdensity>" |
| CTA | "CTA localizes the ruptured aneurysm and defines the anatomy that decides coiling or clipping; it is a separate acquisition after the NCCT." | "<size, location, neck>" |
| labs | "Blood count, electrolytes (sodium, potassium, magnesium), renal function and coagulation are needed before securing or CSF diversion and for sodium and QTc management." | case-specific abnormal values, or "no anemia, thrombocytopenia, electrolyte or coagulation abnormality" |
| ECG | "Neurogenic ECG changes are common in SAH; the ECG screens for a primary cardiac event and sets the QTc baseline." | "<T-wave inversions in ..., QTc N ms>" |
| DSA | "Catheter angiography with 3D rotational imaging confirms the ruptured aneurysm and its relation to branch vessels before securing, and is the reference test when CTA is negative." | "<aneurysm confirmed, neck, dome-to-neck ratio, branch relation>" |
| drug check | case-specific (C10) | the real interaction (C10), never the template sentence |
| echo | "Troponin elevation with neurogenic ECG changes warrants echocardiography for stress cardiomyopathy, which also informs the anesthetic plan." | "<LVEF, wall-motion pattern>" |
| telemetry | "Arrhythmias and QTc prolongation are frequent in the first days after SAH." | "<rhythm and burden since arrival>" (C12) |
| TCD | "Baseline velocities on admission give a reference for surveillance during the vasospasm window; reasonable, not mandatory." | "Baseline velocities on admission" |
| literature | "General evidence on grading and on the choice and timing of aneurysm treatment; not a clinical step." | "General evidence on grading scales and on coiling versus clipping" |

Every criterion's `citations` is `["[Hoh_2023]"]` except: ECG and telemetry `["[Hoh_2023]"]` too
(not Connolly), CSF `["[Hoh_2023]", "[Edlow_2008]"]`, literature `["[Hunt_Hess_1968]",
"[Fisher_1980]", "[Hoh_2023]"]`.

Canonical literature output (the only literature follow-up left in a case, last in the list,
`trigger_action` "request_sah_grading_and_treatment_literature", query
"aneurysmal SAH management Hunt-Hess WFNS Fisher coiling clipping"):

```json
{"query": "aneurysmal SAH management Hunt-Hess WFNS Fisher coiling clipping",
 "results": [
  {"finding": "The Hunt and Hess scale grades the clinical severity of aneurysmal SAH from I to V and correlates with surgical risk and outcome.", "source": "[Hunt_Hess_1968]", "evidence_level": "cohort"},
  {"finding": "The amount and distribution of subarachnoid blood on the admission CT predicts later vasospasm.", "source": "[Fisher_1980]", "evidence_level": "cohort"},
  {"finding": "Surgical or endovascular treatment of the ruptured aneurysm should be performed as early as feasible, preferably within 24 hours of onset; early enteral nimodipine improves outcome.", "source": "[Hoh_2023]", "evidence_level": "guideline recommendation"},
  {"finding": "In ruptured aneurysms suitable for both techniques, endovascular coiling gave a higher rate of independent survival at one year than neurosurgical clipping.", "source": "[Molyneux_2002]", "evidence_level": "randomized controlled trial"}],
 "summary": "Clinical grade (Hunt and Hess, WFNS) and CT blood burden (Fisher) stratify outcome and vasospasm risk. Guidelines recommend securing the ruptured aneurysm as early as feasible, preferably within 24 hours, and early enteral nimodipine. Where an aneurysm suits both techniques, coiling was associated with better one-year independent survival than clipping."}
```

Use only keys present in the existing `LiteratureSearchResult` objects of the case (if a key is
refused by the schema, drop it; `save()` will tell you).

---

## 2. Error classes in this condition

### C1. Securing window 24-72 h, and no securing pathway (PATTERNS 1, 2; all 30)

Template must 4, the duplicate securing must and the securing pearl say "within 24-72 hours" (91
occurrences); literature outputs say "24-48 hours" (S01, S02). No case orders DSA except M01,
M03, P02, and none states securing in its own words. Notes: 38447471 (M01), 53d4e407 (M04),
4daa3aa1 (M07), 6dcebd64 (P03), f8f0befa (P05), a60d0697 (RM11), 9b8af8ad (RP11), f87e2dd7 (RS12,
securing part), fddcb39d (S01), cabb6393 (S04), c3c56bb2 (S06), 09f3f88b (S07), 25ff44d7 (S08),
899fabe8 (S09), 66c7702e (S10). M07 4daa3aa1 and P03 6dcebd64 themselves say 24-72 h: apply the
substance (secure urgently) with the governing window, FIXED, and say so in the log.
Fix, every case: MUST-SECURE replaces both securing musts; securing pearl replaced (1.3); a DSA
criterion and output (C3); "24-48 h" text goes with the literature (C8). P02 (no aneurysm): no
MUST-SECURE; see section 4.

### C2. Pathway order and impossible timeline (PATTERNS 1, 3; 30)

Follow-ups put drug checks, literature or echo before the CTA (M07, P08, S04, S06, S07, S09, S10
drug check or echo at step 1), and every TCD and two lab follow-ups are dated days 2 to 8 after
an ictus that, in most cases, was hours before arrival (M02 step 2 "Day 4 TCD" with confusion;
M05 "Day 7"; RS12 "day 8" with new confusion and leg weakness; P06 "Hgb now 9.2 after
transfusion"). With no securing step, the timeline runs to day 5 to 8 with an unsecured aneurysm,
which R2 names in every securing note. Notes: bf848453 (M02), 61a944ea (P08), and the timeline
part of all C1 notes.
Fix: reorder follow-ups and criteria per section 3. Every result must exist at the time the agent
orders it, that is within the first hours of this encounter:
- TCD: re-date to an admission baseline. `quantitative_data` gets only
  `{"post_ictus_day": "<d>"}` where d is the day of presentation from the HPI (0 for hours, P03 1,
  M08 3 from the sentinel, P01 5). Velocities: d 0 to 2 normal (MCA MFV below 120 cm/s, Lindegaard
  below 3, ACA and basilar normal); P01 (d 5) and M08 (d 3) may keep mild borderline elevation.
  Delete every clinical note in a TCD (confusion, weakness, transfusion). Impression: "Baseline
  transcranial Doppler, post-ictus day <d>: <velocities>. No sonographic evidence of vasospasm."
  `tracer_or_protocol`: "Transtemporal insonation of the MCA, ACA and PCA; transforaminal
  insonation of the basilar artery; submandibular extracranial ICA for the Lindegaard ratio".
  `recommended_actions`: ["Serial transcranial Doppler recommended during days 3 to 14"].
- Remove the future-dated lab follow-ups (M05 `request_hyponatremia_management`, RS12
  `request_hyponatremia_monitoring`); the sodium must stays.
- Remove management results from reports (CTA "after anticoagulation reversal", M07; P06 TCD
  transfusion note; DSA "coiling performed" M01, M03, C3).

### C3. Catheter DSA: absent, mislabelled, or reporting treatment (PATTERNS 1, 2; 30)

DSA is recommended only in M01, M03, P02, with the label "because this case has CTA-occult or
uncertain anatomy" although M01 and M03 have clear CTA aneurysms, and the M01 and M03 DSA outputs
report coiling and Raymond class I occlusion (treatment results inside a diagnostic tool, ruling 4).
Every CTA already recommends "Conventional DSA ... for treatment planning / definitive
characterization". Notes: the "no DSA" part of a60d0697, 9b8af8ad, fddcb39d, cabb6393, c3c56bb2,
09f3f88b, 25ff44d7, 899fabe8, 66c7702e.
Fix: every aneurysmal case (all but P02, which already has one) gets a recommended criterion
`order_advanced_imaging {modality: cerebral_angiography}`, id `dsa-aneurysm-anatomy` (M01, M03,
P02 keep `action-4-order-advanced-imaging`), label "Obtain catheter cerebral angiography with 3D
rotational imaging to confirm the ruptured aneurysm and define its anatomy before securing"
(P02: "... to exclude an aneurysm not shown by CTA"), rationale and evidence per 1.3. Its output
(new follow-up, trigger `request_digital_subtraction_angiography`, modality
`cerebral_angiography`): a diagnostic report only, anatomy matching the CTA (size within 0.3 mm,
same lobulation, neck, daughter sac), plus dome-to-neck ratio, branch incorporation, "No additional
aneurysm or vascular malformation" (or the CTA's second aneurysm), "No angiographic vasospasm".
No coiling, no clipping, no Raymond class, no treatment advice. M01 and M03 outputs: rewrite to
this form. Constraint CTA before DSA (soft).

### C4. Nimodipine must and the IV prohibition (PATTERNS 2; 30)

The nimodipine must is present in all 30, so the notes that ask for nimodipine are ALREADY-FIXED
for the must itself: 75c2bb0f (M07), 5d5b5879 (M08), the nimodipine part of 60a5d171 (S04) and
db7c626e (S07). The prohibition "Do not administer nimodipine intravenously" is factually wrong
(IV formulation licensed in Europe; the hazard is parenteral injection of capsule contents).
Fix: MUST-NIMO and the IV prohibition text (1.3) in all 30; in M02 the drug check moves before the
TCD (C2), which resolves "nimodipine first proposed at step 4" (bf848453).

### C5. Blood pressure before securing: no action, held drugs, invented targets (PATTERNS 1, 2; 30)

The only BP text is "SBP target generally <160" inside the ICU must and a prohibition; drug checks
withhold home antihypertensives (RM11 propranolol and valsartan, S04 metoprolol twice and ramipril,
S06 verapamil, S07 nifedipine, RS12 lisinopril and HCTZ, S01, S02, S03, S09, RS11, M02, M05, P06)
and nothing replaces them; RS12 states "Target SBP 140-160 before aneurysm secured; 120-140 after"
(not in the guideline); S06 proposes hydralazine; S08 gives opposite labetalol instructions in two
steps; P06 "Target MAP >90 mmHg" and P07 "Target MAP >90 given estimated ICP 35-42 cmH2O" are
invented (no ICP was measured). Notes: b12f861e (M07), f6edc7fb (P05), 2b67f747 (P08, BP part),
2ab931d5 (RM11), 03f424a3 (RS12), 60a5d171 (S04), 633fd9a3 (S06), db7c626e (S07), 6e139dfe and
4f899419 (S08), fb64b259 (P02, hold amlodipine).
Fix: MUST-BP-A or MUST-BP-B in every case, MUST-HOME where the patient takes relevant drugs, the
BP prohibition text (1.3), and the drug-check rewrites of C10. Remove the RS12 target sentence, the
hydralazine alternative, both invented MAP targets. Presenting SBP 160 or more (BP-A): M01, M02,
M03, M04, M05, M06, M07, M08, P04, P05, P06, P08, RS11, RS12, S01 to S10. Below 160 (BP-B): P01,
P02, P03, P07, RM11, RP11.

### C6. Hydrocephalus and EVD: template musts that do not fit the CT (PATTERNS 1, 4)

The EVD must ("Consult neurosurgery for emergent external ventricular drain placement given acute
hydrocephalus") is in M02, M05, M06, M07, M08, P04, RS12; M06 and M08 CTs say "No acute
hydrocephalus" (carry-over). Notes: da99e9e0 (M07: the must exists, ALREADY-FIXED for the must;
FIXED for wording and order after reversal), f87e2dd7 (RS12, drain part: ALREADY-FIXED, wording
updated).
Fix: MUST-EVD-NOW in M02 (third-ventricle blood), M07 (IVH, GCS 14; after reversal), P04 (IVH,
GCS 14), RS12 (third-ventricle blood), M05 (hydrocephalus without IVH, confused with GCS 14 after
the C13 exam fix: "with depressed consciousness"). MUST-EVD-WATCH only if Andrea answers section 6
question 1 against EVD in M02 and RS12. Remove the EVD must from M06 and M08. LP avoided action severity `contraindicated` where the CT shows
hydrocephalus, IVH or mass effect (M02, M05, M07, P04, RS12, S04 after its IVH fix); `harm` in the
other CT-positive cases (note 9d172604, M07: FIXED).

### C7. Literature as steps, with wrong or patient-specific content (ruling 5; 30)

The literature criterion is `recommended` in all 30 with the same query; three cases (M01, P04,
RS12) answer it from an `initial_tool_outputs.literature_search` block whose finding repeats the
criterion's `expected_evidence` (scoring-key leak); the others answer it with case-specific
follow-ups that contain errors: Ottawa rule misstated (M03 four criteria and ">40"; P03 "does not
exclude patients with prior headache history", wrong), LP indication reversed (M03 "LP required if
CT negative and presentation <6 hours"; P01 "LP mandatory ... regardless of time"), triple-H (M02,
S01), 24-48 h (S01, S02), "AHA/ASA 2023: anticoagulation delayed minimum 4 weeks" (M07,
unverifiable), "rebleed risk 20-50% in first 24 hours" (M08), SIADH "low urine osmolality" (S10),
"Hgb target 8-10" (P06), patient values inside literature (S05 "Right ICA 2.8 mm", S06 "Current
QTc 516 ms", S07 "Creatinine 1.4", S09 "eGFR 42"), empty summaries (M05, P01, P05, P06, S05, S07,
S09). Notes: 6b4234fb, 6a4a8415 (M03).
Fix, all 30: one literature criterion, `optional`, last, label kept, rationale and evidence per
1.3; delete `initial_tool_outputs.literature_search`; delete every literature follow-up and add the
canonical output (1.3) as the last follow-up. Content that matters clinically moves to musts or
pearls as section 4 says (OCP, anticoagulation restart, alcohol, lithium, incidental aneurysm,
family screening). M03 notes: FIXED by deletion of the misstated text; the Ottawa exclusion
(migraine history, confusion) becomes a red herring (section 4).

### C8. Drug-interaction blocks: template leak, tier, treatment disguised as a check (rulings 4, 6; 30)

Five cases (M07, M08, P04, P07, S05) carry `initial_tool_outputs.drug_interactions.general`, an
empty block whose summary is the criterion's `expected_evidence` (P07 repeats the warning three
times). The criterion is `recommended` everywhere with `drug: nimodipine` and expected evidence
"Nimodipine well-tolerated ... anticoagulation reversed if ...". P04 `request_ffp_coagulopathy`
(4 units FFP for INR 1.4) and P06 `request_transfusion_consideration` (2 units PRBC) are
treatments filed as drug checks.
Fix: delete the five `general` blocks; delete the P04 FFP and P06 transfusion follow-ups (their
content becomes a must, section 4); tier per C10; `expected_evidence` names the case's real
interaction.

### C9. QTc and electrolytes (PATTERNS 1, 2; notes e38a8460 M05, c621cf95 M06, 7f1b4f47 S06)

No case measures magnesium; potassium is missing in P01 to P08, RM11, RP11, S04, S05, S06. QTc is
500 ms or more in M02 512, M05 524 (K 3.4, U waves, furosemide), M07 508, P04 518, P08 532, RS12
512, S06 516; no case has a K/Mg action. M06 note c621cf95 repeats the M05 numbers, but M06 has
QTc 478 ms, K 3.7, no furosemide and no U waves: DECLINED for those facts with this evidence; the
class part (magnesium never measured) is FIXED by the lab addition below.
Fix: add potassium (where missing) and magnesium (all 30) to the stored BMP panel: potassium 3.5 to
4.8 mmol/L unless the case says otherwise, magnesium 1.9 to 2.3 mg/dL, lower (1.5 to 1.8, flagged)
with a loop diuretic (M05, S09) or heavy alcohol use (S06, RS12, P04); keep `abnormal_values_summary`
and `interpretation` in step. MUST-QT in the seven QTc 500+ cases. Do not change the labs
criterion's `required_arguments`.

### C10. Drug-check content and tier (rulings 4, 6)

Errors to remove wherever found: "Hold antihypertensives during triple-H therapy" (M01); andexanet
"high-dose protocol indicated" for a 5 mg dose (M07) and "<10 mg ... >10 mg" thresholds and "4F-PCC
less effective" (S04); "hold metoprolol" in AF or as blanket advice (S04 twice, P06; RM11
propranolol, see 1.2); RS12 SBP targets; S06 hydralazine; S08 "labetalol preferred" (contradicts
its own literature; replace with the S08 wording of section 4); P06 MAP target; P07 MAP/ICP target;
RP11 "JC virus PCR in CSF was negative - PML excluded" (no LP was done); "Never give IV" and "Must
not crush and inject IV" become "Do not inject capsule contents parenterally".
Tier (criterion `importance`): `required` where the interaction changes management: M02, M07, P02,
RS11, S03, S07 (dihydropyridine with nimodipine); M05 (furosemide with QTc 524 and K 3.4); M07 and
S04 (apixaban reversal, a separate criterion `check-apixaban-reversal`, `drug: apixaban`, matched
by the `request_apixaban_reversal` follow-up); P05 (magnesium sulfate with nimodipine); P08
(aspirin, clopidogrel and an extra 325 mg aspirin from EMS); S06 (verapamil, sertraline with QTc
516); S10 (lithium with HCTZ and SAH hyponatremia). `recommended`: M01, M03, M04, M06, M08, P01,
P03, P04, P06, P07, RM11, RP11, RS12, S01, S02, S09. `optional`: S05, S08 (no regular
medicines). Put each required or recommended check after the CTA (M07, S04: before the DSA).

### C11. Differential not updated, carry-over red herrings (ruling 7; PATTERNS 2, 4)

The five-entry differential is the same in 25 cases with generic key features ("pituitary MRI / CT
without sellar enlargement excludes", "CT venogram ... indicated if SAH excluded"). RCVS stays
`moderate` in M08, P01, P03 after CTA shows the aneurysm; P07 "IIH flare" `moderate` after CT shows
blood. The red herring "Past history of migraines, chronic headaches, or fibromyalgia" is in M01,
M02, M08 whose patients have none (carry-over; note 9bd81d95 M02). P01 red herring "Bloody CSF in
tube 1" contradicts a tube 1 RBC of 12/uL. Coital onset (M04, S02) is a classic RCVS trigger with
no entry (note 03a9ce4b M04).
Fix: key features cite the case's own results:
- RCVS: "Thunderclap onset<, and the <exertional/coital> trigger,> overlap with SAH; RCVS gives
  convexity SAH and segmental vasoconstriction, whereas this case shows <basal-cistern blood /
  xanthochromia> and a saccular <location> aneurysm on CTA." `low`.
- Cervical artery dissection: "Headache and neck pain overlap; CTA of the neck shows no
  dissection." `low`.
- Pituitary apoplexy: "Sudden headache overlaps; no sellar mass or hemorrhage on CT and no visual
  field or ocular motor deficit." `low`.
- CVST: "Headache overlaps; no hyperdense sinus or venous infarct on CT, and the aneurysmal SAH
  explains the presentation." `low`.
- Thunderclap migraine: keep `very_low`; "excluded by subarachnoid blood on CT" (CT-negative cases:
  "by xanthochromia on CSF").
M04 and S02: RCVS stays `low` (the work-up excludes it, ruling 7) and gains the coital-trigger
wording above, plus a red herring: data_point "Headache onset during sexual intercourse", field
path `patient.history_present_illness`, intended effect "Coital onset is a classic trigger of
RCVS and could divert to a vasoconstriction work-up", correct interpretation "Coital onset is also
a classic trigger of aneurysmal rupture; basal-cistern blood with a saccular aneurysm on CTA, and
no segmental vasoconstriction, establish aneurysmal SAH." (03a9ce4b: FIXED, option "score the
reasoning", likelihood kept low per ruling 7.) Remove the migraine red herring from M01, M02, M08.

### C12. Telemetry output identical in all 30 (PATTERNS 3, 4; style guide)

"Sinus rhythm with intermittent neurogenic changes; rare malignant arrhythmias warrant
intervention" is impression, finding, event and rhythm summary in all 30 and the telemetry
`expected_evidence`; it contains management, is vague, and is wrong in M07 (AF). 24-hour duration
cannot exist at assessment time.
Fix: case-specific report covering arrival to assessment: `duration_hours` 2 to 6, rhythm as the
ECG (sinus or AF), plausible `heart_rate_range`, quantified ectopy, "No sustained arrhythmia. No
pauses." and, where QTc is 480 ms or more, "QTc <N> ms on monitoring leads; no torsades de
pointes." No management words.

### C13. Exam, grade and CT inconsistencies (PATTERNS 2, 3)

- "Alert and oriented x4" next to GCS 14 or confusion: M03, M07, P04 (and M05 HH3 label with an
  exam of GCS 15, "mild confusion resolved"). Fix the mental status to match the label's grade:
  confused, GCS 14 (E4V4M6), not oriented to date, in M03, M05, M07; somnolent, GCS 14 in P04.
- S04 label "Fisher 4" with "No IVH, no ICH": add small IVH layering in the occipital horns to the
  CT findings and impression (no hydrocephalus); M05 `additional_observations` "Fisher grade 3-4"
  becomes "Fisher grade 3".
- P08 exam "Hunt-Hess Grade 2-3" with GCS 15 and no deficit: "Hunt-Hess Grade 2".
- S06 "GCS 14 (confused initially, now 15)": "GCS 15 (confused at the scene, now oriented)".
- "Large saccular aneurysm" for 6 to 9 mm (M05, P04, P08, RS12, S04, S08): drop "Large".

### C14. Reports doing the agent's work, impossible content (style guide; PATTERNS 3, 5)

CT `additional_observations` with clinical or cross-modality text: M04 "near-isodense in higher
Hgb patient - but Hgb normal here"; M05 "Multiple PKD-related renal cysts visible on lower cuts"
and S07 "Partially visualized right kidney with multiple cysts" (a head CT does not image the
kidneys: impossible, delete); M07 "Anticoagulation may have contributed"; P07 "This patient has
known elevated ICP - LP will require careful interpretation"; RP11 "MS white matter lesions ...
not relevant"; RS12 "Classic presentation"; S04 "Possibly mildly hypodense blood due to
anticoagulation dilution"; S05 "Classic basal cistern SAH pattern"; S07 "PKD patient - aneurysm
association known"; P06 "LP is essential regardless of CT result"; P01, P03, P06 "Note: CT
sensitivity ..." essays in the impression and observations. ECG: P06 "consistent with anemia", S04
"metoprolol effect". CTA: P01 "likely the ruptured aneurysm given late-presentation SAH", P05
"radiation exposure discussed with patient". M04 CT (positive) recommends LP: change to "CT
angiography of the head and neck recommended". CT-negative CTs end "Lumbar puncture recommended if
clinical suspicion persists." (diagnostic step, allowed) without the sensitivity essay.
Labs: delete the "Exclusion studies" panels (BNP "Within reference range", 12 cases) and P01 "Mimic
exclusion"; put a numeric normal BNP (and P01 a numeric normal troponin) in the Cardiac panel. Set
the type-and-screen `clinical_significance` to null (29 cases; the template sentence "which is what
this case's diagnosis rests on" is engineering text).
`metadata.case_body_concerns`: empty it wherever it holds the stale CSF or TCD-tool concerns.

### C15. CSF reports in the CT-negative cases (P01, P03, P06)

P01: appearance "Xanthochromic ... clear in all 4 tubes" and RBC "consistent with xanthochromia"
are contradictory; P06: "Pink-tinged ... not grossly bloody due to anemia dilution effect"
(serum anemia does not change CSF RBC; 68,000/uL is grossly bloody) and a bilirubin peak at an LP
done within hours of a 1-hour-old headache (bilirubin needs about 12 hours). Fix in section 4.
Coagulation-before-LP constraint: `soft` (no anticoagulant or coagulopathy in these three).

### C16. Echo and other criteria that do not fit (PATTERNS 4)

Echo label "given troponin elevation" is true in 27 of 28 echo cases; P03 troponin 0.06 (mildly
raised) is acceptable. P01 has an echo output but no criterion: leave it (normal). P01, P03, P06
MRI: `optional` (the LP is diagnostic); P03 and P06 MRI outputs are one-line teaching sentences:
rewrite as reports. S07 (contrast allergy): delete the `MR_angiography` waste entry (MRA is the
reasonable alternative). P05: delete the EEG waste entry (she seized).

---

## 3. Target pathway and tiers

### 3.1 `action_criteria` order and tiers (keep ids; new ones get the ids given)

1. NCCT, required.
2. Labs, required (initial).
3. ECG, required (initial).
4. CSF, required, only P01, P03, P06.
5. CTA, required.
6. Apixaban reversal check `check-apixaban-reversal`, required, M07 and S04 only.
7. DSA `dsa-aneurysm-anatomy` (or the existing id), recommended, all 30.
8. MRI: P05 (PRES) recommended as now; RP11 recommended as now; P01, P03, P06 optional.
9. Nimodipine / home-drug check, tier per C10.
10. Echo, recommended (as now).
11. Telemetry, recommended.
12. TCD, optional.
13. Literature, optional.

No criterion fakes a consult or treatment; securing, EVD, BP, reversal and transfusion are musts.

### 3.2 Follow-ups

Same order: CTA; reversal check (M07, S04); DSA; MRI; drug checks; echo; telemetry; TCD;
canonical literature last. Initial outputs: CT, ECG, labs (and CSF in P01, P03, P06); no initial
`literature_search` or `drug_interactions`.

### 3.3 Sequence constraints

- Every case: NCCT before CTA, `soft`, reason "CTA follows the diagnostic non-contrast CT", id
  pair (action-1-order-ct-scan, the CTA criterion), citation `[Hoh_2023]`.
- Every case with a DSA criterion: CTA before DSA, `soft`.
- M07, S04: `check-apixaban-reversal` before DSA, `hard`, reason "Arterial puncture and
  endovascular work on unreversed apixaban risk access-site and intracranial bleeding".
- P01, P03, P06: keep NCCT before CSF `hard`; change labs before CSF to `soft`.

### 3.4 Stop rule, exemptions, avoided actions

- `required_before_assessment` = exactly the required criteria; `max_additional_actions` 1.
- Keep `panel_required_exemptions.analyze_csf` in the 27 CT-positive cases.
- Avoided actions: keep the 12 waste entries except S07 MRA and P05 EEG (C16); LP severity per C6.

---

## 4. Per-case index

Notes are full ids; "C" refers to section 2. Every case also gets: C1, C2, C3, C4, C5, C7, C9
(magnesium, and potassium where missing), C11 (differential key features), C12, C14 (type and
screen, Exclusion panels where present, stale concerns), section 3. Below are the case-specific
items.

### SAH-M01 (man 45, left MCA, HH2, Fisher 2, outside CT negative; R2 needs_changes)
- 38447471-76b4-4877-990d-e5988eca2fb6: C1, FIXED.
- DSA: keep id, relabel, rewrite output without coiling (C3). Drug check (lisinopril, ibuprofen):
  recommended; remove triple-H; MUST-HOME withhold lisinopril; MUST-BP-A (164/98). NSAID
  prohibition already covers home ibuprofen.
- Remove migraine red herring (no migraine). QTc 498, no MUST-QT.

### SAH-M02 (woman 48, AComA, HH2, Fisher 3, IVH third ventricle, early hydrocephalus; R2 needs_changes)
- bf848453-6712-4272-b24f-d61bb56634ed: C2 (TCD re-dated day 0, its confusion note removed) and
  order (drug check after CTA), FIXED.
- 9bd81d95-96fb-47eb-a556-556933c74f71: remove the migraine red herring, FIXED.
- Amlodipine + HCTZ: drug check required; MUST-HOME withhold amlodipine (and HCTZ); MUST-BP-A.
- MUST-EVD-NOW (third-ventricle blood); LP `contraindicated`. QTc 512: MUST-QT. Delete the
  vasospasm literature (triple-H).

### SAH-M03 (woman 52, right MCA, HH 2-3, migraine history; R2 needs_changes)
- 6b4234fb-3474-40f4-9b88-dc24d8d72a36: delete the Ottawa text (C7); add red herring: data_point
  "Five-year migraine history and brief confusion", correct interpretation "The Ottawa SAH Rule
  excludes patients with recurrent similar headaches or a new neurological deficit, so it cannot
  rule out SAH here; the instantaneous onset unlike her migraines mandates CT", FIXED.
- 6a4a8415-c085-4ef0-afd0-8bbe8ca3b099: delete the reversed LP statement (C7), FIXED.
- Exam: oriented x4 vs GCS 14 (C13). DSA output: remove post-coiling content (C3).
- Drug check sumatriptan + sertraline: recommended (triptan contraindication); MUST-HOME: no
  triptan, continue propranolol (migraine prophylaxis and hypertension) unless bradycardia.

### SAH-M04 (man 55, right PComA, HH2, Fisher 2, coital onset, outside CT negative; R2 needs_changes)
- 03a9ce4b-c764-4ad9-8a57-d602ddd39600: C11 (coital trigger wording and red herring), FIXED.
- 53d4e407-16bc-4eec-ac9f-b80ac3b63e99: C1, FIXED.
- CT: positive but recommends LP: change to CTA recommendation; remove the Hgb observation (C14).
- Metoprolol continue (MUST-HOME); MUST-BP-A (182/108); metformin around contrast is in the drug
  check, fine. Delete family-screening literature.

### SAH-M05 (woman 50, ADPKD, AComA 8.4 mm plus left PComA 3.1 mm, HH3, Fisher 3, hydrocephalus; R2 approved)
- e38a8460-0826-4c02-b86b-27cb655aea7a: add magnesium (low, furosemide) to labs; MUST-QT (QTc 524,
  K 3.4); drug check (ramipril, furosemide) required with the hypokalemia and QTc content, FIXED.
- Exam to HH3 (C13: confused, GCS 14); MUST-EVD-NOW "with depressed consciousness" (C6);
  delete the kidney observation (C14); delete the day-N sodium follow-up (C2); LVEF 38%:
  MUST-LVEF. MUST-SECURE names the ruptured AComA aneurysm first. Delete PKD literature.

### SAH-M06 (woman 43, OCP, smoker, AComA, HH2, Fisher 3, no hydrocephalus; R2 approved)
- c621cf95-92ee-4525-ae03-02202d225c9c: DECLINED for the numbers (M06 QTc 478, K 3.7, no
  furosemide, no U waves); class part FIXED by magnesium in labs (C9). Cite the values in the log.
- Remove the EVD must (no hydrocephalus, C6). Exclusion-studies panel (C14).
- Add must: "Stop the combined oral contraceptive and arrange non-estrogen contraception." (from
  the drug check, which stays recommended). Delete OCP literature. MUST-BP-A (188/112). Home
  ibuprofen covered by the NSAID prohibition.

### SAH-M07 (man 62, AF on apixaban, basilar apex 7.4 mm, HH3, Fisher 4, IVH, hydrocephalus; R2 needs_changes)
- 4daa3aa1-09bf-45fd-978e-98c4e8ee15f6: C1 (window per Hoh, note's 24-72 h not applied), FIXED.
- da99e9e0-0194-487a-a95b-b5f6d7a2e536: EVD must present (ALREADY-FIXED); reworded MUST-EVD-NOW
  "reverse the anticoagulant first" (FIXED, wording).
- 75c2bb0f-fd1a-4ccc-ab01-a8b09d8dad66: nimodipine must present, ALREADY-FIXED; MUST-NIMO wording.
- b12f861e-6d6b-47f7-aba0-5f0ebb66dc8f: MUST-BP-A with nicardipine or clevidipine (LVEF 35%), FIXED.
- 9d172604-37fd-470f-9bc1-d74ccb0abb83: LP avoided action to `contraindicated`, FIXED.
- MUST-REVERSE (low dose; last dose about 6 h before arrival, anti-Xa 186) replaces the generic
  reversal must; keep the reversal prohibition. Reversal check: criterion `check-apixaban-reversal`
  required, output dosing per 1.2 (remove "high-dose protocol indicated"). Hard constraint reversal
  before DSA. Delete initial `drug_interactions` (C8) and the CTA "after anticoagulation reversal"
  (C2). Amlodipine: withhold (drug check required); metoprolol: continue for AF rate.
- Exam (C13); QTc 508 MUST-QT; LVEF 35% MUST-LVEF; telemetry reports AF (C12); fallback cardiac
  monitoring already AF, fine. AF anticoagulation literature: delete; restart timing is in
  MUST-REVERSE.

### SAH-M08 (woman 58, sentinel headache 3 days ago, re-bleed today, right MCA, HH2, Fisher 2-3; R2 needs_changes)
- 5d5b5879-e5ba-44d0-96fc-79e098655dc3: nimodipine must present, ALREADY-FIXED; TCD re-dated to
  admission (day 3 from the sentinel bleed, mild borderline elevation allowed; remove "moderate
  vasospasm"), FIXED for the timeline.
- ee9a1623-1919-4650-a807-236ac826ff1d: replace the migraine red herring with: data_point "Sudden
  severe headache 3 days earlier attributed to stress", field path
  `patient.history_present_illness`, correct interpretation "A sudden severe headache is a possible
  sentinel bleed and needs immediate non-contrast CT; attributing it to stress delayed diagnosis",
  and add the pearl "A sudden, peak-in-seconds headache needs immediate non-contrast CT even when
  attributed to stress or migraine; a sentinel headache days before the major bleed is a missed
  opportunity." FIXED.
- Remove the EVD must (no hydrocephalus). RCVS `moderate` to `low`. Escitalopram QT check:
  recommended. Delete initial `drug_interactions` and sentinel literature. Aspirin allergy (GI
  upset): no conflict. MUST-BP-A.

### SAH-P01 (woman 38, migraine, late presentation day 5, CT negative, LP positive, AComA 3.4 mm; R2 approved)
- 532566ea-2694-40ee-9bf0-47b36a5faeb9: the misattributed thunderclap headache is the case's
  lesson; add the M08 pearl wording with "migraine" and keep the migraine red herring (valid here),
  FIXED.
- 348b8e71-1c5a-4836-9f2c-85fa43775648: CT pearl replaced (1.3); CT report keeps a plain negative
  impression (C14), FIXED.
- CSF: appearance "Clear and colorless to the eye in tubes 1 to 4; supernatant faintly yellow"
  wording consistent with spectrophotometry; RBC fields as plain counts (remove "consistent with
  xanthochromia" and the comment). Replace the "bloody tube 1" red herring with: data_point "Near
  normal CSF red cell count (12 and 8 per uL) five days after onset", correct interpretation "Red
  cells lyse over days; the bilirubin peak on spectrophotometry is the decisive finding in late
  presenters."
- HPI last sentence: "... asked her to come to the ED for urgent evaluation." RCVS to `low`. MRI
  optional. Drug check sumatriptan: recommended; MUST-HOME: no triptan. MUST-BP-B. Potassium and a
  numeric troponin (Cardiac panel) added. Exclusion and Mimic panels deleted.

### SAH-P02 (man 42, perimesencephalic non-aneurysmal SAH, CTA and DSA negative; R2 approved)
- fb64b259-854d-4d07-9e3b-3329c4e0adde: MUST-HOME "Withhold amlodipine while on nimodipine
  (additive dihydropyridine effect) and monitor blood pressure closely"; drug check required,
  FIXED.
- No MUST-SECURE. Instead keep the existing "repeat vascular imaging at 7-14 days" must and add:
  "Manage as aneurysmal SAH (nimodipine, blood pressure control) until catheter angiography
  excludes an aneurysm; with a negative DSA and a perimesencephalic pattern, no securing procedure
  is needed." DSA criterion stays recommended (existing id). MUST-NIMO as written is acceptable
  pending DSA (see section 6).
- Ibuprofen in HPI: NSAID prohibition covers it. Delete both literature follow-ups; canonical
  last. MUST-BP-B (148/88). CT: no hydrocephalus (survey flag was "No hydrocephalus"). CENTRAL
  synonyms (section 5).

### SAH-P03 (woman 46, fibromyalgia and chronic headaches, 18 h, CT negative, LP positive, left PComA; R2 needs_changes)
- 6dcebd64-48c0-46a6-a73b-ee217f8282d3: C1 (Hoh window, the note's 24-72 h not applied), FIXED.
- 7e2fa463-1268-46d7-8024-5ab90b39acb0: LP is already required (ALREADY-FIXED for the LP); CT
  pearl and LP pearl replaced (1.3), FIXED for the numbers.
- Delete the Ottawa literature (wrong exclusion statement). RCVS `low`. MRI optional and rewritten
  as a report (C16). CT impression without the sensitivity essay (C14). Duloxetine check:
  recommended. MUST-BP-B (158/94). Exclusion panel deleted; potassium added.

### SAH-P04 (man 52, AComA 9.2 mm, HH3, Fisher 4, IVH, hydrocephalus, clonazepam, alcohol, INR 1.4; no notes)
- Exam (C13: somnolent, GCS 14). MUST-EVD-NOW; LP `contraindicated`. QTc 518 MUST-QT. LVEF 28%
  MUST-LVEF. MUST-ALCOHOL. MUST-BP-A with nicardipine or clevidipine (LVEF 28%).
- Delete the FFP follow-up (C8) and add must: "INR 1.4 from liver disease: give vitamin K 10 mg IV;
  plasma is not indicated for this degree of prolongation; agree the INR threshold for EVD
  placement with neurosurgery." Clonazepam check: recommended. Delete initial drug block and
  initial literature. Losartan: withhold (MUST-HOME). Drop "Large" (C13).

### SAH-P05 (woman 35, 2 h postpartum, eclampsia with seizure, PRES, right MCA aneurysm; R2 approved)
- f6edc7fb-b9d3-4a48-85ae-1ea4a27a6cb1: MUST-BP-A with "labetalol boluses or nicardipine
  infusion" (postpartum), FIXED.
- f8f0befa-3974-4122-8d3f-23329c837a5d: C1, FIXED.
- Magnesium check: required, `proposed` "Magnesium sulfate infusion for eclampsia with
  nimodipine" (magnesium was loaded per HPI); keep the monitoring warnings; correct the therapeutic
  range to "4.8 to 8.4 mg/dL" if units are mg/dL, else keep mEq/L consistent. Keep the obstetric
  must. Delete the EEG waste entry (C16). CTA "radiation exposure" observation deleted. PRES stays
  in the differential as co-existing (`high`, key features "co-existing; does not explain the
  aneurysmal SAH"). Delete postpartum literature. No home medicines.

### SAH-P06 (man 62, severe iron-deficiency anemia Hb 7.4, CT negative at 1 h, LP positive, left PComA; no notes)
- CSF: appearance "Grossly bloody, uniformly in tubes 1 to 4"; spectrophotometry "Oxyhemoglobin
  peak present; no bilirubin increment (sample obtained less than 12 hours after onset)"; keep the
  non-clearing counts; interpretation updated. Keep the traumatic-tap red herring (non-clearing
  counts answer it).
- CT: remove the "LP is essential" observation and the sensitivity essay (keep the anemia-related
  density statement as an imaging finding). ECG "consistent with anemia" removed (C14).
- Delete the transfusion follow-up (C8) and the TCD transfusion note (C2); add must: "Transfuse red
  cells for hemoglobin 7.4 g/dL to keep it at or above 8 g/dL before the securing procedure (a
  liberal 10 g/dL threshold showed no benefit in the SAHaRA trial); investigate the iron-deficiency
  anemia once stable." Metoprolol: continue (remove "hold"); remove MAP target. MRI optional,
  rewritten report. MUST-BP-A (168/98). Drug check recommended. Delete anemia literature.

### SAH-P07 (woman 44, IIH on acetazolamide, right MCA 3.6 mm; no notes)
- Remove the HPI sentence on LP interpretation (teaching text) and the CT ICP observation (C14).
- IIH flare `moderate` to `low` ("IIH does not produce subarachnoid blood"). Drug check
  (acetazolamide): recommended; delete the invented MAP/ICP target follow-up
  `request_nimodipine_icp_management`. Delete initial drug block (three repeated warnings) and IIH
  literature. MUST-BP-B (132/82). Keep the IIH prohibition.

### SAH-P08 (man 58, CAD with stent 2 years, DAPT plus EMS aspirin 325 mg, AComA 7.8 mm, Takotsubo LVEF 30%, BP 206/122; R2 needs_changes)
- 61a944ea-e7de-4e6b-8a21-b22c3b998136: CTA first, echo after the drug check (C2), FIXED.
- 2b67f747-643d-4df1-afdd-1573bff9b741: MUST-BP-A with nicardipine or clevidipine; MUST-LVEF with
  moderate mitral regurgitation, FIXED.
- DAPT check required; add must: "Hold aspirin and clopidogrel (including the extra EMS dose);
  agree with cardiology given the 2-year-old coronary stent, and consider platelet transfusion only
  if an EVD or open surgery is required." Keep the cath prohibition. QTc 532 MUST-QT. Metoprolol
  continue (post-MI). Exam HH2 (C13). Drop "Large". Delete neurogenic literature (the troponin red
  herring carries the lesson).

### SAH-RM11 (woman 47, brother with unruptured aneurysm, right MCA 5.6 mm, HH2, Fisher 2, BP 154/92; R2 approved)
- a60d0697-5c3c-494b-8000-3df16913057b: C1, C2, C3, FIXED.
- 2ab931d5-3ccb-4696-80e7-b36636f6ec3a: MUST-BP-B; MUST-HOME "Continue propranolol unless
  bradycardia or hypotension (do not stop abruptly); withhold valsartan during the acute phase";
  drug check recommended with that content, FIXED.
- HPI: delete "A CT was performed on arrival." Aspirin allergy (GI bleeding): no conflict. Delete
  family-screening literature.

### SAH-RP11 (woman 40, RRMS on natalizumab, right PComA 4.8 mm; R2 approved)
- 9b8af8ad-26de-47af-8c4a-f75fa4f755a8: C1, C2, C3, FIXED.
- Drug check (natalizumab): recommended; delete the "JC virus PCR in CSF was negative" warning.
  Delete MS literature. CT observation on MS lesions (C14). MUST-BP-B. Lisinopril (MUST-HOME
  withhold) and baclofen (continue; abrupt withdrawal risk).

### SAH-RS11 (woman 54, smoker, aunt with aneurysm, AComA 6.8 mm, HH2, Fisher 3; no notes)
- Amlodipine: drug check required; MUST-HOME withhold amlodipine. MUST-BP-A (188/114). Delete
  smoking literature. QTc 494: no MUST-QT.

### SAH-RS12 (man 51, AComA 8.2 mm, Fisher 4, third-ventricle blood, early hydrocephalus, BP 204/122; R2 needs_changes)
- f87e2dd7-98fd-4446-b3b5-39a4c4a9e86f: C1 (securing) FIXED; drain must present (ALREADY-FIXED),
  reworded MUST-EVD-NOW.
- 03f424a3-fa19-467f-877d-45b88f2492e9: remove the target sentence; MUST-BP-A with nicardipine or
  clevidipine (LVEF 38%); MUST-HOME withhold lisinopril and HCTZ, FIXED.
- TCD day 8 with new deficits: re-date (C2). Delete day-4 sodium follow-up. QTc 512 MUST-QT. LVEF
  38% MUST-LVEF. MUST-ALCOHOL (3-4 drinks daily). LP `contraindicated`. Drop "Large". Remove "Classic
  presentation". Delete initial literature.

### SAH-S01 (woman 52, AComA 5.4 mm, HH2, Fisher 3; R2 approved)
- fddcb39d-16c7-4bdd-bdab-ba85e450e0f6: C1, C2, C3, FIXED.
- Losartan: recommended check; MUST-HOME; MUST-BP-A (182/106). Delete guideline literature
  (triple-H, 24-48 h).

### SAH-S02 (man 58, coital onset, right PComA 6.2 mm, HH2, Fisher 3; no notes)
- C11 coital wording and red herring (as M04). Lisinopril: recommended; MUST-HOME. MUST-BP-A.
  Metformin with contrast: keep in drug check if present. Delete guideline literature. CT
  impression already "No intraventricular extension": fine.

### SAH-S03 (woman 44, OCP, left MCA 5.0 mm, HH2, Fisher 3; no notes)
- Amlodipine: required check; MUST-HOME withhold amlodipine. OCP must as M06. MUST-BP-A. Delete OCP
  literature.

### SAH-S04 (man 63, paroxysmal AF on apixaban, AComA 7.2 mm, HH2, Fisher 4; R2 approved)
- cabb6393-ffec-4695-9d58-f4509ee19eda: C1, C2, C3; MUST-REVERSE (last dose 8 h, anti-Xa 164:
  low dose) and hard constraint reversal before DSA, FIXED.
- 60a5d171-e5f5-4984-b216-5051d459ab98: remove both metoprolol holds and the digoxin alternative;
  MUST-HOME "Continue metoprolol for AF rate control unless bradycardia or hypotension; withhold
  ramipril during the acute phase"; MUST-BP-A; nimodipine part ALREADY-FIXED (must present), FIXED.
- Reversal check output: dosing per 1.2 (remove "<10 mg / >10 mg", "less effective"). Add IVH to CT
  for Fisher 4 (C13), then LP `contraindicated`. ECG "metoprolol effect" removed. Delete
  anticoagulation-restart literature (restart is in MUST-REVERSE). Drop "Large".

### SAH-S05 (woman 49, no medicines, AComA 4.6 mm ruptured plus incidental right ICA 2.8 mm; no notes)
- Drug check optional (no medicines); delete initial drug block. Delete all three literature
  follow-ups. Add must: "Secure the ruptured AComA aneurysm first; the small incidental right ICA
  aneurysm is managed separately (surveillance or elective treatment) after recovery." MUST-SECURE
  phrase per 1.3. MUST-BP-A (166/94). Exclusion panel deleted; potassium added.

### SAH-S06 (man 56, verapamil, sertraline, heavy alcohol, AComA 5.8 mm, QTc 516, BP 198/114; R2 approved)
- c3c56bb2-e199-4805-8f47-f61e0110d4d2: C1, C2, C3, FIXED.
- 7f1b4f47-fcf5-46eb-88f3-4c840fe7861c: add potassium and low-normal magnesium to labs; MUST-QT,
  FIXED.
- 633fd9a3-78f1-4d02-b4fc-bb8db375af6f: MUST-BP-A (nicardipine, clevidipine or labetalol; LVEF
  42%); replace the hydralazine alternative; MUST-HOME "Withhold verapamil (additive effect with
  nimodipine); withhold sertraline while QTc exceeds 500 ms", FIXED.
- MUST-ALCOHOL. Drug check required. Delete both literature follow-ups. Exam wording (C13).

### SAH-S07 (woman 61, ADPKD, brother died of SAH, cousin with aneurysm, contrast rash, nifedipine, right paraclinoid ICA 5.4 mm; R2 approved)
- 09f3f88b-7b15-493d-bbc4-4781ca0d3624: C1, C2, C3, FIXED.
- aa75afaa-2dab-42e4-8ea1-9bfaaaca6691: replace the pearl with "ADPKD with a family history of
  intracranial aneurysm or SAH is an indication for screening MR angiography; this patient
  qualified but had never been screened." FIXED.
- db7c626e-f23a-4d71-baec-574d34083831: MUST-BP-A; MUST-HOME withhold nifedipine ER; nimodipine
  part ALREADY-FIXED (must present), FIXED.
- Add must: "Do not delay the CTA for the prior mild contrast rash; give accelerated premedication
  per local protocol if it causes no delay." Delete MRA waste (C16), the kidney observation and
  "PKD patient" observation (C14), both literature follow-ups. Drug check required. Creatinine 1.4:
  no change needed.

### SAH-S08 (man 38, cocaine, AComA 6.4 mm, BP 212/126, HR 118, LVEF 42%; R2 approved)
- 6e139dfe-4ffd-45f4-85a0-a303f583594e: delete the cocaine literature; drug-check warning
  becomes "Cocaine use: avoid beta-blockers; labetalol is not first line; use nicardipine or
  clevidipine, with benzodiazepines for agitation and tachycardia", FIXED.
- 25ff44d7-2ee9-4cc5-9b44-32766f58adbe: C1, C2, C3, FIXED.
- 4f899419-8c58-4575-a0cc-899716794530: MUST-BP-A worded "Lower blood pressure now with a
  nicardipine or clevidipine infusion and treat cocaine-related agitation and tachycardia with a
  benzodiazepine; do not give beta-blockers during acute cocaine toxicity; avoid hypotension
  [Hoh_2023]." FIXED.
- Drug check optional (no medicines). Keep the cocaine prohibition. Drop "Large".

### SAH-S09 (woman 67, CKD 3 eGFR 42, diabetes, furosemide, left PComA 4.8 mm; R2 approved)
- 899fabe8-c432-4165-bde1-0c1132149643: C1, C2, C3, FIXED.
- Drug check recommended (candesartan, metformin, furosemide; furosemide is a real home drug).
  MUST-HOME withhold candesartan and furosemide, hold metformin around contrast. Low-normal
  magnesium (furosemide). MUST-BP-A. Delete both literature follow-ups (patient values).
  Penicillin anaphylaxis: no conflict.

### SAH-S10 (man 53, lithium, HCTZ, AComA 4.6 mm with nipple sign; R2 approved)
- 66c7702e-ae23-405b-8ba8-d7325301e810: C1, C2, C3, FIXED.
- Drug check required (lithium, HCTZ); add must: "Withhold hydrochlorothiazide and check serum
  lithium and sodium together at least daily, as SAH-related hyponatremia raises lithium levels."
  MUST-BP-A. Delete both literature follow-ups (one states SIADH has low urine osmolality).

---

## 5. CENTRAL requests

1. Criteria pack `dataset-generation/criteria_packs/SAH.md`: (a) `[Perry_2011]` title is wrong:
   BMJ 2011;343:d4277 is "Sensitivity of computed tomography performed within six hours of onset
   of headache for diagnosis of subarachnoid haemorrhage: prospective cohort study"; (b) add
   `[Perry_2013]` (Ottawa SAH Rule, JAMA 2013;310:1248-1255), `[Molyneux_2002]` (ISAT, Lancet
   2002;360:1267-1274), `[Drew_2010]` (Circulation 2010;121:1047-1060); (c) section 5 "clipping or
   coiling within 24-72h" becomes "as early as feasible, preferably within 24 hours [Hoh_2023]";
   (d) literature "required" and drug check "required" in section 2 are superseded by rulings 5 and
   6; (e) xanthochromia "≥6-12h" should read about 12 hours; (f) TCD tier optional (July review).
2. Allow-list the ESO/EANS/ESMINT 2026 aSAH guideline R2 cites, once Andrea supplies the
   reference.
3. Synonyms (`diagnosis_synonyms.yaml`): SAH-P02 (I60.8, perimesencephalic non-aneurysmal SAH)
   inherits the I60 category labels "aneurysmal subarachnoid hemorrhage", "ruptured intracranial
   aneurysm", "ruptured cerebral aneurysm" and all I60.x codes, so an answer of aneurysmal rupture
   scores as correct. Exclude the aneurysmal labels and the location codes (I60.0 to I60.7) from
   I60.8 cases.
4. Vocabulary: no new term needed (`cerebral_angiography`, `transcranial_doppler`, `magnesium`,
   `xanthochromia_spectrophotometry` are priced).
5. Review UI: show initial outputs and follow-ups in criterion order (already requested).

## 6. Open questions for Andrea

1. EVD with GCS 15: this plan gives an EVD must when hydrocephalus comes with intraventricular
   blood (M02, RS12), following R2's RS12 note, although the guideline's wording is "acute
   symptomatic hydrocephalus". Confirm, or make M02 and RS12 conditional (MUST-EVD-WATCH).
2. DSA tier: recommended in all 30. Should it be required when CTA is negative (P02), or in every
   case where it precedes coiling?
3. Nimodipine in P02 (perimesencephalic, negative DSA): keep the 21-day must or allow stopping
   after a negative DSA? Practice varies.
4. The ESO/EANS/ESMINT 2026 and AANN 2025 references R2 cites: do you have the citations for the
   allow-list?
5. Labels with a grade range (M03 "Hunt-Hess 2-3", S05 "Hunt-Hess 1-2", M08 "Fisher 2-3") are left
   as they are (ruling 3); S05's exam is grade 2. Should the labels be tightened centrally?
6. Seven unnoted cases (P04, P06, P07, RS11, S02, S03, S05) have no status in the notes file; this
   plan assumes they are among R2's 21 approvals. Please confirm.
