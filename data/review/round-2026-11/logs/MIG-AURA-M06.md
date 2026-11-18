# MIG-AURA-M06

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM) | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| b641b8e0-2307-498d-8faf-f5b608eb8c63 | FIXED (class LIT, commit 393c547e) | Nothing left to remove: no search_medical_literature criterion, follow-up or stored output; fallback literature_search null. |
| 16e768ca-3f03-45b3-9057-8b1d0b1e84dc | FIXED (plan D3) | ground_truth.assessment.required_recommendations[3] -> canonical must: "If topiramate is chosen, start it only under the topiramate pregnancy prevention programme with a contraceptive method unaffected by enzyme induction: a copper IUD, a levonorgestrel IUS, or medroxyprogesterone acetate injection used with condoms. Topiramate is treated as a potential enzyme inducer at any dose, so pills and the etonogestrel implant are not adequate." followup_outputs[0].output.warnings[1] and followup_outputs[1].output.interactions[2]: 200 mg/day fact kept, FSRH any-dose caution added. |
| 1b2dc411-7192-492d-86af-12cebb2723d3 | FIXED (plan D8) | ground_truth.diagnosis.accepted[0] "preventive therapy required" -> "preventive therapy to be considered and discussed" (label change). required_recommendations[2] "Offer prevention because ..." -> "Discuss prevention, since the aura is lengthening and has exceeded 60 minutes (AHS 2021 lists prolonged aura under 'consider'), weighing attack-related disability, her preference, comorbidity and drug risks; if she chooses it, ..." (agents, doses and review unchanged). metadata.difficulty_rationale "preventive initiation" -> "discussion of prevention". |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| B | minor | patient.hpi, patient.history_present_illness | "After each visual aura resolves, she develops a severe left-sided throbbing headache" contradicts the same HPI (first headache right-sided), the clinical assessment (right-sided first, left-sided last) and differential[4] (headache changed side) | FIXED (both copies: "a severe throbbing headache (8-9/10), left-sided after the most recent aura,") |
| C | minor | ground_truth.diagnosis.accepted[0] | "migrainous infarction excluded by normal DWI": three weeks after the aura the decisive sequence is FLAIR as well as DWI (the MRI criterion's own rationale says so) | FIXED (label change, same entity: "excluded by MRI (normal DWI and FLAIR)") |
| C | minor | metadata.difficulty_rationale | "preventive initiation" contradicted the note | FIXED |

PATTERNS check: REQ0's switch list (implant included) concerns the aura, not topiramate, and stays (D3); rizatriptan-propranolol interaction correct (label); no TIA prohibition; no leakage; pathway order is clinical.

## Changes
Three changes. The topiramate must now follows FSRH 2022 (copper IUD, levonorgestrel IUS or medroxyprogesterone acetate injection with condoms, under the pregnancy prevention programme; topiramate is a potential enzyme inducer at any dose, so pills and the implant are not adequate), and both drug-check reports carry the same any-dose caution. Prevention is now to be considered and discussed rather than required: the label says so, and the must asks the agent to discuss prevention weighing disability, preference, comorbidity and drug risks, with the same propranolol, candesartan and lamotrigine options. Two consistency corrections: the HPI no longer says every headache was left-sided (the first was right-sided, as the assessment records), and the label says migrainous infarction is excluded by MRI (normal DWI and FLAIR) rather than by DWI alone.

## Verification
perfect_agent.py -v: ok (every required and recommended criterion served by its own report). test_case_guards.py -k <case>: pass. case_io.py check: schema OK, synonym guard OK, no failure names this case (one unrelated failure names MIG-AURA-P05). DiagnosisCriterion.matches re-checked on a plain correct answer after any label edit: True; TIA / mimic answers: False.
Pass 1: 0 errors found
- Checked the D3 canonical must and both report cautions, the D8 label and must, the HPI headache-side correction against the clinical assessment and differential[4], the FLAIR wording against the MRI report, no literature step left, checks pass.
Cosmetic (not counted): none.
Pass 2: 0 errors found
- Checked: D3 canonical must and both report cautions, D8 label and REQ2, HPI headache side against the assessment (right first, left last) and differential[0] (right-field aura, normal left occipital cortex), FLAIR wording against the MRI report. Every note id has a ruling; no literature string left (fallback literature_search null); no new em dash; no answer leakage in the patient block or drug-check outputs.
Cosmetic (not counted): rulings file: field_path_now of 1b2dc411 completed with metadata.difficulty_rationale (already listed in the log table).
Re-run at pass 2: perfect_agent.py -v ok (each required and recommended criterion receives the report carrying its expected evidence); test_case_guards -k for MIG-AURA-M01..M06: 48 passed; case_io.py check: schema OK, synonym guard OK, no failure names this case; mri_probe: no gadolinium text, no MRI pair needed; DiagnosisCriterion.matches: correct answer True, TIA / mimic False.
Condition audit (MIG-AURA auditor, 17 Nov 2026): class finding
- E/metadata (class: 25 of 30 MIG-AURA cases, no other condition; flagged by the workers for a central sweep): metadata.case_body_concerns held the generation-pipeline line "Useless-tool entries dropped because the case has neither output nor fallback (silent irre...", authoring-process text in a field the review app shows to physicians (ROUND_POLICY 'How to edit'; November addendum: no process text in metadata), and no longer accurate after this round's added criteria. FIXED: line deleted; the field is now empty. No clinical content changed; no ruling changes.
Pass 5: 0 errors found
- Full re-verification: git diff 06b74446 read and the whole case read. The D3 canonical must is REQ3, and the any-dose FSRH caution is in FU0 warnings[1] and FU1 interactions[2]. The D8 label "preventive therapy to be considered and discussed" agrees with REQ2, KCE[3], action-check-preventive-with-rizatriptan rationale ("being considered") and metadata.difficulty_rationale. The label wording "excluded by MRI (normal DWI and FLAIR)" matches the MRI additional_observations[0], the MRI criterion and differential[0]. The HPI headache side (right first, left after the last aura) agrees with assessment findings[7], differential[4] and the right-field aura / left occipital cortex in differential[0]. The LIT removal is complete. The metadata.case_body_concerns deletion is clean. Unlogged edit found in the diff, correct and kept: differential[2] (Posterior circulation TIA) key_features gained "(a normal DWI does not exclude TIA; the distinction is clinical)". This is the plan section 1 canonical fact (class TIA-CERT). Rulings file matches the log.
- perfect_agent.py -v ok; test_case_guards -k (M01..M08) 64 passed.
Cosmetic (not counted): none.
