# ALZ-EARLY-P04
Reviewer status: R1 needs_changes, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| e54f2ddc-700b-4f4d-a1c3-e62f77e7afe8 | FIXED | `initial_tool_outputs.clinical_assessment.criteria_met.independence_in_instrumental_activities_lost` true; `scores["severity stage..."]` "mild dementia: instrumental independence lost"; findings add orientation, functional status (medical leave, grading errors, missed conferences despite written reminders) and informant history; impression rewritten per C3 (no storage-type or engineering sentence). Neuropsych impression (`followup_outputs[0].output.impression`) now ends "Multi-domain cognitive impairment with amnestic predominance, at a level consistent with mild dementia given the reported decline in work function" instead of "mild-to-moderate cognitive impairment". |
| 6b002573-69bc-4042-bddc-e5455869f817 | FIXED | "three-generation" corrected to two affected generations in `patient.history_present_illness`, `ground_truth.red_herrings[1]` (data_point and correct_interpretation), `key_clinical_evidence[0]`, `differential[2]`, `metadata.diagnostic_challenge`. The must keeps "construct a three-generation pedigree" (as the reviewer asks) and says the affected relatives span two generations. |
| 4cc451e4-5642-43ad-8184-10d0ec55ac3d | FIXED | `initial_tool_outputs.csf.special_tests`: Abeta40 9850 pg/mL added, Abeta42/40 ratio 0.040 (decreased; 390/9850), keys renamed to the vocabulary (`Abeta42`, `Abeta40`, `Abeta42_40_ratio`, `phospho_tau`, `total_tau`); p-tau181 reference made consistent with the other ALZ cases (<60 pg/mL; 78 stays elevated); interpretation rewritten as a pattern statement. |
| f42edd30-fee0-45ff-9d9f-b2565d1018bb | FIXED | Gene panel label and rationale (`action-7-order-specialized-test`) require pre-test counselling; soft constraint battery before genetics; canonical must "Offer genetic testing only with pre-test and post-test genetic counselling..."; disclosure must in a planned session with a genetic counsellor; prohibition on ordering or disclosing without counselling. The past-tense must "before disclosing PSEN1 result" is gone. |
| b971f1db-cfdf-456a-93ef-19b82817b6eb | FIXED | Must reframed (canonical C12.3): no predictive testing for the children aged 14 and 17; age-appropriate family counselling; predictive testing only for adults who request it. KCE[3] says the same. |
| fbc61064-dcf1-4c61-a09e-4fa1f2eb1024 | FIXED | `action-11-search-medical-literature` and its follow-up deleted; `fallback_tool_outputs.literature_search` null (C8). |
| bc07fb9e-17fc-4165-989a-fb546e1ab02c | FIXED | `initial_tool_outputs.mri.additional_observations[1]` "No mass lesion or pathological enhancement after gadolinium" became "No mass lesion". |
| af88df2d-b905-4179-a914-d29fc938bfaa | FIXED | ECG avoided action `avoid-waste-2-analyze-ecg` deleted; new optional `action-13-analyze-ecg` (baseline ECG before donepezil with escitalopram) with follow-up `order_baseline_ecg` (sinus rhythm 70, QT 396, QTc 428 ms Bazett, normal); the dementia must names the baseline ECG; drug check `action-12` made required with `{"drug": "donepezil"}` (C1.2). `fallback_tool_outputs.ecg` null (superseded). |
| 9ae6dd12-6f83-4a73-93bf-7f10e0bdb626 | FIXED | Summary comment (small inconsistencies): resolved by the notes above. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `followup_outputs` gene panel, `action-7.expected_evidence` | "PSEN1 c.869T>C (p.Leu290Pro)" names a residue that is serine in PSEN1 (codon 290 is the S290 of the exon 9 deletion), and "ClinVar ID: 1234" is a placeholder. | FIXED: a well-characterised pathogenic variant with onset in the 40s to 50s, PSEN1 c.737C>A (p.Ala246Glu), ACMG/AMP pathogenic, no database ID; same change in expected evidence. KCE no longer quotes the variant. |
| D | minor | gene panel `impression`, `recommended_actions` | "Genetic counseling is recommended..." is a referral in a laboratory report. | FIXED: removed (counselling is in the musts). |
| B | major | `action-10-analyze-csf` | "single optional biological-confirmation route"; an amyloid PET order got the library's negative PET (C2). | FIXED: two alternatives with canonical label, rationale, expected evidence; new follow-up `order_amyloid_pet` (18F-florbetaben, positive, Centiloid 96, diffuse cortical and striatal retention, typical of PSEN1 carriers). Probe of every alternative: CSF <- initial, PET <- `followup_outputs[1]`, gene panel <- [2], drug check <- [3], ECG <- [4]; no library answer. |
| C | minor | `followup_outputs[3]` drug check | Trigger "request_drug_interactions_cholinesterase_inhibitor"; content mostly right but not specific (no pulse, GI mechanism vague). | FIXED: trigger `check_drug_interactions_donepezil`; escitalopram additive QT with baseline ECG, ibuprofen GI risk, bradycardia with heart rate 70, GI titration, anticholinergic warning. |
| C | major | `ground_truth.differential` | bvFTD and primary psychiatric disorder left moderate after a work-up that returns valid-effort amnesia, MTA 2 atrophy, Alzheimer CSF and a PSEN1 variant (C11). | FIXED: both low with what excludes them; other entries reworded from case data. |
| C | major | `ground_truth.assessment` | Musts restated the labs, MRI and battery; "case-designated optional CSF biomarker route" (engineering); no cholinesterase-inhibitor must for mild dementia; anticholinergic prohibition in a patient taking none. | FIXED: musts are pedigree, genetic counselling, children, disclosure, canonical biomarker must, canonical dementia AChEI must with baseline ECG, driving, work, finances and planning, research registry and young-onset support. Prohibitions: psychiatric attribution, genetics without counselling, memantine at the mild stage. |
| B | minor | `initial_tool_outputs.labs` | "BMP" panel for a CMP order; interpretation text beyond a recital. | FIXED: CMP with total protein, albumin, ALT, AST, ALP, bilirubin added (normal); stored values unchanged; "All results are within reference ranges." |
| B | minor | `initial_tool_outputs.mri.impression` | Repeated sentence on posterior parietal prominence; unnumbered. | FIXED: numbered, same findings. Em dash in `volumetrics.hippocampal_volume` replaced in the rewritten value. |
| B | minor | `clinical_assessment.findings[0]` | Ended with ";" and omitted the 4-day date error from the exam. | FIXED. |
| C | minor | `ground_truth.key_clinical_evidence` | Six items, several restating the variant or the "case-designated" CSF route (C10). | FIXED: four items. |
| C | minor | `avoided_actions` rationales | Generic. | FIXED: one case-specific sentence each. |
| A | minor | criteria citations, rationales, order; `sequence_constraints`; `stop_rule` | Duplicate keys, rationale = label, no assessment-before-biomarker or battery-before-genetics constraint, `max_additional_actions` 0. | FIXED: one key each, case-specific rationales, order per plan 3.1 (assessment, battery, labs, MRI, biomarker, genetics, drug check, ECG), two soft constraints added, the existing MRI-before-CSF kept; stop rule adds the required drug check; `max_additional_actions` 1. |
| E | minor | `metadata.difficulty_rationale`, `key_educational_points` | Engineering wording on the "only biomarker route". | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The patient is now staged as mild dementia: she cannot do her job despite written reminders, and the clinical assessment and the neuropsychological impression say so. The family history is described as early-onset dementia across two generations (her mother, maternal uncle and aunt, then the patient), and a three-generation pedigree is still a must. The CSF now reports Abeta40 and a real Abeta42/40 ratio (0.040). The gene panel reports a real pathogenic variant, PSEN1 p.Ala246Glu, replacing a variant at a residue that is not leucine and a placeholder ClinVar ID. Amyloid status can be established by CSF or amyloid PET (optional, one test enough; a concordant positive PET was added). The literature step is gone and the MRI no longer mentions gadolinium. Genetic counselling is part of the testing pathway (label, constraint and musts), and the children aged 14 and 17 are offered age-appropriate counselling, not predictive testing. ECG is no longer called useless: the donepezil interaction check is required because of escitalopram, and a baseline ECG is an optional safety step (normal, QTc 428 ms) named in the cholinesterase-inhibitor must. bvFTD and a psychiatric cause are now low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: G30.0 grants "posterior cortical atrophy" and "benson syndrome" to this amnestic familial case (plan 5.1).
- Citation keys used: `[ACMG_NSGC_2011]`, `[NICE_NG97]` (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- None needing Andrea. Decided: the PSEN1 variant was replaced because the stored one cannot exist (reference residue mismatch); p.Ala246Glu was chosen because its reported onset (about 45 to 55) matches this family.

## Verification
Adversarial verifier, 24 Oct 2026. Checked every note row (e54f2ddc, 6b002573, 4cc451e4, f42edd30, b971f1db, fbc61064, bc07fb9e, af88df2d, 9ae6dd12): IADL field true and mild dementia wording in the assessment and neuropsych impressions; "two generations" in HPI, red herring, KCE, differential and metadata (the pedigree must keeps "three-generation pedigree", which is the correct term for the drawing); Abeta40 9850 with ratio 390/9850 = 0.040; counselling and children musts; no literature criterion or output; no gadolinium; ECG avoided action gone, optional ECG criterion with a normal follow-up (QTc 396/sqrt(0.857) = 428 ms at rate 70, matches the vitals), required donepezil check whose content (escitalopram QT, ibuprofen GI risk, pulse 70) is correct and differs from the expected evidence. Verified the variant: PSEN1 c.737C>A is p.Ala246Glu (A246E), a classic pathogenic variant with onset in the mid-40s to 50s, so the replacement fits the family. Both biomarker alternatives have case-authored outputs (CSF initial, amyloid PET follow-up).

Found and fixed:
- B, minor (introduced by the edit), `initial_tool_outputs.clinical_assessment.findings[2]`: "loses 3 points on recall (1/3 words at 5 minutes...)" is wrong arithmetic: recalling 1 of 3 words loses 2 points, and recall 2 + orientation 2 gave 26, not 25. Now "2 points on recall, 2 points on orientation and 1 point on serial sevens"; the MoCA already records serial subtraction errors. Same point added to `patient.neurological_exam.mental_status`, which listed only recall and orientation.
No other change. Both checks clean for the case; case guards pass.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'lasting power of attorney' (UK instrument) changed to 'durable power of attorney' in this US-setting case (1 place).
- MMSE item arithmetic: 2 orientation points were claimed for a single error (the date); now orientation 1 (date) and serial sevens 2 (two errors, consistent with the MoCA serial subtraction errors), still 25/30 (exam and findings[2]).
- MoCA 'clock 4/5' is not a MoCA score (the clock is out of 3); reworded to visuospatial/executive 4/5 with the imprecise cube copy, which keeps the MoCA total at 20/30 (exam and findings[1]).
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.
- Normal values in `Magnesium_homocysteine` varied (Magnesium 2.0 to 2.1, Homocysteine 10.2 to 8.4), all still within the case's reference ranges: the same numbers (magnesium 2.0, homocysteine 10.2, ESR 12, CRP 1.8) had been copied into up to 13 cases, a template artefact raised by the S01 worker; no text cites the changed values.
- Checks re-run after these additions: perfect_agent.py, case_io.py check and test_case_guards clean.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`--prune --conditions alzheimers_early`): removed "posterior cortical atrophy" and "benson syndrome"; code G30.1 (onset before 65); code G30.8 (atypical presentations only). Now: codes ['G30.0', 'G30.9', 'F00']; labels after accepted[0]: ['alzheimer disease', "alzheimer's disease", 'alzheimers disease', 'alzheimer dementia', 'dementia due to alzheimer', 'early onset alzheimer'].
- Added follow-up `order_advanced_imaging` FDG_PET (trigger `order_fdg_pet`, no criterion), after the amyloid-status follow-ups: a case-specific Alzheimer-type metabolic report concordant with the MRI and stage. Before, an FDG order returned the library's normal scan, contradicting the case (summary Q4). Probed: FDG and amyloid PET orders each return their own report, in either order.
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although this case contradicts it (diagnosis, history, medications or a stored finding) now get a case-specific report; every other off-pathway order still gets the library normal. No tier, criterion, diagnosis or existing output changed.

- `order_advanced_imaging modality=tau_PET` -> `followup_outputs[order_tau_pet]`: case-specific tau-positive flortaucipir PET with the distribution of the stored FDG-PET pattern.
- `order_advanced_imaging modality=perfusion_SPECT` -> `followup_outputs[order_perfusion_spect]`: regional hypoperfusion matching the stored FDG-PET hypometabolism.
- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: language findings of the stored neuropsychological battery (naming, fluency) in the speech-language format.
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[order_performance_status]`: dementia-stage performance status (Karnofsky 70/ECOG 1; 60/2 in the rapidly progressive case) instead of Karnofsky 100.

Checks: `perfect_agent.py` ok; `test_case_guards.py -k ALZ-EARLY` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
