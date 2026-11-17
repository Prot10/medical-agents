# MIG-AURA-S06

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 72ca20f5-d740-4fca-97f4-bc9e03e146fb | FIXED (class LIT, commit 393c547e) | Nothing left to change: no search_medical_literature criterion, follow-up or stored output remains in the case (checked); a literature query gets the neutral library text. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | none | ground_truth.assessment.required_recommendations[3] | Checked against class TOPI-CONTRA: the contraception must lists the progestogen-only pill, implant, LNG-IUS or copper IUD while breastfeeding, for the aura, with no topiramate; this is correct (UKMEC 2 for progestogen-only methods) and topiramate is not one of the offered preventives | no change |
| C | none | ground_truth.assessment.required_recommendations[2] | AHS 2021 "consider" threshold for 2 headache days a month with severe disability checked; correct | no change |
| C | minor | ground_truth.avoided_actions (echo and cardiac-monitoring waste entries) | The citation is [ICHD_3], which does not address PFO screening or Holter use; the rationale itself names MIST, PRIMA and PREMIUM. The same template is in other MIG-AURA cases, so it is a condition-level citation question for the lead | FLAGGED |
| C | minor | ground_truth.differential[2].key_features | PRES entry said it "requires marked hypertension and encephalopathy"; PRES can occur with mildly raised or normal blood pressure and present with seizures or visual loss. Reworded (verification pass 1) | FIXED |
| E | minor | metadata.case_body_concerns | Authoring-process text ("Useless-tool entries dropped ...") in metadata, which physicians see. Present in every MIG-AURA case; left for the lead to decide centrally | FLAGGED |

## Changes
Not approved before this round (R1 in progress). The only note asked for the literature search step to go; it was removed by the class LIT change (commit 393c547e) and nothing of it is left. I read every field again: the diagnosis, the ICHD-3 assessment (5 of 6 criterion C characteristics), the breastfeeding drug check, the musts and the prohibitions are consistent and correct, so the case content is unchanged this round apart from the literature removal.

## Verification
Pass 1: 1 errors found
- ground_truth.differential[2].key_features (Postpartum PRES): "Requires marked hypertension and encephalopathy" was factually wrong; PRES can occur with only mildly raised or normal blood pressure and does not always cause encephalopathy (it also presents with seizures or visual loss). Reworded to "Usually presents with hypertension, encephalopathy, seizures or visual loss, although blood pressure can be only mildly raised or normal; here blood pressure 114/70, normal mental status and examination, and attacks identical to the 4-year pre-pregnancy pattern". Likelihood unchanged (very_low). FIXED.
- Note 72ca20f5 ruling checked: no search_medical_literature string left in the case; FIXED (class LIT) is right. TOPI-CONTRA check confirmed: no topiramate-with-implant claim (REQ3 lists the implant only for the aura while breastfeeding). perfect_agent.py -v and test_case_guards pass after the edit.
- Not changed (lead level, already flagged): avoided-action echo and Holter entries cite [ICHD_3] or nothing; the October pack decision assigns [ICHD_3] to this waste class, and condition-wide 12 echo entries have no citation, so it is a condition-level decision for the lead.
Cosmetic (not counted): none.

Pass 2: 0 errors found
- Note 72ca20f5 (the only note in the annotation file) ruled FIXED by class LIT: confirmed, no literature criterion, follow-up or stored output left. Whole case reread: TOPI-CONTRA does not apply (REQ3 lists the implant only for the aura while breastfeeding, plan section 3); the pass-1 PRES wording is accurate; ICHD-3 C count (5 of 6, no succession), AHS 2021 'consider' threshold, UKMEC categories and the lactation choices agree across the HPI, the clinical assessment, the drug report, the musts and the prohibitions.
- Checks re-run on 17 Nov 2026: perfect_agent.py -v passes (every criterion answered by the case's own data, none by the case fallback or the library); case_io.py check: schema and synonym guard OK, no test failure names this case; test_case_guards -k for S06-S11 passes (599 passed). No literature string left; no em dash or non-ASCII character in text added this round.
- Not changed (lead level, as pass 1): the waste entries for echo and Holter cite [ICHD_3], following the October pack decision for this waste class.
Cosmetic (not counted): none.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.
Pass 5: 0 errors found
- Scope: the only change after the last clean pass is the condition-audit class fix (metadata.case_body_concerns). Checked in the diff: the generation-pipeline line was the only entry, the field is now [], no other field changed after pass 4, and no 'Useless-tool' text remains anywhere in the case.
- Checks: perfect_agent.py MIG-AURA-S06 -v passes; test_case_guards -k (8 cases) 64 passed.
Cosmetic (not counted): none.
Pass 6: 0 errors found
- Scope: pass 5 was clean and nothing was written to the case after it (git diff of the case shows only the earlier round changes, the case file is older than the pass-5 log entry); nothing to re-verify.
- Checks: perfect_agent.py MIG-AURA-S06 -v passes; test_case_guards -k (8 cases) 64 passed.
Cosmetic (not counted): none.
