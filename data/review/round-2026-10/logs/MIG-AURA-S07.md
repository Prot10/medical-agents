# MIG-AURA-S07
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance (plan 1.3): structured ICHD-3 history required; no MRI, CSF, ECG, EEG, echo or labs in a typical case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.clinical_history.medications[Yasmin].indication` | "Acne and contraception — REQUIRES REVIEW": a hint at the answer in the patient block. | FIXED: "Acne and contraception". |
| B | minor | `patient.clinical_history.medications` | HPI says she also uses sumatriptan nasal spray 20 mg and ibuprofen or aspirin; the list had only rizatriptan and Yasmin. | FIXED: added sumatriptan nasal spray 20 mg (occasional) and over-the-counter ibuprofen or aspirin (when rizatriptan runs out). |
| A, D | major | `initial_tool_outputs.clinical_assessment` | Template (class A): HPI sentence copied three times, generic SNNOOP10 line, placeholder modality score. | FIXED: rewritten for her: 15 years, 2-3 attacks a month, right-field visual aura 20-30 min, left-sided headache, acute-medication days about 3-5 a month (no overuse), the pill recorded, examination, each SNNOOP10 flag; criteria_met unchanged (5 of 6, consistent); impression ICHD-3 1.2.1. |
| C, D | major | `followup_outputs[0]` (drug check) | Summary-only block, empty structured fields; "CRITICAL ACTION ... CONCLUSION" prescriptive voice repeating the expected text; WHO only, "4-6 fold" in one field and "6-9x" in key evidence. | FIXED (class C): structured output: interactions (pill with triptans none; drospirenone with NSAIDs; two triptans within 24 h; rizatriptan 5 mg with propranolol), contraindication UKMEC 4 / WHO MEC 4, warning with the six-fold risk (Champaloux 2017), progestogen-only and IUD alternatives with categories; trigger names Yasmin, ethinylestradiol, drospirenone, combined oral contraceptive. |
| A, C | major | `ground_truth.action_criteria[action-2-check-drug-interactions]` | `{"context": ...}` alternative, unattainable; `[AAN_2000]` and a duplicate key; expected evidence with "URGENT" and `[Sacco_2022]`. | FIXED: `{"drug": ...}` alternatives "Yasmin", the medication as written, "ethinylestradiol", "drospirenone", "combined oral contraceptive", "combined hormonal contraception"; tier required (plan 3.5); new label, rationale, expected evidence; citations emptied (UKMEC key pending CENTRAL). |
| C, D | major | `followup_outputs[1]` (literature, prevention) | Empty query; patient-specific conclusions ("Rizatriptan 10 mg is appropriate", "topiramate or erenumab preferred"); wrong facts (propranolol "40-120 mg BID", CGRP antibodies "first-line alternatives", the threshold "2 migraine days with significant disability" stated as the indication). | FIXED: general evidence with query set: AHS 2021 thresholds, Silberstein 2012 evidence levels, MHRA 2024 topiramate and valproate, Sacco 2022 CGRP. Kept as the only literature follow-up, last. |
| B | major | `followup_outputs[2]` (literature, WMH) | "3 small WMH in long-term migraineur": no MRI exists in the case. | FIXED: deleted (class E). |
| C | major | `ground_truth.action_criteria[action-1-search-medical-literature]` | Required literature step with a fixed query (ROUND_POLICY 5). | FIXED: optional, `{}`, last, out of the stop rule. |
| A, E | minor | `ground_truth.action_criteria[action-3-perform-clinical-assessment]` | Rationale equal to the label; generic expected evidence; free-text citation. | FIXED: patient-specific expected evidence and rationale; `["[ICHD_3]"]`. |
| C | major | `ground_truth.assessment.required_recommendations` | Diagnostic must ("Confirm ICHD-3 1.2 criteria"); vague acute must ("avoid running out"); preventive must cited `[Holland_2012]` (NSAIDs and complementary treatments); no rizatriptan-propranolol dose adjustment; WHO-only wording. | FIXED: five musts: stop Yasmin with switch options (UKMEC) and alternative acne care; acute plan (rizatriptan at headache onset, adequate supply, no sumatriptan within 24 h, triptan days under 10); offer prevention per AHS 2021 (propranolol with rizatriptan 5 mg, amitriptyline or candesartan); class Q topiramate text; CGRP antibody after oral failures `[Sacco_2022]`. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Ergot boilerplate (no ergot in list or plan); WHO-only pill wording. | FIXED: canonical UKMEC 4 prohibition (class I); ergot line deleted; two-triptan prohibition kept (she uses both). |
| D, E | minor | `ground_truth.key_clinical_evidence` | "July 2026 review applied end to end..." (class D); "6-9x" risk inconsistent with the drug output. | FIXED: three lines; risk stated as about six-fold, consistent with the drug output. |
| B | major | `ground_truth.red_herrings[1]` | WMH red herring with empty field path; no MRI in the case (class E). | FIXED: deleted. Red herring 1 kept, UKMEC wording. |
| B | minor | `ground_truth.differential` | MOH "should be quantified"; no ICD codes. | FIXED: MOH graded low with her acute-medication days against the ICHD-3 8.2 thresholds (G44.41); migraine without aura G43.009; TIA key features expanded. |
| A | minor | `fallback_tool_outputs.specialized_test`, `metadata.fallback_tool_kinds` | Fallback keyed "Neurodiagnostic assessment" (class M). | FIXED: null; kind entry removed. |
| C | minor | `ground_truth.stop_rule` | Literature in the stop rule. | FIXED: clinical assessment and drug check; max 0. |
| E | minor | `patient.history_present_illness`, `metadata`, avoided-action rationales | Pre-existing em dashes in untouched text. | FLAGGED, left unchanged (no churn). |

## Changes, in one paragraph a physician can read before re-reviewing
The patient block no longer flags the pill as "REQUIRES REVIEW", and her medication list now includes the sumatriptan spray and over-the-counter ibuprofen or aspirin the HPI describes. The ICHD-3 assessment is written for her (15 years, 2-3 attacks a month, 5 of 6 C characteristics, about 3-5 acute-medication days a month, no red flag). The pathway is the assessment, then a structured check of Yasmin (UKMEC and WHO MEC category 4 in migraine with aura, about six-fold stroke risk, no pill-triptan interaction, progestogen-only and IUD alternatives, rizatriptan 5 mg if propranolol is started), then an optional general literature search on prevention; the WMH search, with no MRI behind it, is gone. Musts: stop Yasmin and switch contraception; an acute plan with rizatriptan at headache onset and enough supply, no two triptans within 24 hours; offer prevention (propranolol with rizatriptan 5 mg, amitriptyline or candesartan); topiramate only under the pregnancy prevention programme; CGRP antibody after oral failures. Medication overuse is graded low by her actual days of use.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms (plan 5.1): drop "migraine aura" from the G43.109 group.
- Criteria pack (plan 5.3): add `[UKMEC_2016]`, `[WHO_MEC_2015]`, `[AHS_2021]`, `[Silberstein_2012]`, `[MHRA_topiramate_2024]`; literature and drug check no longer required.

## Open questions for Andrea (judgment calls you could not settle)
- None needing Andrea. Decided: two diagnostic label clauses ("critical pharmacovigilance issue ... WHO Category 4") kept unchanged per plan 5.4 (management clause, not wrong).

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the final case. Checked: medication list now matches the HPI; Champaloux 2017 (about six-fold risk) consistent between drug output and key evidence; Silberstein 2012 level A/B lists and Ailani 2021 thresholds in the literature output are correct; prohibitions consistent with musts; UKMEC wording canonical.
Found and fixed: (1) the prevention must and key evidence said that 2-3 severe attacks a month "reach the AHS 2021 threshold to offer" prevention; AHS 2021 offers at 3 days with severe disability and advises considering at 2, so both now say so (`ground_truth.assessment.required_recommendations[2]`, `ground_truth.key_clinical_evidence[2]`). (2) The CGRP must ("after two or more oral preventives") disagreed with S09, where the same condition applies NICE's three failed preventives to a UK patient; it now gives both (EHF 2022 after two; NICE funding after three with at least 4 migraine days a month), with the same wording in S07 and S10, consistent with S09 (`required_recommendations[4]`).
Checks run after my edits: `perfect_agent.py -v` passes (the clinical assessment shows `<- ?` as in every MIG-AURA case: the initial output is served, the source lookup only fails on null fields), `case_io.py check` clean for the case, `test_case_guards.py -k` 2 passed.

## Condition audit
Condition auditor, 24 Oct 2026 (uniformity pass over all 30 MIG-AURA cases).
- `ground_truth.assessment.required_recommendations[2]`: candesartan was offered to a woman who can become pregnant without the pregnancy caution that M06, P03 and S04 carry (candesartan is fetotoxic). Added "(only with reliable contraception, as it is contraindicated in pregnancy)", so the class Q cautions read the same across the condition.

After the edit: `perfect_agent.py` 30/30, `case_io.py check` clean for the condition, `test_case_guards.py -k MIG-AURA` 60 passed.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x1, [ICHD_3] x3.
- UKMEC 2016 -> UKMEC 2025 citation text x1.
- CGRP must: EHF 2022 lists CGRP antibodies as a first-line option (the 'after two failed oral preventives' rule was the 2019 EHF guideline); the NICE threshold is no longer cited to [Sacco_2022].
- synonyms re-derived (`apply_diagnosis_synonyms.py --prune`): "migraine aura" removed (its tokens are a subset of "migraine without aura", a wrong answer); "migraine with aura", "migraine with typical aura", "classic migraine" and G43.1, G43.119, G43.909 kept.
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.
