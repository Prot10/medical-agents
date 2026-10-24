# SYNC-CARD-RS04
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| E | major | `assessment.prohibited_recommendations` | "Do not call `order_specialized_test` with parameters {...}" engineering text; duplicated digoxin/verapamil prohibition; "Do not perform tilt-table" (a test, not management). | FIXED: deleted; prohibitions are AV-nodal blockers or IV amiodarone in pre-excited AF, discharge without an ablation plan, attribution to stress or a vasovagal reaction. Tilt is an avoided action (waste). |
| C | major | tilt follow-up | Isoproterenol tilt (plan RS04: delete). | FIXED: deleted; a tilt order now gets the library's normal tilt, which is true for this patient. |
| C | major | `action-7-search-medical-literature`, `stop_rule`, literature follow-up | Literature required and in the stop rule; follow-up mixed the 2015 ACC/AHA/HRS SVT guideline with unverified reviews (Bhatia 2016, Pappone 2017) and patient-level conclusions. | FIXED: optional, canonical rationale; rewritten from ESC 2019 SVT (ablation Class I; drugs to avoid in pre-excited AF, Class III; exercise testing IIb in asymptomatic pre-excitation); last. |
| C | major | `action-6-check-drug-interactions`, drug follow-up, fallbacks | Required with no drug (plan: optional); "Agent selection ... per electrophysiology evaluation"; with no initial drug output any drug check (verapamil, adenosine) was answered with the procainamide follow-up. | FIXED: optional, `drug: procainamide`; follow-up in report voice (label contraindications, QRS and BP monitoring); a medication-list review with the disease-related cautions (AV-nodal blockers and IV amiodarone in pre-excited AF, adenosine with a defibrillator) stored as initial and fallback drug output, so other drugs receive it instead of the library's "No interaction identified". |
| C | major | `action-5-order-specialized-test`, exercise follow-up | Exercise recommended with expected evidence "loss of pre-excitation argues for low-risk pathway"; the output described a gradual loss (which is not a low-risk marker; it reflects faster AV-nodal conduction) and then called it "rate-dependent block in the accessory pathway". With syncope, EP study and ablation are indicated whatever exercise shows. | FIXED: optional (plan), hard TTE before exercise; output rewritten coherently: pre-excitation persists to 168 bpm with no abrupt loss, no arrhythmia, normal BP. |
| B | minor | `initial_tool_outputs.ecg` | "Posterior left hemiblock pattern with left posterior fascicular block morphology" and "RBBB morphology" described as conduction disease; PR 120 ms called "short, at lower limit of normal". | FIXED: pre-excited QRS described with delta-wave polarity (left-sided pathway), PR 100 ms, right axis and RBBB-like pattern attributed to pre-excitation; expected evidence updated. |
| A | minor | echo follow-up | No `echo_type`; values without units; valves empty. | FIXED: full TTE report with units (LVEF 62% biplane, LVEDD 4.8 cm, LA 3.6 cm, TAPSE 24 mm, RVSP 28 mmHg), normal tricuspid leaflet insertion (Ebstein anomaly is associated with accessory pathways). |
| B | major | `action-4-order-cardiac-monitoring`, monitoring follow-up | Criterion pinned holter_24h under a "Telemetry and Holter" label; "patient diary" in a recording; no case fallback (plan E). | FIXED: alternatives telemetry, holter_24h, holter_48h; "Inpatient telemetry, 24 h" with the same events (three orthodromic AVRT episodes at 178-196 bpm, one symptomatic, no AF), retrograde P waves added; same recording as the monitoring fallback. |
| C | minor | CMR follow-up | "No features of ARVC, HCM, or other structural cardiomyopathy" and em dash. | FIXED: findings only; CMR stays optional. |
| C | minor | `action-2-interpret-labs` | Pinned CBC, BMP, Mg, troponin. | FIXED: recommended, `panels: [BMP]` (plan C). |
| C | major | `avoided_actions` | EEG and tilt not penalised; reasons generic. | FIXED: brain MRI, head CT (age 40, no head injury, no anticoagulant: no NG232 criterion), CSF, EEG and tilt as waste, naming the diagnosis. |
| C | major | `ground_truth.assessment` | "EP consult for ablation" and generic musts. | FIXED: musts are the diagnosis, monitored admission with a defibrillator, EP study and ablation (ESC 2019 SVT Class I), acute management of orthodromic AVRT (vagal, adenosine with defibrillator, cardioversion if unstable), pre-excited AF (cardioversion or procainamide/ibutilide; no AV-nodal blockers or IV amiodarone), no driving or competitive sport until ablation. |
| C | major | `ground_truth.differential` | Pre-excited AF "high", AVNRT and VT "moderate" after telemetry captured orthodromic AVRT and imaging showed a normal heart (plan K). | FIXED: pre-excited AF low (none captured; its risk is the reason for ablation), AVNRT low, VT low, channelopathy low, PRKAG2/Danon-type cardiomyopathy very low (normal wall thickness), vasovagal very low. |
| L | major | `red_herrings` | data_point "Brief palpitations attributed to caffeine" (the HPI says he denies caffeine and attributed them to stress); second red herring pointed at a sentence absent from the ECG ("Resting ECG can intermittently lose delta waves"). | FIXED: first quotes "he dismissed them as being related to stress at work"; second replaced by the RBBB-like pre-excited QRS in `initial_tool_outputs.ecg.findings`. |
| A | minor | all criteria, `stop_rule`, `sequence_constraints` | Free-text section citations, rationale equal to label, `max_additional_actions: 0`, no constraints. | FIXED: keys only, real rationales, stop rule ECG/TTE/monitoring with 3 additional actions, soft ECG before TTE and monitoring, hard TTE before exercise. |

## Changes, in one paragraph a physician can read before re-reviewing

The 40-year-old man with sudden syncope and a WPW pattern now has three required steps (ECG, TTE, inpatient telemetry with Holter accepted) and a recommended BMP. Telemetry captures symptomatic orthodromic AVRT at 178-196 bpm and no atrial fibrillation. The ECG describes a left-sided accessory pathway (PR 100 ms, delta waves, pre-excited QRS 148 ms) rather than bundle branch and fascicular block. The exercise test is optional and now internally coherent (pre-excitation persists to 168 bpm, no abrupt loss), since an EP study is indicated after syncope regardless; CMR, drug review and literature are optional. The isoproterenol tilt and the engineering prohibitions are gone; brain MRI, head CT, CSF, EEG and tilt are waste. Musts: EP study and ablation (ESC 2019 SVT Class I), monitored admission with a defibrillator, acute management of AVRT and of pre-excited AF without AV-nodal blockers or IV amiodarone, no driving or competitive sport until ablation. All alternatives in the differential are low or very low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: "cardiac syncope" is still accepted as a synonym; not hand-edited.
- Plan C2: no `electrophysiology_study` in the vocabulary, so the EP study lives in a must only.

## Open questions for Andrea (judgment calls you could not settle)

None needing Andrea.

## Verification

Checked (24 Oct 2026, adversarial pass): the log against the diff from fa1d22e6 and the whole final case; ECG delta-wave polarity (negative I/aVL, positive V1 and inferior, right axis) is a left lateral pathway, consistent with the text; telemetry (orthodromic AVRT, retrograde P, no AF; fallback identical); exercise follow-up coherent; CMR arithmetic ((142-55)/142 = 61%); ESC 2019 SVT statements in the literature output (ablation Class I; IV amiodarone and AV-nodal blockers Class III in pre-excited AF; IIb non-invasive stratification); procainamide label and QRS-widening stop rule; plan tiers (exercise, CMR, drug check optional; hard TTE before exercise); differential per plan K.

Found and changed:
- Echo `wall_motion` said "subtle early septal activation consistent with pre-excitation", but the ECG places the pathway on the left lateral wall, which pre-excites the basal lateral LV, not the septum. Now "subtle early contraction of the basal lateral wall".
- The hard TTE-before-exercise constraint carried the canonical reason "Exertional syncope requires ...", but this syncope happened standing at a desk, not on exertion. The reason now states the actual rationale for this case (unexplained syncope; obstructive HCM, which can coexist with pre-excitation, and severe AS excluded before exercise), same guideline references.

perfect_agent clean, `case_io.py check` clean for this case, leak guard passes.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).
- Literature follow-up trigger `search_wpw_syncope_management` renamed to `search_wpw_wolff_parkinson_white_accessory_pathway`. Why: the old trigger's meaningful tokens were generic (management, guidelines, diagnosis, syncope, literature), so a generic query hit the disease-specific report; the new tokens are the condition names, so only a query naming the condition reaches it.

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.

## Close-out (24 Oct 2026)

Close-out of the condition (plans/SYNC-CARD-decisions.md). Not a re-review: every change below is cross-case.

- Diagnosis synonyms (`diagnosis_synonyms.yaml` SYNC-CARD block, applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac`): the generic labels "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia" and "conduction disease syncope" are retired (29 of 30 cases accepted "cardiac syncope", so any cardiac answer scored), and R55 is no longer an accepted code.
- "ESC/EACTS 2021" renamed "ESC/EACTS 2025" (2025 ESC/EACTS valvular guideline, Praz 2025, supersedes 2021): `.ground_truth.sequence_constraints[2].reason`.
- Citations now follow the guideline each rationale or reason names (ruling 8; new keys in the criteria pack allow-list): action-3-order-echocardiogram citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2019_SVT]']; action-5-order-specialized-test citations ['[ESC_2018]'] -> ['[ESC_2019_SVT]']; avoid-waste-2-order-ct-scan citations ['[ESC_2018]'] -> ['[NICE_NG232]']; action-3-order-echocardiogram->action-5-order-specialized-test citations ['[ESC_2018]'] -> ['[ESC_2018]', '[ESC_2023_Cardiomyopathy]', '[ESC_EACTS_2025_VHD]'].

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; `test_case_guards.py -k SYNC-CARD-RS04` pass (SYNC-CARD now in `DISCRIMINATOR_CONDITIONS`); synonym `--check` clean.
