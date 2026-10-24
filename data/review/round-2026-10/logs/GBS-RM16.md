# GBS-RM16
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 33eaec73-0153-4ec7-8201-655a987b4078 | FIXED | Weight 76 kg, height 177 cm (`patient.physical_exam.general`, BMI 24.2). `followup_outputs[2]` canonical: FVC 2.2 L (55% of 4.0 L; 29 mL/kg) L, MIP -26 L, MEP 42 L, change from 2.4 L / -30 six hours earlier (the former patient-block values), cough weak; "All values within normal limits" removed. Musts 1-2: ICU-level monitoring now (FVC <60%, MIP weaker than -30, weak cough, autonomic lability) and elective-intubation triggers (FVC <20 mL/kg = 1.5 L, MEP <40, worsening bulbar function). Spirometry removed from `neurological_exam.additional`. |
| 8241358d-e1bf-4e8a-8aa1-745e10dfe385 | FIXED | Red herrings added: (1) the triple CMV/EBV/HSV IgM, now history (serology sent by his primary care physician 3 days ago, `patient.history_present_illness`) and deleted from the current labs, resolved as cross-reactivity or polyclonal activation with acellular CSF and negative CMV/HSV PCR; (2) the apparent T4 level, resolved by the patchy border on detailed testing and the contrast spine MRI. Viral meningoencephalitis added to the differential (very_low); pearl 2 carries the serology point. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `followup_outputs[0]` (CSF) | Report spanned two LPs (day 1 and a day-14 repeat in the future) with arrows (C7). | FIXED: one LP at the encounter (day 10): 4 cells/mm3, protein 78 mg/dL, glucose 62, CMV and HSV PCR not detected. |
| B | major | `patient` | Diplopia and blurred vision in the HPI and chief complaint, but the exam recorded no eye movement finding, the differential stated "absence of ophthalmoplegia", and the plan treats the case as typical sensorimotor GBS without ganglioside testing. | FIXED: diplopia and blurred vision removed; exam states full eye movements, no nystagmus, pupils equal. |
| C | major | `patient.neurological_exam.sensory`, `coordination`, `additional` | "Sensory ataxia" without any large-fibre sensory loss documented (only temperature, a small-fibre modality); `additional` called the temperature pattern "large-fiber". | FIXED: vibration and joint position loss documented, ataxia worse with eyes closed; the apparent T4 level is stated once as patchy on detailed testing; `additional` removed. |
| D | major | `patient.history_present_illness` | "prompted emergent MRI spine" and "raised concern for a primary viral meningoencephalitis" (scored study and editorial, C7). | FIXED: removed; antecedent URI dated 3 weeks ago (was 2 days before onset), macrolide course stated as completed. |
| C | major | `followup_outputs[1]` (spine MRI) | `contrast: false` while reporting gadolinium enhancement; no criterion although a sensory level is a red flag. | FIXED: `contrast: true`, trigger `request_spine_mri_contrast`, em dashes removed; new recommended `action-10-order-body-imaging` (`spine_MRI`, contrast). |
| C | major | `followup_outputs[3]` (telemetry) | 96-hour report with labetalol treatment (C12, ruling 4). | FIXED: first 24 h: hypertensive episode 178/104 settling, nocturnal sinus bradycardia 48 bpm, tachycardia to 118; no treatment. |
| C | major | `followup_outputs[4]` (DDI) | Prescriptive (amoxicillin, avoid macrolide class, "continue clarithromycin") for a completed course. | FIXED: category-level: no current interacting medicine, QT caution for macrolides/fluoroquinolones (relative caution), IVIg SmPC risks; a6 optional. |
| D | minor | `initial_tool_outputs.specialized_test` | "with conduction block" claimed with no conduction-block data; "mixed"; "AIDP" in the pattern field; no needle EMG. | FIXED: severe demyelinating sensorimotor polyradiculoneuropathy with facial nerve involvement; blink reflex stated plainly; needle EMG added. |
| C | major | `initial_tool_outputs.labs` | Viral serology panel and HIV with the leaky sentence; no CMP or CK. | FIXED: removed; CMP and CK added (normal); CRP 18.2, ESR 54 kept. |
| A | major | `followup_outputs` | Anti-GM1/GD1b follow-up (C2) and empty literature placeholder. | FIXED: deleted. |
| C | major | `ground_truth.assessment` | "Initiate IVIG / plasma exchange" without indication; ganglioside and paraneoplastic serology must. | FIXED: ICU-level, intubation plan, IVIg 2 g/kg (about 30 g/day; disability score 4, day 10; PE equivalent), telemetry with QT caution, LMWH. Prohibitions: canonical steroid, renal function, no delay for serology. |
| C | major | `ground_truth.differential` | Sensory ganglionopathy and MFS moderate after a demyelinating motor NCS and full eye movements. | FIXED: low with reasons; viral meningoencephalitis and cord lesion very_low with case reasons. |
| C | minor | `ground_truth.diagnosis.accepted[0]` | "(post-URI)" abbreviation. | FIXED: "... with sensory ataxia, after an upper respiratory infection". |
| D | major | `initial_tool_outputs.literature_search` | Scoring-key echo. | FIXED: canonical general output; a5 optional, last. |
| E | minor | `initial_tool_outputs.ecg.findings`, chief complaint, metadata | Em dashes; difficulty text named anti-GD1b. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The case is a severe demyelinating GBS with sensory ataxia and facial involvement after a URI 3 weeks earlier. The patient block now documents the large-fibre loss that makes the ataxia sensory, full eye movements (diplopia removed), and the apparent T4 temperature level as patchy on detailed testing. Two red herrings are encoded: low-titre IgM to CMV, EBV and HSV from serology done before admission (cross-reactivity, acellular CSF with negative PCR), and the apparent T4 level (normal cord on a new recommended contrast spine MRI, with root enhancement). The CSF is one LP at day 10 (4 cells, protein 78). Weight is 76 kg; FVC fell from 2.4 to 2.2 L (55%, 29 mL/kg) with MIP -26 and a weak cough, so the musts are ICU-level monitoring with an elective-intubation plan, IVIg 2 g/kg now, telemetry for the documented autonomic lability with a QT caution, and LMWH. Telemetry reports 24 hours without treatment; the interaction check is optional and category-level; ganglioside, viral serology and placeholder steps are gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 4 (`CMV_PCR` in `analyze_csf` special tests): the stored CSF report keeps its CMV PCR result, which the agent cannot order separately.

## Open questions for Andrea (judgment calls you could not settle)

- None. The diplopia was removed rather than turned into an ophthalmoparesis because the plan classes this case as typical sensorimotor GBS (no ganglioside step) and the exam never recorded an eye movement deficit.

## Verification (adversarial verifier, 24 Oct 2026)

Checked: FVC 2.2/4.0 L = 55%, 29 mL/kg at 76 kg, BMI 24.2 agrees with 177 cm, 20 mL/kg = 1.5 L, 2.4 to 2.2 L = 8% fall; ICU-level must justified (FVC <60%, MIP -26, weak cough). Both red herrings present in the case and resolved (prior triple IgM dated before admission, deleted from current labs; patchy T4 level resolved by the new recommended contrast spine MRI, `contrast: true` now matches the enhancement). CSF is a single LP at day 10. Diplopia removal is consistent with full eye movements and the plan's typical-sensorimotor class (no ganglioside step). Sensory ataxia now has large-fibre loss. Telemetry 24 h without treatment; ECG QTc 458 borderline for a man and rate 104 = vitals.
Found and fixed: the DDI output warning still prescribed management ("a non-QT-prolonging alternative is preferred if an antibiotic is needed again"), against plan C8 / section 3.2 (category-level, no management instructions). Reworded `followup_outputs[4].output.warnings[0]` to "Macrolides and fluoroquinolones prolong the QT interval; the risk is additive with a borderline QTc (458 ms) and autonomic involvement (relative caution)." The management point stays in must 4.
Checks re-run after the verifier's edits: `perfect_agent.py -v` ok (each criterion served by its intended report; labs, brain MRI and ganglioside probes confirmed by a direct MockServer probe where relevant) and `case_io.py check` clean for this case (the remaining failures name GBS-RP16 and GBS-RS16 only).


## Condition audit (24 Oct 2026)
Condition auditor, after the worker and the verifier. Changes made through case_io; `perfect_agent.py` and `case_io.py check` re-run clean for all 30 GBS cases afterwards, and `test_case_guards.py -k GBS` passes.
- B, minor: `action-7-analyze-ecg` expected_evidence was the condition template ("Sinus tachycardia or bradycardia; conduction or repolarisation abnormalities reflecting autonomic involvement") and the rationale repeated the label, while the ECG shows sinus tachycardia 104 bpm with QTc 458 ms. Rewritten to what the ECG shows, with the rationale used in RP12, RP14-RP16 (the RP12 verifier had flagged this template in this case).

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels and the three AIDP labels (its NCS is demyelinating); "acute motor axonal neuropathy", "AMAN" and "miller fisher syndrome" are no longer accepted (wrong subtype or variant for this case).
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Central vocabulary wired (24 Oct 2026)
Terms added in commit e19131d6 (`interpret_labs` `anti_GQ1b_IgG`, `anti_GT1a_IgG`, `botulinum_toxin_assay`; `analyze_csf` `CMV_PCR`), wired per plan C2/C3/C9 and GBS-decisions CENTRAL 1-3. Checks after the change: `perfect_agent.py -v` pass, `case_io.py check` clean for this case, `test_case_guards -k GBS-` 60 passed; optional criteria probed against the MockServer (served the case's own report, not a fallback).

- No case change. The stored CSF report (CMV and HSV PCR negative) is served to an `analyze_csf` call with `{special_tests: [CMV_PCR]}` (probed). No criterion added: antecedent-infection testing is not part of the work-up (plan C3; EAN/PNS 2023) and the CMV result only resolves the IgM red herring. Closes CENTRAL 4 for this case.
