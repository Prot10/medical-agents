# MG-S01
Reviewer status: none (MG not reviewed in this round; July 2026 tool review only) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: no reviewer notes for this case | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | blocker | `initial_tool_outputs.literature_search` | Any-query literature output whose finding and summary were the `expected_evidence` of the literature criterion (leak guard failing, plan B). | FIXED: literature criterion and the stored output deleted (plan default for S cases); the off-pathway literature fallback ("no directly applicable evidence", false for this question) set to null so the library answers; `metadata.fallback_tool_kinds.literature_search` removed. Guard passes. |
| A | blocker | `initial_tool_outputs.specialized_test`, `followup_outputs[request_repetitive_nerve_stimulation]` | The required RNS criterion was answered by a follow-up holding only a 50 Hz study with no decrement, shadowing the initial decrement report (plan H1). | FIXED: one RNS report (initial): 3 Hz decrement deltoid 18%, nasalis 22%, trapezius 16%, normal baseline CMAPs, post-exercise testing (deltoid 7.8 to 8.2 mV, 5%, no facilitation), normal NCS, technique (warmed, pyridostigmine not taken); follow-up deleted. |
| C | major | `initial_tool_outputs.specialized_test.findings` | Edrophonium (Tensilon) test reported; not available and not orderable (plan fact 9). | FIXED: deleted from findings, impression and quantitative data. |
| B | minor | `patient.neurological_exam.cranial_nerves` | "Limitation of right eye adduction" with diplopia on rightward gaze (right-gaze diplopia comes from the left medial or right lateral rectus). | FIXED: "left eye adduction". |
| C | minor | `patient.neurological_exam.cranial_nerves` | Ptosis measured as levator excursion. | FIXED: MRD1 left 0.5 mm, right 2 mm. |
| D | major | `patient.neurological_exam.additional` | "NIF -58 cmH2O (borderline)" in the patient block while respiratory function is scored (plan K, L). | FIXED: deleted. |
| B | major | `patient.physical_exam` (absent), `followup_outputs[request_respiratory_function]` | No weight anywhere; respiratory report with NIF -58 against "> -60" called "within normal limits", FVC "3.4" without unit or % predicted, an ABG row (plan fact 14, L). | FIXED: `physical_exam` added (general with weight 62.4 kg, height 168 cm matching BMI 22.1; cardiovascular, respiratory, abdomen); report rewritten: FVC 3.05 L, 85% predicted, 49 mL/kg; MIP -52 cmH2O (L); MEP 68 cmH2O (L); single-breath count 28; adequate cough; ABG removed. |
| C | major | ice pack (no criterion, no report; `metadata.actions_withdrawn`) | Bilateral fatigable ptosis without the recommended ice pack test (plan 3.5: recommended with ptosis). | FIXED: recommended criterion `action-ice-pack-test` and a follow-up report (left MRD1 0.5 to 3.5 mm, 3.0 mm); `actions_withdrawn` entry removed. |
| B | major | `initial_tool_outputs.labs` | CBC and BMP reported as "All normal"; two laboratories (AChR < 0.5, MuSK < 0.02); MuSK in an AChR-positive patient; anti-titin (not orderable, plan CENTRAL 7) (plan G, fact 2, H9). | FIXED: CBC and BMP analytes with values; one laboratory (AChR binding <= 0.02 nmol/L, blocking <= 15%, modulating 0-20%); MuSK and anti-titin rows removed; free T4 added; interpretation rewritten. Values kept (12.4 nmol/L, 72%, 88%, TSH 1.8, anti-TPO 22, CK 98). |
| A | major | `followup_outputs[request_thymoma_mri_preop]` | Chest MRI filed under `order_advanced_imaging` with a prose modality "MRI chest" (plan H5). | FIXED: rerouted, not deleted, as `order_body_imaging` (region anterior mediastinum, MRI, contrast) so the accepted `mediastinum_MRI` alternative returns the thymoma rather than a library normal report; content rewritten in report voice (no signal drop on opposed phase, no invasion). |
| B | major | `initial_tool_outputs.body_imaging.region`, `.impression` | Region "mediastinum" only, so a `chest_CT` order would be answered by a library normal chest CT despite a 4.2 cm mass; impression did not state the imaging diagnosis. | FIXED: region "chest, anterior mediastinum" (answers chest_CT and mediastinum_CT); numbered impression "most consistent with a thymoma; thymic carcinoma cannot be excluded". |
| C | major | `followup_outputs[request_ivig_preop]` | IVIG pre-operative plan filed as a drug-interaction check (treatment disguised as a test, plan J). | FIXED: deleted; pre-operative IVIG or PLEX is a must. |
| C | major | `followup_outputs[request_pyridostigmine_ocp_interaction]` | Wrong facts: "corticosteroids increase OCP efficacy", "azathioprine teratogenic"; treatment plan in `proposed` (plan C, fact 19, 23). | FIXED: rewritten as `initial_tool_outputs.drug_interactions.prednisone` in checker voice (ethinylestradiol raises prednisolone exposure; no pyridostigmine interaction; mycophenolate and methotrexate teratogenic; TPMT before azathioprine; perioperative VTE with combined contraception). |
| A | major | `ground_truth.action_criteria` | Template criteria (labs with MuSK and LRP4, drug check with telithromycin required, literature, labels equal to rationales, `[Wolfe_2016]` everywhere) (plan A, N). | FIXED: labs `[anti_AChR, TSH]` required; RNS required; SFEMG optional (RNS diagnostic); ice pack recommended; mediastinal imaging required with alternatives mediastinum_MRI and chest_CT (all served by the case's reports); respiratory recommended; drug check optional with `{}` arguments; order labs, RNS, SFEMG, ice pack, imaging, respiratory, drug check; case-specific labels, rationales and expected evidence. |
| B | minor | `ground_truth.sequence_constraints`, `stop_rule` | `labs -> RNS` with an SFEMG reason; drug check required before assessment; `max_additional_actions: 0` (plan 3.3, 3.4). | FIXED: `RNS -> SFEMG` and `labs -> SFEMG` soft; stop rule labs, RNS, imaging, `max_additional_actions: 1`. |
| C | major | `ground_truth.assessment.required_recommendations` | Diagnostic musts (confirm AChR, CT, respiratory, SFEMG "if diagnostic uncertainty"); "non-hormonal contraception during immunosuppression" (wrong rationale); no steroid plan (plan D). | FIXED: thoracic surgery for thymectomy (thymoma); pre-operative IVIG 2 g/kg (about 125 g) or PLEX because of bulbar weakness, with FVC/MIP before anaesthesia and NMB caution; pyridostigmine titration; low-dose prednisone escalation, azathioprine after TPMT; pregnancy counselling (fact 19); swallow assessment; drug list. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Seven template prohibitions incl. telithromycin and "pyridostigmine bridge". | FIXED: three canonical prohibitions plus "no mycophenolate or methotrexate without contraception and counselling". |
| C | minor | `ground_truth.differential` | "Thymic carcinoma vs thymoma" moderate; LEMS cited only titres; TED and CPEO features thin. | FIXED: "Thymic carcinoma (rather than thymoma)" low with CT/MRI features; LEMS, TED, CPEO key features from the case data. |
| C | minor | `ground_truth.key_clinical_evidence` | Template bullets: "All confirmed MG require CT chest", anti-titin "non-negotiable" (titin not in the case), telithromycin, SFEMG ">95%" (plan E). | FIXED: six case-specific bullets. |
| E | minor | `ground_truth.avoided_actions[*]` | `[Wolfe_2016]` cited for EEG, CSF, PET, echo, monitoring. | FIXED: citations emptied, case rationales with Jacob 2025 in text. |
| D | minor | `fallback_tool_outputs.ct.impression` | "does not address the question" (plan F). | FIXED: plain normal head CT. |
| B | minor | `fallback_tool_outputs.ecg.rate` | 87/min against a resting heart rate of 74. | FIXED: 76. |
| C | minor | `followup_outputs[request_emg_single_fiber]` | No muscle named; blocking in "18/20 pairs (90%)" equal to the jitter count; "most abnormal possible range" (plan I). | FIXED: extensor digitorum communis, 20 pairs, mean MCD 88 microseconds, increased jitter 18/20, blocking 9/20; impression in report voice. |
| E | minor | `metadata` | Difficulty rationale counted the drug check; revision fields. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 34-year-old woman with generalized AChR-positive MG (class IIb-III) and a 4.2 cm anterior mediastinal mass. The work-up reads: AChR antibody and thyroid function (one laboratory, CBC and BMP with values, no MuSK or titin), one RNS report with the 3 Hz decrement (deltoid 18%, nasalis 22%, trapezius 16%) and brief-exercise testing without facilitation (the Tensilon test and the 50 Hz follow-up that shadowed the decrement are gone), an ice pack test of the left ptosis (MRD1 0.5 to 3.5 mm), contrast CT of the chest and mediastinum (now read as most consistent with thymoma, thymic carcinoma not excluded; a mediastinal MRI is available as the accepted alternative), and respiratory staging with weight-based values showing mildly reduced MIP and MEP with preserved FVC (49 mL/kg). SFEMG and the drug check are optional; literature is no longer a criterion. The exam now gives MRD1 values and a left adduction deficit matching right-gaze diplopia, and no NIF. Musts: thymectomy for the thymoma, pre-operative IVIG 2 g/kg or PLEX for her bulbar weakness, pyridostigmine titration, low-dose prednisone escalation with azathioprine after TPMT if needed, pregnancy counselling (mycophenolate and methotrexate teratogenic, azathioprine acceptable), swallow assessment and drug counselling.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 1: `[Jacob_2025]`, `[Evoli_2019]`, `[Lawn_2001]` cited in text only.
- Plan CENTRAL 2: `icd_codes[0]` G70.01 in a stable new diagnosis (G70.00 fits). Not changed.
- Plan CENTRAL 3: synonyms accept "ocular myasthenia gravis" for this generalized case.
- Scratchpad note for the round: the scratchpad directory is shared by all workers, and this worker's first scripts (`edit_s01.py`, `serve.py`) overwrote files of the same name written earlier by another worker. Those were already-applied scratch scripts, so no case was affected; later scripts are in `scratchpad/mgS_worker/`.

## Open questions for Andrea (judgment calls you could not settle)

- None. Pre-operative IVIG or PLEX is made a must (not optional) because she has chewing fatigue, dysarthria and dysphagia with mildly reduced MIP and MEP; Sanders 2016 advises pre-operative IVIG or PLEX in patients with significant bulbar weakness.

## Verification

Adversarial check, 24 Oct 2026. Read the log, the full diff and the final case. Confirmed: one RNS report with a 3 Hz decrement and no Tensilon; left adduction deficit now matches right-gaze diplopia (left medial rectus weakness gives diplopia on right gaze); MRD1 consistent across exam, ice pack and expected evidence; weight/height give BMI 22.1 and FVC 49 mL/kg; IVIG 2 g/kg about 125 g at 62.4 kg; drug output facts correct (ethinylestradiol raises prednisolone exposure; mycophenolate/methotrexate teratogenic; azathioprine acceptable); body imaging region answers mediastinum_CT and chest_CT, the MRI follow-up answers mediastinum_MRI (checked through the MockServer); differential lowered after the work-up; leak guard passes. The reinstated ice pack test (withdrawn in August as "inventing a result") follows plan 3.5 and fact 9 (ptosis present, result authored with MRD1 values); accepted.

Found and fixed:
- D/B major: `fallback_tool_outputs.advanced_imaging.modality` was the prose "FDG-PET scan" (PATTERNS 5 discriminator rule), and its "No abnormality identified" whole-body PET would contradict the 4.2 cm thymoma once routed. Replaced with an `FDG_PET` report showing a moderately FDG-avid anterior mediastinal mass (SUVmax 4.6) without nodal or distant uptake; `metadata.fallback_tool_kinds.advanced_imaging` set to `abnormal_consistent`. FDG_PET stays a waste avoided action.
- E minor: em dash in the rewritten `neurological_exam.cranial_nerves` sentence replaced by a comma.

perfect_agent passes; case_io check clean for this case.

## Condition audit (MG auditor, 24 Oct 2026)

- fallback_tool_outputs.echo.echo_type set to TTE. FIXED.
  Why: the discriminator guard (PATTERNS.md section 5) requires an exact vocabulary value on every case fallback; an empty echo_type answered every echo variant. The RS11-RS16 verifiers fixed this only in their own cases.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.

## Close-out (24 Oct 2026)

- `ground_truth.diagnosis.icd_codes[0]` G70.01 -> G70.00. ICD-10-CM G70.01 is myasthenia gravis with (acute) exacerbation, including crisis; this is a new or stable presentation, not an exacerbation. G70.01 stays accepted as a secondary code (plans/MG-decisions.md, Q2).
- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG']; icd_codes = ['G70.00', 'G70.0', 'G70.01']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
