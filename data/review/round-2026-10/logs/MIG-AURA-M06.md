# MIG-AURA-M06
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance (structured ICHD-3 history required, MRI for red flags only, echo and monitoring removed), applied through the condition plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.clinical_assessment.criteria_met` | `not_better_accounted_for_by_another_diagnosis: false` while concluding migraine with aura; `each_symptom_lasts_five_to_sixty_minutes...: true` although the last aura lasted 70-75 minutes (class A). | FIXED: D true; C3 false; count 4 of 6 (spread, unilateral, positive, headache), which still meets 1.2; `all_criteria_for_migraine_with_typical_aura_1_2_1_met` true. |
| B | major | `initial_tool_outputs.clinical_assessment` (rest) | Template: HPI sentences copied three times, generic red flags, placeholder modality score. | FIXED: one finding per ICHD-3 element with her durations (30, 50, 70-75 minutes), acute treatment history, examination, SNNOOP10 line (aura over 60 minutes, recent onset, lengthening: present), medicines; impression supports 1.2.1 with one prolonged aura. |
| D/B | major | `initial_tool_outputs.mri` | "Normal MRA" inside a brain MRI report (class K); impression said "single punctate" hyperintensity while the structured finding said "bilateral". | FIXED: vessel text removed; finding is a single right frontal punctate focus; occipital cortex and optic radiations reported normal on DWI, ADC, T2 and FLAIR (relevant because DWI may pseudonormalise by three weeks; FLAIR would still show an infarct). No vessel study added (plan). |
| C | major | `ground_truth.differential[0]`, `key_clinical_evidence[0]` | Migrainous infarction cited as "ICHD-3 1.4.1" (that is status migrainosus; it is 1.4.3); "normal DWI rules it out" at three weeks. | FIXED: 1.4.3, excluded by DWI and FLAIR of the left occipital cortex; persistent aura (1.4.2) very low; TIA very low; occipital seizure very low with phenomenology; occipital AVM/structural lesion added very low. |
| D | minor | `patient.clinical_history.medications[0].indication` | "CONTRAINDICATED in migraine with aura" stated the answer. | FIXED: "Dysmenorrhoea and contraception". |
| A | major | `action-2-check-drug-interactions` | `{"context": ...}` criterion not sendable; expected evidence mixed the pill, preventive "topiramate or propranolol [Holland_2012]" (class N) and triptan timing; output called low-dose pill "WHO Category 4" with speculative mechanism text. | FIXED (class C): action-2 = pill check (ten `{"drug": ...}` alternatives, desogestrel deliberately not one because the safe alternative is a desogestrel POP), answered by `followup_outputs[0]` (category 4 at any oestrogen dose, alternatives with categories, LNG-IUS for dysmenorrhoea, lamotrigine and topiramate interactions). New recommended `action-check-preventive-with-rizatriptan` answered by `followup_outputs[1]` (propranolol raises rizatriptan exposure, use 5 mg; topiramate, candesartan, lamotrigine, valproate cautions). |
| C | major | `assessment.required_recommendations` | "Brain MRI with DWI" must (class J); preventive must cited `[Holland_2012]` with no agent; no plan for her dysmenorrhoea after stopping the pill. | FIXED: musts: stop Gedarel 20, switch without a gap, preferably to an LNG-IUS (treats dysmenorrhoea); rizatriptan at headache onset, not during aura; prevention because the aura lengthens (AHS 2021) with named options and the rizatriptan 5 mg rule for propranolol, review at 8-12 weeks (class P); class Q topiramate text; safety-net for an aura over an hour. |
| C | minor | `assessment.prohibited_recommendations` | Ergot boilerplate (class I); "Do not take triptans during the aura phase" (ineffective, not harmful). | FIXED: deleted (timing is in a must); canonical pill prohibition; valproate prohibition (class Q). |
| A | major | `action-1-search-medical-literature`, literature follow-ups | Required literature step; three blocks with vague sources ("AAN/EAN guidelines; Neurology review", "Headache journals"); topiramate "Level A for aura"; iron/ferritin block with no ferritin in the case; prolonged-aura block whose `trigger_action` started with `check_`. | FIXED: optional, `{}`, last; preventive and iron blocks deleted; one follow-up (`followup_outputs[2]`) with ICHD-3 (1.2, 1.4.2, 1.4.3) and Lampl et al., JNNP 2005. |
| B | minor | `ground_truth.red_herrings` | Third entry duplicated the first; second had empty `field_path`; "normal DWI" reasoning. | FIXED: three entries with real paths (HPI, `medications[0]`, MRI finding). |
| D/E | minor | `key_clinical_evidence` | Two engineering sentences (class D). | FIXED: five lines from this case. |
| A | minor | `fallback_tool_outputs.specialized_test`, `metadata.fallback_tool_kinds` | "general_laboratory_panel" fallback (class M). | FIXED: null. |
| C | minor | `avoided_actions` echo entry | `[Charles_2017]` for PFO (class N). | FIXED: rationale names PREMIUM, PRIMA, MIST; citation removed; dashes replaced in two rationales. |
| C | minor | `action-3`, `action-4` | Template labels; MRI arguments narrow; duplicate and free-text citations. | FIXED: case-specific; MRI `{}`, recommended (aura over 60 minutes). |
| C | major | `sequence_constraints`, `stop_rule` | None; literature in stop rule, max 0. | FIXED: soft history-before-MRI; stop rule action-3 and action-2, max 1. Order: history, MRI, pill check, preventive check, literature. |
| B | minor | `metadata.difficulty_description` | "triptans contraindicated during aura". | FIXED: "ineffective during the aura". |

## Changes, in one paragraph a physician can read before re-reviewing

A 31-year-old woman on Gedarel 20 has had three attacks in eight months of unilateral visual aura lasting 30, 50 and then 70-75 minutes, each followed by migrainous headache. The label is unchanged. The structured history now applies ICHD-3 correctly: the last aura fails the 5-60 minute criterion but four other characteristics are met, so this is still migraine with typical aura; the previous output both concluded 1.2.1 and marked "not better accounted for" false. The MRI (recommended) shows a normal occipital cortex on DWI and FLAIR three weeks later and a single punctate frontal hyperintensity; the MRA sentence is gone. Migrainous infarction is now coded 1.4.3 (not 1.4.1) and very low. The pill check (required) states that a 20 microgram pill is still category 4 and points to the LNG-IUS, which also treats her dysmenorrhoea; a recommended preventive check gives the rizatriptan 5 mg rule with propranolol. Musts: stop the pill and switch; rizatriptan at headache onset; offer prevention for the lengthening aura; topiramate only with highly effective contraception; urgent review for an aura over an hour.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `diagnosis_synonyms.yaml` G43.109 group: drop "migraine aura" (plan 5.1).
- Criteria pack allow-list: `[UKMEC_2016]`, `[WHO_MEC_2015]`, `[AHS_2021]`, `[AHS_neuroimaging_2020]`, `[MHRA_topiramate_2024]`, `[PREMIUM_2017]`, `[PRIMA_2016]`, `[MIST_2008]`.

## Open questions for Andrea (judgment calls you could not settle)

None. Note on the plan: it calls prevention "indicated" for M06. At three attacks in eight months the AHS 2021 frequency thresholds are not reached; prevention is offered here on the AHS "consider" ground for prolonged aura, with the escalating duration as the reason, and the must is worded "offer" accordingly.

## Verification

Adversarial verifier, 24 Oct 2026. Checked: the criterion D and C3 fixes against the HPI durations (30, 50, 70-75 minutes), migrainous infarction now 1.4.3 everywhere and persistent aura 1.4.2, MRI laterality (right-field aura, left occipital cortex normal), pill and preventive drug outputs (rizatriptan 5 mg with propranolol per label), literature sources (ICHD-3; Lampl et al., JNNP 2005), musts, prohibitions, red-herring paths, sequence direction, stop rule. Every log claim holds. No reviewer notes exist for this case.

Found and fixed:
- `ground_truth.differential[4]` (occipital AVM): key features said "aura on alternating sides", which nothing in the case states (only the headache side differs between attacks). Rewritten to what the case shows: fully reversible attacks, headache that has changed side, no flow voids, haemorrhage or mass on MRI.
- `assessment.required_recommendations[2]`: candesartan offered without the pregnancy caution that the case's own drug output gives for a woman who can become pregnant. Added "only with reliable contraception, as it is contraindicated in pregnancy".
- `followup_outputs[0].output.interactions[0]`: "no pharmacokinetic interaction" with combined oral contraceptives overstated; now "no clinically relevant interaction".

`perfect_agent.py -v` ok, `case_io.py check` clean for the case, guard tests pass.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x2, [ICHD_3] x2.
- UKMEC 2016 -> UKMEC 2025 citation text x1.
- UKMEC 2016 -> UKMEC 2025 citation text x1.
- synonyms re-derived (`apply_diagnosis_synonyms.py --prune`): "migraine aura" removed (its tokens are a subset of "migraine without aura", a wrong answer); "migraine with aura", "migraine with typical aura", "classic migraine" and G43.1, G43.119, G43.909 kept.
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
