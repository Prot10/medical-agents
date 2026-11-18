# FTD-S10

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-8-search-medical-literature (optional); removed initial literature_search outputs: Familial frontotemporal dementia: diagnostic criteria, genetics and management. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 096c241c | FIXED (class LIT, commit 393c547e) | No literature criterion or stored literature output remains (re-checked). |
| 8b9672cf | FIXED | ground_truth.assessment.required_recommendations[0]: canonical C2 certainty clause. Requested labels already accepted (verified); accepted[0] unchanged. |
| 73ab2e96 | FIXED | ground_truth.avoided_actions[9] (new avoid-waste-als-gene-panel); ALS follow-up moved from followup_outputs[5] to followup_outputs[7] (last), report unchanged. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C clinical | major | ground_truth.assessment.required_recommendations[1] | Alcohol must (8 to 10 beers a day) lacked dependence screening and assisted-withdrawal criteria and argued the drinking away (class C21, aligned with S09 note ade5774b). | FIXED: canonical C21 wording, "does not account for the whole progressive syndrome" |
| C clinical | minor | ground_truth.differential[1].key_features; ground_truth.red_herrings[0].correct_interpretation | Alcohol-related brain damage now "Low as the sole cause; a contribution is not excluded"; red herring aligned (class C21). | FIXED |
| C clinical | minor | ground_truth.diagnosis.rejected | "alcohol-related brain damage" and "alcohol-related dementia" vetoed a correct qualified answer (class C21). | FIXED: removed; "korsakoff" kept; "alcohol-related dementia" alone still does not score (tested) |
| B consistency | minor | followup_outputs[6].output (order_performance_status) | Templated performance status (same two lines and scores in 26 FTD cases) not derived from this patient's history (class C6). | FIXED: rewritten from the HPI: dismissed from his job 2 years ago, large unauthorised purchases so finances need supervision, driving not formally assessed; neglects personal hygiene and needs prompting; Karnofsky 70, ECOG 1. |
| C clinical | minor | ground_truth.avoided_actions[4].rationale | Head CT rationale said CT "lacks the resolution and lobar specificity", which is wrong (Rascovsky 2011 accepts CT atrophy as imaging support); CT is waste here only because MRI is available and done (class C22). | FIXED: canonical C22 text, citations [NICE_NG97], [SNLG_ISS_2024]; severity stays waste |
| C clinical | minor | ground_truth.avoided_actions[6].rationale | Perfusion-MRI rationale presented amyloid PET as interchangeable with FDG-PET for the lobar pattern (class C23). | FIXED: canonical C23 text, citations [NICE_NG97], [Frisoni_2024] |
| C clinical | minor | ground_truth.diagnosis.rejected (FTD-MND, motor neuron disease, motor neurone disease) | Must 5 asks to watch for MND, but the veto does not distinguish "examine for MND at follow-up" in an answer from an over-call; scorer hedge handling. | FLAGGED (lead guard suggestion 8) |

## Changes
Must 0 now asks for possible, probable or definite bvFTD, definite if the counselled panel shows the C9orf72 expansion (label stays probable; C9orf72-associated and definite answers already score). Ordering a separate ALS gene panel is now waste (no motor neuron signs, the FTD panel already tests C9orf72); its stored report is kept and moved to the end of the pathway, and motor neuron review stays a must. The alcohol must follows the condition-wide wording: dependence screening, assisted withdrawal with alcohol services if dependent, wife's control of access as support only, thiamine by nutrition and Wernicke risk; the alcohol differential and red herring keep a contribution open and the rejected list no longer vetoes alcohol qualifiers. The performance-status report was rewritten from this history; the CT and perfusion-MRI waste rationales were corrected. Literature steps were already removed by class LIT.

## Verification
perfect_agent.py -v: pass (every required and recommended criterion served by its own stored report); test_case_guards.py -k <id>: pass; case_io.py check: schema OK, synonym guard OK, no test failure names the case. No MRI edited (mri_probe not needed). Reviewer status: R1 in_progress; not approved before this round.

Pass 1: 0 errors found
- Checked every note ruling, the diff since 06b74446, the final case in full, leakage, consistency and wording; perfect_agent.py -v ok and test_case_guards -k pass. No change.

Pass 2: 0 errors found
- Checked: all 3 note ids; 8b9672cf canonical C2 must 0, C9orf72-associated and definite answers score (re-tested); 73ab2e96 avoid-waste-als-gene-panel matches only genetic_panel:ALS (no criterion overlap) and the ALS report is the last follow-up; must 5 keeps MND follow-up; C21 must 1, differential, red herring and rejected list; C6 performance status from the HPI; C22 and C23; timeline (onset 51, age 53). No change.
- Re-checked: perfect_agent.py -v ok (each required and recommended criterion served with its expected evidence); test_case_guards -k pass (48 tests over the six cases); case_io.py check: schema OK, synonym guard OK, no failure names the case; mri_probe unchanged (no MRI output edited).

Pass 3: 0 errors found
- Checked: 3 note ids; 8b9672cf canonical C2 and 'C9orf72-associated bvFTD' / 'genetically confirmed familial bvFTD' score; 73ab2e96 avoid-waste-als-gene-panel matches only genetic_panel:ALS (no criterion overlap), ALS report last and consistent with the FTD panel (about 700 repeats), must 5 keeps MND follow-up; C21 must 1, differential, red herring, rejected list (qualified alcohol answer scores); C6 performance status from the HPI; C22, C23; red herring paths (caudate atrophy at mri.additional_observations[1]). No change.
- Re-checked: perfect_agent.py -v ok (each required and recommended criterion served by its own stored report); test_case_guards -k pass (48 tests over the six cases); case_io.py check: schema OK, synonym guard OK, no failure names the case; DiagnosisCriterion.matches re-tested on the answers named above. No condition-audit change touched this case (none logged, file unchanged since pass 2).
