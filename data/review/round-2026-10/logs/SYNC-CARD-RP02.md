# SYNC-CARD-RP02
Reviewer status: R1 none, R2 none (SYNC-CARD was never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | minor | `patient.neurological_exam.additional` | A pulmonary-area ejection murmur "radiating to the neck" (the radiation of aortic stenosis). | FIXED: radiates to the left infraclavicular area and the back. |
| B | major | `followup_outputs[0]` (TTE), `followup_outputs[2]` (CMR) | Echo called the RV "severely dilated" and CMR called RVEDVI 92 mL/m2 "severely elevated", which is normal for a man; RV pressure overload from outflow obstruction produces hypertrophy (as the ECG RVH shows). Echo lacked echo_type, PA pressure, LV wall thickness; "no PFO" framing. CMR impression argued "No evidence of ARVC". | FIXED: echo upper-normal RV with 7 mm free-wall hypertrophy, TR 4.9 m/s, RVSP 108, PA systolic about 18 mmHg (RVSP minus the 90 mmHg gradient), LV 9 mm, no LVOT gradient, echo_type TTE, septum "intact"; CMR RVEDVI 94 mL/m2 normal, RVEF 48%, RV hypertrophy, no fat, WMA or LGE stated as findings, mass "most consistent with a myxoma; histological confirmation required". |
| B | major | `followup_outputs[1]`, `action-4-order-cardiac-monitoring`, `fallback_tool_outputs.cardiac_monitoring` | 342 PVCs called "frequent" and "1.4%" (0.3% at 82 bpm average); a Holter reported axis, RVH and Brugada ST changes; patient diary of a stair climb; criterion pinned `holter_24h` with label "Telemetry and Holter". | FIXED (plan E): alternatives telemetry, holter_24h, holter_48h; "Inpatient telemetry, 24 h" with 0.3% burden and monitoring-only findings; symptom reported to the nurse; same recording as the case fallback. |
| C | major | `action-2-interpret-labs` | Recommended with CBC, BMP, Mg, troponin and D-dimer pinned; expected_evidence was policy text. | FIXED (plan C): `panels: [BMP]`; D-dimer stays in the stored output and is used in the differential (low-probability PE, ESC 2019). |
| C | major | `action-6-order-specialized-test` (deleted), `avoided_actions` | Exercise test recommended in exertional syncope with a mobile obstructing RVOT mass; tilt only prohibited in text. | FIXED (plan J): criterion deleted; `avoid-harm-6-exercise-stress-test` and `avoid-harm-5-tilt-table` added; tilt follow-up deleted (plan J, harm). The exercise follow-up is kept, rewritten in test voice, so that a harmful order receives this patient's response (presyncope, BP 106/64 to 85/50) rather than the library's normal test. EEG waste added. |
| C | major | `action-7-check-drug-interactions`, `followup_outputs[3]`, drug initial and fallback | Required medication review whose only stored output was a pre-operative heparin plan (anticoagulation the case should not substitute for surgery). | FIXED (plan B): optional, drug albuterol; heparin follow-up deleted; albuterol follow-up and medication-list review (initial and fallback) in report voice. |
| C | major | `action-8-search-medical-literature`, `followup_outputs[5]` | Literature required and in the stop rule; follow-up cited unverifiable case reports and a patient-specific summary ("normal EEG ... elevated BNP"). | FIXED: optional, canonical rationale; one follow-up with ESC 2018 content only, placed last. |
| A | minor | `stop_rule`, `sequence_constraints`, `citations`, `rationale` | `max_additional_actions: 0`; no constraints; "§" and Locati citations; rationale equal to label. | FIXED: required list ECG, TTE, telemetry, CMR; 3; soft ECG before TTE, ECG before monitoring, TTE before CMR; keys only; real rationales; criteria reordered (ids unchanged). |
| C | blocker | `ground_truth.assessment` | Musts: "anticoagulation consideration", "cardiothoracic surgery consult", "EP consultation"; no excision, histology, Carney screening or driving advice; "Do not call `order_specialized_test`" engineering text; tilt prohibition (a test). | FIXED (plan): musts are diagnosis (RVOT mass, likely myxoma, not epilepsy), monitored admission with restricted exertion, urgent surgical excision this admission, histopathology, Carney complex screening (young age, RV location), post-excision echo surveillance, sport and driving restriction. Prohibitions: anticoagulation instead of excision, discharge before excision, vasodilators or diuretics before excision, epilepsy diagnosis and antiseizure drugs, sport. |
| C | minor | `avoided_actions` rationales | Brain MRI "may be considered if cerebral embolism from a myxoma is suspected" (a right-sided tumour embolises to the lungs); CT rationale ignored the forehead bruise. | FIXED: rationales name the diagnosis, the embolic territory and NICE NG232. |
| C | major | `ground_truth.differential` | HCM and ARVC high, PE and PAH moderate after echo and MRI exclude them; PE argued from a CTPA that is not on the pathway; pulmonary stenosis, sarcoma/thrombus and epilepsy missing. | FIXED (plan K): HCM, ARVC, PE, PAH low with the excluding results (LV 9 mm, no LVOT gradient; normal RV volume, no fat or LGE; D-dimer 0.38 and PA pressure about 18); pulmonary stenosis, sarcoma or thrombus, and epilepsy added as low. |
| L | minor | `ground_truth.red_herrings` | Red herring 1 cited a CTPA not on the pathway; data_points paraphrased. | FIXED: quoted data_points, interpretations from pathway data; albuterol-for-exertional-dyspnoea red herring added. |
| C | minor | `key_clinical_evidence`, `metadata.difficulty_*` | "Anticoagulation may be required for embolic risk"; "young athlete"; generic text. | FIXED: rewritten from the pathway results. |

## Changes, in one paragraph a physician can read before re-reviewing

The 22-year-old man with two exertional collapses, a pulmonary-area murmur and RV heave now has four required steps: ECG (RVH and right precordial strain), TTE, inpatient telemetry (Holter accepted) and cardiac MRI; a BMP is recommended, the albuterol review and the literature lookup optional. The echo and MRI now agree with each other and with the ECG: the obstructing 21 x 18 mm RVOT mass (gradient 90 mmHg, RVSP 108, PA systolic about 18) produces RV hypertrophy with a normal RV volume (RVEDVI 94 mL/m2), not a "severely dilated" RV. Telemetry reports a correct PVC burden (0.3%). Tilt and exercise testing are harm (a patient-consistent exercise report is kept so a harmful order is not answered by a normal library test); EEG, brain MRI, head CT and CSF are waste. The management is urgent surgical excision with histology, monitored admission with restricted exertion, Carney complex screening, post-excision echo surveillance and sport and driving restriction; anticoagulation as a substitute for excision and vasodilators or diuretics are prohibited. HCM, ARVC, PE and PAH are low with the excluding results, and pulmonary stenosis, sarcoma or thrombus and epilepsy are added.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan C1: `accepted` still carries the generic "cardiac syncope"; not hand-edited.
- Plan C3: with the tilt follow-up deleted (harm), a tilt order is answered by the library's normal tilt report (HR 68) although his resting HR is 104.

## Open questions for Andrea (judgment calls you could not settle)

None. Deviation from the plan, decided for consistency of the simulated patient: the exercise-test follow-up is kept (the plan deletes the criterion and makes the test harm, which is done) because without it a harmful exercise order would receive the library's normal treadmill result.

## Verification

Adversarial verification, 24 Oct 2026 (diff against fa1d22e6; the batch-4 checkpoint commit holds the worker's edit).

Checked: no reviewer notes for SYNC-CARD. Plan items: labs recommended BMP with D-dimer kept only as data for a low-probability PE differential; exercise test criterion deleted and made harm; tilt harm and the isoproterenol tilt deleted; "Do not call" text gone; drug check optional; HCM and ARVC low; musts are urgent excision, monitored admission with restricted exertion, histology and Carney screening, with no anticoagulation substitute. CMR volumes are internally consistent (RVEF (168-87)/168 = 48%, LVEF (125-48)/125 = 62%, RVEDVI 94 at BSA about 1.79). The PA systolic estimate (RVSP minus the 90 mmHg RVOT gradient = 18 mmHg) is consistent with the differential. Red herrings quote their fields; guards pass.

Found and fixed:
- `followup_outputs[0].output.valves["Tricuspid valve"]`: TR 4.9 m/s (gradient 96 mmHg) plus the stated RA pressure of 10 mmHg gives 106, not the RVSP of 108 reported in four places. RA pressure set to 12 mmHg (consistent with the moderately dilated RA and a JVP of 10 cm H2O), so every 108 and the derived PA pressure of 18 stand.
- `ground_truth.avoided_actions[avoid-harm-5-tilt-table].rationale` and `prohibited_recommendations[2]` called the obstruction "fixed", while the diagnosis label, the musts, the echo and the CMR describe a mobile mass with dynamic obstruction. Now "severe dynamic" and "severe" respectively.
- With the tilt follow-up deleted, a (harmful) tilt order received the library's normal tilt (HR 68) although his resting HR is 104 (the worker's CENTRAL note). Added a neutral "Tilt-table test not performed. Deferred by the clinical team." follow-up (`test_type: tilt_table`, trigger `request_tilt_table`) before the literature follow-up, as RM04 does; it reveals nothing about the diagnosis and the harm penalty still applies.

perfect_agent.py SYNC-CARD-RP02 -v: ok. case_io.py check: clean for this case.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case pass over the 30 SYNC-CARD cases.

Changed:
- Added `initial_tool_outputs.literature_search.general` (the neutral syncope evaluation block already used in P02-P04 and RM01-RM03: ESC 2018 and ACC/AHA/HRS 2017 initial evaluation and risk stratification). Why: with no initial literature output, MockServer tier 2 answered any generic query (e.g. "syncope guidelines") with the case's disease-specific follow-up, which names the diagnosis. The block repeats no expected_evidence (leak guard passes).
- Literature follow-up trigger `search_exertional_syncope_structural_heart_disease` renamed to `search_exertional_structural_heart_disease`. Why: the old trigger's meaningful tokens were generic (management, guidelines, diagnosis, syncope, literature), so a generic query hit the disease-specific report; the new tokens are the condition names, so only a query naming the condition reaches it.

Re-run after the change: perfect_agent 30/30 clean, case_io check clean for SYNC-CARD, test_case_guards for SYNC-CARD 60 passed, discriminator and hijack guards clean.
