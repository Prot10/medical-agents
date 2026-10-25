# ALS-P01
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| dd04fa1d-5520-44cf-b473-44d5d6bc5d40 | FIXED | `ground_truth.diagnosis.accepted[0]` "... initially possible, confirmed definite on 3-month repeat EMG" -> "Amyotrophic lateral sclerosis (ALS), early limb-onset, possible ALS by Awaji criteria" (`icd_codes[0]` G12.21 and appended synonyms untouched); musts now frame early suspected ALS needing follow-up and repeat EMG (C7) |
| 92755ec0-38eb-48e7-8b12-979108e33695 | FIXED | Criteria reordered (EMG, brain MRI, spine MRI, labs first); literature follow-up `search_benign_fasciculation_als_distinction` and `action-1-search-medical-literature` deleted; follow-ups now respiratory, genetics, riluzole; repeat EMG/NCS in about 3 months is `required_recommendations[1]` (C1, C2, C7) |
| d92369d6-0b68-4c28-b664-06c3b36e07eb | FIXED | Literature step deleted; clinical and electrodiagnostic reassessment carried by the EMG criterion (first), the repeat-EMG must and the prohibition "Do not reassure him on the basis of the earlier benign fasciculation syndrome diagnosis ..." |
| 8ad11950-ddca-4e21-af5a-3f5f73180f0d | FIXED | The statement was in the deleted literature output. The same overstatement in the EMG report ("characteristic of pathological, not benign, fasciculations") removed from `initial_tool_outputs.specialized_test.findings[0]`; the softened wording is `key_clinical_evidence[2]` ("Complex fasciculations raise concern ... are not diagnostic alone; progression on repeat EMG confirms the diagnosis."); `metadata.notes` reworded the same way |
| 0f3c6f3c-3d94-4219-bb84-3d86c9b183c8 | FIXED | Riluzole check moved last, made `optional` (plan: riluzole discussed now, started on confirmation); soft constraint EMG before riluzole check |
| ba745e79-d2d0-4ca1-ae6c-21ae45c57129 | FIXED | Old must list (EMG/MRI/lab actions, "Initiate riluzole") replaced by the plan's P01 set: explain concern for early ALS, repeat EMG/NCS in about 3 months with clinical review, respiratory monitoring, discuss riluzole to start on confirmation, specialist ALS clinic, genetic counselling |
| c2c49db5-2f22-4b15-8bb1-5ce40d23048f | FIXED | Respiratory function moved after the diagnostic core and relabelled as staging (`recommended`); output reference ranges and impression per C4 (normal) |
| 3b92882f-d181-4b84-8463-4cdb4d254fdc | FIXED | AMX0035 removed (`alternatives` = []); non-riluzole warning "Monitor for psychiatric symptoms" removed; canonical summary |
| 3e9a616b-5243-400a-8b3c-b5a823a67ee8 | FIXED | Same as dd04fa1d and 92755ec0: label "possible ALS", musts and pearls state suspected early ALS needing follow-up and repeat EMG; core work-up leads the pathway |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | "A repeat EMG has been ordered." and the reasoning sentence about subtle UMN signs and one-region LMN signs (synthesis of the scored EMG) | FIXED: both sentences deleted (C11); the prior normal EMG 2 years ago stays as history |
| B | major | `initial_tool_outputs.mri` | Brain report impression was the spine impression (C5-C6 foraminal narrowing) and claimed "no enhancing lesion" without contrast | FIXED: brain-only normal report |
| B | major | `initial_tool_outputs.body_imaging` | Spine impression held brain statements (corticospinal tract, infarct, demyelinating disease); JSON dump in `description` | FIXED: plain cervical and cord findings, numbered impression |
| D | minor | `initial_tool_outputs.specialized_test.findings` | Interpretive "characteristic of pathological, not benign, fasciculations"; caps "NO clear fibrillations" without stating chronic change | FIXED: morphology kept, interpretation removed; lumbosacral line states no fibrillations and no chronic change |
| B | minor | `initial_tool_outputs.specialized_test.findings` (Motor NCS) | Only one motor nerve reported, which cannot exclude conduction block in a man with right foot dragging | FIXED: right ulnar, peroneal and tibial motor CMAPs normal, normal latencies and velocities, no block or dispersion added |
| A/B | major | `initial_tool_outputs.labs` | No blood count, renal or liver results although the old criterion required CBC and CMP; Free T4 as a string; template panel names; interpretation names ALS | FIXED: panels per C13 (stored values kept; normal CBC, CMP and free T4 1.3 ng/dL added); CK 312 U/L stated as 1.8x ULN |
| C | major | `ground_truth.action_criteria` | MRI `contrast/protocol`, spine `contrast: false`, nine exact lab panels; label = rationale; mixed citations | FIXED: C16 arguments and canonical texts; EMG expected evidence states that denervation is confined to the right cervical region |
| C | major | `ground_truth.differential` | MMN and "flail arm variant" moderate; anti-GM1 cited though never tested | FIXED: flail arm entry deleted (an ALS phenotype, not a competing diagnosis; C8); BFS, MMN, cervical radiculopathy low; IBM very_low |
| C | minor | `ground_truth.assessment.prohibited_recommendations[1]` | Plan template for cervical surgery says the changes "do not explain denervation in other regions", but here denervation is only in the cervical region | FIXED with case wording: the C5-C6 foraminal narrowing does not explain C8-T1 hand denervation, UMN signs or widespread fasciculations |
| C | minor | `ground_truth.key_clinical_evidence` | Template pearls (engineering text, "2-5x" CK, El Escorial EMG, generic spondylosis) | FIXED: 7 pearls (Gold Coast/Awaji status, K-EMG, complex fasciculations, prior BFS label, K-NCS, K-CK 1.8x, K-RESP) |
| E | minor | `metadata.notes`, `metadata.difficulty_rationale` | "complex fasciculation morphology on EMG is pathological"; "5 required tools" | FIXED: softened wording; "4 required tools" |
| B | minor | `initial_tool_outputs.labs` | B12 420, folate 10, ESR 8, CRP 2 identical across many ALS cases (template) | FLAGGED, not changed (plan: keep stored values) |

## Changes, in one paragraph a physician can read before re-reviewing
The case is now framed as early limb-onset ALS that is "possible" by Awaji: upper motor neuron signs (right Hoffman sign, brisk reflexes) with active and chronic denervation confined to the right cervical region and complex fasciculations elsewhere. The HPI no longer says a repeat EMG has been ordered or reasons about the criteria. The pathway is EMG/NCS, brain MRI, spine MRI and labs, then respiratory baseline, optional genetics and an optional riluzole check; the literature step is gone. The brain and spine MRI reports are separated (brain normal; mild C3-C6 degeneration with right C5-C6 foraminal narrowing, normal cord). The EMG now reports four motor nerves without conduction block and no longer calls the fasciculations "pathological, not benign". The labs are complete and CK is 1.8x ULN. Musts: explain the strong concern and the need for confirmation, repeat EMG/NCS in about 3 months, respiratory monitoring, discuss riluzole now to start on confirmation, specialist ALS clinic, genetic counselling. Prohibitions: no reassurance from the old BFS label, no cervical surgery for the foraminal narrowing, no attribution to anxiety, no immunotherapy.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Label change of `accepted[0]` within G12.21 (plan section 5 item 3: no synonym change needed).
- Citation keys `[EFNS_ALS_2012]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[ALS_genetics_2023]`, `[Riluzole_SmPC]`.
- UI: initial work-up in criterion order.

## Open questions for Andrea (judgment calls you could not settle)
- Plan Q9: Gold Coast 2020 is already met (UMN and LMN dysfunction in the right arm), so a neurologist could offer riluzole now. Following the reviewer's call for caution, the case defers starting riluzole to confirmation at the 3-month review and keeps the interaction check optional. Confirm.
- The repeat EMG is a must, not an orderable criterion (the case has no repeat-EMG output, and a 3-month repeat cannot happen within the encounter). Agree?

## Verification
Adversarial verifier, 23 October 2026. Checked: all 9 note ids present; label "possible ALS by Awaji" with G12.21 and synonyms untouched; musts and prohibitions are exactly the plan's P01 set (repeat EMG in about 3 months, riluzole discussed now and started on confirmation, no BFS reassurance, cervical surgery, functional and immunotherapy prohibitions); DI optional and last; literature gone; HPI no longer says a repeat EMG was ordered and has no criteria reasoning (prior normal EMG kept as history); EMG impression vs findings (active plus chronic change only in the right cervical region, complex fasciculations elsewhere, thoracic and bulbar fasciculations only, four motor nerves without block); the "pathological, not benign" claim is gone from the report and the softened wording is in key evidence (note 8ad11950); brain and spine reports region-pure; the C5-C6 surgery prohibition and the cervical radiculopathy entry correctly cite C8-T1 hand denervation; CK 312/174 = 1.8x ULN; forbidden strings: none. Perfect-agent and case_io check clean. Found nothing that needed a change.

## Condition audit (ALS lead, 23 Oct 2026)
- `followup_outputs[0].output.findings[*].is_abnormal` added (rows carried no abnormality marker), set from each row's reference range as plan C4 prescribes, so all 30 respiratory reports mark abnormal values the same way (values and impression unchanged).

## Open questions resolved (24 Oct 2026)

Decisions recorded in `data/review/round-2026-10/plans/ALS-decisions.md` (Andrea's ruling of 24 Oct 2026: resolve every open point for dataset quality).

- waste citations: [AAN_2009] -> [EFNS_ALS_2012] on 8 waste avoided actions (ground_truth.avoided_actions[*].citations). EFNS 2012 is the guideline on diagnostic investigations in ALS; AAN 2009 Part 1 covers drug, nutritional and respiratory therapy (ALS summary CENTRAL 8).
- accepted[0] relabelled to state Gold Coast met; DI criterion optional -> recommended with rationale; musts 1, 2 and 4 rewritten (diagnosis made now, review at 3 months with repeat EMG only if needed, riluzole offered now with SmPC monitoring); two key_clinical_evidence items reworded; metadata.difficulty_rationale; em dashes in the stored EMG report replaced.
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, ALS case guards pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-5-interpret-labs]`.alternatives: was [CBC, CK, TSH, vitamin_B12]; now [CBC, CK, TSH, vitamin_B12, CMP, folate, inflammatory_markers] | [CBC, CK, TSH, vitamin_B12].
- Decision: serve: new first alternative (old order kept as an alternative). The label and rationale name renal and liver function, calcium, folate, ESR and CRP (liver baseline before riluzole, inflammatory mimics); the order named only CBC, CK, TSH and B12, so the CMP and inflammatory results the evidence cites were not returned.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although the case contradicts it now get a case-specific report; every other off-pathway order still gets the library normal.

- `analyze_csf special_tests=[NfL, NfH]` -> `fallback_tool_outputs.csf`. Why: CSF neurofilaments are raised in ALS; the library reported NfL 420 pg/mL, normal. Basic CSF acellular, protein 38 mg/dL, NfL 2,600 pg/mL..
- `order_specialized_test test_type=emg_single_fiber` -> `fallback_tool_outputs.specialized_test`. Why: the stored EMG shows chronic reinnervation; single-fibre EMG then shows raised fibre density and jitter, not the library's normal study.
- `order_specialized_test test_type=muscle_biopsy` -> `followup_outputs[request_muscle_biopsy]`. Why: muscle in ALS shows neurogenic grouped atrophy; the library reported normal muscle.
- `perform_clinical_assessment assessment_type=performance_status` -> `fallback_tool_outputs.clinical_assessment`. Why: the library reported Karnofsky 100 / ECOG 0 with no limitation; the history documents working as a software engineer; restricted only in strenuous activity (Karnofsky 90, ECOG 1).

Checks: `perfect_agent.py` ok; `test_case_guards.py -k ALS-` pass; every mapped order answered without the library (`verify.py`, map_ALS); no criterion answer changed (snapshot diff).
