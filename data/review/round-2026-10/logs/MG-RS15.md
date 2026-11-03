# MG-RS15
Reviewer status: not reviewed (no MG notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input applied: July 2026 tool guidance via plan MG.md (generalized AChR+ pathway, section 3.5). |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A | major | `followup_outputs[request_neostigmine_challenge]`, criterion `action-8-order-specialized-test` | Neostigmine challenge filed under a prose `test_type` (not orderable, H5); it answered the ice pack criterion (perfect-agent warning) in a woman without ptosis. | FIXED: neostigmine follow-up deleted; ice pack criterion deleted (no ptosis, fact 9); an ice pack order now gets the library normal (no ptosis), consistent with the exam. Neostigmine mentions removed from red herrings and metadata. |
| A | major | criterion `action-3-order-specialized-test` | SFEMG recommended with no SFEMG report in the case (an order would get the library normal, contradicting the diagnosis). | FIXED: SFEMG optional (RNS diagnostic, plan 3.2) with a new report (frontalis MCD 46 microseconds, 45% pairs, 8% blocking). |
| A | major | `followup_outputs[request_achr_musk_lrp4_antibodies]`, `initial_tool_outputs.labs` | Serology behind a TSH stub (H6, G); blocking in nmol/L; MuSK <0.4. | FIXED: initial labs AChR binding 1.11 nmol/L (kept), blocking 27%, MuSK <0.01 (Mayo-style), TSH 1.4, free T4 1.1; follow-up deleted. |
| A | minor | `initial_tool_outputs.body_imaging` | `contrast: false` against the criterion (H4); "Newly suspected MG" indication with an em dash. | FIXED: contrast true, region chest/mediastinum, "Evaluation for thymoma". |
| B | minor | `followup_outputs[request_respiratory_function]` | "meets threshold for adequate"; no litres, mL/kg or MEP. | FIXED: FVC 2.77 L (94%, 47 mL/kg), MIP -74, MEP 86 cmH2O, effective cough; weight 59 kg, height 158 cm in `physical_exam.general` (BMI 23.6 as stored); recommended (laryngeal weakness). |
| B | minor | `followup_outputs[request_repetitive_nerve_stimulation]`, `initial_tool_outputs.mri`, `.ecg` | RNS without CMAPs or technique (en dash); brain MRI tool reporting "brain and spine" and a clinical inference; ECG template PR/QRS, rate 72 against HR 74. | FIXED: RNS technique, CMAPs, exercise check, decrements 13/11/4% kept; MRI "Normal MRI of the brain, including the brainstem"; ECG rate 74, PR 154, QRS 84. |
| B | minor | `patient.history_present_illness` | "Neurological examination was entirely normal" followed by palatal weakness. | FIXED: "otherwise normal". |
| D | major | `followup_outputs[search_hypophonia_mg]`, `[check_pyridostigmine_constipation]`, criteria `action-5`, `action-6` | Literature with a patient-steering summary ("neostigmine challenge and AChR antibody testing are key diagnostic steps"); drug check for psyllium and docusate, no interaction; both required. | FIXED: both outputs deleted; canonical initial literature output, literature optional; drug-check criterion deleted (plan RS15). The pyridostigmine effect on constipation is in the must. |
| C | major | `ground_truth.assessment` | Musts were tests and "ENT/laryngoscopy (already considered)" (done in the history); no thymectomy must at 53. | FIXED: musts: diagnosis (MGFA IIb), pyridostigmine (bowel effect noted), low-dose prednisone and azathioprine after TPMT if needed, thymectomy per MGTX, speech and language therapy with red-flag advice. ENT must deleted (laryngoscopy is in the HPI). Prohibitions: canonical steroid, canonical drug, functional-dysphonia attribution. |
| C | major | `ground_truth.differential` | Functional aphonia left moderate; Parkinson hypophonia raised by a red herring but absent; key features not tied to results. | FIXED: functional low; PD, vocal fold paralysis, ALS, MuSK MG, laryngeal lesion very_low with the excluding data (laryngeal lesion code D38.0). |
| E | minor | criteria, `key_clinical_evidence`, `red_herrings`, `avoided_actions`, `sequence_constraints`, `stop_rule`, `patient` extra keys, `metadata` | Template text (labels equal rationales, Wolfe 2016, telithromycin), empty red-herring paths, wrong labs -> RNS constraint, stop rule with literature and drug check (max 0), duplicate keys, "0 red herrings". | FIXED: criteria per plan 3.2; constraint removed; stop rule labs, RNS, CT, max 2; case-specific evidence; red-herring paths; ethnicity to demographics; difficulty text updated. |

## Changes, in one paragraph a physician can read before re-reviewing

AChR-positive MG presenting as isolated fatigable hypophonia in a 53-year-old woman after a normal laryngoscopy. The neostigmine challenge (not an orderable study) and the ice pack test (no ptosis) were removed. Required: AChR serology with thyroid function (AChR 1.11 nmol/L, blocking 27%, MuSK negative), RNS with facial muscles (13% nasalis, 11% orbicularis, none in ADM) and mediastinal CT with contrast (no thymoma); respiratory function recommended (normal); SFEMG (new report, abnormal frontalis jitter) and literature optional; the drug check was removed. Musts: pyridostigmine, low-dose prednisone and azathioprine if needed, thymectomy per MGTX at 53, speech and language therapy with red flags. Functional dysphonia is low and Parkinson hypophonia very low in the differential.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Text citations `[Jacob_2025]`, `[Evoli_2019]`, `[Lawn_2001]`, `[Narayanaswami_2021]` (plan CENTRAL 1).
- `icd_codes[0]` G70.01 for a stable new diagnosis (plan CENTRAL 2).

## Open questions for Andrea (judgment calls you could not settle)

- The thymectomy must is added on plan fact 20 and class D (generalized AChR+ MG under 66 without thymoma); the per-case plan entry did not mention it. Bulbar-only MG is generalized in the MGFA classification.

## Verification

Verifier, 24 Oct 2026 (adversarial pass; no reviewer notes exist for MG, so the table check is the "no reviewer notes" row).

Checked: neostigmine follow-up and ice pack criterion gone (no ptosis; probed: an ice pack order gets the library no-ptosis report); SFEMG report now exists for the optional criterion; serology in initial labs; laryngoscopy in the HPI so no ENT must; thymectomy must for bulbar (generalized, IIb) AChR+ MG at 53 is consistent with MGTX inclusion (class II-IV); FVC 2.77 L / 59 kg = 47 mL/kg.

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

- `patient.demographics`: weight 55.2 -> 59 kg, height 153 -> 158 cm, BMI 23.6 -> 23.6 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 59 kg, height 158 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 80, ECOG 1 (normal activity with effort; some signs and symptoms) (fallback_tool_outputs.clinical_assessment). Why: rule 1: the library reports Karnofsky 100 / ECOG 0 (no evidence of disease, working); rule 3: fatigable hypophonia interfering with her work as a teacher.
- `order_specialized_test {test_type: emg_ncs}`: normal nerve conductions and needle EMG, stating that neuromuscular transmission was not assessed (fallback_tool_outputs.specialized_test). Why: rule 1: the library report concludes there is no neuromuscular junction disorder, which routine conductions and needle EMG without repetitive stimulation cannot assess and which is not true here; the stored RNS study reports normal nerve conductions, which this report keeps.
- `order_specialized_test {test_type: speech_language_evaluation}`: fatigable hypophonia with volume decrement on sustained phonation; language normal (followup_outputs[3] request_speech_language_evaluation). Why: rule 3: the library reports no dysarthria; the examination documents low-volume speech with a progressive volume decrement on sustained vowels.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
