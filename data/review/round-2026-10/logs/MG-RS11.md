# MG-RS11
Reviewer status: not reviewed (no MG notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input applied: July 2026 tool guidance for myasthenia_gravis via plan MG.md (ocular pathway, section 3.5). |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | HPI ended "prompted consideration of myasthenia gravis" (names the diagnosis); "pseudo-INO" presupposes an NMJ cause; mention of the declined ice pack test hinted at MG and pre-empted the scored bedside test; "presented to the neurology ward" contradicted the referral. | FIXED: diagnosis sentence replaced by referral to neurology after normal imaging; "INO-like pattern"; ice pack sentence deleted; "was admitted". Prior imaging (CT orbits, MRI, MRA, MRV) kept as pre-referral history (not scored). |
| D | minor | `patient.neurological_exam.cranial_nerves`, `patient.physical_exam.neurological` | "(pseudo-INO pattern)" in the exam. | FIXED: "without abducting nystagmus" (descriptive). |
| A | minor | `patient` top-level `age`, `ethnicity`, `hpi`, `pmh`, `sex` | Duplicate keys invisible to the agent (class K). | FIXED: ethnicity moved to `demographics.ethnicity`; duplicates removed (they matched the kept fields). |
| B | minor | `patient.physical_exam.general` | No weight or height for the mL/kg value (fact 14). | FIXED: "Weight 78 kg, height 165 cm" (BMI 28.7 as stored). |
| A | major | `followup_outputs[request_achr_musk_lrp4_antibodies]`, `initial_tool_outputs.labs` | First-line serology sat in a follow-up behind a TSH stub "Within reference range" with no unit (classes H6, G); blocking antibody in nmol/L with a % range; MuSK reference <0.4 nmol/L. | FIXED: serology moved to `initial_tool_outputs.labs` (AChR binding 7.6 nmol/L kept, Mayo-style ranges: binding <=0.02, blocking 38% (<=15%), MuSK <0.01 (<=0.02)); thyroid panel TSH 1.9 mIU/L and free T4 1.2 ng/dL; report-voice interpretation; follow-up deleted. |
| C | major | criterion `action-2-order-specialized-test` | SFEMG-only required criterion with expected evidence "Decrement >10%" (an RNS finding), no RNS report. | FIXED: one neurophysiology criterion with alternatives SFEMG and RNS (plan ocular pathway); new RNS follow-up `request_repetitive_nerve_stimulation` (nasalis 7%, trapezius 4%, ADM 2%, no facilitation: normal, as common in ocular MG); SFEMG report given muscle, MCD, % pairs, blocking. |
| C | minor | `metadata.actions_withdrawn`, criteria | Ice pack withdrawn for lack of a result although left ptosis is present. | FIXED: recommended criterion `action-ice-pack-test` with new follow-up `request_ice_pack_test` (left MRD1 1.0 to 3.5 mm); withdrawal entry removed. |
| D | major | `followup_outputs[search_ocular_mg_management]`, criterion `action-4-search-medical-literature` | Literature as a required step; output with unsourced bullets and a respiratory-monitoring recommendation; criterion query unmatchable (exact string). | FIXED: follow-up deleted; one `initial_tool_outputs.literature_search` in report voice (Sanders 2016, Narayanaswami 2021, Gilhus 2016); criterion optional, last, any query. |
| C | major | `followup_outputs[check_amlodipine_mg]`, criterion `action-5-check-drug-interactions` | Generic pyridostigmine drug check required with telithromycin; `proposed` a slug; no concrete interaction (amlodipine, HCTZ). | FIXED: criterion and output deleted (plan 3.2). |
| B | minor | `followup_outputs[request_respiratory_function]` | NIF "meets threshold", FVC without litres or mL/kg, no MEP. | FIXED: FVC 3.02 L (92%, 39 mL/kg), MIP -68, MEP 88 cmH2O, single-breath count 40; criterion optional (ocular). |
| B | minor | `followup_outputs[request_anti_gq1b_miller_fisher]` | Interpretation "makes this diagnosis less likely" (case-steering). | FIXED: templated hedged comment; criterion `action-anti-gq1b` optional (Miller Fisher kept very_low). |
| B | minor | `initial_tool_outputs.ecg` | "Normal ECG" alongside LVH; "consistent with hypertension" (cross-reference). | FIXED: "Sinus rhythm. Left ventricular hypertrophy by voltage criteria. No acute ST-T changes." |
| D | minor | `initial_tool_outputs.body_imaging` | Indication "Newly diagnosed MG" served before diagnosis; region "mediastinum" refused a chest_CT order. | FIXED: "Evaluation for thymoma"; region "chest/mediastinum". |
| D | minor | `fallback_tool_outputs.ct.impression` | "does not address the question" (class F). | FIXED: canonical plain head CT text. |
| C | major | `ground_truth.differential` | "Generalized MG progression risk" listed as a differential diagnosis (high); brainstem INO and orbital cellulitis raised by red herrings but absent. | FIXED: removed (risk moved to key evidence and musts); added brainstem lesion with INO (very_low) and orbital cellulitis/inflammation (very_low); each entry states the excluding result. |
| C | major | `ground_truth.assessment` | Musts were tests ("Confirm AChR", "RNS and ice-pack", "CT chest"); template prohibitions with telithromycin and SFEMG wording. | FIXED: musts: diagnosis with evidence, pyridostigmine titration, low-dose prednisone if needed (HCTZ potassium monitoring), generalization counselling and follow-up, drug-avoidance list; prohibitions: canonical steroid, canonical drug, brainstem-vascular attribution. |
| E | minor | `ground_truth.key_clinical_evidence`, `red_herrings[*]`, `avoided_actions[*]`, criteria labels | Template pearls (telithromycin, "all MG require CT chest"); empty red-herring field paths; Wolfe 2016 cited for EEG, CSF, echo; labels equal to rationales. | FIXED: case-specific evidence; red herrings with field paths; avoided actions with case rationales and Jacob 2025 text citation; distinct labels and rationales. |
| A | minor | `ground_truth.sequence_constraints`, `stop_rule` | labs -> SFEMG constraint with wrong reason; stop rule listed literature and drug check, max 0. | FIXED: constraint removed (labs and neurophysiology run in parallel in ocular MG, plan 3.3); stop rule labs, neurophysiology, mediastinal CT, max 2. |
| E | minor | `metadata.difficulty_rationale`, `difficulty_description` | "typical AChR+ generalized MG, 0 red herrings". | FIXED: ocular, 3 red herrings. |

## Changes, in one paragraph a physician can read before re-reviewing

Ocular AChR-positive MG (MGFA I) in a 52-year-old woman with an INO-like ophthalmoparesis. The HPI no longer names MG or "pseudo-INO" and no longer mentions the ice pack test; the pre-referral normal CT orbits, MRI, MRA and MRV stay as history. Work-up now: AChR binding antibody with thyroid function (required; initial labs: AChR 7.6 nmol/L, blocking 38%, MuSK negative, TSH 1.9, free T4 1.2), neurophysiology (required, SFEMG or RNS: SFEMG orbicularis oculi MCD 54 microseconds, 16% blocking; new RNS without significant decrement), ice pack test (recommended, new result left MRD1 1.0 to 3.5 mm), mediastinal CT with contrast (required, no thymoma), anti-GQ1b, respiratory function and literature optional. The drug check and literature follow-up were removed. Musts: diagnosis, pyridostigmine 30 mg three times daily titrated, low-dose prednisone if disabling symptoms persist (with potassium and glucose monitoring on HCTZ), counselling about generalization with follow-up, and an MG drug-avoidance list. The differential drops "generalization risk" and adds brainstem INO and orbital inflammation, all low or very low with the excluding result.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[Jacob_2025]`, `[Evoli_2019]`, `[Narayanaswami_2021]` used as text citations (plan CENTRAL 1).
- Synonyms: "generalized myasthenia gravis" is accepted for this ocular case (plan CENTRAL 3).
- `mediastinum_MRI` alternative is answered by the library normal report (consistent with no thymoma).

## Open questions for Andrea (judgment calls you could not settle)

- None. The RNS and ice pack results are new data written per plan (ocular MG: RNS commonly normal; ice pack positive with ptosis); a re-reviewer should check that they read as plausible.

## Verification

Verifier, 24 Oct 2026 (adversarial pass; no reviewer notes exist for MG, so the table check is the "no reviewer notes" row).

Checked: every own-finding row against the file (HPI no longer names MG or the ice pack; serology in initial labs with Mayo-style units and % blocking; RNS and SFEMG reports with values; ice pack on the ptotic left lid only; one literature output in report voice; drug check gone; differential without the generalization-risk entry; musts without tests; no thymectomy must in ocular MG); icd_codes and label unchanged; ice pack laterality matches the exam (left ptosis, Cogan left); FVC 3.02 L / 78 kg = 39 mL/kg; no new dashes or British spellings.

- Found (all six RS11-RS16, missed by the worker, PATTERNS 5 discriminators): `fallback_tool_outputs.echo` had no `echo_type` and `fallback_tool_outputs.advanced_imaging` carried a prose modality, so a normal report answered every echo and every advanced-imaging variant. Changed: echo fallback `echo_type: TTE` (its content is a normal TTE); advanced-imaging fallback set to null and `metadata.fallback_tool_kinds.advanced_imaging` removed, so the library answers per modality (probed: MR_angiography and TEE orders get their own library reports).
- No other error found.

Checks re-run after the edits: `perfect_agent.py -v` passes (only the known mediastinum_MRI alternative served by the library normal), `case_io.py check` clean for the case, `test_case_guards.py -k` passes, and the 24 Oct discriminator guard (run by hand; MG is not yet in `DISCRIMINATOR_CONDITIONS`) reports no defect.
