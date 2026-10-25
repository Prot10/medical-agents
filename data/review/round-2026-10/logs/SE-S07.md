# SE-S07
Reviewer status: R1 not reviewed, R2 approved | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| aeb5068c-eaea-42f6-af39-49f7b7c11740 | FIXED | Deleted the orphan `analyze_csf` follow-up (`request_lp_autoimmune`, which also had "slightly xanthochromic" fluid with 2 RBC and a GFAP "tumor marker"). Added avoided action `avoid-contraindicated-1-analyze-csf` (`analyze_csf`, severity `contraindicated`, mass with 4 mm midline shift, [Tunkel_2008]). The two duplicate LP prohibitions are merged into one. The MRI-before-CSF hard constraint was already absent (ALREADY-FIXED in part); the only remaining constraint (drug check after labs, with a beta-hCG reason) is deleted per plan C13. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| B | major | `patient.chief_complaint`, `history_present_illness` | The seizure was said to start in the right arm, but the tumor, the EEG onset (F4) and the leftward ictal gaze are right frontal, and the exam already records left arm clonic predominance and a left Todd paresis (plan C6). | FIXED: the CC and HPI now say left arm. |
| B/C | blocker | `initial_tool_outputs.eeg`, EEG follow-up `request_continuous_eeg_monitoring` | The initial EEG reported continuous generalized 3 Hz spike-wave "secondary generalisation" for the whole record, although the exam has her opening her eyes to voice after the convulsion. The follow-up reported a "post-treatment" 12-hour record, which shows the effect of treatment (ruling 4). Its trigger also shared the token "continuous" with `continuous_icu` and took over the cEEG order (plan C4). The EEG criterion had no `eeg_type`. | FIXED: follow-up deleted. The initial EEG is rewritten in ACNS terms: four right frontal (F4) seizures in the first hour, each evolving to generalized 3 Hz spike-and-wave, with no return to the interictal background; left arm and face clonic correlate on video; right frontal LPDs at 1 Hz and polymorphic delta between seizures. Electrographic SE is named (Kind 2). T-EEG criterion with `continuous_icu` or `video`. The mental status line now says she opens her eyes to voice but does not speak or follow commands, which is consistent with no return to baseline. |
| B | major | `initial_tool_outputs.ct` | The CT criterion is a non-contrast CT, but the report had `contrast_used: true` and "ring enhancement". The findings said "possibly enlarged" while the impression said "unchanged or minimally increased". A finding cited the steroid taper (cross-modality). There were no sizes. | FIXED: non-contrast report. Heterogeneous right frontal mass 4.3 x 3.8 cm with central low density, larger than on the MRI of 6 weeks earlier. Extensive edema. 4 mm leftward shift with patent cisterns. No hemorrhage. MRI with contrast and perfusion is recommended. a3 expected text updated. |
| B/D | minor | MRI follow-up | Interpretive words sat in the signal fields ("true progression", "high grade tumor"). Central necrosis was described as restricting diffusion. There were no sizes. The criterion's expected "no new acute infarct" was not in the report. | FIXED: T1 post-contrast rim 4.4 x 3.9 cm (from 3.8 x 3.4 cm). Restricted diffusion in the solid rim. rCBV 2.6 times contralateral white matter. Expanded FLAIR. SWI with no blood. The impression favors progression over treatment-related change and states no hemorrhage and no acute infarct. |
| A/C | major | `initial_tool_outputs.labs` | There was a template "Exclusion studies" block (magnesium, ABG, beta-hCG "Within reference range", plan C1). beta-hCG was taken in a 68-year-old woman (plan C2). The CMP had only sodium, glucose and creatinine. The abnormal summary carried causal claims ("dexamethasone effect", "bevacizumab anemia"). CK 1480 within an hour of an 18-minute seizure is implausibly early. | FIXED: block deleted. beta-hCG removed from the panel, the label and the arguments. Full CMP plus magnesium 1.9. ABG pH 7.28, pCO2 41, pO2 68 with lactate 5.8 and CO2 19, which fits the convulsion. CK 386. The INR panel is dropped (not on anticoagulants, not ordered). Plain factual summary and interpretation. T-LABS criterion: CBC, CMP, magnesium, AED_levels. |
| C | major | `followup_outputs[]` `request_aed_optimization` | A "post-IV 3000 mg loading" levetiracetam level and a post-insulin glucose reported the effect of treatment (ruling 4, plan C4). | FIXED: deleted. |
| C/D | major | DDI follow-up, a5 | The output was about citalopram and seizure threshold, with management prose ("Continue citalopram 20 mg"). The expected text gave the wrong rationale for avoiding enzyme inducers: she is not on temozolomide (plan C9). | FIXED: T-DDI content. Phenytoin, fosphenytoin and carbamazepine induce CYP3A4 and lower dexamethasone exposure. Valproate adds a platelet effect to the bleeding risk of bevacizumab. Levetiracetam and lacosamide have no relevant interaction. Citalopram QT is listed. Tier `recommended`. Trigger renamed. |
| C/D | major | literature follow-up, a6 | Literature was required, and its output was a palliative and prognosis essay ("median survival 15 months", "levetiracetam preferred"). | FIXED: optional and last, removed from the stop rule. T-LIT content on tiered SE treatment [Glauser_2016, ESETT_2019, Brophy_2012]. |
| C | major | `assessment` | The musts had no doses for the second-line drug and no steroid dose. There was no cEEG must. One prohibition gave the TMZ rationale, and the LP prohibition appeared twice. | FIXED: T-MUST-BZD (no benzodiazepine documented before arrival); T-MUST-2L (levetiracetam 60 mg/kg, max 4500 mg; avoid fosphenytoin because of the dexamethasone interaction); dexamethasone re-escalation with glucose monitoring; T-MUST-cEEG; early goals of care with neuro-oncology and palliative care. Prohibitions: no LP, no enzyme inducers (dexamethasone reason), no anaesthetic escalation without a goals-of-care discussion. |
| C | major | `ground_truth.differential` | "Tumor progression with new hemorrhage" stayed high although CT and MRI show no hemorrhage. Subtherapeutic level "alone" was high. Infection pointed to CSF, which is contraindicated (ruling 7). | FIXED: intratumoral hemorrhage low (no blood on CT or SWI). Level alone low (MRI shows progression and edema). Citalopram, stroke and CNS infection low, each with the result that excludes it. |
| C | minor | `red_herrings` | The glucose red herring cited "no ketones or hyperosmolarity", which the case does not report. 37.8 C with WBC 14.2 was not explained. | FIXED: the glucose explanation now uses the reported values (calculated osmolality about 296, lactic acidosis). T-HYPERTHERMIA red herring added (37.8 C, WBC on dexamethasone). |
| B | minor | `patient.clinical_history.medications` | The list had dexamethasone 4 mg twice daily (8 mg/day), but the HPI says it was tapered from 8 to 4 mg/day. | FIXED: 4 mg once daily, tapered from 8 mg/day. |
| E | minor | `past_medical_history`, HPI | "Glioblastoma multiforme" is not a WHO CNS5 name. Nausea was attributed to bevacizumab, which is rarely emetogenic, 5 days after the infusion. | FIXED: "Glioblastoma, IDH-wildtype" (68 years, by definition in CNS5). The HPI now just says "because of nausea". |
| A | minor | `fallback_tool_outputs` | Advanced imaging "CT angiography" and specialized test "neuropsychological_testing" are not vocabulary (C10). The fallback ECG showed rate 80 against HR 112. | FIXED: both set to null (the library answers). ECG fallback is sinus tachycardia 108. `metadata.fallback_tool_kinds` updated. |
| E | minor | `avoid-waste-5-order-specialized-test` | It carried the DaTscan rationale under polysomnography. | FIXED: T-PSG text. |
| A | minor | `stop_rule`, `metadata` | `max_additional_actions` was 0, and the stop rule listed the literature and drug check. The rationale counts were stale. | FIXED: required labs, CT, EEG and MRI; max 1; metadata updated. |

## Changes, in one paragraph a physician can read before re-reviewing
SE-S07 keeps its story: focal-to-bilateral convulsive SE in a 68-year-old woman with right frontal glioblastoma progressing on bevacizumab, after a missed levetiracetam dose and a dexamethasone taper. The seizure now starts in the left arm, which matches the right frontal tumor, the F4 onset, the leftward gaze and the left Todd paresis. The CT is a true non-contrast report: enlarging mass, edema, 4 mm shift, no blood. The cEEG shows recurrent right frontal seizures evolving to generalized spike-and-wave without return to baseline, with right frontal LPDs between them. The post-treatment EEG and post-loading levels are gone. The MRI shows progression with more edema and no hemorrhage or infarct. The labs are a full CMP with magnesium, a levetiracetam level of 8, and the lactic acidosis expected after a convulsion. The template exclusion block and beta-hCG are gone. The orphan LP step is gone, and LP is now an avoided action (contraindicated). The drug check (recommended) gives the real interaction, which is that enzyme inducers lower dexamethasone exposure, not temozolomide, plus the valproate-bevacizumab bleeding caution. Literature is optional. The musts are a benzodiazepine, levetiracetam 60 mg/kg, dexamethasone re-escalation with glucose control, cEEG, and early goals of care. The differential is ranked against the results.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: `[ACNS_2021]` and `[Tunkel_2008]` are cited here and need the criteria-pack allow-list.
- Plan CENTRAL 3b: this is focal-to-bilateral convulsive SE, but `icd_codes[0]` is G41.2 and the synonyms include NCSE labels. Recode to G41.0 and prune the NCSE synonyms (central).

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the full diff and the whole final case (approved case, large rewrite).
- Note aeb5068c: confirmed. No `analyze_csf` follow-up remains, `avoid-contraindicated-1-analyze-csf` is present with severity `contraindicated`, there is one LP prohibition, and `sequence_constraints` is empty, so nothing presupposes an LP.
- Cross-field checks: the left arm onset is now the same in the CC, HPI, exam (left clonic predominance, left Todd paresis, leftward ictal gaze away from the right frontal focus), the EEG video correlate (left arm and face) and the F4 onset. Dexamethasone is 4 mg/day in the medication list and the HPI. CT and MRI agree on a 4 mm leftward shift and no blood. No beta-hCG, exclusion block, blood cultures, post-treatment outputs or DaTscan text remains. The musts and prohibitions agree: no enzyme inducers, levetiracetam load. The differential matches the results. Perfect agent, `case_io.py check` and the case guards are clean.
- Found and fixed: the MRI criterion cited [Glauser_2016], a treatment guideline that says nothing about imaging, and called the SE "refractory", which the case does not state. The rationale is now "Structural SE in a known glioma: ... [Brophy_2012]" and the citations are `[Brophy_2012]`. The stale `metadata.revision_reason` described the deleted exclusion block; it now points to this log.
- Left as is: the drug-check rationale cites [ESETT_2019] for the second-line choice. It was there before and is defensible.

## Close-out (24 Oct 2026)
Decisions in `plans/SE-decisions.md`.
- `icd_codes[0]` G41.2 (complex partial SE) -> G41.0: the case is focal-onset SE evolving to bilateral convulsions (ILAE 2015 classifies it with convulsive SE), so the NCSE code and its labels named the wrong type (SE summary CENTRAL 3b). After `--prune --conditions status_epilepticus` the case accepts the generic labels plus "generalized convulsive status epilepticus", "convulsive status epilepticus", "GCSE", "tonic clonic status epilepticus" and codes G41.0, G41.9, G40.901, G40.911; the NCSE labels and G41.2/G41.8 are gone. `accepted[0]` unchanged.
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, SE case guards pass, `apply_diagnosis_synonyms.py --check --conditions status_epilepticus` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `continuous_icu`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## EEG and labs after routing (25 Oct 2026)

Commit 317e46db routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG) and serves an `interpret_labs` order only the stored panels it names. Decisions for the condition in `plans/SE-routing-decisions.md`.

- EEG: a routine order received the library's normal routine EEG, which contradicts the case. Added `fallback_tool_outputs.eeg` with `eeg_type` `routine` (the stored continuous_icu recording cut to a 30-minute portable recording without video, technologist notes for the clinical events, activation not performed): two right frontal-onset seizures evolving to generalized 3 Hz spike-and-wave in 30 minutes without return to background, right frontal LPDs and delta. No criterion, tiers and the reward-relevant policy unchanged; the clinically correct test stays the continuous EEG of `action-1-analyze-eeg`. A `continuous_icu` or `video` order still receives `initial_tool_outputs.eeg`.
- Labs `action-2-interpret-labs`: unserved result cited in `expected_evidence`: lactate 5.8, pH 7.28 (Blood Gas and Muscle Enzymes). TRIM: post-convulsive; served bicarbonate 19 kept in its place. Scoring change: no.
  - action-2-interpret-labs expected_evidence: 'Levetiracetam 8 mcg/mL, below range; glucose 248 on dexamethasone; lactate 5.8 with pH 7.28 after the convulsion; WBC 14.2; hemoglobin 11.4; sodium 138, calcium 9.1, magnesium 1.9 and creatinine 1.0 normal' -> 'Levetiracetam 8 mcg/mL, below range; glucose 248 on dexamethasone; bicarbonate 19 after the convulsion; WBC 14.2; hemoglobin 11.4; sodium 138, calcium 9.1, magnesium 1.9 and creatinine 1.0 normal'
- Checks: `perfect_agent.py -v` pass; `case_io.py check` schema and synonym guard OK, no test failure names the case; probe: routine (omitted and explicit) order -> the new case fallback, `continuous_icu` and `video` -> the stored index recording; every number in each lab criterion's evidence is in what its order returns.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although this case contradicts it (diagnosis, history, medications or a stored finding) now get a case-specific report; every other off-pathway order still gets the library normal. No tier, criterion, diagnosis or existing output changed.

- `analyze_eeg eeg_type=ambulatory` -> `followup_outputs[order_ambulatory]`: ambulatory EEG mirroring the stored continuous EEG (no video).
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[order_performance_status]`: performance status KPS 20, ECOG 4 during the admission.
- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `followup_outputs[order_gait_and_balance_timed]`: timed gait not testable, as on the examination.
- `perform_clinical_assessment assessment_type=cognitive_screen` -> `followup_outputs[order_cognitive_screen]`: baseline cognitive screen not testable in the documented mental state.
- `order_specialized_test test_type=neuropsych_battery` -> `followup_outputs[order_neuropsych_battery]`: neuropsychological battery not testable in the documented mental state.
- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: speech and language evaluation not testable in the documented mental state.
- `labs:lithium_level` -> fallback labs panel `Lithium`: lithium not detected (not prescribed).
- `labs:valproate_level` -> fallback labs panel `Valproate`: valproate not detected (not prescribed).
- `order_advanced_imaging modality=FDG_PET` -> `followup_outputs[order_fdg_pet]`: brain FDG-PET abnormal where the stored MRI shows the lesion.
- `order_advanced_imaging modality=perfusion_MRI` -> `followup_outputs[order_perfusion_mri]`: perfusion MRI as the stored lesion.
- `order_advanced_imaging modality=MR_spectroscopy` -> `followup_outputs[order_mr_spectroscopy]`: MR spectroscopy of the stored lesion.
- `order_advanced_imaging modality=amino_acid_PET` -> `followup_outputs[order_amino_acid_pet]`: amino acid PET: avid rim of the progressing glioblastoma.
- `obtain_tissue_diagnosis procedure=stereotactic_biopsy` -> `followup_outputs[order_stereotactic_biopsy]`: stereotactic biopsy pathology of the stored lesion.
- `obtain_tissue_diagnosis procedure=open_biopsy` -> `followup_outputs[order_open_biopsy]`: open biopsy pathology of the stored lesion.
- `obtain_tissue_diagnosis procedure=resection` -> `followup_outputs[order_resection]`: resection pathology of the stored lesion.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k SE` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
