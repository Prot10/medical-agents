# FEPI-TEMP-RM02
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for FEPI-TEMP) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance for focal_epilepsy_temporal (condition_tool_guidance.yaml), applied through plans/FEPI-TEMP.md. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | blocker | `initial_tool_outputs.mri` | Plan class F: the label is "tuber and ipsilateral hippocampal sclerosis (dual pathology)" but the MRI calls the hippocampus "possible asymmetry ... below definitive hippocampal sclerosis threshold" (13% asymmetry) and places the tuber inside the hippocampus, which makes the two lesions inseparable. | FIXED: 3T epilepsy-protocol report: left mesial temporal tuber in the anterior parahippocampal gyrus and uncus, separate from the hippocampal head; definite left HS (2.25 versus 2.85 cm3, 21% smaller, index 0.12, T2/FLAIR hyperintensity, loss of internal architecture, temporal horn enlargement); right frontal tuber, radial migration lines, calcified non-enhancing subependymal nodule, no SEGA; post-contrast line per class E (lesion seen; SEGA question). Volumes chosen not to repeat other FEPI cases. |
| D | major | `patient.history_present_illness` | Sentence on an admission ECG abnormality "prompting additional cardiac workup" with no ECG anywhere in the case. | FIXED: deleted; `metadata.difficulty_description` no longer cites an ECG abnormality from rhabdomyoma. |
| B | minor | `patient.history_present_illness` | "Compliant ... but acknowledges occasionally missing doses" contradicts itself. | FIXED: "acknowledges missing doses several times over the past month". |
| C | major | `followup_outputs[request_pet_scan]` | Plan class J: FDG-PET no criterion orders. | FIXED: deleted; FDG_PET waste avoided action with the canonical rationale. |
| C | major | `initial_tool_outputs.labs` | Prolactin and lactate rows without timing (class M). | FIXED: `Post-ictal` panel removed; summary and interpretation name the low valproate level and the incidental TSH; troponin kept (routine after a convulsion). |
| D | minor | `initial_tool_outputs.eeg` | Teaching sentences ("should not be confused with pathological epileptiform activity", "interictal sensitivity is limited"). | FIXED: report voice; limitations "Routine 30-minute recording with drowsiness and stage 2 sleep; no habitual event captured." |
| C | blocker | `followup_outputs[check_valproic_acid_interactions]` | "Category X" (pregnancy letter categories are withdrawn); "levetiracetam safe in pregnancy"; no sulfonamide warning for zonisamide in a patient with sulfonamide rash; proposal "valproic acid dose increase". | FIXED: proposal is the switch to lamotrigine or levetiracetam; interactions valproate-lamotrigine (doubling, halved titration, rash), ethinylestradiol-lamotrigine (halving, rise in pill-free week, fall after valproate stops), ethinylestradiol-valproate, clobazam; contraindications: valproate malformation and neurodevelopmental risk with the pregnancy prevention programme, zonisamide, carbapenems; warnings on cross-taper and levels. Summary rewritten so it does not repeat the criterion's evidence (leak guard passes). |
| D | blocker | `followup_outputs[search_tsc_epilepsy_management]` | Class O: Krueger 2015 and Curatolo 2018 with invented titles and claims; EXIST-3 numbers misattributed. | FIXED: Northrup 2021 (surveillance), French 2016 EXIST-3 (responder rates 28% and 40% versus 15%), Tomson 2018 EURAP (valproate about 10%, lamotrigine and levetiracetam about 3%); summary rewritten; moved last. |
| C | major | `followup_outputs` (order) | PET, literature, then drug check. | FIXED: drug check, literature. |
| C | major | `ground_truth.action_criteria` | MRI `{contrast: true}`; literature required; drug check template evidence; labs template; rationale = label; duplicate citations. | FIXED per plan tiers: MRI `{protocol: epilepsy}`, routine EEG and drug check required; labs recommended (`AED_levels`, alternative `valproate_level`); literature optional; case-specific evidence; one key each. Order MRI, EEG, labs, drug check, literature. No ECG criterion (no ECG stored). Ids kept. |
| C | minor | `ground_truth.sequence_constraints` | MRI -> drug check with the shared "low-grade tumor" reason and the false Glauser 2017 key. | FIXED: kept (drug check required) with the canonical reason and `[ILAE_MRI_2019]`. |
| C | major | `ground_truth.stop_rule` | Literature listed; max 0. | FIXED: MRI, routine EEG, drug check; max 2. |
| C | major | `ground_truth.assessment.required_recommendations` | Process musts (video-EEG, 3T MRI), a "Recognize ..." diagnostic must, "lacosamide, lamotrigine; consider everolimus" as the first choice, nothing on valproate in a woman of childbearing potential, adherence, TSC surveillance, safety or SUDEP. | FIXED: nine musts: switch from valproate to levetiracetam or lamotrigine with cross-titration; pregnancy prevention programme with highly effective contraception until then; contraception, pregnancy plans and folic acid; adherence as the provocation; TSC surveillance per Northrup 2021; everolimus only if drug-resistant and surgical referral if two ASMs fail; driving; living alone and laboratory safety; SUDEP. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Carbamazepine tied to "TSC psychiatric comorbidities" rather than the contraceptive interaction; "do not biopsy a tuber" (no one would); screening prohibition phrased as a must. | FIXED: no long-term valproate escalation, no abrupt valproate withdrawal, no inducers without changing contraception, no zonisamide (sulfonamide allergy), no panic-attack attribution; screening moved to the musts. |
| C | major | `ground_truth.differential` | FCD II and multifocal TSC `moderate` after an exam and MRI that establish TSC and a concordant left temporal focus; PNES "excluded by capture on video-EEG" (no video-EEG in the case, class S); her own panic-attack attribution absent. | FIXED: extratemporal TSC focus `low`; FCD without TSC, SEGA, panic attacks, PNES, convulsive syncope `very_low`, each with the case finding that excludes it. |
| C | minor | `ground_truth.key_clinical_evidence` | Engineering lines (class G); neuropsychology claim with no neuropsychology output (class S); unsourced percentages; en dashes. | FIXED: five case lines (semiology, dual pathology with concordant EEG, low valproate level, valproate and interaction issues, TSC surveillance). |
| C | minor | `ground_truth.avoided_actions[*]` | Generic rationales; `[AAN_2007]`. | FIXED: case-specific CSF, Holter and CT rationales (CT waste kept: back to baseline, no head injury, MRI available). |
| E | minor | `metadata.difficulty_description`, `.difficulty_rationale` | ECG abnormality and video-EEG/neuropsychology that the case does not contain. | FIXED: describe the case as it now is. |

Note on `perfect_agent.py -v`: the labs criterion prints `<- ?` because the stored lab panels contain null `clinical_significance` fields and the script compares a dump without nulls; there is no labs fallback, so the answer is `initial_tool_outputs.labs` (valproate 38 mcg/mL).

## Changes, in one paragraph a physician can read before re-reviewing

A 29-year-old woman with tuberous sclerosis, seizure-free since 14 on valproate and clobazam and taking a combined pill, has three months of epigastric auras with automatisms and a first convulsion after missed doses. The epilepsy-protocol MRI now shows a left mesial temporal tuber and a separate, definite left hippocampal sclerosis (dual pathology) with other TSC lesions and no SEGA; the routine EEG has rare left anterior temporal sharp transients; the valproate level is 38 mcg/mL (recommended). The required drug check now gives the real interactions of the switch (valproate doubles and ethinylestradiol halves lamotrigine; levetiracetam has none; zonisamide excluded by her sulfonamide allergy) and the valproate pregnancy risk, without "Category X". PET, prolactin, lactate and the phantom ECG are gone. Musts: switch from valproate within a pregnancy prevention programme, adherence, TSC surveillance, everolimus only for drug resistance with surgical referral if two ASMs fail, driving, safety, SUDEP.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Criteria pack allow-list: `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[EURAP_2018]`, `[TSC_2021]` (plan CENTRAL 2).
- `perfect_agent.py` `_source` prints `<- ?` for stored outputs with null fields (see FEPI-TEMP-RM01 log).

## Open questions for Andrea (judgment calls you could not settle)

None. Departure from the plan: TSH 4.8 mIU/L with normal free T4 was kept as an incidental finding (the plan's stray-row deletion is for RM01); a surgical-referral clause was added to the everolimus must because the MRI shows a resectable concordant lesion.

## Verification

Adversarial check, 24 Oct 2026. Read the log, the diff and the whole final case. Checked: tuber and hippocampal sclerosis are separate lesions in findings, impression, criterion evidence, KCE and label; volumetric arithmetic (0.60/5.10 = 0.12, 1 - 2.25/2.85 = 21%) is right, with the index definition written out (R - L) for the left-sided lesion; the post-contrast line is the class E canonical text for a lesional case; no ECG sentence remains and no ECG criterion exists (no ECG stored); valproate 38 mcg/mL matches labs, criterion and KCE; the drug output agrees with facts 7 to 9 and the sulfonamide allergy (zonisamide contraindicated and prohibited); pregnancy prevention, contraception, TSC surveillance (Northrup 2021) and EXIST-3 figures are correct; differential is the assessment-time view; FDG-PET follow-up gone with FDG_PET waste added; "15 seizure-free years" fits seizure-free since 14 at age 29.
Found and fixed: class H not finished: the labs criterion listed `[NICE_NG217_2025]` and the unbracketed `NICE_NG217_2025`; the duplicate removed. Checks pass after the edit.

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.
- `action-4-search-medical-literature.rationale`: engineering prefix or tier wording removed (was "Optional background; the diagnosis rests...").
- Differential "Subependymal giant cell astrocytoma": ICD-10-CM D33.0 -> D43.0.

## Close-out (24 Oct 2026)

Condition close-out (`plans/FEPI-TEMP-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G40 entries, re-applied with `--prune --conditions focal_epilepsy_temporal`): labels now focal epilepsy, temporal lobe epilepsy, TLE, epilepsy temporal lobe, mesial temporal lobe epilepsy, MTLE (added), mesial temporal sclerosis epilepsy; removed focal seizures; focal onset seizures; focal impaired awareness seizures (seizure-type labels, retired: their tokens occur in an acute symptomatic or functional-seizure answer). Codes: G40.2, G40.1, G40.9 plus G40.209, G40.109, G40.909 (not intractable); the idiopathic G40.009 and G40.019 removed and the intractable codes removed.
- Label (summary CENTRAL 16): the em dash in accepted[0] ("hippocampal sclerosis — dual pathology") replaced by a comma.
- Soft MRI -> drug check constraint: citation `[ILAE_MRI_2019]` -> `[NICE_NG217_2025]`, as in the other cases (ASM choice is what the constraint is about; auditor flag).
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FEPI-TEMP-` passes, now with the discriminator guard and the FEPI-TEMP banned strings.

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-7-interpret-labs]`.expected_evidence: was "Valproic acid 38 mcg/mL, below range, consistent with the missed doses; normal ammonia, liver enzymes and platelets."; now "Valproic acid 38 mcg/mL, below range, consistent with the missed doses.".
- Decision: trim evidence. Ammonia, liver enzymes and platelets are valproate safety bloods, not the level this order names; their panels stay servable to an agent that orders them.
- Scoring: none (evidence only; the reward does not read it).

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.

## Library contradictions (25 Oct 2026)

Orders the benchmark library answered with a normal report that contradicts this case now get a case-specific report (term: gist, where stored):

- analyze_eeg ambulatory: This is an ABNORMAL 48-hour ambulatory EEG due to: 1. Occasional left anterior temporal sharp waves (phase reversal at F7), mainly in NREM sleep. 2. I (fallback_tool_outputs.eeg)
- analyze_eeg video: This is an ABNORMAL 72-hour video-EEG due to: 1. One habitual seizure of left anterior temporal onset (F7/T3): rhythmic 5-6 Hz theta evolving to 2-3 H (followup request_video_eeg)
- order_advanced_imaging FDG_PET: 1. Left mesial and anterior temporal hypometabolism, most marked in the anterior parahippocampal gyrus and uncus. 2. Small focus of right superior fro (fallback_tool_outputs.advanced_imaging)
- obtain_tissue_diagnosis resection: Cortical tuber (fallback_tool_outputs.tissue_diagnosis)
- obtain_tissue_diagnosis stereotactic_biopsy: Cortical tuber (followup request_stereotactic_biopsy)
- obtain_tissue_diagnosis open_biopsy: Cortical tuber (followup request_open_biopsy)
- order_specialized_test neuropsych_battery: Weakness in verbal learning and delayed verbal recall (T-scores 34 and 31) and mild confrontation naming weakness (BNT T-score 39), with visual memory (fallback_tool_outputs.specialized_test)
- order_echocardiogram TTE: small septal intramyocardial nodule (rhabdomyoma), normal function (fallback_tool_outputs.echo)
- order_echocardiogram TEE: 1. Small homogeneous intramyocardial septal nodule without obstruction, in keeping with a small cardiac rhabdomyoma. 2.  (followup request_tee)

Checks: `perfect_agent.py` passes; the criterion snapshot of the case is unchanged; `pytest agent-platform/tests -k FEPI-TEMP` (case guards included), `test_reports_do_not_fabricate.py` and `apply_diagnosis_synonyms.py --check` pass; no new report repeats a 60-character window of any criterion's expected evidence.
