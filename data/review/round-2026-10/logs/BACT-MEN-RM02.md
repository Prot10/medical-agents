# BACT-MEN-RM02
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 6e436225-b347-4cca-89c1-627ff45ae9e8 | FIXED | SCOPE: no NICE citation is used for the disease decisions; every criterion, avoided action and constraint cites `[WHO_Meningitis_2025]`; the HARD constraint reason states "NICE NG240 does not cover this patient (immunosuppressive therapy places him outside its scope)". The only NICE mention left is the canonical hearing must (see Open questions). CRITICAL ACTIONS: the template "vancomycin 15-20 mg/kg + ceftriaxone 2 g" must replaced by the canonical ceftriaxone must with vancomycin conditional on local pneumococcal resistance (`assessment.required_recommendations[0]`), and a Listeria must, ampicillin 2 g IV every 4 hours for age over 60, diabetes and immunosuppressive therapy (`[1]`); the targeted must (`[7]`) states that the ceftriaxone MIC of 0.5 mg/L or less needs no vancomycin. The self-contradiction is gone: the literature step that named ampicillin is deleted (ruling 5), and the drug-check label, output and pearl now give the same regimen as the musts. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `action_criteria` (`action-5-order-ct-scan`), `sequence_constraints[0]`, `assessment.*`, `key_clinical_evidence` | CT before LP justified on IDSA 2004 ("altered mental status, immunocompromise, ... age >60"). | FIXED (plan C2 A): label, rationale, must, prohibition, pearl and HARD reason name the WHO 2025 Annex A.4 limb: a severe immunocompromised state (IV cyclophosphamide 10 days ago with prednisolone restarted at 60 mg). SOFT blood-cultures-before-CT constraint added. |
| B | major | `followup_outputs` | Post-treatment repeat LP was step 1 and would answer any LP call; index CSF and contrast MRI were given upfront. | FIXED (C1, C13): repeat LP deleted; index CSF is `request_lumbar_puncture` after the CT; MRI is `request_mri_brain_contrast` after the LP. `-v` confirms action-3 receives the index LP and action-4 the MRI. |
| B | major | `followup_outputs` (`request_pcr_panel`, `request_audiometry`, `request_cryptococcal_antigen`, literature) | PCR duplicated under `interpret_labs` (with an M. tuberculosis target the panel does not have); audiometry as `baep` before treatment; CSF CrAg filed under `interpret_labs` while the CSF report said "Pending"; literature quoting IDSA 2004 "over 50". | FIXED (C8, C9): all four deleted; CSF CrAg reported in the index CSF as "Negative (lateral flow assay)" (orderable as `analyze_csf` `cryptococcal_antigen`); the serum CrAg is not orderable (plan CENTRAL 4) and adds nothing once the CSF CrAg is negative; hearing must added. |
| B | major | `followup_outputs[0].output.susceptibility` (blood cultures) | Penicillin MIC 0.12 called "Intermediate for meningitis"; anaerobic "No growth at 5 days" at the work-up decision. | FIXED (C6): "MIC 0.12 mg/L, resistant (CLSI meningitis breakpoint: resistant 0.12 or more)", ceftriaxone "MIC 0.5 mg/L or less, susceptible"; anaerobic bottles "No growth at 48 hours; final report at 5 days"; Gram stain field filled; impression "isolated from 2 of 2 sets at 22 and 24 hours". `collected_before_antimicrobials` stays true (no antibiotics before sampling). |
| B | minor | CSF report | Ratio reference "normal >0.6"; lactate gloss "strongly supporting bacterial etiology"; interpretation concluding "consistent with bacterial infection". | FIXED (C7): "0.04 (CSF 11 mg/dL / blood 287 mg/dL; reference 0.5 to 0.8, 0.4 or less abnormally low)" with the lab panel's glucose; RBC "within normal limits"; lactate "(local laboratory reference <3.5 mmol/L)"; pattern-only interpretation. |
| B | major | `followup_outputs[3].output.impression` (MRI) | Impression omitted the scan's main finding, diffuse leptomeningeal enhancement; FLAIR text interpreted ("suggesting proteinaceous or inflammatory material"). | FIXED: enhancement is impression item 1; FLAIR describes the signal only. |
| C | minor | `action_criteria` (`action-4-analyze-brain-mri`) | Generic MRI label ("this case's suspected complication") and expected evidence. | FIXED: case-specific label (complications in an immunosuppressed host, comparison with the imaging behind the presumed vasculitis; after the LP) and expected evidence; tier stays recommended (plan 4). |
| B | minor | `followup_outputs[1].output` (CT) | "No contraindication to lumbar puncture" twice; impression speculating on the cause of the hydrocephalus. | FIXED (C3): findings-only impression, patent cisterns and no midline shift stated. |
| C | major | `assessment.required_recommendations` | No plan for his prednisolone and cyclophosphamide, or for glucose (287 mg/dL) on dexamethasone with metformin and glipizide; dexamethasone must without a stop rule; generic de-escalation must; template dexamethasone prohibition. | FIXED: must to hold prednisolone during dexamethasone and resume without abrupt withdrawal, and to withhold further cyclophosphamide until the infection is controlled and the vasculitis diagnosis reassessed; must to replace oral agents with insulin; canonical dexamethasone must with "Continue for 4 days: Streptococcus pneumoniae is identified" (C5); targeted must (ceftriaxone continued, ampicillin and any vancomycin stopped; no duration, plan 1.2); template prohibition deleted. |
| C | minor | `assessment.prohibited_recommendations`, `red_herrings[4]` | The anchoring trap the metadata describes (presumed CNS vasculitis) was neither declared nor tested. | FIXED: prohibition against attributing the illness to a vasculitis flare or escalating immunosuppression; red-herring block added. |
| C | minor | `ground_truth.differential` | Boilerplate (viral meningitis and HSV moderate, SAH) after a bacterial CSF with a named organism; vasculitis flare, stroke, TB (prior low-glucose lymphocytic meningitis) and leptomeningeal malignancy (nodular enhancement), all raised by the case, missing. | FIXED (C10): vasculitis flare, acute ischaemic stroke, Listeria, TB, cryptococcal meningitis and leptomeningeal malignancy, all low, each with what raises and what excludes it. |
| B | minor | `ground_truth.red_herrings[0..3]` | Pointed at initial outputs; sinus thickening "on MRI" pointing at `initial_tool_outputs.mri`; Gram stain sensitivity "60-90%" and antigen testing as confirmation; hyponatraemia to be treated "with fluid restriction" (not routine in bacterial meningitis; sodium corrects to about 132 for glucose 287); stroke herring described a focal weakness the exam does not show. | FIXED (C11): paths to `followup_outputs[2]` Gram stain, labs BMP and the CT sinus observation; interpretations rewritten (WHO 85% sensitivity; corrected sodium and volume assessment; worsened dysarthria and no acute infarct on MRI). |
| B | minor | `patient.neurological_exam.mental_status`, `.motor` | GCS 10 (E2 V3 M5) against "arousable to loud verbal stimulation" (E3), "oriented to person" (V4), "unable to follow complex commands" (implies M6) and "withdraws" (M4). | FIXED (C12): opens eyes only to pain, not oriented, occasional inappropriate words, does not follow commands, localizes to pain with both arms; total unchanged at 10, so the imaging decision does not rest on GCS. |
| B | minor | `patient.history_present_illness`, `patient.clinical_history.medications` | Steroid timeline contradictory (pulse and taper read as 8 months ago, while prednisolone was "tapered from 60 mg pulse initiated 10 days ago"); cyclophosphamide absent from the medication list; last HPI sentence narrated the team's differential. | FIXED: HPI separates the 7-day methylprednisolone course 8 months ago from prednisolone restarted at 60 mg 10 days ago with the first cyclophosphamide dose; medication entries updated and cyclophosphamide added; the differential sentence deleted. |
| B | minor | `patient.clinical_history.past_medical_history[2]` | "CKD stage 2" with baseline creatinine 1.4 in a 61-year-old man (CKD-EPI 2021 eGFR about 57, stage 3a). | FIXED: "stage 3a ... (estimated GFR about 57 mL/min/1.73m2)"; the drug check uses the current creatinine 1.6 (about 49). |
| B | minor | `initial_tool_outputs.labs` | Differential summed to 98%; no HIV result or liver tests though action-1 orders HIV and CMP. | FIXED (C12 labs): monocytes 2%; HIV-1/2 antigen/antibody non-reactive; AST 24, ALT 31, alkaline phosphatase 82, bilirubin 0.7, albumin 3.4 (low). Anion gap 16, unchanged. |
| B | minor | `followup_outputs[4]` (drug check) | Proposed regimen continued metformin and glipizide alongside the regimen it warned against; vancomycin and rifampin advice; formulary filler. | FIXED (C9): the case's regimen against prednisolone, cyclophosphamide, metformin, glipizide, aspirin; sulfonamide allergy; renal function. Criterion stays recommended with case-specific label and expected evidence; trigger `check_drug_interactions_empirical_regimen`. |
| B | minor | `fallback_tool_outputs.eeg`, `.cardiac_monitoring` | Normal EEG with 9-10 Hz posterior rhythm at GCS 10; Holter minimum 49 with HR 96. | FIXED: diffuse slowing without epileptiform discharges; sinus rhythm range 76 to 118. |
| A | minor | `action_criteria[*].citations`, `avoided_actions[*].citations` | `[IDSA_2004]`, `[De_Gans_2002]` and free-text duplicates. | FIXED: `[WHO_Meningitis_2025]` throughout. |
| B | minor | `metadata.difficulty_rationale`, `.difficulty_description` | "5 required tools; 4 red herrings"; "mixed CSF pleocytosis" (67% neutrophils). | FIXED: "4 required actions; 5 red herrings"; description refers to the negative Gram stain instead. |

## Changes, in one paragraph a physician can read before re-reviewing

The work-up is now labs (with HIV, liver tests and a complete differential), two sets of blood cultures, a non-contrast CT head, the index lumbar puncture, a recommended contrast MRI and a recommended drug check; the CSF and MRI are no longer given upfront, and the post-treatment repeat LP, duplicated PCR panel, CrAg lab step, pre-treatment audiometry and literature step are gone. CT before LP is HARD on WHO 2025 Annex A.4 grounds (severe immunocompromise: cyclophosphamide 10 days ago with high-dose prednisolone); NICE is not cited because it excludes immunosuppressed patients. The CT and MRI reports state findings only, and the MRI impression now leads with the leptomeningeal enhancement. The CSF report uses WHO reference values (ratio 0.04 from 11/287), reports the CSF cryptococcal antigen negative, and has a pattern-only interpretation. Blood cultures report S. pneumoniae in 2 of 2 sets with CLSI meningitis interpretation (penicillin MIC 0.12 resistant, ceftriaxone 0.5 or less susceptible). Musts: ceftriaxone within 60 minutes with vancomycin conditional, ampicillin for Listeria (age 61, diabetes, immunosuppression), dexamethasone 4 days for pneumococcus with the WHO stop rule, prednisolone held during dexamethasone and resumed without abrupt withdrawal, cyclophosphamide withheld, insulin, narrowing to ceftriaxone, droplet precautions, audiology. The record now has one steroid timeline, a GCS whose components match the description, CKD stage 3a, and no HPI sentence naming the differential; the presumed vasculitis is declared as the anchoring red herring and tested by a prohibition.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation key `[WHO_Meningitis_2025]` for the criteria pack allow-list (plan section 5.1).
- `interpret_labs` `serum_cryptococcal_antigen` (plan section 5.4): not needed for this case after the edit, listed only because the plan names RM02.

## Open questions for Andrea (judgment calls you could not settle)

- The plan lists "focal signs and severe immunosuppression" as the imaging limbs. I cite only severe immunocompromise: the bilateral extensor plantar responses and bilateral brisk knee jerks are not lateralizing, and the worsened dysarthria builds on a residual post-stroke dysarthria in a patient with depressed consciousness. The decision (CT required, HARD) is the same either way.
- The hearing must keeps "(NICE NG240)" for the 4-week timing, as the plan's canonical text and RM03 do, although NICE does not cover this patient.
- The steroid timeline is my reconstruction of contradictory text (methylprednisolone pulse 8 months ago; prednisolone restarted at 60 mg with the first cyclophosphamide 10 days ago). The source (PMC8131984) was not consulted.
- I added a must to hold prednisolone during dexamethasone and to withhold further cyclophosphamide; neither is in the plan or the note.

## Verification

Adversarial verifier, 23 October 2026. Checked: note 6e436225 against the final file (no NICE citation on the disease decisions; constraint reason states NICE does not cover him; ampicillin must for age 61, diabetes and immunosuppression; vancomycin conditional and the targeted must states ceftriaxone MIC 0.5 or less; no residual ampicillin-only literature text); CT before the index LP, MRI after it (`-v`); ratio 11/287 = 0.04; anion gap 129 - 94 - 19 = 16 with lactate 2.8; corrected sodium about 132; eGFR 57 (creatinine 1.4) and 49 (creatinine 1.6) by CKD-EPI 2021 verified; GCS E2 V3 M5 = 10 matches the rewritten narrative and is not below 10, so the imaging limb is correctly severe immunocompromise only; one steroid timeline across HPI, medications, CT label and constraint; MRI impression leads with the leptomeningeal enhancement; red-herring paths resolve.

Found and changed:
- `key_clinical_evidence[8]` was the template line "WHO 2025: obtain cultures promptly, but neither LP nor cranial imaging may delay empirical antimicrobials when the pathway requires treatment first.", duplicating `[1]`: deleted.

After the edit: `perfect_agent.py BACT-MEN-RM02 -v` passes; `case_io.py check` clean for the case.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (6 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients

Re-run: `perfect_agent.py` ok; `case_io.py check` clean for the case; BACT-MEN case guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality 'not_applicable', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 20, ECOG 4 (fallback_tool_outputs.clinical_assessment). Why: rule 3: GCS 10, unable to stand, febrile; even the pre-illness baseline (cane, residual dysarthria) excludes the library's Karnofsky 100.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: not testable (GCS 10, unable to stand) (followup_outputs[5] request_gait_and_balance_timed). Why: rule 3: the stored exam records that he cannot stand or walk; baseline gait required a cane.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no parkinsonian signs; bilateral pyramidal signs; challenge not performed (followup_outputs[6] request_levodopa_challenge). Why: rule 3: the library describes a normal motor examination and gait in a somnolent patient with bilateral extensor plantars.
- `perform_clinical_assessment {assessment_type: structured_headache_history_ichd3}`: new acute headache with red flags; criteria for a primary headache disorder not met (followup_outputs[7] request_structured_headache_history_ichd3). Why: rule 1 and 3: a febrile illness with falling consciousness on immunosuppression; the library elicits no red flags.
- `analyze_eeg {eeg_type: continuous_icu}`: continuous generalised theta-delta slowing; no epileptiform discharges or seizures (followup_outputs[8] request_continuous_icu). Why: rule 3: GCS 10 and the stored routine EEG shows diffuse slowing; the library reports a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: continuous generalised theta-delta slowing; no epileptiform discharges or seizures (followup_outputs[9] request_ambulatory). Why: rule 3: GCS 10 and the stored routine EEG shows diffuse slowing; the library reports a normal background.
- `perform_clinical_assessment {assessment_type: cognitive_screen}`: not completed (GCS 10) (followup_outputs[10] request_cognitive_screen). Why: rule 3: the stored exam states cognitive testing is not possible; the library reports MoCA 28/30.
- `order_specialized_test {test_type: neuropsych_battery}`: not completed (reduced consciousness) (fallback_tool_outputs.specialized_test). Why: rule 3: the stored exam states cognitive testing is not possible.
- `order_specialized_test {test_type: speech_language_evaluation}`: severe dysarthria; language not testable (followup_outputs[11] request_speech_language_evaluation). Why: rule 3: the stored exam records severely dysarthric speech, with mild residual dysarthria from a previous stroke.
- `order_microbiology {specimen: whole_blood_pcr}`: Streptococcus pneumoniae DNA detected (fallback_tool_outputs.microbiology). Why: rule 3: blood cultures grow S. pneumoniae in 2 of 2 sets collected before antimicrobials; it is a target of the panel.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: supine BP 142/82, HR 96; standing not performed (followup_outputs[12] request_orthostatic_blood_pressure). Why: rule 3: a patient unable to stand for 2 days cannot complete 3 minutes of standing.
- `order_advanced_imaging {modality: cerebral_angiography}`: hypoplastic arterial segments; no vasculitic change (fallback_tool_outputs.advanced_imaging). Why: rule 3: the history records an angiogram 8 months ago with hypoplastic vascular segments; the library reports normal calibre throughout.
- `order_advanced_imaging {modality: MR_angiography}`: hypoplastic arterial segments; no stenosis (followup_outputs[13] request_mr_angiography). Why: rule 3: the history records hypoplastic vascular segments on angiography 8 months ago; the library reports normal calibre throughout.
- `interpret_labs {panels: [ABG]}`: metabolic acidosis with partial respiratory compensation (fallback_tool_outputs.labs['ABG']). Why: rule 3: stored bicarbonate 19, lactate 2.8, creatinine 1.6 and RR 24; the library reports a normal gas.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
