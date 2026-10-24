# MG-S04
Reviewer status: none (MG not reviewed in this round; July 2026 tool review only) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: no reviewer notes for this case | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.additional` | The patient block named the diagnosis ("began researching myasthenia gravis", "requested MG workup") and gave the AChR result ("borderline positive") while AChR testing is the scored labs criterion (plan K). | FIXED: both sentences rewritten (she recognised the diurnal pattern; urgent referral); the exam note removed. |
| D | major | `patient.neurological_exam.additional` | "NIF -60 cmH2O" in the patient block while respiratory function is scored. | FIXED: deleted. |
| C | minor | `patient.neurological_exam.cranial_nerves`, `.motor` | Ptosis as levator excursion; no documented absence of rigidity although stiff-person syndrome is the case's red herring. | FIXED: MRD1 right 0.5 mm, left 3 mm; motor exam adds "No axial or limb rigidity, no spasms, normal startle". |
| B | minor | `patient.physical_exam` (absent) | No weight for the respiratory mL/kg value. | FIXED: physical exam added (weight 54.8 kg, height 160 cm matching BMI 21.4; insulin pump; no paraspinal rigidity). |
| A | major | `initial_tool_outputs.ct`, `followup_outputs[request_thymectomy_evaluation]` | Chest CT in the head-CT slot plus a "repeat" chest CT follow-up (plan H3). | FIXED: one `initial_tool_outputs.body_imaging` report (contrast, region "chest, anterior mediastinum": fatty involution, no thymoma); `initial_tool_outputs.ct` null; follow-up deleted. |
| B | major | `initial_tool_outputs.labs` | Two laboratories (AChR < 0.5, MuSK < 0.02); MuSK and anti-titin (not orderable) in an AChR-positive patient; HbA1c 6.6% flagged normal against "< 7.0" (a treatment target, not a reference range); no CBC/electrolytes. | FIXED: one laboratory (AChR binding <= 0.02 nmol/L); MuSK and titin removed; HbA1c flagged against < 5.7; CBC, BMP and free T4 added; anti-GAD65 kept (> 2000 IU/mL); interpretation hedged for GAD65. |
| C | major | `initial_tool_outputs.specialized_test` | Edrophonium test reported (plan fact 9); no technique or exercise testing. | FIXED: Tensilon removed; structured RNS with technique, CMAPs, unchanged decrements (deltoid 17%, nasalis 20%), post-exercise 3%, normal NCS. |
| C | major | ice pack (no criterion, no report; `metadata.actions_withdrawn`) | Fatigable bilateral ptosis without the recommended ice pack test (plan 3.5). | FIXED: recommended criterion and report (right MRD1 0.5 to 3.0 mm); `actions_withdrawn` removed. |
| C | major | `followup_outputs[request_insulin_pump_steroid_interaction]`, `[request_pyridostigmine_codeine_interaction]` | Steroid-insulin "interaction check" with a management plan; a codeine "interaction" with a drug nobody proposes (plan C). | FIXED: both deleted; one `initial_tool_outputs.drug_interactions.pyridostigmine` in checker voice (no pyridostigmine interaction; prednisone raises insulin need; avoid codeine; opioid caution); criterion optional. Glucose management is a must. |
| C | major | `followup_outputs[request_mgtx_thymectomy_planning]` | Literature output with "regardless of CT chest" and an unverified 2022 surgical citation. | FIXED: deleted with the literature criterion. |
| C | minor | `followup_outputs[request_respiratory_function]`, `[request_emg_single_fiber]` | Respiratory values without units, % predicted or mL/kg; NIF -60 against "> -60" called normal; SFEMG without muscle, blocking equal to jitter count. | FIXED: FVC 2.95 L (91%, 54 mL/kg), MIP -58, MEP 76 cmH2O, SBC 34; SFEMG orbicularis oculi 20 pairs, MCD 71 microseconds, jitter 16/20, blocking 7/20. |
| A | major | `ground_truth.action_criteria` | Template criteria (labs with MuSK/LRP4, literature and generic drug check required, labels equal to rationales, `[Wolfe_2016]` everywhere). | FIXED: labs `[anti_AChR, TSH]` required; RNS required; SFEMG optional; ice pack recommended; mediastinal imaging required (alternatives; the MRI alternative is answered by a library normal report, consistent with no thymoma); respiratory recommended; drug check optional `{}`; literature removed. |
| B | minor | `ground_truth.sequence_constraints`, `stop_rule` | `labs -> RNS` with an SFEMG reason; literature and drug check required; `max_additional_actions: 0`. | FIXED: `RNS -> SFEMG`, `labs -> SFEMG` soft; stop rule labs, RNS, imaging; `max_additional_actions: 1`. |
| C | major | `ground_truth.assessment.required_recommendations` | Diagnostic musts (confirm AChR, CT, "Single-fiber EMG given diagnostic clarity", "Investigate anti-GAD65"); no thymectomy or steroid plan (plan D). | FIXED: pyridostigmine titration; low-dose prednisone escalation, azathioprine after TPMT; insulin pump plan for steroid hyperglycaemia; elective thymectomy per MGTX (45, AChR+, no thymoma) with pre-operative IVIG/PLEX if bulbar weakness persists; no codeine, opioid caution; anti-GAD65 clinical reassessment; drug list. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Seven template prohibitions incl. telithromycin. | FIXED: canonical three (attribution to SPS, diabetic neuropathy or functional cause) plus "no codeine". |
| C | major | `ground_truth.red_herrings[0]`, `key_clinical_evidence[5]`, `differential[SPS]` | "Anti-GAD65 in this context most often relates to T1DM, not SPS" at a titre > 2000 IU/mL: very high titres are the range of GAD-associated neurological syndromes; the excluding point is the absent rigidity and spasms. | FIXED: all three rewritten with the titre nuance and the clinical exclusion. |
| C | minor | `ground_truth.differential` | Diabetic neuropathy and LEMS features thin. | FIXED from case data. |
| C | minor | `ground_truth.key_clinical_evidence[2..4]` | SFEMG ">95%", "All confirmed MG require CT chest", telithromycin. | FIXED. |
| E | minor | `ground_truth.avoided_actions[*]`, `metadata` | `[Wolfe_2016]` citations; revision fields. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 45-year-old pharmacist with type 1 diabetes on an insulin pump and generalized AChR-positive MG (IIb) without thymoma. The patient block no longer names MG or quotes an outside AChR result or the NIF, and now documents the absence of rigidity and spasms. The work-up is AChR antibody with thyroid function (one laboratory; anti-GAD65 > 2000 IU/mL kept as the red herring; HbA1c flagged correctly), RNS (decrement in deltoid and nasalis, no facilitation; Tensilon removed), an ice pack test of the right ptosis, contrast CT of the chest and mediastinum moved out of the head-CT slot (no thymoma), and respiratory staging with weight-based values (normal). SFEMG and the drug check are optional; literature is not a criterion. Musts: pyridostigmine titration, low-dose prednisone escalation with insulin pump adjustment, azathioprine after TPMT if needed, elective thymectomy per MGTX, no codeine, clinical reassessment for a GAD syndrome if rigidity or ataxia appear, drug counselling. The GAD65 red herring now states that the titre is in the neurological range but that SPS needs rigidity and spasms, which she does not have.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 1: `[Jacob_2025]`, `[Evoli_2019]`, `[Lawn_2001]` in text only.
- Plan CENTRAL 2: `icd_codes[0]` G70.01 for a stable new diagnosis (G70.00 fits). Not changed.
- Plan CENTRAL 3: synonyms accept "ocular myasthenia gravis" for this generalized case.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial check, 24 Oct 2026. Read the log, the full diff and the final case. Confirmed: the patient block no longer names MG, the outside AChR result or the NIF; absence of rigidity, spasms and startle documented in the exam; right adduction deficit with left-gaze diplopia consistent; BMI 21.4 and FVC 54 mL/kg recomputed; HbA1c flagged against < 5.7; anti-GAD65 red herring, differential and key evidence agree; codeine (documented intolerance) never prescribed and named in a prohibition; MGTX thymectomy must valid (45); leak guard passes.

Found and fixed:
- D minor: `fallback_tool_outputs.advanced_imaging.modality` was the prose "FDG-PET scan" (PATTERNS 5). Set to `FDG_PET` with a whole-body protocol (normal result consistent with no thymoma).
- B minor: `fallback_tool_outputs.ecg.rate` 86/min against a resting heart rate of 76 (the class the worker fixed in S01). Set to 78.
- C minor: no thyroid antibodies, although the labs rationale itself cites autoimmune thyroid disease clustering with MG and type 1 diabetes (July 2026 guidance: thyroid antibodies in all patients). Added anti-TPO 14 IU/mL (normal) to the thyroid panel, interpretation and expected evidence; required arguments unchanged.

perfect_agent passes; case_io check clean for this case.
