# FTD-S09

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-7-search-medical-literature (optional); removed initial literature_search outputs: Behavioural variant frontotemporal dementia: diagnostic criteria and management. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| bc253a6c | FIXED (class LIT, commit 393c547e) | No literature output remains (re-checked). |
| 4662ca9b | FIXED (class LIT, commit 393c547e) | Criterion action-7-search-medical-literature was removed; none remains (re-checked). |
| ade5774b | FIXED | ground_truth.assessment.required_recommendations[1] (canonical C21); ground_truth.differential[0].key_features ("Low as the sole cause; a contribution is not excluded."); ground_truth.red_herrings[1].correct_interpretation; ground_truth.diagnosis.rejected minus "alcohol-related brain damage", "alcohol-related dementia" ("korsakoff" kept). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C clinical | minor | fallback_tool_outputs.labs.panels.CDT[0].clinical_significance | Raised %CDT 2.4% had null significance (class C8). | FIXED: "Consistent with sustained heavy alcohol intake." (must 1 manages it; display remark CENTRAL.md item 1) |
| C clinical | minor | ground_truth.avoided_actions[4].rationale | Head CT rationale said CT "lacks the resolution and lobar specificity", which is wrong (Rascovsky 2011 accepts CT atrophy as imaging support); CT is waste here only because MRI is available and done (class C22). | FIXED: canonical C22 text, citations [NICE_NG97], [SNLG_ISS_2024]; severity stays waste |
| C clinical | minor | ground_truth.avoided_actions[6].rationale | Perfusion-MRI rationale presented amyloid PET as interchangeable with FDG-PET for the lobar pattern (class C23). | FIXED: canonical C23 text, citations [NICE_NG97], [Frisoni_2024] |
| B consistency | minor | followup_outputs[8].output (performance status) | Not templated (plan: no C6), but "help with meals, finances and medications" and "needs prompting and help with dressing and hygiene" are not documented in the HPI. | FIXED (verification pass 1): rewritten from the history (restaurant closed after health code violations, crashes from impulsive driving, supervision at home for continuous eating, compulsive rearranging and drinking, finances not formally assessed, basic self-care not reported impaired); Karnofsky 70, ECOG 1 per the plan's C6 scoring rule |
| C clinical | minor | ground_truth.assessment.required_recommendations[3] | "Supervised access to food and alcohol" by the caregiver left caregiver restriction of alcohol standing on its own, which note ade5774b rules is not withdrawal management. | FIXED (verification pass 1): "supervised access to food, and to alcohol as part of the plan agreed after the dependence assessment" |

## Changes
The alcohol must now treats the six glasses of wine a day as both a possible bvFTD behaviour and a contributor that is not excluded: screen for dependence (AUDIT, SADQ) and past withdrawal, arrange medically assisted withdrawal with alcohol services if dependent rather than abrupt abstinence, her husband controls access as support only, and thiamine is oral, or parenteral if Wernicke is suspected or nutrition is poor. The alcohol differential (still low) and red herring say a contribution is not excluded, and the rejected list no longer vetoes 'alcohol-related brain damage' or 'alcohol-related dementia' as qualifiers (a bvFTD term is still required). Her husband's supervision of alcohol in the caregiver plan now follows the plan agreed after the dependence assessment. The performance-status report now matches the history (supervision at home, self-care not reported impaired; Karnofsky 70, ECOG 1). The raised CDT row has a significance line; the CT and perfusion-MRI waste rationales were corrected as in the other FTD cases. Literature steps were already removed by class LIT.

## Verification
perfect_agent.py -v: pass (every required and recommended criterion served by its own stored report); test_case_guards.py -k <id>: pass; case_io.py check: schema OK, synonym guard OK, no test failure names the case. No MRI edited (mri_probe not needed). Reviewer status: R1 in_progress; not approved before this round.

Pass 1: 2 errors found
- followup_outputs[8].output (order_performance_status): the report stated dependence the history does not document (help with meals, finances, medications, dressing and hygiene; Karnofsky 50, ECOG 2). Rewritten from the HPI with the plan's C6 rule: supervision at home for continuous eating, compulsive rearranging and drinking; restaurant closed; impulsive-driving crashes; finances not formally assessed; basic self-care not reported impaired; Karnofsky 70, ECOG 1.
- ground_truth.assessment.required_recommendations[3]: caregiver "supervised access to food and alcohol" contradicted the note ade5774b ruling that caregiver control is support, not withdrawal management; now "supervised access to food, and to alcohol as part of the plan agreed after the dependence assessment".
Re-checked: perfect_agent.py FTD-S09 -v ok; test_case_guards -k FTD-S09 pass; case_io.py check: schema OK, synonym guard OK, no failure names the case.

Pass 2: 0 errors found
- Checked: all 3 note ids; ade5774b must 1 and the pass-1 must 3 wording (dependence screening, assisted withdrawal if dependent, husband as support only, thiamine by nutrition and Wernicke risk); differential and red herring; rejected list (qualified alcohol answer scores, 'alcohol-related dementia' alone does not, re-tested); CDT significance; drug-check outputs agree with the medication list; C22 and C23. No change.
- Flag for the lead (no change, label is reviewer-only): accepted[0] says 'advanced stage', while the history documents no loss of basic self-care and the performance status now reads Karnofsky 70, ECOG 1 per the plan's C6 rule; the qualifier rests on the cognitive and imaging severity (MMSE 20, FAB 9, 25% frontal volume loss) rather than on function.
- Re-checked: perfect_agent.py -v ok (each required and recommended criterion served with its expected evidence); test_case_guards -k pass (48 tests over the six cases); case_io.py check: schema OK, synonym guard OK, no failure names the case; mri_probe unchanged (no MRI output edited).

Pass 3: 0 errors found
- Checked: 3 note ids; ade5774b must 1 is canonical C21 (AUDIT/SADQ, assisted withdrawal if dependent, husband as support only, thiamine by nutrition and Wernicke risk) and must 3 follows it; benzodiazepine prohibition is limited to behavioural control, so it does not contradict assisted withdrawal; differential, red herring and rejected list ('probable bvFTD with a possible contribution from alcohol-related brain damage' scores, 'alcohol-related dementia' alone does not); CDT significance; sertraline and trazodone outputs agree with the medication list (hydrochlorothiazide, levothyroxine) and with normal sodium; pass-1 performance status agrees with the HPI. The 'advanced stage' label flag of pass 2 stands for the lead (label not changeable here). No change.
- Re-checked: perfect_agent.py -v ok (each required and recommended criterion served by its own stored report); test_case_guards -k pass (48 tests over the six cases); case_io.py check: schema OK, synonym guard OK, no failure names the case; DiagnosisCriterion.matches re-tested on the answers named above. No condition-audit change touched this case (none logged, file unchanged since pass 2).
