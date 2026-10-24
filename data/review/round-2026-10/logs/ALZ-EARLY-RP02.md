# ALZ-EARLY-RP02
Reviewer status: R1 not reviewed, R2 not reviewed (no entry in notes/ALZ-EARLY.md) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer note names this case. Condition classes C1.2, C2, C3, C5, C8, C10, C11, C12, C13, C14, C16 of plans/ALZ-EARLY.md applied (see below). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | patient.neurological_exam.cranial_nerves | Visual extinction on the LEFT, while MRI and FDG are left more than right, she has Gerstmann features (dominant parietal) and right-hand astereognosis. | FIXED: extinction on the right; repeated in the clinical assessment. |
| B | minor | initial_tool_outputs.labs (glucose, calcium, platelets, MCV, B12, ESR, Mg, homocysteine, TSH, free T4); followup neuropsych MoCA, CVLT total | Values identical to RP01 (template carry-over between the two 62-year-old PCA cases). | FIXED: this patient's own values (all still normal); MoCA 17/30, CVLT-II total 44/80. |
| B/C | major | initial_tool_outputs.clinical_assessment | Amnestic template with `amnestic_predominant_profile` true, "storage deficit not helped by cueing", engineering sentence; no PCA signs in the findings (C3). | FIXED: amnestic false; cueing true with a recorded cued recall (0/3 free, 2/3 cued) consistent with an added CVLT-II recognition 15/16; findings now carry Balint, alexia, Gerstmann, apraxia, cortical sensory signs, informant and IADL; canonical impression. |
| B | minor | initial_tool_outputs.mri | Post-gadolinium and leptomeningeal statements with contrast false; "age-appropriate" atrophy that is also "disproportionate"; impression proposed "vascular cognitive impairment" (a clinical diagnosis) (C5). | FIXED: enhancement phrases removed; observation reworded; numbered impression with "suggestive of a posterior-predominant neurodegenerative process" and Fazekas 2 as small vessel disease; finding type renamed; duplicated DWI statement removed from FLAIR. |
| D | minor | followup_outputs[amyloid PET].findings[0].signal | "consistent with clinical presentation" (cross-modality) and "posterior-predominant amyloid burden" (amyloid in PCA is diffuse, as in typical AD; tau is posterior). | FIXED: diffuse retention, highest in posterior cingulate, precuneus and lateral parietal; impression now the binary read with plaque density; tracer filled. |
| D | minor | followup_outputs[FDG].findings[0].signal | "atypical for classic amnestic AD" is an interpretive cross-reference. | FIXED: removed; tracer filled. |
| D | major | followup_outputs[genetic panel].findings | Finding value was the criterion's expected_evidence text (scoring-key leakage). | FIXED: per-gene rows; expected_evidence now the result. |
| A | major | followup_outputs (two search_medical_literature) | Literature follow-ups with no criterion (C8). | FIXED: deleted. |
| C | major | followup_outputs[drug check]; action-11 | Output offered memantine "sometimes used earlier" (wrong at the mild stage), lacked the other medicines, and the criterion was optional with empty arguments although escitalopram with donepezil is a concrete QT interaction (C1.2, C14). | FIXED: output rewritten (escitalopram QT, baseline ECG and electrolytes; lisinopril and acetaminophen none; HR 72; bladder outflow warning; galantamine QT note); criterion `{"drug": "donepezil"}`, `required`, added to the stop rule. |
| A | major | ground_truth.action_criteria; followup_outputs | No ECG step although the donepezil plus escitalopram plan needs a baseline tracing (C14). There was no ECG avoided action to delete. | FIXED: new optional `action-12-analyze-ecg` with a follow-up (sinus rhythm 70, QTc 424 ms); fallback ecg stays null. |
| A/B | major | action-9; initial_tool_outputs.csf | Amyloid PET as the "single optional route"; CSF would return the library's normal result (C2). | FIXED: CSF and amyloid PET alternatives; concordant CSF authored (Abeta42 412, Abeta40 12600, ratio 0.033 low, p-tau181 118 high, t-tau 805 high). |
| A | minor | criteria order; sequence_constraints; stop_rule | Genetic panel before labs and MRI; no constraints; max_additional_actions 0 (C16). | FIXED: clinical, neuropsych, labs, MRI, biomarker, FDG, genetic, drug check, ECG; three soft constraints; max 1. |
| E | minor | all criteria | Rationale equal to label; duplicated citations (C13). | FIXED. MRI label now names the exclusions relevant here. |
| C | major | assessment.required_recommendations | Restating musts (labs, MRI, battery, FDG), engineering biomarker must; no treatment, safety plan for getting lost, rehabilitation or counselling (C12). | FIXED: AChEI must with baseline ECG because of escitalopram, canonical biomarker must, OT and low-vision must, safety must (driving, walking out alone, medicines, finances), BP and vascular risk check (Fazekas 2), genetic counselling must, informant and disclosure. |
| C | minor | assessment.prohibited_recommendations | Generic anticholinergic and antipsychotic prohibitions; benzodiazepine one not tied to her anxiety. | FIXED: ocular/anxiety attribution, benzodiazepine for worsening anxiety, mild-stage memantine. |
| C | major | ground_truth.differential | CBS and DLB `moderate` with features absent; CJD cited RT-QuIC and 14-3-3 not in the case; anxiety (raised by the history) and vascular contribution (Fazekas 2) missing (C11). | FIXED: CBS low (apraxia and astereognosis overlap stated), DLB low, CJD very low on DWI and course, anxiety and vascular cognitive impairment added low. |
| D/C | major | ground_truth.key_clinical_evidence | Six template items false for this case (C10). | FIXED: four items (PCA pearl, Balint/Gerstmann localisation, staging, escitalopram-donepezil QT). |
| C | minor | ground_truth.red_herrings | Empty; the plan names the sister's psychiatric symptoms as a red herring to keep. | FIXED: ophthalmology referral and family history red herrings. |
| - | check | 3.6 check | Probe: CSF -> initial csf, amyloid PET, FDG, genetic, drug check and ECG -> their follow-ups; none from the library. perfect_agent -v ok (drug check served the donepezil follow-up). | OK |

## Changes, in one paragraph a physician can read before re-reviewing
PCA due to Alzheimer disease, mild dementia, onset at about 61 (label and G30.0 unchanged). Visual extinction is now on the right, matching left-predominant parietal disease, Gerstmann features and right-hand astereognosis. The clinical assessment is now a PCA assessment with the functional staging explicit. Values copied from RP01 were replaced. The MRI and PET reports no longer contain contrast statements or cross-modality comments. The genetic report no longer carries scoring text, and the literature follow-ups are gone. Because she takes escitalopram, the donepezil interaction check is now required and states the QT interaction, and an optional baseline ECG (QTc 424 ms) was added. Amyloid status can be shown by CSF or amyloid PET, with a concordant CSF report authored. The differential now has CBS and DLB at low and adds anxiety and vascular contribution. The musts now cover treatment with ECG, low vision and OT, a safety plan for getting lost, vascular risk and genetic counselling.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys `[PCA_consensus_2017]`, `[ACMG_NSGC_2011]`, `[NICE_NG97]` (plan section 5.2).
- Synonyms: G30.1 and its labels appended to an early-onset case (plan section 5.1).

## Open questions for Andrea (judgment calls you could not settle)
- Q5 (RP01 versus RP02) decided: keep both. They come from different source reports (PMC10512534 and PMC10767313) and test different traps: RP01 is post-chemotherapy attribution in a cancer survivor with vascular risk; RP02 is an ophthalmology referral with full Balint and Gerstmann features, prosopagnosia, dressing apraxia, a family-history red herring and a real escitalopram-donepezil interaction. The shared template text (labs, key evidence, differential, musts) was the only duplication and has been replaced in both.

## Verification
Adversarial check, 24 Oct 2026. Read the log, the full diff and the whole final case. No reviewer note names this case.
- Confirmed: right-sided visual extinction now agrees with left-predominant MRI and FDG, Gerstmann features and right-hand astereognosis; clinical assessment fields agree with the narrative; MRI and PET reports carry no contrast or cross-modality text; genetic report clean; drug check required with correct content (escitalopram QT, HR 72 matches vitals) and in the stop rule; ECG follow-up internally consistent (QT 392 ms at 70 bpm gives Bazett QTc 423 to 424 ms); no ECG avoided action remains; both biomarker alternatives case-authored and concordant (412/12600 = 0.033); musts, prohibitions and differential match the evidence; Q5 decision (keep both PCA cases) is reasoned.
- Found and fixed (dim B, minor): the MMSE breakdown did not fit the exam it summarised. The exam documents alexia ("cannot read more than individual letters"), yet no point was lost on the written command, and she "states the month incorrectly" and is unsure of the date, which loses 2 orientation points, not 1. Now: oriented to person, place, year and month, unsure of the exact date; MMSE 24/30 = orientation 1 (date), recall 3, reading the written command 1, pentagons 1, serial sevens correct (patient.neurological_exam.mental_status; clinical_assessment.findings[0] and [1]). Gerstmann features here are finger agnosia and left-right confusion without acalculia, so correct serial sevens are consistent. Totals unchanged.
- perfect_agent.py -v and case_io.py check clean after the edits.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (the labs criterion label), the wording the other six cases already use.
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`--prune --conditions alzheimers_early`): removed code G30.1 (onset before 65). Now: codes ['G30.0', 'G30.9', 'F00', 'G30.8']; labels after accepted[0]: ['alzheimer disease', "alzheimer's disease", 'alzheimers disease', 'alzheimer dementia', 'dementia due to alzheimer', 'early onset alzheimer', 'posterior cortical atrophy', 'benson syndrome'].
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
