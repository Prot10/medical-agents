# FND-RM02
Reviewer status: no reviewer notes for FND (R1 and R2 never reviewed this condition) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input is the July 2026 tool guidance (plan 1.3), applied through the plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.action_criteria[action-4-analyze-brain-mri]` | Brain MRI optional with `{contrast: false, protocol: standard}` in an acquired esotropia referred to exclude intracranial pathology; the MRI tool has no default for `contrast`, so an order without it failed the criterion. | FIXED: recommended (plan I), alternative `{}`, rationale on brainstem, posterior fossa and Chiari causes of acquired esotropia; soft constraint exam -> MRI. |
| B | major | `initial_tool_outputs.mri` | Non-contrast criterion but the report gave "post_contrast: No enhancement" and "No leptomeningeal enhancement"; "perfusion-weighted imaging" reported in a routine study; no technique line; the 3 mm focus called "Incidental finding" while the impression said "Essentially normal". | FIXED: technique line (T1, T2, FLAIR, DWI/ADC, SWI, thin brainstem sections, no contrast), enhancement and perfusion statements removed, focus typed as a white matter hyperintensity, normal craniocervical junction and cisternal III, IV, VI; two-point impression naming the nonspecific focus. |
| D | major | `initial_tool_outputs.clinical_assessment` | Template shape: one sign cut from a sentence fragment, midline vibration splitting counted twice (3 signs); impression leak "No further investigation is required...". | FIXED: canonical shape; one rule-in sign (convergence spasm with miosis, `convergence_spasm_with_miosis: true` per plan H), variability, other cranial nerves, midline splitting as supportive only; finding-based impression. |
| B | minor | `patient.neurological_exam.additional`, `.sensory` | Midline vibration splitting stated twice; interpretive sentence "The pattern is inconsistent with a fixed cranial nerve palsy" in the exam. | FIXED: duplicate and interpretation removed from `additional` (kept in `sensory`); full abduction between episodes added to the cranial nerves, which the ophthalmology note already stated as full ductions. |
| C | major | `followup_outputs[1]` (drug check) | Sertraline + sumatriptan content held in a follow-up, with alternatives (a plan). | FIXED: deleted; the initial drug output gives the serotonergic pair as low risk at twice-monthly sumatriptan, the sulfonamide allergy as not relevant to sumatriptan; no alternatives. Criterion optional (plan). |
| D | major | `followup_outputs[0]` (literature) | Unverifiable convergence-spasm sources, and "MRI recommended in all cases" (policy text in a tool result). | FIXED: deleted; canonical motor literature output (Espay, Daum, Nielsen, Stone); criterion optional, last. |
| C | major | `ground_truth.differential` | Template MS, stroke, structural and autoimmune encephalitis rows; no ocular motor differential. | FIXED: acute acquired comitant esotropia or decompensated strabismus, sixth nerve palsy, ocular myasthenia (pupil constricts with the deviation), brainstem or posterior fossa lesion including Chiari, MS (single focus, no dissemination); all low. |
| C | major | `ground_truth.assessment` | Template musts (neuropsychology, video-EEG, duplicates) and prohibitions with long-term ASM and "per Stone 2018". | FIXED: M-DX (functional diplopia with convergence spasm), M-COMM addressing her MS concern, orthoptic assessment with convergence-relaxation exercises; P1, P2, P3, P7, no strabismus surgery. |
| E | major | `ground_truth.key_clinical_evidence` | Template items (Interim composition leak, OPTIONAL item, Stone 2018). | FIXED: five case-specific items. |
| B | minor | `ground_truth.red_herrings` | "Family history of epilepsy" (the family history says none); generic stress item. | FIXED: deleted; real items kept or added: aunt with MS, the 3 mm MRI focus, childhood strabismus surgery with screen time, adjustment disorder on sertraline. |
| B | minor | `patient.clinical_history.family_history` | "No family history of epilepsy or brain tumors" in a non-paroxysmal case fed the epilepsy red herring. | FIXED: "No family history of brain tumors". |
| E | minor | `ground_truth.avoided_actions[*]` | `[Stone_2018]`; generic rationales ("no role once positive functional signs..."), one with an em dash. | FIXED: `[Espay_2018]` / `[Stone_2016]` and patient-specific rationales (prior negative cardiac work-up, no papilledema, no limb deficit). |
| A | minor | `fallback_tool_outputs`, `metadata.fallback_tool_kinds` | Specialized test leak fallback, advanced_imaging `MRI_brain_functional`; echo without `echo_type`. | FIXED: specialized_test, advanced_imaging, drug and literature fallbacks nulled and removed from `metadata.fallback_tool_kinds`; echo `echo_type: TTE`. |
| E | minor | `metadata.difficulty_description`, `difficulty_rationale`, `revision_reason` | "Mildly elevated TSH as metabolic red herring" although the case has no labs; template rationale. | FIXED: rewritten without the TSH; case-specific rationale. |

## Changes, in one paragraph a physician can read before re-reviewing

A 29-year-old woman with childhood bilateral medial rectus recession, 10-12 hours a day of screen time and an aunt with MS has 3 weeks of intermittent distance diplopia. The examination is the required step: convergence spasm with miosis and accommodative effort on lateral gaze, alternating with normal motility and full abduction, is the single rule-in sign; midline vibration splitting is now supportive only. A non-contrast brain MRI is recommended to exclude a brainstem or posterior fossa cause; the report no longer mentions gadolinium or perfusion, shows a normal brainstem and craniocervical junction, and keeps a single 3 mm nonspecific frontal focus, now a red herring for MS. The medication review is optional (sertraline with occasional sumatriptan, low risk). Musts: positive diagnosis of functional diplopia, explanation that addresses her MS fear, and orthoptic assessment with convergence-relaxation exercises; strabismus surgery is prohibited. The differential is now ocular motor: decompensated strabismus or acute acquired comitant esotropia, sixth nerve palsy, ocular myasthenia, posterior fossa lesion, MS, all low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms (plan 5.2): this diplopia case accepts "psychogenic non-epileptic seizures", "PNES", F44.5 and the motor "functional weakness" labels; scope them out.
- Library: the `functional_neuro_signs` canonical `criteria_met` keys have no ocular sign; this case adds `convergence_spasm_with_miosis` (plan H). Add it to the library assessment if the key list is validated anywhere.

## Open questions for Andrea (judgment calls you could not settle)

None open. Decisions taken and their reasons:
- The 3 mm frontal focus is kept and declared a red herring rather than removed: a solitary punctate subcortical focus is common at 29 and tests whether the agent escalates to an MS work-up; it does not meet dissemination in space and cannot cause the diplopia.
- Ocular myasthenia and posterior fossa or Chiari lesions added to the plan's two differential rows: both are standard alternatives for variable acquired esotropia, and the case data (pupil constriction, full ductions, normal MRI posterior fossa) answer them.
- Drug check optional, as the plan says: the only pair is low risk and changes nothing in the plan.

## Verification

Adversarial check (24 Oct 2026) of the log against the case and against the pre-round version (`b8be2153^`). What I checked: the patient diff (epilepsy clause removed from the family history, the duplicated vibration splitting and the interpretive sentence removed, full abduction added, which matches the ophthalmology note of full ductions in the HPI); the MRI (non-contrast technique, no enhancement or perfusion statements, the 3 mm focus typed and named in the impression, posterior fossa and craniocervical junction normal) against the MRI criterion's expected evidence and the MS and posterior-fossa differential rows; the drug output against the medication list and the sulfonamide allergy; the musts (orthoptic assessment, no PHYSIO) against the prohibition on strabismus surgery; signs count 1 with `convergence_spasm_with_miosis`; every log claim marked FIXED.

Found and changed:
- `ground_truth.avoided_actions[avoid-waste-1-order-echocardiogram]` and `[avoid-waste-2-order-cardiac-monitoring]`: both said her palpitations and chest tightness "had a negative cardiac work-up"; the negative work-up was for a chest-pain episode 18 months ago, while the palpitations are of the past several months and were never investigated. Both rationales now say so without claiming the palpitations were worked up.
- `initial_tool_outputs.literature_search...summary`: same mismatch as in M09; replaced with a summary of the four rows returned.

Checks re-run after the changes: `perfect_agent.py -v` ok, `case_io.py check` clean for this case (schema, synonym guard, no failing test names it), `test_case_guards.py -k` passed. The diagnosis label, `icd_codes` and synonyms are unchanged from before the round; no new em dashes or `Stone_2018` strings.
