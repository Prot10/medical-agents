# MIG-AURA-P04
Reviewer status: R1 none, R2 none (no reviewer notes for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input applied is the July 2026 tool guidance for `migraine_with_aura` (structured ICHD-3 history required; MRI for red flags; CSF, ECG, EEG and routine echo removed; CADASIL testing kept as an explicit question) and ROUND_POLICY. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `ground_truth.assessment.required_recommendations`, `ground_truth.key_clinical_evidence` | "confirmed first-degree relative" while the only affected relative is a maternal aunt (second-degree) (plan 4, P04). | FIXED: musts and pearls now say second-degree with a prior risk of up to 25%; the pedigree is stated in the assessment and a red herring. |
| D | major | `patient.hpi`, `patient.history_present_illness`, `patient.chief_complaint` | Timeline leak: the HPI quoted the outside radiologist ("anterior temporal poles and external capsules, CADASIL-pattern") while the MRI is a criterion, and stated the GP had ordered NOTCH3 testing (testing before counselling; plan class O); chief complaint "CADASIL screen ordered". | FIXED: she was told the MRI "showed some small white spots" and brought the images; the GP asked whether she should be tested and no test has been sent; the aunt's NOTCH3 variant is now documented in the family history (c.457C>T p.(Arg153Cys)); disability per attack stated; chief complaint "asking whether she should be tested for CADASIL". |
| C | major | `initial_tool_outputs.mri` | Formal read showed left external capsule and right temporal pole lesions and concluded "borderline CADASIL pattern; NOTCH3 gene testing required" (Kind 1: test prescription); structured findings mixed regions. | FIXED (plan): formal review of the outside study: five punctate deep frontal subcortical foci sparing the U-fibres; normal anterior temporal poles, external capsules, basal ganglia, thalami, pons; no lacunes or microbleeds; impression states the pattern is not that typically seen in CADASIL (imaging-level statement). |
| C | major | `followup_outputs` NOTCH3 | A "variant of uncertain significance ... classified as benign" contradicted "excluded"; free-text report in one finding; `test_type` "genetic_panel" did not match the criterion. | FIXED: `genetic_panel:CADASIL`; exons 2-24 with copy-number analysis negative; the aunt's familial variant not detected; VUS removed. |
| C | major | `followup_outputs` genetic counselling, `action` none | Counselling filed as `order_specialized_test` (class O), placed after the result, and stating "children have NO CADASIL risk" as a test output. | FIXED: follow-up deleted; must "Offer genetic counselling before NOTCH3 testing, covering implications for relatives and the option not to test" placed first; the family implications (children not at risk once negative; mother and maternal relatives still at risk) are a separate must. |
| D | major | `initial_tool_outputs.literature_search`, `initial_tool_outputs.drug_interactions["general"]` | Guard leaks: the literature template and the drug summary repeated the criteria's expected evidence; `[Holland_2012]` misused. | FIXED: initial literature block removed; drug block rewritten as a `sumatriptan` check: no desogestrel interaction; topiramate and POP; valproate, topiramate and candesartan in pregnancy planning; EAN 2020 triptan advice in confirmed CADASIL only; sumatriptan pregnancy registry; NSAIDs from 20 weeks; CGRP antibodies; propranolol or low-dose amitriptyline. |
| A | major | `action-2-check-drug-interactions` | `{"context": ...}` alternative (class C). | FIXED: `{"drug": "sumatriptan"}`, `{"drug": "propranolol"}`; optional (plan; no current interaction changes management). |
| C | major | `followup_outputs` literature (4) | Empty WMH follow-up; patient-level verdicts ("triptans are appropriate", "propranolol safest"); unreferenced "CADASIL management guidelines; EHF guidelines". | FIXED: all deleted; one literature follow-up with Mancuso M et al., Eur J Neurol 2020;27:909-927 and O'Sullivan M et al., Neurology 2001;56:628-634, last. |
| A | major | `action-1-search-medical-literature`, stop rule | Required literature step in the stop rule. | FIXED: optional, `{}`, last; stop rule `[action-3, action-5]`, allowance 1. |
| C | major | `ground_truth.assessment` | Musts were tests (MRI review, NOTCH3 testing, class J), "counselling regardless of result" after the test, no pregnancy-related management although she plans a pregnancy; ergot prohibition without an ergot (class I). | FIXED: counselling before testing; explain the negative result and non-specific WMH; family implications; acute treatment in pregnancy (paracetamol first, sumatriptan acceptable, no NSAIDs from 20 weeks); prevention at 2-3 disabling attacks a month with propranolol or low-dose amitriptyline and a diary. Prohibitions: canonical CHC (UKMEC 4), no valproate, topiramate or candesartan while planning pregnancy, no serial MRI surveillance; ergot line deleted. |
| C | major | `ground_truth.differential` | CADASIL "moderate" after a negative NOTCH3 (class F); "Migraine without aura" entry for the labelled entity's sibling. | FIXED: CADASIL low with the genetic and MRI results; MS and sporadic SVD very low with specific reasons; migraine without aura entry removed. |
| B | major | `ground_truth.red_herrings` | Entries with empty `field_path`; one cited "external capsule and anterior temporal pole WMH" that the corrected MRI no longer shows; 50% risk framing for a second-degree relative. | FIXED: three entries with real paths (family history; MRI findings; mother's headaches in the HPI) and pedigree-correct risk. |
| D | minor | `ground_truth.key_clinical_evidence` | Two July 2026 engineering sentences (class D). | FIXED: deleted; four case pearls. |
| C | minor | `avoid-waste-3-order-echocardiogram` | `[Charles_2017]` cited for PFO (class N). | FIXED: rationale names PREMIUM, PRIMA, MIST; citation removed pending trial keys. |
| A | minor | citations, MRI arguments, order, constraints | Duplicate and free-text citations; MRI `{"contrast": false, "protocol": "standard"}`; literature first; no constraints. | FIXED: one key or none; MRI `{}`; order history, MRI review, NOTCH3, drug, literature; soft constraints history before MRI and MRI before NOTCH3 (plan 3.3). |
| A | minor | `fallback_tool_outputs` | Advanced-imaging fallback keyed "MRA" (not vocabulary); drug fallback "agent not specified" (class M). | FIXED: set to null. Holter, echo, EEG, CT and CSF fallbacks are correct normal reports and stay. |
| E | minor | `metadata.condition_name`, `difficulty_description`, `difficulty_rationale` | "borderline MRI findings" no longer matches the case. | FIXED: rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing
34-year-old woman with 6 years of migraine with typical visual aura (2-3 disabling attacks a month), whose maternal aunt has genetically confirmed CADASIL; she is planning a second pregnancy. The HPI no longer quotes a CADASIL-pattern radiology report or says NOTCH3 testing was already ordered: she brings an outside MRI for review and asks whether to be tested. The formal MRI review shows five punctate deep frontal foci with normal temporal poles and external capsules. Counselling now precedes testing (a must, no longer a fake test), and the NOTCH3 result is clean: no cysteine-altering variant in exons 2-24 and the aunt's p.(Arg153Cys) absent, with the contradictory VUS removed. Musts: counselling before testing, explain the result and that her children are not at risk while her mother remains at risk, acute treatment through pregnancy, prevention with propranolol or low-dose amitriptyline. The pedigree is second-degree throughout (prior risk up to 25%); CADASIL is low in the differential.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Allow-list: `[EAN_CADASIL_2020]`, `[AHS_2021]`, `[UKMEC_2016]`, `[MHRA_topiramate_2024]`, trial keys (named in text only here).

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. No reviewer notes exist for MIG-AURA. Checked: the pedigree is second-degree everywhere (family history, assessment, musts, pearls, red herring) with a prior risk of up to 25%; the HPI no longer quotes a CADASIL-pattern report or says NOTCH3 was ordered; the aunt's variant NOTCH3 c.457C>T p.(Arg153Cys) is nomenclature-consistent (codon 153, exon 4, cysteine-altering) and the result reports it absent with no VUS; counselling is a must, not a test (class O); MRI review shows sparing of temporal poles and external capsules in findings and impression; O'Sullivan 2001 and Mancuso 2020 citations real and correctly summarised; CADASIL low after the negative test; musts and prohibitions agree on pregnancy-safe prevention (no valproate, topiramate or candesartan; propranolol or low-dose amitriptyline) and on continuing sumatriptan once CADASIL is excluded; the MRA waste avoided action matches no criterion; perfect agent and guards pass.
Found: nothing requiring a change. No edit made.

## Condition audit
Condition auditor, 24 Oct 2026 (uniformity pass over all 30 MIG-AURA cases).
- `metadata.case_body_concerns[0]`: stale authoring note "check_drug_interactions (only fallback)", untrue since the drug check now has its own stored output; removed, as P08, P09, RM11 and RS11 had already done (metadata only, not shown to the agent).

After the edit: `perfect_agent.py` 30/30, `case_io.py check` clean for the condition, `test_case_guards.py -k MIG-AURA` 60 passed.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x2, [ICHD_3] x2.
- synonyms re-derived (`apply_diagnosis_synonyms.py --prune`): "migraine aura" removed (its tokens are a subset of "migraine without aura", a wrong answer); "migraine with aura", "migraine with typical aura", "classic migraine" and G43.1, G43.119, G43.909 kept.
- VASCERN 2023 replaces an unverified EAN 2020 attribution in the drug-check output ("expert recommendations advise against triptans and other vasoconstrictors as first-line acute treatment" in confirmed CADASIL) and in its sources line.
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
