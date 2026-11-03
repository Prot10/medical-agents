# NMDAR-ENC-P03
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for NMDAR-ENC) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: condition not reviewed | - | - |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A | blocker | `action-2-analyze-csf`, `action-8-check-drug-interactions`, `action-7-search-medical-literature`, `action-1-analyze-brain-mri`, `action-4-interpret-labs` | Non-schema keys (`basic`, `screen_for`), exact literature `query`, `protocol: standard`, 11-panel list: unreachable for a schema-conformant agent (C1). | FIXED: plan 3.2 minimal arguments (labs A/B; MRI `{contrast: true}`; CSF HSV_PCR + NMDAR_antibodies + OCB or IgG_index; EEG routine/video/continuous_icu; `{study: testicular_ultrasound}`; DDI and literature `{}`). |
| B | blocker | `initial_tool_outputs.csf.special_tests` | Antibody both "Sent, results pending" and "Positive" without titre (C4). | FIXED: `NMDAR_antibodies` = "Positive, titre 1:256 (cell-based assay, IgG anti-GluN1; reference laboratory, resulted day 4)"; pending key deleted; once in `interpretation`. HSV-1 PCR "NEGATIVE" normalised to "Negative"; RBC "2 cells/uL (likely traumatic)" to "2 cells/uL". |
| B | blocker | `initial_tool_outputs.labs.panels` | CSF titre in the labs, including inside the panel named "Serum anti-GluN1 cell-based assay" (C4). | FIXED: CSF entries deleted; serum positive 1:64 in `Serum anti-GluN1 IgG (cell-based assay)`. |
| D | major | `initial_tool_outputs.labs.panels` | "Exclusion studies" (HIV, paraneoplastic) with leaky text, duplicate inflammatory panel, TSH under "Other", no free T4, no toxicology ethanol (C5). | FIXED: rebuilt to plan panels: CBC, BMP, coagulation, inflammatory markers, thyroid function (TSH 1.9, free T4 1.2 ng/dL), thyroid antibodies, serum anti-GluN1, neuronal-surface panel, onconeural panel, infection serology (HIV), toxicology (UDS, ethanol undetectable), other (CK, ammonia, B12, levetiracetam level). Plain recital; `clinical_significance` null. |
| A/C | major | `followup_outputs` `request_ct_cap` | CAP CT plus scrotal ultrasound under `order_ct_scan` (head tool), `contrast_used: false`; not indicated after a normal testicular US in a 28-year-old with post-HSV disease (C11, plan P03). | FIXED: deleted. |
| B | major | `followup_outputs` `request_comparison_mri` | A second MRI report repeating the comparison the initial MRI already makes, with "NO restricted diffusion (not HSV)" essays (plan P03). | FIXED: deleted; the comparison with the outside MRI of 6 weeks ago now sits in the initial MRI's `additional_observations`. |
| D | major | `initial_tool_outputs.mri` | Differential parentheticals inside findings and observations ("argues against HSV relapse, which typically shows DWI restriction", "HSV relapse often shows hemorrhage", "consistent with active inflammatory/autoimmune process"); capitalised prose impression (style guide, C13). | FIXED: findings keep their substance without the rebuttals; numbered impression (new bilateral medial temporal FLAIR signal beyond the chronic change, no restricted diffusion, hemorrhage or enhancement; chronic left encephalomalacia) with one hedged HSV sentence. |
| B | major | `initial_tool_outputs.eeg.impression` | Omitted the extreme delta brush (impression without its own key finding); "(consistent with prior HSV damage)" in background. | FIXED: "This is an ABNORMAL EEG due to:" numbered (EDB, three temporal seizures two right and one left, disorganized slow background); parenthetical removed. |
| D | major | cEEG follow-up `request_continuous_eeg` | Impression "confirming that the seizures are from a new process" and "contralateral to the prior HSV damage" (kind 1, C7). | FIXED: template impression (background, eight temporal seizures five right three left, four with and four without clinical correlate, EDB); a diffuse slowing finding added for consistency with the background; em dashes removed. |
| D | major | `initial_tool_outputs.literature_search` | Placeholder repeating expected_evidence (C3). | FIXED: canonical output plus Armangue 2018 and Schmitt 2012. |
| D/C | major | `initial_tool_outputs.drug_interactions` | Empty interactions, summary repeating expected_evidence (C3, C10). | FIXED: report voice from the real list: valacyclovir duplicates IV aciclovir (stop it), levetiracetam no relevant interaction, aciclovir/IVIG/steroid/lorazepam cautions, D2 class warning, aspirin urticaria and NSAID cross-reactivity, HBV before rituximab. |
| C | major | `action-7-search-medical-literature`, `action-8-check-drug-interactions` | Both recommended (rulings 5, 6). | FIXED: optional, `{}`, last. DDI optional because the valacyclovir switch and levetiracetam dose review are made in the musts. |
| C | major | `fallback_tool_outputs.advanced_imaging`, `.specialized_test` | Catch-all FDG-PET and neuropsychology fallbacks (C14). | FIXED: null; `metadata.fallback_tool_kinds` entries removed. |
| B | major | `fallback_tool_outputs.cardiac_monitoring` | Normal Holter (average 76) against HR 78-118 with labile BP (C14). | FIXED: telemetry, sinus tachycardia episodes to 118 bpm (range 76-118, average 98). `proposed` of the fallback DDI set to "". |
| D | minor | `initial_tool_outputs.ecg.interpretation` | "likely from autonomic instability and agitation" (C13). | FIXED: rate, axis, intervals only. |
| D | minor | `initial_tool_outputs.body_imaging` | Terse findings; impression said "no germ-cell tumour" (C12). | FIXED: both testes and epididymes described; "Normal scrotal ultrasound. No testicular mass." |
| C | major | `assessment.required_recommendations` | Template musts: send paired CSF/serum, aciclovir "until PCR negative" without the post-HSV framing while valacyclovir is on the list, testicular US + CAP CT, "levetiracetam or valproate" in a patient already seizing on levetiracetam, ICU and central hypoventilation the case does not have, urology/oncology consults (C9). | FIXED: M1 post-HSV (IV aciclovir in place of valacyclovir until PCR excludes relapse), M2, M3 male-negative, M4 case-specific (increase levetiracetam 500 mg twice daily or add lacosamide), M5, M6 ward (GCS 13, HR to 118, no hypoventilation or status: the plan rule gives ward), M7, M8 lorazepam for agitation and catatonic posturing, M10 neurology with psychiatry. |
| C/E | minor | `assessment.prohibited_recommendations` | "in a young patient" in P3; dashes (C9). | FIXED: canonical P1-P5. |
| C | major | `ground_truth.differential` | HSV `high`, other AE and psychiatric `moderate` after negative PCR and panels; HSV relapse, the case's own mimic, not named (C8). | FIXED: "HSV-1 encephalitis relapse" low with PCR/MRI/movement evidence; other AE, psychiatric and drug entries low with this case's data; levetiracetam behavioural effects named in the drug entry. |
| C | major | `ground_truth.key_clinical_evidence` | Template with wrong claims (C15). | FIXED: six bullets, including Armangue 2018 and the non-tumour association. |
| B | major | `ground_truth.red_herrings[0]` | "Viral prodrome (URI, fever, cough)": the HPI has no prodrome (C15). | FIXED: replaced by the case's real distractor, the recent HSV encephalitis and the team's relapse hypothesis, with the Armangue 2018 interpretation. |
| C | minor | `ground_truth.red_herrings[1]`, `[2]` | Template interpretations (C15). | FIXED: canonical hyponatraemia (133, mild) and CK text. |
| C | minor | criteria `rationale`, `citations`, `expected_evidence` | Rationale = label; free-text citation twins; generic evidence (C16). | FIXED: case-anchored rationale and evidence; bracketed keys only. |
| A | minor | criteria order, `sequence_constraints`, `stop_rule` | C6, C18. | FIXED: order labs, MRI, CSF, EEG, testicular US, cEEG, DDI, literature; soft MRI-before-CSF; stop rule five required ids, max 2. |
| C | minor | `metadata.clinical_pearls` | "20-30%", "extreme delta brush pathognomonic ... never seen in HSV", unsupported relapse claim. | FIXED: Armangue 2018 figures; non-tumour association; no pathognomonic claim. |
| E | minor | whole case | The case is written in American spelling; the plan's canonical texts are British. | FIXED: all new text follows the case (acyclovir, tumor, hemorrhage, titer, behavioral); the diagnosis label and synonyms untouched. |

## Changes, in one paragraph a physician can read before re-reviewing
NMDAR-ENC-P03 (28-year-old man, 6 weeks after HSV-1 encephalitis) now reports the CSF anti-GluN1 result once, in the CSF report (positive 1:256, HSV PCR negative). The serum result (1:64) is the only antibody entry in the labs. The two follow-ups that did not belong were deleted: a CAP CT filed under the head CT tool and a duplicate comparison MRI. The single MRI report now makes the comparison with the outside study, without differential essays. The routine EEG impression names the extreme delta brush it had omitted. The continuous EEG no longer concludes that "the seizures are from a new process". Literature and drug interactions are optional and report-voice. The drug-interaction output flags that valacyclovir duplicates IV aciclovir. The musts restart IV aciclovir in place of valacyclovir only until the PCR excludes relapse, give first-line immunotherapy, take the levetiracetam dose up (or add lacosamide) because seizures continue on 500 mg twice daily, use lorazepam for agitation and catatonia, and admit to a neurology ward with cardiac monitoring and continuous EEG. HSV relapse is in the differential as low. The prodrome red herring, which the HPI did not support, is replaced by the HSV-relapse distractor.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys used and not yet in the allow-list: `[Armangue_2018]`, `[Gresa-Arribas_2014]`, `[Herman_2015]`, `[Venkatesan_2013]` (plan CENTRAL 1).

## Open questions for Andrea (judgment calls you could not settle)
None. Level of care follows the plan's M6 rule (ward). The case has frequent seizures, a GCS of 13 and labile blood pressure, but none of the ICU triggers.

## Verification
Adversarial verifier, 24 Oct 2026. Checked against the plan (sections 1-4 and the per-case bullet) and ROUND_POLICY: every own-finding row against the file; criterion tiers, minimal arguments, order and ids; soft MRI-before-CSF constraint and stop rule (five required ids, max 2); CSF report carries the only CSF titre and the labs only the serum titre; musts against allergies, medications and level-of-care rule; prohibitions P1-P5; differential and key evidence against the final reports; red-herring field paths; fallbacks; a word-level diff of every changed string against HEAD (to catch accidental edits in correct prose); citation format and new-text dashes. No reviewer notes exist for NMDAR-ENC, so the notes table is complete. `perfect_agent.py -v` passes and `case_io.py check` reports no failure naming the case (case guards included).

Found and changed:
- `metadata.diagnostic_challenge`: the same spelling-pass corruption ("characteriztic"). FIXED: "characteristic".
- `ground_truth.differential[1]`: the worker added GABA-A to the diagnosis name (correct for post-HSV autoimmune encephalitis, Armangue 2018) but the labs never tested it and the key features omitted it. FIXED: `Anti-GABA-A receptor IgG: Negative` added to `labs.panels["Autoimmune encephalitis antibodies (serum)"]` and GABA-A added to the key features.
- `metadata.fallback_tool_kinds.cardiac_monitoring` "normal" against the tachycardic telemetry. FIXED: "sinus_tachycardia".
- Confirmed: post-HSV M1 replacing valacyclovir, DDI duplicate-prodrug content, aspirin-urticaria NSAID cross-reactivity, deletion of the CAP CT and comparison-MRI follow-ups, cEEG laterality consistent with the routine EEG. Ward level of care follows the plan's M6 rule (no ICU trigger) and is logged by the worker; accepted.

## Close-out (24 Oct 2026)

- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions autoimmune_encephalitis_nmdar`): the generic G04.81 labels "autoimmune encephalitis", "antibody mediated encephalitis" and "autoimmune limbic encephalitis" and code G04.90 are no longer accepted, because every token of the first two occurs in "anti-LGI1 autoimmune encephalitis" or "seronegative autoimmune encephalitis" (alternatives the work-up excludes), limbic encephalitis is a different syndrome (Graus 2016) and G04.90 is unspecified encephalitis. Added "glun1 encephalitis", "nr1 encephalitis" and code G04.8. `accepted[0]` and `icd_codes[0]` unchanged. Decisions: `plans/NMDAR-ENC-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although this case contradicts it (diagnosis, history, medications or a stored finding) now get a case-specific report; every other off-pathway order still gets the library normal. No tier, criterion, diagnosis or existing output changed.

- `order_advanced_imaging modality=FDG_PET` -> `followup_outputs[order_fdg_pet]`: brain FDG-PET: frontotemporal hypermetabolism with parieto-occipital hypometabolism, distributed as the stored MRI and EEG.
- `analyze_eeg eeg_type=ambulatory` -> `followup_outputs[order_ambulatory]`: ambulatory EEG mirroring the stored continuous EEG (no video).
- `perform_clinical_assessment assessment_type=cognitive_screen` -> `followup_outputs[order_cognitive_screen]`: baseline cognitive screen as documented in the mental status examination.
- `perform_clinical_assessment assessment_type=cognitive_screen timing=post_intervention` -> `followup_outputs[order_cognitive_screen_post_intervention]`: repeat screen during the admission: persisting impairment.
- `order_specialized_test test_type=neuropsych_battery` -> `followup_outputs[order_neuropsych_battery]`: neuropsychological battery not completable or impaired in the acute encephalopathy.
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[order_performance_status]`: performance status KPS 40, ECOG 3 for the documented dependency.
- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `followup_outputs[order_gait_and_balance_timed]`: timed gait not testable or impaired, as on the examination.
- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: speech and language evaluation reflecting the documented speech disturbance.
- `order_ct_scan` -> `fallback_tool_outputs.ct`: head CT shows the chronic lesion on the stored MRI.
- `order_advanced_imaging modality=MR_spectroscopy` -> `followup_outputs[order_mr_spectroscopy]`: MR spectroscopy abnormal in the encephalomalacic tissue on the stored MRI.
- `order_advanced_imaging modality=perfusion_MRI` -> `followup_outputs[order_perfusion_mri]`: perfusion MRI abnormal in the encephalomalacic tissue on the stored MRI.
- `labs:valproate_level` -> fallback labs panel `Antiseizure medication levels`: antiseizure drug levels: none detected (no antiseizure drug prescribed).

Checks: `perfect_agent.py` ok; `test_case_guards.py -k NMDAR-ENC` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
