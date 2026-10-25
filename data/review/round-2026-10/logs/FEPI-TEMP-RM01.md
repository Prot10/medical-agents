# FEPI-TEMP-RM01
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for FEPI-TEMP) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance for focal_epilepsy_temporal (condition_tool_guidance.yaml), applied through plans/FEPI-TEMP.md. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | blocker | `initial_tool_outputs.mri.findings[1]`, `followup_outputs` (PET), EEG `background.symmetry`, `metadata.case_body_concerns` | Lifelong LEFT hemiparesis with a LEFT frontoparietal encephalomalacia on MRI and PET and lower voltage over the LEFT hemisphere on both EEGs: a left hemiparesis needs a right hemispheric lesion (the metadata AUDIT-FLAG said so). | FIXED: encephalomalacia right frontoparietal (MRI and the new CT), ex vacuo dilatation of the right lateral ventricle; EEG amplitude reduction over the right frontal and central regions in both studies; PET deleted (see below); AUDIT-FLAG removed from `case_body_concerns` as resolved. |
| C | major | `patient.history_present_illness` | Plan class N: postictal "new right arm weakness" (Todd paresis on the side opposite the right hemispheric focus would be the left arm); "fixed stare to the right" before generalization against a right temporal onset (late forced version is contralateral). | FIXED: forced head and eye version to the left before the convulsion; postictal worsening of the baseline left arm weakness, back to baseline over two hours. Right-hand automatisms kept (ipsilateral, consistent). |
| C | blocker | `initial_tool_outputs.mri` | Plan class F: equivocal 1.5T-style report ("may represent early sclerosis", "cannot be confirmed", asymmetry "22%" mislabelled as an index) while the label rests on HS and dual pathology; "No abnormal contrast enhancement" in an HS case (class E). | FIXED: 3T epilepsy-protocol report with definite right HS (volume loss 2.8 versus 3.6 cm3, T2/FLAIR hyperintensity, loss of internal architecture, temporal horn enlargement), index 0.13 = (3.6 - 2.8)/6.4 and 22% = 1 - 2.8/3.6, right frontoparietal encephalomalacia, catheter tip in the right frontal horn, no hydrocephalus, white matter foci and partially imaged cervical changes kept; no gadolinium. |
| C | major | `initial_tool_outputs.ct` (new), `ground_truth.action_criteria` (`action-ct-shunt-check`, new), `ground_truth.avoided_actions` | CT listed as waste although he is shunted and has weeks of headache before a first convulsion (fact 3); a must asked to "confirm VP shunt is functioning (imaging review)", which no criterion scored. | FIXED: CT waste deleted; new recommended `order_ct_scan` criterion, first in the criteria order, answered by a stored CT (catheter tip in the right frontal horn, no hydrocephalus or transependymal edema, chronic right frontoparietal encephalomalacia, no hemorrhage); the generic CT fallback set to null and its `fallback_tool_kinds` entry removed; the shunt must deleted. |
| C | minor | `patient.neurological_exam.cranial_nerves` | No fundoscopy in a shunted patient with headaches, although the differential relies on the absence of papilledema. | FIXED: "Fundi: sharp optic disc margins, no papilledema." |
| B | minor | `patient.neurological_exam.mental_status` | MoCA 24/30 with listed losses summing to 4 (26/30). | FIXED: losses on delayed recall (2/5, 3 points), trail-making, fluency, serial sevens and abstraction (7 points) plus the education point = 24/30. |
| D | major | `initial_tool_outputs.eeg.impression` | Breach rhythm "likely related to prior craniotomy" (he had no craniotomy). | FIXED: "at the shunt burr-hole site"; impression in report voice. |
| D | major | `followup_outputs[request_sleep_deprived_eeg]` | Plan class K: limitations report a subclinical seizure the impression denies; impression identical to M01 and M02; interpretive `clinical_correlation`; no electrode detail. | FIXED: frequent right anterior temporal discharges with phase reversal at F8, about 10 per hour in NREM sleep, breach rhythm; own impression; limitations "60-minute sleep-deprived recording reaching NREM stage 2; no habitual event captured". |
| C | major | `followup_outputs[request_pet_scan]` | Plan class J: FDG-PET no criterion orders, describing a left frontoparietal lesion that does not exist. | FIXED: deleted (not moved to the fallback); FDG_PET waste avoided action added with the canonical rationale. |
| C | major | `initial_tool_outputs.labs` | Prolactin row (class M); CK, lactate and a subclinical TSH rise that nothing in the case uses (metadata called TSH a red herring, but it was not one). | FIXED: `post_ictal_markers` and `thyroid_panel` panels removed; summary and interpretation now list only the mildly raised glucose. |
| D | blocker | `followup_outputs[search_temporal_lobe_epilepsy_treatment]` | Class O: Kanner 2018 cited for "Level A evidence for lamotrigine and levetiracetam" (wrong, fact 6); ERSET and Blumcke 2013 with misstated content and titles. | FIXED: Marson 2021 (SANAD II), Glauser 2013 (Level A for carbamazepine, levetiracetam, phenytoin, zonisamide; lamotrigine only in the elderly), Blumcke 2013 with its real title; summary rewritten; moved last. |
| E | minor | `followup_outputs[check_*_interactions]` | Em dashes in formulary and warnings; warning about "baseline mild encephalopathy" repeated. | FIXED: rephrased without dashes; content kept (baclofen additive sedation, lamotrigine titration and rash). |
| C | major | `followup_outputs` (order) | PET, literature, two drug checks, then the sleep-deprived EEG. | FIXED: sleep-deprived EEG, levetiracetam check, lamotrigine check, literature. |
| C | major | `ground_truth.action_criteria` | MRI `{contrast: true}`; literature and drug check required; template evidence everywhere; rationale = label; duplicate citations. | FIXED per plan tiers: CT recommended (new), MRI `{protocol: epilepsy}` and routine EEG required, sleep-deprived EEG recommended, labs, drug check and literature optional; case-specific evidence; one key each. Order CT, MRI, routine EEG, sleep-deprived EEG, labs, drug check, literature. Ids kept. |
| C | major | `ground_truth.sequence_constraints`, `.stop_rule` | MRI -> drug check soft with the "low-grade tumor" reason while the drug check is optional (class C); max 0 with literature and drug check required. | FIXED: constraint deleted; stop rule MRI and routine EEG, max 2. |
| C | major | `ground_truth.assessment.required_recommendations` | Process musts (video-EEG, 3T MRI, shunt imaging) and a "Recognize ..." diagnostic must; ASM list including lacosamide as first line. | FIXED: five musts: levetiracetam or lamotrigine first line (no interaction with baclofen or omeprazole; mood and sedation with his cognitive impairment), check and reset a programmable shunt valve after the 3T MRI, driving, warehouse work safety, SUDEP (focal to bilateral tonic-clonic seizure). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Carbamazepine-hyponatremia "from meningitis sequelae" (no hyponatremia in the case); valproate prohibition framed only as an IGE error. | FIXED: carbamazepine line deleted (plan); canonical valproate prohibition (MHRA 2024, under 55); shunt LP prohibition kept. |
| C | major | `ground_truth.differential` | "Post-traumatic epilepsy from prior cervical surgery" (cervical surgery cannot cause epilepsy); perinatal injury without HS `moderate` after an MRI that shows HS; the mother's generalized epilepsy, raised by the history, absent. | FIXED: extratemporal epilepsy from the encephalomalacia `low`, shunt malfunction `low` (no papilledema, reservoir refills, no hydrocephalus; ICD T85.09XA), genetic generalized epilepsy `very_low`, PNES and convulsive syncope `very_low`, each with the excluding finding. |
| C | minor | `ground_truth.key_clinical_evidence` | Engineering lines (class G); generic lines; em dash. | FIXED: five case lines (semiology, lateralizing signs, dual pathology explaining the hemiparesis, EEG sequence, CT). |
| C | minor | `ground_truth.red_herrings[0].correct_interpretation` | Did not say why the hemiparesis is irrelevant. | FIXED: lifelong and stable from the right hemispheric injury; cervical surgery unrelated. Path and data point unchanged. |
| C | minor | `ground_truth.avoided_actions[*]` | Generic rationales; `[AAN_2007]`. | FIXED: case-specific CSF (with the shunt caveat), TTE and Holter rationales. |
| A | minor | `fallback_tool_outputs.echo` | No `echo_type` (class I). | FIXED: `"echo_type": "TTE"`. |
| E | minor | `metadata.difficulty_description`, `.difficulty_rationale` | TSH red herring and "video-EEG follow-up" that the case does not contain. | FIXED: describe the case as it now is. |

Note on `perfect_agent.py -v`: the CT and MRI criteria print `<- ?` because the stored reports contain null fields (`borders`, `size`, `density`) and the script's attribution compares a dump without nulls; the calls are answered from the case (not from a fallback: the CT and MRI fallbacks are null), so the evidence comes from `initial_tool_outputs.ct` and `.mri`.

## Changes, in one paragraph a physician can read before re-reviewing

A 24-year-old man with neonatal pneumococcal meningitis, a VP shunt and a lifelong left hemiparesis has two months of olfactory auras and focal impaired awareness seizures (lip-smacking, right-hand automatisms) and a first focal to bilateral tonic-clonic seizure that now begins with forced leftward version and is followed by transient worsening of the left arm (previously a new right arm weakness). The hemispheric lesion is now right frontoparietal everywhere, matching the left hemiparesis. The work-up starts with a recommended head CT that excludes shunt failure, then an epilepsy-protocol MRI with definite right hippocampal sclerosis plus the right frontoparietal encephalomalacia (dual pathology, no gadolinium), an equivocal routine EEG and a recommended sleep-deprived EEG with definite right anterior temporal discharges; labs, drug checks and literature are optional, FDG-PET is waste. Prolactin, CK, lactate and TSH rows are gone. Musts: levetiracetam or lamotrigine, programmable valve check after the 3T MRI, driving, warehouse safety, SUDEP; prohibitions: valproate, lumbar puncture before shunt function is confirmed.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Criteria pack allow-list: `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[SANAD2_2021]` (plan CENTRAL 2).
- `perfect_agent.py` `_source`: compares `model_dump()` of the served output with `initial_tool_outputs.model_dump(exclude_none=True)`, so any stored report with a null field prints `<- ?`; dump both the same way.

## Open questions for Andrea (judgment calls you could not settle)

None. Departures from the plan: the CT criterion is placed first in the criteria order (the plan lists RM01 with the elective cases, but he presented to the emergency department with headaches and a shunt, so CT comes first clinically); the laterality of the encephalomalacia was corrected (not listed in the plan, but flagged in the case metadata and anatomically required by the left hemiparesis); a programmable-valve check after the 3T MRI and a work-safety must were added.

## Verification

Adversarial check, 24 Oct 2026. Read the log, the diff and the whole final case. Checked: the right hemispheric lesion is consistent everywhere with the left hemiparesis (MRI, CT, both EEG asymmetries, breach rhythm over the right parietal burr hole, shunt palpable right parietal, KCE, differential); the Todd paresis is now the left arm and the forced version leftward; the MRI arithmetic (index 0.8/6.4 = 0.13, 1 - 2.8/3.6 = 22%) is right; the CT criterion is answered by the stored CT (no CT fallback); toxicology and glucose 102 in the labs match the labs criterion evidence; prolactin, CK, lactate and TSH rows are gone; Glauser 2013 Level A list and SANAD II are stated correctly; the valproate prohibition is canonical; no FDG-PET follow-up remains and FDG_PET waste is present.
Found and fixed: (1) MoCA arithmetic still wrong: with "serial sevens (1 error)" four subtractions are correct, which scores the full 3 points, so the listed losses were 3 + 1 + 1 + 0 + 1 = 6 and the total 25/30, not 24/30; changed to "serial sevens (2 errors)" (3 correct = 2 points), so losses are 7 and 23 + 1 education point = 24/30 as stated, matching the log's own Own-findings line. (2) Class H: the labs criterion still had the unbracketed duplicate `NICE_NG217_2025`; removed. Checks pass after the edit.

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.
- `action-8-interpret-labs.rationale`: engineering prefix or tier wording removed (was "Optional: a first convulsion is routinel...").
- `action-5-check-drug-interactions.rationale`: engineering prefix or tier wording removed (was "Optional: his medicines have no interact...").
- `action-4-search-medical-literature.rationale`: engineering prefix or tier wording removed (was "Optional background; the diagnosis rests...").
- Sleep-deprived EEG follow-up and criterion: "frequent" discharges at about 10 per hour are "occasional" (ACNS 2021).
- Literature follow-up (served for any query): query and HS classification result named this case's MRI finding; now first-line ASM evidence only; criterion evidence updated.

## Close-out (24 Oct 2026)

Condition close-out (`plans/FEPI-TEMP-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G40 entries, re-applied with `--prune --conditions focal_epilepsy_temporal`): labels now focal epilepsy, temporal lobe epilepsy, TLE, epilepsy temporal lobe, mesial temporal lobe epilepsy, MTLE (added), mesial temporal sclerosis epilepsy; removed focal seizures; focal onset seizures; focal impaired awareness seizures (seizure-type labels, retired: their tokens occur in an acute symptomatic or functional-seizure answer). Codes: G40.2, G40.1, G40.9 plus G40.209, G40.109, G40.909 (not intractable); the idiopathic G40.009 and G40.019 removed and the intractable codes removed.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FEPI-TEMP-` passes, now with the discriminator guard and the FEPI-TEMP banned strings.

## Library contradictions (25 Oct 2026)

Orders the benchmark library answered with a normal report that contradicts this case now get a case-specific report (term: gist, where stored):

- analyze_eeg ambulatory: This is an ABNORMAL 48-hour ambulatory EEG due to: 1. Right anterior temporal sharp waves (phase reversal at F8), maximal in NREM sleep. 2. Intermitte (fallback_tool_outputs.eeg)
- analyze_eeg video: This is an ABNORMAL 72-hour video-EEG due to: 1. Right anterior temporal sharp waves (phase reversal at F8), maximal in NREM sleep. 2. Intermittent ri (followup request_video_eeg)
- order_advanced_imaging FDG_PET: 1. Right mesial and anterior temporal hypometabolism. 2. Right frontoparietal photopenic defect with surrounding cortical hypometabolism and mild cros (fallback_tool_outputs.advanced_imaging)
- obtain_tissue_diagnosis resection: Hippocampal sclerosis, ILAE type 1 (fallback_tool_outputs.tissue_diagnosis)
- obtain_tissue_diagnosis stereotactic_biopsy: Hippocampal neuronal loss with fibrillary gliosis (followup request_stereotactic_biopsy)
- obtain_tissue_diagnosis open_biopsy: Hippocampal neuronal loss with fibrillary gliosis (followup request_open_biopsy)
- order_specialized_test neuropsych_battery: Low average intellectual functioning (FSIQ 82) with impaired visual memory, visuospatial construction, phonemic fluency and executive function; verbal (fallback_tool_outputs.specialized_test)
- perform_clinical_assessment cognitive_screen (baseline): MoCA 24/30, below the normal cut-off, with losses in delayed recall, attention, fluency, trail-making and abstraction. (fallback_tool_outputs.clinical_assessment)
- interpret_labs AED_levels: No levetiracetam, valproate, carbamazepine, phenytoin, lamotrigine or lacosamide detected. (fallback_tool_outputs.labs[AED_levels], also answers valproate_level)

Checks: `perfect_agent.py` passes; the criterion snapshot of the case is unchanged; `pytest agent-platform/tests -k FEPI-TEMP` (case guards included), `test_reports_do_not_fabricate.py` and `apply_diagnosis_synonyms.py --check` pass; no new report repeats a 60-character window of any criterion's expected evidence.
