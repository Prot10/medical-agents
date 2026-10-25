# MG-RS14
Reviewer status: not reviewed (no MG notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input applied: July 2026 tool guidance via plan MG.md (MuSK+ pathway, section 3.5). |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| D | blocker | `patient.history_present_illness` | The HPI listed the whole current work-up and its results: chest CT, spirometry, CSF, "Single-fiber EMG was normal", brain MRI, FDG-PET (class K), plus prior AChR antibodies negative while AChR testing is scored. | FIXED: "Extensive investigations" paragraph deleted; the prior-admission history keeps barium swallow, neck CT, autoimmune screen, IV methylprednisolone response, the lactate pair, anti-Hu/Yo/Ri and the muscle biopsy (none scored); prior AChR result removed so the current labs carry it. |
| B | major | `followup_outputs[request_emg_single_fiber]` | SFEMG stub repeating the expected text; the source HPI called the SFEMG normal. | FIXED: real report: normal jitter in extensor digitorum (29 microseconds), abnormal in orbicularis oculi (52 microseconds, 60% pairs, 10% blocking), the facial-predominant MuSK pattern (plan RS14). |
| A | major | `initial_tool_outputs.labs`, `followup_outputs[request_musk_antibodies]` | TSH stub only in the initial labs; MuSK follow-up with Mayo-style values against a <0.4 range. | FIXED: initial labs AChR binding <0.01 nmol/L, modulating 8%, TSH 2.1, free T4 1.2; MuSK follow-up holds the full panel with MuSK 42 nmol/L (reference <=0.02), so an order of AChR plus MuSK together receives the whole report (checked through the MockServer). MuSK kept as a separate required criterion with a soft AChR -> MuSK constraint. Plan H6 asked for MuSK in the initial labs; that would hand the decisive MuSK result to any first lab order, so it stays a follow-up. |
| A | major | `followup_outputs[request_ice_pack_test]`, criterion `action-8` | Ice pack criterion and stub in a man without ptosis (fact 9). | FIXED: both deleted; an ice pack order is answered by the library normal (no ptosis). |
| A | major | `initial_tool_outputs.csf`, `followup_outputs[request_fdg_pet_report]` | CSF in the initial outputs (fact 13); FDG-PET brain filed with a prose modality (H5). | FIXED: both deleted; CSF added as a waste avoided action; FDG-PET and CSF orders fall to the library normal. |
| A | minor | second `request_respiratory_function` | Unreachable stub (H2). | FIXED: deleted. |
| C | major | `followup_outputs[request_respiratory_function]` | FVC 76% and NIF -58 called "borderline" with "no immediate compromise"; no litres, mL/kg or MEP. | FIXED: FVC 2.43 L (76%, 35 mL/kg) L, MIP -58 L, MEP 64 L, weak cough; impression states mild weakness above the 20/30/40 thresholds; criterion required and first (severe bulbar, plan 3.1 item 7). Weight 69 kg, height 168 cm added to `physical_exam.general` (BMI 24.4 as stored). |
| B | minor | `followup_outputs[request_repetitive_nerve_stimulation]` | No CMAPs or technique; en dash. | FIXED: technique, CMAPs, brief-exercise check; decrements 22/18/6% kept; numbered impression. |
| A | minor | `initial_tool_outputs.body_imaging` | `contrast: false` against a contrast criterion (H4); "paraneoplastic lung cancer screen" indication. | FIXED: contrast true, region chest/mediastinum, "Evaluation for thymoma", numbered impression. |
| C | minor | `initial_tool_outputs.mri` | PSP is the main mimic (downgaze restriction, axial rigidity) but the MRI did not report the midbrain. | FIXED: "no midbrain atrophy (normal midbrain-to-pons proportion)" added; brain MRI an optional criterion. |
| B | minor | `initial_tool_outputs.ecg` | Interpretation "See report details above."; template PR/QRS and rate 72 against HR 68. | FIXED: real interpretation; rate 68, PR 184, QRS 96, QTc 448 kept. |
| D | major | `followup_outputs[search_musk_mg_treatment]`, `[check_musk_mg_parkinson_interaction]` | Literature with ">75% response ... small RCTs" (no RCT exists); drug check built around rituximab, a treatment plan. | FIXED: both deleted; one initial literature output (Sanders 2016 and update on MuSK MG; Punga 2022), one initial drug output (pyridostigmine against levodopa-carbidopa and amlodipine, muscarinic warning); criteria optional. |
| C | major | `ground_truth.assessment` | Musts were tests (confirm MuSK, SFEMG, CT); no acute therapy for MGFA IVb disease; template prohibitions. | FIXED: musts: diagnosis (MGFA IVb), PLEX first (IVIG alternative), inpatient prednisone with early rituximab if inadequate, cautious low-dose pyridostigmine, NG feeding and swallow assessment, daily FVC/MIP with ICU thresholds, later reassessment of parkinsonism. Prohibitions: canonical steroid, canonical drug, no thymectomy in MuSK MG, no attribution to PD or PSP before MuSK and neurophysiology. |
| C | major | `ground_truth.differential` | PD, ALS and AChR MG left moderate after the results; PSP-MSA lumped; mitochondrial disease raised by a red herring but absent. | FIXED: PSP low, PD (as cause) low, ALS low, AChR MG very_low, mitochondrial myopathy very_low, brainstem stroke very_low, each with the excluding result. |
| E | minor | criteria, `key_clinical_evidence`, `red_herrings`, `avoided_actions`, `sequence_constraints`, `stop_rule`, `patient` extra keys, PMH dash, metadata | Template content (labels equal rationales, Wolfe 2016, "SFEMG is the test of choice" pearls, rituximab claim), empty red-herring paths, wrong constraint, stop rule with literature and drug check (max 0), duplicate keys, em dash, "1 red herrings". | FIXED: criteria per plan 3.5 MuSK row (respiratory, AChR+TSH, RNS, MuSK, CT required; SFEMG recommended; brain MRI, drug check, literature optional); constraints labs -> MuSK, labs -> SFEMG, RNS -> SFEMG (soft); stop rule the five required, max 2; case-specific evidence; red-herring paths; ethnicity to demographics; dash removed; difficulty text updated; `fallback_tool_kinds.csf` removed (no case CSF fallback). |

## Changes, in one paragraph a physician can read before re-reviewing

MuSK antibody-positive MG with severe bulbar and oculomotor weakness (MGFA IVb, nasogastric tube) in a 75-year-old man with parkinsonism. The HPI no longer reports the current admission's investigations (it had listed chest CT, spirometry, CSF, a normal SFEMG, MRI and FDG-PET), and the prior AChR result was removed so the agent must order it. Pathway: respiratory function first (mildly reduced, 35 mL/kg, weak cough), AChR with thyroid function (negative, normal), RNS with facial muscles (22% nasalis, 18% orbicularis, 6% ADM), MuSK antibody (42 nmol/L), SFEMG recommended (normal limb, abnormal orbicularis oculi), mediastinal CT with contrast (no thymoma); brain MRI (now reporting no midbrain atrophy), drug check and literature optional. Ice pack (no ptosis), CSF and FDG-PET were removed. Musts: plasma exchange, inpatient prednisone with early rituximab, cautious pyridostigmine, nasogastric feeding and swallow assessment, daily respiratory measurements with ICU thresholds; prohibitions include thymectomy. The differential has PSP, PD and ALS low with the results that exclude them.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Text citations `[Jacob_2025]`, `[Evoli_2019]`, `[Lawn_2001]`, `[Narayanaswami_2021]` (plan CENTRAL 1).
- `icd_codes[0]` G70.01; the case is an active severe presentation, so G70.01 (with exacerbation) is arguably right here, unlike the stable cases (plan CENTRAL 2).
- Synonyms: no MuSK-specific label exists; "ocular myasthenia gravis" is accepted for this generalized case (plan CENTRAL 3).

## Open questions for Andrea (judgment calls you could not settle)

- Departure from plan H6, decided on leakage grounds: the MuSK result stays in a follow-up (holding the full antibody panel) rather than the initial labs, so it is returned only when MuSK is ordered.

## Verification

Verifier, 24 Oct 2026 (adversarial pass; no reviewer notes exist for MG, so the table check is the "no reviewer notes" row).

Checked: the HPI no longer lists the admission work-up or a prior AChR result; MuSK stays in a follow-up (probed: an AChR+TSH order gets the AChR-negative initial labs, an order including anti_MuSK gets the full panel with MuSK 42 nmol/L); ice pack, CSF output and FDG-PET follow-up gone; respiratory values flagged low with FVC 2.43 L / 69 kg = 35 mL/kg; SFEMG facial-predominant pattern; MGFA IVb fits a feeding tube without intubation; PLEX-first and no-thymectomy musts fit MuSK MG; constraints only soft.

- Found (all six RS11-RS16, missed by the worker, PATTERNS 5 discriminators): `fallback_tool_outputs.echo` had no `echo_type` and `fallback_tool_outputs.advanced_imaging` carried a prose modality, so a normal report answered every echo and every advanced-imaging variant. Changed: echo fallback `echo_type: TTE` (its content is a normal TTE); advanced-imaging fallback set to null and `metadata.fallback_tool_kinds.advanced_imaging` removed, so the library answers per modality (probed: MR_angiography and TEE orders get their own library reports).
- Found: one British spelling in new patient text ("fibre atrophy" in the HPI) against the case's American spelling. Changed to "fiber atrophy".

Checks re-run after the edits: `perfect_agent.py -v` passes (only the known mediastinum_MRI alternative served by the library normal), `case_io.py check` clean for the case, `test_case_guards.py -k` passes, and the 24 Oct discriminator guard (run by hand; MG is not yet in `DISCRIMINATOR_CONDITIONS`) reports no defect.

## Close-out (24 Oct 2026)

- `ground_truth.diagnosis.icd_codes[0]` G70.01 -> G70.00. ICD-10-CM G70.01 is myasthenia gravis with (acute) exacerbation, including crisis; this is a new or stable presentation, not an exacerbation. G70.01 stays accepted as a secondary code (plans/MG-decisions.md, Q2).
- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Scoped subtype synonyms added: MuSK labels (MuSK myasthenia gravis, MuSK MG, ...).
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG', 'MuSK myasthenia gravis', 'MuSK antibody positive myasthenia gravis', 'anti-MuSK myasthenia gravis', 'MuSK MG']; icd_codes = ['G70.00', 'G70.0', 'G70.01']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 68.9 -> 69 kg, height 168 -> 168 cm, BMI 24.4 -> 24.4 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 69 kg, height 168 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.
