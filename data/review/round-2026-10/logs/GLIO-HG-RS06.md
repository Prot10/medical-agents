# GLIO-HG-RS06
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 39805cb7-983e-4cfa-ac69-0f7f0ec03ef4 | FIXED | No-seizure class (plan C5). Levetiracetam deleted from the drug-interaction output (`proposed`, the calcium carbonate plus levetiracetam interaction, the lacosamide alternative, `formulary_status`) and from the criterion label. Prohibition added verbatim: "Do not start prophylactic antiseizure medication: the patient has had no seizure, and AIOM recommends against prophylaxis in brain tumour patients without a seizure history." Key evidence item added. The EEG waste entry stays with the canonical rationale. |
| 76ce5cab-3b3a-4584-ace7-410c55256434 | FIXED | Tissue criterion `resection` first, `stereotactic_biopsy` second (group A), canonical label, rationale and surgery must (the interchangeable "stereotactic biopsy or maximal safe resection" must is gone). New `functional_MRI` follow-up (left-lateralised, LI 0.68, Wernicke area 6 mm and angular gyrus 3 mm from the margin, partial task performance) and `DTI_tractography` follow-up (arcuate 4 mm, optic radiation within the FLAIR abnormality 2 mm, CST 18 mm); recommended `action-fmri-functional-mapping` and `action-dti-tractography` with soft constraints to tissue. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A/C | major | action-3 literature criterion, follow-up, stop rule | Literature as a required step (C1); the Perry 2017 entry also carried a title that is not the paper's | FIXED: deleted; Perry 2017 moved to the treatment must |
| A/D | major | initial_tool_outputs.tissue_diagnosis | Tissue served upfront; template meta-text; "(left temporal-parietal)" inside the integrated diagnosis (C2) | FIXED: initial null; resection and biopsy follow-ups; site in `site`; Histology row |
| C | major | action-10 molecular_assays | List had no IDH requirement matching the report and required 1p/19q in an IDH-wildtype tumour (C4) | FIXED: `IDH1_IHC`, `ATRX_IHC`, `MGMT_methylation` (age 71) in both alternatives; report rows for each; IDH sequencing row dropped (not needed at 55 or over) |
| C | major | ground_truth | No performance status; patient is 71 (C7) | FIXED: required `action-performance-status`, in the stop rule; follow-up KPS 70, ECOG 2 |
| D | major | patient.neurological_exam.additional | "Karnofsky performance status estimated at 70" gave away the required assessment; "localizing to the left temporal-parietal cortex and optic radiations" is interpretation | FIXED: replaced by the bedside cognitive findings only |
| C | major | must 5 | Template "consider hypofractionated" must (C11) | FIXED: age 71, KPS 70, MGMT methylated: 40 Gy in 15 fractions with temozolomide (Perry 2017; EANO 2021), or temozolomide alone |
| C | major | drug-interaction output | "Corticosteroids may reduce the immunomodulatory efficacy of hydroxychloroquine" and "dexamethasone can cause QT prolongation" are not established interactions | FIXED: QT risk from hydroxychloroquine increased by steroid hypokalaemia; antacid spacing for calcium carbonate; ondansetron warning; em dash removed |
| C | minor | action-9 | DDI optional (C13: recommended in RS06) | FIXED: recommended, last; expected evidence rewritten (leak guard passes) |
| C | minor | must 6 | Baseline ECG justified by dexamethasone QT prolongation | FIXED: ECG and potassium for the hydroxychloroquine QT effect, avoid ondansetron where possible |
| B | major | initial_tool_outputs.labs | Criterion requires `type_and_screen` but the panel had none | FIXED: type and screen row added (clinical_significance null) |
| B | minor | labs BMP | Creatinine 1.2 with eGFR 63 in a 71-year-old woman (CKD-EPI gives about 47), against the history of CKD stage 2, eGFR 65 | FIXED: creatinine 0.95, eGFR 64; summary and interpretation recomputed without clinical attributions |
| B/C | minor | initial_tool_outputs.mri mass_effect, edema finding | "leftward displacement" of the left atrium and "overall leftward mass effect" with a rightward shift | FIXED: medial displacement; rightward |
| C | minor | initial_tool_outputs.mri FLAIR, edema location | Edema "involving the posterior limb of the left internal capsule" with full strength and no drift; optic radiation not placed | FIXED: optic radiation in the sagittal stratum, reaching the retrolenticular part of the internal capsule |
| D | minor | mri.impression, additional_observations | "consistent with the reported right visual field deficit", "consistent with the identified right homonymous hemianopia", "Tissue diagnosis recommended" (C9) | FIXED: imaging only |
| B/C | major | fallback_tool_outputs.eeg | Normal EEG with "no focal slowing" for a 4.9 cm temporoparietal mass: impossible | FIXED: left temporoparietal polymorphic delta, no epileptiform discharges; `metadata.fallback_tool_kinds.eeg` updated |
| D | minor | follow-up CT CAP kidneys | "consistent with reported CKD" (cross-modality) | FIXED: imaging description only |
| C | minor | patient.history_present_illness | "lupus-like CNS involvement of her RA"; dose increase not stated | FIXED: rheumatoid CNS involvement (meningitis or vasculitis), increased to 200 mg twice daily, matching the medication list |
| C | minor | differential | Metastasis moderate and lymphoma low after glial tissue | FIXED: low and very low |
| C | minor | action-1, -2, -6, -7, -8 | Label-copy rationales; `[Stupp_2005]` on MRI; duplicated citation keys | FIXED |
| C | minor | avoided_actions, sequence_constraints, stop_rule | Templates; soft MRI constraint only | FIXED per plan section 3: hard MRI and labs to tissue, soft fMRI and DTI to tissue; LP harm canonical (5 mm shift) |
| C | minor | red_herrings, key_clinical_evidence | Rewritten from the case's own findings; em dashes | FIXED |
| E | minor | HPI, mental status, perfusion and MRS regions, ECG fallback, prohibitions | Em dashes | FIXED (the shared `metadata.condition_name` is left as it is) |
| B | minor | metadata.difficulty_rationale, difficulty_description | Counts and "two specialist consults" out of date | FIXED |

## Changes, in one paragraph a physician can read before re-reviewing
The pathway is contrast MRI, perfusion, spectroscopy, optional body CT, pre-operative labs (now with a type and screen), performance status (required at 71: KPS 70, ECOG 2, no longer stated in the examination), functional MRI and DTI (Wernicke area 6 mm and angular gyrus 3 mm from the margin, optic radiation within the oedema), then tissue by maximal safe resection with biopsy as the fallback (IDH1 R132H, ATRX, MGMT), and a recommended drug check last for her hydroxychloroquine. She has had no seizure, so levetiracetam is gone from the drug check and prophylaxis is now prohibited. The drug check reports the real interactions: QT prolongation from hydroxychloroquine, made worse by steroid hypokalaemia and by ondansetron, and antacid spacing; the invented dexamethasone QT and efficacy interactions are gone. After the integrated diagnosis the must is hypofractionated radiotherapy 40 Gy in 15 fractions with temozolomide (MGMT methylated, age 71), with Pneumocystis prophylaxis avoiding co-trimoxazole. Creatinine now matches her CKD stage 2, the MRI places the optic radiation in the sagittal stratum, and the fallback EEG shows the focal slowing a mass this size produces.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation key `[AIOM_brain]` on the tissue criterion (plan section 5 item 1).
- Synonym "astrocytoma grade 4" is wrong for an IDH-wildtype glioblastoma (plan section 5 item 2).
- `accepted[0]` still carries the site suffix "(left temporal-parietal)" and "WHO grade 4" rather than "CNS WHO grade 4"; left for the central label pass.

## Open questions for Andrea (judgment calls you could not settle)
- Required performance status at 65 or over follows the plan (open question 5).
- Awake mapping at 71 with anomia: the surgery must keeps the canonical "intraoperative mapping" wording without the feasibility qualifier used in RS05; confirm whether the same qualifier should apply here.

## Verification
Checked: every note id in the notes file is in the table; each FIXED claim against the final JSON (assay lists in both tissue alternatives, one findings row and molecular_findings entry per required assay, resection and biopsy follow-ups with identical integrated diagnosis, initial tissue and literature null, literature criterion gone from criteria, constraints and stop rule, fMRI/DTI retagging, performance status follow-up, musts against allergies and medications, LP harm rationale against the MRI shift); laterality, sex, age and timeline across HPI, exam, MRI, EEG and tissue; lab arithmetic (anion gap, Hb/Hct, PT/INR); differential against the final evidence; leakage (any-query outputs, HPI); report voice. perfect_agent.py -v, case_io.py check and test_case_guards pass after the changes.
Found and changed:
- `ground_truth.differential` "Brain abscess" was left `low` although no fever, rim (not central) restricted diffusion, high rCBV and glial tissue exclude it (ruling 7); "CNS vasculitis / rheumatoid meningitis" likewise `low` after tissue shows glioblastoma. Both set to `very_low`, with the tissue result added to their key features (and the absent leptomeningeal enhancement for rheumatoid meningitis).
- Open question of the worker (awake mapping qualifier) decided rather than left: she has anomia with 2 of 8 paraphasic naming errors, follows two-step commands and has impaired memory at 71, so awake language mapping is possible but not assured. The surgery must now reads "intraoperative mapping (awake language mapping only if her naming and comprehension allow the intraoperative tasks, otherwise asleep resection with subcortical monitoring)". The open question is closed.
- `followup_outputs[request_ct_chest_abdomen_pelvis]` lungs: "Mild background emphysematous changes" in a never smoker with no lung history, an unexplained template finding. Removed.
- `fallback_tool_outputs.ecg`: QTc 441 ms called "at the upper limit of normal" and "borderline"; for a woman the upper limit is 460 ms. Reworded as normal for a woman (the baseline ECG must stays, for the hydroxychloroquine QT risk).
Verified as sound: no-seizure prohibition and levetiracetam removed from the drug check; required performance status (71) in the stop rule; drug check recommended with real hydroxychloroquine QT, antacid spacing and sulfonamide content; hypofractionated 40 Gy/15 with temozolomide (Perry 2017) at 71, KPS 70, MGMT methylated; creatinine 0.95 with eGFR 64 matches CKD stage 2.

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4 (left temporal-parietal)' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4 (left temporal-parietal)' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- must removed: 'Obtain MRI brain with and without gadolinium contrast (tumor protocol) before any invasive procedure' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- must removed: 'Obtain pre-operative labs (CBC, BMP including renal function, coagulation, type and screen) before craniotomy or biopsy' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
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

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-2-interpret-labs]`.alternatives: was [CBC, BMP, coagulation, type_and_screen]; now [CBC, BMP, coagulation, type_and_screen, ESR, CRP] | [CBC, BMP, coagulation, type_and_screen].
- Decision: serve: new first alternative (old order kept as an alternative). Known seropositive RA: the key evidence and the CNS-vasculitis differential rely on ESR, CRP, RF and anti-CCP, stored together.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

Case-specific reports stored where the benchmark library's normal report contradicted the case. Why: the stored MRI shows a mass in the left temporal-parietal lobe (superior temporal and angular gyri) (4.9 x 4.2 x 3.8 cm) with an abnormal routine EEG and a focal history and exam; the library reports a normal head CT, a non-diagnostic biopsy, normal brain metabolism, perfusion and vessels, a normal prolonged EEG, no headache and normal bedside and neurophysiological tests where the exam is abnormal.

- order_ct_scan: CT showing the stored lesion(s) instead of a normal head CT (fallback_tool_outputs.ct)
- obtain_tissue_diagnosis open_biopsy: the stored integrated diagnosis on this procedure's specimen (fallback_tool_outputs.tissue_diagnosis)
- FDG_PET: hypermetabolic lesion(s) (fallback_tool_outputs.advanced_imaging)
- amino_acid_PET: FET-avid lesion(s) (followup request_amino_acid_pet)
- CT_perfusion: lesion perfusion matching the stored perfusion MRI (followup request_ct_perfusion)
- perfusion_SPECT: regional hypoperfusion over the lesion (followup request_perfusion_spect)
- cerebral_angiography: mass effect and lesion vascularity (followup request_cerebral_angiography)
- video EEG: the stored routine EEG's abnormalities over 24 h (followup request_video_eeg)
- ambulatory EEG: the stored routine EEG's abnormalities over 48 h (followup request_ambulatory_eeg)
- structured_headache_history_ichd3: the case's headache, prior primary headache and red flags (fallback_tool_outputs.clinical_assessment)
- cognitive_screen: MoCA matching the exam (followup request_cognitive_screen)
- gait_and_balance_timed: matching the exam (followup request_timed_gait_balance)
- neuropsych_battery: domain deficits matching the exam (fallback_tool_outputs.specialized_test)
- speech_language_evaluation: matching the exam (followup request_speech_language_evaluation)
- visual_field_perimetry: the exam's field defect or blind-spot enlargement (followup request_visual_field_perimetry)

Checks: `perfect_agent.py` pass; `test_case_guards.py -k GLIO-HG-RS06` pass; no fixed order still answered by the library (`lib4.source`); no 60-character window of any criterion's expected_evidence in the added text, except tissue copies that repeat the stored tissue report verbatim; every criterion's served output unchanged (snapshot diff against the baseline).
