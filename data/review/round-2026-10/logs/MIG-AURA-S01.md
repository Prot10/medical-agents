# MIG-AURA-S01
Reviewer status: no reviewer notes for MIG-AURA (R1 and R2 never reviewed this condition) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance for migraine_with_aura, applied below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.history_present_illness`, `patient.hpi` | Aura always in the right visual field with an always left-sided headache: a side-locked aura is an imaging red flag (occipital AVM; plan 1.2), which contradicts a typical S case with no MRI. | FIXED: aura "in the periphery of one visual field (more often the right, sometimes the left)", headache "usually on the side opposite the visual disturbance"; AVM differential and the structured history now state that the side alternates. |
| B | minor | `patient.history_present_illness`, `patient.hpi` | "approximately once monthly for the past 5 years" contradicts "increased from one every 6 weeks to almost monthly over the past year". | FIXED: "for the past 5 years, now almost once a month". |
| B | major | `initial_tool_outputs.clinical_assessment` (class A) | HPI sentences copied twice, generic SNNOOP10 line, placeholder modality score. | FIXED: per-element findings (attacks, visual aura, spread and duration, no succession, positive symptoms, headache and disability, triggers and treatment, exam, named red flags); criteria unchanged (5 of 6) and consistent; impression ICHD-3 1.2.1.1, no red flag. |
| C | major | `followup_outputs[0]` (old literature, class B) | Patient-specific verdicts ("Patient was correct to stop", "CONCLUSION"), "WHO category 3-4", preventive "indicated" at monthly frequency, empty `query`. | FIXED: follow-up deleted; the literature criterion is optional and answered by the library. |
| C | major | `followup_outputs[0].output` (drug, class C) | Summary-only block with empty fields, "This patient: no contraindications", "CONCLUSION" verdict. | FIXED: structured sumatriptan check (ibuprofen interaction none, labelled contraindications, timing, overuse, chest tightness and SSRI warnings, alternatives including non-oral sumatriptan and antiemetics; sources SmPC, NICE CG150). |
| A | major | `ground_truth.action_criteria[action-2]` (class C) | `{"context": ...}` unattainable; required without a concrete interaction. | FIXED: `{"drug": ...}` alternatives sumatriptan, triptan, ibuprofen, naproxen; optional (plan table, ROUND_POLICY 6); expected evidence and rationale rewritten. |
| A | minor | `ground_truth.action_criteria[action-1]` (rule 5) | Literature required, template query, first, in the stop rule. | FIXED: optional, `{}`, last. |
| A | minor | `ground_truth.action_criteria[*].citations`, labels (class N) | Duplicate and free-text citations; label identical to rationale. | FIXED: one key per source; rationales state the reason. |
| A | minor | `ground_truth.stop_rule` | Literature and drug check required before assessment. | FIXED: structured history only; max 0. |
| C | major | `ground_truth.assessment.required_recommendations` (class P) | "Discuss preventive therapy given approximately monthly frequency" (about 1 headache day a month is below AHS 2021); "WHO Category 4"; two diagnostic musts. | FIXED: clinical diagnosis without imaging; sumatriptan at headache onset with NSAID and antiemetic (non-oral route if vomiting); no prevention now, diary and reassess; medication-overuse limits; UKMEC 4 counselling with progestogen-only or IUD options (LNG-IUS for dysmenorrhoea). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` (class I) | Ergot boilerplate (no ergot in the case); combined-pill wording not canonical. | FIXED: ergot line deleted; canonical UKMEC 4 prohibition. |
| D | minor | `ground_truth.key_clinical_evidence` (classes D, E) | "July 2026 review" line; MRI and WMH lines although the case has no MRI; preventive threshold cited to `[Holland_2012]`. | FIXED: four case-specific statements. |
| E | minor | `ground_truth.red_herrings[0]` (class E) | Empty `location` and `field_path`. | FIXED: `patient.history_present_illness`; wording tidied. |
| B | minor | `ground_truth.differential` | Migraine-without-aura and AVM key features vague ("would need MRI"). | FIXED: excluding features stated. |
| A | minor | `fallback_tool_outputs.specialized_test` (class M) | Junk fallback "general_laboratory_panel". | FIXED: null. |
| B | minor | `metadata.difficulty_description`, `.difficulty_rationale` | "normal MRI", "2 required tools", "MRI distractor": none of these exist. | FIXED: rewritten. |
| E | minor | `ground_truth.avoided_actions[*].rationale` | Em dashes. | FIXED: reworded without dashes. |

## Changes, in one paragraph a physician can read before re-reviewing

A 28-year-old woman with 5 years of stereotyped visual aura (fortification spectra spreading over 20-30 min) followed by a severe headache with vomiting, now almost monthly, normal examination. The aura now alternates sides (right more often than left) and the headache is usually contralateral, so there is no side-locked red flag and no imaging, as the July ruling intends; the HPI's frequency is consistent. The only required step is the structured ICHD-3 history, whose output is now this patient's data (5 of 6 criterion C, every SNNOOP10 flag named and absent, about one severe headache day a month). The drug check (optional) gives a real sumatriptan review; the literature follow-up with patient verdicts and "WHO category 3-4" is gone. Musts: clinical diagnosis without imaging; sumatriptan 50-100 mg at headache onset with ibuprofen or naproxen and an antiemetic, non-oral sumatriptan if vomiting; no preventive now, diary and reassess; acute-medication limits; UKMEC 4 counselling with progestogen-only or IUD options. Prohibitions: two triptans within 24 h; combined hormonal contraception.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: "migraine aura" in the G43.109 group credits wrong diagnoses (plan section 5.1).
- Citation keys used in rationale text only until added: AHS 2021, AHS neuroimaging 2020, UKMEC 2016, NICE CG150.

## Open questions for Andrea (judgment calls you could not settle)

- Decided: the plan's S01 entry says to delete the combined-pill prohibition if she uses no combined contraception. She stopped it, but she is 28 with dysmenorrhoea, for which the pill is commonly restarted; class I keeps the prohibition in women of reproductive age, so I kept the canonical prohibition and a counselling must. Nothing missing.
- Decided: the side-locked aura was corrected in the history rather than adding an MRI, because the case is the condition's typical S case and the July ruling keeps MRI for red flags.

## Verification
Adversarial verifier, 24 Oct 2026. Read the final patient block, structured history, drug follow-up, ground truth and fallbacks.
- Checked: each own finding against the file (alternating aura side and contralateral headache in both HPI fields, frequency sentence consistent, ICHD-3 C 5 of 6 consistent with the structured fields, onset at 23 consistent with age 28 and a 5-year history, OCP stopped about 1.5 years ago as the red herring says, literature follow-up gone, `{"drug": ...}` alternatives, optional tiers, stop rule history only with max 0, no preventive must at about one headache day a month per AHS 2021, canonical UKMEC 4 prohibition, ergot line gone, red herring path real). All hold. No MRI or WMH text remains.
- Found and changed: `metadata.fallback_tool_kinds.specialized_test` described the fallback that is now null: key removed.
- Checks after the edit: `perfect_agent.py -v` ok; `case_io.py check` clean for this case; guard tests pass.

## Condition audit
Condition auditor, 24 Oct 2026 (uniformity pass over all 30 MIG-AURA cases).
- `ground_truth.assessment.prohibited_recommendations[0]` "Do not co-administer two different triptans within 24 hours" deleted: template prohibition (PATTERNS 4), since she takes no triptan and the plan offers one (sumatriptan). S07 keeps it because she uses two triptans.
- `ground_truth.differential[0]` (migraine without aura): `icd_code` null set to G43.009, as in S06 to S11.

After the edit: `perfect_agent.py` 30/30, `case_io.py check` clean for the condition, `test_case_guards.py -k MIG-AURA` 60 passed.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x1, [ICHD_3] x3.
- synonyms re-derived (`apply_diagnosis_synonyms.py --prune`): "migraine aura" removed (its tokens are a subset of "migraine without aura", a wrong answer); "migraine with aura", "migraine with typical aura", "classic migraine" and G43.1, G43.119, G43.909 kept.
- key clinical evidence citation [AAN_2000] -> [AHS_neuroimaging_2020].
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-2-check-drug-interactions` rationale: "She takes only ibuprofen and has no vascular disease, so the check does not change management (ROUND_POLICY 6). Sources: sumatriptan SmPC; NICE CG150." -> "She takes only ibuprofen and has no vascular disease, so the check does not change management. Sources: sumatriptan SmPC; NICE CG150."
