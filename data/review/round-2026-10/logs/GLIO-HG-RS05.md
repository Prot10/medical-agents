# GLIO-HG-RS05
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 79fc1c6f-fcc2-4178-9127-aa995d8f41fe | FIXED | Must 4 "Initiate antiepileptic prophylaxis with levetiracetam ..." replaced by the treat must: "Start antiseizure treatment with levetiracetam for the documented 30-second episode of speech arrest with preserved awareness, a focal aware seizure; this is treatment of tumour-related epilepsy, not prophylaxis. Avoid enzyme-inducing antiseizure drugs ...". EEG waste entry `avoid-waste-1-analyze-eeg` deleted (plan C5). Key evidence item added on the seizure. |
| 65ef42fb-0306-4709-b96d-4bedb0c22502 | FIXED | `molecular_assays` now `IDH1_IHC`, `ATRX_IHC`, `MGMT_methylation` (age 64, MVP and necrosis: plan C4), both alternatives. Tissue reports: IDH1 R132H IHC negative, ATRX retained, MGMT methylated (61%), TERT C228T, EGFR amplified, +7/-10 present, 1p/19q not codeleted. |
| 666dbf49-1fcb-4059-aeab-d1a61ae2c083 | FIXED | New `functional_MRI` follow-up (language left-lateralised, LI 0.71, Wernicke area 4 mm from the margin, task performance partial because of impaired comprehension) and `DTI_tractography` follow-up (arcuate 2 mm and partly infiltrated, optic radiation 3 mm, CST 14 mm); recommended `action-fmri-functional-mapping` and `action-dti-tractography` with soft constraints to tissue. Must 2 is the plan's qualified text: awake language mapping is limited by the comprehension and naming deficits, and the approach is decided after neurosurgical and neuropsychological assessment. Key evidence item 5 rewritten the same way. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | patient.history_present_illness | Outpatient contrast MRI and "Repeat MRI on admission confirms a large left temporal heterogeneously enhancing mass" leak the MRI the agent must order (C8) | FIXED: replaced by a non-contrast CT at urgent care showing a left temporal mass with edema and 5 mm shift; dexamethasone start kept |
| C | major | must 3 | Dexamethasone "administer" although HPI says it was started on admission | FIXED: continue at the lowest effective dose, with glucose monitoring, gastric protection and taper |
| C | major | patient.neurological_exam.mental_status | "Speech output is non-fluent" for a superior/middle temporal and temporoparietal lesion with no frontal involvement (a posterior temporal lesion gives fluent paraphasic aphasia; the HPI describes pauses and word substitutions) | FIXED: "fluent in rate but halting, with long word-finding pauses and frequent phonemic and semantic paraphasic errors"; key evidence item 1 follows |
| C | minor | patient.neurological_exam.cranial_nerves | "Confirmed optokinetic nystagmus asymmetry" does not confirm a superior quadrantanopia | FIXED: parenthetical removed |
| C | minor | initial_tool_outputs.mri FLAIR | Optic radiation placed "in the posterior limb of the internal capsule" (C9) | FIXED: temporal loop (Meyer loop) and sagittal stratum |
| D | minor | initial_tool_outputs.mri.impression, additional_observations | "consistent with the clinical right superior quadrantanopia" (cross-modality); "likely incidental in the setting of long-standing hypertension" with an em dash | FIXED |
| B | major | initial_tool_outputs.labs | Criterion requires `type_and_screen` but the panel had none | FIXED: type and screen row added (clinical_significance null) |
| B/C | major | fallback_tool_outputs.eeg | Normal EEG ("no focal slowing") served for an EEG order in a patient with a 5.4 cm temporal mass and a seizure: impossible | FIXED: focal left temporal polymorphic delta slowing, no epileptiform discharges; `metadata.fallback_tool_kinds.eeg` updated |
| D | minor | fallback ecg, echo, CT CAP | "consistent with long-standing hypertension" on the ECG (cross-modality); em dashes | FIXED |
| A/C | major | action-3 literature criterion, follow-up, stop rule | Literature as a required step (C1) | FIXED: deleted |
| A/D | major | initial_tool_outputs.tissue_diagnosis | Tissue upfront; template meta-text; "(left temporal lobe)" inside the integrated diagnosis; "Microscopic description" as a molecular finding (C2) | FIXED: resection and biopsy follow-ups; site in `site`; Histology row |
| C | major | action-10, surgery must | Stereotactic biopsy only (C3, group A) | FIXED: resection then biopsy |
| C | major | ground_truth | No performance status (C7) | FIXED: recommended; follow-up KPS 70, ECOG 2 |
| C | minor | must 6 | Template Stupp consult (C11) | FIXED: entity, age and KPS specific must |
| C | minor | prohibited_recommendations, DDI warning | Enzyme-inducing antiseizure drugs said to "reduce temozolomide efficacy via CYP450 induction"; temozolomide is not CYP-metabolised (spontaneous hydrolysis); the interaction is with dexamethasone and other anticancer drugs | FIXED: wording corrected in the prohibition and the DDI output |
| D | major | action-9 expected_evidence | Repeated verbatim in the DDI output (leak guard failure) | FIXED: rewritten from the case's interactions (aspirin, dexamethasone); amlodipine interaction added to the output; criterion stays optional and last |
| C | minor | differential | Lymphoma left low after glial tissue | FIXED: very low; metastasis key features mention smoking and tissue |
| C | minor | action-1, -2, -6, -7, -8 | Template evidence with an em dash; label-copy rationales; `[Stupp_2005]` on MRI | FIXED |
| C | minor | avoided_actions, sequence_constraints, stop_rule | Templates | FIXED per plan section 3 |
| B | minor | metadata.difficulty_rationale | Counts out of date | FIXED |

## Changes, in one paragraph a physician can read before re-reviewing
The HPI no longer gives away the MRI: an urgent care non-contrast CT shows a left temporal mass with oedema and 5 mm shift. The pathway is contrast MRI, perfusion, spectroscopy, optional body CT, labs (now with the type and screen the criterion asks for), performance status (KPS 70, ECOG 2), functional MRI and DTI (Wernicke area 4 mm and arcuate fasciculus 2 mm from the tumour, with task performance limited by his comprehension deficit), then tissue by maximal safe resection or biopsy, with IDH1 R132H, ATRX and MGMT, and an optional drug check last. The 30-second speech arrest with preserved awareness is treated as a focal aware seizure with levetiracetam, not as prophylaxis, and the EEG is no longer a waste action (its fallback now shows the focal slowing a 5 cm temporal mass would produce). The surgery must states that awake language mapping is limited by his current deficits and that the approach is decided after neurosurgical and neuropsychological assessment. The aphasia is now described as fluent and paraphasic, consistent with the posterior temporal site, and the optic radiation sits in the temporal loop and sagittal stratum.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation key `[AIOM_brain]` on the tissue criterion (plan section 5 item 1).
- Synonym "astrocytoma grade 4" is wrong for an IDH-wildtype glioblastoma (plan section 5 item 2).

## Open questions for Andrea (judgment calls you could not settle)
- None specific to this case; the plan's condition-wide questions apply.
- Decision taken: the EEG stays without a criterion (plan: recommended EEG only in M01, RP02, RM04, RP04, RS03), but it is no longer penalised as waste, since characterising a speech-arrest spell in a patient with progressive aphasia is a defensible order.

## Verification
Checked: every note id in the notes file is in the table; each FIXED claim against the final JSON (assay lists in both tissue alternatives, one findings row and molecular_findings entry per required assay, resection and biopsy follow-ups with identical integrated diagnosis, initial tissue and literature null, literature criterion gone from criteria, constraints and stop rule, fMRI/DTI retagging, performance status follow-up, musts against allergies and medications, LP harm rationale against the MRI shift); laterality, sex, age and timeline across HPI, exam, MRI, EEG and tissue; lab arithmetic (anion gap, Hb/Hct, PT/INR); differential against the final evidence; leakage (any-query outputs, HPI); report voice. perfect_agent.py -v, case_io.py check and test_case_guards pass after the changes.
Found and changed:
- `initial_tool_outputs.mri.impression` ended with "Tissue diagnosis recommended." (plan C9). Removed.
- `key_clinical_evidence[6]` was the template "For IDH-wildtype GBM, standard treatment is maximal safe resection followed by the Stupp protocol", not conditioned on age and KPS (plan C11). Rewritten for this patient: at 64 with KPS 70, 60 Gy in 30 fractions with concomitant and adjuvant temozolomide (Stupp 2005; EANO 2021), MGMT methylation predicting greater benefit. Consistent with must 6.
Verified as sound: HPI leak replaced by a non-contrast CT; speech arrest with preserved awareness classed as a focal aware seizure (treat must); the qualified awake-mapping surgery must against the documented comprehension and naming deficits; fluent paraphasic aphasia matches the posterior temporal site; right-hand sensory and graphesthesia findings are explained by the temporoparietal and inferior parietal extension; aspirin must and prohibition agree; fallback EEG now abnormal.

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4 (left temporal lobe)' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4 (left temporal lobe)' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- must removed: 'Obtain MRI brain with and without gadolinium contrast (tumor protocol) before any invasive procedure' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- must rewritten: 'Obtain pre-operative labs (CBC, BMP, coagulation, type & screen) and discontinue aspirin at least 7-10 days before craniotomy' -> 'Discontinue aspirin 7 to 10 days before craniotomy.' (Q9: the duplicated diagnostic part dropped, the management part kept)
- AIOM question numbers removed from the text (edition 2026 numbering unverified) (Q1: AIOM cited as the 2026 update; Quesito numbering not verifiable)
- fallback specialized_test (generic 'Study within normal limits.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
