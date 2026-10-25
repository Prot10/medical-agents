# BACT-MEN-P05
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 5d084eab-ee89-4a4b-856b-f04cbe38e5c3 | FIXED | Differential: "Acute ischemic stroke with status epilepticus" renamed "Acute ischemic stroke with a post-ictal deficit" (`ground_truth.differential[0]`, likelihood high to low with the excluding data); the same "status epilepticus" wording in `prohibited_recommendations[4]` changed too. Red herring 2: "and confirmed on MRI" removed (`red_herrings[1].data_point`), `field_path` now points at the CT findings (`followup_outputs[1].output.findings`). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | patient.history_present_illness | Last sentence stated the management decision ("mandate non-contrast CT head BEFORE lumbar puncture per IDSA 2004") inside the patient block; "She denies known immunodeficiency" for a patient unable to give a history | FIXED: sentence deleted; "No immunodeficiency is recorded" |
| C | major | ground_truth (CT criterion, constraint, musts, prohibition, key evidence) | Imaging decision justified by IDSA 2004 "four criteria" including age >60 and altered mental status | FIXED: class A on a new-onset seizure in an adult and focal signs (WHO 2025 Annex A.4; NICE 1.4.7 agrees); canonical constraint, SOFT blood cultures before CT, label, expected evidence, must and prohibition |
| B | major | initial_tool_outputs.eeg | Seizure (rightward head turn, right arm tonic posturing), right face, arm and plantar signs localise left; the EEG put the focal slowing over the right hemisphere | FIXED: intermittent left hemispheric polymorphic delta slowing, left frontotemporal; criterion expected evidence matches; EEG moved to `followup_outputs[3]` `request_eeg` (optional) |
| B | major | followup_outputs[request_csf_analysis] | Trigger without the LP token, listed before the CT; culture "preliminary growth at 18 hours" in the index report; RBC 3 "likely traumatic"; ratio reference ">0.6"; Gram stain text truncated ("morphology"); pneumococcal latex antigen as confirmation; interpretation concluded | FIXED: trigger `request_lumbar_puncture`, placed after the CT; culture "Pending"; canonical RBC, ratio and lactate strings; "Gram-positive diplococci seen"; antigen removed (C7); panel lists its targets; interpretation states values and results |
| B | major | followup_outputs[request_blood_culture_results] | "No growth at 5 days" for the anaerobic bottles in a report available at 48 hours; penicillin MIC 0.12 "intermediate"; narrowing and interpretability boilerplate | FIXED: trigger `request_blood_cultures`; anaerobic "no growth at 48 hours; final report at 5 days"; identification and susceptibility at 48 hours; penicillin 0.12 resistant and ceftriaxone 0.5 or less susceptible by CLSI meningitis breakpoints; impression per C6 |
| D | minor | initial_tool_outputs.ct | "Incidental" sinus disease (a judgement that pre-empts the red herring) | FIXED: impression is a numbered findings list; "Incidental" removed; moved to `followup_outputs[1]` `request_ct_head` |
| B | minor | initial_tool_outputs.labs | HIV and liver tests ordered by action-1 but absent | FIXED: HIV-1/2 Ag/Ab non-reactive; AST, ALT, ALP, bilirubin, albumin normal |
| C | major | ground_truth.assessment.required_recommendations | Template vancomycin plus ceftriaxone with ampicillin for "age >50"; dexamethasone 0.15 mg/kg without stop rule; pneumococcal antigen in the CSF panel; generic de-escalation; no antiseizure treatment after a documented seizure; no hearing must | FIXED: canonical base regimen, Listeria line (age over 60), dexamethasone with "Continue for 4 days: S. pneumoniae is identified", LP panel without antigen, targeted ceftriaxone alone (penicillin-resistant, ceftriaxone-susceptible; stop ampicillin and vancomycin), antiseizure must (levetiracetam, EEG if consciousness does not improve), conditional contrast MRI if the deficit persists, hearing must |
| C | major | ground_truth.differential | HSV and post-ictal state left "moderate"; brain abscess excluded by an MRI that does not exist and by ring enhancement a non-contrast CT cannot show; TB excluded by "PCR panel negative for Mycobacterium" (not a panel target); Todd paresis coded G40.909 | FIXED: post-CSF likelihoods with the excluding results; abscess key features cite the non-contrast CT and the conditional MRI; TB key features cite course, CSF and organism; Todd paresis coded G83.84 |
| C | minor | followup_outputs[check_empiric_regimen_interactions] | Vancomycin-based regimen, "age >50", rifampin and chloramphenicol alternatives, SIADH commentary | FIXED: ceftriaxone, ampicillin and dexamethasone against amlodipine, rosuvastatin, inhalers and the codeine intolerance; criterion label and expected evidence match; tier stays recommended |
| D | minor | ground_truth.key_clinical_evidence | IDSA "four criteria" line; antigen "individually confirmatory"; De Gans dexamethasone template; WHO template line | FIXED: canonical A must, C5, C17 lines; CSF line without antigen |
| A | minor | citations | `[IDSA_2004]`, `[De_Gans_2002]` and free-text duplicates | FIXED: `[WHO_Meningitis_2025]` (+ `[NICE_NG240]` on the HARD constraint); EEG criterion `[Brouwer_2012]` |
| B | minor | ground_truth.action_criteria[action-6-search-medical-literature], followup_outputs[search_ct_before_lp_and_empiric_antibiotics] | Literature criterion recommended, output teaching IDSA 2004 | FIXED: deleted (plan C9, ruling 5) |
| E | minor | metadata.difficulty_rationale | "5 required tools", AMS as an imaging trigger | FIXED |

## Changes, in one paragraph a physician can read before re-reviewing

Only the blood panel is given upfront (now with HIV non-reactive and liver tests). The pathway is blood
cultures (S. pneumoniae in 2 of 2 sets at 16 to 17 hours, penicillin MIC 0.12 resistant and ceftriaxone
susceptible by meningitis breakpoints), CT before LP (required because of the new focal seizure and the
right-sided focal signs, WHO 2025 Annex A.4), the index LP (2240 cells, ratio 0.17, Gram-positive
diplococci, PCR S. pneumoniae, culture pending, antigen removed), an optional EEG now lateralised to
the left hemisphere like the seizure and the deficits, and the drug check. The IDSA sentence was removed
from the HPI. Musts: ceftriaxone within 60 minutes with ampicillin for age over 60, dexamethasone
continued 4 days for S. pneumoniae, narrowing to ceftriaxone alone, antiseizure treatment, contrast MRI
if the deficit persists, droplet precautions, sodium, audiology. The stroke differential now reads
"with a post-ictal deficit", the MRI reference in the sinus red herring is gone, and the literature step
is deleted.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- None specific to this case.

## Open questions for Andrea (judgment calls you could not settle)

- The persistent right-sided deficit in pneumococcal meningitis could reflect infarction or cerebritis; I added a conditional must (contrast MRI if the deficit persists beyond the post-ictal period) rather than a scored MRI criterion, because the case has no MRI report. If Andrea wants it scored, an MRI report needs authoring.

## Verification

Adversarial verifier, 23 October 2026. Checked: note 5d084eab against the final file ("Acute ischemic stroke with a post-ictal deficit" in the differential and in `prohibited_recommendations[4]`; "and confirmed on MRI" gone; the sinus red herring points at `followup_outputs[1].output.findings`, which resolves to the CT); EEG slowing now left-sided, concordant with the rightward version seizure, right face, arm and plantar signs; CT before LP justified by new-onset seizure and focal signs (WHO A.4, NICE 1.4.7) and served before the index LP; CLSI meningitis interpretation (penicillin 0.12 resistant, ceftriaxone 0.5 or less susceptible, meropenem 0.25 or less susceptible); narrowing to ceftriaxone with ampicillin stopped; ratio 19/112 = 0.17; anion gap 128 - 94 - 19 = 15 with lactate 3.9; Todd paresis G83.84; Listeria cover on age 64; inhaled steroids not counted as immunocompromise; `[Brouwer_2012]` on the EEG criterion is on the criteria-pack allow-list.

Found and changed:
- The same "status epilepticus" claim the reviewer ruled out survived in `red_herrings[0].intended_effect` ("... acute ischemic stroke (left MCA territory) or status epilepticus as the primary diagnosis"): the 90-second self-terminating seizure is not status epilepticus. Now "... or a primary seizure disorder as the diagnosis".

After the edit: `perfect_agent.py BACT-MEN-P05 -v` passes (action-3 <- `request_lumbar_puncture`, after the CT); `case_io.py check` clean for the case.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (7 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients

Re-run: `perfect_agent.py` ok; `case_io.py check` clean for the case; BACT-MEN case guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality 'not_applicable', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- follow-up EEG `request_eeg`: `eeg_type` set to `routine`, named in the report's own text.
- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 20, ECOG 4 (fallback_tool_outputs.clinical_assessment). Why: rule 3: GCS 11 after a focal-onset seizure, febrile and tachycardic (HR 118); the library's Karnofsky 100 describes a person without disease.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: not testable (GCS 11, unable to walk safely) (followup_outputs[5] request_gait_and_balance_timed). Why: rule 3: the stored exam records gait not assessed; unable to ambulate safely.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no parkinsonian signs; right pyramidal signs; challenge not performed (followup_outputs[6] request_levodopa_challenge). Why: rule 3: the library describes a normal motor examination and gait in a confused patient with right-sided weakness.
- `perform_clinical_assessment {assessment_type: structured_headache_history_ichd3}`: new acute headache with red flags; criteria for a primary headache disorder not met (followup_outputs[7] request_structured_headache_history_ichd3). Why: rule 1 and 3: an acute febrile headache with neck stiffness, confusion and a seizure; the library elicits no red flags.
- `analyze_brain_mri`: leptomeningeal enhancement greater on the left; subtle left frontotemporal cortical signal change; sinus disease (fallback_tool_outputs.mri). Why: rule 1 and 3: no MRI is stored; the stored CT shows sinus disease, the stored EEG left hemispheric slowing and the exam right-sided signs, so an MRI with gadolinium would not be normal.
- `analyze_eeg {eeg_type: continuous_icu}`: generalised delta slowing with left frontotemporal focal slowing; no epileptiform discharges or seizures (followup_outputs[8] request_continuous_icu). Why: rule 3: GCS 11 and the stored routine EEG shows generalised and left hemispheric delta slowing; the library reports a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: generalised delta slowing with left frontotemporal focal slowing; no epileptiform discharges or seizures (followup_outputs[9] request_ambulatory). Why: rule 3: GCS 11 and the stored routine EEG shows generalised and left hemispheric delta slowing; the library reports a normal background.
- `perform_clinical_assessment {assessment_type: cognitive_screen}`: not completed (encephalopathy, paraphasic speech) (followup_outputs[10] request_cognitive_screen). Why: rule 3: the stored exam states she cannot participate in formal cognitive testing; the library reports MoCA 28/30.
- `order_specialized_test {test_type: neuropsych_battery}`: not completed (encephalopathy) (fallback_tool_outputs.specialized_test). Why: rule 3: the stored exam states she cannot participate in formal cognitive testing.
- `order_specialized_test {test_type: speech_language_evaluation}`: paraphasic speech with impaired naming, repetition and comprehension (followup_outputs[11] request_speech_language_evaluation). Why: rule 3: the stored exam records disorganised speech with paraphasic substitutions.
- `order_microbiology {specimen: whole_blood_pcr}`: Streptococcus pneumoniae DNA detected (fallback_tool_outputs.microbiology). Why: rule 3: blood cultures grow S. pneumoniae in 2 of 2 sets with no recent antibiotics; it is a target of the panel.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: supine BP 148/86, HR 118; standing not performed (followup_outputs[12] request_orthostatic_blood_pressure). Why: rule 3: GCS 11 with HR 118; the library reports HR 68 and 3 minutes of standing.
- `interpret_labs {panels: [ABG]}`: metabolic acidosis with hypoxaemia (pO2 61) (fallback_tool_outputs.labs['ABG']). Why: rule 3: SpO2 91-92% on room air, RR 22, stored bicarbonate 19 and lactate 3.9 in a patient with COPD; the library reports a normal gas.
- `order_specialized_test {test_type: respiratory_function}`: not performed (unable to cooperate) (followup_outputs[13] request_respiratory_function). Why: rule 2 and 3: COPD GOLD stage II and a confused patient (GCS 11); the library reports normal spirometry.
- `interpret_labs {panels: [serum_osmolality]}`: serum osmolality 270 mOsm/kg (low) (fallback_tool_outputs.labs['serum_osmolality']). Why: rule 3: stored sodium 128 mmol/L (calculated osmolality about 271); the library reports 288 mOsm/kg.
- Case fallback replaced, `analyze_eeg {eeg_type: routine}`: repeat routine EEG now shows generalised delta slowing with left frontotemporal focal slowing (was a normal awake and drowsy EEG) (fallback_tool_outputs.eeg). Why: the stored routine EEG and the exam (GCS 11) show an encephalopathic record; a normal repeat recording contradicts them.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
