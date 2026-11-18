# FTD-S12

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-6-search-medical-literature (optional); removed initial literature_search outputs: Non-fluent/agrammatic primary progressive aphasia: diagnostic criteria and management. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| bf1184cb | FIXED (class LIT, commit 393c547e) | No literature output remains (re-checked). |
| acb7ab4d | FIXED | ground_truth.assessment.prohibited_recommendations[0] (canonical C26); ground_truth.differential[3].key_features; ground_truth.key_clinical_evidence[2]; ground_truth.action_criteria[4].expected_evidence (no chronic strategic infarct or lacune; DWI only for acute ischaemia). |
| 501bfd6b | FIXED (class LIT, commit 393c547e) | Criterion action-6-search-medical-literature was removed; none remains (re-checked). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| B consistency | major | followup_outputs[5].output.findings[1] (performance status) | Said she "lives alone with family support for correspondence and finances", contradicting the HPI and bedside screen (manages household, finances, medications and calendar alone); also "unable to carry on usual work" though she retired four years ago, before the onset. | FIXED: independent in self-care, household, finances and medications, lives alone, retired before onset; the speech difficulty limits conversation and social activities (isolation documented); Karnofsky 80, ECOG 1 kept |

## Changes
The statement that forbids attributing the speech decline to the old TIA no longer depends on a new DWI finding: it now rests on the continuous 18-month progression, the absence of a chronic strategic infarct or encephalomalacia on MRI and the left posterior fronto-insular atrophy, and notes that a negative DWI this late cannot date or exclude an old event; the stroke differential (still low), key evidence 2 and the MRI criterion's expected evidence say the same. The performance-status report now matches the history (she manages her finances alone and retired before the onset). Literature steps were already removed by class LIT. Criteria, tiers, label and stop rule are unchanged.

## Verification
perfect_agent.py -v: pass (every required and recommended criterion served by its own stored report); test_case_guards.py -k <id>: pass; case_io.py check: schema OK, synonym guard OK, no test failure names the case. No MRI edited (mri_probe not needed). Reviewer status: R1 in_progress; not approved before this round.

Pass 1: 0 errors found
- Checked every note ruling, the diff since 06b74446, the final case in full, leakage, consistency and wording; perfect_agent.py -v ok and test_case_guards -k pass. No change.

Pass 2: 0 errors found
- Checked: all 3 note ids; acb7ab4d canonical C26 prohibition, stroke differential, key evidence 2 and MRI expected evidence (all supported by the stored MRI: no strategic infarct or lacune, no T2/FLAIR signal change); red herring 1 has no DWI prerequisite; performance status agrees with the HPI (lives alone, manages household, finances and medications, retired before onset, isolation documented); nfvPPA criteria count in must 0 matches the assessment. No change.
- Re-checked: perfect_agent.py -v ok (each required and recommended criterion served with its expected evidence); test_case_guards -k pass (48 tests over the six cases); case_io.py check: schema OK, synonym guard OK, no failure names the case; mri_probe unchanged (no MRI output edited).

Pass 3: 0 errors found
- Checked: 3 note ids; acb7ab4d canonical C26 prohibition, stroke differential, key evidence 2 and MRI expected evidence, all supported by the stored MRI (no strategic infarct or lacune, no T2/FLAIR signal change, DWI used only for acute ischaemia); nfvPPA criteria count in must 0; performance status agrees with the HPI (lives alone, manages household and finances, retired before onset, isolation). No change.
- Re-checked: perfect_agent.py -v ok (each required and recommended criterion served by its own stored report); test_case_guards -k pass (48 tests over the six cases); case_io.py check: schema OK, synonym guard OK, no failure names the case; DiagnosisCriterion.matches re-tested on the answers named above. No condition-audit change touched this case (none logged, file unchanged since pass 2).
