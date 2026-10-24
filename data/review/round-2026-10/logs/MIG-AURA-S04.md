# MIG-AURA-S04
Reviewer status: no reviewer notes for MIG-AURA (R1 and R2 never reviewed this condition) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance for migraine_with_aura, applied below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `followup_outputs[1].output` (drug, plan S04, class C) | Claimed propranolol raises sumatriptan levels about 70% by CYP2D6 and told to reduce sumatriptan to 25-50 mg: wrong (the 70% rise and the 5 mg limit are for rizatriptan; sumatriptan needs no change). Summary-only block with "SAFE" verdict. | FIXED: structured check: propranolol with sumatriptan no interaction and no dose change, the rizatriptan limit stated as such; contraindications of propranolol, sumatriptan (uncontrolled hypertension) and candesartan (pregnancy); warnings (propranolol adverse effects and pregnancy, BP checks, timing); alternatives candesartan, metoprolol, amitriptyline; sources SmPC and Silberstein 2012. |
| C | major | `followup_outputs[0]`, `[2]` (literature, class B) | Literature with empty `query`, "CONCLUSION" for this patient, a demographic "Black women" search with patient verdicts, overstated Level A claims for metoprolol and dual indication. | FIXED: both deleted; literature criterion optional, answered by the library. |
| B | major | `initial_tool_outputs.clinical_assessment` (class A) | HPI sentences copied (the "Headache relation" line was the HPI's first sentence), generic SNNOOP10 line, placeholder modalities. | FIXED: per-element findings including disability (2-3 severe days a month), triggers, codeine intolerance, hypertension and BP; red flags named and absent; impression ICHD-3 1.2.1.1. |
| B | minor | `patient.history_present_illness`, `patient.hpi` | Unilateral aura marked true while the aura was described only as central spreading outward; "She had hypertension" (past tense) contradicts the PMH (current stage 1); no onset date for the hypertension although the red herring said the aura history predates it. | FIXED: aura spreads "into one side of her vision (either side)", headache "usually left-sided"; "She has stage 1 hypertension, diagnosed by her PCP last year and managed with lifestyle modification". |
| A | major | `ground_truth.action_criteria[action-2]` (class C) | `{"context": ...}` unattainable; required without a real interaction; expected evidence mentioned SSRIs she does not take. | FIXED: `{"drug": ...}` alternatives propranolol, sumatriptan, candesartan, metoprolol; optional (plan table); rewritten. |
| A | minor | `ground_truth.action_criteria[action-1]` (rule 5), `stop_rule`, citations (class N) | Literature required and first; stop rule with literature and drug check; duplicate and free-text citations. | FIXED: literature optional, `{}`, last; stop rule history only, max 0; one key per source. |
| C | major | `ground_truth.assessment.required_recommendations` (class N) | Preventive must cited `[Holland_2012]` (NSAID and complementary treatments) for propranolol; no dose, no contraindication check; vague BP must; no acute-plan or contraception must. | FIXED: propranolol with starting dose, titration and checks (asthma, bradycardia or block, depression) citing `[Silberstein_2012]`, candesartan only with reliable contraception; sumatriptan continued (up to 100 mg) with antiemetic; BP review with the uncontrolled-hypertension limit; triggers and diary; UKMEC 4 counselling. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` (class I) | Ergot boilerplate; "new-onset HTN" wording (it is not new-onset); non-canonical combined-pill text. | FIXED: ergot deleted; canonical UKMEC 4 prohibition; "do not attribute the attacks to her hypertension"; added "do not withdraw sumatriptan because of controlled stage 1 hypertension" (plan S04) and "no codeine-containing analgesics" (documented intolerance). |
| E | minor | `ground_truth.red_herrings[1]` (class E) | Duplicate of red herring 0 with empty paths. | FIXED: deleted; red herring 0 states that the hypertension began years after the aura. |
| B | minor | `ground_truth.differential` | Hypertensive headache and PRES key features vague; em dash. | FIXED: ICHD-3 hypertensive-crisis threshold and timing; PRES features absent. |
| D | minor | `ground_truth.key_clinical_evidence` (class D) | "July 2026 review" line. | FIXED: deleted; AHS 2021 preventive threshold added. |
| C | minor | `ground_truth.avoided_actions[avoid-waste-3]` (class N) | PFO rationale cited `[Charles_2017]`. | FIXED: citation removed; trials named. |
| A | minor | `fallback_tool_outputs.specialized_test` (class M) | Junk fallback "general_neurodiagnostic_assessment". | FIXED: null. |
| B | minor | `metadata.difficulty_description`, `.difficulty_rationale` | "normal MRI", "drug interaction with sumatriptan", "2 required tools". | FIXED: rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

A 35-year-old nurse with 7 years of typical visual aura followed by severe headache, now 2-3 disabling attacks a month with double shifts, stage 1 hypertension on lifestyle measures (128/78 today), sumatriptan 50 mg effective, codeine intolerance. The false propranolol-sumatriptan interaction (a rizatriptan fact) is gone from the drug check, which is now optional and structured; both literature follow-ups (patient verdicts, a demographic search) are gone. The structured history is this patient's own and documents the 2-3 severely disabling days a month that justify prevention. Musts: clinical diagnosis without imaging; propranolol with dose, titration and contraindication checks, candesartan only with reliable contraception; sumatriptan continued with an antiemetic and no dose change; BP review; triggers and diary; UKMEC 4 counselling. Prohibitions: combined hormonal contraception; attributing the attacks to hypertension; withdrawing sumatriptan for controlled stage 1 hypertension; codeine.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: "migraine aura" in the G43.109 group (plan section 5.1).
- Citation key `[Silberstein_2012]` used in a must per plan section 1.1 (CENTRAL to add to the criteria pack allow-list).

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the final case.
- Checked: each own finding against the file (false sumatriptan-propranolol interaction gone, rizatriptan fact stated as such, hemifield in the HPI, hypertension in the present tense and dated last year, so "6 years before the hypertension" is correct, propranolol must with dose and checks cited to `[Silberstein_2012]`, candesartan with contraception, codeine prohibition consistent with the allergy, BP 128/78 consistent everywhere, `{"drug": ...}` alternatives, optional tiers, stop rule history only with max 0). All hold.
- Found and changed: (1) the key evidence said 2-3 severely disabling days "meet the AHS 2021 threshold to offer" prevention; AHS 2021 says consider at 2 and offer at 3 or more severely disabling days. Key evidence and the preventive must now state both thresholds (the must keeps "Offer", justified by 3 days and the rising frequency). (2) The red herring "Stage 1 hypertension (128/78 today)" pointed at `patient.vitals`, which holds only the numbers; it now points at `patient.history_present_illness`, which contains the whole datum. (3) `metadata.fallback_tool_kinds.specialized_test` removed (fallback is null).
- Checks after the edits: `perfect_agent.py -v` ok; `case_io.py check` clean for this case; guard tests pass.

## Condition audit
Condition auditor, 24 Oct 2026 (uniformity pass over all 30 MIG-AURA cases).
- `ground_truth.differential[0]` (migraine without aura): `icd_code` null set to G43.009, as in S06 to S11.

After the edit: `perfect_agent.py` 30/30, `case_io.py check` clean for the condition, `test_case_guards.py -k MIG-AURA` 60 passed.
