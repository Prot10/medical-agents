# MG-RP14
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MG) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. July 2026 tool guidance (Reviewer 2) applied through the plan: fixed serology order, RNS technique, SFEMG in seronegative patients, mediastinal imaging in every case, no CSF. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.cranial_nerves`, `patient.physical_exam.neurological` | The ice pack result (3 mm bilaterally) was in the HPI and exam while the ice pack test is a scored criterion; the HPI also reported laboratory results (antiphospholipid antibodies, prolonged PTT) that belong in the labs output. | FIXED: ice pack result and lab results removed from the patient block; HPI keeps the TIA concern; em dash removed in the edited sentence. |
| B | minor | `patient.physical_exam.general`, `.abdomen`, `.extremities`, `past_medical_history[0]` | No weight or height for the respiratory report; unexplained "mild tenderness right iliac fossa (not acutely relevant)"; APS entry without thrombosis status. | FIXED: weight 67 kg, height 165 cm (BMI 24.6 as stored); abdomen non-tender; no livedo; APS recorded as obstetric, no prior thrombosis. |
| A | major | `initial_tool_outputs.labs`, follow-up `request_achr_musk_lrp4_antibodies` | Serology behind a TSH stub (plan H6); AChR and MuSK reference <0.4; blocking reference <25% without unit; TSH without units. | FIXED: initial labs hold AChR binding <0.02 and modulating 6% (negative), MuSK <0.02, TSH 2.4, free T4 13.9, the APS profile (aCL 62, anti-beta2-GPI 48, lupus anticoagulant dRVVT 1.6, aPTT 44 s not corrected by mixing, PT and platelets normal) and chemistry. The follow-up now holds the cell-based panel (clustered AChR, clustered MuSK, LRP4 negative), trigger `request_clustered_achr_cell_based_assay_lrp4`. |
| C | minor | `followup_outputs` RNS, SFEMG | RNS without facilitation or NCS (LEMS was in the differential); SFEMG of one muscle without fibre-pair count. | FIXED: RNS technique, decrements, no facilitation, normal NCS; SFEMG of orbicularis oculi (15 of 20 pairs, 26% blocking) and EDC (9 of 20 pairs). |
| D | major | `followup_outputs` respiratory, ice pack | Stubs whose findings repeated the expected evidence (plan I). | FIXED: respiratory FVC 2.9 L (88%, 43.3 mL/kg), MIP -52, MEP 66 (L), single-breath count 30, mouth seal caveat; ice pack MRD1 values (3 and 2.5 mm improvement). |
| D | major | `followup_outputs` literature, echo | Literature summary patient-specific (plan B); echo for Libman-Sacks screening without murmur or cardiac symptom (plan RP14). | FIXED: literature follow-up deleted, one initial output in report voice (Sanders 2016 / Narayanaswami 2021, Gilhus 2019), criterion optional `{}`. Echo criterion and follow-up deleted; an echo order gets the library normal, unscored. |
| C | minor | `followup_outputs` drug check | `proposed` a trigger slug; content limited to aspirin. | FIXED: trigger `check_prednisone_pyridostigmine_aspirin_interactions`, `proposed` prednisone; aspirin GI risk; steroid and IVIG thrombotic risk with antiphospholipid antibodies; azathioprine TPMT/NUDT15 and warfarin. Criterion optional `{}` (plan 3.2). |
| A | major | `ground_truth.action_criteria` | Template criteria: labs with LRP4; literature and generic pyridostigmine check required with telithromycin; labels equal rationales; `[Wolfe_2016]` everywhere. | FIXED: labs `["anti_AChR","anti_MuSK","TSH"]` (or `thyroid`) required; RNS, SFEMG and mediastinum or chest CT required; cell-based panel (or LRP4), ice pack and respiratory recommended; drug check and literature optional. New labels and rationales. |
| A | minor | `sequence_constraints`, `stop_rule` | `labs -> RNS` with an SFEMG reason; max 0 with literature and drug check required. | FIXED: `RNS -> SFEMG` and `standard labs -> cell-based panel`, both soft; stop rule labs, RNS, SFEMG, CT; max 2. |
| D | minor | `initial_tool_outputs.body_imaging`, `.ecg`, `.mri` | CT region "mediastinum" let a `chest_CT` order fall to the library; ECG indication cited APS valves; MRI impression did not name the brainstem. | FIXED: region "chest and mediastinum" (probe: `chest_CT` now served from the case); ECG indication "Baseline"; MRI impression states no brainstem lesion. |
| C | major | `ground_truth.assessment` | Musts were tests (CBA, SFEMG, CT, echo); no treatment. | FIXED: seronegative diagnosis explained; pyridostigmine before meals; low-dose prednisone inpatient with azathioprine after TPMT/NUDT15; haematology plan for steroids and rescue (VTE prophylaxis, plasma exchange preferred over IVIG); swallow assessment and monitoring. No sulfonamide named (allergy). Prohibitions: canonical drug and steroid texts; attribution text with vertebrobasilar ischaemia from APS. No thymectomy must (seronegative, no thymoma). |
| C | major | `ground_truth.differential` | APS CNS, MS and MuSK MG moderate after a normal MRI and negative MuSK (plan M). | FIXED: APS brainstem ischaemia and MS low; MuSK MG, LEMS, thyroid eye disease (new) and functional disorder very_low, each with the excluding data. |
| E | minor | `ground_truth.red_herrings`, `key_clinical_evidence` | Red herrings with empty paths, one duplicating the APS entry; template evidence (telithromycin, "all confirmed MG"). | FIXED: three red herrings with paths (APS/TIA, aPTT, negative antibodies); case-specific evidence. |
| C | minor | `fallback_tool_outputs.ct`, `.advanced_imaging`, avoided actions, patient extra keys | Head CT fallback "does not address the question" (F); FDG-PET modality label; template waste rationales with `[Wolfe_2016]`; duplicate patient keys. | FIXED: plain head CT text; neutral advanced-imaging fallback; case rationales, citations cleared; ethnicity in `demographics`, duplicates dropped; `metadata.difficulty_rationale` updated. |

## Changes, in one paragraph a physician can read before re-reviewing

A 44-year-old woman with obstetric antiphospholipid syndrome on aspirin is admitted with eight weeks of fatigable diplopia, ptosis, chewing fatigue, nasal dysarthria and dysphagia, worse at the end of meals and of the day, with Cogan lid twitch and fatigable neck flexion; a basilar TIA was the first concern. The ice pack result and the APS laboratory values are no longer in the history: the ice pack test is ordered and scored, and the antiphospholipid profile with a lupus-anticoagulant aPTT (not corrected by mixing) appears in the labs. The pathway: AChR, MuSK and thyroid function in one initial panel (required; all negative), RNS (required; facial and hand decrement, no facilitation), single-fibre EMG (required; increased jitter and blocking in two muscles), contrast CT of the chest and mediastinum (required; no thymoma), a cell-based antibody panel, ice pack and respiratory function (recommended), and optional drug check and literature. The echocardiogram is gone (no cardiac question). Musts start pyridostigmine and cautious steroids with azathioprine, and plan steroids and rescue treatment with haematology because steroids and IVIG raise thrombotic risk in APS. APS brainstem ischaemia and MS are now low, MuSK MG very_low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[Jacob_2025]`, `[Evoli_2019]`, `[Narayanaswami_2021]` (plan 5.1); cited by name until they exist.
- Synonyms (plan 5.3): "ocular myasthenia gravis" is accepted for this generalized case; consider "seronegative myasthenia gravis" as an accepted label if not already expanded.

## Open questions for Andrea (judgment calls you could not settle)

- Rescue therapy in APS: the must prefers plasma exchange over IVIG because of thrombotic risk; some centres give IVIG slowly with prophylaxis. Kept as a preference, not a prohibition; please confirm.
- Echo deleted rather than kept optional (plan allowed either); no murmur or cardiac symptom in the case.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the plan (seronegative pathway, RP14 entry) and the whole final case. Checked: no reviewer notes exist; every FIXED own finding is in the file (ice pack and APS laboratory values out of the patient block, AChR/MuSK/TSH in the initial labs with one laboratory, the cell-based panel as a separate follow-up and recommended criterion with a soft labs -> CBA constraint, SFEMG required with two muscles and pair counts, echo removed, drug check optional in checker voice, APS thrombotic risk in the musts). Arithmetic: FVC 2.9 L / 67 kg = 43.3 mL/kg, BMI 67/1.65^2 = 24.6; MRD1 1 to 4 and 2 to 4.5 mm match 3 and 2.5 mm; aPTT 44 s with 42 s on mixing is an inhibitor pattern consistent with the lupus anticoagulant. No sulfonamide is named anywhere (allergy). The Gilhus 2019 citation (Nat Rev Dis Primers 2019;5:30) exists and says what it is cited for. No thymectomy must is consistent with seronegative MG without thymoma. The differential's MRI/MRA statements rest on a stored initial MRI that is not scored; acceptable as the assessment-time view, since RNS and SFEMG alone exclude the vascular and demyelinating mimics.

Found: nothing requiring a change. The open question on plasma exchange versus IVIG in APS stands as logged.

Re-ran `perfect_agent.py MG-RP14 -v` (pass), `case_io.py check` (clean for the case) and the case guards (pass).

## Condition audit (MG auditor, 24 Oct 2026)

- fallback_tool_outputs.advanced_imaging (empty modality) set to null; metadata.fallback_tool_kinds.advanced_imaging removed. FIXED.
  Why: a fallback with an empty modality answers every advanced-imaging study with one generic report; the benchmark library now serves the normal report for the study actually ordered.
- sequence constraint added: action-1-interpret-labs -> action-3-order-specialized-test (soft). FIXED.
  Why: plan MG.md 3.3 sets soft labs -> SFEMG and RNS -> SFEMG wherever an SFEMG criterion exists; these were missing here and present in the sibling cases.
- action-1-interpret-labs.citations: [Sanders_2016] (management guidance) -> [Punga_2022] (antibody biomarkers), plan 1.1. FIXED.
  Why: plan 1.1 reserves [Sanders_2016] for management; antibody testing cites the biomarker key [Punga_2022].
- action-3-order-specialized-test (SFEMG).citations: [Sanders_2016] removed (says nothing on SFEMG); Jacob 2025 in text. FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.

## Close-out (24 Oct 2026)

- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Scoped subtype synonyms added: seronegative and double seronegative labels.
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG', 'seronegative myasthenia gravis', 'seronegative MG', 'double seronegative myasthenia gravis', 'double seronegative MG']; icd_codes = ['G70.00', 'G70.0', 'G70.01']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 59.9 -> 67 kg, height 156 -> 165 cm, BMI 24.6 -> 24.6 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 67 kg, height 165 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 80, ECOG 1 (normal activity with effort; some signs and symptoms) (fallback_tool_outputs.clinical_assessment). Why: rule 1: the library reports Karnofsky 100 / ECOG 0 (no evidence of disease, working); rule 3: generalized fatigable ocular and bulbar weakness in a working patient.
- `order_specialized_test {test_type: emg_ncs}`: normal nerve conductions and needle EMG, stating that neuromuscular transmission was not assessed (fallback_tool_outputs.specialized_test). Why: rule 1: the library report concludes there is no neuromuscular junction disorder, which routine conductions and needle EMG without repetitive stimulation cannot assess and which is not true here; the stored RNS study reports normal nerve conductions, which this report keeps.
- `order_specialized_test {test_type: speech_language_evaluation}`: fatigable hypernasal dysarthria; language normal (followup_outputs[6] request_speech_language_evaluation). Why: rule 3: the library reports no dysarthria; the examination documents dysarthria with a nasal component.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
