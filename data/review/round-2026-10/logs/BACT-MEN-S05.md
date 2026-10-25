# BACT-MEN-S05
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 3f67586c-846f-4a99-b0a8-400c58349e37 | FIXED | `ground_truth.key_clinical_evidence[6]`: "MenACWY at age 11 does not cover serogroup B: this is not vaccine failure or a lapse in coverage. Serogroup B is covered by a separate MenB vaccine, recommended for adolescents and students in several national programmes, which also bears on what contacts are offered." The public health must now adds that vaccination of contacts follows public health advice on MenB vaccine. The blood culture report gives serogroup B from reference typing at 72 hours (it was reported at 10 hours). |
| 7754d72d-0dce-4fe1-949d-75b4610f9a36 | FIXED | Plan C5. Dexamethasone must replaced by the canonical C5 sentence plus "Stop dexamethasone on identification of Neisseria meningitidis (WHO 2025; NICE NG240 1.8.3)."; the key evidence line that recommended dexamethasone "across all causes" replaced by the canonical sentence; literature output claiming it was recommended for all causes deleted. |
| 45c01665-cad3-4c28-ad27-95f662ae2d29 | FIXED | Plan C14. "Monitor closely for signs of meningococcemia progression (... DIC)" replaced by the canonical DIC must (septic shock with overt DIC, vasopressors to MAP 65 mmHg or more, serial platelets, fibrinogen, INR and D-dimer with replacement, serial mapping of purpura, adrenal haemorrhage if shock persists); key evidence line naming the values as overt DIC already present and Waterhouse-Friderichsen as the classic complication. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `initial_tool_outputs.csf`; literature criterion and follow-up | Index CSF in the initial work-up (plan C1); literature step expecting IDSA 2004, ESCMID and De Gans (plan C9). | FIXED: CSF is `followup_outputs[1]` (`request_lumbar_puncture`), confirmed by `-v`; literature criterion and output deleted. |
| D | major | index CSF | Culture "preliminary growth at 12 hours", RBC 3 "likely traumatic tap artifact", ratio reference ">0.6", interpretation concluding "consistent with bacterial infection" (plan C7). | FIXED: culture "Pending"; canonical RBC, ratio (0.25 from 22/88) and lactate strings; values-only interpretation. |
| B | major | blood cultures | Serogroup B at 10 hours; "aerobic" sets; vancomycin line with a management clause; narrowing and interpretability boilerplate; em dashes in keys (plan C6). | FIXED: two sets positive at 10 and 11 hours, identified at 20 hours, susceptibilities at 48 hours, serogroup B from the reference laboratory at 72 hours; vancomycin "Not applicable (Gram-negative organism, intrinsically resistant)" kept as the plan says; trigger renamed `request_blood_cultures`. `collected_before_antimicrobials` true kept (no antibiotics before collection). |
| C | major | `ground_truth.assessment.required_recommendations` | Vancomycin loading plus ceftriaxone mandated (plan C4); targeted course "7-day" from IDSA 2004 against NICE NG240's 5 days for N. meningitidis. | FIXED: canonical base regimen; narrowing must "ceftriaxone (or benzylpenicillin) for Neisseria meningitidis for 5 days (NICE NG240)". No Listeria cover (19 years, negative pregnancy test). |
| E | major | `ground_truth.assessment.prohibited_recommendations` | "Do NOT list analyze_csf as a harmful tool in the absence of mass effect" is an engineering note to case authors, not a clinical prohibition (PATTERNS 5). | FIXED: deleted. The CT prohibition replaced by the canonical no-imaging prohibition. |
| C | minor | `ground_truth.avoided_actions[avoid-waste-6-order-ct-scan]`, key evidence | CT waste rationale and pearl based on IDSA 2004. | FIXED: canonical C rationale with GCS 15; canonical no-imaging must as the pearl; all avoided actions cite `[WHO_Meningitis_2025]`. |
| C | minor | `ground_truth.differential` | "Meningococcemia without meningitis" `high` although the CSF shows meningitis; viral meningitis and pneumococcal meningitis `moderate` although excluded (plan C10). | FIXED: septicaemia without meningitis low (septicaemia present, meningitis proven); pneumococcal and viral low with the excluding data; exanthem and SAH very low. |
| C | minor | `ground_truth.key_clinical_evidence[1]` | Called petechiae "pathognomonic of meningococcemia" (S04 shows the same picture with pneumococcus) and said "(intended red herring)". | FIXED: rewritten without the overclaim or the authoring note. |
| B | minor | `patient.chief_complaint`, `history_present_illness` | "Sudden-onset" and "abrupt-onset ... the worst of her life" headache undeclared as a SAH signal (plan C11); "White woman" irrelevant (class of note c4589441). | FIXED: "Severe headache ..."; "a severe, rapidly worsening bifrontal and occipital headache"; ethnicity removed from the HPI. |
| B | minor | `initial_tool_outputs.labs` | No HIV or liver tests (plan C12); anion gap 17 (133 - 99 - 17); no pregnancy test in a 19-year-old woman, although pregnancy is a Listeria risk factor that decides the empirical regimen. | FIXED: HIV non-reactive; ALT 24, AST 30, ALP 71, bilirubin 0.9, albumin 3.7; chloride 100 (anion gap 16); serum beta-hCG <2 mIU/mL. |
| C | minor | `followup_outputs[2]` (drug check) | Checked vancomycin with dexamethasone, formulary text, hypothetical penicillin allergy (plan C9). | FIXED: ceftriaxone and dexamethasone against no medicines, no allergies and a negative pregnancy test; criterion recommended with concrete expected evidence. |
| D | minor | `fallback_tool_outputs.ct.impression` | "No contraindication to lumbar puncture identified" (plan C3). | FIXED: findings only. |
| A | minor | citations, metadata | IDSA 2004 and free-text citations; "4 required tools" with an em dash. | FIXED: `[WHO_Meningitis_2025]`; "3 required tools". |
| C | minor | `required_recommendations` | No hearing assessment. | FIXED: canonical hearing must. |

## Changes, in one paragraph a physician can read before re-reviewing
The pathway is blood tests (now with HIV, liver tests and a negative pregnancy test), blood cultures and the index LP without imaging (GCS 15, no criterion), then a drug check; the literature step is gone. The CSF reports values and pattern with culture pending and N. meningitidis on PCR; blood cultures grow N. meningitidis at 10 and 11 hours with serogroup B from the reference laboratory at 72 hours. Musts: ceftriaxone without routine vancomycin, dexamethasone stopped once N. meningitidis is identified, droplet precautions, septic shock with overt DIC treated explicitly (including adrenal haemorrhage), public health notification and chemoprophylaxis with MenB advice for contacts, ceftriaxone or benzylpenicillin for 5 days, and audiology. A new teaching point states that MenACWY does not cover serogroup B, so this is not vaccine failure. An engineering note posing as a prohibition was removed and the differential now reflects the results.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys `[NICE_NG240]` and `[WHO_Meningitis_2025]` (plan 5.1).
- Fallback library (plan 5.8): this case's own CT fallback carried "No contraindication to lumbar puncture identified"; the benchmark library should be checked for the same sentence.

## Open questions for Andrea (judgment calls you could not settle)
- Overt DIC is stated as Reviewer 2 ruled. On the ISTH overt-DIC score the values (platelets 94, D-dimer 5.2 mg/L, PT 14.1 s, fibrinogen 158 mg/dL) score about 3 to 4, below the cut-off of 5; with spreading purpura and shock the clinical call is reasonable, but a haematologist may prefer "DIC evolving" wording.
- Duration changed from 7 days (IDSA 2004, stated by the case) to 5 days (NICE NG240, plan 1.2) for N. meningitidis.

## Verification
Adversarial verification, 23 October 2026. Checked: all three note ids present; MenACWY versus serogroup B in key evidence and the contacts must; dexamethasone stop on N. meningitidis; DIC must; no CT criterion, CT waste with the canonical rationale; index CSF served to action-3 (`-v`). Recomputed anion gap 16 (133 - 100 - 17), ratio 0.25 (22/88, BMP glucose). Timeline (onset about 18:30, arrival 02:30) agrees with the 8-hour history. Fallback CT and MRI carry no LP-safety or diagnostic text.
Found and changed:
- DIC must, `differential[0]` and `[3]`, `key_clinical_evidence`: the case called her state "septic shock" and "hypotension", but her pressure is 102/62 after 500 mL (EMS 98/60), with no vasopressor need; Sepsis-3 shock requires vasopressors for MAP 65 mmHg or more with lactate above 2. The must now reads "Treat as meningococcal sepsis with overt DIC: fluid resuscitation guided by perfusion (heart rate 124, blood lactate 3.6 mmol/L), vasopressors to a mean arterial pressure of at least 65 mmHg if hypotension develops, ..., assess for adrenal haemorrhage (Waterhouse-Friderichsen) if shock develops." The differential entries cite "raised lactate" and "coagulopathy" instead of "shock"; the key evidence line says "spreading purpura, tachycardia and a raised lactate". The HPI's "hypotensive at 98/60" (the paramedics' description) is unchanged.
Open question added for Andrea: spreading purpura with platelets 94 is among NICE's reasons to delay lumbar puncture (see the S04 verification); the LP stays required here pending the lead's decision.
Re-run: `perfect_agent.py BACT-MEN-S05 -v` ok; `case_io.py check` clean for the case.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (4 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients
- PT 14.1 -> 15.6 s and INR 1.3 -> 1.4 so the stored values give an ISTH overt-DIC score of 5, matching Reviewer 2's ruling that DIC is present (45c01665)
- Index LP made optional and removed from the stop rule; the 'proceed to LP' must and its prohibition replaced by deferral until the purpura stops spreading, she is stable and coagulation is corrected (NICE NG240 1.4.11, 1.4.12: no LP with extensive or rapidly spreading purpura; WHO 2025 A.1.1: no LP with a bleeding diathesis or haemodynamic compromise); blood cultures and blood PCR carry the diagnosis; differential key features no longer depend on the CSF

Re-run: `perfect_agent.py` ok; `case_io.py check` clean for the case; BACT-MEN case guards pass; synonym `--check` clean.

## Central vocabulary wired (24 Oct 2026)

Blood meningococcal PCR is the existing core term `order_microbiology` `specimen: whole_blood_pcr` (EDTA whole-blood PCR for N. meningitidis, S. pneumoniae and H. influenzae); its description in the tool, the `tool_io.py` mirror, `costs.yaml` and `TOOL_PARAMETER_VOCABULARY.md` now names it as the meningococcal blood PCR. No second spelling was added (one study, one term).

- `ground_truth.action_criteria`: new `action-6-order-microbiology-blood-pcr` (recommended, `{specimen: whole_blood_pcr}`, `[NICE_NG240]`), placed after the blood cultures, so the deferred-LP pathway scores the organism test (plan decisions CENTRAL 2). Not in the stop rule: blood cultures remain the required organism test.
- `followup_outputs[1]`: new `request_whole_blood_meningococcal_pcr`, N. meningitidis (ctrA) detected at 6 hours, S. pneumoniae and H. influenzae not detected, collected before antimicrobials (as the blood cultures).
- Musts and key evidence unchanged: they already say "Blood cultures and blood meningococcal PCR establish the organism meanwhile".

Re-run: `perfect_agent.py BACT-MEN-S05 -v` ok (action-6 receives `followup[1]`); `case_io.py check` schema OK, synonym guard OK, no failure names the case.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality 'MRI', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 30, ECOG 3 (fallback_tool_outputs.clinical_assessment). Why: rule 3: febrile (39.8 C), tachycardic (HR 124), hypotensive after a fluid bolus, with spreading purpura; the library's Karnofsky 100 describes a person without disease.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: slowed antalgic gait, no ataxia (followup_outputs[4] request_gait_and_balance_timed). Why: rule 3: the stored exam records a slow, hunched, antalgic gait; the library reports normal timed values.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no parkinsonian signs; neck stiffness noted; challenge not administered (followup_outputs[5] request_levodopa_challenge). Why: rule 3: the library reports a normal neck and gait in a patient with marked nuchal rigidity and an antalgic gait; no challenge would be given without parkinsonism.
- `perform_clinical_assessment {assessment_type: structured_headache_history_ichd3}`: new acute headache with red flags; criteria for a primary headache disorder not met (followup_outputs[6] request_structured_headache_history_ichd3). Why: rule 1 and 3: an acute febrile headache with neck stiffness and a spreading purpuric rash; the library elicits no red flags.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: supine BP 102/62, HR 124; standing not performed (followup_outputs[7] request_orthostatic_blood_pressure). Why: rule 3: vitals BP 102/62 and HR 124 after a fluid bolus in septic shock; the library reports HR 68 and 3 minutes of standing.
- `interpret_labs {panels: [ABG]}`: lactic metabolic acidosis with partial respiratory compensation (fallback_tool_outputs.labs['ABG']). Why: rule 3: stored bicarbonate 17, lactate 3.6, RR 22 and hypotension in septic shock; the library reports a normal gas.
- `interpret_labs {panels: [peripheral smear]}`: toxic granulation, thrombocytopenia, occasional schistocytes (fallback_tool_outputs.labs['peripheral smear']). Why: rule 3: stored platelets 94, fibrinogen 158, INR 1.4 and D-dimer 5.2 with a purpuric rash; the library reports a normal smear.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
