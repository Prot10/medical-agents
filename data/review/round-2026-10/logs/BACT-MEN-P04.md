# BACT-MEN-P04
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| deec2d03-a0be-4278-be8a-4ae8b2df98e8 | FIXED | Culture timing: the index CSF (moved from `initial_tool_outputs.csf` to `followup_outputs[1]` `request_lumbar_puncture`) now reads "Bacterial_culture: Pending"; the CSF culture result is a separate later step, `followup_outputs[2]` `request_csf_culture_final_report`: "No growth at 48 hours; final report at 5 days". Blood cultures moved to `followup_outputs[0]` `request_blood_cultures`: "No growth at 48 hours; final report at 5 days" for both sets (2 of 2 sets, 4 bottles), `collected_before_antimicrobials` false with the amoxicillin course stated (C6). Red herring 1 rewritten to the 48-hour culture result. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | ground_truth (CT criterion, constraint, must, prohibition) | CT required with a HARD constraint on "altered mental status" (IDSA 2004); GCS 14, no focal sign, no cranial nerve deficit, no papilledema, no seizure, immunocompetent: no WHO 2025 Annex A.4 or NICE 1.4.7 criterion | FIXED: HARD constraint deleted; CT kept as `recommended` for the sinus source (plan class B, see Open questions), placed after the LP, with the canonical B label; SOFT blood cultures before CT; canonical B must and prohibition replace the IDSA ones; CT removed from the stop rule |
| D | major | followup_outputs[request_ct_head].output.impression | "No contraindication to lumbar puncture on imaging"; sinus disease called "incidental" | FIXED: numbered findings only; sinus disease described without a judgement (C3) |
| B | major | initial_tool_outputs.csf | Pneumococcal urinary antigen filed inside the CSF report and used as confirmation; lactate reference <2.1; ratio reference ">0.6"; ratio 0.42 while musts and key evidence rest on "<0.4"; culture "No growth at 5 days" same day; interpretation concluded "discordance" | FIXED: urinary antigen removed (not a CSF test, not orderable, not a WHO 2025 confirmatory test); CSF glucose 38 changed to 34 mg/dL so the ratio is 0.37 (0.4 or less, as the case's teaching assumes); canonical ratio, RBC, lactate strings; culture pending; panel string lists its targets; interpretation states values and results only (C7) |
| B | minor | initial_tool_outputs.labs | action-1 orders HIV and CMP but no HIV result and no liver tests; interpretation ended in a fragment "all bottles)." | FIXED: HIV-1/2 Ag/Ab non-reactive; AST, ALT, ALP, bilirubin, albumin normal; interpretation cleaned (C12 labs) |
| C | major | ground_truth.assessment.required_recommendations | Template vancomycin plus ceftriaxone; dexamethasone without a stop rule; urinary antigen as a confirmatory test; "CT before LP given altered mental status"; duplicate "do not" line among the musts; no hearing must | FIXED: canonical base regimen (no Listeria risk factor, age 33), canonical dexamethasone with "Continue for 4 days: S. pneumoniae is identified", PCR as the organism test, biochemistry must with the WHO thresholds, B must, ceftriaxone as definitive agent (no isolate), stop ibuprofen, ENT for the sinus source, hearing must; duplicate removed |
| C | minor | followup_outputs[check_drug_interactions_empiric_regimen] | Vancomycin-based regimen, rifampicin adjunct, "age <50" Listeria threshold, interpretive amoxicillin paragraph; missed the real NSAID plus corticosteroid interaction | FIXED: checks ceftriaxone with dexamethasone against ibuprofen (stop, bleeding risk), amoxicillin, loratadine; Listeria threshold over 60; criterion label and expected evidence match; tier stays recommended (plan 4.0) |
| C | major | ground_truth.differential | Viral meningitis left "high" and TB "moderate" after S. pneumoniae on PCR; TB key features cited "negative TB/AFB studies" the case does not contain; NSAID meningitis described as lymphocytic with normal protein | FIXED: viral low, TB, HSV, cryptococcal and NSAID very low with the excluding results; NSAID meningitis described as neutrophilic with a normal glucose ratio (C10) |
| D | minor | ground_truth.key_clinical_evidence | Urinary antigen line; "<0.4" and WHO template lines | FIXED: antigen line deleted; C17 canonical ratio and antibiotic-timing lines; B must sentence added |
| A | minor | citations | `[IDSA_2004]`, `[De_Gans_2002]` and free-text duplicates on criteria, avoided actions and constraint | FIXED: `[WHO_Meningitis_2025]` |
| B | minor | ground_truth.action_criteria[action-5-search-medical-literature], followup_outputs[search_partially_treated_meningitis_pcr] | Literature criterion recommended, expected text IDSA 2004 and ESCMID 2016 | FIXED: deleted (plan C9, ruling 5) |
| E | minor | metadata.clinical_notes, difficulty_rationale, teaching_points[1] | Ratio 0.42, antigen as confirmation, "5 required tools" | FIXED |

## Changes, in one paragraph a physician can read before re-reviewing

Only the blood panel is given upfront (now with HIV non-reactive and normal liver tests). The pathway
is blood cultures (no growth at 48 hours after 3.5 days of amoxicillin, final at 5 days), the index LP
(310 cells, 54% neutrophils, protein 148, ratio 0.37 after correcting CSF glucose to 34, lactate 4.6,
Gram stain negative, multiplex PCR S. pneumoniae, culture pending), a later CSF culture report (no growth
at 48 hours), a non-contrast CT for the sinus source, and the drug check. CT is no longer required before
the LP: GCS 14 with confusion is not a WHO 2025 or NICE imaging criterion. The pneumococcal urinary
antigen has been removed from the CSF report; PCR identifies the organism. Musts are ceftriaxone within
60 minutes (vancomycin only for local resistance), dexamethasone continued 4 days for S. pneumoniae,
the partially treated reasoning, stopping ibuprofen, ENT for the sinus source and audiology. The
differential is the post-CSF view, and the literature step is gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- None specific to this case. (Pneumococcal urinary antigen is not orderable; it was removed rather than requested, since WHO 2025 does not recommend antigen detection.)

## Open questions for Andrea (judgment calls you could not settle)

- Plan 4.0 marks P04 as imaging class C (no CT). I kept the CT as `recommended` (class B, sinus source, after the LP), as the plan does for S01 and S02: purulent maxillary and ethmoid sinusitis preceded the meningitis, the stored CT shows it, and identifying a parameningeal focus that may need ENT drainage is a real indication. If the lead prefers C, delete `action-4-order-ct-scan`, the soft constraint, the CT follow-up and the ENT must, and add the CT waste item.
- CSF glucose changed from 38 to 34 mg/dL (ratio 0.42 to 0.37) so the case's own teaching (ratio of 0.4 or less) holds under the WHO 2025 reference; the alternative is to keep 0.42 and rewrite the musts around "below the normal 0.5".

## Verification

Adversarial verifier, 23 October 2026. Checked: note deec2d03 against the final file (index CSF culture "Pending"; the 48-hour CSF culture result is a separate later `analyze_csf` follow-up; blood cultures "No growth at 48 hours; final report at 5 days" with `collected_before_antimicrobials: false` and the amoxicillin course; red herring 1 points at the 48-hour culture, path resolves); the CSF glucose change 38 to 34 mg/dL is carried everywhere (ratio 34/91 = 0.37 in the report, interpretation, differential, musts, `metadata.clinical_notes`; no "38 mg/dL" or "0.42" left); anion gap 133 - 100 - 22 = 11; no HARD constraint and CT out of the stop rule; B must and prohibition agree; dexamethasone continued 4 days for S. pneumoniae; differential post-CSF.

Deviation reviewed: plan 4.0 marks P04 as C (no CT); the worker kept the CT as recommended class B for the purulent maxillary and ethmoid sinusitis that preceded the meningitis, as the plan does for S01 and S02. That is a real parameningeal-source indication documented in the HPI and the CT, and the CT is no longer a prerequisite for LP, so I accept it; it stays an open question for the lead.

Found and changed:
- The drug-interaction output (`followup_outputs[4].output.warnings[2]`, `[3]`) gave regimen-selection reasoning, not interactions ("No Listeria risk factor recorded ...: ampicillin is not required"; a restatement of the WHO vancomycin rule), and warning [2] echoed the criterion's expected evidence (the scoring-key leak PATTERNS 1 names). Replaced both with the category-level line used across the condition: "Vancomycin, if used: dose by weight with AUC or trough monitoring and monitor renal function."; removed "; no Listeria risk factor, so no ampicillin" from `action-6-check-drug-interactions.expected_evidence`. The no-ampicillin decision stays in the musts (base regimen) and key evidence.

After the edits: `perfect_agent.py BACT-MEN-P04 -v` passes (action-3 <- `request_lumbar_puncture`); `case_io.py check` clean for the case.

## Condition audit (23 October 2026)
- Changed `ground_truth.action_criteria[action-2-order-microbiology].alternatives[0].required_arguments`: removed `before_antimicrobials: true` (specimen and tests kept). Reason: the blood culture report sets `collected_before_antimicrobials: false` because an antimicrobial was taken in the 7 days before collection, so `true` is not the truthful value of the parameter ("whether the specimen is being taken before the first antimicrobial dose") and an agent that orders the cultures truthfully would miss a required criterion. Condition-wide rule settled at the audit: the argument is required only where the report flag is true (16 cases) and absent where it is false (14 cases: M01, M02, M03, M05, P02, P04, RM01, RM03, RP01, RP02, RP03, RP05, RS04, S03). Draw-before-treatment timing stays in the musts and in the SOFT blood-cultures-before-CT constraint where one exists. `perfect_agent.py` and `case_io.py check` clean after the edit.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (5 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients
- Leak fix: the drug-check summary no longer repeats the criterion's expected evidence; rewritten in report voice with the same content

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
