# GBS-RS14
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 682b32b6-3e9e-4445-a841-7e6e80c4d080 | FIXED | The head CT follow-up (`order_ct_scan`, `request_head_ct`) is deleted. Head CT is added as waste (`avoid-waste-4-order-ct-scan`) with a case reason: alert, normal cranial nerves, no head injury. |
| 261fe3e8-852a-437b-8501-ffefd465163e | FIXED | Option chosen: remove the trigger requirement (plan C10/RS14). `action-1-interpret-labs` has the canonical label, args (`CBC`, `CMP`, `CK`) and expected_evidence, with no leukocytosis, inflammatory markers, ganglioside or trigger-identification text. The lab report now holds real CBC values (in place of the summary row "CBC: Within reference range" with its leaky significance), a full CMP with albumin, and CK. The antecedent is the pneumonia history (KCE 2 with the canonical antecedent pearl). |
| 682d7003-ed74-4dfd-95e5-b48a7d770687 | FIXED | `ground_truth.red_herrings[0]` is the influenza vaccine given 4 days ago, after weakness began 7 days ago, with the pneumonia as the likely antecedent (plan RS14 text). KCE 3 states the timing. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | The last sentence summarised the exam and resolved the diagnosis ("absent reflexes ... are the critical finding pointing to an acute polyradiculoneuropathy rather than a myelopathy or a functional cause") (C7). | FIXED: deleted; the exam fields carry the findings. |
| D | major | `patient.neurological_exam.additional` | Bedside spirometry (FVC 2.6 L, 70%, single breath count 28, "adequate but warrants serial monitoring") leaked the a4 result. The rest duplicated the HPI (C1/C7). | FIXED: field set to null. |
| A | minor | `patient.physical_exam` | No weight. | FIXED: "Weight 58 kg, height 163 cm" (BMI 21.8 agrees); injection site and chest. |
| E | minor | `patient.neurological_exam` reflexes, gait, cranial nerves | Em dashes and an editorial "Global areflexia" heading. | FIXED: plain findings, same content. |
| C | major | respiratory follow-up | "~70% predicted" with no weight, MIP or MEP. SpO2 was reported as a respiratory-function result (C1). | FIXED: canonical format: FVC 2.6 L (70% predicted; 45 mL/kg at 58 kg) L, MIP -54 L, MEP 66 L, single breath count 28 L, cough effective. No ICU trigger. |
| B/C | major | `initial_tool_outputs.specialized_test` | The peroneal conduction block was placed "at the fibular head", a compression site that does not support AIDP. The sural finding contradicted itself ("reduced SNAP ... sural-sparing pattern"). Median and ulnar had no values, there was no needle EMG, and the pattern field said "meeting electrodiagnostic criteria for AIDP". | FIXED: conduction block in the ankle-to-below-fibular-head segment. Sural normal (15 uV) with reduced median and ulnar SNAPs (sural sparing). Values and limits for median and ulnar motor added. Needle EMG without denervation. Hedged impression; `test_type` "emg_ncs". |
| C | minor | `initial_tool_outputs.labs` | HIV carried the leaky clinical_significance (C10). No platelets, albumin, calcium or CK. | FIXED: HIV Ag/Ab non-reactive with null significance. Full CBC, CMP (glucose 88, consistent with CSF ratio 0.70) and CK 104 added. Lead and urine toxicology kept. |
| C | minor | CSF follow-up | Em dash; interpretation without a close. | FIXED: report voice; values unchanged. |
| C | minor | telemetry follow-up | 72 h (C12). | FIXED: first 24 h with blood pressure range; a8 expected_evidence canonical. |
| A | major | `followup_outputs` | Ganglioside follow-up in typical GBS (C2). Empty literature and DDI placeholders (C9). | FIXED: deleted. |
| D | major | literature | Echoed a5's expected_evidence (C11). | FIXED: canonical general output; a5 optional and last. |
| C | major | criteria, sequence, stop rule | Template criteria. a5 and a6 were required with no medications. Template constraints. Stop rule included literature and DDI with max 0. | FIXED: plan 3.1 order (NCS, CSF, labs, respiratory, telemetry, ECG, optional DDI, optional literature). DDI decision: no medications, a6 optional. Constraints removed. Stop rule: the five required criteria, max 3. a7 expected_evidence describes this ECG. |
| C | major | `ground_truth.assessment` | "Initiate IVIG / plasma exchange" had no indication or dose. "Standard GBS workup as outlined" is not a recommendation. Non-canonical steroid prohibition (C8). | FIXED: monitored bed with named ICU triggers (20 mL/kg is about 1.2 L at 58 kg). IVIg 2 g/kg (about 23 g/day at 58 kg) now, because she cannot walk unaided at day 7, with PE as the alternative. Telemetry. LMWH prophylaxis. Prohibitions: canonical steroid text, renal function before IVIg. |
| C | major | `ground_truth.differential` | Acute-onset CIDP was moderate. The other mimics had generic reasons ("MRI excludes", although no MRI is done) (C5). | FIXED: CIDP low (reassess at 8 weeks). Transverse myelitis, cord compression, Lyme, tick paralysis and toxic neuropathy very_low, each with the case findings (the lead level and toxicology are now used). |
| C | minor | `key_clinical_evidence`, `metadata` | One pearl ("Brighton level 1 ... all supportive features" before the plateau). Rationale said 0 red herrings. | FIXED: four pearls (Brighton level 1 once plateau within 4 weeks, antecedent, vaccine timing, treatment indication); metadata updated. Label unchanged. |

## Changes, in one paragraph a physician can read before re-reviewing
GBS-RS14 stays a classic AIDP in a 19-year-old woman, a week after onset and 3 weeks after a pneumonia. She cannot walk unaided. The influenza vaccine given 4 days ago, three days after the weakness began, is now the red herring with that timing. The patient block no longer leaks the spirometry or a summary of the diagnosis, and it records weight 58 kg. The head CT, ganglioside panel and placeholder steps are gone. The labs are real values, with no template significance sentences. The NCS shows demyelination with conduction block in a non-compression segment and true sural sparing. The respiratory step reports FVC 2.6 L (70%, 45 mL/kg), MIP -54 and MEP 66, with no ICU trigger. The musts are admission to a monitored bed with named ICU triggers, IVIg 2 g/kg now (PE equivalent), telemetry and LMWH. The differential is lowered with case-specific reasons.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 5 (weight field) and 10 (respiratory-report guard).

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case.
- Note 682b32b6: FIXED holds. No head CT follow-up remains; head CT is waste with a case reason.
- Note 261fe3e8: FIXED holds. a1 is canonical; labs are real normal values with no leukocytosis or trigger serology; the pneumonia is history (KCE 2).
- Note 682d7003: FIXED holds. red_herrings[0] and KCE 3 state that the vaccine (4 days ago) followed onset (7 days ago).
- Cross-checks clean: FVC 2.6 L = 45 mL/kg at 58 kg; IVIg 23 g/day; BMI 21.8 agrees; GBS disability score 3 (walks only with assistance) matches the IVIg must; sural sparing and non-compression conduction block are consistent across findings and impression.
- Found and fixed (minor):
  - E: `patient.clinical_history.family_history[0]` kept an em dash; replaced with a semicolon.
  - D: `patient.chief_complaint` contained the exam finding "with global areflexia"; rewritten as the presenting complaint ("... ascending limb weakness with tingling in the feet and hands, three weeks after a pneumonia").
  - B: the CSF follow-up reported "No growth at 3 days" (special_tests.Culture and interpretation), a result not available at the admission assessment; now "No growth to date".
- perfect_agent.py GBS-RS14 -v passes; case_io.py check clean for the case.


## Condition audit (24 Oct 2026)
Condition auditor, after the worker and the verifier. Changes made through case_io; `perfect_agent.py` and `case_io.py check` re-run clean for all 30 GBS cases afterwards, and `test_case_guards.py -k GBS` passes.
- E, minor: `fallback_tool_outputs.drug_interactions.general.proposed` read "(agent not specified on this case's pathway)", an engineering note served to any off-pathway interaction check (PATTERNS 5). Now "Medication list review", as in S01-S03 and RS18.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels and the three AIDP labels (its NCS is demyelinating); "acute motor axonal neuropathy", "AMAN" and "miller fisher syndrome" are no longer accepted (wrong subtype or variant for this case).
- Escalation must: "MIP becomes weaker than -30 cmH2O" -> "-40 cmH2O" (EAN/PNS 2023 MIP <40).
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- follow-up `request_cardiac_monitoring`: `monitor_type` "Continuous inpatient telemetry" -> `telemetry`.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-6-check-drug-interactions` rationale: "She takes no medicines, so the check cannot change management (ROUND_POLICY ruling 6)." -> "She takes no medicines, so the check cannot change management."

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 58.6 -> 58 kg, height 164 -> 163 cm, BMI 21.8 -> 21.8 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 58 kg, height 163 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 50, ECOG 3 (fallback_tool_outputs.clinical_assessment). Why: rule 1: the library reports Karnofsky 100 / ECOG 0 and a working patient; she cannot walk without assistance and cannot rise from a chair without using her arms.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: severely impaired gait and balance: steppage gait with support (berg 20/56); timed tests not completed (followup_outputs[3] request_gait_and_balance_timed). Why: rule 1: the library reports a normal timed gait and balance assessment; she walks only with support with a bilateral steppage gait.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no tremor or rigidity; motor items limited by weakness, response not assessable (followup_outputs[4] request_levodopa_challenge). Why: rule 1: the library describes a normal motor examination, gait and postural reflexes; symmetric flaccid weakness and a steppage gait.
- `order_body_imaging {study: spine_MRI}`: smooth enhancement of the cauda equina roots, ventral more than dorsal; normal cord (fallback_tool_outputs.body_imaging). Why: rule 1: smooth enhancement of the cauda equina and ventral roots is seen in most patients with this polyradiculoneuropathy (Gorson 1996; Byun 1998), while the library reads the roots as normal.
- `order_body_imaging {study: peripheral_nerve_MRI}`: smooth enhancement and mild T2 hyperintensity of the lumbosacral roots, no enlargement (followup_outputs[5] request_peripheral_nerve_mri). Why: rule 1 and 3: the library reads the nerve roots as normal; root enhancement as on the spine MRI of this case.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: active standing not performed (cannot stand unassisted); supine BP 122/78 mmHg, HR 92 bpm; sitting BP 118/78 mmHg, HR 100 bpm (followup_outputs[6] request_orthostatic_blood_pressure). Why: rule 3: she cannot stand unassisted; the library reports 3 minutes of symptom-free standing at a supine heart rate of 68.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
