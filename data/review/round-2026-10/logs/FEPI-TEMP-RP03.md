# FEPI-TEMP-RP03
Reviewer status: no reviewer notes for FEPI-TEMP (R1 and R2 never reviewed this condition in a notes round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input is the July 2026 tool guidance (plan 1.3), applied through plans/FEPI-TEMP.md. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.mri` | The brain MRI reported vertebral metastases (T4, T7, T11, L2, L4) with STIR signal; "edema ... may contribute to seizure susceptibility" (clinical inference); "homogeneous ring enhancement"; no technique or comparison line. | FIXED: spine finding, observation and impression text removed; rim enhancement with a non-enhancing centre, SWI negative for hemorrhage; technique, comparison (0.5 cm 4 months ago), patent cisterns, pituitary normal; numbered impression. |
| B | major | `patient.history_present_illness`, `patient.neurological_exam` | Right hip flexion 4+/5, right dorsiflexion 5-/5 and right patellar 1+ (a right L3-L4 pattern) with bilaterally increased lower-limb tone and an equivocal right plantar, unexplained once the spine leaves the brain MRI. | FIXED: HPI adds the staging spine MRI two weeks ago (vertebral metastases including L2 and L4, right L3-L4 foraminal tumor, no cord compression or epidural disease) and right groin and anterior thigh aching; tone normal; plantars flexor; mild pinprick loss over the right anterior thigh and medial shin; heel-to-shin slowed by hip flexor weakness. |
| B | major | `followup_outputs` CSF | WBC 8, protein 73 and a CSF/serum glucose ratio of 0.44 (a low ratio suggests leptomeningeal disease) while the criterion expected "cytology positive ... or immune-mediated inflammation"; "VGKC complex" antibodies. | FIXED: WBC 3, protein 52, glucose 88 with serum 142 (ratio 0.62); cytology, flow cytometry, oligoclonal bands, IgG index, neuronal surface (cell-based) and paraneoplastic panels negative, Gram stain and culture negative; interpretation notes that one negative cytology does not exclude leptomeningeal disease. |
| C | major | `followup_outputs` FDG-PET, `action-7-order-advanced-imaging` (class J) | PET criterion (recommended) and follow-up whose impression adjudicated "viable tumor rather than treatment-related change". | FIXED: criterion and follow-up deleted; report moved to `fallback_tool_outputs.advanced_imaging` (`FDG_PET`, SUVmax 9.6 instead of RP01's identical 12.4, adjudication removed); `avoid-waste-fdg-pet` with the plan's rationale. |
| D | minor | `initial_tool_outputs.eeg` (class K) | "Breach rhythm" in a patient who never had a craniotomy; impression cited the "known structural lesion" (cross-modality) and ended with a sensitivity note. | FIXED: breach rhythm removed; impression numbered, own findings only; limitations line for a 40-minute routine study. |
| D | major | `initial_tool_outputs.labs` (class M) | Prolactin 42 ng/mL with no timing; levetiracetam 8.2, CRP 18.4, neutrophils 78% and albumin 3.4 identical to RP01 or RP02 (template carry-over). | FIXED: prolactin deleted; levetiracetam 5.9, CRP 11.6, neutrophils 81%, lymphocytes 11%, albumin 3.3; panels `AED Levels` and `Additional Labs`; interpretation names the normal free T4 and electrolytes. |
| B | minor | `initial_tool_outputs.ecg` (class T) | "Sinus tachycardia borderline (86 bpm)"; T-wave change attributed to "metabolic or medication effects"; stale `clinical_correlation`. | FIXED: "Normal sinus rhythm, 86/min"; interpretation factual; field removed. |
| C | major | `fallback_tool_outputs.ct`, `avoid-waste-3-order-ct-scan` | CT scored as waste in a cancer patient with seizures (fact 3, class I); fallback CT showed a benign frontal granuloma and no metastasis. | FIXED: avoided action deleted; fallback CT shows the 1.6 cm left temporal lesion with edema, no hemorrhage or shift, MRI recommended; `fallback_tool_kinds.ct` = `case`. Echo fallback `echo_type: TTE`. |
| C | major | `followup_outputs` drug check | "Lacosamide primarily hepatically metabolized via CYP2C19" (about 40% renal unchanged); no word on escitalopram, BRAF/MEK inhibitors or the sulfonamide allergy. | FIXED: levetiracetam and lacosamide with her medicines, lacosamide PR with escitalopram QT, lacosamide elimination stated correctly, inducers with dexamethasone, dabrafenib/trametinib and escitalopram, zonisamide contraindicated (sulfonamide rash), steroid dose and ICI efficacy, escitalopram hyponatremia; trigger renamed. Recommended (class B). |
| D | major | `followup_outputs` literature (classes A, O) | Required; three unattributed 2022-2024 sources with unverifiable figures and patient-level conclusions. | FIXED: optional, last; Brahmer 2018 (ASCO irAE) and NICE NG217 only; general statements; expected evidence worded so the leak guard passes. |
| A | major | `ground_truth.action_criteria` (classes A, B, E, H, T) | MRI `{contrast: true, protocol: epilepsy}`; CSF required with three assays; literature, drug check, ECG required; template evidence; doubled citations. | FIXED: order MRI, EEG, labs, ECG, CSF, drug check, literature. Required: MRI `{contrast: true}`, routine EEG. Recommended: labs (`AED_levels`, `TSH` or `thyroid`), CSF (`cytology` or `autoimmune_panel`), drug check. Optional: ECG, literature. One key each; case-specific evidence. |
| A | minor | `ground_truth.sequence_constraints`, `.stop_rule` (classes C, D) | Template constraint reason; stop rule with literature, drug check, ECG, CSF, max 0. | FIXED: hard MRI -> CSF (canonical reason), soft MRI -> drug check (canonical reason); stop rule MRI and EEG; max 2. |
| C | major | `ground_truth.assessment` (class L) | Process musts (contrast MRI, CSF); "possible high-dose steroids for ICI neurotoxicity" although the work-up excludes it; no adherence plan, thyroid plan, spine plan. | FIXED: musts: non-inducing ASM with the adherence problem addressed (lacosamide switch or add-on, or higher levetiracetam), oncology and radiation oncology for radiosurgery or resection, ICI continuation and lowest dexamethasone dose, radiation oncology for the L3-L4 foraminal metastasis, thyroid follow-up per ASCO, driving. Prohibitions: LP before imaging, inducers, zonisamide, high-dose steroids for presumed ICI encephalitis, attributing the episodes to fatigue or anxiety. |
| C | major | `ground_truth.differential` (class P) | ICI encephalitis `high` and leptomeningeal disease `moderate` after CSF; hypophysitis coded E23.0; no entry for the weakness or for pseudoprogression. | FIXED: ICI encephalitis, leptomeningeal disease, pseudoprogression (added), immune polyradiculoneuropathy (added), hypophysitis (E23.6) `low`; paraneoplastic limbic encephalitis and stroke `very_low`; each with its excluding finding. |
| E | minor | `ground_truth.key_clinical_evidence` (class G) | Generic lines, PET claim, two July-review engineering lines. | FIXED: six case-specific statements. |
| B | minor | `ground_truth.red_herrings` | One entry; the leg weakness is the case's second misdirection. | FIXED: [0] interpretation reworded; [1] added at `patient.neurological_exam.motor` ("right hip flexion 4+/5", path verified). |
| E | minor | `metadata.difficulty_description`, `.difficulty_rationale` | Referred to post-ictal prolactin and prolonged video-EEG, which the case does not contain. | FIXED: rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

A 30-year-old woman with BRAF V600E metastatic melanoma on ipilimumab and nivolumab, dexamethasone and levetiracetam (missed evening doses because of irritability) has daily episodes of rising epigastric warmth, deja vu, staring, oral and right-hand automatisms, two witnessed on examination, and mild right leg weakness. The history now records the staging spine MRI (right L3-L4 foraminal metastasis, no cord compression) and the exam is a right L3-L4 radiculopathy with normal tone and flexor plantars. The required contrast MRI shows the left temporal metastasis grown from 0.5 to 1.6 cm with edema into the hippocampus and no leptomeningeal disease (the spine is no longer on the brain MRI); the required routine EEG shows left temporal slowing without discharges (no breach rhythm). Recommended: labs (levetiracetam 5.9 low, TSH 6.8 with normal free T4; prolactin removed), CSF (3 cells, protein 52, normal glucose ratio, cytology, flow and antibodies negative, after a hard MRI-first constraint) and the drug check. ECG and literature are optional; FDG-PET is waste; CT is no longer waste. Musts: a non-inducing ASM that fixes the adherence problem, oncology and radiation oncology for the brain and foraminal metastases, ICI and dexamethasone decisions, thyroid follow-up, driving; no inducers, no zonisamide, no high-dose steroids for a CSF-excluded ICI encephalitis.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys used that are not yet in the pack allow-list (plan CENTRAL 2): `[ASCO_irAE_2018]`, `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[NICE_NG217_2025]`.
- Synonyms (plan CENTRAL 6): the inherited "mesial temporal sclerosis epilepsy", the intractable G40.219 and the idiopathic G40.009/G40.019 do not fit a metastasis-related, non-drug-resistant focal epilepsy.

## Open questions for Andrea (judgment calls you could not settle)

None open. Decisions taken and their reasons:
- Laboratory values that duplicated RP01 and RP02 (levetiracetam 8.2, CRP 18.4, neutrophils 78%, albumin 3.4) were changed for this case, although the plan quotes "levetiracetam 8.2": the plan forbids copying numbers across cases, and the new values keep the same meaning (subtherapeutic, mild inflammation).
- Mild right L3-L4 pinprick loss and radicular thigh aching were added so the radiculopathy the plan asks for is clinically complete; no criterion depends on them.
- Pseudoprogression added to the differential as `low`: growth of a metastasis during checkpoint inhibitor therapy raises it, and leaving it out would let the case imply that MRI alone proves progression.
- FDG-PET report kept as the case fallback (consistent with the lesion) so a PET order, scored as waste, does not receive the library's normal PET.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff against master and the whole final case. Checked: spine findings gone from the brain MRI and placed in the HPI; exam now a right L3-L4 radiculopathy (hip flexion, dorsiflexion, patellar 1+, anterior thigh and medial shin pinprick, flexor plantars, normal tone) consistent with the differential and red herring; CSF (WBC 3, protein 52, ratio 0.62, all panels negative) matches the evidence; hard MRI -> CSF; PET criterion and follow-up removed, FDG_PET waste with the plan's rationale, fallback PET with its own SUVmax (9.6, unique in the dataset); ECG wording; TSH 6.8 with free T4 0.9 interpreted as primary thyroid dysfunction (consistent with a normal pituitary on MRI) and the ASCO thyroid must; ipilimumab 3 mg/kg with nivolumab 1 mg/kg every 3 weeks is the standard melanoma regimen; tiers and stop rule per plan; red-herring paths exist.
Found and fixed:
- Pseudoprogression `key_features` claimed the lesion grew "mostly before immunotherapy", which no data supports (only the 4-month-old and current measurements exist): reworded to tripling over 4 months with symptomatic edema in a non-irradiated metastasis, managed as progression with follow-up imaging.
- Drug output named trametinib among the drugs whose exposure inducers lower; trametinib is not CYP-metabolized. Now "CYP3A4-metabolized BRAF and MEK inhibitors (for example dabrafenib, encorafenib and cobimetinib)".
perfect_agent, case_io check and the case guards are clean.

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.
- `action-10-analyze-ecg.rationale`: engineering prefix or tier wording removed (was "Optional baseline before lacosamide (PR)...").
- `action-4-search-medical-literature.rationale`: engineering prefix or tier wording removed (was "Optional background; the diagnosis rests...").

## Close-out (24 Oct 2026)

Condition close-out (`plans/FEPI-TEMP-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G40 entries, re-applied with `--prune --conditions focal_epilepsy_temporal`): labels now focal epilepsy, temporal lobe epilepsy, TLE, epilepsy temporal lobe, mesial temporal lobe epilepsy, MTLE (added); removed mesial temporal sclerosis epilepsy (no hippocampal sclerosis on MRI); focal seizures; focal onset seizures; focal impaired awareness seizures (seizure-type labels, retired: their tokens occur in an acute symptomatic or functional-seizure answer). Codes: G40.2, G40.1, G40.9 plus G40.209, G40.109, G40.909 (not intractable); the idiopathic G40.009 and G40.019 removed and the intractable codes removed.
- Citation: `[ASCO_irAE_2018]` (4 places) -> `[ASCO_irAE_2021]`, the ASCO guideline update (Schneider 2021, J Clin Oncol 39:4073-4126) that supersedes it.
- Soft MRI -> drug check constraint: citation `[ILAE_MRI_2019]` -> `[NICE_NG217_2025]`, as in the other cases (ASM choice is what the constraint is about; auditor flag).
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FEPI-TEMP-` passes, now with the discriminator guard and the FEPI-TEMP banned strings.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-9-interpret-labs]`.alternatives: was [AED_levels] | [TSH] | [thyroid]; now [AED_levels, thyroid, BMP] | [AED_levels] | [TSH] | [thyroid].
- Decision: serve: new first alternative (old order kept as an alternative). The label asks for thyroid function and electrolytes (checkpoint-inhibitor thyroiditis); a must and the hypophysitis differential rely on TSH 6.8 with free T4 0.9.
- Scoring: none (recommended criterion: coverage unchanged, not in the cost reference).

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

Orders the benchmark library answered with a normal report that contradicts this case now get a case-specific report (term: gist, where stored):

- analyze_eeg ambulatory: This is an ABNORMAL 48-hour ambulatory EEG due to: 1. Five electroclinical seizures of left temporal onset (T3/T5), 30-70 seconds, without contralater (fallback_tool_outputs.eeg)
- analyze_eeg video: This is an ABNORMAL 72-hour video-EEG due to: 1. Nine habitual seizures of left temporal onset (T3/T5): rhythmic 5-6 Hz theta evolving to 2-3 Hz delta (followup request_video_eeg)
- obtain_tissue_diagnosis resection: Metastatic melanoma (fallback_tool_outputs.tissue_diagnosis)
- obtain_tissue_diagnosis stereotactic_biopsy: Metastatic melanoma (followup request_stereotactic_biopsy)
- obtain_tissue_diagnosis open_biopsy: Metastatic melanoma (followup request_open_biopsy)
- interpret_labs valproate_level: valproate not detected (fallback_tool_outputs.labs[valproate_level])
- order_body_imaging chest_abdomen_pelvis_CT: pulmonary, breast, hepatic and bone lesions (fallback_tool_outputs.body_imaging)
- order_body_imaging chest_xray: Multiple bilateral pulmonary nodules. No effusion or consolidation. Clinical correlation recommended. (followup request_chest_xray)
- order_body_imaging chest_CTA: 1. No pulmonary embolism. 2. Multiple bilateral pulmonary nodules. 3. Left breast nodule. Clinical correlation recommend (followup request_chest_cta)
- order_body_imaging pelvis_abdomen_MRI: Multiple rim-enhancing hepatic lesions and a left iliac marrow-replacing lesion, consistent with metastases. Clinical co (followup request_pelvis_abdomen_mri)
- order_body_imaging pelvis_abdomen_ultrasound: Several hypoechoic hepatic lesions with a target appearance. Clinical correlation recommended. (followup request_pelvis_abdomen_ultrasound)
- order_advanced_imaging MR_spectroscopy: Elevated choline with reduced NAA and lipid-lactate in the left temporal lesion, without choline elevation in the surrou (followup request_mr_spectroscopy)
- order_advanced_imaging perfusion_MRI: Hyperperfused left temporal lesion (maximum rCBV ratio 3.4) with low perfusion in the surrounding oedema. Clinical corre (followup request_perfusion_mri)
- order_advanced_imaging amino_acid_PET: Metabolically active left temporal lesion (maximum tumour-to-brain ratio 2.9). No other focus. Clinical correlation reco (followup request_amino_acid_pet)
- order_advanced_imaging whole_body_FDG_PET: Multiple hypermetabolic lesions in the lungs, left breast, liver and skeleton, consistent with metastatic disease. Clini (followup request_whole_body_fdg_pet)

Checks: `perfect_agent.py` passes; the criterion snapshot of the case is unchanged; `pytest agent-platform/tests -k FEPI-TEMP` (case guards included), `test_reports_do_not_fabricate.py` and `apply_diagnosis_synonyms.py --check` pass; no new report repeats a 60-character window of any criterion's expected evidence.
