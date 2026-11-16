# FTD-S08

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-8-search-medical-literature (optional); removed initial literature_search outputs: Behavioural variant frontotemporal dementia: diagnostic criteria and management. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 5d03e1fe | FIXED (class LIT, commit 393c547e) | No literature criterion or stored literature output remains (re-checked). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| B consistency | minor | followup_outputs[6].output (order_performance_status) | Templated performance status (same two lines and scores in 26 FTD cases) not derived from this patient's history (class C6). | FIXED: rewritten from the HPI: resigned from his law firm 18 months ago after complaints and ethical violations, major financial decisions without consultation so finances need supervision, driving not formally assessed; basic self-care not reported as impaired; Karnofsky 70, ECOG 1. |
| C clinical | minor | ground_truth.avoided_actions[4].rationale | Head CT rationale said CT "lacks the resolution and lobar specificity", which is wrong (Rascovsky 2011 accepts CT atrophy as imaging support); CT is waste here only because MRI is available and done (class C22). | FIXED: canonical C22 text, citations [NICE_NG97], [SNLG_ISS_2024]; severity stays waste |
| C clinical | minor | ground_truth.avoided_actions[6].rationale | Perfusion-MRI rationale presented amyloid PET as interchangeable with FDG-PET for the lobar pattern (class C23). | FIXED: canonical C23 text, citations [NICE_NG97], [Frisoni_2024] |
| C clinical | - | initial_tool_outputs.clinical_assessment.findings[4] | Checked feature E against the C7 rule: "eats continuously" is listed in the HPI among the new behaviours since the change began, so it is a documented change (binge eating); 4 of 6 kept; F correctly not established at the bedside. | no change |

## Changes
The head CT waste rationale now says CT is redundant because MRI is available and preferred, not that CT cannot show atrophy; the perfusion-MRI waste rationale no longer treats amyloid PET as a substitute for FDG-PET. The performance-status report was rewritten from this history (resigned after complaints, financial decisions need supervision, self-care not reported impaired; Karnofsky 70, ECOG 1). Literature steps were already removed by class LIT. Criteria, tiers, label, musts and stop rule are unchanged.

## Verification
perfect_agent.py -v: pass (every required and recommended criterion served by its own stored report); test_case_guards.py -k <id>: pass; case_io.py check: schema OK, synonym guard OK, no test failure names the case. No MRI edited (mri_probe not needed). Reviewer status: R1 in_progress; not approved before this round.

Pass 1: 0 errors found
- Checked every note ruling, the diff since 06b74446, the final case in full, leakage, consistency and wording; perfect_agent.py -v ok and test_case_guards -k pass. No change.

Pass 2: 0 errors found
- Checked: the LIT note (no remnant); C6 performance status against the HPI (resignation after complaints and ethical violations, unsupervised financial decisions; Karnofsky 70, ECOG 1); C22 and C23 rationales; feature E (eats continuously is a new behaviour) and F not established, 4 of 6 consistent across fields; negative panel, so must 0 correctly has no definite clause; timeline (onset 54, age 56). No change.
- Re-checked: perfect_agent.py -v ok (each required and recommended criterion served with its expected evidence); test_case_guards -k pass (48 tests over the six cases); case_io.py check: schema OK, synonym guard OK, no failure names the case; mri_probe unchanged (no MRI output edited).

Pass 3: 0 errors found
- Checked: LIT note (no remnant); C6 performance status against the HPI (resignation after complaints and ethical violations, financial decisions without consultation); C22 and C23 rationales; negative panel, so must 0 without a definite clause is correct; 4 of 6 features and F not established consistent; MMSE arithmetic; red herring path resolves to the bedside-screen row. No change.
- Re-checked: perfect_agent.py -v ok (each required and recommended criterion served by its own stored report); test_case_guards -k pass (48 tests over the six cases); case_io.py check: schema OK, synonym guard OK, no failure names the case; DiagnosisCriterion.matches re-tested on the answers named above. No condition-audit change touched this case (none logged, file unchanged since pass 2).
