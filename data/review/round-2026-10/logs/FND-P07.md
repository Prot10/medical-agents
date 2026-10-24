# FND-P07
Reviewer status: no reviewer notes for FND (R1 and R2 never reviewed this condition) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input is the July 2026 tool guidance (plan 1.3), applied through the plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.action_criteria[action-4-analyze-brain-mri]` | MRI optional with `contrast: false, protocol: standard`, although a new left arm weakness at 61 is a stroke-mimic question the pack names. | FIXED: recommended, `{}` (any non-gadolinium order matches; see Open questions), rationale and expected evidence for this case; soft constraint exam -> MRI. |
| B | major | `patient.history_present_illness` | Timeline impossible: husband diagnosed 3 months ago, symptoms "about 1 month after" and yet a 4-week history "coinciding with her husband's diagnosis". | FIXED: onset about 2 months after the diagnosis, developing over 4 weeks; "coinciding" removed. |
| D | minor | `patient.history_present_illness` | HPI reported examination findings ("entrains to examiner-imposed rhythms", "suppressed by distracting tasks"). | FIXED: HPI now gives what she reports (faster, with action, lessens when absorbed, drags the leg); signs stay in the examination. |
| C | minor | `patient.neurological_exam.mental_status` | "MoCA 26/30 (mild impairment consistent with PD-MCI baseline)": 26/30 is within the normal range (MCI screening cut-off < 26). | FIXED: "MoCA 26/30." |
| D | major | `initial_tool_outputs.clinical_assessment` | Meta keys; findings were HPI fragments ("New: left leg dragging added."); leak "No further investigation is required...". | FIXED: canonical shape; 3 rule-in signs (entrainment, distractibility, dragging monoplegic gait); left arm strength and baseline parkinsonism recorded. |
| B | minor | `initial_tool_outputs.mri` | No technique; "Stable findings" with no comparison; the report reasoned about "acute left-sided symptoms". | FIXED: non-contrast technique line, no prior for comparison, no infarct or lesion in the right hemisphere or basal ganglia, age-appropriate volume loss (matching the CT fallback). |
| C | major | `followup_outputs[0]` (`levodopa_adjustment_pramipexole`) | Drug check used as a plan (rasagiline, "consider dopaminergic augmentation"). | FIXED: deleted; "Continue the dopaminergic regimen unchanged" is a must and escalation a prohibition. |
| C | major | `followup_outputs[1]` (`palliative_care_referral_husband`) | A referral disguised as a literature search, with an unverifiable PMID. | FIXED: deleted; carer support is in M-COMM. |
| D | major | `initial_tool_outputs` (literature, drug check) | No initial literature output (criterion recommended with the leaking expected evidence); no initial drug output. | FIXED: canonical motor literature output (plan 2B); drug output in report voice (no interacting pair; venlafaxine tremor, pramipexole somnolence and impulse control). Both criteria optional. |
| C | major | `ground_truth.assessment` | Template musts and prohibitions (neuropsychology "recommended", duplicates, "per Stone 2018"). | FIXED: M-DX (coexisting with PD), M-COMM with carer support, M-PHYSIO, M-PSY (depression and grief), continue dopaminergic regimen; P1 (naming DaTscan), P2, P3, P7, no dopaminergic increase. |
| C | major | `ground_truth.differential` | Template rows (structural "normal MRI effectively excludes", neuropathy "when obtained", autoimmune encephalitis, malingering with no incentive); PD progression, stroke and drug tremor absent. | FIXED: PD progression low, right hemisphere stroke or structural lesion low, venlafaxine or enhanced physiological tremor low. |
| E | major | `ground_truth.key_clinical_evidence` | Seven template items with the "Interim composition decision" and OPTIONAL leaks. | FIXED: five case-specific items. |
| B | minor | `ground_truth.red_herrings` | Generic psychiatric and stress items. | FIXED: established PD (progression anchoring), depression on venlafaxine, onset after the husband's diagnosis, each concrete. |
| C | minor | `ground_truth.avoided_actions` | No guard against a DaTscan, the classic over-investigation in a known PD patient. | FIXED: `avoid-waste-datscan` added; a case fallback DaTscan (abnormal, bilateral putaminal loss worse on the left) so the library cannot answer "normal" in a patient with PD. |
| A | minor | `ground_truth.avoided_actions[*]` | `[Stone_2018]`; generic rationales. | FIXED: `[Espay_2018]` / `[Stone_2016]`, patient-specific rationales. |
| B | minor | `fallback_tool_outputs.echo` | Findings name aortic sclerosis, impression names trace mitral regurgitation; no `echo_type`. | FIXED: impression names the aortic sclerosis; `echo_type: TTE`. |
| A | minor | `fallback_tool_outputs.specialized_test` | Leak "negative result is itself a harm", `test_type: ''`. | FIXED: nulled and removed from `metadata.fallback_tool_kinds`. |
| E | minor | `metadata.notes`, `difficulty_rationale`, `revision_reason` | Notes describe a DaTscan and accelerometry that are not in the case. | FIXED: rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

A 61-year-old woman with right-predominant Parkinson's disease for 6 years develops, over 4 weeks while caring for her terminally ill husband, a left 8-10 Hz action tremor that entrains and stops with distraction, left arm weakness and a dragging left leg. The required step is the examination (3 rule-in signs; parkinsonism and reflexes unchanged). A non-contrast brain MRI is now recommended for the new hemibody deficit and shows no lesion. The medication review is optional and names venlafaxine as a possible tremor contributor; the levodopa-adjustment and palliative-referral follow-ups were deleted. A DaTscan is now scored as waste. The HPI timeline was corrected (onset about 2 months after her husband's diagnosis) and the MoCA 26/30 is no longer called impaired. Musts: positive diagnosis of functional tremor and weakness coexisting with PD, explanation with carer support, specialist physiotherapy, psychological therapy and treatment of her depression, and no change to the dopaminergic regimen; prohibitions include increasing dopaminergic treatment for the functional tremor. The differential is PD progression, right hemisphere stroke and drug-induced tremor, all low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms (plan 5.2): this motor-only case accepts "psychogenic non-epileptic seizures", "PNES", "functional seizures" and F44.5.
- Library (`fallback_library.yaml`): the `DaTscan` library report is normal; any case with established Parkinson's disease needs a case fallback (added here) or the library answers a normal scan in a patient with PD.

## Open questions for Andrea (judgment calls you could not settle)

None open. Decisions taken and their reasons:
- MRI criterion `{}` instead of the plan's `{contrast: false}`: the tool has no schema default for `contrast`, so `{contrast: false}` fails an agent that orders an MRI without naming contrast, which is a correct order. Gadolinium without indication stays prohibited (P7).
- M-PSY added (the plan lists DX, COMM, PHYSIO): her treated depression and acute grief are a treatment target, which is the plan's own condition for M-PSY.
- `avoid-waste-datscan` and its DaTscan fallback are not in the plan; added because a DaTscan is the over-investigation this case invites.

## Verification

Adversarial check (24 Oct 2026) of the log against the case and against the pre-round version (`b8be2153^`). What I checked: the corrected timeline (husband diagnosed 3 months ago in the social history, onset about 2 months later, a 4-week history: consistent); MoCA 26/30 no longer called impaired; the DaTscan fallback laterality (right-predominant PD, so the left putamen is the more affected: correct) and that the MockServer serves it only for a `DaTscan` order (the discriminator guard applies, so FDG-PET and other modalities are not answered with it); `monitor_type` and `echo_type` values; "continue the dopaminergic regimen unchanged" against the prohibition on increasing it (consistent); the MRI criterion `{}` against P7 (gadolinium still prohibited); the exam -> MRI constraint; every log claim marked FIXED.

Found and changed:
- `patient.neurological_exam.coordination`, `initial_tool_outputs.clinical_assessment.findings[Distractibility]`, `ground_truth.key_clinical_evidence[0]`: the left arm ataxia "resolves with attention" contradicted the sign it was filed under (distractibility means the deficit improves when attention is drawn away). Changed to "resolves with distraction" in all three places.
- `initial_tool_outputs.literature_search...summary`: same mismatch as in M09 (summary claims video-EEG and antiseizure-taper evidence that none of the four motor rows carries); replaced with a summary of the rows returned.

Left as is: the left arm weakness (3/5) has no arm-specific rule-in sign; the functional diagnosis rests on the entraining, distractible tremor and the dragging monoplegic gait on the same side, which the M-DX must states. Checks re-run after the changes: `perfect_agent.py -v` ok, `case_io.py check` clean for this case (schema, synonym guard, no failing test names it), `test_case_guards.py -k` passed. The diagnosis label, `icd_codes` and synonyms are unchanged from before the round; no new em dashes or `Stone_2018` strings.

## Condition audit

2026-10-24, FND condition auditor.

- `action-neuropsych-battery.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-1-search-medical-literature.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.

## Close-out (24 Oct 2026)

Andrea's FND ruling of 24 Oct 2026 and the close-out decisions (`plans/FND-decisions.md`). What changed and why:

- Diagnosis synonyms scoped by phenotype (`diagnosis_synonyms.yaml` F44 entries; a label or code naming another presentation must not score): removed "psychogenic non-epileptic seizures", "PNES", "functional seizures"; added "functional limb weakness", "functional motor disorder", "functional tremor"; codes removed F44.5.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FND-` passes, now including the discriminator guard.
