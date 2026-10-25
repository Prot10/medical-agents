# NMDAR-ENC-S09
Reviewer status: R1 not reviewed, R2 not reviewed (no `notes/NMDAR-ENC.md`: condition not reviewed this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | None: condition not reviewed. All changes below are the plan's class fixes (plan section 2, S09 entry) and my own findings. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria` | C1: non-schema `basic` and `screen_for`, exact literature `query`, `protocol: standard`, 11-panel labs list. | FIXED: plan 3.2 arguments; the existing cEEG criterion `action-6-analyze-eeg` keeps its id. |
| D | blocker | `followup_outputs` DDI | C3: DDI output repeated the criterion's expected_evidence with empty `interactions`; the leak guard failed. | FIXED: report voice. No home medicines, so the content covers the steroid effect on K 3.0, aciclovir hydration against fluid restriction, IVIG and measured sodium, sedation, the D2 class warning, HBV before rituximab, and the amoxicillin allergy with cefazolin acceptable for surgical prophylaxis. Guard passes. |
| D/C | major | `followup_outputs` literature (`request_literature_bilateral_teratoma`) | Fabricated content: an untraceable 2019 "title", "~10% bilateral" and "bilateral resection associated with better outcomes"; non-standard result keys; empty summary. | FIXED: canonical results plus Dalmau 2011 (teratoma is the main tumour; prompt removal with immunotherapy is associated with faster improvement and fewer relapses). Query "ovarian teratoma in anti-NMDA receptor encephalitis: diagnosis and treatment"; trigger `request_search_medical_literature`. No numbers on bilaterality. |
| C | major | literature and DDI criteria | C2, C10: both `recommended`. | FIXED: both `optional`, `{}`; literature last. |
| B | blocker | `initial_tool_outputs.csf`, `.labs` | C4: CSF antibody in two CSF keys and in the labs `Anti-Neuronal_Autoantibody_Confirmation` panel. | FIXED: one CSF key, final result 1:64; labs keep serum 1:1024 only. |
| C | major | `initial_tool_outputs.csf.glucose`, `.glucose_ratio` | CSF glucose 46 mg/dL, ratio 0.40: not a feature of the disease; it points to bacterial, tuberculous, fungal or carcinomatous meningitis. | FIXED: 70 mg/dL, ratio 0.60 (serum 116). Culture "Pending" becomes "No growth at 48 hours"; IgG index wording; cell differential in `cell_count`. |
| D/B | major | `initial_tool_outputs.labs` | C5: leaky `Exclusion studies`; ESR "Within reference range"; duplicated CRP; BMP without chloride, bicarbonate, BUN or calcium; no hepatic panel, free T4, GABA-B/AMPA, onconeural antibodies, beta-hCG or CK; interpretive summary ("severe SIADH", "mild anemia"). Na 124 with no osmolality after 6 kg of weight loss from refusal to eat. | FIXED: canonical panels. New values: Hct 35.6 (L), MCV 84, Cl 90, HCO3 23, BUN 9, Ca 9.0, liver panel, albumin 3.7, ESR 18, free T4 1.2, CK 342. Also a `Sodium work-up` panel: serum osmolality 258 (calculated 258), urine osmolality 460, urine sodium 52 (against hypovolaemia), cortisol 24.1. Plain recital. |
| C | major | `action_criteria` (new `siadh-workup`) | Na 124 needs the SIADH work-up, more so after poor intake (hypovolaemia to exclude). | FIXED: recommended `siadh-workup`, answered by the initial labs report. |
| B/D | major | `initial_tool_outputs.mri`, `.eeg` | Terse reports: MRI signal given only as prose, no observations; EEG with empty background, an arrow in the location and no correlate. | FIXED: full MRI fields (no restricted diffusion, no haemorrhage on SWI, no enhancement); EEG background, artifact, durations and correlate, ABNORMAL impression, limitations "Continuous EEG monitoring recommended." |
| D | major | `followup_outputs` cEEG | Impression "Very active disease with persistent EDB..." (kind 1 leakage, plan C7); empty background; seizures "bilateral temporal alternating" against a right temporal routine EEG. | FIXED: template impression, eight right temporal seizures without correlate, no electrographic status, extreme delta brush; background filled. |
| D/C | major | `fallback_tool_outputs` | C14: normal ECG at 61 bpm against HR 138; catch-all PET and neuropsychology; Holter average 77. | FIXED: initial ECG sinus tachycardia 136 bpm; ECG, PET and specialized fallbacks null; telemetry 112-142 bpm; `fallback_tool_kinds` updated. CT fallback kept. |
| D/C | major | `initial_tool_outputs.body_imaging` | C12: one line "Right: 3.2 x 2.8 cm dermoid. Left: 2.4 x 2.1 cm dermoid." and a lab-template impression. | FIXED: per-ovary findings with characteristic features (shadowing Rokitansky nodule, lines and dots, fat-fluid level, no vascularity), preserved ovarian tissue, radiology impression. |
| C | major | `ground_truth.assessment` | C9 template; bilateral teratomas, profound hyponatraemia, hypokalaemia and 6 kg weight loss not managed. | FIXED: M1, M2, bilateral laparoscopic ovary-sparing removal (plan), M4 without valproate, M5, M6 ICU (HR 138, BP 172/108, SpO2 94%, RR 24, seizures, profound hyponatraemia), M7, M8, M9 profound with 3% saline bolus for seizures and the 10 mmol/L limit, aciclovir in isotonic saline, potassium replacement, nutrition with refeeding precautions, M10. Prohibitions: canonical P1, P3, plus "Do not perform bilateral oophorectomy when ovary-sparing resection is feasible." |
| C | major | `ground_truth.differential` | C8 template. | FIXED: all `low` with case evidence; the HSV entry notes that the earlier febrile illness resolved without encephalopathy. |
| C | major | `ground_truth.key_clinical_evidence` | C15 template. | FIXED: seven case-specific bullets. |
| B/C | minor | `ground_truth.red_herrings` | "Mild hyponatremia (sodium 124)" is profound; the psychiatric data_point listed paranoia and hallucinations not in the HPI. The untested febrile illness with neck stiffness (a mimic the HPI raises) had no red herring. | FIXED: "Profound hyponatraemia" with the canonical interpretation; psychiatric data_point from the HPI; a third red herring for the earlier febrile illness with the canonical prodrome interpretation. |
| C/B | minor | rationales, citations, `metadata.difficulty_rationale`, `.difficulty_variant_description` | C16; "6 required tools, 2 red herrings"; "severe SIADH". | FIXED: 5 required, 3 red herrings; "profound hyponatraemia from SIADH". |

## Changes, in one paragraph a physician can read before re-reviewing
NMDAR-ENC-S09 is a 23-year-old woman with all six Graus groups, CSF anti-GluN1 1:64 (serum 1:1024) and bilateral ovarian mature cystic teratomas; label unchanged. The CSF glucose ratio was 0.40, a pattern that points to another meningitis; it is now 0.60. The labs are complete and show an SIADH pattern for the sodium of 124 (serum osmolality 258, urine osmolality 460, urine sodium 52), scored by a new recommended criterion. The MRI, EEG, cEEG and ultrasound are full reports; the cEEG no longer says "very active disease". An initial ECG (sinus tachycardia 136) replaces a normal fallback. The literature follow-up lost its fabricated claims. Musts now cover bilateral ovary-sparing teratoma removal (with a prohibition of bilateral oophorectomy when sparing is feasible), ICU care, profound-hyponatraemia management with a 3% bolus for seizures and the 10 mmol/L limit, potassium, and nutrition after 6 kg of weight loss. DDI and literature are optional.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: keys used `[Gresa-Arribas_2014]`, `[Herman_2015]`, `[Abboud_2021]`, `[Lejuste_2016]`, `[Spasovski_2014]`.
- To the lead: new criterion id `siadh-workup`. Here the cEEG criterion already existed as `action-6-analyze-eeg` and keeps that id.

## Open questions for Andrea (judgment calls you could not settle)
None. I decided these myself:
- I did not claim any frequency for bilateral teratomas or any outcome advantage of bilateral resection: I could not verify a source, and the plan asks for unsupported numbers to be deleted.
- The nutrition must is new. Six kilograms lost from refusal to eat, with hypokalaemia, makes refeeding risk real.

## Verification
Checked against the plan (sections 1.2, 2, 3, 4) and the final case file: every own-finding row of the log against the file; criteria order, tiers and minimal arguments (plan 3.2); stop rule (five required ids, max 2) and the soft MRI-before-CSF constraint; one CSF anti-GluN1 key with titre on the same doubling series as serum and no CSF entry in the labs; labs panels, `is_abnormal` flags and plain-recital summaries; laterality across exam, MRI, EEG and cEEG; allergies and medication list against musts and DDI output; musts against prohibitions and avoided actions; differential likelihoods against the results; red-herring data_points against the HPI; literature and DDI outputs for leakage (case guards pass). No reviewer notes exist for this condition, so there is no note id to account for.
Arithmetic checked: calculated serum osmolality (2 x Na + glucose/18 + BUN/2.8) matches the stored value; anion gap normal; CSF glucose ratio matches CSF/serum glucose; the SIADH values (low serum osmolality, urine osmolality above 100, urine sodium above 30, normal TSH, free T4 and cortisol) fit the sodium.
Found and changed:
- `initial_tool_outputs.eeg.findings[1]`: the structured fields were swapped (`frequency` held the rhythm, `morphology` held the seizure count and duration), against the convention of the other reports in this batch. Swapped back; morphology now "Evolving rhythmic ... theta".
- `initial_tool_outputs.labs.panels.Sodium work-up` urine sodium `reference_range`: "random; >30 with low serum osmolality is inappropriate natriuresis" is interpretation inside a lab report (kind 1 leakage toward the SIADH criterion). Now "No fixed reference range (random sample)".
`perfect_agent.py -v` and `case_io.py check` clean after the edits.

## Condition audit (24 Oct 2026)

Condition auditor, after the workers and verifiers. Uniformity checks over all 30 cases; changes made here through `case_io` (all re-checked: `perfect_agent.py` 30/30, `case_io.py check` and the case guards clean):
- `ground_truth.assessment.prohibited_recommendations[1]` and `[3]` (B/E, minor): the canonical P2 and P4 texts still carried an em dash before "antibody turnaround" and before "exclude mass effect", and an en dash in "1-2 weeks", while 18 other cases already had the dash-free canonical wording. Now "...high: antibody turnaround can take 1-2 weeks..." and "...new seizures: exclude mass effect first." Meaning unchanged.

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
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[order_performance_status]`: performance status KPS 30, ECOG 4 for the documented dependency.
- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `followup_outputs[order_gait_and_balance_timed]`: timed gait not testable or impaired, as on the examination.
- `order_specialized_test test_type=speech_language_evaluation` -> `followup_outputs[order_speech_language_evaluation]`: speech and language evaluation reflecting the documented speech disturbance.
- `order_body_imaging study=pelvis_abdomen_CT` -> `followup_outputs[order_pelvis_abdomen_ct]`: pelvic CT shows the teratoma seen on the stored ultrasound.
- `order_body_imaging study=pelvis_abdomen_MRI` -> `followup_outputs[order_pelvis_abdomen_mri]`: pelvic MRI shows the teratoma seen on the stored ultrasound.
- `order_body_imaging study=chest_abdomen_pelvis_CT` -> `followup_outputs[order_chest_abdomen_pelvis_ct]`: CT chest/abdomen/pelvis shows the teratoma seen on the stored ultrasound.
- `order_advanced_imaging modality=whole_body_FDG_PET` -> `followup_outputs[order_whole_body_fdg_pet]`: whole-body PET/CT: non-avid fat-containing adnexal lesion.
- `obtain_tissue_diagnosis procedure=resection` -> `followup_outputs[order_resection]`: resection pathology: mature teratoma with neuroglial tissue.
- `labs:AED_levels` -> fallback labs panel `Antiseizure medication levels`: antiseizure drug levels: none detected (no antiseizure drug prescribed).
- `labs:valproate_level` -> fallback labs panel `Antiseizure medication levels`: antiseizure drug levels: none detected (no antiseizure drug prescribed).

Checks: `perfect_agent.py` ok; `test_case_guards.py -k NMDAR-ENC` pass; every order listed in `plans/LIBRARY-group2-map.yaml` for this case is answered without the library; served answers of every other order unchanged against HEAD. Reasons and doubts: `plans/LIBRARY-group2-decisions.md`.
