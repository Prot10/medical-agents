# MIG-AURA-S10
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance (plan 1.3): structured ICHD-3 history required; no MRI, CSF, ECG, EEG, echo or labs in a typical case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C, B | major | `patient.history_present_illness`, `patient.hpi`, `patient.clinical_history.social_history.note` | "MIDAS 18/27 (Grade IV)": MIDAS grade IV is a score of 21 or more (18 is grade III), and MIDAS has no maximum of 27. The label (`accepted[0]`, "MIDAS grade IV") could not be derived from the data. | FIXED: the data, not the label: MIDAS 24 (grade IV, severe disability) in both HPI fields and the social history; plausible for 2-4 attacks a month of 8-16 hours with missed school days. |
| D | major | `initial_tool_outputs.literature_search` | ICHD-3 template whose finding and summary equal the literature criterion's expected evidence (guard failure). | FIXED: set to null. |
| A, D | major | `initial_tool_outputs.clinical_assessment` | Template (class A): HPI sentences copied twice, generic SNNOOP10 line, placeholder modality score. | FIXED: rewritten (7 years, 2-4 attacks a month, visual aura 20-25 min alternating sides, headache 8-16 h with vomiting, MIDAS 24, acute-drug days about 4-6, no preventive tried, examination, each SNNOOP10 flag); criteria_met unchanged (5 of 6, consistent). |
| C, D | major | `followup_outputs` (two literature blocks) | Both empty (`query` "", `summary` ""); one about WMH, which this case does not contain. | FIXED: both deleted (plan S10). The library answers an optional search. |
| C, D | major | `followup_outputs` (topiramate drug check) | Summary-only; patient conclusion ("partner vasectomy = effective contraception, topiramate acceptable and safe"), contrary to the topiramate pregnancy prevention programme; obsolete FDA "Category D". | FIXED (class C): structured output for propranolol, candesartan, amitriptyline and topiramate against sumatriptan and paracetamol: interactions, contraindications (asthma and heart block; pregnancy; PPP), side effects; trigger names the four drugs. |
| A, C | major | `ground_truth.action_criteria[action-2-check-drug-interactions]` | `{"context": ...}` alternative, unattainable; required without a concrete interaction; `[Holland_2012]`/`[Sacco_2022]` in the expected evidence. | FIXED: recommended (plan 3.5), `{"drug": ...}` for topiramate, propranolol, candesartan, amitriptyline; new label, rationale, expected evidence; citations emptied. |
| C | major | `ground_truth.action_criteria[action-1-search-medical-literature]` | Required literature with a fixed query (ROUND_POLICY 5). | FIXED: optional, `{}`, last, out of the stop rule. |
| A, E | minor | `ground_truth.action_criteria[action-3-perform-clinical-assessment]` | Rationale equal to the label; generic expected evidence; free-text citation. | FIXED: patient-specific; `["[ICHD_3]"]`. |
| C | major | `ground_truth.key_clinical_evidence[0]`, `ground_truth.differential[1]`, `metadata.difficulty_rationale` | "attacks reaching the chronic-migraine threshold", "chronic-borderline migraine with WMH distractor": 2-4 attacks a month is episodic, and there is no WMH or MRI in the case. | FIXED: key evidence states episodic migraine with severe disability; chronic migraine graded very low with the attack count; difficulty rationale rewritten. |
| C | major | `ground_truth.assessment.required_recommendations` | Diagnostic must ("Confirm ICHD-3 ... quantify headache days"); preventive must naming topiramate first without the pregnancy prevention programme (class Q); vague acute must; `[Sacco_2022]` on the first-line must. | FIXED: five musts: diagnosis; start prevention (propranolol MR 80-160 mg with contraindications checked, or candesartan or amitriptyline) with review at 8-12 weeks; class Q topiramate text; acute plan with an NSAID or paracetamol and an antiemetic for her vomiting, adequate supply, triptan days under 10; CGRP antibody after oral failures `[Sacco_2022]`. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Ergot boilerplate; PFO prohibition with no PFO question in the case (class I); non-canonical pill wording. | FIXED: canonical UKMEC 4 combined-contraception prohibition; valproate prohibition (class Q); ergot and PFO lines deleted. |
| D, E, C | minor | `ground_truth.key_clinical_evidence` | "July 2026 review applied end to end..." (class D); PFO line citing `[Charles_2017]` (class N), not about this case. | FIXED: three patient-specific lines. |
| B | minor | `ground_truth.differential` | MOH and chronic migraine "quantify ..." without the quantity; no ICD codes. | FIXED: graded with her days of headache and acute medication; G43.009, G44.41. |
| A | minor | `fallback_tool_outputs.specialized_test`, `metadata.fallback_tool_kinds` | Fallback keyed "Neurodiagnostic assessment" (class M). | FIXED: null; kind entry removed. |
| C | minor | `ground_truth.stop_rule` | Literature and drug check in the stop rule. | FIXED: clinical assessment only; max 0. |
| E | minor | `patient.chief_complaint`, `patient.pmh`, avoided-action rationales | Pre-existing em dashes in untouched text. | FLAGGED, left unchanged (no churn). |

## Changes, in one paragraph a physician can read before re-reviewing
The MIDAS score is now 24 (grade IV), which is what the label states; the old "18/27, grade IV" was not a valid MIDAS result. The case describes episodic migraine with typical aura (2-4 severe attacks a month), not "chronic-borderline" migraine, and the WMH and PFO references, which had no data, are gone. The ICHD-3 assessment is written for her. The pathway is the required assessment, then a recommended check of the candidate preventives (propranolol, candesartan, amitriptyline, topiramate) against her medicines; the two empty literature blocks and the template literature output are removed. Musts: start prevention (propranolol MR, or candesartan or amitriptyline), topiramate only with highly effective contraception under the pregnancy prevention programme, an acute plan with an antiemetic for her vomiting and adequate supply, and a CGRP antibody after oral failures. Prohibitions: combined hormonal contraception and valproate.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms (plan 5.1): drop "migraine aura" from the G43.109 group.
- Criteria pack (plan 5.3): add `[AHS_2021]`, `[MHRA_topiramate_2024]`, `[UKMEC_2016]`, `[Silberstein_2012]`.

## Open questions for Andrea (judgment calls you could not settle)
- None needing Andrea. Decided: whether a partner's vasectomy satisfies the topiramate pregnancy prevention programme depends on her circumstances, so the case no longer asserts it does; the musts name propranolol, candesartan or amitriptyline first and give topiramate only under the canonical class Q condition.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the final case. Checked: MIDAS 24 is grade IV (21 or more) and is stated identically in both HPI fields, the social history, the assessment and the label; the two empty literature follow-ups and the template initial literature block are gone; chronic migraine and MOH graded by her day counts; drug output contradicts nothing in `patient` (no contraception other than partner vasectomy, sumatriptan and paracetamol only).
Found and fixed: (1) the prevention must asserted "(no asthma, depression or bradycardia)" although the case never records asthma or depression status; now "(after checking for asthma, depression and bradycardia)" (`required_recommendations[1]`). (2) CGRP must harmonised with S07 and S09: EHF 2022 after two failed oral preventives, NICE funding after at least three with at least 4 migraine days a month (`required_recommendations[4]`); she is a UK patient.
Checks run after my edits: `perfect_agent.py -v` passes (the clinical assessment shows `<- ?` as in every MIG-AURA case: the initial output is served, the source lookup only fails on null fields), `case_io.py check` clean for the case, `test_case_guards.py -k` 2 passed.

## Condition audit
Condition auditor, 24 Oct 2026 (uniformity pass over all 30 MIG-AURA cases).
- `ground_truth.assessment.required_recommendations[1]`: candesartan was offered to a woman who can become pregnant without the pregnancy caution that M06, P03 and S04 carry (candesartan is fetotoxic). Added "(only with reliable contraception, as it is contraindicated in pregnancy)", so the class Q cautions read the same across the condition.

After the edit: `perfect_agent.py` 30/30, `case_io.py check` clean for the condition, `test_case_guards.py -k MIG-AURA` 60 passed.
