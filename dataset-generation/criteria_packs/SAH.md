# Criteria pack: Subarachnoid hemorrhage (aneurysmal)

**ICD-10:** I60.x (by location; I60.8 for perimesencephalic non-aneurysmal SAH)
**Condition enum:** `NeurologicalCondition.SUBARACHNOID_HEMORRHAGE`
**Case ID prefix:** `SAH`

Revised 24 Oct 2026 after the October 2026 review round (plan `data/review/round-2026-10/plans/SAH.md`,
decisions `plans/SAH-decisions.md`). `[Hoh_2023]` governs every management statement; where it and
`[Connolly_2012]` differ (pre-securing blood pressure target), Hoh governs and Connolly is cited only
for the historical numeric target. `[Vergouwen_2026]` (ESO/EANS/ESMINT) agrees on the 24-hour
securing window and may be cited beside Hoh.

---

## 1. Diagnostic criteria

Clinical presentation: thunderclap headache (maximal within seconds to a minute, "worst headache of
life"), often with vomiting, brief loss of consciousness, neck stiffness, photophobia; focal deficits
from hematoma, hydrocephalus or, later, delayed cerebral ischemia. Severity: Hunt-Hess grade
`[Hunt_Hess_1968]` and WFNS grade (I-V), judged at examination, not from a brief LOC that has
resolved. Hunt-Hess: 1 asymptomatic or mild headache, slight nuchal rigidity; 2 moderate to severe
headache, nuchal rigidity, no deficit other than cranial nerve palsy; 3 drowsiness, confusion or mild
focal deficit; 4 stupor, moderate to severe hemiparesis; 5 coma. "Alert and oriented x4" with GCS 15
cannot be grade 3. The grade is the agent's judgment: it never appears in the patient block.

CT blood: Fisher grade `[Fisher_1980]`: 1 no blood; 2 diffuse thin (<1 mm); 3 localized clot or
thick layer (1 mm or more); 4 intracerebral or intraventricular clot (grade 4 needs IVH or ICH on
the CT). A case label names one grade, never a range.

Diagnostic pathway:
1. Non-contrast CT first. Within 6 hours of onset, on a modern scanner read by an experienced
   radiologist, CT is close to 100% sensitive `[Perry_2011]`; sensitivity falls after 6 hours and
   markedly by days 5 to 7; anemia lowers it at any time.
2. After a negative CT, LP is indicated when the patient presents more than 6 hours after onset or
   has a new neurological deficit `[Hoh_2023]`; within 6 hours a negative CT has its highest
   negative predictive value. Spectrophotometric bilirubin needs about 12 hours to form and
   persists for about two weeks or longer; oxyhemoglobin alone appears earlier and also follows a
   traumatic tap. Non-clearing red cells across tubes 1 to 4 support SAH.
3. CTA after the NCCT (a separate acquisition) to find the aneurysm. Catheter DSA with 3D
   rotational angiography confirms the aneurysm and its anatomy before securing, and is the
   reference test when CTA is negative (indicated for detection except when a noninvasive
   angiogram has already shown the aneurysm, `[Connolly_2012]` Class I).

Ottawa SAH Rule `[Perry_2013]`: for alert patients aged 15 or more with a new severe non-traumatic
headache peaking within one hour. Investigate if any of: age 40 or more; neck pain or stiffness;
witnessed loss of consciousness; onset during exertion; thunderclap onset (instantly peaking
pain); limited neck flexion on examination. Not applicable with a new neurological deficit,
previous aneurysm or SAH, known brain tumour, or recurrent similar headaches (3 or more episodes
over 6 months or more).

## 2. Standard workup hierarchy

Pathway order (criteria and follow-ups): NCCT, labs, ECG, (CSF in CT-negative cases), CTA,
anticoagulant-reversal check where relevant, DSA, MRI where it has a question, drug check, echo,
telemetry, TCD, literature last.

**Required:**
- `order_ct_scan` (`contrast: false`, `angiography: false`) - first study; subarachnoid blood and its
  distribution, intraventricular blood, hydrocephalus [Hoh_2023]
- `order_ct_scan` (`contrast: true`, `angiography: true`, CTA head and neck) - localizes the aneurysm
  and defines the anatomy that decides coiling or clipping [Hoh_2023]
- `interpret_labs` (`panels: [CBC, BMP, coagulation]`) - blood count, sodium, potassium, magnesium,
  renal function and coagulation before securing or CSF diversion and for sodium and QTc management;
  the stored report also carries troponin, BNP (numeric) and type and screen [Hoh_2023]
- `analyze_ecg` - neurogenic changes (deep T-wave inversions, QTc prolongation, ST changes) and the
  QTc baseline; screens for a primary cardiac event [Hoh_2023]
- `analyze_csf` - only after a negative or non-diagnostic NCCT (CT-negative cases), with tube 1 and
  tube 4 counts and xanthochromia spectrophotometry [Hoh_2023] [Edlow_2008]
- `check_drug_interactions` - required only when the case has an interaction that changes
  management (ruling 6): a home dihydropyridine or verapamil with nimodipine, a diuretic with a long
  QTc and low potassium, magnesium sulfate with nimodipine, antiplatelets or anticoagulants, lithium
  with a thiazide; otherwise recommended or optional. The separate apixaban reversal check is required
  where apixaban was taken (`check-apixaban-reversal`).

**Recommended:**
- `order_advanced_imaging` (`modality: cerebral_angiography`) - catheter DSA with 3D rotational imaging,
  diagnostic report only (size, neck, dome-to-neck ratio, branches, other aneurysms, vasospasm), never
  coiling, clipping or a Raymond class. **Required** when CTA is negative (perimesencephalic case,
  SAH-P02).
- `order_echocardiogram` - when troponin is raised or the ECG shows neurogenic changes; informs the
  anesthetic plan
- `order_cardiac_monitoring` (`monitor_type: telemetry`) - arrival to assessment (2 to 6 hours),
  case-specific rhythm, ectopy and QTc; no 24-hour report at assessment time
- `analyze_brain_mri` - only with a case question (PRES, a natalizumab-treated patient); optional in
  CT-negative cases, where the LP is diagnostic

**Optional:**
- `order_advanced_imaging` (`modality: transcranial_doppler`) - admission baseline (COR 2a in
  [Hoh_2023]); velocities at the day of presentation, no clinical notes, serial studies recommended
  during days 3 to 14
- `search_medical_literature` - general evidence on grading and on coiling versus clipping; never a
  clinical step, never the case's expected text (ruling 5); last in the pathway
- `order_advanced_imaging` (`modality: MR_angiography`) - only where CTA is unsuitable (prior contrast
  reaction); elsewhere waste after the CTA. Every case stores an MRA report consistent with its CTA,
  so an MRA order never returns a normal study

Superseded (24 Oct 2026): literature "required" and drug check "required" in every case (rulings 5
and 6); TCD "recommended, daily days 4-14" (July 2026 tool review: optional); "specialist referral"
as a clinical action (management lives in the musts, ruling 4).

**Management musts** (`required_recommendations`; never tool calls): enteral nimodipine 60 mg every
4 hours for 21 days, 30 mg every 2 hours if it causes hypotension [Hoh_2023]; urgent joint
neurosurgical and neurointerventional review and securing of the ruptured aneurysm by coiling or
clipping as early as feasible, preferably within 24 hours of onset [Hoh_2023] [Vergouwen_2026]
(technique chosen jointly; in aneurysms suitable for both, coiling gave better one-year independent
survival [Molyneux_2002]); neurocritical care admission; blood pressure: with SBP 160 or more, lower
it now with a short-acting titratable IV agent (nicardipine or clevidipine infusion, or labetalol
boluses; not labetalol with LVEF 40% or less, bradycardia, asthma or acute cocaine toxicity; no
hydralazine), no numeric target in [Hoh_2023], SBP below 160 the common target [Connolly_2012];
below 160, monitor and treat a sustained rise; home drugs per class (withhold dihydropyridines and
verapamil while on nimodipine; ACE inhibitor, ARB, thiazide may be withheld; continue
beta-blockers unless bradycardia or hypotension, always when they are AF rate control or post-MI
therapy); DCI surveillance days 3 to 14 with frequent examinations, euvolemia, no prophylactic
hypervolemia; sodium monitoring and no hypotonic fluids; QTc 500 ms or more or hypokalemia: K at
least 4.0 mmol/L, Mg at least 2.0 mg/dL, no added QT-prolonging drugs, continuous ECG
[Drew_2010]; LVEF 40% or less: cardiology and neuroanesthesia before securing.

**Hydrocephalus:** urgent EVD for acute symptomatic hydrocephalus [Hoh_2023]: depressed
consciousness, or a decline attributable to the hydrocephalus. In an alert patient (GCS 15) with
early radiological hydrocephalus, even with intraventricular blood, the must is urgent
neurosurgical review with hourly checks, repeat CT on any decline and EVD if it becomes symptomatic.

**Anticoagulant reversal (apixaban, US andexanet label):** low dose (400 mg bolus at 30 mg/min, then
4 mg/min up to 120 minutes) when the last dose was 5 mg or less, or 8 hours or more before; high dose
only when more than 5 mg (or unknown) and less than 8 hours before (or unknown time); alternative
four-factor PCC 50 IU/kg. Andexanet causes heparin resistance, which matters for coiling.
Idarucizumab is for dabigatran and vitamin K for warfarin.

## 3. Tools that are typically USELESS (waste)

- `analyze_eeg` - only if non-convulsive status is suspected as the cause of altered mental status (a
  patient who has seized, e.g. eclampsia, is not a waste case)
- `order_specialized_test` (EMG/NCS, polysomnography, ...) - none indicated acutely
- `order_advanced_imaging` (`amyloid_PET`, `tau_PET`, `DaTscan`, `FDG_PET`, `MIBG_scan`,
  `MR_spectroscopy`, `perfusion_MRI`, `carotid_duplex`; `MR_angiography` after a CTA)

## 4. Tools that are HARMFUL / contraindicated

- `analyze_csf` after a CT that shows SAH: `contraindicated` with mass effect, IVH, hydrocephalus or
  anticoagulation; `harm` otherwise (adds nothing and risks rebleeding or herniation)
  [Hoh_2023] [Edlow_2008]
- Prohibitions (`prohibited_recommendations`): LP before NCCT; antiplatelets and NSAIDs before
  securing; cardiac catheterization for neurogenic troponin; parenteral injection of nimodipine
  capsule contents (an IV infusion formulation exists in Europe, so "never IV" is wrong as written);
  leaving severe hypertension untreated before securing, or lowering BP to hypotension.

## 5. Sequence constraints

- NCCT before CTA (`soft`): CTA follows the diagnostic non-contrast CT [Hoh_2023]
- CTA before DSA (`soft`)
- `check-apixaban-reversal` before DSA (`hard`): arterial puncture and endovascular work on
  unreversed apixaban risk access-site and intracranial bleeding
- CT-negative cases: NCCT before CSF (`hard`) [Edlow_2008]; labs (coagulation) before CSF (`soft`
  without an anticoagulant or coagulopathy; `hard` with one)
- Securing as early as feasible, preferably within 24 hours of onset [Hoh_2023] [Vergouwen_2026], is
  a must, not a sequence constraint (it is not a tool call).

## 6. Subtype variations

- **M (mild):** Hunt-Hess 1-2, small aneurysm, GCS 14-15; standard workup, urgent securing
- **S (standard):** Hunt-Hess 2-3, classic presentation; standard workup with monitoring for
  complications
- **P (progressive / severe or atypical):** Hunt-Hess 3-5, hydrocephalus, IVH, anticoagulation,
  cardiomyopathy, CT-negative late presentation; EVD when hydrocephalus is symptomatic
- **R (mimic / non-aneurysmal):** thunderclap headache without aneurysmal SAH: perimesencephalic
  non-aneurysmal SAH (I60.8; CTA and DSA negative), RCVS (convexity SAH, segmental
  vasoconstriction), cervical artery dissection, pituitary apoplexy, CVST, thunderclap migraine
  (diagnosis of exclusion), spontaneous intracranial hypotension

## 7. Common red-herring categories

- **Severe headache resolved or attributed to stress or migraine** - a sentinel headache days before
  the major bleed needs immediate NCCT; misattribution delays diagnosis
- **Negative CT in a late presenter or an anemic patient** - LP is indicated after 6 hours or with a
  deficit
- **Bloody LP** - traumatic tap clears from tube 1 to tube 4 and has no bilirubin; SAH has
  non-clearing counts and, after about 12 hours, bilirubin on spectrophotometry
- **Coital or exertional onset** - classic for RCVS and for aneurysmal rupture alike
- **Neurogenic troponin, T-wave inversions, apical ballooning** - stress cardiomyopathy, not a
  primary coronary event; the echo reports the wall-motion pattern, it does not "confirm" etiology,
  and a mild apical hypokinesis with preserved EF is not called Takotsubo
- **Atraumatic SAH without aneurysm on CTA** - perimesencephalic non-aneurysmal SAH (pretruncal
  blood), which DSA must confirm
- **Normotensive patient** - absence of hypertension does not exclude SAH

## 8. Allowed citations

- `[Hoh_2023]` - Hoh BL, Ko NU, Amin-Hanjani S, et al. 2023 Guideline for the management of patients
  with aneurysmal subarachnoid hemorrhage: a guideline from the American Heart Association/American
  Stroke Association. Stroke 2023;54:e314-e370. **Governs.**
- `[Vergouwen_2026]` - Vergouwen MDI, Ramos-Pachon A, Terecoasa EO, et al. European Stroke
  Organisation (ESO), European Association of Neurosurgical Societies (EANS) and European Society for
  Minimally Invasive Neurological Therapy (ESMINT) guideline on aneurysmal subarachnoid haemorrhage.
  Eur Stroke J 2026;11(5):aakag043. doi:10.1093/esj/aakag043 (expert consensus: treat the ruptured
  aneurysm within 24 h after ictus when the most dedicated team is available). Verified 24 Oct 2026.
- `[Connolly_2012]` - Connolly ES Jr, Rabinstein AA, Carhuapoma JR, et al. Guidelines for the
  management of aneurysmal subarachnoid hemorrhage. Stroke 2012;43:1711-1737. Superseded by
  `[Hoh_2023]` for management; cite only for the historical SBP <160 target and the DSA
  indication.
- `[Edlow_2008]` - Edlow JA, Panagos PD, Godwin SA, et al. Clinical policy: critical issues in the
  evaluation and management of adult patients presenting to the emergency department with acute
  headache. Ann Emerg Med 2008;52:407-436.
- `[Perry_2011]` - Perry JJ, Stiell IG, Sivilotti MLA, et al. Sensitivity of computed tomography
  performed within six hours of onset of headache for diagnosis of subarachnoid haemorrhage:
  prospective cohort study. BMJ 2011;343:d4277. (Title corrected 24 Oct 2026; the earlier pack
  gave the title of a different Perry paper.)
- `[Perry_2013]` - Perry JJ, Stiell IG, Sivilotti MLA, et al. Clinical decision rules to rule out
  subarachnoid hemorrhage for acute headache. JAMA 2013;310:1248-1255. (Ottawa SAH Rule.)
- `[Hunt_Hess_1968]` - Hunt WE, Hess RM. Surgical risk as related to time of intervention in the
  repair of intracranial aneurysms. J Neurosurg 1968;28:14-20.
- `[Fisher_1980]` - Fisher CM, Kistler JP, Davis JM. Relation of cerebral vasospasm to subarachnoid
  hemorrhage visualized by computerized tomographic scanning. Neurosurgery 1980;6:1-9.
- `[Molyneux_2002]` - Molyneux A, Kerr R, Stratton I, et al. International Subarachnoid Aneurysm
  Trial (ISAT) of neurosurgical clipping versus endovascular coiling in 2143 patients with ruptured
  intracranial aneurysms: a randomised trial. Lancet 2002;360:1267-1274.
- `[Drew_2010]` - Drew BJ, Ackerman MJ, Funk M, et al. Prevention of torsade de pointes in hospital
  settings: a scientific statement from the American Heart Association and the American College of
  Cardiology Foundation. Circulation 2010;121:1047-1060.
- `[English_2024]` - English SW, Delaney A, Fergusson DA, et al. Liberal or restrictive transfusion
  strategy in aneurysmal subarachnoid hemorrhage (SAHaRA). N Engl J Med 2025;392:1079-1088
  (online 10 Dec 2024, hence the key). doi:10.1056/NEJMoa2410962. (Liberal threshold 10 g/dL gave
  no benefit over 8 g/dL.)
- `[Thompson_2015]` - Thompson BG, Brown RD Jr, Amin-Hanjani S, et al. Guidelines for the management
  of patients with unruptured intracranial aneurysms. Stroke 2015;46:2368-2400. (Screening of
  relatives when two or more first-degree relatives have an aneurysm or SAH; ADPKD with a family
  history.)

Not allow-listed: "AANN 2025" (Reviewer 2): no 2025 AANN SAH guideline could be found on 24 Oct
2026 (the AANN guideline found is from 2010); not cited in any case.
