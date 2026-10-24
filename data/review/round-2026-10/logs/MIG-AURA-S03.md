# MIG-AURA-S03
Reviewer status: no reviewer notes for MIG-AURA (R1 and R2 never reviewed this condition) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance for migraine_with_aura, applied below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.history_present_illness`, `patient.hpi` | "approximately 8-10 times per year" stated as the current frequency while the next paragraph reports a significant increase, with no current frequency to judge prevention. | FIXED: "Until recently ... 8-10 attacks per year"; "an increase in attack frequency to about two a month since starting her PhD program 6 months ago". |
| B | minor | `patient.history_present_illness`, `patient.hpi`; `initial_tool_outputs.clinical_assessment.criteria_met` | Unilateral aura marked true although the HPI described only a central scotoma sweeping "to the periphery". | FIXED: arc "sweeps into the periphery of one side of her vision (either side)", which documents the hemifield and that the side varies. |
| B | major | `initial_tool_outputs.clinical_assessment` (class A) | HPI sentences copied (the "Headache relation" line was the opening sentence of the HPI), generic SNNOOP10 line, placeholder modalities. | FIXED: per-element findings; criterion C 5 of 6 (unchanged count, now supported); red flags named and absent; impression ICHD-3 1.2.1.1 with the triggers. |
| C | major | `followup_outputs[0]`, `[1]` (literature, class B) | Literature outputs with empty `query`, patient-directed CONCLUSION, invented figures (75% response rate, "25% reduction per week"), valproate and preventive thresholds. | FIXED: both deleted; literature criterion optional, answered by the library. |
| C | major | `followup_outputs[0].output` (drug, class C) | Summary-only block; "Caffeine can enhance triptan absorption (used in Cafergot preparation)" is wrong (Cafergot is ergotamine with caffeine; caffeine is not used to enhance triptan absorption); "Sumatriptan safe" verdict. | FIXED: structured sumatriptan check (ibuprofen and caffeine no interaction, labelled contraindications, timing, overuse including caffeine combinations, caffeine intake and withdrawal; sources SmPC, NICE CG150). |
| A | major | `ground_truth.action_criteria[action-2]` (class C) | `{"context": ...}` unattainable; required with no concrete interaction. | FIXED: `{"drug": ...}` alternatives sumatriptan, triptan, rizatriptan, ibuprofen; optional; rewritten. |
| A | minor | `ground_truth.action_criteria[action-1]` (rule 5), `stop_rule`, citations (class N) | Literature required, first, in stop rule; duplicate and free-text citations. | FIXED: literature optional, `{}`, last; stop rule history only, max 0; one key per source. |
| C | major | `ground_truth.assessment.required_recommendations` | Vague musts ("Initiate triptan", "Discuss caffeine"); preventive at "4 attacks/month" not the AHS 2021 thresholds; no contraception counselling in a woman of reproductive age. | FIXED: clinical diagnosis without imaging; sumatriptan with ibuprofen and antiemetic at headache onset; trigger management with gradual caffeine taper; diary and preventive discussion at 2 or more disabling days a month after trigger changes; UKMEC 4 counselling. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` (class I) | Ergot boilerplate; non-canonical combined-pill wording. | FIXED: ergot line deleted; canonical UKMEC 4 prohibition. |
| E | minor | `ground_truth.red_herrings[0]` (class E) | Empty `location` and `field_path`; "5-year history predates PhD" imprecise. | FIXED: `patient.history_present_illness`; onset at 19 stated. |
| B | minor | `ground_truth.differential` | IIH "no diurnal pattern, no visual obscurations" not in the case; dash in migraine-without-aura entry. | FIXED: features present in the case (no papilloedema, episodic, BMI 21.3, normal exam). |
| D | minor | `ground_truth.key_clinical_evidence` (class D) | "July 2026 review" line. | FIXED: deleted; four case-specific statements. |
| C | minor | `ground_truth.avoided_actions[avoid-waste-3]` (class N) | PFO rationale cited `[Charles_2017]`. | FIXED: citation removed; trials named. |
| A | minor | `fallback_tool_outputs.specialized_test` (class M) | Junk fallback "general_neurodiagnostic_assessment". | FIXED: null. |
| B | minor | `metadata.difficulty_description` | "normal MRI" (no MRI in the case). | FIXED: rewritten. |

The plan's S03 entry asks to delete an MRI or WMH red herring: this case has none (its only red herring is caffeine), so nothing to delete.

## Changes, in one paragraph a physician can read before re-reviewing

A 24-year-old woman with visual aura since 19 (scotoma expanding into a shimmering arc in one hemifield, either side, over 20-25 min) followed by headache, now about two attacks a month since starting a PhD, with stress, irregular sleep and 3-4 coffees a day. The history now gives the current frequency and documents the hemifield. The structured history is this patient's own (5 of 6 criterion C, no red flag). Both literature follow-ups (invented figures, patient verdicts) are gone; the drug check is optional and no longer claims that caffeine enhances triptan absorption. Musts: clinical diagnosis without imaging; sumatriptan 50-100 mg at headache onset with ibuprofen and an antiemetic; sleep, stress and a gradual caffeine taper; diary with preventive discussion if disabling days stay at 2 or more a month; UKMEC 4 counselling. Prohibition: combined hormonal contraception.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: "migraine aura" in the G43.109 group (plan section 5.1).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the final case.
- Checked: each own finding against the file (current frequency about two a month, hemifield documented, C 5 of 6 consistent, onset at 19, literature follow-ups gone, the Cafergot caffeine claim gone, `{"drug": ...}` alternatives, optional tiers, stop rule history only with max 0, preventive discussion conditional at 2 or more disabling days per AHS 2021 "consider" level, canonical UKMEC 4 prohibition). All hold.
- Found and changed: (1) the seizure differential said "Aura duration 20-30 min" while the case gives 20-25 min: now "Aura spreading over 20-25 min is too slow for seizure propagation". (2) The new drug output stated a "300-400 mg or more" caffeine threshold that has no source in the case (ROUND_POLICY 8: no invented thresholds): now "High daily caffeine intake is associated with more frequent headache, and abrupt withdrawal causes withdrawal headache; reduce gradually." (3) `metadata.fallback_tool_kinds.specialized_test` removed (fallback is null).
- Checks after the edits: `perfect_agent.py -v` ok; `case_io.py check` clean for this case; guard tests pass.

## Condition audit
Condition auditor, 24 Oct 2026 (uniformity pass over all 30 MIG-AURA cases).
- `ground_truth.differential[0]` (migraine without aura): `icd_code` null set to G43.009, as in S06 to S11.

After the edit: `perfect_agent.py` 30/30, `case_io.py check` clean for the condition, `test_case_guards.py -k MIG-AURA` 60 passed.
