# HEP-ENC-P02
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 5fa6804b-d170-4b9f-b3c9-8a27e73d39cc | FIXED | Deleted the template "Blood ethanol Not detected" row (C9). Serum ethanol 22 mg/dL, flagged, now appears once in `initial_tool_outputs.labs.panels.Toxicology[0]` beside the negative urine drug screen. The ethanol red herring (`red_herrings[1].field_path`) points to it, and the label cites it as precipitant (4). |
| 38ed2d53-d3ee-4a16-adeb-ba440e700b49 | FIXED | Deleted "Her lithium level is pending" from `patient.history_present_illness` and "Serum lithium level result pending" from `neurological_exam.additional`. Also removed the other timeline leaks in the HPI (C13): "ammonia is 76" and "valproate level is 118". The facts stay: she takes lithium, valproate and quetiapine, and is adherent. Lithium 1.6 now sits only in `labs.panels["Drug levels"]`. |
| 6cff687b-c064-4379-8af0-576e94210eee | FIXED | `prohibited_recommendations[0]` is now PROHIB-BZD (C12), with no haloperidol. Added a prohibition against treating the presentation as mania with an antipsychotic. It names the haloperidol dystonic reaction from `clinical_history.allergies`. |
| fbc4826d-6e7d-4c44-ad89-0d9c2cd79cf6 | FIXED | Deleted the `interpret_labs` `request_lactulose_rifaximin` follow-up (ammonia 76 to 54 to 36), C1/C2. One admission ammonia (76, range 11-51) is in its own panel. The K-AMM pearl is added to `key_clinical_evidence`. |
| 9d18794f-92c2-489f-bea4-78a827983896 | FIXED | "Lactulose 30 mL TID; rifaximin 550 mg BID" is replaced by MUST-LACT (2-3 soft bowel movements per day, ACG 2026 rec. 10; EASL 2022). It adds that over-titration would also raise the lithium level. Rifaximin is removed because this is a first overt episode (plan C3: recurrence only). |
| e4e6c46c-7ba6-4723-9ec4-3af4e7045af2 | FIXED | She is afebrile (37.1 °C), WBC 7.2, CRP 3.4, with no source. Blood cultures (`action-7-order-microbiology`) and urine culture (`action-8-order-microbiology`) are now `recommended`, with `{"specimen": ...}` arguments and the C7 label and rationale. Both are removed from the stop rule. Blocks are one time point ("no growth at 48 hours") with `collected_before_antimicrobials` null (no antibiotic in the case). There is no ascites, so the `interpret_labs` `request_sbp_paracentesis` follow-up ("paracentesis not performed") is deleted (C6). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `action-3-search-medical-literature`, `followup_outputs` (`psychiatry_consult_bipolar_liver_disease`) | Required literature search (C4). Its follow-up stood in for a psychiatry consult and wrongly called lamotrigine "primarily renally eliminated" (it is glucuronidated in the liver). | FIXED: criterion and follow-up deleted. Its content (mood-stabilizer plan) is now a psychiatry must with correct lamotrigine handling. |
| C | major | `followup_outputs` (DI), `action-4-check-drug-interactions` | Both DI outputs read the patient's labs ("Lithium 1.6 ... present in this patient"). They put the diagnosis in the proposal ("Valproate-induced hyperammonemic encephalopathy") and prescribed (stop HCTZ immediately, lamotrigine 25 mg). They missed the lactulose-lithium fluid interaction. The criterion expected generic text. | FIXED: the criterion stays required (C5: two concrete interactions) and accepts the drug names an agent would write (valproate, valproic acid, divalproex, lithium, lithium carbonate, hydrochlorothiazide, HCTZ). Triggers are renamed so every spelling routes to the right report (checked through the MockServer). The valproate output covers urea-cycle inhibition, carnitine depletion, amplification in cirrhosis, and free fraction with albumin 2.8. The lithium output covers thiazide clearance, hyponatremia and volume, and lactulose-induced fluid loss. Both sit last, with case-specific expected evidence. |
| A | major | `action-1-interpret-labs` | Required 10 named panels (C9). The plan's extra "toxicology" is not an advertised `interpret_labs` term: the agent is shown `tox_screen`, and `_contains_required` compares literally. | FIXED: the two C9 alternatives plus `lithium_level`, `valproate_level` and `tox_screen` (all advertised terms). |
| B | major | `initial_tool_outputs.labs` | Lithium filed in the BMP. Duplicate ethanol (22 vs "Not detected"). "Exclusion studies" block. Template TSH 2.1 and zinc 82. INR and ammonia under LFTs. No CRP or potassium (C9). | FIXED: lithium and valproate in a "Drug levels" panel. One ethanol. Added potassium 3.9, magnesium 1.8 mg/dL, lactate 1.6 mmol/L and CRP 3.4 mg/L. TSH 3.6 (relevant on lithium) and zinc 64. INR in Coagulation, ammonia in its own panel. Summaries list only flagged values. |
| C | major | `patient.neurological_exam.mental_status`, `ground_truth.diagnosis.accepted[0]` | GCS 13 (E3V5M5) contradicted the exam: V5 although disoriented, E3 although talkative with pressured speech, M5 although she does finger-nose and forced arm extension. The label gave no grade, and "multifactorial hyperammonemia ... driven by lithium toxicity and quetiapine" is wrong, since neither raises ammonia. | FIXED: GCS 14 (E4V4M6). Disorientation now covers date and day of the week; she knows she is in a hospital but not which one. This is West Haven grade II, without the full spatial disorientation that defines grade III. The label reads "Hepatic encephalopathy (West Haven grade II), alcoholic cirrhosis (Child-Pugh B, MELD-Na 18), with multiple drug and alcohol precipitants: ..." |
| C | major | `accepted[0]`, `past_medical_history[0]` | "Child-Pugh B, MELD 12" cannot be derived from the values. Computed: MELD 16, MELD-Na 18, Child-Pugh B 8 (C10). | FIXED: label as above. The undated score is removed from the PMH (the dash wording there is replaced too). A score pearl is added to key evidence. |
| B | minor | `patient.history_present_illness`, `medications` (hydrochlorothiazide) | The lithium-HCTZ interaction is named as the trigger of the toxicity, but the case gave no start date for the thiazide. | FIXED: hydrochlorothiazide "started 3 weeks ago" by her primary care physician, in the HPI and the medication indication (see Open questions). |
| B | minor | `patient.chief_complaint` | "psychiatric vs metabolic" framed the differential for the agent. | FIXED: "Acute confusion and unusual behavior over 24 hours". |
| B | minor | `neurological_exam.cranial_nerves`, `additional` | Tremor listed under cranial nerves. Extraocular movements not stated, although Wernicke is in the differential. Duplicated, subjective icterus text ("easily dismissed as eye color"). | FIXED: "Extraocular movements full", tremor left under motor, "Mild scleral icterus" (bilirubin 2.4). |
| B | minor | `initial_tool_outputs.ct` | Empty findings and "restricted diffusion" on CT (C8). | FIXED: canonical normal finding and impression. |
| E | minor | `initial_tool_outputs.eeg.findings` | "No spikes or sharp waves despite bipolar disorder history". Interpretation inside a finding row. | FIXED: plain descriptive rows. Background and impression unchanged. |
| C | major | `assessment.required_recommendations` | Vague musts: "check repeat levels", L-carnitine "if confirmed" without a maximum, dialysis at "lithium >2.5" (not the EXTRIP criteria). Rifaximin at a first episode. Alcohol use and transplant not addressed. Quetiapine and the antihypertensive replacement absent. | FIXED: valproate stop with IV L-carnitine (100 mg/kg, max 6 g, then 15 mg/kg every 4 h). Lithium and HCTZ hold with isotonic saline, levels every 6-12 h, and extracorporeal removal per EXTRIP 2015 triggers. MUST-LACT. MUST-THIA with CIWA-Ar monitoring. Psychiatry review (no valproate, quetiapine held, lithium at a reduced dose without a thiazide, lamotrigine adjusted for hepatic impairment). Amlodipine in place of HCTZ. Transplant referral with alcohol-use disorder treatment (MELD-Na 18). |
| C | minor | `assessment.prohibited_recommendations` | Haloperidol boilerplate (note above). Generic LP line with no LP. Acetaminophen dose unspecified. | FIXED: PROHIB-BZD. LP line deleted. Acetaminophen up to 2 g per day. Valproate and HCTZ lines reworded. Anti-mania prohibition added. |
| C | minor | `ground_truth.differential` | Mania left `moderate` after asterixis, hyperammonemia and EEG slowing, with "does not respond to lactulose" as the discriminator (ruling 7). The withdrawal and Wernicke entries gave no supporting or excluding features. | FIXED: mania `low`, discriminated by asterixis and EEG slowing. Lithium-alone and valproate-alone entries rewritten (moderate, contributors). Withdrawal and Wernicke key features drawn from the case (ethanol still detectable, no diaphoresis; eye movements full, ataxia explained by lithium). |
| A | minor | all `action_criteria`, citations, `stop_rule` | Rationales repeated the labels. Mixed citation strings. CT "before any LP" with no LP. Stop rule listed the literature search and cultures (C17). | FIXED: one-sentence rationales with keys and plan labels. Order: labs, blood cultures, urine, CT, EEG, DI. Follow-ups: urine, valproate DI, lithium DI. `required_before_assessment` = labs and DI. |
| E | minor | `metadata.difficulty_description`, `difficulty_rationale` | Referred to "4 required tools + EEG + psychiatry consult". | FIXED: reworded to the rebuilt policy. |

## Changes, in one paragraph a physician can read before re-reviewing

The label now reads "hepatic encephalopathy, West Haven grade II, in alcoholic cirrhosis (Child-Pugh B 8, MELD-Na 18)". It lists four precipitants: valproate-associated hyperammonemia (118 µg/mL), lithium toxicity (1.6 mEq/L) after hydrochlorothiazide was started 3 weeks ago, quetiapine, and recent alcohol (ethanol 22 mg/dL).

**Patient block.** The exam now gives GCS 14 (E4V4M6): disoriented to date and day, knows she is in a hospital, subtle asterixis, full eye movements. The HPI no longer gives the ammonia, valproate or "pending" lithium results. The chief complaint no longer says "psychiatric vs metabolic".

**Deleted.** The serial ammonia panel, the no-ascites paracentesis note and the literature "psychiatry consult".

**Pathway.** Core labs are required, with lithium and valproate levels and one ethanol; the template "not detected" row, TSH and zinc are gone, and magnesium, lactate, CRP and potassium are added. Blood and urine cultures are recommended (afebrile, WBC 7.2). CT is optional. EEG is recommended. The medication review is required: one report on valproate in cirrhosis and one on lithium with hydrochlorothiazide and lactulose.

**Musts.**
- Stop valproate and give L-carnitine.
- Hold lithium and the thiazide, with saline, serial levels and EXTRIP criteria for dialysis.
- Lactulose to 2-3 soft stools a day.
- Thiamine and withdrawal monitoring.
- A psychiatry plan without valproate.
- Amlodipine in place of the thiazide.
- Transplant referral with alcohol treatment.

**Prohibitions.** No sedatives, no sedating opioids, no valproate restart, no thiazide with lithium, and no anti-mania treatment, with haloperidol excluded by her allergy.

Mania is now low in the differential.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1 (`[ACG_HE_2026]`, `[EASL_HE_2022]`).
- `accepted[0]` changed under ruling 3 (C10 scores and grade; plan CENTRAL 6). No ICD or synonym change.
- **For the lead (spans the condition):** `toxicology` is not an advertised `interpret_labs` term; the agent sees `tox_screen`. `ToolCallPattern.matches` (`_contains_required`) compares folded strings without `normalize_analyte`. So a criterion that requires `toxicology` is met only by an agent that types the unadvertised alias. HEP-ENC-M02's lab criterion requires `toxicology`; P02 uses `tox_screen`. Either switch every case to `tox_screen`, or apply plan CENTRAL 4 (normalise analytes in `_contains_required`). The same applies to any other alias used in criteria.
- The plan's citation table has no key for EXTRIP (Decker BS et al., Extracorporeal treatment for lithium poisoning, Clin J Am Soc Nephrol 2015;10:875-887). The must cites it in text. Add `[EXTRIP_lithium_2015]` if musts are to carry keys.

## Open questions for Andrea (judgment calls you could not settle)

- Hydrochlorothiazide start date: I added "started 3 weeks ago" so that the lithium-thiazide interaction explains a new toxicity. Without a date, it was unclear why a stable combination would now produce a level of 1.6.
- Grade: to make grade II hold, I narrowed "disoriented to date and place" to date and day of the week, with partial place orientation. Under the AASLD/EASL 2014 operative criteria, full spatial disorientation is grade III. If you prefer the original exam, the label should say grade III and Child-Pugh becomes 9, still class B.
- L-carnitine is a must with the toxicology dosing (100 mg/kg, max 6 g, then 15 mg/kg every 4 hours). The evidence for valproate-associated hyperammonemia without overdose is case-series level. Make it "consider" if you prefer.
- Transplant referral in a patient who is still drinking: I wrote it together with alcohol-use disorder treatment. Drop the referral part if you consider active drinking a reason to defer even the assessment.

## Verification

Adversarial verifier, 23 Oct 2026. Read the log, the full diff and the final case.
- The six notes are confirmed fixed:
  - Ethanol 22 is reported once, in `Toxicology[0]`, and the red-herring path resolves.
  - "Pending" is gone from the HPI and the exam, and no other result leaks.
  - PROHIB-BZD has no haloperidol.
  - There is no serial ammonia.
  - MUST-LACT gives 2-3.
  - The cultures are `recommended` and out of the stop rule.
- Scores were recomputed: MELD 16, MELD-Na 18 (Na 134); Child-Pugh B 8. GCS 14 (E4V4M6) agrees with the exam. Grade II is supported, because the patient knows she is in a hospital.
- Lab criterion terms `lithium_level`, `valproate_level` and `tox_screen` are all in `costs.yaml`.
- Every drug-interaction alternative routes to the intended report (checked through the environment):
  - valproate, valproic acid, divalproex and divalproex sodium go to the valproate report;
  - lithium, lithium carbonate, hydrochlorothiazide and HCTZ go to the lithium report;
  - quetiapine falls to the valproate report, which covers it.
- The musts and prohibitions do not contradict each other. Nothing prescribes haloperidol. Quetiapine is held. Valproate and the thiazide are stopped.
- Found: nothing that needed a change. The worker's open questions stand:
  - the HCTZ start date;
  - the L-carnitine dosing, which comes from overdose regimens;
  - transplant referral while she is still drinking.
- Note for Andrea on the open questions: EXTRIP 2015 lists confusion among the "suggested" criteria for extracorporeal treatment. The must's escalation triggers (rising level, worsening kidney function, falling consciousness) are a reasonable bedside reading, given that the confusion has several causes here.
- `perfect_agent.py HEP-ENC-P02 -v` passes; `case_io.py check` reports no failure naming the case.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

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

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-1-interpret-labs]`.alternatives: was [CBC, CMP, coagulation, ammonia, lithium_level, valproate_level, tox_screen] | [CBC, BMP, LFTs, coagulation, ammonia, lithium_level, valproate_level, tox_screen]; now [CBC, CMP, coagulation, ammonia, lithium_level, valproate_level, tox_screen, CRP] | [CBC, CMP, coagulation, ammonia, lithium_level, valproate_level, tox_screen] | [CBC, BMP, LFTs, coagulation, ammonia, lithium_level, valproate_level, tox_screen].
- Decision: serve: new first alternative (old order kept as an alternative). The label names CRP with the core bloods (infection is the precipitant to exclude) and the evidence reads it; CBC, CMP, coagulation and ammonia did not return the inflammatory panel.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: cognitive_screen}`: MoCA 15/30, below the normal range (26 or above), with impaired attention, executive function, delayed recall and orientation to time; naming preserved. (fallback_tool_outputs.clinical_assessment). Why: GCS 14, disoriented to time with slowed processing: a MoCA of 28/30 with full orientation is impossible.
- `order_specialized_test {test_type: neuropsych_battery}`: Abnormal neuropsychological profile dominated by slowed psychomotor speed and impaired attention and executive function, with a retrieval-type memory deficit ... (fallback_tool_outputs.specialized_test). Why: disoriented to time with slowed processing: a battery normal in every domain is impossible.
- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 50, ECOG 3. Requires considerable assistance and frequent supervision; capable of only limited self-care. (followup_outputs[request_performance_status]). Why: Karnofsky 100 / ECOG 0 contradicts an inpatient confused, bed- or chair-bound patient.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: Wide-based, unsteady gait with impaired balance: Timed Up and Go 19.4 s; tandem gait not possible. (followup_outputs[request_gait_and_balance_timed]). Why: stored exam gait: unsteady, ataxic gait; walks unaided but cannot tandem.
- `order_specialized_test {test_type: speech_language_evaluation}`: Abnormal speech and language evaluation: articulation intact; mild tremulousness; pressured, rapid output with flight of ideas and disorganized content ... (followup_outputs[request_speech_language_evaluation]). Why: stored exam speech: articulation intact; mild tremulousness; pressured, rapid output with flight of ideas and disorganized content.
- `analyze_eeg {eeg_type: continuous_icu}`: Continuous EEG monitoring over 24 hours: 1. Generalized theta slowing at 5–6 Hz, moderately disorganized background, absent posterior dominant rhythm. No ... (fallback_tool_outputs.eeg). Why: the stored routine EEG is abnormal; a prolonged recording cannot show a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: 48-hour ambulatory EEG: 1. Generalized theta slowing at 5–6 Hz, moderately disorganized background, absent posterior dominant rhythm. No triphasic waves ... (followup_outputs[request_ambulatory]). Why: the stored routine EEG is abnormal; a 48-hour recording cannot be normal.
- `order_advanced_imaging {modality: MR_spectroscopy}`: Abnormal MR spectroscopy: reduction of myo-inositol (mI/Cr 0.28) and choline (Cho/Cr 0.58) with an increased glutamine-glutamate (Glx) peak; NAA preserved; no ... (fallback_tool_outputs.advanced_imaging). Why: characteristic test of the condition: reduced myo-inositol and choline with raised Glx.
- `order_body_imaging {study: pelvis_abdomen_ultrasound}`: Abdominal and pelvic ultrasound with Doppler: 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal vein. 4. Splenomegaly (14.5 cm). 5. No ... (fallback_tool_outputs.body_imaging). Why: cirrhosis with no ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_CT}`: Contrast-enhanced CT of the abdomen and pelvis (arterial and portal venous phases): 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal ... (followup_outputs[request_pelvis_abdomen_ct]). Why: cirrhosis with no ascites: the library reports a normal liver and spleen.
- `order_body_imaging {study: pelvis_abdomen_MRI}`: Contrast-enhanced MRI of the abdomen and pelvis: 1. Cirrhotic liver morphology. 2. No focal liver lesion. 3. Patent portal vein. 4. Splenomegaly (14.5 cm). 5. ... (followup_outputs[request_pelvis_abdomen_mri]). Why: cirrhosis with no ascites: the library reports a normal liver and spleen.
- `interpret_labs {panels: [peripheral_smear]}`: Normocytic, normochromic red cells with occasional target cells; normal white cell morphology; platelets reduced in number, of normal morphology, without ... (fallback_tool_outputs.labs[peripheral_smear]). Why: stored CBC: platelets 94: 'adequate platelets' contradicts it.
- `interpret_labs {panels: [CDT]}`: 2.4 (fallback_tool_outputs.labs[CDT]). Why: wine every night per her sister.

Checks: `perfect_agent.py` pass; `test_case_guards.py -k HEP-ENC-P02` pass; the map verifier serves every listed term from the case; the snapshot of the 322 previously case-answered orders is unchanged.

Lab prose (25 Oct 2026, same pass): the fallback-labs interpretation now gives the smear as one sentence headed `Peripheral blood smear:` (commas, no semicolons), so an order for another panel no longer receives smear fragments; the smear rows are unchanged.
