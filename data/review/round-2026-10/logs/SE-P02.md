# SE-P02
Reviewer status: R1 not reviewed, R2 not reviewed (no notes) | Approved before this round: per plan

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | The notes file has no note for SE-P02. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | The HPI said "EMG artifact and motion artifact make initial EEG interpretation extremely challenging", which is engineering text about the scored EEG (plan C7). | FIXED: removed. The HPI says blood was drawn on arrival, lamotrigine level included. A duplicate sentence on epilepsy plus PNES was removed. |
| D | minor | `neurological_exam.mental_status`, `sensory` | "Purposeful-appearing arm movements inconsistent with epileptic activity" and "withdrawal inconsistent with true unconsciousness" were interpretation. | FIXED: the observations stay, the verdicts are gone. |
| B/C | major | `initial_tool_outputs.eeg`, follow-up `request_continuous_eeg_monitoring` | The initial EEG was a routine normal study with motion artifact and no video. The event capture that decides the case sat in a separate cEEG follow-up (plan C7). | FIXED: the follow-up is merged into the initial EEG, a video-EEG with 3 captured events (arm shaking with eyes closed, head movement side to side, pelvic thrusting). The 9-10 Hz posterior rhythm persists, with no correlate and no post-event suppression. The follow-up is deleted. |
| A/C | major | `initial_tool_outputs.labs` | It had a template "Exclusion studies" block holding beta-hCG. Lamotrigine 14.2 against a 3-14 range was flagged normal. The prolactin reference "2-29 baseline; >200% ... expected" leaked the teaching point. There were no liver tests and no CMP (C1, C2, C15). | FIXED: block deleted. Beta-hCG is its own panel (<2 mIU/mL, ref <5). Lamotrigine is 8.4 (in range; the "therapeutic" story holds). Prolactin has a plain range (4.8-23.3) and a draw time. The CMP has chloride, BUN, liver tests and albumin. The summary and interpretation are a recital. |
| A | major | `action-2-interpret-labs` | 11 panels including ABG, ammonia and autoimmune markers. | FIXED: T-LABS with AED_levels, tox_screen, beta-hCG and prolactin as extras; rationale notes that normal markers do not exclude an epileptic seizure [LaFrance_2013]. |
| A/C | major | follow-ups (serial prolactin, psychology literature, MRI, autoimmune panel), `action-6` | Serial prolactin, a second literature output and an MRI follow-up repeated or padded the case (plan C15). An autoimmune panel was recommended without any autoimmune feature. | FIXED: all four follow-ups deleted; the autoimmune criterion deleted (the differential ranks it very low with the reason). MRI stays optional and is answered by the fallback (incidental pineal cyst). |
| A | major | `action-4`, `action-5`, sequence constraints | The drug check and literature were required; "EEG before drug check" was hard (plan C9). | FIXED: both optional, literature last; the constraint is soft. Criteria order: labs, CT, EEG, MRI, DDI, literature. EEG accepts `video` or `continuous_icu` (T-EEG for P02). |
| D/C | minor | DDI follow-up | Pregnancy counselling sat inside the interaction report. | FIXED: T-DDI. Lamotrigine-sertraline (minor), lorazepam and levetiracetam (none), valproate raising lamotrigine levels, and lamotrigine clearance in pregnancy. The valproate warning is a fact, not advice. |
| D | minor | literature follow-up | The output was a management plan for this patient. | FIXED: T-LIT on the LaFrance 2013 staged diagnostic levels and on iatrogenic harm in general terms; trigger `request_pnes_literature`. |
| C | major | `assessment` | "Single dose of IV lorazepam is reasonable" stood without a dose, beside a prohibition of benzodiazepines. A prohibition was duplicated. Escalation to anaesthesia or intubation was not prohibited. | FIXED: one dosed lorazepam (0.1 mg/kg, max 4 mg) is allowed while epileptic SE is not excluded, without repetition. Musts: video-EEG before escalation, communication, psychological treatment, continue lamotrigine, precipitants and suicidality. Prohibitions: no anaesthetic infusion or intubation for PNES [LaFrance_2013], no second-line loading, no dismissal, no valproate. |
| C | minor | `differential` | "Breakthrough JME convulsive SE" was high after a video-EEG without correlate. | FIXED: low, with the excluding results. Frontal hypermotor seizures added as low with the distinguishing semiology. |
| A/E | minor | `clinical_history.allergies` | "Valproate (teratogenicity concern)" is not an allergy. | FIXED: no known drug allergies; the valproate alert moved to the past medical history. |
| A | minor | stop rule, PSG avoided action, fallbacks, metadata | Stop rule listed optional criteria with max 0. The PSG rationale was a copy from another condition. FDG-PET and neuropsychology fallbacks (C10). | FIXED: the stop rule lists the 3 required criteria, max 1; T-PSG; advanced_imaging and specialized_test fallbacks null; `fallback_tool_kinds` and difficulty rationale updated. |

## Changes, in one paragraph a physician can read before re-reviewing
SE-P02 keeps its diagnosis: a prolonged psychogenic non-epileptic event in a 38-year-old nurse with JME on lamotrigine and a prior video-EEG diagnosis of PNES, after acute stress. The event capture now sits in the first EEG: a video-EEG that records three typical events with a preserved posterior rhythm and no correlate. The HPI no longer comments on the EEG. The labs are a real CMP and CBC with a lamotrigine level in range, normal prolactin, lactate and CK at 35 minutes, and a negative beta-hCG, with no exclusion block. Serial prolactin, the extra MRI and literature outputs, and the autoimmune panel are gone. The drug check, MRI and literature are optional. The plan allows one dosed lorazepam while epileptic SE is not excluded, then forbids further ASMs, intubation or anaesthesia for PNES, and requires clear communication, psychological treatment and continued lamotrigine. Valproate is prohibited because she is planning a pregnancy.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: `[LaFrance_2013]`, `[ACNS_2021]` and `[Glauser_2016]` are cited and need the allow-list.

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial verification, 24 Oct 2026. Checked: CC and HPI free of EEG results; the merged video-EEG event capture (three events, preserved 9-10 Hz posterior rhythm, no correlate); labs and beta-hCG (woman of 38, value and unit plausible); lamotrigine level in range against the "therapeutic" label; deleted follow-ups (serial prolactin, MRI, second literature, autoimmune panel); tiers (labs, CT, EEG required; MRI, DDI, literature optional); soft EEG-before-DDI constraint; prohibition of anaesthetic escalation or intubation [LaFrance_2013]; valproate prohibition for a woman planning pregnancy; follow-up order; leak guard. Found and changed: CK was used as evidence 35 minutes into the event (KCE 3, differential entry 1, labs rationale), but CK rises only hours after a convulsion and is uninformative this early; the argument now rests on prolactin and lactate, and the rationale says CK rises later. The CK value itself stays in the report. perfect_agent ok; case guards pass; case_io check clean for this case.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
