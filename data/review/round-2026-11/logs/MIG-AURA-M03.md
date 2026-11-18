# MIG-AURA-M03

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM) | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 9664e97f-5ac4-4913-9ed0-b20ac82accde | FIXED (class LIT, commit 393c547e) | Nothing left to remove: no search_medical_literature criterion, follow-up or stored output; fallback literature_search null. |
| 30f0b036-ece6-4028-a5a5-989f73f5a594 | FIXED (plan D4) | ground_truth.assessment.required_recommendations[0] "Stop the aspirin ..." -> "Review the aspirin started for possible TIA once the cerebrovascular evaluation is complete: stop it if judged migraine aura (features listed) and no other indication; continue it if a TIA remains a real possibility; explain to patient and GP". Deleted prohibited_recommendations[1] (TIA antiplatelet prohibition). Class follow-through: key_clinical_evidence[2] (imaging excludes infarction and arterial disease, not TIA; aspirin decision rests on clinical features), red_herrings[1].correct_interpretation (review, not automatic stop), metadata.difficulty_description "empirical aspirin to stop" -> "to review". |
| d33fb521-abee-4c94-86ed-6438cb3ab36c | ALREADY-FIXED (plan D7) | No change. MRI and MRA are recommended criteria and never count as extra actions (policy_reward.py 138-146); ground_truth.stop_rule unchanged (max_additional_actions 1 applies to unlisted actions only). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.diagnosis.accepted[0] | "Probable sporadic hemiplegic migraine (ICHD-3 1.2.3)": one qualifying motor attack is probable hemiplegic migraine, ICHD-3 1.5.2, not 1.2.3 (plan D13 class) | FIXED (label change: code reference 1.2.3 -> 1.5.2; rest of label unchanged; DiagnosisCriterion still matches "probable sporadic hemiplegic migraine") |
| C | major | ground_truth.key_clinical_evidence[2] | "MRI ... and MRA ...; the aspirin started for possible TIA has no indication" makes imaging decide the TIA question (D4 rule 1) | FIXED |
| C | minor | ground_truth.red_herrings[1].correct_interpretation | "once recognised as aura it should be stopped" contradicted the conditional must | FIXED |
| C | minor | metadata.difficulty_description | "empirical aspirin to stop" | FIXED ("to review") |

PATTERNS check: differential[0] already states that a normal DWI does not exclude TIA; triptan avoidance and genetics musts unchanged (no note); pathway order history -> MRI -> MRA -> triptan check is clinical; no leakage in the patient block.

## Changes
The aspirin the GP started for possible TIA is no longer stopped automatically: the must now asks the agent to review it once the cerebrovascular evaluation is complete, to stop it if the episode is judged to be migraine aura with motor features and there is no other indication, to continue it if a TIA remains a real possibility, and to explain the decision to the patient and GP. The blanket prohibition of antiplatelet therapy is gone, and the key evidence and red-herring text now say that MRI and MRA exclude infarction and arterial disease but not TIA. The diagnosis label now cites ICHD-3 1.5.2 (probable hemiplegic migraine, one qualifying attack) instead of 1.2.3; the words of the label are otherwise unchanged. The stop rule is unchanged: MRI and MRA are recommended and are never counted as extra actions. At verification, the prevention must was reworded so that prevention is discussed, not started automatically, if motor aura recurs (AHS 2021 'consider'; same agents).

## Verification
perfect_agent.py -v: ok (every required and recommended criterion served by its own report). test_case_guards.py -k <case>: pass. case_io.py check: schema OK, synonym guard OK, no failure names this case (one unrelated failure names MIG-AURA-P05). DiagnosisCriterion.matches re-checked on a plain correct answer after any label edit: True; TIA / mimic answers: False.
Pass 1: 2 errors found
- ground_truth.assessment.required_recommendations[2] "start prevention if motor aura recurs" mandated prophylaxis on recurrence; class of note 1b2dc411 (plan D8): AHS 2021 lists hemiplegic aura under "consider". Changed to "if motor aura recurs, discuss prevention (AHS 2021 lists hemiplegic aura under 'consider'), weighing attack-related disability, his preference and drug risks: verapamil, lamotrigine, or flunarizine where licensed" (agents unchanged).
- ground_truth.red_herrings[0].intended_effect "May anchor on TIA and continue antiplatelet therapy" contradicted the conditional aspirin must (continue it if a TIA remains a real possibility; note 30f0b036). Changed to "... continue antiplatelet therapy without weighing the clinical features of the attack".
Cosmetic (not counted): none.
Re-run after the fixes: perfect_agent.py ok; test_case_guards -k MIG-AURA-M03 pass; case_io.py check: no failure names this case.
Pass 2: 0 errors found
- Checked: D4 aspirin-review must, prohibition deleted, KCE[2] and red herrings consistent with the conditional must, D13 code 1.5.2, pass-1 D8 prevention wording; triptan prohibition and the triptan-check report agree. Every note id has a ruling; no literature string left (fallback literature_search null); no new em dash; no answer leakage in the patient block or drug-check outputs.
Cosmetic (not counted): rulings file: field_path_now of 30f0b036 completed with key_clinical_evidence[2], red_herrings[1].correct_interpretation and metadata.difficulty_description (already listed in the log table).
Re-run at pass 2: perfect_agent.py -v ok (each required and recommended criterion receives the report carrying its expected evidence); test_case_guards -k for MIG-AURA-M01..M06: 48 passed; case_io.py check: schema OK, synonym guard OK, no failure names this case; mri_probe: no gadolinium text, no MRI pair needed; DiagnosisCriterion.matches: correct answer True, TIA / mimic False.
Condition audit (MIG-AURA auditor, 17 Nov 2026): 1 error found
- D/leak (own finding, TOOL_REPORT_STYLE_GUIDE check_drug_interactions: a drug check must not announce the patient's diagnosis): followup_outputs (check_drug_interactions, trigger check_sumatriptan_..._hemiplegic_migraine).output.summary said 'Triptans and ergots are label-restricted in hemiplegic migraine', applying the label restriction to this patient as if the diagnosis (probable sporadic hemiplegic migraine, which the patient block does not name) were already made. FIXED: '... label-restricted in hemiplegic migraine and migraine with brainstem aura' (the two label exclusions, as in contraindications[0]). The interaction content and the criterion's expected evidence are unchanged; no ruling changes. perfect_agent passes.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.
Pass 5: 0 errors found
- Checked the changes after the last clean pass. (1) The condition-audit edit of the triptan check summary (followup check_sumatriptan_..._hemiplegic_migraine) now reads "label-restricted in hemiplegic migraine and migraine with brainstem aura". That is correct: the triptan and DHE/ergotamine labels exclude both, and contraindications[0] says the same. The criterion expected_evidence, PRO0, REQ1 and KCE are unaffected. (2) metadata.case_body_concerns deletion (condition audit) checked against git diff 06b74446: only the generation-pipeline line was removed, the field is [] and no other field changed with it.
- perfect_agent.py -v ok; test_case_guards -k (M01..M08) 64 passed.
Cosmetic (not counted): none.
