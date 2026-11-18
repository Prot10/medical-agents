# NMDAR-ENC-RS01

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-6-search-medical-literature (optional); removed 2 literature follow-up(s). Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: split initial_tool_outputs.mri (gadolinium study). The gadolinium study, text unchanged, is now followup_outputs[0] (analyze_brain_mri, trigger request_contrast_mri, contrast_used true), first in the pathway as the core diagnostic MRI; the plain copy (contrast_used false) keeps the initial slot: removed observation 'No leptomeningeal enhancement', the post_gadolinium keys of both findings, and 'pathological enhancement' from impression item 1. Pre-contrast sequences and measurements unchanged. Criterion action-1-analyze-brain-mri unchanged: it already requires contrast true, correct for suspected autoimmune encephalitis (Graus 2016; Venkatesan 2013 IEC consensus: gadolinium MRI to exclude structural, neoplastic, infective and enhancing demyelinating mimics before LP), with no plain alternative because a non-contrast study cannot answer that question; its expected_evidence is text of the gadolinium report it receives (verified with mri_probe and perfect_agent -v). No body-imaging MRI with enhancement and contrast false.
- MRI-CONTRAST verified: checked against 393c547e that the gadolinium follow-up (request_contrast_mri, contrast_used true) equals the original study except the flag, that the plain initial copy (contrast_used false) has no gadolinium key, finding, observation or impression clause left and its impression still matches its findings (laterality, sizes, numbering), that the contrast-true criterion fits Graus 2016 / Venkatesan 2013 and its expected_evidence is text of the gadolinium report it receives, that plain, contrast and both-order probes are answered by the case (never the library), that the contrast MRI is first in the pathway, that the case fallback MRI is null, that body-imaging MRIs with enhancement state contrast true, and that nothing else in the case changed; mri_probe and perfect_agent -v pass. No error found, no change made.

## Reviewer notes
Reviewer status: R2 needs_changes (approved before this round: no).

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| NB-87M:NMDAR-ENC-RS01:policy_verdict (a) MRI "contrast used: none" | ALREADY-FIXED | Class MRI-CONTRAST (commit 71517e55): the gadolinium study is followup_outputs[0] (request_contrast_mri, contrast_used true) and is what action-1-analyze-brain-mri {contrast: true} receives; mri_probe clean. |
| (b) Must 1 repeat-PCR clause | FIXED | ground_truth.assessment.required_recommendations[0]: the "within 72 hours" clause replaced by the Graus 2016 wording (PCR can be negative if done too early, for example within 24 hours, and is repeated if suspicion remains high). |
| (c) Bacterial cover | FIXED | required_recommendations[0]: ceftriaxone 2 g IV every 12 hours with vancomycin until the CSF cell count, Gram stain and culture exclude bacterial infection (Abboud 2021, ESCMID 2016); no beta-lactam allergy, age 31. |
| (d) NSAIDs | NO-ACTION | Kept ("without NSAIDs (hold ibuprofen)"), as the physician confirmed. |
| (e) Must 2 timing and combined start | NO-ACTION | Supported; the severity reason is now written into required_recommendations[1]. |
| (f) Doses | FIXED | required_recommendations[1]: methylprednisolone 1 g daily for 3 to 7 days; IVIG 2 g/kg over 2 to 5 days; PLEX 5 to 10 sessions every other day. Same correction in followup_outputs[check_drug_interactions].output.alternatives[0]. |
| (g) IVIG versus PLEX | FIXED | required_recommendations[1]: IVIG preferred (agitation, autonomic instability), with sodium monitoring (131 mEq/L), hydration, slow infusion, VTE prophylaxis and the contraceptive stopped; the contraceptive, immobility and teratoma favour PLEX, the stated alternative (with central access and hemodynamic monitoring). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | minor | ground_truth.assessment.required_recommendations[2] | No bridging must (class K4, D7). | FIXED: new bridging must (Abboud 2021). |
| C | major | ground_truth.assessment.required_recommendations[7] | Escalation "10 to 14 days", no cyclophosphamide dose (class K5, D8). | FIXED: 2 to 4 weeks; IV cyclophosphamide 600 to 1000 mg/m2 monthly (Abboud 2021). |
| C | minor | ground_truth.assessment.required_recommendations[8] | Benzodiazepine-first must without source (class K6). | FIXED: "(Lejuste 2016)". |
| C | minor | ground_truth.action_criteria[action-5-order-body-imaging] | Pelvic MRI not an accepted alternative (class K7A, D13). | FIXED: {study: pelvis_abdomen_MRI} added, label "or pelvic MRI"; served() returns followup order_pelvis_abdomen_mri (2.8 cm left ovarian teratoma, as on ultrasound). |
| B | minor | initial_tool_outputs.labs.panels.Other[Serum osmolality], abnormal_values_summary, interpretation | Measured osmolality 268 was 4 below the calculated 272 (2 x 131 + 102/18 + 12/2.8) (class K10). | FIXED: 274 mOsm/kg (still low against 275-295). |
| B | - | followup_outputs[order_cognitive_screen_post_intervention], [order_performance_status] | Checked against baseline (D24, D25): baseline screen incomplete, two-person-assist gait; consistent. | no change |

## Changes
Must 1 (aciclovir) now uses the Graus 2016 wording on repeating an HSV PCR done too early, keeps hydration and the ibuprofen hold, and adds empirical bacterial meningitis cover (ceftriaxone 2 g IV every 12 hours with vancomycin) until the CSF cell count, Gram stain and culture exclude bacterial infection. Must 2 gives the Abboud 2021 doses (methylprednisolone 1 g daily for 3 to 7 days; IVIG 2 g/kg over 2 to 5 days; plasma exchange 5 to 10 sessions every other day), states the severity that justifies combined therapy (central hypoventilation, autonomic instability, repeated seizures, catatonia), and records the divergence: IVIG preferred for agitation and autonomic instability, with sodium monitoring (131 mEq/L), hydration, slow infusion, VTE prophylaxis and the contraceptive stopped; plasma exchange, favoured by the contraceptive, immobility and teratoma, is the alternative. A bridging must was added, the escalation must now reads 2 to 4 weeks with IV cyclophosphamide 600 to 1000 mg/m2 monthly, and the benzodiazepine must cites Lejuste 2016. The tumour criterion also accepts pelvic MRI (stored MRI matches the ultrasound), the drug-interaction output says 5 to 10 plasma-exchange sessions, and the measured serum osmolality is 274 mOsm/kg so it agrees with the calculated value. The MRI contrast header was already corrected by the October/November MRI class.

## Verification
Pass 1: 0 errors found
- Checked against the note, plan sections 2-3 and D1-D35: every sub-point of the note has a ruling that matches what the case now does; musts vs prohibitions vs avoided actions, allergies and medications against the bacterial-cover regimen, sodium, osmolality and CSF/serum glucose values against the labs, stop-rule ids (all required criteria), sequence ids, key evidence and differential vs reports, no answer leakage in patient text or the drug-interaction output, no em dashes in new text. perfect_agent -v passes with each criterion receiving its evidence (body-imaging, microbiology and lab orders probed with served()); test_case_guards -k for the case passes; case_io check names no failure for the case.
- Nothing changed in this pass.

Pass 2: 0 errors found
- Focused verification: nothing was changed after the last 0-error pass (Pass 1), so no field needed re-verification. perfect_agent -v passes; test_case_guards -k for the case passes. Nothing changed in this pass.

Pass 3: 0 errors found
- Focused verification: nothing was changed after the last 0-error pass, so no field needed re-verification. perfect_agent -v passes; test_case_guards -k for the case passes. Nothing changed in this pass.
