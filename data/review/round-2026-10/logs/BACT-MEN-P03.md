# BACT-MEN-P03
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 53397644-08bd-4739-8019-50c5fc9047ac | FIXED | Contradictory LP bullets: deleted "Do NOT proceed to lumbar puncture: imaging shows mass effect ..."; kept the first bullet ("Do not withhold the lumbar puncture for raised intracranial pressure ...", `prohibited_recommendations[0]`). Pyogenic boilerplate: deleted the "Do NOT discontinue dexamethasone ... pneumococcal" prohibition and added "Do not give adjunctive corticosteroids (dexamethasone) for cryptococcal meningitis" (WHO 2022); "Do NOT treat with oral antibiotics alone" rewritten as "Do not treat with antibacterial therapy alone once the India ink or cryptococcal antigen is positive" (flucytosine is oral and mandated); literature criterion `action-7-search-medical-literature` and `initial_tool_outputs.literature_search` deleted (plan C9). Ordering constraint: CSF, CT and MRI moved out of the initial work-up into `followup_outputs` (blood cultures, CT, index LP, MRI, drug check, therapeutic drainage); HARD CT before CSF kept, reason restated on bilateral grade II papilloedema (WHO 2025 Annex A.4) with the WHO qualifier that in people with HIV and a suspected first episode of cryptococcal meningitis prompt LP with opening pressure and rapid CrAg is preferred, so imaging must not delay the puncture; CT label, expected evidence, must-side prohibition (`prohibited_recommendations[2]`) and key evidence rewritten to match; "altered mental status, immunocompromise, age >60" removed everywhere. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | blocker | initial_tool_outputs.labs (HIV and Immunology) | Serum cryptococcal antigen 1:1024 delivered with the first blood panel: the decisive test, not ordered (not orderable) and handed over before any action | FIXED: removed; CSF CrAg in the index LP establishes the diagnosis |
| B | major | initial_tool_outputs.labs | HIV-1 viral load (multi-day turnaround) in the first panel; procalcitonin and CSF cytology filed as an "Exclusion studies" panel with a narrative; coagulation ordered but absent; summary lines carried interpretation ("(AIDS)") | FIXED: viral load removed (a must now asks for it); procalcitonin 0.08 ng/mL in the inflammatory panel; cytology moved to the CSF report; PT, INR, aPTT added; values and flags only. HIV Ag/Ab reactive, differentiation assay and CD4 45 (4%) kept |
| B | major | initial_tool_outputs.csf | No multiplex panel or cytology result although the criterion orders both; bacterial culture "No growth at 48 hours" in a same-day report; "deceptively clear" appearance; lactate "(mildly elevated)" at 3.2; ratio and RBC strings non-canonical | FIXED: multiplex panel "Cryptococcus neoformans/gattii detected; no other panel target detected" with targets listed; cytology negative; bacterial culture "Pending"; "Clear, colorless"; canonical ratio, RBC and lactate strings; interpretation lists values and stain/antigen/PCR results only (C1, C7) |
| B | major | followup_outputs (request_therapeutic_lp) | Therapeutic LP trigger carried an LP token (served to any "lumbar puncture" order, plan C1); report held "Patient_response" (clinical outcome) and "(goal achieved)" | FIXED: trigger `request_therapeutic_csf_drainage`, placed last; procedure line states a second puncture 24 hours after the diagnostic one; patient response removed; canonical CSF strings |
| B | major | followup_outputs (request_fungal_culture, request_ophtho) | Fungal culture with speciation and MICs at 5 days filed under `interpret_labs`; ophthalmology consultation filed as labs | FIXED: both deleted (C8); fungal culture is pending in the index CSF and the papilloedema is in the examination |
| D | major | initial_tool_outputs.ct | Impression and recommended actions prescribed ICP management and LP guidance | FIXED: numbered findings, "Contrast-enhanced MRI recommended"; moved to `followup_outputs[1]` (C3, C13) |
| D | minor | initial_tool_outputs.mri | Impression pointed to "the differential below" and to CSF; T1 "without transependymal edema" contradicted the T2/FLAIR periventricular signal | FIXED: numbered findings with a one-line imaging differential (gelatinous pseudocysts vs prominent perivascular spaces); T1 line reduced to "Ventricular dilatation"; moved to `followup_outputs[3]` (C13) |
| B | minor | initial_tool_outputs.microbiology | "Specimen taken before the first antimicrobial dose" boilerplate; no interval | FIXED: "No growth at 48 hours in 2 of 2 sets; final report at 5 days" (flag stays true: no systemic antimicrobial before collection; nystatin is not absorbed) |
| C | major | ground_truth.differential | TB left high, bacterial and HSV moderate after a CrAg 1:2048, India ink positive CSF | FIXED: TB low (co-infection possible, screening is a must), bacterial, HSV, lymphoma, toxoplasmosis very low, each with the excluding result (C10) |
| C | major | ground_truth.red_herrings | Only red herring was the pyogenic "negative Gram stain" template | FIXED: replaced with the distractors the case is built on (absent meningism and fever; clear CSF with 35 cells) |
| D | minor | patient.chief_complaint, patient.history_present_illness | "Worst headache of my life" undeclared (C11); chief complaint "3 weeks" against HPI "4 weeks" | FIXED: "a severe, progressively worsening diffuse headache" (the plan's "rapidly" does not fit a 4-week course); last HPI sentence keeps the gradual onset without the quote; chief complaint "over 4 weeks" |
| B | minor | patient.clinical_history.medications | Nystatin prescribed 2 weeks ago in the history but medication list empty | FIXED: added |
| C | major | ground_truth.assessment.required_recommendations | Induction "liposomal amphotericin B 3-4 mg/kg/day plus flucytosine for at least 2 weeks" (not the WHO 2022 preferred regimen); no consolidation or maintenance; no amphotericin toxicity package; CD4 already in the panel | FIXED: WHO 2022 single high-dose liposomal amphotericin B 10 mg/kg + flucytosine 100 mg/kg/day + fluconazole 1200 mg/day for 14 days, with the 2-week L-AmB alternative; consolidation 800 mg/day 8 weeks then 200 mg/day; therapeutic LPs at OP 25 cmH2O or more to below 20, daily; pre-hydration, K and Mg, monitoring; HIV confirmation, viral load, ART at 4 to 6 weeks; TB screening and co-trimoxazole prophylaxis |
| C | minor | ground_truth.action_criteria[action-6] | DDI expected evidence was the template text; label referred to an antiretroviral regimen the patient does not have; initial drug block empty with the expected text as summary | FIXED: label and expected evidence name amphotericin-flucytosine renal interaction, flucytosine marrow toxicity on baseline leukopenia and anemia, electrolytes, fluconazole CYP and QT; new `followup_outputs[4]`; tier stays recommended (plan 4.0) |
| C | minor | ground_truth.action_criteria[action-3, action-4] | CSF label contained "therapeutic drainage" (would token-match the drainage follow-up); MRI label was the generic template | FIXED: CSF label lists the studies sent, "repeated removal of CSF"; MRI label and expected evidence are case-specific |
| D | minor | ground_truth.key_clinical_evidence | "non-negotiable" L-AmB line conflicted with the WHO preferred regimen; last line was the WHO 2025 template | FIXED: induction line states the WHO 2022 preferred regimen; last line states the WHO HIV qualifier on prompt LP |
| A | minor | citations | `[IDSA_2004]` and free-text duplicates | FIXED: `[WHO_Meningitis_2025]`, `[WHO_Cryptococcal_2022]` |
| E | minor | metadata.difficulty_rationale | Stated that imaging "shows mass effect / hydrocephalus that contraindicates LP" | FIXED: rewritten to the ruled position |

## Changes, in one paragraph a physician can read before re-reviewing

Only the blood panel is given upfront, and it no longer contains the serum cryptococcal antigen or the
viral load (HIV reactive with CD4 45 stays). Blood cultures, the non-contrast CT (required before the
LP because of bilateral papilloedema, with the WHO qualifier that imaging must not delay the LP in
HIV), the index LP, the contrast MRI and the drug check are pathway steps in that order, followed by
a second LP for drainage (trigger without the LP token). The index CSF carries opening pressure 38,
35 cells, India ink positive, CrAg 1:2048, multiplex PCR positive for Cryptococcus, cultures pending.
The LP position is single (do not withhold it; image first because of papilloedema); the pyogenic
dexamethasone and antibiotic bullets and the literature step are gone, and corticosteroids are
prohibited. Musts follow WHO 2022 (single high-dose L-AmB with flucytosine and fluconazole,
consolidation and maintenance, daily therapeutic LPs, toxicity prevention, ART at 4 to 6 weeks, TB
screening and co-trimoxazole). The differential is post-CSF, the red herrings are absent meningism and
a bland CSF, and "worst headache of my life" is rephrased.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `interpret_labs` has no `serum_cryptococcal_antigen`, `CD4_count` or `HIV_viral_load` (plan section 5 item 4); CD4 is reported with the HIV test because the label rests on advanced HIV, and serum CrAg and viral load were removed until they can be ordered.
- `analyze_csf` has no `fungal_culture` or `india_ink` term (plan section 5 item 4); both live in the index CSF report.
- Citation key `[WHO_Cryptococcal_2022]` for the criteria pack allow-list.

## Open questions for Andrea (judgment calls you could not settle)

- Plan Q1: cryptococcal meningoencephalitis (B45.1) kept as a non-pyogenic mimic inside `bacterial_meningitis` with a P prefix.
- MRI stays `required` as authored: it is reasonable in advanced HIV with papilloedema to exclude focal opportunistic lesions, but WHO 2022 does not require it once CSF CrAg is positive; downgrade to recommended if Andrea prefers the guideline minimum.

## Verification

Adversarial verifier, 23 October 2026. Checked: note 53397644 against the final file (the "Do NOT proceed to lumbar puncture" bullet is gone, the drainage bullet kept as `prohibited_recommendations[0]`; dexamethasone and oral-antibiotic boilerplate rewritten for cryptococcal disease; corticosteroids prohibited; literature step deleted; CSF, CT and MRI are pathway steps; HARD reason rests on bilateral grade II papilloedema with the WHO HIV qualifier; no "age >60" or "altered mental status" left); action-3 receives the index LP, not the drainage LP (`-v`); drainage trigger carries no LP token; ratios 32/95 = 0.34 and 34/97 = 0.35; anion gap 10; musts against WHO 2022 (single-dose L-AmB 10 mg/kg + flucytosine 100 mg/kg/day + fluconazole 1200 mg/day for 14 days; consolidation 800 mg/day 8 weeks then 200 mg/day; therapeutic LP at 25 cmH2O or more; ART at 4 to 6 weeks); red-herring path `followup_outputs[2].output.cell_count` resolves to the index CSF; chief complaint and HPI both 4 weeks; nystatin is non-absorbed, so `collected_before_antimicrobials: true` is right.

Found and changed:
- `action_criteria[action-4-analyze-brain-mri].citations` kept the free-text duplicate "WHO meningitis guideline 2025": removed.
- `metadata.case_body_concerns` [0], [1], [3], [4], [5], [6] described defects already fixed (DDI and literature "reclassified", harmful-tool conflict, pneumococcal prohibition, `request_chest_ct`, 3 versus 4 weeks) and were false: deleted; [2] (P prefix, plan Q1) kept.

Left as is: CD4 count and the HIV differentiation assay are reported with the first panel (no CD4 vocabulary yet, worker's CENTRAL entry); the MRI tier (required) stays the worker's open question.

After the edits: `perfect_agent.py BACT-MEN-P03 -v` passes; `case_io.py check` clean for the case.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (4 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Contrast MRI downgraded from required to recommended and removed from the stop rule: WHO 2022 bases the diagnosis on CSF opening pressure and CrAg and requires no MRI; the required pre-LP CT already screens for a mass

Re-run: `perfect_agent.py` ok; `case_io.py check` clean for the case; BACT-MEN case guards pass; synonym `--check` clean.
