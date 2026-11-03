# BACT-MEN-RM04
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 7fdda22c-2f7d-4caf-ae22-e4656a3e30b5 | FIXED | CRITICAL ACTIONS (imaging): of the reviewer's two options I took the guideline-literal one (plan 4.0, A): the false must "CT before LP is not mandated in this immunocompetent patient under 60 ..." is replaced by the canonical A must naming the bilateral eighth nerve deficit as a WHO 2025 Annex A.4 cranial nerve deficit (`assessment.required_recommendations[1]`); a matching prohibition (`prohibited_recommendations[1]`), a new required criterion `action-4-order-ct-scan` (`action_criteria[2]`), a HARD constraint CT before CSF with the canonical reason (NICE 1.4.7 agrees, new focal features) and a SOFT constraint blood cultures before CT were added; the CT id joins `stop_rule.required_before_assessment`. CSF PCR PANEL: the interpretive sentence is gone; the field reads "No panel target detected (targets: ...)" with the panel's target list (plan C7 canonical string), and the S. suis point stays in the musts and pearls. CRITICAL ACTIONS (dexamethasone): the must now starts dexamethasone with the first antibiotic dose and carries the reviewer's reassessment on identification of S. suis, with continuation for hearing protection framed as a deliberate trade-off citing Mai et al., NEJM 2007 (`required_recommendations[4]`, `key_clinical_evidence[4]`). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.csf`, `followup_outputs` | Index CSF was handed over upfront; the CSF culture "speciation" follow-up was a placeholder copy ("See initial CSF report") with an interpretation. | FIXED (C1): index CSF is the `request_lumbar_puncture` follow-up after the CT; the culture follow-up is now `request_csf_culture_final_report` holding only the final identification and MICs ("Final report at 48 hours"), with the non-applicable fields stated as such. `-v` confirms action-3 receives the index LP. |
| C | major | `assessment.required_recommendations` | Template empirical regimen ceftriaxone plus vancomycin, no Listeria cover despite diabetes. | FIXED (C4): canonical ceftriaxone must with vancomycin conditional, ampicillin 2 g IV every 4 hours for diabetes. Narrowing must adds stopping ampicillin and vancomycin. |
| C | minor | `assessment.required_recommendations` (audiology) | Audiology "after recovery" only. | FIXED (C8): canonical hearing must, plus early cochlear implant referral for profound bilateral loss because post-meningitic cochlear ossification can preclude implantation. |
| D | major | `action-4-search-medical-literature`, literature follow-up | Literature step expected IDSA 2004 and De Gans; output prescribed ceftriaxone plus vancomycin. | FIXED (C9): criterion and follow-up deleted. |
| B | minor | CSF report (`RBC`, `glucose_ratio`, `CSF_lactate`, `CSF_culture`, `interpretation`) | RBC "(normal)"; ratio "normal >0.6" with an em dash; lactate reference "normal <3.5"; interpretation concluded "consistent with acute bacterial infection" and explained the panel's limits. | FIXED (C7): canonical strings; culture "Pending; preliminary growth ... at 24 hours; identification and susceptibility to follow"; pattern-only interpretation. |
| B | minor | `followup_outputs[0].output` (blood cultures) | "No growth at 5 days" available at the work-up decision; two aerobic bottles and one anaerobic. | FIXED (C6): two sets, "No growth at 48 hours; final report at 5 days"; collection before antimicrobials kept true (betahistine only, no antibiotic before sampling). Red herring updated to match. |
| B | minor | `followup_outputs[1].output.impression` (CT) | "No contraindication to lumbar puncture identified on this study". | FIXED (C3): findings-only impression, mastoid pertinent negative kept. |
| B | minor | `followup_outputs[4]` (drug check) | Proposed the template ceftriaxone plus vancomycin; meropenem alternative for an allergy he does not have; formulary text restating the guideline regimen. | FIXED (C9): case regimen (ceftriaxone, ampicillin, dexamethasone, vancomycin conditional) against metformin and amlodipine; NKDA stated; formulary and alternatives emptied. Criterion stays recommended with case-specific label and expected evidence; trigger `check_drug_interactions_empirical_regimen`. |
| B | minor | `initial_tool_outputs.labs.panels.CBC`, `.interpretation` | Neutrophils 88.3 + bands 6 + lymphocytes 7.4 = 101.7%. | FIXED: lymphocytes 3.7% and monocytes 2.0% added (total 100%); interpretation updated. |
| B | minor | `initial_tool_outputs.labs` | Action-1 orders HIV; no HIV result. | FIXED (C12 labs): HIV-1/2 antigen/antibody non-reactive. Anion gap 13 checked. |
| C | major | `ground_truth.differential` | Labyrinthitis and S. pneumoniae left "high" after CSF culture identified S. suis; pneumococcal entry cited a latex test the case does not contain. | FIXED (C10): all alternatives low with the excluding result; Listeria meningitis added (risk factor present, excluded by Gram morphology, PCR and culture); streptococcal entry recoded G00.2 (streptococcal meningitis) instead of G00.8. |
| C | minor | `key_clinical_evidence[1]`, `[4]` | Hearing loss "approximately 50-66%" (overstated); dexamethasone pearl cited IDSA 2004 and De Gans for all adults. | FIXED: "about half of patients"; C5 sentence with the S. suis trade-off. Empirical-regimen pearl (C17) added. |
| B | minor | `ground_truth.red_herrings[0].field_path`, `[1]` | Labyrinthitis red herring pointed at `patient.clinical_history`; blood culture red herring at a non-existent `panels.Blood_Cultures`. | FIXED: `patient.history_present_illness` and `followup_outputs[0].output.findings`. |
| C | minor | `assessment.required_recommendations[5]` | "Elicit and document" the exposure that the history already gives. | FIXED: "Recognise the occupational swine contact ... as the key epidemiological clue". |
| A | minor | `action_criteria[*].citations`, `avoided_actions[*].citations` | Free-text duplicates and `[IDSA_2004]`, `[De_Gans_2002]`. | FIXED: `[WHO_Meningitis_2025]`. |
| B | minor | `metadata.difficulty_rationale` | Counted 4 required tools without the CT. | FIXED: lists labs, blood cultures, CT, CSF. |

## Changes, in one paragraph a physician can read before re-reviewing

The pathway is labs (HIV added, white-cell differential now sums to 100%), two sets of blood cultures (no growth at 48 hours), a required non-contrast CT before LP, the index lumbar puncture, the final CSF culture report at 48 hours (S. suis by MALDI-TOF, penicillin and ceftriaxone susceptible), then a recommended drug check. CT before LP is required because the bilateral eighth nerve deficit is a cranial nerve deficit under WHO 2025 Annex A.4 (NICE 1.4.7 agrees as a new focal feature); blood cultures and antibiotics come first. The CSF report gives values and pattern only; the PCR field reads "No panel target detected" with its target list, without the commentary. Musts: blood cultures; CT before LP with the WHO limb; ceftriaxone within 60 minutes with vancomycin conditional; ampicillin for Listeria because of diabetes; dexamethasone with the first dose, then reassessment once S. suis is identified, continuation for hearing being an explicit trade-off (Mai et al., NEJM 2007); recognition of the swine exposure and of hearing loss as an S. suis complication; PCR panels do not cover S. suis; narrowing to penicillin G or ceftriaxone; audiology within 4 weeks with early cochlear implant referral. The literature step is gone. The differential now ranks labyrinthitis, pneumococcal, other streptococcal, Listeria, viral and TB meningitis all low with the result that excludes each.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Diagnosis synonyms (plan section 5.5): `accepted` carries "listeria meningitis", "listeria monocytogenes meningitis" and "listeria meningoencephalitis" because `icd_codes[0]` is G00.8; an agent answering Listeria meningitis would score as correct in an S. suis case. Move the Listeria labels to A32.1, give G00.8 neutral labels, consider recoding this case to G00.2 (streptococcal meningitis), and strip the appended Listeria labels here (not hand-edited, per ruling 3).
- Citation keys `[WHO_Meningitis_2025]`, `[NICE_NG240]` for the criteria pack allow-list; a key for Mai NTH et al., N Engl J Med 2007;357:2431-2440 if the dexamethasone trade-off should be cited by key rather than in prose.

## Open questions for Andrea (judgment calls you could not settle)

- Plan Q4: I followed the plan (A, CT required on WHO's unqualified "cranial nerve deficits"). Reviewer 2 also accepted the other option, no CT with the stated reason that cochlear injury is not a sign of mass effect. If you choose that, delete `action-4-order-ct-scan`, both constraints, the CT prohibition and the A must, and use the reviewer's softened wording.
- Dexamethasone: I applied the reviewer's reassessment wording rather than the plan's "stop on identification of another organism", because for S. suis the Vietnamese trial gives a real reason to complete the course. A physician should check the citation sentence for the S. suis subgroup.
- The PCR field lists the panel's targets (plan C7 canonical) rather than the bare "No panel target detected" the reviewer proposed; a target list is what a real panel report shows and states no interpretation.

## Verification

Adversarial verifier, 23 October 2026. Read the log, the diff and the patient, follow-ups and ground truth.
Checked: note 7fdda22c applied in all three parts (A decision on the bilateral CN VIII deficit with the
false must gone, HARD constraint with the canonical reason and NICE 1.4.7 agreement, SOFT cultures-before-CT;
PCR field without interpretive commentary; dexamethasone reassessment on S. suis). The CN VIII deficit is
present at presentation (hearing loss from day 2), so the imaging-first limb holds. Pathway order labs,
blood cultures, CT, index LP, `request_csf_culture_final_report`, drug check; `-v` serves the index LP to
action-3. Cross-field: paired glucose 182 in labs and CSF, ratio 28/182 = 0.15; CBC differential 88.3 + 6 +
3.7 + 2.0 = 100%; CSF differential 100%; anion gap 13; CN VIII, GCS 13 (E3 V4 M6) and the HARD reason agree;
blood cultures `true` correct (betahistine only); Listeria must for diabetes per plan 4.0; differential all
low with excluding results.
Found and fixed: the dexamethasone must and `key_clinical_evidence[4]` said in one sentence "stop it once
another organism is identified" and then that completing the course for hearing is a legitimate trade-off,
so the must contradicted itself. Changed the clause to "for any other organism it can be stopped (WHO 2025;
NICE NG240 1.8.3)", which is WHO's permissive wording and the reviewer's, and keeps the reassessment and
trade-off sentence unchanged.
Left as logged: the Listeria labels in `accepted` (CENTRAL, synonym file) and plan Q4.
`perfect_agent.py -v` and `case_io.py check` clean after the edit.

## Condition audit (23 October 2026)
- Replaced `ground_truth.key_clinical_evidence[6]`, the template line "WHO 2025: obtain cultures promptly, but neither LP nor cranial imaging may delay empirical antimicrobials when the pathway requires treatment first.", with the plan C17 timing line "Antibiotics are given within 60 minutes of suspicion; neither imaging nor lumbar puncture may delay them (WHO 2025; NICE NG240 1.4.1)." (this case had no timing line otherwise). Same template line was removed from RM01, RM02, RM03 and RP01. `perfect_agent.py` and `case_io.py check` clean after the edit.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
G00.8 no longer appends Listeria labels to this S. suis case. Recoding to G00.2 (streptococcal meningitis) left for Andrea (Q8): no reviewer ruling.
- labels removed: "listeria meningitis", "listeria monocytogenes meningitis", "listeria meningoencephalitis"
- labels added: "other bacterial meningitis"
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (5 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients
- icd_codes[0] recoded G00.8 -> G00.2 (ICD-10-CM Streptococcal meningitis; S. suis is a streptococcus, organism code B95.4); synonyms re-derived (the 'other bacterial meningitis' label of G00.8 pruned; 'streptococcus suis meningitis' added via a case-scoped G00.2 entry)
- Dexamethasone trade-off also cites van Samkar et al., PLoS Negl Trop Dis 2015 (S. suis meningitis meta-analysis: dexamethasone associated with less hearing loss)

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

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 20, ECOG 4 (fallback_tool_outputs.clinical_assessment). Why: rule 3: drowsy (GCS 13), febrile (39.1 C), tachycardic, with bilateral deafness and severe imbalance; the library's Karnofsky 100 describes a person without disease.
- `perform_clinical_assessment {assessment_type: gait_and_balance_timed}`: broad-based ataxic gait, Romberg positive, tandem impossible; timed tests not completed (followup_outputs[5] request_gait_and_balance_timed). Why: rule 3: the stored exam records a broad-based staggering gait, positive Romberg and inability to tandem walk; the library reports normal timed gait and balance.
- `perform_clinical_assessment {assessment_type: levodopa_challenge}`: no parkinsonian signs; ataxic gait; challenge not administered (followup_outputs[6] request_levodopa_challenge). Why: rule 3: the library reports a normal gait and postural stability in a patient with a broad-based staggering gait and positive Romberg.
- `perform_clinical_assessment {assessment_type: structured_headache_history_ichd3}`: new acute headache with red flags; criteria for a primary headache disorder not met (followup_outputs[7] request_structured_headache_history_ichd3). Why: rule 1 and 3: an acute febrile headache with neck stiffness, deafness and drowsiness; the library elicits no red flags.
- `analyze_brain_mri`: leptomeningeal enhancement and bilateral labyrinthine enhancement; clear mastoids (fallback_tool_outputs.mri). Why: rule 1 and 3: no MRI is stored; bilateral sudden hearing loss and vertigo with meningism, and the stored CT shows clear mastoids.
- `analyze_eeg {eeg_type: continuous_icu}`: continuous generalised theta-delta slowing; no epileptiform discharges or seizures (followup_outputs[8] request_continuous_icu). Why: rule 3: the patient is drowsy and confused about the date (GCS 13); a normal awake background contradicts the stored exam.
- `analyze_eeg {eeg_type: ambulatory}`: continuous generalised theta-delta slowing; no epileptiform discharges or seizures (followup_outputs[9] request_ambulatory). Why: rule 3: the patient is drowsy and confused about the date (GCS 13); a normal awake background contradicts the stored exam.
- `perform_clinical_assessment {assessment_type: cognitive_screen}`: not completed (drowsy, severe hearing loss) (followup_outputs[10] request_cognitive_screen). Why: rule 3: the stored exam states he cannot cooperate with formal cognitive testing; the library reports MoCA 28/30.
- `order_specialized_test {test_type: neuropsych_battery}`: not completed (drowsy, severe hearing loss) (fallback_tool_outputs.specialized_test). Why: rule 3: the stored exam states he cannot cooperate with formal cognitive testing.
- `order_specialized_test {test_type: audiometry}`: bilateral severe-profound sensorineural hearing loss (followup_outputs[11] request_audiometry). Why: rule 3: the stored exam records no response to whispered or conversational voice in either ear with normal tympanic membranes; the library reports normal hearing.
- `order_specialized_test {test_type: baep}`: absent waves bilaterally (followup_outputs[12] request_baep). Why: rule 3: the stored exam records bilateral severe hearing loss; the library reports normal waves I, III and V.
- `perform_clinical_assessment {assessment_type: orthostatic_blood_pressure}`: supine BP 138/84, HR 108; standing not performed (followup_outputs[13] request_orthostatic_blood_pressure). Why: rule 3: HR 108 and severe imbalance; the library reports HR 68 and 3 minutes of standing without symptoms.
- `interpret_labs {panels: [HbA1c]}`: HbA1c 7.4% (fallback_tool_outputs.labs['HbA1c']). Why: rule 2: type 2 diabetes on metformin with a last HbA1c of 7.4% in the history.
- Case fallback replaced, `analyze_eeg {eeg_type: routine}`: routine EEG now shows continuous generalised theta-delta slowing; no epileptiform discharges or seizures (was a normal awake EEG) (fallback_tool_outputs.eeg). Why: rule 3: the patient is drowsy and confused about the date (GCS 13); a normal awake background contradicts the stored exam.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
