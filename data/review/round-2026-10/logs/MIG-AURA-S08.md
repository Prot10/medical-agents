# MIG-AURA-S08
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance (plan 1.3): structured ICHD-3 history required; no MRI, CSF, ECG, EEG, echo or labs in a typical case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `patient.history_present_illness`, `patient.hpi` | "takes no medications" while the HPI and the list record as-needed ibuprofen. | FIXED: "takes no regular medications" in both fields. |
| A, D | major | `initial_tool_outputs.clinical_assessment` | Template (class A): HPI sentences copied twice, generic SNNOOP10 line, placeholder modality score. | FIXED: rewritten for her (8 years, 1-2 attacks a month, visual aura of about 25 min with side varying between attacks, headache 4-8 h, triggers, ibuprofen use, normal fundi, each SNNOOP10 flag incl. no side-locking and no nocturnal waking); criteria_met unchanged (5 of 6, consistent); impression ICHD-3 1.2.1. |
| C, D | major | `followup_outputs` (triptan literature) | Empty query; patient-specific conclusion ("Sumatriptan 100 mg first-line ... preventive therapy borderline given 1-2/month"); "80% of patients respond" unsupported. | FIXED: general evidence with query set: NICE CG150 combination acute therapy, Bates 1994 and Olesen 2004 (triptan during the aura does not prevent the headache). Moved last. |
| C | minor | `followup_outputs` (trigger literature) | Empty query, patient conclusion; "validated" app claim unsupported. | FIXED: deleted (plan class B, one literature follow-up kept). The diary and trigger advice is a must. |
| C, D | major | `followup_outputs` (drug check) | Summary-only block with empty structured fields; conclusion voice; repeated the expected text. | FIXED (class C): structured output (ibuprofen no interaction; triptan contraindications listed and none recorded for her; timing, adverse effects, overuse threshold, SSRI counselling; alternatives); first follow-up. |
| A, C | major | `ground_truth.action_criteria[action-2-check-drug-interactions]` | `{"context": ...}` alternative, unattainable; required without a concrete interaction; `[AAN_2000]` duplicate keys; `[Holland_2012]` in expected evidence. | FIXED: optional (plan 3.5: triptan start with no interacting drug), `{"drug": ...}` for sumatriptan, rizatriptan, zolmitriptan; new label, rationale, expected evidence; citations emptied. |
| C | major | `ground_truth.action_criteria[action-1-search-medical-literature]` | Required literature step with a fixed query (ROUND_POLICY 5). | FIXED: optional, `{}`, last, out of the stop rule. |
| A, E | minor | `ground_truth.action_criteria[action-3-perform-clinical-assessment]` | Rationale equal to the label; generic expected evidence; free-text citation. | FIXED: patient-specific; `["[ICHD_3]"]`. |
| C | major | `ground_truth.assessment.required_recommendations` | Diagnostic must ("Confirm ICHD-3 1.2 criteria"); unspecific triptan must without timing. | FIXED: four musts: diagnosis without imaging; oral triptan (sumatriptan 50-100 mg) at headache onset, not during the aura, with ibuprofen, repeat dose rule; diary, triggers, under 10 triptan days, review and prevention only if attacks increase (1-2 a month is below the AHS 2021 thresholds, class P); contraception counselling with UKMEC categories. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Ergot boilerplate (no ergot); non-canonical pill wording. | FIXED: canonical UKMEC 4 prohibition (woman of reproductive age, class I); ergot line deleted. |
| D, E | minor | `ground_truth.key_clinical_evidence[2]` | "July 2026 review applied end to end..." (class D). | FIXED: three patient-specific lines. |
| B | major | `ground_truth.red_herrings[0]` | "Episodic monocular visual symptoms" (her symptoms are hemifield, not monocular), "brain MRI normal" (no MRI in the case), empty field path. | FIXED: rewritten to the real datum (her attribution to an eye problem and the normal ophthalmology review), field path `patient.history_present_illness`. |
| B | minor | `ground_truth.differential` | Hemicrania entry "no indomethacin trial yet but features atypical"; migraine without aura no code. | FIXED: hemicrania excluded by attack duration, pain-free intervals, alternating side, no autonomic features; G43.009 added; tension-type wording tightened. Likelihoods unchanged. |
| C | minor | `ground_truth.avoided_actions[avoid-waste-3-order-echocardiogram]` | `[Charles_2017]` cited for PFO (class N). | FIXED: trials in the rationale text; citation `[AAN_2000]`. |
| A | minor | `fallback_tool_outputs.specialized_test`, `metadata.fallback_tool_kinds` | Fallback keyed "Neurodiagnostic assessment" (class M). | FIXED: null; kind entry removed. |
| C | minor | `ground_truth.stop_rule` | Literature and drug check in the stop rule. | FIXED: clinical assessment only; max 0. |
| E | minor | `patient.chief_complaint`, `metadata`, avoided-action rationales | Pre-existing em dashes in untouched text. | FLAGGED, left unchanged (no churn). |

## Changes, in one paragraph a physician can read before re-reviewing
The ICHD-3 assessment is written for her (8 years, 1-2 attacks a month, 5 of 6 C characteristics, normal fundi, no red flag). The only required step is that assessment; the triptan check (no interaction with ibuprofen, no vascular contraindication) and a general literature search on acute treatment are optional. Musts: migraine with typical aura without imaging; start an oral triptan such as sumatriptan 50-100 mg at headache onset, not during the aura, with ibuprofen if needed; a diary with triggers and acute-drug days, triptan days under 10 a month, review in 3 months and prevention only if attacks increase; contraception counselling (combined methods UKMEC 4). The red herring now points at her real eye-clinic history instead of a monocular symptom and an MRI that do not exist.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms (plan 5.1): drop "migraine aura" from the G43.109 group.
- Criteria pack (plan 5.3): add `[NICE_CG150]`, `[UKMEC_2016]`; literature and drug check no longer required.

## Open questions for Andrea (judgment calls you could not settle)
- None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the final case. Checked: Bates 1994 (Neurology 44:1587) and Olesen 2004 (Eur J Neurol 11:671) exist and say what they are cited for; sumatriptan repeat-dose rule (2 hours) matches the SmPC; the drug check is correctly optional; stop rule only the assessment; differential consistent with the history.
Found and fixed: the red herring's correct interpretation called the aura "a homonymous arc", a finding the case never establishes (she describes peripheral lights on either side; no monocular testing is recorded). Reworded to "an arc of flickering light in one hemifield" (`ground_truth.red_herrings[0].correct_interpretation`).
Checks run after my edits: `perfect_agent.py -v` passes (the clinical assessment shows `<- ?` as in every MIG-AURA case: the initial output is served, the source lookup only fails on null fields), `case_io.py check` clean for the case, `test_case_guards.py -k` 2 passed.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x1, [ICHD_3] x3.
- synonyms re-derived (`apply_diagnosis_synonyms.py --prune`): "migraine aura" removed (its tokens are a subset of "migraine without aura", a wrong answer); "migraine with aura", "migraine with typical aura", "classic migraine" and G43.1, G43.119, G43.909 kept.
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.
