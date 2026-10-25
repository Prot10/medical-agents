# GBS-RP14
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 91de81af-b530-4c9f-b3d0-a6095eef7cd4 | FIXED | Day 1 reflexes now have one value, "diminished", stated once in the HPI ("On admission there was no limb weakness and her reflexes were documented as diminished"); the "findings not present at admission" sentence is gone. `patient.neurological_exam` is the day 6 examination only (reflexes patellar 1+, Achilles absent, biceps and brachioradialis 1+, flexor plantars); admission mental status, coordination and cranial-nerve statements moved to the HPI or removed. |
| ed62b4ac-1d07-4a36-8d70-f1962cc4a05b | FIXED | `followup_outputs[1]` (respiratory) in the canonical format: FVC 1.9 L (68% predicted; 23 mL/kg at 81 kg) L, MIP -30 cmH2O L, MEP 46 cmH2O L, cough effective. Weight and height added (`patient.physical_exam.general` "Weight 81 kg, height 165 cm", BMI 29.8 agrees). Must 1: ICU-level monitoring now (MIP at the -30 threshold, weakness spreading to the arms, COPD reducing reserve) with the intubation criteria (FVC <20 mL/kg, about 1.6 L, or <60%; MIP weaker than -30; MEP <40; bulbar weakness; distress, hypoxaemia, hypercapnia). a4 canonical. |
| 797f335a-8ac9-4a20-ae17-6874e4bccdee | FIXED | Musts already done or unorderable deleted (sodium correction, SIADH cause work-up, brain MRI for ODS); the sodium must is now a current-encounter monitoring must (keep the thiazide stopped, fluid restriction, sodium with osmolality every 12-24 h during IVIg, cap any further correction at 8-10 mEq/L/24 h). Brain MRI and EEG remain history (done on admission, not scored); the EEG follow-up was deleted and EEG added to waste with that reason; the brain MRI waste rationale now explains why the day 6 deficit does not call for a repeat. Osmotic demyelination lowered from moderate to very_low (lower motor neuron deficit with sensory loss and areflexia, no bulbar, pseudobulbar or long-tract signs, polyradiculoneuropathy on NCS and CSF). "Primary SIADH" high reworded as "SIADH or thiazide-associated hyponatraemia as the sole cause" low; autoimmune encephalitis very_low (encephalopathy resolved with sodium). The day-1 CSF values were removed from the HPI (C7). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.labs` | The labs returned to an order on day 6 were the admission labs (sodium 110, WBC 18.1, urine osmolality), contradicting the HPI (sodium corrected, encephalopathy resolved); they also carried HIV with the leaky clinical_significance (C10), Campylobacter IgM (C3), lipids and SPEP, and no liver tests, albumin or CK. | FIXED: admission values moved to the HPI as dated history (sodium 110, osmolalities, urine sodium, normal TSH and cortisol, WBC 18.1); the labs report is now day 6: sodium 132 L, serum osmolality 274 L (arithmetic consistent), creatinine 0.4 L, glucose 104 H, WBC 11.4 H, liver tests, albumin 3.6, CK 88 normal. a1 expected_evidence names these values. |
| B | major | `followup_outputs[0]` CSF | The CSF report was the day 1 tap (viral PCR, cultures) that the HPI also quoted, so the scored LP returned a result already in the patient block. | FIXED: the scored CSF is a day 6 lumbar puncture (protein 78 mg/dL, 2 cells/mm3, ratio 0.60 with serum glucose 104); the day 1 tap stays in the HPI only as "no infection; antibiotics stopped", without values. a3 rationale says why the LP is repeated. |
| A | major | `followup_outputs` | Ganglioside follow-up (anti-GM1 IgG 1:80) in typical GBS (C2); EEG follow-up (C9); empty literature and DDI placeholders. | FIXED: all deleted. |
| D | major | `initial_tool_outputs.literature_search` | Echoed a5's expected_evidence (C11). | FIXED: canonical general output; a5 optional and last. |
| C | minor | `initial_tool_outputs.specialized_test` | "AIDP" in the pattern field; median CMAP missing; no needle EMG; `test_type` in prose. | FIXED: pattern "Demyelinating polyradiculoneuropathy"; median CMAP 4.6 mV; lower limb CMAPs labelled reduced; needle EMG line; `test_type` "emg_ncs". |
| C | minor | `initial_tool_outputs.ecg` | QTc 452 ms in a woman called "borderline", "may worsen with SIADH correction" (unfounded, cross-modality). | FIXED: normal intervals. |
| C | minor | `followup_outputs` telemetry | 96-hour "ICU" telemetry with a day 7 event (future), interpretive "Mild autonomic lability" (C12). | FIXED: first 24 h on the ward, the same rates (sinus tachycardia to 108, 58 in sleep) with blood pressure 136/80 to 176/98; a8 canonical. |
| C | major | `ground_truth.assessment` | Musts generic; no ICU or IVIg indication; nothing on IVIg and sodium; "corticosteroids as monotherapy" (C8). | FIXED: ICU-level and intubation must; IVIg 2 g/kg (about 32 g/day at 81 kg) for GBS disability 3 within 2 weeks; sodium monitoring with osmolality (IVIg pseudohyponatraemia); telemetry; LMWH. Prohibitions: canonical steroid text; no hypertonic saline for a measured fall during IVIg without osmolality; renal function before IVIg. |
| C | minor | `ground_truth.action_criteria` a6 | DDI required by template. | FIXED: optional (hydrochlorothiazide, the only management-changing drug, was stopped on admission; losartan is an ARB, not an ACE inhibitor); DDI output category-level (thiazide hyponatraemia, IVIg and measured sodium, losartan and PE, tiotropium retention). Medication entry marks hydrochlorothiazide as stopped on admission. |
| C | minor | `ground_truth.differential`, `red_herrings` | Back pain before the leg symptoms not addressed; hepatic encephalopathy and stroke entries without case support. | FIXED: cord/cauda equina compression very_low; back pain red herring added; hepatic and stroke entries replaced; acute-onset CIDP low. Hyponatraemia red herring moved to the HPI field path and now mentions the thiazide. |
| D | minor | `patient.chief_complaint`, `neurological_exam.additional` | Chief complaint carried the sodium value and the exam findings; `additional` repeated "SIADH confirmed" and the timeline. | FIXED: chief complaint in clinical terms; `additional` holds back pain without spinal tenderness and no sphincter dysfunction. |
| B | minor | `ground_truth.sequence_constraints`, `stop_rule` | Template constraints; stop rule with literature and DDI and 0 extra actions. | FIXED: constraints deleted (a6 optional); stop rule = five required criteria, `max_additional_actions` 3. |
| E | minor | `metadata.difficulty_description` | Referred to the "buried" day 1 CSF clue now removed. | FIXED: rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

A 64-year-old woman (81 kg, COPD) admitted with hyponatraemic encephalopathy (sodium 110, SIADH-pattern urine while on hydrochlorothiazide) was corrected to 120 in 24 hours, recovered cognitively, and on day 6 developed back pain, distal sensory loss and flaccid weakness of the legs more than the arms with depressed or absent reflexes. The patient block now reads as a dated history (day 1 reflexes "diminished", admission labs, MRI and EEG as history) and a single day 6 examination. The work-up returns day 6 results: NCS/EMG demyelinating, a day 6 CSF with protein 78 mg/dL and 2 cells, labs with sodium 132 and normal liver tests, albumin and CK, respiratory function FVC 1.9 L (68%, 23 mL/kg), MIP -30, MEP 46 cmH2O, and 24-hour telemetry. The assessment moves her to ICU-level monitoring with intubation criteria, gives IVIg 2 g/kg, keeps the thiazide stopped and monitors sodium with osmolality during IVIg, with telemetry and DVT prophylaxis. Osmotic demyelination, isolated SIADH and autoimmune encephalitis are now low or very low with reasons; hyponatraemia and back pain are the red herrings.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 5 (weight field) and 10 (respiratory-report guard) apply.

## Open questions for Andrea (judgment calls you could not settle)

- None. Decision recorded: MIP exactly -30 cmH2O does not meet "weaker than -30", but with COPD and spreading weakness I made ICU-level monitoring a present must rather than an escalation trigger (plan C1: the decision is trend plus reserve, not one threshold).

## Verification (adversarial verifier, 24 Oct 2026)

Checked: all three note ids present; day 1 reflexes "diminished" stated once; completed musts removed, brain MRI and EEG are history and waste, EEG follow-up gone; ODS very_low and SIADH-as-sole-cause low with reasons. Day 6 labs consistent (calculated osmolality 2 x 132 + 104/18 + 8/2.8 = 273 against 274 measured); CSF ratio 62/104 = 0.60; BMI 81 / 1.65^2 = 29.8; 1.9 L / 81 kg = 23 mL/kg; disability score 3 matches "cannot walk safely without bilateral support"; a6 optional with a sound reason (thiazide stopped, losartan is an ARB).

Found and fixed:
- C, major: must 1 listed "FVC below 20 mL/kg ... or 60% predicted" as an intubation trigger. FVC <60% predicted is the ICU-level monitoring trigger (plan C1, note 2a09feee), not an intubation criterion, and she is already in ICU-level monitoring. Removed "or 60% predicted" from the intubation list.
- B, minor: a7 expected_evidence and rationale were the template while the ECG is normal sinus rhythm 92 with QTc 452 ms. Rewritten to what the ECG shows.
- B, minor: telemetry finding "Sinus tachycardia 96-108 bpm while awake" (96 is not tachycardia) changed to "Sinus rhythm 96-108 bpm while awake"; the impression already says tachycardia to 108.

Checks run after the edits: `perfect_agent.py -v` passes (every required and recommended criterion served by its own report), `case_io.py check` clean for the case (schema, synonym guard, no test failure naming it), `test_case_guards.py` leak, follow-up and banned-string guards pass.


## Condition audit (24 Oct 2026)
Condition auditor, after the worker and the verifier. Changes made through case_io; `perfect_agent.py` and `case_io.py check` re-run clean for all 30 GBS cases afterwards, and `test_case_guards.py -k GBS` passes.
- E, minor: `fallback_tool_outputs.drug_interactions.general.proposed` read "(agent not specified on this case's pathway)", an engineering note served to any off-pathway interaction check (PATTERNS 5). Now "Medication list review", as in S01-S03 and RS18.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels and the three AIDP labels (its NCS is demyelinating); "acute motor axonal neuropathy", "AMAN" and "miller fisher syndrome" are no longer accepted (wrong subtype or variant for this case).
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- follow-up `request_cardiac_monitoring`: `monitor_type` "Continuous telemetry" -> `telemetry`.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-6-check-drug-interactions` rationale: "The only management-changing drug, hydrochlorothiazide, was stopped on admission; the check does not change the IVIg or plasma exchange decision (ROUND_POLICY ruling 6)." -> "The only management-changing drug, hydrochlorothiazide, was stopped on admission; the check does not change the IVIg or plasma exchange decision."
