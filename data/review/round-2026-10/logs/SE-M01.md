# SE-M01
Reviewer status: R1 none, R2 none (no notes; counted among the R2 approvals per the plan) | Approved before this round: yes (treated as approved per plans/SE.md)

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The notes file has no note for SE-M01. Changes below are plan classes and own findings, each a real error. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.labs.panels["Exclusion studies"]` | Template block (C1): ammonia, lactate, ABG and tox screen "Within reference range" with no number and an engineering clinical_significance. | FIXED: block deleted. Real values: venous lactate 2.6 mmol/L (H) in its own panel; toxicology panel (serum ethanol <10 mg/dL, urine drug screen negative). Ammonia and ABG dropped (not indicated: no liver disease or valproate, SpO2 97%). |
| B | minor | `initial_tool_outputs.labs.panels.BMP` | Criterion asks for CMP but the panel held only Na, glucose, creatinine, Ca, Mg (no K, bicarbonate, BUN, hepatic function). | FIXED: panel renamed CMP with K 4.1, Cl 103, HCO3 22, BUN 18, albumin 3.9, bilirubin 0.6, AST 24, ALT 21, ALP 82 (all normal); magnesium 1.9 in its own panel; interpretation and abnormal summary updated. |
| B | minor | `initial_tool_outputs.labs.panels.Cardiac[0]` | Troponin I 0.04 against a reference "<0.04" flagged normal. | FIXED: 0.02 ng/mL. |
| C | major | `ground_truth.action_criteria` action-12, `initial_tool_outputs.microbiology` | Meningitis-template blood cultures "before antimicrobials" in an afebrile (37.2 C) patient without infection source (C3). | FIXED: criterion, stored output and stop-rule entry deleted. |
| C | major | `followup_outputs` `request_continuous_eeg_monitoring` | Post-treatment EEG ("after lorazepam + LEV") reported the effect of management the agent cannot yet recommend, and its token "continuous" hijacked a correct `continuous_icu` order (C4). | FIXED: follow-up deleted; the cEEG order now receives the initial EEG (verified with `perfect_agent -v`). |
| C | major | `followup_outputs` `request_paraneoplastic_cancer_search` | Orphan advanced-imaging follow-up (no criterion) duplicating the body CT with a different nodule size (1.4 vs 1.1 cm) and a management recommendation (C5). | FIXED: deleted. |
| D | major | `initial_tool_outputs.drug_interactions`, `fallback_tool_outputs.drug_interactions` | Initial "general" block whose summary was the criterion's expected text (leak guard failure); fallback with engineering text (C9). | FIXED: both deleted; a T-DDI follow-up added (lorazepam + alcohol; levetiracetam no interaction, renal dosing; fosphenytoin + lisinopril hypotension; enzyme induction with CYP3A4/P-gp cytotoxics; valproate glucuronidation; lacosamide PR; metformin with contrast). Criterion optional (C9), case-specific text. |
| C | major | `ground_truth.action_criteria` action-9, literature follow-up | Literature required and in the stop rule; output gave a patient-directed treatment plan (ruling 5). | FIXED: optional, removed from stop rule, placed last; output rewritten per T-LIT (general cited voice, no patient values, no antibody named); trigger renamed `request_se_encephalitis_literature`. |
| D | major | `followup_outputs` `request_analyze_ecg` | ECG report "safe to load second-line AED", rate 0, rhythm "see impression" (C7). | FIXED: plain ECG read, sinus rhythm 86, PR 168, QRS 92, QTc 438, no ST-T change. Criterion action-11 kept optional with new label, rationale and evidence. |
| D | minor | `patient.history_present_illness` | "EEG was immediately performed" (timeline statement about a scored study) and "ruling out hypoglycemia" (conclusion). | FIXED: both removed; the home glucose value stays. |
| D | minor | `patient.neurological_exam.additional` | "subtle eye deviation suggests ongoing ictal activity" did the agent's reasoning. | FIXED: descriptive only (intermittent subtle eye deviation, right hand tremulousness). |
| B | minor | `patient.neurological_exam.motor` | "subtle left arm restlessness" contradicts a left temporal focus (C6). | FIXED: removed; right hand tremulousness kept. |
| B | minor | `ground_truth.red_herrings[1].correct_interpretation` | Said ictal eye deviation is toward the focus (it is away, ILAE lateralization in plan 1.2). | FIXED: explains why the gaze preference does not lateralize, and why fluctuation argues against a vascular deficit (C6). |
| C | major | `patient.history_present_illness`, `social_history.tobacco` | Labelled paraneoplastic limbic encephalitis with suspected SCLC, but the HPI had no subacute prodrome ("at his baseline", no illnesses) and a 10 pack-year habit quit 20 years ago, which makes SCLC and the Graus 2016 subacute-onset criterion poorly supported. | FIXED: 5-week prodrome of repeated questions, forgetting same-day conversations, irritability and 4 kg weight loss; tobacco 35 pack-years, quit 6 years ago. |
| C | major | `followup_outputs` MRI (`request_mri_brain_contrast`) | MRI described only lateral cortical DWI ("ictal pseudostroke", "ictal not ischemic", conclusions beyond the modality) with no mesial temporal FLAIR change, so it did not support limbic encephalitis. | FIXED: left hippocampal and amygdala FLAIR hyperintensity with swelling, gyriform diffusion restriction crossing MCA and PCA territories, no enhancement, SWI negative; impression with a worded imaging differential (peri-ictal change and/or limbic encephalitis; infarct unlikely). |
| B | minor | `initial_tool_outputs.eeg` | "2-3 Hz theta-delta" (2-3 Hz is delta), background `dominant_frequency` not a frequency, no evolution described although Salzburg was claimed. | FIXED: ACNS wording, 2-3 Hz rhythmic delta with embedded sharp waves evolving to 3-4 Hz and spreading to F7/C3, subtle right hand twitching and brief rightward eye deviation on video; background theta-delta; impression "electrographic status epilepticus, left temporal". |
| B | minor | `followup_outputs` CSF | Interpretation "(N/A PMN/N/A lymph)"; meningitis panel required but not reported; Hu and NMDAR reported under non-vocabulary keys. | FIXED: differential 90% lymphocytes; special tests keyed by the ordered terms (HSV_PCR, meningitis_panel, autoimmune_panel with CSF Hu 1:4 and surface antibodies negative, cytology); pattern-level interpretation. |
| D | minor | `initial_tool_outputs.body_imaging.impression` | Cross-modality reference ("the tumour most often associated with anti-Hu paraneoplastic disease"). | FIXED: imaging-only impression (suspicious for primary lung carcinoma), tissue diagnosis recommended. |
| B | minor | paraneoplastic panel follow-up | Hu titer stored with unit "titer"; panel lacked other onconeural antibodies; no templated hedged comment. | FIXED: titer confirmed by line blot; CV2/CRMP5, Ma2, amphiphysin, SOX1, GABA-B, CASPR2 negative; hedged templated comment per the style guide. Criterion gains an `autoimmune_encephalitis_panel` alternative. |
| C | major | `ground_truth.assessment.required_recommendations` | Lorazepam without maximum, acyclovir "until HSV PCR returns" (an early negative PCR does not exclude HSV), immunotherapy unspecified, oncology "consultation". | FIXED: T-MUST-BZD, T-MUST-2L (levetiracetam 60 mg/kg max 4500 mg; avoid enzyme-inducing fosphenytoin given expected cytotoxic treatment), T-MUST-cEEG, acyclovir per Tunkel 2008 with a stop condition, methylprednisolone with IVIG or PLEX (Graus 2016/2021), tissue diagnosis of the hilar mass. |
| E | minor | `ground_truth.assessment.prohibited_recommendations` | Wording ("ictal pseudostroke, not vascular-territory infarct") and em dashes. | FIXED: same three prohibitions, reworded. |
| C | major | `ground_truth.differential` | Stroke and HSV left "moderate" after MRI, EEG and CSF exclude them (C14). | FIXED: stroke low, HSV low (with the early-PCR caveat), surface-antibody AE low, metabolic very_low, PNES very_low; each `key_features` names the result. |
| C | minor | `ground_truth.key_clinical_evidence[2]`, `[4]` | "demands urgent CT chest / FDG-PET"; Salzburg paraphrase not the criteria. | FIXED: Graus 2021 tumour-screening pearl; Salzburg pearl per plan 1.2. |
| A | minor | every criterion and avoided action `citations` | Unbracketed duplicates ("Brophy_2012" beside "[Brophy_2012]") (C11). | FIXED: bracketed keys only. |
| E | minor | criteria `rationale` | Rationales copied from labels. | FIXED: T-LABS, T-CT, T-EEG and case-specific rationales and evidence for every criterion. |
| B | minor | `ground_truth.action_criteria`, `followup_outputs` order | Not the diagnostic order. | FIXED: labs, CT, EEG, ECG (optional), MRI, CSF, paraneoplastic panel, body CT, drug check (optional), literature (optional); follow-ups MRI, CSF, panel, ECG, drug check, literature. Ids unchanged. |
| B | minor | `ground_truth.sequence_constraints`, `stop_rule` | Labs-before-drug-check constraint not warranted (C13); `max_additional_actions` 0 (C12). | FIXED: only CT before CSF (hard) kept; stop rule = the 7 required criteria, allowance 1. |
| A | minor | `fallback_tool_outputs.specialized_test`, `metadata` | Specialized-test fallback with a non-vocabulary test type (C10); `fallback_tool_kinds` and `difficulty_rationale` stale. | FIXED: fallback deleted (library answers); kinds list updated; rationale states the 7 required actions. |

## Changes, in one paragraph a physician can read before re-reviewing
A 65-year-old man (now a 35 pack-year former smoker with a 5-week memory, irritability and weight-loss prodrome) has 45 minutes of confusion after a brief convulsion. The pathway is now labs (CMP, magnesium, lactate 2.6, negative toxicology; no template exclusion block, no ammonia or ABG), CT (unchanged subtle left temporal hypodensity), continuous video-EEG (evolving left temporal 2-3 Hz rhythmic delta with sharp waves and subtle right hand twitching: electrographic SE), an optional plain ECG, MRI (left hippocampal and amygdala FLAIR change with non-territorial gyriform diffusion restriction), CSF (lymphocytic pleocytosis, HSV and multiplex PCR negative, CSF anti-Hu positive), serum paraneoplastic panel (anti-Hu 1:1000) and body CT (right hilar mass with nodes). Blood cultures, the post-treatment EEG, the duplicate body-imaging follow-up and the leaking drug and literature blocks are gone; the drug check and literature are optional with neutral content. Musts follow the plan's canonical doses, with acyclovir per Tunkel 2008, first-line immunotherapy and tissue diagnosis of the hilar mass; the differential ranks stroke and HSV low after the work-up.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: the case cites `[ACNS_2021]`, `[Tunkel_2008]`, `[Graus_2016]`, `[Graus_2021]` (plan 1.1 "To add").
- Plan CENTRAL 3b: `icd_codes[0]` is G41.2 (complex partial SE); focal NCSE with impaired awareness fits G41.2, so no recode is needed for this case.

## Open questions for Andrea (judgment calls you could not settle)
None. Decided: the prodrome and smoking history were changed (not only the plan's items) because without them the labelled anti-Hu limbic encephalitis with suspected SCLC was not supported by the patient data (ruling 3: fix the data).

## Verification
`perfect_agent.py SE-M01 -v`: pass; labs, CT and the `continuous_icu` EEG receive the initial outputs, MRI, CSF and panel their follow-ups, body CT the initial body imaging. `test_case_guards -k SE-M01`: 2 passed. `case_io.py check SE-M01`: schema and synonym guard OK; no failure names SE-M01.

## Verification (adversarial verifier, 24 Oct 2026)
Checked: whole final case read against the log and `git diff`; every own-finding row confirmed in the file (blood cultures, post-treatment EEG, orphan cancer-search imaging, leaking drug/literature blocks and the specialized fallback are gone; ECG plain read; EEG left temporal with rightward ictal deviation; exam no longer has left arm restlessness; red herring explains the non-lateralizing gaze; stroke and HSV low; musts per plan 1.2; stop rule equals the 7 required criteria; CT before CSF hard only). No reviewer notes exist for the case. The prodrome and smoking changes are justified (labelled anti-Hu limbic encephalitis with suspected SCLC needs a subacute course and a smoking history) and consistent with the MRI, CSF, panel and chest CT.
Found and fixed:
- B minor `patient.neurological_exam.mental_status`: "GCS 13" with eyes open spontaneously (4), confused speech (4) and follows simple commands (6) sums to 14. FIXED: GCS 14.
- B minor `action-3-order-ct-scan.expected_evidence`: said "not a vascular-territory infarct", which the CT report itself says it cannot distinguish (and had an em dash). FIXED: "Subtle left temporal hypodensity, nonspecific on CT (early infarct versus focal edema); no hemorrhage, mass or midline shift".
- B minor pathway order: the tumour-search chest/abdomen/pelvis CT sat in `initial_tool_outputs.body_imaging` (shown to reviewers as the initial work-up, before the antibody result that prompts it; plan 3.2 limits initial outputs to labs, CT, EEG), and the optional ECG follow-up came after the panel while its criterion is placed before the MRI. FIXED: body CT moved unchanged to a follow-up `request_chest_abdomen_pelvis_ct` right after the paraneoplastic panel (`initial_tool_outputs.body_imaging` null; it is the only body-imaging payload, so any body-imaging order still receives it, probed for `chest_abdomen_pelvis_CT` and `chest_CT`); ECG follow-up moved first, matching the criterion order.
Not changed: the case-level ECG fallback (rate 85) differs from the ECG follow-up (rate 86) but is unreachable (the follow-up answers every ECG order, first or repeat).
Checks re-run after my edits: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, `test_case_guards -k` pass.

## Close-out (24 Oct 2026)
Decisions in `plans/SE-decisions.md`.
- synonyms: the G41 category no longer grants the type codes G41.0, G41.2 and G41.8 (a type code is granted only by the case's own code, so an answer coded with the wrong SE type no longer scores by code); `apply_diagnosis_synonyms.py --prune --conditions status_epilepticus` removed G41.0 and G41.8 from `ground_truth.diagnosis.icd_codes`. Labels unchanged.
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, SE case guards pass, `apply_diagnosis_synonyms.py --check --conditions status_epilepticus` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `continuous_icu`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
