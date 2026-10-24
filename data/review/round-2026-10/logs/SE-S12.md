# SE-S12
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 5daa0f16-4a86-4afc-bc36-0d89ba15c089 | FIXED | Blood cultures deleted: criterion `action-9-order-microbiology`, `initial_tool_outputs.microbiology` and the a9 entry in `stop_rule.required_before_assessment`. The patient is afebrile (37.1 C) with WBC 7.8 and has no infectious focus (plan C3). |
| 19c53320-5fe4-4264-a98f-32347a37ef93 | FIXED | The FBDS are now right face and right arm, contralateral to the left mesial temporal focus: `patient.chief_complaint`, `history_present_illness`, `neurological_exam.additional`, `.cranial_nerves`, `.motor` (mild right hand weakness between events), the EEG video correlate, `key_clinical_evidence`, the differential and the a1 expected text. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| D | blocker | `initial_tool_outputs.drug_interactions['general']` | An initial "general" drug block was served for any drug query (plan C9); the leak guard failed on this case at baseline. | FIXED: deleted. A real interaction follow-up `request_antiseizure_immunotherapy_interaction_check` replaces it (T-DDI): enzyme inducers lower corticosteroid exposure, levetiracetam and lacosamide do not interact with the immunotherapy, steroids with mycophenolate add infection risk, steroids with lisinopril, IVIG renal and thrombotic cautions. a6 optional with a factual expected text (it was a treatment plan). |
| A/C | major | `initial_tool_outputs.labs`, a2 | The labs had a template "Exclusion studies" block (plan C1). They also served the LGI1 titer and CRP for a basic panel order, so the core order revealed the answer. The a2 arguments listed nine panels, including ammonia, lactate and ABG. | FIXED: block deleted; LGI1 and CRP removed from the initial labs; full CMP with magnesium 2.0 and glucose 118; levetiracetam 32 in range. a2 is T-LABS (CBC, CMP, magnesium, AED_levels). |
| C | major | new `action-8-interpret-labs-autoimmune-panel`, follow-up `request_autoimmune_encephalitis_panel` | The serum antibody panel, which is the sensitive test for LGI1, had no criterion of its own. The follow-up mixed serum and CSF results. | FIXED: new required criterion (panels `autoimmune_encephalitis_panel`). The follow-up gives serum LGI1 1:64 (1:32 a month earlier) with CASPR2, NMDAR, GABA-B and AMPA negative, and a hedged templated interpretation. |
| C | major | a5 CSF, CSF follow-up | The CSF was required, although serum is more sensitive for LGI1 and the CSF does not change acute management. The output keys did not match the ordered `autoimmune_panel`, and there was no HSV PCR in an immunosuppressed patient. | FIXED: recommended; output has the `autoimmune_panel` key (LGI1 1:4, others negative) and `HSV_PCR` not detected; WBC 18, protein 56, glucose ratio 0.54 against serum 118. The CT-before-LP hard constraint is kept. |
| C | major | EEG follow-up `request_continuous_eeg_monitoring`, literature follow-up `request_rituximab_consideration` | A post-treatment EEG reported the effect of treatment (plan C4). A second literature output sat on top of a7 and pushed rituximab as a patient-specific step. | FIXED: both deleted. |
| D/E | major | `initial_tool_outputs.eeg`, a1 | The EEG impression stated that the record "meets SE criteria" (a conclusion). The frequency was written as "theta-alpha 8-12 Hz". The video correlate was left-sided. a1 had no `eeg_type`. | FIXED: ACNS-style report of 2-3 s left temporal (T3) 8-10 Hz runs every 60-90 s, time-locked to right face and arm dystonic posturing, with left temporal slowing. T-EEG criterion with continuous ICU and video alternatives, citing [Brophy_2012] and [ACNS_2021]. |
| D | minor | `initial_tool_outputs.ct`, MRI follow-up | The CT and MRI reports named "LGI1 encephalitis" (cross-modality synthesis). | FIXED: report voice. The CT shows a subtle left mesial temporal hypodensity. The MRI shows bilateral mesial temporal FLAIR change, left greater than right, increased since 6 months, with faint enhancement and an imaging-only differential. a3 uses the T-CT label. a4 cites [Graus_2016] in place of [Glauser_2016]. |
| C/D | major | a7 literature, follow-up `request_immunotherapy_fbds_management` | Literature was required. The output carried unsourced figures (a 60-70% remission rate, a "10-20 mg" steroid floor) and patient-specific steps. | FIXED: optional, last; T-LIT output with four general facts citing [Irani_2011], [Graus_2016] and [Glauser_2016]. |
| C | major | `assessment` | There were no doses. A carbamazepine must ("CBZ specific effect on FBDS") contradicted the enzyme-induction problem during steroid re-escalation. The taper prohibition was duplicated. "Do NOT delay LP" made an optional diagnostic test into a prohibition. | FIXED: T-MUST-BZD; IV methylprednisolone 1 g daily for 5 days, then a slower oral taper; IVIG 0.4 g/kg/day for 5 days with renal and hydration checks; continue levetiracetam and add IV lacosamide 200-400 mg if seizures persist, avoiding fosphenytoin; neuroimmunology on maintenance escalation (rituximab); T-MUST-cEEG. Prohibitions: continuing the taper, ASMs alone, enzyme-inducing ASMs with steroids (one each). The carbamazepine line is removed from the musts and from `key_clinical_evidence`. |
| C | minor | `ground_truth.differential` | The ranking did not reflect the results. HSV encephalitis in an immunosuppressed patient was missing (ruling 7). | FIXED: functional events low (time-locked EEG), other autoimmune encephalitis low (panels), subtherapeutic ASM low (level 32), HSV low (afebrile, PCR negative), movement disorder low, each stating its result. |
| B | minor | `red_herrings` | Checked against the new outputs. | No change needed: the levetiracetam level and the mycophenolate entries still hold. |
| A | minor | `fallback_tool_outputs` | `drug_interactions` "lgi1_immunotherapy", `advanced_imaging` "MRI brain" and `specialized_test` neuropsychological testing are not vocabulary values (plan C10). The ECG fallback rate of 84 did not match HR 96. | FIXED: those three nulled; ECG rate 94; `fallback_tool_kinds` updated. |
| E | minor | `avoid-waste-5-order-specialized-test` | The PSG entry carried another template's rationale. | FIXED: T-PSG. |
| A | minor | `stop_rule`, metadata | The stop rule listed literature and microbiology. The difficulty rationale cited "CBZ specific effect". | FIXED: labs, CT, EEG, MRI and autoimmune panel; max 1; difficulty rationale and `last_revised` updated. |

## Changes, in one paragraph a physician can read before re-reviewing
SE-S12 keeps its diagnosis: faciobrachial dystonic seizure status from an anti-LGI1 encephalitis relapse after the prednisone taper, in a 47-year-old on levetiracetam and mycophenolate. The FBDS are now right-sided (face and arm) throughout, contralateral to the left mesial temporal focus on EEG and MRI. The blood cultures are gone. The core labs are plain (levetiracetam 32 in range, glucose 118, normal electrolytes) and no longer reveal the antibody result. A separate required serum autoimmune panel shows LGI1 rising to 1:64 with the other antibodies negative. The CSF is recommended: mild lymphocytic pleocytosis, LGI1 1:4, HSV PCR negative. The EEG captures left temporal runs time-locked to each right faciobrachial event. CT and MRI are written in report voice. The post-treatment EEG, the rituximab literature output and the leaking drug block are gone; the drug check is optional and lists real interactions, and literature is optional. The musts are a benzodiazepine, IV methylprednisolone 1 g for 5 days with a slower taper, IVIG, lacosamide rather than fosphenytoin as the second ASM, neuroimmunology on maintenance escalation, and cEEG. The carbamazepine recommendation is removed.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: `[ACNS_2021]`, `[Graus_2016]` and `[Irani_2011]` are cited here and need the criteria-pack allow-list.
- Diagnosis code: the case's first code is G41.2 (complex partial SE), and the accepted labels include "non-convulsive status epilepticus" and "NCSE". FBDS status with focal motor events fits G41.8 better, and the NCSE labels should be pruned for this case. Not changed here (the synonym expansion is central).

## Open questions for Andrea (judgment calls you could not settle)
- The serum autoimmune panel is required and the CSF only recommended, because serum is the more sensitive LGI1 test and the CSF does not change acute treatment. If you want both specimens required for a relapse, a5 can go back to required.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case (large rewrite; R2 needs changes).
- Note 5daa0f16: confirmed. There is no microbiology criterion, output or stop-rule entry, and "blood culture" appears nowhere.
- Note 19c53320: confirmed. The FBDS are right face and right arm in the CC, HPI, exam (cranial nerves, motor, additional) and the EEG video correlate. They agree with the left temporal T3 runs, the left > right MRI, right hyperreflexia, right hand weakness and right dysmetria.
- Other checks: LGI1 is no longer in the core labs (the leak is fixed). The serum panel is required with its own follow-up, and the CSF is recommended with `autoimmune_panel` and `HSV_PCR` keys. The hard CT-before-CSF constraint is present. The methylprednisolone must matches the plan. The lacosamide and no-fosphenytoin choice agrees with the prohibition on enzyme inducers. The carbamazepine must is gone. Checks are clean.
- Found and fixed: red herring 1 said "re-escalation and IVIG required", while the IVIG must is conditional ("if the FBDS do not settle on steroids"). It now reads "immunotherapy must be re-escalated (high-dose corticosteroids, IVIG if the FBDS do not settle, and maintenance escalation)". The stale `metadata.revision_reason` now points to this log.
- The worker's open question (CSF recommended vs required) is a sound judgment and stays as logged.

## Close-out (24 Oct 2026)
Decisions in `plans/SE-decisions.md`.
- `icd_codes[0]` G41.2 -> G41.8 (other SE): faciobrachial dystonic seizure status is a motor SE, not complex partial NCSE (SE summary CENTRAL 3b). NCSE labels removed; new scoped synonym "faciobrachial dystonic seizures" (entry G41.8+fbds). "LGI1 encephalitis" alone is deliberately not a synonym: the relapsing anti-LGI1 encephalitis is in the history, so naming it does not show the status the case scores. `accepted[0]` unchanged.
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, SE case guards pass, `apply_diagnosis_synonyms.py --check --conditions status_epilepticus` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `continuous_icu`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
