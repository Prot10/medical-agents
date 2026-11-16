# FTD-S07

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-8-search-medical-literature (optional); removed initial literature_search outputs: Familial frontotemporal dementia: diagnostic criteria, genetics and management. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 13d4d753 | FIXED (class LIT, commit 393c547e) | No literature criterion or stored literature output remains (re-checked). |
| b4a2044c | FIXED | ground_truth.assessment.required_recommendations[0]: canonical C2 certainty clause (possible / probable / definite with a pathogenic variant). Requested labels already accepted by the scorer (verified); accepted[0] unchanged. |
| 832dd141 | FIXED | ground_truth.avoided_actions[6].rationale and citations: canonical C23 (FDG-PET vs amyloid PET). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C clinical | minor | fallback_tool_outputs.labs.panels.Plasma progranulin[0].clinical_significance | Abnormal progranulin 41 ng/mL had null significance (shown as "none" in the review app; class C8). | FIXED: "Low, consistent with GRN haploinsufficiency." (display remark CENTRAL.md item 1) |
| B consistency | minor | followup_outputs[6].output (order_performance_status) | Templated performance status (same two lines and scores in 26 FTD cases) not derived from this patient's history (class C6). | FIXED: rewritten from the HPI: gallery closed after impulsive purchases, gifts and unpaid bills, finances need supervision, driving not formally assessed; basic self-care not reported as impaired; Karnofsky 70, ECOG 1 kept (instrumental activities need supervision). |
| C clinical | minor | ground_truth.avoided_actions[4].rationale | Head CT rationale said CT "lacks the resolution and lobar specificity", which is wrong (Rascovsky 2011 accepts CT atrophy as imaging support); CT is waste here only because MRI is available and done (class C22). | FIXED: canonical C22 text, citations [NICE_NG97], [SNLG_ISS_2024]; severity stays waste |
| C clinical | minor | ground_truth.avoided_actions[6].rationale | Perfusion-MRI rationale presented amyloid PET as interchangeable with FDG-PET for the lobar pattern (class C23). | FIXED: canonical C23 text, citations [NICE_NG97], [Frisoni_2024] |
| C clinical | minor | ground_truth.diagnosis.rejected (corticobasal syndrome, CBS, corticobasal degeneration) | The veto also rejects a correct hedged answer such as "bvFTD; monitor for emerging corticobasal syndrome" (tested), while the differential keeps emerging CBS under review. The over-call it guards against (bvFTD with CBS, no cortical signs) is a real error, so left unchanged. | FLAGGED (scorer hedge handling, lead guard suggestion 8) |

## Changes
Must 0 now asks the agent to state possible, probable or definite bvFTD, definite if the counselled gene panel shows the pathogenic GRN variant (the label stays probable; GRN-associated and definite answers already score). The perfusion-MRI waste rationale no longer treats amyloid PET as a substitute for FDG-PET. The head CT waste rationale now says CT is redundant because MRI is available and preferred, not that CT cannot show atrophy. The performance-status report was rewritten from this history (gallery closed after impulsive spending, finances need supervision, self-care not reported impaired; Karnofsky 70, ECOG 1). The low progranulin row now carries a significance line. Literature steps were already removed by class LIT. Nothing else changed; all criteria, tiers, labels and the stop rule are as before.

## Verification
perfect_agent.py -v: pass (every required and recommended criterion served by its own stored report); test_case_guards.py -k <id>: pass; case_io.py check: schema OK, synonym guard OK, no test failure names the case. No MRI edited (mri_probe not needed). Reviewer status: R1 in_progress; not approved before this round.

Pass 1: 0 errors found
- Checked every note ruling, the diff since 06b74446, the final case in full, leakage, consistency and wording; perfect_agent.py -v ok and test_case_guards -k pass. No change.

Pass 2: 0 errors found
- Checked: all 3 note ids have a ruling (LIT re-verified: only null literature slots remain; b4a2044c must 0 is the canonical C2 text and the scorer accepts GRN-associated, genetically confirmed familial and definite FTLD answers, re-tested with DiagnosisCriterion.matches; 832dd141 rationale and citations as C23); C8 progranulin, C6 performance status (matches the HPI: gallery closed after impulsive purchases, gifts and unpaid bills; Karnofsky 70, ECOG 1 per the plan rule), C22 CT rationale; timeline (onset 57, age 59), Rascovsky 5 of 6 consistent across assessment, criterion, key evidence and must 0; red herring paths; no leakage; no em dash in new text. No change.
- Re-checked: perfect_agent.py -v ok (each required and recommended criterion served with its expected evidence); test_case_guards -k pass (48 tests over the six cases); case_io.py check: schema OK, synonym guard OK, no failure names the case; mri_probe unchanged (no MRI output edited).

Pass 3: 0 errors found
- Checked: 3 note ids ruled (LIT no remnant; b4a2044c must 0 = canonical C2, and 'GRN-associated bvFTD', 'genetically confirmed familial bvFTD', 'bvFTD with definite FTLD pathology' score; 832dd141 = canonical C23 with [NICE_NG97], [Frisoni_2024]); C22 CT rationale; C8 progranulin 41 ng/mL line agrees with the pathogenic GRN p.Arg493Ter panel; C6 performance status against the HPI (gallery closed after impulsive purchases, gifts and unpaid bills; Karnofsky 70, ECOG 1 per the plan rule); 5 of 6 Rascovsky features consistent across assessment, criterion and key evidence; MMSE arithmetic; red herring path; no em dash in new text. No change.
- Re-checked: perfect_agent.py -v ok (each required and recommended criterion served by its own stored report); test_case_guards -k pass (48 tests over the six cases); case_io.py check: schema OK, synonym guard OK, no failure names the case; DiagnosisCriterion.matches re-tested on the answers named above. No condition-audit change touched this case (none logged, file unchanged since pass 2).
