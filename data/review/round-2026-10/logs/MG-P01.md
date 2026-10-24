# MG-P01
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MG) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance for myasthenia_gravis, applied through the condition plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `patient.history_present_illness` | The outside test is said to include AChR and MuSK, so repeating MuSK looks redundant and the criterion rationale contradicts the history. | FIXED: "An AChR antibody test at an outside facility 3 months ago (assay not stated) was reported negative". Em dash replaced. |
| B | major | `initial_tool_outputs.labs.panels` | CBC and BMP stored as "All normal" stubs (class G); LRP4 and anti-cortactin rows in the first-line order; anti-cortactin is not in the vocabulary. | FIXED: real CBC, BMP, CK, thyroid, ANA/ESR/CRP rows; AChR binding, blocking, modulating and MuSK by RIA, all negative; LRP4 moved to a cell-based follow-up; cortactin removed. |
| B | major | `followup_outputs` (`request_musk_antibodies`) | MuSK served as a separate follow-up duplicating the initial MuSK row. | FIXED: deleted. New `request_cell_based_assay_lrp4` follow-up (clustered AChR, clustered MuSK, LRP4, all negative); trigger tokens chosen so they do not overlap the first anti_AChR order (probed: `["anti_AChR","TSH"]` gets the initial labs, `["anti_LRP4"]` and `["clustered_AChR_cell_based"]` get the panel). |
| B | major | `initial_tool_outputs.specialized_test` | RNS report mixed with recommendations; decrement values not numbered per muscle. | FIXED: 3 Hz nasalis 7%, trapezius 6%, deltoid 4%, normal CMAPs, no facilitation, normal NCS; impression in report voice; recommended action "Single-fiber EMG". |
| B | major | `followup_outputs` (`request_emg_single_fiber`) | Blocking counts and reference ranges inconsistent; no count of pairs above the individual limit. | FIXED: orbicularis oculi MCD 52 us, 12/20 pairs above limit, blocking 6/20; EDC MCD 41 us, 5/20 above limit, blocking 2/20. |
| B | minor | `initial_tool_outputs.body_imaging` | Contrast false; impression not stating the study. | FIXED: region "mediastinum chest", contrast true, "CT chest with contrast: no anterior mediastinal mass; fatty-replaced thymus". |
| D | major | `patient.neurological_exam.additional` | Bedside NIF -62 in the exam while no respiratory result was stored (`metadata.actions_withdrawn` said so). | FIXED: number removed from the exam; respiratory follow-up added (FVC 3.40 L, 93%, 51 mL/kg; MIP -62; MEP 88; normal); `physical_exam.general` "Weight 67 kg, height 168 cm" (BMI 23.7). |
| C | major | `ground_truth.action_criteria` (ice pack) | Fatigue-induced right ptosis, but no ice-pack result (listed as withdrawn). | FIXED: ice-pack follow-up (MRD1 2.0 to 4.0 mm); criterion optional because ptosis appears only after sustained upgaze (plan says recommended when ptosis is present; see Open questions). `actions_withdrawn` emptied. |
| C | major | `followup_outputs` (`request_pyridostigmine_response`, `request_prednisone_azathioprine_plan`, two literature follow-ups) | Treatment response and management plans stored as tool outputs (class J); literature with patient-specific advice. | FIXED: all deleted; one canonical initial literature output; literature optional and last. |
| C | major | `ground_truth.action_criteria` | Tiers off plan: MuSK separate, drug check required, no respiratory or CBA criterion. | FIXED: labs `["anti_AChR","anti_MuSK","TSH"]` required (one criterion, see Open questions); RNS, SFEMG, mediastinal CT with contrast required (alternatives chest_CT, mediastinum_MRI); CBA panel and respiratory recommended; ice pack, drug check, literature optional. |
| B | minor | `initial_tool_outputs.drug_interactions` | Drug check in a follow-up with narrative `proposed`. | FIXED: initial `drug_interactions["pyridostigmine"]` in checker voice: no relevant interaction with sertraline, pregabalin, omeprazole; clonazepam respiratory caution. |
| C | minor | `ground_truth.sequence_constraints`, `stop_rule` | Missing RNS -> SFEMG; stop rule included literature. | FIXED: labs -> SFEMG, RNS -> SFEMG, labs -> CBA panel (soft); stop rule labs, RNS, SFEMG, CT; max 2. |
| C | major | `ground_truth.assessment` | Thymectomy as a must in seronegative non-thymomatous MG; no objective response measure; prednisone dosing absent. | FIXED: five musts (replace the functional label, pyridostigmine with MG-ADL/QMG, prednisone low and slow with a steroid-sparing agent after TPMT/NUDT15, repeat serology at 6 months, clonazepam caution); prohibitions canonical drug and steroid lines plus the functional-attribution line. |
| C | minor | `ground_truth.differential` | FND and MuSK MG moderate after a positive SFEMG and negative CBA. | FIXED: FND low, MuSK MG very low, LEMS and CMS very low with key features. |
| E | minor | `ground_truth.key_clinical_evidence`, `red_herrings` | Tool-named lines. | FIXED: rewritten clinically. |
| C | minor | `ground_truth.avoided_actions[*]` | Pack keys cited for waste. | FIXED: case rationales, Jacob 2025 in text, citations empty. |
| D | minor | `fallback_tool_outputs.ct` | Class F wording. | FIXED: plain normal head CT. |

## Changes, in one paragraph a physician can read before re-reviewing

A 44-year-old woman with a previous functional label, anxiety and fatigable dysarthria, dysphagia for solids, fatigue-induced right ptosis and adduction lag, whose outside AChR test was negative. The work-up is now: AChR (binding, blocking, modulating), MuSK and thyroid function, all negative; RNS normal (maximum 7%); SFEMG abnormal with jitter and blocking in orbicularis oculi and extensor digitorum; contrast mediastinal CT without thymoma. A cell-based panel (clustered AChR, MuSK, LRP4, negative) and respiratory function (normal) are recommended; ice pack (positive), drug check and literature are optional. Musts: replace the functional label with seronegative generalized MG, pyridostigmine with an objective response measure, low-and-slow prednisone with a steroid-sparing agent if needed, repeat serology at 6 months, clonazepam caution. Thymectomy is no longer a must.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: "seronegative myasthenia gravis" / "double-seronegative generalized myasthenia gravis" should be accepted (plan CENTRAL 3).
- Criteria pack keys `[Jacob_2025]`, `[Evoli_2019]` (named in text only).
- `anti_cortactin` is not in the vocabulary; it was removed rather than requested, since it is a research assay.
- The mediastinum_MRI alternative is answered by the library fallback (perfect-agent warning).

## Open questions for Andrea (judgment calls you could not settle)

- Labs: the plan gives MuSK its own criterion; here AChR, MuSK and TSH are one required criterion, because two criteria would be served the same report (identical-report warning). Should MuSK be scored separately?
- Ice pack set optional, not recommended: ptosis is absent at rest and appears only after 90 s of upgaze. Keep it optional?
- Thymectomy: removed as a must; it may be considered in seronegative generalized MG not responding to treatment (MGTX enrolled only AChR-positive patients). Agree?
