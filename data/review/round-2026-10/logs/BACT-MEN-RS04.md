# BACT-MEN-RS04
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 95fadb54-c24c-468f-a321-41a70d579120 | FIXED | (1) Regimen: the "vancomycin 15-20 mg/kg + ceftriaxone 2 g" must deleted; the first must is now "vancomycin plus meropenem 2 g IV every 8 hours within 60 minutes, after cultures (IDSA 2017), with the meropenem interval adjusted to creatinine clearance"; the old "broaden ... (e.g. meropenem)" must is absorbed into it; prohibition added against the community-acquired regimen. (2) Dexamethasone: template must and the "do NOT discontinue dexamethasone" prohibition deleted; must "Adjunctive dexamethasone is not indicated once Gram-negative bacillary healthcare-associated meningitis is established" with the reasons (CD4 68, antigenaemia, treated TBM); same sentence in key evidence. (3) Cryptococcal antigenaemia: HPI now states "Pre-emptive fluconazole was not started"; must for fluconazole 800 mg daily for 2 weeks, 400 mg for 8 weeks, 200 mg maintenance (WHO 2022, renal adjustment); the CSF must asks for a repeat CSF cryptococcal antigen on this LP (the index CSF reports it negative); key evidence and a red herring explain the antigenaemia. |
| c4b392de-6b45-48f8-abbf-2bdb62280cce | FIXED | Must "Remove or replace the urinary catheter as soon as antibiotics have started" (plan C14 canonical); key evidence names the catheter as the source; new recommended criterion `action-8-order-microbiology-urine` (`order_microbiology {specimen: urine, tests: [culture, susceptibility]}`) answered by new follow-up `request_urine_culture` (Proteus mirabilis above 100,000 CFU/mL, same susceptibilities). |
| 36e776d3-230f-41dc-95a3-8476bd91ab74 | FIXED | `patient.neurological_exam.mental_status` GCS components "(E2 V2 M5)" = 9, matching "incomprehensible sounds" (V2) and "localizes pain" (M5) in the HPI, mental status and motor text. CT criterion, HARD constraint reason, must and prohibition rewritten on the two WHO 2025 Annex A.4 limbs that apply (GCS below 10; severe immunocompromise, CD4 68); "age >60" and IDSA 2004 removed everywhere. |
| 0b615209-0fd8-4228-bd20-ec129a3e7d14 | FIXED | CT follow-up (`request_ct_head`): enhancement finding removed (non-contrast study; `contrast_used` false kept because the criterion orders `contrast: false`); impression "No mass lesion, midline shift, basal cistern effacement or hydrocephalus. No extra-axial collection. Mild generalized cerebral volume loss."; "Safe to proceed with lumbar puncture" deleted. |
| 534b9cf8-0ada-477c-badf-35843aa8e7f1 | FIXED | Blood culture follow-up: `collected_before_antimicrobials` false with a "Collection" line (before the first IV dose, on co-trimoxazole 960 mg daily prophylaxis); impression and key evidence state the trimethoprim-sulfamethoxazole resistance that explains the breakthrough. |
| 361efa4f-ffce-4125-8eca-d9cca632a699 | FIXED | Pauci-cellular CSF pearl deleted from `key_clinical_evidence` and from `metadata.difficulty_rationale`; absent meningism declared as `red_herrings[1]` with the interpretation, and a key evidence line. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A/D | major | initial_tool_outputs.csf, .mri; followup `request_repeat_lp` | Index CSF and MRI in the initial work-up; post-treatment repeat LP as first pathway step (C1, C13) | FIXED: index CSF to follow-up `request_lumbar_puncture` (after the CT), MRI to `request_mri_brain_contrast`; repeat LP deleted; perfect agent confirms each criterion receives its report |
| B/D | major | index CSF | "RBC 5 (likely traumatic)", ratio string, panel result explaining its own limitation, culture identified to species at 24 hours, interpretation concluding "consistent with bacterial infection", `total_WBC` key rendering "WBC: N/A" (metadata concern) | FIXED: canonical RBC, ratio (12/92 = 0.13) and lactate strings; panel "No panel target detected (targets: ...)"; culture "Pending; preliminary growth of Gram-negative bacilli at 24 hours"; mycobacterial culture pending added; interpretation values and pattern only; keys `WBC`, `Neutrophils`...; the resolved `metadata.case_body_concerns` entry removed |
| D | minor | MRI output | Impression omitted its own key finding (leptomeningeal enhancement) and named toxoplasmosis and abscess; "likely related to chronic illness and malnutrition" | FIXED: findings-only impression including the enhancement; interpretive phrases removed |
| B | minor | blood culture output | Susceptibility as a finding row with `susceptibility` null, `gram_stain` null | FIXED: susceptibility dict, Gram stain, identification row |
| A/C | major | followup `request_pcr_panel` (interpret_labs) | CSF PCR filed as a blood lab (C8) | FIXED: deleted |
| A/C | minor | followup `request_audiometry` | Audiometry filed as `baep`, post-recovery result (C8) | FIXED: deleted; hearing must added |
| C | major | action-7 literature | Literature criterion expecting IDSA 2004, ESCMID 2016 (C9) | FIXED: criterion and follow-up deleted |
| C | major | action-6 check_drug_interactions | Template expected evidence; output with valproate filler and "existing AKI" without dosing | FIXED: required (plan 4.0): renal dosing of meropenem, fluconazole, tenofovir disoproxil and lamivudine at creatinine 1.4 (eGFR about 54 by CKD-EPI 2021, lower true clearance with BMI 17.2), vancomycin plus tenofovir nephrotoxicity, dolutegravir and trimethoprim raising creatinine, co-trimoxazole role; output rewritten to match |
| C | major | assessment | No mention that ART was held for several days with VL 137 | FIXED: must to resume ART with renal dosing |
| C | major | assessment | Sodium 119 mmol/L in an obtunded, malnourished patient with no management | FIXED: must (cause, cautious correction, at most 8 mmol/L in 24 hours for osmotic demyelination risk, monitoring); added to the differential as a contributor; prohibition against attributing the obtundation to it without CSF |
| C | minor | assessment | Droplet-precaution must (template) in hospital-acquired Gram-negative rod meningitis without rash | FIXED: deleted |
| C | minor | assessment | "Confirm HIV status" (known) and TBM relapse must that asked for tests "before attributing" the CSF | FIXED: merged into one CSF must that excludes TBM relapse and cryptococcal meningitis on the same specimen without delaying therapy |
| C | major | ground_truth.differential | TBM "high", viral and HSV "moderate" after a neutrophilic CSF with Gram-negative rods; SAH boilerplate (C10) | FIXED: six entries, all low with the supporting or excluding data (TBM relapse, cryptococcal, sepsis-associated encephalopathy, hyponatraemic encephalopathy, toxoplasmosis, HSV) |
| D | minor | patient.history_present_illness | Last sentence names the differential ("CNS infection versus septic encephalopathy") (C12) | FIXED: deleted |
| B | minor | labs.abnormal_values_summary | "Urinalysis: active UTI" (interpretive); serum CrAg flagged "(L)" | FIXED: values listed; flag removed |
| B | minor | initial_tool_outputs.labs | action-1 orders HIV but no HIV panel | FIXED: HIV panel with the known reactive result and the admission CD4 68 and HIV-1 RNA 137 that the case states |
| E | minor | red_herrings[0] | Em dash; field path to the whole clinical history | FIXED |
| C | minor | citations | `[IDSA_2004]`, free-text duplicates, De Gans on the drug check | FIXED: `[IDSA_2017_HCVM]` (governing source, as in M05) for the criteria and avoided actions; `[WHO_Meningitis_2025]` for the CT criterion and constraints |
| B | minor | metadata.difficulty_rationale | "1 red herrings; immunocompromise produces pauci-cellular ..." | FIXED |

## Changes, in one paragraph a physician can read before re-reviewing
Only labs are given upfront (now with the HIV panel). The pathway is blood cultures (Proteus mirabilis in 2 of 2 sets, collected on co-trimoxazole prophylaxis, resistant to TMP-SMX and ampicillin), non-contrast CT before LP because GCS is 9 (E2 V2 M5) and CD4 is 68 (findings only, no LP-safety sentence, no enhancement), the index LP (neutrophilic, ratio 0.13, Gram-negative rods, panel negative with its target list, AFB, Xpert and CSF CrAg negative, cultures pending), contrast MRI with DWI (leptomeningeal enhancement, no lesion), a recommended urine culture (Proteus), and a required drug check centred on renal dosing. The repeat LP, PCR-as-lab, audiometry and literature steps are gone. Management: vancomycin plus meropenem (renally adjusted), catheter removal or replacement, no adjunctive dexamethasone, narrowing on susceptibilities, pre-emptive fluconazole for the antigenaemia (not given earlier, now stated in the HPI) with a repeat CSF antigen, resuming ART, cautious correction of sodium 119, audiology. Red herrings: treated TBM, absent meningism, serum CrAg.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Diagnosis synonyms (plan section 5 item 5): `G00.8` appends "listeria meningitis", "listeria monocytogenes meningitis", "listeria meningoencephalitis", and `G00` appends "community acquired bacterial meningitis", all wrong for this hospital-acquired Proteus case; an agent answering "Listeria meningitis" would be scored correct. Not hand-edited (ruling 3).
- Vocabulary (plan section 5 item 4): `interpret_labs` `serum_cryptococcal_antigen`, `CD4_count`, `HIV_viral_load`; `analyze_csf` mycobacterial terms (the mycobacterial culture is reported in free text in the index CSF).
- Citation keys `[IDSA_2017_HCVM]` and `[WHO_Meningitis_2025]` for the allow-list.

## Open questions for Andrea (judgment calls you could not settle)
- Governing source: plan 1.1 makes IDSA 2017 govern RS04, but IDSA 2017 centres on neurosurgical devices and WHO 2025 excludes hospital-acquired disease. The imaging decision uses WHO Annex A.4 limbs by analogy, as the reviewer asked; the constraint reason says so.
- The urine culture criterion (recommended) and the hyponatraemia, ART and fluconazole musts are additions beyond the notes; drop any you consider out of scope.
- Meropenem is written as 2 g every 8 hours "adjusted to creatinine clearance": with BMI 17.2 her clearance may be below 50 mL/min, where the meningitic interval is every 12 hours. No weight is recorded, so the case cannot settle it.

## Verification
Adversarial check (23 October 2026) of the log against the case file, the plan (4.0 row RS04: imaging A on GCS 9 and CD4 68; meropenem plus vancomycin; DDI required) and the six notes (95fadb54, c4b392de, 36e776d3, 0b615209, 534b9cf8, 361efa4f, all present in the table). Read the whole final case. Confirmed: one empirical regimen (vancomycin plus meropenem, IDSA 2017) with a prohibition of the community-acquired regimen; no adjunctive dexamethasone; pre-emptive fluconazole must (WHO 2022 schedule for antigenaemia without meningitis: 800 mg 2 weeks, 400 mg 8 weeks, 200 mg maintenance) and the HPI now says it was not started; repeat CSF CrAg on this LP (reported negative); catheter removal must; GCS E2 V2 M5 = 9 consistent with HPI, mental status and motor text; CT without enhancement or LP-safety sentence; blood culture `collected_before_antimicrobials` false with the co-trimoxazole line and TMP-SMX resistance explaining the breakthrough; pauci-cellular pearl gone and absent meningism declared. No rifampicin interaction to address (TB treatment completed 3 months ago). Anion gap 13; eGFR about 54 (creatinine 1.4, woman, 25) as stated; meropenem and fluconazole renal statements in the drug check are correct. The wrong appended synonyms (Listeria, community acquired) are correctly left to CENTRAL.
Found and changed: (1) CBC differential summed to 94% (neutrophils 88, lymphocytes 6): Monocytes 6% (reference 2-10, normal) added to `initial_tool_outputs.labs.panels.CBC`. (2) The brain MRI listed "Small bilateral pleural effusions noted on scout images"; a brain MRI localiser does not cover the chest, so the observation is removed (the effusions stay in the examination). (3) `metadata.difficulty_rationale` said 5 required tools; there are 6 (labs, blood cultures, CT, CSF, MRI, drug check). `perfect_agent.py -v` passes with each criterion served its own report; `case_io.py check` clean for the case.

## Condition audit (23 October 2026)
- Changed `ground_truth.action_criteria[action-2-order-microbiology].alternatives[0].required_arguments`: removed `before_antimicrobials: true` (specimen and tests kept). Reason: the blood culture report sets `collected_before_antimicrobials: false` because an antimicrobial was taken in the 7 days before collection, so `true` is not the truthful value of the parameter ("whether the specimen is being taken before the first antimicrobial dose") and an agent that orders the cultures truthfully would miss a required criterion. Condition-wide rule settled at the audit: the argument is required only where the report flag is true (16 cases) and absent where it is false (14 cases: M01, M02, M03, M05, P02, P04, RM01, RM03, RP01, RP02, RP03, RP05, RS04, S03). Draw-before-treatment timing stays in the musts and in the SOFT blood-cultures-before-CT constraint where one exists. `perfect_agent.py` and `case_io.py check` clean after the edit.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
G00.8 no longer appends Listeria labels to this Proteus case; gram-negative bacillary labels scoped to it; "community acquired" removed (healthcare-associated, `except_cases` on `G00+community`).
- labels removed: "community acquired bacterial meningitis", "listeria meningitis", "listeria monocytogenes meningitis", "listeria meningoencephalitis"
- labels added: "other bacterial meningitis", "gram negative bacillary meningitis", "gram-negative bacillary meningitis", "gram negative meningitis"
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (6 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients
- Ward weight 44 kg (height 160 cm, BMI 17.2) recorded; meropenem must states the first dose in full and 2 g every 12 hours at a Cockcroft-Gault clearance of about 43 mL/min, reviewed daily

Re-run: `perfect_agent.py` ok; `case_io.py check` clean for the case; BACT-MEN case guards pass; synonym `--check` clean.

## Central vocabulary wired (24 Oct 2026)

`CD4_count`, `HIV_viral_load`, `serum_cryptococcal_antigen` (`interpret_labs`) and `mycobacterial_panel` (`analyze_csf`) are now core terms (CENTRAL request above).
- `initial_tool_outputs.labs.panels`: the `HIV` panel split into `HIV` (Ag/Ab reactive, known), `CD4_count` (68, admission) and `HIV_viral_load` (137 copies/mL, admission); the serum cryptococcal antigen (positive, 1:4) moved from "Infection screen" to its own `serum_cryptococcal_antigen` panel. Values, summary and interpretation unchanged. No new lab criterion: these are earlier results of this admission, stated in the HPI, and the musts act on them.
- `ground_truth.action_criteria[action-3-analyze-csf]`: `required_arguments.special_tests` now meningitis_panel, mycobacterial_panel, cryptococcal_antigen; label, rationale and expected evidence name the mycobacterial studies and the repeat CSF CrAg on the same specimen, which the must already required (recently treated tuberculous meningitis; antigenaemia at CD4 68).
- `followup_outputs[request_lumbar_puncture].output.special_tests`: `CSF_AFB_stain`, `CSF_GeneXpert_MTB_RIF` and `CSF_mycobacterial_culture` merged into `mycobacterial_panel` ("AFB smear negative; Xpert MTB/RIF Ultra: M. tuberculosis not detected; mycobacterial culture pending, final at up to 6 weeks"); `CSF_cryptococcal_antigen` renamed `cryptococcal_antigen`. Interpretation and `differential[0].key_features` say "AFB smear negative ... Xpert MTB/RIF Ultra not detected", matching the must's assay.
- Checks: `perfect_agent.py BACT-MEN-RS04 -v` ok; `case_io.py check` schema OK, synonym guard OK, no failure names the case; case guards pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality 'MRI', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
