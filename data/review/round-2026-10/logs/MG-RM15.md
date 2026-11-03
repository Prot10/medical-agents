# MG-RM15
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MG) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. July 2026 tool guidance (Reviewer 2) applied through the plan: crisis pathway 3.5, no CSF, mediastinal imaging optional here because he is post-thymectomy with an explained precipitant (plan 3.5, CENTRAL 5). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | blocker | `initial_tool_outputs.labs` | Labelled established AChR-positive MG, but the labs showed anti-AChR, MuSK and LRP4 "Negative" and TSH "Within reference range" with no units, all with the stub "Ordered to exclude an alternative cause" (plan L, G). | FIXED: crisis panel with real values: CBC (WBC 13.6, neutrophils 11.4), BMP (K 3.9, glucose 138), magnesium 2.0 mg/dL, phosphate 3.4 mg/dL, CRP 46 mg/L, procalcitonin 0.18, lactate 1.4, TSH 1.9, pre-intubation ABG (pH 7.22, PaCO2 69, PaO2 58) and ventilated ABG. No antibody rows. |
| B | major | `followup_outputs` (new `request_achr_binding_antibody`) | An agent re-ordering AChR would have received the general panel or a negative result. | FIXED: AChR binding 9.4 nmol/L (ref <=0.02), served only for an antibody order; not scored (diagnosis known). |
| C | major | `ground_truth.action_criteria` | Template criteria for a new diagnosis (AChR/MuSK/LRP4/TSH, RNS required, SFEMG recommended, mediastinal CT required, literature and generic pyridostigmine check required) in a known AChR+ patient in crisis (plan A, 3.5). | FIXED: respiratory function required (first); labs `["CBC","BMP"]` or `["CBC","CMP"]` required; chest X-ray (new `action-chest-xray`) and endotracheal aspirate culture (new `action-tracheal-aspirate`, specimen `sputum`) recommended; mediastinum/chest CT with contrast optional; atracurium drug check recommended; literature optional `{}`, last. Labels and rationales rewritten and distinct. |
| C | major | `followup_outputs` RNS and SFEMG; `avoided_actions` | RNS and SFEMG reports "72 hours post-extubation" (after the encounter; timeline impossible at the consult) for a diagnosis already established. | FIXED: both follow-ups and criteria deleted; new waste avoided actions `avoid-waste-rns`, `avoid-waste-sfemg` with the plan's rationale. |
| D | major | `followup_outputs` respiratory_function | Stub "All values within normal limits" for the scored result of a crisis. | FIXED: bedside VC 0.9 L (26% predicted, 12.9 mL/kg; 68% fall from admission 2.8 L), MIP -16 cmH2O (admission -42), MEP 28 cmH2O, failed SBT (RSBI 142 = 34/0.24), weak cough; TOF 4/4 and sedation hold stated. Weight 70 kg, height 168 cm added to `physical_exam.general`; `demographics.bmi` 24.9 -> 24.8 to match. |
| D | major | `patient.history_present_illness` | NIF -42 and FVC 2.8 L (82%) in the HPI while respiratory function is scored (plan K, fact 16); post-intubation radiograph result stated while the chest X-ray is a criterion. | FIXED: numbers moved to the respiratory report as the admission comparison; HPI says measurements were recorded and he was not breathless; "A post-intubation chest radiograph was obtained." |
| B | minor | `patient.physical_exam.respiratory` | "Right lower lobe decreased breath sounds" against right apical collapse; "on imaging" leaked the image. | FIXED: reduced breath sounds and crackles over the right upper zone. |
| A | minor | `patient` extra keys `age`, `ethnicity`, `hpi`, `pmh`, `sex` | Invisible duplicates (plan K). | FIXED: ethnicity moved to `demographics.ethnicity`; duplicates dropped (content identical to the kept fields). |
| B | major | `initial_tool_outputs.body_imaging` | Chest CT stored with `contrast: false` while describing IV contrast; served as the only chest imaging. | FIXED: initial body imaging is now the chest radiograph (tube position, RUL apical collapse with aspirated contrast); the CT moved to follow-up `request_mediastinum_ct`, `contrast: true`, region "chest and mediastinum" so it also answers `chest_CT`; no residual thymic tissue; venous-phase pulmonary arteries without filling defect. |
| D | major | `followup_outputs` `check_atracurium_in_mg` | Patient-specific conclusion ("this will contribute to prolonged paralysis"), `proposed` a trigger slug, "dose reduced by 50-75%" unsourced. | FIXED: checker voice, `proposed` atracurium, interactions with pyridostigmine, prednisolone (myopathy risk), mycophenolate; MG sensitivity, succinylcholine resistance, sedative effect; alternatives rocuronium with sugammadex. Added an antibiotic check follow-up (ceftriaxone; metronidazole; beta-lactams generally safe; FQ/aminoglycosides/macrolides avoided) so an antibiotic query is answered with antibiotic content. |
| D | major | `initial_tool_outputs.literature_search` | Summary equal to the expected evidence (leak guard failure, plan B); empty literature follow-up. | FIXED: crisis-topic output citing Sanders 2016, Narayanaswami 2021, Lawn 2001 in report voice; empty follow-up and `request_plasmapheresis_evaluation` (empty labs, treatment as test, plan J) deleted. Guard passes. |
| C | major | `ground_truth.assessment.required_recommendations` | "Long-term plan: rituximab, eculizumab" only; no steroid, swallow or antibiotic specifics; no extubation criteria. | FIXED: seven musts: ICU ventilation with extubation on objective recovery; PLEX (5 exchanges) or IVIG 2 g/kg; hold pyridostigmine while intubated; continue and increase prednisolone under ventilation; MG-safe antibiotic (ceftriaxone or piperacillin-tazobactam) if pneumonia, culture-guided; nil by mouth, NG feeding, SLT swallow assessment; refractory MG escalation (mycophenolate dose, complement inhibitor with meningococcal vaccination, FcRn antagonist or rituximab, Narayanaswami 2021). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Shared template set (telithromycin, outpatient prednisone, functional attribution after SFEMG) irrelevant here (plan D). | FIXED: canonical drug prohibition; no premature extubation; do not attribute the failure to aspiration alone without measuring strength. |
| C | major | `ground_truth.differential` | Cholinergic crisis moderate at 240 mg/day without muscarinic signs; sepsis moderate without sepsis features; "recurrent thymoma" after resection of hyperplasia (plan M). | FIXED: aspiration pneumonitis high as the coexisting precipitant (with why it does not explain the failure); cholinergic crisis low; sepsis low; residual thymic tissue low (E32.0); prolonged NMB from atracurium low (new); PE very_low; each with the excluding data. |
| E | minor | `ground_truth.key_clinical_evidence`, `red_herrings` | Template statements (titin, "all confirmed MG require CT", telithromycin); red herrings with empty paths and a CT that the agent no longer receives first. | FIXED: case-specific evidence; red herring paths set (`initial_tool_outputs.body_imaging`, `.labs`, `patient.history_present_illness`). |
| C | minor | `ground_truth.avoided_actions` | `[Wolfe_2016]` on every waste item; cardiac monitoring penalised in a ventilated ICU patient (telemetry is standard care). | FIXED: rationales written for this case, citations cleared; cardiac monitoring avoided action deleted (normal fallback stays). |
| A | minor | `stop_rule`, `sequence_constraints` | Max 0; literature and drug check listed as required. | FIXED: required respiratory function and labs; max 2; soft respiratory -> CT constraint (plan 3.3). |
| D | minor | `fallback_tool_outputs.ct`, `.advanced_imaging`, `initial_tool_outputs.ecg` | Head CT fallback said it "does not address the question" (plan F); advanced-imaging fallback labelled "MRI brain"; ECG text "relevant given ICU medications pending". | FIXED: plain head CT impression; modality cleared; ECG note trimmed. |

## Changes, in one paragraph a physician can read before re-reviewing

A 50-year-old man with AChR-positive generalized MG (thymectomy for hyperplasia 18 months ago, two earlier infective crises, on pyridostigmine 60 mg every 6 hours, mycophenolate 500 mg twice daily and prednisolone 10 mg) aspirates contrast during a swallowing study, then his respiratory rate falls from 22 to 10 with falling saturation, and he is intubated with midazolam and atracurium. The policy is now the crisis pathway: bedside respiratory function first (required; VC 0.9 L, 12.9 mL/kg, a 68% fall, MIP -16, MEP 28, failed breathing trial), crisis labs (required; leukocytosis, CRP 46, normal potassium, magnesium and phosphate, hypercapnic acidosis before intubation), chest radiograph and endotracheal aspirate (recommended), an atracurium drug check (recommended), and optional chest CT and literature. RNS and SFEMG are now waste (the old reports were dated after extubation), and the contradictory "AChR negative" labs are gone. Musts cover ventilation and objective extubation criteria, PLEX or IVIG, holding pyridostigmine, continuing and raising prednisolone under ventilation, an MG-safe antibiotic, swallow assessment and refractory-disease escalation. Cholinergic crisis and sepsis are now low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[Narayanaswami_2021]`, `[Jacob_2025]`, `[Lawn_2001]` (plan 5.1); cited by name in rationales until they exist.
- Synonyms (plan 5.3): add "myasthenic crisis" to the accepted labels for G70.01; "ocular myasthenia gravis" is currently accepted for this generalized crisis.
- Guidance claims (plan 5.5): mediastinum CT is optional in RM15.
- Vocabulary: no `endotracheal_aspirate` microbiology specimen; `sputum` is used for the tracheal aspirate.

## Open questions for Andrea (judgment calls you could not settle)

- None that need information only Andrea has. Decisions taken: thymic re-imaging optional (thymectomy done, precipitant explained); AChR titre available as an unscored follow-up rather than removed, so a re-order is answered consistently with the history.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the plan (3.5 crisis pathway, RM15 entry) and the whole final case. Checked: no reviewer notes exist (none missing); every own finding marked FIXED is present in the file (crisis labs without antibody rows, AChR 9.4 nmol/L only as an unscored follow-up, RNS/SFEMG removed and set as waste, respiratory report, chest radiograph initial, CT follow-up with `contrast: true`, atracurium and antibiotic checks in checker voice, extra patient keys gone, red-herring paths). Arithmetic verified: VC 0.9 L / 70 kg = 12.9 mL/kg, admission 2.8 L = 40 mL/kg, fall 68%, RSBI 34/0.24 = 142, BMI 70/1.68^2 = 24.8; pre-intubation ABG (pH 7.22, PaCO2 69, HCO3 27) and ventilated ABG are Henderson-Hasselbalch consistent; `collected_before_antimicrobials` false matches the metronidazole dose. No allergy conflict (NKDA; piperacillin-tazobactam allowed). Literature and drug outputs pass the leak guard.

Found and fixed:
- C major, `key_clinical_evidence[5]` and the last `required_recommendations` item: "a third crisis despite thymectomy, mycophenolate and prednisolone defines refractory disease" is wrong. Refractory MG (Sanders 2016) means no response to corticosteroids and at least two other immunosuppressants at adequate dose and duration; he takes mycophenolate 500 mg twice daily (half the usual dose) and prednisolone 10 mg. Rewritten: inadequately controlled disease; escalate mycophenolate to a therapeutic dose, and only if still uncontrolled despite adequate treatment consider a complement inhibitor (with meningococcal vaccination, Narayanaswami 2021), rituximab or an FcRn antagonist (the FcRn antagonist is no longer attributed to the 2021 update, which predates it).
- E minor, `metadata.difficulty_rationale`: "9 required tools, 1 red herrings" was stale; now 2 required, 4 red herrings.

Re-ran `perfect_agent.py MG-RM15 -v` (pass, no warnings), `case_io.py check` (no failure names the case) and the case guards (pass).

## Condition audit (MG auditor, 24 Oct 2026)

- fallback_tool_outputs.echo.echo_type set to TTE. FIXED.
  Why: the discriminator guard (PATTERNS.md section 5) requires an exact vocabulary value on every case fallback; an empty echo_type answered every echo variant. The RS11-RS16 verifiers fixed this only in their own cases.
- fallback_tool_outputs.advanced_imaging (empty modality) set to null; metadata.fallback_tool_kinds.advanced_imaging removed. FIXED.
  Why: a fallback with an empty modality answers every advanced-imaging study with one generic report; the benchmark library now serves the normal report for the study actually ordered.
- metadata.actions_withdrawn: stale ice-pack entry ('recommended here') removed; no ice-pack criterion in a ventilated crisis. FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.

## Close-out (24 Oct 2026)

- `icd_codes[0]` G70.01 kept (exacerbation or crisis). G70.00 ("without exacerbation") is no longer accepted; crisis and exacerbation labels added (myasthenic crisis, myasthenic exacerbation, impending myasthenic crisis, MG crisis, MG exacerbation): the case is an impending or established crisis and its differential rates crisis high.
- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'myasthenic crisis', 'myasthenic exacerbation', 'impending myasthenic crisis', 'MG crisis', 'MG exacerbation', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG']; icd_codes = ['G70.01', 'G70.0']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.

## Vocabulary wiring (24 Oct 2026)

New `order_microbiology` specimen `tracheal_aspirate` (MG decisions CENTRAL; summary item 7). No clinical text changed.

| field path | change |
| --- | --- |
| `followup_outputs[1]` (`request_tracheal_aspirate_culture`) `.output.specimen` | `sputum` -> `tracheal_aspirate` (the report is an endotracheal aspirate) |
| `ground_truth.action_criteria[action-tracheal-aspirate]` | `required_arguments.specimen` `sputum` -> `tracheal_aspirate` |

Scoring change: a `sputum` order no longer credits the aspirate criterion and is answered by the library sputum report.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-1-interpret-labs]`.alternatives: was [CBC, BMP] | [CBC, CMP]; now [CBC, BMP, magnesium, phosphate, CRP] | [CBC, BMP] | [CBC, CMP].
- Decision: serve: new first alternative (old order kept as an alternative). The label and rationale ask for magnesium, phosphate and CRP as crisis precipitants; the aspiration differential relies on CRP 46. None was returned by CBC + BMP.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 73.4 -> 70 kg, height 172 -> 168 cm, BMI 24.8 -> 24.8 (the prompt shows height, weight and BMI).
- Why: rule 1: followup_outputs[0].output.findings[0].description states weight 70 kg, height 168 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 20, ECOG 4 (very sick; hospital admission and active supportive treatment necessary) (fallback_tool_outputs.clinical_assessment). Why: rule 1: the library reports Karnofsky 100 / ECOG 0 (no evidence of disease, working); rule 3: intubated and sedated on mechanical ventilation.
- `order_specialized_test {test_type: emg_ncs}`: normal nerve conductions and needle EMG, stating that neuromuscular transmission was not assessed (fallback_tool_outputs.specialized_test). Why: rule 1: the library report concludes there is no neuromuscular junction disorder, which routine conductions and needle EMG without repetitive stimulation cannot assess and which is not true here; AChR-positive myasthenia in crisis.
- `order_specialized_test {test_type: emg_single_fiber}`: increased jitter with blocking in orbicularis oculi (stimulated) (followup_outputs[6] request_emg_single_fiber). Why: rule 1: AChR-positive myasthenia in crisis (binding antibody 9.4 nmol/L); the library reports normal jitter.
- `order_specialized_test {test_type: repetitive_nerve_stimulation}`: decrement 21% nasalis, 9% trapezius, 4% ADM, train-of-four 1.0 (followup_outputs[7] request_repetitive_nerve_stimulation). Why: rule 1: AChR-positive myasthenia in bulbar-predominant crisis; the library reports no decrement.
- `order_body_imaging {study: mediastinum_MRI}`: post-thymectomy mediastinum without residual tissue; right apical collapse (fallback_tool_outputs.body_imaging). Why: rule 2 and 3: thymectomy 18 months ago and right upper lobe apical collapse on the stored CT; the library reports a normal involuted thymus.
- `order_advanced_imaging {modality: whole_body_FDG_PET}`: inflammatory uptake in the collapsed right upper lobe segment, empty thymic bed (fallback_tool_outputs.advanced_imaging). Why: rule 2 and 3: thymectomy and aspiration-related right apical collapse; the library reports normal lungs and thymus.
- `interpret_labs {panels: [tox_screen]}`: urine benzodiazepines positive (midazolam given at intubation), rest negative (fallback_tool_outputs.labs['tox_screen']). Why: rule 2: intubated with intravenous midazolam; the library reports a negative benzodiazepine screen.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: not performed, intubated and sedated (followup_outputs[8] request_gait_and_balance_timed). Why: rule 3: the library reports a normal timed gait (TUG 9.1 s, Berg 56/56); the examination documents that gait was not assessed (intubated).
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: not performed, intubated and sedated (followup_outputs[9] request_levodopa_challenge). Why: rule 3: intubated and sedated; the library describes a normal walking examination.
- `order_specialized_test {test_type: speech_language_evaluation}`: not assessable (intubated and sedated) (followup_outputs[10] request_speech_language_evaluation). Why: rule 3: the library reports no dysarthria; the examination documents that he is intubated, so speech cannot be assessed.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: not performed, intubated; supine 124/78, HR 88 (followup_outputs[11] request_orthostatic_blood_pressure). Why: rule 3: intubated and sedated; the library reports a standing test.
- `perform_clinical_assessment {assessment_type: cognitive_screen}`: not testable, sedated (followup_outputs[12] request_cognitive_screen). Why: rule 3: sedated and intubated; the library reports MoCA 28/30.
- `order_specialized_test {test_type: neuropsych_battery}`: not performed, sedated (followup_outputs[13] request_neuropsych_battery). Why: rule 3: sedated and intubated; the library reports all domains in the average range.
- `perform_clinical_assessment {assessment_type: functional_neuro_signs}`: not assessable, sedated (followup_outputs[14] request_functional_neuro_signs). Why: rule 3: sedated and intubated; the library reports a full examination of positive signs.
- Case fallback replaced, `fallback_tool_outputs.eeg`: diffuse slowing with excess frontal beta, consistent with sedation, without epileptiform discharges, in place of a normal awake EEG. Why: rule 3: intubated and sedated with midazolam; the case fallback reported a normal awake and drowsy EEG with a 9-10 Hz posterior rhythm.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
