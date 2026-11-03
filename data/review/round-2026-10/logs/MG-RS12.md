# MG-RS12
Reviewer status: not reviewed (no MG notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input applied: July 2026 tool guidance via plan MG.md (generalized AChR+ pathway, section 3.5). |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A | minor | `patient` top-level `age`, `ethnicity`, `hpi`, `pmh`, `sex` | Duplicate keys invisible to the agent (class K). | FIXED: ethnicity "South Asian" moved to `demographics.ethnicity`; duplicates removed (identical to kept fields). |
| B | minor | `patient.physical_exam.general` | No weight or height for mL/kg (fact 14). | FIXED: "Weight 72 kg, height 174 cm" (BMI 23.8 as stored). |
| A | major | `followup_outputs[request_achr_musk_lrp4_antibodies]`, `initial_tool_outputs.labs` | Serology in a follow-up behind a TSH stub with no value or unit (H6, G); blocking antibody in nmol/L with a % range; MuSK reference <0.4. | FIXED: serology moved to `initial_tool_outputs.labs` (AChR binding 11.2 nmol/L kept; Mayo-style ranges; blocking 46%; MuSK <0.01); TSH 2.6 mIU/L, free T4 1.1 ng/dL; follow-up deleted. |
| B | major | `ground_truth.red_herrings[1]`, `[2]` | Red herrings cited an ESR of 22 mm/h and an elevated HbA1c that no report contains (22 mm/h is also normal for a 69-year-old man). | FIXED: HbA1c 8.1% and fasting glucose 158 mg/dL added to the initial labs (relevant to the steroid plan) with field path; ESR red herring deleted. |
| A | major | `initial_tool_outputs.ct`, `followup_outputs[request_thymectomy_evaluation]` | Chest CT stored under the head-CT tool (H3); body-imaging follow-up with `contrast: false` while the criterion requires true (H4). | FIXED: one mediastinal CT report in `initial_tool_outputs.body_imaging` (contrast true, region chest/mediastinum, indication "Evaluation for thymoma", numbered impression); `initial_tool_outputs.ct` deleted (library normal head CT answers); follow-up deleted. |
| C | minor | `initial_tool_outputs.specialized_test` | 50 Hz high-rate RNS (painful; fact 8); impression prose with an en dash. | FIXED: brief-exercise facilitation (4%, none); technique with temperature; numbered impression; quantitative data. Decrements 14/16/12% kept. |
| A | minor | `followup_outputs` (second `request_respiratory_function`, `request_ice_pack_test`) | Unreachable respiratory stub (H2); ice pack and respiratory stubs whose findings repeat the expected text (I). | FIXED: stub deleted; respiratory report FVC 3.35 L (86%, 47 mL/kg), MIP -70, MEP 92 cmH2O, cough effective; ice pack left MRD1 0.5 to 3.0 mm, right 2.5 to 4.0 mm. |
| B | minor | `followup_outputs[request_emg_single_fiber]` | No structured values; en dash. | FIXED: muscle, MCD 58 microseconds, 14/20 pairs, 20% blocking kept; criterion optional (RNS diagnostic). |
| D | major | `followup_outputs[search_lichen_planus_mg_association]`, `[check_metformin_mg_interaction]` | Literature with unsourced HLA claims; drug check for metformin, amlodipine, topical betamethasone with no MG-relevant interaction, `proposed` a slug. | FIXED: both deleted (plan RS12); drug-check criterion deleted; steroid hyperglycaemia is now a must. Literature criterion optional, last, with the canonical initial output. |
| B | minor | `initial_tool_outputs.mri`, `.ecg` | MRI "(age/hypertension)" cross-reference; ECG "Normal ECG" with LVH, same PR/QRS as other cases. | FIXED: "mild nonspecific periventricular white matter changes"; ECG LVH by voltage, PR 176, QRS 92 ms. |
| C | major | `ground_truth.assessment` | Musts were tests ("Confirm AChR", "RNS ... 14-16%", "CT chest"); no swallowing safety despite dysphagia to liquids; template prohibitions (telithromycin, SFEMG wording). | FIXED: musts: diagnosis with evidence, swallowing assessment, pyridostigmine before meals, inpatient prednisone plan with bone protection and azathioprine after TPMT, glucose control on steroids (HbA1c 8.1%), respiratory re-measurement with IVIG/PLEX thresholds. Prohibitions: canonical steroid, canonical drug, diabetic/vascular attribution. No thymectomy must (69, no thymoma; plan). |
| C | minor | `ground_truth.differential` | Key features not tied to results; OPMD (classic late-onset ptosis-dysphagia mimic) missing. | FIXED: each entry states the excluding result; OPMD added very_low; LEMS kept G70.80. |
| E | minor | criteria, `key_clinical_evidence`, `avoided_actions`, `sequence_constraints`, `stop_rule`, `metadata.difficulty_rationale` | Labels equal rationales, Wolfe 2016 everywhere, template pearls, labs -> RNS constraint with SFEMG reason, stop rule with literature and drug check (max 0), "0 red herrings, 5 required". | FIXED: criteria rebuilt per plan 3.2 (labs, RNS, CT required; ice pack, respiratory recommended; SFEMG and literature optional); case-specific evidence; Jacob 2025 text citations; constraint removed; stop rule labs, RNS, CT, max 2; rationale updated. |

## Changes, in one paragraph a physician can read before re-reviewing

Late-onset AChR-positive generalized, predominantly bulbar MG in a 69-year-old man with diabetes and lichen planus. Required work-up: AChR binding antibody with thyroid function (initial labs: AChR 11.2 nmol/L, blocking 46%, MuSK negative, normal TSH and free T4, plus HbA1c 8.1%), 3 Hz RNS (12-16% decrement, no facilitation on brief exercise instead of 50 Hz, normal NCS and needle EMG) and mediastinal CT with contrast (no thymoma; moved from the head-CT slot). Ice pack (left MRD1 0.5 to 3.0 mm) and baseline respiratory function (normal) are recommended; SFEMG and literature optional. Drug check and literature follow-ups were deleted. Musts now include a swallowing assessment, pyridostigmine titration, an inpatient prednisone plan with bone protection and a steroid-sparing agent, glucose management on steroids, and IVIG or PLEX thresholds if bulbar or respiratory function worsens; no thymectomy (age 69 without thymoma). The ESR red herring, which no report supported, was removed.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Text citations `[Jacob_2025]`, `[Evoli_2019]`, `[Lawn_2001]`, `[Narayanaswami_2021]` (plan CENTRAL 1).
- `icd_codes[0]` is G70.01 (with exacerbation) for a stable new diagnosis; left unchanged per ROUND_POLICY 3 (plan CENTRAL 2).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Verifier, 24 Oct 2026 (adversarial pass; no reviewer notes exist for MG, so the table check is the "no reviewer notes" row).

Checked: every own-finding row against the file (chest CT moved to body imaging with contrast, head-CT slot null, stub respiratory deleted, HbA1c and fasting glucose now in the labs the red herring points to, RNS brief-exercise check, musts with swallowing and steroid-glucose plans, no thymectomy must at 69 without thymoma); ice pack sides match the left > right ptosis; FVC 3.35 L / 72 kg = 47 mL/kg; label and ICD unchanged.

- Found (all six RS11-RS16, missed by the worker, PATTERNS 5 discriminators): `fallback_tool_outputs.echo` had no `echo_type` and `fallback_tool_outputs.advanced_imaging` carried a prose modality, so a normal report answered every echo and every advanced-imaging variant. Changed: echo fallback `echo_type: TTE` (its content is a normal TTE); advanced-imaging fallback set to null and `metadata.fallback_tool_kinds.advanced_imaging` removed, so the library answers per modality (probed: MR_angiography and TEE orders get their own library reports).
- No other error found.

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

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 70.4 -> 72 kg, height 172 -> 174 cm, BMI 23.8 -> 23.8 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 72 kg, height 174 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 70, ECOG 2 (cares for self; unable to carry on normal activity or active work) (fallback_tool_outputs.clinical_assessment). Why: rule 1: the library reports Karnofsky 100 / ECOG 0 (no evidence of disease, working); rule 3: bulbar MG with severely reduced gag and dysphagia, unable to continue part-time lecturing.
- `order_specialized_test {test_type: emg_ncs}`: normal nerve conductions and needle EMG, stating that neuromuscular transmission was not assessed (fallback_tool_outputs.specialized_test). Why: rule 1: the library report concludes there is no neuromuscular junction disorder, which routine conductions and needle EMG without repetitive stimulation cannot assess and which is not true here; the stored RNS study reports normal nerve conduction and needle EMG, which this report keeps.
- `order_specialized_test {test_type: speech_language_evaluation}`: fatigable hypernasal dysarthria after 2 minutes; language normal (followup_outputs[3] request_speech_language_evaluation). Why: rule 3: the library reports no dysarthria; the examination documents dysarthria worse in the afternoons with weak palatal elevation.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
