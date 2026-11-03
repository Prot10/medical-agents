# BACT-MEN-RS02
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 4f49ce3e-d3e3-4e3c-b82e-d8b1924cb62e | FIXED | (1) Shunt tap: the `interpret_labs` `request_shunt_evaluation` block (8 cells, protein 52, glucose 58) is replaced by an `analyze_csf` follow-up `request_shunt_tap` with a plausible ventriculo-lumbar gradient and sterile culture, the reviewer's first option (410 cells/microL, 88% neutrophils, protein 96 mg/dL, glucose 41 mg/dL, ratio 0.30, Gram stain negative, no growth at 48 hours, held 10 days). The "after 48 hours of therapy" option was not taken because ruling 4 forbids reports of treatment the agent has not recommended. A must asks for neurosurgical shunt assessment with a reservoir tap (IDSA 2017). (2) CT: the post-contrast enhancement finding is removed (`contrast_used` stays false because the criterion orders a non-contrast CT); impression reduced to findings, LP-safety sentence deleted. (3) GCS and imaging criteria: `patient.neurological_exam.mental_status` now E2 V3 M4 = 9 with matching text (eyes open to pain, inappropriate words, withdraws), `motor` and `coordination` rewritten to what can be examined at GCS 9, with the left deficits recorded as chronic and unchanged; the CT stays required (WHO 2025 Annex A.4, GCS below 10) with the canonical label, must, prohibition and HARD constraint ("NICE NG240 does not cover this patient (intracranial shunt)"), plus the SOFT blood cultures before CT constraint; "age >60" and the other non-criteria are gone. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | CT and MRI findings | Encephalomalacia placed in the LEFT frontoparietal region (with left ventricular ex-vacuo dilatation) in a patient with a chronic LEFT spastic hemiparesis, left extensor plantar and left facial weakness | FIXED: right frontoparietal in both reports, right lateral ventricle ex-vacuo; MRI additional observation on ventricular size made consistent |
| B | minor | patient.neurological_exam.cranial_nerves | "Hearing grossly intact" untestable at GCS 9 | FIXED: "Startles to a loud voice bilaterally." |
| B | major | initial_tool_outputs.labs | CBC differential 101%; "possible SIADH" interpretation in the summary; HIV and liver tests ordered but absent (C12) | FIXED: neutrophils 83, monocytes 2 added; "Sodium 131 mEq/L (low)"; LFTs and HIV-1/2 Ag/Ab non-reactive added; confirmed served |
| B/D | major | index CSF (was `initial_tool_outputs.csf`) | Index CSF in the initial work-up with culture already isolated, "likely traumatic" for 5 RBC, ratio reference ">0.6", latex antigen, organism inference in the interpretation (C1, C7) | FIXED: follow-up `request_lumbar_puncture` after the CT; culture "Pending"; canonical RBC, ratio and lactate strings; antigen removed; values-and-pattern interpretation |
| D | major | initial_tool_outputs.mri | MRI in the initial work-up; impression concluding "without evidence of ... associated infection" of the shunt (C13) | FIXED: follow-up `request_mri_brain_contrast`; impression findings only; ventricular debris and ependymal enhancement stated as absent; label and expected evidence specific to the shunted patient (IDSA 2017 citation added) |
| B | major | blood culture follow-up | "the isolate is interpretable" reasoning; no interval; serotype reported on a blood culture (reference-lab result) | FIXED: impression per C6 with 14 and 16 hours, serotype removed, gram_stain filled, CLSI meningitis breakpoint noted |
| C | major | followups `request_repeat_lp`, `request_pcr_panel`, `request_audiometry`, literature | post-treatment repeat LP, CSF PCR filed under labs, audiometry as `baep`, literature criterion expecting IDSA 2004 (C1, C8, C9) | FIXED: all deleted with the literature criterion; hearing must added |
| C | major | ground_truth.assessment | template vancomycin plus ceftriaxone, template dexamethasone prohibition, neurosurgery must without content (C4, C5) | FIXED: canonical base must, dexamethasone with "Continue for 4 days: Streptococcus pneumoniae is identified", targeted must (ceftriaxone or benzylpenicillin, 14 days), shunt assessment must (IDSA 2017), recurrent-meningitis work-up and vaccination must |
| C | major | check_drug_interactions | checked dexamethasone only, cited IDSA guidelines | FIXED: ceftriaxone plus dexamethasone against ibuprofen and multivitamin; recommended tier with concrete expected evidence |
| C | major | ground_truth.differential | shunt infection "high" and HSV "moderate" after S. pneumoniae in blood and CSF; TB, cryptococcal and SAH boilerplate (C10) | FIXED: five entries, all low with excluding data; CoNS spelled out |
| D | minor | red_herrings | chronic left deficits undeclared, readable as new focal signs | FIXED: `red_herrings[1]` added; shunt red herring now says ceftriaxone with dexamethasone, not vancomycin plus ceftriaxone |
| B | minor | fallback_tool_outputs.eeg | normal awake EEG with sleep spindles in a GCS 9 patient | FIXED: generalised slowing; `metadata.fallback_tool_kinds.eeg` set to `abnormal_encephalopathy` |
| B | minor | citations | `[IDSA_2004]` and free-text duplicates | FIXED |
| C | minor | ground_truth.diagnosis.accepted | "community acquired bacterial meningitis" appended to a shunted patient | FLAGGED: correct here (shunt last revised 24 years ago, community onset); no change |

## Changes, in one paragraph a physician can read before re-reviewing
The patient is now recorded at GCS 9 (E2 V3 M4) with an examination written for that level, so a non-contrast CT before lumbar puncture is required on WHO 2025 Annex A.4 (GCS below 10); his left hemiparesis and extensor plantar are chronic and declared as a red herring, and the encephalomalacia that explains them is now on the right in both CT and MRI. The pathway runs blood cultures (S. pneumoniae at 14 and 16 hours), CT (findings only, no enhancement on a non-contrast study), the index LP (Gram-positive diplococci, S. pneumoniae on the panel, culture pending), contrast MRI (purulent leptomeningitis without ventriculitis, abscess, empyema or hydrocephalus), a shunt reservoir tap (inflamed ventricular CSF less than lumbar, sterile), and a drug check (stop ibuprofen during dexamethasone). The repeat LP, PCR-as-lab, audiometry and literature steps are gone. Management: ceftriaxone within 60 minutes, dexamethasone for 4 days (pneumococcus), 14 days of ceftriaxone or benzylpenicillin, neurosurgical shunt assessment, droplet precautions until meningococcus is excluded, work-up for CSF leak and immunodeficiency after a second pneumococcal meningitis, vaccination and audiology.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation key `[IDSA_2017_HCVM]` used on the MRI criterion (plan section 5 item 1).

## Open questions for Andrea (judgment calls you could not settle)
- The shunt tap has no action criterion (the CSF criterion's arguments cannot tell a shunt tap from the LP); it is a must and a follow-up served to an `analyze_csf` call that names the shunt tap. If shunt sampling should be scored, the vocabulary needs a distinguishing CSF source term.

## Verification
Adversarial check (23 October 2026) of the log against the case file, the plan (4.0 row RS02: imaging A on GCS below 10 after the record fix) and note 4f49ce3e. Read the whole final case. Confirmed: all three parts of the note are applied (shunt tap as `analyze_csf` `request_shunt_tap` with a plausible gradient and sterile culture; no enhancement on the non-contrast CT, LP-safety sentence gone; GCS 9 = E2 V3 M4 with mental status, motor, coordination, gait and cranial nerve text consistent with it, chronic left deficits declared as a red herring). The worker's laterality correction is right: right frontoparietal encephalomalacia now explains the chronic left hemiparesis in both CT and MRI, and the shunt enters from the right. Index CSF served to action-3 by `request_lumbar_puncture`; HARD and SOFT constraints match plan C2 A; NICE correctly stated as not covering a shunted patient; CBC differential 100%; anion gap 12; blood culture `collected_before_antimicrobials` true is correct (no antimicrobials in the history); pneumococcal MICs read with CLSI meningitis breakpoints.
Found and changed: (1) The CT said "ventricles are within normal limits" while the MRI reports mild ex-vacuo dilatation of the right lateral ventricle from the same encephalomalacia; `followup_outputs[1].output.additional_observations[0]` now reads "No hydrocephalus; ventricles normal in size apart from mild ex-vacuo dilatation of the right lateral ventricle". (2) `metadata.difficulty_rationale` still said the "device/CSF-leak context demands broader empiric coverage", contradicting the case's own regimen (ceftriaxone, community-acquired) and its first red herring; it now says the shunt needs neurosurgical assessment in parallel while the empirical regimen stays the community-acquired one. Not changed: the MRI criterion's `protocol: standard` argument (pre-existing, used in about 100 cases). `perfect_agent.py -v` passes; `case_io.py check` clean for the case.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (6 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients

Re-run: `perfect_agent.py` ok; `case_io.py check` clean for the case; BACT-MEN case guards pass; synonym `--check` clean.

## Central vocabulary wired (24 Oct 2026)
- Core term `analyze_csf.source` `shunt_tap`: new recommended criterion `action-7-analyze-csf-shunt-tap` (`source: shunt_tap`, IDSA 2017 rationale) after the contrast MRI, served by the existing follow-up `request_shunt_tap` (`source` is not a MockServer discriminator; the trigger tokens route it, confirmed by `-v`). The neurosurgical shunt-assessment must is kept unchanged.
- Re-run: `perfect_agent.py -v` ok; `case_io.py check`: schema OK, synonym guard OK, no test failure names the case.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality 'MRI', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 20, ECOG 4 (fallback_tool_outputs.clinical_assessment). Why: rule 3: GCS 9, febrile (39.8 C) and tachycardic (HR 112); the library's Karnofsky 100 describes a person without disease.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: not testable (GCS 9, unable to stand) (followup_outputs[6] request_gait_and_balance_timed). Why: rule 3: the stored exam records gait not assessable because the patient is too somnolent and unsteady to stand.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable (followup_outputs[7] request_levodopa_challenge). Why: rule 3: the library describes a full normal motor examination and gait in an obtunded patient with a chronic left spastic hemiparesis.
- `perform_clinical_assessment {assessment_type: structured_headache_history_ichd3}`: new acute headache with red flags; criteria for a primary headache disorder not met (followup_outputs[8] request_structured_headache_history_ichd3). Why: rule 1 and 3: an acute febrile headache unlike his usual headaches with neck stiffness and falling consciousness; the library elicits no red flags.
- `analyze_eeg {eeg_type: sleep_deprived}`: continuous generalised theta-delta slowing; no epileptiform discharges or seizures (followup_outputs[9] request_sleep_deprived). Why: rule 3: GCS 9 and the stored routine EEG shows continuous generalised slowing; the library reports a normal background.
- `analyze_eeg {eeg_type: continuous_icu}`: continuous generalised theta-delta slowing; no epileptiform discharges or seizures (followup_outputs[10] request_continuous_icu). Why: rule 3: GCS 9 and the stored routine EEG shows continuous generalised slowing; the library reports a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: continuous generalised theta-delta slowing; no epileptiform discharges or seizures (followup_outputs[11] request_ambulatory). Why: rule 3: GCS 9 and the stored routine EEG shows continuous generalised slowing; the library reports a normal background.
- `perform_clinical_assessment {assessment_type: cognitive_screen}`: not testable (GCS 9) (followup_outputs[12] request_cognitive_screen). Why: rule 3: the stored exam states cognitive testing is not possible (GCS 9); the library reports MoCA 28/30.
- `order_specialized_test {test_type: neuropsych_battery}`: not testable (reduced consciousness) (fallback_tool_outputs.specialized_test). Why: rule 3: an obtunded patient cannot complete a battery in the average range.
- `order_specialized_test {test_type: speech_language_evaluation}`: not testable (GCS 9) (followup_outputs[13] request_speech_language_evaluation). Why: rule 3: the stored exam records speech limited to inappropriate words; the library reports normal speech and language.
- `order_microbiology {specimen: whole_blood_pcr}`: Streptococcus pneumoniae DNA detected (fallback_tool_outputs.microbiology). Why: rule 3: blood cultures grow S. pneumoniae in 2 of 2 bottles, a target of the panel; no antibiotics before presentation.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: supine BP 142/88, HR 112; standing not performed (followup_outputs[14] request_orthostatic_blood_pressure). Why: rule 3: vitals HR 112 in an obtunded patient who cannot stand; the library reports HR 68 and 3 minutes of standing.
- `order_advanced_imaging {modality: perfusion_MRI}`: non-perfused encephalomalacia; sulcal hyperperfusion (fallback_tool_outputs.advanced_imaging). Why: rule 3: the stored MRI shows chronic right frontoparietal encephalomalacia and diffuse leptomeningitis; the library reports symmetric normal perfusion.
- `order_advanced_imaging {modality: MR_spectroscopy}`: reduced metabolites in the encephalomalacia (followup_outputs[15] request_mr_spectroscopy). Why: rule 3: the stored MRI shows chronic right frontoparietal encephalomalacia; the library reports normal metabolite ratios.
- `order_advanced_imaging {modality: FDG_PET}`: right frontoparietal hypometabolism (followup_outputs[16] request_fdg_pet). Why: rule 3: the stored MRI shows chronic right frontoparietal encephalomalacia; the library reports a normal brain FDG-PET.
- `order_advanced_imaging {modality: amino_acid_PET}`: photopenic encephalomalacia; no increased uptake (followup_outputs[17] request_amino_acid_pet). Why: rule 3: the stored MRI shows chronic right frontoparietal encephalomalacia; the library reports a normal brain.
- `order_advanced_imaging {modality: perfusion_SPECT}`: right frontoparietal perfusion defect (followup_outputs[18] request_perfusion_spect). Why: rule 3: the stored MRI shows chronic right frontoparietal encephalomalacia; the library reports a normal study.
- `order_advanced_imaging {modality: DTI_tractography}`: thinned right corticospinal tract at the encephalomalacia (followup_outputs[19] request_dti_tractography). Why: rule 3: chronic right frontoparietal encephalomalacia with a left spastic hemiparesis; the library reports intact symmetric tracts.
- `order_advanced_imaging {modality: functional_MRI}`: altered right motor activation; left language dominance (followup_outputs[20] request_functional_mri). Why: rule 3: chronic right frontoparietal encephalomalacia with a left spastic hemiparesis; the library reports normal motor somatotopy.
- `order_advanced_imaging {modality: CT_perfusion}`: no territorial deficit; encephalomalacia non-perfused (followup_outputs[21] request_ct_perfusion). Why: rule 3: the stored CT shows chronic right frontoparietal encephalomalacia; the library reports a normal study.
- `order_body_imaging {study: chest_xray}`: clear lungs; continuous shunt tubing (fallback_tool_outputs.body_imaging). Why: rule 2: ventriculoperitoneal shunt since age 2, revised at 14; the library report omits the shunt tubing.
- `order_body_imaging {study: pelvis_abdomen_CT}`: distal shunt catheter in place; no pseudocyst or collection (followup_outputs[22] request_pelvis_abdomen_ct). Why: rule 2: ventriculoperitoneal shunt; the library reports a normal abdomen without the catheter.
- `order_body_imaging {study: chest_abdomen_pelvis_CT}`: shunt in place without complication; otherwise normal (followup_outputs[23] request_chest_abdomen_pelvis_ct). Why: rule 2: ventriculoperitoneal shunt; the library reports a normal study without the catheter.
- Case fallback replaced, `analyze_ecg`: sinus tachycardia at 112 bpm, otherwise normal (was a normal ECG) (fallback_tool_outputs.ecg). Why: presenting heart rate 112 bpm.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
