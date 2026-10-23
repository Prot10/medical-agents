# BACT-MEN-P02
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 4b829a78-0714-4017-b03c-ec3d9b634b2a | FIXED | LP statements: deleted prohibitions "Do not perform the lumbar puncture before imaging ... involve neurosurgery first ..." and "Do NOT proceed to lumbar puncture: imaging shows mass effect ..."; replaced the IDSA 2004 template prohibition with one position (`ground_truth.assessment.prohibited_recommendations[0]`): image first because of the cranial nerve palsies, and communicating hydrocephalus without shift is not a reason to withhold the puncture (the teaching pearl, `key_clinical_evidence[0]`, kept). CSF moved out of the initial work-up (`initial_tool_outputs.csf` null, new `followup_outputs[2]` `request_lumbar_puncture`). Pyogenic boilerplate: deleted the "Do NOT discontinue dexamethasone ... pneumococcal" prohibition; "Do NOT treat with oral antibiotics alone" rewritten for TBM (`prohibited_recommendations[3]`, no antibiotics-only management of a lymphocytic Xpert-positive CSF); literature criterion `action-7-search-medical-literature` and `initial_tool_outputs.literature_search` deleted (plan C9). Allergy: `patient.clinical_history.allergies[0]` now states iodinated contrast (urticaria after contrast CT, no prior gadolinium); MRI report states gadolinium given without premedication, no reaction (`followup_outputs[3].output.additional_observations`); MRI criterion label says why gadolinium can be given. Ordering constraint: HARD CT before CSF kept, reason replaced with the reviewer's text (WHO 2025 Annex A.4 cranial nerve deficits; NICE NG240 1.4.7; neither formally covers TBM), CT criterion relabelled with the canonical C2 A text, citations `[WHO_Meningitis_2025]` (+ `[NICE_NG240]` on the constraint); SOFT blood cultures before CT added. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | initial_tool_outputs.ct | CT impression and recommended action deferred LP to "neurosurgical assessment of ICP" (management, and contradicts the ruling); first finding said "mild effacement of the basal cisterns" though nothing compresses them | FIXED: findings describe partially obscured, hyperattenuating cisterns without brainstem compression; impression is a numbered findings list ending "Contrast-enhanced MRI recommended"; CT moved to `followup_outputs[1]` `request_ct_head` (C3, C13) |
| D | major | initial_tool_outputs.mri.impression | Impression referred to "the differential below" and to CSF and microbiology (cross-modality) | FIXED: numbered findings plus a one-line imaging differential (granulomatous basilar meningitis: mycobacterial, fungal, neurosarcoidosis); MRI moved to `followup_outputs[3]` `request_mri_brain_contrast` (C13) |
| B | major | initial_tool_outputs.microbiology | `collected_before_antimicrobials: true` and "taken before the first antimicrobial dose" after 5 days of amoxicillin; no interval stated | FIXED: false, one collection line naming amoxicillin 875 mg twice daily for 5 days; "No growth at 48 hours in 2 of 2 sets; final report at 5 days"; moved to `followup_outputs[0]` `request_blood_cultures` (C6) |
| B | major | initial_tool_outputs.csf | CSF lacked the multiplex panel, ACE and cytology the criterion orders (cytology was filed as a blood "Exclusion studies" panel); bacterial culture "No growth at 48 hours" in a same-day report; lactate reference <2.8; ADA reference text interpretive; ratio string without the paired values | FIXED: added multiplex panel (no target detected, targets listed), CSF ACE (normal), cytology (negative), mycobacterial culture "Pending (final at up to 6 weeks)"; bacterial culture "Pending"; canonical ratio, RBC and lactate strings; ADA "(reference <10 U/L)"; interpretation states values and stain/PCR results only; `Xpert_MTB_RIF_Ultra` key (C1, C7) |
| B | major | followup_outputs (request_afb_culture, request_repeat_lp, request_ophtho) | AFB culture at 21 days and full susceptibilities under `interpret_labs`; post-treatment repeat LP "improved from 220"; ophthalmology consultation filed as labs (choroidal tubercles) | FIXED: all three deleted; mycobacterial culture is pending in the index CSF (C1, C8) |
| D | minor | initial_tool_outputs.labs | QuantiFERON-TB Gold Plus result in the first panel: not ordered by action-1 and not available within the ED encounter (24 to 72 h turnaround) | FIXED: removed |
| B | minor | initial_tool_outputs.labs | action-1 orders `coagulation` but the panel had none; cytology "Exclusion studies" panel; summary lines carried interpretation ("SIADH", "lower than expected for bacterial meningitis") | FIXED: PT, INR, aPTT added (normal); exclusion panel removed; summary and interpretation list values and flags only |
| C | major | ground_truth.differential | Acute bacterial meningitis left "high", cryptococcal and neurosarcoidosis "moderate" after a lymphocytic, Xpert-positive CSF with negative CrAg, India ink, cytology and normal CSF ACE | FIXED: bacterial (including partially treated) low, cryptococcal low, neurosarcoidosis low, viral and carcinomatous very low, each with the excluding result (C10) |
| A | minor | ground_truth.differential[2].icd_code | Neurosarcoidosis coded D86.85 (sarcoid myocarditis) | FIXED: D86.81 (sarcoid meningitis) |
| C | major | ground_truth.red_herrings | Only red herring was the pyogenic "negative Gram stain" template, pointing at a TB case's CSF and arguing the wrong way | FIXED: replaced with the three distractors the case is built on (5 days of amoxicillin as partially treated bacterial meningitis; childhood BCG and no known contact; no pulmonary symptoms) |
| C | major | ground_truth.assessment.required_recommendations | Musts: "RIPE ... within hours" without duration; dexamethasone "(or per latest guideline)"; CSF tests "before steroid initiation alters cellularity" (unsupported); HIV testing already in the baseline panel; no must for the levothyroxine interaction the DDI step exists for | FIXED: 2HRZE then HR to 12 months without waiting for culture (WHO Module 4); dexamethasone 0.4 mg/kg/day tapered over 6 to 8 weeks; CSF AFB, Xpert Ultra, mycobacterial culture with DST, ADA without delaying treatment; neurosurgery for hydrocephalus; chest imaging and sputum; levothyroxine recheck; public health notification and household contact screening |
| C | minor | ground_truth.action_criteria[action-6] | DDI recommended with template expected evidence; the case has a concrete interaction (rifampicin induces levothyroxine metabolism) | FIXED: required (plan 4.0), label and expected evidence name the interaction; new `followup_outputs[4]` `check_antituberculous_drug_interactions` with the real regimen, levothyroxine, dexamethasone and amoxicillin; added to the stop rule |
| B | minor | patient.clinical_history.medications | Amoxicillin 875 mg twice daily for 5 days in the HPI but not in the medication list | FIXED: added |
| C | minor | ground_truth.action_criteria[action-3, action-4] | CSF label omitted the bacterial, fungal and malignant studies the criterion orders and claimed falling yield; MRI label was the generic "only for this case's suspected complication" template | FIXED: CSF label lists what is sent; MRI label and expected evidence are case-specific |
| D | minor | ground_truth.key_clinical_evidence[0], [6] | Pearl ended with a cryptococcal clause (P03 carry-over); last line "when the pathway requires treatment first" | FIXED: cryptococcal clause removed; last line states that empirical treatment does not wait for imaging or LP and ATT starts without waiting for culture |
| A | minor | citations | `[IDSA_2004]`, "IDSA 2004 §V/§VII" and free-text WHO duplicates | FIXED: `[WHO_Meningitis_2025]` on criteria and avoided actions, `[WHO_TB_Module4]` on CSF and DDI |
| E | minor | metadata.difficulty_rationale | Stated that imaging "shows mass effect / hydrocephalus that contraindicates LP" | FIXED: rewritten to the ruled position |

## Changes, in one paragraph a physician can read before re-reviewing

Only the blood panel is given on the first labs order now; blood cultures, the non-contrast CT, the
index LP, the contrast MRI and the drug check are pathway steps in that order. The CT stays required
before the LP because of the bilateral sixth and left seventh nerve palsies (WHO 2025 Annex A.4),
with the reviewer's constraint text, and it reports mild communicating hydrocephalus without mass,
shift or brainstem compression; the case now takes one position: image first, then puncture, since
communicating hydrocephalus is not a contraindication. The CSF report holds everything the criterion
orders (multiplex panel negative, CrAg and India ink negative, cytology negative, CSF ACE normal, rare
AFB, Xpert Ultra positive without rifampicin resistance, ADA 18, cultures pending); the AFB culture at
21 days, the post-treatment repeat LP and the ophthalmology "labs" are gone. Blood cultures record the
5 days of amoxicillin. The musts are tuberculous-meningitis management (2HRZE/10HR, dexamethasone taper
6 to 8 weeks, neurosurgery, chest imaging and sputum, levothyroxine adjustment for rifampicin, public
health and household screening); the pyogenic prohibitions and the literature step are removed. The
contrast allergy is iodinated, and the MRI states gadolinium was given without reaction. The
differential is updated to the post-CSF view and the red herrings are the amoxicillin course, BCG,
and the absence of pulmonary symptoms.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `analyze_csf` vocabulary has no mycobacterial term (AFB smear, Xpert MTB/RIF Ultra, mycobacterial culture, ADA): the CSF criterion orders `meningitis_panel`, `ACE_CSF`, `cytology` and the TB studies live in the same report (plan section 5 item 4: `mycobacterial_panel`, `ADA`).
- Citation keys `[WHO_TB_Module4]` (WHO consolidated guidelines on tuberculosis, Module 4: treatment and care; edition to confirm) and `[NICE_NG240]` for the criteria pack allow-list (plan section 5 item 1).
- Chest imaging is a must, not a criterion: `order_body_imaging {study: chest_CT}` exists, but the case has no chest study and the plan keeps it a must. If Andrea wants it scored, a chest CT report needs authoring.

## Open questions for Andrea (judgment calls you could not settle)

- Plan Q1: the case is tuberculous meningitis (A17.0) inside `bacterial_meningitis` with a P prefix; kept as a non-pyogenic mimic.
- The QuantiFERON result was removed from the first panel as unordered and not available within the encounter; if it was meant as a deliberate clue, it should return as an orderable later result.

## Verification

Adversarial verifier, 23 October 2026. Checked: note 4b829a78 against the final file (one LP position in `prohibited_recommendations[0]` and `key_clinical_evidence[0]`; no "mass effect" bullet; Gram stain dexamethasone prohibition gone; oral-antibiotics bullet rewritten for TBM; literature criterion and output gone; allergy is iodinated contrast and the MRI states gadolinium given without reaction; HARD CT before CSF carries the reviewer's reason, SOFT blood cultures before CT present); index CSF served to action-3 by `request_lumbar_puncture` (`-v`); glucose ratio 22/98 = 0.22 with the panel glucose 98; anion gap 128 - 94 - 24 = 10; MRC grade II matches GCS 13 with cranial nerve palsies; red-herring paths resolve; constraint and stop-rule ids exist; musts against WHO TB Module 4 (2HRZE/10HR, dexamethasone taper 6 to 8 weeks); differential reflects the CSF; no new em dashes (the remaining ones are original exam and MRI text).

Found and changed:
- `action_criteria[action-4-analyze-brain-mri].citations` still carried the free-text duplicate "WHO meningitis guideline 2025" (plan 1.1, 3.1): removed, `[WHO_Meningitis_2025]` kept.
- `key_clinical_evidence[2]` cited "tentorial enhancement", which the MRI does not report (basal cisterns, interpeduncular fossa, sylvian fissures, prepontine): now "Basal cistern enhancement plus ring-enhancing basal-ganglia lesions ...".
- `metadata.case_body_concerns` [0], [1], [3], [4], [5] described defects this round removed (CT "basal-cistern effacement", DDI and literature "reclassified to recommended", analyze_csf as harmful, the pneumococcal prohibition, a `request_chest_ct` follow-up that no longer exists) and were now false: deleted, as other BACT-MEN workers did; [2] (P prefix for a TBM case, plan Q1) kept.

Left as is (judgment, for Andrea): no must names empirical antibacterial cover (ceftriaxone) before the CSF result, although the soft constraint, CT label and `prohibited_recommendations[1]` assume empirical treatment precedes imaging; at assessment time the Xpert-positive lymphocytic CSF makes TBM therapy the decisive must. The imaging differential in the MRI impression (mycobacterial, fungal, neurosarcoidosis) is allowed by TOOL_REPORT_STYLE_GUIDE (`differential_by_imaging`), so it stays despite plan C13's "no differential". `metadata.clinical_pearls[3]` (choroidal tubercles) refers to the deleted ophthalmology step; metadata only, not changed.

After the edits: `perfect_agent.py BACT-MEN-P02 -v` passes (action-3 <- `request_lumbar_puncture`); `case_io.py check` clean for the case.

## Condition audit (23 October 2026)
- Changed `ground_truth.action_criteria[action-2-order-microbiology].alternatives[0].required_arguments`: removed `before_antimicrobials: true` (specimen and tests kept). Reason: the blood culture report sets `collected_before_antimicrobials: false` because an antimicrobial was taken in the 7 days before collection, so `true` is not the truthful value of the parameter ("whether the specimen is being taken before the first antimicrobial dose") and an agent that orders the cultures truthfully would miss a required criterion. Condition-wide rule settled at the audit: the argument is required only where the report flag is true (16 cases) and absent where it is false (14 cases: M01, M02, M03, M05, P02, P04, RM01, RM03, RP01, RP02, RP03, RP05, RS04, S03). Draw-before-treatment timing stays in the musts and in the SOFT blood-cultures-before-CT constraint where one exists. `perfect_agent.py` and `case_io.py check` clean after the edit.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (4 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex

Re-run: `perfect_agent.py` ok; `case_io.py check` clean for the case; BACT-MEN case guards pass; synonym `--check` clean.
