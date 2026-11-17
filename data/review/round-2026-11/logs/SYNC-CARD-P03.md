# SYNC-CARD-P03

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-8-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: split initial_tool_outputs.mri (off-pathway normal study, no MRI criterion): the plain copy (contrast_used false) drops "No abnormal enhancement after gadolinium administration" and its impression now reads "Normal brain MRI. No structural intracranial abnormality identified."; the unchanged gadolinium study (contrast_used true, trigger request_contrast_mri) moved to the end of the pathway, since brain MRI is not part of the syncope work-up (ESC 2018, Class III). No criterion changed.
- MRI-CONTRAST verified: plain initial copy free of gadolinium content with consistent impression, gadolinium copy unchanged (contrast_used true) at the end of the pathway, no MRI criterion (syncope, plain appropriate); mri_probe: plain, contrast and both orders in either sequence answered by the case (never the library), case fallback MRI consistent; no other field changed against 393c547e; perfect_agent -v passes. No error found in the case; removed the two duplicate copies of the worker's MRI-CONTRAST log line.

## Reviewer notes
Reviewer status: R2 needs_changes (avoided_actions, stopping) | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| b3858fff-ed27-4a73-a159-0bf4d163974f | FIXED | ground_truth.assessment.required_recommendations[7]: "Advise no driving until treated; after ICD implantation the Group 1 restriction follows national licensing rules (ESC 2018 syncope Practical Instructions: 1 month after an ICD)". The unsourced "about 3 months (ESC 2018)" is gone (plan C5, D8). |
| 1e6f0501-ce23-49a8-8896-da4a2ebdef5c | ALREADY-FIXED | Class MRI-CONTRAST, commit 71517e55: initial_tool_outputs.mri is the plain study (contrast_used false, plain impression); followup_outputs[7] is the gadolinium study (contrast_used true). Re-checked with mri_probe.py: plain, contrast and both orders in either sequence are answered by the case's own studies. |
| NB-87M:SYNC-CARD-P03:policy_verdict | FIXED | ground_truth.action_criteria[3] (action-3-order-echocardiogram): importance recommended -> required. Label: "Transthoracic echocardiogram to exclude structural heart disease (induced type 1 pattern)". Rationale cites ESC 2022 IIa C (no other heart disease), citations + [ESC_2022_VA_SCD]. ground_truth.stop_rule.required_before_assessment: + action-3-order-echocardiogram (plan C6, D14). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | ground_truth.avoided_actions (new avoid-waste-exercise-echo) | The case fallback echo is an exercise echo. An exercise-echo order had no label, while the exercise test is waste because the events are febrile, not exertional (class C3, D4). | FIXED: waste entry {order_echocardiogram, echo_type exercise_echo}, with the exercise test's rationale and citation. |
| B | minor | metadata.difficulty_rationale | Said "2 required actions"; there are now 3 (ECG, TTE, telemetry). | FIXED |
| B | minor | followup_outputs order | The gene panel (recommended) came after the drug check. | FIXED: the order is now TTE, telemetry, cardiac MRI, gene panel, paracetamol check, then the off-pathway sodium-channel-blocker challenge, exercise test and gadolinium MRI. |
| C | minor | dataset-generation/criteria_packs/SYNC-CARD.md sec.2/7 (Brugada TTE tier) | The pack lists TTE as recommended for Brugada. With an induced pattern it must be required. | FLAGGED: CENTRAL C3 (lead). |

## Changes
The transthoracic echocardiogram is now a required step, and the agent must obtain it before submitting a diagnosis. Here the type 1 Brugada pattern appeared only with fever, and ESC 2022 (IIa C) accepts Brugada syndrome from an induced pattern only when no other heart disease is present, so excluding structural disease is part of the diagnosis. The driving must no longer attributes "about 3 months" to ESC 2018. It now says no driving until treated, and after the ICD the Group 1 restriction follows national licensing rules, citing the ESC 2018 syncope Practical Instructions (1 month after an ICD). The brain MRI header contradiction was already resolved by the November MRI split: the plain study is served first and the gadolinium study separately. An exercise echo order, which the case answers with a deferred-study report, is now labelled waste, like the exercise test (fever-related, not exertional events). In the pathway list the gene panel now comes before the paracetamol check. The difficulty note now counts three required actions. The diagnosis, the other criteria, the reports and the differential are unchanged. The perfect-agent check passes.

## Verification
perfect_agent.py -v passes (each criterion receives the stored report carrying its expected evidence); case_io.py check: schema OK, synonym guard OK, no test failure names the case; test_case_guards.py -k <id> passes. mri_probe.py re-run (MRI not edited): plain and gadolinium orders answered by their own studies.

Pass 1: 0 errors found
- Checked: b3858fff driving text matches plan C5 (P03 text); 1e6f0501 ALREADY-FIXED (plain initial MRI, gadolinium study last); verdict FIXED (TTE required, TTE-only argument, in the stop rule, ESC 2022 IIa C rationale); exercise echo waste mirrors the exercise test entry; no patient-text leakage of the echo; difficulty count 3 required; perfect_agent -v, test_case_guards -k and case_io check. Nothing changed.

Pass 2: 0 errors found
- Pass 1 found 0 errors and no condition-audit or orchestrator change follows it, so nothing was left unverified. Re-ran perfect_agent.py -v (passes) and test_case_guards.py -k (passes). Nothing changed.
Pass 4: 0 errors found
- No change after the last 0-error pass. perfect_agent.py -v passes; test_case_guards.py -k (64 tests for the 8 SYNC-CARD pass-4 cases) passes. Nothing changed.
