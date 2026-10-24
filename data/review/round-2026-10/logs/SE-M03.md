# SE-M03
Reviewer status: R1 none, R2 approved (2 issue notes) | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 0aed33a9-15ce-4875-9146-967f896dbe63 | FIXED | `initial_tool_outputs.labs.panels["Exclusion studies"]` and `["Mimic exclusion"]` deleted (C1). The urinalysis now appears once, in its own panel (protein 2+, RBC casts present, RBC 15-20/hpf added); CRP 4 mg/L is reported in the rheumatology panel and beta-hCG <2 mIU/mL in a pregnancy panel; ABG dropped (not indicated, SpO2 98%). The autoimmune encephalitis antibodies are no longer duplicated in the first-line labs: they are a separate serum panel follow-up (`request_autoimmune_encephalitis_panel`, NMDAR, LGI1, CASPR2, AMPAR, GABA-B, GAD65 negative) answering criterion action-6. |
| adc24e17-c7b6-435c-85e7-0c0285ac63ae | FIXED | One characterisation everywhere: prednisone 30 mg daily on day 10 of a taper started for a joint flare. `patient.history_present_illness` ("low-dose" removed), `medications[prednisone].frequency` "daily (day 10 of a taper)", `past_medical_history[0]` (remission until the joint flare), and `ground_truth.differential[4]` renamed "Steroid-associated hypertension precipitating PRES" (no "high-dose steroid"). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.history_present_illness` | "She has no prior history of seizures or epilepsy" contradicted the medication list and PMH (first unprovoked seizure 6 months ago, on levetiracetam). | FIXED: "She had one previous unprovoked seizure 6 months ago." |
| B | minor | `patient.neurological_exam.cranial_nerves` | Intermittent left gaze preference with a left temporal (T3-T5) seizure focus: ictal deviation is away from the focus (C6). | FIXED: intermittent rightward gaze deviation; the EEG video correlate records it. |
| C | major | `followup_outputs` `request_aed_optimization`, `request_continuous_eeg_monitoring` | Post-escalation levetiracetam level and an EEG "after BP control and levetiracetam escalation" reported management not yet recommended (ruling 4, C4); the EEG trigger also hijacked the cEEG order. | FIXED: both deleted; the `continuous_icu` order receives the initial EEG. |
| D | minor | MRI follow-up `signal_characteristics`, finding types | "confirming vasogenic not cytotoxic edema (reversible PRES)", "ictal not ischemic", "corresponding to NCSE focus" (cross-modality and conclusions in data fields). | FIXED: signal descriptions only; the impression (unchanged) keeps the worded imaging differential. |
| B | minor | CSF follow-up `interpretation` | Called the pleocytosis both mononuclear and lymphocytic (3 lymphocytes, 5 monocytes); "no evidence of bacterial infection" without a Gram stain or culture. | FIXED: mononuclear throughout; Gram stain and culture negative to date added; criterion evidence updated. |
| C | major | criterion action-8 literature, follow-up | Literature required, in the stop rule, with a management expected text; output percentages unsourced (ruling 5). | FIXED: optional, last, out of the stop rule; T-LIT content cited to [Fugate_2015], [Glauser_2016], [ESETT_2019]. |
| C | minor | drug-check follow-up, criterion action-7 | Expected text said "nicardipine drip safe"; output did not mention valproate teratogenicity, enzyme induction or IV antihypertensives. | FIXED: T-DDI content (levetiracetam no interaction; fosphenytoin with prednisone and amlodipine; nicardipine or labetalol with amlodipine; lacosamide with labetalol; hydroxychloroquine QT and seizure threshold; valproate teratogenicity as contraindication). Recommended (C9). |
| C | minor | criterion action-6 | Duplicate lab criterion answered by the "Mimic exclusion" entry of the first-line labs. | FIXED: recommended second-tier serum panel answered by its own follow-up (plan section 4). |
| B | major | `ground_truth.sequence_constraints[1]` | Labs before drug check `hard`: the reverse order is not unsafe (C13). | FIXED: deleted; CT before CSF (hard) kept. |
| C | major | `required_recommendations` | Lorazepam without maximum; BP target without the follow-on target; "load levetiracetam (subtherapeutic)"; a must that was a test already in the labs (beta-hCG); consult wording. | FIXED: T-MUST-BZD; titratable IV BP lowering by no more than 25% in the first hour then towards 160/100 [Fugate_2015]; T-MUST-2L (levetiracetam 60 mg/kg max 4500 mg, avoid valproate for teratogenicity); T-MUST-cEEG; rheumatology and nephrology for the nephritis flare. |
| E | minor | `prohibited_recommendations[1]` | "if cardiac instability develops without monitoring" garbled. | FIXED: "Do NOT give fosphenytoin without continuous cardiac and blood pressure monitoring during the infusion". |
| C | major | `ground_truth.differential` | CNS lupus and hypertensive encephalopathy "high", APS/autoimmune "moderate" after MRI, CSF and the antibody panel exclude them (C14). | FIXED: all low, key features cite the MRI, CSF and antibody results. |
| C | minor | `key_clinical_evidence[0]`, `[2]` | PRES MRI pattern called "pathognomonic"; "triple-hit" wording. | FIXED: "characteristic but not specific [Fugate_2015]"; concurrent precipitants reworded. |
| A | minor | `red_herrings[].field_path` | Both pointed at the whole labs block. | FIXED: levetiracetam value and the RBC-casts row. |
| C | minor | avoided action polysomnography | DaTscan rationale (C11). | FIXED: T-PSG text. |
| E | minor | criteria labels/rationales; EEG arguments | Rationales copied from labels; EEG without `eeg_type`; MRI cited Glauser (treatment). | FIXED: T-LABS (extras AED_levels and beta-hCG; ESR, CRP, urinalysis and ABG no longer required arguments but reported), T-CT, T-EEG, MRI [Brophy_2012; Fugate_2015], CSF [Tunkel_2008]. |
| B | minor | EEG impression | Not in report format. | FIXED: numbered ABNORMAL impression in ACNS terms; data unchanged. |
| A | minor | `fallback_tool_outputs.advanced_imaging`, `.specialized_test` | Prose modality "FDG-PET brain" and non-vocabulary test type (C10). | FIXED: deleted; `fallback_tool_kinds` updated. |
| B | minor | order; `stop_rule` | Not the diagnostic order; allowance 0 (C12). | FIXED: labs, CT, EEG, MRI, CSF, antibody panel, drug check, literature; stop rule = 5 required, allowance 1. |

## Changes, in one paragraph a physician can read before re-reviewing
The presentation is unchanged except for two corrections: the HPI now acknowledges her single prior unprovoked seizure, and prednisone is described once as 30 mg daily on day 10 of a taper for a joint flare. The template exclusion blocks are gone; the labs report each analyte once (low levetiracetam, active lupus serology, nephritic urine, negative beta-hCG, CRP 4). The gaze sign now points away from the left temporal focus. Post-treatment levels and EEG are removed. The serum autoimmune panel is a recommended second-tier test with its own negative report; CSF stays required. Musts: lorazepam, controlled IV BP lowering (no more than 25% in the first hour), levetiracetam load avoiding valproate, cEEG, rheumatology and nephrology. The differential now ranks lupus cerebritis, plain hypertensive encephalopathy and autoimmune or antiphospholipid causes low after the work-up.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: allow-list `[ACNS_2021]`, `[Fugate_2015]`, `[Tunkel_2008]`, `[Graus_2016]` for SE; this case cites them.

## Open questions for Andrea (judgment calls you could not settle)
None. Decided: ESR, CRP and urinalysis are no longer required arguments of the core labs (the plan's T-LABS extras list), although they stay in the stored report; the case's lupus evidence is still delivered to any core-labs order.

## Verification
`perfect_agent.py SE-M03 -v`: pass; each criterion receives its report (labs initial, EEG initial for `continuous_icu`, MRI, CSF, antibody panel and drug check from their follow-ups). `test_case_guards -k SE-M03` and the red-herring path test: pass. `case_io.py check SE-M03`: schema and synonym guard OK; no failure names SE-M03.

## Verification (adversarial verifier, 24 Oct 2026)
Checked: both notes. 0aed33a9: no "Exclusion studies" or "Mimic exclusion" block remains; urinalysis appears once (protein 2+, RBC casts, RBC 15-20/hpf), consistent with the abnormal summary and the red herring path `Urinalysis[1]` (RBC casts); autoimmune antibodies appear only in their own serum follow-up and the CSF. adc24e17: "low-dose" and "high-dose" are gone from the whole file; prednisone is 30 mg daily, day 10 of a taper, in HPI, medication list and PMH; the differential entry reads steroid-associated hypertension. Also confirmed: rightward ictal gaze with a left temporal EEG focus; post-treatment level and EEG follow-ups deleted; beta-hCG kept with a value; drug check recommended with T-DDI content; literature optional and last; hard labs-before-drug-check constraint removed; stop rule equals the 5 required criteria. Allergy (sulfonamides) is not contradicted by any must or drug check.
Found and fixed (real errors only; the case is approved):
- B minor `patient.neurological_exam.mental_status`: "Awake ... GCS 11 (E3V3M5)" while the HPI says she is minimally following commands in the ED: awake is E4 and following commands is M6. FIXED: "GCS 13 (E4V3M6)" and "follows simple commands only intermittently" added so the components are derivable.
- B minor `action-3-order-ct-scan.expected_evidence`: "suggests PRES" (with an em dash) while the CT impression says PRES and ictal edema cannot be distinguished on CT. FIXED: "Subtle bilateral posterior cortical-subcortical hypodensity, nonspecific on CT (PRES versus ictal edema); no hemorrhage or mass".
Checks re-run after my edits: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, `test_case_guards -k` pass.

## Close-out (24 Oct 2026)
Decisions in `plans/SE-decisions.md`.
- synonyms: the G41 category no longer grants the type codes G41.0, G41.2 and G41.8 (a type code is granted only by the case's own code, so an answer coded with the wrong SE type no longer scores by code); `apply_diagnosis_synonyms.py --prune --conditions status_epilepticus` removed G41.0 and G41.8 from `ground_truth.diagnosis.icd_codes`. Labels unchanged.
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, SE case guards pass, `apply_diagnosis_synonyms.py --check --conditions status_epilepticus` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `continuous_icu`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
