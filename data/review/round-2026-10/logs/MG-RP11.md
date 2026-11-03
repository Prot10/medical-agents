# MG-RP11
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MG) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. July 2026 tool guidance (Reviewer 2) applied through the plan: fixed serology order, RNS technique, SFEMG only when RNS is normal, mediastinal imaging in every case, no CSF. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.cranial_nerves`, `patient.physical_exam.neurological` | The ice pack result (3-4 mm improvement, "a positive result") was in the HPI and exam while the ice pack test is a scored criterion; the HPI also said the mass was attributed to lymphoma "rather than thymoma" and that "the connection to an underlying neuromuscular process was not immediately made" (names the answer). | FIXED: ice pack results removed from the patient block; HPI keeps that the team considered lymphoma or a germ cell tumour. "SLURP test" (not a recognised bedside test name) reworded as fatigable palatal elevation on sustained phonation. |
| B | major | `initial_tool_outputs.mri`, `initial_tool_outputs.body_imaging` | A brain and orbit MRI reported the anterior mediastinum "partially visualized" (anatomically impossible), and the CT indication cited it. | FIXED: MRI impression limited to brain, brainstem and orbits; CT indication is the chest radiograph opacity with ptosis and ophthalmoparesis. CT impression numbered; "clinical correlation with neuromuscular findings" removed (plan B/style guide); measurements filled; region "chest and mediastinum" so a `chest_CT` order gets the same study. |
| A | major | `initial_tool_outputs.labs`, `followup_outputs` `request_achr_musk_lrp4_antibodies` | Serology behind a TSH stub (plan H6); TSH "Within reference range" without units; AChR reference <0.4 (one lab) with MuSK <0.4; blocking antibody in nmol/L (plan L). | FIXED: initial labs hold AChR binding 12.4 nmol/L (<=0.02), blocking 62% (<=15%), MuSK <0.02 nmol/L, TSH 2.1 mIU/L, free T4 15.2 pmol/L; follow-up deleted. |
| D | major | `followup_outputs` respiratory_function (two) | First report called NIF -38 "adequate" and FVC 78% "adequate" (plan L); second was an unreachable stub repeating the expected evidence (plan H2, I); no weight. | FIXED: one report: FVC 3.1 L (78%, 37.8 mL/kg), MIP -38 (L), MEP 64 (L), single-breath count 22, weak cough; stub deleted. Weight 82 kg, height 176 cm added to `physical_exam.general` (BMI 26.5 as stored). |
| D | major | `followup_outputs` ice pack | Stub whose findings were the expected evidence (plan I). | FIXED: MRD1 right -1 to 2.5 mm, left 0 to 3 mm after 3 minutes. |
| C | minor | `followup_outputs` RNS, SFEMG | RNS indication "pre-operative assessment for thymectomy" (management in a report); no technique, facilitation or NCS. SFEMG without fibre-pair count. | FIXED: RNS technique, 20/17/12% decrements, no post-exercise facilitation, normal NCS; SFEMG 16 of 20 pairs with increased jitter, 22% blocking. |
| D | major | `followup_outputs` literature, drug check | Literature follow-up with a patient-oriented summary and anti-titin claims absent from the case (plan B); generic pyridostigmine drug check in a man who takes no medicines (plan C, 3.2), `proposed` a trigger slug. | FIXED: both deleted. One initial literature output in report voice (Sanders 2016 / Narayanaswami 2021, Wolfe 2016), any-query safe; drug check criterion deleted. |
| A | major | `ground_truth.action_criteria` | Template criteria (labs with MuSK and LRP4, SFEMG recommended though RNS is diagnostic, literature and drug check required, labels equal rationales, `[Wolfe_2016]` everywhere). | FIXED: respiratory function required and first (breathless, plan 3.5 RP11); labs `["anti_AChR","TSH"]` (or `thyroid`) required; RNS required; ice pack recommended; mediastinum or chest CT with contrast required; SFEMG optional; literature optional `{}`. |
| A | minor | `sequence_constraints`, `stop_rule` | `labs -> RNS` constraint with an SFEMG reason; max 0 with literature and drug check required. | FIXED: `RNS -> SFEMG` soft (plan 3.3); stop rule respiratory, labs, RNS, CT; max 2. |
| C | major | `ground_truth.assessment` | Musts included a test ("Confirm AChR antibody positivity") and vague items; template prohibitions with telithromycin and a "pyridostigmine bridge". | FIXED: thymectomy with complete resection, WHO and Masaoka-Koga staging; pre-operative IVIG 2 g/kg or PLEX (respiratory muscle weakness and palatal fatigue, Sanders 2016); pyridostigmine titration; serial respiratory monitoring with 20/30/40 escalation; anaesthetic plan; low-dose prednisone and azathioprine after TPMT if needed. Prohibitions: canonical drug and steroid texts; no chemotherapy for presumed lymphoma or germ cell tumour without tissue. |
| C | major | `ground_truth.differential` | Thymic carcinoma moderate although the CT is typical of thymoma (plan RP11); LEMS "smoker risk" in a non-smoker; brainstem "no MRI findings"; CPEO and thyroid eye disease raised by red herrings but absent. | FIXED: thymic carcinoma low; lymphoma, germ cell tumour, CPEO (new), thyroid eye disease (new), LEMS and brainstem lesion very_low, each with the excluding data. |
| E | minor | `key_clinical_evidence`, `red_herrings` | Template statements (anti-titin "non-negotiable", telithromycin, "all confirmed MG"); red herrings with empty paths citing anti-titin and an orbital MRI that is not scored. | FIXED: case-specific evidence; red herring paths filled; anti-titin removed. |
| C | minor | `fallback_tool_outputs.advanced_imaging`, `metadata.fallback_tool_kinds.advanced_imaging` | FDG-PET fallback "No abnormality identified" in a patient with a 4.4 cm thymoma. | FIXED: FDG-PET fallback shows moderate uptake in the mass (SUVmax 4.2) without nodal or distant disease; kind "abnormal_consistent". FDG-PET stays a waste avoided action. |
| D | minor | `fallback_tool_outputs.ct`, avoided action rationales, `patient` extra keys, `medications` | Head CT fallback "does not address the question" (plan F); `[Wolfe_2016]` on every waste item; invisible duplicate keys; a "None" medication row. | FIXED: plain head CT text; case rationales, citations cleared; ethnicity moved to `demographics`, duplicates dropped; medications list empty (HPI: no medicines). |

## Changes, in one paragraph a physician can read before re-reviewing

A 68-year-old man who takes no medicines has five months of bilateral complete ptosis, ophthalmoparesis, fatigable palatal elevation and breathlessness on one flight of stairs, with an anterior mediastinal opacity on the chest radiograph. The ice pack result has been taken out of the history so the test is ordered and scored. The pathway: respiratory function first (required; MIP -38 and MEP 64 reduced, weak cough, FVC 78% predicted, 37.8 mL/kg; no longer called adequate), AChR antibody and thyroid function in one initial panel (required; AChR 12.4 nmol/L, blocking 62%, MuSK negative), RNS (required; facial and trapezius decrement without facilitation), ice pack test (recommended; real MRD1 values), contrast CT of the mediastinum (required; 4.4 cm thymoma-like mass without invasion), SFEMG and literature optional. The drug check is gone (no medicines). Musts: thymectomy for the thymoma with staging, pre-operative IVIG or plasma exchange because of respiratory muscle weakness, pyridostigmine, serial respiratory monitoring with escalation thresholds, an MG-aware anaesthetic plan. Thymic carcinoma is now low; CPEO and thyroid eye disease are listed and excluded. The impossible "mediastinum seen on brain MRI" sentence is gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[Jacob_2025]`, `[Narayanaswami_2021]`, `[Lawn_2001]` (plan 5.1); cited by name in rationales until they exist.
- Synonyms (plan 5.3): "ocular myasthenia gravis" is accepted for this generalized case.
- ICD (plan 5.2): `icd_codes[0]` is G70.01 (with exacerbation) for a stable new presentation; left unchanged pending Andrea's approval of the batch reorder.

## Open questions for Andrea (judgment calls you could not settle)

- None that need information only Andrea has. Decision taken: respiratory function is required and ordered first because he is breathless on exertion with palatal fatigue (plan 3.5 RP11).

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the plan (RP11 entry) and the whole final case. Checked: no reviewer notes exist; every FIXED own finding is in the file (ice pack result out of the patient block, serology in the initial labs with one laboratory and blocking in %, one respiratory report with MIP -38 flagged reduced, real MRD1 values, RNS and SFEMG with technique and counts, drug check removed, medications empty, FDG-PET fallback consistent with the mass, MRI impression limited to brain and orbits). Arithmetic: FVC 3.1 L / 82 kg = 37.8 mL/kg, BMI 82/1.76^2 = 26.5, MRD1 -1 to 2.5 and 0 to 3 mm match 3.5 and 3 mm. Tiers and stop rule follow plan 3.5 (respiratory required and first). MGFA IIb fits palatal and respiratory weakness with normal limbs.

Found and fixed: C minor, `initial_tool_outputs.body_imaging` (narrative and impression) ended "Tissue characterization recommended". For a well-defined, non-invasive anterior mediastinal mass typical of thymoma in AChR-positive MG, upfront biopsy is avoided (capsular breach and seeding) and resection is both diagnostic and therapeutic, which is what the thymectomy must and the chemotherapy prohibition say; the recommendation contradicted them and was removed. E minor, `metadata.difficulty_rationale` (5 required, 0 red herrings) updated to 4 required, 3 red herrings.

Re-ran `perfect_agent.py MG-RP11 -v` (pass), `case_io.py check` (clean for the case) and the case guards (pass).

## Condition audit (MG auditor, 24 Oct 2026)

- fallback_tool_outputs.echo.echo_type set to TTE. FIXED.
  Why: the discriminator guard (PATTERNS.md section 5) requires an exact vocabulary value on every case fallback; an empty echo_type answered every echo variant. The RS11-RS16 verifiers fixed this only in their own cases.
- sequence constraint added: action-1-interpret-labs -> action-3-order-specialized-test (soft). FIXED.
  Why: plan MG.md 3.3 sets soft labs -> SFEMG and RNS -> SFEMG wherever an SFEMG criterion exists; these were missing here and present in the sibling cases.
- action-1-interpret-labs.citations: [Sanders_2016] (management guidance) -> [Punga_2022] (antibody biomarkers), plan 1.1. FIXED.
  Why: plan 1.1 reserves [Sanders_2016] for management; antibody testing cites the biomarker key [Punga_2022].
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.

## Close-out (24 Oct 2026)

- `ground_truth.diagnosis.icd_codes[0]` G70.01 -> G70.00. ICD-10-CM G70.01 is myasthenia gravis with (acute) exacerbation, including crisis; this is a new or stable presentation, not an exacerbation. G70.01 stays accepted as a secondary code (plans/MG-decisions.md, Q2).
- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG']; icd_codes = ['G70.00', 'G70.0', 'G70.01']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 87.8 -> 82 kg, height 182 -> 176 cm, BMI 26.5 -> 26.5 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 82 kg, height 176 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 60, ECOG 2 (requires occasional assistance; cares for most needs) (fallback_tool_outputs.clinical_assessment). Why: rule 1: the library reports Karnofsky 100 / ECOG 0 (no evidence of disease, working); rule 3: retired, complete bilateral ptosis covering the visual axis and exertional dyspnoea.
- `order_specialized_test {test_type: emg_ncs}`: normal nerve conductions and needle EMG, stating that neuromuscular transmission was not assessed (fallback_tool_outputs.specialized_test). Why: rule 1: the library report concludes there is no neuromuscular junction disorder, which routine conductions and needle EMG without repetitive stimulation cannot assess and which is not true here; the stored RNS study reports normal nerve conductions, which this report keeps.
- `interpret_labs {panels: [clustered_AChR_cell_based]}`: clustered AChR antibody (cell-based assay) positive (fallback_tool_outputs.labs['clustered_AChR_cell_based']). Why: rule 1: AChR-antibody-positive myasthenia (stored AChR binding antibody 12.4 nmol/L); a cell-based clustered AChR assay is positive when the binding assay is.
- `order_body_imaging {study: mediastinum_MRI}`: 4.4 cm solid anterior mediastinal mass without invasion, thymoma most likely (fallback_tool_outputs.body_imaging). Why: rule 3: the stored CT shows a 4.4 cm anterior mediastinal mass most consistent with thymoma; the library reports an involuted thymus.
- `order_advanced_imaging {modality: whole_body_FDG_PET}`: moderately FDG-avid 4.4 cm anterior mediastinal mass, no nodal or distant disease (followup_outputs[4] request_whole_body_fdg_pet). Why: rule 3: stored 4.4 cm anterior mediastinal mass on CT and the case's FDG-PET report (SUVmax 4.2); the library whole-body PET reports no lesion.
- `order_body_imaging {study: chest_xray}`: oval anterior mediastinal mass over the right heart border (followup_outputs[5] request_chest_xray). Why: rule 3: the emergency radiograph described in the history shows an oval radio-opaque lesion adjacent to the anterior mediastinum; the library reports a normal radiograph.
- `interpret_labs {panels: [ABG]}`: pO2 76 mmHg on room air, normal pH and pCO2 (fallback_tool_outputs.labs['ABG']). Why: rule 3: SpO2 95% on room air with decreased right basal breath sounds and reduced mouth pressures; the library reports pO2 92 mmHg.
- `order_specialized_test {test_type: speech_language_evaluation}`: fatigable hypernasality after 2 minutes; language normal (followup_outputs[6] request_speech_language_evaluation). Why: rule 3: the library reports no dysarthria; the examination documents palatal elevation that fatigues on sustained phonation.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
