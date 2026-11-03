# BACT-MEN-RM03
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 1a8db197-d724-4a60-a5e0-3e6e62616063 | FIXED | SCOPE: every NICE reference removed from this case's musts, constraints and pearls; the HARD constraint reason states "NICE NG240 does not cover this patient (asplenia is an immunodeficiency outside its scope)"; all citations are `[WHO_Meningitis_2025]`. The one exception is the hearing must, which keeps the plan's canonical "(NICE NG240)" timing (see Open questions). RED HERRING NPH: `ground_truth.red_herrings[1].correct_interpretation` is now the reviewer's text verbatim; `field_path` points at the CT finding (`followup_outputs[1].output.findings[0]`) instead of the non-existent `initial_tool_outputs.mri`. DIFFERENTIAL: "Normal pressure hydrocephalus" (G91.2) added at high, with key_features giving what supports it and the CSF that shows it is not the sole cause; cryptococcal meningitis dropped. CRITICAL ACTIONS: template "vancomycin 15-20 mg/kg + ceftriaxone 2 g" must replaced by the canonical ceftriaxone must with vancomycin conditional on local resistance (`required_recommendations[0]`) and a Listeria must, ampicillin 2 g IV every 4 hours for age 74, diabetes and asplenia (`[1]`). ORDERING: index CSF moved from `initial_tool_outputs.csf` to `followup_outputs[2]` (`request_lumbar_puncture`), after the CT (`followup_outputs[1]`); the repeat LP deleted; CT impression no longer says "Safe to proceed with lumbar puncture"; the HARD constraint is kept because a WHO criterion is present. STEP 3: `followup_outputs[0].output.collected_before_antimicrobials` false; impression ends "Collected before the first intravenous dose; patient had received oral amoxicillin-clavulanate 625 mg three times daily for 3 days prior."; the "isolate is interpretable" sentence deleted. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.action_criteria[2]`, `sequence_constraints`, `assessment.*`, `key_clinical_evidence` | CT before LP justified with IDSA 2004 ("altered mental status ... age >60"). | FIXED (plan C2 A): label, rationale, expected evidence, must, prohibition, pearl and HARD constraint now give the WHO 2025 Annex A.4 limbs present: asplenia (severe immunocompromise) and the left extensor plantar response (focal sign). SOFT constraint blood cultures before CT added. |
| B | major | `action_criteria`, `followup_outputs` | Repeat LP (post-treatment, WBC "decreased from 380") was the first pathway step and answered action-3 for the perfect agent; index CSF was handed over upfront. | FIXED (C1): repeat LP deleted; index CSF is the `request_lumbar_puncture` follow-up; `-v` confirms action-3 now receives it. Criteria ordered labs, blood cultures, CT, CSF, drug check. |
| D | major | `followup_outputs` (`request_pcr_panel`), `action-6-search-medical-literature`, literature follow-up | PCR panel duplicated under `interpret_labs`; literature step expected IDSA 2004, ESCMID 2016 and De Gans and gave "ampicillin if over 50". | FIXED (C8, C9): both follow-ups and the literature criterion deleted; the PCR result stays in the index CSF report. |
| B | minor | `followup_outputs` (`request_audiometry`) | Audiometry filed as `baep`, showing hearing loss before any treatment was possible. | FIXED (C8): deleted; hearing must added. |
| B | minor | CSF report (`cell_count.RBC`, `glucose_ratio`, `special_tests`, `interpretation`) | RBC 2 called "likely traumatic tap artifact"; ratio written without paired values or WHO reference; latex pneumococcal antigen reported alongside the confirming PCR; interpretation a copy of the values. | FIXED (C7): "2 cells/microL (within normal limits)"; "0.14 (CSF 32 mg/dL / blood 227 mg/dL; reference 0.5 to 0.8, 0.4 or less abnormally low)"; latex antigen removed (not used deliberately; the red herring also cited it as confirmatory); culture "Pending (final report at 48 hours)"; pattern-only interpretation. |
| B | minor | `followup_outputs[1].output` (CT) | Finding with empty description; impression a run-on sentence with an LP-safety conclusion. | FIXED (C3): description of the ventricular enlargement and patent cisterns; numbered findings-only impression. |
| B | minor | `followup_outputs[0].output` (blood cultures) | One set reported although the must asks for two; anaerobic "no growth at 5 days" given at the work-up decision; MICs as loose findings. | FIXED (C6): set 1 aerobic bottle S. pneumoniae at 14 hours, other bottles "No growth at 48 hours; final report at 5 days"; MICs moved to `susceptibility` with CLSI meningitis breakpoints (penicillin 0.06 susceptible, ceftriaxone 0.5 or less susceptible, vancomycin 0.5); Gram stain field filled. |
| C | major | `assessment.required_recommendations` | Dexamethasone must without a stop rule; template "Do NOT discontinue dexamethasone solely because the Gram stain is negative" prohibition. | FIXED (C5): canonical must plus "Continue for 4 days: Streptococcus pneumoniae is identified."; prohibition deleted. |
| C | minor | `assessment.required_recommendations` | "Reassess and de-escalate" must was generic. | FIXED: targeted must naming the isolate's MICs, stopping ampicillin and any vancomycin, ceftriaxone or benzylpenicillin to continue (no duration added, per plan 1.2). |
| C | minor | `assessment.prohibited_recommendations` | Nothing tested the trap the case is built on. | FIXED: prohibition against attributing the febrile deterioration to NPH, with shunt decisions deferred until the meningitis is treated. Pearl added with the same content. |
| B | minor | `patient.clinical_history.past_medical_history[3]`, `patient.history_present_illness` | "CKD stage 2, baseline creatinine 1.1" in a 74-year-old woman: CKD-EPI 2021 gives an eGFR of about 53 (stage 3a). | FIXED: "stage 3a, baseline creatinine 1.1 mg/dL (estimated GFR about 53 mL/min/1.73m2)" in both places; the drug check uses the current creatinine 1.3 (eGFR about 43). |
| B | minor | `patient.history_present_illness` | Fever "over the past three days" in the first sentence vs "developed a low-grade fever two days ago" later. | FIXED: "over the past two days". |
| D | minor | `patient.history_present_illness` | Last sentence narrated the ED physician weighing NPH against infection (names the differential and its resolution). | FIXED (C12): sentence deleted; the outpatient NPH concern and prior ventricular enlargement stay as history. |
| B | minor | `initial_tool_outputs.labs` | Action-1 orders HIV and CMP, but no HIV result or bilirubin; differential summed to 97.5% (no monocytes). | FIXED (C12 labs): HIV-1/2 antigen/antibody non-reactive, total bilirubin 0.8 mg/dL, monocytes 2.5%. Anion gap 14 checked, unchanged. |
| B | minor | `followup_outputs[3]` (drug check) | Checked only dexamethasone (0.15 mg/kg, a paediatric dose) and missed the antibiotics, the allergy and renal function. | FIXED (C9): proposed regimen is the case's (ceftriaxone, ampicillin, dexamethasone 10 mg, vancomycin conditional); interactions metformin, aspirin, losartan with vancomycin; warnings for the sulfonamide allergy (no beta-lactam cross-reactivity, tolerating amoxicillin-clavulanate), renal dosing, metformin hold, hyperglycaemia; formulary filler removed. Criterion stays recommended with case-specific label and expected evidence; trigger renamed `check_drug_interactions_empirical_regimen`. |
| C | minor | `ground_truth.differential` | Boilerplate list (viral meningitis and HSV moderate) after a bacterial CSF with a named organism. | FIXED (C10): NPH high; Listeria meningitis low (raised by the risk factors, excluded by PCR); viral meningitis, HSV encephalitis, TB low with the excluding results; SAH very low. |
| B | minor | `ground_truth.red_herrings[0]` | Pointed at `initial_tool_outputs.csf`; said antigen testing confirms the organism. | FIXED: points at the Gram stain field of the LP report; interpretation per WHO 2025 sensitivity and the PCR. |
| A | minor | `action_criteria[*].citations`, `avoided_actions[*].citations` | Free-text duplicates ("WHO meningitis guideline 2025", "IDSA 2004 §V", "De Gans 2002") and `[IDSA_2004]`. | FIXED: `[WHO_Meningitis_2025]` throughout. |
| B | minor | `fallback_tool_outputs.ecg` | Fallback ECG at rate 60 in a patient with HR 102. | FIXED: sinus tachycardia, rate 102. |
| B | minor | `metadata.difficulty_rationale` | "5 required tools". | FIXED: "4 required actions; 2 red herrings". |
| A | major | `ground_truth.action_criteria[1].alternatives[0].required_arguments` | `before_antimicrobials: true` was required although she had taken oral amoxicillin-clavulanate for 3 days, so an agent that orders the cultures truthfully (`false`) would miss the criterion. | FIXED: argument removed from the required arguments (specimen and tests kept); the report states the timing. Class issue for every pretreated BACT-MEN case (see Open questions). |

## Changes, in one paragraph a physician can read before re-reviewing

The work-up is now labs (with HIV, bilirubin and a complete differential), two sets of blood cultures, a non-contrast CT head, then the index lumbar puncture, then a recommended drug check; the CSF is no longer given upfront, the post-treatment repeat LP, the duplicated PCR panel, the pre-treatment audiometry and the literature step are gone. CT before LP is kept as a HARD constraint on WHO 2025 Annex A.4 grounds that are actually present (asplenia as a severe immunocompromised state, and the left extensor plantar response), with blood cultures and antibiotics before imaging; NICE is not cited because it excludes asplenic patients. The CT reports communicating hydrocephalus (Evans index 0.37) with patent cisterns and no LP-safety conclusion. The CSF report uses WHO reference values (RBC 2 within normal limits; ratio 0.14 against 0.5 to 0.8) and a pattern-only interpretation; the latex antigen was removed. Blood cultures are flagged as taken after 3 days of oral amoxicillin-clavulanate, report S. pneumoniae from 1 of 2 sets at 14 hours with CLSI meningitis MICs. Musts: ceftriaxone within 60 minutes with vancomycin conditional, ampicillin for Listeria (age 74, diabetes, asplenia), dexamethasone continued 4 days for pneumococcus with the WHO stop rule, blood cultures, CT before LP with the WHO limbs, full CSF panel, narrowing to ceftriaxone or benzylpenicillin on the MICs, droplet precautions, audiology. A new prohibition tests the NPH trap. NPH is in the differential at high (as ruled) with what supports it and why it cannot be the sole cause; cryptococcal meningitis is out. Record fixes: CKD stage 3a (eGFR about 53 from creatinine 1.1), fever two days, the HPI sentence narrating the differential removed.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation key `[WHO_Meningitis_2025]` for the criteria pack allow-list (plan section 5.1).
- Criteria pack still carries the IDSA 2004 imaging list and "add ampicillin if >50" (plan section 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- The hearing must keeps "(NICE NG240)" for the 4-week timing, as the plan's canonical text does, although the reviewer ruled that NICE does not govern this asplenic patient. It is cited for timing only; the requirement itself is also WHO practice. Change to WHO-only wording if you want the case free of NICE.
- NPH is at "high" as Reviewer 2 ruled: I read it as a likely coexisting condition (five weeks of gait and cognitive decline predate the infection), not as the competing explanation of the acute illness, and wrote key_features accordingly.
- The latex pneumococcal antigen was deleted from the CSF report under plan C7 (antigen kept only where used deliberately). The reviewer did not ask for it; restore if you want the partial-treatment antigen teaching point.
- `before_antimicrobials: true` removed from action-2's required arguments because the patient was already on antibiotics; the plan (3.1) keeps action-2 arguments unchanged, but the true value here is `false`. The same applies to every BACT-MEN case with antibiotics before sampling (plan C6 list: M01, M02, M03, M05, P04, RM01, RP03, RS04, S03, S06): the lead should decide it condition-wide.

## Verification

Adversarial verifier, 23 October 2026. Read the log, the full diff and the whole final case.
Checked: note 1a8db197 is applied in every part (WHO-only scope except the canonical hearing must; NPH
red herring carries the reviewer's text and points at the CT finding; NPH high and cryptococcal dropped;
ampicillin must for age 74, diabetes and asplenia, vancomycin conditional; CT before the index LP, repeat
LP gone, no LP-safety sentence in the CT; blood cultures `false` with the reviewer's collection line).
Cross-field: paired glucose 227 in labs and CSF, ratio 32/227 = 0.14; anion gap 131 - 97 - 20 = 14;
CKD-EPI 2021 eGFR 53 (creatinine 1.1) and 43 (1.3) recomputed and correct; differential sums to 100%;
GCS 13 (E3 V4 M6) matches the narrative; HARD and SOFT constraints reference existing ids and the
`-v` trace serves `request_lumbar_puncture` to action-3; no IDSA 2004, "normal >0.6", traumatic-tap,
narrowing or LP-safety text left; no new dashes.
Found and fixed: the must "Send full CSF panel (... lactate)" asked for a CSF lactate that the index CSF
report did not contain (28 of the 30 BACT-MEN CSF reports carry one). Added
`special_tests.CSF_lactate` "6.9 mmol/L (local laboratory reference <3.5 mmol/L)" and the value to the
pattern-only interpretation, consistent with 380 cells and a ratio of 0.14.
Left as logged: the worker's removal of `before_antimicrobials: true` from action-2 is correct against the
tool's parameter definition ("whether the specimen is being taken before the first antimicrobial dose"),
but the condition is now inconsistent: M01, M02, M03, M05, P02, P04, RP05 and RS04 still require `true`
in pretreated patients while RM01, RM03, RP01, RP02 and RP03 do not. A condition-wide decision for the lead.
`perfect_agent.py -v` and `case_io.py check` clean after the edit.

## Condition audit (23 October 2026)
- Condition-wide decision on the open `before_antimicrobials` question raised in this log: the argument is required only where the blood culture report flag `collected_before_antimicrobials` is true, and absent where it is false. This case already follows the rule (argument absent, flag false); no change to the case for it.
- Deleted `ground_truth.key_clinical_evidence` template line "WHO 2025: obtain cultures promptly, but neither LP nor cranial imaging may delay empirical antimicrobials when the pathway requires treatment first." It duplicates the C17 timing line already present and reads as authoring text; the RM01 and RM02 verifiers deleted the same line there.

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

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 20, ECOG 4 (fallback_tool_outputs.clinical_assessment). Why: rule 3: drowsy (GCS 13), febrile, unable to stand; even the pre-illness state (5 weeks of shuffling gait with near-falls, cognitive impairment) excludes the library's Karnofsky 100.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: not testable (drowsy, cannot stand); prior shuffling small-step gait noted (followup_outputs[4] request_gait_and_balance_timed). Why: rule 3: the stored exam records that she cannot stand unassisted, after weeks of a shuffling small-step gait.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no rest tremor; increased tone; challenge not performed (followup_outputs[5] request_levodopa_challenge). Why: rule 3: the library describes a normal motor examination and gait in a drowsy patient who cannot stand and had a shuffling gait.
- `perform_clinical_assessment {assessment_type: structured_headache_history_ichd3}`: new acute headache with red flags; criteria for a primary headache disorder not met (followup_outputs[6] request_structured_headache_history_ichd3). Why: rule 1 and 3: an acute febrile headache with neck stiffness and falling consciousness; the library elicits no red flags.
- `analyze_brain_mri`: communicating hydrocephalus, leptomeningeal and ependymal enhancement with ventricular debris, small vessel change (fallback_tool_outputs.mri). Why: rule 1 and 3: no MRI is stored; the stored CT shows communicating hydrocephalus and small vessel change, and an MRI with gadolinium would not be normal.
- `analyze_eeg {eeg_type: routine}`: continuous generalised theta-delta slowing; no epileptiform discharges or seizures (fallback_tool_outputs.eeg). Why: rule 3: no EEG is stored and the patient is drowsy and confused (GCS 13); the library reports a normal background.
- `analyze_eeg {eeg_type: sleep_deprived}`: continuous generalised theta-delta slowing; no epileptiform discharges or seizures (followup_outputs[7] request_sleep_deprived). Why: rule 3: drowsy and confused (GCS 13); the library reports a normal background.
- `analyze_eeg {eeg_type: continuous_icu}`: continuous generalised theta-delta slowing; no epileptiform discharges or seizures (followup_outputs[8] request_continuous_icu). Why: rule 3: drowsy and confused (GCS 13); the library reports a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: continuous generalised theta-delta slowing; no epileptiform discharges or seizures (followup_outputs[9] request_ambulatory). Why: rule 3: drowsy and confused (GCS 13); the library reports a normal background.
- `perform_clinical_assessment {assessment_type: cognitive_screen}`: K-MMSE about 15/30; MoCA not completed (followup_outputs[10] request_cognitive_screen). Why: rule 3: the stored exam records an estimated K-MMSE of 15 with disorientation and recall 0/3, on known mild cognitive impairment; the library reports MoCA 28/30.
- `order_specialized_test {test_type: neuropsych_battery}`: not completed (reduced arousal, inattention) (fallback_tool_outputs.specialized_test). Why: rule 2 and 3: known mild cognitive impairment and an acute confusional state; the library reports average performance in every domain.
- `order_microbiology {specimen: whole_blood_pcr}`: Streptococcus pneumoniae DNA detected (fallback_tool_outputs.microbiology). Why: rule 3: blood cultures grow S. pneumoniae (1 of 2 sets), a target of the panel; collected after 3 days of oral amoxicillin-clavulanate.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: supine BP 148/82, HR 102; standing not performed (followup_outputs[11] request_orthostatic_blood_pressure). Why: rule 3: a patient who cannot stand unassisted, HR 102; the library reports HR 68 and 3 minutes of standing.
- `interpret_labs {panels: [peripheral smear]}`: Howell-Jolly bodies, toxic granulation (fallback_tool_outputs.labs['peripheral smear']). Why: rule 2: splenectomy at age 52 for ITP; stored WBC 18.7 with 8% bands.
- `interpret_labs {panels: [HbA1c]}`: HbA1c 7.8% (fallback_tool_outputs.labs['HbA1c']). Why: rule 2: type 2 diabetes on metformin with an HbA1c of 7.8% three months ago in the history.
- `order_body_imaging {study: spine_MRI}`: L4-L5 disc herniation; cord normal (fallback_tool_outputs.body_imaging). Why: rule 2: lumbar disc herniation at L4-L5 in the history; the library reports no disc protrusion.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
