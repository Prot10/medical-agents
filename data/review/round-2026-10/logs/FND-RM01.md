# FND-RM01
Reviewer status: no reviewer notes for FND (R1 and R2 never reviewed this condition) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input is the July 2026 tool guidance (plan 1.3), applied through the plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.action_criteria` | No sodium test in a man drinking 7-8 L a day with a prior hyponatremic seizure; no stored labs at all, although `metadata.difficulty_description` speaks of a "current mild hyponatremia". | FIXED: new required `action-sodium-osmolality` (`["sodium", "serum_osmolality"]`) with a stored panel: Na 134 mEq/L, osmolality 278 mOsm/kg (calculated 277.5), glucose 94, calcium 9.3, rest of the electrolytes normal; soft constraint sodium -> video-EEG. |
| C | major | `ground_truth.action_criteria[action-4-analyze-eeg]` | Video-EEG optional in a paroxysmal case with a 72-hour recording of 4 events. | FIXED: required, canonical expected evidence, ILAE 2013 / AAN 2025 rationale; in the stop rule. |
| B | major | `initial_tool_outputs.eeg.findings[2]` | Event 3 said "normal sleep background" while its state said the background was awake during the event. | FIXED: waking background with a reactive posterior dominant rhythm during apparent sleep, stated once. |
| B | minor | `initial_tool_outputs.eeg.impression` | Not in canonical form, no final period. | FIXED: canonical NORMAL video-EEG impression naming the four events. |
| C | major | `patient.neurological_exam.motor` | The Hoover sign was described backwards ("during testing of left hip flexion, involuntary contralateral hip extension is noted"), which is the normal response, not a positive sign. | FIXED: "left hip extension is weak on direct testing but full during right hip flexion against resistance"; same wording in the assessment output. |
| D | major | `initial_tool_outputs.clinical_assessment` | Meta keys; split sentence fragments as two signs; 5 signs counted including the bilateral dragging gait; event witnessed on examination not recorded; impression leak. | FIXED: canonical shape; 3 rule-in signs (collapsing weakness, Hoover, distractibility); observed event and `functional_seizure_semiology_observed: true`; event-based impression; supportive features listed. |
| C | major | `followup_outputs[1]` (`check_risperidone_seizure_threshold`) | Real content held in a follow-up, plus alternative antipsychotics (a plan). | FIXED: deleted; seizure-threshold and prolactin warnings moved to the initial drug output, with antipsychotic hyponatremia, benztropine dry mouth and the haloperidol contraindication; no alternatives. Criterion recommended. |
| D | major | `followup_outputs[0]` (literature) | Unverifiable 2023 systematic review; literature as a clinical step. | FIXED: deleted; canonical literature output (all rows) in `initial_tool_outputs.literature_search`; criterion optional, last. |
| C | major | `ground_truth.differential` | Epileptic seizures `high` after four events without ictal change; hyponatremia-provoked seizures absent; template structural, neuropathy, autoimmune and malingering rows. | FIXED: epileptic low (fact 8, uncle and risperidone noted), hyponatremia-provoked low, antipsychotic tremor or parkinsonism low, proximal myopathy low. |
| C | major | `ground_truth.assessment` | Template musts (video-EEG as a must, neuropsychology, duplicates); prohibitions with "start or continue" ASM and "per Stone 2018". | FIXED: M-DX (mixed), M-COMM with the psychiatric team, M-PHYSIO, M-PSY (anxiety, adapted for schizophrenia), M-RESCUE, continue risperidone with monitored fluid intake and sodium; P1, P2, P3, P5, P6, P7, no haloperidol. |
| C | minor | `ground_truth.avoided_actions[avoid-waste-1-analyze-ecg]` | ECG scored as waste in a patient on risperidone whose events were first reported as loss of consciousness. | FIXED: waste removed; optional `action-ecg` (case fallback ECG answers). |
| E | major | `ground_truth.key_clinical_evidence` | Eight template items (Interim composition leak, OPTIONAL item, Stone 2018). | FIXED: five case-specific items. |
| B | minor | `ground_truth.red_herrings` | Generic family-history, trauma and stress items; the main red herring (polydipsia with a prior hyponatremic seizure) absent. | FIXED: polydipsia and prior hyponatremic seizure, uncle with epilepsy, schizophrenia (overshadowing), trauma and job loss. |
| E | minor | `patient.history_present_illness` | Editorial "Importantly,". | FIXED: removed. |
| A | minor | `ground_truth.avoided_actions[*]`, `fallback_tool_outputs` | `[Stone_2018]`; specialized_test leak fallback and advanced_imaging `MRI_brain_functional`; echo without `echo_type`. | FIXED: `[Espay_2018]` / `[Stone_2016]` with patient-specific rationales; fallbacks nulled and removed from `metadata.fallback_tool_kinds`; echo `echo_type: TTE`. |
| E | minor | `metadata.difficulty_rationale`, `revision_reason` | Template text (family history of MS, SLE). | FIXED: rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

A 38-year-old man with paranoid schizophrenia on risperidone, polydipsia (7-8 L a day) and a hyponatremic seizure 18 months ago has 3 months of shaking events and leg weakness. The required pathway is now the examination (collapsing leg weakness, a left Hoover sign correctly described, distractibility, and an event witnessed with eyes closed and preserved responsiveness), a serum sodium and osmolality (new: 134 mEq/L and 278 mOsm/kg, too mild to provoke seizures) and the 72-hour video-EEG that records four habitual events without ictal change, one from apparent sleep with a waking background. The medication review (recommended) now carries risperidone's small seizure-threshold effect and prolactin rise, antipsychotic-related hyponatremia, benztropine dry mouth and the haloperidol contraindication. An ECG is optional rather than waste. Musts: positive diagnosis of mixed FND, explanation with his psychiatric team, specialist physiotherapy, adapted psychological therapy for anxiety, a written event plan without benzodiazepines, and continuing risperidone with monitored fluid intake and sodium checks. Epileptic seizures and hyponatremia-provoked seizures are low in the differential, with drug-induced tremor and proximal myopathy.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- EEG routing (plan 5.3): a `routine` EEG order is answered with the stored 72-hour video-EEG and its events.

## Open questions for Andrea (judgment calls you could not settle)

None open. Decisions taken and their reasons:
- M-PHYSIO added (the plan lists DX, COMM, PSY, RESCUE): he has functional leg weakness needing help to walk, which is the plan's own condition for M-PHYSIO.
- ECG made optional rather than waste: risperidone can prolong QT and the events were first reported as loss of consciousness, so an ECG is defensible; it carries no diagnostic credit.
- The stored labs are a basic electrolyte panel with osmolality rather than the two named analytes alone, because the stored report answers any lab order and a sodium is reported with its electrolytes.

## Verification

Adversarial check (24 Oct 2026) of the log against the case and against the pre-round version (`b8be2153^`). What I checked: the patient diff (only "Importantly," removed and the Hoover sign rewritten correctly); the new lab panel (calculated osmolality 2 x 134 + 94/18 + 12/2.8 = 277.5, stored 278; Na 134 flagged low, the only abnormal value in `abnormal_values_summary`); the sodium -> video-EEG constraint and the stop rule; the EEG (four events with times, event 3 state now consistent with a waking background); the drug output against the medication list and the haloperidol allergy; the musts (continue risperidone, fluid and sodium monitoring) against the prohibitions (no haloperidol, no ASM, no benzodiazepines): consistent; the differential (epileptic and hyponatremia-provoked seizures low with this case's results); every log claim marked FIXED.

Found and changed:
- `initial_tool_outputs.eeg.impression`: event 2 was summarised as "side-to-side head shaking", which is the examiner-witnessed event, while the EEG finding for event 2 says only "rhythmic head shaking"; the impression now says "head shaking", matching its own finding.
- `fallback_tool_outputs.ecg.intervals.QRS`: 92 ms with an incomplete right bundle branch block in findings and interpretation; incomplete RBBB in adults has a QRS of 110-119 ms (AHA/ACCF/HRS 2009 recommendations). QRS set to 112 ms. This fallback answers the optional `action-ecg`.
- `metadata.clinical_pearls[0]`: described the Hoover sign the same backwards way the worker fixed in the motor exam (contralateral hip extension on testing hip flexion is the normal response). Rewritten as weak hip extension on direct testing that returns to full strength during flexion of the opposite hip against resistance.

Checks re-run after the changes: `perfect_agent.py -v` ok, `case_io.py check` clean for this case (schema, synonym guard, no failing test names it), `test_case_guards.py -k` passed. The diagnosis label, `icd_codes` and synonyms are unchanged from before the round; no new em dashes or `Stone_2018` strings.

## Condition audit

2026-10-24, FND condition auditor.

- `action-neuropsych-battery.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-1-search-medical-literature.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.

## Close-out (24 Oct 2026)

Andrea's FND ruling of 24 Oct 2026 and the close-out decisions (`plans/FND-decisions.md`). What changed and why:

- `action-4-analyze-eeg` (video-EEG) required -> optional, removed from the stop rule; 1 soft constraint(s) naming it removed; rationale now says what the diagnosis rests on without the recording (ILAE 2013 levels).
- `action-sodium-osmolality` required -> recommended (red-flag test), removed from the stop rule.
- M-DX must, COMM must, red-herring interpretations and metadata no longer say the diagnosis rests on the video-EEG: they rest on the positive signs and the event semiology, with video-EEG confirmation where recorded (open question 8).
- Diagnosis synonyms scoped by phenotype (`diagnosis_synonyms.yaml` F44 entries; a label or code naming another presentation must not score): removed "functional movement disorder"; added "psychogenic nonepileptic seizures", "dissociative seizures", "nonepileptic seizures", "functional limb weakness", "functional motor disorder".
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FND-` passes, now including the discriminator guard.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `video`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
