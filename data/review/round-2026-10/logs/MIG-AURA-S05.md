# MIG-AURA-S05
Reviewer status: no reviewer notes for MIG-AURA (R1 and R2 never reviewed this condition) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance for migraine_with_aura, applied below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.history_present_illness`, `patient.hpi` | All four auras in the left visual field with a right-sided headache: side-locked aura is an imaging red flag (plan 1.2), contradicting the no-imaging S case (same class as S01, S02). | FIXED: "one visual field (the left in three episodes, the right in one)", blurred vision "on that side", headache "on the opposite side". |
| B | major | `initial_tool_outputs.clinical_assessment` (class A) | HPI sentences copied (the "Headache relation" line was the HPI's first sentence), generic SNNOOP10 line, placeholder modalities. | FIXED: per-element findings (4 attacks, visual aura, 20 min spread, no succession, contralateral headache, 1-2 days a month, triggers, exam); red flags named and absent including recent onset at 22; criterion C 5 of 6; impression ICHD-3 1.2.1.1. |
| D | major | `initial_tool_outputs.literature_search` (class B) | Template block equal to the literature criterion's expected evidence (guard failure). | FIXED: deleted. |
| D | minor | `followup_outputs[0]` (old) | Empty literature follow-up. | FIXED: deleted. |
| C | major | `followup_outputs[2]` (old literature, class B) | Screen-time search with weak or unsupported claims (blue light "triggers cortical spreading depression", blue-light filters reduce frequency) and a patient CONCLUSION; empty `query`. | FIXED: deleted; trigger advice is a must. |
| C | major | `followup_outputs[0].output` (drug, class C) | Summary-only block naming the patient ("22-year-old woman", "No contraindications in this patient", "Not on OCPs"), duplicated conclusion. | FIXED: structured sumatriptan check (ibuprofen no interaction, labelled contraindications, timing, overuse, chest tightness, alternatives; sources SmPC, NICE CG150). |
| A | major | `ground_truth.action_criteria[action-2]` (class C) | `{"context": ...}` unattainable; required without an interaction; expected evidence contained contraception and preventive decisions. | FIXED: `{"drug": ...}` alternatives sumatriptan, triptan, rizatriptan, ibuprofen; optional; rewritten. |
| A | minor | `ground_truth.action_criteria[action-1]` (rule 5), `stop_rule`, citations (class N) | Literature required and first; stop rule with literature and drug check; duplicate and free-text citations. | FIXED: literature optional, `{}`, last; stop rule history only, max 0; one key per source. |
| C | major | `ground_truth.assessment.required_recommendations` | No acute treatment must although she is triptan-naive with partial ibuprofen relief; two diagnostic musts; contraception must without the category. | FIXED: clinical diagnosis without imaging; sumatriptan at headache onset with ibuprofen and antiemetic; no preventive, diary and trigger advice; UKMEC 4 counselling. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` (class I) | Ergot boilerplate; non-canonical combined-pill text. | FIXED: ergot deleted; canonical UKMEC 4 prohibition. |
| C | minor | `ground_truth.red_herrings[0]`, `ground_truth.key_clinical_evidence[0]`, `metadata.difficulty_description`, `.difficulty_rationale` (class E) | Repeated "MRI is a reasonable cautious step", "normal MRI", "justify cautious MRI" although the case has no MRI and the tier is none. | FIXED: red herring interpretation, key evidence and metadata now say no imaging is needed. |
| D | minor | `ground_truth.key_clinical_evidence` (class D) | "July 2026 review" line. | FIXED: deleted. |
| B | minor | `ground_truth.differential` | Seizure, IIH and AVM key features vague or with dashes. | FIXED: case features (seizure duration, BMI 21.6 and no papilloedema, aura on both sides). |
| C | minor | `ground_truth.avoided_actions[avoid-waste-3]` (class N) | PFO rationale cited `[Charles_2017]`. | FIXED: citation removed; trials named. |
| A | minor | `fallback_tool_outputs.specialized_test` (class M) | Junk fallback "general_neurodiagnostic_assessment". | FIXED: null. |

## Changes, in one paragraph a physician can read before re-reviewing

A 22-year-old woman with four attacks in 3 months of visual aura (photopsia enlarging into a shimmering arc over about 20 min) followed by contralateral headache, normal examination, new job with long screen hours. The aura now occurred on the left three times and on the right once, so it is not side-locked and no imaging is indicated; every "cautious MRI" statement (red herring, key evidence, metadata) now says so. The structured history is this patient's own (5 of 6 criterion C, no red flag, recent onset at 22 is not a red flag). The template literature block, an empty literature follow-up and a screen-time search with unsupported claims are gone; the drug check is optional with a structured sumatriptan review. Musts: clinical diagnosis without imaging; sumatriptan at headache onset with ibuprofen and an antiemetic; no preventive, diary and trigger advice; UKMEC 4 counselling. Prohibition: combined hormonal contraception.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: "migraine aura" in the G43.109 group (plan section 5.1).
- To the lead: side-locked aura corrected in S01, S02 and S05 (all typical S cases); other S cases may carry the same template.

## Open questions for Andrea (judgment calls you could not settle)

- Decided: with only four attacks, three on the left and one on the right is a deliberate data change to keep the typical no-imaging design; if the case is meant to test imaging restraint in a side-locked aura, the alternative would be an MRI criterion, which the plan does not want here.

## Verification
Adversarial verifier, 24 Oct 2026. Read the final case.
- Checked: each own finding against the file (aura left three times and right once, with the side and contralateral headache consistent across the HPI, structured history and AVM differential; C 5 of 6; four attacks in 3 months meet criterion A; every "cautious MRI" statement gone; template and empty literature blocks gone; `{"drug": ...}` alternatives; optional tiers; stop rule history only with max 0; no preventive at 1-2 moderate days a month; canonical UKMEC 4 prohibition). All hold. Nothing clinically wrong found.
- Found and changed: `metadata.fallback_tool_kinds.specialized_test` described the fallback that is now null: key removed.
- Checks after the edit: `perfect_agent.py -v` ok; `case_io.py check` clean for this case; guard tests pass.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x1, [ICHD_3] x2.
- synonyms re-derived (`apply_diagnosis_synonyms.py --prune`): "migraine aura" removed (its tokens are a subset of "migraine without aura", a wrong answer); "migraine with aura", "migraine with typical aura", "classic migraine" and G43.1, G43.119, G43.909 kept.
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.
