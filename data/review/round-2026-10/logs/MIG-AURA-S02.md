# MIG-AURA-S02
Reviewer status: no reviewer notes for MIG-AURA (R1 and R2 never reviewed this condition) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance for migraine_with_aura, applied below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.history_present_illness`, `patient.hpi` | Sensory aura always left-sided with an always right-sided headache: a side-locked aura is an imaging red flag (plan 1.2), contradicting a typical S case without MRI (same class as S01). | FIXED: march begins in "one hand (usually the left, occasionally the right)" and reaches the same side of the face; facial heaviness "of that side"; headache "on the opposite side". |
| B | major | `initial_tool_outputs.clinical_assessment` (class A) | HPI sentences copied, generic SNNOOP10 line, placeholder modalities; "6 of 6" with succession true although the aura is a single sensory modality. | FIXED: per-element findings with this patient's data; succession false, criterion C 5 of 6; red flags named and absent (including side-locked and motor aura); impression ICHD-3 1.2.1.1 with premenstrual clustering. |
| D | major | `initial_tool_outputs.literature_search` (class B) | Template block equal to the literature criterion's expected evidence (guard failure). | FIXED: deleted. |
| C | major | `followup_outputs[0]` (old literature, class B) | "category 3-4 per WHO", CONCLUSION verdict for this patient, empty `query`. | FIXED: deleted. |
| D | minor | `followup_outputs[2]` (old) | Empty literature follow-up triggered by "request_migraine_diary" (a diary is not a literature search). | FIXED: deleted; the diary is a must. |
| C | major | `followup_outputs[0].output` (drug, class C) | Summary-only block, "safe and indicated" verdict, empty fields. | FIXED: structured sumatriptan check (paracetamol and naproxen interactions none, labelled contraindications, timing, overuse including perimenstrual triptans, chest tightness, alternatives; sources SmPC, NICE CG150). |
| A | major | `ground_truth.action_criteria[action-2]` (class C) | `{"context": ...}` unattainable; required without a concrete interaction; expected evidence cited `[Holland_2012]` for frovatriptan. | FIXED: `{"drug": ...}` alternatives (sumatriptan, triptan, frovatriptan, zolmitriptan, naproxen, acetaminophen, paracetamol); optional; rewritten. |
| A | minor | `ground_truth.action_criteria[action-1]` (rule 5) | Literature required, first, template query, in stop rule. | FIXED: optional, `{}`, last. |
| A | minor | `ground_truth.action_criteria[*].citations` (class N), `stop_rule` | Duplicate and free-text citations; stop rule with literature and drug check. | FIXED: one key per source; stop rule history only, max 0. |
| C | major | `ground_truth.assessment.required_recommendations` | "WHO Category 4"; mini-prophylaxis offered unconditionally and attributed to `[Holland_2012]` (which covers NSAIDs, not frovatriptan); no acute triptan must although she responded to sumatriptan. | FIXED: clinical diagnosis without imaging; sumatriptan at headache onset with NSAID or paracetamol and antiemetic; diary for 2-3 cycles; perimenstrual frovatriptan or zolmitriptan (NICE CG150) or naproxen sodium 550 mg twice daily [Holland_2012] only if acute treatment fails; UKMEC 4 counselling including continuous regimens. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` (class I) | Ergot boilerplate; non-canonical combined-pill wording. | FIXED: ergot line deleted; canonical UKMEC 4 prohibition. |
| E | major | `ground_truth.red_herrings` (class E) | Both red herrings cite data that do not exist (bubble echo PFO, a 2 mm WMH on an MRI the case does not have), empty paths. | FIXED: both deleted; one real red herring added from the HPI (facial heaviness that could be misread as motor aura). |
| B | minor | `ground_truth.differential` | Seizure excluded by "no inter-ictal epileptiform discharges" (no EEG in the case). | FIXED: key features from the history; TIA and radiculopathy reworded without dashes. |
| D | minor | `ground_truth.key_clinical_evidence` (class D) | "July 2026 review" line; "the criteria pack allows" (engineering wording). | FIXED: four case-specific statements. |
| A | minor | `fallback_tool_outputs.specialized_test` (class M) | Junk fallback "general_neurodiagnostic_assessment". | FIXED: null. |
| B | minor | `metadata.difficulty_description`, `.difficulty_rationale` | "normal MRI", "2 required tools". | FIXED: rewritten. |
| E | minor | `ground_truth.avoided_actions[*].rationale` | Em dashes. | FIXED: reworded. |

## Changes, in one paragraph a physician can read before re-reviewing

A 32-year-old woman with 3 years of premenstrual attacks of a sensory march (fingertips to face over 15-25 min) followed by a contralateral headache, normal examination. The aura is now usually left-sided and occasionally right-sided, so it is not side-locked and needs no imaging. The structured history output is this patient's own assessment (single sensory modality, so criterion C is 5 of 6, no red flag, facial heaviness without weakness). Literature blocks (template, verdicts, "WHO category 3-4", an empty "diary" search) are gone; the drug check is optional with a real sumatriptan review. Musts: clinical diagnosis without imaging; sumatriptan at headache onset with naproxen or paracetamol and an antiemetic; a headache and menstrual diary; perimenstrual frovatriptan, zolmitriptan or naproxen only if acute treatment fails; UKMEC 4 counselling. The PFO and WMH red herrings (data absent) are replaced by the real facial-heaviness red herring.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: "migraine aura" in the G43.109 group (plan section 5.1).
- To the lead: the side-locked aura (always the same side) occurs in S01 and S02 and may recur in other typical cases; plan 1.2 lists it as an imaging red flag.

## Open questions for Andrea (judgment calls you could not settle)

- Decided: the side-locked aura was corrected in the history (aura usually left, occasionally right) rather than adding an MRI, to keep this the typical no-imaging case the July ruling intends.

## Verification
Adversarial verifier, 24 Oct 2026. Read the final case and the original HPI, red herrings and differential (`git show HEAD`).
- Checked: each own finding against the file (aura side varies in both HPI fields, succession false and C 5 of 6, onset at 29, PFO and WMH red herrings gone, empty diary search gone, `{"drug": ...}` alternatives, optional tiers, stop rule history only with max 0, perimenstrual frovatriptan 2.5 mg twice daily or zolmitriptan 2.5 mg two or three times daily as in NICE CG150, naproxen sodium 550 mg twice daily correctly attributed to `[Holland_2012]`, ICHD-3 menstrual window day -2 to +3). All hold.
- Found and changed: (1) the worker's new red herring and the structured history state "heaviness without weakness", but the HPI never said she had no weakness, so the claim the red herring rests on was not in the patient data. Added to both HPI fields: "but she has never had weakness of the face, arm or leg, speech difficulty or visual symptoms during an episode"; the structured history aura line now says "no weakness of the face, arm or leg in any attack". (2) The red herring raises hemiplegic migraine, which was not in the differential (ROUND_POLICY 7): added "Hemiplegic migraine (motor aura)", G43.409, very_low, with the excluding features. (3) `metadata.fallback_tool_kinds.specialized_test` removed (fallback is null).
- Checks after the edits: `perfect_agent.py -v` ok; `case_io.py check` clean for this case; guard tests pass.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x1, [ICHD_3] x3.
- synonyms re-derived (`apply_diagnosis_synonyms.py --prune`): "migraine aura" removed (its tokens are a subset of "migraine without aura", a wrong answer); "migraine with aura", "migraine with typical aura", "classic migraine" and G43.1, G43.119, G43.909 kept.
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.
