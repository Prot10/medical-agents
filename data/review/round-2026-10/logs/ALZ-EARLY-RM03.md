# ALZ-EARLY-RM03
Reviewer status: R1 not reviewed, R2 not reviewed | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | The case has no reviewer notes; every change below is a class application from the condition plan or an own finding. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.diagnosis`, `clinical_assessment` | Staged as MCI with "instrumental independence preserved" although his wife took over the household finances after unpaid bills and an accounting error, he needs reminders for medicines and appointments, and he gets lost while driving (plan C4 rule 1.2, class application). | FIXED: `accepted[0]` "Early-onset Alzheimer disease (mild dementia, amnestic) with cerebrovascular copathology"; `icd_codes` [G30.0, G30.1, G30.9, G30.8, F00] (onset at 61, G31.84 primary removed, no duplicates); IADL-lost true, stage score "mild dementia", functional finding and impression rewritten; neuropsych impression with mild dementia wording. Synonym labels not hand-edited: CENTRAL. Open question below (plan Q2). |
| B | minor | `patient.neurological_exam.mental_status`, `clinical_assessment.findings` | MoCA 21/30 needs 9 points lost, but the listed losses (delayed recall 5, cube and trail, abstraction 1, date) plus the misplaced clock hands add to 10 or more. | FIXED: visuospatial/executive 2/5 (trail, cube, clock hands), delayed recall 0/5, orientation 5/6, abstraction 2/2 = 21/30. |
| C | minor | `clinical_assessment.findings`, `impression`, `scores` | Informant finding copied the patient introduction ("A 62-year-old right-handed retired civil engineer presents..."); findings split mid-sentence ("person and place;"); engineering impression ("this assessment is where it is decided"); score "administered at the bedside" (C3). | FIXED: examination, informant and functional findings from case data; plain impression; MoCA 21/30 score. |
| B | major | `followup_outputs[1]` CSF | 14-3-3, RT-QuIC, NMDA receptor and VGKC antibodies, oligoclonal bands and IgG index in a slowly progressive amnestic case with no autoimmune or rapid features; keys off vocabulary; references inconsistent with the other cases (C6). | FIXED: routine AD panel only, vocabulary keys, Abeta42 >600 and ratio >0.065 references (412/8200 = 0.050), pattern interpretation; "(normal)" removed from values. |
| B | major | `action-9-analyze-csf` | "single optional biological-confirmation route"; an amyloid PET order got the library's negative report (C2). | FIXED: two alternatives, canonical label, rationale, expected evidence; new follow-up `order_amyloid_pet` (18F-florbetapir, positive, Centiloid 71). Probe of every alternative: neuropsych <- `followup_outputs[0]`, CSF <- [1], PET <- [2], gene panel <- [3], drug check <- [4]; no library answer. |
| C | major | `followup_outputs` (two literature follow-ups) | `search_early_alzheimer_diagnostic_criteria` and `search_vascular_cognitive_impairment_differentiation` without a criterion (C8). | FIXED: both deleted; `initial`/`fallback` literature already null. |
| C | major | drug-check follow-up | Called zolpidem and donepezil an additive "CNS depressant" interaction (donepezil is not a CNS depressant), quoted an ECG the case does not contain, claimed amlodipine affects heart rate and that donepezil worsens sleep apnoea; criterion had empty arguments (C1). | FIXED: correct pharmacology (no PK interaction with zolpidem, which is a cognitive risk itself; aspirin GI risk; amlodipine does not slow HR), pulse 74, no ECG quoted; `{"drug": "donepezil"}`, trigger `check_drug_interactions_donepezil`, optional and last. |
| C | minor | gene panel follow-up, `action-6` | Finding "value" was the criterion's expected-evidence sentence; rationale = label. | FIXED: per-gene APP, PSEN1, PSEN2 results; label and rationale state the low yield with no family history; stays optional; battery-before-genetics constraint. |
| B | minor | `initial_tool_outputs.mri` | "No ... enhancement post-gadolinium", "No meningeal enhancement" and "patent on MRA" in a non-contrast dementia protocol; impression unnumbered and calls the small vessel disease only a "possibility" (C5). | FIXED: contrast and MRA statements removed; numbered impression naming Fazekas 2 small vessel disease. |
| B | minor | `followup_outputs[0]` neuropsych | Letter fluency 32 marked normal against ">33"; GDS 5/15 marked normal against "<5"; MCI wording. | FIXED: FAS marked abnormal (borderline-low), GDS reference "0-5 normal"; numbered impression. |
| B | minor | `initial_tool_outputs.labs` | BMP and separate liver panel for a CMP order; HbA1c and inflammatory markers in the "Dementia Workup" panel; "Reviewed_cognitive_panel_additions" panel name; interpretive summary text (C7). | FIXED: Comprehensive Metabolic Panel (total protein added), separate HbA1c and inflammatory panels, "Magnesium and Homocysteine"; factual summary with the normal free T4; values unchanged. B12 310 needs no MMA. |
| C | major | `ground_truth.assessment` | Musts restated tool steps plus the engineering biomarker must; no driving must despite getting lost twice; no zolpidem deprescribing (C12.2); generic prohibitions. | FIXED: informant, disclosure and young-onset planning, stop driving pending formal assessment, home safety, zolpidem deprescribing with taper and CBT-I and CPAP check [Beers_2023], canonical biomarker and AChEI musts, repeat TSH, vascular risk, Lewy follow-up. Prohibitions: hypothyroidism attribution, zolpidem or OSA attribution, antipsychotic for misperceptions, memantine at the mild stage. |
| C | major | `ground_truth.differential`, `red_herrings` | DLB and FTD `moderate` with template text although the history carries low-light visual misperceptions, waking confusion, slow rapid alternating movements and an uncle with PD; VCI said "No significant cerebrovascular burden" despite Fazekas 2 (C11). | FIXED: DLB low with what raises it and what argues against it; VCI as the sole cause low with copathology; FTD low; new medication- and sleep-related entry; new red herring for the Lewy-type features; TSH red herring names the normal free T4. |
| C | minor | `ground_truth.key_clinical_evidence` | Template items (MMSE in educated patients, APOE, B12, AChEI first-line) (C10). | FIXED: four case-specific items. |
| A | minor | criteria citations, rationales, order; constraints; stop rule | Duplicate keys, rationale = label, order not per plan, `max_additional_actions` 0. | FIXED: one or two keys each, case-specific rationales, order assessment, battery, labs, MRI, biomarker, genetics, drug check; assessment-before-biomarker and battery-before-genetics added; MRI-before-CSF reason shortened (no "older patients" at 62); `max_additional_actions` 1. |
| C | minor | `avoided_actions`, `metadata` | Generic rationales; engineering difficulty text and educational points. | FIXED: case-specific rationales; metadata rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing

No reviewer has seen this case. It is restaged as early-onset mild Alzheimer dementia with cerebrovascular copathology (G30.0, onset at 61), because his wife has taken over the finances after unpaid bills and an accounting error, he needs reminders for medicines and appointments, and he has got lost twice while driving; the clinical assessment, neuropsychological impression and label now agree, and the MoCA item breakdown adds up to 21/30. The CSF contains only the Alzheimer panel (the 14-3-3, RT-QuIC and autoimmune tests are gone), and CSF or amyloid PET can establish amyloid status (optional, one test enough; a concordant positive PET was added). The MRI names Fazekas 2 small vessel disease and no longer mentions gadolinium or MRA. The two literature steps are gone. The donepezil check now has correct pharmacology: zolpidem has no interaction with donepezil but is a cognitive and fall risk itself, and a must asks to deprescribe it with CBT-I and a CPAP check. Driving cessation pending formal assessment is a must. DLB stays in the differential at low likelihood, with the low-light misperceptions, waking confusion and family history of Parkinson disease explained in a red herring and a follow-up must, and an antipsychotic for the misperceptions is prohibited.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms: primary code changed from MCI (G31.84) to G30.0. The labels appended by the old G31.84 entry ("mild cognitive impairment", "MCI", "amnestic mild cognitive impairment", "amnestic MCI", "prodromal alzheimer", "mild cognitive impairment due to alzheimer") are still in `accepted` and would credit an MCI answer; please re-run `apply_diagnosis_synonyms.py --prune --cases ALZ-EARLY-RM03` (plan 5.1). G30.0 also grants "posterior cortical atrophy" and "benson syndrome" to this amnestic case.
- Citation keys used: `[STRIVE_2013]`, `[ACMG_NSGC_2011]`, `[NICE_NG97]`, `[Beers_2023]`, `[McKeith_2017_DLB]`, `[ETA_SCH_2013]` (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- Plan Q2: this case had no reviewer notes, and I restaged it from MCI to mild dementia by the class rule (a third party has taken over a complex instrumental activity). The label change has not been ruled on by a reviewer; please confirm, or say if it should stay MCI with the HPI rewritten so that the finances are only "needing help".

## Verification
Adversarial verifier, 24 Oct 2026. No reviewer notes for this case. Checked the class applications: restaging by the plan 1.2 rule is supported by the HPI (wife took over the finances after unpaid bills and an accounting error, reminders for medicines and appointments, lost twice while driving); IADL field, impression, neuropsych wording and label agree; MoCA breakdown now adds up (visuospatial/executive 3 + recall 5 + orientation 1 = 9, 21/30); CSF has only the AD panel (412/8200 = 0.050; glucose 62 with ratio 0.53 agrees with serum glucose 118); no literature follow-ups; MRI has no contrast or MRA text and names Fazekas 2; drug check content correct (no zolpidem pharmacokinetic interaction, amlodipine, aspirin GI risk, pulse 74 matches the vitals, no ECG quoted); zolpidem deprescribing and driving musts present; DLB low with the reasons and a follow-up must. B12 310 pg/mL is above the plan's MMA threshold despite metformin; no MMA step added. Both biomarker alternatives have case-authored outputs.

Found and fixed:
- C, minor, `ground_truth.assessment.required_recommendations` (subclinical hypothyroidism must): it said "Repeat TSH with free T4 in 6 to 12 weeks ... [ATA_hypothyroidism_2014]", which departs from the plan's canonical text for every case with TSH above range and normal free T4 (C1) and from the key in plan 1.1 (ETA 2013), and omitted TPO antibodies. Now the canonical must: "Repeat TSH and free T4 with TPO antibodies in 2 to 3 months rather than starting levothyroxine; a TSH of 5.8 mIU/L with normal free T4 does not explain the cognitive decline [ETA_SCH_2013]." CENTRAL citation list updated (`[ETA_SCH_2013]` replaces `[ATA_hypothyroidism_2014]`, which the case no longer uses).
No other change. Both checks clean for the case; case guards pass. The Q2 open question (restaging without a reviewer ruling) stays for Andrea: it is a plan-level question about labels no reviewer has ruled on.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- 'lasting power of attorney' (UK instrument) changed to 'durable power of attorney' in this US-setting case (1 place).
- citation key [McKeith_2017_DLB] harmonised to [DLB_2017], the key RP05 and the plan's CENTRAL list use (2 places).
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.
- Normal values in `Magnesium and Homocysteine` varied (Magnesium 2.0 to 2.1, Homocysteine 10.2 to 12.7), all still within the case's reference ranges: the same numbers (magnesium 2.0, homocysteine 10.2, ESR 12, CRP 1.8) had been copied into up to 13 cases, a template artefact raised by the S01 worker; no text cites the changed values.
- Checks re-run after these additions: perfect_agent.py, case_io.py check and test_case_guards clean.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`--prune --conditions alzheimers_early`): removed mild cognitive impairment labels (MCI, amnestic MCI, prodromal alzheimer, MCI due to alzheimer); "posterior cortical atrophy" and "benson syndrome"; code G30.1 (onset before 65); code G30.8 (atypical presentations only). Now: codes ['G30.0', 'G30.9', 'F00']; labels after accepted[0]: ['alzheimer disease', "alzheimer's disease", 'alzheimers disease', 'alzheimer dementia', 'dementia due to alzheimer', 'early onset alzheimer'].
- Added follow-up `order_advanced_imaging` FDG_PET (trigger `order_fdg_pet`, no criterion), after the amyloid-status follow-ups: a case-specific Alzheimer-type metabolic report concordant with the MRI and stage. Before, an FDG order returned the library's normal scan, contradicting the case (summary Q4). Probed: FDG and amyloid PET orders each return their own report, in either order.
- Plan Q2 settled: the restage to mild dementia (G30.0) is confirmed (wife took over finances, medication reminders, lost while driving: NIA-AA 2011 interference with usual activities).
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
