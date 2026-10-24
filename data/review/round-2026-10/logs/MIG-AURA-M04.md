# MIG-AURA-M04
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MIG-AURA) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance (structured ICHD-3 history required, MRI for red flags only, EEG removed), applied through the condition plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `initial_tool_outputs.clinical_assessment.criteria_met` | `at_least_one_unilateral_aura_symptom: true` and `two_or_more_aura_symptoms_in_succession: true` although the visual aura is bilateral from the start, dysarthria and vertigo are not lateralised, and the brainstem symptoms "accompany" the visual aura; the "5 of 6" count was therefore wrong. | FIXED: unilateral false, succession false, spread false; 3 of 6 (duration, positive symptom, headache), which still meets ICHD-3; brainstem keys added (`at_least_two_brainstem_aura_symptoms`, `no_motor_or_retinal_aura_symptoms`, `all_criteria_for_migraine_with_brainstem_aura_1_2_2_met`). |
| B | major | `initial_tool_outputs.clinical_assessment` (rest) | Template (class A): copied HPI sentences, generic red flags, placeholder modality score. | FIXED: one finding per ICHD-3 element with her data, the 1.2.2 brainstem count (dysarthria, vertigo, ataxia), examination today, SNNOOP10 line (brainstem aura and recent onset present), medicines; impression supports 1.2.2. |
| D | major | `initial_tool_outputs.mri.impression` | "No basilar artery stenosis, aneurysm, or posterior fossa AVM on MRA. Normal posterior circulation" inside a brain MRI report (class K); `findings` empty while the impression named WMH. | FIXED: vessel text removed; structured WMH finding; posterior fossa, craniocervical junction, DWI and SWI negatives. No vessel study added (plan: none for M04); the dissection entry in the differential now rests on the history and MRI, not on an MRA. |
| D | minor | `patient.clinical_history.medications` | Pill indication "REQUIRES REVIEW in context of migraine with aura"; ibuprofen indication "Migraine". | FIXED: "Contraception"; "Headache; partial relief". |
| A | major | `action-2-check-drug-interactions` | `{"context": ...}` criterion not sendable; one essay output for the pill with empty structured fields; expected evidence "TRIPTANS ARE CONTRAINDICATED". | FIXED (class C): action-2 is the pill check (nine `{"drug": ...}` alternatives: Rigevidon as written, ethinylestradiol spellings, combined oral contraceptive / hormonal contraception), required, answered by `followup_outputs[0]` (UKMEC 4 / WHO MEC 4 in any aura subtype, topiramate warning, alternatives). The triptan question is a new recommended criterion `action-check-triptan-brainstem-aura` (nine triptan names) answered by `followup_outputs[1]` (label exclusion in brainstem and hemiplegic aura, ergots, NSAID plus antiemetic, gepants). Split so that a triptan check alone cannot satisfy the required contraception check. |
| C | minor | `followup_outputs[2]` (new) | A propranolol or other preventive query had no case answer and was served the pill report. | FIXED: preventive-options drug output (propranolol, amitriptyline, topiramate, candesartan: interactions with her medicines, contraindications, cautions, pregnancy restrictions). Not a criterion. |
| C | major | `assessment.required_recommendations` | "Brain MRI/MRA required" must (class J); garbled "topiramate, propranolol contra-indicated only if asthma [Holland_2012]" (class N: Holland 2012 does not cover these drugs); no acute plan beyond "avoid triptans". | FIXED: musts: stop Rigevidon with named alternatives; explanation and reassurance (brainstem aura, not basilar insufficiency or tumour); NSAID at adequate dose plus antiemetic, no triptans or ergots; prevention because brainstem aura recurs (AHS 2021) with amitriptyline or propranolol (asthma and depression checked), review at 8-12 weeks; class Q topiramate text. |
| C | minor | `assessment.prohibited_recommendations` | Separate triptan and ergot lines; non-canonical pill line. | FIXED: one triptan/ergot line specific to brainstem aura (class I keeps it); canonical pill line; new valproate line (woman who can become pregnant, class Q). |
| C | major | `ground_truth.differential` | Posterior circulation TIA "moderate" at assessment time (class F); dissection "MRA to exclude" with no MRA; vestibular migraine reasoning vague. | FIXED: TIA very low with features; vestibular migraine low with the ICHD-3 precedence reason (appendix A1.6.6); posterior fossa lesion and dissection very low from history and MRI. |
| B | minor | `ground_truth.red_herrings` | Two of three entries with empty `field_path`; one cited a "normal posterior circulation MRA". | FIXED: all four entries with real paths (chief complaint, HPI twice, MRI finding); MRA claim removed. |
| D/E | minor | `key_clinical_evidence` | Two engineering sentences (class D); "contraindicated due to theoretical vasoconstriction" overstated. | FIXED: five lines from this case. |
| A | major | `action-1-search-medical-literature`, literature follow-ups | Required literature step in stop rule; queries as slugs; the preventive block concluded "Initiate topiramate 25 mg/day" for this patient. | FIXED: optional, `{}`, last; the preventive block deleted; one follow-up (`followup_outputs[3]`) with the ICHD-3 1.2.2 definition and comments only. |
| A | minor | `fallback_tool_outputs.specialized_test`, `metadata.fallback_tool_kinds` | Junk fallback (class M). | FIXED: null. Holter, CSF, CT and EEG fallbacks are correct normal reports and stay. |
| C | minor | `action-3`, `action-4` | Template labels; MRI arguments too narrow; duplicate and free-text citations. | FIXED: case-specific; MRI `{}`, recommended. |
| C | major | `sequence_constraints`, `stop_rule` | None; literature in stop rule, max 0. | FIXED: soft history-before-MRI; stop rule action-3 and action-2, max 1. Order: history, MRI, pill check, triptan check, literature. |
| E | minor | `avoided_actions[1]`, `[2]` rationales, `metadata.difficulty_rationale` | Em dashes; rationale said "brainstem aura requires MRI/MRA". | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 33-year-old woman on Rigevidon has had three attacks in four months of bilateral visual aura with vertigo, ataxia and slurred speech followed by an occipital migrainous headache. The label (migraine with brainstem aura, 1.2.2) is unchanged. The structured history now counts the C characteristics correctly: the aura is bilateral and the brainstem symptoms accompany rather than follow the visual aura, so only duration, the positive symptom and the headache count (3 of 6, still enough), with three brainstem symptoms and no motor or retinal symptoms. The MRI (recommended) no longer reports an MRA. The contraception check (required) and a separate triptan check (recommended) are orderable by drug name and give real content. Musts: stop Rigevidon and switch; explain and reassure; NSAID plus antiemetic, no triptans or ergots; offer prevention for recurrent brainstem aura (amitriptyline or propranolol with the cautions checked; topiramate only with highly effective contraception). Posterior circulation TIA is now very low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `diagnosis_synonyms.yaml` G43.109 group: drop "migraine aura" (plan 5.1). Consider a "migraine with brainstem aura" / "basilar-type migraine" synonym for this case's code group, which today accepts only the generic migraine-with-aura labels.
- Criteria pack allow-list: `[UKMEC_2016]`, `[WHO_MEC_2015]`, `[AHS_2021]`, `[AHS_neuroimaging_2020]`, `[MHRA_topiramate_2024]`.

## Open questions for Andrea (judgment calls you could not settle)

None. The plan named propranolol as the preventive; amitriptyline is listed first alongside it because older reports raised a theoretical concern about beta-blockers in brainstem aura and she has untreated anxiety; both are acceptable and the must is checkable either way.

## Verification

Adversarial verifier, 24 Oct 2026. Checked: the corrected 3-of-6 count against the HPI (bilateral from the start, brainstem symptoms accompanying the visual aura), the 1.2.2 brainstem count, MRI report, split of the pill check (required) and triptan check (recommended) with their triggers, the preventive drug output, literature text against the ICHD-3 1.2.2 comments, musts (propranolol cautions, topiramate class Q, valproate prohibition), vestibular migraine appendix code A1.6.6, red-herring paths, sequence direction, stop rule. Every log claim holds. No reviewer notes exist for this case.

Found and fixed:
- `followup_outputs[1].output.interactions[0]`: "no pharmacokinetic interaction with triptans" overstated (oral contraceptives raise zolmitriptan and frovatriptan levels). Now "no clinically relevant interaction with triptans".

`perfect_agent.py -v` ok, `case_io.py check` clean for the case, guard tests pass.

## Condition audit
Condition auditor, 24 Oct 2026 (uniformity pass over all 30 MIG-AURA cases).
- `followup_outputs[1].output.warnings` (triptan check) was empty (class C asks for filled structured fields). Added two warnings: AHS 2021 notes emerging observational data on triptan safety in brainstem aura while the label restriction stands (plan 1.2), and no triptan within 24 hours of an ergot. Summary and contraindications unchanged.

After the edit: `perfect_agent.py` 30/30, `case_io.py check` clean for the condition, `test_case_guards.py -k MIG-AURA` 60 passed.


## Close-out (24 Oct 2026)

Condition close-out (plans/MIG-AURA-decisions.md). Changes and reasons:

- citations [AAN_2000] -> [AHS_neuroimaging_2020] x2, [ICHD_3] x3.
- UKMEC 2016 -> UKMEC 2025 citation text x1.
- UKMEC 2016 -> UKMEC 2025 citation text x1.
- synonyms: generic and typical-aura labels removed (brainstem aura is ICHD-3 1.2.2, not typical aura, and the triptan decision depends on it); "migraine with brainstem aura", "basilar migraine", "basilar type migraine" added. The primary code G43.109 still credits a code-only generic answer (ICD-10-CM has no brainstem-aura code).
- Citation [AAN_2000] retired: Silberstein 2000 covers treatment, not neuroimaging; imaging statements now cite Evans 2020 [AHS_neuroimaging_2020], test-waste statements [ICHD_3] (diagnosis is clinical).
Checks after the change: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MIG-AURA-` 60/60.
