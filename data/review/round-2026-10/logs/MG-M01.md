# MG-M01
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MG) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance for myasthenia_gravis (fixed serology order, RNS technique, SFEMG when RNS is negative, mediastinal imaging in every case, no CSF, no paraneoplastic panel), applied through the condition plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.specialized_test`, `followup_outputs` (`request_repetitive_nerve_stimulation`) | Plan H1: the initial 3 Hz RNS report (the diagnostic decrement) was shadowed by an RNS follow-up holding a 50 Hz study; the RNS criterion received the 50 Hz report, not the decrement. | FIXED: one RNS report (initial): technique (3 Hz, warmed, no pyridostigmine), nasalis 12%, deltoid 11%, trapezius 9%, 10 s post-exercise increment 6% with repair and exhaustion, normal NCS, needle EMG with unstable MUPs; impression in numbered RNS voice. The 50 Hz follow-up deleted (painful study, no added question). Recommended actions (antibodies, CT chest, SFEMG) removed: cross-modality. |
| B | major | `initial_tool_outputs.ct`, `followup_outputs` (`request_thymectomy_evaluation`) | Plan H3: the chest CT was stored under the head CT tool and duplicated as a body-imaging follow-up with surgical-approach text ("VATS or median sternotomy feasible") and a referral. | FIXED: one `initial_tool_outputs.body_imaging` report (region "mediastinum chest", CT, contrast true) so mediastinum_CT and chest_CT orders both receive it; management text removed; impression "most consistent with a thymoma; thymic carcinoma less likely". `initial_tool_outputs.ct` null; `fallback_tool_outputs.ct` plain normal head CT (class F). New follow-up `request_mediastinum_mri` (MRI, contrast) with the same mass, so a mediastinal MRI order does not receive a contradictory library normal. |
| D | major | `initial_tool_outputs.literature_search` | Leak guard failure (class B): the output's summary and finding were the literature criterion's `expected_evidence`. | FIXED: query re-keyed; canonical plan text with three correctly cited results (Sanders 2016, Narayanaswami 2021, Wolfe 2016); nothing patient-specific. Guard passes. |
| A | major | `followup_outputs` (`request_musk_antibodies`) | Plan H9: MuSK, LRP4 and VGCC follow-up in an AChR-positive case (not indicated). | FIXED: deleted (MuSK negative remains in the initial panel). |
| C | major | `initial_tool_outputs.labs` | AChR binding 0.8 nmol/L with reference <0.5 called "borderline positive, equivocal" (fact 2); anti-titin row (not orderable, late onset at 52, fact 4) with "thymoma concern"; summary with causal claims. | FIXED: titin row removed; summary is a list of out-of-range values; interpretation is a pattern recital plus a hedged templated antibody comment. MuSK reference written "<0.02" as in the other rows. |
| D | major | `patient.neurological_exam.additional` | NIF -42 cmH2O in the exam while respiratory function is a criterion (class K). | FIXED: number removed; bedside picture kept. |
| D | minor | `patient.history_present_illness` | Prior TSH value 0.28 identical to the scored lab result. | FIXED: "a mildly low TSH, attributed to levothyroxine over-replacement; the dose was not changed" (prior history kept without the number); one em dash replaced. |
| B | major | `patient.physical_exam`, `followup_outputs` (`request_respiratory_function`) | Respiratory report without units, % predicted or mL/kg, no MEP, no weight in the case (fact 14). | FIXED: `physical_exam.general` "Weight 91 kg, height 178 cm" (BMI 28.7 as in demographics); report FVC 3.20 L (70% predicted, 35 mL/kg), MIP -42 cmH2O (reduced), MEP 72 cmH2O, PEF 380 L/min, ABG, single-breath count 26; flags L. |
| B | minor | `followup_outputs` (`request_emg_single_fiber`) | "All pairs abnormal except one" contradicted a range of 38-148 microseconds (all above 34); fiber density "mildly elevated" unexplained. | FIXED: muscle stated; mean MCD 62 (<=34), 15 of 20 pairs above the individual-pair limit, blocking in 6 of 20; fiber density removed. |
| A | major | `ground_truth.action_criteria` | Template criteria (class A): labs required MuSK and LRP4 in an AChR+ case; SFEMG recommended although RNS diagnostic; drug check required with a generic list including telithromycin; literature recommended; labels equal rationales; duplicate `[Wolfe_2016]`/`Wolfe_2016` citations. | FIXED: labs `["anti_AChR","TSH"]` required; RNS required; SFEMG optional; new `action-ice-pack-test` recommended (fatigable left ptosis); mediastinal imaging required with chest_CT and mediastinum_MRI alternatives; respiratory recommended; drug check optional `{}` (no medicine with an MG interaction); literature optional `{}` last. Labels, case-specific expected evidence and rationales; one citation per source; `[Wolfe_2016]` only on the mediastinal imaging criterion. |
| A | minor | `metadata.actions_withdrawn` | Ice-pack test withdrawn in August for lack of a stored result. | FIXED: result authored (`followup_outputs` `request_ice_pack_test`: left MRD1 1.0 to 3.5 mm, right 2.5 to 3.5 mm) and the withdrawal entry removed. |
| B | major | `followup_outputs` (`request_pyridostigmine_interactions`) | Wrong fact (lisinopril "bradycardic additive effect"), treatment advice ("avoid corticosteroids ... without hospitalization"), patient-specific respiratory advice, `proposed` a dosing plan. | FIXED (class C): checker voice against his list (levothyroxine, lisinopril, aspirin: none; atorvastatin: statin case reports, monitor); pyridostigmine contraindication and warnings; class list of NMJ-impairing drugs without telithromycin. |
| C | major | `ground_truth.sequence_constraints` | Shared `labs -> RNS` constraint with an SFEMG reason. | FIXED (plan 3.3): `labs -> SFEMG` and `RNS -> SFEMG`, both soft. |
| C | major | `ground_truth.stop_rule` | Literature-free but drug check required; `max_additional_actions` 0. | FIXED: labs, RNS, mediastinal imaging; max 2. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts that were tests (confirm AChR, order CT, SFEMG "given borderline RNS"); "anti-titin strongly predicts thymoma"; no steroid plan; 4-6-hourly NIF with a leaked value. | FIXED: six musts: pyridostigmine titration; thymectomy referral for the thymoma with pre-operative IVIG or PLEX for bulbar weakness (Sanders 2016); prednisone low and titrated or high dose only as inpatient, azathioprine after TPMT/NUDT15 if long term; FVC/MIP/MEP twice daily with fact 15 thresholds; swallow assessment; levothyroxine reduction with TSH recheck. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Seven shared prohibitions incl. telithromycin, the "pyridostigmine bridge" steroid line and the functional-attribution line requiring SFEMG. | FIXED (class D): canonical drug prohibition and canonical steroid prohibition; functional line dropped (no functional label in play). |
| C | minor | `ground_truth.differential[0]` | LEMS key features cited the deleted 50 Hz study and a VGCC result not in the case. | FIXED: normal baseline CMAP, 6% post-exercise increment, normal reflexes, positive AChR; likelihood very_low. |
| C | minor | `ground_truth.key_clinical_evidence` | Shared lines (titin "non-negotiable", "All confirmed MG require CT chest", telithromycin, "10% is a statistical convention ... fatigability is decisive", AChR "borderline"). | FIXED: six case-specific lines including the canonical mediastinal CT sentence. |
| C | minor | `ground_truth.red_herrings[1]` | Correct interpretation said fatigability "mandates progression to SFEMG". | FIXED: two muscles exceed 10% and AChR is positive; SFEMG not needed. Red herring 0 reworded ("suppressed" to low). |
| C | minor | `ground_truth.avoided_actions[*]` | `[Wolfe_2016]` cited for EEG, CSF, PET, MRI, echo, Holter. | FIXED: case rationales, Jacob 2025 in text, `citations` empty until CENTRAL adds the key. |
| E | minor | `patient.neurological_exam.gait` | "Mildly slow but antalgic" in a man without pain. | FIXED: "Mildly slow. No ataxia. Waddling pattern on prolonged walking." |

## Changes, in one paragraph a physician can read before re-reviewing

A 52-year-old man with fatigable asymmetric ptosis, diplopia, bulbar and proximal weakness. The work-up is now: AChR binding antibody 0.8 nmol/L (positive against <0.5) with raised blocking and modulating antibodies, MuSK negative, TSH low on levothyroxine with normal free T4 and raised anti-TPO; RNS at 3 Hz with 12% (nasalis) and 11% (deltoid) decrement, normal CMAPs and no facilitation (one report, the 50 Hz study removed); a positive ice-pack test on the left; a contrast mediastinal CT showing a 3.1 cm non-invasive anterior mediastinal mass most consistent with thymoma (moved off the head CT tool); FVC 70% predicted (35 mL/kg) with MIP -42 and MEP 72 cmH2O. SFEMG, the drug check and literature are optional. Musts: pyridostigmine titration, thymectomy referral with pre-operative IVIG or PLEX for bulbar weakness, prednisone started low or high only as inpatient with azathioprine after TPMT/NUDT15 if needed, twice-daily FVC/MIP/MEP with ICU thresholds, swallow assessment, and a modest levothyroxine reduction. Titin, telithromycin and the duplicated serology follow-up are gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Criteria pack keys `[Jacob_2025]`, `[Evoli_2019]`, `[Narayanaswami_2021]`, `[Lawn_2001]` (named in rationale text here, not in `citations`); `[Punga_2022]` title correction (plan CENTRAL 1).
- `icd_codes[0]` is G70.01 ("with exacerbation") for a stable new diagnosis; G70.00 fits (plan CENTRAL 2; left unchanged).
- Synonym group accepts "ocular myasthenia gravis" for this generalized case (plan CENTRAL 3).

## Open questions for Andrea (judgment calls you could not settle)

None.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the plan (M01 entry, classes A-N, 3.5 generalized AChR+ table), the diff against the pre-round version and the whole final case. No notes file exists for MG, so no note id can be missing. Every FIXED finding is in the file: one RNS report (initial, 3 Hz, nasalis 12%, deltoid 11%, no facilitation), the 50 Hz follow-up and MuSK/LRP4/VGCC follow-up gone, chest CT moved to `initial_tool_outputs.body_imaging` (CT, region "mediastinum chest", contrast true) with a consistent mediastinal MRI follow-up, titin row gone, NIF out of the exam, literature in canonical report voice (leak guard passes), drug check in checker voice without telithromycin, stop rule labs/RNS/imaging with max 2, `[Wolfe_2016]` only on the mediastinal criterion. Arithmetic: 3.20 L / 91 kg = 35 mL/kg; BMI 91/1.78^2 = 28.7; MRD1 changes match. Musts agree with the inpatient setting, the thymoma (thymectomy whatever the severity, pre-operative IVIG or PLEX for bulbar weakness) and his medicines; the differential is the assessment-time view. Discriminator check (not yet enforced for MG) passes for every routed output.

Found and changed: `metadata.difficulty_rationale` still said "4 required tools" after the rebuild left three required criteria; corrected to 3.

Noted, not changed: the HPI keeps "a mildly low TSH" from a primary care test without the number. TSH is part of the scored labs criterion, but the prior result is the red herring's background, not the diagnosis or its decisive test, and the scored first labs order is still needed for AChR; acceptable history.

Checks after the change: `perfect_agent.py MG-M01 -v` passes, `case_io.py check` clean for the case, case guards pass.

## Condition audit (MG auditor, 24 Oct 2026)

- patient.neurological_exam.cranial_nerves: levator excursion replaced by MRD1 (left 1.0, right 2.5 mm), the measure the ice-pack report uses as its baseline. FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.

## Close-out (24 Oct 2026)

- `ground_truth.diagnosis.icd_codes[0]` G70.01 -> G70.00. ICD-10-CM G70.01 is myasthenia gravis with (acute) exacerbation, including crisis; this is a new or stable presentation, not an exacerbation. G70.01 stays accepted as a secondary code (plans/MG-decisions.md, Q2).
- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG']; icd_codes = ['G70.00', 'G70.0', 'G70.01']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-5-search-medical-literature` label: "Literature on MG work-up and thymectomy (optional)" -> "Literature on MG work-up and thymectomy"

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 82 -> 91 kg, height 169 -> 178 cm, BMI 28.7 -> 28.7 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 91 kg, height 178 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 70, ECOG 2 (cares for self; unable to carry on normal work) (fallback_tool_outputs.clinical_assessment). Why: rule 1: the library reports Karnofsky 100 / ECOG 0 (no evidence of disease, working); rule 3: inpatient with generalized bulbar and limb weakness and exertional dyspnoea.
- `order_specialized_test {test_type: emg_ncs}`: normal nerve conductions and needle EMG, stating that neuromuscular transmission was not assessed (fallback_tool_outputs.specialized_test). Why: rule 1: the library report concludes there is no neuromuscular junction disorder, which routine conductions and needle EMG without repetitive stimulation cannot assess and which is not true here; the stored RNS study reports normal nerve conductions, which this report keeps.
- `interpret_labs {panels: [clustered_AChR_cell_based]}`: clustered AChR antibody (cell-based assay) positive (fallback_tool_outputs.labs['clustered_AChR_cell_based']). Why: rule 1: AChR-antibody-positive myasthenia (stored AChR binding antibody 0.8 nmol/L); a cell-based clustered AChR assay is positive when the binding assay is.
- `order_advanced_imaging {modality: whole_body_FDG_PET}`: moderately FDG-avid 3.1 cm anterior mediastinal mass, no nodal, pleural or distant disease (fallback_tool_outputs.advanced_imaging). Why: rule 3: the stored CT and mediastinal MRI show a 3.1 cm anterior mediastinal mass most consistent with thymoma; the library reports no mediastinal lesion.
- `interpret_labs {panels: [anti_thyroglobulin]}`: anti-thyroglobulin antibody 210 IU/mL (elevated) (fallback_tool_outputs.labs['anti_thyroglobulin']). Why: rule 2: Hashimoto thyroiditis on levothyroxine (anti-TPO 380 IU/mL stored); the library reports a normal anti-thyroglobulin antibody.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: mildly slow TUG 11.8 s and gait speed 1.02 m/s, waddling on repeated walking, balance preserved (followup_outputs[5] request_gait_and_balance_timed). Why: rule 3: the library reports a normal timed gait (TUG 9.1 s, Berg 56/56); the examination documents hip flexors 4/5 and a mildly slow gait with waddling on prolonged walking.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no parkinsonian signs and no levodopa response; mild gait and chair-rise points from proximal weakness (followup_outputs[6] request_levodopa_challenge). Why: rule 3: the library levodopa challenge describes normal gait, arm swing and postural reflexes, while the examination documents a mildly slow, waddling gait with hip flexor weakness.
- `order_specialized_test {test_type: speech_language_evaluation}`: fatigable flaccid dysarthria with hypernasality after 2 minutes of speech; language normal (followup_outputs[7] request_speech_language_evaluation). Why: rule 3: the library reports no dysarthria; the examination documents dysarthric, nasal speech after prolonged speaking.
- `interpret_labs {panels: [ABG]}`: pH 7.43, pCO2 40, pO2 88 mmHg on room air, normal (fallback_tool_outputs.labs['ABG']). Why: rule 3: the stored respiratory function report gives this room-air gas (pH 7.43, PaCO2 40, PaO2 88 mmHg); the library reports pH 7.40, pCO2 40, pO2 92 mmHg.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
