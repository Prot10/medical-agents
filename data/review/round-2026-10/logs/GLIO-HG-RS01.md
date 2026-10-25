# GLIO-HG-RS01
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| e649546c-c40b-4bf2-94e2-b363198fde60 | FIXED | `initial_tool_outputs.labs.panels["Exclusion studies"]` (the serum `chr7_gain_chr10_loss` row) deleted. +7/-10 is now reported only on tissue ("Chromosome 7 gain / chromosome 10 loss: Present"). |
| 32b30a51-1852-4e3d-82cb-4a748d1c7def | FIXED | `action-10-obtain-tissue-diagnosis` `molecular_assays` now `IDH1_IHC`, `IDH1_IDH2_sequencing` (under 55), `ATRX_IHC`, `MGMT_methylation` in both alternatives (plan C4). Tissue reports have a `findings` row and `molecular_findings` entry for each: IDH1 R132H IHC negative, IDH1/IDH2 sequencing wildtype, ATRX retained, MGMT methylated; TERT C228T, EGFR amplification, +7/-10 and 1p/19q non-codeleted kept. `1p_19q_codeletion`, `TERT_promoter`, `EGFR_amplification`, `chr7_gain_chr10_loss` removed from the required list (histology already shows MVP and necrosis). Label lists the assays in words. |
| 075ad500-72a7-4de4-be25-39f10b254c48 | FIXED | (1) Anatomy: `initial_tool_outputs.mri.findings[2].location` now "Right jugular foramen in the posterior cranial fossa, with erosion of the adjacent petrous temporal bone toward the cochlea; no extension into the cavernous sinus or orbit"; type "Extra-axial skull-base mass"; impression item 3 names it as most consistent with a jugular paraganglioma. (2) Deficits: kept those a jugular foramen paraganglioma can produce (right sensorineural hearing loss, Weber to the left, now with Rinne positive bilaterally; right pulsatile tinnitus added to the HPI); REMOVED the ones neither lesion can produce (right proptosis, right acuity 20/40, right temporal field defect, right V2/V3 hypoaesthesia) from `patient.neurological_exam.cranial_nerves` and `.sensory`, and "vision changes beyond what he attributes to his old injury" from the HPI. Lower cranial nerves documented intact (gag, voice, shoulder shrug). (3) Red herring 2 rewritten: a separate paraganglioma needing its own work-up, not dismissed. (4) New recommended `action-paraganglioma-genetics` (`order_specialized_test` `genetic_panel:hereditary_paraganglioma`) with follow-up `request_germline_paraganglioma_panel` (heterozygous pathogenic SDHD c.112C>T p.(Arg38Ter), other 10 genes negative). (5) Musts added: skull-base MDT referral, plasma free metanephrines before anaesthesia, clinical genetics counselling and cascade testing, chromogranin A IHC. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | patient.neurological_exam.additional vs HPI | Exam said the seizure was "in the emergency department ... with preserved awareness"; HPI says at his desk, witnessed by his partner, with confusion and unresponsiveness | FIXED: exam "No further seizure activity during the emergency department stay"; seizure classed as focal motor with impaired awareness |
| C | major | assessment must 4 | "Initiate antiepileptic therapy ... for documented seizure activity" without naming the seizure or enzyme-inducer avoidance (plan C5, treat class) | FIXED: canonical treat must |
| A/C | major | action-3 literature criterion, follow-up, stop rule | Literature as a required clinical step (ruling 5, C1) | FIXED: criterion, follow-up and stop-rule id deleted |
| A | major | initial_tool_outputs.tissue_diagnosis | Tissue served in the initial work-up, template meta-text in impression, "Microscopic description" listed as a molecular finding (C2) | FIXED: initial null; two follow-ups (`resection`, `stereotactic_biopsy`) with identical integrated diagnosis and molecular results; one `Histology` row; impression "Integrated diagnosis: Glioblastoma, IDH-wildtype, CNS WHO grade 4. MGMT promoter methylated." |
| C | major | action-10, must 1 | Stereotactic biopsy as the only procedure, biopsy and resection interchangeable in must 1 (C3, group A) | FIXED: alternatives resection then stereotactic biopsy; canonical label, rationale and surgery must |
| C | minor | tissue findings | A hemispheric IDH-wildtype glioma at 35: GBM IDH-wildtype requires H3-wildtype and H3 G34 is the young-adult mimic | FIXED: "H3F3A sequencing (H3 K27, G34): No mutation detected" row; "Diffuse hemispheric glioma, H3 G34-mutant" and "Astrocytoma, IDH-mutant, CNS WHO grade 4" added to the differential at low; vocabulary term under CENTRAL |
| A/C | major | followup request_functional_mri | fMRI content tagged `perfusion_MRI`; impression added DTI absent from findings; no scored criterion (C6) | FIXED: retagged `functional_MRI`; new `request_dti_tractography` (`DTI_tractography`: CST 6 mm, optic radiation 8 mm); recommended `action-fmri-functional-mapping` and `action-dti-tractography`; soft constraints to tissue. Rule applied from the MRI: hand motor activation 12 mm (about 1 cm) from the margin with left arm weakness, CST displaced; language cortex left-dominant, not involved |
| C | major | ground_truth | No performance status (C7) | FIXED: recommended `action-performance-status` (age 35) with follow-up KPS 80, ECOG 1 from the exam |
| A/C | major | followup request_catecholamine_workup | Pre-anaesthetic catecholamine screen filed as an unscored `interpret_labs` step with no criterion (C14) | FIXED: follow-up deleted; plasma free metanephrines as a must (no metanephrine panel in the vocabulary: CENTRAL) |
| C | minor | action-8 CT CAP | Optional despite paraganglioma and phaeochromocytoma history | FIXED: recommended, expected evidence from its own report |
| D | minor | initial_tool_outputs.eeg.impression | Template impression omitted the delta activity and sharp waves (C9) | FIXED: ACNS impression listing the three abnormalities |
| D | minor | initial_tool_outputs.mri.impression, additional_observations | Impression one paragraph and omitted the skull-base lesion; "Mild chronic small vessel ischemic changes are not expected for this patient's age"; "two parenchymal lesions" for one parenchymal and one extra-axial lesion | FIXED: numbered impression; observations rewritten |
| B | minor | followup request_mri_perfusion | Impression reported perilesional rCBV absent from findings | FIXED: perilesional finding (rCBV 1.4) added; numbered impression |
| C | minor | action-1, -2, -6, -7, -8 expected_evidence and rationale | Template evidence and rationale copied from the label; `[Stupp_2005]` on the MRI | FIXED: from the case's own reports; `[EANO_2021]` on the MRI |
| C | minor | labs type_and_screen clinical_significance | Template engineering sentence ("which is what this case's diagnosis rests on") | FIXED: null |
| C | major | assessment must 6 | Template Stupp must not conditioned on diagnosis or KPS (C11) | FIXED: entity, age and KPS specific must, with fertility counselling before temozolomide (35-year-old man) |
| C | minor | must 3 | Dexamethasone dose "given imaging evidence of herniation" template | FIXED: canonical C11 must |
| C | minor | differential | IDH-wildtype status cited as excluding metastasis; "no known primary cancer" in a man with prior paraganglioma; corpus callosum involvement not in this MRI | FIXED: key features rewritten from the tissue and CT results |
| C | minor | action-9 DDI | Template expected evidence about diabetics | FIXED: amlodipine, dexamethasone and levetiracetam; levetiracetam line added to the output; stays optional and last |
| C | minor | avoided_actions | Waste rationales templated; LP rationale generic | FIXED: "No cardiac question in this presentation" with `[EANO_2021]`; LP harm with 9 mm shift and uncal herniation |
| C | minor | sequence_constraints | Single soft MRI-to-tissue constraint | FIXED: hard MRI and labs to tissue, soft fMRI and DTI to tissue |
| E | minor | prohibited_recommendations[0] | Em dash | FIXED |
| B | minor | metadata.difficulty_rationale/description | Counts and description out of date | FIXED |

## Changes, in one paragraph a physician can read before re-reviewing
The pathway is now contrast MRI, perfusion, spectroscopy, CT chest/abdomen/pelvis, pre-operative labs, performance status (KPS 80, ECOG 1), functional MRI and DTI tractography (hand motor area 12 mm and CST 6 mm from the tumour), germline hereditary paraganglioma panel (pathogenic SDHD variant), then tissue by maximal safe resection (biopsy as the fallback) with IDH1 R132H IHC, IDH1/IDH2 sequencing, ATRX and MGMT, and an optional drug check last. Tissue is no longer served upfront and literature is not a step. The skull-base lesion is now a right jugular foramen paraganglioma in the posterior fossa, which explains his right pulsatile tinnitus and sensorineural hearing loss; the deficits no lesion could explain (proptosis, reduced right acuity, right temporal field defect, V2/V3 hypoaesthesia) were removed from the exam. The seizure is one focal motor seizure with impaired awareness at home and is treated with levetiracetam. Musts: resection with functional imaging, dexamethasone at the lowest effective dose, levetiracetam, plasma metanephrines before anaesthesia, chromogranin A IHC, skull-base team, clinical genetics, and chemoradiotherapy 60 Gy/30 with temozolomide after the integrated diagnosis with fertility counselling. The serum +7/-10 row is gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Vocabulary: chromogranin A and synaptophysin IHC for `obtain_tissue_diagnosis` (plan C15); an H3 G34 status assay (the report states H3F3A K27/G34 wildtype as a findings row only); a plasma free metanephrines panel for `interpret_labs` (now a must only).
- Citation key `[AIOM_brain]` used on the tissue criterion (plan section 5 item 1).
- Synonym "astrocytoma grade 4" in `accepted` is wrong for an IDH-wildtype glioblastoma (plan section 5 item 2). `accepted[0]` "WHO grade 4" left as is (normalisation to "CNS WHO grade" is central).

## Open questions for Andrea (judgment calls you could not settle)
- None specific to this case. The condition-wide questions of the plan (AIOM edition, biopsy as an equal alternative in group A, `max_additional_actions` 0) apply.
- Decision taken: of the reviewer's two options for the orphaned deficits, I removed them rather than extending the paraganglioma to the cavernous sinus and orbit, because a 2.3 x 1.8 cm jugular foramen lesion with no intracranial mass effect cannot reach the orbit, and enlarging it would make it a giant Fisch D tumour inconsistent with the rest of the case.
- Decision taken: SDHD was chosen as the germline result because paternal transmission (father and paternal uncle) with head and neck paraganglioma is the SDHD pattern (maternal imprinting).

## Verification
Checked: every note id in the notes file is in the table; each FIXED claim against the final JSON (assay lists in both tissue alternatives, one findings row and molecular_findings entry per required assay, resection and biopsy follow-ups with identical integrated diagnosis, initial tissue and literature null, literature criterion gone from criteria, constraints and stop rule, fMRI/DTI retagging, performance status follow-up, musts against allergies and medications, LP harm rationale against the MRI shift); laterality, sex, age and timeline across HPI, exam, MRI, EEG and tissue; lab arithmetic (anion gap, Hb/Hct, PT/INR); differential against the final evidence; leakage (any-query outputs, HPI); report voice. perfect_agent.py -v, case_io.py check and test_case_guards pass after the changes.
Found and changed:
- `initial_tool_outputs.mri.impression` still ended with "Tissue diagnosis recommended for the frontotemporal mass.", a management sentence plan C9 deletes. Removed.
Verified as sound: the decision to remove the deficits no lesion explains (proptosis, acuity, field defect, V2/V3) rather than enlarging the paraganglioma; the SDHD c.112C>T p.(Arg38Ter) result with paternal transmission; the jugular foramen lesion now explains only the pulsatile tinnitus and the right sensorineural loss (Weber left, Rinne positive bilaterally, consistent).
Left as is (minor, not an error): `key_clinical_evidence[6]` is the condition-wide template sentence on off-pathway imaging (DaTscan, amyloid PET...); it is not wrong and appears across the condition, so it is for the lead to decide once for all 30.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `ground_truth.red_herrings[0].field_path` was empty: now `patient.clinical_history.past_medical_history[0]`.
- `ground_truth.red_herrings[1].field_path` was empty: now `patient.clinical_history.past_medical_history[3]`.
- `patient.neurological_exam.mental_status`: "Language is fluent with intact naming and repetition." (right-hemisphere lesion, left-dominant language).
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

## Central vocabulary wired (24 Oct 2026)

Terms added by commit e19131d6 (batch-2 review vocabulary), wired as the plan and this log intended. The earlier CENTRAL vocabulary request in this log is resolved by them.

- `action-10-obtain-tissue-diagnosis`: `chromogranin_A_synaptophysin_IHC` and `H3G34_status` added to the minimum assay list of both alternatives (resection, stereotactic biopsy), as for the melanoma markers in RP04; label, rationale and expected evidence name them. Tissue reports (both procedures): the "Chromogranin A immunostain" row became "Chromogranin A and synaptophysin IHC: Chromogranin A negative; synaptophysin negative in tumour cells, positive only in entrapped neuropil"; the "H3F3A sequencing (H3 K27, G34)" row became "H3 G34 status (H3F3A sequencing): H3 G34R/V not detected; no H3 K27M mutation"; both now also in `molecular_findings`.
- New required criterion `action-plasma-metanephrines` (`interpret_labs` `{"panels": ["plasma_free_metanephrines"]}`), placed after the pre-operative labs, with a hard constraint before tissue and added to the stop rule before tissue. Reason: a known SDHD carrier with a prior phaeochromocytoma and a skull-base paraganglioma must have catecholamine excess excluded (or blocked) before anaesthesia (Lenders JWM et al., Endocrine Society guideline, J Clin Endocrinol Metab 2014;99:1915-1942, key `[Lenders_2014]`). New follow-up `request_plasma_free_metanephrines` before the tissue follow-ups: metanephrine 0.24 nmol/L (<0.50), normetanephrine 0.71 nmol/L (<0.90), supine sampling; normal, consistent with his borderline, amlodipine-controlled blood pressure and a non-secreting head and neck paraganglioma.
- Musts: "Measure plasma free metanephrines before anaesthesia..." (now a criterion) rewritten to its management content: proceed without alpha-blockade given normal metanephrines and inform the anaesthetic team of the syndrome and the jugular foramen paraganglioma. "Ask neuropathology to include chromogranin A immunohistochemistry..." removed (now in the assay list; plan Q9: musts are management).
- Differential: metastatic paraganglioma entry now "chromogranin A- and synaptophysin-negative"; H3 G34 entry "H3 G34 status wildtype". `key_clinical_evidence` tissue item names H3 G34 wildtype and chromogranin/synaptophysin negative; the paraganglioma item says the metanephrines are normal.
- CENTRAL: add `[Lenders_2014]` to the GLIO-HG pack allow-list; the pack sentence "Markers outside the vocabulary (chromogranin, synaptophysin, PAX8, TTF-1, thyroglobulin, H3 G34, methylation profiling) are stated in musts and findings rows, never in `molecular_assays`" is now obsolete.

Checks after the change: `perfect_agent.py GLIO-HG-RS01 -v` ok, `case_io.py check` (schema and synonym guard OK, no failure names the case), `test_case_guards.py -k "GLIO-HG- or ALZ-EARLY-"` 120 passed.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

Case-specific reports stored where the benchmark library's normal report contradicted the case. Why: the stored MRI shows a mass in the right frontotemporal region (inferior frontal and superior temporal gyri, insula) (5.8 x 5.1 x 4.5 cm) with an abnormal routine EEG and a focal history and exam; the library reports a normal head CT, a non-diagnostic biopsy, normal brain metabolism, perfusion and vessels, a normal prolonged EEG, no headache and normal bedside and neurophysiological tests where the exam is abnormal.

- order_ct_scan: CT showing the stored lesion(s) instead of a normal head CT (fallback_tool_outputs.ct)
- obtain_tissue_diagnosis open_biopsy: the stored integrated diagnosis on this procedure's specimen (fallback_tool_outputs.tissue_diagnosis)
- FDG_PET: hypermetabolic lesion(s) (fallback_tool_outputs.advanced_imaging)
- amino_acid_PET: FET-avid lesion(s) (followup request_amino_acid_pet)
- CT_perfusion: lesion perfusion matching the stored perfusion MRI (followup request_ct_perfusion)
- perfusion_SPECT: regional hypoperfusion over the lesion (followup request_perfusion_spect)
- cerebral_angiography: mass effect and lesion vascularity (followup request_cerebral_angiography)
- video EEG: the stored routine EEG's abnormalities over 24 h (fallback_tool_outputs.eeg)
- ambulatory EEG: the stored routine EEG's abnormalities over 48 h (followup request_ambulatory_eeg)
- structured_headache_history_ichd3: the case's headache, prior primary headache and red flags (fallback_tool_outputs.clinical_assessment)
- cognitive_screen: MoCA matching the exam (followup request_cognitive_screen)
- gait_and_balance_timed: matching the exam (followup request_timed_gait_balance)
- neuropsych_battery: domain deficits matching the exam (fallback_tool_outputs.specialized_test)
- audiometry: right sensorineural loss matching the exam (followup request_audiometry)
- MR_venography: right sigmoid-jugular compression as on the stored MRI (followup request_mr_venography)
- whole_body_FDG_PET: the stored jugular foramen mass (followup request_whole_body_fdg_pet)

Checks: `perfect_agent.py` pass; `test_case_guards.py -k GLIO-HG-RS01` pass; no fixed order still answered by the library (`lib4.source`); no 60-character window of any criterion's expected_evidence in the added text, except tissue copies that repeat the stored tissue report verbatim; every criterion's served output unchanged (snapshot diff against the baseline).
