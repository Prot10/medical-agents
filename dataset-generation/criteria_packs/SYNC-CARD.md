# Criteria pack: Cardiac syncope

**ICD-10 (primary codes of the 30 cases):** I44.1 / I44.2 (second-degree / complete AV block),
I45.6 (pre-excitation), I45.81 (long QT syndrome), I47.1 / I47.2 (SVT / VT), I48.3 (typical
atrial flutter), I49.5 (sick sinus syndrome), I49.8 (Brugada syndrome), I42.1 (obstructive HCM),
I42.8 (ARVC), I35.0 (aortic stenosis), I26.09 (PE with acute cor pulmonale), D15.1 (cardiac
myxoma), D86.85 (cardiac sarcoidosis), G13.1 (paraneoplastic brainstem syndrome, the neurological
mimic). R55 (syncope and collapse) is the panel code only and is never an accepted diagnosis code.
**Condition enum:** `NeurologicalCondition.SYNCOPE_CARDIAC`
**Case ID prefix:** `SYNC-CARD`

Revised 24 Oct 2026 (October 2026 review round close-out; `data/review/round-2026-10/plans/SYNC-CARD.md`
and `SYNC-CARD-decisions.md`). Statements below are the plan's canonical facts; a case may depart
from them only with a logged, case-specific reason.

---

## 1. Diagnostic criteria [ESC_2018] [ACC_AHA_HRS_2017]

**Cardiac syncope** = transient loss of consciousness from cerebral hypoperfusion of cardiac
origin: arrhythmic (AV block, sinus node dysfunction, VT, SVT, inherited channelopathies,
pre-excitation) or structural (severe aortic stenosis, obstructive HCM, cardiac tumour or
thrombus, acute PE, pulmonary hypertension, tamponade).

- **Initial evaluation (ESC 2018):** history, examination, supine and standing BP and a 12-lead ECG.
- **High-risk features** (early in-hospital evaluation and immediate ECG monitoring, bedside or
  telemetry, Class I): syncope during exertion or supine; palpitations immediately before the event;
  known structural or coronary heart disease; family history of sudden death under 40; an ECG with
  Mobitz II, complete heart block, bifascicular block, QTc above 460 ms, a Brugada type 1 pattern,
  pre-excitation, NSVT or epsilon waves.
- **Diagnostic ECG or monitoring:** syncope coinciding with a brady- or tachyarrhythmia; without
  symptoms, Mobitz II or third-degree block, a pause over 3 s awake, or rapid prolonged SVT/VT make an
  arrhythmic mechanism likely. A normal ECG does not exclude cardiac syncope.
- **Risk scores:** EGSYS [EGSYS_2008] and ROSE [ROSE_2010] support, never replace, the ESC risk features.
- **Disease definitions used by the cases:** congenital LQTS when QTc is 480 ms or more on repeated
  ECGs or the LQTS score exceeds 3 [ESC_2022_VA_SCD]; Brugada syndrome from a spontaneous or
  fever-induced type 1 pattern [ESC_2022_VA_SCD]; CPVT from exercise-induced bidirectional or
  polymorphic ectopy in a structurally normal heart [ESC_2022_VA_SCD]; ARVC by the 2010 Task Force
  criteria [ARVC_TFC_2010]; obstructive HCM from an LVOT gradient of 50 mmHg or more at rest or on
  provocation [ESC_2023_Cardiomyopathy]; severe AS from AVA below 1.0 cm2, mean gradient 40 mmHg or
  more, or Vmax 4 m/s or more [ESC_EACTS_2025_VHD]; cardiac sarcoidosis from histology (myocardial or
  extracardiac) with a consistent cardiac imaging pattern [HRS_2014_Sarcoid]; acute rheumatic fever
  recurrence by the Jones 2015 criteria [Gewitz_2015]; paraneoplastic neurological syndrome by the
  PNS-Care score [Graus_2021].

## 2. Standard workup hierarchy

> **Clinical tool review, July 2026 (Reviewer 2).** Five annotations on this panel, all
> applied: cardiac monitoring raised to REQUIRED, laboratory studies lowered to OPTIONAL and
> narrowed to targeted assays, EEG and brain MRI retained but re-scoped to the two
> differential-diagnosis indications the guideline supports, and a new OPTIONAL item for
> second-line cardiac imaging.

Pathway order (the order of `followup_outputs` and of `action_criteria`): 12-lead ECG; targeted
labs; TTE; monitoring; the second-line test of the mechanism (CMR, cardiac FDG-PET, CTPA, exercise
test or exercise echo, polysomnography, tissue); drug check; off-pathway reports (tilt, brain MRI,
head CT, EEG, genetics, CSF where kept); literature last.

**Required:**
- `analyze_ecg` (12-lead), every case, first test. It takes only `clinical_context`: no case stores a
  "repeat ECG" follow-up [ESC_2018].
- `order_echocardiogram` (`echo_type: TTE`) when structural heart disease is known or suspected
  (Class I); recommended, not required, where the diagnosis is electrocardiographic and the TTE only
  excludes structure (Brugada). Report LVEF (method), maximal wall thickness, LV dimensions, LA size,
  valves with gradients (AVA, mean gradient and Vmax in AS; LVOT gradient at rest and on Valsalva in
  HCM), RV size and function (TAPSE), PASP, pericardium and masses; no diagnosis sentence and no
  bubble or PFO framing [ESC_2018].
- `order_cardiac_monitoring`, every case, modality by risk and event frequency: `telemetry` in
  hospital with high-risk features (Class I), `holter_24h`/`holter_48h` accepted beside it;
  `event_monitor_14d`/`_30d` for events within a 4-week window (IIa) [Locati_2016];
  `implantable_loop_recorder` for recurrent infrequent unexplained syncope (Class I). The stored
  report names its type truthfully and agrees with the ECG (escape rate, pauses, time stamps), and
  `fallback_tool_outputs.cardiac_monitoring` is the same recording [ESC_2018].
- The test that finds the cause when the mechanism needs one: inflammatory markers (ESR, CRP, ASO) in
  suspected rheumatic carditis; cardiac FDG-PET and nodal biopsy in suspected sarcoid
  [HRS_2014_Sarcoid]; CTPA (`order_body_imaging` `chest_CTA`) in high-probability PE
  [ESC_2019_PE]; CMR in ARVC, HCM and a cardiac mass [ESC_2023_Cardiomyopathy]; exercise echo in
  HCM with a resting and Valsalva gradient below 50 mmHg (Class I) [ESC_2023_Cardiomyopathy];
  exercise test in suspected CPVT (Class I) [ESC_2022_VA_SCD]; ILR when events are months apart.

**Targeted (required only when the named assay drives a decision; otherwise recommended BMP):**
- `interpret_labs`: haemoglobin or haematocrit when bleeding is suspected; electrolytes (BMP) and
  magnesium when an arrhythmia or QT prolongation may be electrolyte driven; troponin and BNP when
  ischaemia, PE or heart failure is in question; D-dimer only at low or intermediate PE probability;
  beta-hCG only where pregnancy changes the imaging decision, never in a woman aged 55 or over; TSH
  only where a thyroid mechanism is on the differential (SVT, flutter, sinus node dysfunction, QT).
  Untargeted thyroid, inflammatory, autoimmune and paraneoplastic panels have no role, except the
  onconeural panel in the paraneoplastic mimic [ESC_2018].
- `check_drug_interactions` (requires `drug`): `required` only for a concrete interaction that
  changes management (QT-prolonging drugs in torsades; AV-nodal blockers in sinus node dysfunction or
  AV block; vasodilators in obstructive HCM; chloroquine in conduction disease; lamotrigine in AV
  block; duplicate beta-blockers; the anticoagulant against aspirin), `recommended` when a
  rate-slowing or QT-active drug is on the list or a new drug is planned, otherwise `optional`. One
  follow-up per named drug, in report voice; the medication-list review stored as the initial and
  fallback block so an unnamed drug is answered with this patient's list.

**Recommended or optional second-line imaging** (report the finding with its relation to the
mechanism; a structural finding alone does not establish the cause):
- `order_advanced_imaging` `cardiac_MRI`: recommended in AV block before 60 without a clear cause
  (ESC 2021 IIa: sarcoid, myocarditis, laminopathy) [ESC_2021_Pacing]; optional in degenerative AV
  block at 60 or over.
- `order_advanced_imaging` `cardiac_FDG_PET` (not `FDG_PET`, the cerebral scan): suspected sarcoid.
- `order_advanced_imaging` `coronary_CTA` / `coronary_angiography`: when ischaemia is a possible
  substrate of a ventricular arrhythmia [ESC_2022_VA_SCD].
- `order_body_imaging` `chest_CT` / `chest_CTA`: PE, aortic dissection, an intrathoracic mass or
  nodal staging. `order_ct_scan` images the head and neck only.
- `obtain_tissue_diagnosis` `lymph_node_biopsy`: the most accessible FDG-avid site in sarcoid.
- `order_specialized_test` `exercise_stress_test`: exertional syncope only after the TTE has excluded
  severe AS and obstructive HCM (hard sequence); optional or recommended in ARVC, LQTS, WPW. It does
  not measure an outflow gradient (`order_echocardiogram` `exercise_echo` does) [Fletcher_2013].
- `search_medical_literature`: optional at most, never in the stop rule, follow-ups last; stored
  outputs give real guideline content, never the case's expected text or a conclusion about the
  patient. A neutral `initial_tool_outputs.literature_search.general` block (initial evaluation and
  risk stratification) answers generic queries; follow-up triggers carry the condition's own words.

**Not in the vocabulary (written as musts until CENTRAL adds them):** electrophysiology study,
sodium-channel-blocker (ajmaline) challenge, cardiac genetic panels, active stand, whole-body
FDG-PET for a tumour search. Never stored under another tool.

## 3. Tools that are typically USELESS (waste avoided actions)

- `analyze_eeg`: waste (ESC 2018 Class III) unless a prior seizure label makes the epilepsy question
  explicit (then optional); interictal EEG is usually normal.
- `analyze_brain_mri`: waste (Class III), except where a central cause is the diagnosis (the anti-Hu
  brainstem encephalitis mimic: required).
- `analyze_csf`: waste, except optional in the paraneoplastic mimic [Graus_2021].
- `order_ct_scan` (head): waste unless NICE NG232 criteria are met: CT within 1 h for GCS below 15,
  suspected skull fracture, two or more vomits, post-traumatic seizure or focal deficit; within 8 h
  for anticoagulation (not antiplatelet monotherapy) or age 65 or over with loss of consciousness or
  amnesia; then recommended as a head-injury study, not part of the syncope diagnosis [NICE_NG232].
- `order_specialized_test` `tilt_table`: waste once the mechanism is arrhythmic or structural.
- `order_specialized_test` `exercise_stress_test`: waste in CHB or Mobitz II with a pacing indication
  already established, and before rate control in 1:1 flutter.
- `interpret_labs` `D_dimer` at high PE probability (straight to CTPA) [ESC_2019_PE]; untargeted panels.

A wasted tilt or exercise order is answered by the case's own report (no isoproterenol, the
patient's own rates) or a "not performed" report, never by the library normal (HR 68, 10.4 METs).

## 4. Tools that are HARMFUL / contraindicated

- `tilt_table`: harm in severe AS, obstructive HCM and RV outflow obstruction. Never isoproterenol
  provocation in ischaemic heart disease, AS or HCM.
- `exercise_stress_test`: harm in symptomatic severe AS [ESC_EACTS_2025_VHD], an obstructing RV
  outflow mass, recurrent pause-dependent torsades, and acute PE with RV dysfunction [Fletcher_2013].

## 5. Treatment statements (musts and prohibitions; no treatment tool)

Every case keeps the definitive therapy, a disposition (admission with monitoring, or outpatient)
and driving advice [ESC_2018]: Group 1 no driving until treated; 1 week after a pacemaker; 3 months
after an ICD for secondary prevention.

- **AV block (ESC 2021):** permanent pacing is Class I for Mobitz II, high-grade or third-degree AV
  block without a reversible cause, symptomatic or not; withdraw rate-slowing drugs first, but pacing
  stays indicated when the block persists. ICD or CRT-D rather than a pacemaker when LVEF is 35% or
  lower, a laminopathy is likely or sarcoid has a VA substrate; CRT rather than RV pacing when LVEF is
  40% or lower with a high expected pacing burden (IIa) [ESC_2021_Pacing]. Bridge with transcutaneous
  or temporary transvenous pacing; beta-agonists only with a low likelihood of coronary ischaemia
  [ACC_AHA_HRS_2018_Bradycardia].
- **Sick sinus syndrome:** pacing Class I for symptomatic SND or tachy-brady syndrome; stop
  non-essential rate-slowing drugs; anticoagulation by CHA2DS2-VA when AF or flutter is documented
  [ESC_2021_Pacing] [ESC_2024_AF].
- **Drug-induced torsades:** stop every QT-prolonging drug; IV magnesium sulfate 2 g even with a
  normal Mg; potassium to 4.5-5.0 mmol/L; temporary pacing (or isoproterenol, only without ischaemia)
  for recurrent pause-dependent torsades; telemetry until QTc below 500 ms; CredibleMeds list
  [Drew_2010] [ESC_2022_VA_SCD].
- **Congenital LQTS:** nadolol or propranolol (Class I); avoid QT-prolonging drugs; correct K and Mg
  during illness; ICD not first-line (after cardiac arrest, or syncope despite an adequate
  beta-blocker); genetic testing and cascade screening (Class I) [ESC_2022_VA_SCD].
- **Brugada syndrome:** treat fever promptly; ICD IIa for a type 1 pattern with arrhythmic syncope; no
  drug challenge after a documented type 1 pattern; avoid brugadadrugs.org drugs [Postema_2009];
  quinidine an option [ESC_2022_VA_SCD].
- **CPVT:** nadolol at the maximal tolerated dose; restriction of competitive sport and strenuous
  exercise; flecainide for breakthrough events; ICD added after arrest or recurrence despite
  therapy, never as sole therapy; LCSD an option [ESC_2022_VA_SCD].
- **ARVC:** ICD Class I after poorly tolerated sustained VT, IIa after arrhythmic syncope (and for
  NSVT with syncope); beta-blocker; exercise restriction; genetic counselling and cascade screening
  [ESC_2022_VA_SCD] [ARVC_TFC_2010].
- **Obstructive HCM:** stop arterial and venous vasodilators (dihydropyridines, ACE inhibitors and
  ARBs, nitrates); non-vasodilating beta-blocker first-line, verapamil or diltiazem the alternative;
  HCM Risk-SCD with unexplained syncope and NSVT entering the ICD decision; avoid dehydration
  [ESC_2023_Cardiomyopathy] [OMahony_2014].
- **Severe AS:** symptomatic severe AS (syncope included) is Class I for intervention after a Heart
  Team decision; TAVI is favoured from 70 years in tricuspid AS when transfemoral access is feasible
  (ESC/EACTS 2025; the 2021 threshold was 75); vasodilators with caution [ESC_EACTS_2025_VHD].
- **WPW with syncope:** EP study for risk stratification and accessory-pathway ablation (Class I); no
  AV-nodal blockers in pre-excited AF; synchronised cardioversion if unstable, IV procainamide or
  ibutilide if stable [ESC_2019_SVT].
- **AVNRT:** modified Valsalva manoeuvre then adenosine [REVERT_2015]; slow-pathway ablation Class I
  for recurrent symptomatic AVNRT; confirm absence of pre-excitation before AV-nodal blockers
  [ESC_2019_SVT].
- **Atrial flutter:** no class IC drug without AV-nodal blockade (1:1 conduction); CTI ablation;
  anticoagulation by CHA2DS2-VA (never CHA2DS2-VASc) [ESC_2024_AF] [ESC_2019_SVT].
- **Acute PE:** high clinical probability goes straight to CTPA (no D-dimer); syncope with RV
  dysfunction and a positive troponin is intermediate-high risk; LMWH (UFH when reperfusion may be
  needed or CrCl below 30 mL/min); monitoring with rescue reperfusion on deterioration, choosing
  catheter-directed or surgical treatment when fibrinolysis is contraindicated (major surgery within
  3 weeks) [ESC_2019_PE].
- **Cardiac sarcoid:** tissue from the most accessible site (EBUS-TBNA of hilar nodes); a device with
  ICD capability when a pacing indication exists (IIa); immunosuppression; repeat FDG-PET for
  response [HRS_2014_Sarcoid] [ATS_2020_Sarcoid].
- **Cardiac myxoma:** urgent surgical excision with histology; anticoagulation does not substitute.
- **Rheumatic carditis with AV block:** temporary pacing while carditis is treated, permanent pacing if
  the block persists; benzathine penicillin G secondary prophylaxis [Gewitz_2015] [ESC_2021_Pacing].
- **Anti-Hu brainstem encephalitis (mimic):** tumour search and tissue diagnosis with oncology
  referral; immunotherapy (IV methylprednisolone, then IVIG or plasma exchange); ventilatory support
  for central apnoea, pacing if asystole persists [Graus_2021].

## 6. Sequence constraints and stop rule

- `analyze_ecg` before `order_echocardiogram` and before `order_cardiac_monitoring` (`soft`): the
  12-lead ECG sets the risk tier that selects the monitor and the urgency of imaging [ESC_2018].
- TTE before any `exercise_stress_test` or `exercise_echo` criterion (`hard`): exertional syncope
  requires severe AS and obstructive HCM to be excluded first [ESC_2018] [ESC_2023_Cardiomyopathy]
  [ESC_EACTS_2025_VHD].
- Case-specific soft constraints: ECG before the drug check in drug-induced torsades; pregnancy test
  before CTPA in a premenopausal woman [ESC_2019_PE]; cardiac FDG-PET before the nodal biopsy
  [HRS_2014_Sarcoid].
- **No labs-before-monitoring constraint, soft or hard:** immediate monitoring of a high-risk patient
  is Class I and must never wait for blood results.
- Stop rule: `required_before_assessment` lists every `required` criterion and nothing else;
  `max_additional_actions` 2 for M and S cases, 3 for P and R cases.

## 7. Subtype variations (tiers applied in the round)

| Subtype | Required | Recommended | Optional | Avoided |
| --- | --- | --- | --- | --- |
| AV block, degenerative, 60 or over | ECG, TTE, monitoring | BMP (required with Mg when a diuretic or QT is in play), drug check | CMR, literature | EEG, MRI, CSF, tilt, exercise; head CT unless NG232 |
| AV block before 60 or with a cause to find | ECG, TTE, monitoring, the cause-finding test | CMR, drug check | literature | as above |
| Severe AS | ECG, TTE, monitoring | BMP, drug check | literature | tilt and exercise (harm), EEG, MRI |
| Drug-induced torsades | ECG, BMP and Mg, drug check, telemetry, TTE | - | EEG, literature | MRI, CSF, tilt, exercise (harm) |
| Congenital LQTS | ECG, TTE, monitoring | drug check, BMP | exercise test, EEG, literature | MRI, CSF, tilt |
| Brugada | ECG, monitoring | TTE, BMP, CMR | drug check, literature | tilt, exercise, MRI, EEG |
| CPVT | ECG, TTE, monitoring, exercise test | CMR, BMP | drug check, literature | tilt, MRI, EEG |
| ARVC | ECG, TTE, monitoring, CMR | exercise test, drug check | literature | tilt, MRI, EEG |
| Obstructive HCM | ECG, TTE, monitoring, CMR, exercise echo, drug check | BMP | literature | tilt (harm), MRI, EEG |
| SVT, WPW, flutter | ECG, TTE, monitoring | BMP, drug check | exercise, CMR, literature | tilt, MRI, EEG |
| VT in ischaemic cardiomyopathy | ECG, BMP and Mg, telemetry, TTE, drug check | - | literature | tilt, exercise, MRI, EEG |
| Sick sinus syndrome | ECG, TTE, monitoring, drug check | BMP (TSH accepted) | literature | tilt, MRI, EEG |
| Acute PE | ECG, troponin, BNP and beta-hCG, TTE, CTPA, telemetry, drug check | - | venous duplex, literature | D-dimer, MRI, EEG, tilt, exercise (harm) |
| RV outflow myxoma | ECG, TTE, monitoring, CMR | BMP | drug check, literature | tilt and exercise (harm), MRI, EEG |
| Neurological mimic (anti-Hu) | ECG, paraneoplastic panel, brain MRI, TTE, monitoring, polysomnography, chest CT tumour search | - | CSF, drug check, literature | EEG, tilt |

R (reverse / mimic) cases keep a cardiac or neurological mechanism that the agent must not miss
(convulsive syncope labelled epilepsy, anti-Hu brainstem encephalitis, postpartum ARVC labelled
eclampsia); vasovagal and orthostatic syncope are differentials, not case labels, and orthostatic
hypotension is diagnosed by active standing (a sustained fall of 20 mmHg systolic or 10 mmHg
diastolic within 3 min), not by tilt.

## 8. Red herrings and pitfalls

- **Convulsive activity:** brief jerks with rapid recovery are convulsive syncope; an antiseizure
  drug started for it is reviewed and withdrawn once the arrhythmia is found.
- **Normal ECG or a negative 24 h Holter:** does not exclude a paroxysmal arrhythmia; choose the
  monitor by event frequency.
- **"Just vasovagal" in an older adult:** a first syncope without prodrome needs the cardiac work-up.
- **Positive tilt:** supports a reflex contribution but does not exclude a concurrent cardiac cause.
- **Exertional syncope:** red flag; echo first, exercise testing only after the TTE has excluded
  severe AS and obstructive HCM.
- **Imaging the wrong organ:** after a non-diagnostic echo the escalation is cardiac MRI, not brain
  MRI or head CT; a treadmill test is not an exercise echocardiogram; a normal ACE does not exclude
  sarcoidosis.
- **Template carry-over:** never copy a number from a sibling case; sex-specific reference ranges.

## 9. Diagnosis labels (scoring)

The accepted labels come from `agent-platform/config/policies/diagnosis_synonyms.yaml`
(SYNC-CARD block, 24 Oct 2026). No generic "cardiac syncope", "arrhythmic syncope",
"bradyarrhythmia" or "tachyarrhythmia" label and no R55: an answer must name the mechanism or the
substrate. AV block grades do not grant each other; congenital and drug-induced LQTS do not grant
each other; SVT and VT are separate; ARVC, CPVT, sarcoid, rheumatic carditis and anti-Hu brainstem
encephalitis must be named where they are the cause.

## 10. Allowed citations

Verified on 24 Oct 2026.

- `[ESC_2018]` — Brignole M et al. 2018 ESC Guidelines for the diagnosis and management of syncope. Eur Heart J 2018;39:1883-1948
- `[ACC_AHA_HRS_2017]` — Shen WK et al. 2017 ACC/AHA/HRS guideline for the evaluation and management of patients with syncope. J Am Coll Cardiol 2017;70:e39-e110; Circulation 2017;136:e60-e122
- `[EGSYS_2008]` — Del Rosso A et al. Clinical predictors of cardiac syncope at initial evaluation in patients referred urgently to a general hospital: the EGSYS score. Heart 2008;94:1620-1626
- `[ROSE_2010]` — Reed MJ et al. The ROSE (Risk Stratification of Syncope in the Emergency Department) study. J Am Coll Cardiol 2010;55:713-721
- `[Strickberger_2006]` — Strickberger SA et al. AHA/ACCF Scientific Statement on the Evaluation of Syncope. Circulation 2006;113:316-327
- `[Locati_2016]` — Locati ET, Moya A, Oliveira M, et al. External prolonged electrocardiogram monitoring in unexplained syncope and palpitations: results of the SYNARR-Flash study. Europace 2016;18:1265-1272
- `[ESC_2021_Pacing]` — Glikson M et al. 2021 ESC Guidelines on cardiac pacing and cardiac resynchronization therapy. Eur Heart J 2021;42:3427-3520
- `[ACC_AHA_HRS_2018_Bradycardia]` — Kusumoto FM et al. 2018 ACC/AHA/HRS guideline on the evaluation and management of patients with bradycardia and cardiac conduction delay. Circulation 2019;140:e382-e482
- `[ESC_2022_VA_SCD]` — Zeppenfeld K et al. 2022 ESC Guidelines for the management of patients with ventricular arrhythmias and the prevention of sudden cardiac death. Eur Heart J 2022;43:3997-4126
- `[ESC_2023_Cardiomyopathy]` — Arbelo E et al. 2023 ESC Guidelines for the management of cardiomyopathies. Eur Heart J 2023;44:3503-3626
- `[ESC_2019_SVT]` — Brugada J et al. 2019 ESC Guidelines for the management of patients with supraventricular tachycardia. Eur Heart J 2020;41:655-720
- `[ESC_2019_PE]` — Konstantinides SV et al. 2019 ESC Guidelines for the diagnosis and management of acute pulmonary embolism. Eur Heart J 2020;41:543-603
- `[ESC_EACTS_2025_VHD]` — Praz F, Borger MA et al. 2025 ESC/EACTS Guidelines for the management of valvular heart disease. Eur Heart J 2025;46:4635-4736 (doi:10.1093/eurheartj/ehaf194; also Eur J Cardiothorac Surg, doi:10.1093/ejcts/ezaf276)
- `[ESC_2024_AF]` — Van Gelder IC et al. 2024 ESC Guidelines for the management of atrial fibrillation. Eur Heart J 2024;45:3314-3414
- `[ARVC_TFC_2010]` — Marcus FI et al. Diagnosis of arrhythmogenic right ventricular cardiomyopathy/dysplasia: proposed modification of the Task Force Criteria. Circulation 2010;121:1533-1541
- `[HRS_2014_Sarcoid]` — Birnie DH et al. HRS expert consensus statement on the diagnosis and management of arrhythmias associated with cardiac sarcoidosis. Heart Rhythm 2014;11:1305-1323 (there is no "HRS 2017" sarcoid consensus)
- `[ATS_2020_Sarcoid]` — Crouser ED et al. Diagnosis and detection of sarcoidosis: an official ATS clinical practice guideline. Am J Respir Crit Care Med 2020;201:e26-e51
- `[OMahony_2014]` — O'Mahony C et al. A novel clinical risk prediction model for sudden cardiac death in hypertrophic cardiomyopathy (HCM Risk-SCD). Eur Heart J 2014;35:2010-2020
- `[Drew_2010]` — Drew BJ et al. Prevention of torsade de pointes in hospital settings: AHA/ACCF scientific statement. Circulation 2010;121:1047-1060
- `[Gewitz_2015]` — Gewitz MH et al. Revision of the Jones criteria for the diagnosis of acute rheumatic fever in the era of Doppler echocardiography: AHA scientific statement. Circulation 2015;131:1806-1818
- `[Graus_2021]` — Graus F et al. Updated diagnostic criteria for paraneoplastic neurologic syndromes. Neurol Neuroimmunol Neuroinflamm 2021;8:e1014
- `[NICE_NG232]` — NICE guideline NG232. Head injury: assessment and early management. May 2023
- `[Fletcher_2013]` — Fletcher GF et al. Exercise standards for testing and training: AHA scientific statement. Circulation 2013;128:873-934
- `[REVERT_2015]` — Appelboam A et al. Postural modification to the standard Valsalva manoeuvre for emergency treatment of supraventricular tachycardias (REVERT). Lancet 2015;386:1747-1753
- `[Postema_2009]` — Postema PG et al. Drugs and Brugada syndrome patients: review of the literature, recommendations, and an up-to-date website (www.brugadadrugs.org). Heart Rhythm 2009;6:1335-1341

Named resources (cited by name in text, no key): CredibleMeds QTdrugs list; LactMed (NLM).

**Superseded (do not cite; kept for traceability):**
- `[Locati_2014]` — the key named a "Heart 2016;102:1772-1778" reference that could not be verified;
  the study is SYNARR-Flash, Europace 2016. Replaced by `[Locati_2016]` (SYNC-CARD-M05, 24 Oct 2026).
- Vahanian A et al. 2021 ESC/EACTS valvular guidelines (Eur Heart J 2022;43:561-632), never a key:
  superseded by `[ESC_EACTS_2025_VHD]` (TAVI threshold 75 -> 70 years in tricuspid AS); text in
  M03, P01, P02, P04, RP01, RP03, RS04, S02, S04, S05 updated 24 Oct 2026.
