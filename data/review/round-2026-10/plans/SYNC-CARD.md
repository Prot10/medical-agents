# SYNC-CARD round plan (October 2026)

Lead plan for the 30 SYNC-CARD cases (M01-M05, P01-P04, RM01-RM04, RP01-RP05, RS01-RS06,
S01-S06). Workers apply it to six cases each. Where this plan names a decision, apply it as
written. Where it gives a rule, apply the rule and the same defect gets the same fix in every
case. There are no reviewer notes for this condition: every log's Reviewer notes section reads
"No reviewer notes for this case".

Baseline on 24 Oct 2026, before any edit:
- `bin/perfect_agent.py` passes 30/30.
- The leak guard in `tests/test_case_guards.py` fails 10 cases (M01, M02, M03, M04, P02, P03,
  S01, S02, S03, S05). In each, an initial literature or drug output repeats the expected_evidence.
- Every stop rule has `max_additional_actions: 0`.
- In every criterion of all 30 cases, `label` equals `rationale`.

Done means all of the following hold after the edits:
- perfect_agent is clean and the leak guard passes.
- `apply_diagnosis_synonyms.py --check` passes.
- No string listed in section 2 H remains.

## 1. Governing guidelines and canonical facts

### Citation keys

Use only these keys in `citations` arrays:

| Key | Source |
| --- | --- |
| [ESC_2018] | Brignole M et al., 2018 ESC Guidelines for the diagnosis and management of syncope. Eur Heart J 2018;39:1883-1948 |
| [ACC_AHA_HRS_2017] | Shen WK et al., 2017 ACC/AHA/HRS syncope guideline. Circulation 2017;136:e60-e122 |
| [EGSYS_2008] | Del Rosso A et al., EGSYS score. Heart 2008;94:1620-1626 |
| [ROSE_2010] | Reed MJ et al., ROSE rule. J Am Coll Cardiol 2010;55:713-721 |
| [Strickberger_2006] | Strickberger SA et al., AHA/ACCF scientific statement on syncope. Circulation 2006;113:316-327 |
| [Locati_2014] | Keep it only where it is already cited; its reference is under verification (CENTRAL C5) |

Every other guideline is cited by name in rationale or reason text, never as a new key. New keys
are requested in CENTRAL C4.

### Guidelines cited in rationale text

Use these exact references:
- ESC 2021 pacing: Glikson M et al., Eur Heart J 2021;42:3427-3520.
- ACC/AHA/HRS 2018 bradycardia: Kusumoto FM et al., Circulation 2019;140:e382-e482.
- ESC 2022 ventricular arrhythmias and sudden cardiac death: Zeppenfeld K et al., Eur Heart J
  2022;43:3997-4126.
- ESC 2023 cardiomyopathies: Arbelo E et al., Eur Heart J 2023;44:3503-3626.
- ESC 2019 SVT: Brugada J et al., Eur Heart J 2020;41:655-720.
- ESC 2019 acute PE: Konstantinides SV et al., Eur Heart J 2020;41:543-603.
- ESC/EACTS 2021 valvular heart disease: Vahanian A et al., Eur Heart J 2022;43:561-632.
- ESC 2024 AF: Van Gelder IC et al., Eur Heart J 2024;45:3314-3414. Use CHA2DS2-VA, never
  CHA2DS2-VASc.
- 2010 ARVC Task Force Criteria: Marcus FI et al., Circulation 2010;121:1533-1541.
- HRS 2014 cardiac sarcoidosis consensus: Birnie DH et al., Heart Rhythm 2014;11:1305-1323.
  There is no "HRS 2017" sarcoid consensus.
- HCM Risk-SCD: O'Mahony C et al., Eur Heart J 2014;35:2010-2020.
- Drug-induced QT and torsades: Drew BJ et al., AHA/ACCF scientific statement, Circulation
  2010;121:1047-1060.
- Jones criteria revision: Gewitz MH et al., Circulation 2015;131:1806-1818.
- Paraneoplastic neurological syndromes: Graus F et al., Neurol Neuroimmunol Neuroinflamm
  2021;8:e1014.
- Head injury: NICE NG232 (2023).
- Exercise testing standards: Fletcher GF et al., Circulation 2013;128:873-934.
- Other references:
  - REVERT: Appelboam A et al., Lancet 2015;386:1747-1753.
  - brugadadrugs.org: Postema PG et al., Heart Rhythm 2009;6:1335-1341.
  - CredibleMeds QTdrugs list.
  - LactMed (NLM).

### Canonical facts

Workers write rationale text from these and do not invent others.

- **Initial evaluation (ESC 2018).** History, examination, supine and standing BP and a 12-lead
  ECG.
  - High-risk features call for early in-hospital evaluation and immediate ECG monitoring (bedside
    or telemetry; Class I). They are:
    - syncope during exertion or supine;
    - palpitations before the event;
    - known structural or coronary heart disease;
    - family history of sudden death under 40;
    - an ECG showing Mobitz II, complete heart block (CHB), bifascicular block, QTc above 460 ms,
      a Brugada type 1 pattern, pre-excitation, NSVT or epsilon waves.
  - Echocardiography is Class I when structural heart disease is known or suspected.
  - Holter is Class IIa when symptoms are frequent (daily or near-daily).
  - An external loop or event recorder is IIa for events within a 4-week window.
  - The ILR is Class I for recurrent unexplained syncope with infrequent events.
  - EEG, brain MRI or CT, carotid ultrasound and routine labs are not recommended without a
    specific indication (Class III).
- **Labs (ESC 2018).** Targeted, not routine:
  - Hb or haematocrit when bleeding is suspected.
  - Electrolytes (BMP) and magnesium when an arrhythmia or QT prolongation may be electrolyte
    driven.
  - Troponin and BNP when ischaemia, PE or heart failure is in question.
  - D-dimer only when the clinical probability of PE is low or intermediate.
- **Pacing (ESC 2021).** Permanent pacing is Class I for Mobitz II, high-grade or third-degree AV
  block, symptomatic or not, when no reversible cause is present.
  - Withdraw rate-slowing drugs first when they may contribute. AV block often persists after the
    drug is withdrawn, and in that case pacing is still indicated.
  - When AV block appears in a patient under 60 with no clear cause, cardiac MRI (or FDG-PET when
    sarcoid is suspected) is IIa to look for sarcoidosis, myocarditis or a laminopathy.
  - Consider an ICD or CRT-D rather than a pacemaker when LVEF is 35% or lower, a laminopathy is
    likely, or sarcoid has a ventricular arrhythmia substrate.
  - CRT is preferred to RV pacing when LVEF is 40% or lower and a high RV pacing burden is
    expected (ESC 2021 IIa).
- **Torsades de pointes (Drew 2010; ESC 2022).**
  - Stop every QT-prolonging drug.
  - Give IV magnesium sulfate 2 g, even when Mg is normal.
  - Replete potassium to 4.5-5.0 mmol/L.
  - Use temporary pacing or isoproterenol for pause-dependent torsades that recurs, but only
    without ischaemia.
  - Telemetry until QTc is below 500 ms.
- **Congenital LQTS (ESC 2022).** LQTS is diagnosed when QTc is 480 ms or longer, or when the
  Schwartz score exceeds 3.
  - A beta-blocker (nadolol or propranolol) is Class I.
  - Avoid QT-prolonging drugs and correct electrolytes.
  - An ICD is not first-line. It is indicated after cardiac arrest, or for syncope despite an
    adequate beta-blocker.
  - Genetic testing and cascade screening are Class I.
- **Brugada syndrome (ESC 2022).** A spontaneous or fever-induced type 1 pattern with arrhythmic
  syncope gives an ICD indication of IIa.
  - A drug challenge is not indicated once a type 1 pattern has been documented.
  - Treat fever promptly.
  - Avoid the drugs listed on brugadadrugs.org.
  - Quinidine is an option.
- **CPVT (ESC 2022).** Treatment:
  - a non-selective beta-blocker (nadolol) at the maximal tolerated dose;
  - restriction of competitive sport and strenuous exercise;
  - flecainide added for recurrent events on a beta-blocker;
  - an ICD added to medication after cardiac arrest or recurrent events despite therapy, never as
    sole therapy;
  - left cardiac sympathetic denervation as an option.
  Diagnosis rests on exercise-induced bidirectional or polymorphic ventricular ectopy with a
  structurally normal heart. Exercise testing is Class I.
- **ARVC (2010 Task Force; ESC 2022).**
  - An ICD is Class I after haemodynamically poorly tolerated sustained VT.
  - An ICD is IIa after arrhythmic syncope, and should be considered for NSVT with syncope.
  - Give a beta-blocker and restrict exercise.
  - Cardiac MRI is the key imaging test.
- **HCM (ESC 2023).**
  - Exercise echo is Class I when the LVOT gradient is below 50 mmHg at rest and on Valsalva in a
    symptomatic patient.
  - In obstructive HCM, stop arterial and venous vasodilators (dihydropyridines, ACE inhibitors
    and ARBs, nitrates).
  - A non-vasodilating beta-blocker is first-line, and verapamil or diltiazem is the alternative.
  - Assess sudden cardiac death risk with HCM Risk-SCD.
  - Unexplained syncope is a risk factor that enters the ICD decision.
- **Severe aortic stenosis (ESC/EACTS 2021).** Severe AS is AVA below 1.0 cm2, mean gradient 40
  mmHg or higher, or Vmax 4 m/s or higher.
  - Symptomatic severe AS (syncope included) is Class I for intervention after a Heart Team
    decision.
  - TAVI is favoured at 75 years or older.
  - Exercise testing is contraindicated in symptomatic severe AS.
  - Vasodilators are used with caution.
- **WPW with syncope (ESC 2019 SVT).**
  - An EP study is Class I for risk stratification, followed by catheter ablation (Class I).
  - In pre-excited AF, AV-nodal blockers (adenosine, verapamil, diltiazem, digoxin,
    beta-blockers) are contraindicated (Class III).
- **AVNRT (ESC 2019 SVT).**
  - Vagal manoeuvres, with the modified Valsalva manoeuvre (REVERT), then adenosine.
  - Slow-pathway ablation is Class I for recurrent symptomatic AVNRT.
- **Atrial flutter (ESC 2024 AF; ESC 2019 SVT).**
  - Do not give class IC drugs without AV-nodal blockade, because of the risk of 1:1 conduction.
  - CTI ablation is Class I after a first symptomatic episode, or IIa as first-line therapy.
  - Anticoagulation follows CHA2DS2-VA, as for AF.
- **Acute PE (ESC 2019).**
  - With high clinical probability, go straight to CTPA; D-dimer is not used.
  - Syncope with RV dysfunction and a positive troponin is intermediate-high risk.
  - Anticoagulate with LMWH (UFH when reperfusion may be needed or CrCl is below 30 mL/min).
  - Monitor, and give rescue thrombolysis if the patient deteriorates.
- **Sick sinus syndrome (ESC 2021).** Pacing is Class I for symptomatic SND or tachy-brady
  syndrome.
  - Rate-control drugs then become usable for the tachy component.
  - Stop non-essential rate-slowing drugs.
- **Head injury after syncope (NICE NG232).** A head CT within 1 h is indicated for GCS below
  15, suspected skull fracture, vomiting twice or more, post-traumatic seizure, or a focal deficit.
  - A CT within 8 h is indicated for anticoagulated patients (antiplatelet monotherapy is not
    enough), or for age 65 and over with loss of consciousness or amnesia.
  - Otherwise head CT is waste.
- **Cardiac sarcoid (HRS 2014).**
  - Diagnosis is histological (myocardial or extracardiac) plus an imaging pattern consistent with
    cardiac sarcoid.
  - AV block warrants a device; an ICD is preferred when a pacing indication exists (IIa).
  - Give immunosuppression.
  - Tissue is obtained from the most accessible site (EBUS-TBNA of hilar nodes).

### Tool vocabulary facts

These come from costs.yaml and limit what a criterion can ask for.

- **Not in the vocabulary.** There is no electrophysiology study, no sodium-channel-blocker
  (ajmaline) challenge, no cardiac genetic panel and no active stand or orthostatic BP. CENTRAL C2
  requests them. Until they exist:
  - Never make them criteria.
  - Never store them under another tool (interpret_labs, analyze_ecg).
  - Write them into the assessment musts.
- **analyze_ecg.** It takes only `clinical_context`. A repeat ECG cannot be targeted, so no case
  keeps a "repeat ECG" follow-up.
- **check_drug_interactions.** It requires `drug`.
- **Monitoring and echo types.**
  - Monitoring types are holter_24h, holter_48h, event_monitor_14d, event_monitor_30d, telemetry
    and implantable_loop_recorder. "Continuous telemetry" is not a value.
  - Echo types are TTE, TEE, bubble_study and exercise_echo.
  - Schema defaults are filled before matching: echo_type TTE, monitor_type holter_24h.
- **Library fallback answers.** These come back for any order a case does not store:
  - cardiac monitoring: a normal recording;
  - tilt: normal, HR 68;
  - drug check: "No interaction identified".
  All three contradict a bradyarrhythmia case. Every case therefore stores its own
  `fallback_tool_outputs.cardiac_monitoring`, consistent with the patient (see 2 E).

## 2. Error classes

Each class gives the description, the cases, the decided fix and, where useful, canonical text.

### A. Literature search scored as work-up (all 30)

**Description.**
- search_medical_literature is required or recommended in all 30 cases, and is in most stop rules.
- Initial literature outputs copy the expected_evidence. This is what trips the leak guard.
- Several cite invented or wrong references: RM01 "Matsumoto 2023", "Saiz 2020" and Dalmau
  claims; P01 "2020 Revised Task Force Criteria" and Sheldon/Rose; the P03 Antzelevitch title.
- The case-level fallback literature answers "Not retrieved on this pathway", or "No directly
  applicable ... evidence" followed by a recommendation.

**Fix.**
1. Set the literature criterion to `optional` and remove it from `stop_rule.required_before_assessment`.
2. Delete every `initial_tool_outputs.literature_search` block.
3. Keep at most two literature follow-ups, placed last in followup_outputs.
   - Each answers a real query with real guideline content only, from section 1.
   - None states a conclusion about this patient.
   - None contains any 60-character window of an expected_evidence.
4. Delete `fallback_tool_outputs.literature_search` wherever it is the "Not retrieved" or
   "no directly applicable" text; the library answers instead.

**Canonical rationale.** "Guideline lookup is optional; the decision rests on the ECG, monitoring
and imaging results already obtained (ESC 2018)."

### B. Drug interaction check (all 30)

**Description.**
- Initial drug outputs repeat the key.
- The "general" blocks are empty templates.
- Their text includes "(agent not specified on this case's pathway)" and "No new antiarrhythmic
  drug initiated on this pathway".
- Pinned `current_medications` appear in RP04 and S06.

**Fix.**
1. Delete `initial_tool_outputs.drug_interactions`.
2. Set the criterion's alternatives to one `{drug: <name>}` per plausible drug, as in the tier
   table below. Drop every `current_medications` pin.
3. Store one follow-up per named drug. Each reviews that drug against the patient's actual
   medication list, written in report voice.
4. Where a concrete interaction exists, set `fallback_tool_outputs.drug_interactions` to the same
   medication-list review. This keeps an unnamed drug from receiving the library's "No interaction
   identified".
5. Delete the empty "general" blocks.

Tiers (decided):

| Tier | Cases and drug(s) to accept |
| --- | --- |
| required | M04: azithromycin, ondansetron, citalopram (QT triple; diagnostic, placed straight after the ECG) |
| required | S06: diltiazem, metoprolol |
| required | P02: amlodipine, losartan (vasodilators in obstructive HCM) |
| required | RM02: chloroquine (conduction toxicity) |
| required | RP04: lamotrigine, levetiracetam (sodium-channel effect of lamotrigine) |
| required | RM04: aspirin plus the chosen anticoagulant (enoxaparin, heparin, apixaban, rivaroxaban) |
| required | RS05: the two beta-blockers in the medication list |
| required | RP05: the vitamin D or calcium supplement in the medication list, but only if the case's calcium is high; otherwise recommended |
| recommended | M01, M02, M03, M05, P01, P04, RP01, RS01, RS02, RS03, RM03, S01, S03, S05, RS06 (rate-slowing or QT-active drug in the list, or a planned new drug) |
| optional | P03, RM01, RP02, RP03, RS04, S02, S04 |

For recommended cases, accept the rate-slowing or QT-active drug in the list. If the list has
none, accept the drug the musts plan to start (for example a beta-blocker in RP01).

### C. Laboratory panels (all 30)

**Description.**
- required_arguments pin CBC+BMP+Mg+troponin almost everywhere, whether or not an assay drives a
  decision.
- beta-hCG is pinned in women over 55 (M04, a 60-year-old woman).
- D-dimer is pinned in high-probability PE (RM04).
- ANA and RF are pinned in sarcoid (RP05).

**Fix.** required_arguments list only the assays that change management.

| Case | Tier | required_arguments `panels` |
| --- | --- | --- |
| M01, M03 | required | BMP, magnesium |
| M04 | required | BMP, magnesium |
| RS05 | required | BMP, magnesium |
| M02 | recommended (K 4.3, Mg 1.8 normal) | BMP |
| RM01 | required | paraneoplastic_panel |
| RM02 | required | ESR, CRP, ASO |
| RM04 | required | troponin, BNP (D_dimer removed) |
| RP01 | required | BMP, magnesium, urinalysis |
| RP05 | required | calcium, ACE |
| RP04 | recommended | AED_levels |
| All other cases | recommended | BMP |

Further rules:
- **TSH.** May be accepted as an extra only in M04, M05, S06 and RS06.
- **beta-hCG.** It appears in required_arguments only in RM04, where pregnancy changes the CTPA
  decision. Never pin it for a woman aged 55 or over.
- **Data errors to fix.**
  - M01: Hb 12.8 with Hct 44.5 is impossible. Set Hct to 38.4.
  - M02: the levetiracetam level is reported, and the HPI says it was started 3 days ago, but the
    medication list lacks it. Add "Levetiracetam 500 mg twice daily (started 3 days ago)".

### D. Sequence constraints and stop rule (all 30)

**Description.**
- A hard constraint labs before monitoring is present in M01, M02, M03, M04, RM02, RM04, RP01,
  RP04, RP05 and RS05. Delaying monitoring for blood results is the unsafe order: ESC 2018 makes
  immediate in-hospital monitoring Class I.
- Stop rules list only some criteria and have `max_additional_actions: 0`.

**Fix.**
1. Delete every labs before monitoring constraint.
2. Add soft constraints ECG before echo, and ECG before monitoring.
   - Canonical reason: "The 12-lead ECG sets the risk tier that selects the monitor and the urgency
     of imaging (ESC 2018)."
3. Add a hard constraint TTE before any exercise_stress_test or exercise_echo criterion.
   - Canonical reason: "Exertional syncope requires severe aortic stenosis and obstructive HCM to
     be excluded on echocardiography before exercise testing (ESC 2018; ESC 2023; ESC/EACTS
     2021)."
4. Per-case changes:
   - RM04: the hard ECG before CTPA constraint becomes soft.
   - RP05: add soft FDG-PET before biopsy.
   - P02: add hard TTE before exercise_echo.
5. Stop rule.
   - `required_before_assessment` lists every `required` criterion and nothing else.
   - `max_additional_actions` is 2 for M and S cases and 3 for P and R cases.

### E. Monitoring modality mismatch (about 20 cases)

**Description.**
- The criterion pins `holter_24h` while the label says telemetry. Outputs mismatch too:
  - M01 stores a 48 h Holter;
  - M03 and S06 return a 48 h Holter under a telemetry trigger;
  - P03 and P04 use "Continuous telemetry", which is not an enum value.

**Fix by risk tier.**
- **High-risk ECG or history** (all CHB, Mobitz II, VT, LQTS, Brugada, ARVC, HCM, PE, flutter
  1:1, WPW and AS cases):
  - Alternatives: telemetry first, then holter_24h and holter_48h.
  - Store one follow-up whose trigger tokens include both `telemetry` and `holter`, and whose
    output names its type truthfully ("Inpatient telemetry, 36 h").
  - Set `fallback_tool_outputs.cardiac_monitoring` to the same case-consistent recording.
- **Not high risk.**
  - M05 (paroxysmal palpitations and syncope every few weeks): event_monitor_14d required,
    event_monitor_30d accepted, holter optional.
  - RP04 (five events in 2 months over 12 years): implantable_loop_recorder required
    (ESC 2018 Class I), event_monitor_30d recommended, holter_24h optional. Delete the separate
    24 h Holter required criterion, and delete the "stepwise escalation" must.
- **Data rule.** Monitoring numbers must agree with the ECG and with each other: escape rate,
  pauses, time stamps and burden.

### F. Studies stored under the wrong tool

| Case | Wrong storage | Fix |
| --- | --- | --- |
| M01 | EP study as interpret_labs follow-up | delete; write "EP study only if pacing indication were uncertain" nowhere (indication is established) |
| P03 | EP study and ajmaline test as analyze_ecg follow-ups | delete both; no drug challenge after a type 1 pattern (ESC 2022) |
| P03, P04, RP03 | genetic testing as interpret_labs follow-up | keep as the last follow-up only, never a criterion; add "genetic counselling and testing with cascade screening of first-degree relatives" to the musts |
| RM01 | polysomnography stored under interpret_labs; real order_specialized_test PSG output is a placeholder equal to the key | move the PSG data into the `order_specialized_test` polysomnography output, written as a PSG report; delete the interpret_labs copy |
| RM01 | chest CT stored under order_ct_scan | move to `order_body_imaging` study chest_CT, contrast true; add required criterion "Tumour search for anti-Hu paraneoplastic syndrome" (alternatives chest_CT, and FDG-PET whole-body via order_advanced_imaging if the modality exists, else chest_CT only) |
| RM01 | amiodarone drug follow-up | delete |

### G. Placeholder or wrong-voice reports

**Description.**
- These outputs equal the key: the P03 echo follow-up (trigger request_tte), the RM01 PSG, and
  the RM03 order_ct_scan follow-up.
- The P01 and P02 echo impressions are lab-style "Abnormal values: ...".

**Fix.** Rewrite each as a full report in its own modality's voice.
- **Echo reports** contain:
  - LVEF (method), maximal wall thickness, LV dimensions and LA diameter (or volume index);
  - valves with gradients (AVA, mean gradient and Vmax when AS is present; LVOT gradient at rest
    and on Valsalva in HCM);
  - RV size and function (TAPSE), estimated PASP, pericardium and masses;
  - and no diagnosis sentence.
- **Other rules.**
  - No PFO or bubble framing (RP04).
  - The RM03 CT output becomes a normal non-contrast head CT report, or is deleted when the head
    CT is made waste (section 4).

### H. Engineering and pipeline text in case content

Delete or rewrite these strings and patterns wherever they occur:
- "Do not call `order_specialized_test` with parameters {...}" prohibitions (P01, P02, RM02, RM03,
  RP01, RP02, RP03, RP04, RS04): delete.
- "cited via EGSYS_2008 ... see metadata.citation_gap" (RP05): delete.
- "Not retrieved on this pathway", "(agent not specified on this case's pathway)" and "No new
  antiarrhythmic drug initiated on this pathway": delete the blocks (A, B).
- Any mention of a tool name (for example "check_drug_interactions") in clinical text (M04
  literature and red herring): rewrite in clinical words ("a review of the medication list").
- Free-text section citations inside `citations` ("ESC 2018 §3.2", 30 of them) and the duplicate
  "Locati 2014": delete; keep the keys.
- `rationale` equal to `label` (every criterion): write a real rationale of one or two sentences
  that says why this test, here, changes management, and names the guideline.
- "CHA2DS2-VASc": replace with CHA2DS2-VA (RS06).

### I. Boilerplate musts and prohibitions

- **Delete these prohibitions.**
  - "Do not perform lumbar puncture" in M01-M04 (no one proposes it).
  - "Hold AV-nodal blockers" where the patient takes none (S02, S04).
- **Musts that restate a scored test.** Rewrite them as a management or disposition must, or
  delete them:
  - P01, P02, RP01: CMR.
  - RM01: MRI, PSG and antibody.
  - M05: ECG and monitoring.
  - P04: exercise test.
  - S05: echo, and "recognise BNP".
  - S04: head CT.
  - RS05: serial troponin.
  - S06: Holter.
- **Tests stay tests.** A tilt or exercise test that should not be done is an avoided action
  (J), not a prohibited recommendation. The only exception is when the prohibition is phrased as
  management, for example "Do not discharge before pacing".
- **Every case keeps at least these musts.**
  - The definitive therapy.
  - A disposition (admission with monitoring, or outpatient).
  - Driving advice: an ESC 2018 driving restriction until treated (Group 1: after pacing, 1 week;
    after an ICD for secondary prevention, 3 months).

### J. Avoided actions (rules)

| Action | Rule |
| --- | --- |
| analyze_eeg | waste in every case without an EEG criterion (ESC 2018 Class III). M04 and P04 keep EEG optional (prior seizure label); RP04 waste (12 years of normal EEGs in history) |
| analyze_brain_mri | waste everywhere except RM01 (required) |
| order_ct_scan (head) | waste unless NICE NG232 criteria met: S04 (82, LOC, head strike) recommended; RM03 (58, aspirin only) waste; RP03 waste unless the HPI documents a head injury meeting NG232 |
| analyze_csf | waste everywhere except RM01, where CSF is optional (paraneoplastic work-up, Graus 2021) with a case-consistent output (mild lymphocytic pleocytosis, raised protein, oligoclonal bands) |
| tilt_table | harm in severe AS (S02, S04, S05), obstructive HCM (P02) and RVOT obstruction (RP02); waste in every other case (diagnosis established; RS01 tilt criterion deleted and made waste) |
| exercise_stress_test | harm in symptomatic severe AS (S02, S04, S05) and in RP02 (exertional syncope with RVOT mass); waste in every CHB or Mobitz II case with a pacing indication (M01-M03, RM02, RM03, RP04, RP05, RS01-RS03, S01, S03) |

Further rules:
- **Tilt follow-ups.** Where a case keeps one, it must be consistent with the patient. Never add
  isoproterenol in ischaemic heart disease, AS or HCM; the current isoproterenol tilt texts are in
  M01, M02, P01, P02, RP02, RP03 and RS04. With "harm" severity, delete the tilt follow-up
  entirely.
- **Diagnosis in the reason.** Each avoided action's reason names the patient's actual diagnosis.

### K. Differentials not updated to the pathway results

**Rule.**
- A mimic excluded by a pathway result is `low`, and its key_features name the excluding result.
- A mimic whose excluding result comes only from an off-pathway test cannot cite that result. Cite
  the ECG, monitoring or imaging that does exclude it.

**Decided downgrades to low.**
- M01: VT, and sinus node dysfunction.
- P03: LQTS (QTc 408 ms), CPVT and myocarditis.
- M05: panic disorder.
- P04: epilepsy.
- RP04: refractory epilepsy (monitoring captures asystole during a typical event).
- RP05: Lev-Lenegre disease (sarcoid on PET and biopsy).
- RS01: vasovagal syncope.
- RM01: obstructive sleep apnoea (PSG central pattern).
- RP01: eclampsia (normal BP and urine) and peripartum cardiomyopathy (normal LVEF).
- RP02: HCM and ARVC.
- RP03: LQTS.
- RS04: AF via the accessory pathway, when the monitoring shows orthodromic AVRT; keep it
  moderate if pre-excited AF is captured.
- S02, S03: VT.

**Mimics to add.**
- RM02: chloroquine cardiotoxicity, acute rheumatic carditis (Jones 2015) and malaria.
- RP03: arrhythmic mitral valve prolapse with mitral annular disjunction. Add it only if the CMR
  shows MVP or MAD; otherwise delete that finding from the CMR.
- RS01: familial conduction disease or laminopathy (father's sudden death at 45, septal mid-wall
  LGE); cardiac sarcoid; Lyme carditis.
- RM01: nocturnal seizure.

### L. Red herrings

- **Delete.**
  - Red herrings that sit only in outputs of non-criterion tools, for example an initial EEG.
  - Red herrings that cite data absent from the case.
- **field_path.** Each one must resolve to the actual field. Fix any that point to missing
  indices.
- **Data point and interpretation.** `data_point` is quoted from the field, and
  `correct_interpretation` explains it clinically, without tool names.

### M. Template carry-over (identical numbers across cases)

| Cases | What is identical | Fix |
| --- | --- | --- |
| M01, M02, M03 | echo (LVEF 50%, IVS 1.3 cm, LA 4.1 cm) | give each its own values consistent with age, hypertension and the conduction disease |
| M01, M03 | 12-lead ECG text | rewrite M03's ECG with its own rates and intervals |
| RS02, RS03 | echo, Holter (average 37, range 30-44, 3.8 s pause), CMR (native T1 1120 ms) | make RS03 distinct (different escape rate, pause timing, T1, LV size) |
| S02, S04 | patient record (medications, PMH, family history) and Holter (average 34, minimum 26 at 02:18) | rewrite S04's record and Holter as its own 82-year-old |
| S01-S04 | exercise and tilt reports | becomes moot: those tests are avoided (J); delete the stored follow-ups |

The rule: never copy a number from a sibling case.

### N. Patient-block leaks

- Remove result text from the HPI:
  - P01: the ED ECG result.
  - RP04: "ECG ... shows normal sinus rhythm".
  - Replace each with "ECG pending" or delete the clause.
- MRI reports contain MRA content (P03 initial MRI, RM01): remove the MRA.

### O. Kind 1 leakage inside reports

Delete these interpretive sentences:
- M01: the ECG's prognosis sentence.
- P03: the repeat ECG's "Long QT syndrome excluded" and "argues against ARVC" (the whole
  follow-up is deleted, F).
- P03: the initial ECG's "In isolation, this ECG would be read as normal" (that ECG is rewritten,
  section 4).
- P01: "(major criterion)" annotations in the CMR.
- RP05: "this satisfies histological confirmation" in the biopsy.

Reports describe findings, and the agent interprets them.

## 3. Target pathway and tiers

Pathway order for followup_outputs (and the order of the perfect agent):

1. 12-lead ECG.
2. Labs.
3. TTE.
4. Monitoring (telemetry or Holter per E).
5. Second-line test: CMR, FDG-PET, CTPA, exercise test or echo, PSG, tissue.
6. Drug check.
7. Off-pathway follow-ups: tilt, brain MRI, head CT, EEG, genetics, and CSF where kept.
8. Literature last.

Tiers by condition subtype:

| Subtype (cases) | Required | Recommended | Optional | Avoided |
| --- | --- | --- | --- | --- |
| Mobitz II, high-grade or complete AV block, degenerative, age 60 or over (M01, M03, RS02, RS03, S01, S02, S03, S04) | ECG, TTE, monitoring | BMP (M01, M03 required: BMP and Mg), drug check (except S02, S04 optional) | CMR, literature | EEG, MRI, CSF, tilt, exercise; head CT except S04 |
| AV block under 60 or with a cause to find (M02 55F, RM02 21F, RM03 58M, RS01 38F, RP04 41F, RP05 42F) | ECG, TTE, monitoring, the cause-finding test (RM02 inflammatory labs; RP05 PET and biopsy; RP04 ILR) | CMR (RP05: FDG-PET required instead), drug check | literature | as above |
| Severe AS (S05; S02 and S04 also have AS) | ECG, TTE, monitoring | BMP, drug check | literature | tilt and exercise (harm), EEG, MRI |
| QT and torsades, drug-induced (M04) | ECG, BMP and Mg, drug check, telemetry, TTE | - | EEG, literature | MRI, CSF, tilt |
| Congenital LQTS (P04) | ECG, TTE, monitoring | exercise test, drug check, BMP | EEG, literature | MRI, CSF, tilt |
| Brugada (P03) | ECG, monitoring | TTE, BMP, CMR | drug check, literature | tilt, exercise, MRI, EEG |
| CPVT (RP03) | ECG, TTE, monitoring, exercise test | CMR, BMP | drug check, literature | tilt, MRI, EEG |
| ARVC (P01, RP01) | ECG, TTE, monitoring, CMR (RP01 also BMP, Mg, urinalysis) | exercise test (P01), drug check | exercise (RP01), literature | tilt, MRI, EEG |
| HCM (P02) | ECG, TTE, monitoring, CMR, exercise echo, drug check | BMP | literature | tilt (harm), MRI, EEG |
| SVT, WPW, flutter (M05, RS04, RS06) | ECG, TTE, monitoring | BMP (TSH accepted), drug check | exercise (RS04), CMR (RS04), literature | tilt, MRI, EEG |
| VT in ischaemic cardiomyopathy (RS05) | ECG, BMP and Mg, telemetry, TTE, drug check | - | literature | tilt, exercise, MRI, EEG |
| SND (S06) | ECG, TTE, monitoring, drug check | BMP (TSH accepted) | literature | tilt, MRI, EEG |
| PE (RM04) | ECG, troponin and BNP, TTE, CTPA, telemetry, drug check | - | venous duplex, literature | D-dimer (not a criterion), MRI, EEG, tilt |
| Myxoma (RP02) | ECG, TTE, monitoring, CMR | BMP, drug check (optional) | literature | tilt and exercise (harm), MRI, EEG |
| Neurological mimic (RM01) | ECG, paraneoplastic panel, brain MRI, TTE, monitoring, PSG, chest CT tumour search | - | CSF, drug check, literature | EEG, tilt |

A note on RM01: PSG goes from recommended to required. It is the study that shows the central
apnoea preceding the asystole.

## 4. Per-case index

Every case also gets the condition-wide fixes. Each bullet list below gives only what is specific
to the case.
- A: literature.
- B: drug-check tier (table in B).
- C: lab tier and panels (table in C).
- D: sequences and stop rule.
- E: monitoring alternatives and fallback.
- H: engineering text and rationales.
- I: musts.
- J: avoided actions.
- K: differential.
- L: red herrings.

**SYNC-CARD-M01** (62M, paroxysmal Mobitz II or high-grade AV block, trifascicular disease)
- Leak guard fail: delete the initial literature and drug blocks (A, B).
- Labs required BMP and Mg. Fix Hct to 38.4 (C).
- Delete the EP-study interpret_labs follow-up (F).
- The monitoring output is a 48 h Holter: make it telemetry or Holter per E.
- Rewrite the echo with its own values (M).
- Delete the ECG prognosis sentence (O).
- Delete the isoproterenol tilt follow-up; tilt is waste (J).
- CMR becomes optional (age 62).
- Differential: VT low, SND low (K).
- Musts: dual-chamber permanent pacing (ESC 2021 Class I); admit with monitoring until paced;
  driving restriction.
- Delete the LP prohibition.

**SYNC-CARD-M02** (55F, Mobitz II, bifascicular block)
- Leak guard fail (A, B).
- Labs become recommended, BMP only.
- Add levetiracetam 500 mg twice daily (started 3 days ago) to the medication list (C).
- Hard labs before monitoring constraint: delete (D).
- Delete the isoproterenol tilt.
- CMR stays recommended (age under 60, ESC 2021 IIa).
- Musts: permanent pacing; review the indication for levetiracetam, since the events were
  arrhythmic; driving restriction.
- Delete the LP prohibition.
- EEG waste (the seizure label explained by the block).

**SYNC-CARD-M03** (71M, paroxysmal high-grade AV block, trifascicular)
- Leak guard fail (A, B).
- Labs required BMP and Mg.
- The monitoring output is a 48 h Holter under a telemetry trigger: fix per E.
- ECG and echo identical to M01: rewrite (M).
- CMR optional.
- Musts: permanent pacing.
- Delete the LP prohibition.

**SYNC-CARD-M04** (60F, drug-induced LQTS with torsades)
- Leak guard fail (A).
- Drug check required, accepting azithromycin, ondansetron or citalopram, ordered straight after
  the ECG. Add a soft sequence ECG before drug check.
- Labs required BMP and Mg. Remove beta-hCG (age 60). TSH accepted.
- Rewrite the literature text and red herring that name check_drug_interactions (H).
- EEG optional; MRI and CSF waste.
- Musts:
  - stop all three drugs;
  - IV magnesium sulfate 2 g;
  - potassium to 4.5-5.0 mmol/L (Drew 2010; replace the current "4.0-4.5" in
    expected_evidence);
  - telemetry until QTc is below 500 ms;
  - temporary pacing for pause-dependent recurrence;
  - avoid QT-prolonging drugs (CredibleMeds).
- Keep the existing prohibition on adding QT-prolonging drugs.
- Delete the LP prohibition.
- icd_codes[0] T46.2X5A is wrong for this case (azithromycin and ondansetron are not T46). Do
  not change it; CENTRAL C1.

**SYNC-CARD-M05** (52F, paroxysmal AVNRT)
- Monitoring event_monitor_14d per E.
- Labs recommended BMP, TSH accepted. Remove beta-hCG unless she is premenopausal per the record
  (52: keep it only if the record lists no menopause).
- Drug check recommended.
- Delete the ECG and monitoring musts (I).
- Differential: panic disorder low.
- Musts: modified Valsalva then adenosine for recurrences (REVERT, ESC 2019); slow-pathway
  ablation (Class I); pre-excitation absent on ECG before AV-nodal blockers.
- Diagnosis synonyms accept VT: CENTRAL C1.

**SYNC-CARD-P01** (55M, exercise-induced sustained VT, ARVC)
- Remove the ED ECG result from the HPI (N).
- Rewrite the echo impression in echo voice (G).
- Delete "(major criterion)" from the CMR (O).
- Delete the "Do not call" prohibition (H).
- Replace the "2020 Revised Task Force Criteria" and Sheldon/Rose references with the 2010 Task
  Force (H).
- Exercise test becomes recommended, with hard TTE before exercise.
- Delete the isoproterenol tilt.
- Drug check recommended.
- Delete the CMR must.
- Musts: ICD (ESC 2022 Class I for sustained VT); beta-blocker; exercise restriction; cascade
  screening of first-degree relatives; genetic counselling.
- The synonyms accept SVT and AVNRT: CENTRAL C1.

**SYNC-CARD-P02** (55M, obstructive HCM with NSVT)
- Leak guard fail (A).
- TTE Valsalva gradient: lower it below 50 mmHg (rest 24, Valsalva 38 mmHg). Exercise echo stays
  required as the provocation (ESC 2023 Class I), with hard TTE before exercise echo. The exercise
  echo output shows the provoked gradient (at least 50 mmHg, for example 78).
- Rewrite the echo impression (G).
- Drug check required: amlodipine and losartan.
- Delete the isoproterenol tilt; tilt is harm.
- Delete the "Do not call" text and the CMR must.
- Musts: stop amlodipine and losartan; non-vasodilating beta-blocker first-line; HCM Risk-SCD
  (O'Mahony 2014) for the ICD decision, counting unexplained syncope and NSVT; avoid dehydration.
- Cite ESC 2023.

**SYNC-CARD-P03** (38M, Brugada, fever-triggered)
- Leak guard fail (A).
- The initial ECG at 38.6 C must show a spontaneous coved type 1 pattern in V1-V2
  (fever-induced). Delete "In isolation, this ECG would be read as normal".
- Delete the EP, ajmaline and repeat-ECG follow-ups (F, O).
- Remove the MRA from the initial MRI (N); MRI waste.
- Monitoring becomes telemetry per E ("Continuous telemetry" is not a value).
- Rewrite the placeholder echo follow-up (G).
- Genetic testing: last follow-up only.
- Differential: LQTS low (QTc 408), CPVT and myocarditis low.
- Musts: treat fever with paracetamol now; ICD (ESC 2022 IIa, type 1 plus arrhythmic syncope);
  avoid brugadadrugs.org drugs; genetic counselling and cascade screening.
- Remove "serotonergic agents" from the prohibitions.
- Drug check optional.
- Replace the Antzelevitch title with the ESC 2022 reference.

**SYNC-CARD-P04** (19F, congenital LQTS, QTc 510 ms)
- Monitoring "Continuous telemetry": fix per E.
- Labs recommended BMP. beta-hCG may stay accepted (age 19), not required.
- Exercise test recommended (QT adaptation), with hard TTE before exercise.
- Delete the exercise-test must.
- EEG optional.
- Differential: epilepsy low.
- Genetic testing as the last follow-up only.
- Musts: nadolol or propranolol (Class I); avoid QT-prolonging drugs; correct K and Mg during
  illness; ICD not first-line; genetic testing and cascade screening.
- Cite ESC 2022 (QTc of 480 ms or more is diagnostic).

**SYNC-CARD-RM01** (71M, central sleep apnoea with sleep asystole, anti-Hu brainstem
encephalitis)
- Keep it in SYNC-CARD (open question Q1).
- MRI: dorsal medullary T2/FLAIR hyperintensity, consistent with the dysphagia and the key.
  Remove the MRA.
- Shorten the 18-minute CPR and intubation to "apnoeic bradycardia and asystole, recovering
  after brief bag-mask ventilation".
- PSG: move the data from interpret_labs into the order_specialized_test polysomnography output,
  written as a PSG report. PSG required.
- Chest CT: move to order_body_imaging chest_CT, and add the required tumour-search criterion (F).
- Delete the amiodarone follow-up.
- CSF optional, with an inflammatory output; remove the CSF avoidance (J).
- Labs required paraneoplastic_panel.
- Delete the MRI, PSG and antibody musts.
- Delete the invented references (Matsumoto 2023, Saiz 2020, Dalmau claims).
- Differential: OSA low; add nocturnal seizure.
- Musts: tumour search and oncology referral (Graus 2021); immunotherapy (IV steroids, IVIG or
  plasma exchange); permanent pacing or ventilatory support for sleep asystole (central apnoea
  treated with ventilation; pacing if asystole persists); monitored bed.

**SYNC-CARD-RM02** (21F, intermittent CHB, rheumatic heart disease)
- Labs required ESR, CRP and ASO.
- Delete the hard labs before monitoring constraint.
- Drug check required: chloroquine.
- Delete the "Do not call" text.
- Exercise test criterion: delete, and make it waste.
- CMR recommended.
- Differential: add chloroquine cardiotoxicity, acute rheumatic carditis (Jones 2015) and
  malaria.
- Musts:
  - stop chloroquine;
  - if ARF activity is shown by the inflammatory markers, temporary pacing while carditis is
    treated, then benzathine penicillin G secondary prophylaxis (she is allergic to sulfonamides
    only);
  - permanent pacing if the block persists;
  - echo follow-up of the valve lesions.

**SYNC-CARD-RM03** (58M, Mobitz II, bifascicular)
- Delete the "Do not call" text.
- Rewrite the placeholder order_ct_scan follow-up as a normal head CT, or delete it. The head CT
  becomes waste (aspirin monotherapy, no NG232 criterion), so delete the follow-up and the
  optional criterion.
- Exercise test: delete, and make it waste.
- CMR recommended (age 58).
- Drug check recommended.
- Musts: permanent pacing; continue aspirin.

**SYNC-CARD-RM04** (48F, acute PE with RV strain)
- Labs required troponin and BNP. Remove D_dimer (high clinical probability, ESC 2019). Keep
  beta-hCG only if she is premenopausal per the record; it is required here because CTPA
  depends on it.
- The hard ECG before CTPA constraint becomes soft.
- Drug check required: aspirin plus the anticoagulant.
- Venous duplex optional (order_body_imaging lower_extremity_venous_duplex).
- Musts:
  - LMWH (UFH if reperfusion is anticipated or CrCl is below 30 mL/min);
  - intermediate-high risk monitoring with rescue thrombolysis on deterioration;
  - review aspirin while she is anticoagulated;
  - hold metformin only if eGFR is below 30 or AKI is present (replace any blanket hold).

**SYNC-CARD-RP01** (29F, postpartum ARVC with NSVT)
- Labs required BMP, Mg and urinalysis.
- Delete the hard labs before monitoring constraint.
- Delete the "Do not call" text.
- Exercise test becomes optional.
- Delete the CMR must.
- Differential: eclampsia low (normal BP and urine), peripartum cardiomyopathy low (normal
  LVEF).
- Musts: ICD (ESC 2022 IIa, arrhythmic syncope with NSVT); a beta-blocker compatible with
  breastfeeding (metoprolol or propranolol, LactMed); exercise restriction; genetic counselling
  and cascade screening; contraception and pregnancy counselling.

**SYNC-CARD-RP02** (22M, RVOT myxoma with dynamic obstruction)
- Labs recommended BMP. Remove D_dimer unless the case's differential keeps PE with a
  low-probability rationale.
- Exercise test: delete, and make it harm (J).
- Tilt harm. Delete the isoproterenol tilt follow-up.
- Delete the "Do not call" text.
- Drug check optional.
- Differential: HCM and ARVC low.
- Musts:
  - urgent surgical excision (replace the anticoagulation must);
  - admission with monitoring and avoidance of exertion until surgery;
  - histology of the mass;
  - Carney complex screening if the history suggests it.
- Do not anticoagulate as a substitute for excision.

**SYNC-CARD-RP03** (38F, CPVT)
- Exercise test required (Class I), with hard TTE before exercise. The exercise output shows
  bidirectional or polymorphic ventricular ectopy rising with workload.
- Delete the isoproterenol tilt and the "Do not call" text.
- Genetic testing as the last follow-up only.
- Head CT waste unless the HPI documents an NG232 head injury.
- CMR recommended. Add the arrhythmic MVP and MAD mimic only if the CMR shows MVP or MAD (K).
- Differential: LQTS low.
- Drug check optional.
- Musts: nadolol at the maximal tolerated dose; exercise restriction; flecainide if events break
  through; ICD not first-line without cardiac arrest (ESC 2022); genetic testing (RYR2) and cascade
  screening.
- Synonyms accept SVT and AVNRT: CENTRAL C1.

**SYNC-CARD-RP04** (41F, intermittent CHB with asystole, misdiagnosed as epilepsy for 12 years)
- Remove "ECG ... shows normal sinus rhythm" from the HPI (N).
- Monitoring per E: ILR required, event_monitor_30d recommended, holter_24h optional. Delete the
  stepwise-escalation must.
- The ILR output captures asystole of at least 6 s during a typical event.
- Labs recommended AED_levels.
- Drug check required, drug lamotrigine or levetiracetam. Drop the current_medications pin.
- Delete the hard labs before monitoring constraint.
- Delete the "Do not call" text.
- Remove the PFO and bubble framing from the echo.
- EEG waste.
- Differential: refractory epilepsy low.
- Musts: permanent pacing; neurology review to withdraw the antiseizure drugs, beginning with
  lamotrigine; driving advice.

**SYNC-CARD-RP05** (42F, cardiac sarcoid with CHB and NSVT)
- Labs required calcium and ACE. Remove ANA and RF.
- Drug check required only if calcium is high (vitamin D); otherwise recommended.
- Delete the hard labs before monitoring constraint.
- Add soft FDG-PET before biopsy.
- Delete the citation_gap text.
- Replace "HRS 2017" with HRS 2014 (Birnie).
- Delete "this satisfies histological confirmation" from the biopsy.
- Differential: Lev-Lenegre low.
- Musts: ICD with pacing capability (HRS 2014 IIa, AV block plus NSVT); immunosuppression
  (corticosteroids); repeat FDG-PET to judge treatment response.
- Diagnosis synonyms include "complete heart block": CENTRAL C1.

**SYNC-CARD-RS01** (38F, CHB; father's sudden death at 45; septal mid-wall LGE)
- Delete the tilt criterion, and make tilt waste.
- CMR recommended.
- Labs recommended BMP. Lyme serology accepted only if the record gives exposure.
- Differential:
  - vasovagal low;
  - add familial conduction disease or laminopathy (LMNA, SCN5A), cardiac sarcoid and Lyme
    carditis.
- Musts:
  - consider an ICD rather than a pacemaker given the likely laminopathy (ESC 2021; ESC 2022);
  - genetic testing (LMNA, SCN5A) and cascade screening;
  - FDG-PET if sarcoid is not excluded.

**SYNC-CARD-RS02** (72M, CHB)
- CMR optional.
- Its echo, Holter and CMR numbers are shared with RS03. RS02 keeps its numbers and RS03 changes
  (M).
- Musts: permanent pacing; stop or reduce rate-slowing drugs if any.

**SYNC-CARD-RS03** (72M, CHB)
- Rewrite the echo, Holter and CMR values so that none equals RS02's (M). The patient record
  also differs.
- CMR optional.
- Musts: permanent pacing.

**SYNC-CARD-RS04** (40M, WPW with accessory-pathway tachyarrhythmia)
- Exercise test optional, with hard TTE before exercise.
- CMR optional.
- Delete the isoproterenol tilt and the "Do not call" text.
- Drug check optional.
- Differential: per K.
- Musts:
  - EP study and catheter ablation of the accessory pathway (ESC 2019 Class I);
  - no AV-nodal blockers if pre-excited AF;
  - synchronised cardioversion if unstable, IV procainamide or ibutilide if stable pre-excited AF.

**SYNC-CARD-RS05** (56F, sustained monomorphic VT, ischaemic cardiomyopathy)
- Labs required BMP and Mg. BNP accepted. beta-hCG is in the output but is not required.
- Delete the hard labs before monitoring constraint.
- Drug check required: the two beta-blockers in the list (a duplicate).
- Delete the serial-troponin must.
- Musts: ICD (ESC 2022 Class I, secondary prevention); keep one beta-blocker and stop the
  duplicate; amiodarone or VT ablation for recurrences; ischaemia evaluation.

**SYNC-CARD-RS06** (67M, atrial flutter with 1:1 conduction)
- Labs recommended BMP, TSH accepted.
- Replace CHA2DS2-VASc with CHA2DS2-VA. The score is 3; check the components against the
  record.
- Musts: a beta-blocker for rate control; anticoagulation per CHA2DS2-VA (ESC 2024); CTI ablation
  (Class I); no class IC drug without AV-nodal blockade.

**SYNC-CARD-S01** (70M, CHB)
- Leak guard fail (A, B).
- CMR optional.
- Exercise and tilt follow-ups: delete (J, M).
- Musts: permanent pacing.

**SYNC-CARD-S02** (74M, CHB with calcific AS, AVA 0.9 cm2)
- Leak guard fail (A).
- Tilt and exercise harm; delete their follow-ups.
- Delete the "Hold AV-nodal blockers" prohibition (he takes none).
- Drug check optional.
- CMR optional.
- Differential: VT low.
- Musts: Heart Team decision on TAVI or SAVR (ESC/EACTS 2021); permanent pacing.

**SYNC-CARD-S03** (66F, CHB, chronic flutter, ischaemic cardiomyopathy, LVEF 35%)
- Leak guard fail (A, B).
- CMR optional.
- Differential: VT low.
- Musts: CRT-D (LVEF 35%, high pacing burden; ESC 2021); continue warfarin uninterrupted
  through device implantation.

**SYNC-CARD-S04** (82M, CHB, calcific degenerative, with head strike)
- Rewrite the patient record and Holter so they no longer match S02's (M).
- Head CT recommended (NG232: age 65 or over with LOC). Delete the head-CT must.
- Tilt and exercise harm (AVA 0.9 severe AS per the case); delete their follow-ups.
- Delete "Hold AV-nodal blockers".
- Drug check optional.
- Musts: permanent pacing; Heart Team assessment of the AS (TAVI favoured at 82).

**SYNC-CARD-S05** (78M, severe AS)
- Leak guard fail (A).
- Tilt and exercise harm (keep the existing harm entries, and name AS in the reason).
- Delete the echo and "recognise BNP" musts.
- Drug check recommended.
- Musts: Heart Team, with TAVI favoured at 78 (ESC/EACTS 2021 Class I); caution with
  vasodilators; admission until the decision.

**SYNC-CARD-S06** (74F, sick sinus syndrome, tachy-brady)
- The 48 h Holter sits under a telemetry trigger: fix per E.
- Drug check required: diltiazem and metoprolol. Drop the current_medications pin.
- Labs recommended BMP, TSH accepted.
- Delete the Holter must.
- Musts: dual-chamber pacing for tachy-brady syndrome (ESC 2021 Class I); stop diltiazem
  (avoid two rate-slowing drugs); anticoagulation per CHA2DS2-VA if AF or flutter is documented.

## 5. CENTRAL requests

- **C1. Diagnosis synonyms** (`diagnosis_synonyms.yaml`).
  - Remove the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia",
    "conduction disease syncope" and "tachyarrhythmia". 29 of the 30 cases accept "cardiac
    syncope", so diagnosis scoring is trivial.
  - Remove R55 from the I44 code list.
  - Split I47 so that SVT and AVNRT (I47.1) and VT (I47.2) are distinct. At present P01 (ARVC)
    and RP03 (CPVT) accept "AVNRT" and "SVT", and M05 (AVNRT) and RS05 (VT) accept the other
    family.
  - Remove "complete heart block" from RP05. The sarcoid diagnosis must be named.
  - The M04 block keys on T46.2X5A, a wrong code for azithromycin, ondansetron and citalopram
    toxicity. Use I45.81 primary, with T36.3X5A, T45.0X5A and T43.225A as adverse-effect codes.
    The M04 icd_codes[0] is not to be changed by workers.
- **C2. Vocabulary** (costs.yaml, with library reports and the tool_io.py mirror).
  - order_specialized_test: `electrophysiology_study` and `sodium_channel_blocker_challenge`.
  - Genetic panels `inherited_arrhythmia` and `cardiomyopathy`.
  - perform_clinical_assessment: `orthostatic_blood_pressure` (active stand).
  - order_advanced_imaging: whole-body FDG-PET (RM01 tumour search), if it is not already there.
- **C3. Library.** The normal monitoring and normal tilt library reports contradict every
  bradyarrhythmia case. Per-case fallbacks cover this round. Consider a library entry that says
  "no recording stored for this order" rather than a normal result.
- **C4. Citation keys.** Add keys for:
  - ESC 2021 pacing, ACC/AHA/HRS 2018 bradycardia, ESC 2022 VA/SCD, ESC 2023 cardiomyopathies,
    ESC 2019 SVT, ESC 2019 PE, ESC/EACTS 2021 VHD and ESC 2024 AF;
  - 2010 ARVC Task Force, HRS 2014 sarcoid, O'Mahony 2014, Drew 2010, Gewitz 2015, Graus 2021,
    NICE NG232 and Fletcher 2013.
- **C5.** Verify the reference behind [Locati_2014]. The pack text says Heart 2016; it may be the
  SYNARR-Flash study (Europace 2016;18:1265-1272). Correct the key or its bibliography entry.
- **C6. BANNED table for SYNC-CARD** (test_case_guards.py):
  - "Do not call `";
  - "cited via";
  - "citation_gap";
  - "Not retrieved on this pathway";
  - "on this case's pathway";
  - "on this pathway";
  - "CHA2DS2-VASc";
  - "Continuous telemetry" as a monitor_type value.
- **C7. Guard.** A tilt report containing "isoproterenol" in a case whose history lists
  ischaemic heart disease, AS or HCM.
- **C8. Review UI.** The case viewer should show the stop-rule criteria and sequence constraints
  next to the action criteria, so that reviewers see the scoring order.

## 6. Open questions for Andrea

- **Q1.** RM01 (anti-Hu brainstem encephalitis with central sleep apnoea and sleep asystole) is a
  neurological cause of syncope-like events, not cardiac syncope. I kept it in SYNC-CARD and
  repaired its data. Should it move to a neuro-oncology or paraneoplastic condition in the dataset
  structure? That is a dataset-design choice only you can make.
- **Q2.** M04 icd_codes[0] is T46.2X5A, the code for adverse effects of other antidysrhythmic
  drugs, which is wrong for these drugs. Changing the primary code touches the scorer through the
  synonyms file. I sent it to CENTRAL (C1) and workers leave it alone. Confirm that CENTRAL owns
  it.
