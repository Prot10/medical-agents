# SE-S10
Reviewer status: R1 not reviewed, R2 not reviewed (no notes) | Approved before this round: treated as approved (plan: no notes, counted among the R2 approvals)

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The notes file has no note for SE-S10. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A/C | major | `initial_tool_outputs.labs`, a2 | There was a template "Exclusion studies" block (ammonia, magnesium, ABG, beta-hCG, urinalysis "Within reference range", plan C1). It contradicted the case: lactate 10.8 with a "normal" ABG, and a "normal" urinalysis in rhabdomyolysis. beta-hCG was taken in a man, and the label read "beta-hCG (here male, n/a)" (C2). Ethanol 0.08 was flagged against a reference of "<0.08". The CMP was partial. There was no acetaminophen or salicylate screen for an unknown ingestion. The summary had causal claims ("severe rhabdomyolysis", "AKI"). | FIXED: block deleted; beta-hCG, ammonia, urinalysis, ABG, lactate and CK removed from the required arguments (T-LABS: CBC, CMP, magnesium, tox_screen). Full CMP with magnesium 1.9, CO2 15. ABG pH 7.14, pCO2 48, pO2 62. Dipstick blood 3+ with 0-2 RBC/hpf. Ethanol reference "<0.01". Acetaminophen and salicylate not detected. Opiate and benzodiazepine screens negative. Amphetamine and TCA results are marked as immunoassays. Factual summary. |
| C | minor | labs (CK) | CK 6840 within about an hour of the convulsion is earlier than CK rises. | FIXED: CK 3120 (exertion, hyperthermia and convulsion); creatinine 1.8 is kept (dehydration and hyperthermia). The musts and expected text are updated. |
| D/B | major | ECG follow-up `request_tca_ecg_management`, a4 | The ECG findings named the drug ("TCA sodium channel blockade", "TCA signature", "TCA + MDMA combined"), which is cross-modality synthesis. The expected text carried management ("sodium bicarbonate indicated"). The ECG sat in a follow-up although plan 3.1 wants it right after the labs. | FIXED: ECG moved to `initial_tool_outputs.ecg` (follow-up deleted). Plain categorical read: sinus tachycardia 152, QRS 128, terminal R in aVR 4 mm with R/S above 0.7, QTc 518. A within-cardiology note "may reflect a sodium-channel blocking drug effect". a4 is placed second, required; the ECG-before-drug-check constraint stays hard. |
| C/D | major | `initial_tool_outputs.eeg`, EEG follow-up | The initial EEG described "massive muscle artifact" and a "stimulant/sympathomimetic pattern" (synthesis). The follow-up was a 12-hour post-treatment "improving" record (ruling 4), and its trigger took over the cEEG order (C4). The EEG criterion had no `eeg_type`. | FIXED: follow-up deleted. Initial EEG in ACNS terms: 20 minutes of continuous generalized 2.5-3.5 Hz spike-and-wave with +F and only subtle facial and finger twitching (subtle SE), then diffuse slowing without seizures. T-EEG criterion. |
| C | major | a7 `interpret_labs` "Rhabdomyolysis and AKI management", rhabdomyolysis literature follow-up | Treatment disguised as a lab criterion (ruling 4, plan C4). The literature output was a patient-specific plan ("CK 6840 with AKI ... 200-500 mL/h"). | FIXED: a7 and that follow-up deleted. Fluids and monitoring are a must. |
| C | major | CSF follow-up `request_lp_autoimmune` | An orphan with no criterion; it claimed "serum tox confirms TCA" (C5). | FIXED: deleted. |
| C/D | major | DDI follow-up, a5 | The output was a treatment protocol (bicarbonate doses, pH targets, cooling) rather than interactions (C4). | FIXED: T-DDI content. Fosphenytoin, lacosamide and class IA, IC and III antiarrhythmics with TCA. TCA with MDMA (serotonergic). Lorazepam with ethanol. Physostigmine and flumazenil contraindications. Levetiracetam has no interaction. Required (C9). |
| C/D | major | a6 literature | Literature was required, and the output had a fabricated "terminal R in aVR >3 mm ... specific for TCA" claim. | FIXED: optional, last. T-LIT on QRS thresholds, bicarbonate and avoiding phenytoin (no allow-listed source exists for TCA, so these are stated without a key per plan 1.1), plus the SE benzodiazepine fact [Glauser_2016]. |
| C | major | `assessment` | No ASM doses were given. Two prohibitions were each duplicated. There was no airway or ventilation must, although GCS 3, SpO2 90 and the acidosis worsen TCA toxicity. Physostigmine was not prohibited. There was no cEEG. | FIXED: T-MUST-BZD; sodium bicarbonate 1-2 mEq/kg to pH 7.45-7.55 with ECG and electrolyte monitoring; airway and ventilation; levetiracetam 60 mg/kg or phenobarbital, avoiding fosphenytoin; active cooling [Boyer_2005]; isotonic fluids with monitoring; T-MUST-cEEG; toxicologist or poison center with telemetry. Prohibitions: phenytoin/fosphenytoin, class IA/IC/III antiarrhythmics, flumazenil, physostigmine (one each). |
| C | major | `ground_truth.differential` | "Isolated TCA overdose" was very_high and "Isolated MDMA" high, which are the components of the label rather than alternatives. Cocaine was moderate despite a negative screen. Diphenhydramine, a classic QRS-widening mimic that gives a false-positive TCA screen, was missing (ruling 7). | FIXED: TCA alone low (MDMA features), MDMA alone low (QRS), serotonin syndrome moderate (an overlapping component), diphenhydramine low, cocaine low (negative), CNS infection low, each stating its result. |
| C | minor | `key_clinical_evidence` | Activated charcoal "may have role", in a convulsing patient with an unprotected airway. | FIXED: replaced by "acidosis worsens TCA cardiotoxicity". |
| A | minor | `fallback_tool_outputs` | `advanced_imaging` "CT chest/abdomen" and `specialized_test` "renal_function_assessment" are not vocabulary (C10). | FIXED: nulled; `fallback_tool_kinds` updated. |
| E | minor | `avoid-waste-5`, `avoid-waste-2` | The PSG entry carried the DaTscan rationale. The Holter rationale "no cardiac comorbidity" contradicts the wide QRS. | FIXED: T-PSG; the Holter rationale now says the 12-lead ECG and inpatient telemetry cover it. |
| D | minor | `initial_tool_outputs.ct` | "No structural cause identified for SE" was a clinical conclusion. | FIXED: plain normal CT. |
| A | minor | `stop_rule`, metadata | `max_additional_actions` was 0, and the stop rule listed literature and a7. | FIXED: labs, ECG, CT, EEG and drug check; max 1; metadata updated. |

## Changes, in one paragraph a physician can read before re-reviewing
SE-S10 keeps its diagnosis: convulsive SE from combined tricyclic and MDMA toxicity with QRS widening, in a 19-year-old after an unknown pill. The pathway is now labs, ECG, CT, cEEG, drug check, then literature (optional). The labs are complete: toxicology immunoassays positive for amphetamines and tricyclics, ethanol 0.08, acetaminophen and salicylate negative, mixed acidosis pH 7.14 with lactate 10.8, CK 3120 with dipstick blood and no red cells, creatinine 1.8, potassium 5.2. The template exclusion block and beta-hCG are gone. The ECG is a plain read (QRS 128, terminal R in aVR, QTc 518) and no longer names the drug. The cEEG shows 20 minutes of subtle SE, then slowing. The post-treatment EEG, the orphan LP and the rhabdomyolysis "lab" criterion are gone. The drug check lists real interactions. The musts are a benzodiazepine, sodium bicarbonate, airway and ventilation, levetiracetam or phenobarbital (no fosphenytoin), cooling, fluids, cEEG and toxicology input. Physostigmine joins flumazenil, phenytoin and the antiarrhythmics as prohibited. The differential now ranks the label's components as low alternatives and adds diphenhydramine.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: `[ACNS_2021]` is cited here and needs the criteria-pack allow-list. No allow-listed source covers TCA toxicology (plan 1.1), so the literature output states those facts without a key; a toxicology reference could be added centrally.

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case (large rewrite).
- No notes. Cross-field checks: beta-hCG and the "here male, n/a" label are gone. The ECG is in the initial outputs and is required second. The hard ECG-before-drug-check constraint is present. The labs agree with the expected text: CK 3120, pH 7.14, pCO2 48, lactate 10.8, Na 134, K 5.2. The musts give bicarbonate for QRS 128, airway, levetiracetam or phenobarbital without fosphenytoin, and cooling. The prohibitions name phenytoin and fosphenytoin, class IA, IC and III antiarrhythmics, flumazenil and physostigmine, once each. The differential is ranked on the results. The literature thresholds (QRS over 100 ms for seizures, over 160 ms for ventricular arrhythmia) are correct and carry no key, as the plan requires. Checks are clean.
- Found and fixed: (1) The drug-check rationale ended with [ESETT_2019], although its content is tricyclic cardiotoxicity and antidote contraindications, which ESETT does not cover. Its `citations` field lists [Brophy_2012]. The key is removed from the rationale, per plan 1.1: no source covers TCA. (2) Red herring 0 named "MDMA positive on tox screen", but the lab reports only an amphetamine immunoassay (includes MDMA). The data point now reads "Urine amphetamine immunoassay positive (includes MDMA)", and the interpretation is reworded without an em dash. (3) The stale `metadata.revision_reason` now points to this log.
- Left as is: the serotonin syndrome differential code T43.225A was there before; ICD coding of the differential is outside this round's scope.

## Close-out (24 Oct 2026)
Decisions in `plans/SE-decisions.md`.
- synonyms: the G41 category no longer grants the type codes G41.0, G41.2 and G41.8 (a type code is granted only by the case's own code, so an answer coded with the wrong SE type no longer scores by code); `apply_diagnosis_synonyms.py --prune --conditions status_epilepticus` removed G41.2 and G41.8 from `ground_truth.diagnosis.icd_codes`. Labels unchanged.
- label: "... with QRS widening requiring sodium bicarbonate" -> "... with QRS widening": the treatment clause is management, not diagnosis (ruling 4; same class as SE-P08). The bicarbonate must is unchanged.
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, SE case guards pass, `apply_diagnosis_synonyms.py --check --conditions status_epilepticus` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `continuous_icu`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## EEG and labs after routing (25 Oct 2026)

Commit 317e46db routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG) and serves an `interpret_labs` order only the stored panels it names. Decisions for the condition in `plans/SE-routing-decisions.md`.

- EEG: a routine order received the library's normal routine EEG, which contradicts the case. Added `fallback_tool_outputs.eeg` with `eeg_type` `routine` (the stored continuous_icu recording cut to a 30-minute portable recording without video, technologist notes for the clinical events, activation not performed): continuous generalized spike-and-wave (+F) for the first 20 minutes (electrographic SE), then diffuse slowing without seizures. No criterion, tiers and the reward-relevant policy unchanged; the clinically correct test stays the continuous EEG of `action-1-analyze-eeg`. A `continuous_icu` or `video` order still receives `initial_tool_outputs.eeg`.
- Labs `action-2-interpret-labs`: unserved result cited in `expected_evidence`: pH 7.14, lactate 10.8, CK 3120 (Blood Gas and Muscle Enzymes). EXTEND with CK: a must treats rhabdomyolysis with acute kidney injury on CK 3120; the CK order returns the whole stored panel, so pH and lactate stay in the evidence. Scoring change: yes.
  - action-2-interpret-labs required_arguments.panels ['CBC', 'CMP', 'magnesium', 'tox_screen'] -> ['CBC', 'CMP', 'magnesium', 'tox_screen', 'CK']
  - action-2-interpret-labs label -> 'Emergency laboratory work-up: glucose, CBC, electrolytes, magnesium, renal and hepatic function, toxicology screen, CK'
  - action-2-interpret-labs rationale + 'CK because rhabdomyolysis follows prolonged convulsions with hyperthermia and decides the fluid management.'
- Checks: `perfect_agent.py -v` pass; `case_io.py check` schema and synonym guard OK, no test failure names the case; probe: routine (omitted and explicit) order -> the new case fallback, `continuous_icu` and `video` -> the stored index recording; every number in each lab criterion's evidence is in what its order returns.

## Matcher fix (25 Oct 2026)

The lab matcher now keeps a urine or CSF row out of a blood order: a urinalysis, urine sodium or urine osmolality row answers only an order that names the urine assay, so a CBC or CMP order no longer returns the urine results. The lab criterion therefore names the urine assays its expected evidence cites.

- `ground_truth.action_criteria[action-2-interpret-labs]`: new first alternative `{panels: ['CBC', 'CMP', 'magnesium', 'tox_screen', 'CK', 'urinalysis']}` (adds `urinalysis`); the previous orders stay as alternatives, so every call that matched before still matches. The expected evidence reads dipstick blood without red cells, which the first order received only through two matcher defects fixed on 25 Oct 2026: a urine row answered a blood-count or metabolic order (`Urine WBC` as WBC, `Urine sodium` as sodium, a urine creatinine ratio as creatinine), and the unit `mg/dL` read as magnesium. Scoring: cost reference only (the policy's reference order is fuller); coverage unchanged.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although this case contradicts it (diagnosis, history, medications or a stored finding) now get a case-specific report; every other off-pathway order still gets the library normal. No tier, criterion, diagnosis or existing output changed.

- `analyze_eeg eeg_type=ambulatory` -> `followup_outputs[order_ambulatory]`: ambulatory EEG mirroring the stored continuous EEG (no video).
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[order_performance_status]`: performance status KPS 20, ECOG 4 during the admission.
- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `followup_outputs[order_gait_and_balance_timed]`: timed gait not testable, as on the examination.
- `perform_clinical_assessment assessment_type=cognitive_screen` -> `followup_outputs[order_cognitive_screen]`: baseline cognitive screen not testable in the documented mental state.
- `order_specialized_test test_type=neuropsych_battery` -> `followup_outputs[order_neuropsych_battery]`: neuropsychological battery not testable in the documented mental state.
- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: speech and language evaluation not testable in the documented mental state.
- `labs:lithium_level` -> fallback labs panel `Lithium`: lithium not detected (not prescribed).
- `labs:AED_levels` -> fallback labs panel `Antiseizure medication levels`: antiseizure drug levels: none detected (no antiseizure drug prescribed).
- `labs:valproate_level` -> fallback labs panel `Antiseizure medication levels`: antiseizure drug levels: none detected (no antiseizure drug prescribed).

Checks: `perfect_agent.py` ok; `test_case_guards.py -k SE` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
