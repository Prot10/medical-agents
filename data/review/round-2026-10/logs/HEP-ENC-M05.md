# HEP-ENC-M05
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| da6eb54c-0ea1-4a46-af1a-b3ff58b35d1a | FIXED | The template `Zinc` panel (82 µg/dL) deleted from `initial_tool_outputs.labs.panels`; zinc is reported once, 180 µg/dL, in `Trace_Elements` with copper 68 µg/dL. The "Exclusion studies" block was deleted with it (magnesium 2.0 mg/dL moved to BMP, lactate 1.2 mmol/L to its own panel). |
| a11d6f3d-05b1-4f83-a87e-948173a73d25 | FIXED | The duplicate `TSH` panel (2.1 mIU/L) deleted; TSH is reported once, 3.8 µIU/mL, in `Thyroid`. |
| cf6cd213-14ff-477a-b87c-f896f7ceb04f | FIXED | The literature follow-up (`search_zinc_toxicity_hepatic_encephalopathy`, unsourced arginase claim) and criterion `action-3-search-medical-literature` deleted. The zinc-excess premise is removed everywhere: label (`accepted[0]`) now reads "precipitated by constipation; excess zinc from over-the-counter supplements with secondary copper deficiency" (plan relabel); pearl `key_clinical_evidence[4]` states that zinc deficiency, not excess, is associated with HE and that excess zinc causes copper deficiency; a red herring now encodes "high zinc does not cause HE"; the prohibition reads "Stop the zinc supplements: excess zinc causes copper deficiency; do not start zinc without a documented deficiency". Old pearl ("toxicity precipitates HE by inhibiting urea-cycle arginase") deleted. |
| 3cb39ca8-0502-4ffa-842b-44c54474b00b | FIXED | The response panel (`request_lactulose_rifaximin`: ammonia 38 at 2 weeks, zinc 180 to 94, lactulose to 3-4 stools) deleted; one admission ammonia (78 µmol/L, range 11-51) stays. K-AMM pearl and a prohibition against using ammonia to grade or monitor added; the HPI no longer reports the ammonia. |
| 9a959a80-2aff-49f2-9f3b-1d3b8953b5a4 | FIXED | Blood and urine cultures (`action-7`, `action-8-order-microbiology`) recommended as an occult-infection screen with the plan's rationale (afebrile, WBC 5.4, no source); arguments reduced to the specimen; no culture must; blocks give one time point ("no growth at 48 hours"; urinalysis "no pyuria") and `collected_before_antimicrobials` null, since no antibiotic is given. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | HPI reported ammonia 78, bilirubin and serum zinc 180 with its reference range (results of the scored labs) (C13). | FIXED: results removed; the supplement history kept as history ("over-the-counter zinc supplements for the past 4 months"), constipation quantified (one bowel movement every 2-3 days). |
| B | major | `patient.clinical_history.medications` | The zinc supplement, the case's medication-reconciliation point, was absent from the medication list. | FIXED: "Zinc (over-the-counter supplement), 50 mg elemental zinc three times daily, past 4 months" added. |
| B | minor | `medications` (lactulose), `past_medical_history` | Lactulose labelled "HE secondary prophylaxis" after a grade 1 (covert) episode; "Child-Pugh B, MELD 15" undated. | FIXED: indication "Prophylaxis after a prior HE episode"; prior score dated "at hepatology review 6 months ago". |
| B | minor | `patient.history_present_illness`, `red_herrings[1]` | "Good biochemical response" to UDCA contradicts ALP 284 (1.9 x ULN) and bilirubin 2.8. | FIXED: "treated with ursodeoxycholic acid since diagnosis"; red herring "PBC treated with UDCA". |
| C | minor | `patient.neurological_exam.mental_status` | Number Connection Test 48 s against a "29 second threshold" (invented; age norms at 63 are higher) in an overt grade II patient whose grade is clinical. | FIXED: sentence deleted. |
| C | major | `ground_truth.diagnosis.accepted[0]`, `key_clinical_evidence` | "Child-Pugh B, MELD 15" not derivable: computed Child-Pugh B (9), MELD 16, MELD-Na 17 (C10). | FIXED: label per plan with MELD-Na 17; score pearl `key_clinical_evidence[2]`. |
| C | major | `followup_outputs` (paracentesis, transplant score, pruritus "drug check") | `interpret_labs` tap in a patient without ascites (C6); MELD-Na/PBC-UK score panel (C1); pruritus treatment filed as a drug check (C1). | FIXED: all deleted; pruritus treatment and transplant referral are musts. |
| C | major | `action-4-check-drug-interactions` | Required check with template expected evidence (C5). | FIXED: optional (plan); alternatives cholestyramine, lactulose, zinc; one output `check_cholestyramine_lactulose_levothyroxine_zinc` placed last, with real content (cholestyramine binds UDCA, levothyroxine and vitamin D and is constipating; calcium-levothyroxine; zinc-copper; avoid sedating antihistamines; rifampicin caution). |
| B | major | `initial_tool_outputs.labs` | "Exclusion studies" without values; no CRP; hemoglobin 11.8 flagged in the interpretation but missing from the summary (C9). | FIXED: magnesium 2.0, lactate 1.2, CRP 2.1 mg/L added; summary and interpretation list every flagged value. |
| A | minor | `action-1-interpret-labs` | Ten named panels demanded. | FIXED: two-alternative core with `zinc` and `copper` (plan Labs+). |
| C | minor | `action-2-order-ct-scan` | CT optional with label "before any LP" (no LP in the case). | FIXED: recommended (see Open questions): two-week subacute decline with word-finding difficulty, INR 1.6, platelets 116; canonical normal CT findings with mild atrophy; "restricted diffusion" removed. |
| C | major | `ground_truth.assessment` | Lactulose 2-4 stools (C3); rifaximin unconditionally in a first overt episode; vague musts ("review dietary protein", "counsel about evidence-free supplement use"); no pruritus plan; no transplant referral at MELD-Na 17 with decompensation; haloperidol boilerplate (C12); generic LP prohibition. | FIXED: musts MUST-PRECIP (constipation), MUST-LACT, rifaximin only if overt HE recurs, stop zinc with recheck of zinc, copper, ceruloplasmin and blood count, cholestyramine separated from UDCA and levothyroxine, normal protein with late-evening snack, MUST-TX. Prohibitions: PROHIB-BZD, opioids (acetaminophen up to 2 g per day), zinc (plan text), sedating antihistamines, ammonia monitoring. LP line deleted. |
| C | minor | `ground_truth.differential` | Copper deficiency (raised by the case) absent; hypothyroid and neurodegenerative entries argued from a "rapid lactulose response" that was a deleted follow-up; SBP entry conditional. | FIXED: copper deficiency (low) and subdural hematoma (low, negative CT) added; key features rewritten from the case's own results. |
| E | minor | criteria, citations, metadata | Rationale = label; free-text citations; metadata described zinc as inhibiting the urea cycle and four required tools. | FIXED: one-sentence rationales with keys; metadata rewritten; EEG impression closes with "Clinical correlation recommended." |

## Changes, in one paragraph a physician can read before re-reviewing

The case no longer claims that zinc excess causes HE. The label now reads overt HE grade II in PBC cirrhosis (Child-Pugh B, 9 points; MELD-Na 17) precipitated by constipation, with excess zinc from over-the-counter supplements and secondary copper deficiency. The zinc supplement is in the medication list and the HPI keeps the history but no longer gives the ammonia or zinc results. Labs report each analyte once (TSH 3.8, zinc 180, copper 68), add magnesium, lactate and CRP, and drop the "Exclusion studies" block. The policy requires only the core labs with zinc and copper; blood and urine cultures (afebrile, WBC 5.4), CT and EEG are recommended and the drug check optional. The literature search, the ammonia response panel, the paracentesis in a patient without ascites, the transplant score panel and the pruritus "drug check" are gone. Musts: relieve constipation, lactulose to 2-3 stools, rifaximin only if overt HE recurs, stop zinc and recheck zinc, copper, ceruloplasmin and blood count, cholestyramine for pruritus separated from ursodeoxycholic acid and levothyroxine, normal protein intake, transplant referral. Prohibitions: sedatives, opioids, zinc without documented deficiency, sedating antihistamines, ammonia-guided treatment.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[ACG_HE_2026]`, `[EASL_HE_2022]`.
- `accepted[0]` relabelled under ruling 3 (reviewer note cf6cd213; plan CENTRAL 6, Q1); ICD codes and synonyms unchanged.
- The pruritus must cites the EASL 2017 PBC guideline (Hirschfield GM et al., J Hepatol 2017;67:145-172) in free text; it has no citation key.

## Open questions for Andrea (judgment calls you could not settle)

- Plan Q1 (the M05 premise): applied as the plan proposes (constipation precipitant, zinc excess with copper deficiency as an incidental supplement finding). Requiring zinc and copper in the core labs rests on the supplement now being in the medication list.
- CT is recommended, not optional as the plan says: the husband reports word-finding difficulty over a two-week subacute course, and with INR 1.6 and platelets 116 a subdural hematoma must be excluded (EASL 2022: imaging when there is diagnostic doubt). If you read word-finding difficulty as the slowed speech of HE, it can return to optional.
- Rifaximin is a conditional must (only if overt HE recurs), because the prior episode was grade 1 (covert) and this is her first overt episode. If the prior episode is meant to have been overt, rifaximin becomes unconditional.
- With all other steps recommended, the stop rule holds only the core labs.

## Verification

Checked (adversarial verifier, 23 Oct 2026): all five note ids (da6eb54c, a11d6f3d, cf6cd213, 3cb39ca8, 9a959a80) are in the table and fixed in the file (zinc 180 and TSH 3.8 reported once each; no arginase claim, literature output or zinc-toxicity premise anywhere; one admission ammonia; cultures recommended with null `collected_before_antimicrobials`). Recomputed: Child-Pugh B 9 (bilirubin 2.8, albumin 2.6, INR 1.6, no ascites, grade II), MELD 16, MELD-Na 17, as in the label and pearl (with the cholestatic bilirubin thresholds sometimes used in PBC the total would be 8, still class B). The HPI no longer gives ammonia or zinc; the zinc supplement is in the medication list; the differential covers copper deficiency, Wilson and SDH; no musts contradict prohibitions; zinc pearl matches plan 1.2.

Found: (1) the worker made the CT recommended against plan 3.1 (optional outside the listed cases) and reviewer note 22fa5945 (ACG 2026 recommendation 6: no routine imaging without a new focal deficit). The justification (word-finding difficulty, coagulopathy) applies equally to M01, where the CT stays optional, so the two cases disagreed. Her exam has no focal deficit and the precipitant is clear. (2) Two red-herring paths pointed at the whole `Trace_Elements` panel.

Changed: `action-2-order-ct-scan` is optional with the rationale "no focal deficit, seizure or head trauma and the precipitant is clear ...; INR 1.6 and platelets 116 lower the threshold to exclude a subdural hematoma if the course is atypical or she does not improve with treatment"; the SDH differential reads "CT, if obtained, shows no extra-axial collection"; `metadata.difficulty_rationale` no longer lists CT as recommended. Red-herring paths now `Trace_Elements[1]` (copper) and `Trace_Elements[0]` (zinc). This supersedes the worker's first Open question. `perfect_agent.py` and `case_io.py check` clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

- Leak guard (Andrea, 24 Oct 2026: any-query outputs must not repeat any criterion's expected evidence, including their own): `ground_truth.action_criteria[action-4-check-drug-interactions].expected_evidence` reworded as the conclusion a grader checks, in words not shared with the stored `check_drug_interactions` follow-up, whose report text is unchanged; clinical content unchanged.
- Q1 premise confirmed as applied (constipation precipitant; zinc excess with copper deficiency incidental). The PBC must's free-text citation now resolves to the verified `[EASL_PBC_2017]` pack entry (J Hepatol 2017;67:145-172); case text unchanged.

Checks: `perfect_agent.py` pass; `case_io.py check` schema and synonym guard OK, no test failure names this case; leak guard clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-2-order-ct-scan` rationale: "Optional: there is no focal deficit, seizure or head trauma and the precipitant is clear, so brain imaging is not routine; INR 1.6 and platelets 116 lower the threshold to exclude a subdural hematoma if the course is atypical or she does not improve with treatment." -> "There is no focal deficit, seizure or head trauma and the precipitant is clear, so brain imaging is not routine; INR 1.6 and platelets 116 lower the threshold to exclude a subdural hematoma if the course is atypical or she does not improve with treatment."
- criterion `action-4-check-drug-interactions` rationale: "Optional: the pruritus treatment (a bile-acid sequestrant) binds ursodeoxycholic acid and levothyroxine and is constipating, which matters in an episode precipitated by constipation." -> "The pruritus treatment (a bile-acid sequestrant) binds ursodeoxycholic acid and levothyroxine and is constipating, which matters in an episode precipitated by constipation."

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-1-interpret-labs]`.alternatives: was [CBC, CMP, coagulation, ammonia, zinc, copper] | [CBC, BMP, LFTs, coagulation, ammonia, zinc, copper]; now [CBC, CMP, coagulation, ammonia, zinc, copper, CRP] | [CBC, CMP, coagulation, ammonia, zinc, copper] | [CBC, BMP, LFTs, coagulation, ammonia, zinc, copper].
- Decision: serve: new first alternative (old order kept as an alternative). The label names CRP with the core bloods (infection is the precipitant to exclude) and the evidence reads it; CBC, CMP, coagulation and ammonia did not return the inflammatory panel.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.
