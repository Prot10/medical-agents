# BACT-MEN-M01
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 3f36b65f-bd2d-492b-a0f3-52f4fd4b55ed | FIXED | `patient.history_present_illness`: "worst headache of his life" rephrased to "a severe, rapidly worsening diffuse headache" (rephrase option chosen: SAH is not an intended red herring). SAH differential key_features now explains the faint yellow tinge (protein 153 mg/dL), CT and RBC 2. |
| 0b3c686b-9355-48de-8b37-9f2b8f10512d | FIXED | Allergy field keeps "No known drug allergies"; drug-interaction follow-up `warnings[0]` now "No known drug allergies; beta-lactam allergy history explicitly investigated and negative." (penicillin-rash sentence deleted). |
| 287dc755-179b-4e4f-a5e9-827ed5d04837 | FIXED | `patient.neurological_exam.mental_status` states the progressive fall (alert at baseline, drowsy and confused by the evening, difficult to rouse in the morning, GCS 12 on arrival). Imaging decision rests on WHO 2025 A.4 severe immunocompromise (asplenia, untreated hypogammaglobulinemia); the constraint reason records that NICE NG240 excludes immunodeficiency from scope but its 1.4.7 progressive-fall limb is also met. |
| 607514ae-6b9c-4540-8437-cba254ec14cb | FIXED | Post-treatment `request_repeat_lp` follow-up deleted (no indication: improving patient). Index CSF moved from `initial_tool_outputs.csf` to `followup_outputs[2]` (`request_lumbar_puncture`) after the CT, so the HARD CT-before-CSF constraint holds in the pathway. |
| 48cfc7b4-7b9d-46dc-bf38-0d9597053aed | FIXED | CT (`followup_outputs[1]`): "No contraindication to lumbar puncture identified" deleted; impression states findings only (no mass, shift, cistern effacement, hydrocephalus, haemorrhage; maxillary sinus thickening). CSF no longer in the initial work-up. |
| 5b00931d-6c6b-4ef2-90be-f01e6e073737 | FIXED | Drug-interaction output `proposed` = ceftriaxone 2 g IV every 12 hours + ampicillin 2 g IV every 4 hours + dexamethasone 10 mg IV every 6 hours; vancomycin only as a conditional alternative; vancomycin trough, rifampin and chloramphenicol text deleted. Listeria must added. |
| 7a7f4ab9-524e-42cb-b50c-3fb8c51652de | FIXED | The proposed management wording became musts (`required_recommendations[0]` base regimen with conditional vancomycin, `[1]` ampicillin for immunocompromise). The DDI criterion (`action-5`) label now checks that regimen against his medicines, allergy history and renal function. |
| 657dd5f2-3c47-44dc-bf09-8292240d0237 | FIXED | Red herring "Low-grade fever (38.4 C)" withdrawn (HPI records 38.9 with rigors). Sinus red herring now points at the CT (`followup_outputs[1].output.additional_observations`), not a non-existent MRI. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.sequence_constraints`, CT criterion, must, prohibition, key evidence | IDSA 2004 imaging list ("age >60", "altered mental status") | FIXED: WHO 2025 A.4 canonical texts (plan C2 A); soft constraint blood cultures before CT added; citations `[IDSA_2004]` replaced by `[WHO_Meningitis_2025]` everywhere (criteria, avoided actions) |
| C | major | `assessment.required_recommendations` | template vancomycin + ceftriaxone, no Listeria cover, dexamethasone without stop rule, no hearing must | FIXED: canonical base, Listeria, dexamethasone (continue 4 days, pneumococcus), targeted (ceftriaxone or benzylpenicillin 14 days), hearing must; asplenia must adds MenB and immunology review for immunoglobulin replacement after a second invasive pneumococcal infection |
| C | minor | `assessment.prohibited_recommendations` | template "Do NOT discontinue dexamethasone solely because the Gram stain is negative" | FIXED: deleted (plan C5); LP prohibition replaced by the canonical A text |
| B | major | `followup_outputs` | Index CSF in initial work-up; `request_pcr_panel` (CSF PCR filed under interpret_labs), `request_audiometry` (audiometry as BAEP), literature follow-up | FIXED: PCR result folded into the index CSF report; audiometry and literature follow-ups and the literature criterion deleted (rulings 4 and 5; plan C8, C9) |
| B | major | blood culture follow-up | `collected_before_antimicrobials: true` and "taken before the first antimicrobial dose" after 2 days of amoxicillin; `gram_stain` null though ordered | FIXED: false with one-line statement; impression with set count and intervals; Gram stain line added; CLSI meningitis breakpoint wording on susceptibilities |
| B | minor | index CSF `glucose_ratio`, `glucose` | ratio 0.24 matches neither paired glucose (142 in CSF, 137 in labs); reference ">0.6" | FIXED: one paired blood glucose 137 (lab value), ratio 0.22, WHO reference |
| B | minor | index CSF RBC, lactate, Gram stain, interpretation | RBC 2 "likely traumatic"; lactate reference without "local"; Gram stain partial-treatment speculation; latex antigen used as confirmation | FIXED: canonical strings; antigen line removed (not ordered; WHO 2025 does not recommend antigen tests); interpretation reduced to values and pattern |
| B | minor | `patient.neurological_exam.mental_status` | "follows simple one-step commands inconsistently" contradicts M5 in GCS 12 (E3 V4 M5) | FIXED: "does not follow one-step commands; he localizes to supraorbital pressure" |
| B | minor | `initial_tool_outputs.labs` | action-1 orders HIV and CMP but no HIV or liver tests reported | FIXED: added Liver function panel (normal) and HIV-1/2 Ag/Ab non-reactive |
| C | minor | `red_herrings[1].correct_interpretation` | prescribed "fluid restriction" for hyponatremia, not supported by current meningitis guidance | FIXED: volume assessment and cautious correction while the infection is treated |
| C | minor | `differential` | boilerplate (viral and HSV moderate) after a pneumococcal CSF | FIXED: viral and HSV low with excluding data; cryptococcal (panel negative, not an immunodeficiency of that kind) replaced by sinus-source parameningeal infection (the CT finding the case raises); TB and SAH very low |
| B | minor | `key_clinical_evidence` | C17 template lines (IDSA criteria, vancomycin, Gram stain 60-90%, ratio <0.4, De Gans dexamethasone); duplicated WHO timing line | FIXED: canonical replacements; duplicate deleted |
| B | minor | `avoid-waste-2-order-echocardiogram` | rationale "No evidence of endocarditis as a primary source" read oddly beside a bacteraemic case; citation IDSA | FIXED: rationale "not part of the meningitis work-up; nothing in the case suggests endocarditis" (kept waste); all avoided-action citations now `[WHO_Meningitis_2025]` |
| E | minor | `metadata.clinical_pearls`, `difficulty_rationale` | latex agglutination pearl; "5 required tools; 4 red herrings" | FIXED |

## Changes, in one paragraph a physician can read before re-reviewing
The work-up now starts from the presentation: labs, blood cultures, then CT before LP (WHO 2025 A.4 severe immunocompromise from asplenia and untreated hypogammaglobulinemia; HARD constraint), then the index LP, then a recommended drug-interaction check. Only labs are given as the initial work-up. The repeat LP, the CSF PCR filed as a lab, the audiometry filed as BAEP and the literature search are gone; the PCR result now sits in the index CSF report, which reads culture pending, ratio 0.22 against the paired blood glucose of 137, RBC within normal limits and lactate against a local reference, with no partial-treatment comment and no antigen test. The blood culture report states that 2 days of oral amoxicillin preceded collection. The musts give ceftriaxone with ampicillin (immunocompromise) and dexamethasone continued 4 days for the pneumococcus, CT after cultures and first dose, narrowing to ceftriaxone or benzylpenicillin for 14 days, droplet precautions, vaccination and immunology review, and a hearing assessment. The progressive fall in consciousness is stated in the examination. The SAH-type headache wording, the contradicted fever red herring and the penicillin-rash sentence are gone; the differential reflects the results.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys `[NICE_NG240]` used in must texts (plan section 5 item 1).
- Synonym `community acquired bacterial meningitis` is appended (G00); fine here.

## Open questions for Andrea (judgment calls you could not settle)
- NICE NG240 excludes people with immunodeficiency, yet Reviewer 2's note 287dc755 reasons with the NICE 1.4.7 progressive-fall limb for this asplenic patient. The constraint reason states both facts; the musts keep the canonical NICE references for the regimen (concordant with WHO). Confirm this is the intended handling for the immunocompromised cases.
- Bilateral sluggish pupils in the examination could be read as NICE's "abnormal pupillary reactions"; not used as an imaging limb here.

## Verification
Adversarial verifier, 23 October 2026. Read the whole final case, the notes file and the plan entry.
- All 8 note ids are in the table and each FIXED claim holds in the file: headache rephrased; NKDA with the drug-check line; progressive fall in consciousness stated in `mental_status`; repeat LP gone, index CSF is `followup_outputs[2]` after the CT (HARD constraint satisfied); CT impression is findings only; ampicillin in `proposed` and as a must; fever red herring withdrawn; sinus red herring points at the CT.
- Cross-field checks: GCS 12 = E3 V4 M5 and matches the HPI and exam text; ratio 30.7/137 = 0.22 with the lab glucose; anion gap 126 - 96 - 18 = 12 with lactate 3.1; eGFR 75 (CKD-EPI 2021, creatinine 1.15, 55, male) correct; MICs read with CLSI meningitis breakpoints; `collected_before_antimicrobials` false after 2 days of amoxicillin; red-herring paths resolve; constraints use existing ids; no IDSA 2004, "age >", ">0.6", "traumatic", LP-safety or narrowing boilerplate left.
- Found: `metadata.difficulty_description` still described "mixed pleocytosis and borderline values" for a CSF with 72% neutrophils, ratio 0.22 and lactate 6.8. Changed to "CSF modified by prior oral amoxicillin, including a negative Gram stain that could mislead toward viral meningitis". No other change.
- Flagged (class, see M02 and M03 logs): M01, M02 and M03 shared one CSF template (72% neutrophils, lactate 6.8, RBC 2) and one social-history template. M01 is kept as the reference; M02 and M03 were de-duplicated.
- `perfect_agent.py` ok (action-3 answered by `request_lumbar_puncture`); `case_io.py check` clean for this case.

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

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 20, ECOG 4 (fallback_tool_outputs.clinical_assessment). Why: rule 3: drowsy and confused, GCS 12, too somnolent to stand; the library's Karnofsky 100 describes a person without disease.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: not testable (drowsy, unable to stand); timed tests not performed (followup_outputs[4] request_gait_and_balance_timed). Why: rule 3: the stored exam records gait not assessed because the patient is too somnolent to stand.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable (followup_outputs[5] request_levodopa_challenge). Why: rule 3: the library describes a full normal motor examination and gait in a drowsy patient with nuchal rigidity who cannot stand.
- `perform_clinical_assessment {assessment_type: structured_headache_history_ichd3}`: new acute headache with red flags; criteria for a primary headache disorder not met (followup_outputs[6] request_structured_headache_history_ichd3). Why: rule 1 and 3: an acute febrile headache with neck pain, photophobia and falling consciousness; the library elicits no red flags.
- `analyze_brain_mri`: diffuse leptomeningeal enhancement and sulcal FLAIR hyperintensity; maxillary sinus mucosal thickening; no complication (fallback_tool_outputs.mri). Why: rule 1 and 3: no MRI is stored; the stored CT shows maxillary sinus mucosal thickening, and an MRI with gadolinium in this patient would not be normal.
- `analyze_eeg {eeg_type: continuous_icu}`: continuous generalised theta-delta slowing; no epileptiform discharges or seizures (followup_outputs[7] request_continuous_icu). Why: rule 3: the patient is drowsy and confused (GCS 12); the library reports a normal waking background.
- `analyze_eeg {eeg_type: ambulatory}`: continuous generalised theta-delta slowing; no epileptiform discharges or seizures (followup_outputs[8] request_ambulatory). Why: rule 3: the patient is drowsy and confused (GCS 12); the library reports a normal waking background.
- `perform_clinical_assessment {assessment_type: cognitive_screen}`: not completed (drowsy, inattentive); disoriented to place and time (followup_outputs[9] request_cognitive_screen). Why: rule 3: GCS 12, inattentive and disoriented; the library reports MoCA 28/30.
- `order_specialized_test {test_type: neuropsych_battery}`: not completed (reduced arousal, inattention) (fallback_tool_outputs.specialized_test). Why: rule 3: a drowsy, confused patient cannot complete a battery in the average range.
- `order_specialized_test {test_type: speech_language_evaluation}`: dysarthria; language content appropriate; testing limited by drowsiness (followup_outputs[10] request_speech_language_evaluation). Why: rule 3: the stored exam records slow, dysarthric speech.
- `order_microbiology {specimen: whole_blood_pcr}`: Streptococcus pneumoniae DNA detected (fallback_tool_outputs.microbiology). Why: rule 3: blood cultures grow S. pneumoniae in 2 of 2 sets, a target of the panel; collected after oral amoxicillin, so not before antimicrobials.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: supine BP 107/67, HR 106; standing not performed (followup_outputs[11] request_orthostatic_blood_pressure). Why: rule 3: vitals HR 106, BP 107/67 and a patient too somnolent to stand; the library reports HR 68 and 3 minutes of standing.
- `interpret_labs {panels: [peripheral smear]}`: Howell-Jolly bodies, neutrophilia with toxic granulation (fallback_tool_outputs.labs['peripheral smear']). Why: rule 2: splenectomy at age 32; stored WBC 18.0 with 12% bands.
- `interpret_labs {panels: [quantitative_Ig]}`: IgG 410 mg/dL (low) (fallback_tool_outputs.labs['quantitative_Ig']). Why: rule 2: hypogammaglobulinaemia diagnosed 5 years ago, not on replacement.
- `interpret_labs {panels: [IgG_subclasses]}`: IgG1, IgG2, IgG3 low (fallback_tool_outputs.labs['IgG_subclasses']). Why: rule 2: hypogammaglobulinaemia not on replacement.
- `interpret_labs {panels: [ABG]}`: metabolic acidosis with partial respiratory compensation (fallback_tool_outputs.labs['ABG']). Why: rule 3: stored bicarbonate 18, lactate 3.1 and RR 22 in sepsis; the library reports a normal gas.
- `interpret_labs {panels: [serum_osmolality]}`: serum osmolality 266 mOsm/kg (low) (fallback_tool_outputs.labs['serum_osmolality']). Why: rule 3: stored sodium 126 mmol/L (calculated osmolality about 268); the library reports 288 mOsm/kg.
- Case fallback replaced, `analyze_eeg {eeg_type: routine}`: routine EEG now shows continuous generalised theta-delta slowing (was a normal awake and drowsy EEG) (fallback_tool_outputs.eeg). Why: the patient is drowsy and confused (GCS 12); a normal waking background contradicts the stored exam.
- Case fallback replaced, `analyze_ecg`: sinus tachycardia at 106 bpm, otherwise normal (was a normal ECG) (fallback_tool_outputs.ecg). Why: presenting heart rate 106 bpm.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
