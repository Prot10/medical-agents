# ALZ-EARLY-S04
Reviewer status: R1 not reviewed, R2 not reviewed (no notes for this case) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The case has no reviewer notes. The condition-plan classes C1 to C16 were applied as a class (ruling 2); see Own findings. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | minor | staging (C4) | Checked: his wife has taken over bill paying and the checkbook and restricts his driving; IADL field true is consistent; mild dementia, onset about 79, G30.1 correct. | No change to label, ICD or field. |
| D | major | initial_tool_outputs.clinical_assessment.impression, .findings, .scores | Template impression with the engineering sentence; fragment rows ending in ";"; the driving incident and clothing prompts missing. | FIXED: impression from the case (MMSE 21/30 domains, no benefit from category or multiple-choice cues, wife's report, finances taken over, driving restricted); rows rebuilt. Cueing field false kept (consistent). |
| E | minor | patient.history_present_illness, patient.neurological_exam.mental_status | "is a 81-year-old"; "delayed copy of intersecting pentagons" (pentagon copy is not a delayed item). | FIXED: "an 81-year-old"; "copy of intersecting pentagons". |
| B | major | initial_tool_outputs.labs.panels.BMP (chloride) | Chloride 110 with sodium 140 and CO2 27 gives an anion gap of 3 (implausible), unaddressed anywhere. | FIXED: chloride 103; summary and interpretation updated (BUN 21, glucose 122, HbA1c 6.3% remain). |
| B | minor | initial_tool_outputs.labs.panels | CMP ordered, BMP returned; CBC indices (Hct 40.2/RBC 4.43 = 91 fL vs MCV 85.5; Hct/Hb ratio 2.8); template reviewed-panel values. | FIXED: CMP with hepatic values (normal); RBC 4.95, Hct 43.4, MCV 87.7; magnesium 2.2, homocysteine 11.8, ESR 19 (reference 0-40 for a man of 81), CRP 1.4. |
| C | minor | (C7.2 check) | B12 340 pg/mL on metformin with normal homocysteine: not in the low-normal band; no MMA criterion. The generic B12 key-evidence item was removed (C10). | No MMA criterion. |
| D | major | initial_tool_outputs.mri | "No abnormal leptomeningeal or parenchymal enhancement" with contrast false (C5); "Patent intracranial vasculature on MRA" (not part of the protocol); "in the setting of vascular risk factors" (cross-modality); impression argued the differential ("exceeds what would be expected from vascular disease alone"). | FIXED: lines removed; risk-factor clause removed; numbered impression with Kind 2 statements only. |
| B | major | ground_truth.differential[Vascular cognitive impairment] | "No significant cerebrovascular burden" while the MRI shows Fazekas 1-2. | FIXED: low, with Fazekas 1-2 named as a possible contributor and no infarcts or microbleeds. |
| C | major | ground_truth.differential (C11) | DLB and FTD moderate without features. | FIXED: low with excluding features; depression low (GDS 3/15); reversible causes low, the weight loss named as needing its own evaluation. |
| C | major | ground_truth.assessment, patient weight loss | The unintentional 5-lb weight loss in six months was not addressed anywhere, although a cholinesterase inhibitor can worsen anorexia. | FIXED: must to evaluate and monitor weight; drug-check output and AChEI must mention baseline weight. |
| B | minor | followup_outputs[neuropsych].impression (C4) | "Amnestic mild cognitive impairment, multi-domain type" in a dementia case; em dash. | FIXED: canonical C4 wording; RAVLT recognition 4th percentile added. |
| B | minor | followup_outputs[CSF] (C6) | 14-3-3, RT-QuIC, "N/A"; glucose ratio 0.58 for 72.6/118 = 0.62; non-vocabulary keys. | FIXED; values otherwise unchanged. |
| C | major | action-8-analyze-csf (C2) | Single route; PET would have returned the library's negative PET. | FIXED: CSF or amyloid PET alternatives; follow-up `order_amyloid_pet` (florbetaben, positive, centiloid 88). Probe: alt1 <- `request_csf_biomarkers`, alt2 <- `order_amyloid_pet`. |
| C | minor | followup_outputs (plan Q4) | FDG-PET would have returned a normal library study. | FIXED: concordant `order_fdg_pet` follow-up, no criterion; verified served from the case. |
| B | major | followup_outputs[drug check], action-9 (C1.2) | Heart rate 76 vs vitals 72; criterion matched any drug. | FIXED: optional, `{"drug": "donepezil"}`, last; output with HR 72, tamsulosin, aspirin, weight loss, beta-blocker note. Leak guard passes. |
| C | major | ground_truth.assessment (C12) | Restating musts, engineering biomarker must, generic prohibitions; no AChEI or vascular must. | FIXED: musts are informant, driving evaluation and supervision, disclosure, AChEI trial [NICE_NG97], weight-loss evaluation, vascular risk management, biomarker offer. Prohibitions: attributing to normal aging; memantine at the mild stage. ACE-inhibitor angioedema checked: no must prescribes an ACE inhibitor. |
| C | minor | key_clinical_evidence (C10) | Generic items (MRI "sufficient", APOE, B12). | FIXED: four items true for this case. |
| A | minor | citations and rationales (C13) | Duplicates; rationale copied from label. | FIXED; expected evidence states this case's results. |
| C | minor | sequence_constraints, stop_rule (C16) | | FIXED: clinical assessment before biomarker added; MRI before CSF kept; max_additional_actions 1. |
| E | minor | fallback literature, metadata, avoided rationales | | FIXED: literature fallback null; metadata updated; patient-specific rationales. Other fallbacks normal and consistent, kept. |

## Changes, in one paragraph a physician can read before re-reviewing
Diagnosis and staging are unchanged (mild Alzheimer dementia, amnestic, G30.1; his wife has taken over the finances and restricts his driving). The bedside assessment and neuropsychology impression now describe his own results (no benefit from cues, added recognition score), and the neuropsychology report no longer says MCI. A chloride of 110 that gave an impossible anion gap was corrected; the CMP now has hepatic values and the red-cell indices agree. The MRI no longer mentions enhancement or MRA and no longer argues the differential; mild-to-moderate small vessel disease is named, and the differential treats it as a possible contributor. Amyloid status is optional by CSF or a new concordant positive amyloid PET, with a concordant FDG-PET if ordered. Musts now include a formal driving evaluation, a cholinesterase-inhibitor trial with tamsulosin and weight counseling, evaluation of his unintentional weight loss, and vascular risk management.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Synonyms: PCA, Benson and early-onset labels and G30.0 in a late-onset amnestic case (plan 5.1).
- Citation key `[NICE_NG97]` (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Checked against the plan (C1 to C16, sections 3.1 to 3.6) and PATTERNS.md: log claims against the file, criterion order and tiers, the biomarker criterion's two alternatives each answered by a case-authored follow-up (CSF and amyloid PET, plus a concordant FDG-PET), fallbacks (advanced_imaging, literature and drug_interactions null where required; the remaining Holter, CT, ECG, echo and EEG fallbacks read), CSF arithmetic (Abeta42/40 ratio, CSF/serum glucose ratio), CBC indices, musts and prohibitions against allergies, medicines and avoided actions, the differential against the final evidence, and leakage of expected evidence into any-query outputs (test_case_guards passes).
Found and fixed:
- patient.neurological_exam.mental_status and clinical_assessment.findings[1]: the exam says he "fails three-step commands" but the listed MMSE items already sum to 21/30; serial sevens set to 2 errors and the three-stage command point added. Score unchanged.
- followup_outputs[CSF]: total tau 520 and serum glucose 118 were identical to S02 and S03; total tau 498 and serum glucose 122 (his panel value; ratio 72.6/122 = 0.60); interpretation updated. Abeta42/40 362/7850 = 0.046 verified.
Checked and correct: losartan with an ACE-inhibitor angioedema allergy is acceptable (no must prescribes an ACE inhibitor); weight-loss must is case-grounded (5 lb in six months) and the donepezil anorexia warning agrees; HbA1c 6.3% on metformin alone carries no hypoglycemia risk; B12 340 with normal homocysteine needs no MMA; heart rate 72 matches the drug check.
Flag for the lead: near-duplicate of S02 and S03 (see the S02 verification).
perfect_agent.py -v and case_io.py check: clean after the edits.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine_ESR_CRP` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (2 places: the labs criterion label and metadata), the wording the other six cases already use.
- MMSE orientation: 2 points were lost but only the date error was named; the second error (day of the week) is now stated in the exam and in clinical assessment findings[0], so the items sum to the stated total.
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`--prune --conditions alzheimers_early`): removed "posterior cortical atrophy" and "benson syndrome"; "early onset alzheimer" and code G30.0 (onset at 65 or later); code G30.8 (atypical presentations only). Added "late onset alzheimer". Now: codes ['G30.1', 'G30.9', 'F00']; labels after accepted[0]: ['alzheimer disease', "alzheimer's disease", 'alzheimers disease', 'alzheimer dementia', 'dementia due to alzheimer', 'late onset alzheimer'].
- Dataset diversity (as S03): "retired postal carrier" -> "retired city bus driver". No clinical content changed.
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although this case contradicts it (diagnosis, history, medications or a stored finding) now get a case-specific report; every other off-pathway order still gets the library normal. No tier, criterion, diagnosis or existing output changed.

- `order_advanced_imaging modality=tau_PET` -> `followup_outputs[order_tau_pet]`: case-specific tau-positive flortaucipir PET with the distribution of the stored FDG-PET pattern.
- `order_advanced_imaging modality=perfusion_SPECT` -> `followup_outputs[order_perfusion_spect]`: regional hypoperfusion matching the stored FDG-PET hypometabolism.
- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: language findings of the stored neuropsychological battery (naming, fluency) in the speech-language format.
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[order_performance_status]`: dementia-stage performance status (Karnofsky 70/ECOG 1; 60/2 in the rapidly progressive case) instead of Karnofsky 100.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k ALZ-EARLY` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
