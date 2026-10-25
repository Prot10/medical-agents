# BACT-MEN-M02
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| d308acf2-10de-4fbb-bc5a-d0b1d21a218d | FIXED | Allergy field keeps "Contrast dye (mild reaction)". Drug-interaction follow-up rewritten: the penicillin-allergy contraindication is deleted and `warnings[0]` states the recorded allergy is iodinated contrast, no antibiotic allergy, non-contrast CT needs no premedication. |
| 18203dd9-813a-4f7c-9bc1-41eba2c7caa8 | FIXED | `patient.neurological_exam.mental_status` ends "GCS 14 (E4 V4 M6)." The imaging decision no longer rests on "altered mental status": it rests on asplenia (WHO 2025 A.4 severe immunocompromise), and the constraint reason says she is alert, GCS 14, no focal sign. |
| ec012471-c7cc-4e0b-bc6e-32be63a27b0d | FIXED | CT impression now "No mass lesion, midline shift, basal cistern effacement or hydrocephalus. No intracranial hemorrhage." (LP sentence deleted). Index CSF moved out of the initial work-up to `followup_outputs[2]` (`request_lumbar_puncture`), after the CT; the post-treatment repeat LP is deleted. |
| eed97d31-7a7d-4b9e-a852-674e40d85c0d | FIXED | Same edit as d308acf2: `contraindications` emptied of the non-existent penicillin allergy. |
| aedde17d-13ba-4817-aa43-6cd6ee20e34e | FIXED | `proposed` = ceftriaxone 2 g IV every 12 hours + ampicillin 2 g IV every 4 hours + dexamethasone 10 mg IV every 6 hours; vancomycin only as a conditional alternative. Musts: canonical base regimen and Listeria cover for diabetes and asplenia. |
| 258fbb73-7240-4970-a845-b76b667543e1 | FIXED | `differential[0]` = "Meningococcal disease (meningococcal sepsis with or without meningitis)", A39.0, moderate (as the reviewer asked), key_features with the exclusion route (N. meningitidis not detected on CSF PCR, S. pneumoniae in 2 of 2 blood sets). Droplet must rewritten around the rash. |
| f1a4e06a-fa5d-47ee-9477-ca4ffecacad5 | FIXED | HARD constraint reason uses the reviewer's WHO 2025 A.4 wording with "post-traumatic asplenia with incomplete pneumococcal immunisation"; IDSA 2004 removed; SOFT constraint blood cultures before CT added; CT label, must, prohibition and key evidence use the same limb. |
| 17b31064-1cb3-4c0c-b825-3fd2016e74f0 | FIXED | (1) Petechial rash declared as a red herring (`red_herrings[3]`, `patient.neurological_exam.additional`) and meningococcal disease added to the differential; key evidence line on NICE 1.1.9 added. (2) Anion gap: chloride 105 to 92 (gap 13 with lactate 3.2); summary and interpretation updated. (3) IDSA 2004 replaced by WHO 2025 / NICE NG240 throughout. (4) Susceptibility: penicillin MIC 0.12 "Resistant, CLSI meningitis breakpoint", ceftriaxone 0.25 "Susceptible"; the targeted must says it explains the amoxicillin failure and continues ceftriaxone alone for 14 days. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `followup_outputs` | CSF PCR filed as `interpret_labs` `request_pcr_panel`; audiometry as BAEP; literature follow-up and recommended literature criterion | FIXED: PCR result in the index CSF report; the others deleted (plan C1, C8, C9); hearing must added |
| B | major | blood culture follow-up | `collected_before_antimicrobials: true` with "taken before the first antimicrobial dose, so the isolate is interpretable" after 3 days of amoxicillin; narrowing sentence; no intervals; Gram stain null | FIXED: false with one-line statement; set count and intervals (16 and 19 hours; anaerobic no growth at 5 days); Gram stain; narrowing sentence deleted |
| B | minor | index CSF | ratio 0.18 from blood 188 (labs 194), reference ">0.6"; Gram stain partial-treatment speculation; latex antigen; culture turnaround text | FIXED: paired 194, ratio 0.19, WHO reference; canonical RBC and lactate strings; antigen removed; interpretation reduced to values and pattern |
| B | minor | `labs.panels.BMP` Creatinine | male reference range (0.74-1.35) in a woman; 1.25 mg/dL is raised for her | FIXED: female range 0.59-1.04, flagged high; eGFR about 55 (CKD-EPI 2021) used in the drug check (metformin hold, no antibiotic dose change) |
| B | minor | `labs.panels.Coagulation` PT | PT 13.5 (normal) with INR 1.3 | FIXED: PT 15.2 (H) |
| B | minor | `labs` | HIV and liver tests ordered but not reported; low calcium without albumin | FIXED: Liver function panel (albumin 3.3 low, which accounts for calcium 7.9) and HIV-1/2 Ag/Ab non-reactive |
| C | major | musts and prohibitions | template vancomycin regimen, dexamethasone without stop rule, "Do NOT discontinue dexamethasone..." | FIXED: canonical musts (plan C4, C5); prohibition deleted; asplenia must now names PCV completion, MenACWY, MenB, Hib, standby antibiotics |
| D | minor | `patient.history_present_illness` | "far worse than anything she had experienced before" is the SAH descriptor class (PATTERNS C11), undeclared | FIXED: "a severe, rapidly worsening headache that she rated as 9 out of 10" |
| C | minor | `red_herrings[1]` | fluid restriction prescribed for hyponatremia | FIXED: volume assessment and cautious correction |
| C | minor | `differential` | viral and HSV moderate after a pneumococcal CSF; cryptococcal and TB boilerplate | FIXED: excluded entities low with the excluding result; sinus-source parameningeal infection added (chronic sinusitis in the history); cryptococcal and TB removed |
| B | minor | `key_clinical_evidence`, `metadata.clinical_pearls` | C17 template lines; pearl gave de Gans' overall mortality (15% to 7%) as the pneumococcal figure; antigen pearl | FIXED |
| B | minor | avoided actions | `[IDSA_2004]` citations | FIXED: `[WHO_Meningitis_2025]` |

## Changes, in one paragraph a physician can read before re-reviewing
The pathway is now labs, blood cultures, CT (WHO 2025 A.4 severe immunocompromise: post-traumatic asplenia; HARD before LP, SOFT after cultures), the index LP, then a recommended drug check; only labs are given upfront. The repeat LP, the lab-filed PCR, the audiometry and the literature search are gone. The CSF carries the PCR result, culture pending, ratio 0.19 against the paired glucose 194. The blood culture states 3 days of oral amoxicillin, intervals, and CLSI meningitis interpretation (penicillin 0.12 resistant, ceftriaxone 0.25 susceptible). GCS 14 is recorded. The anion gap is corrected (chloride 92), the creatinine has a female reference, PT agrees with INR, and liver tests and HIV are reported. The drug check handles her real issues (metformin hold, steroid hyperglycemia in diabetes, aspirin, contrast allergy irrelevant to the antibiotics). Musts give ceftriaxone with ampicillin, dexamethasone 4 days, narrowing to ceftriaxone alone for 14 days, meningococcal precautions because of the rash, asplenia vaccination and a hearing assessment. The rash is a declared red herring and meningococcal disease is in the differential.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation key `[NICE_NG240]` (plan section 5 item 1).

## Open questions for Andrea (judgment calls you could not settle)
- Meningococcal disease is kept at `moderate` as Reviewer 2 asked, although ROUND_POLICY ruling 7 would put an alternative the work-up excludes at `low`. The key_features state the exclusion. Lower it if ruling 7 should prevail.

## Verification
Adversarial verifier, 23 October 2026. Read the whole final case, the notes file and the plan entry.
- All 8 note ids are in the table and each FIXED claim holds: contrast allergy only, no penicillin-allergy text; GCS 14 (E4 V4 M6) recorded and consistent with "alert, follows one-step commands"; CT impression findings only; ampicillin for diabetes and asplenia; meningococcal disease in the differential with the exclusion route; WHO A.4 asplenia reason in constraint, label, must, prohibition and key evidence; rash declared as red herring; chloride 92 gives anion gap 13; penicillin MIC 0.12 resistant, ceftriaxone 0.25 susceptible (CLSI meningitis).
- Cross-field checks: ratio 36.4/194 = 0.19 with the lab glucose; eGFR 55 (CKD-EPI 2021, creatinine 1.25, 42, female) correct; PT 15.2 with INR 1.3; corrected calcium normal with albumin 3.3; temperature 100.8 F = 38.2 C matches vitals and the fever red herring; PPSV23-only history matches the vaccination must.
- Found (PATTERNS 4, template carry-over): the index CSF repeated M01's numbers exactly (72% neutrophils, 24% lymphocytes, lactate 6.8 mmol/L) and the social history repeated M01 and M03 word for word ("Lives with wife in a single-story home", "civil engineer", "Former smoker, quit 10 years ago, 15 pack-year history"). Changed: CSF neutrophils 81%, lymphocytes 15%, lactate 7.6 mmol/L in `cell_count`, `special_tests.CSF_lactate`, `interpretation` and `differential[1].key_features`; social history "Lives with her wife in a two-story townhouse", "Middle school administrative assistant" (fits the HPI's student contact), "Never smoker". `metadata.difficulty_description` no longer says "mixed pleocytosis" (the CSF is neutrophilic): now "The negative Gram stain could initially suggest a non-bacterial etiology."
- Left as logged: meningococcal disease kept `moderate` (Reviewer 2's explicit request and the plan; the open question to Andrea stands).
- `perfect_agent.py` ok; `case_io.py check` clean for this case.

## Condition audit (23 October 2026)
- Changed `ground_truth.action_criteria[action-2-order-microbiology].alternatives[0].required_arguments`: removed `before_antimicrobials: true` (specimen and tests kept). Reason: the blood culture report sets `collected_before_antimicrobials: false` because an antimicrobial was taken in the 7 days before collection, so `true` is not the truthful value of the parameter ("whether the specimen is being taken before the first antimicrobial dose") and an agent that orders the cultures truthfully would miss a required criterion. Condition-wide rule settled at the audit: the argument is required only where the report flag is true (16 cases) and absent where it is false (14 cases: M01, M02, M03, M05, P02, P04, RM01, RM03, RP01, RP02, RP03, RP05, RS04, S03). Draw-before-treatment timing stays in the musts and in the SOFT blood-cultures-before-CT constraint where one exists. `perfect_agent.py` and `case_io.py check` clean after the edit.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (6 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients
- Meningococcal disease likelihood moderate -> low: assessment-time view (ruling 7); the key features already give Reviewer 2's exclusion route (258fbb73) and the entry stays

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

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 20, ECOG 4 (fallback_tool_outputs.clinical_assessment). Why: rule 3: febrile, tachycardic (HR 119), intermittently confused and unwilling to walk; the library's Karnofsky 100 describes a person without disease.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: not performed (headache, photophobia, confusion); brief supported standing steady (followup_outputs[4] request_gait_and_balance_timed). Why: rule 3: the stored exam records gait not formally assessed because of severe headache and photophobia.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable (followup_outputs[5] request_levodopa_challenge). Why: rule 3: the library describes a normal gait and postural reflexes in a patient who could not walk.
- `perform_clinical_assessment {assessment_type: structured_headache_history_ichd3}`: new acute headache with red flags; criteria for a primary headache disorder not met (followup_outputs[6] request_structured_headache_history_ichd3). Why: rule 1 and 3: an acute febrile headache with photophobia, vomiting and confusion; the library elicits no red flags.
- `analyze_brain_mri`: diffuse leptomeningeal enhancement and sulcal FLAIR hyperintensity; no complication (fallback_tool_outputs.mri). Why: rule 1: no MRI is stored; an MRI with gadolinium in this patient would not be normal (stored CT without mass, shift or hydrocephalus).
- `analyze_eeg {eeg_type: continuous_icu}`: mild generalised theta slowing; no epileptiform discharges or seizures (followup_outputs[7] request_continuous_icu). Why: rule 3: the patient is slowed, inattentive and disoriented (GCS 14); a normal background contradicts the stored exam.
- `analyze_eeg {eeg_type: ambulatory}`: mild generalised theta slowing; no epileptiform discharges or seizures (followup_outputs[8] request_ambulatory). Why: rule 3: the patient is slowed, inattentive and disoriented (GCS 14); a normal background contradicts the stored exam.
- `perform_clinical_assessment {assessment_type: cognitive_screen}`: MoCA 17/30 with inattention and temporal disorientation (followup_outputs[9] request_cognitive_screen). Why: rule 3: the stored exam records impaired attention, repeated questions and a wrong date; the library reports MoCA 28/30.
- `order_specialized_test {test_type: neuropsych_battery}`: not completed (inattention, acute confusion) (fallback_tool_outputs.specialized_test). Why: rule 3: an acutely confused patient cannot complete a battery in the average range.
- `order_microbiology {specimen: whole_blood_pcr}`: Streptococcus pneumoniae DNA detected (fallback_tool_outputs.microbiology). Why: rule 3: blood cultures grow S. pneumoniae in 2 of 2 sets, a target of the panel; collected after 3 days of oral amoxicillin.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: supine BP 102/70, HR 119; standing not performed (followup_outputs[10] request_orthostatic_blood_pressure). Why: rule 3: vitals HR 119 and BP 102/70 in a patient who could stand only briefly; the library reports HR 68 and 3 minutes of standing.
- `interpret_labs {panels: [peripheral smear]}`: Howell-Jolly bodies, toxic granulation (fallback_tool_outputs.labs['peripheral smear']). Why: rule 2: splenectomy at age 32; stored WBC 18.7 with 8% bands and platelets 139.
- `interpret_labs {panels: [serum_osmolality]}`: serum osmolality 268 mOsm/kg (low) (fallback_tool_outputs.labs['serum_osmolality']). Why: rule 3: stored sodium 126 mmol/L (calculated osmolality about 270); the library reports 288 mOsm/kg.
- Case fallback replaced, `analyze_eeg {eeg_type: routine}`: routine EEG now shows mild generalised theta slowing; no epileptiform discharges or seizures (was a normal awake and drowsy EEG) (fallback_tool_outputs.eeg). Why: rule 3: the patient is slowed, inattentive and disoriented (GCS 14); a normal background contradicts the stored exam.
- Case fallback replaced, `analyze_ecg`: sinus tachycardia at 119 bpm, otherwise normal (was a normal ECG) (fallback_tool_outputs.ecg). Why: presenting heart rate 119 bpm.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
