# MG-RM12
Reviewer status: none (condition not reviewed in this round; July 2026 tool review only) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none | - | No reviewer notes for this case (`notes/MG.md` does not exist). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `patient.clinical_history.medications` | Enoxaparin listed as a current medicine while its indication says "now discontinued". | FIXED: removed from the list; the HPI says it was stopped at discharge. |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.additional` | HPI closed with "new cranial NMJ-pattern symptoms" (names the localisation); exam held NIF -46 (scored respiratory result, class K) and "new NMJ findings". | FIXED: neutral wording; NIF removed; bedside speech fatigue kept. The prior admission's CSF (protein 58, 2 cells) moved from the current labs into the HPI as history (CSF is not scored). |
| A | minor | `patient.physical_exam` | No weight or height for mL/kg. | FIXED: 83.0 kg, 176 cm (BMI 26.8). |
| B | major | `initial_tool_outputs.labs` | Prior-admission CSF protein reported as a current serum result; qualitative "CBC/BMP All normal" and a TSH stub row (class G); anti-ganglioside bundle "All negative"; mixed laboratory ranges; percentages as strings. | FIXED: CSF row moved to history; CBC, BMP, TSH and free T4 with values; ganglioside bundle removed (GQ1b kept, it is the relevant antibody for ophthalmoplegia after GBS and carries red herring 2); one laboratory's ranges; report-voice interpretation. |
| A | major | `initial_tool_outputs.ct`, `followup_outputs[request_thymectomy_evaluation]` | Chest CT stored in the head-CT slot (`order_ct_scan` images head and neck only, class H3), duplicated by a body-imaging follow-up; both recommended "surgical evaluation" (management). | FIXED: one `initial_tool_outputs.body_imaging` report (mediastinum, chest; contrast) describing a diffusely enlarged thymus with preserved shape, most consistent with hyperplasia, no thymoma; head-CT slot set to null (the library answers a head CT with a normal report); follow-up deleted. |
| B | major | `initial_tool_outputs.specialized_test` | "High-rate RNS 50 Hz ... >100% increment threshold" (plan fact 8: brief exercise, 60% cut-off); interpretive "(residual GBS demyelination)" and "prior GBS makes interpretation complex"; SFEMG recommendation. | FIXED: technique row; motor NCS and F-waves with values compared with the study 5 weeks ago (improving residual demyelinating features); nasalis 13%, deltoid 9%; 10 s exercise increment 6% with exhaustion at 3 min; numbered impression; no recommended actions. |
| C | major | `followup_outputs[request_respiratory_function]` | FVC without % or mL/kg, reference "> 3.0 L predicted", MIP reference sign inverted. | FIXED: FVC 2.6 L (57%, 31.3 mL/kg) with a 12% supine fall, MIP -46, MEP 62, single-breath count 19, all flagged. |
| D | major | `followup_outputs` (literature, MuSK/LRP4/VGCC, IVIG drug check) | Patient-directed literature with unverifiable sources and the wrong phrase "post-synaptic peripheral demyelination"; MuSK/LRP4 re-test in an AChR-positive case (H9); IVIG "drug check" giving a treatment plan (class J). | FIXED: all deleted; one canonical initial literature output. No drug output kept: gabapentin is the only medicine and has no interaction (plan 3.2), so the drug criterion was deleted. Leak guard passes. |
| C | minor | `followup_outputs[request_emg_single_fiber]` | Blocking 65% against a "<10%" reference; no jitter count. | FIXED: mean MCD 62 us, 15/20 pairs with increased jitter, 9/20 blocking; report voice. |
| C | major | new criterion `action-ice-pack-test`; `metadata.actions_withdrawn` | Ice pack withdrawn in August; bilateral fatigable ptosis is present. | FIXED: recommended criterion and report (left MRD1 1.0 to 3.5 mm); withdrawn entry removed. |
| C | major | `action_criteria` tiers, order, arguments | Template tiers (literature and generic pyridostigmine check required with `screen_for`, exact query, MuSK and LRP4 in the labs criterion); SFEMG recommended although RNS is diagnostic and jitter is non-specific after a neuropathy. | FIXED: order respiratory (required: bulbar with reduced FVC and MIP, plan 3.2), ice pack, labs `[anti_AChR, TSH]`, RNS, SFEMG (optional), mediastinal CT (alternative chest CT), literature (optional); drug criterion deleted; case rationales. |
| C | major | `sequence_constraints`, `stop_rule` | Template `labs -> SFEMG`; stop rule with literature and drug check, 0 extra actions. | FIXED: soft `labs -> SFEMG`, `RNS -> SFEMG`; stop rule respiratory, labs, RNS, CT; `max_additional_actions: 2`. |
| C | major | `assessment.required_recommendations` | Musts were tests ("SFEMG", "thoracic imaging/MRI") and vague statements; no symptomatic, rapid or thymectomy plan. | FIXED: pyridostigmine; PLEX or IVIG for bulbar weakness with reduced reserve (repeat IVIG after the GBS course acceptable); monitored bed with 20/30/40 triggers; steroid start low or inpatient high dose, azathioprine after TPMT; thymectomy when stable (MGTX, 42, hyperplasia); drug list. |
| C | minor | `assessment.prohibited_recommendations` | Template set with telithromycin and the functional-disorder line. | FIXED: canonical drug and steroid prohibitions; mimic prohibition naming GBS relapse or variant. |
| C | major | `ground_truth.differential` | Recurrent GBS `moderate` after the results; MFS "reflexes preserved" while he is hyporeflexic; brainstem lesion "no focal MRI findings" with no MRI in the pathway. | FIXED: recurrent GBS low (improving NCS), A-CIDP low, MFS/GBS with ophthalmoplegia very_low (GQ1b negative, no ataxia, residual hyporeflexia explained), brainstem very_low on clinical grounds, functional very_low. |
| C | minor | `key_clinical_evidence`, `red_herrings[0]`, `metadata` | Template bullets; difficulty text "anti-GQ1b testing critical". | FIXED: six case-specific bullets; red herring mentions the improving NCS; difficulty text and rationale updated. |
| C | minor | `avoided_actions[*]` | `[Wolfe_2016]` on every waste item. | FIXED: case rationales (CSF already examined in the GBS admission; brain MRI not needed for pupil-sparing fatigable signs); citations emptied. |

## Changes, in one paragraph a physician can read before re-reviewing

A 42-year-old man develops fatigable ptosis, diplopia, jaw fatigue and nasal speech while recovering from presumed GBS. The pathway now reads: respiratory function first (required; FVC 2.6 L, 57%, 31.3 mL/kg, 12% supine fall, MIP -46, MEP 62 cmH2O), ice-pack test (recommended, positive on the left), AChR antibody with thyroid function (required; AChR binding 2.1 nmol/L, blocking and modulating raised, MuSK and GQ1b negative), RNS with repeat NCS (required; 13% nasalis decrement, no facilitation, residual demyelinating features improving since the GBS study), SFEMG (optional), mediastinal CT with contrast (required, now in the body-imaging slot; thymic hyperplasia, no thymoma) and literature (optional). The prior CSF result now sits in the history, the drug check and the IVIG, MuSK and literature follow-ups are gone. Musts: pyridostigmine, PLEX or IVIG with monitored care and respiratory triggers, cautious steroids with azathioprine after TPMT, thymectomy when stable, drug list. GBS relapse and A-CIDP are low after the improving conduction studies.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys in text only: Jacob 2025, Narayanaswami 2021, Lawn 2001 (plan CENTRAL 1).

## Open questions for Andrea (judgment calls you could not settle)

- None that need Andrea's information. Decisions recorded: (1) respiratory function is `required` (plan 3.2: bulbar symptoms with reduced FVC and MIP stated in the case), not `recommended` as the plan's 3.5 table says; the PLEX/IVIG and monitoring musts depend on it. (2) The plan asked that the RNS report show no demyelination; the report keeps mild residual demyelinating features improving compared with the GBS study, which is what 4 weeks after GBS looks like and is what excludes a relapse. (3) SFEMG is `optional` rather than recommended because the RNS is diagnostic and a recovering neuropathy also raises jitter.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log and the whole final case. No reviewer notes exist for MG. Checked each own-finding row against the file: enoxaparin removed from the medicines and stated as stopped, prior CSF moved to the HPI as history, chest CT now one body-imaging report (thymic hyperplasia, no thymoma) with the head-CT slot null, RNS report with technique, nasalis 13% decrement, post-activation exhaustion and improving residual demyelinating NCS, SFEMG with pair counts, respiratory values correct (FVC 2.6 L = 31.3 mL/kg at 83.0 kg, 57% of 4.6 L, supine fall 12%), BMI 26.8 matches, drug criterion and output deleted (gabapentin only, no interaction; check_drug_interactions is not a panel-required modality), musts specific (PLEX or IVIG with the second-course note, 20/30/40 triggers, thymectomy when stable per MGTX), differential lowered with the excluding results.

Found and fixed:
- B minor, `followup_outputs[request_respiratory_function].output.findings[Single-breath count]`: a count of 19 against a reference of >=25 was not flagged although every other reduced value is (plan fact 14). Now "19 L".

`perfect_agent.py MG-RM12 -v` passes, `case_io.py check` reports no failure naming the case, case guards pass.

## Close-out (24 Oct 2026)

- `ground_truth.diagnosis.icd_codes[0]` G70.01 -> G70.00. ICD-10-CM G70.01 is myasthenia gravis with (acute) exacerbation, including crisis; this is a new or stable presentation, not an exacerbation. G70.01 stays accepted as a secondary code (plans/MG-decisions.md, Q2).
- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG']; icd_codes = ['G70.00', 'G70.0', 'G70.01']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.
