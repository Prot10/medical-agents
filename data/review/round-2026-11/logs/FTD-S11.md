# FTD-S11

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-7-search-medical-literature (optional); removed initial literature_search outputs: Semantic variant primary progressive aphasia: diagnostic criteria and management. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 6689c73e | FIXED (class LIT, commit 393c547e) | No literature output remains (re-checked). |
| 8d60dcbe | FIXED | ground_truth.red_herrings[1].correct_interpretation (canonical C25); ground_truth.assessment.required_recommendations[2] ("the earlier outside scan cannot be reinterpreted without its images"); ground_truth.key_clinical_evidence[1] and ground_truth.differential[2].key_features (definite "fits early svPPA" replaced by tentative wording). |
| 1a346239 | FIXED (class LIT, commit 393c547e) | Criterion action-7-search-medical-literature was removed; none remains (re-checked). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C clinical | minor | initial_tool_outputs.labs.panels.Chemistry[5,12]; followup_outputs[2].output.panels.Chemistry[5,12] | Fasting glucose 118 and HbA1c 6.8% (known type 2 diabetes on metformin) had no significance line (class C8). | FIXED: glucose "Raised fasting glucose, in keeping with his known type 2 diabetes."; HbA1c "In keeping with his known type 2 diabetes; slightly above the usual 6.5% target on metformin alone (NICE NG28), for review in his routine diabetes care." No must added: managed in routine diabetes care, not part of this decision. Display remark CENTRAL.md item 1 |
| C clinical | minor | ground_truth.avoided_actions[4].rationale | CT rationale "lacks the resolution" (class C22, PPA wording). | FIXED: canonical C22 PPA text, citations [NICE_NG97], [SNLG_ISS_2024] |
| B consistency | minor | followup_outputs[5].output (performance status) | Said "unable to carry on usual work" and that communication limits work, but he retired three years ago, before the onset. | FIXED: retired before onset; independent in self-care, finances, medications and driving (as documented); communication limits complex social activities; Karnofsky 80, ECOG 1 kept |

## Changes
The earlier outside MRI 'asymmetry' is no longer read as definite early svPPA: the red herring, must 2, key evidence 1 and the HSV differential now say it may have been early atrophy but cannot be reinterpreted without the images, while the current MRI and the progressive course argue against encephalitis sequelae. The glucose and HbA1c rows carry a significance line referring to his known diabetes. The CT waste rationale now says CT is redundant because MRI is available and preferred. The performance-status report no longer says he cannot work (he retired before the onset). Literature steps were already removed by class LIT. Criteria, tiers, label and stop rule are unchanged.

## Verification
perfect_agent.py -v: pass (every required and recommended criterion served by its own stored report); test_case_guards.py -k <id>: pass; case_io.py check: schema OK, synonym guard OK, no test failure names the case. No MRI edited (mri_probe not needed). Reviewer status: R1 in_progress; not approved before this round.

Pass 1: 0 errors found
- Checked every note ruling, the diff since 06b74446, the final case in full, leakage, consistency and wording; perfect_agent.py -v ok and test_case_guards -k pass. No change.

Pass 2: 0 errors found
- Checked: all 3 note ids; 8d60dcbe wording in red herring 2, must 2, key evidence 1 and the HSV differential (tentative, images unavailable); glucose and HbA1c significance agree with the PMH (HbA1c 6.8%, metformin; NICE NG28 6.5% target is correct for a single non-hypoglycaemic drug); performance status agrees with the HPI (retired before onset, independent in medications, finances and driving; must 4 supervision is a forward safety step, not a contradiction); C22 PPA wording; Gorno-Tempini counts (2 core, 3 supporting at the bedside). No change.
- Re-checked: perfect_agent.py -v ok (each required and recommended criterion served with its expected evidence); test_case_guards -k pass (48 tests over the six cases); case_io.py check: schema OK, synonym guard OK, no failure names the case; mri_probe unchanged (no MRI output edited).

Pass 3: 0 errors found
- Checked: 3 note ids; 8d60dcbe tentative wording in red herring 2, must 2, key evidence 1 and the HSV differential, all supported by the stored MRI (no gliosis, encephalomalacia, haemosiderin or T2/FLAIR change); glucose and HbA1c lines in both lab copies agree with the PMH and NICE NG28 (6.5% target on metformin alone); performance status agrees with the HPI (retired before onset; independent in medications, finances, driving); C22 PPA wording. No change.
- Re-checked: perfect_agent.py -v ok (each required and recommended criterion served by its own stored report); test_case_guards -k pass (48 tests over the six cases); case_io.py check: schema OK, synonym guard OK, no failure names the case; DiagnosisCriterion.matches re-tested on the answers named above. No condition-audit change touched this case (none logged, file unchanged since pass 2).
