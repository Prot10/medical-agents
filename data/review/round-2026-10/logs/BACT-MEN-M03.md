# BACT-MEN-M03
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 790f6cf0-c6d4-4ffe-99f4-2492093ab211 | FIXED | Blood culture `susceptibility` split per drug; "Penicillin MIC: 0.12 ug/mL (Resistant, CLSI meningitis breakpoint)"; ceftriaxone and meropenem labelled with the meningitis breakpoint. Targeted must and a metadata pearl state that the resistance explains the amoxicillin failure. |
| e5f3a2fd-93dc-4200-b4ff-bd654cf1485e | FIXED | Index CSF moved out of `initial_tool_outputs.csf` to `followup_outputs[2]` (`request_lumbar_puncture`) after the CT; repeat LP deleted; CT impression reports findings only, "No contraindication to lumbar puncture" deleted. The HARD constraint is now satisfiable and satisfied by the pathway order. |
| 5968179a-9eb3-4dc1-a385-eed5502dba63 | FIXED | CT criterion (`action-4-order-ct-scan`, now listed third) label and rationale rest on WHO 2025 A.4 severe immunocompromise (post-traumatic asplenia with incomplete pneumococcal immunisation); IDSA 2004, "age >60" and "altered mental status" removed. The HARD constraint reason uses the reviewer's wording and states that WHO 2025 governs where NICE NG240 diverges (and that NICE excludes asplenia from scope). The governing-source statement is in the constraint reason, not in metadata (ROUND_POLICY forbids review notes in metadata). |
| 690ddd54-22f7-4bed-8d03-328d7a84eedb | FIXED | `required_recommendations[1]`: ampicillin 2 g IV every 4 hours for age over 60, diabetes and asplenia, with the reviewer's point that a negative Listeria PCR does not remove the empirical indication. |
| ba73014b-7f14-4e98-96e9-a86cb3caf5d8 | FIXED | `required_recommendations[0]` replaced by the canonical ceftriaxone/cefotaxime within 60 minutes must with vancomycin conditional. |
| 1b519f0a-f3aa-4663-98b1-ef203ddd28c3 | FIXED | Initial `literature_search` (which reproduced the expected text of action 6) set to null and the literature criterion deleted; penicillin MIC corrected; antigen removed from the CSF and the PCR now answers the LP order inside the index CSF report (`request_pcr_panel` under interpret_labs deleted, so no redundant step 4); HARD constraint satisfiable; WHO 2025 imaging rationale; Listeria cover added; vancomycin no longer mandated; the drug check no longer discusses a non-existent penicillin allergy (tetracycline photosensitivity is stated); blood cultures marked `collected_before_antimicrobials: false` with 2 days of amoxicillin stated. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `followup_outputs` | two drug-interaction follow-ups for one `{}` criterion (ceftriaxone only; dexamethasone only); audiometry filed as BAEP; repeat LP | FIXED: one drug check on the full regimen (allopurinol with ampicillin rash, metformin hold, steroid hyperglycemia, aspirin with dexamethasone and no PPI, lisinopril, oral amoxicillin stop, tetracycline allergy, eGFR about 60); dexamethasone follow-up, audiometry and repeat LP deleted; hearing must added |
| B | minor | `patient.history_present_illness` | "seen by his PCP the day prior" (1 day of amoxicillin) against the medication list "started 2 days ago" | FIXED: "seen by his primary care physician two days ago" |
| B | minor | `patient.neurological_exam.mental_status` | "Alert but confused" with E3 in GCS 13 and "difficult to arouse" in the HPI | FIXED: "Drowsy and confused; opens eyes to voice." |
| B | minor | index CSF | ratio 0.19 from blood 168 (labs 167), reference ">0.6"; RBC 2 "likely traumatic"; Gram stain speculation; culture "preliminary no growth at 24 hours" at the time of the LP; interpretation repeated the PCR list | FIXED: paired 167, ratio 0.21, canonical strings, culture pending, interpretation reduced to values and pattern |
| B | minor | blood culture | `gram_stain` null; narrowing and interpretability sentences | FIXED |
| B | minor | `labs` | PT 13.6 with INR 1.3; HIV and liver tests ordered but not reported | FIXED: PT 15.0; Liver function panel and HIV-1/2 Ag/Ab non-reactive added |
| C | major | musts, prohibitions, key evidence | template regimen, dexamethasone without stop rule, IDSA criteria, "Do NOT discontinue dexamethasone..." | FIXED: canonical texts (plan C2 A, C4, C5, C17); asplenia vaccination must made specific |
| C | minor | `differential` | boilerplate (viral and HSV moderate, cryptococcal) | FIXED: excluded entities low with the excluding data; sinus-source parameningeal infection added |
| C | minor | `red_herrings` | sinus thickening "on MRI" (no MRI); fluid restriction for hyponatremia | FIXED: points at the CT; volume assessment wording |
| E | minor | `metadata.case_body_concerns` | stale engineering notes (literature reclassification; penicillin-allergy flag now resolved) | FIXED: removed; pearls and difficulty rationale updated |

## Changes, in one paragraph a physician can read before re-reviewing
Labs, blood cultures, CT before LP for asplenia (WHO 2025 A.4; WHO governs where NICE diverges), index LP, then one recommended drug check: only labs are given upfront. The literature block that leaked the scoring key, the repeat LP, the lab-filed PCR, the audiometry and the duplicate drug check are gone. The CSF report carries the PCR result, culture pending, ratio 0.21 against the paired glucose 167 and no antigen. Blood cultures state 2 days of amoxicillin, and penicillin MIC 0.12 is resistant by CLSI meningitis breakpoints. The drug check now reflects his real list (allopurinol with ampicillin, metformin, aspirin, tetracycline allergy). Musts: ceftriaxone plus ampicillin (age, diabetes, asplenia), dexamethasone continued 4 days, narrowing to ceftriaxone alone for 14 days, droplet precautions, asplenia vaccination, hearing assessment. The HPI timeline and the GCS wording are consistent.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation key `[NICE_NG240]` (plan section 5 item 1).

## Open questions for Andrea (judgment calls you could not settle)
- None beyond plan Q3 (WHO 2025 governs over NICE NG240 for asplenia as an imaging trigger).

## Verification
Adversarial verifier, 23 October 2026. Read the whole final case, the notes file and the plan entry.
- All 6 note ids are in the table and each FIXED claim holds: penicillin MIC 0.12 resistant (CLSI meningitis); repeat LP gone and CT before index LP; WHO A.4 asplenia reason with the WHO-over-NICE statement; ampicillin with all three risk factors and the negative-PCR caveat; canonical ceftriaxone must; literature block null and criterion deleted; drug check states the tetracycline allergy; blood cultures flagged as after 2 days of amoxicillin.
- Cross-field checks: GCS 13 = E3 V4 M6 matches "drowsy, opens eyes to voice, follows one-step commands"; HPI timeline (PCP two days ago) matches the medication list; ratio 34.9/167 = 0.21; anion gap 122 - 91 - 18 = 13; eGFR about 60 (CKD-EPI 2021, creatinine 1.3, 68, male) correct; allopurinol-ampicillin rash and metformin hold match the medication list.
- Found (PATTERNS 4, template carry-over): the index CSF was M01's template (72% neutrophils, lactate 6.8, RBC 2, "mildly turbid, slightly yellow-tinged") and the social history repeated M01 and M02 word for word. Changed: CSF neutrophils 86%, lymphocytes 11%, RBC 4 cells/uL (within normal limits), lactate 5.9 mmol/L, appearance "Turbid, colorless" in `cell_count`, `appearance`, `special_tests.csf_lactate`, `interpretation`, and `differential[0]` and `differential[4]` key_features; social history "Lives with his wife in a two-story house", "Former smoker, quit 25 years ago, 20 pack-year history", "One glass of wine with dinner most evenings".
- `perfect_agent.py` ok; `case_io.py check` clean for this case.

## Condition audit (23 October 2026)
- Changed `ground_truth.action_criteria[action-2-order-microbiology].alternatives[0].required_arguments`: removed `before_antimicrobials: true` (specimen and tests kept). Reason: the blood culture report sets `collected_before_antimicrobials: false` because an antimicrobial was taken in the 7 days before collection, so `true` is not the truthful value of the parameter ("whether the specimen is being taken before the first antimicrobial dose") and an agent that orders the cultures truthfully would miss a required criterion. Condition-wide rule settled at the audit: the argument is required only where the report flag is true (16 cases) and absent where it is false (14 cases: M01, M02, M03, M05, P02, P04, RM01, RM03, RP01, RP02, RP03, RP05, RS04, S03). Draw-before-treatment timing stays in the musts and in the SOFT blood-cultures-before-CT constraint where one exists. `perfect_agent.py` and `case_io.py check` clean after the edit.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (6 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients

Re-run: `perfect_agent.py` ok; `case_io.py check` clean for the case; BACT-MEN case guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality 'not_applicable', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 20, ECOG 4 (fallback_tool_outputs.clinical_assessment). Why: rule 3: drowsy and confused (GCS 13), febrile and tachycardic (HR 114); the library's Karnofsky 100 describes a person without disease.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: not testable (drowsy, clinically unstable); timed tests not performed (followup_outputs[4] request_gait_and_balance_timed). Why: rule 3: the stored exam records gait not assessed because of altered mental status and clinical instability.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable (followup_outputs[5] request_levodopa_challenge). Why: rule 3: the library describes a normal gait and postural reflexes in a drowsy patient who could not stand.
- `perform_clinical_assessment {assessment_type: structured_headache_history_ichd3}`: new acute headache with red flags; criteria for a primary headache disorder not met (followup_outputs[6] request_structured_headache_history_ichd3). Why: rule 1 and 3: an acute febrile headache with neck stiffness, vomiting and falling consciousness; the library elicits no red flags.
- `analyze_brain_mri`: diffuse leptomeningeal enhancement and sulcal FLAIR hyperintensity; maxillary sinus mucosal thickening; no complication (fallback_tool_outputs.mri). Why: rule 1 and 3: no MRI is stored; the stored CT shows maxillary sinus mucosal thickening, and an MRI with gadolinium in this patient would not be normal.
- `analyze_eeg {eeg_type: continuous_icu}`: continuous generalised theta-delta slowing; no epileptiform discharges or seizures (followup_outputs[7] request_continuous_icu). Why: rule 3: the patient is drowsy and confused (GCS 13); a normal background contradicts the stored exam.
- `analyze_eeg {eeg_type: ambulatory}`: continuous generalised theta-delta slowing; no epileptiform discharges or seizures (followup_outputs[8] request_ambulatory). Why: rule 3: the patient is drowsy and confused (GCS 13); a normal background contradicts the stored exam.
- `perform_clinical_assessment {assessment_type: cognitive_screen}`: not completed (drowsy, inattentive); disoriented to time (followup_outputs[9] request_cognitive_screen). Why: rule 3: GCS 13, intermittently drowsy and disoriented to date; the library reports MoCA 28/30.
- `order_specialized_test {test_type: neuropsych_battery}`: not completed (reduced arousal, inattention) (fallback_tool_outputs.specialized_test). Why: rule 3: a drowsy, confused patient cannot complete a battery in the average range.
- `order_microbiology {specimen: whole_blood_pcr}`: Streptococcus pneumoniae DNA detected (fallback_tool_outputs.microbiology). Why: rule 3: blood cultures grow S. pneumoniae in 2 of 2 sets, a target of the panel; collected after 2 days of oral amoxicillin.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: supine BP 132/79, HR 114; standing not performed (followup_outputs[10] request_orthostatic_blood_pressure). Why: rule 3: HR 114 and a patient who cannot stand; the library reports HR 68 and 3 minutes of standing.
- `interpret_labs {panels: [peripheral smear]}`: Howell-Jolly bodies, toxic granulation (fallback_tool_outputs.labs['peripheral smear']). Why: rule 2: splenectomy at age 38; stored WBC 18.4 with 13% bands.
- `interpret_labs {panels: [HbA1c]}`: HbA1c 7.3% (fallback_tool_outputs.labs['HbA1c']). Why: rule 2: type 2 diabetes for 5 years on metformin.
- `interpret_labs {panels: [ABG]}`: metabolic acidosis with partial respiratory compensation (fallback_tool_outputs.labs['ABG']). Why: rule 3: stored bicarbonate 18, lactate 3.4 and SpO2 95% in sepsis; the library reports a normal gas.
- `interpret_labs {panels: [serum_osmolality]}`: serum osmolality 260 mOsm/kg (low) (fallback_tool_outputs.labs['serum_osmolality']). Why: rule 3: stored sodium 122 mmol/L (calculated osmolality about 262); the library reports 288 mOsm/kg.
- Case fallback replaced, `analyze_eeg {eeg_type: routine}`: routine EEG now shows continuous generalised theta-delta slowing; no epileptiform discharges or seizures (was a normal awake and drowsy EEG) (fallback_tool_outputs.eeg). Why: rule 3: the patient is drowsy and confused (GCS 13); a normal background contradicts the stored exam.
- Case fallback replaced, `analyze_ecg`: sinus tachycardia at 114 bpm, otherwise normal (was a normal ECG) (fallback_tool_outputs.ecg). Why: presenting heart rate 114 bpm.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
