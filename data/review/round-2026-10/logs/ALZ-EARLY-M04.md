# ALZ-EARLY-M04
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 243a201d-94c7-4c9b-90f8-325d4ae3521e | FIXED | MCI kept (plan C4). `patient.history_present_illness`: the metformin lapse is one episode he noticed himself; he now uses automatic refills with delivery, a pill organizer he fills, calendar and phone reminders, with no further errors in six weeks; Denise has not taken over medicines, finances or appointments. `initial_tool_outputs.clinical_assessment` adds an "Instrumental activities" finding and a functional sentence in the impression stating the errors were isolated and compensated. |
| fb473466-167b-46a9-83e3-5caf790c2932 | ALREADY-FIXED | Agreement note (A+T+N+ well supported). Label and CSF values unchanged; CSF interpretation still names "an A+T+N+ profile" and the biomarker criterion expects "amyloid positivity with tau pathology". |
| 4ffea6c8-e76a-47da-a882-8f3aadb1422b | FIXED | `initial_tool_outputs.clinical_assessment.criteria_met.informant_history_obtained` true; informant finding (daughter Denise) added. |
| 03a603fe-c1f5-46a6-b75d-26d0811e7049 | FIXED | `criteria_met.delayed_recall_improves_with_cueing` false; impression states recall 1/3 (MMSE) and 1/5 (MoCA) with no improvement after cues, consistent with the exam. |
| b5a52f53-3e23-483c-99a9-dc6a3baa24b1 | FIXED | Donepezil plus levothyroxine drug-check follow-up and criterion `action-10-check-drug-interactions` deleted; initial and fallback `drug_interactions` null; MCI prohibition added. |
| 8ac152e7-514d-41cd-ac81-5736f960bee3 | FIXED | `initial_tool_outputs.labs.panels.Reviewed_cognitive_panel_additions[Homocysteine].clinical_significance` null (it also leaked the MMA result into the initial labs); homocysteine added to the abnormal summary and interpretation. Must added: IM hydroxocobalamin 1 mg alternate days then every 2 months, recheck cognition, "a treatable contributor, not an alternative to the Alzheimer diagnosis". Differential and KCE call it a confirmed contributor. New recommended criterion `action-11-interpret-labs-mma` for the existing MMA follow-up. |
| 4ce60934-ce0b-47ef-ab5d-536e8bfad15b | FIXED | Levothyroxine removed from musts and from the (deleted) drug check. Must: repeat TSH and free T4 with TPO antibodies in 2-3 months. Prohibition: no levothyroxine for TSH 6.8 with normal free T4 [TRUST_2017]. Differential, KCE and red herring 1 reworded (retest, not treat). |
| d758bd87-f70d-46fe-8337-0c1816c240e6 | FIXED | `action-8-analyze-csf` relabelled, optional, CSF and amyloid PET alternatives; amyloid PET follow-up authored (`followup_outputs[3]`, positive, Centiloid 81). Engineering must ("case-designated optional CSF route") replaced by the canonical amyloid-testing must; prohibition 2 that cited it removed. |
| a67cc21b-a4dc-4e4b-a827-a6031641b2c4 | FIXED | Criterion `action-9-search-medical-literature` and its follow-up deleted; `fallback_tool_outputs.literature_search` null. |
| e6e47d83-99a1-45b7-9325-04ffc44b2084 | FIXED | Summary comment; covered by 243a201d, 4ffea6c8, 03a603fe and b5a52f53. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| E | major | `initial_tool_outputs.clinical_assessment.impression`, `.findings` | Engineering template sentences; truncated orientation line; an HPI sentence copied as the only informant finding. | FIXED (C3). |
| B | minor | `initial_tool_outputs.labs.interpretation` | Free T4 "within normal limits" listed under "Abnormal values"; homocysteine (19.8, H) missing from the abnormal list. | FIXED. |
| B | minor | `initial_tool_outputs.labs.panels.Reviewed_cognitive_panel_additions` | Mg, ESR, CRP identical to M01 (template). | FIXED: 2.2, 14, 0.9 (normal). |
| B | minor | `followup_outputs[2].output` (CSF) | 14-3-3, RT-QuIC and an unordered NfL; em dash. | FIXED (C6): canonical five analytes, values unchanged. |
| C | minor | `followup_outputs[0].output.impression` | Rey delayed recall counted as executive; "minimal benefit from recognition cueing" wording. | FIXED: visual memory; recognition 10/15 stated directly. |
| B | minor | `initial_tool_outputs.mri.additional_observations[1]` | "No ... abnormal enhancement" with `contrast: false`. | FIXED: "No mass lesions". |
| C | major | `ground_truth.assessment` | Musts restated tool steps and prescribed levothyroxine; prohibitions generic (benzodiazepines). | FIXED (C12): B12 replacement, thyroid retest, disclosure addressing his belief, reassessment with exercise, safety for a man living alone, BP 148/88 and HbA1c, amyloid testing. Prohibitions: attribution to B12/thyroid, levothyroxine, MCI AChEI, antimuscarinic for nocturia. |
| C | major | `ground_truth.differential[0..1]` | B12 deficiency and subclinical hypothyroidism left `moderate` as causes after the work-up. | FIXED: both `low` as sole causes; B12 described as a confirmed contributor. |
| B | minor | `ground_truth.key_clinical_evidence` | Six items, several overclaiming ("definitive anchor", "settle the differential" from an optional test). | FIXED (C10): four true items. |
| E | minor | HPI, exam, red herrings, metadata | Em dashes. | FIXED in the sentences rewritten. |
| A | minor | criteria citations, rationales | Duplicate bare keys; rationale equal to label. | FIXED (C13). |
| B | minor | sequence, stop rule | No clinical-assessment-before-biomarker constraint; `max_additional_actions` 0. | FIXED. |
| - | check | plan 3.6 | Alternatives probed: CSF, amyloid PET and MMA served by case follow-ups. perfect_agent.py ok; test_case_guards pass. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The case stays amnestic multi-domain MCI due to Alzheimer disease (A+T+N+ CSF unchanged: ratio 0.043, p-tau181 78, t-tau 482). The HPI now makes the staging explicit: the missed pickups and a five-day metformin lapse he noticed himself were isolated, he now uses automatic refills, a pill organizer and reminders with no further errors, and his daughter has not taken over any complex activity. The bedside assessment records the daughter as informant and no benefit from cues. B12 deficiency (180 pg/mL, MMA 0.68, homocysteine 19.8, atrophic gastritis) is treated as a real contributor with IM hydroxocobalamin and a cognitive recheck; the subclinical hypothyroidism (TSH 6.8, normal free T4) is retested in 2-3 months with TPO antibodies, and levothyroxine is now prohibited. The donepezil/levothyroxine check and the literature search are gone. Amyloid status is one optional step met by CSF or amyloid PET (positive, Centiloid 81 added). The homocysteine annotation that revealed the MMA result in the initial labs is removed.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: G31.84 expansion grants dementia, PCA, Benson and early-onset labels to this MCI case (plan 5.1).
- New citation keys used: `[NIA_AA_MCI_2011]`, `[BSH_B12_2014]`, `[ETA_SCH_2013]`, `[TRUST_2017]`, `[Beers_2023]`.

## Open questions for Andrea (judgment calls you could not settle)

- Plan C7.3 says "Do not change M04's criterion tier". I read it as "do not change the tiers of existing criteria" and added a recommended MMA criterion for the follow-up that already existed (as in M01..M03), because the B12 must rests on the MMA result. If the lead meant that MMA must stay without a criterion here, delete `action-11-interpret-labs-mma`.

## Verification
Adversarial check, 24 Oct 2026. Read the log, the diff and the whole final case.
- Notes: all ten ids present; each FIXED claim holds (informant field true, cueing field false matching the exam, levothyroxine removed and prohibited, thyroid retest must, B12 replacement must, drug check and literature gone, biomarker alternatives with authored PET). fb473466 ALREADY-FIXED is correct: CSF A+T+N+ values unchanged and the label still "biomarker-supported".
- Found and fixed (MMSE arithmetic, PATTERNS 2 scores): the exam and `initial_tool_outputs.clinical_assessment.findings[1]` listed recall 2 + serial sevens 1 + "one point on orientation to time" = 4 lost points against a total of 25/30, while the same text records two orientation errors (wrong day of the week, date off by four days). Now "two points on orientation to time (day of the week and date)" in `patient.neurological_exam.mental_status` and the finding, so 25/30 adds up; MoCA 21/30 is consistent with its listed deficits plus the two orientation errors.
- Cross-field: homocysteine 19.8 identical in labs and the MMA follow-up; free T4 normal and no longer listed as abnormal; HPI functional rewrite internally consistent (two pickups and one lapse in three months, none in six weeks); B12 regimen (IM hydroxocobalamin, alternate days then every 2 months) matches BSH 2014 for possible neurological involvement with malabsorption.
- Found and fixed: the Fazekas grade 1 white matter finding was described as "punctate and early confluent periventricular hyperintensities" (beginning confluence is Fazekas 2). Reworded to "Thin periventricular caps and pencil-thin lining bilaterally" (`initial_tool_outputs.mri.findings[2].signal_characteristics.T2_FLAIR`), consistent with grade 1 in the size field, impression, criterion and differential.
- Worker's open question on the MMA criterion: settled. C7.3 protects the existing criteria's tiers; the B12 must rests on MMA, and every other case with an MMA follow-up gets the recommended criterion (C7.2), so keeping `action-11-interpret-labs-mma` is correct.
- perfect_agent.py ok; case_io.py check clean; test_case_guards pass.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine_ESR_CRP` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (2 places: the labs criterion label and metadata), the wording the other six cases already use.
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.
