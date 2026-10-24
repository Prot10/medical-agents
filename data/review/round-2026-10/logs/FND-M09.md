# FND-M09
Reviewer status: no reviewer notes for FND (R1 and R2 never reviewed this condition) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input is the July 2026 tool guidance (plan 1.3), applied through the plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `initial_tool_outputs.literature_search` | Summary and only finding were the criterion's `expected_evidence` (leak guard failed); source "Nielsen_2015" cited for a CBT claim. | FIXED: canonical plan 2B output, motor rows only (Espay 2018, Daum 2014, Nielsen 2024, Stone 2005); criterion optional, last, new expected evidence. |
| C | major | `ground_truth.action_criteria[action-4-analyze-brain-mri]` | MRI optional and `contrast: false, protocol: standard`, although a new deficit on natalizumab with JC index 2.8 must be imaged with gadolinium for relapse and PML. | FIXED: required, `{contrast: true}`, rationale cites McGuigan 2016 consensus; in the stop rule; soft constraint exam -> MRI. |
| B | major | `initial_tool_outputs.mri.findings[0].location` | Prior lesion placed in the "right corticospinal tract", which cannot cause her baseline right leg spasticity and hyperreflexia; no lesion for the right heel-shin ataxia. | FIXED: left corona radiata along the corticospinal tract and right middle cerebellar peduncle, plus periventricular and juxtacortical lesions. |
| B | minor | `initial_tool_outputs.mri` | Report gave no technique and did not say gadolinium was given, yet reported "no enhancing lesions". | FIXED: technique line (T1, T2, FLAIR, DWI/ADC, SWI, post-gadolinium T1), comparison, numbered impression with no PML features. |
| D | major | `patient.history_present_illness` | Editorial sentence "Natalizumab is the MS disease-modifying therapy with the highest PML risk"; duplicated sentences (4 years on natalizumab twice; "feels different" twice). | FIXED: commentary removed, JC index kept as a dated prior result ("routine check 3 months ago"), duplicates removed. |
| D | major | `initial_tool_outputs.clinical_assessment` | Meta keys in `criteria_met`; impression ended with the leak "No further investigation is required..."; non-anatomical sensory loss counted as a rule-in sign; "improvement with distraction" counted separately from the Hoover sign it restates. | FIXED: canonical shape (plan 2H); 2 rule-in signs (Hoover, dragging monoplegic gait); sensory loss and unobserved walking listed as supportive; unchanged MS baseline recorded. |
| B | major | `initial_tool_outputs.labs` | JC index (a prior result in the HPI) and a qualitative "natalizumab level" reported as new results; CMP, TSH and B12 as "Within reference range" with no unit; template `clinical_significance`. | FIXED: CBC, CMP, TSH and B12 with values, units and ranges (Hct 40.2 = MCV 89 x RBC 4.52 / 10, MCHC 33.3); stored WBC 6.4 and lymphocytes 1.4 kept; JC and drug-level rows removed. |
| C | major | `followup_outputs[0]` (`natalizumab_pml_risk_management`) | A drug check used as a management plan (switch options, dosing interval). | FIXED: deleted; the real content is now a must (refer PML risk to the MS team). |
| D | minor | `initial_tool_outputs.drug_interactions.general` | Empty block with the leak warning "...is a prescribing decision, not an output of this check". | FIXED: natalizumab PML boxed warning and concomitant-immunosuppressant note; lorazepam sedation and balance; no interaction. Criterion optional (plan section 4 overrides the table in 3.2). |
| C | major | `ground_truth.assessment` | Template musts (neuropsychology "recommended", two duplicates); prohibitions cite "per Stone 2018"; gadolinium prohibition contradicts the indicated contrast MRI. | FIXED: M-DX, M-COMM, M-PHYSIO and a natalizumab must; P1, P2, P3 and "treat as MS relapse with high-dose corticosteroids"; P7 removed. |
| C | major | `ground_truth.differential` | MS `moderate` after a stable MRI; template structural, neuropathy ("when obtained" EMG) and autoimmune encephalitis rows; malingering resting on an unperformed symptom-validity test; PML absent. | FIXED: MS relapse low, PML low, malingering low with the medical leave named; template rows deleted. |
| E | major | `ground_truth.key_clinical_evidence` | Seven template items including the "Interim composition decision" and "OPTIONAL" leaks and Stone 2018 claims. | FIXED: five case-specific items. |
| B | minor | `ground_truth.red_herrings` | Single generic psychiatric red herring. | FIXED: established MS (relapse anchoring), JC index (PML anchoring), anxiety on lorazepam. |
| A | minor | `ground_truth.avoided_actions[*]` | `[Stone_2018]` (non-existent key); generic rationales. | FIXED: `[Espay_2018]` / `[Stone_2016]`, patient-specific rationales; all kept as waste. |
| B | minor | `fallback_tool_outputs.ct.impression` | "no associated ... enhancement" on a non-contrast CT. | FIXED: "without mass effect or surrounding edema". |
| A | minor | `fallback_tool_outputs` | specialized_test, advanced_imaging (`MRI_brain_functional`) and literature fallbacks; echo without `echo_type`. | FIXED: three nulled and removed from `metadata.fallback_tool_kinds`; echo `echo_type: TTE`. |
| C | minor | `ground_truth.action_criteria` | No spine imaging considered for new leg weakness in MS. | FIXED: optional `action-spine-mri` (`order_body_imaging {study: spine_MRI}`), see Open questions. |
| A | minor | `ground_truth.action_criteria` | Labels equal rationales; "FND criteria pack - ..." citations. | FIXED: short labels, distinct rationales, sourced citations; optional neuropsychology criterion added (plan 3.2). |
| E | minor | `metadata.notes`, `difficulty_rationale`, `revision_reason` | Template text; "JC PCR mandatory for PML exclusion" is wrong with a stable MRI. | FIXED: rewritten for this case. |

## Changes, in one paragraph a physician can read before re-reviewing

The case is a 47-year-old woman with RRMS stable on natalizumab for 4 years (JC index 2.8) and 10 days of new right leg weakness. The required work-up is now the examination for positive signs (Hoover sign, dragging monoplegic gait; baseline spasticity, reflexes and ataxia unchanged) followed by a brain MRI with gadolinium, which is required because natalizumab raises two questions the examination cannot answer (a new or enhancing lesion, PML); the MRI shows a stable lesion load, no enhancement and no PML pattern. Laterality of the prior lesions was corrected (left corticospinal, right cerebellar peduncle) to fit her right-sided baseline signs. Blood tests, spine MRI, medication review, neuropsychology and literature are optional; the PML-risk "drug check" follow-up was deleted. Musts: positive diagnosis of functional weakness coexisting with MS, explanation, specialist physiotherapy, and no change of DMT for the functional symptom with the PML risk (JC 2.8 after 4 years) referred to her MS team for risk-benefit review and 3- to 4-monthly MRI. Prohibitions: further tests without a new question, dismissive language, invasive tests, and steroid treatment as an MS relapse. The differential is MS relapse, PML and malingering, all low with the case evidence.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms (plan 5.2): this motor-only case accepts "psychogenic non-epileptic seizures", "PNES", "functional seizures" and F44.5; scope them to the paroxysmal cases.
- Citation keys (plan 5.1): `[Stone_2016]` used; McGuigan C et al. J Neurol Neurosurg Psychiatry 2016;87:117-125 (natalizumab PML risk stratification and MRI surveillance) cited in full; add to the pack if a key is wanted.
- The library spine MRI normal report says "no intramedullary T2 lesion", which is acceptable here but would be wrong for an MS patient with known cord lesions; no change needed for this case.

## Open questions for Andrea (judgment calls you could not settle)

None open. Decisions taken and their reasons:
- The plan asked for `{contrast: true, protocol: ms}`. I required `{contrast: true}` only: the protocol does not change the study or its bill, and requiring `ms` would fail an agent that orders a gadolinium MRI under `standard`.
- Spine MRI added as an optional criterion (not in the plan). A cord relapse would not show on the brain MRI, so a neurologist could defend the order; the exam (unchanged tone and reflexes, positive signs, normal walking when unobserved) makes it non-required. Optional keeps it from being penalised as an unjustified action.
- The plan's 3.2 table lists the M09 drug check as recommended and section 4 as optional; section 4 is authoritative and is clinically right (no interaction changes management).
- Labs kept optional with `CBC, CMP` (plan); TSH and B12 stay in the stored panel with real values.
