# FND-S10
Reviewer status: R1 not reviewed, R2 not reviewed (no FND notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search[...]` | Summary and only finding were the criterion's `expected_evidence`; leak guard failed (plan baseline). | FIXED: canonical motor-only output (plan B, without the LaFrance and Goldstein rows); literature criterion `optional`, last. |
| A | major | `ground_truth.action_criteria` | Template tiers (literature and drug `recommended`, MRI `optional`), labels equal rationales, template citation strings. | FIXED (plan 3.2): exam (required), MRI `action-4` (recommended, `{contrast: false}`), drug check (optional), new `action-neuropsych-battery` (optional), literature (optional). |
| A | minor | `ground_truth.sequence_constraints`, `stop_rule` | None; exam only. | FIXED: soft exam -> MRI; `required_before_assessment` exam; max 0. |
| B | minor | `patient.neurological_exam.motor` | Hoover sign stated without the weakness of left hip extension on direct testing; em dash. | FIXED: left hip extension weak on direct testing, full strength during right hip flexion against resistance; distractible arm weakness kept. |
| E | minor | `patient.neurological_exam.additional` | Repeated the history ("Entire episode witnessed by roommate...") inside the examination. | FIXED: removed; face, tongue and speech findings kept. |
| C | major | `initial_tool_outputs.clinical_assessment` | Meta keys; midline splitting counted among 4 rule-in signs; impression leak "No further investigation is required...". | FIXED (plan H): library keys; 3 validated signs (Hoover, distractibility, dragging gait); midline split and normal walking when unobserved supportive; canonical impression. |
| B | major | `initial_tool_outputs.mri` | "with and without contrast ... no abnormal enhancement" with a non-contrast criterion (plan I). | FIXED: non-contrast report with DWI/ADC and SWI; motor-pathway pertinent negatives kept. |
| D | minor | `initial_tool_outputs.drug_interactions` | Medication list only, with the leak warning. | FIXED (plan C): "No clinically significant interactions among the current medicines." |
| C | major | `ground_truth.assessment` | Template musts and prohibitions (plan D). | FIXED: DX (left hemiparesis), COMM, PHYSIO, PSY (social anxiety disorder); prohibitions P1, P2, P3, P7. |
| C | major | `ground_truth.differential` | Template MS ("young adult"), structural ("effectively excludes") and autoimmune encephalitis ("normal EEG background": no EEG in the case) rows. | FIXED (plan F): one row, acute ischemic stroke including cervical artery dissection or TIA `low` (face and tongue spared, positive signs, normal reflexes, no restricted diffusion); the others are not raised by a sudden hemiparesis without prior episodes and were deleted. |
| D | major | `ground_truth.key_clinical_evidence` | Template items with the composition leak. | FIXED: four case-specific items. |
| C | minor | `ground_truth.red_herrings` | Generic data points. | FIXED: social anxiety and past anorexia; onset after the dissertation call with the visa at stake; pallor at onset with HR 104 (new, cardiac distractor). |
| C | minor | `ground_truth.avoided_actions[*]` | `[Stone_2018]`, generic rationales. | FIXED (plan L): same 7 waste ids, `[Espay_2018]` / `[Stone_2016]`, patient-specific rationales. |
| D | minor | `fallback_tool_outputs` | Specialized-test, advanced-imaging, drug and literature stubs; Holter impression "only benign findings" without naming them. | FIXED (plan G): stubs nulled and removed from `metadata.fallback_tool_kinds`; Holter impression names the brief asymptomatic sinus tachycardia. |
| E | minor | `metadata.notes`, `difficulty_rationale`, `revision_reason` | Template; "supportive normal labs" with no labs. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing
The examination is the required act and counts three validated signs of a functional left hemiparesis: Hoover sign (with the weak direct hip extension now stated), left arm weakness that improves from 2/5 to 4/5 during an arithmetic task, and a dragging monoplegic gait; sensory loss stopping at the midline and normal walking when unobserved are supportive only. One non-contrast MRI with DWI is recommended for the stroke question of a sudden hemiparesis in a young woman and is reported as a normal non-contrast study. The differential is now the one alternative the presentation raises, stroke including dissection or TIA, `low` with case reasons. Musts: positive diagnosis, explanation, FND physiotherapy, psychological therapy treating her social anxiety; prohibitions P1-P3 and P7. Literature and drug-check outputs no longer echo the scoring key.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms (plan 5.2): this motor-only case still accepts "psychogenic non-epileptic seizures", "PNES", "functional seizures" and F44.5.

## Open questions for Andrea (judgment calls you could not settle)
- None.

## Checks
- `perfect_agent.py FND-S10 -v`: ok; exam and MRI receive the stored clinical assessment and non-contrast MRI (verified through the environment).
- `case_io.py check FND-S10`: schema and synonym guard OK; the leak failure that named S10 is gone; the only remaining condition failure names FND-P08 (another worker's case).
- `test_case_guards.py -k FND-S10`: pass.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case against the plan (section 4 S10) and PATTERNS.md.
- Confirmed: Hoover wording with weak direct hip extension; three validated signs, sensory midline split and unobserved walking supportive; non-contrast MRI with DWI; one stroke or dissection row `low`; musts DX, COMM, PHYSIO, PSY (social anxiety) and prohibitions P1-P3, P7 as planned; Holter fallback names its incidental finding; diagnosis unchanged.
- Found and fixed: `key_clinical_evidence[1]` claimed that face and tongue sparing with normal reflexes "does not fit a hemiparesis from a single brain lesion", an overstatement (face can be spared by some brain lesions and reflexes are often normal two days after a stroke). Rewritten as a supportive feature that does not by itself exclude a brain lesion.
- Checks after my edits: `perfect_agent.py -v` ok (each required and recommended call served by the case's own stored report, not a fallback; the "<- ?" source label is a dump-format artefact, confirmed by executing the calls through the environment); `case_io.py check` schema and synonym guard OK, no test failure names the case; `test_case_guards.py -k` pass; discriminator guard (FND not yet enabled) run by hand: clean.
