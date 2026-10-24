# GLIO-HG-RS02
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 7fdc5cfc-8b15-4035-8e56-01f81a602ade | FIXED | `action-10-obtain-tissue-diagnosis` alternatives now `resection` first, `stereotactic_biopsy` second (group A); canonical label and rationale, adding that resection also treats the mass effect; must 1 is the canonical surgery must (maximal safe resection with preoperative fMRI, DTI and intraoperative mapping); "stereotactic biopsy or maximal safe resection" must deleted; tissue moved from `initial_tool_outputs` to two follow-ups, one per procedure (`request_resection_histomolecular`, `request_stereotactic_biopsy_histomolecular`), identical diagnosis and molecular results. |
| c27c5e41-f95e-4872-8d71-3f286fe2d05d | FIXED | `molecular_assays` now `IDH1_IHC`, `ATRX_IHC`, `MGMT_methylation` (age 59, MVP and necrosis on histology: plan C4) in both alternatives. Tissue reports carry a row and a `molecular_findings` entry for each: IDH1 R132H IHC negative, ATRX retained, MGMT methylated (42%); TERT C228T, EGFR amplification and 1p/19q not codeleted kept as results. Label lists the assays in words. |
| 6e655625-8a33-4986-81bb-89c048a6d0f6 | FIXED | Follow-up `request_functional_mri` retagged `modality: functional_MRI` (trigger `request_functional_mri_motor_language`), DTI sentence removed from its impression; new `request_dti_tractography` (`DTI_tractography`: right CST displaced, continuous, 7 mm from the posterior enhancing margin). Recommended `action-fmri-functional-mapping` and `action-dti-tractography` added, with soft constraints to tissue; the surgery must names both. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | patient.neurological_exam.additional | Exam re-described the home seizure as a second 45 s + 75 s seizure "during the ED evaluation", contradicting the HPI (alert and conversant on arrival) | FIXED: "No further seizure activity during the emergency department evaluation" |
| B | minor | patient.neurological_exam.cranial_nerves | "Subtle left inferior quadrantanopia": no lesion explains it (frontal tumour, edema frontal and capsular, not parietal) | FIXED: visual fields full |
| C | major | musts 3 and 4 | HPI says dexamethasone and levetiracetam were started in the ED; musts said "administer" and "initiate ... for documented seizure activity" (C5 treat class, continue form) | FIXED: continue dexamethasone at the lowest effective dose; continue levetiracetam for the documented focal to bilateral seizure of left-hand onset, with dose review and enzyme-inducer avoidance |
| A/C | major | action-3 literature criterion, follow-up, stop rule | Literature as a required step (C1) | FIXED: deleted |
| A/D | major | initial_tool_outputs.tissue_diagnosis | Tissue served upfront; template meta-text in impression; no Histology row (C2) | FIXED: initial null; follow-ups with `Histology`, GFAP and Ki-67 rows; impression "Integrated diagnosis: Glioblastoma, IDH-wildtype, CNS WHO grade 4. MGMT promoter methylated." |
| B/C | major | two `check_drug_interactions` follow-ups | Two DDI outputs; the temozolomide one said contraception was "not applicable in this male patient's age group" (wrong: temozolomide is genotoxic and men need contraception) and ignored ibuprofen | FIXED: merged into one output (`check_levetiracetam_dexamethasone_temozolomide`) listing his lisinopril and ibuprofen, the sulfonamide allergy against co-trimoxazole for Pneumocystis prophylaxis, and the male contraception warning; criterion stays optional and last; expected evidence is the case's own interactions |
| C | major | assessment | Ibuprofen with dexamethasone and before neurosurgery not addressed | FIXED: must to stop ibuprofen and use paracetamol |
| C | major | assessment must 6 | Template Stupp must (C11) | FIXED: entity, age and KPS specific must with sulfonamide-safe Pneumocystis prophylaxis |
| C | major | ground_truth | No performance status (C7) | FIXED: recommended `action-performance-status` (age 59) with follow-up KPS 70, ECOG 2 from the exam (hemiparesis, foot drag, unable to work) |
| D | minor | initial_tool_outputs.eeg.impression | "The sharp wave localization correlates with the clinical seizure semiology" (cross-modality) | FIXED: ACNS impression listing the three abnormalities |
| D | minor | initial_tool_outputs.mri.impression | "which has implications for surgical planning" (management) | FIXED: numbered imaging-only impression |
| B | minor | initial_tool_outputs.ecg.interpretation | Omitted the rhythm and the LVH listed in findings | FIXED |
| B | minor | labs CBC, coagulation, CRP | Values identical to the shared template (RS01: WBC 8.2, Hb 15.1, Hct 44.2, platelets 245, PT 12.8, aPTT 28, CRP 3.8) | FIXED: case-specific normal values (WBC 9.6, Hb 14.6, Hct 43.1, MCHC 33.9, platelets 231, PT 12.4, aPTT 30, CRP 2.6) |
| C | minor | labs type_and_screen clinical_significance | Template engineering text | FIXED: null |
| C | minor | differential, red_herrings | The case's own mimic (paraesthesias attributed to cycling posture, cervical spondylosis) neither in the differential nor declared as a red herring (ruling 7) | FIXED: "Ulnar neuropathy or cervical radiculopathy" at very low with the excluding signs; red herring added |
| C | minor | differential | Lymphoma "low" despite necrotic ring enhancement and glial tissue | FIXED: very low with tissue |
| C | minor | action-1, -2, -6, -7, -8 | Template expected evidence and label-copy rationales; `[Stupp_2005]` on MRI | FIXED from the case's own reports; `[EANO_2021]` |
| C | minor | avoided_actions, prohibited_recommendations[0] | Templated waste rationales; LP text with an em dash | FIXED: "No cardiac question in this presentation"; LP harm citing 9 mm shift and papilloedema |
| C | minor | sequence_constraints, stop_rule | Template soft constraint; literature in stop rule | FIXED: hard MRI and labs to tissue, soft fMRI and DTI to tissue; stop rule MRI, labs, tissue |
| B | minor | metadata.difficulty_rationale | Counts out of date | FIXED |

## Changes, in one paragraph a physician can read before re-reviewing
The pathway is contrast MRI, perfusion, spectroscopy, optional body CT, pre-operative labs, performance status (KPS 70, ECOG 2), functional MRI (hand motor area 8 mm from the margin) and DTI (corticospinal tract 7 mm), then tissue by maximal safe resection with stereotactic biopsy as the fallback, with IDH1 R132H, ATRX and MGMT, and one optional drug check last. Tissue is no longer given upfront and literature is not a step. The exam no longer repeats the home seizure as a second seizure in the ED, and the unexplained quadrantanopia is gone. Because the ED already started dexamethasone and levetiracetam, the musts continue both (lowest effective steroid dose; levetiracetam as treatment of a documented focal to bilateral seizure). New musts stop ibuprofen (with dexamethasone and before surgery) and, after the integrated diagnosis, give 60 Gy/30 with temozolomide and Pneumocystis prophylaxis that avoids co-trimoxazole because of his sulfonamide allergy. The paraesthesias first attributed to cycling are declared as a red herring and as an excluded mimic.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation key `[AIOM_brain]` on the tissue criterion (plan section 5 item 1).
- Synonym "astrocytoma grade 4" is wrong for an IDH-wildtype glioblastoma (plan section 5 item 2).

## Open questions for Andrea (judgment calls you could not settle)
- None specific to this case; the plan's condition-wide questions apply (AIOM edition, biopsy as a full-credit alternative in group A, `max_additional_actions`).
- Decision taken: the drug check stays optional (plan C13) although the case now has real interactions; the management they change (stop ibuprofen, no co-trimoxazole) is carried by musts, so an agent that knows them without the tool is not penalised.

## Verification
Checked: every note id in the notes file is in the table; each FIXED claim against the final JSON (assay lists in both tissue alternatives, one findings row and molecular_findings entry per required assay, resection and biopsy follow-ups with identical integrated diagnosis, initial tissue and literature null, literature criterion gone from criteria, constraints and stop rule, fMRI/DTI retagging, performance status follow-up, musts against allergies and medications, LP harm rationale against the MRI shift); laterality, sex, age and timeline across HPI, exam, MRI, EEG and tissue; lab arithmetic (anion gap, Hb/Hct, PT/INR); differential against the final evidence; leakage (any-query outputs, HPI); report voice. perfect_agent.py -v, case_io.py check and test_case_guards pass after the changes.
Found and changed:
- `initial_tool_outputs.mri.impression` ended with "Tissue diagnosis recommended." (plan C9). Removed.
- Template imaging numbers shared verbatim with RS01 and RS03 (PATTERNS 4, identical numbers across cases): rCBV 4.1 / necrotic core 0.3, edema 95 cm3, language laterality index 0.82 (also RS01). Changed to rCBV 3.6 and 0.4 (perfusion findings and impression), edema 88 cm3 (MRI volumetrics), laterality index 0.77 (fMRI finding and impression), and the same values in `action-6` and `action-fmri-functional-mapping` expected evidence and `key_clinical_evidence[2]`.
Verified as sound: the continue forms of the dexamethasone and levetiracetam musts (both started in the ED per the HPI); ibuprofen stop must; sulfonamide-safe Pneumocystis prophylaxis; KPS 70 / ECOG 2 matches the exam; drug check optional and last.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `ground_truth.red_herrings[0].field_path` was empty: now `patient.history_present_illness`.
- `patient.neurological_exam.mental_status`: "Language fluent with intact naming and repetition." (right-hemisphere lesion, left-dominant language).
- `fallback_tool_outputs.csf`: opening pressure 16 changed to 24 cm H2O, interpretation "Elevated opening pressure. Normal cell count, protein and glucose."; a normal pressure contradicts the documented papilloedema (same class as S02, S03, S04, S06).
- Drug check (`followup_outputs` DDI and `action-check-drug-interactions`): temozolomide was proposed before any tissue diagnosis (plan C13). Now levetiracetam 1000 mg twice daily and dexamethasone 4 mg every 6 hours with lisinopril and as-needed ibuprofen; temozolomide interactions and warnings removed; the sulfonamide contraindication reads "if Pneumocystis prophylaxis becomes necessary, use an alternative agent (inhaled pentamidine or atovaquone)"; label rewritten accordingly. The treatment must adds "and effective contraception during and after temozolomide."
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- must removed: 'Obtain MRI brain with and without gadolinium contrast (tumor protocol) before any invasive procedure' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- must removed: 'Obtain pre-operative labs (CBC, BMP, coagulation, type & screen) before craniotomy/biopsy' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- AIOM question numbers removed from the text (edition 2026 numbering unverified) (Q1: AIOM cited as the 2026 update; Quesito numbering not verifiable)
- fallback specialized_test (generic 'Study within normal limits.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
