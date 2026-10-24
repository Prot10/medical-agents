# GBS-RS11
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| c1f03f5c-5825-4c73-9861-1a3e3111f6c7 | FIXED | Option chosen (plan RS11): no limb weakness, with paresthesias, so the case is the recognised variant. `patient.neurological_exam.motor` now gives 5/5 throughout (the 4/5 and 4+/5 values are gone). Distal paresthesias were added to the HPI and chief complaint (fingers and feet, 6 days), and `neurological_exam.sensory` now records mild vibration loss at the great toes. Gait is normal and Romberg negative, because ataxia would point to the MFS spectrum. The reduced reflexes stay. `ground_truth.diagnosis.accepted[0]` changes from "bilateral facial diplegia variant" to "Guillain-Barré syndrome, bifacial weakness with paresthesias variant" [Wakerley_2014]. KCE 1 names the variant and says Brighton does not apply without limb weakness. |
| 22430160-f2dc-4969-ad80-707f33b703cf | FIXED | Option chosen: negative (plan C2/RS11), since GQ1b is not the marker of this variant. The ganglioside follow-up now reports anti-GQ1b IgG only, negative, with a hedged templated comment, and its trigger is renamed `request_anti_gq1b_gt1a_ganglioside_panel`. Anti-GM1 IgG was removed. Differential: "Miller Fisher syndrome or GBS overlap" very_low (full eye movements, no ataxia, GQ1b negative). KCE 4 is the canonical ganglioside pearl. No criterion scores the antibody: see CENTRAL 1. Even with the term it would be optional at most here. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B/C | major | `patient.history_present_illness`, `chief_complaint` | A 1-day "sudden" bilateral palsy on waking does not fit a GBS time course, and CSF protein 78 with demyelinating NCS on day 1 is implausible. The HPI also ended with two editorial sentences ("strongly suggests an underlying systemic process", "raises the clinical suspicion for a broader peripheral neuropathy") (C7). | FIXED: paresthesias from 6 days ago, then the right face 2 days ago (the GP's Bell's palsy diagnosis) and the left face yesterday, complete this morning. The editorial sentences were deleted. Pertinent negatives added (diplopia, unsteadiness, swallowing, breathing, rash, sphincters). |
| D | major | `patient.neurological_exam.additional` | Spirometry (FVC 3.2 L, 73%, NIF -42) leaked the a4 result, and the editorial "bilateral Bell's palsy is rare and should trigger systemic workup" was there too (C1/C7). | FIXED: field set to null. |
| C | minor | `patient.neurological_exam.cranial_nerves` | "Unable to clench teeth" is trigeminal motor weakness, not facial. | FIXED: jaw closure strong, facial sensation intact; bulbar and neck negatives added. |
| A | minor | `patient.physical_exam` | No weight (plan 1.2). | FIXED: "Weight 76 kg, height 175 cm" (BMI 24.8 agrees), plus pertinent sarcoid negatives (no rash, lymphadenopathy, parotid swelling, uveitis). |
| C | major | `initial_tool_outputs.labs` | EBV IgM, CMV IgM and serum HSV PCR were in the current labs (C3). HIV was listed twice, one copy with the leaky clinical_significance sentence (C10). Lyme ELISA sat in the baseline labs although Lyme now has its own criterion. Potassium, glucose, liver tests, albumin, platelets and CK were missing although a1 expects them. | FIXED: antecedent serology deleted. One HIV Ag/Ab non-reactive, significance null. Lyme moved to its own follow-up. CMP (glucose 89, consistent with CSF ratio 0.70), platelets and CK 142 added, all normal. ACE, ANA, dsDNA and ANCA kept. |
| D/B | major | `initial_tool_outputs.specialized_test` | The blink finding said "bilateral facial nerve demyelination confirmed" (Kind 1). The facial motor values had no numbers. Sural SNAP 14 uV was called "mildly reduced" (normal >6). There was no needle EMG and `test_type` was prose. | FIXED: report rewritten with numbers and limits: facial DL and CMAP, blink R1/R2 efferent pattern, median and peroneal DML/CV/CMAP, F and H, median SNAP reduced with normal sural (sural sparing), needle EMG (facial reduced recruitment, limbs normal). Hedged impression; `test_type` "emg_ncs". |
| C | minor | `followup_outputs` CSF | The interpretation had "(N/A PMN/N/A lymph)". | FIXED: report-voice interpretation with opening pressure, ratio and the dissociation pattern. Values unchanged. |
| A | major | `followup_outputs` brain MRI | Served under `order_advanced_imaging` (`request_brain_mri`), with an MRA nothing asks for and em dashes (C9). | FIXED: moved to `analyze_brain_mri` (trigger `order_brain_mri_facial_nerves`). MRIReport has smooth bilateral labyrinthine/geniculate facial nerve enhancement (Kind 2) and no brainstem, mass or leptomeningeal lesion. MRA dropped. New recommended criterion `action-10-analyze-brain-mri`. `avoid-waste-3-analyze-brain-mri` removed. |
| A | minor | `followup_outputs` chest CT | Served under `order_ct_scan` (`request_chest_imaging`) (C9). | FIXED: moved to `order_body_imaging` (`request_chest_ct`, region chest, modality CT). New optional criterion `action-12-order-body-imaging-chest-ct` (sarcoidosis). |
| C | major | `ground_truth.action_criteria` | Lyme was a must ("Lyme serology and CSF analysis") but no criterion ordered it. | FIXED: recommended `action-11-interpret-labs-lyme` (`panels: ['Lyme_serology']`), served by a new negative Lyme ELISA follow-up. The must was removed (both acts are now criteria). |
| C | major | respiratory follow-up | "All values within normal limits" for FVC 68%, NIF "well above threshold", no MEP and no weight (C1). | FIXED: canonical format: FVC 3.0 L (68% predicted; 39 mL/kg at 76 kg) L, MIP -58 L, MEP 86 L, cough effective, measured with a face mask because of poor lip seal. No ICU trigger is met. |
| C | minor | telemetry follow-up | 48 h (C12). | FIXED: first 24 h with blood pressure range; a8 expected_evidence canonical. |
| A | major | `followup_outputs` | Empty literature (`search_gbs_treatment`) and DDI (`check_ivig_drug_interactions`) placeholders (C9). | FIXED: deleted. |
| D | major | `initial_tool_outputs.literature_search` | It echoed a5's expected_evidence with "guideline recommendation" and the bare `van_den_Berg_2014` (C11). | FIXED: population-keyed output on the variant and on the treatment indication [Wakerley_2014, EAN_PNS_2023]. a5 is optional and last. |
| C | major | criteria, sequence, stop rule | Template criteria: a1 required HIV, inflammatory markers and anti-GM1 IgM and expected trigger identification; a3 said "cells <10"; a5 and a6 were required with no medications. The constraints named the wrong criteria, the stop rule included literature and DDI with max 0, and citations were free text. | FIXED: plan 3.1 order (NCS, CSF, brain MRI, Lyme, labs, respiratory, telemetry, ECG, then optional chest CT, DDI, literature) with canonical texts. a6 is optional: no medications (DDI decision per plan 3.1 item 7). Constraints removed. Stop rule: the five required criteria, max 3. Citations are plan keys. a7 expected_evidence describes this normal ECG. |
| C | major | `ground_truth.assessment` | "Initiate IVIG / plasma exchange" did not meet the indication: he walks and runs (GBS disability score 1). There were no respiratory monitoring or ICU triggers, and the steroid prohibition was not the canonical one (C8). | FIXED: must 1 is a monitored bed with serial FVC/MIP/MEP (face mask), a swallow and cough check, and named ICU triggers (20 mL/kg is about 1.5 L at 76 kg). Must 2: IVIg or PE is not routinely advised while he walks and the weakness stays facial, and is started on progression [EAN_PNS_2023]. The eye-care must is made specific. Telemetry must kept. Prohibitions: canonical steroid text, renal function before IVIg. |
| C | major | `ground_truth.differential` | Lyme was moderate with no supporting finding. The sarcoid and MG reasons were generic or wrong ("Preserved reflexes"). The case's own mimics (MFS overlap, basal meningitis) were missing (C5). | FIXED: Lyme low (no exposure, serology negative, acellular CSF); neurosarcoidosis, bilateral Bell's, MFS overlap, basal meningeal process and MG very_low, each with case findings. Acute-onset CIDP low. |
| C | minor | `ground_truth.key_clinical_evidence` | Two generic pearls. | FIXED: five pearls (variant definition, CSF/NCS against the mimics, the facial diplegia work-up, ganglioside pearl, treatment indication). |
| C | minor | `ground_truth.red_herrings` | Empty, though the case contains a genuine distractor (C6). | FIXED: the GP's initial Bell's palsy diagnosis, resolved by the sequential bilateral palsy with paresthesias and hyporeflexia. |
| E | minor | `initial_tool_outputs.drug_interactions.warnings`, `metadata` | Taper boilerplate warning. The difficulty rationale said "6 required tools, 0 red herring(s)". | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing
GBS-RS11 is now a clean bifacial weakness with paresthesias variant. A 36-year-old man has 6 days of distal tingling, then a right and next-day left lower motor neuron facial palsy (first called Bell's palsy, now the red herring). His limbs are 5/5, reflexes are reduced (ankles absent), vibration is mildly reduced at the toes, and gait is normal. The CSF shows albuminocytological dissociation (78 mg/dL, 2 cells). The NCS shows bilateral facial neuropathy and a demyelinating limb pattern with sural sparing. Brain MRI shows only facial nerve enhancement, and Lyme serology and anti-GQ1b are negative. Respiratory function is reported with weight and a face mask, all flagged low, and no ICU trigger is met. Management is admission to a monitored bed with serial respiratory, swallow and cardiac monitoring and eye protection. IVIg or PE is held unless he progresses, as EAN/PNS 2023 advises for a mildly affected patient, and corticosteroids are prohibited. Antecedent-infection serology, the placeholder steps and the template criteria are gone. Brain MRI and Lyme serology are recommended criteria, and chest CT, the interaction check and literature are optional.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- `ground_truth.diagnosis.accepted[0]` changed (reviewer ruling c1f03f5c): "bilateral facial diplegia variant" became "bifacial weakness with paresthesias variant". Synonyms untouched.
- Plan CENTRAL 1 and 11: there is no `interpret_labs` term for anti-GQ1b IgG. The follow-up `request_anti_gq1b_gt1a_ganglioside_panel` is reachable when the call names "GQ1b" or "ganglioside", but no criterion scores it. In this case it would be optional at most.
- Plan CENTRAL 6: this variant case accepts "AIDP", "AMAN" and "miller fisher syndrome" through the code-level synonyms. "miller fisher syndrome" is wrong for a bifacial case without ophthalmoplegia or ataxia.
- Plan CENTRAL 5 (weight field).

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case.
- Note c1f03f5c: FIXED holds. Limbs 5/5 everywhere (motor, gait, neck), reflexes reduced (ankles absent, others 1+), paresthesias in HPI and sensory exam, mild toe vibration loss, no ataxia; label, KCE 1, differential and literature all name the bifacial weakness with paresthesias variant [Wakerley_2014]; Brighton correctly not applied.
- Note 22430160: FIXED holds. Ganglioside follow-up is GQ1b IgG negative only, interpreted in the differential (MFS overlap very_low) and KCE 4; probe confirms the follow-up is served when the call names GQ1b or ganglioside.
- Cross-checks clean: CSF/serum glucose 62/89 = 0.70; FVC 3.0 L at 76 kg = 39 mL/kg; ECG rate 88 = vitals; BMI 24.8 agrees; no ICU trigger met and must 1 names the triggers; IVIg withheld at GBS disability score 1 per EAN/PNS 2023; brain MRI and Lyme criteria served by their own follow-ups (perfect agent -v); literature and DDI outputs pass the leak guards.
- Found and fixed (minor, B): `patient.chief_complaint` said "after a week of tingling" while the HPI dates the tingling to 6 days ago and still present. Rewritten as "...; tingling in the fingers and feet for six days." No other change.
- perfect_agent.py GBS-RS11 -v passes; case_io.py check clean for the case.


## Condition audit (24 Oct 2026)
Condition auditor, after the worker and the verifier. Changes made through case_io; `perfect_agent.py` and `case_io.py check` re-run clean for all 30 GBS cases afterwards, and `test_case_guards.py -k GBS` passes.
- E, minor: `fallback_tool_outputs.drug_interactions.general.proposed` read "(agent not specified on this case's pathway)", an engineering note served to any off-pathway interaction check (PATTERNS 5). Now "Medication list review", as in S01-S03 and RS18.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels plus "bifacial weakness with paraesthesias/paresthesias"; AIDP, AMAN and Miller Fisher labels removed.
- Escalation must: "MIP becomes weaker than -30 cmH2O" -> "-40 cmH2O" (EAN/PNS 2023 MIP <40).
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Central vocabulary wired (24 Oct 2026)
Terms added in commit e19131d6 (`interpret_labs` `anti_GQ1b_IgG`, `anti_GT1a_IgG`, `botulinum_toxin_assay`; `analyze_csf` `CMV_PCR`), wired per plan C2/C3/C9 and GBS-decisions CENTRAL 1-3. Checks after the change: `perfect_agent.py -v` pass, `case_io.py check` clean for this case, `test_case_guards -k GBS-` 60 passed; optional criteria probed against the MockServer (served the case's own report, not a fallback).

- New `action-13-interpret-labs-anti-gq1b` (optional; `{panels: [anti_GQ1b_IgG]}`), after Lyme serology, answered by `request_anti_gq1b_gt1a_ganglioside_panel` (GQ1b negative). Optional: no ophthalmoplegia or ataxia, so EAN/PNS 2023 does not advise it; the criterion keeps the order from counting as unjustified. Closes CENTRAL 1 for this case.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- follow-up `request_cardiac_monitoring`: `monitor_type` "Continuous telemetry" -> `telemetry`.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
