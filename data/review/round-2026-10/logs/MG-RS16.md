# MG-RS16
Reviewer status: not reviewed (no MG notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input applied: July 2026 tool guidance via plan MG.md (generalized AChR+ pathway, section 3.5). |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A | major | `followup_outputs[request_achr_musk_lrp4_antibodies]`, `initial_tool_outputs.labs` | Serology behind a TSH-stub initial lab (H6, G); blocking antibody in nmol/L against a % range; MuSK <0.4; the CK of 78 U/L quoted by a red herring was in no lab output. | FIXED: initial labs AChR binding 8.0 nmol/L (kept), blocking 62%, MuSK <0.01 (Mayo-style), CK 78 U/L, TSH 2.3, free T4 1.2, HbA1c 7.4% (known diabetes, steroid planning); follow-up deleted. |
| B | major | `patient.history_present_illness` | "was on no medications prior to admission" against four listed medicines; "neck flexion weakness" against 2/5 extensors; no fatigability described; MRI results and a steering sentence ("highly atypical for Parkinson's disease, which prompted dedicated neuromuscular evaluation"). | FIXED: medicines listed, statin long-standing; extensor weakness; diurnal worsening of head drop, dysphagia and voice added; MRI paragraph and steering sentence removed (MRI stays in its tool output). |
| A | major | `followup_outputs[request_ice_pack_test]`, criterion `action-8` | Ice pack criterion and stub in a man without ptosis (fact 9). | FIXED: both deleted; an ice pack order gets the library normal (no ptosis). |
| A | minor | second `request_respiratory_function` | Unreachable stub (H2). | FIXED: deleted. |
| B | minor | `followup_outputs[request_respiratory_function]` | NIF -64 and FVC 88% "adequate"; no litres, mL/kg or MEP; no weight for mL/kg. | FIXED: FVC 3.30 L (88%, 39 mL/kg), MIP -64 (lower limit), MEP 78 cmH2O, effective cough; weight 84 kg, height 174 cm in `physical_exam.general` (BMI 27.7 as stored); recommended (bulbar symptoms, planned steroids). |
| B | minor | `initial_tool_outputs.specialized_test`, `followup_outputs[request_emg_single_fiber]` | RNS without CMAPs or exercise check, em dashes; SFEMG with null quantitative data, micro sign and em dash. | FIXED: RNS technique, CMAPs, brief-exercise check, decrements 19/16/12/5% kept, needle EMG listing muscles, numbered impression; SFEMG structured (MCD 72 microseconds, 26% blocking kept), optional. |
| B | minor | `initial_tool_outputs.ecg`, `.mri`, `.body_imaging`, `patient.physical_exam.respiratory` | ECG "Mild LVH ... Normal ECG", rate 72 against HR 70; MRI not numbered; CT indication "Newly suspected MG" with em dash; unexplained "decreased breath sounds at right base" with a normal chest CT. | FIXED: ECG rate 70, LVH voltage stated without "normal ECG"; MRI numbered (nigral SWI "of uncertain significance"); CT "Evaluation for thymoma", region chest/mediastinum; chest clear. |
| D | major | `followup_outputs[search_head_drop_mg_neck_extensors]`, `[request_mgtx_thymectomy]`, `[check_atorvastatin_mg_interaction]`, criteria `action-5`, `action-6` | Two literature outputs, one a differential tutorial for this case, one answering the thymectomy question for age 73; drug check built around the statin red herring; both required. | FIXED: all three deleted; canonical initial literature output (optional); initial drug output keyed pyridostigmine with the statin association noted (optional). |
| C | major | `ground_truth.assessment` | Musts were tests ("Confirm AChR", "RNS", "CT"); template prohibitions (telithromycin, "single-fiber EMG workup"). | FIXED: musts: diagnosis (MGFA IIIa, axial predominance), pyridostigmine with bradycardia caution, low-start prednisone with glucose monitoring and early azathioprine, cervical collar, swallowing assessment with red flags. Prohibitions: canonical steroid, canonical drug, attribution to PD antecollis. No thymectomy must (73, no thymoma). |
| C | major | `ground_truth.differential` | INEM moderate after a decrement, AChR positivity and normal needle EMG; "camptocormia" mislabel; statin myopathy raised by a red herring but absent. | FIXED: INEM low, PD antecollis low, myelopathy, ALS, IBM and statin myopathy very_low, each with the excluding result; INEM code G72.89. |
| E | minor | criteria, `key_clinical_evidence`, `red_herrings`, `avoided_actions`, `sequence_constraints`, `stop_rule`, `patient` extra keys, `metadata` | Template text (Wolfe 2016 everywhere, "SFEMG sensitivity >95%", thyroid eye disease), three red herrings with empty paths, labs -> RNS constraint, stop rule with literature and drug check (max 0), duplicate ethnicity key, "1 red herrings". | FIXED: criteria per plan 3.5; constraint removed; stop rule labs, RNS, CT, max 2; case-specific evidence; red-herring paths; ethnicity to demographics; difficulty text and condition name updated; class F head CT fallback; British spellings changed to American in RS11-RS16. |

## Changes, in one paragraph a physician can read before re-reviewing

AChR-positive MG presenting as head drop (neck extensors 2/5) with mild fatigable dysphagia and dysphonia in a 73-year-old man with coexisting parkinsonism, diabetes and coronary disease. The HPI no longer says he took no medicines (he takes metformin, amlodipine, aspirin and atorvastatin), describes the evening worsening, and no longer reports the MRI or the reasoning that led to neuromuscular testing. Required: AChR serology with thyroid function (AChR 8.0 nmol/L, blocking 62%, MuSK negative, CK normal), RNS with neck, trapezius and nasalis decrements and a normal needle EMG, and mediastinal CT with contrast (no thymoma); respiratory function recommended (normal, MIP at the lower limit); SFEMG, the drug check and literature optional; the ice pack test (no ptosis) and two literature outputs were removed. Musts: pyridostigmine, low-start prednisone with glucose monitoring and early azathioprine, a cervical collar and a swallowing assessment; thymectomy is not required at 73 without thymoma. Neck extensor myopathy and Parkinson antecollis are low, statin myopathy very low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Text citations `[Jacob_2025]`, `[Evoli_2019]`, `[Lawn_2001]`, `[Narayanaswami_2021]` (plan CENTRAL 1).
- `icd_codes[0]` G70.01 for a stable new diagnosis (plan CENTRAL 2).
- Synonyms: "ocular myasthenia gravis" is accepted for this generalized case (plan CENTRAL 3).

## Open questions for Andrea (judgment calls you could not settle)

- MGFA class IIIa is my call for 2/5 neck extensor weakness with mild bulbar symptoms; class II would also be defensible if neck weakness is judged mild in function.
- The statin is kept (coronary disease) with the reported association noted in the drug output; no must asks to stop it.

## Verification

Verifier, 24 Oct 2026 (adversarial pass; no reviewer notes exist for MG, so the table check is the "no reviewer notes" row).

Checked: HPI medication contradiction fixed and the MRI and steering sentence removed; CK 78 U/L now in the labs the red herring cites; ice pack removed (no ptosis); RNS with needle EMG; differential and musts consistent (no thymectomy at 73 without thymoma; cervical collar, swallowing).

- Found (all six RS11-RS16, missed by the worker, PATTERNS 5 discriminators): `fallback_tool_outputs.echo` had no `echo_type` and `fallback_tool_outputs.advanced_imaging` carried a prose modality, so a normal report answered every echo and every advanced-imaging variant. Changed: echo fallback `echo_type: TTE` (its content is a normal TTE); advanced-imaging fallback set to null and `metadata.fallback_tool_kinds.advanced_imaging` removed, so the library answers per modality (probed: MR_angiography and TEE orders get their own library reports).
- Found: `red_herrings[0].intended_effect` still said "Parkinson camptocormia" although the log says the camptocormia mislabel was fixed (head drop is antecollis, camptocormia is trunk flexion). Changed to "Attribute the head drop to Parkinson disease antecollis and miss MG."
- Found: the respiratory report used an MEP lower limit of >=60 cmH2O for a 73-year-old man while the other male MG RS cases (RS12, RS14) use >=80 cmH2O; MEP 78 would be low on that scale yet the report and criterion called it normal. Changed to reference >=80 cmH2O and MEP 88 cmH2O in findings, quantitative_data, impression and `action-7` expected_evidence (the case's normal-respiratory picture is unchanged).

Checks re-run after the edits: `perfect_agent.py -v` passes (only the known mediastinum_MRI alternative served by the library normal), `case_io.py check` clean for the case, `test_case_guards.py -k` passes, and the 24 Oct discriminator guard (run by hand; MG is not yet in `DISCRIMINATOR_CONDITIONS`) reports no defect.

## Condition audit (MG auditor, 24 Oct 2026)

- sequence constraint added: action-1-interpret-labs -> action-3-order-specialized-test (soft). FIXED.
  Why: plan MG.md 3.3 sets soft labs -> SFEMG and RNS -> SFEMG wherever an SFEMG criterion exists; these were missing here and present in the sibling cases.
- sequence constraint added: action-2-order-specialized-test -> action-3-order-specialized-test (soft). FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.

## Close-out (24 Oct 2026)

- `ground_truth.diagnosis.icd_codes[0]` G70.01 -> G70.00. ICD-10-CM G70.01 is myasthenia gravis with (acute) exacerbation, including crisis; this is a new or stable presentation, not an exacerbation. G70.01 stays accepted as a secondary code (plans/MG-decisions.md, Q2).
- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG']; icd_codes = ['G70.00', 'G70.0', 'G70.01']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
