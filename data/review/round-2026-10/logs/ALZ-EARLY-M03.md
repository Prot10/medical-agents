# ALZ-EARLY-M03
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 84330594-c8f6-4ad7-a745-95d1389e5483 | FIXED | `ground_truth.diagnosis.accepted[0]` now "Amnestic multidomain mild cognitive impairment, suspected Alzheimer disease pathology (intermediate likelihood) with vascular contribution" (G31.84 kept), following the note's own wording (it names the vascular contribution, which the plan's label omits; see Open questions). CSF interpretation names the measured profile (decreased ratio, tau high-normal) with no A+T+ claim; biomarker `expected_evidence` "amyloid positivity without established tau pathology". |
| 30a27ac9-d3ba-48f7-acf1-81015ed15a93 | FIXED | `initial_tool_outputs.clinical_assessment.criteria_met.delayed_recall_improves_with_cueing` false, impression states recall 1/3 with no improvement after cues (matches `patient.neurological_exam.mental_status`); "partial benefit" template removed. |
| 2a2dd64e-a213-4b24-be79-0d7b5632cd00 | FIXED | Donepezil drug-check criterion `action-9-check-drug-interactions` and its follow-up deleted; initial and fallback `drug_interactions` null; MCI prohibition added. The deleted output's errors (amlodipine slowing the heart, tamsulosin anticholinergic) are not repeated anywhere: the new prohibition states tamsulosin is an alpha-1 blocker without anticholinergic effect. |
| aec83190-eec4-43f4-b80d-c3eb1fccbb13 | FIXED | `action-8-analyze-csf` relabelled, optional, with CSF and amyloid PET alternatives; new rationale; amyloid PET follow-up authored (`followup_outputs[3]`, positive, Centiloid 43); must on amyloid testing only if it changes management. |
| 55554aec-5637-44e2-afd7-dec35b28c040 | FIXED | MMA added: `followup_outputs[1]` (0.26 umol/L, normal) and recommended criterion `action-10-interpret-labs-mma` after the labs; reversible-cause differential cites the result. |
| 8e850ae1-3277-4069-8df0-0aa706b5685d | FIXED | Neuropsych impression (`followup_outputs[0].output.impression`) states testing in English, his dominant language, with norms adjusted for age, education and bilingual speakers where available, and caution on naming and fluency; criterion `action-5-order-specialized-test` label, rationale and expected evidence say the same; KCE item on bilingual norms. |
| 2c169efe-ec2e-49ce-a3df-7d60a8f5309f | FIXED | Summary comment; covered by 84330594 (not biomarker-confirmed, vascular and metabolic contribution named in label, disclosure and vascular musts). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.neurological_exam.mental_status`, `initial_tool_outputs.clinical_assessment.findings[1]` | MMSE arithmetic: date 1 + recall 2 + serial sevens 1 + wrong floor 1 = 5 points lost, but the total is 26/30 (also in the neuropsych report). | FIXED: the "wrong floor" place point removed (he is recorded as oriented to place); 4 points lost, 26/30 holds everywhere. |
| E | major | `initial_tool_outputs.clinical_assessment` | Engineering sentences; truncated orientation line; informant finding copied the patient introduction. | FIXED (C3): findings rewritten from the informant's account; impression per skeleton. |
| C | minor | `followup_outputs[0].output.impression` | "Storage-type deficit" from free recall alone in the neuropsych report. | FIXED: removed from the report (no recognition measure); the storage interpretation lives in the KCE, supported by the bedside cue failure. |
| B | minor | `followup_outputs[2].output` (CSF) | 14-3-3 and RT-QuIC; "N/A" artefact; p-tau 52 and t-tau 345 identical to M01. | FIXED (C6): canonical keys; p-tau181 56 and t-tau 371 (still high-normal, as the reviewer read it); Abeta values unchanged. |
| B | minor | `initial_tool_outputs.labs.panels.Reviewed_cognitive_panel_additions` | Mg, homocysteine, ESR, CRP identical to M01. | FIXED: 2.1, 12.3, 10, 1.4 (all normal). |
| C | minor | `initial_tool_outputs.mri.volumetrics.ventricular_system`, `.impression` | "Ventricular enlargement disproportionate to sulcal widening" suggests NPH that nothing else in the case supports (normal gait, nocturia from BPH); prose impression. | FIXED: "proportionate to the sulcal widening"; numbered impression. |
| C | major | `ground_truth.assessment` | Template musts and prohibitions; BP 153/84 in clinic not addressed. | FIXED (C12): disclosure; 6-12 month reassessment and exercise; BP above target, HbA1c 6.5%, statin, CPAP non-adherence; driving and finance safety; amyloid testing must. Prohibitions: MCI AChEI; no antimuscarinic for nocturia (tamsulosin can continue); do not attribute to OSA or aging. |
| B | minor | `ground_truth.differential` | VCI `high` with microbleeds the MRI does not show and "biomarker positivity". | FIXED: moderate as contributor; depression and reversible entries case-specific. |
| B | minor | `ground_truth.key_clinical_evidence` | MMSE pearl about "highly educated" patients (he has high-school education), APOE, AChEI first-line. | FIXED: four items: storage-type pearl (true here), bilingual norms, low-normal B12 on metformin, AChEI not for MCI. |
| E | minor | `ground_truth.red_herrings[1].data_point` | Em dash. | FIXED. |
| A | minor | criteria citations, rationale, expected_evidence | Duplicate bare keys; rationale equal to label. | FIXED (C13). |
| B | minor | sequence constraints, stop rule, `fallback_tool_outputs.literature_search`, metadata | No clinical-assessment-before-biomarker constraint; `max_additional_actions` 0; literature fallback; engineering educational point. | FIXED: soft constraint added; 1; null; reworded. |
| - | check | plan 3.6 | Each alternative probed on a fresh environment: CSF, amyloid PET and MMA served by case follow-ups. perfect_agent.py ok; test_case_guards pass. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The case stays MCI but is now labelled "amnestic multidomain MCI, suspected Alzheimer disease pathology (intermediate likelihood) with vascular contribution", because the CSF shows a decreased Abeta42/40 ratio (0.053) with p-tau181 (56) and total tau (371) high-normal. The bedside assessment now agrees with the exam: recall 1/3 at 5 minutes without benefit from cues; the MMSE point count was corrected so 26/30 adds up. The neuropsychological report states that testing was done in English, his dominant language, with norms appropriate for a bilingual man of his education. The donepezil step is removed; MCI musts are disclosure, reassessment with exercise, blood pressure (153/84) and CPAP adherence, driving and finances; no antimuscarinic for nocturia. MMA (0.26, normal) is a new recommended step for B12 299 on metformin. An amyloid PET alternative (positive, Centiloid 43) answers the biomarker step if chosen instead of CSF; 14-3-3 and RT-QuIC were removed from the CSF. The MRI no longer describes ventricular enlargement as disproportionate.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonym re-run for the new `accepted[0]`; the G31.84 expansion grants dementia, PCA, Benson and early-onset labels and G30.x codes to this MCI case (plan 5.1).
- New citation keys used: `[NIA_AA_MCI_2011]`, `[STRIVE_2013]`, `[BSH_B12_2014]`, `[Beers_2023]`.

## Open questions for Andrea (judgment calls you could not settle)

- Plan C4 gives M03 the label "MCI due to Alzheimer disease (amnestic, multi-domain), intermediate likelihood" without the vascular contribution; I followed Reviewer 1's notes 84330594 and 2c169efe, which ask for "suspected/probable early AD pathology and vascular contribution", and the MRI (Fazekas 2, putaminal lacune). The resulting label is identical in form to M01's. Tell the lead if the plan's shorter label is preferred.

## Verification
Adversarial check, 24 Oct 2026. Read the log, the diff and the whole final case.
- Notes: all seven ids present and each FIXED claim holds (label without A+T+, cueing field false matching "did not improve with cues", drug check gone, two-alternative biomarker with authored PET, MMA criterion and follow-up, bilingual norms statement in the neuropsych impression and criterion).
- Cross-field: MMSE corrected to 4 lost points = 26/30 in exam, assessment and neuropsych; CSF ratio 478/9100 = 0.053; p-tau 56 and t-tau 371 high-normal, consistent with "amyloid positivity without established tau pathology"; BP 153/84 addressed in a must; no repetition of the deleted output's errors (tamsulosin correctly called an alpha-1 blocker); no post-contrast text, no 14-3-3 or RT-QuIC.
- Worker's open question (label with vascular contribution vs the plan's shorter label): settled, not open. The reviewer's own wording in 84330594 and 2c169efe names the vascular contribution and the MRI supports it (Fazekas 2, putaminal lacune); the note governs over the plan's draft label.
- No changes made. perfect_agent.py ok; case_io.py check clean; test_case_guards pass.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine_ESR_CRP` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (2 places: the labs criterion label and metadata), the wording the other six cases already use.
- `BMP` completed to `CMP` with normal liver tests (total protein 7.2, albumin 4.3, AST 26, ALT 31, ALP 68, bilirubin 0.8): the labs criterion orders a CMP, so the authored report has to carry the hepatic part; no field_path points into the panel.
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.
- CBC indices made consistent (MCV = hematocrit x 10 / RBC): RBC 4.98 to 4.81; values within reference ranges and cited nowhere else in the case.
- Checks re-run after these additions: perfect_agent.py, case_io.py check and test_case_guards clean.
