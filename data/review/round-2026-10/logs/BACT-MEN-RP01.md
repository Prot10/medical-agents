# BACT-MEN-RP01
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 65ca8833-9e95-4d73-8436-55ec977ec77a | FIXED | Imaging (plan C2, C): no WHO 2025 Annex A.4 criterion at presentation (49, GCS 14, no focal signs, no papilledema, no seizure, immunodeficiency not yet known). Deleted the CT criterion `action-4-order-ct-scan`, the HARD constraint, the CT id from `stop_rule.required_before_assessment` and the CT follow-up; the IDSA must is replaced by "Proceed to lumbar puncture without prior cranial imaging ..." (`assessment.required_recommendations[3]`), the IDSA prohibition by "Do not delay lumbar puncture or antibiotics to obtain a CT head ..." (`prohibited_recommendations[1]`), and a waste avoided action `avoid-waste-5-order-ct-scan` was added. Microbiology: `followup_outputs[0].output.collected_before_antimicrobials` false; impression ends "Collected before the first IV dose; patient had taken amoxicillin-clavulanate 875/125 mg twice daily for 5 days before sampling."; the narrowing and "isolate is interpretable" sentences deleted. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.csf`, `followup_outputs` (`request_repeat_lp`) | Index CSF handed over upfront; a "repeat LP" (320 cells, Gram-positive diplococci, culture growth, antigen positive) was the first pathway step and answered action-3. | FIXED (C1): repeat LP deleted; index CSF is the `request_lumbar_puncture` follow-up; `-v` confirms action-3 receives it. |
| B | major | `followup_outputs` (`request_pcr_panel`, `request_audiometry`), `action-6-search-medical-literature` | PCR duplicated under `interpret_labs`; audiometry as `baep` before treatment; literature step expecting IDSA 2004, ESCMID, De Gans. | FIXED (C8, C9): all deleted; PCR result stays in the CSF report; hearing must added. |
| A | major | `ground_truth.action_criteria` | The label names CVID, but no criterion ordered the immunoglobulins that the case stores. | FIXED (plan): `action-5-interpret-labs-immunoglobulins` required, `interpret_labs {panels: [quantitative_Ig]}`, in the stop rule. The follow-up trigger was renamed `request_quantitative_ig` and its panel "Quantitative immunoglobulins" so a fresh `quantitative_Ig` order is served this report (the coverage test `test_no_required_order_receives_nothing_it_names` failed with the old names). |
| B | minor | `followup_outputs[2].output.panels.HIV_screen` | HIV result sat in the immunoglobulin report while action-1 orders HIV. | FIXED: moved to `initial_tool_outputs.labs.panels.HIV`. |
| C | major | `followup_outputs[0].output.susceptibility` | Penicillin MIC 0.12 called "intermediate". | FIXED (C6): "resistant (CLSI meningitis breakpoint: resistant at 0.12 or more)"; ceftriaxone 0.5 or less susceptible; second set and bottle intervals stated ("No growth at 48 hours; final report at 5 days"). |
| C | major | `assessment.required_recommendations` | Template vancomycin plus ceftriaxone; dexamethasone without stop rule; template Gram-stain dexamethasone prohibition; immunology must asked for IgG subclasses and an Ig level the case already measures. | FIXED (C4, C5): canonical ceftriaxone must (no Listeria risk factor), canonical dexamethasone must with "Continue for 4 days"; prohibition deleted; narrowing must (continue ceftriaxone, do not switch to penicillin or amoxicillin, MIC 0.12); immunology must to confirm CVID after excluding secondary causes and plan immunoglobulin replacement; hearing must. |
| B | minor | CSF report (`RBC`, `glucose`, `glucose_ratio`, `CSF_lactate`, `CSF_culture`, `interpretation`) | Glucose 38 called "low-normal" against a 40-70 reference; ratio "reference >0.6"; lactate reference "<2.1". | FIXED (C7): "38 mg/dL (low ...)", canonical ratio and lactate strings, culture "Pending (final report at 48 hours)", pattern-only interpretation. |
| B | minor | `followup_outputs[3]` (drug check) | Proposed dexamethasone 0.15 mg/kg with vancomycin; ampicillin "age >50" alternative; formulary text citing IDSA. | FIXED (C9): case regimen; sulfonamide allergy (avoid TMP-SMX, no beta-lactam allergy); dexamethasone and vancomycin CSF penetration if vancomycin is used; stop oral amoxicillin-clavulanate. Criterion stays recommended with case-specific expected evidence. |
| C | major | `ground_truth.red_herrings[1]`, `key_clinical_evidence` | Claimed that humoral immunodeficiency (HIV, CVID) blunts the CSF response and produces pauci-cellular CSF; the case's muted, mixed CSF is explained by 5 days of oral amoxicillin-clavulanate. | FIXED: red herring rewritten around partial treatment; pearl replaced by a partial-treatment pearl and a CVID recognition pearl. |
| B | minor | `ground_truth.red_herrings[2]` | "Sinus mucosal thickening on MRI" with no MRI in the case. | FIXED (C11): points at the HPI, where primary care attributed the headache to sinusitis; the CT with the sinus finding no longer exists (imaging C). |
| C | minor | `ground_truth.differential` | Viral meningitis and HSV moderate after S. pneumoniae on PCR; SAH entry irrelevant. | FIXED (C10): all low with the excluding result; sinusitis without meningitis replaces SAH; cryptococcal kept low (immunodeficiency, CrAg negative). |
| B | minor | `patient.history_present_illness` | Confusion noticed "today" (chief complaint, first paragraph) and "Yesterday" (second paragraph). | FIXED: "Earlier today, her husband noted ...". |
| B | minor | `initial_tool_outputs.labs` | "Sodium 131 (low — SIADH?)" in the summary; differential summed to 98.8%; no HIV or bilirubin. | FIXED: "(low)"; monocytes 1.2% (reference 0-10); HIV moved in; bilirubin 0.6 mg/dL. Anion gap 11 checked. |
| E | minor | `followup_outputs[2].output.abnormal_values_summary` | "critically low" and "Failed pneumococcal vaccine response" (interpretive). | FIXED: values with (low) and the titer result as measured. |
| A | minor | `action_criteria[*].citations`, `avoided_actions[*].citations` | Free-text duplicates, `[IDSA_2004]`, `[De_Gans_2002]`. | FIXED: `[WHO_Meningitis_2025]`. |
| B | minor | `metadata.difficulty_rationale`, `.difficulty_description` | "5 required tools", "immunocompromise produces pauci-cellular CSF", "sinusitis on imaging". | FIXED to match the case. |
| A | major | `ground_truth.action_criteria[1].alternatives[0].required_arguments` | `before_antimicrobials: true` was required although she had taken amoxicillin-clavulanate for 5 days, so an agent that orders the cultures truthfully (`false`) would miss the criterion. | FIXED: argument removed from the required arguments (specimen and tests kept); the report states the timing. Class issue for every pretreated BACT-MEN case (see Open questions). |

## Changes, in one paragraph a physician can read before re-reviewing

The pathway is labs (HIV, bilirubin, complete differential), two sets of blood cultures, the index lumbar puncture without prior imaging, quantitative immunoglobulins (now a required step, since the label names CVID), and a recommended drug check. No CT: at presentation she is 49, GCS 14, without focal signs, papilledema, seizure or known immunocompromise, so WHO 2025 Annex A.4 gives no imaging criterion; ordering a CT is waste, and the must and prohibition say why. The post-treatment repeat LP, the duplicate PCR panel, the audiometry and the literature step are gone. The CSF report keeps the partially treated picture (68 cells, mixed, glucose ratio 0.35, protein 78, lactate 3.8, Gram stain negative, S. pneumoniae on PCR) with WHO reference strings. Blood cultures are flagged as taken after 5 days of amoxicillin-clavulanate and the penicillin MIC of 0.12 is read as resistant by meningitis breakpoints, ceftriaxone susceptible. Musts: ceftriaxone within 60 minutes (vancomycin conditional), dexamethasone continued 4 days for pneumococcus, blood cultures, LP without CT, full CSF panel, continue ceftriaxone without switching to penicillin, droplet precautions, immunology referral to confirm CVID and plan immunoglobulin replacement, audiology. The red herrings now rest on partial treatment and on the primary-care sinusitis attribution, not on an unproven CVID effect or a non-existent MRI.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[WHO_Meningitis_2025]`, `[NICE_NG240]` for the criteria pack allow-list.

## Open questions for Andrea (judgment calls you could not settle)

- Plan Q2: CT is a `waste` avoided action here (no imaging criterion), following S05.
- The immunoglobulin report keeps the post-vaccine pneumococcal titers (12 of 14 serotypes non-protective). Such titers usually take days to return; if you want strict turnaround realism, move them to the immunology must instead.
- I added a second blood culture set with no growth (the must asks for two sets; the old report had only one aerobic bottle).
- `before_antimicrobials: true` removed from action-2's required arguments because the patient was already on antibiotics; the plan (3.1) keeps action-2 arguments unchanged, but the true value here is `false`. The same applies to every BACT-MEN case with antibiotics before sampling (plan C6 list: M01, M02, M03, M05, P04, RM01, RP03, RS04, S03, S06): the lead should decide it condition-wide.

## Verification

Adversarial verifier, 23 October 2026. Read the log, the diff and the whole patient, follow-ups and ground truth.
Checked: note 65ca8833 applied in both parts (C decision with CT criterion, HARD constraint, CT follow-up and
stop-rule id removed, canonical must, prohibition and waste avoided action; blood cultures `false` with the
5-day amoxicillin-clavulanate line). The plan's `action-5-interpret-labs-immunoglobulins` exists, is
required, in the stop rule and is served `request_quantitative_ig` under `-v`. Cross-field: paired glucose
108, ratio 38/108 = 0.35; CBC differential 78.5 + 12.3 + 8 + 1.2 = 100%; anion gap 11; total protein 5.2 with
albumin 3.1 fits hypogammaglobulinaemia (IgG 185); penicillin MIC 0.12 resistant and ceftriaxone susceptible by
CLSI meningitis breakpoints, and the narrowing must keeps ceftriaxone; no Listeria risk factor at presentation;
sulfonamide allergy consistent in patient, drug check and musts; no IDSA or template residue.
Found and fixed: `metadata.difficulty_description` called her "afebrile in the ED (on acetaminophen)" while
the vitals give 37.8 degrees Celsius; now "has only a low-grade temperature in the ED (37.8 degrees Celsius
on acetaminophen)".
Left as logged: post-vaccine pneumococcal titres in the immunoglobulin report (turnaround), the
condition-wide `before_antimicrobials` decision (see RM03 verification for the list of inconsistent cases).
`perfect_agent.py -v` and `case_io.py check` clean after the edit.

## Condition audit (23 October 2026)
- Condition-wide decision on the open `before_antimicrobials` question raised in this log: the argument is required only where the blood culture report flag `collected_before_antimicrobials` is true, and absent where it is false. This case already follows the rule (argument absent, flag false); no change to the case for it.
- Deleted `ground_truth.key_clinical_evidence` template line "WHO 2025: obtain cultures promptly, but neither LP nor cranial imaging may delay empirical antimicrobials when the pathway requires treatment first." It duplicates the C17 timing line already present and reads as authoring text; the RM01 and RM02 verifiers deleted the same line there.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (4 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients
- Serotype-specific pneumococcal antibody result made pending with a realistic send-out turnaround (about 2 weeks) instead of returning with the immunoglobulins; the immunology must no longer relies on it

Re-run: `perfect_agent.py` ok; `case_io.py check` clean for the case; BACT-MEN case guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality 'not_applicable', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 40, ECOG 3 (fallback_tool_outputs.clinical_assessment). Why: rule 3: progressive headache, neck stiffness and new confusion (GCS 14) on a background of 2 years of recurrent infections; the library's Karnofsky 100 describes a person without disease.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: not performed (headache, unsteadiness on standing) (followup_outputs[4] request_gait_and_balance_timed). Why: rule 3: the stored exam records gait not formally tested, with mild unsteadiness on standing.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no parkinsonian signs; neck stiffness noted; challenge not administered (followup_outputs[5] request_levodopa_challenge). Why: rule 3: the library reports a normal gait and neck in a patient with neck stiffness and unsteadiness on standing; no challenge would be given without parkinsonism.
- `perform_clinical_assessment {assessment_type: structured_headache_history_ichd3}`: new acute headache with red flags; criteria for a primary headache disorder not met (followup_outputs[6] request_structured_headache_history_ichd3). Why: rule 1 and 3: a progressive febrile headache with neck stiffness and confusion; the library elicits no red flags.
- `analyze_brain_mri`: thin leptomeningeal enhancement; paranasal sinus disease; no complication (fallback_tool_outputs.mri). Why: rule 1: no brain imaging is stored; an MRI with gadolinium in this patient would not be normal (recurrent sinopulmonary infections, current sinus symptoms).
- `perform_clinical_assessment {assessment_type: cognitive_screen}`: MoCA 24/30 with mild inattention and reduced recall (followup_outputs[7] request_cognitive_screen). Why: rule 3: the stored exam records mild inattention, recall 2 of 3 and an initial error on the date; the library reports MoCA 28/30.
- `order_specialized_test {test_type: neuropsych_battery}`: mildly reduced attention, processing speed and recall (fallback_tool_outputs.specialized_test). Why: rule 3: the stored exam records mild inattention and reduced recall.
- `order_microbiology {specimen: whole_blood_pcr}`: Streptococcus pneumoniae DNA detected (fallback_tool_outputs.microbiology). Why: rule 3: blood cultures grow S. pneumoniae (1 of 2 sets), a target of the panel; collected after 5 days of amoxicillin-clavulanate.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: no orthostatic hypotension; resting HR 92 (followup_outputs[8] request_orthostatic_blood_pressure). Why: rule 3: presenting HR 92 and unsteadiness on standing; the library reports a supine HR of 68 without symptoms.
- `interpret_labs {panels: [IgA]}`: IgA 12 mg/dL (low) (fallback_tool_outputs.labs['IgA']). Why: rule 3: the stored immunoglobulin panel shows IgA 12 mg/dL; the library reports IgA 210.
- `interpret_labs {panels: [IgG_subclasses]}`: all IgG subclasses low (fallback_tool_outputs.labs['IgG_subclasses']). Why: rule 3: the stored total IgG is 185 mg/dL; subclasses cannot all be normal.
- `order_body_imaging {study: chest_CT}`: bilateral basal bronchiectasis with mucus plugging (fallback_tool_outputs.body_imaging). Why: rule 2: bronchiectasis on chest CT 6 months ago, bilateral basal crackles now; the library reports clear lungs.
- `order_body_imaging {study: chest_CTA}`: no embolism; bilateral basal bronchiectasis (followup_outputs[9] request_chest_cta). Why: rule 2: bronchiectasis on chest CT 6 months ago; the library reports normal lungs.
- `order_body_imaging {study: chest_xray}`: basal bronchial wall thickening (followup_outputs[10] request_chest_xray). Why: rule 2: known bronchiectasis with basal crackles; the library reports clear lungs.
- `order_body_imaging {study: chest_abdomen_pelvis_CT}`: bronchiectasis and mild splenomegaly (followup_outputs[11] request_chest_abdomen_pelvis_ct). Why: rule 2 and 3: known bronchiectasis and mild splenomegaly on palpation; the library reports a normal study.
- `order_body_imaging {study: pelvis_abdomen_CT}`: mild splenomegaly (followup_outputs[12] request_pelvis_abdomen_ct). Why: rule 3: mild splenomegaly on palpation; the library reports a normal spleen.
- `order_body_imaging {study: pelvis_abdomen_ultrasound}`: mild splenomegaly (followup_outputs[13] request_pelvis_abdomen_ultrasound). Why: rule 3: mild splenomegaly on palpation; the library reports a normal spleen size.
- `order_body_imaging {study: pelvis_abdomen_MRI}`: mild splenomegaly (followup_outputs[14] request_pelvis_abdomen_mri). Why: rule 3: mild splenomegaly on palpation; the library reports a normal spleen.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
