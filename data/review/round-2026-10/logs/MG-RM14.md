# MG-RM14
Reviewer status: none (condition not reviewed in this round; July 2026 tool review only) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none | - | No reviewer notes for this case (`notes/MG.md` does not exist). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.additional` | HPI ended "Her NIF is -18 cmH2O ... at threshold for intubation" (em dash); exam held NIF and FVC (scored respiratory result, class K). | FIXED: numbers removed; bedside picture kept (accessory muscles, weak cough, pooled secretions, SpO2 91%); absence of muscarinic signs stated for the cholinergic differential. |
| B | minor | `patient.history_present_illness`, `clinical_history.past_medical_history` | "Stable remission on pyridostigmine for 2 years" against "minimal symptoms for 18 months"; AChR status not in the history although it is not scored. | FIXED: diagnosed 2 years ago, remission on pyridostigmine alone for 18 months; AChR-positive at diagnosis and CT without thymoma kept as history; the urgent care urine culture result added as history. |
| A | minor | `patient.physical_exam` | No weight or height for mL/kg. | FIXED: 72.4 kg, 160 cm (matches BMI 28.3). |
| C | major | `initial_tool_outputs.specialized_test` | Respiratory report built from bedside notes ("formal RNS deferred", bulbar observation), no mL/kg, no MEP, recommended RNS. | FIXED: FVC 1.2 L (38%, 16.6 mL/kg), MIP -18, MEP 28 cmH2O, single-breath count 8, weak cough, all flagged; numbered impression; no recommended actions. |
| A | major | `initial_tool_outputs.labs` | NIF, FVC in labs (class H8); urine culture in labs; TSH stub row (class G); AChR reference "<0.5"; ABG as a qualitative string; interpretation a list of flags. | FIXED: CBC, BMP with magnesium and phosphate, CRP, ABG as rows (pH 7.34, pCO2 52, pO2 58), urinalysis, TSH and free T4, AChR 8.4 nmol/L against <=0.02; respiratory values moved to the respiratory report; culture moved to microbiology; report-voice interpretation. |
| C | major | `initial_tool_outputs.microbiology` | Urine culture growing pansensitive E. coli although taken on day 4 of an effective antibiotic. | FIXED: the pre-treatment urgent care culture is history; today's culture (on treatment) shows no significant growth, `collected_before_antimicrobials: false`. New recommended criterion `action-urine-culture`. |
| C | major | `initial_tool_outputs.body_imaging`, new follow-up `request_mediastinum_ct` | Only a thymoma-screening CT, with interpretive text ("no imaging correlate to account for..."); no chest radiograph for aspiration in a patient who cannot swallow. | FIXED: initial chest radiograph (xray, chest: low volumes, bibasal atelectasis, no consolidation) with a new recommended criterion; the CT moved to a follow-up (mediastinum, chest), reworded. |
| B | major | `followup_outputs` | Six follow-ups: post-plasmapheresis NIF/FVC/AChR and pre-IVIG labs (class J, results of treatment), long-term immunosuppression "drug check" (class C), two literature outputs with unverifiable sources and the wrong "Rule of 20-30: intubate if NIF <-20" (fact 23). | FIXED: all deleted; no literature output kept (no literature criterion). |
| C | major | `initial_tool_outputs.drug_interactions`, `action-4` | Drug check was the generic pyridostigmine screen with `screen_for` (unreachable) and telithromycin; the ciprofloxacin check lived in a follow-up written in capitals with a treatment plan. | FIXED: one initial output keyed `ciprofloxacin` in checker voice (FDA boxed warning, stop; levothyroxine minor; losartan and pyridostigmine none; MG drug list; nitrofurantoin or fosfomycin as alternatives). Criterion required, `{drug: ciprofloxacin}`. |
| C | minor | `initial_tool_outputs.ecg` | Findings attributed the tachycardia to anxiety (interpretive). | FIXED: report voice. |
| C | major | `action_criteria` tiers and order | Template set: MuSK and LRP4 in the labs criterion of a known AChR-positive patient; literature required with an exact query; mediastinal CT required although thymoma was excluded and the precipitant is clear. | FIXED (plan 3.5 crisis pathway): respiratory (required, first), ciprofloxacin check (required), labs `[CBC, BMP, CRP]` (required), urine culture and chest radiograph (recommended), AChR repeat (optional), mediastinal CT with chest CT alternative (optional); literature criterion deleted. |
| C | major | `sequence_constraints`, `stop_rule` | Constraint "literature before respiratory"; stop rule with literature and CT, 0 extra actions. | FIXED: soft respiratory -> CT (lying flat worsens diaphragmatic weakness); stop rule respiratory, drug check, labs; `max_additional_actions: 2`. |
| C | major | `assessment.required_recommendations` | Intubation thresholds "FVC <15 mL/kg or NIF less negative than -25"; "PLEX or IVIG within 24 hours" without doses; no plan for pyridostigmine, steroids or thymectomy. | FIXED: ICU and elective intubation now (20/30/40 crossed with hypercapnia; reduced-dose non-depolarising blocker), stop ciprofloxacin and use an MG-safe antibiotic, PLEX 5 exchanges or IVIG 2 g/kg, hold pyridostigmine while intubated, steroids under ventilatory monitoring with azathioprine after TPMT and a thymectomy discussion (MGTX, 55), drug list. No aspirin (listed intolerance). |
| C | minor | `assessment.prohibited_recommendations` | Template set with telithromycin and the functional-disorder line. | FIXED: no fluoroquinolone, aminoglycoside or macrolide for the UTI; canonical drug and steroid prohibitions; do not wait for desaturation; do not raise pyridostigmine. |
| C | major | `ground_truth.differential` | Cholinergic crisis `moderate` at 180 mg/day without muscarinic signs; aspiration/sepsis moderate without supporting data; PE "D-dimer and CT angiography may be warranted". | FIXED: cholinergic low, aspiration or sepsis low (clear radiograph, sterile culture), PE very_low (hypercapnic neuromuscular failure), cardiac and thymoma very_low. |
| C | minor | `key_clinical_evidence`, `red_herrings[0]`, `metadata` | Template bullets (SFEMG sensitivity, thyroid eye disease); difficulty "8 required tools"; withdrawn RNS, SFEMG and ice pack entries. | FIXED: five case bullets; red herring reworded; difficulty text updated; withdrawn entries cleared (RNS and SFEMG are now waste actions, ice pack has no place in crisis). |
| C | minor | `avoided_actions[*]` | `[Wolfe_2016]` on every waste item; RNS and SFEMG not listed. | FIXED: case rationales, citations emptied; RNS and SFEMG added as waste with the plan's rationale. Fallback head-CT impression set to the canonical text. |

## Changes, in one paragraph a physician can read before re-reviewing

A 55-year-old woman with AChR-positive generalised MG in remission on pyridostigmine 180 mg/day develops ptosis, bulbar and limb weakness and dyspnoea from the day after starting ciprofloxacin for cystitis. The pathway is now the crisis pathway: bedside respiratory function first (required; FVC 1.2 L, 38%, 16.6 mL/kg, MIP -18, MEP 28 cmH2O, weak cough), the ciprofloxacin check (required; boxed warning), blood count, electrolytes with magnesium and phosphate, CRP and ABG (required; mild leukocytosis, hypercapnic acidosis), urine culture and chest radiograph (recommended; no growth on treatment, atelectasis only), AChR repeat and mediastinal CT (optional). RNS and SFEMG are waste. Musts: ICU and elective intubation, stop ciprofloxacin and use an MG-safe antibiotic, PLEX or IVIG, hold pyridostigmine while intubated, steroids under monitoring with azathioprine after TPMT and a later thymectomy discussion, drug list. Cholinergic crisis and infection as the main driver are low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys in text only: Lawn 2001 (plan CENTRAL 1).
- Synonyms: "myasthenic crisis" should be accepted under G70.01 (plan CENTRAL 3); this case's `accepted` list still carries "ocular myasthenia gravis" from the shared group.

## Open questions for Andrea (judgment calls you could not settle)

- None that need Andrea's information. Decisions recorded: (1) mediastinal CT is `optional` (plan 3.5 leaves M04 and RM14 to the worker): the history documents a CT without thymoma at diagnosis 2 years ago and the crisis has a clear drug trigger. (2) Today's urine culture shows no growth, because a culture taken on day 4 of an effective antibiotic would not grow a sensitive E. coli; the positive pre-treatment culture is history. (3) The musts call for elective intubation now rather than a trial of non-invasive ventilation, because hypercapnia (pCO2 52) predicts NIV failure in myasthenic crisis.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log and the whole final case. No reviewer notes exist for MG. Checked each own-finding row against the file: NIF/FVC out of the patient block with the bedside picture kept; remission timeline (diagnosed 2 years ago, remission 18 months) consistent; respiratory values correct (FVC 1.2 L = 16.6 mL/kg at 72.4 kg, 38% of 3.2 L) and all flagged; BMI 28.3 matches; ABG coherent for acute hypercapnia (pH 7.34, pCO2 52, HCO3 27); urine culture on day 4 of ciprofloxacin is sterile and `collected_before_antimicrobials` false, with the pre-treatment culture as history; ciprofloxacin output in checker voice with the FDA boxed warning and MG-safe alternatives that match the reported susceptibilities; treatment-response follow-ups and the "Rule of 20-30" literature are gone; RNS and SFEMG are waste avoided actions; no must prescribes aspirin (listed intolerance); cholinergic crisis low at 180 mg/day without muscarinic signs, with the exam stating their absence; constraint respiratory before CT is soft.

No error found; nothing changed. Noted for CENTRAL (already in the log): "ocular myasthenia gravis" and the missing "myasthenic crisis" synonym. `perfect_agent.py MG-RM14 -v` passes, `case_io.py check` reports no failure naming the case, case guards pass.

## Condition audit (MG auditor, 24 Oct 2026)

- action-1-interpret-labs: alternative panels [CBC, CMP, CRP] added (as M04 and RM15 accept CMP for BMP). FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.

## Close-out (24 Oct 2026)

- `icd_codes[0]` G70.01 kept (exacerbation or crisis). G70.00 ("without exacerbation") is no longer accepted; crisis and exacerbation labels added (myasthenic crisis, myasthenic exacerbation, impending myasthenic crisis, MG crisis, MG exacerbation): the case is an impending or established crisis and its differential rates crisis high.
- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'myasthenic crisis', 'myasthenic exacerbation', 'impending myasthenic crisis', 'MG crisis', 'MG exacerbation', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG']; icd_codes = ['G70.01', 'G70.0']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-achr-repeat` label: "Repeat AChR antibody (optional)" -> "Repeat AChR antibody"
- criterion `action-2-order-body-imaging` label: "Repeat mediastinal CT once stable (optional)" -> "Repeat mediastinal CT once stable"

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 68 -> 72.4 kg, height 155 -> 160 cm, BMI 28.3 -> 28.3 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 72.4 kg, height 160 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 20, ECOG 4 (very sick; hospital admission and active supportive treatment necessary) (fallback_tool_outputs.clinical_assessment). Why: rule 1: the library reports Karnofsky 100 / ECOG 0 (no evidence of disease, working); rule 3: crisis with FVC 1.2 L, neck flexors 1/5 and inability to walk.
- `order_specialized_test {test_type: emg_ncs}`: normal nerve conductions and needle EMG, stating that neuromuscular transmission was not assessed (fallback_tool_outputs.specialized_test). Why: rule 1: the library report concludes there is no neuromuscular junction disorder, which routine conductions and needle EMG without repetitive stimulation cannot assess and which is not true here; AChR-positive myasthenia in crisis.
- `order_specialized_test {test_type: emg_single_fiber}`: severely increased jitter with frequent blocking in EDC and frontalis (followup_outputs[1] request_emg_single_fiber). Why: rule 1: AChR-positive myasthenia in crisis (binding antibody 8.4 nmol/L); the library reports normal jitter.
- `order_specialized_test {test_type: repetitive_nerve_stimulation}`: decrement 34% nasalis, 29% trapezius, 16% ADM (followup_outputs[2] request_repetitive_nerve_stimulation). Why: rule 1: AChR-positive myasthenia in crisis with severe generalized weakness; the library reports no decrement.
- `order_specialized_test {test_type: ice_pack_test}`: positive bilaterally (MRD1 +2.5 mm) (followup_outputs[3] request_ice_pack_test). Why: rule 3: severe bilateral ptosis with the eyes nearly closed at rest; the library reports no ptosis at baseline.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: not performed, unable to stand safely (followup_outputs[4] request_gait_and_balance_timed). Why: rule 3: the library reports a normal timed gait (TUG 9.1 s, Berg 56/56); the examination documents that she is unable to walk safely.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: not performed, oral challenge unsafe in crisis (followup_outputs[5] request_levodopa_challenge). Why: rule 3: severe dysphagia and respiratory distress; the library describes a normal walking examination.
- `order_specialized_test {test_type: speech_language_evaluation}`: severe flaccid dysarthria, barely intelligible; language normal (followup_outputs[6] request_speech_language_evaluation). Why: rule 3: the library reports no dysarthria; the examination documents nasal, barely intelligible speech.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: not performed, unable to stand; supine 158/96, HR 118 (followup_outputs[7] request_orthostatic_blood_pressure). Why: rule 3: unable to stand in crisis, BP 158/96 and HR 118; the library reports a standing test with BP 128/78 and HR 68.
- Case fallback replaced, `fallback_tool_outputs.cardiac_monitoring`: persistent sinus tachycardia (mean 108, minimum 92, maximum 132 bpm) without arrhythmia, in place of a normal sinus rhythm with minimum 49 bpm. Why: rule 3: sinus tachycardia at 118 bpm on the stored ECG and at the bedside in respiratory distress; the case fallback reported sinus rhythm averaging 80 bpm.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
