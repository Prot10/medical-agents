# NMDAR-ENC-S01

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-6-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: split initial_tool_outputs.mri (gadolinium study). The gadolinium study, text unchanged, is now followup_outputs[0] (analyze_brain_mri, trigger request_contrast_mri, contrast_used true), first in the pathway as the core diagnostic MRI; the plain copy (contrast_used false) keeps the initial slot: removed the post_contrast key of the medial temporal finding and 'enhancement' from impression item 1 (now 'without restricted diffusion or mass effect'). Pre-contrast sequences and measurements unchanged. Criterion action-1-analyze-brain-mri unchanged: it already requires contrast true, correct for suspected autoimmune encephalitis (Graus 2016; Venkatesan 2013 IEC consensus: gadolinium MRI to exclude structural, neoplastic, infective and enhancing demyelinating mimics before LP), with no plain alternative because a non-contrast study cannot answer that question; its expected_evidence is text of the gadolinium report it receives (verified with mri_probe and perfect_agent -v). No body-imaging MRI with enhancement and contrast false.
- MRI-CONTRAST verified: checked against 393c547e that the gadolinium follow-up (request_contrast_mri, contrast_used true) equals the original study except the flag, that the plain initial copy (contrast_used false) has no gadolinium key, finding, observation or impression clause left and its impression still matches its findings (laterality, sizes, numbering), that the contrast-true criterion fits Graus 2016 / Venkatesan 2013 and its expected_evidence is text of the gadolinium report it receives, that plain, contrast and both-order probes are answered by the case (never the library), that the contrast MRI is first in the pathway, that the case fallback MRI is null, that body-imaging MRIs with enhancement state contrast true, and that nothing else in the case changed; mri_probe and perfect_agent -v pass. No error found, no change made.

## Reviewer notes
Reviewer status: R2 approved (approved before this round: yes; changed only for class defects).

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| NB-87M:NMDAR-ENC-S01:policy_verdict | NO-ACTION | Plain approval, no comment. No change for the note itself; the class edits below apply (plan NMDAR-ENC section 3, S01). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | ground_truth.assessment.required_recommendations[0] | Template "within 72 hours" repeat-PCR clause and no empirical bacterial cover (class K2, D2, D3; R2 ruled it wrong in 24 cases). | FIXED: Graus 2016 wording; ceftriaxone 2 g IV every 12 hours with vancomycin until CSF cell count, Gram stain and culture exclude bacterial infection (Abboud 2021, ESCMID 2016). |
| C | major | ground_truth.assessment.required_recommendations[1] | Template first-line doses (5 days; "5 to 7 exchanges"), no combined-start reason and no IVIG/PLEX trade-off (class K3, D4-D6). | FIXED: methylprednisolone 1 g daily for 3 to 7 days combined from the start with IVIG 2 g/kg over 2 to 5 days or PLEX 5 to 10 sessions every other day, severity reason stated; IVIG preferred (agitation, autonomic instability) with sodium monitoring (133 mEq/L), hydration, slow infusion, VTE prophylaxis and the contraceptive stopped; COC and teratoma favor PLEX, kept as the alternative. |
| C | minor | ground_truth.assessment.required_recommendations[2] | No bridging must (class K4, D7). | FIXED: new bridging must (Abboud 2021). |
| C | major | ground_truth.assessment.required_recommendations[7] | Escalation "10 to 14 days", no cyclophosphamide dose (class K5, D8). | FIXED: 2 to 4 weeks after first-line therapy; rituximab regimen kept; IV cyclophosphamide 600 to 1000 mg/m2 monthly; fertility preservation kept (Abboud 2021). |
| C | minor | ground_truth.assessment.required_recommendations[8] | Benzodiazepine-first must without source (class K6, D10). | FIXED: "(Lejuste 2016)" appended. |
| C | minor | ground_truth.action_criteria[action-5-order-body-imaging] | Pelvic MRI not accepted as an alternative to ultrasound (class K7A, D13). | FIXED: alternative {study: pelvis_abdomen_MRI} and label "or pelvic MRI"; served() returns followup order_pelvis_abdomen_mri (1.8 cm right ovarian teratoma, same as the ultrasound). |
| C | minor | followup_outputs[check_drug_interactions].output.alternatives[0] | "Plasma exchange (5 to 7 exchanges)" (class K3, D4). | FIXED: "5 to 10 sessions every other day". |
| B | minor | initial_tool_outputs.csf.glucose_ratio, .interpretation | CSF report paired with serum glucose 98 mg/dL while the labs glucose is 106 (class K9, D21). | FIXED: "0.58 (serum glucose 106 mg/dL)"; interpretation ratio 0.58. |
| B | - | followup_outputs[order_cognitive_screen_post_intervention] | Template post-intervention screen checked against the baseline (D24): baseline not completed, so "persisting marked impairment" is consistent. | no change |

## Changes
Approved case, changed only for the condition-wide template defects the physician ruled wrong elsewhere (plan NMDAR-ENC K2-K7, K9). Must 1 now uses the Graus 2016 wording for repeating a too-early HSV PCR and adds empirical bacterial meningitis cover (ceftriaxone 2 g IV every 12 hours with vancomycin) until the CSF cell count, Gram stain and culture exclude bacterial infection. Must 2 gives the Abboud 2021 doses (methylprednisolone 1 g daily for 3 to 7 days; IVIG 2 g/kg over 2 to 5 days; plasma exchange 5 to 10 sessions every other day), states why combined therapy starts at once (autonomic instability, generalized seizures, fluctuating consciousness), and names IVIG as preferred for the agitation and autonomic instability, with sodium monitoring (133 mEq/L), hydration, slow infusion, VTE prophylaxis and the oral contraceptive stopped, and plasma exchange as the alternative favored by the contraceptive and teratoma. A bridging must was added (oral prednisone taper or monthly IVIG/methylprednisolone). The escalation must now reads 2 to 4 weeks after first-line therapy with IV cyclophosphamide 600 to 1000 mg/m2 monthly, and the benzodiazepine must cites Lejuste 2016. The tumour criterion also accepts pelvic MRI (the stored MRI shows the same 1.8 cm right teratoma). The drug-interaction output says plasma exchange 5 to 10 sessions, and the CSF glucose ratio is paired with the labs glucose (106 mg/dL, ratio 0.58).

## Verification
Pass 1: 0 errors found
- Checked against the note, plan sections 2-3 and D1-D35: every sub-point of the note has a ruling that matches what the case now does; musts vs prohibitions vs avoided actions, allergies and medications against the bacterial-cover regimen, sodium, osmolality and CSF/serum glucose values against the labs, stop-rule ids (all required criteria), sequence ids, key evidence and differential vs reports, no answer leakage in patient text or the drug-interaction output, no em dashes in new text. perfect_agent -v passes with each criterion receiving its evidence (body-imaging, microbiology and lab orders probed with served()); test_case_guards -k for the case passes; case_io check names no failure for the case.
- Nothing changed in this pass.

Pass 2: 0 errors found
- Focused verification: nothing was changed after the last 0-error pass (Pass 1), so no field needed re-verification. perfect_agent -v passes; test_case_guards -k for the case passes. Nothing changed in this pass.

Pass 3: 0 errors found
- Focused verification: nothing was changed after the last 0-error pass, so no field needed re-verification. perfect_agent -v passes; test_case_guards -k for the case passes. Nothing changed in this pass.
