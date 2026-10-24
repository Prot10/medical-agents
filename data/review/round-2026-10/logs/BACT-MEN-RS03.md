# BACT-MEN-RS03
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 779f9ec1-e8f6-4601-8700-9943f3c27e6d | FIXED | (1) Regimen: template "vancomycin 15-20 mg/kg + ceftriaxone 2 g" must replaced by the canonical base must (ceftriaxone within 60 minutes, vancomycin only where resistance is prevalent, per plan C4 rather than the reviewer's vancomycin wording, since WHO 2025 makes vancomycin conditional) and the Listeria must "Add ampicillin 2 g IV every 4 hours ... because of age over 60 (74 years) and corticosteroid therapy (prednisolone 30 mg daily)"; Listeria monocytogenes meningitis added to `ground_truth.differential` (low, with the excluding PCR and blood isolate). (2) GCA: both options taken; declared as `red_herrings[0]` with the interpretation (prodrome fits GCA better than isolated PMR, 30 mg is below a GCA dose, arteritis does not explain purulent CSF, assess after the acute phase, withdrawal risks visual loss), added to the differential as M31.6 (low as the cause of the acute illness), and a must: ask now about visual disturbance and jaw claudication, then temporal artery examination and ultrasound or biopsy with rheumatology after the acute phase, GCA dose if confirmed. No tool exists for temporal artery ultrasound or biopsy, so it is a must, not a criterion. (3) Steroid plan: drug-interaction warning "discontinuing prednisolone to avoid excessive immunosuppression" removed; output and a new must say hold prednisolone during dexamethasone, then resume or taper, never stop abruptly (adrenal suppression; visual loss if arteritis). (4) `red_herrings` block created with three entries: PMR label/GCA, IgA MGUS, intrathecal IgA (index CSF `special_tests.Intrathecal_IgA_synthesis`, now a neutral "IgA index raised" result without the interpretive "likely related to known serum IgA gammopathy"). (5) Literature criterion `action-6-search-medical-literature` and its follow-up deleted (plan C9, ruling 5) rather than rewritten to WHO 2025/NICE; the "age >50" key evidence line replaced by the C17 text with "over 60". Imaging decided C (plan, Q5). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | action-4-order-ct-scan, sequence_constraints, CT must and prohibition, key_clinical_evidence[2], stop_rule | CT required with a HARD constraint on IDSA 2004 criteria ("altered mental status", "immunocompromise", "age >60"); none is a WHO 2025 Annex A.4 criterion here: GCS 14, no focal signs, no cranial nerve deficit, fundoscopy without papilloedema, no seizure, prednisolone 30 mg for about two weeks not counted as severe immunocompromise (plan C2, C) | FIXED: criterion, constraint and CT follow-up deleted; C must, C prohibition, key evidence line and waste avoided action `avoid-waste-5-order-ct-scan` added; CT id removed from `stop_rule` |
| A/D | major | initial_tool_outputs.csf; followup `request_repeat_lp` | Index CSF in the initial work-up and a post-treatment repeat LP (improving patient, no indication) as first pathway step (C1) | FIXED: index CSF moved to follow-up `request_lumbar_puncture` (initial `csf` null); repeat LP deleted; perfect agent confirms action-3 receives the index LP |
| B/D | major | index CSF | "RBC 5 cells/uL (likely traumatic)", ratio string without paired values, lactate reference, latex agglutination used as confirmation, interpretation listing every test; culture reported as identified organism at 18 hours (C7, C1) | FIXED: RBC "(within normal limits)", canonical ratio string (12/168 = 0.07), canonical lactate string, latex antigen removed, culture "Pending; preliminary growth of Gram-positive diplococci at 18 hours", interpretation reduced to values and pattern |
| B | minor | followup blood cultures | Only one finding row, no intervals, MICs in findings with `susceptibility` null, boilerplate "taken before the first antimicrobial dose, so the isolate is interpretable" (C6) | FIXED: two sets with positivity times (14, 16, 18 hours; one anaerobic bottle no growth at 5 days), identification row, `gram_stain`, MICs in `susceptibility` read against CLSI meningitis breakpoints, canonical impression. `collected_before_antimicrobials` true is correct (no antimicrobial in the history) |
| A/C | major | followup `request_pcr_panel` (interpret_labs) | CSF PCR filed as a blood lab and duplicated in the CSF (C8) | FIXED: deleted |
| A/C | minor | followup `request_audiometry` | Audiometry filed as `baep`, a post-recovery result (C8) | FIXED: deleted; hearing must added |
| C | major | followup `request_ct_head` | CT impression "No contraindication to lumbar puncture" (C3) | FIXED: follow-up deleted with the CT criterion |
| C | major | followup check_drug_interactions | Template vancomycin regimen with trough monitoring; prednisolone discontinuation advice | FIXED: checks ceftriaxone, ampicillin, dexamethasone against prednisolone, aspirin, ramipril, amlodipine, atorvastatin; eGFR about 58 (CKD-EPI 2021 from creatinine 1.3, age 74, male); expected evidence concrete; tier recommended (plan 4.0) |
| C | major | assessment.prohibited_recommendations | Template "Do NOT discontinue dexamethasone solely because the Gram stain is negative" (C5) | FIXED: deleted; dexamethasone must in canonical form with "Continue for 4 days: Streptococcus pneumoniae is identified." |
| C | minor | assessment.required_recommendations | "Reassess and de-escalate" without a target | FIXED: targeted must (penicillin MIC 0.02, ceftriaxone or benzylpenicillin, stop ampicillin, 14 days per NICE NG240) |
| C | minor | assessment.prohibited_recommendations | No guard against attributing the syndrome to the rheumatological illness | FIXED: prohibition added (mirrors red herring 0) |
| C | major | ground_truth.differential | Viral meningitis and HSV "moderate" after a neutrophilic CSF with S. pneumoniae; SAH boilerplate (C10, ruling 7) | FIXED: six entries, all low with the excluding data (Listeria, viral, HSV, TB, cryptococcal, GCA); SAH dropped (no thunderclap onset once the headache wording is fixed, RBC 5) |
| D | minor | patient.history_present_illness | Undeclared "worst of his life" headache (C11) | FIXED: "a severe, rapidly worsening diffuse headache" |
| B | minor | patient.history_present_illness | PCP "referred him to the emergency department", then 48 hours of deterioration before arrival | FIXED: PCP "arranged a review"; the 48-hour deterioration then leads to the ED visit |
| B | major | initial_tool_outputs.labs.panels.CBC | Neutrophils 89% plus bands 12% with no lymphocytes (101%) | FIXED: neutrophils 77, bands 12, lymphocytes 7 (L), monocytes 4; summary and interpretation updated |
| B | major | initial_tool_outputs.labs | HIV and liver tests ordered by action-1 but absent (C12) | FIXED: LFTs (normal; albumin 3.6) and HIV-1/2 Ag/Ab non-reactive added |
| D | minor | labs.abnormal_values_summary | "Glucose 168 mg/dL (stress/steroid hyperglycemia)" attributes a cause | FIXED: "(elevated)" |
| C | minor | action_criteria, avoided_actions citations | `[IDSA_2004]` and free-text duplicates | FIXED: `[WHO_Meningitis_2025]` |
| C | minor | key_clinical_evidence | Template lines (C17), duplicate WHO timing line | FIXED: C17 replacements; host-specific steroid line added; duplicate removed |
| B | minor | metadata.difficulty_rationale | "5 required tools; 0 red herrings" | FIXED: "3 required tools; 3 red herrings" |

## Changes, in one paragraph a physician can read before re-reviewing
The pathway is now blood cultures, then lumbar puncture without prior CT (GCS 14, no focal or cranial nerve signs, no papilloedema, no seizure; prednisolone 30 mg for about two weeks is not treated as severe immunocompromise, so CT is a waste action), then a drug check. The post-treatment repeat LP, the CT, the PCR filed as a blood test, audiometry and the literature step are gone. The index CSF reports values only (culture pending with preliminary Gram-positive diplococci, PCR S. pneumoniae, a neutral raised IgA index); the blood culture report gives intervals and CLSI-read MICs. Management: ceftriaxone within 60 minutes with ampicillin for Listeria (age 74, prednisolone), dexamethasone for 4 days for pneumococcus, droplet precautions, narrowing to ceftriaxone or benzylpenicillin for 14 days, holding prednisolone during dexamethasone and then resuming or tapering it (never abruptly), asking now about visual symptoms and jaw claudication and assessing giant cell arteritis after the acute phase, and audiology. The PMR/GCA prodrome, the IgA MGUS and the raised CSF IgA index are declared red herrings. Record fixes: headache wording, referral timeline, CBC differential 100%, liver tests and HIV added.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Vocabulary: no tool or term for temporal artery ultrasound (`order_body_imaging` study) or temporal artery biopsy (`obtain_tissue_diagnosis` procedure); the GCA assessment is a must only. Consider adding them if arteritis questions should be scoreable.
- Citation key `[WHO_Meningitis_2025]` on the allow-list (plan section 5 item 1).

## Open questions for Andrea (judgment calls you could not settle)
- Plan Q5: prednisolone 30 mg daily for about two weeks is not counted as WHO severe immunocompromise, so no CT before LP. Doses of 20 mg or more for 14 days or longer are often called high-level immunosuppression; if you rule otherwise, this case becomes A (CT required, HARD constraint).
- The droplet-precaution must is kept (acute presentation, organism unknown at presentation), as in RS02 and RP05; it could be dropped once Gram-positive diplococci are seen.
- The GCA must asks for assessment after the acute phase, as the plan says; a reviewer could prefer temporal artery ultrasound during the admission.

## Verification
Adversarial check (23 October 2026) of the log against the case file, the plan (4.0 row RS03: imaging C per Q5, Listeria yes) and note 779f9ec1. Read the whole final case. Confirmed: canonical base and Listeria musts (age 74, prednisolone), Listeria in the differential; GCA declared as a red herring, in the differential (low) and as a must, with the visual-loss warning; prednisolone plan (hold during dexamethasone, then resume or taper, never abruptly) in a must, the drug check and key evidence, and the old "discontinue prednisolone" advice gone; red-herring block with PMR/GCA, IgA MGUS and intrathecal IgA; literature criterion and follow-up deleted (plan C9), no "age >50"; CT criterion, constraint and follow-up deleted with C must, prohibition and waste action. Index CSF served to action-3 by `request_lumbar_puncture`; preliminary culture growth carries its interval (18 hours); blood culture `collected_before_antimicrobials` true is correct (no antimicrobials); HPI timeline (prednisolone about 2 weeks, review at day 10, 48 hours of deterioration) is consistent; CBC differential 100%; anion gap 12; eGFR about 58 (creatinine 1.3, man, 74) as stated; differential all low with the excluding results.
Found: nothing that needed a change. `perfect_agent.py -v` passes with action-3 served by `request_lumbar_puncture`; `case_io.py check` clean for the case.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (4 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients
- Pre-LP CT made neutral (no criterion, no waste penalty): prednisolone 30 mg for about 2 weeks meets the IDSA 2013 high-level immunosuppression threshold while WHO 2025 gives no steroid threshold; the no-imaging must, its prohibition and the CT waste avoided action replaced by a must that accepts either course with antibiotics first

Re-run: `perfect_agent.py` ok; `case_io.py check` clean for the case; BACT-MEN case guards pass; synonym `--check` clean.

## Central vocabulary wired (24 Oct 2026)
- DECLINED: no temporal artery ultrasound or biopsy criterion. Giant cell arteritis is not a competing explanation of the presentation (the neutrophilic CSF with S. pneumoniae in CSF and blood excludes it as the cause; `differential` GCA low), but a comorbid question the plan assigns to after the acute phase. A stored result would either add an unscored second diagnosis (a halo sign) or a negative that does not exclude GCA after two weeks of prednisolone 30 mg; the GCA must (ultrasound or biopsy with rheumatology review, glucocorticoid dose if confirmed) carries it. No case change.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality 'MRI', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
