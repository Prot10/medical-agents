# MG-S03
Reviewer status: none (MG not reviewed in this round; July 2026 tool review only) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: no reviewer notes for this case | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | blocker | `initial_tool_outputs.literature_search` | Any-query literature output repeating the literature criterion's `expected_evidence` (leak guard failing, plan B). | FIXED: literature criterion and output deleted (S-case default); the "no applicable evidence" literature fallback set to null (library answers); `fallback_tool_kinds.literature_search` removed. Guard passes. |
| D | major | `patient.neurological_exam.additional` | "NIF -54 cmH2O" and "Anti-titin ordered as part of initial workup" in the patient block (plan K). | FIXED: both deleted. |
| D | minor | `patient.history_present_illness` | "levothyroxine is adequate (TSH 1.4)": prior TSH value while TSH is scored. | FIXED: "he takes levothyroxine for hypothyroidism"; HbA1c (not scored) kept. |
| C | minor | `patient.neurological_exam.cranial_nerves` | Ptosis given as levator excursion. | FIXED: MRD1 right 2 mm, left 4 mm. |
| B | minor | `patient.physical_exam` (absent) | No weight for the respiratory mL/kg value. | FIXED: physical exam added (weight 88.1 kg, height 178 cm matching BMI 27.8; cardiovascular, respiratory, abdomen). |
| A | major | `initial_tool_outputs.ct`, `followup_outputs[request_thymectomy_evaluation]` | Chest CT stored in the head-CT slot, with a second chest CT report in a body-imaging follow-up (plan H3). | FIXED: one `initial_tool_outputs.body_imaging` report (region "chest, anterior mediastinum", contrast): encapsulated 3.6 x 2.9 x 3.1 cm mass, most consistent with thymoma, thymic carcinoma not excluded; `initial_tool_outputs.ct` null; follow-up deleted. A mediastinal MRI follow-up added so the accepted `mediastinum_MRI` alternative returns the mass instead of a library normal report. |
| B | major | `initial_tool_outputs.labs` | CBC and BMP "Normal"; two laboratories; MuSK in an AChR-positive patient; anti-titin row (not orderable, plan CENTRAL 7); HbA1c 6.9% flagged normal against "< 7.0". | FIXED: analytes with values incl. creatinine and eGFR (metformin, contrast), fasting glucose 128 (H), HbA1c 6.9% (H against the diagnostic range < 5.7), free T4; one laboratory (AChR <= 0.02 nmol/L); MuSK and titin removed. |
| C | minor | `initial_tool_outputs.specialized_test` | "Post-exercise facilitation followed by exhaustion" (the LEMS term used for repair of the decrement); no technique or CMAP values. | FIXED: structured report: technique, baseline CMAPs, unchanged decrements (deltoid 16%, nasalis 19%, masseter 21%), post-exercise deltoid 6% (no facilitation) with repair and exhaustion, normal NCS including peroneal and sural. |
| C | major | ice pack (no criterion, no report; `metadata.actions_withdrawn`) | Fatigable right ptosis without the recommended ice pack test (plan 3.5). | FIXED: recommended criterion and report (right MRD1 2.0 to 4.5 mm); `actions_withdrawn` removed. |
| C | major | `followup_outputs[request_ivig_preop]` | Pre-IVIG labs as a diagnostic step (treatment disguised as a test, plan J). | FIXED: deleted; pre-operative IVIG or PLEX is a must. |
| C | major | `followup_outputs[request_diabetes_management_steroids]`, `[request_metoprolol_interaction_pyridostigmine]` | Steroid-diabetes "interaction check" with a treatment plan; metoprolol check only about bradycardia, omitting the beta-blocker caution in MG (plan C, fact 22). | FIXED: both deleted and replaced by one `initial_tool_outputs.drug_interactions.pyridostigmine` in checker voice (pyridostigmine-metoprolol bradycardia; beta-blocker caution in MG; prednisone-metformin hyperglycaemia; levothyroxine none; prednisone-aspirin GI bleeding; metformin and contrast at eGFR 92). Glucose management is also a must. |
| A | major | `ground_truth.action_criteria` | Template criteria (labs with MuSK/LRP4, generic pyridostigmine check with telithromycin required, literature recommended, labels equal to rationales, `[Wolfe_2016]` everywhere) (plan A, N). | FIXED: labs `[anti_AChR, TSH]` required; RNS required; SFEMG optional; ice pack recommended; mediastinal imaging required (alternatives mediastinum_MRI, chest_CT, all served by the case's reports); respiratory recommended; drug check recommended with `{}` arguments (metoprolol and metformin, plan 3.2); literature removed. |
| B | minor | `ground_truth.sequence_constraints`, `stop_rule` | `labs -> RNS` with an SFEMG reason; drug check required before assessment; `max_additional_actions: 0`. | FIXED: `RNS -> SFEMG` and `labs -> SFEMG` soft; stop rule labs, RNS, imaging; `max_additional_actions: 1`. |
| C | major | `ground_truth.assessment.required_recommendations` | Diagnostic musts (confirm AChR, anti-titin, CT, respiratory and cardiac assessment); no pyridostigmine or steroid plan; beta-blocker not addressed. | FIXED: thymectomy for the thymoma; pre-operative IVIG 2 g/kg (about 175 g) or PLEX with anaesthetic NMB caution; pyridostigmine with heart-rate monitoring; low-dose prednisone escalation and azathioprine after TPMT; glucose monitoring and escalation; metoprolol review; drug list. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Seven template prohibitions incl. telithromycin. | FIXED: canonical three (attribution to diabetic cranial neuropathy or functional cause). |
| B | major | `ground_truth.differential`, `ground_truth.red_herrings[0].correct_interpretation` | Diabetic neuropathy entry said the presentation is "bilateral" (it is a right ptosis with right abduction deficit); LEMS "anti-VGCC negative" (never tested); cervical myelopathy "no cord disease on imaging" (no spine imaging, and myelopathy does not cause ptosis); no thymic carcinoma entry despite a 3.6 cm mass (ruling 7). | FIXED: diabetic cranial neuropathy rewritten from the case data; LEMS from RNS and exam; cervical myelopathy removed; brainstem stroke cites the prior MRI; thymic carcinoma added (low); the red herring interpretation rewritten the same way (fixed, fatigable, AChR-positive). |
| C | minor | `ground_truth.key_clinical_evidence` | Template bullets incl. anti-titin "non-negotiable" (titin no longer in the case), telithromycin, "All confirmed MG require CT chest". | FIXED: six case-specific bullets. |
| E | minor | `ground_truth.avoided_actions[*]` | `[Wolfe_2016]` citations; brain MRI rationale ignored the prior MRI. | FIXED: emptied; case rationales with Jacob 2025 in text. |
| B | minor | `fallback_tool_outputs.mri` | A brain MRI order returned a pineal cyst with no white matter change, contradicting the prior MRI in the HPI ("mild white matter changes, age-appropriate"). | FIXED: fallback reports few punctate white matter hyperintensities (Fazekas 1), normal brainstem, cavernous sinuses and orbits. |
| E | minor | `metadata` | Difficulty rationale, revision fields. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 62-year-old man with hypertension on metoprolol, type 2 diabetes on metformin and treated hypothyroidism, with generalized AChR-positive MG (IIb) and a 3.6 cm thymoma. The work-up is AChR antibody with thyroid function (one report with values; MuSK and titin removed; HbA1c and fasting glucose flagged), RNS with technique and brief-exercise testing (decrements unchanged), an ice pack test of the right ptosis, contrast CT of the chest and mediastinum (moved out of the head-CT slot; mass most consistent with thymoma), an optional mediastinal MRI that agrees with it, respiratory staging with weight-based values (MIP and MEP mildly reduced, FVC 41 mL/kg), and a recommended drug check that now covers the beta-blocker caution in MG, bradycardia with pyridostigmine and steroid hyperglycaemia. Literature is no longer a criterion. The patient block no longer quotes the NIF, the TSH or a titin order. Musts: thymectomy, pre-operative IVIG or PLEX for bulbar weakness, pyridostigmine with heart-rate monitoring, low-dose prednisone escalation with azathioprine after TPMT if needed, glucose management, metoprolol review, drug counselling. The differential gains thymic carcinoma (low) and loses cervical myelopathy.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 1: `[Jacob_2025]`, `[Evoli_2019]`, `[Lawn_2001]` in text only.
- Plan CENTRAL 2: `icd_codes[0]` G70.01 for a stable new diagnosis (G70.00 fits). Not changed.
- Plan CENTRAL 3: synonyms accept "ocular myasthenia gravis" for this generalized case.
- Plan CENTRAL 7: anti-titin removed from the stored labs (not orderable); titin was positive in the original case, a thymoma marker of no consequence once the CT shows the thymoma.

## Open questions for Andrea (judgment calls you could not settle)

- None. Pre-operative IVIG or PLEX is a must because of chewing fatigue, nasal speech, dysphagia and a reduced MIP (Sanders 2016).

## Verification

Adversarial check, 24 Oct 2026. Read the log, the full diff and the final case. Confirmed: NIF, TSH and the titin order gone from the patient block; right abduction deficit with right-gaze diplopia consistent; chest CT moved to body imaging; MRI follow-up served for mediastinum_MRI and concordant with the CT; BMI 27.8 and FVC 41 mL/kg recomputed; IVIG about 175 g at 88.1 kg; drug output agrees with the medication list (metoprolol caution, bradycardia, steroid hyperglycaemia, aspirin GI risk, metformin with contrast at eGFR 92); brain MRI fallback agrees with the prior MRI in the HPI; thymic carcinoma added low; leak guard passes.

Found and fixed:
- D/B major: `fallback_tool_outputs.advanced_imaging.modality` was the prose "FDG-PET scan" and its normal whole-body PET would contradict the 3.6 cm thymoma once routed. Replaced with an `FDG_PET` report of a moderately FDG-avid anterior mediastinal mass (SUVmax 3.9) without nodal or distant uptake; `fallback_tool_kinds.advanced_imaging` = `abnormal_consistent`.
- C minor: no thyroid antibodies although he has treated hypothyroidism (plan fact 3: antibodies when thyroid disease is known; July 2026 guidance: in all patients). Added anti-TPO 148 IU/mL (H) to the thyroid panel, the abnormal summary and the interpretation; the labs label and expected evidence now name thyroid antibodies; the hypothyroid myopathy entry notes the anti-TPO (treated Hashimoto thyroiditis). The required arguments are unchanged (`anti_AChR`, `TSH`).
- E minor: em dash in the rewritten `neurological_exam.cranial_nerves` sentence replaced by a comma.

perfect_agent passes; case_io check clean for this case.

## Condition audit (MG auditor, 24 Oct 2026)

- fallback_tool_outputs.echo.echo_type set to TTE. FIXED.
  Why: the discriminator guard (PATTERNS.md section 5) requires an exact vocabulary value on every case fallback; an empty echo_type answered every echo variant. The RS11-RS16 verifiers fixed this only in their own cases.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.

## Close-out (24 Oct 2026)

- `ground_truth.diagnosis.icd_codes[0]` G70.01 -> G70.00. ICD-10-CM G70.01 is myasthenia gravis with (acute) exacerbation, including crisis; this is a new or stable presentation, not an exacerbation. G70.01 stays accepted as a secondary code (plans/MG-decisions.md, Q2).
- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG']; icd_codes = ['G70.00', 'G70.0', 'G70.01']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
