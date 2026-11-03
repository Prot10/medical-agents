# BACT-MEN-RP04
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 8f75c86a-41e8-45e9-a036-98ce1b1e9cf3 | FIXED (parts 2 to 4); BLOCKED (part 1, own step for beta-2 transferrin) | Part 1, beta-2 transferrin: removed from the CSF report (`special_tests.Beta_2_transferrin` and the interpretation sentence), so the pivot is no longer handed over and nothing is misfiled as a CSF test. It cannot get its own pathway step yet: no tool vocabulary term exists for a beta-2 transferrin assay on nasal secretion (`interpret_labs` has `beta2_microglobulin` only), and the plan forbids filing it under another assay. The must now reads "Send a nasal secretion sample for beta-2 transferrin ... usually a send-out assay reported within several days and does not delay treatment" (`assessment.required_recommendations[5]`); the differential no longer claims a positive result. BLOCKED on CENTRAL vocabulary. Part 2, imaging (plan C2, B): HARD constraint deleted; SOFT constraint blood cultures before CT added; CT criterion `action-5-order-ct-scan` stays required, relabelled "Non-contrast CT of the head with thin-section bone windows through the anterior skull base to identify the bony defect ...; it is not a prerequisite for lumbar puncture here (no WHO 2025 Annex A.4 criterion)", placed after the CSF; the IDSA must and prohibition replaced by the canonical B texts (`required_recommendations[3]`, `prohibited_recommendations[2]`). Part 3: index CSF moved from `initial_tool_outputs.csf` to `followup_outputs[1]` `request_lumbar_puncture` and the MRI to `followup_outputs[3]` `request_mri_brain_contrast`; `-v` confirms action-3 and action-4 receive them. Part 4: CBC differential now neutrophils 80%, bands 10%, lymphocytes 6%, monocytes 4% (new line, reference 2-10) = 100%; summary and interpretation updated. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.history_present_illness` | Timeline contradiction: chief complaint and HPI give an 18-hour history beginning "yesterday morning", but "He presented to the ED approximately 8 hours after symptom onset". | FIXED: "approximately 18 hours after symptom onset". |
| B | major | `patient.neurological_exam.mental_status` | "Alert" with E3 (eyes open to voice) and "disoriented to date" with V5 (oriented); GCS components contradict the narrative (plan C12). | FIXED: "GCS 14 (E4 V4 M6)"; total unchanged, so the imaging decision and the note's reference to GCS 14 hold. |
| B | major | `followup_outputs` (`search_recurrent_meningitis_workup`), `action-6-search-medical-literature` | Literature step recommended, expecting IDSA 2004 and De Gans, with an IDSA 2004 summary of vancomycin plus ceftriaxone and the "age >60" CT criteria (plan C9, ruling 5). | FIXED: criterion and follow-up deleted. |
| B | minor | `followup_outputs[1]` (index CSF) | Ratio "reference >0.6"; lactate reference "<2.1"; culture "preliminary identification in progress at 24 hours" in the report returned at the LP; glucose "critically low" (plan C1 item 5, C7). | FIXED: canonical ratio string (0.16, CSF 18 / blood 112, same paired glucose as the labs) and lactate string; culture "Pending"; pattern-only interpretation; PCR targets listed. RBC 8 cells/uL left as a number, without "traumatic". |
| B | major | `followup_outputs[0]` (blood cultures) | One set only, against the must's two sets; Gram stain null; em dashes in susceptibility keys; "Specimen taken before the first antimicrobial dose" phrasing; trigger `request_blood_cultures_result` (plan C6). | FIXED: set 1 positive at 24 hours, set 2 and the anaerobic bottle "No growth at 48 hours; final report at 5 days"; Gram stain; susceptibilities with CLSI meningitis wording at 48 hours; trigger `request_blood_cultures`. `collected_before_antimicrobials` stays true (no antibiotics in the week before), so action-2 keeps `before_antimicrobials: true`. |
| B | minor | `followup_outputs[3]` (MRI) | `recommended_actions` prescribed the skull-base CT (management in a report). | FIXED: emptied; impression keeps findings (meningoencephalocele is what MRI legitimately shows). |
| A | major | `ground_truth.action_criteria` | The immune work-up report existed with no criterion, so the stop rule penalised a standard investigation of recurrent pneumococcal meningitis (plan RP04 entry). | FIXED: `action-8-interpret-labs-immunoglobulins-complement` recommended, `interpret_labs {panels: [quantitative_Ig, complement]}`; follow-up trigger renamed `request_quantitative_ig_complement` so the order is served this report; interpretation reduced to values; the HIV screen moved from this report to `initial_tool_outputs.labs.panels.HIV`, where action-1 orders it. |
| B | minor | `initial_tool_outputs.labs` | Action-1 orders CMP and coagulation but no liver tests or coagulation results; interpretive labels "likely SIADH", "consistent with bacterial infection", "stress hyperglycemia" (plan C12 labs). | FIXED: ALT, AST, ALP, bilirubin, albumin and PT, INR, aPTT added within reference ranges; labels reduced to (low)/(elevated). Anion gap 12 checked. |
| C | major | `assessment.required_recommendations` | Template vancomycin plus ceftriaxone; dexamethasone 0.15 mg/kg without stop rule; IDSA CT must; no targeted therapy; no hearing must; meningococcal vaccine for a CSF leak (plan C4, C5, C8). | FIXED: canonical ceftriaxone must (no Listeria risk factor, plan 4.0); canonical dexamethasone must with "Continue for 4 days: Streptococcus pneumoniae is identified"; B must; narrowing must (ceftriaxone or benzylpenicillin, penicillin MIC 0.06, 14 days); hearing must. Vaccination must now pneumococcal conjugate vaccination only: a CSF leak is an indication for pneumococcal vaccine, not for meningococcal vaccine (meningococcal vaccination is for asplenia or complement deficiency, which the case excludes); `key_clinical_evidence` prevention line aligned. |
| C | major | `followup_outputs[5]` (drug check), `action-7-check-drug-interactions` | Proposed vancomycin, ceftriaxone, weight-based dexamethasone; ampicillin line "age <50 ... not required" (wrong threshold and wrong logic); formulary text citing IDSA; vaccination advice in a drug check; expected evidence generic (plan C9). | FIXED: checks the case regimen (ceftriaxone, dexamethasone 10 mg every 6 hours) against loratadine and mometasone, allergies and renal function; vancomycin line kept only as conditional; tier recommended (no concrete interaction). |
| C | minor | `ground_truth.differential` | CSF fistula key features relied on a beta-2 transferrin result the agent can no longer receive; immunoglobulin deficiency "moderate" after normal immunoglobulins (ruling 7). | FIXED: fistula features rest on CT, MRI, reservoir sign and the head injury, with beta-2 transferrin "when it returns"; immunoglobulin deficiency low with the excluding values. |
| D | minor | `ground_truth.red_herrings[2]` | Pointed at `initial_tool_outputs.mri` (now null). | FIXED: points at the skull-base CT sinus finding (`followup_outputs[2].output.findings[2]`); locations made readable. |
| A | minor | `action_criteria[*].citations`, `avoided_actions[*].citations`, `key_clinical_evidence` | `[IDSA_2004]`, `[De_Gans_2002]` and free-text duplicates; De Gans dexamethasone line; duplicate WHO timing line. | FIXED: `[WHO_Meningitis_2025]`; C5 dexamethasone sentence; C17 timing line; new line saying why the CT is not an LP prerequisite here. |
| B | minor | `metadata.difficulty_rationale` | "6 required tools", "literature" in the synthesis. | FIXED to the 5 required actions. |

## Changes, in one paragraph a physician can read before re-reviewing

The pathway is labs (now with liver tests, coagulation, HIV and a differential that sums to 100%), two sets of blood cultures, the index LP without prior imaging, a required non-contrast skull-base CT with bone windows to find the defect, contrast MRI of the meningoencephalocele, a recommended immunoglobulin and complement panel, and a recommended drug check. At 28 with GCS 14 (now E4 V4 M6, matching "alert, disoriented to date"), no focal signs, cranial nerve deficit, papilledema, seizure or immunocompromise, no WHO 2025 Annex A.4 criterion applies, so the HARD CT-before-LP constraint is gone and the CT is ordered for the skull base, after blood cultures. The CSF and MRI are no longer handed over upfront; beta-2 transferrin is removed from the CSF report and is now a must with a realistic turnaround, because no tool can order it yet. The literature step is gone. Musts: ceftriaxone within 60 minutes (vancomycin conditional), dexamethasone continued 4 days for pneumococcus, blood cultures, LP without CT, CSF panel, beta-2 transferrin on nasal secretion, skull-base CT, MRI and immune tests for the predisposing cause, narrowing to ceftriaxone or benzylpenicillin for 14 days, ENT and neurosurgical repair, pneumococcal vaccination (not meningococcal), droplet precautions, audiology. The HPI now says he presented 18 hours after onset, as the chief complaint states.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Vocabulary: a beta-2 transferrin assay on nasal (or ear) secretion (plan section 5.4, `interpret_labs` `beta2_transferrin`, with the `tool_io.py` mirror and a library normal "not detected"). When it exists, add a required criterion and a follow-up `request_beta2_transferrin` returning "Beta-2 transferrin detected in nasal secretion (send-out assay, reported at 3 days)" after the CSF, and change the must back to a pointer to that step.
- Citation keys `[WHO_Meningitis_2025]` and `[NICE_NG240]` for the criteria pack allow-list (plan 5.1), and a key for the recurrent-meningitis work-up (for example ter Horst L et al., Clin Infect Dis 2020, CSF leakage cohort), so `action-8-interpret-labs-immunoglobulins-complement` can cite a source; it has none now.

## Open questions for Andrea (judgment calls you could not settle)

- The trace pneumocephalus on the skull-base CT is reported after the LP in the new order (the CT is no longer a pre-LP study). A small CSF fistula does not contraindicate a diagnostic LP, and I did not make it one; say if you want the CT ordered before the LP for that reason instead.
- I removed the meningococcal vaccine from the vaccination must (CSF leak is a pneumococcal, not a meningococcal, vaccine indication). If you follow a national schedule that also offers MenACWY after any meningitis episode, restore it.

## Verification

Adversarial verifier, 23 October 2026. Read the log, the diff and the whole patient, follow-ups and ground truth.
Checked: note 8f75c86a part by part. Part 1 BLOCKED is sound: no vocabulary term for beta-2 transferrin
exists, the result is gone from the CSF report and interpretation, nothing claims a positive result, and the
must gives a realistic send-out turnaround. Parts 2 to 4 FIXED: B decision with the HARD constraint deleted,
SOFT cultures-before-CT present, CT relabelled for the defect and ordered after the CSF; CSF and MRI are
follow-ups served to action-3 and action-4 under `-v`; CBC differential 80 + 10 + 6 + 4 = 100% with a
monocyte line. The plan's recommended `quantitative_Ig` plus `complement` criterion exists and is served.
Cross-field: GCS 14 (E4 V4 M6) matches "alert, disoriented to date"; 18-hour history consistent across chief
complaint and HPI; paired glucose 112, ratio 18/112 = 0.16; anion gap 12; laterality (left nostril, left
cribriform defect, left sinuses, right sinuses clear) consistent across exam, CT and MRI; defect 3.8 mm on CT
and about 4 mm on MRI; immune panel normal and the differential says so; blood cultures `true` correct (no
antibiotics in the prior week); pneumococcal conjugate vaccination with the current ACIP options, meningococcal
vaccine correctly dropped.
Found: nothing requiring a change.
`perfect_agent.py -v` and `case_io.py check` clean.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (5 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients
- Immunoglobulin and complement criterion cites [Tebruegge_2008] (Tebruegge M, Curtis N, Clin Microbiol Rev 2008;21:519-537: 36% of recurrent bacterial meningitis is due to immunodeficiency, chiefly complement and antibody defects)

Re-run: `perfect_agent.py` ok; `case_io.py check` clean for the case; BACT-MEN case guards pass; synonym `--check` clean.

## Central vocabulary wired (24 Oct 2026)
- Note 8f75c86a part 1, BLOCKED -> FIXED with the new core term `interpret_labs` `beta2_transferrin`: new required criterion `action-9-interpret-labs-beta2-transferrin` (`panels: [beta2_transferrin]`), placed after the contrast MRI and before the immunoglobulins; follow-up `request_beta2_transferrin` (`followup_outputs[4]`, after the MRI): "Beta-2 transferrin, nasal secretion (left), immunofixation: Detected", send-out, reported at 3 days; added to `stop_rule.required_before_assessment`.
- `required_recommendations[5]` no longer stands in for the order: "Confirm the CSF leak with beta-2 transferrin on the left nasal secretion, collected while the rhinorrhea is active; it is a send-out assay reported in about 3 days, so antibiotics, dexamethasone and the skull-base imaging proceed without waiting for it."
- `differential[0].key_features`: "beta-2 transferrin detected in the left nasal secretion confirms that the rhinorrhea is CSF" (was "confirms CSF when it returns"). `metadata.difficulty_rationale`: 6 required actions.
- Re-run: `perfect_agent.py -v` ok; `case_io.py check`: schema OK, synonym guard OK, no test failure names the case.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality 'MRI', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg` set to null: it describes no single recording, so it cannot be typed; an off-pathway EEG order now gets the library normal of the type ordered.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 30, ECOG 4 (fallback_tool_outputs.clinical_assessment). Why: rule 3: febrile (39.1 C), tachycardic (HR 108), disoriented to date with marked meningism, refusing to stand; the library's Karnofsky 100 describes a person without disease.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: not performed (refuses to stand: headache, photophobia) (followup_outputs[7] request_gait_and_balance_timed). Why: rule 3: the stored exam records gait not assessed because the patient refuses to stand.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable (followup_outputs[8] request_levodopa_challenge). Why: rule 3: the library describes a normal gait and postural reflexes in a patient who refuses to stand, with marked nuchal rigidity.
- `perform_clinical_assessment {assessment_type: structured_headache_history_ichd3}`: new acute headache with red flags; criteria for a primary headache disorder not met (followup_outputs[9] request_structured_headache_history_ichd3). Why: rule 1 and 3: an acute febrile headache with neck stiffness and photophobia, the second such episode; the library elicits no red flags.
- `analyze_eeg {eeg_type: routine}`: mild generalised theta slowing; no epileptiform discharges or seizures (fallback_tool_outputs.eeg). Why: rule 3: no EEG is stored and the patient is disoriented to date with impaired concentration (GCS 14); the library reports a normal background.
- `analyze_eeg {eeg_type: sleep_deprived}`: mild generalised theta slowing; no epileptiform discharges or seizures (followup_outputs[10] request_sleep_deprived). Why: rule 3: disoriented to date with impaired concentration (GCS 14); the library reports a normal background.
- `analyze_eeg {eeg_type: continuous_icu}`: mild generalised theta slowing; no epileptiform discharges or seizures (followup_outputs[11] request_continuous_icu). Why: rule 3: disoriented to date with impaired concentration (GCS 14); the library reports a normal background.
- `analyze_eeg {eeg_type: ambulatory}`: mild generalised theta slowing; no epileptiform discharges or seizures (followup_outputs[12] request_ambulatory). Why: rule 3: disoriented to date with impaired concentration (GCS 14); the library reports a normal background.
- `perform_clinical_assessment {assessment_type: cognitive_screen}`: MoCA 18/30 with inattention and temporal disorientation (followup_outputs[13] request_cognitive_screen). Why: rule 3: the stored exam records disorientation to date and serial subtraction lost after two steps; the library reports MoCA 28/30.
- `order_specialized_test {test_type: neuropsych_battery}`: not completed (inattention, acute confusion) (fallback_tool_outputs.specialized_test). Why: rule 3: an acutely confused patient cannot complete a battery in the average range.
- `order_microbiology {specimen: whole_blood_pcr}`: Streptococcus pneumoniae DNA detected (fallback_tool_outputs.microbiology). Why: rule 3: blood cultures grow S. pneumoniae in 1 of 2 sets, a target of the panel; no antibiotics in the week before presentation.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: supine BP 122/74, HR 108; standing not performed (followup_outputs[14] request_orthostatic_blood_pressure). Why: rule 3: vitals HR 108 in a patient who refuses to stand; the library reports HR 68 and 3 minutes of standing.
- `interpret_labs {panels: [serum_osmolality]}`: serum osmolality 267 mOsm/kg (low) (fallback_tool_outputs.labs['serum_osmolality']). Why: rule 3: stored sodium 128 mmol/L (calculated osmolality about 268); the library reports 288 mOsm/kg.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
